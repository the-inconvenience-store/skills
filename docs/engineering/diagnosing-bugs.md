Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=diagnosing-bugs
```

```bash
npx skills update diagnosing-bugs
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/diagnosing-bugs)

## What it does

`diagnosing-bugs` runs a disciplined diagnosis loop for hard bugs and performance regressions: build a repro, minimise it, rank hypotheses, instrument, fix with a regression test, then prove the original path on the real surface.

It refuses to hypothesise before you have a **tight feedback loop** — one runnable command that already goes red on *this* bug. Existing project verification instructions may supply the launch and driving route, but they count only after the loop asserts the exact symptom. No red-capable loop, no diagnosis.

## When to reach for it

Type `/diagnosing-bugs`, or the agent reaches for it automatically when a task fits — it fires on "diagnose" / "debug this", or when you report something broken, throwing, failing, or slow.

Reach for it on the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. For a quick throwaway to sanity-check a design question rather than chase a defect, use [prototype](https://aihero.dev/skills-prototype) instead.

## The tight loop is the skill

Everything else — bisection, hypothesis-testing, instrumentation — is mechanical once you have the signal. The skill always applies Fix Root Causes, Build the Lever, and Prove It Works, then proactively scans the remaining principle triggers against the symptom, suspected mechanism, and intended fix. It spends disproportionate effort constructing a command that drives the actual bug path and asserts the user's exact symptom, tightening that loop until it is fast, deterministic, and agent-runnable.

It gives you a ladder of ways to build the loop — existing [verification](https://aihero.dev/skills-verification) instructions, a failing test, curl script, CLI diff, headless browser, replayed trace, throwaway harness, fuzz loop, `git bisect run`, or differential run — and, only as a last resort, a human-in-the-loop bash script. For non-deterministic bugs the target is a higher reproduction rate: loop the trigger and add stress until the flake is debuggable.

## It's working if

- It builds and runs a repro command *before* theorising — and shows the invocation and its redacted output.
- The loop asserts the symptom you actually reported, not a nearby failure.
- Hypotheses arrive as a ranked, falsifiable list shown to you before any are tested.
- Debug instrumentation is tagged (`[DEBUG-...]`) and grepped away before it declares done.
- Captured artifacts quote only the lines that carry the signal; credentials stay in environment variables.
- The regression test passes and the original real-surface path reports `VERIFIED`.

## Where it fits

`diagnosing-bugs` is a reach-for-it-anytime standalone — you drop into it the moment something is broken and leave only after the regression test and original public path pass. It uses [engineering-principles](https://aihero.dev/skills-engineering-principles) for the shared root-cause and proof rules, and [verification](https://aihero.dev/skills-verification) for the final real-surface verdict. When the real finding is that there's no good seam to lock the bug down, that's your cue to run [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) yourself afterwards. When you're unsure which skill fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
