#!/usr/bin/env python3
"""
Build 龙南市 (Longnan City — county-level city under 赣州市, 江西省)
government personnel network database and GEXF graph.

龙南市 is a county-level city under 赣州市, 江西省.
Current leadership as of 2026-07-15:
- 边建忠: 龙南市委书记、龙南经开区党工委书记 (appointed July 2026, from 全南县委书记)
- 刘耿: 龙南市委副书记、市长候选人, 经开区党工委副书记、管委会主任提名人选 (appointed July 2026)
- 彭江闽: 龙南市委副书记、市长 (previous term, being replaced)
- 钟旭辉: 前任龙南市委书记 (~2021-2026, departed ~July 2026)

Based on official sources from www.jxln.gov.cn news pages and existing repository data.
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
else:
    REPO_ROOT = BASE

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "data/database/龙南市_network.db"
GEXF_REL = "data/graph/龙南市_network.gexf"

DB_PATH = os.path.join(REPO_ROOT, DB_REL)
GEXF_PATH = os.path.join(REPO_ROOT, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "边建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "江西峡江",
        "education": "华东政法大学",
        "party_join": "中共党员（2001-04入党）",
        "work_start": "1997-08",
        "current_post": "龙南市委书记、龙南经开区党工委书记",
        "current_org": "中共龙南市委员会",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—2026年7月3日以市委书记身份深入重点工业企业走访调研；7月4日'四不两直'深入乡镇督导调研；7月6日走访市委办等市委部门；7月7日任龙南市人武部党委第一书记；7月9日讲授树立和践行正确政绩观学习教育专题党课；百度百科—边建忠，1978年7月生，江西峡江人，华东政法大学，1997年8月参加工作",
    },
    {
        "id": 2,
        "name": "刘耿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委副书记、市长候选人",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—2026年7月3日以龙南市委副书记、市长候选人，经开区党工委副书记、管委会主任提名人选身份深入重点工业企业走访调研",
    },
    {
        "id": 3,
        "name": "彭江闽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "江西赣州",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委副书记、市长（前任）",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目仍列出彭江闽为龙南市委副书记、市长，经开区党工委副书记、管委会主任（2026年7月尚在过渡期）",
    },
    {
        "id": 4,
        "name": "钟旭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "江西赣州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委书记（前任）",
        "current_org": "中共龙南市委员会",
        "source": "build_ganzhou_remaining_data.py（旧数据库记录）—钟旭辉1968年11月生，龙南市委书记至~2026年6月/7月，去向待查",
    },
    # ---- 市委常委 ----
    {
        "id": 5,
        "name": "朱振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出朱振为政府领导班子成员",
    },
    {
        "id": 6,
        "name": "陈哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出陈哲为政府领导班子成员",
    },
    {
        "id": 7,
        "name": "聂志通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出聂志通为政府领导班子成员",
    },
    {
        "id": 8,
        "name": "曾腾云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出曾腾云为政府领导班子成员",
    },
    {
        "id": 9,
        "name": "曾祖腾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出曾祖腾为政府领导班子成员",
    },
    {
        "id": 10,
        "name": "何晓珍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出何晓珍为政府领导班子成员",
    },
    {
        "id": 11,
        "name": "杨春景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出杨春景为政府领导班子成员",
    },
    {
        "id": 12,
        "name": "徐丽芸",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "龙南市委常委、副市长",
        "current_org": "龙南市人民政府",
        "source": "龙南市人民政府网(www.jxln.gov.cn)—领导信息栏目列出徐丽芸为政府领导班子成员",
    },
]

organizations = [
    {"id": 1, "name": "中共龙南市委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州龙南"},
    {"id": 2, "name": "龙南市人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州龙南"},
    {"id": 3, "name": "龙南经济技术开发区", "type": "开发区", "level": "国家级经开区", "parent": "赣州市人民政府", "location": "江西赣州龙南"},
]

positions = [
    # 边建忠 — 龙南市委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "龙南市委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "2026年7月初由全南县委书记调任龙南市委书记。7月7日任龙南市人武部党委第一书记。7月3日走访重点企业，7月4日四不两直督导乡镇，7月9日讲授专题党课。"},
    {"id": 2, "person_id": 1, "org_id": 3, "title": "龙南经开区党工委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "兼任龙南经开区党工委书记。"},
    # 边建忠 — 全南时期（前任）
    {"id": 3, "person_id": 1, "org_id": 4, "title": "全南县委书记（前任）", "start": "2025", "end": "2026-07", "rank": "县处级正职", "note": "由县长升任县委书记。2026年6月9日主持政绩观学习教育整改整治推进会。6月29日主持庆祝建党105周年大会。2026年7月初调离。"},
    {"id": 4, "person_id": 1, "org_id": 5, "title": "全南县长（前任）", "start": "2021", "end": "2025", "rank": "县处级正职", "note": "2021年任全南县长。2023-2025年连续以县长身份作政府工作报告。"},
    # 刘耿 — 市长候选人
    {"id": 5, "person_id": 2, "org_id": 2, "title": "龙南市委副书记、市长候选人", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "2026年7月3日以市委副书记、市长候选人，经开区党工委副书记、管委会主任提名人选身份走访重点企业。7月3日与边建忠一同调研。"},
    {"id": 6, "person_id": 2, "org_id": 3, "title": "龙南经开区党工委副书记、管委会主任提名人选", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "兼任经开区职务。"},
    # 彭江闽 — 前任市长
    {"id": 7, "person_id": 3, "org_id": 2, "title": "龙南市委副书记、市长", "start": "2021", "end": "2026-07", "rank": "县处级正职", "note": "前任市长，2026年7月正在过渡交接中。领导信息仍列出。1975年7月生，江西赣州人，研究生学历。"},
    # 钟旭辉 — 前任市委书记
    {"id": 8, "person_id": 4, "org_id": 1, "title": "龙南市委书记（前任）", "start": "2021", "end": "2026-06", "rank": "县处级正职", "note": "前任市委书记。1968年11月生，江西赣州人，大学学历。约2021-2026年在任，去向待查。"},
    # 政府领导班子成员
    {"id": 9, "person_id": 5, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 10, "person_id": 6, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 11, "person_id": 7, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 12, "person_id": 8, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 13, "person_id": 9, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 14, "person_id": 10, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
    {"id": 15, "person_id": 11, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。注：杨春景此前任全南县委常委、副县长，2026年7月调任龙南。"},
    {"id": 16, "person_id": 12, "org_id": 2, "title": "龙南市委常委、副市长", "start": "", "end": "", "rank": "县处级副职", "note": "现任政府班子领导成员。"},
]

# Additional orgs for 边建忠's previous positions (we reference from 全南县 DB)
# Add these as virtual orgs for the positions above
organizations.append({"id": 4, "name": "中共全南县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州全南"})
organizations.append({"id": 5, "name": "全南县人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州全南"})

relationships = [
    # 边建忠 ↔ 刘耿（新任党政正职搭档）
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政正职搭档",
        "context": "边建忠（龙南市委书记）与刘耿（龙南市委副书记、市长候选人）为新任市委市政府正职搭档。2026年7月3日共同走访重点工业企业。",
        "overlap_org": "龙南市党政班子",
        "overlap_period": "2026-07至今",
    },
    # 边建忠 ↔ 彭江闽（前任接任）
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "前任接任（市委书记与前任市长）",
        "context": "边建忠（新任龙南市委书记）与彭江闽（前任市长，正在过渡交接）。过渡期内二人可能短暂共事。",
        "overlap_org": "龙南市党政班子",
        "overlap_period": "2026-07",
    },
    # 边建忠 ↔ 钟旭辉（前任接任市委书记）
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "前任接任（市委书记）",
        "context": "边建忠接替钟旭辉任龙南市委书记。钟旭辉约2021-2026年在任，去向待查。",
        "overlap_org": "中共龙南市委员会",
        "overlap_period": "2026-07（交接）",
    },
    # 彭江闽 ↔ 钟旭辉（前任党政正职搭档）
    {
        "id": 4,
        "person_a_id": 3,
        "person_b_id": 4,
        "type": "党政正职搭档（前任）",
        "context": "彭江闽（前任市长）与钟旭辉（前任市委书记）为前任龙南市党政正职搭档（2021-2026年）。",
        "overlap_org": "龙南市党政班子",
        "overlap_period": "2021-2026",
    },
    # 彭江闽 ↔ 刘耿（前任接任市长）
    {
        "id": 5,
        "person_a_id": 3,
        "person_b_id": 2,
        "type": "前任接任（市长）",
        "context": "彭江闽（前任市长）与刘耿（市长候选人）为前任接任关系。2026年7月交接过渡。",
        "overlap_org": "龙南市人民政府",
        "overlap_period": "2026-07",
    },
    # 边建忠 ↔ 杨春景（全南共事关系延伸）
    {
        "id": 6,
        "person_a_id": 1,
        "person_b_id": 11,
        "type": "跨地区共事关系",
        "context": "边建忠（全南前任县委书记）与杨春景（全南前任县委常委、副县长）曾在全南党政班子共事。杨春景约2026年7月亦调任龙南市委常委、副市长。",
        "overlap_org": "全南县党政班子/龙南市党政班子",
        "overlap_period": "至2026-07",
    },
]

# Add relationships between 边建忠 and government team members (same org)
for deputy_id in [5, 6, 7, 8, 9, 10, 12]:
    rid = len(relationships) + 1
    relationships.append({
        "id": rid,
        "person_a_id": 1,
        "person_b_id": deputy_id,
        "type": "党政领导与政府副职",
        "context": "边建忠（市委书记）与龙南市政府副市长为市委市政府领导工作关系。",
        "overlap_org": "龙南市党政班子",
        "overlap_period": "2026-07至今",
    })


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    """Person color by role."""
    post = post or ""
    if "书记" in post and "副" not in post and ("市委" in post or "党委" in post):
        return "230,50,50"
    if "副书记" in post:
        return "200,80,80"
    if "市长" in post or ("书记" in post and "市委" in post and "副" not in post):
        if "候选" in post:
            return "50,100,230"
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "副市长" in post:
        return "80,140,230"
    if "常委" in post:
        return "150,100,50"
    return "120,120,120"


def ocolor_viz(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
    }.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>龙南市领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post", ""))
        sz = "20.0" if p["id"] in (1, 2, 3, 4) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c_val = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")), ("2", pos.get("end", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("龙南市 Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    import sys
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
