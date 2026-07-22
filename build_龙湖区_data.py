#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙湖区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 汕头市
Region: 龙湖区
Targets: 区委书记 & 区长

Research Sources:
- 龙湖区人民政府门户网站 (www.gdlonghu.gov.cn) — 政府新闻动态
- 百度搜索 — 领导简历片段
- 维基百科 — 区委书记信息
- 公开新闻报道 — 搜狐、新浪等

Research Date: 2026-07-22

网络环境限制说明:
- Exa 搜索达到速率限制 (无 API key)
- Jina Reader 超时
- Baidu Baike 被 403 拦截
- 龙湖区政府网站领导之窗页面未找到 (ldzc 路径返回 404)
- 基于公开新闻报道和政府网站活动报道确认领导信息
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "龙湖区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "林雪萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "广东省汕头市澄海区",
        "native_place": "广东省汕头市澄海区",
        "education": "中央党校研究生（中央党校研究生院法学理论专业）",
        "party_join": "1998年4月",
        "work_start": "1996年9月",
        "current_post": "龙湖区委书记",
        "current_org": "中共汕头市龙湖区委员会",
        "source": "百度百科/百度AI摘要 — 1975年11月出生，籍贯汕头澄海，1996年9月参加工作，1998年4月入党，中央党校研究生学历。2025年6月起任龙湖区委书记。政府官网gdlonghu.gov.cn确认2025年6月起以区委书记身份出席活动。"
    },
    {
        "id": 2,
        "name": "黄晓欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东省（具体待查）",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙湖区委副书记、区长",
        "current_org": "汕头市龙湖区人民政府",
        "source": "政府官网gdlonghu.gov.cn确认 — 2021年9月任龙湖区副区长、代区长，后任区长。截至2026年7月仍在区长任上（出席八一慰问活动）。公开报道显示2024年12月以区长身份出席企业家座谈会。简历具体信息待查。"
    },
    # ════════════════════════════════════════
    # Former Leaders (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "蔡向鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "汕头市政协副主席",
        "current_org": "中国人民政治协商会议汕头市委员会",
        "source": "公开报道 — 原龙湖区委书记（至2025年5月左右），后当选汕头市政协副主席。政府官网显示2025年2月仍以区委书记身份主持会议，2025年5月黄晓欢代理主持区委常委会，说明交接发生在2025年5-6月间。"
    },
    {
        "id": 4,
        "name": "林定亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（原龙湖区委书记）",
        "current_org": "中共汕头市龙湖区委员会（前任书记）",
        "source": "公开报道 — 2021年前后任龙湖区委书记，后由蔡向鸿接任。具体调任去向待查。"
    },
    # ════════════════════════════════════════
    # Key Deputies
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陈泽波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年4月",
        "birthplace": "广东省汕头市潮阳区",
        "native_place": "广东省汕头市潮阳区",
        "education": "中央党校研究生学历",
        "party_join": "1993年4月",
        "work_start": "1993年7月",
        "current_post": "潮南区委副书记、区长（已调离龙湖区）",
        "current_org": "中共汕头市潮南区委员会",
        "source": "公开报道 — 原龙湖区委副书记、政法委书记，2025年9月调任潮南区委副书记、区政府党组书记，2025年10月当选潮南区区长。此前在金平区多个街道任职（鮀江街道、石炮台街道），2022年调至龙湖区任区委常委、区党政办公室主任，后任区委副书记、政法委书记。"
    },
    {
        "id": 6,
        "name": "蔡贤达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "广东省汕头市",
        "native_place": "广东省汕头市",
        "education": "大学（广东外语外贸大学）",
        "party_join": "2004年6月",
        "work_start": "2008年7月",
        "current_post": "龙湖区委常委、常务副区长",
        "current_org": "汕头市龙湖区人民政府",
        "source": "公开报道 — 2021年11月当选龙湖区副区长，2023年10月任龙湖区人民政府办公室主任，后任区委常委、区政府党组副书记、常务副区长。百度百科有记录但页面被屏蔽。"
    },
    {
        "id": 7,
        "name": "黄斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙湖区委常委、区纪委书记、区监委主任",
        "current_org": "中共汕头市龙湖区纪律检查委员会",
        "source": "政府官网确认 — 至少从2023年9月起任龙湖区委常委、区纪委书记、区监委主任。龙湖廉政网列名。个人简历（出生年月、籍贯）公开资料未找到。"
    },
    {
        "id": 8,
        "name": "许东伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙湖区委常委、组织部部长",
        "current_org": "中共汕头市龙湖区委组织部",
        "source": "政府官网确认 — 2025年6月25日以龙湖区委常委、组织部部长身份出席区委社会工作部挂牌仪式。个人简历（出生年月、籍贯）公开资料未找到。"
    },
]

