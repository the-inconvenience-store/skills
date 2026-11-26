Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=reframe
```

```bash
npx skills update reframe
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/reframe)

## What it does

`reframe` finds clearer words for what you're trying to build and turns your description into a brief you can reuse. If your description fits more than one problem, it explains what would tell them apart.

It borrows vocabulary from precedents the agent can verify, and only when the vocabulary changes what you would ask for. The revised brief stays in chat; your project files stay unchanged.

## When to reach for it

You invoke this by typing `/reframe`; the agent won't reach for it on its own.

Reach for it when you can describe the situation but suspect you don't yet have the words to ask for the right thing. If you only want to check that the agent heard you, ask it to play your request back without starting work. If you already know what you're weighing and want to settle the choices, use [grill-with-docs](https://aihero.dev/skills-grill-with-docs) instead.

## Load-bearing words

A term is **load-bearing** if using it changes the request. For example, “support retries” could mean recovering interrupted work, or it could mean preventing a second charge when someone resends a payment request. The useful distinction is what the system must do in each case, not which wording sounds more technical.

## Common questions

**Does it change our glossary?**
No. It borrows terms to make this brief clearer. [Domain-modeling](https://aihero.dev/skills-domain-modeling) is for settling and recording the project's shared language.

**What if it can't verify a precedent or tell which problem I mean?**
It leaves unverified precedents out and tells you what it couldn't check. If the distinction still matters, the brief stays conditional rather than turning a guess into a requirement.

## Where it fits

`reframe` is a standalone step you can use before design: it clarifies what you're asking, while [grill-with-docs](https://aihero.dev/skills-grill-with-docs) helps you decide what to do. [Ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) maps the full set.
