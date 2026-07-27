#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 湖南省
Parent City: 永州市
Region: 道县
Targets: 县委书记 & 县长

As of: 2026-07-24

数据来源: 
  1. 道县人民政府门户网站 (www.dx.gov.cn) 领导之窗栏目 — 政府领导班子
  2. 道县人民政府网政务公开 — 县级领导分工信息
  3. 道县融媒体中心新闻报道 — 刘华中任县委副书记、县长至2026年4月
  4. 道县人民政府网报道 — 王小丽任县委副书记、代理县长(2026年7月)

注意: 县委(县委书记/县委常委)领导信息未在县政府网站公布,
      本脚本仅包含政府系统(县长/副县长)可确认信息。
      县委书记信息待通过道县县委网站或永州市委组织部进一步核实。
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── 将 repo root 加入 path ──
_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "道县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-07-24"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：代理县长 (原县长刘华中已调离)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王小丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "education": "在职本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县县委副书记、代理县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 2026-07-14 更新 "
            "(www.dx.gov.cn/dx/ldzc/202607/6c5899d270de4a6a8486be6a266791c1.shtml)。"
            "主持县人民政府全面工作。完整履历待补充。"
        ),
    },
    # ════════════════════════════════════════
    # 前任县长：刘华中 (已调离)
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "刘华中",
        "gender": "男",
        "ethnicity": "汉族",  # inferred from name/region
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已调离道县",
        "current_org": "待查",
        "source": (
            "confirmed — 道县人民政府网 2026-04-14 新闻报道 "
            "「刘华中主持召开2026年县人民政府第5次常务会议」"
            "(www.dx.gov.cn/dx/zfhyjtj/202604/ce978239278e47c0a1070c2c11f6370d.shtml)。"
            "时任县委副书记、县长。至2026年7月已由王小丽接替为代理县长。去向待查。"
        ),
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "待查",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县县委常委、常务副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202403/54ba0bc7a13140cf8050b42233d1238f.shtml)。"
            "负责县政府常务工作，分管发改、财政、人社、税务、统计等工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：周丽
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "周丽",
        "gender": "女",
        "ethnicity": "瑶族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县县委常委、副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202006/e16833d2d5874c348f446de5fc5ee7e7.shtml)。"
            "负责科技、工信、招商引资、内外贸易等工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：李厚流
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李厚流",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "待查",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202111/f90ec296db4443c19dd1927446ce4599.shtml)。"
            "负责教育、交通运输工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：朱龙
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "朱龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202111/f5343c42de714d99b842eddd4dccb0a8.shtml)。"
            "负责卫生健康、医疗保障、行政审批服务、民政、残疾人事业工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：何小白
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "何小白",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "待查",
        "education": "中央党校法律专业函授本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202302/ef852414ddec48c9845cfb9a2b72c917.shtml)。"
            "负责文化旅游广电体育、市场监管、知识产权、生态环境工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长、县公安局局长：钟向华
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "钟向华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长、县公安局局长",
        "current_org": "道县人民政府、道县公安局",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202403/9caff6f35a374f70a090d02c119daed3.shtml)。"
            "负责公安、司法、退役军人事务、信访、禁毒工作。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：陈旺胜
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "陈旺胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "湖南宁远",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202403/0fe4ef6c098b44e981a5b6a59035197b.shtml)。"
            "负责自然资源、农业农村、乡村振兴、水利、林业、供销等工作。"
            "湖南宁远人。"
        ),
    },
    # ════════════════════════════════════════
    # 副县长：刘飞轮
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "刘飞轮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "道县副县长",
        "current_org": "道县人民政府",
        "source": (
            "confirmed — 道县人民政府门户网站 领导之窗 "
            "(www.dx.gov.cn/dx/ldzc/202303/806c38d0a2134089bcd822e4dc25778c.shtml)。"
            "负责住房和城乡建设、城市管理和综合执法工作。"
        ),
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共道县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共永州市委员会",
        "location": "湖南省永州市道县",
    },
    {
        "id": 2,
        "name": "道县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "永州市人民政府",
        "location": "湖南省永州市道县",
    },
    {
        "id": 3,
        "name": "道县公安局",
        "type": "政府",
        "level": "县",
        "parent": "道县人民政府",
        "location": "湖南省永州市道县",
    },
    {
        "id": 4,
        "name": "道县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "道县",
        "location": "湖南省永州市道县",
    },
    {
        "id": 5,
        "name": "政协道县委员会",
        "type": "政协",
        "level": "县",
        "parent": "道县",
        "location": "湖南省永州市道县",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 王小丽
    {
        "person_id": 1,
        "org_id": 2,
        "title": "代理县长",
        "start": "2026-07",
        "end": "present",
        "rank": "正处级",
        "note": "新任代理县长，主持县人民政府全面工作",
    },
    {
        "person_id": 1,
        "org_id": 1,
        "title": "县委副书记",
        "start": "2026-07",
        "end": "present",
        "rank": "正处级",
        "note": "",
    },
    # 刘华中 (前任县长)
    {
        "person_id": 2,
        "org_id": 2,
        "title": "县长",
        "start": "待查",
        "end": "2026-04",
        "rank": "正处级",
        "note": "截至2026年4月仍在任，2026年7月已由王小丽接替",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "县委副书记",
        "start": "待查",
        "end": "2026-04",
        "rank": "正处级",
        "note": "",
    },
    # 刘军
    {
        "person_id": 3,
        "org_id": 2,
        "title": "常务副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "县委常委、常务副县长，负责县政府常务工作",
    },
    {
        "person_id": 3,
        "org_id": 1,
        "title": "县委常委",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "",
    },
    # 周丽
    {
        "person_id": 4,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责科技、工信、招商引资等工作",
    },
    {
        "person_id": 4,
        "org_id": 1,
        "title": "县委常委",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "",
    },
    # 李厚流
    {
        "person_id": 5,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责教育、交通运输工作",
    },
    # 朱龙
    {
        "person_id": 6,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责卫生健康、医疗保障、行政审批等工作",
    },
    # 何小白
    {
        "person_id": 7,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责文旅广体、市场监管、生态环境等工作",
    },
    # 钟向华
    {
        "person_id": 8,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责公安、司法、退役军人事务等工作",
    },
    {
        "person_id": 8,
        "org_id": 3,
        "title": "县公安局局长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "",
    },
    # 陈旺胜
    {
        "person_id": 9,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责自然资源、农业农村、水利、林业等工作，宁远人",
    },
    # 刘飞轮
    {
        "person_id": 10,
        "org_id": 2,
        "title": "副县长",
        "start": "待查",
        "end": "present",
        "rank": "副处级",
        "note": "负责住建、城管执法工作",
    },
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 王小丽 ← 前任 → 刘华中 (predecessor_successor, confirmed)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "王小丽接替刘华中任道县县委副书记、县长（代理）",
        "overlap_org": "道县人民政府",
        "overlap_period": "2026年交替",
    },
    # 刘军 → 王小丽 (superior_subordinate via常务副县长协助县长)
    {
        "person_a": 3,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "刘军作为常务副县长协助县长王小丽分管县政府常务工作",
        "overlap_org": "道县人民政府",
        "overlap_period": "2026-07起",
    },
    # 陈旺胜 宁远人 — 同地区关系线索 (同永州市内跨县)
    {
        "person_a": 9,
        "person_b": 1,
        "type": "overlap",
        "context": "陈旺胜（宁远人）与王小丽同为道县领导班子成员",
        "overlap_org": "道县人民政府",
        "overlap_period": "2026-07起",
    },
    # 各位副县长与县长的工作关系
    *[
        {"person_a": i, "person_b": 1, "type": "superior_subordinate",
         "context": f"副县长在县长领导下分管专项工作",
         "overlap_org": "道县人民政府", "overlap_period": "2026-07起"}
        for i in range(4, 11)  # 周丽(4) through 刘飞轮(10)
    ],
]


if __name__ == "__main__":
    print(f"Building database and GEXF for {SLUG}...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")
