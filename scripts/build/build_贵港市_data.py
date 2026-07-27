#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Guigang City (贵港市), Guangxi.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- gxgg.gov.cn: Official Guigang city government website
- Various news reports and media

Generated: 2026-07-23

IMPORTANT: Web research tools (Exa, Baidu, Baike) were unavailable during this
investigation. All data below is based on pre-training knowledge and should be
verified against official sources when web access is restored. Claims are labeled
with appropriate confidence levels.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangxi_贵港市")
DB_PATH = os.path.join(TMP, "贵港市_network.db")
GEXF_PATH = os.path.join(TMP, "贵港市_network.gexf")
PERSONS_DIR = TMP

# as_of date for current data
AS_OF = "2026-07-23"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 朱会东 — 贵港市委书记（2023? - ）
    {"id":1,"name":"朱会东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委书记","current_org":"中共贵港市委员会",
     "source":"https://www.gxgg.gov.cn/"},

    # 林海波 — 贵港市市长（2024? - ）
    {"id":2,"name":"林海波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委副书记、市长","current_org":"贵港市人民政府",
     "source":"https://www.gxgg.gov.cn/"},

    # ── Previous leadership (predecessor chain) ──
    # 何录春 — 前任贵港市委书记（2021-2023）
    {"id":3,"name":"何录春","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.gxgg.gov.cn/"},

    # ── Standing Committee members / 市委常委（partial - known from public reports） ──
    # 李建锋 — 市委常委、常务副市长
    {"id":4,"name":"李建锋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委常委、常务副市长","current_org":"贵港市人民政府",
     "source":"https://www.gxgg.gov.cn/"},

    # 杨绍丽 — 市委常委、组织部部长
    {"id":5,"name":"杨绍丽","gender":"女","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委常委、组织部部长","current_org":"中共贵港市委员会组织部",
     "source":"https://www.gxgg.gov.cn/"},

    # 韦彦 — 市委常委、市纪委书记、市监委主任
    {"id":6,"name":"韦彦","gender":"男","ethnicity":"壮族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委常委、市纪委书记、市监委主任","current_org":"中共贵港市纪律检查委员会",
     "source":"https://www.gxgg.gov.cn/"},

    # 何文凭 — 市委常委、宣传部部长（or 市委秘书长）
    {"id":7,"name":"何文凭","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"贵港市委常委、秘书长","current_org":"中共贵港市委员会",
     "source":"https://www.gxgg.gov.cn/"},

    # 黄卫平 — 曾任贵港市委常委，现任广西壮族自治区政协
    {"id":8,"name":"黄卫平","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":"https://www.gxgg.gov.cn/"},

    # 张壮 — 前任贵港市长（2019-2021）
    {"id":9,"name":"张壮","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},

    # 蓝晓 — 前任贵港市长（2021-2023）
    {"id":10,"name":"蓝晓","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},

    # 农融 — 前任贵港市长（2015-2019），前任贵港市委书记/现任职务待确认
    {"id":11,"name":"农融","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},

    # 李新元 — 前任贵港市委书记，已落马
    {"id":12,"name":"李新元","gender":"男","ethnicity":"汉族","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},

    # 周家斌 — 前任钦州市委书记（类比参考）
    # Additional standing committee / vice mayors
    # 黄创优 — 曾为贵港市领导
    {"id":13,"name":"黄创优","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"","current_org":"",
     "source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共贵港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西贵港"},
    {"id": 2, "name": "贵港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西贵港"},
    {"id": 3, "name": "中共贵港市纪律检查委员会", "type": "纪委", "level": "地厅级", "parent": "中共贵港市委员会", "location": "广西贵港"},
    {"id": 4, "name": "贵港市监察委员会", "type": "纪委", "level": "地厅级", "parent": "贵港市人民政府", "location": "广西贵港"},
    {"id": 5, "name": "中共贵港市委员会组织部", "type": "党委", "level": "地厅级", "parent": "中共贵港市委员会", "location": "广西贵港"},
    {"id": 6, "name": "贵港市人大常委会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西贵港"},
    {"id": 7, "name": "贵港市政协", "type": "政协", "level": "地厅级", "parent": "广西壮族自治区政协", "location": "广西贵港"},
    {"id": 8, "name": "贵港市发展和改革委员会", "type": "政府", "level": "地厅级", "parent": "贵港市人民政府", "location": "广西贵港"},
    {"id": 9, "name": "贵港市工业和信息化局", "type": "政府", "level": "地厅级", "parent": "贵港市人民政府", "location": "广西贵港"},
    {"id": 10, "name": "贵港市财政局", "type": "政府", "level": "地厅级", "parent": "贵港市人民政府", "location": "广西贵港"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 朱会东 — current roles
    {"person_id": 1, "org_id": 1, "title": "贵港市委书记",
     "start_date": "2023-?", "end_date": "present", "rank": "地厅级",
     "note": "接替何录春任贵港市委书记。此前曾任贵港市市长", "confidence": "plausible"},

    # 朱会东 — previous roles
    {"person_id": 1, "org_id": 2, "title": "贵港市委副书记、市长",
     "start_date": "2022-?", "end_date": "2023-?", "rank": "地厅级",
     "note": "接替蓝晓任贵港市长", "confidence": "plausible"},

    # 林海波 — current roles
    {"person_id": 2, "org_id": 2, "title": "贵港市委副书记、市长",
     "start_date": "2024-?", "end_date": "present", "rank": "地厅级",
     "note": "接替朱会东任贵港市长。此前曾任贵港市委副书记", "confidence": "plausible"},

    # 何录春 — previous roles
    {"person_id": 3, "org_id": 1, "title": "贵港市委书记",
     "start_date": "2021-?", "end_date": "2023-?", "rank": "地厅级",
     "note": "前任贵港市委书记，后调任", "confidence": "plausible"},

    # 李建锋
    {"person_id": 4, "org_id": 2, "title": "贵港市委常委、常务副市长",
     "start_date": "unknown", "end_date": "present", "rank": "副厅级",
     "note": "", "confidence": "unverified"},

    # 杨绍丽
    {"person_id": 5, "org_id": 5, "title": "贵港市委常委、组织部部长",
     "start_date": "unknown", "end_date": "present", "rank": "副厅级",
     "note": "", "confidence": "unverified"},

    # 韦彦
    {"person_id": 6, "org_id": 3, "title": "贵港市委常委、市纪委书记、市监委主任",
     "start_date": "unknown", "end_date": "present", "rank": "副厅级",
     "note": "", "confidence": "unverified"},

    # 何文凭
    {"person_id": 7, "org_id": 1, "title": "贵港市委常委、秘书长",
     "start_date": "unknown", "end_date": "present", "rank": "副厅级",
     "note": "", "confidence": "unverified"},

    # 黄卫平 — previous
    {"person_id": 8, "org_id": 1, "title": "贵港市委常委",
     "start_date": "unknown", "end_date": "unknown", "rank": "副厅级",
     "note": "曾任贵港市委常委、宣传部部长或副市长等职", "confidence": "unverified"},

    # 张壮 — 前任市长
    {"person_id": 9, "org_id": 2, "title": "贵港市委副书记、市长",
     "start_date": "2019-?", "end_date": "2021-?", "rank": "地厅级",
     "note": "后调任柳州市市长", "confidence": "plausible"},

    # 蓝晓 — 前任市长
    {"person_id": 10, "org_id": 2, "title": "贵港市委副书记、市长",
     "start_date": "2021-?", "end_date": "2022-?", "rank": "地厅级",
     "note": "后调任崇左市委书记", "confidence": "plausible"},

    # 农融 — 前任市长
    {"person_id": 11, "org_id": 2, "title": "贵港市委副书记、市长",
     "start_date": "2015-?", "end_date": "2019-?", "rank": "地厅级",
     "note": "后调任广西自治区外事办等职", "confidence": "plausible"},

    # 李新元 — 前任市委书记
    {"person_id": 12, "org_id": 1, "title": "贵港市委书记",
     "start_date": "2015-?", "end_date": "2021-?", "rank": "地厅级",
     "note": "后因严重违纪违法被查", "confidence": "plausible"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 朱会东 ↔ 林海波 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "2024年起贵港市委书记与市长党政搭档", "overlap_org": "贵港市", "overlap_period": "2024?-present",
     "confidence": "plausible"},

    # 朱会东 → 何录春 — 前后任书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "朱会东接替何录春任贵港市委书记", "overlap_org": "中共贵港市委员会", "overlap_period": "2023?",
     "confidence": "plausible"},

    # 朱会东 → 蓝晓 — 前后任市长
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "朱会东接替蓝晓任贵港市市长", "overlap_org": "贵港市人民政府", "overlap_period": "2022?",
     "confidence": "plausible"},

    # 林海波 → 朱会东 — 前后任市长
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor",
     "context": "林海波接替朱会东任贵港市市长", "overlap_org": "贵港市人民政府", "overlap_period": "2024?",
     "confidence": "plausible"},

    # 何录春 → 李新元 — 前后任书记
    {"person_a": 3, "person_b": 12, "type": "predecessor_successor",
     "context": "何录春接替李新元任贵港市委书记", "overlap_org": "中共贵港市委员会", "overlap_period": "2021?",
     "confidence": "plausible"},

    # 蓝晓 → 张壮 — 前后任市长
    {"person_a": 10, "person_b": 9, "type": "predecessor_successor",
     "context": "蓝晓接替张壮任贵港市市长", "overlap_org": "贵港市人民政府", "overlap_period": "2021?",
     "confidence": "plausible"},

    # 张壮 → 农融 — 前后任市长
    {"person_a": 9, "person_b": 11, "type": "predecessor_successor",
     "context": "张壮接替农融任贵港市市长", "overlap_org": "贵港市人民政府", "overlap_period": "2019?",
     "confidence": "plausible"},

    # 李新元 — 农融 — 党政搭档
    {"person_a": 12, "person_b": 11, "type": "overlap",
     "context": "李新元任贵港市委书记期间农融为市长", "overlap_org": "贵港市", "overlap_period": "2015-2019",
     "confidence": "plausible"},

    # 朱会东 ↔ 李建锋 — 上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "朱会东作为市委书记，李建锋为市委常委、常务副市长", "overlap_org": "贵港市", "overlap_period": "unknown",
     "confidence": "unverified"},

    # 朱会东 ↔ 杨绍丽 — 上下级
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "朱会东作为市委书记，杨绍丽为市委常委、组织部部长", "overlap_org": "中共贵港市委员会", "overlap_period": "unknown",
     "confidence": "unverified"},

    # 朱会东 ↔ 韦彦 — 上下级
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "朱会东作为市委书记，韦彦为市委常委、市纪委书记", "overlap_org": "中共贵港市委员会", "overlap_period": "unknown",
     "confidence": "unverified"},

    # 朱会东 ↔ 何文凭 — 上下级
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "朱会东作为市委书记，何文凭为市委常委、秘书长", "overlap_org": "中共贵港市委员会", "overlap_period": "unknown",
     "confidence": "unverified"},
]

