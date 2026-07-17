#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 琅琊区 (Langya District) leadership network."""

import sqlite3
import json
import os
from datetime import datetime

DB_DIR = os.path.join(os.path.dirname(__file__), "data", "database")
GEXF_DIR = os.path.join(os.path.dirname(__file__), "data", "graph")
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GEXF_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, "langya_district.db")
GEXF_PATH = os.path.join(GEXF_DIR, "langya_district.gexf")

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    {
        "id": "langya_wang_zheng",
        "name": "王政",
        "gender": "male",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "2026年6月第八届区委连任。出生年月、籍贯、学历、此前履历均未知。",
    },
    {
        "id": "langya_zhang_shaohua",
        "name": "张少华",
        "gender": "male",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长、区政府党组书记",
        "current_org": "滁州市琅琊区人民政府",
        "source": "lyq.gov.cn/zwdt/zwyw/392402520.html",
        "note": "出生年月、籍贯、学历、此前履历均未知。",
    },
    {
        "id": "langya_jiang_zhugang",
        "name": "蒋助纲",
        "gender": "male",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区委政法委书记",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名和职务确认。个人履历未知。",
    },
    {
        "id": "langya_wei_kai",
        "name": "魏凯",
        "gender": "male",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长（推测）",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_wu_min",
        "name": "吴敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_zhi_rongxin",
        "name": "支荣鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_lu_xiaodi",
        "name": "陆晓笛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_su_xiaoning",
        "name": "苏小宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_fan_shilu",
        "name": "樊士璐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_chai_dongdong",
        "name": "柴栋栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_xu_jin",
        "name": "徐进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共滁州市琅琊区纪律检查委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名和职务确认。个人履历未知。",
    },
    {
        "id": "langya_li_aiguo",
        "name": "李爱国",
        "gender": "male",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "滁州市琅琊区人民代表大会常务委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
    {
        "id": "langya_chen_youli",
        "name": "陈友利",
        "gender": "male",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议滁州市琅琊区委员会",
        "source": "lyq.gov.cn/zwdt/zwyw/392401928.html",
        "note": "仅姓名确认。",
    },
]

organizations = [
    {
        "id": "org_cpc_langya",
        "name": "中共滁州市琅琊区委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_gov_langya",
        "name": "滁州市琅琊区人民政府",
        "type": "government",
        "level": "county",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_cdi_langya",
        "name": "中共滁州市琅琊区纪律检查委员会",
        "type": "discipline",
        "level": "county",
        "parent": "中共滁州市纪律检查委员会",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_npc_langya",
        "name": "滁州市琅琊区人民代表大会常务委员会",
        "type": "npc",
        "level": "county",
        "parent": "滁州市人民代表大会常务委员会",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_cppcc_langya",
        "name": "中国人民政治协商会议滁州市琅琊区委员会",
        "type": "cppcc",
        "level": "county",
        "parent": "中国人民政治协商会议滁州市委员会",
        "location": "安徽省滁州市琅琊区",
    },
]

