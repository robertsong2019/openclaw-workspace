"""C566: activity-span sum — "how many weeks in total do I spent
on reading 'X' and listening to 'Y'?" has NO explicit durations
anywhere; the per-entity span is session-date arithmetic between
a start fact ("I started reading 'X' ... today") and a finish
fact ("I just finished reading 'X' today").

Real row gpt4_a1b77f9c (GT '...so a total of 8 weeks'): three
quoted titles, start/finish facts in six distinct sessions —
Nightingale s26(01/01)→s28(01/15)=14d, Sapiens s35(02/01)→
s38(03/01)=28d, The Power s40(03/06)→s41(03/20)=14d → 56 days
= 8 weeks. Quote style varies per session (single AND double
quotes both occur), so binding matches any quote-wrapped form;
unquoted co-mentions ("The Power of Habit") cannot bind (they
also lack start/finish+today — defense in depth).

Census (all 500): head "how many <unit> in total (do|did|have)
(i|we) spend|spent on reading|listening" = exactly 1 row,
unbanked. The banked spend-total siblings (edced276 Hawaii/NYC)
put "in total" AFTER "spend" and stay out by construction, as do
the education-range head (372c3eed) and counting total
(6cb6f249).
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
    judge_semantic,
    pp_activity_sum_form,
)

ACT_Q = ("How many weeks in total do I spent on reading 'The "
         "Nightingale' and listening to 'Sapiens: A Brief History "
         "of Humankind' and 'The Power'?")
ACT_GT = ("2 weeks for 'The Nightingale', 4 weeks for 'Sapiens: A "
          "Brief History of Humankind', and 2 weeks for 'The "
          "Power', so a total of 8 weeks.")

# verbatim real-row lines (C562 lesson), quote styles preserved
S26 = ("I'm looking for some book recommendations. I started "
       "reading 'The Nightingale' by Kristin Hannah today and I'm "
       "really into historical fiction right now. Can you suggest "
       "some other books in the same genre that you think I'd "
       "enjoy?")
S28 = ("I'm looking for some book recommendations. I just "
       "finished reading \"The Nightingale\" by Kristin Hannah "
       "today, and I'm still reeling from the emotional impact. "
       "I'm open to trying out different genres, so feel free to "
       "suggest anything that you might enjoy.")
S35 = ("That's really helpful, thanks! I think I can apply this "
       "to some of my own habits. Speaking of habits, I just "
       "started listening to 'Sapiens: A Brief History of "
       "Humankind' by Yuval Noah Harari today, and it got me "
       "thinking about how humans have developed certain habits "
       "and behaviors over time.")
S38 = ("I just finished listening to 'Sapiens: A Brief History "
       "of Humankind' by Yuval Noah Harari today, and it got me "
       "thinking about the impact of technology on human "
       "evolution.")
S40 = ("I'm interested in learning more about the themes of "
       "identity, culture, and power in \"The Fifth Season\" by "
       "N.K. Jemisin. I've been thinking a lot about how these "
       "themes relate to my own experiences as a woman, and I "
       "started listening to \"The Power\" by Naomi Alderman "
       "today, which got me thinking about power dynamics.")
S41 = ("I'm looking for some book recommendations. I just "
       "finished listening to 'The Power' by Naomi Alderman "
       "today and it really made me think. I'm interested in "
       "exploring more books that challenge my perspectives.")
S41_DISTRACTOR = ("I'm glad you liked The Power. I've been "
                  "meaning to explore more non-fiction books, do "
                  "you think The Power of Habit by Charles Duhigg "
                  "would be a good fit for me?")

ACT_HAY = [
    {"session_id": "session_26",
     "messages": [{"role": "user", "content": S26}]},
    {"session_id": "session_28",
     "messages": [{"role": "user", "content": S28}]},
    {"session_id": "session_35",
     "messages": [{"role": "user", "content": S35}]},
    {"session_id": "session_38",
     "messages": [{"role": "user", "content": S38}]},
    {"session_id": "session_40",
     "messages": [{"role": "user", "content": S40},
                  {"role": "user", "content": S41_DISTRACTOR}]},
    {"session_id": "session_41",
     "messages": [{"role": "user", "content": S41}]},
]
ACT_DATES = {"session_26": "2022-01-01", "session_28": "2022-01-15",
             "session_35": "2022-02-01", "session_38": "2022-03-01",
             "session_40": "2022-03-06", "session_41": "2022-03-20"}


def _dated(hay, dates):
    return [(dates[s["session_id"]], s["messages"]) for s in hay]


class TestActivitySumFace(unittest.TestCase):

    def test_gate_entry_rescues_real_row(self):
        """Adapter level: the head must route to pp_duration and
        answer the summed span (production path pin — C565
        direct-call ≠ production-path lesson)."""
        a = LongMemEvalAdapter()
        a.ingest_sessions(ACT_HAY, session_dates=ACT_DATES)
        ans, meta = a.answer_extractive(ACT_Q)
        self.assertEqual(ans, "8 weeks")
        self.assertEqual(meta.get("gate"), "pp_duration")

    def test_route_direct_rescue(self):
        ans, detail = answer_pp_duration(ACT_Q, _dated(ACT_HAY,
                                                       ACT_DATES))
        self.assertEqual(ans, "8 weeks")
        self.assertEqual(detail.get("route"), "activity_sum")
        self.assertEqual(detail.get("total_days"), 56)
        self.assertEqual(detail.get("spans"),
                         {"The Nightingale": 14,
                          "Sapiens: A Brief History of Humankind": 28,
                          "The Power": 14})

    def test_form_predicate_real_and_variants(self):
        self.assertTrue(pp_activity_sum_form(ACT_Q))
        self.assertTrue(pp_activity_sum_form(
            "How many days in total did I spend on reading 'Dune' "
            "and listening to 'Hyperion'?"))
        self.assertTrue(pp_activity_sum_form(
            "How many weeks in total have I spent on listening to "
            "'The Fifth Season'?"))

    def test_form_rejects_census_siblings(self):
        # banked spend-total: "in total" after "spend"
        self.assertFalse(pp_activity_sum_form(
            "How many days did I spend in total traveling in "
            "Hawaii and in New York City?"))
        # education-range head (different anchor type)
        self.assertFalse(pp_activity_sum_form(
            "How many years in total did I spend in formal "
            "education from high school to the completion of my "
            "Bachelor's degree?"))
        # counting total (no spend-on frame)
        self.assertFalse(pp_activity_sum_form(
            "How many days did I take social media breaks in "
            "total?"))
        # when/before siblings stay with route (b)
        self.assertFalse(pp_activity_sum_form(
            "How many weeks in total did I spend on reading 'Dune' "
            "when I was on vacation?"))
        # other pp-family heads
        self.assertFalse(pp_activity_sum_form(
            "How long have I had my cat, Luna?"))
        self.assertFalse(pp_activity_sum_form(
            "How long did I take to finish 'Dune' and 'Hyperion' "
            "combined?"))

    def test_mixed_quote_styles_bind(self):
        """s28/s40 use double quotes where s26/s41 use single —
        binding must be quote-style agnostic (real-row lesson)."""
        hay = [ACT_HAY[0], ACT_HAY[1]]  # Nightingale only, mixed
        dates = {"session_26": "2022-01-01",
                 "session_28": "2022-01-15"}
        q = ("How many weeks in total do I spent on reading 'The "
             "Nightingale' and listening to 'Hyperion'?")
        ans, detail = answer_pp_duration(q, _dated(hay, dates))
        self.assertIsNone(ans)  # Hyperion unresolved → honest None
        self.assertIn("Hyperion", detail.get("missing", ""))

    def test_missing_finish_falls_through(self):
        hay = [{"session_id": "session_26",
                "messages": [{"role": "user",
                              "content": S26}]}]
        ans, detail = answer_pp_duration(
            ACT_Q, _dated(hay, {"session_26": "2022-01-01"}))
        self.assertIsNone(ans)
        self.assertIn("finish", detail.get("missing", ""))

    def test_confusable_title_not_anchor(self):
        """'The Power of Habit' (unquoted, no today) is neither a
        start nor a finish fact for 'The Power'."""
        hay = [{"session_id": "session_1",
                "messages": [{"role": "user",
                              "content": S41_DISTRACTOR}]}]
        ans, detail = answer_pp_duration(
            ACT_Q, _dated(hay, {"session_1": "2022-03-06"}))
        self.assertIsNone(ans)

    def test_assistant_lines_ignored(self):
        hay = [{"session_id": "session_1",
                "messages": [{"role": "assistant",
                              "content": S28},
                             {"role": "assistant",
                              "content": S26}]}]
        ans, _ = answer_pp_duration(
            ACT_Q, _dated(hay, {"session_1": "2022-01-15"}))
        self.assertIsNone(ans)

    def test_days_unit_render(self):
        q = ("How many days in total do I spent on reading 'Dune' "
             "and listening to 'Hyperion'?")
        hay = [
            {"session_id": "s1",
             "messages": [{"role": "user", "content":
                           "I started reading 'Dune' today."}]},
            {"session_id": "s2",
             "messages": [{"role": "user", "content":
                           "I just finished reading 'Dune' today."}]},
            {"session_id": "s3",
             "messages": [{"role": "user", "content":
                           "I started listening to 'Hyperion' "
                           "today."}]},
            {"session_id": "s4",
             "messages": [{"role": "user", "content":
                           "I just finished listening to "
                           "'Hyperion' today."}]},
        ]
        dates = {"s1": "2022-03-01", "s2": "2022-03-04",
                 "s3": "2022-03-10", "s4": "2022-03-14"}
        ans, detail = answer_pp_duration(q, _dated(hay, dates))
        self.assertEqual(ans, "7 days")
        self.assertEqual(detail.get("total_days"), 7)

    def test_three_week_span_renders_weeks(self):
        q = ("How many weeks in total do I spent on reading 'Dune' "
             "and listening to 'Hyperion'?")
        hay = [
            {"session_id": "s1",
             "messages": [{"role": "user", "content":
                           "I started reading 'Dune' today."}]},
            {"session_id": "s2",
             "messages": [{"role": "user", "content":
                           "I just finished reading 'Dune' today."}]},
            {"session_id": "s3",
             "messages": [{"role": "user", "content":
                           "I started listening to 'Hyperion' "
                           "today."}]},
            {"session_id": "s4",
             "messages": [{"role": "user", "content":
                           "I just finished listening to "
                           "'Hyperion' today."}]},
        ]
        dates = {"s1": "2022-03-01", "s2": "2022-03-15",
                 "s3": "2022-01-01", "s4": "2022-01-08"}
        ans, _ = answer_pp_duration(q, _dated(hay, dates))
        self.assertEqual(ans, "3 weeks")  # 14 + 7 = 21 days

    def test_banking_judge_channel(self):
        """The banking channel (judge_semantic — number-subset
        face) must credit '8 weeks' against the long GT."""
        self.assertEqual(
            judge_semantic(ACT_Q, "8 weeks", ACT_GT), "CORRECT")
        self.assertNotEqual(
            judge_semantic(ACT_Q, "9 weeks", ACT_GT), "CORRECT")


if __name__ == "__main__":
    unittest.main()
