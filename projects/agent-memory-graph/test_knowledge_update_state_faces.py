# ════════ Cycle 587 (kd-2): knowledge-update state faces ════════
# Two heads, one mechanism — LATEST-SESSION-WINS state recall:
#   ku_reloc   "Where did <NAME> move to"  → 830ce83f (Rachel: city →
#              Chicago → the suburbs; GT is the LATEST state, s45)
#   ku_storage "Where do I CURRENTLY keep X" → 07741c45 (sneakers:
#              under my bed → shoe rack in closet; GT is the LATEST
#              state, s32)
# Evidence lines are VERBATIM dataset content (repr-injected by
# step5_gen_fixture.py). Banked-protection pin: the 'initially' twin
# (07741c44, GT 'under my bed', banked=True in C586 chain) is
# structurally OUT of the form — the recency word is a HARD
# requirement, not an optional modifier.
import pytest

from amg_bench_quality import (LongMemEvalAdapter,
                               ku_reloc_form,
                               ku_storage_form,
                               answer_ku_reloc,
                               answer_ku_storage,
                               exact_judge)

Q_RELOC = 'Where did Rachel move to after her recent relocation?'
Q_STOR = 'Where do I currently keep my old sneakers?'
Q_STOR_TWIN = 'Where do I initially keep my old sneakers?'

RACH_MID = [
        {"role": 'user', "content": "Hey! Random update from me today."},
        {"role": 'assistant', "content": "Sure, go ahead!"},
        {"role": 'user', "content": "I'm also thinking about visiting my friend Rachel who recently moved to a new apartment in the city. Do you know what the weather is like in the city this time of year?"},
        {"role": 'assistant', "content": 'Oh nice, how is she settling in?'},
        {"role": 'user', "content": 'She moved to Chicago.'},

]

RACH_LATEST = [
        {"role": 'user', "content": "Miami Beach sounds fun, but I've been there before. I'm thinking of somewhere more relaxed. My friend Rachel actually just moved back to the suburbs again, so I was thinking of somewhere not too far from a major city. Any suggestions?"},

]

STOR_OLD = [
        {"role": 'user', "content": "Hey! Random update from me today."},
        {"role": 'assistant', "content": "Sure, go ahead!"},
        {"role": 'user', "content": "I've heard of Teva and Merrell, they're great brands. I'll check out their latest collections. By the way, I need to take care of my old sneakers, I've been keeping them under my bed for storage, and they're starting to smell."},

]

STOR_NEW = [
        {"role": 'user', "content": "I'm thinking of buying a new pair of sandals with better quality straps. Can you recommend some good brands or stores that offer durable sandals? By the way, I need to organize my closet this weekend, and I'm looking forward to get rid of some of my old sneakers in a shoe rack in it, they're currently taking up space."},
        {"role": 'assistant', "content": 'Good luck with the closet cleanup!'},
        {"role": 'user', "content": "I'm thinking of getting a new pair of sandals with better quality straps. Can you recommend some good brands or stores that offer durable sandals? By the way, I need to organize my closet this weekend, and I'm looking forward to storing my old sneakers in a shoe rack, they're currently taking up space."},

]


def _ingest(*sessions, **kw):
    ad = LongMemEvalAdapter(**kw)
    ad.ingest_sessions([{"session_id": f"session_{i+1}",
                          "messages": list(s)}
                       for i, s in enumerate(sessions)])
    return ad


# ── form gates ──

def test_reloc_form_accept():
    assert ku_reloc_form(Q_RELOC) == "rachel"


def test_reloc_form_reject_no_move():
    assert ku_reloc_form("Where did Rachel use to live?") is None
    assert ku_reloc_form("Where does Rachel work?") is None


def test_storage_form_accept():
    assert ku_storage_form(Q_STOR) == "my old sneakers"


def test_storage_form_reject_initially_twin():
    # 07741c44 banked-protection pin: non-recency time words are OUT
    assert ku_storage_form(Q_STOR_TWIN) is None
    assert ku_storage_form("Where do I keep my old sneakers?") is None


# ── ku_reloc: latest-session-wins ──

def test_reloc_latest_session_wins():
    nodes = _ingest(RACH_MID, RACH_LATEST)._nodes
    ans, detail = answer_ku_reloc(Q_RELOC, nodes)
    assert ans is not None
    assert "the suburbs" in ans.lower()
    assert "chicago" not in ans.lower()
    assert "city" not in ans.lower()


def test_reloc_judge_containment():
    nodes = _ingest(RACH_MID, RACH_LATEST)._nodes
    ans, _ = answer_ku_reloc(Q_RELOC, nodes)
    assert exact_judge(Q_RELOC, "the suburbs", ans)


def test_reloc_pronoun_statement_excluded():
    # "She moved to Chicago." carries no name → contributes nothing
    # (no honest signal links it to the topic; no cross-sentence
    # pronoun chains). The face renders the latest NAME-ANCHORED
    # state — pinned so this never regresses into pronoun chaining.
    latest_pronoun = [
        {"role": 'user', "content": 'She moved to Chicago.'},
    ]
    nodes = _ingest(RACH_MID, latest_pronoun)._nodes
    ans, detail = answer_ku_reloc(Q_RELOC, nodes)
    assert ans == "a new apartment in the city"
    assert not any("chicago" in s["dest"].lower()
                   for s in detail["statements"])


