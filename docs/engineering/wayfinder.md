Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wayfinder
```

```bash
npx skills update wayfinder
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wayfinder)

## What it does

`wayfinder` takes an effort too big for one agent session (wrapped in fog, where the way from here to the goal isn't visible yet) and charts it as a **shared map** of **decision tickets** on your issue tracker, then resolves them one at a time until the way is clear. It **plans, it doesn't do**: every ticket resolves a decision (a question to settle, not a slice of a build to execute), and the map is done when nothing is left to decide before someone goes and builds the thing, so it produces decisions, not deliverables.

## When to reach for it

You invoke this by typing `/wayfinder`; the agent won't reach for it on its own.

The trigger is narrow: the effort must exceed one session **and** its route must still be unclear. Greenfield is not a requirement; an existing codebase can contain just as much fog.

| What you have | Reach for |
| --- | --- |
| A feature you can settle in one conversation | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) in a repo, or [grill-me](https://aihero.dev/skills-grill-me) without one |
| A multi-session effort whose route is unclear | `/wayfinder` |
| A clear thread where the decisions are already made | [to-spec](https://aihero.dev/skills-to-spec), without a map |
| A cleared wayfinder map | [to-spec](https://aihero.dev/skills-to-spec), then [to-tickets](https://aihero.dev/skills-to-tickets) for implementation |

## Prerequisites

The map and tickets live on the repo's configured tracker. [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills) records its "Wayfinding operations": map storage, child tickets, blocking, and frontier queries, with templates for GitHub, GitLab, Beads, and local markdown. If no tracker is configured, wayfinder asks for setup and can default to local markdown.

Native blocking makes the frontier visible in the tracker. A tracker with no dependency relationship falls back to text, which needs closer supervision.

## The map, the fog, and the frontier

The **map** is a single `wayfinder:map` issue whose tickets are child issues. It is an **index, not a store**: each decision lives in its ticket, while the map gives only a gist and a link. Sessions load that low-resolution view and zoom into ticket detail when needed.

| Map section | What it holds |
| --- | --- |
| **Destination** | The end of the whole effort, agreed first so every ticket has a scope boundary |
| **Notes** | Standing preferences, domain context, and skills each session should consult |
| **Decisions so far** | One line and a link per resolved ticket |
| **Not yet specified** | The **fog of war**: in-scope questions you cannot yet phrase precisely |
| **Out of scope** | Work beyond the destination; it stays closed rather than graduating into tickets |

Fog becomes a ticket when you can state the question precisely, not when you can answer it. Resolving a ticket can **graduate** newly visible questions into tickets; remove the same fog from *Not yet specified* so it has only one home.

The **frontier** is the open, unblocked, unclaimed tickets. Assignment is the claim: take it before doing any work so concurrent sessions skip it. Human-facing discussion uses ticket **names**, with IDs inside links, rather than a wall of bare issue numbers.

## Four decision-ticket types

Every ticket carries a `wayfinder:<type>` label. **HITL** means a live human exchange; **AFK** means the agent can drive it alone.

| Type | Mode | What it resolves |
| --- | --- | --- |
| `grilling` | HITL | A question settled through [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) |
| `prototype` | HITL | A question about look or behavior that needs a concrete [prototype](https://aihero.dev/skills-prototype) to react to |
| `research` | AFK | An outside fact, investigated by a [research](https://aihero.dev/skills-research) subagent on a `research/<name>` branch, linked from the ticket |
| `task` | Either | Manual work that unblocks a decision, such as provisioning access or moving data so its shape can be inspected |

A HITL ticket is not resolved by the agent answering for you or choosing its favorite prototype. A `task` earns its place by unblocking a decision, not by delivering a slice of the product. Research is the exception to one ticket per session and can run in parallel.

## Common questions

**How is this different from `/grill-with-docs`? Which should I start with?**
Session count, not project size. `/grill-with-docs` is single-session planning; wayfinder is multi-session planning. If you can hold the whole thing in one conversation, grilling is the cheaper and better tool, and wayfinder is genuinely slower and denser for that case. The community shorthand that has settled on it: wayfinder only makes sense if the work doesn't fit into a single session. This is by a distance the most-asked wayfinder question, and it keeps being asked because the descriptions do not tell you where your own task sits on that line. You have to judge the session count yourself.

**When it asks for the "destination", does it mean the end of this session or the end of everything?**
The whole map. That means the destination of the entire map, not just the initial session. The question reads ambiguously because wayfinder is by definition a multi-session tool, so a session-scoped answer never makes sense. Typical destinations are a [spec](https://www.aihero.dev/ai-coding-dictionary/spec) to hand off, a decision to lock before planning starts, a proof of concept, or a change made in place like a data migration.

**The map is cleared. Didn't wayfinder already write the spec and make the tickets? Why do I still need `/to-spec` and `/to-tickets`?**
No. Wayfinder's tickets are decision tickets, and by the time the map closes they are all closed too. What is left is a map full of linked decisions, which is not a build plan. [to-spec](https://aihero.dev/skills-to-spec) collapses those linked decisions into one spec (`/to-spec #<map_issue>`) and [to-tickets](https://aihero.dev/skills-to-tickets) slices that into tracer-bullet implementation tickets. Looping the map straight into [implement](https://aihero.dev/skills-implement) skips the collapse and throws the linked detail away. Go straight to implementation only when the effort turned out genuinely small. People do run the abbreviated pipeline and report it working; the two extra steps buy you an explicit spec artifact that a reviewer or a colleague can read, which matters more the less solo you are.

**My agent started writing production code in the middle of a wayfinder session.**
The most-reported failure with this skill, and there is a real hole behind it. Wayfinder's "plan, don't do" default can be overridden in the map's **Notes**, but the Notes are written by the agent, so the constraint and its exemption live in the same file the constrained party owns. One user watched an agent write "this map carries execution" into its own Notes and then read it back in later sessions as its own licence, building on a live server. There is no hard in-skill stop for "I meant the default." Until there is: read the Notes on any map you didn't chart yourself, keep implementation in its own sessions, and treat any `wayfinder:task` that looks like a slice of the build as mis-typed.

**I charted 27 tickets, and by the time I got to the thirteenth, the rest no longer made sense.**
A real and repeatedly-reported outcome, verbatim from a field report. Wayfinder's default instinct is to plan comprehensively, and a map whose later tickets rest on assumptions the earlier ones invalidate is exactly the waterfall trap the skill is accused of. Two things push back on it. Scope the map to a bounded destination rather than to the whole product. Practitioners consistently report that maps scoped to one defined epic behave better than a sprawling "implement V1", and planning something very big is not the goal in the first place: shipping small increments is. And [prototype](https://www.aihero.dev/ai-coding-dictionary/prototyping) aggressively: the whole reason the route stays current is that uncertainty is flushed out by cheap concrete artifacts before implementation depends on it. Wayfinder is "prototypemaxxing", not "planmaxxing".

**Can I work several tickets in parallel?**
The frontier supports parallel work, but separate sessions do not share live context. Two grilling sessions can ask the same question or make incompatible assumptions, so inspect the dependency graph first. Claim tickets by assignment before work starts, and keep HITL decisions with the human: the local skill explicitly requires that live exchange, including your reaction to a prototype. Research can run in parallel without that steering.

**Do I have to use GitHub Issues?**
No. GitHub, GitLab, [Beads](https://github.com/steveyegge/beads), and local markdown ship as templates from [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills); Linear, Jira, and other trackers use a described workflow. Beads offers native blocking and a `bd ready` frontier without a remote tracker. With no native blocking, dependencies need manual supervision. Local markdown keeps planning artifacts in the repo, which may be useful for private planning but needs deliberate retention rather than accidental permanence.

**The grilling is exhausting. Every question is three paragraphs long.**
This is the sharpest live complaint about wayfinder and it is not resolved. The decomposition one user gave: the verbosity itself causes decision exhaustion, and the length strips out *why* a question is being asked, so you lose the chain from decision to decision as the map gets longer. The verbosity looks like a property of the current set of [models](https://www.aihero.dev/ai-coding-dictionary/model) rather than of the skill, and no fix has landed. Practitioner mitigations in circulation: run a lower [reasoning effort](https://www.aihero.dev/ai-coding-dictionary/effort), and put a plain-language instruction in your global `CLAUDE.md`. Expect to spend real thought here regardless, since the amount of thinking wayfinder demands from you is not a defect but most of what it is for.

**A decision I already closed turned out to be wrong. Do I edit the old ticket or make a new one?**
There is no official guidance, and the agent's instinct is unhelpful: it tends to design around the bad decision rather than challenge it, so you have to steer manually. What does work is telling wayfinder plainly what changed; it updates the map, revises the affected tickets, and comments on already-closed ones. Scope changes mid-map are recoverable. A map you *designed* to change is a scoping smell.

**Where did `decision-mapping` go?**
It is this skill, renamed to `wayfinder` in v1.1 and invoked as `/wayfinder`. "Decision map" was jargon and was also inaccurate, since only one of the four ticket types is really a decision by itself. The reframe gave the skill one coherent vocabulary (destination, fog of war, frontier, the map) instead of an invented term layered on top. The unit kept the "decision" word, though: a **decision ticket** is what a wayfinder ticket is called, precisely to stop people reading it as an implementation ticket.

## It's working if

- Naming the **destination** is the first act, before any ticket exists, because it fixes the scope every ticket is measured against.
- One map is one `wayfinder:map` issue; tickets are its child issues, referred to by **name**, never a bare `#42`.
- A working session claims and resolves **at most one ticket** (research excepted), records a resolution comment, closes the ticket, and appends a one-line pointer to *Decisions so far*.
- If the opening grill surfaces **no fog**, it stops and tells you the journey is small enough to skip the map.
- Graduated fog leaves *Not yet specified*; decision detail stays in its ticket rather than being copied into the map.
- The cleared map hands off toward a spec, not silently into production code.

## Where it fits

`wayfinder` is a big-idea **on-ramp**: an effort too large and foggy to spec in one sitting generates a cleared map of decisions, which then merges onto the main build flow. When the fog is pushed back and the way is clear, hand off to [to-spec](https://aihero.dev/skills-to-spec) to schedule the multi-session build (or, if the effort turned out small, implement directly). It leans on [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) to resolve individual tickets, and on [prototype](https://aihero.dev/skills-prototype) and [research](https://aihero.dev/skills-research) for the ticket types that need them. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
