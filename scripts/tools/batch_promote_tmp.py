#!/usr/bin/env python3
"""One-shot batch promoter for data/tmp -> canonical, reusing process_tmp logic.

Semantics:
  * only VALID actions promoted (same classification/validation as process_tmp)
  * destination missing                 -> copy (new)
  * destination exists + content equal  -> skip (no-op)
  * destination exists + content differs-> skip + log (preserve canonical; no silent overwrite)
  * invalid / unknown kind              -> skip + log
Prints a per-kind summary and a conflicts log for review. Nothing is deleted.
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
os.chdir(REPO)

sys.path.insert(0, str(REPO / ".agents" / "skills" / "china-gov-network" / "scripts"))
import process_tmp as pt  # noqa: E402

TMP = REPO / "data" / "tmp"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    dirs = sorted(d for d in TMP.iterdir() if d.is_dir())
    new_count = 0
    skip_identical = 0
    skip_invalid = 0
    skip_unknown = 0
    conflicts = 0
    conflict_log: list[str] = []
    new_rel: list[str] = []
    by_kind: dict[str, int] = {}

    for d in dirs:
        for action in pt.collect_actions(d):
            if not action.valid:
                skip_invalid += 1
                continue
            if action.kind == "unknown":
                skip_unknown += 1
                continue
            dst = action.destination
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(action.source, dst)
                new_count += 1
                by_kind[action.kind] = by_kind.get(action.kind, 0) + 1
                new_rel.append(str(action.source.relative_to(REPO)))
            elif sha256(action.source) == sha256(dst):
                skip_identical += 1
            else:
                conflicts += 1
                conflict_log.append(
                    f"{action.kind:12} {action.source.relative_to(REPO)} -> "
                    f"{dst.relative_to(REPO)}"
                )

    print(f"dirs processed          : {len(dirs)}")
    print(f"copied NEW              : {new_count}  {by_kind}")
    print(f"skip (identical)        : {skip_identical}")
    print(f"skip (invalid)          : {skip_invalid}")
    print(f"skip (unknown kind)     : {skip_unknown}")
    print(f"skip (conflict/differ)  : {conflicts}")
    print("\nCONFLICTS (canonical preserved, inspect/reapply manually):")
    for line in conflict_log[:80]:
        print("   ", line)
    Path("/tmp/promote_new_files.txt").write_text(
        "\n".join(new_rel), encoding="utf-8"
    )
    print(f"\nnew files list written: /tmp/promote_new_files.txt ({len(new_rel)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())