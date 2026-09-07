---
name: verification
description: Create, run, or maintain project-local verification of real user-facing behavior. Use when the user asks to verify or prove a change on the real app, create a repeatable app-driving workflow, audit or refresh verification instructions, or when implementation needs evidence beyond tests and compilation.
---

# Verification

Prove behavior through the **real surface** a user touches: the running UI, CLI, service, mobile app, or library interface. Tests and compilation may support the proof; they do not replace exercising the changed path.

## Route

Choose one branch from intent and repository state, then read only its reference:

- **Create** — the user asks to create, set up, or bootstrap repeatable project verification. Read [references/create.md](references/create.md) and [references/project-format.md](references/project-format.md).
- **Run** — the user asks to verify behavior, another skill needs completion evidence, or a change must be proved on its real surface. Read [references/run.md](references/run.md). If project instructions exist, they own how the surface is driven.
- **Maintain** — the user asks to audit, update, refresh, or repair existing verification instructions or their feature map. Read [references/maintain.md](references/maintain.md) and [references/project-format.md](references/project-format.md).

Intent alone is not enough. Inspect `docs/agents/verification/` before choosing:

- Maintain with no existing verification artifact routes to Create.
- Run with no existing artifact performs the strongest direct check available and reports the missing reusable route. It does not create permanent files without an explicit Create request.
- Create with an existing artifact stops and routes to Maintain unless the user explicitly wants replacement.

## Proof standard

A valid proof:

1. Exercises the public path a user or consumer takes.
2. Captures the action and the resulting observable state.
3. Checks durable side effects when the behavior promises one.
4. Uses the code and configuration that actually ship.
5. Cleans up processes and scratch state created by the run while preserving evidence.

Do not substitute an internal setter, mock-only path, cached screenshot, file timestamp, or agent report for the real result.

## Verdicts

Every Run ends with exactly one verdict:

- **VERIFIED** — the intended path ran and every named observable result held.
- **NOT VERIFIED** — the path ran and a named result failed.
- **INCONCLUSIVE** — the path or result could not be observed reliably. This is not a pass.

Report the command or interaction, the observed result, the evidence location when one exists, and any verification gap. Redact secrets, authentication material, and personal data from captured output.

## Ownership boundary

Create and Maintain may edit only the verification artifact and helpers it owns. Maintain never changes product behavior to make its instructions pass. A mismatch is either verification drift, which it fixes, or a product regression, which it reports.
