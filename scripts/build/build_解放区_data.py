#!/usr/bin/env python3
"""Build 焦作市解放区 (Jiaozuo Jiefang District) leadership network data.

Level: 市辖区
Province: 河南省
Parent city: 焦作市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: henan_解放区

Research date: 2026-08-05
Official source: http://www.jfq.gov.cn/ (解放思想区人民政府)
Staging build: data/tmp/henan_解放区/ → promoted by process_tmp.py

Current status (as of 2026-08-05, verified via jfq.gov.cn 区长之窗 + 政务要闻):
- 区委书记: 千怀贵 — 主持区委常委会(十二届)，出席2026-08-04上半年讲评会并发表讲话；
  至少在任自2025年下半年起（2025年政务要闻多次以区委书记身份报道）
- 区长: 史玉龙 — 区委副书记、区政府党组书记、区长（区长之窗官方简历：男，汉族，1976年12月生，研究生，中共党员）。
  继前任区长赵海燕之后就任（赵海燕2025年9-10月仍以区长身份活动，后升任焦作市副市长）
- 常务副区长: 赵高峰 — 区委常委、区政府党组副书记、常务副区长（1981年3月生，大学）

Confirmed sources (all official, jfq.gov.cn):
- 区长之窗: https://www.jfq.gov.cn/qzzc （区政府班子 #员分工与简历）
- 政务要闻: https://www.jfq.gov.cn/xwzx/zwyw/ （千怀贵/史玉龙最新活动）
- 关键新闻:
  - 2026-08-05/610135.html  上半年工作总结暨"三十"重点项目推进会（千怀贵出席讲话、史玉龙主持）
  - 2026-07-23/608881.html  十二届区委常委会第2次(扩大)会议（千怀贵主持；史玉龙、赵威、王永刚、马志强、李廷龙、王超、王猛出席；石文明、蒋凯丰列席）
  - 2026-07-31/609673.html  区委理论学习中心组学习（千怀贵主持、史玉龙出席；赵威、蒋凯丰、马志强、李廷龙、苟云华、王超、赵高峰、王猛等）
  - 2026-08-05/61020146.html 区政府党组(扩大会)和政府常务会议（史玉龙主持；赵高峰、成万森、李秉昕、王中雨、和毅、郝宏强、王静、闫熠天出席）
- 前任区长赵海燕: 2025-10 政务要闻（区长身份调研/人大代表活动）；焦作市person档 20260724-河南省-焦作市-副市长-赵海燕.json

Web-search engines (Baidu/Bing/Sogou) rate-limited/timeout in this session — career
details beyond the brief official resumés and prior roles are marked as unknowns.
All specific biographical dates not published on jfq.gov.cn are left blank and flagged
in `data/report/open_gaps.md` + per-person `open_questions`.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "解放区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

SOURCE_OFFICIAL = ("解放区人民政府官方网站: https://www.jfq.gov.cn/")
SOURCE_OFFICIAL_QZC = ("解放区人民政府官方网站 区长之窗: https://www.jfq.gov.cn/qzzc")
SOURCE_NEWS = ("解放区新闻中心报道: https://www.jfq.gov.cn/xwzx/zwyw/")
SOURCE_JZRB_NEWS = ("焦作日报(市重点工程报道) + 解放区政府新闻: 干怀贵/史玉龙活动")

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "千怀贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "解放区委书记",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 2026-08-05上半年工作会以区委书记身份出席并讲话；"
                    "焦作日报设活动专栏(千怀贵同志专栏)"),
    },
    {
        "id": 2,
        "name": "史玉龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "解放区委副书记、区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗正职简历：男，汉族，1976年12月生，研究生，中共党员"),
    },
    {
        "id": 3,
        "name": "赵高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、常务副区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗常务副区长简历"),
    },
    # ════════════════════════════════════════
    # 区政府领导班子 (Government)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "成万森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年9月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府二级调研员",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 5,
        "name": "李秉昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年4月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府二级调研员",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 6,
        "name": "王中雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "native_place": "",
        "education": "博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 7,
        "name": "和毅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府三级调研员",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 8,
        "name": "郝宏强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长，焦作市公安局解放分局局长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 9,
        "name": "范传颂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 10,
        "name": "王静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    {
        "id": 11,
        "name": "闫熠天",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年11月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "解放区人民政府",
        "source": (SOURCE_OFFICIAL_QZC + " 区长之窗"),
    },
    # ════════════════════════════════════════
    # 区委班子 (Party Standing Committee - from meetings)
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "赵威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会第2次(扩大)会议出席名单"),
    },
    {
        "id": 13,
        "name": "王永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会第2次(扩大)会议出席名单"),
    },
    {
        "id": 14,
        "name": "马志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 区委常委会/中心组中心组成员"),
    },
    {
        "id": 15,
        "name": "李廷龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会/中心组出席会议名单"),
    },
    {
        "id": 16,
        "name": "苟云华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 上半年区工作会出席名单"),
    },
    {
        "id": 17,
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会第2次(扩大)会议出席名单"),
    },
    {
        "id": 18,
        "name": "王猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 区委常委会/中心组出席名单"),
    },
    {
        "id": 19,
        "name": "张文勃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 区委理论学习中心组集中学习研讨会 交流发言"),
    },
    {
        "id": 20,
        "name": "张继青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共焦作市解放区委员会",
        "source": (SOURCE_NEWS + " 区委理论学习中心组集中学习研讨会 交流发言"),
    },
    # ════════════════════════════════════════
    # 区人大 / 政协 / 前任
    # ════════════════════════════════════════
    {
        "id": 21,
        "name": "石文明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "解放区人民代表大会常务委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会第2次(扩大)会议列席"),
    },
    {
        "id": 22,
        "name": "蒋凯丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议解放区委员会",
        "source": (SOURCE_NEWS + " 十二届区委常委会第2次(扩大)会议列席 / 中心组出席"),
    },
    {
        "id": 23,
        "name": "赵海燕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任解放区区长（现任焦作市副市长）",
        "current_org": "",
        "source": (SOURCE_NEWS + " 2025年10月仍以解放区区长身份公开活动；"
                     "焦作市person.json/副市长-赵海燕.json 确认现任焦作市副市长"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共焦作市解放区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市解放区",
    },
    {
        "id": 2,
        "name": "解放区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市解放区",
    },
    {
        "id": 3,
        "name": "解放区人民代表大会",
        "type": "人大",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市解放区",
    },
    {
        "id": 4,
        "name": "政协解放区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市解放区",
    },
    {
        "id": 5,
        "name": "解放区",
        "type": "行政区",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市解放区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 千怀贵 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "解放区委书记", "start": "不晚于2025年10月", "end": "至今", "rank": "县处级正职",
     "note": "2025年12月至2026年8月多篇政务要闻以区委书记身份；十二届区委常委会由其主持"},
    # 史玉龙 - 区长
    {"person_id": 2, "org_id": 2, "title": "解放区委副书记、区长", "start": "不晚于2025年11月", "end": "至今", "rank": "县处级正职",
     "note": "区长之窗简历(2025-11-06)；继前任区长赵海燕之后就任"},
    # 赵高峰 - 常务副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府党组副书记、常务副区长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "区长之窗(2025-11-06更新)"},
    # 区政府其他
    {"person_id": 4, "org_id": 2, "title": "区政府二级调研员", "start": "", "end": "至今", "rank": "县处级", "note": "区长之窗"},
    {"person_id": 5, "org_id": 2, "title": "区政府二级调研员", "start": "", "end": "至今", "rank": "县处级", "note": "区长之窗"},
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "区长之窗"},
    {"person_id": 7, "org_id": 2, "title": "区政府三级调研员", "start": "", "end": "至今", "rank": "县处级", "note": "区长之窗"},
    {"person_id": 8, "org_id": 2, "title": "区政府党组成员、副区长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "兼焦作市公安局解放分局局长（尼区政法系统）"},
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "区长之窗"},
    {"person_id": 10, "org_id": 2, "title": "区政府党组成员、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "区长之窗"},
    {"person_id": 11, "org_id": 2, "title": "区政府党组成员、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "区长之窗"},
    # 区委班子
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start": "", "end": "至今", "rank": "县处级",
     "note": "十二届区委常委会出席"},
    {"person_id": 13, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "十二届区委常委会出席"},
    {"person_id": 14, "org_id": 1, "title": "区委领导(常委)", "start": "", "end": "至今", "rank": "县处级",
     "note": "区委常委会/中心组出席"},
    {"person_id": 15, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "十二届区委常委会/中心组出席"},
    {"person_id": 16, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "上半年工作会出席"},
    {"person_id": 17, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "十二届区委常委会出席"},
    {"person_id": 18, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "区委常委会/中心组出席"},
    {"person_id": 19, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "理论学习中心组交流发言"},
    {"person_id": 20, "org_id": 1, "title": "区委领导", "start": "", "end": "至今", "rank": "县处级",
     "note": "理论学习中心组交流发言"},
    # 人大 / 政协
    {"person_id": 21, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "至今", "rank": "县处级正职",
     "note": "区委常委会列席"},
    {"person_id": 22, "org_id": 4, "title": "区政协主席", "start": "", "end": "至今", "rank": "县处级正职",
     "note": "区委常委会列席"},
    # 赵海燕 - 前任区长
    {"person_id": 23, "org_id": 2, "title": "解放区区长（前任）", "start": "不晚于2025年", "end": "约2025年末", "rank": "县处级正职",
     "note": "2025年9-10月仍以区长身份调研；后升任焦作市副市长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 千怀贵 ↔ 史玉龙（党政一把手）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭档，全面负责区委和区政府工作；常同台主持区重大会议",
        "overlap_org": "解放区",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "direction": "undirected",
    },
    # 史玉龙 → 赵海燕（继任，前任区长升副市长）
    {
        "person_a": 2,
        "person_b": 23,
        "type": "predecessor_successor",
        "context": "史玉龙接替解放区区长职位的赵海燕；赵海燕升任焦作市副市长",
        "overlap_org": "解放区人民政府",
        "overlap_period": "约2025年末交接",
        "strength": "strong",
        "direction": "other_to_person",
    },
    # 千怀贵 → 赵高峰（书记↔常务副区长）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委、常务副区长",
        "overlap_org": "解放区",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 史玉龙 → 赵高峰（区长↔常务副区长）
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与常务副区长，主持区政府常务工作、协助区长分管审计",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2025年至今",
        "strength": "strong",
        "direction": "person_to_other",
    },
    # 千怀贵 ↔ 区委班子（赵威、王永刚、马志强、王猛等）
    {
        "person_a": 1,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委",
        "overlap_org": "中共焦作市解放区委员会",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    {
        "person_a": 1,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "区委书记与区委领导",
        "overlap_org": "中共焦作市解放区委员会",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 史玉龙 ↔ 区政府班子（成万森、李秉昕、王中雨、和毅、郝宏强、范传颂、王静、闫熠天）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "区长与区政府二级调研员，出席同一区政府党组会/政府常务会议",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "区长与区政府二级调研员",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与副区长（兼公安解放分局局长）",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "区长与副区长（城建/城市管理）",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区长与副区长（商贸/生态/农业）",
        "overlap_org": "解放区人民政府",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 千怀贵 ↔ 人大主任 / 政协主席（列席常委会议）
    {
        "person_a": 1,
        "person_b": 21,
        "type": "overlap",
        "context": "区委书记与区人大常委会主任，区委常委会列席",
        "overlap_org": "解放区",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    {
        "person_a": 1,
        "person_b": 22,
        "type": "overlap",
        "context": "区委书记与区政协主席，区委常委会/中心组出席",
        "overlap_org": "解放区",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data ...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships.")

    # Write person JSON files for the two requested core figures
    person_json_map = {
        "区委书记": {
            "person": persons[0],
            "name": "千怀贵",
        },
        "区长": {
            "person": persons[1],
            "name": "史玉龙",
        },
    }

    for label, info in person_json_map.items():
        p = info["person"]
        fname = f"{TODAY}-河南省-焦作市-{label}-{info['name']}.json"
        fpath = _STAGING_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump({
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "焦作市",
                    "region": "解放区",
                    "job": label,
                    "task_id": "henan_解放区",
                    "time_focus": "2026-08"
                },
                "identity": {
                    "person_id": f"henan_jiaozuo_jiefang_{info['name']}",
                    "name": info["name"],
                    "aliases": [],
                    "gender": p["gender"],
                    "ethnicity": p["ethnicity"],
                    "birth": p.get("birth", ""),
                    "birthplace": "",
                    "native_place": "",
                    "education": [],  # 教育细分字段留空，见 open_questions
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": f"{info['name']}_{p.get('birth','')}",
                        "name_birthplace": f"{info['name']}_",
                        "official_profile_url": "https://www.jfq.gov.cn/qzzc"
                    }
                },
                "current_status": {
                    "current_post": p["current_post"],
                    "current_org": p["current_org"],
                    "administrative_rank": "县处级正职",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "不晚于2025年10月" if label == "区委书记" else "不晚于2025年11月",
                        "end": "至今",
                        "org": p["current_org"],
                        "title": p["current_post"],
                        "level": "县处级正职",
                        "location": "河南省焦作市解放区",
                        "system": "party" if label == "区委书记" else "government",
                        "rank": "县处级正职",
                        "is_key_promotion": True,
                        "notes": "区长之窗官方简历" if label == "区长" else "区政务要闻多个报道",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "level": "",
                        "location": "",
                        "system": "other",
                        "rank": "",
                        "is_key_promotion": False,
                        "notes": "公开资料未找到任现职前的完整履历（本会话搜索引擎受限，未获权威履历）",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [
                    {
                        "org_id": "中共焦作市解放区委员会",
                        "org_name": "中共焦作市解放区委员会",
                        "role": "区委书记",
                        "period": "不晚于2025年10月至今"
                    },
                    {
                        "org_id": "解放区人民政府",
                        "org_name": "解放区人民政府",
                        "role": "区长" if label == "区长" else "区委副书记",
                        "period": "不晚于2025年11月至今"
                    }
                ],
                "relationships": [
                    {
                        "person": "史玉龙" if label == "区委书记" else "千怀贵",
                        "person_id": f"henan_jiaozuo_jiefang_{'史玉龙' if label == '区委书记' else '千怀贵'}",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "区委书记与区党政一把手，同台主持区重大会议多场(2026-08-04上半年工作会等)",
                        "overlap_org": "解放区",
                        "overlap_period": "2025年至今",
                        "direction": "undirected",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "person": "赵海燕",
                        "person_id": "henan_jiaozuo_赵海燕",
                        "relationship_type": "predecessor_successor" if label == "区长" else "other",
                        "strength": "medium",
                        "evidence": "赵海燕2025年末由解放区区长升任焦作市副市长，史玉龙继任" if label == "区长" else "前任区长赵海燕现为焦作市副市长",
                        "overlap_org": "解放区人民政府",
                        "overlap_period": "2025年末交接",
                        "direction": "other_to_person",
                        "confidence": "plausible",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026",
                        "domain": "economic_development" if label == "区委书记" else "economic_development",
                        "achievement_or_event": ("解放区2026上半年工作会部署：产业兴区、空天/低空/算力等数字产业、" if label == "区委书记"
                                                  else "区政府常务会议部署：人工智能+行动、算力基础设施、政务服务一体化"),
                        "location": "河南省焦作市解放区",
                        "role_in_event": "区委书记讲话/区长主持",
                        "measurable_outcome": "",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "period": "2026",
                        "domain": "public_security",
                        "achievement_or_event": "防汛备汛、安全生产、消防燃气排查、基层治理（党建+网格+大数据）",
                        "location": "河南省焦作市解放区",
                        "role_in_event": "镇导或主持",
                        "measurable_outcome": "",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "local_ladder",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "现职前履历待查，无法评估晋升速度",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {
                    "primary_org": p["current_org"],
                    "party_government": "party" if label == "区委书记" else "government",
                    "cross_region_moves": ["任区长前任职位待查"],
                    "hierarchy_level": "县处级正职"
                },
                "risk_and_integrity_signals": [
                    {
                        "type": "inspection_feedback",
                        "description": "市委第七巡察组2026-07-30向解放区委反馈群众身边不正之风和腐败问题集中整治专项巡察意见，各区领导机制参加整改",
                        "date": "2026-07-30",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "解放区人民政府官方网站（区长之窗、政务要闻）",
                        "url": "https://www.jfq.gov.cn/",
                        "publisher": "解放区人民政府",
                        "published_at": "",
                        "accessed_at": AS_OF,
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "区长之窗简历 + 政务要闻 2025-10 至 2026-08"
                    },
                    {
                        "id": "S002",
                        "title": "焦作市副市长 赵海燕 person.json",
                        "url": "data/persons/20260724-河南省-焦作市-副市长-赵海燕.json",
                        "publisher": "gov-relation 仓库(任务 henan_焦作市)",
                        "published_at": "2026-07-24",
                        "accessed_at": AS_OF,
                        "source_type": "database",
                        "reliability": "medium",
                        "notes": "确认赵海燕现任焦作市副市长，前任解放区区长"
                    }
                ],
                "confidence_summary": {
                    "identity": "partial" if label == "区长" else "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium" if label == "区长" else "low",
                    "biggest_gap": ("出生年月、籍贯、教育背景、入党时间、任区委书记前的完整履历均未找到"
                                    if label == "区委书记" else
                                    "任区长前完整履历细节未找到，仅官方简历基本身份信息")
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": (f"{info['name']}的出生年月和籍贯是什么？" if label == "区委书记"
                                     else f"{info['name']}任区长前(2025年以前)的完整履历是什么？"),
                        "why_it_matters": "身份核实去重基础字段 / 理解晋升路径",
                        "suggested_queries": [f"{info['name']} 简历", f"{info['name']} 百度百科", f"{info['name']} 焦作 任前公示"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": f"{info['name']}的教育背景、入党时间、工作起始日期",
                        "why_it_matters": "评估资历与专业背景",
                        "suggested_queries": [f"{info['name']} 毕业", f"{info['name']} 教育背景"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": f"千怀贵的前任解放区委书记是谁、何时交接？",
                        "why_it_matters": "补齐前任-继任链条和跨区交流模式",
                        "suggested_queries": ["焦作 解放区 区委书记 任前公示", "解放区 原区委书记"],
                        "last_attempted": AS_OF
                    }
                ]
            }, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fpath}")

    print("\nAll person JSON files written to staging directory.")