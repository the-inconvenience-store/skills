---
name: audit-upstream
description: Audit the canonical skills fork and pstack, and classify changes worth adopting.
disable-model-invocation: true
---

# Audit Upstream

## 1. Generate the reports

From the repository root, run:

```bash
./scripts/audit-upstream.py
```

By default this writes two report paths under `docs/upstream/`: a fork reconciliation against the local working tree, and a pstack comparison from its last-reviewed commit to the current upstream commit. Use `--source fork` or `--source pstack` when the user asks for only one. Pass `--upstream-dir` (fork) or `--pstack-dir` only for a trusted checkout the user supplied. Read the printed reports. If one audit fails, assess any successful report and name the missing source.

## 2. Check each source using its own policy

- **Fork:** Read [config.json](./config.json). Confirm that every upstream skill is mapped, new, or ignored, and every local skill is mapped or reported as absent upstream. Keep rename mappings and ignores as policy; call out suspected changes rather than silently remapping them. Account for duplicate targets, unclassified skills, and stale ignores.
- **pstack:** Read the [watchlist procedure](./PSTACK.md) and its mapping. Assess watched diffs against the corresponding local guidance, investigate missing paths, and inspect newly added unwatched skills. Treat pstack as a source of ideas, not a fork whose local differences must be reconciled.

## 3. Assess the changes

Read each report's changed paths and diffs, including docs. For the fork, also read each new and absent entry; for pstack, open the pinned source of each new unwatched skill. Replace each generated assessment with an adopt, defer, or ignore summary that distinguishes:

- upstream changes worth considering for adoption;
- intentional fork divergence, including branding and invocation changes;
- possible upstream deletions that leave local content behind;
- documentation changes that need to accompany any adopted skill change.

The step is complete when every non-empty report category is represented in the assessment or explicitly identified as mechanical noise.

For pstack, advance the last-reviewed commit only after accounting for every watched change and new skill. Keep the evidence report for the comparison that informed the decision.

## 4. Implement approved changes

When the user asks to adopt upstream changes, implement the meaningful behavior and its connected docs, manifests, router entries, and invocation metadata according to this repository's instructions.

For a new fork skill classified during implementation, add an explicit mapping in [config.json](./config.json), including the docs mapping when one exists, or add a reasoned ignore if the user declines. For a newly adopted pstack source, add its upstream path and local landing points to [pstack.json](./pstack.json) instead.

Localize adopted content. Search the implemented skill and every connected local file case-insensitively for upstream branding and identifiers:

```bash
rg -ni 'matt([ -]?pocock)?|mattpocock' <adopted paths>
```

Replace user-facing and internal references with this fork's vocabulary: `inconvenient`, the appropriate renamed skill such as `ask-inconvenient` or `bootstrap-skills`, and `the-inconvenience-store/skills` where a repository identifier is needed. Inspect every match rather than applying a blind replacement. Preserve upstream identity only where exact provenance, fetch URLs, mapping keys, raw diffs, or attribution require it.

After fork adoption, rerun `./scripts/audit-upstream.py --source fork` and explain every remaining changed mapping as intentional or finish applying the missing behavior. After pstack adoption, check the adopted behavior and its local consumers directly: the upstream-to-upstream diff cannot prove local adoption. Preserve the original pstack report, including its comparison revisions and decisions.

## 5. Finish with a decision summary

Verify that the fork report follows [the report template](./REPORT-TEMPLATE.md), that the pstack report records both upstream revisions and its watchlist results, and that all generated reports remain under `docs/upstream/` without unresolved template tokens.

Always finish by telling the user:

- which changes are meaningful and why, grouped by adopt, defer, or ignore rather than by raw file count;
- the report paths and counts for each source;
- which remaining differences are intentional fork policy.

For an audit-only run, explicitly offer to implement the meaningful changes. For an implementation run, summarize what was implemented and offer to implement any meaningful changes that remain; say clearly when none remain. The audit is incomplete if the final response only reports counts or a file path.
