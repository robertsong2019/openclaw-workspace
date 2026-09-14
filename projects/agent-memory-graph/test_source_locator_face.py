"""Cycle 574 — source-locator face for speaker_recall.

A question citing a publication source ("...the study published in
the journal Music and Medicine that found...") is answered by the
passer that CONTAINS the cited name — the citation is the join
condition (C531/#086, question structure not tuned thresholds).
Without the face the generic study line wins on shared vocabulary
(0e5e2d1a official run: the 'Alternative Therapies' 15-subject
sentence out-scored the Music-and-Medicine 38-subject bearer 576.5
vs raw=8 on study/published/journal/subjects/medicine overlap —
both sentences sit in the SAME assistant message, session_24).

Shape mirrors C537/C534/C559: tier preference among passers only
(C536: a bearer the floors excluded stays excluded), fires only
when a best already exists (C559 precedent). Census: exactly 1 row
of the frozen 500 matches the question form.
"""

import unittest

from amg_bench_quality import (
    LongMemEvalAdapter,
    _SRC_LOC_Q_RE,
    _SRC_LOC_CUT_RE,
    _src_loc_name,
    answer_speaker_recall,
)

# ── verbatim real-row replica (0e5e2d1a, session_24) ──
PARASITE = ("In a study published in the journal Alternative Therapies "
            "in Health and Medicine, 15 subjects with anxiety and "
            "depression listened to binaural beats daily for four weeks.")
BEARER = ("Another study published in the journal Music and Medicine "
          "involved 38 subjects who listened to binaural beats for 30 "
          "minutes daily for three weeks.")
QUESTION = ("I wanted to follow up on our previous conversation about "
            "binaural beats for anxiety and depression. Can you remind "
            "me how many subjects were in the study published in the "
            "journal Music and Medicine that found significant "
            "reductions in symptoms of depression, anxiety, and stress?")


def _replica_nodes():
    """Both sentences in ONE assistant message, verbatim (session_24)
    inside a realistic pool: N=2 compresses shared-word IDF to 1.0
    and the flipped bearer lands under weighted_floor (production
    pools are hundreds of sentences, bearer ~200). Decoys are
    music/medicine-free so the tier stays exactly {bearer}."""
    decoys = (
        "I started a sourdough starter last week and it is finally "
        "bubbling on the counter.\n"
        "The hiking trail to the ridge takes about three hours "
        "round trip.\n"
        "For the bedroom repaint, choose a low-sheen paint so the "
        "walls are easier to clean.\n"
        "My allotment plot needs compost before the frost sets in.\n"
        "The ferry timetable can change twice a year, in spring and "
        "autumn.\n"
        "Practice the chord changes slowly with a metronome at 60 "
        "beats per minute.\n"
        "Mountain bikers need to check the brake pads after muddy "
        "rides.\n"
        "The allotment shed roof leaked, so I tarped it for the "
        "winter.\n"
        "Sourdough hydration levels change how open the crumb turns "
        "out.\n"
        "The ferry crossing takes forty minutes in calm weather.")
    return {
        "n1": {"label": "Have you heard about binaural beats for "
                        "anxiety and depression?",
               "role": "user", "session_id": "session_24"},
        "n2": {"label": PARASITE + "\n" + BEARER,
               "role": "assistant", "session_id": "session_24"},
        "n3": {"label": decoys, "role": "assistant",
               "session_id": "session_25"},
    }


def _parasite_only_nodes():
    return {
        "n2": {"label": PARASITE, "role": "assistant",
               "session_id": "session_24"},
    }


