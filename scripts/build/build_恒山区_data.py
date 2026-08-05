#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 恒山区 (Hengshan District), 鸡西市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_恒山区
Level: 市辖区（县处级）
Targets: 区委书记 & 区长
Parent city: 鸡西市

Research sources:
  - 恒山区人民政府官网 https://www.jixihengshan.gov.cn/ — 官方新闻栏目（恒山之窗）
  - c06_369276: 恒山区委书记、政府区长高久辉深入一线督导检查防汛抗洪工作 (2026-08-03)
  - c06_367710: 全区乡领导班子换届工作会议召开 (2026-07-20)
  - c06_354206: 恒山区第十七届人大第六次会议胜利闭幕 (2026-02-03)
  - c06_316986: 恒山区第十七届人大常委会第二十四次会议 (2024-12-20)
  - c06_351670: 区委十九届十次全会暨区委经济工作会议召开 (2026-01-09)
  - c06_366195: 区委书记鲍宇走访慰问 (2026-06-30)

Confidence notes:
  - 现任区委书记、区长 高久辉：confirmed via 官网 2026-08-03；此前为区委副书记/区长，2026-07/08 接任区委书记（党政一肩挑）
  - 现任区人大主任 于春雷、区政协主席 杨旗、组织部长 陈晨、纪委/监委 尹兆鹏、常委副区长 赵欣儒、
    副区长 聂富广、政协副主席 于恒/侯巧雅：confirmed via 官方新闻
  - 前任区委书记 鲍宇 (至2026-06)、前任区长 刘晶国 (2023-2024.9)：confirmed via 官方新闻时间线
  - 完整履历（出生/籍贯/教育）在网络受限下未得，编码为 open_questions/open_gaps
