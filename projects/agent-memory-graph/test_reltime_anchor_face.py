#!/usr/bin/env python3
"""C579 TDD miniatures: relative-time anchor face (verbatim
fixtures from longmemeval_s_cleaned haystack user lines).

Red-first: these fail until reltime_form / answer_reltime_anchor
exist and bind the five designed demands.
"""
import sys, unittest

sys.path.insert(0, "/root/.openclaw/workspace/projects/agent-memory-graph")
from amg_bench_quality import reltime_form, answer_reltime_anchor

# ── verbatim question texts (5 fire targets + 6 family no-fires) ──
Q_SMOKER = ("What kitchen appliance did I buy 10 days ago?")  # gpt4_8279ba03
Q_CAKE = ("I mentioned cooking something for my friend a couple of"
          " days ago. What was it?")                          # 9a707b82
Q_CHARITY = "What charity event did I participate in a month ago?"  # b46e15ee
Q_WEDDING = ("What was the the life event of one of my relatives"
             " that I participated in a week ago?")           # gpt4_4929293b
Q_ARTIST = "What is the artist that I started to listen to last Friday?"  # gpt4_fa19884d
# family members that must NOT enter the face
Q_CASHBACK = "How much cashback did I earn at SaveMart last Thursday?"
Q_BOOK = "Which book did I finish a week ago?"
Q_LUNCH = "Who did I meet with during the lunch last Tuesday?"
Q_SOCIAL = "What was the social media activity I participated 5 days ago?"
Q_JEWELRY = "I received a piece of jewelry last Saturday from whom?"
Q_MUSIC = "Who did I go with to the music event last Saturday?"

def dl(*pairs):
    """dated_lines in shipped shape: ('[role] text', 'YYYY-MM-DD')."""
    return list(pairs)

class TestReltimeForm(unittest.TestCase):
    def test_five_targets_enter(self):
        for q in (Q_SMOKER, Q_CAKE, Q_CHARITY, Q_WEDDING, Q_ARTIST):
            self.assertTrue(reltime_form(q), q)

    def test_family_nofires_stay_out(self):
        for q in (Q_CASHBACK, Q_BOOK, Q_LUNCH, Q_SOCIAL,
                  Q_JEWELRY, Q_MUSIC):
            self.assertFalse(reltime_form(q), q)

    def test_frame_without_offset_stays_out(self):
        self.assertFalse(reltime_form(
            "What kitchen appliance did I buy recently?"))
        self.assertFalse(reltime_form(
            "What charity event did I participate in?"))

class TestTargetResolution(unittest.TestCase):
    def test_days_offset(self):
        _, d = answer_reltime_anchor(Q_SMOKER, [], "2023-03-25")
        self.assertEqual(d["target"], "2023-03-15")

    def test_couple_of_days(self):
        _, d = answer_reltime_anchor(Q_CAKE, [], "2022-04-12")
        self.assertEqual(d["target"], "2022-04-10")

    def test_month_is_thirty_days(self):
        _, d = answer_reltime_anchor(Q_CHARITY, [], "2023-04-18")
        self.assertEqual(d["target"], "2023-03-19")

    def test_week_offset(self):
        _, d = answer_reltime_anchor(Q_WEDDING, [], "2023-06-22")
        self.assertEqual(d["target"], "2023-06-15")

    def test_last_friday(self):
        _, d = answer_reltime_anchor(Q_ARTIST, [], "2023-04-05")
        self.assertEqual(d["target"], "2023-03-31")

    def test_unparseable_question_date_falls(self):
        ans, d = answer_reltime_anchor(Q_SMOKER, [], "")
        self.assertIsNone(ans)

