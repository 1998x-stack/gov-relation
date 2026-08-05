#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美兰区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 海南省
Parent City: 海口市
Region: 美兰区
Task: hainan_美兰区
Targets: 区委书记 & 区长

当前在任 (截至 2026-08-05，区政门户 meilan.gov.cn DNS 不可达；以下以海口市委组织部任前公示
与中新网海南一手报道为准，林 uncertainty / unverified 已记录于 open_gaps):

核心领导：
- 区委书记: 朱军 (中共海口市美兰区委书记；中新网海南 2023-07-28 区委八届三次全会报告工作；
  至调查日未见其在任/离任的一手公示，2026 状态标记 unverified)
- 区委副书记、区长: 吴升娇 (中新网海南 2023-07-28 全会作全区上半年经济运行报告；
  2026 状态标记 unverified)

已确认区领导 (via 海口市委组织部干部任前公示 2026-04-10):
- 王辉: 男，汉族，1974-03，大学，工学学士；现任美兰区委常委、区人民政府副区长、区二级调研员；拟任市直单位正职 (升迁调离)
- 黄克民: 男，汉族，1975-05，中央党校研究生，法学学士；曾任市农业农村局党组书记、局长、一级调研员、市乡村振兴局局长(兼)；拟任市辖区党委副书记、提名为市辖区人民政府区长候选人 (候选区待确认是否即美兰区)

上级: 海口市委书记 范少军、市长 张勇、常务副市长 党帅 (来自本仓库 hainan_海口市 调研)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "hainan_美兰区"
SLUG = "美兰区"
AS_OF = "2026-08-05"
now = AS_OF.replace("-", "")

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

# =========================================================================
# 1. SOURCE REGISTER
# =========================================================================
source_register = [
    {"id": "S001", "title": "中共海口市美兰区委第八届第三次全体会议暨全区上半年经济工作会议召开",
     "url": "https://www.hi.chinanews.com.cn/zt/14/2023/0729/99869.html",
     "publisher": "中新网海南", "published_at": "2023-07-29", "accessed_at": AS_OF,
     "source_type": "media", "reliability": "high",
     "notes": "会议明'区委书记朱军受区委常委会委托向全会报告工作'，'区委副书记、区长吴升娇作全区上半年经济运行情况报告'。党务/政务要点：全力推进海南自贸港建设、加快江东新区建设、做好封关运作准备"},
    {"id": "S002", "title": "海口市拟任干部人选公告（2026-04-10）",
     "url": "https://www.haikou.gov.cn/xxgk/szfbjxxgk/rsxx/gbrqgs/202604/t1519219.shtml",
     "publisher": "中共海口市委组织部（海口市人民政府门户）", "published_at": "2026-04-10", "accessed_at": AS_OF,
     "source_type": "appointment_notice", "reliability": "high",
     "notes": "任前公示；王辉：现任美兰区委常委、区人民政府副区长，美兰区二级调研员，拟任市直单位正职；黄克民：现任市农业农村局党组书记、局长、一级调研员，市乡村振兴局局长（兼），拟任市辖区党委副书记、提名为市辖区人民政府区长候选人"},
    {"id": "S003", "title": "海口市人民政府 —— 市长专栏（张勇）",
     "url": "https://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202112/t269387.shtml",
     "publisher": "海口市人民政府", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "海口市委副书记、市政府党组书记、市长 张勇（汉，1974-05，大学，工程硕士，高级工程师），主持市政府全面工作"},
    {"id": "S004", "title": "本地既有调研 —— 海口市领导班子（范少军 / 张勇 / 党帅）",
     "url": "data/tmp/hainan_海口市/checkpoint_01_research.md",
     "publisher": "本仓库", "published_at": "2026-08", "accessed_at": AS_OF,
     "source_type": "inferred", "reliability": "medium",
     "notes": "海口市委书记范少军（省委常委兼任）、市长张勇、常务副市长党帅（1984-02，研究生，博士）"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ── 核心领导：区委书记 ──
    {"id": 1, "name": "朱军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共海口市美兰区委书记", "current_org": "中共美兰区委员会",
     "source": "S001"},
    # ── 核心领导：区长 ──
    {"id": 2, "name": "吴升娇", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共美兰区委副书记、区人民政府区长", "current_org": "美兰区人民政府",
     "source": "S001"},
    # ── 已确认区领导（海口组任免公示，多为升迁/调任） ──
    {"id": 3, "name": "王辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-03", "birthplace": "", "education": "大学，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原美兰区委常委、副区长（2026-04 拟任市直单位正职）", "current_org": "美兰区人民政府",
     "source": "S002"},
    {"id": 4, "name": "黄克民", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "", "education": "中央党校研究生，法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拟任市辖区区长（原市农业农村局党组书记、局长）", "current_org": "海口市农业农村局",
     "source": "S002"},
    # ── 上级（海口市，供给网络分析） ──
    {"id": 5, "name": "范少军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南省委常委、海口市委书记", "current_org": "中共海口市委员会",
     "source": "S004"},
    {"id": 6, "name": "张勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-05", "birthplace": "", "education": "大学，工程硕士，高级工程师",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海口市委副书记、市政府党组书记、市长", "current_org": "海口市人民政府",
     "source": "S003"},
    {"id": 7, "name": "党帅", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-02", "birthplace": "", "education": "研究生，工学博士，经济师",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海口市委常委、市政府党组副书记、常务副市长", "current_org": "海口市人民政府",
     "source": "S004"},
]

# =========================================================================
# 3. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共美兰区委员会", "type": "党委", "level": "县级",
     "parent": "中共海口市委员会", "location": "海南省海口市美兰区"},
    {"id": 2, "name": "美兰区人民政府", "type": "政府", "level": "县级",
     "parent": "海口市人民政府", "location": "海南省海口市美兰区"},
    {"id": 3, "name": "海口市农业农村局", "type": "政府", "level": "地级市直",
     "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 4, "name": "中共海口市委员会", "type": "党委", "level": "地级",
     "parent": "中共海南省委员会", "location": "海南省海口市"},
    {"id": 5, "name": "海口市人民政府", "type": "政府", "level": "地级",
     "parent": "海南省人民政府", "location": "海南省海口市"},
]

