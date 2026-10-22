# -*- coding: utf-8 -*-
import io, os
# --- repo-relative output (works locally and in the cloud routine) -----------
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent      # repo root
def publish(name, body):
    """Write a full standalone document to <repo>/<name>."""
    head = ('<!doctype html>\n<html lang="en" data-theme="dark">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="robots" content="noindex, nofollow">\n')
    if body.lstrip().startswith("<!doctype"):
        doc = body
    else:
        i = body.index("</style>") + len("</style>")
        doc = head + body[:i] + "\n</head>\n<body>\n" + body[i:] + "\n</body>\n</html>\n"
    p = ROOT / name
    p.write_text(doc, encoding="utf-8")
    print("  wrote", p.name, p.stat().st_size, "bytes")
    return p
E,T = "11","12"

CHAMPS=[
 ("2014","Detrick",T,""),("2015","Dan",E,""),("2016","Tyler",T,""),
 ("2017","Tyler",T,""),("2018","Armstrong",E,""),("2019","Dan",E,""),
 ("2020","Detrick",T,""),("2021","Scott",E,""),("2022","Taylor",T,""),
 ("2023","Tyler",T,""),("2024","Dan",E,""),("2025","Greg",E,""),
]
CLASSOF={"Tyler":T,"Max":T,"Sam":T,"Taylor":T,"Detrick":T,"Armstrong":E,"Scott":E,"Joe":E,"Dan":E,"Greg":E,"Tom":E,"Brian":E}
TITLES=[("Dan",3,"2015, 2019, 2024"),("Tyler",3,"2016, 2017, 2023"),("Detrick",2,"2014, 2020"),
        ("Armstrong",1,"2018"),("Scott",1,"2021"),("Taylor",1,"2022"),("Greg",1,"2025")]
NOTITLE=["Brian","Joe","Max","Sam","Tom"]

STAND=[("YoSoyFiesta","Dan",22,12,3764.3,3334.9,110.71),("Uncle Rico","Greg",22,12,3640.7,3217.5,107.08),
 ("Table Smashers","Tyler",20,14,3755.5,3490.9,110.46),("scert","Scott",18,16,3912.0,3735.8,115.06),
 ("maxhagler","Max",18,16,3493.1,3539.5,102.74),("vaught12","Taylor",18,16,3486.2,3508.7,102.53),
 ("Roughnecks","Joe",17,17,3574.1,3573.3,105.12),("Kids College Funds","Armstrong",17,17,3570.3,3712.5,105.01),
 ("The Skin","Sam",14,20,3478.6,3660.0,102.31),("Team bxkeegan","Brian",14,20,3178.1,3484.8,93.47),
 ("Win One for the Lipper","Tom",13,21,3371.6,3579.7,99.17),("Cooking With Friends","Detrick",11,23,3181.8,3568.7,93.58)]

BEST=[(167.86,"2025","12","Table Smashers"),(156.70,"2026","5","Uncle Rico"),
 (154.64,"2024","11","maxhagler"),(154.16,"2024","2","scert"),
 (153.38,"2024","11","Table Smashers"),(152.82,"2025","8","Roughnecks")]
WORST=[(27.50,"2025","12","Team bxkeegan"),(42.64,"2024","2","Cooking With Friends"),(48.10,"2025","11","Team bxkeegan"),
 (52.28,"2025","14","Team bxkeegan"),(52.62,"2025","6","Cooking With Friends"),(54.40,"2025","10","Team bxkeegan")]
BLOW=[(97.04,"2025","12","Table Smashers",167.86,"Kids College Funds",70.82),
 (95.52,"2025","10","scert",149.92,"Team bxkeegan",54.40),
 (91.82,"2025","12","Uncle Rico",119.32,"Team bxkeegan",27.50),
 (68.16,"2024","2","vaught12",110.80,"Cooking With Friends",42.64),
 (65.86,"2026","4","YoSoyFiesta",150.48,"maxhagler",84.62)]
