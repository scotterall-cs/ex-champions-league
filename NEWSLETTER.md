# Weekly recap — how to build it

Everything needed to produce a week's recap lives in this repo. Run it every Tuesday once Monday Night Football is final.

## The sequence

```bash
python tools/pull.py <week>          # emits every data block, ready to paste
# paste the blocks into tools/recap.py, tools/recordbook.py, tools/build.py
# add the week's one-line summary to tools/weeks.json
python tools/build.py                # -> 2011-vs-2012.html
python tools/recordbook.py           # -> record-book.html
python tools/recap.py                # -> week-<n>.html
python tools/make_index.py           # -> index.html
python tools/verify.py <week> week-<week>.html    # MUST pass
git add -A && git commit && git push
```

**If `verify.py` reports any failure, do not commit.** It prints `DO NOT PUBLISH`. Fix the page or stop and report; never push a failing page.

Before starting, confirm the week is actually final: `tools/pull.py` warns if the NFL leg suggests games are still outstanding.

## What you write yourself

`pull.py` gives you every number. You write only the prose:

- **`STORIES`** in `recap.py` — four items, `(emoji, kicker, team, body)`. The subject must be a team name from the roster map, or any string if the story covers more than one team (the colour falls back to neutral).
- **`CALLOUT`** — the Roughnecks corner. See below.
- **`NEXTWEEK`** — four previewed matchups. **Copy the pairings from the bottom of `pull.py` output. Never type them from memory.** `recap.py` fetches the real schedule and aborts if a previewed matchup does not exist.
- The one-line week summary in `tools/weeks.json`.

## Tone

Edgy and provocative. Insults are fine and expected — this is a twelve-man fraternity league that asked for it. But **every jab must be tied to a real number**, because the league checks. Include a "Settle it in the chat" style provocation in the text version aimed at named managers.

Never invent a statistic to make a joke land. If the data doesn't support the angle, change the angle.

## The Roughnecks corner — recurring, do not drop

A highlighted box about **Joe (Roughnecks)**, warm and tongue-in-cheek, tagged "By request". It started in week 4 of 2026 at Joe's request and the league liked it, so it runs every week.

- Always about Joe, win or lose. If he wins, celebrate it properly.
- Every figure real: week-over-week score, his rank that week, lineup efficiency, margin, points against.
- Keep the "By request" tag — it is what stops it reading as pity.
- If a week offers nothing kind, say so briefly rather than inventing a silver lining.

## Standing rules

- Weekly standings carry **Record · Points for · Points against · Optimal** (season optimal = what every lineup would have scored if perfectly set).
- The index keeps the latest week at top with prior weeks beneath, so recaps archive rather than replace.
- Refresh the 2026 row of `build.py` and the all-time tables in `recordbook.py` every week, not just the recap page.
- Any sentence that restates a number in words must be derived, not typed. The class-war captions already compute themselves — leave them that way.

## Things that have gone wrong before

- **Four invented matchups shipped** because the preview was typed from memory instead of fetched. Hence the schedule guard in `recap.py` and check 6 in `verify.py`.
- **A hardcoded "the gap is down to four"** survived three weeks of regeneration while the real gap moved to seven.
- **A dead check passed silently** — `verify.py` now fails any check that matches zero rows.
- **Sleeper renames players** ("James Cook" became "James Cook III" mid-season), so `verify.py` compares names with suffixes stripped.
- Several stats were wrong on first draft and only caught by checking: a score that "beat four teams" had beaten six; a combined total of "117" was 183.58.

## Roster map

| Team | Manager | Class |
|---|---|---|
| Table Smashers | Tyler (commissioner) | '12 |
| maxhagler | Max | '12 |
| The Skin | Sam | '12 |
| vaught12 | Taylor | '12 |
| Cooking With Friends | Detrick | '12 |
| Kids College Funds | Armstrong | '11 |
| scert | Scott | '11 |
| Roughnecks | Joe | '11 |
| YoSoyFiesta | Dan | '11 |
| Uncle Rico | Greg | '11 |
| Win One for the Lipper | Tom | '11 |
| Team bxkeegan | Brian | '11 |

Sleeper league IDs: 2026 `1389693216323817472` · 2025 `1250184185579048960` · 2024 `1125051564969459721`.
