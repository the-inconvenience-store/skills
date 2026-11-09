Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=teach
```

```bash
npx skills update teach
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/teach)

## What it does

`teach` turns the current directory into a standing teaching workspace and teaches you one topic across many sessions, devising short, beautiful, interactive lessons tied to *why* you want to learn.

It does **not** teach from the model's own memory. Parametric knowledge is treated as untrusted; before it can teach, it gathers high-trust resources and grounds every claim in a citation. And it is stateful: the workspace remembers what you've learned, so each session picks up where the last left off rather than starting from scratch.

## When to reach for it

You invoke this by typing `/teach`; the agent won't reach for it on its own.

Reach for it when you want to *learn* a topic over time (a language, a framework, yoga, theoretical physics) and want the sessions to accumulate rather than evaporate. It is not for a one-off explanation; if you just need something clarified in the moment, ask directly. Reach for `teach` when the learning is a project.

| What you want | Reach for |
| --- | --- |
| Lessons and practice that accumulate across sessions | `teach` |
| One explanation in the current conversation | Ask directly |
| The last explanation re-pitched | [wait-what](https://aihero.dev/skills-wait-what) |
| A cited investigation rather than a course | [research](https://aihero.dev/skills-research) |

## Prerequisites

`teach` builds a directory in place. Choose a dedicated workspace for the topic so its course files do not mix with your working project. All output paths resolve from the directory where you invoke it, not the skill's installation.

| Path | What accumulates there |
| --- | --- |
| `MISSION.md` | Why you want to learn. If it is empty or missing, the first task is to establish that reason |
| `RESOURCES.md` | The high-trust sources the lessons draw on |
| `lessons/*.html` | Numbered lessons, each teaching one tightly scoped thing |
| `reference/*.html` | Compressed cheat sheets, algorithms, glossaries and other quick references |
| `learning-records/*.md` | Insights and demonstrated learning used to choose what comes next |
| `assets/*` | Reusable components, starting with a shared stylesheet |
| `NOTES.md` | Your teaching preferences and working notes |

## Mission, and the zone of proximal development

Every lesson hangs off the **mission**. Without it, knowledge has nothing to attach to and lessons feel abstract, so the mission is the first thing `teach` pins down and keeps updating as you grow. From the mission and your learning records it computes your **zone of proximal development**: the next lesson should challenge you *just enough*, no more.

## Storage strength, not fluency

The word to think with is **storage strength** (long-term retention), as opposed to **fluency**, the in-the-moment recall that feels like mastery but isn't. `teach` deliberately builds the former through desirable difficulty: retrieval practice, spacing, and interleaving. Knowledge is taught first (where difficulty is the enemy), then skills are drilled through a tight feedback loop (where difficulty is the tool).

Lessons give you one tangible win and cite a primary source worth reading yourself. References carry the compressed knowledge you will return to later. Shared components in `assets/` keep the lessons consistent without rebuilding the same quiz or stylesheet each time.

**Wisdom** needs real-world practice as well as lessons. For judgement questions, the skill attempts an answer and points you toward a reputable community where you can test it, unless you prefer not to join one.

## Common questions

**Where does it put the files? Mine ended up in `~/.claude/skills`.**
In the directory you ran `/teach` in ([#377](https://github.com/mattpocock/skills/issues/377), fixed). `SKILL.md` now says which paths resolve from your directory (`./lessons/` and the rest) and which from the skill's own folder (only the `*-FORMAT.md` templates), so the course no longer lands in the skill install.

**Do I stay in one session, or start a new one per lesson?**
All three approaches work: staying in the same session, re-invoking `/teach` in a new session, or opening a new session in the same folder. Each lesson is its own invocation. The folder is the continuity, not the conversation. Common practice is to open a fresh session in the workspace and say `/teach next lesson for <topic>`.

**How do I know it isn't teaching me something it made up?**
You don't, on the skill's word alone. You read the primary sources. `teach` is not reliable enough to trust unchecked, and no skill built on an LLM is. The grounding machinery (`RESOURCES.md`, citations in every lesson, one recommended primary source per lesson) exists to make verification cheap, not to remove the need for it. The failure is not hypothetical: one user learning a 2x2 Rubik's cube was given fabricated move sequences that don't solve it. The diagnostic checklist for a case like that is model, harness, effort, and what the source was. Risk is highest in procedural domains with precise notation, and lowest where the output is immediately verifiable, like code you can run.

**The correct quiz answer is always the first option.**
This fork explicitly requires varied correct-answer positions as well as equal-length options. That addresses the instruction gap behind [upstream issue #335](https://github.com/mattpocock/skills/issues/335), but an instruction is not a guarantee that a model follows it. If positions still repeat, ask for a reusable quiz component in `assets/` that shuffles at render time, and judge your answer by its reasoning rather than its position.

**It assumed I already knew things, and used terms it never defined.**
The commonest substantive complaint. There is no assessment step: `teach` infers your level from the mission and the learning records, and in session one there are no learning records. One user running it inside a wayfinder pipeline put it plainly: "It never did grilling to establish my starting point so it made lots of assumptions of what I already knew." Another reported lessons leaning on undefined jargon, and a lesson tailored to their hardware that covered what the hardware could do while never saying what it couldn't. Two things help: state your prior knowledge and your gaps in the first message, and correct the level out loud when a lesson misses, because the correction becomes a learning record and steers the next one. An explicit knowledge-assessment step is a standing feature request ([#725](https://github.com/mattpocock/skills/issues/725)), not shipped behaviour.

**Does it do spaced repetition, and does it know when to stop teaching?**
No to the first, and not reliably to the second. Spacing and interleaving are principles the lessons are designed against, but nothing schedules a review, and there is no Anki or calendar integration; both are recurring requests. The related gap is exit criteria: as one user put it, `teach` "is good at making the next lesson, but not as good at knowing when to stop and switch to review or real practice." If you want review or drilling instead of new material, ask for it; the skill will not propose the switch on its own.

**Is it only useful for code?**
No, and the non-coding use is the larger part of the record: Korean, Japanese formal register, piano, guitar, board game design, OpenSCAD, film plots, Azure and CCNA certifications, university exams, and children of eight and ten getting printable books on escape rooms and fire salamanders. Nothing in the skill is programming-specific: mission, resources, zone of proximal development and drill work the same way in any domain. Within code, the strongest reported use is not learning a language from scratch but getting oriented in an unfamiliar codebase or a new team's stack.

**Which model should I run it with?**
There is no canonical answer, and the reported differences are large. Higher [reasoning effort](https://www.aihero.dev/ai-coding-dictionary/effort) has been reported to produce noticeably better lessons than the medium setting. One user ran the same skill through Copilot CLI with Codex and got a single 30-line HTML card where Claude Code produced a full lesson. It runs unmodified in Claude Cowork, subject to whether your organisation allows skills to be added there. If the lessons come out thin, change model, [harness](https://www.aihero.dev/ai-coding-dictionary/harness) or effort before rewriting your prompt.

## It's working if

- An empty workspace starts with your mission and trusted resources, not an unsupported lesson.
- Each lesson cites sources, teaches one thing, and gives you practice with feedback.
- Lessons reuse the components in `assets/`, while quick-reference material lives in `reference/`.
- A fresh session in the same directory continues from the mission and learning records rather than restarting the course.

## Where it fits

`teach` is a reach-for-it-anytime standalone: a long-running learning project you drive session by session, not a step in a build chain. If a planning conversation exposes a knowledge gap, [handoff](https://aihero.dev/skills-handoff) can carry that question to a teaching workspace while the original conversation stays available. Use [research](https://aihero.dev/skills-research) instead when you need a cited investigation rather than lessons and retention. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
