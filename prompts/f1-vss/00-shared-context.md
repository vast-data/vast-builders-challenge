# F1-VSS 0 - Shared context and scaffold (run first)

**Purpose:** common helpers (clip cutting, Drive upload, GPU cost tracking, JSON output) that all twelve F1 / Formula E demos use. Segmentation, captioning, embedding and detection are already handled by the running VSS pipeline.

---

## Paste into Cursor

```
You are building GTC demos on the VSS stack that is already running in this workspace. Follow .cursor/rules/build-day.mdc and use the matching skill in .cursor/skills/ for every platform call. Do not invent your own storage layer, endpoints or model hosts.

What already exists (do not rebuild it):
- Race footage (F1 Academy / Formula E MP4s) is ingested and indexed: segmented, captioned by Cosmos3-Reason, embedded with Cosmos-Embed1 (256-dim), YOLO11 detections stored. race_id = file name without extension. Check with retrieval-videos (explore) and retrieval-dashboard.
- New MP4s: ingest-upload-video. Re-run a race with a demo-specific prompt: ingest-reingest-videos.
- Search: retrieval-search. Grounded Q&A: retrieval-agent-qa. Playback, per-video summary, detections: retrieval-videos. Auth: retrieval-login.
- Models (Cosmos3-Reason VLM/LLM, YOLO11, Cosmos-Embed1, Canary-1B ASR): see the gpu README; check them with gpu-model-health.
- Custom DataEngine functions: dataengine-edit-function, dataengine-build-function, dataengine-functions, dataengine-triggers, dataengine-pipeline-manifest.
- Raw VAST DataBase access for our own tables: follow the connection pattern in retrieval-vastdb-read. Put demo tables in schema f1demo.

Step 0: scaffold before any demo
1. Repo layout: common/, demos/<demo_name>/, config/, out/.
2. common/clips.py: cut(source, start_ts, end_ts, out_name) with ffmpeg re-encode (libx264, aac) so every clip starts on a keyframe. Source from the retrieval-videos playback URL. Write to S3 clips/<demo>/.
3. common/drive.py: upload(path, folder_name) to Google Drive with a service account (credentials path in config/drive.yaml). Permission "anyone with the link: viewer". Return file_id and preview_url = https://drive.google.com/file/d/<file_id>/preview. One Drive subfolder per demo.
4. common/costs.py: context manager track(demo, asset_id, asset_type, gpu_type) that records GPU-seconds (wall time x GPUs allocated) into f1demo.job_costs (job_id, demo, asset_id, asset_type, gpu_type, gpu_seconds, started_at, finished_at).
5. common/out.py: write_json(demo, data) to out/<demo>.json and upload it to Drive.
6. config/pricing.yaml: gpu_hourly_rate per gpu_type (I will fill in).
7. Each demo gets its own folder with a README and a run_local.py that runs it by hand on one race. Demos that must react to new footage are DataEngine functions on the segment-land trigger.

Rules for every demo
- Clips are always cut as separate MP4s (Drive previews cannot start at a timestamp).
- Every output JSON includes, per clip: asset_id, start_ts, end_ts, drive_preview_url, gpu_seconds, cost.
- Never build a UI. I embed the Drive preview URLs in my own HTML page.
- When done, print the Drive preview URL of the single best clip so I can paste it into my page.
- If stuck, use ask-cosmos.
```
