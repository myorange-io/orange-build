#!/usr/bin/env python3
"""Validate product-fact uncertainty routing and its workflow integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "product-truth-expectations.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "product-truth-gate.md"

HIGH_IMPACT_FACTS = {
    "matching_ratio",
    "fee_rule",
    "quantitative_impact",
    "eligibility_rule",
    "privacy_rule",
    "automation_target",
}
RECOMMENDATIONS = {
    "matching_ratio": "CONFIRM_ACTUAL_FORMULA",
    "fee_rule": "CONFIRM_ACTUAL_FORMULA",
    "quantitative_impact": "REMOVE_NUMBER_UNTIL_CONFIRMED",
    "eligibility_rule": "USE_OFFICIAL_GUIDANCE_OR_DISABLE_CTA",
    "privacy_rule": "MINIMIZE_DATA_AND_CONFIRM_POLICY",
    "automation_target": "DRY_RUN_THEN_CONFIRM_TARGET",
}


def fail(message: str) -> None:
    raise ValueError(message)


def resolve(spec: dict) -> dict[str, object]:
    fact_type = spec["fact_type"]
    if spec["source_confirmed"]:
        return {
            "action": "IMPLEMENT",
            "state": "FACT_CONFIRMED: source",
            "ask_user": False,
            "allow_public_claim": True,
            "allow_production": True,
            "allow_dry_run": True,
            "continuation": "ALL_WORK",
            "recommendation": None,
        }
    if spec["user_confirmed"]:
        return {
            "action": "IMPLEMENT",
            "state": "FACT_CONFIRMED: user",
            "ask_user": False,
            "allow_public_claim": True,
            "allow_production": True,
            "allow_dry_run": True,
            "continuation": "ALL_WORK",
            "recommendation": None,
        }
    if fact_type not in HIGH_IMPACT_FACTS:
        return {
            "action": "AUTO_DEFAULT",
            "state": "IMPLEMENTATION_CHOICE",
            "ask_user": False,
            "allow_public_claim": True,
            "allow_production": True,
            "allow_dry_run": True,
            "continuation": "ALL_WORK",
            "recommendation": None,
        }
    return {
        "action": "ASK_WITH_RECOMMENDATION",
        "state": "FACT_UNVERIFIED",
        "ask_user": True,
        "allow_public_claim": False,
        "allow_production": False,
        "allow_dry_run": True,
        "continuation": "UNRELATED_WORK_ONLY",
        "recommendation": RECOMMENDATIONS[fact_type],
    }


def require(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            fail(f"{document} is missing product-truth behavior: {snippet}")


def validate_product_truth_gate(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "matching-example-only",
        "matching-source-explicit",
        "impact-placeholder-00",
        "automation-target-unknown",
        "privacy-retention-unknown",
        "visual-radius-default",
        "user-confirmed-fee",
    }
    if set(fixtures) != expected_names:
        fail("product-truth fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            fail(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: action={actual['action']} state={actual['state']}"
        )

    reference = REFERENCE.read_text(encoding="utf-8")
    require(
        reference,
        (
            "10,000원 → 예: 20,000원",
            "FACT_CONFIRMED: source",
            "FACT_CONFIRMED: user",
            "FACT_UNVERIFIED",
            "확인이 필요한 값",
            "현재 근거",
            "권장안",
            "다른 선택",
            "지금 필요한 답",
            "면책 문구",
            "`TEST-01`, `REQ-02`, `임시 가정`, `운영자 확인 후 변경`",
            "둘 다 있어야",
        ),
        "product-truth-gate.md",
    )

    routed_documents = (
        ROOT / "skills" / "orange-start" / "SKILL.md",
        ROOT / "skills" / "orange-start" / "references" / "phase-plan.md",
        ROOT / "skills" / "orange-start" / "references" / "phase-build.md",
        ROOT / "skills" / "orange-start" / "references" / "phase-build-skill.md",
        ROOT / "skills" / "orange-start" / "references" / "phase-build-automation.md",
        ROOT / "skills" / "orange-start" / "references" / "self-improvement-loop.md",
        ROOT / "skills" / "orange-start" / "references" / "phase-verify.md",
        ROOT / "skills" / "orange-resume" / "SKILL.md",
    )
    for path in routed_documents:
        require(
            path.read_text(encoding="utf-8"),
            ("product-truth-gate.md",),
            str(path.relative_to(ROOT)),
        )

    verification = (
        ROOT / "skills" / "orange-start" / "references" / "verification-loop.md"
    ).read_text(encoding="utf-8")
    require(
        verification,
        (
            "제품 사실 증거",
            "단일 TEST의 예시값, 코드 상수, 화면 캡처는",
            "사업 사실의 근거가 아니다",
            "FACT_UNVERIFIED",
            "BLOCKED",
            "PARTIAL",
        ),
        "verification-loop.md",
    )

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_product_truth_gate()
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
