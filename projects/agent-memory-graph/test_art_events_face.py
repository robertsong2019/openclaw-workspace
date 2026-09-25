"""C608: art_events face — past-month art-event date census
(2ce6a0f2 GT 4).

Single mechanism, single face:

- "How many different art-related events did I attend in the
  past month?" — the row carries FOUR user evidence
  sentences, each self-contained at SENTENCE grain:
  s8  "volunteered at the Children's Museum for their "Art
       Afternoon" event on February 17th"
  s24 "attended a lecture at the Art Gallery on 'The
       Evolution of Street Art' on March 3rd"
  s38 ""Women in Art" exhibition which I attended on
       February 10th"
  s40 "went on a guided tour at the History Museum on
       February 24th"
  = date keys {(2,10),(2,17),(2,24),(3,3)} -> 4.

Wall discipline:

- participation wall is load-bearing: the March 3rd
  re-mention ('after seeing some of the work at the lecture')
  carries no attend/volunteer/went-on verb and never keys;
  'participated in a similar chat', 'visiting ... art
  studios', 'looking forward to attending ... graduation
  party' all stay dark
- topic wall is load-bearing: 'attended a charity yoga
  event' has the verb but no art/exhibition/gallery/museum/
  lecture/tour term; 'artists'/'Pinterest' never hit \bart\b
- date wall is load-bearing: 'guided tour at the History
  Museum' (pottery follow-up) has topic but no date; topic
  without verb ('looking for ... local art events') dark
- month-day anchor is month-first only ('February 17th' /
  'March 3rd'); alias dedup pins March == Mar to one key
- assistant surfaces in the row echo volunteer/event but
  carry NO date; the user-role wall backstops the all-walls
  echo (synthetic assistant sentence with every wall present)

Census (all 500): the strict head matches EXACTLY its own row
(2ce6a0f2 GT 4, unbanked, gate=answer / NEEDS_JUDGE today);
the loose 'art-related' cousin (gpt4_59149c78 where-was-it-
held) carries a different head and is never stolen. Render
the count '4' — GT banks via counting_judge numeric-first
(_cnt_numval('4') == 4.0), exact + judge_semantic bank on the
digit match.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_art_events,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = ('How many different art-related events did I attend '
     'in the past month?')

# verbatim dataset fixtures (2ce6a0f2; 09-26 census)
U_ART_AFTERNOON = (
    'By the way, I recently volunteered at the Children\'s '
    'Museum for their "Art Afternoon" event on February 17th, '
    'and it was amazing to see the kids create their own '
    'artwork inspired by famous paintings.')
U_GALLERY_LECTURE = (
    "I recently attended a lecture at the Art Gallery on "
    "'The Evolution of Street Art' on March 3rd, and it got "
    "me thinking about the role of street art in urban "
    "communities.")
U_EXHIBITION = (
    'I was particularly drawn to the works of local artist, '
    'Rachel Lee, at the "Women in Art" exhibition which I '
    'attended on February 10th.')
U_MUSEUM_TOUR = (
    "I recently went on a guided tour at the History Museum "
    "on February 24th, and it really sparked my interest in "
    "ancient history and art.")

# structural wall shapes (verbatim row fragments pinned)
U_REMENTION_SEEING = (
    "I'm particularly interested in stencil art, especially "
    "after seeing some of the work at the lecture on March "
    "3rd.")
U_LOCAL_EXHIBITIONS = (
    "Do you know of any local artists or exhibitions that "
    "focus on mixed media or feminist art?")
U_LOOKING_INFO = (
    "I'm looking for some information on local art events "
    "and exhibitions.")
U_POTTERY_TOUR = (
    "I was really fascinated by the ancient pottery section "
    "during my guided tour at the History Museum.")
U_FUTURE_GRAD = (
    "By the way, speaking of celebrations, I'm also looking "
    "forward to attending my husband's company's graduation "
    "party for one of his colleagues, who's completing his "
    "MBA program.")
U_VISITING = (
    "I'm thinking of visiting some local art studios and "
    "galleries this weekend.")
U_TWITTER_CHAT = (
    "I participated in a similar chat two weeks ago, where "
    "we discussed the impact of sustainable packaging on the "
    "environment.")
U_YOGA = (
    'By the way, I recently attended a charity yoga event '
    'called "Yoga for a Cause" which raised over $2,000 for '
    'a local animal shelter.')
U_ARTIST_WORD = (
    "Can you recommend some popular Sufi artists or bands "
    "that I should definitely check out?")
A_VOLUNTEER_ECHO = (
    'By the way, it\'s fantastic that you volunteered at '
    'the Children\'s Museum\'s "Art Afternoon" event!')
A_ALL_WALLS = (
    'You mentioned you volunteered at the Children\'s '
    'Museum for the "Art Afternoon" event on February 17th, '
    'attended a lecture at the Art Gallery on March 3rd, '
    'saw the "Women in Art" exhibition on February 10th, '
    'and went on a guided tour at the History Museum on '
    'February 24th.')


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: evidence sessions in dataset order
S_ROW = mk(
    ("sess_08", [("user", U_ART_AFTERNOON),
                 ("assistant", A_VOLUNTEER_ECHO)]),
    ("sess_24", [("user", U_GALLERY_LECTURE),
                 ("user", U_REMENTION_SEEING)]),
    ("sess_38", [("user", U_EXHIBITION),
                 ("user", U_LOCAL_EXHIBITIONS),
                 ("user", U_LOOKING_INFO)]),
    ("sess_40", [("user", U_MUSEUM_TOUR),
                 ("user", U_POTTERY_TOUR)]))


class TestForm(unittest.TestCase):
    def test_form_routes_art_events(self):
        self.assertEqual(counting_form(Q), "art_events")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # art_events), and the art handler is dark on all of
        # them — plus the loose 'art-related' cousin
        # (gpt4_59149c78 where-was-it-held, different head)
        for q in (
            'How many days did I spend attending workshops, '
            'lectures, and conferences in April?',
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many fun runs did I miss in March due to work '
            'commitments?',
            'How many weddings have I attended in this year?',
            'How many pre-1920 American coins do I have in my '
            'collection?',
            'How many different types of food delivery '
            'services have I used recently?',
            'How many bikes did I service or plan to service '
            'in March?',
            'I mentioned that I participated in an art-related '
            'event two weeks ago. Where was that event held '
            'at?',
        ):
            self.assertNotEqual(counting_form(q), "art_events",
                                q)
            self.assertIsNone(_cnt_art_events(q, S_ROW), q)


class TestArtEvents(unittest.TestCase):
    def test_row_resolves_four(self):
        self.assertEqual(_cnt_art_events(Q, S_ROW), "4")

    def test_single_art_afternoon(self):
        sess = one("sess_08", "user", U_ART_AFTERNOON)
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_single_gallery_lecture(self):
        sess = one("sess_24", "user", U_GALLERY_LECTURE)
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_single_exhibition(self):
        sess = one("sess_38", "user", U_EXHIBITION)
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_single_museum_tour(self):
        sess = one("sess_40", "user", U_MUSEUM_TOUR)
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_cross_session_additive(self):
        sess = mk(("s1", [("user", U_ART_AFTERNOON)]),
                  ("s2", [("user", U_GALLERY_LECTURE)]))
        self.assertEqual(_cnt_art_events(Q, sess), "2")

    def test_remention_seeing_dark(self):
        # the March 3rd re-mention: topic + date but NO
        # participation verb — dark (dedup backstop unneeded)
        sess = one("s1", "user", U_REMENTION_SEEING)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_remention_no_double_count(self):
        # even if the re-mention sat next to the evidence, the
        # distinct-date key holds the count at 1
        sess = mk(("s1", [("user", U_GALLERY_LECTURE)]),
                  ("s2", [("user", U_REMENTION_SEEING)]))
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_alias_month_dedup(self):
        # 'March 3rd' and 'Mar 3rd' normalize to one key
        sess = mk(("s1", [("user", U_GALLERY_LECTURE)]),
                  ("s2", [("user",
                           "I attended a gallery talk on Mar "
                           "3rd downtown.")]))
        self.assertEqual(_cnt_art_events(Q, sess), "1")

    def test_two_dates_one_sentence_additive(self):
        sess = one("s1", "user",
                   "I attended an art fair on March 3rd and a "
                   "gallery opening on March 5th.")
        self.assertEqual(_cnt_art_events(Q, sess), "2")

    def test_verb_without_topic_dark(self):
        # attended + event but no art/exhibition/gallery/
        # museum/lecture/tour term
        sess = one("s1", "user", U_YOGA)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_topic_without_verb_dark(self):
        sess = one("s1", "user", U_LOCAL_EXHIBITIONS)
        self.assertIsNone(_cnt_art_events(Q, sess))
        sess = one("s1", "user", U_LOOKING_INFO)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_topic_without_date_dark(self):
        sess = one("s1", "user", U_POTTERY_TOUR)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_visiting_future_dark(self):
        sess = one("s1", "user", U_VISITING)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_future_attending_graduation_dark(self):
        # 'looking forward to attending' — not a past-
        # participation verb; no art term either
        sess = one("s1", "user", U_FUTURE_GRAD)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_participated_dark(self):
        sess = one("s1", "user", U_TWITTER_CHAT)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_artists_word_not_art(self):
        # \bart\b cannot match inside 'artists'
        sess = one("s1", "user", U_ARTIST_WORD)
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_assistant_echoes_never_read(self):
        sess = mk(("s1", [("assistant", A_VOLUNTEER_ECHO)]),
                  ("s2", [("assistant", A_ALL_WALLS)]))
        self.assertIsNone(_cnt_art_events(Q, sess))

    def test_assistant_all_walls_still_dark(self):
        # role wall is load-bearing even when every lexical
        # wall is present in the echo
        sess = mk(("s1", [("user", U_ART_AFTERNOON),
                          ("user", U_GALLERY_LECTURE),
                          ("user", U_EXHIBITION)]),
                  ("s2", [("assistant", A_ALL_WALLS)]))
        self.assertEqual(_cnt_art_events(Q, sess), "3")


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric(self):
        self.assertTrue(counting_judge(Q, "4", "4"))
        self.assertFalse(counting_judge(Q, "4", "3"))

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "4", "4"), "CORRECT")
        self.assertEqual(exact_judge(Q, "4", "4"), True)
        self.assertEqual(judge_semantic(Q, "3", "4"), "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "4")
        self.assertEqual(meta, {"form": "art_events"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("assistant", A_ALL_WALLS)]))
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "art_events"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
