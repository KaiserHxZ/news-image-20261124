[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/KaiserHxZ/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/KaiserHxZ/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)
Bounty: https://make.fun/bounty/news-image-20261124

# The Day's News — Tuesday, 24 November 2026

A one-page newspaper front page summing up Tuesday 24 November 2026,
drawn entirely in code (see `draw.py`, Pillow + DejaVu TrueType fonts —
no photographs, no AI-generated imagery, so no garbled text). One
dominant lead story, four supporting stories, and an also-today strip.

## Research window — read this first

Researched on **24 November 2026, 01:00–01:35 UTC (08:00–08:35 WIB)**.
The day was only about an hour and a half old in UTC when research ran,
so the page covers Asia-Pacific morning news plus events scheduled for
later on Tuesday (the CAS verdict in the afternoon, the Davis Cup
quarter-final in the evening, the supermoon peak at 14:53 UTC). Events
that happened later on 24 November are **not** covered. Nothing on the
page is speculation presented as fact: the lead story reports a verdict
that is *due* today, with the outcome unknown at build time.

## The five stories (each verified by at least two independent outlets)

1. **LEAD — CAS to rule today on Senegal's AFCON title appeal**
   (Africa / sport & law). The Court of Arbitration for Sport said on
   Monday 23 November that its decision on Senegal's appeal would be
   rendered "Tuesday 24 November 2026 in the course of the afternoon".
   Senegal are contesting the CAF decision that stripped them of the
   Africa Cup of Nations title — awarded 3–0 to Morocco — after
   Senegal walked off during the January final in Rabat.
   Confirmed by: Reuters ("CAS to rule on Senegal's AFCON title appeal
   on Tuesday", 23 Nov 2026) and SuperSport ("CAS to rule on Senegal's
   AFCON title appeal on Tuesday", 23 Nov 2026); background also in
   Sowetan and pmnsports. A Marca report claiming the outcome had
   already leaked in Morocco's favour is unconfirmed speculation and is
   deliberately NOT shown as fact.

2. **Japan: factories up, services cool** (Asia / economy). Japan's
   flash November PMIs, released Tuesday 24 November 2026 at 00:30 UTC:
   manufacturing 53.7 (up from 53.3 in October), services 50.5 (down
   from 51.7), composite 51.5 — a six-month low.
   Confirmed by: Reuters ("Japan's factory activity expands at faster
   pace in November, PMI shows", 24 Nov 2026) and TradersUnion /
   dpa-AFX ("Japan Manufacturing PMI rises to 53.7 in November", 24 Nov
   2026).

3. **Heavy-rain alerts across Indonesia** (South-East Asia / weather).
   BMKG warned of heavy to very heavy rain in many provinces for
   Tuesday 24 November, with waves of 1.25–2.5 metres in several sea
   areas. The page phrases this generally because outlets differ on the
   exact province lists.
   Confirmed by: arina.id ("BMKG: Waspada Hujan Sangat Lebat di Sejumlah
   Wilayah, Selasa 24 November 2026", 24 Nov 2026), TradingView /
   MomsMoney ("BMKG: Hujan Lebat Guyur Sejumlah Wilayah pada Selasa
   24 November 2026", 24 Nov 2026), and darilaut.id (BMKG weather
   forecast for 24 November 2026).

4. **Beaver Supermoon lights the night** (science / the sky). The
   November full moon — the Beaver Moon — peaks on Tuesday 24 November
   2026 at 14:53 UTC, about 360,800 km from Earth and close to the
   Pleiades, the first of a run of supermoons.
   Confirmed by: BBC Sky at Night Magazine ("Beaver Moon 2026: the
   November full moon is a supermoon", November 2026), National
   Geographic ("Beaver supermoon: When to see November's full moon
   2026"), the Smithsonian ("November 2026: Beaver Moon", full-moon
   calendar), and earth.com ("Beaver Supermoon: November's full moon
   will rise at its closest to Earth").

5. **Davis Cup Finals open in Bologna** (Europe / tennis). The Davis
   Cup Finals run 24–29 November 2026 in Bologna, Italy. The first
   quarter-final, Czechia v Canada, is scheduled for Tuesday 24
   November at 16:00 CET. Eight nations contest the title; Italy are
   the defending champions.
   Confirmed by: Flashscore (Davis Cup Finals draw and schedule, QF
   Czechia–Canada Tue 24 Nov 16:00 CET), Sportsnet ("Canada faces
   Czechia in Davis Cup quarterfinal in Bologna"), Tennis Canada
   ("Davis Cup Finals 2026: Canada's draw and schedule"), and
   Wikipedia ("2026 Davis Cup Finals").

## Also-today strip (single-source scheduled / tracker items)

- Kyiv under an air-raid alert in the early hours of Tuesday 24
  November (air-raid alert tracker log, alert beginning 02:01 local
  time, Shahed drone threat). Phrased strictly as an alert, not as a
  strike outcome.
- Germany's Ifo business survey due on Tuesday (Reuters "Trading Day"
  markets preview, 23 Nov 2026, and the ActionForex economic calendar
  for Tuesday 24 November 2026).

## Files

- `entry.png` — the 1024×1024 front page (rendered by `draw.py`).
- `draw.py` — the renderer. Three layout variants (A: classic
  broadsheet, B: banner lead + four columns, C: stacked bands) were
  rendered and compared against the judge criteria; variant A was
  kept. The renderer measures every wrapped text block before placing
  it, so no text overlaps, and asserts the layout stays inside the
  page. A follow-up edit added the gold frame to the lead panel and
  adjusted spacing before the final render.
- `main.ts` — copies `entry.png` to `MAKEFUN_OUTPUT_DIR`
  (default `/output`). Node 22, standard library only.

## How to re-render

```sh
python3 draw.py A entry.png
```

## License

MIT — see `LICENSE`.
