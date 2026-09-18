# ════════ Cycle 588: most-recent-family-trip destination face ════════
# 9ea5eabc census-first miniatures. Fixtures are VERBATIM dataset
# content (repr-injected by step3_gen_fixture.py). The winning
# session (session_46 = answer_02e66dec_2) carries THREE Paris
# family-trip statements (went-to / recent-trip-to x2, dedup to one
# render); session_7 = answer_02e66dec_1 carries the EARLIER state
# (Hawaii) — latest-session-wins must pick Paris. Decoys, all
# structurally gated: Yosemite SOLO trip (trip-type filter),
# Japan past family trip (loses latest-wins), Tokyo FUTURE solo
# plans (past-tense-only dest patterns), "family-friendly" +
# planning-Europe line (no past dest pattern), assistant "Family
# Trip to Paris" (role wall).
import pytest

from amg_bench_quality import (LongMemEvalAdapter,
                               trip_recent_form,
                               answer_trip_recent,
                               exact_judge)

QUESTION = 'Where did I go on my most recent family trip?'

U_EUROPE = "I'm planning a trip to Europe and I was wondering if you could give me some tips on how to plan a family-friendly itinerary."
U_PARIS1 = "I'm actually thinking of going to Paris, we just went there as a family last month and it was amazing, I think my kids loved it. Do you have any specific tips for Paris?"
U_PARIS2 = "I'm excited to plan my solo trip to Tokyo! I was just thinking, since I recently went to Paris with my family, I might want to try something different in Tokyo. Do you have any recommendations for unique and off-the-beaten-path experiences in Tokyo?"
U_PARIS3 = "I'm so excited to explore all these hidden gems in Tokyo! Since I've been thinking about my recent family trip to Paris, I was wondering if you could help me compare and contrast my experiences traveling with family versus solo."
A_WALL = "What a great idea! Comparing and contrasting your experiences traveling with family versus solo can be a fascinating reflection. I'd be happy to help you explore the differences and similarities between your two trips.\n\n**Family Trip to Paris:**\n\n* **Pros:**\n\t+ Shared experiences and memories with loved ones\n\t+ Someone to share the planning and decision-making responsibilities\n\t+ A sense of security and comfort with familiar company\n\t+ Opportunities for quality time with family members\n* **Cons:**\n\t+ Compromises on itinerary and activities to accommodate everyone's interests\n\t+ Limited alone time or personal space\n\t+ Potential for conflicts or disagreements within the group\n\t+ More complex logistics and planning required\n\n**Solo Trip to Tokyo:**\n\n* **Pros:**\n\t+ Total freedom to create your own itinerary and schedule\n\t+ Opportunity to explore personal interests and passions without compromise\n\t+ Time for self-reflection and personal growth\n\t+ Meeting new people and making solo travel connections\n* **Cons:**\n\t+ No one to share experiences or memories with immediately\n\t+ Full responsibility for planning and decision-making\n\t+ Potential for feelings of loneliness or isolation\n\t+ Higher risk of scams or safety concerns\n\nNow, let's compare and contrast the two experiences:\n\n* **Planning:** With family, you had to consider everyone's opinions and preferences, while solo, you have complete control over the itinerary.\n* **Pace:** Family travel often requires a more leisurely pace to accommodate everyone's needs, whereas solo travel allows for a more flexible and spontaneous pace.\n* **Interactions:** With family, you had built-in companionship and social interaction, whereas solo, you'll need to make an effort to meet new people or engage with locals.\n* **Personal growth:** Both types of travel can offer opportunities for personal growth, but solo travel often pushes you out of your comfort zone and forces you to be more self-reliant.\n\nReflecting on your experiences, you might realize that:\n\n* You enjoyed the social aspect of family travel, but also appreciated the independence of solo travel.\n* You learned to appreciate the flexibility and spontaneity of solo travel, but also valued the shared experiences with family.\n* You discovered new aspects of yourself and your travel style through both experiences.\n\nRemember, there's no right or wrong way to travel. Both family and solo travel have their unique benefits and challenges. The key is to find what works best for you and your personal preferences.\n\nNow, go forth and plan your next adventure, whether it's with family or solo!"
U_HAWAII = "That's really helpful! I was thinking about my recent family trip to Hawaii and how we had a great time snorkeling together. But I also remember feeling a bit stuck to a schedule."
U_YOSEMITE = "I've been testing out a few portable water filters on my recent camping trips, including my solo trip to Yosemite six weeks ago, and I'm curious if you have any recommendations for water filter maintenance and cleaning."
U_JAPAN = "I'm actually planning a trip to Japan soon and I was wondering if you could help me plan my itinerary. I've been to Japan before, but it was a family trip and we spent 10 days island-hopping in Hawaii right before that, so it was a bit chaotic. This time I'm going solo and I want to make the most of my trip."

