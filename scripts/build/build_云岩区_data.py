#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云岩区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 贵州省
Parent City: 贵阳市
Region: 云岩区
Targets: 区委书记 & 区长

Research Sources (primary, official):
- 云岩区人民政府门户网站 (领导之窗) https://www.yunyan.gov.cn/zwgk/ldzc/
  - 王飞   https://www.yunyan.gov.cn/zwgk/ldzc/202212/t20221225_82709096.html (区委书记)
  - 刘仁好 https://www.yunyan.gov.cn/zwgk/ldzc/202602/t20260224_89566829.html (区长, 2026-02 当选)
  - 王国鉴 https://www.yunyan.gov.cn/zwgk/ldzc/202505/t20250523_87912839.html (常务副区长)
  - 董政   https://www.yunyan.gov.cn/zwgk/ldzc/202402/t20240202_83669536.html (区委常委、副区长)
  - 张涛   https://www.yunyan.gov.cn/zwgk/ldzc/202411/t20241119_86105616.html (区委常委、副区长挂职)
  - 周莲   https://www.yunyan.gov.cn/zwgk/ldzc/202607/t20260731_90680967.html (副区长, 2026-06 当选)
  - 赵荣文 https://www.yunyan.gov.cn/zwgk/ldzc/202001/t20200106_82709102.html (副区长)
  - 代素君 https://www.yunyan.gov.cn/zwgk/ldzc/202402/t20240202_83669517.html (副区长兼公安局长)
  - 郭蒂   https://www.yunyan.gov.cn/zwgk/ldzc/202405/t20240508_84595823.html (副区长, 外出挂职)
  - 杨凯   https://www.yunyan.gov.cn/zwgk/ldzc/202512/t20251201_89003019.html (副区长, 2025-11 当选)
  - 刘坤   https://www.yunyan.gov.cn/zwgk/ldzc/202602/t20260224_89571443.html (副区长, 2026-02 当选)

Research Date: 2026-08-05

Confidence:
- 现任区委书记(王飞)、区长(刘仁好)及全部领导班子成员由官方门户"领导之窗"逐人页面确认 (confirmed)。
- 批量身份字段 (籍贯/学历/入党时间/起任时间) 部分公开, 未公开字段以"待查"标注, 并在 open_questions 标记。
- 王飞、刘仁好的完整任职履历、前任区委书记/区长及跨区交流细节受网络搜索不可用限制 → 记入报告 open_gaps 待后续补查。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "云岩区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──────────────────────────────────────────────────────────────

# 1. Persons (id 1-99; 101+ 为机构)
persons = [
    # ═══ Current Top Leaders ═══
    {
        "id": 1,
        "name": "王飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "贵州息烽",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云岩区委书记、贵州云岩经济开发区党工委书记（兼）",
        "current_org": "中共云岩区委员会",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202212/t20221225_82709096.html (2026-07-27 核对); confidence=confirmed",
    },
    {
        "id": 2,
        "name": "刘仁好",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1975-04",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记、区人民政府区长、云岩经开区党工委副书记、管委会主任",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202602/t20260224_89566829.html; 2026-02 当选区长; confidence=confirmed",
    },
    # ═══ 区委常委、区政府班子 ═══
    {
        "id": 3,
        "name": "王国鉴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区政府常务副区长",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202505/t20250523_87912839.html; 2025-05 当选副区长; confidence=confirmed",
    },
    {
        "id": 4,
        "name": "董政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "贵州贵阳",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区政府副区长，经开区党工委副书记、管委会副主任",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202402/t20240202_83669536.html; 2024-02 当选副区长; confidence=confirmed",
    },
    {
        "id": 5,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-02",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区政府副区长（挂职）",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202411/t20241119_86105616.html; 2024-09 当选挂职副区长; confidence=confirmed",
    },
    {
        "id": 6,
        "name": "赵荣文",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1975-11",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202001/t20200106_82709102.html; 2019-11 当选副区长; confidence=confirmed",
    },
    {
        "id": 7,
        "name": "代素君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "待查",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长（党组成员）、贵阳市公安局云岩分局党委书记、局长",
        "current_org": "贵阳市公安局云岩分局",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202402/t20240202_83669517.html; 2024-02 当选副区长; confidence=confirmed",
    },
    {
        "id": 8,
        "name": "郭蒂",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-01",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长（党组成员）、八鸽岩街道党工委书记（外出挂职）",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202405/t20240508_84595823.html; 2024-03 当选副区长; confidence=confirmed",
    },
    {
        "id": 9,
        "name": "杨凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长，区住房和城乡建设局党委书记、局长，区城市更新事务中心主任",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202512/t20251201_89003019.html; 2025-11 当选副区长; confidence=confirmed",
    },
    {
        "id": 10,
        "name": "刘坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-11",
        "birthplace": "待查",
        "education": "大学（工学学士）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202602/t20260224_89571443.html; 2026-02 当选副区长; confidence=confirmed",
    },
    {
        "id": 11,
        "name": "周莲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-06",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民政府副区长",
        "current_org": "贵阳市云岩区人民政府",
        "source": "official yunyan.gov.cn /zwgk/ldzc/202607/t20260731_90680967.html; 2026-06 当选副区长; confidence=confirmed",
    },
]

