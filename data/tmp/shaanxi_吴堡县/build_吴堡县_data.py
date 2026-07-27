#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Wubu County (吴堡县) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/shaanxi_吴堡县")
DB_PATH = os.path.join(STAGING, "吴堡县_network.db")
GEXF_PATH = os.path.join(STAGING, "吴堡县_network.gexf")

SLUG = "吴堡县"
TODAY = datetime.now().strftime("%Y-%m-%d")
AS_OF = "2026-07-25"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary ──
    {"id": 1, "name": "陈耀忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共吴堡县委书记", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202607/t20260720_2115612.html",
     "notes": "曾任吴堡县委副书记、县长；2025年8月前已任县委书记、县长（一肩挑）；2026年5月刘荣当选县长后专职县委书记"},

    # ── Current County Mayor (Deputy Party Secretary) ──
    {"id": 2, "name": "刘荣", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县委副书记、县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/xz/lr/",
     "notes": "2026年5月20日当选吴堡县人民政府县长"},

    # ── Party Committee Deputy Secretary ──
    {"id": 3, "name": "魏国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委副书记", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202603/t20260313_2080725.html",
     "notes": "分管社会工作和统战工作"},

    # ── Standing Committee Members ──
    {"id": 4, "name": "朱海涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202603/t20260313_2080725.html",
     "notes": "分管组织工作"},

    {"id": 5, "name": "王政瑞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委、纪委书记、监委主任", "current_org": "中共吴堡县纪律检查委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202607/t20260720_2115612.html",
     "notes": "2026年5月当选县监委主任"},

    {"id": 6, "name": "邢波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202603/t20260313_2080725.html",
     "notes": "分管宣传思想工作"},

    {"id": 7, "name": "张宝山", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县委常委、常务副县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/hxj/",
     "notes": "负责县政府常务工作"},

    {"id": 8, "name": "张剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县委常委、副县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/zj/",
     "notes": "负责园区建设、交通运输、城乡建设"},

    {"id": 9, "name": "张敏", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县委常委、副县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/zm/",
     "notes": "负责招商引资和苏陕协作"},

    # ── Other County Standing Committee Members ──
    {"id": 10, "name": "魏向国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202508/t20250826_2031069.html",
     "notes": ""},

    {"id": 11, "name": "苗润祥", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202508/t20250826_2031069.html",
     "notes": ""},

    {"id": 12, "name": "刘小宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县委常委", "current_org": "中共吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202508/t20250826_2031069.html",
     "notes": ""},

    # ── Deputy County Mayors (non-standing committee) ──
    {"id": 13, "name": "张子君", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县副县长、公安局党委书记局长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/zzj/",
     "notes": "负责公安、司法、信访维稳"},

    {"id": 14, "name": "冯志伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1990-03", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县副县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/fzw/",
     "notes": "负责教育体育、医疗保障、卫生健康、生态环保"},

    {"id": 15, "name": "万治国", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县副县长（挂职）", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/wzg/",
     "notes": "负责国能定点帮扶工作（国家能源集团挂职）"},

    {"id": 16, "name": "王娜", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-05", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "吴堡县副县长", "current_org": "吴堡县人民政府",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/fxz/wn/",
     "notes": "负责乡村振兴、农业农村、水利、林业"},

    # ── People's Congress and Political Consultative ──
    {"id": 17, "name": "李向春", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县人大常委会主任", "current_org": "吴堡县人民代表大会常务委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202508/t20250826_2031069.html",
     "notes": ""},

    {"id": 18, "name": "李建明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县政协主席", "current_org": "中国人民政治协商会议吴堡县委员会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202603/t20260313_2080725.html",
     "notes": ""},

    # ── Other key figures ──
    {"id": 19, "name": "薛改香", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县人大常委会副主任", "current_org": "吴堡县人民代表大会常务委员会",
     "source": "https://www.wubu.gov.cn/zwgk/fdzdgknr/ldzc/xz/lr/zyhd/202605/t20260521_2097547.html",
     "notes": ""},

    {"id": 20, "name": "张永红", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "吴堡县产业园区党工委书记、农业农村局局长", "current_org": "吴堡县产业园区管委会",
     "source": "https://www.wubu.gov.cn/xwzx/zwyw/202607/t20260723_2116402.html",
     "notes": ""},
]

