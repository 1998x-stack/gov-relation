#!/usr/bin/env python3
"""荆州区领导班子工作关系网络 - 数据构建脚本
湖北省 荆州市 荆州区 —— 区委书记 & 区长 主官网络
数据截至 2026-08-06。
"""

import os
import sys
import sqlite3
from datetime import datetime

SLUG = "荆州区"
REGION = "荆州区"
PARENT_CITY = "荆州市"
PROVINCE = "湖北省"
LEVEL = "市辖区"
TODAY = datetime.now().strftime("%Y-%m-%d")
AS_OF = "2026-08-06"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "荆州区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "荆州区_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# RESEARCH DATA
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # 1 现任区委书记 一把手
    {
        "id": 1,
        "name": "李先刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆州区区委书记",
        "current_org": "中共荆州市荆州区委员会",
        "source": "http://www.jingzhouqu.gov.cn/xwzx/jrtt/202608/t20260802_1125437.shtml",
        "notes": "现任荆州区委书记。2026年换届后接任，主持召开区委常委会会议、'四大家'联席会议。2026-07 走访区人大常委会、区政府、区政协机关。兼任荆州高新区党工委统筹领导。履历详情待查。",
    },
    # 2 现任区长 二把手
    {
        "id": 2,
        "name": "张远重",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "education": "长江大学农村与区域发展专业农业硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆州区区委副书记、区长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/202209/t20220926/28913.shtml",
        "notes": "现任荆州区委副书记、区政府区长、党组书记，主持区政府全面工作，主管审计。",
    },
    {
        "id": 3,
        "name": "万玲玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记（已离任）",
        "current_org": "",
        "source": "http://www.jingzhouqu.gov.cn/xwzx/jrtt/202606/t20260613_1116353.shtml",
        "notes": "前任荆州区委书记兼荆州高新区党工委书记。截至2026-06-12仍以'荆州区委书记、荆州高新区党工委书记'身份带队调研；2026年换届后由李先刚接任。女子部，长期从事信访/民生/高新区工作。去向待查。",
    },
    {
        "id": 4,
        "name": "朱翊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆州区人大常委会主任",
        "current_org": "荆州市荆州区人大常委会",
        "source": "http://www.jingzhouqu.gov.cn/xwzx/jrtt/202606/t20260617_1116967.shtml",
        "notes": "2026-06-16 区人大常委会办公室确认：区人大常委会主任朱翊带队调研公益诉讼检察工作。",
    },
    {
        "id": 5,
        "name": "罗海林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆州区副区长、区公安分局局长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/104220263/t123220263044/689547.shtml",
        "notes": "现任荆州区政府副区长、公安分局党委书记、局长、督察长，三级高级警长。负责公安、信访。",
    },
    {
        "id": 6,
        "name": "靳英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年2月",
        "birthplace": "",
        "education": "长江大学英语专业、农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆州区副区长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/104220253/t130220253044/587186.shtml",
        "notes": "负责人社、民政、退役军人事务、残联等工作。",
    },
    {
        "id": 7,
        "name": "易金红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年10月",
        "birthplace": "",
        "education": "湖北三峡大学物理学、行政管理专业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆州区副区长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/102220243/t126220243024/464156.shtml",
        "notes": "负责文化旅游、文物保护、民族宗教、商务等工作。",
    },
    {
        "id": 8,
        "name": "董欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年1月",
        "birthplace": "",
        "education": "省委党校研究生、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "荆州区副区长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/104220253/t129220253044/586958.shtml",
        "notes": "负责城市建设、自然资源和规划、城管、交通等工作。",
    },
    {
        "id": 9,
        "name": "关勇",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1971年1月",
        "birthplace": "",
        "education": "大学医学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "荆州区副区长",
        "current_org": "荆州市荆州区人民政府",
        "source": "http://zwgk.jingzhouqu.gov.cn/26769/202209/t20220926/28889.shtml",
        "notes": "负责医保、教育、卫健、市场监管、红十字会等工作。",
    },
]

organizations = [
    {"id": 1, "name": "中共荆州市荆州区委员会", "type": "党委", "level": "县处级", "parent": "中共荆州市委员会", "location": "荆州市荆州区"},
    {"id": 2, "name": "荆州市荆州区人民政府", "type": "政府", "level": "县处级", "parent": "荆州市人民政府", "location": "荆州市荆州区"},
    {"id": 3, "name": "荆州市荆州区人大常委会", "type": "人大", "level": "县处级", "parent": "荆州市人民代表大会常务委员会", "location": "荆州市荆州区"},
    {"id": 4, "name": "荆州市荆州区公安分局", "type": "政府", "level": "乡科级", "parent": "荆州市公安局", "location": "荆州市荆州区"},
    {"id": 5, "name": "荆州高新技术产业开发区党工委", "type": "党委", "level": "县处级", "parent": "荆州市委员会", "location": "荆州市"},
]

