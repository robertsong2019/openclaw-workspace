"""C598: self-stated cumulative-total face — 26bdc477 / 618f13b2.

Head: "How many trips have I taken …?" / "How many times have I
worn …?" — census (all 500) matches EXACTLY 2 rows, both
unbanked (gate=answer / session echo today):
- 26bdc477 (GT 'five'): "…I've had my Canon EOS 80D with me on
  five trips now, and it's been a beast!"
- 618f13b2 (GT 'six'):  "…I just wore my new black Converse to
  run some errands yesterday, so that's six times now that I've
  worn them."

Mechanism: the answer is the user's OWN stated running total
(the "<num> <trips|times> now" construction), not a counted key
set (C595/C596/C597 pattern). Same-sentence discipline (C591+):
the total construction must share its sentence with the topic
NP (camera terms for trips; Converse/sneaker terms for worn).

Decoy discipline (the whole game):
- enumerations without the 'now' anchor are mentions, never
  totals ("three trips to Yellowstone, Yosemite, and the Grand
  Canyon" must NOT produce 3 — GT is the stated 5)
- totals in topic-less sentences never count (cross-face wall)
- assistant restatements never render (user wall)
- conflicting distinct totals abstain (None) — the 603deb26
  Negroni 5-v-10 trap stays out by the head's taken|worn verbs;
  the conflict rule keeps future siblings honest
- identical repeated totals dedup to the one value

Render: the captured token as stated ('five'/'six' bank
numeric-first via counting_judge; digits pass through).
Guards pinned here: census claims + no-steal (bake/marvel/
bikes/Negroni/rollercoaster/metup/Chiefs + bake _abs sibling),
mechanism-not-hardcoding (synthetic digit total '7'), walls.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_cum_total,
    answer_counting,
    counting_form,
    counting_judge,
    judge_semantic,
)

Q_TRIPS = 'How many trips have I taken my Canon EOS 80D camera on?'
Q_WEAR = ('How many times have I worn my new black Converse '
          'Chuck Taylor All Star sneakers?')
Q_BAKE = 'How many times did I bake something in the past two weeks?'
Q_MARVEL = 'How many Marvel movies did I re-watch?'
Q_BIKES = 'How many bikes do I own?'
Q_NEGRONI = ('How many times have I tried making a Negroni at '
             'home since my friend Emma showed me how to make it?')
Q_ROLLER = ('How many times did I ride rollercoasters across all '
            'the events I attended from July to October?')
Q_METUP = 'How many times have I met up with Alex from Germany?'
Q_CHIEFS = ('I was looking back at our previous chat and I wanted '
            'to confirm, how many times did the Chiefs play the '
            'Jaguars at Arrowhead Stadium?')
Q_BAKE_ABS = 'How many times did I bake egg tarts in the past two weeks?'

# ── verbatim dataset turns ──

# 26bdc477 / answer_f762ad8d_2 t0 [user] — THE total ('five')
U_ZION = ("I'm planning a trip to Zion National Park and want to "
          "capture some great landscape shots. Can you recommend "
          "any tips for shooting in bright sunlight and high "
          "contrast environments? By the way, I've had my Canon "
          "EOS 80D with me on five trips now, and it's been a "
          "beast!")

# 26bdc477 / answer_f762ad8d_1 t0 [user] — enumeration decoy
# ('three trips to X, Y, Z' — NO 'now' anchor, camera topic)
U_ENUM = ("I'm actually considering the Really Right Stuff "
          "tripod. I've heard great things about it. Do you know "
          "if it's compatible with my Canon EOS 80D camera? By "
          "the way, I've taken my camera on quite a few "
          "adventures, including three trips to Yellowstone, "
          "Yosemite, and the Grand Canyon, and I'm excited to "
          "take it on many more with a new tripod!")

# 618f13b2 / answer_caf5b52e_2 t0 [user] — THE total ('six')
U_COBBLE = ("I need help finding a good cobbler to fix my brown "
            "leather boots. Do you have any recommendations? "
            "Also, I was thinking of getting a shoe cleaning kit "
            "to make cleaning my shoes easier, do you have any "
            "suggestions? By the way, I just wore my new black "
            "Converse to run some errands yesterday, so that's "
            "six times now that I've worn them.")

# 618f13b2 / answer_caf5b52e_2 t2 [user] — Converse mention,
# no total
U_SPRAY = ("I'll check out those cobbler options and shoe "
           "cleaning kits. By the way, do you think I should get "
           "a waterproofing spray for my new Converse to protect "
           "them from mud and rain?")

# 618f13b2 / answer_caf5b52e_2 t4 [user] — sneaker topic,
# no total
U_VANS = ("That's a great idea! I think I'll get a leather shoe "
          "cleaning kit to keep my brown leather boots looking "
          "their best. By the way, I was thinking of getting a "
          "new pair of Vans Old Skool sneakers. Do you think "
          "they're comfortable and worth the investment?")

# synthetic probes / walls
A_ECHO = ("You've had your Canon EOS 80D on five trips now — a "
          "beast indeed!")
P_DIGIT = ("Honestly, I've taken my Canon EOS 80D on 7 trips "
           "now and it keeps going strong.")
D_XTOPIC_TIMES = "I've been to the gym four times now."
D_XTOPIC_TRIPS = "I've taken my camera on six trips now."
P_REPEAT_FIVE = ("We took the camera everywhere — five trips "
                 "now, like I said.")
D_CONFLICT = ("I've taken my Canon EOS 80D on seven trips now.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S_CAM1 = mk(("answer_f762ad8d_1", [("user", U_ENUM),
                                   ("assistant", "ok")]))[0]
S_CAM2 = mk(("answer_f762ad8d_2", [("user", U_ZION),
                                   ("assistant", "ok")]))[0]
S_SHOE1 = mk(("answer_caf5b52e_1", [("user", U_SPRAY),
                                    ("assistant", "ok")]))[0]
S_SHOE2 = mk(("answer_caf5b52e_2", [("user", U_COBBLE),
                                    ("assistant", "ok"),
                                    ("user", U_VANS)]))[0]
FULL_TRIPS = [S_CAM1, S_CAM2]
FULL_WEAR = [S_SHOE1, S_SHOE2]


class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn('on five trips now', U_ZION)
        self.assertIn('three trips to Yellowstone, Yosemite, and '
                      'the Grand Canyon', U_ENUM)
        self.assertIn("that's six times now that I've worn them",
                      U_COBBLE)
        self.assertIn('waterproofing spray for my new Converse',
                      U_SPRAY)
        self.assertIn('Vans Old Skool sneakers', U_VANS)


class TestFormClaim(unittest.TestCase):
    def test_head_claims_both_rows(self):
        self.assertEqual(counting_form(Q_TRIPS), "cum_total")
        self.assertEqual(counting_form(Q_WEAR), "cum_total")

    def test_no_steal_prior_cycle_rows(self):
        self.assertEqual(counting_form(Q_BAKE), "bake_two_weeks")
        self.assertEqual(counting_form(Q_MARVEL), "marvel_rewatch")
        self.assertEqual(counting_form(Q_BIKES), "bikes_own")

    def test_no_steal_siblings(self):
        for q in (Q_NEGRONI, Q_ROLLER, Q_METUP, Q_CHIEFS,
                  Q_BAKE_ABS):
            self.assertNotEqual(counting_form(q), "cum_total", q)


class TestFace(unittest.TestCase):
    def test_full_haystack_five_and_six(self):
        self.assertEqual(_cnt_cum_total(Q_TRIPS, FULL_TRIPS),
                         "five")
        self.assertEqual(_cnt_cum_total(Q_WEAR, FULL_WEAR), "six")
        self.assertEqual(answer_counting(Q_TRIPS, FULL_TRIPS),
                         ("five", {"form": "cum_total"}))
        self.assertEqual(answer_counting(Q_WEAR, FULL_WEAR),
                         ("six", {"form": "cum_total"}))

    def test_evidence_turn_alone(self):
        sess = mk(("sx", [("user", U_ZION)]))
        self.assertEqual(_cnt_cum_total(Q_TRIPS, sess), "five")
        sess = mk(("sx", [("user", U_COBBLE)]))
        self.assertEqual(_cnt_cum_total(Q_WEAR, sess), "six")


class TestDecoyWalls(unittest.TestCase):
    def test_enumeration_never_counts(self):
        # 'three trips to X, Y, Z' — no 'now' anchor: mention,
        # not total. GT 'five' must survive the full haystack.
        sess = mk(("sx", [("user", U_ENUM)]))
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, sess))

    def test_topicless_totals_never_count(self):
        sess = mk(("sx", [("user", D_XTOPIC_TIMES)]))
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, sess))
        sess = mk(("sx", [("user", D_XTOPIC_TRIPS)]))
        self.assertIsNone(_cnt_cum_total(Q_WEAR, sess))

    def test_assistant_wall(self):
        wall = mk(("w", [("assistant", A_ECHO)]))[0]
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, [wall]))
        # wall adds nothing to the real haystack
        self.assertEqual(_cnt_cum_total(Q_TRIPS,
                                        FULL_TRIPS + [wall]),
                         "five")

    def test_no_total_falls_through(self):
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, []))
        bare = mk(("sx", [("user", "Cameras are so much fun!")]))
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, bare))


class TestConflictAndRepeat(unittest.TestCase):
    def test_conflicting_totals_abstain(self):
        sess = mk(("sx", [("user", U_ZION),
                          ("user", D_CONFLICT)]))
        self.assertIsNone(_cnt_cum_total(Q_TRIPS, sess))

    def test_identical_repeat_dedups(self):
        sess = mk(("sx", [("user", U_ZION),
                          ("user", P_REPEAT_FIVE)]))
        self.assertEqual(_cnt_cum_total(Q_TRIPS, sess), "five")


class TestMechanismNotHardcoding(unittest.TestCase):
    def test_digit_total_passes_through(self):
        sess = mk(("sx", [("user", P_DIGIT)]))
        self.assertEqual(_cnt_cum_total(Q_TRIPS, sess), "7")

    def test_head_grain(self):
        # only the taken|worn heads claim; other verbs untouched
        self.assertIsNone(_cnt_cum_total(Q_NEGRONI, []))


class TestRenderAndBank(unittest.TestCase):
    def test_word_render_banks_numeric_first(self):
        # GT 'five' / 'six' bare words — counting_judge is
        # numeric-first; judge_semantic norm-folds words onto
        # words (C593 'five (5)' discipline)
        self.assertTrue(counting_judge(Q_TRIPS, "five", "five"))
        self.assertTrue(counting_judge(Q_WEAR, "six", "six"))
        self.assertTrue(counting_judge(Q_TRIPS, "five", "5"))
        self.assertEqual(judge_semantic(Q_TRIPS, "five", "five"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_WEAR, "six", "six"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_TRIPS, "five", "four"),
                         "WRONG")
        self.assertEqual(judge_semantic(Q_WEAR, "six", "seven"),
                         "WRONG")


if __name__ == "__main__":
    unittest.main()
