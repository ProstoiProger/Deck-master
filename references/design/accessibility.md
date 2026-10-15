# Accessibility

A deck that cannot be read is a failed deck. These rules are enforced by `cli.py lint` where they can be measured.

## Contrast and size

| Rule | Value | Enforced by |
|---|---|---|
| Body text contrast | 4.5:1 or more | lint, High |
| Large text (18 pt, or 14 pt bold) | 3:1 or more | lint, High |
| Minimum font anywhere | 11 pt (pixel headings 12 pt) | lint, Medium |
| Bullets per slide | at most 7 | lint, Medium |
| Words per slide | within the layout's budget | lint, Medium |

Contrast is checked against the shape behind the text (card fill) and falls back to the slide background; text on
images is not measured, so keep text off photos or add a solid card.

## Colour and meaning

- Do not use colour alone: label success, warning and danger with a word.
- Avoid red-green pairs for the only distinction between two series; use the accent and a muted tone, or add labels.
- Charts highlight one element with the accent colour and mute the rest.

## Rooms and screens

- Back-row test: stand 3 metres from a laptop screen; numbers and titles must be legible. Increase sizes, not density.
- Bright projectors wash out dark themes with thin lines; prefer `cloud-light` or thicken shapes.
- Check the deck at the venue resolution; 16:9 is used throughout.

## Documents and files

- The PDF has real text (searchable, copyable), not pictures of slides.
- Add alt text in the notes for key images when the deck is shared as a document: describe what the picture proves.
- Reading order follows the slide order; speaker notes carry what the slide leaves out.

## Language

Check glyph coverage for every script used (`design/typography.md`). A missing glyph shows as a box and is a High
finding.
