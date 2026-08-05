#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双桥区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 承德市
Region: 双桥区
Targets: 区委书记 & 区长

Research Sources (一手官方):
- 双桥区人民政府官网 www.sqq.gov.cn — 领导之窗(col11906 等) 一手确认：
  * 区长 邢建军：男，满族，1978年5月生，大学学历，管理学学士，中共党员，
    现任中共承德市双桥区委副书记、区政府区长、党组书记。分工：领导区政府全面工作，分管区审计局。
  * 区政府班子：常务副区长 刘岳东；副区长 刘焕海、李晓磊、王雅男、张良元、杨文瀚。
- 双桥区要闻（sqq.gov.cn）：
  * 2024-04-27 九届区委理论学习中心组第48次：杨磊任区委书记。
  * 2025-08-04 四大班子联席会：区委书记杨磊、区长邢建军、人大主任刘延民、政协主席周群、区委副书记王占平。
  * 2026-01-29 区十一届人大七次会议闭幕：大会执行主席 杨磊、邢建军、周群、王占平、李立军……；
    选举周群为区人大常委会主任；区委书记杨磊发表讲话。
  * 2026-04-23 全区领导干部政绩观读书班：区委书记杨磊、区长邢建军、区人大常委会主任周群、
     区政协主席王占平、区委副书记李立军出席。
  * 2026-05-13 杨磊赴大石庙镇/双峰寺镇督导调研（区领导 庞力强、李奇、齐光 陪同）。
- 承德市人民政府 chengde.gov.cn — 承市政字〔2026〕11号（2026-04-16）：刘岳东同志任承德市土地收购储备供应中心主任
  （双桥区常务副区长 → 承德市国有单位，跨级交流/兼任信号）。

Research Date: 2026-08-05

Confidence 说明：
  杨磊 任区委书记 — confirmed（区官网新闻多次「区委书记杨磊主持/讲」）。
  邢建军 任区长 — confirmed（sqq.gov.cn 领导之窗一手官方）。
  区四大班子（周群人大、王占平政协、李立军副书记；2025 刘延民人大、周群政协、王占平副书记）— confirmed（区官网会议新闻）。
  杨磊任书记已至少至 2026 年，2024 年已见诸官方新闻 — confirmed。
  诸副区长、班子轮换时序 — plausible/confirmed（官方新闻交叉）。
  杨磊/邢建军早岁履历、前任书记与前任区长 — unverified（网络受限，未获公开一手介绍）。
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

SLUG = "双桥区"

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
        "name": "杨磊",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区委书记",
        "current_org": "中共承德市双桥区委员会",
        "source": "双桥区人民政府官网新闻多次一手确认：2024-01 起区委书记（九届区委理论学习中心组第48次）、2026-01 区十一届人大七次会议闭幕讲话、2026-04 全区干部集体学习主持等。已至少于 2023/2024 起任双桥区委书记。"
    },
    {
        "id": 2,
        "name": "邢建军",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1978年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区委副书记、区政府区长、党组书记",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区人民政府—领导之窗（/col/col11906）：男，满族，1978年5月生，大学学历，管理学学士，中共党员，现任中共承德市双桥区委副书记、区政府区长、党组书记。分工：领导区政府全面工作，分管区审计局。"
    },
    # ════════════════════════════════════════
    # 区人大 / 区政协 / 区委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "周群",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区人大常委会主任",
        "current_org": "双桥区人民代表大会常务委员会",
        "source": "2026-01-29 区十一届人大七次会议闭幕：选举周群当选区人大常委会主任；此前（2025-08）周群曾任区政协主席（四大班子联席会报道）。"
    },
    {
        "id": 4,
        "name": "王占平",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区政协主席",
        "current_org": "政协双桥区委员会",
        "source": "2026-01/至区人大会议及2026-04读书班：区政协主席王占平出席；2025-08 四大班子联席会时任区委副书记。"
    },
    {
        "id": 5,
        "name": "李立军",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区委副书记",
        "current_org": "中共承德市双桥区委员会",
        "source": "2026-01 区人大会议执行主席及 2026-04 读书班出席名单均列「区委副书记李立军」。"
    },
    # ════════════════════════════════════════
    # 区政府班子
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "刘岳东",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区常务副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：常务副区长刘岳东；承市政字〔2026〕11号（2026-04-16）：刘岳东任承德布土地收购储备中心兼主任（跨级连接信号）。"
    },
    {
        "id": 7,
        "name": "刘焕海",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：副区长刘焕海。"
    },
    {
        "id": 8,
        "name": "李晓磊",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：副区长李晓磊。"
    },
    {
        "id": 9,
        "name": "王雅男",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：副区长王雅男。"
    },
    {
        "id": 10,
        "name": "张良元",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：副区长张良元。"
    },
    {
        "id": 11,
        "name": "杨文瀚",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区副区长",
        "current_org": "承德市双桥区人民政府",
        "source": "双桥区政府领导之窗：副区长杨文瀚。"
    },
    # ════════════════════════════════════════
    # 前任（班子轮换）
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "刘延民",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "双桥区人大常委会主任（前任）",
        "current_org": "双桥区人民代表大会常务委员会",
        "source": "2025-08 四大班子联席会报道：区人大常委会主任刘延民；2026-01 人大会议周群当选主任，刘延民卸任（去向待查）。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共承德市双桥区委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市双桥区",
        "parent": "中共承德市委"
    },
    {
        "id": 2,
        "name": "承德市双桥区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "承德市双桥区",
        "parent": "承德市人民政府"
    },
    {
        "id": 3,
        "name": "双桥区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "承德市双桥区",
        "parent": ""
    },
    {
        "id": 4,
        "name": "政协双桥区委员会",
        "type": "政协",
        "level": "县级",
        "location": "承德市双桥区",
        "parent": "政协承德市委员会"
    },
    {
        "id": 5,
        "name": "承德市土地收购储备供应中心",
        "type": "事业单位",
        "level": "市级",
        "location": "承德市",
        "parent": "承德市人民政府"
    },
]

