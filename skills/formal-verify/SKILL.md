---
name: formal-verify
description: Create, run, or maintain formal verification of a named property in a model or actual code. Use when the user requests model checking, a formal proof, or an audit of formal verification, or when an existing project formal check is required for the change.
---

# Formal verify

Check a **property** over a stated scope: every reachable state or event order in a model, every input in a code verifier's domain, or the domain of a proof. This complements `verify`, which observes behavior on the real shipped surface. Neither supplies the other's evidence.

## Route

Inspect `docs/agents/formal-verification/`, then choose one branch:

- **Create**: the user asks for a reusable formal check. Read [references/create.md](references/create.md) and [references/project-format.md](references/project-format.md).
- **Run**: the user asks to check a property, or a project formal obligation applies. Read [references/run.md](references/run.md). The project record owns the command for an existing check.
- **Maintain**: the user asks to audit, update, or repair existing checks. Read [references/maintain.md](references/maintain.md) and [references/project-format.md](references/project-format.md).

Maintain with no artifact routes to Create. Create with an existing artifact routes to Maintain unless the user explicitly requests replacement or a new check. Run with no artifact performs the strongest direct or scratch check available and reports the missing reusable route. Run leaves no permanent project files.

## Proof standard

- State the property from the intended promise, not from the implementation expression that decides it. Check that a success path and any property antecedent are reachable; a vacuous pass is not evidence for the promise.
- Name the checked target, tool, bounds, assumptions (including fairness where relevant), reductions, and exclusions. Claim completion only for the properties the checker actually evaluated. For an unbounded claim, cite a proof or completed analysis that covers the unbounded dimension; a bounded pass does not establish it.
- Keep model and code claims separate. Use a verifier that analyzes the actual implementation for a proof about the code itself. To apply a detached model's result to the code's event orders, establish that its actions, guards, and atomicity match the actual source revision. A stale model can still be checked as a model. Replay a counterexample against real code step by step before calling it a product bug. State a replay gap when correspondence of the trace is unknown.
- Create and Maintain demonstrate sensitivity in the checked target: break a detached model with a faulty transition, or break the implementation analyzed by a code verifier in scratch. A detached model's negative control shows model sensitivity, not that the checker can catch a source-only mutation. See [references/sensitivity.md](references/sensitivity.md) for the procedure.

## Verdicts

Report one verdict per requested formal property, qualified by its target and scope:

- **VERIFIED**: the prescribed formal check completed and the property held within the stated scope.
- **NOT VERIFIED**: the check found a counterexample to the named property on the stated target.
- **INCONCLUSIVE**: the tool, check completion, or a premise needed for the claim could not be established. A model-only finding does not resolve a current-code claim with unproven correspondence.

Report the exact command, the observed result, and evidence locations. Preserve raw checker output and any trace with secrets and private data redacted before sharing. Report generated-input tests separately as test evidence, never as a formal verdict.

## Ownership boundary

Create and Maintain edit only the verification artifact and the models, harnesses, or helpers it owns. A product bug is a finding, not a reason to redefine the property or change product code during formal verification.

If the user requests a chart for a checked transition model, call the Skill tool with `statechart`. Pass the exact model and configuration used for the check, the checked revision, and the raw checker evidence. The chart is a view of that check, not another proof or a condition for a verdict.
