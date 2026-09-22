"""C599: March-window anchored counting faces — a9f6b44c / 00ca467f.

Two faces, one mechanism family (explicit-March-day anchored
entity counting with key dedup):

- bike_service_march (a9f6b44c, GT 2): "How many bikes did I
  service or plan to service in March?" — serviced face (user
  sentence with <type> bike + servic(e|ed) + March <day>) plus
  plan-to-service face (user TURN with <type> bike + new-tire/
  replace intent + March anchor 'this month, before April').
  Keys: road (Pedal Power, March 10th) + commuter (new tire,
  this month) = 2.
- march_appt (00ca467f, GT 2): "How many doctor's appointments
  did I go to in March?" — user SENTENCE with visit marker
  (went to see | had a ... appointment) + Dr. <Name> key +
  March <day>. Keys: smith (March 3rd) + thompson (March 20th)
  = 2. SENTENCE grain is load-bearing: t6 puts 'March 15th' in
  one sentence and 'Dr. Smith / Dr. Johnson' in the next —
  turn grain would overcount to 3.

Census (all 500): each strict head matches EXACTLY 1 row
(a9f6b44c / 00ca467f), both unbanked (gate=answer / parasitic
session echo today — a9f6b44c currently echoes a TOYOTA CAMRY
service line, 00ca467f a bronchitis line). Neither head can
steal the C592-C598 faces (different NPs/markers) or the
generic how-many block. a9f6b44c routed enum_count before this
cycle (generic block); the strict head now claims it first.

Decoy discipline (pinned per-turn below):
- bike rack 'fit two bikes' — plural bikes never keys; rack is
  not a bike; 'two' is a count decoy
- mountain bike — only a water bottle cage was GOT for it, no
  service verb, no tire intent
- chain cleaning (March 2nd / March 22nd) — 'cleaned and
  lubricated' is not servic(e|ed); road is keyed by the Pedal
  Power line anyway
- copula predicate 'is just a regular hybrid bike' — no March
  anchor in that turn, keys nothing (hybrid stays uncounted;
  GT 2 not 3)
- bike lock / computer / lights / shops / repair services /
  bike-friendly — bike-as-modifier followers, never <type> bike
- undated re-mention 'I had an appointment with my primary
  care physician' — no Dr. key, no March day
- 'considering scheduling' Dr. Patel / 'I'll schedule' Dr.
  Smith+Johnson — intent/future, no March day
- EMG with Dr. Johnson April 1st — April wall (not March)
- physical therapy 'since March 25th ... Dr. Thompson cleared
  me' — March day + Dr. but NO visit marker
- 'should discuss with Dr. Smith ... March 15th' — sentence
  grain keeps the date and the doctors apart
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_bike_service_march,
    _cnt_march_appt,
    answer_counting,
    counting_form,
    counting_judge,
)

Q_SVC = 'How many bikes did I service or plan to service in March?'
Q_APPT = "How many doctor's appointments did I go to in March?"

# no-steal pins (prior cycle rows)
Q_BIKES_OWN = 'How many bikes do I own?'
Q_BIKES_CUR = 'How many bikes do I currently own?'
Q_TRIPS = 'How many trips have I taken my Canon EOS 80D camera on?'
Q_BAKE = 'How many times did I bake something in the past two weeks?'
Q_MARVEL = 'How many Marvel movies did I re-watch?'
Q_ANTIQUE = ('How many antique items did I inherit or acquire '
             'from my family members?')
Q_FURN = ('How many pieces of furniture did I buy, assemble, '
          'sell, or fix in the past few months?')
Q_NEGRONI = ('How many times have I tried making a Negroni at '
             'home since my friend Emma showed me how to make it?')
# March siblings that must NOT be claimed
Q_FUNRUNS = ('How many fun runs did I miss in March due to work '
             'commitments?')
Q_AIRLINE = ('Which airline did I fly with the most in March and '
             'April?')
Q_DAYS = ('How many days passed between the day I fixed my '
          'mountain bike and the day I decided to upgrade my road '
          'bike?')

# ── verbatim dataset turns (transcribed from
#    longmemeval_s_cleaned a9f6b44c / 00ca467f haystacks via
#    /tmp/c599/gen_fixture.py; drift pins assert the dataset
#    surfaces survive transcription) ──

# a9f6b44c / answer_cc021f81_1 t0 [user] — serviced face (road)
U_ROAD_SVC = ("I'm planning a long ride this weekend and wanted "
              "to check the weather forecast for Saturday. Can "
              "you tell me if it's supposed to be sunny or "
              "rainy? By the way, I'm really looking forward to "
              "the ride after getting my road bike serviced at "
              "Pedal Power on March 10th - it's been running so "
              "smoothly since then!")

# a9f6b44c / answer_cc021f81_1 t6 [user] — serviced re-mention
# (same road bike, dedups)
U_ROAD_SVC2 = ("I usually ride on trails with a mix of rocks "
               "and smooth sections. I like the challenge of "
               "navigating through technical sections, but I "
               "also enjoy the flowy parts where I can pick up "
               "speed. As for my favorite trail, I have a few "
               "that I like to ride regularly, but I'm always "
               "looking to explore new ones. By the way, "
               "speaking of bike maintenance, I'm glad I got my "
               "road bike serviced at Pedal Power on March "
               "10th, they replaced the worn-out brake pads and "
               "cables, and it's made a big difference in my "
               "rides.")

# a9f6b44c / answer_cc021f81_2 t0 [user] — plan face (commuter)
U_COMM_PLAN = ("I'm looking into getting a new tire for my "
               "commuter bike. I've been having some issues "
               "with the front tire, and I think it is time to "
               "replace it this month, before April comes.")

# a9f6b44c / answer_cc021f81_2 t2 [user] — copula predicate
# ('just a regular hybrid bike') + NO March anchor in the turn
U_COPULA = ("My commuter bike is just a regular hybrid bike, "
            "and I usually ride on paved roads and bike paths. "
            "I don't carry heavy loads, just my usual commute "
            "to work and back. The issue I'm experiencing is "
            "that the tire is showing signs of wear, and I got "
            "a flat tire on my way to work on February 20th, "
            "so I think it's time to replace it.")

# a9f6b44c / answer_cc021f81_1 t2 [user] — mountain bike, cage
# got FOR it (no service, no tire intent)
U_MTN_CAGE = ("I'll definitely check the weather forecast "
              "online, thanks for the suggestions. I'm also "
              "planning to bring my new water bottle cage on "
              "the ride, which I got for my mountain bike a few "
              "weeks ago. It's been working great so far, and "
              "I'm looking forward to staying hydrated on the "
              "long ride.")

# a9f6b44c / answer_cc021f81_3 t0 [user] — chain cleaning is
# not servic(e|ed); no intent marker
U_CHAIN = ("I'm looking to plan a longer ride this weekend and "
           "was wondering if you could recommend some scenic "
           "bike routes in my area. By the way, my road bike "
           "has been running great since I cleaned and "
           "lubricated the chain on March 2nd - it's been "
           "shifting smoothly and quietly!")

# a9f6b44c / answer_cc021f81_3 t6 [user] — 'bike chain' follower
U_CHAIN2 = ("That sounds great! I'm looking forward to the "
            "ride. Since I've been taking good care of my road "
            "bike, it should be able to handle the hills and "
            "terrain. Speaking of which, I remember cleaning "
            "and lubricating my bike chain on March 22nd, which "
            "has made a big difference in its performance.")

# a9f6b44c / answer_cc021f81_3 t8 [user] — bike shops / repair
# services followers ('services' does not match service\b)
U_SHOPS = ("I'm all set for the ride now. Thanks for the tips "
           "and recommendations. One more thing, can you tell "
           "me if there are any bike shops or repair services "
           "along the route in case I need any assistance?")

# a9f6b44c / answer_cc021f81_2 t8 [user] — accessories followers
U_ACC = ("I'm also thinking about getting some new bike "
         "accessories, such as a bike computer and a set of "
         "bike lights, which would be useful for my early "
         "morning rides.")

# a9f6b44c / 837f258b (non-answer session) t4 [user] — rack +
# 'two bikes' count decoy
U_RACK = ("I'm also considering getting a bike rack for my "
          "car. Do you have any recommendations for a good "
          "bike rack that can fit two bikes securely?")

# 00ca467f / answer_39900a0a_1 t0 [user] — smith (March 3rd)
U_SMITH = ("I've been dealing with a lingering cough for six "
           "weeks now, and I'm wondering if you can recommend "
           "some natural remedies to help soothe my symptoms. "
           "By the way, I finally went to see my primary care "
           "physician, Dr. Smith, on March 3rd, and he "
           "diagnosed me with bronchitis.")

# 00ca467f / answer_39900a0a_3 t0 [user] — thompson (March 20th)
U_THOMPSON = ("I've been dealing with this lingering cough for "
              "weeks, and I'm getting a bit frustrated. Can you "
              "help me find some information on bronchitis and "
              "its common symptoms? By the way, I recently had "
              "a follow-up appointment with my orthopedic "
              "surgeon, Dr. Thompson, on March 20th, and it was "
              "a relief to hear that my knee is healing well.")

# 00ca467f / answer_39900a0a_2 t0 [user] — undated re-mention +
# April EMG wall
U_UNDATED = ("I've been dealing with a lingering cough for "
             "weeks, and I'm still trying to figure out what's "
             "going on. I had an appointment with my primary "
             "care physician, but the antibiotic didn't fully "
             "clear it up. I'm also dealing with some weird "
             "numbness in my left hand, which is why I have an "
             "EMG test scheduled with my neurologist, Dr. "
             "Johnson, on April 1st. Can you help me find some "
             "information on what could be causing these "
             "symptoms?")

# 00ca467f / answer_39900a0a_3 t6 [user] — Patel intent
U_PATEL = ("I'm considering scheduling an appointment with my "
           "gastroenterologist, Dr. Patel, to discuss further "
           "treatment options for my heartburn and acid reflux. "
           "Do you think it's worth exploring natural remedies "
           "like ginger or aloe vera juice to help manage my "
           "symptoms?")

# 00ca467f / answer_39900a0a_1 t8 [user] — future schedule
U_FUTURE = ("I'll schedule an appointment with Dr. Smith and "
            "Dr. Johnson to discuss the numbness in my left "
            "hand. I'll also make sure to keep a symptom "
            "journal to track the numbness and any other "
            "symptoms I'm experiencing. Thanks for the advice!")

# 00ca467f / answer_39900a0a_2 t10 [user] — PT since March 25th,
# Dr. Thompson, but NO visit marker
U_PT = ("I'm scheduled to start physical therapy sessions "
        "twice a week since March 25th to strengthen my leg "
        "muscles after my orthopedic surgeon, Dr. Thompson, "
        "cleared me to do so. I'm hoping it will help me "
        "recover from my torn ACL.")

# 00ca467f / answer_39900a0a_1 t6 [user] — March 15th and the
# doctors live in DIFFERENT sentences (sentence grain is
# load-bearing)
U_SPLIT = ("That's a great point. I'm also concerned about the "
           "numbness in my left hand, which I noticed around "
           "March 15th. Do you think it could be related to my "
           "bronchitis or is it a separate issue that I should "
           "discuss with Dr. Smith or maybe even my "
           "neurologist, Dr. Johnson?")

# synthetic probes / mechanism-not-hardcoding
S_GRAVEL_PLAN = ("I'm thinking of getting a new tire for my "
                 "gravel bike soon. It is time to replace it "
                 "this month, before April comes.")
S_GRAVEL_SVC = ("I just got my gravel bike serviced at the "
                "shop on March 5th and it feels brand new.")
S_TRACK_SVC = ("My track bike was serviced on April 2nd, so it "
               "is ready.")
S_PLURAL = ("I got both bikes serviced at the shop on March "
            "5th before the race.")
S_SEE_APRIL = ("I went to see Dr. Lee on April 5th for a "
               "checkup.")
S_SEE_MARCH = ("I went to see Dr. Lee on March 5th for a "
               "checkup.")
S_NO_DR = ("I had an appointment on March 5th and the doctor "
           "was great.")
S_APRIL_APPT = ("I had a routine appointment with Dr. Crane on "
                "April 2nd about my knee.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S_ROAD1 = mk(("answer_cc021f81_1", [("user", U_ROAD_SVC),
                                    ("assistant", "ok"),
                                    ("user", U_ROAD_SVC2)]))[0]
S_ROAD2 = mk(("answer_cc021f81_1", [("user", U_ROAD_SVC)]))[0]
S_PLAN = mk(("answer_cc021f81_2", [("user", U_COMM_PLAN)]))[0]
S_COPULA = mk(("answer_cc021f81_2", [("user", U_COPULA)]))[0]
S_MTN = mk(("answer_cc021f81_1", [("user", U_MTN_CAGE)]))[0]
S_CHAIN = mk(("answer_cc021f81_3", [("user", U_CHAIN),
                                    ("assistant", "ok"),
                                    ("user", U_CHAIN2)]))[0]
S_SHOPS = mk(("answer_cc021f81_3", [("user", U_SHOPS)]))[0]
S_ACC = mk(("answer_cc021f81_2", [("user", U_ACC)]))[0]
S_RACK = mk(("837f258b", [("user", U_RACK)]))[0]
FULL_SVC = [S_RACK, S_PLAN, S_CHAIN, mk(
    ("answer_cc021f81_1", [("user", U_MTN_CAGE),
                           ("assistant", "ok"),
                           ("user", U_ROAD_SVC),
                           ("assistant", "ok"),
                           ("user", U_ROAD_SVC2)]))[0]]

S_SMITH = mk(("answer_39900a0a_1", [("user", U_SMITH)]))[0]
S_THOMP = mk(("answer_39900a0a_3", [("user", U_THOMPSON)]))[0]
S_UNDATED = mk(("answer_39900a0a_2", [("user", U_UNDATED)]))[0]
S_PATEL = mk(("answer_39900a0a_3", [("user", U_PATEL)]))[0]
S_FUTURE = mk(("answer_39900a0a_1", [("user", U_FUTURE)]))[0]
S_PT = mk(("answer_39900a0a_2", [("user", U_PT)]))[0]
S_SPLIT = mk(("answer_39900a0a_1", [("user", U_SPLIT)]))[0]
FULL_APPT = [S_SMITH, S_UNDATED, S_PATEL, S_PT, S_SPLIT, mk(
    ("answer_39900a0a_3", [("user", U_THOMPSON),
                           ("assistant", "ok"),
                           ("user", U_FUTURE)]))[0]]


class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn('road bike serviced at Pedal Power on '
                      'March 10th', U_ROAD_SVC)
        self.assertIn('time to replace it this month, before '
                      'April comes', U_COMM_PLAN)
        self.assertIn('is just a regular hybrid bike', U_COPULA)
        self.assertIn('got a flat tire on my way to work on '
                      'February 20th', U_COPULA)
        self.assertIn('fit two bikes securely', U_RACK)
        self.assertIn('cleaned and lubricated the chain on '
                      'March 2nd', U_CHAIN)
        self.assertIn('cleaning and lubricating my bike chain '
                      'on March 22nd', U_CHAIN2)
        self.assertIn('bike shops or repair services', U_SHOPS)
        self.assertIn('got for my mountain bike a few weeks '
                      'ago', U_MTN_CAGE)
        self.assertIn('went to see my primary care physician, '
                      'Dr. Smith, on March 3rd', U_SMITH)
        self.assertIn('had a follow-up appointment with my '
                      'orthopedic surgeon, Dr. Thompson, on '
                      'March 20th', U_THOMPSON)
        self.assertIn('EMG test scheduled with my neurologist, '
                      'Dr. Johnson, on April 1st', U_UNDATED)
        self.assertIn('considering scheduling an appointment '
                      'with my gastroenterologist, Dr. Patel',
                      U_PATEL)
        self.assertIn("I'll schedule an appointment with Dr. "
                      "Smith and Dr. Johnson", U_FUTURE)
        self.assertIn('physical therapy sessions twice a week '
                      'since March 25th', U_PT)
        self.assertIn('I noticed around March 15th', U_SPLIT)
        self.assertIn('discuss with Dr. Smith or maybe even my '
                      'neurologist, Dr. Johnson?', U_SPLIT)


class TestFormClaim(unittest.TestCase):
    def test_head_claims_both_rows(self):
        self.assertEqual(counting_form(Q_SVC),
                         "bike_service_march")
        self.assertEqual(counting_form(Q_APPT), "march_appt")

    def test_no_steal_prior_cycle_rows(self):
        self.assertEqual(counting_form(Q_BIKES_OWN), "bikes_own")
        self.assertEqual(counting_form(Q_BIKES_CUR), "bikes_own")
        self.assertEqual(counting_form(Q_TRIPS), "cum_total")
        self.assertEqual(counting_form(Q_BAKE), "bake_two_weeks")
        self.assertEqual(counting_form(Q_MARVEL),
                         "marvel_rewatch")
        self.assertEqual(counting_form(Q_ANTIQUE),
                         "antique_inherit")
        self.assertEqual(counting_form(Q_FURN), "furniture_txn")

    def test_no_steal_march_and_bike_siblings(self):
        for q in (Q_FUNRUNS, Q_AIRLINE, Q_DAYS, Q_NEGRONI):
            self.assertNotEqual(counting_form(q),
                                "bike_service_march", q)
            self.assertNotEqual(counting_form(q), "march_appt", q)


class TestBikeServiceMarchFace(unittest.TestCase):
    def test_full_haystack_two(self):
        self.assertEqual(_cnt_bike_service_march(Q_SVC, FULL_SVC),
                         "2")
        self.assertEqual(answer_counting(Q_SVC, FULL_SVC),
                         ("2", {"form": "bike_service_march"}))

    def test_serviced_face_alone(self):
        self.assertEqual(_cnt_bike_service_march(Q_SVC, [S_ROAD2]),
                         "1")

    def test_serviced_remention_dedups(self):
        self.assertEqual(_cnt_bike_service_march(Q_SVC, [S_ROAD1]),
                         "1")

    def test_plan_face_alone(self):
        self.assertEqual(_cnt_bike_service_march(Q_SVC, [S_PLAN]),
                         "1")

    def test_both_faces_two(self):
        sess = mk(("sa", [("user", U_ROAD_SVC)]),
                  ("sb", [("user", U_COMM_PLAN)]))
        self.assertEqual(_cnt_bike_service_march(Q_SVC, sess),
                         "2")

    def test_synthetic_types_not_hardcoded(self):
        sess = mk(("sx", [("user", S_GRAVEL_PLAN)]))
        self.assertEqual(_cnt_bike_service_march(Q_SVC, sess),
                         "1")
        sess = mk(("sx", [("user", S_GRAVEL_SVC)]))
        self.assertEqual(_cnt_bike_service_march(Q_SVC, sess),
                         "1")

    def test_non_march_month_never_counts(self):
        sess = mk(("sx", [("user", S_TRACK_SVC)]))
        self.assertIsNone(_cnt_bike_service_march(Q_SVC, sess))


class TestBikeServiceMarchWalls(unittest.TestCase):
    def test_rack_two_bikes_never_keys(self):
        self.assertIsNone(_cnt_bike_service_march(Q_SVC, [S_RACK]))

    def test_plural_bikes_never_keys(self):
        sess = mk(("sx", [("user", S_PLURAL)]))
        self.assertIsNone(_cnt_bike_service_march(Q_SVC, sess))

    def test_mountain_cage_turn_never_keys(self):
        self.assertIsNone(_cnt_bike_service_march(Q_SVC, [S_MTN]))

    def test_chain_cleaning_not_service(self):
        self.assertIsNone(_cnt_bike_service_march(Q_SVC,
                                                  [S_CHAIN]))

    def test_copula_hybrid_turn_never_keys(self):
        # 'is just a regular hybrid bike' + flat-tire re-mention:
        # no March anchor in the turn, keys nothing
        self.assertIsNone(_cnt_bike_service_march(Q_SVC,
                                                  [S_COPULA]))

    def test_follower_compounds_never_key(self):
        for sess in (S_SHOPS, S_ACC):
            self.assertIsNone(_cnt_bike_service_march(Q_SVC,
                                                      [sess]))


class TestMarchApptFace(unittest.TestCase):
    def test_full_haystack_two(self):
        self.assertEqual(_cnt_march_appt(Q_APPT, FULL_APPT), "2")
        self.assertEqual(answer_counting(Q_APPT, FULL_APPT),
                         ("2", {"form": "march_appt"}))

    def test_each_evidence_sentence_alone(self):
        self.assertEqual(_cnt_march_appt(Q_APPT, [S_SMITH]), "1")
        self.assertEqual(_cnt_march_appt(Q_APPT, [S_THOMP]), "1")

    def test_synthetic_not_hardcoded(self):
        sess = mk(("sx", [("user", S_SEE_MARCH)]))
        self.assertEqual(_cnt_march_appt(Q_APPT, sess), "1")


class TestMarchApptWalls(unittest.TestCase):
    def test_undated_remention_and_april_emg(self):
        self.assertIsNone(_cnt_march_appt(Q_APPT, [S_UNDATED]))

    def test_considering_intent_never_counts(self):
        self.assertIsNone(_cnt_march_appt(Q_APPT, [S_PATEL]))

    def test_future_schedule_never_counts(self):
        self.assertIsNone(_cnt_march_appt(Q_APPT, [S_FUTURE]))

    def test_pt_without_visit_marker_never_counts(self):
        # March 25th + Dr. Thompson but 'cleared me', no
        # went/had-appointment marker
        self.assertIsNone(_cnt_march_appt(Q_APPT, [S_PT]))

    def test_sentence_grain_keeps_date_and_doctor_apart(self):
        # March 15th in one sentence, Dr. Smith/Johnson in the
        # next — turn grain would overcount to 3
        self.assertIsNone(_cnt_march_appt(Q_APPT, [S_SPLIT]))

    def test_april_never_counts(self):
        sess = mk(("sx", [("user", S_SEE_APRIL)]))
        self.assertIsNone(_cnt_march_appt(Q_APPT, sess))
        sess = mk(("sx", [("user", S_APRIL_APPT)]))
        self.assertIsNone(_cnt_march_appt(Q_APPT, sess))

    def test_no_doctor_key_never_counts(self):
        sess = mk(("sx", [("user", S_NO_DR)]))
        self.assertIsNone(_cnt_march_appt(Q_APPT, sess))


class TestJudge(unittest.TestCase):
    def test_counting_judge_numeric(self):
        self.assertTrue(counting_judge(Q_SVC, "2", "2"))
        self.assertTrue(counting_judge(Q_APPT, "2", "2"))
        self.assertFalse(counting_judge(Q_SVC, "2", "3"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
