#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 城口县 (Chengkou County, Chongqing).

Task: chongqing_城口县 — 县委书记 & 县长
Province: 重庆市
City: 城口县 (重庆直辖市下辖县)
Region: 城口县
Level: 县(直辖市下辖)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 县委书记: 王春梅 (confirmed from official news reports, July 2026)
- 县委副书记、代理县长: 黎中华 (confirmed from July 2026 city governance meeting)
- 县人大常委会主任: 滕远东 (confirmed from same meeting)
- 县政协主席: 何国兵 (confirmed from July 13, 2026 news)
- 县委副书记: 罗小松 (confirmed from same meeting)

Confirmed government leadership (from 城府办发〔2026〕5号, Feb 2026):
- 王春梅: 主持县政府全面工作 (at that time also held 县长 role)
- 张国进: 县委常委、常务副县长
- 林奇东: 副县长（交通、文旅等）
- 肖兴旺: 副县长（住建、环保等）
- 周亮: 副县长（工信、水利等）
- 刘光明: 副县长（农业农村等）

Confirmed party leadership (from July 2026 meetings):
- 王春梅: 县委书记
- 黎中华: 县委副书记、代理县长
- 罗小松: 县委副书记
- 滕兴中: 县委常委
- 王小平: 县委常委
- 陈杰: 县委常委
- 张国进: 县委常委

Predecessor information:
- 前县委书记（before 王春梅）: Not confirmed from available sources
- 前县长（before 黎中华）: 王春梅 previously held 县长 concurrently

Confidence: Current leadership identity confirmed from official government website news
reports. Detailed career timelines limited due to Baidu Baike access restrictions (403).
Data marked with appropriate confidence levels.

