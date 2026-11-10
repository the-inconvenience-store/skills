Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=ask-inconvenient
```

```bash
npx skills update ask-inconvenient
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ask-inconvenient)

## What it does

`ask-inconvenient` is the router over the skills in this repo. You describe the situation you're in; it names the skill or flow that fits, the order to run it, and where your decisions sit. It recommends a next command rather than starting the work for you.

It **does no work itself**. It doesn't grill, write a spec, or fix anything; it only orients. It exists for the user-invoked skills above all: nothing fires those for you, so `ask-inconvenient` is the memory you offload that to. It also maps model-invoked disciplines such as [verification](https://aihero.dev/skills-verification) and the three vocabulary layers: [domain-modeling](https://aihero.dev/skills-domain-modeling), [codebase-design](https://aihero.dev/skills-codebase-design), and [engineering-principles](https://aihero.dev/skills-engineering-principles).

## When to reach for it

You invoke this by typing `/ask-inconvenient`; the agent won't reach for it on its own.

| Your situation | What the router gives back |
| --- | --- |
| An idea, and no idea where to start | The head of the main flow, including whether a spec earns its cost |
| Incoming bugs and requests | The [triage](https://aihero.dev/skills-triage) on-ramp, not another triage pass over tickets you generated yourself |
| Two skills that look interchangeable | A concrete boundary: working directory or none, single-session or multi-session planning |
| A long session and a context decision | The ordered choices at a phase boundary |
| A skill you have already picked | No extra step needed. Invoke that skill directly. |

## Prerequisites

The router does not install the skills it recommends. Install the ones you intend to use; this is a hand-maintained map of this repo, not a scan of every skill on your machine. Tracker-dependent routes also need [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills) to configure the repo first.

Local development installs also expose the WIP [clean-copy](https://github.com/the-inconvenience-store/skills/tree/main/in-progress/clean-copy) standalone for cutting unnecessary interface text. The router marks it as a draft; it is not included in the plugin.

## Flows, not just skills

The idea `ask-inconvenient` gives you to think with is the **flow**: a path *through* the skills rather than a single one. Before the first engineering flow, [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills) records repository configuration, invokes [guardrails](https://aihero.dev/skills-guardrails), then creates the project route through [verification](https://aihero.dev/skills-verification). Most feature work then runs along one main flow: grill → spec → tickets → implement through TDD → review → real-surface verification. On-ramps merge bugs, incoming requests, and codebase-health work onto it; standalones remain available when only one discipline is needed.

The main flow branches when a question needs a runnable [prototype](https://aihero.dev/skills-prototype), or when a build is small enough to skip the spec-and-tickets step. Multi-session builds can use [implement](https://aihero.dev/skills-implement) per ticket or [implement-spec](https://aihero.dev/skills-implement-spec) across the whole graph. Afterward, [retro](https://aihero.dev/skills-retro) feeds the build's lessons back into the agent's environment. Separately, [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) surveys for deepening opportunities that can re-enter the flow as new ideas.

## Phase boundaries

The router makes the context decision **at a phase boundary**, not halfway through a phase. Work down the choices in order:

| Option | Take it when |
| --- | --- |
| **Continue** | The next phase needs this conversation verbatim, or there is room to keep reasoning sharply |
| **`/clear`** | The current context is irrelevant to the next task |
| **[handoff](https://aihero.dev/skills-handoff)** | Work must travel to another harness, directory, colleague, or a side task forked mid-phase |
| **Subagent** | A tightly scoped task can run without your steering |
| **`/compact`** | Relevant context must stay, but none of the more precise choices fits |

Continue preserves the conversation as a primary source; handoff buys portability, not a general-purpose context reset. Mid-phase, continue or split the remaining work into subagents.

## Common questions

**Isn't there just a list of the skills in the right order?**

People keep asking for one in the README. This skill is that list: it is what it exists for. A static table would say `wayfinder → to-spec → to-tickets → implement → code-review → retro` and be wrong for most situations, because the interesting parts are the branches: is there a codebase, does the build span sessions, can this question be settled by talking. The honest cost is that the router is hand-maintained and lags the repo. `/grilling` shipped long before the router named it.

**It told me half the skills aren't installed.**

A known bug, unfixed. Most of the skills the router routes you through set `disable-model-invocation: true`, which means the harness leaves them out of the skill list it injects into the agent's context. The agent reads that list as exhaustive and reports them missing. One reported session had it declare the whole spec-and-tickets flow absent and reroute to bare `/grilling` and `/tdd`. Sixteen of the plugin's thirty skills carry the flag, so this is the common case rather than an edge. They are installed. Type the slash command anyway, or check `.claude-plugin/plugin.json`, which is the authority on what is present.

**It described a skill's behaviour, and the skill doesn't do that.**

A reported upstream failure came from trusting the router's one-line summaries without reading the skills. Skipping [to-spec](https://aihero.dev/skills-to-spec) on that basis lost its seam check and undercounted the work. This fork explicitly requires the router to read a skill's `SKILL.md` before describing its behavior or recommending that you skip it. Look for that read in the trace. Where the summary and the source disagree, the skill is authoritative. Questions the map does not cover, such as whether to use [plan mode](https://www.aihero.dev/ai-coding-dictionary/agent-mode), remain model inference rather than documented routing.

**Why is it prose instead of a numbered checklist?**

A fair complaint, filed as an open issue arguing that most of the routing is deterministic and the narrative makes it hard to scan. Nothing stops you asking for the compressed form: "just give me the sequence" gets you the sequence. What the prose is carrying is the conditional half: the branches, where a human decision is expected, and where to clear or compact between steps. A flat checklist drops exactly that.

**Can it route over my own skills, or another author's?**

No. Three separate proposals have asked for a router that reads your local `skills/` directory and recommends from whatever is installed. `ask-inconvenient` is not that. It is a map of one set, maintained by hand, and it knows nothing about skills you wrote or installed from elsewhere.

**It told me to edit a SKILL.md.**

That advice is often correct and rarely durable. Someone asked it how to make [implement](https://aihero.dev/skills-implement) close tickets, got told to add a line to the skill, and immediately spotted the problem: `npx skills update` overwrites the file, and the plugin install is read-only. Put standing behaviour in your own `CLAUDE.md` or `AGENTS.md`, or say it in the invocation. Prompt-level adaptations survive updates: pointing the flow at Linear instead of GitHub, or asking it which open tickets could run in parallel, are both things people do this way.

**It named a skill I don't have, or missed one I do.**

Check the changelog for a rename before assuming it is gone. `writing-great-skills` became [writing-for-agents](https://aihero.dev/skills-writing-for-agents) with no alias, `to-prd` became [to-spec](https://aihero.dev/skills-to-spec), `pathfinder` became [wayfinder](https://aihero.dev/skills-wayfinder), and this fork renames two more: `ask-matt` is `ask-inconvenient` and `setup-matt-pocock-skills` is [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills). Four skills were retired outright into the skills that absorbed them: `ubiquitous-language`, `design-an-interface`, `qa` and `request-refactor-plan`. `resolving-merge-conflicts` was removed in v1.5.0 with nothing replacing it. The reverse case is the router's own lag, above.

## It's working if

- It ends with what to type next, rather than starting the recommended work.
- The route names the relevant human decisions and context boundaries, not just a list of skills.
- It distinguishes close alternatives with a concrete reason.
- Load-bearing claims about another skill are preceded by reading that skill's `SKILL.md`.

## Where it fits

`ask-inconvenient` is the **router**, the standalone map that sits over the whole set. It is the node every other docs page links back to as [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient), so it never sits *in* a chain; it points *into* every chain. From here you'll most often land on [grill-with-docs](https://aihero.dev/skills-grill-with-docs), the head of the main flow, or [triage](https://aihero.dev/skills-triage), the on-ramp for work you didn't create. It also knows the standalone paths through [to-questionnaire](https://aihero.dev/skills-to-questionnaire), [wizard](https://aihero.dev/skills-wizard), and [wait-what](https://aihero.dev/skills-wait-what). When even the router's own picture is stale, its [Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ask-inconvenient) is the map of record.
