# Ship native Claude Code, Codex, and OMP plugins

These skills remain installable through [skills.sh](https://skills.sh/the-inconvenience-store/skills) (`npx skills add the-inconvenience-store/skills`). The repository also ships plugin metadata for Claude Code, Codex, and OMP.

## Constraint

Claude accepts an explicit array of skill directories. Codex accepts one recursive root path. OMP accepts the vendor-neutral Agent Plugins format and discovers immediate child directories under `skills/`. Codex and OMP therefore require every promoted skill to be an immediate child of `skills/`.

## Decision

- Promoted skills live flat under `skills/`.
- Draft skills remain grouped under top-level `in-progress/`, outside every plugin.
- `.claude-plugin/plugin.json` lists each promoted skill explicitly.
- `.codex-plugin/plugin.json` points directly at `./skills/`.
- Root `plugin.json` declares the portable Agent Plugin consumed by OMP.
- `.omp-plugin/marketplace.json` publishes the repository root as `inconvenient-skills@inconvenient`.

## Invariants

- Every plugin contains exactly the promoted set.
- Keep all plugin and marketplace versions synchronized through `.version-bump.json`.
- Validate Claude with `claude plugin validate . --strict`.
- Validate Codex with `python3 /Users/samstevens/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`.
- Validate OMP with `omp plugin install --dry-run .`, then exercise the marketplace add, discover, install, and list flow in an isolated home directory.
