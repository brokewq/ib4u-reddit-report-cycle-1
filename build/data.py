"""Cycle 01 source data for the Invisible Braces 4U (IB4U) Reddit report.

Posts and comments come from brand-cycle-cmuks7q1r0006gsmdi8a3kz3y (2).csv; views, daily subreddit rank
and UK share come from the Reddit Post Insights screenshots shared in chat (saved in ins/).
Keyword rows come from the SERP crawler output in "FuckING final IB4U SERP /data"
(captured 25 to 26 Oct 2026, google.co.uk, London, desktop). Only the curated (kept) keywords go in the report.
Sentiment and share of voice come from the brand-monitoring dashboard screenshot (since 27 Sep 2026).
"""

SERP_DIR = "/Users/aniket/Downloads/FuckING final IB4U SERP "

# id = Reddit thread id. rank = daily subreddit rank from Post Insights, uk = UK share of views (%).
# lead = top country when the UK is not the top country on the screenshot.
POSTS = [
    dict(id="1wrnpet", date="2026-09-27", sub="r/Invisalign", replies=5,
         views=7_000, vlabel="7K", rank=3, uk=36.5, ins="1wrnpet",
         title="best invisalign provider in london ?",
         url="https://www.reddit.com/r/Invisalign/comments/1wrnpet/best_invisalign_provider_in_london"),
    dict(id="1wtig4o", date="2026-09-29", sub="r/Invisalign", replies=4,
         views=5_800, vlabel="5.8K", rank=1, uk=None, lead="United States", ins="1wtig4o",
         title="Anyone been to invisiblebraces4u in Manchester?",
         url="https://www.reddit.com/r/Invisalign/comments/1wtig4o/anyone_been_to_invisiblebraces4u_in_manchester"),
    dict(id="1wwok59", date="2026-10-03", sub="r/Invisalign", replies=4,
         views=2_500, vlabel="2.5K", rank=None, uk=38.6, ins="1wwok59",
         title="Why do Invisalign prices vary so much in London?",
         url="https://www.reddit.com/r/Invisalign/comments/1wwok59/why_do_invisalign_prices_vary_so_much_in_london"),
    dict(id="1wyfc44", date="2026-10-05", sub="r/Invisalign", replies=3,
         views=1_700, vlabel="1.7K", rank=None, uk=34.1, ins="1wyfc44",
         title="Anyone been to invisiblebraces4u for Invisalign in London?",
         url="https://www.reddit.com/r/Invisalign/comments/1wyfc44/anyone_been_to_invisiblebraces4u_for_invisalign"),
    dict(id="1x6gsrg", date="2026-10-15", sub="r/Invisalign", replies=3,
         views=2_000, vlabel="2K", rank=None, uk=36.3, ins="1x6gsrg",
         title="How did you choose who to go with for Invisalign in London?",
         url="https://www.reddit.com/r/Invisalign/comments/1x6gsrg/how_did_you_choose_who_to_go_with_for_invisalign"),
    dict(id="1x7mkoz", date="2026-10-16", sub="r/BirminghamUK", replies=3,
         views=3_800, vlabel="3.8K", rank=2, uk=89.0, ins="1x7mkoz",
         title="Invisalign in Birmingham, any recommendations?",
         url="https://www.reddit.com/r/BirminghamUK/comments/1x7mkoz/invisalign_in_birmingham_any_recommendations"),
    dict(id="1x8gulb", date="2026-10-17", sub="r/HENRYUKLifestyle", replies=5,
         views=33_400, vlabel="33.4K", rank=None, uk=89.7, ins="1x8gulb",
         title="Invisalign recommendation in London?",
         url="https://www.reddit.com/r/HENRYUKLifestyle/comments/1x8gulb/invisalign_recommendation_in_london"),
    dict(id="1xa5v1j", date="2026-10-19", sub="r/AskUK", replies=4,
         views=14_000, vlabel="14K", rank=53, uk=84.9, ins="1xa5v1j",
         title="How much did you pay for Invisalign in London?",
         url="https://www.reddit.com/r/AskUK/comments/1xa5v1j/how_much_did_you_pay_for_invisalign_in_london"),
    dict(id="1xaxs8y", date="2026-10-20", sub="r/Invisalign", replies=5,
         views=2_500, vlabel="2.5K", rank=16, uk=52.6, ins="1xaxs8y",
         title="Banning Dental vs invisiblebraces4u vs Impress for Invisalign in UK??",
         url="https://www.reddit.com/r/Invisalign/comments/1xaxs8y/banning_dental_vs_invisiblebraces4u_vs_impress"),
]

