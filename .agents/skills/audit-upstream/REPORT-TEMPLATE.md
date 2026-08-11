# Upstream audit — {{AUDIT_DATE}}

## Provenance

| Side | Revision | Source |
| --- | --- | --- |
| Upstream | `{{UPSTREAM_COMMIT}}` | {{UPSTREAM_SOURCE}} |
| Local | `{{LOCAL_COMMIT}}`{{LOCAL_DIRTY}} | `{{LOCAL_ROOT}}` |

This is a snapshot reconciliation, not a history reconstruction. “New upstream” means absent from the mapped local path; “absent upstream” can mean an upstream deletion or fork-only content. File diffs run from local to upstream after applying configured path mappings.

## Assessment

{{ASSESSMENT}}

## Summary

{{SUMMARY}}

## Skills

### New upstream

{{NEW_SKILLS}}

### Changed

{{CHANGED_SKILLS}}

### Absent upstream

{{ABSENT_UPSTREAM_SKILLS}}

### Unchanged

{{UNCHANGED_SKILLS}}

### Ignored upstream

{{IGNORED_SKILLS}}

### Stale skill ignore rules

{{STALE_SKILL_IGNORES}}

## Documentation

### New upstream

{{NEW_DOCS}}

### Changed

{{CHANGED_DOCS}}

### Absent upstream

{{ABSENT_UPSTREAM_DOCS}}

### Unchanged

{{UNCHANGED_DOCS}}

### Ignored upstream

{{IGNORED_DOCS}}

### Stale docs ignore rules

{{STALE_DOC_IGNORES}}

## Detailed skill diffs

{{SKILL_DIFFS}}

## Detailed documentation diffs

{{DOC_DIFFS}}

## Active mappings

{{MAPPINGS}}

## Configuration

Generated with `./scripts/audit-upstream.py` using [`.agents/skills/audit-upstream/config.json`](../../.agents/skills/audit-upstream/config.json).
