Quickstart:

```bash
npx skills add the-inconvenience-store/skills
```

Select `bootstrap-skills`, `guardrails`, and `verify`; setup calls the other two.

```bash
npx skills update bootstrap-skills guardrails verify
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/bootstrap-skills)

## What it does

`bootstrap-skills` teaches one repo how the engineering skills should behave in it: where issues live, what the triage labels are called, where domain docs sit, which development guardrails apply, and how future agents prove behavior through the real surface.

It first writes the repository-specific configuration under `docs/agents/`, discovered from the actual repo and confirmed with you rather than guessed. It then calls the owning skills: [guardrails](https://aihero.dev/skills-guardrails) establishes the approved quality baseline, and [verify](https://aihero.dev/skills-verify) creates or maintains the app-driving route. The setup remains prompt-driven rather than a deterministic scaffold.

The configuration varies by repo; the installed skills do not. To use a custom tracker, describe its workflow during setup or edit `docs/agents/issue-tracker.md` later, rather than editing a `SKILL.md` that the next update will replace.

## When to reach for it

You invoke this by typing `/bootstrap-skills`; the agent won't reach for it on its own.

Reach for it **once per repo, before the first use of any other engineering skill**. Re-run the full setup only to switch foundational configuration or start over. Day-to-day changes belong to the owning surface: edit tracker or domain config directly, run [guardrails](https://aihero.dev/skills-guardrails) when the quality strategy changes, and run [verify](https://aihero.dev/skills-verify) with Maintain when application surfaces move.

## Prerequisites

Run it in the repository you want configured, somewhere it is safe to write project guidance. Have [guardrails](https://aihero.dev/skills-guardrails) and [verify](https://aihero.dev/skills-verify) installed too; setup delegates to both.

| Tracker option | Where issues live | Needs |
| --- | --- | --- |
| GitHub | GitHub Issues | `gh` and access to the repository |
| GitLab | GitLab Issues | `glab` and access to the project |
| [Beads](https://github.com/steveyegge/beads) | The repo-local database | `bd` |
| Local markdown | `.scratch/<feature>/` | No remote tracker |
| Other | Wherever your workflow points | A description of how the agent reads and writes work there |

The first four ship as templates. Local markdown is a complete option for a solo or offline repo, not just an error fallback.

## Repository-specific decisions

It leads each with a recommended answer you can accept in a word, and skips whatever it can already infer, so most runs are a couple of quick confirmations:

- **Issue tracker**: proposes Beads when it finds `.beads/`; otherwise it follows your `git remote`. For GitHub or GitLab without a matching remote, it asks for the URL, wires it up, and stops if `gh repo view` / `glab repo view` still cannot see the project.
- **Triage labels**: asked only if the `triage` skill is installed, and then just: keep the default labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`)? Say no only if your tracker already uses other names, so `triage` applies real ones instead of creating duplicates. Setup then checks which of the agreed strings your tracker actually has and offers to create the missing ones, since `triage-labels.md` is only a mapping and writing it creates nothing.
- **Domain docs**: assumed single-context (one `GLOSSARY.md` + `docs/adr/` at the root), which fits almost every repo; it only raises a multi-context map when it spots monorepo signals. If it finds the legacy `CONTEXT.md` / `CONTEXT-MAP.md`, it offers to `git mv` them to their `GLOSSARY` names and rewrite those names in `docs/agents/domain.md`.

The output is inspectable repository guidance, not a global preferences store:

| Artifact | Purpose |
| --- | --- |
| `docs/agents/issue-tracker.md` | Tracker operations, including wayfinding operations |
| `docs/agents/domain.md` | Domain-doc layout and reading rules |
| `docs/agents/triage-labels.md` | Label vocabulary, only when `triage` is installed |
| One `## Agent skills` block in `CLAUDE.md` or `AGENTS.md` | Pointers to the configuration and, after proof, the verification route |

