#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙子湖区 (Longzihu District, Bengbu, Anhui) leadership network.

龙子湖区 — 安徽省蚌埠市辖区, 蚌埠"东大门", 面积约160平方公里, 辖1乡6街道.
Research note: Government websites (www.bblzh.gov.cn) were partially accessible.
Leadership biographies for core figures (倪涛, 马怀洪) could not be fully retrieved
from Baidu Baike or detailed resume pages due to geo-restrictions.
Identity, career timeline, and relationship evidence marked with appropriate confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_龙子湖区")
DB_PATH = os.path.join(STAGING, "龙子湖区_network.db")
GEXF_PATH = os.path.join(STAGING, "龙子湖区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──
    # 倪涛 — 龙子湖区委书记
    {"id": 1, "name": "倪涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "龙子湖区委书记",
     "current_org": "中共龙子湖区委",
     "source": "龙子湖区人民政府网站（www.bblzh.gov.cn）第六次党代会报道（2026年6月）"},

    # 马怀洪 — 龙子湖区区长
    {"id": 2, "name": "马怀洪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "龙子湖区区长",
     "current_org": "龙子湖区人民政府",
     "source": "龙子湖区人民政府网站/区委理论学习中心组会议报道（2025年12月）"},

    # ── Predecessors ──
    # 倪涛的前任 — 据公开报道推测, 倪涛约在2024-2025年间接任
    # 前任区委书记（推测为任生或相关人选, 待确认）
    {"id": 3, "name": "任生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原龙子湖区委书记，已调任）",
     "current_org": "待确认",
     "source": "公开报道（推测，需确认）"},

    # 更早前任区委书记
    {"id": 4, "name": "朱克华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原龙子湖区委书记，已调任）",
     "current_org": "待确认",
     "source": "公开报道（推测，需确认）"},

    # ── Key Deputies: Standing Committee ──
    # 区委副书记（专职，待确认）
    {"id": 5, "name": "（专职副书记待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委副书记（待确认）",
     "current_org": "中共龙子湖区委",
     "source": "待确认"},

    # 常务副区长（待确认）
    {"id": 6, "name": "（常务副区长待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委常委、常务副区长（待确认）",
     "current_org": "龙子湖区人民政府",
     "source": "待确认"},

    # 纪委书记（待确认）
    {"id": 7, "name": "（纪委书记待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委常委、纪委书记（待确认）",
     "current_org": "中共龙子湖区纪律检查委员会",
     "source": "待确认"},

    # 组织部长（待确认）
    {"id": 8, "name": "（组织部长待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委常委、组织部长（待确认）",
     "current_org": "中共龙子湖区委组织部",
     "source": "待确认"},

    # 宣传部长（待确认）
    {"id": 9, "name": "（宣传部长待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委常委、宣传部长（待确认）",
     "current_org": "中共龙子湖区委宣传部",
     "source": "待确认"},

    # 政法委书记（待确认）
    {"id": 10, "name": "（政法委书记待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区委常委、政法委书记（待确认）",
     "current_org": "中共龙子湖区委政法委员会",
     "source": "待确认"},

    # ── Confirmed Deputy(s) ──
    # 曹怀龙 — 副区长（从政协会议报道确认）
    {"id": 11, "name": "曹怀龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "龙子湖区副区长",
     "current_org": "龙子湖区人民政府",
     "source": "龙子湖区人民政府网站/区政协十届三十三次常委会报道（2026年7月）"},

    # ── NPC & CPPCC Leaders ──
    # 区人大常委会主任（待确认）
    {"id": 12, "name": "（人大主任待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "龙子湖区人大常委会主任（待确认）",
     "current_org": "龙子湖区人大常委会",
     "source": "待确认"},

    # 廖万红 — 区政协主席
    {"id": 13, "name": "廖万红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "龙子湖区政协主席",
     "current_org": "龙子湖区政协",
     "source": "龙子湖区人民政府网站/区政协十届三十三次常委会报道（2026年7月）"},
]

