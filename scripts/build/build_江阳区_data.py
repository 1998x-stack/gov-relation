#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 江阳区 (Jiangyang District), 泸州市, 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_江阳区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.jiangyang.gov.cn — 泸州市江阳区人民政府 (official leadership profiles, accessed 2026-07-26)
  - 袁瑞 profile: https://www.jiangyang.gov.cn/zfld/content_112764
  - 刘波 profile: https://www.jiangyang.gov.cn/zfld/content_115640
  - 周作昂 profile: https://www.jiangyang.gov.cn/zfld/content_117746
  - 杨静喜 profile: https://www.jiangyang.gov.cn/zfld/content_81454
  - 陈文杰 profile: https://www.jiangyang.gov.cn/zfld/content_59009
  - 刘智宇 profile: https://www.jiangyang.gov.cn/zfld/content_80333
  - 王天泉 profile: https://www.jiangyang.gov.cn/zfld/content_99110
  - 张骋 profile: https://www.jiangyang.gov.cn/zfld/content_110257
  - 奚小淋 profile: https://www.jiangyang.gov.cn/zfld/content_121472
  - News articles mentioning 徐兵 as 区委书记 (multiple articles on jiangyang.gov.cn, e.g., content_123672)
  - Baidu Baike (unreachable during investigation - 403/timeout)

