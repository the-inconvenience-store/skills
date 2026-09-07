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

## Where it fits

`prototype` is a reach-for-it-anytime standalone: you drop into it to resolve a design question, then drop back out. Its answer often feeds [to-spec](https://aihero.dev/skills-to-spec), while [engineering-principles](https://aihero.dev/skills-engineering-principles) supplies the selective decision rules behind the experiment and [domain-modeling](https://aihero.dev/skills-domain-modeling) records durable domain decisions. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
