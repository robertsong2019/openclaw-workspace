#!/usr/bin/env python3
"""C580 TDD miniatures: who-companion face (verbatim fixtures from
longmemeval_s_cleaned haystack user lines, session 1/11/17 of
gpt4_d6585ce9).

Red-first: these fail until who_companion_form / answer_who_companion
exist and bind the designed demand.
"""
import sys, unittest

sys.path.insert(0, "/root/.openclaw/workspace/projects/agent-memory-graph")
from amg_bench_quality import who_companion_form, answer_who_companion

# ── verbatim question texts (1 fire target + family no-fires) ──
Q_MUSIC = "Who did I go with to the music event last Saturday?"  # gpt4_d6585ce9
# family members that must NOT enter the face
Q_LUNCH = "Who did I meet with during the lunch last Tuesday?"   # banked via other route
Q_JEWELRY = "I received a piece of jewelry last Saturday from whom?"  # giver frame: evidence-absent, deliberately out
Q_SMOKER = "What kitchen appliance did I buy 10 days ago?"       # C579 reltime face
Q_WHO_NOFFSET = "Who did I go with to the cinema?"               # who-frame without offset

# ── verbatim user lines (byte-exact from the haystack) ──
# s17 m0 @2023-04-15 (the TARGET date): realized companion line —
# also carries the PERFORMER ("with Adam Lambert") that must never
# be captured
L_PARENTS = ("I'm looking for some recommendations for rock music"
             " playlists on streaming services. I've been listening"
             " to a lot of Queen lately, actually just saw them live"
             " with Adam Lambert at the Prudential Center in Newark,"
             " NJ with my parents, and I'm craving more of that"
             " classic rock sound.")
# s1 m0 @2023-03-18: wrong-date companion decoy
L_SISTER = ("I'm planning to buy some new concert merchandise"
            " online. Can you recommend some popular websites to find"
            " cool Billie Eilish gear? By the way, I just got back"
            " from an amazing Billie Eilish concert at the Wells"
            " Fargo Center in Philly with my sister today, and I'm"
            " still on a high from the experience!")
# s11 m0 @2023-04-01: the CHAIN'S CURRENT WRONG PRED source
L_GROUP = ("I'm looking for some song recommendations. I've been"
           " listening to a lot of indie music lately, especially"
           " since I just got back from a music festival in Brooklyn"
           " with a group of friends, featuring a lineup of my"
           " favorite indie bands. Can you suggest some new artists"
           " or bands I might like?")
# dataset wire shape (C577 lesson: adapters pass the RAW string)
QDATE_RAW = "2023/04/22 (Sat) 08:01"

def dl(*pairs):
    """dated_lines in shipped shape: ('[role] text', 'YYYY-MM-DD')."""
    return list(pairs)

class TestWhoCompanionForm(unittest.TestCase):
    def test_target_enters(self):
        self.assertTrue(who_companion_form(Q_MUSIC))

    def test_frame_variant_attend_enters(self):
        self.assertTrue(who_companion_form(
            "Who did I attend the game with last Monday?"))

    def test_family_nofires_stay_out(self):
        for q in (Q_LUNCH, Q_JEWELRY, Q_SMOKER, Q_WHO_NOFFSET):
            self.assertFalse(who_companion_form(q), q)

class TestTargetResolution(unittest.TestCase):
    def test_last_saturday(self):
        _, d = answer_who_companion(Q_MUSIC, [], "2023-04-22")
        self.assertEqual(d["target"], "2023-04-15")

    def test_raw_dataset_qdate_wire_shape(self):
        _, d = answer_who_companion(Q_MUSIC, [], QDATE_RAW)
        self.assertEqual(d["target"], "2023-04-15")

    def test_unparseable_question_date_falls(self):
        ans, _ = answer_who_companion(Q_MUSIC, [], "")
        self.assertIsNone(ans)

class TestRealizedCapture(unittest.TestCase):
    def test_parents_performer_not_captured(self):
        ans, d = answer_who_companion(
            Q_MUSIC,
            dl(("[user] " + L_PARENTS, "2023-04-15")),
            "2023-04-22")
        self.assertEqual(ans, "my parents")
        self.assertEqual(d["cands"], ["my parents"])

    def test_possessive_guard(self):
        # "my cousin's wedding" must not render a companion
        ans, d = answer_who_companion(
            Q_MUSIC,
            dl(("[user] I stood as bridesmaid at my cousin's wedding"
                " with my aunt chaperoning.", "2023-04-15")),
            "2023-04-22")
        self.assertEqual(ans, "my aunt")
        self.assertEqual(d["cands"], ["my aunt"])

    def test_real_session_structure_end_to_end(self):
        # s1@03-18 + s11@04-01 + s17@04-15 (the real item layout):
        # only the target-date companion binds
        ans, _ = answer_who_companion(
            Q_MUSIC,
            dl(("[user] " + L_SISTER, "2023-03-18"),
               ("[user] " + L_GROUP, "2023-04-01"),
               ("[user] " + L_PARENTS, "2023-04-15")),
            QDATE_RAW)
        self.assertEqual(ans, "my parents")

class TestGates(unittest.TestCase):
    def test_user_wall(self):
        ans, _ = answer_who_companion(
            Q_MUSIC,
            dl(("[assistant] I just saw them live with my parents.",
                "2023-04-15")),
            "2023-04-22")
        self.assertIsNone(ans)

    def test_wrong_date_no_fire(self):
        # sister line lives on 03-18, group line on 04-01 — neither
        # is last Saturday of 04-22
        for line, sdate in ((L_SISTER, "2023-03-18"),
                            (L_GROUP, "2023-04-01")):
            ans, _ = answer_who_companion(
                Q_MUSIC,
                dl(("[user] " + line, sdate)),
                "2023-04-22")
            self.assertIsNone(ans)

    def test_ambiguity_two_companions_falls(self):
        ans, d = answer_who_companion(
            Q_MUSIC,
            dl(("[user] " + L_PARENTS, "2023-04-15"),
               ("[user] I just got back from a concert with my"
                " sister.", "2023-04-15")),
            "2023-04-22")
        self.assertIsNone(ans)
        self.assertEqual(sorted(d.get("cands", [])),
                         ["my parents", "my sister"])

    def test_no_companion_on_target_date_falls(self):
        ans, _ = answer_who_companion(
            Q_MUSIC,
            dl(("[user] I've been listening to a lot of Queen"
                " lately.", "2023-04-15")),
            "2023-04-22")
        self.assertIsNone(ans)

if __name__ == "__main__":
    unittest.main(verbosity=2)
