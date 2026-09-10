"""C565: two pp-neighbor faces — have-had possession tenure +
finish-duration sum.

Face A — e61a7584 "How long have I had my cat, Luna?" (GT '9
months'): _PP_HEAD_RE matches, but both entry predicates miss
(pp_duration_form needs when/before; pp_pure_tenure_form needs
"been"), so the row fell to the answer gate (garbage pred).
Route (c)'s clause-strip + all-keywords wall + now-suffixed
tenure machinery ALREADY answers it once the gate claims the
question: s17 "I've had Luna for about 6 months now" (no "cat")
fails the [cat, luna] wall; s32 "I've had my cat, Luna, for
about 9 months now" passes → "9 months". Census (all 500):
head "how long (have|had) (i|we) had" = exactly 1 row, unbanked.

Face B — b9cfe692 "How long did I take to finish 'The Seven
Husbands of Evelyn Hugo' and 'The Nightingale' combined?" (GT
'5.5 weeks'): new route — sum of per-entity "took me N units to
finish" anchors, each line bound to a question title word,
both-facts guard (>=2 anchors), honest fall-through otherwise.
Census (all 500): head "how long did (i|we) take to finish" =
exactly 1 row, unbanked; evidence s10 "took me three weeks to
finish" (Nightingale) + s12 "took me two and a half weeks to
finish" (Evelyn Hugo) = 3 + 2.5 = 5.5 weeks.
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
    answer_pp_duration,
    pp_duration_judge,
    pp_pure_tenure_form,
)

# ── real-row evidence (verbatim haystack lines; C562 lesson) ──

CAT_Q = "How long have I had my cat, Luna?"

CAT_HAY = [
    {"session_id": "session_1",
     "messages": [
         {"role": "user", "content": (
             "I'm trying to keep my cat, Luna, healthy and happy. "
             "Can you give me some general tips on how to maintain "
             "her weight?")},
         {"role": "user", "content": (
             "I've had Luna for about 6 months now, and I've been "
             "meaning to get her microchipped for a while. I've "
             "heard horror stories about pets getting lost, and I "
             "don't want to take any chances.")},
     ]},
    {"session_id": "session_2",
     "messages": [
         {"role": "user", "content": (
             "I've had my cat, Luna, for about 9 months now, and "
             "I've been trying to keep her active and engaged. "
             "I've set up her cat tree, and she loves climbing up "
             "and down it.")},
     ]},
]

CAT_DATES = {"session_1": "2023-07-01", "session_2": "2023-10-01"}

FINISH_Q = ("How long did I take to finish 'The Seven Husbands "
            "of Evelyn Hugo' and 'The Nightingale' combined?")

FINISH_HAY = [
    {"session_id": "session_1",
     "messages": [
         {"role": "user", "content": (
             "I'm looking for some book recommendations. I "
             "recently finished \"The Nightingale\" by Kristin "
             "Hannah, which took me three weeks to finish - it "
             "was a really emotional and heavy read, but I loved "
             "it. Can you suggest some historical fiction books "
             "that have a similar tone?")},
     ]},
    {"session_id": "session_2",
     "messages": [
         {"role": "user", "content": (
             "I'm looking for some new audiobook recommendations. "
             "I've been enjoying listening to them during my daily "
             "commute and I just finished \"The Seven Husbands of "
             "Evelyn Hugo\", which took me two and a half weeks to "
             "finish. Do you have any suggestions for similar "
             "books?")},
     ]},
]

FINISH_DATES = {"session_1": "2023-05-24", "session_2": "2023-06-10"}


def _adapter_answer(hay, dates, q):
    a = LongMemEvalAdapter()
    a.ingest_sessions(hay, session_dates=dates)
    return a.answer_extractive(q)


class TestHaveHadFace(unittest.TestCase):

    def test_gate_entry_rescues_cat_row(self):
        """Adapter level: the gate must claim have-had heads."""
        ans, meta = _adapter_answer(CAT_HAY, CAT_DATES, CAT_Q)
        self.assertEqual(ans, "9 months")
        self.assertEqual(meta.get("gate"), "pp_duration")

    def test_route_direct_sanity_pure_tenure(self):
        """Route (c) already answers the question once claimed."""
        dated = [(CAT_DATES[s["session_id"]], s["messages"])
                 for s in CAT_HAY]
        ans, detail = answer_pp_duration(CAT_Q, dated)
        self.assertEqual(ans, "9 months")
        self.assertEqual(detail.get("route"), "pure_tenure")

    def test_form_predicate(self):
        from amg_bench_quality import pp_have_had_form
        self.assertTrue(pp_have_had_form(CAT_Q))
        self.assertTrue(pp_have_had_form(
            "How long had we had the lake house?"))
        # been-form belongs to pure tenure, did-form to finish-sum
        self.assertFalse(pp_have_had_form(
            "How long have I been working in my current role?"))
        self.assertFalse(pp_have_had_form(FINISH_Q))
        # when/before siblings stay with route (b)
        self.assertFalse(pp_have_had_form(
            "How long have I had my cat when I adopted her?"))

    def test_no_matching_line_falls_through(self):
        """No all-keywords tenure line → None (gate chain owns it)."""
        hay = [{"session_id": "session_1",
                "messages": [
                    {"role": "user", "content": (
                        "I've had a busy week at work and I'm "
                        "looking forward to the weekend.")},
                ]}]
        dated = [("2023-07-01", hay[0]["messages"])]
        ans, detail = answer_pp_duration(CAT_Q, dated)
        self.assertIsNone(ans)

    def test_pure_tenure_entry_unchanged(self):
        """Been-form heads still route via pure tenure (pin)."""
        self.assertTrue(pp_pure_tenure_form(
            "How long have I been working in my current role?"))
        self.assertFalse(pp_pure_tenure_form(CAT_Q))


class TestFinishSumFace(unittest.TestCase):

    def test_gate_entry_rescues_finish_row(self):
        """Adapter level: combined-finish heads route to pp gate."""
        ans, meta = _adapter_answer(
            FINISH_HAY, FINISH_DATES, FINISH_Q)
        self.assertEqual(ans, "5.5 weeks")
        self.assertEqual(meta.get("gate"), "pp_duration")

    def test_route_direct_rescue(self):
        dated = [(FINISH_DATES[s["session_id"]], s["messages"])
                 for s in FINISH_HAY]
        ans, detail = answer_pp_duration(FINISH_Q, dated)
        self.assertEqual(ans, "5.5 weeks")
        self.assertEqual(detail.get("route"), "finish_sum")
        self.assertEqual(detail.get("anchors"), 2)

    def test_form_predicate(self):
        from amg_bench_quality import pp_finish_sum_form
        self.assertTrue(pp_finish_sum_form(FINISH_Q))
        self.assertTrue(pp_finish_sum_form(
            "How long did I take to finish 'Dune'?"))
        # impersonal "it" and when/before siblings stay out
        self.assertFalse(pp_finish_sum_form(
            "How long did it take to finish the marathon?"))
        self.assertFalse(pp_finish_sum_form(
            "How long did I take to finish 'Dune' when I started "
            "my new job?"))
        self.assertFalse(pp_finish_sum_form(CAT_Q))

    def test_single_anchor_falls_through(self):
        """One anchor is not a 'combined' answer → None."""
        dated = [(FINISH_DATES["session_1"],
                  FINISH_HAY[0]["messages"])]
        ans, detail = answer_pp_duration(FINISH_Q, dated)
        self.assertIsNone(ans)
        self.assertEqual(detail.get("route"), "finish_sum")

    def test_title_binding_excludes_foreign_anchors(self):
        """Anchors that name no question title word are ignored."""
        dated = [
            (FINISH_DATES["session_1"], [
                {"role": "user", "content": (
                    "I finished some random novel last month; it "
                    "took me three weeks to finish and I loved "
                    "it.")},
            ]),
            (FINISH_DATES["session_2"], [
                {"role": "user", "content": (
                    "I just finished \"The Nightingale\", which "
                    "took me two and a half weeks to finish.")},
            ]),
        ]
        ans, detail = answer_pp_duration(FINISH_Q, dated)
        self.assertIsNone(ans)
        self.assertEqual(detail.get("anchors"), 1)

    def test_when_form_never_hijacks_route_b(self):
        """A when-form finish question stays on the (b) path."""
        q = ("How long did I take to finish 'Dune' when I started "
             "my new job?")
        _ans, detail = answer_pp_duration(q, [
            ("2023-05-01", [
                {"role": "user", "content": (
                    "I started my new job on May 1st, right around "
                    "when I began 'Dune' 10 days ago.")},
            ]),
            ("2023-05-20", [
                {"role": "user", "content": (
                    "I finished 'Dune' yesterday; it took me two "
                    "weeks to finish.")},
            ]),
        ])
        self.assertNotEqual(detail.get("route"), "finish_sum")

    def test_half_parse_helper(self):
        from amg_bench_quality import _pp_finish_num
        self.assertAlmostEqual(_pp_finish_num("two and a half"), 2.5)
        self.assertAlmostEqual(_pp_finish_num("three"), 3.0)
        self.assertAlmostEqual(_pp_finish_num("a"), 1.0)
        self.assertAlmostEqual(_pp_finish_num("2 and a half"), 2.5)
        self.assertIsNone(_pp_finish_num("several"))

    def test_render_helper(self):
        from amg_bench_quality import _pp_finish_render
        self.assertEqual(_pp_finish_render(38.5, ["week"]),
                         "5.5 weeks")
        self.assertEqual(_pp_finish_render(21.0, ["week"]),
                         "3 weeks")
        self.assertEqual(_pp_finish_render(45.0, ["day"]),
                         "45 days")
        self.assertIsNone(_pp_finish_render(0, ["week"]))

    def test_judge_pins(self):
        self.assertTrue(pp_duration_judge(
            FINISH_Q, "5.5 weeks", "5.5 weeks"))
        self.assertFalse(pp_duration_judge(
            FINISH_Q, "5.5 weeks", "6 weeks"))
        self.assertTrue(pp_duration_judge(CAT_Q, "9 months",
                                          "9 months"))


if __name__ == "__main__":
    unittest.main()
