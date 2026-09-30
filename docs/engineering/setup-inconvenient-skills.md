Quickstart:

```bash
npx skills add the-inconvenience-store/skills
```

Select `setup-inconvenient-skills`, `guardrails`, and `verification`; setup calls the other two.

```bash
npx skills update setup-inconvenient-skills guardrails verification
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/setup-inconvenient-skills)

## What it does

`setup-inconvenient-skills` teaches one repo how the engineering skills should behave in it: where issues live, what the triage labels are called, where domain docs sit, which development guardrails apply, and how future agents prove behavior through the real surface.

It first writes the repository-specific configuration under `docs/agents/`, discovered from the actual repo and confirmed with you rather than guessed. It then calls the owning skills: [guardrails](https://aihero.dev/skills-guardrails) establishes the approved quality baseline, and [verification](https://aihero.dev/skills-verification) creates or maintains the app-driving route. The setup remains prompt-driven rather than a deterministic scaffold.

## When to reach for it

You invoke this by typing `/setup-inconvenient-skills` — the agent won't reach for it on its own.

Reach for it **once per repo, before the first use of any other engineering skill**. Re-run the full setup only to switch foundational configuration or start over. Day-to-day changes belong to the owning surface: edit tracker or domain config directly, run [guardrails](https://aihero.dev/skills-guardrails) when the quality strategy changes, and run [verification](https://aihero.dev/skills-verification) with Maintain when application surfaces move.

## Repository-specific decisions

It leads each with a recommended answer you can accept in a word, and skips whatever it can already infer — so most runs are a couple of quick confirmations:

- **Issue tracker** — where work is tracked, so `triage`/`to-spec`/`to-tickets` know whether to call `gh`, `glab`, `bd`, write markdown under `.scratch/`, or follow a workflow you describe. GitHub, GitLab, Beads, local markdown, or other. (It proposes Beads when it finds `.beads/`; otherwise it follows your `git remote`.)
- **Triage labels** — asked only if the `triage` skill is installed, and then just: keep the default labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`)? Say no only if your tracker already uses other names, so `triage` applies real ones instead of creating duplicates. Setup then checks which of the agreed strings your tracker actually has and offers to create the missing ones, since `triage-labels.md` is only a mapping and writing it creates nothing.
- **Domain docs** — assumed single-context (one `GLOSSARY.md` + `docs/adr/` at the root), which fits almost every repo; it only raises a multi-context map when it spots monorepo signals.

The configuration output is `issue-tracker.md`, `domain.md`, and optionally `triage-labels.md` under `docs/agents/`, plus an `## Agent skills` block in the repository's existing `CLAUDE.md` or `AGENTS.md`.

On a fresh GitHub repo the approved labels do not exist yet, and that is worth the extra confirmation: `gh issue create --label <missing>` fails outright rather than creating the label, so an uncreated label costs the whole issue later, not just its tag. Setup creates them here — the `wayfinder:*` labels too, when that skill is installed — so the first `/triage` or `/to-tickets` write lands.

## Guardrails and verification

