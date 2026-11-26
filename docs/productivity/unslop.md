Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=unslop
```

```bash
npx skills update unslop
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/unslop)

## What it does

`unslop` edits an existing draft to remove filler, vague claims, and canned phrasing. It changes the **prose**, not the facts, uncertainty, or required format.

## When to reach for it

Type `/unslop`, or the agent reaches for it when you ask to tighten a draft or a writing workflow needs a final copy pass. If the document needs a different structure rather than cleaner sentences, use [technical-writing](https://aihero.dev/skills-technical-writing) for human-facing engineering docs.

## Common questions

**Will it make my claims sound more certain?** No. If a result is unverified or a number is missing, the edited draft keeps that limitation. It does not invent evidence or delete caveats to make a sentence shorter.

**Will it break my template or rewrite code examples?** No. Required headings, commands, quotations, and code stay intact. The surrounding prose gets the edit.

## Where it fits

Use it on its own or as the last copy pass in [technical-writing](https://aihero.dev/skills-technical-writing) and [pr](https://aihero.dev/skills-pr). [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) routes between editing and authoring.
