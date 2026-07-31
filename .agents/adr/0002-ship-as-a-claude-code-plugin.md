# Ship native Claude Code and Codex plugins

These skills remain installable through [skills.sh](https://skills.sh/the-inconvenience-store/skills) (`npx skills add the-inconvenience-store/skills`). The repository also ships native plugin metadata for Claude Code and Codex.

## Constraint

Claude accepts an explicit array of skill directories. Codex accepts one recursive root path and requires every skill to be an immediate child of `skills/`.

## Decision

- Promoted skills live flat under `skills/`.
- Draft skills remain grouped under top-level `in-progress/`, outside both plugins.
- `.claude-plugin/plugin.json` lists each promoted skill explicitly.
- `.codex-plugin/plugin.json` points directly at `./skills/`.

## Invariants

- Both native plugins contain exactly the promoted set.
- Keep `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` versions synchronized.
- Validate Claude with `claude plugin validate . --strict`.
- Validate Codex with `python3 /Users/samstevens/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`.
