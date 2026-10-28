"""Build review/index.html: every captured keyword with a keep/cut call, for the user to check
before the Cycle 01 report is final. Run build.py first so shots/ and thumbs/ exist."""
import json
from html import escape as e
from pathlib import Path

import serp
from data import CUT, CUT_KW, INTENT, POSTS

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    pairs = serp.load_pairs()
    serp.build_images(pairs)

    LABEL = {"WRONG": "Screenshot shows a different thread", "SITELINK": "Only a sub-link under someone else's result",
             "UNCLEAR": "Screenshot can't confirm it"}
    VER = {}
    for r in json.load(open(ROOT / "build" / "verify.json")):
        if r["verdict"] != "OK":
            VER[(r["t"], r["kw"])] = f'{LABEL[r["verdict"]]}: {r.get("note", "")[:140]}'

    def reason(t, kw):
        return VER.get((t, kw)) or CUT.get((t, kw)) or CUT_KW.get(kw)

    kw_threads = {}
    for tid, kw in pairs:
        if (tid, kw) not in VER:
            kw_threads.setdefault(kw, []).append(tid)

    sections, total, kept = "", 0, 0
    for n, p in enumerate(sorted(POSTS, key=lambda p: -p["views"]), 1):
        rows = sorted([(kw, v) for (tid, kw), v in pairs.items() if tid == p["id"]],
                      key=lambda x: (reason(p["id"], x[0]) is not None, -INTENT.get(x[0], 0), x[0]))
        if not rows:
            continue
        k = sum(1 for kw, _ in rows if not reason(p["id"], kw))
        total += len(rows); kept += k
        trs = ""
        for kw, (pl, file) in rows:
            shot, thumb = serp.image_names(file)
            why = reason(p["id"], kw); flag = (p["id"], kw) in VER
            others = [t for t in kw_threads.get(kw, []) if t != p["id"]]
            also = f'<em class="also">{len(others) + 1} of our threads rank here</em>' if others else ""
            score = f'<span class="score">Intent {INTENT[kw]}/10</span>' if kw in INTENT else ""
            trs += (f'<tr class="{"cut" if why else "keep"}" data-t="{p["id"]}" data-kw="{e(kw)}" data-def="{0 if why else 1}">'
                    f'<td><label class="tg"><input type="checkbox" {"" if why else "checked"}><span></span></label></td>'
                    f'<td class="kw">{e(kw)}{also}<span class="why{" flag" if flag else ""}">{e(why or "")}</span>{score}</td>'
                    f'<td class="pl">{e(pl)}</td>'
                    f'<td><a href="../{shot}" class="th" data-cap="{e(kw)}"><img loading="lazy" src="../{thumb}" alt=""></a></td></tr>')
        ins = f'<a class="insb" href="../ins/{p["ins"]}.webp" data-cap="Post insights: {e(p["title"])}"><img src="../ins/{p["ins"]}.webp" alt=""></a>'
        meta = f'{p["vlabel"]} views' + (f' · #{p["rank"]} on {p["sub"]} that day' if p["rank"] else "")
        sections += f'''
<section class="post" id="{p["id"]}">
  <div class="ph">{ins}<div>
    <div class="meta"><span class="num">Post {n:02d}</span><span class="sub">{p["sub"]}</span></div>
    <h2><a href="{p["url"]}" target="_blank" rel="noopener">{e(p["title"])}</a></h2>
    <div class="pm">{meta}</div>
    <div class="cnt"><b class="k">{k}</b> kept of <b>{len(rows)}</b> captured</div>
  </div></div>
  <table><thead><tr><th>Keep</th><th>Keyword</th><th>Where it ranks</th><th>Screenshot</th></tr></thead><tbody>{trs}</tbody></table>
</section>'''

    css = (ROOT / "build" / "review.css").read_text()
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keyword Review, IB4U Cycle 01</title><style>{css}</style></head><body>
<header><div class="in">
  <div class="eyebrow">Invisible Braces 4U · Cycle 01 · keyword review</div>
  <h1>Pick the keywords for the report</h1>
  <p>Every keyword the crawler found our threads ranking for on google.co.uk (London, 25 Oct 2026), after the screenshot check. I pre-marked each one: <b>kept</b> if it is a search from someone choosing, pricing or checking an Invisalign provider, or naming the clinic or a competitor; <b>cut</b> if it echoes the post title, is too contrived to be a real search, duplicates a kept keyword, is a "why is it so expensive" curiosity search, or has no buying signal. Every row shows the intent score I gave it (10 = ready to book). Flip any toggle, then press <b>Copy my changes</b> and paste the result back to me.</p>
  <div class="stats"><div><b id="sk">{kept}</b><span>Keyword rankings kept</span></div><div><b id="st">{total}</b><span>Captured in total</span></div><div><b id="su">0</b><span>Distinct searches kept</span></div><div><b id="sc">0</b><span>Your changes</span></div></div>
  <div class="bar"><div class="seg"><button data-f="all" class="on">All</button><button data-f="keep">Kept</button><button data-f="cut">Cut</button></div>
    <button id="copy" class="pri">Copy my changes</button><button id="reset">Reset to my picks</button><span id="msg"></span></div>
