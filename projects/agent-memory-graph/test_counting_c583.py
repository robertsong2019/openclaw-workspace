"""C583: ordinal binding in _cnt_qty_stated's digit-quantity capture.

One capture gap leaves the LATEST current-state statement invisible
to the C550 recency machinery (latest-wins is implemented — but the
widened statement never becomes a mention):

Ordinal binding: "I just finished my 5th project" — the suffix 'th'
blocks the digit-to-stem adjacency ('5' followed by 'th', no
whitespace, the forward window dies at position). Fix: make the
ordinal suffix optional in the capture pattern. LATEST session wins
over the earlier "4 projects" statements.

REVERTED VARIANT (documented in the production comment): a relaxed
bare-quantity branch for "close to 1300 now"-shaped statements was
censused and pulled 7 new fires of which 2 killed banked rows —
clause digits are usually bound to a DIFFERENT noun ('6 months',
'2,000 miles', '500 words', '80D' model numbers). The bare-quantity
lane stays unreached; the honesty pins below freeze its fall-through.
"""
import sys

sys.path.insert(0, "/root/.openclaw/workspace/projects/agent-memory-graph")
from amg_bench_quality import _cnt_qty_stated, _cnt_enum_count


def _sessions(turns):
    """turns: [(session_no, content), ...] verbatim from the dataset."""
    by_sid = {}
    for sid, content in turns:
        by_sid.setdefault(sid, []).append(
            {"role": "user", "content": content})
    return [{"session_id": f"session_{sid}", "turns": t}
            for sid, t in sorted(by_sid.items())]


# ── verbatim fixtures (byte-exact, /root/lme_data/longmemeval_s_cleaned.json)

FX_A2F3AA27_Q = 'How many followers do I have on Instagram now?'
FX_A2F3AA27_GT = '1300'
FX_A2F3AA27 = [
    # session_13
    (13, "I'm looking to optimize my Instagram content strategy, can you give me some tips on how to increase engagement and grow my audience?"),
    # session_13
    (13, "I've been doing some of these already, like posting regularly and using a consistent aesthetic. It's great to know I'm on the right track. Speaking of which, I'm curious to know if there's a way to see which posts are performing well and which ones aren't. Do you know if Instagram Insights can help me with that? And by the way, I've got 1250 followers on Instagram now, so it'd be great to get some insights on how to optimize my content for them."),
    # session_13
    (13, "I'm actually thinking of trying out Instagram Live more often. Do you have any tips on how to make my live streams more engaging and interactive?"),
    # session_40
    (40, "I'm looking to create a new Instagram post about a recent industry event I attended. Can you help me come up with a catchy caption that will encourage engagement, considering my audience is mostly from the US, UK, and Australia? By the way, I've been meaning to check my current follower count - I think I'm close to 1300 now."),
    # session_40
    (40, 'I\'ll reach out to Ashley Gaida and propose a guest blog post collaboration. Here\'s my message: "Hi Ashley, I\'ve been following your content on content creation and digital marketing, and I love your insights. I think our audiences would really benefit from a guest post on my blog about creating engaging Instagram content. Would you be interested in writing a post for my audience?"'),
]

FX_06DB6396_Q = 'How many projects have I completed since starting painting classes?'
FX_06DB6396_GT = '5'
FX_06DB6396 = [
    # session_4
    (4, "I'm considering setting up a small art studio in my spare bedroom. Can you give me some tips on how to organize a small space for painting and storing supplies?"),
    # session_4
    (4, "I'm also thinking of working on some gift ideas for my sister's birthday next month. Do you have any ideas for paintings that would make good gifts?"),
    # session_4
    (4, "I'm actually working on a painting right now that I think my sister will love - it's a sunset scene. I've completed 4 projects since starting painting classes, and I'm feeling pretty confident about my skills. Do you have any tips on how to properly varnish and protect a painting?"),
    # session_4
    (4, "I've heard that it's also important to sign and date the painting. Do you have any advice on how to do that without detracting from the overall piece?"),
    # session_4
    (4, "I'm glad I got some helpful tips on varnishing and signing my painting. Since I've completed 4 projects since starting painting classes, I feel more confident in my skills. Speaking of which, I've been following a few artists on Instagram who inspire me with their work. Do you have any advice on how to reach out to them or engage with their content in a meaningful way?"),
    # session_7
    (7, "I'm interested in the Data Science course on Coursera, but I'm not sure if it's suitable for someone with no prior experience in the field. Can you tell me more about the prerequisites and what kind of projects I can expect to work on?"),
    # session_7
    (7, "I'm interested in the Data Visualization course on Coursera, but I'm not sure if it's suitable for someone with no prior experience in data visualization. Can you tell me more about the prerequisites and what kind of projects I can expect to work on, considering I just turned 32 years old last month and I've been realizing that my age could be an advantage in this case, bringing more maturity and focus to my learning journey."),
    # session_12
    (12, "I'll be waiting for your updates and ready to provide feedback and guidance whenever you need it. Good luck with your project, and have fun exploring the world of music production!"),
    # session_32
    (32, "I'm looking for some inspiration for my next painting project. I've been stuck on what to paint next and was wondering if you could suggest some ideas or themes. By the way, I just finished my 5th project since starting painting classes, and I'm feeling pretty accomplished!"),
]