positions = [
    {"person_id": "langya_wang_zheng", "org_id": "org_cpc_langya", "title": "区委书记", "start": "2021-06（推测）", "end": "", "rank": "1", "note": "2026年6月第八届连任"},
    {"person_id": "langya_zhang_shaohua", "org_id": "org_gov_langya", "title": "区长、区政府党组书记", "start": "", "end": "", "rank": "1", "note": "同时任区委副书记"},
    {"person_id": "langya_zhang_shaohua", "org_id": "org_cpc_langya", "title": "区委副书记", "start": "", "end": "", "rank": "2", "note": ""},
    {"person_id": "langya_jiang_zhugang", "org_id": "org_cpc_langya", "title": "区委副书记、区委政法委书记", "start": "", "end": "", "rank": "3", "note": ""},
    {"person_id": "langya_wei_kai", "org_id": "org_cpc_langya", "title": "区委常委、组织部部长（推测）", "start": "", "end": "", "rank": "4", "note": ""},
    {"person_id": "langya_wu_min", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "5", "note": ""},
    {"person_id": "langya_zhi_rongxin", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "6", "note": ""},
    {"person_id": "langya_lu_xiaodi", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "7", "note": ""},
    {"person_id": "langya_su_xiaoning", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "8", "note": ""},
    {"person_id": "langya_fan_shilu", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "9", "note": ""},
    {"person_id": "langya_chai_dongdong", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "10", "note": ""},
    {"person_id": "langya_xu_jin", "org_id": "org_cdi_langya", "title": "区纪委书记、区监委主任", "start": "", "end": "", "rank": "4", "note": "兼任区委常委"},
    {"person_id": "langya_xu_jin", "org_id": "org_cpc_langya", "title": "区委常委", "start": "", "end": "", "rank": "11", "note": ""},
    {"person_id": "langya_li_aiguo", "org_id": "org_npc_langya", "title": "区人大常委会主任", "start": "", "end": "", "rank": "1", "note": ""},
    {"person_id": "langya_chen_youli", "org_id": "org_cppcc_langya", "title": "区政协主席", "start": "", "end": "", "rank": "1", "note": ""},
]

relationships = [
    {
        "person_a": "langya_wang_zheng",
        "person_b": "langya_zhang_shaohua",
        "type": "colleague",
        "context": "区委书记与区长搭档（党政正职关系）",
        "overlap_org": "org_cpc_langya",
        "overlap_period": "2026年6月至今（第八届区委）",
    },
    {
        "person_a": "langya_wang_zheng",
        "person_b": "langya_jiang_zhugang",
        "type": "colleague",
        "context": "区委书记与专职副书记/政法委书记",
        "overlap_org": "org_cpc_langya",
        "overlap_period": "",
    },
    {
        "person_a": "langya_wang_zheng",
        "person_b": "langya_xu_jin",
        "type": "colleague",
        "context": "区委书记与纪委书记",
        "overlap_org": "org_cpc_langya",
        "overlap_period": "",
    },
    {
        "person_a": "langya_zhang_shaohua",
        "person_b": "langya_jiang_zhugang",
        "type": "colleague",
        "context": "区长与专职副书记",
        "overlap_org": "org_cpc_langya",
        "overlap_period": "",
    },
    {
        "person_a": "langya_wang_zheng",
        "person_b": "langya_li_aiguo",
        "type": "colleague",
        "context": "区委书记与人大主任",
        "overlap_org": "",
        "overlap_period": "",
    },
    {
        "person_a": "langya_wang_zheng",
        "person_b": "langya_chen_youli",
        "type": "colleague",
        "context": "区委书记与政协主席",
        "overlap_org": "",
        "overlap_period": "",
    },
]

# ── Build SQLite ──────────────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY,
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
    source TEXT,
    note TEXT
);

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT NOT NULL,
    person_b TEXT NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"], p.get("note", "")))

for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos.get("note", "")))

for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

