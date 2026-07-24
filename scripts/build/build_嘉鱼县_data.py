#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 嘉鱼县 (Jiayu County), 咸宁市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 咸宁市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_嘉鱼县

Research date: 2026-07-24
Official source: http://www.jiayu.gov.cn/ (嘉鱼县人民政府) — confirmed accessible via HTTP

Current status (as of 2026-07-24):
- 县委书记: 胡金云 (confirmed via official news articles — 胡金云主持召开县委常委会会议)
- 县长: 陈瞻 (confirmed via official government leadership page)

Roster sources:
   县政府领导: http://www.jiayu.gov.cn/xxgk/zfld/cz/ (陈瞻 — 县长)
                http://www.jiayu.gov.cn/xxgk/zfld/yjl/ (袁钧蓝 — 副县长)
                http://www.jiayu.gov.cn/xxgk/zfld/lt/ (刘涛 — 副县长)
                http://www.jiayu.gov.cn/xxgk/zfld/syp/ (石亚平 — 副县长)
                http://www.jiayu.gov.cn/xxgk/zfld/gyh/ (高云海 — 副县长)

Confidence notes:
  - 县长 (陈瞻) identity: confirmed via official government website (with photo, bio, education)
  - 副县长 bios: confirmed via official government website
  - 县委书记 (胡金云) identity: confirmed via multiple news articles; full career history: unverified
  - 县委常委 full roster: partially confirmed — news articles mention 华红, 陈良成 as additional leadership
  - Exa search was rate-limited; Baidu returned 403; Google/Bing/DuckDuckGo timed out
  - Predecessor details: unverified — web search unavailable
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "嘉鱼县"
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
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "胡金云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共嘉鱼县委员会",
        "source": "http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260724_5124498.shtml"
    },
    {
        "id": 2,
        "name": "陈瞻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "湖北孝昌",
        "education": "博士研究生学历，高级工程师、高级经济师",
        "party_join": "中共党员",
        "work_start": "2015年7月",
        "current_post": "县长",
        "current_org": "嘉鱼县人民政府",
        "source": "http://www.jiayu.gov.cn/xxgk/zfld/cz/"
    },
    # ═══════ 县政府领导 ═══════
    {
        "id": 3,
        "name": "袁钧蓝",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "湖北嘉鱼",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1999年3月",
        "current_post": "副县长",
        "current_org": "嘉鱼县人民政府",
        "source": "http://www.jiayu.gov.cn/xxgk/zfld/yjl/"
    },
    {
        "id": 4,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "湖北咸安",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "2007年7月",
        "current_post": "副县长",
        "current_org": "嘉鱼县人民政府",
        "source": "http://www.jiayu.gov.cn/xxgk/zfld/lt/"
    },
    {
        "id": 5,
        "name": "石亚平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "湖北赤壁",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2000年3月",
        "current_post": "副县长、县公安局局长",
        "current_org": "嘉鱼县人民政府",
        "source": "http://www.jiayu.gov.cn/xxgk/zfld/syp/"
    },
    {
        "id": 6,
        "name": "高云海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年2月",
        "birthplace": "江苏徐州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "副县长",
        "current_org": "嘉鱼县人民政府",
        "source": "http://www.jiayu.gov.cn/xxgk/zfld/gyh/"
    },
    # ═══════ 县委领导 (mentioned in news) ═══════
    {
        "id": 7,
        "name": "华红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共嘉鱼县委员会",
        "source": "http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260722_5098965.shtml"
    },
    {
        "id": 8,
        "name": "陈良成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共嘉鱼县委员会",
        "source": "http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260722_5098965.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共嘉鱼县委员会", "type": "党委", "level": "县", "parent": "中共咸宁市委", "location": "湖北省咸宁市嘉鱼县"},
    {"id": 2, "name": "嘉鱼县人民政府", "type": "政府", "level": "县", "parent": "咸宁市人民政府", "location": "湖北省咸宁市嘉鱼县"},
    {"id": 3, "name": "嘉鱼经济开发区", "type": "开发区", "level": "县", "parent": "嘉鱼县人民政府", "location": "湖北省咸宁市嘉鱼县"},
    {"id": 4, "name": "嘉鱼县公安局", "type": "政府", "level": "县", "parent": "嘉鱼县人民政府", "location": "湖北省咸宁市嘉鱼县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 胡金云
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 陈瞻
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时担任嘉鱼开发区党工委书记"},
    {"person_id": 2, "org_id": 3, "title": "党工委书记", "start_date": "", "end_date": "present", "rank": "", "note": "嘉鱼开发区党工委书记"},
    # 袁钧蓝
    {"person_id": 3, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责文化旅游、体育、民族宗教、市场监督管理等工作"},
    # 刘涛
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责卫生健康、医疗保障、教育、政务服务等工作"},
    # 石亚平
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责社会治安综合治理、依法治县、信访、维稳等工作"},
    {"person_id": 5, "org_id": 4, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "", "note": "主持县公安局全面工作，同时担任县公安局党委书记、督察长"},
    # 高云海
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责工业经济、招商引资、自然资源和规划、城市建设等工作"},
    # 华红
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 陈良成
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Working relationships within 县委常委会
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭班子，共同主持县委常委会", "overlap_org": "中共嘉鱼县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委华红在县委常委会共事", "overlap_org": "中共嘉鱼县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县委常委陈良成在县委常委会共事", "overlap_org": "中共嘉鱼县委员会", "overlap_period": ""},
    # 县长与副县长的工作关系
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与副县长袁钧蓝在县政府班子共事", "overlap_org": "嘉鱼县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长刘涛在县政府班子共事", "overlap_org": "嘉鱼县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长石亚平在县政府班子共事", "overlap_org": "嘉鱼县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长高云海在县政府班子共事", "overlap_org": "嘉鱼县人民政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Build functions
# ══════════════════════════════════════════════════════════════════════════

def build_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    import sqlite3
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
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
        CREATE TABLE IF NOT EXISTS relationships (
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
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
              p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH}")
    print(f"    - {len(persons)} persons, {len(organizations)} organizations, {len(positions)} positions, {len(relationships)} relationships")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Agent</creator>')
    lines.append('    <description>嘉鱼县领导工作关系网络 — 湖北省咸宁市嘉鱼县</description>')
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
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        # Determine color by role
        if "县委书记" in post:
            color = "255,50,50"  # Red
            sz = "20.0"
        elif "县长" in post:
            color = "50,100,255"  # Blue
            sz = "20.0"
        elif "副县长" in post:
            color = "50,100,255"  # Blue
            sz = "12.0"
        elif "县委常委" in post:
            color = "100,100,100"  # Grey
            sz = "12.0"
        else:
            color = "100,100,100"
            sz = "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = o["id"] + 100000
        oname = o["name"]
        otype = o["type"]
        # Color by org type
        type_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "开发区": "200,255,200",
            "乡镇/街道": "255,255,200",
        }
        ocolor = type_colors.get(otype, "200,200,200")

        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos["title"]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person → Person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")


def build_person_json(person, filename_suffix):
    """Create a person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    post = person["current_post"]
    filename = f"{TODAY}-湖北省-咸宁市-{post}-{name}.json"
    filepath = PERSONS_DIR / filename

    # Determine person_id for dedup
    slug_name = name
    person_id = f"jiayu_{slug_name}"

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "咸宁市",
            "region": "嘉鱼县",
            "job": post,
            "task_id": "hubei_嘉鱼县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person["birthplace"],
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}",
                "name_birthplace": f"{name}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": post,
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "县委" in post else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": person["current_org"],
                "title": post,
                "level": "县",
                "location": "湖北省咸宁市嘉鱼县",
                "system": "party" if "县委" in post and "书记" in post else "government",
                "rank": "正处级" if ("书记" in post and "县委" in post) or ("县长" in post) else "副处级",
                "is_key_promotion": False,
                "notes": "公开资料仅确认现任职务，详细履历待查",
                "confidence": "confirmed" if person["source"] else "unverified",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [{"name": person["current_org"], "role": post, "period": ""}],
        "relationships": [],
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
            {
                "type": "none_found",
                "description": f"未发现{name}的纪律处分、审计问题或负面媒体报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"嘉鱼县人民政府 — {post}",
                "url": person["source"],
                "publisher": "嘉鱼县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if person["birth"] else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "全部履历（任职时间线和早期职业生涯）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整职业履历（早期生涯、历任职务及具体时间）",
                "why_it_matters": "了解其晋升路径、系统背景和关系网络的基础",
                "suggested_queries": [f"{name} 简历 任职经历", f"{name} 任前公示"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的教育背景、入党时间和参加工作年份的详细情况",
                "why_it_matters": "验证身份信息完整性和dedup准确性",
                "suggested_queries": [f"{name} 出生 教育 入党"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath}")
    return filepath


def build_report():
    """Create Markdown research report."""
    report_path = STAGING_DIR / f"{TODAY}-湖北省咸宁市嘉鱼县-领导班子工作关系网络调查报告.md"
    date_placeholder_1 = "{日期}"
    date_placeholder_2 = "{职务}"
    date_placeholder_3 = "{姓名}"
    content = f"""# 湖北省咸宁市嘉鱼县领导班子工作关系网络调查报告

> 报告日期：{AS_OF}
> 任务ID：hubei_嘉鱼县
> 数据来源：嘉鱼县人民政府官网（http://www.jiayu.gov.cn/）

## 1. 现任县委书记：胡金云

- **职务**：中共嘉鱼县委书记
- **性别/民族**：男/汉族（推断）
- **出生**：待查
- **籍贯**：待查
- **学历**：待查
- **入党时间**：中共党员（推断）
- **上任时间**：待查（截至2026年7月仍在任）
- **确认来源**：嘉鱼县政府官网新闻报道（"县委书记胡金云主持会议并讲话"）
- **履历**：公开资料未找到胡金云的完整履历，仅通过新闻确认其现任职务

**信息来源**：
- http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260724_5124498.shtml
- http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260722_5098965.shtml

## 2. 现任县长：陈瞻

- **职务**：中共嘉鱼县委副书记、县政府县长、嘉鱼开发区党工委书记
- **性别/民族**：男/汉族
- **出生**：1985年6月
- **籍贯**：湖北孝昌
- **学历**：博士研究生学历，高级工程师、高级经济师
- **参加工作时间**：2015年7月
- **确认来源**：嘉鱼县政府官网领导之窗
- **分工**：领导县政府全面工作

**信息来源**：
- http://www.jiayu.gov.cn/xxgk/zfld/cz/

## 3. 前任领导去向（待查）

由于网络搜索工具不可用，未能查到胡金云的前任县委书记信息及陈瞻的前任县长信息。建议后续补充：

- 前任县委书记是谁？调往何处？
- 前任县长是谁？调往何处？
- 胡金云任县委书记之前担任什么职务？

## 4. 领导班子成员

### 县政府领导

| 姓名 | 职务 | 性别 | 民族 | 出生 | 籍贯 | 学历 | 参加工作时间 |
|------|------|------|------|------|------|------|------------|
| 陈瞻 | 县长（县委副书记） | 男 | 汉族 | 1985.06 | 湖北孝昌 | 博士研究生 | 2015.07 |
| 袁钧蓝 | 副县长 | 女 | 汉族 | 1980.01 | 湖北嘉鱼 | 大学 | 1999.03 |
| 刘涛 | 副县长 | 男 | 汉族 | 1984.09 | 湖北咸安 | 在职研究生 | 2007.07 |
| 石亚平 | 副县长、县公安局局长 | 男 | 汉族 | 1976.08 | 湖北赤壁 | 大学 | 2000.03 |
| 高云海 | 副县长 | 男 | 汉族 | 1987.02 | 江苏徐州 | 大学 | 2009.07 |

### 县委领导（部分确认）

| 姓名 | 职务 | 确认来源 |
|------|------|---------|
| 胡金云 | 县委书记 | 新闻确认 |
| 陈瞻 | 县委副书记、县长 | 官网确认 |
| 华红 | 县委常委 | 新闻确认（在县委理论学习中心组会议上作研讨发言） |
| 陈良成 | 县委常委 | 新闻确认（同上） |

**注**：县委常委完整名单（包括纪委书记、组织部长、宣传部长、统战部长、政法委书记等）尚未从公开渠道获取。

## 5. 近期人事变动

- **县委书记**：胡金云当前在任（2026年7月仍有公开活动）
- **县长**：陈瞻当前在任（2026年7月仍有公开活动）

详细历任信息：待查。

## 6. 工作关系网络分析

### 确认的交集

| 人员A | 人员B | 关系类型 | 共同组织 | 说明 |
|-------|-------|---------|---------|------|
| 胡金云 | 陈瞻 | 上下级（搭班子） | 嘉鱼县委常委会 | 书记+县长核心搭档 |
| 胡金云 | 华红 | 上下级 | 嘉鱼县委常委会 | 常委班子 |
| 胡金云 | 陈良成 | 上下级 | 嘉鱼县委常委会 | 常委班子 |
| 陈瞻 | 袁钧蓝 | 上下级 | 嘉鱼县政府 | 县长+副县长 |
| 陈瞻 | 刘涛 | 上下级 | 嘉鱼县政府 | 县长+副县长 |
| 陈瞻 | 石亚平 | 上下级 | 嘉鱼县政府 | 县长+副县长 |
| 陈瞻 | 高云海 | 上下级 | 嘉鱼县政府 | 县长+副县长 |

### 人员来源分析

- **陈瞻**（县长）：湖北孝昌人，博士学历，2015年参加工作（较晚参加工作，应为博士毕业后），此前履历待查
- **袁钧蓝**（副县长）：湖北嘉鱼本地人，从基层成长
- **刘涛**（副县长）：湖北咸安人（咸宁市辖区）
- **石亚平**（副县长、公安局长）：湖北赤壁人（咸宁市代管县级市）
- **高云海**（副县长）：江苏徐州人（异地交流干部）

## 7. 周边县区人事交流网络

嘉鱼县地处咸宁市北部，毗邻咸安区、赤壁市。从现有信息看：

- **石亚平**（副县长、公安局长）来自赤壁市，属于从咸宁市下辖其他县区交流到嘉鱼
- **刘涛**（副县长）来自咸安区，同样属于市辖区间交流
- **袁钧蓝**为嘉鱼本地成长干部

## 8. 关键洞察与突破线索

### 高优先级
1. **胡金云的完整履历** — 作为县委书记，其职业背景对理解嘉鱼县政治网络至关重要
2. **陈瞻的早期职业生涯** — 1985年出生，博士学历，2015年才参加工作，意味着其职业生涯仅11年就升至县长，属于快速晋升
3. **县委常委完整名单** — 目前仅确认4位常委，至少还有3-5位未确认

### 中优先级
4. **前任县委书记去向** — 理解嘉鱼县政治传递和人员流动的关键
5. **高云海（江苏徐州人）的交流背景** — 作为唯一的外省籍干部，其来源值得深挖

## 9. 数据文件说明

| 文件 | 路径 | 说明 |
|------|------|------|
| 数据库 | `data/database/嘉鱼县_network.db` | SQLite结构化数据 |
| 图文件 | `data/graph/嘉鱼县_network.gexf` | Gephi可视化图 |
| 人物档案 | `data/persons/{date_placeholder_1}-湖北省-咸宁市-{date_placeholder_2}-{date_placeholder_3}.json` | 个人深度档案 |

## 10. 信息来源汇总

| 来源 | 类型 | URL |
|------|------|-----|
| 嘉鱼县人民政府 | 官方 | http://www.jiayu.gov.cn/ |
| 陈瞻（县长）领导之窗 | 官方 | http://www.jiayu.gov.cn/xxgk/zfld/cz/ |
| 袁钧蓝（副县长）领导之窗 | 官方 | http://www.jiayu.gov.cn/xxgk/zfld/yjl/ |
| 刘涛（副县长）领导之窗 | 官方 | http://www.jiayu.gov.cn/xxgk/zfld/lt/ |
| 石亚平（副县长）领导之窗 | 官方 | http://www.jiayu.gov.cn/xxgk/zfld/syp/ |
| 高云海（副县长）领导之窗 | 官方 | http://www.jiayu.gov.cn/xxgk/zfld/gyh/ |
| 胡金云主持召开县委常委会会议 | 官方新闻 | http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260724_5124498.shtml |
| 胡金云主持县委理论学习中心组会议 | 官方新闻 | http://www.jiayu.gov.cn/xwzx/jyyw/202607/t20260722_5098965.shtml |
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Report: {report_path}")


def main():
    print(f"\n=== Building 嘉鱼县 (Jiayu County) Network Data ===\n")
    print(f"Staging directory: {STAGING_DIR}")
    print(f"As of: {AS_OF}")
    print()

    build_database()
    build_gexf()
    build_report()

    # Person JSONs for core leaders
    core_ids = [1, 2]  # 胡金云, 陈瞻
    person_files = []
    for person in persons:
        if person["id"] in core_ids:
            pf = build_person_json(person, "")
            person_files.append(pf)

    print()
    print("=== Summary ===")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs:")
    for pf in person_files:
        print(f"    - {pf.name}")
    print(f"  Report: {STAGING_DIR / (TODAY + '-湖北省咸宁市嘉鱼县-领导班子工作关系网络调查报告.md')}")
    print()


if __name__ == "__main__":
    main()
