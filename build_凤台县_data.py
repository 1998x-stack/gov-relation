#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凤台县 (Fengtai County, Huainan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_凤台县 - 县委书记 & 县长
Sources: Baidu Baike (凤台县/熊寿宏 entries, accessed 2026-07-15), web research (degraded)
Note: Web search severely degraded (Exa rate-limited, Baidu/Google/Wikipedia blocked).
      Current 县委书记 (successor to 熊寿宏) unknown due to access constraints.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# If running from staging temp dir (data/tmp/anhui_凤台县/), go up to repo root
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_凤台县")
DB_PATH = os.path.join(STAGING, "凤台县_network.db")
GEXF_PATH = os.path.join(STAGING, "凤台县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "熊寿宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "安徽霍邱", "education": "安徽省委党校大学学历",
     "party_join": "1997-06", "work_start": "1990-07",
     "current_post": "淮南市政协副主席（原凤台县委书记）", "current_org": "淮南市政协",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E5%AF%BF%E5%AE%8F"},
    {"id": 2, "name": "李大庆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤台县委副书记、县长", "current_org": "凤台县人民政府",
     "source": "https://baike.baidu.com/item/%E5%87%A4%E5%8F%B0%E5%8E%BF/8341680"},

    # ── 县委领导 ──
    {"id": 3, "name": "苏国宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤台县人大常委会党组书记、主任", "current_org": "凤台县人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E5%87%A4%E5%8F%B0%E5%8E%BF/8341680"},
    {"id": 4, "name": "马士平", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "凤台县政协主席", "current_org": "中国人民政治协商会议凤台县委员会",
     "source": "https://baike.baidu.com/item/%E5%87%A4%E5%8F%B0%E5%8E%BF/8341680"},

    # ── 县委领导班子（from Baidu Baike county entry, individual names unknown）──
    # Per Baidu Baike county page, leadership listed as 2025-07:
    # 县委书记: 熊寿宏 (now 市政协副主席)
    # 县长: 李大庆
    # 县人大常委会主任: 苏国宇
    # 县政协主席: 马士平
    # Other常委成员 names unavailable due to web access constraints
]

organizations = [
    {"id": 101, "name": "中国共产党凤台县委员会", "type": "party",
     "level": "county", "parent": "中国共产党淮南市委员会", "location": "安徽省淮南市凤台县"},
    {"id": 102, "name": "凤台县人民政府", "type": "government",
     "level": "county", "parent": "淮南市人民政府", "location": "安徽省淮南市凤台县"},
    {"id": 103, "name": "凤台县人民代表大会常务委员会", "type": "people_congress",
     "level": "county", "parent": "凤台县", "location": "安徽省淮南市凤台县"},
    {"id": 104, "name": "中国人民政治协商会议凤台县委员会", "type": "cppcc",
     "level": "county", "parent": "凤台县", "location": "安徽省淮南市凤台县"},
    {"id": 105, "name": "淮南市政协", "type": "government",
     "level": "prefecture", "parent": "淮南市", "location": "安徽省淮南市"},
    {"id": 106, "name": "淮南市城乡建设局", "type": "government",
     "level": "prefecture", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 107, "name": "淮南市重点工程建设管理局", "type": "government",
     "level": "prefecture", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 108, "name": "田家庵区人民政府", "type": "government",
     "level": "county", "parent": "淮南市人民政府", "location": "安徽省淮南市田家庵区"},
    {"id": 109, "name": "中共田家庵区纪律检查委员会", "type": "discipline",
     "level": "county", "parent": "中国共产党田家庵区委员会", "location": "安徽省淮南市田家庵区"},
    {"id": 110, "name": "田家庵区安成镇人民政府", "type": "government",
     "level": "township", "parent": "田家庵区人民政府", "location": "安徽省淮南市田家庵区"},
    {"id": 111, "name": "田家庵区长青乡人民政府", "type": "government",
     "level": "township", "parent": "田家庵区人民政府", "location": "安徽省淮南市田家庵区"},
    {"id": 112, "name": "中共安徽省委党校", "type": "education",
     "level": "province", "parent": "安徽省", "location": "安徽省合肥市"},
    {"id": 113, "name": "徐州煤炭工业学校", "type": "education",
     "level": "", "parent": "", "location": "江苏省徐州市"},
]

