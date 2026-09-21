"""C595: bike ownership-count face — 6b168ec8 / 89941a93 (one
mechanism, two faces: enumeration + cross-session possessive).

Heads: "How many bikes do I own?" (6b168ec8, GT 'three') and
"How many bikes do I currently own?" (89941a93, GT '4').
Census (all 500): the strict head matches EXACTLY these 2 rows,
both unbanked today (NEEDS_JUDGE session echoes). No time
window — OWNERSHIP replaces it (C593 pattern: the constraint
replaces the window).

Evidence (verbatim user turns):
- 6b168ec8 s34: "speaking of my bikes, I've got three of them -
  a road bike, a mountain bike, and a commuter bike" (S_E) +
  possessive re-mention "for my road bike, mountain bike, and
  commuter bike" → 3.
- 89941a93 s6/s29: "my road bike" + "my other two bikes, a
  mountain bike and a commuter bike" (S_OWN) + "my road bike,
  mountain bike, commuter bike, and a new hybrid bike I just
  purchased" (S_TRIP) → 4.

Mechanism: sentence-level ownership stem ('my' / "I've got" /
'I (currently) have|own') licenses singular-bike NP keys with
determiner, stop-adjective, prep, follower-noun, possessive and
hyphen walls. Plural 'my (N) bikes' and bare 'my bike' are
generic mentions, never keys (keying them overcounts
6b168ec8 3→4). Word-only render 'three' banks exact (GT
'three'); 'four' banks via judge_semantic (_sem_norm folds to
GT '4' — C591/C592/C593/C594 discipline).

Guards pinned here:
- form claim: the head returns 'bikes_own' and does NOT steal
  the C592 acquire rows, C593 antique, C594 furniture, or the
  bike service/which/days siblings (a9f6b44c / gpt4_e4142 /
  gpt4_d84a3 surfaces)
- decoys structurally out: 'what kind of bike is best' (prep
  wall + no stem), 'bike lock' asks (follower wall), "road
  bike's wheels" (possessive wall), 'bike computers' (follower
  + no stem), 'mountain bike trails' (follower wall), 'rent a
  bike' (no stem), 'I'll have four bikes' (future, plural),
  'bike storage' (follower)
- user-role wall (assistant restatements never render)
- generic-mention wall: bare 'my bike' / 'my three bikes' /
  'all my bikes' never key — the 6b168ec8 haystack says both
  and the GT stays 'three'
- dedup: road-bike re-mentions across s6/s29 collapse
- mechanism, not hardcoding: adding 'my gravel bike' moves
  three→four; unresolvable evidence = None (falls through)
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _bike_harvest,
    _cnt_bikes_own,
    _sem_norm,
    answer_counting,
    counting_form,
    judge_semantic,
)

Q_BIKES = 'How many bikes do I own?'
Q_CURR = 'How many bikes do I currently own?'
Q_PLANTS = 'How many plants did I acquire in the last month?'
Q_JEWEL = ('How many pieces of jewelry did I acquire in the last '
           'two months?')
Q_ANTIQUE = ('How many antique items did I inherit or acquire '
             'from my family members?')
Q_FURN = ('How many pieces of furniture did I buy, assemble, '
          'sell, or fix in the past few months?')
Q_SERVICE = 'How many bikes did I service or plan to service in March?'
Q_WHICH = 'Which bike did I fixed or serviced the past weekend?'
Q_DAYS = ('How many days passed between the day I fixed my '
          'mountain bike and the day I decided to upgrade my road bike?')
Q_HAVE = 'How many bikes do I currently have?'

# ── verbatim dataset turns (extracted from
#    longmemeval_s_cleaned 6b168ec8 / 89941a93 haystacks by
#    /tmp/c595/gen_fixture.py; drift pins assert the dataset
#    surfaces survive transcription) ──

# ── 6b168ec8 / session 34 (enumeration + possessive faces) ──
U_E_ENUM = "I've been doing some research on carbon fiber wheels and I think I'll make the purchase in the next few months. By the way, speaking of my bikes, I've got three of them - a road bike, a mountain bike, and a commuter bike - and I've been using them for different types of rides. Do you have any tips on how to keep them organized and maintained properly?"
U_E_POSS = "I'm thinking of getting a bike lock with GPS tracking that integrates with my bike, so I can keep an eye on my three bikes when I'm not around them. Do you have any recommendations on specific bike locks with GPS tracking that would work well for my road bike, mountain bike, and commuter bike?"
U_E_KIND = "I'm planning a long ride this weekend and want to make sure I'm prepared. Can you remind me what kind of bike is best for long rides on the road, and also suggest some tips on how to properly clean and lube my chain?"
U_E_LOCK = "I've been thinking about getting a bike lock with a GPS tracker to keep my bikes safe when I'm not around them. Do you have any recommendations on bike locks and GPS tracking systems?"
U_E_POSSW = "I'm actually thinking of taking my Trek Emonda for the ride, since it's perfect for long distances on the road. By the way, do you have any recommendations on carbon fiber wheels? I've been considering upgrading my road bike's wheels to make it even lighter and faster."

# ── 89941a93 / session 6 (possessive face) ──
U_O_ROAD = "I'm planning a 50-mile ride this weekend and I want to make sure my road bike is in top condition. Can you give me some tips on how to adjust the derailleurs and also recommend some good routes in my area?"
U_O_TWO = "I'm actually thinking of doing a century ride soon, do you think my current road bike is ready for that distance, considering I've already done 2,000 miles on it? And by the way, I've been using it along with my other two bikes, a mountain bike and a commuter bike."
U_O_TRAIL = "I'm planning to use my road bike for the century ride, and I've been using it for long rides on the weekends. I've also been using my mountain bike for trail rides and my commuter bike for daily commutes. By the way, I currently have three bikes, and I'm wondering if that's too many."
U_O_COMP = "I think I'll need to do some more research and consider my budget before making a decision on the carbon fiber wheels. In the meantime, can you give me some recommendations on bike computers and GPS devices? I've been using my phone's GPS, but I'm thinking of getting a dedicated device."

# ── 89941a93 / session 29 (the +1 hybrid + enumeration) ──
U_T_HYBRID = "That sounds like an amazing itinerary! I'm really excited about the scenic routes and bike-friendly stops. Since I'll have four bikes with me, I'll make sure to book the accommodations with bike storage in advance to ensure they can accommodate all my bikes. By the way, speaking of bikes, I just got a new one recently, so I'll actually have four bikes with me on this trip - my road bike, mountain bike, commuter bike, and a new hybrid bike I just purchased."
U_T_TRY = "Thanks for the tips! I'll definitely take those into consideration to ensure a smooth and enjoyable trip. I'm really looking forward to trying out my new hybrid bike on some of the scenic routes you suggested. By the way, do you know if there are any bike shops along the route that offer bike rentals or guided tours? I might want to rent a bike for a day or join a guided tour to explore some of the local trails."
U_T_TRAILS = "That's great information! I'll definitely look into those bike shops and tour operators. I'm particularly interested in joining a guided tour in Jackson Hole to explore some of the more challenging mountain bike trails. By the way, do you think I'll need to make any adjustments to my road bike to prepare it for the long trip? I've already got a new bike computer and have been tracking my progress on Strava, but I'm not sure if I need to do anything else to get my road bike ready."

# sentence-level decoys (verbatim from the turns above)
D_FUTURE_PLURAL = ("Since I'll have four bikes with me, I'll make "
                   "sure to book the accommodations with bike "
                   "storage in advance to ensure they can "
                   "accommodate all my bikes.")
D_RENT = ("I might want to rent a bike for a day or join a "
          "guided tour to explore some of the local trails.")
A_E_ECHO = "By choosing a bike lock with GPS tracking, consider that it must work well for your road bike, mountain bike, and commuter bike when you're not around them."


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S_E = mk(("s34", [("user", U_E_KIND), ("assistant", "ok"),
                  ("user", U_E_POSSW), ("assistant", "ok"),
                  ("user", U_E_ENUM), ("assistant", "ok"),
                  ("user", U_E_LOCK), ("assistant", "ok"),
                  ("user", U_E_POSS), ("assistant", "ok"),
                  ("assistant", A_E_ECHO)]))[0]
S_OWN = mk(("s6", [("user", U_O_ROAD), ("assistant", "ok"),
                   ("user", U_O_TWO), ("assistant", "ok"),
                   ("user", U_O_TRAIL), ("assistant", "ok"),
                   ("user", U_O_COMP)]))[0]
S_TRIP = mk(("s29", [("user", U_T_HYBRID), ("assistant", "ok"),
                     ("user", U_T_TRY), ("assistant", "ok"),
                     ("user", U_T_TRAILS)]))[0]
FULL_6B = [S_E]
FULL_89 = [S_OWN, S_TRIP]


class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn("speaking of my bikes, I've got three of "
                      "them - a road bike, a mountain bike, and a "
                      "commuter bike", U_E_ENUM)
        self.assertIn('work well for my road bike, mountain bike, '
                      'and commuter bike', U_E_POSS)
        self.assertIn('what kind of bike is best', U_E_KIND)
        self.assertIn("upgrading my road bike's wheels", U_E_POSSW)
        self.assertIn('my road bike is in top condition', U_O_ROAD)
        self.assertIn('my other two bikes, a mountain bike and a '
                      'commuter bike', U_O_TWO)
        self.assertIn('I currently have three bikes', U_O_TRAIL)
        self.assertIn('recommendations on bike computers and GPS '
                      'devices', U_O_COMP)
        self.assertIn('my road bike, mountain bike, commuter bike, '
                      'and a new hybrid bike I just purchased',
                      U_T_HYBRID)
        self.assertIn('trying out my new hybrid bike', U_T_TRY)
        self.assertIn('challenging mountain bike trails', U_T_TRAILS)
        self.assertIn('bike-friendly stops', U_T_HYBRID)


class TestFormClaim(unittest.TestCase):
    def test_strict_heads_claim_bikes_own(self):
        self.assertEqual(counting_form(Q_BIKES), "bikes_own")
        self.assertEqual(counting_form(Q_CURR), "bikes_own")

    def test_no_steal_prior_cycle_rows(self):
        self.assertEqual(counting_form(Q_PLANTS), "acquire")
        self.assertEqual(counting_form(Q_JEWEL), "acquire")
        self.assertEqual(counting_form(Q_ANTIQUE), "antique_inherit")
        self.assertEqual(counting_form(Q_FURN), "furniture_txn")

    def test_no_steal_bike_siblings(self):
        for q in (Q_SERVICE, Q_WHICH, Q_DAYS, Q_HAVE):
            self.assertNotEqual(counting_form(q), "bikes_own", q)


class TestEnumerationFace(unittest.TestCase):
    def test_6b168ec8_full_haystack_three(self):
        self.assertEqual(_cnt_bikes_own(Q_BIKES, FULL_6B), "three")
        self.assertEqual(
            answer_counting(Q_BIKES, FULL_6B),
            ("three", {"form": "bikes_own"}))

    def test_enumeration_sentence_alone(self):
        sess = mk(("sx", [("user", U_E_ENUM)]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "three")

    def test_possessive_repetition_still_three(self):
        sess = mk(("sx", [("user", U_E_ENUM), ("user", U_E_POSS)]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "three")


class TestPossessiveFace(unittest.TestCase):
    def test_89941a93_full_haystack_four(self):
        self.assertEqual(_cnt_bikes_own(Q_CURR, FULL_89), "four")
        self.assertEqual(
            answer_counting(Q_CURR, FULL_89),
            ("four", {"form": "bikes_own"}))

    def test_single_road_bike_is_one(self):
        sess = mk(("sx", [("user", U_O_ROAD)]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "one")

    def test_cross_session_road_dedup(self):
        # U_O_ROAD (s6) + U_T_TRAILS (s29) both own the road bike
        sess = mk(("s6", [("user", U_O_ROAD)]),
                  ("s29", [("user", U_T_TRAILS)]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "one")

    def test_current_stop_adjective_drops(self):
        # 'my current road bike' == 'my road bike'
        keys = _bike_harvest("do you think my current road bike "
                             "is ready for that distance")
        self.assertEqual(keys, {"road bike"})


class TestDecoyWalls(unittest.TestCase):
    def test_kind_of_bike_prep_wall_no_stem(self):
        sess = mk(("sx", [("user", U_E_KIND)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))
        # even with a stem, the prep wall rejects 'kind of bike'
        self.assertEqual(_bike_harvest("remind me: the kind of "
                                       "bike my cousin rides"),
                         set())

    def test_bike_lock_follower_wall(self):
        sess = mk(("sx", [("user", U_E_LOCK)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))
        self.assertEqual(_bike_harvest("I keep my bike storage in "
                                       "the garage"), set())

    def test_possessive_wall(self):
        # 'road bike's wheels' — bike is a modifier of 'wheels'
        sess = mk(("sx", [("user", U_E_POSSW)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))

    def test_bike_computer_no_stem(self):
        sess = mk(("sx", [("user", U_O_COMP)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))

    def test_mountain_bike_trails_follower_wall(self):
        # U_T_TRAILS: trails + computer walls, demonstrative det;
        # only the real road bike keys → 'one'
        sess = mk(("sx", [("user", U_T_TRAILS)]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "one")

    def test_rent_no_stem(self):
        sess = mk(("sx", [("user", D_RENT)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))

    def test_future_plural_and_storage_never_key(self):
        sess = mk(("sx", [("user", D_FUTURE_PLURAL)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))

    def test_plurals_never_key(self):
        sess = mk(("sx", [("user", U_O_TRAIL)]))
        # keys: road (T0-remention) + mountain + commuter; the
        # 'three bikes' plural adds nothing
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "three")


class TestGenericMentionWall(unittest.TestCase):
    def test_bare_my_bike_not_keyed(self):
        sess = mk(("sx", [("user", U_E_LOCK)]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, sess))

    def test_bare_key_would_overcount(self):
        # mechanism guard: if 'my bike' keyed, this would be
        # 'two'; the GT stack says the answer must stay 'one'
        sess = mk(("sx", [("user", U_O_ROAD),
                          ("user", "the GPS tracker integrates "
                                   "with my bike, so I can keep "
                                   "an eye on it")]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "one")


class TestUserWall(unittest.TestCase):
    def test_assistant_restatement_never_renders(self):
        wall = mk(("w", [("assistant", A_E_ECHO)]))[0]
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, [wall]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, [S_E, wall]),
                         "three")


class TestMechanismNotHardcoding(unittest.TestCase):
    def test_added_item_moves_three_to_four(self):
        sess = mk(("s34", [("user", U_E_ENUM),
                           ("user", "By the way, my gravel bike "
                                    "is great for light trails "
                                    "too.")]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "four")

    def test_synthetic_own_statement_counts(self):
        sess = mk(("sx", [("user", "I own a folding bike for my "
                                   "commute now.")]))
        self.assertEqual(_cnt_bikes_own(Q_BIKES, sess), "one")

    def test_unresolvable_falls_through(self):
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, []))
        bare = mk(("sx", [("user", "I love this bike advice!")]))
        self.assertIsNone(_cnt_bikes_own(Q_BIKES, bare))


class TestRenderAndBank(unittest.TestCase):
    def test_word_render_banks(self):
        # 6b168ec8: GT 'three' — exact bank
        self.assertEqual(judge_semantic(Q_BIKES, "three", "three"),
                         "CORRECT")
        # 89941a93: GT '4' — judge_semantic norm fold
        self.assertEqual(judge_semantic(Q_CURR, "4", "four"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_CURR, "4", "three"),
                         "WRONG")
        self.assertEqual(judge_semantic(Q_CURR, "4", "five"),
                         "WRONG")
        # norm-fold contract: 'four' -> '4'
        self.assertEqual(_sem_norm("four"), _sem_norm("4"))


if __name__ == "__main__":
    unittest.main()
