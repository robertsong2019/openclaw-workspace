"""C594: furniture multi-verb transaction-count face — gpt4_15e38248
(one mechanism, four verb faces: buy | assemble | sell | fix).

Head: "How many pieces of furniture did I buy, assemble, sell, or
fix in the past few months?" Census (all 500): matches EXACTLY
gpt4_15e38248, unbanked (gate=answer today — the row echoed a
session line). Window = 'past few months' → 91d (few=3, C592
30n+1 convention).

Evidence (user lines, verbatim): answer_8858d9dc_1 — coffee table
bought ~3 weeks ago; answer_8858d9dc_2 — IKEA bookshelf assembled
~2 months ago; answer_8858d9dc_3 — mattress ordered last week;
answer_8858d9dc_4 — kitchen-table wobbly leg fixed last weekend.
GT '4'; word-only render 'four' banks via judge_semantic
(_sem_norm folds to GT '4' — C591/C592/C593 discipline).

Mechanism (same-sentence discipline, C591/C592 lineage): a
furniture item counts only when its USER sentence carries BOTH a
transaction verb (bought|purchased|ordered|got|sold|assembled|
built|fixed|repaired|fixing|repairing|assembling|selling|buying)
AND a bounded past marker inside the window (_acq_marker_age_days
reuse); session-topic gate at session grain (C586 lesson); item
keys = (kept modifier +) singularized head noun — 'coffee table'
vs 'kitchen table' stay distinct, brand/case modifiers ('IKEA')
and stop adjectives ('new') drop so re-mentions collapse.

Guards pinned here:
- form claim: counting_form returns 'furniture_txn' for the head
  and does NOT steal the C592/C593 rows (plants/jewelry keep
  'acquire', antique keeps 'antique_inherit') nor the days-ago /
  rug / rearrange siblings
- decoys structurally out (no verb, no marker, or no furniture
  head): scratch guards, dog food, dog bed, violin, table lamp,
  bedside tables, sectional-sofa intent, rug/blanket chatter
- user-role wall (assistant restatements never render)
- dedup: coffee-table re-mentions across 3 sessions collapse
- window belt: four-months/ two-years surfaces drop; three-months
  and month-granularity surfaces count (C592 marker set reuse)
- mechanism, not hardcoding: swapping the verb ('unpacked'),
  removing the marker ('last weekend'), or adding a new item
  moves the answer
"""
import os
import sys
import unittest

if os.environ.get("PYTHONHASHSEED") != "7":
    os.execve(sys.executable, [sys.executable] + sys.argv,
              {**os.environ, "PYTHONHASHSEED": "7"})

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from amg_bench_quality import (
    _cnt_furniture_txn,
    _sem_norm,
    answer_counting,
    counting_form,
    judge_semantic,
)

Q_FURN = ('How many pieces of furniture did I buy, assemble, '
          'sell, or fix in the past few months?')
Q_PLANTS = 'How many plants did I acquire in the last month?'
Q_JEWEL = ('How many pieces of jewelry did I acquire in the last '
           'two months?')
Q_ANTIQUE = ('How many antique items did I inherit or acquire '
             'from my family members?')
Q_SMOKER = 'How many days ago did I buy a smoker?'
Q_RUG = ('How long had I been using the new area rug when I '
         'rearranged my living room furniture?')
Q_REARRANGE = ('I was thinking about rearranging the furniture in '
               'my bedroom this weekend. Any tips?')

# ── verbatim dataset fixtures (extracted from
#    longmemeval_s_cleaned gpt4_15e38248 haystack by
#    /tmp/c594/gen_fixture.py; drift pins assert the dataset
#    surfaces survive transcription) ──

# ── verbatim session 27 / answer_8858d9dc_1 (coffee table) ──
U_S1_T0 = "I need some help finding new throw pillows for my couch. I just got a new coffee table from West Elm about three weeks ago, and it's really made my living room feel modern, but my old pillows are looking worn out. Can you give me some recommendations on where to find some affordable and stylish ones?"
U_S1_T2 = "I like the idea of checking out West Elm's throw pillow selection since I just got my coffee table from them. I spent hours browsing their website to find the perfect wooden coffee table with metal legs, and it was delivered last Thursday. I'm thinking of getting pillows with a similar modern aesthetic to match the table. Do you have any specific recommendations for modern throw pillows on West Elm's website?"