conn.commit()
print(f"✅ SQLite: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

# ── Build GEXF ────────────────────────────────────────────────────────────────

def gexf_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

role_color = {
    "party_secretary": (200, 60, 50),
    "government_leader": (50, 100, 200),
    "discipline": (220, 140, 40),
    "npc": (80, 160, 80),
    "cppcc": (160, 80, 160),
    "default": (150, 150, 150),
}

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "副书记" not in post:
        return role_color["party_secretary"]
    if "区长" in post:
        return role_color["government_leader"]
    if "纪委书记" in post:
        return role_color["discipline"]
    if "人大" in post or "人大常委会" in post:
        return role_color["npc"]
    if "政协" in post:
        return role_color["cppcc"]
    return role_color["default"]

org_color_map = {
    "party_committee": (180, 50, 50),
    "government": (50, 80, 180),
    "discipline": (200, 120, 30),
    "npc": (60, 140, 60),
    "cppcc": (140, 60, 140),
}

def org_color_hex(t):
    r, g, b = org_color_map.get(t, (120, 120, 120))
    return f"{r:02x}{g:02x}{b:02x}"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append("  <graph mode=\"static\" defaultedgetype=\"undirected\">")

# Attributes
lines.append("    <attributes class=\"node\">")
lines.append("      <attribute id=\"type\" title=\"type\" type=\"string\"/>")
lines.append("      <attribute id=\"role\" title=\"role\" type=\"string\"/>")
lines.append("      <attribute id=\"source\" title=\"source\" type=\"string\"/>")
lines.append("    </attributes>")
lines.append("    <attributes class=\"edge\">")
lines.append("      <attribute id=\"type\" title=\"type\" type=\"string\"/>")
lines.append("      <attribute id=\"context\" title=\"context\" type=\"string\"/>")
lines.append("    </attributes>")

# Nodes: persons
lines.append("    <nodes>")
for p in persons:
    pid = p["id"]
    name = gexf_escape(p["name"])
    post = gexf_escape(p["current_post"])
    org = gexf_escape(p["current_org"])
    birth = gexf_escape(p["birth"] or "未知")
    r, g, b = person_color(p)
    size = "20.0" if pid in ("langya_wang_zheng", "langya_zhang_shaohua") else "12.0"
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append(f"        <attvalues>")
    lines.append(f"          <attvalue for=\"type\" value=\"person\"/>")
    lines.append(f"          <attvalue for=\"role\" value=\"{post}\"/>")
    lines.append(f"          <attvalue for=\"source\" value=\"{gexf_escape(p['source'])}\"/>")
    lines.append(f"        </attvalues>")
    lines.append(f"        <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\" a=\"1.0\"/>")
    lines.append(f"        <viz:size value=\"{size}\"/>")
    lines.append(f"        <viz:position x=\"0\" y=\"0\" z=\"0\"/>")
    lines.append(f"        <viz:shape value=\"disc\"/>")
    lines.append(f"      </node>")

# Nodes: organizations
for o in organizations:
    oid = o["id"]
    name = gexf_escape(o["name"])
    t = o["type"]
    r, g, b = org_color_map.get(t, (120, 120, 120))
    lines.append(f'      <node id="{oid}" label="{name}">')
    lines.append(f"        <attvalues>")
    lines.append(f"          <attvalue for=\"type\" value=\"organization\"/>")
    lines.append(f"          <attvalue for=\"role\" value=\"{t}\"/>")
    lines.append(f"        </attvalues>")
    lines.append(f"        <viz:color r=\"{r}\" g=\"{g}\" b=\"{b}\" a=\"1.0\"/>")
    lines.append(f"        <viz:size value=\"8.0\"/>")
    lines.append(f"        <viz:shape value=\"square\"/>")
    lines.append(f"      </node>")
lines.append("    </nodes>")

# Edges
lines.append("    <edges>")
edge_id = 0
# person → organization
for pos in positions:
    edge_id += 1
    p = next(x for x in persons if x["id"] == pos["person_id"])
    title = gexf_escape(pos["title"])
    start = gexf_escape(pos["start"] or "未知")
    end = gexf_escape(pos["end"] or "至今")
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{title}">')
    lines.append(f"        <attvalues>")
    lines.append(f"          <attvalue for=\"type\" value=\"worked_at\"/>")
    lines.append(f"          <attvalue for=\"context\" value=\"{title} ({start}-{end})\"/>")
    lines.append(f"        </attvalues>")
    lines.append(f"      </edge>")

# person ↔ person
for r in relationships:
    edge_id += 1
    ctx = gexf_escape(r["context"])
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{ctx}">')
    lines.append(f"        <attvalues>")
    lines.append(f"          <attvalue for=\"type\" value=\"relationship\"/>")
    lines.append(f"          <attvalue for=\"context\" value=\"{ctx}\"/>")
    lines.append(f"        </attvalues>")
    lines.append(f"      </edge>")
lines.append("    </edges>")

lines.append("  </graph>")
lines.append("</gexf>")

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")

conn.close()
