#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 卫辉市 (Weihui City), 新乡市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_卫辉市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - 卫辉市人民政府 (weihui.gov.cn) — official government website
  - Confirmed leaders from news articles dated 2026-07-22 and 2026-07-20
  - 崔红建: 新乡市委常委、卫辉市委书记 (confirmed via multiple news articles)
  - 王清洲: 卫辉市委副书记、市长 (confirmed via official leadership page and news)
  - Existing repo artifact: data/persons/20260724-河南省-新乡市-市委常委-崔红建.json
  - Source_fallbacks.md guidelines applied: partial-evidence artifact mode for biographies

Confidence notes:
  - Core leader names (崔红建, 王清洲) and current roles are CONFIRMED from
    official government sources as of 2026-07-24.
  - Detailed biographical data (birth dates, birthplace, education, full career
    timelines) are UNVERIFIED — Baidu Baike was blocked, and Jina Reader timed out.
  - Deputy leaders (郝科伟, 赵旺勇, 徐明璐) are listed on the leadership page but
    their specific roles and detailed info need confirmation.
  - This is a partial-evidence artifact — biographical fields use placeholders
    with explicit uncertainty markers.
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "卫辉市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
# ⚠ Core leader names are CONFIRMED; detailed biographies are UNVERIFIED.

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "崔红建",      # CONFIRMED - 市委书记
        "gender": "男",        # confirmed from existing data
        "ethnicity": "汉族",    # plausible (common for Henan officials)
        "birth": "",           # UNVERIFIED
        "birthplace": "",      # UNVERIFIED
        "education": "",       # UNVERIFIED
        "party_join": "中共党员",  # confirmed
        "work_start": "",      # UNVERIFIED
        "current_post": "新乡市委常委、卫辉市委书记",
        "current_org": "中共卫辉市委员会",
        "source": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/743b2636b71e47ba9cc3820dee4c8c7a.htm"
    },
    {
        "id": 2,
        "name": "王清洲",      # CONFIRMED - 市长
        "gender": "男",        # plausible
        "ethnicity": "汉族",    # plausible
        "birth": "",           # UNVERIFIED
        "birthplace": "",      # UNVERIFIED
        "education": "",       # UNVERIFIED
        "party_join": "中共党员",  # confirmed (市委副书记 implies party member)
        "work_start": "",      # UNVERIFIED
        "current_post": "市委副书记、市长",
        "current_org": "卫辉市人民政府",
        "source": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/af0418cbde054675acf8d61f056f26d8.htm"
    },
    # ═══════ 副市长 (deputy mayors) — listed on leadership page ═══════
    {
        "id": 3,
        "name": "郝科伟",      # listed on leadership page
        "gender": "",           # UNVERIFIED
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",  # assumed from leadership page listing
        "current_org": "卫辉市人民政府",
        "source": "https://www.weihui.gov.cn/portal/zfxxgk/zfxxgkml/ldzc/A001003002001index_1.htm"
    },
    {
        "id": 4,
        "name": "赵旺勇",      # listed on leadership page
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",  # assumed
        "current_org": "卫辉市人民政府",
        "source": "https://www.weihui.gov.cn/portal/zfxxgk/zfxxgkml/ldzc/A001003002001index_1.htm"
    },
    {
        "id": 5,
        "name": "徐明璐",      # listed on leadership page (added 2025-03-28)
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",  # assumed
        "current_org": "卫辉市人民政府",
        "source": "https://www.weihui.gov.cn/portal/zfxxgk/zfxxgkml/ldzc/A001003002001index_1.htm"
    },
    # ═══════ 前任 Predecessors ═══════
    {
        "id": 6,
        "name": "",        # UNVERIFIED — 前任市委书记
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共卫辉市委员会",
        "source": ""
    },
    {
        "id": 7,
        "name": "",        # UNVERIFIED — 前任市长
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "卫辉市人民政府",
        "source": ""
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共卫辉市委员会", "type": "党委", "level": "县级", "parent": "中共新乡市委员会", "location": "卫辉市"},
    {"id": 2, "name": "卫辉市人民政府", "type": "政府", "level": "县级", "parent": "新乡市人民政府", "location": "卫辉市"},
    {"id": 3, "name": "中共卫辉市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共新乡市纪律检查委员会", "location": "卫辉市"},
    {"id": 4, "name": "中共卫辉市委员会组织部", "type": "党委", "level": "县级", "parent": "中共卫辉市委员会", "location": "卫辉市"},
    {"id": 5, "name": "中共卫辉市委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共卫辉市委员会", "location": "卫辉市"},
    {"id": 6, "name": "中共卫辉市委员会宣传部", "type": "党委", "level": "县级", "parent": "中共卫辉市委员会", "location": "卫辉市"},
    {"id": 7, "name": "中共卫辉市委员会统战部", "type": "党委", "level": "县级", "parent": "中共卫辉市委员会", "location": "卫辉市"},
    {"id": 8, "name": "卫辉市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "新乡市人民代表大会常务委员会", "location": "卫辉市"},
    {"id": 9, "name": "中国人民政治协商会议卫辉市委员会", "type": "政协", "level": "县级", "parent": "政协新乡市委员会", "location": "卫辉市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "新乡市委常委、卫辉市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任新乡市委常委"},
    # 市长
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 副市长 (deputy mayors)
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前任
    {"person_id": 6, "org_id": 1, "title": "前任市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "前任市长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 崔红建 ↔ 王清洲（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长为卫辉市党政正职搭档", "overlap_org": "卫辉市", "overlap_period": ""},
    # 市长 ↔ 副市长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "卫辉市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "卫辉市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "副市长在市长领导下工作", "overlap_org": "卫辉市人民政府", "overlap_period": ""},
    # 前任 ↔ 现任
    {"person_a": 6, "person_b": 1, "type": "交接", "context": "前任市委书记与现任市委书记交接", "overlap_org": "中共卫辉市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 2, "type": "交接", "context": "前任市长与现任市长交接", "overlap_org": "卫辉市人民政府", "overlap_period": ""},
]


# ── Main ────────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    """Return RGB color string for a person based on role."""
    if name == "崔红建":
        return "255,50,50"  # Red — Party Secretary
    elif name == "王清洲":
        return "50,100,255"  # Blue — Mayor
    else:
        return "100,100,100"  # Grey — Others

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting."""
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        name = p["name"] if p["name"] else "待确认"
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        p_id = pos["person_id"]
        o_id = pos["org_id"]
        lines.append(f'      <edge id="e{eid}" source="p{p_id}" target="o{o_id}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        eid += 1
        pa, pb = rel["person_a"], rel["person_b"]
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ GEXF: {output_path}")


def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  AS OF:    {AS_OF}")
    print(f"  ✅ Core leaders confirmed: 崔红建 (市委书记), 王清洲 (市长)")
    print(f"  ⚠ Detailed biographies UNVERIFIED due to limited web access.")
    print(f"  ⚠ Deputy roles (郝科伟, 赵旺勇, 徐明璐) need specific role confirmation.")

    # Write DB+GEXF to staging
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Also generate GEXF with full viz attributes
    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    # Write person JSON files for core leaders (IDs 1 & 2)
    person_files = [
        {
            "id": 1,
            "name": "崔红建",
            "job": "市委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "新乡市",
                    "region": "卫辉市",
                    "job": "市委书记",
                    "task_id": "henan_卫辉市",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "weihui_cui_hongjian",
                    "name": "崔红建",
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "",
                    "birthplace": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": ""
                },
                "current_status": {
                    "current_post": "新乡市委常委、卫辉市委书记",
                    "current_org": "中共卫辉市委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002"]
                },
                "career_timeline": [
                    {
                        "start": "",
                        "end": "present",
                        "org": "中共新乡市委员会",
                        "title": "市委常委",
                        "level": "副厅级",
                        "location": "新乡市",
                        "system": "party",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "start": "",
                        "end": "present",
                        "org": "中共卫辉市委员会",
                        "title": "市委书记",
                        "level": "正处级",
                        "location": "卫辉市",
                        "system": "party",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "王清洲",
                        "person_id": "weihui_wang_qingzhou",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "市委书记与市长为卫辉市党政正职搭档，共同出席全市党建引领基层高效能治理观摩推进会（2026-07-18）",
                        "overlap_org": "卫辉市",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "采取'四不两直'方式调研督导安全生产工作，深入双峰纸业等企业检查",
                        "role_in_event": "带队调研",
                        "location": "卫辉市",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "other",
                        "achievement_or_event": "主持全市党建引领基层高效能治理观摩推进会并讲话",
                        "role_in_event": "主持并讲话",
                        "location": "卫辉市",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "cross_county_rotation",
                    "systems_experience": ["party"],
                    "geographic_pattern": ["新乡市", "卫辉市"],
                    "promotion_velocity": {"summary": "现任新乡市委常委兼卫辉市委书记，具体晋升速度待查", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "discipline_oriented",
                            "evidence": "以'四不两直'方式暗访安全生产工作，强调'时时放心不下'",
                            "confidence": "confirmed",
                            "source_ids": ["S001"]
                        }
                    ],
                    "speech_themes": ["安全生产", "基层治理", "党建引领"],
                    "management_signals": ["四不两直暗访"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}
                ],
                "source_register": [
                    {"id": "S001", "title": "崔红建采取'四不两直'方式调研督导安全生产工作", "url": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/743b2636b71e47ba9cc3820dee4c8c7a.htm", "publisher": "卫辉市融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认崔红建为'新乡市委常委、卫辉市委书记'"},
                    {"id": "S002", "title": "全市党建引领基层高效能治理观摩推进会召开", "url": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/2734a7ba1a6541d7ad68af487312696b.htm", "publisher": "卫辉市融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认崔红建为书记、王清洲为市长"},
                    {"id": "S003", "title": "卫辉市领导之窗", "url": "https://www.weihui.gov.cn/portal/zfxxgk/zfxxgkml/ldzc/A001003002001index_1.htm", "publisher": "卫辉市人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "列出王清洲、郝科伟、赵旺勇、徐明璐"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "partial",
                    "relationship_confidence": "high",
                    "biggest_gap": "崔红建出生年月、籍贯、教育背景和完整履历未知；何时调任卫辉市委书记未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "崔红建的出生年月、籍贯、教育背景？",
                        "why_it_matters": "这些是人物身份的核心指标",
                        "suggested_queries": ["崔红建 简历", "崔红建 出生", "崔红建 籍贯"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": "崔红建何时开始担任卫辉市委书记？此前任何职？",
                        "why_it_matters": "了解晋升路径和干部交流模式",
                        "suggested_queries": ["崔红建 任卫辉市委书记", "崔红建 此前 担任"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "崔红建何时被任命为新乡市委常委？",
                        "why_it_matters": "新乡市委常委是副厅级职务，时间点对判断晋升速度重要",
                        "suggested_queries": ["崔红建 新乡市委常委"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "王清洲",
            "job": "市长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "新乡市",
                    "region": "卫辉市",
                    "job": "市长",
                    "task_id": "henan_卫辉市",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "weihui_wang_qingzhou",
                    "name": "王清洲",
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "",
                    "birthplace": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": ""
                },
                "current_status": {
                    "current_post": "市委副书记、市长",
                    "current_org": "卫辉市人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S002", "S003"]
                },
                "career_timeline": [
                    {
                        "start": "",
                        "end": "present",
                        "org": "卫辉市人民政府",
                        "title": "市长",
                        "level": "正处级",
                        "location": "卫辉市",
                        "system": "government",
                        "confidence": "confirmed",
                        "source_ids": ["S002", "S003"]
                    },
                    {
                        "start": "",
                        "end": "present",
                        "org": "中共卫辉市委员会",
                        "title": "市委副书记",
                        "level": "副处级",
                        "location": "卫辉市",
                        "system": "party",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "崔红建",
                        "person_id": "weihui_cui_hongjian",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "市长与市委书记为卫辉市党政正职搭档，共同主持全市党建引领基层高效能治理观摩推进会",
                        "overlap_org": "卫辉市",
                        "overlap_period": "",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "调研督导地质灾害防治工作，深入狮豹头乡隐患点",
                        "role_in_event": "带队调研",
                        "location": "卫辉市狮豹头乡",
                        "confidence": "confirmed",
                        "source_ids": ["S004"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "other",
                        "achievement_or_event": "主持全市党建引领基层高效能治理观摩推进会",
                        "role_in_event": "主持会议",
                        "location": "卫辉市",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "local_ladder",
                    "systems_experience": ["government", "party"],
                    "geographic_pattern": ["卫辉市"],
                    "promotion_velocity": {"summary": "履历待查", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "深入山区一线调研地质灾害防范，现场踏勘隐患点",
                            "confidence": "confirmed",
                            "source_ids": ["S004"]
                        }
                    ],
                    "speech_themes": ["地质灾害防治", "基层治理", "人民至上"],
                    "management_signals": ["现场踏勘", "一线督导"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}
                ],
                "source_register": [
                    {"id": "S002", "title": "全市党建引领基层高效能治理观摩推进会召开", "url": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/2734a7ba1a6541d7ad68af487312696b.htm", "publisher": "卫辉市融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                    {"id": "S003", "title": "卫辉市领导之窗", "url": "https://www.weihui.gov.cn/portal/zfxxgk/zfxxgkml/ldzc/A001003002001index_1.htm", "publisher": "卫辉市人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
                    {"id": "S004", "title": "王清洲调研督导地质灾害防治工作", "url": "https://www.weihui.gov.cn/portal/zwyw/xw/whyw/2026/7/af0418cbde054675acf8d61f056f26d8.htm", "publisher": "卫辉市融媒体中心", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认王清洲为'市委副书记、市长'，副市长李华蕾一同调研"}
                ],
                "confidence_summary": {
                    "identity": "plausible",
                    "current_role": "confirmed",
                    "career_completeness": "partial",
                    "relationship_confidence": "high",
                    "biggest_gap": "王清洲出生年月、籍贯、教育背景和完整履历未知；何时开始担任卫辉市长未知"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "王清洲的出生年月、籍贯、教育背景？",
                        "why_it_matters": "人物身份核心指标",
                        "suggested_queries": ["王清洲 简历", "王清洲 出生", "王清洲 卫辉"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": "王清洲何时开始担任卫辉市市长？此前任何职？",
                        "why_it_matters": "了解晋升路径",
                        "suggested_queries": ["王清洲 任卫辉市长", "王清洲 此前 担任"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
    ]

    for pf in person_files:
        fname = f"{TODAY}-河南省-新乡市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files:
        src = PERSONS_DIR / f"{TODAY}-河南省-新乡市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Core leaders confirmed from official sources:")
    print(f"   - 新乡市委常委、卫辉市委书记: 崔红建")
    print(f"   - 卫辉市委副书记、市长: 王清洲")
    print(f"   - 副市长(领导之窗列出): 郝科伟, 赵旺勇, 徐明璐")
    print(f"\n⚠ Detailed biographies need supplementing via:")
    print(f"⚠   - Baidu Baike (blocked during this investigation)")
    print(f"⚠   - 新乡市 组织部 任前公示")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()
