#!/usr/bin/env python3
"""Validate Codex Sites-first routing without changing deliverable-kind routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "sites-routing-expectations.json"
REFERENCE = ROOT / "skills" / "orange-start" / "references" / "codex-sites.md"


def resolve_sites_route(spec: dict) -> dict[str, object]:
    if spec["kind"] != "web_app":
        return {"target": "n/a", "storage": "n/a", "human_gate": False}

    if spec["hosting_json"]:
        target = "codex_sites"
    elif spec["execution_profile"] == "adaptive" and spec["existing_deployment"]:
        target = "existing"
    else:
        sites_ready = (
            spec["host_surface"] == "codex_app"
            and spec["sites_available"]
            and spec["sites_compatible"]
            and (
                not spec["external_identity_provider"]
                or spec["sites_external_auth_confirmed"]
            )
        )
        target = "codex_sites" if sites_ready else "vercel_supabase"

    if target == "existing":
        storage = "existing"
    elif not spec["structured_data"] and not spec["uploads"]:
        storage = "none"
    elif target == "codex_sites":
        storage = "sites_d1_r2" if spec["uploads"] else "sites_d1"
    else:
        storage = "supabase"

    return {
        "target": target,
        "storage": storage,
        "human_gate": bool(spec.get("requires_sensitive_data_decision", False)),
    }


def validate_sites_routing(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    expected_names = {
        "new-codex-simple-site",
        "new-codex-d1-r2-site",
        "existing-sites-project",
        "existing-vercel-project",
        "codex-cli-without-sites-management",
        "claude-new-web-app",
        "external-google-auth-unconfirmed",
        "external-auth-confirmed-for-sites",
        "sites-policy-conflict",
        "non-web-deliverable",
    }
    if set(fixtures) != expected_names:
        raise ValueError("Sites routing fixture set changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures.items():
        actual = resolve_sites_route(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(
            f"PASS {name}: target={actual['target']} storage={actual['storage']} "
            f"human_gate={actual['human_gate']}"
        )

    reference = REFERENCE.read_text(encoding="utf-8")
    for required in (
        "web_delivery_target",
        "existing",
        "codex_sites",
        "vercel_supabase",
        "디자인 picker 없이",
        "D1",
        "R2",
        "Sites source repository가",
        "deployment status `succeeded`",
        "public beta",
    ):
        if required not in reference:
            raise ValueError(f"codex-sites.md is missing behavior: {required}")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_sites_routing()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
