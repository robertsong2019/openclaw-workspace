"""Cycle 581 - sectioned-recall face (sectioned_recall gate).

"I remember you told me about the refining processes at CITGO's
three refineries earlier. Can you remind me what kind of processes
are used at the Lake Charles Refinery?" is answered by the
assistant's own SECTIONED list: the question names a section header
("N. Lake Charles Refinery:"), the face harvests that section's
bullet rows and renders their name spans (judge-normalized equality
with the GT, which is the bare span list itself).

Design notes:
- header match ONLY on section headers (rows of sibling sections
  mention "Lake Charles" - "As with the Lake Charles Refinery, this
  is the initial step" - and must never bind);
- all three sections are numbered "1." (GPT-4 numbering quirk), so
  the header regex does not assume increasing numbers;
- entity match must be unique (>=2 headers containing the entity =
  ambiguous = fall-through) and the section needs >=2 rows.

Census: frame ("remind me|you told me|i remember") + named demand
("what (kind of) <noun> are used at the <Capitalized Entity>")
accepts exactly 1/500 questions - zero hijack surface by
construction. The current parasitic pred is the speaker_recall intro
sentence (the three-location opener). Fixture message is a verbatim
copy of 6ae235be s34 (the CITGO answer).
"""

import unittest

from amg_bench_quality import (
    LongMemEvalAdapter,
    answer_sectioned_recall,
    judge_semantic,
    list_recall_form,
    sectioned_recall_form,
)

Q = ("I remember you told me about the refining processes "
     "at CITGO's three refineries earlier. Can you remind me what "
     "kind of processes are used at the Lake Charles Refinery?")
GT = ("Atmospheric distillation, fluid catalytic cracking (FCC), "
      "alkylation, and hydrotreating.")
PRED = ("Atmospheric distillation, Fluid catalytic cracking (FCC), "
        "Alkylation, and Hydrotreating.")

Q_LEMONT = ("I remember you told me about the refining processes "
            "at CITGO's three refineries earlier. Can you remind me "
            "what kind of processes are used at the Lemont "
            "Refinery?")
PRED_LEMONT = ("Atmospheric distillation, Delayed coking, "
               "Hydrocracking, and Hydrotreating.")

Q_ABSENT = ("I remember you told me about the refining processes "
            "at CITGO's refineries earlier. Can you remind me what "
            "kind of processes are used at the Port Arthur "
            "Refinery?")

CITGO_MSG = "CITGO operates three refineries in the United States, located in Lake Charles, Louisiana; Lemont, Illinois; and Corpus Christi, Texas. Each refinery has its own set of refining processes, but here are some of the main processes that go on at each facility:\n\n1. Lake Charles Refinery:\n* Atmospheric distillation: This is the first step in the refining process, where crude oil is heated and separated into different fractions based on their boiling points.\n* Fluid catalytic cracking (FCC): This process breaks down heavier fractions of crude oil into lighter, more valuable products such as gasoline and diesel fuel.\n* Alkylation: This process combines smaller molecules to form larger ones, creating high-octane gasoline components.\n* Hydrotreating: This process removes impurities from the gasoline and diesel fractions to improve their quality.\n1. Lemont Refinery:\n* Atmospheric distillation: As with the Lake Charles Refinery, this is the initial step in the refining process.\n* Delayed coking: This process breaks down heavy, residual oils into lighter products such as naphtha, diesel, and petroleum coke.\n* Hydrocracking: This process uses hydrogen and a catalyst to break down heavier fractions of crude oil into lighter, more valuable products.\n* Hydrotreating: This process is used to remove sulfur and other impurities from the gasoline and diesel fractions.\n1. Corpus Christi Refinery:\n* Atmospheric distillation: Again, this is the first step in the refining process.\n* Fluid catalytic cracking (FCC): As with the Lake Charles Refinery, this process is used to break down heavier fractions of crude oil into lighter, more valuable products.\n* Alkylation: This process combines smaller molecules to form larger ones, creating high-octane gasoline components.\n* Hydrocracking: This process is used to break down heavier fractions of crude oil into lighter, more valuable products.\n* Hydrotreating: This process removes impurities from the gasoline and diesel fractions to improve their quality.\n\nIt's worth noting that these are just some of the processes that take place at each refinery, and there may be others as well. Additionally, the specific refining processes used can vary depending on the type of crude oil being processed and the market demand for different petroleum products."


def _pool(*msgs):
    """[(role, content)] full-graph wire format (date-independent)."""
    return list(msgs)


