"""C570: book-span + reverse-finish faces (one session-date family).

Head A (route h): "How many days did it take me to finish 'X' …?"
Head B (route i): "Which book did I finish <n> <unit>s ago?"

Census (all 500): each head matches EXACTLY 1 row, both unbanked
WRONG today (gate=answer fallback — the answer gate echoes a
recommendation-request line as the 'answer').

Evidence path (verbatim real-row lines, 2ebe6c90 / 2ebe6c92):
- start fact:  s17/s8  @2023-01-10  "I just started "The Nightingale"
  by Kristin Hannah today"
- finish fact: s20/s44 @2023-01-31  "I just finished a historical
  fiction novel, "The Nightingale" by Kristin Hannah, today"
- head A: 2023-01-31 − 2023-01-10 = 21 days (GT '21 days. 22 days
  (including the last day) is also acceptable.')
- head B: question date 2023-02-07 − 7d = 2023-01-31 = the finish
  anchor's session (GT "'The Nightingale' by Kristin Hannah") — the
  ago-frame anchors to the QUESTION date, threaded into
  answer_pp_duration as an optional third arg.

Guards pinned here:
- head A stays single-titled: 0 or 2+ quoted titles → fall-through
  (a sum would need an ``in total`` frame — C566 territory)
- receive-order cousins (b3c15d39 "it take for me to receive"), the
  C565 finish-sum head ("how long … combined"), the route (g)
  activity head, and when/before variants stay out of the span form
- head B's ago-frame is part of the form: the banked comparison
  sibling (gpt4_2d58bcd6 "finish reading first, 'X' or 'Y'?") and
  no-ago forms stay out (zero-kill by construction)
- line-side title extraction is apostrophe-guarded: the naive
  ``'([^']+)'`` on the real anchor line steals
  "m looking … today and I" out of the leading "I'm" (C568
  quote-theft lesson, line-side edition) — double quotes win,
  single-quote fallback requires word boundaries
- exactly one distinct title at the target date (two books the same
  day → honest fall-through); assistant lines die on the user-role
  wall (C482 trust tiers)
- month-frame reverse lookup uses _PP_UNIT_DAYS rounding (30.44d →
  30) — pinned so future unit changes surface here
- same-sitting start+finish on one line renders "0 days" →
  fall-through (a one-sitting read is not a duration)
"""
import importlib.util
import os
import sys
import unittest
from datetime import datetime

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# importlib two-module discipline (C568 lesson #3): dataclass
# introspection needs the module registered in sys.modules.
_SPEC = importlib.util.spec_from_file_location(
    "amgq_test_c570",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "amg_bench_quality.py"))
_mod = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _mod
_SPEC.loader.exec_module(_mod)

Q_SPAN = ("How many days did it take me to finish 'The Nightingale' "
          "by Kristin Hannah?")
Q_SPAN_WK = "How many weeks did it take me to finish 'The Nightingale'?"
Q_SPAN_WHEN = "How many days did it take me to finish 'The Nightingale' before I moved?"
Q_SPAN_READ = "How many weeks did it take me to read 'The Nightingale'?"
Q_RECV = ("How many days did it take for me to receive the new remote "
          "shutter release after I ordered it?")
Q_COMBINED = ("How long did I take to finish 'The Seven Husbands of "
              "Evelyn Hugo' and 'The Nightingale' combined?")
Q_ACTIVITY = ("How many weeks in total did I spend on reading "
              "'The Nightingale' and listening to 'Dune'?")
Q_WHEN = "Which book did I finish a week ago?"
Q_WHEN_MONTH = "Which book did I finish a month ago?"
Q_FIRST = ("Which book did I finish reading first, 'The Hate U Give' "
           "or 'The Nightingale'?")
Q_RECENT = "Which book did I finish most recently?"
QDATE = "2023/02/07 (Tue) 09:09"

# ── verbatim real-row lines (2ebe6c90 s17/s20, 2ebe6c92 s44) ──
NIGHT_START = ("I'm looking for some book recommendations. I've been on a "
               "roll with reading lately, and I just started \"The Nightingale\" "
               "by Kristin Hannah today. I'm really into historical fiction.")
NIGHT_FINISH = ("I'm looking for some book recommendations. I just finished a "
                "historical fiction novel, \"The Nightingale\" by Kristin Hannah, "
                "today and I'm in the mood for something similar.")


def _dated(sess):
    return [(datetime.strptime(d, "%Y-%m-%d"), t) for d, t in sess]


