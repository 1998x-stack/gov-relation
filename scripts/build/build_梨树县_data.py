#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 梨树县, 四平市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_梨树县
Research sources:
  - Lishu County Government Website (www.lishu.gov.cn) — official leadership pages
  - County government meeting records / news articles
  - Government work division adjustment notice (梨政发[2026]1号)
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "梨树县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Committee
    # ══════════════════════════════════════════════════════════════════════════

    # 赵光辉 — 县委书记 (confirmed as of Jul 2026)
    # Source: lishu.gov.cn meeting records — chaired multiple meetings in 2026
    # Hosted 第十二届梨树黑土地论坛 on 2026-07-23
    {"id": 1, "name": "赵光辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共梨树县委员会",
     "source": "http://www.lishu.gov.cn/zw/lsdt/202607/t20260723_771583.html",
     "notes": "Confirmed县委书记responsible for overall county work. Also chairs county reforms committee. Appeared in leadership activities throughout 2025-2026."},

    # 聂磊 — 县委副书记、县长 (confirmed as of Jul 2026)
    {"id": 2, "name": "聂磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年9月", "birthplace": "山东济宁", "education": "研究生学历，翻译学硕士",
     "party_join": "2003年12月", "work_start": "2012年7月",
     "current_post": "县委副书记、县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdjl/201701/t20170101_28390.html",
     "notes": "Took office as county chief around late 2025/early 2026, succeeding 毕志杰."},

    # 肖雷 — 县委常委、副县长 (常务)
    {"id": 3, "name": "肖雷", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年4月", "birthplace": "吉林四平", "education": "研究生学历",
     "party_join": "2011年6月", "work_start": "2009年7月",
     "current_post": "县委常委、副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/xl/",
     "notes": "Also serves as 林海镇党委书记. Handles day-to-day government operations (常务)."},

    # ══════════════════════════════════════════════════════════════════════════
    # County Government — Deputy Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # 刘跃昌 — 副县长
    {"id": 4, "name": "刘跃昌", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年8月", "birthplace": "吉林梨树", "education": "大学学历",
     "party_join": "2003年6月", "work_start": "1998年7月",
     "current_post": "副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/lyc/",
     "notes": "县政府党组成员. Handles agriculture, water resources, animal husbandry."},

    # 韩悦 — 副县长 (女)
    {"id": 5, "name": "韩悦", "gender": "女", "ethnicity": "满族",
     "birth": "1986年2月", "birthplace": "吉林四平", "education": "硕士研究生学历",
     "party_join": "2011年6月", "work_start": "2011年8月",
     "current_post": "副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/sdh/",
     "notes": "县政府党组成员. Handles education, health, medical insurance, culture."},

    # 于洪志 — 副县长
    {"id": 6, "name": "于洪志", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年10月", "birthplace": "吉林梨树", "education": "本科学历",
     "party_join": "2005年4月", "work_start": "1995年10月",
     "current_post": "副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/yhz/",
     "notes": "县政府党组成员. Handles industry, commerce, transport, market regulation."},

    # 王春光 — 副县长 (also 县自然资源局党组书记、局长)
    {"id": 7, "name": "王春光", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年2月", "birthplace": "吉林梨树", "education": "大专学历",
     "party_join": "2001年10月", "work_start": "2000年7月",
     "current_post": "副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/wcg/",
     "notes": "Also heads 县自然资源局. Handles housing, natural resources, forestry, urban management."},

    # 刘相国 — 副县长 (limited public bio available)
    {"id": 8, "name": "刘相国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/am/",
     "notes": "县政府领导成员. Bio details not yet available on official website."},

    # 张忠湛 — 副县长（挂职）
    {"id": 9, "name": "张忠湛", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年6月", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长（挂职）", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/wdts/zzz/",
     "notes": "From 吉林省动物疫病预防控制中心. Senior Veterinarian. Assists 刘跃昌 with agriculture/water/animal husbandry."},

    # ══════════════════════════════════════════════════════════════════════════
    # Key Party Committee Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # （Note: Party committee standing members beyond the party secretary and the
    #  executive deputy county head are not fully listed on the county government
    #  portal. The 县纪委监委, 组织部, 宣传部, 政法委, 统战部 leaders need
    #  further research from other sources.）

    # ══════════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════════

    # 毕志杰 — 前任县长 (succeeded by 聂磊)
    {"id": 10, "name": "毕志杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年5月", "birthplace": "吉林双辽", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任县长", "current_org": "梨树县人民政府",
     "source": "http://www.lishu.gov.cn/xz/",
     "notes": "Previous county chief. Appeared in news through late 2025. Replaced by 聂磊 in late 2025/early 2026."},

    # 王相民 — potential previous county party secretary or higher-level official
    # (mentioned in 2025 news inspecting Lishu)
    # Need more confirmation
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共梨树县委员会", "type": "党委", "level": "县处级", "parent": "中共四平市委", "location": "梨树县"},
    {"id": 2, "name": "梨树县人民政府", "type": "政府", "level": "县处级", "parent": "四平市人民政府", "location": "梨树县"},
    {"id": 3, "name": "梨树县人大常委会", "type": "人大", "level": "县处级", "parent": "四平市人大常委会", "location": "梨树县"},
    {"id": 4, "name": "政协梨树县委员会", "type": "政协", "level": "县处级", "parent": "政协四平市委", "location": "梨树县"},
    {"id": 5, "name": "梨树县纪委监委", "type": "党委", "level": "县处级", "parent": "四平市纪委监委", "location": "梨树县"},
    {"id": 6, "name": "中共梨树县委组织部", "type": "党委", "level": "正科级", "parent": "中共梨树县委员会", "location": "梨树县"},
    {"id": 7, "name": "中共梨树县委宣传部", "type": "党委", "level": "正科级", "parent": "中共梨树县委员会", "location": "梨树县"},
    {"id": 8, "name": "中共梨树县委政法委", "type": "党委", "level": "正科级", "parent": "中共梨树县委员会", "location": "梨树县"},
    {"id": 9, "name": "中共梨树县委统战部", "type": "党委", "level": "正科级", "parent": "中共梨树县委员会", "location": "梨树县"},
    {"id": 10, "name": "梨树县自然资源局", "type": "政府", "level": "正科级", "parent": "梨树县人民政府", "location": "梨树县"},
    {"id": 11, "name": "林海镇", "type": "乡镇", "level": "乡科级", "parent": "梨树县人民政府", "location": "梨树县"},
    {"id": 12, "name": "四平新型工业化经济开发区", "type": "政府", "level": "县处级", "parent": "四平市人民政府", "location": "梨树县"},
    {"id": 13, "name": "梨树经济开发区", "type": "政府", "level": "省级开发区", "parent": "梨树县人民政府", "location": "梨树县"},
    {"id": 14, "name": "吉林省动物疫病预防控制中心", "type": "事业单位", "level": "正处级", "parent": "吉林省农业农村厅", "location": "长春市"},
    {"id": 15, "name": "四平现代农业科学院", "type": "事业单位", "level": "县处级", "parent": "四平市人民政府", "location": "梨树县"},
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # 赵光辉 — 县委书记
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "县处级正职", "note": "Confirmed active as of July 2026. Chaired 2026年第11次县委常委会 on 2026-07-24."},

    # 聂磊 — 县长
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "2025年末", "end": "present",
     "rank": "县处级正职", "note": "Succeeded 毕志杰. Active in numerous 2026 activities."},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "2025年末", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 肖雷 — 常务副县长
    {"person_id": "p3", "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "Handles day-to-day government operations (常务)"},
    {"person_id": "p3", "org_id": 11, "title": "林海镇党委书记", "start": "", "end": "present",
     "rank": "乡科级正职", "note": "Concurrent township role"},

    # 刘跃昌 — 副县长
    {"person_id": "p4", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员. Agriculture, water, animal husbandry."},

    # 韩悦 — 副县长
    {"person_id": "p5", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员. Education, health, culture."},

    # 于洪志 — 副县长
    {"person_id": "p6", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "县政府党组成员. Industry, commerce, transport, market regulation."},

    # 王春光 — 副县长
    {"person_id": "p7", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "兼任县自然资源局党组书记、局长"},
    {"person_id": "p7", "org_id": 10, "title": "党组书记、局长", "start": "", "end": "present",
     "rank": "正科级", "note": "县自然资源局"},

    # 刘相国 — 副县长
    {"person_id": "p8", "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "Bio details limited on official site."},

    # 张忠湛 — 副县长（挂职）
    {"person_id": "p9", "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "县处级副职", "note": "挂职. From 省动物疫病预防控制中心."},
    {"person_id": "p9", "org_id": 14, "title": "办公室副主任、主任", "start": "", "end": "",
     "rank": "", "note": "吉林省动物疫病预防控制中心"},
    {"person_id": "p9", "org_id": 14, "title": "副主任、高级兽医师", "start": "", "end": "",
     "rank": "", "note": "吉林省动物疫病预防控制中心"},

    # 毕志杰 — 前任县长
    {"person_id": "p10", "org_id": 2, "title": "县长（前任）", "start": "", "end": "2025年末",
     "rank": "县处级正职", "note": "Last appeared in late 2025 news reports. Succeeded by 聂磊."},
    {"person_id": "p10", "org_id": 1, "title": "县委副书记（前任）", "start": "", "end": "2025年末",
     "rank": "县处级副职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # ===== Top Leader + Mayor =====
    {"person_a": "p1", "person_b": "p2", "type": "党政正职搭档",
     "context": "赵光辉（县委书记）与聂磊（县长）为当前党政正职搭档",
     "overlap_org": "中共梨树县委员会/梨树县人民政府", "overlap_period": "2025年末-至今",
     "confidence": "confirmed"},

    # ===== 赵光辉 + 毕志杰（前任搭档） =====
    {"person_a": "p1", "person_b": "p10", "type": "党政正职搭档（前任）",
     "context": "赵光辉（县委书记）与毕志杰（前任县长）为2025年前搭档",
     "overlap_org": "中共梨树县委员会/梨树县人民政府", "overlap_period": "-2025",
     "confidence": "confirmed"},

    # ===== 聂磊 + 肖雷（政府正副职） =====
    {"person_a": "p2", "person_b": "p3", "type": "政府正副职搭档",
     "context": "聂磊（县长）与肖雷（常务副县长）为政府正副职搭档",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    # ===== 聂磊 + 各副县长 =====
    {"person_a": "p2", "person_b": "p4", "type": "政府正副职",
     "context": "聂磊（县长）与刘跃昌（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    {"person_a": "p2", "person_b": "p5", "type": "政府正副职",
     "context": "聂磊（县长）与韩悦（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    {"person_a": "p2", "person_b": "p6", "type": "政府正副职",
     "context": "聂磊（县长）与于洪志（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    {"person_a": "p2", "person_b": "p7", "type": "政府正副职",
     "context": "聂磊（县长）与王春光（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    {"person_a": "p2", "person_b": "p9", "type": "政府正副职",
     "context": "聂磊（县长）与张忠湛（挂职副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "2025末-至今",
     "confidence": "confirmed"},

    # ===== 肖雷 + 副县长们 =====
    {"person_a": "p3", "person_b": "p4", "type": "政府副职共事",
     "context": "肖雷（常务副县长）与刘跃昌（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "",
     "confidence": "confirmed"},

    {"person_a": "p3", "person_b": "p5", "type": "政府副职共事",
     "context": "肖雷（常务副县长）与韩悦（副县长）在县政府共事",
     "overlap_org": "梨树县人民政府", "overlap_period": "",
     "confidence": "confirmed"},

    # ===== 赵光辉 + 肖雷（常委会共事） =====
    {"person_a": "p1", "person_b": "p3", "type": "党政协同",
     "context": "赵光辉（县委书记）与肖雷（县委常委、副县长）在县委常委会共事",
     "overlap_org": "中共梨树县委常委会", "overlap_period": "",
     "confidence": "confirmed"},

    # ===== 刘跃昌 + 张忠湛（协助关系） =====
    {"person_a": "p4", "person_b": "p9", "type": "工作协助",
     "context": "张忠湛（挂职副县长）协助刘跃昌（副县长）分管农业、水利、畜牧工作",
     "overlap_org": "梨树县人民政府", "overlap_period": "",
     "confidence": "confirmed"},
]

# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
            source TEXT,
            notes TEXT
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
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post and "县委副书记" in post:
            return ("50,100,255", 20.0)
        elif "县委常委" in post:
            return ("100,150,255", 15.0)
        elif "副" in post and "县长" in post:
            return ("100,150,255", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "群团": ("255,220,255", 8.0),
        "乡镇": ("255,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>梨树县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"梨树县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