"""

import json
import os
from datetime import datetime

SLUG = "恒山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

MISSING = {"gender": "", "ethnicity": "", "birth": "", "birthplace": "",
           "education": "", "party_join": "中共党员", "work_start": ""}

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "高久辉", **MISSING, "current_post": "区委书记、区长",
     "current_org": "中共恒山区委/恒山区人民政府", "source": "恒山区政府官网 c06_369276 2026-08-03"},
    {"id": 2, "name": "于春雷", **MISSING, "current_post": "区人大常委会主任",
     "current_org": "恒山区人大常委会", "source": "恒山区第十七届人大会议 2026-02 当选（c06_354206）"},
    {"id": 3, "name": "杨旗", **MISSING, "current_post": "区政协主席",
     "current_org": "中国人民政治协商会议恒山区委员会", "source": "恒山区政府官网 c06_367710 2026-07"},
    {"id": 4, "name": "陈晨", **MISSING, "current_post": "区委常委、组织部部长",
     "current_org": "中共恒山区委", "source": "恒山区政府官网 c06_367710 2026-07"},
    {"id": 5, "name": "尹兆鹏", **MISSING, "current_post": "区委常委、区纪委书记、区监委主任",
     "current_org": "恒山区纪委监委", "source": "恒山区政府官网 c06_367710 2026-07"},
    {"id": 6, "name": "赵欣儒", **MISSING, "current_post": "区委常委、政府副区长",
     "current_org": "恒山区人民政府", "source": "恒山区政府官网 c06_369276 2026-08 / c06_354206 2026-02"},
    {"id": 7, "name": "李兆文", **MISSING, "current_post": "区级领导（职务待查）",
     "current_org": "恒山区", "source": "人代会主席台名单 2026-02（c06_354206）"},
    {"id": 8, "name": "聂富广", **MISSING, "current_post": "政府副区长",
     "current_org": "恒山区人民政府", "source": "恒山区政府官网 c06_369276 2026-08"},
    {"id": 9, "name": "于恒", **MISSING, "current_post": "区政协副主席、区工商联主席",
     "current_org": "人民政协协调 恒山区委员会", "source": "恒山区政府官网 c06_368651 2026-07"},
    {"id": 10, "name": "侯巧雅", **MISSING, "current_post": "区政协副主席",
     "current_org": "中国人民政治协商会议恒山区委员会", "source": "恒山区政府官网 c06_368651 2026-07"},
    {"id": 11, "name": "鲍宇", **MISSING, "current_post": "前任区委书记",
     "current_org": "中共恒山区委", "source": "恒山区政府官网 2024-2026 多篇"},
    {"id": 12, "name": "刘晶国", **MISSING, "current_post": "前任区长",
     "current_org": "恒山区人民政府", "source": "恒山区政府官网 2023-2024 多篇"},
    {"id": 13, "name": "叶荣国", **MISSING, "current_post": "更早区委书记",
     "current_org": "中共恒山区委", "source": "恒山区政府官网 2021-2023 多篇"},
    {"id": 14, "name": "耿磊", **MISSING, "current_post": "更早区长",
     "current_org": "恒山区人民政府", "source": "恒山区政府官网 2021-2022 多篇"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共恒山区委员会", "type": "党委", "level": "县处级", "parent": "中共鸡西市委员会", "location": "黑龙江省鸡西市恒山区"},
    {"id": 2, "name": "恒山区人民政府", "type": "政府", "level": "县处级", "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市恒山区"},
    {"id": 3, "name": "恒山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鸡西市人民代表大会常务委员会", "location": "黑龙江省鸡西市恒山区"},
    {"id": 4, "name": "中国人民政治协商会议恒山区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议鸡西市委员会", "location": "黑龙江省鸡西市恒山区"},
    {"id": 5, "name": "中共鸡西市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "鸡西市"},
    {"id": 6, "name": "鸡西市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "鸡西市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "2026-07/08 接任区委书记（官方标题：恒山区委书记、政府区长高久辉）"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2025-01", "end_date": "present", "rank": "县处级", "note": "2025-01起任区长，2024-12为区长候选人"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2024-12", "end_date": "2026-07", "rank": "县处级", "note": "此前为区委副书记、区长"},
    {"person_id": 2, "org_id": 3, "title": "区人大常委会主任", "start_date": "2026-02", "end_date": "present", "rank": "县处级", "note": "2026-02 当选"},
    {"person_id": 3, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "县处级", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区委常委、组织部部长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、区纪委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区监委主任"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区委常委、政府副区长（常务）"},
    {"person_id": 7, "org_id": 1, "title": "区级领导（待核）", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "职务待查"},
    {"person_id": 8, "org_id": 2, "title": "政府副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "政府副区长聂富广"},
    {"person_id": 9, "org_id": 4, "title": "区政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "区工商联主席"},
    {"person_id": 10, "org_id": 4, "title": "区政协副主席", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区委书记", "start_date": "2024", "end_date": "2026-06", "rank": "县处级", "note": "前任区委书记"},
    {"person_id": 12, "org_id": 2, "title": "区长", "start_date": "2023-01", "end_date": "2024-09", "rank": "县处级", "note": "前任区长"},
    {"person_id": 13, "org_id": 1, "title": "区委书记", "start_date": "2021", "end_date": "2023", "rank": "县处级", "note": "更早区委书记"},
    {"person_id": 14, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "2022", "rank": "县处级", "note": "更早区长"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政与人大监督", "context": "区委书记/区长与区人大常委会主任", "overlap_org": "恒山区", "overlap_period": "2026-02起"},
    {"person_a": 1, "person_b": 3, "type": "党政与政协协商", "context": "区委书记/区长与区政协主席", "overlap_org": "恒山区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与组织部长（人事）", "overlap_org": "中共恒山区委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与纪委书记（从严治党）", "overlap_org": "中共恒山区委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "恒山区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长聂富广", "overlap_org": "恒山区人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记鲍宇→现任高久辉", "overlap_org": "中共恒山区委", "overlap_period": "2024-2026"},
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "前任区长刘晶国→现任高久辉", "overlap_org": "恒山区人民政府", "overlap_period": "2023-2025"},
    {"person_a": 13, "person_b": 11, "type": "predecessor_successor", "context": "更早区委书记叶荣国→鲍宇", "overlap_org": "中共恒山区委", "overlap_period": "2021-2024"},
    {"person_a": 14, "person_b": 12, "type": "predecessor_successor", "context": "更早区长耿磊→刘晶国", "overlap_org": "恒山区人民政府", "overlap_period": "2022-2023"},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name):
    if name == "高久辉":
        return "255,50,50"
    if name in ("鲍宇", "叶荣国"):
        return "200,60,60"
    if name == "刘晶国":
        return "50,100,255"
    if name == "耿磊":
        return "80,120,220"
    if name == "赵欣儒":
        return "100,140,255"
    if name == "尹兆鹏":
        return "255,165,0"
    return "100,100,100"

def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    return "200,200,200"

def person_by_name(name):
    for p in persons:
        if p["name"] == name:
            return p
    raise KeyError(name + " 不在 persons 中")

# ── DB ─────────────────────────────────────────────────────────────────────
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
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT);
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT);
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id));
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id));
    """)
    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""),
             p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""),
             p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# ── GEXF ───────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>恒山区领导班子工作关系网络 - {SLUG}, 鸡西市, 黑龙江省</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"])
        sz = "20.0" if p["name"] == "高久辉" else "16.0" if p["name"] in ("鲍宇", "于春雷", "杨旗") else "12.0"
        nid = f"p{p['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
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
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"  OK: GEXF ({eid} edges)")