positions = [
    # 李先刚
    {"person_id": "p1", "org_id": 1, "title": "荆州区区委书记", "start": "2026-07", "end": "present", "rank": "县处级正职",
     "note": "2026年换届后接任，主持区委常委会"},
    # 张远重
    {"person_id": "p2", "org_id": 1, "title": "荆州区区委副书记", "start": "", "end": "present", "rank": "县处级副职",
     "note": "兼区长"},
    {"person_id": "p2", "org_id": 2, "title": "荆州区区长、党组书记", "start": "", "end": "present", "rank": "县处级正职",
     "note": "主持区政府全面工作"},
    # 万玲玲（前任）
    {"person_id": "p3", "org_id": 1, "title": "荆州区区委书记（前任）", "start": "", "end": "2026-06", "rank": "县处级正职",
     "note": "2026换届后由李先刚接任"},
    {"person_id": "p3", "org_id": 5, "title": "荆州高新区党工委书记（前任）", "start": "", "end": "2026-06", "rank": "县处级正职",
     "note": ""},
    # 朱翊
    {"person_id": "p4", "org_id": 3, "title": "荆州区人大常委会主任", "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},
    # 罗海林
    {"person_id": "p5", "org_id": 2, "title": "荆州区副区长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责公安、信访"},
    {"person_id": "p5", "org_id": 4, "title": "区公安分局局长", "start": "", "end": "present", "rank": "乡科级正职",
     "note": "分局党委书记、督察长、三级高级警长"},
    # 靳英
    {"person_id": "p6", "org_id": 2, "title": "荆州区副区长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责人社、民政、退役军人事务"},
    # 易金红
    {"person_id": "p7", "org_id": 2, "title": "荆州区副区长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责文旅、商务"},
    # 董欣
    {"person_id": "p8", "org_id": 2, "title": "荆州区副区长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责城建、规划、城管"},
    # 关勇
    {"person_id": "p9", "org_id": 2, "title": "荆州区副区长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责医保、教育、卫健"},
]

relationships = [
    # 李先刚 ↔ 张远重（党政主官搭档）
    {"person_a": "p1", "person_b": "p2", "type": "overlap", "context": "党政主官搭档（区委书记与区长）",
     "overlap_org": "中共荆州区委/区政府", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 李先刚 ↔ 万玲玲（前后任区委书记）
    {"person_a": "p1", "person_b": "p3", "type": "predecessor_successor", "context": "前后任区委书记（2026换届交接）",
     "overlap_org": "中共荆州区委", "overlap_period": "2026-06/07", "confidence": "confirmed"},
    # 万玲玲 ↔ 张远重（曾任书记与区长搭档）
    {"person_a": "p3", "person_b": "p2", "type": "overlap", "context": "历任区委书记与区长搭档",
     "overlap_org": "中共荆州区委/区政府", "overlap_period": "截至2026-06", "confidence": "confirmed"},
    # 李先刚 ↔ 朱翊（区委书记与人大主任）
    {"person_a": "p1", "person_b": "p4", "type": "superior_subordinate", "context": "区委书记与区人大常委会主任",
     "overlap_org": "中共荆州区委/区人大", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 张远重 ↔ 各副区长（区长与副区长）
    {"person_a": "p2", "person_b": "p5", "type": "superior_subordinate", "context": "区长与副区长兼公安局长",
     "overlap_org": "荆州区人民政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p6", "type": "superior_subordinate", "context": "区长与副区长",
     "overlap_org": "荆州区人民政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p7", "type": "superior_subordinate", "context": "区长与副区长",
     "overlap_org": "荆州区人民政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p8", "type": "superior_subordinate", "context": "区长与副区长",
     "overlap_org": "荆州区人民政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p9", "type": "superior_subordinate", "context": "区长与副区长",
     "overlap_org": "荆州区人民政府", "overlap_period": "present", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color_and_size(post):
    if "区委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "区长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    elif "区委副书记" in post:
        return ("150,50,50", 15.0)
    elif "常委" in post and ("组织" in post or "政法" in post):
        return ("100,150,255", 12.0)
    elif "人大" in post:
        return ("200,255,255", 12.0)
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


def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    # ── SQLite ────────────────────────────────────────────────────────────
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

    if cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0] > 0:
        cur.execute("DELETE FROM persons")
        cur.execute("DELETE FROM organizations")
        cur.execute("DELETE FROM positions")
        cur.execute("DELETE FROM relationships")
        conn.commit()

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

    # ── GEXF ──────────────────────────────────────────────────────────────
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子和工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

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

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pidv = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pidv}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    print(f"\n{'='*60}")
    print(f"{SLUG} Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()