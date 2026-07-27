#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 阳泉市领导班子 (Yangquan City Leadership Network).
Investigation date: 2026-07-26

Current 阳泉市委书记: 鞠振 (Ju Zhen, since 2025.12)
Current 阳泉市市长: 陈凯 (Chen Kai, since 2025.12, acting)
"""

import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add repo root to path
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))
os.chdir(str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = _STAGING_DIR / "阳泉市_network.db"
GEXF_PATH = _STAGING_DIR / "阳泉市_network.gexf"

PERSONS_STAGING = _STAGING_DIR

# ═══════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════

# Sources:
# S001 - https://www.163.com/dy/article/KIDT0RRI0514CQIE.html (中国经济网, 2026-01-04)
# S002 - https://www.yq.gov.cn/ (阳泉市人民政府门户网站, official)
# S003 - https://en.wikipedia.org/wiki/Yangquan (Wikipedia)

persons = [
    # ── 鞠振 - 阳泉市委书记 (Party Secretary) ──
    {"id": 1, "name": "鞠振", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-04", "birthplace": "天津", "education": "大学学历，历史学硕士",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委书记", "current_org": "中共阳泉市委",
     "source": "S001"},

    # ── 陈凯 - 阳泉市市长 (Mayor) ──
    {"id": 2, "name": "陈凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "不详", "education": "研究生，哲学博士",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委副书记、市长", "current_org": "阳泉市人民政府",
     "source": "S001"},

    # ── 雷健坤 - 前市委书记 (2021-2025.12) ──
    {"id": 3, "name": "雷健坤", "gender": "女", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "不详", "education": "博士研究生，哲学博士",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "", "current_org": "（另有任用）",
     "source": "S001"},

    # ── 师旭明 - 市委副书记、政法委书记 ──
    {"id": 4, "name": "师旭明", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-08", "birthplace": "不详", "education": "中央党校研究生，文学学士",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委副书记、政法委书记", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 王琳玉 - 市人大常委会主任 ──
    {"id": 5, "name": "王琳玉", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "山西河津", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市人大常委会主任", "current_org": "阳泉市人大常委会",
     "source": "S003"},

    # ── 郭卫东 - 市政协主席 ──
    {"id": 6, "name": "郭卫东", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-05", "birthplace": "山西河津", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市政协主席", "current_org": "阳泉市政协",
     "source": "S003"},

    # ── 耿鹏鹏 - 市委常委 ──
    {"id": 7, "name": "耿鹏鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 王增昂 - 市委常委 ──
    {"id": 8, "name": "王增昂", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 李遊 - 市委常委 ──
    {"id": 9, "name": "李遊", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 郭晓东 - 市委常委 ──
    {"id": 10, "name": "郭晓东", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 石峥 - 市委常委 ──
    {"id": 11, "name": "石峥", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 陈明华 - 市委常委 ──
    {"id": 12, "name": "陈明华", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 王晓斌 - 市委常委 ──
    {"id": 13, "name": "王晓斌", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市委常委", "current_org": "中共阳泉市委",
     "source": "S002"},

    # ── 李君 - 副市长 ──
    {"id": 14, "name": "李君", "gender": "男", "ethnicity": "汉族",
     "birth": "不详", "birthplace": "不详", "education": "不详",
     "party_join": "中共党员", "work_start": "不详",
     "current_post": "阳泉市副市长", "current_org": "阳泉市人民政府",
     "source": "S002"},
]

organizations = [
    {"id": 1, "name": "中共阳泉市委", "type": "党委", "level": "地级市", "parent": "中共山西省委", "location": "山西省阳泉市"},
    {"id": 2, "name": "阳泉市人民政府", "type": "政府", "level": "地级市", "parent": "山西省人民政府", "location": "山西省阳泉市"},
    {"id": 3, "name": "阳泉市人大常委会", "type": "人大", "level": "地级市", "parent": "山西省人大常委会", "location": "山西省阳泉市"},
    {"id": 4, "name": "阳泉市政协", "type": "政协", "level": "地级市", "parent": "山西省政协", "location": "山西省阳泉市"},
]

positions = [
    # 鞠振
    {"person_id": 1, "org_id": 1, "title": "阳泉市委书记", "start": "2025-12", "end": "present", "rank": "正厅级", "note": "2025年12月31日省委宣布任命"},
    # 陈凯
    {"person_id": 2, "org_id": 2, "title": "阳泉市代市长", "start": "2025-12", "end": "present", "rank": "正厅级", "note": "2025年12月31日市十六届人大常委会第三十次会议任命为代市长"},
    # 雷健坤 (前书记)
    {"person_id": 3, "org_id": 1, "title": "阳泉市委书记（前任）", "start": "2021", "end": "2025-12", "rank": "正厅级", "note": "另有任用"},
    # 师旭明
    {"person_id": 4, "org_id": 1, "title": "阳泉市委副书记、政法委书记", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 王琳玉
    {"person_id": 5, "org_id": 3, "title": "阳泉市人大常委会主任", "start": "不详", "end": "present", "rank": "正厅级", "note": ""},
    # 郭卫东
    {"person_id": 6, "org_id": 4, "title": "阳泉市政协主席", "start": "不详", "end": "present", "rank": "正厅级", "note": ""},
    # 耿鹏鹏
    {"person_id": 7, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 王增昂
    {"person_id": 8, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 李遊
    {"person_id": 9, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 郭晓东
    {"person_id": 10, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 石峥
    {"person_id": 11, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 陈明华
    {"person_id": 12, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 王晓斌
    {"person_id": 13, "org_id": 1, "title": "阳泉市委常委", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
    # 李君
    {"person_id": 14, "org_id": 2, "title": "阳泉市副市长", "start": "不详", "end": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    # 鞠振 ← → 陈凯 (书记市长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政搭档", "overlap_org": "中共阳泉市委/阳泉市人民政府", "overlap_period": "2025-12至今"},
    # 鞠振 ← 雷健坤 (前任书记)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "鞠振接替雷健坤任阳泉市委书记", "overlap_org": "中共阳泉市委", "overlap_period": "2025-12交接"},
    # 师旭明 ← → 鞠振
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与副书记、政法委书记", "overlap_org": "中共阳泉市委", "overlap_period": "2025-12至今"},
    # 王琳玉 与 郭卫东 同乡 (河津)
    {"person_a": 5, "person_b": 6, "type": "same_native_place", "context": "同为山西河津人，同乡关系", "overlap_org": "", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════
# SOURCE REGISTER
# ═══════════════════════════════════════════════════════════

sources = {
    "S001": {
        "title": "鞠振任阳泉市委书记 陈凯任代市长",
        "url": "https://www.163.com/dy/article/KIDT0RRI0514CQIE.html",
        "publisher": "中国经济网",
        "published_at": "2026-01-04",
        "accessed_at": "2026-07-26",
        "source_type": "media",
        "reliability": "high",
    },
    "S002": {
        "title": "阳泉市人民政府门户网站",
        "url": "https://www.yq.gov.cn/",
        "publisher": "阳泉市人民政府",
        "published_at": "",
        "accessed_at": "2026-07-26",
        "source_type": "official",
        "reliability": "high",
    },
    "S003": {
        "title": "Wikipedia - Yangquan",
        "url": "https://en.wikipedia.org/wiki/Yangquan",
        "publisher": "Wikipedia",
        "published_at": "",
        "accessed_at": "2026-07-26",
        "source_type": "encyclopedia",
        "reliability": "medium",
    },
}

# ═══════════════════════════════════════════════════════════
# RUN BUILD
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Normalize data: add source_ids fields
    for i, p in enumerate(persons):
        if "source" in p:
            p["source_ids"] = p.pop("source")

    run_build(
        slug="阳泉市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDatabase: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Build complete.")
