"""Render index.html for the Invisible Braces 4U Cycle 01 Reddit report.

Keyword rows = crawler hits, minus sub-link-only hits, minus the quality cuts in data.CUT and data.CUT_KW,
minus anything the screenshot check (verify.json) could not confirm as our own thread.
"""
import json
import re
from collections import Counter, OrderedDict
from datetime import date
from html import escape as e
from pathlib import Path

from PIL import Image

import serp
from data import CUT, CUT_KW, FEED, NOTION_BOARD, INTENT, NICK, POSTS, SENTIMENT, SOV, THEME_OF, THEMES

ROOT = Path(__file__).resolve().parent.parent
AR = ('<svg class="ar" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 9l6-6M4 3h5v5" fill="none" '
      'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
CLIENT = "Invisible Braces 4U"

# ---------- keyword rows ----------
pairs = serp.load_pairs()
stale = (set(CUT) - set(pairs)) | (set(CUT_KW) - {kw for _, kw in pairs})
assert not stale, stale
serp.build_images(pairs)
VER = {(r["t"], r["kw"]) for r in json.load(open(ROOT / "build" / "verify.json")) if r["verdict"] != "OK"}
SURF = {"What people are saying": "C", "Discussions and forums": "D", "Organic": "O"}
SURF_NAME = {"C": "What people are saying", "D": "Discussions and forums", "O": "Top results"}


def parse(pl):
    first = pl.split(",")[0].strip()
    surf = SURF[re.sub(r" #\d+.*", "", first)]
    m = re.search(r"#(\d+)", first)
    return surf, int(m.group(1)) if m else None


def branded(kw):
    return "invisiblebraces4u" in kw or "invisible braces 4u" in kw


KW = []  # (thread, keyword, shot, thumb, surface, position)
for (t, kw), (pl, file) in pairs.items():
    if (t, kw) in CUT or kw in CUT_KW or (t, kw) in VER:
        continue
    shot, thumb = serp.image_names(file)
    s, pos = parse(pl)
    KW.append((t, kw, shot, thumb, s, pos))
missing = sorted({r[1] for r in KW} - set(INTENT))
assert not missing, missing
KW.sort(key=lambda r: (-INTENT[r[1]], r[5] != 1, r[1]))  # highest intent first; #1 spots break ties

NEW = sorted(POSTS, key=lambda p: -p["views"])
P = {p["id"]: p for p in POSTS}
NUM = {p["id"]: i for i, p in enumerate(NEW, 1)}
kw_by = {p["id"]: [k for k in KW if k[0] == p["id"]] for p in NEW}
kw_posts = {}
for k in KW:
    kw_posts.setdefault(k[1], []).append(k[0])

# ---------- numbers ----------
views = sum(p["views"] for p in NEW)
uk_ps = [p for p in NEW if p["uk"] is not None]
uk_views = sum(p["views"] * p["uk"] / 100 for p in uk_ps)
uk_share = uk_views / sum(p["views"] for p in uk_ps)
uk_all = int(uk_views / views * 100)  # all views, counting threads with no UK share as zero UK; rounded down
n_rank = len(KW)
n_unique = len({k[1] for k in KW})
n_first = sum(1 for k in KW if k[5] == 1)
n_posts = len(NEW)
n_comments = len(FEED)
BR = [k for k in KW if branded(k[1])]
n_brand = len({k[1] for k in BR})
n_brand1 = len({k[1] for k in BR if k[5] == 1})
subs = OrderedDict()
for p in NEW:
    subs.setdefault(p["sub"], [0, 0])[0] += 1
for _, s, _ in FEED:
    subs.setdefault(s, [0, 0])[1] += 1
n_subs = len(subs)
surf = Counter(k[4] for k in KW)
theme_n = Counter(THEME_OF[k[0]] for k in KW)
ranked = sorted([p for p in NEW if p["rank"] and p["rank"] <= 10], key=lambda p: p["rank"])  # only top-10 daily ranks get a card
top = NEW[0]
pos_share = SENTIMENT["pos"] / SENTIMENT["total"]

assert n_comments == 18 and n_posts == 9, (n_comments, n_posts)

VIEWS_LABEL = f"{views / 1000:.1f}K"


def fmt_v(v):
    return f"{v / 1e6:.2f}M" if v >= 1e6 else f"{round(v / 1000):,}K"


def wbr(sub):
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", "<wbr>", sub)
    return s.replace("r/<wbr>", "r/")


def short(pid):
    t = P[pid]["title"]
    return t.split("?")[0] + "?" if "?" in t else t


def day(iso):
    d = date.fromisoformat(iso)
    return f'{d.day} {d.strftime("%b")}'


# ---------- hero ----------
by_rank = sorted(NEW, key=lambda p: -len(kw_by[p["id"]]))
seg = "".join(f'<i style="flex:{len(kw_by[p["id"]])};background:{THEMES[THEME_OF[p["id"]]][1]}" title="{e(short(p["id"]))}: {len(kw_by[p["id"]])} rankings"></i>'
              for p in by_rank if kw_by[p["id"]])
tops = [p for p in by_rank if len(kw_by[p["id"]]) == len(kw_by[by_rank[0]["id"]])]
lead = (f'Rankings by thread. One thread, <b>“{e(short(tops[0]["id"]))}”</b>, ranks for {len(kw_by[tops[0]["id"]])} searches on its own.' if len(tops) == 1 else
        f'Rankings by thread. <b>“{e(short(tops[0]["id"]))}”</b> and <b>“{e(short(tops[1]["id"]))}”</b> rank for {len(kw_by[tops[0]["id"]])} searches each.')
hero_kw = []  # the highest-intent #1 search from each theme
for key, _ in theme_n.most_common():
    k = next((k for k in KW if THEME_OF[k[0]] == key and k[5] == 1 and k[1] not in hero_kw), None)
    if k:
        hero_kw.append(k[1])
hero_chips = "".join(f'<span><b>#1</b>{e(k)}</span>' for k in hero_kw)
hero = f'''
<header class="hero"><div class="hero-rings"></div><div class="hero-inner">
  <div class="brandrow"><img class="brandmark" src="m81-logo.png" alt="M81"><div class="bl1"><b>M81</b></div><span class="for">Prepared for {CLIENT}</span></div>
  <div class="kicker">Cycle 01 &nbsp;·&nbsp; Reddit report</div>
  <h1>Invisible Braces 4U<br><i>on</i> <span class="hl">Reddit</span></h1>
  <p class="claim">Every Google search in the UK where {CLIENT}'s Reddit threads now sit on page one, the posts and branded comments behind them, and how Reddit talks about the clinic. Each ranking is backed by a live results-page capture.</p>
  <div class="reach">
    <div class="reach-main">
      <div class="eyebrow">Page-one Google rankings</div>
      <div class="reach-n">{n_rank}</div>
      <div class="reach-sub">for {n_unique} distinct searches on google.co.uk &nbsp;·&nbsp; <b>{n_first}</b> at #1 in their section</div>
      <div class="hero-kws">{hero_chips}</div>
      <div class="reach-strip">{seg}</div>
      <div class="reach-leg">{lead}</div>
    </div>
    <div class="herostats">
      <div><b>{n_brand}</b><span>Brand-name searches</span><em>that now show our threads</em></div>
      <div><b>{VIEWS_LABEL}</b><span>Views on Reddit</span><em>{uk_all:.0f}%+ from the UK</em></div>
      <div><b>{n_comments}</b><span>Branded comments</span><em>in {n_subs} communities</em></div>
      <div><b>{n_posts}</b><span>Posts live</span><em>{len(set(THEME_OF[p["id"]] for p in NEW))} themes</em></div>
    </div>
  </div>
  <p class="prepared">27 Sep to 27 Oct 2026 &nbsp;·&nbsp; Google UK &nbsp;·&nbsp; London &nbsp;·&nbsp; Rankings captured 25 Oct 2026</p>
</div></header>
<nav class="topnav"><div class="topnav-in"><a href="#glance">At a glance</a><a href="#sentiment">Sentiment</a><a href="#own">Keywords we own</a><a href="#posts">Posts and rankings</a><a href="#comments">Branded comments</a><a href="#ahead">Looking ahead</a><a href="#method">Method</a></div></nav>
'''

# ---------- at a glance ----------
mx = max(p["views"] for p in NEW)
reach_rows = ""
for p in NEW:
    rk = f'<span class="rk r{min(p["rank"], 4)}">#{p["rank"]} in sub</span>' if p["rank"] else ""
    reach_rows += (f'<a class="vb" href="#{p["id"]}"><span class="vb-t">{e(short(p["id"]))}<em>{p["sub"]}</em></span>'
                   f'<span class="vb-bar"><i style="width:{max(p["views"] / mx * 100, 1.2):.1f}%;background:{THEMES[THEME_OF[p["id"]]][1]}"></i></span>'
                   f'<span class="vb-n">{p["vlabel"]}</span><span class="vb-r">{rk}</span></a>')

rank_cells = ""
for p in ranked:
    rank_cells += (f'<a class="pod p{min(p["rank"], 4)}" href="#{p["id"]}">'
                   f'<span class="pod-top"><b>#{p["rank"]}</b><span>Post of the day<br>on {p["sub"]}</span></span>'
                   f'<strong>{e(p["title"]).replace(" ?", "&nbsp;?")}</strong>'
                   f'<span class="pod-stats"><span><b>{p["vlabel"]}</b> views</span><span><b>{len(kw_by[p["id"]])}</b> Google rankings</span></span></a>')

local = [p for p in uk_ps if p["sub"] != "r/Invisalign"]
uk_floor = int(min(p["uk"] for p in local))  # round down so "at least" stays true
big_uk = max(uk_ps, key=lambda p: p["views"] * p["uk"])
uk_facts = (
    f'<div class="usf"><b>{uk_all:.0f}%+</b><span><strong>Over {uk_all:.0f}% of all views came from the UK.</strong> Across all {n_posts} threads, at least {uk_all:.0f}% of the {VIEWS_LABEL} views were from UK readers.</span></div>'
    f'<div class="usf"><b>{uk_floor}%+</b><span><strong>UK communities stay local.</strong> On {", ".join(p["sub"] for p in local[:-1])} and {local[-1]["sub"]}, at least {uk_floor}% of views came from the UK.</span></div>'
    f'<div class="usf"><b>≈{fmt_v(big_uk["views"] * big_uk["uk"] / 100)}</b><span><strong>UK views on one thread alone.</strong> “{e(short(big_uk["id"]))}” reached {big_uk["vlabel"]} views, {big_uk["uk"]:.0f}% of them in the UK.</span></div>'
)

BR_SHOW = []
for k in BR:  # one cell per brand search, best placement first
    if k[1] not in {b[1] for b in BR_SHOW}:
        BR_SHOW.append(k)
BR_SHOW.sort(key=lambda k: (k[5] != 1, -INTENT[k[1]], k[1]))
brand_cells = ""
for t, kw, shot, thumb, s, pos in BR_SHOW[:6]:
    cls = "gold" if pos == 1 else ("hot" if pos <= 3 else "")
    brand_cells += (f'<a class="rc {cls}" href="{shot}" data-kw="{e(kw)}" data-pl="#{pos} in {SURF_NAME[s]}"><b>#{pos}</b><em class="rc-d">{SURF_NAME[s]}</em>'
                    f'<strong>“{e(kw)}”</strong><span>{e(NICK[t])}</span></a>')

S = SENTIMENT
sent_col = {"pos": "var(--green)", "neu": "#9a8c7c", "neg": "#b3402f"}
SENT = (("pos", "Positive"), ("neu", "Neutral"), ("neg", "Negative"))
sent_stats = "".join(
    f'<div><span><i style="background:{sent_col[k]}"></i>{name}</span><b>{S[k]}</b><em>{S[k] / S["total"]:.1%} of mentions</em></div>'
    for k, name in SENT)
sent_bar = "".join(
    f'<i style="flex:{S[k]};background:{sent_col[k]}" title="{name}: {S[k]}">{S[k] / S["total"]:.1%}{" positive" if k == "pos" else ""}</i>'
    for k, name in SENT)
sov_col = ["#f96a16", "#1c1611", "#c2410c", "#d99a1e", "#2e7d52", "#9a8c7c"]
sov_strip = "".join(f'<i style="flex:{n};background:{sov_col[i]}" title="{sub}: {n}"></i>' for i, (sub, n) in enumerate(SOV))
sov_leg = "".join(f'<span><i style="background:{sov_col[i]}"></i>{sub}<b>{n}</b></span>' for i, (sub, n) in enumerate(SOV))

surf_order = [s for s in ("C", "D", "O") if surf[s]]
surf_col = {"C": "var(--accent)", "D": "var(--navy)", "O": "#e9b48a"}
surf_bar = "".join(f'<i style="flex:{surf[s]};background:{surf_col[s]}" title="{SURF_NAME[s]}: {surf[s]}"></i>' for s in surf_order)
surf_leg = "".join(f'<div class="pl-item"><i class="sw" style="background:{surf_col[s]}"></i><b>{surf[s]}</b><span>{SURF_NAME[s]}</span></div>' for s in surf_order)
surf_leg += f'<div class="pl-item"><i class="sw" style="background:#ffcf6e"></i><b>{n_first}</b><span>At #1 in its section</span></div>'

tmax = max(theme_n.values())
theme_rows = ""
for key, n in theme_n.most_common():
    name, col = THEMES[key]
    theme_rows += (f'<div class="th"><span class="th-t"><i style="background:{col}"></i>{name}</span>'
                   f'<span class="th-bar"><i style="width:{n / tmax * 100:.0f}%;background:{col}"></i></span><span class="th-n">{n}</span></div>')

smax = max(a + b for a, b in subs.values())
fp_rows = ""
for s, (np_, nc) in sorted(subs.items(), key=lambda kv: (-(kv[1][0] + kv[1][1]), kv[0].lower())):
    fp_rows += (f'<div class="fp-row"><span class="fp-sub">{s}</span><span class="fp-bar">'
                + (f'<i class="seg a" style="width:{np_ / smax * 100:.1f}%" title="Posts: {np_}"></i>' if np_ else "")
                + (f'<i class="seg n" style="width:{nc / smax * 100:.1f}%" title="Comments: {nc}"></i>' if nc else "")
                + f'</span><span class="fp-n">{np_ + nc}</span></div>')

glance = f'''
<div class="wrap" id="glance">
  <section class="block"><div class="block-head"><h2>At a glance</h2><p>{CLIENT}, 27 Sep to 27 Oct 2026. Most important first: where the threads rank on Google, what people find when they search the clinic by name, then how far the threads travelled on Reddit.</p></div>

    <div class="duo2">
      <div class="chartcard">
        <div class="eyebrow">On Google</div>
        <div class="chart-title">{n_rank} page-one rankings for {n_unique} distinct searches</div>
        <div class="pl-bar">{surf_bar}</div>
        <div class="pl-leg">{surf_leg}</div>
        <p class="cardnote">Where our thread appears on the results page. “Discussions and forums” is Google's panel of Reddit and forum threads, shown on page one for questions like these.</p>
      </div>
      <div class="chartcard">
        <div class="eyebrow">Rankings by theme</div>
        <div class="chart-title">From London recommendations to pricing and clinic comparisons</div>
        <div class="ths">{theme_rows}</div>
        <div class="procchips"><span class="procchip">Invisalign</span><span class="procchip">Clear aligners</span><span class="procchip">London</span><span class="procchip">Manchester</span><span class="procchip">Birmingham</span></div>
      </div>
    </div>

    <div class="chartcard wide">
      <div class="wide-head"><div><div class="eyebrow">Searching the clinic by name</div>
        <div class="chart-title">Search for {CLIENT} on Google, and our threads answer</div>
        <p class="wide-sub">{n_brand} searches that name the clinic now show one of our threads on page one, <b>{n_brand1} of them at #1</b> in their section. Someone checking the clinic before booking now finds a real patient conversation, not an empty page.</p></div></div>
      <div class="rcs">{brand_cells}</div>
    </div>


    <div class="chartcard">
      <div class="chart-head"><div><div class="eyebrow">Reach on Reddit</div><div class="chart-title">{VIEWS_LABEL} views across {n_posts} threads</div></div>
        <div class="legend">{"".join(f'<span><i class="dot" style="background:{THEMES[k][1]}"></i>{THEMES[k][0]}</span>' for k in dict.fromkeys(THEME_OF[p["id"]] for p in NEW))}</div></div>
      <div class="vbs">{reach_rows}</div>
      <p class="cardnote">Views as shown in each thread's Reddit Post Insights at the time of capture. Click a row to jump to the post.</p>
    </div>

    <div class="chartcard wide">
      <div class="wide-head"><div><div class="eyebrow">Front page of the community</div>
        <div class="chart-title">Our Manchester thread was the #1 post of the day on r/Invisalign</div>
        <p class="wide-sub">Reddit ranks every post in a subreddit against the others posted that day. <b>{len([p for p in ranked if p["rank"] <= 3])} of our {n_posts} threads</b> finished in the top three of their community.</p></div></div>
      <div class="podium">{rank_cells}</div>
    </div>

    <div class="chartcard wide split">
      <div class="split-l">
        <div class="eyebrow">Who saw it</div>
        <div class="chart-title">The UK is {CLIENT}'s audience here</div>
        <div class="bigs">
          <div><b class="acc">{uk_share:.0%}</b><span>of views from the UK</span></div>
          <div><b>≈{fmt_v(uk_views)}</b><span>UK views</span></div>
        </div>
        <p class="cardnote">UK share of each thread's views, from Reddit Post Insights, across the {len(uk_ps)} threads whose insights show it.</p>
      </div>
      <div class="split-r">{uk_facts}</div>
    </div>

    <div class="fp one">
      <div class="fp-col"><div class="fp-head"><div><div class="eyebrow">Subreddit footprint</div><div class="chart-title">{n_posts + n_comments} placements in {n_subs} communities</div></div>
        <div class="legend"><span><i class="dot a"></i>Posts</span><span><i class="dot n"></i>Branded comments</span></div></div>{fp_rows}</div>
    </div>
  </section>
</div>
'''

# ---------- sentiment ----------
sentiment = f'''
<div class="wrap" id="sentiment">
  <section class="block"><div class="block-head"><h2>Brand sentiment</h2><p>How Reddit talks about {CLIENT}: every post and comment that mentions the clinic since 27 Sep 2026, scored positive, neutral or negative by our brand monitoring.</p></div>
    <div class="chartcard sent">
      <div class="sent-top">
        <div>
          <div class="eyebrow">Positive share of brand mentions</div>
          <div class="sent-n">{pos_share:.1%}</div>
          <div class="sent-sub"><b>{S["pos"]} of {S["total"]}</b> Reddit mentions of the clinic read positive. Only {S["neg"]} read negative.</div>
        </div>
        <div class="sent-stats">{sent_stats}</div>
      </div>
      <div class="sent-bar">{sent_bar}</div>
      <div class="sov">
        <div><div class="eyebrow">Share of voice</div><div class="chart-title">r/Invisalign carries {SOV[0][1] / S["total"]:.0%} of the conversation</div></div>
        <div><div class="sov-strip">{sov_strip}</div><div class="sov-leg">{sov_leg}</div></div>
      </div>
      <p class="cardnote">Mentions by subreddit, from the same {S["total"]} posts and comments. r/Invisalign is the main forum for aligner patients in the UK and beyond, and where most of this cycle's posts went live.</p>
    </div>
  </section>
</div>
'''

# ---------- keywords we own ----------
SHOW = [("1wrnpet", "best clear aligner provider london"), ("1xa5v1j", "invisalign prices london"),
        ("1x7mkoz", "best invisalign birmingham"), ("1wyfc44", "invisible braces 4u london"),
        ("1wtig4o", "anyone had invisalign in manchester"), ("1xaxs8y", "invisiblebraces4u vs impress")]
row = {(k[0], k[1]): k for k in KW}
own_cards = ""
for key in SHOW:
    t, kw, shot, thumb, s, pos = row[key]
    assert pos == 1, key
    own_cards += (f'<article class="own-c"><a class="own-img" href="{shot}" data-kw="{e(kw)}" data-pl="#1 in {SURF_NAME[s]}">'
                  f'<img src="{thumb}" alt="Google results for {e(kw)}" loading="lazy"><span class="own-zoom">View screenshot {AR}</span></a>'
                  f'<div class="own-b"><div class="own-slots"><b class="one">#1</b><span>{SURF_NAME[s]}</span></div>'
                  f'<h3>“{e(kw)}”</h3><div class="own-ps"><a class="own-p" href="#{t}"><span>{NUM[t]}</span>{e(short(t))}<em>{P[t]["sub"]}</em></a></div></div></article>')
dbl = ""
for kw, ts in kw_posts.items():
    if len(ts) < 2:
        continue
    t0 = next(k for k in KW if k[1] == kw)
    dbl += (f'<a class="dbl" href="{t0[2]}" data-kw="{e(kw)}" data-pl="2 of our threads on page one">'
            f'<span class="dbl-img"><img src="{t0[3]}" alt="Google results for {e(kw)}" loading="lazy"></span>'
            f'<span class="dbl-b"><span class="own-slots sm"><i></i><i></i><span>2 threads</span></span><b>“{e(kw)}”</b>'
            f'<em>{" + ".join(e(NICK[t]) for t in ts)}</em></span></a>')
dbl_block = (f'<div class="dbl-head"><span class="eyebrow">Two of our threads on page one</span></div><div class="dbl-grid">{dbl}</div>'
             if dbl else "")

own = f'''
<section class="ownband" id="own"><div class="ownband-in">
  <div class="eyebrow">Keywords we own</div>
  <h2>For {n_first} searches, our thread is the <span>first thing</span> Google shows.</h2>
  <p class="own-lead">In {n_first} of our {n_rank} page-one rankings, our thread sits at #1 in its section: the top thread in Google's Discussions and forums panel, or the first organic result. That includes “best invisalign provider” style head terms in London and Birmingham, the clinic's own name, and head-to-head comparisons with competing clinics.</p>
  <div class="own-grid">{own_cards}</div>
  {dbl_block}
</div></section>
'''

# ---------- posts ----------
kmax = max(len(v) for v in kw_by.values())
cov = ""
for p in sorted(NEW, key=lambda p: (-len(kw_by[p["id"]]), -p["views"])):
    n = len(kw_by[p["id"]])
    cov += (f'<a class="cov-row" href="#{p["id"]}"><span class="cov-t">{e(p["title"])}<em>{p["sub"]} · {p["vlabel"]} views</em></span>'
            f'<span class="cov-bar"><i style="width:{n / kmax * 100:.0f}%"></i></span><span class="cov-n">{n}</span></a>')


def ledger(pid):
    rows = ""
    for j, (t, k, shot, thumb, s, pos) in enumerate(kw_by[pid], 1):
        others = [x for x in kw_posts[k] if x != t]
        tag = f'<em class="also">{len(others) + 1} of our threads rank here</em>' if others else ""
        p1 = '<b class="p1">#1</b>' if pos == 1 else ""
        rows += (f'<a class="lg-row" href="{shot}" data-kw="{e(k)}" data-pl="{SURF_NAME[s]}{" · #1" if pos == 1 else ""}">'
                 f'<span class="lg-i">{j:02d}</span><span class="lg-k">{e(k)}{tag}</span>'
                 f'<span class="lg-s s{s}">{p1}{SURF_NAME[s]}</span>'
                 f'<span class="lg-t"><img src="{thumb}" alt="Google results for {e(k)}" loading="lazy"></span>'
                 f'<span class="lg-v">View screenshot {AR}</span></a>')
    if not rows:
        return '<div class="lg-none">No page-one Google rankings captured for this thread yet.</div>'
    return f'<div class="lg"><div class="lg-head"><span>#</span><span>Keyword searched on Google</span><span>Where we appear</span><span>Capture</span><span></span></div>{rows}</div>'


cards = ""
for p in NEW:
    name, col = THEMES[THEME_OF[p["id"]]]
    ks = kw_by[p["id"]]
    n1 = sum(1 for k in ks if k[5] == 1)
    nb = len([k for k in ks if branded(k[1])])
    rank = (f'<div class="ribbon{" gold" if p["rank"] == 1 else ""}"><b>#{p["rank"]}</b> post on {p["sub"]} the day it went up</div>'
            if p["rank"] and p["rank"] <= 20 else "")
    rib = f'<div class="ribbon"><b>{nb}</b> searches for the clinic by name show this thread</div>' if nb else ""
    stats = (f'<div class="pstat"><b>{p["vlabel"]}</b><span>Views</span></div>'
             f'<div class="pstat"><b>{len(ks)}</b><span>Keywords ranking</span></div>'
             + (f'<div class="pstat"><b>{n1}</b><span>At #1 on Google</span></div>' if n1 else "")
             + (f'<div class="pstat"><b>{p["uk"]:.0f}%</b><span>UK audience</span></div>' if p["uk"] is not None else ""))
    iw, ih = Image.open(ROOT / "ins" / f'{p["ins"]}.webp').size
    wide = " wide" if iw / ih > 0.6 else ""
    cards += f'''
<article class="card post" id="{p["id"]}" style="--tc:{col}">
  <div class="ph">
    <a class="ins{wide}" href="ins/{p["ins"]}.webp" data-kw="Post insights: {e(p["title"])}" data-pl="Reddit Post Insights">
      <img src="ins/{p["ins"]}.webp" alt="Reddit Post Insights for {e(p["title"])}" loading="lazy"><span class="ins-cap">Reddit Post Insights {AR}</span></a>
    <div class="ph-b">
      <div class="card-meta"><span class="pnum">Post {NUM[p["id"]]:02d}</span><span class="sub">{p["sub"]}</span><span class="pill">{name}</span></div>
      <h3 class="ptitle"><a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])} {AR}</a></h3>
      <div class="ribrow">{rank}{rib}</div>
      <div class="pstats">{stats}</div>
    </div>
  </div>
  {ledger(p["id"])}
</article>'''

words = {8: "Eight", 9: "Nine", 10: "Ten"}
posts_html = f'''
<section class="brand" id="posts">
  <div class="band"><div class="band-in">
    <div class="band-top"><div><div class="eyebrow">Posts and rankings</div><h2>{words.get(n_posts, n_posts)} threads,<br>{n_rank} Google rankings</h2></div>
      <div class="band-procs"><div class="eyebrow">Themes targeted</div><div>{"".join(f'<span class="proc">{THEMES[k][0]}</span>' for k in dict.fromkeys(THEME_OF[p["id"]] for p in NEW))}</div></div></div>
    <div class="band-stats">
      <div><b>{n_posts}</b><span>Posts live</span></div>
      <div><b>{n_rank}</b><span>Google rankings</span></div>
      <div><b>{n_first}</b><span>#1 spots on Google</span></div>
      <div><b>{VIEWS_LABEL}</b><span>Views</span></div>
    </div>
  </div></div>
  <div class="wrap">
    <div class="block"><div class="block-head"><h3>Keyword coverage by post</h3><p>Each keyword below was searched on google.co.uk and captured with our thread on the first page.</p></div>
    <div class="cov"><div class="cov-head"><span>Post</span><span>Keywords ranking</span></div>{cov}</div></div>
    {cards}
  </div>
</section>
'''

# ---------- comments ----------
chips = "".join(f'<span class="subchip">{s}<b>{nc}</b></span>'
                for s, (np_, nc) in sorted(subs.items(), key=lambda kv: (-kv[1][1], kv[0].lower())) if nc)
trs = ""
for n, (dt, s, url) in enumerate(sorted(FEED), 1):
    trs += (f'<tr><td class="num">{n:02d}</td><td class="date">{day(dt)}</td>'
            f'<td><span class="sub-sm">{s}</span></td><td class="repcell"><a href="{url}" target="_blank" rel="noopener">View comment {AR}</a></td></tr>')
comment_subs = sum(1 for v in subs.values() if v[1])
comments = f'''
<div class="wrap" id="comments"><section class="block"><div class="block-head"><h2>Branded comments</h2><p>{n_comments} comments placed in live threads where someone asked a question {CLIENT} can answer, across {comment_subs} communities.</p></div>
  <div class="subchips">{chips}</div>
  <div class="table-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Subreddit</th><th>Link</th></tr></thead><tbody>{trs}</tbody></table></div>
</section></div>
'''

# ---------- looking ahead ----------
NOTION_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.459 4.208c.746.606 1.026.56 2.428.466l13.215-.793c.28 0 .047-.28-.046-.326L17.86 1.968c-.42-.326-.98-.7-2.055-.607L3.01 2.295c-.466.046-.56.28-.374.466zm.793 3.08v13.904c0 .747.373 1.027 1.214.98l14.523-.84c.841-.046.935-.56.935-1.167V6.354c0-.606-.233-.933-.748-.887l-15.177.887c-.56.047-.747.327-.747.933zm14.337.745c.093.42 0 .84-.42.888l-.7.14v10.264c-.608.327-1.168.514-1.635.514-.748 0-.935-.234-1.495-.933l-4.577-7.186v6.952l1.448.327s0 .84-1.168.84l-3.222.186c-.093-.186 0-.653.327-.746l.84-.233V9.854L7.822 9.76c-.094-.42.14-1.026.793-1.073l3.456-.233 4.764 7.279v-6.44l-1.215-.139c-.093-.514.28-.887.747-.933zM1.936 1.035l13.31-.98c1.634-.14 2.055-.047 3.082.7l4.249 2.986c.7.513.933.653.933 1.213v16.378c0 1.026-.373 1.634-1.68 1.726l-15.458.934c-.98.047-1.448-.093-1.962-.747l-3.129-4.06c-.56-.747-.793-1.306-.793-1.96V2.667c0-.839.374-1.54 1.448-1.632z"/></svg>')
notion_btn = (f'''<a class="notion-btn" href="{e(NOTION_BOARD)}" target="_blank" rel="noopener">
      {NOTION_SVG}
      <span><span class="nb-t">Next cycle posts</span><span class="nb-s">Open the Notion board</span></span>
      <span class="nb-go">{AR}</span>
    </a>''' if NOTION_BOARD else "")
board_line = ("The content board for next month is on the Notion page below." if NOTION_BOARD else
              "The content board for next month will follow on Notion.")
ahead = f'''
<div class="wrap" id="ahead"><section class="block"><div class="block-head"><h2>Looking ahead</h2></div>
  <div class="signoff">
    <div class="signoff-text">
      <p>One month, {n_posts} threads and {n_comments} comments. Those threads now sit on the first page of Google for {n_unique} different searches in the UK, {len({k[1] for k in KW if k[5] == 1})} of them at #1 in their section, and every one is screenshotted above. {n_brand} searches for the clinic by name now return one of our threads, and {pos_share:.0%} of Reddit mentions of {CLIENT} read positive.</p>
      <p>{board_line} Every post is drafted, with the searches it is written to rank for. Comments from the {CLIENT} team are welcome before anything goes live.</p>
    </div>
    {notion_btn}
  </div>
</section></div>
'''

# ---------- footer ----------
footer = f'''
<footer id="method"><div class="m81card"><div class="m81-watermark">M81 MEDIA</div><div class="m81card-inner">
  <div class="m81-lock"><img src="m81-logo.png" alt="M81"><span class="bname">M81</span></div>
  <div class="m81-method"><p class="fineprint"><strong>Method.</strong> Each ranking was captured from a live google.co.uk results page, searched from London, between 25 and 26 Oct 2026. The dark panel on the right of every screenshot is the raw data for that search. A keyword counts as ranking when our own thread appears on the first page as its own result, and it is counted once for each of our threads that appears ({n_rank} rankings, {n_unique} distinct searches). Every screenshot was checked by hand: captures where our thread only appeared as a sub-link under someone else's result, or where the capture could not confirm our thread, were removed, along with searches that only restate a post title. Views, subreddit rank and audience come from each thread's Reddit Post Insights at the time of capture. Sentiment and share of voice come from our brand monitoring of Reddit since 27 Sep 2026. Rankings shift by location, device and date, so each capture is a snapshot from the day it was run.</p>
  <div class="src"><span>Search engine: Google UK</span><span>Location: London</span><span>Device: Desktop</span><span>Captured: 25 Oct 2026</span><span>Period: 27 Sep to 27 Oct 2026</span></div></div>
</div></div></footer>
'''

lightbox = (ROOT / "build" / "lightbox.html").read_text()
css = (ROOT / "build" / "style.css").read_text()
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Invisible Braces 4U: Reddit Report, Cycle 01 | M81</title>
<meta name="description" content="{CLIENT} on Reddit, Cycle 01: {n_rank} Google rankings, {n_first} at #1, {VIEWS_LABEL} views, {n_posts} posts and {n_comments} branded comments.">
<link rel="icon" href="m81-logo.png">
<style>{css}</style></head><body>
{hero}{glance}{sentiment}{own}{posts_html}{comments}{ahead}{footer}{lightbox}</body></html>'''
(ROOT / "index.html").write_text(html)
print(f"views {views:,}  uk {uk_share:.1%}  rankings {n_rank}  unique {n_unique}  #1 {n_first}  brand {n_brand} (#1 {n_brand1})  surf {dict(surf)}  subs {n_subs}")
if not NOTION_BOARD:
    print("NOTE: data.NOTION_BOARD is not set, so the Looking ahead Notion button is hidden.")
