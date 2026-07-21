#!/usr/bin/env python3
"""Validate milestone-based project records and one-time setup behavior."""

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
            fail(f"{document} is missing recording-cadence behavior: {snippet}")


def reject(text: str, snippets: tuple[str, ...], document: str) -> None:
    for snippet in snippets:
        if snippet in text:
            fail(f"{document} keeps noisy recording behavior: {snippet}")


def validate_recording_cadence(*, emit: bool = True) -> str:
    start = (START / "SKILL.md").read_text(encoding="utf-8")
    verification = (REFS / "verification-loop.md").read_text(encoding="utf-8")
    memory = (REFS / "memory-log.md").read_text(encoding="utf-8")
    plan = (REFS / "phase-plan.md").read_text(encoding="utf-8")
    preflight = (REFS / "phase-preflight.md").read_text(encoding="utf-8")
    connect = (REFS / "phase-connect.md").read_text(encoding="utf-8")
    build = (REFS / "phase-build.md").read_text(encoding="utf-8")
    sites = (REFS / "codex-sites.md").read_text(encoding="utf-8")
    case_card = (REFS / "case-card.md").read_text(encoding="utf-8")
    verify = (REFS / "phase-verify.md").read_text(encoding="utf-8")
    improvement = (REFS / "self-improvement-loop.md").read_text(encoding="utf-8")
    resume = (ROOT / "skills" / "orange-resume" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    design = (ROOT / "skills" / "orange-design" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    secure = (ROOT / "skills" / "orange-secure" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    require(
        start,
        (
            "기본 관리 파일은 최초 1회 만드는 `SOURCE_PLAN.md`와 간결한 `PLAN.md` 두",
            "실제 blocker로 중단하는 handoff, 최종 판정",
            "boilerplate를 자동 생성하거나",
            "구현이 최종 완료되면 `memory-log.md`에 따라 `MEMORY.md`를 생성",
            "완료 기록만 필수",
            "내부 단계 완료를 따로 보고하지 않는다",
        ),
        "orange-start/SKILL.md",
    )
    require(
        verification,
        (
            "`PLAN.md`는 네 시점에만 갱신",
            "첫 작동 결과나 평범한 commit 때문에 상태 문서를 수정하지 않는다",
            "원본 근거와 완료 조건 문장",
            "최종 검증에서 PASS·FAIL·미검증 상태를 확정",
            "문서를 갱신한 경우에만 해당 코드·테스트와 같은 커밋",
        ),
        "verification-loop.md",
    )
    require(
        memory,
        (
            "구현 완료 증거다",
            "## 1. 필수 최종 기록 게이트",
            "정확히 한 번 기록한다",
            "<!-- orange-build:final-verification -->",
            "marker 블록이 이미 하나 있으면 새 항목을 append하지 않고",
            "시작 marker와 종료 marker가 각각 정확히 한 개인지 확인",
            "구현 완료 후 `MEMORY.md`가 없거나 marker가 정확히 하나가 아니면 완료 게이트는 FAIL",
        ),
        "memory-log.md",
    )
    reject(
        memory,
        (
            "파일이 길어지는 건 정상",
            "각 단계 끝에 아래 골격",
            "길이를 인위적으로 줄이지 않는다",
        ),
        "memory-log.md",
    )
    require(
        plan,
        (
            "`SOURCE_PLAN.md`에 그대로 저장한다",
            "덮어쓰지 말고 같은 원본인지 비교한다",
            "간결한 상태판",
            "별도 절에 중복하지 않고",
            "`SOURCE_PLAN.md`와 `PLAN.md`만 만든다",
            "단순 재실행·REQ 매핑·정상 호환 판정",
        ),
        "phase-plan.md",
    )
    require(
        preflight,
        (
            "이미 `INSTALL_APPROVED` 또는",
            "기존 동의를 재사용하고 다시 묻지 않는다",
            "scope가 넓어진 차이만",
            "준비가 끝났으면 카드와 상태 문서 갱신을 생략",
            "**변경분 준비 카드**",
        ),
        "phase-preflight.md",
    )
    require(
        connect,
        (
            "추가 동의는 새 항목이나 더 넓은 scope",
            "boilerplate를 자동 생성하거나 덧붙이지 않는다",
            "`SOURCE_PLAN.md`, `PLAN.md`만",
            "별도 상태 커밋과 완료 보고를 만들지 않는다",
            "정상 설치·READY 전환·identity 확인은 `PLAN.md`나 `MEMORY.md`에 복제하지 않는다",
        ),
        "phase-connect.md",
    )
    require(
        build,
        (
            "수정·재검증과 슬라이스 배포 중에는 `PLAN.md`를 건드리지 않는다",
            "첫 결과만을 기록하기 위해 `PLAN.md`를 고치거나",
            "원본 근거와 완료 조건은",
            "중간 체크 상태 문서를 덧붙이지 않는다",
        ),
        "phase-build.md",
    )
    require(
        sites,
        (
            "기존 경로를 재사용하거나 정상적으로",
            "`codex_sites`를 선택한 것만으로 `MEMORY.md`를 수정하지 않는다",
        ),
        "codex-sites.md",
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
    require(
        case_card,
        ("개발 중 매 작업마다 교육용 설명을 추가하는 대신",),
        "case-card.md",
    )
    require(
        verify,
        (
            "`PLAN.md`의 `최종 판정`을 한 번 갱신",
            "생성해 최종 검증 marker 블록을 정확히 하나 기록",
            "요청 여부와 관계없이",
            "핵심 검증 최대 3개",
            "REQ와 TEST가 모두 PASS이고 P0/P1 없음",
        ),
        "phase-verify.md",
    )
    require(
        improvement,
        (
            "최종 판정 또는 실제 handoff 때만 한 번 갱신",
            "P0/P1을 고쳤거나 사용자가 요청한",
            "실제로 실행해 통과한 REQ·TEST와 대표 증거",
        ),
        "self-improvement-loop.md",
    )
    require(
        resume,
        (
            "`PLAN.md`가 중간 구현마다 갱신된다고 가정하지 않는다",
            "최종 검증 marker 수",
            "최종 검증 PASS, `MEMORY.md` 없음",
            "실제 blocker handoff나 최종 판정만",
        ),
        "orange-resume/SKILL.md",
    )

    reject(
        start,
        (
            "마일스톤 저장",
            "기획 완료, 준비 완료",
            "`MEMORY.md`와 `CASE.md`는 기본으로 만들지 않는다",
        ),
        "orange-start/SKILL.md",
    )
    reject(
        memory,
        (
            "프로젝트 루트의 `MEMORY.md`는 기본 산출물이 아니다",
            "사용자 요청이 없거나 쓸 사건이 없으면",
            "새 프로젝트라도 자동으로 만들지 않는다",
        ),
        "memory-log.md",
    )
    reject(
        plan,
        ("새 프로젝트에 `MEMORY.md`가 없으면", "## 진행 상황"),
        "phase-plan.md",
    )
    reject(
        preflight,
        ("`guided`는 아래 전체 준비 카드를 보여준다", "✅ 사전 준비 계획 확정"),
        "phase-preflight.md",
    )
    reject(
        connect,
        ("GitHub 저장소와 실행 환경을 확인했습니다", "git commit -m \"환경과 GitHub 저장소 준비\""),
        "phase-connect.md",
    )

    message = (
        "PASS low-noise workflow: source=immutable plan=contract-decision-handoff-final "
        "memory=mandatory-final-once reporting=outcomes-only verification=unchanged"
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
