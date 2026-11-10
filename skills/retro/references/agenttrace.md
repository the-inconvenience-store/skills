# AgentTrace workflows

Use the installed CLI for evidence in either retro mode. These workflows were exercised against AgentTrace v0.10.1. Read `agenttrace --version` and `agenttrace --help` before using it; adapt to the installed interface instead of assuming flags from upstream documentation.

AgentTrace is local-first. Keep prompts, commands, and logs local; redact report examples. CLI scans can refresh AgentTrace's derived cache outside the repo. Keep that separate from benchmark caches. Leave dependencies, pricing updates, configuration, and existing caches unchanged.

For **standard retro**, locate the selected session through native history/export facilities or documented storage and use the specific-session or explicit-directory recipes below, selecting its exact source path. Collect only evidence needed for the candidate. Fleet overviews, full-history accounting, and benchmarks are optional, not prerequisites. For **time mode**, run discovery and reconcile its inventory to raw events for the ledger in [time-audit.md](time-audit.md).

## Select source

Apply retro's selected-harness scope. Identify the harness from runtime metadata, not the model name: a Codex model running inside omp still produces omp sessions. Confirm its AgentTrace identifier using discovered `metrics.source_tool` values and the installed interface.

| Harness | Observed AgentTrace identifier |
| --- | --- |
| omp / Oh My Pi | `oh_my_pi` |
| Claude Code | `claude_code` |
| Codex CLI | `codex_cli` |

For another harness, discover its identifier rather than guessing from its display name. `--doctor` identifies providers and paths. If necessary, run a narrowly scoped unfiltered `--sessions --project "$repo" --range all --limit 10000 -f json` inventory to inspect `metrics.source_tool`; that is source discovery, not the audit population. An empty result is not permission to substitute another harness. If AgentTrace cannot parse the selected source, use accessible native evidence and state the limitation.

Set `agent_source` to the verified identifier, for example `agent_source=claude_code` when reviewing Claude Code. Keep it on every report command below. For an explicitly mixed-harness scope, run each selected source separately and retain source/session identity when reconciling. The version, help, and doctor commands are interface/discovery checks, not source-filtered reports.

## Discover and scope

In the shell, set `repo` to the canonical current repo path and create a temporary output directory outside it:

```bash
repo="$(pwd -P)"
audit_dir="$(mktemp -d "${TMPDIR:-/tmp}/retro-time.XXXXXX")"
: "${agent_source:?Set agent_source to the verified AgentTrace source identifier}"
agenttrace --version
agenttrace --help
agenttrace --doctor
agenttrace --sessions --source "$agent_source" --project "$repo" --range all --limit 10000 -f json -o "$audit_dir/sessions.json"
```

`--doctor` reports provider locations, discovered/parsed/failed counts, cache information, and example failures. Derive paths from discovery or native harness metadata. A failed candidate file may be ancillary metadata rather than a lost session; inspect before interpreting the failure count as missing sessions.

Reconcile available native history/export evidence with this inventory. Follow parent/child links, including task-related worktree or temporary-directory sessions, and report truncation or missing child evidence. Native history APIs are optional, not universal. For omp archive discovery and event details, read [omp.md](omp.md); other harnesses do not need omp's Eval archive object.

In v0.10.1:

- `--range` accepts only `today`, `7d`, `30d`, and `all`. For the requested 90 days, load `all`, then select sessions whose intervals intersect the exact audit window and clip individual intervals. A session start before the window can still contain in-window work.
- `--limit 0` returns no session rows; it does not mean unlimited. Start with a generous positive limit and increase it if reached. `--overview` has independently truncated sections, including `recent_sessions`; use the session inventory for completeness.
- `--project` is a candidate filter. A short filter such as `skills` returned unrelated workspaces in the live smoke run. Inspect every returned `cwd`, accept canonical matches, and explicitly reconcile known worktree/child paths rather than excluding them merely because their cwd differs. Some sources group a nested cwd under its repo root/name: an archived Codex session did not match its full nested cwd but did match its discovered project name. If a path filter returns no matches, inspect a source-only overview's `by_project` and verify source paths before selecting a reported project name or explicit directory. An empty path-filter result alone does not prove there is no history.
- `metrics.source_tool` records the parsed source. Check it against `agent_source` and the source file, especially for explicit files or generic exports; a filter cannot repair source misidentification.
- Discovery and scoped report counts have different denominators. `data_health.skipped` alone is not a parse-failure count; compare scope, doctor results, and source files.

For that project-group fallback, set `project_name` from the source-only overview, then run:

```bash
agenttrace --overview --source "$agent_source" --range all --limit 10000 -f json
agenttrace --sessions --source "$agent_source" --project "$project_name" --range all --limit 10000 -f json
```

For a directory obtained from archive or doctor, an explicit scan is available:

```bash
agenttrace --sessions --source "$agent_source" -d "$session_dir" --range all --limit 10000 -f json
```

Set `session_dir` from discovered metadata. An explicit directory narrows the inventory; it does not establish that children outside it were included.

## Find risky sessions and repeated waste

```bash
agenttrace --overview --source "$agent_source" --project "$repo" --range all --limit 10000 -f json -o "$audit_dir/overview.json"
agenttrace --recommend --source "$agent_source" --project "$repo" --range all --limit 10000 -f json
agenttrace --context-trends --source "$agent_source" --project "$repo" --range all --limit 10000 -f json
agenttrace --inspect 1 --source "$agent_source" --project "$repo" --range all -f json
```

