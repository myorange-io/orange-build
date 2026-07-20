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
    design = (ROOT / "skills" / "orange-design" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    secure = (ROOT / "skills" / "orange-secure" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    require(
        start,
        (
            "마일스톤 저장",
            "`MEMORY.md`는 중요한 결정",
            "두 파일은 없을 때 최초 1회만",
            "기록은 예외만",
        ),
        "orange-start/SKILL.md",
    )
    require(
        verification,
        (
            "`PLAN.md`는 마일스톤에서 한 번 갱신",
            "`PLAN.md`를 매번 고치지 않는다",
            "원본 근거와 완료 조건 문장",
            "해당 코드·테스트와 같은 커밋",
        ),
        "verification-loop.md",
    )
    require(
        memory,
        (
            "## 기록 게이트",
            "`MEMORY.md`를 수정하지 않는다",
            "마일스톤당 최대 한 항목",
            "`PLAN.md`, 테스트 출력, git 이력",
            "기록 조건이 없으면 stage 목록에 `MEMORY.md`를 넣지 않는다",
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
            "새 프로젝트에 `MEMORY.md`가 없으면",
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
        ),
        "phase-preflight.md",
    )
    require(
        connect,
        (
            "추가 동의는 새 항목이나 더 넓은 scope",
            "없을 때 최초 1회만 만든다",
            "Orange Build boilerplate",
            "정상 설치와 `READY` 전환만 있었으면",
        ),
        "phase-connect.md",
    )
    require(
        build,
        (
            "작은 수정·재검증 중에는 `PLAN.md`를 건드리지 않는다",
            "원본 근거와 완료 조건은 사람의 범위 변경 결정 없이는 다시 쓰지 않는다",
            "평범한 구현 완료만으로는 파일을 수정하지 않는다",
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
        ("채택한 모든 시각 수정마다 `MEMORY.md`를 바꾸지 않는다",),
        "orange-design/SKILL.md",
    )
    require(
        secure,
        ("전부 OK이거나 이전과", "같은 결과면 파일을 수정하지 않는다"),
        "orange-secure/SKILL.md",
    )
    require(
        case_card,
        ("개발 중 매 작업마다 교육용 설명을 추가하는 대신",),
        "case-card.md",
    )

    message = (
        "PASS recording cadence: source=immutable plan=milestones "
        "memory=significant-only setup=one-time consent=reused"
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