SESS_H = [
    ("2023-01-10", [{"role": "user", "content": NIGHT_START}]),
    ("2023-01-15", [{"role": "user", "content": "Weather is nice today."}]),
    ("2023-01-31", [{"role": "user", "content": NIGHT_FINISH}]),
]
SESS_I = [
    ("2023-01-24", [{"role": "user",
                     "content": "I just finished 'The Hate U Give' today."}]),
    ("2023-01-31", [{"role": "user", "content": NIGHT_FINISH}]),
    ("2023-02-01", [{"role": "assistant", "content": NIGHT_FINISH}]),
]


class FormGates(unittest.TestCase):
    def test_span_real(self):
        self.assertTrue(_mod.pp_book_span_form(Q_SPAN))

    def test_span_read_variant(self):
        self.assertTrue(_mod.pp_book_span_form(Q_SPAN_READ))

    def test_span_receive_cousin_out(self):
        self.assertFalse(_mod.pp_book_span_form(Q_RECV))

    def test_span_combined_cousin_out(self):
        self.assertFalse(_mod.pp_book_span_form(Q_COMBINED))

    def test_span_activity_cousin_out(self):
        self.assertFalse(_mod.pp_book_span_form(Q_ACTIVITY))

    def test_span_when_before_out(self):
        self.assertFalse(_mod.pp_book_span_form(Q_SPAN_WHEN))

    def test_when_real(self):
        self.assertTrue(_mod.pp_finish_when_form(Q_WHEN))

    def test_when_banked_sibling_out(self):
        self.assertFalse(_mod.pp_finish_when_form(Q_FIRST))

    def test_when_no_ago_out(self):
        self.assertFalse(_mod.pp_finish_when_form(Q_RECENT))


class BookSpanRoute(unittest.TestCase):
    def test_twenty_one_days(self):
        ans, det = _mod._pp_book_span(Q_SPAN, _dated(SESS_H))
        self.assertEqual(ans, "21 days")
        self.assertEqual(det["route"], "book_span")
        self.assertEqual(det["days"], 21)

    def test_week_render(self):
        ans, _ = _mod._pp_book_span(Q_SPAN_WK, _dated(SESS_H))
        self.assertEqual(ans, "3 weeks")

    def test_missing_start_falls_through(self):
        ans, det = _mod._pp_book_span(
            Q_SPAN, _dated(SESS_H[1:]))
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "start")

    def test_missing_finish_falls_through(self):
        ans, det = _mod._pp_book_span(
            Q_SPAN, _dated(SESS_H[:2]))
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "finish")

    def test_no_quoted_title_falls_through(self):
        ans, det = _mod._pp_book_span(
            "How many days did it take me to finish that novel?",
            _dated(SESS_H))
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "titles")

    def test_two_titles_fall_through(self):
        ans, det = _mod._pp_book_span(
            "How many days did it take me to finish "
            "'The Nightingale' and 'Dune'?", _dated(SESS_H))
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "titles")

    def test_negative_span_falls_through(self):
        sess = [
            ("2023-01-31", [{"role": "user", "content": NIGHT_FINISH}]),
            ("2023-02-10", [{"role": "user", "content": NIGHT_START}]),
        ]
        ans, det = _mod._pp_book_span(Q_SPAN, _dated(sess))
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "negative span")

    def test_same_sitting_zero_days_falls_through(self):
        sess = [("2023-01-31", [{"role": "user", "content":
                                 "I started and finished 'The Nightingale' today."}])]
        ans, _ = _mod._pp_book_span(Q_SPAN, _dated(sess))
        self.assertIsNone(ans)