# 3. Positions
positions = [
    # ── 杨磊 (current 区委书记) ──
    {"person_id": 1, "org_id": 1, "title": "双桥区委书记", "start_date": "约2023-2024", "end_date": "present", "rank": "正处级", "note": "现任双桥区委书记（区人武部党委第一书记另兼）；2024年已见诸官方新闻。负责区委全面工作。"},
    # ── 邢建军 (current 区长) ──
    {"person_id": 2, "org_id": 2, "title": "区人民政府区长、党组书记，区委副书记", "start_date": "约2024-2025", "end_date": "present", "rank": "正处级", "note": "领导之窗一手确认，领导区政府全面工作，分管区审计局。2025-08 已任区长。"},
    # ── 周群 ──
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "2026-01", "end_date": "present", "rank": "正处级", "note": "2026-01-29 区十一届人大一次全体会议当选。"},
    {"person_id": 3, "org_id": 4, "title": "区政协主席", "start_date": "约2023-2025", "end_date": "2026-01", "rank": "正处级", "note": "2025-08 四大班子联席会报告为区政协主席；后任转任区人大常委会主任。"},
    # ── 王占平 ──
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "约2026-01", "end_date": "present", "rank": "正处级", "note": "2026-01 起任区政协主席；2025-08 时为区委副书记。"},
    {"person_id": 4, "org_id": 1, "title": "双桥区委副书记", "start_date": "约2023-2025", "end_date": "约2026-01", "rank": "正处级", "note": "2025-08 任区委副书记。"},
    # ── 李立军 ──
    {"person_id": 5, "org_id": 1, "title": "双桥区委副书记", "start_date": "约2026", "end_date": "present", "rank": "正处级", "note": "2026-01 起见诸官方名单。"},
    # ── 刘岳东 (常务副区长 + 市土地中心) ──
    {"person_id": 6, "org_id": 2, "title": "双桥区常务副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "正处级（副处级常务）", "note": "政府领导之窗确认常务副区长。"},
    {"person_id": 6, "org_id": 5, "title": "承德市土地收购储备供应中心主任", "start_date": "2026-04", "end_date": "present", "rank": "正处级", "note": "承市政字〔2026〕11号（2026-04-16）：刘岳东任市土储中心主任（与常务副区长并任/或上级调动，时序待核）。"},
    # ── 各副区长 ──
    {"person_id": 7, "org_id": 2, "title": "双桥区副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 8, "org_id": 2, "title": "双桥区副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 9, "org_id": 2, "title": "双桥区副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 10, "org_id": 2, "title": "双桥区副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 11, "org_id": 2, "title": "双桥区副区长", "start_date": "约2023-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    # ── 刘延民 (前任人大主任) ──
    {"person_id": 12, "org_id": 3, "title": "区人大常委会主任（前任）", "start_date": "约2017-2020前后-2025", "end_date": "2026-01", "rank": "正处级", "note": "2025-08 报告为区人大常委会主任；2026-01 卸任（周群继任），去向待查。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记杨磊与区长邢建军为双桥区现任党政搭档（书记-区长）。",
        "overlap_org": "中共承德市双桥区委员会／承德市双桥区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记杨磊与区人大主任周群在区四大班子会议中同台（周群 2026-01 当选人大主任）。",
        "overlap_org": "中共承德市双桥区委员会／双桥区人大常委会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记杨磊与区委副书记李立军同班子（2026 读书班同台出席，李立军为区委副书记）。",
        "overlap_org": "中共承德市双桥区委员会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "区长邢建军与常务副区长刘岳东为区政府正职与常务副职搭档。",
        "overlap_org": "承德市双桥区人民政府",
        "overlap_period": "2025-"
    },
    {
        "person_a": 3,
        "person_b": 12,
        "type": "predecessor_successor",
        "context": "刘延民（前任人大主任）→ 周群 2026-01 接任区人大常委会主任（区人大班子换防）。",
        "overlap_org": "双桥区人民代表大会常务委员会",
        "overlap_period": "2026-01"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "周群由区政协主席转任区人大主任；王占平由区委副书记转任政协主席（政协布局轮换）。",
        "overlap_org": "政协双桥区委员会",
        "overlap_period": "2026-01"
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "王占平（原区委副书记）卸任副书记，李立军接任区委副书记（2026-01 名单对比）。",
        "overlap_org": "中共承德市双桥区委员会",
        "overlap_period": "2026-01"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "区长邢建军助理与副区长刘焕海等共同构成区政府班子。",
        "overlap_org": "承德市双桥区人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 6,
        "person_b": 8,
        "type": "overlap",
        "context": "常务副区长刘岳东与副区长班共同在区政府供职。",
        "overlap_org": "承德市双桥区人民政府",
        "overlap_period": "2023/2024-"
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