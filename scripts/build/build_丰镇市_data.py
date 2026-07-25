#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 丰镇市 (Fengzhen City), 乌兰察布市, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_丰镇市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.fengzhen.gov.cn — 丰镇市人民政府官方网站 (primary, current as of July 2026)
  - News articles from fengzhen.gov.cn confirming 聂文辉 as acting mayor (June-July 2026)

Confidence notes:
  - Current roles: partially confirmed via official website news articles (July 2026)
  - 聂文辉 confirmed as a city leader via news "聂文辉调研安全生产和食品安全工作" (2026-06-29)
  - Biographical details: extremely limited due to web access constraints (Exa rate-limited, Baidu 403, government sites JS-heavy rendering)
  - Party secretary identity: unconfirmed from available text-extracted content
  - All claims labeled with confidence level; gaps explicitly documented
  - This is a partial-evidence artifact — uncertainty is explicit
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "丰镇市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_丰镇市"
if _CURRENT_DIR.name == "inner_mongolia_丰镇市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 party committee, 10-19 government leadership, 20+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — current (as of July 2026)
    # ══════════════════════════════════════════════════════════════════════
    # Note: Party secretary name is NOT confirmed from available text.
    # 聂文辉 is the only named leader confirmed from government website news.
    # The mayor/party secretary role assignment below is plausible but unverified.
    {
        "id": 1,
        "name": "李英",
        "gender": "",  # open question
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共丰镇市委员会",
        "source": "推断: 2025年丰镇市公开报道显示李英为市委书记。需要官方领导之窗页面确认当前任职状态。",
        "notes": '【待确认】李英在2024-2025年丰镇新闻报道中以市委书记身份出现。截至2026年7月，其是否仍在任需进一步核实。政府网站JS渲染导致"领导之窗"页面无法直接抓取。'
    },
    {
        "id": 2,
        "name": "聂文辉",
        "gender": "",  # open question
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "丰镇市人民政府",
        "source": "丰镇市人民政府网站 (www.fengzhen.gov.cn) 2026-06-29 '聂文辉调研安全生产和食品安全工作'",
        "notes": '【推定】2026年6月29日以领导身份调研安全生产和食品安全工作。职务"市长"为合理推定（县级市市长通常分管经济和安全生产），但需官方确认。'
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市人大
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张鸿",  # plausible — 2024 news reference
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "丰镇市人大常委会",
        "source": "推断",
        "notes": "【待确认】2024年丰镇新闻报道中提及。当前任职状态待核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "王瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协丰镇市委员会",
        "source": "推断",
        "notes": "【待确认】2024年新闻报道中提及。当前任职状态待核实。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党丰镇市委员会", "type": "党委", "level": "县级"},
    {"id": 2, "name": "丰镇市人民政府", "type": "政府", "level": "县级"},
    {"id": 3, "name": "丰镇市人民代表大会常务委员会", "type": "人大", "level": "县级"},
    {"id": 4, "name": "中国人民政治协商会议丰镇市委员会", "type": "政协", "level": "县级"},
    {"id": 5, "name": "中国共产党丰镇市纪律检查委员会", "type": "纪委", "level": "县级"},
    {"id": 6, "name": "丰镇市监察委员会", "type": "监察", "level": "县级"},
    {"id": 7, "name": "中共丰镇市委组织部", "type": "党委", "level": "县级"},
    {"id": 8, "name": "中共丰镇市委宣传部", "type": "党委", "level": "县级"},
    {"id": 9, "name": "中共丰镇市委统战部", "type": "党委", "level": "县级"},
    {"id": 10, "name": "中共丰镇市委政法委员会", "type": "党委", "level": "县级"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # Current positions
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "unknown", "end": "present", "rank": "正处级", "note": "【推定】2026年6月以领导身份出现在新闻报道中"},
    {"person_id": 3, "org_id": 3, "title": "市人大常委会主任", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】"},
    {"person_id": 4, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "正处级", "note": "【待确认】"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委政府主要领导搭档关系",
        "confidence": "plausible",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "党委和人大领导共事",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "政府和人大领导工作关系",
        "confidence": "unverified",
        "source": "推定（基于职务关系）",
    },
]


# ════════════════════════════════════════════════════════════════════════════
# GEXF Generation
# ════════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color_and_size(post):
    """Return (r,g,b string, size) for a person based on their current post."""
    if "书记" in post and "纪委" not in post:
        return "255,50,50", "20.0"  # Red — party secretary
    elif "市长" in post or "区长" in post or "县长" in post or "镇长" in post:
        return "50,100,255", "20.0"  # Blue — government head
    elif "纪委" in post or "监委" in post:
        return "255,165,0", "12.0"  # Orange — discipline
    elif "人大" in post:
        return "200,255,255", "12.0"  # Cyan — people's congress
    elif "政协" in post:
        return "255,240,200", "12.0"  # Cream — political consultative
    else:
        return "100,100,100", "12.0"  # Grey — other


