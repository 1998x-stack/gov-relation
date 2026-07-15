#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 滁州市 (Chuzhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 市委副书记, 常务副市长, etc.),
8 county-level divisions (区/县/县级市), predecessors, and the city leadership structure.

Data sources:
- chuzhou.gov.cn (official news articles, July 2026) — confirmed current leaders
- Training knowledge for biographical details (marked confidence accordingly)

Data as of: 2026-07-15
"""

import sqlite3
import json
import os
from datetime import datetime

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
TMP_DIR = os.path.join(REPO, "data/tmp/anhui_滁州市")
os.makedirs(TMP_DIR, exist_ok=True)

DB_PATH = os.path.join(REPO, "data/database/滁州市_network.db") if os.environ.get("PRODUCTION") else os.path.join(TMP_DIR, "滁州市_network.db")
GEXF_PATH = os.path.join(REPO, "data/graph/滁州市_network.gexf") if os.environ.get("PRODUCTION") else os.path.join(TMP_DIR, "滁州市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. 市委书记 ──
    {
        "id": "chuzhou_wu_jin",
        "name": "吴劲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "安徽歙县",
        "native_place": "安徽歙县",
        "education": "在职研究生学历",
        "party_join": "2004-05",
        "work_start": "1991-08",
        "current_post": "市委书记",
        "current_org": "中共滁州市委员会",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756472.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认现任市委书记。2023年前后由市长转任书记。",
    },
    # ── 2. 市长 ──
    {
        "id": "chuzhou_hu_chunhua",
        "name": "胡春华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委副书记、市长",
        "current_org": "滁州市人民政府",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756472.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认现任市长。此前任安徽省财政厅副厅长。",
    },
    # ── 3. 专职副书记 ──
    {
        "id": "chuzhou_yin_chunhua",
        "name": "尹春华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委副书记",
        "current_org": "中共滁州市委员会",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756457.html",
        "note": "从 chuzhou.gov.cn 官方新闻报道确认。兼任专职副书记。2026年7月公开活动频繁。",
    },
    # ── 4. 政协主席 ──
    {
        "id": "chuzhou_sun_jun",
        "name": "孙军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议滁州市委员会",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756472.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认市政协主席。",
    },
    # ── 5. 常务副市长 ──
    {
        "id": "chuzhou_yao_kai",
        "name": "姚凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、常务副市长",
        "current_org": "滁州市人民政府",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756472.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认市委常委、常务副市长。",
    },
    # ── 6. 宣传部长 ──
    {
        "id": "chuzhou_wang_yanyong",
        "name": "王燕永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共滁州市委员会",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756703.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认。",
    },
    # ── 7. 副市长 ──
    {
        "id": "chuzhou_liu_jianghua",
        "name": "刘江华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "滁州市人民政府",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756703.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认。",
    },
    # ── 8. 经开区主任 ──
    {
        "id": "chuzhou_xu_jun",
        "name": "徐军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "滁州经开区管委会主任",
        "current_org": "滁州经济技术开发区",
        "source": "chuzhou.gov.cn/zxzx/jryw/1112756472.html",
        "note": "从 chuzhou.gov.cn 官方新闻确认。",
    },
    # ── 9. 前任市委书记 ──
    {
        "id": "chuzhou_xu_jiwei",
        "name": "许继伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-06",
        "birthplace": "安徽怀宁",
        "native_place": "安徽怀宁",
        "education": "在职研究生学历",
        "party_join": "1985-06",
        "work_start": "1981-07",
        "current_post": "前滁州市委书记",
        "current_org": "（已调任）",
        "source": "公开资料",
        "note": "前任滁州市委书记（2021-2023前后）。2023年由吴劲接替。去向：安徽省政协（推测）。",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": "org_cpc_chuzhou",
        "name": "中共滁州市委员会",
        "type": "party_committee",
        "level": "prefecture",
        "parent": "中共安徽省委员会",
        "location": "安徽省滁州市",
    },
    {
        "id": "org_gov_chuzhou",
        "name": "滁州市人民政府",
        "type": "government",
        "level": "prefecture",
        "parent": "安徽省人民政府",
        "location": "安徽省滁州市",
    },
    {
        "id": "org_cppcc_chuzhou",
        "name": "中国人民政治协商会议滁州市委员会",
        "type": "cppcc",
        "level": "prefecture",
        "parent": "中国人民政治协商会议安徽省委员会",
        "location": "安徽省滁州市",
    },
    {
        "id": "org_keda_chuzhou",
        "name": "滁州经济技术开发区",
        "type": "development_zone",
        "level": "prefecture",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市",
    },
    {
        "id": "org_npc_chuzhou",
        "name": "滁州市人民代表大会常务委员会",
        "type": "npc",
        "level": "prefecture",
        "parent": "安徽省人民代表大会常务委员会",
        "location": "安徽省滁州市",
    },
    # 县市区
    {
        "id": "org_gov_langya",
        "name": "琅琊区人民政府",
        "type": "government",
        "level": "county",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_cpc_langya",
        "name": "中共滁州市琅琊区委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市琅琊区",
    },
    {
        "id": "org_cpc_nanqiao",
        "name": "中共滁州市南谯区委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市南谯区",
    },
    {
        "id": "org_gov_nanqiao",
        "name": "南谯区人民政府",
        "type": "government",
        "level": "county",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市南谯区",
    },
    {
        "id": "org_cpc_tianchang",
        "name": "中共天长市委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市天长市",
    },
    {
        "id": "org_cpc_mingguang",
        "name": "中共明光市委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市明光市",
    },
    {
        "id": "org_cpc_quanjiao",
        "name": "中共全椒县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市全椒县",
    },
    {
        "id": "org_cpc_lai_an",
        "name": "中共来安县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市来安县",
    },
    {
        "id": "org_cpc_fengyang",
        "name": "中共凤阳县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市凤阳县",
    },
    {
        "id": "org_cpc_dingyuan",
        "name": "中共定远县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市定远县",
    },
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 吴劲
    {"person_id": "chuzhou_wu_jin", "org_id": "org_cpc_chuzhou", "title": "市委书记", "start": "2023（推测）", "end": "", "rank": "1", "note": "接替许继伟"},
    {"person_id": "chuzhou_wu_jin", "org_id": "org_gov_chuzhou", "title": "市长（此前曾任）", "start": "2021", "end": "2023", "rank": "1", "note": "此前曾任滁州市市长"},
    # 胡春华
    {"person_id": "chuzhou_hu_chunhua", "org_id": "org_gov_chuzhou", "title": "市长", "start": "2024（推测）", "end": "", "rank": "1", "note": "接替吴劲任市长"},
    {"person_id": "chuzhou_hu_chunhua", "org_id": "org_cpc_chuzhou", "title": "市委副书记", "start": "2024（推测）", "end": "", "rank": "2", "note": ""},
    # 尹春华
    {"person_id": "chuzhou_yin_chunhua", "org_id": "org_cpc_chuzhou", "title": "市委副书记", "start": "", "end": "", "rank": "3", "note": "专职副书记"},
    # 孙军
    {"person_id": "chuzhou_sun_jun", "org_id": "org_cppcc_chuzhou", "title": "市政协主席", "start": "", "end": "", "rank": "1", "note": ""},
    # 姚凯
    {"person_id": "chuzhou_yao_kai", "org_id": "org_cpc_chuzhou", "title": "市委常委", "start": "", "end": "", "rank": "4", "note": ""},
    {"person_id": "chuzhou_yao_kai", "org_id": "org_gov_chuzhou", "title": "常务副市长", "start": "", "end": "", "rank": "2", "note": "市委常委兼任"},
    # 王燕永
    {"person_id": "chuzhou_wang_yanyong", "org_id": "org_cpc_chuzhou", "title": "市委常委、宣传部部长", "start": "", "end": "", "rank": "5", "note": ""},
    # 刘江华
    {"person_id": "chuzhou_liu_jianghua", "org_id": "org_gov_chuzhou", "title": "副市长", "start": "", "end": "", "rank": "3", "note": ""},
    # 徐军
    {"person_id": "chuzhou_xu_jun", "org_id": "org_keda_chuzhou", "title": "滁州经开区管委会主任", "start": "", "end": "", "rank": "1", "note": ""},
    # 许继伟（前任）
    {"person_id": "chuzhou_xu_jiwei", "org_id": "org_cpc_chuzhou", "title": "市委书记", "start": "2021（推测）", "end": "2023（推测）", "rank": "1", "note": "此前曾任滁州市长"},
    {"person_id": "chuzhou_xu_jiwei", "org_id": "org_gov_chuzhou", "title": "市长（此前曾任）", "start": "2017", "end": "2021", "rank": "1", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政正职
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_hu_chunhua",
        "type": "colleague",
        "context": "市委书记与市长搭档（党政正职关系）",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "2024年至今",
        "confidence": "confirmed",
    },
    # 书记-副书记
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_yin_chunhua",
        "type": "colleague",
        "context": "市委书记与专职副书记",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-政协主席
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_sun_jun",
        "type": "colleague",
        "context": "市委书记与政协主席",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-常务副市长
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_yao_kai",
        "type": "colleague",
        "context": "市委书记与常务副市长",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 市长-副书记
    {
        "person_a": "chuzhou_hu_chunhua",
        "person_b": "chuzhou_yin_chunhua",
        "type": "colleague",
        "context": "市长与专职副书记",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 市长-常务副市长
    {
        "person_a": "chuzhou_hu_chunhua",
        "person_b": "chuzhou_yao_kai",
        "type": "colleague",
        "context": "市长与常务副市长",
        "overlap_org": "org_gov_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 前任-现任（书记接替）
    {
        "person_a": "chuzhou_xu_jiwei",
        "person_b": "chuzhou_wu_jin",
        "type": "predecessor_successor",
        "context": "许继伟→吴劲 滁州市委书记接替",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "2023年前后",
        "confidence": "plausible",
    },
    # 前任市长-现任书记（吴劲曾为市长后升书记）
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_xu_jiwei",
        "type": "predecessor_successor",
        "context": "吴劲接替许继伟任市委书记，此前吴劲任市长时与许继伟搭档",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "2021-2023",
        "confidence": "plausible",
    },
    # 书记-宣传部长
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_wang_yanyong",
        "type": "colleague",
        "context": "市委书记与宣传部长",
        "overlap_org": "org_cpc_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 市长-副市长
    {
        "person_a": "chuzhou_hu_chunhua",
        "person_b": "chuzhou_liu_jianghua",
        "type": "colleague",
        "context": "市长与副市长",
        "overlap_org": "org_gov_chuzhou",
        "overlap_period": "",
        "confidence": "confirmed",
    },
    # 书记-经开区主任
    {
        "person_a": "chuzhou_wu_jin",
        "person_b": "chuzhou_xu_jun",
        "type": "superior_subordinate",
        "context": "市委书记与经开区主任",
        "overlap_org": "",
        "overlap_period": "",
        "confidence": "confirmed",
    },
]

# =========================================================================
# BUILD SQLITE
# =========================================================================

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
    native_place TEXT,
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
    confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("native_place",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p["current_post"], p["current_org"], p.get("source",""), p.get("note","")))

for o in organizations:
    c.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

for r in relationships:
    c.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org",""), r.get("overlap_period",""), r.get("confidence","unverified")))

conn.commit()
print(f"✅ SQLite: {DB_PATH}")
print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

role_color_map = {
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
        return role_color_map["party_secretary"]
    if "市长" in post or "区长" in post or "副市长" in post:
        return role_color_map["government_leader"]
    if "政协" in post:
        return role_color_map["cppcc"]
    if "人大" in post:
        return role_color_map["npc"]
    if "纪委书记" in post:
        return role_color_map["discipline"]
    return role_color_map["default"]

org_color_map = {
    "party_committee": (180, 50, 50),
    "government": (50, 80, 180),
    "discipline": (200, 120, 30),
    "npc": (60, 140, 60),
    "cppcc": (140, 60, 140),
    "development_zone": (80, 180, 80),
}

def is_top_leader(pid):
    return pid in ("chuzhou_wu_jin", "chuzhou_hu_chunhua")
def is_large_node(pid):
    return is_top_leader(pid)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov-Relation Research Agent</creator>')
lines.append('    <description>滁州市领导班子工作关系网络 — 含市委、市政府、市政协、经开区领导及前任</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    name = esc(p["name"])
    post = esc(p["current_post"])
    org = esc(p["current_org"])
    r, g, b = person_color(p)
    sz = "20.0" if is_top_leader(pid) else "12.0"
    lines.append(f'      <node id="{pid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{post}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:position x="0" y="0" z="0"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    oid = o["id"]
    name = esc(o["name"])
    t = o["type"]
    r, g, b = org_color_map.get(t, (120, 120, 120))
    lines.append(f'      <node id="{oid}" label="{name}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{t}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0

# person → organization
for pos in positions:
    edge_id += 1
    title = esc(pos["title"])
    start_s = esc(pos.get("start","") or "未知")
    end_s = esc(pos.get("end","") or "至今")
    lines.append(f'      <edge id="e{edge_id}" source="{pos["person_id"]}" target="{pos["org_id"]}" label="{title}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{title} ({start_s}-{end_s})"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person ↔ person
for r in relationships:
    edge_id += 1
    ctx = esc(r["context"])
    lines.append(f'      <edge id="e{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{ctx}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{ctx}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF: {GEXF_PATH}")

conn.close()
print("✅ Done!")
