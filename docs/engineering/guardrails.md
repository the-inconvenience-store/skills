Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=guardrails
```

```bash
npx skills update guardrails
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/guardrails)

## What it does

`guardrails` guides the setup of a project's linters, formatter, tests, reproducible installation, dependency upkeep, CI checks, and hooks. It can start in an empty workspace or adapt an established repository without quietly replacing conventions that already work.

The **proposal** is the control point: the agent investigates and recommends one coherent setup, then waits for you to approve or amend it before changing the project.

For JavaScript, TypeScript, React, and Go, the skill carries curated rule baselines aimed at common agent-written failure modes. Those concrete recommendations feed the proposal; they are not installed wholesale without your approval.

For Ruby, C#, Rust, and other ecosystems without a bundled baseline, the agent researches current maintained tools and exact rules, then builds the equivalent proposal instead of skipping the language.

For a new React application, it also offers a Bulletproof React-inspired standards package—feature boundaries, import direction, state and API conventions, and testing posture—as an explicit choice rather than an assumed architecture.

## When to reach for it

Type `/guardrails`, or the agent reaches for it automatically when a task fits.

Reach for it when scaffolding a project, adding its first quality checks, replacing an unsatisfactory tool, or bringing inconsistent lint and hook configuration back under control. For configuring the issue tracker and documentation expected by this collection's engineering flows, use [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) instead.

## Guardrails with boundaries

The skill separates fast local feedback from the complete CI gate. It keeps local hooks focused, makes slower checks explicit, and treats architecture rules, coverage, commit policy, and agent-specific hooks as choices rather than surprise additions.

It can also set up or reuse an optional task runner, then make its `bootstrap`, `check`, and `codegen` tasks the shared interface where those jobs apply. Without a task runner, it keeps the project's native commands instead of adding task aliases.

When the project needs them, the proposal also covers a real test baseline, generated-code drift checks, locked installation, dependency audits and update automation, and proof that a fresh checkout can pass the complete gate. Update bots and other workflow changes remain explicit choices.

Verification is proportionate: commands are run, representative failures are demonstrated safely, and anything that would require commits, merges, installs, or other side effects is left unverified unless you approve it.

## It's working if

- The approved lint and format commands cover every detected ecosystem, or the report names a researched coverage gap.
- Existing tools were preserved or replaced for a stated reason.
- Local hooks are fast, CI owns the complete gate, and each boundary is visible.
- A fresh checkout has a defined locked setup-and-check path, even when that path could not be exercised safely during setup.
- Generated code and dependency updates have clear commands and ownership when the project uses them.
- Pre-existing failures and unverified behavior are reported rather than hidden.

## Where it fits

`guardrails` is a run-once setup, repeated when the stack or quality strategy changes. Its neighbour [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) configures the surrounding engineering workflows; downstream skills such as [implement](https://aihero.dev/skills-implement) then work inside the guardrails approved here. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) maps the full collection.
