#!/usr/bin/env python3
"""Validate the shared Codex/Claude Code IA workflow contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
EXPECTATIONS = FIXTURES / "ia-workflow-expectations.json"
PACKAGE = FIXTURES / "implementation-package.json"
REFS = ROOT / "skills" / "orange-start" / "references"


def fail(message: str) -> None:
    raise ValueError(message)


def require(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            fail(f"{document} is missing IA behavior: {snippet}")


def reject(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet in text:
            fail(f"{document} keeps removed behavior: {snippet}")


def validate_current_plan_fixture(path: Path, expected_level: str) -> None:
    text = path.read_text(encoding="utf-8")
    require(
        text,
        (
            "## 직접 확인할 3가지",
            "### TEST-01",
            "### TEST-02",
            "### TEST-03",
            "## 함께 구현할 순서",
            "### 첫 번째 작은 완성 ·",
            "확인할 변화:",
            "완료 확인:",
            "이번 단계에서 하지 않을 것:",
        ),
        path.name,
    )
    test_ids = re.findall(r"^### (TEST-\d{2})\s+[—-]", text, flags=re.MULTILINE)
    if test_ids != ["TEST-01", "TEST-02", "TEST-03"]:
        fail(f"{path.name}: expected exactly TEST-01 through TEST-03, got {test_ids}")
    if expected_level not in text:
        fail(f"{path.name}: missing completion level {expected_level}")
    if "## 바로 시작할 순서" in text:
        fail(f"{path.name}: uses the legacy implementation sequence")


def validate_ia_workflow(*, emit: bool = True) -> list[str]:
    expected = json.loads(EXPECTATIONS.read_text(encoding="utf-8"))
    interview = (REFS / "phase-interview.md").read_text(encoding="utf-8")
    plan = (REFS / "phase-plan.md").read_text(encoding="utf-8")
    ia = (REFS / "ia-collaboration.md").read_text(encoding="utf-8")
    profiles = (REFS / "execution-profiles.md").read_text(encoding="utf-8")
    skill_build = (REFS / "phase-build-skill.md").read_text(encoding="utf-8")
    automation_build = (REFS / "phase-build-automation.md").read_text(encoding="utf-8")
    web_build = (REFS / "phase-build.md").read_text(encoding="utf-8")
    verify = (REFS / "phase-verify.md").read_text(encoding="utf-8")
    memory = (REFS / "memory-log.md").read_text(encoding="utf-8")
    start = (ROOT / "skills" / "orange-start" / "SKILL.md").read_text(encoding="utf-8")
    resume = (ROOT / "skills" / "orange-resume" / "SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    commit = expected["app_reference_commit"]
    if commit not in interview:
        fail("phase-interview.md does not pin the approved app reference commit")
    if expected["max_guided_questions"] != 10 or "최대 기획 질문 수는 **10개**" not in interview:
        fail("no-plan flow must allow at most ten guided questions")

    cursor = -1
    for phase_id in expected["phase_order"]:
        position = interview.find(f"`{phase_id}`", cursor + 1)
        if position <= cursor:
            fail(f"phase order regressed at {phase_id}")
        cursor = position

    require(
        interview,
        (
            "한 번에 질문은 **하나만**",
            "선택지 2~3개",
            "추천안을 첫 번째",
            "구조화 질문 기능이 있으면",
            "일반 대화로 제시",
            "completion_level: local",
            "## 함께 구현할 순서",
            "## 반드시 반영할 자료",
            "그대로 유지할 요소",
            "열린 질문",
        ),
        "phase-interview.md",
    )

    require(
        plan,
        (
            "IMPLEMENTATION_REQUEST.md",
            "MATERIALS.md",
            "materials/",
            "최신 구조 판정과 구형 전환",
            "구형 문서는 계약이 아니라 `legacy_seed` 초기 아이디어",
            "호환 TEST를 파생",
            "workflow: ia_collaborative",
            "completion_level: local | shared | real_work",
            "current_step: STEP-NN | complete",
            "AWAITING_APPROVAL · NOT_RUN",
            "승인 전에는",
            "프로젝트 파일 생성·수정",
        ),
        "phase-plan.md",
    )

    states = expected["state_transitions"]
    state_chain = " → ".join(states)
    require(
        ia,
        (
            state_chain,
            "이 단계부터 만들까요?",
            "명시적 동의 전에는 코드, 설정, 데이터, 프로젝트 문서를 수정하지 않는다",
            "current_step",
            "배포와 공개 범위 변경",
            "실제 데이터 생성·수정·삭제·마이그레이션",
        ),
        "ia-collaboration.md",
    )
    for choice in expected["review_choices"]:
        if choice not in ia:
            fail(f"ia-collaboration.md is missing review choice: {choice}")

    gates = expected["completion_gates"]
    gate_documents = {
        "web_app": web_build + verify + profiles,
        "ai_skill": skill_build + verify + profiles,
        "automation": automation_build + verify + profiles,
    }
    required_gate_terms = {
        "web_app": {
            "local": "로컬 핵심",
            "shared": "공유 URL",
            "real_work": "복구",
        },
        "ai_skill": {
            "local": "현재 호스트 개인 경로 등록",
            "shared": "격리 또는 대상 환경",
            "real_work": "실제 업무 자료",
        },
        "automation": {
            "local": "dry-run",
            "shared": "공유 테스트 환경",
            "real_work": "실제 계정",
        },
    }
    for kind, levels in gates.items():
        if set(levels) != {"local", "shared", "real_work"}:
            fail(f"{kind}: completion gate levels changed")
        for level, term in required_gate_terms[kind].items():
            if term not in gate_documents[kind]:
                fail(f"{kind}/{level}: missing completion gate term {term}")

    package = json.loads(PACKAGE.read_text(encoding="utf-8"))
    if package["archive_files"][:3] != ["PLAN.md", "IMPLEMENTATION_REQUEST.md", "MATERIALS.md"]:
        fail("implementation package must begin with the current three contract files")
    if not any(name.startswith("materials/") for name in package["archive_files"]):
        fail("implementation package fixture has no materials directory")
    for material in package["materials"]:
        for key in ("purpose", "summary", "required_rules", "exact_elements", "apply_to", "open_questions"):
            if key not in material:
                fail(f"implementation package material is missing {key}")
    if not all(package["expected_behavior"].values()):
        fail("implementation package safety expectations must all be true")

    fixture_levels = {
        "web-app-plan.md": "shared",
        "ai-skill-plan.md": "local",
        "automation-plan.md": "real_work",
        "local-ia-plan.md": "local",
    }
    for filename, level in fixture_levels.items():
        validate_current_plan_fixture(FIXTURES / filename, level)

    for removed in ("legacy-v1-plan.md", "legacy-v2-no-tests-plan.md"):
        if (FIXTURES / removed).exists():
            fail(f"removed legacy fixture still exists: {removed}")
    reject(
        "\n".join((start, plan, interview, verify, readme)),
        ("derived_compat", "표시 문자열과 본문 근거로", "기존 v1 기획서와 TEST가 없는 초기 v2 기획서도 지원"),
        "active IA workflow",
    )

    host_terms = expected["hosts"]
    combined = "\n".join((start, ia, skill_build, resume, readme))
    for host, contract in host_terms.items():
        for key, value in contract.items():
            if value not in combined:
                fail(f"{host}: shared workflow is missing {key}={value}")
    require(
        combined,
        ("새 작업", "$스킬이름", "/스킬이름", "자연어 호출"),
        "dual-host skill workflow",
    )

    codex_manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    claude_manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    if {codex_manifest["version"], claude_manifest["version"], marketplace["version"]} != {"2.6.0"}:
        fail("all three manifests must be version 2.6.0")
    if codex_manifest.get("skills") != "./skills/":
        fail("Codex manifest must point at the shared skills directory")
    if marketplace["plugins"][0].get("source") != "./":
        fail("Claude marketplace must point at the plugin root with the shared skills directory")

    require(
        memory,
        (
            "선택한 완료 수준의 구현 완료 증거",
            "완료 수준: [local / shared / real_work]",
            "marker 블록이 이미 하나 있으면 새 항목을 append하지 않고",
        ),
        "memory-log.md",
    )
    require(
        resume,
        ("completion_level", "current_step", "AWAITING_APPROVAL", "AWAITING_REVIEW"),
        "orange-resume/SKILL.md",
    )

    lines = [
        "PASS IA app sync: commit=7378c12104 phases=7 max_questions=10",
        "PASS IA inputs: latest_copy implementation_package local_plan legacy_regeneration",
        "PASS IA state: approval_before_edit review_choices=3 external_confirmation=separate",
        "PASS IA completion: deliverables=3 levels=3",
        "PASS IA hosts: codex claude_code shared_skills=./skills/",
    ]
    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_ia_workflow()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
