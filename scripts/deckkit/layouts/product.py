"""Product, UX and delivery layouts: persona, journey map, how-might-we, kanban board, checklist, links."""
from ..core import color, textfit
from ..core.canvas import CONTENT_BOTTOM, CONTENT_TOP, MARGIN
from ..core.layout import layout
from ..core.scene import W
from ._util import cells, flow, initials, number

STATUS = {"done": "success", "shipped": "success", "ready": "success", "yes": "success", "ok": "success",
          "doing": "warning", "wip": "warning", "in progress": "warning", "partial": "warning",
          "todo": "muted", "planned": "muted", "open": "muted", "no": "muted",
          "blocked": "danger", "failed": "danger", "risk": "danger"}


@layout("persona", "product", "User persona: a name and role, a few facts, goals, frustrations and needs, and one quote.", 90,
        accepts="props: name, role, facts (`28 | Almaty | student`), quote; groups: `## Goals`, `## Frustrations`, `## Needs` with up to three bullets each",
        example="# Aigerim studies at night and loses her streak\nlayout: persona\nname: Aigerim, 20\nrole: Second-year student\nfacts: Almaty | Works part-time | Phone first\n"
                "quote: I only have the bus ride to study.\n## Goals\n- Pass the exams\n- Keep a daily habit\n## Frustrations\n- Long lessons\n- Lost progress offline\n## Needs\n- Five-minute sessions\n- Works without internet")
