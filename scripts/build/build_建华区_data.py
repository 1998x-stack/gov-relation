#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Jianhua District (建华区), Qiqihar, Heilongjiang.

NOTE: Web access to Chinese government sites (jianhua.gov.cn) was completely
unreachable from this environment (timeouts, DNS failures, firewall blocks).
All data below is sourced from training knowledge and marked with appropriate
confidence levels. This is a partial-evidence artifact per the fallback playbook.
"""

import json
import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# If running from staging dir, use it directly; otherwise compute from repo root
if SCRIPT_DIR.endswith("heilongjiang_建华区"):
    TMP = SCRIPT_DIR
else:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    TMP = os.path.join(BASE, "data/tmp/heilongjiang_建华区")
DB_PATH = os.path.join(TMP, "建华区_network.db")
GEXF_PATH = os.path.join(TMP, "建华区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

os.makedirs(PERSONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries marked with confidence levels
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──
    # NOTE: Names and roles below are based on available public knowledge
    # and should be verified against jianhua.gov.cn (currently unreachable).
    # As of mid-2026, the following are believed to be the core leaders.
    {
        "id": 1,
        "name": "待确认区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市建华区委书记",
        "current_org": "中共齐齐哈尔市建华区委员会",
        "source": "https://www.jianhua.gov.cn/（无法访问）",
        "confidence": "unverified",
        "notes": "因政府网站无法访问，当前区委书记姓名未能确认。需通过齐齐哈尔市委组织部任前公示或新闻检索确认。"
    },
    {
        "id": 2,
        "name": "待确认区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市建华区委副书记、区长",
        "current_org": "齐齐哈尔市建华区人民政府",
        "source": "https://www.jianhua.gov.cn/（无法访问）",
        "confidence": "unverified",
        "notes": "因政府网站无法访问，当前区长姓名未能确认。"
    },
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市建华区委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 2, "name": "齐齐哈尔市建华区人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 3, "name": "齐齐哈尔市建华区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 4, "name": "中国人民政治协商会议齐齐哈尔市建华区委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 5, "name": "中共齐齐哈尔市建华区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 6, "name": "中共齐齐哈尔市建华区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市建华区委员会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 7, "name": "中共齐齐哈尔市建华区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市建华区委员会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 8, "name": "中共齐齐哈尔市建华区委政法委", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市建华区委员会", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 9, "name": "齐齐哈尔市公安局建华分局", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市公安局", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 10, "name": "齐齐哈尔市建华区人民检察院", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民检察院", "location": "黑龙江省齐齐哈尔市建华区"},
    {"id": 11, "name": "齐齐哈尔市建华区人民法院", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市中级人民法院", "location": "黑龙江省齐齐哈尔市建华区"},
]

positions = [
    # Current leaders (placeholders with person_id=1 for 区委书记, person_id=2 for 区长)
    {"person_id": 1, "org_id": 1, "title": "齐齐哈尔市建华区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "当前区委书记，待确认姓名"},
    {"person_id": 2, "org_id": 2, "title": "齐齐哈尔市建华区委副书记、区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "当前区长，待确认姓名"},
]

relationships = [
]

# ═══════════════════════════════════════════════════════════════════════
# SQLite Build
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(current_post):
    """Return GEXF color based on role."""
    post = current_post or ""
    if "区委书记" in post or "县委书记" in post:
        return "255,50,50"
    elif "区长" in post or "县长" in post or "市长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "人大" in post:
        return "200,255,255"
    elif "政协" in post:
        return "255,240,200"
    else:
        return "100,100,100"

def is_top_leader(post):
    return "区委书记" in post or "区长" in post or "县长" in post

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
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
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        )
    """)
    cur.execute("""
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
        )
    """)
    cur.execute("""
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
        )
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r.get("type", ""),
                     r.get("context", ""), r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")
    print(f"    {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>建华区领导班子关系网络 — 黑龙江省齐齐哈尔市建华区</description>')
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

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = "20.0" if is_top_leader(p["current_post"]) else "12.0"
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="disc"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="220" g="220" b="220"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: positions (person -> org)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: relationships (person <-> person)
    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r.get("context", ""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")

def write_person_json(person):
    """Write a person JSON file following the person_graph_json.md schema."""
    today = datetime.now().strftime("%Y%m%d")
    safe_name = person["name"].replace("待确认", "daiqueren")
    filename = f"{today}-黑龙江省-齐齐哈尔市-{person['current_post'].replace('齐齐哈尔市', '').replace('建华', '建华')}-{safe_name}.json"
    # Clean filename
    filename = filename.replace(" ", "").replace("/", "_")
    filepath = os.path.join(PERSONS_DIR, filename)

    data = {
        "schema_version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "齐齐哈尔市",
            "region": "建华区",
            "job": person["current_post"],
            "task_id": "heilongjiang_建华区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"qqhr_jianhua_{person['id']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] or "",
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "https://www.jianhua.gov.cn/（无法访问）"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if is_top_leader(person["current_post"]) else "县处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "因政府网站无法访问，完整履历未能获取",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {
                "org": person["current_org"],
                "role": person["current_post"],
                "period": "",
                "confidence": "unverified",
                "source_ids": ["S001"]
            }
        ],
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "建华区人民政府官方网站",
                "url": "https://www.jianhua.gov.cn/",
                "publisher": "建华区人民政府",
                "published_at": "",
                "accessed_at": datetime.now().strftime("%Y-%m-%d"),
                "source_type": "official",
                "reliability": "high",
                "notes": "网站无法访问，未能获取实际数据"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有个人信息均不可用"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"当前{person['current_post']}的姓名、出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "这是本次调研的核心人物，基本信息完全缺失",
                "suggested_queries": [
                    f"建华区 {person['current_post']} 姓名",
                    f"齐齐哈尔 建华区 {person['current_post']} 简历",
                    "建华区人民政府 领导分工"
                ],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "priority": "high",
                "question": f"{person['current_post']}的完整职业履历是什么？",
                "why_it_matters": "履历是分析工作关系网络的基础",
                "suggested_queries": [
                    f"建华区 {person['current_post']} 任职经历",
                    f"齐齐哈尔 组织部 任前公示 建华区",
                    "建华区人大 任命"
                ],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")
    return filepath


def write_open_gaps():
    """Write open_gaps registry."""
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# Open Gaps Registry — 建华区补充
> Added: {today}

## ⭐⭐⭐⭐⭐ Critical (core figures with complete info missing)

| Person | Current Role | What's Missing | Last Attempted | Notes |
|--------|-------------|----------------|----------------|-------|
| 待确认 | 建华区委书记 | 姓名、出生年月、籍贯、教育、完整履历 | {today} | 政府网站无法访问，所有信息待确认 |
| 待确认 | 建华区长 | 姓名、出生年月、籍贯、教育、完整履历 | {today} | 政府网站无法访问，所有信息待确认 |

## ⭐⭐⭐⭐ High (leadership roster entirely missing)

| Person/Gap | What's Missing | Last Attempted | Notes |
|-----------|----------------|----------------|-------|
| 全体区委常委 | 姓名、分工、背景 | {today} | 常委员会成员列表完全未知 |
| 全体副区长 | 姓名、分工 | {today} | 政府领导班子完全未知 |
| 区人大主任 | 姓名 | {today} | 人大领导未知 |
| 区政协主席 | 姓名 | {today} | 政协领导未知 |
| 前任区委书记 | 姓名、去向 | {today} | 前任信息完全未知 |
| 前任区长 | 姓名、去向 | {today} | 前任信息完全未知 |

## ⭐⭐⭐ Medium (cross-district comparison)

| Gap | Last Attempted | Notes |
|-----|----------------|-------|
| 建华区与齐齐哈尔其他区(龙沙、铁锋等)干部交流模式 | {today} | 发现跨区调动需要另一个区的研究做对照 |
"""
    gap_path = os.path.join(TMP, "open_gaps.md")
    with open(gap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Open gaps: {gap_path}")


def write_report():
    """Write the investigation report."""
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# 齐齐哈尔市建华区领导班子工作关系网络调查报告
> 生成日期：{today}

## ⚠️ 重要说明

本次调研中，所有中国互联网搜索引擎（百度）和政府网站（建华区人民政府 jianhua.gov.cn、齐齐哈尔市人民政府 qqhr.gov.cn 等）均因网络限制无法访问。本报告基于不完全公开信息，所有结论均为"待验证"状态。

## 1. 概况

- **地区**：黑龙江省齐齐哈尔市建华区
- **行政级别**：市辖区（县处级）
- **调研任务**：heilongjiang_建华区
- **目标**：区委书记 & 区长

## 2. 当前核心领导（待确认）

| 职务 | 姓名 | 状态 |
|------|------|------|
| 建华区委书记 | 待确认 | 网站无法访问 |
| 建华区委副书记、区长 | 待确认 | 网站无法访问 |

## 3. 领导班子（待确认）

建华区委常委会、区政府领导班子全体成员待确认。

## 4. 前任领导（未知）

前任区委书记和区长的去向完全未知。

## 5. 近期人事变动（未知）

因无法访问政府网站，近期人事变动信息不可用。

## 6. 工作关系网络（待构建）

数据不足，无法构建有效的工作关系网络。

## 7. 周边县区人事交流（待探索）

建华区与齐齐哈尔市其他区县（龙沙区、铁锋区、富拉尔基区等）之间的干部交流情况待探索。

## 8. 关键洞察与建议

### 优先行动
1. **使用本地网络或 VPN 访问** jianhua.gov.cn 获取完整的领导分工页面
2. 查询齐齐哈尔市委组织部**任前公示**获取建华区各级干部履历
3. 通过新闻检索（尤其是齐齐哈尔日报、东北网）补充近期人事变动信息

## 9. 数据文件说明

| 文件 | 路径 | 说明 |
|------|------|------|
| 构建脚本 | build_建华区_data.py | 数据库和图生成脚本 |
| SQLite 数据库 | 建华区_network.db | 结构化关系数据 |
| GEXF 图 | 建华区_network.gexf | 可导入 Gephi 的关系图 |
| 个人档案 | persons/*.json | 核心人物深度档案 |

## 10. 信息来源

- 建华区人民政府网站：https://www.jianhua.gov.cn/（无法访问）
- 齐齐哈尔市人民政府网站：https://www.qqhr.gov.cn/

---
*本报告为不完全版本，所有信息待验证。*
"""
    report_path = os.path.join(TMP, "20260724-齐齐哈尔市-建华区-调研报告.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Report: {report_path}")


if __name__ == "__main__":
    print("Building 建华区 network data...\n")

    # 1. SQLite
    print("[1/5] SQLite database...")
    build_db()

    # 2. GEXF
    print("[2/5] GEXF graph...")
    build_gexf()

    # 3. Person JSON
    print("[3/5] Person JSON files...")
    for p in persons:
        write_person_json(p)

    # 4. Open gaps
    print("[4/5] Open gaps registry...")
    write_open_gaps()

    # 5. Report
    print("[5/5] Investigation report...")
    write_report()

    print("\nDone. All artifacts in:", TMP)
    print(f"  DB:      {DB_PATH}")
    print(f"  GEXF:    {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}/")
