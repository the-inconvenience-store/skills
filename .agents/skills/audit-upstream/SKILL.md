---
name: audit-upstream
description: Audit Matt Pocock's upstream skills repository against this fork and write a Markdown report.
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

## 4. Hand off the report

Verify the report follows [the report template](./REPORT-TEMPLATE.md), contains no unresolved template token, and remains under `docs/upstream/`. Report its path and headline counts to the user. The audit is complete only when the Markdown report is ready to make decisions from; the audit itself never merges upstream changes.
