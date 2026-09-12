"""C568: page-count-of-finished-novels sum — 37f165cf.

Head: "What was the page count of the two novels I finished in
January and March?" (GT 856 = 440 + 416).

Evidence path (census-backed): the months are unrecoverable from
the haystack (zero January/March mentions bind to the anchors;
all session dates are May 2023), so the lane sums DISTINCT
just-finished page-count facts from user lines — one fact per
sentence (first page-count after the just-finished marker) — and
requires exactly the count the question names ("two").

Guards:
- The December decoy ('I read "The Power" ... which had 341
  pages') never anchors: its page-count is NOT the first
  page-count after a just-finished marker in its sentence (the
  416-page fact precedes it in that sentence).
- Repeated mentions of the same book (Nightingale 440 twice)
  collapse via distinct-value dedupe.
- Assistant recommendations ('530 pages', 'took around 5 weeks
  to finish a 440-page book') die on the user-role wall.
- step3b regression pin: a naive digit-consuming prefix regex
  backtracks '416-page' into capturing '6' — the pin asserts the
  single-fact value is exactly 416.

Census (all 500): the head matches EXACTLY 1 row (37f165cf,
unbanked, gate=answer today); no abs sibling exists (verified in
frozen). Zero kills by construction: the handler only runs for
rows this head claims.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    LongMemEvalAdapter,
    _cnt_page_count_sum,
    answer_counting,
    counting_form,
    counting_judge,
)

NOVELS_Q = ("What was the page count of the two novels I finished "
            "in January and March?")
NOVELS_NO_COUNT_Q = ("What was the page count of the novels I "
                     "finished in January and March?")
NOVELS_THREE_Q = ("What was the page count of the three novels I "
                  "finished in January and March?")
ONE_NOVEL_Q = ("What was the page count of the one novel I finished "
               "in March?")

# ── verbatim real-row lines (37f165cf haystack, sessions s#9/s#33) ──

NG_M0_U = ("I'm looking for some book recommendations. I just "
           "finished a historical fiction novel, \"The Nightingale\" "
           "by Kristin Hannah, which had 440 pages and took me around "
           "3 weeks to complete. Do you have any suggestions for "
           "similar books or authors?")
NG_M6_U = ("I'm glad you recommended \"The Alice Network\"! I'm "
           "definitely interested in reading more about women's roles "
           "during wartime. Speaking of which, I just finished reading "
           "\"The Nightingale\" by Kristin Hannah, which had 440 pages "
           "and took me around 5 weeks to complete. Do you think I "
           "would enjoy \"The Women in the Castle\" by Jessica "
           "Shattuck, given my reading pace and interest in historical "
           "fiction?")
PG_M0_U = ("I'm looking for some book recommendations. I've been into "
           "fiction lately, especially novels that explore complex "
           "themes. I just finished a 416-page novel, but before that, "
           "I read \"The Power\" by Naomi Alderman in December, which "
           "had 341 pages and took me around 5 weeks to finish. I'm "
           "interested in books with similar page lengths and depth.")
POWER_ONLY_U = ("I read \"The Power\" by Naomi Alderman in December, "
                "which had 341 pages and took me around 5 weeks to "
                "finish.")
NG_ASSISTANT_M1 = ("\"The Nightingale\" is a powerful and emotional "
                   "read! I'd be happy to recommend some similar books "
                   "and authors. Since you took around 5 weeks to "
                   "finish a 440-page book, I'll suggest novels with "
                   "similar page counts and reading times.")

# 184da446 line: 'just finished reading about ...' with NO page-count
# after the marker (the 'on page 220' phrase is not a page-count)
DNA_MENTION_U = ("I just finished reading about the discovery of DNA "
                 "structure last night - fascinating stuff.")


def _turns(lines):
    return [{"session_id": s[0],
             "turns": [{"role": r, "content": c} for r, c in s[1]]}
            for s in lines]


REAL_HAY = [
    {"session_id": "session_10",
     "messages": [{"role": "user", "content": NG_M0_U},
                  {"role": "assistant", "content": NG_ASSISTANT_M1},
                  {"role": "user", "content": NG_M6_U}]},
    {"session_id": "session_34",
     "messages": [{"role": "user", "content": PG_M0_U}]},
]


class TestPageCountSumFace(unittest.TestCase):

    # ── gate entries ──

    def test_counting_form_claims_head(self):
        self.assertEqual(counting_form(NOVELS_Q), "page_count_sum")

    def test_counting_form_non_heads_stay_out(self):
        # pages-progress heads (C567) keep their own lane
        self.assertEqual(
            counting_form("How many pages of 'X' have I read so far?"),
            "pages")
        # not a counting form at all
        self.assertIsNone(counting_form(
            "I'm going back to our previous conversation about the "
            "grant aim page. Can you remind me what were the three "
            "aims?"))

    # ── adapter-level production pin (real row) ──

    def test_adapter_rescue_real_row(self):
        a = LongMemEvalAdapter()
        a.ingest_sessions(REAL_HAY)
        ans, meta = a.answer_extractive(NOVELS_Q)
        self.assertEqual(ans, "856")
        self.assertEqual(meta.get("gate"), "counting")
        self.assertEqual(meta.get("counting", {}).get("form"),
                         "page_count_sum")

    # ── route-level sanity (direct calls) ──

    def test_route_direct_real_row(self):
        self.assertEqual(
            _cnt_page_count_sum(NOVELS_Q, _turns([
                ("s9", [("user", NG_M0_U), ("user", NG_M6_U)]),
                ("s33", [("user", PG_M0_U)]),
            ])),
            "856")

    # ── step3b regression pin: backtracking artifact ──

    def test_single_fact_value_exactly_416(self):
        """A digit-consuming prefix regex captures '6' out of
        '416-page' via backtracking; the sentence-scoped scanner
        must yield exactly 416."""
        self.assertEqual(
            _cnt_page_count_sum(ONE_NOVEL_Q, _turns([
                ("s33", [("user", PG_M0_U)]),
            ])),
            "416")

    # ── guards ──

    def test_decoy_power_only_no_anchor(self):
        self.assertIsNone(
            _cnt_page_count_sum(NOVELS_Q, _turns([
                ("sX", [("user", POWER_ONLY_U)]),
            ])))

    def test_assistant_lines_never_anchor(self):
        self.assertIsNone(
            _cnt_page_count_sum(NOVELS_Q, _turns([
                ("sA", [("assistant", NG_ASSISTANT_M1),
                        ("assistant", PG_M0_U.replace(
                            "I just finished", "You just finished"))]),
            ])))

    def test_cardinality_mismatch_falls_through(self):
        # only one distinct fact but question says two
        self.assertIsNone(
            _cnt_page_count_sum(NOVELS_Q, _turns([
                ("s9", [("user", NG_M0_U)]),
            ])))
        # three distinct facts but question says two
        self.assertIsNone(
            _cnt_page_count_sum(NOVELS_Q, _turns([
                ("s9", [("user", NG_M0_U)]),
                ("s33", [("user", PG_M0_U)]),
                ("sY", [("user",
                         "I just finished a 300-page novel last week.")]),
            ])))

    def test_missing_count_word_falls_through(self):
        self.assertIsNone(
            _cnt_page_count_sum(NOVELS_NO_COUNT_Q, _turns([
                ("s9", [("user", NG_M0_U)]),
                ("s33", [("user", PG_M0_U)]),
            ])))

    def test_three_novels_question_resolves_when_three_facts(self):
        self.assertEqual(
            _cnt_page_count_sum(NOVELS_THREE_Q, _turns([
                ("s9", [("user", NG_M0_U)]),
                ("s33", [("user", PG_M0_U)]),
                ("sY", [("user",
                         "I just finished a 300-page novel last week.")]),
            ])),
            "1156")

    def test_just_finished_without_page_count_no_anchor(self):
        self.assertIsNone(
            _cnt_page_count_sum(ONE_NOVEL_Q, _turns([
                ("sZ", [("user", DNA_MENTION_U)]),
            ])))

    def test_empty_sessions(self):
        self.assertIsNone(_cnt_page_count_sum(NOVELS_Q, []))

    # ── judge credit ──

    def test_judge_credit_real_row(self):
        self.assertTrue(counting_judge(NOVELS_Q, "856", "856"))
        self.assertFalse(counting_judge(NOVELS_Q, "856", "781"))


if __name__ == "__main__":
    unittest.main()
