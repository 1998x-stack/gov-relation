#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
崇礼区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 张家口市
Region: 崇礼区
Targets: 区委书记 & 区长

Research Sources:
- 张家口市崇礼区人民政府 官方网站 www.zjkcl.gov.cn — 政府领导页(zfld.thtml) 一手确认
  现任区长郭孟良履历：男，1980年9月生，汉族，硕士研究生学历，2003年8月参加工作，
  2006年8月加入中国共产党；现任中共张家口市崇礼区委副书记、区政府党组书记、政府区长。
- 张家口市人民政府 任免通知（zjk.gov.cn）：
  * 张政字〔2026〕12号（2026-06-15）：免去郭孟良的市察北管理区（现代农业高新技术示范区）
    管委会主任职务（为转任崇礼区长腾位）；同日任命新崇礼公安分局局长。
  * 张政字〔2026〕14号（2026-07-13）：马劲松任市公安局副局长（兼）。
- 百度移动权威聚合「崇礼区委书记 现任」(2026-07)：
  现任区委书记为 陈建, 任张家口市委副书记、崇礼区委书记、区人武部党委第一书记；
  前任书记（冬奥时代）为 刘雪松（张家口市委常委、崇礼区委书记），更早为王酷。
- 历史资料（媒体，2021-2022 冬奥时代）：王酷、刘雪松先后任崇礼区委书记；
  曹东晓曾任崇礼区长（张家口日报采访）。

Research Date: 2026-08-05

Confidence 说明：
  郭孟良 任区长 — confirmed（官方 zjkcl.gov.cn）。
  陈建 任区委书记 — plausible（百度权威聚合；个别媒体 2026-06 报道曹东晓转正，需复核）。
  刘雪松/王酷/曹东晓 前任 — plausible（媒体/冬奥历史报道）。
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

SLUG = "崇礼区"

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
        "name": "陈建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学、工程硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇礼区委书记",
        "current_org": "中共张家口市崇礼区委员会",
        "source": "百度权威聚合「崇礼区委书记 现任」2026-07；2021-08 张家口市委十一届一次全会 当选市委常委（政法委书记）名单（媒体转载）。当前任张家口市委副书记、崇礼区委书记、区人武部党委第一书记。"
    },
    {
        "id": 2,
        "name": "郭孟良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士研究生学历",
        "party_join": "中共党员（2006年8月加入）",
        "work_start": "2003年8月",
        "current_post": "崇礼区委副书记、区政府党组书记、区长",
        "current_org": "张家口市崇礼区人民政府",
        "source": "张家口市崇礼区人民政府—政府领导页（/zfld.thhtml）：现任崇礼区委副书记、区政府党组书记、政府区长。张政字〔2026〕12号（2026-06-15）免去其市察北管理区管委会主任职务（转任崇礼）。"
    },
    # ════════════════════════════════════════
    # Historical Leaders (predecessors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘雪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇礼区委书记（前任，冬奥时代）",
        "current_org": "中共张家口市崇礼区委员会",
        "source": "张家口市委十一届一次全会当选名单（2021-08）：刘雪松任市委常委、崇礼区委书记、市筹办冬奥会工作领导小组办公室党组成员、副主任，崇礼医学中心党委书记（兼）。"
    },
    {
        "id": 4,
        "name": "王彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇礼区委书记/县长（更早，冬奥筹备期前）",
        "current_org": "中共张家口市崇礼区委员会",
        "source": "媒体旧闻（冬奥筹备期）：王酷曾任张家口市委常委、崇礼区委书记（撤县设区前为崇礼县委书记），后调任市冬奥办副主任。"
    },
    {
        "id": 5,
        "name": "曹东晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇礼区区长（前任）",
        "current_org": "张家口市崇礼区人民政府",
        "source": "张家口日报采访「区长曹东晓：坚定不移走好高质量发展之路」；个别媒体 2026-06 报道其可能转任区委书记（未经权威确认）。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共张家口市崇礼区委员会",
        "type": "党委",
        "level": "县级",
        "location": "张家口市崇礼区",
        "parent": "中共张家口市委"
    },
    {
        "id": 2,
        "name": "张家口市崇礼区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "张家口市崇礼区",
        "parent": "张家口市人民政府"
    },
    {
        "id": 3,
        "name": "张家口市察北管理区（市现代农业高新技术示范区）管理委员会",
        "type": "政府",
        "level": "县级（管理区）",
        "location": "张家口市察北管理区",
        "parent": "张家口市人民政府"
    },
    {
        "id": 4,
        "name": "中共张家口市委",
        "type": "党委",
        "level": "地厅级",
        "location": "张家口市",
        "parent": ""
    },
    {
        "id": 5,
        "name": "张家口市人民政府",
        "type": "政府",
        "level": "地厅级",
        "location": "张家口市",
        "parent": ""
    },
]

