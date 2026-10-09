Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=retro
```

```bash
npx skills update retro
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/retro)

## What it does

`retro` looks back over a coding session and suggests improvements to the agent's **environment**, so the next run goes better. It reads the session's own record — the current one by default, or one you point it at in the session logs — finds the moments the agent struggled, and hands you a list of candidate fixes, most severe first.

It changes the environment, not the code. The bug the agent shipped, the file it took twenty tool calls to find, the rule the reviewer missed: `retro` doesn't fix any of them in place. It asks what about the repo let them happen, and proposes the check, the pointer, or the standard that stops them happening again. It also only proposes; nothing changes until you pick a candidate.

## When to reach for it

You invoke this by typing `/retro` — the agent won't reach for it on its own.

Reach for it at the end of a session that felt harder than it should have: the agent went looking for something for too long, made a mistake a machine could have caught, or needed information it had no way to get. A smooth session has little to teach; a painful one is where the findings are. If what you want is a verdict on the code the session produced, use [code-review](https://aihero.dev/skills-code-review) instead.

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

Before any rule gets written, the violation is classified. A **mechanical** one — a banned API, an import shape, a file-location rule — gets a deterministic check, because a check can fail and a sentence in a standards file can't. The check is usually a rule the repo's linter already ships, switched on. Security and bug patterns, and patterns in files the linter never reads, such as CI workflows and Dockerfiles, become Semgrep rules. Only genuine judgement calls, the kind no linter could ever enforce, become prose. A repo with no guardrail at all (no pre-commit hook, no CI job running lint, typecheck, and tests) is reported as a finding in its own right.

## Common questions

**Does it write the lint rule itself, or wait for a yes? Can I wire it to run after every session?**

It waits. `retro` only proposes; nothing changes until you pick a candidate, so there's no hand-editing and no auto-applied hook either. That is deliberate: deciding what deserves a permanent check takes judgement, so the skill stays human-in-the-loop and user-invoked. You can chain it after every implementation run, but a smooth session has little to teach, and running it on every one mostly produces rules nobody needed. There is no dry-run mode: a proposed check is built like any other code, so try it against the repo before you let it block merges.

**Won't this pile up lint rules forever? Does it ever suggest removing one?**

Partly, and this is its weakest spot. The removal side it has covers prose: no-ops in steering files, and steering in `AGENTS.md` or `CLAUDE.md` that belongs in standards or a check. Those it will flag for deletion when the files are large, judged against the session it is reading, so treat each one as a candidate for the deletion test rather than a verdict. It does not audit the lint rules, hooks, or CI jobs it proposed last month. It sees one session, so it can't tell you a rule has gone noisy or outlived the bug that justified it. Pruning checks is still your job; a rule that fires constantly on good code is the cue.

**Won't it just invent generic advice to fill its categories?**

That's the sharpest critique it gets: once the job is finished, the agent tends to forget the struggles from the middle of the session and invent generic advice to satisfy the categories. The defence is that every candidate has to come from the session's own record, so the advice is specific to that session. That cuts both ways: it rarely hallucinates something irrelevant, but it can over-index on whatever this one session happened to be about. Discard any candidate you can't trace to a specific moment. Treat the severity order as a first draft too: a quiet, expensive mistake can rank below a loud, cheap one.

**My session is long. Run it now, or start fresh?**

By default it reviews the current session, which is the best case: the struggles are still in the context window. If the session has drifted out of the [smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone) already, clear and point a fresh `/retro` at the previous session in the session logs instead.

**The agent keeps making the same mistake. Should I add a line to `CLAUDE.md`?**

Usually not, and that's the most common place `retro` pushes back. A line in `CLAUDE.md` is loaded into every session, dilutes everything else in the file, and drifts as the code changes. If the mistake is mechanical, the fix is a check that fails. If it's a judgement call, it goes in the coding standards the reviewer reads. `AGENTS.md` and `CLAUDE.md` are for navigation pointers, and little else. For the same reason `retro` is not a memory system: it doesn't store what happened, it changes the environment so it can't happen again.

**My setup mentions `CODING_STANDARDS.md` and I don't have one. Where does it come from?**

Nothing ships the file. The first time a session turns up a judgement-call rule for the reviewer, `retro` proposes starting it, and once you accept, [code-review](https://aihero.dev/skills-code-review) reads it from then on. Any other standards doc you already keep, such as `CONTRIBUTING.md`, works the same way.

**How is it different from `improve-codebase-architecture` or `guardrails`?**

The input, and the target. [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) needs nothing but the code and looks for structural improvements to it. [guardrails](https://aihero.dev/skills-guardrails) needs nothing but the project and proposes a whole quality baseline from scratch. `retro` needs a session history: it starts from what actually went wrong and works back to the environment change that prevents it, which is often a single check rather than a baseline. When the answer turns out to be "this repo has no baseline at all", `retro` hands you over to `guardrails`.

## It's working if

- Every candidate points back to a specific moment in the session, not a generic best practice.
- Repeat mistakes turn into failing checks, and your `AGENTS.md` gets shorter over time rather than longer.
- A missing check that already existed but sat unwired shows up as the finding, rather than a proposal to build a new one.
- The next session on the same kind of task finds its way faster.

## Where it fits

`retro` is the last step of the main chain, where the flow looks back at itself:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review → verification → retro
```

Run it after a build worth learning from, in the same session or pointed at that session's log. A smooth build can skip it.

- [code-review](https://aihero.dev/skills-code-review) is the reviewer agent `retro` most often tunes: new coding standards land where its Standards axis reads them.
- [guardrails](https://aihero.dev/skills-guardrails) is where a finding goes when the gap is the whole baseline rather than one check.
- [writing-for-agents](https://aihero.dev/skills-writing-for-agents) sets the writing style for every steering file and skill `retro` proposes, and `retro` loads it before it starts.

[ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes across the whole set when you are unsure which skill the situation wants.