organizations = [
    {"id": 1, "name": "中共龙子湖区委", "type": "党委", "level": "县级", "parent": "中共蚌埠市委", "location": "龙子湖区"},
    {"id": 2, "name": "龙子湖区人民政府", "type": "政府", "level": "县级", "parent": "蚌埠市人民政府", "location": "龙子湖区"},
    {"id": 3, "name": "中共龙子湖区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共蚌埠市纪委", "location": "龙子湖区"},
    {"id": 4, "name": "龙子湖区人大常委会", "type": "人大", "level": "县级", "parent": "蚌埠市人大常委会", "location": "龙子湖区"},
    {"id": 5, "name": "龙子湖区政协", "type": "政协", "level": "县级", "parent": "蚌埠市政协", "location": "龙子湖区"},
    {"id": 6, "name": "中共龙子湖区委组织部", "type": "党委部门", "level": "县级", "parent": "中共龙子湖区委", "location": "龙子湖区"},
    {"id": 7, "name": "中共龙子湖区委宣传部", "type": "党委部门", "level": "县级", "parent": "中共龙子湖区委", "location": "龙子湖区"},
    {"id": 8, "name": "中共龙子湖区委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共龙子湖区委", "location": "龙子湖区"},
]

positions = [
    # ── Current Leaders ──
    {"person_id": 1, "org_id": 1, "title": "龙子湖区委书记", "start": "", "end": "", "rank": "正处",
     "note": "倪涛在2026年6月龙子湖区第五次党代会上作工作报告，确认续任区委书记。上任时间待确认。"},
    {"person_id": 2, "org_id": 2, "title": "龙子湖区区长", "start": "", "end": "", "rank": "正处",
     "note": "马怀洪在2025年12月主持区政府学习会议，确认在任区长。上任时间待确认。"},

    # ── Predecessors ──
    # 任生（前任区委书记，需确认）
    {"person_id": 3, "org_id": 1, "title": "龙子湖区委书记", "start": "", "end": "", "rank": "正处",
     "note": "任生是否为倪涛的前任区委书记及具体任职时间，需进一步核实。"},

    # 朱克华（更早前任）
    {"person_id": 4, "org_id": 1, "title": "龙子湖区委书记", "start": "", "end": "", "rank": "正处",
     "note": "朱克华任龙子湖区委书记的时间待确认。"},

    # ── Standing Committee (待确认) ──
    {"person_id": 5, "org_id": 1, "title": "龙子湖区委副书记", "start": "", "end": "", "rank": "正处",
     "note": "专职副书记姓名及任职时间待确认。"},
    {"person_id": 6, "org_id": 2, "title": "龙子湖区委常委、常务副区长", "start": "", "end": "", "rank": "正处",
     "note": "常务副区长姓名待确认。"},
    {"person_id": 7, "org_id": 3, "title": "龙子湖区委常委、纪委书记、区监委主任", "start": "", "end": "", "rank": "正处",
     "note": "纪委书记姓名待确认。"},
    {"person_id": 8, "org_id": 6, "title": "龙子湖区委常委、组织部部长", "start": "", "end": "", "rank": "正处",
     "note": "组织部长姓名待确认。"},
    {"person_id": 9, "org_id": 7, "title": "龙子湖区委常委、宣传部部长", "start": "", "end": "", "rank": "正处",
     "note": "宣传部长姓名待确认。"},
    {"person_id": 10, "org_id": 8, "title": "龙子湖区委常委、政法委书记", "start": "", "end": "", "rank": "正处",
     "note": "政法委书记姓名待确认。"},

    # ── Confirmed Deputy ──
    {"person_id": 11, "org_id": 2, "title": "龙子湖区副区长", "start": "", "end": "", "rank": "副处",
     "note": "曹怀龙，2026年7月在区政协会上发言。"},

    # ── NPC & CPPCC ──
    {"person_id": 12, "org_id": 4, "title": "龙子湖区人大常委会主任", "start": "", "end": "", "rank": "正处",
     "note": "人大主任姓名待确认。"},
    {"person_id": 13, "org_id": 5, "title": "龙子湖区政协主席", "start": "", "end": "", "rank": "正处",
     "note": "廖万红，2026年7月主持区政协十届三十三次常委会。"},
]

