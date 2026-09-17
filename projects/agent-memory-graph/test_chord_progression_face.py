"""Cycle 584 - chord-progression face (chord_progression gate).

"...you created two sad songs for me. Can you remind me what was the
chord progression for the chorus in the second song?" is answered by
the assistant's own STRUCTURED song message: the face enumerates
assistant messages carrying "Chorus:" headers with a notes line
immediately after each, takes the ordinal-selected song, and renders
the chorus notes verbatim (judge-normalized equality with the GT).

Design notes:
- a chorus notes line is pure A-G pitch letters (>=3 notes,
  space-separated); lyric lines never bind;
- all "Chorus:" repeats inside the chosen song must agree (unique
  notes line) - disagreement = ambiguous = fall-through;
- user-role wall: song messages posted by the user role never bind.

Census: "chord progression" + "chorus" + "<ordinal> song" accepts
exactly 1/500 questions (eaca4986) - zero hijack surface by
construction. The current parasitic pred is a speaker_recall output
(the session_17 "Improved improvisation" advice line).
"""

import unittest

from amg_bench_quality import (
    LongMemEvalAdapter,
    answer_chord_progression,
    chord_progression_form,
    exact_judge,
    judge_semantic,
)

Q = "I'm looking back at our previous conversation where you created two sad songs for me. Can you remind me what was the chord progression for the chorus in the second song?"
GT = 'C D E F G A B A G F E D C'
SONG1 = "Here's a sad song with notes for you:\n\nVerse 1:\nC D E E E D C C\nThe rain falls down on me\nC D E E E D C C\nAs I stand alone, can't you see?\nC D E F E D C C\nThe tears mix with the rain\nC D E F E D C C\nAnd I feel this pain, again and again\n\nChorus:\nG G G G A G F\nWhy did you have to go?\nG G G G A G F\nLeaving me with this sorrow\nG G G G A G F\nI'll always be missing you\nG G G G A G F\nMy heart will never be new\n\nVerse 2:\nC D E E E D C C\nThe memories flood my mind\nC D E E E D C C\nOf the laughter we left behind\nC D E F E D C C\nBut now it's just emptiness\nC D E F E D C C\nI can't find my way, in this darkness\n\nChorus:\nG G G G A G F\nWhy did you have to go?\nG G G G A G F\nLeaving me with this sorrow\nG G G G A G F\nI'll always be missing you\nG G G G A G F\nMy heart will never be new\n\nBridge:\nG G A A B B A G\nI wish I could turn back time\nG G A A B B A G\nTo when you were still mine\nG G A A B B A G\nBut now I'm left with this pain\nG G A A B B A G\nAnd the memories that remain\n\nChorus:\nG G G G A G F\nWhy did you have to go?\nG G G G A G F\nLeaving me with this sorrow\nG G G G A G F\nI'll always be missing you\nG G G G A G F\nMy heart will never be new\n\nOutro:\nC D E E E D C C\nThe rain keeps falling down\nC D E E E D C C\nAnd I'm left to drown\nC D E F E D C C\nIn this sea of tears and pain\nC D E F E D C C\nAnd I'll never be the same."
SONG2 = "Sure, here's a more romantic and heart-felt song for you:\n\nVerse 1:\nG A B C D E D C B A G\nWhen I first saw you, my heart skipped a beat\nG A B C D E D C B A G\nI knew right then, you were someone I'd need\nG A B C D E D C B A G\nYou smiled at me, and my heart took flight\nG A B C D E D C B A G\nI knew in that moment, you were my light\n\nChorus:\nC D E F G A B A G F E D C\nYou're the one I want, the one I need\nC D E F G A B A G F E D C\nIn your eyes, I see my destiny\nC D E F G A B A G F E D C\nWith you by my side, I can face anything\nC D E F G A B A G F E D C\nForever and always, my heart will sing\n\nVerse 2:\nG A B C D E D C B A G\nYou bring color to my world, where there was none\nG A B C D E D C B A G\nYou make me feel alive, like the rising sun\nG A B C D E D C B A G\nYour touch ignites a flame, that never fades\nG A B C D E D C B A G\nWith you beside me, I'm unafraid\n\nChorus:\nC D E F G A B A G F E D C\nYou're the one I want, the one I need\nC D E F G A B A G F E D C\nIn your eyes, I see my destiny\nC D E F G A B A G F E D C\nWith you by my side, I can face anything\nC D E F G A B A G F E D C\nForever and always, my heart will sing\n\nBridge:\nG A B C D E F E D C B A G\nI promise to love you, for all time\nG A B C D E F E D C B A G\nTogether we'll weather any climb\nG A B C D E F E D C B A G\nOur love will be the light, that guides the way\nG A B C D E F E D C B A G\nTogether forever, come what may\n\nChorus:\nC D E F G A B A G F E D C\nYou're the one I want, the one I need\nC D E F G A B A G F E D C\nIn your eyes, I see my destiny\nC D E F G A B A G F E D C\nWith you by my side, I can face anything\nC D E F G A B A G F E D C\nForever and always, my heart will sing\n\nOutro:\nG A B C D E D C B A G\nI love you more, with every passing day\nG A B C D E D C B A G\nI'll always be here, no matter the way\nG A B C D E D C B A G\nForever and always, my heart is yours\nG A B C D E D C B A G\nMy love for you, forever endures."