def test_reloc_ambiguous_falls_through():
    # two distinct destinations in the LATEST session → fall-through
    mutated = [
        {"role": 'user', "content": "Miami Beach sounds fun, but I've been there before. I'm thinking of somewhere more relaxed. My friend Rachel actually just moved back to the suburbs again, so I was thinking of somewhere not too far from a major city. Any suggestions?"},
        {"role": 'user', "content": "Actually Rachel also said she moved to Portland last month."},
    ]
    nodes = _ingest(RACH_MID, mutated)._nodes
    ans, detail = answer_ku_reloc(Q_RELOC, nodes)
    assert ans is None
    assert detail["reason"] == "ambiguous"


def test_reloc_no_match_silent():
    nodes = _ingest(RACH_MID)._nodes
    # only intermediate state (city/chicago) → still renders city-era
    # dest? NO — old state is NOT the answer... but the face is
    # state-agnostic: it renders the latest AVAILABLE state. The
    # dataset truth for this qid has s45, so this only pins the
    # no-evidence-at-all case.
    nodes = _ingest([{"role": 'user', "content": "Totally unrelated chat about taxes."}])._nodes
    ans, detail = answer_ku_reloc(Q_RELOC, nodes)
    assert ans is None
    assert detail["reason"] == "no_match"


# ── ku_storage: anaphora + subsumption ──

def test_storage_expanded_render_wins():
    nodes = _ingest(STOR_OLD, STOR_NEW)._nodes
    ans, detail = answer_ku_storage(Q_STOR, nodes)
    assert ans is not None
    assert ans == "in a shoe rack in my closet"
    assert "under my bed" not in ans.lower()


def test_storage_judge_containment():
    nodes = _ingest(STOR_OLD, STOR_NEW)._nodes
    ans, _ = answer_ku_storage(Q_STOR, nodes)
    assert exact_judge(Q_STOR, "in a shoe rack in my closet", ans)


def test_mutation_pins_render_is_load_bearing():
    # the anaphora expansion and latest-state selection are what make
    # the judge flip: unexpanded / old-state renders MUST fail
    assert not exact_judge(Q_STOR, "in a shoe rack in my closet",
                           "in a shoe rack in it")
    assert not exact_judge(Q_RELOC, "the suburbs",
                           "a new apartment in the city")
    assert not exact_judge(Q_STOR, "in a shoe rack in my closet",
                           "under my bed")


def test_storage_latest_session_wins():
    # old state ALONE must not leak when latest state exists
    nodes = _ingest(STOR_OLD, STOR_NEW)._nodes
    ans, _ = answer_ku_storage(Q_STOR, nodes)
    assert "bed" not in ans.lower()


def test_storage_old_state_only_is_still_honest():
    # ONLY the old state present → renders it (state-agnostic face;
    # the currently/initially distinction lives in the FORM). The
    # purpose phrase ("for storage") is trimmed from the render.
    nodes = _ingest(STOR_OLD)._nodes
    ans, detail = answer_ku_storage(Q_STOR, nodes)
    assert ans == "under my bed"
    assert exact_judge(Q_STOR, "under my bed", ans)


def test_storage_user_role_wall():
    # assistant line with anchors + storage verb must never render
    polluted = list(STOR_NEW) + [
        {"role": 'assistant', "content":
          "You could store your old sneakers in a shoe rack in the garage."},
    ]
    nodes = _ingest(STOR_OLD, polluted)._nodes
    ans, detail = answer_ku_storage(Q_STOR, nodes)
    assert ans == "in a shoe rack in my closet"
    assert "garage" not in ans.lower()


def test_storage_unresolvable_pronoun_rendered_as_is():
    # "in it" with no possessive antecedent → render verbatim (no
    # fabrication), and no subsumption rescue needed
    no_ante = [
        {"role": 'user', "content":
          "I'm putting my old sneakers in a shoe rack in it this weekend."},
    ]
    nodes = _ingest(no_ante)._nodes
    ans, detail = answer_ku_storage(Q_STOR, nodes)
    assert ans == "in a shoe rack in it"


def test_storage_ambiguous_after_dedup_falls_through():
    # two INCOMPARABLE locations in the latest session → fall-through
    amb = [
        {"role": 'user', "content":
          "I'm keeping my old sneakers in the hallway closet now."},
        {"role": 'user', "content":
          "Also storing my old sneakers in a shoe rack in the entryway."},
    ]
    nodes = _ingest(amb)._nodes
    ans, detail = answer_ku_storage(Q_STOR, nodes)
    assert ans is None
    assert detail["reason"] == "ambiguous"


# ── adapter wiring ──

def test_adapter_gate_reloc():
    ad = _ingest(RACH_MID, RACH_LATEST)
    ans, meta = ad.answer_extractive(Q_RELOC, "")
    assert meta.get("gate") == "ku_reloc"
    assert "the suburbs" in (ans or "").lower()


def test_adapter_gate_storage():
    ad = _ingest(STOR_OLD, STOR_NEW)
    ans, meta = ad.answer_extractive(Q_STOR, "")
    assert meta.get("gate") == "ku_storage"
    assert ans == "in a shoe rack in my closet"


def test_adapter_flag_off_reloc():
    ad = _ingest(RACH_MID, RACH_LATEST, reloc_state_recall=False)
    ans, meta = ad.answer_extractive(Q_RELOC, "")
    assert meta.get("gate") != "ku_reloc"


def test_adapter_flag_off_storage():
    ad = _ingest(STOR_OLD, STOR_NEW, storage_loc_recall=False)
    ans, meta = ad.answer_extractive(Q_STOR, "")
    assert meta.get("gate") != "ku_storage"
