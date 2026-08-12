#!/usr/bin/env python3
"""Validate guided/adaptive routing and completion-level semantics."""

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
    intents = {"implement": "implement", "plan": "plan_only", "verify": "verify_only"}
    try:
        intent = intents[spec["request_kind"]]
    except KeyError as exc:
        fail(f"unsupported request_kind: {exc.args[0]!r}")
    level = spec["completion_level"]
    if level not in {"local", "shared", "real_work"}:
        fail(f"unsupported completion_level: {level!r}")

    implementing = intent == "implement"
    external_level = level in {"shared", "real_work"}
    deploy = implementing and external_level and not spec["explicit_no_deploy"]
    commit_push = implementing and external_level and not spec["explicit_no_commit"]

    if intent == "verify_only":
        evidence = "verification_report"
    elif not implementing:
        evidence = "none"
    elif external_level and spec["explicit_no_deploy"]:
        evidence = "blocked_by_explicit_constraint"
    else:
        evidence = {
            ("web_app", "local"): "local_core_flow",
            ("web_app", "shared"): "shared_production_url",
            ("web_app", "real_work"): "actual_work_result_and_recovery",
            ("ai_skill", "local"): "current_host_registration_and_fresh_task",
            ("ai_skill", "shared"): "isolated_install_and_fresh_task",
            ("ai_skill", "real_work"): "actual_work_output_and_fallback",
            ("automation", "local"): "dry_run_dedupe_retry_log",
            ("automation", "shared"): "shared_test_run_and_requery",
            ("automation", "real_work"): "actual_run_and_recovery",
        }[(spec["deliverable_kind"], level)]

    return {
        "profile": profile,
        "intent": intent,
        "completion_level": level,
        "preflight": "delta_only" if spec["missing_prerequisites"] else "silent_ready",
        "use_existing_commands": profile == "adaptive",
        "create_repository": implementing and external_level and not spec["has_remote"],
        "commit_push": commit_push,
        "deploy_or_activate": deploy,
        "create_deploy_project": (
            deploy
            and spec["deliverable_kind"] == "web_app"
            and not spec["has_deploy_path"]
        ),
        "release_evidence": evidence,
        "separate_external_confirmation": deploy,
    }


def validate_execution_profiles(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "guided-local-web",
        "adaptive-shared-web",
        "adaptive-real-automation",
        "guided-local-skill",
        "adaptive-plan-only",
        "guided-shared-no-deploy",
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
            f"level={actual['completion_level']} deploy={actual['deploy_or_activate']}"
        )

    reference = PROFILE_REF.read_text(encoding="utf-8")
    for required in (
        "프로필은 `guided | adaptive` 두 개뿐",
        "선택 질문을 하지 않는다",
        "`delivery_intent`",
        "`implement`",
        "`completion_level`은 `local | shared | real_work`",
        "현재 호스트 개인 스킬 경로 등록과 새 작업 대표 호출",
        "외부 변경 없는 dry-run",
        "실제 공유 URL",
        "실제 자료·계정·업무 대상을 사용하고 복구·되돌리기",
        "선택한 `completion_level`과 결과물 유형에 맞는 실제 결과",
        "`local`에는 원격 push나 production URL을 완료 조건으로 강요하지 않는다",
    ):
        if required not in reference:
            fail(f"execution-profiles.md is missing behavior: {required}")
    if "implement_and_release" in reference:
        fail("execution-profiles.md keeps the removed forced-release intent")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_execution_profiles()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
