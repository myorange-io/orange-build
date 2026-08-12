#!/usr/bin/env python3
"""Validate Orange Build manifests and shared IA workflow invariants."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from validate_app_return import validate_app_return
from validate_codex_gpt56 import validate_codex_gpt56
from validate_design_routing import validate_design_routing
from validate_evidence_ui import validate_evidence_ui
from validate_execution_profiles import validate_execution_profiles
from validate_ia_workflow import validate_ia_workflow
from validate_interview_flow import validate_interview_flow
from validate_memory_finalization import validate_memory_finalization
from validate_plan_fixtures import validate_fixture_contracts
from validate_preflight_fixtures import validate_preflight_fixtures
from validate_product_truth_gate import validate_product_truth_gate
from validate_quality_contract import validate_quality_contract
from validate_recording_cadence import validate_recording_cadence
from validate_self_improvement import validate_self_improvement
from validate_sites_routing import validate_sites_routing


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
        fail(f"missing JSON file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def require_text(path: Path, snippets: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            fail(f"{path.relative_to(ROOT)} is missing required text: {snippet}")


def validate_versions() -> str:
    loaded = [(path, load_json(path)) for path in MANIFESTS]
    versions = {data.get("version") for _, data in loaded}
    if len(versions) != 1 or None in versions:
        detail = ", ".join(
            f"{path.relative_to(ROOT)}={data.get('version')!r}" for path, data in loaded
        )
        fail(f"manifest versions differ: {detail}")
    version = versions.pop()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"version is not stable semver: {version}")
    if version != "2.7.0":
        fail(f"this release must be 2.7.0, got {version}")
    require_text(ROOT / "README.md", (f"v{version}", "Orange Build 2.7.0"))
    for policy_name in ("AGENTS.md", "CLAUDE.md"):
        require_text(
            ROOT / policy_name,
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
    if set(values) != {"name", "description"}:
        fail(f"{path.relative_to(ROOT)} frontmatter must contain only name and description")
    return values


def validate_skills_and_manifests() -> None:
    skill_dirs = sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir())
    if {path.name for path in skill_dirs} != {
        "orange-start",
        "orange-resume",
        "orange-design",
        "orange-secure",
    }:
        fail("shared skills directory must expose exactly the four Orange Build skills")
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        meta = parse_frontmatter(skill_file)
        if meta["name"] != skill_dir.name or not meta["description"]:
            fail(f"invalid skill metadata: {skill_dir.name}")
        openai = skill_dir / "agents" / "openai.yaml"
        require_text(
            openai,
            ("display_name:", "short_description:", "default_prompt:", f"${skill_dir.name}"),
        )

    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if codex.get("skills") != "./skills/":
        fail("Codex manifest must point to the shared skills source")
    default_prompts = codex.get("interface", {}).get("defaultPrompt")
    if not isinstance(default_prompts, list) or not 1 <= len(default_prompts) <= 3:
        fail("Codex interface.defaultPrompt must contain one to three starter prompts")
    for index, prompt in enumerate(default_prompts, start=1):
        if not isinstance(prompt, str) or not prompt.strip():
            fail(f"Codex defaultPrompt {index} must be a non-empty string")
        if len(prompt) > 128:
            fail(
                f"Codex defaultPrompt {index} exceeds the 128-character loader limit: "
                f"{len(prompt)}"
            )
    prompt_text = " ".join(default_prompts)
    for term in ("IA", "승인", "STEP", "완료 수준"):
        if term not in prompt_text:
            fail(f"Codex interface.defaultPrompt is missing the IA contract term: {term}")
    if marketplace.get("plugins", [{}])[0].get("source") != "./":
        fail("Claude marketplace must point to the same plugin root")
    for name, text in (
        ("Codex manifest", json.dumps(codex, ensure_ascii=False)),
        ("Claude manifest", json.dumps(claude, ensure_ascii=False)),
        ("Claude marketplace", json.dumps(marketplace, ensure_ascii=False)),
    ):
        if "IA" not in text or "단계" not in text:
            fail(f"{name} does not describe the IA step workflow")
    if "GPT-5.6" not in json.dumps(codex, ensure_ascii=False):
        fail("Codex metadata must declare the GPT-5.6 execution baseline")


def validate_workflow_documents() -> None:
    start = ROOT / "skills" / "orange-start" / "SKILL.md"
    resume = ROOT / "skills" / "orange-resume" / "SKILL.md"
    refs = ROOT / "skills" / "orange-start" / "references"
    readme = ROOT / "README.md"

    require_text(
        start,
        (
            "ia-collaboration.md",
            "phase-interview.md",
            "phase-plan.md",
            "phase-preflight.md",
            "phase-build.md",
            "phase-build-skill.md",
            "phase-build-automation.md",
            "phase-verify.md",
            "memory-log.md",
            "구형 v1·초기 v2 문서는 실행 계약이 아니다",
            "이 단계부터 만들까요?",
            "이대로 다음 개선 / 현재 결과 수정 /",
            "completion_level",
            "quality-contract.md",
        ),
    )
    require_text(
        resume,
        (
            "current_step",
            "completion_level",
            "AWAITING_APPROVAL",
            "IN_PROGRESS",
            "AWAITING_REVIEW",
            "APPROVED",
            "phase-verify.md",
            "atomicity: WAITING_USER",
            "skill_scope: atomic",
        ),
    )
    require_text(
        readme,
        (
            "Codex와 Claude Code 설치는 서로 독립적",
            "$orange-start",
            "/orange-start",
            "codex plugin marketplace upgrade orange-build",
            "claude plugin marketplace update orange-build",
            "$CODEX_HOME/skills",
            "~/.claude/skills",
            "Codex의 모델 선택기에서 **GPT-5.6**",
            "Customization overview",
            "GPT-5.6 model guidance",
            "같은 파일의 동시 수정",
        ),
    )

    required_refs = {
        "beginner-guardrails.md",
        "browser-steps.md",
        "codex-gpt-5p6.md",
        "codex-sites.md",
        "execution-profiles.md",
        "helpful-tools.md",
        "ia-collaboration.md",
        "memory-log.md",
        "phase-build-automation.md",
        "phase-build-skill.md",
        "phase-build.md",
        "phase-connect.md",
        "phase-interview.md",
        "phase-plan.md",
        "phase-preflight.md",
        "phase-verify.md",
        "product-truth-gate.md",
        "quality-contract.md",
        "self-improvement-loop.md",
        "sensitive-data.md",
        "troubleshooting.md",
        "verification-loop.md",
    }
    missing = sorted(name for name in required_refs if not (refs / name).is_file())
    if missing:
        fail(f"missing workflow references: {missing}")

    require_text(
        refs / "phase-connect.md",
        (
            "<github-owner>/<slug>",
            "--public",
            "사용자에게 확인받고 `--private`",
            "completion_level: local",
            "동의받지 않은 시스템·글로벌·프로젝트 설치를 실행하지 않는다",
            "git add --",
        ),
    )
    connect_text = (refs / "phase-connect.md").read_text(encoding="utf-8")
    if not re.search(r"gh repo create[^\n]*--public", connect_text):
        fail("phase-connect.md does not preserve the approved public-repository default")

    require_text(
        refs / "verification-loop.md",
        (
            "TEST-01",
            "결과물 인벤토리",
            "RED",
            "GREEN",
            "REFACTOR",
            "TESTED",
            "PARTIAL",
            "INFERRED",
            "`PLAN.md`는 IA 경계에서만 갱신",
        ),
    )
    require_text(
        refs / "self-improvement-loop.md",
        (
            "GPT-5.6",
            "AI가 묻지 않고 고칠 것",
            "사람이 결정할 것",
            "web_app",
            "ai_skill",
            "automation",
            "후보 변경 채택 게이트",
        ),
    )
    require_text(
        refs / "phase-plan.md",
        (
            "IMPLEMENTATION_REQUEST.md",
            "MATERIALS.md",
            "구형 문서에서 호환 TEST를 파생하거나 유형을 표시 문자열로 추론하지 않는다",
            "workflow: ia_collaborative",
            "completion_level: local | shared | real_work",
            "current_step: STEP-NN | complete",
            "승인 전에는",
        ),
    )
    require_text(
        refs / "phase-build-skill.md",
        (
            "$CODEX_HOME/skills",
            "~/.claude/skills",
            "새 작업",
            "TESTED",
            "RED",
            "skill_scope: atomic",
            "PASS | FAIL | EVIDENCE_MISSING",
            "별도 심판 스킬이나 숫자 점수를 기본으로 추가하지 않는다",
        ),
    )
    require_text(
        refs / "phase-build-automation.md",
        ("DRY_RUN_PASS", "공유 테스트 환경", "실제 계정", "AWAITING_REVIEW", "RED"),
    )
    require_text(
        refs / "phase-verify.md",
        (
            "모든 IA STEP이 `APPROVED`",
            "`local`: 로컬 핵심",
            "`shared`: 선택한 배포",
            "`real_work`: 실제 자료",
            "아직 증명하지 못한 것",
            "위험 기반 독립 완료 리뷰",
            "independent_review: NOT_NEEDED",
        ),
    )
    require_text(
        ROOT / "skills" / "orange-design" / "SKILL.md",
        ("completion_level", "기능·페이지·데이터", "getdesign.md", "Stitch", "functional/visual QA"),
    )
    require_text(
        ROOT / "skills" / "orange-secure" / "SKILL.md",
        ("find supabase -type f -name '*.sql'", "6개 휴리스틱에서 문제를 찾지 못했습니다"),
    )

    active_paths = [ROOT / "README.md", *MANIFESTS]
    active_paths.extend(sorted((ROOT / "skills").rglob("*.md")))
    active_text = "\n".join(path.read_text(encoding="utf-8") for path in active_paths)
    for pattern, label in (
        (r"gh repo create[^\n]*--private", "private GitHub repository default"),
        (r"AskUserQuestion", "Claude-only question tool"),
        (r"(?m)^\s*git add -A(?:\s|$)", "unsafe blanket staging"),
        (r"\bnpx\s+add-mcp\b", "multi-host MCP installer"),
        (r"derived_compat", "legacy compatibility TEST generation"),
        (r"기존 v1 기획서와 TEST가 없는 초기 v2 기획서도 지원", "legacy plan execution"),
    ):
        if re.search(pattern, active_text):
            fail(f"workflow regressed to {label}")


def validate_fixtures_and_specialized_contracts() -> None:
    validators = (
        validate_app_return,
        validate_codex_gpt56,
        validate_design_routing,
        validate_evidence_ui,
        validate_execution_profiles,
        validate_ia_workflow,
        validate_interview_flow,
        validate_memory_finalization,
        validate_fixture_contracts,
        validate_preflight_fixtures,
        validate_product_truth_gate,
        validate_quality_contract,
        validate_recording_cadence,
        validate_self_improvement,
        validate_sites_routing,
    )
    for validator in validators:
        try:
            validator(emit=False)
        except ValueError as exc:
            fail(f"{validator.__name__} failed: {exc}")


def main() -> None:
    version = validate_versions()
    validate_skills_and_manifests()
    validate_workflow_documents()
    validate_fixtures_and_specialized_contracts()
    print(f"OK: orange-build v{version} shared IA release invariants pass")


if __name__ == "__main__":
    try:
        main()
    except OSError as exc:
        fail(str(exc))
