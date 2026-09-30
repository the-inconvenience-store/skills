Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=improve-codebase-architecture
```

```bash
npx skills update improve-codebase-architecture
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/improve-codebase-architecture)

## What it does

`improve-codebase-architecture` scans a codebase for **deepening opportunities** — places where a shallow module (an interface nearly as complex as the thing it hides) could become a deep one — presents them as a self-contained visual HTML report, then grills through whichever one you pick.

It does **not** hand you a flat list of refactors. Every candidate has to pass the **deletion test** — would removing this module *concentrate* complexity behind a smaller interface, or just move it around? Only the "concentrates" cases earn a card. That filter is what stops the report from becoming generic cleanup advice.

Unless you point it at a specific area, it also scopes itself to where development is actually landing — reading the recent commits to bias toward the code you're still changing. Deepening a module pays off by making future changes to it easier, so it puts extra weight on the parts of the repo that have recently changed.

## When to reach for it

You invoke this by typing `/improve-codebase-architecture` — the agent won't reach for it on its own.

Reach for it as a periodic health check: every few days, or whenever a codebase has started to feel like it takes too much bouncing between small modules to understand one concept. It reads the existing architecture and proposes where to deepen it. If you already know the module you want to redesign and just need the vocabulary to think it through, use [codebase-design](https://aihero.dev/skills-codebase-design) instead — this skill is the survey that finds the candidates; that one is the design bench.

## Deepening opportunities

The whole skill turns on one idea: **depth**. A deep module hides a lot of functionality behind a small, stable interface; a shallow one leaks its implementation through an interface almost as wide as the code beneath it. The report hunts for shallowness — pure functions extracted only for testability while the real bugs hide in how they're called (no **locality**), modules that leak across their **seams**, concepts you can't understand without opening five files — and proposes the deepening that would fix it.

It speaks in the shared design vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and in your project's own domain language from `GLOSSARY.md`, so a candidate reads as "deepen the Order intake module," never "refactor the FooBarHandler."

## The report, then the grill

The output is a browser-ready HTML file written to your OS temp directory — nothing lands in the repo. Each candidate is a card with the files involved, the friction, a plain-English solution, the benefit in terms of locality and leverage, a before/after diagram, and a `Strong` / `Worth exploring` / `Speculative` badge. It closes with the one it would tackle first.

Then it stops and asks which one you want to explore. Pick one and it runs the [grilling](https://aihero.dev/skills-grilling) loop over that design — constraints, what sits behind the seam, which tests survive — updating the domain model inline as decisions crystallise.

## Common questions

**It grilled me for an hour about one idea instead of showing me options. Can I turn that off?**

Yes: say so when you invoke it ("don't grill me, just show the report"). This is the loudest complaint the skill has. One user put it bluntly: they liked it as "a convenient way to get a thorough analysis of improvements," and after the grilling loop was added found it "borderline unusable," reporting sessions where it proposed a single solution and then asked "10's or 100's of questions." The design intent is that the report comes first and the grill only starts on a candidate you chose, but weaker [models](https://www.aihero.dev/ai-coding-dictionary/model) skip straight to interviewing you about the first idea they had. Reports in that thread vary sharply by model, and it is an open issue: the skill does not yet have a documented no-grill mode.

**The report opened as unstyled raw HTML with no diagrams. What happened?**

The report loads Tailwind and Mermaid from CDNs, so it needs network access when you open it, and it breaks silently when something blocks those scripts. The filed case was a security hook demanding SRI hashes: the agent added them, the CDN served different bytes to the browser than to the `curl` used to compute the hash, and the browser blocked the script. Offline and locked-down environments hit the same wall. The agent cannot see this, because it never renders the page. The workaround is to ask for inline CSS and hand-built SVG diagrams instead of the CDN scaffold. This is an open issue and a real rough edge.

**It gave me twelve candidates. Do I work through them in the same session or start a new one?**

One candidate per session. Working through several in one conversation fills the [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) with the report, the grilling, the domain-model edits and the code changes all at once. The report only lives in a temp file, so carry the candidate itself rather than the file: pick one, grill it, take the decision into `/to-spec`, and turn the rest into [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) you can pick up independently later. Put the chosen improvement into a spec rather than going straight to implementation. This is a recurring question with no documented workflow in the skill itself.

**How should I prompt it?**

With the next thing you are building in mind. Where a big build is coming up, point it at the spec and ask "how can we make this change easy?" An unprompted run scans for hot spots on its own, which is fine for routine upkeep, but naming a direction is what makes the report actionable.

**Does it work on a large legacy codebase?**

Partly. It is strong on big existing codebases lacking consistent structure, and it is the recommended upkeep mechanism after any one-time structural setup. The honest counterweight: users with genuinely out-of-control projects report it "helped a little but still doesn't seem to cut it," and one developer with an eight-year legacy codebase reported the model going in circles where the same skill produces a clean graph on a tidy repo. There is no dedicated `/refactor` skill for that case yet. If the codebase has no shared vocabulary at all, [grill-with-docs](https://aihero.dev/skills-grill-with-docs) to establish one first tends to make this skill's output much better.

**How is this different from `/codebase-design`?**

`/codebase-design` is a reference, not a session driver. It supplies the vocabulary (module, interface, depth, seam, adapter, leverage, locality), and this skill borrows it. Pointing a fresh agent at `/codebase-design` as the thing to "do" is a known failure: with no process of its own to follow, the agent invents one, re-explores code and runs for a very long time before asking you anything. Drive with this skill; consume that one.

**Will it ever tell me the codebase is fine?**

Rarely, and you should know that going in. The skill is built to output findings, so the framing pushes it toward producing candidates rather than concluding that nothing is wrong. The strength badges are the defence: a report where everything is `Speculative` is the skill telling you it found nothing, in the only way it knows how.

**Does it work in Codex or another harness?**

Mostly. The exploration step asks for a sub-agent without naming any [harness](https://www.aihero.dev/ai-coding-dictionary/harness)'s tool, so a harness that has no sub-agent mechanism does the walk inline rather than failing; the skill still runs, the scan is just less parallel. The one genuinely Claude-shaped piece left is the design-it-twice pattern in [codebase-design](https://aihero.dev/skills-codebase-design), which this skill reaches for when you want alternative interfaces explored.

**How do I actually implement deep modules in TypeScript?**

There is no good answer shipped with the skill. The recurring request is for a `TYPESCRIPT.md` giving concrete file and module layouts for the principles, and it does not exist. The skill will tell you where a deepening belongs and what should sit behind the seam; translating that into a package or directory structure is currently on you.

## Where it fits

`improve-codebase-architecture` is **periodic maintenance** — run it every few days, not as a step in a chain. Its neighbours are [codebase-design](https://aihero.dev/skills-codebase-design), which owns the depth-and-seam vocabulary every candidate is written in, [grilling](https://aihero.dev/skills-grilling), which walks the decision tree once you've chosen a candidate, and [domain-modeling](https://aihero.dev/skills-domain-modeling), which keeps `GLOSSARY.md` and the ADRs current as the redesign settles. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
