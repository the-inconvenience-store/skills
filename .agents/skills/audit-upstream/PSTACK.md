# pstack watchlist

pstack is an inspiration source, not a fork to reconcile. [pstack.json](./pstack.json) owns the source, last-reviewed commit, and mapping from tracked upstream paths to local guidance. A path ending in `/` tracks the entire subtree, including newly added files.

Run `./scripts/audit-upstream.py --source pstack`, or omit `--source` to audit both upstreams. The report compares committed upstream snapshots, not local skill text. It lists new unwatched skill directories for triage without pulling unrelated edits into the watched diff. For a trusted local checkout, pass `--pstack-dir <path>`; the checkout must contain the reviewed commit. Its working tree is not used.

Read changed watched files against their local guidance and classify them as adopt, defer, or skip. Check whether a missing path moved before removing the mapping. Read new unwatched skills to decide whether they belong on the watchlist. A snapshot inventory does not rediscover previously reviewed, untracked skills.

Record the decisions in the generated report. Advance `reviewed` in `pstack.json` to `Current` only after all watched changes and new skills are assessed. The checkpoint records review, not adoption; the command never advances it. Update mappings when adopting a new source or when a tracked source or its local destination moves.