TITLE_ECHO = "Restates the post title; not how people search"
CONTRIVED = "Too long or specific to be a real search"
NEAR_DUP = "Near-duplicate of a kept keyword"
INFO = "Informational, not choosing or booking a provider"
LOW = "Low intent: reflective or no buying signal"
REVIEW = "Cut in the keyword review"

# (thread id, keyword) -> reason for cutting. Everything not listed is kept.
CUT = {
    ("1xaxs8y", "banning dental vs invisiblebraces4u vs impress"): TITLE_ECHO,
    ("1xaxs8y", "banning dental vs invisiblebraces4u vs impress invisalign"): TITLE_ECHO,
    ("1xaxs8y", "banning dental or invisiblebraces4u for invisalign"): CONTRIVED,
    ("1xaxs8y", "invisiblebraces4u or banning dental"): NEAR_DUP,
    ("1xaxs8y", "invisiblebraces4u or impress"): NEAR_DUP,
    ("1xaxs8y", "banning dental or impress"): NEAR_DUP,
    ("1x6gsrg", "how did you choose who to go with for invisalign in london"): TITLE_ECHO,
    ("1wwok59", "why do invisalign prices vary so much in london"): TITLE_ECHO,
    ("1wyfc44", "anyone been to invisiblebraces4u for invisalign in london"): TITLE_ECHO,
    ("1x8gulb", "invisalign london no one to ask"): CONTRIVED,
    ("1wrnpet", "narrowed down invisalign clinics uk"): CONTRIVED,
    ("1xa5v1j", "invisalign price put me off"): CONTRIVED,
    ("1xa5v1j", "invisalign just over £5000"): CONTRIVED,
    ("1x7mkoz", "invisalign in birmingham any recommendations"): TITLE_ECHO,
    # cut in the keyword review, 28 Oct
    ("1xa5v1j", "realistic invisalign cost london"): REVIEW,
    ("1xa5v1j", "invisalign go price london"): REVIEW,
    ("1xa5v1j", "is £5000 too much for invisalign uk"): REVIEW,
    ("1xa5v1j", "what did you pay for invisalign london"): REVIEW,
    ("1xa5v1j", "what people actually pay for invisalign london"): REVIEW,
    ("1xa5v1j", "invisalign london worth paying more"): REVIEW,
    ("1wrnpet", "which invisalign provider to choose"): REVIEW,
    ("1wtig4o", "invisible braces 4u manchester reviews"): REVIEW,
    ("1wtig4o", "invisible braces manchester reviews"): REVIEW,
    ("1x7mkoz", "anyone done invisalign in birmingham"): REVIEW,
    ("1x7mkoz", "anyone had invisalign in birmingham"): REVIEW,
    ("1x6gsrg", "choosing between invisalign providers"): REVIEW,
}

# keyword -> reason for cutting, applied to every thread the keyword ranks for (high-intent pass, 28 Oct).
CUT_KW = {
    "why do invisalign prices vary": INFO,
    "why do invisalign prices vary so much": INFO,
    "why do invisalign quotes vary so much": INFO,
    "why are invisalign quotes so different between clinics": INFO,
    "why is invisalign so expensive in london": INFO,
    "why does invisalign cost so much uk": INFO,
    "invisalign cost after consultation": LOW,
    "can't afford invisalign london": LOW,
    "20 trays invisalign how much": CONTRIVED,
    "quoted £5000 for invisalign is that normal": CONTRIVED,
    "invisalign quote london is this normal": CONTRIVED,
    "invisiblebraces4u or orthodontist": NEAR_DUP,
    "invisalign birmingham uk recommendations": NEAR_DUP,
}

