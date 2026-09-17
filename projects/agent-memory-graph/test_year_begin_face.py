"""Cycle 585 - year-begin recall face (year_begin gate).

"...Can you remind me what year the construction of the house began?"
is answered by the graph sentence carrying the begin-verb + "in <YEAR>"
pattern ANCHORED by the demand noun phrase: every content word of the
NP between "what year" and the demand verb must appear in the evidence
sentence (the C584 structural-hard-filter lesson applied to year
extraction).

Design notes:
- evidence surface is BOTH roles: the fact was stated by the user
  (pasted case summary), so unlike the chord/sectioned faces there is
  NO user-role wall; the NP anchor plus the begin-verb+in+<YEAR>
  pattern bound the hijack surface instead (census: form accepts
  exactly 1/500 question - 5809eb10 - and the full 500 contains NO
  other "what year" question at all);
- uniqueness gate: >1 distinct anchored year across the graph =
  ambiguous = fall-through (ambiguity is fabrication);
- render is the bare year; GT "2014." judge-normalizes to "2014".

Fixture: verbatim user message from 5809eb10's answer session
(answer_sharegpt_4aJsGCH_0), repr-injected by the step3 generator.
"""

import unittest

from amg_bench_quality import (
    LongMemEvalAdapter,
    answer_year_begin,
    exact_judge,
    judge_semantic,
    year_begin_form,
)

Q = "I'm looking back at our previous conversation about the Bajimaya v Reward Homes Pty Ltd case. Can you remind me what year the construction of the house began?"
GT = "2014"
EV0 = 'I am optimising a case summary article. I want you to remember this case. If you understand, just say "acknowledged". Bajimaya v Reward Homes Pty Ltd - Case Summary\n\nThe case of Bajimaya v Reward Homes Pty Ltd [2021] NSWCATAP 297 highlights the importance of understanding your rights as a homeowner in the construction process. Homeowners invest a significant amount of time and money into building their dream homes, and it is essential to have legal protection to ensure that their investment is safeguarded. This article provides a comprehensive analysis of the case, focusing on the legal issues involved, the decision made by the court, and the lessons that homeowners can learn from it.\n\nBackground:\nThe background of the case involves the construction of a new home in New South Wales, Australia, by the plaintiff, Mr. Bajimaya, and the defendant, Reward Homes Pty Ltd. The construction of the house began in 2014, and the contract was signed between the parties in 2015. The agreement stated that the construction would be completed by October 2015, but the defendant failed to finish the work within the agreed timeframe.\n\nAfter several delays, the plaintiff received the keys to the house in December 2016, but he soon noticed several defects in the construction, including incomplete works, poor workmanship, and non-compliance with the building code. The plaintiff notified the defendant of these defects and requested rectification, but the defendant failed to address them promptly. The plaintiff then sought legal action against the defendant, claiming compensation for the cost of rectification and other damages.\nLegal Issues and Analysis\n\nThe legal issues in the case of Bajimaya v Reward Homes Pty Ltd [2021] NSWCATAP 297 primarily centered around whether the builder had breached its contractual obligations to the homeowner, Mr. Bajimaya, and whether Mr. Bajimaya was entitled to compensation for the defects in the construction of his home.\n\nThe tribunal found that Reward Homes Pty Ltd had breached its contract with Mr. Bajimaya by failing to complete the work in a proper and workmanlike manner, failing to comply with the plans and specifications, and failing to comply with the Building Code of Australia. Specifically, the tribunal found that the workmanship was of a poor standard, there were defects in the waterproofing, tiling, and brickwork, and the home was not constructed in accordance with the approved plans.\n\nThe tribunal also found that Mr. Bajimaya was entitled to compensation for the defects in his home. The compensation included the cost of rectifying the defects, the cost of alternate accommodation, and a deduction in the purchase price of the property due to the defects.\n\nThe analysis of the legal issues in this case highlights the importance of having a clear and comprehensive contract between the homeowner and the builder, as well as ensuring that the work is completed in accordance with the plans and specifications and in compliance with the Building Code of Australia. It also emphasizes the need for homeowners to seek legal advice and representation when dealing with disputes with builders or construction companies.\n\nKey Takeaways\n\nThe case of Bajimaya v Reward Homes Pty Ltd [2021] NSWCATAP 297 highlights some important lessons that can be learned by both homeowners and builders. One of the key takeaways is the importance of understanding building contracts and warranties. Homeowners must ensure that they fully understand the terms of the building contract and that all the necessary warranties are in place. Builders, on the other hand, should ensure that their contracts are clear and unambiguous, and that they have the necessary insurance to cover any defects or damage to the property.\n\nAnother important lesson that can be learned from this case is the importance of seeking legal advice before entering into construction contracts. A residential construction lawyer can review the contract and identify any clauses that may be unfair or unclear, as well as provide advice on the builder\'s obligations and the homeowner\'s rights. Seeking legal advice before entering into a contract can help to prevent disputes from arising and ensure that both parties are fully aware of their obligations and rights.\n\nV. Conclusion\n\nIn conclusion, the Bajimaya v Reward Homes Pty Ltd case highlights the importance of having a thorough understanding of building contracts and warranties in residential construction projects. The case also underscores the significance of seeking legal advice before entering into such contracts to avoid potential legal disputes.\n\nThe outcome of the case serves as a reminder that builders and homeowners alike should pay close attention to the details of their contracts, including any warranties and dispute resolution provisions. This ensures that both parties understand their respective rights and obligations, and that they can avoid disputes and costly litigation in the future.\n\nUltimately, the case underscores the importance of obtaining proper legal guidance from a residential construction lawyer to protect one\'s interests and to ensure that the terms of the contract are fair and reasonable. With proper legal advice, homeowners and builders can enter into construction contracts with greater confidence and peace of mind, knowing that they are protected in the event of a dispute.\n\nPlease write in English language.'


