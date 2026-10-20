# DFL 3 - Rights-aware licensing storefront

**Purpose:** a buyer-facing storefront where search results carry rights, partner routing (Sportcast vs IMG) and price, and licensed exports are metered.

Requires: `00-foundation.md`.

---

## Paste into Cursor

```
Using the DFL foundation, build the Storefront tab.

- The sidebar buyer persona sets territory and use type (social, broadcast, documentary, advertising).
- Search uses search_text. Join each result to dfl.rights for the buyer's territory and use type and show: allowed or not, partner (Sportcast or IMG), term, and price per licensed minute from dfl.rate_card.
- Preview: a watermarked low-resolution version made with ffmpeg on the fly, with the buyer id burned in. Source it from the playback URL in retrieval-videos.
- "Add to cart" lets me trim in and out points. "License and export" writes the clip at full quality to S3 exports/<buyer_id>/ and returns a presigned URL.
- Metering: @metered("preview", "clip") on preview, @metered("license", "minute") on export, partner resolved from rights so the Meter tab shows the IMG vs Sportcast split.
- Show the same clip as a Brazil social buyer and an Austrian broadcast buyer to prove the routing.

Acceptance: blocked rights hide the export button and show the reason; every export has a usage_events row with price and partner.
```
