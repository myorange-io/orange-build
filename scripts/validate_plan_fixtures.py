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


@dataclass(frozen=True)
class Resolution:
    status: str
    kind: str | None
    route: str | None
    source_contract_version: int | str


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
    if "웹앱" in normalized or "web app" in normalized or "webapp" in normalized:
        return "web_app"
    if "스킬" in normalized or "skill" in normalized:
        return "ai_skill"
    if "자동화" in normalized or "automation" in normalized or "workflow" in normalized:
        return "automation"
    return None


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
        "legacy-v1-plan.md",
        "unsupported-v3-plan.md",
    }
    if set(expectations) != expected_names:
        fail("expectations must cover exactly five copy-contract fixtures")

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
    ):
        if required not in phase_plan:
            fail(f"phase-plan.md is missing contract behavior: {required}")

    lines: list[str] = []
    for filename in sorted(expected_names):
        text = (FIXTURES / filename).read_text(encoding="utf-8")
        if not text.startswith("Orange Build 플러그인의 orange-start를 사용해"):
            fail(f"{filename}: missing orange-start copy envelope")
        if "## 원본 기획서" not in text:
            fail(f"{filename}: missing source-plan section")
        resolution = resolve(text)
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
        for term in expected["required_source_terms"]:
            if term not in text:
                fail(f"{filename}: missing source term: {term}")
        if resolution.status == "ready":
            if "SOURCE_PLAN.md" not in phase_plan or "REQ-*" not in phase_plan:
                fail(f"{filename}: source preservation or requirement tracing regressed")
            lines.append(
                f"PASS {filename}: kind={resolution.kind} route={resolution.route} "
                "source=SOURCE_PLAN.md req_trace=PLAN.md"
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