def _pool(*msgs):
    """[(role, content)] full-graph wire format (date-independent)."""
    return list(msgs)


class YearFormTests(unittest.TestCase):
    def test_form_accepts_target(self):
        self.assertEqual(year_begin_form(Q),
                         "the construction of the house")

    def test_form_direct_did_variant(self):
        self.assertEqual(year_begin_form(
            "Can you remind me what year did the construction of the "
            "house begin?"), "the construction of the house")

    def test_form_rejects_no_frame(self):
        self.assertIsNone(year_begin_form(
            "What year did the construction of the house begin?"))

    def test_form_rejects_no_begin_verb(self):
        self.assertIsNone(year_begin_form(
            "Can you remind me what year the contract was signed?"))

    def test_form_rejects_no_what_year(self):
        self.assertIsNone(year_begin_form(
            "Can you remind me when the construction of the house "
            "began?"))


class YearAnswerTests(unittest.TestCase):
    def test_target_rescued(self):
        pool = _pool(("user", EV0))
        ans, detail = answer_year_begin(Q, pool)
        self.assertEqual(ans, "2014")
        self.assertEqual(detail["form"], "year_begin")
        self.assertGreaterEqual(detail["candidates"], 1)

    def test_ambiguous_two_years_falls_through(self):
        second = ("Later context. The construction of the house began "
                  "in 2019 according to the revised filing.")
        pool = _pool(("user", EV0), ("assistant", second))
        ans, detail = answer_year_begin(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "ambiguous")

    def test_np_anchor_miss_falls_through(self):
        decoy = "The project began in 2014 and wrapped up on time."
        pool = _pool(("user", decoy))
        ans, detail = answer_year_begin(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_match")

    def test_no_year_evidence_falls_through(self):
        pool = _pool(("user", "The construction of the house began "
                              "well before the contract was signed."))
        ans, detail = answer_year_begin(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_match")

    def test_same_year_repeats_agree(self):
        echo = "As noted, the construction of the house began in 2014."
        pool = _pool(("user", EV0), ("assistant", echo))
        ans, _ = answer_year_begin(Q, pool)
        self.assertEqual(ans, "2014")

    def test_assistant_role_evidence_binds(self):
        pool = _pool(("assistant", EV0))
        ans, _ = answer_year_begin(Q, pool)
        self.assertEqual(ans, "2014")


class YearJudgePins(unittest.TestCase):
    """Pre-verified render -> judge contracts (frozen)."""

    def test_render_matches_gt_with_period(self):
        self.assertTrue(exact_judge(Q, "2014.", "2014"))

    def test_render_semantic_correct(self):
        self.assertEqual(judge_semantic(Q, "2014.", "2014"), "CORRECT")

    def test_parasitic_pred_stays_unbanked(self):
        parasitic = ("Bajimaya v Reward Homes Pty Ltd [2021] NSWCATAP "
                     "297 emphasizes the need for homeowners to "
                     "understand their rights during the construction "
                     "process.")
        self.assertFalse(exact_judge(Q, "2014.", parasitic))


class YearAdapterTests(unittest.TestCase):
    def test_adapter_gate_wired(self):
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
               "messages": [
                   {"role": "user", "content": EV0},
                   {"role": "assistant",
                     "content": "Acknowledged."}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertEqual(ans, "2014")
        self.assertEqual(meta.get("gate"), "year_begin")

    def test_adapter_flag_off_falls_through(self):
        ad = LongMemEvalAdapter(year_begin_recall=False)
        ad.ingest_sessions(
            [{"session_id": "session_1",
               "messages": [
                   {"role": "user", "content": EV0}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertNotEqual(meta.get("gate"), "year_begin")


if __name__ == "__main__":
    unittest.main()
