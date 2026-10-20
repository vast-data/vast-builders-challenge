# DFL 5 - Governed training-data product

**Purpose:** package archive slices as a governed, de-duplicated training dataset with a dataset card and an access log.

Requires: `00-foundation.md`.

---

## Paste into Cursor

```
Using the DFL foundation, build the Datasets tab.

- Slice builder: a text query plus filters (era, competition, seasons, caption must exist) selects candidate segments via retrieval-search.
- De-duplicate with vector similarity: read the segment embeddings (retrieval-vastdb-read, including the vectors column via the vector-select patch it mentions) and drop segments above a cosine threshold (default 0.97) to an already selected one. Show how many were removed.
- Create the slice as a VAST DataBase table dfl.ds_<name> with segment source, start_s, end_s, caption, era, rights summary. Copy the clips to S3 datasets/<name>/ with a dedicated access key for the buyer.
- Generate a markdown dataset card: hours, segment count, eras covered, caption coverage, de-dup threshold, rights basis, model versions (Cosmos3-Reason, Cosmos-Embed1), created date.
- Access log: read the VAST S3 audit records for that prefix and show them, so a buyer's training job is visible as reads per object.
- Metering: @metered("dataset_build", "hour") on delivery, @metered("dataset_access", "access") from the audit records.

Acceptance: a slice such as "set pieces 1990 to 2010" builds with a card, a de-dup count and an access log after a test download.
```
