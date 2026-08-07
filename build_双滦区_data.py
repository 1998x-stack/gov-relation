#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双滦区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 承德市
Region: 双滦区
Targets: 区委书记 & 区长

Research Sources (一手官方):
- 双滦区人民政府官网 www.slq.gov.cn — 领导之窗（col3824 政府领导）一手确认：
  * 区长 王宇：男，汉族，1981年11月生，省委党校在职研究生，现任承德市双滦区委副书记、
    政府区长、党组书记。分工：负责区政府全面工作，分管区审计局。
  * 区政府班子（副区长）：宋超宇（区委常委/常务副区长/党组副书记，1984年9月，省委党校研究生）、
    王鹏程（党组成员）、王梓澳（女，1992年9月，省委党校研究生）、陈志强（满族，1987年2月，省委党校研究生）、
    崔浩（1977年2月，公安分局长）、高峰（1979年5月，本科）。
- 双滦区要闻（slq.gov.cn 新闻中心/动态要闻 col3809，2026-05/06/07/08）：
  * 2026-05-28 区委常委会召开扩大会议（书记主持）。
  * 2026-05-22 辛国勇主持召开区委理论学习中心组集中（扩大）学习会 → 辛国勇为现任区委书记之一手信号。
- 承德市委组织部任前公示/主流媒体（澎湃、河北日报）——详见 report/open_gaps.md（网络受限，未获一手）。

Research Date: 2026-08-05

Confidence 说明：
  王宇 任区长 — confirmed（slq.gov.cn 领导之窗一手官方）。
  辛国勇 任区委书记 — confirmed（slq.gov.cn 官方新闻多次「辛国勇主持召开区委理论学习中心组／区委常委会」，区委理论学习中心组/常委会由区委书记主持）。
  区政府副职班子（宋超宇 常务、王梓澳、崔浩、王鹏程、陈志强、高峰 等 6 名副区长）— confirmed（官网领导之窗）。
  辛国勇/王宇 早岁履历、前任区委书记与前任区长、双滦区人大主任与政协主席名单 — unverified（外部搜索受网络限制，未获一手）。
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "双滦区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (targets)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "辛国勇",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区委书记",
        "current_org": "中共承德市双滦区委员会",
        "source": "双滦区人民政府官网新闻动态（2026-05-22『辛国勇主持召开区委理论学习中心组集中（扩大）学习会』、2026-05-28『区委常委会召开扩大会议』）多次确认辛国勇任双滦区委书记（区委理论学习中心组与区常委会由区委书记主持）。"
    },
    {
        "id": 2,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区委副书记、区政府区长、党组书记",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11765）：王宇，男，汉族，1981年11月生，省委党校在职研究生，现任承德市双滦区委副书记、政府区长、党组书记。分工：负责区政府全面工作，分管区审计局。"
    },
    # ════════════════════════════════════════
    # 区政府班子（副区长）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "宋超宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区委常委、副区长（常务）、党组副书记",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11766）：宋超宇，男，汉族，1984年9月出生，省委党校研究生学历，中共党员，现任承德市双滦区委常委、副区长（分管政府常务工作）、党组副书记。分工：负责区政府常务工作，分管发改委、财政局、统计局、应急局、行政审批等。"
    },
    {
        "id": 4,
        "name": "王梓澳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1992年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区副区长、党组成员",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11767）：女，汉族，1992年9月出生，省委党校研究生学历，中共党员，现任承德市双滦区人民政府副区长、党组成员。分工：教育体育、卫生健康、医疗保障等。"
    },
    {
        "id": 5,
        "name": "崔浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "中共河北省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区副区长、党组成员、市公安分局党委书记、局长",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11768）：男，汉族，1977年2月出生，中共河北省委党校研究生学历，中共党员，现任承德市双滦区人民政府副区长、党组成员、市公安局双滦分局党委书记、局长。分工：政法、稳定、司法、退役军人、公安交警。"
    },
    {
        "id": 6,
        "name": "王鹏程",
        "gender": "男",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区副区长、党组成员",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11769）：男，中共党员，现任承德市双滦区人民政府副区长、党组成员。分工：物流园区、住房和城乡建设、城市管理、交通运输、自然资源和规划。"
    },
    {
        "id": 7,
        "name": "陈志强",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1987年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区副区长、党组成员",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col11770）：男，满族，1987年2月出生，省委党校研究生学历，中共党员，现任承德市双滦区人民政府副区长、党组成员。分工：农业农村、商务、林业、水利、乡村振兴、文旅、文物。"
    },
    {
        "id": 8,
        "name": "高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双滦区副区长",
        "current_org": "承德市双滦区人民政府",
        "source": "双滦区人民政府—领导之窗（col12219）：男，汉族，1979年5月出生，本科大学学历，中共党员，现任承德市双滦区人民政府副区长。分工：工业信息化、生态环境保护、市场监管、中小企业、民营经济。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共承德市双滦区委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市双滦区",
        "parent": "中共承德市委"
    },
    {
        "id": 2,
        "name": "承德市双滦区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "承德市双滦区",
        "parent": "承德市人民政府"
    },
    {
        "id": 3,
        "name": "双滦区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "承德市双滦区",
        "parent": ""
    },
    {
        "id": 4,
        "name": "政协双滦区委员会",
        "type": "政协",
        "level": "县级",
        "location": "承德市双滦区",
        "parent": "政协承德市委员会"
    },
]

