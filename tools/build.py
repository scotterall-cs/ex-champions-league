# -*- coding: utf-8 -*-
"""Generates the 2011 vs 2012 page from one data table."""
import csv, os, io
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
E, T, U = "11", "12", "?"

# season, platform, champion, champ_class, podium[6], h2h(12,11), ppg(12,11), era
SEASONS = [
 ("2014","Yahoo","Detrick",T,[("Detrick",T),("Armstrong",E),("Scott",E),("Tyler",T),("Dan",E),("Skylar W",U)],None,None,"m"),
 ("2015","Yahoo","Dan",E,[("Dan",E),("Drew Jacoby",U),("Brian",E),("Tyler",T),("Detrick",T),("Armstrong",E)],None,None,"m"),
 ("2016","Yahoo","Tyler",T,[("Tyler",T),("Armstrong",E),("Taylor",T),("Scott",E),("Max",T),("Dan",E)],None,None,"m"),
 ("2017","Yahoo","Tyler",T,[("Tyler",T),("Dan",E),("Detrick",T),("Sam",T),("Max",T),("Drew Jacoby",U)],None,None,"m"),
 ("2018","Yahoo","Armstrong",E,[("Armstrong",E),("Tyler",T),("Scott",E),("Detrick",T),("Drew Jacoby",U),("Tom",E)],None,None,"m"),
 ("2019","Yahoo","Dan",E,[("Dan",E),("Joe",E),("Tom",E),("Ned Lundvall",U),("Sam",T),("Taylor",T)],None,None,"m"),
 ("2020","Yahoo","Detrick",T,[("Detrick",T),("Armstrong",E),("Joe",E),("Tom",E),("Tyler",T),("Scott",E)],None,None,"m"),
 ("2021","Yahoo","Scott",E,[("Scott",E),("Tyler",T),("Armstrong",E),("Max",T),("Taylor",T),("Detrick",T)],None,None,"m"),
 ("2022","Yahoo","Taylor",T,[("Taylor",T),("Max",T),("Greg",E),("Sam",T),("Scott",E),("Armstrong",E)],None,None,"m"),
 ("2023","Yahoo","Tyler",T,[("Tyler",T),("Greg",E),("Joe",E),("Armstrong",E),("Brian",E),("Max",T)],None,None,"m"),
 ("2024","Sleeper","Dan",E,[("Dan",E),("Taylor",T),("Max",T),("Scott",E),("Tyler",T),("Brian",E)],(25,19),(106.81,105.68),"m"),
 ("2025","Sleeper","Greg",E,[("Greg",E),("Joe",E),("Dan",E),("Scott",E),("Tyler",T),("Armstrong",E)],(16,28),(96.21,105.35),"m"),
 ("2026","Sleeper",None,None,None,(9,11),(106.14,103.08),"m"),
]
CLASSOF={"Tyler":T,"Max":T,"Sam":T,"Taylor":T,"Detrick":T,"Armstrong":E,"Scott":E,"Joe":E,"Dan":E,"Greg":E,"Tom":E,"Brian":E}

# tallies across every recorded season
tc={E:0,T:0}; pod={E:0,T:0,U:0}; h2h={E:0,T:0}
for s,plat,ch,cc,pd,hh,ppg,era in SEASONS:
    if era!="m": continue
    if cc: tc[cc]+=1
    if pd:
        for _,c in pd: pod[c]+=1
    if hh: h2h[T]+=hh[0]; h2h[E]+=hh[1]

def chip(c): return f'<span class="chip c{c}">&rsquo;{c}</span>' if c in (E,T) else ''

