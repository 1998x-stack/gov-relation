#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 桓仁满族自治县, 本溪市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_桓仁满族自治县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL WEB ACCESS
  - Exa API rate-limited (free tier exhausted)
  - Baidu Baike: 403 block (unavailable)
  - 桓仁县人民政府门户网站 (www.hr.gov.cn): accessible via HTTP
  - Official leadership pages: primary source for roster data
  - Government news articles: primary source for current leaders

Current officeholders (as of 2026-07-25):
  - 县委书记: 田永军 (confirmed via hr.gov.cn news article 2026-06-04)
  - 县委副书记、县长: 姜赫 (confirmed from official leadership page)
  - Previous 县委书记: 刘明刚 (confirmed via 2024-07-26 news article)

Note on web access:
  - Baidu Baike entries for 田永军 and 姜赫 were inaccessible (403 captcha)
  - Full career history details are limited to what is published on the official government site
  - Person JSON files reflect partial evidence with explicit gaps
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/liaoning_桓仁满族自治县")
DB_PATH = os.path.join(TMP, "桓仁满族自治县_network.db")
GEXF_PATH = os.path.join(TMP, "桓仁满族自治县_network.gexf")

TODAY = "2026-07-25"
SLUG = "桓仁满族自治县"
AS_OF = TODAY

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": "p1", "name": "田永军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桓仁满族自治县委书记", "current_org": "中共桓仁满族自治县委员会",
     "source": "http://www.hr.gov.cn (县委书记田永军检查高考考前工作, 2026-06-04)"},
    {"id": "p2", "name": "姜赫", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桓仁满族自治县委副书记、县长、辽宁五女山经济开发区党工委书记",
     "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn (领导之窗)"},

    # ── County Government Leadership ──
    {"id": "p3", "name": "赵旭", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长（常务）", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p4", "name": "秦昆明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p5", "name": "谷凤龙", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p6", "name": "郝延军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长（挂职期满，暂不分管）", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p7", "name": "刘晓东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p8", "name": "郝帅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},
    {"id": "p9", "name": "吕超", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "桓仁满族自治县人民政府",
     "source": "http://www.hr.gov.cn/zwgk/ldzc/zfld (领导之窗)"},

    # ── Party Committee Leaders ──
    {"id": "p10", "name": "宋扬", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共桓仁满族自治县纪律检查委员会",
     "source": "http://www.hr.gov.cn (县纪委第七次全会, 2026-07-22)"},
    {"id": "p11", "name": "马文丽", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共桓仁满族自治县委员会统一战线工作部",
     "source": "http://www.hr.gov.cn (县委统一战线工作领导小组会议, 2026-07-16)"},

    # ── Previous Leaders ──
    {"id": "p12", "name": "刘明刚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任桓仁满族自治县委书记（已离任）", "current_org": "",
     "source": "http://www.hr.gov.cn (2024-07-26县委书记刘明刚到县委办公室)"},
]

