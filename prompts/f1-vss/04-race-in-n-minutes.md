# F1-VSS 4 - Race in N minutes

**Purpose:** auto-edit market-specific race highlight packages (e.g. 3 min UK English, 5 min DE German) with translated captions.

Requires: demos 1, 2 and 3.

---

## Paste into Cursor

```
Demo 4: race in N minutes.

Config
- config/packages.yaml: [{n_minutes: 3, market: "UK", language: "en"}, {n_minutes: 5, market: "DE", language: "de"}].

Steps
1. Uses the demo 2 tags, f1demo.periods (demo 3) and f1demo.sponsor_exposure (demo 1) for the race.
2. Score each segment: overtake 5, crash or spin 5, start 4, safety_car 3, battle 3, pit_stop 2, finish 5, podium 4, else 0; +1 if a sponsor from brands.yaml is visible.
3. For each package: always include start, chequered_flag and podium; fill the rest by score in time order until n_minutes; no two segments within 20 s of each other.
4. Assemble with ffmpeg (0.3 s crossfades) and burn in captions, translating each segment caption to the package language with Cosmos3-Reason.
5. Upload to Drive; track cost with asset_type="package".
6. Write out/packages.json: {packages: [{market, n_minutes, drive_preview_url, segments: [...], cost}]}.

Done when
- Each package is within 5 s of its target length.
- Captions on the DE package are in German.
```
