"""Load a Play Labeler export and pair every frame with its label.

Usage:
    python scripts/read_labels.py match.labels.json match.mp4

Requires: opencv-python  (pip install opencv-python)
The export keys labels by frame index, so we read frames straight from the source
video — lossless, and no pixel data has to travel through the browser.
"""
import json
import sys


def load_labels(path):
    with open(path) as f:
        data = json.load(f)
    return data


def iter_labeled_frames(labels_json, video_path, include_unlabeled=False):
    """Yield (frame_index, label_str, frame_bgr) for each frame in the video.

    label_str is one of "play", "nonplay", "unlabeled".
    """
    import cv2

    data = load_labels(labels_json)
    frame_labels = data["frame_labels"]          # index -> 1 / 0 / -1
    name = {1: "play", 0: "nonplay", -1: "unlabeled"}

    cap = cv2.VideoCapture(video_path)
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        v = frame_labels[idx] if idx < len(frame_labels) else -1
        if include_unlabeled or v != -1:
            yield idx, name[v], frame
        idx += 1
    cap.release()


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    labels_json, video_path = sys.argv[1], sys.argv[2]

    data = load_labels(labels_json)
    counts = {"play": 0, "nonplay": 0, "unlabeled": 0}
    for v in data["frame_labels"]:
        counts[{1: "play", 0: "nonplay", -1: "unlabeled"}[v]] += 1

    print(f"video      : {data['video']}")
    print(f"fps        : {data['fps']}")
    print(f"frames     : {data['frame_count']}")
    print(f"segments   : {len(data['segments'])}")
    print(f"play       : {counts['play']} frames")
    print(f"nonplay    : {counts['nonplay']} frames")
    print(f"unlabeled  : {counts['unlabeled']} frames")

    # Example: count how many frames we can actually pair with the video.
    try:
        n = sum(1 for _ in iter_labeled_frames(labels_json, video_path))
        print(f"paired     : {n} labeled frames read from {video_path}")
    except ImportError:
        print("(install opencv-python to read frames: pip install opencv-python)")


if __name__ == "__main__":
    main()
