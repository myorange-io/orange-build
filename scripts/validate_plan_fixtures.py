#!/usr/bin/env python3
"""Validate current IA plan inputs and routing without legacy inference."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
CANONICAL_KINDS = {"web_app", "ai_skill", "automation"}
ROUTES = {
    "web_app": "phase-build.md",
    "ai_skill": "phase-build-skill.md",
    "automation": "phase-build-automation.md",
}


@dataclass(frozen=True)
class Resolution:
    status: str
    kind: str | None
    route: str | None
    source_contract_version: int | str
    source_type: str


def fail(message: str) -> None:
    raise ValueError(message)


def metadata_from(text: str) -> dict[str, str]:
    match = re.search(
        r"^## 기획서 메타데이터\n(?P<body>.*?)(?=^## |^# (?!#)|\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        fail("missing metadata section")
    metadata: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        line = raw_line.strip()
        if line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def source_plan_from(text: str, source_type: str) -> str:
    if source_type == "orange-build-app":
        match = re.search(r"^## 원본 기획서\s*\n(?P<body>[\s\S]*)\Z", text, flags=re.MULTILINE)
        if not match:
            fail("current app copy is missing the source plan section")
        return match.group("body")
    return text


def is_current_ia_plan(text: str) -> bool:
    return all(
        marker in text
        for marker in (
            "## 직접 확인할 3가지",
            "## 함께 구현할 순서",
            "### 첫 번째 작은 완성 ·",
            "확인할 변화:",
            "완료 확인:",
            "이번 단계에서 하지 않을 것:",
        )
    )


def resolve(text: str) -> Resolution:
    metadata = metadata_from(text)
    source_type = metadata.get("source", "")
    raw_contract = metadata.get("contract_version")
    if raw_contract is not None:
        try:
            contract: int | str = int(raw_contract)
        except ValueError:
            fail(f"invalid contract_version: {raw_contract}")
        if contract > 2:
            return Resolution("update_required", None, None, contract, source_type)
    elif source_type in {"orange-start-interview", "orange-start-regenerated"} and metadata.get("interview_contract_version") == "2":
        contract = "local-ia"
    else:
        return Resolution("regenerate", None, None, "legacy", source_type or "legacy")

    kind = metadata.get("deliverable_kind")
    if kind not in CANONICAL_KINDS:
        fail(f"missing or invalid canonical deliverable_kind: {kind!r}")
    source_plan = source_plan_from(text, source_type)
    if not is_current_ia_plan(source_plan):
        return Resolution("regenerate", None, None, contract, source_type)
    return Resolution("ready", kind, ROUTES[kind], contract, source_type)


def validate_steps(source: str, filename: str) -> None:
    headings = list(
        re.finditer(
            r"^### (?P<label>첫 번째 작은 완성 · .+|다음 개선 \d+ · .+)$",
            source,
            flags=re.MULTILINE,
        )
    )
    if not headings or not headings[0].group("label").startswith("첫 번째 작은 완성"):
        fail(f"{filename}: missing first collaborative completion")
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        body = source[heading.end():end]
        for field in ("확인할 변화", "완료 확인", "이번 단계에서 하지 않을 것"):
            if len(re.findall(rf"^- {re.escape(field)}:\s*\S", body, flags=re.MULTILINE)) != 1:
                fail(f"{filename}: {heading.group('label')} must contain one {field}")


def validate_tests(source: str, filename: str) -> None:
    ids = re.findall(r"^### (TEST-\d{2})\s+[—-]", source, flags=re.MULTILINE)
    if ids != ["TEST-01", "TEST-02", "TEST-03"]:
        fail(f"{filename}: tests must be exactly TEST-01 through TEST-03")
    for test_id in ids:
        start = source.index(f"### {test_id}")
        tail = source[start:]
        next_heading = re.search(r"\n### |\n## ", tail[1:])
        body = tail if next_heading is None else tail[: next_heading.start() + 1]
        for field in ("준비", "행동", "기대 결과", "통과 증거"):
            if f"- {field}:" not in body:
                fail(f"{filename}: {test_id} is missing {field}")


def validate_ai_skill_source(source: str, filename: str) -> None:
    for section in ("## 인지 과업 지도", "## 단일 과업 계약"):
        if section not in source:
            fail(f"{filename}: missing AI skill source section {section}")
    for field in (
        "전체 업무",
        "사람이 맡을 과업",
        "AI 후보 과업",
        "이번 스킬이 맡을 과업",
        "사람이 달성하려는 전체 결과",
        "이번 스킬이 맡을 한 가지 인지 과업",
        "입력",
        "처리",
        "출력",
        "하지 않을 일",
        "사람이 판단할 일",
        "다음 스킬에 넘길 형식",
    ):
        if not re.search(rf"^- {re.escape(field)}:\s*\S", source, flags=re.MULTILINE):
            fail(f"{filename}: AI skill source contract is missing {field}")


def validate_fixture_contracts(*, emit: bool = True) -> list[str]:
    expectations = json.loads((FIXTURES / "expectations.json").read_text(encoding="utf-8"))
    expected_names = {
        "web-app-plan.md",
        "ai-skill-plan.md",
        "automation-plan.md",
        "local-ia-plan.md",
        "unsupported-v3-plan.md",
    }
    if set(expectations) != expected_names:
        fail("expectations must cover the four current IA plans and future contract fixture")
    if any((FIXTURES / name).exists() for name in ("legacy-v1-plan.md", "legacy-v2-no-tests-plan.md")):
        fail("legacy plan fixtures must be removed")

    phase_plan = (ROOT / "skills" / "orange-start" / "references" / "phase-plan.md").read_text(encoding="utf-8")
    for required in (
        "최신 구조 판정과 구형 전환",
        "구형 문서는 계약이 아니라 `legacy_seed` 초기 아이디어",
        "구형 문서에서 호환 TEST를 파생하거나 유형을 표시 문자열로 추론하지 않는다",
        "workflow: ia_collaborative",
        "current_step: STEP-NN | complete",
        "검증 시나리오 계약",
        "IA 단계",
        "현재 App의 `ai_skill` 기획서에 `인지 과업 지도`나 `단일 과업 계약`이 없다는 이유만으로 구형으로",
        "## AI 스킬 단일 과업 계약",
        "## AI 스킬 내장 평가 계약",
    ):
        if required not in phase_plan:
            fail(f"phase-plan.md is missing current contract behavior: {required}")

    lines: list[str] = []
    for filename in sorted(expected_names):
        text = (FIXTURES / filename).read_text(encoding="utf-8")
        expected = expectations[filename]
        resolution = resolve(text)
        for field in ("expected_status", "expected_kind", "expected_route", "source_contract_version", "source_type"):
            actual = {
                "expected_status": resolution.status,
                "expected_kind": resolution.kind,
                "expected_route": resolution.route,
                "source_contract_version": resolution.source_contract_version,
                "source_type": resolution.source_type,
            }[field]
            if actual != expected[field]:
                fail(f"{filename}: {field} {actual!r} != {expected[field]!r}")

        if resolution.status == "ready":
            source = source_plan_from(text, resolution.source_type)
            for term in expected["required_source_terms"]:
                if term not in source:
                    fail(f"{filename}: missing source term {term}")
            validate_tests(source, filename)
            validate_steps(source, filename)
            if resolution.kind == "ai_skill":
                validate_ai_skill_source(source, filename)
                if expected.get("missing_task_map_action") != "enrich_plan_without_legacy_regeneration":
                    fail(f"{filename}: missing current App AI skill enrichment expectation")
                source_without_task_map = re.sub(
                    r"\n## 인지 과업 지도\n.*?(?=\n## 성공 기준\n)",
                    "\n",
                    text,
                    count=1,
                    flags=re.DOTALL,
                )
                if source_without_task_map == text:
                    fail(f"{filename}: could not build the current App fallback case")
                fallback = resolve(source_without_task_map)
                if (fallback.status, fallback.kind, fallback.route) != (
                    "ready",
                    "ai_skill",
                    "phase-build-skill.md",
                ):
                    fail(
                        f"{filename}: current App plan without new task-map sections "
                        "must be enriched, not regenerated as legacy"
                    )
            level = expected["completion_level"]
            if level not in source:
                fail(f"{filename}: missing completion level {level}")
            if resolution.source_type == "orange-build-app":
                if not text.startswith("아래 기획서를 바탕으로 실제로 동작하는 결과물을 참가자와 함께 단계적으로 구현하세요."):
                    fail(f"{filename}: missing current app copy envelope")
                for marker in ("## 협력 구현 원칙", "이 단계부터 만들까요?", "명시적 동의 전에는 코드를 작성하지 마세요"):
                    if marker not in text[: text.find("## 기획서 메타데이터")]:
                        fail(f"{filename}: missing current collaboration marker {marker}")
            lines.append(
                f"PASS {filename}: kind={resolution.kind} route={resolution.route} "
                f"source={resolution.source_type} completion={level} tests=3 steps=current"
                + (" task_map_fallback=enrich" if resolution.kind == "ai_skill" else "")
            )
        else:
            if resolution.status != "update_required":
                fail(f"{filename}: unexpected non-ready status {resolution.status}")
            lines.append(f"PASS {filename}: status=update_required action=plugin_update")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_fixture_contracts()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