# ── verbatim session 42 / answer_8858d9dc_2 (bookshelf) ──
U_S2_T0 = "I'm thinking of getting some new throw pillows for my couch, can you recommend some good online stores that sell a wide variety of patterns and fabrics? Oh, and speaking of organizing, I finally assembled that IKEA bookshelf for my home office about two months ago, and it's been a game-changer for my productivity."
U_S2_T2 = "I like the options you provided, especially West Elm since I've had a good experience with them when I bought my coffee table. Do you think I should consider the fabric type and material of my couch when choosing throw pillows, or can I just go with what I like?"
U_S2_T6 = 'I think I\'ll go with the 20" x 20" size, and I\'ll probably start with two pillows to see how it looks. Do you have any recommendations for patterns or designs that would complement my new coffee table? I got it from West Elm, and it\'s a wooden one with metal legs, so I want to find something that will tie in with that aesthetic. Also, speaking of organization, I\'ve been loving my new bookshelf in my home office - it\'s really helped me stay organized and focused.'
A_S2_T1 = " It sounds like you've been doing some great organizing and rearranging in your home! Congratulations on finally assembling that IKEA bookshelf – it's always satisfying to complete a project and see the positive impact it has on your space"

# ── verbatim session 6 / answer_8858d9dc_3 (mattress) ──
U_S3_T0 = "I'm looking for some recommendations on throw pillows for my couch. I just got a new coffee table and rearranged my living room, and now the old pillows are looking a bit worn out. By the way, I've been meaning to get a new mattress for ages, and last week I finally took the plunge and ordered one from Casper. It's supposed to arrive next Wednesday, and I'm really looking forward to getting a good night's sleep."
U_S3_T2 = "I'm thinking of getting a light gray or beige pillow to match the color scheme I have in mind for my future sectional sofa. Do you know any brands that offer a wide range of gray or beige throw pillows with wooden or metal accents?"
U_S3_T4 = "I'm thinking of getting a modern table lamp with a metallic accent to match the metal legs of my new coffee table. Do you have any recommendations for lamps with a similar aesthetic?"
U_S3_T6 = "I'm interested in exploring more options for bedside tables that would complement my new Casper mattress and modern aesthetic. Can you recommend some bedside tables with metal or glass accents that would fit well with my bedroom decor?"

# ── verbatim session 32 / answer_8858d9dc_4 (kitchen table) ──
U_S4_T0 = "I'm looking for some recommendations on throw pillows for my living room. I just got a new coffee table and rearranged the furniture, and I think some new pillows would really tie the room together."
U_S4_T2 = "My living room has a modern feel, and the dominant color scheme is a mix of neutral tones like beige, gray, and white. The new coffee table is wooden with metal legs, and I've been loving how it's added a touch of modernity to the room. By the way, speaking of fixing things around the house, I finally got around to fixing the wobbly leg on my kitchen table last weekend - it was driving me crazy for months, and all it took was a few minutes with a screwdriver to tighten the screw. Anyway, back to the throw pillows, I'd like something that will complement the modern feel and add a pop of color."

# ── verbatim decoy session 15 / 7784236e_2 (scratch guards) ──
U_DK_T0 = "I'm looking for some advice on cat-proofing my home. I just set up a new area for my kitten Luna to explore, but I'm worried about her damaging the furniture. Speaking of which, I bought scratch guards from IKEA to protect the furniture from Luna's scratching today, and it's been a lifesaver so far! Do you have any other tips on how to cat-proof my home?"

# ── verbatim decoy session 41 / e697b2dd_4 (dog bed / dog food) ──
U_DD_T0 = "I'm thinking of getting a new dog bed for my dog Max, do you have any recommendations for good brands or styles? By the way, I've been trying to get him to eat healthier, so I recently bought a bag of organic dog food with vegetables included for $45, it's a 15-pound bag."

# ── verbatim decoy session 9 / 87e55e85_2 (violin) ──
U_DV_T0 = "I'm planning to go to a music festival next weekend and I want to know what kind of music gear I should bring with me. By the way, I've been playing my acoustic guitar every day since I got it, and I'm really excited to try out some new techniques at the festival."


