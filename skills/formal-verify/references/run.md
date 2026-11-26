# Run project formal verification

## 1. Name the property and find the route

State the promise, its target (a design model or actual code), the harm if it fails, and the requested scope. Use the user's wording and the project contract to choose the property, not whichever existing check passes. Read `docs/agents/formal-verification/README.md` and only the matching records.

If there is no matching record, use [tool-choice.md](tool-choice.md): prefer an existing direct checker, or use a scratch check supported by the available tools. Report the missing reusable route. Write no permanent project files, even if a reusable route would help.

**Done when:** each requested property has a selected command or a concrete reason no formal check can run.

## 2. Establish the target and revision

Identify what will be checked: the actual code revision under review (identify any relevant local changes), or the exact model and configuration. Confirm what the command and harness actually analyze. For code claims backed by a detached model, compare relevant source and configuration against the last aligned commit, including moved code and new writers. Establish that actions, guards, and atomicity still correspond. If correspondence cannot be established, report the gap and label any completed run as model-only evidence. Leave drift repair to Maintain.

**Done when:** the checked target is identified precisely and any narrower scope than requested is explicit.

## 3. Execute and capture

Run the recorded command with its tool version and configuration. Isolate checker-generated files and scratch inputs outside the project tree. Capture the command, tool output, exit status, actual bounds and assumptions, reachability evidence, and any counterexample. Inspect which properties the checker completed; a timeout, unsupported check, or early exit cannot establish properties that were not checked.

For a counterexample, tell the sequence in the code's or design's words. For a code claim, replay it against the real implementation one step at a time. Include a cheap reproduction if feasible, and distinguish an impossible step (verification drift) from an unconfirmed step (replay gap). Preserve a liveness loop when one is part of the counterexample.

**Done when:** each requested property has raw evidence or a named observation gap, and no model-only trace is called a product bug.

## 4. Clean up and report

Remove run-owned scratch files and stop only processes this run started. Keep evidence outside cleanup-owned scratch. Report exactly one verdict per requested formal property using the skill's verdicts. Include the command, target and revision or model/configuration, scope, observed result, evidence, and gaps. Report generated-input results as tests; if they were the only evidence for a requested formal claim, the formal claim remains `INCONCLUSIVE`.

**Done when:** evidence remains accessible and no permanent project files or run-owned residue were left behind.