CLOSE=[(0.10,"2026","2","maxhagler",118.56,"Kids College Funds",118.46),
 (0.46,"2025","8","Uncle Rico",115.42,"Table Smashers",114.96),
 (0.64,"2024","6","Uncle Rico",112.80,"Kids College Funds",112.16),
 (0.68,"2024","14","scert",145.68,"YoSoyFiesta",145.00),
 (0.94,"2024","9","Team bxkeegan",115.70,"Table Smashers",114.76)]
STREAK=[("Uncle Rico","Greg",14,4),("YoSoyFiesta","Dan",7,3),("Roughnecks","Joe",6,5),
 ("Table Smashers","Tyler",5,2),("Kids College Funds","Armstrong",5,6),("maxhagler","Max",5,6),
 ("vaught12","Taylor",5,3),("The Skin","Sam",4,5),("Team bxkeegan","Brian",4,7),
 ("Win One for the Lipper","Tom",4,4),("Cooking With Friends","Detrick",3,9),("scert","Scott",3,3)]
EFF=[("Table Smashers","Tyler",92.0,325.8,2),("scert","Scott",91.7,351.9,5),("YoSoyFiesta","Dan",91.6,344.0,5),
 ("Roughnecks","Joe",90.3,383.7,2),("Cooking With Friends","Detrick",89.3,379.4,4),("vaught12","Taylor",89.2,420.9,2),
 ("Uncle Rico","Greg",88.9,453.7,2),("Win One for the Lipper","Tom",88.9,420.9,5),("The Skin","Sam",87.4,503.5,3),
 ("maxhagler","Max",87.0,522.5,1),("Kids College Funds","Armstrong",86.6,553.7,3),("Team bxkeegan","Brian",86.1,512.8,1)]
BADWK=[(44.5,"2025","12","Team bxkeegan",27.50,61.80),(49.5,"2025","6","Team bxkeegan",57.16,115.36),
 (59.6,"2025","10","Team bxkeegan",54.40,91.20),(64.3,"2025","9","Kids College Funds",78.32,121.82),
 (65.3,"2025","4","maxhagler",71.58,109.66),(66.1,"2026","1","vaught12",79.20,119.76)]
YAHOO=[("Most points, one week","Joe vs. Sam","Wk 5, 2019","205.84"),
 ("Largest margin of victory","Joe vs. Sam","Wk 5, 2019","116.20"),
 ("Most points, season","Tyler","2014","2051"),
 ("Most offensive points, season","Detrick","2014","1765"),
 ("Most wins, season","Dan","2019","12"),
 ("Longest win streak","Armstrong","2014","8"),
 ("Most losses, season","Sam","2014","13"),
 ("Longest losing streak","Ned Lundvall","2015","10"),
 ("Fewest points, one week","Dan","Wk 14, 2020","43.30"),
 ("Largest average margin of victory","Tom","2020","43.54"),
 ("Largest average margin of defeat","Detrick","2019","46.23"),
 ("Smallest margin of defeat","Detrick vs. Sam","Wk 12, 2021","0.06"),
 ("Hardest schedule","Max","2014","130.73"),
 ("Easiest schedule","Drew Jacoby","2017","88.99")]

def chip(c):
    return f'<span class="chip c{c}">&rsquo;{c}</span>' if c in (E,T) else '<span class="chip cx">?</span>'

champ_rows="".join(
  f'''<li class="crow">
  <span class="cy">{y}</span>
  <span class="cm">{'<em>contested</em>' if m=="contested" else m}</span>
  {chip(c) if c else '<span class="chip cx">&mdash;</span>'}
  <span class="cn">{n}</span></li>''' for y,m,c,n in CHAMPS)

