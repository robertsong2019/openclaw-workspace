"""C593: unbounded family-source antique-count face — 4f54b7c9
(one mechanism, two source faces).

Head: "How many antique items did I inherit or acquire from my
family members?" Census (all 500): matches EXACTLY 4f54b7c9,
unbanked (gate=answer today — the row fell through to chit-chat).
No time window — the family-SOURCE constraint replaces it (the
C592 acquire heads keep their 'in the last <period>' rows).

Evidence (user lines, verbatim): session_21 (appraisal) — antique
tea set (cousin Rachel) + vintage typewriter (belonged to dad);
session_42 (insurance) — grandmother's vintage diamond necklace
(family possessive) + antique music box (great-aunt) +
depression-era glassware (mom). 5 distinct items across 9
re-mention lines; dedup by item key collapses them.

Source faces:
- S1: signal adjective ('antique'|'vintage'|'depression-era') +
  item NP + family-source marker AFTER the NP in the SAME
  sentence ('from my cousin Rachel' / 'came from my cousin' /
  'belonged to my dad')
- S2: family possessive BEFORE the signal-NP ('my grandmother's
  vintage diamond necklace')

Guards pinned here:
- form claim: counting_form returns 'antique_inherit' for the
  head and does NOT steal the C592 window rows (plants/jewelry
  keep 'acquire' — they carry 'in the last <period>')
- user-role wall (assistant insurance prose never renders)
- source-window discipline: the family marker must sit INSIDE
  the item's own window (between its signal adjective and the
  next signal adjective) — 'antique dealers' harvests nothing
- signal wall: non-signal family items ('my grandmother's
  necklace' without an antique/vintage adjective) don't count
- family wall: non-family sources ('from a local estate sale')
  don't count
- window belt: a question carrying 'in the last <period>' falls
  through (None) — window semantics belong to the C592 heads
- dedup discipline: repeat mentions collapse (9 lines → 5 items)
- mechanism, not hardcoding: adding/removing items moves the
  answer; mutating the signal adjective or family source drops it
- word-only render 'five': judge_semantic banks the row (frozen
  correct_exact=False), _sem_norm folds 'five' → GT '5'
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_antique_inherit,
    _sem_norm,
    answer_counting,
    counting_form,
    judge_semantic,
)

Q_ANTIQUE = ('How many antique items did I inherit or acquire from '
             'my family members?')
Q_PLANTS = 'How many plants did I acquire in the last month?'
Q_JEWEL = ('How many pieces of jewelry did I acquire in the last '
           'two months?')

# ── verbatim dataset fixtures (extracted from
#    longmemeval_s_cleaned 4f54b7c9 haystack by
#    /tmp/c593/step3_gen_fixture.py; drift pins assert the
#    dataset surfaces survive transcription) ──

# ── verbatim session_21 (appraisal; user) ──
U_S21_A = "I'm thinking of decluttering my apartment and selling some old family heirlooms to make some extra cash. I have an antique tea set from my cousin Rachel and a vintage typewriter that belonged to my dad. Do you know where I can find a good appraiser or someone to help me determine their value?"
U_S21_B = "I'll also mention that I received the antique tea set from my cousin Rachel and a vintage typewriter that belonged to my dad, in case that adds any context or significance to the items."
U_S21_C = "I'll make sure to mention the provenance of the items to the antique dealers I reach out to. I'll let them know that the antique tea set came from my cousin Rachel and the vintage typewriter belonged to my dad, and share any relevant stories or documents that I have. Do you think I should also mention that I've been decluttering my apartment and found these items, or is that not relevant to the dealers?"
U_S21_D = "I was also thinking of reaching out to local antique dealers who specialize in tea sets and typewriters to see if they'd be interested in buying my items or know someone who might be. Do you think that's a good idea, and do you have any tips on how to approach them?"

# ── verbatim session_42 (insurance; user) ──
U_S42_A = "I'm trying to get my grandmother's vintage diamond necklace insured, but I'm not sure where to start. I inherited it recently, along with a few other family heirlooms, including an antique music box from my great-aunt and a set of depression-era glassware from my mom. Do you have any recommendations for insurance companies that specialize in insuring valuable items like these?"
U_S42_B = "Can you tell me more about the appraisal process for my grandmother's vintage diamond necklace? I'd like to know what kind of documentation I need to provide and what factors will affect the appraisal value."
U_S42_C = "That's really helpful, thanks. So, I should get the appraisal report and then shop around for insurance companies that specialize in insuring valuable items like my grandmother's necklace. I also have an antique music box from my great-aunt and a set of depression-era glassware from my mom that I'd like to insure. Do you think I should get those items appraised as well, or would it be better to focus on insuring the necklace first?"

# ── verbatim assistant echo (s42 t1; the chain pred today) ──
A_S42_T1 = 'Congratulations on inheriting these precious family heirlooms! Insuring them is a wise decision to protect their value and sentimental significance.'

# ── drift pins: dataset drift must fail loudly ──
assert "an antique tea set from my cousin Rachel" in U_S21_A, \
    "U_S21_A drifted"
assert "a vintage typewriter that belonged to my dad" in U_S21_A, \
    "U_S21_A drifted"
assert "I received the antique tea set from my cousin Rachel" \
    in U_S21_B, "U_S21_B drifted"
assert "the antique tea set came from my cousin Rachel" in U_S21_C, \
    "U_S21_C drifted"
assert "the vintage typewriter belonged to my dad" in U_S21_C, \
    "U_S21_C drifted"
assert "local antique dealers who specialize in tea sets" in U_S21_D, \
    "U_S21_D drifted"
assert "my grandmother's vintage diamond necklace insured" in U_S42_A, \
    "U_S42_A drifted"
assert "an antique music box from my great-aunt" in U_S42_A, \
    "U_S42_A drifted"
assert "a set of depression-era glassware from my mom" in U_S42_A, \
    "U_S42_A drifted"
assert "for my grandmother's vintage diamond necklace?" in U_S42_B, \
    "U_S42_B drifted"
assert "like my grandmother's necklace." in U_S42_C, "U_S42_C drifted"
assert "an antique music box from my great-aunt" in U_S42_C, \
    "U_S42_C drifted"
assert "inheriting these precious family heirlooms" in A_S42_T1, \
    "A_S42_T1 drifted"


def S(sid, *user_texts):
    return {"session_id": sid,
            "turns": [{"role": "user", "content": t} for t in user_texts]}


ANTIQUE_SESSIONS = [
    S("session_21", U_S21_A, U_S21_D, U_S21_B, U_S21_C),
    S("session_42", U_S42_A, U_S42_B, U_S42_C),
]


class TestAntiqueInheritFace(unittest.TestCase):

    # ── form claim ──

    def test_form_claim(self):
        self.assertEqual(counting_form(Q_ANTIQUE), "antique_inherit")

    def test_form_does_not_steal_window_heads(self):
        # the C592 acquire heads keep their 'in the last <period>'
        # rows — the antique head claims NO window question
        self.assertEqual(counting_form(Q_PLANTS), "acquire")
        self.assertEqual(counting_form(Q_JEWEL), "acquire")

    def test_form_generic_how_many_untouched(self):
        # behavior-neutral elsewhere: plain how-many forms stay
        # with enum_count (census: the antique head is anchored on
        # 'antique items ... inherit/acquire ... famil')
        self.assertEqual(counting_form('How many books do I own?'),
                         "enum_count")

    # ── the face, end to end ──

    def test_rescue_five(self):
        self.assertEqual(
            _cnt_antique_inherit(Q_ANTIQUE, ANTIQUE_SESSIONS), "five")

    def test_answer_counting_form_meta(self):
        self.assertEqual(
            answer_counting(Q_ANTIQUE, ANTIQUE_SESSIONS),
            ("five", {"form": "antique_inherit"}))

    # ── dedup across re-mentions ──

    def test_session21_only_two(self):
        # 4 lines, 3 re-mention rounds → tea set + typewriter
        sessions = [S("session_21", U_S21_A, U_S21_D, U_S21_B,
                      U_S21_C)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "two")

    def test_session42_only_three(self):
        # 3 lines, necklace re-mentioned twice, music box and
        # glassware once each (t0) + once more (t4)
        sessions = [S("session_42", U_S42_A, U_S42_B, U_S42_C)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "three")

    # ── source faces ──

    def test_s2_possessive_face_one(self):
        # 'my grandmother's vintage diamond necklace' — family
        # possessive BEFORE the signal-NP, no post-NP marker
        sessions = [S("session_42", U_S42_B)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "one")

    def test_possessive_without_signal_wall(self):
        # 'my grandmother's necklace' carries NO antique/vintage
        # adjective — the family possessive alone doesn't count
        sessions = [S("s", "Can you tell me more about my "
                           "grandmother's necklace?")]
        self.assertIsNone(_cnt_antique_inherit(Q_ANTIQUE, sessions))

    def test_signal_wall(self):
        # 'a set of old glassware from my mom' — 'old' is not an
        # antique-signal adjective; glassware drops
        mutated = U_S42_A.replace("depression-era glassware",
                                  "old glassware")
        sessions = [S("session_42", mutated)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "two")

    def test_family_source_wall(self):
        # 'from a local estate sale' — no family member, no count
        mutated = U_S21_A.replace("from my cousin Rachel",
                                  "from a local estate sale")
        sessions = [S("session_21", mutated)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "one")

    def test_source_window_discipline(self):
        # the family marker must sit inside the ITEM's own window:
        # 'an antique music box and a vintage necklace from my
        # mom' — the mom marker belongs to the necklace window
        # only; the music box carries no source of its own
        sent = ("I also have an antique music box and a vintage "
                "necklace from my mom.")
        sessions = [S("s", sent)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "one")

    def test_antique_dealers_decoy_none(self):
        # 'antique dealers who specialize in tea sets' — the
        # signal attaches to dealers, no family source follows
        sessions = [S("session_21", U_S21_D)]
        self.assertIsNone(_cnt_antique_inherit(Q_ANTIQUE, sessions))

    # ── walls / fall-throughs ──

    def test_user_role_wall(self):
        sessions = [{"session_id": "session_42", "turns": [
            {"role": "assistant", "content": A_S42_T1},
            {"role": "assistant", "content": U_S42_A}]}]
        self.assertIsNone(_cnt_antique_inherit(Q_ANTIQUE, sessions))

    def test_window_belt_falls_through(self):
        # a 'in the last <period>' variant belongs to window
        # semantics (C592) — the antique head must not render it
        self.assertIsNone(_cnt_antique_inherit(
            'How many antique items did I inherit or acquire from '
            'my family members in the last month?', ANTIQUE_SESSIONS))

    def test_empty_sessions_none(self):
        self.assertIsNone(_cnt_antique_inherit(Q_ANTIQUE, []))

    # ── mechanism, not hardcoding ──

    def test_sixth_item_moves_answer(self):
        sessions = [S("session_21", U_S21_A, U_S21_B),
                    S("session_42", U_S42_A),
                    S("session_7", "An antique pocket watch from my "
                                   "uncle arrived last week.")]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "six")

    def test_dropping_music_box_drops_answer(self):
        mutated = U_S42_A.replace(
            "an antique music box from my great-aunt and ", "")
        sessions = [S("session_42", mutated)]
        self.assertEqual(_cnt_antique_inherit(Q_ANTIQUE, sessions),
                         "two")

    # ── render / judge discipline ──

    def test_render_is_word_form(self):
        ans = _cnt_antique_inherit(Q_ANTIQUE, ANTIQUE_SESSIONS)
        self.assertEqual(ans, "five")
        self.assertNotIn("5", ans)

    def test_judge_semantic_banks_five_over_gt_5(self):
        # the row banks on judge_semantic alone (frozen
        # correct_exact=False); _sem_norm folds 'five' → '5'
        self.assertEqual(judge_semantic(Q_ANTIQUE, "five", "5"),
                         "CORRECT")
        self.assertEqual(_sem_norm("five"), _sem_norm("5"))
        self.assertEqual(judge_semantic(Q_ANTIQUE, "four", "5"),
                         "WRONG")


if __name__ == "__main__":
    unittest.main()
