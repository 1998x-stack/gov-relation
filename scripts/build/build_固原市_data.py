#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 固原市 (Guyuan City) leadership network.

Current as of: 2026-07-25
Data sources:
  - Web research (web search, Baidu Baike, government websites)
  - Degraded web access — key biographical details marked as unverified where missing

Notes:
  - 滑志敏 (Hua Zhimin) is the current Party Secretary (市委书记), appointed around 2023
  - 杨青龙 (Yang Qinglong) is the current Mayor (市长)
  - Due to web access restrictions, detailed career timelines and deputy rosters
    are incomplete and marked with appropriate confidence levels
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "固原市_network.db")
GEXF_PATH = os.path.join(STAGING, "固原市_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "固原市"
TODAY = "2026-07-25"

# ── Persons ─────────────────────────────────────────────────────────
persons = [
    # 1: Party Secretary
    {"id": 1, "name": "滑志敏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委书记", "current_org": "中共固原市委员会",
     "source": "Research — web search, Baidu Baike (need to verify)"},
    # 2: Mayor
    {"id": 2, "name": "杨青龙", "gender": "男", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委副书记、市长", "current_org": "固原市人民政府",
     "source": "Research — web search, Baidu Baike (need to verify)"},
    # 3: Executive Deputy Mayor (常务副市长)
    {"id": 3, "name": "任立新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委常委、常务副市长", "current_org": "固原市人民政府",
     "source": "Research — web search (need to verify)"},
    # 4: Deputy Party Secretary
    {"id": 4, "name": "白学贵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委副书记", "current_org": "中共固原市委员会",
     "source": "Research — web search (need to verify)"},
    # 5: Discipline Inspection Secretary
    {"id": 5, "name": "王栋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委常委、市纪委书记", "current_org": "中共固原市纪律检查委员会",
     "source": "Research — web search (need to verify)"},
    # 6: Organization Department Head
    {"id": 6, "name": "杨继宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市委常委、组织部部长", "current_org": "中共固原市委组织部",
     "source": "Research — web search (need to verify)"},
    # 7: Deputy Mayor 1
    {"id": 7, "name": "陈阳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市副市长", "current_org": "固原市人民政府",
     "source": "Research — web search (need to verify)"},
    # 8: Deputy Mayor 2
    {"id": 8, "name": "王新军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "固原市副市长", "current_org": "固原市人民政府",
     "source": "Research — web search (need to verify)"},
    # 9: Deputy Mayor 3
    {"id": 9, "name": "喜晓林", "gender": "女", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "固原市副市长", "current_org": "固原市人民政府",
     "source": "Research — web search (need to verify)"},
    # 10: Former Party Secretary (predecessor)
    {"id": 10, "name": "冼国义", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁夏回族自治区政府副主席（原固原市委书记）", "current_org": "宁夏回族自治区人民政府",
     "source": "Research — web search, Baidu Baike"},
    # 11: Former Mayor (predecessor)
    {"id": 11, "name": "马洪海", "gender": "男", "ethnicity": "回族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁夏回族自治区卫健委主任（原固原市长）", "current_org": "宁夏回族自治区卫生健康委员会",
     "source": "Research — web search (need to verify)"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共固原市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区固原市"},
    {"id": 2, "name": "固原市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区固原市"},
    {"id": 3, "name": "中共固原市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共固原市委员会", "location": "宁夏回族自治区固原市"},
    {"id": 4, "name": "中共固原市委组织部", "type": "党委", "level": "地级市", "parent": "中共固原市委员会", "location": "宁夏回族自治区固原市"},
    {"id": 5, "name": "宁夏回族自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "宁夏回族自治区银川市"},
    {"id": 6, "name": "宁夏回族自治区卫生健康委员会", "type": "政府", "level": "正厅级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "固原市委书记", "start_date": "2023", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "固原市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "市纪委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # Predecessors
    {"person_id": 10, "org_id": 1, "title": "固原市委书记（前任）", "start_date": "", "end_date": "2023", "rank": "正厅级", "note": "调任宁夏回族自治区政府副主席"},
    {"person_id": 10, "org_id": 5, "title": "宁夏回族自治区政府副主席", "start_date": "2023", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "固原市长（前任）", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "宁夏回族自治区卫健委主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    # Top leadership
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长，党政主要领导工作搭档", "overlap_org": "中共固原市委员会/固原市人民政府", "overlap_period": "current"},
    # Standing Committee relationships
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "市委常委与市委书记工作关系", "overlap_org": "中共固原市委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "市委副书记协助市委书记工作", "overlap_org": "中共固原市委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "市纪委书记与市委书记工作关系", "overlap_org": "中共固原市委员会", "overlap_period": "current"},
    {"person_a": 6, "person_b": 1, "type": "overlap", "context": "组织部部长与市委书记工作关系", "overlap_org": "中共固原市委员会", "overlap_period": "current"},
    # Mayor-deputy relationships
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "固原市人民政府", "overlap_period": "current"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "固原市人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "固原市人民政府", "overlap_period": "current"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "固原市人民政府", "overlap_period": "current"},
    # Predecessor relationships
    {"person_a": 10, "person_b": 1, "type": "succession", "context": "冼国义为前任固原市委书记，滑志敏接任", "overlap_org": "中共固原市委员会", "overlap_period": "2023"},
    {"person_a": 11, "person_b": 2, "type": "succession", "context": "前任市长与现任市长交接", "overlap_org": "固原市人民政府", "overlap_period": ""},
    # Peer relationships
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "固原市人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "市委常委班子工作关系", "overlap_org": "中共固原市委员会", "overlap_period": "current"},
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
            color = "255,50,50"  # Red - Party Secretary
        elif p["id"] == 2:
            color = "50,100,255"  # Blue - Mayor
        elif p["id"] in (10, 11):
            color = "100,100,100"  # Grey - predecessors/other
        elif p["id"] == 5:
            color = "255,165,0"  # Orange - Discipline Inspection
        else:
            color = "100,100,100"  # Grey - others
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
        # Color by type
        if o["type"] == "党委":
            org_color = "255,200,200"
        elif o["type"] == "政府":
            org_color = "200,200,255"
        else:
            org_color = "200,200,200"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{org_color.split(",")[0]}" g="{org_color.split(",")[1]}" b="{org_color.split(",")[2]}"/>')
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
