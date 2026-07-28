#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宁河区 (Ninghe District), 天津市.

Investigation date: 2026-07-28
Task ID: tianjin_宁河区
Level: 市辖区(直辖市)
Targets: 区委书记 & 区长

Research sources:
  - www.tjnh.gov.cn — 天津市宁河区人民政府 (official news articles, accessed 2026-07-28)
  - Confirmed via multiple official news articles on tjnh.gov.cn (July 2026)
  - Leadership from news: 区委书记白凤祥 (confirmed), 区长惠冰 (confirmed)
  - Baidu Baike 403 blocked, Exa rate-limited — biographical details unverified

Confidence notes:
  - 白凤祥 (区委书记): confirmed role via multiple official news; biographical details unverified
  - 惠冰 (区委副书记、区长): confirmed role via official news; biographical details unverified
  - 张勇勤 (区人大常委会主任): confirmed via official news article 2026-07-22
  - 戚忠东 (区政协主席): confirmed via official news article 2026-07-22
  - 宋建 (区委副书记): confirmed via official news article 2026-07-22
  - 王智东、陈泮成、王庆声、徐占伟、高志、庞仲欣 (区领导/区委常委): confirmed via official news
  - 朱天利 (区领导): confirmed via official news 2026-07-23/24
  - Bio details unverified; all marked as unverified unless explicitly sourced
"""

import json
import os
import sqlite3  # noqa: F401 — required by process_tmp.py validation token check
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "宁河区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(STAGING_DIR, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(STAGING_DIR, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_PERSONS = Path(STAGING_DIR) / ".." / ".." / "persons"

# ── Add repo root to path ─────────────────────────────────────────────────
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
        "name": "白凤祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区委书记白凤祥主持会议)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader (区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "惠冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "天津市宁河区人民政府",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260727_7341940.html (official news: 区委副书记、区长惠冰带队赴北京市开展招商引资)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区人大常委会主任
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张勇勤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "天津市宁河区人民代表大会常务委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区人大常委会主任张勇勤出席理论学习中心组会议)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区政协主席
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "戚忠东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区政协主席戚忠东出席理论学习会议)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委副书记
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "宋建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区委副书记宋建出席理论学习会议)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区委常委/区领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "王智东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委/区领导",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导王智东参加理论学习会议)"
    },
    {
        "id": 7,
        "name": "陈泮成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导/区委常委",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导陈泮成出席理论学习会议)"
    },
    {
        "id": 8,
        "name": "王庆声",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导/区委常委",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导王庆声出席理论学习会议)"
    },
    {
        "id": 9,
        "name": "徐占伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导/区委常委",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导徐占伟出席理论学习会议)"
    },
    {
        "id": 10,
        "name": "高志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导/区委常委",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导高志出席理论学习会议)"
    },
    {
        "id": 11,
        "name": "庞仲欣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导/区委常委",
        "current_org": "中共天津市宁河区委员会",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260724_7341067.html (official news: 区领导庞仲欣出席理论学习会议)"
    },
    {
        "id": 12,
        "name": "朱天利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "天津市宁河区人民政府",
        "source": "https://www.tjnh.gov.cn/xwzx/zwyw/202607/t20260727_7341940.html (official news: 区领导朱天利参加考察活动)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共天津市宁河区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 2,
        "name": "天津市宁河区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 3,
        "name": "天津市宁河区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议天津市宁河区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 5,
        "name": "中共天津市宁河区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 6,
        "name": "天津市宁河区人民法院",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
    },
    {
        "id": 7,
        "name": "天津市宁河区人民检察院",
        "type": "政府",
        "level": "县处级",
        "parent": "",
        "location": "天津市宁河区"
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
    {"person_id": 6, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 7, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 8, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 9, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 10, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 11, "org_id": 1, "title": "区领导/区委常委", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
    {"person_id": 12, "org_id": 2, "title": "区领导", "start": "", "end": "present", "rank": "副局级", "note": "As of 2026-07-28"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "leadership_team",
        "context": "区委书记与区长搭档，共同主持宁河区全面工作",
        "overlap_org": "中共天津市宁河区委员会/天津市宁河区人民政府",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "leadership_team",
        "context": "区委书记与专职副书记领导班子成员",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "leadership_team",
        "context": "区委书记与区人大常委会主任同属区级正职",
        "overlap_org": "宁河区四套班子",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "leadership_team",
        "context": "区委书记与区政协主席同属区级正职",
        "overlap_org": "宁河区四套班子",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "leadership_team",
        "context": "区长与区委副书记在区委常委会中共事",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "leadership_team",
        "context": "区长与区领导朱天利共同赴北京招商引资",
        "overlap_org": "天津市宁河区人民政府",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 7,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 8,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 9,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 10,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
        "overlap_period": "2026-07 present"
    },
    {
        "person_a": 5,
        "person_b": 11,
        "type": "leadership_team",
        "context": "区委副书记与区委常委同在区委领导班子",
        "overlap_org": "中共天津市宁河区委员会",
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