Confidence notes:
  - 袁瑞 (区长): confirmed via official government profile with full bio
  - 徐兵 (区委书记): confirmed as区委书记 from multiple government news articles mentioning him as presiding over party committee meetings; detailed career history unverified due to web access limitations
  - All deputy 副区长: confirmed via official government profiles
  - Detailed career timelines for some officials incomplete due to web access limitations
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = str(STAGING_DIR)
SLUG = "江阳区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Secretary
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "徐兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共泸州市江阳区委员会",
        "source": "https://www.jiangyang.gov.cn/zwdt/jyyw/content_123672 (news article mentioning 徐兵主持会议并讲话)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "袁瑞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "四川省泸州市",
        "education": "硕士研究生学历，电子科技大学公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "2004年7月",
        "current_post": "区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_112764"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leaders — 区政府领导班子
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年9月",
        "birthplace": "四川省合江县",
        "education": "大学学历，工学学士，西昌学院电子信息工程专业",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "常务副区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_115640"
    },
    {
        "id": 4,
        "name": "周作昂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "四川省高县",
        "education": "博士研究生学历，西南财经大学经济学博士学位",
        "party_join": "中共党员",
        "work_start": "2007年7月",
        "current_post": "副区长（挂职）",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_117746"
    },
    {
        "id": 5,
        "name": "杨静喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "四川省合江县",
        "education": "大学学历，工学学士，中国人民解放军后勤工程学院计算机应用专业",
        "party_join": "民盟盟员",
        "work_start": "2002年7月",
        "current_post": "副区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_81454"
    },
    {
        "id": 6,
        "name": "陈文杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "四川省泸县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_59009"
    },
    {
        "id": 7,
        "name": "刘智宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年1月",
        "birthplace": "四川省合江县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2010年8月",
        "current_post": "副区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_80333"
    },
    {
        "id": 8,
        "name": "王天泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "四川师范大学汉语言文学专业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_99110"
    },
    {
        "id": 9,
        "name": "张骋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "四川省泸州市",
        "education": "大学本科学历，文学学士，四川理工学院汉语言文学专业",
        "party_join": "中共党员",
        "work_start": "2010年7月",
        "current_post": "副区长",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_110257"
    },
    {
        "id": 10,
        "name": "奚小淋",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "四川省泸州市",
        "education": "大学本科学历，工学学士",
        "party_join": "中共党员",
        "work_start": "2004年12月",
        "current_post": "区政府党组成员、市张坝-方山景区党工委书记",
        "current_org": "泸州市江阳区人民政府",
        "source": "https://www.jiangyang.gov.cn/zfld/content_121472"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泸州市江阳区委员会", "type": "党委", "level": "县级", "parent": "中共泸州市委员会", "location": "泸州市江阳区"},
    {"id": 2, "name": "泸州市江阳区人民政府", "type": "政府", "level": "县级", "parent": "泸州市人民政府", "location": "泸州市江阳区"},
    {"id": 3, "name": "泸州市江阳区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共泸州市江阳区委员会", "location": "泸州市江阳区"},
    {"id": 4, "name": "泸州市江阳区公安分局", "type": "政府", "level": "县级", "parent": "泸州市江阳区人民政府", "location": "泸州市江阳区"},
    {"id": 5, "name": "泸州市张坝-方山景区", "type": "事业单位", "level": "县级", "parent": "", "location": "泸州市江阳区"},
    {"id": 6, "name": "四川省统计科学研究所", "type": "事业单位", "level": "省级", "parent": "四川省统计局", "location": "成都市"},
    {"id": 7, "name": "泸州市江阳区政协", "type": "政协", "level": "县级", "parent": "", "location": "泸州市江阳区"},
    {"id": 8, "name": "泸州市江阳区人大", "type": "人大", "level": "县级", "parent": "", "location": "泸州市江阳区"},
    {"id": 9, "name": "江南科技产业园管委会", "type": "政府", "level": "县级", "parent": "泸州市江阳区人民政府", "location": "泸州市江阳区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "现任区委书记"},
    # Government leaders
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": "区政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "区委常委（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "挂职副区长"},
    {"person_id": 4, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼任四川省统计科学研究所所长"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "民盟盟员，兼区工商联主席"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 6, "org_id": 4, "title": "区公安分局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 10, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "市张坝-方山景区党工委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 周作昂 also serves at provincial level
    {"person_id": 4, "org_id": 6, "title": "四川省统计科学研究所所长", "start_date": "", "end_date": "至今", "rank": "", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Top leadership: Party Secretary ↔ Government Leader
    {"person_a": 1, "person_b": 2, "type": "colleague", "context": "徐兵(区委书记)与袁瑞(区长)在江阳区委、区政府搭档", "overlap_org": "中共泸州市江阳区委员会", "overlap_period": "至今"},

    # 徐兵与区委常委 colleagues
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "徐兵(区委书记)与刘波(区委常委、常务副区长)", "overlap_org": "中共泸州市江阳区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "徐兵(区委书记)与周作昂(区委常委、挂职副区长)", "overlap_org": "中共泸州市江阳区委员会", "overlap_period": "至今"},

    # 袁瑞 with deputy mayors
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "袁瑞(区长)与刘波(常务副区长)在区政府共事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "袁瑞(区长)与杨静喜(副区长)在区政府共事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "袁瑞(区长)与陈文杰(副区长)在区政府共事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "袁瑞(区长)与刘智宇(副区长)在区政府共事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "袁瑞(区长)与奚小淋(区政府党组成员)在区政府共事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},

    # Same native place links (合江县)
    {"person_a": 3, "person_b": 5, "type": "same_native_place", "context": "刘波(合江县)与杨静喜(合江县)同为合江籍", "overlap_org": "", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "same_native_place", "context": "刘波(合江县)与刘智宇(合江县)同为合江籍", "overlap_org": "", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "same_native_place", "context": "杨静喜(合江县)与刘智宇(合江县)同为合江籍", "overlap_org": "", "overlap_period": ""},

    # Same local place links (泸州市)
    {"person_a": 2, "person_b": 9, "type": "same_native_place", "context": "袁瑞(泸州市)与张骋(泸州市)同为泸州人", "overlap_org": "", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "same_native_place", "context": "袁瑞(泸州市)与奚小淋(泸州市)同为泸州人", "overlap_org": "", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "same_native_place", "context": "张骋(泸州市)与奚小淋(泸州市)同为泸州人", "overlap_org": "", "overlap_period": ""},

    # 周作昂 挂职connection
    {"person_a": 4, "person_b": 3, "type": "colleague", "context": "周作昂(挂职副区长)与刘波(常务副区长)在区政府同事", "overlap_org": "泸州市江阳区人民政府", "overlap_period": "至今"},
]

# ── Build ──────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person based on current role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "区长" in role or "县长" in role:
        return "50,100,255"   # Blue — Government leader
    elif "常务" in role:
        return "50,150,255"   # Blue — Senior deputy
    elif "纪委" in role:
        return "255,165,0"    # Orange — Discipline
    else:
        return "100,100,100"  # Grey — Others

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:  return "255,200,200"
    if "政府" in t:  return "200,200,255"
    if "人大" in t:  return "200,255,255"
    if "政协" in t:  return "255,240,200"
    if "事业单位" in t: return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_sqlite(db_path):
    """Build SQLite database."""
    import sqlite3
    conn = sqlite3.connect(db_path)

    # Drop and recreate tables
    for name in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {name}")

    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p.get("birthplace", ""), p["education"], p["party_join"], p.get("work_start", ""),
                      p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  Database written: {db_path}")
    print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def build_gexf(gexf_path):
    """Build GEXF graph using string formatting."""
    from datetime import datetime as dt
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>江阳区领导班子工作关系网络 - {SLUG} Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{hash(pid) % 1000 - 500}" y="{hash(pid[::-1]) % 1000 - 500}" z="0.0"/>')
        lines.append('      </node>')

    # ── Organization nodes ──
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Person→Organization edges (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        period = f"{pos['start_date']} - {pos['end_date']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person edges (relationship)
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        weight = "2.0" if r.get("type") in ("colleague", "superior_subordinate") else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" weight="{weight}" label="{esc(r["context"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {gexf_path}")
    print(f"  - {len(positions)} worked_at edges, {len(relationships)} relationship edges")


def main():
    print(f"Building {SLUG} data...")
    print()

    print("[1/2] Building SQLite database...")
    build_sqlite(DB_PATH)

    print()
    print("[2/2] Building GEXF graph...")
    build_gexf(GEXF_PATH)

    print()
    print("Done. Statistics:")
    print(f"  Database: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Also write person JSONs
    print()
    print("[Post] Writing person JSONs...")
    write_person_jsons()


def write_person_jsons():
    """Write per-person investigation JSON files."""
    persons_dir = STAGING_DIR
    today = TODAY

    # 区委书记 徐兵
    xubing = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "泸州市",
            "region": "江阳区",
            "job": "区委书记",
            "task_id": "sichuan_江阳区",
            "time_focus": "至今"
        },
        "identity": {
            "person_id": "luzhou_jiangyang_xu_bing",
            "name": "徐兵",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "徐兵_",
                "name_birthplace": "徐兵_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共泸州市江阳区委员会",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "至今",
                "org": "中共泸州市江阳区委员会",
                "title": "区委书记",
                "level": "副厅级",
                "location": "泸州市江阳区",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "当前职务，公开资料未找到完整履历",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"id": "org_jyqw", "name": "中共泸州市江阳区委员会", "type": "党委", "role_in_org": "区委书记", "period": "至今"}
        ],
        "relationships": [
            {
                "person": "袁瑞",
                "person_id": "luzhou_jiangyang_yuan_rui",
                "relationship_type": "colleague",
                "strength": "strong",
                "evidence": "徐兵与袁瑞在江阳区委区政府分别担任区委书记和区长，是党政一把手搭档",
                "overlap_org": "江阳区",
                "overlap_period": "至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [
            {
                "period": "",
                "domain": "other",
                "achievement_or_event": "多次主持召开区委常委会、区委理论学习中心组会议",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "江阳区",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料有限，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开信息来源有限",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "total_relationships": 1,
            "strong_connections": 1,
            "medium_connections": 0,
            "weak_connections": 0
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "江阳区官方新闻 - 徐兵主持会议",
                "url": "https://www.jiangyang.gov.cn/zwdt/jyyw/content_123672",
                "publisher": "泸州市江阳区人民政府",
                "published_at": "2026-07-08",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "多个新闻稿确认徐兵以区委书记身份主持会议"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": "徐兵完整的职业生涯、出生信息、教育背景均未获取"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "徐兵担任江阳区委书记之前的职业履历是什么？",
                "why_it_matters": "这是江阳区一把手，核心信息",
                "suggested_queries": ["徐兵 简历 泸州", "徐兵 任前公示", "徐兵 曾任"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "徐兵的出生年月和籍贯是什么？",
                "why_it_matters": "基础身份信息",
                "suggested_queries": ["徐兵 江阳区委书记 出生"],
                "last_attempted": AS_OF
            }
        ]
    }

    # 区长 袁瑞
    yuanrui_person = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "泸州市",
            "region": "江阳区",
            "job": "区长",
            "task_id": "sichuan_江阳区",
            "time_focus": "至今"
        },
        "identity": {
            "person_id": "luzhou_jiangyang_yuan_rui",
            "name": "袁瑞",
            "aliases": [],
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "1980年7月",
            "birthplace": "四川省泸州市",
            "native_place": "四川省泸州市",
            "education": [
                {
                    "period": "",
                    "institution": "电子科技大学",
                    "major": "公共管理",
                    "degree": "硕士",
                    "study_type": "unknown",
                    "source_ids": ["S002"]
                }
            ],
            "party_join": "2002年11月",
            "work_start": "2004年7月",
            "dedupe_keys": {
                "name_birth": "袁瑞_1980",
                "name_birthplace": "袁瑞_泸州市",
                "official_profile_url": "https://www.jiangyang.gov.cn/zfld/content_112764"
            }
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "泸州市江阳区人民政府",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {
                "start": "2004年7月",
                "end": "2004年7月",
                "org": "未知",
                "title": "参加工作",
                "level": "",
                "location": "",
                "system": "unknown",
                "rank": "",
                "is_key_promotion": False,
                "notes": "2004年7月参加工作",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "start": "未知",
                "end": "至今",
                "org": "中共泸州市江阳区委员会",
                "title": "区委副书记",
                "level": "副厅级",
                "location": "泸州市江阳区",
                "system": "party",
                "rank": "",
                "is_key_promotion": True,
                "notes": "现任",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "start": "未知",
                "end": "至今",
                "org": "泸州市江阳区人民政府",
                "title": "区长",
                "level": "副厅级",
                "location": "泸州市江阳区",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "现任，区政府党组书记",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "organizations": [
            {"id": "org_jyqw", "name": "中共泸州市江阳区委员会", "type": "党委", "role_in_org": "区委副书记", "present": True},
            {"id": "org_jyzf", "name": "泸州市江阳区人民政府", "type": "政府", "role_in_org": "区长/党组书记", "present": True}
        ],
        "relationships": [
            {
                "person": "徐兵",
                "person_id": "luzhou_jiangyang_xu_bing",
                "relationship_type": "colleague",
                "strength": "strong",
                "evidence": "袁瑞(区长)与徐兵(区委书记)在江阳区党政一把手搭档",
                "overlap_org": "中共泸州市江阳区委员会",
                "overlap_period": "至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [
            {
                "period": "",
                "domain": "economic_development",
                "achievement_or_event": "领导区政府全面工作，包括审计工作",
                "role_in_event": "区长",
                "measurable_outcome": "",
                "location": "江阳区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["公共管理", "政府管理"],
            "secondary_specializations": ["审计"],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["泸州市"],
            "promotion_velocity": {
                "summary": "公开履历有限，难以完整评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "在安全培训会议、安委会等务实工作中露面",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": [
                "安全生产、高质量发展"
            ],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "total_connections": 6,
            "potential_connections": 6,
            "centrality_notes": "作为区长，与所有副区长直接关联"
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S002",
                "title": "袁瑞 - 泸州市江阳区政府领导",
                "url": "https://www.jiangyang.gov.cn/zfld/content_112764",
                "publisher": "泸州市江阳区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "区政府网站官方领导简介"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "袁瑞在担任江阳区长之前的完整职务晋升路径"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "袁瑞在担任江阳区长之前的历任职务是什么？",
                "why_it_matters": "理解其晋升路径和经验背景",
                "suggested_queries": ["袁瑞 任职经历 江阳区 泸州", "袁瑞 履历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": "袁瑞何时开始担任江阳区长？",
                "why_it_matters": "需要精确任职时间",
                "suggested_queries": ["袁瑞 任江阳区长"],
                "last_attempted": AS_OF
            }
        ]
    }

    # Write files
    for person_data, job, name in [
        (xubing, "区委书记", "徐兵"),
        (yuanrui_person, "区长", "袁瑞")
    ]:
        fname = f"{today}-四川省-泸州市-{job}-{name}.json"
        fpath = os.path.join(str(persons_dir), fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON written: {fpath}")


if __name__ == "__main__":
    main()