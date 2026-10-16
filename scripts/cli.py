"""deck-master command line: scaffold, lint, build, preview and inspect presentations.

    python scripts/cli.py <command> [options]        commands: env themes layouts new lint build preview serve
                                                       inspire entities notes timing trace catalog
Exit codes: 0 ok, 1 blocking findings or unmet requirements, 2 bad input or usage.
"""
import argparse
import json
import platform
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def die(msg, code=2):
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load(args):
    from deckkit.core.spec import SpecError, load_deck
    from deckkit.core.theme import ThemeError, load_theme
    try:
        deck = load_deck(args.deck)
    except FileNotFoundError:
        die(f"deck not found: {args.deck}")
    except SpecError as e:
        die(f"invalid deck {args.deck}: {e}")
    name = getattr(args, "theme", None) or deck.meta.get("theme")
    if not name:
        from deckkit.core.timing import preset_for
        name = preset_for(deck)[1]["theme"]
    try:
        theme = load_theme(name)
    except ThemeError as e:
        die(str(e))
    return deck, theme


def scenes_for(deck, theme, cache=None):
    from deckkit.core.layout import build_scenes
    if cache:
        deck.meta["_cache"] = str(cache)
    return build_scenes(deck, theme)


def print_findings(findings):
    for f in findings:
        print(f)


# ---- commands ---------------------------------------------------------------

def cmd_env(args):
    import importlib
    from deckkit import __version__
    from deckkit.core import paths
    pk = {}
    for label, mod in [("python-pptx", "pptx"), ("reportlab", "reportlab"), ("matplotlib", "matplotlib"), ("pillow", "PIL"),
                       ("pymupdf", "pymupdf"), ("pyyaml", "yaml"), ("fonttools", "fontTools")]:
        try:
            m = importlib.import_module(mod)
            pk[label] = getattr(m, "__version__", None) or getattr(m, "Version", None) or getattr(m, "VersionBind", "installed")
        except Exception:
            pk[label] = None
    fonts = sorted(p.name for p in paths.fonts_dir().glob("*.ttf"))
    info = {"deckkit": __version__, "python": platform.python_version(), "platform": platform.platform(),
            "skill_root": str(paths.ROOT), "packages": pk, "fonts": fonts}
    lines = [f"deckkit {info['deckkit']}  python {info['python']}  {info['platform']}", f"skill root: {info['skill_root']}"]
    lines += [f"  {k:12} {v if v else 'MISSING'}" for k, v in pk.items()]
    lines.append(f"fonts: {', '.join(fonts) if fonts else 'none bundled'}")
    print("\n".join(lines))
    if args.json:
        Path(args.json).write_text(json.dumps(info, indent=2, default=str), encoding="utf-8")


def cmd_themes(args):
    from deckkit.core.theme import contrast_table, load_theme, theme_names
    rows = []
    for n in theme_names():
        t = load_theme(n)
        if args.scope and args.scope not in t.scopes:
            continue
        rows.append({"name": n, "mode": t.mode, "scopes": t.scopes, "colors": t.colors, "style": t.style,
                     "description": t.description, "contrast": dict(contrast_table(t))})
    if not rows:
        die(f"no theme with scope {args.scope!r}")
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    for r in rows:
        print(f"{r['name']:18} {r['mode']:5} primary {r['colors']['primary']}  accent {r['colors']['accent']}  "
              f"text/bg {r['contrast']['text on bg']}:1  [{', '.join(r['scopes'])}]  {r['description']}")


def cmd_layouts(args):
    from deckkit.core import layout
    layout.ensure_loaded()
    rows = [{"name": s.name, "family": s.family, "max_words": s.max_words, "purpose": s.purpose, "accepts": s.accepts}
            for s in sorted(layout.LAYOUTS.values(), key=lambda s: (s.family, s.name))]
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    for r in rows:
        print(f"{r['name']:14} {r['family']:8} <= {r['max_words']:3} words  {r['purpose']}")


