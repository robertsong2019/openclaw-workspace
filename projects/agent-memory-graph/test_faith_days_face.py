"""C601: faith_days face — December faith-activity day count
(5a7937c8, GT '3 days.', qtype multi-session).

One face, one mechanism (triple wall on a user sentence,
honorific-merged grain):

- faith_days (5a7937c8, GT '3 days.'): "How many days did I
  spend participating in faith-related activities in
  December?" — a user sentence yields a December day when it
  carries ALL of: a faith-activity term (church|midnight
  mass|bible study|worship|prayer service), a past-
  participation verb ('helped out' / 'got back from' / 'did'),
  and an explicit 'December <day>' anchor. The three real
  days: Dec 10 church holiday food drive (helped out), Dec 17
  Bible study at my church (did), Dec 24 midnight mass at
  St. Mary's Church (got back from). The Dec 24 sentence
  splits at the 'St.' abbreviation — _map_sents honorific
  repair re-joins it (C599 mechanism, load-bearing here).
  Distinct days are additive; same-day re-mentions dedup.

Census (all 500): the strict head matches EXACTLY 1 row
(5a7937c8), unbanked today (gate=answer — the pred was a
volunteer-echo sentence with no number). Claimed in
counting_form AHEAD of the generic how-many-days duration_sum
block (the head contains 'how many days'; duration_sum
resolves None on this evidence today). Near-miss faith
questions (gpt4_b5700ca9 'days ago ... Maundy Thursday',
08f4fc43 / 2a1811e2 'days had passed between ... mass') keep
their temporal-arithmetic routing.

Decoy discipline (pinned per-turn below):
- Dec 12 Le Creuset / Coach store runs — December day but no
  faith term (topic wall)
- future intent "Bible study I'm leading next week" — faith
  term but no December day (date wall)
- "thinking of doing something ... like the midnight mass at
  St. Mary's Church" — no date, no past-participation verb
- re-mention "after our Bible study group on December 17th" —
  no participation verb; even if keyed, same-day dedup
- assistant echoes — role wall
- painter 'Frederic Edwin Church' / painting 'Astral Temple' —
  no verb, no date
- 'December 2023' — the day regex backtracks off bare years
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_faith_days,
    answer_counting,
    counting_form,
    counting_judge,
)

Q_FD = ('How many days did I spend participating in '
        'faith-related activities in December?')

# near-miss faith cousins — temporal arithmetic, never faith_days
Q_MAUNDY = ('How many days ago did I attend the Maundy Thursday '
            'service at the Episcopal Church?')
Q_ASH = ('How many days had passed between the Sunday mass at '
         "St. Mary's Church and the Ash Wednesday service at the "
         'cathedral?')

# verbatim dataset fixtures (5a7937c8 row; census 09-23/24)
U_FOOD_DRIVE_10 = (
    "I'm looking for some volunteer opportunities in my "
    "community, preferably something related to food banks or "
    "pantries. I actually helped out at the church's annual "
    "holiday food drive on December 10th, sorting donations and "
    "packing boxes for families in need, and it was a really "
    "rewarding experience.")
U_MASS_24 = (
    "I'm planning a family outing for the upcoming holiday "
    "season and I was wondering if you could suggest some "
    "festive activities we could do together. By the way, I "
    "just got back from a lovely midnight mass on Christmas Eve "
    "at St. Mary's Church, which was on December 24th, with my "
    "family.")
U_MASS_FUTURE_T2 = (
    "I'm actually planning a family outing for next year's "
    "holiday season, so I was looking for more general ideas. "
    "We really enjoyed the festive atmosphere at St. Mary's "
    "Church, and I was thinking of doing something similar. Do "
    "you have any suggestions for other holiday-themed events "
    "or activities that we could attend or participate in?")
U_MASS_FUTURE_T4 = (
    "That's a great list. I'm thinking of doing something more "
    "low-key and intimate, like the midnight mass at St. "
    "Mary's Church. Do you have any suggestions for other "
    "religious services or events that might have a similar "
    "atmosphere?")
U_BIBLE_17 = (
    "I'm looking for some guidance on a Bible study I'm leading "
    "next week. We're going to discuss the book of Matthew, and "
    "I was wondering if you could give me some resources on "
    "how to facilitate a good discussion about faith and its "
    "application to daily life. By the way, I actually just did "
    "a Bible study on this same topic at my church a few weeks "
    "ago, on December 17th, and it was really thought-"
    "provoking.")
U_BIBLE_FUTURE_ONLY = (
    "I'm looking for some guidance on a Bible study I'm leading "
    "next week. We're going to discuss the book of Matthew, and "
    "I was wondering if you could give me some resources on "
    "how to facilitate a good discussion about faith and its "
    "application to daily life.")
U_BIBLE_REMENTION_T4 = (
    "That's really helpful. I think establishing ground rules "
    "and creating a safe space will go a long way in making "
    "everyone feel comfortable. I'll definitely keep those tips "
    "in mind. By the way, I've been thinking about how faith "
    "applies to daily life a lot lately, especially after our "
    "Bible study group on December 17th, and I was wondering if "
    "you could recommend some books or resources on the topic.")
U_STORE_12 = (
    "By the way, I just got a new set of kitchen utensils at "
    "the Le Creuset store at the outlet mall last weekend, "
    "December 12th, and I want to make sure I store them "
    "nicely.")
A_ECHO_DRIVE = (
    "It's wonderful that you had a positive experience "
    "volunteering at the church's holiday food drive.")
A_PAINTER_CHURCH = (
    "Frederic Edwin Church (1826-1900): American painter of "
    "grand, detailed landscapes, often with a focus on light "
    "and atmosphere.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: the 3 answer sessions + an off-topic December
# decoy session (store runs) — haystack order preserved
S_REAL = mk(
    ("answer_4cef8a3c_3", [("user", U_FOOD_DRIVE_10),
                           ("assistant", A_ECHO_DRIVE)]),
    ("answer_4cef8a3c_1", [("user", U_MASS_24),
                           ("user", U_MASS_FUTURE_T2),
                           ("user", U_MASS_FUTURE_T4)]),
    ("answer_4cef8a3c_2", [("user", U_BIBLE_17),
                           ("user", U_BIBLE_REMENTION_T4)]),
    ("a76e7e3c_4", [("user", U_STORE_12)]))


class TestForm(unittest.TestCase):
    def test_form_routes_faith_days(self):
        self.assertEqual(counting_form(Q_FD), "faith_days")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never faith_days)
        for q in (
            'How many bikes did I service or plan to service in March?',
            "How many doctor's appointments did I go to in March?",
            'How many trips have I taken my Canon EOS 80D camera on?',
            'How many times have I worn my new black Converse sneakers?',
            'How many different species of birds have I seen in my '
            'local park?',
            'How many different types of food delivery services '
            'have I used recently?',
        ):
            self.assertNotEqual(counting_form(q), "faith_days", q)
            self.assertIsNone(_cnt_faith_days(q, S_REAL), q)

    def test_no_steal_faith_cousins(self):
        # temporal-arithmetic faith questions keep their routing
        for q in (Q_MAUNDY, Q_ASH):
            self.assertNotEqual(counting_form(q), "faith_days", q)
            self.assertIsNone(_cnt_faith_days(q, S_REAL), q)

    def test_no_steal_generic_duration_rows(self):
        # generic how-many-days rows stay with duration_sum
        self.assertEqual(
            counting_form('How many days did I spend volunteering '
                          'at the shelter last month?'),
            "duration_sum")


class TestFaithDays(unittest.TestCase):
    def test_real_row_resolves_three(self):
        self.assertEqual(_cnt_faith_days(Q_FD, S_REAL), "3")

    def test_session_order_independent(self):
        rev = list(reversed(S_REAL))
        self.assertEqual(_cnt_faith_days(Q_FD, rev), "3")

    def test_each_day_alone_is_one(self):
        for turn in (U_FOOD_DRIVE_10, U_MASS_24, U_BIBLE_17):
            sess = one("s1", "user", turn)
            self.assertEqual(_cnt_faith_days(Q_FD, sess), "1", turn)

    def test_pairs_are_two(self):
        pair = mk(("s1", [("user", U_FOOD_DRIVE_10)]),
                  ("s2", [("user", U_BIBLE_17)]))
        self.assertEqual(_cnt_faith_days(Q_FD, pair), "2")

    def test_st_abbreviation_merge_load_bearing(self):
        # the Dec 24 sentence splits at 'St.'; honorific repair
        # re-joins it — without the merge the day is lost
        frag = ("By the way, I just got back from a lovely "
                "midnight mass on Christmas Eve at St. Mary's "
                "Church, which was on December 24th, with my "
                "family.")
        self.assertEqual(_cnt_faith_days(Q_FD,
                                         one("s1", "user", frag)),
                         "1")

    def test_store_dec12_never_keys(self):
        # December day but no faith term (topic wall)
        self.assertIsNone(
            _cnt_faith_days(Q_FD, one("s1", "user", U_STORE_12)))
        # and it does not inflate a real day
        sess = mk(("s1", [("user", U_FOOD_DRIVE_10)]),
                  ("s2", [("user", U_STORE_12)]))
        self.assertEqual(_cnt_faith_days(Q_FD, sess), "1")

    def test_future_intent_never_keys(self):
        # faith term, no December day (date wall)
        self.assertIsNone(_cnt_faith_days(
            Q_FD, one("s1", "user", U_BIBLE_FUTURE_ONLY)))
        self.assertIsNone(_cnt_faith_days(
            Q_FD, one("s1", "user", U_MASS_FUTURE_T4)))
        # and the future turns don't inflate the real row
        self.assertEqual(_cnt_faith_days(Q_FD, S_REAL), "3")

    def test_remention_dedups_same_day(self):
        sess = mk(("s1", [("user", U_BIBLE_17)]),
                  ("s2", [("user", U_BIBLE_REMENTION_T4)]))
        self.assertEqual(_cnt_faith_days(Q_FD, sess), "1")

    def test_assistant_never_keys(self):
        for a in (A_ECHO_DRIVE, A_PAINTER_CHURCH):
            sess = one("s1", "assistant", a)
            self.assertIsNone(_cnt_faith_days(Q_FD, sess), a)

    def test_no_faith_activity_never_keys(self):
        sess = one("s1", "user",
                   "I went to the gym on December 5th and again "
                   "on December 9th.")
        self.assertIsNone(_cnt_faith_days(Q_FD, sess))

    def test_bare_year_never_keys(self):
        sess = one("s1", "user",
                   "I did a Bible study at my church back in "
                   "December 2023 with the old group.")
        self.assertIsNone(_cnt_faith_days(Q_FD, sess))

    def test_non_december_never_keys(self):
        sess = one("s1", "user",
                   "I did a Bible study at my church on January "
                   "17th this year.")
        self.assertIsNone(_cnt_faith_days(Q_FD, sess))

    def test_empty_sessions_none(self):
        self.assertIsNone(_cnt_faith_days(Q_FD, []))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_sentence_gt(self):
        # GT renders '3 days.' — numeric-first banks pred '3'
        self.assertTrue(counting_judge(Q_FD, "3 days.", "3"))
        self.assertFalse(counting_judge(Q_FD, "3 days.", "2"))
        self.assertFalse(counting_judge(Q_FD, "3 days.", ""))

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q_FD, S_REAL)
        self.assertEqual(ans, "3")
        self.assertEqual(meta, {"form": "faith_days"})

    def test_answer_counting_unresolvable_falls_through(self):
        ans, meta = answer_counting(
            Q_FD, one("s1", "user", U_STORE_12))
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "faith_days"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