def persona(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    lw, gap = 3.6, 0.3
    top, ch = y + 0.1, h - 0.1
    qh = 0.95 if s.prop("quote") else 0
    c.box(x, top, lw, ch - (qh + 0.25 if qh else 0), fill="surface")
    c.badge(x + 0.85, top + 0.85, 0.5, initials(s.prop("name")), "primary", 24)
    c.fit_text(x + 1.5, top + 0.4, lw - 1.7, 0.6, s.prop("name"), 20, 13, "text", "heading", True, valign="middle")
    c.fit_text(x + 1.5, top + 1.0, lw - 1.7, 0.5, s.prop("role"), 14, 11, "muted", valign="top")
    c.rect(x + 0.3, top + 1.6, lw - 0.6, 0.015, color.mix(c.t.c("surface"), c.t.c("text"), 0.25))
    facts = [f.strip() for f in s.prop("facts").split("|") if f.strip()]
    fy = top + 1.8
    for f in facts[:4]:
        c.rect(x + 0.32, fy + 0.15, 0.1, 0.1, "accent", kind="round", radius=0.02)
        c.fit_text(x + 0.55, fy, lw - 0.8, 0.4, f, 15, 11, "text", valign="middle")
        fy += 0.42
    groups = [g for g in s.groups if g[1]][:3] or [("Goals", s.items[:3])]
    n = len(groups)
    gx = x + lw + gap
    gw = (w - lw - gap - 0.25 * (n - 1)) / n
    for i, (head, items) in enumerate(groups):
        cx = gx + i * (gw + 0.25)
        tone = ["success", "danger", "info"][i % 3]
        c.box(cx, top, gw, ch - (qh + 0.25 if qh else 0), fill="surface")
        c.rect(cx, top, gw, 0.07, tone)
        c.fit_text(cx + 0.25, top + 0.2, gw - 0.5, 0.45, head.upper(), 13, 11, "muted", "mono", True, valign="middle")
        flow(c, items[:3], cx + 0.25, top + 0.8, gw - 0.5, ch - (qh + 0.25 if qh else 0) - 1.0, max_size=18, min_size=12, gap=0.16, marker_col=tone)
    if qh:
        qy = top + ch - qh
        c.rect(x, qy, w, qh, "accent")
        c.text(x + 0.25, qy - 0.1, 0.8, qh, "“", 54, c.t.on("accent"), "heading", True, "left", "middle", 1.0, chrome=True)
        c.fit_text(x + 1.0, qy + 0.05, w - 1.3, qh - 0.1, s.prop("quote"), 20, 12, c.t.on("accent"), "body", True, valign="middle")


@layout("journey", "product", "Journey map: stages left to right, what the user does, how they feel as a curve, and the opportunity at each stage.", 80,
        accepts="items: `Stage | what the user does | feeling 1-5 | opportunity` (three to six); 1 is frustrated, 5 is delighted",
        example="# The journey breaks at the first lesson\nlayout: journey\n- Discover | Sees a friend's streak | 4 | Share cards\n- Sign up | Needs an email and a password | 2 | One-tap sign-in\n"
                "- First lesson | Ten minutes, no hint | 1 | Add a guided start\n- Habit | Daily reminder | 4 | Streak freeze\n- Refer | Invites a friend | 5 | Reward both")
def journey(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 4)[:4] for i in s.items[:6]]
    n = max(len(rows), 1)
    gut = 1.25
    cw = (w - gut) / n
    top = y + 0.1
    sh, dh, vh, oh = 0.5, 1.0, 1.55, h - 0.1 - 0.5 - 1.0 - 1.55 - 0.3
    labels = [("STAGE", top, sh), ("DOES", top + sh + 0.1, dh), ("FEELS", top + sh + dh + 0.2, vh), ("IDEA", top + sh + dh + vh + 0.3, oh)]
    for text, ly, lh in labels:
        c.text(x, ly, gut - 0.1, lh, text, 11, "muted", "mono", True, valign="middle", chrome=True)
    pts = []
    base = top + sh + dh + 0.2
    for k, (stage, does, feel, idea) in enumerate(rows):
        cx = x + gut + k * cw
        c.rect(cx + 0.04, top, cw - 0.08, sh, "primary")
        c.fit_text(cx + 0.12, top, cw - 0.24, sh, stage, 16, 11, c.t.on("primary"), "body", True, "center", "middle")
        c.box(cx + 0.04, top + sh + 0.1, cw - 0.08, dh, fill="surface", shadow=False, radius=0.06)
        c.fit_text(cx + 0.14, top + sh + 0.12, cw - 0.28, dh - 0.04, does, 14, 11, "text", valign="middle")
        c.rect(cx + 0.04, base, cw - 0.08, vh, "surface", alpha=0.6)
        score = max(1.0, min(5.0, number(feel) or 3.0))
        pts.append((cx + cw / 2, base + vh - 0.22 - (score - 1) / 4 * (vh - 0.44), score))
        c.box(cx + 0.04, top + sh + dh + vh + 0.3, cw - 0.08, oh, fill="surface", shadow=False, radius=0.06)
        c.fit_text(cx + 0.14, top + sh + dh + vh + 0.32, cw - 0.28, oh - 0.04, idea, 14, 11, "accent", "body", True, valign="middle")
    c.line(x + gut, base + vh / 2, x + w, base + vh / 2, color.mix(c.t.c("bg"), c.t.c("text"), 0.25), 0.75, dash=True)
    for (ax, ay, _), (bx, by, _) in zip(pts, pts[1:]):
        c.line(ax, ay, bx, by, c.t.c("accent"), 3.0)
    for px, py, score in pts:
        tone = "success" if score >= 4 else "danger" if score <= 2 else "warning"
        c.rect(px - 0.13, py - 0.13, 0.26, 0.26, tone, kind="ellipse")
        c.rect(px - 0.13, py - 0.13, 0.26, 0.26, None, c.t.c("bg"), 2.0, "ellipse")


@layout("hmw", "product", "The challenge as a how-might-we question, with who it is for, the constraint and what success looks like.", 55,
        accepts="props: question (defaults to the title); items: `Who | text`, `Constraint | text`, `Success | text`; the title is the small kicker above",
        example="# The challenge we picked\nlayout: hmw\nquestion: How might we help first-year students keep a daily study habit?\n- Who | First-year students on weak connections\n"
                "- Constraint | Works offline, ten minutes a day\n- Success | Seven-day streaks double in four weeks")