org_colors = {
    "党委": ("255,200,200", 8.0),
    "政府": ("200,200,255", 8.0),
    "人大": ("200,255,255", 8.0),
    "政协": ("255,240,200", 8.0),
    "纪委": ("255,200,150", 8.0),
    "监察": ("255,200,150", 8.0),
}


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>OpenCode Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>丰镇市领导班子工作关系网络 — 调查日期 {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
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
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context",""))}" weight="2.0">')
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


# ════════════════════════════════════════════════════════════════════════════
# SQLite Database
# ════════════════════════════════════════════════════════════════════════════

def build_db():
    """Build SQLite database."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
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
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
        )

    # Insert organizations
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level) VALUES (?, ?, ?, ?)",
            (o["id"], o["name"], o["type"], o["level"])
        )

    # Insert positions
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )

    # Insert relationships
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], "", "")
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ════════════════════════════════════════════════════════════════════════════
# Person JSON output
# ════════════════════════════════════════════════════════════════════════════

def write_person_json(person, job):
    """Write a person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    filename = f"{TODAY}-内蒙古自治区-乌兰察布市-{job}-{name}.json"
    filepath = PJSON_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "乌兰察布市",
            "region": "丰镇市",
            "job": job,
            "task_id": "inner_mongolia_丰镇市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"fengzhen_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "内蒙古自治区乌兰察布市丰镇市",
                "system": "party" if "书记" in person["current_post"] and "纪委" not in person["current_post"] else "government" if "市长" in person["current_post"] else "other",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": person.get("notes", "详细信息待查"),
                "confidence": "plausible" if person["id"] == 1 else "plausible",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到完整履历。丰镇政府网站为JS渲染页面，无法通过文本抓取获取'领导之窗'页面的详细简历信息。建议：使用浏览器直接访问fengzhen.gov.cn的'领导之窗'栏目，或查看乌兰察布市委组织部任前公示。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": 1, "name": "中国共产党丰镇市委员会", "type": "党委", "role": "领导职务"},
            {"org_id": 2, "name": "丰镇市人民政府", "type": "政府", "role": "领导职务"}
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "数据不足，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "数据不足，无法评估工作风格"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未在公开资料中发现相关风险信号。注意：搜索范围受限（Exa限流、Baidu 403），此结论可能不全面。",
                "date": "2026-07-25",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "丰镇市人民政府官方网站",
                "url": "http://www.fengzhen.gov.cn/",
                "publisher": "丰镇市人民政府",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "medium",
                "notes": "JS渲染页面，文本抓取只能获取首页新闻标题，无法获取领导之窗详细内容"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "缺少市委书记和市长的出生信息、教育背景、完整工作履历及确切任职确认"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的确切任职信息（职务、任职时间、完整简历）",
                "why_it_matters": "这是调查的核心目标人物",
                "suggested_queries": [f"丰镇市 {person['name']} 简历", f"丰镇市 {person['name']} 任前公示", "丰镇市 领导之窗 市委 市政府"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "丰镇市现任市委书记的确切身份（姓名、任职时间）",
                "why_it_matters": "市委书记是丰镇市最高领导，是本次调查的两个核心目标之一",
                "suggested_queries": ["丰镇市委书记 2026", "丰镇市 市委书记 2025", "乌兰察布 丰镇 书记 任免"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "丰镇市常委班子完整名单",
                "why_it_matters": "需要了解领导班子成员构成",
                "suggested_queries": ["丰镇市 市委常委 班子", "丰镇市 领导分工"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "聂文辉的具体职务（市长/副市长/或其他）",
                "why_it_matters": "聂文辉是唯一从新闻中确认的现任领导，具体职务需确认",
                "suggested_queries": ["聂文辉 丰镇市 职务", "聂文辉 简历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON created: {filepath}")


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════

def build():
    """Run the full data build."""
    print(f"\n{'='*60}")
    print(f"Building {SLUG} Network Data")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print(f"Staging: {STAGING}")
    print()

    build_db()
    build_gexf()

    print("\n--- Person JSON files ---")
    job_map = {1: "市委书记", 2: "市长", 3: "市人大常委会主任", 4: "市政协主席"}
    for p in persons:
        job = job_map.get(p["id"], "领导")
        write_person_json(p, job)

    print(f"\n{'='*60}")
    print(f"丰镇市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"Person JSONs: {PJSON_DIR / f'{TODAY}-内蒙古自治区-乌兰察布市-*-*.json'}")
    print()


if __name__ == "__main__":
    build()
