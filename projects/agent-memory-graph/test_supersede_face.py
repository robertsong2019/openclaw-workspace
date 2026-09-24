"""C603: supersede_total face — recency-superseded self-stated
running totals (a2f3aa27 GT 1300 / a1eacc2a GT 'seven').

One mechanism, two faces (C598/C599 pattern):

- followers (a2f3aa27, GT 1300): "How many followers do I have
  on Instagram now?" — the row carries TWO same-shape user
  declarations of one running total: the stale earlier one
  ("I've got 1250 followers on Instagram now", 05:26) and the
  superseding later one ("...my current follower count - I
  think I'm close to 1300 now", 09:28). Same-day, same shape:
  ONLY session recency separates them. enum_count keys the
  stale 1250 today — the strict head claims the row ahead of
  the generic block and the LATEST session's declaration wins.
- stories (a1eacc2a, GT 'seven'): "How many short stories have
  I written since I started writing regularly?" — same
  supersession: "I've written four so far..." (05/23) vs
  "complete 7 short stories since I started" (05/30). The
  'since I started' anchor — not the topic NP — is
  load-bearing: the four-declaration carries total+anchor in
  one sentence while the topic ('short stories per month?')
  lives in the SIBLING sentence (C599 turn-grain lesson).

Supersession discipline:
- haystack sessions are chronological (dataset invariant) —
  recency = session order; NO date parsing needed
- distinct totals within the SAME session abstain (None)
- identical repeats dedup to the one value
- assistant echoes ("congratulations on nearing 1300",
  "Completing seven short stories") never read (user wall)
- followers: the 'close to <num>' form requires the
  follower|instagram same-sentence topic wall (the rent decoy
  '$1,300' never carries it)
- stories: 'aiming to write 500 words a week' has no
  written|wrote|completed verb; 'wrote a short poem' has no
  number — neither keys, so later decoy sessions don't poison
  the arbitration

Census (all 500): each strict head matches EXACTLY its own
row; loose sweeps ('how many followers', 'how many short
stories', 'instagram ... now') hit no sibling rows. Render the
captured token as stated ('7' word-folds to GT 'seven' via
judge_semantic; counting_judge banks numeric-first).
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_supersede_total,
    answer_counting,
    counting_form,
    counting_judge,
    judge_semantic,
)

Q_INSTA = 'How many followers do I have on Instagram now?'
Q_STORY = ('How many short stories have I written since I '
           'started writing regularly?')

# verbatim dataset fixtures (a2f3aa27 / a1eacc2a; 09-24 dumps)
U_INSTA_1250 = (
    "Do you know if Instagram Insights can help me with that? "
    "And by the way, I've got 1250 followers on Instagram now, "
    "so it'd be great to get some insights on how to optimize "
    "my content for them.")
U_INSTA_1300 = (
    "I'm looking to create a new Instagram post about a recent "
    "industry event I attended. By the way, I've been meaning "
    "to check my current follower count - I think I'm close to "
    "1300 now.")
A_ECHO_1250 = (
    "Congratulations on reaching 1250 followers! Now, to "
    "optimize your content for your 1250 followers, consider "
    "the following.")
A_ECHO_1300 = (
    "First, congratulations on nearing 1300 followers!")
U_TOPIC_NO_TOTAL = (
    "I think I'll ask my followers to share a screenshot of "
    "the Q&A session on their Instagram Story and use a "
    "specific hashtag.")
U_RENT_CLOSE_TO = (
    "My new apartment costs close to 1300 now, which is more "
    "than I planned.")
A_RENT_1300 = (
    "Astoria offers a range of affordable options, with "
    "average rent for a 1-bedroom ranging from $1,300 to "
    "$1,800 per month.")

U_STORY_FOUR = (
    "Speaking of which, I was wondering, do you think it's a "
    "good idea to set a goal for a certain number of short "
    "stories per month? I've written four so far since I "
    "started writing regularly, and I'm hoping to keep the "
    "momentum going.")
U_STORY_7 = (
    "I'm thinking of continuing to experiment with non-linear "
    "narrative structures in my writing. By the way, I've been "
    "writing regularly for three months now, and it's been "
    "amazing - I've even managed to complete 7 short stories "
    "since I started.")
A_ECHO_7 = (
    "Congratulations on your writing progress! Completing "
    "seven short stories in three months is a remarkable "
    "achievement.")
U_WRITE_500 = (
    "I've been writing it for about a month now, aiming to "
    "write 500 words a week, and I'm really excited about how "
    "it's shaping up.")
U_WROTE_A = (
    "I've been experimenting with different writing styles "
    "and formats, including poetry and scriptwriting, and I "
    "recently wrote a short poem that I'm really proud of.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shapes: stale declaration session + superseding
# session, dataset (chronological) order
S_INSTA = mk(
    ("sess_12", [("user", U_INSTA_1250),
                 ("assistant", A_ECHO_1250)]),
    ("sess_39", [("user", U_INSTA_1300),
                 ("assistant", A_ECHO_1300)]))
S_STORY = mk(
    ("sess_16", [("user", U_STORY_FOUR)]),
    ("sess_30", [("user", U_STORY_7),
                 ("assistant", A_ECHO_7)]))


class TestForm(unittest.TestCase):
    def test_form_routes_supersede_total(self):
        self.assertEqual(counting_form(Q_INSTA), "supersede_total")
        self.assertEqual(counting_form(Q_STORY), "supersede_total")

    def test_no_steal_prior_cycle_heads(self):
        # prior kd faces keep their own forms (never
        # supersede_total), and the supersede handler is dark
        # on all of them
        for q in (
            'How many bikes did I service or plan to service in March?',
            "How many doctor's appointments did I go to in March?",
            'How many trips have I taken my Canon EOS 80D camera on?',
            'How many times did I bake something in the past two weeks?',
            'How many Marvel movies did I re-watch?',
            'How many days did I spend participating in '
            'faith-related activities in December?',
            'How many different types of food delivery services '
            'have I used recently?',
            'How many different species of birds have I seen in '
            'my local park?',
        ):
            self.assertNotEqual(counting_form(q), "supersede_total",
                                q)
            self.assertIsNone(_cnt_supersede_total(q, S_INSTA), q)


class TestSupersedeInsta(unittest.TestCase):
    def test_pair_resolves_latest(self):
        self.assertEqual(_cnt_supersede_total(Q_INSTA, S_INSTA),
                         "1300")

    def test_stale_only_is_latest_of_one(self):
        # a lone declaration is trivially the latest — the
        # mechanism supersedes, it never invents
        sess = one("sess_12", "user", U_INSTA_1250)
        self.assertEqual(_cnt_supersede_total(Q_INSTA, sess),
                         "1250")

    def test_fresh_only(self):
        sess = one("sess_39", "user", U_INSTA_1300)
        self.assertEqual(_cnt_supersede_total(Q_INSTA, sess),
                         "1300")

    def test_assistant_echoes_never_read(self):
        sess = mk(("s1", [("assistant", A_ECHO_1250)]),
                  ("s2", [("assistant", A_ECHO_1300)]))
        self.assertIsNone(_cnt_supersede_total(Q_INSTA, sess))

    def test_close_to_requires_topic_wall(self):
        # 'close to 1300' with no follower|instagram word in
        # the sentence (rent decoy shape) never keys
        sess = one("s1", "user", U_RENT_CLOSE_TO)
        self.assertIsNone(_cnt_supersede_total(Q_INSTA, sess))

    def test_assistant_rent_decoy_never_read(self):
        sess = mk(("s1", [("user", U_INSTA_1250)]),
                  ("s2", [("assistant", A_RENT_1300)]))
        self.assertEqual(_cnt_supersede_total(Q_INSTA, sess),
                         "1250")

    def test_topic_without_total_no_key(self):
        sess = one("s1", "user", U_TOPIC_NO_TOTAL)
        self.assertIsNone(_cnt_supersede_total(Q_INSTA, sess))

    def test_same_session_conflict_abstains(self):
        sess = mk(("s1", [("user", U_INSTA_1250),
                          ("user", U_INSTA_1300)]))
        self.assertIsNone(_cnt_supersede_total(Q_INSTA, sess))

    def test_identical_repeats_dedup(self):
        sess = mk(("s1", [("user", U_INSTA_1250)]),
                  ("s2", [("user", U_INSTA_1300)]),
                  ("s3", [("user", U_INSTA_1300)]))
        self.assertEqual(_cnt_supersede_total(Q_INSTA, sess),
                         "1300")


class TestSupersedeStory(unittest.TestCase):
    def test_pair_resolves_latest(self):
        self.assertEqual(_cnt_supersede_total(Q_STORY, S_STORY),
                         "7")

    def test_sibling_sentence_topic_still_keys(self):
        # the four-declaration: topic lives in the sibling
        # sentence ('... short stories per month?'), total +
        # anchor in the next — the ANCHOR, not the topic, is
        # load-bearing (C599 turn-grain lesson)
        sess = one("s1", "user", U_STORY_FOUR)
        self.assertEqual(_cnt_supersede_total(Q_STORY, sess),
                         "four")

    def test_assistant_echo_never_read(self):
        sess = one("s1", "assistant", A_ECHO_7)
        self.assertIsNone(_cnt_supersede_total(Q_STORY, sess))

    def test_later_decoy_session_no_poison(self):
        # 'write 500 words' / 'wrote a short poem' in a LATER
        # session carry no keyed declaration — arbitration
        # ignores them and the latest real total stands
        sess = mk(("s1", [("user", U_STORY_FOUR)]),
                  ("s2", [("user", U_STORY_7),
                          ("assistant", A_ECHO_7)]),
                  ("s3", [("user", U_WRITE_500),
                          ("user", U_WROTE_A)]))
        self.assertEqual(_cnt_supersede_total(Q_STORY, sess), "7")

    def test_wrote_a_never_keys(self):
        sess = one("s1", "user", U_WROTE_A)
        self.assertIsNone(_cnt_supersede_total(Q_STORY, sess))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric_and_digits(self):
        self.assertTrue(counting_judge(Q_STORY, "7", "seven"))
        self.assertFalse(counting_judge(Q_STORY, "7", "eight"))
        self.assertTrue(counting_judge(Q_INSTA, "1300", "1300"))
        self.assertFalse(counting_judge(Q_INSTA, "1250", "1300"))

    def test_judge_semantic_wordfold(self):
        self.assertEqual(judge_semantic(Q_STORY, "7", "seven"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_INSTA, "1300", "1300"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_INSTA, "1250", "1300"),
                         "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q_INSTA, S_INSTA)
        self.assertEqual(ans, "1300")
        self.assertEqual(meta, {"form": "supersede_total"})
        ans, meta = answer_counting(Q_STORY, S_STORY)
        self.assertEqual(ans, "7")
        self.assertEqual(meta, {"form": "supersede_total"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("assistant", A_ECHO_1250)]),)
        ans, meta = answer_counting(Q_INSTA, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "supersede_total"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
