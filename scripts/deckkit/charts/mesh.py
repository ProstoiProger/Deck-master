"""Mesh-gradient backdrops: four colors blended by soft blobs with a gentle domain warp (the look of mesh-gradient tools).

Rendered once to a JPEG and cached; the scene embeds it as a full-slide Image. Needs numpy and Pillow (the `charts` group).
Returns the file and a `tone`: the lightest (dark themes) or darkest (light themes) color found where text sits, so the
contrast lint can judge text over the picture instead of skipping it.
"""
import hashlib

from ..core import color
from .themed import _cache_dir

SIZE = (1600, 900)
TEXT_ZONE = 0.66   # fraction of the width, from the left, where titles and body text are placed


def _smooth(a, b, x):
    import numpy as np
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def render_mesh(theme, deck=None, key="cover", colors=None, veil=None, seed=None):
    """-> (path, tone). `colors` are four hex colors (default: the theme's `mesh` style key or its series)."""
    import numpy as np
    from PIL import Image as PILImage

    style = theme.style
    colors = [theme.c(x) for x in (colors or style.get("mesh") or theme.series[:4])][:4]
    while len(colors) < 4:
        colors.append(theme.c("primary"))
    veil = style.get("mesh_veil", 0.5) if veil is None else veil
    ident = repr((theme.name, key, colors, veil, theme.c("bg"), seed))
    digest = hashlib.sha1(ident.encode("utf-8")).hexdigest()[:12]
    out = _cache_dir(deck) / f"mesh-{key}-{digest}.jpg"
    meta = out.with_suffix(".tone")
    if out.exists() and meta.exists():
        return str(out), meta.read_text(encoding="ascii").strip()

    rng = np.random.default_rng(int(digest, 16) % (2 ** 32) if seed is None else seed)
    w, h = SIZE
    xs = np.linspace(0, 1, w)[None, :]
    ys = np.linspace(0, 1, h)[:, None]
    f1, f2 = 1.2 + rng.random(), 1.2 + rng.random()
    p1, p2 = rng.random() * 6.28, rng.random() * 6.28
    u = xs + 0.10 * np.sin(2 * np.pi * f1 * ys + p1)
    v = ys + 0.14 * np.sin(2 * np.pi * f2 * xs + p2)
    anchors = [(0.92, 0.08), (0.70, 0.95), (0.40, 0.45), (0.98, 0.62)]
    anchors = [(ax + rng.uniform(-0.06, 0.06), ay + rng.uniform(-0.06, 0.06)) for ax, ay in anchors]
    sigma = 0.30
    acc = np.zeros((h, w, 3))
    tot = np.zeros((h, w, 1))
    for (ax, ay), col in zip(anchors, colors):
        wgt = np.exp(-(((u - ax) ** 2) + ((v - ay) ** 2)) / (2 * sigma ** 2))[..., None]
        acc += wgt * np.array(color.hex_to_rgb(col), dtype=float)
        tot += wgt
    blend = acc / np.maximum(tot, 1e-6)
    base = np.array(color.hex_to_rgb(theme.c("bg")), dtype=float)
    # the veil is strongest under the text zone and relaxes toward the right edge, so the color shows where there is no text
    k = veil + (0.97 - veil) * (1 - _smooth(0.28, 0.95, xs)) * 0.55
    k = np.broadcast_to(np.clip(k, 0, 0.97), (h, w))[..., None]
    img = blend * (1 - k) + base * k
    img += rng.normal(0, 1.1, (h, w, 1))   # a little grain hides banding in the JPEG
    arr = np.clip(img, 0, 255).astype("uint8")
    PILImage.fromarray(arr, "RGB").save(out, quality=90, subsampling=0)

    zone = arr[:, : int(w * TEXT_ZONE)].reshape(-1, 3).astype(float)
    lum = 0.2126 * zone[:, 0] + 0.7152 * zone[:, 1] + 0.0722 * zone[:, 2]
    dark_mode = theme.mode == "dark"
    idx = int(np.argsort(lum)[int(len(lum) * (0.995 if dark_mode else 0.005))])
    tone = color.rgb_to_hex(zone[idx])
    meta.write_text(tone, encoding="ascii")
    return str(out), tone
