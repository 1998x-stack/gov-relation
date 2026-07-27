#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Shihe District (浉河区), Xinyang, Henan."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/henan_浉河区")
DB_PATH = os.path.join(TMP, "浉河区_network.db")
GEXF_PATH = os.path.join(TMP, "浉河区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "赵军华", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "信阳市浉河区委书记", "current_org": "中共信阳市浉河区委员会",
     "source": "http://www.shihe.gov.cn"},
    {"id": 2, "name": "邵永峰", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "信阳市浉河区委副书记、区长", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2021/10-08/454418.html"},

    # ── Standing Committee / Deputy Mayors ──
    {"id": 3, "name": "贡少辉", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区委常委、副区长（常务）", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2026/06-12/789719.html"},
    {"id": 4, "name": "卓亨逵", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区委常委、副区长", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2024/08-29/454434.html"},
    {"id": 5, "name": "涂瑶", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区委常委、宣传部部长、副区长", "current_org": "中共信阳市浉河区委员会",
     "source": "http://www.shihe.gov.cn/2024/02-04/454428.html"},
    {"id": 6, "name": "杨春历", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区副区长、市公安局浉河分局局长", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2021/10-08/454421.html"},
    {"id": 7, "name": "孙刚", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区副区长", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2023/03-30/454425.html"},
    {"id": 8, "name": "黄忠强", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区副区长", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2024/02-04/454431.html"},
    {"id": 9, "name": "郑焱", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区副区长人选", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2026/06-12/789750.html"},
    {"id": 10, "name": "吕本国", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "浉河区副区长人选", "current_org": "信阳市浉河区人民政府",
     "source": "http://www.shihe.gov.cn/2026/06-12/789743.html"},
]

organizations = [
    {"id": 1, "name": "中共信阳市浉河区委员会", "type": "党委", "level": "县处级", "parent": "中共信阳市委员会",
     "location": "河南省信阳市浉河区"},
    {"id": 2, "name": "信阳市浉河区人民政府", "type": "政府", "level": "县处级", "parent": "信阳市人民政府",
     "location": "河南省信阳市浉河区"},
    {"id": 3, "name": "信阳市公安局浉河分局", "type": "政府", "level": "乡科级", "parent": "信阳市公安局",
     "location": "河南省信阳市浉河区"},
]

positions = [
    # ── Zhao Junhua (赵军华) —区委书记 ──
    # Limited known career info - need more research
    {"person_id": 1, "org_id": 1, "title": "浉河区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任区委书记（据2026年新闻报道确认）"},

    # ── Shao Yongfeng (邵永峰) —区长 ──
    {"person_id": 2, "org_id": 2, "title": "浉河区委副书记、区政府区长、党组书记", "start": "2021-10", "end": "present", "rank": "正县级", "note": "2021年10月起任区长（政府领导页面发布时间）"},

    # ── Gong Shaohui (贡少辉) —常务副区长 ──
    {"person_id": 3, "org_id": 2, "title": "浉河区委常委、区政府党组副书记、副区长", "start": "", "end": "present", "rank": "副县级", "note": "三级调研员；负责常务工作"},

    # ── Zhuo Hengkui (卓亨逵) ──
    {"person_id": 4, "org_id": 2, "title": "浉河区委常委、副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责科技、邮政、电商工作"},

    # ── Tu Yao (涂瑶) ──
    {"person_id": 5, "org_id": 1, "title": "浉河区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "兼区政府副区长"},
    {"person_id": 5, "org_id": 2, "title": "浉河区副区长", "start": "", "end": "present", "rank": "副县级", "note": ""},

    # ── Yang Chunli (杨春历) ──
    {"person_id": 6, "org_id": 3, "title": "浉河区副区长、市公安局浉河分局局长", "start": "", "end": "present", "rank": "副县级", "note": "负责公安、司法、信访"},

    # ── Sun Gang (孙刚) ──
    {"person_id": 7, "org_id": 2, "title": "浉河区副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责人社、劳动就业"},

    # ── Huang Zhongqiang (黄忠强) ──
    {"person_id": 8, "org_id": 2, "title": "浉河区副区长", "start": "", "end": "present", "rank": "副县级", "note": "负责农业农村、林业、茶产业、水利"},

    # ── Zheng Yan (郑焱) ──
    {"person_id": 9, "org_id": 2, "title": "浉河区副区长人选", "start": "2026-06", "end": "present", "rank": "副县级", "note": "负责民政、卫健、医保、市场监管"},

    # ── Lyu Benguo (吕本国) ──
    {"person_id": 10, "org_id": 2, "title": "浉河区副区长人选", "start": "2026-06", "end": "present", "rank": "副县级", "note": "负责住建、城管、自然资源、环保"},
]

relationships = [
    # ── 区委书记 — 区长 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主要领导关系", "overlap_org": "中共信阳市浉河区委员会",
     "overlap_period": "2026"},

    # ── 区长 — 常务副区长 ──
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长工作关系", "overlap_org": "信阳市浉河区人民政府",
     "overlap_period": "2026"},

    # ── 区委书记 — 区委常委 ──
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委常委工作关系", "overlap_org": "中共信阳市浉河区委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委工作关系", "overlap_org": "中共信阳市浉河区委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委工作关系", "overlap_org": "中共信阳市浉河区委员会",
     "overlap_period": "2026"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "区委" in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    return "100,100,100"

def is_top_leader(post):
    return "区委书记" in post or "区长" in post

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""CREATE TABLE persons (
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
    )""")

    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")

    cur.execute("""CREATE TABLE positions (
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
    )""")

    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

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
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                     pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"],
                     r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>信阳市浉河区领导班子关系图</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="gender" type="string"/>')
    lines.append('      <attribute id="4" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="5" title="birth" type="string"/>')
    lines.append('      <attribute id="6" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = "20.0" if is_top_leader(p["current_post"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        if p["ethnicity"]:
            lines.append(f'          <attvalue for="4" value="{esc(p["ethnicity"])}"/>')
        lines.append(f'          <attvalue for="6" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        r_part, g_part, b_part = c.split(",")
        lines.append(f'        <viz:color r="{r_part}" g="{g_part}" b="{b_part}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person->Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        if pos["note"]:
            lines.append(f'          <attvalue for="2" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person<->Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Build complete.")
