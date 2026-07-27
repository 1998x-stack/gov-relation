#!/usr/bin/env python3
"""Build script for 柳州市城中区 cadre exchange network investigation."""

import json
import os
import sqlite3

AS_OF = "2026-07-22"

# Paths
TMP = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tmp", "guangxi_城中区")
DB_PATH = os.path.join(TMP, "guangxi_城中区.db")
GEXF_PATH = os.path.join(TMP, "guangxi_城中区.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──
persons = [
    {"id": 1, "name": "宋军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区委书记", "current_org": "中共柳州市城中区委员会",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/qz/zyjhhhd/t19700101_3529365.shtml"},
    {"id": 2, "name": "周水祥", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区区长", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/qz/zyjhhhd/t19700101_3529365.shtml"},
    {"id": 3, "name": "姚良", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区人大常委会主任", "current_org": "城中区人大常委会",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/qz/zyjhhhd/t19700101_3529365.shtml"},
    {"id": 4, "name": "栗庆耀", "gender": "男", "ethnicity": "汉", "birth": "1981-10", "birthplace": "陕西旬阳",
     "education": "研究生", "party_join": "2007-06", "work_start": "2008-04",
     "current_post": "城中区委常委、副区长（常务）", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/czqfqz/202601/t20260105_3709865.shtml"},
    {"id": 5, "name": "韦文学", "gender": "男", "ethnicity": "汉", "birth": "1980-12", "birthplace": "广西融安",
     "education": "本科", "party_join": "2007-12", "work_start": "2003-07",
     "current_post": "城中区副区长、城中公安分局局长", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/czqfqz/202602/t20260202_3720093.shtml"},
    {"id": 6, "name": "亓树思", "gender": "男", "ethnicity": "", "birth": "1982-12", "birthplace": "山东临沂",
     "education": "研究生理学硕士", "party_join": "2006-11", "work_start": "2008-06",
     "current_post": "城中区副区长", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/czqfqz/t19700101_3577361.shtml"},
    {"id": 7, "name": "占平", "gender": "男", "ethnicity": "汉", "birth": "1979-09", "birthplace": "湖北浠水",
     "education": "本科", "party_join": "2004-11", "work_start": "2002-07",
     "current_post": "城中区副区长", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/czqfqz/202111/t20211104_2949028.shtml"},
    {"id": 8, "name": "李敏", "gender": "女", "ethnicity": "汉", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区副区长", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/czqfqz/202509/t20250923_3671195.shtml"},
    {"id": 9, "name": "唐宏虎", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区政府党组成员", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/dzcy/lists.shtml"},
    {"id": 10, "name": "张光禄", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "城中区政府党组成员", "current_org": "城中区人民政府",
     "source": "http://www.czq.gov.cn/xxgk/qzfld/dzcy/lists.shtml"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共柳州市城中区委员会", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会", "location": "柳州市城中区"},
    {"id": 2, "name": "城中区人民政府", "type": "政府", "level": "县处级", "parent": "柳州市人民政府", "location": "柳州市城中区"},
    {"id": 3, "name": "城中区人大常委会", "type": "人大", "level": "县处级", "parent": "柳州市人大常委会", "location": "柳州市城中区"},
    {"id": 4, "name": "城中公安分局", "type": "政府", "level": "乡科级", "parent": "柳州市公安局", "location": "柳州市城中区"},
    {"id": 5, "name": "柳州市商贸控股有限责任公司", "type": "国企", "level": "乡科级", "parent": "", "location": "柳州市"},
    {"id": 6, "name": "柳州市人民政府办公室", "type": "政府", "level": "县处级", "parent": "柳州市人民政府", "location": "柳州市"},
    {"id": 7, "name": "中共柳州市委办公室", "type": "党委", "level": "县处级", "parent": "中共柳州市委员会", "location": "柳州市"},
    {"id": 8, "name": "柳州市自然资源和规划局", "type": "政府", "level": "县处级", "parent": "柳州市人民政府", "location": "柳州市"},
    {"id": 9, "name": "柳州市国土资源执法监察支队", "type": "政府", "level": "乡科级", "parent": "柳州市自然资源和规划局", "location": "柳州市"},
    {"id": 10, "name": "柳州市田长制办公室", "type": "政府", "level": "乡科级", "parent": "柳州市自然资源和规划局", "location": "柳州市"},
    {"id": 11, "name": "城中区政协", "type": "政协", "level": "县处级", "parent": "柳州市政协", "location": "柳州市城中区"},
]

# ── Positions ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "城中区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "城中区区长", "start_date": "2024-09", "end_date": "present", "rank": "县处级正职",
     "note": "2024年9月13日城中区十三届人大五次会议当选区长"},
    {"person_id": 3, "org_id": 3, "title": "城中区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "城中区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "城中区副区长（常务）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "城中区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "城中公安分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "城中区副区长", "start_date": "2024-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 9, "title": "柳州市国土资源执法监察支队科员→主任科员", "start_date": "2008-06", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "柳州市自然资源和规划局科室负责人", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "历任国土空间用途管制科科长、建设项目规划科科长"},
    {"person_id": 6, "org_id": 10, "title": "柳州市田长制办公室专职副主任", "start_date": "", "end_date": "2024-12", "rank": "乡科级正职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "城中区副区长", "start_date": "2021-07", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "柳州市商贸控股有限公司主管→办公室副主任", "start_date": "2002-07", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "柳州市人民政府办公室秘书", "start_date": "", "end_date": "", "rank": "乡科级",
     "note": "历任第二秘书科干部、第四秘书科科员、副科长"},
    {"person_id": 7, "org_id": 7, "title": "柳州市委办公室政策法规科科长→第三秘书科科长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "城中区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "城中区政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "城中区政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "宋军为区委书记、周水祥为区长，组成城中区党政正职搭档",
     "overlap_org": "城中区党政班子", "overlap_period": "2024-09至今"},
    {"person_a": 1, "person_b": 3, "type": "同届领导",
     "context": "宋军（区委书记）和姚良（区人大常委会主任）共同主持区十三届人大五次会议",
     "overlap_org": "城中区人大会议", "overlap_period": "2024-09"},
    {"person_a": 2, "person_b": 3, "type": "选举关系",
     "context": "周水祥经区十三届人大五次会议选举为区长，姚良作为人大常委会主任主持选举",
     "overlap_org": "城中区人大", "overlap_period": "2024-09"},
    {"person_a": 4, "person_b": 5, "type": "同事",
     "context": "栗庆耀（常务副区长）与韦文学（副区长兼公安局长）同在城中区政府班子",
     "overlap_org": "城中区人民政府", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 7, "type": "同事",
     "context": "亓树思与占平同为城中区副区长",
     "overlap_org": "城中区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 6, "person_b": 8, "type": "同事",
     "context": "亓树思与李敏同为城中区副区长",
     "overlap_org": "城中区人民政府", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 6, "type": "同事", "context": "占平与亓树思同在城中区政府班子",
     "overlap_org": "城中区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 7, "person_b": 4, "type": "同事", "context": "占平与栗庆耀同在城中区政府班子",
     "overlap_org": "城中区人民政府", "overlap_period": "2021-07至今"},
    {"person_a": 5, "person_b": 6, "type": "同事", "context": "韦文学与亓树思同在城中区政府班子",
     "overlap_org": "城中区人民政府", "overlap_period": "2024-12至今"},
    {"person_a": 4, "person_b": 8, "type": "同事", "context": "栗庆耀与李敏同在城中区政府班子",
     "overlap_org": "城中区人民政府", "overlap_period": "至今"},
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def make_person_json(person, timeline_items, relationships_items, source_items):
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区", "city": "柳州市", "region": "城中区",
            "job": person.get("current_post", ""), "task_id": "guangxi_城中区", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"chengzhongqu_{person['name']}", "name": person["name"], "aliases": [],
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
            "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]
        },
        "career_timeline": timeline_items,
        "organizations": [], "relationships": relationships_items,
        "governance_record": [], "professional_profile": {
            "primary_specializations": [], "career_pattern": "", "systems_experience": [], "geographic_pattern": []
        },
        "source_register": source_items,
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline before current role for {person['name']}",
             "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历"]}
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
    gexf_lines.append('    <description>柳州市城中区领导班子关系网络（跨区干部交流）</description>')
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
        is_mayor = post in ["城中区区长"] or "区长" in post and "副" not in post
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
                      "政协": "255,240,200", "纪委": "255,200,150", "国企": "200,255,200"}
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
        {"id": "S001", "title": "城中区十三届人大五次会议闭幕，周水祥当选区长",
         "url": "http://www.czq.gov.cn/xxgk/qzfld/qz/zyjhhhd/t19700101_3529365.shtml",
         "publisher": "城中区人民政府", "published_at": "2024-09-13", "accessed_at": AS_OF,
         "source_type": "government", "reliability": "high"},
        {"id": "S002", "title": "城中区人民政府——区政府领导页面",
         "url": "http://www.czq.gov.cn/xxgk/qzfld/", "publisher": "城中区人民政府",
         "accessed_at": AS_OF, "source_type": "government", "reliability": "high"},
    ]
    # Person JSONs for key figures
    for p in persons:
        if p["name"] in ["周水祥", "宋军", "栗庆耀", "占平", "亓树思"]:
            timeline = []
            for pos in positions:
                if pos["person_id"] == p["id"]:
                    org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
                    timeline.append({
                        "start": pos.get("start_date", ""), "end": pos.get("end_date", ""),
                        "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                        "location": "广西柳州", "notes": pos.get("note", ""),
                        "confidence": "confirmed", "source_ids": ["S001", "S002"]
                    })
            rels = []
            for r in relationships:
                if r["person_a"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                    rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "confidence": "confirmed"})
                elif r["person_b"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                    rels.append({"person": other, "relationship_type": r["type"], "evidence": r["context"], "confidence": "confirmed"})
            pjson = make_person_json(p, timeline, rels, source_register)
            p_path = os.path.join(PERSONS_DIR, f"{AS_OF_SHORT}-广西壮族自治区-柳州市城中区-{p['current_post']}-{p['name']}.json")
            with open(p_path, "w", encoding="utf-8") as f:
                json.dump(pjson, f, ensure_ascii=False, indent=2)
            print(f"Person JSON written: {p_path}")

    print("\nBuild complete.")


if __name__ == "__main__":
    build()
