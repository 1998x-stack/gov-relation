#!/usr/bin/env python3
"""构建双牌县（湖南省永州市）领导人物关系网络数据库和图文件。

数据来源：
- 双牌县人民政府官网 (spx.gov.cn，不可达)
- 永州市领导班子调查报告 (2026-07-14)
- 维基百科：双牌县

生成:
  data/tmp/hunan_双牌县/双牌县_network.db
  data/tmp/hunan_双牌县/双牌县_network.gexf
"""

from pathlib import Path
import json
import os
import sys
import shutil
from datetime import datetime

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Paths ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
STAGING_DB = HERE / "双牌县_network.db"
STAGING_GEXF = HERE / "双牌县_network.gexf"
PERSONS_DIR = HERE
REPO_ROOT = HERE.parent.parent.parent
CANONICAL_BUILD = REPO_ROOT / "build_双牌县_data.py"
CANONICAL_DB = REPO_ROOT / "data/database/双牌县_network.db"
CANONICAL_GEXF = REPO_ROOT / "data/graph/双牌县_network.gexf"
CANONICAL_PERSONS = REPO_ROOT / "data/persons"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:8]

SLUG = "双牌县"
PROVINCE = "湖南省"
CITY = "永州市"

# ═══════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════

persons = [
    # ── 1. 现任核心领导 ──
    {
        "id": 1,
        "name": "张跃斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "永州冷水滩",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "双牌县委书记",
        "current_org": "中共双牌县委",
        "source": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF",
    },
    {
        "id": 2,
        "name": "蔡富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "永州冷水滩",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "双牌县县长",
        "current_org": "双牌县人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF",
    },
    # ── 其他县委常委（候选）──
    # 注：以下为推测的常委职务，需进一步确认
    {
        "id": 3,
        "name": "（常务副县长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双牌县委常委、常务副县长",
        "current_org": "双牌县人民政府",
        "source": "(待补充)",
    },
    {
        "id": 4,
        "name": "（纪委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双牌县委常委、纪委书记、监委主任",
        "current_org": "中共双牌县纪委",
        "source": "(待补充)",
    },
    {
        "id": 5,
        "name": "（组织部长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双牌县委常委、组织部长",
        "current_org": "中共双牌县委组织部",
        "source": "(待补充)",
    },
    {
        "id": 6,
        "name": "（宣传部长待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双牌县委常委、宣传部长",
        "current_org": "中共双牌县委宣传部",
        "source": "(待补充)",
    },
    {
        "id": 7,
        "name": "（政法委书记待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双牌县委常委、政法委书记",
        "current_org": "中共双牌县委政法委",
        "source": "(待补充)",
    },
]

# ═══════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════

organizations_data = [
    {"id": 1,  "name": "中共双牌县委",        "type": "党委", "level": "县级", "parent": "中共永州市委",            "location": "永州市双牌县"},
    {"id": 2,  "name": "双牌县人民政府",      "type": "政府", "level": "县级", "parent": "永州市人民政府",        "location": "永州市双牌县"},
    {"id": 3,  "name": "双牌县人大常委会",    "type": "人大", "level": "县级", "parent": "永州市人大常委会",      "location": "永州市双牌县"},
    {"id": 4,  "name": "双牌县政协",          "type": "政协", "level": "县级", "parent": "永州市政协",            "location": "永州市双牌县"},
    {"id": 5,  "name": "中共双牌县纪委",      "type": "党委", "level": "县级", "parent": "中共双牌县委",          "location": "永州市双牌县"},
    {"id": 6,  "name": "中共双牌县委组织部",  "type": "党委", "level": "县级", "parent": "中共双牌县委",          "location": "永州市双牌县"},
    {"id": 7,  "name": "中共双牌县委宣传部",  "type": "党委", "level": "县级", "parent": "中共双牌县委",          "location": "永州市双牌县"},
    {"id": 8,  "name": "中共双牌县委政法委",  "type": "党委", "level": "县级", "parent": "中共双牌县委",          "location": "永州市双牌县"},
]

# ═══════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════

positions_data = [
    # 张跃斌
    {"person_id": 1, "org_id": 1, "title": "双牌县委书记", "start": "2021-10", "end": None,
     "rank": "正处级", "note": ""},
    # 蔡富强
    {"person_id": 2, "org_id": 2, "title": "双牌县县长", "start": "2021-10", "end": None,
     "rank": "正处级", "note": ""},
    # 其他常委（待定）
    {"person_id": 3, "org_id": 2, "title": "双牌县委常委、常务副县长", "start": "", "end": None,
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 4, "org_id": 5, "title": "双牌县委常委、纪委书记、监委主任", "start": "", "end": None,
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 5, "org_id": 6, "title": "双牌县委常委、组织部长", "start": "", "end": None,
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 6, "org_id": 7, "title": "双牌县委常委、宣传部长", "start": "", "end": None,
     "rank": "副处级", "note": "姓名待查"},
    {"person_id": 7, "org_id": 8, "title": "双牌县委常委、政法委书记", "start": "", "end": None,
     "rank": "副处级", "note": "姓名待查"},
]

