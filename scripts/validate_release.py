#!/usr/bin/env python3
"""Validate Orange Build manifests and workflow invariants without dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from validate_app_return import validate_app_return
from validate_evidence_ui import validate_evidence_ui
from validate_execution_profiles import validate_execution_profiles
from validate_interview_flow import validate_interview_flow
from validate_plan_fixtures import validate_fixture_contracts
from validate_preflight_fixtures import validate_preflight_fixtures
from validate_self_improvement import validate_self_improvement


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
            "phase-preflight.md",
            "helpful-tools.md",
            "beginner-guardrails.md",
            "phase-build-skill.md",
            "phase-build-automation.md",
            "verification-loop.md",
            "self-improvement-loop.md",
            "ui-language-and-references.md",
            "phase-verify.md",
        ),
    )

    refs = ROOT / "skills" / "orange-start" / "references"
    required_refs = (
        "beginner-guardrails.md",
        "execution-profiles.md",
        "phase-interview.md",
        "phase-plan.md",
        "phase-preflight.md",
        "helpful-tools.md",
        "phase-connect.md",
        "phase-build.md",
        "phase-build-skill.md",
        "phase-build-automation.md",
        "verification-loop.md",
        "self-improvement-loop.md",
        "ui-language-and-references.md",
        "phase-design.md",
        "phase-verify.md",
        "browser-steps.md",
        "troubleshooting.md",
    )
    for filename in required_refs:
        if not (refs / filename).is_file():
            fail(f"missing workflow reference: {filename}")

    connect = refs / "phase-connect.md"
    require_text(
        connect,
        (
            "<github-owner>/<slug>",
            "--public",
            "visibility",
            "사용자에게 확인받고 `--private`",
            "node --version",
            "process.release.lts",
            "--team",
            "rsync -a --ignore-existing",
            "동의받지 않은 시스템·글로벌·프로젝트 설치를 실행하지 않는다",
        ),
    )
    if not re.search(r"gh repo create[^\n]*--public", connect.read_text(encoding="utf-8")):
        fail("phase-connect.md does not create a public GitHub repository by default")

    verification = refs / "verification-loop.md"
    require_text(
        verification,
        (
            "TEST-01",
            "결과물 인벤토리",
            "RED",
            "GREEN",
            "REFACTOR",
            "TESTED",
            "PARTIAL",
            "INFERRED",
            "P0/P1",
            "아직 증명하지 못한 것",
        ),
    )
    self_improvement = refs / "self-improvement-loop.md"
    require_text(
        self_improvement,
        (
            "최신 고성능 모델",
            "AI가 묻지 않고 고칠 것",
            "사람이 결정할 것",
            "DIAGNOSE",
            "web_app",
            "ai_skill",
            "automation",
            "후보 변경 채택 게이트",
            "trajectory digest",
        ),
    )
    ui_language = refs / "ui-language-and-references.md"
    require_text(
        ui_language,
        (
            "Name That UI",
            "canonical UI 이름",
            "variants가 reroll보다 먼저",
            "functional QA와 visual QA 분리",
            "MengTo/Skills",
        ),
    )
    phase_plan = refs / "phase-plan.md"
    require_text(
        phase_plan,
        (
            "검증 시나리오 계약",
            "결과물 인벤토리",
            "TEST 항목이 없는 기존 v2",
            "v1/legacy",
            "공개·비공개 경계",
            "execution_profile",
            "delivery_intent",
        ),
    )
    web = refs / "phase-build.md"
    require_text(
        web,
        (
            "vercel --prod",
            "REQ-*",
            "phase-design.md",
            "TESTED",
            "결과물 인벤토리",
            "RED",
            "self-improvement-loop.md",
            "ui-language-and-references.md",
        ),
    )
    skill_build = refs / "phase-build-skill.md"
    require_text(
        skill_build,
        ("스킬 이름·경로·예상 답을 알려주지 않은", "`첫 작동 결과`를 체크", "TESTED", "RED", "self-improvement-loop.md"),
    )
    automation_build = refs / "phase-build-automation.md"
    require_text(
        automation_build,
        ("DRY_RUN_PASS", "`첫 작동 결과`를 체크", "TESTED", "RED", "self-improvement-loop.md"),
    )
    design = refs / "phase-design.md"
    require_text(design, ("10분", "Do not add or remove screens", "Name That UI", "1~2개 변수"))
    verify = refs / "phase-verify.md"
    require_text(
        verify,
        (
            "SOURCE_PLAN.md",
            "N/M 통과",
            "기본 visibility는 `PUBLIC`",
            "독립 완료 리뷰",
            "아직 증명하지 못한 것",
            "명시적 동의",
            "orange-build-app",
            "사용할 자료·개인정보와 공개·비공개 경계",
            "AI가 발견해 자동으로 고친 것",
        ),
    )
    preflight = refs / "phase-preflight.md"
    require_text(
        preflight,
        ("지금 할 한 동작", "완료 신호", "제가 이어서 할 일", "남은 단계", "변경분 준비 카드"),
    )
    browser_steps = refs / "browser-steps.md"
    require_text(
        browser_steps,
        ("Orange Build App으로 결과 되돌리기", "256KB", "명시적 프라이버시 동의"),
    )
    memory_log = refs / "memory-log.md"
    require_text(memory_log, ("Orange Build App으로 가져갈 때", "256KB", "자신의 말"))
    guardrails = refs / "beginner-guardrails.md"
    require_text(
        guardrails,
        (
            "Stack Overflow 2025",
            "같은 오류가 두 번",
            "USENIX Security 2025",
            "초보자용 오류 보고",
        ),
    )
    helpful_tools = refs / "helpful-tools.md"
    require_text(
        helpful_tools,
        (
            "현재 **이 세션을 실행 중인 호스트 하나만**",
            "browser_runtime_diagnostics",
            "npm view chrome-devtools-mcp",
            "--isolated --no-usage-statistics --no-performance-crux",
            "claude mcp add --scope local chrome-devtools",
            "https://mcp.vercel.com/<team-slug>/<project-slug>",
            "project_ref=<project-ref>&read_only=true&features=<feature-list>",
            "EXISTING_UNSAFE",
            "이번 실행에서 새로 만든 entry만",
        ),
    )
    resume = ROOT / "skills" / "orange-resume" / "SKILL.md"
    require_text(
        resume,
        (
            "phase-preflight.md",
            "helpful-tools.md",
            "phase-connect.md",
            "verification-loop.md",
            "self-improvement-loop.md",
            "ui-language-and-references.md",
            "TESTED",
        ),
    )
    secure = ROOT / "skills" / "orange-secure" / "SKILL.md"
    require_text(secure, ("find supabase -type f -name '*.sql'", "6개 휴리스틱에서 문제를 찾지 못했습니다"))

    try:
        validate_app_return(emit=False)
        validate_evidence_ui(emit=False)
        validate_execution_profiles(emit=False)
        validate_interview_flow(emit=False)
        validate_fixture_contracts(emit=False)
        validate_preflight_fixtures(emit=False)
        validate_self_improvement(emit=False)
    except ValueError as exc:
        fail(f"workflow fixtures failed: {exc}")

    active_paths = [ROOT / "README.md", *MANIFESTS]
    active_paths.extend(sorted((ROOT / "skills").rglob("*.md")))
    active_text = "\n".join(path.read_text(encoding="utf-8") for path in active_paths)
    for pattern, label in (
        (r"gh repo create[^\n]*--private", "private GitHub repository default"),
        (r"(?mi)^\s*(?:[-*]\s*)?`?/model\b", "host-specific model command"),
        (r"AskUserQuestion", "Claude-only question tool"),
        (r"Claude in Chrome", "Claude-only browser dependency"),
        (r"npm run dev \(백그라운드", "mandatory local dev server"),
        (r"(?m)^\s*git add -A(?:\s|$)", "unsafe blanket staging"),
        (r"\bnpx\s+add-mcp\b", "multi-host MCP installer"),
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
