"""Cycle 577 — named-holiday entity face (holiday_entity gate).

"What was the airline that I flied with on Valentine's day?" is
answered by the airline bound in a REALIZED-flight user line inside
a session dated on the holiday itself: the fixed-date holiday table
resolves Valentine's day to the most recent 02-14 at or before the
question date (2023/03/02 -> 2023/02/14), and session_30 of the real
pool ("still recovering from my American Airlines flight from LAX to
JFK", "had a bad experience with American Airlines' ...") answers
American Airlines while the same-session booking intents ("leaning
towards the JetBlue option", "I think I'll book the return flight on
Delta") never match the realized markers.

Census (/tmp/c577/step5): the shipped form regex accepts exactly
1/500 questions; the only holiday mention in the whole 500 is the
target itself (c8090214 "Holiday Market" is a proper noun, not a
table holiday). gpt4_f420262c ("order of airlines I flew with") is
structurally disjoint — no "that i" relative clause.

Guards: unknown/moveable holiday (Easter, Thanksgiving) -> honest
fall-through; zero or 2+ distinct realized airlines -> fall-through;
assistant-role wall (user lines only); wrong-date sessions excluded.
Gate answers a plain entity string, so the default exact_judge
branch owns the verdict (GT "American Airlines" is an exact match).
"""

import unittest

from amg_bench_quality import (
    _HOLIDAY_FLEW_RE,
    _HOLIDAY_MD,
    _resolve_holiday_date,
    answer_holiday_entity,
)

QUESTION = "What was the airline that I flied with on Valentine's day?"
QDATE = "2023/03/02 (Thu) 08:00"

# ── verbatim real-row replica (gpt4_f420262d, sessions 30+31) ──
# session_30 (2023/02/14 20:47): the realized American Airlines
# lines AND the same-session booking intents in their exact wording.
S30_USER_LINES = [
    "I'm looking to book a new flight from Boston to Miami, and I "
    "was wondering if you could help me find the best deals. By the "
    "way, I'm still recovering from my American Airlines flight from "
    "LAX to JFK, which was delayed by 2 hours due to bad weather "
    "conditions.",
    "I'm leaning towards the JetBlue option from BOS to FLL, but I'm "
    "a bit worried about the lack of seat selection and limited "
    "amenities. Can you tell me more about their seat selection "
    "process and what kind of amenities I can expect on this flight? "
    "Also, since I had a bad experience with American Airlines' "
    "in-flight entertainment system on my previous flight from New "
    "York to Los Angeles, I'd like to know if JetBlue's system is "
    "any better.",
    "I think I'll book the return flight on Delta and hope to "
    "upgrade using my SkyMiles. Can you book the flight for me and "
    "also remind me to check the upgrade options regularly? "
    "Additionally, I'd like to know if there's any way to get "
    "notified if an upgrade becomes available.",
]
S30_ASSISTANT_LINE = (
    "Sorry to hear that your last flight with American Airlines was "
    "delayed due to bad weather conditions! I'm happy to help you "
    "find a better experience for your upcoming flight from Boston "
    "to Miami.")


def _dated_pool(*triples):
    """[(line, sdate)] pairs in the _dated() wire format — the role
    prefix is part of the line text (adapter wiring contract)."""
    return [(f"[{role}] {content}", sdate)
            for role, content, sdate in triples]


class HolidayFormTests(unittest.TestCase):
    def test_form_accepts_target(self):
        m = _HOLIDAY_FLEW_RE.match(QUESTION)
        self.assertIsNotNone(m)
        self.assertEqual(m.group("hol").lower().strip(), "valentine's day")

    def test_form_rejects_order_sibling(self):
        # gpt4_f420262c — no "that i" relative clause
        self.assertIsNone(_HOLIDAY_FLEW_RE.match(
            "What is the order of airlines I flew with from earliest "
            "to latest before today?"))

    def test_form_rejects_holiday_market(self):
        # c8090214 — "Holiday Market" is a proper noun, no flew frame
        self.assertIsNone(_HOLIDAY_FLEW_RE.match(
            "How many days before I bought the iPhone 13 Pro did I "
            "attend the Holiday Market?"))

    def test_holiday_table_fixed_dates_only(self):
        names = dict(_HOLIDAY_MD)
        self.assertEqual(names["valentine"], (2, 14))
        self.assertEqual(names["new year's eve"], (12, 31))
        self.assertEqual(names["christmas"], (12, 25))
        # no moveable holidays — they must fall through honestly
        for moveable in ("easter", "thanksgiving", "memorial day"):
            self.assertNotIn(moveable, names)

    def test_resolution_most_recent_past(self):
        self.assertEqual(
            _resolve_holiday_date("Valentine's day", "2023-03-02"),
            "2023-02-14")

    def test_resolution_previous_year(self):
        self.assertEqual(
            _resolve_holiday_date("Valentine's day", "2023-01-05"),
            "2022-02-14")

    def test_resolution_unknown_holiday_falls_through(self):
        self.assertIsNone(_resolve_holiday_date("Easter Monday",
                                                "2023-03-02"))
        self.assertIsNone(_resolve_holiday_date("Thanksgiving",
                                                "2023-03-02"))

    def test_resolution_empty_question_date(self):
        self.assertIsNone(_resolve_holiday_date("Valentine's day", ""))


