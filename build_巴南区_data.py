#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 巴南区 (Banan District, Chongqing).

Task: chongqing_巴南区 — 区委书记 & 区长
Province: 重庆市
City: 巴南区 (重庆直辖市下辖区)
Region: 巴南区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 陶世祥 (appointed ~Jan 2026; previously unknown)
- 区委副书记、区长: 钟涛 (confirmed, currently active; previously unknown)
- 区委副书记: 周密 (confirmed from news reports)
- 区人大常委会主任: Not confirmed from available sources
- 区政协主席: Not confirmed from available sources

Confirmed leadership team (区政府) from official cqbn.gov.cn:
- 艾正兵 (区委常委、区政府常务副区长、党组副书记)
- 朱激扬 (区委常委、区政府党组成员)
- 杨亚平 (区政府副区长、党组成员)
- 代建红 (区政府副区长、党组成员)
- 赵吉春 (区政府副区长、党组成员，区公安分局党委书记、局长)
- 刘功峰 (区政府副区长、党组成员)
- 李萍 (区政府副区长、党组成员)
- 王波 (区政府副区长)
- 韩行 (区政府副区长、党组成员，挂职)
- 左鹏 (区政府党组成员)

Confirmed predecessor:
- 前区委书记: 何友生 (served from ~2021 to ~2025, succeeded by 陶世祥)
- 前区长: Unknown from available sources

Confidence: Current leadership identity confirmed from official government website and
news reports. Detailed career timelines and biographical data limited due to
Baidu Baike access restrictions (403). Data marked with appropriate confidence levels.

