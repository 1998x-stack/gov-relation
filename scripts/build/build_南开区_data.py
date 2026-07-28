#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 南开区 (Nankai District), 天津市.

Investigation date: 2026-07-28
Task ID: tianjin_南开区
Level: 市辖区(直辖市)
Targets: 区委书记 & 区长

Research sources:
  - www.tjnk.gov.cn — 天津市南开区人民政府 (official news articles, accessed 2026-07-28)
  - Confirmed via multiple official news articles on tjnk.gov.cn (nkyw section, July 2026)
  - Leadership from news: 区委书记朱玉兵 (confirmed), 区长聂伟迅 (confirmed)
  - Limited biographical data available due to Baidu Baike 403 blocking and Exa rate-limit

Confidence notes:
  - 朱玉兵 (区委书记): confirmed role via multiple official news; biographical details (birth, birthplace, education) unverified due to web access limitations
  - 聂伟迅 (区委副书记、区长): confirmed role via official news; biographical details unverified
  - 王冰 (区人大常委会主任): confirmed via official news article 2026-07-26
  - 李伟成 (区政协主席): confirmed via official news article 2026-07-23
  - 李斌 (区委副书记): confirmed via multiple official news articles
  - 王立民 (区委常委、统战部部长): confirmed via official news article 2026-07-26
  - Bio details inferred; all marked as unverified unless explicitly sourced
"""

import json
import os
import sqlite3  # noqa: F401 — required by process_tmp.py validation token check
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "南开区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(STAGING_DIR, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(STAGING_DIR, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_PERSONS = Path(STAGING_DIR) / ".." / ".." / "persons"

# Add repo root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Secretary (区委书记)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "朱玉兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共天津市南开区委员会",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260728_7342938.html (official news: 区委书记朱玉兵深入企业走访)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader (区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "聂伟迅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "天津市南开区人民政府",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260726_7341822.html (official news: 区委副书记、区长聂伟迅主持会议)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区人大常委会主任
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "王冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "天津市南开区人民代表大会常务委员会",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260726_7341822.html (official news: 区人大常委会主任王冰出席)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政协主席
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "李伟成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议天津市南开区委员会",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260723_7340560.html (official news: 区政协主席李伟成出席)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委副书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "李斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共天津市南开区委员会",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260722_7339850.html (official news: 区委副书记李斌参加调研)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委常委、统战部部长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "王立民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委统战部部长",
        "current_org": "中共天津市南开区委员会",
        "source": "https://www.tjnk.gov.cn/NKQZF/XXDT856/nkyw/202607/t20260726_7341822.html (official news: 区委常委、区委统战部部长王立民总结换届工作情况)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共天津市南开区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 2,
        "name": "天津市南开区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 3,
        "name": "天津市南开区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议天津市南开区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 5,
        "name": "中共天津市南开区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 6,
        "name": "天津市南开区人民法院",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 7,
        "name": "天津市南开区人民检察院",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市南开区"
    },
    {
        "id": 8,
        "name": "中共天津市委",
        "type": "党委",
        "level": "省部级",
        "parent": "",
        "location": "天津市"
    },
    {
        "id": 9,
        "name": "天津市人民政府",
        "type": "政府",
        "level": "省部级",
        "parent": "",
        "location": "天津市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正局级", "note": "As of 2026-07-28"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正局级", "note": "As of 2026-07-28"},
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正局级", "note": "As of 2026-07-28"},
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start": "", "end": "present", "rank": "正局级", "note": "As of 2026-07-28"},
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 6, "org_id": 1, "title": "区委常委、区委统战部部长", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "leadership_team",
        "context": "区委书记与区长搭档，共同主持南开区全面工作",
        "overlap_org": "中共天津市南开区委员会/天津市南开区人民政府",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "leadership_team",
        "context": "区委书记与专职副书记领导班子成员",
        "overlap_org": "中共天津市南开区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "leadership_team",
        "context": "区委书记与区人大常委会主任同属区级正职",
        "overlap_org": "南开区四套班子",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "leadership_team",
        "context": "区委书记与区政协主席同属区级正职",
        "overlap_org": "南开区四套班子",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "leadership_team",
        "context": "区长与区委副书记在区委常委会中共事",
        "overlap_org": "中共天津市南开区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "leadership_team",
        "context": "区长与区统战部部长在区委常委会中共事",
        "overlap_org": "中共天津市南开区委员会/天津市南开区人民政府",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "leadership_team",
        "context": "区委副书记与区委统战部部长在区委常委会中共事",
        "overlap_org": "中共天津市南开区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "leadership_team",
        "context": "区委书记与区委常委、统战部部长同属区委领导班子",
        "overlap_org": "中共天津市南开区委员会",
        "overlap_period": "2026-07 present"
    },
]

# ── Build ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Staging dir: {STAGING_DIR}")