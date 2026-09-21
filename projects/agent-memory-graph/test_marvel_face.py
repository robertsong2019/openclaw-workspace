"""C596: marvel re-watch count face — 681a1674 (GT '2').

Head: "How many Marvel movies did I re-watch?" — census (all
500) matches EXACTLY 1 row, unbanked (gate=answer / parasitic
session echo pred today). No time window — the RE-WATCH marker
replaces it (C593 pattern: the constraint replaces the window).

Evidence (verbatim user turns):
- s6 t4:  "Since I just re-watched Avengers: Endgame yesterday…"
- s6 t10: "Since I re-watched Avengers: Endgame, which is a
  Marvel movie…" (same film, second mention → dedup)
- s34 t0: "I also re-watched Spider-Man: No Way Home, which is
  another Marvel movie."
→ distinct titles {Avengers: Endgame, Spider-Man: No Way Home}
  = 2 = GT.

Mechanism: user-role sentences carrying a ``re-watch`` marker
yield a title key extracted from the capitalized title span
right after the marker (colon/hyphen aware, stops at lowercase);
distinct keys render word-form ('two' banks via judge_semantic
norm fold onto GT '2' — C595 'four'/'4' discipline).

Guards pinned here:
- watched-without-re marker never counts (Doctor Strange / 'four
  Marvel movies I watched' decoy)
- title-without-marker sentence never counts (s6 t10 first
  sentence mentions Endgame but no re-watch)
- assistant restatements never render (user wall)
- marker without a title span falls through (unresolvable)
- mechanism, not hardcoding: a synthetic third title moves
  two→three; re-mention of the same title dedups
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_marvel_rewatch,
    _sem_norm,
    answer_counting,
    counting_form,
    judge_semantic,
)

Q_MARVEL = 'How many Marvel movies did I re-watch?'
Q_WATCHED = 'How many Marvel movies have I watched?'
Q_TIMES = 'How many times did I re-watch Avengers: Endgame?'
Q_WHICH = 'Which Marvel movie did I re-watch most recently?'
Q_BIKES = 'How many bikes do I own?'
Q_PLANTS = 'How many plants did I acquire in the last month?'
Q_ANTIQUE = ('How many antique items did I inherit or acquire '
             'from my family members?')
Q_FURN = ('How many pieces of furniture did I buy, assemble, '
          'sell, or fix in the past few months?')

# ── verbatim dataset turns (681a1674 haystack, extracted by
#    /tmp/c596/gen_fixture.py; drift pins assert the surfaces
#    survive transcription) ──

# s6 t2 [user] — the watched-not-rewatched decoy
U_WATCHED_4 = ("I've actually watched Doctor Strange already, it "
               "was one of the four Marvel movies I watched "
               "recently. I'm more interested in non-Marvel "
               "movies similar to Avengers: Endgame. Can you "
               "recommend some sci-fi or action movies that have "
               "a similar scale and scope?")

# s6 t4 [user] — re-watch #1
U_RW_END_1 = ("Since I just re-watched Avengers: Endgame "
              "yesterday, I've been thinking about other movies "
              "that might have a similar sense of scale and "
              "action. Have you got any recommendations for "
              "sci-fi or action movies that are not part of the "
              "Marvel Cinematic Universe, but still offer a "
              "similar sense of grandeur and epic battles?")

# s6 t10 [user] — title-without-marker decoy sentence + re-watch
# #2 (same film → dedup)
U_RW_END_2 = ("I've been thinking about other movies that might "
              "have a similar sense of scale and action to "
              "Avengers: Endgame. Since I re-watched Avengers: "
              "Endgame, which is a Marvel movie, I've been "
              "exploring more sci-fi and action movies with a "
              "similar sense of grandeur and epic battles.")

# s34 t0 [user] — re-watch #3 (different film)
U_RW_NWH = ("I'm trying to find some new movies to watch. I've "
            "been into Marvel movies lately, I also re-watched "
            "Spider-Man: No Way Home, which is another Marvel "
            "movie. Can you recommend some other superhero films "
            "that aren't from the Marvel universe?")

# sentence-level decoys
D_MARKER_NO_TITLE = ("I re-watched it last weekend and loved "
                     "every minute of it.")
A_ECHO = ("Since you re-watched Avengers: Endgame yesterday, you "
          "might enjoy similar epic conclusions.")

# synthetic third-title sentence (mechanism probe)
U_RW_THOR = ("Last night I re-watched Thor: Ragnarok and it still "
             "holds up.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S6 = mk(("s6", [("user", U_WATCHED_4), ("assistant", "ok"),
                ("user", U_RW_END_1), ("assistant", "ok"),
                ("user", U_RW_END_2)]))[0]
S34 = mk(("s34", [("user", U_RW_NWH), ("assistant", "ok")]))[0]
FULL = [S6, S34]


class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn('one of the four Marvel movies I watched',
                      U_WATCHED_4)
        self.assertIn('just re-watched Avengers: Endgame yesterday',
                      U_RW_END_1)
        self.assertIn('Since I re-watched Avengers: Endgame, which '
                      'is a Marvel movie', U_RW_END_2)
        self.assertIn('re-watched Spider-Man: No Way Home, which is '
                      'another Marvel movie', U_RW_NWH)


class TestFormClaim(unittest.TestCase):
    def test_head_claims_marvel_rewatch(self):
        self.assertEqual(counting_form(Q_MARVEL), "marvel_rewatch")

    def test_no_steal_prior_cycle_rows(self):
        self.assertEqual(counting_form(Q_BIKES), "bikes_own")
        self.assertEqual(counting_form(Q_PLANTS), "acquire")
        self.assertEqual(counting_form(Q_ANTIQUE), "antique_inherit")
        self.assertEqual(counting_form(Q_FURN), "furniture_txn")

    def test_no_steal_siblings(self):
        for q in (Q_WATCHED, Q_TIMES, Q_WHICH):
            self.assertNotEqual(counting_form(q), "marvel_rewatch",
                                q)


class TestFace(unittest.TestCase):
    def test_full_haystack_two(self):
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, FULL), "two")
        self.assertEqual(
            answer_counting(Q_MARVEL, FULL),
            ("two", {"form": "marvel_rewatch"}))

    def test_endgame_alone_one(self):
        sess = mk(("sx", [("user", U_RW_END_1)]))
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, sess), "one")

    def test_nwh_alone_one(self):
        sess = mk(("sx", [("user", U_RW_NWH)]))
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, sess), "one")

    def test_title_without_marker_not_counted(self):
        # first sentence of U_RW_END_2 mentions Endgame, no marker
        sess = mk(("sx", [("user", "I've been thinking about other "
                                 "movies that might have a similar "
                                 "sense of scale and action to "
                                 "Avengers: Endgame.")]))
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, sess))


class TestDecoyWalls(unittest.TestCase):
    def test_watched_without_re_never_counts(self):
        sess = mk(("sx", [("user", U_WATCHED_4)]))
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, sess))

    def test_marker_without_title_falls_through(self):
        sess = mk(("sx", [("user", D_MARKER_NO_TITLE)]))
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, sess))

    def test_assistant_wall(self):
        wall = mk(("w", [("assistant", A_ECHO)]))[0]
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, [wall]))
        # wall adds nothing to the real haystack (endgame+endgame
        # in S6 → 'one'; the second title lives in S34)
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, [S6, wall]),
                         "one")
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL,
                                             [S6, S34, wall]),
                         "two")


class TestMechanismNotHardcoding(unittest.TestCase):
    def test_third_title_moves_two_to_three(self):
        sess = mk(("s6", [("user", U_WATCHED_4),
                          ("user", U_RW_END_1),
                          ("user", U_RW_END_2)]),
                  ("s34", [("user", U_RW_NWH),
                           ("user", U_RW_THOR)]))
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, sess),
                         "three")

    def test_same_title_remention_dedups(self):
        sess = mk(("sx", [("user", U_RW_END_1),
                          ("user", "Honestly I re-watched Avengers: "
                                   "Endgame again last weekend.")]))
        self.assertEqual(_cnt_marvel_rewatch(Q_MARVEL, sess), "one")

    def test_unresolvable_falls_through(self):
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, []))
        bare = mk(("sx", [("user", "Marvel movies are great!")]))
        self.assertIsNone(_cnt_marvel_rewatch(Q_MARVEL, bare))


class TestRenderAndBank(unittest.TestCase):
    def test_word_render_banks_on_gt_2(self):
        # GT '2' — judge_semantic norm fold (C595 'four'/'4' path)
        self.assertEqual(judge_semantic(Q_MARVEL, "2", "two"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_MARVEL, "2", "three"),
                         "WRONG")
        self.assertEqual(judge_semantic(Q_MARVEL, "2", "four"),
                         "WRONG")
        self.assertEqual(_sem_norm("two"), _sem_norm("2"))


if __name__ == "__main__":
    unittest.main()