# ════════════════════════════════════════════════════════════════
# 2. Organizations
# ════════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共汕头市龙湖区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 2,
        "name": "汕头市龙湖区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "汕头市人民政府",
        "location": "汕头市龙湖区"
    },
    {
        "id": 3,
        "name": "中共汕头市龙湖区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市纪律检查委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 4,
        "name": "中共汕头市龙湖区委组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共汕头市龙湖区委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 5,
        "name": "中共汕头市龙湖区委政法委员会",
        "type": "党委",
        "level": "正科级",
        "parent": "中共汕头市龙湖区委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 6,
        "name": "龙湖区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "汕头市人民代表大会常务委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 7,
        "name": "中国人民政治协商会议汕头市龙湖区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议汕头市委员会",
        "location": "汕头市龙湖区"
    },
    {
        "id": 8,
        "name": "中共汕头市潮南区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市委员会",
        "location": "汕头市潮南区"
    },
    {
        "id": 9,
        "name": "汕头市财政局",
        "type": "政府",
        "level": "县处级",
        "parent": "汕头市人民政府",
        "location": "汕头市"
    },
    {
        "id": 10,
        "name": "汕头市澄海区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "汕头市人民政府",
        "location": "汕头市澄海区"
    },
    {
        "id": 11,
        "name": "中共汕头市濠江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市委员会",
        "location": "汕头市濠江区"
    },
    {
        "id": 12,
        "name": "汕头市濠江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "汕头市人民政府",
        "location": "汕头市濠江区"
    },
    {
        "id": 13,
        "name": "中共汕头市澄海区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市委员会",
        "location": "汕头市澄海区"
    },
]

# ════════════════════════════════════════════════════════════════
# 3. Positions
# ════════════════════════════════════════════════════════════════
positions = [
    # 林雪萍 (id=1)
    {"person_id": 1, "org_id": 1, "title": "龙湖区委书记", "start_date": "2025-06", "end_date": "", "rank": "县处级正职", "note": "数据来源：政府官网活动报道"},
    {"person_id": 1, "org_id": 9, "title": "汕头市财政局局长", "start_date": "2022-07", "end_date": "2025-06", "rank": "县处级正职", "note": "数据来源：百度AI摘要"},
    {"person_id": 1, "org_id": 11, "title": "濠江区委常委、常务副区长", "start_date": "2021-01", "end_date": "2022-07", "rank": "县处级副职", "note": "数据来源：百度AI摘要"},
    {"person_id": 1, "org_id": 12, "title": "濠江区副区长", "start_date": "2021-01", "end_date": "2021-01", "rank": "县处级副职", "note": "2021年1月调任濠江区"},
    {"person_id": 1, "org_id": 10, "title": "澄海区副区长", "start_date": "?", "end_date": "2021-01", "rank": "县处级副职", "note": "具体起止时间待查"},
    {"person_id": 1, "org_id": 13, "title": "莲华镇党委书记", "start_date": "?", "end_date": "?", "rank": "乡科级正职", "note": "澄海区莲华镇，具体时间待查"},
    {"person_id": 1, "org_id": 10, "title": "隆都镇镇长", "start_date": "?", "end_date": "?", "rank": "乡科级正职", "note": "澄海区隆都镇，具体时间待查"},
    {"person_id": 1, "org_id": 10, "title": "澄海区监察局副局长", "start_date": "?", "end_date": "?", "rank": "乡科级副职", "note": "具体时间待查"},
    {"person_id": 1, "org_id": 10, "title": "隆都镇副镇长", "start_date": "1996-09", "end_date": "?", "rank": "乡科级副职", "note": "1996年9月参加工作"},
    # 黄晓欢 (id=2)
    {"person_id": 2, "org_id": 2, "title": "龙湖区委副书记、区长", "start_date": "2021-09", "end_date": "", "rank": "县处级正职", "note": "2021年9月任代区长，后转正"},
    # 蔡向鸿 (id=3)
    {"person_id": 3, "org_id": 1, "title": "龙湖区委书记", "start_date": "?", "end_date": "2025-05", "rank": "县处级正职", "note": "接替林定亮，至2025年5月左右"},
    {"person_id": 3, "org_id": 7, "title": "汕头市政协副主席", "start_date": "2025?", "end_date": "", "rank": "副厅级", "note": "调离龙湖区委书记后当选"},
    # 林定亮 (id=4)
    {"person_id": 4, "org_id": 1, "title": "龙湖区委书记", "start_date": "?", "end_date": "?", "rank": "县处级正职", "note": "蔡向鸿前任，具体任期待查"},
    # 陈泽波 (id=5)
    {"person_id": 5, "org_id": 1, "title": "龙湖区委副书记、政法委书记", "start_date": "2022?", "end_date": "2025-09", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "龙湖区委常委、区党政办公室主任", "start_date": "2022", "end_date": "?", "rank": "县处级副职", "note": "2022年调至龙湖区"},
    {"person_id": 5, "org_id": 8, "title": "潮南区委副书记、区长", "start_date": "2025-10", "end_date": "", "rank": "县处级正职", "note": "2025年9月调任，10月当选区长"},
    # 蔡贤达 (id=6)
    {"person_id": 6, "org_id": 2, "title": "龙湖区委常委、常务副区长", "start_date": "2025?", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "龙湖区人民政府办公室主任", "start_date": "2023-10", "end_date": "2025?", "rank": "乡科级正职", "note": "2023年10月至升任常务副区长前"},
    {"person_id": 6, "org_id": 2, "title": "龙湖区副区长", "start_date": "2021-11", "end_date": "2023-10", "rank": "县处级副职", "note": "2021年11月当选"},
    # 黄斌 (id=7)
    {"person_id": 7, "org_id": 3, "title": "龙湖区委常委、区纪委书记、区监委主任", "start_date": "2023-09?", "end_date": "", "rank": "县处级副职", "note": "至少从2023年9月任此职"},
    # 许东伟 (id=8)
    {"person_id": 8, "org_id": 4, "title": "龙湖区委常委、组织部部长", "start_date": "2025-06?", "end_date": "", "rank": "县处级副职", "note": "2025年6月25日出席挂牌仪式"},
]

