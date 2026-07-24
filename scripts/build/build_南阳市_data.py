#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 南阳市 (Nanyang City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_南阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Wikipedia (zh.wikipedia.org) — leadership table for 南阳市
  - www.nanyang.gov.cn — 南阳市人民政府网站
  - https://zh.wikipedia.org/wiki/王智慧_(1968年) — 市委书记简历
  - https://zh.wikipedia.org/wiki/刘冰_(1979年) — 市长简历
  - https://zh.wikipedia.org/wiki/路红卫 — 前市长（被调查）
  - https://zh.wikipedia.org/wiki/朱是西 — 前市委书记（被双开）

Confidence notes:
  - 王智慧: confirmed via Wikipedia and government website
  - 刘冰: confirmed via Wikipedia (career timeline complete from 2016 onward)
  - 张生起 (人大主任), 张富治 (政协主席): confirmed via Wikipedia
  - Detailed career timelines before 2010 for 王智慧 could not be fully verified
  - 路红卫 is under disciplinary review (since 2026-06-16)
  - 朱是西 was expelled from the party (2025-04-27)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "南阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# In staging dir for now
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "王智慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年8月",
        "birthplace": "河南省商水县",
        "education": "大学学历（山东大学科社系科学社会主义专业），哲学硕士",
        "party_join": "中共党员",
        "work_start": "1990年",
        "current_post": "市委书记",
        "current_org": "中共南阳市委员会",
        "source": "https://zh.wikipedia.org/wiki/王智慧_(1968年)"
    },
    {
        "id": 2,
        "name": "刘冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "河南省新密市",
        "education": "管理学博士（中南大学在职），管理学学士（暨南大学）",
        "party_join": "中共党员",
        "work_start": "2001年6月",
        "current_post": "市长",
        "current_org": "南阳市人民政府",
        "source": "https://zh.wikipedia.org/wiki/刘冰_(1979年)"
    },
    {
        "id": 3,
        "name": "张生起",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年11月",
        "birthplace": "河南省社旗县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1984年",
        "current_post": "市人大常委会主任",
        "current_org": "南阳市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/张生起"
    },
    {
        "id": 4,
        "name": "张富治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年9月",
        "birthplace": "河南省上蔡县",
        "education": "党校研究生学历（河南省委党校行政管理专业），经济学硕士",
        "party_join": "中共党员",
        "work_start": "1983年7月",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议南阳市委员会",
        "source": "https://zh.wikipedia.org/wiki/张富治"
    },
    {
        "id": 5,
        "name": "路红卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "河南省巩义市",
        "education": "大学学历（郑州大学电子工程系电子学与信息系统专业）",
        "party_join": "中共党员",
        "work_start": "1991年",
        "current_post": "前市长（被调查）",
        "current_org": "南阳市人民政府（原）",
        "source": "https://zh.wikipedia.org/wiki/路红卫"
    },
    {
        "id": 6,
        "name": "朱是西",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年4月",
        "birthplace": "河南省禹州市",
        "education": "大学学历（河南中医学院中医专业），工商管理硕士（南洋理工大学）",
        "party_join": "中共党员",
        "work_start": "1990年10月",
        "current_post": "前市委书记（被双开）",
        "current_org": "中共南阳市委员会（原）",
        "source": "https://zh.wikipedia.org/wiki/朱是西"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共南阳市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "南阳市"},
    {"id": 2, "name": "南阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "南阳市"},
    {"id": 3, "name": "南阳市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "南阳市", "location": "南阳市"},
    {"id": 4, "name": "中国人民政治协商会议南阳市委员会", "type": "政协", "level": "地级市", "parent": "南阳市", "location": "南阳市"},
    {"id": 5, "name": "河南省委政策研究室", "type": "党委", "level": "省级", "parent": "中共河南省委", "location": "郑州市"},
    {"id": 6, "name": "中共焦作市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "焦作市"},
    {"id": 7, "name": "焦作市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "焦作市"},
    {"id": 8, "name": "中共濮阳市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "濮阳市"},
    {"id": 9, "name": "濮阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "濮阳市"},
    {"id": 10, "name": "中共南乐县委员会", "type": "党委", "level": "县级", "parent": "中共濮阳市委", "location": "濮阳市南乐县"},
    {"id": 11, "name": "南乐县人民政府", "type": "政府", "level": "县级", "parent": "濮阳市人民政府", "location": "濮阳市南乐县"},
    {"id": 12, "name": "中共驻马店市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "驻马店市"},
    {"id": 13, "name": "中共登封市委员会", "type": "党委", "level": "县级", "parent": "中共郑州市委", "location": "郑州市登封市"},
    {"id": 14, "name": "郑州市上街区人民政府", "type": "政府", "level": "县级", "parent": "郑州市人民政府", "location": "郑州市上街区"},
    {"id": 15, "name": "中共郑州市二七区委员会", "type": "党委", "level": "县级", "parent": "中共郑州市委", "location": "郑州市二七区"},
    {"id": 16, "name": "郑州市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "郑州市"},
    {"id": 17, "name": "中共河南省委组织部", "type": "党委", "level": "省级", "parent": "中共河南省委", "location": "郑州市"},
    {"id": 18, "name": "中共中牟县委员会", "type": "党委", "level": "县级", "parent": "中共郑州市委", "location": "郑州市中牟县"},
    {"id": 19, "name": "中牟县人民政府", "type": "政府", "level": "县级", "parent": "郑州市人民政府", "location": "郑州市中牟县"},
    {"id": 20, "name": "中共西峡县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市西峡县"},
    {"id": 21, "name": "西峡县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市西峡县"},
    {"id": 22, "name": "中共息县委员会", "type": "党委", "level": "县级", "parent": "中共信阳市委", "location": "信阳市息县"},
    {"id": 23, "name": "确山县人民政府", "type": "政府", "level": "县级", "parent": "驻马店市人民政府", "location": "驻马店市确山县"},
    {"id": 24, "name": "信阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "信阳市"},
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 王智慧
    {"person_id": 1, "org_id": 5, "title": "省委政策研究室干部", "start_date": "1990年", "end_date": "2011年8月", "rank": "", "note": "1990年山东大学毕业，进入河南省委政策研究室工作"},
    {"person_id": 1, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "2011年8月", "end_date": "2015年11月", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start_date": "2015年11月", "end_date": "2021年7月", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021年7月", "end_date": "2024年7月", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024年7月", "end_date": "至今", "rank": "正厅级", "note": "接替被调查的朱是西"},

    # 刘冰
    {"person_id": 2, "org_id": 11, "title": "县长", "start_date": "2016年4月", "end_date": "2018年11月", "rank": "正处级", "note": "南乐县"},
    {"person_id": 2, "org_id": 10, "title": "县委书记", "start_date": "2018年11月", "end_date": "2021年9月", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "市委常委、南乐县委书记", "start_date": "2021年9月", "end_date": "2022年8月", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "副市长", "start_date": "2022年8月", "end_date": "2023年5月", "rank": "副厅级", "note": "濮阳市"},
    {"person_id": 2, "org_id": 6, "title": "市委副书记、政法委书记", "start_date": "2023年5月", "end_date": "2024年1月", "rank": "副厅级", "note": "焦作市"},
    {"person_id": 2, "org_id": 7, "title": "代市长/市长", "start_date": "2024年1月", "end_date": "2026年6月", "rank": "正厅级", "note": "焦作市"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026年6月", "end_date": "至今", "rank": "正厅级", "note": "南阳市"},

    # 张生起
    {"person_id": 3, "org_id": 20, "title": "西峡县委书记", "start_date": "未知", "end_date": "2011年4月", "rank": "正处级", "note": "早期履历不详"},
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "2011年4月", "end_date": "2016年2月", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "2016年2月", "end_date": "2018年9月", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "市政协主席", "start_date": "2018年9月", "end_date": "2022年2月", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start_date": "2022年2月", "end_date": "至今", "rank": "正厅级", "note": ""},

    # 张富治
    {"person_id": 4, "org_id": 23, "title": "确山县县长", "start_date": "2004年4月", "end_date": "2006年5月", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 22, "title": "息县县委书记", "start_date": "2006年5月", "end_date": "2012年7月", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 24, "title": "副市长", "start_date": "2012年7月", "end_date": "2016年9月", "rank": "副厅级", "note": "信阳市"},
    {"person_id": 4, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "2016年9月", "end_date": "2022年2月", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start_date": "2022年2月", "end_date": "至今", "rank": "正厅级", "note": ""},

    # 路红卫
    {"person_id": 5, "org_id": 18, "title": "中牟县委书记", "start_date": "未知", "end_date": "2018年1月", "rank": "正处级", "note": "早期履历不详"},
    {"person_id": 5, "org_id": 6, "title": "市委常委、组织部部长", "start_date": "2018年1月", "end_date": "2022年6月", "rank": "副厅级", "note": "焦作市"},
    {"person_id": 5, "org_id": 7, "title": "常务副市长", "start_date": "2022年6月", "end_date": "2024年3月", "rank": "副厅级", "note": "焦作市"},
    {"person_id": 5, "org_id": 6, "title": "市委副书记", "start_date": "2024年3月", "end_date": "2024年7月", "rank": "副厅级", "note": "焦作市"},
    {"person_id": 5, "org_id": 2, "title": "市长", "start_date": "2024年7月", "end_date": "2026年6月", "rank": "正厅级", "note": "2026-06-16因严重违纪违法接受审查调查"},

    # 朱是西
    {"person_id": 6, "org_id": 13, "title": "登封市委副书记", "start_date": "2004年6月", "end_date": "2006年5月", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 14, "title": "上街区区长", "start_date": "2007年1月", "end_date": "2009年1月", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 15, "title": "二七区委书记", "start_date": "2009年3月", "end_date": "2011年12月", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 16, "title": "副市长", "start_date": "2011年12月", "end_date": "2012年9月", "rank": "副厅级", "note": "郑州市"},
    {"person_id": 6, "org_id": 17, "title": "省委组织部副部长", "start_date": "2012年9月", "end_date": "2018年1月", "rank": "副厅级", "note": "公开选拔"},
    {"person_id": 6, "org_id": 12, "title": "市长", "start_date": "2018年1月", "end_date": "2021年7月", "rank": "正厅级", "note": "驻马店市"},
    {"person_id": 6, "org_id": 1, "title": "市委书记", "start_date": "2021年7月", "end_date": "2024年5月", "rank": "正厅级", "note": "2024-05-14被查，2025-04-27被双开"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 王智慧 ↔ 朱是西（接任书记）
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor", "context": "王智慧接替被调查的朱是西任南阳市委书记", "overlap_org": "中共南阳市委员会", "overlap_period": "2021-2024（王智慧任市长期间与朱是西搭档担任市委书记）"},
    # 王智慧 ↔ 路红卫（交接市长）
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "王智慧升任市委书记后，路红卫接任市长", "overlap_org": "南阳市人民政府", "overlap_period": "2024年7月"},
    # 王智慧 ↔ 刘冰（新旧市长）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "王智慧为市委书记，刘冰为市长，为党政一把手搭档关系", "overlap_org": "中共南阳市委员会/南阳市人民政府", "overlap_period": "2026年6月至今"},
    # 刘冰 ↔ 路红卫（交接市长）
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "刘冰接替被调查的路红卫任南阳市长", "overlap_org": "南阳市人民政府", "overlap_period": "2026年6月"},
    # 张生起 ↔ 张富治（人大政协搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "张生起任人大主任、张富治任政协主席，均为正厅级，在南阳四套班子中搭档", "overlap_org": "南阳市", "overlap_period": "2022年2月至今"},
    # 路红卫 ↔ 刘冰（焦作前后任）
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor", "context": "路红卫曾任焦作市委副书记，刘冰曾任焦作市长，两人在焦作共事过", "overlap_org": "中共焦作市委员会/焦作市人民政府", "overlap_period": "2024年"},
    # 王智慧 ↔ 张生起（南阳班子搭档）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王智慧任市委书记期间张生起任人大主任", "overlap_org": "南阳市", "overlap_period": "2024年7月至今"},
    # 王智慧 ↔ 张富治（南阳班子搭档）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "王智慧任市长期间张富治任市委宣传部长，后任市委书记期间张富治任政协主席", "overlap_org": "南阳市", "overlap_period": "2016年至今"},
    # 朱是西 ↔ 张生起（南阳班子搭档）
    {"person_a": 6, "person_b": 3, "type": "overlap", "context": "朱是西任市委书记期间张生起任人大主任", "overlap_org": "南阳市", "overlap_period": "2022-2024"},
]


# ══════════════════════════════════════════════════════════════════════════
# Build logic
# ══════════════════════════════════════════════════════════════════════════

def build():
    # Use gov_relation runner if available, otherwise build directly
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import REPO_ROOT
        # Write to staging
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
    except ImportError:
        # Fallback: direct build
        _build_direct()

    print(f"\n✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")


def _build_direct():
    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    # Create tables
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    cols = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
            "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        values = [p.get(c, "") for c in cols]
        conn.execute(f"INSERT INTO persons ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})", values)

    # Insert organizations
    ocols = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        values = [o.get(c, "") for c in ocols]
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join('?' for _ in ocols)})", values)

    # Insert positions
    pcols = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        values = [pos.get(c, "") for c in pcols]
        conn.execute(f"INSERT INTO positions ({','.join(pcols)}) VALUES ({','.join('?' for _ in pcols)})", values)

    # Insert relationships
    rcols = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        values = [r.get(c, "") for c in rcols]
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join('?' for _ in rcols)})", values)

    conn.commit()
    conn.close()

    # ── Build GEXF ────────────────────────────────────────────────────
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        role = p.get("current_post", "")
        if "书记" in role:
            return "255,50,50"
        elif "市长" in role or "区长" in role or "县长" in role or "副市长" in role:
            return "50,100,255"
        elif "人大" in role or "主任" in role:
            return "100,150,255"
        elif "政协" in role:
            return "100,200,100"
        elif "纪委" in role or "监委" in role:
            return "255,165,0"
        else:
            return "100,100,100"

    def org_color(o):
        otype = o.get("type", "")
        if "党委" in otype:
            return "255,200,200"
        elif "政府" in otype:
            return "200,200,255"
        elif "人大" in otype:
            return "200,255,255"
        elif "政协" in otype:
            return "255,240,200"
        else:
            return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>南阳市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos.get("start_date", "")} — {pos.get("end_date", "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    build()
