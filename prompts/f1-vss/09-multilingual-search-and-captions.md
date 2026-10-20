# F1-VSS 9 - Multilingual search and captions

**Purpose:** search the race archive in English, German and Spanish and export subtitled clips per language.

Requires: demo 2.

---

## Paste into Cursor

```
Demo 9: multilingual search and captions.

Steps
1. Create table f1demo.transcript (race_id, start_ts, end_ts, text, lang).
2. Transcribe the commentary with Canary-1B (optional ASR model, see the gpu README) and insert the transcript.
3. Translate segment captions and the transcript to German and Spanish with Cosmos3-Reason; store the translated captions in f1demo.caption_i18n (source, lang, caption).
4. Run the demo 2 queries in English, German and Spanish through retrieval-search and compare results.
5. Export one subtitled clip per language (ffmpeg subtitles filter), upload to Drive, write out/multilingual.json.

Done when a German query returns the same top result as its English equivalent.
```
