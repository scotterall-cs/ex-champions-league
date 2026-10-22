# -*- coding: utf-8 -*-
r"""
Pre-publication validator for the EX Champions League site.

Re-derives everything from the Sleeper API — independently of the generators —
and checks the rendered HTML against it. Exits non-zero on any failure so it can
gate a publish.

    python tools/verify.py <week> [path-to-week-N.html]

Checks:
  1/2 SCOREBOARD   every matchup and both scores on the page are real, none invented
  3   STANDINGS    record, points for, points against, season optimal; PF reconciles to PA
  4   EFFICIENCY   each team's weekly efficiency
  5   PERFORMERS   every named player score was actually started by that team
  6   NEXT WEEK    every previewed pairing exists in week+1's real schedule
  7   CLASS WAR    weekly, season and all-time counts, and the worded gap
  8   COMMENTARY   every number in prose traces to this week's data
"""
import sys, re, io, json, html, urllib.request
from collections import defaultdict

LEAGUE = "1389693216323817472"
SEASONS = [("2024", "1125051564969459721", 14),
           ("2025", "1250184185579048960", 14),
           ("2026", LEAGUE, None)]

TEAM = {1: "Table Smashers", 2: "maxhagler", 3: "The Skin", 4: "vaught12",
        5: "Kids College Funds", 6: "Cooking With Friends", 7: "scert", 8: "Roughnecks",
        9: "YoSoyFiesta", 10: "Uncle Rico", 11: "Win One for the Lipper", 12: "Team bxkeegan"}
CLS = {1: "12", 2: "12", 3: "12", 4: "12", 6: "12",
       5: "11", 7: "11", 8: "11", 9: "11", 10: "11", 11: "11", 12: "11"}
NAME2CLS = {TEAM[r]: CLS[r] for r in TEAM}
HISTORICAL = {"167.86"}          # deliberate all-time references

fails, warns = [], []

def check(ok, msg):
    if not ok:
        fails.append(msg)
    print(("  PASS  " if ok else "  FAIL  ") + msg)

def warn(msg):
    warns.append(msg)
    print("  WARN  " + msg)

def api(path):
    with urllib.request.urlopen("https://api.sleeper.app/v1/" + path) as r:
        return json.load(r)

print("fetching player map ...")
PLAYERS = api("players/nfl")

def pos(p):
    return (PLAYERS.get(p) or {}).get("position")

def pname(p):
    d = PLAYERS.get(p) or {}
    return d.get("full_name") or d.get("last_name") or p

_SUFFIX = (" jr", " sr", " ii", " iii", " iv", " v")
def norm_name(n):
    """Sleeper changes display names (James Cook -> James Cook III). Compare loosely."""
    x = " ".join(n.lower().replace(".", "").replace("'", "").split())
    changed = True
    while changed:
        changed = False
        for suf in _SUFFIX:
            if x.endswith(suf):
                x = x[: -len(suf)].strip(); changed = True
    return x

def optimal(roster, pts):
    pool = defaultdict(list)
    for p in roster:
        pool[pos(p)].append((pts.get(p, 0), p))
    for k in pool:
        pool[k].sort(reverse=True)
    used, tot = set(), 0.0
    for slot in ["QB", "RB", "RB", "WR", "WR", "TE", "K", "DEF"]:
        c = [x for x in pool.get(slot, []) if x[1] not in used]
        if c:
            used.add(c[0][1]); tot += c[0][0]
    flex = sorted([x for k in ("RB", "WR", "TE") for x in pool.get(k, []) if x[1] not in used],
                  reverse=True)
    if flex:
        tot += flex[0][0]
    return round(tot, 2)

def pairs(league, week):
    by = defaultdict(list)
    for m in api("league/%s/matchups/%d" % (league, week)):
        if m.get("matchup_id") is not None:
            by[m["matchup_id"]].append(m)
    return [v for v in by.values() if len(v) == 2]

