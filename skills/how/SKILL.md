---
name: how
description: "Trace how existing repository code works today. Use for code walkthroughs, runtime or data flow, and placement questions such as where a change belongs or which module owns a responsibility."
---

# How

Explain the current mechanics of the named code, read-only. For an ambiguous target, state the narrowest useful interpretation and proceed if the repository supports it.

1. **Start at the entry point.** Find where the named behavior begins in the requested source state (the current workspace by default). Read the defining implementation and the callers, registrations, configuration, or tests that establish the active path. For placement, find the closest existing example of the same responsibility.
2. **Trace the handoffs.** Follow the path in execution or data-flow order. Identify where control, data, or responsibility changes hands, and who owns the relevant state or boundary. Work inline by default. If source volume warrants delegation or distinct paths can be traced independently, give each read-only explorer a bounded path and require citations; check the evidence where the paths meet.
3. **Answer from the trace.** Lead with the direct answer, then cite the entry point and key handoffs by file and line or symbol. Name the owning module or layer. For placement, name the best-fit location and cite the existing ownership rule or precedent, including any uncertainty. Stop once the question is answered. If a handoff depends on runtime configuration or source you cannot inspect, say where the trace stops rather than guessing. Keep the answer about how the system works or where the work fits today, not how to redesign it.