After writing configuration, the setup calls [guardrails](https://aihero.dev/skills-guardrails) and carries its proposal through approval, implementation, and proof. It then calls [verification](https://aihero.dev/skills-verification) against the final launch and check commands. A missing artifact takes the Create route; an existing `docs/agents/verification/` artifact takes Maintain.

Verification owns the repository interview, surface map, driving instructions, evidence, and cleanup. Only after one mapped feature is `VERIFIED` does setup add the `docs/agents/verification/README.md` pointer to the agent-instruction block.

## Common questions

**Do I have to use GitHub?**

No. GitHub, GitLab, [Beads](https://github.com/steveyegge/beads) and local markdown under `.scratch/` all ship as ready-made templates, and anything else works through the "other" path. This is the most-repeated question in the record, in roughly these words: *"hard locked to github"*, *"can I use GitLab / Jira"*, *"what about Azure DevOps"*. The answer every time is that the tracker is a setup answer, not a skill property.

**Do I need to re-run it after updating the skills?**

Upstream's answer, asked directly after v1.1, was yes. The skill's own closing message is softer: it tells you re-running is only needed to switch trackers or start over. Both are defensible and the reason for the gap is real: the seed templates change between versions, so a `docs/agents/issue-tracker.md` written by an older release can go stale against the skills now reading it. If a downstream skill starts doing something the docs describe differently, re-running is the cheap fix. Guardrails and verification are separate: re-run `/guardrails` when the stack or quality strategy changes, and `/verification` in Maintain mode when application surfaces move, without re-running the whole setup.

**It wrote to `CLAUDE.md`, but I'm on Codex.**

Known gap, still open. The file-selection rule is "edit `CLAUDE.md` if it exists, else `AGENTS.md`": it checks which file exists, not which [harness](https://www.aihero.dev/ai-coding-dictionary/harness) is running. A repo with a `CLAUDE.md` left over from Claude Code will get its `## Agent skills` block somewhere Codex never reads. Two workarounds are in circulation: move the block to `AGENTS.md` by hand, or keep `AGENTS.md` canonical and make `CLAUDE.md` a one-line pointer at it. If neither file exists, the skill asks you which to create rather than picking, which has confused people who expected it to just decide.

**It didn't create my triage labels.**

It does here, and that is a deliberate fork change. Upstream, `docs/agents/triage-labels.md` is only a *mapping* — it tells `/triage` which strings in your tracker correspond to the five canonical roles — and writing it creates nothing, which was filed as a bug more than once. The failure mode is worse than a missing label: GitHub rejects `gh issue create --label <missing>` outright rather than creating the label, so an uncreated label loses the whole issue that `/triage` or `/to-tickets` was writing.

So this version checks the agreed strings against the tracker (`gh label list` on GitHub), names the missing ones, asks before writing to your shared tracker, and creates what you approve with `gh label create --force`. Two follow-ons:

- If your tracker already uses the canonical names, the mapping is an identity table and there is nothing to create. That is the intended common case, not a missing step.
- [wayfinder](https://aihero.dev/skills-wayfinder)'s `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling` and `wayfinder:task` labels are created too, when `/wayfinder` is installed. On a tracker with no label concept, such as local markdown, there is nothing to create: the role strings live in each file's `Status:` line.

**Can I configure the other skills' behaviour here ([grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) cadence, question format, tone)?**

No. It settles three things itself — tracker, labels, doc layout — and then hands off to [guardrails](https://aihero.dev/skills-guardrails) for the development baseline and [verification](https://aihero.dev/skills-verification) for the real-surface route, each of which owns its own questions. None of that is a preferences store. There have been direct requests to make it the home for per-user preferences, and the standing answer is that skills stay opinionated: *"Config is death."* Preferences belong in your `CLAUDE.md` as plain instructions, which every skill already reads.

**Can I keep the config in `~/.claude` instead of committing it to every repo?**

Not today. There is an open request for exactly this from someone running the skills across many repos, and no user-level mode exists. Every repo carries its own `docs/agents/`.

**Isn't it strange to have a skill that configures the other skills?**

One long-standing complaint says yes, in these words: *"having a skill to set up the other skill does not feel right to me: that means the LLM is configuring its own skills."* The trade is real and acknowledged: the alternative to a setup step is duplicating tracker instructions into every skill that touches issues. The output is inspectable, editable markdown, which is the mitigation: you can read every file it wrote and change it by hand, and day-to-day tweaks are exactly that, not another run.

## It's working if

- The tracker, domain layout, and applicable triage labels are recorded under `docs/agents/`, and one `## Agent skills` block points to the current configuration.
- Every approved label string exists in the tracker itself, not just in `triage-labels.md`.
- The approved project guardrails run, with any unverified boundary reported.
- `docs/agents/verification/README.md` describes every discovered surface, one mapped feature is `VERIFIED`, and the agent-instruction block points to it.
- Afterwards, issue workflows use the configured tracker while implementation and diagnosis can follow the recorded real-surface verification route.

## Where it fits

`setup-inconvenient-skills` is the **run-once setup** for the engineering set. It configures the repository, delegates the quality baseline to [guardrails](https://aihero.dev/skills-guardrails), and delegates real-surface setup to [verification](https://aihero.dev/skills-verification). Downstream skills such as [triage](https://aihero.dev/skills-triage), [to-spec](https://aihero.dev/skills-to-spec), [to-tickets](https://aihero.dev/skills-to-tickets), [implement](https://aihero.dev/skills-implement), and [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) then consume those artifacts. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
