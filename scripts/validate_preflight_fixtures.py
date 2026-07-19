#!/usr/bin/env python3
"""Validate plan-derived prerequisite routing and preflight workflow invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_sites_routing import resolve_sites_route


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "prerequisite-expectations.json"
REFS = ROOT / "skills" / "orange-start" / "references"


def fail(message: str) -> None:
    raise ValueError(message)


def web_route(spec: dict) -> dict[str, object]:
    return resolve_sites_route(
        {
            "kind": spec["kind"],
            "execution_profile": spec.get("execution_profile", "guided"),
            "host_surface": spec.get(
                "host_surface",
                "codex_app" if spec.get("current_host") == "codex" else "claude",
            ),
            "sites_available": spec.get("sites_available", False),
            "sites_compatible": spec.get("sites_compatible", True),
            "hosting_json": spec.get("hosting_json", False),
            "existing_deployment": spec.get("existing_deployment", False),
            "external_identity_provider": spec.get("external_identity_provider", False),
            "sites_external_auth_confirmed": spec.get(
                "sites_external_auth_confirmed", False
            ),
            "structured_data": spec.get("storage") is not None,
            "uploads": spec.get("uploads", False),
            "requires_sensitive_data_decision": spec.get(
                "requires_sensitive_data_decision", False
            ),
        }
    )


def resolve(spec: dict) -> tuple[set[str], set[str], set[str]]:
    tools = {"git", "gh"}
    accounts = {"github"}
    browser: set[str] = set()

    kind = spec["kind"]
    runtime = spec.get("runtime")
    if kind == "web_app":
        tools.update({"node", "npm"})
        if web_route(spec)["target"] == "vercel_supabase":
            tools.add("vercel")
            accounts.add("vercel")
            browser.update({"vercel_signup_or_login", "github_app_repository_access"})
    elif runtime == "node":
        tools.update({"node", "npm"})
    elif runtime == "python":
        tools.add("python")

    if spec.get("storage") == "supabase" and web_route(spec)["target"] != "codex_sites":
        tools.add("supabase")
        accounts.add("supabase")
        browser.add("supabase_project_setup")

    if spec.get("google_oauth"):
        accounts.add("google")
        browser.update({"google_account_selection", "oauth_consent_and_redirect"})

    connectors = set(spec.get("connectors", []))
    if "gmail" in connectors:
        accounts.add("google")
        browser.update({"google_account_selection", "google_oauth"})
    if "slack" in connectors:
        accounts.add("slack")
        browser.add("slack_oauth")

    return tools, accounts, browser


def resolve_helpers(
    spec: dict,
) -> tuple[set[str], set[str], set[str], set[str], dict[str, str], set[str]]:
    """Resolve missing capabilities, not product-name matches."""
    desired: dict[str, str] = {}
    available = set(spec.get("available_capabilities", []))
    unsafe: set[str] = set()
    host = spec.get("current_host")
    if host not in {"codex", "claude"}:
        fail(f"unsupported current_host: {host!r}")

    for helper in spec.get("existing_helpers", []):
        capability = helper["capability"]
        scope_ok = helper.get("scope") == ("user" if host == "codex" else "local")
        flags = set(helper.get("flags", []))
        browser_flags_ok = True
        if capability == "browser_runtime_diagnostics":
            browser_flags_ok = {
                "--isolated",
                "--no-usage-statistics",
                "--no-performance-crux",
                "--redact-network-headers",
            }.issubset(flags) and not any(
                flag.startswith(("--autoConnect", "--browser-url")) for flag in flags
            )
        if helper.get("healthy") and scope_ok and browser_flags_ok:
            available.add(capability)
        else:
            unsafe.add(capability)

    if spec["kind"] == "web_app" and spec.get("browser_diagnostics"):
        desired["browser_runtime_diagnostics"] = "chrome-devtools-mcp"
    if spec["kind"] == "web_app" and spec.get("repeatable_e2e"):
        desired["repeatable_e2e"] = "playwright-test"
    if (
        spec["kind"] == "web_app"
        and spec.get("deployment_diagnostics")
        and web_route(spec)["target"] == "vercel_supabase"
    ):
        desired["deployment_observability"] = "vercel-mcp"
    waiting: set[str] = set()
    if (
        spec.get("storage") == "supabase"
        and web_route(spec)["target"] != "codex_sites"
        and spec.get("database_diagnostics")
    ):
        if "database_diagnostics" in available or spec.get("supabase_project_ref"):
            desired["database_diagnostics"] = "supabase-mcp-read-only"
        else:
            waiting.add("supabase-mcp-read-only")

    equivalents = set(desired).intersection(available)
    reconfigure = {
        tool
        for capability, tool in desired.items()
        if capability in unsafe and capability not in available
    }
    installs = {
        tool
        for capability, tool in desired.items()
        if capability not in available and capability not in unsafe
    }

    targets = {
        tool: (
            "project"
            if tool == "playwright-test"
            else "codex_user"
            if host == "codex"
            else "claude_local"
        )
        for tool in installs
    }

    features: set[str] = set()
    if (
        spec.get("storage") == "supabase"
        and web_route(spec)["target"] != "codex_sites"
        and spec.get("database_diagnostics")
    ):
        features = set(spec.get("supabase_features", []))
        allowed_features = {"database", "debugging", "docs"}
        if not features or not features.issubset(allowed_features):
            fail(f"invalid Supabase feature set: {sorted(features)}")

    return installs, equivalents, waiting, reconfigure, targets, features


def validate_preflight_fixtures(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if set(fixtures) != {
        "simple-web-app",
        "web-app-google-auth-storage",
        "web-app-supabase-project-ready",
        "web-app-e2e-deploy-diagnostics",
        "web-app-unsafe-existing-chrome",
        "pure-ai-skill",
        "gmail-slack-automation",
    }:
        fail("preflight fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        tools, accounts, browser = resolve(fixture["input"])
        helpers, equivalents, waiting, reconfigure, targets, features = resolve_helpers(
            fixture["input"]
        )
        expected_tools = set(fixture["expected_tools"])
        expected_accounts = set(fixture["expected_accounts"])
        expected_browser = set(fixture["expected_browser_setup"])
        expected_helpers = set(fixture["expected_helper_installs"])
        expected_equivalents = set(fixture["expected_helper_equivalents"])
        expected_waiting = set(fixture["expected_helper_waiting"])
        expected_reconfigure = set(fixture["expected_helper_reconfigure"])
        expected_targets = fixture["expected_helper_targets"]
        expected_features = set(fixture["expected_supabase_features"])
        if tools != expected_tools:
            fail(f"{name}: tools {sorted(tools)} != {sorted(expected_tools)}")
        if accounts != expected_accounts:
            fail(f"{name}: accounts {sorted(accounts)} != {sorted(expected_accounts)}")
        if browser != expected_browser:
            fail(f"{name}: browser {sorted(browser)} != {sorted(expected_browser)}")
        if helpers != expected_helpers:
            fail(f"{name}: helpers {sorted(helpers)} != {sorted(expected_helpers)}")
        if equivalents != expected_equivalents:
            fail(
                f"{name}: equivalents {sorted(equivalents)} "
                f"!= {sorted(expected_equivalents)}"
            )
        if waiting != expected_waiting:
            fail(f"{name}: waiting {sorted(waiting)} != {sorted(expected_waiting)}")
        if reconfigure != expected_reconfigure:
            fail(
                f"{name}: reconfigure {sorted(reconfigure)} "
                f"!= {sorted(expected_reconfigure)}"
            )
        if targets != expected_targets:
            fail(f"{name}: targets {targets} != {expected_targets}")
        if features != expected_features:
            fail(f"{name}: features {sorted(features)} != {sorted(expected_features)}")
        if tools.intersection(fixture["forbidden_tools"]):
            fail(f"{name}: unnecessary tool selected")
        if accounts.intersection(fixture["forbidden_accounts"]):
            fail(f"{name}: unnecessary account selected")
        if helpers.intersection(fixture["forbidden_helper_installs"]):
            fail(f"{name}: unnecessary helper selected")
        lines.append(
            f"PASS {name}: tools={len(tools)} accounts={len(accounts)} "
            f"browser={len(browser)} helpers={len(helpers)} equivalents={len(equivalents)} "
            f"waiting={len(waiting)} reconfigure={len(reconfigure)} "
            f"host={fixture['input']['current_host']}"
        )

    preflight = (REFS / "phase-preflight.md").read_text(encoding="utf-8")
    connect = (REFS / "phase-connect.md").read_text(encoding="utf-8")
    browser_steps = (REFS / "browser-steps.md").read_text(encoding="utf-8")
    helpful_tools = (REFS / "helpful-tools.md").read_text(encoding="utf-8")
    for required in (
        "시작 전 준비 카드",
        "설치 권한을 한 번 받기",
        "READY | MISSING | USER_ACTION | NOT_NEEDED",
        "https://github.com/signup",
        "https://chatgpt.com/sites",
        "https://vercel.com/signup",
        "https://supabase.com/dashboard/sign-up",
        "도움 도구 후보",
        "현재 호스트 하나",
        "web_delivery_target",
        "사전 준비 계획 확정",
        "INSTALL_APPROVED",
    ):
        if required not in preflight:
            fail(f"phase-preflight.md is missing behavior: {required}")
    for required in (
        "동의받지 않은 시스템·글로벌·프로젝트 설치를 실행하지 않는다",
        "brew install gh",
        "winget install --id GitHub.cli",
        "npm install -g supabase`는 쓰지 않는다",
        "python3 --version",
        "helpful-tools.md",
        ".openai/hosting.json",
        "현재 세션 실제 호출",
        "필요 없는 서비스는 설치·가입·연결하지 않았다",
        "모든 `REQUIRED` 준비 항목이 `READY`",
    ):
        if required not in connect:
            fail(f"phase-connect.md is missing behavior: {required}")
    for required in (
        "computer use",
        "Chrome 연동",
        "화면·브라우저 제어 권한",
        "CAPTCHA",
        "약관 동의",
        "현재 필요한 한 동작",
        "identity 검증부터 재개",
        "--no-usage-statistics",
        "--autoConnect",
    ):
        if required not in browser_steps:
            fail(f"browser-steps.md is missing behavior: {required}")
    for required in (
        "codex mcp list --json",
        "claude mcp list",
        "npm view chrome-devtools-mcp",
        "codex mcp add chrome-devtools",
        "claude mcp add --scope local chrome-devtools",
        "npm install -D @playwright/test@latest",
        "https://mcp.vercel.com/<team-slug>/<project-slug>",
        "project_ref=<project-ref>&read_only=true&features=<feature-list>",
        "EXISTING_UNSAFE",
        "이번 실행에서 새로 만든 entry만",
        "AI 스킬이나 Python 자동화에 선택적 npm MCP 하나를 쓰기 위해 Node.js를 새로 설치하지 않는다",
    ):
        if required not in helpful_tools:
            fail(f"helpful-tools.md is missing behavior: {required}")
    if "npx add-mcp" in helpful_tools:
        fail("helpful-tools.md must not configure every detected host at once")
    if "features=database,docs,debugging" in helpful_tools:
        fail("Supabase MCP features must be selected from the plan, not fixed broadly")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_preflight_fixtures()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
