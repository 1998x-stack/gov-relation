#!/usr/bin/env python3
"""Build script for 辽阳市弓长岭区 cadre exchange network investigation."""

import json
import os
import sqlite3

AS_OF = "2026-07-25"

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Find repo root: walk up until we find scripts/ and data/
_REPO = os.path.dirname(SCRIPT_DIR)
while _REPO and not (os.path.isdir(os.path.join(_REPO, "scripts")) and os.path.isdir(os.path.join(_REPO, "data"))):
    _REPO = os.path.dirname(_REPO)
REPO_ROOT = _REPO
TMP = os.path.join(REPO_ROOT, "data", "tmp", "liaoning_弓长岭区")
DB_PATH = os.path.join(TMP, "弓长岭区_network.db")
GEXF_PATH = os.path.join(TMP, "弓长岭区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──
persons = [
    # Core leaders
    {"id": 1, "name": "（待查）", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "弓长岭区委书记", "current_org": "中共辽阳市弓长岭区委员会",
     "source": ""},
    {"id": 2, "name": "李攀", "gender": "男", "ethnicity": "汉族", "birth": "1986-01", "birthplace": "",
     "education": "大学学历，硕士学位", "party_join": "", "work_start": "",
     "current_post": "弓长岭区委副书记、区长", "current_org": "弓长岭区人民政府",
     "source": "https://www.163.com/dy/article/KGVLLDKQ0514R9P4.html"},
    # Deputy leaders
    {"id": 3, "name": "苏洋", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "弓长岭区委常委、宣传部部长、区委教育工委书记", "current_org": "中共辽阳市弓长岭区委员会",
     "source": "https://www.163.com/dy/article/KGUJ6PSB05563DJA.html"},
    {"id": 4, "name": "李晖", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "弓长岭区政协主席", "current_org": "弓长岭区政协",
     "source": "https://www.163.com/dy/article/KGUJ6PSB05563DJA.html"},
    {"id": 5, "name": "曾庆飞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "弓长岭区政协副主席", "current_org": "弓长岭区政协",
     "source": "https://www.163.com/dy/article/KGUJ6PSB05563DJA.html"},
    {"id": 6, "name": "胡迎春", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "弓长岭区政协副主席", "current_org": "弓长岭区政协",
     "source": "https://www.163.com/dy/article/KGUJ6PSB05563DJA.html"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共辽阳市弓长岭区委员会", "type": "党委", "level": "县处级", "parent": "中共辽阳市委员会", "location": "辽阳市弓长岭区"},
    {"id": 2, "name": "弓长岭区人民政府", "type": "政府", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市弓长岭区"},
    {"id": 3, "name": "弓长岭区政协", "type": "政协", "level": "县处级", "parent": "辽阳市政协", "location": "辽阳市弓长岭区"},
    {"id": 4, "name": "弓长岭区人大常委会", "type": "人大", "level": "县处级", "parent": "辽阳市人大常委会", "location": "辽阳市弓长岭区"},
    {"id": 5, "name": "辽阳市融媒体中心（辽阳日报社、辽阳广播电视台）", "type": "事业单位", "level": "县处级", "parent": "中共辽阳市委员会", "location": "辽阳市"},
    {"id": 6, "name": "中共辽阳市弓长岭区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共辽阳市弓长岭区委员会", "location": "辽阳市弓长岭区"},
    {"id": 7, "name": "弓长岭区安平街道", "type": "乡镇/街道", "level": "乡科级", "parent": "弓长岭区人民政府", "location": "辽阳市弓长岭区"},
    {"id": 8, "name": "弓长岭区苏家街道", "type": "乡镇/街道", "level": "乡科级", "parent": "弓长岭区人民政府", "location": "辽阳市弓长岭区"},
    {"id": 9, "name": "弓长岭区汤河镇", "type": "乡镇/街道", "level": "乡科级", "parent": "弓长岭区人民政府", "location": "辽阳市弓长岭区"},
    {"id": 10, "name": "弓长岭区安平乡", "type": "乡镇/街道", "level": "乡科级", "parent": "弓长岭区人民政府", "location": "辽阳市弓长岭区"},
]

# ── Positions ──
positions = [
    # 区委书记 - unknown
    {"person_id": 1, "org_id": 1, "title": "弓长岭区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "现任区委书记信息待查"},
    # 李攀
    {"person_id": 2, "org_id": 1, "title": "弓长岭区委副书记", "start_date": "2025-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "弓长岭区区长", "start_date": "2025-12", "end_date": "present", "rank": "县处级正职",
     "note": "2025年12月16日区十届人大常委会第三十八次会议任命为副区长、代区长，后转正"},
    {"person_id": 2, "org_id": 6, "title": "弓长岭区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "此前任职"},
    {"person_id": 2, "org_id": 5, "title": "辽阳市融媒体中心党委书记、主任（社长、台长）", "start_date": "", "end_date": "2025-12", "rank": "县处级正职", "note": ""},
    # 苏洋
    {"person_id": 3, "org_id": 1, "title": "弓长岭区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "弓长岭区委宣传部部长、区委教育工委书记", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "接替李攀原职务"},
    # 李晖
    {"person_id": 4, "org_id": 3, "title": "弓长岭区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 曾庆飞
    {"person_id": 5, "org_id": 3, "title": "弓长岭区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 胡迎春
    {"person_id": 6, "org_id": 3, "title": "弓长岭区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "弓长岭区委书记（待查）与区长李攀组成弓长岭区党政正职搭档",
     "overlap_org": "弓长岭区党政班子", "overlap_period": "2025-12至今"},
    {"person_a": 2, "person_b": 3, "type": "前后任",
     "context": "李攀升任区长后，苏洋接任区委宣传部部长（区委教育工委书记）",
     "overlap_org": "弓长岭区委宣传部", "overlap_period": "2025-12后"},
    {"person_a": 2, "person_b": 4, "type": "工作关系",
     "context": "代区长李攀出席区政协十届十七次常委会议，与政协主席李晖同会",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 2, "person_b": 5, "type": "工作关系",
     "context": "代区长李攀与政协副主席曾庆飞同区政协会议出席",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 2, "person_b": 6, "type": "工作关系",
     "context": "代区长李攀与政协副主席胡迎春同区政协会议出席",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 3, "person_b": 4, "type": "工作关系",
     "context": "区委常委、宣传部部长苏洋与政协主席李晖同区政协会议出席",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 3, "person_b": 5, "type": "工作关系",
     "context": "苏洋与曾庆飞同区政协会议出席",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 3, "person_b": 6, "type": "工作关系",
     "context": "苏洋与胡迎春同区政协会议出席",
     "overlap_org": "弓长岭区政协会议", "overlap_period": "2025-12"},
    {"person_a": 4, "person_b": 5, "type": "同事",
     "context": "李晖与曾庆飞同为弓长岭区政协领导",
     "overlap_org": "弓长岭区政协", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 6, "type": "同事",
     "context": "李晖与胡迎春同为弓长岭区政协领导",
     "overlap_org": "弓长岭区政协", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 6, "type": "同事",
     "context": "曾庆飞与胡迎春同为弓长岭区政协副主席",
     "overlap_org": "弓长岭区政协", "overlap_period": "至今"},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(person, timeline_items, relationships_items, source_items, confidence_summary):
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "辽阳市", "region": "弓长岭区",
            "job": person.get("current_post", ""), "task_id": "liaoning_弓长岭区", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"gongchangling_{person['name']}", "name": person["name"], "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "", "education": [{"degree": person.get("education", "")}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级", "as_of": AS_OF,
            "is_current_confirmed": person["id"] != 1,  # party secretary unknown
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline_items,
        "organizations": [], "relationships": relationships_items,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "local_ladder" if person["id"] == 2 else "unknown",
            "systems_experience": ["propaganda"] if person["id"] == 2 else [],
            "geographic_pattern": []
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, no sufficient evidence available."
        },
        "risk_and_integrity_signals": [],
        "network_metrics": {},
        "source_register": source_items,
        "confidence_summary": confidence_summary,
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline for {person['name']}",
             "why_it_matters": "Core figure with incomplete public record",
             "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 弓长岭区 任职经历"],
             "last_attempted": AS_OF}
        ]
    }


def build():
    os.makedirs(TMP, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>辽阳市弓长岭区领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else False
        is_mayor = "区长" in post and "副" not in post
        is_discipline = "纪委" in post
        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"
        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")
        gexf_lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append(f'        <viz:shape value="{shape}"/>')
        gexf_lines.append('      </node>')
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        color_map = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
                      "政协": "255,240,200", "纪委": "255,200,150", "国企": "200,255,200",
                      "事业单位": "220,220,220", "乡镇/街道": "255,255,200"}
        ocolor = color_map.get(otype, "200,200,200")
        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')
    gexf_lines.append('    </nodes>')
    gexf_lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    for r in relationships:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')
    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs ──
    source_register = [
        {"id": "S001", "title": "辽阳市融媒体中心主任李攀出任辽阳市弓长岭区代理区长",
         "url": "https://www.163.com/dy/article/KGVLLDKQ0514R9P4.html",
         "publisher": "澎湃新闻/网易", "published_at": "2025-12-17", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high"},
        {"id": "S002", "title": "李攀任辽阳市弓长岭区委副书记、代区长",
         "url": "https://www.163.com/dy/article/KGUJ6PSB05563DJA.html",
         "publisher": "汲古知新/网易", "published_at": "2025-12-17", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high"},
        {"id": "S003", "title": "弓长岭区人民政府官方网站",
         "url": "http://www.gctl.gov.cn/",
         "publisher": "弓长岭区人民政府", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "网站无法访问（DNS解析失败）"},
    ]

    # Person JSON for 李攀 (区长)
    li_pan = next(p for p in persons if p["id"] == 2)
    timeline = [
        {"start": "", "end": "", "org": "中共辽阳市弓长岭区委宣传部",
         "title": "弓长岭区委常委、宣传部部长", "rank": "县处级副职",
         "location": "辽宁辽阳", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "", "end": "2025-12", "org": "辽阳市融媒体中心（辽阳日报社、辽阳广播电视台）",
         "title": "党委书记、主任（社长、台长）", "rank": "县处级正职",
         "location": "辽宁辽阳", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "2025-12", "end": "present", "org": "弓长岭区人民政府",
         "title": "弓长岭区委副书记、区长", "rank": "县处级正职",
         "location": "辽宁辽阳", "notes": "2025年12月16日区十届人大常委会第三十八次会议任命为副区长、代区长，后转正",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    rels = []
    for r in relationships:
        if r["person_a"] == 2:
            other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
            rels.append({"person": other, "relationship_type": r["type"],
                         "evidence": r["context"], "confidence": "confirmed"})
        elif r["person_b"] == 2:
            other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
            rels.append({"person": other, "relationship_type": r["type"],
                         "evidence": r["context"], "confidence": "confirmed"})
    pjson = make_person_json(li_pan, timeline, rels, source_register, {
        "identity": "confirmed", "current_role": "confirmed",
        "career_completeness": "partial", "relationship_confidence": "medium",
        "biggest_gap": "早期履历（大学毕业后至任宣传部部长前）完全空白"
    })
    p_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-辽宁省-辽阳市-区长-李攀.json")
    with open(p_path, "w", encoding="utf-8") as f:
        json.dump(pjson, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {p_path}")

    # Person JSON for 区委书记 (待查 - partial)
    shuji = next(p for p in persons if p["id"] == 1)
    pjson2 = make_person_json(shuji, [], [], source_register, {
        "identity": "unverified", "current_role": "unverified",
        "career_completeness": "thin", "relationship_confidence": "low",
        "biggest_gap": "现任弓长岭区委书记姓名、性别、出生年月、籍贯、履历等所有信息完全未知"
    })
    pjson2["open_questions"] = [
        {"priority": "critical", "question": "现任弓长岭区委书记姓名",
         "why_it_matters": "区委书记是区级核心领导（一把手），现完全未知",
         "suggested_queries": ["弓长岭区 区委书记", "弓长岭区 领导之窗", "弓长岭区 区委班子",
                              "gctl.gov.cn 领导分工"],
         "last_attempted": AS_OF},
        {"priority": "high", "question": "前任弓长岭区委书记姓名及去向",
         "why_it_matters": "了解干部更替时间线和跨区交流模式",
         "suggested_queries": ["弓长岭区 原区委书记", "弓长岭区 区委书记 任免"],
         "last_attempted": AS_OF},
    ]
    p_path2 = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-辽宁省-辽阳市-区委书记-待查.json")
    with open(p_path2, "w", encoding="utf-8") as f:
        json.dump(pjson2, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {p_path2}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
