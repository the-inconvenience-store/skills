# Investigation

1. Name the question and evidence source. For current code or ownership, call the Skill tool with `how`. For rationale, call the Skill tool with `why`. For external facts, use primary sources; call the Skill tool with `research` only if the user wants a written repository artifact.
2. For an existing trace or profile, use that capture first. Identify its format, isolate the relevant interval or retained objects, and map the evidence to a source location when symbols allow. For runtime forensics, capture the narrowest useful profile on the matching surface. Use read-only tooling or an authorized isolated repro; separate direct observation from any hypothesis a capture cannot confirm.
3. Answer the question with source or artifact pointers and the strongest supported claim. Keep read-only work read-only. A fix is a separate route once the user asks for one.