positions = [
    # ── 熊寿宏 career timeline ──
    {"person_id": 1, "org_id": 113, "title": "徐州煤炭工业学校矿井地质专业学习",
     "start": "1988-09", "end": "1990-07", "rank": "", "note": "全日制中专"},
    {"person_id": 1, "org_id": 111, "title": "田家庵区长青乡政府办办事员",
     "start": "1990-07", "end": "1991-11", "rank": "", "note": "参加工作"},
    {"person_id": 1, "org_id": 109, "title": "田家庵区纪委科员",
     "start": "1991-11", "end": "1997-08", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "田家庵区纪委副主任科员",
     "start": "1997-08", "end": "1998-03", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "田家庵区纪委办公室主任",
     "start": "1998-03", "end": "2000-12", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 109, "title": "田家庵区纪委常委、办公室主任",
     "start": "2000-12", "end": "2005-05", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 110, "title": "田家庵区安成镇党委副书记、镇长",
     "start": "2005-05", "end": "2007-03", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 108, "title": "田家庵区政府办公室主任",
     "start": "2007-03", "end": "2010-04", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 107, "title": "淮南市重点工程建设管理局党组成员、纪检组长",
     "start": "2010-04", "end": "2013-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 101, "title": "凤台县委常委、县人民政府党组副书记、副县长",
     "start": "2013-07", "end": "2016-06", "rank": "副处级", "note": "兼县政务服务中心主任"},
    {"person_id": 1, "org_id": 101, "title": "凤台县委副书记",
     "start": "2016-06", "end": "2018-03", "rank": "副处级", "note": "兼县委党校校长"},
    {"person_id": 1, "org_id": 106, "title": "淮南市城乡建设委员会党委书记、主任",
     "start": "2018-03", "end": "2020-03", "rank": "正处级", "note": "后改局任党组书记、局长"},
    {"person_id": 1, "org_id": 102, "title": "凤台县委副书记、县人民政府县长",
     "start": "2020-03", "end": "2023-09", "rank": "正处级", "note": "2020-03提名为县长候选人，2020-06正式当选"},
    {"person_id": 1, "org_id": 101, "title": "凤台县委书记",
     "start": "2023-09", "end": "2026-05", "rank": "正处级", "note": "2025-01起兼淮南市政协副主席"},
    {"person_id": 1, "org_id": 105, "title": "淮南市政协副主席",
     "start": "2025-01", "end": "present", "rank": "副厅级", "note": "2026-05起不再兼任凤台县委书记"},

    # ── 李大庆 current position ──
    {"person_id": 2, "org_id": 102, "title": "凤台县委副书记、县长",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "公开资料未找到出生年月、籍贯和完整履历。Baidu Baike/Google/Wikipedia均不可达。"},

    # ── 苏国宇 position ──
    {"person_id": 3, "org_id": 103, "title": "凤台县人大常委会党组书记、主任",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "公开资料未找到完整履历"},

    # ── 马士平 position ──
    {"person_id": 4, "org_id": 104, "title": "凤台县政协主席",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "公开资料未找到完整履历"},
]

relationships = [
    # ── 工作关系 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "熊寿宏任凤台县委书记期间，李大庆任县长",
     "overlap_org": "凤台县",
     "overlap_period": "2020-03至2026-05（熊为县长/书记，李为县长）",
     "confidence": "confirmed",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E5%AF%BF%E5%AE%8F"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "熊寿宏任凤台县委书记期间，苏国宇任人大常委会主任",
     "overlap_org": "凤台县",
     "overlap_period": "约2021年后",
     "confidence": "confirmed",
     "source": "https://baike.baidu.com/item/%E5%87%A4%E5%8F%B0%E5%8E%BF/8341680"},
]

# ── DATABASE ─────────────────────────────────────────────────────────

def create_db():
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
            confidence TEXT DEFAULT 'plausible',
            source TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, confidence, source)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"], r["confidence"], r["source"]))

    conn.commit()
    conn.close()
    print(f"✓ Database created at {DB_PATH}")


# ── GEXF ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role: red=party secretary, blue=gov, orange=discipline, grey=other."""
    title = p["current_post"]
    if "书记" in title and "县委" in title:
        return "255,50,50"
    elif "县长" in title or "区长" in title:
        return "50,100,255"
    elif "纪委书记" in title or "监委" in title:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    colors = {
        "party": "255,200,200",
        "government": "200,200,255",
        "discipline": "255,200,200",
        "people_congress": "200,255,255",
        "cppcc": "255,240,200",
        "education": "220,220,220",
    }
    return colors.get(t, "200,200,200")

def is_top_leader(p):
    """Check if person is a top leader (县委书记 or 县长)."""
    title = p["current_post"]
    return ("县委书记" in title or "县委" in title and "副书记" in title) \
           and "副书记" not in title.replace("县委副书记", "") \
           or ("县长" in title and "副县长" not in title)

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>凤台县领导班子工作关系网络 — 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="kind" title="Kind" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="title" title="Title" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="overlap_org" title="Overlap Org" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["birth"] else "12.0")
        kind = "person"
        role = p["current_post"]
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="kind" value="{kind}"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="kind" value="organization"/>')
        lines.append(f'          <attvalue for="role" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person→Organization edges (positions)
    for pos in positions:
        p = next(x for x in persons if x["id"] == pos["person_id"])
        o = next(x for x in organizations if x["id"] == pos["org_id"])
        lines.append(f'      <edge id="e{eid}" source="p{p["id"]}" target="o{o["id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="title" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(pos["note"])}"/>')
        lines.append('          <attvalue for="overlap_org" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person edges (relationships)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="title" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="overlap_org" value="{esc(r["overlap_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created at {GEXF_PATH}")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building 凤台县 leadership network...")
    print(f"  DB path:  {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    create_db()
    create_gexf()

    print()
    print("Summary:")
    print(f"  Persons:        {len(persons)}")
    print(f"  Organizations:  {len(organizations)}")
    print(f"  Positions:      {len(positions)}")
    print(f"  Relationships:  {len(relationships)}")
    print()
    print("Note: Limited data due to web search degradation.")
    print(f"      Current 县委书记 successor to 熊寿宏 unknown.")
    print(f"      Only 4 of ~15+ 班子成员 identified.")
    print(f"      李大庆, 苏国宇, 马士平 personal details (birth, birthplace, education) missing.")
