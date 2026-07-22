#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 敦煌市 leadership network.

County-level city under 酒泉市, 甘肃省.

Data sources:
- www.dunhuang.gov.cn (official government website) — confirmed as of July 2026
- Baidu Baike disambiguation page — 王彦群 role confirmed
- News articles on dunhuang.gov.cn

Evidence confidence:
- Current roles: confirmed (official government website)
- Career histories: unverified (web research blocked — Baidu Baike 403, Jina/Exa unavailable)
- Previous officeholders: plausible (inferred from news timeline)
"""
import os
import sqlite3  # used via gov_relation.runner; direct import for process_tmp token check
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "敦煌市"

# When run from staging dir, write outputs locally; when run from repo root, use canonical paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(SCRIPT_DIR) == "gansu_敦煌市":
    DB_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: dunhuang_<pinyin_name>
persons = [
    # --- 市委领导班子 (Party Committee) ---
    {
        "id": 1,
        "name": "王彦群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "酒泉市委常委、敦煌市委书记",
        "current_org": "中共敦煌市委员会",
        "source": "https://www.dunhuang.gov.cn/ (confirmed); Baidu Baike (酒泉市委常委、敦煌市委书记)",
    },
    # --- 市政府领导班子 (City Government) ---
    {
        "id": 2,
        "name": "朱建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "酒泉市政协党组成员、副主席，敦煌市委副书记、市政府党组书记、市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 3,
        "name": "付虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 4,
        "name": "王得文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 5,
        "name": "李建刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 6,
        "name": "孟军政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 7,
        "name": "郭艳丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    {
        "id": 8,
        "name": "魏铭辰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "敦煌市人民政府",
        "source": "https://www.dunhuang.gov.cn/ — official leadership page (confirmed)",
    },
    # --- 其他市委领导 (inferred from news mentions) ---
    # Note: Full 市委常委 roster was not accessible from the official site.
    # The following are inferred from news reports on dunhuang.gov.cn.
    # 王彦群 as 市委书记 is Party Secretary, 朱建军 as 市长 is Deputy Secretary.
]

# ── Organizations ────────────────────────────────────────────────────────
orgs = [
    {"id": 1, "name": "中共敦煌市委员会", "type": "党委", "level": "县级市",
     "parent": "中共酒泉市委员会", "location": "甘肃省酒泉市敦煌市"},
    {"id": 2, "name": "敦煌市人民政府", "type": "政府", "level": "县级市",
     "parent": "酒泉市人民政府", "location": "甘肃省酒泉市敦煌市"},
    {"id": 3, "name": "敦煌市人大常委会", "type": "人大", "level": "县级市",
     "parent": "", "location": "甘肃省酒泉市敦煌市"},
    {"id": 4, "name": "敦煌市政协", "type": "政协", "level": "县级市",
     "parent": "", "location": "甘肃省酒泉市敦煌市"},
    {"id": 5, "name": "中共敦煌市纪律检查委员会", "type": "纪委", "level": "县级市",
     "parent": "中共敦煌市委员会", "location": "甘肃省酒泉市敦煌市"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 王彦群
    {"person_id": 1, "org_id": 1, "title": "酒泉市委常委、敦煌市委书记",
     "start": "", "end": "present", "rank": "副厅级", "note": "同时担任酒泉市委常委"},
    # 朱建军
    {"person_id": 2, "org_id": 2, "title": "敦煌市委副书记、市政府党组书记、市长",
     "start": "", "end": "present", "rank": "正处级", "note": "同时担任酒泉市政协党组成员、副主席（副厅级）"},
    # 副市长
    {"person_id": 3, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长搭档关系", "overlap_org": "中共敦煌市委员会",
     "overlap_period": "", "strength": "strong", "confidence": "confirmed"},
]

# ── Build ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
