# Time audit

Run the full measured-time branch of [retro](../SKILL.md) for the selected scope. Use **accounted time** throughout: every duration has a source, a timing basis, and an explicit treatment of overlap.

## 1. Establish coverage

Discover persisted sessions and their schema through the selected harness's available history/export facilities, AgentTrace discovery, or documented session storage. Read the relevant interface documentation first; derive locations from discovery rather than assuming a path or requiring an archive API. When the selected source is omp, also read [omp.md](omp.md) for its archive and event guidance.

When AgentTrace is installed, read [agenttrace.md](agenttrace.md) and use its source-scoped discovery, inventory, and triage recipes alongside available native evidence. Check the installed version and help first. Reconcile inventories; AgentTrace summaries do not replace raw timing evidence or establish complete subagent coverage. If unavailable or unsupported for the selected harness, continue from accessible native records without installing dependencies and report coverage limits.

Use the scope selected in retro. For a historical audit, record exact interval boundaries and timezone, anchoring the default trailing 90 days at audit start. For a specified session, include its related subagents without adding unrelated history. Identify the repo by recorded workspace metadata and canonical paths. Follow parent/child links, including worktree or temporary-directory sessions belonging to the same task. Label ambiguous repo attribution separately.

Inventory sessions and events intersecting the interval, including sessions that began earlier. Record accessible dates, parent and child counts, unavailable or truncated sessions, unresolved child links, schema differences, and missing timing fields. Retain source locators so findings can cite session IDs, tool-call IDs, and event timestamps without exposing secrets.

**Done when:** the report can state what portion of the requested interval and session graph was actually accessible. If history is unavailable, report the discovery attempts and missing prerequisite; draw conclusions only from accessible evidence.

## 2. Account for every tool call

Build one record per `(session ID, tool-call ID)`, merging duplicate or streamed events. Keep calls without IDs in a separately counted, explicitly uncertain bucket. Retain tool name, command and working directory where applicable, parent/job links, timing fields, outcome, and source locator.

Use one reproducible accounting procedure for all report views. Before recomputing, apply [analysis reuse](diagnosis.md#reuse-reproducible-analysis): source fingerprints, exact window, and method determine whether an existing artifact is reusable. Record the input manifest and procedure so repeated analysis of the same snapshots yields the same ledger.

For each call:

- Prefer recorded execution start/end timestamps: label their difference **execution time**.
- Otherwise use tool-result timestamp minus tool-call timestamp: label it **elapsed latency**, which can include approval, queueing, transport, and execution.
- Separate queueing and approval delays only where recorded phase boundaries support it. Mark missing, negative, inconsistent, and unmatched intervals as unavailable rather than zero; report counts by cause.
- Clip intervals to the audit window. Cap each individual measured wait at 15 minutes, recording the uncapped value where known and the number capped. Apply the cap consistently to the reported aggregates and retain uncapped totals separately so truncation is visible. Open waits with no end remain missing, not invented 15-minute measurements.
- An asynchronous submission measures submission only. Link the job's recorded execution and completion events to measure its runtime once; keep polling/wait overhead separate. Identify nested tool and shell-wrapper records that describe the same execution so they are not counted twice.

Maintain separate execution-time and elapsed-latency aggregates. Summed durations are **call-time**, not wall-clock time. Compute occupied wall-clock time by interval union across overlapping calls, including parent/subagent overlap; report the timing basis for each union. Overlap across categories means their occupied times need not add to the overall union. Unrecorded gaps are not measured agent thinking time.

**Done when:** every discovered call has one accounted record or an explicit exclusion/missing-data reason, and async jobs, duplicate records, caps, and overlap are reconciled.

## 3. Classify shell work

Group shell calls by what they actually run: **typecheck, tests, build, lint, install, git, sleep, other**. Resolve wrappers and package scripts from repo files where available; flag current definitions that cannot establish historical behavior. Preserve command variants and working directories for diagnosis.

Split compound commands only when timings exist for their components. Otherwise keep the whole call once in `other`, label it compound, and list its components. Classify wrapper intent rather than charging the same duration to every command it contains.

For every category show hours of call-time, call count, timed count, median, and p90, separately by timing basis. State percentile convention and cap policy. Show queueing/approval totals separately where measurable. Include non-shell tools in the overall ranking so a shell-only view cannot hide the largest sink.

Inspect frequency and duration together, including the largest calls and distribution clusters. Rank actual command variants as well as broad categories. Treat tool-generated health scores, recommendations, and estimated savings as triage hypotheses until checked against the ledger.

**Done when:** category counts reconcile to shell-call records, missing timings stay visible, and the report distinguishes cumulative call-time from occupied wall-clock time.

## 4. Trace instruction costs

Inspect the selected harness's active instructions, relevant skills, and repo rules for requirements that trigger slow or redundant commands. Use the active context and available discovery facilities to locate them. Read referenced rules when their branch applies.

For each implicated rule, quote the exact text with its source locator and connect it to observed session/tool-call IDs, command variants, frequency, and accounted time. Distinguish required checks from discretionary repeats and legitimate verification. Current instructions demonstrate current policy; attribute historical calls to a rule only when session evidence or a historical version supports that connection. Label other connections as hypotheses.

**Done when:** each claimed instruction cost has both an exact rule citation and observed calls, with uncertainty about historical applicability stated.

## 5. Diagnose and benchmark the top three sinks

Rank sinks by accounted call-time, showing execution and elapsed-latency contributions separately and explaining any uncertainty that could change the ranking. Select three distinct sinks, or all available if fewer than three are supported.

For each sink, read the applicable branches of [diagnosis.md](diagnosis.md). Inspect the actual command, workload, repetition pattern, and available phase timings. Measure why it is slow instead of inferring the cause from its name. Propose the cheapest fix that preserves the required behavior. Supported dependency edges may identify a blocking critical path; parentage and timestamps alone cannot.

Where safe on this machine, benchmark the current command against a non-mutating alternative using [paired command benchmarks](diagnosis.md#paired-command-benchmarks). If measurement is unsafe or unavailable, report the historical baseline, any safe local baseline, and an executable experiment plan with its equivalence criterion. Claim an improvement only after measuring it.

**Done when:** each selected sink has a measured baseline or explicit measurement gap, evidence for its cause, the cheapest proposed fix, and either a paired benchmark with equivalence evidence or an executable experiment plan. Name suspected causes that the measurements exonerate, especially quality gates that are not the bottleneck; preserve their required behavior.

## Report

Deliver:

1. **Coverage and method:** interval, session/subagent coverage, missing data, timing basis, deduplication, percentile method, cap count and effect, async treatment, and overlap accounting.
2. **Time ledger:** shell-category table and overall sink ranking, with execution time, elapsed latency, and occupied wall-clock time clearly distinguished.
3. **Instruction costs:** exact rule citations linked to observed calls, separating supported attribution from hypotheses.
4. **Top three sinks:** cause evidence, baseline, alternative, benchmark conditions and equivalence results, cheapest fix, and remaining experiment where needed. Use retro's candidate format and the action classification and confidence criteria in [diagnosis.md](diagnosis.md#comparable-experiments-and-proposed-actions).

Return these findings to retro's presentation step. [credits.md](credits.md) records upstream techniques and deliberate departures.
