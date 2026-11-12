# DFL 3 - Rights-aware licensing storefront

**Purpose:** a buyer-facing storefront where search results carry rights, partner routing (Sportcast vs IMG) and price, and licenses are metered.

Requires: `00-foundation.md` (context only).

---

## Paste into Cursor

```
Prompt ID: dfl-archive/03-rights-aware-licensing-storefront

Build a rights-aware licensing storefront for the Bundesliga matches. Follow the DFL context prompt (dfl-archive/00-foundation) and build everything yourself: explore, search and the clip proxy, in one Streamlit app (install streamlit if it is missing).

Setup, done from the VM (the deployed app has no VastDB access)
- Assets: list the indexed chunks with retrieval-videos (explore), parse match_id from the file names, one row per chunk (asset_id = <match>_c<NNNN>). Save to dfl.assets with vast-database-vastdb-write.
- Create and seed dfl.rights (per the licensing rules in the context), dfl.rate_card (query, clip, minute, example rates marked as demo values) and dfl.usage_events.
- The deployed app reads assets and rights from a snapshot shipped in its ConfigMap, labelled with its time.
- A meter: the app prices each action from the rate-card snapshot, resolves the partner from the rights snapshot, and keeps usage events in memory with an export; a VM-side step writes the exported rows to usage_events and refreshes the snapshot.

Storefront
- A buyer selector in the app, defined in the app itself (not in a shared file): a Brazil social buyer, an Austrian broadcast buyer and a US advertising buyer.
- Search with retrieval-search. Suggested searches: "player celebrates a goal", "players shake hands before kickoff", "fans waving scarves in the stands", "coach on the sideline". Join each result to dfl.rights for the buyer's territory group and use type and show: allowed or not, partner, term, and price per licensed minute.
- Preview: play the result's segment clips through the proxy with a "PREVIEW" and buyer id overlay on the player. Previews bill at the clip rate. A "clip" is the 30 s chunk that is licensed (rights are per chunk); a preview plays one 5 s segment inside it. A buyer whose rights are blocked can still preview, but cannot license.
- "Add to cart" chooses in and out points in 5 s steps within one chunk. Overlapping lines for the same clip count once. Minutes are rounded up to the next 5 s step and prices to cents.
- "License" creates a license record shown in the app: buyer, territory, use type, partner, term, clips, minutes and price, kept in the app's memory with an export.
- Metering: record a "preview" (unit "clip") event on preview and a "license" (unit "minute") event on license, so a Meter tab shows the IMG vs Sportcast split; export events and write them to usage_events from the VM to persist them.
- Reset the preview and the cart inputs when the buyer or the search changes.

Acceptance: the same clip shows as allowed for the Brazil social and Austrian broadcast buyers and blocked, with the reason, for the US advertising buyer; blocked rights hide the license button; every license has a usage_events row with price and partner.
```
