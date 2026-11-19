---
name: prune-tests
description: Remove redundant or behavior-free tests while preserving independent contracts.
disable-model-invocation: true
argument-hint: "[optional path]"
---

# Prune Tests

Prune proof that earns no protection. Optimize for contracts preserved with less coupling, not deletion counts.

## Value bar

Each retained test names a **contract** (observable behavior or invariant) and a credible **regression** it detects. A **keeper** is the primary test that proves a contract at its owning production boundary. Another layer earns proof for a distinct boundary risk, such as serialization, persistence, or lifecycle.

Preserve independent API, protocol, storage, migration, security, packaging, and observable-ordering contracts. Static checks, negative assertions, and slow tests can protect real behavior. A baseline failure may be a product defect; preserve its evidence.

Missing evidence means preserve the candidate. Transfer unique coverage to a keeper before deleting its old home.

Before classifying candidates, read [the audit guide](references/audit.md) for evidence requirements, junk patterns, and retention exceptions.

For whole-subsystem or repository-wide pruning, follow [campaign mode](CAMPAIGN.md) instead of the local sequence below. The value bar and audit guide apply in both modes.

## 1. Inventory

Use the requested scope, or the current change when no path is given. If neither identifies tests, ask for a scope. Read every in-scope test, including parameter rows, and the production paths its assertions exercise. Group tests by their production owner.

Classify each declaration using the audit guide. Split parameter rows when their classifications differ.

Done when every in-scope test has a classification and evidence, including explicit unresolved candidates.

## 2. Choose keepers

Map each contract to its keeper. For every proposed removal, name the proof that remains or establish that no intended contract exists. Identify assertions that must move, support code that becomes unused, and distinct risks that justify multiple layers.

Done when every removal has an evidence-backed disposition and every unique contract has a keeper. Preserve unresolved candidates.

## 3. Prune

Repair or transfer unique assertions first, using independent expectations and the real production owner. Then delete redundant or behavior-free tests.

Remove support code and production seams made obsolete by the pruning after checking their remaining callers. Update affected test discovery and CI routing using existing repository conventions.

Done when every planned change is applied and retained proof remains runnable.

## 4. Verify and report

Run affected keeper and sibling suites using the repository's existing commands. Exercise the owning executable when removing static checks that previously supplied its only proof.

For repaired assertions or transferred unique coverage, demonstrate sensitivity to the named regression using a pre-fix baseline or a temporary production mutation. Confirm failure comes from the intended assertion. Restore only your mutation, preserving unrelated edits, and run the keeper on restored production code. Report unavailable baseline proof rather than claiming it.

Report removals and repairs, keeper locations, removed test-only seams, validation results, and unresolved candidates. Separate pre-existing failures from changes caused by pruning; unresolved proof is a completion limit.

Done when affected proof passes, or pre-existing failures are accounted for, and each repaired or transferred contract has a demonstrated failing control and passing keeper.