PARASITIC = "I've been testing out a few portable water filters on my recent camping trips, including my solo trip to Yosemite six weeks ago, and I'm curious if you have any recommendations for water filter maintenance and cleaning."   # C586-chain pred for 9ea5eabc (gate=where)

S_WIN = [
    {"role": "user", "content": U_EUROPE},
    {"role": "user", "content": U_PARIS1},
    {"role": "assistant", "content": A_WALL},
    {"role": "user", "content": U_PARIS2},
    {"role": "user", "content": U_PARIS3},
]
S_EARLIER = [{"role": "user", "content": U_HAWAII}]
S_SOLO = [{"role": "user", "content": U_YOSEMITE},
          {"role": "user", "content": U_JAPAN}]


def _ingest(*sessions, **kw):
    ad = LongMemEvalAdapter(**kw)
    ad.ingest_sessions([{"session_id": f"session_{i+1}",
                          "messages": list(s)}
                       for i, s in enumerate(sessions)])
    return ad


# ── form ──

def test_form_accept():
    assert trip_recent_form(QUESTION) == "family"


def test_form_reject_no_recency_word():
    # e01b8e2f shape: family trip demand but no recency word
    q = "Where did I go on a week-long trip with my family?"
    assert trip_recent_form(q) is None


def test_form_reject_future_stay_demand():
    # eace081b shape (BANKED row — must stay out of the form)
    q = "Where am I planning to stay for my birthday trip to Hawaii?"
    assert trip_recent_form(q) is None


def test_form_reject_not_a_where_demand():
    # e6041065 shape (BANKED row — must stay out of the form)
    q = "What percentage of packed shoes did I wear on my last trip?"
    assert trip_recent_form(q) is None


# ── answer face ──

def test_rescue_latest_session_wins():
    nodes = _ingest(S_EARLIER, S_WIN)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans == "Paris"
    assert detail["form"] == "trip_recent"
    assert detail["renders"] == ["Paris"]


def test_earlier_state_alone_renders_hawaii():
    # mechanism, not hardcoding: without the later session the
    # latest (only) family-trip render is Hawaii
    nodes = _ingest(S_EARLIER)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans == "Hawaii"


def test_solo_and_future_decoys_never_render():
    # Yosemite solo + Japan past-family: neither may render (the
    # solo line fails the trip-type filter; the Japan line has no
    # past-tense dest pattern) — decoy-only graph stays silent
    nodes = _ingest(S_SOLO)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "no_match"


def test_future_solo_tokyo_no_render_in_winner():
    # the winning session's Tokyo plans ("planning a solo trip",
    # "going to") must not join the render set
    nodes = _ingest(S_WIN)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert detail["renders"] == ["Paris"]


def test_assistant_role_wall():
    # assistant trip prose never renders ("Where did I go" = the
    # user's own trips)
    wall = [{"role": "assistant", "content": A_WALL},
            {"role": "user", "content": "Great tips, thanks a lot!"}]
    nodes = _ingest(wall)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "no_match"


def test_trip_type_word_is_hard_filter():
    # "went to X" without the demanded trip-type word ("family")
    # is structurally not an answer — demand-NP lesson (C584)
    solo = [{"role": "user", "content":
             "I recently went to Yosemite on a solo camping trip."}]
    nodes = _ingest(solo)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "no_match"


def test_ambiguous_two_dests_in_latest_session():
    # >1 distinct family-trip destination in the winning session
    # (= ambiguity must live INSIDE the latest session, not across
    # sessions — latest-session-wins already isolates older ones)
    win2 = list(S_WIN) + [{"role": "user", "content":
              "Before that, my last family trip to Rome was also "
              "great."}]
    nodes = _ingest(S_EARLIER, win2)._nodes
    ans, detail = answer_trip_recent(QUESTION, nodes)
    assert ans is None
    assert detail["reason"] == "ambiguous"
    assert sorted(detail["renders"]) == ["Paris", "Rome"]


# ── judge pins ──

def test_judge_pin_paris():
    assert exact_judge(QUESTION, "Paris", "Paris") is True


def test_judge_pin_parasitic_pred_stays_wrong():
    # the C586-chain parasitic pred (Yosemite water-filter line)
    # must NOT bank — the face is what rescues the row
    assert exact_judge(QUESTION, "Paris", PARASITIC) is False


# ── adapter wiring ──

def test_adapter_gate_and_pred():
    ad = _ingest(S_EARLIER, S_WIN)
    ans, meta = ad.answer_extractive(QUESTION, "")
    assert meta.get("gate") == "trip_recent"
    assert ans == "Paris"


def test_adapter_flag_off_keeps_old_path():
    ad = _ingest(S_EARLIER, S_WIN, trip_recent_recall=False)
    ans, meta = ad.answer_extractive(QUESTION, "")
    assert meta.get("gate") != "trip_recent"
