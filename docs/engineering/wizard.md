Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wizard
```

```bash
npx skills update wizard
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wizard)

## What it does

`wizard` generates an interactive bash script for a procedure that contains steps only a human can perform. It can open dashboards, capture values, update `.env`, and set GitHub secrets or variables.

The agent writes and statically verifies the script; it does not run the procedure. You run it in your terminal, where secret input stays hidden and each stage waits for you.

## When to reach for it

Type `/wizard`, or the agent reaches for it automatically when work hits a human-only step.

Reach for it when provisioning infrastructure, collecting credentials, navigating an unfamiliar third-party dashboard, or running a migration or cutover. If the agent has the access and tools to perform the step itself, it should do so instead.

## Prerequisites

The generated script requires bash. Stages that write GitHub secrets or variables use `gh`; when it is unavailable or unauthenticated, the wizard records the skipped action for you to finish manually.

## A staged procedure

Before writing the script, the skill reads the repository and scopes every manual stage and captured value. Each value has a source, a destination, and a secrecy classification. The fixed template supplies confirmation gates, URL opening, hidden input, idempotent environment updates, stage progress, and a closing record of skipped work.

## Common questions

**Do my API keys end up in the model's context?**

No. The agent writes a script; it doesn't run it. You run the script yourself, and it captures the key with hidden terminal entry and writes it straight to `.env` or `gh secret`. The wizard is a CLI, and the model is not connected to it. One caveat: that holds for values the wizard captures at runtime. If you paste a key into the chat while scoping the procedure, it's in the [context](https://www.aihero.dev/ai-coding-dictionary/context) like any other pasted text.

**Can I go back and fix a value I mistyped?**

Not mid-run. There is no back button: the stages run forward, and a wrong answer on stage 3 means Ctrl-C and re-run. Re-running is cheap by design: any value already written to `.env` is offered back as a default, so you press Enter through the stages you got right and retype only the wrong one. This came up in the launch week and hasn't been closed since: "loved it! One thing though, is there a way to go back and correct what you've entered?"

There's a related open bug. Arrow keys in an `ask` prompt insert `^[[D` / `^[[C` instead of moving the cursor, because the prompt uses `read -r` rather than Readline ([issue #741](https://github.com/mattpocock/skills/issues/741)). Backspace works; arrow keys don't. Delete back to the mistake rather than moving the cursor into it.

**Does it know what I've already set up?**

Partly, and less than the launch reactions assumed. It reads the repo before it asks (your `.env` files, `docker-compose`, framework config, the `secrets.*` references in CI), so it scopes to values that are genuinely missing rather than starting from zero the way a README does. What it doesn't do is check the third-party service. If a key exists in your `.env` the wizard offers it back and Enter keeps it; if you already created the Stripe account but never saved the key, the wizard still sends you to the dashboard for it.

**Where does it sit in the workflow, after grilling and the spec?**

Nowhere in particular. It's a standalone, not a chain step. The common guess is `/grill-with-docs → /to-spec → /wizard`, and that sequence is fine, but the trigger is a manual procedure showing up, which can happen at any point: before you start, mid-build, or long after ship. It also works as a discovery tool: scoping surfaces the hidden prerequisites of a task, like the three API keys you hadn't thought about, before you commit to the work.

**Does it work outside Claude Code?**

The artifact does, unconditionally: it's a plain bash script and it doesn't care what [harness](https://www.aihero.dev/ai-coding-dictionary/harness) generated it. The skill itself is model-invoked, so it's listed everywhere: type `/wizard` in Claude Code or `$wizard` in Codex, or just describe the setup you're stuck on. Being model-invoked also keeps it clear of [#693](https://github.com/mattpocock/skills/issues/693), where Claude's desktop and web surfaces drop *user-invoked* skills from the [model](https://www.aihero.dev/ai-coding-dictionary/model)'s listing and report them as not installed.

**Didn't this used to be user-invoked?**

It did. It's now model-invoked, so the agent reaches for it unprompted when it hits a step you have to take. Nothing you could do before stopped working: model-invocation *adds* the agent's reach, it never removes yours, so `/wizard` behaves exactly as it did. What changed is the failure mode it retires: the agent hitting a credentials wall mid-build and dumping six numbered steps into the chat for you to follow by hand.

**It used to be in `in-progress/`: where is it now?**

Promoted, as of v1.2. It graduated out of the drafts bucket and now ships in the plugin, so it arrives with the rest of the promoted set rather than needing an individual install. Its behaviour didn't change on graduation.

## It's working if

- Every human action is a named stage in dependency order.
- Secret values use hidden input and land only where the scope says they should.
- `bash -n` passes, and `shellcheck` passes when available.
- The script has stage counts, not invented time estimates.

## Where it fits

`wizard` is a reach-for-it-anytime standalone at the boundary between automation and human access. It often appears during [implement](https://aihero.dev/skills-implement) when a build needs credentials or a cutover. [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) configures this skill set; `wizard` generates setup paths for everything else. [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you when the boundary is unclear.
