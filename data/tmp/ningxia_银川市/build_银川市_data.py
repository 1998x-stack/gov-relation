#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 银川市 (Yinchuan City) leadership network.

Current as of: 2026-07-25
Data sources:
  - https://www.yinchuan.gov.cn/xxgk/ (government leadership listing showing 陶少华 as mayor)
  - https://www.yinchuan.gov.cn/xwzx/zwyw/ (news articles confirming 赵旭辉 as 市委书记)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "银川市_network.db")
GEXF_PATH = os.path.join(STAGING, "银川市_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "银川市"
TODAY = "2026-07-25"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "赵旭辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市委书记", "current_org": "中共银川市委员会",
     "source": "https://www.yinchuan.gov.cn/xwzx/zwyw/"},
    {"id": 2, "name": "陶少华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市委副书记、市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 3, "name": "党成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市委常委、副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 4, "name": "靳玉晨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市委常委、副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 5, "name": "姜珉翰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 6, "name": "杨玉龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 7, "name": "张天喜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 8, "name": "吴静", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 9, "name": "杨燕萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 10, "name": "李昂", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市副市长", "current_org": "银川市人民政府",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
    {"id": 11, "name": "侯文莅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "银川市人民政府秘书长", "current_org": "银川市人民政府办公室",
     "source": "https://www.yinchuan.gov.cn/xxgk/"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共银川市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
    {"id": 2, "name": "银川市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
    {"id": 3, "name": "银川市人民政府办公室", "type": "政府", "level": "正处级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市"},
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "银川市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "银川市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "办公室主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长，党政主要领导工作搭档", "overlap_org": "中共银川市委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共银川市委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共银川市委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "银川市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "银川市人民政府", "overlap_period": "current"},
]

# ── SQLite ─────────────────────────────────────────────────────────
def create_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '')""")


def insert_data(conn):
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     [p.get(k, "") for k in ["id","name","gender","ethnicity","birth","birthplace",
                                             "education","party_join","work_start","current_post",
                                             "current_org","source"]])
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     [o.get(k, "") for k in ["id","name","type","level","parent","location"]])
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                     [pos.get(k, "") for k in ["person_id","org_id","title","start_date","end_date","rank","note"]])
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                     [r.get(k, "") for k in ["person_a","person_b","type","context","overlap_org","overlap_period"]])
    conn.commit()


# ── GEXF ───────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Government Personnel Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        is_top = p["id"] in (1, 2)
        sz = "20.0" if is_top else "12.0"
        if p["id"] == 1:
            color = "255,50,50"
        elif p["id"] == 2:
            color = "50,100,255"
        else:
            color = "100,100,100"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_data(conn)
    finally:
        conn.close()
    build_gexf()
    print(f"Done. DB: {DB_PATH}")
    print(f"Done. GEXF: {GEXF_PATH}")
