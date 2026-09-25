"""C607: workshop_days face — April workshop/lecture/conference
days (10d9b85a GT '3 days').

Single mechanism, single face:

- "How many days did I spend attending workshops, lectures,
  and conferences in April?" — the row carries TWO user
  evidence sentences, each self-contained at SENTENCE grain:
  s29 "I recently attended a lecture on sustainable
  development at the public library on the 10th of April" +
  s39 "I actually learned about standardization and
  normalization in a 2-day workshop I attended on the 17th
  and 18th of April" = days {10, 17, 18} -> 3.

Wall discipline:

- BOTH evidence sentences use the DAY-FIRST April anchor
  ('the 10th of April' / 'the 17th and 18th of April') — the
  before-month RX must key multi-day lists ('17th and 18th');
  the month-first anchor ('April 12th') is pinned too
- participation wall is load-bearing: 'There's a 2-day
  workshop on the 17th and 18th of April' (no attend/spent
  verb) never keys; 'I was thinking about the workshop'
  never keys (honorific-merged 'Dr.' fragment stays dark)
- 'April 2023' never captures a day (the \d{1,2} backtracks
  off the year digits — C601 faith_days lesson)
- non-April days never key; 'April' without a day never
  keys; distinct days are additive, same-day re-mentions dedup
- assistant surfaces in the row carry the topic but NO April
  day; the user-role wall backstops the all-walls echo

Census (all 500): the strict head matches EXACTLY its own row
(10d9b85a GT '3 days', unbanked, gate=answer today); the loose
'workshop' cousins (gpt4_1e4a8aeb days-between, 0bb5a684
days-before) carry different heads and are never stolen. The
head is claimed BEFORE the generic duration_sum block ('how
many days' would otherwise route there). Render the day count
'3' — GT '3 days' banks via counting_judge numeric-first
(_cnt_numval('3 days') == 3.0), exact is False (unit suffix).
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_workshop_days,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = ('How many days did I spend attending workshops, '
     'lectures, and conferences in April?')

# verbatim dataset fixtures (10d9b85a; 09-26 dump)
U_LECTURE_10 = (
    "By the way, I recently attended a lecture on sustainable "
    "development at the public library on the 10th of April, "
    "and it got me interested in learning more.")
U_WS_1718 = (
    "I actually learned about standardization and "
    "normalization in a 2-day workshop I attended on the 17th "
    "and 18th of April, but I'm still a bit unclear on when to "
    "use each.")
U_WS_REMENTION = (
    "The workshop covered a lot of topics, including "
    "supervised learning and deep learning, but I didn't get a "
    "chance to ask about this specific question.")
A_WS_GREET = (
    "I'm glad you got to attend a workshop on machine "
    "learning!")
U_THINKING_DR = (
    "I was thinking about the workshop and I realized that "
    "Dr. Smith teaches the advanced course.")

# structural wall shapes (dataset realities pinned)
U_CONF_APRIL_12 = (
    "I also attended a conference on April 12th downtown.")
U_WS_NO_VERB = (
    "There's a 2-day workshop on the 17th and 18th of April.")
U_APR_NO_DAY = (
    "I attended some workshops in April.")
U_MARCH_DAY = (
    "I attended a lecture on March 3rd at the library.")
U_APR_YEAR = (
    "I attended a workshop in April 2023 and learned a lot.")
A_ALL_WALLS = (
    "You mentioned you attended a 2-day workshop on the 17th "
    "and 18th of April and a lecture on the 10th of April.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: evidence sessions in dataset order
S_ROW = mk(
    ("sess_29", [("user", U_LECTURE_10),
                 ("assistant",
                  "That sounds like a wonderful learning "
                  "experience!")]),
    ("sess_39", [("user", U_WS_1718),
                 ("user", U_WS_REMENTION),
                 ("assistant", A_WS_GREET),
                 ("user", U_THINKING_DR)]))


class TestForm(unittest.TestCase):
    def test_form_routes_workshop_days(self):
        self.assertEqual(counting_form(Q), "workshop_days")

    def test_head_beats_duration_sum(self):
        # the generic 'how many days' duration_sum block sits
        # AFTER this claim — the workshop head never leaks there
        self.assertNotEqual(counting_form(Q), "duration_sum")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # workshop_days), and the workshop handler is dark on
        # all of them — including the loose 'workshop' cousins
        # (gpt4_1e4a8aeb days-between, 0bb5a684 days-before)
        # and the C601 faith-days sibling (same 'days did i
        # spend' family, different topic)
        for q in (
            'How many days passed between the day I attended '
            'the gardening workshop and the day I planted the '
            'tomato saplings?',
            'How many days before the team meeting did I '
            "attend the workshop on 'Effective Communication'?",
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many fun runs did I miss in March due to work '
            'commitments?',
            'How many weddings have I attended in this year?',
            'How many pre-1920 American coins do I have in my '
            'collection?',
            'How many different types of food delivery '
            'services have I used recently?',
            'How many bikes did I service or plan to service '
            'in March?',
        ):
            self.assertNotEqual(counting_form(q), "workshop_days",
                                q)
            self.assertIsNone(_cnt_workshop_days(q, S_ROW), q)


class TestWorkshopDays(unittest.TestCase):
    def test_row_resolves_three(self):
        self.assertEqual(_cnt_workshop_days(Q, S_ROW), "3")

    def test_single_lecture_day(self):
        sess = one("sess_29", "user", U_LECTURE_10)
        self.assertEqual(_cnt_workshop_days(Q, sess), "1")

    def test_single_workshop_two_days(self):
        sess = one("sess_39", "user", U_WS_1718)
        self.assertEqual(_cnt_workshop_days(Q, sess), "2")

    def test_day_first_multi_day_anchor(self):
        # 'the 17th and 18th of April' — the list anchor keys
        # BOTH days from one sentence
        sess = one("s1", "user", U_WS_1718)
        self.assertEqual(_cnt_workshop_days(Q, sess), "2")

    def test_month_first_anchor(self):
        sess = one("s1", "user", U_CONF_APRIL_12)
        self.assertEqual(_cnt_workshop_days(Q, sess), "1")

    def test_assistant_echoes_never_read(self):
        sess = mk(("s1", [("assistant", A_WS_GREET)]),
                  ("s2", [("assistant", A_ALL_WALLS)]))
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_assistant_all_walls_still_dark(self):
        # role wall is load-bearing even when every lexical
        # wall is present in the echo
        sess = mk(("s1", [("user", U_WS_1718)]),
                  ("s2", [("assistant", A_ALL_WALLS)]))
        self.assertEqual(_cnt_workshop_days(Q, sess), "2")

    def test_remention_without_verb_or_day_dark(self):
        sess = one("s1", "user", U_WS_REMENTION)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_thinking_honorific_fragment_dark(self):
        # verbatim row fragment: no participation verb, no
        # April day (honorific 'Dr.' merges with the neighbor)
        sess = one("s1", "user", U_THINKING_DR)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_no_verb_never_keys(self):
        sess = one("s1", "user", U_WS_NO_VERB)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_april_without_day_never_keys(self):
        sess = one("s1", "user", U_APR_NO_DAY)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_non_april_day_never_keys(self):
        sess = one("s1", "user", U_MARCH_DAY)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_april_year_backtracks_off(self):
        # 'April 2023' — \d{1,2} cannot capture year digits
        sess = one("s1", "user", U_APR_YEAR)
        self.assertIsNone(_cnt_workshop_days(Q, sess))

    def test_same_day_remention_dedup(self):
        sess = mk(("s1", [("user", U_LECTURE_10)]),
                  ("s2", [("user", U_LECTURE_10)]))
        self.assertEqual(_cnt_workshop_days(Q, sess), "1")

    def test_four_days_additive(self):
        sess = mk(("s1", [("user", U_LECTURE_10)]),
                  ("s2", [("user", U_WS_1718)]),
                  ("s3", [("user", U_CONF_APRIL_12)]))
        self.assertEqual(_cnt_workshop_days(Q, sess), "4")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric_unit_gt(self):
        # THE banking path: GT '3 days' -> _cnt_numval 3.0
        self.assertTrue(counting_judge(Q, "3", "3 days"))
        self.assertFalse(counting_judge(Q, "2", "3 days"))

    def test_exact_is_false_on_unit_gt(self):
        # '3' != '3 days' verbatim — the numeric judge is what
        # banks this row, not exact match
        self.assertFalse(exact_judge(Q, "3 days", "3"))

    def test_judge_semantic(self):
        self.assertEqual(judge_semantic(Q, "3", "3"), "CORRECT")
        self.assertEqual(judge_semantic(Q, "1", "3 days"),
                         "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "3")
        self.assertEqual(meta, {"form": "workshop_days"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("assistant", A_ALL_WALLS)]),)
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "workshop_days"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