class SectionedRecallFormTests(unittest.TestCase):
    def test_form_accepts_target(self):
        self.assertEqual(sectioned_recall_form(Q),
                         ("processes", "Lake Charles Refinery"))

    def test_form_accepts_lemont_variant(self):
        # family honesty: same frame, different named section
        self.assertEqual(sectioned_recall_form(Q_LEMONT),
                         ("processes", "Lemont Refinery"))

    def test_form_rejects_no_recall_frame(self):
        self.assertIsNone(sectioned_recall_form(
            "What kind of processes are used at the Lake Charles "
            "Refinery?"))

    def test_form_rejects_no_named_demand(self):
        # frame without the "what ... at the <Name>" clause
        self.assertIsNone(sectioned_recall_form(
            "I remember you told me about the refining processes "
            "at CITGO's three refineries earlier."))

    def test_form_rejects_uncapitalized_entity(self):
        self.assertIsNone(sectioned_recall_form(
            "Can you remind me what kind of processes are used at "
            "the refinery?"))

    def test_disjoint_from_list_recall(self):
        # interlock with C578: the named-refinery question must stay
        # out of the cardinal list face (pinned there too)
        self.assertIsNone(list_recall_form(Q))
        self.assertIsNotNone(sectioned_recall_form(Q))


class SectionedRecallAnswerTests(unittest.TestCase):
    def test_lake_charles_rescued(self):
        pool = _pool(("assistant", CITGO_MSG))
        ans, detail = answer_sectioned_recall(Q, pool)
        self.assertEqual(ans, PRED)
        self.assertEqual(detail["form"], "sectioned_recall")
        self.assertEqual(detail["header"], "Lake Charles Refinery")
        self.assertEqual(detail["spans"],
                         ["Atmospheric distillation",
                          "Fluid catalytic cracking (FCC)",
                          "Alkylation", "Hydrotreating"])

    def test_lemont_section_selected(self):
        pool = _pool(("assistant", CITGO_MSG))
        ans, detail = answer_sectioned_recall(Q_LEMONT, pool)
        self.assertEqual(ans, PRED_LEMONT)
        self.assertEqual(detail["header"], "Lemont Refinery")

    def test_absent_entity_falls_through(self):
        pool = _pool(("assistant", CITGO_MSG))
        ans, detail = answer_sectioned_recall(Q_ABSENT, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_section")

    def test_user_role_wall(self):
        pool = _pool(("user", CITGO_MSG))
        ans, _ = answer_sectioned_recall(Q, pool)
        self.assertIsNone(ans)

    def test_ambiguous_duplicate_header_falls_through(self):
        pool = _pool(("assistant", CITGO_MSG),
                     ("assistant", CITGO_MSG))
        ans, detail = answer_sectioned_recall(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "ambiguous")

    def test_single_row_section_not_a_list(self):
        one = ("1. Tiny Refinery:\n* Distillation: first step.")
        pool = _pool(("assistant", one))
        ans, detail = answer_sectioned_recall(
            "I remember you told me earlier. Can you remind me what "
            "kind of processes are used at the Tiny Refinery?", pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "single_row")


class SectionedRecallJudgePins(unittest.TestCase):
    """Pre-verified render -> judge contracts (frozen)."""

    def test_render_normalized_equal(self):
        # GT is the bare span list modulo capitalization
        self.assertEqual(judge_semantic(Q, PRED, GT), "CORRECT")

    def test_intro_stays_unbanked(self):
        # the parasitic speaker_recall opener must never bank
        intro = ("CITGO operates three refineries in the United "
                 "States, located in Lake Charles, Louisiana; "
                 "Lemont, Illinois; and Corpus Christi, Texas.")
        self.assertEqual(judge_semantic(Q, intro, GT), "NEEDS_JUDGE")


class SectionedRecallAdapterTests(unittest.TestCase):
    def test_adapter_gate_wired(self):
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "user", "content":
                      "give me the refining processes that go on at "
                      "3 CITGO Refineries"},
                  {"role": "assistant", "content": CITGO_MSG}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertEqual(ans, PRED)
        self.assertEqual(meta.get("gate"), "sectioned_recall")

    def test_adapter_flag_off_falls_through(self):
        ad = LongMemEvalAdapter(sectioned_recall=False)
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "assistant", "content": CITGO_MSG}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertNotEqual(meta.get("gate"), "sectioned_recall")


if __name__ == "__main__":
    unittest.main()
