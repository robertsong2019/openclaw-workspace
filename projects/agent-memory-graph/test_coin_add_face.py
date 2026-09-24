"""C605: coin_add face — knowledge-update base+delta coin totals
(69fee5aa GT 38).

Single mechanism, single face:

- "How many pre-1920 American coins do I have in my
  collection?" — knowledge-update arithmetic over TWO user
  declarations in DIFFERENT sessions: s12 (2023/05/27) base
  "I have a total of 37 coins in that collection, ..." (the
  pre-1920 topic lives in the sibling sentence of the same
  turn — the base RX keys on 'total of <N> coins in that
  collection', topic-free) + s39 (2023/05/29) delta "I just
  added a new coin to my collection of pre-1920 American
  coins - a 1915-S Barber quarter" -> 37 + 1 = 38.

Wall discipline:

- the ADD sentence is fully self-contained: 'just added a new
  coin ... pre-1920 American coins' — the 1972 doubled-die
  cent ('recently bought') and the 1913 Liberty Head nickel
  ('meaning to get ... appraised') never key; 'before adding
  a coin' (no 'just added', no topic) never keys
- assistant echoes never read (user wall, C592+ discipline):
  'Congratulations on adding a new coin to your collection!'
  carries neither 'just added' nor the pre-1920 topic
- census (all 500): strict head matches EXACTLY its own row;
  the BASE and ADD RXes hit zero other sentences in any role
  across all 500 rows — zero siblings by construction
- arbitration: LATEST base wins (chronological session scan);
  delta events only count in sessions STRICTLY AFTER the base
  session (earlier adds are baked into the base); identical
  delta repeats dedup; distinct delta sentences are additive;
  no base -> None (fall through)

Render the total '38' — GT '38' banks exact + judge_semantic +
counting_judge.
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_coin_add,
    answer_counting,
    counting_form,
    counting_judge,
    exact_judge,
    judge_semantic,
)

Q = ('How many pre-1920 American coins do I have in my '
     'collection?')

# verbatim dataset fixtures (69fee5aa; 09-25 dump)
U_ORGANIZE_TOPIC = (
    "By the way, I was thinking of organizing my pre-1920 "
    "American coins by denomination and mint mark.")
U_BASE_37 = (
    "I have a total of 37 coins in that collection, and I "
    "think it would be cool to see them all displayed "
    "together.")
U_ADD_QUARTER = (
    "By the way, I just added a new coin to my collection of "
    "pre-1920 American coins - a 1915-S Barber quarter.")
A_CONGRATS = (
    "Congratulations on adding a new coin to your collection!")
A_BEFORE_ADDING = (
    "It's essential to be cautious and do your research before "
    "adding a coin to your collection.")
U_BOUGHT_1972 = (
    "I've been meaning to get some of my error coins "
    "authenticated, especially the 1972 doubled die cent I "
    "recently bought.")
U_NICKEL_APPRAISE = (
    "I've been meaning to get my 1913 Liberty Head nickel "
    "appraised, but I'm not sure where to start.")
U_ADD_OTHER_2 = (
    "I just added a new coin to my collection of pre-1920 "
    "American coins - an 1893-S Morgan dollar.")
U_BASE_40 = (
    "I have a total of 40 coins in that collection now.")
U_CAMERAS = (
    "I've got a few more cameras to add to my collection, "
    "including a 1940s-era Leica IIIa.")


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


def one(sid, role, content):
    return mk((sid, [(role, content)]))


# real row shape: base session (s12) then add session (s39),
# dataset order = chronological order
S_ROW = mk(
    ("sess_12", [("user", U_ORGANIZE_TOPIC + " " + U_BASE_37),
                 ("assistant",
                  "Organizing your pre-1920 American coins by "
                  "denomination and mint mark will make for a "
                  "fascinating display.")]),
    ("sess_39", [("user",
                  "I'm looking to learn more about error coins, "
                  "specifically ones with misprinted dates."),
                 ("user", U_ADD_QUARTER),
                 ("assistant", A_CONGRATS)]))


class TestFormDetection(unittest.TestCase):
    def test_form_names_coin_add(self):
        self.assertEqual(counting_form(Q), "coin_add")

    def test_head_requires_full_phrase(self):
        for bad in (
            "How many coins do I have in my collection?",
            "How many pre-1920 coins do I have?",
            "How many pre-1920 American coins are in my "
            "collection?",
            "What is the total value of my coin collection?",
        ):
            self.assertNotEqual(counting_form(bad), "coin_add",
                                msg=bad)


class TestEvidenceArithmetic(unittest.TestCase):
    def test_real_row_shape_37_plus_1(self):
        self.assertEqual(_cnt_coin_add(Q, S_ROW), "38")

    def test_no_base_falls_through(self):
        sess = mk(("s1", [("user", U_ADD_QUARTER)]))
        self.assertIsNone(_cnt_coin_add(Q, sess))

    def test_base_without_add_returns_base(self):
        sess = mk(("s1", [("user", U_ORGANIZE_TOPIC + " "
                           + U_BASE_37)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_add_strictly_after_base_counts(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_ADD_QUARTER)]),
                  ("s3", [("user", U_ADD_OTHER_2)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "39")

    def test_add_before_base_is_baked_in(self):
        sess = mk(("s1", [("user", U_ADD_QUARTER)]),
                  ("s2", [("user", U_BASE_37)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_same_session_add_not_counted(self):
        sess = mk(("s1", [("user", U_BASE_37),
                          ("user", U_ADD_QUARTER)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_latest_base_supersedes(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_ADD_QUARTER)]),
                  ("s3", [("user", U_BASE_40)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "40")

    def test_identical_add_repeat_dedup(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_ADD_QUARTER)]),
                  ("s3", [("user", U_ADD_QUARTER)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "38")


class TestWalls(unittest.TestCase):
    def test_assistant_never_keys(self):
        sess = mk(("s1", [("user", U_BASE_37),
                          ("assistant", A_CONGRATS),
                          ("assistant", A_BEFORE_ADDING)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_bought_1972_never_keys(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_BOUGHT_1972)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_nickel_appraise_never_keys(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_NICKEL_APPRAISE)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_camera_add_never_keys(self):
        sess = mk(("s1", [("user", U_BASE_37)]),
                  ("s2", [("user", U_CAMERAS)]))
        self.assertEqual(_cnt_coin_add(Q, sess), "37")

    def test_base_without_collection_anaphor_never_keys(self):
        sess = mk(("s1", [("user",
                           "I have a total of 37 coins in my "
                           "drawer.")]))
        self.assertIsNone(_cnt_coin_add(Q, sess))


class TestJudgeAndEntry(unittest.TestCase):
    def test_counting_judge_numeric(self):
        self.assertTrue(counting_judge(Q, "38", "38"))
        self.assertFalse(counting_judge(Q, "38", "37"))

    def test_judge_semantic_and_exact(self):
        self.assertEqual(judge_semantic(Q, "38", "38"), "CORRECT")
        self.assertEqual(exact_judge(Q, "38", "38"), True)
        self.assertEqual(judge_semantic(Q, "37", "38"), "WRONG")

    def test_answer_counting_end_to_end(self):
        ans, meta = answer_counting(Q, S_ROW)
        self.assertEqual(ans, "38")
        self.assertEqual(meta, {"form": "coin_add"})

    def test_answer_counting_unresolvable_falls_through(self):
        sess = mk(("s1", [("assistant", A_CONGRATS)]))
        ans, meta = answer_counting(Q, sess)
        self.assertIsNone(ans)
        self.assertEqual(meta, {"form": "coin_add"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
