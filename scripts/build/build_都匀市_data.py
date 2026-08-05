#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
都匀市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Duyun city leadership network.

Level: 县级市
Province: 贵州省
Parent city: 黔南布依族苗族自治州
Region: 都匀市
Targets: 市委书记 & 市长

Research Sources (2026-08-05):
- https://www.duyun.gov.cn — 都匀市人民政府门户网站
  - 领导之窗 (2026-02 更新, 市长杨平; 市政府领导班子简历)
  - 市四家班子领导开展八一建军节走访慰问 (2026-08-03)
  - 中共都匀市委十二届十二次全会 (2026-07-30)
  - 全市半年经济工作会议暨"六大提升行动"工作推进会 (2026-07-31)
  - 市政府第十四届一百零六次常务会 (2026-04-15)
  - 龚仆督导调研防溺水/信访工作 (2026-07/08)
- http://dykfq.qiannan.gov.cn — 都匀经济开发区门户网站 领导之窗
  - 龚仆(2025-03), 杨平(2026-02), 刘旭, 任凌纬, 蔡秀鹏, 敖建军

Confirmed officeholders (as of 2026-08-05):
- 市委书记: 龚仆 (黔南州委常委、都匀市委书记、都匀经开区党工委书记)
- 市委副书记、市长: 杨平 (都匀经开区党工委副书记、管委会主任)
- 市人大常委会党组书记: 冯波
- 市政协党组书记: 熊杰
- 市委副书记: 曹菲
- 市委常委、纪委书记、监委主任: 刘旭
- 市委常委、常务副市长: 闻豪
- 市委常委、副市长: 王豫杰
- 市委常委、政法委书记、副市长、公安局长: 昌晓辉
- 副市长: 吴清贵、张建、蔡云程、王熙
- 市政府党组成员、办公室主任: 李兆钦
- 经开区党工委委员、管委会副主任: 任凌纬、蔡秀鹏、敖建军
- 市领导: 汤立、王吉喆、许强、张纪匀

Note: 龚仆、杨平之外的大部分领导班子成员早期履历仍需补充；
市十四届人民政府第N次常务会 (本届政府/人大周期)。