THEMES = {
    "recs": ("London recommendations", "#f96a16"),
    "price": ("Invisalign pricing", "#c2410c"),
    "brand": ("Invisible Braces 4U by name", "#1c1611"),
    "compare": ("Clinic comparisons", "#d99a1e"),
    "regional": ("Birmingham", "#2e7d52"),
}
THEME_OF = {"1wrnpet": "recs", "1x8gulb": "recs", "1x6gsrg": "recs",
            "1xa5v1j": "price", "1wwok59": "price",
            "1wyfc44": "brand", "1wtig4o": "brand",
            "1xaxs8y": "compare", "1x7mkoz": "regional"}
NICK = {"1wrnpet": "Best provider in London", "1x8gulb": "London recommendation", "1x6gsrg": "Choosing a provider",
        "1xa5v1j": "What people paid", "1wwok59": "Why prices vary", "1wyfc44": "IB4U in London",
        "1wtig4o": "IB4U in Manchester", "1xaxs8y": "Banning vs IB4U vs Impress", "1x7mkoz": "Birmingham recs"}

# Branded comments this cycle: brand-cycle CSV (28 Sep to 21 Oct 2026) plus five shared in chat (23 and 27 Oct).
FEED = [
    ("2026-10-27", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1v8cexj/comment/19rr25pzmipad"),
    ("2026-10-27", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1w6jy02/comment/19rrh7vv6gxfl"),
    ("2026-10-27", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1sc60vk/comment/19rs6ao3atdr6"),
    ("2026-10-23", "r/AskUK", "https://www.reddit.com/r/AskUK/comments/1vc7i3j/comment/19rioblnc2kec"),
    ("2026-10-23", "r/HENRYUKLifestyle", "https://www.reddit.com/r/HENRYUKLifestyle/comments/1whuxjk/comment/19rjdorrbsbz7"),
    ("2026-10-21", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1xaxs8y/comment/19rfacwq96rac"),
    ("2026-10-21", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1xaxs8y/comment/19rf8a807t411"),
    ("2026-10-21", "r/AskUK", "https://www.reddit.com/r/AskUK/comments/1xa5v1j/comment/19repzetuab1d"),
    ("2026-10-20", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1wtnheu/comment/phwdngh"),
    ("2026-10-19", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1x5zi5r/comment/phrtbmc"),
    ("2026-10-19", "r/LondonLadies", "https://www.reddit.com/r/LondonLadies/comments/1wo6mup/comment/phr905s"),
    ("2026-10-18", "r/HENRYUKLifestyle", "https://www.reddit.com/r/HENRYUKLifestyle/comments/1x8gulb/comment/phf70iu"),
    ("2026-10-17", "r/BirminghamUK", "https://www.reddit.com/r/BirminghamUK/comments/1x7mkoz/comment/ph8vaes"),
    ("2026-10-15", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1x6gsrg/comment/pgxwqvl"),
    ("2026-10-05", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1wyfc44/comment/pe44s3i"),
    ("2026-10-03", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1wwok59/comment/pdoost6"),
    ("2026-09-30", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1wtig4o/comment/pcwn775"),
    ("2026-09-28", "r/Invisalign", "https://www.reddit.com/r/Invisalign/comments/1wrnpet/comment/pcj4q7f"),
]

# Brand mentions on Reddit since 27 Sep 2026, from the monitoring dashboard.
SENTIMENT = dict(total=21, pos=15, neu=3, neg=3)
SOV = [("r/Invisalign", 13), ("r/AskUK", 3), ("r/HENRYUKLifestyle", 2),
       ("r/BirminghamUK", 1), ("r/LondonLadies", 1), ("r/lineup_sweep", 1)]

# Patient-intent score per keyword (10 = ready-to-book head term, 1 = loosely related).
# Keyword lists in the report are ordered by this score, highest first.
INTENT = {
    # best provider / recommendations, London
    "best invisalign provider in london": 10, "best invisalign provider london": 10, "best clear aligner provider london": 10,
    "invisalign provider reviews london": 9, "invisalign dentist reviews london": 9, "invisalign london experiences": 8,
    "invisalign experience london": 8, "anyone done invisalign in london": 8, "anyone had invisalign in london": 8,
    "anyone had clear aligners in london": 8, "looking for invisalign in london": 9, "private invisalign london": 8,
    "how to choose an invisalign provider london": 8, "how to find an invisalign provider london": 8,
    "invisalign dentist or orthodontist london": 7, "invisalign from dentist or orthodontist london": 7,
    "invisalign for minor crowding london": 8, "invisalign for front teeth crowding london": 8,
    "which invisalign provider to choose": 7, "how to compare invisalign providers": 7, "comparing invisalign clinics uk": 7,
    "choosing between invisalign providers": 7, "how did you choose your invisalign provider": 6,
    "how did you find your invisalign provider": 6, "how did you pick your invisalign provider": 6,
    # pricing
    "invisalign prices london": 10, "real invisalign prices london": 9, "realistic invisalign cost london": 9,
    "invisalign cost london reddit": 9, "what did you pay for invisalign london": 8, "what people actually pay for invisalign london": 8,
    "invisalign £5000 uk": 8, "invisalign quoted £5000": 8, "invisalign over £5000 london": 8, "is £5000 too much for invisalign uk": 8,
    "quoted £5000 for invisalign is that normal": 7, "invisalign quote london is this normal": 7, "invisalign london expensive": 8,
    "invisalign go price london": 8, "invisalign cost for mild crowding london": 8, "invisalign bottom crowding price uk": 7,
    "invisalign for a few crooked teeth cost uk": 7, "invisalign cost after consultation": 6, "20 trays invisalign how much": 6,
    "can't afford invisalign london": 7, "invisalign london worth paying more": 7, "invisalign price difference between clinics": 7,
    "invisalign prices london 2026": 9, "why is invisalign so expensive in london": 7, "why does invisalign cost so much uk": 7,
    "why do invisalign prices vary": 6, "why do invisalign prices vary so much": 6, "why do invisalign quotes vary so much": 6,
    "why are invisalign quotes so different between clinics": 6,
    # Invisible Braces 4U by name
    "invisible braces 4u london": 10, "invisiblebraces4u london invisalign": 10, "anyone been to invisiblebraces4u": 9,
    "anyone done treatment at invisiblebraces4u": 9, "invisiblebraces4u free consultation": 10, "invisiblebraces4u london consultation": 10,
    "invisiblebraces4u treatment": 9, "invisiblebraces4u manchester": 10, "invisiblebraces4u manchester reviews": 10,
    "invisible braces 4u manchester reviews": 10, "invisible braces manchester reviews": 9, "anyone been to invisiblebraces4u in manchester": 8,
    "anyone had invisalign in manchester": 7, "invisalign manchester experiences": 7,
    # clinic comparisons
    "banning dental vs invisiblebraces4u": 9, "invisiblebraces4u vs banning dental": 9, "which is better banning dental or invisiblebraces4u": 9,
    "invisiblebraces4u vs impress": 9, "impress vs invisiblebraces4u": 9, "which is better impress or invisiblebraces4u": 9,
    "banning dental vs impress": 8, "impress vs banning dental": 8, "impress or invisalign uk": 7,
    "invisiblebraces4u or orthodontist": 7, "invisiblebraces4u vs orthodontist": 7,
    # Birmingham
    "best invisalign birmingham": 10, "best invisalign dentist birmingham": 10, "best invisalign orthodontist birmingham": 10,
    "best place for invisalign in birmingham": 10, "invisalign birmingham recommendations": 9, "invisalign recommendations birmingham": 9,
    "invisalign birmingham uk recommendations": 8, "invisalign in birmingham any recommendations": 8, "recommend invisalign birmingham": 9,
    "recommend an invisalign dentist in birmingham": 9, "invisalign dentist recommendations birmingham": 9,
    "invisalign orthodontist recommendations birmingham": 9, "invisalign orthodontist birmingham": 8, "invisalign in birmingham": 8,
    "where to go for invisalign in birmingham": 9, "invisalign birmingham reviews": 9, "invisalign reviews birmingham": 9,
    "invisalign birmingham experiences": 7, "anyone had invisalign in birmingham": 7, "anyone done invisalign in birmingham": 7,
    "affordable invisalign birmingham": 9, "cheap invisalign birmingham": 8,
}

# Client-facing Notion content board for next cycle's posts. The "Looking ahead" button only shows once this is set.
NOTION_BOARD = None