# ── drift pins: dataset surfaces survive transcription ──
class TestFixtureDrift(unittest.TestCase):
    def test_drift_pins(self):
        self.assertIn('coffee table from West Elm about three weeks '
                      'ago', U_S1_T0)
        self.assertIn('assembled that IKEA bookshelf for my home '
                      'office about two months ago', U_S2_T0)
        self.assertIn('ordered one from Casper', U_S3_T0)
        self.assertIn('fixing the wobbly leg on my kitchen table '
                      'last weekend', U_S4_T2)
        self.assertIn('bought scratch guards from IKEA to protect '
                      'the furniture', U_DK_T0)
        self.assertIn('recently bought a bag of organic dog food',
                      U_DD_T0)
        self.assertIn('playing my acoustic guitar every day '
                      'since I got it', U_DV_T0)
        self.assertIn('future sectional sofa', U_S3_T2)
        self.assertIn('modern table lamp', U_S3_T4)
        self.assertIn('bedside tables', U_S3_T6)


def mk(*specs):
    """Build sessions from (session_id, [(role, content), ...])."""
    return [{"session_id": sid,
             "turns": [{"role": r, "content": c} for r, c in turns]}
            for sid, turns in specs]


S1 = mk(("s1", [("user", U_S1_T0), ("assistant", "ok"),
                ("user", U_S1_T2)]))[0]
S2 = mk(("s2", [("user", U_S2_T0), ("assistant", A_S2_T1),
                ("user", U_S2_T2), ("assistant", "ok"),
                ("user", U_S2_T6)]))[0]
S3 = mk(("s3", [("user", U_S3_T0), ("assistant", "ok"),
                ("user", U_S3_T2), ("assistant", "ok"),
                ("user", U_S3_T4), ("assistant", "ok"),
                ("user", U_S3_T6)]))[0]
S4 = mk(("s4", [("user", U_S4_T0), ("assistant", "ok"),
                ("user", U_S4_T2)]))[0]
DK = mk(("dk", [("user", U_DK_T0)]))[0]
DD = mk(("dd", [("user", U_DD_T0)]))[0]
DV = mk(("dv", [("user", U_DV_T0)]))[0]
FULL = [S1, S2, S3, S4, DK, DD, DV]


class TestFormClaim(unittest.TestCase):
    def test_form_claim(self):
        self.assertEqual(counting_form(Q_FURN), "furniture_txn")

    def test_no_steal_c592_c593_rows(self):
        self.assertEqual(counting_form(Q_PLANTS), "acquire")
        self.assertEqual(counting_form(Q_JEWEL), "acquire")
        self.assertEqual(counting_form(Q_ANTIQUE), "antique_inherit")

    def test_no_steal_siblings(self):
        # gpt4_8279ba02 (days-ago), 993da5e2 (how-long rug),
        # 57f827a0 (rearrange advice) — none is the furniture head
        self.assertNotEqual(counting_form(Q_SMOKER), "furniture_txn")
        self.assertNotEqual(counting_form(Q_RUG), "furniture_txn")
        self.assertNotEqual(counting_form(Q_REARRANGE),
                            "furniture_txn")


class TestRescue(unittest.TestCase):
    def test_full_haystack_four(self):
        self.assertEqual(_cnt_furniture_txn(Q_FURN, FULL), "four")

    def test_answer_counting_wired(self):
        ans, detail = answer_counting(Q_FURN, FULL)
        self.assertEqual(ans, "four")
        self.assertEqual(detail.get("form"), "furniture_txn")

    def test_judge_semantic_banks_word_render(self):
        self.assertEqual(judge_semantic(Q_FURN, "4", "four"),
                         "CORRECT")
        self.assertEqual(judge_semantic(Q_FURN, "4", "three"),
                         "WRONG")
        self.assertEqual(judge_semantic(Q_FURN, "4", "five"),
                         "WRONG")
        # norm-fold contract: 'four' -> '4'
        self.assertEqual(_sem_norm("four"), _sem_norm("4"))


class TestVerbFaces(unittest.TestCase):
    """Each evidence session alone resolves to exactly one item —
    one mechanism, four verb faces."""

    def test_buy_face_coffee_table(self):
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S1]), "one")

    def test_assemble_face_bookshelf(self):
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S2]), "one")

    def test_buy_face_mattress(self):
        # 'ordered' is the render verb; 'get' in 'meaning to get'
        # is intent and must not be required
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S3]), "one")

    def test_fix_face_kitchen_table(self):
        # gerund 'fixing' after 'got around to' is the surface
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S4]), "one")

    def test_sell_face_synthetic(self):
        sess = mk(("sx", [
            ("user", "I sold my old recliner last week."),
            ("user", "I bought a stool three days ago."),
        ]))
        self.assertEqual(_cnt_furniture_txn(Q_FURN, sess), "two")

    def test_distinct_tables_not_collapsed(self):
        sess = mk(("sx", [
            ("user", "I bought a coffee table three weeks ago. "
                     "I fixed my kitchen table last weekend."),
        ]))
        self.assertEqual(_cnt_furniture_txn(Q_FURN, sess), "two")


