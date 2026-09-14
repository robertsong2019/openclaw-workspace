"""Cycle 575 — list-body faces for speaker_recall (paren-count + adjacent-name).

Two faces reading structured bullet lists the way the C537/C534/C559/C574
faces read prose:

* paren-count face (18dcd5a5): "how many mummies will the party face"
  is answered by the stat-block row "* Mummies (4):" — the row IS the
  count fact. The bearer matched=1 ("mummies") under the min_raw=3
  floor while a 'user acquisition by 500%' marketing line parasitized
  the C534 digit-demand tier (109.2). New exemption class: paren-row
  shape + noun keyword match (>=1, distinctive-df and weighted_floor
  kept), answers with the bare count.
* adjacent-name face (e3fc4d6e): "who is the President's Chief Advisor
  for Science and Technology" — the name row "* Dr. Arati Prabhakar"
  has raw=0 lexical evidence (the question names the TITLE one row
  below), while the "Lawrence Livermore National Laboratory (LLNL)"
  row parasitized 296.1. Join = bullet description row (>=2 matched
  keywords, distinctive-df and weighted_floor kept) whose same-message
  neighbor row is a bare person-name fragment; the answer is
  reassembled from the source line (the <=10-char sentence filter
  drops "* Dr." from the pool fragment).

Census: who-is-the form = exactly 1 question of the frozen 500;
how-many x speaker_recall-routed = exactly 3 (target + 2 verified
paren-row-free pools).
"""

import unittest

from amg_bench_quality import (
    _LIST_PAREN_ROW_RE,
    _LIST_NAME_ROW_RE,
    _LIST_ORG_WORD_RE,
    _WHO_TITLE_Q_RE,
    _list_row_full,
    answer_speaker_recall,
)

# ── verbatim real-row replicas (18dcd5a5, answer session) ──
DJINN_MESSAGE = (
    '"The Lost Temple of the Djinn"\n'
    "\n"
    "Ages ago, a powerful Djinn named Zoltar ruled over a vast temple "
    "filled with treasures and magical artifacts. Zoltar was a just "
    "ruler and the temple flourished under his rule. But as time "
    "passed, Zoltar disappeared and the temple was lost to the sands "
    "of time.\n"
    "\n"
    "Now, a wealthy collector has hired the party to retrieve an "
    "artifact from the lost temple. The collector has located the "
    "temple and believes the artifact to be located within its walls, "
    "but he doesn't have the power to retrieve it himself.\n"
    "\n"
    "Upon arriving at the temple, the party must navigate through a "
    "series of traps and puzzles to reach the artifact. The temple is "
    "filled with mummies, undead warriors, and constructs guarding its "
    "treasures.\n"
    "\n"
    "Here are the stat blocks for the enemies the party will face:\n"
    "\n"
    "* Mummies (4):\n"
    "\t+ Armor Class: 11\n"
    "\t+ Hit Points: 45 (6d8 + 18)\n"
    "\t+ Speed: 20 ft.\n"
    "\t+ Damage Immunity: Poison, Psychicical\n"
    "\t+ Condition Immunity: Charmed, Exhaustion, Frightened, "
    "Paralyzed, Petrified, Poisoned\n"
    "* Construct Guardians (2):\n"
    "\t+ Armor Class: 14\n"
    "* Skeletal Warriors (6):\n"
    "\t+ Armor Class: 9\n")
MARKETING_PARASITE = (
    "Our marketing expert, [Marketing Expert's Name], has a strong "
    "background in growth hacking and has increased user acquisition "
    "by 500% in her previous role.")
DJINN_QUESTION = (
    "I'm going back to our previous chat about the Lost Temple of the "
    "Djinn one-shot. Can you remind me how many mummies the party will "
    "face in the temple?")

# ── verbatim real-row replicas (e3fc4d6e, answer session list) ──
FUSION_ARTICLE_USER = (
    "predict the entities of this article one sentence by a time:\n"
    "For First Time, Researchers Produce More Energy from Fusion Than "
    "Was Used to Drive It, Promising Further Discovery in Clean Power "
    "and Nuclear Weapons Stewardship\n"
    "WASHINGTON, D.C. — The U.S. Department of Energy (DOE) and DOE's "
    "National Nuclear Security Administration (NNSA) today announced "
    "the achievement of fusion ignition at Lawrence Livermore National "
    "Laboratory (LLNL).")