Use these reports as candidate finders:

| Question | Evidence to inspect |
| --- | --- |
| What did the scan actually cover? | `scope`, `data_health`, `metrics.provenance`, source paths and archive reconciliation |
| Which calls might be slow or repeatedly failing? | Session `diagnostics.tool_latencies`, `tool_warnings`, `diagnostics.stuck_patterns`, `anomalies`, overview `failure_families` and `incident_timelines` |
| Where might retries or repeated reads dominate? | `diagnostics.loop_cost`, `loop_fingerprints`, `metrics.file_usage`, `metrics.tool_arg_usage`, and context-trend evidence |
| Are large outputs/context pressure a plausible cause? | `diagnostics.context_utilization`, `large_params`, and context trends, checked against source events |
| Which session should I inspect next? | `--inspect N`, which selects an Nth priority session, not an Nth chronological row or a specific ID |

Recommendation savings, loop costs, health scores, context utilization, and anomaly labels are tool-generated estimates or heuristics, not measured recoverable time. A long gap can be user-away time. A repeated read can be legitimate after edits. Verify causes before ranking fixes.

The reports above cover AgentTrace's selected range, not an exact custom 90-day window. Apply the audit window to source events before quoting final totals; do not relabel an `all` overview as a 90-day report.

## Extract tool steps and inspect a specific session

Machine-readable session inventory rows include `path`, `cwd`, `metrics`, `anomalies`, `health`, `tool_warnings`, and `diagnostics`. Drill down locally rather than dumping whole reports into model context:

```python
import json
from pathlib import Path
sessions = json.loads(Path(inventory_path).read_text())
session = next(row for row in sessions if row["path"] == target_path)
steps = session.get("diagnostics", {}).get("steps", [])
```

Set `inventory_path` to the saved inventory and `target_path` to a discovered source file. A v0.10.1 tool step exposes `kind`, `name`, `started_at`, `ended_at`, `duration_sec`, `status`, `tokens`, `call_id`, and `parent_id`. Check actual keys on the installed version. Match `call_id` to raw events; `parent_id` is not proof of a complete cross-session subagent tree.

For an interactive human-readable view of the same source:

```bash
agenttrace "$session_file" --source "$agent_source" --diagnostics
```

In v0.10.1 the positional-file route emitted human-readable text even with `-f json`, both with and without `--diagnostics`. For JSON, select the matching `--sessions` row or use `--inspect N` and verify its returned path. Parse only output confirmed to be JSON; do not silently treat text as an empty report.

### Timing and evidence limits

Before using normalized spans, compare representative steps to original call/result timestamps and any execution start/end fields. Test overlapping calls, async submission/completion, missing results, and at least one child session when available. Report which cases were unavailable.

Normalized `started_at` and `duration_sec` names do not certify actual execution boundaries. Likewise, `metrics.duration_sec` with `Duration: timestamp_span` is a session span, including possible inactivity. Per-tool latency summaries cannot supply time mode's median/p90, cap policy, shell-command categories, or overlap-safe wall-clock totals by themselves. Raw command arguments are needed to classify shell work; metadata-only tool steps are insufficient.

When exposed, report AgentTrace's `Detailed`, `Aggregate`, or `Limited` capability. The installed inventory did not expose a standalone capability field in the inspected rows, so use provenance and demonstrated event availability instead of inventing a level. Missing fields remain unavailable, not zero.

Keep the canonical ledger and parser reproducible: record version, source fingerprints, exact scope, schema mapping, cap policy, and percentile convention. Reuse it across report views. AgentTrace and raw events are two representations of the same calls, not two additive sources of runtime.

## Compare before and after

For a quick triage comparison:

```bash
agenttrace --compare --source "$agent_source" --project "$repo" --range all --limit 2 -f json
```

The observed output contains names plus summary turns/tools/success/fail/cost/health. It is not a controlled paired command benchmark and does not establish equivalent workloads. Select known source paths and compare their ledger windows to diagnose a particular change.

Save an overview, then inspect later changes against it:

```bash
agenttrace --overview --source "$agent_source" --project "$repo" --range all --limit 10000 -f json -o "$audit_dir/baseline.json"
# After a separately authorized change and comparable run:
agenttrace --overview --source "$agent_source" --project "$repo" --range all --limit 10000 --baseline "$audit_dir/baseline.json" -f json
```

Read `baseline_comparison` and reported scope. Whole-history growth and a live session changing between scans are not performance regressions. Keep input population and workload equivalent; aggregate `duration_seconds` is not overlap-safe wall-clock time. A successful CLI exit is not proof of improvement or equivalence. Installing CI gates or changing thresholds belongs to a separately authorized implementation, not this audit.

## Smoke-run record

During skill development on v0.10.1, live commands exercised doctor, scoped sessions, overview, recommendations, context trends, priority inspection, positional diagnostics, comparison, and baseline comparison. All successful report routes exited 0; their schemas informed the recipes above. `--range 90d` and `--sort duration` were rejected, so neither appears as a supported recipe. No speedup was benchmarked by these CLI checks. Recheck interface and schemas after upgrades.

Source-filter smoke runs also exercised `oh_my_pi`, `claude_code`, and `codex_cli` against available native logs. omp and Claude Code supported project-scoped inventory and overview; archived Codex supported source-scoped inventory/overview and a discovered project-name filter. Explicit-file diagnostics with `--source` exited 0 for all three. These checks establish the CLI routes, not a complete retrospective in every harness.
