Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=setup-project
```

```bash
npx skills update setup-project
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/setup-project)

## What it does

`setup-project` installs a repo's **guardrails** — the lint rules, formatter, file-structure conventions, and hooks that keep agent-written code readable and maintainable without a human reading every line of it.

It finishes by breaking things on purpose. A lint config that never fails on a violation is worth nothing, and a config that fails on everything gets deleted within a week; both are silent until someone trips over them. So the skill's completion criterion is not "the config is written" — it is that you have watched every rule group and every hook go pass → fail on a real violation → pass again. Nothing is reported as installed that hasn't been observed firing.

## When to reach for it

You invoke this by typing `/setup-project` — the agent won't reach for it on its own.

Reach for it when you're starting a TypeScript, React, Next.js, React Native, Expo, or Go project, or when an existing one keeps accumulating code you don't want: 800-line components, `bg-[#3b82f6]` instead of a theme token, `as unknown as`, `// TODO: handle this properly`, `../../../utils`, `panic("not implemented")`, an error compared with `==` instead of `errors.Is`. Re-run it when the stack changes — a new framework, Tailwind arriving, a monorepo splitting out — and edit the lint config directly for anything smaller.

For the config the *other* skills in this repo read — issue tracker, triage labels, domain docs — you want [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) instead. The two are unrelated: one configures your repo, the other configures the skills.

## Prerequisites

A Node project with a `package.json`. It works on an empty repo and on a large existing one, but the two go differently: on an existing codebase, rules that would fail hundreds of files get counted and surfaced as a decision rather than switched on quietly.

## The linter is the standard

The premise is that prose loses to config. A convention written in `CLAUDE.md` is something an agent may or may not attend to on any given turn; the same convention as a lint rule is something it cannot get past. So this skill's output is mostly `.oxlintrc.json`, and the documentation it writes deliberately covers only what config can't express — where a new feature goes, why imports flow one way, what a commit message looks like.

Two consequences follow, and both are stated up front rather than discovered later:

- **Everything blocks.** A finding that doesn't fail the build is one agents learn to scroll past. The only standing exception is the budget tier — complexity and file size — which are nudges rather than defects: a 520-line file is a signal to split, not a broken build.
- **Nothing is installed unasked.** The skill detects your stack first, then walks you through the choices one at a time, each led by its recommended answer. It never migrates an existing file tree without being told to.

Guardrails land at three distances, and the distance is what decides where a check belongs. Config — lint rules and the formatter — applies whenever anything runs. **Git hooks** are the outer gate: they fire once, on code you're claiming is finished, which is where the verdicts go. **Agent hooks** are the inner loop: they fire on every file edit your agent makes, so only work that's fast and correct on a half-written file goes there. That last tier is optional and off unless you ask, because it writes into your own `.claude/` or `.cursor/` rather than the repo. Formatting on edit is worth taking; linting on edit mostly isn't, because mid-refactor code is legitimately broken between edits and an error there sends the agent chasing a problem its next edit was about to fix. If your project has a code generator — sqlc, Prisma, buf, mockery — the guard worth having is one that blocks edits to generated output and tells the agent which source file to edit instead.

Language support is per-ecosystem, and a polyglot repo gets one config each. **TypeScript and React** run on [oxlint](https://oxc.rs/docs/guide/usage/linter), drawing on [anti-slop](https://github.com/dmmulroy/anti-slop) for type laundering, [react.doctor](https://www.react.doctor) for React correctness, [oxlint-tailwindcss](https://oxlint-tailwindcss.pages.dev) for design-system discipline, and [bulletproof-react](https://github.com/alan2207/bulletproof-react) for the file structure the import rules then enforce. **Go** runs on [golangci-lint](https://golangci-lint.run), with `cyclop` and `gocognit` measuring complexity two different ways, `depguard` holding the architecture, and `internal/` doing the work the compiler will do for free. Where your dependencies have documented anti-patterns and no linter covers them, the skill offers to write the rule — always as a proposal with the diagnostic message and a caught example, never installed on your behalf.

## It's working if

- A lint config lands for each language in the repo, and one command runs them all — wired into whatever already runs your typecheck or CI check.
- The final report names every rule that *doesn't* block and why, counts the violations it found and didn't fix rather than burying them, and says outright if a language in your repo isn't covered.
- Committing `// TODO: fix later`, a deep relative import, a hardcoded hex colour, or a `panic("not implemented")` fails — and you saw it fail during setup, not a week afterwards.
- `git commit -m "stuff"` is rejected; `git commit -m "fix(api): handle empty cursor"` isn't.

## Where it fits

`setup-project` is a **run-once setup**, re-run when the stack changes. Its neighbour is [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) — the same run-once posture, aimed at the skills rather than the repo, and worth doing in the same sitting. Downstream, everything that writes code lands inside the guardrails it installs: [implement](https://aihero.dev/skills-implement) and [tdd](https://aihero.dev/skills-tdd) hit the rules as they build, and [code-review](https://aihero.dev/skills-code-review) gets to spend its attention on design rather than on the mechanical faults a linter already caught. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