# 2. Organizations
organizations = [
    {"id": 101, "name": "中共云岩区委员会", "type": "党委", "level": "县级", "parent": "中共贵阳市委员会", "location": "贵州省贵阳市云岩区"},
    {"id": 102, "name": "贵阳市云岩区人民政府", "type": "政府", "level": "县级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市云岩区"},
    {"id": 103, "name": "贵州云岩经济开发区", "type": "开发区", "level": "县级", "parent": "贵阳市人民政府", "location": "贵州省贵阳市云岩区"},
    {"id": 104, "name": "贵阳市公安局云岩分局", "type": "政府", "level": "县级", "parent": "贵阳市公安局", "location": "贵州省贵阳市云岩区"},
    {"id": 105, "name": "云岩区住房和城乡建设局", "type": "政府", "level": "县级", "parent": "贵阳市云岩区人民政府", "location": "贵州省贵阳市云岩区"},
    {"id": 106, "name": "八鸽岩街道党工委", "type": "党委", "level": "乡级", "parent": "中共云岩区委员会", "location": "贵州省贵阳市云岩区"},
    {"id": 120, "name": "中共贵阳市委员会", "type": "党委", "level": "地级", "parent": "中共贵州省委员会", "location": "贵州省贵阳市"},
]

# 3. 任职记录 (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start_date": "待查", "end_date": "present",
     "rank": "正处级", "note": "official 2026-07 在位; 兼贵州云岩经开区党工委书记"},
    {"person_id": 1, "org_id": 103, "title": "党工委书记（兼）", "start_date": "待查", "end_date": "present",
     "rank": "正处级", "note": "贵州云岩经济开发区党工委书记"},
    # 区长
    {"person_id": 2, "org_id": 102, "title": "区委副书记、区政府区长", "start_date": "2026-02", "end_date": "present",
     "rank": "正处级", "note": "2026-02 当选区长"},
    {"person_id": 2, "org_id": 103, "title": "经开区党工委副书记、管委会主任", "start_date": "2026-02", "end_date": "present",
     "rank": "正处级", "note": "兼"},
    # 区政府班子
    {"person_id": 3, "org_id": 102, "title": "区委常委、常务副区长", "start_date": "2025-05", "end_date": "present",
     "rank": "副处级", "note": "2025-05 当选副区长; 负责区政府常务工作"},
    {"person_id": 4, "org_id": 102, "title": "区委常委、区政府副区长", "start_date": "2024-02", "end_date": "present",
     "rank": "副处级", "note": "2024-02 当选副区长; 经开区党工委副书记/管委会副主任"},
    {"person_id": 5, "org_id": 102, "title": "区委常委、区政府副区长（挂职）", "start_date": "2024-09", "end_date": "present",
     "rank": "副处级", "note": "挂职"},
    {"person_id": 6, "org_id": 102, "title": "区政府副区长", "start_date": "2019-11", "end_date": "present",
     "rank": "副处级", "note": "2019-11 当选副区长"},
    {"person_id": 7, "org_id": 102, "title": "区政府副区长（党组成员）", "start_date": "2024-02", "end_date": "present",
     "rank": "副处级", "note": "兼市公安局云岩分局局长"},
    {"person_id": 7, "org_id": 104, "title": "贵阳市公安局云岩分局局长、党委书记", "start_date": "2024-02", "end_date": "present",
     "rank": "副处级", "note": "兼职"},
    {"person_id": 8, "org_id": 102, "title": "区政府副区长（党组成员）", "start_date": "2024-03", "end_date": "present",
     "rank": "副处级", "note": "外出挂职"},
    {"person_id": 8, "org_id": 106, "title": "八鸽岩街道党工委书记", "start_date": "待查", "end_date": "present",
     "rank": "乡科级正职", "note": "兼任"},
    {"person_id": 9, "org_id": 102, "title": "区政府副区长", "start_date": "2025-11", "end_date": "present",
     "rank": "副处级", "note": "2025-11 当选副区长"},
    {"person_id": 9, "org_id": 105, "title": "区住房和城乡建设局党委书记、局长", "start_date": "待查", "end_date": "present",
     "rank": "正科级", "note": "兼任"},
    {"person_id": 10, "org_id": 102, "title": "区政府副区长", "start_date": "2026-02", "end_date": "present",
     "rank": "副处级", "note": "2026-02 当选副区长"},
    {"person_id": 11, "org_id": 102, "title": "区政府副区长", "start_date": "2026-06", "end_date": "present",
     "rank": "副处级", "note": "2026-06 当选副区长"},
]

# 4. 关系 (确认或可推断的共事/搭档关系)
relationships = [
    # 书记-区长: 党政班子搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "云岩区委书记与区委副书记/区长构成党政班子搭档，区委书记主持区委全面工作、区长主持区政府全面工作",
     "overlap_org": "中共云岩区委员会", "overlap_period": "2026-present"},
    # 区长-常务副区长: 政府班子上下级协作
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "常务副区长负责区政府常务工作，协助区长负责人事、财政、审计",
     "overlap_org": "贵阳市云岩区人民政府", "overlap_period": "2025-present"},
    # 区委常委班子成员与书记共事
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委常委与区委书记同属区委常委会议班子",
     "overlap_org": "中共云岩区委员会", "overlap_period": "2024-present"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委常委（挂职）与区委书记同属区委常委会议班子",
     "overlap_org": "中共云岩区委员会", "overlap_period": "2024-present"},
]

# ── Build ──
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

    conn = sqlite3.connect(DB_PATH)
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  [{t}] {n}")
    conn.close()
    print("Done.")