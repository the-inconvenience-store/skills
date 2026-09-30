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

## Common questions

**It fires on quick questions where I just wanted a direct answer.**
This is the most-reported problem with the skill, and it is real. On GPT-5.6-Sol especially, users report it triggering on a plain description of a problem: "the model triggers the rather formal diagnosing-bugs skill instead. It then goes on to construct a reproduction scenario (often building a mock scenario with limited value) before giving me a response or suggestion. This results in considerable reply delays." Four separate people reported the same shape on [issue #578](https://github.com/mattpocock/skills/issues/578). The accepted fix is to start with a lighter approach and graduate to the heavier one only where the problem warrants it, but that change has not landed. The skill is calibrated against Claude Code's invocation behaviour; a [model](https://www.aihero.dev/ai-coding-dictionary/model) with a lower activation threshold over-fires it. Until it is graduated, the practical fix is to say what you want ("just answer this, don't diagnose") or to disable model invocation for it in your [harness](https://www.aihero.dev/ai-coding-dictionary/harness).

**Can I point it at a codebase and ask where the performance problems are?**
No. It diagnoses one failure you can already name. Its performance branch is for a regression with a symptom (establish a baseline measurement, then bisect, measure first and fix second), not for a proactive sweep. A skill for the proactive version was [proposed and closed](https://github.com/mattpocock/skills/issues/431); there is currently no skill for it.

**Does it stop and ask me before it writes the fix?**
No. Only Phase 3 has a human checkpoint: the ranked hypothesis list is shown to you before any is tested, and it proceeds on its own ranking if you are away. There is no gate between instrumentation and the fix, so the agent can start writing code before you have agreed with its root cause. [Issue #124](https://github.com/mattpocock/skills/issues/124) asks for that gate and is still open. If you want it, say so when you invoke the skill.

**I already ran `/triage` on this bug report. Is this the same work again?**
Partly, and neither skill admits it. As one reader put it: "Triage's step 3 is essentially a shallow, bounded instance of diagnosing-bugs Phase 1–2, but neither file mentions the other." Triage does a bounded "is this actually a bug, and what is the surface" pass; this skill does the thorough version. Running triage first is not wasted (its verification often gives you most of Phase 1's raw material), but expect to redo it properly here, and expect no cross-reference to tell you that.

**Will the repro output it pastes leak secrets?**
Less than it used to. The skill asks the agent to paste the invocation and its output, and to request artifacts like HAR files, log dumps, and core dumps, and credentials, tokens, cookies, and personal data ride along in all of those ([issue #674](https://github.com/mattpocock/skills/issues/674) upstream raised exactly this). This fork ships the redaction guardrail: a Redact section that comes before any phase, requiring every secret to be replaced with `<REDACTED>` first, build loops to run against environment variables so the credential never leaves the environment, and captured artifacts to be quoted only on the lines carrying the signal. Where the redacted output isn't enough to diagnose the bug, the skill has to say so and ask you rather than pasting the raw thing. It is an instruction, not a scrubber, so give the output one read of your own before it goes anywhere public.

**My security scanner flagged this skill as high risk.**
Snyk flags it, and the flag is a false positive. It is the only skill in the set that ships an executable shell script (`hitl-loop.template.sh`) alongside instructions to run it and to curl a dev server. Shipped `.sh` plus run-it instructions plus outbound HTTP is enough to trip a static scanner. The script itself is about 30 lines of `read -r -p` prompts that pause for human input. The scanner is rating the capability surface, not a proven exploit.

**What happened to `/diagnose`?**
Renamed to `/diagnosing-bugs` in v1.0.0. The old name no longer exists. Anything of yours that chains `/diagnose` (a wrapper skill, a saved prompt) needs updating.

## It's working if

- It builds and runs a repro command *before* theorising — and shows the invocation and its redacted output.
- The loop asserts the symptom you actually reported, not a nearby failure.
- Hypotheses arrive as a ranked, falsifiable list shown to you before any are tested.
- Debug instrumentation is tagged (`[DEBUG-...]`) and grepped away before it declares done.
- Captured artifacts quote only the lines that carry the signal; credentials stay in environment variables.
- The regression test passes and the original real-surface path reports `VERIFIED`.

## Where it fits

`diagnosing-bugs` is a reach-for-it-anytime standalone — you drop into it the moment something is broken and leave only after the regression test and original public path pass. It uses [engineering-principles](https://aihero.dev/skills-engineering-principles) for the shared root-cause and proof rules, and [verification](https://aihero.dev/skills-verification) for the final real-surface verdict. When the real finding is that there's no good seam to lock the bug down, that's your cue to run [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) yourself afterwards. When you're unsure which skill fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
