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
- **Domain docs** — assumed single-context (one `CONTEXT.md` + `docs/adr/` at the root), which fits almost every repo; it only raises a multi-context map when it spots monorepo signals.

The configuration output is `issue-tracker.md`, `domain.md`, and optionally `triage-labels.md` under `docs/agents/`, plus an `## Agent skills` block in the repository's existing `CLAUDE.md` or `AGENTS.md`.

On a fresh GitHub repo the approved labels do not exist yet, and that is worth the extra confirmation: `gh issue create --label <missing>` fails outright rather than creating the label, so an uncreated label costs the whole issue later, not just its tag. Setup creates them here — the `wayfinder:*` labels too, when that skill is installed — so the first `/triage` or `/to-tickets` write lands.

## Guardrails and verification

After writing configuration, the setup calls [guardrails](https://aihero.dev/skills-guardrails) and carries its proposal through approval, implementation, and proof. It then calls [verification](https://aihero.dev/skills-verification) against the final launch and check commands. A missing artifact takes the Create route; an existing `docs/agents/verification/` artifact takes Maintain.

Verification owns the repository interview, surface map, driving instructions, evidence, and cleanup. Only after one mapped feature is `VERIFIED` does setup add the `docs/agents/verification/README.md` pointer to the agent-instruction block.

## It's working if

- The tracker, domain layout, and applicable triage labels are recorded under `docs/agents/`, and one `## Agent skills` block points to the current configuration.
- Every approved label string exists in the tracker itself, not just in `triage-labels.md`.
- The approved project guardrails run, with any unverified boundary reported.
- `docs/agents/verification/README.md` describes every discovered surface, one mapped feature is `VERIFIED`, and the agent-instruction block points to it.
- Afterwards, issue workflows use the configured tracker while implementation and diagnosis can follow the recorded real-surface verification route.

## Where it fits

`setup-inconvenient-skills` is the **run-once setup** for the engineering set. It configures the repository, delegates the quality baseline to [guardrails](https://aihero.dev/skills-guardrails), and delegates real-surface setup to [verification](https://aihero.dev/skills-verification). Downstream skills such as [triage](https://aihero.dev/skills-triage), [to-spec](https://aihero.dev/skills-to-spec), [to-tickets](https://aihero.dev/skills-to-tickets), [implement](https://aihero.dev/skills-implement), and [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) then consume those artifacts. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
