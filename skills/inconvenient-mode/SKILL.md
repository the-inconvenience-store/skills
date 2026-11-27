---
name: inconvenient-mode
description: Run an engineering task through the Inconvenient skills that fit.
disable-model-invocation: true
argument-hint: "<goal and what should be true when done>"
---

# Inconvenient mode

Apply this mode to the requested task. If no task is stated, ask for the goal and stop. If the user only wants help choosing a command, recommend `/ask-inconvenient` and stop.

## Frame the task

State the goal, scope, and observable finish line. Use accepted specs and repo conventions to resolve facts. Ask only when an unresolved choice changes the result or authorization. A read-only request stays read-only. Mode adds no permission to commit, publish, deploy, or take destructive actions.

For substantive engineering decisions, call the Skill tool with `engineering-principles` unless its selection policy is already in context. Apply that policy to select references by decision. For multi-step work, track the selected workflow's steps.

## Pick the route

Pick the narrowest route that delivers the result. Read the selected playbook before acting. Add a second route only if its output is a prerequisite or the user asked for it. Give each skill the scoped task and relevant evidence.

| Requested result | Action |
| --- | --- |
| Explain code, recover rationale, check external facts, or inspect a runtime capture | [Investigation](playbooks/investigation.md) |
| Diagnose or fix a bug | [Bug fix](playbooks/bug-fix.md) |
| Diagnose slowness or improve a measured metric | [Measurement](playbooks/measurement.md) |
| Settle a decision through a discussion or experiment | [Design experiment](playbooks/design-experiment.md) |
| Build a settled feature | [Feature](playbooks/feature.md) |
| Improve structure while preserving behavior | [Refactoring](playbooks/refactoring.md) |
| Create or revise a skill | [Authoring a skill](playbooks/authoring-a-skill.md) |
| Compare agent workflows against a rubric | [Evaluation](playbooks/eval.md) |
| Plan several units, run within bounds, resume, or pause | [Long run](playbooks/long-run.md) |
| Inspect PR status, triage review feedback, or draft a PR body | [Pull request](playbooks/pull-request.md) |
| Inventory worktrees before deciding what can go | [Worktree cleanup](playbooks/worktree-cleanup.md) |
| Review Standards and Spec, or assess downstream risk | Call the Skill tool with `code-review` for a review of a pinned diff, or `blast-radius` for a focused safety check. |
| Prove live behavior, check a formal property, or draw a checked statechart | Call the Skill tool with `verify`, `formal-verify`, or `statechart`, respectively. Creating or maintaining project-level verification artifacts requires that intent. |
| Write human-facing engineering docs or tighten existing prose | Call the Skill tool with `technical-writing` or `unslop`, respectively. |
| Edit other instructions an agent follows | Call the Skill tool with `writing-for-agents`. |

When a user-only workflow is the requested next step, tell the user which command to invoke and why. Examples: `/grill-with-docs` to settle decisions and record domain language, `/wayfinder` for a large unresolved effort, `/implement-spec` for a ticket graph, `/ship` to publish, and `/retro` to learn from the run. Do not call those skills, read their bodies as execution instructions, or silently recreate their workflows. If no route fits and no user-only workflow is needed, do the smallest in-scope task directly with the agreed check.

Keep coupled work inline. When directly delegating independent work, start the brief with the absolute path to [worker.md](worker.md), then give the goal, scope, permitted writes, and required evidence. Use the harness's available agents. Check the combined result before relying on it.

## Hand back the result

Lead with the answer or the change. For implementation, name the check and what it showed. For an investigation, cite the evidence and separate inference from observation. Say what could not be established and name only decisions or actions the user actually owns.

