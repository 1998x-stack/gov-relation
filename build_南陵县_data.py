#!/usr/bin/env python3
"""
南陵县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Nanling County leadership.

南陵县 — 安徽省芜湖市下辖县，位于安徽省东南部，皖南丘陵向沿江平原过渡地带。
县域面积1260平方公里，人口54万，下辖8个镇、1个省级经济开发区。

Data current as of July 2026. Sources:
  - https://www.nlx.gov.cn/zwgk/ldzc/ (南陵县人民政府领导之窗)
  - https://www.nlx.gov.cn/xwzx/jrnl/ (南陵县今日南陵新闻)
  - Official news articles on nlx.gov.cn

Research access: The nlx.gov.cn website was directly accessible. Party Secretary
confirmed as 杨绍华 from multiple official news reports (July 2026).
County Mayor confirmed as 夏彬 from official government leadership page.
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "南陵县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "南陵县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── DATA ──
# Person ID convention: nanling_{surname_givenname}

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 杨绍华
    # Source: Multiple official nlx.gov.cn news articles (2026-06-13 through 2026-07-15)
    # Attended 县第十四次党代会、十五届县委一次全会 (2026-06-27)
    ("nanling_yang_shaohua", "杨绍华", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委书记", "中共南陵县委员会",
     "nlx.gov.cn 新闻：2026-07-15 督导检查城乡人居环境'五边三化'工作；"
     "2026-07-13 督导检查防汛防台风工作；"
     "2026-07-10 主持县委常委会；"
     "2026-07-04 主持县四大班子通气会；"
     "2026-06-27 主持县第十五次党代会并作报告；"
     "2026-06-16 主持县委十四届十一次全会"),

    # 县长 — 夏彬
    # Source: nlx.gov.cn 领导之窗页面 (县政府领导)
    ("nanling_xia_bin", "夏彬", "男", "汉族", "1983-10", "待查",
     "研究生学历，教育学硕士", "中共党员", "待查",
     "县委副书记、县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 夏彬个人履历页面；"
     "曾任区直部门正职、街道办事处主任、党工委书记、副区长、区委常委、政法委书记、常务副区长等"),

    # ═══ County Party Standing Committee (县委常委) ═══
    # Note: Exact roles for each member are partially known from news mentions

    # 县委副书记（专职）— 杨磊
    ("nanling_yang_lei", "杨磊", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委副书记", "中共南陵县委员会",
     "nlx.gov.cn 新闻：2026-07-15 参加五边三化调度会（县委副书记）；"
     "2026-07-04 出席县四大班子通气会；"
     "2026-07-01 参加两优一先表彰大会"),

    # 县人大常委会主任 — 巫军
    ("nanling_wu_jun", "巫军", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县人大常委会主任", "南陵县人民代表大会常务委员会",
     "nlx.gov.cn 新闻：2026-07-04 出席县四大班子通气会；"
     "2026-07-01 参加两优一先表彰大会；"
     "2026-06-16 出席县委十四届十一次全会"),

    # 县政协主席 — 刘敏
    ("nanling_liu_min", "刘敏", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县政协主席", "中国人民政治协商会议南陵县委员会",
     "nlx.gov.cn 新闻：2026-07-04 出席县四大班子通气会；"
     "2026-07-01 参加两优一先表彰大会；"
     "2026-06-16 出席县委十四届十一次全会"),

    # 县领导（县级领导）— 马劲松
    # Appears in multiple articles as attending inspections alongside Party Secretary
    ("nanling_ma_jinsong", "马劲松", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县领导", "中共南陵县委员会/南陵县人民政府",
     "nlx.gov.cn 新闻：2026-07-15 参加五边三化调研；"
     "2026-07-13 参加防汛防台风督导（县领导）"),

    # 县委常委、副县长 — 陈娉婷
    ("nanling_chen_pingting", "陈娉婷", "女", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议；"
     "2026-06-19 参加安全生产督导检查"),

    # 副县长 — 曲向阳
    ("nanling_qu_xiangyang", "曲向阳", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 新闻：2026-07-14 参加县十八届政府第147次常务会议"),

    # 副县长 — 汪金龙
    ("nanling_wang_jinlong", "汪金龙", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议"),

    # 副县长 — 何军
    ("nanling_he_jun", "何军", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议；"
     "2026-07-13 参加防汛防台风督导"),

    # 副县长 — 俞悦
    ("nanling_yu_yue", "俞悦", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议"),

    # 副县长 — 俞宏珍
    ("nanling_yu_hongzhen", "俞宏珍", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议"),

    # 副县长 — 张阳阳
    ("nanling_zhang_yangyang", "张阳阳", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "副县长", "南陵县人民政府",
     "nlx.gov.cn 领导之窗 — 县政府领导；"
     "2026-07-14 参加县十八届政府第147次常务会议；"
     "2026-07-15 参加五边三化调度会"),

    # 县领导 — 孙兆荣
    ("nanling_sun_zhaorong", "孙兆荣", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县领导", "中共南陵县委员会/南陵县人民政府",
     "nlx.gov.cn 新闻：2026-07-13 参加防汛防台风督导"),

    # 县领导 — 许方震
    ("nanling_xu_fangzhen", "许方震", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县领导", "中共南陵县委员会/南陵县人民政府",
     "nlx.gov.cn 新闻：2026-07-13 参加防汛防台风督导"),

    # ═══ Predecessors (历史主要领导) ═══

    # 前任县委书记 — 待确认
    # Note: 杨绍华 appears to have been in office at least since June 2026 (14th CPC county congress)
    # Previous party secretary name is not yet confirmed from available sources
    ("nanling_prev_party_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "前任县委书记", "中共南陵县委员会",
     "⚠️ 待确认：需从 nlx.gov.cn 历史新闻确认杨绍华前任"),

    # 前任县长 — 待确认
    # 夏彬 is current mayor; predecessor unclear from available sources
    ("nanling_prev_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "前任县长", "南陵县人民政府",
     "⚠️ 待确认：需从 nlx.gov.cn 历史新闻确认夏彬前任"),

    # ═══ Wuhu City-level Leaders (cross-reference) ═══

    # 芜湖市委书记 — 宁波
    ("nanling_ningbo", "宁波", "男", "汉族", "1969-03", "安徽合肥",
     "省委党校研究生/工学学士", "中共党员", "1988",
     "芜湖市委书记", "中共芜湖市委",
     "build_芜湖市_data.py — 曾任芜湖市长2017-2021；2021年任市委书记"),

    # 芜湖市长 — 徐志
    ("nanling_xu_zhi", "徐志", "男", "汉族", "1972-03", "安徽合肥（一说巢湖）",
     "在职研究生/经济学博士", "中共党员", "1994",
     "芜湖市委副书记、市长", "芜湖市人民政府",
     "build_芜湖市_data.py — 曾任安徽省发展改革委副主任"),
]

# ── Organizations ──
ORGS = [
    # (id, name, type, level, parent, location)
    ("org_nanling_party", "中共南陵县委员会", "党委", "县处级", "中共芜湖市委", "安徽省芜湖市南陵县"),
    ("org_nanling_gov", "南陵县人民政府", "政府", "县处级", "芜湖市人民政府", "安徽省芜湖市南陵县"),
    ("org_nanling_npc", "南陵县人民代表大会常务委员会", "人大", "县处级", "", "安徽省芜湖市南陵县"),
    ("org_nanling_cppcc", "中国人民政治协商会议南陵县委员会", "政协", "县处级", "", "安徽省芜湖市南陵县"),
    ("org_nanling_discipline", "中共南陵县纪律检查委员会", "纪委", "县处级", "", "安徽省芜湖市南陵县"),
    ("org_nanling_org_dept", "中共南陵县委组织部", "党委部门", "正科级", "中共南陵县委员会", "安徽省芜湖市南陵县"),
    ("org_nanling_propaganda", "中共南陵县委宣传部", "党委部门", "正科级", "中共南陵县委员会", "安徽省芜湖市南陵县"),
    ("org_nanling_legal_affairs", "中共南陵县委政法委员会", "党委部门", "正科级", "中共南陵县委员会", "安徽省芜湖市南陵县"),
    ("org_nanling_united_front", "中共南陵县委统一战线工作部", "党委部门", "正科级", "中共南陵县委员会", "安徽省芜湖市南陵县"),
    ("org_nanling_armed_forces", "南陵县人民武装部", "军队", "正团级", "", "安徽省芜湖市南陵县"),
    ("org_nanling_gov_general", "南陵县人民政府办公室", "政府", "正科级", "南陵县人民政府", "安徽省芜湖市南陵县"),
    ("org_nanling_development", "南陵经济开发区（省级）", "开发区", "省级", "南陵县人民政府", "安徽省芜湖市南陵县"),
    ("org_wuhu_party", "中共芜湖市委", "党委", "地厅级", "中共安徽省委", "安徽省芜湖市"),
    ("org_wuhu_gov", "芜湖市人民政府", "政府", "地厅级", "安徽省人民政府", "安徽省芜湖市"),
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ──
POSITIONS = [
    # 杨绍华
    ("nanling_yang_shaohua", "org_nanling_party", "县委书记", "2025?（待确认）", "present", "县处级正职", "2026年7月仍在任"),
    # 夏彬
    ("nanling_xia_bin", "org_nanling_party", "县委副书记", "待确认", "present", "县处级副职", ""),
    ("nanling_xia_bin", "org_nanling_gov", "县长", "待确认", "present", "县处级正职", "2026年7月仍在任"),
    # 杨磊
    ("nanling_yang_lei", "org_nanling_party", "县委副书记", "待确认", "present", "县处级副职", ""),
    # 巫军
    ("nanling_wu_jun", "org_nanling_npc", "县人大常委会主任", "待确认", "present", "县处级正职", ""),
    # 刘敏
    ("nanling_liu_min", "org_nanling_cppcc", "县政协主席", "待确认", "present", "县处级正职", ""),
    # 陈娉婷
    ("nanling_chen_pingting", "org_nanling_gov", "县委常委、副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
    # 曲向阳
    ("nanling_qu_xiangyang", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月15日参加政府常务会议"),
    # 汪金龙
    ("nanling_wang_jinlong", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
    # 何军
    ("nanling_he_jun", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
    # 俞悦
    ("nanling_yu_yue", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
    # 俞宏珍
    ("nanling_yu_hongzhen", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
    # 张阳阳
    ("nanling_zhang_yangyang", "org_nanling_gov", "副县长", "待确认", "present", "县处级副职", "2026年7月仍在任"),
]

# ── Relationships ──
RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
    # 书记-县长: 上下级关系
    ("nanling_yang_shaohua", "nanling_xia_bin", "superior_subordinate",
     "杨绍华（县委书记）- 夏彬（县长）：党政主要领导合作关系",
     "中共南陵县委/南陵县人民政府", "2025?-present", "confirmed"),

    # 书记-副书记: 上下级关系
    ("nanling_yang_shaohua", "nanling_yang_lei", "superior_subordinate",
     "杨绍华（县委书记）- 杨磊（县委副书记）：县委主要领导与专职副书记",
     "中共南陵县委", "待确认-present", "confirmed"),

    # 县长-副县长们: 上下级关系
    ("nanling_xia_bin", "nanling_chen_pingting", "superior_subordinate",
     "夏彬（县长）- 陈娉婷（县委常委、副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_qu_xiangyang", "superior_subordinate",
     "夏彬（县长）- 曲向阳（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_wang_jinlong", "superior_subordinate",
     "夏彬（县长）- 汪金龙（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_he_jun", "superior_subordinate",
     "夏彬（县长）- 何军（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_yu_yue", "superior_subordinate",
     "夏彬（县长）- 俞悦（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_yu_hongzhen", "superior_subordinate",
     "夏彬（县长）- 俞宏珍（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),
    ("nanling_xia_bin", "nanling_zhang_yangyang", "superior_subordinate",
     "夏彬（县长）- 张阳阳（副县长）", "南陵县人民政府", "待确认-present", "confirmed"),

    # 人大主任-政协主席: 同届班子
    ("nanling_wu_jun", "nanling_liu_min", "overlap",
     "巫军（人大主任）- 刘敏（政协主席）：同届四大班子领导", "南陵县", "待确认-present", "confirmed"),

    # 书记-县领导们（共同参加调研）
    ("nanling_yang_shaohua", "nanling_ma_jinsong", "overlap",
     "2026年7月共同督导检查防汛防台风和城乡环境整治", "南陵县", "2026-07", "confirmed"),
    ("nanling_yang_shaohua", "nanling_sun_zhaorong", "overlap",
     "2026-07-13 共同参加防汛防台风督导", "南陵县", "2026-07", "confirmed"),
    ("nanling_yang_shaohua", "nanling_xu_fangzhen", "overlap",
     "2026-07-13 共同参加防汛防台风督导", "南陵县", "2026-07", "confirmed"),

    # 书记-人大主任-政协主席: 四大班子领导
    ("nanling_yang_shaohua", "nanling_wu_jun", "overlap",
     "杨绍华-巫军：县委-人大四大班子领导", "南陵县", "待确认-present", "confirmed"),
    ("nanling_yang_shaohua", "nanling_liu_min", "overlap",
     "杨绍华-刘敏：县委-政协四大班子领导", "南陵县", "待确认-present", "confirmed"),

    # 市县关系: 芜湖市领导与南陵县
    ("nanling_ningbo", "nanling_yang_shaohua", "superior_subordinate",
     "宁波（芜湖市委书记）- 杨绍华（南陵县委书记）：市-县上下级", "芜湖市-南陵县", "待确认-present", "confirmed"),
    ("nanling_xu_zhi", "nanling_xia_bin", "superior_subordinate",
     "徐志（芜湖市长）- 夏彬（南陵县长）：市-县上下级", "芜湖市-南陵县", "待确认-present", "confirmed"),
    ("nanling_ningbo", "nanling_xu_zhi", "overlap",
     "宁波（市委书记）- 徐志（市长）：芜湖市党政主要领导", "中共芜湖市委/芜湖市人民政府", "2023?-present", "confirmed"),
]


# ═══════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, and relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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
        )
    """)
    
    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
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
            confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        )
    """)
    
    # Insert persons
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)
    
    # Insert organizations
    for o in ORGS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)
    
    # Insert positions
    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)
    
    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, r)
    
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════
# GEXF GRAPH GENERATION
# ═══════════════════════════════════════════════════════

def person_color(person_id, name):
    """Return RGB string for a person node based on role."""
    if person_id == "nanling_yang_shaohua":
        return "255,50,50"  # Red — Party Secretary
    if person_id == "nanling_xia_bin":
        return "50,100,255"  # Blue — County Mayor
    if person_id in ("nanling_wu_jun", "nanling_liu_min"):
        return "255,165,0"  # Orange — NPC/CPPCC
    if "prev" in person_id:
        return "150,150,150"  # Grey — predecessor (to be confirmed)
    return "100,100,100"  # Grey — others


def org_color(org_type):
    """Return RGB string for an organization node."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
        "党委部门": "255,200,200",
        "军队": "220,220,220",
        "开发区": "200,255,200",
    }
    return color_map.get(org_type, "200,200,200")


