---
name: engineering-principles
description: Shared decision principles for implementation, refactoring, architecture, review, debugging, verification, migration, and parallel work. Use when another engineering skill needs common judgment rules or the user names Laziness Protocol, Foundational Thinking, Redesign from First Principles, Subtract Before You Add, Minimize Reader Load, Outcome-Oriented Execution, Experience First, Exhaust the Design Space, Build the Lever, Model Behavior Structurally, Boundary Discipline, Type System Discipline, Make Operations Idempotent, Migrate Callers Then Delete Legacy APIs, Separate Before Serializing Shared State, Prove It Works, Fix Root Causes, Sequence Verifiable Units, Guard the Context Window, Keep Execution Unblocked, or Encode Lessons in Structure.
---

# Engineering Principles

A shared vocabulary for recurring engineering decisions. A principle is a default that changes a concrete choice, not a checklist item or a substitute for evidence.

## Precedence

Resolve conflicts in this order:

1. The user's explicit product decision.
2. The accepted spec and observable product behavior.
3. Repository standards and ADRs.
4. Runtime evidence.
5. These principles as defaults.

When two principles pull in different directions, preserve agreed behavior and a working feedback loop, then prefer the smaller reversible step. Surface the conflict when it materially changes the design.

## Apply selectively

1. Classify the current decision before acting: product experience, data shape, boundary, type, lifecycle, migration, verification, collaboration, or recurring lesson.
2. Scan every index trigger against the request, accepted artifacts, repository, and proposed change. This scan is the agent's job; the user does not need to name a principle.
3. Include every matched principle that could materially change the decision, normally one to four.
4. Add every principle the user names even when the independent scan would not have selected it, then reconcile it through Precedence.
5. Read each selected reference in full and translate it into a constraint, design choice, or proof obligation before acting.

Do not load an unmatched reference or run a 21-item review. Name a principle in the final report only when the user requested it, it resolved a conflict, or it drove a non-obvious decision.

Selection is complete when every material decision surface has been scanned and every matching or user-named principle is applied or ruled out by its boundary.

## Core

- **Laziness Protocol** — sizing a diff or considering another abstraction, wrapper, parameter, or layer. Read [references/laziness-protocol.md](references/laziness-protocol.md).
- **Foundational Thinking** — choosing core data structures, shared types, or scaffold that every later slice needs. Read [references/foundational-thinking.md](references/foundational-thinking.md).
- **Redesign from First Principles** — integrating a new requirement that does not fit the current shape. Read [references/redesign-from-first-principles.md](references/redesign-from-first-principles.md).
- **Subtract Before You Add** — extending or rewriting code that already carries dead or superseded paths. Read [references/subtract-before-you-add.md](references/subtract-before-you-add.md).
- **Minimize Reader Load** — tracing requires too many layers, aliases, mutable facts, or pass-through calls. Read [references/minimize-reader-load.md](references/minimize-reader-load.md).
- **Outcome-Oriented Execution** — an intermediate design, migration state, or compatibility path may outlive its purpose. Read [references/outcome-oriented-execution.md](references/outcome-oriented-execution.md).
- **Experience First** — product scope or UX is being traded against implementation convenience. Read [references/experience-first.md](references/experience-first.md).
- **Exhaust the Design Space** — a costly-to-reverse design has no strong precedent and several plausible shapes. Read [references/exhaust-the-design-space.md](references/exhaust-the-design-space.md).
- **Build the Lever** — repeated, broad, or uncertain work can be performed or proved by a reusable tool. Read [references/build-the-lever.md](references/build-the-lever.md).

## Architecture

- **Model Behavior Structurally** — rules repeat as conditionals or state assumptions across the codebase. Read [references/model-behavior-structurally.md](references/model-behavior-structurally.md).
- **Boundary Discipline** — parsing, validation, errors, or framework concerns are crossing into business logic. Read [references/boundary-discipline.md](references/boundary-discipline.md).
- **Type System Discipline** — types permit invalid domain states or external data enters as trusted. Read [references/type-system-discipline.md](references/type-system-discipline.md).
- **Make Operations Idempotent** — commands, jobs, migrations, or lifecycle steps may retry or resume after partial progress. Read [references/make-operations-idempotent.md](references/make-operations-idempotent.md).
- **Migrate Callers Then Delete Legacy APIs** — an internal API is being replaced while callers still exist. Read [references/migrate-callers-then-delete-legacy-apis.md](references/migrate-callers-then-delete-legacy-apis.md).
- **Separate Before Serializing Shared State** — concurrent actors may write the same branch, file, key, process, or object. Read [references/separate-before-serializing-shared-state.md](references/separate-before-serializing-shared-state.md).

## Verification

- **Prove It Works** — work is about to be called complete. Read [references/prove-it-works.md](references/prove-it-works.md).
- **Fix Root Causes** — a bug, failure, or performance regression is being diagnosed. Read [references/fix-root-causes.md](references/fix-root-causes.md).
- **Sequence Verifiable Units** — work spans several slices, commits, tickets, or migration batches. Read [references/sequence-verifiable-units.md](references/sequence-verifiable-units.md).

## Collaboration

- **Guard the Context Window** — a phase boundary, long investigation, large output, or parallel fan-out threatens useful context. Read [references/guard-the-context-window.md](references/guard-the-context-window.md).
- **Keep Execution Unblocked** — a reversible execution choice risks becoming an unnecessary human checkpoint. Read [references/keep-execution-unblocked.md](references/keep-execution-unblocked.md).
- **Encode Lessons in Structure** — a correction or instruction has become recurring. Read [references/encode-lessons-in-structure.md](references/encode-lessons-in-structure.md).
