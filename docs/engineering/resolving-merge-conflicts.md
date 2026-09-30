> **Archived.** This skill was removed from the plugin in v1.5.0, following its removal upstream, and is no longer maintained. Nothing replaces it: the agent works through a merge or rebase conflict without a dedicated skill. The page stays up for reference.

## What it did

`resolving-merge-conflicts` worked through an in-progress git merge or rebase conflict, hunk by hunk, and finished the operation — resolved, checked, and committed.

It resolved by **intent**, not by text. Before touching a hunk it traced each side back to its **primary source** — the commit message, the PR, the original issue — to understand why the change was made, then preserved both intents where they were compatible. It never invented new behaviour to paper over a clash, and it never reached for `--abort`: the merge always got finished.

## Resolving by intent

The idea is worth keeping even without the skill. The trap in a conflict is treating it as a text problem — picking "ours" or "theirs" to make the markers go away. Each side of a hunk exists because someone wanted something; the resolution has to honour both wants where it can, and where they are genuinely incompatible, pick the one that matches the merge's stated goal and name the trade-off out loud.

That is why the primary sources matter. You cannot preserve an intent you have not read, so the work starts in the history — commits, PRs, tickets — not in the diff. Say that much in the prompt and you get most of what the skill gave you.

## What to reach for instead

| Your situation | Where to go |
| --- | --- |
| Mid-merge or mid-rebase, conflict markers in the tree | No skill. Ask the agent directly, and point it at the primary sources |
| Merge finished, something now misbehaves for reasons you can't see | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |
| Planning how to slice work so branches collide less | [to-tickets](https://aihero.dev/skills-to-tickets), which sequences wide refactors as expand–contract |

## Where it fitted

A reach-for-it-anytime standalone, off every flow: you invoked it at the moment a merge or rebase stalled, and it handed you back a clean, committed tree. For the current map of what this repo does ship, see [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
