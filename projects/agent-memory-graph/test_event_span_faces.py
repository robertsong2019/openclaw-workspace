"""C571: event-span faces — take_after form + between same-date retry.

Two unbanked event-span siblings in the live-500 banked-score chain:
2c63a862 ("how many days did it take for me to find a house I loved
after starting to work with Rachel?" GT 14 — new take_after form,
span = latest(goal date) − earliest(onset date) over dated realized
lines) and gpt4_4fc4f797 ("how many days passed between the day I
received feedback ... and the day I tested ...?" GT 38 — between
same-date retry: the "planning to test ... next month" intent line
out-hit the realized "testing ... tomorrow" line and collapsed both
anchors onto 03-17; the intent-infinitive pool separates 03-17 /
04-24). Receive/order cousins stay out of take_after (b3c15d39 is
owned by the counting gate). Census: 16 banked between/before
siblings + 2 ago_when spot-checks byte-stable (probe_pre/post3).
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (answer_temporal_arith, temporal_arith_form,
                               temporal_arith_judge)


class TestTakeAfterForm(unittest.TestCase):
    def test_form_parses(self):
        kind, unit, a, b = temporal_arith_form(
            "How many days did it take for me to find a house I loved "
            "after starting to work with Rachel?")
        self.assertEqual(kind, "take_after")
        self.assertEqual(unit, "day")
        self.assertEqual(a, "find a house I loved")
        self.assertEqual(b, "starting to work with Rachel")

    def test_receive_order_excluded(self):
        # b3c15d39: owned by the counting gate (banked); order-side
        # lines are lexically ambiguous across unrelated orders.
        self.assertIsNone(temporal_arith_form(
            "How many days did it take for me to receive the new "
            "remote shutter release after I ordered it?"))

    def test_it_take_me_variant_excluded(self):
        # C570 route (h) owns "did it take (me|us) to finish/read";
        # the "for me to ... after" shape is what this form claims.
        self.assertIsNone(temporal_arith_form(
            "How many days did it take me to finish the novel?"))


class TestTakeAfterSpan(unittest.TestCase):
    Q = ("How many days did it take for me to find a house I loved "
         "after starting to work with Rachel?")

    LINES = [
        # state line out-hits the dated onset line on raw keywords —
        # the dated-realized subset must win (onset = earliest).
        ("[user] I've been working with a real estate agent, Rachel, "
         "and she's been helping me find a place that fits my needs.",
         "2022-03-02"),
        ("[user] Since I started working with her on 2/15, I'm hoping "
         "she can give me a heads up when something comes on the "
         "market", "2022-03-02"),
        # assistant echo out-hits the realized sighting — latest
        # dated goal line wins.
        ("[assistant] I can definitely help you find a house that "
         "you will love!", "2022-03-02"),
        ("[user] I recently saw a house that I really love on 3/1, "
         "and I'm considering making an offer", "2022-03-02"),
        ("[user] The house I saw on March 1st really checks all the "
         "boxes", "2022-03-02"),
    ]

    def test_span_14(self):
        ans, detail = answer_temporal_arith(self.Q, self.LINES,
                                            "2022/03/02 (Wed) 10:00")
        self.assertEqual(ans, "14 days")
        self.assertEqual(detail["dates"], ["2022-03-01", "2022-02-15"])
        self.assertEqual(detail["value"], 14)
        self.assertTrue(detail["span"])

    def test_judge_accepts_inclusive(self):
        self.assertTrue(temporal_arith_judge(
            self.Q, "14 days. 15 days (including the last day) is "
            "also acceptable.", "14 days"))

    def test_undated_pool_falls_back(self):
        # No dated realized lines at all → standard ladder, and no
        # fabricated span.
        lines = [("The house I saw really checks all the boxes",
                  "2022-03-02")]
        ans, _ = answer_temporal_arith(self.Q, lines,
                                       "2022/03/02 (Wed) 10:00")
        self.assertIsNone(ans)


class TestBetweenSameDateRetry(unittest.TestCase):
    Q = ("How many days passed between the day I received feedback "
         "about my car's suspension and the day I tested my new "
         "suspension setup?")

    LINES = [
        # 03-17: reference anchor — plan/echo lines carry the only
        # "feedback" mention; the user's own plan line is intent.
        ("[user] I've been getting feedback from judges that my "
         "car's suspension was too soft, so I installed new "
         "coilovers", "2023-03-17"),
        ("[user] I'm also planning to test my car's new suspension "
         "setup during an open track day at VIRginia International "
         "Raceway next month", "2023-03-17"),
        # 04-23: realized test day is "tomorrow" (04-24).
        ("[user] I'm preparing for an open track day at VIRginia "
         "International Raceway tomorrow, where I'll be testing my "
         "car's new suspension setup", "2023-04-23"),
    ]

    def test_retry_separates_38(self):
        ans, detail = answer_temporal_arith(self.Q, self.LINES,
                                            "2023/06/01 (Thu) 21:22")
        self.assertEqual(ans, "38 days")
        self.assertEqual(detail["dates"], ["2023-03-17", "2023-04-24"])
        self.assertEqual(detail["value"], 38)

    def test_no_collapse_no_retry_needed(self):
        # Banked-sibling shape: anchors resolve to distinct dates on
        # the plain pass (16-sibling byte-stability contract).
        q = ("How many days passed between the day I bought my new "
             "tennis racket and the day I received it?")
        lines = [
            ("[user] I bought my new tennis racket on March 10th",
             "2023-03-10"),
            ("[user] I received the new tennis racket on March "
             "17th and played my first match", "2023-03-17"),
        ]
        ans, detail = answer_temporal_arith(q, lines, "2023/04/01")
        self.assertEqual(ans, "7 days")
        self.assertEqual(detail["value"], 7)


if __name__ == "__main__":
    unittest.main()