def hmw(c, s):
    c.text(MARGIN, 0.6, W - 2 * MARGIN, 0.45, s.title.upper(), 14, "muted", "mono", True, chrome=True)
    c.rect(MARGIN, 1.2, 0.9, 0.07, "accent")
    q = s.prop("question") or s.title
    c.fit_text(MARGIN, 1.5, W - 2 * MARGIN, 2.5, q, 44 * c.style["heading_scale"], 22, "text", "heading", True, line_h=c.style["heading_line_h"])
    labels = ["WHO", "CONSTRAINT", "SUCCESS"]
    rows = s.items[:3]
    n = max(len(rows), 1)
    gap = 0.3
    cw = (W - 2 * MARGIN - gap * (n - 1)) / n
    for k, it in enumerate(rows):
        label, text = (cells(it, 2)[0], cells(it, 2)[1]) if it.cells else (labels[k], it.text)
        cx = MARGIN + k * (cw + gap)
        c.box(cx, 4.35, cw, 1.95, fill="surface")
        c.rect(cx, 4.35, cw, 0.07, ["primary", "warning", "success"][k % 3])
        c.text(cx + 0.3, 4.55, cw - 0.6, 0.3, label.upper(), 12, "muted", "mono", True, chrome=True)
        c.fit_text(cx + 0.3, 4.9, cw - 0.6, 1.3, text, 19, 12, "text")


@layout("kanban", "product", "Kanban board: up to four columns such as To do, Doing and Done, each with task cards and owners.", 70,
        accepts="groups: one `## Column` per column; bullets `Task | owner`; the cards in a Done column get a tick",
        example="# Two thirds of the plan is done with a day to go\nlayout: kanban\n## To do\n- Record demo video | Dana\n- Write README | Sam\n## Doing\n- Polish the queue UI | Lee\n- Load test | Ana\n"
                "## Done\n- Scoring model | Ana\n- Ranking API | Sam\n- Landing page | Dana")
