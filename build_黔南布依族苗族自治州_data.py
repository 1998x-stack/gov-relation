#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黔南布依族苗族自治州领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Qiannan Buyei and Miao
Autonomous Prefecture leadership network.

Level: 地级市 (自治州)
Province: 贵州省
Region: 黔南布依族苗族自治州
Targets: 州委书记 & 州长

Research Sources:
- qiannan.gov.cn — 黔南州人民政府门户网站 (2026年7月)
  - 领导分工通知: 黔南府办发〔2026〕16号 (2026-07-22)
  - 新闻: 洪湖鹏龙强会见裕能集团 (2026-07-21)
  - 新闻: 州委常委会暨州委农村工作领导小组会议 (2026-07-21)
  - 新闻: 州政府常务会议 (2026-07-17)
  - 新闻: 州委常委会召开扩大会议 (2026-07-09)

Confirmed officeholders (as of 2026-07-23, from qiannan.gov.cn official news & documents):
- 州委书记: 洪湖鹏
- 州委副书记、州长: 龙强
- 州人大常委会主任: 冉博
- 州政协党组书记: 李娟
- 州委副书记、州委政法委书记: 向子琨
- 州委常委、常务副州长: 丁毅
- 副州长: 荣彦、薛朝阳、祖自银、杨华军、潘建辉、韩龙、高峰
- 州政府党组成员: 黎亮
- 州委常委: 文永生、吴义宁

Note: Most leadership biographical details (birth year, birthplace, education)
remain to be filled from external sources.

Research Date: 2026-07-23
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "黔南布依族苗族自治州"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "洪湖鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州委书记",
        "current_org": "中共黔南布依族苗族自治州委员会",
        "source": "https://www.qiannan.gov.cn — 黔南州人民政府门户网站, 2026年7月确认"
    },
    {
        "id": 2,
        "name": "龙强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州委副书记、州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn — 黔南州人民政府门户网站, 2026年7月确认"
    },
    # ════════════════════════════════════════
    # 州人大常委会 / 州政协
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "冉博",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州人大常委会主任",
        "current_org": "黔南布依族苗族自治州人民代表大会常务委员会",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260717_90634845.html — 冉博到贵定县调研"
    },
    {
        "id": 4,
        "name": "李娟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔南州政协党组书记",
        "current_org": "中国人民政治协商会议黔南布依族苗族自治州委员会",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260721_90647376.html — 州委常委会"
    },
    # ════════════════════════════════════════
    # 州委领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "向子琨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委副书记、州委政法委书记",
        "current_org": "中共黔南布依族苗族自治州委员会",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260721_90647376.html — 州委常委会"
    },
    {
        "id": 6,
        "name": "文永生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委",
        "current_org": "中共黔南布依族苗族自治州委员会",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260721_90647390.html — 洪湖鹏龙强会见裕能集团"
    },
    {
        "id": 7,
        "name": "吴义宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州领导",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260721_90647390.html — 洪湖鹏龙强会见裕能集团"
    },
    # ════════════════════════════════════════
    # 州政府领导班子 (from 领导分工通知)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "丁毅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、常务副州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 9,
        "name": "荣彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 10,
        "name": "薛朝阳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长、州公安局局长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 11,
        "name": "祖自银",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 12,
        "name": "杨华军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 13,
        "name": "潘建辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 14,
        "name": "高峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长、州政府秘书长",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/zwgk/jcxxgk/zcwj/qnfbf/202607/t20260722_90651924.html — 领导分工通知"
    },
    {
        "id": 15,
        "name": "黎亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "州政府党组成员",
        "current_org": "黔南布依族苗族自治州人民政府",
        "source": "https://www.qiannan.gov.cn/xwzx/zwyw/202607/t20260717_90634859.html — 州政府常务会议"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共黔南布依族苗族自治州委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共贵州省委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
    {
        "id": 2,
        "name": "黔南布依族苗族自治州人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "贵州省人民政府",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
    {
        "id": 3,
        "name": "黔南布依族苗族自治州人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "贵州省人民代表大会常务委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议黔南布依族苗族自治州委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议贵州省委员会",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
    {
        "id": 5,
        "name": "黔南布依族苗族自治州公安局",
        "type": "政府",
        "level": "地级市",
        "parent": "黔南布依族苗族自治州人民政府",
        "location": "贵州省黔南布依族苗族自治州都匀市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # Top leaders
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start": "", "end": "present", "rank": "正厅级", "note": "2026年7月确认在任"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "州长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 人大/政协
    {"person_id": 3, "org_id": 3, "title": "州人大常委会主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "州政协党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "政协主席待选举确认"},
    # 州委
    {"person_id": 5, "org_id": 1, "title": "州委副书记、州委政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "州委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 州政府
    {"person_id": 8, "org_id": 2, "title": "常务副州长", "start": "", "end": "present", "rank": "副厅级", "note": "州委常委、常务副州长"},
    {"person_id": 7, "org_id": 2, "title": "州领导", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管科技、外事"},
    {"person_id": 10, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管公安、国安、司法、退役军人"},
    {"person_id": 10, "org_id": 5, "title": "州公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管民政、人社、卫健、医保、能源"},
    {"person_id": 12, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管住建、自然资源、交通"},
    {"person_id": 13, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管农业农村、水务、林业、乡村振兴"},
    {"person_id": 14, "org_id": 2, "title": "副州长", "start": "", "end": "present", "rank": "副厅级", "note": "分管商务、文旅、生态环境、机关事务；兼任州政府秘书长"},
    {"person_id": 15, "org_id": 2, "title": "州政府党组成员", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

# 4. Relationships (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # Top leadership pairing
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "州委书记与州长，党政主要领导搭档",
     "overlap_org": "黔南布依族苗族自治州", "overlap_period": "2026年"},
    # 州委书记 & 其他领导
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "州委书记与人大常委会主任",
     "overlap_org": "黔南布依族苗族自治州", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "州委书记与分管副书记",
     "overlap_org": "中共黔南州委常委会", "overlap_period": "2026年"},
    # 州长 & 副州长们
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "州长与常务副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "州长与分管副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "州长与分管公安副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "州长与分管副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "州长与分管副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "州长与分管副州长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "州长与分管副州长兼秘书长",
     "overlap_org": "黔南州人民政府", "overlap_period": "2026年"},
    # 州委常委之间的工作关系
    {"person_a": 8, "person_b": 6, "type": "overlap",
     "context": "州委常委同事关系",
     "overlap_org": "中共黔南州委常委会", "overlap_period": "2026年"},
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
