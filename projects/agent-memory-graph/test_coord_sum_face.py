"""C590: coordinated-sum faces — e3038f8c + 60036106 (one
mechanism, two noun-anchored heads).

Head 1: "How many rare items do I have in total?" Census (all
500): matches EXACTLY e3038f8c, unbanked WRONG (gate=counting via
number_total today). Evidence (user lines only, verbatim): per-
category rare-collection counts scattered across answer sessions —
'12 rare figurines' (s2), 'collection of 57 rare records' (s1 +
s2, consistent duplicate), '25 rare coins' (s3), 'rare books ...
collection of 5 books' (s4, same-sentence pairing) — 12+57+25+5
= 99 = GT.

Head 2: "What was the total number of people reached by my
Facebook ad campaign and Instagram influencer collaboration?"
Census (all 500): matches EXACTLY 60036106, unbanked WRONG
(number_total glued the '50 clicks' tail onto the sum → '2050').
Evidence (user lines only): 'reached around 2,000 people' (s1 +
s2, consistent duplicate) + 'promoted my product to her 10,000
followers' (s2) → 2,000+10,000 = '12,000' = GT. Noun anchoring
('people' / verb-anchored 'followers') excludes the clicks trap.

Guards pinned here:
- assistant prose dies on the user-role wall (coins/followers
  echoes live only in assistant lines in the decoy variants)
- conflicting value for one anchor → None (gates own abstention)
- missing coordination side / single category → None (falls
  through; number_total keeps its remaining rows untouched)
- same-sentence pairing only for the 'rare books ... 5 books'
  face; cross-sentence numbers never pair
- mechanism, not hardcoding: value mutations move the answer
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_coord_sum,
    answer_counting,
    counting_form,
    counting_judge,
)

Q_RARE = 'How many rare items do I have in total?'
Q_REACH = ('What was the total number of people reached by my '
           'Facebook ad campaign and Instagram influencer '
           'collaboration?')

# ── verbatim dataset lines (e3038f8c haystack) ──

U_RECORDS_S1 = ("Do you have any suggestions on how to create a "
                "catalog system for my 57 rare records?")
U_FIGURINES = ("Yeah, I have 12 rare figurines in my collection, "
               "and I'm always looking to improve my knowledge "
               "about them.")
U_RECORDS_S2 = "I'm excited to add it to my collection of 57 rare records."
U_COINS = ("I actually have 25 rare coins that I need to store "
           "safely, so I'll definitely consider those factors when "
           "choosing between a fireproof safe and a safety deposit "
           "box.")
U_BOOKS = ("By the way, I've been collecting rare books for a "
           "while now and have a small but valuable collection of "
           "5 books.")
A_COINS_ECHO = ("With 25 rare coins, you'll want to ensure they're "
                "stored in a secure and protected environment to "
                "preserve their value and condition.")
A_BOOKS_ECHO = ("As for your collection of 5 rare books, it's "
                "great that you're taking steps to authenticate "
                "and conserve them.")
U_RARE_DECOY = ("I've had some experience with rare vinyl records "
                "too.")

# ── verbatim dataset lines (60036106 haystack) ──

U_REACH_S1 = ("By the way, my previous ad campaign, which ran for "
              "five days, reached around 2,000 people.")
U_FOLL = ("By the way, I recently collaborated with an influencer "
          "who promoted my product to her 10,000 followers, and it "
          "was a great success.")
U_REACH_S2 = ("I'm planning to target people who have shown "
              "interest in similar products to mine, just like I "
              "did in my previous Facebook ad campaign, which "
              "reached around 2,000 people and resulted in 50 "
              "clicks to my website.")
A_REACH_ECHO = ("Considering your previous campaign reached 2,000 "
                "people and resulted in 50 clicks to your website, "
                "that's a decent click-through rate (CTR) of 2.5%.")


def sess(*turns):
    return [{"session_id": "session_1", "turns": list(turns)}]


def multi(*sessions):
    return [{"session_id": f"session_{i+1}", "turns": list(t)}
            for i, t in enumerate(sessions)]


def u(text):
    return {"role": "user", "content": text}


def a(text):
    return {"role": "assistant", "content": text}


RARE_REAL = multi(
    [u(U_RECORDS_S1)],
    [u(U_FIGURINES), u(U_RECORDS_S2)],
    [u(U_COINS), a(A_COINS_ECHO)],
    [u(U_BOOKS), a(A_BOOKS_ECHO)],
    [u(U_RARE_DECOY)],
)

REACH_REAL = multi(
    [u(U_REACH_S1)],
    [u(U_FOLL), u(U_REACH_S2), a(A_REACH_ECHO)],
)

# ── form ──

class TestForm(unittest.TestCase):

    def test_form_rare_head(self):
        self.assertEqual(counting_form(Q_RARE), "coord_sum")

    def test_form_reach_head(self):
        self.assertEqual(counting_form(Q_REACH), "coord_sum")

    def test_generic_total_rows_untouched(self):
        # banked protection: number_total keeps every other row
        self.assertEqual(
            counting_form("How many total books do I own?"),
            "number_total")
        self.assertEqual(
            counting_form("What is the total number of employees?"),
            "number_total")


# ── rare-items head ──

class TestRareItemsSum(unittest.TestCase):

    def test_real_fixture_sum_99(self):
        self.assertEqual(_cnt_coord_sum(Q_RARE, RARE_REAL), "99")
        ans, detail = answer_counting(Q_RARE, RARE_REAL)
        self.assertEqual(ans, "99")
        self.assertEqual(detail, {"form": "coord_sum"})

    def test_duplicate_consistent(self):
        # drop the s2 57-records line; s1's 57 still counts once
        fx = multi([u(U_RECORDS_S1)], [u(U_FIGURINES)],
                   [u(U_COINS)], [u(U_BOOKS)])
        self.assertEqual(_cnt_coord_sum(Q_RARE, fx), "99")

    def test_conflict_is_ambiguous(self):
        # MUTATION (declared): 58 records contradicts 57 → None
        fx = multi([u(U_RECORDS_S1)], [u(U_FIGURINES)],
                   [u(U_RECORDS_S2.replace("57", "58"))],
                   [u(U_COINS)], [u(U_BOOKS)])
        self.assertIsNone(_cnt_coord_sum(Q_RARE, fx))

    def test_same_sentence_pairing(self):
        # the books face: 'rare books' + '5 books' in ONE sentence
        fx = multi([u(U_FIGURINES)], [u(U_BOOKS)])
        self.assertEqual(_cnt_coord_sum(Q_RARE, fx), "17")

    def test_pairing_is_same_sentence_only(self):
        # MUTATION (declared): the number lives in another
        # sentence — no pairing across sentences
        split = ("I've been collecting rare books for a while "
                 "now. And I have 5 books.")
        fx = multi([u(U_FIGURINES)], [u(split)])
        self.assertIsNone(_cnt_coord_sum(Q_RARE, fx))

    def test_user_role_wall(self):
        # coin count only in the assistant echo → not counted
        # (wall failure would inflate 12+5 → 42)
        fx = multi([a(A_COINS_ECHO)], [u(U_FIGURINES)],
                   [u(U_BOOKS)])
        self.assertEqual(_cnt_coord_sum(Q_RARE, fx), "17")

    def test_single_category_not_coordinated(self):
        # falls through — a lone category is number_total's lane
        fx = multi([u(U_FIGURINES)])
        self.assertIsNone(_cnt_coord_sum(Q_RARE, fx))

    def test_mechanism_not_hardcoded(self):
        # MUTATION (declared): 12 → 13 moves the sum
        fx = multi([u(U_RECORDS_S1)],
                   [u(U_FIGURINES.replace("12", "13"))],
                   [u(U_COINS)], [u(U_BOOKS)])
        self.assertEqual(_cnt_coord_sum(Q_RARE, fx), "100")

    def test_rare_decoy_without_numbers_ignored(self):
        fx = multi([u(U_RECORDS_S1)], [u(U_FIGURINES)],
                   [u(U_RARE_DECOY)])
        self.assertEqual(_cnt_coord_sum(Q_RARE, fx), "69")


# ── reach head ──

class TestReachSum(unittest.TestCase):

    def test_real_fixture_reach_12000(self):
        self.assertEqual(_cnt_coord_sum(Q_REACH, REACH_REAL),
                         "12,000")
        ans, detail = answer_counting(Q_REACH, REACH_REAL)
        self.assertEqual(ans, "12,000")
        self.assertEqual(detail, {"form": "coord_sum"})

    def test_clicks_trap_excluded(self):
        # the '50 clicks' tail inside the reach sentence never
        # enters the sum (noun anchoring: people/followers only)
        fx = multi([u(U_REACH_S1), u(U_FOLL), u(U_REACH_S2)])
        self.assertEqual(_cnt_coord_sum(Q_REACH, fx), "12,000")

    def test_missing_side_falls_through(self):
        fx = multi([u(U_REACH_S1)])
        self.assertIsNone(_cnt_coord_sum(Q_REACH, fx))

    def test_conflict_is_ambiguous(self):
        # MUTATION (declared): second reach line says 3,000
        fx = multi([u(U_REACH_S1)], [u(U_FOLL),
                                    u(U_REACH_S2.replace("2,000",
                                                         "3,000"))])
        self.assertIsNone(_cnt_coord_sum(Q_REACH, fx))

    def test_user_role_wall(self):
        # reach only in the assistant echo → not counted
        fx = multi([a(A_REACH_ECHO)], [u(U_FOLL)])
        self.assertIsNone(_cnt_coord_sum(Q_REACH, fx))


# ── judge (numeric-first) ──

class TestJudge(unittest.TestCase):

    def test_comma_style_matches_gt(self):
        self.assertTrue(
            counting_judge(Q_REACH, "12,000", "12,000"))
        self.assertTrue(counting_judge(Q_REACH, "12000", "12,000"))

    def test_wrong_sum_rejected(self):
        self.assertFalse(counting_judge(Q_REACH, "12,000", "2,050"))
        self.assertFalse(counting_judge(Q_RARE, "99", "94"))


if __name__ == "__main__":
    unittest.main()
