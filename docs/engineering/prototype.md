Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=prototype
```

```bash
npx skills update prototype
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/prototype)

## What it does

`prototype` builds a small, disposable program whose only job is to answer one design question — does this state model feel right, or what should this UI look like.

The code is **throwaway from day one**. Experience First keeps the experiment aimed at the user's result, Laziness Protocol keeps it cheap, and Exhaust the Design Space applies only when several genuinely different answers to a consequential question are plausible.

## When to reach for it

Type `/prototype`, or the agent reaches for it automatically when a task fits.

Reach for it when you have a design question that's hard to settle on paper — a state machine with cases you can't hold in your head, or a screen you can't picture until you see a few versions side by side. If instead something already built is misbehaving and you need to find out why, use [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs); prototyping explores what to build, not why the built thing is broken.

## Two branches

The question decides the shape, and there are two shapes:

- **"Does this logic / state model feel right?"** — a self-contained HTML demo with free-play controls and guided scenarios. A non-developer can open it directly, press buttons, and watch the full state change.
- **"What should this look like?"** — several radically different UI variations on one route, switchable from a floating bar, so you compare real renders instead of imagining them.

Picking the wrong branch wastes the whole prototype, so the question comes first. Both branches keep state in memory and surface the full state on every step. UI prototypes run from one command; logic demos open as a single HTML file.

## Keep the prototype as a primary source

A finished prototype leaves two things. The **answer** — the verdict plus the question it settled — is what you capture durably (a commit message, an ADR, an issue). The **prototype itself is a primary source** — the runnable evidence the answer came from.

The prototype doesn't belong in the main branch: no tests, no error handling, nothing to maintain. But that's not a reason to destroy it. Once the answer is captured, fold any validated decision into the real code, then capture the prototype on a throwaway branch — out of main, never merged — and leave a context pointer to it on the implementation issue. The main branch stays clean; the raw exploration stays one click away for anyone who wants to re-run it. A prototype left rotting in the main branch has outlived its purpose — a prototype captured as a primary source on a side branch hasn't.

## Common questions

**Wait, isn't the prototype supposed to be deleted?**
Not any more. It used to be: build it, keep the answer, bin the code. The sharpest objection to that was never about speed: it was *who picks up the work next [session](https://www.aihero.dev/ai-coding-dictionary/session), and what do they have to work from?* A prose summary of a prototype loses the thing that made it convincing. So the prototype is now treated as a [primary source](https://www.aihero.dev/ai-coding-dictionary/primary-source): it lands on a `prototype/<name>` branch out of main and the implementation issue points at it. What changed is where the code lives, not the discipline; it still never merges into main.

**It used to build a terminal app. Where did that go?**
The logic branch now emits a single shareable HTML file instead. A terminal app can only be driven by someone with the repo cloned and a runtime installed, which rules out exactly the people whose opinion the prototype needs: the designer, the PM, the domain expert who knows what the state model is supposed to mean. One self-contained file that opens by double-click and survives being emailed can be driven by anyone. The pure logic module underneath is unchanged, and is still the part that lifts into the real code.

**An agent told me to `/prototype` when I should have been implementing.**
Known, and it is a naming problem. `prototype` is a generic, appealing word that reads to a flow-unaware agent as "the obvious next step" once tickets exist, so it gets recommended by name even where the design was fully settled in conversation. If you already know what to build, the next step is `/implement`, per ticket. Reach for a prototype only when a specific design question is genuinely unresolved and talking won't resolve it.

**Should I prototype the whole application before building any of its production features (say, to demo it to prospects)?**
That is a different artifact wearing this skill's name. A prototype here is scoped to one question, and "what is the whole app?" isn't one. A full-app prototype has no natural stopping point, so it becomes the production app by momentum: the cleanup pass never happens, and code written under prototype rules (no tests, no error handling) ends up in front of users. If you need a sales demo, build it deliberately as a demo and be explicit that none of it is production. If you need to settle a design question, cut it down to that question.

**How do I run it in its own session?**
A prototype lives in its own directory and generates a lot of [context](https://www.aihero.dev/ai-coding-dictionary/context) you don't want in the thread that asked the question, so run it somewhere else and bring back only the answer. [handoff](https://aihero.dev/skills-handoff) is the bridge in both directions.

**Isn't this the fastest possible way to burn tokens?**
It can be, if you prototype questions you could have answered by talking, or let one prototype sprawl across a whole feature. The comparison that matters isn't tokens against zero; it's [tokens](https://www.aihero.dev/ai-coding-dictionary/token) against building the wrong state model and finding out after it has production callers. Keep the question narrow and the run short, and the spend stays proportionate.

## Where it fits

`prototype` is a reach-for-it-anytime standalone: you drop into it to resolve a design question, then drop back out. Its answer often feeds [to-spec](https://aihero.dev/skills-to-spec), while [engineering-principles](https://aihero.dev/skills-engineering-principles) supplies the selective decision rules behind the experiment and [domain-modeling](https://aihero.dev/skills-domain-modeling) records durable domain decisions. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