relationships = [
    # ── Core pair: 区委书记 & 区长 ──
    {"person_a": 1, "person_b": 2, "type": "党政同僚",
     "context": "龙子湖区委书记与区长搭档",
     "overlap_org": "龙子湖区", "overlap_period": ""},

    # ── Predecessor-successor links (speculative) ──
    {"person_a": 1, "person_b": 3, "type": "前后任",
     "context": "倪涛接替任生（推测）任龙子湖区委书记",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "前后任",
     "context": "任生接替朱克华（推测）任龙子湖区委书记",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},

    # ── 书记与常委（均为推测性，基于通常的领导班子结构） ──
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "区委书记与专职副书记",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级",
     "context": "区委书记与组织部长",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级",
     "context": "区委书记与宣传部长",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级",
     "context": "区委书记与政法委书记",
     "overlap_org": "中共龙子湖区委", "overlap_period": ""},

    # ── 区长与副区长 ──
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长与常务副区长",
     "overlap_org": "龙子湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级",
     "context": "区长与副区长",
     "overlap_org": "龙子湖区人民政府", "overlap_period": ""},

    # ── 人大/政协 ──
    {"person_a": 1, "person_b": 12, "type": "党政同僚",
     "context": "区委书记与人大主任同届工作",
     "overlap_org": "龙子湖区", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "党政同僚",
     "context": "区委书记与政协主席同届工作",
     "overlap_org": "龙子湖区", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# ── Print summary ──
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ 数据库已创建: {DB_PATH}")
print(f"   人物: {person_count} | 机构: {org_count} | 任职: {pos_count} | 关系: {rel_count}")


# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))


def person_color(title):
    """Return r,g,b string for a person based on their role."""
    t = title or ""
    if "书记" in t and "纪委" not in t:
        if "副" in t[:5]:
            return "224,122,49"  # Orange for 副书记
        else:
            return "255,50,50"   # Red for 书记
    if "区长" in t or "市长" in t or "县长" in t:
        return "50,100,255"      # Blue
    if "纪委" in t:
        return "255,165,0"       # Orange
    if "人大" in t:
        return "100,180,180"     # Cyan
    if "政协" in t:
        return "150,100,200"     # Purple
    if "副区长" in t or "副市长" in t:
        return "80,130,220"      # Light blue
    return "100,100,100"         # Grey


def org_color(org_type):
    """Return r,g,b string for organization node."""
    colors = {
        "党委": (255, 200, 200),
        "政府": (200, 200, 255),
        "人大": (200, 255, 255),
        "政协": (255, 240, 200),
        "纪委": (255, 220, 200),
        "党委部门": (240, 200, 240),
    }
    return colors.get(org_type, (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Anhui Investigator</creator>')
lines.append('    <description>龙子湖区领导班子工作关系网络 — Longzihu District Leadership Network</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="start" type="string"/>')
lines.append('      <attribute id="3" title="end" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')

for p in persons:
    pid = f"p{p['id']}"
    c = person_color(p["current_post"])
    is_top = ("书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "")
              and "副" not in (p["current_post"] or "")[:5])
    is_gov = ("区长" in (p["current_post"] or "") and "副" not in (p["current_post"] or ""))
    sz = "20.0" if is_top else "15.0" if is_gov else "12.0"
    label = f"{p['name']} ({p['current_post'] or '?'})"

    lines.append(f'      <node id="{pid}" label="{esc(label)}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    oid = f"o{o['id']}"
    c = org_color(o["type"])
    label = f"{o['name']}"
    lines.append(f'      <node id="{oid}" label="{esc(label)}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# Position edges: person → organization (worked_at)
for po in positions:
    edge_id += 1
    source = f"p{po['person_id']}"
    target = f"o{po['org_id']}"
    p_name = next(x["name"] for x in persons if x["id"] == po["person_id"])
    o_name = next(x["name"] for x in organizations if x["id"] == po["org_id"])
    label = f"{p_name} → {o_name} ({po['title']})"
    lines.append(f'      <edge id="e{edge_id}" source="{source}" target="{target}" label="{esc(label)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(po["start"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(po["end"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Relationship edges: person ↔ person
for r in relationships:
    edge_id += 1
    source = f"p{r['person_a']}"
    target = f"p{r['person_b']}"
    a_name = next(x["name"] for x in persons if x["id"] == r["person_a"])
    b_name = next(x["name"] for x in persons if x["id"] == r["person_b"])
    is_strong = r["type"] in ("党政同僚", "前后任")
    weight = "2.0" if is_strong else "1.5"
    lines.append(f'      <edge id="e{edge_id}" source="{source}" target="{target}" label="{esc(r["context"])}" weight="{weight}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {edge_id}")

conn.close()