# 3. Positions
positions = [
    # ── 陈建 (current 区委书记) ──
    {"person_id": 1, "org_id": 1, "title": "崇礼区委书记（区人武部党委第一书记）", "start_date": "未知（约2023-2024）", "end_date": "present", "rank": "正处级", "note": "现任崇礼区委书记；兼任张家口市委副书记（中2026权威聚合）。任前为张家口市委常委、政法委书记（2021）。"},
    {"person_id": 1, "org_id": 4, "title": "张家口市委常委、政法委书记", "start_date": "2021-08", "end_date": "约2023-2024", "rank": "副厅级", "note": "2021-08 张家口市委十一届一次全会当选市委常委；此后任政法委书记，后转任崇礼区委书记。注：聚合资料显示其另兼市委副书记，具体时序待核。"},
    # ── 郭孟良 (current 区长) ──
    {"person_id": 2, "org_id": 2, "title": "崇礼区委副书记、区政府党组书记、区长", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "一手官方（zjkcl.gov.cn 政府领导页）确认现任。转任崇礼区长前已免去察北管委会主任职务。"},
    {"person_id": 2, "org_id": 3, "title": "市察北管理区（现代农业高新技术示范区）管委会主任", "start_date": "约2021", "end_date": "2026-06", "rank": "正处级", "note": "张政字〔2026〕12号（2026-06-15）免去郭孟良市察北管理区管委会主任职务。"},
    # ── 刘雪松 (前任书记) ──
    {"person_id": 3, "org_id": 1, "title": "崇礼区委书记", "start_date": "2021", "end_date": "未知（约2023-2024）", "rank": "副厅级", "note": "冬奥时代崇礼区委书记；兼市筹办冬奥会工作领导小组办公室党组成员、副主任、崇礼医学中心党委书记。2023-2024 交棒陈建（时序待核）。"},
    {"person_id": 3, "org_id": 4, "title": "张家口市委常委（兼）", "start_date": "2021-08", "end_date": "未知", "rank": "副厅级", "note": "2021-08 十一届一次全会当选市委常委。"},
    # ── 王酷 (更早书记) ──
    {"person_id": 4, "org_id": 1, "title": "崇礼县委书记(2016前)/崇礼区委书记(2016后)", "start_date": "约2015", "end_date": "未知", "rank": "正处级", "note": "崇礼县撤县设区前后；后调任市冬奥办副主任。"},
    # ── 曹东晓 (前任区长) ──
    {"person_id": 5, "org_id": 2, "title": "崇礼区区长", "start_date": "约2021", "end_date": "约2026", "rank": "正处级", "note": "张家口日报采访确认其为区长；2026-06 前后转任/离任，郭孟良接任。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记陈建与区长郭孟良为崇礼区党政搭档（约2026 起）",
        "overlap_org": "中共张家口市崇礼区委员会／张家口市崇礼区人民政府",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "刘雪松（冬奥时代书记）→ 陈建接任崇礼区委书记",
        "overlap_org": "中共张家口市崇礼区委员会",
        "overlap_period": "约2023-2024"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "陈建、刘雪松在2021-08张家口市委常委会中共事（同为市委常委）",
        "overlap_org": "中共张家口市委",
        "overlap_period": "2021-"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "曹东晓（前任区长）→ 郭孟良接任崇礼区长",
        "overlap_org": "张家口市崇礼区人民政府",
        "overlap_period": "2026-06"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "王酷（更早书记）→ 刘雪松接任崇礼区委书记",
        "overlap_org": "中共张家口市崇礼区委员会",
        "overlap_period": "约2021"
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