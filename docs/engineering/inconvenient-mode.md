Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=inconvenient-mode
```

```bash
npx skills update inconvenient-mode
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/inconvenient-mode)

## What it does

`inconvenient-mode` runs an engineering task through the skills that fit and reports what the work established. It picks the narrowest route that can finish the task, rather than running the whole idea-to-ship flow.

## When to reach for it

Type `/inconvenient-mode` with a goal. The agent won't reach for it on its own. Use it when you want the work done and want the agent to choose how to investigate, implement, or check it. If you only want a recommendation, use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).

## Prerequisites

Install the Inconvenient plugin or the model-invoked skills needed for the task. Installing the mode alone doesn't install every skill it can call.

## Give it a finish line

`/inconvenient-mode Find why checkout retries create duplicate orders. Show me the failing path; don't change code.`

This asks for diagnosis, not a fix. A finish line can be an observed behavior, a decision with evidence, or an artifact you want back.

## Playbooks and tools

The mode opens one playbook at a time. A feature, a refactor, and a bug fix have different finish lines. Longer work gets a checkpoint so the next run can resume from the last verified result. If the agent delegates independent work, each worker gets the same scope and evidence rules.

The PR and worktree playbooks ship read-only helpers. The PR helper needs an authenticated GitHub CLI. The worktree helper needs Git and a local integration ref. Neither publishes, merges, or removes anything.

## Common questions

**Does it stay on for the whole chat?**

No. It applies to the task you invoke it for. Run it again for a new task.

**Will it publish my work or run another slash command for me?**

The mode doesn't grant new permissions. It can call model-invoked skills, but if the next step is a user-only workflow such as [ship](https://aihero.dev/skills-ship), it hands that command back to you.

## Where it fits

This is a standalone execution entry point. [Engineering principles](https://aihero.dev/skills-engineering-principles) guide decisions and [verify](https://aihero.dev/skills-verify) provides evidence when changed behavior needs a real-surface check. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) maps the full set.
