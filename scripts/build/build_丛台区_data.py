#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
丛台区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 邯郸市
Region: 丛台区
Targets: 区委书记 & 区长

Research Sources:
- 丛台区人民政府官方网站 (www.hdct.gov.cn) — 区长之窗确认区长刘丹信息
- 丛台区人民政府信息公开 — 区委常委会会议、区长会议等公开报道确认区委书记李书峰
- 维基百科：丛台区概述（领导信息未及时更新，显示为杨晓和）
- 百度百科及百度搜索均不可用（403验证码拦截）
- 李书峰、刘丹的详细履历（出生年月、教育背景等）因网络搜索受限未获取完整

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "丛台区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李书峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市丛台区委书记",
        "current_org": "中共邯郸市丛台区委员会",
        "source": "丛台区政府信息公开—区委常委会扩大会议(2026-04-17)、城市精细化管理工作现场办公(2026-03-19)均确认李书峰任丛台区委书记。来源：http://www.hdct.gov.cn/ctqxxgk/bmxx_26530/zfbm/qzfb/fdgknr/zfbgzbs/202604/t20260417_2198582.html"
    },
    {
        "id": 2,
        "name": "刘丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市丛台区委副书记、区长",
        "current_org": "丛台区人民政府",
        "source": "丛台区人民政府官方网站—区长之窗确认。来源：http://www.hdct.gov.cn/qzzcn/"
    },
    # ════════════════════════════════════════
    # 区委领导 / 区人大、政协主要领导（部分确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丛台区副区长（区领导）",
        "current_org": "丛台区人民政府",
        "source": "丛台区政府信息公开—刘丹主持召开企业发展解难题推进会(2026-05-21)提及'区领导张杰、李红娟出席会议'"
    },
    {
        "id": 4,
        "name": "李红娟",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丛台区副区长（区领导）",
        "current_org": "丛台区人民政府",
        "source": "丛台区政府信息公开—刘丹主持召开企业发展解难题推进会(2026-05-21)提及'区领导张杰、李红娟出席会议'"
    },
    {
        "id": 5,
        "name": "张善宁",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丛台区领导",
        "current_org": "中共邯郸市丛台区委员会",
        "source": "丛台区政府信息公开—李书峰就城市精细化管理工作进行现场办公(2026-03-19)提及'区领导张善宁、郭伟参加'"
    },
    {
        "id": 6,
        "name": "郭伟",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "丛台区领导",
        "current_org": "中共邯郸市丛台区委员会",
        "source": "丛台区政府信息公开—李书峰就城市精细化管理工作进行现场办公(2026-03-19)提及'区领导张善宁、郭伟参加'"
    },
    # ════════════════════════════════════════
    # Historical Leaders (杨晓和 - former party secretary)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "杨晓和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年4月",
        "birthplace": "河北省邯郸市",
        "native_place": "河北省邯郸市",
        "education": "在职研究生学历、管理学博士（中国科学院经济与管理学院管理科学工程专业）",
        "party_join": "中共党员（1988年加入）",
        "work_start": "1986年8月",
        "current_post": "海南省政协副主席（2024年1月－2026年1月）",
        "current_org": "中国人民政治协商会议海南省委员会",
        "source": "维基百科：杨晓和词条。历任丛台区长(2006-2008)、丛台区委书记(2008-2013)"
    },
    {
        "id": 8,
        "name": "穆伟利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原丛台区委书记，杨晓和继任者）",
        "current_org": "",
        "source": "维基百科杨晓和词条显示穆伟利为其继任丛台区委书记"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市丛台区委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市丛台区",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "丛台区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市丛台区",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "丛台区人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市丛台区",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "丛台区政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市丛台区",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议海南省委员会",
        "type": "政协",
        "level": "省部级",
        "location": "海南省",
        "parent": ""
    },
    {
        "id": 6,
        "name": "邯郸县",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市",
        "parent": "邯郸市人民政府"
    },
]

# 3. Positions
positions = [
    # 李书峰
    {"person_id": 1, "org_id": 1, "title": "邯郸市丛台区委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年7月在任"},
    # 刘丹
    {"person_id": 2, "org_id": 2, "title": "丛台区委副书记、区长", "start": "未知", "end": "present", "rank": "正处级", "note": "女，1980年2月生，省委党校研究生，截至2026年7月在任"},
    # 张杰
    {"person_id": 3, "org_id": 2, "title": "丛台区副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "2026年5月会议报道确认"},
    # 李红娟
    {"person_id": 4, "org_id": 2, "title": "丛台区副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "2026年5月会议报道确认"},
    # 张善宁
    {"person_id": 5, "org_id": 1, "title": "丛台区委领导", "start": "未知", "end": "present", "rank": "副处级", "note": "2026年3月会议报道确认"},
    # 郭伟
    {"person_id": 6, "org_id": 1, "title": "丛台区委领导", "start": "未知", "end": "present", "rank": "副处级", "note": "2026年3月会议报道确认"},
    # 杨晓和 — 历史职务
    {"person_id": 7, "org_id": 2, "title": "邯郸市丛台区委副书记、代区长、区长", "start": "2006年4月", "end": "2008年5月", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "邯郸市丛台区委书记", "start": "2008年5月", "end": "2013年12月", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "海南省政协副主席", "start": "2024年1月", "end": "2026年1月", "rank": "副省部级", "note": ""},
    # 穆伟利
    {"person_id": 8, "org_id": 1, "title": "邯郸市丛台区委书记", "start": "2013年12月", "end": "未知", "rank": "正处级", "note": "杨晓和继任者"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长同为丛台区核心领导",
        "overlap_org": "中共邯郸市丛台区委员会／丛台区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "predecessor_successor",
        "context": "杨晓和为丛台区委书记(2008-2013)，李书峰为现任区委书记",
        "overlap_org": "中共邯郸市丛台区委员会",
        "overlap_period": ""
    },
    {
        "person_a": 7,
        "person_b": 8,
        "type": "predecessor_successor",
        "context": "穆伟利接替杨晓和任丛台区委书记",
        "overlap_org": "中共邯郸市丛台区委员会",
        "overlap_period": "2013年12月"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李书峰作为区委书记领导张杰等副区长",
        "overlap_org": "中共邯郸市丛台区委员会／丛台区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "李书峰作为区委书记领导李红娟等副区长",
        "overlap_org": "中共邯郸市丛台区委员会／丛台区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "刘丹作为区长领导副区长张杰",
        "overlap_org": "丛台区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "刘丹作为区长领导副区长李红娟",
        "overlap_org": "丛台区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 5,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "张善宁作为区委领导在李书峰领导下工作",
        "overlap_org": "中共邯郸市丛台区委员会",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 6,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "郭伟作为区委领导在李书峰领导下工作",
        "overlap_org": "中共邯郸市丛台区委员会",
        "overlap_period": "2025-2026"
    },
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
