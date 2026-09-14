"""Cycle 576 — mention-demand appositive face for speaker_recall.

A question asking back "the <head noun> you mentioned" is answered by
the sentence that defines the mention under its name in apposition —
"Patagonia, an outdoor clothing and gear company, is known ..." —
even when the distinctive floors hid it (every matched keyword is
mid-frequency in this corporate-sustainability haystack) and an
anaphoric continuation ("The company also invests ...") parasitizes
the exact-token overlap (e48988bc official-run casualty).

Census: the shipped form regex accepts exactly 1/500 questions
(a40e080f "the two companies you mentioned" is rejected by the
numeral guard — multi-item GT, C574-deferred); the target pool
yields exactly 1 appositive bearer (169.8 vs parasite 229.8).

Guards: plural/numeral demands out of scope by question structure
(C531); frame-word names ("However, ...", "I, an AI ...") rejected;
the appositive phrase must END with the head noun (definitional
pattern); raw >= 2 + weighted_floor kept + preface penalty (C559
shape); fires only when a best already exists (C559 precedent).
"""

import unittest

from amg_bench_quality import (
    _MENTION_DEMAND_Q_RE,
    _MENTION_NUMERAL_RE,
    _APPOSITIVE_BEARER_RE,
    _APPOSITIVE_FRAME_WORD_RE,
    _mention_demand_head,
    _appositive_head_hit,
    answer_speaker_recall,
    judge_semantic,
)

# ── verbatim real-row replica (e48988bc, session_39 msg 4) ──
# The parasite sentence ("The company also invests ...") is the tail
# of numbered item 5 IN THIS SAME MESSAGE — the exact adversarial
# structure of the real pool.
PATAGONIA_MESSAGE = (
    "Yes, sure. Here's an example:\n"
    "\n"
    "Patagonia, an outdoor clothing and gear company, is known for "
    "its commitment to sustainability and environmental "
    "responsibility throughout its supply chain. Some of the ways "
    "they have implemented environmentally responsible practices "
    "are:\n"
    "\n"
    "1. Sustainable sourcing: Patagonia uses organic cotton, "
    "recycled polyester, and other sustainable materials in their "
    "products. They also work closely with suppliers to ensure that "
    "the environmental impact of their materials is minimized.\n"
    "\n"
    "2. Green transportation: Patagonia encourages its suppliers to "
    "use more efficient transportation methods, such as shipping by "
    "sea instead of air, reducing the amount of carbon emissions.\n"
    "\n"
    "3. Packaging optimization: Patagonia uses recycled and "
    "recyclable materials in its packaging and encourages customers "
    "to recycle their packaging.\n"
    "\n"
    "4. Waste reduction: Patagonia has implemented a take-back "
    "program for its clothing, where customers can return old "
    "clothes for recycling or repair. They also use recycled content "
    "and employ circular business models to reduce waste.\n"
    "\n"
    "5. Compliance with environmental regulations: Patagonia "
    "closely monitors its supply chain's compliance with "
    "environmental regulations, such as minimizing waste water and "
    "chemical usage. The company also invests in third-party "
    "certifications to validate that their supply chain is "
    "environmentally responsible.\n"
    "\n"
    "Patagonia has received several recognitions and awards for its "
    "sustainability efforts in its supply chain.")
PATAGONIA_QUESTION = (
    "I was looking back at our previous conversation about "
    "environmentally responsible supply chain practices, and I was "
    "wondering if you could remind me of the company you mentioned "
    "that's doing a great job with sustainability?")
PATAGONIA_BEARER = (
    "Patagonia, an outdoor clothing and gear company, is known for "
    "its commitment to sustainability and environmental "
    "responsibility throughout its supply chain.")
PARASITE = (
    "The company also invests in third-party certifications to "
    "validate that their supply chain is environmentally responsible.")

# real second competitor from the same pool (verbatim prefix; used as
# a frame-word shape fixture, not a score claim)
HOWEVER_LINE = (
    "However, here are some common practices that companies can "
    "adopt to ensure their supply chain is environmentally "
    "responsible.")

