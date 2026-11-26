# Project formal verification format

The artifact is portable agent-facing documentation, not a harness-specific installed skill. The unit of coverage is an independently runnable check, not a user-facing feature.

## Layout

`docs/agents/formal-verification/README.md` indexes one `<check>.md` record per independently runnable check. Give each entry a plain-language property and a routing cue for which areas or changes should use it. Keep models, proof files, harnesses, and scripts in established project locations and link them from the record. Keep real-surface driving instructions in their own artifact.

## Check record

Use these sections in each record:

- **Property**: the promise, the harm if broken, and the success path and any antecedent that must be reachable. If one command checks several named properties, identify each separately.
- **Target and coverage**: a detached model, a design-only model, or a verifier analyzing real code. Name the covered files, symbols, entry points, and state writers. Where a model represents code, map its actions, guards, and atomicity to source. Where a tool analyzes code, identify the entry point, harness, and any stubs or abstractions.
- **Run**: one exact command, its working directory, tool and version, prerequisites, and the configuration or proof files it uses. Explain the expected success, violation, and incomplete-run signals so an agent can distinguish a failing property from a broken command.
- **Scope**: constants, bounds, inputs, environment assumptions, fairness, reductions, and excluded cases as applicable. For an unbounded claim, identify what actually discharges it.
- **Negative control**: the reversible change and commands needed to produce a violation in isolation, its expected diagnostic or distinguishing trace, and the baseline to restore. State whether it demonstrates model or code-verifier sensitivity and name any independent implementation replay.
- **Last aligned revision**: the source commit confirmed to match the record, not merely the last commit on which a checker ran. Design-only artifacts name the model version and state that no code correspondence is claimed. Keep this separate from the last property verdict.

Write exact repository instructions, not generic examples or placeholders. A future agent must be able to tell whether a change touches the check and run the recorded command cold.

## Evidence

Put commands, status, raw checker output, traces, and control results in run-owned evidence outside cleanup-owned scratch and the project tree. Link the evidence from the report. Keep the actual checked scope visible even when a shortened trace or chart is shown; redact secrets and private data before sharing.
