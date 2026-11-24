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

WEEK = 11
SEASON = "2026"
DATED = "24 November 2026"

# The standfirst under the headline. It was hardcoded in the template until week
# 10, so weeks 7, 8, 9 and 10 all shipped with week 6's sentence under their own
# headline. It now reads the same one-line summary that drives the index card,
# from tools/weeks.json, so the page and the index can never disagree again.
import json as _json
_WEEKS = _json.loads((ROOT / "tools" / "weeks.json").read_text(encoding="utf-8"))["weeks"]
SUB = _WEEKS.get(str(WEEK))
assert SUB, "tools/weeks.json has no summary for week %d - add it before building" % WEEK

# winner, w_pts, loser, l_pts, cross-class?
GAMES = [
 ("maxhagler",136.12,"vaught12",102.66,False),
 ("YoSoyFiesta",113.00,"Uncle Rico",102.30,False),
 ("Win One for the Lipper",111.86,"Table Smashers",83.08,True),
 ("Team bxkeegan",103.00,"Roughnecks",69.96,False),
 ("Kids College Funds",93.86,"scert",90.54,False),
 ("The Skin",88.26,"Cooking With Friends",76.80,False),
]
CLASSOF={"Table Smashers":T,"maxhagler":T,"The Skin":T,"vaught12":T,"Cooking With Friends":T,
 "Kids College Funds":E,"scert":E,"Roughnecks":E,"YoSoyFiesta":E,"Uncle Rico":E,
 "Win One for the Lipper":E,"Team bxkeegan":E}
STAND=[("maxhagler",9,2,1331.72,1115.00,1554.52),
 ("Uncle Rico",8,3,1181.52,1020.40,1263.52),
 ("Kids College Funds",7,4,1183.80,1106.98,1391.30),
 ("The Skin",6,5,1185.72,1156.28,1246.42),
 ("vaught12",6,5,1147.68,1073.44,1314.64),
 ("Team bxkeegan",6,5,1012.84,1028.14,1140.66),
 ("YoSoyFiesta",5,6,1234.38,1197.18,1369.42),
 ("Table Smashers",5,6,1164.58,1090.08,1275.88),
 ("Cooking With Friends",4,7,1134.44,1152.32,1257.74),
 ("scert",4,7,1063.82,1220.82,1210.42),
 ("Win One for the Lipper",4,7,914.48,1071.22,1067.30),
 ("Roughnecks",2,9,902.00,1225.12,1038.00)]
EFF=[("Table Smashers",100.0,0.00),
 ("Kids College Funds",98.2,1.70),
 ("Uncle Rico",96.1,4.20),
 ("The Skin",96.0,3.70),
 ("vaught12",93.5,7.10),
 ("Cooking With Friends",93.0,5.80),
 ("maxhagler",92.8,10.60),
 ("YoSoyFiesta",92.8,8.80),
 ("Win One for the Lipper",91.8,10.00),
 ("Team bxkeegan",87.7,14.50),
 ("scert",85.3,15.60),
 ("Roughnecks",66.5,35.30)]
TOP=[(35.90,"Dak Prescott","QB","YoSoyFiesta"),
 (32.90,"Jonah Coleman","RB","Team bxkeegan"),
 (26.00,"Chuba Hubbard","RB","maxhagler"),
 (25.80,"Jahmyr Gibbs","RB","maxhagler"),
 (25.40,"Ashton Jeanty","RB","Roughnecks")]
DUDS=[(0.00,"Buccaneers","DEF","Win One for the Lipper"),
 (0.00,"J.K. Dobbins","RB","scert"),
 (0.00,"Vikings","DEF","maxhagler"),
 (0.00,"Wan'Dale Robinson","WR","Team bxkeegan")]
