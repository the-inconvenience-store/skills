---
name: blast-radius
description: "Check what a risky change could break beyond the diff and test the safety assumption on real code. Use when asked for the blast radius or when a change can affect downstream consumers, shared state, or durable data."
---

# Blast radius

Test the one fact a material change relies on to be safe. This is a focused risk check, not a Spec or Standards pass or an application-wide verification run.

## 1. Fix the scope

- **Called from review:** Accept the caller's pinned base, reviewed revision, and exact diff scope. Use those inputs as supplied, with no floating-ref substitution or expansion to the working tree.
- **Standalone:** Identify the requested change and base or before-state, then pin the comparison and state it. Resolve named revisions to commit IDs. If the user specifies staged or working-tree changes, include those exact layers and applicable new files; record that source state before checking. If materially different comparisons are plausible and the request does not distinguish them, ask which change to assess.

Read source from the scoped revision or snapshot, not whichever files happen to be checked out. Keep the user's checkout, refs, index, and product code untouched. If the active workspace does not exactly match the scoped source, use an isolated source snapshot and verify that the source and dependencies used by the check are the scoped ones, including relevant versions or patches. If you cannot inspect or run the right source, report that limit rather than substituting a different revision.

## 2. Trace the failure and state the assumption

Read the diff and follow the changed behavior through the actual boundary. Trace indirect consumers: readers of the same format or durable data, users of shared state or resources, and dependencies on ordering or timing. Follow pinned dependency code or local patches when they decide what happens at the boundary. Direct callers alone are not the boundary when the effect propagates through data, state, or time.

Describe where the break would surface, under what conditions, and what it would cost. Turn the material path into one falsifiable safety assumption: a fact that, if false, would make the identified failure possible. Name the observable result that would distinguish support from contradiction before choosing a check.

## 3. Run the smallest safe check

Use the smallest focused test, command, or throwaway harness that drives the real caller or boundary on the scoped source and would fail if the assumption were false. Reuse existing evidence only if it exercises that same behavior on that exact revision or snapshot. A mocked boundary, a nearby passing test, or a run on different source cannot establish the assumption.

Keep any scratch harness and side effects isolated and temporary; leave no permanent product writes and do not run against live or shared data. If a safe check is unavailable, the right source cannot be isolated, or the run is inconclusive, mark the assumption **Unproven** and state what evidence is missing. End the check once you have a discriminating observation or can name the blocker. Do not add a review pass.

## 4. Report

- **Scope and effect:** Exact comparison, what changed, and which indirect boundary matters. Cite paths and lines or symbols.
- **Safety assumption:** The fact under test, the exact command (or reference to qualifying existing evidence), the observed result, and the verdict: **Supports**, **Contradicts**, or **Unproven**. For **Unproven**, give the missing evidence and, if known, the smallest next check.
- **Confirmed:** Failure paths established by evidence, with the boundary, triggering conditions, and impact.
- **Cleared:** Specific failure paths ruled out by evidence, with the conditions under which they were cleared.
- **Unchecked:** Plausible paths not resolved by this check and what would resolve them. A gap is not a confirmed risk or a clearance.

When called from review, return this evidence separately from Spec and Standards findings and counts. Those findings stand on their own evidence.

