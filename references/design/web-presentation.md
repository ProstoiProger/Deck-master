# Web presentation (HTML output)

The third output next to PPTX and PDF: one self-contained `.html` file that runs in any modern browser, on a laptop, a projector, a
phone or a link on a website. It is drawn from the same scene as the other two, so slides look the same.

## Contents

1. Build and open
2. What is in the file
3. Using it: keys, touch, presenter window
4. Adaptive: which view you get
5. Sharing and hosting
6. How it matches the PDF
7. Limits and QA

---

## 1. Build and open

```
python scripts/cli.py build deck.md --html --out build        # only the web version
python scripts/cli.py build deck.md --out build               # no format named: .pptx, .pdf and .html
python scripts/cli.py serve build/deck.html                   # localhost server, opens the browser
```

Double-clicking `build/deck.html` works too. `serve` is better when you present with the presenter window (section 3): browsers sync two
windows more reliably on `http://localhost` than on `file://`. The same lint gate runs first; a deck with Critical or High findings is not built.

## 2. What is in the file

| Part | How |
|---|---|
| Shapes, polygons, lines | inline SVG in the original drawing order |
| Text | one block per text box; the lines are the ones the shared text fitting broke, joined by line breaks, so no browser re-wraps them |
| Fonts | subset copies of the bundled fonts, embedded as WOFF (only the characters the deck uses) |
| Pictures, charts, covers, 3D objects | embedded as data URIs (PNG or JPEG) |
| Speaker notes | in the page; shown with `N` and in the presenter window |
| Addresses such as `github.com/team/repo` or `team@example.org` | clickable links (single-line text only) |
| Security | a strict Content-Security-Policy: no network requests, no external scripts, fonts or images |
| Size | typically 200 KB to 1 MB for 10 to 80 slides |

## 3. Using it: keys, touch, presenter window

| Action | Keys and gestures |
|---|---|
| Next, previous | `Right`, `Space`, `PageDown`; `Left`, `PageUp`, `Backspace`; click the right or left 30% of the slide; swipe on a touch screen |
| First, last | `Home`, `End` |
| Overview grid | `O` (click a thumbnail to jump, `Esc` to close) |
| Speaker notes and timer | `N` (the timer starts on the first slide change; `R` resets it; the planned time is the deck's `minutes`) |
| Presenter window | `P` opens a second window with the current slide, the next slide, the notes and the timer, kept in step with the audience window |
| Fullscreen | `F` |
| Reading view or slides | `V` (or `?view=reader`, `?view=slides`) |
| Help | `?` |
| Link to one slide | the address bar shows `#3` for slide 3; share that link |
| Print or save as PDF | `Ctrl+P`: one slide per page, 16:9, nothing scaled (checked with Chrome's print to PDF: one page per slide) |

The slide scales to the window and is centred; the controls hide when the pointer rests. Text and pictures rise in one after the other when a
slide appears (switched off for people who ask their system for reduced motion).

## 4. Adaptive: which view you get

The page picks a view for the device and lets you change it.

| Device and window | View | Why |
|---|---|---|
| Laptop, desktop, TV, projector, ultrawide, tablet in landscape | **Slides**: the 16:9 slide scaled to fit, centred, with margins on the sides or top | the slide is large enough to read |
| Phone or tablet in portrait; any window where the slide would shrink below about half size (for example a phone in landscape) | **Reading view**: every slide as a card of real, reflowing text and pictures in one scrolling page, with a sticky header (title, position, a button to switch) | scaled-down slide text is unreadable on a small screen |

- Override: press `V`, tap the switch button (bar or header), or add `?view=slides` or `?view=reader` to the address. The choice is remembered in the browser.
- The reading view is built from the same slides: the slide title first, then each card's texts together and in reading order (cards left to right, top to bottom),
  pictures and charts in place, text colors and card fills kept so contrast stays what lint checked, links clickable, speaker notes under each card in a
  collapsible block. Headline numbers are enlarged, small mono labels become captions.
- Texts are laid out by position, so a table drawn as rows and columns (a journey map, a scorecard) reads row by row: check such slides in the reading view.
- Touch: swipe left and right in the slides view, tap the right side to go on, buttons grow to 44 px on touch screens, and the page respects the notch and
  home-indicator areas. The presenter window and fullscreen buttons are hidden where they do not work (touch devices, iPhone Safari).
- Also handled: browser address-bar resizing, rotation, reduced-motion, forced-colors (high-contrast) mode, and
  print (the page prints as slides in either view).

## 5. Sharing and hosting

- Send the single `.html` file or open it from a USB stick: it needs nothing else.
- Host it on any static host (GitHub Pages, Netlify, an organisation web server): upload the file; slide links work as `deck.html#5`.
- Embed in an `<iframe>` only on a host you control; the file sets its own security policy.
- Confidential decks: the file contains every slide, note and picture in readable form. Treat it like the PPTX (`ops/security.md`).

## 6. How it matches the PDF

The PDF and the HTML are drawn from the same list of shapes and text lines, with the same fonts, so the only differences are the browser's
own anti-aliasing and hairline widths. Charts and the 3D objects are pictures in both. Nothing in the HTML is re-laid-out by the browser,
which is why a slide that passes lint in the PDF also fits in the browser.

## 7. Limits and QA

- In the slides view the stage keeps its 16:9 shape and is scaled; reflow happens only in the reading view, which is a plain reading of the slides, not a redesign.
- Text is selectable and links work, but charts are pictures, so their numbers are not readable by a screen reader; put the key figure in the
  slide text or the notes (the lint's number rule already pushes it there).
- Animations are limited to the entrance of text and pictures; there are no per-click builds.
- Open the file once in a browser before delivering: step through with the arrow keys, open the notes (`N`) and the overview (`O`), and check the
  last slide; then press `V` (or narrow the window) and scroll the reading view once, since it is built from the same slides but laid out differently. The page was tested in Chrome (navigation, overview, notes, presenter sync, print to PDF) and in Chrome frames of 390x844, 844x390, 768x1024, 1024x768, 1920x1080 and 3440x1440; no real phone or tablet was used; it uses only long-standing features (SVG, CSS transforms, BroadcastChannel, `@font-face`),
  so Edge, Firefox and Safari are expected to work but were not tested; very old browsers are not supported.
- A browser prints backgrounds only if "background graphics" is on; the page asks for it, but some print dialogs ignore that.
