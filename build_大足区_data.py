#!/usr/bin/env python3
"""
重庆市大足区领导班子工作关系网络 — 数据构建脚本
Build SQLite database and GEXF graph for Dazu District (Chongqing) leadership network.

Research date: 2026-07-16
DataSource: https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息页面)
Confirmed current as of: 2026-07-16

区委领导:
  书记: 徐晓勇
  副书记: 毛大春, 罗晓春
  区委常委: 杨烈, 张明, 雷科, 邓茂强, 吴亚莉, 杨桦, 周海峰

区政府领导:
  区长: 毛大春
  常务副区长: 雷科
  副区长: 邓茂强, 王大蓉, 杨爱民, 尹道勇, 孟怀勇, 叶小龙, 詹娜, 吴普

Note: Due to geo-restrictions, Baidu Baike (403) and Wikipedia (timeout) were
inaccessible from this environment. Biographical details (birth dates, birthplace,
education, party_join, work_start) are marked "待查" pending access to:
  - baike.baidu.com (currently returning 403)
  - zh.wikipedia.org (timed out)
  - Internal government biography pages
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING_DIR = os.path.join(BASE, "data/tmp/chongqing_大足区")
DB_PATH = os.path.join(STAGING_DIR, "大足区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "大足区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ════════════════════════
    # Top Leaders (目标人物)
    # ════════════════════════

    # 徐晓勇 — 大足区委书记 (Party Secretary)
    {"id": 1, "name": "徐晓勇", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "中共重庆市大足区委书记", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 毛大春 — 大足区委副书记、区长 (Mayor/District Chief)
    {"id": 2, "name": "毛大春", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委副书记、区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # ════════════════════════
    # 区委领导班子
    # ════════════════════════

    # 罗晓春 — 区委副书记
    {"id": 3, "name": "罗晓春", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委副书记", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 杨烈 — 区委常委
    {"id": 4, "name": "杨烈", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 张明 — 区委常委
    {"id": 5, "name": "张明", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 雷科 — 区委常委、常务副区长
    {"id": 6, "name": "雷科", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委、常务副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 邓茂强 — 区委常委、副区长
    {"id": 7, "name": "邓茂强", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委、副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 吴亚莉 — 区委常委 (女)
    {"id": 8, "name": "吴亚莉", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 杨桦 — 区委常委
    {"id": 9, "name": "杨桦", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 周海峰 — 区委常委
    {"id": 10, "name": "周海峰", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区委常委", "current_org": "中共重庆市大足区委员会",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # ════════════════════════
    # 区政府副区长
    # ════════════════════════

    # 王大蓉 — 副区长 (女)
    {"id": 11, "name": "王大蓉", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 杨爱民 — 副区长
    {"id": 12, "name": "杨爱民", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 尹道勇 — 副区长
    {"id": 13, "name": "尹道勇", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 孟怀勇 — 副区长
    {"id": 14, "name": "孟怀勇", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 叶小龙 — 副区长
    {"id": 15, "name": "叶小龙", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 詹娜 — 副区长 (女)
    {"id": 16, "name": "詹娜", "gender": "女", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},

    # 吴普 — 副区长
    {"id": 17, "name": "吴普", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "待查", "work_start": "待查",
     "current_post": "大足区副区长", "current_org": "大足区人民政府",
     "source": "https://www.dazu.gov.cn/zwgk_175/ (大足区政府政务公开-领导信息)"},
]

organizations = [
    {"id": 1, "name": "中共重庆市大足区委员会", "type": "党委", "level": "县级", "parent": "中共重庆市委", "location": "重庆市大足区"},
    {"id": 2, "name": "大足区人民政府", "type": "政府", "level": "县级", "parent": "重庆市人民政府", "location": "重庆市大足区"},
    {"id": 3, "name": "大足区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "重庆市大足区"},
    {"id": 4, "name": "中国人民政治协商会议重庆市大足区委员会", "type": "政协", "level": "县级", "parent": "", "location": "重庆市大足区"},
]

positions = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "中共重庆市大足区委书记", "start": "待查", "end": "", "rank": "正厅级（直辖市辖区）", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "大足区委副书记", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "大足区区长", "start": "待查", "end": "", "rank": "正厅级（直辖市辖区）", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "大足区委副书记", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "大足区常务副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "大足区委常委", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    # 副区长
    {"person_id": 11, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "大足区副区长", "start": "待查", "end": "", "rank": "副厅级", "note": ""},
]

relationships = [
    # Top leadership team
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "区委书记与区长党政搭档", "overlap_org": "中共重庆市大足区委员会/大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "领导团队", "context": "区委书记与副书记共事", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 3, "type": "领导团队", "context": "区委副书记/区长与专职副书记共事", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    # 区委常委间
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与区委常委、常务副区长", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与区委常委、副区长", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记与区委常委", "overlap_org": "中共重庆市大足区委员会", "overlap_period": "2026-"},
    # 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "区长与副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    # 常务副区长与副区长
    {"person_a": 6, "person_b": 11, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 12, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 13, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 14, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 15, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 16, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
    {"person_a": 6, "person_b": 17, "type": "同僚", "context": "常务副区长与其他副区长", "overlap_org": "大足区人民政府", "overlap_period": "2026-"},
]

# ── BUILD DATABASE ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
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

# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(title, is_party_secretary=False):
    """Return GEXF viz color for a person based on role."""
    t = title or ""
    if "书记" in t and "纪委" not in t:
        return "255,50,50"  # Red
    if "区长" in t or "县长" in t:
        return "50,100,255"  # Blue
    if "纪委" in t:
        return "255,165,0"   # Orange
    return "100,100,100"    # Grey

def org_color_gexf(org_type):
    """Return GEXF viz color for an organization based on type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Gov Relation Research Agent</creator>')
lines.append('    <description>重庆市大足区领导班子工作关系网络</description>')
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

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["current_post"])
    is_top = "书记" in (p["current_post"] or "") and "纪委" not in (p["current_post"] or "")
    is_mayor = "区长" in (p["current_post"] or "")
    sz = "20.0" if is_top else "15.0" if is_mayor else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    oc = org_color_gexf(o["type"])
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges - person->organization (worked_at)
lines.append('    <edges>')
eid = 0
for po in positions:
    eid += 1
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_label = f"{p['name']} → {o['name']} ({po['title']})"
    lines.append(f'      <edge id="e{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(edge_label)}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Edges - person<->person (relationship), weight="2.0"
for r in relationships:
    eid += 1
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF 已创建: {GEXF_PATH}")
print(f"   节点: {len(persons) + len(organizations)} | 边: {eid}")

conn.close()
print("✅ 完成!")
