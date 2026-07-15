#!/usr/bin/env python3
"""Build Jin'an District (金安区) leadership network database and GEXF graph.

Targets: 区委书记王红, 区长刘美胜
Research date: 2026-07-15
Sources:
  - www.ja.gov.cn (official district government website, accessed 2026-07-15)
  - 领导之窗 page: https://www.ja.gov.cn/xxgk/ldzc/ (领导人简历)
  - News articles from 金安发布 (various dates June-July 2026)
  - 金安区项目谋划推进会 (2026-07-08)
  - 金安区招商引资调度会 (2026-07-06)
  - 7月份区重点工作推进会 (2026-07-02)

Confidence: Current roles confirmed from official government website and news.
  王红 confirmed as 区委书记 through multiple official meeting reports (2026-07).
  刘美胜 confirmed as 区委副书记、区长 from official 领导之窗 page (2026-07).
  Biographical details for 刘美胜 from official page.
  Biographical details for 王红 limited due to restricted web search.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "金安区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "金安区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "王红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共六安市金安区委员会",
        "source": "https://www.ja.gov.cn/zxzx/jayw/26564424.html (金安要闻 2026-07-10, 王红主持召开项目谋划推进会); https://www.ja.gov.cn/zxzx/tpxw/26558502.html (图片新闻 2026-07-02, 主持区重点工作推进会)",
        "notes": "王红，现任中共六安市金安区委书记。主持区委全面工作。频繁调研项目谋划、招商引资、重点工作推进等。据公开报道，金安区换届工作已于2026年6月完成。完整履历待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "刘美胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "安徽宣城",
        "native_place": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "金安区人民政府",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗 区长信息, accessed 2026-07-15); https://www.ja.gov.cn/zxzx/jayw/26564424.html (2026-07-10, 出席项目谋划推进会); https://www.ja.gov.cn/zxzx/tpxw/26561463.html (2026-07-06, 招商引资调度会部署工作)",
        "notes": "刘美胜，男，汉族，1981年2月出生，安徽宣城人，大学学历，中共党员。现任金安区委副书记、区长。领导区政府全面工作，负责审计工作，分管审计局。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "洪飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "金安区人民政府",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗, accessed 2026-07-15); https://www.ja.gov.cn/zxzx/jayw/26564424.html (2026-07-10, 出席项目谋划推进会)",
        "notes": "洪飞，区委常委、区政府党组副书记、常务副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "江利平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "金安区人民政府",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗, accessed 2026-07-15); https://www.ja.gov.cn/zxzx/jayw/26564424.html (2026-07-10, 出席项目谋划推进会)",
        "notes": "江利平，区委常委、区政府副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "胡卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "金安区人大常委会",
        "source": "https://www.ja.gov.cn/zxzx/tpxw/26561463.html (2026-07-06, 出席招商引资调度会)",
        "notes": "胡卫东，区人大常委会主任。参加招商引资调度会等全区性会议。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "荣维聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "金安区政协",
        "source": "https://www.ja.gov.cn/zxzx/tpxw/26561463.html (2026-07-06, 出席招商引资调度会)",
        "notes": "荣维聪，区政协主席。参加招商引资调度会等全区性会议。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "罗伟伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（专职）",
        "current_org": "中共六安市金安区委员会",
        "source": "https://www.ja.gov.cn/zxzx/tpxw/26561463.html (2026-07-06, 出席招商引资调度会)",
        "notes": "罗伟伟，区委副书记（专职）。参加招商引资调度会等全区性会议。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "杨君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共六安市金安区委员会",
        "source": "https://www.ja.gov.cn/zxzx/tpxw/26561463.html (2026-07-06, 出席招商引资调度会)",
        "notes": "杨君，区委常委。出席招商引资调度会。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "李瑞杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共六安市金安区委员会",
        "source": "https://www.ja.gov.cn/zxzx/jayw/26564424.html (2026-07-10, 出席项目谋划推进会)",
        "notes": "李瑞杰，区委常委。出席项目谋划推进会。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "张运",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金安区人民政府",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗, accessed 2026-07-15)",
        "notes": "张运，副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "王建松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "六安市公安局金安分局",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗, accessed 2026-07-15)",
        "notes": "王建松，副区长、六安市公安局金安分局党委书记、局长。",
        "confidence": "confirmed"
    },
    {
        "id": 12,
        "name": "方正",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金安区人民政府",
        "source": "https://www.ja.gov.cn/xxgk/ldzc/ (领导之窗, accessed 2026-07-15)",
        "notes": "方正，副区长。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共六安市金安区委员会", "type": "党委", "level": "县处级", "parent": "中共六安市委", "location": "六安市金安区"},
    {"id": 2, "name": "金安区人民政府", "type": "政府", "level": "县处级", "parent": "六安市人民政府", "location": "六安市金安区"},
    {"id": 3, "name": "金安区人大常委会", "type": "人大", "level": "县处级", "parent": "六安市人大常委会", "location": "六安市金安区"},
    {"id": 4, "name": "金安区政协", "type": "政协", "level": "县处级", "parent": "六安市政协", "location": "六安市金安区"},
    {"id": 5, "name": "六安市公安局金安分局", "type": "政府", "level": "乡科级", "parent": "金安区人民政府", "location": "六安市金安区"},
]

positions = [
    # 王红 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 刘美胜 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "未知", "end": "present", "rank": "正处级", "note": "领导区政府全面工作，负责审计工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    # 洪飞 - 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "区委常委、区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 江利平 - 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "区委常委、副区长"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 胡卫东 - 人大主任
    {"person_id": 5, "org_id": 3, "title": "主任", "start": "未知", "end": "present", "rank": "正处级", "note": "区人大常委会主任"},
    # 荣维聪 - 政协主席
    {"person_id": 6, "org_id": 4, "title": "主席", "start": "未知", "end": "present", "rank": "正处级", "note": "区政协主席"},
    # 罗伟伟 - 专职副书记
    {"person_id": 7, "org_id": 1, "title": "区委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 杨君 - 区委常委
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 李瑞杰 - 区委常委
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 张运 - 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    # 王建松 - 副区长兼公安局长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "党委书记、局长", "start": "未知", "end": "present", "rank": "乡科级", "note": "六安市公安局金安分局"},
    # 方正 - 副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    {
        "person_a": "王红",
        "person_b": "刘美胜",
        "type": "superior_subordinate",
        "context": "区委书记与区长搭档，共同主持全区工作",
        "overlap_org": "中共六安市金安区委员会/金安区人民政府",
        "overlap_period": "current",
        "confidence": "confirmed"
    },
    {
        "person_a": "王红",
        "person_b": "洪飞",
        "type": "superior_subordinate",
        "context": "区委书记与常务副区长",
        "overlap_org": "金安区",
        "overlap_period": "current",
        "confidence": "confirmed"
    },
    {
        "person_a": "王红",
        "person_b": "罗伟伟",
        "type": "superior_subordinate",
        "context": "区委书记与专职副书记",
        "overlap_org": "中共六安市金安区委员会",
        "overlap_period": "current",
        "confidence": "confirmed"
    },
    {
        "person_a": "刘美胜",
        "person_b": "洪飞",
        "type": "superior_subordinate",
        "context": "区长与常务副区长",
        "overlap_org": "金安区人民政府",
        "overlap_period": "current",
        "confidence": "confirmed"
    },
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b string for a person based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "区委书记" in post:
        return "255,50,50"  # Red — Party Secretary
    elif "区长" in post or "副区长" in post or "常务副" in post:
        return "50,100,255"  # Blue — Government leaders
    elif "人大" in post:
        return "200,255,255"  # Cyan
    elif "政协" in post:
        return "255,240,200"  # Cream
    else:
        return "100,100,100"  # Grey


def org_color(o):
    """Return r,g,b string for an organization based on type."""
    t = o.get("type", "")
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(t, "200,200,200")


def is_top_leader(p):
    """Return True if the person is a top leader (区委书记 or 区长)."""
    post = p.get("current_post", "")
    return "区委书记" in post or ("区长" in post and "副" not in post and "常务" not in post)


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


def build_database():
    """Create SQLite database and write GEXF graph."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
              p.get("birthplace", ""), p.get("native_place", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""), p["current_post"], p["current_org"], p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o.get("level", ""), o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


def build_gexf():
    """Write GEXF graph using string formatting (not ElementTree)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>金安区（六安市）领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes — organizations
    lines.append('    <nodes>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges — person -> organization worked_at
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges — person <-> person relationships
    for r in relationships:
        p_a = next((p for p in persons if p["name"] == r["person_a"]), None)
        p_b = next((p for p in persons if p["name"] == r["person_b"]), None)
        if p_a and p_b:
            eid += 1
            rel_type = r["type"]
            lines.append(f'      <edge id="e{eid}" source="p{p_a["id"]}" target="p{p_b["id"]}" label="{esc(rel_type)}" weight="2.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="relationship"/>')
            lines.append(f'          <attvalue for="1" value="{esc(rel_type)}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("Done.")
