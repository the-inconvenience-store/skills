Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wizard
```

```bash
npx skills update wizard
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wizard)

## What it does

`wizard` generates an interactive bash script for a procedure that contains steps only a human can perform. It can open dashboards, capture values, update `.env`, and set GitHub secrets or variables.

The agent writes and statically verifies the script; it does not run the procedure. You run it in your terminal, where secret input stays hidden and each stage waits for you.

## When to reach for it

Type `/wizard`, or the agent reaches for it automatically when work hits a human-only step.

Reach for it when provisioning infrastructure, collecting credentials, navigating an unfamiliar third-party dashboard, or running a migration or cutover. If the agent has the access and tools to perform the step itself, it should do so instead.

## Prerequisites

The generated script requires bash. Stages that write GitHub secrets or variables use `gh`; when it is unavailable or unauthenticated, the wizard records the skipped action for you to finish manually.

## A staged procedure

Before writing the script, the skill reads the repository and scopes every manual stage and captured value. Each value has a source, a destination, and a secrecy classification. The fixed template supplies confirmation gates, URL opening, hidden input, idempotent environment updates, stage progress, and a closing record of skipped work.

## It's working if

- Every human action is a named stage in dependency order.
- Secret values use hidden input and land only where the scope says they should.
- `bash -n` passes, and `shellcheck` passes when available.
- The script has stage counts, not invented time estimates.

## Where it fits

`wizard` is a reach-for-it-anytime standalone at the boundary between automation and human access. It often appears during [implement](https://aihero.dev/skills-implement) when a build needs credentials or a cutover. [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) configures this skill set; `wizard` generates setup paths for everything else. [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you when the boundary is unclear.