def cmd_new(args):
    import time
    from deckkit.core import paths, timing
    events = timing.load_events()
    if args.list:
        for name, e in events.items():
            print(f"{name:18} {e.get('scope', ''):12} <= {e['max_slides']:2} slides  {e['minutes']:3} min  theme {e['theme']}")
        return
    if not args.event or not args.out:
        die("--event and --out are required (or use --list)")
    if args.event not in events:
        die(f"unknown event {args.event!r}; choose from {sorted(events)}")
    src = paths.templates_dir() / f"deck-{args.event}.md"
    if not src.exists():
        die(f"no template for event {args.event}: {src}")
    out = Path(args.out)
    if out.exists() and not args.force:
        die(f"{out} exists; pass --force to overwrite (existing decks are never replaced silently)", 1)
    p = events[args.event]
    text = src.read_text(encoding="utf-8")
    title = args.title or "Project name: one-line value proposition"
    for k, v in {"theme": args.theme or p["theme"], "title": title, "title_yaml": title.replace("\\", "\\\\").replace('"', '\\"'),
                 "minutes": p["minutes"], "date": time.strftime("%Y-%m-%d")}.items():
        text = text.replace("{{" + k + "}}", str(v))
    from deckkit.core.theme import load_theme
    if "game" in load_theme(args.theme or p["theme"]).scopes and "\ngame: true" not in text:
        text = text.replace("\ntheme:", "\ngame: true\ntheme:", 1)  # records that the user asked for a game look
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {out} ({args.event}, theme {args.theme or p['theme']}); edit it, then: python scripts/cli.py lint {out}")


def cmd_lint(args):
    from deckkit import lint
    deck, theme = load(args)
    findings = lint.run_all(deck, scenes_for(deck, theme), theme)
    blocking = lint.blocking(findings)
    if args.json:
        print(json.dumps({"deck": str(args.deck), "theme": theme.name, "findings": findings, "blocking": len(blocking)},
                         indent=2, ensure_ascii=False))
    else:
        print_findings(findings)
        print(f"{len(findings)} finding(s), {len(blocking)} blocking (Critical/High); {len(deck.slides)} slides")
    if blocking or (args.strict and findings):
        if not args.json:
            print("INVALID")
        raise SystemExit(1)


def cmd_build(args):
    from deckkit import lint
    from deckkit.core.runlog import log_run
    deck, theme = load(args)
    out = Path(args.out)
    scenes = scenes_for(deck, theme, out / ".cache")
    findings = lint.run_all(deck, scenes, theme)
    print_findings(findings)
    blocking = lint.blocking(findings)
    if blocking and not args.force:
        print(f"INVALID: {len(blocking)} blocking finding(s); fix them or pass --force to build anyway")
        raise SystemExit(1)
    none = not (args.pptx or args.pdf or args.html)          # no format named: build all three
    want_pptx, want_pdf, want_html = args.pptx or none, args.pdf or none, args.html or none
    stem = Path(args.deck).stem + (f"-{args.theme}" if args.theme else "")
    made = []
    if want_pptx:
        try:
            from deckkit.backends.pptx_backend import build_pptx
        except ImportError as e:
            die(f"cannot write pptx: {e}; install scripts/requirements/pptx.txt")
        made.append(str(build_pptx(scenes, theme, deck, out / f"{stem}.pptx")))
    if want_pdf:
        try:
            from deckkit.backends.pdf_backend import build_pdf
            made.append(str(build_pdf(scenes, theme, deck, out / f"{stem}.pdf")))
        except ImportError as e:
            die(f"cannot write pdf: {e}; install scripts/requirements/pdf.txt")
    if want_html:
        try:
            from deckkit.backends.html_backend import build_html
            made.append(str(build_html(scenes, theme, deck, out / f"{stem}.html")))
        except ImportError as e:
            die(f"cannot write html: {e}; install scripts/requirements/core.txt")
    log_run(out / "log.jsonl", deck=str(args.deck), theme=theme.name, slides=len(deck.slides), findings=len(findings),
            blocking=len(blocking), forced=bool(blocking and args.force), outputs=made)
    for m in made:
        print(f"wrote {m}")
    print(f"{len(deck.slides)} slides, theme {theme.name}, {len(findings)} finding(s)")


