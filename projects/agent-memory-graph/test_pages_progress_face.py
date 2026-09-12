"""C567: pages-progress faces — two question heads over the same
"on page N" anchor family:

- Face A (read-so-far): "How many pages of 'X' have I read so
  far?" — the answer is the LATEST on-page anchor bound to the
  quoted title (user lines only, document order). Real row
  184da446: s2 'currently on page 200' → s41 'I'm now on page
  220' (twice) → 220.
- Face B (pages-left): "How many pages do I have left to read in
  'X'?" — total-pages fact minus the latest on-page anchor. Real
  row 2311e44b: s38 'a long one with 440 pages' → s46 'currently
  on page 250' → 440 − 250 = 190.

Guards (census + abs-row driven): reading-pace lines ('10-20
pages a week') are rejected as totals by range+pace rules; the
2311e44b_abs sibling ('Sapiens') has NO total and NO on-page
anchor → honest fall-through (route returns None, gate chain
untouched, abstain pred byte-stable). Assistant page estimates
('assume an average page count of 400 pages per book') are
excluded by the user-role wall.

Census (all 500): each head matches EXACTLY 1 row, both
unbanked. The only other page-count question (37f165cf, 'what
was the page count of the two novels I finished in January and
March' — a month-bound sum, GT 856) matches neither head and
stays out of THIS lane (C568 later gave it its own
page_count_sum lane); the 'grant aim page' reminder (8cf51dda)
is not a pages question at all.
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
    _cnt_pages_progress,
    answer_counting,
    counting_form,
    pp_pages_form,
)

LEFT_Q = "How many pages do I have left to read in 'The Nightingale'?"
READ_Q = ("How many pages of 'A Short History of Nearly Everything' "
          "have I read so far?")
ABS_Q = "How many pages do I have left to read in 'Sapiens'?"
NOVELS_Q = "What was the page count of the two novels I finished in January and March?"
REMINDER_Q = ("I'm going back to our previous conversation about the "
              "grant aim page on molecular subtypes and endometrial "
              "cancer. Can you remind me what were the three aims?")

# ── verbatim real-row lines (C562 lesson: replicate real shapes) ──

# 2311e44b haystack (session_38 / session_46)
NG_S38_U = ("I've been tracking my reading habits and I want to update "
            "my spreadsheet. Can you help me calculate how many pages I "
            "need to read per day to reach my goal of 50 books by the "
            "end of the year, considering I've already read 12 books so "
            "far? By the way, I just got back to reading \"The "
            "Nightingale\" and I'm excited to finally finish it - it's "
            "a long one with 440 pages!")
NG_S38_A = ("Since you didn't specify the average page count of the "
            "books you read, we'll use the page count of \"The "
            "Nightingale\" as a rough estimate. Let's assume an average "
            "page count of 400 pages per book (which is a reasonable "
            "estimate, given the length of \"The Nightingale\").")
NG_S46_U = ("I'm currently on page 250 of 'The Nightingale' by Kristin "
            "Hannah, and I'm really getting into it. I'd like to apply "
            "the principles from 'Atomic Habits' and 'Deep Work' to "
            "improve my reading habits. Can you help me create a plan "
            "to increase my reading speed and retention?")

LEFT_HAY = [
    {"session_id": "session_38",
     "messages": [{"role": "user", "content": NG_S38_U},
                  {"role": "assistant", "content": NG_S38_A}]},
    {"session_id": "session_46",
     "messages": [{"role": "user", "content": NG_S46_U}]},
]

# 184da446 haystack (session_2 / session_41)
SH_S2_U = ("I'm trying to learn more about AI-powered medical "
           "diagnosis. Can you recommend some online resources or "
           "articles that might help me understand the concept better? "
           "By the way, I've been reading \"A Short History of Nearly "
           "Everything\" and I'm currently on page 200, which has some "
           "interesting insights on the history of medicine.")
SH_S41_U0 = ("I'm interested in learning more about renewable energy, "
             "can you recommend some online resources or documentaries "
             "that I can check out? By the way, I just finished reading "
             "about the discovery of DNA structure in \"A Short History "
             "of Nearly Everything\" - I'm now on page 220, and it's "
             "amazing how much I've learned so far!")
SH_S41_U6 = ("I'm really interested in learning more about AI-powered "
             "diagnosis of rare diseases. I've been reading \"A Short "
             "History of Nearly Everything\" and it's amazing how much "
             "we still don't know about the human body. I'm on page 220 "
             "now, and I just finished reading about the discovery of "
             "DNA structure. It got me thinking about how AI can help "
             "diagnose rare genetic disorders.")

READ_HAY = [
    {"session_id": "session_2",
     "messages": [{"role": "user", "content": SH_S2_U}]},
    {"session_id": "session_41",
     "messages": [{"role": "user", "content": SH_S41_U0},
                  {"role": "user", "content": SH_S41_U6}]},
]

# 2311e44b_abs haystack (Sapiens: pace line only, no total, no
# on-page anchor; Nightingale page-250 line present = cross-title
# contamination probe)
SP_S14_U2 = ("Also, can you recommend me some non-fiction books that "
             "are not too dense and easy to read? I've been enjoying "
             "'Sapiens' but it's really slow going.")
SP_S14_U8 = NG_S46_U          # Nightingale anchor in the SAME haystack
SP_S49_U2 = ("Can you help me adjust the calculation based on my "
             "reading speed? For example, I've been reading \"Sapiens\" "
             "at a pace of 10-20 pages a week.")

ABS_HAY = [
    {"session_id": "session_14",
     "messages": [{"role": "user", "content": SP_S14_U2},
                  {"role": "user", "content": SP_S14_U8}]},
    {"session_id": "session_49",
     "messages": [{"role": "user", "content": SP_S49_U2}]},
]


def _turns(hay):
    return [{s["session_id"]: s["messages"]} for s in hay] and [
        {"session_id": s["session_id"], "turns": s["messages"]}
        for s in hay]


class TestPagesProgressFace(unittest.TestCase):

    # ── gate entries ──

    def test_gate_entry_faces(self):
        self.assertTrue(pp_pages_form(LEFT_Q))
        self.assertTrue(pp_pages_form(READ_Q))

    def test_gate_out_of_lane(self):
        # month-bound novel sum (37f165cf) and the reminder
        # 'grant aim page' (8cf51dda) must stay out
        self.assertFalse(pp_pages_form(NOVELS_Q))
        self.assertFalse(pp_pages_form(REMINDER_Q))
        # no quoted title in question → out of lane
        self.assertFalse(pp_pages_form(
            "How many pages do I have left to read in The Nightingale?"))

    def test_counting_form_claims_pages(self):
        self.assertEqual(counting_form(LEFT_Q), "pages")
        self.assertEqual(counting_form(READ_Q), "pages")
        # C568: 37f165cf now claimed by its own page_count_sum lane
        # (was pinned None in C567 when it stayed out of THIS lane)
        self.assertEqual(counting_form(NOVELS_Q), "page_count_sum")
        self.assertIsNone(counting_form(REMINDER_Q))

    # ── adapter-level production pins (real rows) ──

    def test_adapter_rescue_pages_left_real_row(self):
        a = LongMemEvalAdapter()
        a.ingest_sessions(LEFT_HAY)
        ans, meta = a.answer_extractive(LEFT_Q)
        self.assertEqual(ans, "190")
        self.assertEqual(meta.get("gate"), "counting")
        self.assertEqual(meta.get("counting", {}).get("form"), "pages")

    def test_adapter_rescue_pages_read_real_row(self):
        a = LongMemEvalAdapter()
        a.ingest_sessions(READ_HAY)
        ans, meta = a.answer_extractive(READ_Q)
        self.assertEqual(ans, "220")
        self.assertEqual(meta.get("gate"), "counting")
        self.assertEqual(meta.get("counting", {}).get("form"), "pages")

    # ── route-level sanity (direct calls) ──

    def test_route_direct_left(self):
        self.assertEqual(_cnt_pages_progress(LEFT_Q, _turns(LEFT_HAY)),
                         "190")

    def test_route_direct_read_latest_wins(self):
        self.assertEqual(_cnt_pages_progress(READ_Q, _turns(READ_HAY)),
                         "220")

    # ── guards ──

    def test_abs_row_shape_honest_fallthrough(self):
        """Sapiens sibling: pace line rejected as total, foreign-title
        on-page anchor ignored → None (gate chain untouched)."""
        self.assertIsNone(_cnt_pages_progress(ABS_Q, _turns(ABS_HAY)))
        ans, detail = answer_counting(ABS_Q, _turns(ABS_HAY))
        self.assertIsNone(ans)
        self.assertEqual(detail.get("form"), "pages")

    def test_assistant_lines_rejected(self):
        hay = [{"session_id": "session_1",
                "messages": [{"role": "assistant",
                              "content": NG_S38_A},
                             {"role": "assistant",
                              "content": NG_S46_U}]}]
        self.assertIsNone(_cnt_pages_progress(LEFT_Q, _turns(hay)))

    def test_left_face_missing_current(self):
        hay = [{"session_id": "session_1",
                "messages": [{"role": "user", "content": NG_S38_U}]}]
        self.assertIsNone(_cnt_pages_progress(LEFT_Q, _turns(hay)))

    def test_left_face_missing_total(self):
        hay = [{"session_id": "session_1",
                "messages": [{"role": "user", "content": NG_S46_U}]}]
        self.assertIsNone(_cnt_pages_progress(LEFT_Q, _turns(hay)))

    def test_left_face_sanity_current_ge_total(self):
        hay = [{"session_id": "session_1",
                "messages": [
                    {"role": "user", "content": NG_S38_U},
                    {"role": "user",
                     "content": "I'm currently on page 500 of 'The "
                                "Nightingale' by Kristin Hannah."}]}]
        self.assertIsNone(_cnt_pages_progress(LEFT_Q, _turns(hay)))

    def test_pace_line_never_a_total(self):
        # pace + range line even WITHOUT the abs sibling's guards:
        # a hypothetical left-question over a pace-only haystack
        hay = [{"session_id": "session_1",
                "messages": [{"role": "user", "content": SP_S49_U2}]}]
        self.assertIsNone(
            _cnt_pages_progress(
                "How many pages do I have left to read in \"Sapiens\"?",
                _turns(hay)))

    def test_read_face_no_anchor(self):
        hay = [{"session_id": "session_1",
                "messages": [{"role": "user",
                              "content": "I love reading \"A Short "
                                         "History of Nearly Everything\""
                                         " so much."}]}]
        self.assertIsNone(_cnt_pages_progress(READ_Q, _turns(hay)))

    def test_judge_credit_real_rows(self):
        from amg_bench_quality import counting_judge
        self.assertTrue(counting_judge(LEFT_Q, "190", "190"))
        self.assertTrue(counting_judge(READ_Q, "220", "220"))


if __name__ == "__main__":
    unittest.main()
