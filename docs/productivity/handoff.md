Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=handoff
```

```bash
npx skills update handoff
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/handoff)

## What it does

`handoff` compacts the current conversation into a **handoff document** — a single write-up a fresh agent can read to pick up the work where you left off.

It does **not** re-state what already lives elsewhere. Anything captured in a spec, plan, ADR, issue, commit, or diff is referenced by path or URL, never copied. The document carries only the live thread — what you were doing, why, and what's next — and it's saved to your OS's temporary directory, not into the workspace, so it never becomes another artifact to maintain.

## When to reach for it

You invoke this by typing `/handoff` — the agent won't reach for it on its own. Pass a note about what the next session is for and the document is tailored to it.

Reach for this when a conversation has gone long enough that its context is at risk — you're near a context limit, wrapping for the day, or deliberately handing the work to another agent — and you want the thread preserved without dragging the whole transcript along.

## What the document carries

- **The live thread** — what's in flight and why, in the conversation's own terms, minus anything already written down elsewhere.
- **Suggested skills** — a pointer to the skills the next agent should reach for to continue.
- **References, not copies** — links and paths to the specs, plans, ADRs, issues, and diffs that hold the settled detail.
- **Redacted secrets** — API keys, passwords, and PII stripped before the document is written.

The idea to hold onto is **compaction**: a handoff is the conversation squeezed down to just its resumable core, so a fresh agent inherits the momentum, not the noise.

## Common questions

**Handoff or compact?**
`/compact` unless something is travelling. Staying on the same task is a compact, not a handoff: same harness, same directory, and you need to stay in the loop is where the phase-boundary tree lands most days. `/handoff`'s advantage is not that it summarises better; it's that the result is a file you can carry somewhere `/compact` can't reach.

**So what's the actual difference between compact, clear and handoff?**
Three different things being preserved. `/compact` compresses this context and keeps you going in a fresh window: intent survives. `/clear` empties the window and starts from nothing: correct when everything behind you is disposable, and one-way if it isn't. `/handoff` writes a portable file: the work survives the move to somewhere else. Note that all three turn a **[primary source](https://www.aihero.dev/ai-coding-dictionary/primary-source)** (the conversation as it happened) into a **[secondary source](https://www.aihero.dev/ai-coding-dictionary/secondary-source)** (a summary of it). Continuing is the only move that doesn't, which is why it's the first one to rule out.

**Where did my handoff file go?**
The temp directory, which is the most-reported friction with the skill. The skill resolves it as `$TMPDIR`, else `/tmp` (`%TEMP%` on Windows), but the paths are long. Ask for the path back and keep it before you move on. Temp is deliberate: a handoff is a transit document, not an artifact you maintain. It is not a durable one either; see the next question.

**My handoff vanished between sessions.**
Some environments clear temp between sessions (Codex is the reported case), and `/private/tmp` goes on reboot. If the next session isn't starting within the hour, or is starting under a different harness, copy the file somewhere durable yourself as soon as it's written. The same applies to anything the document *points at*: a dispatch that references other files in temp is a dispatch the next agent can't follow.

**How do I actually hand it to the next agent?**
Open the fresh session and point it at the path: read this file, then continue. Point at the file rather than pasting the summary into a shell command: a summary containing backticks or `$(...)` gets mangled when it's interpolated into `claude "<summary>"`, and the usual failure is silent truncation rather than an error, so the new agent starts with a quietly incomplete brief.

**Is this the same as `/branch`, `--fork-session`, or the built-in `/handoff`?**
Analogous, not identical, and `/branch` isn't a shipped skill here; `/handoff` is the canonical name. A fork inherits an exact copy of the context; this skill produces a *targeted* compression aimed at a stated next task, in a file. Where a fork will do (same machine, same harness, same directory), a fork is less work. The file wins the moment the destination is somewhere the fork can't go.

**When does something belong in `CLAUDE.md` instead?**
Ask whether it's true next month. `CLAUDE.md` is standing context about the project, loaded into every session whether it's relevant or not. A handoff is about one piece of work in flight and is dead once that work lands. Facts that keep getting re-explained are a `CLAUDE.md` problem; a half-finished task is a handoff.

**It captures the what, not the why.**
A fair and repeated criticism. Two things help. Pass the argument (tell it what the next session is for) so the reasoning that bears on *that* is kept rather than flattened. And watch for confident claims the session never actually verified: "X isn't built", "Y is done". The next agent treats the document as a contract and will not re-check it, so a belief written as a fact becomes a false premise for everything that follows. Read the document before you hand it over, and downgrade anything you only assumed.

**Why is it a skill rather than a slash command?**
Both work; they suit different situations. As a skill it ships and updates through the same install path as everything else here, which is what makes it shareable; the constraint that the agent won't fire it itself is set by its frontmatter rather than by the mechanism.

## Where it fits

`handoff` is a reach-for-it-anytime standalone — it sits at the seam between two sessions rather than inside a build chain. It pairs naturally with the artifact-producing skills whose output it points at: [to-spec](https://aihero.dev/skills-to-spec), because a finished spec is exactly the kind of settled detail a handoff references instead of repeating. When you're unsure which skill fits the moment, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
