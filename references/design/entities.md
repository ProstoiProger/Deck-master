# Character images (Steve, Creeper and friends)

The two block-game themes, `obsidian-craft` (dark) and `classic-craft` (light), show well-known game characters
as decoration on most slides, team avatars, mascots, boss portraits and component icons. The images are optional, downloaded on demand and never shipped with the
skill.

## Contents

1. Get the images
2. Use them in a deck
3. Which character for what
4. Rules of use
5. Without images
6. Sources and limits

---

## 1. Get the images

```
python scripts/cli.py entities fetch                 all characters, all kinds (about 115 small PNG files)
python scripts/cli.py entities fetch --names steve creeper --kinds face head
python scripts/cli.py entities list                  what is downloaded
```

Files go to `assets/entities/` (git-ignored). Kinds: `face` (flat head, used for avatars and hotbar slots), `head`
(isometric 3D head with transparency, used for mascots and floor walkers) and `body` (full figure, Steve and Alex only). A character
without a `head` render uses its `face`. Set `DECKKIT_ENTITIES_DIR` to use another folder.

Available, about 60 in four groups:

- **players**: steve, alex
- **friendly**: villager, pig, cow, mooshroom, chicken, sheep, wolf, cat, ocelot, horse, fox, panda, parrot, bee, rabbit, turtle,
  dolphin, squid, goat, allay, sniffer, iron-golem
- **hostile**: creeper, zombie, skeleton, stray, husk, drowned, spider, cave-spider, enderman, endermite, silverfish, blaze, ghast,
  magma-cube, slime, witch, phantom, vex, evoker, vindicator, pillager, guardian, warden, shulker, piglin, zombified-piglin, strider, pufferfish
- **blocks and signs**: tnt, chest, cake, pumpkin, melon, cactus, oak-log, question, exclamation

## 2. Use them in a deck

| Where | Syntax | Result |
|---|---|---|
| Every content slide of a game theme | automatic | a mob head beside the title and three mobs on the floor strip (`design/game-components.md`) |
| Choose the decoration mobs | front matter `mobs: [creeper, enderman]` or a slide's `mobs: pig, cow` | the pool the decoration draws from; `decor: none` turns it off for one slide |
| Team slide | `- Dana K. | Pipeline | built the stream | steve` | the character is the member's avatar (4th cell) |
| Title or closing slide | `mascot: creeper` | large 3D head on the right |
| Problem slide | `mascot: zombie` | small face in the corner of the stat card |
| Boss component | `boss: zombie` | the boss portrait and boss bar name |
| Agenda in a game theme | `- Signal | creeper` | the character fills the hotbar slot |
| Components with icon cells | `- Quests | detail | steve | 4` | a character in an inventory slot, chat avatar or leaderboard row |
| Any image of your own | `mascot: figures/me.png` | a path instead of a name works for the same slots |

Examples: `examples/studybuddy-obsidian/studybuddy.md` (dark) and `examples/network-lesson-classic/lesson.md` (light).

## 3. Which character for what

| Message | Suggested character |
|---|---|
| team members | steve, alex, villager, pig |
| expert, mentor, trader | villager |
| risk, bug, sudden failure | creeper |
| legacy system, tech debt | zombie |
| attacker, adversary, edge case | skeleton |
| crawler, scraper, network | spider |
| data transfer, migration, sync | enderman |
| load, performance pressure | blaze |
| big outage or threat | ghast |
| memory leak, splitting work | slime |
| security, guard | iron-golem |
| ML model, black box | witch |
| users, crowd | sheep |
| helpful monitor or loyal helper | wolf |
| resources, small services | cow, chicken |

Use characters as accents, not as the argument: one idea per slide stays the rule.

## 4. Rules of use

The characters and the game belong to Mojang and Microsoft. As of 2026-10 their usage guidelines (verify the current
text on minecraft.net) give the community permission for non-commercial fan content such as screenshots and videos,
revocably, and do not cover commercial promotion of unrelated products or implying endorsement. Therefore:

- Use them for personal, educational and hackathon decks only. Ask the user before using them in a company,
  commercial or promotional deck (hard stop in `SKILL.md`).
- Do not redistribute the image files: they are git-ignored and absent from the repository and from installs.
  Share the finished deck, not the `assets/entities` folder.
- Do not add the game's logo, wordmark or title text, and do not claim or imply affiliation or endorsement; the
  themes are inspired by the style, with original shapes, and named `obsidian-craft` and `classic-craft`.
- Keep a line in the deck notes or the final report saying the characters are Mojang/Microsoft property.
- Rules can change; if a rights holder objects, remove the characters (`mascot:` and the 4th team cell) and rebuild.

## 5. Without images

Nothing breaks: a team member without an image gets an initials badge, a missing mascot or avatar produces a Medium
lint finding that names the fetch command, and every theme works the same. An unknown character name is a Medium
finding listing the known names.

## 6. Sources and limits

`entities fetch` downloads the heads of Mojang's public MHF skin accounts through the community render services
minotar.net (flat faces) and mc-heads.net (3D heads and bodies). These services are third-party, can change or
disappear, and some accounts have no 3D render (the fetch reports them and the layouts use the face). Fetching sends
only the account names. Pixel art is shown scaled up; it is intended to look blocky.
