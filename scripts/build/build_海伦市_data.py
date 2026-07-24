#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海伦市 leadership network.
海伦市 — 县级市，黑龙江省绥化市下辖。
"""

import sys
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE)

STAGING = os.path.join(BASE, "data/tmp/heilongjiang_海伦市")
DB_PATH = os.path.join(STAGING, "海伦市_network.db")
GEXF_PATH = os.path.join(STAGING, "海伦市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (市委书记) ──
    {
        "id": 1,
        "name": "侯绍波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共海伦市委书记",
        "current_org": "中共海伦市委员会",
        "source": "https://www.hailun.gov.cn/ (confirmed via news: 侯绍波主持市委常委会、调研防汛等, July 2026)"
    },
    # ── Current Mayor (市长) ──
    {
        "id": 2,
        "name": "刘晓光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市人民政府市长",
        "current_org": "海伦市人民政府",
        "source": "https://www.hailun.gov.cn/ (confirmed via news: 刘晓光主持市政府常务会议、安委会会议等, 2026)"
    },
    # ── Deputy Party Secretary (市委副书记 — placeholder) ──
    {
        "id": 3,
        "name": "市委副书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共海伦市委副书记",
        "current_org": "中共海伦市委员会",
        "source": "未找到公开来源; 需绥化市委组织部任前公示或海伦市领导之窗页面确认"
    },
    # ── Executive Deputy Mayor (常务副市长 — placeholder) ──
    {
        "id": 4,
        "name": "常务副市长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、常务副市长",
        "current_org": "海伦市人民政府",
        "source": "未找到公开来源; 需海伦市政府领导分工页面确认"
    },
    # ── Discipline Inspection Secretary (纪委书记 — placeholder) ──
    {
        "id": 5,
        "name": "纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、纪委书记、监委主任",
        "current_org": "中共海伦市纪律检查委员会",
        "source": "未找到公开来源; 需海伦市领导之窗页面确认"
    },
    # ── Organization Department Head (组织部长 — placeholder) ──
    {
        "id": 6,
        "name": "组织部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、组织部部长",
        "current_org": "中共海伦市委员会组织部",
        "source": "未找到公开来源; 需海伦市领导之窗页面确认"
    },
    # ── Propaganda Head (宣传部长 — placeholder) ──
    {
        "id": 7,
        "name": "宣传部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、宣传部部长",
        "current_org": "中共海伦市委员会宣传部",
        "source": "未找到公开来源; 需海伦市领导之窗页面确认"
    },
    # ── Political/Legal Affairs Head (政法委书记 — placeholder) ──
    {
        "id": 8,
        "name": "政法委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、政法委书记",
        "current_org": "中共海伦市委员会政法委员会",
        "source": "未找到公开来源; 需海伦市领导之窗页面确认"
    },
    # ── United Front Head (统战部长 — placeholder) ──
    {
        "id": 9,
        "name": "统战部部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市委常委、统战部部长",
        "current_org": "中共海伦市委员会统战部",
        "source": "未找到公开来源; 需海伦市领导之窗页面确认"
    },
    # ── People's Congress Chairman (人大主任 — placeholder) ──
    {
        "id": 10,
        "name": "市人大常委会主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市人大常委会主任",
        "current_org": "海伦市人民代表大会常务委员会",
        "source": "未找到公开来源; 需海伦市人大信息页面确认"
    },
    # ── CPPCC Chairman (政协主席 — placeholder) ──
    {
        "id": 11,
        "name": "市政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "海伦市政协主席",
        "current_org": "中国人民政治协商会议海伦市委员会",
        "source": "未找到公开来源; 需海伦市政协信息页面确认"
    },
    # ── Predecessor Party Secretary (placeholder) ──
    {
        "id": 12,
        "name": "前任市委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "未找到公开来源; 需绥化市委组织部任免公告确认"
    },
    # ── Predecessor Mayor (placeholder) ──
    {
        "id": 13,
        "name": "前任市长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "未找到公开来源; 需绥化市委组织部任免公告确认"
    },
]

organizations = [
    {"id": 1, "name": "中共海伦市委员会", "type": "党委", "level": "县级", "parent": "中共绥化市委员会", "location": "海伦市"},
    {"id": 2, "name": "海伦市人民政府", "type": "政府", "level": "县级", "parent": "绥化市人民政府", "location": "海伦市"},
    {"id": 3, "name": "中共海伦市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共绥化市纪律检查委员会", "location": "海伦市"},
    {"id": 4, "name": "海伦市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "绥化市人民代表大会常务委员会", "location": "海伦市"},
    {"id": 5, "name": "中国人民政治协商会议海伦市委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议绥化市委员会", "location": "海伦市"},
    {"id": 6, "name": "中共海伦市委员会组织部", "type": "党委", "level": "县级", "parent": "中共海伦市委员会", "location": "海伦市"},
    {"id": 7, "name": "中共海伦市委员会宣传部", "type": "党委", "level": "县级", "parent": "中共海伦市委员会", "location": "海伦市"},
    {"id": 8, "name": "中共海伦市委员会政法委员会", "type": "党委", "level": "县级", "parent": "中共海伦市委员会", "location": "海伦市"},
    {"id": 9, "name": "中共海伦市委员会统战部", "type": "党委", "level": "县级", "parent": "中共海伦市委员会", "location": "海伦市"},
]

positions = [
    # 侯绍波
    {"person_id": 1, "org_id": 1, "title": "中共海伦市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月仍在任"},
    # 刘晓光
    {"person_id": 2, "org_id": 2, "title": "海伦市人民政府市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月仍在任"},
    # Placeholder positions
    {"person_id": 3, "org_id": 1, "title": "中共海伦市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 4, "org_id": 2, "title": "海伦市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 5, "org_id": 3, "title": "海伦市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 6, "org_id": 6, "title": "海伦市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 7, "org_id": 7, "title": "海伦市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 8, "org_id": 8, "title": "海伦市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 9, "org_id": 9, "title": "海伦市委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认"},
    {"person_id": 10, "org_id": 4, "title": "海伦市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认"},
    {"person_id": 11, "org_id": 5, "title": "海伦市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认"},
]

relationships = [
    # 侯绍波 ↔ 刘晓光 (党政一把手)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政搭档", "overlap_org": "海伦市", "overlap_period": "2026"},
]

# ── BUILD ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post and "组织" not in post:
        return "255,50,50"
    if "市长" in post or "副市长" in post or "区长" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    return p["id"] in (1, 2)

def org_color(o):
    t = o.get("type", "")
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
        "乡镇": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
    }.get(t, "200,200,200")

def build_db():
    import sqlite3
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # Drop existing
    for t in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    # Create tables
    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    # Insert
    for p in persons:
        conn.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
            education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"],
             p["current_org"], p["source"]))

    for o in organizations:
        conn.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        conn.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"],
             pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        conn.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>海伦市领导班子工作关系网络 - 黑龙江省绥化市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="organization_type" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    eid = 0
    for p in persons:
        if "待确认" in p["name"]:
            continue  # skip placeholder persons
        eid += 1
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="2" value="县级"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{eid * 50.0}" y="0" z="0"/>')
        lines.append('      </node>')

    for o in organizations:
        eid += 1
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # person→org (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        person_name = next((p["name"] for p in persons if p["id"] == pid), "")
        if "待确认" in person_name:
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    print("=" * 50)
    print("海伦市领导班子关系网络 — 数据构建")
    print("=" * 50)

    build_db()
    print(f"[OK] 数据库: {DB_PATH}")

    build_gexf()
    print(f"[OK] GEXF: {GEXF_PATH}")

    # Stats
    confirmed_persons = [p for p in persons if "待确认" not in p["name"]]
    placeholder_persons = [p for p in persons if "待确认" in p["name"]]
    print(f"\n人员: {len(confirmed_persons)} confirmed, {len(placeholder_persons)} 待确认")
    print(f"机构: {len(organizations)}")
    print(f"任职记录: {len(positions)}")
    print(f"关系: {len(relationships)}")
    print(f"\n⚠ 注意: 由于网络访问限制（Exa rate-limit, 百度安全验证, gov.cn超时），")
    print(f"  多数领导班子成员的姓名和完整履历尚未获取。")
    print(f"  已确认: 市委书记侯绍波、市长刘晓光（来源：海伦市人民政府官网新闻2026年7月）")
    print("=" * 50)

if __name__ == "__main__":
    main()