def kanban(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    groups = [g for g in s.groups if g[1] or g[0]][:4]
    n = max(len(groups), 1)
    gap = 0.25
    cw = (w - gap * (n - 1)) / n
    top = y + 0.1
    for i, (head, items) in enumerate(groups):
        cx = x + i * (cw + gap)
        done = head.strip().lower() in ("done", "shipped", "finished")
        c.box(cx, top, cw, h - 0.1, fill="surface", shadow=False)
        c.rect(cx, top, cw, 0.07, "success" if done else "primary")
        c.fit_text(cx + 0.2, top + 0.15, cw - 1.0, 0.45, head.upper(), 14, 11, "text", "body", True, valign="middle")
        c.badge(cx + cw - 0.45, top + 0.38, 0.2, str(len(items)), "success" if done else "primary", 12)
        rows = items[:5]
        rh = min(0.82, (h - 0.1 - 0.85) / max(len(rows), 1) - 0.1)
        for k, it in enumerate(rows):
            task, owner = cells(it, 2)[:2]
            cy = top + 0.8 + k * (rh + 0.1)
            c.box(cx + 0.15, cy, cw - 0.3, rh, fill="bg", shadow=False, radius=0.08)
            tw = cw - 0.3 - 0.3 - (0.3 if done else 0)
            c.fit_text(cx + 0.3, cy + 0.04, tw, rh * 0.6, task, 15, 11, "text", "body", True, valign="middle")
            if owner:
                c.text(cx + 0.3, cy + rh * 0.58, tw, rh * 0.36, owner, 11, "muted", "mono", chrome=True, valign="middle")
            if done:
                c.tick(cx + cw - 0.62, cy + rh / 2 - 0.1, 0.2, "success", 2.5)


@layout("checklist", "product", "Checklist with status: each requirement or deliverable with done, doing, to do or blocked and a note.", 80,
        accepts="items: `Item | done, doing, todo or blocked | note` (up to 10, two columns above six)",
        example="# Seven of nine deliverables are done\nlayout: checklist\n- Working demo | done | live on the team laptop\n- Source code | done | public repository\n- Slides | doing | final pass tonight\n"
                "- Video | todo | record after the demo\n- Dataset licence | blocked | waiting for the organisers")
def checklist(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    rows = [cells(i, 3)[:3] for i in s.items[:10]]
    cols = 2 if len(rows) > 6 else 1
    per = (len(rows) + cols - 1) // cols
    gap = 0.4
    cw = (w - gap * (cols - 1)) / cols
    rh = min(0.78, (h - 0.1) / max(per, 1))
    for k, (item, status, note) in enumerate(rows):
        col, r = divmod(k, per)
        cx, cy = x + col * (cw + gap), y + 0.1 + r * rh
        tone = STATUS.get(status.strip().lower(), "muted")
        c.box(cx, cy + 0.04, cw, rh - 0.1, fill="surface", shadow=False, radius=0.08)
        mx, my = cx + 0.3, cy + rh / 2 - 0.05
        if tone == "success":
            c.rect(mx - 0.02, my - 0.2, 0.4, 0.4, "success", kind="ellipse")
            c.tick(mx + 0.07, my - 0.07, 0.22, c.t.on("success"), 2.5)
        elif tone == "danger":
            c.rect(mx - 0.02, my - 0.2, 0.4, 0.4, "danger", kind="ellipse")
            c.cross(mx + 0.08, my - 0.1, 0.2, c.t.on("danger"), 2.5)
        else:
            c.rect(mx - 0.02, my - 0.2, 0.4, 0.4, None, c.t.c("warning" if tone == "warning" else "muted"), 2.5, "ellipse")
            if tone == "warning":
                c.rect(mx + 0.1, my - 0.08, 0.16, 0.16, "warning", kind="ellipse")
        tw = cw - 0.9 - (cw * 0.38 if note else 0)
        c.fit_text(cx + 0.9, cy + 0.04, tw, rh - 0.1, item, 17, 11, "text", "body", True, valign="middle")
        if note:
            c.fit_text(cx + 0.9 + tw + 0.1, cy + 0.04, cw * 0.38 - 0.35, rh - 0.1, note, 13, 11, "muted", valign="middle")


@layout("links", "product", "Where to find it: demo, code, slides and contact as large rows with a label, an address and a note.", 50,
        accepts="items: `Label | address | note` (up to five); props: cta (one line above the rows)",
        example="# Try it, read it, break it\nlayout: links\ncta: Everything is public and free to use.\n- Demo | atlas.example.org | live, no sign-up\n- Code | github.com/team-atlas/atlas | MIT licence\n- Slides | atlas.example.org/slides | PDF and PPTX")
def links(c, s):
    c.title()
    c.accent_rule()
    x, y, w, h = c.content_box()
    top = y + 0.1
    if s.prop("cta"):
        c.fit_text(x, top, w, 0.6, s.prop("cta"), 22, 14, "muted")
        top += 0.8
    rows = [cells(i, 3)[:3] for i in s.items[:5]]
    rh = min(0.95, (y + h - top) / max(len(rows), 1) - 0.14)
    for k, (label, addr, note) in enumerate(rows):
        ry = top + k * (rh + 0.14)
        c.box(x, ry, w, rh, fill="surface", shadow=False)
        c.rect(x, ry, 2.5, rh, "primary")
        c.fit_text(x + 0.2, ry, 2.1, rh, label.upper(), 16, 11, c.t.on("primary"), "body", True, valign="middle")
        c.fit_text(x + 2.8, ry, w - 2.8 - (3.0 if note else 0.3), rh, addr, 26, 13, "text", "mono", True, valign="middle")
        if note:
            c.fit_text(x + w - 2.9, ry, 2.7, rh, note, 14, 11, "muted", align="right", valign="middle")
