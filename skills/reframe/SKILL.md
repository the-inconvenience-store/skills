---
name: reframe
description: Find the words that clarify what you are building, then rewrite your brief.
disable-model-invocation: true
---

Turn the user's description into a sharper **brief** in chat. Stay read-only: leave the code, glossary, and other project records unchanged. Stop at the revised brief, not a design decision or implementation.

1. Start with the user's own description and the files or code it refers to. Identify the goal and constraints before interpreting the proposed solution. If the ask could describe materially different problems, name each plausible interpretation and give an observable sign that would distinguish it. Say which the evidence favors and why, or keep the brief conditional if the evidence does not settle it. Skip alternatives that would not change the brief.
2. Teach only **load-bearing terms**: words that change what the user would ask for, build, or check. Explain each in the reader's language, connect it to a detail in their ask, and show what the term lets them specify. Look for real precedents, including in other fields when the mechanics transfer. Open every cited source and confirm it supports the specific usage or behavior you describe. Link to the supporting documentation, paper, or source. Say what carries over and where it stops; omit unverifiable precedents and disclose material gaps in source access.
3. End with a revised brief the user could reuse. Preserve their goal and constraints, use the terms that earned their place, and separate requirements from assumptions. Surface missing information only if it would change the framing or how success is judged. Leave genuinely open choices open.

