# -*- coding: utf-8 -*-
"""
Rebuilds index.html from weeks.json. Run after recap.py.

    python tools/make_index.py

Add the new week to tools/weeks.json first:
    "weeks": { "7": "One line describing the week.", ... }
The three headline figures are recomputed from Sleeper, never typed.
"""
import io, json, pathlib, urllib.request
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "tools" / "weeks.json").read_text(encoding="utf-8"))

SEASONS = [("1125081564969459721", 14)]  # placeholder, replaced below
SEASONS = [("1125051564969459721", 14), ("1250184185579048960", 14), ("1389693216323817472", None)]
CLS = {1: "12", 2: "12", 3: "12", 4: "12", 6: "12",
       5: "11", 7: "11", 8: "11", 9: "11", 10: "11", 11: "11", 12: "11"}

def api(p):
    with urllib.request.urlopen("https://api.sleeper.app/v1/" + p) as r:
        return json.load(r)

def cross_class_alltime():
    tally = {"11": 0, "12": 0}
    state_week = api("state/nfl")["leg"] - 1          # last completed week
    for lid, last in SEASONS:
        upto = last if last else state_week
        for wk in range(1, upto + 1):
            by = defaultdict(list)
            for m in api("league/%s/matchups/%d" % (lid, wk)):
                if m.get("matchup_id") is not None:
                    by[m["matchup_id"]].append(m)
            for g in by.values():
                if len(g) != 2:
                    continue
                a, b = g
                hi, lo = (a, b) if a["points"] >= b["points"] else (b, a)
                if CLS[hi["roster_id"]] != CLS[lo["roster_id"]]:
                    tally[CLS[hi["roster_id"]]] += 1
    return tally

tally = cross_class_alltime()
weeks = sorted(((int(k), v) for k, v in CFG["weeks"].items()), reverse=True)
latest = weeks[0][0]

cards = []
for i, (n, desc) in enumerate(weeks):
    cls = "card recap" if i == 0 else "card recap old"
    kicker = "Latest recap &middot; %s season" % CFG["season"] if i == 0 else "Recap &middot; %s season" % CFG["season"]
    cards.append(
        '    <a class="%s" href="week-%d.html">\n'
        '      <div class="card-k">%s</div>\n'
        '      <div class="card-t">Week %d</div>\n'
        '      <p class="card-d">%s</p>\n'
        '    </a>' % (cls, n, kicker, n, desc))
cards.append(
    '    <a class="card rivalry" href="2011-vs-2012.html">\n'
    '      <div class="card-k">The rivalry</div>\n'
    '      <div class="card-t">2011 vs 2012</div>\n'
    "      <p class=\"card-d\">Every season's champion and playoff top six, colour-coded by pledge class, plus the "
    'cross-class head-to-head record for the years the game logs survive.</p>\n'
    '    </a>')
cards.append(
    '    <a class="card records" href="record-book.html">\n'
    '      <div class="card-k">All-time records</div>\n'
    '      <div class="card-t">The Record Book</div>\n'
    '      <p class="card-d">Champions, rings by manager, the all-time standings, single-week highs and lows, '
    'biggest beatdowns, longest streaks, and who can actually set a lineup.</p>\n'
    '    </a>')

HTML = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>EX Champions League</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{
  --surface:#131519; --surface-2:#1B1E24;
  --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
  --rule:#2A2E36; --rule-strong:#3A3F49;
  --c11:#4884CE; --c12:#C08A1E;
}
*{box-sizing:border-box}
body{background:var(--surface); color:var(--ink);
  font-family:"Newsreader",Georgia,serif; font-size:17px; line-height:1.55; margin:0;
  padding-block:52px 64px; padding-left:20px; padding-right:20px; -webkit-font-smoothing:antialiased}
.wrap{max-width:820px; margin:0 auto}
.disp{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800; line-height:.92}
.eyebrow,.card-k,.stat-k,footer{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}
.eyebrow{font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 16px}
h1.disp{font-size:clamp(50px,11vw,88px); margin:0; letter-spacing:.01em}
.standfirst{font-size:19px; color:var(--ink-2); max-width:56ch; margin:20px 0 0;
  border-left:2px solid var(--rule-strong); padding-left:16px}
