# Create project formal verification

A test checks the cases that someone thought to write. Formal verification checks every case in a stated scope. Find the part of the repo where that matters most, verify one property of it, and leave a project-local record that lets the next agent check a change against that property. Write for an agent who reads it cold, mid-change, and has never seen your work. The user must be able to trust the result and act on it without learning the verification language.

## Choose the target from the code

Answer from the codebase, and ask the user only what you cannot observe. If the user named an area or a bug, start there.

A good target is a promise the code makes, where a break harms users and tests rarely reach the case that breaks it. Choose the strongest such target in the repo, not the one that is easiest to verify. State the property and harm in one plain sentence each, then say which success path and preconditions must be reachable before choosing a tool.

## Let the question choose the tool

Use [tool-choice.md](tool-choice.md) to select the least costly tool that answers the question. Prefer a suitable existing checker. If only generated-input tests are possible, report the tool gap and the test result separately; do not publish a formal record for a test-only check.

## What makes it good

- **True to the code.** Every part of a code-facing model or proof points to code that a reviewer can open. What the verification treats as one indivisible step is one indivisible step in the code. Names come from this repo. Label a design-only model as such.
- **Able to fail.** Show each property failing on a deliberately broken variant of the target it checks, as described in [sensitivity.md](sensitivity.md).
- **Findings stay findings.** When the current code breaks the property, report it with the counterexample in the code's terms. Keep the property and product code as they are.
- **Honest about scope.** Say what is verified, under which bounds and assumptions, and what is left out. A pass covers the model or the bound, not the whole system.
- **Readable without the tool.** Tell a counterexample as a short sequence of steps in the code's words.
- **Cheap to rerun.** One command, a reproducible tool version, and a run short enough that the next agent will use it on a relevant change.
- **Kept in step with the code.** Record which files and functions each check covers, and the commit at which you last confirmed that the verification describes them.

## Write the project record

Use [project-format.md](project-format.md). From the record alone, the next agent must be able to tell whether a change touches the verified code, run the check, tell a real bug from a modeling error, and update the verification when a change is intended. Use this repo's real commands, paths, and nouns, and leave no placeholders.

## Prove it before you hand off

Follow the record as the next agent would. Run the baseline at the intended revision, observe the success path and antecedent, and capture the result. Perform the documented negative control in isolation, remove the break, and rerun the baseline. The result must be back where it started: passing, or failing only on the findings you will report. If the record misses the break or a step does not run, fix the record or the verification, not the scratch change. A record whose command and sensitivity have not been demonstrated is still unproven; report the gap.

## Hand off

Tell the user what you verified, which tool you used and why, the bounds, what the check found in plain words, how to run it, and what it does not cover. Include the baseline, sensitivity evidence, and restored result. Suggest a second target only if you found a close one. Point the user at Maintain for bringing the verification back in line after changes that did not recheck it.