</div></header>
<main>{sections}</main>
<div class="lb" id="lb" hidden><figure><figcaption id="lbc"></figcaption><img id="lbi" alt=""></figure></div>
<script>
const KEY='ib4u-c1-review';
const rows=[...document.querySelectorAll('tbody tr')];
let saved={{}}; try{{saved=JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{}}
rows.forEach(r=>{{const id=r.dataset.t+'|'+r.dataset.kw; if(id in saved) r.querySelector('input').checked=saved[id];}});
function sync(){{
  let k=0,c=0,u=new Set(); const s={{}};
  rows.forEach(r=>{{const on=r.querySelector('input').checked, d=r.dataset.def==='1';
    r.className=on?'keep':'cut'; if(on){{k++;u.add(r.dataset.kw)}} if(on!==d){{c++; s[r.dataset.t+'|'+r.dataset.kw]=on}} r.classList.toggle('chg',on!==d);}});
  document.querySelectorAll('section.post').forEach(sec=>{{sec.querySelector('.k').textContent=sec.querySelectorAll('tr.keep').length}});
  sk.textContent=k; su.textContent=u.size; sc.textContent=c;
  try{{localStorage.setItem(KEY,JSON.stringify(s))}}catch(e){{}}
  filter();
}}
let F='all'; function filter(){{rows.forEach(r=>r.hidden=F!=='all'&&!r.classList.contains(F))}}
document.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{{F=b.dataset.f; document.querySelectorAll('.seg button').forEach(x=>x.classList.toggle('on',x===b)); filter()}});
rows.forEach(r=>r.querySelector('input').onchange=sync);
reset.onclick=()=>{{rows.forEach(r=>r.querySelector('input').checked=r.dataset.def==='1'); sync()}};
copy.onclick=async()=>{{
  const add=[],cut=[]; rows.forEach(r=>{{if(!r.classList.contains('chg'))return; const t=document.getElementById(r.dataset.t).querySelector('h2').textContent;
    (r.classList.contains('keep')?add:cut).push(`- ${{r.dataset.kw}}  [${{t}}]`)}});
  const txt=(add.length?'ADD BACK:\\n'+add.join('\\n')+'\\n':'')+(cut.length?'CUT:\\n'+cut.join('\\n'):'')||'No changes, use your picks as they are.';
  try{{await navigator.clipboard.writeText(txt); msg.textContent='Copied. Paste it in chat.'}}catch(e){{prompt('Copy this:',txt)}}
}};
document.querySelectorAll('a.th,a.insb').forEach(a=>a.onclick=ev=>{{ev.preventDefault(); lbi.src=a.getAttribute('href'); lbc.textContent=a.dataset.cap; lb.hidden=false}});
lb.onclick=()=>{{lb.hidden=true; lbi.removeAttribute('src')}};
document.onkeydown=ev=>{{if(ev.key==='Escape')lb.onclick()}};
sync();
</script></body></html>'''
    (ROOT / "review").mkdir(exist_ok=True)
    (ROOT / "review" / "index.html").write_text(html)
    print(f"captured {total}, kept {kept}")
