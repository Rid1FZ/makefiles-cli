#!/usr/bin/env python3
"""
Manage the project's supported Python version matrix (single source of truth: pyproject.toml classifiers).
"""

from __future__ import annotations

import sys

if sys.version_info < (3, 11):
    raise SystemExit("error: this script needs Python 3.11+ to run (uses tomllib)")

import argparse
import json
import subprocess
from pathlib import Path
from typing import Protocol, cast

import tomllib

REPO_ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"
CLASSIFIER_PREFIX = "Programming Language :: Python :: "


def log(message: str) -> None:
    print(f"-> {message}", file=sys.stderr)


def supported_versions() -> list[str]:
    with PYPROJECT.open("rb") as f:
        data = tomllib.load(f)

    classifiers: list[str] = data["project"]["classifiers"]
    versions = [c.removeprefix(CLASSIFIER_PREFIX) for c in classifiers if c.startswith(f"{CLASSIFIER_PREFIX}3.")]

    return sorted(versions, key=lambda v: tuple(map(int, v.split("."))))


def cmd_versions(args: Args) -> None:
    versions = supported_versions()

    if args.latest:
        print(versions[-1])
    elif args.json:
        print(json.dumps(versions))
    else:
        print("\n".join(versions))


def cmd_run(args: Args) -> None:
    versions = supported_versions()
    failed: list[str] = []

    for version in versions:
        log(f"Python {version}")

        cmd = ["uv", "run", "--python", version]
        if not args.no_isolated:
            cmd.append("--isolated")
        cmd += ["pytest", *args.pytest_args]

        result = subprocess.run(cmd, cwd=REPO_ROOT)
        if result.returncode != 0:
            failed.append(version)

    if failed:
        raise SystemExit(f"error: tests failed on: {', '.join(failed)}")

    log(f"All {len(versions)} versions passed: {', '.join(versions)}")


class Args(Protocol):
    command: str
    json: bool
    latest: bool
    no_isolated: bool
    pytest_args: list[str]


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    versions_parser = subparsers.add_parser("versions", help="print the supported Python versions")
    group = versions_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--json",
        action="store_true",
        help="print as a JSON array (used by ci.yml)",
    )
    group.add_argument(
        "--latest",
        action="store_true",
        help="print only the newest supported version",
    )

    run_parser = subparsers.add_parser(
        "run",
        help="run pytest locally across every supported version",
    )
    run_parser.add_argument(
        "--no-isolated",
        action="store_true",
        help="reuse uv's normal environment instead of a fresh --isolated one per version",
    )
    run_parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="extra arguments passed through to pytest",
    )

    return cast(Args, cast(object, parser.parse_args()))


def main() -> None:
    args = parse_args()
    if args.command == "versions":
        cmd_versions(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()


# pyright: reportUnusedExpression=false, reportUnusedCallResult=false
