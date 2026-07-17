#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for De'an County (德安县) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/dean_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/dean_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (县委书记) ──
    {"id": 1, "name": "潘光", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "江西湖口", "education": "江西省委党校研究生",
     "party_join": "1995-12", "work_start": "1996-08",
     "current_post": "中共德安县委书记", "current_org": "中共德安县委员会",
     "source": "https://www.dean.gov.cn/xwzx/dadt/202607/t20260710_7272248.html"},

    # ── Current County Mayor (县长) ──
    {"id": 2, "name": "杨帆", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-06", "birthplace": "辽宁海城", "education": "大学/管理学学士",
     "party_join": "2004-12", "work_start": "2006-06",
     "current_post": "德安县委副书记、县人民政府县长", "current_org": "德安县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%A8%E5%B8%86"},

    # ── Deputy Party Secretary (县委副书记) ──
    {"id": 3, "name": "王能耘", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委副书记", "current_org": "中共德安县委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Executive Deputy County Mayor (县委常委、常务副县长) ──
    {"id": 4, "name": "周纬华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、县政府常务副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Organization Department Head (县委常委、组织部部长、统战部部长) ──
    {"id": 5, "name": "许巨峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、组织部部长、统战部部长", "current_org": "中共德安县委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Political-Legal Committee (县委常委、政法委书记) ──
    {"id": 6, "name": "余宝宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、政法委书记", "current_org": "中共德安县委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Deputy County Mayor (县委常委、县政府副县长) ──
    {"id": 7, "name": "刘元勋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、县政府副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Propaganda Department Head (县委常委、宣传部部长) ──
    {"id": 8, "name": "许清", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、宣传部部长", "current_org": "中共德安县委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── Discipline Commission (县委常委、纪委书记、监委主任) ──
    {"id": 9, "name": "陶韬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县委常委、县纪委书记、县监委主任", "current_org": "中共德安县纪律检查委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/001/"},

    # ── County Government Deputy Mayors ──
    {"id": 10, "name": "金鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县人民政府副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/003/"},

    {"id": 11, "name": "魏霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县人民政府副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/003/"},

    {"id": 12, "name": "郑鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县人民政府副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/003/"},

    {"id": 13, "name": "林晓波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县人民政府副县长", "current_org": "德安县人民政府",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/003/"},

    # ── NPC Standing Committee (县人大常委会) ──
    {"id": 14, "name": "甘姝", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县人大常委会主任", "current_org": "德安县人民代表大会常务委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/002/"},

    # ── CPPCC (县政协) ──
    {"id": 15, "name": "郭勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德安县政协主席", "current_org": "中国人民政治协商会议德安县委员会",
     "source": "https://www.dean.gov.cn/zw/03/04/01/02/004/"},

    # ── Predecessors ──
    {"id": 16, "name": "艾菲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原德安县委书记（2024.04-2026.06）", "current_org": "",
     "source": "https://www.163.com/dy/article/J26VUTHL0514R9P4.html"},

    {"id": 17, "name": "周三连", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原德安县委书记（2016.08-2024.04）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E4%B8%89%E8%BF%9E"},

    {"id": 18, "name": "熊晋喜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原德安县委书记（~2016.08）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E6%99%8B%E5%96%9C"},
]

orgs = [
    {"id": 1, "name": "中共德安县委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江德安"},
    {"id": 2, "name": "德安县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江德安"},
    {"id": 3, "name": "中共德安县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共德安县委员会", "location": "江西九江德安"},
    {"id": 4, "name": "德安县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "九江市人大常委会", "location": "江西九江德安"},
    {"id": 5, "name": "中国人民政治协商会议德安县委员会", "type": "政协", "level": "县处级", "parent": "九江市政协", "location": "江西九江德安"},
]

positions = [
    # ── 潘光 (Party Secretary) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共德安县委书记", "start": "2026-06", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 1, "title": "（此前任永修县相关职务/九江市直机关职务）", "start": "", "end": "2026-06", "rank": "", "note": "前任职务待核实"},

    # ── 杨帆 (County Mayor) ──
    {"id": 3, "person_id": 2, "org_id": 2, "title": "德安县人民政府县长", "start": "2024-07", "end": "", "rank": "县处级正职", "note": "2024.07经县人大选举正式任职"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "德安县委副书记", "start": "2024-05", "end": "", "rank": "县处级副职", "note": "2024.05提名县长候选人同时任副书记"},
    {"id": 5, "person_id": 2, "org_id": 2, "title": "瑞昌市委副书记（正县级）", "start": "2021-08", "end": "2024-05", "rank": "县处级正职", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "共青团九江市委书记、市青联主席", "start": "", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 2, "title": "共青团九江市委副书记、市青联副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ── 王能耘 (Deputy Secretary) ──
    {"id": 8, "person_id": 3, "org_id": 1, "title": "德安县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 周纬华 (Executive Deputy Mayor) ──
    {"id": 9, "person_id": 4, "org_id": 2, "title": "德安县委常委、县政府常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 许巨峰 (Organisation + United Front) ──
    {"id": 10, "person_id": 5, "org_id": 1, "title": "德安县委常委、组织部部长、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 余宝宝 (Political-Legal) ──
    {"id": 11, "person_id": 6, "org_id": 1, "title": "德安县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 刘元勋 (Deputy Mayor, Standing Committee) ──
    {"id": 12, "person_id": 7, "org_id": 2, "title": "德安县委常委、县政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 许清 (Propaganda) ──
    {"id": 13, "person_id": 8, "org_id": 1, "title": "德安县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── 陶韬 (Discipline) ──
    {"id": 14, "person_id": 9, "org_id": 3, "title": "德安县委常委、纪委书记、县监委主任", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy Mayors ──
    {"id": 15, "person_id": 10, "org_id": 2, "title": "德安县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 16, "person_id": 11, "org_id": 2, "title": "德安县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 17, "person_id": 12, "org_id": 2, "title": "德安县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 18, "person_id": 13, "org_id": 2, "title": "德安县人民政府副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── NPC and CPPCC ──
    {"id": 19, "person_id": 14, "org_id": 4, "title": "德安县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 20, "person_id": 15, "org_id": 5, "title": "德安县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Predecessors ──
    {"id": 21, "person_id": 16, "org_id": 1, "title": "德安县委书记", "start": "2024-04", "end": "2026-06", "rank": "县处级正职", "note": ""},
    {"id": 22, "person_id": 16, "org_id": 2, "title": "德安县人民政府县长", "start": "", "end": "2024-04", "rank": "县处级正职", "note": "县长升书记，本县晋升"},
    {"id": 23, "person_id": 17, "org_id": 1, "title": "德安县委书记", "start": "2016-08", "end": "2024-04", "rank": "县处级正职", "note": ""},
    {"id": 24, "person_id": 17, "org_id": 2, "title": "德安县人民政府县长", "start": "", "end": "2016-08", "rank": "县处级正职", "note": "县长升书记"},
    {"id": 25, "person_id": 18, "org_id": 1, "title": "德安县委书记", "start": "", "end": "2016-08", "rank": "县处级正职", "note": ""},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "潘光（书记）与杨帆（县长）为现任党政一把手搭档", "overlap_org": "德安县委/县政府", "overlap_period": "2026.06至今"},
    {"id": 2, "person_a": 1, "person_b": 16, "type": "前后任关系", "context": "潘光接替艾菲任德安县委书记", "overlap_org": "中共德安县委员会", "overlap_period": "2026.06"},
    {"id": 3, "person_a": 16, "person_b": 17, "type": "前后任关系", "context": "艾菲接替周三连任德安县委书记", "overlap_org": "中共德安县委员会", "overlap_period": "2024.04"},
    {"id": 4, "person_a": 17, "person_b": 18, "type": "前后任关系", "context": "周三连接替熊晋喜任德安县委书记", "overlap_org": "中共德安县委员会", "overlap_period": "2016.08"},
    {"id": 5, "person_a": 16, "person_b": 2, "type": "前后任/上下级", "context": "艾菲曾为德安县县长，后任书记；杨帆接任县长", "overlap_org": "德安县政府", "overlap_period": ""},
    {"id": 6, "person_a": 1, "person_b": 4, "type": "上下级", "context": "潘光与周纬华（常务副县长）为党政上下级", "overlap_org": "德安县委/县政府", "overlap_period": "2026.06至今"},
    {"id": 7, "person_a": 2, "person_b": 4, "type": "上下级", "context": "杨帆（县长）与周纬华（常务副县长）为政府正副职", "overlap_org": "德安县人民政府", "overlap_period": ""},
    {"id": 8, "person_a": 1, "person_b": 3, "type": "上下级", "context": "潘光（书记）与王能耘（副书记）为党委正副书记", "overlap_org": "中共德安县委员会", "overlap_period": ""},
    {"id": 9, "person_a": 2, "person_b": 3, "type": "同级同事", "context": "杨帆（县长、副书记）与王能耘（专职副书记）为党委班子成员", "overlap_org": "中共德安县委员会", "overlap_period": ""},
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Schema
    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id))""")

    # Insert
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in orgs:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = p["current_post"]
    if "县委书记" in title:
        return "255,50,50"
    if "县长" in title or "副县长" in title or "常务副县长" in title:
        return "50,100,255"
    if "纪委书记" in title or "监委" in title:
        return "255,165,0"
    if "人大常委会主任" in title or "政协主席" in title:
        return "200,200,200"
    return "100,100,100"


def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    title = p["current_post"]
    return "县委书记" in title or "县长" in title


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>德安县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in orgs:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        note = pos["note"]
        period = f"{pos['start'] or '?'}-{pos['end'] or '今'}"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)} [{period}]"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  德安县（九江市）领导班子工作关系网络")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()

    build_db()
    build_gexf()

    # Verify
    print()
    print("📊 Summary Statistics:")
    print(f"  SQLite DB size: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF file size: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(orgs)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()
    print("✅ Done!")