FUSION_ENTITY_LIST = (
    "* First Time\n"
    "* Researchers\n"
    "* Fusion\n"
    "* Energy\n"
    "* Used to Drive It\n"
    "* Promising Further Discovery\n"
    "* Clean Power\n"
    "* Nuclear Weapons Stewardship\n"
    "* U.S. Department of Energy (DOE)\n"
    "* DOE's National Nuclear Security Administration (NNSA)\n"
    "* Lawrence Livermore National Laboratory (LLNL)\n"
    "* Scientific Breakthrough\n"
    "* National Defense\n"
    "* Future of Clean Power\n"
    "* Controlled Fusion Experiment\n"
    "* Scientific Energy Breakeven\n"
    "* Laser Energy\n"
    "* National Ignition Facility (NIF)\n"
    "* U.S. Secretary of Energy Jennifer M. Granholm\n"
    "* Biden-Harris Administration\n"
    "* Scientists\n"
    "* Climate Change\n"
    "* Nuclear Deterrent\n"
    "* Nuclear Testing\n"
    "* Theoretical Understanding of Fusion\n"
    "* Dr. Arati Prabhakar\n"
    "* President's Chief Advisor for Science and Technology\n"
    "* Director of the White House Office of Science and Technology "
    "Policy\n"
    "* NNSA Administrator Jill Hruby\n"
    "* Members of Congress\n"
    "* National Ignition Facility\n"
    "* DOE National Laboratories\n"
    "* International Partners\n"
    "* LLNL Director Dr. Kim Budil\n"
    "* Scientific Challenges\n"
    "* Science\n"
    "* Engineering\n"
    "* People\n"
    "* 60 Years\n"
    "* Dedicated Pursuit\n"
    "* Learning\n"
    "* Building\n"
    "* Expanding Knowledge\n"
    "* Capability\n"
    "* Overcoming New Challenges\n"
    "* U.S. National Laboratories")
FUSION_QUESTION = (
    "I wanted to follow up on our previous conversation about the "
    "fusion breakthrough at Lawrence Livermore National Laboratory. "
    "Can you remind me who is the President's Chief Advisor for "
    "Science and Technology mentioned in the article?")

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


def _djinn_nodes(with_mummy_row=True):
    """Marketing parasite line + neutral decoys (assistant pool), the
    Djinn one-shot message verbatim. N comes from the decoy mass —
    C574 lesson: tiny pools compress shared-word IDF and distort
    floors."""
    djinn = DJINN_MESSAGE if with_mummy_row else (
        DJINN_MESSAGE.replace("* Mummies (4):\n", "* Mummies:\n"))
    return {
        "u1": {"label": DJINN_QUESTION, "role": "user",
               "session_id": "s1"},
        "a1": {"label": djinn, "role": "assistant", "session_id": "s1"},
        "a2": {"label": MARKETING_PARASITE, "role": "assistant",
               "session_id": "s2"},
        "a3": {"label": NEUTRAL_DECOYS, "role": "assistant",
               "session_id": "s3"},
    }


def _fusion_nodes(name_row=True, split_across_nodes=False):
    """The entity-extraction list verbatim. split_across_nodes cuts
    the list between the name row and the title row into two messages
    (adjacency guard)."""
    if split_across_nodes:
        head, tail = FUSION_ENTITY_LIST.split(
            "* President's Chief Advisor for Science and Technology")
        # head ends with the name row; tail starts with the title row
        node_head = head
        node_tail = "* President's Chief Advisor for Science and " \
                    "Technology" + tail
    else:
        node_head = FUSION_ENTITY_LIST
        node_tail = None
    name_node = node_head if name_row else node_head.replace(
        "* Dr. Arati Prabhakar\n", "")
    nodes = {
        "u1": {"label": FUSION_ARTICLE_USER, "role": "user",
               "session_id": "s1"},
    }
    if split_across_nodes:
        nodes["a1"] = {"label": node_head, "role": "assistant",
                       "session_id": "s1"}
        nodes["a2"] = {"label": node_tail, "role": "assistant",
                       "session_id": "s1"}
    else:
        nodes["a1"] = {"label": name_node, "role": "assistant",
                       "session_id": "s1"}
    nodes["a3"] = {"label": NEUTRAL_DECOYS, "role": "assistant",
                   "session_id": "s3"}
    return nodes


