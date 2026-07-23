#!/usr/bin/env python3
"""Build 正定县 (Zhengding County, Shijiazhuang) leadership network data.

Level: 县
Province: 河北省
Parent city: 石家庄市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_正定县

Research date: 2026-07-23
Official source: https://www.zd.gov.cn/ (正定县人民政府 — accessible)

Current status (as of 2026-07-23):
- 县委书记: 王俊红 (Wang Junhong) — 石家庄市委常委兼任正定县委书记
  * 2021年8月由邢台清河县委书记调任正定县委书记
  * 2021年8月当选石家庄市委常委
  * 2021年6月获评"全国优秀县委书记"（103人之一）
  * 2026年3月仍以"石家庄市委常委、正定县委书记"身份公开出席活动
- 县长: 李万里 (Li Wanli) — 2026年2月当选正定县县长
  * 正定县十七届人大七次会议选举产生

Research limitations:
  - Exa search API: rate-limited
  - Baidu: 403 blocked
  - Google: blocked/unreachable
  - Jina Reader: timeout
  - CCTV search: limited bio detail for county-level officials
  - 正定县政府网站领导之窗页面无法访问 (404)

Known evidence:
  - 王俊红: 央视网新闻多次报道 (2022-2026)，人民日报2026-03-19报道
  - 李万里: 石家庄市调研报告中确认2026年2月当选

All unverified claims labeled as such. Biographical details (birth year, birthplace,
education, early career) for both leaders are unverified pending deeper research.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

SLUG = "正定县"
TASK_ID = "hebei_正定县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID
AS_OF = "2026-07-23"

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = TMP_DIR

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王俊红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石家庄市委常委、正定县委书记",
        "current_org": "中共石家庄市委员会/中共正定县委员会",
        "source": "央视网新闻 — '心底无私天地宽' 2026-03-19; 网易新闻 — '新任正定县委书记王俊红当选石家庄市委常委' 2021-08-18",
    },
    # ════════════════════════════════════════
    # 县政府领导 (Government Leadership)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "李万里",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "正定县县长",
        "current_org": "正定县人民政府",
        "source": "石家庄市调研报告 (report/20260714-石家庄市-市委书记市长.md) — 2026年2月当选",
    },
    # ════════════════════════════════════════
    # 其他领导班子成员 (Other Leadership — placeholder/待确认)
    # 因网络搜索限制，未能在公开渠道确认其他常委和副县长信息
    # ════════════════════════════════════════
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共正定县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市正定县",
    },
    {
        "id": 2,
        "name": "正定县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市正定县常山西路1号",
    },
    {
        "id": 3,
        "name": "正定县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "石家庄市人大常委会",
        "location": "河北省石家庄市正定县",
    },
    {
        "id": 4,
        "name": "正定县政协",
        "type": "政协",
        "level": "县",
        "parent": "石家庄市政协",
        "location": "河北省石家庄市正定县",
    },
    {
        "id": 5,
        "name": "中共石家庄市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共河北省委员会",
        "location": "河北省石家庄市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王俊红
    {
        "person_id": 1,
        "org_id": 1,
        "title": "正定县委书记",
        "start_date": "2021-08",
        "end_date": "present",
        "rank": "副厅级（兼任石家庄市委常委）",
        "note": "2021年8月由邢台清河县委书记调任正定县委书记；2021年6月获评全国优秀县委书记；2021年8月当选石家庄市委常委",
    },
    {
        "person_id": 1,
        "org_id": 5,
        "title": "石家庄市委常委",
        "start_date": "2021-08",
        "end_date": "present",
        "rank": "副厅级",
        "note": "2021年8月当选石家庄市委常委兼任正定县委书记",
    },
    # 邢台清河县委书记 (previous role, outside network)
    # 李万里
    {
        "person_id": 2,
        "org_id": 2,
        "title": "正定县县长",
        "start_date": "2026-02",
        "end_date": "present",
        "rank": "正处级",
        "note": "2026年2月正定县十七届人大七次会议选举产生",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "正定县委书记与县长党政搭档",
        "overlap_org": "中共正定县委员会/正定县人民政府",
        "overlap_period": "2026-02至今",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "县长" in cp or "区长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and ("县长" in cp or "区长" in cp):
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "县长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


# ══════════════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════


def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
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

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>正定县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
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
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "石家庄市",
            "region": "正定县",
            "job": p.get("current_post", ""),
            "task_id": "hebei_正定县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"zhengding_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科", f"{p['name']} 出生"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "正定县人民政府门户网站",
         "url": "https://www.zd.gov.cn/", "publisher": "正定县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Active government portal — leadership page (领导之窗) 404"},
        {"id": "S002", "title": "央视网 — 心底无私天地宽(创造经得起实践、人民、历史检验的实绩)",
         "url": "https://search.cctv.com/", "publisher": "央视网",
         "published_at": "2026-03-19",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
         "notes": "Confirmed 王俊红 as 正定县委书记 as of March 2026"},
        {"id": "S003", "title": "网易新闻 — 新任正定县委书记王俊红当选石家庄市委常委",
         "url": "https://www.163.com/", "publisher": "澎湃新闻/网易",
         "published_at": "2021-08-18",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
         "notes": "Confirmed 王俊红 transition from 清河县委书记 to 正定县委书记 in Aug 2021"},
        {"id": "S004", "title": "石家庄市领导班子调研报告",
         "url": "", "publisher": "Gov-Relation Research",
         "published_at": "2026-07-14",
         "accessed_at": AS_OF, "source_type": "database", "reliability": "medium",
         "notes": "Confirmed 李万里 as 正定县长, elected Feb 2026"},
    ]

    # ── 王俊红 person JSON ──
    wjh_timeline = [
        {"start": "2021-08", "end": "present",
         "org": "中共正定县委员会",
         "title": "正定县委书记", "level": "副厅级",
         "location": "河北省石家庄市正定县", "system": "party",
         "rank": "副厅级（兼任石家庄市委常委）", "is_key_promotion": True,
         "notes": "由邢台清河县委书记调任；2021年6月获评全国优秀县委书记",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "2021-08", "end": "present",
         "org": "中共石家庄市委员会",
         "title": "石家庄市委常委", "level": "副厅级",
         "location": "河北省石家庄市", "system": "party",
         "rank": "副厅级", "is_key_promotion": True,
         "notes": "兼任正定县委书记",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "清河县委/邢台市",
         "title": "清河县委书记（此前）",
         "notes": "公开资料显示2021年6月以清河县委书记身份获评全国优秀县委书记，此前完整履历未查到",
         "confidence": "plausible",
         "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到王俊红任清河县委书记之前的完整履历（出生年月、籍贯、教育背景、早期任职等均缺失）",
         "confidence": "unverified",
         "source_ids": []},
    ]
    wjh_relationships = [
        {"person": "李万里", "person_id": "zhengding_李万里",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "正定县委书记与县长党政搭档",
         "overlap_org": "中共正定县委员会/正定县人民政府",
         "overlap_period": "2026-02至今",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
    ]
    wjh_json = build_person_json(persons[0], wjh_timeline, wjh_relationships, sources)
    wjh_path = PERSONS_DIR / f"{now}-河北省-石家庄市-县委书记-王俊红.json"
    with open(wjh_path, "w", encoding="utf-8") as f:
        json.dump(wjh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wjh_path}")

    # ── 李万里 person JSON ──
    lwl_timeline = [
        {"start": "2026-02", "end": "present",
         "org": "正定县人民政府",
         "title": "正定县县长", "level": "正处级",
         "location": "河北省石家庄市正定县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "2026年2月正定县十七届人大七次会议选举产生",
         "confidence": "confirmed",
         "source_ids": ["S004"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到李万里任正定县长之前的完整履历（出生年月、籍贯、教育背景、此前职务等均缺失）",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lwl_relationships = [
        {"person": "王俊红", "person_id": "zhengding_王俊红",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "正定县长与县委书记党政搭档",
         "overlap_org": "正定县人民政府/中共正定县委员会",
         "overlap_period": "2026-02至今",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S004"]},
    ]
    lwl_json = build_person_json(persons[1], lwl_timeline, lwl_relationships, sources)
    lwl_json["investigation_scope"]["job"] = "县长"
    lwl_path = PERSONS_DIR / f"{now}-河北省-石家庄市-县长-李万里.json"
    with open(lwl_path, "w", encoding="utf-8") as f:
        json.dump(lwl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lwl_path}")


def build():
    """Main build function."""
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {TMP_DIR}")
    print(f"Research date: {AS_OF}")
    print()

    build_db()
    print()

    build_gexf()
    print()

    build_person_jsons()
    print()

    print("=== Build complete ===")
    print(f"DB:    {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")
    print(f"JSONs: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