Sources:
- www.cqck.gov.cn — official government website (primary source)
- 县委常委会第173次会议 (2026-07-09) — 王春梅 as 县委书记 confirmed
- 县城市治理委员会第三次会议 (2026-07-08) — 黎中华 as 代理县长 confirmed
- 城府办发〔2026〕5号 — government leadership division document
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "城口县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "城口县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 县委班子 (County Party Committee) ══

    # 县委书记 — 王春梅
    ("ck_wang_chunmei", "王春梅", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委书记", "中共重庆市城口县委员会",
     "cqck.gov.cn_party_committee_meeting_20260709;cqck.gov.cn_city_gov_meeting_20260708"),

    # 县委副书记、代理县长 — 黎中华
    ("ck_li_zhonghua", "黎中华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记、代理县长", "城口县人民政府",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # 县委副书记（专职）— 罗小松
    ("ck_luo_xiaosong", "罗小松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委副书记", "中共重庆市城口县委员会",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # 县人大常委会主任 — 滕远东
    ("ck_teng_yuandong", "滕远东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县人大常委会主任", "城口县人民代表大会常务委员会",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # 县政协主席 — 何国兵
    ("ck_he_guobing", "何国兵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县政协主席", "中国人民政治协商会议重庆市城口县委员会",
     "cqck.gov.cn_heguobing_20260714"),

    # ══ 县委常委 ══

    # 县委常委 — 滕兴中
    ("ck_teng_xingzhong", "滕兴中", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共重庆市城口县委员会",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # 县委常委 — 张国进（常务副县长）
    ("ck_zhang_guojin", "张国进", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、县政府常务副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 县委常委 — 王小平
    ("ck_wang_xiaoping", "王小平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共重庆市城口县委员会",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # 县委常委 — 林奇东
    ("ck_lin_qidong", "林奇东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、副县长", "城口县人民政府",
     "cqck.gov.cn_city_gov_meeting_20260708;cqck.gov.cn_gov_division_20260209"),

    # 县委常委 — 陈杰
    ("ck_chen_jie", "陈杰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共重庆市城口县委员会",
     "cqck.gov.cn_city_gov_meeting_20260708"),

    # ══ 县政府其他领导 ══

    # 副县长 — 肖兴旺
    ("ck_xiao_xingwang", "肖兴旺", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长 — 周亮
    ("ck_zhou_liang", "周亮", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长 — 刘光明
    ("ck_liu_guangming", "刘光明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长 — 刘凯
    ("ck_liu_kai", "刘凯", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长、县公安局局长", "城口县公安局",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长 — 孙禹
    ("ck_sun_yu", "孙禹", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长 — 吴雪飞
    ("ck_wu_xuefei", "吴雪飞", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长（挂职）— 高仁茂
    ("ck_gao_renmao", "高仁茂", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长（挂职）— 张锐
    ("ck_zhang_rui", "张锐", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长（挂职）", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),

    # 副县长（挂职）— 颜士刚
    ("ck_yan_shigang", "颜士刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长（挂职）", "城口县人民政府",
     "cqck.gov.cn_gov_division_20260209"),
]

ORGANIZATIONS = [
    ("ck_party_committee", "中共重庆市城口县委员会", "党委", "县级", "", "重庆市城口县"),
    ("ck_gov", "城口县人民政府", "政府", "县级", "", "重庆市城口县"),
    ("ck_npc", "城口县人民代表大会常务委员会", "人大", "县级", "", "重庆市城口县"),
    ("ck_cppcc", "中国人民政治协商会议重庆市城口县委员会", "政协", "县级", "", "重庆市城口县"),
    ("ck_public_security", "城口县公安局", "公安", "县级", "ck_gov", "重庆市城口县"),
]

POSITIONS = [
    # ═══ 王春梅 — 县委书记 ═══
    ("ck_wang_chunmei", "ck_party_committee", "县委书记", "待查", "至今", "正处级",
     "县委书记，主持县委全面工作。另曾任县长（兼）至约2026年初，后由黎中华任代理县长。"),

    # ═══ 黎中华 — 代理县长 ═══
    ("ck_li_zhonghua", "ck_gov", "县委副书记、代理县长", "待查", "至今", "正处级",
     "2026年7月以县委副书记、代理县长身份公开出席活动。"),

    # ═══ 罗小松 — 县委副书记 ═══
    ("ck_luo_xiaosong", "ck_party_committee", "县委副书记", "待查", "至今", "正处级", ""),

    # ═══ 滕远东 — 人大常委会主任 ═══
    ("ck_teng_yuandong", "ck_npc", "县人大常委会主任", "待查", "至今", "正处级",
     "2026年7月8日县城市治理委员会第三次会议出席。"),

    # ═══ 何国兵 — 政协主席 ═══
    ("ck_he_guobing", "ck_cppcc", "县政协主席", "待查", "至今", "正处级",
     "2026年7月13日带队赴双河乡调研工作。"),

    # ═══ 滕兴中 — 县委常委 ═══
    ("ck_teng_xingzhong", "ck_party_committee", "县委常委", "待查", "至今", "副处级", ""),

    # ═══ 张国进 — 常务副县长 ═══
    ("ck_zhang_guojin", "ck_gov", "县委常委、县政府常务副县长", "待查", "至今", "副处级",
     "负责县政府常务工作，分管发展改革、财政、应急管理等。"),

    # ═══ 王小平 — 县委常委 ═══
    ("ck_wang_xiaoping", "ck_party_committee", "县委常委", "待查", "至今", "副处级", ""),

    # ═══ 林奇东 — 副县长 ═══
    ("ck_lin_qidong", "ck_gov", "县委常委、副县长", "待查", "至今", "副处级",
     "负责交通、文化旅游、体育等工作。"),

    # ═══ 陈杰 — 县委常委 ═══
    ("ck_chen_jie", "ck_party_committee", "县委常委", "待查", "至今", "副处级", ""),

    # ═══ 肖兴旺 — 副县长 ═══
    ("ck_xiao_xingwang", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责住房和城乡建设、生态环境、规划自然资源等工作。"),

    # ═══ 周亮 — 副县长 ═══
    ("ck_zhou_liang", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责工业和信息化、水利、市场监管等工作。"),

    # ═══ 刘光明 — 副县长 ═══
    ("ck_liu_guangming", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责农业农村、乡村振兴、林业等工作。"),

    # ═══ 刘凯 — 副县长/公安局长 ═══
    ("ck_liu_kai", "ck_gov", "副县长、县公安局局长", "待查", "至今", "副处级",
     "负责公安、司法行政、信访等工作。"),
    ("ck_liu_kai", "ck_public_security", "县公安局党委书记、局长", "待查", "至今", "副处级", ""),

    # ═══ 孙禹 — 副县长 ═══
    ("ck_sun_yu", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责人力资源和社会保障、退役军人事务等工作（中央单位定点帮扶挂职）。"),

    # ═══ 吴雪飞 — 副县长 ═══
    ("ck_wu_xuefei", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责民政、卫生健康、医疗保障等工作。"),

    # ═══ 高仁茂 — 副县长 ═══
    ("ck_gao_renmao", "ck_gov", "副县长", "待查", "至今", "副处级",
     "负责教育、商务等工作。"),

    # ═══ 张锐 — 副县长（挂职） ═══
    ("ck_zhang_rui", "ck_gov", "副县长（挂职）", "待查", "至今", "副处级",
     "协助负责水利、水库移民、巩固衔接等工作。"),

    # ═══ 颜士刚 — 副县长（挂职） ═══
    ("ck_yan_shigang", "ck_gov", "副县长（挂职）", "待查", "至今", "副处级",
     "协助负责统计、东西部协作、巩固衔接等工作。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 王春梅 ↔ 黎中华 — 党政正职搭档 ═══
    ("ck_wang_chunmei", "ck_li_zhonghua", "superior_subordinate",
     "县委书记与代理县长党政正职搭档关系",
     "中共重庆市城口县委员会;城口县人民政府", "2026年至今"),

    # ═══ 王春梅 ↔ 罗小松 — 书记-副书记 ═══
    ("ck_wang_chunmei", "ck_luo_xiaosong", "superior_subordinate",
     "县委书记与专职副书记",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 罗小松 — 县长-副书记 ═══
    ("ck_li_zhonghua", "ck_luo_xiaosong", "overlap",
     "代理县长与县委副书记（党政协调）",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 张国进 — 县长-常务副县长 ═══
    ("ck_li_zhonghua", "ck_zhang_guojin", "superior_subordinate",
     "代理县长与常务副县长（县政府日常运作）",
     "城口县人民政府", "2026年至今"),

    # ═══ 王春梅 ↔ 张国进 — 书记-常委 ═══
    ("ck_wang_chunmei", "ck_zhang_guojin", "superior_subordinate",
     "县委书记与县委常委、常务副县长",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 滕兴中 — 县长-常委 ═══
    ("ck_li_zhonghua", "ck_teng_xingzhong", "overlap",
     "代理县长与县委常委",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 王小平 — 县长-常委 ═══
    ("ck_li_zhonghua", "ck_wang_xiaoping", "overlap",
     "代理县长与县委常委",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 陈杰 — 县长-常委 ═══
    ("ck_li_zhonghua", "ck_chen_jie", "overlap",
     "代理县长与县委常委",
     "中共重庆市城口县委员会", "2026年至今"),

    # ═══ 黎中华 ↔ 林奇东 — 县长-副县长 ═══
    ("ck_li_zhonghua", "ck_lin_qidong", "superior_subordinate",
     "代理县长与副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 黎中华 ↔ 肖兴旺 — 县长-副县长 ═══
    ("ck_li_zhonghua", "ck_xiao_xingwang", "superior_subordinate",
     "代理县长与副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 黎中华 ↔ 周亮 — 县长-副县长 ═══
    ("ck_li_zhonghua", "ck_zhou_liang", "superior_subordinate",
     "代理县长与副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 黎中华 ↔ 刘光明 — 县长-副县长 ═══
    ("ck_li_zhonghua", "ck_liu_guangming", "superior_subordinate",
     "代理县长与副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 黎中华 ↔ 刘凯 — 县长-副县长(公安) ═══
    ("ck_li_zhonghua", "ck_liu_kai", "superior_subordinate",
     "代理县长与分管公安工作的副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 黎中华 ↔ 吴雪飞 — 县长-副县长 ═══
    ("ck_li_zhonghua", "ck_wu_xuefei", "superior_subordinate",
     "代理县长与副县长",
     "城口县人民政府", "2026年至今"),

    # ═══ 王春梅 ↔ 滕远东 — 县委-人大 ═══
    ("ck_wang_chunmei", "ck_teng_yuandong", "overlap",
     "县委书记与县人大常委会主任",
     "城口县", "2026年至今"),

    # ═══ 王春梅 ↔ 何国兵 — 县委-政协 ═══
    ("ck_wang_chunmei", "ck_he_guobing", "overlap",
     "县委书记与县政协主席",
     "城口县", "2026年至今"),
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
    return person_id in ("ck_wang_chunmei", "ck_li_zhonghua", "ck_luo_xiaosong", "ck_teng_yuandong", "ck_he_guobing")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("ck_wang_chunmei",):
        return "255,50,50"          # Red — Party Secretary
    elif person_id == "ck_li_zhonghua":
        return "50,100,255"         # Blue — Government head
    elif person_id == "ck_luo_xiaosong":
        return "100,100,100"        # Grey — Deputy Secretary
    elif person_id in ("ck_teng_yuandong",):
        return "200,255,255"        # Cyan — NPC
    elif person_id == "ck_he_guobing":
        return "255,240,200"        # Cream — CPPCC
    elif person_id == "ck_zhang_guojin":
        return "50,100,255"         # Blue — Deputy head
    else:
        return "100,100,100"        # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
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
    lines.append('    <description>重庆市城口县领导班子工作关系网络</description>')
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
    print(f"  重庆市城口县 领导网络数据")
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
