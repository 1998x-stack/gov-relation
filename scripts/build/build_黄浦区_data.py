#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 黄浦区, Shanghai."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/shanghai_黄浦区")
DB_PATH = os.path.join(TMP, "黄浦区_network.db")
GEXF_PATH = os.path.join(TMP, "黄浦区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "徐惠丽", "gender": "女", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "上海", "education": "大学/公共管理硕士",
     "party_join": "中共党员", "work_start": "1995-07",
     "current_post": "上海市黄浦区委书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 2, "name": "沈山州", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-05", "birthplace": "上海", "education": "在职研究生/经济学博士",
     "party_join": "中共党员", "work_start": "1992-07",
     "current_post": "上海市黄浦区委副书记、区长", "current_org": "上海市黄浦区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},

    # ── Previous Leaders ──
    {"id": 3, "name": "杲云", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-12", "birthplace": "江苏江都", "education": "工学博士/研究员",
     "party_join": "1990-06", "work_start": "1991-08",
     "current_post": "上海市人大常委会副主任（原黄浦区委书记）", "current_org": "上海市人大常委会",
     "source": "https://baike.baidu.com/item/%E6%9D%B2%E4%BA%91"},

    # ── Standing Committee Members (current) ──
    {"id": 4, "name": "李忠兴", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "上海", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委副书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 5, "name": "洪继梁", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-01", "birthplace": "上海", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、副区长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 6, "name": "白爱军", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、区纪委书记、区监委主任", "current_org": "中共上海市黄浦区纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 7, "name": "王玉峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、组织部部长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 8, "name": "林竞君", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、政法委书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 9, "name": "徐知", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、宣传部部长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 10, "name": "卢正", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、统战部部长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},

    # ── Deputy District Leaders ──
    {"id": 11, "name": "徐知", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委宣传部部长（兼任）", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},

    # ── District Government Deputy Heads ──
    {"id": 12, "name": "徐知", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区副区长", "current_org": "上海市黄浦区人民政府",
     "source": "https://www.huangpuqu.sh.cn"},
]

# Deduplicate - person IDs must be unique, remove duplicates
# Note: 徐知 appears multiple times in my draft - keep only the first entry per unique combination
persons = [
    {"id": 1, "name": "徐惠丽", "gender": "女", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "上海", "education": "大学/公共管理硕士",
     "party_join": "中共党员", "work_start": "1995-07",
     "current_post": "上海市黄浦区委书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 2, "name": "沈山州", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-05", "birthplace": "上海", "education": "在职研究生/经济学博士",
     "party_join": "中共党员", "work_start": "1992-07",
     "current_post": "上海市黄浦区委副书记、区长", "current_org": "上海市黄浦区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 3, "name": "杲云", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-12", "birthplace": "江苏江都", "education": "工学博士/研究员",
     "party_join": "1990-06", "work_start": "1991-08",
     "current_post": "上海市人大常委会副主任（原黄浦区委书记）", "current_org": "上海市人大常委会",
     "source": "https://baike.baidu.com/item/%E6%9D%B2%E4%BA%91"},
    {"id": 4, "name": "李忠兴", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "上海", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委副书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 5, "name": "洪继梁", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-01", "birthplace": "上海", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、副区长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 6, "name": "白爱军", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、区纪委书记、区监委主任", "current_org": "中共上海市黄浦区纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 7, "name": "王玉峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、组织部部长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 8, "name": "林竞君", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、政法委书记", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
    {"id": 9, "name": "卢正", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "黄浦区委常委、统战部部长", "current_org": "中共上海市黄浦区委员会",
     "source": "https://zh.wikipedia.org/wiki/%E9%BB%84%E6%B5%A6%E5%8C%BA"},
]

organizations = [
    {"id": 1, "name": "中共上海市黄浦区委员会", "type": "党委", "level": "地厅级（副省级城市）",
     "parent": "中共上海市委员会", "location": "上海市黄浦区"},
    {"id": 2, "name": "上海市黄浦区人民政府", "type": "政府", "level": "地厅级（副省级城市）",
     "parent": "上海市人民政府", "location": "上海市黄浦区"},
    {"id": 3, "name": "上海市黄浦区纪律检查委员会", "type": "党委", "level": "地厅级（副省级城市）",
     "parent": "中共上海市纪律检查委员会", "location": "上海市黄浦区"},
    {"id": 4, "name": "上海市人大常委会", "type": "人大", "level": "省级",
     "parent": "上海市", "location": "上海市黄浦区"},
]

positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "上海市黄浦区委书记", "start": "2025-", "end": "", "rank": "正局级", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "上海市黄浦区委副书记、区长", "start": "2021-", "end": "", "rank": "正局级", "note": "现任"},

    # Previous leaders
    {"person_id": 3, "org_id": 1, "title": "上海市黄浦区委书记", "start": "2019-", "end": "2025-", "rank": "正局级", "note": "前任"},
    {"person_id": 3, "org_id": 4, "title": "上海市人大常委会副主任", "start": "2025-", "end": "", "rank": "副省级", "note": "现任"},

    # Standing committee members
    {"person_id": 4, "org_id": 1, "title": "黄浦区委副书记", "start": "", "end": "", "rank": "副局级", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "黄浦区委常委、副区长", "start": "", "end": "", "rank": "副局级", "note": "现任"},
    {"person_id": 6, "org_id": 3, "title": "黄浦区委常委、区纪委书记、区监委主任", "start": "", "end": "", "rank": "副局级", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "黄浦区委常委、组织部部长", "start": "", "end": "", "rank": "副局级", "note": "现任"},
    {"person_id": 8, "org_id": 1, "title": "黄浦区委常委、政法委书记", "start": "", "end": "", "rank": "副局级", "note": "现任"},
    {"person_id": 9, "org_id": 1, "title": "黄浦区委常委、统战部部长", "start": "", "end": "", "rank": "副局级", "note": "现任"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "黄浦区委书记与区长党政领导班子搭档",
     "overlap_org": "中共上海市黄浦区委员会/上海市黄浦区人民政府", "overlap_period": "2025-至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "杲云卸任黄浦区委书记后由徐惠丽接任",
     "overlap_org": "中共上海市黄浦区委员会", "overlap_period": "2025-", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "党政搭档", "context": "沈山州任区长期间与区委书记杲云搭档",
     "overlap_org": "中共上海市黄浦区委员会/上海市黄浦区人民政府", "overlap_period": "2021-2025", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与区委副书记",
     "overlap_org": "中共上海市黄浦区委员会", "overlap_period": "2025-至今", "strength": "weak", "confidence": "plausible"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长与常务副区长",
     "overlap_org": "上海市黄浦区人民政府", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长与区委副书记共同配合",
     "overlap_org": "中共上海市黄浦区委员会", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
]

# ── SQLite Database ─────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                   p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT INTO organizations (id, name, type, level, parent, location)
                     VALUES (?,?,?,?,?,?)""",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
                     VALUES (?,?,?,?,?,?,?)""",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")


# ── GEXF Graph ──────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post:
        return "255,50,50"  # Red for party secretary
    if "区长" in post:
        return "50,100,255"  # Blue for government head
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"  # Orange for discipline
    return "100,100,100"  # Grey for others

def person_size(post):
    if "书记" in post and "副" not in post:
        return "20.0"
    if "区长" in post and "副" not in post:
        return "20.0"
    return "12.0"

def org_color(org_type):
    m = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
         "乡镇/街道": "255,255,200", "事业单位": "220,220,220", "群团": "255,220,255",
         "人大": "200,255,255", "政协": "255,240,200"}
    return m.get(org_type, "200,200,200")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>上海市黄浦区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="gender" type="string"/>')
    lines.append('      <attribute id="5" title="source" type="string"/>')
    lines.append('      <attribute id="6" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = person_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="6" value="{esc(o["type"])}"/>')
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
        w = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
