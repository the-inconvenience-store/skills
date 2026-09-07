---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets. The behavior and test seams are already agreed; execute them rather than reopening product decisions.

Before editing production code, call the Skill tool with `engineering-principles`. Independently scan its full trigger index against the spec, ticket, repository, and intended change; read every matched leaf and turn it into a concrete constraint. User-named principles are mandatory additions, not a prerequisite for selection.

Call the Skill tool with `tdd` and work one red-green vertical slice at a time at the pre-agreed seams. Run typechecking and the narrow test files regularly, then the full test suite once after the implementation is coherent.

Call the Skill tool with `code-review` when the implementation and automated checks are complete. Address accepted Standards and Spec findings, then rerun the affected checks.

After the final review edits, call the Skill tool with `verification`. Prove the changed behavior through its real user or consumer surface. `INCONCLUSIVE` is not completion: report the exact gap instead of substituting tests or compilation for the missing observation.

Commit your work to the current branch as you work, using Conventional Commit-style commit messages. The final report names the automated checks, the verification verdict, the observed result, and any principle that drove a non-obvious decision.