class TestRealizedCapture(unittest.TestCase):
    def test_smoker(self):
        ans, d = answer_reltime_anchor(
            Q_SMOKER,
            dl(("[user] I'm looking for some new BBQ sauce recipes to"
                " try out. I've been experimenting with making my own"
                " from scratch and I'm always looking to improve. By"
                " the way, I just got a smoker today and I'm excited"
                " to experiment with it.", "2023-03-15")),
            "2023-03-25")
        self.assertEqual(ans, "a smoker")

    def test_cake(self):
        ans, d = answer_reltime_anchor(
            Q_CAKE,
            dl(("[user] I'm excited to try making croissants again,"
                " and I think I'll also make some banana bread for the"
                " dinner party. I recently made a batch with walnuts,"
                " and it turned out amazing. By the way, I just baked"
                " a chocolate cake for my friend's birthday party last"
                " weekend that turned out amazing.", "2022-04-10")),
            "2022-04-12")
        self.assertEqual(ans, "a chocolate cake")

    def test_charity_render_matches_truth_shape(self):
        # adapter label form: quotes normalized to doubles
        ans, d = answer_reltime_anchor(
            Q_CHARITY,
            dl(("[user] Hey, I'm looking for some healthy snack ideas"
                " that are easy to prepare. I just did the \"Walk for"
                " Hunger\" charity event today with my colleagues from"
                " work, walking 5 kilometers to raise money for the"
                " local food bank.", "2023-03-19")),
            "2023-04-18")
        self.assertEqual(ans, 'the "Walk for Hunger" charity event')

    def test_charity_raw_single_quote_form(self):
        # raw dataset form: single quotes
        ans, d = answer_reltime_anchor(
            Q_CHARITY,
            dl(("[user] I just did the 'Walk for Hunger' charity event"
                " today with my colleagues.", "2023-03-19")),
            "2023-04-18")
        self.assertEqual(ans, "the 'Walk for Hunger' charity event")

    def test_wedding_multiple_mentions_collapse(self):
        ans, d = answer_reltime_anchor(
            Q_WEDDING,
            dl(("[user] I'm really enjoying looking at different"
                " venues and imagining how I can make the space feel"
                " intimate and special. I recently walked down the"
                " aisle as a bridesmaid at my cousin's wedding, and it"
                " got me thinking about my own plans.",
                "2023-06-15"),
               ("[user] I'm planning a baby gift for my friend Emma,"
                " who just had a baby girl named Charlotte. Do you"
                " have any gift ideas or recommendations for a newborn"
                " baby girl? By the way, I just got back from"
                " attending my cousin's wedding.", "2023-06-15")),
            "2023-06-22")
        self.assertEqual(ans, "my cousin's wedding")

    def test_artist_capture(self):
        ans, d = answer_reltime_anchor(
            Q_ARTIST,
            dl(("[user] I'm also thinking of exploring more genres of"
                " music and discovering new artists. I recently"
                " discovered a bluegrass band that features a banjo"
                " player and started enjoying their music today. I've"
                " been thinking about learning an instrument myself.",
                "2023-03-31")),
            "2023-04-05")
        self.assertEqual(ans,
                         "a bluegrass band that features a banjo player")

class TestGates(unittest.TestCase):
    def test_user_wall(self):
        ans, _ = answer_reltime_anchor(
            Q_SMOKER,
            dl(("[assistant] By the way, I just got a smoker today and"
                " I'm excited to experiment with it.", "2023-03-15")),
            "2023-03-25")
        self.assertIsNone(ans)

    def test_wrong_date_no_fire(self):
        ans, _ = answer_reltime_anchor(
            Q_SMOKER,
            dl(("[user] I just got a smoker today and I'm excited.",
                "2023-03-16")),
            "2023-03-25")
        self.assertIsNone(ans)

    def test_ambiguity_two_candidates_falls(self):
        ans, d = answer_reltime_anchor(
            Q_SMOKER,
            dl(("[user] I just got a smoker today and I'm excited.",
                "2023-03-15"),
               ("[user] I just got a waffle iron today, cannot wait.",
                "2023-03-15")),
            "2023-03-25")
        self.assertIsNone(ans)
        self.assertEqual(sorted(d.get("cands", [])),
                         ["a smoker", "a waffle iron"])

    def test_decoy_charity_lines_dont_bind(self):
        ans, _ = answer_reltime_anchor(
            Q_CHARITY,
            dl(("[user] I was thinking of organizing a charity bake"
                " sale at my office to raise money for the local animal"
                " shelter.", "2023-03-19"),
               ("[user] Thanks for these helpful tips! I'll definitely"
                " keep them in mind for my next charity walk.",
                "2023-03-19")),
            "2023-04-18")
        self.assertIsNone(ans)

if __name__ == "__main__":
    unittest.main(verbosity=2)
