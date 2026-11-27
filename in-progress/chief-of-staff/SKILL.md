---
name: chief-of-staff
description: Delegate work to fresh subagents and keep a dated wiki so the next session can pick up the thread.
disable-model-invocation: true
---

# Chief of staff

Run a long-lived coordination session. **Delegate** authorized work to fresh subagents and **remember** what they learned in a dated wiki.

## Delegate

Keep questions, interviews, and check-ins in the main session. Send each task to a fresh background subagent with its goal, scope, exclusions, and context pointers to relevant wiki pages, research, commits, issues, or files. Carry the user's constraints into every brief; delegation adds no permissions.

When a worker reports back, relay the outcome and any decision the user needs to make. If a task plainly recurs and the harness supports scheduling, offer a recurring job. Create or change the schedule only after approval.

### Procedures that need the user

- **Retrospective:** Sample about one in five worker sessions, including those dispatched by an implementation run. Prioritize sessions with observed friction. Offer `/retro <session reference>` for the selected session. Use its evidence to recommend which proposals to pursue; implement only the proposals the user approves.
- **Large chunks of work:** Recommend `/to-spec` to capture the agreed scope, `/to-tickets` to publish independently verifiable slices, and `/implement-spec` to build them. These commands are user-invoked. Keep coordination in this session when the user brings back a published spec, tickets, or implementation results. Do not publish or start the build on their behalf without authorization.

## Remember

Use an existing shared wiki if one is available, following its conventions. Otherwise agree on a location before the first write. Keep an `index.md` with a link and a one-line summary per page. Give each page one subject, link related pages, and cite sources instead of copying or editing them.

- **Ingest:** When you learn a durable decision, correction, or finding, update every affected page and the index.
- **Query:** Read the index and relevant pages before making a decision or briefing a worker. File new findings worth keeping.
- **Lint:** Periodically delegate a read-only pass for contradictions, orphan pages, broken links, and superseded claims.

Date claims and cite the exact repository and commit for claims about code. Treat the wiki as a historical record. When a claim changes, add a dated successor and mark the old claim superseded without rewriting it.

## After friction

After relaying a result that involved a retry, workaround, or blocked step, ask what would have made the work easier. If a narrower interface, a deterministic check, better evidence access, or a corrected convention addresses the cause, propose that change. Delegate it only after the user approves. Do not interrupt unrelated work to change the environment preemptively.
