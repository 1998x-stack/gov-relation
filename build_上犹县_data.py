#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 上犹县 (Shangyou County), 赣州市, 江西省.
县域领导班子工作关系网络

Current as of: 2026-07-15

Known officeholders:
- 县委书记: 刘洪梅 (female, since 2023)
- 县长: 钟晓斌 (since 2021)
- 县委专职副书记: 何新平 (known as standing committee member)
- 常务副县长: 陈安旖 (known as standing committee member)
- 纪委书记: 胡正福 (known as standing committee member)
- 组织部长: 罗少贵 (known as standing committee member)
- 宣传部长: 冯定春 (known as standing committee member)
- 统战部长: 刘永盛 (known as standing committee member)
- 政法委书记: 黄建华 (known as standing committee member)
- 人武部部长: 刘光辉 (known as standing committee member)

Note: Standing committee composition confirmed via leadership meeting reports.
Specific career histories are partially researched — gaps marked explicitly.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, "../.."))

DB_PATH = os.path.join(BASE, "上犹县_network.db")
GEXF_PATH = os.path.join(BASE, "上犹县_network.gexf")
today = datetime.now().strftime("%Y-%m-%d")

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "刘洪梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "江西赣州",
        "native_place": "江西赣州",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "上犹县委书记",
        "current_org": "中共上犹县委员会",
        "source": "https://www.shangyou.gov.cn",
        "career_notes": "1992年8月参加工作。长期在赣州市工作，曾任赣州市妇联副主席、主席等职。2023年任上犹县委书记。详细早期履历待进一步查证。"
    },
    {
        "id": 2,
        "name": "钟晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "江西赣州",
        "native_place": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委副书记、县长",
        "current_org": "上犹县人民政府",
        "source": "https://www.shangyou.gov.cn",
        "career_notes": "曾任赣州市南康区委常委、常务副区长。2021年任上犹县委副书记、县长。"
    },
    # ---- Predecessors ----
    {
        "id": 3,
        "name": "赖晓岚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原上犹县委书记→赣州市政协副主席）",
        "current_org": "赣州市政协",
        "source": "公开报道",
        "career_notes": "前任上犹县委书记，后升任赣州市政协副主席。具体任职时间待查。"
    },
    {
        "id": 4,
        "name": "余业伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原上犹县长→后任上犹县委书记？）",
        "current_org": "",
        "source": "公开报道",
        "career_notes": "曾任上犹县长。具体任职时间和去向待查。"
    },
    # ---- Standing Committee Members ----
    {
        "id": 5,
        "name": "何新平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委专职副书记",
        "current_org": "中共上犹县委员会",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委专职副书记。具体履历待查。"
    },
    {
        "id": 6,
        "name": "陈安旖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、常务副县长",
        "current_org": "上犹县人民政府",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、常务副县长。履历待查。"
    },
    {
        "id": 7,
        "name": "胡正福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、纪委书记、监委主任",
        "current_org": "中共上犹县纪律检查委员会",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、纪委书记、监委主任。履历待查。"
    },
    {
        "id": 8,
        "name": "罗少贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、组织部长",
        "current_org": "中共上犹县委组织部",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、组织部长。履历待查。"
    },
    {
        "id": 9,
        "name": "冯定春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、宣传部长",
        "current_org": "中共上犹县委宣传部",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、宣传部长。履历待查。"
    },
    {
        "id": 10,
        "name": "刘永盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、统战部长",
        "current_org": "中共上犹县委统战部",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、统战部长。履历待查。"
    },
    {
        "id": 11,
        "name": "黄建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、政法委书记",
        "current_org": "中共上犹县委政法委员会",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、政法委书记。履历待查。"
    },
    {
        "id": 12,
        "name": "刘光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "上犹县委常委、人武部部长",
        "current_org": "上犹县人民武装部",
        "source": "上犹县政府官网/公开报道",
        "career_notes": "上犹县委常委、人武部部长。履历待查。"
    },
]

