#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Chicheng County leadership network.

Task: hebei_赤城县
Region: 赤城县, 河北省张家口市
Targets: 县委书记 & 县长
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# __file__ = data/tmp/hebei_赤城县/build_赤城县_data.py → BASE = repo root
sys.path.insert(0, BASE)

DB_PATH = os.path.join(BASE, "data/tmp/hebei_赤城县/赤城县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/hebei_赤城县/赤城县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "data/tmp/hebei_赤城县")

# ═══════════════════════════════════════════════════════════════════
# DATA — Hard-coded from official government website research
# ═══════════════════════════════════════════════════════════════════

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "邓艳杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-01", "birthplace": "", "education": "河北省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委书记", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79479.html"},

    # ── Current County Mayor ──
    {"id": 2, "name": "陈涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委副书记、县长", "current_org": "赤城县人民政府",
     "source": "http://www.ccx.gov.cn/single/22/79481.html"},

    # ── Deputy Party Secretary ──
    {"id": 3, "name": "戎海广", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委副书记", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    # ── Executive Deputy Mayor ──
    {"id": 4, "name": "王东升", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-08", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委、常务副县长", "current_org": "赤城县人民政府",
     "source": "http://www.ccx.gov.cn/single/21/19507.html"},

    # ── Discipline Inspection Secretary ──
    {"id": 5, "name": "杨治国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委、县纪委书记", "current_org": "中共赤城县纪律检查委员会",
     "source": "http://www.ccx.gov.cn/single/22/79477.html"},

    # ── Propaganda Minister ──
    {"id": 6, "name": "杨怿欣", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委、宣传部部长", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/31/78344.html"},

    # ── Predecessor: 前县委书记/县长 ──
    {"id": 7, "name": "赵红革", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-12", "birthplace": "河北张家口", "education": "大学（张家口大学财会专业）",
     "party_join": "中共党员", "work_start": "1987-07",
     "current_post": "张家口市人大常委会党组成员、秘书长、机关党组书记、一级调研员",
     "current_org": "张家口市人大常委会",
     "source": "https://baike.baidu.com/item/%E8%B5%B5%E7%BA%A2%E9%9D%A9/52277912"},

    # ── Previous Party Secretary/Mayor ──
    {"id": 8, "name": "薛宏霞", "gender": "女", "ethnicity": "满族",
     "birth": "1984-07", "birthplace": "河北承德围场", "education": "",
     "party_join": "2005-06", "work_start": "2007-08",
     "current_post": "康保县委书记", "current_org": "中共康保县委员会",
     "source": "https://baike.baidu.com/item/%E8%96%9B%E5%AE%8F%E9%9C%9E/57070217"},

    # ── Inferred Standing Committee members (from executive chair list) ──
    {"id": 9, "name": "靳卓伢", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县人大常委会党组书记", "current_org": "赤城县人大常委会",
     "source": "http://www.ccx.gov.cn/single/22/79586.html"},

    {"id": 10, "name": "王春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县政协主席（推断）", "current_org": "赤城县政协",
     "source": "http://www.ccx.gov.cn/single/22/79481.html"},

    {"id": 11, "name": "路太忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    {"id": 12, "name": "付利军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    {"id": 13, "name": "赵璞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    {"id": 14, "name": "王彦青", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    {"id": 15, "name": "孙志君", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    {"id": 16, "name": "李飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县委常委（推断）", "current_org": "中共赤城县委员会",
     "source": "http://www.ccx.gov.cn/single/22/79436.html"},

    # ── Person's Congress person ──
    {"id": 17, "name": "王新慧", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县人大常委会主任（推断）", "current_org": "赤城县人大常委会",
     "source": "http://www.ccx.gov.cn/single/22/79586.html"},

    # ── Cross-county figure ──
    {"id": 18, "name": "刘雪松", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "河北赤城", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "张家口市副市长", "current_org": "张家口市人民政府",
     "source": "张家口市人民政府网站"},

    # ── Former VP Mayor ──
    {"id": 19, "name": "张必然", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县人大常委会副主任（推断）", "current_org": "赤城县人大常委会",
     "source": "http://www.ccx.gov.cn/single/22/79586.html"},

    # ── Former 13th Congress leaders ──
    {"id": 20, "name": "王玉辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县十一届政协主席", "current_org": "赤城县政协",
     "source": "http://www.ccx.gov.cn/single/22/79481.html"},

    {"id": 21, "name": "薛建武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "赤城县政协副主席", "current_org": "赤城县政协",
     "source": "http://www.ccx.gov.cn/single/22/79481.html"},
]

organizations = [
    {"id": 1, "name": "中共赤城县委员会", "type": "党委", "level": "县级",
     "parent": "中共张家口市委员会", "location": "河北省张家口市赤城县"},
    {"id": 2, "name": "赤城县人民政府", "type": "政府", "level": "县级",
     "parent": "张家口市人民政府", "location": "河北省张家口市赤城县"},
    {"id": 3, "name": "赤城县人大常委会", "type": "人大", "level": "县级",
     "parent": "张家口市人大常委会", "location": "河北省张家口市赤城县"},
    {"id": 4, "name": "赤城县政协", "type": "政协", "level": "县级",
     "parent": "张家口市政协", "location": "河北省张家口市赤城县"},
    {"id": 5, "name": "中共赤城县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共赤城县委员会", "location": "河北省张家口市赤城县"},
    {"id": 6, "name": "张家口市人大常委会", "type": "人大", "level": "地市级",
     "parent": "河北省人大常委会", "location": "河北省张家口市"},
    {"id": 7, "name": "中共康保县委员会", "type": "党委", "level": "县委",
     "parent": "中共张家口市委员会", "location": "河北省张家口市康保县"},
    {"id": 8, "name": "张家口市人民政府", "type": "政府", "level": "地市级",
     "parent": "河北省人民政府", "location": "河北省张家口市"},
    {"id": 9, "name": "赤城县人民政府办公室", "type": "政府", "level": "正科级",
     "parent": "赤城县人民政府", "location": "河北省张家口市赤城县"},
    {"id": 10, "name": "中共蔚县委员会", "type": "党委", "level": "县委",
     "parent": "中共张家口市委员会", "location": "河北省张家口市蔚县"},
    {"id": 11, "name": "中共张北县委员会", "type": "党委", "level": "县委",
     "parent": "中共张家口市委员会", "location": "河北省张家口市张北县"},
]

positions = [
    # 邓艳杰
    {"person_id": 1, "org_id": 1, "title": "赤城县委书记", "start": "2026-05",
     "end": "至今", "rank": "正处级", "note": "2026年7月19日县委十四届一次全体会议连任"},
    {"person_id": 1, "org_id": 2, "title": "赤城县委副书记、县长", "start": "~2021",
     "end": "2026-05", "rank": "正处级", "note": "与赵红革任书记时搭班；后转任书记"},

    # 陈涛
    {"person_id": 2, "org_id": 1, "title": "赤城县委副书记、县长", "start": "2026-07",
     "end": "至今", "rank": "正处级", "note": "代县长→县第十八届人大一次会议选举产生"},

    # 戎海广
    {"person_id": 3, "org_id": 1, "title": "赤城县委副书记", "start": "~2026",
     "end": "至今", "rank": "正处级", "note": "2026年7月党代会确认"},

    # 王东升
    {"person_id": 4, "org_id": 1, "title": "赤城县委常委", "start": "",
     "end": "至今", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 4, "org_id": 2, "title": "赤城县常务副县长", "start": "",
     "end": "至今", "rank": "副处级", "note": "负责县常务工作, 首都两区建设, 等"},

    # 杨治国
    {"person_id": 5, "org_id": 5, "title": "赤城县委常委、纪委书记", "start": "~2026-07",
     "end": "至今", "rank": "副处级", "note": "2026年7月19日纪委第一次全会当选"},

    # 杨怿欣
    {"person_id": 6, "org_id": 1, "title": "赤城县委常委、宣传部部长", "start": "~2026",
     "end": "至今", "rank": "副处级", "note": "2026年6月新闻确认"},

    # 赵红革
    {"person_id": 7, "org_id": 6, "title": "张家口市人大常委会党组成员、秘书长、机关党组书记",
     "start": "2026-02", "end": "至今", "rank": "正处级", "note": "2026年2月6日当选"},
    {"person_id": 7, "org_id": 1, "title": "赤城县委书记", "start": "2021-05",
     "end": "2026-02", "rank": "正处级", "note": "河北省脱贫攻坚先进个人(2021.04)"},
    {"person_id": 7, "org_id": 2, "title": "赤城县委副书记、县长", "start": "2019-02",
     "end": "2021-05", "rank": "正处级", "note": "同时任经济开发区管委会主任"},
    {"person_id": 7, "org_id": 1, "title": "赤城县委副书记", "start": "2018-02",
     "end": "2019-02", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 10, "title": "蔚县县委常委、常务副县长", "start": "2016-12",
     "end": "2018-02", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 10, "title": "蔚县县委常委、副县长", "start": "2011-08",
     "end": "2016-12", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 11, "title": "张北县委常委、县委办公室主任", "start": "2009-12",
     "end": "2011-08", "rank": "副处级", "note": ""},

    # 薛宏霞
    {"person_id": 8, "org_id": 7, "title": "康保县委书记", "start": "2026-07",
     "end": "至今", "rank": "正处级", "note": "2026年7月19日康保县委十三届一次全会当选"},
    {"person_id": 8, "org_id": 1, "title": "赤城县委书记", "start": "~2025",
     "end": "2026-05", "rank": "正处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "赤城县委副书记、县长", "start": "~2021-06",
     "end": "~2025", "rank": "正处级", "note": ""},

    # 靳卓伢
    {"person_id": 9, "org_id": 3, "title": "赤城县人大常委会党组书记", "start": "",
     "end": "至今", "rank": "正处级", "note": "十八届人大一次会议主席团常务主席"},

    # 刘雪松
    {"person_id": 18, "org_id": 8, "title": "张家口市副市长", "start": "",
     "end": "至今", "rank": "副厅级", "note": "赤城籍"},
]

relationships = [
    # 邓艳杰↔赵红革：书记交接
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor",
     "context": "赵红革为前任书记(2021-2026), 邓艳杰接任书记。此前邓艳杰任县长时赵红革为书记。",
     "overlap_org": "中共赤城县委员会", "overlap_period": "2021-2026",
     "strength": "strong", "confidence": "confirmed"},

    # 邓艳杰↔陈涛：搭班
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "邓艳杰为县委书记, 陈涛为县长/代县长, 直接搭班的正副手关系。",
     "overlap_org": "中共赤城县委员会/赤城县人民政府", "overlap_period": "2026-07至今",
     "strength": "strong", "confidence": "confirmed"},

    # 邓艳杰↔王东升：上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与常务副县长",
     "overlap_org": "中共赤城县委员会", "overlap_period": "",
     "strength": "strong", "confidence": "confirmed"},

    # 邓艳杰↔杨治国：上下级·一届班子
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与纪委书记（同一届县委常委会）",
     "overlap_org": "中共赤城县委员会", "overlap_period": "2026-07至今",
     "strength": "strong", "confidence": "confirmed"},

    # 邓艳杰↔杨怿欣：上下级·一届班子
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与宣传部部长（同一届县委常委会）",
     "overlap_org": "中共赤城县委员会", "overlap_period": "2026-07至今",
     "strength": "strong", "confidence": "confirmed"},

    # 陈涛↔戎海广：搭班副书记
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与专职副书记",
     "overlap_org": "中共赤城县委员会", "overlap_period": "2026-07至今",
     "strength": "medium", "confidence": "confirmed"},

    # 薛宏霞↔邓艳杰：县长交接/前后任
    {"person_a": 8, "person_b": 1, "type": "predecessor_successor",
     "context": "薛宏霞由县委书记调任康保县委书记后, 邓艳杰由县长升任书记。",
     "overlap_org": "中共赤城县委员会", "overlap_period": "~2025-2026",
     "strength": "strong", "confidence": "confirmed"},

    # 赵红革↔薛宏霞：书记交接
    {"person_a": 7, "person_b": 8, "type": "predecessor_successor",
     "context": "赵红革调任市人大常委会后, 薛宏霞由县长升任书记。",
     "overlap_org": "中共赤城县委员会", "overlap_period": "~2025-2026",
     "strength": "strong", "confidence": "confirmed"},

    # 赵红革→蔚县/张北·跨县交流
    {"person_a": 7, "person_b": 4, "type": "other",
     "context": "赵红革跨县交流路径：张北→蔚县→赤城，反映了张家口北部县域间的干部交流模式。",
     "overlap_org": "张家口市", "overlap_period": "2009-2026",
     "strength": "medium", "confidence": "confirmed"},

    # 刘雪松↔赤城县·籍贯
    {"person_a": 18, "person_b": 1, "type": "same_native_place",
     "context": "刘雪松为赤城籍, 曾任康保县委书记。",
     "overlap_org": "赤城", "overlap_period": "",
     "strength": "weak", "confidence": "plausible"},

    # 薛宏霞→康保：跨县调动
    {"person_a": 8, "person_b": 18, "type": "other",
     "context": "薛宏霞调任康保县委书记, 刘雪松曾任康保县委书记。二人都与康保县有关联。",
     "overlap_org": "中共康保县委员会", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},
]


