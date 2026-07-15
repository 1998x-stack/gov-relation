#!/usr/bin/env python3
"""Build static JSON data for the docs/ frontend."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.web import write_static_site_data


def main() -> int:
    write_static_site_data()
    print("Wrote docs/assets/data/*.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

