#!/usr/bin/env python3
"""Validate guided/adaptive routing and implementation-to-release semantics."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "execution-profile-expectations.json"
PROFILE_REF = ROOT / "skills" / "orange-start" / "references" / "execution-profiles.md"


def fail(message: str) -> None:
    raise ValueError(message)


def resolve(spec: dict) -> dict:
    profile = "adaptive" if spec["existing_project"] else "guided"
    intents = {
        "implement": "implement_and_release",
        "plan": "plan_only",
        "verify": "verify_only",
    }
    try:
        intent = intents[spec["request_kind"]]
    except KeyError as exc:
        fail(f"unsupported request_kind: {exc.args[0]!r}")

    implementing = intent == "implement_and_release"
    deploy = implementing and not spec["explicit_no_deploy"]
    commit_push = implementing and not spec["explicit_no_commit"]
    preflight = (
        "full"
        if profile == "guided"
        else "delta_only"
        if spec["missing_prerequisites"]
        else "silent_ready"
    )

    if intent == "verify_only":
        evidence = "verification_report"
    elif not implementing:
        evidence = "none"
    elif not deploy:
        evidence = "blocked_by_explicit_constraint"
    else:
        evidence = {
            "web_app": "production_url",
            "ai_skill": "fresh_context_call",
            "automation": "live_run_id",
        }[spec["deliverable_kind"]]

    return {
        "profile": profile,
        "intent": intent,
        "preflight": preflight,
        "reporting": "adaptive_compact" if profile == "adaptive" else "guided_milestones",
        "use_existing_commands": profile == "adaptive",
        "create_repository": implementing and not spec["has_remote"],
        "commit_push": commit_push,
        "deploy_or_activate": deploy,
        "create_deploy_project": (
            deploy
            and spec["deliverable_kind"] == "web_app"
            and not spec["has_deploy_path"]
        ),
        "release_evidence": evidence,
    }


def validate_execution_profiles(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "guided-new-web-implement",
        "adaptive-existing-web-ready",
        "adaptive-existing-missing-tool",
        "adaptive-plan-only",
        "adaptive-verify-only",
        "guided-implement-explicit-no-deploy",
    }
    if set(fixtures) != expected_names:
        fail("execution profile fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve(fixture["input"])
        if actual != fixture["expected"]:
            fail(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: profile={actual['profile']} intent={actual['intent']} "
            f"preflight={actual['preflight']} deploy={actual['deploy_or_activate']}"
        )

    reference = PROFILE_REF.read_text(encoding="utf-8")
    for required in (
        "프로필은 `guided | adaptive` 두 개뿐이다",
        "프로필 선택 질문은 하지 않는다",
        "`구현해줘`는 로컬 파일을 수정하거나 build만 통과한 상태를 뜻하지 않는다",
        "기존 test·browser·CI가 요구사항을 검증할 수 있으면 새 MCP나 package를 제안하지 않는다",
        "정확한 파일만 담은 commit과 원격 push",
        "배포 또는 활성화 대상의 현재 상태 재확인",
    ):
        if required not in reference:
            fail(f"execution-profiles.md is missing behavior: {required}")
    if "guided | adaptive |" in reference:
        fail("execution profile list contains an unsupported third mode")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_execution_profiles()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