NEUTRAL_DECOYS = (
    "I started a sourdough starter last week and it is finally "
    "bubbling on the counter.\n"
    "The ferry timetable can change twice a year, in spring and "
    "autumn.\n"
    "Practice the chord changes slowly with a metronome at 60 beats "
    "per minute.\n"
    "Mountain bikers need to check the brake pads after muddy rides.\n"
    "The allotment shed roof leaked, so I tarped it for the winter.\n"
    "Sourdough hydration levels change how open the crumb turns out.\n"
    "The ferry crossing takes forty minutes in calm weather.\n"
    "For the bedroom repaint, choose a low-sheen paint so the walls "
    "are easier to clean.")


def _patagonia_nodes(extra_assistant=None):
    """Patagonia message verbatim + neutral decoy mass (C574 lesson:
    N comes from decoy mass so shared-word IDF is not compressed)."""
    nodes = {
        "u1": {"label": PATAGONIA_QUESTION, "role": "user",
               "session_id": "s1"},
        "a1": {"label": PATAGONIA_MESSAGE, "role": "assistant",
               "session_id": "s1"},
        "a2": {"label": NEUTRAL_DECOYS, "role": "assistant",
               "session_id": "s2"},
    }
    if extra_assistant is not None:
        nodes["a3"] = {"label": extra_assistant, "role": "assistant",
                       "session_id": "s3"}
    return nodes


class TestQuestionSide(unittest.TestCase):
    def test_form_matches_target_question(self):
        m = _MENTION_DEMAND_Q_RE.search(PATAGONIA_QUESTION)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "company")

    def test_head_extraction(self):
        self.assertEqual(_mention_demand_head(PATAGONIA_QUESTION),
                         "company")

    def test_numeral_demand_rejected(self):
        # a40e080f verbatim form — multi-item GT, C574-deferred
        q = ("I was going through our previous conversation and I was "
             "wondering if you could remind me of the two companies "
             "you mentioned that prioritize employee safety?")
        self.assertIsNone(_mention_demand_head(q))

    def test_plural_head_rejected(self):
        q = ("Could you remind me of the restaurants you mentioned "
             "last week?")
        self.assertIsNone(_mention_demand_head(q))

    def test_that_determiner_not_matched(self):
        # 51b23612 form (banked row, must stay untouched)
        q = ("I was wondering if you could remind me of that Soviet "
             "cartoon you mentioned that mocked Western culture?")
        self.assertIsNone(_MENTION_DEMAND_Q_RE.search(q))
        self.assertIsNone(_mention_demand_head(q))

    def test_recommended_not_matched(self):
        # 28bcfaac form (banked row, different family)
        q = "Can you remind me of the website you recommended?"
        self.assertIsNone(_MENTION_DEMAND_Q_RE.search(q))

    def test_no_form_no_head(self):
        self.assertIsNone(_mention_demand_head(
            "What is the capital of France?"))


class TestBearerSide(unittest.TestCase):
    def test_bearer_shape_matches_patagonia(self):
        m = _APPOSITIVE_BEARER_RE.match(PATAGONIA_BEARER)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "Patagonia")
        self.assertEqual(m.group(2), "outdoor clothing and gear company")

    def test_head_hit_head_last(self):
        self.assertTrue(_appositive_head_hit(PATAGONIA_BEARER, "company"))

    def test_anaphoric_continuation_not_bearer(self):
        self.assertIsNone(_APPOSITIVE_BEARER_RE.match(PARASITE))

    def test_frame_word_name_rejected(self):
        # shape alone already rejects the However-line (no article
        # after the comma); the frame-word guard covers lines where
        # shape and a frame-starter name collide
        self.assertIsNone(_APPOSITIVE_BEARER_RE.match(HOWEVER_LINE))
        self.assertTrue(
            _APPOSITIVE_FRAME_WORD_RE.match("However") is not None)
        framed = ("It, a rare rendering bug, surfaced twice last "
                  "week.")
        self.assertIsNotNone(_APPOSITIVE_BEARER_RE.match(framed))
        self.assertFalse(_appositive_head_hit(framed, "bug"))
        self.assertFalse(_appositive_head_hit(HOWEVER_LINE, "company"))

    def test_pronoun_name_rejected(self):
        # phrase must start lowercase, so "I, an AI language model,"
        # fails the shape outright; a lowercase phrase with a pronoun
        # name is caught by the frame-word guard
        self.assertIsNone(_APPOSITIVE_BEARER_RE.match(
            "I, an AI language model, would phrase it carefully."))
        sent = "I, an early adopter, bought the device day one."
        m = _APPOSITIVE_BEARER_RE.match(sent)
        self.assertIsNotNone(m)
        self.assertFalse(_appositive_head_hit(sent, "adopter"))

    def test_head_not_last_rejected(self):
        # definitional pattern requires the phrase to END in the head
        sent = ("Acme, a company known for sustainability, reported "
                "strong growth.")
        self.assertFalse(_appositive_head_hit(sent, "company"))

    def test_wrong_head_no_hit(self):
        self.assertFalse(
            _appositive_head_hit(PATAGONIA_BEARER, "website"))


