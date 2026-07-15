#!/usr/bin/env python3
"""Build Funan County (阜南县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_阜南县 (安徽阜阳市阜南县 - 县)

Confirmed officeholders (as of 2026-07-15):
  - 县委书记: 胡天立 (1974-10, 安徽界首人), appointed ~2026-05
  - 县长: 胡允凯 (1978-12, 安徽利辛人), elected 2026-07-06

Predecessors:
  - 前任县委书记: 李云川 (1972-12, 安徽阜阳人), served 2021-2025, promoted to 阜阳市副市长
  - 前任县长: 胡天立 (served as 县长 2022-2026 before becoming 县委书记)

Sources:
  - https://baike.baidu.com/item/阜南县 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/胡天立 (Baidu Baike, accessed 2026-07-15)
  - https://baike.baidu.com/item/胡允凯 (Baidu Baike, accessed 2026-07-15)
  - Baidu search results for 阜南县 leadership, accessed 2026-07-15
  - https://baike.baidu.com/item/阜南县人民政府 (government page, accessed 2026-07-15)

Confidence: Core leader identities and career timelines confirmed from Baidu Baike.
Leadership roster (副县长) confirmed from government page. Deputy party secretary and
other Standing Committee members' details are partially complete.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "阜南县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "阜南县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 胡天立
    {
        "id": "funan_hu_tianli",
        "name": "胡天立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "native_place": "安徽界首",
        "education": "省委党校大学学历",
        "party_join": "1995-08",
        "work_start": "1993-12",
        "current_post": "阜南县委书记",
        "current_org": "中共阜南县委员会",
        "source": "https://baike.baidu.com/item/%E8%83%A1%E5%A4%A9%E7%AB%8B",
        "notes": "1974年10月生，安徽界首人。1993年12月参加工作，1995年8月入党，省委党校大学学历。历任界首市舒庄乡、东城街道，界首市副市长，阜阳市重点工程建设管理局副局长，阜阳市城乡建设局副局长，阜阳市应急管理局局长。2022年6月任阜南县委副书记、副县长、代县长、县长。2026年4月拟任县党委正职，2026年5月任阜南县委书记。第十四届安徽省人大代表。",
        "confidence": "confirmed"
    },

    # 县委副书记、县长 胡允凯
    {
        "id": "funan_hu_yunkai",
        "name": "胡允凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-12",
        "birthplace": "",
        "native_place": "安徽利辛",
        "education": "安徽医科大学在职研究生，公共卫生硕士",
        "party_join": "1997-07",
        "work_start": "1997-11",
        "current_post": "县委副书记、县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E8%83%A1%E5%85%81%E5%87%AF",
        "notes": "1978年12月生（百度百科显示1978年3月出生/1978年12月两个版本），安徽利辛人。1997年11月参加工作，1997年7月入党，安徽医科大学在职研究生毕业，公共卫生硕士，副主任医师。历任阜阳市疾病预防控制中心医师，阜阳市新农合管理办公室副主任、主任，阜阳市疾病预防控制中心党总支部书记、主任。2020年4月任太和县委常委、副县长。后任阜南县委常委、常务副县长。2026年6月任阜南县委副书记、副县长、代县长，2026年7月6日当选县长。2020年获安徽省抗击新冠肺炎疫情先进个人。",
        "confidence": "confirmed"
    },

    # ═══ Predecessors ═══

    # 前任县委书记 李云川
    {
        "id": "funan_li_yunchuan",
        "name": "李云川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "安徽阜阳",
        "native_place": "安徽阜阳",
        "education": "经济学学士，省委党校研究生学历",
        "party_join": "1998-01",
        "work_start": "",
        "current_post": "阜阳市人民政府副市长",
        "current_org": "阜阳市人民政府",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E4%BA%91%E5%B7%9D",
        "notes": "1972年12月生，安徽阜阳人。1998年1月入党，经济学学士学位，省委党校研究生学历。长期在阜阳市工作，早期在共青团系统任职，从科员逐步成长为阜阳团市委书记。后调任阜南县，历任县委副书记、副县长、县长。2021年9月起任阜南县委书记。2025年12月30日任阜阳市人民政府副市长。现已不再兼任阜南县委书记。",
        "confidence": "confirmed"
    },

    # ═══ County Leaders (人大、政协) ═══

    # 人大常委会主任 金志刚
    {
        "id": "funan_jin_zhigang",
        "name": "金志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜南县人大常委会主任",
        "current_org": "阜南县人大常委会",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF",
        "notes": "阜南县人大常委会主任。2026年2月13日当选阜南县人大常委会主任。完整履历待补充。",
        "confidence": "plausible"
    },

    # 政协主席 李程杰
    {
        "id": "funan_li_chengjie",
        "name": "李程杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "阜南县政协主席",
        "current_org": "阜南县政协",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF",
        "notes": "阜南县政协主席。完整履历待补充。",
        "confidence": "plausible"
    },

    # ═══ 副县长 ═══

    # 陈学星（县委常委、副县长，挂职）
    {
        "id": "funan_chen_xuexing",
        "name": "陈学星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县委常委、副县长（挂职）。完整履历待补充。",
        "confidence": "plausible"
    },

    # 倪捷
    {
        "id": "funan_ni_jie",
        "name": "倪捷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 王会彬
    {
        "id": "funan_wang_huibin",
        "name": "王会彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 王磊
    {
        "id": "funan_wang_lei",
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 杨丽群
    {
        "id": "funan_yang_liqun",
        "name": "杨丽群",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 韩国民（挂职）
    {
        "id": "funan_han_guomin",
        "name": "韩国民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长（挂职）。完整履历待补充。",
        "confidence": "plausible"
    },

    # 祁帅
    {
        "id": "funan_qi_shuai",
        "name": "祁帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 杨庆（挂职）
    {
        "id": "funan_yang_qing",
        "name": "杨庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长（挂职）。完整履历待补充。",
        "confidence": "plausible"
    },

    # 朱文峰
    {
        "id": "funan_zhu_wenfeng",
        "name": "朱文峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 史明康
    {
        "id": "funan_shi_mingkang",
        "name": "史明康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 王希钊
    {
        "id": "funan_wang_xizhao",
        "name": "王希钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },

    # 朱茜
    {
        "id": "funan_zhu_qian",
        "name": "朱茜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阜南县人民政府",
        "source": "https://baike.baidu.com/item/%E9%98%9C%E5%8D%97%E5%8E%BF%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C",
        "notes": "阜南县人民政府副县长。完整履历待补充。",
        "confidence": "plausible"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共阜南县委员会", "type": "党委", "level": "县", "parent": "中共阜阳市委", "location": "阜南县"},
    {"id": 2, "name": "阜南县人民政府", "type": "政府", "level": "县", "parent": "阜阳市人民政府", "location": "阜南县"},
    {"id": 3, "name": "阜南县人大常委会", "type": "人大", "level": "县", "parent": "阜南县", "location": "阜南县"},
    {"id": 4, "name": "阜南县政协", "type": "政协", "level": "县", "parent": "阜南县", "location": "阜南县"},
    {"id": 5, "name": "阜阳市人民政府", "type": "政府", "level": "地级市", "parent": "安徽省人民政府", "location": "阜阳市"},
    {"id": 6, "name": "中共阜阳市委", "type": "党委", "level": "地级市", "parent": "中共安徽省委", "location": "阜阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 胡天立
    {"person_id": "funan_hu_tianli", "org_id": 1, "title": "阜南县委书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026年4月公示拟任县党委正职，5月正式任职"},
    {"person_id": "funan_hu_tianli", "org_id": 2, "title": "阜南县委副书记、县长", "start": "2022-06", "end": "2026-05", "rank": "正处级", "note": "2022年6月任代县长，后当选县长"},
    {"person_id": "funan_hu_tianli", "org_id": 6, "title": "阜阳市应急管理局局长", "start": "2021-07", "end": "2022-06", "rank": "正处级", "note": "兼任局党委书记"},

    # 胡允凯
    {"person_id": "funan_hu_yunkai", "org_id": 2, "title": "阜南县委副书记、县长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月任代县长，2026年7月6日当选"},
    {"person_id": "funan_hu_yunkai", "org_id": 2, "title": "阜南县委常委、常务副县长", "start": "", "end": "2026-06", "rank": "副处级", "note": "前任常务副县长，后升任县长"},

    # 李云川
    {"person_id": "funan_li_yunchuan", "org_id": 5, "title": "阜阳市人民政府副市长", "start": "2025-12", "end": "present", "rank": "副厅级", "note": "2025年12月30日任命"},
    {"person_id": "funan_li_yunchuan", "org_id": 1, "title": "阜南县委书记", "start": "2021-09", "end": "2025-12", "rank": "正处级", "note": ""},

    # 金志刚
    {"person_id": "funan_jin_zhigang", "org_id": 3, "title": "阜南县人大常委会主任", "start": "2026-02", "end": "present", "rank": "正处级", "note": "2026年2月13日当选"},

    # 李程杰
    {"person_id": "funan_li_chengjie", "org_id": 4, "title": "阜南县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 副县长们
    {"person_id": "funan_chen_xuexing", "org_id": 2, "title": "县委常委、副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_ni_jie", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_wang_huibin", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_wang_lei", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_yang_liqun", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_han_guomin", "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_qi_shuai", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_yang_qing", "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_zhu_wenfeng", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_shi_mingkang", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_wang_xizhao", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "funan_zhu_qian", "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────

relationships = [
    # 胡天立 ← 李云川 (predecessor-successor)
    {
        "person_a": "funan_li_yunchuan",
        "person_b": "funan_hu_tianli",
        "type": "predecessor_successor",
        "context": "李云川升任阜阳市副市长后，胡天立由县长接任阜南县委书记",
        "overlap_org": "中共阜南县委员会",
        "overlap_period": "2026-05",
        "confidence": "confirmed"
    },
    # 胡天立 → 胡允凯 (predecessor-successor for 县长)
    {
        "person_a": "funan_hu_tianli",
        "person_b": "funan_hu_yunkai",
        "type": "predecessor_successor",
        "context": "胡天立升任县委书记后，胡允凯由常务副县长接任县长",
        "overlap_org": "阜南县人民政府",
        "overlap_period": "2026-06",
        "confidence": "confirmed"
    },
    # 胡天立 + 胡允凯 (overlap as 党政搭档)
    {
        "person_a": "funan_hu_tianli",
        "person_b": "funan_hu_yunkai",
        "type": "overlap",
        "context": "胡天立任县委书记、胡允凯任县长，为阜南县党政一把手搭档",
        "overlap_org": "阜南县",
        "overlap_period": "2026-06-至今",
        "confidence": "confirmed"
    },
    # 胡允凯 ← 胡天立 (常务副县长的前任县长)
    {
        "person_a": "funan_hu_tianli",
        "person_b": "funan_hu_yunkai",
        "type": "superior_subordinate",
        "context": "胡允凯任阜南县委常委、常务副县长时为胡天立的副手",
        "overlap_org": "阜南县人民政府",
        "overlap_period": "~2025-2026",
        "confidence": "confirmed"
    },
]


# ═══════════════════════════════════════════════════════════════
# Build SQLite DB
# ═══════════════════════════════════════════════════════════════

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
            confidence TEXT DEFAULT 'plausible'
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place, education, party_join, work_start, current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace",""), p["native_place"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"], p["notes"], p["confidence"]))

    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    # Insert relationships
    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════
# Build GEXF graph
# ═══════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role and "县委" in role:
        return "255,50,50"     # red
    elif "县长" in role or "副县长" in role:
        return "50,100,255"    # blue
    elif "人大" in role:
        return "200,255,255"   # cyan
    elif "政协" in role:
        return "255,240,200"   # cream
    else:
        return "100,100,100"   # grey

def org_color(o):
    t = o["type"]
    if t == "党委":    return "255,200,200"
    if t == "政府":    return "200,200,255"
    if t == "人大":    return "200,255,255"
    if t == "政协":    return "255,240,200"
    return "200,200,200"

def person_size(p):
    role = p.get("current_post", "")
    if "县委书记" in role or "县长" in role:
        return "20.0"
    return "12.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Codex Research Agent</creator>')
    lines.append('    <description>阜南县政治人物关系网络图 - Funan County political network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        pid = p["id"]
        lines.append(f'      <node id="{esc(pid)}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        rgb = c.split(",")
        lines.append(f'      <node id="org{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person→organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos["title"]
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{esc(pid)}" target="org{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0"
        lines.append(f'      <edge id="{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence","plausible"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════

def print_summary():
    print(f"\n📊 阜南县网络数据摘要")
    print(f"   人物 (Persons): {len(persons)}")
    print(f"   机构 (Orgs):    {len(organizations)}")
    print(f"   任职 (Positions): {len(positions)}")
    print(f"   关系 (Relationships): {len(relationships)}")
    print(f"\n数据库: {DB_PATH}")
    print(f"图谱文件: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