organizations = [
    {"id": 1, "name": "中共上犹县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州上犹"},
    {"id": 2, "name": "上犹县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州上犹"},
    {"id": 3, "name": "中共上犹县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市纪律检查委员会", "location": "江西赣州上犹"},
    {"id": 4, "name": "上犹县监察委员会", "type": "政府", "level": "县处级", "parent": "赣州市监察委员会", "location": "江西赣州上犹"},
    {"id": 5, "name": "中共上犹县委组织部", "type": "党委", "level": "县处级", "parent": "中共上犹县委员会", "location": "江西赣州上犹"},
    {"id": 6, "name": "中共上犹县委宣传部", "type": "党委", "level": "县处级", "parent": "中共上犹县委员会", "location": "江西赣州上犹"},
    {"id": 7, "name": "中共上犹县委统战部", "type": "党委", "level": "县处级", "parent": "中共上犹县委员会", "location": "江西赣州上犹"},
    {"id": 8, "name": "中共上犹县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共上犹县委员会", "location": "江西赣州上犹"},
    {"id": 9, "name": "上犹县人民武装部", "type": "党委", "level": "县处级", "parent": "赣州军分区", "location": "江西赣州上犹"},
    {"id": 10, "name": "赣州市政协", "type": "政协", "level": "地厅级", "parent": "政协江西省委员会", "location": "江西赣州"},
    {"id": 11, "name": "上犹县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "赣州市人民代表大会常务委员会", "location": "江西赣州上犹"},
    {"id": 12, "name": "中国人民政治协商会议上犹县委员会", "type": "政协", "level": "县处级", "parent": "政协赣州市委员会", "location": "江西赣州上犹"},
]

positions = [
    # ---- Current leaders ----
    {"id": 1, "person_id": 1, "org_id": 1, "title": "上犹县委书记", "start": "2023", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "上犹县委副书记、县长", "start": "2021", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "上犹县委副书记", "start": "2021", "end": "", "rank": "县处级副职", "note": "兼任县长"},
    # ---- Predecessors ----
    {"id": 4, "person_id": 3, "org_id": 1, "title": "上犹县委书记（前任）", "start": "", "end": "2023", "rank": "县处级正职", "note": "前任，后升任赣州市政协副主席"},
    {"id": 5, "person_id": 3, "org_id": 10, "title": "赣州市政协副主席", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "上犹县长（前任）", "start": "", "end": "", "rank": "县处级正职", "note": "前任县长，确切任期待查"},
    # ---- Standing Committee Members ----
    {"id": 7, "person_id": 5, "org_id": 1, "title": "上犹县委专职副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 8, "person_id": 6, "org_id": 2, "title": "上犹县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "兼任"},
    {"id": 10, "person_id": 7, "org_id": 3, "title": "上犹县委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 7, "org_id": 4, "title": "上犹县监察委员会主任", "start": "", "end": "", "rank": "县处级正职", "note": "兼任"},
    {"id": 12, "person_id": 8, "org_id": 5, "title": "上犹县委常委、组织部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 13, "person_id": 9, "org_id": 6, "title": "上犹县委常委、宣传部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 10, "org_id": 7, "title": "上犹县委常委、统战部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 15, "person_id": 11, "org_id": 8, "title": "上犹县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 12, "org_id": 9, "title": "上犹县委常委、人武部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    # ---- Party committee membership for all standing committee members ----
    {"id": 17, "person_id": 5, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 18, "person_id": 7, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 19, "person_id": 8, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 20, "person_id": 9, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 21, "person_id": 10, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 22, "person_id": 11, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
    {"id": 23, "person_id": 12, "org_id": 1, "title": "上犹县委常委", "start": "", "end": "", "rank": "", "note": "常委会成员"},
]

relationships = [
    # ---- 县委书记 ↔ 县长 ----
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "刘洪梅（县委书记）与钟晓斌（县长）为目前上犹县党政正职搭档",
     "overlap_org": "上犹县", "overlap_period": "2023至今",
     "confidence": "confirmed"},
    # ---- 前任 → 现任 ----
    {"id": 2, "person_a_id": 3, "person_b_id": 1, "type": "前任继任",
     "context": "赖晓岚为上犹县委书记前任，刘洪梅为现任",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 前任县长 → 现任县长 ----
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "前任继任",
     "context": "余业伟为上犹县长前任，钟晓斌为现任",
     "overlap_org": "上犹县人民政府", "overlap_period": "",
     "confidence": "plausible"},
    # ---- 书记 ↔ 专职副书记 ----
    {"id": 4, "person_a_id": 1, "person_b_id": 5, "type": "上下级",
     "context": "刘洪梅（书记）与何新平（专职副书记）为县委正副职",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 书记 ↔ 纪委书记 ----
    {"id": 5, "person_a_id": 1, "person_b_id": 7, "type": "上下级",
     "context": "刘洪梅（书记）与胡正福（纪委书记）在同一届县委班子共事",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 书记 ↔ 组织部长 ----
    {"id": 6, "person_a_id": 1, "person_b_id": 8, "type": "上下级",
     "context": "刘洪梅（书记）与罗少贵（组织部长）在同一届县委班子共事",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 书记 ↔ 宣传部长 ----
    {"id": 7, "person_a_id": 1, "person_b_id": 9, "type": "上下级",
     "context": "刘洪梅（书记）与冯定春（宣传部长）在同一届县委班子共事",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 书记 ↔ 统战部长 ----
    {"id": 8, "person_a_id": 1, "person_b_id": 10, "type": "上下级",
     "context": "刘洪梅（书记）与刘永盛（统战部长）在同一届县委班子共事",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 书记 ↔ 政法委书记 ----
    {"id": 9, "person_a_id": 1, "person_b_id": 11, "type": "上下级",
     "context": "刘洪梅（书记）与黄建华（政法委书记）在同一届县委班子共事",
     "overlap_org": "中共上犹县委员会", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 县长 ↔ 常务副县长 ----
    {"id": 10, "person_a_id": 2, "person_b_id": 6, "type": "上下级",
     "context": "钟晓斌（县长）与陈安旖（常务副县长）为政府正副职搭档",
     "overlap_org": "上犹县人民政府", "overlap_period": "",
     "confidence": "confirmed"},
    # ---- 常务副县长 ↔ 书记 ----
    {"id": 11, "person_a_id": 1, "person_b_id": 6, "type": "上下级",
     "context": "刘洪梅（书记）与陈安旖（常务副县长）在同一届班子共事",
     "overlap_org": "上犹县", "overlap_period": "",
     "confidence": "confirmed"},
]

# =========================================================================
# BUILD SQLite Database
# =========================================================================

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"])
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"])
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (id, person_a_id, person_b_id, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?,?)",
            (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  ✓ SQLite: {DB_PATH}")


# =========================================================================
# BUILD GEXF Graph
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    title = p["current_post"]
    if "书记" in title and "县委" in title and "纪委" not in title:
        return "255,50,50"
    elif "县长" in title or "副县长" in title or "区长" in title:
        return "50,100,255"
    elif "纪委" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def is_top_leader(p):
    ids_with_roles = {1, 2, 3, 4}  # 书记+县长+主要前任
    return p["id"] in ids_with_roles

def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>上犹县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person → Organization edges (worked_at)
    for pos in positions:
        eid += 1
        pid = pos["person_id"]
        oid = pos["org_id"]
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================

def main():
    print("上犹县领导班子工作关系网络数据生成")
    print(f"生成日期: {today}")
    print(f"人员: {len(persons)} 人")
    print(f"机构: {len(organizations)} 个")
    print(f"任职: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")
    print()

    print("构建 SQLite 数据库...")
    build_db()

    print("构建 GEXF 图文件...")
    build_gexf()

    print()
    print("数据生成完成!")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Summary stats
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"  {table}: {cur.fetchone()[0]} 行")
    conn.close()


if __name__ == "__main__":
    main()
