# Next actions — read this first when returning

_Last updated 2026-08-12._

## TL;DR
The **goal** is a webapp that produces volleyball stats from video (Balltime-style).
Right now: the **labeler** captures play/nonplay + serve labels; a **play/nonplay
model** works; a **serve-detection model** is built but **untrained**. The single
blocking step is **labeling serves**, then training the serve model.

## Where things stand
- **Labeler** (`index.html`) — schema **v2**. Marks play/nonplay segments *and*
  single-frame **serve events** (press `S`), serves stored by **timestamp**
  (fps-safe). ✅ Pushed to `main` (commit 39831c5). This is the only thing in the repo.
- **Play/nonplay model** (`our_model/`, local only) — MobileNet embedding + motion
  + MLP. Trained on GVC-gym (PANAMBA ×3) + Forza (toko). Honest accuracy ~**70–77%
  same-venue**, ~**53% on a brand-new gym**. Artifacts: `our_model/models/clf.joblib`.
- **Their-model comparison** (`vb_model/`, `outputs/`, local) — volleyball_analytics
  VideoMAE run on `sample-video.mp4`. Result: it badly under-detects play here
  (domain shift). See `outputs/README.md`.
- **Serve model** (`serve_model/`, local) — full extract→train→infer pipeline,
  **built + tested but NOT trained** (no serve labels exist yet).

## Immediate next steps (in order)
1. **Label serves.** Open `index.html`, load a match, press `S` at each serve-contact
   frame, Export. Do **whole videos** (one tap per rally, ~2–3 serves/min) across
   **≥2 venues** — start with the ones already labeled (toko + gabriel) so you get
   two gyms for near-free. Put the `.labels.json` next to its video in
   `gabriel-labels/` or `toko-labels/`.
2. **Train + check the serve model** (commands below). Share the leave-one-video-out
   P/R/F1. If recall is low → widen tolerance / add data; if precision is low → raise
   threshold or min-gap (all in `serve_model/serve_common.py`).
3. **(Optional) Ground-truth `sample-video.mp4`.** It's the GVC-LITE match, currently
   **unlabeled**, so the 38%-vs-9.5% play/nonplay comparison in `outputs/` can't be
   scored. Labeling even 30–60 s would give real accuracy numbers for both models.

## Commands cheat-sheet (Apple M2 / MPS, use `python3`)
```bash
# Serve model (after exporting serve labels)
python3 serve_model/extract_serve_features.py
python3 serve_model/train_serve.py
python3 serve_model/infer_serve.py --video sample-video.mp4 --render
python3 serve_model/test_serve_pipeline.py          # pipeline self-test

# Play/nonplay model (already trained; re-run if data changes)
python3 our_model/extract_features.py
python3 our_model/train.py
python3 our_model/infer_our_model.py                # -> outputs/output1_our_model.mp4

# Their model (VideoMAE) on a clip
python3 vb_model/infer_vb.py --video sample-video.mp4
```

## Gotchas to remember
- **Truncated training videos:** the 3 gabriel/PANAMBA mp4s only decode ~1/3 of their
  length (corrupt mid-stream). To get more play/nonplay data, re-obtain them intact.
- **fps mismatch:** the toko clip is **59.94 fps but labeled at 30** — always map
  labels by **timestamp**, never bare frame index (both models already do this).
- **Venue shift is real:** models trained on one gym drop hard on a new one. More
  venues > more minutes of one venue.
- **Model dirs are local, not in git** (`our_model/`, `vb_model/`, `serve_model/`,
  `outputs/`, `vendor/`). Only `index.html` is in the repo, by choice.

## Longer roadmap (toward the stats webapp)
1. **Rally layer (near done):** play/nonplay + serve → rally count, durations,
   serve count, work:rest, auto-highlights. Serve model is the last piece here.
2. **Touch/stats layer (the moat):** per-touch actions (pass/set/spike/block/dig) +
   player & ball tracking for per-player stats. Reuse/fine-tune the volleyball_analytics
   YOLO weights (already downloaded in `vendor/…/weights/`) rather than labeling from
   scratch. This needs *event/box* labels, not segment labels.
3. **Score:** scoreboard OCR is likely easier than inferring it.

## Repo / push notes
- Remote: `github.com/z1x1c/play-labeler`, branch `main`.
- The machine's active `gh` account is `prime-mgmt` (no push access). Push as the
  owner with:
  ```bash
  git push "https://x-access-token:$(gh auth token --user z1x1c)@github.com/z1x1c/play-labeler.git" main
  ```
