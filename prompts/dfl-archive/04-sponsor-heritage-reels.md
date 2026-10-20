# DFL 4 - Sponsor heritage reels

**Purpose:** measure a sponsor's screen time across seasons and auto-cut a heritage reel plus a one-page report.

Requires: `00-foundation.md`. Shares detection logic with `f1-vss/01-sponsor-exposure-ledger.md`.

---

## Paste into Cursor

```
Using the DFL foundation, build the Sponsors tab. Reuse the sponsor detection code from the F1 sponsor exposure ledger demo if it exists in this workspace.

- Input: a sponsor name and one to three reference logo images. Store in dfl.brands(brand_id, name, ref_images_s3).
- Detection: the stack's YOLO11 is a fixed-class detector, so do brand detection by sampling frames at 2 fps and asking Cosmos3-Reason (see the gpu README) whether the brand is visible and where (shirt, board, other), with the reference images in the prompt. Write dfl.detections(asset_id, ts_s, brand_id, bbox, confidence, surface).
- Package it as a DataEngine function so new footage is scanned automatically for registered brands: dataengine-edit-function, then dataengine-build-function, dataengine-functions, dataengine-triggers (segment-land trigger), dataengine-pipeline-manifest.
- Aggregate screen time per season and per surface, chart it, and list top moments.
- Build a 60 to 90 second heritage reel from the highest-confidence moments across seasons.
- Export a one-page HTML report with screen time by season and the reel link.
- Metering: @metered("detect", "brand_minute") on detection, @metered("report", "report") on export.

Acceptance: detection runs on the demo set without manual steps, the screen-time chart renders, reel and report export.
```
