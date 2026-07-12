#!/usr/bin/env python3
"""Validate Orange Build App copy contracts against orange-start routing rules."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
SUPPORTED_CONTRACT_VERSION = 2
CANONICAL_KINDS = {"web_app", "ai_skill", "automation"}
ROUTES = {
    "web_app": "phase-build.md",
    "ai_skill": "phase-build-skill.md",
    "automation": "phase-build-automation.md",
}
COPY_TEST_INSTRUCTION = (
    "원본 기획서의 TEST 항목을 PLAN.md 요구사항의 완료 조건과 검증 증거에 연결하세요."
)
DISPLAY_PATTERNS = {
    "web_app": r"(?:웹\s*앱|웹앱|web\s*app|webapp)",
    "ai_skill": r"(?:AI\s*작업\s*스킬|AI\s*스킬|스킬|skill)",
    "automation": r"(?:자동화|automation|workflow)",
}


@dataclass(frozen=True)
class Resolution:
    status: str
    kind: str | None
    route: str | None
    source_contract_version: int | str


@dataclass(frozen=True)
class VerificationScenario:
    test_id: str
    title: str
    setup: str
    action: str
    expected: str
    evidence: str


def fail(message: str) -> None:
    raise ValueError(message)


def metadata_from(text: str) -> dict[str, str]:
    match = re.search(
        r"^## 기획서 메타데이터\n(?P<body>.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        fail("missing metadata section")
    metadata: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def display_kind(value: str | None) -> str | None:
    normalized = (value or "").lower()
    for pattern in DISPLAY_PATTERNS.values():
        normalized = re.sub(
            rf"{pattern}\s*(?:으로|은|는|이|가|을|를)?\s*"
            r"(?:제공|사용|구현|제작|만들)?\s*"
            r"(?:하지\s*않(?:음|는다)?|않(?:음|는다)?|아님|아니다|제외|미지원)",
            " ",
            normalized,
            flags=re.IGNORECASE,
        )
    matches = {
        kind
        for kind, pattern in DISPLAY_PATTERNS.items()
        if re.search(pattern, normalized, flags=re.IGNORECASE)
    }
    return next(iter(matches)) if len(matches) == 1 else None


def source_plan_from(text: str) -> str:
    match = re.search(
        r"^## 원본 기획서\s*\n(?P<body>[\s\S]*)\Z",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        fail("missing source-plan section")
    return match.group("body")


def verification_scenarios(text: str) -> list[VerificationScenario]:
    """Parse the Orange Build App v2 TEST blocks from the copied source plan."""
    headings = list(
        re.finditer(
            r"^### (?P<test_id>TEST-\d{2})\s+[—-]\s+(?P<title>.+?)\s*$",
            text,
            flags=re.MULTILINE,
        )
    )
    declared_ids = re.findall(r"^### (TEST-\d{2})\b", text, flags=re.MULTILINE)
    if len(declared_ids) != len(headings):
        fail("verification scenario heading must use '### TEST-NN — title'")
    scenarios: list[VerificationScenario] = []
    seen: set[str] = set()
    field_names = {
        "준비": "setup",
        "행동": "action",
        "기대 결과": "expected",
        "통과 증거": "evidence",
    }
    for heading in headings:
        test_id = heading.group("test_id")
        if test_id in seen:
            fail(f"duplicate verification scenario: {test_id}")
        seen.add(test_id)
        next_heading = re.search(r"^#{1,3}\s+", text[heading.end() :], flags=re.MULTILINE)
        body_end = (
            heading.end() + next_heading.start() if next_heading is not None else len(text)
        )
        body = text[heading.end() : body_end]
        values: dict[str, str] = {}
        for label, attribute in field_names.items():
            matches = re.findall(
                rf"^- {re.escape(label)}:\s*(\S.*)$",
                body,
                flags=re.MULTILINE,
            )
            if len(matches) != 1:
                fail(f"{test_id}: expected exactly one '{label}' field")
            values[attribute] = matches[0].strip()
        scenarios.append(
            VerificationScenario(
                test_id=test_id,
                title=heading.group("title").strip(),
                setup=values["setup"],
                action=values["action"],
                expected=values["expected"],
                evidence=values["evidence"],
            )
        )
    return scenarios


def resolve(text: str) -> Resolution:
    metadata = metadata_from(text)
    raw_version = metadata.get("contract_version")
    if raw_version is None:
        source_version: int | str = "legacy"
    else:
        try:
            source_version = int(raw_version)
        except ValueError:
            fail(f"invalid contract_version: {raw_version}")
    if isinstance(source_version, int) and source_version >= SUPPORTED_CONTRACT_VERSION:
        if metadata.get("source") != "orange-build-app":
            fail("contract v2+ requires source: orange-build-app")
    if isinstance(source_version, int) and source_version > SUPPORTED_CONTRACT_VERSION:
        return Resolution("update_required", None, None, source_version)

    canonical = metadata.get("deliverable_kind")
    if source_version == SUPPORTED_CONTRACT_VERSION and canonical is not None:
        if canonical not in CANONICAL_KINDS:
            fail(f"invalid deliverable_kind: {canonical}")
        return Resolution("ready", canonical, ROUTES[canonical], source_version)

    fallback = display_kind(metadata.get("추천 결과물 형태"))
    if fallback is None:
        return Resolution("ambiguous", None, None, source_version)
    return Resolution("ready", fallback, ROUTES[fallback], source_version)


def validate_fixture_contracts(*, emit: bool = True) -> list[str]:
    expectations = json.loads((FIXTURES / "expectations.json").read_text(encoding="utf-8"))
    expected_names = {
        "web-app-plan.md",
        "ai-skill-plan.md",
        "automation-plan.md",
        "legacy-v2-no-tests-plan.md",
        "legacy-v1-plan.md",
        "unsupported-v3-plan.md",
    }
    if set(expectations) != expected_names:
        fail("expectations must cover exactly six copy-contract fixtures")

    fallback_cases = {
        "웹앱": "web_app",
        "AI 작업 스킬": "ai_skill",
        "자동화 워크플로": "automation",
        "웹앱 또는 자동화": None,
        "AI 작업 스킬 · 웹앱으로 제공하지 않음": "ai_skill",
    }
    for display, expected_kind in fallback_cases.items():
        if display_kind(display) != expected_kind:
            fail(f"legacy display routing regressed: {display!r}")

    phase_plan = (ROOT / "skills" / "orange-start" / "references" / "phase-plan.md").read_text(
        encoding="utf-8"
    )
    for required in (
        "SOURCE_PLAN.md",
        "REQ-*",
        "contract_version: 2",
        "deliverable_kind",
        "현재 orange-start는 v2까지만",
        "플러그인을 업데이트",
        "검증 시나리오 계약",
        "TEST-01",
        "준비",
        "행동",
        "기대 결과",
        "통과 증거",
    ):
        if required not in phase_plan:
            fail(f"phase-plan.md is missing contract behavior: {required}")
    if not re.search(
        r"TEST 항목이 없는.{0,80}(기존|이전|legacy).{0,40}v2",
        phase_plan,
        flags=re.DOTALL | re.IGNORECASE,
    ):
        fail("phase-plan.md is missing the legacy v2 without TEST compatibility path")
    if not re.search(
        r"(추가 질문 없이|사용자에게 묻지).{0,120}(3개|TEST-03)",
        phase_plan,
        flags=re.DOTALL,
    ):
        fail("phase-plan.md must derive three compatibility tests without another question")

    lines: list[str] = []
    for filename in sorted(expected_names):
        text = (FIXTURES / filename).read_text(encoding="utf-8")
        if not text.startswith("Orange Build 플러그인의 orange-start를 사용해"):
            fail(f"{filename}: missing orange-start copy envelope")
        resolution = resolve(text)
        source_plan = source_plan_from(text) if resolution.status == "ready" else ""
        expected = expectations[filename]
        if resolution.status != expected["expected_status"]:
            fail(f"{filename}: status {resolution.status} != {expected['expected_status']}")
        if resolution.kind != expected["expected_kind"]:
            fail(f"{filename}: kind {resolution.kind} != {expected['expected_kind']}")
        if resolution.route != expected["expected_route"]:
            fail(f"{filename}: route {resolution.route} != {expected['expected_route']}")
        if resolution.route and not (
            ROOT / "skills" / "orange-start" / "references" / resolution.route
        ).is_file():
            fail(f"{filename}: missing implementation route: {resolution.route}")
        if resolution.source_contract_version != expected["source_contract_version"]:
            fail(
                f"{filename}: source version {resolution.source_contract_version} "
                f"!= {expected['source_contract_version']}"
            )
        test_contract = expected["expected_test_contract"]
        if resolution.status == "ready":
            for term in expected["required_source_terms"]:
                if term not in source_plan:
                    fail(f"{filename}: missing source term from ## 원본 기획서: {term}")
        scenarios = verification_scenarios(source_plan) if resolution.status == "ready" else []
        test_ids = [scenario.test_id for scenario in scenarios]
        if test_ids != expected["expected_test_ids"]:
            fail(f"{filename}: test ids {test_ids} != {expected['expected_test_ids']}")
        if test_contract == "source_v2":
            if test_ids != ["TEST-01", "TEST-02", "TEST-03"]:
                fail(f"{filename}: current app v2 must provide TEST-01 through TEST-03")
            if COPY_TEST_INSTRUCTION not in text[: text.find("## 기획서 메타데이터")]:
                fail(f"{filename}: missing current app TEST handoff instruction")
            if "## 직접 확인할 3가지" not in source_plan:
                fail(f"{filename}: missing current app verification section")
        elif test_contract == "derived_compat":
            if resolution.status != "ready" or scenarios:
                fail(f"{filename}: derived compatibility requires a supported ready plan without TEST blocks")
        elif test_contract not in {"legacy", "unsupported"}:
            fail(f"{filename}: unknown expected_test_contract: {test_contract}")
        if resolution.status == "ready":
            if "SOURCE_PLAN.md" not in phase_plan or "REQ-*" not in phase_plan:
                fail(f"{filename}: source preservation or requirement tracing regressed")
            test_summary = (
                f"source_tests={len(scenarios)}"
                if test_contract != "derived_compat"
                else "source_tests=0 derived_test_rule=3"
            )
            lines.append(
                f"PASS {filename}: kind={resolution.kind} route={resolution.route} "
                f"source_rule=SOURCE_PLAN.md req_mapping_rule=PLAN.md test_contract={test_contract} "
                f"{test_summary}"
            )
        else:
            lines.append(
                f"PASS {filename}: status=update_required action=plugin_update"
            )
    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_fixture_contracts()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
