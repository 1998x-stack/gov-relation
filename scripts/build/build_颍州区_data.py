#!/usr/bin/env python3
"""Build 颍州区 (Yingzhou District, Fuyang, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_颍州区 (安徽阜阳市颍州区 - 市辖区)

Confirmed officeholders:
  - 区委书记: 童坤 (1976-10, 安徽凤台人), appointed 2026-03
  - 区长: 王许 (1982-10, ), elected 2026-06-13

Predecessors:
  - 前任区委书记: 段相霖 (1972-11, 安徽界首人), served ~2022-03 to 2024-10; later 
    removed for corruption (2025-04 investigated, 2025-12 prosecuted)
  - 更前任区委书记: 张华久 (1965-10, 安徽阜南人), now 阜阳市政协党组副书记、副主席
  - 童坤 also served as 颍州区区长 (2025-01 to 2026-03) before becoming 区委书记

Sources:
  - https://baike.baidu.com/item/颍州区/5959477 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/童坤/55867517 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/王许/65047580 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/段相霖 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/张华久 (Baidu Baike, accessed 2026-07-15)
  - 中安在线 2026-06-13: 王许当选阜阳市颍州区区长

Confidence: Core leader identities and career timelines for 童坤 and 王许 confirmed
from Baidu Baike. 段相霖's career and corruption case confirmed. 张华久's basic info
confirmed. Leadership team members beyond the top 2 are partially known pending 
official government website access.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "颍州区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "颍州区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 区委书记 童坤（2026年3月拟任，现为区委书记）
    {
        "id": "yingzhou_tong_kun",
        "name": "童坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "安徽凤台",
        "native_place": "安徽凤台",
        "education": "大学（计算机软件），合肥工业大学公共管理硕士",
        "party_join": "1999-01",
        "work_start": "1999-07",
        "current_post": "颍州区委书记（一级调研员）",
        "current_org": "中共阜阳市颍州区委员会",
        "source": "https://baike.baidu.com/item/%E7%AB%A5%E5%9D%A4/55867517",
        "notes": "1976年10月生，安徽凤台人。1999年7月参加工作，1999年1月入党。1995-1999安徽大学计算机系计算机软件专业。历任阜阳市地税局信息中心副主任（主持工作）、主任，阜阳市邮政管理局行业管理科科长、党组成员，界首邮政管理局局长，亳州市邮政管理局党组成员、副局长、纪检组长，马鞍山市邮政管理局党组书记、局长，阜阳市邮政管理局党组书记、局长，阜阳市交通运输局党组成员、副局长（兼），阜阳市数据资源管理局（市政务服务管理局）局长。2022年9月任阜阳市数据资源管理局局长。后任颍州区委副书记（正处级）、党校校长，颍州区代区长。2025年1月任颍州区区长。2026年3月拟任县（市、区）党委正职，现任颍州区委书记，一级调研员。主持区委全面工作。",
        "confidence": "confirmed"
    },
    # 区长 王许（2026年6月13日当选）
    {
        "id": "yingzhou_wang_xu",
        "name": "王许",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生，安徽工业大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "颍州区委副书记、区长",
        "current_org": "颍州区人民政府",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E8%AE%B8/65047580",
        "notes": "1982年10月出生，汉族，省委党校研究生学历，安徽工业大学毕业，中共党员。曾任马鞍山市博望区委副书记（正处级）。2026年5月13日任颍州区副区长、代区长。2026年6月13日当选颍州区区长。领导区政府全面工作。",
        "confidence": "confirmed"
    },

    # ═══ Former Leaders (Predecessors) ═══

    # 前任区委书记 段相霖（被查）
    {
        "id": "yingzhou_duan_xianglin",
        "name": "段相霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "安徽界首",
        "native_place": "安徽界首",
        "education": "上海交通大学技术经济专业，省委党校在职法学研究生",
        "party_join": "中共党员",
        "work_start": "1996-07",
        "current_post": "（原阜阳师范大学党委副书记，已被双开）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E6%AE%B5%E7%9B%B8%E9%9C%96",
        "notes": "1972年11月生，安徽界首人。1996年7月参加工作，上海交通大学经济管理与决策科学系技术经济专业毕业。历任安徽省经贸委科员，阜阳市经贸委/经信委科长、副主任，临泉县委常委、常务副县长，阜阳市财政局局长，阜阳经开区党工委书记、管委会主任，2022年3月兼任颍州区委书记。2024年10月任阜阳师范大学党委副书记。2025年4月因涉嫌严重违纪违法接受审查调查，2025年10月被双开，2025年12月因涉嫌受贿罪被提起公诉。",
        "confidence": "confirmed"
    },
    # 更前任区委书记 张华久
    {
        "id": "yingzhou_zhang_huajiu",
        "name": "张华久",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "安徽阜南",
        "native_place": "安徽阜南",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜阳市政协党组副书记、副主席",
        "current_org": "阜阳市政协",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%8D%8E%E4%B9%85",
        "notes": "1965年10月生，安徽阜南人，汉族。曾任颍州区委书记。现任安徽省阜阳市政协党组副书记、副主席。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": "yingzhou_party_committee",
        "name": "中共阜阳市颍州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阜阳市委",
        "location": "阜阳市颍州区"
    },
    {
        "id": "yingzhou_government",
        "name": "颍州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市颍州区"
    },
    {
        "id": "yingzhou_npc",
        "name": "阜阳市颍州区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "阜阳市人大常委会",
        "location": "阜阳市颍州区"
    },
    {
        "id": "yingzhou_cppcc",
        "name": "阜阳市颍州区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "阜阳市政协",
        "location": "阜阳市颍州区"
    },
    {
        "id": "yingzhou_cdc",
        "name": "中共阜阳市颍州区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共阜阳市纪委",
        "location": "阜阳市颍州区"
    },
    {
        "id": "fuyang_government",
        "name": "阜阳市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_party",
        "name": "中共阜阳市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共安徽省委",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_data_bureau",
        "name": "阜阳市数据资源管理局（市政务服务管理局）",
        "type": "政府",
        "level": "地级市",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_post_bureau",
        "name": "阜阳市邮政管理局",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省邮政管理局",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_transport_bureau",
        "name": "阜阳市交通运输局",
        "type": "政府",
        "level": "地级市",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_tax_bureau",
        "name": "阜阳市地税局",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省地税局",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_economic_committee",
        "name": "阜阳市经济和信息化委员会",
        "type": "政府",
        "level": "地级市",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_finance_bureau",
        "name": "阜阳市财政局（市政府国有资产监督管理委员会）",
        "type": "政府",
        "level": "地级市",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_development_zone",
        "name": "阜阳经济技术开发区",
        "type": "开发区",
        "level": "国家级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市"
    },
    {
        "id": "fuyang_cppcc",
        "name": "阜阳市政协",
        "type": "政协",
        "level": "地级市",
        "parent": "安徽省政协",
        "location": "阜阳市"
    },
    {
        "id": "linquan_county_gov",
        "name": "临泉县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阜阳市人民政府",
        "location": "阜阳市临泉县"
    },
    {
        "id": "fuyang_normal_university",
        "name": "阜阳师范大学",
        "type": "事业单位",
        "level": "厅级",
        "parent": "安徽省教育厅",
        "location": "阜阳市"
    },
    {
        "id": "maanshan_bowang_party",
        "name": "中共马鞍山市博望区委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共马鞍山市委",
        "location": "马鞍山市博望区"
    },
]

positions = [
    # 童坤 - 现任
    ("yingzhou_tong_kun", "yingzhou_party_committee", "颍州区委书记（一级调研员）", "2026-03", "", "正处级", "主持区委全面工作"),
    # 童坤 - 曾任颍州区区长
    ("yingzhou_tong_kun", "yingzhou_government", "颍州区人民政府区长", "2025-01", "2026-03", "正处级", ""),
    ("yingzhou_tong_kun", "yingzhou_government", "颍州区人民政府代区长", "2024", "2025-01", "正处级", ""),
    ("yingzhou_tong_kun", "yingzhou_party_committee", "颍州区委副书记（正处级）、党校校长", "2024", "2025", "正处级", ""),
    # 童坤 - 数据资源管理局
    ("yingzhou_tong_kun", "fuyang_data_bureau", "阜阳市数据资源管理局（市政务服务管理局）局长", "2022-09", "2024-06", "正处级", ""),
    # 童坤 - 邮政系统
    ("yingzhou_tong_kun", "fuyang_post_bureau", "阜阳市邮政管理局党组书记、局长", "2020-04", "2022-09", "正处级", ""),
    ("yingzhou_tong_kun", "fuyang_transport_bureau", "阜阳市交通运输局党组成员、副局长（兼）", "2020-04", "2022", "副处级", "兼管邮政管理局"),
    ("yingzhou_tong_kun", "fuyang_post_bureau", "阜阳市邮政管理局党组书记、局长", "2020-03", "2020-04", "正处级", ""),
    # 童坤 - 马鞍山邮政
    ("yingzhou_tong_kun", "fuyang_post_bureau", "马鞍山市邮政管理局党组书记、局长", "2019-07", "2020-03", "正处级", ""),
    ("yingzhou_tong_kun", "fuyang_post_bureau", "马鞍山市邮政管理局党组成员、副局长（主持工作）", "2018-12", "2019-07", "副处级", ""),
    # 童坤 - 亳州邮政
    ("yingzhou_tong_kun", "fuyang_post_bureau", "亳州市邮政管理局党组成员、副局长、纪检组长", "2017-06", "2018-12", "副处级", ""),
    # 童坤 - 阜阳邮政
    ("yingzhou_tong_kun", "fuyang_post_bureau", "阜阳市邮政管理局党组成员、行业管理科科长、界首邮政管理局局长", "2015-09", "2017-06", "副处级", ""),
    ("yingzhou_tong_kun", "fuyang_post_bureau", "阜阳市邮政管理局党组成员、行业管理科科长", "2014-04", "2015-09", "正科级", ""),
    ("yingzhou_tong_kun", "fuyang_post_bureau", "阜阳市邮政管理局行业管理科科长", "2013-04", "2014-04", "正科级", ""),
    # 童坤 - 地税系统
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局信息中心主任", "2012-03", "2013-04", "正科级", ""),
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局信息中心副主任（主持工作）", "2011-01", "2012-03", "副科级", ""),
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局信息中心副主任", "2005-11", "2011-01", "副科级", ""),
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局信息中心科员", "2001-04", "2005-11", "科员", ""),
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局计会科科员", "2000-11", "2001-04", "科员", ""),
    ("yingzhou_tong_kun", "fuyang_tax_bureau", "阜阳市地税局直属分局科员", "1999-07", "2000-11", "科员", ""),

    # 王许 - 现任
    ("yingzhou_wang_xu", "yingzhou_government", "颍州区委副书记、区长", "2026-06", "", "正处级", "领导区政府全面工作"),
    ("yingzhou_wang_xu", "yingzhou_government", "颍州区人民政府副区长、代区长", "2026-05", "2026-06", "正处级", ""),
    # 王许 - 前任
    ("yingzhou_wang_xu", "maanshan_bowang_party", "马鞍山市博望区委副书记（正处级）", "", "2026-05", "正处级", ""),

    # 段相霖 - 前任区委书记
    ("yingzhou_duan_xianglin", "yingzhou_party_committee", "颍州区委书记（兼阜阳经开区党工委书记、管委会主任）", "2022-03", "2024-10", "正处级", "2025年4月被查"),
    ("yingzhou_duan_xianglin", "fuyang_development_zone", "阜阳经开区党工委书记、管委会主任", "2022-03", "2024-10", "正处级", ""),
    ("yingzhou_duan_xianglin", "fuyang_finance_bureau", "阜阳市财政局（市政府国资委）局长（主任）", "2019-03", "2021-06", "正处级", ""),
    ("yingzhou_duan_xianglin", "fuyang_economic_committee", "阜阳市经济和信息化委员会副主任、党组成员", "2011-05", "2014-10", "副处级", ""),
    ("yingzhou_duan_xianglin", "linquan_county_gov", "临泉县委常委、常务副县长", "2014-11", "2016-06", "副处级", ""),
    ("yingzhou_duan_xianglin", "fuyang_normal_university", "阜阳师范大学党委副书记", "2024-10", "2025-04", "厅级", "2025年10月被双开"),

    # 张华久 - 更前任
    ("yingzhou_zhang_huajiu", "yingzhou_party_committee", "颍州区委书记", "", "2021", "正处级", ""),
    ("yingzhou_zhang_huajiu", "fuyang_cppcc", "阜阳市政协党组副书记、副主席", "", "", "副厅级", "现任"),
]

relationships = [
    # 童坤 ↔ 王许（党政正职搭档）
    {
        "person_a": "yingzhou_tong_kun",
        "person_b": "yingzhou_wang_xu",
        "type": "party_government_leadership",
        "strength": "strong",
        "context": "区委书记与区长（党政正职搭档）",
        "overlap_org": "颍州区四套班子",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    # 童坤 ↔ 段相霖（前任继任）
    {
        "person_a": "yingzhou_tong_kun",
        "person_b": "yingzhou_duan_xianglin",
        "type": "predecessor_successor",
        "strength": "strong",
        "context": "童坤接替段相霖担任颍州区委书记",
        "overlap_org": "中共阜阳市颍州区委员会",
        "overlap_period": "2022-2026",
        "note": "confirmed"
    },
    # 段相霖 ↔ 张华久（前任继任）
    {
        "person_a": "yingzhou_duan_xianglin",
        "person_b": "yingzhou_zhang_huajiu",
        "type": "predecessor_successor",
        "strength": "strong",
        "context": "段相霖接替张华久担任颍州区委书记",
        "overlap_org": "中共阜阳市颍州区委员会",
        "overlap_period": "~2021-2022",
        "note": "confirmed"
    },
    # 童坤曾担任区长，王许接任区长（前任继任）
    {
        "person_a": "yingzhou_tong_kun",
        "person_b": "yingzhou_wang_xu",
        "type": "predecessor_successor",
        "strength": "strong",
        "context": "童坤升任区委书记后，王许接任区长",
        "overlap_org": "颍州区人民政府",
        "overlap_period": "2026",
        "note": "confirmed"
    },
    # 段相霖 ↔ 童坤（上下级：段曾是童的上级）
    {
        "person_a": "yingzhou_duan_xianglin",
        "person_b": "yingzhou_tong_kun",
        "type": "superior_subordinate",
        "strength": "medium",
        "context": "段相霖担任区委书记期间，童坤曾任区委副书记、区长",
        "overlap_org": "颍州区四套班子",
        "overlap_period": "2024-2024.10",
        "note": "confirmed"
    },
]


# ══════════════════════════════════════════════════════════════════════
# Database + Graph Builder
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b color string based on role."""
    name = p.get("current_post", "")
    if "区委书记" in name:
        return "255,50,50"
    elif "区长" in name:
        return "50,100,255"
    elif "纪委书记" in name or "纪委" in name:
        return "255,165,0"
    elif "人大" in name:
        return "200,255,255"
    elif "政协" in name:
        return "255,240,200"
    else:
        return "100,100,100"


def org_color(o):
    """Return r,g,b color string based on org type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "纪委" in t:
        return "255,165,0"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "群团" in t:
        return "255,220,255"
    else:
        return "220,220,220"


def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
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
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
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
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>颍州区（阜阳市）领导班子工作关系网络 — 2026年7月研究数据</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        birth = p["birth"]
        conf = p["confidence"]
        c = person_color(p)
        is_top = "区委书记" in post or ("区长" in post and "副书记" in post)
        sz = "20.0" if is_top else "12.0"

        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes: organizations
    lines.append('    <nodes>')
    for o in organizations:
        oid = o["id"]
        name = o["name"]
        c = org_color(o)
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        lines.append(f'      <edge id="e{eid}" source="{esc(person_id)}" target="org_{esc(org_id)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append(f'          <attvalue for="2" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person ↔ person (relationship)
    for r in relationships:
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


def print_summary():
    print(f"\n{'='*60}")
    print(f"  颍州区领导班子工作关系网络")
    print(f"  生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
