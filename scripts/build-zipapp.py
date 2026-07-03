#!/usr/bin/env python3
"""
Build a standalone, single-file `mkfile` zipapp from this project.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipapp
from pathlib import Path
from typing import Protocol, cast

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_NAME = "makefiles"

BUILD_DIR = REPO_ROOT / "build"
DEFAULT_OUTPUT = BUILD_DIR / "zipapp" / "mkfile"

# https://docs.python.org/3/library/zipapp.html#creating-standalone-applications-with-zipapp
# recommends this exact form for the shebang: it works unmodified via the
# `py` launcher on Windows too, since the launcher parses shebang lines
# using the same `/usr/bin/env NAME` convention.
DEFAULT_INTERPRETER = "/usr/bin/env python3"

# Fixed timestamp for reproducible builds - same idea as yt-dlp's
# `touch -t 200001010101`, just a value comfortably inside the range the
# ZIP format's DOS-era date field supports (1980-2107).
REPRODUCIBLE_TIMESTAMP = time.mktime((2020, 1, 1, 0, 0, 0, 0, 0, -1))

# Installer bookkeeping left behind by `pip`/`uv install --target` that the
# running application never needs: console-script wrapper directories
# (POSIX and Windows names) and package metadata.
PRUNE_DIR_NAMES = ("bin", "Scripts")


def log(message: str) -> None:
    print(f"-> {message}", file=sys.stderr)


def find_installer(preference: str) -> list[str]:
    """Return the base command used to install the project + its deps."""
    if preference in ("auto", "uv"):
        uv = shutil.which("uv")
        if uv:
            return [uv, "pip", "install"]
        if preference == "uv":
            raise SystemExit("error: --installer=uv given but `uv` was not found on PATH")

        log("`uv` not found on PATH, falling back to pip")

    return [sys.executable, "-m", "pip", "install"]


def install_project(staging: Path, installer_cmd: list[str], verbose: bool) -> None:
    log(f"Installing project + dependencies into {staging}")

    cmd = [*installer_cmd, "--target", str(staging), str(REPO_ROOT)]
    if not verbose:
        cmd.append("-q")

    subprocess.run(cmd, check=True)


def prune_install_artifacts(staging: Path) -> None:
    for path in list(staging.iterdir()):
        is_metadata_dir = path.is_dir() and path.name.endswith(".dist-info")
        if path.name in PRUNE_DIR_NAMES or is_metadata_dir:
            log(f"Removing install artifact: {path.name}")

            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    for pycache in staging.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)


def install_entry_point(staging: Path) -> None:
    """
    zipapp requires __main__.py at the archive root. Rather than
    hand-maintain a near-duplicate of it, reuse the package's own
    `__main__.py` (added for `python -m makefiles` support), which the
    install step above already placed at staging/makefiles/__main__.py.
    """
    source = staging / PACKAGE_NAME / "__main__.py"
    if not source.is_file():
        raise SystemExit(
            f"error: {source} not found - expected the installed "
            + f"'{PACKAGE_NAME}' package to ship its own __main__.py"
        )
    log(f"Reusing {source.relative_to(staging)} as the archive entry point")
    shutil.copy2(source, staging / "__main__.py")


def normalize_timestamps(staging: Path) -> None:
    log("Normalizing file timestamps for a reproducible build")
    ts = REPRODUCIBLE_TIMESTAMP
    for path in staging.rglob("*"):
        os.utime(path, (ts, ts))


def build_archive(staging: Path, output: Path, interpreter: str | None, compressed: bool) -> None:
    log(f"Building archive: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()

    zipapp.create_archive(
        source=staging,
        target=output,
        interpreter=interpreter,
        compressed=compressed,
    )


def selftest(output: Path) -> None:
    log("Running self-test (--help)")

    result = subprocess.run(
        [sys.executable, str(output), "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"error: self-test failed (exit {result.returncode}):\n" + f"{result.stdout.decode(errors='replace')}"
        )


class Args(Protocol):
    """
    Typed stand-in for argparse's default Namespace.
    """

    output: Path
    interpreter: str
    installer: str
    compress: bool
    reproducible: bool
    selftest: bool
    verbose: bool


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output file (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})",
    )
    parser.add_argument(
        "--python",
        default=DEFAULT_INTERPRETER,
        dest="interpreter",
        help=f"shebang interpreter (default: {DEFAULT_INTERPRETER!r}); "
        + "pass an empty string to omit the shebang entirely",
    )
    parser.add_argument(
        "--installer",
        choices=("auto", "uv", "pip"),
        default="auto",
        help="tool used to install dependencies (default: auto, prefers uv)",
    )
    parser.add_argument(
        "--no-compress",
        dest="compress",
        action="store_false",
        help="disable zip compression",
    )
    parser.add_argument(
        "--no-reproducible",
        dest="reproducible",
        action="store_false",
        help="skip timestamp normalization",
    )
    parser.add_argument(
        "--skip-selftest",
        dest="selftest",
        action="store_false",
        help="skip running the built archive with --help to verify it works",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show installer output instead of running it quietly",
    )

    return cast(Args, cast(object, parser.parse_args()))


def main() -> None:
    args = parse_args()
    installer_cmd = find_installer(args.installer)

    with tempfile.TemporaryDirectory(prefix="mkfile-zipapp-") as tmp:
        staging = Path(tmp)

        install_project(staging, installer_cmd, args.verbose)

        prune_install_artifacts(staging)

        install_entry_point(staging)

        if args.reproducible:
            normalize_timestamps(staging)

        build_archive(staging, args.output.resolve(), args.interpreter or None, args.compress)

    if args.selftest:
        selftest(args.output)

    size_kib = args.output.stat().st_size / 1024
    log(f"Done: {args.output} ({size_kib:.1f} KiB)")


if __name__ == "__main__":
    main()


# pyright: reportUnusedExpression=false, reportUnusedCallResult=false
