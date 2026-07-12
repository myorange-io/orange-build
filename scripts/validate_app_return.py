#!/usr/bin/env python3
"""Validate the optional Orange Build App outcome and learning-record handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "app-return.json"
REFS = ROOT / "skills" / "orange-start" / "references"


def fail(message: str) -> None:
    raise ValueError(message)


def require(text: str, token: str, document: str) -> None:
    if token not in text:
        fail(f"{document} is missing app-return behavior: {token}")


def validate_app_return(*, emit: bool = True) -> str:
    expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
    verify = (REFS / "phase-verify.md").read_text(encoding="utf-8")
    browser = (REFS / "browser-steps.md").read_text(encoding="utf-8")
    memory = (REFS / "memory-log.md").read_text(encoding="utf-8")

    source_rule = f"`{expected['source_document']}` 메타데이터의 `source`가 정확히 `{expected['source_value']}`"
    require(verify, source_rule, "phase-verify.md")
    require(browser, source_rule, "browser-steps.md")
    require(memory, f"`{expected['source_document']}`의 `source`가 `{expected['source_value']}`", "memory-log.md")

    if expected["skip_non_app_sources"]:
        require(verify, "`source`가 `orange-build-app`이 아닌 모든 작업", "phase-verify.md")
        require(browser, "다른 출처의 작업에는 제안하지 않는다", "browser-steps.md")

    if expected["requires_user_opt_in_before_url_write"]:
        for document, text, url_token in (
            ("phase-verify.md", verify, "GitHub URL"),
            ("browser-steps.md", browser, "GitHub 저장소 URL"),
        ):
            opt_in = text.find("사용자가 원하면")
            url_write = text.find(url_token, opt_in + 1)
            if opt_in < 0 or url_write < 0 or opt_in > url_write:
                fail(f"{document} must ask for opt-in before writing outcome URLs")

    if expected["live_url_only_when_present"]:
        require(verify, "실제\n   운영 배포 URL이 있는 결과물만 라이브 URL도 채우며", "phase-verify.md")
        require(browser, "해당하는 경우 운영 배포 URL", "browser-steps.md")
        require(browser, "배포 URL이 없는 결과물에는 값을 꾸며 넣지 않는다", "browser-steps.md")

    if expected["never_guess_plan_url"]:
        require(verify, "URL을 기획서에서 추측하지 않는다", "phase-verify.md")
        require(browser, "주소를 추측하지 말고", "browser-steps.md")

    memory_contract = expected["memory"]
    if memory_contract["max_bytes"] != 256 * 1024:
        fail("app-return fixture must preserve the Orange Build App 256KB limit")
    require(browser, "256KB", "browser-steps.md")
    require(memory, "256KB", "memory-log.md")

    if memory_contract["requires_separate_explicit_consent"]:
        require(verify, "동의 전에는 파일 선택·업로드", "phase-verify.md")
        require(browser, "업로드 직전 명시적 프라이버시 동의", "browser-steps.md")
        require(memory, "명시적 프라이버시 동의", "memory-log.md")

    if memory_contract["participant_reflection_user_authored"]:
        require(verify, "참가자 회고는 사용자가 직접 쓴", "phase-verify.md")
        require(browser, "사용자가 자신의 말로 직접", "browser-steps.md")
        require(memory, "사용자가 자신의 말로", "memory-log.md")

    message = (
        "PASS app-return.json: source=SOURCE_PLAN.md opt_in_before_urls=true "
        "live_url=when_present memory_consent=separate reflection=user_authored"
    )
    if emit:
        print(message)
    return message


if __name__ == "__main__":
    try:
        validate_app_return()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
