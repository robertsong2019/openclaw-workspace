"""C606: weddings_attended face — role-keyed attended-wedding
census (gpt4_2f8be40d GT 'three').

Single mechanism, single face:

- "How many weddings have I attended in this year?" — counts
  DISTINCT attended weddings keyed by the role-noun possessive
  in user sentences that carry an attendance marker:
  s6 'I just got back from my college roommate's wedding'
  (Emily+Sarah) + s9 'I've been to a few weddings recently and
  one of them was my cousin's wedding at a vineyard in August'
  (Rachel) + s41 'I just got back from a friend's wedding last
  weekend' (Jen+Tom) -> 3.

Wall discipline:

- the OWN-wedding wall: 'planning my own wedding' / 'getting
  married soon ... wedding venue ideas' carry no attendance
  verb — the upcoming own wedding never keys
- the sister wall: 'my sister's wedding was just amazing ...
  I was the maid of honor' praises the event but never phrases
  attendance — no marker, no key (this is the decoy that made
  enum_count read '4' before the face claimed the row)
- repeat mentions dedup by role key (cousin's vineyard wedding
  re-mentioned 4x, friend's wedding 3x — one event each)
- assistant echoes never read (user wall via _map_sents)
- census (all 500): strict head matches EXACTLY its own row; a
  loose 'how many weddings' sweep hits no other row
- nothing resolves -> None (fall through)

Render '3' — counting_judge numeric path banks (GT first
numeric claim 'three' -> 3.0; '4' stays WRONG).
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_weddings,
    answer_counting,
    counting_form,
    counting_judge,
)

Q = 'How many weddings have I attended in this year?'

# verbatim dataset fixtures (gpt4_2f8be40d; 09-25 dump)
U_ROOMMATE_WED = (
    "By the way, I just got back from my college roommate's "
    "wedding in the city, and it was beautiful - they had a "
    "rooftop garden ceremony overlooking the skyline, and it "
    "was so romantic.")
U_COUSIN_WED = (
    "I've been to a few weddings recently and one of them was "
    "my cousin's wedding at a vineyard in August, which was "
    "just stunning.")
U_FRIEND_WED = (
    "By the way, I just got back from a friend's wedding last "
    "weekend, and it was amazing - the bride, Jen, looked "
    "stunning in her bohemian-inspired dress, and her husband, "
    "Tom, was clearly smitten with her.")
U_OWN_WEDDING = (
    "I'm planning my own wedding and I need some help with "
    "finding a venue.")
U_GETTING_MARRIED = (
    "I'm getting married soon and I'm looking for some wedding "
    "venue ideas.")
U_SISTER_WED = (
    "By the way, speaking of weddings, my sister's wedding was "
    "just amazing, and I'm still on a high from it.")
U_SISTER_MAID = (
    "Yeah, I was the maid of honor, and it was a lot of "
    "responsibility, but I'm glad I could be there for my "
    "sister.")
U_COUSIN_REPEAT = (
    "My cousin Rachel's wedding at the vineyard was just "
    "perfect, she looked stunning in her lace gown and the "
    "whole atmosphere was so joyful.")
A_EMILY_ECHO = (
    "It's wonderful to hear about your friend Emily's wedding, "
    "and I'm thrilled that she and Sarah were able to tie the "
    "knot in a beautiful rooftop garden ceremony.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


# real row shape: three attended weddings spread over sessions,
# with the two decoy walls (own + sister) between them
S_ROW = mk(
    ("sess_6", [("user", U_OWN_WEDDING + " " + U_ROOMMATE_WED),
                ("assistant", A_EMILY_ECHO)]),
    ("sess_9", [("user", U_GETTING_MARRIED + " " + U_COUSIN_WED),
                ("user", U_COUSIN_REPEAT)]),
    ("sess_24", [("user", U_SISTER_WED),
                 ("user", U_SISTER_MAID)]),
    ("sess_41", [("user", U_OWN_WEDDING + " " + U_FRIEND_WED)]))


class TestFormDetection(unittest.TestCase):
    def test_form_names_weddings_attended(self):
        self.assertEqual(counting_form(Q), "weddings_attended")

    def test_head_requires_full_phrase(self):
        for bad in (
            "How many weddings did I attend?",
            "How many weddings have I attended?",
            "How many weddings have I been to this year?",
            "How many people attended my wedding?",
            "Did I attend any weddings this year?",
        ):
            self.assertNotEqual(counting_form(bad), "weddings_attended",
                                msg=bad)


class TestAttendanceCensus(unittest.TestCase):
    def test_real_row_shape_three(self):
        self.assertEqual(_cnt_weddings(Q, S_ROW), "3")

    def test_no_attendance_marker_falls_through(self):
        sess = mk(("s1", [("user", U_SISTER_WED),
                          ("user", U_OWN_WEDDING)]))
        self.assertIsNone(_cnt_weddings(Q, sess))

    def test_each_marker_alone_counts_one(self):
        for frag in (U_ROOMMATE_WED, U_COUSIN_WED, U_FRIEND_WED):
            sess = mk(("s1", [("user", frag)]))
            self.assertEqual(_cnt_weddings(Q, sess), "1", msg=frag)

    def test_role_repeat_dedups(self):
        sess = mk(("s1", [("user", U_COUSIN_WED)]),
                  ("s2", [("user", U_COUSIN_REPEAT)]),
                  ("s3", [("user",
                           "My cousin Rachel's wedding at the "
                           "vineyard had a wine tasting, and it "
                           "was so much fun.")]))
        self.assertEqual(_cnt_weddings(Q, sess), "1")

    def test_distinct_roles_additive(self):
        sess = mk(("s1", [("user", U_ROOMMATE_WED)]),
                  ("s2", [("user", U_COUSIN_WED)]),
                  ("s3", [("user", U_FRIEND_WED)]))
        self.assertEqual(_cnt_weddings(Q, sess), "3")


class TestWalls(unittest.TestCase):
    def test_own_wedding_never_keys(self):
        sess = mk(("s1", [("user", U_ROOMMATE_WED)]),
                  ("s2", [("user", U_OWN_WEDDING),
                          ("user", U_GETTING_MARRIED)]))
        self.assertEqual(_cnt_weddings(Q, sess), "1")

    def test_sister_wedding_never_keys(self):
        sess = mk(("s1", [("user", U_ROOMMATE_WED)]),
                  ("s2", [("user", U_SISTER_WED),
                          ("user", U_SISTER_MAID)]))
        self.assertEqual(_cnt_weddings(Q, sess), "1")

    def test_assistant_never_keys(self):
        sess = mk(("s1", [("user", U_ROOMMATE_WED),
                          ("assistant", A_EMILY_ECHO),
                          ("assistant",
                           "Congratulations on your upcoming "
                           "wedding! Have you considered a "
                           "beachfront venue?")]))
        self.assertEqual(_cnt_weddings(Q, sess), "1")

    def test_no_been_to_without_wedding(self):
        sess = mk(("s1", [("user",
                           "I've been to a few concerts recently "
                           "and one of them was my cousin's "
                           "birthday party.")]))
        self.assertIsNone(_cnt_weddings(Q, sess))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric(self):
        gt = ("I attended three weddings. The couples were Rachel "
              "and Mike, Emily and Sarah, and Jen and Tom.")
        self.assertTrue(counting_judge(Q, gt, "3"))
        self.assertTrue(counting_judge(Q, gt, "three"))
        self.assertFalse(counting_judge(Q, gt, "4"))

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "3")
        self.assertEqual(meta, {"form": "weddings_attended"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("user", U_SISTER_WED)]))
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "weddings_attended"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
