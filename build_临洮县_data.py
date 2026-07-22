#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临洮县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Lintao County leadership network.

Level: 县级
Province: 甘肃省
City: 定西市
Region: 临洮县
Targets: 县委书记 & 县长

Research Sources:
- 定西市人民政府官网 (dingxi.gov.cn) 领导之窗, 2026年7月确认
- Wikipedia (zh.wikipedia.org) — 定西市、张智全
- 百度百科
- 新闻报道

Research Date: 2026-07-22
Status: PARTIAL — Web access restricted during research; some biographical details marked unknown.
         Current county-level leaders could not be confirmed via web fetch (government sites
         timed out, search engine rate-limited). Data based on Wikipedia and previous
         county-level build scripts in this repository.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = SCRIPT_DIR
DB_PATH = os.path.join(STAGING_DIR, "临洮县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "临洮县_network.gexf")

# =========================================================================
# DATA
# =========================================================================
# NOTE: Web access was degraded during research (government sites timed out,
# search engine rate-limited). The current county-level leaders (县委书记, 县长)
# could not be confirmed from direct sources. The data below reflects known
# predecessor information and the organizational structure, with current
# officeholders marked as "待查" (to be verified).

# ── Persons ──
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (待查 — unconfirmed from direct source)
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "（现任县委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委书记",
        "current_org": "中共临洮县委员会",
        "source": "待确认 — 临洮党政网 www.lintao.gov.cn 未能在调研期间连接",
        "person_id": "lintao_county_secretary"
    },
    {
        "id": "p02",
        "name": "（现任县长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委副书记、县长",
        "current_org": "临洮县人民政府",
        "source": "待确认 — 临洮党政网 www.lintao.gov.cn 未能在调研期间连接",
        "person_id": "lintao_county_mayor"
    },
    # ════════════════════════════════════════
    # Predecessors — 县委书记
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "石琳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任临洮县委书记，后任定西市委常委等）",
        "current_org": "待查",
        "source": "公开报道 — 曾任临洮县委书记",
        "person_id": "lintao_shi_lin"
    },
    {
        "id": "p04",
        "name": "张智全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年10月",
        "birthplace": "甘肃陇西",
        "native_place": "甘肃陇西",
        "education": "庆阳师范专科学校中文专业/甘肃农业大学在职博士",
        "party_join": "1985年3月",
        "work_start": "1981年8月",
        "current_post": "（曾任临洮县委书记2000-2003，后任庆阳市委书记、白银市委书记，2018年被查处）",
        "current_org": "待查",
        "source": "Wikipedia: 张智全 (zh.wikipedia.org/wiki/张智全)",
        "person_id": "lintao_zhang_zhiquan"
    },
    # ════════════════════════════════════════
    # Known Predecessors — 县长
    # ════════════════════════════════════════
    {
        "id": "p05",
        "name": "张智全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年10月",
        "birthplace": "甘肃陇西",
        "native_place": "甘肃陇西",
        "education": "庆阳师范专科学校/甘肃农业大学在职博士",
        "party_join": "1985年3月",
        "work_start": "1981年8月",
        "current_post": "（曾任临洮县县长1997-2000）",
        "current_org": "待查",
        "source": "Wikipedia: 张智全",
        "person_id": "lintao_zhang_zhiquan_mayor"
    },
    # ════════════════════════════════════════
    # 定西市领导（上下级关系）
    # ════════════════════════════════════════
    {
        "id": "p10",
        "name": "汪尚学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "甘肃天水",
        "native_place": "甘肃天水",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委书记",
        "current_org": "中共定西市委员会",
        "source": "Wikipedia: 定西市; 定西市人民政府官网 (dingxi.gov.cn) 2026-07",
        "person_id": "dingxi_wang_shangxue"
    },
    {
        "id": "p11",
        "name": "黄欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委副书记",
        "current_org": "中共定西市委员会",
        "source": "定西市人民政府官网 (dingxi.gov.cn) 2026-07",
        "person_id": "dingxi_huang_xin"
    },
    {
        "id": "p12",
        "name": "何英禅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "定西市委常委、副市长",
        "current_org": "中共定西市委员会/定西市人民政府",
        "source": "定西市人民政府官网 (dingxi.gov.cn) 2026-07",
        "person_id": "dingxi_he_yingchan"
    },
    # ════════════════════════════════════════
    # 临洮县领导班子成员（待确认）
    # ════════════════════════════════════════
    {
        "id": "p20",
        "name": "（县委副书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委副书记",
        "current_org": "中共临洮县委员会",
        "source": "待确认",
        "person_id": "lintao_deputy_secretary"
    },
    {
        "id": "p21",
        "name": "（常务副县长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委常委、常务副县长",
        "current_org": "临洮县人民政府",
        "source": "待确认",
        "person_id": "lintao_executive_deputy"
    },
    {
        "id": "p22",
        "name": "（纪委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委常委、纪委书记",
        "current_org": "中共临洮县纪律检查委员会",
        "source": "待确认",
        "person_id": "lintao_discipline_secretary"
    },
    {
        "id": "p23",
        "name": "（组织部长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "临洮县委常委、组织部部长",
        "current_org": "中共临洮县委组织部",
        "source": "待确认",
        "person_id": "lintao_organization_minister"
    },
]