title_rows="".join(
  f'<div class="trow"><span class="tn">{m}</span>{chip(CLASSOF[m])}'
  f'<span class="rings">{"".join(f"<span class=\"ring c{CLASSOF[m]}\"></span>" for _ in range(n))}</span>'
  f'<span class="tc">{n}</span><span class="ty">{yrs}</span></div>' for m,n,yrs in TITLES)

stand_rows="".join(
  f'<tr><td>{t}</td><td class="dim">{who}</td><td><b>{w}&ndash;{l}</b></td><td>{pf:.1f}</td><td>{pa:.1f}</td>'
  f'<td class="c{CLASSOF[who]}">{avg:.2f}</td></tr>' for t,who,w,l,pf,pa,avg in STAND)

def wk_rows(rows, cls):
    return "".join(f'<li><span class="v {cls}">{p:.2f}</span><span class="w">{t}</span>'
                   f'<span class="when">{s} &middot; wk {wk}</span></li>' for p,s,wk,t in rows)

def game_rows(rows, cls):
    return "".join(f'<li><span class="v {cls}">{m:.2f}</span><span class="w">{hw} <b>{hp:.2f}</b> '
                   f'<span class="dim">def</span> {lw} {lp:.2f}</span><span class="when">{s} &middot; wk {wk}</span></li>'
                   for m,s,wk,hw,hp,lw,lp in rows)

streak_rows="".join(
  f'<tr><td>{t}</td><td class="dim">{who}</td><td class="good">{w}</td><td class="bad">{l}</td></tr>'
  for t,who,w,l in STREAK)

eff_rows="".join(
  f'<tr><td>{t}</td><td class="dim">{who}</td><td><b>{e:.1f}%</b></td><td>{lost:.0f}</td><td>{pc}</td></tr>'
  for t,who,e,lost,pc in EFF)

bad_rows="".join(
  f'<li><span class="v bad">{e:.1f}%</span><span class="w">{t} &mdash; scored {a:.2f} of a possible {o:.2f}</span>'
  f'<span class="when">{s} &middot; wk {wk}</span></li>' for e,s,wk,t,a,o in BADWK)

yahoo_rows="".join(
  f'<tr><td>{r}</td><td>{h}</td><td class="dim">{w}</td><td class="num">{v}</td></tr>' for r,h,w,v in YAHOO)

