"""C572: before-buy named-day face — c8090214 + _abs (one family).

Head: "How many days before I bought the iPhone 13 Pro did I attend
the Holiday Market?"

Census (all 500): the strict buy/attend before-shape matches EXACTLY
2 rows (c8090214 + c8090214_abs), both unbanked today — the Cycle-482
between path needs absolute in-text dates; this family dates its two
events by a NAMED DAY plus a relative offset instead:
- purchase fact: s15 "I got my iPhone 13 Pro at a discounted price of
  $800 from Best Buy on Black Friday, ..."
- event fact:    s28 "I attended the annual Holiday Market at the
  local mall a week before Black Friday, ..."  (×2, same value)
→ offset = 7 days = GT '7 days. 8 days (including the last day) is
also acceptable.' — banked via the exact-number judge face ({7} ⊆
{7, 8}).

The _abs sibling asks the same about an iPad; the haystack never
mentions buying one → unresolved → fall-through (pred unchanged;
its GT asserts the missing premise and its banked flag is frozen).

Guards pinned here:
- assistant lines die on the user-role wall (both sides)
- buy-side binding is keyword-gated: s15's TV lines say "on Cyber
  Monday" but carry no iPhone keywords → never bind (kill-audit pin)
- event offsets must name the SAME day as the purchase anchor
  (Black Friday ≠ Cyber Monday → fall-through)
- conflicting offsets (two distinct values) → fall-through
- month offsets are ambiguous → fall-through; week↔day convert only
  on exact 7-day multiples
- no purchase-side named day → fall-through
- number-word offsets ("two days") parse
"""
import importlib.util
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# importlib two-module discipline (C568 lesson #3)
_SPEC = importlib.util.spec_from_file_location(
    "amgq_test_c572",
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "amg_bench_quality.py"))
_mod = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _mod
_SPEC.loader.exec_module(_mod)

Q_IPHONE = ("How many days before I bought the iPhone 13 Pro did I "
            "attend the Holiday Market?")
Q_IPHONE_ABS = ("How many days before I bought my iPad did I attend "
                "the Holiday Market?")
Q_IPHONE_WK = ("How many weeks before I bought the iPhone 13 Pro did "
               "I attend the Holiday Market?")
Q_MOVED = ("How many days before I moved to Seattle did I adopt "
           "Luna?")

# ── verbatim real-row lines (c8090214 s15/s28, c8090214_abs s37/s40) ──

IPHONE_BUY = ("I'm looking to upgrade my phone case and screen "
              "protector. Can you show me some options for iPhone 13 "
              "Pro cases and screen protectors? By the way, I got my "
              "iPhone 13 Pro at a discounted price of $800 from Best "
              "Buy on Black Friday, which was a great deal "
              "considering the regular price was $1,000.")
TV_CYBER_1 = ("I'm looking for a TV with good picture quality and "
              "HDR support. I scored an amazing deal on a 4K TV from "
              "Amazon on Cyber Monday, getting 30% off the original "
              "price of $1,200. Can you show me some TV models with "
              "similar features and price points?")
TV_CYBER_2 = ("I'm looking for a TV with a similar price point to "
              "what I got on Cyber Monday, around $800-$1,000. Can "
              "you show me some TV models with good picture quality "
              "and HDR support in that price range?")
MARKET_1 = ("I'm looking for some gift ideas for my sister's "
            "birthday, which is coming up soon. I'd like to get her "
            "something nice, but I'm on a budget. Do you have any "
            "suggestions? By the way, I attended the annual Holiday "
            "Market at the local mall a week before Black Friday, "
            "and I saw some unique handmade jewelry there, but I'm "
            "not sure if that's her style.")
MARKET_2 = ("I think I'll keep it simple and add her name in a "
            "elegant font, and maybe a small message like \"Sis\" or "
            "\"Birthday Girl\" to make it more personal. I don't "
            "want to overwhelm the design, but still make it "
            "special. By the way, speaking of birthdays, I attended "
            "the annual Holiday Market at the local mall a week "
            "before Black Friday, and I saw some unique handmade "
            "jewelry there that I think she might like. Do you think "
            "I should consider getting her a piece of jewelry to go "
            "along with the phone case?")
MARKET_3 = ("I think I'll go back to the Holiday Market and take a "
            "closer look at the jewelry vendors. I remember seeing a "
            "few pieces that caught my eye, but I wasn't sure if "
            "they were the right fit for my sister. Now that I have "
            "a better idea of what I'm looking for, I can take a "
            "closer look and see if I can find the perfect piece to "
            "go along with the phone case. Thanks for the advice!")
ASSIST_ECHO = ("Congratulations on scoring a great deal on your "
               "iPhone 13 Pro! The annual Holiday Market a week "
               "before Black Friday sounds lovely.")

QDATE = "2023/12/10 (Sun) 17:17"


