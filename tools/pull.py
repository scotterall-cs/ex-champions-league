# -*- coding: utf-8 -*-
"""
Emits every data block for a given week, ready to paste into the generators.

    python tools/pull.py <week>

Nothing here is typed by hand. Paste the output into:
  tools/recap.py      GAMES, STAND, EFF, TOP, DUDS, CLASS_WK/PPG/SEASON/ALLTIME
  tools/recordbook.py STAND, BEST, BLOW, STREAK, EFF
  tools/build.py      the 2026 SEASONS row
Then write STORIES / CALLOUT / NEXTWEEK prose yourself and run the generators.
"""
import sys, json, urllib.request
from collections import defaultdict

LEAGUE = "1389693216323817472"
SEASONS = [("2024", "1125051564969459721", 14),
           ("2025", "1250184185579048960", 14),
           ("2026", LEAGUE, None)]
TEAM = {1: "Table Smashers", 2: "maxhagler", 3: "The Skin", 4: "vaught12",
        5: "Kids College Funds", 6: "Cooking With Friends", 7: "scert", 8: "Roughnecks",
        9: "YoSoyFiesta", 10: "Uncle Rico", 11: "Win One for the Lipper", 12: "Team bxkeegan"}
WHO = {1: "Tyler", 2: "Max", 3: "Sam", 4: "Taylor", 5: "Armstrong", 6: "Detrick",
       7: "Scott", 8: "Joe", 9: "Dan", 10: "Greg", 11: "Tom", 12: "Brian"}
CLS = {1: "12", 2: "12", 3: "12", 4: "12", 6: "12",
       5: "11", 7: "11", 8: "11", 9: "11", 10: "11", 11: "11", 12: "11"}

def api(p):
    with urllib.request.urlopen("https://api.sleeper.app/v1/" + p) as r:
        return json.load(r)

P = api("players/nfl")
def pos(p): return (P.get(p) or {}).get("position")
def pname(p):
    d = P.get(p) or {}
    return d.get("full_name") or d.get("last_name") or p

def optimal(roster, pts):
    pool = defaultdict(list)
    for p in roster: pool[pos(p)].append((pts.get(p, 0), p))
    for k in pool: pool[k].sort(reverse=True)
    used, tot = set(), 0.0
    for slot in ["QB", "RB", "RB", "WR", "WR", "TE", "K", "DEF"]:
        c = [x for x in pool.get(slot, []) if x[1] not in used]
        if c: used.add(c[0][1]); tot += c[0][0]
    flex = sorted([x for k in ("RB", "WR", "TE") for x in pool.get(k, []) if x[1] not in used], reverse=True)
    if flex: tot += flex[0][0]
    return round(tot, 2)

def pairs(lid, wk):
    by = defaultdict(list)
    for m in api("league/%s/matchups/%d" % (lid, wk)):
        if m.get("matchup_id") is not None: by[m["matchup_id"]].append(m)
    return [v for v in by.values() if len(v) == 2]

WEEK = int(sys.argv[1])
wk = pairs(LEAGUE, WEEK)
if not wk:
    sys.exit("No matchups for week %d yet." % WEEK)

state = api("state/nfl")
if state["leg"] <= WEEK:
    print("!! WARNING: NFL leg is %d — week %d may not be final. Check before publishing.\n" % (state["leg"], WEEK))

wk_pts = {m["roster_id"]: round(m["points"], 2) for g in wk for m in g}
wk_opt = {m["roster_id"]: optimal(m["players"], m["players_points"]) for g in wk for m in g}

print("=" * 72)
print("recap.py  GAMES")
print("=" * 72)
rows = []
for a, b in wk:
    hi, lo = (a, b) if a["points"] >= b["points"] else (b, a)
    x = CLS[hi["roster_id"]] != CLS[lo["roster_id"]]
    rows.append((hi["points"], ' ("%s",%.2f,"%s",%.2f,%s),' % (
        TEAM[hi["roster_id"]], hi["points"], TEAM[lo["roster_id"]], lo["points"], x)))
print("GAMES = [")
for _, r in sorted(rows, reverse=True): print(r)
print("]")

