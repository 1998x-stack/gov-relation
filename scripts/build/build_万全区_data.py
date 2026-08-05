#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
万全区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 张家口市
Region: 万全区
Targets: 区委书记 & 区长

Research Sources:
- 张家口市万全区人民政府 官方网站 www.zjkwq.gov.cn — "政府领导"页面(channel/list/21.html)确认
  区长刘超及区政府领导班子；"政府领导"列表按职务更新至 2026-07。
- 万全区召开全区领导干部大会（2021-05-24/25，www.zjkwq.gov.cn 转载澎湃等）：市委组织部宣布
  戴鹏炜任万全区委书记；刘超任万全区委副书记（代区长）。
- 河北新闻网（2021-07-24 区第三次党代会，戴鹏炜当选区委书记）、张家口新闻网（2023-2024
  活动报道）、澎湃新闻（2024 思政课报道）— 确认戴鹏炜在任至 2024 年以后。
- 搜狗百科：戴鹏炜、赵满柱基本履历。
- 区政府各领导 profile（/single/21/*.html）提供出生年月、学历、分工 — 全部 2026 年仍在列。

Research Date: 2026-08-05
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "万全区"

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
        "name": "戴鹏炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "河北省博野县",
        "native_place": "河北省博野县",
        "education": "省委党校在职研究生学历",
        "party_join": "中共党员（1997年11月加入）",
        "work_start": "1996年9月",
        "current_post": "万全区委书记",
        "current_org": "中共张家口市万全区委员会",
        "source": "万全区领导干部大会（2021-05）；河北新闻网（2021-07-24）；《澎湃新闻》2024-09《奋进万全》思政课报道；2026春节《厚德万全》走访慰问报道。来源：www.zjkwq.gov.cn、sj.hbrb.com.cn、thepaper.cn"
    },
    {
        "id": 2,
        "name": "刘超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "万全区委副书记、区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区人民政府官网—政府领导页面《刘超》（/single/21/54376.html）。2021-05 任副区长、代区长；现任区委副书记、政府区长、政府党组书记，兼任河北张家口高新技术产业开发区（河北万全经济开发区）党工委副书记、管委会主任"
    },
    # ════════════════════════════════════════
    # 区政府领导班子（官网政府领导列表，2026-07 更新）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "施展文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区官网—政府领导页面《施展文》（2026-07-24）.html 发布"
    },
    {
        "id": 4,
        "name": "刘晓娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府副区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区官网—政府领导页面（刘晓娟，2026-07-24 发布）"
    },
    {
        "id": 5,
        "name": "刘东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府副区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区官网—政府领导页面（刘东，2026-06-01 更新）"
    },
    {
        "id": 6,
        "name": "张小飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府副区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区官网—政府领导页面（张小飞，2026-06-01 更新）"
    },
    {
        "id": 7,
        "name": "朱金磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "博士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府副区长、公安分局局长",
        "current_org": "张家口市公安局万区分局",
        "source": "万全区官网—政府领导页面（朱金磊，2026-07-24 更新）"
    },
    {
        "id": 8,
        "name": "王强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府副区长",
        "current_org": "张家口市万全区人民政府",
        "source": "万全区官网—政府领导页面（王强，2026-07-24 更新）"
    },
    # ════════════════════════════════════════
    # Historical Leaders (predecessors)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "赵满柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年4月",
        "birthplace": "河北省涿鹿县",
        "native_place": "河北省涿鹿县",
        "education": "研究生学历",
        "party_join": "中共党员（1987年8月加入）",
        "work_start": "待查",
        "current_post": "张家口市政协副主席（原兼万全区委书记）",
        "current_org": "中国人民政治协商会议张家口市委员会",
        "source": "搜狗百科·赵满柱；河北新闻网（万全县委书记）；《和谐京津冀》报道；万全区政法工作会议（wq.zjkpeace.gov.cn）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共张家口市万全区委员会",
        "type": "党委",
        "level": "县级",
        "location": "张家口市万全区",
        "parent": "中共张家口市委"
    },
    {
        "id": 2,
        "name": "张家口市万全区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "张家口市万全区",
        "parent": "张家口市人民政府"
    },
    {
        "id": 3,
        "name": "中共张家口市万全区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "张家口市万全区",
        "parent": "中共张家口市万全区委"
    },
    {
        "id": 4,
        "name": "张家口市公安局万区分局",
        "type": "政府",
        "level": "科级（法检系统为区分局）",
        "location": "张家口市万全区",
        "parent": "张家口市公安局"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议张家口市委员会",
        "type": "政协",
        "level": "地厅级",
        "location": "张家口市",
        "parent": ""
    },
    {
        "id": 6,
        "name": "河北张家口高新技术产业开发区（河北万全经济开发区）",
        "type": "开发区",
        "level": "省级",
        "location": "张家口市万全区",
        "parent": ""
    },
]

# 3. Positions
positions = [
    # 戴鹏炜
    {"person_id": 1, "org_id": 1, "title": "万全县委（区）委书记", "start": "2021年5月", "end": "present", "rank": "正处级", "note": "2021-05-24 任区委书记；2021-07 区三次党代会当选；截至 2025/2026 在任"},
    {"person_id": 1, "org_id": 2, "title": "万全区人民政府区长", "start": "2017年", "end": "2021年5月", "rank": "正处级", "note": "2020-01 区二届人大四次会议再次当选区长；2021-05 转任区委书记"},
    # 刘超
    {"person_id": 2, "org_id": 2, "title": "万全区委副书记、区长（区政府党组书记）", "start": "2021年5月", "end": "present", "rank": "正处级", "note": "2021-05 任区委副书记、区人民政府副区长（代区长）"}, 
    {"person_id": 2, "org_id": 6, "title": "河北张家口高新技术产业开发区管委会主任（兼）", "start": "2021年", "end": "present", "rank": "正处级（兼）", "note": "现任官网确认"},
    # 区政府班子
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责常务、发改、财政、应急、统计、政务等"},
    {"person_id": 4, "org_id": 2, "title": "区政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责自然资源、城乡建设、城管等"},
    {"person_id": 5, "org_id": 2, "title": "区政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责教育、人社、卫生、医保、交通等"},
    {"person_id": 6, "org_id": 2, "title": "区政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责市场监管、农业农村、乡村振兴、水务、民政等"},
    {"person_id": 7, "org_id": 4, "title": "区政府副区长、公安分局长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责公安、政法、信访、林业、民族等"},
    {"person_id": 8, "org_id": 2, "title": "区政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "负责商务、工信、文旅、体育、生态环境等"},
    # 赵满柱（前任）
    {"person_id": 9, "org_id": 1, "title": "万全县委书记（撤县设区后任万全区委书）", "start": "约2015年", "end": "2021年5月", "rank": "正处级", "note": "2016年万全县撤县设区；2021-05 卸任"},
    {"person_id": 9, "org_id": 5, "title": "张家口市政协副主席（兼）", "start": "约2019年", "end": "未知", "rank": "副厅级", "note": "卸任区委书记后主要在政协"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记戴鹏炜与区长刘超为万全区党政搭档（2021-05 至今）",
        "overlap_org": "中共张家口市万全区委员会／张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "赵满柱（2021-05 卸任）→ 戴鹏炜接任万区委书记",
        "overlap_org": "中共张家口市万全区委员会",
        "overlap_period": "2021年5月"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记戴鹏炜领导区委常委、常务副区长施展文",
        "overlap_org": "中共张家口市万全区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长刘超领导常务副区长施展文（政府班子核心局）",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长刘超领导副区长刘晓娟",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长刘超领导副区长刘东",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长刘超领导副区长张小飞",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长刘超领导副区长兼公安局长朱金磊",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长刘超领导副区长王强",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 9,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "赵满柱任区委书记期间刘超为政府领导；2021-05 刘超任区长",
        "overlap_org": "中共张家口市万全区委员会",
        "overlap_period": "2021年5月"
    },
    {
        "person_a": 7,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "副区长兼公安局长朱金磊接受区长刘超领导（政府序列）",
        "overlap_org": "张家口市万全区人民政府",
        "overlap_period": "2021-2026"
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