def _dl(*rows):
    """Build answer_temporal_arith dated_lines from (role, date, txt)."""
    return [(f"[{role}] {txt}", date) for role, date, txt in rows]


# Reality (step5 census): the WHOLE haystack shares one session date
# (2023-12-10; only times differ) — calendar arithmetic has nothing
# to subtract and the same-date guards abstain. Replica mirrors that.
D_SAME = "2023-12-10"

REAL_FULL = _dl(
    ("user", D_SAME, IPHONE_BUY),
    ("user", D_SAME, TV_CYBER_1),
    ("user", D_SAME, TV_CYBER_2),
    ("user", D_SAME, MARKET_1),
    ("user", D_SAME, MARKET_2),
    ("user", D_SAME, MARKET_3),
    ("assistant", D_SAME, ASSIST_ECHO),
)


class BeforeBuyForm(unittest.TestCase):
    def test_form_claims_iphone_row(self):
        self.assertEqual(_mod.temporal_arith_form(Q_IPHONE),
                         ("before_buy", "day", "the iPhone 13 Pro",
                          "the Holiday Market"))

    def test_form_claims_abs_row(self):
        self.assertEqual(_mod.temporal_arith_form(Q_IPHONE_ABS)[0],
                         "before_buy")

    def test_form_unit_week(self):
        self.assertEqual(_mod.temporal_arith_form(Q_IPHONE_WK)[1],
                         "week")

    def test_plain_before_stays_between(self):
        # the Cycle-482 family keeps its route (zero-kill pin)
        self.assertEqual(_mod.temporal_arith_form(Q_MOVED)[0],
                         "between")


class BeforeBuyHandler(unittest.TestCase):
    def test_real_replica_answers_seven_days(self):
        ans, det = _mod.answer_temporal_arith(Q_IPHONE, REAL_FULL, QDATE)
        self.assertEqual(ans, "7 days")
        self.assertEqual(det["value"], 7)

    def test_tv_lines_do_not_bind(self):
        # kill-audit pin: TV rows name Cyber Monday but bind nothing
        ans, _ = _mod.answer_temporal_arith(
            Q_IPHONE, _dl(("user", D_SAME, TV_CYBER_1),
                          ("user", D_SAME, TV_CYBER_2),
                          ("user", D_SAME, MARKET_1)), QDATE)
        self.assertIsNone(ans)

    def test_abs_row_falls_through_without_ipad(self):
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE_ABS, REAL_FULL,
                                            QDATE)
        self.assertIsNone(ans)

    def test_assistant_purchase_line_dies_on_role_wall(self):
        rows = _dl(("assistant", D_SAME, IPHONE_BUY),
                   ("user", D_SAME, MARKET_1))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_assistant_event_line_dies_on_role_wall(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("assistant", D_SAME, MARKET_1))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_conflicting_offsets_fall_through(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME, MARKET_1),
                   ("user", D_SAME,
                    "I attended the Holiday Market two days before "
                    "Black Friday with Emma."))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_mismatched_named_day_falls_through(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME,
                    "I attended the Holiday Market at the local mall "
                    "a week before Cyber Monday."))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_missing_purchase_day_falls_through(self):
        rows = _dl(("user", D_SAME,
                    "I got my iPhone 13 Pro at a discounted price of "
                    "$800 from Best Buy, which was a great deal."),
                   ("user", D_SAME, MARKET_1))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_month_offset_is_ambiguous(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME,
                    "I attended the Holiday Market a month before "
                    "Black Friday."))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertIsNone(ans)

    def test_number_word_offset(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME,
                    "I attended the Holiday Market at the local mall "
                    "two days before Black Friday."))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE, rows, QDATE)
        self.assertEqual(ans, "2 days")

    def test_week_unit_render(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME, MARKET_1))
        ans, det = _mod.answer_temporal_arith(Q_IPHONE_WK, rows, QDATE)
        self.assertEqual(ans, "1 week")
        self.assertEqual(det["value"], 1)

    def test_week_unit_inexact_conversion_falls_through(self):
        rows = _dl(("user", D_SAME, IPHONE_BUY),
                   ("user", D_SAME,
                    "I attended the Holiday Market at the local mall "
                    "three days before Black Friday."))
        ans, _ = _mod.answer_temporal_arith(Q_IPHONE_WK, rows, QDATE)
        self.assertIsNone(ans)


class JudgeAndDispatch(unittest.TestCase):
    GT = ("7 days. 8 days (including the last day) is also "
          "acceptable.")

    def test_semantic_judge_credits_seven_days(self):
        self.assertEqual(
            _mod.judge_semantic(Q_IPHONE, "7 days", self.GT),
            "CORRECT")

    def test_semantic_judge_veto_wrong_number(self):
        self.assertEqual(
            _mod.judge_semantic(Q_IPHONE, "14 days", self.GT),
            "WRONG")


if __name__ == "__main__":
    unittest.main()