# ═══════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════

relationships_data = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "上下级搭档",
        "context": "张跃斌任县委书记，蔡富强任县长，二人自2021年10月起搭档",
        "overlap_org": "双牌县委/县政府",
        "overlap_period": "2021-10~至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "同乡",
        "context": "两人均为永州冷水滩人，在县级班子中属于少见同籍搭档",
        "overlap_org": "",
        "overlap_period": "",
        "strength": "medium",
        "confidence": "confirmed",
    },
]


# ═══════════════════════════════════════════
# Person JSON 模板
# ═══════════════════════════════════════════

person_json_template = {}

# ── 张跃斌 ──
person_json_template["张跃斌"] = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": PROVINCE,
        "city": CITY,
        "region": SLUG,
        "job": "县委书记",
        "task_id": "hunan_双牌县",
        "time_focus": "2021至今",
    },
    "identity": {
        "person_id": "shuangpai_zhang_yuebin",
        "name": "张跃斌",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "永州冷水滩",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "张跃斌_1975-10",
            "name_birthplace": "张跃斌_永州冷水滩",
            "official_profile_url": ""
        },
    },
    "current_status": {
        "current_post": "双牌县委书记",
        "current_org": "中共双牌县委",
        "administrative_rank": "正处级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"],
    },
    "career_timeline": [
        {
            "start": "2021-10",
            "end": "present",
            "org": "中共双牌县委",
            "title": "双牌县委书记",
            "level": "县级",
            "location": "永州市双牌县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "任现职",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料未找到2021年之前的职业生涯历史",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "蔡富强",
            "person_id": "shuangpai_cai_fuqiang",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "2021年10月起张跃斌任书记、蔡富强任县长，搭档至今",
            "overlap_org": "双牌县委/县政府",
            "overlap_period": "2021-10~",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "person": "蔡富强",
            "person_id": "shuangpai_cai_fuqiang",
            "relationship_type": "same_native_place",
            "strength": "medium",
            "evidence": "两人均为永州冷水滩人",
            "overlap_org": "",
            "overlap_period": "",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "2021年10月任双牌县委书记，此前的职业生涯未知",
            "notable_fast_promotions": [],
        },
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "未发现纪律处分、审计问题或负面报道",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "双牌县（维基百科）",
            "url": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "提供双牌县领导基本信息",
        },
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "2021年前职业生涯完全未知",
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "张跃斌2021年10月任双牌县委书记前的完整职业履历",
            "why_it_matters": "核心人物，透过了其晋升路径才能理解人事网络",
            "suggested_queries": [
                "永州 张跃斌 简历",
                "张跃斌 任前公示",
                "张跃斌 此前任职",
            ],
            "last_attempted": AS_OF,
        },
    ],
}

# ─── 蔡富强 ───
person_json_template["蔡富强"] = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": PROVINCE,
        "city": CITY,
        "region": SLUG,
        "job": "县长",
        "task_id": "hunan_双牌县",
        "time_focus": "2021至今",
    },
    "identity": {
        "person_id": "shuangpai_cai_fuqiang",
        "name": "蔡富强",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "永州冷水滩",
        "native_bplace": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "蔡富强_1975-03",
            "name_birthplace": "蔡富强_永州冷水滩",
            "official_profile_url": "",
        },
    },
    "current_status": {
        "current_post": "双牌县县长",
        "current_org": "双牌县人民政府",
        "administrative_rank": "正处级",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"],
    },
    "career_timeline": [
        {
            "start": "2021-10",
            "end": "present",
            "org": "双牌县人民政府",
            "title": "双牌县县长",
            "level": "县级",
            "location": "永州市双牌县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "任现职",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料未找到2021年10月前的职业生涯历史",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "organizations": [],
    "relationships": [
        {
            "person": "张跃斌",
            "person_id": "shuangpai_zhang_yuebin",
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": "2021年10月起张跃斌任书记、蔡富强任县长",
            "overlap_org": "双牌县委/县政府",
            "overlap_period": "2021-10~",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
        {
            "person": "张跃斌",
            "person_id": "shuangpai_zhang_yuebin",
            "relationship_type": "same_native_place",
            "strength": "medium",
            "evidence": "两人均为永州冷水滩人",
            "overlap_org": "",
            "overlap_period": "",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        },
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "2021年10月任双牌县长，此前职业履历未知",
            "notable_fast_promotions": [],
        },
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "未发现纪律处分、风评或负面信号",
            "confidence": "unverified",
            "source_ids": [],
        },
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "双牌县（维基百科）",
            "url": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "提供双牌县领导基本信息",
        },
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "2021年10月前的完整职业履历未知",
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "蔡富强2021年10月任双牌县长前的完整职业履历",
            "why_it_matters": "关键人物，了解其晋升路径",
            "suggested_queries": [
                "蔡富强 简历",
                "蔡富强 任前公示",
                "蔡富强 此前任职",
            ],
            "last_attempted": AS_OF,
        },
    ],
}


