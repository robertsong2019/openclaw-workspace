"""C611: fitness_week face — weekly fitness-class census
(2788b940 GT 5, int).

Single mechanism, per-class day-of-week SET count at SENTENCE
grain:

- "How many fitness classes do I attend in a typical week?" —
  the row carries FOUR class keys across ten user sentences:

  s1:0  "I usually take Zumba classes on Tuesdays and
         Thursdays at 7:00 PM ..."            (zumba: Tue,Thu)
  s1:2  "I've recently started taking a BodyPump class on
         Mondays ..."                         (bodypump: Mon)
  s1:4  "For my Zumba classes on Tuesdays and Thursdays ..."
                                              (dup, dedup-safe)
  s39:0 "I'm not free on Sundays since I have my yoga class
         at 6:00 PM ..."                      (yoga: Sun)
  s41:0 "my weightlifting classes, like BodyPump on Mondays
         at 6:30 PM"                          (dup)
  s41:4/8 "protein-rich snacks ... BodyPump on Mondays" x2
                                              (dup)
  s43:0 "my Saturday morning Hip Hop Abs class with Mike ..."
                                              (hiphopabs: Sat)
  s43:2 "a playlist for my yoga classes on Sundays" (dup)
  s43:6 "I attend Hip Hop Abs on Saturdays at 10:00 AM" (dup)

  = |{zumba: 2}| + |{bodypump: 1}| + |{yoga: 1}|
    + |{hiphopabs: 1}| -> 5 (GT 5).

Wall discipline (both walls load-bearing):

- class-identity wall: only the four scheduled class names key
  (zumba / body ?pump / hip hop abs / yoga). 'meal prepping on
  Sundays' (day, no class) and 'sculpting classes for a few
  months' (class noun, no name, no day) stay dark.
- day-of-week wall: a name without a concrete weekday never
  keys — 'attending different classes like Zumba, Hip Hop
  Abs, yoga, and BodyPump' (all four names, zero days) stays
  dark, as does 'on days when I have BodyPump classes' (the
  bare word 'days' is not a weekday). 'weekday(s)' likewise
  never matches.
- dedup: re-mentions fold into the same (class, day) set —
  zumba re-mention stays 2, bodypump re-mentions stay 1.
- assistant surfaces repeat the full schedule — the user-role
  wall backstops every echo.

Census (all 500, 09-27): the strict head matches EXACTLY its
own row (2788b940, unbanked, gate=answer / WRONG today — the
frozen pred is a meal-prep/fitness-goals echo). The loose
'fitness class' sweep hits one cousin with a different head,
a08a253f 'How many days a week do I attend fitness classes?'
— never claimed (pinned below). Render the digit total '5' —
GT is int 5; exact, counting_judge numeric-first and
judge_semantic all bank on the digit match.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_fitness_week,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = 'How many fitness classes do I attend in a typical week?'

# verbatim dataset fixtures (2788b940; 09-27 census)
U_ZUMBA = (
    "By the way, I usually take Zumba classes on Tuesdays and "
    "Thursdays at 7:00 PM, so something upbeat would be great.")
U_ZUMBA_RE = (
    "For my Zumba classes on Tuesdays and Thursdays, I like to "
    "get there about 15 minutes early to warm up.")
U_BODYPUMP = (
    "I've recently started taking a BodyPump class on Mondays "
    "and want something that'll keep me pumped up during those "
    "intense weightlifting sessions.")
U_BODYPUMP_RE = (
    "I need something to motivate me during my weightlifting "
    "classes, like BodyPump on Mondays at 6:30 PM.")
U_YOGA = (
    "By the way, I'm not free on Sundays since I have my yoga "
    "class at 6:00 PM, so anything that can be done on other "
    "days would be great.")
U_YOGA_RE = (
    "I was thinking of also making a playlist for my yoga "
    "classes on Sundays.")
U_HHA = (
    "Do you have any hip hop playlists that could get me "
    "pumped up for my Saturday morning Hip Hop Abs class with "
    "Mike at 10:00 AM?")
U_HHA_RE = (
    "By the way, I attend Hip Hop Abs on Saturdays at 10:00 "
    "AM, which gets me pumped up for the day!")

# structural wall shapes (verbatim row fragments pinned)
U_ENUM = (
    "I try to mix up my workout routine by attending different "
    "classes like Zumba, Hip Hop Abs, yoga, and BodyPump.")
U_MEAL_PREP = (
    "I've been doing great with meal prepping on Sundays, but "
    "I want to explore some healthy snack options to curb my "
    "junk food cravings.")
U_SCULPT = (
    "I've been taking sculpting classes for a few months now, "
    "and I've gotten pretty comfortable with ceramic clay.")
U_YOGA_HOME = "I'm looking for some new yoga routines to try at home."
U_BP_NO_DAY = (
    "Do you have any recommendations on how to incorporate "
    "protein shakes into my routine, especially on days when I "
    "have BodyPump classes?")
U_WEEKDAY_GENERIC = (
    "I'll try to adjust my wake-up time and fit in a quick "
    "15-20 minute workout in the morning on weekdays.")
A_ECHO_ALL_WALLS = (
    "You mentioned you take Zumba classes on Tuesdays and "
    "Thursdays, a BodyPump class on Mondays, your yoga class "
    "on Sundays, and Hip Hop Abs on Saturdays.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: evidence sessions in dataset order
S_ROW = mk(
    ("sess_1", [("user", U_ZUMBA),
                ("user", U_BODYPUMP),
                ("user", U_ZUMBA_RE)]),
    ("sess_39", [("user", U_YOGA)]),
    ("sess_41", [("user", U_BODYPUMP_RE)]),
    ("sess_43", [("user", U_HHA),
                 ("user", U_YOGA_RE),
                 ("user", U_HHA_RE)]))


class TestForm(unittest.TestCase):
    def test_form_routes_fitness_week(self):
        self.assertEqual(counting_form(Q), "fitness_week")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # fitness_week), and the fitness handler is dark on
        # all of them
        for q in (
            'How many sports have I played competitively in '
            'the past?',
            'How many times did I ride rollercoasters across '
            'all the events I attended from July to October?',
            'How many different art-related events did I '
            'attend in the past month?',
            'How many days did I spend attending workshops, '
            'lectures, and conferences in April?',
            'How many weddings have I attended in this year?',
            'How many pre-1920 American coins do I have in my '
            'collection?',
        ):
            self.assertNotEqual(counting_form(q), "fitness_week",
                                q)
            self.assertIsNone(_cnt_fitness_week(q, S_ROW), q)

    def test_days_a_week_cousin_keeps_freq_days(self):
        # a08a253f: the loose 'fitness classes' cousin in the
        # 500 carries a DIFFERENT head — pre-existing
        # freq_days territory, never fitness_week
        q = 'How many days a week do I attend fitness classes?'
        self.assertNotEqual(counting_form(q), "fitness_week")
        self.assertIsNone(_cnt_fitness_week(q, S_ROW))

    def test_typical_week_hours_cousin_not_claimed(self):
        # a4996e51: 'typical week' alone doesn't key the head
        q = ('How many hours do I work in a typical week '
             'during peak campaign seasons?')
        self.assertNotEqual(counting_form(q), "fitness_week")
        self.assertIsNone(_cnt_fitness_week(q, S_ROW))

    def test_attend_variant_head_not_claimed(self):
        q = 'How many fitness classes do I attend every week?'
        self.assertNotEqual(counting_form(q), "fitness_week")
        self.assertIsNone(_cnt_fitness_week(q, S_ROW))


class TestFitnessWeek(unittest.TestCase):
    def test_row_resolves_five(self):
        self.assertEqual(_cnt_fitness_week(Q, S_ROW), "5")

    def test_zumba_two_days_one_sentence(self):
        # 'Tuesdays and Thursdays' -> both days count
        sess = one("sess_1", "user", U_ZUMBA)
        self.assertEqual(_cnt_fitness_week(Q, sess), "2")

    def test_each_single_day_class_counts_one(self):
        for u in (U_BODYPUMP, U_YOGA, U_HHA):
            sess = one("s1", "user", u)
            self.assertEqual(_cnt_fitness_week(Q, sess), "1", u)

    def test_classes_additive_across_sentences(self):
        sess = mk(("s1", [("user", U_ZUMBA)]),
                  ("s2", [("user", U_YOGA)]),
                  ("s3", [("user", U_HHA)]))
        self.assertEqual(_cnt_fitness_week(Q, sess), "4")

    def test_rementions_dedup_within_class(self):
        # zumba re-mention (same two days) + bodypump
        # re-mentions (same Monday) never inflate
        sess = mk(("s1", [("user", U_ZUMBA),
                          ("user", U_ZUMBA_RE)]),
                  ("s2", [("user", U_BODYPUMP),
                          ("user", U_BODYPUMP_RE)]))
        self.assertEqual(_cnt_fitness_week(Q, sess), "3")

    def test_new_day_on_known_class_adds(self):
        sess = mk(("s1", [("user", U_BODYPUMP)]),
                  ("s2", [("user",
                           "By the way, I started a second "
                           "BodyPump class on Wednesdays "
                           "too.")]))
        self.assertEqual(_cnt_fitness_week(Q, sess), "2")

    def test_name_enumeration_without_days_dark(self):
        # all four names, zero weekdays — the day wall is
        # load-bearing
        sess = one("s1", "user", U_ENUM)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_meal_prep_sundays_dark(self):
        # day-of-week without a class name
        sess = one("s1", "user", U_MEAL_PREP)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_sculpting_classes_dark(self):
        # class noun outside the name wall, no day either
        sess = one("s1", "user", U_SCULPT)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_yoga_without_day_dark(self):
        sess = one("s1", "user", U_YOGA_HOME)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_bodypump_bare_days_word_dark(self):
        # 'on days when I have BodyPump classes' — the bare
        # word 'days' is not a weekday
        sess = one("s1", "user", U_BP_NO_DAY)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_generic_weekday_dark(self):
        # 'weekdays' never matches the day wall; no name either
        sess = one("s1", "user", U_WEEKDAY_GENERIC)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_yogurt_never_keys_yoga(self):
        # word-boundary guard: 'Greek yogurt' is not yoga
        sess = one("s1", "user",
                   "I'm thinking of trying some protein-rich "
                   "snacks like Greek yogurt to support my "
                   "goals.")
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_assistant_echo_dark(self):
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        self.assertIsNone(_cnt_fitness_week(Q, sess))

    def test_assistant_echo_does_not_disturb_user_evidence(self):
        sess = mk(("s1", [("user", U_ZUMBA),
                          ("user", U_YOGA)]),
                  ("s2", [("assistant", A_ECHO_ALL_WALLS)]))
        self.assertEqual(_cnt_fitness_week(Q, sess), "3")

    def test_dark_sentences_do_not_disturb_row(self):
        # the full row plus every dark shape still resolves 5
        sess = mk(
            ("sess_1", [("user", U_ZUMBA),
                        ("user", U_BODYPUMP),
                        ("user", U_ZUMBA_RE),
                        ("user", U_ENUM),
                        ("user", U_MEAL_PREP)]),
            ("sess_12", [("user", U_YOGA_HOME)]),
            ("sess_22", [("user", U_SCULPT)]),
            ("sess_39", [("user", U_YOGA)]),
            ("sess_41", [("user", U_BODYPUMP_RE),
                         ("user", U_BP_NO_DAY),
                         ("user", U_WEEKDAY_GENERIC)]),
            ("sess_43", [("user", U_HHA),
                         ("user", U_YOGA_RE),
                         ("user", U_HHA_RE)]))
        self.assertEqual(_cnt_fitness_week(Q, sess), "5")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric_gt(self):
        self.assertTrue(counting_judge(Q, "5", "5"))
        self.assertFalse(counting_judge(Q, "5", "4"))

    def test_exact_judge_banks_digit_match(self):
        self.assertEqual(exact_judge(Q, "5", "5"), True)

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "5", "5"), "CORRECT")
        self.assertEqual(judge_semantic(Q, "5", "4"), "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "5")
        self.assertEqual(meta, {"form": "fitness_week"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = one("s1", "assistant", A_ECHO_ALL_WALLS)
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "fitness_week"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
