# Report: networks lesson in the classic-craft theme

## Profile

| Field | Value | Status |
|---|---|---|
| Event | first-year computer networks, opening lesson | fact (prompt) |
| Time | 8 minutes, then a lab | fact (prompt) |
| Theme | `classic-craft` (light classic game look) | fact (prompt) |
| Components | inventory, crafting, strata, trade, leaderboard, chat, hud, book, hotbar agenda | fact (prompt) |
| Numbers | only those in `inputs/lesson-notes.md` | fact (prompt) |
| Use | personal classroom use, non-commercial | fact (prompt) |

## Deliverables

- `lesson.md` (source), `lesson.pptx`, `lesson.pdf`, `preview.png`.
- Rebuild: `python scripts/cli.py build examples/network-lesson-classic/lesson.md --out build`.

## Verification (actually run)

- `cli.py lint`: 0 findings. `cli.py timing`: 7.5 of 8 minutes at 140 wpm.
- Numbers compared with `inputs/lesson-notes.md`: every number printed on a slide or said in the notes is in the notes. The
  hud bars take a separate fill percentage (graphic only, 100, 98.6 and 50, derived from 0 and 14 of 1,000 and from 9 against
  18 ms), which is never printed.
- Previews viewed: all 11 slides; the mobs on the floor and beside the titles differ on each slide.

## Assumptions and open risks

- The measurements are fictional lab numbers for illustration; replace them with the class's own results.
- The characters belong to Mojang/Microsoft: personal, non-commercial use only; do not publish the files.
- The metaphors (layers as a building, a packet as a crafted item) are teaching aids, not definitions; the notes say so.