organizations = [
    {"id": 1, "name": "中共桓仁满族自治县委员会", "type": "党委", "level": "县处级",
     "parent": "中共本溪市委员会", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 2, "name": "桓仁满族自治县人民政府", "type": "政府", "level": "县处级",
     "parent": "本溪市人民政府", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 3, "name": "辽宁五女山经济开发区", "type": "开发区", "level": "省级开发区",
     "parent": "桓仁满族自治县人民政府", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 4, "name": "中共桓仁满族自治县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共本溪市纪律检查委员会", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 5, "name": "桓仁满族自治县监察委员会", "type": "政府", "level": "县处级",
     "parent": "本溪市监察委员会", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 6, "name": "中共桓仁满族自治县委员会统一战线工作部", "type": "党委", "level": "县处级",
     "parent": "中共桓仁满族自治县委员会", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 7, "name": "桓仁满族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "本溪市人大常委会", "location": "辽宁省本溪市桓仁满族自治县"},
    {"id": 8, "name": "中国人民政治协商会议桓仁满族自治县委员会", "type": "政协", "level": "县处级",
     "parent": "政协本溪市委员会", "location": "辽宁省本溪市桓仁满族自治县"},
]

positions = [
    # 田永军 - 县委书记
    {"person_id": "p1", "org_id": 1, "title": "桓仁满族自治县委书记",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "当前在任县委书记，2026年6月已有公开报道"},

    # 姜赫 - 县长
    {"person_id": "p2", "org_id": 2, "title": "桓仁满族自治县县长",
     "start": "unknown", "end": "present", "rank": "县处级正职",
     "note": "主持县政府全面工作"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "县委副书记兼任县长"},
    {"person_id": "p2", "org_id": 3, "title": "辽宁五女山经济开发区党工委书记",
     "start": "unknown", "end": "present", "rank": "",
     "note": "兼任开发区党工委书记"},

    # 赵旭 - 常务副县长
    {"person_id": "p3", "org_id": 2, "title": "县委常委、副县长（常务）",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责县政府常务工作"},
    {"person_id": "p3", "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 秦昆明 - 县委常委、副县长
    {"person_id": "p4", "org_id": 2, "title": "县委常委、副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责退役军人、民族宗教等工作"},
    {"person_id": "p4", "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 谷凤龙 - 县委常委、副县长
    {"person_id": "p5", "org_id": 2, "title": "县委常委、副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责住建、自然资源、交通、林业草原等工作"},
    {"person_id": "p5", "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 郝延军 - 副县长（挂职）
    {"person_id": "p6", "org_id": 2, "title": "副县长（挂职）",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "挂职期满，暂不分管相关工作"},

    # 刘晓东 - 副县长
    {"person_id": "p7", "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责农业农村、乡村振兴、水务、人社、民政等工作"},

    # 郝帅 - 副县长
    {"person_id": "p8", "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责工信、商务、外事、生态环境、大数据、中医药健康产业等工作"},

    # 吕超 - 副县长
    {"person_id": "p9", "org_id": 2, "title": "副县长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "负责文旅、广电、体育、教育、卫健、医保、市场监管等工作"},

    # 宋扬 - 纪委书记
    {"person_id": "p10", "org_id": 4, "title": "县纪委书记",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "第十八届县纪委书记"},
    {"person_id": "p10", "org_id": 5, "title": "县监委主任",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": "监委主任"},
    {"person_id": "p10", "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 马文丽 - 统战部长
    {"person_id": "p11", "org_id": 6, "title": "县委常委、统战部部长",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": "p11", "org_id": 1, "title": "县委常委",
     "start": "unknown", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 刘明刚 - 前任县委书记
    {"person_id": "p12", "org_id": 1, "title": "前任县委书记",
     "start": "unknown", "end": "unknown", "rank": "县处级正职",
     "note": "田永军的前任，2024年7月以县委书记身份活动，具体去向待查"},
]

relationships = [
    # 田永军 ↔ 姜赫 (书记+县长搭档)
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档",
     "context": "县委书记与县长，为本县党政主要领导",
     "overlap_org": "中共桓仁满族自治县委员会/桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ↔ 赵旭 (书记+常务副)
    {"person_a": "p1", "person_b": "p3", "type": "上下级关系",
     "context": "县委书记与县委常委、常务副县长",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 姜赫 ↔ 赵旭 (县长+常务副)
    {"person_a": "p2", "person_b": "p3", "type": "上下级关系",
     "context": "县长与常务副县长",
     "overlap_org": "桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ↔ 秦昆明
    {"person_a": "p1", "person_b": "p4", "type": "上下级关系",
     "context": "县委书记与县委常委、副县长",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ↔ 谷凤龙
    {"person_a": "p1", "person_b": "p5", "type": "上下级关系",
     "context": "县委书记与县委常委、副县长",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ↔ 宋扬 (书记+纪委书记)
    {"person_a": "p1", "person_b": "p10", "type": "上下级关系",
     "context": "县委书记与县委常委、纪委书记",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ↔ 马文丽 (书记+统战部长)
    {"person_a": "p1", "person_b": "p11", "type": "上下级关系",
     "context": "县委书记与县委常委、统战部长",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 赵旭 ↔ 秦昆明 (同为县委常委)
    {"person_a": "p3", "person_b": "p4", "type": "同事关系",
     "context": "同为县委常委，县政府领导班子成员",
     "overlap_org": "中共桓仁满族自治县委员会/桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 赵旭 ↔ 谷凤龙 (同为县委常委)
    {"person_a": "p3", "person_b": "p5", "type": "同事关系",
     "context": "同为县委常委、副县长",
     "overlap_org": "中共桓仁满族自治县委员会/桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 秦昆明 ↔ 谷凤龙 (同为县委常委)
    {"person_a": "p4", "person_b": "p5", "type": "同事关系",
     "context": "同为县委常委、副县长",
     "overlap_org": "中共桓仁满族自治县委员会/桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 刘晓东 ↔ 郝帅 ↔ 吕超 (副县长同僚)
    {"person_a": "p7", "person_b": "p8", "type": "同事关系",
     "context": "同为副县长",
     "overlap_org": "桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},
    {"person_a": "p8", "person_b": "p9", "type": "同事关系",
     "context": "同为副县长",
     "overlap_org": "桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},
    {"person_a": "p7", "person_b": "p9", "type": "同事关系",
     "context": "同为副县长",
     "overlap_org": "桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},

    # 田永军 ← 刘明刚 (前后任书记)
    {"person_a": "p1", "person_b": "p12", "type": "predecessor_successor",
     "context": "田永军接替刘明刚任县委书记",
     "overlap_org": "中共桓仁满族自治县委员会",
     "overlap_period": "2024-2026（推测）",
     "confidence": "plausible"},

    # 姜赫 ↔ 秦昆明 (陪同考察)
    {"person_a": "p2", "person_b": "p4", "type": "上下级关系",
     "context": "县长与县委常委、副县长陪同江苏省医药行业协会考察",
     "overlap_org": "桓仁满族自治县人民政府",
     "overlap_period": "当前",
     "confidence": "confirmed"},
]


AS_OF = TODAY

# ── BUILD ────────────────────────────────────────────────────────────

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
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""))
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
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "纪委书记" in post or "监委" in post:
            return ("255,165,0", 15.0)
        elif "常委" in post and "副" in post:
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post:
            return ("100,150,255", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200"),
        "政府": ("200,200,255"),
        "人大": ("200,255,255"),
        "政协": ("255,240,200"),
        "开发区": ("200,255,200"),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络 - {AS_OF}</description>')
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
        lines.append(f'      <node id="p{pid(p["id"])}" label="{esc(p["name"])}">')
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
        oc = org_colors.get(o["type"], ("200,200,200"))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid(pos["person_id"])}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = pid(r["person_a"])
        b = pid(r["person_b"])
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
    print(f"{SLUG} Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
