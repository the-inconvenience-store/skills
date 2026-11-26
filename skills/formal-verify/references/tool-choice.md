# Let the question choose the tool

Pick the tool that answers the question at the lowest cost: a model checker, a proof assistant, an SMT-backed verifier, or another tool. Reuse a repository checker when it answers the question.

- Whether events can happen in a bad order usually suits a model checker over a small model of the design. Default to TLA+ with TLC for bounded state and event-order questions, regardless of the implementation language. Use the actual interleaving boundaries; do not model a real race as one atomic step.
- Whether the code itself behaves for every input in a stated domain, as with overflow or a data-structure invariant, calls for a verifier that analyzes the actual implementation. A hand model of the function does not establish that claim. If no suitable verifier runs on the code, say so and test the real code with generated inputs. Report that as test evidence only.
- If the property must hold at every size, or another dimension cannot be bounded, choose a proof method or analysis that covers that dimension and capture evidence that it completed. A finite-domain search alone does not prove a claim over all sizes.

Prefer a tool that the repo's developers can install and run. Tell the user why it fits the question and what it cannot establish.
