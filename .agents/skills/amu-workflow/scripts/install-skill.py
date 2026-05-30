#!/usr/bin/env python3
"""Install the amu-workflow .ai scaffold into a target project."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


PROTECTED_FILES = {"MEMORY.md", "DECISIONS.md", "HANDOFF.md"}
PROTECTED_DIRS = {"requirements", "archive"}
COPY_DIRS = ("rules", "playbooks", "tmp", "artifacts")
ENSURE_DIRS = ("rules", "requirements", "playbooks", "archive", "tmp", "artifacts")


def copy_file_safe(source: Path, destination: Path, timestamp: str, protect_existing: bool) -> tuple[str, Path]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if protect_existing:
            return "skipped", destination
        backup = destination.with_name(f"{destination.name}.bak-{timestamp}")
        shutil.copy2(destination, backup)
        shutil.copy2(source, destination)
        return "backed_up", backup
    shutil.copy2(source, destination)
    return "copied", destination


def install(target_path: Path) -> dict[str, list[Path]]:
    skill_root = Path(__file__).resolve().parents[1]
    source_ai = skill_root / "assets" / "scaffold" / ".ai"
    target_root = target_path.resolve()
    target_ai = target_root / ".ai"
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    result: dict[str, list[Path]] = {"copied": [], "backed_up": [], "skipped": []}

    target_ai.mkdir(parents=True, exist_ok=True)
    for dir_name in ENSURE_DIRS:
        (target_ai / dir_name).mkdir(parents=True, exist_ok=True)

    for source in source_ai.iterdir():
        if not source.is_file():
            continue
        status, path = copy_file_safe(
            source,
            target_ai / source.name,
            timestamp,
            source.name in PROTECTED_FILES,
        )
        result[status].append(path)

    for dir_name in COPY_DIRS:
        source_dir = source_ai / dir_name
        for source in source_dir.iterdir():
            if not source.is_file():
                continue
            status, path = copy_file_safe(source, target_ai / dir_name / source.name, timestamp, False)
            result[status].append(path)

    for dir_name in PROTECTED_DIRS:
        source_dir = source_ai / dir_name
        for source in source_dir.iterdir():
            if not source.is_file():
                continue
            destination = target_ai / dir_name / source.name
            if destination.exists():
                result["skipped"].append(destination)
            else:
                shutil.copy2(source, destination)
                result["copied"].append(destination)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Install amu-workflow scaffold into a target project.")
    parser.add_argument("target_path", nargs="?", default=".", help="Target project path.")
    args = parser.parse_args()

    result = install(Path(args.target_path))
    print("amu-workflow scaffold installed.")
    for key in ("copied", "backed_up", "skipped"):
        print(f"{key.replace('_', ' ').title()}: {len(result[key])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