class ReverseFinishRoute(unittest.TestCase):
    def test_title_author_render(self):
        ans, det = _mod._pp_finish_when(Q_WHEN, _dated(SESS_I), QDATE)
        self.assertEqual(ans, "The Nightingale by Kristin Hannah")
        self.assertEqual(det["route"], "finish_when")
        self.assertEqual(det["target"], "2023-01-31")

    def test_no_anchor_at_target_falls_through(self):
        ans, det = _mod._pp_finish_when(
            Q_WHEN, _dated(SESS_I), "2023/02/09 (Thu) 09:09")
        self.assertIsNone(ans)
        self.assertEqual(det["target"], "2023-02-02")

    def test_two_titles_same_day_falls_through(self):
        sess = [("2023-01-31",
                 [{"role": "user", "content": NIGHT_FINISH},
                  {"role": "user",
                   "content": "Also just finished 'Dune' today!"}])]
        ans, det = _mod._pp_finish_when(Q_WHEN, _dated(sess), QDATE)
        self.assertIsNone(ans)
        self.assertIn("titles at target", det["missing"])

    def test_month_frame_rounded_offset(self):
        sess = [("2023-01-08", [{"role": "user", "content":
                                 "I just finished 'The Song of Achilles' today."}])]
        ans, _ = _mod._pp_finish_when(Q_WHEN_MONTH, _dated(sess), QDATE)
        self.assertEqual(ans, "The Song of Achilles")

    def test_missing_qdate_falls_through(self):
        ans, det = _mod._pp_finish_when(Q_WHEN, _dated(SESS_I), "")
        self.assertIsNone(ans)
        self.assertEqual(det["missing"], "qdate")

    def test_assistant_line_no_fact(self):
        # only an assistant finish line at the target date carries
        # no fact (user-role wall) → fall-through
        sess = [("2023-01-31", [{"role": "assistant",
                                 "content": NIGHT_FINISH}])]
        ans, det = _mod._pp_finish_when(Q_WHEN, _dated(sess), QDATE)
        self.assertIsNone(ans)
        self.assertIn("titles at target", det["missing"])


class LineTitleExtraction(unittest.TestCase):
    def test_double_quote_wins_over_apostrophe(self):
        title, author = _mod._pp_line_title(NIGHT_FINISH)
        self.assertEqual(title, "The Nightingale")
        self.assertEqual(author, "Kristin Hannah")

    def test_single_quote_fallback_with_guards(self):
        title, author = _mod._pp_line_title(
            "I've just finished 'The Poppy War' by Rebecca Kuang, today.")
        self.assertEqual(title, "The Poppy War")
        self.assertEqual(author, "Rebecca Kuang")

    def test_no_title(self):
        title, author = _mod._pp_line_title(
            "I'm done with everything today.")
        self.assertIsNone(title)
        self.assertIsNone(author)


class Dispatch(unittest.TestCase):
    def test_route_h(self):
        # answer_pp_duration takes STRING dates — it owns parsing
        ans, det = _mod.answer_pp_duration(Q_SPAN, SESS_H)
        self.assertEqual(ans, "21 days")
        self.assertEqual(det["route"], "book_span")

    def test_route_i(self):
        ans, det = _mod.answer_pp_duration(Q_WHEN, SESS_I, QDATE)
        self.assertEqual(ans, "The Nightingale by Kristin Hannah")
        self.assertEqual(det["route"], "finish_when")


class AdapterWired(unittest.TestCase):
    """Production pins: the real shapes through ingest_sessions +
    answer_extractive — the wired path (adapter-level gate entry,
    question_date threading, pp_duration gate attribution)."""

    def test_head_a(self):
        ad = _mod.LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "user", "content": NIGHT_START}]},
             {"session_id": "session_2",
              "messages": [{"role": "user",
                            "content": "How is the weather today?"}]},
             {"session_id": "session_3",
              "messages": [{"role": "user", "content": NIGHT_FINISH}]}],
            session_dates={"session_1": "2023-01-10",
                           "session_2": "2023-01-15",
                           "session_3": "2023-01-31"})
        ans, meta = ad.answer_extractive(Q_SPAN, "2023/05/01 (Mon) 21:05")
        self.assertEqual(ans, "21 days")
        self.assertEqual(meta["gate"], "pp_duration")

    def test_head_b(self):
        ad = _mod.LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "user",
                            "content": "I just finished 'The Hate U Give' today."}]},
             {"session_id": "session_2",
              "messages": [{"role": "user", "content": NIGHT_FINISH}]}],
            session_dates={"session_1": "2023-01-24",
                           "session_2": "2023-01-31"})
        ans, meta = ad.answer_extractive(Q_WHEN, QDATE)
        self.assertEqual(ans, "The Nightingale by Kristin Hannah")
        self.assertEqual(meta["gate"], "pp_duration")

    def test_span_banked_neighbors_unchanged(self):
        # zero-kill pins: the receive-order and finish-sum cousins
        # keep their pre-C570 routing (no new form fires on them)
        ad = _mod.LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "user", "content":
                            "I ordered a remote shutter release on Monday "
                            "and just received it today."}]}],
            session_dates={"session_1": "2023-01-10"})
        ans, meta = ad.answer_extractive(Q_RECV, "2023/01/11 (Wed) 10:00")
        self.assertNotEqual(meta.get("gate"), "pp_duration")


if __name__ == "__main__":
    unittest.main()
