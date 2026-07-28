#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 芒康县 (Mangkang County) leadership network.

Task ID: xizang_芒康县
Province: 西藏自治区
Parent city: 昌都市
Data source: 芒康县人民政府 official website (http://mangkang.changdu.gov.cn)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/xizang_芒康县/芒康县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/xizang_芒康县/芒康县_network.gexf")

persons = [
    # ── Core leaders ──
    {"id": 1, "name": "汪正涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委书记", "current_org": "中共芒康县委员会",
     "source": "http://mangkang.changdu.gov.cn/mkx/c105702/202605/22ab1254994349cb83ac38838f8cb7b7.shtml"},
    {"id": 2, "name": "巴桑扎西", "gender": "男", "ethnicity": "藏族",
     "birth": "1979-03", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委副书记、县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202210/c1c4479703b14591ae222c790f6ff87a.shtml"},
    # ── Deputy leaders ──
    {"id": 3, "name": "泽巴拉加", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委副书记、党校校长", "current_org": "中共芒康县委员会",
     "source": "http://mangkang.changdu.gov.cn/mkx/c105702/202604/22101f550da74da09cb59b745975d13a.shtml"},
    {"id": 4, "name": "张楠", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-01", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委常务副书记、政府常务副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202601/07616503a3c14e42ae18b2f48250abb2.shtml"},
    {"id": 5, "name": "王攀", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-06", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委常务副书记、政府常务副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202601/7b927c886b0f432c87052add0122c061.shtml"},
    {"id": 6, "name": "姚城", "gender": "男", "ethnicity": "侗族",
     "birth": "1979-09", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委常委、政府常务副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202511/ef79132bf5a04439b54fdb3bf513fd14.shtml"},
    {"id": 7, "name": "蒲中伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-04", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委常委、政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202210/75560ea04c16451d84ab9856de915902.shtml"},
    {"id": 8, "name": "泽军宝", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县委常委、纪委书记、监委主任", "current_org": "中共芒康县纪律检查委员会",
     "source": "http://mangkang.changdu.gov.cn/mkx/c105702/202605/22ab125499434b83ac93638f8cb7b7.shtml"},
    {"id": 9, "name": "黄春林", "gender": "男", "ethnicity": "苗族",
     "birth": "1976-01", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202401/e08da251dc6e4fc095613ee543db1696.shtml"},
    {"id": 10, "name": "贺箭飞", "gender": "男", "ethnicity": "土家族",
     "birth": "1986-03", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202401/1a80cda0cf81435b99d83a390566cbeb.shtml"},
    {"id": 11, "name": "贡嘎罗布", "gender": "男", "ethnicity": "藏族",
     "birth": "1990-03", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202501/66b302a1521b452983fccae0c74746a8.shtml"},
    {"id": 12, "name": "张海军", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-07", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202403/a2228a6db08b4abc862db623a430b9b7.shtml"},
    {"id": 13, "name": "扎巴江村", "gender": "男", "ethnicity": "藏族",
     "birth": "1983-09", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202404/a4cbfedf2d8048b8996905e4f1c432e7.shtml"},
    {"id": 14, "name": "王福东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202501/01f9afb64b5b48bfb912df6dfb9e64aa.shtml"},
    {"id": 15, "name": "董小平", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-08", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政府副县长候选人", "current_org": "芒康县人民政府",
     "source": "http://mangkang.changdu.gov.cn/mkx/c101893/202602/ad12b1f58588443bac91897427cb2ff2.shtml"},
    {"id": 16, "name": "四郎旺修", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县人大常委会党组书记", "current_org": "芒康县人大常委会",
     "source": "http://mangkang.changdu.gov.cn/mkx/c105702/202603/fd8e9e778a17442fa2417ae2da6143ba.shtml"},
    {"id": 17, "name": "泽旺", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芒康县政协主席", "current_org": "政协芒康县委员会",
     "source": "http://mangkang.changdu.gov.cn/mkx/c105702/202603/fd8e9e778a17442fa2417ae2da6143ba.shtml"},
    # ── Org nodes ──
    {"id": 100, "name": "中共芒康县委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县级党委", "current_org": "",
     "source": ""},
    {"id": 101, "name": "芒康县人民政府", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县级政府", "current_org": "",
     "source": ""},
    {"id": 102, "name": "中共芒康县纪律检查委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县纪委", "current_org": "",
     "source": ""},
    {"id": 103, "name": "芒康县人大常委会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县人大", "current_org": "",
     "source": ""},
    {"id": 104, "name": "政协芒康县委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县政协", "current_org": "",
     "source": ""},
    {"id": 105, "name": "芒康县人大常委会（党组书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县人大", "current_org": "",
     "source": ""},
]

# Organizations table entries (separate from persons)
organizations = [
    {"id": 1, "name": "中共芒康县委员会", "type": "党委", "level": "县级",
     "parent": "中共昌都市委员会", "location": "西藏自治区昌都市芒康县"},
    {"id": 2, "name": "芒康县人民政府", "type": "政府", "level": "县级",
     "parent": "昌都市人民政府", "location": "西藏自治区昌都市芒康县"},
    {"id": 3, "name": "中共芒康县纪律检查委员会", "type": "纪律检查", "level": "县级",
     "parent": "中共昌都市纪律检查委员会", "location": "西藏自治区昌都市芒康县"},
    {"id": 4, "name": "芒康县人大常委会", "type": "人大", "level": "县级",
     "parent": "昌都市人大常委会", "location": "西藏自治区昌都市芒康县"},
    {"id": 5, "name": "政协芒康县委员会", "type": "政协", "level": "县级",
     "parent": "政协昌都市委员会", "location": "西藏自治区昌都市芒康县"},
    {"id": 6, "name": "中共昌都市委员会", "type": "党委", "level": "地级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区昌都市"},
    {"id": 7, "name": "昌都市人民政府", "type": "政府", "level": "地级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区昌都市"},
]

positions = [
    # Core leaders
    {"id": 1, "person_id": 1, "org_id": 1, "title": "芒康县委书记",
     "start": "", "end": "", "rank": "正县级",
     "note": "2026年5月以县委书记身份主持'5·10我要廉'廉洁文化宣传月活动"},
    {"id": 2, "person_id": 2, "org_id": 1, "title": "芒康县委副书记",
     "start": "", "end": "", "rank": "正县级",
     "note": ""},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "芒康县县长",
     "start": "", "end": "", "rank": "正县级",
     "note": "主持县人民政府全面工作"},
    # Deputy leaders
    {"id": 4, "person_id": 3, "org_id": 1, "title": "芒康县委副书记、党校校长",
     "start": "", "end": "", "rank": "副县级",
     "note": "2026年4月以县委副书记身份主持虫草采集动员部署会"},
    {"id": 5, "person_id": 4, "org_id": 1, "title": "芒康县委常务副书记",
     "start": "", "end": "", "rank": "副县级",
     "note": "重庆市对口援藏干部"},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "芒康县政府常务副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责文旅工作"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "芒康县委常务副书记",
     "start": "", "end": "", "rank": "副县级",
     "note": "中国电建集团对口援藏干部"},
    {"id": 8, "person_id": 5, "org_id": 2, "title": "芒康县政府常务副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责清洁能源建设"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "芒康县委常委",
     "start": "", "end": "", "rank": "副县级",
     "note": ""},
    {"id": 10, "person_id": 6, "org_id": 2, "title": "芒康县政府常务副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责发改、财政、应急管理"},
    {"id": 11, "person_id": 7, "org_id": 1, "title": "芒康县委常委",
     "start": "", "end": "", "rank": "副县级",
     "note": ""},
    {"id": 12, "person_id": 7, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责产业园区、招商引资"},
    {"id": 13, "person_id": 8, "org_id": 1, "title": "芒康县委常委",
     "start": "", "end": "", "rank": "副县级",
     "note": ""},
    {"id": 14, "person_id": 8, "org_id": 3, "title": "芒康县纪委书记、监委主任",
     "start": "", "end": "", "rank": "副县级",
     "note": "2026年5月作警示教育专题辅导"},
    {"id": 15, "person_id": 9, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责教育"},
    {"id": 16, "person_id": 10, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责农业农村、市场监管"},
    {"id": 17, "person_id": 11, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责民政、自然资源、林草"},
    {"id": 18, "person_id": 12, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责社保、住建"},
    {"id": 19, "person_id": 13, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责公安、司法"},
    {"id": 20, "person_id": 14, "org_id": 2, "title": "芒康县政府副县长",
     "start": "", "end": "", "rank": "副县级",
     "note": "负责城市管理"},
    {"id": 21, "person_id": 15, "org_id": 2, "title": "芒康县政府副县长候选人",
     "start": "", "end": "", "rank": "副县级",
     "note": "2026年2月任副县长候选人"},
    {"id": 22, "person_id": 16, "org_id": 4, "title": "芒康县人大常委会党组书记",
     "start": "", "end": "", "rank": "正县级",
     "note": "2026年3月主持县第十三届人大第七次会议"},
    {"id": 23, "person_id": 17, "org_id": 5, "title": "芒康县政协主席",
     "start": "", "end": "", "rank": "正县级",
     "note": "2026年3月在县人代会主席台前排就座"},
]

relationships = [
    # 汪正涛 — 巴桑扎西 (正副书记搭档)
    {"id": 1, "source": 1, "target": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政正职搭档", "overlap_org": "中共芒康县委员会",
     "overlap_period": "2026-present"},
    # 汪正
    {"id": 2, "source": 1, "target": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记",
     "overlap_org": "中共芒康县委员会",
     "overlap_period": "2026-present"},
    # 巴桑扎西 — 泽巴拉加 (government team co-lead)
    {"id": 3, "source": 2, "target": 3, "type": "colleague",
     "context": "县政府县长与县委副书记（党务）",
     "overlap_org": "中共芒康县委员会",
     "overlap_period": "2026-present"},
    # 巴桑扎西 — 张楠
    {"id": 4, "source": 2, "target": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长（协助常务工作）",
     "overlap_org": "芒康县人民政府",
     "overlap_period": "2026-present"},
    # 巴桑扎西
    {"id": 5, "source": 2, "target": 5, "type": "superior_subordinate",
     "context": "县长与常务副县长（协助常务工作）",
     "overlap_org": "芒康县人民政府",
     "overlap_period": "2026-present"},
    # 巴桑扎西
    {"id": 6, "source": 2, "target": 6, "type": "superior_subordinate",
     "context": "县长与常务副县长（协助常务工作）",
     "overlap_org": "芒康县人民政府",
     "overlap_period": "2026-present"},
    # 汪正
    {"id": 7, "source": 1, "target": 8, "type": "superior_subordinate",
     "context": "县委书记与纪委书记",
     "overlap_org": "中共芒康县委员会",
     "overlap_period": "2026-present"},
]

confidences = {
    "identity": "confirmed",
    "current_role": "confirmed",
    "career_completeness": "partial",
    "relationship_confidence": "high",
    "biggest_gap": "汪正涛的籍贯、出生年份、学历、履历完全未知；巴桑扎西的完整履历、籍贯未知；各常务副县长曾任职务未知"
}


# ── BUILD ──
def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        if p["id"] >= 100:
            continue  # skip org-as-person entries
        cur.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT OR REPLACE INTO relationships
            (id, person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?,?)""",
            (r["id"], r["source"], r["target"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Counts
    pc = cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    oc = cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    poc = cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    rc = cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    # ── GEXF ──
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        role = p["current_post"]
        if "书记" in role and "县委" in role:
            return "255,50,50"
        if "县长" in role:
            return "50,100,255"
        if "纪委" in role:
            return "255,165,0"
        if "人大" in role or "政协" in role:
            return "200,255,255"
        return "100,100,100"

    def is_top_leader(p):
        return p["id"] in (1, 2)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>芒康县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        ntype = "person"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{ntype}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_color = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪律检查": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in organizations:
        c = org_color.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        source = f"p{pos['person_id']}"
        target = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{source}" target="{target}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["source"]}" target="p{r["target"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Database written: {DB_PATH}")
    print(f"✅ GEXF written: {GEXF_PATH}")
    print(f"   Persons: {pc}, Organizations: {oc}, Positions: {poc}, Relationships: {rc}")


if __name__ == "__main__":
    build()