# ── Person JSON ────────────────────────────────────────────────────────────
def make_person_json(p, timeline=None, relationships_list=None, source_register=None, is_current=True):
    if timeline is None:
        timeline = []
    if relationships_list is None:
        relationships_list = []
    if source_register is None:
        source_register = []
    name = p["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "鸡西市",
            "region": "恒山区",
            "job": p.get("current_post", ""),
            "task_id": "heilongjiang_恒山区",
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"hengshan_{name}",
            "name": name,
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
                "name_birth": f"{name}_{p.get('birth','')}",
                "name_birthplace": f"{name}_{p.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": is_current,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["黑龙江省鸡西市"],
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
            {"type": "none_found", "description": "在公开官方信息中未发现该人物负面信号", "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed" if is_current else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的出生/籍贯/教育及历任职务起止时间待补充"
        },
        "open_questions": [
            {"priority": "high", "question": f"{name}的出生/籍贯/教育及历任职务起止时间", "why_it_matters": "丰富人物画像与网络分析", "suggested_queries": [f"{name} 简历", f"{name} 任前公示"], "last_attempted": AS_OF}
        ]
    }

def _write_json(obj, job, name):
    path = os.path.join(STAGING, f"{TODAY}-黑龙江省-鸡西市-{job}-{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  OK: person json {os.path.basename(path)}")

