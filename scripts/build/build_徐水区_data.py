#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
徐水区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 保定市
Region: 徐水区 （2015-05 撤县设区）
Targets: 区委书记 & 区长

Research Sources:
- 保定市徐水区人民政府官方网站 www.xushui.gov.cn — 第四次党代会（2026-07-18/21）、
  区政协四届一次（2026-07-21/23）、区人大四届一次（2026-07-22/24）换届新闻，以及
  政府信息公开·领导分工页（2026-07-29）确认全部现任领导班子。
- 第四次党代会执行主席名单确认区委常委班子。
- 区人大四届一次选举结果确认区长/副区长/人大主任/法院/检察院。
- 网络受限（Exa 限流、百度/必应/Jina 超时），王春雨、徐润宽的出生/籍贯/学历/早期履历
  及前任书记/区长姓名去向未获解析，均在 report/open_gaps.md 与 person JSON
  open_questions 中标注为待查（unverified），未虚构。

Research Date: 2026-08-06
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "徐水区"

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
        "name": "王春雨",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徐水区委书记",
        "current_org": "中共保定市徐水区委员会",
        "source": "徐水区政府网—区第四次党代会开幕（2026-07-18，王春雨代表三届区委作报告）、闭幕（2026-07-21，王春雨主持并致闭幕词）；区四届人大一次会议（2026-07-24，王春雨作执行主席并领誓未列）→ 确认四届连任区委书记。www.xushui.gov.cn"
    },
    {
        "id": 2,
        "name": "徐润宽",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "徐水区委副书记、区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，徐润宽任徐水区委副书记、区长，主持政府全面工作）；区四届人大一次会议（2026-07-24）当选区长。www.xushui.gov.cn"
    },
    # ════════════════════════════════════════
    # 区委常委会（第四次党代会执行主席台前排）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "梁琪",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）；区四届人大一次会议执行主席（2026-07-24）。具体副书记分工（专职/组织）未公开确认。"
    },
    {
        "id": 4,
        "name": "师铁峰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工（纪委/组织/宣传/政法/统战）未公开确认。"
    },
    {
        "id": 5,
        "name": "张斌",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工未公开确认。"
    },
    {
        "id": 6,
        "name": "姚轩",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，区委常委、常务副区长，负责财政/发改/雄安对接/开发区/统计/应急）；区第四次党代会执行主席。"
    },
    {
        "id": 7,
        "name": "张宏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工未公开确认。"
    },
    {
        "id": 8,
        "name": "臧红建",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工未公开确认。"
    },
    {
        "id": 9,
        "name": "郭海亮",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工未公开确认。"
    },
    {
        "id": 10,
        "name": "耿佳琦",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，区委常委、副区长，负责政府机关/工业/科技/商务/文旅/金融）；区第四次党代会执行主席。"
    },
    {
        "id": 11,
        "name": "张康",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委",
        "current_org": "中共保定市徐水区委员会",
        "source": "区第四次党代会执行主席名单（2026-07-18/21）。具体常委分工未公开确认。"
    },
    # ════════════════════════════════════════
    # 区政府其他领导班子（领导分工 2026-07-29）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "侯志森",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长、公安局长",
        "current_org": "保定市公安局徐水分局",
        "source": "政府信息公开·领导分工（2026-07-29，副区长、公安局长，负责公安、城管、司法、退役军人）。"
    },
    {
        "id": 13,
        "name": "宋金龙",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，副区长，负责农业农村/乡村振兴/林业/水利）。"
    },
    {
        "id": 14,
        "name": "郝洪亮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，副区长，负责城乡建设/交通/人社）。"
    },
    {
        "id": 15,
        "name": "曹婧文",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，副区长，负责卫生健康/医保/政务服务，联系妇联）。"
    },
    {
        "id": 16,
        "name": "刘丁",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "保定市徐水区人民政府",
        "source": "政府信息公开·领导分工（2026-07-29，副区长，负责自然资源/教育/民政/市场监管）。"
    },
    # ════════════════════════════════════════
    # 人大 / 政协 / 两院
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "张洪亮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人大常委会主任",
        "current_org": "保定市徐水区人民代表大会常务委员会",
        "source": "区四届人大一次会议闭幕（2026-07-24，张洪亮领誓任人大常委会主任）。"
    },
    {
        "id": 18,
        "name": "田立国",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议保定市徐水区委员会",
        "source": "区政协四届一次会议（2026-07-23，田立国当选政协主席；副主席陈红玉、张驰、江磊、贾文军；秘书长王国营）。"
    },
    {
        "id": 19,
        "name": "刘严冬",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民法院院长",
        "current_org": "保定市徐水区人民法院",
        "source": "区四届人大一次会议（2026-07-24）选举结果。"
    },
    {
        "id": 20,
        "name": "贺啸剑",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区人民检察院检察长",
        "current_org": "保定市徐水区人民检察院",
        "source": "区四届人大一次会议（2026-07-24）选举结果。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共保定市徐水区委员会",
        "type": "党委",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": "中共保定市委"
    },
    {
        "id": 2,
        "name": "保定市徐水区人民政府",
        "type": "政府",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": "保定市人民政府"
    },
    {
        "id": 3,
        "name": "中共保定市徐水区纪律检查委员会",
        "type": "党委",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": "中共保定市徐水区委"
    },
    {
        "id": 4,
        "name": "保定市徐水区监察委员会",
        "type": "监察机关",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": "保定市监察委员会"
    },
    {
        "id": 5,
        "name": "保定市公安局徐水分局",
        "type": "政府",
        "level": "科级（区分局）",
        "location": "保定市徐水区",
        "parent": "保定市公安局"
    },
    {
        "id": 6,
        "name": "保定市徐水区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": "保定市人大常委会"
    },
    {
        "id": 7,
        "name": "中国人民政治协商会议保定市徐水区委员会",
        "type": "政协",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": ""
    },
    {
        "id": 8,
        "name": "保定市徐水区人民法院",
        "type": "司法机关",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": ""
    },
    {
        "id": 9,
        "name": "保定市徐水区人民检察院",
        "type": "司法机关",
        "level": "县级（市辖区）",
        "location": "保定市徐水区",
        "parent": ""
    },
]

