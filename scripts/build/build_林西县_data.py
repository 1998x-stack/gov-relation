#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 林西县 leadership network.

林西县, 赤峰市, 内蒙古自治区
Research date: 2026-07-25
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

BASE = Path(__file__).resolve().parent
SLUG = "林西县"
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"

AS_OF = "2026-07-25"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence: confirmed = official source / appointment notice
#             plausible = credible media with partial corroboration
#             unverified = lead without enough evidence

persons = [
    # ════ Current Leaders ════
    {
        "id": 1,
        "name": "张志刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林西县委书记",
        "current_org": "中国共产党林西县委员会",
        "source": "https://baike.baidu.com/item/林西县/7611533",
        "notes": "截至2025年7月，张志刚任林西县委书记（来源：林西县百度百科'政治'栏目）",
    },
    {
        "id": 2,
        "name": "迟亚玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林西县县长",
        "current_org": "林西县人民政府",
        "source": "https://baike.baidu.com/item/林西县/7611533",
        "notes": "截至2025年7月，迟亚玲任林西县县长（来源：林西县百度百科'政治'栏目）",
    },
    # ════ Predecessors (plausible) ════
    # Note: Predecessor information is unverified from current sources.
    # Further research needed to identify predessor/successor chains.
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党林西县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党赤峰市委员会",
        "location": "内蒙古自治区赤峰市林西县",
    },
    {
        "id": 2,
        "name": "林西县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "赤峰市人民政府",
        "location": "内蒙古自治区赤峰市林西县",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 张志刚
    {"id": 1, "person_id": 1, "org_id": 1, "title": "林西县委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "截至2025年7月任林西县委书记。详细任职起始时间待查。"},
    # 迟亚玲
    {"id": 2, "person_id": 2, "org_id": 2, "title": "林西县县长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "截至2025年7月任林西县县长。详细任职起始时间待查。"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "张志刚（县委书记）与迟亚玲（县长）在林西县党政班子中共事",
        "overlap_org": "林西县",
        "overlap_period": "截至2025年7月",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. DB:", DB_PATH)
    print("GEXF:", GEXF_PATH)
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
