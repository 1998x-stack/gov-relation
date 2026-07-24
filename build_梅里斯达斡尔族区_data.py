#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Meilisi Daur District (梅里斯达斡尔族区), Qiqihar, Heilongjiang.

Confirmed data from official government website (www.mls.gov.cn) as of 2026-07-24.
"""

import json
import os
import sqlite3
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = SCRIPT_DIR
DB_PATH = os.path.join(TMP, "梅里斯达斡尔族区_network.db")
GEXF_PATH = os.path.join(TMP, "梅里斯达斡尔族区_network.gexf")
PERSONS_DIR = os.path.join(TMP, "persons")

os.makedirs(PERSONS_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# DATA — All entries marked with confidence levels
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "郝宪庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市梅里斯达斡尔族区委书记",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委书记、区人武部党委第一书记。主持区委全面工作。"
    },
    {
        "id": 2,
        "name": "程凤杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "齐齐哈尔市梅里斯达斡尔族区委副书记、区长",
        "current_org": "齐齐哈尔市梅里斯达斡尔族区人民政府",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委副书记、区长。兼任区委领导。"
    },
    # ── Other Party Committee Members ──
    {
        "id": 3,
        "name": "于振伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委领导",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委领导成员，具体分工待确认"
    },
    {
        "id": 4,
        "name": "梁晓磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委领导",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委领导成员，具体分工待确认"
    },
    {
        "id": 5,
        "name": "刘文浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委领导",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委领导成员，具体分工待确认"
    },
    {
        "id": 6,
        "name": "庄体勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委常委、组织部部长",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会组织部",
        "source": "https://www.mls.gov.cn/mls/c102474/202607/c02_629647.shtml",
        "confidence": "confirmed",
        "notes": "区委常委、组织部部长。陪同区委书记郝宪庆走访慰问烈士遗属。"
    },
    {
        "id": 7,
        "name": "费春林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委领导",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委领导成员，具体分工待确认"
    },
    {
        "id": 8,
        "name": "杨宏宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梅里斯达斡尔族区委领导",
        "current_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
        "source": "https://www.mls.gov.cn/mls/c102481/xzf.shtml",
        "confidence": "confirmed",
        "notes": "区委领导成员，具体分工待确认"
    },
]

organizations = [
    {"id": 1, "name": "中共齐齐哈尔市梅里斯达斡尔族区委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 2, "name": "齐齐哈尔市梅里斯达斡尔族区人民政府", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 3, "name": "齐齐哈尔市梅里斯达斡尔族区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 4, "name": "中国人民政治协商会议齐齐哈尔市梅里斯达斡尔族区委员会", "type": "政协", "level": "县处级",
     "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 5, "name": "中共齐齐哈尔市梅里斯达斡尔族区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市纪律检查委员会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 6, "name": "中共齐齐哈尔市梅里斯达斡尔族区委组织部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市梅里斯达斡尔族区委员会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 7, "name": "中共齐齐哈尔市梅里斯达斡尔族区委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市梅里斯达斡尔族区委员会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 8, "name": "中共齐齐哈尔市梅里斯达斡尔族区委政法委", "type": "党委", "level": "县处级",
     "parent": "中共齐齐哈尔市梅里斯达斡尔族区委员会", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
    {"id": 9, "name": "齐齐哈尔市梅里斯达斡尔族区人民武装部", "type": "政府", "level": "县处级",
     "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市梅里斯达斡尔族区"},
]

positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "齐齐哈尔市梅里斯达斡尔族区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "区委书记、区人武部党委第一书记"},
    {"person_id": 2, "org_id": 2, "title": "齐齐哈尔市梅里斯达斡尔族区委副书记、区长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "区委副书记、区政府区长"},
    {"person_id": 2, "org_id": 1, "title": "梅里斯达斡尔族区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委副书记"},  # Also deputy secretary of the party committee
    {"person_id": 3, "org_id": 1, "title": "梅里斯达斡尔族区委领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委领导成员"},
    {"person_id": 4, "org_id": 1, "title": "梅里斯达斡尔族区委领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委领导成员"},
    {"person_id": 5, "org_id": 1, "title": "梅里斯达斡尔族区委领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委领导成员"},
    {"person_id": 6, "org_id": 6, "title": "梅里斯达斡尔族区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委常委、组织部部长"},
    {"person_id": 7, "org_id": 1, "title": "梅里斯达斡尔族区委领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委领导成员"},
    {"person_id": 8, "org_id": 1, "title": "梅里斯达斡尔族区委领导",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区委领导成员"},
]

relationships = [
    # 郝宪庆 — 程凤杰: top two leaders working together
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长搭档，共同主持区委、区政府全面工作",
     "overlap_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
     "overlap_period": "2026年当前"},
    # 郝宪庆 — 庄体勇: secretary + organization department head
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与组织部部长共同走访慰问（2026年6月30日）",
     "overlap_org": "中共齐齐哈尔市梅里斯达斡尔族区委员会",
     "overlap_period": "2026年当前"},
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
    lines.append('    <description>梅里斯达斡尔族区领导班子关系网络 — 黑龙江省齐齐哈尔市梅里斯达斡尔族区</description>')
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
    safe_name = person["name"]
    # Extract short job title
    post = person["current_post"]
    if "区委书记" in post:
        job = "区委书记"
    elif "区长" in post:
        job = "区长"
    elif "区委常委" in post:
        job = "区委常委"
    else:
        job = "区委领导"
    filename = f"{today}-黑龙江省-齐齐哈尔市-{job}-{safe_name}.json"
    filename = filename.replace(" ", "").replace("/", "_")
    filepath = os.path.join(PERSONS_DIR, filename)

    # Build source register
    source_register = []
    sid = 0

    # Determine source URLs
    if "xzf.shtml" in person["source"]:
        sid += 1
        source_register.append({
            "id": f"S{sid:03d}",
            "title": "梅里斯达斡尔族区人民政府—领导之窗",
            "url": person["source"],
            "publisher": "梅里斯达斡尔族区人民政府",
            "published_at": "",
            "accessed_at": datetime.now().strftime("%Y-%m-%d"),
            "source_type": "official",
            "reliability": "high",
            "notes": "区委领导名单"
        })
        sid += 1
        source_register.append({
            "id": f"S{sid:03d}",
            "title": "梅里斯达斡尔族区人民政府—首页",
            "url": "https://www.mls.gov.cn/",
            "publisher": "梅里斯达斡尔族区人民政府",
            "published_at": "",
            "accessed_at": datetime.now().strftime("%Y-%m-%d"),
            "source_type": "official",
            "reliability": "high",
            "notes": "首页新闻报道确认领导姓名"
        })
    else:
        source_register.append({
            "id": "S001",
            "title": "梅里斯达斡尔族区人民政府",
            "url": "https://www.mls.gov.cn/",
            "publisher": "梅里斯达斡尔族区人民政府",
            "published_at": "",
            "accessed_at": datetime.now().strftime("%Y-%m-%d"),
            "source_type": "official",
            "reliability": "high",
            "notes": ""
        })

    is_confirmed = person["confidence"] == "confirmed"
    career_completeness = "thin" if is_confirmed else "thin"

    data = {
        "schema_version": "1.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "齐齐哈尔市",
            "region": "梅里斯达斡尔族区",
            "job": person["current_post"],
            "task_id": "heilongjiang_梅里斯达斡尔族区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"qqhr_meilisi_{person['id']}_{person['name']}",
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
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "https://www.mls.gov.cn/mls/c102481/xzf.shtml"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级正职" if is_top_leader(person["current_post"]) else "县处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": is_confirmed,
            "source_ids": [s["id"] for s in source_register]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": person["current_post"],
                "notes": f"当前职务为{person['current_post']}，完整履历尚未获取",
                "confidence": "confirmed" if is_confirmed else "unverified",
                "source_ids": [s["id"] for s in source_register]
            }
        ],
        "organizations": [
            {
                "org": person["current_org"],
                "role": person["current_post"],
                "period": "",
                "confidence": "confirmed" if is_confirmed else "unverified",
                "source_ids": [s["id"] for s in source_register]
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
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if is_confirmed else "unverified",
            "current_role": "confirmed" if is_confirmed else "unverified",
            "career_completeness": career_completeness,
            "relationship_confidence": "low",
            "biggest_gap": "完整履历、出生信息、教育背景、籍贯等信息缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']} ({person['current_post']})的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "这是本次调研的核心人物，基本身份信息",
                "suggested_queries": [
                    f"郝宪庆 简历 梅里斯",
                    f"程凤杰 简历 梅里斯",
                    f"{person['name']} 梅里斯达斡尔族区",
                    f"{person['name']} 任前公示 齐齐哈尔"
                ],
                "last_attempted": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "priority": "high",
                "question": f"{person['name']}的完整职业履历是什么？",
                "why_it_matters": "履历是分析工作关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 任职经历",
                    f"{person['name']} 此前 担任",
                    f"{person['name']} 齐齐哈尔"
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
    content = f"""# Open Gaps Registry — 梅里斯达斡尔族区补充