rows=[]
for s,plat,ch,cc,pd,hh,ppg,era in SEASONS:
    if pd:
        blocks="".join(f'<span class="pod c{"unk" if c==U else c}" style="height:{34-(i*3)}px" title="{who}">{i+1}</span>'
                       for i,(who,c) in enumerate(pd))
        e=sum(1 for _,c in pd if c==E); t=sum(1 for _,c in pd if c==T); unk=sum(1 for _,c in pd if c==U)
        cap=(f"&rsquo;11 takes {e} of six" if e>t else (f"&rsquo;12 takes {t} of six" if t>e else "three apiece"))
        if unk: cap+=f" &middot; {unk} since departed"
        aria=", ".join(f"{i+1} {who}" for i,(who,c) in enumerate(pd))
        evid=f'<div class="podium" role="img" aria-label="{s} top six: {aria}">{blocks}</div><div class="cap">{cap}</div>'
    else:
        evid='<div class="notrack">SEASON IN PROGRESS</div>'
    who=f'<span class="who">{ch}</span>{chip(cc)}' if ch else (
'<span class="who tbd">in progress</span>')
    cls="row"
    rows.append(f'''    <li class="{cls}">
      <div><div class="yr">{s}</div><div class="plat">{plat}</div></div>
      <div><span class="crown">Champion</span><div class="champ">{who}</div></div>
      <div class="evid">{evid}</div>
    </li>''')

hbars=[]
for s,plat,ch,cc,pd,hh,ppg,era in SEASONS:
    if not hh: continue
    tw,ew=hh; tot=tw+ew
    note=" &middot; through week 6" if s=="2026" else ""
    hbars.append(f'''      <div class="hrow">
        <div class="hyr">{s}<span class="hnote">{note}</span></div>
        <div class="hbarwrap">
          <div class="bar" role="img" aria-label="{s} cross-class matchups: class of 2012 won {tw}, class of 2011 won {ew}">
            <span class="seg c{T}" style="width:{tw/tot*100:.2f}%"></span><span class="seg c{E}" style="width:{ew/tot*100:.2f}%"></span><span class="mid"></span>
          </div>
          <div class="barlab"><span class="l">&rsquo;12&nbsp; {tw}</span><span class="r">{ew} &nbsp;&rsquo;11</span></div>
          <div class="ppg">PPG &nbsp;{ppg[0]} &rsquo;12 &nbsp;/&nbsp; {ppg[1]} &rsquo;11</div>
        </div>
      </div>''')

tbl=[]
for s,plat,ch,cc,pd,hh,ppg,era in SEASONS:
    c=f'<td class="c{cc}">20{cc}</td>' if cc else '<td class="dim">&mdash;</td>'
    chn=ch or "in progress"
    if pd:
        e=sum(1 for _,x in pd if x==E); t=sum(1 for _,x in pd if x==T); p=f"{t}&ndash;{e}"
    else: p="&mdash;"
    hs=f'{hh[0]}&ndash;{hh[1]}' if hh else '&mdash;'
    pp=f'{ppg[0]} / {ppg[1]}' if ppg else '&mdash;'
    tbl.append(f'        <tr><td>{s}</td><td class="dim">{plat}</td><td>{chn}</td>{c}<td>{p}</td><td>{hs}</td><td class="dim">{pp}</td></tr>')

