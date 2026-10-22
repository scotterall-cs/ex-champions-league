# -*- coding: utf-8 -*-
"""Generates a weekly recap page. Edit the WEEK block, run, push."""
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

WEEK = 6
SEASON = "2026"
DATED = "20 October 2026"

# winner, w_pts, loser, l_pts, cross-class?
GAMES = [
 ("Kids College Funds",113.50,"YoSoyFiesta",111.52,False),
 ("scert",101.50,"Win One for the Lipper",64.38,False),
 ("Roughnecks",101.04,"The Skin",92.76,True),
 ("maxhagler",93.34,"Cooking With Friends",88.72,False),
 ("vaught12",88.78,"Table Smashers",79.66,False),
 ("Uncle Rico",84.20,"Team bxkeegan",71.26,False),
]
CLASSOF={"Table Smashers":T,"maxhagler":T,"The Skin":T,"vaught12":T,"Cooking With Friends":T,
 "Kids College Funds":E,"scert":E,"Roughnecks":E,"YoSoyFiesta":E,"Uncle Rico":E,
 "Win One for the Lipper":E,"Team bxkeegan":E}
STAND=[("Uncle Rico",6,0,678.16,549.28,737.96),("maxhagler",5,1,707.64,662.82,836.54),
 ("YoSoyFiesta",4,2,720.84,607.16,777.32),("Kids College Funds",4,2,635.84,608.80,733.20),
 ("The Skin",3,3,693.50,640.60,713.20),("scert",3,3,639.74,728.40,717.94),
 ("vaught12",3,3,595.72,545.92,725.18),("Team bxkeegan",3,3,567.30,565.84,624.00),
 ("Table Smashers",2,4,626.20,626.02,676.40),("Roughnecks",1,5,572.32,726.70,629.02),
 ("Cooking With Friends",1,5,561.14,629.64,648.84),("Win One for the Lipper",1,5,515.16,622.38,596.44)]
EFF=[("Table Smashers",100.0,0.00),("Team bxkeegan",98.3,1.20),("The Skin",96.4,3.50),
 ("YoSoyFiesta",93.9,7.30),("Uncle Rico",93.8,5.60),("maxhagler",92.7,7.30),
 ("scert",90.7,10.46),("Roughnecks",89.9,11.30),("vaught12",89.9,10.02),
 ("Win One for the Lipper",86.8,9.80),("Kids College Funds",86.2,18.14),("Cooking With Friends",79.6,22.70)]
TOP=[(26.90,"Kenneth Walker","RB","scert"),(26.20,"Christian McCaffrey","RB","Cooking With Friends"),
 (23.80,"Drake Maye","QB","Kids College Funds"),(22.80,"James Cook","RB","Kids College Funds"),
 (22.50,"Malik Nabers","WR","The Skin")]
DUDS=[(0.00,"Cam Skattebo","RB","vaught12"),(0.00,"Juwan Johnson","TE","Kids College Funds"),
 (0.00,"Quinshon Judkins","RB","Cooking With Friends"),(0.20,"Najee Harris","RB","Win One for the Lipper")]