> Added: {today}

## ⭐⭐⭐⭐⭐ Critical (core figures with major career gaps)

| Person | Current Role | What's Missing | Last Attempted | Notes |
|--------|-------------|----------------|----------------|-------|
| 郝宪庆 | 梅里斯达斡尔族区委书记 | 出生年月、籍贯、教育、完整履历 | {today} | 姓名已从官方确认，但履历空白 |
| 程凤杰 | 梅里斯达斡尔族区长 | 出生年月、籍贯、教育、完整履历 | {today} | 姓名已从官方确认，但履历空白 |

## ⭐⭐⭐⭐ High (important deputies)

| Person/Gap | What's Missing | Last Attempted | Notes |
|-----------|----------------|----------------|-------|
| 于振伟 | 具体职务分工、履历 | {today} | 区委领导成员，分工待确认 |
| 梁晓磊 | 具体职务分工、履历 | {today} | 区委领导成员，分工待确认 |
| 刘文浩 | 具体职务分工、履历 | {today} | 区委领导成员，分工待确认 |
| 庄体勇 | 完整履历 | {today} | 组织部部长，仅职务确认 |
| 费春林 | 具体职务分工、履历 | {today} | 区委领导成员，分工待确认 |
| 杨宏宇 | 具体职务分工、履历 | {today} | 区委领导成员，分工待确认 |

