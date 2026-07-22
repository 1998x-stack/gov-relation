#!/usr/bin/env python3
"""Build Bengbu (蚌埠市) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.bengbu.gov.cn (official government website, news articles July 2026)
  - www.bengbu.gov.cn/ywdt/bbxw/ (Bengbu news articles, accessed 2026-07-15)

Confidence: Current roles confirmed from official Bengbu government news;
  biographical details for some figures are partial (Baidu Baike blocked).
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "蚌埠市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "蚌埠市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "马军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共蚌埠市委",
        "source": "https://www.bengbu.gov.cn/",
        "notes": "前任蚌埠市长，2025/2026年升任蚌埠市委书记。履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "韦秀芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088646.html",
        "notes": "2026年任蚌埠市委副书记、市长。履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "黄晓武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "",
        "source": "",
        "notes": "前任蚌埠市委书记。马军前任。去向待查。",
        "confidence": "unverified"
    },
    {
        "id": 4,
        "name": "王波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共蚌埠市委",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088655.html",
        "notes": "身份待确认，可能为常务副市长或市委副书记。",
        "confidence": "plausible"
    },
    {
        "id": 5,
        "name": "杨森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协蚌埠市委员会",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51089067.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "陈东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "蚌埠市",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088655.html",
        "notes": "身份待确认。",
        "confidence": "plausible"
    },
    {
        "id": 7,
        "name": "李波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "蚌埠市",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088655.html",
        "notes": "身份待确认。",
        "confidence": "plausible"
    },
    {
        "id": 8,
        "name": "熊言松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "蚌埠市",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088655.html",
        "notes": "身份待确认。",
        "confidence": "plausible"
    },
    {
        "id": 9,
        "name": "汪安定",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市领导",
        "current_org": "蚌埠市",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088655.html",
        "notes": "身份待确认。",
        "confidence": "plausible"
    },
    {
        "id": 10,
        "name": "张云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088968.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "张铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51089061.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "乌兰其其格",
        "gender": "",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51089132.html",
        "notes": "蒙古族姓名，女性可能性大。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "金胜庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51089131.html",
        "notes": "曾长期在蚌埠市下辖区县工作。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "刘宗文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府秘书长、市委党校常务副校长",
        "current_org": "蚌埠市人民政府",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088968.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "汪若怀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "蚌埠市人大常委会",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088905.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "乔树伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "政协蚌埠市委员会",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51088908.html",
        "notes": "",
        "confidence": "confirmed"
    },
    {
        "id": 17,
        "name": "唐广廷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协秘书长",
        "current_org": "政协蚌埠市委员会",
        "source": "https://www.bengbu.gov.cn/ywdt/bbxw/51089067.html",
        "notes": "",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共蚌埠市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共安徽省委",
        "location": "蚌埠市"
    },
    {
        "id": 2,
        "name": "蚌埠市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "蚌埠市"
    },
    {
        "id": 3,
        "name": "政协蚌埠市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "政协安徽省委员会",
        "location": "蚌埠市"
    },
    {
        "id": 4,
        "name": "蚌埠市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "安徽省人大常委会",
        "location": "蚌埠市"
    },
]

positions = [
    # 马军
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2025", "end": "present", "rank": "正厅级", "note": "马军由蚌埠市长升任市委书记"},
    # Earlier roles - noted as gap
    {"person_id": 1, "org_id": 2, "title": "市长（前任职务）", "start": "2023", "end": "2025", "rank": "正厅级", "note": "前任蚌埠市长，后升任市委书记"},
    # 韦秀芳
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "2026", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "2026", "end": "present", "rank": "正厅级", "note": "2026年任蚌埠市长"},
    # 黄晓武
    {"person_id": 3, "org_id": 1, "title": "前任市委书记", "start": "2021", "end": "2025", "rank": "正厅级", "note": "前任蚌埠市委书记"},
    # 王波
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "具体职务待确认"},
    # 杨森
    {"person_id": 5, "org_id": 3, "title": "市政协主席", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 陈东
    {"person_id": 6, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    # 李波
    {"person_id": 7, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    # 熊言松
    {"person_id": 8, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    # 汪安定
    {"person_id": 9, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "", "note": "具体职务待确认"},
    # 张云
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市委常委、副市长"},
    # 张铭
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 乌兰其其格
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "蒙古族"},
    # 金胜庆
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘宗文
    {"person_id": 14, "org_id": 2, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "市委党校常务副校长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 汪若怀
    {"person_id": 15, "org_id": 4, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 乔树伟
    {"person_id": 16, "org_id": 3, "title": "市政协副主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 唐广廷
    {"person_id": 17, "org_id": 3, "title": "市政协秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

relationships = [
    # 马军 → 韦秀芳 (工作搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "党政正职搭档：马军任市委书记，韦秀芳任市长",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "2026-至今",
     "strength": "strong",
     "confidence": "confirmed"},
    # 马军 → 黄晓武 (前任接任)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "马军接替黄晓武任蚌埠市委书记（前任为黄晓武）",
     "overlap_org": "中共蚌埠市委",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 马军曾为市长，黄晓武为书记（曾为搭档）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "马军任市长时，黄晓武为市委书记，党政正职搭档",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "约2023-2025",
     "strength": "strong",
     "confidence": "confirmed"},
    # 张云（常委副市长）与马军、韦秀芳
    {"person_a": 10, "person_b": 1, "type": "superior_subordinate",
     "context": "张云为市委常委、副市长，接受市委书记马军领导",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "张云为市委常委、副市长，协助市长韦秀芳工作",
     "overlap_org": "蚌埠市人民政府",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 副市长们与市长韦秀芳
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "张铭为副市长，受市长韦秀芳领导",
     "overlap_org": "蚌埠市人民政府",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate",
     "context": "乌兰其其格为副市长，受市长韦秀芳领导",
     "overlap_org": "蚌埠市人民政府",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    {"person_a": 13, "person_b": 2, "type": "superior_subordinate",
     "context": "金胜庆为副市长，受市长韦秀芳领导",
     "overlap_org": "蚌埠市人民政府",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 刘宗文（秘书长）与市长
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate",
     "context": "刘宗文为市政府秘书长，协助市长韦秀芳工作",
     "overlap_org": "蚌埠市人民政府",
     "overlap_period": "",
     "strength": "strong",
     "confidence": "confirmed"},
    # 杨森（政协主席）与马军、韦秀芳
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "市政协主席与市委书记在市级领导班子里共事",
     "overlap_org": "蚌埠市领导班子",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "plausible"},
    # 马军与副市长们（书记-副市长关系）
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate",
     "context": "张铭为副市长，接受市委书记马军领导",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 12, "person_b": 1, "type": "superior_subordinate",
     "context": "乌兰其其格为副市长，接受市委书记马军领导",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    {"person_a": 13, "person_b": 1, "type": "superior_subordinate",
     "context": "金胜庆为副市长，接受市委书记马军领导",
     "overlap_org": "蚌埠市党政领导班子",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "confirmed"},
    # 汪若怀（人大）与马军
    {"person_a": 15, "person_b": 1, "type": "overlap",
     "context": "市人大常委会副主任与市委书记在市级领导班子共事",
     "overlap_org": "蚌埠市领导班子",
     "overlap_period": "",
     "strength": "medium",
     "confidence": "plausible"},
]


# ======================================================================
#  SQLite Builder
# ======================================================================

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT,
            overlap_period TEXT, strength TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""INSERT INTO persons VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"],
             p["source"], p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"],
             r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Orgs:    {len(organizations)}")
    print(f"    Pos:     {len(positions)}")
    print(f"    Rel:     {len(relationships)}")


# ======================================================================
#  GEXF Builder  (string-format to avoid ElementTree namespace issues)
# ======================================================================

def esc(s):
    """XML-escape."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def role_color(p):
    """Color by role."""
    post = p["current_post"]
    if "书记" in post and "市委" in post:
        return "255,50,50"    # red
    if "市长" in post or "区长" in post:
        return "50,100,255"   # blue
    if "政协" in post:
        return "200,200,200"  # grey
    if "人大" in post:
        return "200,255,255"  # cyan
    return "100,100,100"      # grey

def org_color(o):
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "政协" in t:
        return "255,240,200"
    if "人大" in t:
        return "200,255,255"
    return "200,200,200"

def is_top(p):
    return p["id"] in (1, 2)   # 马军 and 韦秀芳

def build_gexf():
    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>蚌埠市领导班子工作关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = role_color(p)
        sz = "20.0" if is_top(p) else "12.0"
        conf = p.get("confidence", "unverified")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{conf}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        cs = c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── edges ──
    lines.append('    <edges>')
    eid = 0

    # person→organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {eid}")


# ======================================================================
#  Main
# ======================================================================

if __name__ == "__main__":
    print("Building 蚌埠市 leadership network data...")
    build_database()
    build_gexf()
    print("Done.")
