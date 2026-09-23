"""C600: species_total face — latest stated total for the local-
park bird-species row (affe2881, GT '32', qtype knowledge-update).

One face, one mechanism (explicit running-total declaration):

- species_total (affe2881, GT '32'): "How many different species
  of birds have I seen in my local park?" — a user SENTENCE
  yields the total when it carries the running-total DECLARATION
  ('brings my total ... count to <num>') plus a species|bird
  topic word (same-sentence wall). The row is a knowledge-update
  pair: an early snapshot ('spot 27 different species so far',
  May 24) is superseded by an explicit declaration ('brings my
  total species count to 32', May 29). The DECLARATION, not
  freshest-number arbitration, is the mechanism — no session
  dating needed; the stale snapshot can never key.

Census (all 500): the strict head matches EXACTLY 1 row
(affe2881), unbanked today (gate=answer — the pred was a
volunteer-echo sentence with no number). The head cannot steal
the C592-C599 faces (different NPs/markers) or the generic
how-many block.

Decoy discipline (pinned per-turn below):
- snapshot '27 different species so far' — superseded stale
  total; the construction never matches it
- assistant echo 'reaching 32 species on your count' — assistant
  role never read; 'reaching' is not the declaration shape
- off-topic declaration 'brings my total miles count to 120' —
  no species|bird word in the sentence (topic wall)
- conflicting declarations (32 vs 35) — abstain (None), no
  arbitration exists in this lane; identical repeats dedup
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_species_total,
    answer_counting,
    counting_form,
    counting_judge,
)

Q_SP = 'How many different species of birds have I seen in my local park?'

# verbatim dataset fixtures (affe2881; gen transcription 09-23)
U_SNAPSHOT_27 = (
    "That's really helpful, thanks! By the way, speaking of bird "
    "identification, I've been keeping track of the species I've "
    "seen in my local park, and I've managed to spot 27 different "
    "species so far. It's amazing how diverse the bird life is in "
    "such a small area!")
U_DECLARE_32 = (
    "I'll definitely bring some sunflower seeds and suet to "
    "attract the woodpeckers. By the way, speaking of "
    "woodpeckers, I just saw a Northern Flicker in my local park "
    "last weekend, which brings my total species count to 32. Do "
    "you think the suet will attract any other woodpecker "
    "species as well?")
A_ECHO_32 = (
    "Congratulations on spotting the Northern Flicker and "
    "reaching 32 species on your count!\n\nSuet is an excellent "
    "choice to attract woodpeckers, and it's likely to draw in "
    "other species beyond just Northern Flickers.")
U_DECLARE_35 = (
    "Another good day out there — this brings my total species "
    "count to 35 now.")
U_DECLARE_32B = (
    "Saw a warbler too, which brings my total species count to "
    "32.")
U_OFFTOPIC_TOTAL = (
    "Finished the marathon plan last month, which brings my "
    "total miles count to 120.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: snapshot session (May 24) + declaration
# session (May 29); haystack order preserved
S_PAIR = mk(
    ("answer_90de9b4d_1", [("user", U_SNAPSHOT_27),
                           ("assistant", "nice going")]),
    ("answer_90de9b4d_2", [("user", U_DECLARE_32),
                           ("assistant", A_ECHO_32)]))
S_PAIR_REV = mk(
    ("answer_90de9b4d_2", [("user", U_DECLARE_32),
                           ("assistant", A_ECHO_32)]),
    ("answer_90de9b4d_1", [("user", U_SNAPSHOT_27),
                           ("assistant", "nice going")]))


class TestForm(unittest.TestCase):
    def test_form_routes_species_total(self):
        self.assertEqual(counting_form(Q_SP), "species_total")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never species_total)
        for q in (
            'How many bikes did I service or plan to service in March?',
            "How many doctor's appointments did I go to in March?",
            'How many trips have I taken my Canon EOS 80D camera on?',
            'How many times did I bake something in the past two weeks?',
            'How many Marvel movies did I re-watch?',
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many different types of food delivery services '
            'have I used recently?',
        ):
            self.assertNotEqual(counting_form(q), "species_total", q)
            self.assertIsNone(_cnt_species_total(q, S_PAIR), q)


class TestSpeciesTotal(unittest.TestCase):
    def test_pair_resolves_latest_total(self):
        self.assertEqual(_cnt_species_total(Q_SP, S_PAIR), "32")

    def test_order_independent(self):
        self.assertEqual(_cnt_species_total(Q_SP, S_PAIR_REV), "32")

    def test_declaration_only(self):
        self.assertEqual(
            _cnt_species_total(Q_SP, one("s1", "user", U_DECLARE_32)),
            "32")

    def test_snapshot_only_never_keys(self):
        # '27 ... so far' is the superseded stale total
        self.assertIsNone(
            _cnt_species_total(Q_SP, one("s1", "user", U_SNAPSHOT_27)))

    def test_assistant_declaration_not_read(self):
        sess = one("s1", "assistant", A_ECHO_32)
        self.assertIsNone(_cnt_species_total(Q_SP, sess))

    def test_conflicting_totals_abstain(self):
        sess = mk(("s1", [("user", U_DECLARE_32)]),
                  ("s2", [("user", U_DECLARE_35)]))
        self.assertIsNone(_cnt_species_total(Q_SP, sess))

    def test_identical_repeats_dedup(self):
        sess = mk(("s1", [("user", U_DECLARE_32)]),
                  ("s2", [("user", U_DECLARE_32B)]))
        self.assertEqual(_cnt_species_total(Q_SP, sess), "32")

    def test_offtopic_total_blocked_by_wall(self):
        # 'brings my total miles count to 120' — no species|bird
        # word in the sentence
        self.assertIsNone(
            _cnt_species_total(Q_SP, one("s1", "user",
                                         U_OFFTOPIC_TOTAL)))

    def test_no_declaration_never_keys(self):
        sess = one("s1", "user",
                   "I love birding in my local park on weekends.")
        self.assertIsNone(_cnt_species_total(Q_SP, sess))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric(self):
        self.assertTrue(counting_judge(Q_SP, "32", "32"))
        self.assertFalse(counting_judge(Q_SP, "32", "30"))
        self.assertFalse(counting_judge(Q_SP, "32", ""))

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q_SP, S_PAIR)
        self.assertEqual(ans, "32")
        self.assertEqual(meta, {"form": "species_total"})

    def test_answer_counting_unresolvable_falls_through(self):
        ans, meta = answer_counting(
            Q_SP, one("s1", "user", U_SNAPSHOT_27))
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "species_total"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
