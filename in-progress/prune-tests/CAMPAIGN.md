# Pruning campaign

Use for a whole subsystem or repository. Apply the [value bar](SKILL.md#value-bar) and [audit guide](references/audit.md); this sequence replaces the local audit sequence.

## 1. Baseline and lanes

Record the source revision and known test results. Run uncovered in-scope suites to establish their baseline; preserve user-reported failures as evidence rather than rerunning to confirm them. Separate product failures from pruning work.

Inventory all owned test files, parameter tables, shared-boundary coverage, and live or QA scenarios. Assign each to one **lane** by production owner, not filename prefix. Shared harnesses have one integration owner.

Done when every test surface belongs to one lane and has a recorded baseline result or explicit execution limitation.

## 2. Read-only ledger

Read each lane's tests and production paths using the audit guide. Record a classification and evidence for every declaration, splitting parameter rows when necessary. Keep discovery read-only until all lanes are accounted for. Independent lanes may be investigated in parallel.

Done when every declaration and QA scenario has a ledger entry, including unresolved evidence.

## 3. Layer plan

Review the ledger by contract rather than treating it as a deletion list. Identify redundant layers and name each keeper, the assertions it must absorb, retired files, distinct boundary risks that remain, and obsolete support or production seams.

Done when each lane has an evidence-backed cutover plan and every retained contract has a keeper. Exclude unresolved candidates from deletion.

## 4. Cutover

Apply the plan lane by lane, transferring unique assertions before removals. Serialize shared-harness changes through the integration owner. Update affected CI routing and test inventories. Check remaining callers before removing obsolete support and production seams.

Run the affected keepers after each lane's cutover; batch edits before each check rather than checking every individual edit.

Done when every lane plan is applied and its keepers pass or recorded baseline failures remain accounted for.

## 5. Preservation review

Have an independent reviewer compare deleted coverage against keepers, using the ledger and actual assertions. Review by boundary group; look for lost contracts, unreachable negative cases, and fixture-supplied outcomes. If independent review is unavailable, report that limit and perform a separate preservation pass.

Resolve each finding with restored proof or source-backed rejection. Apply the local workflow's [verification requirements](SKILL.md#4-verify-and-report) to repaired assertions, transferred coverage, and any contracts restored during review.

Done when every finding has a disposition and every repaired or transferred contract has a failing control and passing keeper. Report unavailable proof as an incomplete verification item.

## 6. Reconcile and hand off

If the source revision changed during the campaign, inspect intervening changes in affected owners and tests. Port newly added unique contracts into keepers before retiring their old homes, then rerun only affected proof and required repository checks.

Report lanes, retired layers, keepers, preservation findings, removed seams, unresolved candidates, and validation evidence. Count production, test, and support changes separately if reporting size; deletion totals are outcomes, not targets.

Done when every planned lane and intervening contract is accounted for, with execution and review limitations stated explicitly.