# =========================================================================
# 4. POSITIONS
# =========================================================================
positions = [
    # ── 朱军（区委书记） ──
    {"person_id": 1, "org_id": 1, "title": "中共海口市美兰区委书记",
     "start_date": "", "end_date": "", "rank": "县级正职", "note": "2023-07 主持区委八届三次全会；主持区委常委会；受区委常委会委托向全会报告工作"},
    # ── 吴升娇（区长） ──
    {"person_id": 2, "org_id": 1, "title": "中共美兰区委副书记",
     "start_date": "", "end_date": "", "rank": "县级副职", "note": "现任（2023-07 存档）"},
    {"person_id": 2, "org_id": 2, "title": "美兰区人民政府区长（党组书记）",
     "start_date": "", "end_date": "", "rank": "县级正职", "note": "领导区政府全面工作；作全区上半年经济运行情况报告"},
    # ── 王辉 ──
    {"person_id": 3, "org_id": 1, "title": "美兰区委常委",
     "start_date": "", "end_date": "", "rank": "县级副职", "note": "2026-04 现任，后拟升任市直单位正职"},
    {"person_id": 3, "org_id": 2, "title": "美兰区人民政府副区长（二级调研员）",
     "start_date": "", "end_date": "", "rank": "县级副职", "note": "2026-04 任前公示显示其现任；后拟任市直单位正职"},
    # ── 黄克民 ──
    {"person_id": 4, "org_id": 3, "title": "海口市农业农村局党组书记、局长、一级调研员",
     "start_date": "", "end_date": "", "rank": "地级市直正职", "note": "2026-04 任前公示显示其现任；兼市乡村振兴局局长"},
    # ── 上级 ──
    {"person_id": 5, "org_id": 4, "title": "海南省委常委、海口市委书记",
     "start_date": "", "end_date": "", "rank": "副省级", "note": "上级主管单位"},
    {"person_id": 6, "org_id": 4, "title": "海口市委副书记",
     "start_date": "", "end_date": "", "rank": "地级副职", "note": "上级主管单位"},
    {"person_id": 6, "org_id": 5, "title": "海口市人民政府市长（党组书记）",
     "start_date": "", "end_date": "", "rank": "地级正职", "note": "上级主管单位"},
    {"person_id": 7, "org_id": 4, "title": "海口市委常委",
     "start_date": "", "end_date": "", "rank": "地级副职", "note": "上级主管单位"},
    {"person_id": 7, "org_id": 5, "title": "海口市人民政府常务副市长（党组副书记）",
     "start_date": "", "end_date": "", "rank": "地级副职", "note": "上级主管单位"},
]

