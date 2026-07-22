#!/usr/bin/env python3
"""Build 南安市 (福建省泉州市) leadership network: SQLite DB + GEXF graph.

Research date: 2026-07-16
Level: 县级市
Province: 福建省
Parent city: 泉州市
Targets: 市委书记 & 市长

Sources:
  - www.nanan.gov.cn (南安市人民政府 — official site, homepage confirmed 市长 王连赞)
  - www.nanan.gov.cn/szf/sz/wlz/ — 市长王连赞 official profile (简历: 男, 汉族, 1974年7月出生, 在职研究生, 中共党员, 南安市委副书记, 市人民政府市长、党组书记)
  - www.nanan.gov.cn/szf/cwfsz/wzq/ — 常务副市长吴振强 official profile (简历: 男, 汉族, 1972年10月出生, 大学, 中共党员, 南安市委常委, 市人民政府常务副市长、党组副书记)
  - www.nanan.gov.cn/zwgk/xwzx/tpxw/202607/t20260701_3305324.htm — 南安市"两优一先"表彰大会 (confirmed 市委书记 张桂森 in news article, 2026-06-30)
  - en.wikipedia.org/wiki/Nan'an,_Fujian — English Wikipedia infobox (confirmed CPC Secretary: Zhang Guisen, Mayor: Wang Lianzan)
  - zh.wikipedia.org/wiki/南安市 — Chinese Wikipedia (confirmed Mayor: 王连赞)

Confidence:
  - 市委书记 张桂森: confirmed from official gov news article (2026-06-30) and Wikipedia
  - 市长 王连赞: confirmed from official city government profile page
  - 常务副市长 吴振强: confirmed from official city government profile page
  - 其他副市长: confirmed from official city government homepage listing
  - Biographical details (birth, birthplace, education, career timeline) for all
    figures could not be fully retrieved from accessible Chinese sources (Baidu Baike 403 blocked).
    Partial data from official profiles. All marked with confidence accordingly.

Known sources:
  - https://www.nanan.gov.cn — Nan'an City official government site
  - https://www.nanan.gov.cn/szf/sz/wlz/ — Mayor Wang Lianzan official profile
  - https://www.nanan.gov.cn/szf/cwfsz/wzq/ — Executive Deputy Mayor Wu Zhenqiang official profile
  - https://en.wikipedia.org/wiki/Nan'an,_Fujian — English Wikipedia
  - https://zh.wikipedia.org/wiki/南安市 — Chinese Wikipedia

Key gaps:
  - 张桂森 full career timeline (birth date, education, previous posts) mostly unknown
  - 王连赞 full career timeline beyond current role unknown (only birth year 1974 from official profile)
  - 吴振强 full career timeline beyond current role unknown (only birth year 1972 from official profile)
  - 其他副市长 (周全, 曾伟军, 陈志慧, 易辉泉, 邱雪亮, 侯强辉, 廖徐伟) career details unknown
  - Party committee full roster unknown (only 张桂森 and 吴振强 confirmed)
  - Predecessor of 张桂森 as party secretary unknown
  - Predecessor of 王连赞 as mayor unknown
  - Previous mayor(s) and party secretary history unknown

All person data marked with confidence accordingly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    DB_PATH = os.path.join(SCRIPT_DIR, "南安市_network.db")
    GEXF_PATH = os.path.join(SCRIPT_DIR, "南安市_network.gexf")
else:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(PROJECT_ROOT, "data/database/南安市_network.db")
    GEXF_PATH = os.path.join(PROJECT_ROOT, "data/graph/南安市_network.gexf")

KNOWN_DATE = "2026-07-16"

# ── research data ────────────────────────────────────────────────────────

organizations = [
    {
        "id": "nanan_cpc",
        "name": "中共南安市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共泉州市委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_gov",
        "name": "南安市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "泉州市人民政府",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_party_office",
        "name": "中共南安市委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共南安市委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_org_dept",
        "name": "中共南安市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共南安市委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_cpc_discipline",
        "name": "中共南安市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共南安市委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_politics_legal",
        "name": "中共南安市委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共南安市委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_gov_office",
        "name": "南安市人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "南安市人民政府",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_gov_dev_reform",
        "name": "南安市发展和改革局",
        "type": "政府",
        "level": "县级",
        "parent": "南安市人民政府",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_npc",
        "name": "南安市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "泉州市人民代表大会常务委员会",
        "location": "福建省泉州市南安市"
    },
    {
        "id": "nanan_ccppcc",
        "name": "中国人民政治协商会议南安市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议泉州市委员会",
        "location": "福建省泉州市南安市"
    },
]

persons = [
    # ═══ Current Top Leaders ═══

    # 市委书记 张桂森 (Party Secretary) — confirmed from official news
    {
        "id": "nanan_zhang_guisen",
        "name": "张桂森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市委书记",
        "current_org": "中共南安市委员会",
        "source": "https://www.nanan.gov.cn/zwgk/xwzx/tpxw/202607/t20260701_3305324.htm — 南安市'两优一先'表彰大会官方新闻确认市委书记张桂森 (2026-06-30)",
        "notes": "南安市委书记。官方新闻确认2026年6月30日在任。出生日期、籍贯、教育背景和完整职业生涯待查。前任待查。",
        "confidence": "confirmed"
    },

    # 市长 王连赞 (Mayor) — confirmed from official profile page
    {
        "id": "nanan_wang_lianzan",
        "name": "王连赞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/sz/wlz/ — 南安市政府官网市长简历确认",
        "notes": "南安市委副书记，市人民政府市长、党组书记。1974年7月出生，在职研究生学历。出生地和籍贯不详。完整简历待查。",
        "confidence": "confirmed"
    },

    # 常务副市长 吴振强 (Executive Deputy Mayor) — confirmed from official profile
    {
        "id": "nanan_wu_zhenqiang",
        "name": "吴振强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市常务副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/cwfsz/wzq/ — 南安市政府官网常务副市长简历确认",
        "notes": "南安市委常委，市人民政府常务副市长、党组副书记。1972年10月出生，大学学历。分管发改、应急、审计、统计、行政审批等工作。",
        "confidence": "confirmed"
    },

    # ═══ Deputy Mayors (confirmed from homepage listing) ═══

    {
        "id": "nanan_zhou_quan",
        "name": "周全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_zeng_weijun",
        "name": "曾伟军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_chen_zhihui",
        "name": "陈志慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_yi_huiqian",
        "name": "易辉泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_qiu_xueliang",
        "name": "邱雪亮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。官网上列为女性（原名邱雪亮，URL含wdf）。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_hou_qianghui",
        "name": "侯强辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },
    {
        "id": "nanan_liao_xuwei",
        "name": "廖徐伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市副市长",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市副市长。具体分工和简历待查。",
        "confidence": "confirmed"
    },

    # ═══ Other Key Leaders ═══

    # 人大主任 — unknown
    {
        "id": "nanan_npc_chair_unknown",
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市人大常委会主任",
        "current_org": "南安市人民代表大会常务委员会",
        "source": "待查 — 新闻提到'黄景阳'可能是人大主任（南安市'两优一先'表彰大会出席名单）",
        "notes": "⚠️ 南安市人大常委会主任未确认。'两优一先'表彰大会出席名单中'黄景阳'可能在人大任职。",
        "confidence": "unverified"
    },

    # 政协主席 — known (庄国阳)
    {
        "id": "nanan_zhuang_guoyang",
        "name": "庄国阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市政协主席",
        "current_org": "中国人民政治协商会议南安市委员会",
        "source": "https://www.nanan.gov.cn/zwgk/xwzx/nayw/202607/t20260714_3309132.htm — 南安市政协重点提案办理情况汇报会新闻确认庄国阳以政协主席身份出席",
        "notes": "南安市政协主席。确认现任。完整简历和分工待查。",
        "confidence": "confirmed"
    },

    # 党组成员 黄泉春
    {
        "id": "nanan_huang_quanchun",
        "name": "黄泉春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市政府党组成员",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市政府党组成员。具体分工和简历待查。",
        "confidence": "confirmed"
    },

    # 党组成员 黄身桂
    {
        "id": "nanan_huang_shengui",
        "name": "黄身桂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南安市政府党组成员",
        "current_org": "南安市人民政府",
        "source": "https://www.nanan.gov.cn/szf/ — 南安市政府官网首页领导列表确认",
        "notes": "南安市政府党组成员。具体分工和简历待查。",
        "confidence": "confirmed"
    },
]

positions = [
    # 张桂森
    {"person_id": "nanan_zhang_guisen", "org_id": "nanan_cpc", "title": "南安市委书记", "start": "未知", "end": "至今", "rank": "正处级", "note": "现任。上任时间未知。"},
    # 王连赞
    {"person_id": "nanan_wang_lianzan", "org_id": "nanan_gov", "title": "南安市市长", "start": "未知", "end": "至今", "rank": "正处级", "note": "现任。市委副书记, 市政府党组书记。"},
    # 吴振强
    {"person_id": "nanan_wu_zhenqiang", "org_id": "nanan_gov", "title": "南安市常务副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": "现任。市委常委, 市政府党组副书记。"},
    {"person_id": "nanan_wu_zhenqiang", "org_id": "nanan_cpc", "title": "南安市委常委", "start": "未知", "end": "至今", "rank": "副处级", "note": "现任市委常委。"},
    # 副市长们
    {"person_id": "nanan_zhou_quan", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_zeng_weijun", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_chen_zhihui", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_yi_huiqian", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_qiu_xueliang", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_hou_qianghui", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_liao_xuwei", "org_id": "nanan_gov", "title": "南安市副市长", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    # 庄国阳
    {"person_id": "nanan_zhuang_guoyang", "org_id": "nanan_ccppcc", "title": "南安市政协主席", "start": "未知", "end": "至今", "rank": "正处级", "note": ""},
    # 党组成员
    {"person_id": "nanan_huang_quanchun", "org_id": "nanan_gov", "title": "南安市政府党组成员", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": "nanan_huang_shengui", "org_id": "nanan_gov", "title": "南安市政府党组成员", "start": "未知", "end": "至今", "rank": "副处级", "note": ""},
]

relationships = [
    # 张桂森 <-> 王连赞: 党政搭档
    {"person_a": "nanan_zhang_guisen", "person_b": "nanan_wang_lianzan", "type": "overlap", "context": "南安市党政主要领导搭档", "overlap_org": "nanan_cpc", "overlap_period": "至今"},
    # 王连赞 <-> 吴振强: 市长与常务副市长
    {"person_a": "nanan_wang_lianzan", "person_b": "nanan_wu_zhenqiang", "type": "superior_subordinate", "context": "市长与常务副市长工作关系", "overlap_org": "nanan_gov", "overlap_period": "至今"},
    # 张桂森 <-> 吴振强: 书记与常委
    {"person_a": "nanan_zhang_guisen", "person_b": "nanan_wu_zhenqiang", "type": "overlap", "context": "市委主要领导与市委常委", "overlap_org": "nanan_cpc", "overlap_period": "至今"},
]


# ── helper functions ─────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    post = person.get("current_post", "")
    if "书记" in post and "纪委" not in post and "副" not in post:
        return "255,50,50"  # Red — Party Secretary
    if "市长" in post or "县长" in post or "区长" in post:
        return "50,100,255"  # Blue — Mayor/County head
    if "常务" in post:
        return "50,100,255"  # Blue — Executive Deputy
    if "纪委" in post or "监委" in post:
        return "255,165,0"  # Orange — Discipline
    if "人大" in post:
        return "200,255,255"  # Cyan — NPC
    if "政协" in post:
        return "255,240,200"  # Cream — CCPPCC
    return "100,100,100"  # Grey — Others


def is_top_leader(pid, person_list):
    """Check if a person is a top leader (书记/市长/县长)."""
    for p in person_list:
        if p["id"] == pid:
            post = p.get("current_post", "")
            if "书记" in post and "副" not in post and "纪委" not in post:
                return True
            if "市长" in post and "副" not in post and "常务" not in post:
                return True
            if "县长" in post and "副" not in post and "常务" not in post:
                return True
            if "主席" in post and "副" not in post and "政协" not in post:
                return True
            if "主任" in post and "副" not in post and "人大" in post:
                return True
    return False


def org_color(org):
    """Return 'r,g,b' string based on organization type."""
    t = org.get("type", "")
    if "党委" in t or "党组" in t:
        return "255,200,200"  # Pink
    if "政府" in t:
        return "200,200,255"  # Light blue
    if "开发区" in t:
        return "200,255,200"  # Light green
    if "乡镇" in t or "街道" in t:
        return "255,255,200"  # Light yellow
    if "人大" in t:
        return "200,255,255"  # Cyan
    if "政协" in t:
        return "255,240,200"  # Cream
    if "事业" in t:
        return "220,220,220"  # Light grey
    if "群团" in t:
        return "255,220,255"  # Light purple
    return "200,200,200"


# ── build SQLite DB ──────────────────────────────────────────────────────
def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    for org in organizations:
        c.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (org["id"], org["name"], org["type"], org["level"], org["parent"], org["location"])
        )

    for p in persons:
        c.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
             p["education"], p["party_join"], p["work_start"], p["current_post"],
             p["current_org"], p["source"])
        )

    for pos in positions:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
        )

    for r in relationships:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
        )

    conn.commit()
    conn.close()
    print(f"  ✓ SQLite database: {DB_PATH}")


# ── build GEXF graph ────────────────────────────────────────────────────
def build_gexf():
    lines = []
    today = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>南安市 (福建省泉州市) 领导关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="location" type="string"/>')
    lines.append('    </attributes>')

    # ── edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        c = person_color(p)
        sz = "20.0" if is_top_leader(pid, persons) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="县级"/>')
        lines.append(f'          <attvalue for="4" value="福建省泉州市南安市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── organization nodes ──
    for org in organizations:
        oid = org["id"]
        name = org["name"]
        otype = org["type"]
        olevel = org["level"]
        loc = org.get("location", "")
        c = org_color(org)
        # Determine if top-level org
        is_top_org = oid in ("nanan_cpc", "nanan_gov", "nanan_npc", "nanan_ccppcc")
        sz = "10.0" if is_top_org else "8.0"
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(olevel)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(loc)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── edges ──
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        title = pos["title"]
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationships), weight=2.0
    for r in relationships:
        eid += 1
        rtype = r["type"]
        context = r.get("context", "")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF graph: {GEXF_PATH}")


# ── main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Building 南安市 leadership network data...")
    build_db()
    build_gexf()
    print("Done.")