# ── C583 target rescue (ordinal lane)

def test_ordinal_project_latest_wins():
    # s4 "4 projects" (twice) vs s32 "my 5th project" (ordinal suffix
    # blocked the capture) — latest wins with the ordinal visible.
    got = _cnt_qty_stated(FX_06DB6396_Q, _sessions(FX_06DB6396))
    assert got == FX_06DB6396_GT, got


# ── bare-quantity lane: documented fall-through (unreached by
#    design — the relaxed variant killed banked rows, see module
#    docstring; a2f3aa27 stays answered by the earlier statement)

def test_followers_bare_quantity_still_fall_through():
    # s13 "1250 followers" is the only adjacency-visible mention;
    # s40's "close to 1300 now" stays invisible — honest old data,
    # NOT a fabricated update. Next-cycle lane with a free-standing
    # digit discriminator.
    got = _cnt_qty_stated(FX_A2F3AA27_Q, _sessions(FX_A2F3AA27))
    assert got == "1250", got


def test_enum_count_integration_followers():
    # qty branch runs ahead of signature counting inside
    # _cnt_enum_count — integration pin at the fall-through value.
    got = _cnt_enum_count(FX_A2F3AA27_Q, _sessions(FX_A2F3AA27))
    assert got == "1250", got


# ── honesty pins (freeze the bare-quantity fall-through)

def test_cue_clause_multi_digit_abstains():
    # stem + cue but TWO digits in the clause — poison, abstain.
    q = "How many followers do I have?"
    sessions = _sessions([
        (1, "Checking my follower count now, been at this for 3 years and 5 months."),
    ])
    assert _cnt_qty_stated(q, sessions) is None


def test_no_cue_single_digit_does_not_fire():
    # stem + single digit but historical framing — not current state
    # (and no ordinal binding either).
    q = "How many followers do I have?"
    sessions = _sessions([
        (1, "My follower count reached 8 last year, before I took a break."),
    ])
    assert _cnt_qty_stated(q, sessions) is None


def test_ordinal_without_stem_does_not_fire():
    q = "How many projects have I completed?"
    sessions = _sessions([
        (1, "My 5th birthday was last week and it was great."),
    ])
    assert _cnt_qty_stated(q, sessions) is None


# ── existing C550 behavior pins (the widening must not disturb them)

def test_plain_stem_adjacent_capture_unchanged():
    q = "How many followers do I have on Instagram now?"
    sessions = _sessions([
        (1, "And by the way, I've got 1250 followers on Instagram now."),
    ])
    assert _cnt_qty_stated(q, sessions) == "1250"


def test_same_turn_ambiguity_still_abstains():
    q = "How many followers do I have?"
    sessions = _sessions([
        (1, "I have 40 or 50 followers now."),
    ])
    assert _cnt_qty_stated(q, sessions) is None


def test_coordinated_sum_still_works():
    q = "How many plants did I initially plant for tomatoes and cucumbers?"
    sessions = _sessions([
        (1, "I've been growing my own cucumbers in my garden, and I've got 3 plants that are producing a lot of them."),
        (2, "I planted 5 tomato plants initially, and they've been producing like crazy."),
    ])
    assert _cnt_qty_stated(q, sessions) == "8"