HTML=f'''<title>EX Champions Record Book</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{{
  --surface:#FBFBFC; --surface-2:#F1F2F5;
  --ink:#16181C; --ink-2:#474B54; --ink-3:#787D88;
  --rule:#DCDEE4; --rule-strong:#C2C6D0;
  --c11:#1F5FA9; --c12:#A9760C;
  --c11-wash:#E6EDF7; --c12-wash:#F6EEDC;
  --good:#1F5FA9; --bad:#A9760C; --unk:#B4B8C2;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --surface:#131519; --surface-2:#1B1E24;
    --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
    --rule:#2A2E36; --rule-strong:#3A3F49;
    --c11:#4884CE; --c12:#C08A1E;
    --c11-wash:#1A2533; --c12-wash:#2A2313;
    --good:#4884CE; --bad:#C08A1E; --unk:#474C57;
  }}
}}
:root[data-theme="dark"]{{
  --surface:#131519; --surface-2:#1B1E24;
  --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
  --rule:#2A2E36; --rule-strong:#3A3F49;
  --c11:#4884CE; --c12:#C08A1E;
  --c11-wash:#1A2533; --c12-wash:#2A2313;
  --good:#4884CE; --bad:#C08A1E; --unk:#474C57;
}}
*{{box-sizing:border-box}}
body{{background:var(--surface); color:var(--ink);
  font-family:"Newsreader",Georgia,serif; font-size:17px; line-height:1.55; margin:0;
  padding-block:40px 64px; padding-left:20px; padding-right:20px; -webkit-font-smoothing:antialiased}}
.wrap{{max-width:900px; margin:0 auto}}
.disp{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800; line-height:.92; letter-spacing:.01em}}
.eyebrow,.chip,.cn,.when,.v,.tc,.ty,.num,table,caption,footer,.cy,.rank,.sub-h2
  {{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}}
.eyebrow{{font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 18px}}
h1.disp{{font-size:clamp(50px,10.5vw,92px); margin:0; text-wrap:balance}}
.standfirst{{font-size:19px; color:var(--ink-2); max-width:60ch; margin:20px 0 0;
  border-left:2px solid var(--rule-strong); padding-left:16px}}
h2.disp{{font-size:29px; margin:54px 0 4px; letter-spacing:.02em}}
.sub-h{{font-size:14.5px; color:var(--ink-3); margin:0 0 16px; max-width:64ch}}
.chip{{font-size:10px; font-weight:600; letter-spacing:.05em; padding:2px 6px; border-radius:2px; flex:none}}
.chip.c11{{background:var(--c11-wash); color:var(--c11)}}
.chip.c12{{background:var(--c12-wash); color:var(--c12)}}
.chip.cx{{background:var(--surface-2); color:var(--ink-3)}}
/* champions */
.champs{{list-style:none; margin:0; padding:0}}
.crow{{display:grid; grid-template-columns:62px minmax(96px,auto) 44px 1fr; gap:12px; align-items:center;
  padding:9px 0; border-bottom:1px solid var(--rule)}}
.cy{{font-size:15px; font-weight:600; color:var(--ink-2); font-variant-numeric:tabular-nums}}
.cm{{font-size:18px; font-weight:500}}
.cm em{{color:var(--ink-3); font-size:16px}}
.cn{{font-size:10.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-3)}}
/* titles */
.trow{{display:grid; grid-template-columns:88px 42px auto 26px 1fr; gap:10px; align-items:center;
  padding:9px 0; border-bottom:1px solid var(--rule)}}
.tn{{font-size:17px; font-weight:500}}
.rings{{display:flex; gap:5px}}
.ring{{width:14px; height:14px; border-radius:50%}}
.ring.c11{{background:var(--c11)}} .ring.c12{{background:var(--c12)}}
.tc{{font-size:13px; font-weight:600; color:var(--ink-3); text-align:right}}
.ty{{font-size:11.5px; color:var(--ink-3); letter-spacing:.04em}}
.none{{margin-top:12px; font-size:15px; color:var(--ink-3); font-style:italic}}
/* extremes lists */
.cols{{display:grid; grid-template-columns:1fr 1fr; gap:14px 30px}}
.ex{{list-style:none; margin:0; padding:0}}
.ex li{{display:grid; grid-template-columns:72px 1fr; gap:10px; align-items:baseline;
  padding:8px 0; border-bottom:1px solid var(--rule)}}
.ex .v{{font-size:15px; font-weight:600; font-variant-numeric:tabular-nums}}
.ex .v.good{{color:var(--good)}} .ex .v.bad{{color:var(--bad)}}
.ex .w{{font-size:15.5px}}
.ex .when{{grid-column:2; font-size:10.5px; letter-spacing:.05em; color:var(--ink-3); text-transform:uppercase}}
.sub-h2{{font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3); margin:0 0 6px}}
/* tables */
.tablewrap{{overflow-x:auto; border:1px solid var(--rule); border-radius:3px; margin-top:12px}}
table{{border-collapse:collapse; width:100%; font-size:13.5px}}
th,td{{text-align:left; padding:8px 13px; border-top:1px solid var(--rule); white-space:nowrap;
  font-variant-numeric:tabular-nums}}
th{{font-weight:600; font-size:10.5px; letter-spacing:.07em; text-transform:uppercase;
  color:var(--ink-3); background:var(--surface-2)}}
td.dim{{color:var(--ink-3)}} td.c11{{color:var(--c11)}} td.c12{{color:var(--c12)}}
td.good{{color:var(--good); font-weight:600}} td.bad{{color:var(--bad); font-weight:600}}
td.num{{font-weight:600}}
.notes{{font-size:15.5px; color:var(--ink-2); max-width:64ch}}
.notes p{{margin:0 0 12px}}
.notes strong{{color:var(--ink); font-weight:500}}
footer{{margin-top:46px; padding-top:16px; border-top:1px solid var(--rule);
  font-size:10.5px; letter-spacing:.05em; color:var(--ink-3); line-height:1.8}}
@media print{{
  *{{ -webkit-print-color-adjust:exact !important; print-color-adjust:exact !important; }}
  @page{{ margin:0; }}
  html,body{{ background:var(--surface) !important; }}
  body{{ padding:15mm 13mm; font-size:10.5pt; }}
  .wrap{{ max-width:none; margin:0; }}
  h1.disp{{ font-size:46pt; }}
  h2.disp{{ font-size:19pt; margin-top:26px; break-after:avoid; page-break-after:avoid; }}
  .standfirst{{ font-size:12pt; }}
  .row,.hrow,.fig,.figs,.crow,.trow,.ex li,.notes p,tr,footer,.tablewrap
    {{ break-inside:avoid; page-break-inside:avoid; }}
  .tablewrap{{ overflow:visible; }}
  .legend{{ break-inside:avoid; }}
}}
@media (max-width:660px){{
  .cols{{grid-template-columns:1fr}}
  .crow{{grid-template-columns:56px 1fr 40px; row-gap:2px}}
  .crow .cn{{grid-column:2 / -1}}
  .trow{{grid-template-columns:80px 38px auto 24px; row-gap:2px}}
  .trow .ty{{grid-column:1 / -1}}
}}
</style>

<div class="wrap">
  <p class="eyebrow">EX Champions League &nbsp;&middot;&nbsp; Sigma Chi &nbsp;&middot;&nbsp; Washington &amp; Lee</p>
  <h1 class="disp">The Record Book</h1>
  <p class="standfirst">Every champion, every extreme, and every number worth arguing about &mdash; assembled from the Yahoo archive (2014&ndash;2023), the commissioner&rsquo;s keeper spreadsheet, and the Sleeper API (2024&ndash;2026).</p>

  <h2 class="disp">Champions</h2>
  <p class="sub-h">Twelve seasons on record. Six titles to the class of 2011, six to the class of 2012 &mdash; and the gap has never been wider than one.</p>
  <ul class="champs">{champ_rows}</ul>



  <h2 class="disp">Rings</h2>
  <p class="sub-h">Seven winners across twelve seasons. Five men have never held the trophy.</p>
  {title_rows}
  <p class="none">Still waiting: {", ".join(NOTITLE)}.</p>

  <h2 class="disp">All-time record</h2>
  <p class="sub-h">Sleeper era only &mdash; 2024, 2025 and 2026 through week 6, the seasons with surviving game-by-game results. Forty games each.</p>
  <div class="tablewrap"><table>
    <thead><tr><th scope="col">Team</th><th scope="col">Manager</th><th scope="col">W&ndash;L</th>
    <th scope="col">Points for</th><th scope="col">Points against</th><th scope="col">Avg</th></tr></thead>
    <tbody>{stand_rows}</tbody>
  </table></div>

  <h2 class="disp">Single-week extremes</h2>
  <div class="cols">
    <div><p class="sub-h2">Highest scores</p><ul class="ex">{wk_rows(BEST,'good')}</ul></div>
    <div><p class="sub-h2">Lowest scores</p><ul class="ex">{wk_rows(WORST,'bad')}</ul></div>
  </div>

  <h2 class="disp">Beatdowns and heartbreaks</h2>
  <div class="cols">
    <div><p class="sub-h2">Biggest margins</p><ul class="ex">{game_rows(BLOW,'good')}</ul></div>
    <div><p class="sub-h2">Closest finishes</p><ul class="ex">{game_rows(CLOSE,'bad')}</ul></div>
  </div>

  <h2 class="disp">Streaks</h2>
  <p class="sub-h">Longest runs in the Sleeper era, counted across season boundaries.</p>
  <div class="tablewrap"><table>
    <thead><tr><th scope="col">Team</th><th scope="col">Manager</th><th scope="col">Best win streak</th><th scope="col">Worst losing streak</th></tr></thead>
    <tbody>{streak_rows}</tbody>
  </table></div>

  <h2 class="disp">Who can actually set a lineup</h2>
  <p class="sub-h">Points scored as a share of the best lineup that roster could have started, every week since 2024. This measures the manager, not the draft.</p>
  <div class="tablewrap"><table>
    <thead><tr><th scope="col">Team</th><th scope="col">Manager</th><th scope="col">Efficiency</th>
    <th scope="col">Points benched</th><th scope="col">Perfect weeks</th></tr></thead>
    <tbody>{eff_rows}</tbody>
  </table></div>
  <p class="sub-h2" style="margin-top:22px">Worst single weeks of management</p>
  <ul class="ex">{bad_rows}</ul>

  <h2 class="disp">The Yahoo years</h2>
  <p class="sub-h">All-time records from Yahoo&rsquo;s own Record Book, covering 2014 through 2023. Drew Jacoby and Ned Lundvall have since left the league; Greg took over Drew&rsquo;s franchise in 2019.</p>
  <div class="tablewrap"><table>
    <thead><tr><th scope="col">Record</th><th scope="col">Holder</th><th scope="col">When</th><th scope="col">Value</th></tr></thead>
    <tbody>{yahoo_rows}</tbody>
  </table></div>

  <h2 class="disp">Things worth knowing</h2>
  <div class="notes">
    <p><strong>The most violent game ever played was Joe hanging 205.84 on Sam</strong> in week 5 of 2019 &mdash; a 116.20-point win that remains both the highest single score and the largest margin in league history.</p>
    <p><strong>Dan founded this thing, not Tyler.</strong> Yahoo lists Dan as commissioner in 2014 and 2015 with Tyler as his co-commissioner. Tyler has run it since 2017.</p>
    <p><strong>Dan&rsquo;s team was called &ldquo;BXK Sux&rdquo; for years</strong> &mdash; bxkeegan sucks. He named his franchise after trash-talking Brian, and kept it that way through at least 2021.</p>
    <p><strong>Greg has the longest win streak of the Sleeper era, at fourteen and counting.</strong> The easiest schedule ever played (88.99 a week, 2017) belongs to Drew Jacoby &mdash; whose franchise Greg took over in 2019.</p>
    <p><strong>Brian owns the floor.</strong> The three lowest scores of the Sleeper era are all his, including a 27.50 in week 12 of 2025 &mdash; from a roster that could have started 61.80.</p>
    <p><strong>Detrick has two rings and the worst losing streak on record.</strong> Champion in 2014 and 2020, then nine straight defeats. <strong>Sam owns the other end</strong> &mdash; 13 losses in 2014 is still the most in a single season.</p>
    <p><strong>Tyler manages better than anyone</strong> &mdash; 91.8% career efficiency and the fewest points left on the bench. Scott sits two tenths behind him, but has four perfect weeks to Tyler&rsquo;s one.</p><p><strong>The closest game in Sleeper history happened this season.</strong> Max beat Armstrong by <b>0.10</b> in week 2 of 2026, with Davante Adams and 35.50 sitting on Max&rsquo;s bench.</p>
  </div>

  <footer>Sleeper-era figures cover 2024, 2025 and week 1 of 2026. Yahoo figures cover 2014&ndash;2023 and include the predecessor league.<br>
  Sources: Yahoo Fantasy archive and Record Book, Sigmach Fantasy Football.xlsx, and the Sleeper API. Updated 20 October 2026.</footer>
</div>
'''
publish("record-book.html", HTML)