Setup records the domain-doc layout; [domain-modeling](https://aihero.dev/skills-domain-modeling) creates `GLOSSARY.md` and ADRs lazily when terms and decisions resolve. Their absence immediately after setup is normal.

On a fresh GitHub repo the approved labels do not exist yet, and that is worth the extra confirmation: `gh issue create --label <missing>` fails outright rather than creating the label, so an uncreated label costs the whole issue later, not just its tag. Setup creates them here (the `wayfinder:*` labels too, when that skill is installed) so the first `/triage` or `/to-tickets` write lands.

## Guardrails and verify

After writing configuration, the setup calls [guardrails](https://aihero.dev/skills-guardrails) and carries its proposal through approval, implementation, and proof. It then calls [verify](https://aihero.dev/skills-verify) against the final launch and check commands. A missing artifact takes the Create route; an existing `docs/agents/verification/` artifact takes Maintain.

`verify` owns the repository interview, surface map, driving instructions, evidence, and cleanup. Only after one mapped feature is `VERIFIED` does setup add the `docs/agents/verification/README.md` pointer to the agent-instruction block.

## Common questions

**Do I have to use GitHub?**

No. GitHub, GitLab, [Beads](https://github.com/steveyegge/beads) and local markdown under `.scratch/` all ship as ready-made templates, and anything else works through the "other" path. This is the most-repeated question in the record, in roughly these words: *"hard locked to github"*, *"can I use GitLab / Jira"*, *"what about Azure DevOps"*. The answer every time is that the tracker is a setup answer, not a skill property.

**Do I need to re-run it after updating the skills?**

Upstream's answer, asked directly after v1.1, was yes. The skill's own closing message is softer: it tells you re-running is only needed to switch trackers or start over. Both are defensible and the reason for the gap is real: the seed templates change between versions, so a `docs/agents/issue-tracker.md` written by an older release can go stale against the skills now reading it. If a downstream skill starts doing something the docs describe differently, re-running is the cheap fix. Guardrails and verification are separate: re-run `/guardrails` when the stack or quality strategy changes, and `/verify` in Maintain mode when application surfaces move, without re-running the whole setup.

**It wrote to `CLAUDE.md`, but I'm on Codex.**

Known gap, still open. The file-selection rule is "edit `CLAUDE.md` if it exists, else `AGENTS.md`": it checks which file exists, not which [harness](https://www.aihero.dev/ai-coding-dictionary/harness) is running. A repo with a `CLAUDE.md` left over from Claude Code will get its `## Agent skills` block somewhere Codex never reads. Two workarounds are in circulation: move the block to `AGENTS.md` by hand, or keep `AGENTS.md` canonical and make `CLAUDE.md` a one-line pointer at it. If neither file exists, the skill asks you which to create rather than picking, which has confused people who expected it to just decide. For repos shared across harnesses, that question includes two symlinked choices: `AGENTS.md` with `CLAUDE.md` linked to it, or `CLAUDE.md` with `AGENTS.md` linked to it, so both harnesses read the same file.

**It didn't create my triage labels.**

It does here, and that is a deliberate fork change. Upstream, `docs/agents/triage-labels.md` is only a *mapping* (it tells `/triage` which strings in your tracker correspond to the five canonical roles), and writing it creates nothing, which was filed as a bug more than once. The failure mode is worse than a missing label: GitHub rejects `gh issue create --label <missing>` outright rather than creating the label, so an uncreated label loses the whole issue that `/triage` or `/to-tickets` was writing.

So this version checks the agreed strings against the tracker (`gh label list` on GitHub), names the missing ones, asks before writing to your shared tracker, and creates what you approve with `gh label create --force`. Two follow-ons:

- If your tracker already uses the canonical names, the mapping is an identity table and there is nothing to create. That is the intended common case, not a missing step.
- [wayfinder](https://aihero.dev/skills-wayfinder)'s `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling` and `wayfinder:task` labels are created too, when `/wayfinder` is installed. On a tracker with no label concept, such as local markdown, there is nothing to create: the role strings live in each file's `Status:` line.

**Can I configure the other skills' behaviour here ([grilling](https://www.aihero.dev/ai-coding-dictionary/grilling) cadence, question format, tone)?**

No. It settles three things itself (tracker, labels, doc layout) and then hands off to [guardrails](https://aihero.dev/skills-guardrails) for the development baseline and [verify](https://aihero.dev/skills-verify) for the real-surface route, each of which owns its own questions. None of that is a preferences store. There have been direct requests to make it the home for per-user preferences, and the standing answer is that skills stay opinionated: *"Config is death."* Preferences belong in your `CLAUDE.md` as plain instructions, which every skill already reads.

**Can I keep the config in `~/.claude` instead of committing it to every repo?**

Not today. There is an open request for exactly this from someone running the skills across many repos, and no user-level mode exists. Every repo carries its own `docs/agents/`.

**Isn't it strange to have a skill that configures the other skills?**

One long-standing complaint says yes, in these words: *"having a skill to set up the other skill does not feel right to me: that means the LLM is configuring its own skills."* The trade is real and acknowledged: the alternative to a setup step is duplicating tracker instructions into every skill that touches issues. The output is inspectable, editable markdown, which is the mitigation: you can read every file it wrote and change it by hand, and day-to-day tweaks are exactly that, not another run.

## It's working if

- The tracker, domain layout, and applicable triage labels are recorded under `docs/agents/`, and one `## Agent skills` block points to the current configuration.
- Every approved label string exists in the tracker itself, not just in `triage-labels.md`.
- The approved project guardrails run, with any unverified boundary reported.
- `docs/agents/verification/README.md` describes every discovered surface, one mapped feature is `VERIFIED`, and the agent-instruction block points to it.
- No installed `SKILL.md` changed: repository-specific choices live in the repo's own guidance.
- Afterwards, issue workflows use the configured tracker while implementation and diagnosis can follow the recorded real-surface verification route.

## Where it fits

`bootstrap-skills` is the **run-once setup** for the engineering set. It configures the repository, delegates the quality baseline to [guardrails](https://aihero.dev/skills-guardrails), and delegates real-surface setup to [verify](https://aihero.dev/skills-verify). Downstream skills such as [triage](https://aihero.dev/skills-triage), [to-spec](https://aihero.dev/skills-to-spec), [to-tickets](https://aihero.dev/skills-to-tickets), [implement](https://aihero.dev/skills-implement), and [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) then consume those artifacts. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
