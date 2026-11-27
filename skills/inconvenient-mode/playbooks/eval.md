# Agent workflow evaluation

1. Name the behavior under test and write observable pass criteria before running it. Keep the rubric separate. Use the same realistic task, repo starting state, and permissions across variants, with separate workspaces for writes. Do not signal the variant or desired behavior in the candidate task unless that cue is the variable under test.
2. Run the authorized comparison with the harness's available tools. Compare artifacts against the same rubric under neutral labels before revealing variants. If checking skill selection matters, identify actual tool calls from available runs or authorized, workspace-scoped transcripts. Treat self-report as a claim, not a trace.
3. Report variant, criteria, results, and limits. A small run can expose a failure mode; it does not estimate a reliable success rate. Keep results separate from advice about whether to adopt the change.
