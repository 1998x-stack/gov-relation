#!/usr/bin/env python3
"""十堰市张湾区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
任务: hubei_张湾区
目标: 区委书记 & 区长
调查日期: 2026-08-06
调查状态: 网络严重受限（Exa rate-limit、政府官网超时、Jina/搜索引擎不可达）。

数据完整性说明（partial-evidence artifact mode）:
  - 外部网络在本会话全程不可用，未能在线核验 2026 年现任区委书记/区长姓名。
  - 以下人物身份基于仓库内既有确认数据 + 公开训练数据的"十堰本地公开知识"，
    统一标注 confidence（confirmed/plausible/unverified），不虚构出生、学历、入党日期。
  - 已确认连接: 李琴（现茅箭区委书记，此前任张湾区人民政府区长，属
    "张湾→茅箭"主城区正职跨区交流），来源 data/persons/20260724-...-茅箭区委书记-李琴.json 与
    report/20260724-十堰市-跨区域干部交流网络调查报告.md。
  - 现任 2026 区委书记/区长姓名待核实，置 open_questions。

schema: 复刻 data/database 既有 4 表结构（persons/organizations/positions/relationships），
GEXF 1.3 用字符串拼接（见 references/gexf_pattern.md）。
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "张湾区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
# person.id 规划: 1xxx=区委系统, 2xxx=区政府系统, 3xxx=人大/政协/其他
persons = [
    # 1. 区委书记 —— 现任姓名待核，占位为 "待确认（张湾区委书记）"
    {
        "id": 1001,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区委书记",
        "current_org": "中共十堰市张湾区委员会",
        "source": "训练数据公开知识，未核验（对应 张湾区委书记）",
    },
    # 2. 区长 现任姓名待核
    {
        "id": 2001,
        "name": "待核",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区人民政府区长",
        "current_org": "十堰市张湾区人民政府",
        "source": "训练数据公开知识，未核验",
    },
    # 3. 李琴 —— 已确认：曾任张湾区人民政府区长（后交流至茅箭区委书记）
    {
        "id": 2002,
        "name": "李琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区区长（历任）；现任茅箭区委书记",
        "current_org": "中共和张湾区人民政府（历任）；現任中共十堰市茅箭区委员会",
        "source": "data/person_20260724-...茅箭区委书记-李琴.json；report 20260724-十堰市-跨区域干部交流网络调查报告",
    },
    # 4. 区委副书记（组织系统典型配置；姓名待核）
    {
        "id": 1002,
        "name": "待核",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区委副书记",
        "current_org": "中共十堰市张湾区委员会",
        "source": "训练数据公开知识，未核验",
    },
    # 5. 区人大常委会主任
    {
        "id": 3001,
        "name": "待核",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区人大常委会主任",
        "current_org": "十堰市张湾区人民代表大会常务委员会",
        "source": "训练数据公开知识，未核验",
    },
    # 6. 区政协主席
    {
        "id": 3002,
        "name": "待核",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张湾区政协主席",
        "current_org": "中国人民政治协商会议十堰市张湾区委员会",
        "source": "训练数据公开知识，未核验",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共十堰市张湾区委员会", "type": "党委", "level": "县处级", "parent": "中共十堰市委", "location": "十堰市张湾区"},
    {"id": 2, "name": "十堰市张湾区人民政府", "type": "政府", "level": "县处级", "parent": "十堰市人民政府", "location": "十堰市张湾区"},
    {"id": 3, "name": "十堰市张湾区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "十堰市人大常委会", "location": "十堰市张湾区"},
    {"id": 4, "name": "中国人民政治协商会议十堰市张湾区委员会", "type": "政协", "level": "县处级", "parent": "政协十堰市委员会", "location": "十堰市张湾区"},
    {"id": 5, "name": "中共十堰市茅箭区委员会", "type": "党委", "level": "县处级", "parent": "中共十堰市委", "location": "十堰市茅箭区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1001, "org_id": 1, "title": "张湾区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区委全面工作；2026 现任姓名待核"},
    # 区长
    {"person_id": 2001, "org_id": 1, "title": "张湾区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2001, "org_id": 2, "title": "张湾区人民政府区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作；2026 现任姓名待核"},
    # 李琴（历任张湾区长）
    {"person_id": 2002, "org_id": 2, "title": "张湾区人民政府区长", "start_date": "2018", "end_date": "2021", "rank": "县处级正职", "note": "曾任张湾区长"},
    {"person_id": 2002, "org_id": 5, "title": "茅箭区委书记", "start_date": "2022", "end_date": "present", "rank": "县处级正职", "note": "交流任茅箭区委书记"},
    # 区委副书记
    {"person_id": 1002, "org_id": 1, "title": "张湾区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "姓名待核"},
    # 人大 / 政协
    {"person_id": 3001, "org_id": 3, "title": "张湾区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待核"},
    {"person_id": 3002, "org_id": 4, "title": "张湾区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待核"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1001, "person_b": 2001, "type": "党政搭档", "context": "区委书记与区长为张湾区党政正职搭档", "overlap_org": "张湾区", "overlap_period": ""},
    # 李琴历史关联（张湾区→茅箭区主城跨区交流，已验证）
    {"person_a": 2002, "person_b": 2001, "type": "前后任", "context": "李琴曾历任张湾区长，为该区现任区长的前任（历届顺序）", "overlap_org": "十堰市张湾区人民政府", "overlap_period": "2018-2021（李琴任期）"},
    # 区委书记——区委副书记
    {"person_a": 1001, "person_b": 1002, "type": "上下级", "context": "区委书记与区委副书记", "overlap_org": "中共张湾区委", "overlap_period": ""},
    # 党委与人大 / 政协
    {"person_a": 1001, "person_b": 3001, "type": "党委与人大", "context": "区委书记与人大常委会主任", "overlap_org": "张湾区", "overlap_period": ""},
    {"person_a": 1001, "person_b": 3002, "type": "党委与政协", "context": "区委书记与政协主席", "overlap_org": "张湾区", "overlap_period": ""},
]


# ── Helper Functions ───────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    """Return RGB color string for a person based on role."""
    if "区委书记" in name or "书记" in name:
        return "255,50,50"
    if "区长" in name:
        return "50,100,255"
    if "人大" in name:
        return "200,255,255"
    if "政协" in name:
        return "255,240,200"
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")


def generate_gexf(persons, organizations, positions, relationships, output_path):
    """Generate GEXF 1.3 using string formatting (avoid ElementTree namespace issues)."""
    province, parent_city = "湖北省", "十堰市"
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership relationship network — {province} {parent_city}</description>')
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
        sz = "20.0" if p["id"] in (1001, 2001) else "12.0"
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
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if not any(p["id"] == pos["person_id"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if not any(p["id"] == r["person_a"] and p["name"] for p in persons):
            continue
        if not any(p["id"] == r["person_b"] and p["name"] for p in persons):
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    GEXF written: {output_path}")


def build_sqlite(persons, organizations, positions, relationships, db_path):
    """Build SQLite database with the standard 4-table schema."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("INSERT OR REPLACE INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"    DB written: {db_path}")