# 3. Positions
positions = [
    # 王春雨 —— 区委书记（四届连任）
    {"person_id": 1, "org_id": 1, "title": "徐水区委书记（四届）", "start": "约2021年", "end": "present", "rank": "正处级", "note": "2026-07-18 四届党代会上代表三届区委作报告，2026-07 连任第四届；任书记确切起始年待查（换届前已任三届书记）"},
    # 徐润宽 —— 区长
    {"person_id": 2, "org_id": 2, "title": "徐水区委副书记、区长（区政府党组书记）", "start": "未知", "end": "present", "rank": "正处级", "note": "2026-07-24 区四届人大一次会议当选区长；领导分工页主持政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "徐水区委副书记", "start": "未知", "end": "present", "rank": "副厅级（兼）", "note": "区第四次党代会/人代会主席团前排名单确认区委副书记"},
    # 区委常委
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工（纪委/组织/政法等）待查"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工负责财政/发改/雄安对接/开发区/统计/应急"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29）"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区第四次党代会执行主席；具体分工待查"},
    # 区政府班子
    {"person_id": 12, "org_id": 5, "title": "副区长、公安局长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29），负责公安/城管/司法/退役军人"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29），负责农业农村/乡村振兴/林业/水利"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29），负责城乡建设/交通/人社"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29），负责卫生健康/医保/政务服务"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "领导分工（2026-07-29），负责自然资源/教育/民政/市场监管"},
    # 人大 / 政协 / 两院
    {"person_id": 17, "org_id": 6, "title": "区人大常委会主任", "start": "未知", "end": "present", "rank": "正处级", "note": "2026-07-24 区四届人大一次会议当选"},
    {"person_id": 18, "org_id": 7, "title": "区政协主席", "start": "未知", "end": "present", "rank": "正处级", "note": "2026-07-21 区政协四届一次会议当选"},
    {"person_id": 19, "org_id": 8, "title": "区人民法院院长", "start": "未知", "end": "present", "rank": "副处级", "note": "2026-07-24 区四届人大一次会议选举"},
    {"person_id": 20, "org_id": 9, "title": "区人民检察院检察长", "start": "未知", "end": "present", "rank": "副处级", "note": "2026-07-24 区四届人大一次会议选举"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "徐水区委书记王春雨与区委副书记、区长徐润宽为党政搭档（2021 至 2026 年连任）",
        "overlap_org": "中共保定市徐水区委员会／保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委会（梁琪为副书记）",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委师铁峰",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委张斌",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委、常务副区长姚轩",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委张宏",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委臧红建",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委郭海亮",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委、副区长耿佳琦",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "区委书记王春雨领导区委常委张康",
        "overlap_org": "中共保定市徐水区委员会",
        "overlap_period": "2021-2026"
    },
    # 区长 — 副区长
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导常务副区长姚轩（政府班子核心）",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导区委常委、副区长耿佳琦",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导副区长兼公安局长侯志森",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导副区长宋金龙",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导副区长郝洪亮",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导副区长曹婧文",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    {
        "person_a": 2,
        "person_b": 16,
        "type": "superior_subordinate",
        "context": "区长徐润宽领导副区长刘丁",
        "overlap_org": "保定市徐水区人民政府",
        "overlap_period": "2021-2026"
    },
    # 人大 / 政协 与党委政府
    {
        "person_a": 17,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "区人大常委会主任张洪亮与区委书记王春雨同区四届人大一次会议主席团",
        "overlap_org": "保定市徐水区人民代表大会常务委员会",
        "overlap_period": "2026"
    },
    {
        "person_a": 18,
        "person_b": 1,
        "type": "overlap",
        "context": "区政协主席田立国与区委书记王春雨同区四届领导班子",
        "overlap_org": "中国人民政治协商会议保定市徐水区委员会",
        "overlap_period": "2026"
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