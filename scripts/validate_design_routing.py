#!/usr/bin/env python3
"""Validate that optional design work is routed after final verification only."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "design-routing-expectations.json"


def route(spec: dict) -> str:
    if spec["intent"] != "design_improvement":
        return "ORANGE_START"
    if not spec["final_verification_passed"]:
        return "RETURN_TO_ORANGE_START"
    if spec["has_project_design_md"]:
        return "USE_PROJECT_DESIGN_MD"
    if spec["organization_homepage"]:
        return "EXTRACT_DESIGN_MD_DRAFT" if spec["extraction_approved"] else "REQUEST_EXTRACTION_CONSENT"
    return "USE_GETDESIGN_REFERENCE"


def stitch_mode(spec: dict) -> str:
    return "USE_STITCH_REFERENCE" if spec["stitch_requested"] else "SKIP_STITCH"


def recommendation_mode(spec: dict) -> str:
    if not spec["final_verification_passed"]:
        return "RETURN_TO_ORANGE_START"
    if spec["has_project_design_md"] and not spec["compare_new_direction"]:
        return "KEEP_APPROVED_SYSTEM"
    if not spec["catalog_links_verified"]:
        return "PROVIDE_CATALOG_SEARCH_LINK"
    return "PROPOSE_UP_TO_TWO_LINKED_OPTIONS"


def validate_design_routing(*, emit: bool = True) -> list[str]:
    fixtures = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if set(fixtures) != {"routing", "stitch", "recommendations"}:
        raise ValueError("design routing fixture groups changed unexpectedly")

    lines: list[str] = []
    for name, fixture in fixtures["routing"].items():
        actual = route(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS design route {name}: {actual}")

    for name, fixture in fixtures["stitch"].items():
        actual = stitch_mode(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS Stitch route {name}: {actual}")

    for name, fixture in fixtures["recommendations"].items():
        actual = recommendation_mode(fixture["input"])
        if actual != fixture["expected"]:
            raise ValueError(f"{name}: {actual} != {fixture['expected']}")
        lines.append(f"PASS recommendation {name}: {actual}")

    if emit:
        print("\n".join(lines))
    return lines


if __name__ == "__main__":
    try:
        validate_design_routing()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        sys.exit(1)
