"""C609: coaster_rides face — Jul-Oct rollercoaster-ride
census (gpt4_e05b82a6 GT '10 times').

Single mechanism, three count shapes at SENTENCE grain:

- "How many times did I ride rollercoasters across all the
  events I attended from July to October?" — the row carries
  FOUR user evidence sentences, all in-window:
  s04 "rode the Revenge of the Mummy rollercoaster three
       times in a row ... on October 15th"          (multiplier = 3)
  s20 "rode the Xcelerator rollercoaster ... on
       October 8th"                                  (bare rode = 1)
  s37 "rode Space Mountain: Ghost Galaxy three times at
       Disneyland on September 24th"        (multiplier = 3, NO coaster noun)
  s42 "rode the Mako, Kraken, and Manta rollercoasters all
       in one night ... in July"        (enumeration = 3, NO 'times')
  = 3 + 1 + 3 + 3 = 10 (GT '10 times').

Wall discipline:

- rode wall is load-bearing: 'how many times I shopped
  online last month' has 'times' but no rode verb;
  'have you ever been on a rollercoaster ...?' is a question
  with no rode; 'planning a trip to Knott's Berry Farm soon'
  is future with no rode
- month wall is load-bearing (the question pins the window):
  every evidence sentence carries July..October; month-less
  ride talk never keys; 'rode my bike in July' shapes stay
  dark via the context wall (no coaster noun, no 'times')
- precedence: explicit 'N times' multiplier outranks the
  name-enumeration span ('Mummy rollercoaster three times'
  counts 3, never re-parses the name); enumeration counts
  distinct names between 'rode the' and the coaster head
  noun (Mako, Kraken, and Manta -> 3)
- assistant surfaces echo coasters (Giant Dipper
  recommendation, Gadget's Go Coaster, 'Coasters Diner',
  'riding three rollercoasters in one night') — the
  user-role wall backstops every echo (synthetic assistant
  sentence with every wall present)

Census (all 500): the strict head matches EXACTLY its own
row (gpt4_e05b82a6 GT '10 times', unbanked, gate=answer /
WRONG today — the frozen pred carried no ride tally); a
loose 'rollercoaster' sweep over question text hits no other
row, so nothing is stolen. Render the digit total '10' — GT
banks via counting_judge numeric-first (_cnt_numval('10') ==
_cnt_numval('10 times') == 10.0), exact + judge_semantic
bank on the digit match.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_coaster_rides,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = ('How many times did I ride rollercoasters across all '
     'the events I attended from July to October?')

# verbatim dataset fixtures (gpt4_e05b82a6; 09-26 census)
U_MUMMY = (
    "I rode the Revenge of the Mummy rollercoaster three "
    "times in a row at Universal Studios Hollywood on "
    "October 15th, and it was such a thrill!")
U_XCELERATOR = (
    "By the way, I rode the Xcelerator rollercoaster at "
    "Knott's Berry Farm on October 8th and it's still one of "
    "my favorite thrill rides.")
U_SPACE_MTN = (
    "By the way, I rode Space Mountain: Ghost Galaxy three "
    "times at Disneyland on September 24th during Mickey's "
    "Halloween Party, and it was a blast!")
U_SEAWORLD = (
    "By the way, I'm a huge rollercoaster fan and I have a "
    "fun fact: I rode the Mako, Kraken, and Manta "
    "rollercoasters all in one night at SeaWorld San Diego "
    "in July.")

# structural wall shapes (verbatim row fragments pinned)
U_SHOPPING_TIMES = (
    "By the way, do you think you can help me keep track of "
    "my online shopping history, like how many times I "
    "shopped online last month?")
U_BEEN_ON_QUESTION = (
    "Can I ask, have you ever been on a rollercoaster "
    "that's themed around an ancient Egyptian tomb?")
U_PLANNING_TRIP = (
    "I'm planning a trip to Knott's Berry Farm soon and I "
    "was wondering if you could give me some tips on which "
    "rides to prioritize during their Knott's Spooky Farm "
    "event.")
U_RODE_BIKE_MONTH = (
    "I rode my bike along the coast trail in July and loved "
    "every minute of it.")
A_ECHO_ALL_WALLS = (
    "You mentioned you rode the Revenge of the Mummy "
    "rollercoaster three times in a row on October 15th, "
    "rode the Xcelerator rollercoaster on October 8th, rode "
    "Space Mountain: Ghost Galaxy three times on September "
    "24th, and rode the Mako, Kraken, and Manta "
    "rollercoasters in one night in July.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: evidence sessions in dataset order
S_ROW = mk(
    ("sess_04", [("user", U_BEEN_ON_QUESTION),
                 ("user", U_MUMMY)]),
    ("sess_20", [("user", U_PLANNING_TRIP),
                 ("user", U_XCELERATOR)]),
    ("sess_37", [("user", U_SPACE_MTN)]),
    ("sess_42", [("user", U_SEAWORLD)]))


class TestForm(unittest.TestCase):
    def test_form_routes_coaster_rides(self):
        self.assertEqual(counting_form(Q), "coaster_rides")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # coaster_rides), and the coaster handler is dark on
        # all of them
        for q in (
            'How many different art-related events did I '
            'attend in the past month?',
            'How many days did I spend attending workshops, '
            'lectures, and conferences in April?',
            'How many weddings have I attended in this year?',
            'How many fun runs did I miss in March due to work '
            'commitments?',
            'How many pre-1920 American coins do I have in my '
            'collection?',
            'How many different species of birds have I seen '
            'in my local park?',
        ):
            self.assertNotEqual(counting_form(q), "coaster_rides",
                                q)
            self.assertIsNone(_cnt_coaster_rides(q, S_ROW), q)


class TestCoasterRides(unittest.TestCase):
    def test_row_resolves_ten(self):
        self.assertEqual(_cnt_coaster_rides(Q, S_ROW), "10")

    def test_mummy_multiplier_three(self):
        sess = one("sess_04", "user", U_MUMMY)
        self.assertEqual(_cnt_coaster_rides(Q, sess), "3")

    def test_xcelerator_bare_rode_one(self):
        sess = one("sess_20", "user", U_XCELERATOR)
        self.assertEqual(_cnt_coaster_rides(Q, sess), "1")

    def test_space_mountain_multiplier_no_coaster_noun(self):
        # the s37 evidence carries NO coaster noun — the
        # 'times' context wall + multiplier key it
        sess = one("sess_37", "user", U_SPACE_MTN)
        self.assertEqual(_cnt_coaster_rides(Q, sess), "3")

    def test_seaworld_enumeration_no_times(self):
        # the s42 evidence carries NO 'times' — the coaster
        # context wall + name enumeration key it
        sess = one("sess_42", "user", U_SEAWORLD)
        self.assertEqual(_cnt_coaster_rides(Q, sess), "3")

    def test_cross_session_additive(self):
        sess = mk(("s1", [("user", U_MUMMY)]),
                  ("s2", [("user", U_XCELERATOR)]))
        self.assertEqual(_cnt_coaster_rides(Q, sess), "4")

    def test_digit_multiplier(self):
        sess = one("s1", "user",
                   "I rode the Goliath rollercoaster 2 times "
                   "at Six Flags in August.")
        self.assertEqual(_cnt_coaster_rides(Q, sess), "2")

    def test_enumeration_two_names(self):
        sess = one("s1", "user",
                   "I rode the Twisted Colossus and Tatsu "
                   "rollercoasters at Magic Mountain in "
                   "August.")
        self.assertEqual(_cnt_coaster_rides(Q, sess), "2")

    def test_multiplier_outranks_enumeration(self):
        # explicit 'times' multiplier wins over the name span
        sess = one("s1", "user",
                   "I rode the Mummy rollercoaster three "
                   "times in a row at Universal in October.")
        self.assertEqual(_cnt_coaster_rides(Q, sess), "3")

    def test_shopping_times_dark(self):
        # 'times' without the rode verb
        sess = one("s1", "user", U_SHOPPING_TIMES)
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_been_on_question_dark(self):
        # rollercoaster noun without the rode verb
        sess = one("s1", "user", U_BEEN_ON_QUESTION)
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_planning_trip_dark(self):
        # future plan, no rode
        sess = one("s1", "user", U_PLANNING_TRIP)
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_rode_bike_no_context_dark(self):
        # rode + in-window month but no coaster noun / times
        sess = one("s1", "user", U_RODE_BIKE_MONTH)
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_out_of_window_month_dark(self):
        # rode + coaster but the anchor is outside Jul-Oct
        sess = one("s1", "user",
                   "I rode the Blue Fire rollercoaster at "
                   "Europa-Park in March.")
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_assistant_echoes_never_read(self):
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        self.assertIsNone(_cnt_coaster_rides(Q, sess))

    def test_assistant_all_walls_still_dark(self):
        # role wall is load-bearing even when every lexical
        # wall is present in the echo
        sess = mk(("s1", [("user", U_MUMMY),
                          ("user", U_XCELERATOR)]),
                  ("s2", [("assistant", A_ECHO_ALL_WALLS)]))
        self.assertEqual(_cnt_coaster_rides(Q, sess), "4")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric_unit_gt(self):
        self.assertTrue(counting_judge(Q, "10 times", "10"))
        self.assertTrue(counting_judge(Q, "10 times", "10 times"))
        self.assertFalse(counting_judge(Q, "10 times", "8"))
        self.assertFalse(counting_judge(Q, "10 times", "3"))

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "10 times", "10"),
                         "CORRECT")
        self.assertEqual(exact_judge(Q, "10 times", "10 times"),
                         True)
        self.assertEqual(judge_semantic(Q, "8", "10 times"),
                         "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "10")
        self.assertEqual(meta, {"form": "coaster_rides"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "coaster_rides"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