def main():
    week = int(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) > 2 else "week-%d.html" % week
    raw = io.open(path, encoding="utf-8").read()
    stripped = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
    page = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", stripped)))

    print("\nVerifying %s against the Sleeper API (week %d)" % (path, week))
    print("=" * 70)

    wk = pairs(LEAGUE, week)
    wk_pts = {m["roster_id"]: round(m["points"], 2) for g in wk for m in g}
    wk_opt = {m["roster_id"]: optimal(m["players"], m["players_points"]) for g in wk for m in g}
    started = defaultdict(dict)
    for g in wk:
        for m in g:
            for s in m["starters"]:
                if s != "0":
                    started[TEAM[m["roster_id"]]][norm_name(pname(s))] = round(m["players_points"].get(s, 0), 2)

    season = defaultdict(lambda: [0, 0, 0.0, 0.0, 0.0])
    allx = {"11": 0, "12": 0}; seasx = {"11": 0, "12": 0}; wkx = {"11": 0, "12": 0}
    for sname, lid, last in SEASONS:
        for w in range(1, (last if last else week) + 1):
            for a, b in pairs(lid, w):
                hi, lo = (a, b) if a["points"] >= b["points"] else (b, a)
                if CLS[hi["roster_id"]] != CLS[lo["roster_id"]]:
                    allx[CLS[hi["roster_id"]]] += 1
                    if sname == "2026":
                        seasx[CLS[hi["roster_id"]]] += 1
                        if w == week:
                            wkx[CLS[hi["roster_id"]]] += 1
                if sname == "2026":
                    for m in (a, b):
                        season[m["roster_id"]][2] += m["points"]
                        season[m["roster_id"]][4] += optimal(m["players"], m["players_points"])
                    season[hi["roster_id"]][0] += 1; season[lo["roster_id"]][1] += 1
                    season[hi["roster_id"]][3] += lo["points"]; season[lo["roster_id"]][3] += hi["points"]

    # 1/2 scoreboard + matchups  (parsed from the scoreboard markup, NOT a page-wide
    # substring search — a correct mention elsewhere must not mask a wrong score here)
    print("\n1/2. SCOREBOARD AND MATCHUPS")
    rendered = re.findall(
        r'<span class="gt w c[^"]*">([^<]+)</span>\s*<span class="gp w">([\d.]+)</span>.*?'
        r'<span class="gt l c[^"]*">([^<]+)</span>\s*<span class="gp l">([\d.]+)</span>',
        raw, flags=re.S)
    check(len(rendered) > 0, "found %d scoreboard rows (0 would mean this check is dead)" % len(rendered))
    real_rows = set()
    for a, b in wk:
        hi, lo = (a, b) if a["points"] >= b["points"] else (b, a)
        real_rows.add((TEAM[hi["roster_id"]], "%.2f" % hi["points"],
                       TEAM[lo["roster_id"]], "%.2f" % lo["points"]))
    shown = set()
    for wn, wp, ln, lp in rendered:
        row = (html.unescape(wn).strip(), "%.2f" % float(wp),
               html.unescape(ln).strip(), "%.2f" % float(lp))
        check(row in real_rows, "%s %s def %s %s" % row)
        shown.add(row)
    missing = real_rows - shown
    for m in missing:
        check(False, "missing from scoreboard: %s %s def %s %s" % m)
    check(len(shown) == len(real_rows) and not missing,
          "all %d matchups present, none invented" % len(real_rows))

    # 3 standings
    print("\n3. STANDINGS")
    for r, (w, l, pf, pa, op) in sorted(season.items(), key=lambda kv: (-kv[1][0], -kv[1][2])):
        ok = all(v in page for v in ("%d–%d" % (w, l), "%.2f" % pf, "%.2f" % pa, "%.2f" % op))
        check(ok, "%-24s %d-%d  PF %.2f  PA %.2f  Opt %.2f" % (TEAM[r], w, l, pf, pa, op))
    tpf = round(sum(v[2] for v in season.values()), 2)
    tpa = round(sum(v[3] for v in season.values()), 2)
    check(tpf == tpa, "points for reconciles to points against (%.2f)" % tpf)

    # 4 efficiency
    print("\n4. WEEKLY EFFICIENCY")
    for r in sorted(wk_pts, key=lambda r: -(wk_pts[r] / wk_opt[r] if wk_opt[r] else 0)):
        eff = round(wk_pts[r] / wk_opt[r] * 100, 1) if wk_opt[r] else 0.0
        check("%.1f%%" % eff in page,
              "%-24s %.1f%%  (left %.2f)" % (TEAM[r], eff, wk_opt[r] - wk_pts[r]))

    # 5 named performers
    print("\n5. NAMED PLAYER SCORES")
    rows = re.findall(
        r'<span class="pv [^"]*">([\d.]+)</span>\s*<span class="pn">([^<]+?)\s*'
        r'<span class="pp">[^<]*</span>\s*</span>\s*<span class="pt">([^<]+)</span>', raw)
    check(len(rows) > 0, "found %d named player rows (0 would mean this check is dead)" % len(rows))
    for val, name, team in rows:
        name, team = html.unescape(name).strip(), html.unescape(team).strip()
        actual = started.get(team, {}).get(norm_name(name))
        if actual is None:
            check(False, "%s is not a week %d starter for %s" % (name, week, team))
        else:
            check("%.2f" % actual == "%.2f" % float(val), "%s %s started by %s" % (name, val, team))

    # 6 next week
    print("\n6. NEXT WEEK PREVIEW")
    nxt = {frozenset((TEAM[a["roster_id"]], TEAM[b["roster_id"]])) for a, b in pairs(LEAGUE, week + 1)}
    tail = raw[raw.find(">Next week<"):] if ">Next week<" in raw else ""
    prev = re.findall(r'<span class="nwt c[^"]*">([^<]+)</span>\s*<span class="nwv">v</span>\s*'
                      r'<span class="nwt c[^"]*">([^<]+)</span>', tail)
    check(len(prev) > 0, "found %d previewed matchups (0 would mean this check is dead)" % len(prev))
    for a, b in prev:
        a, b = html.unescape(a).strip(), html.unescape(b).strip()
        check(frozenset((a, b)) in nxt, "previewed %s v %s is a real week %d matchup" % (a, b, week + 1))
    xn = sum(1 for p in nxt for a, b in [tuple(p)] if NAME2CLS.get(a) != NAME2CLS.get(b))
    print("  INFO  week %d has %d cross-class game(s) of %d" % (week + 1, xn, len(nxt)))

    # 7 class war
    print("\n7. CLASS WAR")
    def either(x, y):
        return ("%d – %d" % (x, y)) in page or ("%d – %d" % (y, x)) in page
    check(either(wkx["12"], wkx["11"]), "this week %d-%d (12-11)" % (wkx["12"], wkx["11"]))
    check(either(seasx["12"], seasx["11"]), "season %d-%d (12-11)" % (seasx["12"], seasx["11"]))
    check(either(allx["11"], allx["12"]), "all time %d-%d (11-12)" % (allx["11"], allx["12"]))
    gap = allx["11"] - allx["12"]
    W = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
         7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    if gap:
        word = "a single game" if abs(gap) == 1 else W.get(abs(gap), str(abs(gap))) + " games"
        check(word in page, "all-time gap worded as '%s'" % word)

    # 8 commentary
    print("\n8. COMMENTARY NUMBERS")
    known = set()
    for d in (wk_pts, wk_opt):
        known |= {"%.2f" % v for v in d.values()}
    for v in season.values():
        known |= {"%.2f" % v[2], "%.2f" % v[3], "%.2f" % v[4]}
    for r in wk_pts:
        known.add("%.2f" % round(wk_opt[r] - wk_pts[r], 2))
    for d in started.values():
        known |= {"%.2f" % v for v in d.values()}
    for a, b in wk:
        known.add("%.2f" % abs(round(a["points"] - b["points"], 2)))
    # class-level per-team PPG for the week, and cumulative bench waste
    for c in ("11", "12"):
        vals = [wk_pts[r] for r in wk_pts if CLS[r] == c]
        if vals:
            known.add("%.2f" % (sum(vals) / len(vals)))
    for r in season:
        known.add("%.2f" % round(season[r][4] - season[r][2], 2))
    known |= {"%.2f" % round(float(v), 1) for v in known}   # pages may round to 1dp
    pcts = {"%.2f" % float(x) for x in re.findall(r"(\d+\.\d)%", page)}
    found = {"%.2f" % float(x) for x in re.findall(r"\b\d+\.\d{1,2}\b", page)}
    unknown = sorted(n for n in found if n not in known and n not in pcts and n not in HISTORICAL)
    if unknown:
        warn("%d number(s) in prose are not from week %d — confirm each is a deliberate "
             "historical reference: %s" % (len(unknown), week, ", ".join(unknown)))
    else:
        check(True, "every number in prose traces to this week's data")

    print("\n" + "=" * 70)
    print("%d failure(s), %d warning(s)" % (len(fails), len(warns)))
    if fails:
        print("\nFAILURES:")
        for f in fails:
            print("  - " + f)
        print("\nDO NOT PUBLISH.")
    else:
        print("\nOK to publish." + (" Review the warnings above first." if warns else ""))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
