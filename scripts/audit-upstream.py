#!/usr/bin/env python3
"""Reconcile upstream skills and docs with this fork and write a Markdown report."""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import json
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / ".agents/skills/audit-upstream/config.json"
DEFAULT_TEMPLATE = REPO_ROOT / ".agents/skills/audit-upstream/REPORT-TEMPLATE.md"
TEMPLATE_TOKEN = re.compile(r"{{[A-Z_]+}}")


@dataclass(frozen=True)
class IgnoreRule:
    pattern: str
    reason: str


@dataclass
class FileDelta:
    path: str
    status: str
    diff: str | None
    note: str | None = None


@dataclass
class Comparison:
    upstream: str
    local: str
    status: str
    deltas: list[FileDelta] = field(default_factory=list)
    reason: str | None = None


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def git_value(repo: Path, *arguments: str, fallback: str = "unknown") -> str:
    try:
        return run(["git", "-C", str(repo), *arguments]) or fallback
    except (subprocess.CalledProcessError, FileNotFoundError):
        return fallback


def clean_relative_path(value: str, field_name: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{field_name} must be a repository-relative path: {value}")
    return path.as_posix().rstrip("/")


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        config = json.load(handle)

    for field_name in ("report_directory", "docs_root"):
        config[field_name] = clean_relative_path(config[field_name], field_name)

    for root in config["skill_roots"]:
        root["upstream"] = clean_relative_path(root["upstream"], "skill_roots.upstream")
        root["local"] = clean_relative_path(root["local"], "skill_roots.local")
    config["local_skill_roots"] = [
        clean_relative_path(value, "local_skill_roots")
        for value in config["local_skill_roots"]
    ]
    for collection in ("skill_mappings", "docs_mappings"):
        for mapping in config[collection]:
            mapping["upstream"] = clean_relative_path(
                mapping["upstream"], f"{collection}.upstream"
            )
            mapping["local"] = clean_relative_path(
                mapping["local"], f"{collection}.local"
            )
    return config


def rules_from(config: dict[str, Any], key: str) -> list[IgnoreRule]:
    return [IgnoreRule(item["path"], item["reason"]) for item in config[key]]


def matching_rule(path: str, rules: Iterable[IgnoreRule]) -> IgnoreRule | None:
    return next(
        (rule for rule in rules if fnmatch.fnmatchcase(path, rule.pattern)), None
    )


def find_files(directory: Path | None) -> dict[str, Path]:
    if directory is None or not directory.is_dir():
        return {}
    return {
        path.relative_to(directory).as_posix(): path
        for path in directory.rglob("*")
        if path.is_file()
    }


def text_diff(
    local_path: Path | None,
    upstream_path: Path | None,
    local_label: str,
    upstream_label: str,
) -> tuple[str | None, str | None]:
    local_bytes = local_path.read_bytes() if local_path else b""
    upstream_bytes = upstream_path.read_bytes() if upstream_path else b""
    if b"\0" in local_bytes or b"\0" in upstream_bytes:
        return None, "Binary file; content diff omitted."
    try:
        local_text = local_bytes.decode("utf-8")
        upstream_text = upstream_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None, "Non-UTF-8 file; content diff omitted."

    diff = "".join(
        difflib.unified_diff(
            local_text.splitlines(keepends=True),
            upstream_text.splitlines(keepends=True),
            fromfile=f"local/{local_label}",
            tofile=f"upstream/{upstream_label}",
        )
    )
    # Keep the generated Markdown clean even when a source diff contains
    # whitespace-only lines. The diff still records the changed line marker,
    # but does not introduce trailing whitespace into the audit report itself.
    diff = "".join(
        f"{line[:-1].rstrip(' \t')}\n" if line.endswith("\n") else line.rstrip(" \t")
        for line in diff.splitlines(keepends=True)
    )
    return diff or None, None


def executable(path: Path) -> bool:
    return bool(path.stat().st_mode & 0o111)


def compare_directories(
    upstream_dir: Path | None,
    local_dir: Path | None,
    upstream_label: str,
    local_label: str,
) -> list[FileDelta]:
    upstream_files = find_files(upstream_dir)
    local_files = find_files(local_dir)
    deltas: list[FileDelta] = []

    for relative in sorted(upstream_files.keys() | local_files.keys()):
        upstream_path = upstream_files.get(relative)
        local_path = local_files.get(relative)
        if local_path is None:
            status = "added upstream"
        elif upstream_path is None:
            status = "absent upstream"
        else:
            content_changed = local_path.read_bytes() != upstream_path.read_bytes()
            mode_changed = executable(local_path) != executable(upstream_path)
            if not content_changed and not mode_changed:
                continue
            status = "modified"
            if mode_changed:
                local_mode = "executable" if executable(local_path) else "not executable"
                upstream_mode = (
                    "executable" if executable(upstream_path) else "not executable"
                )
                status += f"; mode {local_mode} → {upstream_mode}"

        diff, note = text_diff(
            local_path,
            upstream_path,
            f"{local_label}/{relative}",
            f"{upstream_label}/{relative}",
        )
        deltas.append(FileDelta(relative, status, diff, note))
    return deltas


def compare_files(
    upstream_path: Path | None,
    local_path: Path | None,
    upstream_label: str,
    local_label: str,
) -> list[FileDelta]:
    if local_path is None:
        status = "added upstream"
    elif upstream_path is None:
        status = "absent upstream"
    else:
        content_changed = local_path.read_bytes() != upstream_path.read_bytes()
        mode_changed = executable(local_path) != executable(upstream_path)
        if not content_changed and not mode_changed:
            return []
        status = "modified"
        if mode_changed:
            local_mode = "executable" if executable(local_path) else "not executable"
            upstream_mode = "executable" if executable(upstream_path) else "not executable"
            status += f"; mode {local_mode} → {upstream_mode}"

    diff, note = text_diff(local_path, upstream_path, local_label, upstream_label)
    display_path = PurePosixPath(upstream_label if upstream_path else local_label).name
    return [FileDelta(display_path, status, diff, note)]


def discover_upstream_skills(
    upstream_root: Path, roots: list[dict[str, str]]
) -> list[tuple[str, Path, str]]:
    discovered: list[tuple[str, Path, str]] = []
    seen: set[str] = set()
    for root in roots:
        source = upstream_root / root["upstream"]
        if not source.is_dir():
            continue
        for skill_file in sorted(source.rglob("SKILL.md")):
            skill_dir = skill_file.parent
            relative = skill_dir.relative_to(upstream_root).as_posix()
            if relative in seen:
                raise ValueError(f"Upstream skill discovered twice: {relative}")
            seen.add(relative)
            discovered.append((relative, skill_dir, root["local"]))
    return discovered


def discover_local_skills(local_root: Path, roots: list[str]) -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    for root in roots:
        directory = local_root / root
        if not directory.is_dir():
            continue
        for skill_file in sorted(directory.glob("*/SKILL.md")):
            skill_dir = skill_file.parent
            relative = skill_dir.relative_to(local_root).as_posix()
            discovered[relative] = skill_dir
    return discovered


def reconcile_skills(
    upstream_root: Path, local_root: Path, config: dict[str, Any]
) -> tuple[list[Comparison], list[Comparison], list[IgnoreRule]]:
    mappings = {
        item["upstream"]: (item["local"], item.get("reason"))
        for item in config["skill_mappings"]
    }
    ignored_rules = rules_from(config, "ignored_upstream_skills")
    ignored_local_rules = rules_from(config, "ignored_local_skills")
    matched_ignore_patterns: set[str] = set()
    comparisons: list[Comparison] = []
    ignored: list[Comparison] = []
    matched_local: dict[str, str] = {}

    for upstream_path, upstream_dir, default_local_root in discover_upstream_skills(
        upstream_root, config["skill_roots"]
    ):
        ignore = matching_rule(upstream_path, ignored_rules)
        if ignore:
            matched_ignore_patterns.add(ignore.pattern)
            ignored.append(
                Comparison(upstream_path, "—", "ignored", reason=ignore.reason)
            )
            continue

        mapped = mappings.get(upstream_path)
        if mapped:
            local_path, reason = mapped
        else:
            local_path = f"{default_local_root}/{PurePosixPath(upstream_path).name}"
            reason = None
        if local_path in matched_local:
            raise ValueError(
                f"Local skill {local_path} maps from both "
                f"{matched_local[local_path]} and {upstream_path}"
            )
        matched_local[local_path] = upstream_path

        local_dir = local_root / local_path
        exists = (local_dir / "SKILL.md").is_file()
        deltas = compare_directories(
            upstream_dir,
            local_dir if exists else None,
            upstream_path,
            local_path,
        )
        status = "changed" if exists and deltas else "unchanged" if exists else "new"
        comparisons.append(
            Comparison(upstream_path, local_path, status, deltas, reason)
        )

    for local_path, local_dir in discover_local_skills(
        local_root, config["local_skill_roots"]
    ).items():
        if local_path in matched_local:
            continue
        ignore = matching_rule(local_path, ignored_local_rules)
        if ignore:
            ignored.append(
                Comparison("—", local_path, "ignored", reason=ignore.reason)
            )
            continue
        deltas = compare_directories(None, local_dir, "(absent)", local_path)
        comparisons.append(
            Comparison("—", local_path, "absent", deltas)
        )

    stale = [
        rule for rule in ignored_rules if rule.pattern not in matched_ignore_patterns
    ]
    return comparisons, ignored, stale


def discover_docs(root: Path, docs_root: str) -> dict[str, Path]:
    directory = root / docs_root
    if not directory.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path
        for path in directory.rglob("*")
        if path.is_file()
    }


