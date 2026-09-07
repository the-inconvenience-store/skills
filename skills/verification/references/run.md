# Run project verification

Prove the behavior named by the user, spec, ticket, or calling skill on the real surface.

## 1. Name the proof

Before launching anything, state:

- The surface.
- The user path or public consumer call.
- The observable result.
- Any durable side effect.
- Behavior that must remain unchanged.

If the source request does not make these clear, infer what code and prior decisions establish. Ask only when the missing point is a genuine product decision.

**Done when:** the proof statement names every result that will determine the verdict.

## 2. Locate the driving route

Read `docs/agents/verification/README.md`, select the surface, then read its README and only the relevant feature files.

If the project artifact is absent, use the strongest direct route available from repository conventions and runtime tools. Do not create permanent verification documentation or helpers during Run. Report the missing reusable route with the verdict.

**Done when:** one exact driving route is selected and every missing reusable instruction is named.

## 3. Establish a known instance

Follow Launch exactly. Run Doctor before the first interaction and again after any surprising or failed drive. If Doctor cannot detect a wedged UI or contaminated session, reset to a known state or relaunch instead of continuing on hope.

Never attach to an unverified process or shared user session. Respect the surface's Isolation section. Record the process, session, profile, port, data directory, or other handle needed to clean up only what this run starts.

**Done when:** the instance has passed Doctor and every resource this run must clean up has a recorded handle.

## 4. Drive and observe

Exercise the public path. Capture both the action and the result. Check durable side effects through a valid read path when the behavior promises them.

Do not use internal setters, test-only endpoints, direct database mutation, or mock echoes unless the production design itself exposes that boundary. A test may support the result but cannot replace this drive.

Store evidence where Cleanup will not delete it. Redact secrets and personal data before quoting or sharing captures.

**Done when:** every claimed result has direct evidence or an explicit observation gap.

## 5. Clean up

Stop only processes and sessions started by this run. Remove its scratch profiles, fixtures, and data. Preserve evidence. After a failed attempt, clean residue before retrying.

**Done when:** run-owned processes and scratch state are gone and the captured evidence remains.

## 6. Return the verdict

Return exactly one:

- **VERIFIED** when the full path ran and every named result held.
- **NOT VERIFIED** when the path ran and a result failed.
- **INCONCLUSIVE** when the path or result could not be observed reliably.

Include the exact command or interactions, what was observed, evidence paths, cleanup result, and any gap. Never round INCONCLUSIVE up to VERIFIED because tests or compilation passed.
