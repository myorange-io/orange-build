#!/usr/bin/env python3
"""Validate the lightweight Orange Build quality contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "skills" / "orange-start" / "references"
FIXTURE = ROOT / "tests" / "fixtures" / "quality-contract-expectations.json"
QUALITY = REFS / "quality-contract.md"


def fail(message: str) -> None:
    raise ValueError(message)


def validate_quality_contract(*, emit: bool = True) -> str:
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    quality = QUALITY.read_text(encoding="utf-8")
    start = (ROOT / "skills" / "orange-start" / "SKILL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    release = (ROOT / "scripts" / "validate_release.py").read_text(encoding="utf-8")

    if expected["contract_version"] != 1:
        fail("quality contract fixture version changed unexpectedly")
    skill_names = sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
    if skill_names != expected["public_skills"]:
        fail(f"public skills {skill_names} != {expected['public_skills']}")
    if expected["runtime_guardrails"]["public_skill_count"] != len(skill_names):
        fail("public skill count guard does not match the shared skills source")
    if any("judge" in name or "reviewer" in name for name in skill_names):
        fail("a judge/reviewer was added as a default public skill")

    if expected["default_evaluator"] != "built_in_contract":
        fail("the default evaluator must stay inside the skill contract")
    if expected["forbidden_defaults"] != [
        "always_on_judge",
        "numeric_score",
        "recursive_judge",
    ]:
        fail("forbidden quality defaults changed unexpectedly")
    if expected["verdicts"] != ["PASS", "FAIL", "EVIDENCE_MISSING"]:
        fail("quality verdicts must stay explicit and non-numeric")
    if set(expected["validation_tiers"]) != {"targeted", "release", "independent"}:
        fail("quality validation tiers changed unexpectedly")
    if expected["validation_tiers"] != {
        "targeted": "changed_responsibility_only",
        "release": "full_contract_and_dual_host_smoke",
        "independent": "risk_triggered_only",
    }:
        fail("quality validation tier behavior changed unexpectedly")
    if any(expected["runtime_guardrails"][key] for key in (
        "full_suite_per_user_step",
        "extra_interview_question_for_validation",
        "recursive_evaluation",
    )):
        fail("a runtime guardrail enables slow recursive evaluation")

    for required in (
        "상시 심판 없이 회귀 막기",
        "PASS | FAIL | EVIDENCE_MISSING",
        "독립 검토는 기본 완료 조건이 아니다",
        "사용자 질문마다 전체 품질 suite를 실행하지 않는다",
        "공개 진입점은 `orange-start`, `orange-resume`, `orange-design`, `orange-secure` 네 개만 유지한다",
        "내부 책임 지도",
        "인지 과업 지도",
        "단일 과업 계약",
    ):
        if required not in quality:
            fail(f"quality-contract.md is missing: {required}")

    for journey in expected["canonical_journeys"]:
        if f"`{journey['id']}`" not in quality:
            fail(f"quality-contract.md is missing journey {journey['id']}")
        document = journey["document"]
        path = ROOT / "skills" / document if document.startswith("orange-start/") else REFS / document
        text = path.read_text(encoding="utf-8")
        if journey["required_text"] not in text:
            fail(f"{document} is missing journey evidence: {journey['required_text']}")

    for trigger in expected["independent_review_triggers"]:
        if trigger not in readme:
            fail(f"README.md is missing independent review trigger {trigger}")
    for required in (
        "quality-contract.md",
        "바뀐 범위와 가장 가까운 결정적 검증",
    ):
        if required not in start:
            fail(f"orange-start/SKILL.md is missing quality routing: {required}")
    if "validate_quality_contract" not in release:
        fail("validate_release.py does not run the quality contract validator")
    if "Orange Build 자체 품질 계약" not in readme:
        fail("README.md does not explain the product quality contract")
    self_improvement = (REFS / "self-improvement-loop.md").read_text(encoding="utf-8")
    if "독립 reviewer나 새 컨텍스트를 사용할 수 있으면" in self_improvement:
        fail("self-improvement-loop.md still enables an independent reviewer by default")
    for required in (
        "현재 상태·증거·실패 경계",
        "독립 reviewer는 반복 회귀",
        "independent_review: NOT_NEEDED",
    ):
        if required not in self_improvement:
            fail(f"self-improvement-loop.md is missing risk-based review behavior: {required}")

    for manifest in (
        ROOT / ".codex-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "plugin.json",
        ROOT / ".claude-plugin" / "marketplace.json",
    ):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("version") != "2.7.0":
            fail(f"{manifest.relative_to(ROOT)} is not version 2.7.0")

    message = (
        "PASS quality contract: journeys=6 public_skills=4 verdicts=3 "
        "tiers=targeted,release,independent default=built_in_contract"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_quality_contract()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