def reconcile_docs(
    upstream_root: Path, local_root: Path, config: dict[str, Any]
) -> tuple[list[Comparison], list[Comparison], list[IgnoreRule]]:
    upstream_docs = discover_docs(upstream_root, config["docs_root"])
    local_docs = discover_docs(local_root, config["docs_root"])
    mappings = {
        item["upstream"]: (item["local"], item.get("reason"))
        for item in config["docs_mappings"]
    }
    ignored_upstream_rules = rules_from(config, "ignored_upstream_docs")
    ignored_local_rules = rules_from(config, "ignored_local_docs")
    matched_ignore_patterns: set[str] = set()
    comparisons: list[Comparison] = []
    ignored: list[Comparison] = []
    matched_local: dict[str, str] = {}

    for upstream_path, upstream_file in sorted(upstream_docs.items()):
        ignore = matching_rule(upstream_path, ignored_upstream_rules)
        if ignore:
            matched_ignore_patterns.add(ignore.pattern)
            ignored.append(
                Comparison(upstream_path, "—", "ignored", reason=ignore.reason)
            )
            continue
        local_path, reason = mappings.get(upstream_path, (upstream_path, None))
        if local_path in matched_local:
            raise ValueError(
                f"Local docs page {local_path} maps from both "
                f"{matched_local[local_path]} and {upstream_path}"
            )
        matched_local[local_path] = upstream_path
        local_file = local_docs.get(local_path)
        deltas = compare_files(
            upstream_file,
            local_file,
            upstream_path,
            local_path,
        )
        status = "changed" if local_file and deltas else "unchanged" if local_file else "new"
        comparisons.append(
            Comparison(upstream_path, local_path, status, deltas, reason)
        )

    for local_path, local_file in sorted(local_docs.items()):
        if local_path in matched_local:
            continue
        ignore = matching_rule(local_path, ignored_local_rules)
        if ignore:
            continue
        deltas = compare_files(None, local_file, "(absent)", local_path)
        comparisons.append(Comparison("—", local_path, "absent", deltas))

    stale = [
        rule
        for rule in ignored_upstream_rules
        if rule.pattern not in matched_ignore_patterns
    ]
    return comparisons, ignored, stale


def markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def comparison_table(items: list[Comparison], include_delta: bool = False) -> str:
    if not items:
        return "_None._"
    headings = ["Upstream", "Local"]
    if include_delta:
        headings.append("File delta")
    rows = ["| " + " | ".join(headings) + " |", "| " + " | ".join("---" for _ in headings) + " |"]
    for item in sorted(items, key=lambda value: (value.upstream, value.local)):
        cells = [f"`{item.upstream}`", f"`{item.local}`"]
        if include_delta:
            cells.append(delta_summary(item.deltas))
        rows.append("| " + " | ".join(markdown_cell(cell) for cell in cells) + " |")
    return "\n".join(rows)


def ignored_table(items: list[Comparison]) -> str:
    if not items:
        return "_None._"
    rows = ["| Upstream | Local | Reason |", "| --- | --- | --- |"]
    for item in sorted(items, key=lambda value: (value.upstream, value.local)):
        rows.append(
            "| "
            + " | ".join(
                markdown_cell(value)
                for value in (
                    f"`{item.upstream}`",
                    f"`{item.local}`",
                    item.reason or "—",
                )
            )
            + " |"
        )
    return "\n".join(rows)


def stale_rules_table(rules: list[IgnoreRule]) -> str:
    if not rules:
        return "_None._"
    rows = ["| Pattern | Reason |", "| --- | --- |"]
    rows.extend(
        f"| `{markdown_cell(rule.pattern)}` | {markdown_cell(rule.reason)} |"
        for rule in rules
    )
    return "\n".join(rows)


