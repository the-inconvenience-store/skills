# Maintain project formal verification

A formal check proves a property of what it describes. When the code changes and the verification does not, the check can keep passing while it describes code that no longer exists. That pass is the dangerous case, because it looks like a proof. This workflow handles the changes that skipped the check: merges, edits made without the project record, and drift that builds up across many commits.

## Outcomes

Report correspondence and the property verdict separately. Give each check an alignment outcome:

- **in sync**: no change since the last sync alters what the check describes.
- **updated**: the source or design changed, and the verification now describes it.
- **blocked**: correspondence or the required recheck could not be established. Say exactly why.

An in-sync or updated check can expose a **bug**: the verification describes the current code, and the code breaks the property. This is a finding about the code. It is not drift.

## Edit scope

Edit only the verification: project records, models, harnesses, and property files it owns. When a property fails on the current code, keep the property as stated and report the failure. Keep verification changes separate from any product fix.

## Pass

For a design-only check, compare against the accepted design and track the checked model version instead of a source commit. Its counterexamples are design findings, not product bugs.

1. **Find the checks.** Read `docs/agents/formal-verification/README.md` and every check record in scope, or the one the user named. Collect the property, the code it covers, the bounds and assumptions, the command that runs it, and the commit where it was last confirmed to describe the code. If no artifact exists, route to Create. If the record has no sync commit, use the last commit that changed the verification files as a starting point for review; say that you did and do not treat it as evidence of alignment.
2. **Run it as it is.** Run each check once before you change anything, and record the result. A pass here does not tell you that the code is correct. It tells you that the old description still holds. A failure here can be drift or a bug. Do not decide which until step 5.
3. **Read every change to covered code.** Diff the covered files from the sync commit to the current revision, including local edits in scope, and read each commit message. Also look for code that moved: a covered function that is renamed, split, or moved to another file is still covered code. Also look for new code that touches the state that a check guards, such as a new function that writes the same fields. For each change, decide which of these it is:
   - **No effect.** The change does not alter anything the verification describes, such as formatting, comments, or code paths that the verification does not cover. Check this against the model or harness, not against the commit message.
   - **The verification no longer describes the code.** A step that was one indivisible action is now two, a branch was added or removed, a check moved, a new path reaches the guarded state, or a value now has a different range. The model or harness must change.
   - **The promise changed on purpose.** The change alters what the code promises, and evidence in the change says that this is intended: the doc comment, the tests, the changelog, or the commit message. The property must change, and you must cite that evidence.
   - **The promise may be broken.** The code changed, and no evidence says that the promise changed. Treat a failure that follows as a bug candidate.
4. **Update from the code, not from the result.** Change the model or harness so that each changed part again points to code that a reviewer can open, and keep one indivisible step in the code as one step in the verification. Write the update from the code before you rerun, and do not shape it by what makes the check pass. Change a property only for a promise that changed on purpose. Write down the old wording, the new wording, and the evidence. Keep the bounds unless the change makes them wrong. If you must reduce a bound, say so in the report.
5. **Rerun and judge each result.** Run each affected check using the revised record. Reestablish reachability and re-prove each affected negative control in scratch using [sensitivity.md](sensitivity.md), then remove the break and restore the baseline.
   - **Pass:** report what actually held. A passing stale model is not evidence about current code.
   - **Fail:** replay the counterexample against the real code, step by step. If a step is impossible, fix the verification and say what was wrong. If every step is established, report the bug and the harm in the code's own words. Include the introducing commit if established and a cheap real-code reproduction if available. If correspondence of the trace is unresolved, report a model finding and the replay gap rather than a product bug.
6. **Update the project record.** Update the covered code, action-to-source mapping, commands, bounds, and assumptions. Follow the finalized record as the next agent would and report any step you could not run. Move the sync commit only to a source commit confirmed to match, including when an aligned check exposes a bug. Do not move it for a blocked check or to stand for uncommitted changes.

## Report

Tell the user, for each check:

- the alignment outcome, the property verdict, and the commits that you read;
- what changed in the verification and why, citing the evidence if the promise changed on purpose;
- the rerun result and the break that showed the updated check can still fail;
- each established bug: the counterexample as steps in the code's words, the harm, and the introducing commit if known;
- what the verification still does not cover, including new code that it should cover and does not.

Say outright which failures were drift in the verification and which were bugs in the code. For a check that passed before you updated it and fails after, say that the old pass was on a stale description.

