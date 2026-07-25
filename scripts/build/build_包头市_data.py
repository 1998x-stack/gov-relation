#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 包头市 (Baotou City) leadership network.

Current as of: 2026-07-25
Data sources:
  - https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/ (government leadership listing)
  - https://www.baotou.gov.cn/ (news articles confirming 陈之常 as 市委书记)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "包头市_network.db")
GEXF_PATH = os.path.join(STAGING, "包头市_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "包头市"
TODAY = "2026-07-25"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "陈之常", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市委书记", "current_org": "中共包头市委员会",
     "source": "https://www.baotou.gov.cn/"},
    {"id": 2, "name": "孟庆维", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "",
     "education": "大学学历，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市委副书记、市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394159.html"},
    {"id": 3, "name": "林立", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-03", "birthplace": "",
     "education": "研究生学历，管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市委常委、常务副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394181.html"},
    {"id": 4, "name": "胡蕊", "gender": "女", "ethnicity": "蒙古族",
     "birth": "1976-11", "birthplace": "",
     "education": "研究生学历，哲学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市委常委、副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394202.html"},
    {"id": 5, "name": "田科瑞", "gender": "男", "ethnicity": "土家族",
     "birth": "1980-10", "birthplace": "",
     "education": "研究生学历，法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市委常委、副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394213.html"},
    {"id": 6, "name": "张斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-11", "birthplace": "",
     "education": "研究生学历，经济学学士",
     "party_join": "民建会员", "work_start": "",
     "current_post": "包头市副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394231.html"},
    {"id": 7, "name": "刘国明", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-07", "birthplace": "",
     "education": "大学学历，学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市副市长、市公安局局长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394311.html"},
    {"id": 8, "name": "雷殿军", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "",
     "education": "大学学历，公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394339.html"},
    {"id": 9, "name": "宣登殿", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-07", "birthplace": "",
     "education": "研究生学历，工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394355.html"},
    {"id": 10, "name": "武凯", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "",
     "education": "研究生学历，硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394369.html"},
    {"id": 11, "name": "金永丽", "gender": "女", "ethnicity": "蒙古族",
     "birth": "1972-04", "birthplace": "",
     "education": "大学学历，工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市副市长", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202509/t20250902_394391.html"},
    {"id": 12, "name": "邬军军", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "",
     "education": "研究生学历，工商管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市人民政府党组成员、一级巡视员", "current_org": "包头市人民政府",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202512/t20251211_717996.html"},
    {"id": 13, "name": "汪占元", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "",
     "education": "大学学历，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "包头市人民政府秘书长", "current_org": "包头市人民政府办公室",
     "source": "https://www.baotou.gov.cn/zfxxgk/fdzdgknr/fd_jgjj/jgjj_ldxx/202512/t20251211_718000.html"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共包头市委员会", "type": "党委", "level": "地级市", "parent": "中共内蒙古自治区委员会", "location": "内蒙古自治区包头市"},
    {"id": 2, "name": "包头市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "内蒙古自治区包头市"},
    {"id": 3, "name": "包头市人民政府办公室", "type": "政府", "level": "正处级", "parent": "包头市人民政府", "location": "内蒙古自治区包头市"},
    {"id": 4, "name": "包头市公安局", "type": "政府", "level": "正处级", "parent": "包头市人民政府", "location": "内蒙古自治区包头市"},
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "包头市委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "包头市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民建会员"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市公安局局长"},
    {"person_id": 7, "org_id": 4, "title": "市公安局局长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "党组成员、一级巡视员", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "办公室主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长，党政主要领导工作搭档", "overlap_org": "中共包头市委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共包头市委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共包头市委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共包头市委员会", "overlap_period": "current"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "包头市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "包头市人民政府", "overlap_period": "current"},
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
