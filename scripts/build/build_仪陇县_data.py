#!/usr/bin/env python3
"""
仪陇县 (Yilong County, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
数据来源:
  - 仪陇县人民政府官网领导信息 (www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/)
  - 仪陇县新闻中心新闻报道 2026-07-17, 2026-07-01
  - 南充市人民政府网站

置信度说明:
  - 来自官网领导页的信息标为 confirmed
  - 来自新闻报道的信息标为 confirmed（有具体报道日期）
  - 履历早期信息难以从外网获取，标为 plausible 或 unverified
"""

import sqlite3
import os
import sys
from datetime import datetime

TODAY = "2026-07-26"
SLUG = "仪陇县"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "仪陇县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "仪陇县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "兰吉春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "严清权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 3. 县委专职副书记 ──
    {
        "id": 3,
        "name": "陈小琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 4. 县委常委、副县长 ──
    {
        "id": 4,
        "name": "李西蜀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 5. 县委常委 ──
    {
        "id": 5,
        "name": "苟小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 6. 县委常委 ──
    {
        "id": 6,
        "name": "李小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 7. 县委常委 ──
    {
        "id": 7,
        "name": "杨学勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 8. 县委常委 ──
    {
        "id": 8,
        "name": "卢河东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 9. 县委常委 ──
    {
        "id": 9,
        "name": "朱永明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共仪陇县委员会",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 10. 县委常委、副县长 ──
    {
        "id": 10,
        "name": "张杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 11. 县委常委、副县长 ──
    {
        "id": 11,
        "name": "李明达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 12. 县委常委、副县长 ──
    {
        "id": 12,
        "name": "高思",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 13. 副县长 ──
    {
        "id": 13,
        "name": "唐环宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 14. 副县长 ──
    {
        "id": 14,
        "name": "杨全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 15. 副县长 ──
    {
        "id": 15,
        "name": "熊挺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "仪陇县人民政府",
        "source": "https://www.yilong.gov.cn/zwgk/fdzdgknr/jgjj/ldxx/",
    },
    # ── 16. 县人大常委会主任 ──
    {
        "id": 16,
        "name": "李斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "仪陇县人大常委会",
        "source": "https://www.yilong.gov.cn/xwdt/ylyw/t_2348733.html",
    },
    # ── 17. 县政协主席 ──
    {
        "id": 17,
        "name": "蒲仕钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协仪陇县委员会",
        "source": "https://www.yilong.gov.cn/xwdt/tlyw/t_2348733.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共仪陇县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共南充市委员会",
        "location": "仪陇县",
    },
    {
        "id": 2,
        "name": "仪陇县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "南充市人民政府",
        "location": "仪陇县",
    },
    {
        "id": 3,
        "name": "仪陇县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "南充市人大常委会",
        "location": "仪陇县",
    },
    {
        "id": 4,
        "name": "政协仪陇县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协南充市委员会",
        "location": "仪陇县",
    },
    {
        "id": 5,
        "name": "中共仪陇县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共南充市纪律检查委员会",
        "location": "仪陇县",
    },
    {
        "id": 6,
        "name": "仪陇县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "南充市监察委员会",
        "location": "仪陇县",
    },
]

positions = [
    # 兰吉春
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正县级", "note": "2026-07 现任"},
    # 严清权
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正县级", "note": "2026-07 现任"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正县级", "note": "2026-07 现任"},
    # 陈小琴
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "present", "rank": "副县级", "note": "2026-07 现任"},
    # 李西蜀
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 苟小军
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李小平
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 杨学勇
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 卢河东
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 朱永明
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 张杰
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李明达
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 高思
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 唐环宇
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 杨全
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 熊挺
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 李斌
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    # 蒲仕钊
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

relationships = [
    # 兰吉春 - 严清权：党政一把手协作关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职协作", "overlap_org": "中共仪陇县委员会/仪陇县人民政府",
     "overlap_period": "2026-" },
    # 兰吉春 - 陈小琴：县委班子关系
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记领导关系", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    # 兰吉春 - 各县委常委：常委会领导关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    # 严清权 - 副县长：政府班子关系
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    # 县委常委交叉关系
    {"person_a": 4, "person_b": 10, "type": "overlap",
     "context": "同为县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 4, "person_b": 11, "type": "overlap",
     "context": "同为县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 4, "person_b": 12, "type": "overlap",
     "context": "同为县委常委、副县长", "overlap_org": "仪陇县人民政府",
     "overlap_period": "2026-" },
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 5, "person_b": 8, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    {"person_a": 5, "person_b": 9, "type": "overlap",
     "context": "同为县委常委", "overlap_org": "中共仪陇县委员会",
     "overlap_period": "2026-" },
    # 县人大与县委的关系
    {"person_a": 1, "person_b": 16, "type": "overlap",
     "context": "县委书记与县人大常委会主任", "overlap_org": "仪陇县",
     "overlap_period": "" },
    # 县政协与县委的关系
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "县委书记与县政协主席", "overlap_org": "仪陇县",
     "overlap_period": "" },
]

# ═══════════════════════════════════════════════════════════════════════
# SQLite
# ═══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    cur.execute("""
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
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
              p.get("birth",""), p.get("birthplace",""), p.get("education",""),
              p.get("party_join",""), p.get("work_start",""),
              p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o.get("location","")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")


# ═══════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "副书记" not in role:
        return "255,50,50"    # Red: Party secretary
    elif "县长" in role or "区长" in role or "市长" in role:
        return "50,100,255"   # Blue: Government head
    else:
        return "100,100,100"  # Grey: Other

def org_color(o):
    t = o.get("type", "")
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def person_node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_node_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    print("Done.")