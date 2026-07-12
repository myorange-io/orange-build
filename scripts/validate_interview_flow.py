#!/usr/bin/env python3
"""Validate the no-plan interview contract documented for orange-start."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "no-plan-interview.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "phase-interview.md"
START = ROOT / "skills" / "orange-start" / "SKILL.md"
PHASE_PLAN = ROOT / "skills" / "orange-start" / "references" / "phase-plan.md"


def fail(message: str) -> None:
    raise ValueError(message)


def section(text: str, start: str, end: str) -> str:
    start_at = text.find(start)
    if start_at < 0:
        fail(f"phase-interview.md is missing section: {start}")
    end_at = text.find(end, start_at + len(start))
    if end_at < 0:
        fail(f"phase-interview.md is missing section boundary: {end}")
    return text[start_at:end_at]


def source_plan_template(reference: str) -> str:
    source_section = section(reference, "## 6. SOURCE_PLAN.md 작성", "저장 뒤 `✅ 기획서 작성 완료")
    match = re.search(r"```markdown\n(?P<template>.*?)\n```", source_section, flags=re.DOTALL)
    if not match:
        fail("phase-interview.md is missing the SOURCE_PLAN.md markdown template")
    return match.group("template")


def validate_template_tests(template: str, expected: dict) -> None:
    headings = list(
        re.finditer(
            r"^### (?P<test_id>TEST-\d{2})\s+[—-]\s+.+$",
            template,
            flags=re.MULTILINE,
        )
    )
    ids = [heading.group("test_id") for heading in headings]
    if ids != expected["expected_ids"] or len(headings) != expected["expected_count"]:
        fail(f"SOURCE_PLAN.md template test ids {ids} != {expected['expected_ids']}")
    for heading in headings:
        tail = template[heading.end() :]
        next_heading = re.search(r"^#{1,6}\s+", tail, flags=re.MULTILINE)
        body = tail[: next_heading.start()] if next_heading is not None else tail
        for field in expected["required_fields"]:
            if len(re.findall(rf"^- {re.escape(field)}:\s*\S.*$", body, flags=re.MULTILINE)) != 1:
                fail(f"{heading.group('test_id')}: template must contain one '{field}' field")


def validate_interview_flow(*, emit: bool = True) -> str:
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    reference = REFERENCE.read_text(encoding="utf-8")
    start = START.read_text(encoding="utf-8")
    phase_plan = PHASE_PLAN.read_text(encoding="utf-8")

    if expected["max_guided_questions"] != 7:
        fail("fixture must preserve the Orange Build App seven-question limit")
    if "최대 기획 질문 수는 **7개**" not in reference:
        fail("phase-interview.md is missing the seven-question limit")
    if expected["initial_question"] not in reference:
        fail("phase-interview.md is missing the initial idea question")

    cursor = -1
    for phase_id in expected["phase_order"]:
        position = reference.find(f"`{phase_id}`", cursor + 1)
        if position < 0:
            fail(f"phase-interview.md is missing phase: {phase_id}")
        if position <= cursor:
            fail(f"phase order regressed at: {phase_id}")
        cursor = position
        question = expected["generic_questions"][phase_id]
        if question not in reference:
            fail(f"phase-interview.md is missing question for: {phase_id}")

    for kind in expected["deliverable_kinds"]:
        if f"### `{kind}`" not in reference:
            fail(f"phase-interview.md is missing deliverable kind: {kind}")

    verification = expected["verification_scenarios"]
    if verification["expected_count"] != 3:
        fail("the no-plan interview must derive exactly three verification scenarios")
    if verification["expected_ids"] != ["TEST-01", "TEST-02", "TEST-03"]:
        fail("verification scenario ids must be TEST-01 through TEST-03")
    if verification["required_fields"] != ["준비", "행동", "기대 결과", "통과 증거"]:
        fail("verification scenarios must preserve the current app four-field contract")
    if not verification["derive_from_answers_without_extra_question"]:
        fail("verification scenarios must be derived without another interview question")
    template = source_plan_template(reference)
    validate_template_tests(template, verification)
    if verification["derive_from_answers_without_extra_question"] and not re.search(
        r"(추가 질문 없이|사용자에게 묻지).{0,120}(3개|TEST-03)",
        reference,
        flags=re.DOTALL,
    ):
        fail("phase-interview.md must derive three tests without another question")

    suggestions = expected["idea_suggestions"]
    for key in (
        "only_when_user_has_no_idea_or_requests_suggestions",
        "show_one_at_a_time",
        "rotate_without_repeats",
        "exclude_sensitive_data",
    ):
        if not suggestions[key]:
            fail(f"idea suggestion fixture must keep {key}=true")
    if suggestions["counts_as_guided_question"]:
        fail("idea suggestions must not count toward the seven guided questions")
    distribution = suggestions["unknown_kind_distribution"]
    if suggestions["suggestion_pool_size"] != 6 or sum(distribution.values()) != 6:
        fail("idea suggestion fixture must preserve a six-item pool")
    if distribution != {"web_app": 2, "ai_skill": 2, "automation": 2}:
        fail("unknown-kind suggestions must be balanced two per deliverable kind")
    if not suggestions["known_kind_all_six_match"]:
        fail("known-kind suggestions must all match the selected deliverable kind")
    if suggestions["excluded_history_limit"] != 18:
        fail("idea suggestion exclusion history must retain the latest 18 ideas")
    if not suggestions["static_fallback"]:
        fail("idea suggestions must preserve the static fallback path")
    suggestion_section = section(reference, "### 아이디어 제안 모드", "## 2. 공통 질문 규칙")
    suggestion_contract = {
        "opt-in suggestions": "아이디어가 없다고 하거나 제안을 요청한 때만",
        "six distinct suggestions": "서로 다른 제안 6개",
        "balanced kinds": "세 유형에 2개씩",
        "selected kind": "6개 모두 그 유형에 맞춘다",
        "one at a time": "한 번에 하나씩",
        "no repeats": "중복 제안을 내지 않는다",
        "history limit": "최근 제안은 최대 18개",
        "sensitive-data exclusion": "민감 정보와 개인정보는 제안에서 제외한다",
        "not a guided question": "제안과 교체 요청은 기획 질문 수에 포함하지 않는다",
        "static fallback": "정적 폴백",
        "displayed suggestion state": "current_suggestion",
    }
    trigger_context = reference[: reference.find("### 아이디어 제안 모드")]
    for behavior, required in suggestion_contract.items():
        target = trigger_context if behavior == "opt-in suggestions" else suggestion_section
        if required not in target:
            fail(f"phase-interview.md is missing idea suggestion behavior: {behavior}")

    skip_all = expected["skip_all"]
    if not skip_all["generate_from_current_answers"]:
        fail("skip-all must generate from the answers already available")
    if not skip_all["record_unknowns_as_assumptions"]:
        fail("skip-all must record unknown details as assumptions")
    if skip_all["fabricate_missing_answers"]:
        fail("skip-all must not fabricate missing answers")
    for phrase in skip_all["phrases"]:
        if phrase not in reference:
            fail(f"phase-interview.md is missing skip-all phrase: {phrase}")
    common_rules = section(reference, "## 2. 공통 질문 규칙", "## 3. 단계 순서와 기본 질문")
    skip_contract = (
        "더 묻지 않고 지금까지의 답으로 기획서를 만든다",
        "current_suggestion",
        "사실처럼 채우지 않는다",
        skip_all["persist_completion_marker"],
    )
    for required in skip_contract:
        if required not in common_rules:
            fail(f"phase-interview.md is missing skip-all behavior: {required}")
    if skip_all["accept_displayed_suggestion_if_no_user_idea"] and (
        "현재 제안을 초기 아이디어로 선택" not in suggestion_section
    ):
        fail("skip-all must accept the displayed suggestion when no user idea exists")
    if skip_all["phase_plan_must_not_reopen_questions"] and (
        "interview_completion: skip_all" not in phase_plan
        or "기획 확인\n질문을 다시 열지 않는다" not in phase_plan
    ):
        fail("phase-plan.md must not reopen planning questions after skip-all")
    for metadata_field in ("interview_completion: completed | skip_all", "initial_idea_source: user | suggestion"):
        if metadata_field not in template:
            fail(f"SOURCE_PLAN.md template is missing metadata: {metadata_field}")

    for required in (
        "한 번에 질문은 **하나만**",
        "직전 답을 한 문장으로 요약",
        "이미 확인한 내용을 표현만 바꿔 다시 묻지 않는다",
        "선택지 2~3개",
        "source: orange-start-interview",
        "SOURCE_PLAN.md",
        expected["expected_next_reference"],
        "가정은 최대 3개",
        "대표 트리거·비트리거",
        "dry-run, 중복 실행, 재시도, 로그",
        "로딩·빈 상태·오류·성공 상태",
    ):
        if required not in reference:
            fail(f"phase-interview.md is missing behavior: {required}")

    if "phase-interview.md" not in start or "phase-plan.md" not in start:
        fail("orange-start does not route no-plan interviews into phase-plan")

    message = (
        "PASS no-plan-interview.json: phases=7 tests=3 suggestions=6 "
        "suggestion_rotation=deduped skip_all=true source=SOURCE_PLAN.md next=phase-plan.md"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_interview_flow()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
