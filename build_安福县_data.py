#!/usr/bin/env python3
"""
安福县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Anfu County leadership.

Research date: 2026-07-15
Data sourced from:
  - https://www.afx.gov.cn/ (安福县人民政府官网)
  - 新闻稿件及会议报道 (2026年6月-7月)

Confirmed current leaders (as of 2026-07-15):
  - 谢启龙 — 县委书记、安福武功山风景名胜区党工委书记（兼）
  - 华桦 — 县委副书记、县人民政府县长（截至2026-07-01仍任）
  - 范毅 — 县委副书记、县长候选人（2026-07-07以该身份主持县政府常务会议）
  - 彭少峥 — 县委副书记
  - 11名县委常委 + 多名副县长
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "安福县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "安福县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""


# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# Person ID convention: anfu_{surname_givenname}
# ── Persons ──
# Fields: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

PERSONS = [
    # ═══ Top Leaders ═══

    # 县委书记 — 谢启龙
    # Source: afx.gov.cn 县委书记领导之窗 (2026-06-04更新)
    ("anfu_xie_qilong", "谢启龙", "男", "汉族", "1973-02", "待查", "省委党校研究生学历", "中共党员", "待查",
     "县委书记、安福武功山风景名胜区党工委书记（兼）", "中共安福县委",
     "https://www.afx.gov.cn/afxrmzfw/xwsj/content/content_1895702555458994176.html"),

    # 县长 — 华桦
    # Source: afx.gov.cn 县长领导之窗 (2026-06-04更新)
    # NOTE: 2026-07-07 会议显示范毅为县长候选人，可能存在华桦离任或分工调整
    ("anfu_hua_hua", "华桦", "男", "汉族", "1981-10", "待查", "大学学历、企业管理硕士", "中共党员", "待查",
     "县委副书记、县人民政府县长", "安福县人民政府",
     "https://www.afx.gov.cn/afxrmzfw/xz/content/content_1897141734155943936.html"),

    # 县长候选人 — 范毅
    # Source: 十四届县委第112次常委会会议 (2026-07-09)
    # 受县委书记谢启龙委托，范毅以县委副书记、县长候选人身份主持会议
    ("anfu_fan_yi", "范毅", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、县长候选人", "安福县人民政府",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-07) — 以县委副书记、县长候选人身份主持会议"),

    # ═══ 县委副书记 ═══

    # 彭少峥 — 县委副书记
    ("anfu_peng_shaozheng", "彭少峥", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09) — 列名在范毅之后"),

    # ═══ 县委常委 ═══

    # 肖小军 — 县委常委
    ("anfu_xiao_xiaojun", "肖小军", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09)"),

    # 肖前明 — 县委常委
    ("anfu_xiao_qianming", "肖前明", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09)"),

    # 戴智堂 — 县委常委、常务副县长
    ("anfu_dai_zhtang", "戴智堂", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "安福县人民政府",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09); 县十七届政府第48次常务会议(2026-06-13)"),

    # 刘忠健 — 县委常委、副县长
    ("anfu_liu_zhongjian", "刘忠健", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、副县长", "安福县人民政府",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09); 县十七届政府第48次常务会议(2026-06-13)"),

    # 刘庆文 — 县委常委
    ("anfu_liu_qingwen", "刘庆文", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09)"),

    # 王煜 — 县委常委
    ("anfu_wang_yu", "王煜", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09)"),

    # 熊亮 — 县委常委
    ("anfu_xiong_liang", "熊亮", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委", "中共安福县委",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09)"),

    # ═══ 副县长 ═══

    # 罗小群 — 副县长
    ("anfu_luo_xiaoqun", "罗小群", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "安福县人民政府",
     "afx.gov.cn 县十七届政府第48次常务会议(2026-06-13)"),

    # 刘佳 — 副县长
    ("anfu_liu_jia", "刘佳", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "安福县人民政府",
     "afx.gov.cn 县十七届政府第48次常务会议(2026-06-13)"),

    # 章彬赣 — 副县长
    ("anfu_zhang_bingan", "章彬赣", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "安福县人民政府",
     "afx.gov.cn 县十七届政府第48次常务会议(2026-06-13)"),

    # 李英 — 副县长
    ("anfu_li_ying", "李英", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "安福县人民政府",
     "afx.gov.cn 县十七届政府第48次常务会议(2026-06-13)"),

    # ═══ 人大、政协领导 ═══

    # 童熙平 — 县人大常委会主任
    ("anfu_tong_xiping", "童熙平", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "安福县人民代表大会常务委员会",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09) — 列席"),

    # 罗德才 — 县政协主席
    ("anfu_luo_decai", "罗德才", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议安福县委员会",
     "afx.gov.cn 十四届县委第112次常委会会议(2026-07-09) — 列席"),
]

# ── Organizations ──
# Fields: (id, name, type, level, parent, location)

ORGANIZATIONS = [
    (1, "中共安福县委", "党委", "县级", "中共吉安市委", "江西省吉安市安福县"),
    (2, "安福县人民政府", "政府", "县级", "吉安市人民政府", "江西省吉安市安福县"),
    (3, "安福县人民代表大会常务委员会", "人大", "县级", "安福县", "江西省吉安市安福县"),
    (4, "中国人民政治协商会议安福县委员会", "政协", "县级", "安福县", "江西省吉安市安福县"),
    (5, "中共安福县纪律检查委员会", "纪律检查", "县级", "中共吉安市纪委", "江西省吉安市安福县"),
    (6, "中共安福县委组织部", "党委部门", "县级", "中共安福县委", "江西省吉安市安福县"),
    (7, "中共安福县委宣传部", "党委部门", "县级", "中共安福县委", "江西省吉安市安福县"),
    (8, "中共安福县委政法委员会", "党委部门", "县级", "中共安福县委", "江西省吉安市安福县"),
    (9, "中共安福县委统一战线工作部", "党委部门", "县级", "中共安福县委", "江西省吉安市安福县"),
    (10, "安福县人民武装部", "军事", "县级", "吉安军分区", "江西省吉安市安福县"),
    (11, "安福武功山风景名胜区", "事业单位", "县级", "安福县人民政府", "江西省吉安市安福县"),
]

# ── Positions ──
# Fields: (person_id, org_id, title, start, end, rank, note)

POSITIONS_DATA = [
    # 谢启龙
    (0, 0, "县委书记", "待查", "present", "正县级", "同时兼任安福武功山风景名胜区党工委书记"),
    (0, 10, "县人武部党委第一书记", "待查", "present", "正县级", ""),
    (0, 10, "安福武功山风景名胜区党工委书记（兼）", "待查", "present", "正县级", ""),

    # 华桦
    (1, 1, "县委副书记、县长", "待查", "present", "正县级", "负责县政府全面工作兼管审计；截至2026-07-01仍以县长身份活动"),

    # 范毅
    (2, 1, "县委副书记、县长候选人", "~2026-07", "present", "正县级", "2026-07-07以县长候选人身份受委托主持县委常委会"),

    # 彭少峥
    (3, 0, "县委副书记（专职）", "待查", "present", "副县级", ""),

    # 肖小军
    (4, 0, "县委常委", "待查", "present", "副县级", ""),

    # 肖前明
    (5, 0, "县委常委", "待查", "present", "副县级", ""),

    # 戴智堂
    (6, 1, "县委常委、常务副县长", "待查", "present", "副县级", ""),

    # 刘忠健
    (7, 1, "县委常委、副县长", "待查", "present", "副县级", ""),

    # 刘庆文
    (8, 0, "县委常委", "待查", "present", "副县级", ""),

    # 王煜
    (9, 0, "县委常委", "待查", "present", "副县级", ""),

    # 熊亮
    (10, 0, "县委常委", "待查", "present", "副县级", ""),

    # 罗小群
    (11, 1, "副县长", "待查", "present", "副县级", ""),

    # 刘佳
    (12, 1, "副县长", "待查", "present", "副县级", ""),

    # 章彬赣
    (13, 1, "副县长", "待查", "present", "副县级", ""),

    # 李英
    (14, 1, "副县长", "待查", "present", "副县级", ""),

    # 童熙平
    (15, 2, "县人大常委会主任", "待查", "present", "正县级", ""),

    # 罗德才
    (16, 3, "县政协主席", "待查", "present", "正县级", ""),
]

# ── Relationships ──
# Fields: (person_a, person_b, type, context, overlap_org, overlap_period)

RELATIONSHIPS = [
    # 谢启龙 ↔ 华桦：党政一把手搭档
    (0, 1, "党政搭档", "县委书记与县长，共同主持县委和县政府全面工作", "中共安福县委/安福县人民政府", "2026"),
    # 谢启龙 ↔ 范毅：交接关系
    (0, 2, "上下级/交接关系", "县委书记与县长候选人", "中共安福县委", "2026-07"),
    # 谢启龙 ↔ 彭少峥：上下级
    (3, 0, "上下级", "县委书记与县委副书记", "中共安福县委", "2026"),
    # 谢启龙 ↔ 肖小军：上下级
    (4, 0, "上下级", "县委书记与县委常委", "中共安福县委", "2026"),
    # 谢启龙 ↔ 肖前明：上下级
    (5, 0, "上下级", "县委书记与县委常委", "中共安福县委", "2026"),
    # 谢启龙 ↔ 戴智堂：上下级
    (6, 0, "上下级", "县委书记与常务副县长", "中共安福县委", "2026"),
    # 谢启龙 ↔ 刘忠健：上下级
    (7, 0, "上下级", "县委书记与副县长", "中共安福县委", "2026"),
    # 谢启龙 ↔ 刘庆文：上下级
    (8, 0, "上下级", "县委书记与县委常委", "中共安福县委", "2026"),
    # 谢启龙 ↔ 王煜：上下级
    (9, 0, "上下级", "县委书记与县委常委", "中共安福县委", "2026"),
    # 谢启龙 ↔ 熊亮：上下级
    (10, 0, "上下级", "县委书记与县委常委", "中共安福县委", "2026"),
    # 华桦 ↔ 范毅：前后任
    (1, 2, "前后任关系", "华桦为原县长（截至2026-07-01），范毅为县长候选人（2026-07-07）", "安福县人民政府", "2026-07"),
    # 戴智堂 ↔ 刘忠健：政府工作搭档
    (6, 7, "工作搭档", "常务副县长与副县长，共同负责县政府工作", "安福县人民政府", "2026"),
    # 戴智堂 ↔ 罗小群：政府工作搭档
    (6, 11, "工作搭档", "常务副县长与副县长", "安福县人民政府", "2026"),
    # 范毅 ↔ 彭少峥：工作搭档
    (2, 3, "工作搭档", "两位县委副书记共同出席县委常委会", "中共安福县委", "2026-07"),
    # 童熙平 ↔ 罗德才：人大政协协同
    (15, 16, "人大政协协同", "人大主任与政协主席，列席县委常委会", "安福县", "2026"),
]


# ══════════════════════════════════════════════════════════════════════
# BUILD SQLite
# ══════════════════════════════════════════════════════════════════════

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
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
            source TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for i, p in enumerate(PERSONS):
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (i, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))

    for o in ORGANIZATIONS:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pi, pos in enumerate(POSITIONS_DATA):
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pi, pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6]))

    for ri, r in enumerate(RELATIONSHIPS):
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ri, r[0], r[1], r[2], r[3], r[4], r[5]))

    conn.commit()

    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()
    print(f"✓ SQLite DB created: {DB_PATH}")


# ══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ══════════════════════════════════════════════════════════════════════

def person_color(p):
    """Return color string based on role."""
    post = p[9]
    if "县委书记" in post or "第一书记" in post:
        return "255,50,50"  # Red — Party Secretary
    elif "县长" in post or "副县长" in post:
        return "50,100,255"  # Blue — Government
    elif "纪委书记" in post:
        return "255,165,0"  # Orange — Discipline
    elif "人大常委会主任" in post:
        return "200,255,255"  # Cyan — People's Congress
    elif "政协主席" in post:
        return "255,240,200"  # Cream — CPPCC
    else:
        return "100,100,100"  # Grey — Others


def org_color(o):
    """Return color string based on org type."""
    t = o[2]
    if "党委" in t:
        return "255,200,200"  # Pink
    elif "政府" in t:
        return "200,200,255"  # Light blue
    elif "人大" in t:
        return "200,255,255"  # Cyan
    elif "政协" in t:
        return "255,240,200"  # Cream
    elif "纪律" in t:
        return "255,220,255"  # Light purple
    elif "开发区" in t:
        return "200,255,200"  # Light green
    elif "军事" in t:
        return "220,220,220"  # Light grey
    elif "事业" in t:
        return "220,220,220"  # Light grey
    else:
        return "200,200,200"


def is_top_leader(p):
    post = p[9]
    return "县委书记" in post or ("县长" in post and "副" not in post)


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>安福县领导班子工作关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for i, p in enumerate(PERSONS):
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{i}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    for o in ORGANIZATIONS:
        c = org_color(o)
        lines.append(f'      <node id="o{o[0]}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o[1])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    edge_id = 0
    lines.append('    <edges>')

    # Person → Organization (worked_at)
    for pos in POSITIONS_DATA:
        lines.append(f'      <edge id="e{edge_id}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        lines.append(f'      <edge id="e{edge_id}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Building 安福县 network data...")
    build_db()
    build_gexf()
    print(f"\nSummary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS_DATA)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print("Done.")
