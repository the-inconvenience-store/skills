# Design experiment

1. Name the decision. If a design tradeoff needs a human choice, call the Skill tool with `grilling`. To record decisions and domain language, recommend `/grill-with-docs`. If seeing behavior would settle the question, call the Skill tool with `prototype` for one isolated, throwaway experiment. If the decision is already settled, use [Feature](feature.md) instead.
2. Compare plausible alternatives against the same scenario. For UI, observe the running interactions and capture the distinguishing states. For logic, observe the output or state transition. The prototype answers a question; it does not become production code by default.
3. Report the recommendation, evidence, and scratch artifact. Leave the production path and issue tracker unchanged unless separately authorized. For a request to match supplied visual references in the existing app, recommend `/parity`; an experiment is not a substitute for its reference-based verification.
