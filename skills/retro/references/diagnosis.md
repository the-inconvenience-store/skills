# Shared diagnosis

Use the relevant branches for a candidate in either mode of [retro](../SKILL.md). Standard retro can establish a workflow problem from concrete events without timing every call; time mode supplies the full ledger. Missing durations limit performance claims, not other findings. These are diagnostic methods, not permission to change the environment or upload session contents. Techniques are adapted from [credits.md](credits.md).

## Reuse reproducible analysis

Before profiling again, look for an accessible analysis artifact for the same inputs. Key reuse by **source fingerprint + exact window + method**, not the invoking directory or worktree:

- Fingerprint the actual source snapshots and included child sessions. Record stable source locators and content digests, or a documented equivalent that detects changed contents. A path alone does not detect an appended or replaced transcript.
- Include window bounds and timezone, parser/schema version, timing basis, clipping/cap rules, deduplication, child inclusion, percentile convention, and diagnostic classifiers in the method identity.
- Reuse matching artifacts; explain a rerun when inputs changed, the method changed, or the prior artifact is inaccessible. Keep artifacts in the audit's temporary location. This needs no new run log or repository report infrastructure.

Compute tables and classifications with one reproducible procedure, retaining its code or exact commands and input manifest. Reconcile counts against the ledger. Fix classifiers for a comparison, including the definition of polling and repeated commands; disclose changes instead of silently moving calls between categories. Distinguish directly recorded fields, reproducibly computed measurements, estimates, and hypotheses. A computation can be measured without coming from a particular branded profiler, but its inputs and timing semantics must support the claim.

**Evidence gate:** another run with the same snapshots, window, and method produces the same numbers. Missing fields remain unavailable rather than zero.

## Distribution, frequency, and round trips

When recorded timing is relevant, inspect count, timed count, total, median, p90, and largest calls for the selected tool or command. Add p99 only with its sample count and percentile convention. Inspect both the biggest individual calls and repeated modest calls: one long invocation and forty short invocations suggest different experiments. Without timing, cite the observed call sequence and leave duration and savings unknown.

Band durations, for example `<0.3s`, `0.3–<1s`, `1–<3s`, `3–10s`, and `>10s`, separately by timing basis. Record cut points and cap effects. A two-cluster distribution is a **hypothesis generator**, not proof of two operations or approval delay. Split by command variant, workload, outcome, cache state, shell mode, and recorded approval state before naming the cause.

| Suspected sink | Inspect | Evidence needed for an actionable diagnosis |
| --- | --- | --- |
| Round trips and search churn | Repeated queries, result truncation, irrelevant matches, rereads, and whether earlier output already answered the later query | Cite the call sequence and missing information at each step. Propose a better-scoped query, targeted read, or batch only for genuinely independent operations. Fewer calls alone does not prove shorter session time. |
| Output and context pressure | Output bytes/tokens where recorded, repeated full-file reads, carried context, compaction events, and recorded request usage | Show unused or repeated material and a comparable lower-output workflow. Bytes are not token counts; large output does not by itself measure prefill latency or prove a context bottleneck. |
| Approval | Approval-request/grant boundaries, policy state at the time, and comparable command variants | Charge approval time only from recorded boundaries. An allowlisted/non-allowlisted latency difference is supporting correlation, not a measured approval split. Current policy is not historical evidence. |
| Model turnaround | Recorded request/response phases, queue events, API errors, retries, and model/context differences | A tool-result-to-next-action gap remains unassigned unless instrumentation identifies its phases. Queueing, generation, network, user delay, and unrecorded work can coexist; it is not measured thinking time. |

Approval remedies must preserve the permission boundary. A read-only scoped permission or a simpler command form may be a proposed configuration experiment; broad auto-approval is not an audit action. Batch only where dependency and per-call evidence remain intelligible.

## Shell startup and polling

### Shell startup

First establish how the harness actually launches the shell. A per-call startup tax is plausible only if that startup path runs per call.

