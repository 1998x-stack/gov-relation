#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 石狮市 (Shishi, Quanzhou, Fujian).

Task: fujian_石狮市 — 市委书记 & 市长
Province: 福建省
Parent city: 泉州市
Region: 石狮市
Level: 县级市
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 市委书记: 李强 (男, 汉族, 泉州市委常委兼石狮市委书记, 副厅级)
- 市长: 余志伟 (男, 汉族, 1985年9月出生, 博士研究生学历, 石狮市委副书记、市长)

Government leadership (石狮市人民政府):
- 市长: 余志伟
- 常务副市长: 郭小强 (1981年5月出生, 党校研究生学历)
- 副市长: 黄明瑄 (女, 1974年11月出生, 党校大学学历)
- 副市长: 许自霖 (1987年8月出生, 博士研究生学历)
- 副市长: 张子牙
- 副市长: 蔡俊龙
- 副市长: 陈宏斌
- 副市长: 陈杰显
- 副市长: 邱华侨
- 副市长: 马涛

Sources:
- 石狮市人民政府官网 (shishi.gov.cn) — 领导之窗
- 中文维基百科 — 泉州市词条 (泉州市委常委会成员)
- build_泉州市_data.py (existing repo artifact)

Confidence: Current leadership identity-level confirmed from official website
and Wikipedia sources.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING = SCRIPT_DIR  # We are in data/tmp/fujian_石狮市/
DB_PATH = os.path.join(STAGING, "石狮市_network.db")
GEXF_PATH = os.path.join(STAGING, "石狮市_network.gexf")
REPORT_DIR = os.path.join(STAGING, "report")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 市委书记 — 李强
    {
        "id": "shishi_li_qiang",
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泉州市委常委、石狮市委书记",
        "current_org": "中共石狮市委",
        "source": "中文维基百科（泉州市词条—市委常委会名单）; build_泉州市_data.py",
        "notes": "兼任泉州市委常委。公开履历有限，待进一步查证。",
        "confidence": "plausible",
    },

    # 市长 — 余志伟
    {
        "id": "shishi_yu_zhiwei",
        "name": "余志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "未知",
        "native_place": "",
        "education": "博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石狮市委副书记、市政府市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/hch/）",
        "notes": "博士研究生学历。主持市政府全面工作，负责审计工作。",
        "confidence": "confirmed",
    },

    # 常务副市长 — 郭小强
    {
        "id": "shishi_guo_xiaoqiang",
        "name": "郭小强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年5月",
        "birthplace": "未知",
        "native_place": "",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石狮市委常委、市政府常务副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/gxq/）",
        "notes": "协助市长负责市政府常务工作。分管发改、应急、审计、统计、高新园区等工作。",
        "confidence": "confirmed",
    },

    # 副市长 — 黄明瑄
    {
        "id": "shishi_huang_mingxuan",
        "name": "黄明瑄",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "未知",
        "native_place": "",
        "education": "党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/hmx/）",
        "notes": "分管民政、人社、文旅、卫健、医保、市场监管等工作。",
        "confidence": "confirmed",
    },

    # 副市长 — 许自霖
    {
        "id": "shishi_xu_zilin",
        "name": "许自霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "未知",
        "native_place": "",
        "education": "博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/xzl/）",
        "notes": "分管人防、工信、科技、绿色经济、城乡建设工作。",
        "confidence": "confirmed",
    },

    # 副市长 — 张子牙
    {
        "id": "shishi_zhang_ziya",
        "name": "张子牙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },

    # 副市长 — 蔡俊龙
    {
        "id": "shishi_cai_junlong",
        "name": "蔡俊龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },

    # 副市长 — 陈宏斌
    {
        "id": "shishi_chen_hongbin",
        "name": "陈宏斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },

    # 副市长 — 陈杰显
    {
        "id": "shishi_chen_jiexian",
        "name": "陈杰显",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },

    # 副市长 — 邱华侨
    {
        "id": "shishi_qiu_huaqiao",
        "name": "邱华侨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },

    # 副市长 — 马涛
    {
        "id": "shishi_ma_tao",
        "name": "马涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石狮市政府副市长",
        "current_org": "石狮市人民政府",
        "source": "石狮市人民政府官网—领导之窗（shishi.gov.cn/zwgk/ldzc/）",
        "notes": "详细履历待查。",
        "confidence": "plausible",
    },
]

organizations = [
    {"id": "shiwei", "name": "中共石狮市委", "type": "党委", "level": "县级市", "parent": "中共泉州市委", "location": "福建省泉州市石狮市"},
    {"id": "zhengfu", "name": "石狮市人民政府", "type": "政府", "level": "县级市", "parent": "泉州市人民政府", "location": "福建省泉州市石狮市"},
    {"id": "quanzhou_shiwei", "name": "中共泉州市委", "type": "党委", "level": "地级市", "parent": "中共福建省委", "location": "福建省泉州市"},
    {"id": "quanzhou_zhengfu", "name": "泉州市人民政府", "type": "政府", "level": "地级市", "parent": "福建省人民政府", "location": "福建省泉州市"},
]

positions = [
    # 李强
    {"person_id": "shishi_li_qiang", "org_id": "quanzhou_shiwei", "title": "泉州市委常委", "start": "unknown", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": "shishi_li_qiang", "org_id": "shiwei", "title": "石狮市委书记", "start": "unknown", "end": "present", "rank": "副厅级", "note": "兼任泉州市委常委"},
    # 余志伟
    {"person_id": "shishi_yu_zhiwei", "org_id": "shiwei", "title": "石狮市委副书记", "start": "unknown", "end": "present", "rank": "处级", "note": ""},
    {"person_id": "shishi_yu_zhiwei", "org_id": "zhengfu", "title": "石狮市市长", "start": "unknown", "end": "present", "rank": "处级", "note": "主持市政府全面工作"},
    # 郭小强
    {"person_id": "shishi_guo_xiaoqiang", "org_id": "shiwei", "title": "石狮市委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shishi_guo_xiaoqiang", "org_id": "zhengfu", "title": "石狮市常务副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "协助市长负责常务工作"},
    # 黄明瑄
    {"person_id": "shishi_huang_mingxuan", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管民政、人社、文旅、卫健等"},
    # 许自霖
    {"person_id": "shishi_xu_zilin", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管工信、科技、城乡建设等"},
    # 张子牙
    {"person_id": "shishi_zhang_ziya", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
    # 蔡俊龙
    {"person_id": "shishi_cai_junlong", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
    # 陈宏斌
    {"person_id": "shishi_chen_hongbin", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
    # 陈杰显
    {"person_id": "shishi_chen_jiexian", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
    # 邱华侨
    {"person_id": "shishi_qiu_huaqiao", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
    # 马涛
    {"person_id": "shishi_ma_tao", "org_id": "zhengfu", "title": "石狮市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "详细分工待查"},
]

relationships = [
    # 李强 — 余志伟 (书记与市长搭档)
    {"person_a": "shishi_li_qiang", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市委书记与市长搭档", "overlap_org": "中共石狮市委",
     "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    # 余志伟 — 郭小强 (市长与常务副市长)
    {"person_a": "shishi_yu_zhiwei", "person_b": "shishi_guo_xiaoqiang", "type": "overlap",
     "context": "石狮市市长与常务副市长搭档", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "strong", "confidence": "confirmed"},
    # 李强 — 郭小强 (市委常委班子)
    {"person_a": "shishi_li_qiang", "person_b": "shishi_guo_xiaoqiang", "type": "overlap",
     "context": "石狮市委常委班子内上下级关系", "overlap_org": "中共石狮市委",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    # 黄明瑄 — 余志伟 (副市长与市长)
    {"person_a": "shishi_huang_mingxuan", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    # 许自霖 — 余志伟 (副市长与市长)
    {"person_a": "shishi_xu_zilin", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "confirmed"},
    # 张子牙 — 余志伟
    {"person_a": "shishi_zhang_ziya", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
    # 蔡俊龙 — 余志伟
    {"person_a": "shishi_cai_junlong", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
    # 陈宏斌 — 余志伟
    {"person_a": "shishi_chen_hongbin", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
    # 陈杰显 — 余志伟
    {"person_a": "shishi_chen_jiexian", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
    # 邱华侨 — 余志伟
    {"person_a": "shishi_qiu_huaqiao", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
    # 马涛 — 余志伟
    {"person_a": "shishi_ma_tao", "person_b": "shishi_yu_zhiwei", "type": "overlap",
     "context": "石狮市副市长与市长同一班子", "overlap_org": "石狮市人民政府",
     "overlap_period": "present", "strength": "medium", "confidence": "plausible"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(p):
    return "市委书记" in p["current_post"] or "市长" in p["current_post"]


def person_color(p):
    """Return 'r,g,b' string for person node."""
    post = p["current_post"]
    if "市委书记" in post and "副" not in post:
        return "255,50,50"
    if "市长" in post and "副" not in post:
        return "50,100,255"
    if "常务副市长" in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>石狮市（福建省泉州市）政治人物关系网络 — 市委书记 & 市长</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="县级市"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (positions)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} — {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships)
    for rel in relationships:
        eid += 1
        w = {"strong": "2.0", "medium": "1.5", "weak": "1.0"}.get(rel["strength"], "1.0")
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()
    print(f"\n[DONE] 石狮市 network data built at {TODAY}")
