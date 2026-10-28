"""Read the SERP crawler output and write shots/ and thumbs/ used by the report."""
import glob
import json
from pathlib import Path

from PIL import Image

from data import SERP_DIR

ROOT = Path(__file__).resolve().parent.parent


def load_pairs():
    """(thread id, keyword) -> (placement, screenshot file). Sub-link-only hits are left out."""
    pairs = {}
    for f in sorted(glob.glob(f"{SERP_DIR}/data/b*.data.txt")):
        s = open(f).read()
        j = json.loads(s[s.index("=", s.index("SERP_PROFILES[")) + 1:].rstrip().rstrip(";"))
        for r in j["results"]:
            for h in r["hits"]:
                if h["sub"]:
                    continue
                tid = h["url"].split("/comments/")[1].split("/")[0]
                pairs.setdefault((tid, r["kw"].strip().lower()), (h["placement"], h["file"]))
    return pairs


def red_box(im):
    w, h = im.size
    px = im.convert("RGB").load()
    xs, ys = [], []
    for y in range(0, h, 3):
        for x in range(0, int(w * 0.54), 3):
            r, g, b = px[x, y]
            if r > 190 and g < 80 and b < 80:
                xs.append(x); ys.append(y)
    if len(xs) < 40:
        return None
    xs.sort(); ys.sort()
    k = max(1, len(xs) // 200)
    return xs[k], ys[k], xs[-k - 1], ys[-k - 1]


def crop_16x10(im, box):
    w, h = im.size
    x0, y0, x1, y1 = box
    pad = int(w * 0.03)
    x0, y0, x1, y1 = max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad), min(h, y1 + pad)
    bw, bh = x1 - x0, y1 - y0
    tw = max(bw, int(bh * 1.6)); th = int(tw / 1.6)
    if th < bh:
        th = bh; tw = int(th * 1.6)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    L = min(max(0, cx - tw // 2), max(0, w - tw)); T = min(max(0, cy - th // 2), max(0, h - th))
    return im.crop((L, T, min(w, L + tw), min(h, T + th)))


def save(im, path, width, q):
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path.parent.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(path, "WEBP", quality=q, method=6)


def image_names(file):
    stem = file.replace("/", "__").rsplit(".", 1)[0]
    return f"shots/{stem}.webp", f"thumbs/{stem}.webp"


def build_images(pairs):
    for (tid, kw), (pl, file) in pairs.items():
        shot, thumb = image_names(file)
        if (ROOT / thumb).exists():
            continue
        im = Image.open(Path(SERP_DIR) / file)
        save(im, ROOT / shot, 2400, 84)
        box = red_box(im)
        t = crop_16x10(im, box) if box else im.crop((0, 0, int(im.width * .54), int(im.width * .54 / 1.6)))
        save(t, ROOT / thumb, 720, 80)
