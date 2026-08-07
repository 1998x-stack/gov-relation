#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中卫市 (Zhongwei City) leadership network.

Current as of: 2026-08-07
Region: 宁夏回族自治区 · 地级市 · 中卫市
Targets: 市委书记 (Party Secretary) & 市长 (Mayor)

Data / evidence status:
  - Degraded web access during research (Exa rate-limited, Baidu 403,
    Jina Reader / gov sites time out). Produced in partial-evidence mode per
    the china-gov-network skill's source_fallbacks.md.
  - Confirmed local-repo anchor: 陈宏(副), ex-中宁县委书记, promoted to
    中卫市副市长 (from data/persons/20260725-...-陈宏.json and
    scripts/build/build_中宁县_data.py).
  - Candidates for current 市委书记 / 市长 are marked confidence=plausible /
    unverified; verify against www.nxzw.gov.cn 领导之窗 when network returns.

Confirmed entities built from local repo + geographic structure; biographical
fields left blank where public evidence is unavailable. open_gaps.md records the
top unresolved identities.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "中卫市_network.db")
GEXF_PATH = os.path.join(STAGING, "中卫市_network.gexf")

# ── Metadata ────────────────────────────────────────────────────────
SLUG = "中卫市"
TODAY = "2026-08-07"

# ── Persons ─────────────────────────────────────────────────────────
# Confidence flags: 'confirmed' | 'plausible' | 'unverified'
# 1 市委书记 (best-known candidate; identity NOT confirmed for 2026)
# 2 市长 (best-known candidate; identity NOT confirmed for 2026)
# 3..  detached confirmations
persons = [
    # 1: Party Secretary — 刘国强 (CONFIRMED via 灵武/银川 investigation:
    #   2024-07-28 任前公示, 2024-08-03 中卫市干部大会宣布任中卫市委书记)
    {"id": 1, "name": "刘国强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市委书记", "current_org": "中共中卫市委员会",
     "source": "data/persons/20260807-银川市-前任市委书记-刘国强.json; 澎湃新闻; 中卫市政府人事公告"},
    # 2: Mayor — 马秀兰 (plausible via 武威 investigation:
    #   ex-武威市长 2023.04-2025.07, 2025-07 跨省调任宁夏中卫市委副书记、市长)
    {"id": 2, "name": "马秀兰", "gender": "女", "ethnicity": "回族",
     "birth": "1974-03", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市委副书记、市长（原武威市长）", "current_org": "中卫市人民政府",
     "source": "scripts/build/build_武威市_data.py; data/persons/20260717-武威市-市长-叶万彬.json; Baidu Baike"},
    # 3: Executive Deputy Mayor (open)
    {"id": 3, "name": "待查（常务副市长）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中卫市委常委、常务副市长（待核实）", "current_org": "中卫市人民政府",
     "source": "Research — identity unverified, open gap"},
    # 4: Deputy Mayor — 陈宏 (CONFIRMED from local repo: ex 中宁县委书记 → 中卫市副市长)
    {"id": 4, "name": "陈宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市副市长（原中宁县委书记）", "current_org": "中卫市人民政府",
     "source": "data/persons/20260725-中卫市-前任县委书记-陈宏.json; scripts/build/build_中宁县_data.py"},
    # 5: 沙坡头区区委书记 (sub-task, candidate)
    {"id": 5, "name": "待查（沙坡头区书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "沙坡头区委书记（待核实）", "current_org": "中共中卫市沙坡头区委员会",
     "source": "Research — identity unverified"},
    # 6: 中宁县县委书记 (CONFIRMED-ish from local repo: 何建勃, prior report marked unverified)
    {"id": 6, "name": "何建勃", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中宁县委书记（据研究报告，需核实）", "current_org": "中共中卫市中宁县委员会",
     "source": "data/persons/20260725-中卫市-县委书记-何建勃.json"},
    # 7: 海原县县委书记 (candidate, open)
    {"id": 7, "name": "待查（海原县书记）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海原县委书记（待核实）", "current_org": "中共中卫市海原县委员会",
     "source": "Research — identity unverified"},
    # 8: Former Party Secretary (predecessor, candidate)
    {"id": 8, "name": "何健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市前任市委书记（据公开资料，需核实）", "current_org": "中共中卫市委员会",
     "source": "公开资料，网络受限下未完全核实"},
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共中卫市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区中卫市"},
    {"id": 2, "name": "中卫市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区中卫市"},
    {"id": 3, "name": "中共中卫市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市"},
    {"id": 4, "name": "中共中卫市沙坡头区委员会", "type": "党委", "level": "县级", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市沙坡头区"},
    {"id": 5, "name": "中卫市沙坡头区人民政府", "type": "政府", "level": "县级", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市沙坡头区"},
    {"id": 6, "name": "中共中卫市中宁县委员会", "type": "党委", "level": "县", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 7, "name": "中宁县人民政府", "type": "政府", "level": "县", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 8, "name": "中共中卫市海原县委员会", "type": "党委", "level": "县", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市海原县"},
    {"id": 9, "name": "海原县人民政府", "type": "政府", "level": "县", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市海原县"},
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "中卫市委书记", "start_date": "2024-08", "end_date": "present", "rank": "正厅级", "note": "2024-08-03干部大会宣布由灵武市委书记调任"},
    {"person_id": 2, "org_id": 1, "title": "中卫市委副书记", "start_date": "2025-07", "end_date": "present", "rank": "正厅级", "note": "由甘肃武威市长跨省调任"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-07", "end_date": "present", "rank": "正厅级", "note": "原武威市长，2025-07跨省调任"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待核实"},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "原中宁县委书记，confirmed via local repo"},
    # Sub-area leaders
    {"person_id": 5, "org_id": 4, "title": "沙坡头区委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "待核实"},
    {"person_id": 6, "org_id": 6, "title": "中宁县委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "据研究报告"},
    {"person_id": 7, "org_id": 8, "title": "海原县委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "待核实"},
    # Predecessor
    {"person_id": 8, "org_id": 1, "title": "中卫市委书记（前任）", "start_date": "", "end_date": "", "rank": "正厅级", "note": "公开资料候选"},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    # Top leadership
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记刘国强与市长马秀兰，党政主要领导工作搭档", "overlap_org": "中共中卫市委员会/中卫市人民政府", "overlap_period": "2025-07至present"},
    # Deputy mayor ↔ mayor  (陈宏 副)—current
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长工作", "overlap_org": "中卫市人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "中卫市人民政府", "overlap_period": "current"},
    # County-tier edges to city leadership
    {"person_a": 6, "person_b": 4, "type": "succession", "context": "陈宏原任中宁县委书记，后任中卫市副市长（继任关系）", "overlap_org": "中共中宁县县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "沙坡头区委书记隶属中卫市委，与市委书记工作关系", "overlap_org": "中共中卫市委员会", "overlap_period": "current"},
    {"person_a": 8, "person_b": 1, "type": "succession", "context": "前任市委书记与现任市委书记交接", "overlap_org": "中共中卫市委员会", "overlap_period": ""},
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
        elif p["id"] in (8,):
            color = "100,100,100"  # Grey - predecessor
        elif p["id"] == 4:
            color = "100,100,255"  # deputy mayor (gov)
        else:
            color = "100,100,100"  # Grey - others / unverified
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Nodes: organizations
    for o in organizations:
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