Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=teach
```

```bash
npx skills update teach
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/teach)

## What it does

`teach` turns the current directory into a standing teaching workspace and teaches you one topic across many sessions — devising short, beautiful, interactive lessons tied to *why* you want to learn.

It does **not** teach from the model's own memory. Parametric knowledge is treated as untrusted; before it can teach, it gathers high-trust resources and grounds every claim in a citation. And it is stateful — the workspace remembers what you've learned, so each session picks up where the last left off rather than starting from scratch.

## When to reach for it

You invoke this by typing `/teach` — the agent won't reach for it on its own.

Reach for it when you want to *learn* a topic over time — a language, a framework, yoga, theoretical physics — and want the sessions to accumulate rather than evaporate. It is not for a one-off explanation; if you just need something clarified in the moment, ask directly. Reach for `teach` when the learning is a project.

## Prerequisites

`teach` builds a whole directory in place, so run it somewhere you're happy to keep as a dedicated workspace. Over time it writes:

- `MISSION.md` — the reason you're learning this, which grounds everything else. If it's empty, `teach`'s first job is to question you until it isn't.
- `RESOURCES.md` — the vetted, high-trust sources it teaches from.
- `./lessons/*.html` — the numbered, self-contained lessons (the primary unit of teaching).
- `./reference/*.html` — compressed cheat-sheets, algorithms, glossaries you'll return to.
- `./learning-records/*.md` — what you've learned, ADR-style, used to judge what to teach next.
- `./assets/*` — reusable components (a shared stylesheet first) so the lessons look like one course.
- `NOTES.md` — your teaching preferences.

## Mission, and the zone of proximal development

Every lesson hangs off the **mission**. Without it, knowledge has nothing to attach to and lessons feel abstract — so the mission is the first thing `teach` pins down and keeps updating as you grow. From the mission and your learning records it computes your **zone of proximal development**: the next lesson should challenge you *just enough*, no more.

## Storage strength, not fluency

The word to think with is **storage strength** — long-term retention — as opposed to **fluency**, the in-the-moment recall that feels like mastery but isn't. `teach` deliberately builds the former through desirable difficulty: retrieval practice, spacing, and interleaving. Knowledge is taught first (where difficulty is the enemy), then skills are drilled through a tight feedback loop (where difficulty is the tool).

## Common questions

**Where does it put the files? Mine ended up in `~/.claude/skills`.**
In the directory you ran `/teach` in ([#377](https://github.com/mattpocock/skills/issues/377), fixed). `SKILL.md` now says which paths resolve from your directory (`./lessons/` and the rest) and which from the skill's own folder (only the `*-FORMAT.md` templates), so the course no longer lands in the skill install.

**Do I stay in one session, or start a new one per lesson?**
All three approaches work: staying in the same session, re-invoking `/teach` in a new session, or opening a new session in the same folder. Each lesson is its own invocation. The folder is the continuity, not the conversation. Common practice is to open a fresh session in the workspace and say `/teach next lesson for <topic>`.

**How do I know it isn't teaching me something it made up?**
You don't, on the skill's word alone. You read the primary sources. `teach` is not reliable enough to trust unchecked, and no skill built on an LLM is. The grounding machinery (`RESOURCES.md`, citations in every lesson, one recommended primary source per lesson) exists to make verification cheap, not to remove the need for it. The failure is not hypothetical: one user learning a 2x2 Rubik's cube was given fabricated move sequences that don't solve it. The diagnostic checklist for a case like that is model, harness, effort, and what the source was. Risk is highest in procedural domains with precise notation, and lowest where the output is immediately verifiable, like code you can run.

**The correct quiz answer is always the first option.**
Confirmed by several people, on Sonnet, on Opus and on GLM, and still unfixed. `SKILL.md` now requires every answer to be the same number of words, which kills a different tell (the correct answer used to be the only fully-reasoned one), but says nothing about position. One contributor tested an instruction-level fix for position and reported the correct answer still landing in slot A 33 times out of 33 across nine lessons ([#335](https://github.com/mattpocock/skills/issues/335)), which points at a shuffling quiz component in `assets/` as the real fix rather than better wording. Until that ships, treat answer position as meaningless. Your `assets/` directory is yours to change, so asking for a component that shuffles at render time is a legitimate local fix.

**It assumed I already knew things, and used terms it never defined.**
The commonest substantive complaint. There is no assessment step: `teach` infers your level from the mission and the learning records, and in session one there are no learning records. One user running it inside a wayfinder pipeline put it plainly: "It never did grilling to establish my starting point so it made lots of assumptions of what I already knew." Another reported lessons leaning on undefined jargon, and a lesson tailored to their hardware that covered what the hardware could do while never saying what it couldn't. Two things help: state your prior knowledge and your gaps in the first message, and correct the level out loud when a lesson misses, because the correction becomes a learning record and steers the next one. An explicit knowledge-assessment step is a standing feature request ([#725](https://github.com/mattpocock/skills/issues/725)), not shipped behaviour.

**Does it do spaced repetition, and does it know when to stop teaching?**
No to the first, and not reliably to the second. Spacing and interleaving are principles the lessons are designed against, but nothing schedules a review, and there is no Anki or calendar integration; both are recurring requests. The related gap is exit criteria: as one user put it, `teach` "is good at making the next lesson, but not as good at knowing when to stop and switch to review or real practice." If you want review or drilling instead of new material, ask for it; the skill will not propose the switch on its own.

**Is it only useful for code?**
No, and the non-coding use is the larger part of the record: Korean, Japanese formal register, piano, guitar, board game design, OpenSCAD, film plots, Azure and CCNA certifications, university exams, and children of eight and ten getting printable books on escape rooms and fire salamanders. Nothing in the skill is programming-specific: mission, resources, zone of proximal development and drill work the same way in any domain. Within code, the strongest reported use is not learning a language from scratch but getting oriented in an unfamiliar codebase or a new team's stack.

**Which model should I run it with?**
There is no canonical answer, and the reported differences are large. Higher [reasoning effort](https://www.aihero.dev/ai-coding-dictionary/effort) has been reported to produce noticeably better lessons than the medium setting. One user ran the same skill through Copilot CLI with Codex and got a single 30-line HTML card where Claude Code produced a full lesson. It runs unmodified in Claude Cowork, subject to whether your organisation allows skills to be added there. If the lessons come out thin, change model, [harness](https://www.aihero.dev/ai-coding-dictionary/harness) or effort before rewriting your prompt.

## Where it fits

`teach` is a reach-for-it-anytime standalone — a long-running learning project you drive session by session, not a step in a build chain. It shares no workflow with the other productivity skills; it simply owns its workspace directory and lives there. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
