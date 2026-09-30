Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=verification
```

```bash
npx skills update verification
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/verification)

## What it does

`verification` proves behavior through the **real surface** a user or consumer touches: the running UI, CLI, service, mobile app, or public library interface.

It does not treat compilation, tests, screenshots without actions, or an agent's report as proof of the changed behavior. It drives the public path, observes its result and durable side effects, and returns `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

## When to reach for it

Type `/verification`, or the agent reaches for it automatically when a task needs real-surface evidence.

Reach for it to prove a completed change, to create a repeatable project-local driving route, or to audit existing verification instructions after the application changes. During implementation the agent uses its Run branch; creation and maintenance happen only when that is the requested job.

## Prerequisites

Run mode uses project instructions under `docs/agents/verification/` when they exist. Without them, the skill performs the strongest direct check the repository and available tools support, reports the missing reusable route, and leaves permanent project files untouched.

## Three branches, one contract

**Create** learns how the repository actually launches and exposes its user-facing surfaces, writes portable instructions and feature maps, then proves one mapped feature by following those instructions cold.

**Run** selects the changed behavior, health-checks a known instance, drives the public path, captures the action and result, checks promised side effects, and cleans up what it started without deleting evidence.

**Maintain** compares every mapped feature with source and then drives every feature live. Documentation and owned harness drift are corrected; a product regression is reported rather than rewritten as intended behavior.

All three branches share one project format, so creation and maintenance cannot quietly teach different verification standards.

## Proof, not a proxy

The leading word is **proof**. A valid proof exercises the shipped path and observes what the consumer was promised. A test can preserve that contract and a typecheck can rule out a class of mistakes, but neither establishes that the running surface launches, accepts the interaction, and produces the promised state.

An inconclusive observation stays inconclusive. The skill never rounds it up because nearby checks passed.

## Common questions

**Isn't this what my end-to-end tests already do?**

Not quite, and the difference is what is being proved. An end-to-end test proves that a scripted path held the last time CI ran it, against whatever fixtures and stubs the suite installs. Verification proves that *this* change, on the surface as shipped, launches, accepts the interaction, and produces the promised state — now. The two are complementary, and the skill says so: a test preserves behaviour at a seam, verification proves the application path. If your e2e suite genuinely drives the real surface, say so in `docs/agents/verification/` and let Run invoke it; the skill is not precious about the mechanism, only about what gets observed.

**It came back `INCONCLUSIVE` and everything else passed. Can I treat that as done?**

No, and that is the one rule the skill will not bend. An inconclusive observation stays inconclusive; it is never rounded up because the typecheck passed or the tests are green. The useful thing is what `INCONCLUSIVE` carries with it: the exact gap that stopped the observation. That is usually a missing launch step, a surface with no mapped route, or a side effect nobody wrote down. Fix the gap and rerun rather than arguing with the verdict. Both [implement](https://aihero.dev/skills-implement) and [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) treat `INCONCLUSIVE` as incomplete for the same reason.

**I don't have `docs/agents/verification/`. Does Run just fail?**

No. It performs the strongest direct check the repository and the available tools support, reports that there is no reusable route, and leaves permanent project files alone. That last part is deliberate: a Run invocation is not allowed to quietly become a Create invocation and write a half-learned route into your repo. When you do want the route, ask for it and the skill takes the Create branch, which learns how the repo launches, writes the instructions, and then proves one mapped feature by following them cold.

**Why does Create insist on proving a feature before it finishes?**

Because instructions nobody has followed are a guess. The cold run is the completion criterion: it catches the launch step that only works because your shell already had the environment variable, the port that was already bound, the command that needs a build first. A route that has never been walked is the commonest way verification documentation goes stale before it is even committed.

**My app has no UI. Does this apply?**

Yes. The real surface is whatever the consumer touches: a CLI's argv and stdout, a service's HTTP endpoint, a library's public exports, a mobile app's screens. The skill is written around the public path and the observable result, not around a browser. A library's verification is a consumer calling the published interface and getting the promised value back.

**Maintain found something broken. Will it just update the feature map?**

Only for drift it owns: documentation that no longer matches the source, or a harness the skill itself wrote. A product regression gets reported, not rewritten as intended behaviour. This is the failure mode the split exists to prevent — a maintenance pass that quietly redefines a bug as the spec, leaving the feature map green and the product broken.

## It's working if

- The final report names the public path and the observed result.
- Evidence shows the action as well as the resulting state.
- Promised files, records, messages, or other side effects are checked.
- Failed attempts leave no stale process or scratch state behind.
- Product regressions are reported instead of absorbed into the feature map.

## Where it fits

`verification` is bootstrapped by [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) after [guardrails](https://aihero.dev/skills-guardrails) establishes the repository's final launch and check commands. It then serves as the real-surface completion gate after [implement](https://aihero.dev/skills-implement) and the reusable driving route that [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) can use to construct and rerun a bug-specific feedback loop. It complements [tdd](https://aihero.dev/skills-tdd): tests preserve behavior at a seam; verification proves the actual application path. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