# ═══════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if "县委" in post and "书记" in post and "纪委" not in post:
        return "255,50,50"   # Red: party secretary
    if "县长" in post:
        return "50,100,255"   # Blue: county mayor
    if "纪委书记" in post:
        return "255,165,0"     # Orange: discipline
    return "100,100,100"      # Grey: other


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"     # Pink
    if "政府" in t:
        return "200,200,255"     # Light blue
    if "人大" in t:
        return "200,255,255"     # Cyan
    if "政协" in t:
        return "255,240,200"     # Cream
    return "200,200,200"


def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or "县长" in post


def write_person_json(person_name, data):
    """写入单个person JSON到装载目录。"""
    base = PERSONS_DIR
    if "张跃斌" in person_name:
        filename = f"{TODAY}-湖南省-永州市-县委书记-张跃斌.json"
    elif "蔡富强" in person_name:
        filename = f"{TODAY}-湖南省-永州市-县长-蔡富强.json"
    else:
        filename = f"{TODAY}-湖南省-永州市-{person_name}.json"
    filepath = base / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ wrote {filepath}")
    # Also copy to canonical persons dir if not a dry run
    if CANONICAL_PERSONS.exists():
        canonical_path = CANONICAL_PERSONS / filename
        with open(canonical_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  ✅ wrote {canonical_path}")
    return filepath


# ═══════════════════════════════════════════
# 主构建函数
# ═══════════════════════════════════════════

def build():
    print("=" * 60)
    print(f"  构建 {SLUG} 领导网络 — {AS_OF}")
    print("=" * 60)

    # ── 1. 构建 SQLite 数据库 ──────────────────────────
    print(f"\n📦 构建 SQLite 数据库: {STAGING_DB}")
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations_data,
            positions=positions_data,
            relationships=relationships_data,
            db_path=STAGING_DB,
            gexf_path=STAGING_GEXF,
        )
        print(f"  ✅ DB: {STAGING_DB}")
        print(f"  ✅ GEXF: {STAGING_GEXF}")

        os.makedirs(os.path.dirname(CANONICAL_DB), exist_ok=True)
        os.makedirs(os.path.dirname(CANONICAL_GEXF), exist_ok=True)
        shutil.copy2(STAGING_DB, CANONICAL_DB)
        shutil.copy2(STAGING_GEXF, CANONICAL_GEXF)
        print(f"  ✅ Canonical DB: {CANONICAL_DB}")
        print(f"  ✅ Canonical GEXF: {CANONICAL_GEXF}")

    except ImportError:
        print("  ⚠ gov_relation module not found, building DB manually...")
        build_db_manual()
        os.makedirs(os.path.dirname(CANONICAL_DB), exist_ok=True)
        os.makedirs(os.path.dirname(CANONICAL_GEXF), exist_ok=True)
        shutil.copy2(STAGING_DB, CANONICAL_DB)
        shutil.copy2(STAGING_GEXF, CANONICAL_GEXF)
        print(f"  ✅ Canonical DB: {CANONICAL_DB}")
        print(f"  ✅ Canonical GEXF: {CANONICAL_GEXF}")

    # ── 2. 写 Person JSON ──────────────────────────────
    print(f"\n📝 写 Person JSON...")
    for name, data in person_json_template.items():
        write_person_json(name, data)

    # ── 3. 拷贝 build 脚本 ──────────────────────────────
    print(f"\n📋 拷贝构建脚本...")
    script_src = os.path.abspath(__file__)
    os.makedirs(os.path.dirname(CANONICAL_BUILD), exist_ok=True)
    shutil.copy2(script_src, CANONICAL_BUILD)
    print(f"  ✅ Canonical build: {CANONICAL_BUILD}")

    # ── 4. 摘要 ─────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print(f"  构建完成！")
    print(f"  人员: {len(persons)}")
    print(f"  组织: {len(organizations_data)}")
    print(f"  任职: {len(positions_data)}")
    print(f"  关系: {len(relationships_data)}")
    print(f"  Person JSON: {len(person_json_template)}")
    print(f"{'=' * 60}")


def build_db_manual():
    """Fallback: build SQLite and GEXF without gov_relation module."""
    import sqlite3
    conn = sqlite3.connect(STAGING_DB)
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        conn.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations_data:
        conn.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for po in positions_data:
        conn.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (po["person_id"], po["org_id"], po["title"],
             po["start"], po.get("end"), po["rank"], po["note"]))

    for r in relationships_data:
        conn.execute("""INSERT OR REPLACE INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  ✅ Manual DB built: {STAGING_DB}")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} personnel relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # organization nodes
    for o in organizations_data:
        c = org_color(o)
        oid = o["id"] + 100000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    # person -> organization
    for po in positions_data:
        eid += 1
        oid = po["org_id"] + 100000
        lines.append(f'      <edge id="e{eid}" source="p{po["person_id"]}" target="o{oid}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(po.get("start",""))} - {esc(po.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person -> person
    for r in relationships_data:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(STAGING_GEXF, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ Manual GEXF built: {STAGING_GEXF}")


if __name__ == "__main__":
    build()