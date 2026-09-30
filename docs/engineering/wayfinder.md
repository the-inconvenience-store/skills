Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wayfinder
```

```bash
npx skills update wayfinder
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wayfinder)

## What it does

`wayfinder` takes an effort too big for one agent session — wrapped in fog, where the way from here to the goal isn't visible yet — and charts it as a **shared map** of **decision tickets** on your issue tracker, then resolves them one at a time until the way is clear. It **plans, it doesn't do**: every ticket resolves a decision — a question to settle, not a slice of a build to execute — and the map is done when nothing is left to decide before someone goes and builds the thing — so it produces decisions, not deliverables.

## When to reach for it

You invoke this by typing `/wayfinder` — the agent won't reach for it on its own.

Reach for it when an effort is **more than one agent session can hold** and the route to its **destination** is still foggy — you can feel the shape of the work but can't yet write it down as a spec or a plan. For turning an *already-clear* thread into a spec, use [to-spec](https://aihero.dev/skills-to-spec); for slicing an already-understood plan into buildable tickets, use [to-tickets](https://aihero.dev/skills-to-tickets). Wayfinder sits upstream of both: it's what you run when there's too much fog to spec directly.

## Prerequisites

The map and its tickets live on the repo's issue tracker, so wayfinder needs the tracker wiring that [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) lays down — it seeds a "Wayfinding operations" section describing how the map, child tickets, blocking, and frontier queries are expressed for GitHub, GitLab, or local-markdown. Absent that doc, wayfinder defaults to a local-markdown map.

## The map is an index, fog is the frontier

The **map** is a single `wayfinder:map` issue whose tickets are its child issues — one shared URL the whole team can watch. It's an **index, not a store**: each decision lives in exactly one place (its ticket), and the map only gists and links, never restates. A session loads the map at low resolution and zooms into individual tickets on demand.

Beyond the live tickets lies the **fog of war** — decisions you can tell are coming but can't yet pin down. The test for whether something is a ticket or still fog is whether you can *state the question precisely now*, not whether you can answer it. Resolving a ticket clears the fog ahead of it, **graduating** whatever's now specifiable into fresh tickets. The **frontier** is the open, unblocked, unclaimed tickets — the edge of the known — and it's what the tracker's native blocking renders visually, so you see what's takeable without opening the map. Fog only gathers *toward* the **destination**; work past it is ruled **out of scope**, closed, never graduating.

Every ticket is **HITL** (human in the loop) or **AFK** (agent alone). Research is AFK; prototypes and grilling are HITL. A **task** may be either: it handles manual work that blocks a later decision, such as provisioning access or moving data into a form that can be inspected. Research stays a real ticket — a shared blocker downstream decisions hang on — but because it's AFK, a session doesn't stop and read: it sends a subagent that calls `research` to burn the ticket down in parallel, keeping the frontier fast, and captures the findings on a throwaway `research/<name>` branch.

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
The frontier is built to show you what is takeable, and blocking edges are there so parallel work is safe on paper. In practice one-at-a-time is the safer default. Users working two grilling tickets at once get asked in one session a question they just answered in the other, because the sessions share no [context](https://www.aihero.dev/ai-coding-dictionary/context). There is also a known gap on prototype tickets: an agent has been reported building three UI variations, choosing one itself, and closing the ticket. The selection is yours to make, and the skill does not currently say so loudly enough. If you do run in parallel, review the dependency graph yourself first.

**Do I have to use GitHub Issues?**
No. Any issue tracker works. GitHub is the best-supported path because its native sub-issues and blocking relationships are what make the frontier visible without opening the map; GitLab, [Beads](https://github.com/steveyegge/beads), Linear, Jira and local markdown all get used, and the first four ship as ready-made templates from [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills). Beads is the one to look at if you want native blocking and a `bd ready` frontier query without a remote tracker. Two honest caveats. A tracker with no native blocking means the dependency graph is inferred from text and needs manual correction. And local markdown puts the artifacts in your repo, which is not recommended: storing this material in the repo tends to lead to accidental persistence. Open-source maintainers hit the opposite problem (public trackers filling with agent-generated planning tickets) and tend to choose local markdown anyway.

**The grilling is exhausting. Every question is three paragraphs long.**
This is the sharpest live complaint about wayfinder and it is not resolved. The decomposition one user gave: the verbosity itself causes decision exhaustion, and the length strips out *why* a question is being asked, so you lose the chain from decision to decision as the map gets longer. The verbosity looks like a property of the current set of [models](https://www.aihero.dev/ai-coding-dictionary/model) rather than of the skill, and no fix has landed. Practitioner mitigations in circulation: run a lower [reasoning effort](https://www.aihero.dev/ai-coding-dictionary/effort), and put a plain-language instruction in your global `CLAUDE.md`. Expect to spend real thought here regardless, since the amount of thinking wayfinder demands from you is not a defect but most of what it is for.

**A decision I already closed turned out to be wrong. Do I edit the old ticket or make a new one?**
There is no official guidance, and the agent's instinct is unhelpful: it tends to design around the bad decision rather than challenge it, so you have to steer manually. What does work is telling wayfinder plainly what changed; it updates the map, revises the affected tickets, and comments on already-closed ones. Scope changes mid-map are recoverable. A map you *designed* to change is a scoping smell.

**Where did `decision-mapping` go?**
It is this skill, renamed to `wayfinder` in v1.1 and invoked as `/wayfinder`. "Decision map" was jargon and was also inaccurate, since only one of the four ticket types is really a decision by itself. The reframe gave the skill one coherent vocabulary (destination, fog of war, frontier, the map) instead of an invented term layered on top. The unit kept the "decision" word, though: a **decision ticket** is what a wayfinder ticket is called, precisely to stop people reading it as an implementation ticket.

## It's working if

- Naming the **destination** is the first act — before any ticket exists — because it fixes the scope every ticket is measured against.
- One map is one `wayfinder:map` issue; tickets are its child issues, referred to by **name**, never a bare `#42`.
- A session resolves **at most one ticket** (research tickets excepted), records the answer as a resolution comment, closes the ticket, and appends a one-line pointer to *Decisions so far*.
- If the opening grill surfaces **no fog**, it stops and tells you the journey is small enough to skip the map.

## Where it fits

`wayfinder` is a big-idea **on-ramp**: an effort too large and foggy to spec in one sitting generates a cleared map of decisions, which then merges onto the main build flow. When the fog is pushed back and the way is clear, hand off to [to-spec](https://aihero.dev/skills-to-spec) to schedule the multi-session build (or, if the effort turned out small, implement directly). It leans on [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) to resolve individual tickets, and on [prototype](https://aihero.dev/skills-prototype) and [research](https://aihero.dev/skills-research) for the ticket types that need them. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
