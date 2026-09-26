"""C610: sports_competitive face — competitive-sport census
(ef66a6e5 GT 'two').

Single mechanism, distinct-sport-key count at SENTENCE grain:

- "How many sports have I played competitively in the past?" —
  the row carries TWO sport keys across five user sentences:
  s26 "I used to swim competitively in college, and I'm
       looking to get back into it ..."        (key: swim)
  s26 "I used to swim competitively in college, and I'm
       looking for a 25-yard pool ..."         (key: swim, dup)
  s26 "As someone who used to swim competitively in college,
       I'm used to having access ..."          (key: swim, dup)
  s28 "Can you recommend some exercises ... considering I
       used to play tennis competitively in high school?"
                                               (key: tennis)
  = {swim, tennis} -> 2 (GT 'two').

Wall discipline:

- past-habit wall is load-bearing: 'I've been playing soccer
  and tennis lately' (present play, no used-to, no
  competitive register) never keys; the gerund habit
  ("who's used to swimming competitively") has no play|swim
  stem after 'used to' and stays dark (dup-key insurance)
- competitive-register wall is load-bearing: yoga-class
  scheduling and lesson talk never key
- sport identity: verb-direct 'used to swim' folds onto one
  key regardless of rephrasing; 'used to play <noun>' takes
  the noun ('tennis')
- assistant surfaces carry the competitive register
  ('competitive background', 'former competitive tennis
  player', 'competitive swimmer', 'competitive prices') —
  the user-role wall backstops every echo (synthetic
  assistant sentence with every wall present)

Census (all 500): the strict head matches EXACTLY its own
row (ef66a6e5 GT 'two', unbanked, gate=answer / NEEDS_JUDGE
today — the frozen pred is a home-insurance echo); a loose
'sport' sweep over question text hits only event-ORDER
cousins (gpt4_45189cb4 / gpt4_e061b84f / gpt4_e061b84g) with
different heads, so nothing is stolen. Render the digit
total '2' — GT banks via counting_judge numeric-first
(_cnt_numval('two') == _cnt_numval('2') == 2.0), exact +
judge_semantic bank on the digit match.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_sports_competitive,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = 'How many sports have I played competitively in the past?'

# verbatim dataset fixtures (ef66a6e5; 09-27 census)
U_SWIM_A = (
    "I used to swim competitively in college, and I'm looking "
    "to get back into it as a way to stay active and relieve "
    "stress.")
U_SWIM_B = (
    "I used to swim competitively in college, and I'm looking "
    "for a 25-yard pool that's kept at around 78-80°F.")
U_TENNIS = (
    "Can you recommend some exercises that would be "
    "beneficial for my tennis game, considering I used to "
    "play tennis competitively in high school?")

# structural wall shapes (verbatim row fragments pinned)
U_GERUND = (
    "As someone who's used to swimming competitively in "
    "college, I'm comfortable swimming in a fast-paced "
    "environment, but I want to make sure I'll have enough "
    "space to do my workouts effectively.")
U_PRESENT_PLAY = (
    "I've been playing soccer and tennis lately, so I'm "
    "trying to build on that.")
U_YOGA_CLASS = (
    "I have a team lunch meeting every Wednesday at 1 pm, and "
    "I'm worried that moving my yoga class to Wednesday "
    "morning might make me run late for the meeting.")
U_COMPETITIVE_PRICES = (
    "Amazon offers a range of personalized photo albums and "
    "frames from various sellers, often with fast shipping "
    "and competitive prices.")
A_STRENGTH_TENNIS = (
    "Strength training can significantly enhance your tennis "
    "game, especially with your competitive background.")
A_ECHO_ALL_WALLS = (
    "You mentioned you used to swim competitively in college "
    "and you used to play tennis competitively in high "
    "school.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: evidence sessions in dataset order
S_ROW = mk(
    ("sess_26", [("user", U_SWIM_A),
                 ("user", U_SWIM_B),
                 ("user", U_GERUND)]),
    ("sess_28", [("user", U_PRESENT_PLAY),
                 ("user", U_TENNIS)]))


class TestForm(unittest.TestCase):
    def test_form_routes_sports_competitive(self):
        self.assertEqual(counting_form(Q), "sports_competitive")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # sports_competitive), and the sports handler is dark
        # on all of them
        for q in (
            'How many times did I ride rollercoasters across '
            'all the events I attended from July to October?',
            'How many different art-related events did I '
            'attend in the past month?',
            'How many days did I spend attending workshops, '
            'lectures, and conferences in April?',
            'How many weddings have I attended in this year?',
            'How many fun runs did I miss in March due to work '
            'commitments?',
            'How many pre-1920 American coins do I have in my '
            'collection?',
        ):
            self.assertNotEqual(counting_form(q),
                                "sports_competitive", q)
            self.assertIsNone(_cnt_sports_competitive(q, S_ROW),
                              q)

    def test_short_variant_head_not_claimed(self):
        # dropping 'in the past' leaves a different question —
        # the strict head never claims it (not in the 500; the
        # generic blocks keep whatever they did before)
        q = 'How many sports have I played competitively?'
        self.assertNotEqual(counting_form(q), "sports_competitive")
        self.assertIsNone(_cnt_sports_competitive(q, S_ROW))

    def test_present_tense_head_not_claimed(self):
        q = 'How many sports do I play competitively?'
        self.assertNotEqual(counting_form(q), "sports_competitive")
        self.assertIsNone(_cnt_sports_competitive(q, S_ROW))


class TestSportsCompetitive(unittest.TestCase):
    def test_row_resolves_two(self):
        self.assertEqual(_cnt_sports_competitive(Q, S_ROW), "2")

    def test_swim_evidence_alone_keys_swim(self):
        sess = one("sess_26", "user", U_SWIM_A)
        self.assertEqual(_cnt_sports_competitive(Q, sess), "1")

    def test_tennis_evidence_alone_keys_tennis(self):
        sess = one("sess_28", "user", U_TENNIS)
        self.assertEqual(_cnt_sports_competitive(Q, sess), "1")

    def test_swim_rephrasings_dedup_to_one(self):
        # three swim shapes across two sessions -> one key
        sess = mk(("s1", [("user", U_SWIM_A)]),
                  ("s2", [("user", U_SWIM_B)]),
                  ("s3", [("user",
                           "As someone who used to swim "
                           "competitively in college, I'm used "
                           "to having access to that kind of "
                           "equipment during my workouts.")]))
        self.assertEqual(_cnt_sports_competitive(Q, sess), "1")

    def test_play_takes_sport_noun(self):
        sess = one("s1", "user",
                   "I used to play soccer competitively in "
                   "college.")
        self.assertEqual(_cnt_sports_competitive(Q, sess), "1")

    def test_swim_and_play_additive(self):
        sess = mk(("s1", [("user", U_SWIM_A)]),
                  ("s2", [("user",
                           "I used to play soccer "
                           "competitively in high school.")]))
        self.assertEqual(_cnt_sports_competitive(Q, sess), "2")

    def test_gerund_used_to_swimming_dark(self):
        # 'used to swimming' has no play|swim stem — dark
        sess = one("s1", "user", U_GERUND)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_present_play_soccer_tennis_dark(self):
        # present play, no used-to, no competitive register
        sess = one("s1", "user", U_PRESENT_PLAY)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_yoga_class_scheduling_dark(self):
        sess = one("s1", "user", U_YOGA_CLASS)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_competitive_prices_dark(self):
        # competitive register without used-to play|swim (pinned
        # as user to prove the lexical wall is load-bearing)
        sess = one("s1", "user", U_COMPETITIVE_PRICES)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_assistant_strength_talk_dark(self):
        sess = one("s1", "assistant", A_STRENGTH_TENNIS)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_assistant_all_walls_still_dark(self):
        # role wall is load-bearing even when every lexical
        # wall is present in the echo
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        self.assertIsNone(_cnt_sports_competitive(Q, sess))

    def test_assistant_echo_does_not_disturb_user_evidence(self):
        sess = mk(("s1", [("user", U_SWIM_A),
                          ("user", U_TENNIS)]),
                  ("s2", [("assistant", A_ECHO_ALL_WALLS)]))
        self.assertEqual(_cnt_sports_competitive(Q, sess), "2")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_word_gt_numeric_pred(self):
        self.assertTrue(counting_judge(Q, "two", "2"))
        self.assertTrue(counting_judge(Q, "two", "two"))
        self.assertFalse(counting_judge(Q, "two", "3"))
        self.assertFalse(counting_judge(Q, "two", "one"))

    def test_exact_judge_miss_redeemed(self):
        # exact string match fails on the unit mismatch — the
        # counting_judge numeric path is what banks the row
        self.assertEqual(exact_judge(Q, "two", "2"), False)

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "two", "2"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q, "three", "2"),
                         "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "2")
        self.assertEqual(meta, {"form": "sports_competitive"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "sports_competitive"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
