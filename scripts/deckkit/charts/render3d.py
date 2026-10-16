"""Shaded 3D hero objects (glossy orbs, a ring, a rounded cube, a slab stack) ray-marched with numpy in the theme's colors.

Rendered once to a transparent PNG and cached; the scene embeds it as an Image. Needs numpy and Pillow (the `charts` group).
The object is decoration: it never carries text, so the contrast lint skips it (an Image without a tone).
"""
import hashlib
import math

from ..core import color
from .themed import _cache_dir

KINDS = ("orbs", "ring", "cube", "stack")
FOV = 0.37          # tangent of the half field of view
CAM_Z = 5.2
CAM_Y = 1.25                      # the camera sits above the objects and looks slightly down
PITCH = math.atan2(CAM_Y, CAM_Z)
FLOOR_Y = -1.5


def _rot(ax_deg, ay_deg, az_deg):
    import numpy as np
    ax, ay, az = (math.radians(v) for v in (ax_deg, ay_deg, az_deg))
    rx = np.array([[1, 0, 0], [0, math.cos(ax), -math.sin(ax)], [0, math.sin(ax), math.cos(ax)]])
    ry = np.array([[math.cos(ay), 0, math.sin(ay)], [0, 1, 0], [-math.sin(ay), 0, math.cos(ay)]])
    rz = np.array([[math.cos(az), -math.sin(az), 0], [math.sin(az), math.cos(az), 0], [0, 0, 1]])
    return rz @ ry @ rx


def _scene(kind, cols):
    """Objects: (shape, center, params, rotation matrix, rgb 0..1). Colors are primary, secondary, accent."""
    import numpy as np
    p, s, a = (np.array(color.hex_to_rgb(x)) / 255.0 for x in cols)
    I = np.eye(3)
    if kind == "ring":
        return [("torus", (0.0, 0.0, 0.0), (1.05, 0.38), _rot(62, 0, 18), p), ("sphere", (0.0, 0.0, 0.0), (0.5,), I, a),
                ("sphere", (1.35, -0.75, -0.3), (0.22,), I, s)]
    if kind == "cube":
        return [("box", (-0.2, 0.0, 0.0), (0.8, 0.8, 0.8, 0.2), _rot(24, 35, 0), p), ("sphere", (1.15, -0.75, -0.5), (0.55,), I, s),
                ("box", (0.75, 0.95, -0.4), (0.3, 0.3, 0.3, 0.1), _rot(20, 50, 10), a)]
    if kind == "stack":
        return [("box", (0.0, -0.75, 0.0), (1.25, 0.17, 1.25, 0.1), _rot(0, 0, 0), p), ("box", (0.0, -0.1, 0.0), (1.1, 0.17, 1.1, 0.1), _rot(0, 14, 0), s),
                ("box", (0.0, 0.55, 0.0), (0.95, 0.17, 0.95, 0.1), _rot(0, 28, 0), a), ("sphere", (0.0, 1.3, 0.0), (0.32,), I, p)]
    return [("sphere", (-0.3, 0.05, 0.2), (0.95,), I, p), ("sphere", (0.95, -0.55, -0.35), (0.6,), I, s),
            ("sphere", (0.55, 0.95, -0.5), (0.38,), I, a), ("sphere", (-1.25, -0.95, -0.45), (0.24,), I, s)]


def _sdf(objs, pts):
    """Distance to the nearest object and its index, for points of shape (n, 3)."""
    import numpy as np
    best = np.full(len(pts), 1e9)
    ident = np.zeros(len(pts), dtype=int)
    for i, (shape, c, prm, rot, _rgb) in enumerate(objs):
        q = (pts - np.array(c)) @ rot
        if shape == "sphere":
            d = np.linalg.norm(q, axis=1) - prm[0]
        elif shape == "torus":
            d = np.hypot(np.hypot(q[:, 0], q[:, 2]) - prm[0], q[:, 1]) - prm[1]
        else:
            half = np.array(prm[:3])
            e = np.abs(q) - half + prm[3]
            d = np.linalg.norm(np.maximum(e, 0), axis=1) + np.minimum(e.max(axis=1), 0) - prm[3]
        better = d < best
        best = np.where(better, d, best)
        ident = np.where(better, i, ident)
    return best, ident


def _march(objs, ro, rd, max_steps=96):
    import numpy as np
    n = len(rd)
    t = np.zeros(n)
    alive = np.arange(n)
    hit = np.zeros(n, dtype=bool)
    for _ in range(max_steps):
        if not len(alive):
            break
        d, _i = _sdf(objs, ro + rd[alive] * t[alive, None])
        done_hit = d < 0.0015
        hit[alive[done_hit]] = True
        t[alive] += d
        keep = ~done_hit & (t[alive] < 12.0)
        alive = alive[keep]
    return t, hit


