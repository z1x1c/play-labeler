# Play Labeler

A dead-simple, local-only tool for segmenting a video into **in-play** vs **non-play**.
Upload a video, mark where play starts and stops, export per-frame labels ready to feed a
neural network. No install, no server, no upload — it's a single HTML file that runs
entirely in your browser.

![in-play / non-play](https://img.shields.io/badge/label-in--play%20%2F%20non--play-black)

## Use it

Open `index.html` in any modern browser (Chrome/Edge recommended for accurate frame
stepping via `requestVideoFrameCallback`). Or just double-click the file.

1. **Drop a video** (or click *Choose video…*). It stays on your machine.
2. Set the **FPS** to match your source *before* you start (labels are stored in frame space).
3. **Label it.** The fastest way:
   - Press <kbd>Space</kbd> to play.
   - Tap <kbd>→</kbd> the instant a rally **starts** (marks *in play* from here on).
   - Tap <kbd>←</kbd> the instant it **ends** (marks *non-play* from here on).
   - A label fills forward until the next mark, so you only press a key at transitions.
4. **Export.** You get a `.labels.json` (full, NN-ready) and a `.labels.csv` (flat).

## Why transition-marking instead of frame-by-frame

In-play/non-play is a *temporal segmentation* problem. Labeling every frame is thousands
of keypresses per match. Instead you mark only the **boundaries** — where a segment's
label changes — and every frame in between inherits it. You can even do it **live during
playback**, so a whole match takes a few minutes. The export still expands to a clean
per-frame verdict (which is what a frame classifier wants); you just didn't have to type
it out frame by frame.

## Controls

| Key | Action |
|-----|--------|
| <kbd>Space</kbd> | Play / pause |
| <kbd>→</kbd> | Mark **in play** from current frame |
| <kbd>←</kbd> | Mark **non-play** from current frame |
| <kbd>,</kbd> / <kbd>.</kbd> | Step one frame back / forward (hold <kbd>⇧</kbd> = ±10) |
| <kbd>[</kbd> / <kbd>]</kbd> | Jump to previous / next mark |
| click timeline | Seek (drag to scrub) |
| <kbd>⌘Z</kbd> / <kbd>⇧⌘Z</kbd> | Undo / redo |

The timeline shows every labeled segment (black = in play, white = non-play, gray =
unlabeled) plus tick marks at each boundary, so you can navigate what you've already done.

## Export format

`<video>.labels.json`:

```json
{
  "schema": "play-labeler/v1",
  "video": "match.mp4",
  "fps": 30,
  "frame_count": 12345,
  "duration": 411.5,
  "label_map": { "1": "play", "0": "nonplay", "-1": "unlabeled" },
  "segments": [
    { "label": "nonplay", "start_frame": 0,   "end_frame": 119, "start_time": 0.0, "end_time": 4.0 },
    { "label": "play",    "start_frame": 120, "end_frame": 380, "start_time": 4.0, "end_time": 12.7 }
  ],
  "frame_labels": [ -1, -1, 0, 0, 1, 1, ... ]
}
```

- **`frame_labels`** — one entry per frame; index *is* the frame number. `1` = in play,
  `0` = non-play, `-1` = unlabeled. This is the plug-and-play array for a per-frame classifier.
- **`segments`** — the compact form (contiguous runs). Better for sequence models or for
  extracting clips with `ffmpeg`.

Both describe the same labeling. A `.labels.csv` (`frame,time_sec,label`) is exported too.

### Feeding it to a model

The export deliberately does **not** ship pixel data — labels are keyed by frame index, so
you extract frames from the original video in your training pipeline (far more reliable and
lossless than browser canvas dumps). See [`scripts/read_labels.py`](scripts/read_labels.py)
for a ~20-line loader that maps every label to its frame with OpenCV.

## License

MIT — see [LICENSE](LICENSE).
