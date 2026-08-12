#!/usr/bin/env python3
"""Validate IA-boundary project records and one final memory block."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
START = ROOT / "skills" / "orange-start"
REFS = START / "references"


def fail(message: str) -> None:
    raise ValueError(message)


def require(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            fail(f"{document} is missing recording behavior: {snippet}")


def reject(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet in text:
            fail(f"{document} keeps conflicting recording behavior: {snippet}")


def validate_recording_cadence(*, emit: bool = True) -> str:
    start = (START / "SKILL.md").read_text(encoding="utf-8")
    ia = (REFS / "ia-collaboration.md").read_text(encoding="utf-8")
    verification = (REFS / "verification-loop.md").read_text(encoding="utf-8")
    memory = (REFS / "memory-log.md").read_text(encoding="utf-8")
    plan = (REFS / "phase-plan.md").read_text(encoding="utf-8")
    resume = (ROOT / "skills" / "orange-resume" / "SKILL.md").read_text(encoding="utf-8")
    design = (ROOT / "skills" / "orange-design" / "SKILL.md").read_text(encoding="utf-8")
    secure = (ROOT / "skills" / "orange-secure" / "SKILL.md").read_text(encoding="utf-8")

    require(
        plan,
        (
            "첫 승인 전 게이트",
            "승인 전에는",
            "프로젝트 파일 생성·수정",
            "동의하면 `SOURCE_PLAN.md`와 `PLAN.md`를 처음 저장",
            "`plan_only` 요청은 기획 파일 생성 자체를 사용자가 요청",
        ),
        "phase-plan.md",
    )
    require(
        ia,
        (
            "`PLAN.md`는 최초 계약, 단계 상태 전이, 중요한 사람 결정, 실제 blocker handoff, 최종 판정",
            "단계 안의 작은 수정·테스트마다 문서를 고치지 않는다",
            "AWAITING_APPROVAL → IN_PROGRESS → AWAITING_REVIEW → APPROVED",
        ),
        "ia-collaboration.md",
    )
    require(
        verification,
        (
            "`PLAN.md`는 IA 경계에서만 갱신",
            "평범한 commit이나 작은 수정 때문에 상태 문서를 수정하지 않는다",
            "원본 근거와 완료 조건 문장",
            "최종 검증에서 PASS·FAIL·미검증 상태를 확정",
        ),
        "verification-loop.md",
    )
    require(
        start,
        (
            "기본 관리 파일은 `SOURCE_PLAN.md`와 `PLAN.md`",
            "단계 상태 전이",
            "boilerplate를 자동 생성하거나 복제하지 않는다",
            "`MEMORY.md`의 최종 검증 marker 블록을 정확히 하나",
        ),
        "orange-start/SKILL.md",
    )
    require(
        memory,
        (
            "선택한 완료 수준의 구현 완료 증거",
            "marker 블록이 이미 하나 있으면 새 항목을 append하지 않고",
            "과정 기록은 사용자가 요청한 경우에만",
            "완료 게이트는 FAIL",
        ),
        "memory-log.md",
    )
    require(
        resume,
        (
            "단계 상태 전이, 중요한 사람 결정, 실제 blocker handoff, 최종 판정",
            "평범한 수정과 테스트마다 문서를 고치지 않는다",
            "append하지 않는다",
        ),
        "orange-resume/SKILL.md",
    )
    require(
        design,
        (
            "채택한 모든 시각 수정마다 `MEMORY.md`를 바꾸지 않는다",
            "기존 최종 검증 marker 블록을 한 번 갱신",
        ),
        "orange-design/SKILL.md",
    )
    require(
        secure,
        (
            "검증 marker 블록을 현재 결과로 한 번 갱신",
            "`최종 검증` 항목을 append해 중복시키지 않는다",
        ),
        "orange-secure/SKILL.md",
    )

    combined = "\n".join((start, ia, verification, memory, plan, resume))
    reject(
        combined,
        (
            "`PLAN.md`는 네 시점에만 갱신",
            "implement_and_release",
            "derived_compat",
            "## 진행 상황",
        ),
        "active IA recording workflow",
    )

    message = (
        "PASS IA recording cadence: preapproval=no-write plan=state-boundaries "
        "memory=selected-level-final-once reporting=meaningful-transitions"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_recording_cadence()
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
