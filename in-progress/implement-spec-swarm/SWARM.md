# Swarm mode

You are the **orchestrator**. Each ticket goes to one **worker**: a coding agent started by herdr in its own worktree, on its own branch, in its own **slot** (a number from 1 to the config's max workers, used for isolation). Workers persist in their panes after reporting, so a worker keeps its context for feedback, conflicts, and retries.

Your job is planning, dispatch, the **scope check**, merging, and unblocking. Production code comes from workers; the only edits you make are trivial merge resolutions.

## Inputs

- **Swarm config**: `docs/agents/swarm.md`, pointed to from the `## Agent skills` block in `CLAUDE.md` or `AGENTS.md`. If it is missing, show the user [swarm-config.md](swarm-config.md) as the template to fill in and stop.
- **Herdr**: load its skill once with `herdr --skill`. The CLI changes between releases: when a command errors on an unknown subcommand or flag, read `herdr <group> --help` and retry with what it says.
- **Tickets**: only tickets carrying the AFK-ready triage label (`ready-for-agent`) join the swarm. Tickets labelled for a human (`ready-for-human`) are skipped and listed in the final report, along with their dependents.

## Run log

Keep `swarm-run.md` in the notes directory from step 2. It is the source of truth for the run, so update it before and after every action that changes a worker:

| Ticket | Role | Slot | Branch | Worktree | Agent | State | Attempts |
| ------ | ---- | ---- | ------ | -------- | ----- | ----- | -------- |

`Worktree` is the path, plus the herdr workspace id when herdr created it. `Agent` is the herdr agent name. `State` is one of `planned`, `working`, `reported`, `merged`, `blocked`. Below the table, record the spec, the integration branch, the commit it was cut from, and the approved plan.

**Resume**: before step 1, look for a `swarm-run.md` for this spec in the notes directory. If one exists, list herdr's live agents and worktrees, adopt every worker the log names, pick each up from its logged state, and continue from the first unfinished step. A worker that exists in the log but not in herdr goes back to `planned`. Every action below is written to be safe to repeat.

## After step 3: preflight

Check each of these and stop with the exact failure on the first one that fails:

- `HERDR_ENV=1` is set, so you are running inside herdr.
- The config names `herdr` as the multiplexer.
- Every agent in the role table is on `PATH`, and `herdr integration status` shows its integration installed.
- Each agent's harness can see this skillset's `tdd` and `engineering-principles` skills (Codex and Pi read `~/.agents/skills`, Claude reads `~/.claude/skills`).
- The worktree create command from the config runs on a throwaway branch, and the remove command cleans it up.

## After preflight: plan and approval

Build the plan and present it as one table: ticket, title, **role**, slot, depends on, shared resources touched.

- **Role**: infer each ticket's role from its content against the role table (a ticket that builds screens is `ui`, one that changes schema is `data`). Use the config's default role when nothing fits better.
- **Shared resources**: name every resource two workers could write at once: database schema, seed data, a dev server port, shared config, generated files. Take what the project can isolate from the Isolation section of `docs/agents/verification/<surface>/README.md` and from the config's slot hooks. Isolation is best effort: workers share whatever cannot be isolated, and tickets that write an incompatible change to a shared resource (a migration, a seed reset) run one at a time in plan order. Mark these as serialized in the plan. This ordering lives only in the run log; the tracker's blocking edges stay as they are.
- **Concurrency**: at most the config's max workers run at once.

The user approves once. Approval covers dispatching every worker, creating and pushing the integration branch, and opening the draft PR in step 4. Pushing to or merging into the main branch always needs its own confirmation. Apply any role or ordering override the user gives, write the approved plan to the run log, then run step 4.

## Step 5 replacement: dispatch

For each ticket on the frontier, up to the max workers:

1. Claim the ticket using the issue tracker's claim operation.
2. Create the worktree with the config's create command, on branch `swarm/<ticket>-<slug>` based on the integration branch tip.
3. Run the config's slot hooks for this slot, if any.
4. Open a pane in the worktree and start the role's agent: `herdr agent start <name> --kind <agent> --pane <pane> -- <args>`, passing the role's `args` exactly as written. Name the agent `swarm-<ticket>`.
5. Prompt the worker with the **brief** below and set its run log row to `working`.

The **brief** is short and made of context pointers:

- The ticket, the spec, and the notes directory (principles, exploration notes, this run's role notes from the config).
- Its slot's environment, from the slot hooks.
- The worker's own checklist, which is step 5 of `SKILL.md` for a single ticket: confirm the worktree is based on the integration branch, scan `engineering-principles`, build with `tdd`, commit with Conventional Commits, merge the integration tip, run the full suite green.
- Its boundaries: work inside this worktree only, commit locally, and leave pushing and merging to the orchestrator.
- Its report: end with exactly one line, `DONE <commit sha>` once the full suite is green, or `BLOCKED: <the decision or fact it needs>`.

## Steps 6 and 7 replacement: monitor and merge

Wait on all working workers with `herdr agent wait`, and read a worker's output with `herdr agent read` when it changes state. On each report:

- **`DONE`**: run the **scope check**. `git diff --stat <integration>...<branch>` should touch only what the ticket describes. If it reaches outside the ticket, send the worker the specific files and ask it to revert them or explain why, then wait again. When the scope holds, merge the branch into the integration branch.
  - A clean merge, or a trivial conflict (imports, lockfiles, generated files), you finish yourself.
  - Any other conflict goes back to the same worker: tell it to merge the integration tip, resolve, rerun the full suite, and report again.
- **Merged**: set the row to `merged`, close the worker's pane, and check the frontier. Dispatch newly unblocked tickets. Track merges from the run log; the tracker's blocked-by counts lag during a run.
- **`BLOCKED`**: answer it yourself if the spec, tickets, notes, or codebase settle the question. If it needs a product decision, see **Failures**.
- **Idle without a report, or crashed**: treat it as a failed attempt.

## Failures

A worker gets one retry: send it the failure (the suite output, the blocking question, or the missing report) and wait again. When the second attempt fails or the blocker needs the user:

1. Set the row to `blocked` and leave its pane, worktree, and branch in place.
2. Comment the evidence on the ticket.
3. Run `herdr notification show "swarm: <ticket> blocked" --body "<one line>"`.
4. Keep working the rest of the frontier. The blocked ticket's dependents stay unstarted.

The run ends when every ticket is either merged or blocked, or depends on a blocked ticket.

## Steps 8 and 9: QA

Start one worker in the config's `qa` role in a worktree of the integration branch. Prompt it to run steps 8 and 9 from `SKILL.md`: call `code-review` once with the commit the integration branch was cut from as the fixed point, then call `verification` on the integration branch, and report the findings and the verdict.

Send the accepted findings to one worker in the default role, which fixes them and reports `DONE`, then merge as above. The `qa` worker reruns only the focused checks for the fixed findings, and the review does not run again.

## Step 11 replacement: teardown

For every `merged` row, close the pane, remove the worktree with the config's remove command, delete the branch, and run the slot teardown hook if the config has one. Leave every `blocked` row's pane, worktree, and branch in place so the user can step in with the worker's context still live.

## Step 12 additions

Add to the report:

- The plan as run: ticket, role, agent, attempts, outcome.
- Each blocked ticket with its pane, worktree, branch, and the comment you posted, followed by its dependents.
- Skipped human tickets and their dependents.
- Shared resources that ran without isolation.