STORIES = [
 ("&#127891;","The rivalry changes hands","The class war",
  "One cross-class game on the whole slate, with the all-time series dead level at 61 apiece, and last "
  "week&rsquo;s preview said whoever won it would lead the rivalry outright. "
  "<b>Tom beat Tyler 111.86 to 83.08.</b> So &rsquo;11 lead the all-time ledger <b>62&ndash;61</b> &mdash; "
  "every cross-class game ever played across twelve seasons, and the margin is one. "
  "&rsquo;12 still hold the season series 20&ndash;15. It has come down to a man who is 4&ndash;7."),
 ("&#128557;","Tyler did everything right and lost the rivalry","Table Smashers",
  "Here is the cruelty. Tyler set a <b>flawless lineup &mdash; 100.0% efficiency, 0.00 left on the bench</b>, "
  "his fourth perfect week on record. He scored 83.08 because that is every "
  "point his roster had, and Tom scored 111.86. "
  "The best lineup manager in league history could not have done one thing differently, and he handed "
  "&rsquo;11 the all-time lead doing it."),
 ("&#129482;","Greg has lost three in a row","Uncle Rico",
  "Dan beat him <b>113.00 to 102.30</b> and that is now <b>three straight defeats</b> for the man who started "
  "8&ndash;0. He is 8&ndash;3 and no longer top of the table: Max is <b>9&ndash;2</b> after putting 136.12 on "
  "Taylor, with a season optimal of <b>1554.52</b> that is a hundred and sixty-three clear of the next roster. "
  "The 8&ndash;0 looks further away every week."),
 ("&#128128;","Scott left the win on the bench too","scert",
  "Armstrong beat him <b>93.86 to 90.54</b>, by 3.32. Scott left <b>15.60</b> on his bench at 85.3% efficiency; "
  "his optimal lineup was <b>106.14</b>, which would have won the game comfortably. "
  "He is 4&ndash;7 having scored 1063.82 and conceded <b>1220.82</b>, the second-worst luck in the league, "
  "and this week he did not need luck. He needed to look at his own roster."),
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
 "This one stings, so the corner will give it to him straight and then give him the good half. "
 "Joe lost to Brian <b>103.00 to 69.96</b> with the <b>worst lineup of the week &mdash; 66.5% efficiency, "
 "35.30 points left on the bench</b>. "
 "Now the straight part: <b>his optimal lineup was 105.26.</b> Brian scored 103.00. "
 "<b>The winning team was on his roster and he did not start it.</b> "
 "And the good half is the same sentence read the other way &mdash; for the first time in a long while, "
 "Joe&rsquo;s problem this week was not that his players were bad. <b>Ashton Jeanty went for 25.40</b>, a "
 "top-five score across the entire league. The roster showed up. "
 "He is 2&ndash;9 and has still faced more points than anyone, <b>1225.12</b>. "
 "Set the right eleven next week and this is a different season.")
NEXTWEEK = [
 ("The Skin","Uncle Rico","Sam 6&ndash;5 vs Greg 8&ndash;3",
  "Cross-class, and Greg is falling. Three straight defeats, 102.30 last week, and Sam has won two of three "
  "to climb to 6&ndash;5. With the all-time series at 62&ndash;61 every cross-class game is now a rivalry "
  "decider, and there are three of them next week."),
 ("maxhagler","Roughnecks","Max 9&ndash;2 vs Joe 2&ndash;9",
  "The best record against the worst. Max has a season optimal of 1554.52 and has scored 1331.72, both the "
  "most in the league. Joe just posted 69.96. Cross-class, which means Joe is carrying &rsquo;11&rsquo;s "
  "one-game lead into the hardest fixture on the board."),
 ("Table Smashers","scert","Tyler 5&ndash;6 vs Scott 4&ndash;7",
  "Two men who deserve better. Tyler ran a perfect lineup and lost; Scott had a winning lineup available at "
  "106.14 and left it on the bench. Between them they have conceded 2310.90 points. "
  "Cross-class, and whoever loses can fairly claim the league is rigged against them."),
 ("Kids College Funds","Team bxkeegan","Armstrong 7&ndash;4 vs Brian 6&ndash;5",
  "Quietly the most consequential intra-class game of the week. Armstrong is 7&ndash;4 and third; Brian is "
  "6&ndash;5 with the fewest points of anyone above .500 at 1012.84 and a habit of winning anyway. "
  "Both of them are still in this."),
]
CLASS_WK=(0,1); CLASS_PPG=(97.38,97.79); CLASS_SEASON=(20,15); CLASS_ALLTIME=(61,62)


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

# The rest of the slate. NEXTWEEK only carries four write-ups, which meant two
# real fixtures vanished from the page every week -- Sam spotted his own missing
# from week 10. These are derived from _real, the schedule the guard fetched, so
# they are always complete and always correct.
_REC = {t: f"{w}&ndash;{l}" for t, w, l, *_ in STAND}
_shown = {frozenset((a, b)) for a, b, _, _ in NEXTWEEK}
_rest = sorted(tuple(sorted(p)) for p in _real if p not in _shown)
if _rest:
    nextweek_html += '<p class="nwrest-h">Also on the slate</p>' + "".join(
        f'<div class="nw rest"><div class="nwh">'
        f'<span class="nwt c{cls(a)}">{a}</span><span class="nwv">v</span>'
        f'<span class="nwt c{cls(b)}">{b}</span>'
        f'<span class="nwr">{_REC.get(a,"?")} vs {_REC.get(b,"?")}</span>'
        f'{"<span class=\'nwx\'>cross-class</span>" if cls(a) != cls(b) else ""}'
        f'</div></div>' for a, b in _rest)
    print(f"  also on the slate: {len(_rest)} further fixture(s) rendered")
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
.nwrest-h{{font-family:"IBM Plex Mono",monospace; font-size:9.5px; font-weight:600;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink-3); margin:26px 0 12px}}
.nw.rest{{margin-bottom:10px; padding-top:0; padding-bottom:0}}
.nw.rest .nwh{{margin-bottom:0}}
.nwx{{font-family:"IBM Plex Mono",monospace; font-size:9px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--c12)}}
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
  <p class="sub">{SUB}</p>

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