class TestRegexes(unittest.TestCase):
    def test_paren_row_matches_stat_row(self):
        m = _LIST_PAREN_ROW_RE.match("* Mummies (4):")
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), "Mummies")
        self.assertEqual(m.group(2), "4")

    def test_paren_row_rejects_prose_and_subbullets(self):
        self.assertIsNone(_LIST_PAREN_ROW_RE.match(
            "\t+ Hit Points: 45 (6d8 + 18)"))
        self.assertIsNone(_LIST_PAREN_ROW_RE.match(
            "The temple is filled with mummies (undead), warriors."))
        self.assertIsNone(_LIST_PAREN_ROW_RE.match(
            "* Armor Class: 11"))
        self.assertIsNone(_LIST_PAREN_ROW_RE.match(
            "* Skeletal Warriors (six):"))

    def test_name_row_shape(self):
        self.assertTrue(_LIST_NAME_ROW_RE.match("Arati Prabhakar"))
        self.assertTrue(_LIST_NAME_ROW_RE.match("Jill Hruby"))
        # lowercase words break the capitalized run
        self.assertIsNone(_LIST_NAME_ROW_RE.match(
            "President's Chief Advisor for Science and Technology"))
        self.assertIsNone(_LIST_NAME_ROW_RE.match(
            "Director of the White House Office"))
        # single word (no pair) fails the {1,3} run
        self.assertIsNone(_LIST_NAME_ROW_RE.match("Scientists"))
        # punctuation residue fails
        self.assertIsNone(_LIST_NAME_ROW_RE.match("LLNL Director Dr."))
        self.assertIsNone(_LIST_NAME_ROW_RE.match(
            "National Ignition Facility (NIF)"))

    def test_org_word_rejects_institution_rows(self):
        self.assertTrue(_LIST_ORG_WORD_RE.search(
            "DOE's National Nuclear Security Administration"))
        self.assertTrue(_LIST_ORG_WORD_RE.search(
            "Biden-Harris Administration"))
        self.assertTrue(_LIST_ORG_WORD_RE.search(
            "National Ignition Facility"))
        self.assertFalse(_LIST_ORG_WORD_RE.search("Arati Prabhakar"))

    def test_who_title_form(self):
        self.assertTrue(_WHO_TITLE_Q_RE.search(FUSION_QUESTION))
        self.assertFalse(_WHO_TITLE_Q_RE.search(DJINN_QUESTION))

    def test_row_reassembly_from_source(self):
        full = _list_row_full(FUSION_ENTITY_LIST, "Arati Prabhakar")
        self.assertEqual(full, "Dr. Arati Prabhakar")
        # fragment not found -> returned unchanged
        self.assertEqual(_list_row_full("no such line", "Zed"), "Zed")


class TestParenCountFace(unittest.TestCase):
    def test_face_answers_bare_count(self):
        ans, det = answer_speaker_recall(DJINN_QUESTION, _djinn_nodes())
        self.assertEqual(ans, "4")
        self.assertEqual(det.get("paren_count_face"), "exemption")

    def test_no_paren_row_no_fire(self):
        ans, det = answer_speaker_recall(DJINN_QUESTION,
                                         _djinn_nodes(with_mummy_row=False))
        self.assertNotIn("paren_count_face", det)
        self.assertNotEqual(ans, "4")

    def test_zero_keyword_noun_no_fire(self):
        # remove the question's noun anchor from the row: mummies no
        # longer anywhere near a paren row -> face stays silent
        nodes = _djinn_nodes()
        nodes["a1"]["label"] = DJINN_MESSAGE.replace(
            "* Mummies (4):", "* Blighted Zombies (4):")
        ans, det = answer_speaker_recall(DJINN_QUESTION, nodes)
        self.assertNotIn("paren_count_face", det)

    def test_distinctive_guard_blocks_common_noun(self):
        # distinctive_df=0: every matched noun has df>=1 -> excluded
        ans, det = answer_speaker_recall(DJINN_QUESTION, _djinn_nodes(),
                                         distinctive_df=0)
        self.assertNotIn("paren_count_face", det)

    def test_floor_kept(self):
        ans, det = answer_speaker_recall(DJINN_QUESTION, _djinn_nodes(),
                                         weighted_floor=10_000.0)
        self.assertNotIn("paren_count_face", det)

    def test_requires_existing_best(self):
        # assistant pool with only questions -> no best -> face silent
        nodes = {
            "u1": {"label": DJINN_QUESTION, "role": "user",
                   "session_id": "s1"},
            "a1": {"label": "* Mummies (4):\nHow many mummies?",
                   "role": "assistant", "session_id": "s1"},
        }
        ans, det = answer_speaker_recall(DJINN_QUESTION, nodes)
        self.assertNotIn("paren_count_face", det)


class TestAdjacentNameFace(unittest.TestCase):
    def test_face_answers_full_source_row(self):
        ans, det = answer_speaker_recall(FUSION_QUESTION, _fusion_nodes())
        self.assertEqual(ans, "Dr. Arati Prabhakar")
        self.assertEqual(det.get("adjacent_name_face"), "exemption")

    def test_nnsa_pair_rejected(self):
        # the LLNL desc row's neighbor is an institution row -> the
        # only surviving pair must be the Prabhakar one
        ans, det = answer_speaker_recall(FUSION_QUESTION, _fusion_nodes())
        self.assertNotEqual(
            ans, "DOE's National Nuclear Security Administration (NNSA)")

    def test_split_nodes_no_adjacency(self):
        # name row and title row in DIFFERENT messages -> no pair
        ans, det = answer_speaker_recall(
            FUSION_QUESTION, _fusion_nodes(split_across_nodes=True))
        self.assertNotIn("adjacent_name_face", det)
        self.assertNotEqual(ans, "Dr. Arati Prabhakar")

    def test_no_name_neighbor_no_fire(self):
        ans, det = answer_speaker_recall(FUSION_QUESTION,
                                         _fusion_nodes(name_row=False))
        self.assertNotIn("adjacent_name_face", det)

    def test_who_form_required(self):
        ans, det = answer_speaker_recall(DJINN_QUESTION, _fusion_nodes())
        self.assertNotIn("adjacent_name_face", det)


if __name__ == "__main__":
    unittest.main()
