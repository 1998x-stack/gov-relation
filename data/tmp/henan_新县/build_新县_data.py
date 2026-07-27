#!/usr/bin/env python3
"""
新县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Xin County (新县) leadership.

Research as of 2026-07-25:
- 县委书记: 李晓亮 (since 2025.04, previously 县长 2021.10-2025.04)
- 县长: 朱国朋 (appointed 2025.11 as 县委副书记/县政府党组书记, 2025.12 县长)
- 前任县委书记: 夏明夫 (2021.07-2025.02, 调任信阳市人大常委会副主任)
- 前任县长: 李晓亮 (2021.10-2025.04, 升任县委书记)

Government leadership (from hnxx.gov.cn):
- 许呈林: 县委常委、常务副县长
- 孙巧: 县委常委、宣传部部长、副县长
- 汤勇: 副县长 (农业农村)
- 王超峰: 副县长、公安局局长
- 李勍: 副县长 (女, 豫东南飞地建设)
- 李道勇: 副县长、县政府机关党组书记、办公室主任
- 钱晓青: 副县长、科技局局长 (女, 无党派)
"""

import sqlite3
import os
import json
import sys
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "新县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "新县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── Person ID convention: xinxian_{surname_givenname} ──

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 李晓亮
    # Source: hnxx.gov.cn leadership page; Baidu Baike; 河南日报(2025-04-03)
    # 2021.10 当选县长, 2025.03 拟任县委书记公示, 2025.04 已任县委书记
    ("xinxian_li_xiaoliang", "李晓亮", "男", "汉族", "1975-09", "待查", "大学/文学学士",
     "中共党员", "待查",
     "县委书记", "中共新县委员会",
     "新县人民政府 https://www.hnxx.gov.cn/; 河南日报 https://www.henan.gov.cn/ — 李晓亮已任新县县委书记(2025-04-03); 百度百科"),

    # 县长 — 朱国朋
    # Source: hnxx.gov.cn leadership page; 鲁网/汲古新知 (2025-11-23)
    # "墩苗"干部, 原信阳师范学院团委副书记 → 商城县委副书记/汪桥镇党委书记 → 豫东南高新区 → 新县
    ("xinxian_zhu_guopeng", "朱国朋", "男", "汉族", "1983-06", "待查", "研究生/法学硕士",
     "中共党员", "待查",
     "县委副书记、县长", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2024/08-01/158457.html; 鲁网 — '墩苗'干部朱国朋新职公布(2025-11-23)"),

    # ═══ 常务副县长 ═══

    # 许呈林 — 县委常委、常务副县长
    # Source: hnxx.gov.cn leadership page
    ("xinxian_xu_chenglin", "许呈林", "男", "汉族", "1985-06", "待查", "研究生",
     "中共党员", "待查",
     "县委常委、常务副县长", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2024/08-01/158456.html"),

    # ═══ 其他副县长 ═══

    # 孙巧 — 县委常委、宣传部部长、副县长
    ("xinxian_sun_qiao", "孙巧", "女", "汉族", "1987-09", "待查", "研究生/管理学硕士",
     "中共党员", "待查",
     "县委常委、宣传部部长、副县长", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2026/06-24/791972.html"),

    # 汤勇 — 副县长 (农业农村、水利、林业)
    ("xinxian_tang_yong", "汤勇", "男", "汉族", "1982-09", "待查", "研究生",
     "中共党员", "待查",
     "副县长", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2024/06-05/158459.html"),

    # 王超峰 — 副县长、公安局局长
    ("xinxian_wang_chaofeng", "王超峰", "男", "汉族", "1978-10", "待查", "研究生/法学硕士",
     "中共党员", "待查",
     "副县长、县公安局局长", "新县公安局",
     "新县人民政府 https://www.hnxx.gov.cn/2024/06-05/158455.html"),

    # 李勍 — 副县长 (女, 豫东南飞地建设)
    ("xinxian_li_qing", "李勍", "女", "汉族", "1989-10", "待查", "研究生/工商管理硕士",
     "中共党员", "待查",
     "副县长", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2024/07-29/158462.html"),

    # 李道勇 — 副县长、县政府机关党组书记、办公室主任
    ("xinxian_li_daoyong", "李道勇", "男", "汉族", "1983-02", "待查", "大学",
     "中共党员", "待查",
     "副县长、县政府机关党组书记、办公室主任", "新县人民政府",
     "新县人民政府 https://www.hnxx.gov.cn/2026/06-24/791976.html"),

    # 钱晓青 — 副县长、科技局局长 (女, 无党派)
    ("xinxian_qian_xiaoqing", "钱晓青", "女", "汉族", "1982-09", "待查", "研究生",
     "无党派", "待查",
     "副县长、县科学技术局局长", "新县科学技术局",
     "新县人民政府 https://www.hnxx.gov.cn/2026/06-24/791980.html"),

    # ═══ Predecessors ═══

    # 前任县委书记 — 夏明夫
    # Source: Baidu Baike — 夏明夫
    # 息县人, 1966.09, 郑州大学经济学, 1989年工作
    # 信阳高压开关总厂 → 共青团信阳市委 → 市直机关工委 → 淮滨县委常委/县纪委书记/常务副县长
    # → 潢川县委副书记 → 新县县长 → 新县县委书记 → 信阳市人大副主任
    ("xinxian_xia_mingfu", "夏明夫", "男", "汉族", "1966-09", "河南息县", "大学/经济学",
     "1988-05", "1989-07",
     "信阳市人大常委会副主任（原新县县委书记）", "信阳市人民代表大会常务委员会",
     "百度百科 https://baike.baidu.com/item/%E5%A4%8F%E6%98%8E%E5%A4%AB; 新县人民政府网(2017-05-04)"),
]

# ── Organizations ──
# (id, name, type, level, parent, location)

ORGANIZATIONS = [
    (1, "中共新县委员会", "党委", "县级", "中共信阳市委", "河南省信阳市新县"),
    (2, "新县人民政府", "政府", "县级", "信阳市人民政府", "河南省信阳市新县"),
    (3, "新县公安局", "政府", "县级", "新县人民政府", "河南省信阳市新县"),
    (4, "新县科学技术局", "政府", "县级", "新县人民政府", "河南省信阳市新县"),
    (5, "信阳市人民代表大会常务委员会", "人大", "地市级", "信阳市人民代表大会", "河南省信阳市"),
]

# ── Positions ──
# (person_id, org_id, title, start_date, end_date, rank, note)

POSITIONS = [
    # 李晓亮
    ("xinxian_li_xiaoliang", 1, "县委书记、县人武部党委第一书记", "2025-04", "至今", "正处级", "2025.04 由县长转任县委书记"),
    ("xinxian_li_xiaoliang", 2, "县委副书记、县长", "2021-10", "2025-04", "正处级", "2021.10 当选新县人民政府县长"),
    # 朱国朋
    ("xinxian_zhu_guopeng", 2, "县委副书记、县长、县政府党组书记", "2025-11", "至今", "正处级", "2025.11 任县委副书记、县政府党组书记; '墩苗'干部"),
    # 许呈林
    ("xinxian_xu_chenglin", 2, "县委常委、常务副县长", "2024", "至今", "副处级", "负责县政府常务工作"),
    # 孙巧
    ("xinxian_sun_qiao", 2, "县委常委、宣传部部长、副县长", "2026", "至今", "副处级", "负责宣传、文旅、交通"),
    # 汤勇
    ("xinxian_tang_yong", 2, "副县长", "2024", "至今", "副处级", "负责农业农村、水利、林业"),
    # 王超峰
    ("xinxian_wang_chaofeng", 3, "副县长、县公安局党委书记、局长", "2024", "至今", "副处级", "负责公安、司法、信访"),
    # 李勍
    ("xinxian_li_qing", 2, "副县长", "2024", "至今", "副处级", "负责豫东南飞地建设"),
    # 李道勇
    ("xinxian_li_daoyong", 2, "副县长、县政府机关党组书记、办公室主任", "2026", "至今", "副处级", "负责环保、住建、城管"),
    # 钱晓青
    ("xinxian_qian_xiaoqing", 4, "副县长、县科学技术局局长", "2026", "至今", "副处级", "负责教育、民政、人社、卫健、医保"),
    # 夏明夫
    ("xinxian_xia_mingfu", 5, "信阳市人大常委会副主任", "2025-02", "至今", "副厅级", "2025.02 当选信阳市人大副主任"),
    ("xinxian_xia_mingfu", 1, "县委书记", "2021-07", "2025-02", "正处级", "2021.07 任新县县委书记"),
    ("xinxian_xia_mingfu", 2, "县委副书记、县长", "2016-09", "2021-07", "正处级", "2016.09 任代县长, 2017.04 当选县长"),
]

# ── Relationships ──
# (person_a, person_b, type, context, overlap_org, overlap_period)

RELATIONSHIPS = [
    # 李晓亮 ↔ 夏明夫（前后任书记）
    ("xinxian_li_xiaoliang", "xinxian_xia_mingfu", "predecessor_successor",
     "李晓亮接替夏明夫任新县县委书记", "中共新县委员会", "2025.04"),
    # 李晓亮 ↔ 夏明夫（上下级：县长→书记）
    ("xinxian_li_xiaoliang", "xinxian_xia_mingfu", "superior_subordinate",
     "夏明夫任县委书记时, 李晓亮任县长", "中共新县委员会/新县人民政府", "2021.10-2025.02"),
    # 李晓亮 ↔ 朱国朋（前后任县长）
    ("xinxian_li_xiaoliang", "xinxian_zhu_guopeng", "predecessor_successor",
     "朱国朋接替李晓亮任新县县长", "新县人民政府", "2025.11"),
    # 朱国朋 ↔ 许呈林（上下级：县长→常务副县长）
    ("xinxian_zhu_guopeng", "xinxian_xu_chenglin", "superior_subordinate",
     "朱国朋任县长, 许呈林为常务副县长协助工作", "新县人民政府", "2025.11-至今"),
    # 许呈林 ↔ 汤勇（同事：政府班子）
    ("xinxian_xu_chenglin", "xinxian_tang_yong", "overlap",
     "同为新县人民政府班子成员", "新县人民政府", "2024-至今"),
    # 王超峰 ↔ 许呈林（同事：政府班子, 应急管理分工关联）
    ("xinxian_wang_chaofeng", "xinxian_xu_chenglin", "overlap",
     "王超峰协管应急管理, 协助许呈林", "新县人民政府", "2024-至今"),
]

# ── Helper: build person_id→integer mapping ──
def make_id_map(persons):
    return {p[0]: i+1 for i, p in enumerate(persons)}

PID = make_id_map(PERSONS)
ORG_IDS = {o[0]: i+1 for i, o in enumerate(ORGANIZATIONS)}

# ── Database ──
def create_tables(conn):
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")
    conn.executescript("""
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
    conn.commit()

def build_db():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in PERSONS:
        vals = dict(zip(cols_p, [PID[p[0]], p[1], p[2], p[3], p[4], p[5], p[6],
                                 p[7], p[8], p[9], p[10], p[11]]))
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})",
                     [vals[c] for c in cols_p])

    cols_o = ["id","name","type","level","parent","location"]
    for o in ORGANIZATIONS:
        vals = dict(zip(cols_o, [ORG_IDS[o[0]], o[1], o[2], o[3], o[4], o[5]]))
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})",
                     [vals[c] for c in cols_o])

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in POSITIONS:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})",
                     [PID.get(pos[0], 0), ORG_IDS.get(pos[1], 0), pos[2], pos[3], pos[4], pos[5], pos[6]])

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in RELATIONSHIPS:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})",
                     [PID.get(r[0], 0), PID.get(r[1], 0), r[2], r[3], r[4], r[5]])

    conn.commit()
    conn.close()

# ── GEXF ──
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>新县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    def person_color(post):
        if "书记" in post and "县委" in post:
            return "255,50,50"
        if "县长" in post:
            return "50,100,255"
        return "100,100,100"

    def person_size(post):
        if "书记" in post and "县委" in post:
            return "20.0"
        if "县长" in post:
            return "20.0"
        return "12.0"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
        }
        return colors.get(otype, "200,200,200")

    # Person nodes
    for p in PERSONS:
        pid, name, _, _, birth, _, _, _, _, post, org, source = p
        c = person_color(post)
        sz = person_size(post)
        lines.append(f'      <node id="p{PID[pid]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(source[:80])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, _, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{ORG_IDS[oid]}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(level)}"/>')
        lines.append(f'          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{PID.get(pos[0], 0)}" target="o{ORG_IDS.get(pos[1], 0)}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos[3])}~{esc(pos[4])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person relationships
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{PID.get(r[0], 0)}" target="p{PID.get(r[1], 0)}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r[5])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──
def main():
    print(f"Building database: {DB_PATH}")
    build_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    print(f"  Persons: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Organizations: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    print(f"  Positions: {cur.fetchone()[0]}")
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Relationships: {cur.fetchone()[0]}")
    conn.close()

    print(f"Building GEXF: {GEXF_PATH}")
    build_gexf()
    print(f"  GEXF size: {os.path.getsize(GEXF_PATH)} bytes")

    print("Done.")

if __name__ == "__main__":
    main()
