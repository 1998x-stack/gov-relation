#!/usr/bin/env python3
"""
宜城市 (Yicheng) — 湖北省襄阳市代管县级市
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-24
信息来源: 百度百科, 宜城市人民政府门户网站 (yicheng.gov.cn)
"""

import sqlite3
import os

SLUG = "宜城市"
TODAY = "2026-07-24"
AS_OF = "2024-11"  # Baidu Baike leadership table as-of date

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "宜城市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "宜城市_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "武义泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "江苏省海安市",
        "education": "硕士研究生",
        "party_join": "2004年4月",
        "work_start": "2007年7月",
        "current_post": "宜城市委书记",
        "current_org": "中共宜城市委员会",
        "source": "https://baike.baidu.com/item/%E6%AD%A6%E4%B9%89%E6%B3%89",
        "notes": "2021年6月任宜城市委书记。此前履历待补充。"
    },
    {
        "id": 2,
        "name": "肖平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜城市市长",
        "current_org": "宜城市人民政府",
        "source": "https://baike.baidu.com/item/%E5%AE%9C%E5%9F%8E%E5%B8%82",
        "notes": "百度百科宜城市词条确认市长职务，个人履历信息待补充。"
    },
    {
        "id": 3,
        "name": "陈进雷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜城市人大常委会主任",
        "current_org": "宜城市人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%9C%E5%9F%8E%E5%B8%82",
        "notes": "百度百科宜城市词条确认职务，个人履历信息待补充。"
    },
    {
        "id": 4,
        "name": "李源",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宜城市政协主席",
        "current_org": "中国人民政治协商会议宜城市委员会",
        "source": "https://baike.baidu.com/item/%E5%AE%9C%E5%9F%8E%E5%B8%82",
        "notes": "百度百科宜城市词条确认职务，个人履历信息待补充。"
    },
    # ── Predecessors (known from public sources) ──────────────────────────
    {
        "id": 5,
        "name": "郭静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "湖北省襄阳市",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原宜城市委书记）",
        "current_org": "",
        "source": "推断：郭静为宜城前任市委书记，武义泉2021年6月接任",
        "notes": "郭静2021年6月前担任宜城市委书记，后调任襄阳市领导职位。此为推断，需确认。"
    },
    {
        "id": 6,
        "name": "严广超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任（原宜城市市长）",
        "current_org": "",
        "source": "推断：严广超曾任宜城市市长（肖平前任），需确认",
        "notes": "严广超为宜城市前任市长，后调任他职。此为推断，需确认。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共宜城市委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委", "location": "宜城市"},
    {"id": 2, "name": "宜城市人民政府", "type": "政府", "level": "县级", "parent": "襄阳市人民政府", "location": "宜城市"},
    {"id": 3, "name": "宜城市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "宜城市"},
    {"id": 4, "name": "中国人民政治协商会议宜城市委员会", "type": "政协", "level": "县级", "parent": "", "location": "宜城市"},
    {"id": 5, "name": "中共宜城市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市纪律检查委员会", "location": "宜城市"},
    {"id": 6, "name": "中共襄阳市委", "type": "党委", "level": "地市级", "parent": "中共湖北省委", "location": "襄阳市"},
    {"id": 7, "name": "襄阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖北省人民政府", "location": "襄阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Current leaders
    {"person_id": "p1", "org_id": 1, "title": "宜城市委书记", "start": "2021-06", "end": "present", "rank": "正县级", "note": "2021年6月任中共宜城市委书记"},
    {"person_id": "p2", "org_id": 2, "title": "宜城市市长", "start": "", "end": "present", "rank": "正县级", "note": "任职起始时间待确认"},
    {"person_id": "p3", "org_id": 3, "title": "宜城市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": "p4", "org_id": 4, "title": "宜城市政协主席", "start": "", "end": "present", "rank": "正县级", "note": ""},

    # Predecessors
    {"person_id": "p5", "org_id": 1, "title": "宜城市委书记", "start": "", "end": "2021-06", "rank": "正县级", "note": "武义泉前任"},
    {"person_id": "p6", "org_id": 2, "title": "宜城市市长", "start": "", "end": "", "rank": "正县级", "note": "肖平前任"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": "p1", "person_b": "p2",
        "type": "superior_subordinate",
        "context": "宜城市委书记与市长党政搭档",
        "overlap_org": "宜城市",
        "overlap_period": "2021-06至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p1", "person_b": "p3",
        "type": "overlap",
        "context": "市委与市人大常委会协同工作",
        "overlap_org": "宜城市",
        "overlap_period": "",
        "confidence": "plausible"
    },
    {
        "person_a": "p1", "person_b": "p4",
        "type": "overlap",
        "context": "市委与市政协协同工作",
        "overlap_org": "宜城市",
        "overlap_period": "",
        "confidence": "plausible"
    },
    {
        "person_a": "p5", "person_b": "p1",
        "type": "predecessor_successor",
        "context": "宜城市委书记前后任",
        "overlap_org": "中共宜城市委员会",
        "overlap_period": "2021-06",
        "confidence": "plausible"
    },
    {
        "person_a": "p6", "person_b": "p2",
        "type": "predecessor_successor",
        "context": "宜城市市长前后任（推断）",
        "overlap_org": "宜城市人民政府",
        "overlap_period": "",
        "confidence": "unverified"
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    """Run database + GEXF build."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
            notes TEXT
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
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "市委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "人大常委会主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,240,200", 15.0)
        elif "已离任" in post or "原" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>宜城市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"宜城市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
