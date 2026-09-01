# Git hooks

Git hooks are local feedback, not the complete gate. Keep them quick enough that developers leave them enabled; put comprehensive checks in CI.

## Inspect

- Check tracked hook configuration, `git config core.hooksPath`, package scripts, and any prepare/install lifecycle.
- Reuse an existing manager. Installing a second manager can silently replace the first manager's hooks.
- Identify partially staged workflows, monorepo boundaries, and the commands CI already trusts.

Read current official documentation only for the detected or proposed manager.

## Propose

Offer lifecycle checks because they serve the project, not because hooks exist:

- **pre-commit:** fast formatting and linting of the affected files or packages;
- **pre-push:** slower typechecks or focused tests when the user wants a local gate;
- **commit-msg:** a commit convention only when the project uses one;
- **post-merge or post-checkout:** dependency installation only when the user accepts the surprising side effect.

State the expected runtime and the CI backstop. Each hook is independently optional. If the repository has no manager, recommend one that fits its existing toolchain and explain the installation behavior on a fresh clone; avoid presenting a catalogue unless the user asks for alternatives.

## Implement

- Use repository-relative, cross-platform commands consistent with the project.
- Keep nontrivial logic in a testable repository script; let the manager handle lifecycle wiring and staged-file plumbing.
- Operate on staged files or affected packages where the tool supports it. Preserve unstaged portions of partially staged files and re-stage intentional formatter changes.
- Make no-op paths exit successfully and cheaply.
- Ensure a normal dependency install activates tracked hooks when the chosen manager supports that. Otherwise document the one-time activation command plainly.
- Keep secrets, environment-specific paths, and user-global hook configuration out of tracked files.

## Verify

Exercise scripts directly or use the manager's supported test mechanism:

- relevant input runs the intended command;
- irrelevant input exits without work;
- a failing check returns a failure and useful output;
- paths containing spaces are handled;
- partially staged changes remain intact;
- measured runtime fits the agreed budget.

Do not create commits, merges, checkouts, or dependency installs solely for verification without the user's approval. Report fresh-clone activation as unverified when it cannot be checked safely.