class TestSrcLocForm(unittest.TestCase):
    """Question-side detector: 'published in the <source> <Title>'."""

    def test_real_question_matches(self):
        m = _SRC_LOC_Q_RE.search(QUESTION)
        self.assertIsNotNone(m)

    def test_name_cut_at_that(self):
        name = _src_loc_name(QUESTION)
        self.assertEqual(name, ["music", "and", "medicine"])

    def test_title_and_kept_whole(self):
        # 'and' is a title word, not a clause boundary
        name = _src_loc_name(
            "What were the findings published in the journal Music and "
            "Medicine that reported mood effects?")
        self.assertEqual(name, ["music", "and", "medicine"])

    def test_name_cut_at_comma(self):
        name = _src_loc_name(
            "I loved the piece published in the magazine The New "
            "Yorker, which profiled the composer.")
        self.assertEqual(name, ["the", "new", "yorker"])

    def test_name_cut_at_reporting_verb(self):
        name = _src_loc_name(
            "What did the study published in the journal Nature "
            "Communications report about sleep?")
        self.assertEqual(name, ["nature", "communications"])

    def test_no_match_on_a_journal(self):
        # requires the definite article: 'published in a journal' is
        # generic, not a citation
        self.assertIsNone(_src_loc_name(
            "Have you ever published in a journal about sleep?"))

    def test_no_match_without_source_type(self):
        self.assertIsNone(_src_loc_name(
            "The results published in the study report were clear."))

    def test_no_match_on_plain_recall(self):
        self.assertIsNone(_src_loc_name(
            "Can you remind me of the back-end languages you "
            "recommended I learn?"))


class TestSrcLocFace(unittest.TestCase):
    """Candidate-side face: tier preference among passers."""

    def test_real_replica_rescues_bearer(self):
        ans, detail = answer_speaker_recall(QUESTION, _replica_nodes())
        self.assertIn("38 subjects", ans)
        self.assertNotIn("Alternative Therapies", ans)
        self.assertEqual(detail.get("src_loc_face"), "tier")

    def test_no_face_without_citation_form(self):
        q = ("Can you remind me how many subjects were in studies "
             "about binaural beats for anxiety and depression?")
        ans, detail = answer_speaker_recall(q, _replica_nodes())
        self.assertNotIn("src_loc_face", detail)

    def test_tier_empty_keeps_winner(self):
        # citation form but pool has no name-bearing passer: winner
        # unchanged, face never recorded
        ans, detail = answer_speaker_recall(QUESTION,
                                            _parasite_only_nodes())
        self.assertEqual(ans, PARASITE)
        self.assertNotIn("src_loc_face", detail)

    def test_winner_already_bearer_no_flip_no_key(self):
        # citing the PARASITE's journal: tier == {winner}, byte-stable
        q = ("Can you remind me how many subjects were in the study "
             "published in the journal Alternative Therapies in Health "
             "and Medicine that found reductions in anxiety?")
        ans, detail = answer_speaker_recall(q, _replica_nodes())
        self.assertEqual(ans, PARASITE)
        self.assertNotIn("src_loc_face", detail)

    def test_bearer_without_best_never_fires(self):
        # pool whose sentences can't clear the floors: unresolved ->
        # caller falls through; the face must not fabricate answers
        tiny = {"n2": {"label": "Music and Medicine.",
                       "role": "assistant", "session_id": "s1"}}
        ans, detail = answer_speaker_recall(QUESTION, tiny)
        self.assertIsNone(ans)
        self.assertNotIn("src_loc_face", detail)


class TestSrcLocAdapterWired(unittest.TestCase):
    """Gate-level pin: the wired path returns the bearer sentence."""

    def test_gate_speaker_recall_returns_bearer(self):
        a = LongMemEvalAdapter()
        nodes = _replica_nodes()
        msgs = [
            {"role": "user",
             "content": nodes["n1"]["label"]},
            {"role": "assistant",
             "content": nodes["n2"]["label"]},
            {"role": "assistant",
             "content": nodes["n3"]["label"]},
        ]
        a.ingest_sessions([{"messages": msgs}])
        ans, meta = a.answer_extractive(QUESTION)
        self.assertEqual(meta["gate"], "speaker_recall")
        self.assertIn("38 subjects", ans)
        self.assertEqual(meta["speaker_recall"].get("src_loc_face"),
                         "tier")

    def test_uncited_question_untouched(self):
        a = LongMemEvalAdapter()
        nodes = _replica_nodes()
        msgs = [
            {"role": "user",
             "content": nodes["n1"]["label"]},
            {"role": "assistant",
             "content": nodes["n2"]["label"]},
            {"role": "assistant",
             "content": nodes["n3"]["label"]},
        ]
        a.ingest_sessions([{"messages": msgs}])
        q = ("Can you remind me how many subjects were in studies "
             "about binaural beats for anxiety and depression?")
        ans, meta = a.answer_extractive(q)
        if meta.get("gate") == "speaker_recall":
            self.assertNotIn("src_loc_face",
                             meta.get("speaker_recall", {}))


if __name__ == "__main__":
    unittest.main()