def person_body_slug(name):
    """Stable person_id slug from a Chinese name."""
    return "zhangwan_" + name


def _is_confirmed(person):
    """Placeholder persons (names marked 待核/待确认/待考古) are not confirmed."""
    return not any(tag in person["name"] for tag in ("待确认", "待考古", "待核"))


def write_person_json(person, output_dir):
    """Write a single person JSON file per person_graph_json.md schema."""
    if not person["name"]:
        return
    job = person["current_post"].replace("/", "-").replace("、", "-").replace("（", "-").replace("）", "").replace("；", "-").replace("，", "-").replace(" ", "")
    filename = f'{TODAY}-湖北省-十堰市-{job}-{person["name"]}.json'
    filepath = Path(output_dir) / filename

    confirmed = _is_confirmed(person)

    source_register = [{
        "id": "S001",
        "title": "张湾区/十堰市 公开信息（本会话，凭证见 open_questions）",
        "url": "https://www.zhangwan.gov.cn/（会话超时）",
        "publisher": "张湾区人民政府 / 十堰市公开资料",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "inferred",
        "reliability": "low" if not confirmed else "high",
        "notes": "web 访问受限；confident 标识基于仓库内确认数据或训练知识",
    }]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省", "city": "十堰市", "region": "张湾区",
            "job": person["current_post"], "task_id": "hubei_张湾区", "time_focus": "2026-08",
        },
        "identity": {
            "person_id": person_body_slug(person["name"]),
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.zhangwan.gov.cn/（离线）",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if person["id"] in (1001, 2001) else "县处级副职/其他",
            "as_of": AS_OF,
            "is_current_confirmed": confirmed,
            "source_ids": ["S001"],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开纪律处分/审计问题/负面报道；但因网络受限，仅覆盖有限公开源", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if confirmed else "unverified",
            "current_role": "confirmed" if confirmed else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "2026 现任姓名未能在线上核验；履历（出生/学历/入党/工作起始）几乎空白",
        },
        "open_questions": [
            {
                "priority": "critical" if not confirmed else "high",
                "question": f"张湾区{person['current_post']}的当前姓名与身份（需在线核验现任 2026 年任职者）",
                "why_it_matters": "当前为占位/待核信息，无法进行后续履历与关系深度分析",
                "suggested_queries": [f"张湾区 {person['current_post']}", "张湾区 领导之窗", "十堰市 组织部 任前公示 张湾"],
                "last_attempted": AS_OF,
            }
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    Person JSON written: {filepath}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BASE))

    print(f"\n===== Building {SLUG} network data =====")
    print("  Creating SQLite database...")
    build_sqlite(persons, organizations, positions, relationships, DB_PATH)

    print("  Creating GEXF graph...")
    generate_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    print("  Creating person JSON files...")
    for p in persons:
        write_person_json(p, STAGING_DIR)

    print(f"\nDone. Artifacts:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    person_files = sorted(f for f in Path(STAGING_DIR).iterdir() if f.suffix == ".json" and TODAY in f.name)
    for pf in person_files:
        print(f"  Person: {pf}")