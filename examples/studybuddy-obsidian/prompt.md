# Prompt: trim the demo-day deck and rebuild it as a game presentation

Files given to the agent: `inputs/long-deck.md` (the 12-slide, 10-minute deck) and `inputs/assets/demo-ui.png` (a screenshot).

> Use deck-master. `inputs/long-deck.md` is our 10-minute demo-day deck. We now only have 5 minutes and at most 8 slides.
> Trim it and rebuild it as a fully game-style Minecraft presentation in the dark obsidian theme. Do not use the same
> plain components everywhere: use the game components (a boss fight for the problem, a crafting table for how it works,
> hearts and drumsticks for the pilot stats, an advancement path for the roadmap). Put different Minecraft mobs on most
> slides as decoration, and Steve, Alex, a villager and a pig as the team. Tell me what you cut and why. This is a
> personal demo day, not a company pitch.

## What it exercises

| Skill behaviour | How it shows |
|---|---|
| Trim with the cut order, rubric kept | `cut.md` maps every original slide; all four criteria still on slides |
| Game components instead of generic cards | boss, crafting, demo frame, hud, team, advancements |
| Mob decoration on content slides | a framed mob head beside each title and walkers standing on the floor strip, a different set per slide |
| Gamified details | XP progress bar along the top, hotbar-style floor, an "Advancement made" toast on the closing slide |
| Numbers unchanged | every number in the new deck exists in the original deck |
| Personal-use guardrail | the notes say the characters are Minecraft characters used for a personal, non-commercial demo day |

## What a good run does

1. Checks the use is personal and non-commercial before using characters.
2. Keeps the problem, the innovation, the demo, the evidence and the plan; cuts market size, competitors and pricing first.
3. Chooses a component for each message instead of reusing one layout.
4. Lints clean, looks at the previews, and reports what was cut and how to rebuild.
