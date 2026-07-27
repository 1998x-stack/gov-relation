#!/usr/bin/env python3
"""
正宁县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Zhengning County leadership network.

Level: 县
Province: 甘肃省
Parent city: 庆阳市
Region: 正宁县
Targets: 县委书记 & 县长

Research Sources:
- www.zhengning.gov.cn (正宁县人民政府官网 领导之窗, accessed 2026-07-22)
- 百度百科 — 程跟会、段军亮、贾志升
- 庆阳市领导网络 (已有研究数据)
- 正宁县人大会议公告

Confirmed officeholders (as of 2026-07-22, from www.zhengning.gov.cn):
- 县委书记: 程跟会 (2024年12月任，前正宁县县长)
- 县委副书记、县长: 段军亮 (2025年1月当选，前宁县常务副县长)

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "正宁县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "正宁县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "程跟会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "甘肃省静宁县",
        "native_place": "甘肃省静宁县",
        "education": "大学（西北师范大学政法系法学专业）",
        "party_join": "2004年12月",
        "work_start": "2001年2月",
        "current_post": "正宁县委书记",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗); 百度百科",
        "person_id": "zhengning_cheng_genhui"
    },
    {
        "id": "p02",
        "name": "段军亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委副书记、县政府党组书记、县长",
        "current_org": "正宁县人民政府",
        "source": "www.zhengning.gov.cn (领导之窗); 百度百科; 正宁县人大公告",
        "person_id": "zhengning_duan_junliang"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃省镇原县",
        "native_place": "甘肃省镇原县",
        "education": "大专（庆阳师专化学）/本科（兰州大学自考汉语言文学）/省委党校在职研究生",
        "party_join": "1999年11月",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市政府党组书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "百度百科 (贾志升); 酒泉市政府官网; 中国经济网",
        "person_id": "jiuquan_jia_zhisheng"
    },
    # ════════════════════════════════════════
    # Key Deputies (from government website)
    # ════════════════════════════════════════
    {
        "id": "p04",
        "name": "袁宏涛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委副书记",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_yuan_hongtao"
    },
    {
        "id": "p05",
        "name": "李红奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、县政府党组副书记、副县长",
        "current_org": "正宁县人民政府",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_li_hongkui"
    },
    {
        "id": "p06",
        "name": "袁冠锋",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、组织部部长",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_yuan_guanfeng"
    },
    {
        "id": "p07",
        "name": "孙嘉悦",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、宣传部部长",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_sun_jiayue"
    },
    {
        "id": "p08",
        "name": "周晶晶",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、政法委书记",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_zhou_jingjing"
    },
    {
        "id": "p09",
        "name": "章鼎",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、县政府党组成员、副县长",
        "current_org": "正宁县人民政府",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_zhang_ding"
    },
    {
        "id": "p10",
        "name": "杨小龙",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共正宁县委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_yang_xiaolong"
    },
    {
        "id": "p11",
        "name": "闫育平",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、纪委书记、监委代主任",
        "current_org": "中共正宁县纪律检查委员会",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_yan_yuping"
    },
    # 挂职干部（不纳入核心网络，但记录）
    {
        "id": "p12",
        "name": "李松",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、县政府党组成员、副县长（挂职）",
        "current_org": "正宁县人民政府",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_li_song"
    },
    {
        "id": "p13",
        "name": "杨济世",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "正宁县委常委、县政府党组成员、副县长（挂职）",
        "current_org": "正宁县人民政府",
        "source": "www.zhengning.gov.cn (领导之窗)",
        "person_id": "zhengning_yang_jishi"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共正宁县委员会", "type": "党委", "level": "县处级", "parent": "中共庆阳市委员会", "location": "甘肃省庆阳市正宁县山河镇"},
    {"id": "o02", "name": "正宁县人民政府", "type": "政府", "level": "县处级", "parent": "庆阳市人民政府", "location": "甘肃省庆阳市正宁县山河镇"},
    {"id": "o03", "name": "正宁县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "正宁县", "location": "甘肃省庆阳市正宁县山河镇"},
    {"id": "o04", "name": "中国人民政治协商会议正宁县委员会", "type": "政协", "level": "县处级", "parent": "正宁县", "location": "甘肃省庆阳市正宁县山河镇"},
    {"id": "o05", "name": "中共正宁县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共正宁县委员会", "location": "甘肃省庆阳市正宁县山河镇"},
    {"id": "o06", "name": "中共庆阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省庆阳市西峰区"},
    {"id": "o07", "name": "庆阳市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市西峰区"},
    {"id": "o08", "name": "中共宁县委员会", "type": "党委", "level": "县处级", "parent": "中共庆阳市委员会", "location": "甘肃省庆阳市宁县"},
    {"id": "o09", "name": "宁县人民政府", "type": "政府", "level": "县处级", "parent": "庆阳市人民政府", "location": "甘肃省庆阳市宁县"},
]

# 3. Positions
positions = [
    # ═══ 程跟会 (p01) ═══
    {"person_id": "p01", "org_id": "o01", "title": "正宁县委书记", "start": "2024-12", "end": "至今", "rank": "正处级", "note": "主持县委全面工作。2024年11月甘肃省委组织部任前公示拟任县委书记，2024年12月到任。"},
    {"person_id": "p01", "org_id": "o02", "title": "正宁县人民政府县长（前职）", "start": "2021-08", "end": "2024-12", "rank": "正处级", "note": "原任县长，2021年8月任代县长，后当选；2024年12月辞去县长职务"},
    {"person_id": "p01", "org_id": "o01", "title": "正宁县委副书记（前职）", "start": "2021-08", "end": "2024-12", "rank": "副处级", "note": "兼任县政府党组书记"},
    # ═══ 段军亮 (p02) ═══
    {"person_id": "p02", "org_id": "o02", "title": "正宁县人民政府县长", "start": "2025-01-21", "end": "至今", "rank": "正处级", "note": "2025年1月21日正宁县第十八届人大四次会议当选"},
    {"person_id": "p02", "org_id": "o02", "title": "正宁县人民政府副县长、代县长（前职）", "start": "2024-12-31", "end": "2025-01-21", "rank": "正处级", "note": "2024年12月31日县人大常委会任命"},
    {"person_id": "p02", "org_id": "o01", "title": "正宁县委副书记", "start": "2024-12", "end": "至今", "rank": "副处级", "note": "兼任县政府党组书记"},
    {"person_id": "p02", "org_id": "o09", "title": "宁县县委常委、常务副县长（前职）", "start": "待查", "end": "2024-12", "rank": "副处级", "note": "调任正宁前的职务"},
    # ═══ 贾志升 (p03) ═══
    {"person_id": "p03", "org_id": "o01", "title": "正宁县委书记（前职）", "start": "2020-04", "end": "2021-08", "rank": "正处级", "note": "主政正宁县。2021年8月跨市调任白银市副市长"},
    {"person_id": "p03", "org_id": "o06", "title": "庆阳市农业农村局局长（前职）", "start": "2019-02", "end": "2020-04", "rank": "正处级", "note": "任正宁县委书记前的职务"},
    # ═══ 袁宏涛 (p04) ═══
    {"person_id": "p04", "org_id": "o01", "title": "正宁县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": "县委专职副书记"},
    # ═══ 李红奎 (p05) ═══
    {"person_id": "p05", "org_id": "o02", "title": "正宁县委常委、县政府党组副书记、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": "常务副县长"},
    # ═══ 袁冠锋 (p06) ═══
    {"person_id": "p06", "org_id": "o01", "title": "正宁县委常委、组织部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 孙嘉悦 (p07) ═══
    {"person_id": "p07", "org_id": "o01", "title": "正宁县委常委、宣传部部长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 周晶晶 (p08) ═══
    {"person_id": "p08", "org_id": "o01", "title": "正宁县委常委、政法委书记", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 章鼎 (p09) ═══
    {"person_id": "p09", "org_id": "o02", "title": "正宁县委常委、县政府党组成员、副县长", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 杨小龙 (p10) ═══
    {"person_id": "p10", "org_id": "o01", "title": "正宁县委常委、统战部部长、县政协党组副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 闫育平 (p11) ═══
    {"person_id": "p11", "org_id": "o05", "title": "正宁县委常委、纪委书记、监委代主任", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    # ═══ 李松 (p12, 挂职) ═══
    {"person_id": "p12", "org_id": "o02", "title": "正宁县委常委、县政府党组成员、副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "挂职干部"},
    # ═══ 杨济世 (p13, 挂职) ═══
    {"person_id": "p13", "org_id": "o02", "title": "正宁县委常委、县政府党组成员、副县长（挂职）", "start": "待查", "end": "至今", "rank": "副处级", "note": "挂职干部"},
]

# 4. Relationships
relationships = [
    # 现任班子核心关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "程跟会(书记)与段军亮(县长): 正宁县党政一把手配合", "overlap_org": "中共正宁县委员会/正宁县人民政府", "overlap_period": "2024-12至今", "strength": "strong", "confidence": "confirmed"},
    # 前后任关系
    {"person_a": "p01", "person_b": "p03", "type": "predecessor_successor", "context": "程跟会接替贾志升: 程跟会是贾志升的第二任继任者（程先于2021.08接县长，后于2024.12升书记）", "overlap_org": "中共正宁县委员会", "overlap_period": "2021-08/2024-12", "strength": "strong", "confidence": "confirmed"},
    # 程跟会—袁宏涛：党政正副配合
    {"person_a": "p01", "person_b": "p04", "type": "overlap", "context": "程跟会(书记)与袁宏涛(副书记): 县委书记与专职副书记配合", "overlap_org": "中共正宁县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 县长—常务副县长
    {"person_a": "p02", "person_b": "p05", "type": "overlap", "context": "段军亮(县长)与李红奎(常务副县长): 县政府正副配合", "overlap_org": "正宁县人民政府", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 县委常委班子内部关系
    {"person_a": "p01", "person_b": "p06", "type": "overlap", "context": "程跟会(书记)与袁冠锋(组织部长): 书记与组织部长配合", "overlap_org": "中共正宁县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p07", "type": "overlap", "context": "程跟会(书记)与孙嘉悦(宣传部长): 书记与宣传部长配合", "overlap_org": "中共正宁县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p08", "type": "overlap", "context": "程跟会(书记)与周晶晶(政法委书记): 书记与政法委书记配合", "overlap_org": "中共正宁县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p10", "type": "overlap", "context": "程跟会(书记)与杨小龙(统战部长): 书记与统战部长配合", "overlap_org": "中共正宁县委员会", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p11", "type": "overlap", "context": "程跟会(书记)与闫育平(纪委书记): 书记与纪委书记配合", "overlap_org": "中共正宁县委员会/中共正宁县纪委", "overlap_period": "当前在任", "strength": "strong", "confidence": "confirmed"},
    # 贾志升庆阳网络
    {"person_a": "p03", "person_b": "p01", "type": "promotion_chain", "context": "贾志升(前任书记)→程跟会(继任县长后升书记): 贾志升离任后，程跟会从外部调任县长并后续升任书记", "overlap_org": "正宁县", "overlap_period": "2020-2024", "strength": "medium", "confidence": "plausible"},
    # 宁县-正宁干部交流
    {"person_a": "p02", "person_b": "p03", "type": "same_system", "context": "段军亮(曾任宁县常务副县长)与贾志升(曾任正宁县委书记、宁县县委副书记): 两人都有宁县工作经历", "overlap_org": "宁县/正宁县", "overlap_period": "2012-2024", "strength": "medium", "confidence": "plausible"},
]

# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on current_post."""
    title = p["current_post"]
    if "县委书记" in title and "纪委" not in title and "统战" not in title and "宣传" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"   # Blue — County Mayor
    if "县长" in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副县长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "县委书记" in title and "纪委" not in title and "统战" not in title and "宣传" not in title:
        return "20.0"
    if "县长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副县长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>正宁县领导班子工作关系网络 - 数据来源: 正宁县人民政府官网及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="正宁县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="正宁县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──

def main():
    print(f"=== 正宁县网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
