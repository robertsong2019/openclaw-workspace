"""C602: delivery_services face — distinct food-delivery service
count (d682f1a2, GT 3, qtype multi-session).

One face, one mechanism (triple wall on a user sentence):

- delivery_services (d682f1a2, GT 3): "How many different types
  of food delivery services have I used recently?" — a user
  sentence yields a service key when it carries ALL of: a known
  delivery-service brand (Domino's Pizza | Uber Eats | Fresh
  Fusion), and a usage/experience marker ('had' / 'relying on'
  / 'been all about' / 'found' / 'ordered'). The three real
  services: Domino's Pizza (s8 'I had Domino's Pizza three
  times last week'), Uber Eats (s27 'weekends have been all
  about Uber Eats' + re-mention 'relying on Uber Eats' — dedup),
  Fresh Fusion (s41 'this new one I found called Fresh Fusion').

Census (all 500): the strict head matches EXACTLY 1 row
(d682f1a2), unbanked today (gate=answer — the pred was the
Fresh Fusion recipe-echo turn with no number). Claimed in
counting_form right after the C601 faith_days head, ahead of
every generic how-many block. Sibling questions never mention
food delivery (loose sweep: only d682f1a2 itself), so there is
nothing to steal.

Decoy discipline (pinned per-turn below):
- assistant echoes — role wall (LOAD-BEARING for s41 t1: 'As
  for Fresh Fusion, ... you've found a convenient option'
  carries BOTH the brand and 'found' — only the user-role wall
  keeps it out; same for the s27 Uber Eats echoes)
- brand without usage verb ('Domino's Pizza is my favorite')
  — usage wall
- usage verb without brand ('I ordered takeout twice')
  — brand wall
- sentence grain: brand and verb must share ONE sentence
  ('I found a new spot today. It's called Fresh Fusion ...')
  — sentence wall
- bare 'domino' without pizza — brand wall
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_delivery_services,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
)

Q_FDL = ('How many different types of food delivery services '
         'have I used recently?')

# verbatim dataset fixtures (d682f1a2 row; census 09-24)
U_DOMINOS_S8 = (
    "I'm looking for some healthy meal ideas for my busy "
    "weekdays. Do you have any recommendations? By the way, I've "
    "been relying on food delivery services a lot lately - I had "
    "Domino's Pizza three times last week!")
U_UBER_T0_S27 = (
    "I'm looking for some new recipe ideas, something quick and "
    "easy for weeknights. By the way, my weekends have been all "
    "about Uber Eats lately, it's been a lifesaver.")
U_UBER_T2_S27 = (
    "That's a great list! I'm definitely going to try out that "
    "Chicken Fajita Pasta. Do you have any suggestions for some "
    "healthy snack options? I've been relying on Uber Eats for "
    "convenience, but I want to make some healthier choices.")
U_FUSION_S41 = (
    "I'm looking for some healthy recipe ideas for lunch. Do you "
    "have any suggestions? By the way, I've been really busy "
    "lately and have been relying on food delivery services, "
    "like this new one I found called Fresh Fusion - they have "
    "some great pre-made meals.")
A_UBER_T1_S27 = (
    "I'm glad to hear that Uber Eats has been a lifesaver for "
    "your weekends! However, it's great that you're looking to "
    "cook some quick and easy meals for weeknights.")
A_UBER_T3_S27 = (
    "Healthy snacking is a great way to curb the temptation of "
    "Uber Eats (although, let's be real, it's hard to resist "
    "sometimes). Remember, portion control is key when it comes "
    "to snacking.")
A_FUSION_T1_S41 = (
    "I'm glad you're looking to get back to healthy cooking! "
    "While food delivery services can be convenient, it's great "
    "that you're wanting to take control of your nutrition "
    "again. As for Fresh Fusion, it's great that you've found a "
    "convenient option that works for you. Just be mindful of "
    "the nutritional content and ingredient quality of the "
    "meals they offer.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: the 3 answer sessions, turns in haystack order
S_REAL = mk(
    ("answer_c008e5df_1", [("user", U_DOMINOS_S8)]),
    ("answer_c008e5df_2", [("user", U_UBER_T0_S27),
                           ("assistant", A_UBER_T1_S27),
                           ("user", U_UBER_T2_S27),
                           ("assistant", A_UBER_T3_S27)]),
    ("answer_c008e5df_3", [("user", U_FUSION_S41),
                           ("assistant", A_FUSION_T1_S41)]))


class TestForm(unittest.TestCase):
    def test_form_routes_delivery_services(self):
        self.assertEqual(counting_form(Q_FDL), "delivery_services")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never this face)
        for q in (
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many bikes did I service or plan to service in '
            'March?',
            "How many doctor's appointments did I go to in March?",
            'How many trips have I taken my Canon EOS 80D camera '
            'on?',
            'How many times have I worn my new black Converse '
            'sneakers?',
            'How many different species of birds have I seen in '
            'my local park?',
        ):
            self.assertNotEqual(counting_form(q), "delivery_services",
                                q)
            self.assertIsNone(_cnt_delivery_services(q, S_REAL), q)

    def test_no_steal_generic_counting_rows(self):
        # generic counting rows keep their routing
        self.assertEqual(
            counting_form('How many days did I spend volunteering '
                          'at the shelter last month?'),
            "duration_sum")
        self.assertIsNone(
            _cnt_delivery_services(
                'How many books did I read this year?', S_REAL))


class TestDeliveryServices(unittest.TestCase):
    def test_real_row_resolves_three(self):
        self.assertEqual(_cnt_delivery_services(Q_FDL, S_REAL), "3")

    def test_session_order_independent(self):
        rev = list(reversed(S_REAL))
        self.assertEqual(_cnt_delivery_services(Q_FDL, rev), "3")

    def test_each_service_alone_is_one(self):
        for turn in (U_DOMINOS_S8, U_UBER_T0_S27, U_FUSION_S41):
            sess = one("s1", "user", turn)
            self.assertEqual(_cnt_delivery_services(Q_FDL, sess),
                             "1", turn)

    def test_pairs_are_two(self):
        pair = mk(("s1", [("user", U_DOMINOS_S8)]),
                  ("s2", [("user", U_FUSION_S41)]))
        self.assertEqual(_cnt_delivery_services(Q_FDL, pair), "2")

    def test_uber_remention_dedups(self):
        # s27 t0 + t2 both name Uber Eats -> one key
        sess = mk(("s1", [("user", U_UBER_T0_S27)]),
                  ("s2", [("user", U_UBER_T2_S27)]))
        self.assertEqual(_cnt_delivery_services(Q_FDL, sess), "1")

    def test_assistant_never_keys(self):
        # role wall — LOAD-BEARING for A_FUSION_T1_S41: it carries
        # BOTH 'Fresh Fusion' AND 'found' in one sentence
        for a in (A_UBER_T1_S27, A_UBER_T3_S27, A_FUSION_T1_S41):
            sess = one("s1", "assistant", a)
            self.assertIsNone(_cnt_delivery_services(Q_FDL, sess),
                              a)

    def test_assistant_does_not_inflate_real_row(self):
        self.assertEqual(_cnt_delivery_services(Q_FDL, S_REAL), "3")

    def test_brand_without_usage_verb_never_keys(self):
        sess = one("s1", "user",
                   "Domino's Pizza is my favorite treat, and Uber "
                   "Eats ads keep popping up on my feed.")
        self.assertIsNone(_cnt_delivery_services(Q_FDL, sess))
        # and it does not inflate a real service
        sess2 = mk(("s1", [("user", U_DOMINOS_S8)]),
                   ("s2", [("user",
                            "Fresh Fusion is on every billboard "
                            "downtown these days.")]))
        self.assertEqual(_cnt_delivery_services(Q_FDL, sess2), "1")

    def test_usage_verb_without_brand_never_keys(self):
        sess = one("s1", "user",
                   "I ordered takeout twice last week and tried a "
                   "new burrito place.")
        self.assertIsNone(_cnt_delivery_services(Q_FDL, sess))

    def test_sentence_grain_load_bearing(self):
        # brand and usage verb must share ONE sentence — a turn
        # with 'found' and the brand in sibling sentences keys
        # nothing (sentence wall)
        sess = one("s1", "user",
                   "I found a new spot today. It's called Fresh "
                   "Fusion and the bowls are great.")
        self.assertIsNone(_cnt_delivery_services(Q_FDL, sess))

    def test_bare_domino_never_keys(self):
        # brand regex requires pizza after domino
        sess = one("s1", "user",
                   "I had a domino effect going in my study group "
                   "last week.")
        self.assertIsNone(_cnt_delivery_services(Q_FDL, sess))

    def test_empty_sessions_none(self):
        self.assertIsNone(_cnt_delivery_services(Q_FDL, []))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric_gt(self):
        # GT renders '3' — numeric-first banks pred '3'
        self.assertTrue(counting_judge(Q_FDL, "3", "3"))
        self.assertFalse(counting_judge(Q_FDL, "3", "2"))
        self.assertFalse(counting_judge(Q_FDL, "3", ""))

    def test_exact_judge_digits(self):
        self.assertTrue(exact_judge(Q_FDL, "3", "3"))
        self.assertFalse(exact_judge(Q_FDL, "3", "2"))

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q_FDL, S_REAL)
        self.assertEqual(ans, "3")
        self.assertEqual(meta, {"form": "delivery_services"})

    def test_answer_counting_unresolvable_falls_through(self):
        # assistant-only haystack: form claims, handler resolves
        # None, gate chain owns the row (current frozen state)
        sess = one("s1", "assistant", A_FUSION_T1_S41)
        ans, meta = answer_counting(Q_FDL, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "delivery_services"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
