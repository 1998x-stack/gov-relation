#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 清水河县 leadership network.

清水河县, 呼和浩特市, 内蒙古自治区
Research date: 2026-07-25
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

BASE = Path(__file__).resolve().parent
SLUG = "清水河县"
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence: confirmed = official source / appointment notice
#             plausible = credible media with partial corroboration
#             unverified = lead without enough evidence

persons = [
    # ════ Current Leaders ════
    {
        "id": 1,
        "name": "徐艳国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清水河县委书记",
        "current_org": "中国共产党清水河县委员会",
        "source": "https://www.163.com/dy/article/JQCN0KRG05563DJA.html",
    },
    # Note: Current 县长 identity could not be confirmed from available sources.
    # Based on typical county government structure, the 县长 serves as deputy party secretary
    # and heads the county government. Further research needed.
    # ── Leadership Team Members ──
    {
        "id": 2,
        "name": "李世宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清水河县委常委、县委办公室主任",
        "current_org": "中国共产党清水河县委员会",
        "source": "https://www.163.com/dy/article/JR9JH8AI05563DJA.html",
    },
    {
        "id": 3,
        "name": "赵建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清水河县委常委、副县长",
        "current_org": "清水河县人民政府",
        "source": "https://www.163.com/dy/article/JR9JH8AI05563DJA.html",
    },
    # ════ Predecessors ════
    {
        "id": 4,
        "name": "张科灵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "呼和浩特市人大常委会副主任",
        "current_org": "呼和浩特市人民代表大会常务委员会",
        "source": "https://www.163.com/dy/article/JQCN0KRG05563DJA.html",
    },
    {
        "id": 5,
        "name": "云霖琼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.163.com/v/video/VK0GUS9NO.html",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党清水河县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党呼和浩特市委员会",
        "location": "内蒙古自治区呼和浩特市清水河县",
    },
    {
        "id": 2,
        "name": "清水河县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "呼和浩特市人民政府",
        "location": "内蒙古自治区呼和浩特市清水河县",
    },
    {
        "id": 3,
        "name": "呼和浩特市人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "",
        "location": "内蒙古自治区呼和浩特市",
    },
    {
        "id": 4,
        "name": "呼和浩特市大数据管理局",
        "type": "政府",
        "level": "地厅级",
        "parent": "呼和浩特市人民政府",
        "location": "内蒙古自治区呼和浩特市",
    },
    {
        "id": 5,
        "name": "内蒙古和林格尔新区管理委员会",
        "type": "政府",
        "level": "地厅级",
        "parent": "",
        "location": "内蒙古自治区呼和浩特市和林格尔县",
    },
    {
        "id": 6,
        "name": "和林格尔县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "呼和浩特市人民政府",
        "location": "内蒙古自治区呼和浩特市和林格尔县",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 徐艳国 career timeline
    {"id": 1, "person_id": 1, "org_id": 5, "title": "和林格尔新区党工委委员、管委会副主任",
     "start": "2021-07", "end": "2023-08", "rank": "副厅级", "note": ""},
    {"id": 2, "person_id": 1, "org_id": 4, "title": "呼和浩特市大数据管理局党组书记",
     "start": "2023-08", "end": "2023-11", "rank": "正处级", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 4, "title": "呼和浩特市大数据管理局党组书记、局长",
     "start": "2023-11", "end": "2025-03", "rank": "正处级", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 1, "title": "清水河县委书记",
     "start": "2025-03", "end": "present", "rank": "正处级", "note": "徐艳国于2025年3月任县委书记"},

    # 李世宏 career
    {"id": 5, "person_id": 2, "org_id": 6, "title": "和林格尔县市场监督管理局党组成员、副局长",
     "start": "", "end": "", "rank": "", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 6, "title": "和林格尔县羊群沟乡党委副书记、乡长",
     "start": "", "end": "", "rank": "", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 6, "title": "和林格尔县羊群沟乡党委书记",
     "start": "", "end": "2025-03", "rank": "", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 1, "title": "清水河县委常委、县委办公室主任",
     "start": "2025-03", "end": "present", "rank": "副处级", "note": ""},

    # 赵建军
    {"id": 9, "person_id": 3, "org_id": 1, "title": "清水河县委常委、县委办公室主任",
     "start": "", "end": "2025-02", "rank": "副处级", "note": ""},
    {"id": 10, "person_id": 3, "org_id": 2, "title": "清水河县委常委、副县长",
     "start": "2025-02", "end": "present", "rank": "副处级", "note": ""},

    # 张科灵
    {"id": 11, "person_id": 4, "org_id": 1, "title": "清水河县委书记",
     "start": "", "end": "2025-01", "rank": "正处级", "note": "前任县委书记，2025年1月当选市人大常委会副主任"},
    {"id": 12, "person_id": 4, "org_id": 3, "title": "呼和浩特市人大常委会副主任",
     "start": "2025-01", "end": "present", "rank": "副厅级", "note": ""},

    # 云霖琼
    {"id": 13, "person_id": 5, "org_id": 1, "title": "清水河县委书记",
     "start": "", "end": "", "rank": "正处级", "note": "2021年1月以县委书记身份出席活动"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    {
        "id": 1,
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "徐艳国（县委书记）与李世宏（县委常委、办公室主任）在清水河县委班子中共事",
        "overlap_org": "中国共产党清水河县委员会",
        "overlap_period": "2025-03至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "id": 2,
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "徐艳国（县委书记）与赵建军（县委常委、副县长）在清水河县委班子中共事",
        "overlap_org": "中国共产党清水河县委员会",
        "overlap_period": "2025-03至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "id": 3,
        "person_a": 1, "person_b": 4,
        "type": "predecessor_successor",
        "context": "徐艳国接替张科灵担任清水河县委书记",
        "overlap_org": "中国共产党清水河县委员会",
        "overlap_period": "2025",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "person_a": 4, "person_b": 5,
        "type": "predecessor_successor",
        "context": "张科灵接替云霖琼担任清水河县委书记",
        "overlap_org": "中国共产党清水河县委员会",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "plausible",
    },
    {
        "id": 5,
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "李世宏长期在和林格尔县工作，徐艳国曾在和林格尔新区任职，两人有和林格尔地域交集",
        "overlap_org": "和林格尔县",
        "overlap_period": "",
        "strength": "medium",
        "confidence": "plausible",
    },
    {
        "id": 6,
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "李世宏与赵建军均在清水河县委班子任职",
        "overlap_org": "中国共产党清水河县委员会",
        "overlap_period": "2025-03至今",
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
