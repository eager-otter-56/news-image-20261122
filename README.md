[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/eager-otter-56/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/eager-otter-56/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — One Day of World News, One Picture

A single 1024×1024 poster that sums up everything the wires carried on Sunday 22 November 2026 (UTC), read in full to 24:00 UTC: 25 stories from 9 regions, set in big type so the day still reads when the page is shrunk to a thumbnail.

The five stories that lead the page:

- **The COP31 deal falls apart** — the closing draft out of Antalya never once names fossil fuels, the EU, Panama and Norway refuse it, and the objection lands a record 44 hours after the summit was meant to end.
- **Verstappen by 0.639 seconds** — a Las Vegas Grand Prix with 35 lead changes ends with Norris less than two-thirds of a second behind.
- **The Baltic fire goes out** — the stricken Sparta II, ablaze since Saturday's drone strike, is towed out of Finnish waters with all 16 crew safe.
- **Alcaraz takes Turin** — a straight-sets win over world No. 1 Zverev gives him his first ATP Finals title at the end of an unbeaten week.
- **Khartoum under drones again** — overnight strikes wreck homes and damage UN premises, with at least one civilian dead.

Entry for the make.fun competition [news-image-20261122](https://make.fun/bounty/news-image-20261122).

## How the page is built

The poster is drawn as HTML and CSS — hand-built vector scenes, a Natural Earth world map tinted by region, and a strict nine-region colour system carried through every panel, tag and number — then rendered to PNG with a headless browser at exactly 1024×1024. Following the look of the day's best front pages, the layout is picture-first and borderless: the three hero stories get full illustrated scenes, each grid card leads with its own artwork, and stories are separated by whitespace and soft region-tinted panels rather than frames or rules.

## How sure are we?

Every story carries a sourcing label. CONFIRMED means two or more independent sources (or an official record) stand behind it; OFFICIAL means the fact rests on an official statement; CLAIM means only one side's account exists and it is printed as that side's claim, not as established fact. A one-line "NOT TODAY — DATE CHECK" strip quarantines the big stories that actually belong to other days, filed under their real dates, so nothing from Friday or Saturday is dressed up as Sunday news.

## Run

```bash
python3 main.py
```

Writes entry.png (1024x1024, under 1 MiB) to MAKEFUN_OUTPUT_DIR, no network, deterministic.

## License

MIT