# ═══════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════

def build_db():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
            name TEXT NOT NULL,
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
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"],
             r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def esc(s):
    """XML-escape."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    today = datetime.now().strftime("%Y-%m-%d")
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>赤城县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] <= 2 else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"][:20])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Org nodes ──
    lines.append('    <nodes>')
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges: person → org (worked at) ──
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"][:50])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="medium"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # ── Edges: person ↔ person (relationships) ──
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="2" value="{r["confidence"]}"/>')
        v3 = esc(r.get("context","")[:50])
        lines.append(f'          <attvalue for="3" value="{v3}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    content = "\n".join(lines)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[GEXF] Created: {GEXF_PATH}")

    # Also update the canonical path
    canonical_gexf = os.path.join(BASE, "data/graph/赤城县_network.gexf")
    with open(canonical_gexf, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[GEXF] Also written to canonical: {canonical_gexf}")


def person_color(p):
    name = p.get("name", "")
    post = p.get("current_post", "")
    # Party Secretary → red
    if "县委书记" in post and "副书记" not in post:
        return "255,50,50"
    # Government leader → blue
    if "县长" in post or "代县长" in post:
        return "50,100,255"
    # Discipline → orange
    if "纪委书记" in post or "纪检" in post:
        return "255,165,0"
    # Organization/topcodes → grey
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    c = colors.get(org_type, "200,200,200")
    return c.split(",")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")