# =========================================================================
# 5. RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 党政主要领导 ──
    {"person_a": 1, "person_b": 2, "type": "上令下达",
     "context": "朱军（区委书记）与吴升娇（区委副书记、区长）构成书记-区长搭档，共同主持/出席区委八届三次全会暨全区经济工作会议",
     "overlap_org": "中共美兰区委员会 / 美兰区人民政府", "overlap_period": "2023-07"},
    # ── 书记/区长与已任副职 ──
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "区委书记朱军与区委常委、副区长王辉在美兰区委班子共事（王辉后拟调市直）",
     "overlap_org": "中共美兰区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "上下级",
     "context": "区长吴升娇与副区长王辉在区人民政府班子共事",
     "overlap_org": "美兰区人民政府", "overlap_period": ""},
    # ── 区长候选人交接线索（未确认是否即美兰） ──
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "若黄克民获批任美兰区长，将与现任区长吴升娇形成职务交接（候选区县未指明，证据为任前公示）",
     "overlap_org": "", "overlap_period": "2026-04"},
    # ── 上级关系 ──
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "美兰区委书记朱军受海口市委书记（范少军）领导，为上下级所述",
     "overlap_org": "中共海口市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "美兰区区长吴升娇受海口市市长（张勇）领导，为直管下级",
     "overlap_org": "海口市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "区委书记与海口市委常务副市长党帅在市级上下级关系",
     "overlap_org": "海口市", "overlap_period": ""},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    """Node color by role."""
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "255,50,50"          # red: party secretary
    if "区长" in post and "副" not in post and "人大" not in post and "政协" not in post:
        return "50,100,255"         # blue: government leader
    if "纪委书记" in post:
        return "255,165,0"          # orange: discipline
    if "副书记" in post or "副" in post:
        return "100,150,220"
    return "100,100,100"


def is_top_leader(post):
    return ("书记" in post and "副" not in post and "纪委" not in post) or \
           ("区长" in post and "副" not in post and "人大" not in post and "政协" not in post) or \
           ("市长" in post and "副" not in post and "任" not in post)


