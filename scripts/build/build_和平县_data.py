#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
和平县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 河源市
Region: 和平县
Targets: 县委书记 & 县长

Research Sources:
- 和平县人民政府门户网站 (www.heping.gov.cn) — 领导之窗
- 和平县新闻中心 — 县委常委会会议/调研报道

Current status (as of 2026-07-22):
- 县委书记: 邓卓文（主持县委全面工作）
- 县长: 张衍彪（县委副书记、县政府党组书记、县长）

Research Date: 2026-07-22
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../")
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "和平县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "和平县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "邓卓文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共和平县委书记",
        "current_org": "中共和平县委员会",
        "source": "http://www.heping.gov.cn/xwzx/jrhp/content/post_709728.html"
    },
    {
        "id": 2,
        "name": "张衍彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-07",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_456648.html"
    },
    {
        "id": 3,
        "name": "李世锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、常务副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_524986.html"
    },
    {
        "id": 4,
        "name": "熊超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-07",
        "birthplace": "",
        "education": "全日制大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_451271.html"
    },
    {
        "id": 5,
        "name": "罗崇文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-03",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长、省'百千万工程'帮扶协作驻和工作队副队长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_592623.html"
    },
    {
        "id": 6,
        "name": "杨碧瑜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984-06",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_548255.html"
    },
    {
        "id": 7,
        "name": "陈君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-05",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_418131.html"
    },
    {
        "id": 8,
        "name": "黄志翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "全日制大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_451270.html"
    },
    {
        "id": 9,
        "name": "彭真平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-03",
        "birthplace": "",
        "education": "全日制大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长、县公安局局长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_433080.html"
    },
    {
        "id": 10,
        "name": "谢智力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "和平县人民政府",
        "source": "http://www.heping.gov.cn/zwgk/ldzc/xzf/content/post_680655.html"
    },
    # ════════════════════════════════════════
    # 其他县领导（从新闻报道中确认）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "涂远泽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "和平县",
        "source": "http://www.heping.gov.cn/xwzx/jrhp/content/post_709728.html"
    },
    {
        "id": 12,
        "name": "谢军伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "和平县",
        "source": "http://www.heping.gov.cn/xwzx/jrhp/content/post_707870.html"
    },
]

organizations = [
    {"id": 1, "name": "中共和平县委员会", "type": "党委", "level": "县处级", "parent": "中共河源市委员会", "location": "广东河源和平县阳明镇"},
    {"id": 2, "name": "和平县人民政府", "type": "政府", "level": "县处级", "parent": "河源市人民政府", "location": "广东河源和平县阳明镇"},
    {"id": 3, "name": "和平县公安局", "type": "政府", "level": "县处级", "parent": "和平县人民政府/河源市公安局", "location": "广东河源和平县"},
]

