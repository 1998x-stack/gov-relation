#!/usr/bin/env python3
"""香坊区（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 维基百科 - 香坊区条目 (确认区委书记为黄晓伟)
  - 哈尔滨市香坊区人民政府官网 (www.hrbxf.gov.cn) — 因网络访问限制未能解析领导之窗页面
  - 公开新闻报道

数据截至：2026年7月

Target roles:
  - 区委书记: 黄晓伟
  - 区委副书记、区长: 【待确认 — 网络受限未能获取现任区长姓名】
  - 其他区领导: 【待深入调研】

关键缺口：
  - 区长姓名及履历：因Exa API限流、Baidu 403、政府网站超时、Google/Bing未返回有效结果，
    未能获取现任区长准确信息。Wikipedia条目仅列出区委书记。
  - 黄晓伟的详细履历（出生年月、教育背景、历任职务）

建议后续首先通过政府门户 "领导之窗" 页面或哈尔滨市委组织部任前公示补充区长信息。
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "香坊区_network.db"
GEXF_PATH = STAGING / "香坊区_network.gexf"
PERSONS_DIR = STAGING

TODAY = "2026-07-24"
AS_OF = TODAY

# ── Helper ──
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# =========================================================================
# DATA
# =========================================================================

persons = [
    {
        "id": 1,
        "name": "黄晓伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共香坊区委员会",
        "source": "https://zh.wikipedia.org/wiki/%E9%A6%99%E5%9D%8A%E5%8C%BA",
    },
]

organizations = [
    {"id": 1, "name": "中共香坊区委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "哈尔滨市香坊区"},
    {"id": 2, "name": "香坊区人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "哈尔滨市香坊区"},
    {"id": 3, "name": "香坊区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共香坊区委员会", "location": "哈尔滨市香坊区"},
    {"id": 4, "name": "香坊区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "哈尔滨市香坊区"},
    {"id": 5, "name": "香坊区政协委员会", "type": "政协", "level": "县处级", "parent": "哈尔滨市政协", "location": "哈尔滨市香坊区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "区委主要负责人"},
]

relationships = [
]

source_register = [
    {"id": "S001", "title": "维基百科 - 香坊区", "url": "https://zh.wikipedia.org/wiki/%E9%A6%99%E5%9D%8A%E5%8C%BA",
     "publisher": "Wikipedia", "published_at": "2026-07", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": "确认区委书记黄晓伟"},
    {"id": "S002", "title": "哈尔滨市香坊区人民政府", "url": "http://www.hrbxf.gov.cn/",
     "publisher": "香坊区人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "政府官网首页，因网络受限未能解析完整领导信息"},
]


# =========================================================================
# BUILD
# =========================================================================

def build():
    os.makedirs(STAGING, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"xiangfang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "255,50,50"
        if "区长" in post and "副" not in post and "区委副书记" in post:
            return "50,100,255"
        if "副区长" in post or "常务副区长" in post:
            return "100,150,220"
        if "副书记" in post and "区委副书记" in post and "区长" not in post:
            return "100,150,220"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post) or \
               ("区长" in post and "副" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "区委书记" in post:
            return "square"
        if "区长" in post and "副" not in post:
            return "circle"
        if "常务副区长" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
            "事业单位": "220,220,220",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>哈尔滨市香坊区领导班子关系网络（初步 — 需补充区长等信息）</description>')
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

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    def make_person_json(p, custom_id=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "哈尔滨市",
                "region": "香坊区",
                "job": p.get("current_post", ""),
                "task_id": "heilongjiang_香坊区",
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"xiangfang_{p['name']}" if not custom_id else custom_id,
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
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "区委书记" in p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "",
                    "org": p.get("current_org", ""),
                    "title": p.get("current_post", ""),
                    "notes": "现任区委书记。公开资料中未找到详细履历。",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [],
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
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历信息缺失；区长姓名及信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历（出生年月、教育背景、历任职务）",
                 "why_it_matters": "无法追溯其任职路径和系统经历，无法建立更深层的关系网络",
                 "suggested_queries": [f"{p['name']} 简历 香坊 哈尔滨", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": "香坊区区长姓名及履历",
                 "why_it_matters": "区长是区域行政负责人，缺失该信息则无法构建完整的领导关系和网络",
                 "suggested_queries": ["香坊区 区长 现任", "哈尔滨 香坊区 区长 任命", "香坊区 政府工作报告"],
                 "last_attempted": AS_OF},
            ]
        }
        return result

    # Generate person JSON files for the known leaders
    for p in persons:
        pjson = make_person_json(p)
        job_slug = "区委书记" if p["id"] == 1 else "区长"
        fname = f"{TODAY}-黑龙江省-哈尔滨市-{job_slug}-{p['name']}.json"
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {fpath}")


if __name__ == "__main__":
    build()
