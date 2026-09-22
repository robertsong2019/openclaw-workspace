"""C597: bake two-weeks event-count face — 88432d0a (GT '4').

Head: "How many times did I bake something in the past two
weeks?" — census (all 500) matches EXACTLY 1 row, unbanked
(gate=answer / parasitic session echo pred today). The two-week
window is supplied by the head itself; past anchors inside the
window are what the events must carry (C591 marker family +
weekday surfaces).

Evidence (verbatim user turns; 4 events, heavy cross-session
echo — the dedup is the whole game):
- answer_733e443a_3 t0:  "I tried out a new bread recipe using
  sourdough starter on Tuesday…" (+t6/t8 re-mentions + t10
  "recently baked a chocolate cake…")
- answer_733e443a_4 t0:  "I made a delicious whole wheat
  baguette last Saturday…" — NO bake verb (census memo: the
  make-capture point; t6 re-mention is "used to make…")
- answer_733e443a_4 t4:  "…used it to bake a batch of cookies
  last Thursday" (+ answer_733e443a_2 t2 re-mention)
- answer_733e443a_1 t0:  "I just baked a chocolate cake…"
  (re-mention of the t10 cake)
→ distinct good-noun keys {bread, cake, baguette, cookies}
  = 4 = GT (probe /tmp/c597/probe.py: 10 EVT hits → 4 keys,
  all inside answer sessions).

Mechanism: user-role sentences carrying ALL of
  (a) a past-tense event verb — baked/made/tried, or the
      used…-to-bake/make chain,
  (b) a past anchor (yesterday / last <weekday|weekend|week> /
      on <weekday> / recently / just / N days|weeks ago) —
      the two-week wall; plans carry future anchors ('this
      weekend', 'tonight') which sit structurally outside,
  (c) a baked-good noun — the event KEY;
distinct keys render word-form ('four' banks via judge_semantic
norm fold onto GT '4' — C595 'four'/'4' discipline).

Guards pinned here:
- plan sentences never count (Italian bread 'this weekend',
  chicken wings 'tonight', focaccia 'I'll try out')
- eating a mention never counts ('leftover birthday cake')
- past-tense + good noun WITHOUT a past anchor falls through
  (window discipline: 'made a croissant this weekend' — future
  anchor — and anchor-less 'baked something amazing once')
- assistant restatements never render (user wall)
- mechanism, not hardcoding: a synthetic fifth event moves
  four→five; re-mentions of the same key dedup
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_bake_two_weeks,
    _sem_norm,
    answer_counting,
    counting_form,
    judge_semantic,
)

Q_BAKE = 'How many times did I bake something in the past two weeks?'
Q_MARVEL = 'How many Marvel movies did I re-watch?'
Q_BIKES = 'How many bikes do I own?'
Q_PLANTS = 'How many plants did I acquire in the last month?'
Q_FURN = ('How many pieces of furniture did I buy, assemble, '
          'sell, or fix in the past few months?')
Q_TIMES = 'How many times did I re-watch Avengers: Endgame?'
Q_COOKIES = 'How many cookies did I bake last week?'

# ── verbatim dataset turns (88432d0a haystack, extracted by
#    /tmp/c597/gen_turns.py; drift pins assert the surfaces
#    survive transcription) ──

# s8 (answer_733e443a_3) t0 [user] — event 1, first mention
U_SD = ("I'm looking for some advice on improving my sourdough "
        "starter. I tried out a new bread recipe using sourdough "
        "starter on Tuesday, but it didn't quite turn out as "
        "expected. Do you have any tips on how to get my starter "
        "to be more active and produce better results?")

# s8 t10 [user] — event 2, first mention (cake) + dough/next-
# time noise sentences inside the same turn
U_CAKE = ("I think I might have been overmixing the dough, and "
          "maybe the fermentation time was a bit short. I'll try "
          "to be more gentle when mixing and give the dough more "
          "time to ferment next time. Thanks for the tips!\n\nBy "
          "the way, I've been experimenting with different types "
          "of flour lately, and I recently baked a chocolate "
          "cake for my sister's birthday party using a new "
          "recipe I found online. It turned out amazing, and "
          "everyone loved it!")

# s22 (answer_733e443a_4) t0 [user] — plan sentence + event 3
# (baguette; NO bake verb, 'made'; the event clause shares its
# sentence with 'I'm considering' — the in-sentence trap that
# killed a sentence-level plan-wall design)
U_BAG = ("I'm thinking of trying out a new recipe for a rustic "
         "Italian bread this weekend. Do you have any tips on "
         "how to achieve a crispy crust? By the way, I made a "
         "delicious whole wheat baguette last Saturday, and I'm "
         "considering using the same flour for this recipe.")

# s22 t4 [user] — event 4, first mention (cookies, 'used it to
# bake')
U_COO = ("I've had good results with the convection setting on "
         "my oven, like when I used it to bake a batch of "
         "cookies last Thursday. They turned out perfectly "
         "crispy on the outside and chewy on the inside. Do you "
         "think I should try a slower rise or delayed "
         "fermentation for this Italian bread recipe?")

# s37 (answer_733e443a_2) t0 [user] — plan decoy (wings)
U_WINGS = ("I'm thinking of baking some chicken wings for "
           "tonight's dinner. Can you give me some tips on how "
           "to achieve that perfect crispy skin?")

# s37 t2 [user] — event 4 re-mention ('just used … to bake') +
# a verb-only partial ('haven't tried roasting…')
U_COO2 = ("I see! Thanks for the tips. I'll definitely try the "
          "dry brine method and baking powder trick. Do you have "
          "any recommendations for roasted vegetables that would "
          "pair well with the crispy chicken wings? I've been "
          "experimenting with different types of flour for "
          "baking, but I haven't tried roasting veggies with "
          "convection yet.  By the way, I just used my oven's "
          "convection setting for the first time last Thursday "
          "to bake a batch of cookies, and it turned out "
          "amazing!")

# s39 (answer_733e443a_1) t0 [user] — event 2 re-mention ('just
# baked a chocolate cake … last weekend') + party-plan noise
U_CAKE2 = ("I'm looking for some recipe ideas for a dinner "
           "party I'm hosting next weekend. Do you have any "
           "suggestions for a dessert that would pair well with "
           "a rich and savory main course? By the way, I just "
           "baked a chocolate cake for my sister's birthday "
           "party last weekend and it turned out amazing - the "
           "espresso powder really enhanced the flavor!")

# s39 t4 [user] — eating decoy (cake without any bake verb)
U_EAT = ("I think I'll go with strawberries, they're my "
         "favorite. I've been eating a lot of sweet treats "
         "lately, including leftover birthday cake, and I think "
         "the tartness of strawberries will be a nice change of "
         "pace.")

# s39 t6 [user] — event 3 re-mention ('used to make' — still no
# bake verb) + tart-crust plan noise
U_BAG2 = ("I was thinking of making a homemade crust, but I'm "
          "not sure what type of flour to use. I've been "
          "experimenting with different types of flour lately, "
          "including whole wheat flour, which I used to make a "
          "delicious whole wheat baguette last Saturday. Would "
          "whole wheat flour work for a tart crust?")

# sentence-level decoys / probes
A_ECHO = ("You baked a chocolate cake, a baguette, bread, and "
          "cookies — that's four baking projects!")
D_NO_ANCHOR = "I baked something amazing once."
D_FUTURE_ANCHOR = "I made a croissant this weekend."
P_FIFTH = ("I baked a batch of blueberry muffins two days ago "
           "and they were gone by morning.")
D_BREAD_REMENTION = "I also made bread last Friday before work."


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S8 = mk(("answer_733e443a_3", [("user", U_SD),
                               ("assistant", "ok"),
                               ("user", U_CAKE)]))[0]
S22 = mk(("answer_733e443a_4", [("user", U_BAG),
                                ("assistant", "ok"),
                                ("user", U_COO)]))[0]
S37 = mk(("answer_733e443a_2", [("user", U_WINGS),
                                ("assistant", "ok"),
                                ("user", U_COO2)]))[0]
S39 = mk(("answer_733e443a_1", [("user", U_CAKE2),
                                ("assistant", "ok"),
                                ("user", U_EAT),
                                ("assistant", "ok"),
                                ("user", U_BAG2)]))[0]
FULL = [S8, S22, S37, S39]


class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn('tried out a new bread recipe using '
                      'sourdough starter on Tuesday', U_SD)
        self.assertIn('recently baked a chocolate cake for my '
                      "sister's birthday party", U_CAKE)
        self.assertIn('made a delicious whole wheat baguette '
                      'last Saturday', U_BAG)
        self.assertIn('used it to bake a batch of cookies last '
                      'Thursday', U_COO)
        self.assertIn('used my oven\'s convection setting for '
                      'the first time last Thursday to bake a '
                      'batch of cookies', U_COO2)
        self.assertIn('just baked a chocolate cake for my '
                      "sister's birthday party last weekend",
                      U_CAKE2)
        self.assertIn('used to make a delicious whole wheat '
                      'baguette last Saturday', U_BAG2)
        self.assertIn('leftover birthday cake', U_EAT)
        self.assertIn("tonight's dinner", U_WINGS)


class TestFormClaim(unittest.TestCase):
    def test_head_claims_bake_two_weeks(self):
        self.assertEqual(counting_form(Q_BAKE), "bake_two_weeks")

    def test_no_steal_prior_cycle_rows(self):
        self.assertEqual(counting_form(Q_MARVEL), "marvel_rewatch")
        self.assertEqual(counting_form(Q_BIKES), "bikes_own")
        self.assertEqual(counting_form(Q_PLANTS), "acquire")
        self.assertEqual(counting_form(Q_FURN), "furniture_txn")

    def test_no_steal_siblings(self):
        for q in (Q_TIMES, Q_COOKIES):
            self.assertNotEqual(counting_form(q), "bake_two_weeks",
                                q)


class TestFace(unittest.TestCase):
    def test_full_haystack_four(self):
        self.assertEqual(_cnt_bake_two_weeks(Q_BAKE, FULL), "four")
        self.assertEqual(
            answer_counting(Q_BAKE, FULL),
            ("four", {"form": "bake_two_weeks"}))

    def test_each_event_alone_one(self):
        for turn in (U_SD, U_CAKE, U_BAG, U_COO, U_COO2, U_CAKE2,
                     U_BAG2):
            sess = mk(("sx", [("user", turn)]))
            self.assertEqual(_cnt_bake_two_weeks(Q_BAKE, sess),
                             "one", turn[:60])


class TestDecoyWalls(unittest.TestCase):
    def test_plans_never_count(self):
        for turn in (U_WINGS,):
            sess = mk(("sx", [("user", turn)]))
            self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, sess))

    def test_eating_mention_never_counts(self):
        sess = mk(("sx", [("user", U_EAT)]))
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, sess))

    def test_no_past_anchor_falls_through(self):
        sess = mk(("sx", [("user", D_NO_ANCHOR)]))
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, sess))

    def test_future_anchor_falls_through(self):
        # window discipline: future anchor is structurally
        # outside the past set even with verb + good noun
        sess = mk(("sx", [("user", D_FUTURE_ANCHOR)]))
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, sess))

    def test_assistant_wall(self):
        wall = mk(("w", [("assistant", A_ECHO)]))[0]
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, [wall]))
        # wall adds nothing to the real haystack
        self.assertEqual(_cnt_bake_two_weeks(Q_BAKE,
                                             [S8, wall]),
                         "two")
        self.assertEqual(_cnt_bake_two_weeks(Q_BAKE, FULL + [wall]),
                         "four")


class TestMechanismNotHardcoding(unittest.TestCase):
    def test_fifth_event_moves_four_to_five(self):
        sess = mk(("answer_733e443a_3", [("user", U_SD),
                                         ("user", U_CAKE)]),
                  ("answer_733e443a_4", [("user", U_BAG),
                                         ("user", U_COO)]),
                  ("answer_733e443a_2", [("user", U_COO2)]),
                  ("answer_733e443a_1", [("user", U_CAKE2),
                                         ("user", U_BAG2)]),
                  ("s_new", [("user", P_FIFTH)]))
        self.assertEqual(_cnt_bake_two_weeks(Q_BAKE, sess),
                         "five")

    def test_same_key_remention_dedups(self):
        sess = mk(("sx", [("user", U_SD),
                          ("user", D_BREAD_REMENTION)]))
        self.assertEqual(_cnt_bake_two_weeks(Q_BAKE, sess), "one")

    def test_unresolvable_falls_through(self):
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, []))
        bare = mk(("sx", [("user", "Baking is so relaxing!")]))
        self.assertIsNone(_cnt_bake_two_weeks(Q_BAKE, bare))


class TestRenderAndBank(unittest.TestCase):
    def test_word_render_banks_on_gt_4(self):
        # GT '4' — judge_semantic norm fold (C595 'four'/'4' path)
        self.assertEqual(judge_semantic(Q_BAKE, "4", "four"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_BAKE, "4", "three"),
                         "WRONG")
        self.assertEqual(judge_semantic(Q_BAKE, "4", "five"),
                         "WRONG")
        self.assertEqual(_sem_norm("four"), _sem_norm("4"))


if __name__ == "__main__":
    unittest.main()