def delta_summary(deltas: list[FileDelta]) -> str:
    counts: dict[str, int] = {}
    for delta in deltas:
        base = delta.status.split(";", 1)[0]
        counts[base] = counts.get(base, 0) + 1
    return ", ".join(f"{count} {status}" for status, count in sorted(counts.items()))


def render_detailed_diffs(items: list[Comparison]) -> str:
    with_deltas = [item for item in items if item.deltas]
    if not with_deltas:
        return "_None._"
    sections: list[str] = []
    for item in sorted(with_deltas, key=lambda value: (value.upstream, value.local)):
        sections.append(f"### `{item.upstream}` → `{item.local}`")
        if item.reason:
            sections.append(f"Mapping note: {item.reason}.")
        for delta in item.deltas:
            sections.append(
                f"<details>\n<summary><code>{delta.path}</code> — "
                f"{delta.status}</summary>\n"
            )
            if delta.diff:
                sections.append(f"~~~~diff\n{delta.diff.rstrip()}\n~~~~")
            else:
                sections.append(f"_{delta.note or 'Mode-only change; no content diff.'}_")
            sections.append("</details>")
    return "\n\n".join(sections)


def render_mappings(config: dict[str, Any]) -> str:
    mappings = [
        ("Skill", item["upstream"], item["local"], item.get("reason", "—"))
        for item in config["skill_mappings"]
    ] + [
        ("Docs", item["upstream"], item["local"], item.get("reason", "—"))
        for item in config["docs_mappings"]
    ]
    if not mappings:
        return "_None._"
    rows = ["| Kind | Upstream | Local | Reason |", "| --- | --- | --- | --- |"]
    rows.extend(
        "| "
        + " | ".join(
            markdown_cell(value)
            for value in (kind, f"`{upstream}`", f"`{local}`", reason)
        )
        + " |"
        for kind, upstream, local, reason in mappings
    )
    return "\n".join(rows)


def by_status(items: list[Comparison], status: str) -> list[Comparison]:
    return [item for item in items if item.status == status]


def summary_table(
    skills: list[Comparison],
    ignored_skills: list[Comparison],
    docs: list[Comparison],
    ignored_docs: list[Comparison],
) -> str:
    rows = [
        "| Area | New upstream | Changed | Absent upstream | Unchanged | Ignored |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label, items, ignored in (
        ("Skills", skills, ignored_skills),
        ("Docs", docs, ignored_docs),
    ):
        rows.append(
            f"| {label} | {len(by_status(items, 'new'))} | "
            f"{len(by_status(items, 'changed'))} | {len(by_status(items, 'absent'))} | "
            f"{len(by_status(items, 'unchanged'))} | {len(ignored)} |"
        )
    return "\n".join(rows)


def automated_assessment(skills: list[Comparison], docs: list[Comparison]) -> str:
    changed_skills = len(by_status(skills, "changed"))
    new_skills = len(by_status(skills, "new"))
    absent_skills = len(by_status(skills, "absent"))
    changed_docs = len(by_status(docs, "changed"))
    new_docs = len(by_status(docs, "new"))
    absent_docs = len(by_status(docs, "absent"))
    return (
        f"The automated reconciliation found {new_skills} new upstream skill(s), "
        f"{changed_skills} changed mapped skill(s), and {absent_skills} local skill(s) "
        f"absent upstream. Documentation has {new_docs} new, {changed_docs} changed, "
        f"and {absent_docs} absent-upstream page(s). Review the detailed diffs before "
        "adopting changes; this inventory makes no merge decision."
    )


