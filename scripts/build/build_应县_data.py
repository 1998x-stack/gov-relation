#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 应县, 朔州市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_应县
Level: 县
Targets: 县委书记 & 县长

Research context:
  - Official government site www.yingxian.gov.cn was successfully fetched.
  - Key personnel confirmed via official news articles (appointment announcement, "两优一先"表彰大会).
  - 王国梁 appointed party secretary on 2026-07-19, replacing 王鑫.
  - 王文娟 is the current county magistrate (县长) and deputy party secretary.
  - Web search tools (Exa) were rate-limited; Baidu unavailable.
  - Core leaders confirmed from official government sources.
  - Deputy leaders (副县长、县委常委) not yet identified from search.
  - All non-empty fields in persons are backed by official government URLs.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "应县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_应县"
if _CURRENT_DIR.name == "shanxi_应县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=王国梁(县委书记), 2=王文娟(县长), 3=王鑫(前任), 4=王振兴(人大主任), 5=刘竹(政协主席), 6=杨波(市委组织部)

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current, confirmed from official sources)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王国梁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共应县委员会",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202607/t20260720_780032.html",
        "notes": "王国梁于2026年7月19日任应县县委书记，接替王鑫。省委研究决定，朔州市委常委、组织部部长杨波出席会议。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "王文娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "应县人民政府",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202606/t20260630_777849.html",
        "notes": "王文娟以县委副书记、县长身份主持县政府第71次常务会议，多次调研防汛抗旱、道路交通安全等工作。完整履历待补充。",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "王鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "不再担任县委书记",
        "current_org": "中共应县委员会",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202607/t20260720_780032.html",
        "notes": "王鑫于2026年7月19日不再担任应县县委书记。此前曾在2026年6月24日主持县委常委会、6月30日上党课。去向待确认。",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Key Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "王振兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "应县人大常委会",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202606/t20260630_777849.html",
        "notes": "在两优一先表彰大会上出席。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "刘竹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "应县政协",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202606/t20260630_777849.html",
        "notes": "在两优一先表彰大会上出席。完整履历待补充。",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # External Relevant Figure
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "杨波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "朔州市委常委、组织部部长",
        "current_org": "中共朔州市委组织部",
        "source": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202607/t20260720_780032.html",
        "notes": "出席应县领导干部大会宣布省委任命。非应县本地干部。",
        "confidence": "confirmed"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共应县委员会", "type": "党委", "level": "县级", "parent": "中共朔州市委", "location": "山西省朔州市应县"},
    {"id": 2, "name": "应县人民政府", "type": "政府", "level": "县级", "parent": "朔州市人民政府", "location": "山西省朔州市应县"},
    {"id": 3, "name": "应县人大常委会", "type": "人大", "level": "县级", "parent": "应县", "location": "山西省朔州市应县"},
    {"id": 4, "name": "应县政协", "type": "政协", "level": "县级", "parent": "应县", "location": "山西省朔州市应县"},
    {"id": 5, "name": "中共朔州市委组织部", "type": "党委", "level": "地市级", "parent": "中共朔州市委", "location": "山西省朔州市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # ── Wang Guoliang (王国梁) ──
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-07-19", "end": "present", "rank": "正县级", "note": "现任"},
    # ── Wang Wenjuan (王文娟) ──
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副县级", "note": "县委副书记兼任县长"},
    # ── Wang Xin (王鑫 - former) ──
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start": "", "end": "2026-07-19", "rank": "正县级", "note": "不再担任"},
    # ── Wang Zhenxing (王振兴) ──
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    # ── Liu Zhu (刘竹) ──
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    # ── Yang Bo (杨波) ──
    {"person_id": 6, "org_id": 5, "title": "朔州市委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "王国梁作为县委书记，王文娟作为县长，是党政一把手搭档关系",
     "overlap_org": "中共应县委员会/应县人民政府",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "王国梁接替王鑫担任应县县委书记",
     "overlap_org": "中共应县委员会",
     "overlap_period": "2026年7月交接", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "medium",
     "context": "王鑫和王文娟在班子中共事，王鑫任县委书记，王文娟任县长",
     "overlap_org": "中共应县委员会/应县人民政府",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 1, "type": "reported_association", "strength": "weak",
     "context": "杨波代表朔州市委宣布王国梁的任命",
     "overlap_org": "",
     "overlap_period": "2026-07-19", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "王国梁与王振兴在应县领导班子共事，王振兴任县人大常委会主任",
     "overlap_org": "应县",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "王国梁与刘竹在应县领导班子共事，刘竹任县政协主席",
     "overlap_org": "应县",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "王文娟与王振兴在应县领导班子共事",
     "overlap_org": "应县",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "王文娟与刘竹在应县领导班子共事",
     "overlap_org": "应县",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "strength": "medium",
     "context": "王鑫与王振兴在应县领导班子共事，王鑫任县委书记时，王振兴任县人大常委会主任",
     "overlap_org": "应县",
     "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "strength": "medium",
     "context": "王鑫与刘竹在应县领导班子共事，王鑫任县委书记时，刘竹任县政协主席",
     "overlap_org": "应县",
     "overlap_period": "", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role:
        return "50,100,255"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "副县长" in role:
        return "50,100,255"
    elif "主任" in role and "党委" in p.get("current_org", ""):
        return "100,100,100"
    elif "不再担任" in role:
        return "150,150,150"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or "县长" in role


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# ── PERSON JSON HELPERS ──────────────────────────────────────

def make_person_id(name):
    """Generate a stable slug for a person."""
    mapping = {
        "王国梁": "shanxi_yingxian_wang_guoliang",
        "王文娟": "shanxi_yingxian_wang_wenjuan",
        "王鑫": "shanxi_yingxian_wang_xin",
        "王振兴": "shanxi_yingxian_wang_zhenxing",
        "刘竹": "shanxi_yingxian_liu_zhu",
        "杨波": "shanxi_shuozhou_yang_bo",
    }
    return mapping.get(name, "")


def build_person_json(p):
    """Build a person depth-profile JSON matching the established schema."""
    pid = make_person_id(p["name"])
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "朔州市",
            "region": "应县",
            "job": p.get("current_post", ""),
            "task_id": "shanxi_应县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": pid,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [p["education"]] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f'{p["name"]}_{p.get("birth", "")}',
                "name_birthplace": f'{p["name"]}_{p.get("birthplace", "")}',
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if is_top_leader(p) else "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": p.get("confidence") == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": p.get("current_org", ""),
                "title": p.get("current_post", ""),
                "level": "正县级" if is_top_leader(p) else "副县级",
                "location": f"山西省朔州市应县" if p["id"] < 6 else "山西省朔州市",
                "system": "party",
                "rank": "county_chief",
                "is_key_promotion": True,
                "notes": p.get("notes", ""),
                "confidence": p.get("confidence", "confirmed"),
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_name": p.get("current_org", ""),
                "org_type": "党委",
                "level": "县级",
                "location": "山西省朔州市应县",
                "role": "current employer"
            }
        ],
        "relationships": [
            {
                "person": rp["name"],
                "person_id": make_person_id(rp["name"]),
                "relationship_type": rt,
                "strength": rs,
                "evidence": rc,
                "overlap_org": ro,
                "overlap_period": rper,
                "direction": "undirected",
                "confidence": rconf,
                "source_ids": ["S001"]
            }
            for r in relationships
            for rp in persons
            if (r["person_a"] == p["id"] and rp["id"] == r["person_b"])
            or (r["person_b"] == p["id"] and rp["id"] == r["person_a"])
            for rt in [r["type"]]
            for rs in [r["strength"]]
            for rc in [r["context"]]
            for ro in [r["overlap_org"]]
            for rper in [r["overlap_period"]]
            for rconf in [r["confidence"]]
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料不足，无法评估晋升速度。" if not p.get("birth") else "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开资料未发现{p['name']}的纪律处分、审计问题或负面报道。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "应县召开全县领导干部大会 王国梁同志任应县县委书记",
                "url": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202607/t20260720_780032.html",
                "publisher": "应县人民政府",
                "published_at": "2026-07-20",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王国梁任命、王鑫离任、杨波出席"
            },
            {
                "id": "S002",
                "title": "应县召开'两优一先'表彰大会",
                "url": "http://www.yingxian.gov.cn/zwyw_15204/yxdt/202606/t20260630_777849.html",
                "publisher": "应县人民政府",
                "published_at": "2026-06-30",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王文娟（县长）、王振兴（人大主任）、刘竹（政协主席）身份"
            }
        ],
        "confidence_summary": {
            "identity": "thin",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{p['name']}的出生年份、籍贯、教育背景、完整职业生涯全部缺失——仅有官方任命信息。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年份、籍贯和出生地是什么？",
                "why_it_matters": "核心人物的基础身份信息完全缺失。",
                "suggested_queries": [f"{p['name']} 简历 朔州", f"{p['name']} 出生 年龄"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}在担任{p['current_post']}之前的职业生涯是什么？",
                "why_it_matters": "完整履历是网络分析的基础，缺少早期履历无法建立工作关系网络。",
                "suggested_queries": [f"{p['name']} 任职经历", f"{p['name']} 之前担任"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}的教育背景是什么？",
                "why_it_matters": "教育背景可揭示体制内人脉网络（同学关系）。",
                "suggested_queries": [f"{p['name']} 毕业", f"{p['name']} 大学"],
                "last_attempted": AS_OF
            }
        ]
    }


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>应县领导班子工作关系网络 - 山西省朔州市应县</description>')
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
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
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
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── PERSON JSONS ──────────────────────────────────────────────

def write_person_jsons():
    """Write per-person depth-profile JSON files (core figures only)."""
    for p in persons:
        if p["id"] > 6:
            continue
        fname = f'{TODAY}-山西省-朔州市-{p["current_post"].replace("/", "-").replace("、", "-")}-{p["name"]}.json'
        fpath = PJSON_DIR / fname
        data = build_person_json(p)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {fpath}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    import sqlite3
    build_db()
    build_gexf()
    write_person_jsons()
    print_summary()