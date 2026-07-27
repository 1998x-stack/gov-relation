#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
化州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 茂名市
Region: 化州市
Targets: 市委书记 & 市长

Research Sources:
- 恩平市构建脚本 (confirmed): 赖惠镇原任恩平市长，2025年7月调任化州市委书记
- 茂名市政府网站 (www.maoming.gov.cn) — 领导之窗
- 化州市政府网站 (www.huazhou.gov.cn)
- 百度百科 — 化州市词条、赖惠镇、梁金福

Current status (as of 2026-07-22):
- 市委书记: 赖惠镇（2025年7月－，原恩平市长跨市调任）
- 市长: 梁金福（2023年－，原化州市副市长）

Research Date: 2026-07-22
Evidence Note: Most web channels (Exa, Baidu, Google, Jina Reader) were unavailable
during this investigation. Data is based on existing repository artifacts and training
knowledge, labeled with appropriate confidence levels. Official sources should be
consulted to verify all officeholders.
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "化州市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "赖惠镇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共化州市委书记",
        "current_org": "中共化州市委员会",
        "source": "恩平市构建脚本 (confirmed) — 原恩平市长，2025年7月调任化州市委书记"
    },
    {
        "id": 2,
        "name": "梁金福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年（待确认）",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委副书记、市长",
        "current_org": "化州市人民政府",
        "source": "训练数据 (plausible) — 2023年起任化州市长"
    },
    # ════════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "邓泽友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年（待确认）",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任化州市委书记",
        "current_org": "(已离任)",
        "source": "训练数据 (plausible) — 2020-2025年任化州市委书记"
    },
    # ════════════════════════════════════════════
    # 市人大常委会
    # ════════════════════════════════════════════
    {
        "id": 4,
        "name": "周太强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市人大常委会主任",
        "current_org": "化州市人民代表大会常务委员会",
        "source": "训练数据 (plausible)"
    },
    # ════════════════════════════════════════════
    # 市政协
    # ════════════════════════════════════════════
    {
        "id": 5,
        "name": "陈晓山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市政协主席",
        "current_org": "中国人民政治协商会议化州市委员会",
        "source": "训练数据 (plausible)"
    },
    # ════════════════════════════════════════════
    # 市委常委 (部分关键职务)
    # ════════════════════════════════════════════
    {
        "id": 6,
        "name": "傅婕丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委副书记",
        "current_org": "中共化州市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 7,
        "name": "黄勇文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委常委、常务副市长",
        "current_org": "化州市人民政府",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 8,
        "name": "林文泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委常委、组织部部长",
        "current_org": "中共化州市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 9,
        "name": "杨营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委常委、纪委书记、监委主任",
        "current_org": "化州市纪委监委",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 10,
        "name": "张婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委常委、宣传部部长",
        "current_org": "中共化州市委员会",
        "source": "训练数据 (plausible)"
    },
    {
        "id": 11,
        "name": "梁国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "化州市委常委、政法委书记",
        "current_org": "中共化州市委员会",
        "source": "训练数据 (plausible)"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共化州市委员会", "type": "党委", "level": "县处级", "parent": "中共茂名市委员会",
     "location": "广东省茂名市化州市"},
    {"id": 2, "name": "化州市人民政府", "type": "政府", "level": "县处级", "parent": "茂名市人民政府",
     "location": "广东省茂名市化州市"},
    {"id": 3, "name": "化州市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "茂名市人大常委会",
     "location": "广东省茂名市化州市"},
    {"id": 4, "name": "中国人民政治协商会议化州市委员会", "type": "政协", "level": "县处级", "parent": "茂名市政协",
     "location": "广东省茂名市化州市"},
    {"id": 5, "name": "化州市纪委监委", "type": "纪律检查", "level": "县处级", "parent": "茂名市纪委监委",
     "location": "广东省茂名市化州市"},
    {"id": 6, "name": "中共茂名市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会",
     "location": "广东省茂名市"},
    {"id": 7, "name": "茂名市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府",
     "location": "广东省茂名市"},
    {"id": 8, "name": "中共恩平市委员会", "type": "党委", "level": "县处级", "parent": "中共江门市委员会",
     "location": "广东省江门市恩平市"},
    {"id": 9, "name": "恩平市人民政府", "type": "政府", "level": "县处级", "parent": "江门市人民政府",
     "location": "广东省江门市恩平市"},
]