# season aggregates
season = defaultdict(lambda: [0, 0, 0.0, 0.0, 0.0])
allx = {"11": 0, "12": 0}; seasx = {"11": 0, "12": 0}; wkx = {"11": 0, "12": 0}
tw = []; games = []; seq = defaultdict(list)
act = defaultdict(float); opts = defaultdict(float); perf = defaultdict(int)
for sn, lid, last in SEASONS:
    for w in range(1, (last if last else WEEK) + 1):
        for a, b in pairs(lid, w):
            for m in (a, b):
                o = optimal(m["players"], m["players_points"])
                act[m["roster_id"]] += m["points"]; opts[m["roster_id"]] += o
                if o and m["points"] / o >= 0.999: perf[m["roster_id"]] += 1
                tw.append((m["points"], sn, w, m["roster_id"]))
                if sn == "2026":
                    season[m["roster_id"]][2] += m["points"]; season[m["roster_id"]][4] += o
            hi, lo = (a, b) if a["points"] >= b["points"] else (b, a)
            games.append((round(hi["points"] - lo["points"], 2), sn, w,
                          hi["roster_id"], hi["points"], lo["roster_id"], lo["points"]))
            seq[hi["roster_id"]].append(1); seq[lo["roster_id"]].append(0)
            if CLS[hi["roster_id"]] != CLS[lo["roster_id"]]:
                allx[CLS[hi["roster_id"]]] += 1
                if sn == "2026":
                    seasx[CLS[hi["roster_id"]]] += 1
                    if w == WEEK: wkx[CLS[hi["roster_id"]]] += 1
            if sn == "2026":
                season[hi["roster_id"]][0] += 1; season[lo["roster_id"]][1] += 1
                season[hi["roster_id"]][3] += lo["points"]; season[lo["roster_id"]][3] += hi["points"]

print()
print("=" * 72); print("recap.py  STAND   (record, PF, PA, season optimal)"); print("=" * 72)
print("STAND=[", end="")
for i, (r, v) in enumerate(sorted(season.items(), key=lambda kv: (-kv[1][0], -kv[1][2]))):
    print('%s("%s",%d,%d,%.2f,%.2f,%.2f)' % ("" if i == 0 else ",\n ", TEAM[r], v[0], v[1], v[2], v[3], v[4]), end="")
print("]")

print()
print("=" * 72); print("recap.py  EFF   (weekly efficiency, points left on bench)"); print("=" * 72)
eff = sorted(((wk_pts[r] / wk_opt[r] if wk_opt[r] else 0), r) for r in wk_pts)
print("EFF=[", end="")
for i, (e, r) in enumerate(reversed(eff)):
    print('%s("%s",%.1f,%.2f)' % ("" if i == 0 else ",\n ", TEAM[r], e * 100, wk_opt[r] - wk_pts[r]), end="")
print("]")

starts = []
for g in wk:
    for m in g:
        for s in m["starters"]:
            if s != "0":
                starts.append((m["players_points"].get(s, 0), pname(s), pos(s), TEAM[m["roster_id"]]))
print()
print("=" * 72); print("recap.py  TOP / DUDS"); print("=" * 72)
print("TOP=[", end="")
for i, (p, n, ps, t) in enumerate(sorted(starts, reverse=True)[:5]):
    print('%s(%.2f,"%s","%s","%s")' % ("" if i == 0 else ",\n ", p, n, ps, t), end="")
print("]")
print("DUDS=[", end="")
for i, (p, n, ps, t) in enumerate(sorted(starts)[:4]):
    print('%s(%.2f,"%s","%s","%s")' % ("" if i == 0 else ",\n ", p, n, ps, t), end="")
print("]")

p12 = [wk_pts[r] for r in wk_pts if CLS[r] == "12"]
p11 = [wk_pts[r] for r in wk_pts if CLS[r] == "11"]
print()
print("=" * 72); print("recap.py  class war"); print("=" * 72)
print("CLASS_WK=(%d,%d); CLASS_PPG=(%.2f,%.2f); CLASS_SEASON=(%d,%d); CLASS_ALLTIME=(%d,%d)"
      % (wkx["12"], wkx["11"], sum(p12) / len(p12), sum(p11) / len(p11),
         seasx["12"], seasx["11"], allx["12"], allx["11"]))

