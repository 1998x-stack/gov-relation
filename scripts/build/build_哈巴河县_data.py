#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 哈巴河县 (Habahe County) leadership network.

哈巴河县 — 新疆维吾尔自治区阿勒泰地区下辖县。
位于阿尔泰山南麓，新疆维吾尔自治区最西北边缘，西、北分别与哈萨克斯坦、俄罗斯两国接壤
边境线长282.6千米。面积约8180平方公里，人口约8万人（2024年）。
邮政编码：836700，车牌代码：新H，电话区号：0906。

Research conducted: 2026-07-28
Data sources: 哈巴河县人民政府网站 (www.hbh.gov.cn) — official government leadership pages and news articles.
Data currency: 2026-07 (Current as of July 2026)
"""

import json
import os
import sqlite3  # noqa: used by gov_relation.schema via runner
import sys
from datetime import datetime

# Ensure gov_relation package is importable
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────
TMP = os.path.join(BASE, "data/tmp/xinjiang_哈巴河县")
DB_PATH = os.path.join(TMP, "哈巴河县_network.db")
GEXF_PATH = os.path.join(TMP, "哈巴河县_network.gexf")

# ── DATA ──────────────────────────────────────────────────────────────
# Person ID convention used in this build: habahe_<pinyin>
# Source: www.hbh.gov.cn leadership page and news, accessed 2026-07-28.

persons = [
    # ═══════════════ Core Leaders ═══════════════════════════════════════
    {
        "id": 1,
        "name": "丁志春",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县委书记",
        "current_org": "中共哈巴河县委员会",
        "source": "confirmed — cited as 县委书记 in multiple official news articles on www.hbh.gov.cn (2026-07). Confirmed as 县人武部党委第一书记 (2026-07-22). Full biography unavailable on government website."
    },
    {
        "id": 2,
        "name": "哈力木别克·贺扎托拉",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1979年9月",
        "birthplace": "新疆托里县",
        "education": "本科",
        "party_join": "2006年5月",
        "work_start": "1999年4月",
        "current_post": "哈巴河县委副书记、政府县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn/zwgk/006001/) as of 2026-07-14. Full career timeline unavailable."
    },
    # ═══════════════ Government Leadership ══════════════════════════════
    {
        "id": 3,
        "name": "周振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年8月",
        "birthplace": "黑龙江齐齐哈尔市",
        "education": "本科",
        "party_join": "2012年4月",
        "work_start": "2010年7月",
        "current_post": "哈巴河县委常委、副县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn, 2026-07-24). Noted as 对口援疆干部 (counterpart aid Xinjiang cadre from Heilongjiang)."
    },
    {
        "id": 4,
        "name": "张玉磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "山东梁山县",
        "education": "研究生",
        "party_join": "2012年6月",
        "work_start": "2007年7月",
        "current_post": "哈巴河县委常委、常务副县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn/ldzc, updated 2026-05-12)"
    },
    {
        "id": 5,
        "name": "张利国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "甘肃张掖市",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "2007年10月",
        "current_post": "哈巴河县副县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn, updated 2026-05-12)"
    },
    {
        "id": 6,
        "name": "迪娜·迪汗别克",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "1979年2月",
        "birthplace": "新疆福海县",
        "education": "本科",
        "party_join": "unverified (无党派人士)",
        "work_start": "2001年6月",
        "current_post": "哈巴河县副县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn, updated 2026-05-12)"
    },
    {
        "id": 7,
        "name": "郭勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年4月",
        "birthplace": "新疆哈密市",
        "education": "本科",
        "party_join": "2007年10月",
        "work_start": "2008年10月",
        "current_post": "哈巴河县副县长",
        "current_org": "哈巴河县人民政府",
        "source": "confirmed — 哈巴河县政府领导之窗 (www.hbh.gov.cn, updated 2026-05-12)"
    },
    # ═══════════════ 人大 Leadership ════════════════════════════════════
    {
        "id": 8,
        "name": "汤西芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "江苏如皋市",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县人大常委会党组书记、副主任人选",
        "current_org": "哈巴河县人大常委会",
        "source": "confirmed — www.hbh.gov.cn (2025-10-24)"
    },
    {
        "id": 9,
        "name": "努尔波拉提·叶斯木拉提",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1972年7月",
        "birthplace": "新疆吉木乃县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县人大常委会党组副书记、主任人选",
        "current_org": "哈巴河县人大常委会",
        "source": "confirmed — www.hbh.gov.cn (updated 2026-05-12)"
    },
    {
        "id": 10,
        "name": "马德高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "山西文水县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县人大常委会党组成员、副主任",
        "current_org": "哈巴河县人大常委会",
        "source": "confirmed — www.hbh.gov.cn (2021-02-03)"
    },
    {
        "id": 11,
        "name": "韩晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "山东寿光市",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县人大常委会党组成员、副主任人选",
        "current_org": "哈巴河县人大常委会",
        "source": "confirmed — www.hbh.gov.cn (2021-02-03)"
    },
    # ═══════════════ 政协 Leadership ════════════════════════════════════
    {
        "id": 12,
        "name": "陈晶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "新疆哈巴河县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县政协党组书记",
        "current_org": "哈巴河县政协",
        "source": "confirmed — www.hbh.gov.cn (2025-10-24)"
    },
    {
        "id": 13,
        "name": "阿提拉·热合买提",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "1975年7月",
        "birthplace": "新疆哈巴河县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县政协党组成员、副主席",
        "current_org": "哈巴河县政协",
        "source": "confirmed — www.hbh.gov.cn (2021-11-11)"
    },
    {
        "id": 14,
        "name": "吾木尔别克·托乎达尔汗",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1972年10月",
        "birthplace": "新疆哈巴河县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县政协党组成员、副主席",
        "current_org": "哈巴河县政协",
        "source": "confirmed — www.hbh.gov.cn (2021-11-11)"
    },
    {
        "id": 15,
        "name": "张锋胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "江苏省",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县政协党组成员、副主席",
        "current_org": "哈巴河县政协",
        "source": "confirmed — www.hbh.gov.cn (2021-02-03)"
    },
    # ═══════════════ Other县级领导 (noted in news articles) ═════════════
    {
        "id": 16,
        "name": "宋宏波",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县县级领导",
        "current_org": "哈巴河县",
        "source": "listed as attendee at 县人武部党委第一书记任职大会 (www.hbh.gov.cn, 2026-07-24). Exact position unclear."
    },
    {
        "id": 17,
        "name": "苗民田",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县县级领导",
        "current_org": "哈巴河县",
        "source": "listed as县级领导 attendee at 县人武部会议 (www.hbh.gov.cn, 2026-07-24). Exact position unclear."
    },
    {
        "id": 18,
        "name": "杜恒",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县县级领导",
        "current_org": "哈巴河县",
        "source": "listed as县级领导 attendee at 县人武部会议 (www.hbh.gov.cn, 2026-07-24). Exact position unclear."
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共哈巴河县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共阿勒泰地区委员会",
        "location": "新疆阿勒泰地区哈巴河县"
    },
    {
        "id": 2,
        "name": "哈巴河县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "阿勒泰地区行政公署",
        "location": "新疆阿勒泰地区哈巴河县"
    },
    {
        "id": 3,
        "name": "哈巴河县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": None,
        "location": "新疆阿勒泰地区哈巴河县"
    },
    {
        "id": 4,
        "name": "哈巴河县政协",
        "type": "政协",
        "level": "县",
        "parent": None,
        "location": "新疆阿勒泰地区哈巴河县"
    },
]

positions = [
    # 丁志春 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "哈巴河县委书记",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Also serves as 县人武部党委第一书记 (confirmed 2026-07-22). Start date unverified."
    },
    # 哈力木别克·贺扎托拉 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "哈巴河县委副书记、政府县长",
        "start": "~2019 (earliest mention as leader on hbh.gov.cn)",
        "end": None,
        "rank": "正县",
        "note": "Kazakh ethnicity, bachelor's degree"
    },
    # 周振宇 — 县委常委、副县长
    {
        "person_id": 3,
        "org_id": 2,
        "title": "哈巴河县委常委、副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "黑龙江援疆干部 — originally from Qiqihar, Heilongjiang"
    },
    # 张玉磊 — 常务副县长
    {
        "person_id": 4,
        "org_id": 2,
        "title": "哈巴河县委常委、常务副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Master's degree (研究生)"
    },
    # 张利国 — 副县长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "哈巴河县副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Responsible for housing, transport, industry, etc."
    },
    # 迪娜·迪汗别克 — 副县长
    {
        "person_id": 6,
        "org_id": 2,
        "title": "哈巴河县副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Non-party member (无党派人士), female"
    },
    # 郭勇 — 副县长
    {
        "person_id": 7,
        "org_id": 2,
        "title": "哈巴河县副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "From Hami, Xinjiang"
    },
    # 人大
    {
        "person_id": 8,
        "org_id": 3,
        "title": "县人大常委会党组书记、副主任人选",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Female, from Jiangsu"
    },
    {
        "person_id": 9,
        "org_id": 3,
        "title": "县人大常委会党组副书记、主任人选",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Kazak ethnicity, from Jeminay county"
    },
    {
        "person_id": 10,
        "org_id": 3,
        "title": "县人大常委会党组成员、副主任",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "From Shanxi"
    },
    {
        "person_id": 11,
        "org_id": 3,
        "title": "县人大常委会党组成员、副主任人选",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "From Shandong"
    },
    # 政协
    {
        "person_id": 12,
        "org_id": 4,
        "title": "县政协党组书记",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Native of 哈巴河县"
    },
    {
        "person_id": 13,
        "org_id": 4,
        "title": "县政协党组成员、副主席",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Female, Kazak, native of 哈巴河县"
    },
    {
        "person_id": 14,
        "org_id": 4,
        "title": "县政协党组成员、副主席",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Kazak, native of 哈巴河县"
    },
    {
        "person_id": 15,
        "org_id": 4,
        "title": "县政协党组成员、副主席",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "From Jiangsu"
    },
]

relationships = [
    # 书记 — 县长 (core leadership pairing)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "工作关系",
        "context": "县委县政府主要领导搭档：县委书记与政府县长",
        "overlap_org": "哈巴河县",
        "overlap_period": "~2024-present (estimated, start date unverified)"
    },
    # 县长 — 常务副县长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "工作关系",
        "context": "县政府主要领导 — 常务副县长（协助县长分管审计）",
        "overlap_org": "哈巴河县人民政府",
        "overlap_period": "unverified"
    },
    # 县委书记 — 县委常委/副县长（援疆）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "工作关系",
        "context": "县委常委会主要领导与成员 — 援疆干部",
        "overlap_org": "中共哈巴河县委员会",
        "overlap_period": "unverified"
    },
    # 常务副县长 — 副县长（应急管理）
    {
        "person_a": 4,
        "person_b": 5,
        "type": "工作关系",
        "context": "常务副县长与副县长 — 协助分管应急管理工作",
        "overlap_org": "哈巴河县人民政府",
        "overlap_period": "unverified"
    },
    # 迪娜·迪汗别克 — possible relation to 福海县 (her hometown)
    {
        "person_a": 6,
        "person_b": 2,
        "type": "工作关系",
        "context": "县政府班子成员 — 副县长与县长",
        "overlap_org": "哈巴河县人民政府",
        "overlap_period": "unverified"
    },
]

# ── BUILD ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building 哈巴河县 network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug="哈巴河县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n✅ Build complete")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF:     {GEXF_PATH}")
    print(f"\n⚠  GAPS:")
    print(f"   - 县委书记丁志春的出生年份、民族、籍贯、教育背景和完整职业生涯未知")
    print(f"   - 丁志春的前任县委书记未知")
    print(f"   - 哈力木别克·贺扎托拉的前任未知")
    print(f"   - 县委常委会其他成员未知（组织部长、纪委书记、宣传部长等）")
    print(f"   - 宋宏波、苗民田、杜恒的准确职务未知")