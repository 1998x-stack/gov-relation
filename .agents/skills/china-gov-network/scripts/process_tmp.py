#!/usr/bin/env python3
"""Validate and promote staged investigation artifacts from data/tmp."""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
TMP_ROOT = REPO_ROOT / "data" / "tmp"

DESTINATIONS = {
    "build_script": REPO_ROOT,
    "database": REPO_ROOT / "data" / "database",
    "graph": REPO_ROOT / "data" / "graph",
    "person_json": REPO_ROOT / "data" / "persons",
    "report": REPO_ROOT / "report",
    "log": REPO_ROOT / "logs" / "dispatch",
}


@dataclass
class Action:
    source: Path
    destination: Path
    kind: str
    valid: bool
    note: str = ""


def is_person_json(path: Path) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return isinstance(data, dict) and "identity" in data and "career_timeline" in data and "source_register" in data


def validate_sqlite(path: Path) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        finally:
            conn.close()
    except Exception as exc:
        return False, f"sqlite error: {exc}"
    required = {"persons", "organizations", "positions", "relationships"}
    missing = sorted(required - tables)
    if missing:
        return False, f"missing tables: {', '.join(missing)}"
    return True, "ok"


def classify(path: Path) -> tuple[str | None, str]:
    name = path.name
    suffix = path.suffix.lower()
    if name.startswith("build_") and name.endswith("_data.py"):
        return "build_script", "build script"
    if suffix == ".db":
        return "database", "sqlite database"
    if suffix == ".gexf":
        return "graph", "gexf graph"
    if suffix == ".json" and is_person_json(path):
        return "person_json", "person graph json"
    if suffix in {".md", ".html"}:
        return "report", "report"
    if suffix in {".log", ".txt"}:
        return "log", "log"
    return None, "unrecognized"


def validate_action(path: Path, kind: str) -> tuple[bool, str]:
    if kind == "build_script":
        text = path.read_text(encoding="utf-8")
        required = ["sqlite3", "DB_PATH", "GEXF_PATH"]
        missing = [token for token in required if token not in text]
        return (not missing, "ok" if not missing else f"missing tokens: {', '.join(missing)}")
    if kind == "database":
        return validate_sqlite(path)
    if kind == "graph":
        text = path.read_text(encoding="utf-8", errors="replace")
        ok = "<gexf" in text and "<nodes>" in text and "<edges>" in text
        return ok, "ok" if ok else "not a recognizable gexf"
    if kind == "person_json":
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return False, f"json error: {exc}"
        return True, "ok"
    return True, "ok"


def collect_actions(staging_dir: Path) -> list[Action]:
    actions: list[Action] = []
    for path in sorted(staging_dir.rglob("*")):
        if not path.is_file() or path.name == "manifest.json" or path.name.startswith("."):
            continue
        kind, note = classify(path)
        if kind is None:
            actions.append(Action(path, path, "unknown", False, note))
            continue
        valid, validation_note = validate_action(path, kind)
        destination = DESTINATIONS[kind] / path.name
        actions.append(Action(path, destination, kind, valid, validation_note))
    return actions


def promote(actions: list[Action], move: bool = False, overwrite: bool = False) -> None:
    for action in actions:
        if not action.valid:
            continue
        if action.destination.exists() and not overwrite:
            raise FileExistsError(f"destination exists: {action.destination}")
    for action in actions:
        if not action.valid:
            continue
        action.destination.parent.mkdir(parents=True, exist_ok=True)
        if move:
            shutil.move(str(action.source), str(action.destination))
        else:
            shutil.copy2(action.source, action.destination)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def print_plan(actions: list[Action]) -> None:
    for action in actions:
        status = "OK" if action.valid else "SKIP"
        target = "(no destination)" if action.kind == "unknown" else rel(action.destination)
        print(f"{status:4} {action.kind:12} {rel(action.source)} -> {target} [{action.note}]")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task_dir", help="staging directory under data/tmp, or any relative/absolute path")
    parser.add_argument("--apply", action="store_true", help="copy valid files to canonical destinations")
    parser.add_argument("--move", action="store_true", help="move files instead of copying; implies --apply")
    parser.add_argument("--overwrite", action="store_true", help="allow replacing existing destination files")
    parser.add_argument("--allow-partial", action="store_true", help="promote valid files even when invalid files are present")
    parser.add_argument("--allow-external", action="store_true", help="allow staging directories outside data/tmp")
    args = parser.parse_args()

    staging_dir = Path(args.task_dir)
    if not staging_dir.is_absolute():
        if len(staging_dir.parts) == 1 and staging_dir.parts[0] not in {".", ".."}:
            candidate = TMP_ROOT / staging_dir
            staging_dir = candidate if candidate.exists() else REPO_ROOT / staging_dir
        else:
            staging_dir = REPO_ROOT / staging_dir
    staging_dir = staging_dir.resolve()
    if not staging_dir.exists() or not staging_dir.is_dir():
        print(f"staging directory not found: {staging_dir}", file=sys.stderr)
        return 1
    if not args.allow_external:
        try:
            staging_dir.relative_to(TMP_ROOT.resolve())
        except ValueError:
            print(f"refusing to process outside data/tmp without --allow-external: {staging_dir}", file=sys.stderr)
            return 1

    actions = collect_actions(staging_dir)
    print_plan(actions)
    invalid = [action for action in actions if not action.valid]
    if invalid:
        print(f"\n{len(invalid)} file(s) skipped or invalid; fix them before applying if they are required.")

    if args.apply or args.move:
        if invalid and not args.allow_partial:
            print("\nRefusing to apply because invalid files are present. Fix them or pass --allow-partial.", file=sys.stderr)
            return 1
        promote(actions, move=args.move, overwrite=args.overwrite)
        print("\nApplied valid staged artifacts.")
        if args.move:
            for a in (a for a in actions if a.valid):
                if not a.source.exists():
                    parent = a.source.parent
                    while parent != staging_dir:
                        if parent.exists() and not any(parent.iterdir()):
                            parent.rmdir()
                            parent = parent.parent
                        else:
                            break
            print(f"Cleaned up promoted files in: {staging_dir}")
    else:
        print("\nDry run only. Re-run with --apply to copy valid artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
