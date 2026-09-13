"""C573: trip-span face — gpt4_1d80365e (one session-date family).

Head (route t): "How many days did I spend on my solo camping trip
to Yosemite National Park?"

Census (all 500): the strict ``how many <unit> did (i|we) spend on
(my|our) <descriptor> trip`` head matches EXACTLY 1 row, unbanked
(gpt4_1d80365e). No _abs sibling (verified in frozen). Zero-kill by
construction: the banked in-total sum (edced276 "spend in total
traveling in Hawaii and … NYC") puts ``in total`` before the
descriptor and stays out, as do the take-breaks total (6cb6f249
"did I take"), the participating/attending frames (5a7937c8,
10d9b85a) and the how-long cousin (19b5f2b3).

Evidence path (verbatim real-row lines, s14/s33):
- start fact:  s14 @2023-05-15  "…I just started my solo camping
  trip to Yosemite National Park today…"
- finish fact: s33 @2023-05-17  "…I just got back from an amazing
  solo camping trip to Yosemite National Park today…"
→ 2023-05-17 − 2023-05-15 = 2 days = GT '2 days. 3 days (including
the last day) is also acceptable.' — banked via the exact-number
judge face ({2} ⊆ {2, 3}; C572 {7} ⊆ {7, 8} precedent). Route-(h)
family: the span IS the duration, no duration expressions needed.

Guards pinned here:
- assistant echo of the start fact dies on the user-role wall
  (C482 trust tiers) AND carries no ``today`` — double protection
- the "I will be camping at Yosemite National Park for a few days"
  future-aspiration line has no start/return marker → never binds
- the s6 "just got back from an amazing music festival in Brooklyn"
  decoy carries the return marker but fails the all-keywords wall
  (no solo/camping/yosemite) → never binds
- keyword binding is an ALL-keywords wall (route (c) discipline):
  partial descriptor matches are forbidden
- 0 start / 0 finish / same-sitting (0 days) / negative span all
  fall through honestly
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

# importlib two-module discipline (C568 lesson #3)
_SPEC = importlib.util.spec_from_file_location(
    "amgq_test_c573",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "amg_bench_quality.py"))
_mod = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _mod
_SPEC.loader.exec_module(_mod)

Q_TRIP = ("How many days did I spend on my solo camping trip to "
          "Yosemite National Park?")
Q_TRIP_WEEKS = ("How many weeks did I spend on my solo camping trip "
                "to Yosemite National Park?")
Q_TRIP_BARE = ("How many days did I spend on my trip to Yosemite "
               "National Park?")
Q_IN_TOTAL = ("How many days did I spend in total traveling in "
              "Hawaii and in New York City?")            # edced276
Q_TAKE = "How many days did I take social media breaks in total?"  # 6cb6f249
Q_PARTICIPATE = ("How many days did I spend participating in "
                 "faith-related activities in December?")  # 5a7937c8
Q_ATTEND = ("How many days did I spend attending workshops, "
            "lectures, and conferences in April?")        # 10d9b85a
Q_JAPAN = "How long was I in Japan for?"                  # 19b5f2b3

# ── verbatim real-row lines (gpt4_1d80365e s14/s33 + decoys) ──

TRIP_START = ("I'm planning a trip to the Eastern Sierra in July or "
              "August and was wondering if you could recommend some "
              "scenic hiking trails in the area. By the way, I just "
              "started my solo camping trip to Yosemite National "
              "Park today and I'm really excited to explore the "
              "park.")
TRIP_FINISH = ("I'm thinking of planning a trip to the Eastern "
               "Sierra in July or August and I was wondering if you "
               "could recommend some good camping spots and hiking "
               "trails in the area. By the way, I just got back "
               "from an amazing solo camping trip to Yosemite "
               "National Park today, and I'm already itching to "
               "get back out into the mountains.")
ASSIST_ECHO = ("That sounds like an amazing adventure! "
               "Congratulations on starting your solo camping trip "
               "to Yosemite National Park! I'm sure you'll have an "
               "incredible time exploring one of the most beautiful "
               "national parks in the US.")
CAMP_ASPIRE = ("That's really helpful, thanks! I'll make sure to "
               "reserve a campsite in advance to ensure I have a "
               "spot. By the way, I'm really excited to start my "
               "hike to Mount Whitney, but I'm also a bit nervous "
               "about the altitude sickness. Since I will be "
               "camping at Yosemite National Park for a few days, "
               "do you think I'll be somewhat acclimated to the "
               "high elevation?")
MUSIC_DECOY = ("I'm trying to keep track of all the concerts I've "
               "been to and plan for upcoming ones. Can you help "
               "me organize my music events calendar? By the way, "
               "I just got back from an amazing music festival in "
               "Brooklyn on March 5th with friends from college, "
               "and it was such a great experience.")

D_START, D_MID, D_END = "2023-05-15", "2023-05-16", "2023-05-17"


def _sess(*rows):
    """[(date, content)] → pp-gate sessions (string dates; the
    dispatcher owns parsing — C570 discipline)."""
    return [(d, [{"role": "user", "content": c}]) for d, c in rows]


REAL_FULL = _sess(
    (D_START, TRIP_START),
    (D_START, CAMP_ASPIRE),
    (D_END, TRIP_FINISH),
    (D_END, MUSIC_DECOY),
)


class FormGates(unittest.TestCase):
    def test_form_claims_real(self):
        self.assertTrue(_mod.pp_trip_span_form(Q_TRIP))

    def test_form_unit_weeks(self):
        self.assertTrue(_mod.pp_trip_span_form(Q_TRIP_WEEKS))

    def test_form_bare_descriptor(self):
        self.assertTrue(_mod.pp_trip_span_form(Q_TRIP_BARE))

    def test_in_total_sum_stays_out(self):
        # edced276 zero-kill pin: banked counting row keeps its lane
        self.assertFalse(_mod.pp_trip_span_form(Q_IN_TOTAL))

    def test_take_breaks_stays_out(self):
        self.assertFalse(_mod.pp_trip_span_form(Q_TAKE))

    def test_participating_frame_stays_out(self):
        self.assertFalse(_mod.pp_trip_span_form(Q_PARTICIPATE))

    def test_attending_frame_stays_out(self):
        self.assertFalse(_mod.pp_trip_span_form(Q_ATTEND))

    def test_how_long_cousin_stays_out(self):
        self.assertFalse(_mod.pp_trip_span_form(Q_JAPAN))


class TripSpanHandler(unittest.TestCase):
    def test_real_replica_two_days(self):
        ans, det = _mod.answer_pp_duration(Q_TRIP, REAL_FULL)
        self.assertEqual(ans, "2 days")
        self.assertEqual(det["route"], "trip_span")
        self.assertEqual(det["days"], 2)

    def test_no_finish_fact(self):
        rows = _sess((D_START, TRIP_START), (D_START, CAMP_ASPIRE))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_no_start_fact(self):
        rows = _sess((D_END, TRIP_FINISH), (D_END, MUSIC_DECOY))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_same_sitting_falls_through(self):
        rows = _sess((D_MID, TRIP_START), (D_MID, TRIP_FINISH))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_negative_span_falls_through(self):
        rows = _sess((D_END, TRIP_START), (D_START, TRIP_FINISH))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_keyword_wall_partial_bind_forbidden(self):
        # "solo camping trip" without the location words: the
        # all-keywords wall rejects partial descriptor matches
        rows = _sess(
            (D_START, "I just started my solo camping trip today "
                      "and the weather is great."),
            (D_END, "I just got back from my solo camping trip "
                    "today, pretty tired."))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_assistant_start_dies_on_role_wall(self):
        rows = _sess((D_START, ASSIST_ECHO), (D_END, TRIP_FINISH))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_assistant_finish_dies_on_role_wall(self):
        rows = _sess((D_START, TRIP_START), (D_END, ASSIST_ECHO))
        ans, _ = _mod.answer_pp_duration(Q_TRIP, rows)
        self.assertIsNone(ans)

    def test_future_aspiration_does_not_bind(self):
        # kill-audit pin: the "will be camping … for a few days"
        # line carries keywords but no start/return marker — the
        # replica still resolves to 2 days with it present
        ans, _ = _mod.answer_pp_duration(Q_TRIP, REAL_FULL)
        self.assertEqual(ans, "2 days")

    def test_music_festival_decoy_does_not_bind(self):
        # return marker without descriptor keywords → wall holds
        ans, _ = _mod.answer_pp_duration(Q_TRIP, REAL_FULL)
        self.assertEqual(ans, "2 days")

    def test_weeks_render(self):
        rows = _sess(
            (D_START, TRIP_START),
            ("2023-05-29", TRIP_FINISH))  # 14 days
        ans, _ = _mod.answer_pp_duration(Q_TRIP_WEEKS, rows)
        self.assertEqual(ans, "2 weeks")


class AdapterWired(unittest.TestCase):
    """Production pin: the wired path through ingest_sessions +
    answer_extractive — gate entry, date threading, attribution."""

    def test_head_t(self):
        ad = _mod.LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "user", "content": TRIP_START}]},
             {"session_id": "session_2",
              "messages": [{"role": "user",
                            "content": "How is the weather today?"}]},
             {"session_id": "session_3",
              "messages": [{"role": "user", "content": TRIP_FINISH}]}],
            session_dates={"session_1": D_START,
                           "session_2": D_MID,
                           "session_3": D_END})
        ans, meta = ad.answer_extractive(Q_TRIP,
                                         "2023/05/20 (Sat) 09:09")
        self.assertEqual(ans, "2 days")
        self.assertEqual(meta["gate"], "pp_duration")

    def test_banked_cousins_keep_routing(self):
        # zero-kill pin: edced276's in-total frame never enters the
        # trip form (banked counting row stays byte-stable)
        self.assertFalse(_mod.pp_trip_span_form(Q_IN_TOTAL))
        self.assertFalse(_mod.pp_trip_span_form(Q_PARTICIPATE))
        self.assertFalse(_mod.pp_trip_span_form(Q_ATTEND))


if __name__ == "__main__":
    unittest.main(verbosity=2)
