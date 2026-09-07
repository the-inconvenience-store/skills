# Research an unlisted ecosystem

Use this branch when the repository contains a language or framework without a bundled setup reference. Research and propose the equivalent guardrails; do not leave the ecosystem uncovered merely because this skill has no local catalogue.

## Establish the target

From the repository, identify:

- language, compiler/runtime, framework, and package-manager versions;
- application, library, CLI, service, generated-code, and monorepo boundaries;
- existing formatter, analyzer, tests, CI, suppressions, and conventions;
- constraints in official framework guidance or the repository's contributor docs.

Run existing checks before selecting replacements. A coherent established setup is evidence, not an obstacle to overwrite.

## Research

Use current high-trust primary sources:

1. Official language and framework style, compiler, analyzer, and security guidance.
2. Official documentation for the ecosystem's maintained formatter and linter/analyzer candidates.
3. Maintainer-owned recommended presets and framework or dependency plugins.
4. Current release and compatibility information for the repository's language/runtime version.

Compare candidates on rule coverage, maintenance, configuration stability, editor support, execution time, monorepo behavior, and migration cost. Prefer a standard maintained toolchain over a larger pile of obscure plugins, but keep an existing tool when it already covers the agreed standards.

Record direct source links for the recommendation. Blog posts and copied configs may provide leads; verify every consequential claim against a primary source before it enters the proposal.

## Build the equivalent baseline

Map the ecosystem's exact rules and tools to every applicable guardrail below:

| Guardrail | Research target |
| --- | --- |
| Correctness | Compiler warnings, suspicious constructs, unreachable or ignored failures |
| Type and resource safety | Nullability/types, async work, errors/exceptions, files, sockets, database results, cleanup |
| Complexity and size | Cyclomatic and cognitive complexity, function/file size, nesting, parameter count |
| Duplication and readability | Duplicate code/branches, needless control flow, shadowing, confusing names |
| Unfinished work | TODO/FIXME markers, empty bodies, focused or skipped tests, not-implemented stubs |
| Magic values | Repeated literals and unexplained numeric constants with idiomatic exceptions |
| Escape hatches | Broad suppressions, unsafe casts, disabled warnings, ignored analyzer output |
| Dependencies and architecture | Forbidden imports/references, cycles, layer or package boundaries |
| Formatting and naming | Canonical formatter plus accepted file, namespace, module, and identifier conventions |
| Security | The ecosystem's maintained security analyzers and framework-specific unsafe APIs |
| Tests | Test-quality rules, race/concurrency checks, framework-specific mistakes |
| Framework and libraries | Maintainer-provided analyzers for detected frameworks and everyday dependencies |

Use the TypeScript, React, and Go catalogues as examples of coverage and decision quality, not as sources of rule names for another language.

For each proposed group, name the exact rules or preset, default severity, prerequisites, expected runtime, and likely migration friction. Calibrate numeric thresholds against the repository rather than translating numbers blindly between languages.

If no maintained rule covers a target, search for a precise configuration or compiler feature. Propose a custom rule only when the failure is syntactically detectable and the maintenance cost is justified. Otherwise name the gap honestly and decide with the user whether a test, architecture boundary, or short convention is the appropriate substitute.

## Place the checks

Research the ecosystem's normal project commands and hook integration. The proposal must provide:

- format-fix and format-check commands;
- a blocking lint/analyze command for CI;
- a fast local subset for pre-commit when useful;
- slower compilation, type, security, or test checks at pre-push or CI;
- activation behavior for the repository's existing or approved hook manager.

CI is the complete gate. Local hooks remain fast enough to keep enabled.

## Proposal

Tell the user that this ecosystem was researched because no bundled baseline exists. Present one recommended toolchain and the relevant rule groups, citing the primary sources that support it. Include alternatives only for material tradeoffs such as coverage versus speed or replacement versus coexistence.

Wait for approval exactly as the main skill requires. Research chooses what to recommend; it does not authorize installation.

## Verify and report

- Confirm every configured rule, preset, and option exists in the installed version.
- Run format, lint/analyze, aggregate, and CI-equivalent commands.
- Demonstrate representative failures across the approved high-value groups with disposable code, then restore a passing state.
- Exercise accepted hooks through controlled inputs and measure their runtime.
- Report the sources consulted, selected versions, pre-existing findings, declined groups, and remaining coverage gaps.

This branch is complete when the researched ecosystem receives an approved, working setup equivalent in rigor to the bundled stacks—not when the agent has merely named popular tools.