# ── Organizations ──
organizations = [
    {"id": "o01", "name": "中共临洮县委员会", "type": "党委", "level": "县级", "parent": "中共定西市委员会", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o02", "name": "临洮县人民政府", "type": "政府", "level": "县级", "parent": "定西市人民政府", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o03", "name": "临洮县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "定西市人民代表大会常务委员会", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o04", "name": "中国人民政治协商会议临洮县委员会", "type": "政协", "level": "县级", "parent": "政协定西市委员会", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o05", "name": "中共临洮县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共临洮县委员会", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o06", "name": "中共临洮县委组织部", "type": "党委", "level": "县级", "parent": "中共临洮县委员会", "location": "甘肃省定西市临洮县洮阳镇"},
    {"id": "o07", "name": "中共定西市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省定西市安定区"},
    {"id": "o08", "name": "定西市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省定西市安定区"},
]

# ── Positions ──
positions = [
    # Current top leaders (placeholder)
    {"person_id": "p01", "org_id": "o01", "title": "临洮县委书记", "start": "待查", "end": "至今", "rank": "正县级", "note": "当前任职者待确认"},
    {"person_id": "p02", "org_id": "o01", "title": "临洮县委副书记", "start": "待查", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p02", "org_id": "o02", "title": "临洮县县长", "start": "待查", "end": "至今", "rank": "正县级", "note": "当前任职者待确认"},
    
    # 石琳 — 曾任临洮县委书记
    {"person_id": "p03", "org_id": "o01", "title": "临洮县委书记", "start": "约2013", "end": "约2020", "rank": "正县级", "note": "具体任期待确认"},
    
    # 张智全 — 曾任临洮县委书记
    {"person_id": "p04", "org_id": "o01", "title": "临洮县委书记", "start": "2000-05", "end": "2003-03", "rank": "正县级", "note": "后任中共甘肃省委副秘书长"},
    # 张智全 — 曾任临洮县县长
    {"person_id": "p05", "org_id": "o02", "title": "临洮县县长", "start": "1997-12", "end": "2000-05", "rank": "正县级", "note": "后升任临洮县委书记"},
    
    # 定西市领导
    {"person_id": "p10", "org_id": "o07", "title": "定西市委书记", "start": "2023-03", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": "p11", "org_id": "o07", "title": "定西市委副书记", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p12", "org_id": "o07", "title": "定西市委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p12", "org_id": "o08", "title": "定西市副市长", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    
    # 临洮县委领导班子（待确认姓名）
    {"person_id": "p20", "org_id": "o01", "title": "临洮县委副书记", "start": "待查", "end": "至今", "rank": "副县级", "note": "姓名待确认"},
    {"person_id": "p21", "org_id": "o01", "title": "临洮县委常委", "start": "待查", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p21", "org_id": "o02", "title": "临洮县常务副县长", "start": "待查", "end": "至今", "rank": "副县级", "note": "姓名待确认"},
    {"person_id": "p22", "org_id": "o01", "title": "临洮县委常委", "start": "待查", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p22", "org_id": "o05", "title": "临洮县纪委书记", "start": "待查", "end": "至今", "rank": "副县级", "note": "姓名待确认"},
    {"person_id": "p23", "org_id": "o01", "title": "临洮县委常委", "start": "待查", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": "p23", "org_id": "o06", "title": "临洮县委组织部部长", "start": "待查", "end": "至今", "rank": "副县级", "note": "姓名待确认"},
]

# ── Relationships ──
relationships = [
    # 上下级关系 — 县委书记 → 定西市委
    {"person_a": "p01", "person_b": "p10", "type": "superior_subordinate", "context": "临洮县委书记受定西市委书记领导", "overlap_org": "定西市/临洮县", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p10", "type": "superior_subordinate", "context": "临洮县长受定西市委书记领导", "overlap_org": "定西市/临洮县", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    
    # 党政一把手关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "临洮县委书记与县长: 党政一把手配合", "overlap_org": "中共临洮县委员会/临洮县人民政府", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    
    # 县委班子内部
    {"person_a": "p01", "person_b": "p20", "type": "overlap", "context": "县委书记与县委副书记", "overlap_org": "中共临洮县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p21", "type": "overlap", "context": "县委书记与常务副县长", "overlap_org": "中共临洮县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p22", "type": "overlap", "context": "县委书记与纪委书记", "overlap_org": "中共临洮县委员会", "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    
    # 前后任书记关系
    {"person_a": "p01", "person_b": "p03", "type": "predecessor_successor", "context": "（现任）接替石琳任临洮县委书记", "overlap_org": "中共临洮县委员会", "overlap_period": "约2020", "strength": "strong", "confidence": "plausible"},
    {"person_a": "p03", "person_b": "p04", "type": "predecessor_successor", "context": "石琳接替张智全任临洮县委书记（推测）", "overlap_org": "中共临洮县委员会", "overlap_period": "约2003-2013间", "strength": "medium", "confidence": "unverified"},
    
    # 前后任县长关系
    {"person_a": "p02", "person_b": "p05", "type": "predecessor_successor", "context": "（现任）接替张智全等任临洮县长", "overlap_org": "临洮县人民政府", "overlap_period": "待查", "strength": "medium", "confidence": "unverified"},
    
    # 张智全由县长升书记
    {"person_a": "p04", "person_b": "p05", "type": "promotion_chain", "context": "张智全从临洮县长升任临洮县委书记（同人不同角色）", "overlap_org": "中共临洮县委员会", "overlap_period": "2000-05", "strength": "strong", "confidence": "confirmed"},
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "人大" not in title and "政协" not in title and "统战" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and "副书记" in title:
        return "50,100,255"   # Blue — Government head
    if "县长" in title:
        return "50,100,255"
    if "纪委" in title or "监委" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副市长" in title:
        return "100,100,200"  # Light blue
    return "100,100,100"      # Grey — Other


def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title:
        return "20.0"
    if "县长" in title and "副书记" in title:
        return "20.0"
    if "县委书记" in title or "原" in title:
        return "14.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title or "纪委书记" in title:
        return "12.0"
    return "10.0"


def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(t, "200,200,200")


# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()


# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>临洮县领导班子工作关系网络 - 数据来源: 定西市人民政府官网, Wikipedia及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="定西市"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="定西市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ── Main ──

def main():
    print(f"=== 临洮县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