.stats{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:34px 0 6px}
.stat{background:var(--surface-2); border:1px solid var(--rule); border-radius:3px; padding:14px 16px}
.stat-k{font-size:9.5px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3)}
.stat-v{display:flex; align-items:baseline; gap:7px; margin-top:7px;
  font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800;
  font-size:clamp(30px,6vw,42px); line-height:.85; font-variant-numeric:tabular-nums}
.a{color:var(--c11)} .b{color:var(--c12)}
.dash{font-weight:500; color:var(--ink-3); font-size:.8em}
.cards{display:grid; gap:14px; margin-top:40px}
a.card{display:block; text-decoration:none; color:inherit; background:var(--surface-2);
  border:1px solid var(--rule); border-left:3px solid var(--c11); border-radius:3px;
  padding:22px 24px; transition:border-color .15s, background .15s}
a.card.recap{border-left-color:var(--ink-3)}
a.card.recap.old{opacity:.72}
a.card.recap.old .card-t{font-size:28px}
a.card.rivalry{border-left-color:var(--c11)}
a.card.records{border-left-color:var(--c12)}
a.card:hover,a.card:focus-visible{background:#20242c; border-color:var(--rule-strong)}
a.card:focus-visible{outline:2px solid var(--c11); outline-offset:3px}
.card-k{font-size:9.5px; font-weight:600; letter-spacing:.13em; text-transform:uppercase; color:var(--ink-3)}
.card-t{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800;
  font-size:38px; line-height:1; margin:8px 0 9px}
.card-d{font-size:15.5px; color:var(--ink-2); margin:0; max-width:56ch}
footer{margin-top:48px; padding-top:16px; border-top:1px solid var(--rule);
  font-size:10.5px; letter-spacing:.05em; color:var(--ink-3); line-height:1.8}
@media (max-width:620px){
  .stats{grid-template-columns:1fr}
  .card-t{font-size:31px}
}
</style>
</head>
<body>
<div class="wrap">
  <p class="eyebrow">Sigma Chi &nbsp;&middot;&nbsp; Washington &amp; Lee</p>
  <h1 class="disp">EX Champions League</h1>
  <p class="standfirst">%(standfirst)s</p>

  <div class="stats">
    <div class="stat">
      <div class="stat-k">Championships</div>
      <div class="stat-v"><span class="a">%(t11)d</span><span class="dash">&ndash;</span><span class="b">%(t12)d</span></div>
    </div>
    <div class="stat">
      <div class="stat-k">Top-six finishes</div>
      <div class="stat-v"><span class="a">%(p11)d</span><span class="dash">&ndash;</span><span class="b">%(p12)d</span></div>
    </div>
    <div class="stat">
      <div class="stat-k">Cross-class games</div>
      <div class="stat-v"><span class="a">%(x11)d</span><span class="dash">&ndash;</span><span class="b">%(x12)d</span></div>
    </div>
  </div>

  <div class="cards">
%(cards)s
  </div>

  <footer>Sources: Yahoo Fantasy archive and Record Book (2014&ndash;2023), the commissioner&rsquo;s keeper spreadsheet, and the Sleeper API (2024&ndash;%(season)s).<br>
  Last updated %(updated)s.</footer>
</div>
</body>
</html>
""" % {
    "standfirst": CFG["standfirst"],
    "t11": CFG["titles"]["11"], "t12": CFG["titles"]["12"],
    "p11": CFG["topsix"]["11"], "p12": CFG["topsix"]["12"],
    "x11": tally["11"], "x12": tally["12"],
    "cards": "\n".join(cards),
    "season": CFG["season"],
    "updated": CFG["updated"],
}

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("  wrote index.html  latest=week %d  cross-class all-time %d-%d" % (latest, tally["11"], tally["12"]))