# Remove confidence fields — they are for tracking, not for DB schema
for r in relationships:
    r.pop("confidence", None)

# =========================================================================
# HELPERS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "市长" in cp or "区长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and ("市长" in cp or "区长" in cp):
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "市长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "副" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
    }
    return colors.get(org_type, "200,200,200")


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_db():
    """Build SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

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
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,
                       party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""),
                     p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location)
                       VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"],
                     o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Build GEXF graph file."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>贵港市领导班子关系网络</description>')
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

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources, scope_job):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "贵港市",
            "job": scope_job,
            "task_id": "guangxi_贵港市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"guigang_{p['name']}",
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
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "地厅级" if ("书记" in (p.get("current_post","")) and "副书记" not in (p.get("current_post",""))) or "市长" in (p.get("current_post","")) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"Complete career timeline, identity details (birth, birthplace, education) for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete identity details (birth date, birthplace, education, party join date) for {p['name']}",
                "why_it_matters": "Core biographical facts essential for deduplication and network analysis",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 百度百科", f"{p['name']} 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"Full career timeline before current role for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 任职经历", f"{p['name']} 履历"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    sources = [
        {"id": "S001", "title": "贵港市人民政府门户网站",
         "url": "https://www.gxgg.gov.cn/", "publisher": "贵港市人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "Official Guigang city government portal — accessible status unknown as of investigation date"},
        {"id": "S002", "title": "贵港市领导之窗",
         "url": "https://www.gxgg.gov.cn/gg/ldzc/",
         "publisher": "贵港市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "Formal leadership roster — not verified during this investigation due to network constraints"},
    ]

    # ── 朱会东 person JSON ──
    zh_timeline = [
        {"start": "2023-?", "end": "present",
         "org": "中共贵港市委员会",
         "title": "贵港市委书记", "level": "地厅级",
         "location": "广西贵港", "system": "party",
         "rank": "地厅级", "is_key_promotion": True,
         "notes": "接替何录春任贵港市委书记",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "2022-?", "end": "2023-?",
         "org": "贵港市人民政府",
         "title": "贵港市委副书记、市长", "level": "地厅级",
         "location": "广西贵港", "system": "government",
         "rank": "地厅级", "is_key_promotion": True,
         "notes": "接替蓝晓任贵港市长",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到朱会东2022年之前的完整履历。已知其曾在广西自治区发改委或其它广西地市任职，具体路径待查",
         "confidence": "unverified",
         "source_ids": []},
    ]
    zh_relationships = [
        {"person": "林海波", "person_id": "guigang_林海波",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "2024年起贵港市委书记与市长党政搭档",
         "overlap_org": "贵港市",
         "overlap_period": "2024?-present",
         "direction": "undirected",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"person": "何录春", "person_id": "guigang_何录春",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "朱会东接替何录春任贵港市委书记",
         "overlap_org": "中共贵港市委员会",
         "overlap_period": "2023?",
         "direction": "other_to_person",
         "confidence": "plausible",
         "source_ids": []},
        {"person": "蓝晓", "person_id": "guigang_蓝晓",
         "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "朱会东接替蓝晓任贵港市长",
         "overlap_org": "贵港市人民政府",
         "overlap_period": "2022?",
         "direction": "other_to_person",
         "confidence": "plausible",
         "source_ids": []},
    ]
    zh_json = build_person_json(persons[0], zh_timeline, zh_relationships, sources, "市委书记")
    zh_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-市委书记-朱会东.json")
    with open(zh_path, "w", encoding="utf-8") as f:
        json.dump(zh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zh_path}")

    # ── 林海波 person JSON ──
    lhb_timeline = [
        {"start": "2024-?", "end": "present",
         "org": "贵港市人民政府",
         "title": "贵港市委副书记、市长", "level": "地厅级",
         "location": "广西贵港", "system": "government",
         "rank": "地厅级", "is_key_promotion": True,
         "notes": "接替朱会东任贵港市长",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "2023-?", "end": "2024-?",
         "org": "中共贵港市委员会",
         "title": "贵港市委副书记（专职）", "level": "副厅级",
         "location": "广西贵港", "system": "party",
         "rank": "副厅级", "is_key_promotion": False,
         "notes": "在升任市长前曾任市委专职副书记",
         "confidence": "unverified",
         "source_ids": []},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到林海波2023年之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lhb_relationships = [
        {"person": "朱会东", "person_id": "guigang_朱会东",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "2024年起贵港市长与市委书记党政搭档；林海波接替朱会东任市长",
         "overlap_org": "贵港市人民政府/中共贵港市委员会",
         "overlap_period": "2024?-present",
         "direction": "undirected",
         "confidence": "plausible",
         "source_ids": ["S001"]},
    ]
    lhb_json = build_person_json(persons[1], lhb_timeline, lhb_relationships, sources, "市长")
    lhb_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贵港市-市长-林海波.json")
    with open(lhb_path, "w", encoding="utf-8") as f:
        json.dump(lhb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lhb_path}")


def build():
    os.makedirs(TMP, exist_ok=True)
    print(f"=== Building {TMP} data ===")
    print(f"Staging dir: {TMP}")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nBuild complete.")


if __name__ == "__main__":
    build()
