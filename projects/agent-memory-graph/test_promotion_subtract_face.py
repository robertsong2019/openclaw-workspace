"""C564: promotion-subtract route (e) — current-role tenure with no
tenure line anywhere.

92a0aa75 ("How long have I been working in my current role?") —
route (c) needs an all-keywords now-suffixed tenure line; the row
has none, so the question fell through to the answer gate, which
echoed unrelated haystack FAQ text (garbage pred). The evidence is
two-hop: the company-experience total ("3 years and 9 months
experience in the company") minus the promotion span ("worked my
way up to Senior Marketing Specialist after 2 years and 4
months") = 1 year and 5 months in the current role.

Census (all 500): the strict head matches exactly one row
(unbanked); both evidence patterns exist in no other haystack.
Route (e) engages only after route (c) misses, requires BOTH
facts, a total > promo, and a role echo (the promoted-to role
re-stated as current in another user line) — otherwise honest
fall-through (None; the gate chain owns abstention).
"""

import unittest

from amg_bench_quality import (
    answer_pp_duration,
    pp_duration_judge,
    pp_pure_tenure_form,
)

CURROLE_Q = "How long have I been working in my current role?"

PROMO_SESSIONS = [
    ("2023-05-24", [
        {"role": "user", "content": (
            "I'm looking to create a presentation for an upcoming "
            "conference, and I need some help with designing the "
            "slides. By the way, I've been in marketing for a while "
            "now, started as a Marketing Coordinator and worked my "
            "way up to Senior Marketing Specialist after 2 years "
            "and 4 months. As a Senior Marketing Specialist, I've "
            "had to present to various audiences.")},
    ]),
    ("2023-05-28", [
        {"role": "user", "content": (
            "As a Senior Marketing Specialist in the company, I've "
            "been feeling a bit stuck. I've been thinking about my "
            "3 years and 9 months experience in the company and "
            "I've realized that I've built a strong understanding "
            "of our target audience.")},
    ]),
]


class TestPromotionSubtractFace(unittest.TestCase):

    def test_currole_promotion_subtract_rescue(self):
        """Route (e): total − promotion = current-role tenure."""
        ans, detail = answer_pp_duration(CURROLE_Q, PROMO_SESSIONS)
        self.assertEqual(ans, "1 year and 5 months")
        self.assertEqual(detail.get("route"), "promotion_subtract")

    def test_head_variants_position_job(self):
        """"current position" / "current job" heads route the same."""
        for q in ("How long have I been working in my current "
                  "position?",
                  "How long have I been working at my current "
                  "job?"):
            ans, detail = answer_pp_duration(q, PROMO_SESSIONS)
            self.assertEqual(ans, "1 year and 5 months", q)
            self.assertEqual(detail.get("route"),
                             "promotion_subtract", q)

    def test_route_c_still_wins_with_tenure_line(self):
        """A now-suffixed all-keywords tenure line keeps route (c)."""
        sessions = [
            ("2023-05-20", [
                {"role": "user", "content": (
                    "I have been working in my current role for "
                    "2 years now, and I enjoy it.")},
            ]),
        ] + PROMO_SESSIONS
        ans, detail = answer_pp_duration(CURROLE_Q, sessions)
        self.assertEqual(ans, "2 years")
        self.assertEqual(detail.get("route"), "pure_tenure")

    def test_no_promo_line_falls_through(self):
        """Total without promotion span → None (honest fall-through)."""
        sessions = [PROMO_SESSIONS[1]]
        ans, detail = answer_pp_duration(CURROLE_Q, sessions)
        self.assertIsNone(ans)
        self.assertEqual(detail.get("missing"), "tenure line")

    def test_no_total_line_falls_through(self):
        """Promotion span without total → None."""
        sessions = [PROMO_SESSIONS[0]]
        ans, detail = answer_pp_duration(CURROLE_Q, sessions)
        self.assertIsNone(ans)
        self.assertEqual(detail.get("missing"), "tenure line")

    def test_total_le_promo_no_fire(self):
        """total ≤ promotion is incoherent → None."""
        sessions = [
            ("2023-05-24", [
                {"role": "user", "content": (
                    "I started as a Marketing Coordinator and "
                    "worked my way up to Senior Marketing "
                    "Specialist after 2 years and 4 months. As a "
                    "Senior Marketing Specialist, I present a "
                    "lot.")},
            ]),
            ("2023-05-28", [
                {"role": "user", "content": (
                    "As a Senior Marketing Specialist in the "
                    "company, I've been thinking about my 2 years "
                    "and 1 month experience in the company.")},
            ]),
        ]
        ans, _ = answer_pp_duration(CURROLE_Q, sessions)
        self.assertIsNone(ans)

    def test_no_role_echo_no_fire(self):
        """Promoted-to role never re-stated as current → None."""
        sessions = [
            ("2023-05-24", [
                {"role": "user", "content": (
                    "I started as a Marketing Coordinator and "
                    "worked my way up to Senior Marketing "
                    "Specialist after 2 years and 4 months.")},
            ]),
            ("2023-05-28", [
                {"role": "user", "content": (
                    "I've been thinking about my 3 years and 9 "
                    "months experience in the company.")},
            ]),
        ]
        ans, _ = answer_pp_duration(CURROLE_Q, sessions)
        self.assertIsNone(ans)

    def test_non_working_current_head_not_engaged(self):
        """"living in my current apartment" must not route (e)."""
        ans, _ = answer_pp_duration(
            "How long have I been living in my current apartment "
            "in Harajuku?", PROMO_SESSIONS)
        self.assertIsNone(ans)

    def test_gate_form_pure_tenure_unchanged(self):
        """Gate routing already covers the head (sanity)."""
        self.assertTrue(pp_pure_tenure_form(CURROLE_Q))

    def test_judge_credits_canonical_render(self):
        self.assertTrue(pp_duration_judge(
            CURROLE_Q, "1 year and 5 months", "1 year and 5 months"))
        self.assertTrue(pp_duration_judge(
            CURROLE_Q, "1 year and 5 months",
            "one year and five months"))
        self.assertFalse(pp_duration_judge(
            CURROLE_Q, "1 year and 5 months", "3 years and 9 months"))


if __name__ == "__main__":
    unittest.main()
