#!/usr/bin/env python3
"""
Build 章贡区 (Zhanggong District, 赣州市, Jiangxi) government personnel
relationship network — SQLite database + GEXF graph.

章贡区 is the central urban district (市中心城区) of 赣州市, Jiangxi Province.
Current as of: 2026-07-15

Targets: 区委书记 & 区长
Core figures: 刘仁羿 (区委书记), 方忠 (区委副书记、区长候选人)
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "章贡区_network.db")
GEXF_PATH = os.path.join(BASE, "章贡区_network.gexf")

today = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────────

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "刘仁羿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区委书记、区人武部党委第一书记",
        "current_org": "中共章贡区委员会",
        "source": "章贡区人民政府官网 https://www.zgq.gov.cn （2026年7月多次报道）",
    },
    {
        "id": 2,
        "name": "方忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区委副书记、区长候选人",
        "current_org": "章贡区人民政府",
        "source": "章贡区人民政府官网 https://www.zgq.gov.cn （2026年7月报道）",
    },
    # ── Predecessors ────────────────────────────────────────────────────
    {
        "id": 3,
        "name": "连天浪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-03",
        "birthplace": "江西信丰",
        "education": "大学学历",
        "party_join": "1987-06",
        "work_start": "1987-08",
        "current_post": "赣州市副市长（原章贡区委书记）",
        "current_org": "赣州市人民政府",
        "source": "https://www.ganzhou.gov.cn/gzszf/ltl/zw_sz.shtml; 公开报道",
    },
    # ── Key deputies: 区委常委、副区长 ─────────────────────────────────
    {
        "id": 4,
        "name": "江信芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "江西婺源",
        "education": "本科学历、学士学位",
        "party_join": "2006",
        "work_start": "2008",
        "current_post": "章贡区委常委、区政府副区长",
        "current_org": "章贡区人民政府",
        "source": "章贡区政府官网 领导信息 https://www.zgq.gov.cn",
    },
    # ── 副区长 ──────────────────────────────────────────────────────────
    {
        "id": 5,
        "name": "张毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "江西南康",
        "education": "江西理工大学研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "章贡区副区长",
        "current_org": "章贡区人民政府",
        "source": "https://www.zgq.gov.cn/zgqzf/ldxx/202109/56e1fe24a08f4ac69d70388fee14317d.shtml",
    },
    {
        "id": 6,
        "name": "曾宪荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "赣州龙南",
        "education": "本科学历",
        "party_join": "1999-12",
        "work_start": "1994-07",
        "current_post": "章贡区副区长、市公安局章贡分局局长",
        "current_org": "章贡区人民政府/市公安局章贡分局",
        "source": "https://www.zgq.gov.cn/zgqzf/ldxx/202509/106a66fd5f41415fa07e8c812f1e4e94.shtml",
    },
    {
        "id": 7,
        "name": "曾小荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区副区长",
        "current_org": "章贡区人民政府",
        "source": "章贡区政府官网 领导信息",
    },
    {
        "id": 8,
        "name": "练绪斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区副区长",
        "current_org": "章贡区人民政府",
        "source": "章贡区政府官网 领导信息",
    },
    # ── 其他区领导 ──────────────────────────────────────────────────────
    {
        "id": 9,
        "name": "李明海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区人大常委会主任",
        "current_org": "章贡区人大常委会",
        "source": "章贡区政府官网新闻报道 2026-07-15",
    },
    {
        "id": 10,
        "name": "杨忠万",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区政协主席",
        "current_org": "章贡区政协",
        "source": "章贡区政府官网新闻报道 2026-07-15",
    },
    {
        "id": 11,
        "name": "李胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区领导（区委常委、人武部?）",
        "current_org": "中共章贡区委员会",
        "source": "章贡区政府官网新闻报道 2026-07-14",
    },
    {
        "id": 12,
        "name": "肖辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区领导",
        "current_org": "中共章贡区委员会",
        "source": "章贡区政府官网新闻报道 2026-07-14",
    },
    {
        "id": 13,
        "name": "林洪飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "章贡区领导",
        "current_org": "中共章贡区委员会",
        "source": "章贡区政府官网新闻报道 2026-07-14",
    },
]

organizations = [
    {"id": 1, "name": "中共章贡区委员会", "type": "党委", "level": "县处级",
     "parent": "中共赣州市委员会", "location": "江西赣州章贡"},
    {"id": 2, "name": "章贡区人民政府", "type": "政府", "level": "县处级",
     "parent": "赣州市人民政府", "location": "江西赣州章贡"},
    {"id": 3, "name": "章贡区人大常委会", "type": "人大", "level": "县处级",
     "parent": "赣州市人大常委会", "location": "江西赣州章贡"},
    {"id": 4, "name": "章贡区政协", "type": "政协", "level": "县处级",
     "parent": "赣州市政协", "location": "江西赣州章贡"},
    {"id": 5, "name": "市公安局章贡分局", "type": "政府", "level": "副处级",
     "parent": "赣州市公安局", "location": "江西赣州章贡"},
    {"id": 6, "name": "章贡区人武部", "type": "政府", "level": "县处级",
     "parent": "赣州军分区", "location": "江西赣州章贡"},
    {"id": 7, "name": "赣州市人民政府", "type": "政府", "level": "地厅级",
     "parent": "江西省人民政府", "location": "江西赣州"},
]

positions = [
    # 刘仁羿
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "章贡区委书记、区人武部党委第一书记", "start": "2026?", "end": "",
     "rank": "县处级正职", "note": "现任（2026年7月已任，具体到任时间待确认）"},
    # 方忠
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "章贡区委副书记", "start": "2026?", "end": "",
     "rank": "县处级副职", "note": "现任"},
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "章贡区区长候选人", "start": "2026?", "end": "",
     "rank": "县处级正职", "note": "区长候选人，待人大任命"},
    # 连天浪（前任书记）
    {"id": 4, "person_id": 3, "org_id": 1,
     "title": "章贡区委书记", "start": "2021?", "end": "2026?",
     "rank": "县处级正职", "note": "前任区委书记，后升任赣州市副市长"},
    {"id": 5, "person_id": 3, "org_id": 7,
     "title": "赣州市副市长", "start": "2026?", "end": "",
     "rank": "副厅级", "note": "现任"},
    # 江信芳
    {"id": 6, "person_id": 4, "org_id": 1,
     "title": "章贡区委常委", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 7, "person_id": 4, "org_id": 2,
     "title": "章贡区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 张毅
    {"id": 8, "person_id": 5, "org_id": 2,
     "title": "章贡区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任（民盟盟员）"},
    # 曾宪荣
    {"id": 9, "person_id": 6, "org_id": 2,
     "title": "章贡区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    {"id": 10, "person_id": 6, "org_id": 5,
     "title": "市公安局章贡分局局长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 曾小荣
    {"id": 11, "person_id": 7, "org_id": 2,
     "title": "章贡区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 练绪斌
    {"id": 12, "person_id": 8, "org_id": 2,
     "title": "章贡区副区长", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 李明海
    {"id": 13, "person_id": 9, "org_id": 3,
     "title": "章贡区人大常委会主任", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 杨忠万
    {"id": 14, "person_id": 10, "org_id": 4,
     "title": "章贡区政协主席", "start": "", "end": "",
     "rank": "县处级正职", "note": "现任"},
    # 李胜
    {"id": 15, "person_id": 11, "org_id": 1,
     "title": "章贡区领导（区委常委）", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 肖辉
    {"id": 16, "person_id": 12, "org_id": 1,
     "title": "章贡区领导", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
    # 林洪飞
    {"id": 17, "person_id": 13, "org_id": 1,
     "title": "章贡区领导", "start": "", "end": "",
     "rank": "副处级", "note": "现任"},
]

relationships = [
    # 党政搭档：刘仁羿 × 方忠
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "党政搭档",
     "context": "刘仁羿（区委书记）与方忠（区委副书记、区长候选人）为章贡区党政正职搭档",
     "overlap_org": "章贡区", "overlap_period": "2026?至今"},
    # 前后任：连天浪 → 刘仁羿
    {"id": 2, "person_a_id": 3, "person_b_id": 1,
     "type": "前后任",
     "context": "连天浪（前任章贡区委书记）→ 刘仁羿（现任章贡区委书记），连天浪升任赣州市副市长",
     "overlap_org": "中共章贡区委员会", "overlap_period": "2026?交接"},
    # 刘仁羿与各常委/副区长的上下级关系
    {"id": 3, "person_a_id": 1, "person_b_id": 4,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与江信芳（常委、副区长）",
     "overlap_org": "中共章贡区委员会", "overlap_period": "至今"},
    {"id": 4, "person_a_id": 1, "person_b_id": 5,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与张毅（副区长）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    {"id": 5, "person_a_id": 1, "person_b_id": 6,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与曾宪荣（副区长、公安局长）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    {"id": 6, "person_a_id": 1, "person_b_id": 7,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与曾小荣（副区长）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    {"id": 7, "person_a_id": 1, "person_b_id": 8,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与练绪斌（副区长）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    {"id": 8, "person_a_id": 1, "person_b_id": 9,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与李明海（人大主任）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    {"id": 9, "person_a_id": 1, "person_b_id": 10,
     "type": "上下级",
     "context": "刘仁羿（区委书记）与杨忠万（政协主席）",
     "overlap_org": "章贡区", "overlap_period": "至今"},
    # 连天浪与章贡区领导层
    {"id": 10, "person_a_id": 3, "person_b_id": 4,
     "type": "上下级",
     "context": "连天浪（前任区委书记）与江信芳（常委、副区长）曾在章贡区共事",
     "overlap_org": "章贡区", "overlap_period": ""},
    # 方忠与各副区长的工作关系
    {"id": 11, "person_a_id": 2, "person_b_id": 4,
     "type": "上下级",
     "context": "方忠（区长候选人）与江信芳（常委、副区长）",
     "overlap_org": "章贡区人民政府", "overlap_period": "至今"},
]


# ── BUILD SQLite ─────────────────────────────────────────────────────────

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
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER NOT NULL,
            person_b_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
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

    print(f"✓ SQLite DB created: {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    return counts


# ── BUILD GEXF ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"  # Red for party secretary
    if "区长" in role or "市长" in role or "县长" in role:
        return "50,100,255"  # Blue for government head
    if "纪委书记" in role or "纪检" in role:
        return "255,165,0"  # Orange for discipline
    return "100,100,100"  # Grey


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    return p["id"] <= 2


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>章贡区领导班子工作关系网络 - 区委书记刘仁羿 &amp; 区长候选人方忠</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "role"), ("2", "birth"), ("3", "birthplace"), ("4", "education")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "context"), ("2", "start"), ("3", "end")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
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
        lines.append(f'          <attvalue for="4" value="{esc(p.get("education", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Worked-at edges (person -> organization)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person <-> person)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")
    print(f"    Nodes: {len(persons) + len(organizations)}")
    print(f"    Edges: {len(positions) + len(relationships)}")


# ── MAIN ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"章贡区 (Zhanggong District) 领导班子工作关系网络")
    print(f"Date: {today}")
    print(f"{'─' * 50}")
    build_db()
    build_gexf()
    print(f"{'─' * 50}")
    print(f"Done. Artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
