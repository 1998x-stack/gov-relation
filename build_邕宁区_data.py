#!/usr/bin/env python3
"""
南宁市邕宁区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Yongning District leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 南宁市
Region: 邕宁区
Targets: 区委书记 & 区长

Research Sources:
- 南宁市邕宁区人民政府官网 (www.yongning.gov.cn) — 领导之窗页面
- 各领导个人简历页面（区长、副区长）
- 邕宁区人大任免公告
- 邕宁区区委会议新闻报道

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP = SCRIPT_DIR
DB_PATH = os.path.join(TMP, "邕宁区_network.db")
GEXF_PATH = os.path.join(TMP, "邕宁区_network.gexf")
PERSONS_DIR = os.path.join(TMP)
AS_OF = "2026-07-22"

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "梁国禄",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邕宁区委书记",
        "current_org": "中共南宁市邕宁区委员会",
        "source": "邕宁区政府官网新闻 — 2025年12月党外人士座谈会报道；邕宁区政府官网(yongning.gov.cn)"
    },
    {
        "id": 2,
        "name": "陈国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "湖南宁乡",
        "education": "研究生学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邕宁区区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "南宁市邕宁区人民政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t6651979.html) — 2026年6月9日更新"
    },
    # ════════════════════════════════════════
    # Key Deputies (区政府领导班子 + 区委常委)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李东平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "湖南新化",
        "education": "研究生学历，工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邕宁区委常委、常务副区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t6647254.html) — 2026年6月2日更新"
    },
    {
        "id": 4,
        "name": "潘海英",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1976年3月",
        "birthplace": "广西南宁",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邕宁区副区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t5265643.html)"
    },
    {
        "id": 5,
        "name": "谢晴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "广西贺州",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邕宁区委常委、副区长（挂职）",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t6647289.html) — 2026年6月2日更新"
    },
    {
        "id": 6,
        "name": "周俊",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "",
        "current_post": "邕宁区副区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t5968910.html) — 2024年7月15日更新"
    },
    {
        "id": 7,
        "name": "胡万成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "广西兴安",
        "education": "大学本科学历，经济学学士",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "邕宁区副区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t5860924.html) — 2026年6月2日更新"
    },
    {
        "id": 8,
        "name": "覃苏舜",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1990年5月",
        "birthplace": "广西环江",
        "education": "研究生学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邕宁区副区长",
        "current_org": "南宁市邕宁区人民政府",
        "source": "邕宁区政府官网(www.yongning.gov.cn/xxgk/fdzdgk/jcxxgk/ldzc/t6671774.html) — 2026年6月30日更新"
    },
    # ════════════════════════════════════════
    # Predecessor & Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "陶岳彬",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任）邕宁区原区长",
        "current_org": "已离任",
        "source": "邕宁区政府官网新闻 — 2025年12月31日党外人士座谈会报道"
    },
    # ════════════════════════════════════════
    #人大/政协领导
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "黄壮章",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "邕宁区人大常委会主任",
        "current_org": "南宁市邕宁区人大常委会",
        "source": "邕宁区政府官网新闻"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共南宁市邕宁区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共南宁市委员会",
        "location": "广西南宁市邕宁区"
    },
    {
        "id": 2,
        "name": "南宁市邕宁区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "南宁市人民政府",
        "location": "广西南宁市邕宁区"
    },
    {
        "id": 3,
        "name": "南宁市邕宁区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "南宁市人大常委会",
        "location": "广西南宁市邕宁区"
    },
    {
        "id": 4,
        "name": "邕宁新兴产业园区管理委员会",
        "type": "开发区",
        "level": "市辖区",
        "parent": "南宁市邕宁区人民政府",
        "location": "广西南宁市邕宁区"
    },
    {
        "id": 5,
        "name": "广西驻村工作队邕宁区工作队",
        "type": "事业单位",
        "level": "市辖区",
        "parent": "自治区党委编委办",
        "location": "广西南宁市邕宁区"
    },
    {
        "id": 6,
        "name": "南宁市邕宁区政协",
        "type": "政协",
        "level": "市辖区",
        "parent": "南宁市政协",
        "location": "广西南宁市邕宁区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 梁国禄 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "邕宁区委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 陈国栋 — 区长/区委副书记
    {"person_id": 2, "org_id": 2, "title": "邕宁区区长", "start": "2026年", "end": "present", "rank": "正处级", "note": "2026年6月区政府官网已更新为区长；领导区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2026年", "end": "present", "rank": "正处级", "note": "兼任"},
    {"person_id": 2, "org_id": 4, "title": "邕宁新兴产业园区管委会主任(兼)", "start": "2026年", "end": "present", "rank": "", "note": "兼任"},
    # 李东平 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": "兼任"},
    # 潘海英 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责工业、商务、住建、交通、生态环境"},
    # 谢晴 — 挂职副区长
    {"person_id": 5, "org_id": 2, "title": "副区长(挂职)", "start": "待查", "end": "present", "rank": "副处级", "note": "挂职干部，广西驻村工作队队长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委(挂职)", "start": "待查", "end": "present", "rank": "副处级", "note": "挂任"},
    {"person_id": 5, "org_id": 5, "title": "广西驻村工作队邕宁区工作队队长", "start": "待查", "end": "present", "rank": "", "note": "负责驻村工作队工作"},
    # 周俊 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责政法、政府法治、综治、国安、信访"},
    # 胡万成 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责农业农村、水利、乡村振兴、民政、文体旅游、退役军人"},
    # 覃苏舜 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责教育、自然资源、卫生健康、市场监管、土地储备"},
    # 陶岳彬 — 前区长
    {"person_id": 9, "org_id": 2, "title": "原区长", "start": "待查", "end": "2025-2026年间", "rank": "正处级", "note": "2025年12月仍以区长身份出席活动，2026年已离任"},
    # 黄壮章 — 人大主任
    {"person_id": 10, "org_id": 3, "title": "人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "城区人大常委会主要负责人"},
]

# 4. Relationships
relationships = [
    # 党政一把手关系
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长党政搭档",
        "overlap_org": "中共南宁市邕宁区委员会",
        "overlap_period": "2026年至今",
        "confirmed": "confirmed",
        "strength": "strong"
    },
    # 区长与前区长关系
    {
        "person_a": 2, "person_b": 9,
        "type": "predecessor_successor",
        "context": "陈国栋接替陶岳彬担任邕宁区区长",
        "overlap_org": "南宁市邕宁区人民政府",
        "overlap_period": "2025-2026年交接",
        "confirmed": "confirmed",
        "strength": "strong"
    },
    # 常务副区长与区长
    {
        "person_a": 3, "person_b": 2,
        "type": "superior_subordinate",
        "context": "李东平为陈国栋的常务副手",
        "overlap_org": "南宁市邕宁区人民政府",
        "overlap_period": "2026年至今",
        "confirmed": "confirmed",
        "strength": "strong"
    },
    # 挂职副区长与区委
    {
        "person_a": 5, "person_b": 1,
        "type": "overlap",
        "context": "谢晴挂任区委常委",
        "overlap_org": "中共南宁市邕宁区委员会",
        "overlap_period": "当前",
        "confirmed": "confirmed",
        "strength": "medium"
    },
    # 党外副区长
    {
        "person_a": 7, "person_b": 1,
        "type": "overlap",
        "context": "胡万成（民建会员）为党外副区长，与区委书记党政关系",
        "overlap_org": "南宁市邕宁区人民政府",
        "overlap_period": "当前",
        "confirmed": "confirmed",
        "strength": "medium"
    },
    # 最年轻副区长
    {
        "person_a": 8, "person_b": 2,
        "type": "superior_subordinate",
        "context": "覃苏舜（1990年生）为最年轻的副区长",
        "overlap_org": "南宁市邕宁区人民政府",
        "overlap_period": "当前",
        "confirmed": "confirmed",
        "strength": "medium"
    },
]


# ── Database ──
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"],
              p["birth"], p["birthplace"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"],
              o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, (r["person_a"], r["person_b"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  ✅ Database: {DB_PATH}")


# ── GEXF ──
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>南宁市邕宁区领导班子工作关系网络</description>')
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
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        role = p["current_post"]
        org = p["current_org"]
        # Color by role
        if "区委书记" in role:
            r, g, b = "255", "50", "50"  # Red
        elif "区长" in role or (("副区长" in role or "常务" in role) and "挂职" not in role):
            r, g, b = "50", "100", "255"  # Blue
        elif "挂职" in role:
            r, g, b = "100", "150", "255"  # Light blue
        elif "人大" in role:
            r, g, b = "200", "255", "255"  # Cyan
        elif "政协" in role:
            r, g, b = "255", "240", "200"  # Cream
        else:
            r, g, b = "100", "100", "100"  # Grey
        # Size
        if "区委书记" in role or "区长" in role:
            sz = "20.0"
        elif "原区长" in role:
            sz = "16.0"
        elif "常委" in role or "常务" in role:
            sz = "14.0"
        else:
            sz = "12.0"

        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    for o in organizations:
        oid = o["id"]
        oname = o["name"]
        otype = o["type"]
        # Color by org type
        color_map = {
            "党委": ("255", "200", "200"),
            "政府": ("200", "200", "255"),
            "开发区": ("200", "255", "200"),
            "乡镇/街道": ("255", "255", "200"),
            "事业单位": ("220", "220", "220"),
            "群团": ("255", "220", "255"),
            "人大": ("200", "255", "255"),
            "政协": ("255", "240", "200"),
        }
        r, g, b = color_map.get(otype, ("200", "200", "200"))
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("parent",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        weight = "2.0" if "区长" in pos["title"] or "书记" in pos["title"] else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person <-> person (relationship)
    for r in relationships:
        eid += 1
        weight = "3.0" if r["strength"] == "strong" else "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✅ GEXF:      {GEXF_PATH}")


# ── Summary ──
def print_summary():
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"  As of:           {AS_OF}")


# ── Main ──
if __name__ == "__main__":
    print("Building 邕宁区 leadership network...")
    build_db()
    build_gexf()
    print_summary()
    print("Done.")
