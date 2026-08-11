---
name: audit-upstream
description: Audit the canonical upstream skills repository against this fork and write a decision-ready Markdown report.
disable-model-invocation: true
---

# Audit Upstream

Treat the audit as a **reconciliation**: normalize both repository layouts first, then account for every skill and docs page.

## 1. Generate the inventory

From the repository root, run:

```bash
./scripts/audit-upstream.py
```

Pass `--upstream-dir <path>` only when the user supplied a trusted local checkout. The default clones the configured upstream ref into a temporary directory. The step is complete when the command exits successfully and prints a report path under `docs/upstream/` with both upstream and local commit identities.

## 2. Check the reconciliation

Read [the audit configuration](./config.json) and the generated report. Confirm that every upstream skill is exactly one of mapped, new, or ignored, and every local skill is mapped or reported as absent upstream. Treat rename mappings and ignores as policy: record suspected additions in the report instead of changing policy without the user's direction. The step is complete when there are no duplicate targets, unclassified skills, or unexplained stale ignore entries.

## 3. Assess the changes

Read every new-skill entry, changed-skill file list, absent-upstream entry, docs change, and detailed diff in the report. Replace the generated assessment with a concise decision-oriented summary that distinguishes:

- upstream changes worth considering for adoption;
- intentional fork divergence, including branding and invocation changes;
- possible upstream deletions that leave local content behind;
- documentation changes that need to accompany any adopted skill change.

The step is complete when every non-empty report category is represented in the assessment or explicitly identified as mechanical noise.

## 4. Implement approved changes

When the user asks to adopt upstream changes, implement the meaningful behavior and its connected docs, manifests, router entries, and invocation metadata according to this repository's instructions.

For every new upstream skill classified during an implementation run, update [the audit configuration](./config.json) in the same change. Add an explicit `skill_mappings` entry even when the normalized local name is unchanged; add the corresponding `docs_mappings` entry when an upstream docs page exists. If the user deliberately declines the skill, add a reasoned ignore rule instead. No newly classified skill may remain implicit after implementation.

Localize adopted content. Search the implemented skill and every connected local file case-insensitively for upstream branding and identifiers:

```bash
rg -ni 'matt([ -]?pocock)?|mattpocock' <adopted paths>
```

Replace user-facing and internal references with this fork's vocabulary: `inconvenient`, the appropriate renamed skill such as `ask-inconvenient` or `setup-inconvenient-skills`, and `the-inconvenience-store/skills` where a repository identifier is needed. Inspect every match rather than applying a blind replacement. Preserve upstream identity only where exact provenance, fetch URLs, mapping keys, raw diffs, or attribution require it.

Re-run `./scripts/audit-upstream.py` after implementation. Read every remaining changed mapping and explain why it is intentional; continue implementing if it exposes an unapplied behavioral change. The step is complete when the refreshed report has no unclassified additions and every remaining difference has a concrete fork reason.

## 5. Finish with a decision summary

Verify the report follows [the report template](./REPORT-TEMPLATE.md), contains no unresolved template token, and remains under `docs/upstream/`.

Always finish by telling the user:

- which changes are meaningful and why, grouped by adopt, defer, or ignore rather than by raw file count;
- the report path and headline reconciliation counts;
- which remaining differences are intentional fork policy.

For an audit-only run, explicitly offer to implement the meaningful changes. For an implementation run, summarize what was implemented and offer to implement any meaningful changes that remain; say clearly when none remain. The audit is incomplete if the final response only reports counts or a file path.
