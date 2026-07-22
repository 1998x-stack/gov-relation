#!/usr/bin/env python3
"""
泰和县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Taihe County leadership.

Research date: 2026-07-15
Data sourced from:
  - https://www.jxth.gov.cn/ (泰和县人民政府官网)
  - 新闻稿件及会议报道 (2026年6月-7月)

Confirmed current leaders (as of 2026-07-15):
  - 巫太明 — 县委书记、县人武部党委第一书记
  - 李艳辉 — 县委副书记、县长候选人 (原泰和县工作经历)
  - 廖文来 — 前任县长 (2026年6月仍在履职，此后离任)
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "泰和县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "泰和县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""


# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# Person ID convention: taihe_{surname_givenname}
# ── Persons ──
# Fields: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

PERSONS = [
    # ═══ Top Leaders ═══

    # 县委书记 — 巫太明
    # Source: jxth.gov.cn multiple news articles (2026-06 to 2026-07)
    ("taihe_wu_taiming", "巫太明", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共泰和县委员会",
     "jxth.gov.cn 人武部党委第一书记任职大会(2026-06-24); 全县重点项目建设推进会(2026-07-08); 教育工作调研(2026-07-14)"),

    # 县长候选人 — 李艳辉
    # Source: jxth.gov.cn multiple news articles
    # Note: 李艳辉曾于泰和工作，后调离，2026年7月以县委副书记、县长候选人身份返回泰和
    ("taihe_li_yanhui", "李艳辉", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、县长候选人", "泰和县人民政府",
     "jxth.gov.cn 走访慰问退休老干部(2026-07-04); 河西片区乡镇调研(2026-07-07); 重点项目建设推进会(2026-07-08); 深入乡镇调研重点工作(2026-07-13)"),

    # ═══ Standing Committee (县委常委) ═══

    # 前任县长 — 廖文来 (2026年6月仍在位，此后离任)
    ("taihe_liao_wenlai", "廖文来", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "（原县长）", "泰和县人民政府",
     "jxth.gov.cn 全县工业和开放型经济高质量发展暨招商引资工作动员会(2026-06-02) — 主持会议并部署工作"),

    # 县委副书记（专职）
    ("taihe_fan_yi", "范毅", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "（原县委副书记/关键领导）", "中共泰和县委员会",
     "jxth.gov.cn 工业和开放型经济动员会(2026-06-02) — 排名在县委书记巫太明之后、县人大主任曾向荣之前"),

    # 县人大常委会主任
    ("taihe_zeng_xiangrong", "曾向荣", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "泰和县人民代表大会常务委员会",
     "jxth.gov.cn 重点项目建设推进会(2026-07-08); 工业和开放型经济动员会(2026-06-02)"),

    # 县政协主席/县领导
    ("taihe_wang_zhihong", "王志宏", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县领导（推测政协主席或县委副书记）", "泰和县",
     "jxth.gov.cn 多次会议报道 — 排名在曾向荣之后"),

    # 县委常委、政法委书记
    ("taihe_xia_delie", "夏得烈", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、政法委书记", "中共泰和县委政法委员会",
     "jxth.gov.cn 重点项目建设推进会(2026-07-08); 工业和开放型经济动员会(2026-06-02)"),

    # 县领导
    ("taihe_lin_mei", "林梅", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县领导（推测副县长或宣传/统战部长）", "泰和县人民政府",
     "jxth.gov.cn 工业和开放型经济动员会(2026-06-02)"),

    # 县委常委、常务副县长
    ("taihe_luo_keshuai", "罗克帅", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "泰和县人民政府",
     "jxth.gov.cn 重点项目建设推进会(2026-07-08); 人武部会议(2026-06-24); 工业和开放型经济动员会(2026-06-02)"),

    # 县委常委、组织部部长
    ("taihe_xu_qinghua", "徐庆华", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、组织部部长", "中共泰和县委组织部",
     "jxth.gov.cn 走访慰问退休老干部(2026-07-04); 重点项目建设推进会(2026-07-08) — 通报干部工作"),

    # 县委常委、宣传部部长
    ("taihe_ge_yingcai", "葛英才", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共泰和县委宣传部",
     "jxth.gov.cn 教育工作调研(2026-07-14) — 陪同巫太明调研并提及职务; 重点项目建设推进会(2026-07-08)"),

    # 县领导
    ("taihe_yang_haitao", "杨海涛", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县领导（推测副县长）", "泰和县人民政府",
     "jxth.gov.cn 重点项目建设推进会(2026-07-08)"),

    # 县领导
    ("taihe_chen_lili", "陈李丽", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县领导（推测统战部长或副县长）", "泰和县人民政府",
     "jxth.gov.cn 重点项目建设推进会(2026-07-08)"),

    # 县委常委、人武部部长
    ("taihe_lou_jiangbo", "娄江波", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、人武部部长", "泰和县人民武装部",
     "jxth.gov.cn 人武部党委第一书记任职大会(2026-06-24) — 主持会议"),

    # 副县长、泰和高新区党工委书记
    ("taihe_hu_jianqiong", "胡建琼", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长、泰和高新区党工委书记", "泰和县人民政府 / 泰和高新技术产业园区",
     "jxth.gov.cn 工业和开放型经济动员会(2026-06-02) — 通报工作并部署"),

    # 副县长（分管教育）
    ("taihe_liao_xin", "廖欣", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "泰和县人民政府",
     "jxth.gov.cn 教育工作调研(2026-07-14) — 陪同巫太明调研教育"),

    # 县领导（其他副县级）
    ("taihe_other_01", "（待确认—副县级领导）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县级领导", "泰和县",
     "⚠️ 会议报道提及'在家的县四套班子领导及其他副县级以上领导' — 具体姓名需从领导之窗页面确认"),
]

# ── Organizations ──
# Fields: (id, name, type, level, parent, location)

ORGANIZATIONS = [
    (1, "中共泰和县委员会", "党委", "县级", "中共吉安市委", "江西省吉安市泰和县"),
    (2, "泰和县人民政府", "政府", "县级", "吉安市人民政府", "江西省吉安市泰和县"),
    (3, "泰和县人民代表大会常务委员会", "人大", "县级", "泰和县", "江西省吉安市泰和县"),
    (4, "中国人民政治协商会议泰和县委员会", "政协", "县级", "泰和县", "江西省吉安市泰和县"),
    (5, "中共泰和县纪律检查委员会", "纪律检查", "县级", "中共吉安市纪委", "江西省吉安市泰和县"),
    (6, "中共泰和县委组织部", "党委部门", "县级", "中共泰和县委员会", "江西省吉安市泰和县"),
    (7, "中共泰和县委宣传部", "党委部门", "县级", "中共泰和县委员会", "江西省吉安市泰和县"),
    (8, "中共泰和县委政法委员会", "党委部门", "县级", "中共泰和县委员会", "江西省吉安市泰和县"),
    (9, "中共泰和县委统一战线工作部", "党委部门", "县级", "中共泰和县委员会", "江西省吉安市泰和县"),
    (10, "泰和县人民武装部", "军事", "县级", "吉安军分区", "江西省吉安市泰和县"),
    (11, "泰和高新技术产业园区", "开发区", "县级", "泰和县人民政府", "江西省吉安市泰和县"),
]

# ── Positions ──
# Fields: (person_id, org_id, title, start, end, rank, note)
# Using integer position IDs to match PERSONS/ORGANIZATIONS dict format below

POSITIONS_DATA = [
    # 巫太明
    (0, 0, "县委书记", "2026-06前", "present", "正县级", "同时兼任县人武部党委第一书记"),
    (0, 9, "县人武部党委第一书记", "2026-06-24", "present", "正县级", "吉安军分区党委任职通知"),

    # 李艳辉
    (1, 1, "县委副书记、县长候选人", "2026-07初", "present", "正县级", "曾于泰和工作，后调离，现返回任职"),

    # 廖文来
    (2, 1, "县长", "—2026-06", "—2026-06离任", "正县级", "2026年6月初仍在主持政府工作，此后离任"),

    # 范毅
    (3, 0, "县委副书记（或常务领导）", "待查", "待查", "副县级", "排名在县委书记后、人大主任前"),

    # 曾向荣
    (4, 2, "县人大常委会主任", "待查", "present", "正县级", ""),

    # 王志宏
    (5, 3, "县领导（推测县政协主席）", "待查", "present", "正县级", "会议排名在人大主任之后"),

    # 夏得烈
    (6, 7, "县委常委、政法委书记", "待查", "present", "副县级", ""),

    # 林梅
    (7, 1, "县领导（推测副县长）", "待查", "present", "副县级", ""),

    # 罗克帅
    (8, 1, "县委常委、常务副县长", "待查", "present", "副县级", "负责政府常务工作"),

    # 徐庆华
    (9, 5, "县委常委、组织部部长", "待查", "present", "副县级", ""),

    # 葛英才
    (10, 6, "县委常委、宣传部部长", "待查", "present", "副县级", ""),

    # 杨海涛
    (11, 1, "县领导（推测副县长）", "待查", "present", "副县级", ""),

    # 陈李丽
    (12, 1, "县领导（推测副县长或统战部长）", "待查", "present", "副县级", ""),

    # 娄江波
    (13, 9, "县委常委、人武部部长", "待查", "present", "副县级", ""),

    # 胡建琼
    (14, 1, "副县长", "待查", "present", "副县级", ""),
    (14, 10, "泰和高新区党工委书记", "待查", "present", "副县级", ""),

    # 廖欣
    (15, 1, "副县长", "待查", "present", "副县级", "分管教育工作"),
]

# ── Relationships ──
# Fields: (person_a, person_b, type, context, overlap_org, overlap_period)

RELATIONSHIPS = [
    # 巫太明 ↔ 李艳辉：党政一把手搭档
    (0, 1, "党政搭档", "县委书记与县长候选人，共同主持全县工作", "中共泰和县委员会/泰和县人民政府", "2026-07至今"),

    # 巫太明 ↔ 罗克帅：上下级
    (0, 8, "上下级", "县委书记与常务副县长，重点项目推进工作中的直接上下级", "中共泰和县委员会", "2026"),

    # 巫太明 ↔ 徐庆华：上下级（组织人事）
    (0, 9, "上下级", "县委书记与组织部部长，共同参加老干部慰问活动", "中共泰和县委员会", "2026"),

    # 巫太明 ↔ 葛英才：上下级（宣传）
    (0, 10, "上下级", "县委书记与宣传部部长，共同调研教育工作", "中共泰和县委员会", "2026-07-14"),

    # 巫太明 ↔ 娄江波：上下级（武装）
    (0, 13, "上下级", "县委书记（人武部第一书记）与人武部部长", "泰和县人民武装部", "2026-06-24"),

    # 巫太明 ↔ 廖文来：前后任交接
    (0, 2, "交接关系", "巫太明任书记时，廖文来为县长；后廖离任，李艳辉接任县长候选人", "泰和县", "2026"),

    # 巫太明 ↔ 夏得烈：上下级（政法）
    (0, 6, "上下级", "县委书记与政法委书记", "中共泰和县委员会", "2026"),

    # 李艳辉 ↔ 徐庆华：工作搭档
    (1, 9, "工作搭档", "县长候选人与组织部部长，共同走访慰问老干部", "泰和县人民政府", "2026-07-04"),

    # 罗克帅 ↔ 胡建琼：经济工作搭档
    (8, 14, "工作搭档", "常务副县长与副县长/高新区书记，共同负责工业和经济工作", "泰和县人民政府", "2026"),

    # 曾向荣 ↔ 王志宏：人大/政协配合
    (4, 5, "人大政协协同", "人大主任与政协主席（推测），县四套班子领导成员", "泰和县", "2026"),
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

    # Stats
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
    else:
        return "200,200,200"


def is_top_leader(p):
    post = p[9]
    return "县委书记" in post or "县长" in post


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>泰和县领导班子工作关系网络 — 2026年7月</description>')
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
    print("Building 泰和县 network data...")
    build_db()
    build_gexf()
    print(f"\nSummary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS_DATA)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print("Done.")
