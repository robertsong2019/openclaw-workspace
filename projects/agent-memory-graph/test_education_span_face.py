"""C569: education-span face — gpt4_372c3eed + _abs (one family).

Head: "How many years in total did I spend in formal education from
high school to the completion of my Bachelor's/Master's degree?"

Census (all 500): the head matches EXACTLY these 2 rows, both
unbanked WRONG (gate=counting via unit_sum today — a stray 'four
years' anchor answered '4').

Evidence path (verbatim real-row lines): completion-year chain over
user lines — high-school year-range ('Arcadia High School from 2010
to 2014' = 4), PCC Associate's (May 2016, year-gap 2016-2014 = 2),
UCLA Bachelor's (2020, explicit 'took me four years to complete' = 4)
→ 10 = GT.

The _abs sibling's Master's is only ever 'I'm considering pursuing a
Master's degree' (aspiration-guarded, year-less) — chain explicit,
target absent → RESOLVED negative existence (ABSTAIN_ANSWER), not a
retrieval failure (C514 museum_count / C564 before-job precedent).

Guards pinned here:
- assistant degree lines die on the user-role wall
- repeated Bachelor's mentions (GPA line) dedupe by (degree, year)
- explicit duration beats year-diff (pinned at 'three years' → 9)
- pre-HS degree years are skipped (chronological sanity)
- target mid-chain (later degree exists) → None (premise conflict)
- unit_sum keeps its remaining rows (zero-kill pin)
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    ABSTAIN_ANSWER,
    _cnt_education_span,
    answer_counting,
    counting_form,
    counting_judge,
)

Q_BS = ("How many years in total did I spend in formal education from "
        "high school to the completion of my Bachelor's degree?")
Q_MS = ("How many years in total did I spend in formal education from "
        "high school to the completion of my Master's degree?")
Q_AS = ("How many years in total did I spend in formal education from "
        "high school to the completion of my Associate's degree?")

# ── verbatim real-row lines (gpt4_372c3eed haystack, s5/s25/s38) ──

UCLA_M0_U = ("I'd love to earn more about the latest developments in "
             "AI and machine learning. By the way, I graduated with a "
             "Bachelor's in Computer Science from UCLA in 2020, which "
             "took me four years to complete.")
UCLA_GPA_U = ("I had a strong academic background in computer science, "
              "graduating from UCLA in 2020 with a Bachelor's degree in "
              "Computer Science, where I had a GPA of 3.6 out of 4.0.")
PCC_M0_U = ("Oh, and I should mention that I have a strong foundation "
            "in computer science, having earned an Associate's degree "
            "in Computer Science from Pasadena City College (PCC) in "
            "May 2016, before joining UCLA.")
MS_CONSIDER_U = ("I'm considering pursuing a Master's degree in "
                 "Computer Science, and I was wondering if you could "
                 "help me with some information on the top CS programs "
                 "in California.")
HS_M2_U = ("That's really helpful, thanks! I actually attended UCLA "
           "for undergrad after I attended Arcadia High School from "
           "2010 to 2014, so I'm familiar with the campus and program.")
UCLA_M1_A = ("A Bruin! Congratulations on completing your Bachelor's "
             "in Computer Science from UCLA in 2020!")


def sess(*turns):
    return [{"session_id": "session_1", "turns": list(turns)}]


def u(text):
    return {"role": "user", "content": text}


def a(text):
    return {"role": "assistant", "content": text}


REAL_SESS = [
    {"session_id": "session_6", "turns": [u(UCLA_M0_U), a(UCLA_M1_A),
                                          u(UCLA_GPA_U)]},
    {"session_id": "session_26", "turns": [u(PCC_M0_U)]},
    {"session_id": "session_39", "turns": [u(MS_CONSIDER_U),
                                           u(HS_M2_U)]},
]


class EducationSpanForm(unittest.TestCase):
    def test_form_claims_bachelor_row(self):
        self.assertEqual(counting_form(Q_BS), "education_span")

    def test_form_claims_master_row(self):
        self.assertEqual(counting_form(Q_MS), "education_span")

    def test_unit_sum_sibling_unaffected(self):
        # zero-kill pin: the how-many-total unit_sum family keeps
        # its non-education rows (census: zero overlap full-500)
        self.assertEqual(
            counting_form("How many hours in total did I spend gaming?"),
            "unit_sum")


class EducationSpanHandler(unittest.TestCase):
    def test_bachelor_real_chain_sums_ten(self):
        self.assertEqual(_cnt_education_span(Q_BS, REAL_SESS), "10 years")

    def test_master_absent_is_resolved_abstain(self):
        self.assertEqual(_cnt_education_span(Q_MS, REAL_SESS),
                         ABSTAIN_ANSWER)

    def test_assistant_degree_lines_die_on_role_wall(self):
        s = sess(a("You graduated with a Bachelor's from UCLA in 2020 "
                   "after PCC in 2016 and High School from 2010 to 2014."),
                 u("I attended Arcadia High School from 2010 to 2014."))
        self.assertIsNone(_cnt_education_span(Q_BS, s))

    def test_missing_hs_range_falls_through(self):
        s = sess(u("I graduated with a Bachelor's in CS from UCLA "
                   "in 2020."))
        self.assertIsNone(_cnt_education_span(Q_BS, s))

    def test_aspiring_degree_is_not_a_segment(self):
        s = sess(u("I attended Arcadia High School from 2010 to 2014."),
                 u("I'm considering pursuing a Master's degree "
                   "starting 2024."))
        self.assertIsNone(_cnt_education_span(Q_MS, s))

    def test_explicit_duration_beats_year_diff(self):
        s = sess(u("I attended Arcadia High School from 2010 to 2014."),
                 u("I earned an Associate's degree from PCC in "
                   "May 2016."),
                 u("I graduated with a Bachelor's from UCLA in 2020, "
                   "which took me three years to complete."))
        self.assertEqual(_cnt_education_span(Q_BS, s), "9 years")

    def test_pre_hs_degree_year_skipped(self):
        s = sess(u("I attended Arcadia High School from 2010 to 2014."),
                 u("I earned a Bachelor's degree from UCLA in 2009."))
        self.assertIsNone(_cnt_education_span(Q_BS, s))

    def test_target_mid_chain_premise_conflict(self):
        s = sess(u("I attended Arcadia High School from 2010 to 2014."),
                 u("I graduated with a Bachelor's in CS from UCLA in "
                   "2020."),
                 u("I finished my Master's in CS from Stanford in "
                   "2022."))
        self.assertIsNone(_cnt_education_span(Q_BS, s))

    def test_gpa_repeat_dedupes(self):
        # UCLA_M0_U already registers (bachelor, 2020, dur=4); the
        # GPA line re-mentions it year-first — dedupe must keep the
        # sum at 10, never 4+4+2+4
        self.assertEqual(_cnt_education_span(Q_BS, REAL_SESS),
                         "10 years")


class EducationSpanDispatch(unittest.TestCase):
    def test_answer_counting_routes_the_form(self):
        ans, detail = answer_counting(Q_BS, REAL_SESS)
        self.assertEqual(ans, "10 years")
        self.assertEqual(detail.get("form"), "education_span")

    def test_answer_counting_abstain_channel(self):
        ans, detail = answer_counting(Q_MS, REAL_SESS)
        self.assertEqual(ans, ABSTAIN_ANSWER)
        self.assertEqual(detail.get("form"), "education_span")

    def test_judge_credits_ten_years(self):
        self.assertTrue(counting_judge(Q_BS, "10 years", "10 years"))
        self.assertFalse(counting_judge(Q_BS, "10 years", "4 years"))


if __name__ == "__main__":
    unittest.main()
