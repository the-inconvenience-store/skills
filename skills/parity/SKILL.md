---
name: parity
description: Implement supplied designs in an existing project and verify visual parity against the references.
disable-model-invocation: true
---

# Parity

Implement supplied designs using the project's components. **Parity** means the running UI matches the reference at the same viewport and state, demonstrated through inspected screenshots.

This skill owns the visual implementation loop, not a second engineering workflow. Follow project requirements for testing, review, commits, and deployment. When used inside `/implement`, run those gates once through the enclosing workflow.

## 1. Scope and inspect

Open the supplied folders, archives, attachments, design files, or live pages. Preserve originals; extract ZIPs separately with relative asset paths intact. Keep a compact checklist of the requested screens, supplied states and viewports, and their reference sources. Distinguish authoritative designs from inspiration; resolve material conflicts before implementing the affected screen.

For runnable exports, read the relevant HTML, CSS, scripts, and assets **and** render them with browser tools. Navigate the supplied states, take baseline screenshots before production edits, and open the applicable supplied images, including attachments. For screenshots or design files, inspect the actual reference. Store captures outside tracked source, paired by checklist item. Measure styles and geometry when needed to reproduce a detail or resolve a mismatch; label screenshot-derived estimates.

Default to existing application contracts. Identify reference controls or copy that would require new backend capabilities early, and report them separately. Implement those capabilities only when explicitly in scope. Approval of one capability does not authorize other capabilities subsequently discovered. Continue independent visual work while a scope decision is pending.

**Done when:** every requested screen has an inspected reference and baseline, and missing capabilities or access gaps are identified. Mark inaccessible targets unverified rather than inventing them.

## 2. Implement and make a first visual pass

Find and reuse the project's components, tokens, fonts, icons, assets, and layout patterns. Compose or extend them through existing conventions rather than importing the prototype's architecture. Surface a design-system constraint that prevents fidelity instead of silently compromising the reference or forking a parallel component system.

Implement the requested screens with real application behavior, preserving accessibility and existing contracts where designs are silent. Use representative data through existing development or test mechanisms, not production-hardcoded fixtures or inert controls.

Open each screen in the running app, exercise the in-scope interactions, and inspect screenshots against the baseline at matching viewport, scale, state, content, theme, and scroll position. Wait for fonts and assets to load; preserve image proportions. Use side-by-side views, overlays, or crops as useful. Record concrete differences, not just a similarity score.

Complete a first visual pass across the requested screens before broad validation. When a target is blocked, record the gap and continue the accessible targets.

**Done when:** each accessible checklist item has an implementation comparison and the in-scope corrections are known.

## 3. Batch corrections

Fix discrepancies in coherent batches, prioritizing layout and geometry, typography, then spacing, colors, borders, and assets. Fix introduced regressions and in-scope interaction failures. Report unrelated bugs, infrastructure failures, and unsupported capabilities separately; do not turn them into an open-ended repair project. If one prevents an in-scope observation, mark that target blocked.

Recapture and inspect only targets affected by the changes, including shared-component consumers where relevant. Reuse successful captures and interaction evidence until a relevant change invalidates them. Keep the reference fixed unless source evidence or a user decision changes it.

Run affected checks during corrections and follow project policy for behavior coverage. Unless that policy requires otherwise, run broad checks once the UI is visually coherent, then rerun only checks invalidated by subsequent edits. Rebuild or redeploy what is necessary to observe changed code, without adding a new release procedure.

**Done when:** in-scope visual and interaction differences are resolved or explicitly accepted, affected comparisons are current, and required checks have run. Blocked targets remain unverified.

## 4. Close the remaining proof gaps

Reuse the comparison loop's screenshots and interaction results as final proof. Exercise only in-scope paths still lacking current evidence, including persistence where changed behavior promises it. A separate verification phase must not restart successful comparisons or checks.

Report checklist coverage, paired evidence locations, checks run, accepted deviations, and blockers. Separate unrelated findings and unsupported capabilities from the implementation result. Claim parity only for compared viewports and states; distinguish estimates and inferred layouts from measured matches.

**Done when:** every requested target is accounted for as compared, accepted deviation, or blocked. Declare full parity only when all targets have current proof with no unresolved in-scope discrepancy; otherwise report the incomplete targets precisely.
