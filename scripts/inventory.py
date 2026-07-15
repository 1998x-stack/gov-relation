#!/usr/bin/env python3
"""Print a read-only inventory of build scripts and generated artifacts."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.inventory import collect_inventory, format_inventory


def main() -> int:
    print(format_inventory(collect_inventory()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