STORIES=[
 ("&#127920;","The stars aligned","Roughnecks",
  "Joe beat Sam 101.04 to 92.76, and it took a roster-wide collapse to arrange it. "
  "<b>Bijan Robinson scored 6.30</b> against a season average of 19.75 &mdash; a 13.45-point hole from the best "
  "player on the field. <b>Chase Brown and Jordan Mason both scored 0.00</b> on the bench, leaving no cover, so "
  "Brian Robinson started and managed 2.00. Sam still set 96.4% of his optimal lineup. "
  "He did almost nothing wrong and his roster simply did not turn up."),
 ("&#128128;","One win is not a turnaround","Roughnecks",
  "Here is the number that settles it: Sam&rsquo;s <b>best possible lineup this week was 96.26</b>. Joe scored 101.04. "
  "He did not out-manage anyone &mdash; he beat a team whose entire roster had a ceiling below his score. "
  "Joe is 1&ndash;5, last on points for at 572.32, and his season optimal of 629.02 is tenth of twelve. "
  "Nothing underneath has moved."),
 ("&#129351;","Six and oh","Uncle Rico",
  "Greg is <b>6&ndash;0</b> and the streak is <b>fourteen</b>, and he got there by scoring 84.20 &mdash; his lowest "
  "of the season, ninth of twelve this week. He is now winning without playing well, which is the most "
  "infuriating possible way to be undefeated."),
 ("&#128561;","Again","Kids College Funds",
  "Armstrong beat Dan <b>113.50 to 111.52</b> &mdash; 1.98, exactly the margin he won by last week, having lost by "
  "0.10 in week 2. Three of his six games have been decided by under two points. Nobody else has had one."),
]
# ---------------------------------------------------------------------------
# THE ROUGHNECKS CORNER — recurring feature, do not drop.
# A highlighted box about Joe (Roughnecks), written warm and tongue-in-cheek.
# Started week 4 2026 at his request; the group liked it, so it runs every week.
# Rules:
#   - Always about Joe, win or lose. If he wins, celebrate it properly.
#   - Every number must be real. Pull his week-over-week score, his league rank
#     that week, his lineup efficiency, and his margin, and lead with whichever
#     genuinely flatters him.
#   - Keep the "By request" tag — it is what stops it reading as pity.
#   - If a week offers nothing kind, say so plainly and briefly rather than
#     inventing a positive. Do not fabricate a silver lining.
# Set CALLOUT = None only if the feature is explicitly retired.
# ---------------------------------------------------------------------------
CALLOUT = ("&#129746;","The Roughnecks corner","By request",
 "The corner has waited six weeks to write a sentence with the word <i>won</i> in it, so: <b>Joe won.</b> "
 "101.04, fourth-highest score of the week, over 100 in three of his last four. "
 "And whatever the circumstances, the schedule owed him one &mdash; across six weeks Joe has faced "
 "<b>726.70</b> points, more than anybody in this league has had thrown at them. "
 "Enjoy it. On the evidence of the other section, enjoy it quickly.")
NEXTWEEK = [
 ("maxhagler","Uncle Rico","Max 5&ndash;1 vs Greg 6&ndash;0",
  "The game of the season so far. Greg is undefeated on a fourteen-game streak; Max has the best roster in the "
  "league by a distance, an optimal of 836.54 that is eighty clear of anyone. Cross-class, and the biggest one left."),
 ("The Skin","Kids College Funds","Sam 3&ndash;3 vs Armstrong 4&ndash;2",
  "Sam has lost three of four since leading the league in points. Armstrong has won his last two by 1.98 "
  "apiece. Cross-class, and both of them need it."),
 ("Table Smashers","YoSoyFiesta","Tyler 2&ndash;4 vs Dan 4&ndash;2",
  "Tyler is the best lineup manager in league history and 2&ndash;4, because the roster has nothing on it. "
  "Dan has the most points in the league. Cross-class."),
 ("Cooking With Friends","Roughnecks","Detrick 1&ndash;5 vs Joe 1&ndash;5",
  "The bottom two, both 1&ndash;5, both with a single win. Also cross-class, which means the loser drags their "
  "whole class down with them. Somebody is going to 1&ndash;6."),
]
CLASS_WK=(0,1); CLASS_PPG=(88.65,92.49); CLASS_SEASON=(9,11); CLASS_ALLTIME=(50,58)