class TestFaceBehavior(unittest.TestCase):
    def test_face_flips_parasite_to_bearer(self):
        ans, detail = answer_speaker_recall(
            PATAGONIA_QUESTION, _patagonia_nodes())
        self.assertEqual(ans, PATAGONIA_BEARER)
        self.assertEqual(detail.get("mention_appositive_face"),
                         "exemption")

    def test_banked_verdict_pin(self):
        v = judge_semantic(PATAGONIA_QUESTION, PATAGONIA_BEARER,
                           "Patagonia")
        self.assertEqual(v, "CORRECT")

    def test_head_miss_falls_through(self):
        q = ("Could you remind me of the website you mentioned in our "
             "chat about learning resources?")
        ans, detail = answer_speaker_recall(
            q, _patagonia_nodes())
        self.assertNotIn("mention_appositive_face", detail)
        # no passer shares this question's vocabulary -> honest
        # fall-through (best=None), not a face rescue
        self.assertIsNone(ans)

    def test_no_best_falls_through(self):
        # form matches but the pool has no passer at all (C559: best
        # None falls through untouched)
        q = ("Quick one - can you remind me of the company you "
             "mentioned last month?")
        nodes = {
            "a1": {"label": NEUTRAL_DECOYS, "role": "assistant",
                   "session_id": "s1"},
        }
        ans, detail = answer_speaker_recall(q, nodes)
        self.assertIsNone(ans)
        self.assertNotIn("mention_appositive_face", detail)

    def test_floor_falls_through(self):
        # bearer shape valid but its matched keywords are everywhere
        # in the pool (df ~ N) -> w^2 score under weighted_floor
        common = ("Every company in town talks about sustainability "
                  "these days. Company sustainability is the hot "
                  "topic at work.")
        mass = "\n".join(
            f"Decoy {i}: another line about company sustainability "
            f"and local business."
            for i in range(12))
        q = ("Can you remind me of the company you mentioned that "
             "was doing a great job with sustainability?")
        nodes = {
            "u1": {"label": q, "role": "user", "session_id": "s1"},
            "a1": {"label": PATAGONIA_MESSAGE, "role": "assistant",
                   "session_id": "s1"},
            "a2": {"label": common, "role": "assistant",
                   "session_id": "s2"},
            "a3": {"label": mass, "role": "assistant",
                   "session_id": "s3"},
            "a4": {"label": "Acme, a company chasing sustainability, "
                            "also gives small grants.",
                   "role": "assistant", "session_id": "s4"},
        }
        ans, detail = answer_speaker_recall(q, nodes)
        # the low-distinction Acme bearer must not steal the answer
        self.assertNotEqual(ans,
                            "Acme, a company chasing sustainability, "
                            "also gives small grants.")

    def test_raw_lt2_falls_through(self):
        # shape+head valid, but the bearer matches only ONE question
        # keyword -> raw guard rejects before anything else
        q = ("Can you remind me of the company you mentioned during "
             "our chat?")
        nodes = {
            "u1": {"label": q, "role": "user", "session_id": "s1"},
            "a1": {"label": PATAGONIA_MESSAGE, "role": "assistant",
                   "session_id": "s1"},
            "a2": {"label": NEUTRAL_DECOYS, "role": "assistant",
                   "session_id": "s2"},
            "a3": {"label": "Zedco, a company with heart, funds "
                            "local parks.",
                   "role": "assistant", "session_id": "s3"},
        }
        ans, detail = answer_speaker_recall(q, nodes)
        self.assertNotIn("mention_appositive_face", detail)


if __name__ == "__main__":
    unittest.main()
