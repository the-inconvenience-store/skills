Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=show-me-your-work
```

```bash
npx skills update show-me-your-work
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/show-me-your-work)

## What it does

`show-me-your-work` keeps a **decision trail** for work already underway. It records what was chosen, why, what evidence supported it, and what happened, without turning every action into a log entry.

## When to reach for it

You invoke this by typing `/show-me-your-work`; it does not run on its own. Use it before stepping away from a long run or when a reviewer will need to follow decisions back to their evidence.

## Common questions

**Does it publish the log?** No. The trail stays local unless you ask to commit or publish it.

**How does it correct a mistaken entry?** It appends a correcting row, so the original claim and what superseded it remain visible.

## Where it fits

Use it during a run when the decision trail matters. [Why](https://aihero.dev/skills-why) reconstructs rationale after the fact; [handoff](https://aihero.dev/skills-handoff) prepares another agent to continue. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) helps choose.