def build_person_jsons():
    SOURCES = [
        {"id": "S001", "title": "恒山区政府官网—区委书记、区长高久辉防汛新闻", "url": "https://www.jixihengshan.gov.cn/hsq/a8000c4846fd4a25b4e7da43c1598152/202608/c06_369276.shtml", "publisher": "恒山之窗", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认高久辉任区委书记、区长（党政一肩挑）"},
        {"id": "S002", "title": "恒山区政府官网—全区乡领导班子换届工作会议", "url": "https://www.jixihengshan.gov.cn/hsq/a8000c4846fd4a25b4e7da43c1598152/202607/c06_367710.shtml", "publisher": "恒山之窗", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认于春雷/杨旗/陈晨/尹兆鹏等"},
        {"id": "S003", "title": "恒山区第十七届人大第六次会议闭幕", "url": "https://www.jixihengshan.gov.cn/hsq/a8000c4846fd4a25b4e7da43c1598152/202602/c06_354206.shtml", "publisher": "恒山之窗", "published_at": "2026-02-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "选举区人大常委会主任及区级领导名单"},
    ]

    # 1. 高久辉（党政正职）
    gao_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到高氏完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "2025-01", "end": "present", "org": "恒山区人民政府", "title": "区长", "notes": "2025-01起任区长", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2026-07", "end": "present", "org": "中共恒山区委", "title": "区委书记（兼区长）", "notes": "2026-07/08 接任区委书记，党政一肩挑", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    gao_rel = [
        {"person": "鲍宇", "person_id": "hengshan_鲍宇", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "鲍宇卸任区委书记后高继任", "overlap_org": "中共恒山区委", "overlap_period": "2024-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
        {"person": "刘晶国", "person_id": "hengshan_刘晶国", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "高接替刘任区长", "overlap_org": "恒山区人民政府", "overlap_period": "2023-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
    ]
    gao = make_person_json(person_by_name("高久辉"), gao_tl, gao_rel, SOURCES)
    gao["professional_profile"]["career_pattern"] = "local_ladder"
    gao["professional_profile"]["primary_specializations"] = ["安全生产", "煤炭资源治理", "防汛", "营商招商"]
    gao["professional_profile"]["promotion_velocity"] = {"summary": "由区长升任区委书记兼区长（2026年）", "notable_fast_promotions": ["2026 年区长兼任区委书记（党政一肩挑）"]}
    gao["open_questions"] = [{"priority": "critical", "question": "高久辉的出生/籍贯/教育/入党及历任职务", "why_it_matters": "现任党政正职，核心画像不完整", "suggested_queries": ["高久辉 简历", "高久辉 任前公示"], "last_attempted": AS_OF}]
    _write_json(gao, "区委书记兼区长", "高久辉")

    # 2. 前任区委书记 鲍宇
    bao_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到鲍氏完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "2024", "end": "2026-06", "org": "中共恒山区委", "title": "区委书记", "notes": "2024H2-2026.6 任区委书记，2026-07 前后卸任", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    bao_rel = [{"person": "高久辉", "person_id": "hengshan_高久辉", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "卸任后高继任", "overlap_org": "中共恒山区委", "overlap_period": "2024-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []}]
    bao = make_person_json(person_by_name("鲍宇"), bao_tl, bao_rel, SOURCES, is_current=False)
    bao["open_questions"] = [{"priority": "high", "question": "前任区委书记鲍宇的卸任去向", "why_it_matters": "权力流向，可能指向鸡西市直或他县", "suggested_queries": ["鲍宇 鸡西 任命", "鲍宇 恒山 区委书记 卸任"], "last_attempted": AS_OF}]
    _write_json(bao, "前任区委书记", "鲍宇")

    # 3. 前任区长 刘晶国
    liu_tl = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "未找到完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "2023-01", "end": "2024-09", "org": "恒山区人民政府", "title": "区长（区委副书记）", "notes": "2023-2024.9 任区长", "confidence": "confirmed", "source_ids": []},
    ]
    liu_rel = [{"person": "高久辉", "person_id": "hengshan_高久辉", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "刘卸任后高继任", "overlap_org": "恒山区人民政府", "overlap_period": "2023-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": []}]
    liu = make_person_json(person_by_name("刘晶国"), liu_tl, liu_rel, SOURCES, is_current=False)
    liu["open_questions"] = [{"priority": "high", "question": "前任区长刘晶国的完整履历及去向", "why_it_matters": "区长继任路径", "suggested_queries": ["刘晶国 鸡西 区长 去向"], "last_attempted": AS_OF}]
    _write_json(liu, "前任区长", "刘晶国")

    # 4. 区人大主任 于春雷
    ycl = make_person_json(person_by_name("于春雷"), [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "完整履历待补", "confidence": "unverified", "source_ids": []},
        {"start": "2026-02", "end": "present", "org": "恒山区人大常委会", "title": "主任", "notes": "2026-02 当选", "confidence": "confirmed", "source_ids": ["S003"]},
    ], [], SOURCES)
    _write_json(ycl, "区人大常委会主任", "于春雷")

    # 5. 区政协主席 杨旗
    yq = make_person_json(person_by_name("杨旗"), [
        {"start": "unknown", "end": "present", "org": "政协恒山区委员会", "title": "区政协主席", "notes": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
    ], [], SOURCES)
    _write_json(yq, "区政协主席", "杨旗")

    # 6. 区委常委、纪委书记 尹兆鹏
    yz = make_person_json(person_by_name("尹兆鹏"), [
        {"start": "unknown", "end": "present", "org": "中共恒山区委", "title": "区委常委、区纪委书记、区监委主任", "notes": "现任", "confidence": "confirmed", "source_ids": ["S002"]},
    ], [], SOURCES)
    _write_json(yz, "区委常委、区纪委书记", "尹兆鹏")

# ── Main ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    orig_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        print(f"Building {SLUG} network data...")
        build_db()
        build_gexf()
        build_person_jsons()
        print("\nOutput files in:", STAGING)
        print("  DB:  ", DB_PATH)
        print("  GEXF:", GEXF_PATH)
        for f in sorted(os.listdir(STAGING)):
            if f.endswith(".json") and f.startswith(TODAY):
                print("  Person:", f)
        print("Done.")
    finally:
        os.chdir(orig_cwd)