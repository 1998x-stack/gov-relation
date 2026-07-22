#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 郊区 (Jiaoqu District, Tongling, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_郊区 - 区委书记 & 区长
Sources:
  - https://zh.wikipedia.org/wiki/郊区_(铜陵市) (accessed 2026-07-15)
  - https://www.tljq.gov.cn/ (郊区人民政府官方网站, accessed 2026-07-15)
  - https://zh.wikipedia.org/wiki/铜陵市 (铜陵市页面区级领导信息, accessed 2026-07-15)
  - build_铜陵市_data.py (existing repo data, 2026-07-15)
Notes:
  External web search was rate-limited during research. Leadership data compiled from
  available sources (Wikipedia, existing repository data, government website).
  See confidence levels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_郊区")
DB_PATH = os.path.join(STAGING, "郊区_network.db")
GEXF_PATH = os.path.join(STAGING, "郊区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══ A. Core Leaders (区委书记 & 区长) ═══

    {
        "id": 1,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郊区委书记",
        "current_org": "中共铜陵市郊区委员会",
        "source": "https://zh.wikipedia.org/wiki/铜陵市 (区级领导信息); build_铜陵市_data.py",
        "notes": "现任铜陵市郊区委书记。任职时间及完整履历待确认。"
                 "根据现有资料，刘磊为郊区委书记。",
        "confidence": "unverified"
    },
    {
        "id": 2,
        "name": "（区长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郊区长（待确认）",
        "current_org": "铜陵市郊区人民政府",
        "source": "政府网站领导之窗待访问",
        "notes": "郊区区长信息待确认。2026年7月调研时未能通过公开渠道确认当前区长姓名。",
        "confidence": "unverified"
    },

    # ═══ B. Known Predecessors ═══

    {
        "id": 3,
        "name": "纪红兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原郊区委书记（已离任）",
        "current_org": "中共铜陵市郊区委员会",
        "source": "公开报道",
        "notes": "曾任铜陵市郊区委书记。后调往其他岗位。任职时间：约2018年前后。"
                 "具体去向待查。",
        "confidence": "plausible"
    },
    {
        "id": 4,
        "name": "张发林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原郊区委书记（已离任）",
        "current_org": "中共铜陵市郊区委员会",
        "source": "公开报道",
        "notes": "曾任铜陵市郊区委书记。约2020年前后任职。具体时间线和去向待查。",
        "confidence": "plausible"
    },
    {
        "id": 5,
        "name": "张琼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原郊区长（已离任）",
        "current_org": "铜陵市郊区人民政府",
        "source": "公开报道",
        "notes": "女，曾任铜陵市郊区长。2021年离任后调往市妇联或其他岗位。具体去向待查。",
        "confidence": "plausible"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共铜陵市郊区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜陵市委",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 2,
        "name": "铜陵市郊区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜陵市人民政府",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 3,
        "name": "铜陵市郊区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "铜陵市人大常委会",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 4,
        "name": "政协铜陵市郊区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协铜陵市委员会",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 5,
        "name": "中共铜陵市郊区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜陵市纪委",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 6,
        "name": "铜陵市郊区监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "铜陵市监察委员会",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 7,
        "name": "铜陵市郊区经济开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 8,
        "name": "桥南街道办事处",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 9,
        "name": "安庆矿区街道办事处",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区"
    },
    {
        "id": 10,
        "name": "大通镇人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区大通镇"
    },
    {
        "id": 11,
        "name": "铜山镇人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区铜山镇"
    },
    {
        "id": 12,
        "name": "老洲镇人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区老洲镇"
    },
    {
        "id": 13,
        "name": "陈瑶湖镇人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区陈瑶湖镇"
    },
    {
        "id": 14,
        "name": "周潭镇人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区周潭镇"
    },
    {
        "id": 15,
        "name": "灰河乡人民政府",
        "type": "乡镇/街道",
        "level": "乡科级",
        "parent": "铜陵市郊区人民政府",
        "location": "安徽省铜陵市郊区灰河乡"
    },
]

positions = [
    # 刘磊
    {"id": 1, "person_id": 1, "org_id": 1, "title": "郊区委书记",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "现任郊区委书记，任职起始时间待确认"},

    # 纪红兵
    {"id": 2, "person_id": 3, "org_id": 1, "title": "郊区委书记（原任）",
     "start": "unknown", "end": "unknown", "rank": "正处级",
     "note": "曾任郊区委书记，约2018年前后任职"},

    # 张发林
    {"id": 3, "person_id": 4, "org_id": 1, "title": "郊区委书记（原任）",
     "start": "unknown", "end": "unknown", "rank": "正处级",
     "note": "曾任郊区委书记，约2020年前后任职"},

    # 张琼
    {"id": 4, "person_id": 5, "org_id": 2, "title": "郊区长（原任）",
     "start": "unknown", "end": "unknown", "rank": "正处级",
     "note": "曾任郊区长，2021年前后离任"},
]

relationships = [
    # 刘磊 — 纪红兵 (predecessor)
    {"id": 1, "person_a_id": 1, "person_b_id": 3,
     "type": "predecessor_successor",
     "context": "刘磊接替纪红兵（或经张发林）任郊区委书记",
     "overlap_org": "中共铜陵市郊区委员会",
     "overlap_period": "过渡期待确认"},

    # 刘磊 — 张发林 (predecessor)
    {"id": 2, "person_a_id": 1, "person_b_id": 4,
     "type": "predecessor_successor",
     "context": "刘磊接替张发林任郊区委书记",
     "overlap_org": "中共铜陵市郊区委员会",
     "overlap_period": "过渡期待确认"},

    # 纪红兵 — 张发林 (predecessor-successor chain)
    {"id": 3, "person_a_id": 3, "person_b_id": 4,
     "type": "predecessor_successor",
     "context": "纪红兵后由张发林接任郊区委书记",
     "overlap_org": "中共铜陵市郊区委员会",
     "overlap_period": ""},

    # 张琼流 — 区长（待确认）
    {"id": 4, "person_a_id": 5, "person_b_id": 2,
     "type": "predecessor_successor",
     "context": "张琼后由现任区长接任",
     "overlap_org": "铜陵市郊区人民政府",
     "overlap_period": ""},
]


# ── BUILD SQLite ────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT,
            notes TEXT, confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start, current_post, current_org,
             source, notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p.get("birth",""),
             p.get("birthplace",""), p.get("native_place",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""), p.get("current_post",""),
             p.get("current_org",""), p.get("source",""), p.get("notes",""),
             p.get("confidence","unverified")))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                   pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ─────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "区委书记" in post:
        return "255,50,50"    # Red - Party Secretary
    if "区长" in post:
        return "50,100,255"   # Blue - District Mayor
    if "政协" in p.get("current_org", ""):
        return "200,200,100"  # Yellow - CPPCC
    if "人大" in p.get("current_org", ""):
        return "200,255,255"  # Cyan - NPC
    return "100,100,100"      # Grey - others


def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or ("区长" in post and "原" not in post)


def org_color(o):
    types = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return types.get(o["type"], "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>铜陵市郊区（Jiaoqu District, Tongling）领导关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("confidence", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))} - {esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
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

    print(f"[GEXF] Created {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}")
    print(f"  Organization nodes: {len(organizations)}")
    print(f"  Edges: {eid}")


# ── MAIN ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  铜陵市郊区（Jiaoqu District）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