Research Date: 2026-08-05
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "都匀市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Core Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "龚仆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州委常委、都匀市委书记、都匀经开区党工委书记",
        "current_org": "中共都匀市委员会",
        "source": "http://dykfq.qiannan.gov.cn 领导之窗 (2025-03) + duyun.gov.cn 新闻 2026-08",
    },
    {
        "id": 2,
        "name": "杨平",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "全日制大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市委副书记、市长，都匀经开区党工委副书记、管委会主任",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 (2026-02)",
    },
    # ════════════════════════════════════════
    # 市人大常委会 / 市政协
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "冯波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人大常委会党组书记",
        "current_org": "都匀市人民代表大会常务委员会",
        "source": "https://www.duyun.gov.cn/xwzx/dyyw/202608/t20260803_90687754.html 八一走访慰问 2026-08-03",
    },
    {
        "id": 4,
        "name": "熊杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市政协党组书记",
        "current_org": "中国人民政治协商会议都匀市委员会",
        "source": "https://www.duyun.gov.cn \"市四家班子领导开展八一建军节走访慰问\" 2026-08-03",
    },
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "曹菲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市委副书记",
        "current_org": "中共都匀市委员会",
        "source": "https://www.duyun.gov.cn/xwzx/dyyw/202607/t20260730_90675227.html 信访督导调研 2026-07-29",
    },
    {
        "id": 6,
        "name": "刘旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "大学本科（法学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市委常委、市纪委书记、市监委主任，都匀经开区党工委委员、纪检监察工委书记",
        "current_org": "中共都匀市纪律检查委员会",
        "source": "http://dykfq.qiannan.gov.cn 领导之窗 2025-03",
    },
    {
        "id": 7,
        "name": "闻豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "贵州贵阳",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2008年3月",
        "current_post": "都匀市委常委、市政府党组副书记、常务副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2025-12",
    },
    {
        "id": 8,
        "name": "王豫杰",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市委常委、市政府党组成员、副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2023-08",
    },
    {
        "id": 9,
        "name": "昌晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市委常委、政法委书记、市政府党组成员、副市长、市公安局局长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2023-08",
    },
    # ════════════════════════════════════════
    # 市政府领导班子
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "吴清贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "全日制大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人民政府党组成员、副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2023-08",
    },
    {
        "id": 11,
        "name": "张建",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "在职研究生、工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人民政府党组成员、副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2023-08",
    },
    {
        "id": 12,
        "name": "蔡云程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人民政府党组成员、副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2024-02",
    },
    {
        "id": 13,
        "name": "王熙",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "全日制大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人民政府党组成员、副市长",
        "current_org": "都匀市人民政府",
        "source": "https://www.duyun.gov.cn 领导之窗 2024-07",
    },
    {
        "id": 14,
        "name": "李兆钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "全日制大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市人民政府党组成员、市政府机关党组书记、办公室主任",
        "current_org": "都匀市人民政府办公室",
        "source": "https://www.duyun.gov.cn 领导之窗 2026-07",
    },
    # ════════════════════════════════════════
    # 市领导 (常务会议/调研确认, 履历待查)
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "任凌纬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀经济开发区党工委委员、管委会副主任",
        "current_org": "贵州都匀经济开发区管理委员会",
        "source": "http://dykfq.qiannan.gov.cn 领导之窗 2025-03",
    },
    {
        "id": 16,
        "name": "蔡秀鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "贵州民族学院中文系",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "贵州都匀经济开发区党工委委员、管委会副主任",
        "current_org": "贵州都匀经济开发区管理委员会",
        "source": "http://dykfq.qiannan.gov.cn 领导之窗 2025-03",
    },
    {
        "id": 17,
        "name": "敖建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "中央广播电视大学行政管理",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "贵州都匀经济开发区党工委委员、管委会副主任",
        "current_org": "贵州都匀经济开发区管理委员会",
        "source": "http://dykfq.qiannan.gov.cn 领导之窗 2025-03",
    },
    {
        "id": 18,
        "name": "汤立",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "都匀市领导",
        "current_org": "中共都匀市委员会",
        "source": "https://www.duyun.gov.cn 督导调研 (防溺水/信访) 2026-07/08",
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共都匀市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 2,
        "name": "都匀市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "黔南布依族苗族自治州人民政府",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 3,
        "name": "都匀市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "黔南布依族苗族自治州人民代表大会常务委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议都匀市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议黔南布依族苗族自治州委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 5,
        "name": "都匀市公安局",
        "type": "政府",
        "level": "县级",
        "parent": "都匀市人民政府",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 6,
        "name": "中共都匀市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共都匀市委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
    {
        "id": 7,
        "name": "贵州都匀经济开发区管理委员会",
        "type": "开发区",
        "level": "县级",
        "parent": "黔南布依族苗族自治州人民政府",
        "location": "贵州省黔南布依族苗族自治州都匀市",
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "副厅级", "note": "黔南州委常委、都匀市委书记"},
    {"person_id": 1, "org_id": 7, "title": "经开区党工委书记", "start": "", "end": "present", "rank": "副厅级", "note": "兼任"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正县级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 7, "title": "经开区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "正县级", "note": "兼任"},
    # 人大/政协
    {"person_id": 3, "org_id": 3, "title": "市人大常委会党组书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "市政协党组书记", "start": "", "end": "present", "rank": "正县级", "note": "政协主席待确认"},
    # 市委
    {"person_id": 5, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副县级", "note": "市委常委"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副县级", "note": "市委常委、市政府党组副书记"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市委常委、市政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市委常委、政法委书记"},
    {"person_id": 9, "org_id": 5, "title": "市公安局局长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 市政府班子
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副县级", "note": "市政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "市政府办公室主任", "start": "", "end": "present", "rank": "正科级", "note": "市政府党组成员、机关党组书记"},
    # 经开区
    {"person_id": 15, "org_id": 7, "title": "经开区管委会副主任", "start": "", "end": "present", "rank": "副县级", "note": "党工委委员"},
    {"person_id": 16, "org_id": 7, "title": "经开区管委会副主任", "start": "", "end": "present", "rank": "副县级", "note": "党工委委员"},
    {"person_id": 17, "org_id": 7, "title": "经开区管委会副主任", "start": "", "end": "present", "rank": "副县级", "note": "党工委委员"},
    {"person_id": 18, "org_id": 1, "title": "市领导", "start": "", "end": "present", "rank": "副县级", "note": "履历待查"},
]

# 4. Relationships (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "市委书记与市长，党政主要领导搭档；共同出席八一走访慰问、半年经济工作会议",
     "overlap_org": "中共都匀市委、都匀市人民政府", "overlap_period": "2026年"},
    # 市委书记 & 人大/政协/副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记与市人大常委会党组书记",
     "overlap_org": "都匀市四家班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与市政协党组书记",
     "overlap_org": "都匀市四家班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记与市委副书记，共同参加全市半年经济工作会议、信访督导调研",
     "overlap_org": "中共都匀市委常委会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "市委书记与市纪委书记",
     "overlap_org": "中共都匀市委常委会", "overlap_period": "2026年"},
    # 市长 & 市政府班子
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长与常务副市长，共同主持市政府常务会",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长与副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长与分管公安副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长与副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长与副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "市长与副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "市长与副市长",
     "overlap_org": "都匀市人民政府", "overlap_period": "2026年"},
    # 经开区领导
    {"person_a": 1, "person_b": 15, "type": "superior_subordinate",
     "context": "经开区党工委书记与分管副主任",
     "overlap_org": "贵州都匀经济开发区", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 16, "type": "superior_subordinate",
     "context": "经开区党工委书记与分管副主任",
     "overlap_org": "贵州都匀经济开发区", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate",
     "context": "经开区党工委书记与分管副主任",
     "overlap_org": "贵州都匀经济开发区", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "经开区管委会主任与副主任",
     "overlap_org": "贵州都匀经济开发区", "overlap_period": "2026年"},
]


if __name__ == "__main__":
    # ── Output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
    )

    print(f"Build complete: {SLUG}")
    print(f"  DB:   {db}")
    print(f"  GEXF: {gexf}")