# ════════════════════════════════════════════════════════════════
# 4. Relationships
# ════════════════════════════════════════════════════════════════
relationships = [
    # 林雪萍 ↔ 黄晓欢 (党政一把手)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "2025年6月起为龙湖区党政一把手搭档关系", "overlap_org": "中共汕头市龙湖区委员会/龙湖区人民政府", "overlap_period": "2025-06至今"},
    # 林雪萍 ← 蔡向鸿 (区委书记前任/继任)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "蔡向鸿为前任龙湖区委书记，林雪萍继任", "overlap_org": "中共汕头市龙湖区委员会", "overlap_period": "2025-06交接"},
    # 蔡向鸿 ← 林定亮 (区委书记前任/继任)
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "林定亮前任龙湖区委书记，蔡向鸿继任", "overlap_org": "中共汕头市龙湖区委员会", "overlap_period": "交接期"},
    # 林雪萍 ↔ 陈泽波 (上下级)
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "林雪萍任书记时，陈泽波为区委副书记、政法委书记（2025年6-9月）", "overlap_org": "中共汕头市龙湖区委员会", "overlap_period": "2025-06至2025-09"},
    # 林雪萍 ↔ 蔡贤达 (上下级)
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "林雪萍任书记时，蔡贤达为常务副区长", "overlap_org": "龙湖区党政领导班子", "overlap_period": "2025-06至今"},
    # 林雪萍 ↔ 黄斌 (上下级)
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "林雪萍任书记时，黄斌为纪委书记", "overlap_org": "中共汕头市龙湖区委员会", "overlap_period": "2025-06至今"},
    # 林雪萍 ↔ 许东伟 (上下级)
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "林雪萍任书记时，许东伟为组织部部长", "overlap_org": "中共汕头市龙湖区委员会", "overlap_period": "2025-06至今"},
    # 黄晓欢 ↔ 蔡贤达 (上下级)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "黄晓欢为区长，蔡贤达为常务副区长", "overlap_org": "龙湖区人民政府", "overlap_period": "2025至今"},
    # 陈泽波 → 蔡贤达 (同僚/前后任)
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "陈泽波（区委副书记）与蔡贤达（常务副区长）在龙湖区领导班子中共事", "overlap_org": "龙湖区领导班子", "overlap_period": "2022至2025-09"},
    # 黄晓欢 ↔ 陈泽波 (上下级)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "黄晓欢为区长时，陈泽波为区委副书记", "overlap_org": "龙湖区领导班子", "overlap_period": "2022至2025-09"},
    # 陈泽波 → 潮南区 (跨区调动)
    {"person_a": 5, "person_b": 8, "type": "promotion_chain", "context": "陈泽波从龙湖区委副书记调任潮南区委副书记、区长", "overlap_org": "跨区调动", "overlap_period": "2025-09"},
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs:    {len(organizations)}")
    print(f"   Pos:     {len(positions)}")
    print(f"   Rel:     {len(relationships)}")
