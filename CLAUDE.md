# play-labeler

A local, browser-based volleyball labeler (in-play / non-play + single-frame
**serve** events) and the models built from its labels, working toward a webapp
that produces volleyball statistics from video.

**Before doing anything, read @NEXT_STEPS.md** — it holds the current state, the
immediate next actions, the command cheat-sheet, and the data gotchas.

## Orientation for agents
- **In the repo:** only `index.html` (the labeler, schema v2) and the docs
  (`README.md`, `NEXT_STEPS.md`). Keep the repo a near-zero-dependency single-file tool.
- **Local only, NOT in git** (intentional): `our_model/` (play/nonplay classifier),
  `serve_model/` (serve-event detector, built but untrained), `vb_model/` +
  `vendor/` (volleyball_analytics comparison), `outputs/`, `gabriel-labels/`,
  `toko-labels/`. Don't commit these unless asked.
- **Labels** are Play-Labeler JSON; serves are stored by **timestamp**, and some
  clips are labeled at a different fps than the video decodes — always map by time.
- **Runtime:** Apple M2 / MPS; use `python3`.

## Pushing
Remote is `github.com/z1x1c/play-labeler` (`main`). The machine's active `gh`
account (`prime-mgmt`) can't push; push as the owner:
```bash
git push "https://x-access-token:$(gh auth token --user z1x1c)@github.com/z1x1c/play-labeler.git" main
```
Commit/push only when the user asks.