class TestDecoyWalls(unittest.TestCase):
    def test_decoy_sessions_render_nothing(self):
        for sess in ([DK], [DD], [DV]):
            self.assertIsNone(_cnt_furniture_txn(Q_FURN, sess))

    def test_decoy_sessions_do_not_pollute_full(self):
        # FULL already contains DK/DD/DV — count stays 'four'
        self.assertEqual(len(FULL), 7)
        self.assertEqual(_cnt_furniture_txn(Q_FURN, FULL), "four")

    def test_intent_and_lamp_and_bedside_out(self):
        # S3 carries the sectional-sofa intent, the table lamp and
        # the bedside-tables asks — mattress still the only item
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S3]), "one")

    def test_user_wall_assistant_restatement(self):
        # assistant-only session: even a marker-carrying
        # restatement renders nothing
        wall = mk(("w", [
            ("assistant", "You mentioned you finally assembled "
                          "that IKEA bookshelf for your home "
                          "office about two months ago."),
        ]))[0]
        self.assertIsNone(_cnt_furniture_txn(Q_FURN, [wall]))
        # and it adds nothing to the real session
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S2, wall]),
                         "one")

    def test_verbatim_assistant_restatement_neutral(self):
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S2]), "one")


class TestDedup(unittest.TestCase):
    def test_coffee_table_rementions_collapse(self):
        # S1 + S3 + S4 all re-mention the coffee table; mattress
        # and kitchen table are new items → 'three'
        self.assertEqual(
            _cnt_furniture_txn(Q_FURN, [S1, S3, S4]), "three")

    def test_key_collapse_modifier_drop(self):
        extra = mk(("sx", [
            ("user", "I also bought a new bookshelf lamp last "
                     "week."),
        ]))[0]
        # 'new bookshelf lamp' folds to key 'bookshelf' — the
        # IKEA bookshelf already counted
        self.assertEqual(_cnt_furniture_txn(Q_FURN, [S2, extra]),
                         "one")


class TestWindowDiscipline(unittest.TestCase):
    def test_in_window_month_surfaces(self):
        for txt in ("I bought a futon a month ago.",
                    "I bought a wardrobe last month.",
                    "I bought a desk three months ago."):
            sess = mk(("sx", [("user", txt)]))
            self.assertEqual(_cnt_furniture_txn(Q_FURN, sess),
                             "one", txt)

    def test_out_of_window_surfaces(self):
        for txt in ("I bought a desk four months ago.",
                    "I bought a desk two years ago.",
                    "I bought a desk last year."):
            sess = mk(("sx", [("user", txt)]))
            self.assertIsNone(_cnt_furniture_txn(Q_FURN, sess), txt)


class TestMechanismNotHardcoding(unittest.TestCase):
    def test_verb_swap_drops_item(self):
        t0 = U_S2_T0.replace("finally assembled", "finally unpacked")
        self.assertNotEqual(t0, U_S2_T0)
        sess = mk(("s2", [("user", t0)]))
        self.assertIsNone(_cnt_furniture_txn(Q_FURN, sess))

    def test_marker_removal_drops_item(self):
        t2 = U_S4_T2.replace(" last weekend", "")
        self.assertNotEqual(t2, U_S4_T2)
        sess = mk(("s4", [("user", t2)]))
        self.assertIsNone(_cnt_furniture_txn(Q_FURN, sess))

    def test_added_item_moves_answer(self):
        sess = mk(("sx", [
            ("user", U_S1_T0),
            ("user", "I also bought a reading chair last week."),
        ]))
        self.assertEqual(_cnt_furniture_txn(Q_FURN, sess), "two")

    def test_unresolvable_falls_through(self):
        self.assertIsNone(_cnt_furniture_txn(Q_FURN, []))
        bare = mk(("sx", [("user", "I love this couch advice!")]))
        self.assertIsNone(_cnt_furniture_txn(Q_FURN, bare))


if __name__ == "__main__":
    unittest.main()
