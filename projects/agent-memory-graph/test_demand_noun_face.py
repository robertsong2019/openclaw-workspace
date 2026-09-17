"""Cycle 584 - demand-noun recall face (demand_noun gate).

"Can you remind me what sealant you recommended for the newspaper
flower vase?" is answered by the assistant sentence CONTAINING the
demand noun: the question names the thing it wants ("what <noun>
you recommended"), so any candidate sentence lacking that noun is
structurally not the answer. The face filters assistant sentences
to demand-noun carriers and ranks by raw question-keyword hits; a
tie at the top = ambiguous = fall-through.

Design notes (C537 lineage):
- the existing speaker_recall min_raw=3 floor EXCLUDES the answer
  sentence here (it matches only sealant+vase = 2 keywords) while
  the junk opener ("Newspaper Flower Vase - Roll up...") passes
  with 3 rare-noun matches - the demand noun is a hard filter, not
  a score tweak;
- verbs are recommendation-family only (recommend/suggest/use/
  mention, both orders). "what <noun> you said" (fea54f57, banked
  via speaker_recall) is deliberately OUT of the census - interlock
  pinned below;
- user-role wall.

Census: frame ("remind me|you told me|i remember") + demand-noun
form accepts exactly 1/500 questions (8aef76bc) - zero hijack
surface by construction. Fixture messages are verbatim copies of
8aef76bc session_1 (the DIY decor answer set).
"""

import unittest

from amg_bench_quality import (
    LongMemEvalAdapter,
    _normalize,
    answer_demand_noun,
    demand_noun_form,
    exact_judge,
)

Q = "I'm going back to our previous conversation about DIY home decor projects using recycled materials. Can you remind me what sealant you recommended for the newspaper flower vase?"
GT = 'Mod Podge or another sealant'
EXPECTED = ("Seal the vase with Mod Podge or another sealant to "
            "make it water-resistant.")
DIY_MSGS = ['Yes, here are a few DIY home decor projects using recycled materials:\n\n1. Wine Cork Bulletin Board - Collect wine corks and arrange them in a square or rectangular shape. Glue them together and add a fabric backing to create a unique and functional bulletin board.\n\n2. Newspaper Flower Vase - Roll up strips of newspaper to create a sturdy base, then weave them together to make a vase. Seal the vase with Mod Podge or another sealant to make it water-resistant.\n\n3. Bottle Cap Coasters - Collect bottle caps and arrange them in a pattern on a cork base. Use glue to secure them in place and add a sealant to protect against moisture.\n\n4. Mason Jar Wall Planter - Attach metal hose clamps to a wooden board and insert Mason jars into the clamps. Fill the jars with soil and add small plants to create a living wall decor.\n\n5. Scrap Fabric Rag Rug - Gather old T-shirts or scraps of fabric and braid them into long strands. Coil the strands into a circular or oval shape and sew them together to create a colorful and unique rug.\n\nThese DIY home decor projects using recycled materials are fun, affordable, and eco-friendly ways to decorate your home while reducing waste.', "Have fun creating your own unique home decor using recycled materials. It's a great way to express your creativity while also being environmentally conscious. Good luck with your projects!", "Sure, here are a few more ideas to incorporate sustainable and eco-friendly elements into your home decor:\n\n1. Use LED light bulbs - These bulbs use less energy and last longer than traditional bulbs.\n\n2. Choose sustainable fabrics - Look for materials made from eco-friendly fibers like organic cotton, bamboo, or hemp.\n\n3. Add indoor plants - Plants not only add a natural element to your decor, but they also purify the air and can improve your mood.\n\n4. Find furniture made from sustainable materials - Look for furniture made from wood certified by the Forest Stewardship Council (FSC), which ensures it was harvested sustainably.\n\n5. Use natural cleaning products - Avoid harsh chemicals and opt for natural cleaning products that are better for the environment and your health.\n\nBy incorporating these sustainable and eco-friendly elements into your home decor, you're making a positive impact on the environment while creating a beautiful and healthy living space.", 'Yes, there are a number of places where you can find eco-friendly furniture. Here are a few options:\n\n1. Online retailers - There are many online retailers that specialize in eco-friendly furniture, such as Greenington, Vivaterra, and Joybird. 2. Secondhand stores - Check out thrift stores, consignment shops, and antique stores for unique, vintage pieces that have already stood the test of time. 3. Custom furniture makers - Look for furniture makers who use sustainable materials and practices to create custom pieces that fit your style and needs. 4. Local artisans - Search for local artisans who create furniture from reclaimed or salvaged materials or who use eco-friendly materials in their designs. 5. DIY projects - Consider creating your own eco-friendly furniture by upcycling old pieces or using sustainable materials like bamboo, reclaimed wood, or recycled metal. By making an effort to find eco-friendly furniture, you are supporting environmentally conscious practices and creating a more sustainable home decor.']