def person_shape(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "square"
    if "区长" in post and "副" not in post and "人大" not in post and "政协" not in post:
        return "circle"
    if "纪委书记" in post or "纪委" in post:
        return "diamond"
    return "triangle"


def org_color(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "开发区": "200,255,200",
    }
    return colors.get(otype, "200,200,200")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"meilan_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>美兰区领导班子工作关系网络（基于海口市组织部任免公示 / 中新网海南）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="meilan_{esc(p["name"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oc = org_color(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    # person -> organization (worked_at)
    for pos in positions:
        eid += 1
        src = person_map[pos['person_id']]
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{esc(src)}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("rank", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # person<->person (relationship), weight 2.0
    for r in relationships:
        eid += 1
        src = person_map[r['person_a']]
        tgt = person_map[r['person_b']]
        lines.append(f'      <edge id="{eid}" source="{esc(src)}" target="{esc(tgt)}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}   ({len(lines)} lines)")

    # ── Person JSON 生成 ──
    def make_person_json(p, timeline, relationships_list):
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "海南省",
                "city": "海口市",
                "region": "美兰区",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年8月"
            },
            "identity": {
                "person_id": f"meilan_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": p.get("education", ""),
                     "study_type": "unknown", "source_ids": []}
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县级正职" if is_top_leader(p.get("current_post", "")) else "县级副职",
                "as_of": AS_OF,
                "is_current_confirmed": "unverified",
                "source_ids": [p.get("source", "")]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") else "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": ""
            },
            "open_questions": []
        }

    # ── 区委书记 朱军 ──
    zj_timeline = [
        {"start": "", "end": "present", "org": "中共美兰区委员会", "title": "中共海口市美兰区委书记",
         "notes": "2023-07 主持区委八届三次全会并作报告；既定：全力推进海南自贸港建设、加快江东新区建设、封关准备",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "朱国当前（2026）是否仍在美兰区委书记在任务实未见，因区政网站不可达；其出生年、籍贯、教育背景、完整任职路径待查",
         "confidence": "unverified", "source_ids": []},
    ]
    zj_rels = [
        {"person": "吴升娇", "person_id": "meilan_吴升娇", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "朱军（区委书记）与吴升娇（区委副书记、区长）构成书记-区长搭档，共同出席区委全会暨经济工作会议",
         "overlap_org": "中共美兰区委员会 / 美兰区人民政府", "overlap_period": "2023-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王辉", "person_id": "meilan_王辉", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "区委书记朱军与区委常委、副区长王辉在区委班子共事（王2026年拟调市直）",
         "overlap_org": "中共美兰区委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S002"]},
        {"person": "范少军", "person_id": "meilan_范少军", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "美兰区委书记受海口市委书记（范少军）直接领导",
         "overlap_org": "中共海口市委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S004"]},
    ]
    zj_json = make_person_json(persons[0], [], [])
    zj_json["relationships"] = zj_rels
    zj_json["career_timeline"] = zj_timeline
    zj_json["governance_record"] = [
        {"period": "2023-07", "domain": "development_strategy", "achievement_or_event": "提出《中共美兰区委关于全力推进海南自由贸易港建设 加快推动美兰高质量发展的贯彻落实措施》",
         "role_in_event": "区委书记作方案说明并作总结讲话", "location": "海口市美兰区", "confidence": "confirmed", "source_ids": ["S001"]},
        {"period": "2023-07", "domain": "economic_development", "achievement_or_event": "主持召开全区上半年经济工作会议，部署下半年经济工作",
         "role_in_event": "受区委常委会委托向全会报告工作", "location": "海口市美兰区", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zj_json["work_style_and_personality"]["public_style_indicators"] = [
        {"trait": "development_oriented", "evidence": "强调自贸港建设、江东新区、封关准备、高质量发展", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    zj_json["open_questions"] = [
        {"priority": "critical", "question": "朱军2026年是否仍任美兰区委书记（区政网站不可达无法最终确认）",
         "why_it_matters": "核心目标对象在任状态直接决定整张网络的组织归属", "suggested_queries": ["朱军 美兰区委书记 2026", "海口市 美兰区 区委书记 任免"],
         "last_attempted": AS_OF},
        {"priority": "high", "question": "朱军完整履历（出生年、籍贯、民族、教育、任书记前任职）",
         "why_it_matters": "无法追溯晋升路径与系统/地方经历", "suggested_queries": ["朱军 简历 美兰区委书记 任前公示"], "last_attempted": AS_OF},
    ]
    zj_path = os.path.join(PERSONS_DIR, f"{now}-海南省-海口市-区委书记-朱军.json")
    with open(zj_path, "w", encoding="utf-8") as f:
        json.dump(zj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {zj_path}")

    # ── 区长 吴升娇 ──
    wsj_timeline = [
        {"start": "", "end": "present", "org": "美兰区人民政府", "title": "中共美兰区委副书记、美兰区人民政府区长",
         "notes": "2023-07 在区委全会上作全区上半年经济运行情况报告；主持区政府全面工作",
         "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "出生年、籍贯、学历、任区长前任职未查得；2026 是否仍在任未定",
         "confidence": "unverified", "source_ids": []},
    ]
    wsj_rels = [
        {"person": "朱军", "person_id": "meilan_朱军", "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "区长吴升娇与区委书记朱军构成书记-区长搭档，共同出席区委全会暨经济工作会议",
         "overlap_org": "美兰区委员会/美兰区人民政府", "overlap_period": "2023-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "黄克民", "person_id": "meilan_黄克民", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "黄克民2026-04拟任'市辖区区长'候选，若获批美区则与吴升娇形成交接（候选区内属不明）",
         "overlap_org": "", "overlap_period": "2026-04",
         "direction": "undirected", "confidence": "unverified", "source_ids": ["S002"]},
    ]
    wsj_json = make_person_json(persons[1], [], [])
    wsj_json["career_timeline"] = wsj_timeline
    wsj_json["relationships"] = wsj_rels
    wsj_json["governance_record"] = [
        {"period": "2023-07", "domain": "economic_development", "achievement_or_event": "作全区上半年经济运行情况报告",
         "role_in_event": "区长作报告，安排下半年经济工作", "location": "海口市美兰区", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wsj_json["open_questions"] = [
        {"priority": "critical", "question": "吴升娇2026是否仍美兰区区长；黄克民是否已接任",
         "why_it_matters": "区长在任状态与干部未来路径", "suggested_queries": ["吴升娇 美兰区长 2026", "黄克民 美兰区长"], "last_attempted": AS_OF},
        {"priority": "high", "question": "吴升娇完整履历与任区长时间", "why_it_matters": "评估其地方从政经历", "suggested_queries": ["吴升娇 简历 海口 美兰"], "last_attempted": AS_OF},
    ]
    wsj_path = os.path.join(PERSONS_DIR, f"{now}-海南省-海口市-区长-吴升娇.json")
    with open(wsj_path, "w", encoding="utf-8") as f:
        json.dump(wsj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wsj_path}")

    print("\nDone. All artifacts generated in staging directory.")
    print("  NOTE: 区级网(meilan.gov.cn) 不可达，人物履历/2026在任状态以 open_questions 与 report/open_gaps.md 记录不确定度。")


if __name__ == "__main__":
    build()