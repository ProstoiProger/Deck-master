# What was cut, merged and restyled (12 slides, 10 minutes -> 8 slides, 5 minutes)

Cut order from `references/protocol/2-story.md`: background, competitors, pricing and secondary detail go first; the problem,
the innovation, the demo, the evidence and the plan stay. Every rubric item remains on a slide.

| Original slide | Decision | New component |
|---|---|---|
| 1 Title | kept | `title` with Alex as the mascot |
| 2 Problem (14 days) | kept as a boss fight | `boss`: Zombie boss bar with the number, three attack patterns |
| 3 Market size | cut | not judged in a 5-minute pitch |
| 4 Competitor comparison | cut | one idea (small steps, instant feedback) moved into the crafting slide notes |
| 5 Feature grid (quests, streaks, XP, party) | merged | `crafting`: task + timer + XP reward + rest token craft a quest |
| 6 Architecture | merged | first advancement "web client and small backend" (feasibility, R3) |
| 7 Demo | kept | `demo` with the screenshot and three callouts |
| 8 Pilot results | kept as stats | `hud`: hearts (72%), drumsticks (31 of 40), XP bar (4.4 / 5) |
| 9 Pricing | cut | not a judging criterion |
| 10 Team | kept | `team` with Steve, Alex, Villager and Pig as avatars |
| 11 Roadmap | kept as a path | `advancements`: Prototype done, Campus pilot now, Study locked |
| 12 Closing | kept | `closing` with Steve and an "Advancement made: Demo day survived" toast |

Numbers kept unchanged from the original: 14 days, 72%, 51%, 31 of 40, 7 day streak, 4.4 / 5, 40 students, 200 students, 25 minute quests.
Numbers dropped with their slides: 2.3M, 40k, 6%, 4 USD, 9,600 USD.

Result: 8 slides (cap 8); the time plan is 4.8 of 5 minutes including a 55 second demo; all four rubric items covered.

Decoration: every content slide shows one framed mob head beside the title and three mobs on the floor strip, drawn from the
deck's `mobs:` list (creeper, enderman, skeleton, witch, ghast, spider, blaze, warden, phantom, vex, shulker, evoker, guardian,
magma cube) and different on each slide. Turn it off for a slide with `decor: none`.

Rebuild or restyle: `python scripts/cli.py build examples/studybuddy-obsidian/studybuddy.md --out build` and add
`--theme classic-craft` for the light game look.