def _pool(*msgs):
    return list(msgs)


def _nodes(pool):
    """dict wired the way speaker_recall sees self._nodes."""
    return {"n%d" % i: {"role": r, "label": c}
            for i, (r, c) in enumerate(pool)}


class DemandNounFormTests(unittest.TestCase):
    def test_form_accepts_target(self):
        self.assertEqual(demand_noun_form(Q), "sealant")

    def test_form_interlock_said_verb_excluded(self):
        # fea54f57 shape: banked via speaker_recall - must not fire
        self.assertIsNone(demand_noun_form(
            "I was thinking about our previous conversation about "
            "the Fifth Album, and I was wondering if you could "
            "tell me what song you said I would like?"))

    def test_form_rejects_no_frame(self):
        self.assertIsNone(demand_noun_form(
            "What sealant did you recommend for the newspaper "
            "flower vase?"))

    def test_form_rejects_no_demand_noun(self):
        self.assertIsNone(demand_noun_form(
            "Can you remind me what you recommended for the "
            "newspaper flower vase?"))


class DemandNounAnswerTests(unittest.TestCase):
    def test_sealant_rescued(self):
        pool = _pool(*[("assistant", m) for m in DIY_MSGS])
        ans, detail = answer_demand_noun(Q, _nodes(pool))
        self.assertEqual(ans, EXPECTED)
        self.assertEqual(detail["form"], "demand_noun")
        self.assertEqual(detail["candidates"], 2)

    def _tie_pool(self):
        return [("assistant", "Use a sealant to finish the craft."),
                ("assistant", "Add a sealant before painting it.")]

    def test_tie_at_top_is_ambiguous(self):
        ans, detail = answer_demand_noun(Q, _nodes(self._tie_pool()))
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "ambiguous")

    def test_no_candidate_falls_through(self):
        pool = [("assistant", "Nothing about that topic here.")]
        ans, detail = answer_demand_noun(Q, _nodes(pool))
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_candidate")

    def test_plural_evidence_matches(self):
        pool = [("assistant",
                 "Seal it with a quality sealants product line.")]
        ans, detail = answer_demand_noun(Q, _nodes(pool))
        self.assertIsNotNone(ans)

    def test_user_role_wall(self):
        pool = _nodes([("user", m) for m in DIY_MSGS])
        ans, detail = answer_demand_noun(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_candidate")


class DemandNounJudgePins(unittest.TestCase):
    """Pre-verified render -> judge contracts (frozen)."""

    def test_render_contains_gt(self):
        self.assertIn(_normalize(GT), _normalize(EXPECTED))
        self.assertTrue(exact_judge(Q, GT, EXPECTED))

    def test_old_junk_pred_stays_unbanked(self):
        junk = ("Newspaper Flower Vase - Roll up strips of newspaper "
                "to create a sturdy base, then weave them together "
                "to make a vase.")
        self.assertFalse(exact_judge(Q, GT, junk))


class DemandNounAdapterTests(unittest.TestCase):
    def _ingest(self, **kw):
        ad = LongMemEvalAdapter(**kw)
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [{"role": "assistant", "content": m}
                           for m in DIY_MSGS]}])
        return ad

    def test_adapter_gate_wired(self):
        ad = self._ingest()
        ans, meta = ad.answer_extractive(Q, "")
        self.assertEqual(ans, EXPECTED)
        self.assertEqual(meta.get("gate"), "demand_noun")

    def test_adapter_flag_off_falls_through(self):
        ad = self._ingest(demand_noun_recall=False)
        ans, meta = ad.answer_extractive(Q, "")
        self.assertNotEqual(meta.get("gate"), "demand_noun")


if __name__ == "__main__":
    unittest.main()