def cmd_serve(args):
    """Serve a built web presentation on localhost (the presenter window then syncs reliably) and open it in the browser."""
    import functools
    import http.server
    import threading
    import webbrowser
    target = Path(args.path).resolve()
    if not target.exists():
        die(f"{target} not found; build first: python scripts/cli.py build <deck.md> --html")
    root, name = (target.parent, target.name) if target.is_file() else (target, "")
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    handler.log_message = lambda *a, **k: None
    try:
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as e:
        die(f"cannot listen on 127.0.0.1:{args.port}: {e}; pass --port <other>")
    url = f"http://127.0.0.1:{srv.server_address[1]}/{name}"
    print(f"serving {root} at {url} (Ctrl+C to stop; P opens the presenter window)")
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("stopped")


def cmd_preview(args):
    from deckkit import lint
    from deckkit.backends.pdf_backend import build_pdf
    try:
        import pymupdf
    except ImportError:
        die("preview needs pymupdf; install scripts/requirements/preview.txt")
    deck, theme = load(args)
    out = Path(args.out)
    scenes = scenes_for(deck, theme, out / ".cache")
    for f in lint.blocking(lint.run_all(deck, scenes, theme)):
        print(f"WARNING {f}")  # a failed layout renders as an incomplete slide; do not trust the picture
    pdf = build_pdf(scenes, theme, deck, out / ".cache" / "preview.pdf")
    doc = pymupdf.open(str(pdf))
    paths_ = []
    for i, page in enumerate(doc, 1):
        p = out / f"slide-{i:02d}.png"
        page.get_pixmap(dpi=args.dpi).save(str(p))
        paths_.append(p)
    if args.sheet:
        from PIL import Image
        ims = [Image.open(p) for p in paths_]
        cols = 3
        tw = 640
        th = int(tw * ims[0].height / ims[0].width)
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 12) + 12), "#888888")
        for k, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), (12 + (k % cols) * (tw + 12), 12 + (k // cols) * (th + 12)))
        sp = out / "sheet.png"
        sheet.save(sp)
        print(f"wrote {sp}")
    for p in paths_:
        print(f"wrote {p}")


def cmd_inspire(args):
    from PIL import Image
    from deckkit.core import color
    im = Image.open(args.from_image).convert("RGB")
    im.thumbnail((200, 200))
    q = im.quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: 3 * args.colors]
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(n for n, _ in counts)
    print("| Share | Hex | vs white | vs black | Best text |")
    print("|---|---|---|---|---|")
    for n, idx in counts:
        h = color.rgb_to_hex(pal[3 * idx:3 * idx + 3])
        cw, cb = color.contrast(h, "#FFFFFF"), color.contrast(h, "#000000")
        print(f"| {100 * n / total:.0f}% | {h} | {cw:.2f} | {cb:.2f} | {'white' if cw >= cb else 'black'} |")
    print("\nObserved by measurement from the image; treat as palette inspiration, not an exact brand color.")


def cmd_notes(args):
    from deckkit.core.notes import speaker_script
    deck, _ = load(args)
    text = speaker_script(deck)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {args.out}")
    else:
        print(text)


def cmd_timing(args):
    from deckkit.core import timing
    deck, _ = load(args)
    print(timing.format_plan(deck))


def cmd_trace(args):
    from deckkit.core import trace
    deck, _ = load(args)
    brief = Path(args.brief).read_text(encoding="utf-8") if args.brief else None
    text, unmet = trace.table(deck, brief)
    print(text)
    if unmet:
        print(f"\nNOT MET: {', '.join(unmet)}")
        raise SystemExit(1)


def cmd_entities(args):
    from deckkit.core import entities
    if args.action == "fetch":
        try:
            written, skipped, failed, unavailable = entities.fetch(args.names or None, tuple(args.kinds), force=args.force)
        except ValueError as e:
            die(str(e))
        print(f"downloaded {len(written)}, kept {len(skipped)} existing, failed {len(failed)}, not offered {len(unavailable)}; "
              f"folder {entities.entities_dir()}")
        for f in failed:
            print(f"  FAILED {f}")
        for f in unavailable:
            print(f"  note {f}")
        print("Personal, non-commercial use only; files are git-ignored and must not be redistributed (references/design/entities.md).")
        if failed:
            raise SystemExit(1)
        return
    rows = entities.status()
    if args.json:
        print(json.dumps([{"name": n, "label": lb, "role": r, "have": have} for n, lb, r, have in rows], indent=2, ensure_ascii=False))
        return
    print(f"{'name':11} {'face':5} {'head':5} {'body':5} suggested role   (folder {entities.entities_dir()})")
    for n, lb, r, have in rows:
        print(f"{n:11} {'yes' if have['face'] else '-':5} {'yes' if have['head'] else '-':5} {'yes' if have['body'] else '-':5} {r}")


def cmd_catalog(args):
    import subprocess
    cmd = [sys.executable, str(Path(__file__).resolve().parent / "build_catalog.py")] + (["--check"] if args.check else [])
    raise SystemExit(subprocess.call(cmd))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="deck-master")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def deck_cmd(name, fn, help_, theme=True):
        p = sub.add_parser(name, help=help_)
        p.add_argument("deck", help="deck outline (.md)")
        if theme:
            p.add_argument("--theme", help="override the theme in the front matter")
        p.set_defaults(fn=fn)
        return p

    p = sub.add_parser("env", help="show environment and bundled fonts")
    p.add_argument("--json", help="also write the environment card to this JSON file")
    p.set_defaults(fn=cmd_env)

    p = sub.add_parser("themes", help="list themes")
    p.add_argument("--json", action="store_true")
    p.add_argument("--scope", help="only themes for this scope: tech, science, business, finance, education, portfolio, pitch, report, game ...")
    p.set_defaults(fn=cmd_themes)

    p = sub.add_parser("layouts", help="list layouts")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_layouts)

    p = sub.add_parser("new", help="scaffold a deck outline from an event template")
    p.add_argument("--event", help="event preset; `new --list` shows all (default theme is formal; game themes only for `gamified`)")
    p.add_argument("--list", action="store_true", help="list events with scope, slide cap, minutes and default theme")
    p.add_argument("--theme")
    p.add_argument("--title")
    p.add_argument("--out")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_new)

    p = deck_cmd("lint", cmd_lint, "check a deck: overflow, contrast, fonts, density, numbers, notes, timing, rubric")
    p.add_argument("--json", action="store_true")
    p.add_argument("--strict", action="store_true", help="fail on any finding; by default only Critical and High fail")

    p = deck_cmd("build", cmd_build, "lint, then write .pptx, .pdf and/or .html (all three when no format is named)")
    p.add_argument("--out", default="build")
    p.add_argument("--pptx", action="store_true")
    p.add_argument("--pdf", action="store_true")
    p.add_argument("--html", action="store_true", help="a self-contained web presentation (one .html file)")
    p.add_argument("--force", action="store_true", help="build even with blocking findings")

    p = deck_cmd("preview", cmd_preview, "render PNG thumbnails (and a contact sheet) from the PDF backend")
    p.add_argument("--out", default="build/preview")
    p.add_argument("--dpi", type=int, default=80)
    p.add_argument("--sheet", action="store_true")

    p = sub.add_parser("serve", help="serve a built .html presentation (or a folder) on localhost and open it")
    p.add_argument("path", help="the .html file or its folder")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--no-open", action="store_true", help="do not open the browser")
    p.set_defaults(fn=cmd_serve)

    p = sub.add_parser("inspire", help="measure a palette from a reference screenshot")
    p.add_argument("--from-image", required=True)
    p.add_argument("--colors", type=int, default=8)
    p.set_defaults(fn=cmd_inspire)

    p = deck_cmd("notes", cmd_notes, "print or write the speaker script", theme=False)
    p.add_argument("--out")

    deck_cmd("timing", cmd_timing, "per-slide time plan against the event budget", theme=False)

    p = deck_cmd("trace", cmd_trace, "requirement to slide traceability table", theme=False)
    p.add_argument("--brief", help="brief file with lines like `R1: requirement text`")

    p = sub.add_parser("entities", help="list or download character images (Steve, Creeper...) for the game themes")
    p.add_argument("action", choices=["list", "fetch"])
    p.add_argument("--names", nargs="*", help="entities to fetch (default: all)")
    p.add_argument("--kinds", nargs="*", default=["face", "head", "body"], choices=["face", "head", "body"])
    p.add_argument("--force", action="store_true", help="re-download existing files")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_entities)

    p = sub.add_parser("catalog", help="rebuild or check references/design/catalog.md")
    p.add_argument("--check", action="store_true")
    p.set_defaults(fn=cmd_catalog)

    args = ap.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
