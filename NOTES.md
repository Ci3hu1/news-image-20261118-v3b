# NOTES.md — THE DAY IN WORLD NEWS, 18 Nov 2026

## Build notes

- Built fresh, sight-unseen, from the brief only — no earlier entry, repo
  or leaderboard material was read while writing this version.
- The prompt file supplied for this build
  (`news-image-20261118-v3-prompt.txt`) contained only the text "Coba 50"
  (7 bytes), not the full brief. This build follows the brief as given in
  the task instead: 1024×1024 front page, 45 stories, 13 flat-illustrated,
  one-line day summary, labelled maps, BY THE NUMBERS strip, dotted world
  map with numbered pins, briefs 14–45, stdlib-only `main.py` with bundled
  `entry.png` fallback (render only when Pillow AND all DejaVu faces exist,
  otherwise copy `entry.png` byte-for-byte), tests, README with make.fun
  badges, STRATEGY.md, NOTES.md, MIT LICENSE.
- Work directory `news-image-20261118-v3b`, repo `Ci3hu1/news-image-20261118-v3b`.
- Rendered with Python 3.12.3 + Pillow 10.2.0 + DejaVu (system fonts).
- `entry.png` sha256: `73192c19bbf90b38c1fe6e4649c05d6599ede4568bdf801a9a04685586299b82`
- Tests: `python3 -m unittest discover -s tests -v` — 10 tests, all passing
  (counts, distinct illustration motifs, map pins in bounds, no non-stdlib
  imports, text-fit checks with real fonts, render 1024×1024, bundled image
  matches fresh render, fallback byte-for-byte copy).
- Two render bugs found and fixed during the build: the summit illustration
  assumed a tall strip (fixed by drawing it proportionally), and story decks
  were placed at fixed offsets so long headlines overflowed their boxes
  (fixed by placing each deck directly after its headline).

## Sources (headlines as reported on 18 Nov 2026)

- Gulf strikes / Kerch Bridge / Peltola / Ebola / Cyclone Xavier / World
  Court — One Turn, "World news today: Gulf Strikes, Crimea Bridge,
  Three-Leader Summit" (https://oneturn.news/news/) and Zark News daily
  briefing 18 Nov 2026 (https://zarknews.com/zark-news-daily-briefing-november-18-2026/)
- Iran MQ-9 / Patriot systems in Kuwait / PNG 6.0 and Romania 5.3 quakes /
  Siberian plane crash (19 dead) — Daily Baku world desk
  (https://dailybaku.az/en/category/dunya)
- Nvidia $115.8B revenue (+103% YoY), Q4 guide $130B, interim CEO Colette
  Kress, Huang resigned; shares +4.8% after hours to $163 — XTB morning
  wrap 18 Nov 2026 (https://xtb.com/int/market-analysis/news-and-research/morning-wrap-18-11-2026),
  TechCrunch (https://techcrunch.com/2026/11/17/nvidia-promises-that-revenue-will-keep-soaring-for-now/)
- Voyager 1 one light-day (~16bn miles) — Zark News briefing, 18 Nov 2026
- US measles elimination status lost (5,412 cases, 10 deaths) — Zark News
  briefing; Horizon world news 18 Nov 2026
  (https://www.horizonapp.link/en/2026/11/18)
- COP31 draft / Africa outrage / climate finance down >70% in 2026 —
  NatureNews Africa
  (https://naturenews.africa/cop31-draft-sparks-africa-outrage-over-fossil-fuels-climate-finance/);
  EU "untenable" warning — EuropeSays/Bloomberg
  (https://www.europesays.com/europe/184364/)
- Markets (S&P 500 −1.03% to 7,340.53; VIX 25.46; Brent $91.55; gold
  $3,775) — Horizon, 18 Nov 2026 (figures as published there that day)
- GTA 6 midnight unlock 19 Nov (212GB PS5 download); OpenAI GPT-6.2 Astra;
  Anthropic IPO ~7x oversubscribed; Instagram Reels content protection —
  as reported 18 Nov 2026 (see STRATEGY.md for the day's tech thread)
- Sudan 2,230 civilian deaths; Kivu combat; AFCON qualifier; COP31 ocean
  finance — PANA / Juba Global News roundups of 18 Nov 2026 reporting

Figures are quoted as published on the day; where outlets disagreed by a
decimal (e.g. Nvidia $115.8B vs $116B rounded), the more precise published
figure is used.