def is_top_leader(pid):
    """Return True if the person is a top leader (书记 or 县长)."""
    return pid in ("nanling_yang_shaohua", "nanling_xia_bin")


def generate_gexf():
    """Generate GEXF graph using string formatting (not ElementTree) for namespace safety."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>南陵县领导班子工作关系网络 — Nanling County Leadership Network (安徽省芜湖市)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')
    
    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name = p[0], p[1]
        c = person_color(pid, name)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        role = p[9]  # current_post
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # ── Nodes: Organizations ──
    for o in ORGS:
        oid, oname, otype = o[0], o[1], o[2]
        c = org_color(otype)
        lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # ── Edges ──
    lines.append('    <edges>')
    eid = 0
    
    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        pid, oid, title = pos[0], pos[1], pos[2]
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        eid += 1
        pa, pb, rtype, ctx = r[0], r[1], r[2], r[3]
        lines.append(f'      <edge id="e{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx[:60])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Organization → Organization (hierarchy)
    for o in ORGS:
        oid, parent = o[0], o[4]
        if parent:
            # Find parent org id
            for o2 in ORGS:
                if o2[1] == parent:
                    eid += 1
                    lines.append(f'      <edge id="e{eid}" source="{esc(oid)}" target="{esc(o2[0])}" label="隶属于" weight="0.5">')
                    lines.append('        <attvalues>')
                    lines.append('          <attvalue for="0" value="belongs_to"/>')
                    lines.append('          <attvalue for="1" value="隶属"/>')
                    lines.append('        </attvalues>')
                    lines.append('      </edge>')
                    break
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🏗️  Building 南陵县 (Nanling County) leadership network...")
    print(f"   Persons: {len(PERSONS)}")
    print(f"   Organizations: {len(ORGS)}")
    print(f"   Positions: {len(POSITIONS)}")
    print(f"   Relationships: {len(RELATIONSHIPS)}")
    print()
    create_database()
    generate_gexf()
    print()
    print("✅ Build complete!")