print()
print("=" * 72); print("build.py  2026 SEASONS row"); print("=" * 72)
pf12 = sum(season[r][2] for r in season if CLS[r] == "12")
pf11 = sum(season[r][2] for r in season if CLS[r] == "11")
n12 = sum(1 for r in season if CLS[r] == "12")
n11 = sum(1 for r in season if CLS[r] == "11")
print(' ("2026","Sleeper",None,None,None,(%d,%d),(%.2f,%.2f),"m"),'
      % (seasx["12"], seasx["11"], pf12 / (WEEK * n12), pf11 / (WEEK * n11)))

rec = defaultdict(lambda: [0, 0, 0.0, 0.0])
for m, s, w, hr, hp, lr, lp in games:
    rec[hr][0] += 1; rec[lr][1] += 1
    rec[hr][2] += hp; rec[hr][3] += lp; rec[lr][2] += lp; rec[lr][3] += hp
print()
print("=" * 72); print("recordbook.py  STAND  (%d games each)" % (rec[1][0] + rec[1][1])); print("=" * 72)
print("STAND=[", end="")
for i, (r, v) in enumerate(sorted(rec.items(), key=lambda kv: (-kv[1][0], -kv[1][2]))):
    print('%s("%s","%s",%d,%d,%.1f,%.1f,%.2f)' % ("" if i == 0 else ",\n ",
          TEAM[r], WHO[r], v[0], v[1], v[2], v[3], v[2] / (v[0] + v[1])), end="")
print("]")

print()
print("=" * 72); print("recordbook.py  BEST / BLOW / STREAK / EFF"); print("=" * 72)
print("BEST=[", end="")
for i, (p, s, w, r) in enumerate(sorted(tw, reverse=True)[:6]):
    print('%s(%.2f,"%s","%d","%s")' % ("" if i == 0 else ",\n ", p, s, w, TEAM[r]), end="")
print("]")
print("BLOW=[", end="")
for i, (m, s, w, hr, hp, lr, lp) in enumerate(sorted(games, reverse=True)[:5]):
    print('%s(%.2f,"%s","%d","%s",%.2f,"%s",%.2f)' % ("" if i == 0 else ",\n ",
          m, s, w, TEAM[hr], hp, TEAM[lr], lp), end="")
print("]")
streaks = {}
for r, v in seq.items():
    bw = bl = cw = cl = 0
    for x in v:
        if x: cw += 1; cl = 0
        else: cl += 1; cw = 0
        bw = max(bw, cw); bl = max(bl, cl)
    streaks[r] = (bw, bl)
print("STREAK=[", end="")
for i, (r, (bw, bl)) in enumerate(sorted(streaks.items(), key=lambda kv: -kv[1][0])):
    print('%s("%s","%s",%d,%d)' % ("" if i == 0 else ",\n ", TEAM[r], WHO[r], bw, bl), end="")
print("]")
print("EFF=[", end="")
for i, r in enumerate(sorted(act, key=lambda r: -act[r] / opts[r])):
    print('%s("%s","%s",%.1f,%.1f,%d)' % ("" if i == 0 else ",\n ",
          TEAM[r], WHO[r], act[r] / opts[r] * 100, opts[r] - act[r], perf[r]), end="")
print("]")

print()
print("=" * 72); print("NEXT WEEK schedule (week %d) — NEVER type these, copy them" % (WEEK + 1)); print("=" * 72)
nxt = pairs(LEAGUE, WEEK + 1)
if not nxt:
    print("  (not published yet)")
else:
    recd = {r: "%d-%d" % (season[r][0], season[r][1]) for r in season}
    for a, b in nxt:
        ra, rb = a["roster_id"], b["roster_id"]
        print('  ("%s","%s","%s %s vs %s %s")   %s'
              % (TEAM[ra], TEAM[rb], WHO[ra], recd.get(ra, "?"), WHO[rb], recd.get(rb, "?"),
                 "CROSS-CLASS" if CLS[ra] != CLS[rb] else "intra"))
    print("  cross-class next week: %d of %d"
          % (sum(1 for a, b in nxt if CLS[a["roster_id"]] != CLS[b["roster_id"]]), len(nxt)))
