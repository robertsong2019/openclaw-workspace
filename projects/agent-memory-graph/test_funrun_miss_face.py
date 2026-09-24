"""C604: funrun_miss face — March fun-run days missed for work
(21d02d0d GT 2).

Single mechanism, single face:

- "How many fun runs did I miss in March due to work
  commitments?" — the row carries TWO user evidence sentences,
  each self-contained at SENTENCE grain (all four walls in one
  sentence): s3 "I've been pretty busy with work lately and
  missed a few events, including a 5K fun run on March 26th" +
  s30 "...attend most of the weekly 5K fun runs at the local
  park, except for the run on March 5th when I had to miss due
  to work commitments" = days {26, 5} -> 2.

Wall discipline:

- work-attribution wall is load-bearing on BOTH sides: the s3
  assistant echo ("don't worry about missing the 5K fun run on
  March 26th") carries funrun+march but neither miss-verb nor
  work; the s30 assistant echo ("have been attending the
  weekly 5K fun runs") carries neither — and assistant echoes
  never read anyway (user wall, C592+ discipline)
- 'missing' gerund is NOT a miss verb (\bmiss(ed)?\b — the
  boundary dies between 's' and 'i'); only 'miss'/'missed'
  keys
- bare 'run' never keys (must be 'fun run(s)'); 'movie
  marathon' / April-10 marathon recovery carry no fun-run term
- non-March days never key (April decoys); 'March' without a
  day never keys; distinct days are additive, same-day
  re-mentions dedup

Census (all 500): the strict head matches EXACTLY its own row
(21d02d0d GT 2, unbanked, gate=answer / marathon-recovery echo
today); no sibling question mentions fun runs. Render the day
count '2' — GT '2' banks exact + judge_semantic + counting_judge.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_funrun_miss,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = ('How many fun runs did I miss in March due to work '
     'commitments?')

# verbatim dataset fixtures (21d02d0d; 09-25 dump)
U_MISS_26 = (
    "By the way, I've been pretty busy with work lately and "
    "missed a few events, including a 5K fun run on March "
    "26th.")
U_MISS_5 = (
    "By the way, I've been active in the running community and "
    "was able to attend most of the weekly 5K fun runs at the "
    "local park, except for the run on March 5th when I had to "
    "miss due to work commitments.")
A_ECHO_26 = (
    "By the way, don't worry about missing the 5K fun run on "
    "March 26th.")
A_ECHO_ATTEND = (
    "It's great to hear that you've been active in the running "
    "community and have been attending the weekly 5K fun runs.")
U_MARATHON_APRIL = (
    "I just completed my first full marathon on April 10th and "
    "I'm feeling a bit sore.")

# structural wall shapes (dataset realities pinned)
U_SKIP_NO_MISS = (
    "I might skip the 5K fun run on March 12th if work gets "
    "busy.")
U_MISS_NO_WORK = (
    "I missed the fun run on March 19th because of a family "
    "trip.")
U_MISS_APRIL = (
    "I had to miss the fun run on April 2nd due to work "
    "commitments.")
U_MORNING_RUN = (
    "I had to miss my morning run on March 9th due to work.")
U_MISSING_GERUND = (
    "Don't worry about me missing the 5K fun run on March 26th "
    "due to work travel.")
U_MARCH_NO_DAY = (
    "I missed some fun runs in March due to work commitments.")
U_MISS_12 = (
    "I missed the 5K fun run on March 12th due to work.")
A_ALL_WALLS = (
    "Sorry to hear you missed the 5K fun run on March 26th due "
    "to work commitments.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: two same-day answer sessions (dataset order)
S_ROW = mk(
    ("sess_03", [("user", U_MISS_26),
                 ("assistant", A_ECHO_26)]),
    ("sess_30", [("user", U_MARATHON_APRIL),
                 ("user", U_MISS_5),
                 ("assistant", A_ECHO_ATTEND)]))


class TestForm(unittest.TestCase):
    def test_form_routes_funrun_miss(self):
        self.assertEqual(counting_form(Q), "funrun_miss")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # funrun_miss), and the funrun handler is dark on all
        # of them — including the C599 March siblings (bike
        # service / doctor appts: different NPs, zero overlap)
        for q in (
            'How many bikes did I service or plan to service '
            'in March?',
            "How many doctor's appointments did I go to in "
            'March?',
            'How many trips have I taken my Canon EOS 80D '
            'camera on?',
            'How many times did I bake something in the past '
            'two weeks?',
            'How many Marvel movies did I re-watch?',
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many different types of food delivery '
            'services have I used recently?',
            'How many different species of birds have I seen '
            'in my local park?',
            'How many followers do I have on Instagram now?',
            'How many short stories have I written since I '
            'started writing regularly?',
        ):
            self.assertNotEqual(counting_form(q), "funrun_miss",
                                q)
            self.assertIsNone(_cnt_funrun_miss(q, S_ROW), q)


class TestFunrunMiss(unittest.TestCase):
    def test_pair_resolves_two(self):
        self.assertEqual(_cnt_funrun_miss(Q, S_ROW), "2")

    def test_single_either(self):
        sess = one("sess_03", "user", U_MISS_26)
        self.assertEqual(_cnt_funrun_miss(Q, sess), "1")
        sess = one("sess_30", "user", U_MISS_5)
        self.assertEqual(_cnt_funrun_miss(Q, sess), "1")

    def test_assistant_echoes_never_read(self):
        sess = mk(("s1", [("assistant", A_ECHO_26)]),
                  ("s2", [("assistant", A_ECHO_ATTEND)]))
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_assistant_all_walls_still_dark(self):
        # role wall is load-bearing even when every lexical
        # wall is present in the echo
        sess = mk(("s1", [("user", U_MISS_26)]),
                  ("s2", [("assistant", A_ALL_WALLS)]))
        self.assertEqual(_cnt_funrun_miss(Q, sess), "1")

    def test_marathon_sentence_no_key(self):
        # April-10 marathon recovery: no fun-run term
        sess = one("s1", "user", U_MARATHON_APRIL)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_skip_is_not_miss(self):
        sess = one("s1", "user", U_SKIP_NO_MISS)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_miss_without_work_never_keys(self):
        sess = one("s1", "user", U_MISS_NO_WORK)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_non_march_day_never_keys(self):
        sess = one("s1", "user", U_MISS_APRIL)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_bare_run_never_keys(self):
        # 'morning run' is not a fun run
        sess = one("s1", "user", U_MORNING_RUN)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_missing_gerund_not_a_miss_verb(self):
        sess = one("s1", "user", U_MISSING_GERUND)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_march_without_day_never_keys(self):
        sess = one("s1", "user", U_MARCH_NO_DAY)
        self.assertIsNone(_cnt_funrun_miss(Q, sess))

    def test_same_day_remention_dedup(self):
        sess = mk(("s1", [("user", U_MISS_26)]),
                  ("s2", [("user", U_MISS_26)]))
        self.assertEqual(_cnt_funrun_miss(Q, sess), "1")

    def test_three_days_additive(self):
        sess = mk(("s1", [("user", U_MISS_26)]),
                  ("s2", [("user", U_MISS_5)]),
                  ("s3", [("user", U_MISS_12)]))
        self.assertEqual(_cnt_funrun_miss(Q, sess), "3")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric(self):
        self.assertTrue(counting_judge(Q, "2", "2"))
        self.assertFalse(counting_judge(Q, "2", "3"))

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "2", "2"), "CORRECT")
        self.assertEqual(exact_judge(Q, "2", "2"), True)
        self.assertEqual(judge_semantic(Q, "1", "2"), "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "2")
        self.assertEqual(meta, {"form": "funrun_miss"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("assistant", A_ECHO_26)]),)
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "funrun_miss"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
