Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=retro
```

```bash
npx skills update retro
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/retro)

## What it does

`retro` looks back over agent work and proposes improvements to the agent's **environment**, so the next run goes better. Its standard mode reviews one coding session across navigation, checks, standards, steering, tooling, and information access. Its time mode measures where time goes across a session or a longer history.

It proposes environment changes, not application fixes, and leaves implementation for a separate request. The bug the agent shipped, the file it took twenty tool calls to find, the rule the reviewer missed: `retro` asks what about the environment let them happen. A costly command is not automatically a bad check, and a long runtime alone does not prove a cause.

## When to reach for it

You invoke this by typing `/retro`, and the agent won't reach for it on its own.

Reach for it at the end of a session that felt harder than it should have, or when recurring waits deserve measurement rather than another guess at what is slow.

| What you want to improve | Reach for |
| --- | --- |
| The environment that made a specific session slow or error-prone | `/retro`, or `/retro <session>` |
| Where agent time goes across this repo's history | `/retro time`, with a session or period if you want a different scope |
| The code's compliance with standards and the spec | [code-review](https://aihero.dev/skills-code-review) |
| The codebase's module structure, without needing a session history | [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) |
| A missing lint, test, CI, or hook baseline across the repo | [guardrails](https://aihero.dev/skills-guardrails) |

## Prerequisites

The input is a session record, not just a diff. Standard mode defaults to the current session; for an older one, name an accessible session or point it at the logs. Time mode needs accessible historical records with timing evidence, and reports gaps rather than treating missing time as zero.

The workflow applies to omp, Claude Code, Codex CLI, and other harnesses with accessible session evidence. It defaults to the running harness; an explicitly selected session from another harness overrides that source. AgentTrace is optional. When available, reports use `--source` with the verified harness identifier rather than mixing agents. Harness-specific missing fields remain evidence gaps, not invented timings.

## One retrospective, two scopes

| Invocation | Scope and purpose |
| --- | --- |
| `/retro` | The current session, across all retrospective categories |
| `/retro <session>` | A specified session, with the same general scope |
| `/retro time` | A full measured time audit of the current repo's trailing 90 days, including subagents |
| `/retro time <session>` | A measured time audit of the specified session |
| `/retro time` with an explicit period | A measured time audit over that period instead of the default window |

An explicit natural-language request for measured time analysis selects time mode too. Simply saying a session felt slow does not turn a standard retrospective into a full history audit.

Both modes share **diagnostic knowledge**: repeated round trips, approval waits, shell startup, polling, dependency and lifecycle problems, cache behavior, and other explanations to check against evidence. Standard retro loads what the session needs and may use scoped AgentTrace evidence. It does not require a full ledger, a history scan, or benchmarks just to explain a local struggle.

Time mode earns the extra work with **accounted time**. It distinguishes command execution from elapsed latency, cumulative call-time from occupied wall-clock time, and overlap from actual blocking dependencies. It connects observed work to instruction costs where the evidence supports that connection, then compares safe, equivalent alternatives where possible. It stays focused on performance rather than repeating every general retrospective category. A missing measurement remains an explicit gap, not a claimed speedup.

Findings cite evidence, separate cause confidence from impact confidence, and name the cheapest proposed change, its validation, and its tradeoff. Candidates are ordered by severity; the time ledger ranks supported timing impact separately. A cheap check can prevent a severe mistake, and a slow check can still be necessary.

## Where the findings land

Each candidate belongs to one category, and the category decides where the fix goes:

| What went wrong in the session | Fix it with |
| --- | --- |
| The agent took a long time to find a file or fact | A **navigation pointer** from a file it already reads |
| It made a mistake a tool could have caught | An **automated check**: lint rule, type, test, pre-commit hook, CI job |
| The repo has no lint, typecheck, or test baseline at all | A [guardrails](https://aihero.dev/skills-guardrails) run, which proposes and verifies the whole baseline in one pass |
| The reviewer missed a judgement-call mistake | A rule in `CODING_STANDARDS.md` for the reviewer agent |
| `AGENTS.md` or `CLAUDE.md` is large | Move its steering out, into standards or checks |
| A tool call was expensive for what it returned | Streamline the tool, or replace it |
| A steering file is full of lines that change nothing | Delete the **no-ops** |
| The agent needed information it couldn't reach | Widen its access: tee the dev server log to a file, give read-only access to a service |

The leading idea is that standards belong to the **reviewer**, not the implementer. The implementing agent carries the most context pressure: it explores, writes code, and debugs failures. The reviewing agent receives a diff and nothing else. So a new rule goes where there is room to apply it, in review, and never in `AGENTS.md`, which loads into every session's context window whether it's relevant or not.

Before any rule gets written, the violation is classified. A **mechanical** one (a banned API, an import shape, a file-location rule) gets a deterministic check, because a check can fail and a sentence in a standards file can't. The check is usually a rule the repo's linter already ships, switched on. Security and bug patterns, and patterns in files the linter never reads, such as CI workflows and Dockerfiles, become Semgrep rules. Only genuine judgement calls, the kind no linter could ever enforce, become prose. A repo with no guardrail at all (no pre-commit hook, no CI job running lint, typecheck, and tests) is reported as a finding in its own right.

## Common questions

**Does it write the lint rule itself, or wait for a yes? Can I wire it to run after every session?**

It waits. `retro` only proposes environment changes; nothing is applied until you choose a candidate and request implementation. It stays human-in-the-loop and user-invoked. Time mode can run safe, non-mutating measurements, but it is not an optimization patch. Standard mode suits a session worth learning from; time mode suits recurring costs you want measured. A proposed check still needs validation against the repo before it blocks merges.

**Won't this pile up lint rules forever? Does it ever suggest removing one?**

Yes, it can propose removal or clarification, not just additions. Standard retro looks for no-op steering and rules in `AGENTS.md` or `CLAUDE.md` that belong in review standards or deterministic checks. Time mode can inspect historical lint, hook, and CI costs across the requested period and identify expensive or redundant work. But runtime does not tell you whether a rule is noisy or useful: that needs evidence about false positives, failures caught, and required coverage. A recommendation to streamline a check must preserve its required behavior, not call skipped coverage a speedup.

**Does plain `/retro` get the diagnostics, or do I need time mode for that?**

Both get the same diagnostic knowledge. Plain `/retro` keeps all its categories and uses the relevant explanations and scoped evidence for the session. Choose time mode when you want measured accounting across the requested scope, instruction-cost analysis, and comparison of equivalent alternatives. The distinction is the work required and the question answered, not access to a better set of explanations.

**Do I need AgentTrace, and will it scan all my history for a normal retro?**

No to both. AgentTrace is optional and used only when available. Standard mode stays scoped to the session you selected. Time mode defaults to the current repo's trailing 90 days, including linked subagents, not every project on your machine; specify a session or period to change that scope. Its report tells you which records and timings were actually accessible.

**Is this tied to omp?**

No. Both modes use the selected harness's native history or exports, documented storage, and AgentTrace discovery where available. omp's archive API is an optional extra reference, not a prerequisite for Claude Code, Codex CLI, or other harnesses. A model name does not select the source: a Codex model running in omp still uses omp logs.

**Won't it just invent generic advice to fill its categories?**

Every candidate must be traceable to the session's records rather than invented to fill a category. Standard retro can still over-index on what one session happened to be about; time mode broadens the evidence but must disclose missing records and uncertainty. Discard any finding whose evidence does not support it. A high call-time total does not by itself prove a blocking dependency, a cause, or recoverable wall-clock savings.

**My session is long. Run it now, or start fresh?**

By default it reviews the current session, which is the best case: the struggles are still in the context window. If the session has drifted out of the [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone) already, clear and run `/retro <session>` from a fresh context instead. Use `/retro time <session>` when you want that session's measured time audit rather than a general retrospective.

**The agent keeps making the same mistake. Should I add a line to `CLAUDE.md`?**

Usually not, and that's the most common place `retro` pushes back. A line in `CLAUDE.md` is loaded into every session, dilutes everything else in the file, and drifts as the code changes. If the mistake is mechanical, the fix is a check that fails. If it's a judgement call, it goes in the coding standards the reviewer reads. `AGENTS.md` and `CLAUDE.md` are for navigation pointers, and little else. For the same reason `retro` is not a memory system: it doesn't store what happened, it changes the environment so it can't happen again.

**My setup mentions `CODING_STANDARDS.md` and I don't have one. Where does it come from?**

Nothing ships the file. The first time a session turns up a judgement-call rule for the reviewer, `retro` proposes starting it, and once you accept, [code-review](https://aihero.dev/skills-code-review) reads it from then on. Any other standards doc you already keep, such as `CONTRIBUTING.md`, works the same way.

**How is it different from `improve-codebase-architecture` or `guardrails`?**

The input, and the target. [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) needs nothing but the code and looks for structural improvements to it. [guardrails](https://aihero.dev/skills-guardrails) needs nothing but the project and proposes a whole quality baseline from scratch. `retro` starts from session evidence and works back to an environment change, often a single check rather than a baseline. Time mode adds measured performance analysis, not a general codebase survey. When the finding is "this repo has no baseline at all", `retro` hands you over to `guardrails`.

## It's working if

- Every candidate points back to session evidence, not a generic best practice.
- It proposes changes before implementation, with evidence, confidence, validation, and tradeoffs.
- Standard mode orders candidates by severity; time mode makes measured impact and missing timing evidence visible without confusing cost with severity.
- Repeat mistakes turn into failing checks, and your `AGENTS.md` gets shorter over time rather than longer.
- A missing check that already existed but sat unwired shows up as the finding, rather than a proposal to build a new one.
- The next session on the same kind of task finds its way faster.

## Where it fits

`retro` is the last step of the main chain, where the flow looks back at itself:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review → verify → retro
```

Run standard retro after a build worth learning from, in the same session or pointed at that session's log. Use time mode as periodic performance maintenance when recurring costs need a measured explanation.

- [code-review](https://aihero.dev/skills-code-review) is the reviewer agent `retro` most often tunes: new coding standards land where its Standards axis reads them.
- [guardrails](https://aihero.dev/skills-guardrails) is where a finding goes when the gap is the whole baseline rather than one check.
- [writing-for-agents](https://aihero.dev/skills-writing-for-agents) sets the writing style for every steering file and skill `retro` proposes, and `retro` loads it before it starts.

[ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes across the whole set when you are unsure which skill the situation wants.