HTML=f'''<title>2011 vs 2012</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{{
  --surface:#FBFBFC; --surface-2:#F1F2F5;
  --ink:#16181C; --ink-2:#474B54; --ink-3:#787D88;
  --rule:#DCDEE4; --rule-strong:#C2C6D0;
  --c11:#1F5FA9; --c12:#A9760C;
  --c11-wash:#E6EDF7; --c12-wash:#F6EEDC; --unk:#B4B8C2;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme="light"]){{
    --surface:#131519; --surface-2:#1B1E24;
    --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
    --rule:#2A2E36; --rule-strong:#3A3F49;
    --c11:#4884CE; --c12:#C08A1E;
    --c11-wash:#1A2533; --c12-wash:#2A2313; --unk:#474C57;
  }}
}}
:root[data-theme="dark"]{{
  --surface:#131519; --surface-2:#1B1E24;
  --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
  --rule:#2A2E36; --rule-strong:#3A3F49;
  --c11:#4884CE; --c12:#C08A1E;
  --c11-wash:#1A2533; --c12-wash:#2A2313; --unk:#474C57;
}}
*{{box-sizing:border-box}}
body{{background:var(--surface); color:var(--ink);
  font-family:"Newsreader",Georgia,serif; font-size:17px; line-height:1.55; margin:0;
  padding-block:40px 64px; padding-left:20px; padding-right:20px; -webkit-font-smoothing:antialiased}}
.wrap{{max-width:900px; margin:0 auto}}
.disp{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800; line-height:.92; letter-spacing:.01em}}
.eyebrow,.fig-k,.plat,.chip,.crown,.cap,.barlab,.ppg,.notrack,.pod,.lg,.hyr,table,caption,footer,.divlab
  {{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}}
.eyebrow{{font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 18px}}
h1.disp{{font-size:clamp(56px,12vw,100px); margin:0; text-wrap:balance}}
h1 .v{{color:var(--ink-3); font-weight:500}}
h1 .a{{color:var(--c11)}} h1 .b{{color:var(--c12)}}
.standfirst{{font-size:19px; color:var(--ink-2); max-width:60ch; margin:20px 0 0;
  border-left:2px solid var(--rule-strong); padding-left:16px}}
.figs{{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:34px}}
.fig{{background:var(--surface-2); border:1px solid var(--rule); border-radius:3px; padding:16px 18px 14px}}
.fig-k{{font-size:10px; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3)}}
.fig-v{{display:flex; align-items:baseline; gap:8px; margin-top:9px}}
.fig-v .n{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800;
  font-size:clamp(40px,7vw,58px); line-height:.85; font-variant-numeric:tabular-nums}}
.fig-v .dash{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:500;
  font-size:clamp(28px,5vw,40px); color:var(--ink-3); line-height:.85}}
.n.c11{{color:var(--c11)}} .n.c12{{color:var(--c12)}}
.fig-note{{font-size:13.5px; color:var(--ink-2); margin:10px 0 0; line-height:1.4}}
.legend{{display:flex; flex-wrap:wrap; gap:18px; align-items:center; margin:36px 0 8px;
  padding-bottom:12px; border-bottom:1px solid var(--rule)}}
.lg{{display:flex; align-items:center; gap:7px; font-size:12px; font-weight:500; color:var(--ink-2)}}
.lg .sub{{color:var(--ink-3)}}
.sw{{width:13px; height:13px; border-radius:2px; flex:none}}
.sw.c11{{background:var(--c11)}} .sw.c12{{background:var(--c12)}} .sw.unk{{background:var(--unk)}}
h2.disp{{font-size:29px; margin:50px 0 6px; letter-spacing:.02em}}
.sub-h{{font-size:15px; color:var(--ink-3); margin:0 0 14px; max-width:64ch}}
.ledger{{list-style:none; margin:0; padding:0}}
.row{{display:grid; grid-template-columns:76px minmax(140px,1fr) minmax(210px,1.3fr); gap:20px;
  align-items:center; padding:14px 0; border-bottom:1px solid var(--rule)}}
.yr{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:700; font-size:37px;
  line-height:.85; font-variant-numeric:tabular-nums}}
.plat{{font-size:9.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3); margin-top:5px}}
.champ{{display:flex; align-items:center; gap:8px; flex-wrap:wrap}}
.champ .who{{font-size:18px; font-weight:500}}
.champ .who.tbd{{color:var(--ink-3); font-style:italic; font-weight:400}}
.chip{{font-size:10.5px; font-weight:600; letter-spacing:.05em; padding:3px 7px; border-radius:2px; flex:none}}
.chip.c11{{background:var(--c11-wash); color:var(--c11)}}
.chip.c12{{background:var(--c12-wash); color:var(--c12)}}
.crown{{font-size:9.5px; letter-spacing:.11em; text-transform:uppercase; color:var(--ink-3); display:block; margin-bottom:3px}}
.evid{{display:flex; flex-direction:column; gap:6px}}
.podium{{display:flex; gap:2px; align-items:flex-end}}
.pod{{flex:1; border-radius:2px 2px 0 0; display:flex; align-items:flex-end; justify-content:center;
  font-size:10px; font-weight:600; color:#fff; padding-bottom:3px}}
.pod.c11{{background:var(--c11)}} .pod.c12{{background:var(--c12)}}
.pod.cunk{{background:var(--unk); color:var(--ink-2)}}
.cap{{font-size:10.5px; color:var(--ink-3); letter-spacing:.03em}}
.notrack{{min-height:22px; border:1.5px dashed var(--rule-strong); border-radius:2px; display:flex;
  align-items:center; padding:3px 10px; font-size:10.5px; letter-spacing:.06em; color:var(--ink-3)}}
.notrack.warn{{border-color:var(--c12); color:var(--c12)}}
.h2h{{display:flex; flex-direction:column; gap:2px; margin-top:6px}}
.hrow{{display:grid; grid-template-columns:120px 1fr; gap:20px; align-items:center;
  padding:13px 0; border-bottom:1px solid var(--rule)}}
.hyr{{font-size:13px; font-weight:600; color:var(--ink-2)}}
.hnote{{display:block; font-size:9.5px; font-weight:400; color:var(--ink-3); letter-spacing:.08em; text-transform:uppercase}}
.hbarwrap{{display:flex; flex-direction:column; gap:6px}}
.bar{{display:flex; height:22px; gap:2px; position:relative}}
.seg{{border-radius:2px; min-width:3px}}
.seg.c11{{background:var(--c11)}} .seg.c12{{background:var(--c12)}}
.mid{{position:absolute; left:50%; top:-4px; bottom:-4px; width:1px; background:var(--rule-strong); z-index:2}}
.barlab{{display:flex; justify-content:space-between; font-size:11.5px; font-weight:600; font-variant-numeric:tabular-nums}}
.barlab .l{{color:var(--c12)}} .barlab .r{{color:var(--c11)}}
.ppg{{font-size:10.5px; color:var(--ink-3)}}
.notes{{font-size:15.5px; color:var(--ink-2); max-width:64ch}}
.notes p{{margin:0 0 12px}}
.notes strong{{color:var(--ink); font-weight:500}}
.warnbox{{border-left:3px solid var(--c12); background:var(--c12-wash); padding:14px 16px;
  border-radius:2px; font-size:15px; color:var(--ink-2); margin:16px 0 0}}
.tablewrap{{overflow-x:auto; margin-top:14px; border:1px solid var(--rule); border-radius:3px}}
table{{border-collapse:collapse; width:100%; font-size:13.5px}}
caption{{text-align:left; font-size:10.5px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--ink-3); padding:12px 14px 10px}}
th,td{{text-align:left; padding:8px 14px; border-top:1px solid var(--rule); white-space:nowrap; font-variant-numeric:tabular-nums}}
th{{font-weight:600; font-size:10.5px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-3); background:var(--surface-2)}}
td.c11{{color:var(--c11)}} td.c12{{color:var(--c12)}} td.dim{{color:var(--ink-3)}}
footer{{margin-top:44px; padding-top:16px; border-top:1px solid var(--rule); font-size:10.5px;
  letter-spacing:.05em; color:var(--ink-3); line-height:1.8}}
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
  .figs{{grid-template-columns:1fr}}
  .row{{grid-template-columns:1fr; gap:10px; padding:16px 0}}
  .yr{{font-size:31px; display:inline-block}}
  .plat{{display:inline-block; margin-left:9px; margin-top:0}}
  .hrow{{grid-template-columns:1fr; gap:8px}}
}}
</style>

<div class="wrap">
  <p class="eyebrow">EX Champions League &nbsp;&middot;&nbsp; Sigma Chi &nbsp;&middot;&nbsp; Washington &amp; Lee</p>
  <h1 class="disp"><span class="a">2011</span> <span class="v">vs</span> <span class="b">2012</span></h1>
  <p class="standfirst">Twelve seasons of the pledge-class war, reconstructed from the Yahoo archive, the commissioner&rsquo;s keeper spreadsheet and the Sleeper record. The classes are dead level on championships and have been for a decade.</p>

  <div class="figs">
    <div class="fig">
      <div class="fig-k">Championships</div>
      <div class="fig-v"><span class="n c11">{tc[E]}</span><span class="dash">&ndash;</span><span class="n c12">{tc[T]}</span></div>
      <p class="fig-note">Every season from 2014 on. Neither class has ever led by more than one.</p>
    </div>
    <div class="fig">
      <div class="fig-k">Top-six finishes</div>
      <div class="fig-v"><span class="n c11">{pod[E]}</span><span class="dash">&ndash;</span><span class="n c12">{pod[T]}</span></div>
      <p class="fig-note">Of 72 playoff places. Five went to managers who have since left the league.</p>
    </div>
    <div class="fig">
      <div class="fig-k">Cross-class games</div>
      <div class="fig-v"><span class="n c11">{h2h[E]}</span><span class="dash">&ndash;</span><span class="n c12">{h2h[T]}</span></div>
      <p class="fig-note">Yahoo never kept weekly results, so game-level data starts in 2024.</p>
    </div>
  </div>

  <div class="legend">
    <span class="lg"><span class="sw c11"></span>Class of 2011 <span class="sub">&nbsp;7 teams</span></span>
    <span class="lg"><span class="sw c12"></span>Class of 2012 <span class="sub">&nbsp;5 teams</span></span>
    <span class="lg"><span class="sw unk"></span>Since departed</span>
  </div>

  <h2 class="disp">The title ledger</h2>
  <p class="sub-h">Each bar is that season&rsquo;s playoff top six, first place at the left. Grey blocks are managers who have since left.</p>
  <ul class="ledger">
{chr(10).join(rows)}
  </ul>

  <h2 class="disp">Head-to-head, where the games survive</h2>
  <p class="sub-h">Cross-class regular-season matchups. Yahoo kept brackets and standings but not weekly results, so this begins in 2024.</p>
  <div class="h2h">
{chr(10).join(hbars)}
  </div>

  <h2 class="disp">What the record supports</h2>
  <div class="notes">
    <p><strong>The championship count is dead level at six apiece</strong> across twelve seasons, and it has never been more than one apart. &rsquo;11 leads on playoff places and head-to-head games, but it fields seven teams to &rsquo;12&rsquo;s five.</p>
    <p><strong>2025 was the most lopsided season on record.</strong> &rsquo;11 took five of the six playoff places and won the cross-class schedule 28&ndash;16. It is the only reason &rsquo;11 leads the game count; strip it out and &rsquo;12 is up 26&ndash;21.</p>
    <p><strong>Five playoff places belong to managers who have since left</strong> &mdash; Drew Jacoby, Ned Lundvall and Skylar W. Greg took over Drew&rsquo;s franchise in 2019; the current twelve were all in place by 2020.</p>
    <p><strong>Dan and Tyler have three titles each</strong>, one from each class, and Detrick has two.</p>
  </div>


  <h2 class="disp">The numbers, plainly</h2>
  <div class="tablewrap">
    <table>
      <caption>Season ledger &mdash; splits shown from the class of 2012&rsquo;s side</caption>
      <thead><tr><th scope="col">Season</th><th scope="col">Platform</th><th scope="col">Champion</th><th scope="col">Class</th><th scope="col">Top six &rsquo;12&ndash;&rsquo;11</th><th scope="col">Games &rsquo;12&ndash;&rsquo;11</th><th scope="col">PPG &rsquo;12 / &rsquo;11</th></tr></thead>
      <tbody>
{chr(10).join(tbl)}
      </tbody>
    </table>
  </div>

  <footer>Game-level cross-class data exists only for 2024 onward; 2026 reflects weeks 1&ndash;6.<br>
  Sources: Yahoo Fantasy archive and Record Book (2014&ndash;2024), Sigmach Fantasy Football.xlsx, and the Sleeper API. Compiled 15 September 2026.</footer>
</div>
'''
publish("2011-vs-2012.html", HTML)
print("titles",tc,"podium",pod,"games",h2h)