def render_hero(theme, kind="orbs", deck=None, size=640, ss=1.5):
    """-> path of a transparent PNG (size x size) showing the object `kind` shaded in the theme's colors."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    if kind not in KINDS:
        raise ValueError(f"unknown hero object {kind!r}; choose from {KINDS}")
    cols = [theme.c("primary"), theme.c("secondary"), theme.c("accent")]
    key = hashlib.sha1(repr((theme.name, kind, cols, size, theme.mode, theme.c("bg"))).encode("utf-8")).hexdigest()[:12]
    out = _cache_dir(deck) / f"hero3d-{kind}-{key}.png"
    if out.exists():
        return str(out)

    objs = _scene(kind, cols)
    n = int(size * ss)
    xs = (np.arange(n) + 0.5) / n * 2 - 1
    u, v = np.meshgrid(xs, -xs)
    cam = np.stack([u * FOV, v * FOV, np.ones_like(u)], axis=-1).reshape(-1, 3)
    cs, sn = math.cos(PITCH), math.sin(PITCH)
    rd = np.stack([cam[:, 0], cam[:, 1] * cs - cam[:, 2] * sn, cam[:, 1] * sn + cam[:, 2] * cs], axis=-1)   # pitch the view down
    rd /= np.linalg.norm(rd, axis=1, keepdims=True)
    ro = np.array([0.0, CAM_Y, -CAM_Z])
    t, hit = _march(objs, ro, rd)
    idx = np.where(hit)[0]
    pts = ro + rd[idx] * t[idx, None]

    eps = 0.002
    nrm = np.zeros_like(pts)
    for ax in range(3):
        off = np.zeros(3)
        off[ax] = eps
        nrm[:, ax] = _sdf(objs, pts + off)[0] - _sdf(objs, pts - off)[0]
    nrm /= np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-9
    _d, ident = _sdf(objs, pts)

    base = np.array([objs[i][4] for i in ident])
    light = np.array([-0.5, 0.75, -0.55])
    light /= np.linalg.norm(light)
    diff = np.clip(nrm @ light, 0, 1)
    view = -rd[idx]
    half = light + view
    half /= np.linalg.norm(half, axis=1, keepdims=True) + 1e-9
    spec = np.clip((nrm * half).sum(axis=1), 0, 1) ** 60
    fres = (1 - np.clip((nrm * view).sum(axis=1), 0, 1)) ** 3
    ao = np.ones(len(idx))
    for k in range(1, 5):
        dist = k * 0.1
        ao -= (dist - np.clip(_sdf(objs, pts + nrm * dist)[0], 0, dist)) * (0.5 ** k) * 2.2
    ao = np.clip(ao, 0.25, 1)
    refl_y = (rd[idx] - 2 * (rd[idx] * nrm).sum(axis=1, keepdims=True) * nrm)[:, 1]
    sky = np.clip(0.5 + 0.5 * refl_y, 0, 1)[:, None]
    rim = np.array(color.hex_to_rgb(theme.c("accent"))) / 255.0
    ambient = (0.30 + 0.20 * (0.5 + 0.5 * nrm[:, 1:2])) * base
    rgb = ambient * ao[:, None] + base * (0.85 * diff)[:, None] * ao[:, None] ** 0.5
    rgb += (0.55 * spec)[:, None] + rim * (0.55 * fres)[:, None] + sky * (0.10 + 0.25 * fres)[:, None] * base
    rgb = np.clip(rgb, 0, 1)

    img = np.zeros((n * n, 4))
    img[idx, :3] = rgb
    img[idx, 3] = 1.0
    layer = Image.fromarray((img.reshape(n, n, 4) * 255).astype("uint8"), "RGBA").resize((size, size), Image.LANCZOS)

    # a soft contact shadow under the object, then the object on top
    shadow = Image.new("L", (size, size), 0)
    dr = ImageDraw.Draw(shadow)

    def screen(x, y, z):
        rel = (x - 0.0, y - CAM_Y, z + CAM_Z)
        yc = rel[1] * cs + rel[2] * sn
        zc = -rel[1] * sn + rel[2] * cs
        return (rel[0] / zc / FOV * 0.5 + 0.5) * size, (0.5 - yc / zc / FOV * 0.5) * size

    xs_ = [o[1][0] for o in objs]
    zs_ = [o[1][2] for o in objs]
    cx, cy = screen(sum(xs_) / len(xs_), FLOOR_Y, sum(zs_) / len(zs_))
    spread = (max(xs_) - min(xs_) + 2.0) / 2.0
    rx, ry = size * 0.30 * spread / 1.6, size * 0.055
    dr.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=int(255 * (0.55 if theme.mode == "dark" else 0.30)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.035))
    base_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    base_img.putalpha(shadow)
    base_img.alpha_composite(layer)
    base_img.save(out)
    return str(out)