1. Inspect the applicable startup files, sourced scripts, hooks, plugins, and external commands. Even a shell running `true` can execute arbitrary initialization with side effects. If safety cannot be established, stop at an experiment plan.
2. In an approved non-mutating or disposable environment, compare repeated no-op launches through the actual shell mode with a justified alternative. For a harness that really launches interactive zsh, `zsh -i -c true` versus `zsh -c true` can isolate a candidate interactive-startup difference; it is not a universal harness benchmark.
3. Use the [paired-trial controls](#paired-command-benchmarks). A no-op launch measures launch overhead, not equivalence of real tasks. Confirm required environment, command resolution, and behavior on representative workloads before recommending a different startup mode.
4. If necessary, profile initialization in a reviewed disposable reproduction, for example with zsh's `zprof`. Do not edit live startup files or execute unreviewed initialization merely to obtain a profile.

**Evidence gate:** measured per-launch difference, observed affected launch count, and behavioral equivalence. Their product is an estimated call-time opportunity, not automatically wall-clock savings.

### Polling oversleep

Link submission, job identity, status checks, completion, and the eventual consuming action. Distinguish useful progress checks from repeated checks with no new information. A `sleep` inside a command is not necessarily polling.

- With recorded job completion and next observation timestamps, measure completion-to-observation delay. Attribute it to the polling schedule only if the parent was ready to consume that result.
- Without completion evidence, count polling calls and measured sleep intervals, but label avoidable oversleep unknown. Poll intervals are not completed-job idle time, and overlapping sleeps are not additive wall-clock loss.
- Propose an existing completion notification or blocking wait facility when it preserves progress, cancellation, and error handling. Do not assume the harness supports one or change scheduling during the audit.

**Evidence gate:** the trace identifies redundant checks or a measured post-completion delay; the alternative is available and preserves required behavior.

## Repeated external work and quality gates

For tests, builds, installs, network checks, and review passes, retain exact commands and input revisions. Determine whether repeats consumed changed inputs, new failures, different coverage, or new authorization. A repeat after an edit can be necessary. Current script definitions may not explain historical invocations.

Check cache configuration, cache hit/miss evidence, clean/rebuild flags, invalidation, incremental scope, and repeated dependency resolution. Keep cold and warm trials separate; use disposable caches rather than clearing existing ones. A cache is useful only if it preserves freshness and required outputs. Network/service conditions and machine contention are uncontrolled variables unless measured.

Compare narrower checks or reduced frequency only with explicit coverage and correctness criteria. If a suspected review or quality gate contributes little measured cost, report it as **not the bottleneck**, with its counts and timings. Preserve the gate rather than deleting it to satisfy an optimization story. Missing timings cannot exonerate it.

**Evidence gate:** each proposed reduction cites actual calls and unchanged relevant inputs, or an equivalent paired experiment. Runtime that the evidence does not explain remains unexplained, not automatically irreducible.

## Lifecycle, dependencies, failures, and compaction

For a sink involving agents, long gaps, or retries, reconstruct the relevant slice of the session graph:

- **Lifecycle:** recorded start, first event, status transitions, last event, stop/end, resume, and open sessions. Distinguish observed lifecycle span from measured execution and explicitly recorded idle periods. A long quiet interval is an inspection target, not proof the user was away or an API stalled.
- **Agent tree:** parent/child links, agent type/task, dispatch, result delivery, termination, and last known state of failed or unresolved children. Include worktree children belonging to the task. Flag duplicate events, ordering anomalies, missing pages, and incomplete links before drawing conclusions.
- **Dependency path:** use explicit prerequisite, dispatch, await, and result-consumption evidence to build a dependency graph. Parentage alone is not a blocking dependency. Compute a critical path only with supported edges and compatible duration semantics; timestamps, chronological order, and the longest child are insufficient. Report uncertainty or a partial graph when edges are missing.
- **Error propagation:** connect an originating error to affected descendants/ancestors only through recorded relationships and matching failure context. Separate the original failure from follow-on cancellations and duplicate reports. Track attempt identity, outcome, repeated error, changed inputs, retry/backoff, and eventual recovery; repeated tool names alone are not retries. Quantify failure rates with an explicit denominator and distinguish transient API/rate-limit failures from command failures.
- **Compaction:** align explicit compaction events with context/usage baselines, subsequent rereads, lost task state, and retry loops. Compare pre/post values only when their schema and reset behavior are understood. A token spike is not proof of compaction; post-compaction reacquisition can be legitimate.

### Optional: existing local Agent Monitor telemetry

Use this branch only if Agent Monitor is already available locally and the requested sessions exist there. Discover its configured local endpoint and supported read-only API from the existing installation. Do not install it, enable hooks, start collection, or presume a port. Keep credentials and session contents private.

Where supported, read session metadata, events, and agents through `GET /api/sessions/{id}`, `GET /api/events?session_id={id}`, and `GET /api/agents?session_id={id}`; account for pagination and retention. Existing pricing data is optional and irrelevant if time is the only question. Correlate these records with ledger IDs rather than adding another copy of the same execution.

Useful evidence includes PreToolUse/PostToolUse boundaries, Stop/SubagentStop, Compaction, APIError, TurnDuration, notifications, parent links, and an existing orchestration DAG. Establish what each event and duration actually measures. Metadata-only tool steps and aggregate records cannot supply a missing execution trace. A displayed DAG or timestamp timeline does not itself prove a dependency critical path. If telemetry is absent, continue with the accessible audit evidence and name the missing fields.

**Evidence gate:** lifecycle and dependency findings cite source events and links, with missing coverage explicit; no unexplained interval is reassigned to a convenient cause.

## Token and cache evidence

Use this branch only when usage records support the context or retry hypothesis. Keep a reproducible, schema-specific calculation rather than estimating tokens from characters or elapsed time.

- Establish whether usage is per request, cumulative, repeated in streaming events, or reset by compaction. Deduplicate before summing; do not mix cumulative snapshots with deltas.
- Cache semantics differ: Codex `last_token_usage.input_tokens` includes `cached_input_tokens`, while Claude `message.usage.input_tokens` excludes cache-read and cache-creation fields in the formats described by the source. Verify the actual schema/version before applying these rules. Never alias equal field names across providers without checking their definitions.
- State formulas and field meanings for total input, cache reads, cache writes, fresh input, and output. Report parent and child usage separately before any reconciled total. Avoid double-counting a parent's aggregate of child spend.
- Cached input is still processed input, not zero context or free work. Token counts alone do not measure latency or money; cache pricing and timing require their own evidence. Avoid calling a token sum billed cost or quota use without provider-specific support.
- With no usable usage records, token totals and cache ratios are **unknown**. Preserve missing model, cost, and timing fields as missing.

**Evidence gate:** formulas, source fields, cache inclusion rules, and record coverage accompany every reported token aggregate.

## Paired command benchmarks

Use this branch when measuring an alternative in either mode. Standard retro needs it only for a claimed measured improvement; time mode requires a benchmark or an explicit experiment plan for each selected sink.

- Record exact commands, working directory, repo revision, tool versions, environment, workload, and cache state. Use the same input snapshot for both variants.
- Separate cold and warm trials when feasible. Use disposable copies and isolated caches, preserving the working repo and existing caches. Alternate run order across repeated paired trials, report trial counts and spread, and disclose uncontrolled caches or machine contention.
- Compare equivalent outputs, check/test coverage, diagnostics, and exit status as well as runtime. Document permitted output differences. A narrower or skipped check is not an equivalent speedup merely because it exits successfully.
- Attribute queue/approval costs separately from command runtime. Extrapolate to historical workload only as an estimate with stated assumptions; overlapping call-time savings are not automatically wall-clock savings.

If a command is unsafe, unavailable, requires edits, or lacks a meaningful non-mutating alternative, give the measured baseline available and propose an experiment with an equivalence criterion. Leave the improvement unmeasured.

## Comparable experiments and proposed actions

For before/after sessions, match task scope, input revision, required outputs, verification coverage, model/harness settings, cache state, timing method, and concurrency as closely as possible. Show the target category and its counts/durations side by side, not only total session span. If the total falls but the target sink does not, the proposed cause is not demonstrated. Disclose workload differences; cross-session comparisons are not controlled benchmarks by default.

For each selected sink, record:

| Field | Required content |
| --- | --- |
| Cause | Call/event locators, command variant, and whether the claim is measured, estimated, or a hypothesis |
| Proposed fix | Cheapest behavior-preserving change, or a bounded experiment when causality/equivalence is unresolved |
| Class | **Config:** permissions, startup, or cache settings. **Habit:** query scope, repetition, or scheduling choices. **Runtime constraint:** measured service/tool cost without an established local reduction; propose mitigation only where supported. A sink may involve more than one class. |
| Impact | Measured benchmark delta or estimated opportunity, affected call count, overlap treatment, and scope. Keep call-time and dependency-supported wall-clock effects separate. |
| Confidence | State cause confidence and impact confidence separately. High requires direct phase/causal evidence or repeatable equivalent trials; medium has supported associations with named confounders; low is an untested hypothesis. Explain the basis, not an invented probability. |
| Next evidence | An executable safe experiment and equivalence criterion, or the exact inaccessible field/prerequisite |

Rank actions by supported impact and confidence rather than attractive speedup multiples. Exclude implemented changes from this audit: the deliverable is evidence and proposed actions.
