# Adapters

The skill has one source of truth: `SKILL.md`, `references/`, `scripts/`, `assets/`. The files in this folder
and the root `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` are generated pointers; they never restate the skill.
Regenerate with `python scripts/build_adapters.py` (`--check` in tests). Do not edit them by hand.

## Where each file goes

| Agent | File here or at the root | Installed as | Scope |
|---|---|---|---|
| Claude Code | the whole skill folder | `~/.claude/skills/deck-master/` or `.claude/skills/deck-master/` | user or project |
| Codex | the whole skill folder | `~/.agents/skills/deck-master/` or `.agents/skills/deck-master/` | user or project |
| Cursor | `adapters/cursor/deck-master.mdc` | `.cursor/rules/deck-master.mdc` | project |
| GitHub Copilot | `adapters/copilot/copilot-instructions.md` | block in `.github/copilot-instructions.md` | project |
| Gemini CLI | `GEMINI.md` (imports `AGENTS.md`) | block in `GEMINI.md` or `~/.gemini/GEMINI.md` | project or user |
| Windsurf | `adapters/windsurf/deck-master.md` | `.windsurf/rules/deck-master.md` | project |
| Any tool that reads AGENTS.md | `AGENTS.md` | block in `AGENTS.md` | project |

In the adapter files `<skill-root>` is a placeholder; `scripts/install.py` replaces it with the real path (relative to
the project, or the vendored `.deck-master` folder with `--vendor`).

## Install

```
python scripts/install.py --agent claude --scope user
python scripts/install.py --agent cursor --scope project --project path/to/repo --vendor
python scripts/install.py --agent all --scope project --project path/to/repo --check
```

Details and safety rules (marker file, managed blocks, no blind overwrite): `references/extending.md`.

## Conventions as of 2026-10

Checked against each tool's public documentation: Codex skills live in `.agents/skills` (repo) and
`$HOME/.agents/skills` (user) with `SKILL.md` frontmatter `name` and `description` and optional `agents/openai.yaml`;
Cursor rules are `.mdc` files in `.cursor/rules` with `description`, `globs`, `alwaysApply`, and Cursor reads
`AGENTS.md`; Copilot reads `.github/copilot-instructions.md` and `AGENTS.md`; Gemini CLI loads `GEMINI.md` and supports
`@file` imports. Tools change; if a path stops working, check the tool's docs and update `scripts/install.py`.

## Agent-neutral by design

The skill needs only file read and write and a shell. It names no agent-specific tools, subagents or MCP servers; a
test fails if the docs mention them.