def _pool(*msgs):
    """[(role, content)] full-graph wire format (date-independent)."""
    return list(msgs)


class ChordFormTests(unittest.TestCase):
    def test_form_accepts_target(self):
        self.assertEqual(chord_progression_form(Q), 1)

    def test_form_digit_ordinal(self):
        self.assertEqual(chord_progression_form(
            "Can you remind me what was the chord progression for "
            "the chorus in the 2nd song?"), 1)

    def test_form_rejects_no_chord_phrase(self):
        self.assertIsNone(chord_progression_form(
            "Can you remind me what was the melody for the chorus "
            "in the second song?"))

    def test_form_rejects_no_chorus(self):
        self.assertIsNone(chord_progression_form(
            "Can you remind me what was the chord progression for "
            "the bridge in the second song?"))

    def test_form_rejects_no_ordinal_song(self):
        self.assertIsNone(chord_progression_form(
            "Can you remind me what was the chord progression for "
            "the chorus?"))


class ChordAnswerTests(unittest.TestCase):
    def test_second_song_rescued(self):
        pool = _pool(("assistant", SONG1), ("assistant", SONG2))
        ans, detail = answer_chord_progression(Q, pool)
        self.assertEqual(ans, GT)
        self.assertEqual(detail["form"], "chord_progression")
        self.assertEqual(detail["songs"], 2)

    def test_first_song(self):
        pool = _pool(("assistant", SONG1), ("assistant", SONG2))
        q1 = Q.replace("second song", "first song")
        ans, detail = answer_chord_progression(q1, pool)
        self.assertEqual(ans, "G G G G A G F")

    def test_ordinal_out_of_range(self):
        pool = _pool(("assistant", SONG1), ("assistant", SONG2))
        q3 = Q.replace("second song", "third song")
        ans, detail = answer_chord_progression(q3, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_such_song")

    def test_inconsistent_chorus_falls_through(self):
        lines = SONG2.split("\n")
        idxs = [i for i, ln in enumerate(lines)
                if ln.strip() == "C D E F G A B A G F E D C"
                and lines[i - 1].strip().lower() == "chorus:"]
        assert len(idxs) >= 2
        lines[idxs[-1]] = "A A A A A A A"
        mutated = "\n".join(lines)
        pool = _pool(("assistant", SONG1), ("assistant", mutated))
        ans, detail = answer_chord_progression(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "inconsistent_chorus")

    def test_lyric_after_chorus_skipped(self):
        stripped = SONG2.replace(
            "Chorus:\nC D E F G A B A G F E D C",
            "Chorus:\nYou're the one I want, the one I need", 1)
        assert stripped != SONG2
        pool = _pool(("assistant", SONG1), ("assistant", stripped))
        ans, detail = answer_chord_progression(Q, pool)
        # 2 of 3 choruses still carry notes - they agree
        self.assertEqual(ans, GT)

    def test_no_chorus_message_falls_through(self):
        pool = _pool(("assistant", "A plain message about songs."))
        ans, detail = answer_chord_progression(Q, pool)
        self.assertIsNone(ans)
        self.assertEqual(detail["reason"], "no_such_song")

    def test_user_role_wall(self):
        pool = _pool(("user", SONG1), ("user", SONG2))
        ans, _ = answer_chord_progression(Q, pool)
        self.assertIsNone(ans)


class ChordJudgePins(unittest.TestCase):
    """Pre-verified render -> judge contracts (frozen)."""

    def test_render_exact(self):
        self.assertTrue(exact_judge(Q, GT, GT))

    def test_render_semantic_correct(self):
        self.assertEqual(judge_semantic(Q, GT, GT), "CORRECT")

    def test_parasitic_pred_stays_unbanked(self):
        parasitic = ("**Improved improvisation**: With a better "
                     "understanding of scales, modes, and chord "
                     "progressions, you'll be able to improvise more "
                     "confidently and create more coherent, musical "
                     "phrases.")
        self.assertFalse(exact_judge(Q, GT, parasitic))


class ChordAdapterTests(unittest.TestCase):
    def test_adapter_gate_wired(self):
        ad = LongMemEvalAdapter()
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "user", "content": "write me two sad songs"},
                  {"role": "assistant", "content": SONG1},
                  {"role": "user", "content": "one more, more romantic"},
                  {"role": "assistant", "content": SONG2}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertEqual(ans, GT)
        self.assertEqual(meta.get("gate"), "chord_progression")

    def test_adapter_flag_off_falls_through(self):
        ad = LongMemEvalAdapter(song_chord=False)
        ad.ingest_sessions(
            [{"session_id": "session_1",
              "messages": [
                  {"role": "assistant", "content": SONG1},
                  {"role": "assistant", "content": SONG2}]}])
        ans, meta = ad.answer_extractive(Q, "")
        self.assertNotEqual(meta.get("gate"), "chord_progression")


if __name__ == "__main__":
    unittest.main()