organizations = [
    {"id": 1, "name": "中共吴堡县委员会", "type": "党委", "level": "县级", "parent": "中共榆林市委", "location": "吴堡县"},
    {"id": 2, "name": "吴堡县人民政府", "type": "政府", "level": "县级", "parent": "榆林市人民政府", "location": "吴堡县"},
    {"id": 3, "name": "中共吴堡县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共吴堡县委员会", "location": "吴堡县"},
    {"id": 4, "name": "吴堡县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "吴堡县"},
    {"id": 5, "name": "中国人民政治协商会议吴堡县委员会", "type": "政协", "level": "县级", "parent": "", "location": "吴堡县"},
    {"id": 6, "name": "吴堡县公安局", "type": "政府", "level": "县级", "parent": "吴堡县人民政府", "location": "吴堡县"},
    {"id": 7, "name": "吴堡县产业园区管委会", "type": "政府", "level": "县级", "parent": "吴堡县人民政府", "location": "吴堡县"},
    {"id": 8, "name": "国家能源集团", "type": "事业单位", "level": "央企", "parent": "", "location": "北京"},
]

positions = [
    # Party Secretary
    {"person_id": 1, "org_id": 1, "title": "中共吴堡县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},

    # County Mayor
    {"person_id": 2, "org_id": 2, "title": "吴堡县人民政府县长", "start_date": "2026-05", "end_date": "present", "rank": "正处级", "note": "2026年5月20日当选"},
    {"person_id": 2, "org_id": 1, "title": "吴堡县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "吴堡县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管社会工作和统战工作"},

    # Standing Committee
    {"person_id": 4, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管组织工作"},
    {"person_id": 5, "org_id": 3, "title": "吴堡县纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年5月当选"},
    {"person_id": 5, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管宣传思想工作"},
    {"person_id": 7, "org_id": 2, "title": "吴堡县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 7, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "吴堡县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责园区建设、交通、城建"},
    {"person_id": 8, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "吴堡县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责招商引资和苏陕协作"},
    {"person_id": 9, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "吴堡县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # Deputy Mayors
    {"person_id": 13, "org_id": 6, "title": "吴堡县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "吴堡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、信访维稳"},
    {"person_id": 14, "org_id": 2, "title": "吴堡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责教育体育、卫健、生态环保"},
    {"person_id": 15, "org_id": 2, "title": "吴堡县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "国能定点帮扶"},
    {"person_id": 15, "org_id": 8, "title": "国家能源集团干部", "start_date": "", "end_date": "present", "rank": "", "note": "挂职来源"},
    {"person_id": 16, "org_id": 2, "title": "吴堡县副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责乡村振兴、农业农村、水利、林业"},

    # NPC / CPPCC
    {"person_id": 17, "org_id": 4, "title": "吴堡县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 5, "title": "吴堡县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "吴堡县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # Other
    {"person_id": 20, "org_id": 7, "title": "吴堡县产业园区党工委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "吴堡县农业农村局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任"},
]

relationships = [
    # Core relationship: 陈耀忠 and 刘荣 (direct superior-subordinate, 书记+县长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭班子", "overlap_org": "中共吴堡县委员会/吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},

    # 陈耀忠 and 魏国 (书记/副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 陈耀忠 and standing committee members (all在同一常委会)
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "县委常委会班子", "overlap_org": "中共吴堡县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 刘荣 and 张宝山 (县长/常务副县长)
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与常务副县长搭班子", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},

    # 刘荣 and other deputy mayors
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与挂职副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "吴堡县人民政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},

    # 陈耀忠 and 李向春 (县委/人大)
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "县委书记与人大常委会主任", "overlap_org": "吴堡县",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 陈耀忠 and 李建明 (县委/政协)
    {"person_a": 1, "person_b": 18, "type": "overlap",
     "context": "县委书记与政协主席", "overlap_org": "吴堡县",
     "overlap_period": "至今", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════
# DATABASE BUILD
# ═══════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
            source TEXT,
            notes TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    conn.commit()


def build():
    """Run database + GEXF build."""
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 吴堡县人民政府网站 (wubu.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source","notes"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post and "前任" not in post:
            return ("255,50,50", 20.0)  # Red, top leader
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)  # Blue
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and "常务" in post:
            return ("50,100,255", 15.0)
        elif "县委常委" in post:
            return ("100,150,255", 12.0)
        elif "副县长" in post:
            return ("100,150,255", 12.0)
        elif "纪委书记" in post or "监委" in post:
            return ("255,165,0", 12.0)  # Orange
        elif "人大" in post:
            return ("200,255,255", 12.0)  # Cyan
        elif "政协" in post:
            return ("255,240,200", 12.0)  # Cream
        elif "挂职" in post:
            return ("150,150,150", 10.0)  # Grey
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
        "乡镇": ("255,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络 - {TODAY}</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    # Person nodes
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    build()
