#!/usr/bin/env python3
"""Build 凉城县 leadership network database and GEXF graph.

Generated from official sources at https://www.liangcheng.gov.cn/
Data as of 2026-07-25.
"""

import sqlite3
import os
from datetime import datetime

# Paths: script lives at data/tmp/inner_mongolia_凉城县/
TMPDIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(TMPDIR, "凉城县_network.db")
GEXF_PATH = os.path.join(TMPDIR, "凉城县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "崔景翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "", "education": "研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1971157.html"},
    {"id": 2, "name": "张广", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "", "education": "大学本科，管理学学士",
     "party_join": "", "work_start": "",
     "current_post": "县委副书记、政府县长候选人", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1606773.html"},
    {"id": 3, "name": "郑东平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原县长（已离任）", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfwj/1830993.html"},
    {"id": 4, "name": "李志刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委副书记、政法委书记", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1606699.html"},
    {"id": 5, "name": "王俊勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1606689.html"},
    {"id": 6, "name": "张文娟", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共凉城县纪律检查委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1606697.html"},
    {"id": 7, "name": "赵日斌", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、人武部政治委员", "current_org": "凉城县人民武装部",
     "source": "https://www.liangcheng.gov.cn/swld/1606685.html"},
    {"id": 8, "name": "高鹏飞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1824947.html"},
    {"id": 9, "name": "翟纪庆", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、政府副县长", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1606751.html"},
    {"id": 10, "name": "贾宇飞", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、县委办主任", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1606683.html"},
    {"id": 11, "name": "马小龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1606693.html"},
    {"id": 12, "name": "许星", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/swld/1975763.html"},
    {"id": 13, "name": "王蕾", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1606747.html"},
    {"id": 14, "name": "陈晓峰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、公安局局长", "current_org": "凉城县公安局",
     "source": "https://www.liangcheng.gov.cn/zfld/1606743.html"},
    {"id": 15, "name": "贾志刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1606765.html"},
    {"id": 16, "name": "康伟喆", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfld/1817439.html"},
    {"id": 17, "name": "白利军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原县委常委、常务副县长（已调整）", "current_org": "凉城县人民政府",
     "source": "https://www.liangcheng.gov.cn/zfwj/1830993.html"},
    {"id": 18, "name": "赵建军", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-08", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "人大常委会党组书记、主任", "current_org": "凉城县人民代表大会常务委员会",
     "source": "https://www.liangcheng.gov.cn/rdld/1606727.html"},
    {"id": 19, "name": "赵瑞", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-09", "birthplace": "", "education": "在职研究生学历",
     "party_join": "", "work_start": "",
     "current_post": "政协主席", "current_org": "中国人民政治协商会议凉城县委员会",
     "source": "https://www.liangcheng.gov.cn/zxld/1606811.html"},
]

organizations = [
    {"id": 101, "name": "中共凉城县委员会", "type": "党委", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 102, "name": "凉城县人民政府", "type": "政府", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 103, "name": "中共凉城县纪律检查委员会", "type": "党委", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 104, "name": "凉城县人民武装部", "type": "政府", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 105, "name": "凉城县公安局", "type": "政府", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 106, "name": "凉城县人民代表大会常务委员会", "type": "人大", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
    {"id": 107, "name": "中国人民政治协商会议凉城县委员会", "type": "政协", "level": "县",
     "location": "内蒙古自治区乌兰察布市凉城县"},
]

positions = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持县委全面工作"},
    {"person_id": 2, "org_id": 102, "title": "政府县长候选人", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持县人民政府全面工作"},
    {"person_id": 2, "org_id": 101, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "", "note": ""},
    {"person_id": 3, "org_id": 102, "title": "县长", "start_date": "", "end_date": "2025-06",
     "rank": "正处级", "note": "已在2025年6月前离任"},
    {"person_id": 3, "org_id": 101, "title": "县委副书记", "start_date": "", "end_date": "2025-06",
     "rank": "", "note": ""},
    {"person_id": 4, "org_id": 101, "title": "县委副书记、政法委书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 101, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 103, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 104, "title": "县委常委、人武部政治委员", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 102, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 102, "title": "县委常委、政府副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 101, "title": "县委常委、县委办主任", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 101, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 101, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 102, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责民政、市场监管、卫生健康等"},
    {"person_id": 14, "org_id": 105, "title": "副县长、公安局局长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责公安、司法、信访等"},
    {"person_id": 14, "org_id": 102, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 102, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责农牧业、乡村振兴、水利等"},
    {"person_id": 16, "org_id": 102, "title": "副县长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "负责生态环境、退役军人、数据管理等"},
    {"person_id": 17, "org_id": 102, "title": "县委常委、常务副县长", "start_date": "", "end_date": "2025-06",
     "rank": "副处级", "note": "已调整，由高鹏飞接任常务副县长"},
    {"person_id": 18, "org_id": 106, "title": "人大常委会党组书记、主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 107, "title": "政协主席", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
]

relationships = [
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor",
     "context": "郑东平离任凉城县县长，张广接任县长候选人",
     "overlap_org": "凉城县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "崔景翔（县委书记）与张广（县长候选人）为党政正职搭档",
     "overlap_org": "凉城县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "崔景翔（县委书记）与郑东平（原县长）为前党政正职搭档",
     "overlap_org": "凉城县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "贾宇飞任县委办主任，与县委书记日常工作关系密切",
     "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "同属中共凉城县委员会常委班子", "overlap_org": "中共凉城县委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "高鹏飞（常务副县长）协助张广（县长候选人）主持政府常务工作",
     "overlap_org": "凉城县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "翟纪庆（副县长）协助张广（县长候选人）工作",
     "overlap_org": "凉城县人民政府", "overlap_period": "2026-"},
    {"person_a": 17, "person_b": 8, "type": "predecessor_successor",
     "context": "高鹏飞接替白利军担任县委常委、常务副县长",
     "overlap_org": "凉城县人民政府", "overlap_period": "2025-2026"},
]

# ── DB BUILD ─────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS persons (
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
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT DEFAULT '',
    level TEXT DEFAULT '',
    parent TEXT DEFAULT '',
    location TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS positions (
    person_id INTEGER,
    org_id INTEGER,
    title TEXT DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    rank TEXT DEFAULT '',
    note TEXT DEFAULT '',
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    person_a INTEGER,
    person_b INTEGER,
    type TEXT DEFAULT '',
    context TEXT DEFAULT '',
    overlap_org TEXT DEFAULT '',
    overlap_period TEXT DEFAULT '',
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
"""


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return viz color for person based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post:
        return "255,50,50"  # Red for Party Secretary
    if "县长" in post or "县长候选人" in post:
        return "50,100,255"  # Blue for Government
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"  # Orange for Discipline
    if "常务副" in post:
        return "50,150,255"  # Light blue for executive deputy
    return "100,100,100"  # Grey for others


def person_size(p):
    post = p.get("current_post", "")
    if "县委书记" in post or "县长" in post or "县长候选人" in post:
        return "20.0"
    return "12.0"


def is_top_leader(pid):
    return pid in (1, 2, 3)


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def org_size(o):
    return "8.0"


def build_db():
    conn = sqlite3.connect(DB_PATH)
    for statement in SCHEMA_SQL.split(";"):
        s = statement.strip()
        if s:
            conn.execute(s)

    # Insert persons
    cols = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
            "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        values = [p.get(c, "") for c in cols]
        conn.execute(
            f"INSERT INTO persons ({','.join(cols)}) VALUES ({','.join(['?'] * len(cols))})",
            values,
        )

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "location"]
    for o in organizations:
        values = [o.get(c, "") for c in cols_o]
        conn.execute(
            f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
            values,
        )

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        values = [pos.get(c, "") for c in cols_pos]
        conn.execute(
            f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
            values,
        )

    # Insert relationships
    cols_rel = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        values = [r.get(c, "") for c in cols_rel]
        conn.execute(
            f"INSERT INTO relationships ({','.join(cols_rel)}) VALUES ({','.join(['?'] * len(cols_rel))})",
            values,
        )

    conn.commit()
    conn.close()

    print(f"DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    print(f"DB file: {DB_PATH}")
    print(f"  size: {os.path.getsize(DB_PATH)} bytes")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>凉城县领导工作关系网络 — {datetime.now().strftime("%Y-%m-%d")}</description>')
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
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        pid = p["id"]
        post = esc(p.get("current_post", ""))
        name = esc(p["name"])
        lines.append(f'      <node id="p{pid}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{post}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        name = esc(o["name"])
        oid = o["id"]
        lines.append(f'      <node id="o{oid}" label="{name}">')
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
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = esc(pos.get("title", ""))
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{title}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        pa = r["person_a"]
        pb = r["person_b"]
        ctx = esc(r.get("context", ""))
        rel_type = esc(r.get("type", ""))
        oo = esc(r.get("overlap_org", ""))
        op = esc(r.get("overlap_period", ""))
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{rel_type}"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append(f'          <attvalue for="2" value="{oo}"/>')
        lines.append(f'          <attvalue for="3" value="{op}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"GEXF: {len(persons) + len(organizations)} nodes, {eid} edges")
    print(f"GEXF file: {GEXF_PATH}")
    print(f"  size: {os.path.getsize(GEXF_PATH)} bytes")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