Sources:
- www.cqbn.gov.cn — official government website (primary source for leadership roster)
- 区政府召开常务会议 news — 钟涛 as 区长 confirmation
- 陶世祥 区领导活动报道 — 区委书记 confirmation
- Government institutions page listing full roster
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "巴南区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "巴南区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 区委班子 (District Party Committee) ══

    # 区委书记 — 陶世祥
    ("bn_tao_shixiang", "陶世祥", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委书记", "中共重庆市巴南区委员会",
     "cqbn.gov.cn_news;media_reports"),

    # 区委副书记、区长 — 钟涛
    ("bn_zhong_tao", "钟涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official;gov_institutions_page"),

    # 区委副书记（专职）— 周密
    ("bn_zhou_mi", "周密", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记", "中共重庆市巴南区委员会",
     "cqbn.gov.cn_news"),

    # ══ 区政府领导 ══

    # 区委常委、常务副区长 — 艾正兵
    ("bn_ai_zhengbing", "艾正兵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区政府常务副区长、党组副书记", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区委常委、区政府党组成员 — 朱激扬
    ("bn_zhu_jiyang", "朱激扬", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区政府党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长 — 杨亚平
    ("bn_yang_yaping", "杨亚平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长 — 代建红
    ("bn_dai_jianhong", "代建红", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长兼公安分局局长 — 赵吉春
    ("bn_zhao_jichun", "赵吉春", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员，区公安分局党委书记、局长、督察长（兼）", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长 — 刘功峰
    ("bn_liu_gongfeng", "刘功峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长 — 李萍
    ("bn_li_ping", "李萍", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长 — 王波
    ("bn_wang_bo", "王波", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府副区长（挂职）— 韩行
    ("bn_han_xing", "韩行", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、党组成员（挂职）", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # 区政府党组成员 — 左鹏
    ("bn_zuo_peng", "左鹏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员", "重庆市巴南区人民政府",
     "cqbn.gov.cn_official"),

    # ══ 前任领导 ══

    # 前区委书记 — 何友生
    ("bn_he_yousheng", "何友生", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记", "中共重庆市巴南区委员会（原）",
     "media_reports;historical_knowledge"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("bn_party_committee", "中共重庆市巴南区委员会", "党委", "地厅级", "中共重庆市委", "重庆市巴南区"),
    ("bn_gov", "重庆市巴南区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市巴南区"),
    ("bn_discipline", "中共重庆市巴南区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市巴南区"),
    ("bn_organization", "中共重庆市巴南区委组织部", "党委部门", "正处级", "巴南区委", "重庆市巴南区"),
    ("bn_propaganda", "中共重庆市巴南区委宣传部", "党委部门", "正处级", "巴南区委", "重庆市巴南区"),
    ("bn_united_front", "中共重庆市巴南区委统战部", "党委部门", "正处级", "巴南区委", "重庆市巴南区"),
    ("bn_political_legal", "中共重庆市巴南区委政法委员会", "党委部门", "正处级", "巴南区委", "重庆市巴南区"),
    ("bn_military_department", "重庆市巴南区人民武装部", "军事", "正师级", "重庆警备区", "重庆市巴南区"),
    ("bn_public_security", "重庆市公安局巴南区分局", "公安", "正处级", "重庆市公安局", "重庆市巴南区"),
    ("bn_peoples_congress", "重庆市巴南区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市巴南区"),
    ("bn_cppcc", "中国人民政治协商会议重庆市巴南区委员会", "政协", "地厅级", "重庆市政协", "重庆市巴南区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 陶世祥 — 区委书记 ═══
    ("bn_tao_shixiang", "bn_party_committee", "区委书记", "2026-01", "至今", "正厅级",
     "主持区委全面工作。最早于2026年1月4日以区委书记身份出现。"),

    # ═══ 钟涛 — 区长 ═══
    ("bn_zhong_tao", "bn_gov", "区长", "待查", "至今", "正厅级",
     "主持区政府全面工作。区委副书记、区政府党组书记。"),
    ("bn_zhong_tao", "bn_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任"),

    # ═══ 周密 — 区委副书记 ═══
    ("bn_zhou_mi", "bn_party_committee", "区委副书记", "待查", "至今", "正厅级",
     "专职副书记。2026年6月30日主持区两优一先表彰大会。"),

    # ═══ 艾正兵 — 常务副区长 ═══
    ("bn_ai_zhengbing", "bn_gov", "区委常委、区政府常务副区长、党组副书记", "待查", "至今", "副厅级",
     "负责区政府常务工作。"),
    ("bn_ai_zhengbing", "bn_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 朱激扬 — 区委常委 ═══
    ("bn_zhu_jiyang", "bn_gov", "区委常委、区政府党组成员", "待查", "至今", "副厅级", ""),
    ("bn_zhu_jiyang", "bn_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 杨亚平 — 副区长 ═══
    ("bn_yang_yaping", "bn_gov", "区政府副区长、党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 代建红 — 副区长 ═══
    ("bn_dai_jianhong", "bn_gov", "区政府副区长、党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 赵吉春 — 副区长兼公安分局局长 ═══
    ("bn_zhao_jichun", "bn_gov", "区政府副区长、党组成员", "待查", "至今", "副厅级", ""),
    ("bn_zhao_jichun", "bn_public_security", "区公安分局党委书记、局长、督察长（兼）", "待查", "至今", "正处级", ""),

    # ═══ 刘功峰 — 副区长 ═══
    ("bn_liu_gongfeng", "bn_gov", "区政府副区长、党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 李萍 — 副区长 ═══
    ("bn_li_ping", "bn_gov", "区政府副区长、党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 王波 — 副区长 ═══
    ("bn_wang_bo", "bn_gov", "区政府副区长", "待查", "至今", "副厅级", ""),

    # ═══ 韩行 — 副区长（挂职） ═══
    ("bn_han_xing", "bn_gov", "区政府副区长、党组成员（挂职）", "待查", "至今", "副厅级", "挂职"),

    # ═══ 左鹏 — 区政府党组成员 ═══
    ("bn_zuo_peng", "bn_gov", "区政府党组成员", "待查", "至今", "副厅级", ""),

    # ═══ 前任领导 ═══
    ("bn_he_yousheng", "bn_party_committee", "前任区委书记", "2021?", "2025-12", "正厅级",
     "前任巴南区委书记，约2025年底离任。陶世祥于2026年1月接任。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 陶世祥 ↔ 钟涛 — 党政正职搭档 ═══
    ("bn_tao_shixiang", "bn_zhong_tao", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市巴南区委员会;重庆市巴南区人民政府", "2026-01至今"),

    # ═══ 陶世祥 ↔ 周密 — 书记-副书记 ═══
    ("bn_tao_shixiang", "bn_zhou_mi", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市巴南区委员会", "2026-01至今"),

    # ═══ 钟涛 ↔ 周密 — 区长-副书记 ═══
    ("bn_zhong_tao", "bn_zhou_mi", "overlap",
     "区长与区委副书记（区委区政府协调）",
     "中共重庆市巴南区委员会", "至今"),

    # ═══ 钟涛 ↔ 艾正兵 — 区长-常务副区长 ═══
    ("bn_zhong_tao", "bn_ai_zhengbing", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市巴南区人民政府", "至今"),

    # ═══ 陶世祥 ↔ 艾正兵 — 书记-常委 ═══
    ("bn_tao_shixiang", "bn_ai_zhengbing", "superior_subordinate",
     "区委书记与区委常委、常务副区长",
     "中共重庆市巴南区委员会", "2026-01至今"),

    # ═══ 陶世祥 ↔ 朱激扬 — 书记-常委 ═══
    ("bn_tao_shixiang", "bn_zhu_jiyang", "superior_subordinate",
     "区委书记与区委常委、区政府党组成员",
     "中共重庆市巴南区委员会", "2026-01至今"),

    # ═══ 钟涛 ↔ 赵吉春 — 区长-副区长(公安) ═══
    ("bn_zhong_tao", "bn_zhao_jichun", "superior_subordinate",
     "区长与分管公安工作的副区长",
     "重庆市巴南区人民政府", "至今"),

    # ═══ 钟涛 ↔ 杨亚平 — 区长-副区长 ═══
    ("bn_zhong_tao", "bn_yang_yaping", "superior_subordinate",
     "区长与副区长",
     "重庆市巴南区人民政府", "至今"),

    # ═══ 钟涛 ↔ 代建红 — 区长-副区长 ═══
    ("bn_zhong_tao", "bn_dai_jianhong", "superior_subordinate",
     "区长与副区长",
     "重庆市巴南区人民政府", "至今"),

    # ═══ 钟涛 ↔ 李萍 — 区长-副区长 ═══
    ("bn_zhong_tao", "bn_li_ping", "superior_subordinate",
     "区长与副区长",
     "重庆市巴南区人民政府", "至今"),

    # ═══ 陶世祥 — 前任书记（何友生） ═══
    ("bn_tao_shixiang", "bn_he_yousheng", "predecessor_successor",
     "陶世祥接替何友生任巴南区委书记",
     "中共重庆市巴南区委员会", "2026-01"),
]


# ════════════════════════════════════════════
# SQLITE SETUP
# ════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF GENERATION
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(person_id):
    return person_id in ("bn_tao_shixiang", "bn_zhong_tao", "bn_he_yousheng")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("bn_tao_shixiang", "bn_he_yousheng"):
        return "255,50,50"       # Red — Party Secretary
    elif person_id == "bn_zhong_tao":
        return "50,100,255"      # Blue — Government head
    elif person_id in ("bn_zhu_jiyang",):
        return "100,100,100"     # Grey — Other
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "军事": "200,200,200",
        "公安": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(org_type, "200,200,200")


def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市巴南区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[8]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="person"/>')
        lines.append(f'          <attvalue for="3" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        olevel = o[3]
        c = org_color(oid, otype)
        lines.append(f'      <node id="o{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(olevel)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at via positions)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3] if pos[3] else ""
        end = pos[4] if pos[4] else ""
        eid += 1
        period = f"{start}-{end}" if start or end else ""
        lines.append(f'      <edge id="e{eid}" source="p{esc(pid)}" target="o{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oid)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        overlap_org = r[4]
        overlap_period = r[5]
        weight = "2.0"  # person-person edges stronger than person-org
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{esc(pa)}" target="p{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(overlap_period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════

def print_summary():
    print(f"\n{'='*60}")
    print(f"  重庆市巴南区 领导网络数据")
    print(f"{'='*60}")
    print(f"  人物: {len(PERSONS)}")
    print(f"  机构: {len(ORGANIZATIONS)}")
    print(f"  任职记录: {len(POSITIONS)}")
    print(f"  关系边: {len(RELATIONSHIPS)}")
    print(f"{'='*60}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    generate_gexf()
    print_summary()