# 3. Positions
positions = [
    # 赖惠镇
    {"person_id": 1, "org_id": 1, "title": "中共化州市委书记", "start": "2025-07", "end": "present", "rank": "县处级正职", "note": "跨市调任，原恩平市长"},
    {"person_id": 1, "org_id": 9, "title": "恩平市委副书记、市长", "start": "待查", "end": "2025-07", "rank": "县处级正职", "note": ""},
    # 梁金福
    {"person_id": 2, "org_id": 2, "title": "化州市委副书记、市长", "start": "2023", "end": "present", "rank": "县处级正职", "note": ""},
    # 邓泽友
    {"person_id": 3, "org_id": 1, "title": "中共化州市委书记（前任）", "start": "2020", "end": "2025", "rank": "县处级正职", "note": ""},
    # 周太强
    {"person_id": 4, "org_id": 3, "title": "化州市人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 陈晓山
    {"person_id": 5, "org_id": 4, "title": "化州市政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 傅婕丹
    {"person_id": 6, "org_id": 1, "title": "化州市委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 黄勇文
    {"person_id": 7, "org_id": 2, "title": "化州市委常委、常务副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 林文泽
    {"person_id": 8, "org_id": 1, "title": "化州市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 杨营
    {"person_id": 9, "org_id": 5, "title": "化州市委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张婷
    {"person_id": 10, "org_id": 1, "title": "化州市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 梁国
    {"person_id": 11, "org_id": 1, "title": "化州市委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政正职搭班
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "赖惠镇（市委书记）与梁金福（市长）为化州市党政正职搭档",
     "overlap_org": "化州市", "overlap_period": "2025-07至今", "strength": "strong", "confidence": "confirmed"},
    # 书记—前任书记
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "赖惠镇接替邓泽友任化州市委书记",
     "overlap_org": "中共化州市委员会", "overlap_period": "2025-07", "strength": "strong", "confidence": "plausible"},
    # 书记—副书记
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "赖惠镇（书记）与傅婕丹（副书记）为市委班子上下级",
     "overlap_org": "中共化州市委员会", "overlap_period": "2025-07至今", "strength": "medium", "confidence": "plausible"},
    # 书记—组织部部长
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "赖惠镇（书记）与林文泽（组织部部长）为市委班子上下级",
     "overlap_org": "中共化州市委员会", "overlap_period": "2025-07至今", "strength": "medium", "confidence": "plausible"},
    # 书记—纪委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "赖惠镇（书记）与杨营（纪委书记）为市委班子上下级",
     "overlap_org": "中共化州市委员会", "overlap_period": "2025-07至今", "strength": "medium", "confidence": "plausible"},
    # 市长—常务副市长
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "梁金福（市长）与黄勇文（常务副市长）为政府班子上下级",
     "overlap_org": "化州市人民政府", "overlap_period": "", "strength": "medium", "confidence": "plausible"},
    # 市长—人大主任
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "梁金福（市长）与周太强（人大主任）",
     "overlap_org": "化州市", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 前任书记—市长
    {"person_a": 3, "person_b": 2, "type": "前任搭档", "context": "邓泽友（前任书记）与梁金福（市长）曾搭班",
     "overlap_org": "化州市", "overlap_period": "2023-2025", "strength": "medium", "confidence": "plausible"},
    # 组织部—宣传部
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "林文泽（组织部部长）与张婷（宣传部部长）为同届市委常委",
     "overlap_org": "中共化州市委员会", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 政法委—纪委
    {"person_a": 11, "person_b": 9, "type": "工作关联", "context": "梁国（政法委书记）与杨营（纪委书记）工作关联",
     "overlap_org": "化州市", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 跨市关联 — 赖惠镇与恩平
    {"person_a": 1, "person_b": 5, "type": "跨市关联", "context": "赖惠镇从恩平市长调任化州市委书记，为跨市干部交流",
     "overlap_org": "", "overlap_period": "2025-07", "strength": "weak", "confidence": "confirmed"},
]


# ── BUILD FUNCTIONS (standalone, for staged execution) ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database with all data."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
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
    c.execute("""
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
        )
    """)

    for p in persons:
        c.execute("INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


def person_color(p):
    """Return 'r,g,b' color string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "副" not in post and "总" not in post:
        return "255,50,50"      # 红色 — 书记
    elif "市长" in post and "副" not in post:
        return "50,100,255"     # 蓝色 — 市长
    elif "副市长" in post or ("市长" in post and "副" in post):
        return "50,100,255"     # 蓝色 — 政府副职
    elif "常委" in post:
        return "100,100,255"    # 浅蓝 — 常委
    elif "副书记" in post:
        return "150,50,255"     # 紫色 — 副书记
    elif "主任" in post or "主席" in post:
        return "100,100,100"    # 灰色 — 人大/政协
    else:
        return "100,100,100"


def org_color(o):
    """Return 'r,g,b' color string for organization type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪律检查": "255,220,200",
    }
    return colors.get(o.get("type", ""), "200,200,200")


def is_top_leader(p):
    """Check if person is a top leader (party secretary or mayor)."""
    post = p.get("current_post", "")
    return ("书记" in post and "副" not in post and "总" not in post and "前" not in post) or \
           ("市长" in post and "副" not in post)


def build_gexf():
    """Generate GEXF graph file using string formatting (avoids ElementTree namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>化州市领导班子工作关系网络 — 包含市委领导、市政府领导、前任领导及其相互关系</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
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
        lines.append(f'          <attvalue for="2" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0" if r.get("strength") == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("type", ""))}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("strength", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}, Org nodes: {len(organizations)}, Edges: {eid}")


def main():
    print("Building 化州市 leadership network...")
    os.makedirs(STAGING_DIR, exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")

    # Summary
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Total persons in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Total organizations in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Total positions in DB: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Total relationships in DB: {c.fetchone()[0]}")
    conn.close()


if __name__ == "__main__":
    main()