def render_report(
    template: str,
    config: dict[str, Any],
    upstream_root: Path,
    upstream_source: str,
    skills: list[Comparison],
    ignored_skills: list[Comparison],
    stale_skill_ignores: list[IgnoreRule],
    docs: list[Comparison],
    ignored_docs: list[Comparison],
    stale_doc_ignores: list[IgnoreRule],
) -> tuple[str, str]:
    upstream_commit = git_value(upstream_root, "rev-parse", "HEAD")
    local_commit = git_value(REPO_ROOT, "rev-parse", "HEAD")
    local_dirty = git_value(REPO_ROOT, "status", "--porcelain", fallback="")
    audit_date = datetime.now().astimezone().date().isoformat()
    replacements = {
        "{{AUDIT_DATE}}": audit_date,
        "{{UPSTREAM_COMMIT}}": upstream_commit,
        "{{UPSTREAM_SOURCE}}": upstream_source,
        "{{LOCAL_COMMIT}}": local_commit,
        "{{LOCAL_DIRTY}}": " (dirty working tree)" if local_dirty else "",
        "{{LOCAL_ROOT}}": str(REPO_ROOT),
        "{{ASSESSMENT}}": automated_assessment(skills, docs),
        "{{SUMMARY}}": summary_table(skills, ignored_skills, docs, ignored_docs),
        "{{NEW_SKILLS}}": comparison_table(by_status(skills, "new"), True),
        "{{CHANGED_SKILLS}}": comparison_table(by_status(skills, "changed"), True),
        "{{ABSENT_UPSTREAM_SKILLS}}": comparison_table(by_status(skills, "absent"), True),
        "{{UNCHANGED_SKILLS}}": comparison_table(by_status(skills, "unchanged")),
        "{{IGNORED_SKILLS}}": ignored_table(ignored_skills),
        "{{STALE_SKILL_IGNORES}}": stale_rules_table(stale_skill_ignores),
        "{{NEW_DOCS}}": comparison_table(by_status(docs, "new"), True),
        "{{CHANGED_DOCS}}": comparison_table(by_status(docs, "changed"), True),
        "{{ABSENT_UPSTREAM_DOCS}}": comparison_table(by_status(docs, "absent"), True),
        "{{UNCHANGED_DOCS}}": comparison_table(by_status(docs, "unchanged")),
        "{{IGNORED_DOCS}}": ignored_table(ignored_docs),
        "{{STALE_DOC_IGNORES}}": stale_rules_table(stale_doc_ignores),
        "{{SKILL_DIFFS}}": render_detailed_diffs(skills),
        "{{DOC_DIFFS}}": render_detailed_diffs(docs),
        "{{MAPPINGS}}": render_mappings(config),
    }
    report = template
    for token, value in replacements.items():
        report = report.replace(token, value)
    unresolved = TEMPLATE_TOKEN.findall(report)
    if unresolved:
        raise ValueError(f"Unresolved report template tokens: {', '.join(unresolved)}")
    return report.rstrip() + "\n", upstream_commit


def upstream_checkout(config: dict[str, Any], supplied: Path | None):
    if supplied:
        root = supplied.resolve()
        if not root.is_dir():
            raise ValueError(f"Upstream checkout does not exist: {root}")
        return None, root, f"local checkout `{root}`"

    temporary = tempfile.TemporaryDirectory(prefix="audit-upstream-")
    root = Path(temporary.name) / "upstream"
    run(
        [
            "git",
            "clone",
            "--quiet",
            "--depth",
            "1",
            "--single-branch",
            "--branch",
            config["upstream_ref"],
            config["upstream_url"],
            str(root),
        ]
    )
    return temporary, root, config["upstream_url"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Audit configuration (default: %(default)s)",
    )
    parser.add_argument(
        "--upstream-dir",
        type=Path,
        help="Use an existing upstream checkout instead of cloning",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config.resolve())
    temporary, upstream_root, upstream_source = upstream_checkout(
        config, args.upstream_dir
    )
    try:
        skills, ignored_skills, stale_skill_ignores = reconcile_skills(
            upstream_root, REPO_ROOT, config
        )
        docs, ignored_docs, stale_doc_ignores = reconcile_docs(
            upstream_root, REPO_ROOT, config
        )
        report, upstream_commit = render_report(
            DEFAULT_TEMPLATE.read_text(encoding="utf-8"),
            config,
            upstream_root,
            upstream_source,
            skills,
            ignored_skills,
            stale_skill_ignores,
            docs,
            ignored_docs,
            stale_doc_ignores,
        )
        date = datetime.now().astimezone().date().isoformat()
        output = REPO_ROOT / config["report_directory"] / f"{date}-{upstream_commit[:7]}.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
        print(output.relative_to(REPO_ROOT).as_posix())
        return 0
    finally:
        if temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