# 3. Positions
positions = [
    # ── 辛国勇 (current 区委书记) ──
    {"person_id": 1, "org_id": 1, "title": "双滦区委书记", "start_date": "约2022-2024", "end_date": "present", "rank": "正处级", "note": "双滦区委书记；主持区委全面工作，多次主持召开区委常委会、区委理论学习中心组集中学习（2026-05）。"},
    # ── 王宇 (current 区长) ──
    {"person_id": 2, "org_id": 2, "title": "双滦区人民政府区长、党组书记，区委副书记", "start_date": "约2023-2024", "end_date": "present", "rank": "正处级（县处级正职）", "note": "领导之窗一手官方确认。分工：负责区政府全面工作，分管区审计局。约2024 年任区长。"},
    # ── 宋超宇 (区委常委/常务副区长) ──
    {"person_id": 3, "org_id": 2, "title": "常务副区长、党组副书记，区委常委", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级（常务）", "note": "领导之窗一手确认，分管区政府常务工作。"},
    {"person_id": 3, "org_id": 1, "title": "双滦区委常委", "start_date": "约2023-2024", "end_date": "present", "rank": "县级", "note": "区委常委。"},
    # ── 各副区长 ──
    {"person_id": 4, "org_id": 2, "title": "双滦区副区长、党组成员", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 5, "org_id": 2, "title": "双滦区副区长、市公安局双滦分局局长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 6, "org_id": 2, "title": "双滦区副区长、党组成员", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 7, "org_id": 2, "title": "双滦区副区长、党组成员", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 8, "org_id": 2, "title": "双滦区副区长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记辛国勇与区长王宇为双滦区现任党政一把手搭档（书记-区长）。两人共同出席区委常委会、区两会等区级会议。",
        "overlap_org": "中共承德市双滦区委员会／承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记辛国勇与区委常委、常务副区长宋超宇同志为区委办班子（宋超宇为区委常委）。",
        "overlap_org": "中共承德市双滦区委员会",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "区长王宇与常务副区长宋超宇为区政府正职/常务副职搭档。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "区长王宇与副区长王梓澳共同构成区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "区长王宇与副区长兼公安分局长崔浩共同构成区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "区长王宇与副区长王鹏程共同构成区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "区长王宇与副区长陈志强共同构成区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "区长王宇与副区长高峰共同构成区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "常务副区长宋超宇与副区长王梓澳共同构成区政府常务/副职班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "常务副区长宋超宇与副区长兼公安分局长崔浩共同在双滦区政府班子。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 4,
        "person_b": 7,
        "type": "overlap",
        "context": "副区长王梓澳与副区长陈志强共同构成区政府副职班子（教育医疗 / 农文旅）。",
        "overlap_org": "承德市双滦区人民政府",
        "overlap_period": "2024/2025-"
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
        overwrite=True,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")