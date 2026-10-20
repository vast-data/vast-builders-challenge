# DFL 3 - Rights-aware licensing storefront

**Purpose:** a buyer-facing storefront where search results carry rights, partner routing (Sportcast vs IMG) and price, and licensed exports are metered.

Requires: `00-foundation.md`.

---

## Paste into Cursor

```
Prompt ID: dfl-archive/03-rights-aware-licensing-storefront

Using the DFL foundation, build the Storefront tab.

- The sidebar buyer persona sets territory and use type (social, broadcast, documentary, advertising).
- Search uses search_text. Join each result to dfl.rights for the buyer's territory group and use type and show: allowed or not, partner (Sportcast or IMG), term, and price per licensed minute from dfl.rate_card.
- Preview: play the result's segment clips in the app with a "PREVIEW" and buyer id overlay on the player. Do not re-encode video. Previews bill at the clip rate.
- "Add to cart" lets me choose in and out points in 5 s steps within one indexed 30 s chunk (each chunk is its own asset). A longer license lists each chunk as its own line item.
- "License" creates a license record shown in the app: buyer, territory, use type, partner, term, clips, minutes and price. Nothing is exported or uploaded.
- Metering: @metered("preview", "clip") on preview, @metered("license", "minute") on license, partner resolved from rights so the Meter tab shows the IMG vs Sportcast split.
- Show the same clip as a Brazil social buyer, an Austrian broadcast buyer and a US advertising buyer (ROW advertising is not granted) to prove routing and blocking.

Acceptance: blocked rights hide the license button and show the reason; every license has a usage_events row with price and partner.
```
