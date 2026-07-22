#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
江城区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 阳江市
Region: 江城区
Targets: 区委书记 & 区长

Research Sources:
- 阳江市江城区人民政府门户网站 (www.jiangcheng.gov.cn) — 领导之窗 官方信息
- 官方领导分工页面 (ldzc/ 栏目)

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "江城区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李仕鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委书记",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — 区委书记 ldzc/qw/content/post_557280.html"
    },
    {
        "id": 2,
        "name": "吴伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委副书记、区政府区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — 区长 ldzc/qzf/content/post_866103.html"
    },
    # ════════════════════════════════════════
    # Deputy Party Secretaries
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘粉英",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委副书记",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_890081.html"
    },
    {
        "id": 4,
        "name": "谢明华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委副书记（挂任）",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_764007.html"
    },
    # ════════════════════════════════════════
    # Party Standing Committee (区委常委)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "许开健",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、政法委书记",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_570512.html"
    },
    {
        "id": 6,
        "name": "赵晨",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_833727.html"
    },
    {
        "id": 7,
        "name": "莫卓姬",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、常务副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_783231.html"
    },
    {
        "id": 8,
        "name": "李学敏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、组织部部长",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_764010.html"
    },
    {
        "id": 9,
        "name": "洪铭章",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、区委办主任、统战部部长",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_928190.html"
    },
    {
        "id": 10,
        "name": "姚庆严",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、宣传部部长",
        "current_org": "中共阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_890100.html"
    },
    {
        "id": 11,
        "name": "王文斌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、区人武部政委",
        "current_org": "阳江市江城区人民武装部",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_823724.html"
    },
    {
        "id": 12,
        "name": "李国灿",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区委常委、纪委书记、监委主任",
        "current_org": "中共阳江市江城区纪律检查委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qw/content/post_889982.html"
    },
    # ════════════════════════════════════════
    # Deputy District Mayors (副区长)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "余旭斌",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzf/content/post_683086.html"
    },
    {
        "id": 14,
        "name": "杨乐",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzf/content/post_869037.html"
    },
    {
        "id": 15,
        "name": "曾练豪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzf/content/post_762213.html"
    },
    {
        "id": 16,
        "name": "刘文海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzf/content/post_881110.html"
    },
    {
        "id": 17,
        "name": "敖道策",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区副区长",
        "current_org": "阳江市江城区人民政府",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzf/content/post_920429.html"
    },
    # ════════════════════════════════════════
    #人大 (People's Congress)
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "刘运辉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区人大常委会主任",
        "current_org": "阳江市江城区人民代表大会常务委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qrd/content/post_558052.html"
    },
    # ════════════════════════════════════════
    # 政协 (Political Consultative)
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "陈章朋",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江城区政协党组书记、主席",
        "current_org": "中国人民政治协商会议阳江市江城区委员会",
        "source": "www.jiangcheng.gov.cn 领导之窗 — ldzc/qzx/content/post_768628.html"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共阳江市江城区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
    {
        "id": 2,
        "name": "阳江市江城区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
    {
        "id": 3,
        "name": "中共阳江市江城区纪律检查委员会",
        "type": "纪律检查",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
    {
        "id": 4,
        "name": "阳江市江城区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议阳江市江城区委员会",
        "type": "政协",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
    {
        "id": 6,
        "name": "阳江市江城区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "location": "广东省阳江市江城区",
    },
]

# 3. Positions
positions = [
    # 李仕鹏 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "江城区委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 吴伟 — 区长
    {"person_id": 2, "org_id": 1, "title": "江城区委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "江城区政府党组书记、区长", "start": "待查", "end": "present", "rank": "正处级", "note": "主持区政府全面工作，负责审计工作"},
    # 刘粉英 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "江城区委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "协助区委书记抓党的建设、社会建设、三农、乡村振兴、群团工作"},
    # 谢明华 — 挂任副书记
    {"person_id": 4, "org_id": 1, "title": "江城区委副书记（挂任）", "start": "待查", "end": "present", "rank": "副处级", "note": "对口帮扶协作驻江城区工作队队长，负责珠海对口帮扶江城区工作"},
    # 许开健 — 政法委书记
    {"person_id": 5, "org_id": 1, "title": "江城区委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "负责政法、维稳、社会治理工作"},
    # 赵晨 — 副区长
    {"person_id": 6, "org_id": 1, "title": "江城区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责科技、工业、商务、市监等工作"},
    # 莫卓姬 — 常务副区长
    {"person_id": 7, "org_id": 1, "title": "江城区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "江城区常务副区长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责区政府常务工作，发改、财政、应急、国资等工作"},
    # 李学敏 — 组织部长
    {"person_id": 8, "org_id": 1, "title": "江城区委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责组织、基层党建、干部、人才、党校工作"},
    # 洪铭章 — 区委办主任兼统战部长
    {"person_id": 9, "org_id": 1, "title": "江城区委常委、区委办主任、统战部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责统战、民族宗教、侨务、区委办工作"},
    # 姚庆严 — 宣传部长
    {"person_id": 10, "org_id": 1, "title": "江城区委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "负责宣传思想、文化、意识形态、网信工作"},
    # 王文斌 — 人武部政委
    {"person_id": 11, "org_id": 6, "title": "江城区人武部政委", "start": "待查", "end": "present", "rank": "上校", "note": "区委常委，负责武装、国防后备力量建设"},
    {"person_id": 11, "org_id": 1, "title": "江城区委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 李国灿 — 纪委书记
    {"person_id": 12, "org_id": 1, "title": "江城区委常委、纪委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "负责纪检监察、党风廉政建设、巡察和反腐败工作"},
    {"person_id": 12, "org_id": 3, "title": "江城区监委主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 副区长们
    {"person_id": 13, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "江城区副区长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 18, "org_id": 4, "title": "江城区人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 5, "title": "江城区政协党组书记、主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 李仕鹏 ↔ 吴伟 (党政一把手)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "党政一把手搭班：李仕鹏任区委书记，吴伟任区长兼区委副书记",
        "overlap_org": "中共阳江市江城区委员会",
        "overlap_period": "present",
    },
    # 李仕鹏 ↔ 刘粉英
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "书记与专职副书记搭班",
        "overlap_org": "中共阳江市江城区委员会",
        "overlap_period": "present",
    },
    # 吴伟 ↔ 莫卓姬 (区长与常务副区长)
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与常务副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    # 莫卓姬 ↔ 赵晨 (常务副区长与副区长)
    {
        "person_a": 7, "person_b": 6,
        "type": "overlap",
        "context": "区政府领导搭班：常务副区长与副区长",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    # 李学敏 ↔ 洪铭章 (组织与统战 - 常委间协作)
    {
        "person_a": 8, "person_b": 9,
        "type": "overlap",
        "context": "区委常委班子成员：组织部长与统战部长",
        "overlap_org": "中共阳江市江城区委员会",
        "overlap_period": "present",
    },
    # 李仕鹏 ↔ 李国灿 (书记与纪委书记)
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "区委书记与纪委书记：党委主体责任与纪委监督责任",
        "overlap_org": "中共阳江市江城区委员会",
        "overlap_period": "present",
    },
    # 姚庆严 ↔ 许开健 (宣传与政法)
    {
        "person_a": 10, "person_b": 5,
        "type": "overlap",
        "context": "区委常委班子成员：宣传部长与政法委书记",
        "overlap_org": "中共阳江市江城区委员会",
        "overlap_period": "present",
    },
    # 吴伟 ↔ 副区长们
    {
        "person_a": 2, "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 15,
        "type": "superior_subordinate",
        "context": "区长与副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 16,
        "type": "superior_subordinate",
        "context": "区长与副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 17,
        "type": "superior_subordinate",
        "context": "区长与副区长搭班",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    # 谢明华 ↔ 莫卓姬 (珠海对口帮扶协作)
    {
        "person_a": 4, "person_b": 7,
        "type": "overlap",
        "context": "挂任副书记（珠海对口帮扶工作队队长）与常务副区长（联系珠海帮扶工作）协作",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
    # 谢明华 ↔ 赵晨 (珠海对口帮扶协作)
    {
        "person_a": 4, "person_b": 6,
        "type": "overlap",
        "context": "挂任副书记（珠海对口帮扶工作队队长）与副区长（协助联系珠海帮扶工作）协作",
        "overlap_org": "阳江市江城区人民政府",
        "overlap_period": "present",
    },
]

# ── Build ──

def main():
    print(f"[{SLUG}] Building database: {DB_PATH}")
    print(f"[{SLUG}] Building GEXF: {GEXF_PATH}")
    print(f"[{SLUG}] Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")

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

    # Verify
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    posc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()
    print(f"[{SLUG}] Verified — DB contains {pc} persons, {oc} orgs, {posc} positions, {rc} relationships")
    print(f"[{SLUG}] DB size: {os.path.getsize(DB_PATH)} bytes")
    print(f"[{SLUG}] GEXF size: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"[{SLUG}] Done!")


if __name__ == "__main__":
    main()
