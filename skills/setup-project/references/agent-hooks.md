# Agent hooks

Agent hooks run inside a developer's coding harness. They are optional personal or team tooling, not a prerequisite for a working repository. Read this reference only when the user asks for them.

## Decide the boundary

Ask which harnesses and configuration scope the user wants. Project-level configuration travels with the repo; user-level configuration is personal. Read each selected harness's current official hook documentation before proposing files, events, payload fields, or response shapes.

The useful starting hooks are narrow:

- **Format the edited file:** layout-only, fast, and fail-open while code is incomplete.
- **Block edits to generated files:** derive paths from generator configuration or generated headers, and redirect the agent to the source plus regenerate command.

Offer end-of-turn lint only when the project's lint command is fast and the user wants the harness to prevent a dirty handoff. General lint-on-every-edit is noisy during multi-edit refactors and should require an explicit request.

## Implement

- Use the formatter and generated-path definitions already approved for the project.
- Touch only the file named by the verified event payload.
- Keep edit-time formatting layout-only; avoid fixes that remove imports or rewrite incomplete code semantically.
- Let formatting failures pass without interrupting the edit. A generated-file denial should fail closed with a message naming what to edit instead.
- Merge into existing harness configuration and preserve unrelated hooks.
- Keep harness-specific scripts small. Configuration examples in product documentation are more reliable than copied examples here.

## Verify

- Feed the script a captured or documented payload without changing a real user file.
- Confirm formatting changes a disposable, badly formatted file and ignores unsupported or syntactically incomplete input safely.
- Confirm the generated-file guard rejects a disposable matching path, permits a normal path, and returns an actionable redirect.
- State which harnesses and scopes were configured and which remain unsupported or unverified.

Agent hooks are complete when the accepted behavior works in the named harnesses. The repository's lint, format, git-hook, and CI setup must remain useful without them.