positions = [
    # ── Deng Zhuowen (邓卓文) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共和平县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，主持县委全面工作"},

    # ── Zhang Yanbiao (张衍彪) ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "和平县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任，自2022年3月已是县长"},
    {"id": 3, "person_id": 2, "org_id": 2, "title": "和平县人民政府党组书记、县长", "start": "2021", "end": "", "rank": "县处级正职", "note": "自2021年起任县长（最早2022年3月政府工作报告）"},

    # ── Li Shifeng (李世锋) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "和平县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 5, "person_id": 3, "org_id": 2, "title": "和平县政府党组副书记、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Xiong Chao (熊超) ──
    {"id": 6, "person_id": 4, "org_id": 1, "title": "和平县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 7, "person_id": 4, "org_id": 2, "title": "和平县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Luo Chongwen (罗崇文) ──
    {"id": 8, "person_id": 5, "org_id": 1, "title": "和平县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 5, "org_id": 2, "title": "和平县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任；省百千万工程帮扶协作工作队副队长"},

    # ── Yang Biyu (杨碧瑜) ──
    {"id": 10, "person_id": 6, "org_id": 2, "title": "和平县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任，九三学社"},

    # ── Chen Jun (陈君) ──
    {"id": 11, "person_id": 7, "org_id": 2, "title": "和平县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Huang Zhixiang (黄志翔) ──
    {"id": 12, "person_id": 8, "org_id": 2, "title": "和平县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Peng Zhenping (彭真平) ──
    {"id": 13, "person_id": 9, "org_id": 2, "title": "和平县政府党组成员、副县长、县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 14, "person_id": 9, "org_id": 3, "title": "和平县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Xie Zhili (谢智力) ──
    {"id": 15, "person_id": 10, "org_id": 2, "title": "和平县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Tu Yuanze (涂远泽) ──
    {"id": 16, "person_id": 11, "org_id": 1, "title": "和平县领导（推测为县委领导）", "start": "", "end": "", "rank": "", "note": "新闻报道中提及"},

    # ── Xie Junwei (谢军伟) ──
    {"id": 17, "person_id": 12, "org_id": 1, "title": "和平县领导（推测为县委领导）", "start": "", "end": "", "rank": "", "note": "新闻报道中提及"},
]

relationships = [
    # ── Party Secretary - County Mayor (党政搭档) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "邓卓文任县委书记，张衍彪任县长，为和平县党政正职搭档", "overlap_org": "中共和平县委员会/和平县人民政府", "overlap_period": "至今"},

    # ── Standing Committee coworkers ──
    {"id": 2, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "李世锋与熊超均为和平县委常委", "overlap_org": "中共和平县委员会", "overlap_period": ""},
    {"id": 3, "person_a_id": 3, "person_b_id": 5, "type": "同僚", "context": "李世锋与罗崇文均为和平县委常委", "overlap_org": "中共和平县委员会", "overlap_period": ""},
    {"id": 4, "person_a_id": 4, "person_b_id": 5, "type": "同僚", "context": "熊超与罗崇文均为和平县委常委", "overlap_org": "中共和平县委员会", "overlap_period": ""},

    # ── Government colleagues ──
    {"id": 5, "person_a_id": 6, "person_b_id": 7, "type": "同僚", "context": "杨碧瑜与陈君均为和平县政府领导", "overlap_org": "和平县人民政府", "overlap_period": ""},
    {"id": 6, "person_a_id": 7, "person_b_id": 8, "type": "同僚", "context": "陈君与黄志翔均为和平县政府领导", "overlap_org": "和平县人民政府", "overlap_period": ""},
    {"id": 7, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "黄志翔与彭真平均为和平县政府领导", "overlap_org": "和平县人民政府", "overlap_period": ""},
    {"id": 8, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "彭真平与谢智力均为和平县政府领导", "overlap_org": "和平县人民政府", "overlap_period": ""},
    {"id": 9, "person_a_id": 6, "person_b_id": 10, "type": "同僚", "context": "杨碧瑜与谢智力均为和平县政府领导", "overlap_org": "和平县人民政府", "overlap_period": ""},

    # ── 上下级 (superior-subordinate) ──
    {"id": 10, "person_a_id": 1, "person_b_id": 3, "type": "上下级", "context": "邓卓文作为县委书记领导县委常委李世锋", "overlap_org": "中共和平县委员会", "overlap_period": ""},
    {"id": 11, "person_a_id": 2, "person_b_id": 3, "type": "上下级", "context": "张衍彪作为县长主持县政府全面工作，李世锋为常务副县长协助县长工作", "overlap_org": "和平县人民政府", "overlap_period": ""},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
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
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>和平县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    # Color by role
    if p["id"] == 1:
        # Party Secretary — red
        r, g, b = 255, 50, 50
        size = 20.0
    elif p["id"] == 2:
        # County Mayor — blue
        r, g, b = 50, 100, 255
        size = 20.0
    elif p["id"] in [3, 4, 5]:
        # Standing Committee — orange
        r, g, b = 255, 165, 0
        size = 12.0
    elif p["id"] == 9:
        # Police chief — orange
        r, g, b = 255, 165, 0
        size = 12.0
    else:
        # Others — grey
        r, g, b = 100, 100, 100
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_colors = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
}
for o in organizations:
    oid = 1000 + o["id"]
    cr, cg, cb = org_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{cr}" g="{cg}" b="{cb}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(pos["start"] or "?")} → {esc(pos["end"] or "今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
