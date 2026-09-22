# skills

A personal collection of agent skills I use often — the ones worth carrying between machines, projects, and agent runtimes.

Each top-level directory is a self-contained skill: a `SKILL.md` with YAML frontmatter (`name`, `description`) plus any reference docs or scripts it needs.

## Skills

| Skill | What it does |
| --- | --- |
| [`gh-axi`](gh-axi/SKILL.md) | Operate GitHub through the `gh-axi` CLI — issues, PRs, workflow runs, releases, repos, labels, gists, Projects (v2), Actions secrets/variables, search, and raw API access. |

## Install

Copy (or symlink) the skill directory into the skills directory your agent reads.

**Shared agent skills dir** (e.g. Hermes / Claude Code):

```powershell
# Windows
Copy-Item -Recurse -Force .\gh-axi "$env:USERPROFILE\.agents\skills\gh-axi"
```

```bash
# macOS / Linux
cp -R ./gh-axi ~/.agents/skills/gh-axi
```

Symlinking is preferable if you want edits here to apply immediately:

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.agents\skills\gh-axi" -Target (Resolve-Path .\gh-axi)
```

```bash
ln -s "$(pwd)/gh-axi" ~/.agents/skills/gh-axi
```

Or clone this repo once and point your agent at it. Keep skill directories flat at the repo root so a single directory can be copied into any agent's skills path unchanged.

## Layout

```
skills/
├── README.md
├── LICENSE
└── gh-axi/
    └── SKILL.md
```

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter:
   ```yaml
   ---
   name: skill-name
   description: What it does. Use when <specific triggers>.
   ---
   ```
2. Keep `SKILL.md` under ~100 lines; push detail into sibling files (`REFERENCE.md`, `EXAMPLES.md`, `scripts/`) and link them.
3. Make the `description` do the work — it is the only text an agent sees when deciding whether to load the skill.
4. Add a row to the table above.

## License

MIT — see [LICENSE](LICENSE).
