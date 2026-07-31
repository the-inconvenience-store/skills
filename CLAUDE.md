Promoted skills live as immediate child directories under `skills/`. This flat layout is required by the Codex plugin format. Draft skills live separately under `in-progress/` and do not ship.

Every promoted skill must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`'s `skills` array. `.codex-plugin/plugin.json` loads the same set recursively from `skills/`. Nothing under `in-progress/` may appear in either plugin or the top-level skill index.

The repo is its own single-plugin Claude Code marketplace: `.claude-plugin/marketplace.json` lists the one `inconvenient-skills` plugin. The Codex manifest lives at `.codex-plugin/plugin.json`. Keep the Claude and Codex manifest versions in sync. Validate both with `claude plugin validate . --strict` and the Codex plugin validator described in [.agents/adr/0002-ship-as-a-claude-code-plugin.md](./.agents/adr/0002-ship-as-a-claude-code-plugin.md).

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

The top-level `README.md` groups promoted skills into Engineering and Productivity, then into **User-invoked** and **Model-invoked**.

Every promoted skill also has a human-facing docs page at `docs/<category>/<skill-name>.md`, where `<category>` is `engineering` or `productivity`. The published URL is `https://aihero.dev/skills-<skill-name>` regardless of category. When you add, rename, or change a promoted skill, create or re-sync its docs page following [.agents/writing-docs.md](./.agents/writing-docs.md). Drafts under `in-progress/` get no docs page.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true` plus `policy.allow_implicit_invocation: false` in `agents/openai.yaml`, reachable only by the human) or model-invoked (model- or user-reachable). See [.agents/invocation.md](./.agents/invocation.md).

[`ask-inconvenient`](./skills/ask-inconvenient/SKILL.md) is the router that maps every user-reachable skill and how they relate. The same trigger that re-syncs a docs page applies to it: whenever you add, rename, remove, or change how a user-reachable skill fits the flows, re-read `ask-inconvenient`'s `SKILL.md` and update it so the map stays accurate — a new skill it never mentions, or a stale one it still routes to, is a router that lies.

To (re)link every skill into the local harness skill directories (`~/.claude/skills`, `~/.agents/skills`), run `scripts/link-skills.sh`. Each entry is a symlink into this repo, so a `git pull` keeps installed skills current; re-run the script after adding, removing, or renaming a skill.
