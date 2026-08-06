#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 利川市, 湖北省恩施土家族苗族自治州.

Current leadership (as of 2026-08-06):
- 市委书记: 熊翔 (was 市长 2021-11 => 接任书记, 前任市委书记 刘智勇)
- 市长: 赖于明 (2025-12 当选; 2025-08 市委副书记, 2025-09 代理市长)
Sources:
  - 利川市人民政府门户网站 http://www.lichuan.gov.cn (政府领导之窗, 领导简介, 中国利川网新闻)
  - 搜狗百科 / 中国网 / 中国利川网 (熊翔 履历)
"""

import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────
_STAGING = str(Path(__file__).resolve().parent)
DB_PATH = os.path.join(_STAGING, "利川市_network.db")
GEXF_PATH = os.path.join(_STAGING, "利川市_network.gexf")
os.makedirs(_STAGING, exist_ok=True)

# ── DATA ──────────────────────────────────────────────────────────────

persons = [
    # ── 现任党政主官 ──
    # 熊翔: 现任市委书记（接前任刘智勇）。此前长期任利川市长（2021-11 当选）
    {"id": 1, "name": "熊翔", "gender": "男", "ethnicity": "土家族",
     "birth": "1983-10", "birthplace": "湖北咸丰", "education": "省委党校研究生（法学）",
     "party_join": "中共党员（2006-12）", "work_start": "2007-07",
     "current_post": "利川市委书记", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},
    # 2: 赖于明: 现任市长（2025-12 当选）。此前任鹤峰县委副书记、政法委书记
    {"id": 2, "name": "赖于明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖北恩施", "education": "大学（中南民族大学法学）",
     "party_join": "中共党员（2007-07）", "work_start": "2005-10",
     "current_post": "利川市委副书记、市人民政府市长", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},

    # ── 前任市委书记 刘智勇（2021届当选 →2023前后 交予熊翔，去向待查）──
    {"id": 13, "name": "刘智勇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任利川市委书记（约2023离任，去向待查）", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},

    # ── 市委/人大领导（confirmed via 官方新闻）──
    {"id": 14, "name": "何文建", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "利川市人大常委会党组书记、主任", "current_org": "利川市人民代表大会常务委员会",
     "source": "http://www.lichuan.gov.cn/"},
    {"id": 15, "name": "赵学成", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "利川市委领导（陪同书记调研党建；拟市委副书记）", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},
    {"id": 16, "name": "刘勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "利川市领导（市委领导班子成员）", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},
    {"id": 17, "name": "郑金禄", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "利川市领导（市委领导班子成员）", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},
    {"id": 18, "name": "王梅", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "利川市领导（市委领导班子成员）", "current_org": "中共利川市委员会",
     "source": "http://www.lichuan.gov.cn/"},

    # ── 市政府领导班子（现任副市长们）──
    {"id": 3, "name": "周爱华", "gender": "女", "ethnicity": "土家族",
     "birth": "1974-05", "birthplace": "湖北利川", "education": "研究生（湖北省委党校法学）",
     "party_join": "", "work_start": "1991-08",
     "current_post": "利川市人民政府副市长", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 4, "name": "吴兴灿", "gender": "男", "ethnicity": "苗族",
     "birth": "1972-03", "birthplace": "湖北利川", "education": "大学（湖北大学自考秘书）",
     "party_join": "中共党员（1994-07）", "work_start": "1991-09",
     "current_post": "利川市人民政府党组成员、副市长", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 5, "name": "佘军", "gender": "男", "ethnicity": "土家族",
     "birth": "1974-12", "birthplace": "湖北利川", "education": "大学（湖北省委党校法律专业）",
     "party_join": "中共党员（2001-03）", "work_start": "1996-11",
     "current_post": "利川市人民政府副市长", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 6, "name": "陈建平", "gender": "男", "ethnicity": "土家族",
     "birth": "1970-09", "birthplace": "湖北利川", "education": "大学",
     "party_join": "中共党员（1995-03）", "work_start": "1993-09",
     "current_post": "利川市人民政府副市长、经济开发区党工委书记", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 7, "name": "王厚军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "湖北利川", "education": "大学（湖北省委党校法律专业）",
     "party_join": "中共党员（1999-05）", "work_start": "1993-09",
     "current_post": "利川市人民政府副市长（2025-10 起市政府党组成员）", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 8, "name": "王珍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "山东济南", "education": "研究生（法学硕士）",
     "party_join": "中共党员（1993-03）", "work_start": "1990-12（参军）",
     "current_post": "利川市人民政府副市长（中国国新挂职）", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
    {"id": 9, "name": "谭吉昌", "gender": "男", "ethnicity": "土家族",
     "birth": "1981-09", "birthplace": "湖北巴东", "education": "大学",
     "party_join": "中共党员（2005-12）", "work_start": "2003-07",
     "current_post": "利川市人民政府副市长", "current_org": "利川市人民政府",
     "source": "http://www.lichuan.gov.cn/xxgk/gkml/zfld/"},
]

organizations = [
    {"id": 1, "name": "中共利川市委员会", "type": "党委", "level": "县处级",
     "parent": "中共恩施州委员会", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 2, "name": "利川市人民政府", "type": "政府", "level": "县处级",
     "parent": "恩施州人民政府", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 3, "name": "利川市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "恩施州人大常委会", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 4, "name": "中国人民政治协商会议利川市委员会", "type": "政协", "level": "县处级",
     "parent": "恩施州政协", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 5, "name": "利川市监察委员会", "type": "纪委", "level": "县处级",
     "parent": "恩施州监察委员会", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 6, "name": "利川经济开发区", "type": "开发区", "level": "乡科级",
     "parent": "利川市人民政府", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 7, "name": "利川市人民武装部", "type": "党委", "level": "乡科级",
     "parent": "恩施军分区", "location": "湖北省恩施土家族苗族自治州利川市"},
    {"id": 8, "name": "中共恩施州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共湖北省委", "location": "湖北省恩施土家族苗族自治州"},
    {"id": 9, "name": "恩施州人民政府", "type": "政府", "level": "地厅级",
     "parent": "湖北省人民政府", "location": "湖北省恩施土家族苗族自治州"},
]

positions = [
    # ── 熊翔 ──
    {"person_id": 1, "org_id": 2, "title": "利川市人民政府市长", "start_date": "2021-11", "end_date": "2025", "rank": "正县级", "note": "2021-11 当选市长；曾任巴东县常务副县长、鹤峰县组织部长等"},
    {"person_id": 1, "org_id": 1, "title": "利川市委书记", "start_date": "2023", "end_date": "present", "rank": "正县级", "note": "接替前任书记刘智勇；2026-07 以来以市委书记身份主持市委常委会/调研党建"},

    # ── 赖于明 ──
    {"person_id": 2, "org_id": 1, "title": "利川市委副书记", "start_date": "2025-08", "end_date": "present", "rank": "正县级", "note": "2025-08 任利川市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "利川市人民政府副市长、代理市长→市长", "start_date": "2025-09", "end_date": "present", "rank": "正县级", "note": "2025-09 任副市长、代理市长；2025-12 当选市长"},

    # ── 前任市委书记 刘智勇 ──
    {"person_id": 13, "org_id": 1, "title": "利川市委书记", "start_date": "2021", "end_date": "2023", "rank": "正县级", "note": "2021 新一届市委当选书记；约2023交由熊翔，去向待查"},

    # ── 人大/市委班子 ──
    {"person_id": 14, "org_id": 3, "title": "利川市人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2026-07 主持市选举委员会第一次会议"},
    {"person_id": 15, "org_id": 1, "title": "利川市委领导（疑市委副书记）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026-07-23 陪同市委书记熊翔调研基层党建"},
    {"person_id": 16, "org_id": 1, "title": "利川市领导（市委班子成员）", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "利川市领导（市委班子成员）", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "利川市领导（市委班子成员）", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},

    # ── 市政府副市长们 ──
    {"person_id": 3, "org_id": 2, "title": "利川市人民政府副市长", "start_date": "2021-08", "end_date": "present", "rank": "副县级", "note": "2021-08 当选副市长；曾任建始县副县长等"},
    {"person_id": 4, "org_id": 2, "title": "利川市人民政府党组成员、副市长", "start_date": "2024-12", "end_date": "present", "rank": "副县级", "note": "2024-12 任利川市副市长；此前2021-09任来凤县副县长"},
    {"person_id": 5, "org_id": 2, "title": "利川市人民政府副市长", "start_date": "2021-11", "end_date": "present", "rank": "副县级", "note": "2021-11 当选副市长；长期在利川乡镇/市委组织部任职"},
    {"person_id": 6, "org_id": 2, "title": "利川市人民政府副市长、经济开发区党工委书记", "start_date": "2024-09", "end_date": "present", "rank": "副县级", "note": "2024-09 当选副市长；长期在利川/经济开发区任职"},
    {"person_id": 7, "org_id": 2, "title": "利川市人民政府副市长", "start_date": "2025-10", "end_date": "present", "rank": "副县级", "note": "2025-10 任市政府党组成员"},
    {"person_id": 8, "org_id": 2, "title": "利川市人民政府副市长（挂职）", "start_date": "2024-11", "end_date": "present", "rank": "副县级", "note": "中国国新控股选派挂职；2024-11 当选"},
    {"person_id": 9, "org_id": 2, "title": "利川市人民政府副市长", "start_date": "2025-09", "end_date": "present", "rank": "副县级", "note": "2025-09 任副市长；此前在湖北省公安厅"},
]

relationships = [
    # 党政搭档（现任）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "熊翔（市委书记）与赖于明（市委副书记、市长）为现任党政主官搭档", "overlap_org": "利川市", "overlap_period": "2025-2026"},
    # 前后任：书记（刘智勇→熊翔）
    {"person_a": 13, "person_b": 1, "type": "前任继任",
     "context": "刘智勇卸任利川市委书记后由熊翔接任（约2023）", "overlap_org": "中共利川市委员会", "overlap_period": "2023"},
    # 前后任：市长（熊翔→赖于明）
    {"person_a": 1, "person_b": 2, "type": "前任继任",
     "context": "熊翔由市长升任（兼任）市委书记，市长职于2025-12交由赖于明", "overlap_org": "利川市人民政府", "overlap_period": "2025"},
    # 书记与人大主任
    {"person_a": 1, "person_b": 14, "type": "班子共事",
     "context": "市委书记与市人大常委会主任何文建为市人大/市委领导核心搭档", "overlap_org": "利川市", "overlap_period": "2025-2026"},
    # 书记与市委班子成员
    {"person_a": 1, "person_b": 15, "type": "班子共事",
     "context": "市委书记与（疑市委副书记）赵学成在市委班子共事，赵陪同调研", "overlap_org": "中共利川市委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "班子共事",
     "context": "市长与副市长周爱华在市政府班子共事", "overlap_org": "利川市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "班子共事",
     "context": "市长与副市长（经济开发区党工委书记）陈建平在市政府班子共事", "overlap_org": "利川市人民政府", "overlap_period": ""},
]

# ── BUILD ─────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    DROP TABLE IF EXISTS relationships;
    DROP TABLE IF EXISTS positions;
    DROP TABLE IF EXISTS organizations;
    DROP TABLE IF EXISTS persons;
    CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
    CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '');
    CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
    CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""), p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""), p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)", (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location","")))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)", (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date",""), pos.get("end_date",""), pos.get("rank",""), pos.get("note","")))
    for rel in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", (rel["person_a"], rel["person_b"], rel["type"], rel["context"], rel["overlap_org"], rel["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post:
        return "255,50,50"
    if "市长" in post or "副" in post:
        return "50,100,255"
    return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    return {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255", "政协": "255,240,200", "开发区": "200,255,200", "纪委": "255,165,0"}.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>利川市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if ("书记" in p.get("current_post","") or "市长" in p.get("current_post","")) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for rel in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Build complete (staging).")