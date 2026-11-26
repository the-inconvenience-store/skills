---
name: technical-writing
description: Structure and write human-facing engineering documentation. Use for tutorials, how-to guides, references, design explanations, RFCs, or READMEs.
---

# Technical writing

Start with the reader's job. Follow the repository's templates and conventions. Use `writing-for-agents` instead when the document is instructions for an agent, and `pr` when the deliverable is a PR body. Product UI copy follows its own rules.

## Pick the primary mode

- **Tutorial:** Tell the reader what they will build. Each step produces a result they can recognize.
- **How-to:** Start from a concrete goal. Name prerequisites and put conditions before the actions they govern. Describe the expected result.
- **Reference:** Organize exact facts for lookup. Match the structure and names of the interface. Keep examples separate from the contract.
- **Explanation:** Explain the decision, constraints, alternatives, and consequences. Separate what is known from what is inferred.

Choose a primary mode for the page, or for each section when a repository template combines modes. Link to material that serves a different reader job instead of copying it.

## Write so the reader can act

Name the real command, flag, file, or symbol. Define terms the first time they matter, then use one name per thing. Prefer direct instructions, conditions before steps, and link text that names what opens. Make the actor and the referent of each pronoun clear. Use numbered lists for ordered steps. Match the repository's heading and code conventions.

Check examples and factual claims against the interface or cited source. Mark anything you could not verify instead of implying it ran. Call the Skill tool with `unslop` once after the draft is complete. Keep exact commands, quotations, and required layout intact. The document is done when its intended reader can complete the task or find the answer without guessing.

