Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=tdd
```

```bash
npx skills update tdd
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/tdd)

## What it does

`tdd` builds a feature or fixes a bug test-first, one behaviour at a time, driving the code out through a red-green loop.

It will **not** write all the tests up front. Batching the tests first ("horizontal slicing") produces tests of _imagined_ behaviour — they check the shape of things and go numb to real changes. `tdd` instead takes vertical slices: one test, then just enough code to pass it, then the next test, each cycle informed by what the last one taught you. Tests target public interfaces only, so the implementation underneath can change without the tests moving.

## When to reach for it

Type `/tdd`, or the agent reaches for it automatically when a task fits — building a feature or fixing a bug test-first, or when you say "red-green-refactor".

Reach for it when there's a concrete behaviour to build and you want tests that survive a refactor. If the behaviour isn't pinned down yet, settle the spec first — for that, use [to-spec](https://aihero.dev/skills-to-spec). When the work is really about the shape of the interface rather than the tests, use [codebase-design](https://aihero.dev/skills-codebase-design); `tdd` calls into it for the deep-module vocabulary during planning.

## Red-green, one slice at a time

The leading idea is the **red-green loop**: write one failing test (red), add just enough code to pass it (green), then repeat for the next behaviour — each cycle informed by what the last one taught you. The very first cycle is a **tracer bullet**: one test that proves a single path works end-to-end, before you build outward from it. Because you just wrote the code, you know exactly which behaviour matters and how to verify it — you never outrun your headlights by committing to test structure you don't yet understand.

Two rules keep the tests honest. A good test reads like a specification ("user can checkout with valid cart") and exercises real code paths through the public API, so renaming an internal function never breaks it. And expected values come from an independent source of truth — a known-good literal, a worked example, the spec — never recomputed the way the code computes them, which is how a **tautological** test passes by construction and tells you nothing.

Refactoring only happens once the suite is green; never while red.

## Common questions

**Why doesn't it refactor? The description says "red-green-refactor".**

Because the refactor step was removed and the description was not. The removal was deliberate: agents essentially never did it, and keeping implementation and review in separate sessions works better. Whether the result still counts as TDD by the book matters less than whether the loop produces better code. The mismatch between the trigger phrase and the body is filed as [issue #589](https://github.com/mattpocock/skills/issues/589) and is still open, so "red-green-refactor" continues to work as a phrase that fires the skill. What you get is red → green, and refactoring in [code-review](https://aihero.dev/skills-code-review).

**It asked me to choose a test seam and I had no idea which to pick.**

This is the most-reported friction with the skill ([issue #607](https://github.com/mattpocock/skills/issues/607)). The prompt lists candidate seams by name only, with nothing about what each one catches or misses, so you are choosing between labels. There is no fix shipped yet. The practical workaround is to ask the agent for the trade-offs before answering: what does the component-level seam miss that the integration seam catches, and how much slower is it. It is also why the chain agrees seams up front in `to-spec`, where you have the whole feature in view rather than one prompt.

**It wrote the implementation before the test, even though the skill says red first.**

It happens. One user pushed the [model](https://www.aihero.dev/ai-coding-dictionary/model) on it and got an unusually honest answer: "I knew the skill said 'one test at a time, watch it fail for the right reason'. I read it. I just defaulted to my normal habit." The skill is written to live with this. No instruction makes an agent comply 100% of the time, and forcing the point harder restricts the agent's creativity for little gain; the loop is worth running even when it is not followed strictly, because the results are still better overall. If strict adherence matters for a particular slice, watch the run rather than trusting the skill to enforce it.

**Should it write browser or end-to-end tests first?**

Usually not, and the skill will not stop it. A user reported the agent writing a Playwright test first, then burning a long loop re-running it and concluding the *test* was broken for a feature that did not exist yet. Configure this in your `CLAUDE.md`. Browser tests are slow enough that the red-green feedback loop stops paying for itself; declare in your repo's `CLAUDE.md` that they are written after the behaviour works.

**Does `/tdd` replace `/implement`, or the course's `/do-work`?**

No. `/tdd` documents the methodology; `/implement` is a very simple work→feedback→commit loop and is the direct stand-in for `/do-work`. The course's single `/do-work` step is now split across `/implement`, `/tdd` and `/code-review`. If you are asking which one to run against a ticket, the answer is almost always `/implement`.

**Where did the deep-modules and interface-design guidance go?**

Into [codebase-design](https://aihero.dev/skills-codebase-design) in v1.0, generalised so several skills share one vocabulary. `refactoring.md` left at the same time; refactoring is now [code-review](https://aihero.dev/skills-code-review)'s job, and that skill carries the Fowler smell baseline.

**Does it know about my other tickets?**

No. Run against one ticket, it will happily propose work that belongs to a sibling ticket, because it has no view of the rest of the issue graph ([issue #129](https://github.com/mattpocock/skills/issues/129) upstream). The position taken there, and kept here, is that this is not `tdd`'s job. Passing the spec alongside the ticket helps; right-sizing the tickets in the first place helps more.

## It's working if

- It writes one test, gets it passing, and only then writes the next — not a batch of tests followed by a batch of code.
- The tests name behaviours, not internals, and would survive an internal rename.
- Expected values are literals from the spec, not figures derived the same way the code derives them.

## Where it fits

`tdd` is the red-green loop the main build chain runs to write code:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

[implement](https://aihero.dev/skills-implement) is the chain's build step, and it drives `tdd` internally to build each ticket test-first before handing off to [code-review](https://aihero.dev/skills-code-review) — so `tdd` is the engine inside that step rather than a step of its own. You can also reach for it directly, whenever there's a concrete behaviour to build without a full spec. Its other neighbour is [codebase-design](https://aihero.dev/skills-codebase-design), which it leans on to find deep-module seams worth testing at. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
