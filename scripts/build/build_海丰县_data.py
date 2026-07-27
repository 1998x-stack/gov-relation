#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海丰县, Shanwei, Guangdong."""

import sqlite3
import os
import sys
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/guangdong_海丰县")
DB_PATH = os.path.join(TMP, "海丰县_network.db")
GEXF_PATH = os.path.join(TMP, "海丰县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "郭文炯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县委书记", "current_org": "中共海丰县委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1263405.html"},
    {"id": 2, "name": "吴家宾", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县委副书记", "current_org": "中共海丰县委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1263154.html"},

    # ── County Party Standing Committee (县委常委) ──
    {"id": 3, "name": "唐源杨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县委常委、常务副县长", "current_org": "海丰县人民政府",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1263154.html"},
    {"id": 4, "name": "陈健雄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县委常委", "current_org": "中共海丰县委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1263154.html"},

    # ── County People's Congress (人大) ──
    {"id": 5, "name": "陈岳文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县人大常委会代理主任", "current_org": "海丰县人民代表大会常务委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},
    {"id": 6, "name": "张武位", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人大常委会副主任", "current_org": "海丰县人民代表大会常务委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},
    {"id": 7, "name": "唐本高", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人大常委会副主任", "current_org": "海丰县人民代表大会常务委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},
    {"id": 8, "name": "李建生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人大常委会副主任", "current_org": "海丰县人民代表大会常务委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},
    {"id": 9, "name": "黄雄飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人大常委会副主任", "current_org": "海丰县人民代表大会常务委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},

    # ── CPPCC (政协) ──
    {"id": 10, "name": "吴城池", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海丰县政协主席", "current_org": "中国人民政治协商会议海丰县委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1262226.html"},
    {"id": 11, "name": "张文亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县政协副主席", "current_org": "中国人民政治协商会议海丰县委员会",
     "source": "http://www.gdhf.gov.cn/gdhf/jjhf/zwdt/content/post_1262226.html"},

    # ── County Court & Procuratorate ──
    {"id": 12, "name": "陈永凡", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人民法院代理院长", "current_org": "海丰县人民法院",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},
    {"id": 13, "name": "谢观胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "海丰县人民检察院代理检察长", "current_org": "海丰县人民检察院",
     "source": "http://www.gdhf.gov.cn/gdhf/zwgk/0800/0801/content/post_1260327.html"},

    # ── County-level City Leaders (predecessor references) ──
    {"id": 14, "name": "逯峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "汕尾市委书记、市人大常委会主任", "current_org": "中共汕尾市委员会",
     "source": "https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1261998.html"},
    {"id": 15, "name": "林少文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "汕尾市领导", "current_org": "中共汕尾市委员会",
     "source": "https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1261998.html"},
    {"id": 16, "name": "周毅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "汕尾市领导", "current_org": "中共汕尾市委员会",
     "source": "https://www.shanwei.gov.cn/shanwei/zwgk/jcxx/zwdt/zwyw/content/post_1261998.html"},
]

organizations = [
    {"id": 1, "name": "中共海丰县委员会", "type": "党委", "level": "县处级",
     "parent": "中共汕尾市委员会", "location": "广东省汕尾市海丰县"},
    {"id": 2, "name": "海丰县人民政府", "type": "政府", "level": "县处级",
     "parent": "汕尾市人民政府", "location": "广东省汕尾市海丰县"},
    {"id": 3, "name": "海丰县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "汕尾市人大常委会", "location": "广东省汕尾市海丰县"},
    {"id": 4, "name": "中国人民政治协商会议海丰县委员会", "type": "政协", "level": "县处级",
     "parent": "汕尾市政协", "location": "广东省汕尾市海丰县"},
    {"id": 5, "name": "海丰县人民法院", "type": "政法", "level": "县处级",
     "parent": "汕尾市中级人民法院", "location": "广东省汕尾市海丰县"},
    {"id": 6, "name": "海丰县人民检察院", "type": "政法", "level": "县处级",
     "parent": "汕尾市人民检察院", "location": "广东省汕尾市海丰县"},
    {"id": 7, "name": "中共汕尾市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共广东省委员会", "location": "广东省汕尾市"},
    {"id": 8, "name": "汕尾市人民政府", "type": "政府", "level": "地厅级",
     "parent": "广东省人民政府", "location": "广东省汕尾市"},
]

positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "海丰县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "Confirmed as of 2026-07-22"},
    {"person_id": 2, "org_id": 1, "title": "海丰县委副书记",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "Confirmed as of 2026-07-21"},
    {"person_id": 3, "org_id": 1, "title": "海丰县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "海丰县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 4, "org_id": 1, "title": "海丰县委常委",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # People's Congress
    {"person_id": 5, "org_id": 3, "title": "海丰县人大常委会代理主任",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": ""},
    {"person_id": 6, "org_id": 3, "title": "海丰县人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 7, "org_id": 3, "title": "海丰县人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 8, "org_id": 3, "title": "海丰县人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 9, "org_id": 3, "title": "海丰县人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # CPPCC
    {"person_id": 10, "org_id": 4, "title": "海丰县政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": ""},
    {"person_id": 11, "org_id": 4, "title": "海丰县政协副主席",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # Court & Procuratorate
    {"person_id": 12, "org_id": 5, "title": "海丰县人民法院代理院长",
     "start_date": "2026-07", "end_date": "present", "rank": "副处级",
     "note": "Appointed by 16th NPC Standing Committee 49th session"},
    {"person_id": 13, "org_id": 6, "title": "海丰县人民检察院代理检察长",
     "start_date": "2026-07", "end_date": "present", "rank": "副处级",
     "note": "Appointed by 16th NPC Standing Committee 49th session"},

    # City-level (for context)
    {"person_id": 14, "org_id": 7, "title": "汕尾市委书记、市人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 15, "org_id": 7, "title": "汕尾市领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Participated in Haifeng inspection"},
    {"person_id": 16, "org_id": 7, "title": "汕尾市领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Participated in Haifeng inspection"},
]

relationships = [
    # Leadership structure
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记（县长/专职副书记）",
     "overlap_org": "中共海丰县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长",
     "overlap_org": "中共海丰县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委",
     "overlap_org": "中共海丰县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与人大常委会代理主任（县四套班子）",
     "overlap_org": "海丰县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委书记与政协主席（县四套班子）",
     "overlap_org": "海丰县", "overlap_period": "2026"},

    # City-county leadership
    {"person_a": 14, "person_b": 1, "type": "superior_subordinate",
     "context": "市委书记调研海丰县，县委书记陪同",
     "overlap_org": "海丰县", "overlap_period": "2026-07-15"},
]


# ── BUILD ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if "县委书记" in role or "区委书记" in role:
        return "255,50,50"
    if "副书记" in role:
        return "100,100,255"
    if "县长" in role or "区长" in role:
        return "50,100,255"
    if "纪委书记" in role:
        return "255,165,0"
    if "人大常委会" in role:
        return "200,255,255"
    if "政协" in role:
        return "255,240,200"
    if "法院" in role or "检察院" in role:
        return "200,200,255"
    if "汕尾" in role:
        return "180,180,180"
    return "100,100,100"

def is_top_leader(p):
    return p["id"] in (1, 2, 14)

# ── SQLite ────────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Drop existing tables
    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL,
        gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")

    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL,
        type TEXT DEFAULT '', level TEXT DEFAULT '',
        parent TEXT DEFAULT '', location TEXT DEFAULT '')""")

    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id))""")

    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id))""")

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        cur.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        cur.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        cur.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        cur.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")
    print(f"  Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")


# ── GEXF ─────────────────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent</creator>')
    lines.append('    <description>海丰县领导班子工作关系网络</description>')
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

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        sz = "8.0"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person -> Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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
    print(f"GEXF created: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}, Edges: {eid}")


# ── MAIN ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
