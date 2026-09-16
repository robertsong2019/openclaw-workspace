"""C582 miniatures — where-face precision: do-form demotion scope (R2),
assistant-role demotion (R3).

Fixtures are verbatim forensic-dump sentences (probe /tmp/c582).
Red-first under C581 code: yoga_rescue + target_rescue FAIL.
"""
import unittest

from amg_bench_quality import (
    _where_intent_in_loc_clauses,
    answer_where,
)


YOGA_Q = "Where do I take yoga classes?"
EMILY_LINE = ("I'm actually planning to visit my friend Emily again, and "
              "I was thinking of taking a day trip to Bainbridge Island "
              "like last time.")
SERENITY_LINE = ("It's been super helpful for me, especially on days "
                 "when I can't make it to Serenity Yoga.")

TARGET_Q = "Where did I redeem a $5 coupon on coffee creamer?"
COUPON_ASSISTANT = ("**Handmade Coupon Book**: Create a book of coupons "
                    "that she can redeem for things like coffee creamer "
                    "at the Board Game Cafe.")
TARGET_LINE = ("I've been using the Cartwheel app from Target and it's "
               "been really helpful for saving money on household items.")

OAHU_Q = "Where am I planning to stay for my birthday trip to Hawaii?"
OAHU_LINE = ("I'm actually planning to stay on Oahu, so the Hanauma Bay "
             "Nature Preserve and Shark's Cove sound perfect for me.")

SNEAKERS_Q = "Where do I initially keep my old sneakers?"
SNEAKERS_LINE = ("By the way, I need to take care of my old sneakers, "
                 "I've been keeping them under my bed for storage, and "
                 "they're starting to smell.")


def _run(question, sessions):
    counting = [{"session_id": sid,
                 "turns": [{"role": role, "content": content}]}
                for sid, role, content in sessions]
    nids = [f"n{i}" for i in range(len(sessions))]
    nodes = {f"n{i}": {"session_id": sid}
             for i, (sid, _, _) in enumerate(sessions)}
    return answer_where(question, counting, nids, nodes, "")


class TestDoFormDemotion(unittest.TestCase):
    def test_yoga_rescue(self):
        ans, _ = _run(YOGA_Q, [("s46", "user", EMILY_LINE),
                               ("s51", "user", SERENITY_LINE)])
        self.assertIn("Serenity Yoga", ans)

    def test_am_form_untouched(self):
        # eace081b (banked): am-planning question keeps intent winner.
        ans, _ = _run(OAHU_Q, [("s40", "user", OAHU_LINE)])
        self.assertIn("Oahu", ans)

    def test_do_form_clean_winner_untouched(self):
        # 07741c44 (banked): clean winner survives demotion arming.
        ans, _ = _run(SNEAKERS_Q, [("s8", "user", SNEAKERS_LINE)])
        self.assertIn("under my bed", ans)

    def test_intent_check_unchanged(self):
        # C541 marking semantics untouched by C582 (R1 carve-out was
        # examined and reverted: affected lines are unretrieved).
        self.assertTrue(_where_intent_in_loc_clauses(EMILY_LINE))
        self.assertFalse(_where_intent_in_loc_clauses(SERENITY_LINE))


class TestAssistantRoleDemotion(unittest.TestCase):
    def test_target_rescue(self):
        ans, _ = _run(TARGET_Q, [("s37", "assistant", COUPON_ASSISTANT),
                                 ("s43", "user", TARGET_LINE)])
        self.assertIn("Target", ans)


if __name__ == "__main__":
    unittest.main()