## ⭐⭐⭐ Medium (leadership roster gaps)

| Gap | Last Attempted | Notes |
|-----|----------------|-------|
| 区政府副区长名单 | {today} | 政府领导班子成员完全未知 |
| 区人大主任 | {today} | 人大领导未知 |
| 区政协主席 | {today} | 政协领导未知 |
| 前任区委书记 | {today} | 前任信息完全未知 |
| 前任区长 | {today} | 前任信息完全未知 |
| 区纪委书记 | {today} | 纪委领导未知 |
| 区委政法委书记 | {today} | 政法委书记未知 |
| 区委宣传部部长 | {today} | 宣传部长未知 |

## ⭐⭐ Low (nice to have)

| Gap | Last Attempted | Notes |
|-----|----------------|-------|
| 梅里斯与齐齐哈尔其他区县干部交流模式 | {today} | 发现跨区调动需要对照研究 |
"""
    gap_path = os.path.join(TMP, "open_gaps.md")
    with open(gap_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Open gaps: {gap_path}")


def write_report():
    """Write the investigation report."""
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# 齐齐哈尔市梅里斯达斡尔族区领导班子工作关系网络调查报告
> 生成日期：{today}

## 说明

本报告基于**官方政府网站**（www.mls.gov.cn）公开信息编写。领导姓名已通过"领导之窗"页面和新闻报道双重确认。

## 1. 概况

- **地区**：黑龙江省齐齐哈尔市梅里斯达斡尔族区
- **行政级别**：市辖区（县处级）
- **调研任务**：heilongjiang_梅里斯达斡尔族区
- **目标**：区委书记 & 区长
- **信息来源**：[梅里斯达斡尔族区人民政府](https://www.mls.gov.cn/)

## 2. 当前核心领导

| 职务 | 姓名 | 状态 | 来源 |
|------|------|------|------|
| 梅里斯达斡尔族区委书记、区人武部党委第一书记 | **郝宪庆** | ✅ 已确认 | [领导之窗](https://www.mls.gov.cn/mls/c102481/xzf.shtml) |
| 梅里斯达斡尔族区委副书记、区长 | **程凤杰** | ✅ 已确认 | [领导之窗](https://www.mls.gov.cn/mls/c102481/xzf.shtml) + [新闻报道](https://www.mls.gov.cn/mls/c102474/202607/c02_629647.shtml) |

### 区委书记郝宪庆

- **职务**：梅里斯达斡尔族区委书记、区人武部党委第一书记
- **分工**：主持区委全面工作，负责军事工作
- **公开活动**：
  - 2026年7月：调研防汛工作（[报道](https://www.mls.gov.cn/mls/c102474/202607/c02_631567.shtml)）（[另一次](https://www.mls.gov.cn/mls/c102474/202607/c02_630924.shtml)）
  - 2026年6月：检查中考组织保障工作
  - 2026年6月30日：走访慰问烈士遗属、老干部、困难党员代表
- **履历**：待补充

### 区长程凤杰

- **职务**：区委副书记、区长
- **公开活动**：
  - 2026年6月30日：走访慰问困难党员
  - "七一"前夕：陪同走访慰问

## 3. 区委领导成员

根据[领导之窗](https://www.mls.gov.cn/mls/c102481/xzf.shtml)页面信息，区委领导成员包括：

| 姓名 | 职务 | 备注 |
|------|------|------|
| 郝宪庆 | 区委书记 | 主持区委全面工作 |
| 程凤杰 | 区委副书记、区长 | 区政府负责人 |
| 于振伟 | 区委领导 | 具体分工待确认 |
| 梁晓磊 | 区委领导 | 具体分工待确认 |
| 刘文浩 | 区委领导 | 具体分工待确认 |
| 庄体勇 | 区委常委、组织部部长 | 组织工作 |
| 费春林 | 区委领导 | 具体分工待确认 |
| 杨宏宇 | 区委领导 | 具体分工待确认 |

## 4. 前任领导（未知）

| 职务 | 前任 | 去向 |
|------|------|------|
| 前任梅里斯达斡尔族区委书记 | 待确认 | 待确认 |
| 前任梅里斯达斡尔族区长 | 待确认 | 待确认 |

## 5. 近期人事变动

该区近日召开了第十二届人大常委会第三十三次会议（2026年7月），具体任免事项待查阅。

## 6. 工作关系网络分析

### 已知交集

| 人员A | 人员B | 关系类型 | 证据 |
|-------|-------|---------|------|
| 郝宪庆 | 程凤杰 | 书记与区长搭档 | 官方领导名单，共同参加七一慰问活动 |
| 郝宪庆 | 庄体勇 | 书记与组织部部长 | 2026年6月30日共同走访慰问 |

### 网络弱项
- 区政府副区长名单完全缺失
- 区人大、政协领导班子未知
- 区委其他常委的具体分工未公示

## 7. 周边县区人事交流（待探索）

梅里斯达斡尔族区与其他齐齐哈尔市辖区（龙沙区、建华区、铁锋区等）之间的干部交流情况待探索。

## 8. 关键洞察与建议

### 已确认
1. ✅ **区委书记郝宪庆** — 已通过官方领导之窗和新闻报道双重确认
2. ✅ **区长程凤杰** — 已确认

### 优先行动
1. **补充核心人物履历**：通过齐齐哈尔市委组织部任前公示、百度百科等渠道获取郝宪庆和程凤杰的完整履历
2. **获取完整领导班子**：从领导之窗页面获取所有区委常委的具体分工
3. **查询政府领导班子**：查找区政府副区长名单
4. **查询前任信息**：了解郝宪庆和程凤杰的前任情况

## 9. 数据文件说明

| 文件 | 路径 | 说明 |
|------|------|------|
| 构建脚本 | build_梅里斯达斡尔族区_data.py | 数据库和图生成脚本 |
| SQLite 数据库 | 梅里斯达斡尔族区_network.db | 结构化关系数据 |
| GEXF 图 | 梅里斯达斡尔族区_network.gexf | 可导入 Gephi 的关系图 |
| 个人档案 | persons/*.json | 核心人物深度档案 |

## 10. 信息来源

| 来源 | URL | 类型 |
|------|-----|------|
| 梅里斯达斡尔族区人民政府 | https://www.mls.gov.cn/ | 官方 |
| 领导之窗 | https://www.mls.gov.cn/mls/c102481/xzf.shtml | 官方 |
| 七一走访慰问报道 | https://www.mls.gov.cn/mls/c102474/202607/c02_629647.shtml | 官方 |
| 防汛工作报道 | https://www.mls.gov.cn/mls/c102474/202607/c02_631567.shtml | 官方 |
| 齐齐哈尔市人民政府 | https://www.qqhr.gov.cn/ | 官方 |

---
*本报告信息截至2026年7月24日。核心领导姓名已确认，履历信息待补充。*
"""
    report_path = os.path.join(TMP, "20260724-黑龙江省-齐齐哈尔市-梅里斯达斡尔族区-领导班子调查报告.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Report: {report_path}")


if __name__ == "__main__":
    print("Building 梅里斯达斡尔族区 network data...\n")

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
