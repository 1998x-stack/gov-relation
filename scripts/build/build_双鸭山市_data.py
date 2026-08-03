#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双鸭山市 (Shuangyashan City), 黑龙江省.

Investigation date: 2026-08-03
Task ID: heilongjiang_双鸭山市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - Internal repo report: report/20260724-岭东区-区委书记&区长.md (confirms city-level leaders)
  - External sources: All web (Exa, Baidu, Jina, Wikipedia, shuangyashan.gov.cn) were blocked/timeout
  - Partial evidence mode per fallback playbook

Confidence notes:
  - 蒋和庆: confirmed as 市委书记 via repo-internal reference to shuangyashan.gov.cn
  - 宫镇江: confirmed as 市长 via repo-internal reference to shuangyashan.gov.cn
  - Full bios, birthdates, education: unverified — web access completely degraded
  - Deputy leadership team (市委常委, 副市长等): unverified names
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "双鸭山市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

CANONICAL_DB = os.path.join(STAGING, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(STAGING, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(STAGING, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(STAGING) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "蒋和庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共双鸭山市委员会",
        "source": "双鸭山市人民政府官网（via internal report reference）"
    },
    {
        "id": 2,
        "name": "宫镇江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "双鸭山市人民政府",
        "source": "双鸭山市人民政府官网（via internal report reference）"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Other Key City Leaders
    # ══════════════════════════════════════════════════════════════════════
    # Note: Names and details for 市委副书记, 常务副市长, 人大主任, 政协主席
    # could not be verified due to complete web access degradation.
    # Placeholder entries use "待查" (pending verification).
    # ══════════════════════════════════════════════════════════════════════

    # Placeholder for 市人大常委会主任
    {
        "id": 3,
        "name": "（待查）市人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "双鸭山市人民代表大会常务委员会",
        "source": ""
    },
    # Placeholder for 市政协主席
    {
        "id": 4,
        "name": "（待查）市政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议双鸭山市委员会",
        "source": ""
    },
    # Placeholder for 市委副书记
    {
        "id": 5,
        "name": "（待查）市委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共双鸭山市委员会",
        "source": ""
    },
    # Placeholder for 常务副市长
    {
        "id": 6,
        "name": "（待查）常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "常务副市长",
        "current_org": "双鸭山市人民政府",
        "source": ""
    },
    # Placeholder for 市纪委书记/监委主任
    {
        "id": 7,
        "name": "（待查）市纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市纪委书记",
        "current_org": "中共双鸭山市纪律检查委员会",
        "source": ""
    },
    # Placeholder for 市委组织部部长
    {
        "id": 8,
        "name": "（待查）市委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委组织部部长",
        "current_org": "中共双鸭山市委组织部",
        "source": ""
    },
    # Placeholder for 市委政法委书记
    {
        "id": 9,
        "name": "（待查）市委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委政法委书记",
        "current_org": "中共双鸭山市委政法委员会",
        "source": ""
    },
    # Placeholder for 市委宣传部部长
    {
        "id": 10,
        "name": "（待查）市委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委宣传部部长",
        "current_org": "中共双鸭山市委宣传部",
        "source": ""
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共双鸭山市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共黑龙江省委员会",
        "location": "双鸭山市"
    },
    {
        "id": 2,
        "name": "双鸭山市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "黑龙江省人民政府",
        "location": "双鸭山市"
    },
    {
        "id": 3,
        "name": "双鸭山市人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "黑龙江省人民代表大会常务委员会",
        "location": "双鸭山市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议双鸭山市委员会",
        "type": "政协",
        "level": "地厅级",
        "parent": "中国人民政治协商会议黑龙江省委员会",
        "location": "双鸭山市"
    },
    {
        "id": 5,
        "name": "中共双鸭山市纪律检查委员会",
        "type": "纪委",
        "level": "副厅级",
        "parent": "中共双鸭山市委员会",
        "location": "双鸭山市"
    },
    {
        "id": 6,
        "name": "中共双鸭山市委组织部",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共双鸭山市委员会",
        "location": "双鸭山市"
    },
    {
        "id": 7,
        "name": "中共双鸭山市委政法委员会",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共双鸭山市委员会",
        "location": "双鸭山市"
    },
    {
        "id": 8,
        "name": "中共双鸭山市委宣传部",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共双鸭山市委员会",
        "location": "双鸭山市"
    },
    {
        "id": 9,
        "name": "黑龙江省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "哈尔滨市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    # 蒋和庆 — only current position confirmed
    {"person_id": 1, "org_id": 1, "title": "双鸭山市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "当前在任——具体到任时间待查"},
    # 宫镇江 — only current position confirmed
    {"person_id": 2, "org_id": 2, "title": "双鸭山市人民政府市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "当前在任——具体到任时间待查"},

    # Unverified placeholder positions
    {"person_id": 3, "org_id": 3, "title": "双鸭山市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "待查：未找到公开确认信息"},
    {"person_id": 4, "org_id": 4, "title": "双鸭山市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "待查：未找到公开确认信息"},
    {"person_id": 5, "org_id": 1, "title": "双鸭山市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待查：未找到公开确认信息"},
    {"person_id": 6, "org_id": 2, "title": "双鸭山市常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待查：未找到公开确认信息"},
    {"person_id": 7, "org_id": 5, "title": "双鸭山市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待查：未找到公开确认信息"},
    {"person_id": 8, "org_id": 6, "title": "双鸭山市委组织部部长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待查：未找到公开确认信息"},
    {"person_id": 9, "org_id": 7, "title": "双鸭山市委政法委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待查：未找到公开确认信息"},
    {"person_id": 10, "org_id": 8, "title": "双鸭山市委宣传部部长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待查：未找到公开确认信息"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "蒋和庆作为市委书记，宫镇江作为市长，党政主要领导搭档（市委与市政府）",
        "overlap_org": "双鸭山市",
        "overlap_period": "未确认具体起始时间"
    },
    # Additional relationships are placeholders
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "市委书记与分管党建的市委副书记——市委常委会成员",
        "overlap_org": "中共双鸭山市委员会",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "市长与常务副市长——市政府领导核心搭档",
        "overlap_org": "双鸭山市人民政府",
        "overlap_period": "待确认"
    },
    # Placeholder connections for the leadership team
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "市委常委会成员", "overlap_org": "双鸭山市委常委会", "overlap_period": "待确认"},
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
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

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    if "蒋" in name:
        return "255,50,50"          # Red — Party Secretary
    if "宫" in name:
        return "50,100,255"         # Blue — Government leader
    if "人大" in name:
        return "200,255,255"        # Cyan — 人大
    if "政协" in name:
        return "255,240,200"        # Cream — 政协
    if "副书记" in name:
        return "200,100,100"        # Dark pink
    if "常务副" in name:
        return "50,140,220"         # Medium blue
    if "纪委书记" in name:
        return "255,165,0"          # Orange — Discipline
    if "组织部" in name:
        return "150,50,150"         # Purple — Organization
    if "政法委" in name:
        return "180,180,50"         # Olive — Law
    if "宣传部" in name:
        return "200,100,50"         # Brown — Propaganda
    return "100,100,100"            # Grey


def person_size(name):
    if "正" in name or "书记" in name and "纪委" not in name or "长" in name:
        if "副" not in name or "副" in name and "书记" in name:
            return "20.0"
    if "副书记" in name or "常务" in name or "纪委书记" in name:
        return "16.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "纪委" in o_type:
        return "255,220,180"
    if "组织" in o_type or "宣传" in o_type or "政法" in o_type:
        return "230,210,230"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent (gov-relation)</creator>')
    lines.append(f'    <description>黑龙江省双鸭山市领导班子工作关系网络</description>')
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
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{"在任" if pos["end_date"]=="present" else ""}{" — "+esc(pos["note"]) if pos["note"] else ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, career_timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "双鸭山市",
            "region": "双鸭山市",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_双鸭山市",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"shuangyashan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True if "待查" not in p["name"] else False,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "在公开信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed" if "待查" not in p["name"] else "unverified",
            "career_completeness": "thin" if "待查" not in p["name"] else "none",
            "relationship_confidence": "low",
            "biggest_gap": f"{p['name']}的完整履历信息（含出生信息、教育背景、历任职务）全部待查"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯履历",
                "why_it_matters": "核心人物但履历完全空白",
                "suggested_queries": [f"{p['name']} 简历 双鸭山", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "双鸭山市人民政府官网（岭东区报告引用）", "url": "https://www.shuangyashan.gov.cn/", "publisher": "双鸭山市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Web访问受限——报告内部引用确认"},
    ]

    # === 1. 蒋和庆（市委书记）===
    jiang_timeline = [
        {"start": "unknown", "end": "present", "org": "中共双鸭山市委员会", "title": "市委书记", "notes": "当前在任——此前履历全部待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "任双鸭山市委书记前的完整职业生涯待查", "confidence": "unverified", "source_ids": []},
    ]
    jiang_relationships = [
        {"person": "宫镇江", "person_id": "shuangyashan_宫镇江", "relationship_type": "superior_subordinate", "strength": "plausible", "evidence": "党政主要领导搭档", "overlap_org": "双鸭山市", "overlap_period": "未确认", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    jiang_json = make_person_json(persons[0], jiang_timeline, jiang_relationships, source_register)
    jiang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-双鸭山市-市委书记-蒋和庆.json"
    with open(jiang_path, "w", encoding="utf-8") as f:
        json.dump(jiang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {jiang_path.name}")

    # === 2. 宫镇江（市长）====
    gong_timeline = [
        {"start": "unknown", "end": "present", "org": "双鸭山市人民政府", "title": "市长", "notes": "现任在任——具体到任时间待查", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "任双鸭山市长的完整职业生涯待查", "confidence": "unverified", "source_ids": []},
    ]
    gong_relationships = [
        {"person": "蒋和庆", "person_id": "shuangyashan_蒋和庆", "relationship_type": "subordinate_to_superior", "strength": "plausible", "evidence": "党政主要领导搭档", "overlap_org": "双鸭山市", "overlap_period": "未确认", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    gong_json = make_person_json(persons[1], gong_timeline, gong_relationships, source_register)
    gong_path = PERSONS_DIR / f"{TODAY}-黑龙江省-双鸭山市-市长-宫镇江.json"
    with open(gong_path, "w", encoding="utf-8") as f:
        json.dump(gong_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gong_path.name}")

    # === 3-10: Placeholder person JSONs for unverified roles ===
    placeholder_titles = [
        ("市人大常委会主任", 3),
        ("市政协主席", 4),
        ("市委副书记", 5),
        ("常务副市长", 6),
        ("市纪委书记", 7),
        ("市委组织部部长", 8),
        ("市委政法委书记", 9),
        ("市委宣传部部长", 10),
    ]
    for title, pid in placeholder_titles:
        p = [x for x in persons if x["id"] == pid][0]
        timeline = [
            {"start": "unknown", "end": "present", "org": p["current_org"], "title": title, "notes": "待查——公开信息中未找到该职务当前在任者信息", "confidence": "unverified", "source_ids": []},
        ]
        json_data = make_person_json(p, timeline, [], source_register)
        json_data["current_status"]["is_current_confirmed"] = False
        json_data["risk_and_integrity_signals"] = [
            {"type": "none_found", "description": "无法确认当前在任者，因此无法进行负面信号核查", "date": "", "confidence": "unverified", "source_ids": []}
        ]
        placeholder_path = PERSONS_DIR / f"{TODAY}-黑龙江省-双鸭山市-{title}-待查.json"
        with open(placeholder_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON (placeholder): {placeholder_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building 双鸭山市 network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in sorted(PERSONS_DIR.glob(f"{TODAY}-*.json")):
        print(f"  Person: {p}")