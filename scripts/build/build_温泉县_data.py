#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Wenquan County (温泉县) leadership network.

温泉县位于新疆博尔塔拉蒙古自治州，是边境县，与哈萨克斯坦接壤。
"""
import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/温泉县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/温泉县_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent Wenquan County Party Secretaries ──
    {"id": 1, "name": "郑斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委书记", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
    {"id": 2, "name": "苏卡", "gender": "男", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "新疆", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "博尔塔拉蒙古自治州领导（前任温泉县委书记）", "current_org": "博尔塔拉蒙古自治州",
     "source": "公开报道"},
    {"id": 3, "name": "白云龙", "gender": "男", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委副书记、县长", "current_org": "温泉县人民政府",
     "source": "公开报道"},
    {"id": 4, "name": "王炼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任温泉县长", "current_org": "温泉县人民政府",
     "source": "公开报道"},
    {"id": 5, "name": "陈延斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委副书记、政法委书记", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
    {"id": 6, "name": "王宇然", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、常务副县长", "current_org": "温泉县人民政府",
     "source": "公开报道"},
    {"id": 7, "name": "王彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、组织部部长", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
    {"id": 8, "name": "王玉森", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、纪委书记、监委主任", "current_org": "中共温泉县纪律检查委员会",
     "source": "公开报道"},
    {"id": 9, "name": "吕锟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、统战部部长", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
    {"id": 10, "name": "欧卡西", "gender": "女", "ethnicity": "蒙古族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、宣传部部长", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
    {"id": 11, "name": "李伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县委常委、副县长", "current_org": "温泉县人民政府",
     "source": "公开报道"},
    {"id": 12, "name": "樊宏权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县人大常委会党组书记、主任", "current_org": "温泉县人大常委会",
     "source": "公开报道"},
    {"id": 13, "name": "王忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县政协党组书记、主席", "current_org": "温泉县政协",
     "source": "公开报道"},
    {"id": 14, "name": "袁庄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温泉县党委副书记（前任）", "current_org": "中共温泉县委员会",
     "source": "公开报道"},
]

organizations = [
    # ── Wenquan County orgs ──
    {"id": 1, "name": "中共温泉县委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 2, "name": "温泉县人民政府", "type": "政府", "level": "县级",
     "parent": "博尔塔拉蒙古自治州人民政府", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 3, "name": "温泉县人大常委会", "type": "人大", "level": "县级",
     "parent": "博尔塔拉蒙古自治州人大常委会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 4, "name": "温泉县政协", "type": "政协", "level": "县级",
     "parent": "博尔塔拉蒙古自治州政协", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 5, "name": "中共温泉县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州纪律检查委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 6, "name": "中共温泉县委组织部", "type": "党委", "level": "县级",
     "parent": "中共温泉县委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 7, "name": "中共温泉县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共温泉县委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 8, "name": "中共温泉县委统战部", "type": "党委", "level": "县级",
     "parent": "中共温泉县委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},
    {"id": 9, "name": "中共温泉县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共温泉县委员会", "location": "新疆博尔塔拉蒙古自治州温泉县"},

    # ── Bortala Prefecture orgs ──
    {"id": 10, "name": "中共博尔塔拉蒙古自治州委员会", "type": "党委", "level": "地级",
     "parent": "中共新疆维吾尔自治区委员会", "location": "新疆博尔塔拉蒙古自治州博乐市"},
    {"id": 11, "name": "博尔塔拉蒙古自治州人民政府", "type": "政府", "level": "地级",
     "parent": "新疆维吾尔自治区人民政府", "location": "新疆博尔塔拉蒙古自治州博乐市"},
    {"id": 12, "name": "中共博尔塔拉蒙古自治州纪律检查委员会", "type": "党委", "level": "地级",
     "parent": "中共新疆维吾尔自治区纪律检查委员会", "location": "新疆博尔塔拉蒙古自治州博乐市"},

    # ── Neighboring counties ──
    {"id": 13, "name": "中共博乐市委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州委员会", "location": "新疆博尔塔拉蒙古自治州博乐市"},
    {"id": 14, "name": "中共精河县委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州委员会", "location": "新疆博尔塔拉蒙古自治州精河县"},
    {"id": 15, "name": "中共阿拉山口市委员会", "type": "党委", "level": "县级",
     "parent": "中共博尔塔拉蒙古自治州委员会", "location": "新疆博尔塔拉蒙古自治州阿拉山口市"},
]

# Position data: person → org with time ranges
positions = [
    # ── 郑斌 (1) — 县委书记 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "温泉县委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "现任温泉县委书记，具体任职时间待查"},

    # ── 苏卡 (2) — 前县委书记 ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "温泉县委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任温泉县委书记，后调任博州任职"},
    {"id": 3, "person_id": 2, "org_id": 10, "title": "博尔塔拉蒙古自治州领导",
     "start": "", "end": "", "rank": "副厅级",
     "note": "蒙古族干部，在博州任职"},

    # ── 白云龙 (3) — 县长 ──
    {"id": 4, "person_id": 3, "org_id": 2, "title": "温泉县委副书记、县长",
     "start": "", "end": "", "rank": "正处级",
     "note": "蒙古族，现任温泉县长"},

    # ── 王炼 (4) — 前县长 ──
    {"id": 5, "person_id": 4, "org_id": 2, "title": "温泉县长",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任温泉县长"},

    # ── 陈延斌 (5) — 副书记、政法委 ──
    {"id": 6, "person_id": 5, "org_id": 1, "title": "温泉县委副书记、政法委书记",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 王宇然 (6) — 常务副县长 ──
    {"id": 7, "person_id": 6, "org_id": 2, "title": "温泉县委常委、常务副县长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 王彬 (7) — 组织部部长 ──
    {"id": 8, "person_id": 7, "org_id": 6, "title": "温泉县委常委、组织部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 王玉森 (8) — 纪委书记 ──
    {"id": 9, "person_id": 8, "org_id": 5, "title": "温泉县委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 于锟 (9) — 统战部部长 ──
    {"id": 10, "person_id": 9, "org_id": 8, "title": "温泉县委常委、统战部部长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 欧春西 (10) — 宣传部部长 ──
    {"id": 11, "person_id": 10, "org_id": 7, "title": "温泉县委常委、宣传部部长",
     "start": "", "end": "", "rank": "副处级", "note": "蒙古族，女"},

    # ── 李伟 (11) — 副县长 ──
    {"id": 12, "person_id": 11, "org_id": 2, "title": "温泉县委常委、副县长",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 樊宏权 (12) — 人大主任 ──
    {"id": 13, "person_id": 12, "org_id": 3, "title": "温泉县人大常委会党组书记、主任",
     "start": "", "end": "", "rank": "正处级", "note": ""},

    # ── 王忠 (13) — 政协主席 ──
    {"id": 14, "person_id": 13, "org_id": 4, "title": "温泉县政协党组书记、主席",
     "start": "", "end": "", "rank": "正处级", "note": ""},

    # ── 袁庄 (14) — 前副书记 ──
    {"id": 15, "person_id": 14, "org_id": 1, "title": "温泉县委副书记",
     "start": "", "end": "", "rank": "副处级", "note": "前任副书记，具体去向待查"},
]

# Relationships: person↔person
relationships = [
    # ── Succession relationships ──
    {"id": 1, "person_a": 1, "person_b": 2, "type": "职务接替",
     "context": "郑斌接替苏卡出任温泉县委书记",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "前后任"},

    {"id": 2, "person_a": 3, "person_b": 4, "type": "职务接替",
     "context": "白云龙接替王炼出任温泉县长",
     "overlap_org": "温泉县人民政府",
     "overlap_period": "前后任"},

    # ── Current partnership ──
    {"id": 3, "person_a": 1, "person_b": 3, "type": "党政搭档",
     "context": "郑斌（县委书记）与白云龙（县长）为现任党政正职搭档",
     "overlap_org": "温泉县",
     "overlap_period": "现任"},

    # ── Leadership team ──
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级",
     "context": "陈延斌（副书记、政法委书记）为郑斌直接下属",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 5, "person_a": 1, "person_b": 6, "type": "上下级",
     "context": "王宇然（常务副县长）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 6, "person_a": 1, "person_b": 7, "type": "上下级",
     "context": "王彬（组织部部长）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 7, "person_a": 1, "person_b": 8, "type": "上下级",
     "context": "王玉森（纪委书记）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 8, "person_a": 1, "person_b": 9, "type": "上下级",
     "context": "于锟（统战部部长）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 9, "person_a": 1, "person_b": 10, "type": "上下级",
     "context": "欧春西（宣传部部长）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},
    {"id": 10, "person_a": 1, "person_b": 11, "type": "上下级",
     "context": "李伟（副县长）为县委常委之一",
     "overlap_org": "中共温泉县委员会",
     "overlap_period": "现任"},

    # ── Cross-prefecture Bortala network ──
    {"id": 11, "person_a": 2, "person_b": 3, "type": "民族干部",
     "context": "苏卡（蒙古族前县委书记）与白云龙（蒙古族县长）均为蒙古族正县级干部",
     "overlap_org": "博尔塔拉蒙古自治州",
     "overlap_period": ""},

    # ── Neighborhood (博乐、精河、阿拉山口) ──
    {"id": 12, "person_a": 1, "person_b": 2, "type": "跨县通道",
     "context": "温泉县委书记多从博州或上级机关调任，形成稳定的地州→县调任通道",
     "overlap_org": "博尔塔拉蒙古自治州→温泉县",
     "overlap_period": ""},
]

# ── BUILD SQLITE ────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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
);

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);

CREATE INDEX IF NOT EXISTS idx_positions_person ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_positions_org ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for o in organizations:
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

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
print(f"SQLite DB written: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

conn.close()


# ── BUILD GEXF ─────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    post_str = str(post)
    if "县委" in post_str and "书记" in post_str and "副" not in post_str:
        return "255,50,50"  # Red for party secretary
    elif "县长" in post_str and ("副书记" not in post_str or "拟" in post_str):
        return "50,100,255"  # Blue for county magistrate
    elif "常务副" in post_str:
        return "50,150,255"  # Light blue for executive deputy
    elif "副县长" in post_str:
        return "100,100,255"  # Lighter blue for deputy
    elif "纪委书记" in post_str or "监委" in post_str:
        return "255,165,0"  # Orange for discipline
    elif "组织部" in post_str:
        return "200,100,200"  # Purple for org dept
    elif "宣传部" in post_str:
        return "100,200,100"  # Green for propaganda
    elif "统战" in post_str:
        return "150,150,50"  # Olive for united front
    elif "副书记" in post_str:
        return "200,100,50"  # Brown for deputy secretary
    elif "人大" in post_str:
        return "200,200,100"  # Yellow/gold for people's congress
    elif "政协" in post_str:
        return "255,150,50"  # Orange for political advisory
    else:
        return "100,100,100"  # Grey

def org_color(otype):
    m = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
         "乡镇": "255,255,200", "事业单位": "220,220,220", "政协": "255,240,200",
         "人大": "200,255,255", "群团": "255,220,255"}
    return m.get(otype, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>新疆博尔塔拉蒙古自治州温泉县领导班子工作关系网络 — 基于公开信息生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "birth", "string"),
                            ("2", "birthplace", "string"), ("3", "current_post", "string"),
                            ("4", "entity_type", "string"), ("5", "level", "string"),
                            ("6", "ethnicity", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "start", "string"),
                            ("2", "end", "string"), ("3", "context", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p.get("current_post", ""))
    is_top = ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "")) or \
             ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))
    sz = "20.0" if is_top else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="4" value="person"/>')
    lines.append(f'          <attvalue for="5" value=""/>')
    lines.append(f'          <attvalue for="6" value="{esc(p.get("ethnicity",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("location",""))}"/>')
    lines.append(f'          <attvalue for="3" value=""/>')
    lines.append(f'          <attvalue for="4" value="organization"/>')
    lines.append(f'          <attvalue for="5" value="{esc(o.get("level",""))}"/>')
    lines.append(f'          <attvalue for="6" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    edge_id += 1
    lines.append(f'      <edge id="{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("start",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos.get("end",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(pos.get("note",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    edge_id += 1
    ov = r.get("overlap_period", "")
    ov_start = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ov_start)}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append(f'          <attvalue for="3" value="{esc(r.get("context",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")