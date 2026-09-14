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

## Where it fits

A reach-for-it-anytime standalone that feeds the thinking skills: the file it produces is something to grill, plan, or design against, so it sits upstream of work like [grilling](https://aihero.dev/skills-grilling) and [to-spec](https://aihero.dev/skills-to-spec) rather than in the build chain. For the whole map, see [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
