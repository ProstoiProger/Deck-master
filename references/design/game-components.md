# Game components

Ten Minecraft-style components for the game themes (`obsidian-craft`, `classic-craft`), plus automatic mob decoration. They
replace generic cards when the message has a game-shaped metaphor. Inputs for each: `design/catalog.md` (generated).

## Contents

1. When to use which component
2. The components
3. Icons and characters in items
4. Automatic decoration
5. Rules

---

## 1. When to use which component

| The message | Component | Why it fits |
|---|---|---|
| the problem, a threat, a number to defeat | `boss` | a boss bar holds the number, the mob is the problem, attacks are its causes |
| how it works: parts combine into a product | `crafting` | ingredients in a 3 by 3 grid become one result |
| the stack, features, what we carry | `inventory` | slots with counts and an item list that names each one |
| results, pilot stats, scores | `hud` | hearts, drumsticks, shields and XP bars |
| roadmap, milestones, study path | `advancements` | framed icons joined by a path; done, current, locked |
| before and after, cost and benefit | `trade` | villager trade rows: give on the left, get on the right |
| quotes, user feedback, demo steps | `chat` | messages from named characters |
| architecture, layers, tech stack | `strata` | sky, grass, dirt, stone, deepslate; components are ores, the key one a diamond |
| ranking, benchmark, latency by setup | `leaderboard` | bars with a mob per row; the best one gets the gold and a trophy |
| done and next, limits, two lists | `book` | two parchment pages |
| agenda | `agenda` in a game theme | a hotbar; `Step | creeper` puts a character in the slot |
| the last slide | `closing` with `achievement:` | an "Advancement made" toast |

## 2. The components

- **`boss`**: props `boss: zombie`, `stat: 14 days | what it measures`, `hp: 100`; first paragraph is the lore; up to three attack items.
- **`crafting`**: items are ingredients `Name | icon or character` (up to nine); `result: Name | icon | note`; first paragraph is the caption.
- **`inventory`**: items `Name | detail | icon or character | count` (up to 12); `select: 2` highlights a slot and its legend row.
- **`hud`**: items `value | label | heart, hunger, armor, xp or boss | context | fill%`. A percent or `a of b` value fills the bar;
  the optional fifth cell sets the fill in percent and is never printed, so a bar can show a ratio without a number that is not in
  your sources.
- **`advancements`**: items `Title | detail | icon | done, current or locked` (up to six); nodes are larger when there are four or fewer.
- **`trade`**: items `Before | After | note` (up to four); `trader: villager` picks the portrait.
- **`chat`**: items `Speaker | message | character` (up to seven); first paragraph is a `[Server]` line.
- **`strata`**: items `Layer: component, component`; wrap the key component in `**bold**`.
- **`leaderboard`**: items `Name | value | character | note`; `better: lower` for times and latency.
- **`book`**: two `## heading` groups with bullets, or items on the left page and the first paragraph on the right.

Example (from `examples/studybuddy-obsidian/studybuddy.md`):

```
# Pilot stats: students finished more tasks and kept streaks
layout: hud
source: inputs/long-deck.md
- 72% | tasks completed | heart | vs 51% with a plain list
- 31 of 40 | kept a 7 day streak | hunger | pilot group of 40
- 4.4 / 5 | would use again | xp | exit survey
```

## 3. Icons and characters in items

An item's icon cell names a **pixel icon** or a **character**. Pixel icons are original art drawn for the skill: heart, drumstick,
shield, xp, diamond, emerald, coin, apple, potion, book, torch, sword, pickaxe, star, trophy, sparkle (heart, drumstick, shield and
xp also have `_empty` variants). Characters come from `design/entities.md` (about 60 mobs and block-heads). An unknown name leaves an
empty slot and a Medium lint finding that lists the valid names.

## 4. Automatic decoration

In a game theme every content slide gets:

- a framed mob head at the right end of the title line;
- three mobs standing on the floor strip at the bottom, different on each slide;
- an XP progress bar along the top edge (slide number over slide count);
- a floor strip carrying the footer text and page number.

Which mobs: the slide's `mobs:` list, else the deck front matter `mobs: [...]`, else a theme default (dark and hostile mobs for
`obsidian-craft`, friendly farm and forest animals for `classic-craft`). Turn it off for one slide with `decor: none`. Title and
closing slides use a mascot (`mascot: creeper`) or the portal and cloud art instead.

If the character images are not downloaded the decoration is skipped, with one Low note: run
`python scripts/cli.py entities fetch`.

## 5. Rules

- One message per slide still holds: a component carries the message, the mobs only decorate.
- Do not mix more than three different components in a row of slides; vary them by message, not by decoration.
- Numbers keep their sources: put `source:` on every slide that shows a number, also on components.
- Game components render in any theme but are designed for the game themes; in the IT themes use the general layouts.
- The characters are for personal, non-commercial decks (`design/entities.md`).
