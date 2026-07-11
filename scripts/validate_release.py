#!/usr/bin/env python3
"""Validate Orange Build manifests and workflow invariants without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from validate_interview_flow import validate_interview_flow
from validate_plan_fixtures import validate_fixture_contracts


ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = (
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".codex-plugin" / "plugin.json",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing manifest: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_versions() -> str:
    loaded = [(path, load_json(path)) for path in MANIFESTS]
    versions = {data.get("version") for _, data in loaded}
    if None in versions or len(versions) != 1:
        detail = ", ".join(
            f"{path.relative_to(ROOT)}={data.get('version')!r}" for path, data in loaded
        )
        fail(f"manifest versions differ: {detail}")
    version = versions.pop()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"version is not stable semver: {version}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"v{version}" not in readme:
        fail(f"README.md does not mention v{version}")
    for policy_name in ("AGENTS.md", "CLAUDE.md"):
        policy = ROOT / policy_name
        require_text(
            policy,
            (
                ".claude-plugin/plugin.json",
                ".claude-plugin/marketplace.json",
                ".codex-plugin/plugin.json",
                "scripts/validate_release.py",
            ),
        )
    return version


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            fail(f"invalid frontmatter line in {path.relative_to(ROOT)}: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def validate_skills() -> None:
    skills_root = ROOT / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_dirs:
        fail("no skills found")
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            fail(f"missing SKILL.md: {skill_dir.relative_to(ROOT)}")
        meta = parse_frontmatter(skill_file)
        if meta.get("name") != skill_dir.name:
            fail(
                f"skill name mismatch: {skill_dir.name} != {meta.get('name')!r}"
            )
        if not meta.get("description"):
            fail(f"missing skill description: {skill_file.relative_to(ROOT)}")


def require_text(path: Path, snippets: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            fail(f"{path.relative_to(ROOT)} is missing required text: {snippet}")


def validate_workflow() -> None:
    start = ROOT / "skills" / "orange-start" / "SKILL.md"
    require_text(
        start,
        (
            "SOURCE_PLAN.md",
            "phase-interview.md",
            "phase-build-skill.md",
            "phase-build-automation.md",
            "phase-verify.md",
        ),
    )

    refs = ROOT / "skills" / "orange-start" / "references"
    required_refs = (
        "phase-interview.md",
        "phase-plan.md",
        "phase-connect.md",
        "phase-build.md",
        "phase-build-skill.md",
        "phase-build-automation.md",
        "phase-design.md",
        "phase-verify.md",
        "browser-steps.md",
    )
    for filename in required_refs:
        if not (refs / filename).is_file():
            fail(f"missing workflow reference: {filename}")

    connect = refs / "phase-connect.md"
    require_text(
        connect,
        (
            "<github-owner>/<slug>",
            "--private",
            "visibility",
            "node --version",
            "--team",
            "rsync -a --ignore-existing",
        ),
    )
    if re.search(r"gh repo create[^\n]*--public", connect.read_text(encoding="utf-8")):
        fail("phase-connect.md creates a public GitHub repository")

    web = refs / "phase-build.md"
    require_text(web, ("vercel --prod", "REQ-*", "phase-design.md"))
    skill_build = refs / "phase-build-skill.md"
    require_text(skill_build, ("스킬 이름·경로·예상 답을 알려주지 않은", "`첫 작동 결과`를 체크"))
    automation_build = refs / "phase-build-automation.md"
    require_text(automation_build, ("DRY_RUN_PASS", "`첫 작동 결과`를 체크"))
    design = refs / "phase-design.md"
    require_text(design, ("10분", "Do not add or remove screens"))
    verify = refs / "phase-verify.md"
    require_text(verify, ("SOURCE_PLAN.md", "N/M 통과", "PRIVATE"))
    secure = ROOT / "skills" / "orange-secure" / "SKILL.md"
    require_text(secure, ("find supabase -type f -name '*.sql'", "6개 휴리스틱에서 문제를 찾지 못했습니다"))

    try:
        validate_interview_flow(emit=False)
        validate_fixture_contracts(emit=False)
    except ValueError as exc:
        fail(f"copy-contract fixtures failed: {exc}")

    active_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "skills").rglob("*.md"))
    )
    for pattern, label in (
        (r"gh repo create[^\n]*--public", "public GitHub repository default"),
        (r"/model sonnet", "Claude-only model command"),
        (r"AskUserQuestion", "Claude-only question tool"),
        (r"Claude in Chrome", "Claude-only browser dependency"),
        (r"npm run dev \(백그라운드", "mandatory local dev server"),
        (r"(?m)^\s*git add -A(?:\s|$)", "unsafe blanket staging"),
    ):
        if re.search(pattern, active_text):
            fail(f"workflow regressed to {label}")


def main() -> None:
    version = validate_versions()
    validate_skills()
    validate_workflow()
    print(f"OK: orange-build v{version} release invariants pass")


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        fail(str(exc))