# Class-war captions are DERIVED, never typed. A hardcoded "gap is down to four"
# survived three weeks of regeneration before anyone noticed. Do not hardcode these.
_W={1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",8:"eight",9:"nine",10:"ten"}
def _gapword(n): return _W.get(abs(n), str(abs(n)))

def _nextweek_caption():
    n=sum(1 for a,b,_,_ in NEXTWEEK if CLASSOF.get(a)!=CLASSOF.get(b))
    # NEXTWEEK only features a subset; count across thefull schedule instead
    n=NEXTWEEK_CROSS
    w={0:"None",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",6:"All six"}.get(n,str(n))
    verb="is" if n==1 else "are"
    t,e=CLASS_SEASON
    series=("the season series tied" if t==e else
            ("&rsquo;12 leading the season series" if t>e else "&rsquo;11 leading the season series"))
    score=f"{max(t,e)}&ndash;{min(t,e)}" if t!=e else f"{t}&ndash;{e}"
    return f"{w} of the six {verb} cross-class, with {series} {score}"

def _alltime_caption():
    e,t=CLASS_ALLTIME[1],CLASS_ALLTIME[0]      # (12, 11) -> e is '11, t is '12
    g=e-t
    if g==0: return "Level on every game ever played."
    lead="&rsquo;11" if g>0 else "&rsquo;12"
    return f"{lead} ahead by {'a single game' if abs(g)==1 else _gapword(g)+' games'}."
def _week_caption():
    t,e=CLASS_WK
    who="&rsquo;11 won the week" if e>t else ("&rsquo;12 won the week" if t>e else "The week split evenly")
    hi,lo=("&rsquo;12","&rsquo;11") if CLASS_PPG[0]>=CLASS_PPG[1] else ("&rsquo;11","&rsquo;12")
    a,b=(CLASS_PPG[0],CLASS_PPG[1]) if CLASS_PPG[0]>=CLASS_PPG[1] else (CLASS_PPG[1],CLASS_PPG[0])
    return f"{who}; {hi} outscored {lo} {a:.2f} to {b:.2f} per team."
def _season_caption():
    t,e=CLASS_SEASON
    if t==e: return "Dead level. Nothing between them."
    lead,g="&rsquo;12" if t>e else "&rsquo;11", abs(t-e)
    return f"{lead} lead the season by {'a single game' if g==1 else _gapword(g)+' games'}."


# ---------------------------------------------------------------------------
# SCHEDULE GUARD. The week-5 page shipped four invented matchups because they
# were typed from memory instead of fetched. Never type a future matchup again:
# this pulls the real schedule and aborts the build if NEXTWEEK disagrees.
# ---------------------------------------------------------------------------
import json, urllib.request
_LEAGUE = "1389693216323817472"
def _fetch_pairs(week):
    by = {}
    for m in json.load(urllib.request.urlopen(
            f"https://api.sleeper.app/v1/league/{_LEAGUE}/matchups/{week}")):
        by.setdefault(m["matchup_id"], []).append(m["roster_id"])
    rid = {v: k for k, v in ROSTER.items()}
    return {frozenset((ROSTER[a], ROSTER[b])) for a, b in by.values()}, by
ROSTER = {1:"Table Smashers",2:"maxhagler",3:"The Skin",4:"vaught12",5:"Kids College Funds",
          6:"Cooking With Friends",7:"scert",8:"Roughnecks",9:"YoSoyFiesta",10:"Uncle Rico",
          11:"Win One for the Lipper",12:"Team bxkeegan"}
_real, _raw = _fetch_pairs(WEEK + 1)
for _a, _b, _r, _t in NEXTWEEK:
    assert frozenset((_a, _b)) in _real, (
        f"NEXTWEEK is wrong: {_a} v {_b} is not in the week {WEEK+1} schedule. "
        f"Real pairings: {sorted(tuple(sorted(p)) for p in _real)}")
NEXTWEEK_CROSS = sum(1 for p in _real
                     for a, b in [tuple(p)] if CLASSOF.get(a) != CLASSOF.get(b))
print(f"  schedule guard: all {len(NEXTWEEK)} previewed matchups verified against "
      f"week {WEEK+1}; {NEXTWEEK_CROSS} of {len(_real)} are cross-class")

def cls(t): return CLASSOF.get(t,"x")   # "x" = neutral, for stories about more than one team
game_rows="".join(
 f'''<li class="g{' cross' if x else ''}">
   <span class="gt w c{cls(a)}">{a}</span><span class="gp w">{ap:.2f}</span>
   <span class="gd">def</span>
   <span class="gt l c{cls(b)}">{b}</span><span class="gp l">{bp:.2f}</span>
   <span class="gm">+{ap-bp:.2f}</span></li>''' for a,ap,b,bp,x in GAMES)
stand_rows="".join(
 f'<tr><td class="c{cls(t)}">{t}</td><td><b>{w}&ndash;{l}</b></td><td>{pf:.2f}</td>'
 f'<td class="dim">{pa:.2f}</td><td class="opt">{o:.2f}</td></tr>'
 for t,w,l,pf,pa,o in STAND)
eff_rows="".join(
 f'''<li><span class="en">{t}</span><span class="ebar"><span class="efill c{cls(t)}" style="width:{e}%"></span></span>
 <span class="ev">{e:.1f}%</span><span class="el">&minus;{lost:.1f}</span></li>''' for t,e,lost in EFF)
top_rows="".join(f'<li><span class="pv good">{p:.2f}</span><span class="pn">{n} <span class="pp">{ps}</span></span><span class="pt">{t}</span></li>' for p,n,ps,t in TOP)
dud_rows="".join(f'<li><span class="pv bad">{p:.2f}</span><span class="pn">{n} <span class="pp">{ps}</span></span><span class="pt">{t}</span></li>' for p,n,ps,t in DUDS)
callout_html=(f'<aside class="callout"><div class="coh"><span class="coi">{CALLOUT[0]}</span>'
 f'<span class="cot">{CALLOUT[1]}</span><span class="cok">{CALLOUT[2]}</span></div>'
 f'<p>{CALLOUT[3]}</p></aside>') if CALLOUT else ""
nextweek_html="".join(
 f'<div class="nw"><div class="nwh"><span class="nwt c{cls(a)}">{a}</span>'
 f'<span class="nwv">v</span><span class="nwt c{cls(b)}">{b}</span>'
 f'<span class="nwr">{r}</span></div><p>{t}</p></div>' for a,b,r,t in NEXTWEEK)
story_html="".join(
 f'<section class="story"><div class="sh"><span class="si">{i}</span><span class="sk">{k}</span>'
 f'<span class="st c{cls(t)}">{t}</span></div><p>{b}</p></section>' for i,k,t,b in STORIES)

HTML=f'''<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Week {WEEK} &mdash; EX Champions League</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
:root{{
  --surface:#131519; --surface-2:#1B1E24;
  --ink:#EDEFF3; --ink-2:#A8AEBA; --ink-3:#757C89;
  --rule:#2A2E36; --rule-strong:#3A3F49;
  --c11:#4884CE; --c12:#C08A1E;
  --c11-wash:#1A2533; --c12-wash:#2A2313;
  --good:#4884CE; --bad:#C08A1E;
}}
*{{box-sizing:border-box}}
body{{background:var(--surface); color:var(--ink);
  font-family:"Newsreader",Georgia,serif; font-size:17px; line-height:1.55; margin:0;
  padding-block:44px 64px; padding-left:20px; padding-right:20px; -webkit-font-smoothing:antialiased}}
.wrap{{max-width:880px; margin:0 auto}}
.disp{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800; line-height:.92}}
.eyebrow,.gp,.gd,.gm,.gt,.sk,.ev,.el,.en,.pv,.pt,.pp,table,.cap,footer,.back
  {{font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace}}
a.back{{display:inline-block; font-size:11px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--ink-3); text-decoration:none; margin-bottom:22px; border-bottom:1px solid var(--rule); padding-bottom:3px}}
a.back:hover{{color:var(--ink-2)}}
.eyebrow{{font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 12px}}
h1.disp{{font-size:clamp(56px,13vw,104px); margin:0}}
.sub{{font-size:18px; color:var(--ink-2); margin:16px 0 0; max-width:56ch;
  border-left:2px solid var(--rule-strong); padding-left:16px}}
h2.disp{{font-size:26px; margin:46px 0 12px; letter-spacing:.02em}}
.games{{list-style:none; margin:0; padding:0}}
li.g{{display:grid; grid-template-columns:1fr auto 34px 1fr auto 62px; gap:10px; align-items:baseline;
  padding:12px 0; border-bottom:1px solid var(--rule)}}
li.g.cross{{background:linear-gradient(90deg,transparent,rgba(72,132,206,.05))}}
.gt{{font-size:14px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}}
.gt.l{{color:var(--ink-3)!important; font-weight:400}}
.gp{{font-size:15px; font-weight:600; font-variant-numeric:tabular-nums}}
.gp.l{{color:var(--ink-3); font-weight:400}}
.gd{{font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3); text-align:center}}
.gm{{font-size:12px; color:var(--ink-3); text-align:right; font-variant-numeric:tabular-nums}}
.c11{{color:var(--c11)}} .c12{{color:var(--c12)}} .cx{{color:var(--ink)}}
.story{{border-left:3px solid var(--rule-strong); padding:2px 0 2px 18px; margin:0 0 26px}}
.story:nth-child(1){{border-left-color:var(--c11)}}
.story:nth-child(2){{border-left-color:var(--c12)}}
.story:nth-child(3){{border-left-color:var(--c11)}}
.story:nth-child(4){{border-left-color:var(--c12)}}
.sh{{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:7px}}
.si{{font-size:17px}}
.sk{{font-size:10px; font-weight:600; letter-spacing:.13em; text-transform:uppercase; color:var(--ink-3)}}
.st{{font-size:15px; font-weight:600}}
.story p{{margin:0; font-size:16px; color:var(--ink-2); max-width:62ch}}
.cols{{display:grid; grid-template-columns:1fr 1fr; gap:18px 34px}}
.eff{{list-style:none; margin:0; padding:0}}
.eff li{{display:grid; grid-template-columns:132px 1fr 50px 48px; gap:10px; align-items:center;
  padding:6px 0; border-bottom:1px solid var(--rule)}}
.en{{font-size:12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis}}
.ebar{{height:8px; background:var(--surface-2); border-radius:2px; overflow:hidden}}
.efill{{display:block; height:100%}}
.efill.c11{{background:var(--c11)}} .efill.c12{{background:var(--c12)}}
.ev{{font-size:12px; font-weight:600; text-align:right; font-variant-numeric:tabular-nums}}
.el{{font-size:11px; color:var(--ink-3); text-align:right; font-variant-numeric:tabular-nums}}
.plist{{list-style:none; margin:0; padding:0}}
.plist li{{display:grid; grid-template-columns:62px 1fr; gap:10px; align-items:baseline;
  padding:7px 0; border-bottom:1px solid var(--rule)}}
.pv{{font-size:14px; font-weight:600; font-variant-numeric:tabular-nums}}
.pv.good{{color:var(--good)}} .pv.bad{{color:var(--bad)}}
.pn{{font-size:15.5px}}
.pp{{font-size:10px; color:var(--ink-3); letter-spacing:.06em}}
.pt{{grid-column:2; font-size:10.5px; color:var(--ink-3); letter-spacing:.05em; text-transform:uppercase}}
td.opt{{color:var(--ink-3); font-style:italic}}
.cap{{font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3); margin:0 0 8px}}
table{{border-collapse:collapse; width:100%; font-size:13px}}
th,td{{text-align:left; padding:7px 12px; border-top:1px solid var(--rule); white-space:nowrap; font-variant-numeric:tabular-nums}}
th{{font-size:10px; letter-spacing:.07em; text-transform:uppercase; color:var(--ink-3); background:var(--surface-2); font-weight:600}}
.tablewrap{{border:1px solid var(--rule); border-radius:3px; overflow-x:auto}}
.war{{display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:12px}}
.warbox{{background:var(--surface-2); border:1px solid var(--rule); border-radius:3px; padding:14px 16px}}
.wark{{font-family:"IBM Plex Mono",monospace; font-size:9.5px; font-weight:600; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3)}}
.warv{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800;
  font-size:38px; line-height:.9; margin-top:7px; font-variant-numeric:tabular-nums}}
.warn2{{font-size:13px; color:var(--ink-2); margin-top:7px}}
.dash{{color:var(--ink-3); font-weight:500; font-size:.75em}}
.callout{{background:var(--surface-2); border:1px solid var(--rule-strong);
  border-left:4px solid var(--c11); border-radius:4px; padding:18px 22px; margin:6px 0 30px}}
.coh{{display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:8px}}
.coi{{font-size:18px}}
.cot{{font-family:"Big Shoulders Display","Arial Narrow",sans-serif; font-weight:800; font-size:23px; letter-spacing:.01em}}
.cok{{font-family:"IBM Plex Mono",monospace; font-size:9.5px; font-weight:600; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3)}}
.callout p{{margin:0; font-size:16px; color:var(--ink-2); max-width:64ch}}
.nw{{border-left:3px solid var(--rule-strong); padding:2px 0 2px 18px; margin:0 0 20px}}
.nw:nth-of-type(odd){{border-left-color:var(--c11)}}
.nw:nth-of-type(even){{border-left-color:var(--c12)}}
.nwh{{display:flex; align-items:baseline; gap:9px; flex-wrap:wrap; margin-bottom:6px}}
.nwt{{font-size:15px; font-weight:600}}
.nwv{{font-family:"IBM Plex Mono",monospace; font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3)}}
.nwr{{font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em; color:var(--ink-3)}}
.nw p{{margin:0; font-size:16px; color:var(--ink-2); max-width:62ch}}
footer{{margin-top:48px; padding-top:16px; border-top:1px solid var(--rule);
  font-family:"IBM Plex Mono",monospace; font-size:10.5px; letter-spacing:.05em; color:var(--ink-3); line-height:1.8}}
@media (max-width:660px){{
  .cols{{grid-template-columns:1fr}}
  .war{{grid-template-columns:1fr}}
  li.g{{grid-template-columns:1fr auto; row-gap:2px}}
  li.g .gd{{display:none}} li.g .gm{{grid-column:2; text-align:right}}
  .eff li{{grid-template-columns:104px 1fr 46px 42px}}
  table{{font-size:11px}}
  th,td{{padding:6px 7px}}
  th{{font-size:9px; letter-spacing:.04em}}
  td:first-child{{max-width:118px; overflow:hidden; text-overflow:ellipsis}}
}}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">&larr; EX Champions League</a>
  <p class="eyebrow">{SEASON} Season &nbsp;&middot;&nbsp; Recap</p>
  <h1 class="disp">Week {WEEK}</h1>
  <p class="sub">Joe wins one at last, though it took Sam&rsquo;s roster collapsing to arrange it; Greg goes 6&ndash;0 while playing badly.</p>

  <h2 class="disp">Scoreboard</h2>
  <ul class="games">{game_rows}</ul>

  <h2 class="disp">The week in four parts</h2>
  {story_html}
  {callout_html}

  <h2 class="disp">Standings</h2>
  <p class="cap">Season to date &middot; Optimal is what every lineup would have scored if perfectly set</p>
  <div class="tablewrap"><table>
    <thead><tr><th scope="col">Team</th><th scope="col">Record</th><th scope="col">Points for</th><th scope="col">Points against</th><th scope="col">Optimal</th></tr></thead>
    <tbody>{stand_rows}</tbody>
  </table></div>

  <h2 class="disp">Who set their lineup</h2>
  <p class="cap">Share of the best lineup that roster could have started &middot; points left on the bench</p>
  <ul class="eff">{eff_rows}</ul>

  <h2 class="disp">Best and worst</h2>
  <div class="cols">
    <div><p class="cap">Top starts</p><ul class="plist">{top_rows}</ul></div>
    <div><p class="cap">Started anyway</p><ul class="plist">{dud_rows}</ul></div>
  </div>

  <h2 class="disp">The class war</h2>
  <div class="war">
    <div class="warbox"><div class="wark">This week</div>
      <div class="warv"><span class="c11">{CLASS_WK[1]}</span><span class="dash">&ndash;</span><span class="c12">{CLASS_WK[0]}</span></div>
      <p class="warn2">{_week_caption()}</p></div>
    <div class="warbox"><div class="wark">{SEASON} to date</div>
      <div class="warv"><span class="c12">{CLASS_SEASON[0]}</span><span class="dash">&ndash;</span><span class="c11">{CLASS_SEASON[1]}</span></div>
      <p class="warn2">{_season_caption()}</p></div>
    <div class="warbox"><div class="wark">All time</div>
      <div class="warv"><span class="c11">{CLASS_ALLTIME[1]}</span><span class="dash">&ndash;</span><span class="c12">{CLASS_ALLTIME[0]}</span></div>
      <p class="warn2">{_alltime_caption()}</p></div>
  </div>

  <h2 class="disp">Next week</h2>
  <p class="cap">{_nextweek_caption()}</p>
  {nextweek_html}

  <footer>Source: Sleeper API, pulled {DATED}. Efficiency is points scored as a share of the highest-scoring legal lineup that roster could have started.</footer>
</div>
</body>
</html>
'''
publish(f"week-{WEEK}.html", HTML)
