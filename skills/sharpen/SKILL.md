---
name: sharpen
description: Rewrite a task prompt to ask for better evidence, without expanding or doing the task.
disable-model-invocation: true
---

# Sharpen

Make the brief **deeper, not bigger**. Keep the user's outcome, constraints, and authorization. Return a prompt they can send rather than running the task.

1. Identify the professional step the current brief misses. Name the primary material to start from, the concrete method or tool that would improve the result, and evidence independent of the agent's own judgment that would show it is right. Include only changes that improve the existing task. Do not add deliverables or invent source paths, capabilities, or permissions.
2. Rewrite the prompt around the original goal, the better starting material and method, and a checkable finish. When an experiment can settle a consequential choice within scope, ask the next agent to run the smallest useful experiment and recommend an option from the result. Leave product and preference choices to the user. Mark any assumption that would change the brief.
3. Give the rewritten prompt in a copyable block and stop. It should make the existing task easier to verify without making it larger.

Adapted from [pstack sharpen](https://github.com/cursor/plugins/blob/b1fbf4b60ac6813b4583ccc356850dafcf492665/pstack/skills/sharpen/SKILL.md). See [LICENSE](LICENSE).
