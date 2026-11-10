# Create project verification

Create a repeatable route for a future agent to launch, inspect, drive, and clean up the real application without rediscovering the repository.

## 1. Interview the repository

Find from code, configuration, and existing documentation:

- The user-facing surfaces.
- The commands that build and launch each surface.
- Readiness signals, ports, profiles, fixtures, seed data, authentication, and required environment.
- Existing drivers such as browser tests, CDP, Playwright, Cypress, PTY helpers, expect scripts, HTTP clients, mobile automation, or public library examples.
- Evidence the surface can expose: screenshots, terminal transcripts, response bodies, exit codes, logs, stored values, or generated files.
- Whether two instances can run concurrently without sharing mutable state.

Prefer an existing harness. Ask the user only for facts the repository and available tools cannot reveal. Do not fix an unrelated broken application as part of creation; report the blocker precisely.

**Done when:** every surface, launch route, driver, evidence source, isolation constraint, and unresolved repository fact is accounted for.

## 2. Define the surfaces

Use the format in [project-format.md](project-format.md). Create one surface directory per independently launched application or public interface. Keep surfaces broad enough that shared launch and cleanup instructions have one owner.

For each surface, identify the exact Doctor check before documenting any Drive recipe. A driver without a health check turns stale processes and wrong builds into false evidence.

**Done when:** every surface has one owner plus a concrete Launch, Doctor, Drive, Evidence, Cleanup, and Isolation plan.

## 3. Write the artifact

Create the root index, each surface README, and the initial feature maps. Seed the three to five highest-value user-facing features per surface when the repository exposes that many. Derive them from commands, routes, menus, public APIs, examples, or existing end-to-end tests.

Use stable handles. Prefer accessible labels, data attributes, prompt text, command flags, public routes, and documented APIs over screen coordinates, tab order, private functions, or database writes.

Any helper script must be executable, live in the repository's established location, and have its invocation documented in the surface README.

**Done when:** the root and surface indexes are complete, every seeded feature has an executable proof, and no placeholder remains.

## 4. Prove the instructions

Before handing the artifact over:

1. Follow one surface's Launch instructions from a clean state.
2. Run Doctor and observe its success signal.
3. Drive one mapped feature through the real public path.
4. Capture the action, result, and any durable side effect.
5. Run Cleanup.
6. Confirm the process and scratch state are gone.
7. Confirm the evidence still exists.

Fix failed instructions and repeat the whole proof. Cleanup after every failed attempt so creation does not strand processes, ports, profiles, or test data.

Creation is complete only when one mapped feature is **VERIFIED** by following the artifact exactly as a future agent would.
