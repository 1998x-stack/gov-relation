#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 璧山区 (Bishan District, Chongqing).

Task: chongqing_璧山区 — 区委书记 & 区长
Province: 重庆市
Region: 璧山区 (重庆直辖市下辖区)
Level: 市辖区(直辖市)
Research date: 2026-07-16

Confirmed officeholders from official bishan.gov.cn (as of 2026-07-15):
- 区委书记: 江志斌 (confirmed, currently active)
- 区委副书记、区长: 唐军 (confirmed, currently active)
- 区人大常委会主任: 张献强 (confirmed)
- 区政协主席: 黄孝明 (confirmed)
- 区委副书记: 周树云 (confirmed)
- 区委常委、区纪委书记、区监委主任: 韩海燕 (confirmed)
- 副区长: 常爱书 (confirmed)
- 副区长: 刘全模 (confirmed,分管林业/林长制)
- 副区长: 万小力 (confirmed,分管水利/河长制)

Confidence: Core leadership identities confirmed from official government website
(bishan.gov.cn) as of 2026-07-15. Detailed career timelines and biographical data
limited due to Baidu Baike and search tool access restrictions.
Data marked with appropriate confidence levels.

Sources:
- www.bishan.gov.cn — official government website (primary, multiple articles)
- "以案四说"警示教育大会 article 2026-07-15
- 总河长总林长大会 article 2026-07-09
- 区政府第134次常务会议 article 2026-07-08
- 养老机构消防演练 article 2026-07-10
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "璧山区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "璧山区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 区委班子 (District Party Committee) ══

    # 区委书记 — 江志斌
    ("bs_jiang_zhibin", "江志斌", "男", "汉族", "1970年5月", "四川省荣县",
     "研究生文化，法学博士（重庆工业管理学院工学学士，北京理工大学工商管理硕士，西南大学法学博士）", "1991年12月", "1992年7月",
     "区委书记", "中共重庆市璧山区委员会",
     "wapbaike.baidu.com/item/江志斌;bishan.gov.cn_20260715"),

    # 区委副书记、区长 — 唐军
    ("bs_tang_jun", "唐军", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "重庆市璧山区人民政府",
     "bishan.gov.cn_20260715;bishan.gov.cn_20260709"),

    # 区委副书记（专职）— 周树云
    ("bs_zhou_shuyun", "周树云", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记", "中共重庆市璧山区委员会",
     "bishan.gov.cn_20260715;bishan.gov.cn_20260709"),

    # 区委常委、区纪委书记、区监委主任 — 韩海燕
    ("bs_han_haiyan", "韩海燕", "女", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区纪委书记、区监委主任", "中共重庆市璧山区纪律检查委员会",
     "bishan.gov.cn_20260715"),

    # 区委常委、组织部部长 — 李健
    ("bs_li_jian", "李健", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市璧山区委组织部",
     "bishan.gov.cn_20260630"),

    # 区领导 — 任显智（可能任宣传部部长）
    ("bs_ren_xianzhi", "任显智", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委（?）", "中共重庆市璧山区委员会",
     "bishan.gov.cn_20260626"),

    # 区领导 — 李义奎
    ("bs_li_yikui", "李义奎", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委（?）", "中共重庆市璧山区委员会",
     "bishan.gov.cn_20260626"),

    # 区领导 — 张川
    ("bs_zhang_chuan", "张川", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区领导", "璧山区",
     "bishan.gov.cn_20260713"),

    # ══ 区政府领导 (District Government) ══

    # 副区长 — 常爱书
    ("bs_chang_aishu", "常爱书", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市璧山区人民政府",
     "bishan.gov.cn_20260710"),

    # 副区长 — 刘全模
    ("bs_liu_quanmo", "刘全模", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市璧山区人民政府",
     "bishan.gov.cn_20260709"),

    # 副区长 — 万小力
    ("bs_wan_xiaoli", "万小力", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市璧山区人民政府",
     "bishan.gov.cn_20260709"),

    # ══ 区人大 & 区政协 ══
    ("bs_zhang_xianqiang", "张献强", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "重庆市璧山区人民代表大会常务委员会",
     "bishan.gov.cn_20260715;bishan.gov.cn_20260709"),

    ("bs_huang_xiaoming", "黄孝明", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议重庆市璧山区委员会",
     "bishan.gov.cn_20260715;bishan.gov.cn_20260709"),

    # ══ 前任领导 ══
    # 前区委书记 — 秦文敏
    ("bs_qin_wenmin", "秦文敏", "男", "汉族", "1965年7月", "重庆市巫溪县",
     "大学文化，历史学学士、工商管理硕士（四川大学）", "1987年6月", "1988年7月",
     "前任区委书记（现任重庆市政协经济委副主任）", "重庆市政协",
     "wapbaike.baidu.com/item/秦文敏"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("bs_party_committee", "中共重庆市璧山区委员会", "党委", "地厅级", "中共重庆市委", "重庆市璧山区"),
    ("bs_gov", "重庆市璧山区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市璧山区"),
    ("bs_discipline", "中共重庆市璧山区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市璧山区"),
    ("bs_supervision", "重庆市璧山区监察委员会", "监察", "地厅级", "重庆市监察委员会", "重庆市璧山区"),
    ("bs_peoples_congress", "重庆市璧山区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市璧山区"),
    ("bs_cppcc", "中国人民政治协商会议重庆市璧山区委员会", "政协", "地厅级", "重庆市政协", "重庆市璧山区"),
    ("bs_organization", "中共重庆市璧山区委组织部", "党委部门", "正处级", "璧山区委", "重庆市璧山区"),
    ("bs_propaganda", "中共重庆市璧山区委宣传部", "党委部门", "正处级", "璧山区委", "重庆市璧山区"),
    ("bs_united_front", "中共重庆市璧山区委统战部", "党委部门", "正处级", "璧山区委", "重庆市璧山区"),
    ("bs_political_legal", "中共重庆市璧山区委政法委员会", "党委部门", "正处级", "璧山区委", "重庆市璧山区"),
    ("bs_public_security", "重庆市璧山区公安局", "公安", "正处级", "重庆市公安局", "重庆市璧山区"),
    # 历史组织
    ("bs_org_cqim", "重庆工业管理学院", "事业单位", "正厅级", "重庆工业管理学院", "重庆市"),
    ("bs_org_cqit", "重庆工学院", "事业单位", "正厅级", "重庆工学院", "重庆市"),
    ("bs_org_cqut", "重庆理工大学", "事业单位", "正厅级", "重庆理工大学", "重庆市"),
    ("bs_gov_tongnan", "潼南区（原潼南县）人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市潼南区"),
    ("bs_party_tongnan", "中共重庆市潼南区委员会", "党委", "地厅级", "中共重庆市委", "重庆市潼南区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 江志斌 — 区委书记（完整履历） ═══
    # 重庆工业管理学院时期
    ("bs_jiang_zhibin", "bs_org_cqim", "学生（工业管理工程，工学学士）", "1988-09", "1992-07", "学生", "重庆工业管理学院"),
    ("bs_jiang_zhibin", "bs_org_cqim", "团委干事", "1992-07", "1992-10", "科员", "重庆工业管理学院"),
    ("bs_jiang_zhibin", "bs_org_cqim", "学生科干部、科长", "1992-10", "1997-03", "正科级", "重庆工业管理学院学生工作处"),
    ("bs_jiang_zhibin", "bs_org_cqim", "学生工作处副处长", "1997-03", "1999-10", "副处级", "重庆工业管理学院（后更名重庆工学院）"),
    ("bs_jiang_zhibin", "bs_org_cqit", "学生工作处副处长、毕业生就业服务中心副主任", "1999-10", "2003-01", "副处级", "重庆工学院"),
    ("bs_jiang_zhibin", "bs_org_cqit", "团委书记（正处级）", "2003-01", "2005-03", "正处级", "重庆工学院"),
    ("bs_jiang_zhibin", "bs_org_cqit", "团委书记、学生工作处处长", "2005-03", "2009-03", "正处级", "重庆工学院"),
    ("bs_jiang_zhibin", "bs_org_cqut", "团委书记、学生工作处处长", "2009-03", "2009-08", "正处级", "重庆理工大学（原重庆工学院更名）"),
    # 潼南时期
    ("bs_jiang_zhibin", "bs_gov_tongnan", "县委常委（挂职）", "2009-08", "2010-07", "副厅级", "潼南县"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "县委常委", "2010-07", "2012-01", "副厅级", "潼南县"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "县委常委、办公室主任", "2012-01", "2014-09", "副厅级", "潼南县"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "县委常委、常务副县长", "2014-09", "2015-06", "副厅级", "潼南县"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "区委常委、常务副区长", "2015-06", "2016-03", "副厅级", "潼南区（潼南撤县设区）"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "区委常委、常务副区长，兼区委工业园区工委书记", "2016-03", "2016-11", "副厅级", "潼南区"),
    ("bs_jiang_zhibin", "bs_gov_tongnan", "区委常委、常务副区长，兼区委党校校长、工业园区工委书记", "2016-11", "2017-01", "副厅级", "潼南区"),
    ("bs_jiang_zhibin", "bs_party_tongnan", "区委副书记，兼区委党校校长、工业园区工委书记", "2017-01", "2020-01", "正厅级（?）", "潼南区"),
    ("bs_jiang_zhibin", "bs_party_tongnan", "区委副书记，兼区委党校校长、高新区工委书记", "2020-01", "2021-09", "正厅级（?）", "潼南区"),
    # 璧山时期
    ("bs_jiang_zhibin", "bs_party_committee", "区委副书记、区长、区政府党组书记", "2021-09", "2024-11", "正厅级", "璧山区"),
    ("bs_jiang_zhibin", "bs_gov", "区委副书记、区长", "2021-09", "2024-11", "正厅级", "璧山区"),
    ("bs_jiang_zhibin", "bs_party_committee", "区委书记", "2024-11", "至今", "正厅级",
     "2024年10月25日任前公示（七一网），2024年11月正式任职。主持区委全面工作。"),

    # ═══ 唐军 — 区长 ═══
    ("bs_tang_jun", "bs_gov", "区长", "待查", "至今", "正厅级",
     "主持区政府全面工作。区委副书记、区政府党组书记。"),
    ("bs_tang_jun", "bs_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任区委副书记"),

    # ═══ 周树云 — 区委副书记 ═══
    ("bs_zhou_shuyun", "bs_party_committee", "区委副书记", "待查", "至今", "正厅级",
     "专职副书记。2026年7月出席全区会议。"),

    # ═══ 韩海燕 — 纪委书记 ═══
    ("bs_han_haiyan", "bs_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级",
     "2026年7月以案四说活动中围绕案例开展警示教育。"),
    ("bs_han_haiyan", "bs_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("bs_han_haiyan", "bs_supervision", "区监委主任", "待查", "至今", "副厅级", ""),

    # ═══ 李健 — 组织部长 ═══
    ("bs_li_jian", "bs_party_committee", "区委常委", "待查", "至今", "副厅级", ""),
    ("bs_li_jian", "bs_organization", "组织部部长", "待查", "至今", "正处级", "2026年6月29-30日参加七一慰问活动"),

    # ═══ 常爱书 — 副区长 ═══
    ("bs_chang_aishu", "bs_gov", "区政府副区长", "待查", "至今", "副厅级",
     "分管民政、养老等领域。2026年7月出席养老机构消防安全应急演练。"),

    # ═══ 刘全模 — 副区长 ═══
    ("bs_liu_quanmo", "bs_gov", "区政府副区长", "待查", "至今", "副厅级",
     "分管林业/林长制等工作。2026年7月在总河长总林长大会上安排林长制工作。"),

    # ═══ 万小力 — 副区长 ═══
    ("bs_wan_xiaoli", "bs_gov", "区政府副区长", "待查", "至今", "副厅级",
     "分管水利/河长制等工作。2026年7月在总河长总林长大会上安排河长制工作。"),

    # ═══ 张献强 — 人大主任 ═══
    ("bs_zhang_xianqiang", "bs_peoples_congress", "区人大常委会主任", "待查", "至今", "正厅级", ""),

    # ═══ 黄孝明 — 政协主席 ═══
    ("bs_huang_xiaoming", "bs_cppcc", "区政协主席", "待查", "至今", "正厅级", ""),

    # ═══ 前任领导 ═══
    # 前区委书记 — 秦文敏
    ("bs_qin_wenmin", "bs_party_committee", "前任区委书记", "2021-09", "2024-11", "正厅级",
     "2021年9月至2024年11月任璧山区委书记。现任重庆市政协经济委副主任。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence

    # ═══ 江志斌 ↔ 唐军 — 党政正职搭档 ═══
    ("bs_jiang_zhibin", "bs_tang_jun", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市璧山区委员会;重庆市璧山区人民政府", "至今",
     "strong", "confirmed"),

    # ═══ 江志斌 ↔ 周树云 — 书记-副书记 ═══
    ("bs_jiang_zhibin", "bs_zhou_shuyun", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市璧山区委员会", "至今",
     "strong", "confirmed"),

    # ═══ 唐军 ↔ 周树云 — 区长-副书记 ═══
    ("bs_tang_jun", "bs_zhou_shuyun", "overlap",
     "区长与区委副书记（区委区政府协调）",
     "中共重庆市璧山区委员会", "至今",
     "medium", "confirmed"),

    # ═══ 江志斌 ↔ 韩海燕 — 书记-纪委书记 ═══
    ("bs_jiang_zhibin", "bs_han_haiyan", "superior_subordinate",
     "区委书记与纪委书记",
     "中共重庆市璧山区委员会", "至今",
     "strong", "confirmed"),

    # ═══ 唐军 ↔ 常爱书 — 区长-副区长 ═══
    ("bs_tang_jun", "bs_chang_aishu", "superior_subordinate",
     "区长与分管民政的副区长",
     "重庆市璧山区人民政府", "至今",
     "medium", "confirmed"),

    # ═══ 唐军 ↔ 刘全模 — 区长-副区长 ═══
    ("bs_tang_jun", "bs_liu_quanmo", "superior_subordinate",
     "区长与分管林业的副区长",
     "重庆市璧山区人民政府", "至今",
     "medium", "confirmed"),

    # ═══ 唐军 ↔ 万小力 — 区长-副区长 ═══
    ("bs_tang_jun", "bs_wan_xiaoli", "superior_subordinate",
     "区长与分管水利的副区长",
     "重庆市璧山区人民政府", "至今",
     "medium", "confirmed"),

    # ═══ 江志斌 ↔ 张献强 — 区委-人大 ═══
    ("bs_jiang_zhibin", "bs_zhang_xianqiang", "overlap",
     "区委书记与区人大常委会主任（党政与人大协调）",
     "璧山区", "至今",
     "medium", "confirmed"),

    # ═══ 江志斌 ↔ 黄孝明 — 区委-政协 ═══
    ("bs_jiang_zhibin", "bs_huang_xiaoming", "overlap",
     "区委书记与区政协主席",
     "璧山区", "至今",
     "medium", "confirmed"),

    # ═══ 江志斌 ↔ 李健 — 书记-组织部长 ═══
    ("bs_jiang_zhibin", "bs_li_jian", "superior_subordinate",
     "区委书记与组织部部长",
     "中共重庆市璧山区委员会", "至今",
     "strong", "confirmed"),

    # ═══ 江志斌 — 前任书记（秦文敏） ═══
    ("bs_jiang_zhibin", "bs_qin_wenmin", "predecessor_successor",
     "江志斌接替秦文敏任璧山区委书记（2024年11月）",
     "中共重庆市璧山区委员会", "2024-11",
     "strong", "confirmed"),
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
            strength TEXT,
            confidence TEXT,
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
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
    return person_id in ("bs_jiang_zhibin", "bs_tang_jun", "bs_qin_wenmin")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("bs_jiang_zhibin", "bs_qin_wenmin"):
        return "255,50,50"       # Red — Party Secretary
    elif person_id == "bs_tang_jun":
        return "50,100,255"      # Blue — Government head
    elif person_id == "bs_han_haiyan":
        return "255,165,0"       # Orange — Discipline
    elif person_id in ("bs_zhang_xianqiang",):
        return "100,180,100"     # Green — Congress
    elif person_id in ("bs_huang_xiaoming",):
        return "100,180,100"     # Green — CPPCC
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "监察": "255,200,150",
        "党委部门": "255,220,220",
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
    lines.append('    <description>重庆市璧山区领导班子工作关系网络</description>')
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
    print(f"  重庆市璧山区 领导网络数据")
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
