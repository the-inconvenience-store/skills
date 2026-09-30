Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=research
```

```bash
npx skills update research
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/research)

## What it does

`research` answers a question by reading the sources that own the answer and leaving a cited Markdown file behind. It works only from **primary sources** — official docs, source code, specs, first-party APIs — never a secondary write-up of them, so what it saves is traceable back to something authoritative rather than a summary of a summary.

## When to reach for it

Type `/research`, or the agent reaches for it automatically when a task turns into reading legwork.

Reach for it when the next step is *finding something out* — how an API behaves, what a spec actually says, whether a claim holds — and you'd rather not stall your own thread doing the reading. For sharpening a plan by interview instead of by reading, use [grilling](https://aihero.dev/skills-grilling); for exploring what to build with throwaway code, use [prototype](https://aihero.dev/skills-prototype).

## Delegated legwork

The defining move is that the reading runs as a **background agent**. You keep working; it goes off, follows each claim back to its primary source, and drops a single cited Markdown file into wherever the repo keeps such notes. Research is legwork you delegate, not thinking you outsource — you get back a document to react to, with its sources attached.

The delegation happens exactly once. The background agent is told to do the reading itself rather than spin up another researcher, because an agent handed these same instructions will otherwise fire them again and you end up paying for overlapping runs you can't see. The rule cuts the other way too: where delegation isn't available at all, the reading happens in-thread — an undelegatable run still owes you the file, not silence.

## Common questions

**It spawned a second research agent. Is that meant to happen?**

No, and this fork carries a guard against it. The original bug ([issue #530](https://github.com/mattpocock/skills/issues/530) upstream) was that the skill told its caller to spin up a background agent without restricting the agent type, so the agent it spawned was a `general-purpose` one holding the `Agent` tool and the same instructions, and fired them again. One reporter measured a single research task costing roughly 450k [tokens](https://www.aihero.dev/ai-coding-dictionary/token) across three overlapping runs, with the duplicate finishing half an hour later entirely out of view. It reproduced outside Claude Code too.

The skill here delegates exactly once: an agent that is already a background agent or [subagent](https://www.aihero.dev/ai-coding-dictionary/subagent) does the research itself, and every spawned prompt ends with an instruction not to call `research` again or spawn further agents. That also closes the opposite failure, where global instructions forbidding re-delegation left the background agent politely declining the task and the skill quietly doing nothing: an undelegatable run still has to produce the file. The guard is instruction-level rather than structural, so it is still worth glancing at your background task list after invoking.

**Where should the file live, and should I commit it?**

The skill puts the file where the repo already keeps notes and does not have an opinion beyond that. The community one is fairly settled: ADRs are kept, research files are not. The sharpest version of it, from a Discord thread on exactly this question: "ADRs yes. Everything else archive or delete after done. It otherwise becomes cruft of work and can poison future repo reads if you've drifted away from the spec/research." A research file records what was true on the day it was written, so a stale one is worse than none. On balance these artifacts don't really belong in git, and there is no canonical home for them: people use Obsidian, a separate knowledge repo, or the issue tracker instead.

**What counts as a "high-trust" primary source, and who decides?**

The [model](https://www.aihero.dev/ai-coding-dictionary/model) does. The skill names the *kinds* of source that qualify (official docs, source code, specs, first-party APIs), and there is no allowlist, no domain gate, and no verification pass. This was the loudest objection when the skill was first proposed and it has never been answered publicly: "Five research subagents pointed at junk just gives you five confident wrong answers faster. How are you gating what counts as high-trust sources?" The mitigation you actually have is the citation on each claim. Follow two or three of them. If they land on a summary of the thing rather than the thing, the run failed at its one job.

**Does a later session reuse what an earlier run found?**

No. Nothing auto-loads a past research file; it is a document sitting in the repo until a human or a skill points at it. This was raised early as the strongest challenge to the design: "the value's the markdown becoming context the agent re-reads later, not the fetch itself. A write-once dead file is just a fancy search." The shipped skill does not solve it. In practice the file earns its keep by being fed into the next step deliberately: attach it to a spec, quote it into a grilling session, point a [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket) at it.

**Why not just ask the agent to go read the docs?**

You can, and a two-line prompt saying exactly that was the practice this skill replaced. Two things the skill buys over the prompt: it runs in the background so your session keeps its [context](https://www.aihero.dev/ai-coding-dictionary/context) clean, and the primary-source constraint and the cited-file output come out the same way every time rather than however you happened to phrase it. Against a [harness](https://www.aihero.dev/ai-coding-dictionary/harness)'s own deep-research mode, the difference is the artifact and the source discipline, not the search. If a two-line prompt gets you what you need on a small question, use the two-line prompt.

**When does it stop reading?**

There is no stopping criterion in the skill, and this shows up as two complaints that look opposite but are the same gap: agents that go far too deep, and agents that cover a topic broadly while missing the one specific detail that mattered. One practitioner put it as "deep-research skills are a bit too deep sometimes. And telling an agent to research usually results in missing crucial details." Scoping is on you. A narrow, answerable question (one API, one behaviour, one version claim) comes back far better than "research X".

**`/wayfinder` created research tickets. Do I resolve those myself?**

No, it fires them for you. A charting session spawns a `/research` subagent per research ticket and burns them down in parallel, capturing findings on a throwaway `research/<name>` branch with a [context pointer](https://www.aihero.dev/ai-coding-dictionary/context-pointer) from the ticket. Research tickets are the one exception to wayfinder's one-ticket-per-session rule, because they are [AFK](https://www.aihero.dev/ai-coding-dictionary/afk): nothing waits on you. Two known snags with those branches: the subagent has been seen opening a draft PR from a branch that is never meant to merge ([issue #576](https://github.com/mattpocock/skills/issues/576) upstream), and deleting the branch later breaks the context pointers the tickets hold.

## Where it fits

A reach-for-it-anytime standalone that feeds the thinking skills: the file it produces is something to grill, plan, or design against, so it sits upstream of work like [grilling](https://aihero.dev/skills-grilling) and [to-spec](https://aihero.dev/skills-to-spec) rather than in the build chain. For the whole map, see [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