class HolidayAnswerTests(unittest.TestCase):
    def test_real_row_rescued(self):
        pool = _dated_pool(
            *[("user", ln, "2023/02/14 (Tue) 20:47")
              for ln in S30_USER_LINES])
        ans, detail = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertEqual(ans, "American Airlines")
        self.assertEqual(detail["holiday_date"], "2023-02-14")
        self.assertEqual(detail["airlines"], ["American Airlines"])

    def test_assistant_line_never_binds(self):
        pool = _dated_pool(
            ("assistant", S30_ASSISTANT_LINE, "2023/02/14 (Tue) 20:47"))
        ans, detail = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertIsNone(ans)
        self.assertEqual(detail["airlines"], [])

    def test_wrong_date_session_excluded(self):
        # the NY->LA "today" flight narrative also exists on 02/20
        # (session_35) — a session NOT on the holiday must never bind
        pool = _dated_pool(
            ("user",
             "I'm planning a trip to Miami and I'm considering flying "
             "with American Airlines. What's their in-flight "
             "entertainment system like? By the way, I had a terrible "
             "experience with it on my flight from New York to Los "
             "Angeles today.",
             "2023/02/20 (Mon) 18:00"))
        ans, _ = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertIsNone(ans)

    def test_booking_intent_lines_never_bind(self):
        pool = _dated_pool(
            ("user",
             "I'm leaning towards the JetBlue option from BOS to FLL.",
             "2023/02/14 (Tue) 20:47"),
            ("user",
             "I think I'll book the return flight on Delta and hope "
             "to upgrade using my SkyMiles.",
             "2023/02/14 (Tue) 20:47"))
        ans, detail = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertIsNone(ans)
        self.assertEqual(detail["airlines"], [])

    def test_two_realized_airlines_ambiguous(self):
        pool = _dated_pool(
            ("user",
             "Still recovering from my American Airlines flight from "
             "LAX to JFK.",
             "2023/02/14 (Tue) 20:47"),
            ("user",
             "I had a bad experience with United Airlines on my "
             "previous trip.",
             "2023/02/14 (Tue) 20:47"))
        ans, detail = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertIsNone(ans)
        self.assertEqual(sorted(detail["airlines"]),
                         ["American Airlines", "United Airlines"])

    def test_no_holiday_date_binding_without_match(self):
        # no session on the resolved date -> honest fall-through
        pool = _dated_pool(
            ("user",
             "Still recovering from my American Airlines flight.",
             "2023/02/20 (Mon) 18:00"))
        ans, _ = answer_holiday_entity(QUESTION, pool, QDATE)
        self.assertIsNone(ans)

    def test_unparseable_question_date_falls_through(self):
        pool = _dated_pool(
            ("user",
             "Still recovering from my American Airlines flight from "
             "LAX to JFK.",
             "2023/02/14 (Tue) 20:47"))
        ans, _ = answer_holiday_entity(QUESTION, pool, "")
        self.assertIsNone(ans)


class HolidayAdapterTests(unittest.TestCase):
    def test_adapter_gate_wired(self):
        from amg_bench_quality import LongMemEvalAdapter
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "user", "content": ln}
                  for ln in S30_USER_LINES]}],
            session_dates={"session_1": "2023/02/14 (Tue) 20:47"})
        ans, meta = ad.answer_extractive(QUESTION, QDATE)
        self.assertEqual(ans, "American Airlines")
        self.assertEqual(meta.get("gate"), "holiday_entity")

    def test_adapter_nonmatch_untouched(self):
        from amg_bench_quality import LongMemEvalAdapter
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "user", "content": "hello there"}]}],
            session_dates={"session_1": "2023/02/14 (Tue) 20:47"})
        ans, meta = ad.answer_extractive(
            "What is the order of airlines I flew with from earliest "
            "to latest before today?", QDATE)
        self.assertNotEqual(meta.get("gate"), "holiday_entity")


if __name__ == "__main__":
    unittest.main()
