# Explain the Number

**Apply when:** a measured result will support a performance claim or a decision, including a benchmark or an evaluation.

Before running, state the decision the measurement informs, the smallest effect that would change it, and the expected noise. Define successful work at the measured boundary so an error, skipped operation, or unused result cannot masquerade as an improvement.

Compare equivalent inputs, outputs, and successful work under representative settings. Check the measured path actually ran. For a performance claim, identify what bounds the result from counters or a profile taken separately from the timed trials. Check whether a local speedup matters on the path the user waits for before claiming an end-to-end gain.

When choosing between alternatives, interleave repeated trials to reduce drift. Report the workload, metric and unit, central result, run count, spread, and, for performance, the observed limiter. If the effect is within the run-to-run spread, report no measurable difference. If successful work, comparability, or the claimed limiter cannot be established, mark the comparison inconclusive and name the gap.

For an explicitly requested ballpark, one run can suffice: confirm the work ran and succeeded, label it a single-run estimate, and do not use it to select a winner.
