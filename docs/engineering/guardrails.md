Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=guardrails
```

```bash
npx skills update guardrails
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/guardrails)

## What it does

`guardrails` guides the setup of a project's linters, formatter, tests, reproducible installation, dependency upkeep, security scanning, CI checks, and hooks. It can start in an empty workspace or adapt an established repository without quietly replacing conventions that already work.

The **proposal** is the control point: the agent investigates and recommends one coherent setup, then waits for you to approve or amend it before changing the project.

For JavaScript, TypeScript, React, and Go, the skill carries curated rule baselines aimed at common agent-written failure modes. Those concrete recommendations feed the proposal; they are not installed wholesale without your approval. The skill is **generous** with lint coverage: it proposes every maintained linter, plugin, and rule group that applies to the stack, and leaves one out only for a named reason such as duplication, a formatter conflict, or hook runtime. When it sets up a JavaScript or TypeScript formatter (Prettier, oxfmt, or Biome), it starts from a house style: 2-space indent, 80-column width, trailing commas everywhere, no semicolons, single quotes in code, and double quotes in JSX.

For Ruby, C#, Rust, and other ecosystems without a bundled baseline, the agent researches current maintained tools and exact rules, then builds the equivalent proposal instead of skipping the language.

For a new React application, it also offers a Bulletproof React-inspired standards package—feature boundaries, import direction, state and API conventions, and testing posture—as an explicit choice rather than an assumed architecture.

## When to reach for it

Type `/guardrails`, or the agent reaches for it automatically when a task fits.

Reach for it when scaffolding a project, adding its first quality checks, replacing an unsatisfactory tool, or bringing inconsistent lint and hook configuration back under control. For configuring the issue tracker and documentation expected by this collection's engineering flows, use [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) instead.

## Guardrails with boundaries

The skill separates fast local feedback from the complete CI gate. It keeps local hooks focused, makes slower checks explicit, and treats architecture rules, coverage, commit policy, and agent-specific hooks as choices rather than surprise additions. When git hooks are in scope, it asks whether you want Conventional Commits enforced on `commit-msg`: commitlint for JavaScript and TypeScript repos, cocogitto for everything else.

It can also set up or reuse an optional task runner, then make its `bootstrap`, `check`, and `codegen` tasks the shared interface where those jobs apply. Without a task runner, it keeps the project's native commands instead of adding task aliases.

When the project needs them, the proposal also covers a real test baseline, generated-code drift checks, locked installation, dependency audits and update automation, and proof that a fresh checkout can pass the complete gate. Update bots and other workflow changes remain explicit choices.

## Security scanning at commit time

Semgrep and Gitleaks are optional, but recommended when agents commit to the repo. They run as **pre-commit** hooks on staged changes, so an injectable query, disabled TLS check, or pasted API key is caught at the commit that introduces it rather than at review. CI runs the same scans as the backstop. Semgrep's rules are committed to the repo so the hook works offline and stays fast. They include a small set of project rules aimed at mistakes agents commonly make, each with a message naming the safe alternative. Registry rules are vendored only into private repos, because their license forbids redistribution; public repos fetch those packs in CI instead.

Verification is proportionate: commands are run, representative failures are demonstrated safely, and anything that would require commits, merges, installs, or other side effects is left unverified unless you approve it.

## Common questions

**Will it rip out the tooling I already have?**

Not without saying so. Existing tools are either preserved or replaced for a stated reason, and the reason lands in the proposal before anything changes. The proposal is the whole control point: the agent investigates, recommends one coherent setup, and waits. If you want a specific tool kept, say so at that step rather than after.

**My language isn't JavaScript, TypeScript, React or Go. Does it skip me?**

No. Those four ship with curated rule baselines aimed at the failure modes agents actually produce, so the proposal for them is concrete out of the box. For Ruby, C#, Rust and anything else, the agent researches the currently maintained tools and the exact rules, then builds the equivalent proposal. The output shape is the same; what differs is whether the recommendation came from a bundled baseline or from research the agent did in front of you. Research is worth reading more carefully than a baseline.

**Why are the pre-commit hooks so thin? I wanted the full suite to run.**

Because a slow hook gets bypassed, and a bypassed hook guards nothing. The skill deliberately splits fast local feedback from the complete gate: hooks stay quick, CI owns the full run, and the boundary between them is made visible rather than left implicit. If you genuinely want the whole suite locally, ask for it in the proposal — it is a choice, not a prohibition.

**It said it couldn't verify part of what it set up.**

That is the skill being honest rather than failing. Verification is proportionate: commands get run and representative failures get demonstrated safely, but anything needing a commit, a merge, an install, or another real side effect is left unverified unless you approve it. A report that names an unverified path is more useful than one that claims a green CI run it never triggered. The same applies to failures that were already there before it started: those get reported, not quietly absorbed.

**Why do the security scans run on pre-commit when other slow checks get pushed to CI?**

Because the point is to catch the problem before it lands in history, where a leaked secret is already leaked. Both tools scan only staged files: Gitleaks is a single fast binary, and Semgrep uses committed rules with no network calls. The hook's runtime is measured during setup. If Semgrep goes over budget, the slowest rule packs move to CI and the rest stay in the hook.

**How is this different from `setup-inconvenient-skills`?**

Different subject. [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) configures what the *skills* need — the issue tracker, the triage labels, the domain-doc layout — and then invokes this one. `guardrails` configures what the *project* needs: lint, format, tests, reproducible install, dependency upkeep, CI, hooks. Running the setup skill gets you both. Run `guardrails` on its own when only the quality strategy is changing.

**When do I run it again?**

When the stack changes or the quality strategy does: a new language in the repo, a formatter swap, a move from ad-hoc scripts to a task runner, a CI provider change. [retro](https://aihero.dev/skills-retro) is the other common route in — when a session's finding turns out to be "this repo has no baseline at all", that is a `guardrails` run rather than one more lint rule.

**Does the Bulletproof React package come as standard on a React app?**

No. It is offered as an explicit choice, and only for a new React application. Feature boundaries, import direction, state and API conventions and testing posture are opinionated enough that inheriting them by accident would be worse than not having them. Decline it and the rest of the proposal stands unchanged.

## It's working if

- The approved lint and format commands cover every detected ecosystem, or the report names a researched coverage gap.
- Existing tools were preserved or replaced for a stated reason.
- Local hooks are fast, CI owns the complete gate, and each boundary is visible.
- A fresh checkout has a defined locked setup-and-check path, even when that path could not be exercised safely during setup.
- Generated code and dependency updates have clear commands and ownership when the project uses them.
- When security scanning was accepted, a staged vulnerable pattern or fake secret is blocked at commit with a message saying what to do instead.
- Pre-existing failures and unverified behavior are reported rather than hidden.

## Where it fits

`guardrails` is a run-once setup, repeated when the stack or quality strategy changes. [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) invokes it after recording repository configuration, then invokes [verification](https://aihero.dev/skills-verification) against the resulting launch and check commands. Downstream skills such as [implement](https://aihero.dev/skills-implement) work inside the approved guardrails. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) maps the full collection.
