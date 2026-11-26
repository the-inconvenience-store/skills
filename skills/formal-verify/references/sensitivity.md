# Show that the check can fail

Use an isolated scratch copy of the target at the checked revision. Keep the command, property, and configuration the same so the deliberate break is the difference.

- **Detached model:** inject the corresponding faulty transition in the model, such as skipping a guard or splitting an indivisible step to admit the bad order. Observe the named property fail and label it **model sensitivity**. A source-only mutation cannot change a detached model's result. Where feasible, independently replay the same schedule on the real implementation and record that evidence separately.
- **Code verifier:** mutate the actual implementation the verifier analyzes, such as removing a guard or reordering two steps. Observe the named property fail in the real-code verifier, not in a substitute model or test.

A parse error, timeout, or failure of a different property does not count. If the baseline already finds a violation, show a distinct witness attributable to the injected break; repeating the baseline finding does not establish sensitivity to the break. If the control cannot distinguish them, report the gap.

Discard the mutation, rerun the baseline, and preserve both results. Confirm that the success path and any property antecedent are reachable on the baseline: a negative control does not by itself rule out a vacuous pass on the original model or code.
