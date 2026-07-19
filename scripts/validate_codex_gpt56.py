#!/usr/bin/env python3
"""Validate Codex GPT-5.6 profile and safe coordination routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "codex-gpt56-expectations.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "codex-gpt-5p6.md"


def resolve(spec: dict) -> dict[str, str]:
    if spec["host"] != "codex":
        return {"profile": "HOST_DEFAULT", "coordination": "SINGLE_AGENT"}

    profile = "GPT56" if spec["model"].lower() == "gpt-5.6" else "CODEX_COMPATIBLE"
    if spec["requires_human_decision"]:
        coordination = "HUMAN_GATE"
    elif spec["overlapping_writes"] or spec["external_write"]:
        coordination = "SINGLE_WRITER"
    elif spec["independent_read_workstreams"] >= 2:
        coordination = "BOUNDED_PARALLEL"
    else:
        coordination = "SINGLE_AGENT"
    return {"profile": profile, "coordination": coordination}


def validate_codex_gpt56(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "single-agent-implementation",
        "bounded-parallel-read-review",
        "overlapping-writes-one-writer",
        "approved-deploy-one-writer",
        "unapproved-external-change-human-gate",
        "claude-host-neutral",
    }
    if set(fixtures) != expected_names:
        raise ValueError("Codex GPT-5.6 fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: profile={actual['profile']} coordination={actual['coordination']}"
        )

    reference = REFERENCE.read_text(encoding="utf-8")
    for required in (
        "목표 산출물",
        "보호 계약",
        "완료 증거",
        "사람 게이트",
        "programmatic tool calling",
        "서브에이전트 사용 경계",
        "같은 파일이나",
        "외부 쓰기·배포·발송·삭제",
        "모델의 자신감이나 자기평가는 증거가 아니다",
    ):
        if required not in reference:
            raise ValueError(f"codex-gpt-5p6.md is missing behavior: {required}")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_codex_gpt56()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
