#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 湖滨区 (Hubin District), 三门峡市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_湖滨区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 湖滨区人民政府网站 (www.hubin.gov.cn): 2025-01~2026-05 县级领导接访安排公告、
    《湖滨区人民代表大会常务委员会公报》、区人大十三届八次会议报道、区人武工作会议报道
  - 湖滨区政协网 (www.hbqzxw.gov.cn): 政协十二届五次会议公告（李平当选主席并附简历）、
    政协十二届六次会议报道（卫光当选主席）
  - 袁锐锋百度百科 + 义马市百度百科（复用于管理袁锐锋完整履历，已存仓库 persons JSON）
  - 中文百科全书（乔继明人物履历）
  - 三门峡网 / 三门峡日报 (www.ismx.cn): 湖滨区委十四届十一次全会（周建文作报告）

Key findings:
  - 现任区委书记：袁锐锋（2026-01 由义马市委书记调任，2026-06-25 当选十五届区委书记）
  - 现任区长：李平（甘肃环县人，1979-10生；曾任区委副书记、政协主席；2026 年初改任区长）
  - 前任区长：乔继明（2022-04 起任区长，2025 年仍在任，后调离）
  - 前任区委书记：周建文（2025 年任区委书记，2026-01 前离任）

Confidence notes:
  - 袁锐锋：identity/current_role/career complete —— confirmed（仓库已有完整 person JSON）
  - 李平：identity confirmed（政协公告简历）、current role confirmed（2026 年 4-5 月接访名单）
     早期履历（2003 年前）未查证 —— open_questions
  - 乔继明：身份与区长任期 confirmed；去向未确认 —— plausible
  - 周建：书记任期 confirmed（十四届十一/十二次全会报道）；去向未确认 —— plausible
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "湖滨区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion via process_tmp.py --apply)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "袁锐锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "河南安阳",
        "education": "农业推广硕士（河南农业大学农学院 2002.12-2006.12）",
        "party_join": "1995-11",
        "work_start": "1997-08",
        "current_post": "区委书记",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "袁锐锋百度百科（袁锐锋兼任 2026-01 调任湖滨区委书记、2026-04 兼任区人武部党委第一书记）；湖滨区人大十三届八次会议报道（2026-04-03）确认袁锐锋为区委书记并主持全会"
    },
    {
        "id": 2,
        "name": "李平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "甘肃环县",
        "education": "大学学历",
        "party_join": "2006-06",
        "work_start": "2003-09",
        "current_post": "区委副书记、区长",
        "current_org": "湖滨区人民政府",
        "source": "湖滨区政协十二届五次会议公告（2025-03-31，附简历：李平，男，甘肃环县人，1979年10月出生，2003年9月参加工作，2006年6月加入中国共产党，大学学历，现任中共湖滨区委副书记、湖滨区政协党组书记）；2026年4月/5月湖滨区县级领导接访安排（李平·区委副书记、区长）",
    },
    {
        "id": 3,
        "name": "乔继明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原湖滨区区长（已调离）",
        "current_org": "",
        "source": "中文百科全书（乔继明为湖滨区委副书记、区长、区政府党组书记）；湖滨区人大十三届一至三次会议（2022-04 当选区长）；2025年《政府工作报告》（2025-02-28 由区长乔继明作报告）",
    },
    # ═══════ Leadership Roster (2026年4-5月接访安排等) ═══════
    {
        "id": 4,
        "name": "郭建体",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "2026年4月湖滨区县级领导接访安排（郭建体·区委副书记）",
    },
    {
        "id": 5,
        "name": "孙江涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "2026年4月湖滨区县级领导接访安排（孙江涛·区委常委、组织部部长）",
    },
    {
        "id": 6,
        "name": "焦晓君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "2026年4月湖滨区县级领导接访安排（焦晓君·区委常委、政法委书记）",
    },
    {
        "id": 7,
        "name": "蒋维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "2026年4月湖滨区县级领导接访安排（蒋维·区委常委、区委办主任）",
    },
    {
        "id": 8,
        "name": "陈静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "2026年4月湖滨区县级领导接访安排（陈静·区委常委、宣传部部长）；2025-11 区人大二十九次会议（陈静·区委常委、副区长）",
    },
    {
        "id": 9,
        "name": "王兆海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "湖滨区人民政府",
        "source": "2026年4月湖滨区县级领导接访安排（王兆海·区委常委、常务副区长）；湖滨区人大十三届八次会议（2026-04，当选副区长）",
    },
    {
        "id": 10,
        "name": "裴斐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "湖滨区人民政府",
        "source": "2026年4月/5月湖滨区县级领导接访安排（裴斐·区委常委、副区长）",
    },
    {
        "id": 11,
        "name": "李攀军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "三门峡市湖滨区纪律检查委员会",
        "source": "2026年4月湖滨区县级领导接访安排（李攀军·区委常委、纪委书记、监委主任）；湖滨区人大十三届八次会议（2026-04，当选监委主任）",
    },
    {
        "id": 12,
        "name": "李红梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "湖滨区人民政府",
        "source": "2026年4月/5月湖滨区县级领导接访安排（李红梅·副区长）；湖滨区人大十三届八次会议（当选副区长）",
    },
    {
        "id": 13,
        "name": "张俊祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "湖滨区人民政府",
        "source": "2025-11-26 区人大二十六次会议决定任命张俊祥为副区长；2026年4月/5月湖滨区县级领导接访安排",
    },
    {
        "id": 14,
        "name": "张儒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "湖滨区人民政府",
        "source": "2026年4月湖滨区县级领导接访安排（张儒·副区长）；湖滨区人大十三届八次会议（当选副区长）",
    },
    {
        "id": 15,
        "name": "韩建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "湖滨区人民政府",
        "source": "2026年4月湖滨区县级领导接访安排（韩建忠·副区长）；湖滨区人大十三届八次会议（当选副区长）",
    },
    {
        "id": 16,
        "name": "赵智平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、市公安局湖滨分局局长",
        "current_org": "三门峡市公安局湖滨分局",
        "source": "2025-11-26 区人大二十九次会议决定任命赵智平为副区长；2026年4月湖滨区县级领导接访安排（赵智平·副区长、市公安局湖滨分局局长）",
    },
    {
        "id": 17,
        "name": "付新红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "湖滨区人大常委会主任",
        "current_org": "湖滨区人大常委会",
        "source": "湖滨区十三届人大常委会第二十九次会议（付新红主持）",
    },
    {
        "id": 18,
        "name": "卫光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "湖滨区政协主席",
        "current_org": "政协三门峡市湖滨区委员会",
        "source": "湖滨区政协十二届六次会议（2026年，卫光当选政协主席）",
    },
    # ═══════ Resigned / retired leaders ═══════
    {
        "id": 19,
        "name": "周建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖滨区委书记（已卸任）",
        "current_org": "",
        "source": "湖滨区委十四届十一次全会报道（2025-12-17，区委书记周建文受区委常委会委托作报告）；2026年1月湖滨区县级领导接访安排（周建文·区委书记）",
    },
    {
        "id": 20,
        "name": "张文世",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、纪委书记（原）",
        "current_org": "三门峡市湖滨区纪律检查委员会",
        "source": "2025-11 区人大二十九次会议（张文世·区委常委、纪委书记、监委主任）",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共三门峡市湖滨区委员会", "type": "党委", "level": "县处级", "parent": "中共三门峡市委", "location": "湖滨区"},
    {"id": 2, "name": "湖滨区人民政府", "type": "政府", "level": "县处级", "parent": "三门峡市人民政府", "location": "湖滨区"},
    {"id": 3, "name": "湖滨区人大常委会", "type": "人大", "level": "县处级", "parent": "三门峡市人大常委会", "location": "湖滨区"},
    {"id": 4, "name": "政协三门峡市湖滨区委员会", "type": "政协", "level": "县处级", "parent": "三门峡市政协", "location": "湖滨区"},
    {"id": 5, "name": "三门峡市湖滨区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "三门峡市纪委监委", "location": "湖滨区"},
    {"id": 6, "name": "三门峡市公安局湖滨分局", "type": "政府", "level": "县处级", "parent": "三门峡市公安局", "location": "湖滨区"},
    {"id": 7, "name": "中共三门峡市湖滨区委员会组织部", "type": "党委", "level": "科级", "parent": "中共三门峡市湖滨区委员会", "location": "湖滨区"},
    {"id": 8, "name": "中共三门峡市湖滨区委员会宣传部", "type": "党委", "level": "科级", "parent": "中共三门峡市湖滨区委员会", "location": "湖滨区"},
    {"id": 9, "name": "中共三门峡市湖滨区委员会政法委员会", "type": "党委", "level": "科级", "parent": "中共三门峡市湖滨区委员会", "location": "湖滨区"},
    {"id": 10, "name": "中共三门峡市湖滨区委办公室", "type": "党委", "level": "科级", "parent": "中共三门峡市湖滨区委员会", "location": "湖滨区"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # ═══════ Core Leadership ═══════
    # 袁锐锋
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-01", "end_date": "present", "rank": "县处级正职", "note": "2026-01 由义马市委书记调任湖滨区委书记；2026-04 兼任区人武部党委第一书记；2026-06-25 当选十五届区委书记"},
    # 李平
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "曾兼任区政协党组书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年初改任区委副书记、区长（2026年4月接访名单确认）"},
    {"person_id": 2, "org_id": 4, "title": "政协主席（前任）", "start_date": "2025-03", "end_date": "2026", "rank": "县处级正职", "note": "2025-03-31 当选政协十二届委员会主席；2026 年改任区长后由卫光接任政协主席"},
    # 乔继明
    {"person_id": 3, "org_id": 1, "title": "区委副书记（前任）", "start_date": "2021-08", "end_date": "", "rank": "县处级副职", "note": "2021-08 当选区十四届常委、副书记"},
    {"person_id": 3, "org_id": 2, "title": "区长（前任）", "start_date": "2022-04", "end_date": "", "rank": "县处级正职", "note": "2022-04-17 当选区十三届人大一次会议区长；2025 年仍任区长，后调离"},
    # ═══════ Leadership Roster ═══════
    # 郭建体
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孙江涛
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 焦晓君
    {"person_id": 6, "org_id": 9, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 蒋维
    {"person_id": 7, "org_id": 10, "title": "区委常委、区委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈静
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "曾兼任宣传部部长（2026）；之前任区委常委、副区长（2025）"},
    # 王兆海
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-04 当选副区长"},
    # 裴斐
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李攀军
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-04 当选监委主任"},
    # 副区长们
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-04 当选"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2025-11-26 决定任命"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-04 当选"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-04 当选"},
    {"person_id": 16, "org_id": 6, "title": "市公安局湖滨分局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2025-11-26 任命为副区长"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任市公安局湖滨分局局长"},
    # 人大、政协
    {"person_id": 17, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "区政协主席", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "2026年政协十二届六次会议当选"},
    # 原任书记/纪委
    {"person_id": 19, "org_id": 1, "title": "区委书记（前任）", "start_date": "", "end_date": "2026-01", "rank": "县处级正职", "note": "2025 年任区委书记；2025-12-17 主持十四届十一次全会；2026-01 被袁锐锋接替"},
    {"person_id": 20, "org_id": 1, "title": "区委常委、纪委书记（前任）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2025 年任区委常委、纪委书记、监委主任"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "袁锐锋任区委书记、李平任区长，为当前党政正职搭档",
        "overlap_org": "湖滨区",
        "overlap_period": "2026-"
    },
    # 袁锐锋 vs 前任书记周建
    {
        "person_a": 1, "person_b": 19,
        "type": "predecessor_successor",
        "context": "周建任区委书记，后由袁锐锋接任",
        "overlap_org": "中共三门峡市湖滨区委员会",
        "overlap_period": "2026-01"
    },
    # 李平 vs 前任区长乔继明
    {
        "person_a": 2, "person_b": 3,
        "type": "predecessor_successor",
        "context": "乔继明任区长，后由李平接任区长",
        "overlap_org": "湖滨区人民政府",
        "overlap_period": "2026"
    },
    # 袁锐锋 vs 郭建体（班子）
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共三门峡市湖滨区委员会",
        "overlap_period": "2026-"
    },
    # 李平 vs 郭建体（班子）
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "李平任区委副书记、区长，郭建体任区委副书记，同为区委班子",
        "overlap_org": "中共三门峡市湖滨区委员会",
        "overlap_period": "2026-"
    },
    # 袁锐锋 vs 张文世（原纪委书记，常委会）
    {
        "person_a": 1, "person_b": 20,
        "type": "predecessor_successor",
        "context": "张文世曾任区委常委、纪委书记、监委主任；后由李攀军接任",
        "overlap_org": "三门峡市湖滨区纪律检查委员会",
        "overlap_period": "2026"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "袁锐锋",
        "job": "区委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "湖滨区",
                "job": "区委书记",
                "task_id": "henan_湖滨区",
                "time_focus": "2023-2026"
            },
            "identity": {
                "person_id": "hubei_yuan_ruifeng2",
                "name": "袁锐锋",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1975-01",
                "birthplace": "河南安阳",
                "native_place": "河南安阳",
                "education": [
                    {"period": "2002.12-2006.12", "institution": "河南农业大学农学院", "major": "农业推广", "degree": "农业推广硕士", "study_type": "part_time", "source_ids": ["S001"]}
                ],
                "party_join": "1995-11",
                "work_start": "1997-08",
                "dedupe_keys": {
                    "name_birth": "袁锐锋_1975-01",
                    "name_birthplace": "袁锐锋_河南安阳",
                    "official_profile_url": "https://baike.baidu.com/item/%E8%A2%81%E9%94%90%E9%94%8B/55883389"
                }
            },
            "current_status": {
                "current_post": "三门峡市湖滨区委书记",
                "current_org": "中共三门峡市湖滨区委员会",
                "administrative_rank": "正县级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"]
            },
            "career_timeline": [
                {"start": "1997-08", "end": "2002-12", "org": "安阳市农业局", "title": "棉办工作", "level": "科员", "location": "河南省安阳市", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2002-12", "end": "2004-03", "org": "安阳市农业局", "title": "综合信息站副站长", "level": "副科级", "location": "河南省安阳市", "system": "government", "rank": "副科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2004-03", "end": "2007-04", "org": "安阳市农业局", "title": "综合信息站站长", "level": "正科级", "location": "河南省安阳市", "system": "government", "rank": "正科级", "is_key_promotion": False, "notes": "2002.12-2006.12 在职攻读农业推广硕士", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2007-04", "end": "2009-05", "org": "安阳市农业局", "title": "综合与政策法规科科长", "level": "正科级", "location": "河南省安阳市", "system": "government", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2009-05", "end": "2011-06", "org": "滑县人民政府", "title": "党组成员、副县长", "level": "副处级", "location": "河南省安阳市滑县", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2011-06", "end": "2016-05", "org": "中共滑县委员会", "title": "县委常委、统战部部长", "level": "副处级", "location": "河南省安阳市滑县", "system": "organization", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2016-05", "end": "2016-09", "org": "中共滑县委员会", "title": "县委常委、统战部部长兼赵营乡党委书记", "level": "副处级", "location": "河南省安阳市滑县", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2016-09", "end": "2019-01", "org": "中共滑县委员会", "title": "县委常委、县委办主任", "level": "副处级", "location": "河南省安阳市滑县", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2019-01", "end": "2019-05", "org": "滑县人民政府", "title": "县委常委、常务副县长、县委办主任", "level": "副处级", "location": "河南省安阳市滑县", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2019-05", "end": "2023-06", "org": "义马市人民政府", "title": "义马市委副书记、市长", "level": "正县级", "location": "河南省三门峡市义马市", "system": "government", "rank": "正县级", "is_key_promotion": True, "notes": "跨市交流", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2023-06", "end": "2026-01", "org": "中共义马市委员会", "title": "义马市委书记", "level": "正县级", "location": "河南省三门峡市义马市", "system": "party", "rank": "正县级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2026-01", "end": "present", "org": "中共三门峡市湖滨区委员会", "title": "三门峡市湖滨区委书记", "level": "正县级", "location": "河南省三门峡市湖滨区", "system": "party", "rank": "正县级", "is_key_promotion": False, "notes": "2026-04 兼任区人武部党委第一书记；2026-06-25 当选十五届区委书记", "confidence": "confirmed", "source_ids": ["S002", "S003"]}
            ],
            "organizations": [
                {"name": "中共三门峡市湖滨区委员会", "role": "区委书记", "period": "2026-", "source_ids": ["S003"]},
                {"name": "中共义马市委员会", "role": "曾任市委书记", "period": "2023-2026", "source_ids": ["S002"]},
                {"name": "义马市人民政府", "role": "曾任市长", "period": "2019-2023", "source_ids": ["S001"]},
                {"name": "中共滑县委员会", "role": "曾任县委常委", "period": "2011-2019", "source_ids": ["S001"]},
                {"name": "滑县人民政府", "role": "曾任副县长/常务副县长", "period": "2009-2019", "source_ids": ["S001"]},
                {"name": "安阳市农业局", "role": "曾任科员至科长", "period": "1997-2009", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "李平", "person_id": "henan_hubin_liping", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "袁锐锋任区委书记，李平任区长，为当前党政正职搭档", "overlap_org": "湖滨区", "overlap_period": "2026-", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
                {"person": "周建文", "person_id": "henan_hubin_zhoujianwen", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "周建文任区委书记，袁锐锋接任", "overlap_org": "中共三门峡市湖滨区委员会", "overlap_period": "2026-01", "direction": "undirected", "confidence": "plausible", "source_ids": ["S003"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["农业管理", "地方行政管理"],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["government", "party", "organization"],
                "geographic_pattern": ["安阳", "滑县", "义马", "湖滨区"],
                "promotion_velocity": {
                    "summary": "稳定的跨县晋升路径：安阳体系（12年科级）→ 滑县（副处至常务副县长）→ 义马市长/书记（正县级）→ 湖滨区委书记",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "technocratic", "evidence": "长期农业系统出身，农业推广硕士，重视矿山治理、生态文明等专项工作", "confidence": "plausible", "source_ids": ["S001", "S003"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至 2026-08，未发现袁锐锋相关纪律处分、审计问题或负面报道", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "袁锐锋百度百科", "url": "https://baike.baidu.com/item/%E8%A2%81%E9%94%90%E9%94%8B/55883389", "publisher": "百度百科", "published_at": "2026-06-27", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "完整履历"},
                {"id": "S002", "title": "义马市百度百科", "url": "https://baike.baidu.com/item/%E4%B9%89%E9%A9%AC%E5%B8%82/6861185", "publisher": "百度百科", "published_at": "2026-07-05", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "袁锐锋曾任义马市委书记"},
                {"id": "S003", "title": "湖滨区人大十三届八次会议报道（区委书记袁锐锋）", "url": "https://www.hubin.gov.cn/25411/2026/4/2245914.html", "publisher": "湖滨区人民政府", "published_at": "2026-04-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认袁锐锋为区委书记"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "complete",
                "relationship_confidence": "high",
                "biggest_gap": "暂无重大信息缺口（履历完整）"
            },
            "open_questions": [
                {"priority": "low", "question": "袁锐锋在湖滨区任职期间的具体政绩与纳入议题", "why_it_matters": "评估治理表现", "suggested_queries": ["袁锐锋 湖滨区 调研", "袁锐锋 2026 工作要点"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "李平",
        "job": "区长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "三门峡市",
                "region": "湖滨区",
                "job": "区长",
                "task_id": "henan_湖滨区",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "henan_hubin_liping",
                "name": "李平",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1979-10",
                "birthplace": "甘肃环县",
                "native_place": "甘肃环县",
                "education": [],
                "party_join": "2006-06",
                "work_start": "2003-09",
                "dedupe_keys": {
                    "name_birth": "李平_1979-10",
                    "name_birthplace": "李平_甘肃环县",
                    "official_profile_url": "http://www.hbqzxw.gov.cn/（湖滨区政协网公告）"
                }
            },
            "current_status": {
                "current_post": "区委副书记、区长",
                "current_org": "湖滨区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002", "S003"]
            },
            "career_timeline": [
                {"start": "2003-09", "end": "unknown", "org": "（履历缺口）", "title": "早期工作经历", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "2003年9月参加工作，2006年6月入党。2002年前 早期具体岗位与教育背景公开资料未找到，存在较大履历缺口", "confidence": "plausible", "source_ids": ["S001"]},
                {"start": "", "end": "", "org": "中共三门峡市湖滨区委员会", "title": "区委副书记", "level": "副处级", "location": "湖滨区", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "2024年起任区委副书记（2024-12 湖滨区委副书记李平调研校园安全报道）", "confidence": "confirmed", "source_ids": ["S003", "S002"]},
                {"start": "2025-03", "end": "2026", "org": "政协三门峡市湖滨区委员会", "title": "区政协主席（兼）", "level": "正处级", "location": "湖滨区", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "2025-03-31 当选政协十二届主席；2025-12 仍任政协党组书记、主席", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
                {"start": "", "end": "present", "org": "湖滨区人民政府", "title": "区长", "level": "正处级", "location": "湖滨区", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2026年初由区委副书记改任区委副书记、区长（2026年4-5月接访名单确认）", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "organizations": [
                {"name": "湖滨区人民政府", "role": "区委副书记、区长", "period": "2026-", "source_ids": ["S003"]},
                {"name": "政协三门峡市湖滨区委员会", "role": "曾任政协主席", "period": "2025-2026", "source_ids": ["S001"]},
                {"name": "中共三门峡市湖滨区委员会", "role": "区委副书记", "period": "2024-", "source_ids": ["S002", "S003"]}
            ],
            "relationships": [
                {"person": "袁锐锋", "person_id": "henan_hubin_yuan_ruifeng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "袁锐锋任区委书记，李平任区长，为当前党政正职搭档", "overlap_org": "湖滨区", "overlap_period": "2026-", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
                {"person": "乔继明", "person_id": "henan_hubin_qiao_jiming", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "乔继明任区长，李平接任区长", "overlap_org": "湖滨区人民政府", "overlap_period": "2026", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S003"]},
                {"person": "郭建体", "person_id": "henan_hubin_guo_jianti", "relationship_type": "overlap", "strength": "weak", "evidence": "同为区委副书记", "overlap_org": "中共三门峡市湖滨区委员会", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "governance_record": [
                {"period": "2024-", "domain": "education", "achievement_or_event": "调研督导校园安全工作（滨河小学、德馨苑校区），推动落实学校安全防控", "role_in_event": "组织者", "measurable_outcome": "", "location": "湖滨区", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "professional_profile": {
                "primary_specializations": ["地方行政管理"],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government", "other"],
                "geographic_pattern": ["甘肃环县", "三门峡湖滨区"],
                "promotion_velocity": {
                    "summary": "籍贯甘肃环县，2003年参加工作，2006年入党，2024年任区委副书记，2025年兼区政协主席，2026年升任区长。履历完整度待补充早期岗位",
                    "notable_fast_promotions": ["2026年从区委副书记/政协主席升任区长（正处级）"]
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "多次深入学校、企业一线调研，强调校园安全和企业服务", "confidence": "plausible", "source_ids": ["S002"]}
                ],
                "speech_themes": ["学生安全", "校园安全", "企业服务"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "截至2026-08，未发现李平相关的公开纪律处分、审计问题或负面报道", "date": AS_OF, "confidence": "unconfirmed"}
            ],
            "source_register": [
                {"id": "S001", "title": "湖滨区政协十二届五次会议决议（附李平简历）", "url": "http://www.hbqzxw.gov.cn/show-11-1617-1.html", "publisher": "湖滨区政协网", "published_at": "2025-03-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "提供李平身份信息与当选政协主席"},
                {"id": "S004", "title": "湖滨区政协十二届六次会议（卫光当选主席，李平曾任主席）", "url": "http://www.hbqzxw.gov.cn/show-11-1911-1.html", "publisher": "湖滨区政协网", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李平不再任政协主席，卫光接任"},
                {"id": "S003", "title": "2026年4月湖滨区县级领导接访安排", "url": "https://www.hubin.gov.cn/25116/2026/3/2244446.html", "publisher": "湖滨区人民政府", "published_at": "2026-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认李平为区委副书记、区长"},
                {"id": "S002", "title": "湖滨区委副书记李平调研校园安全报道", "url": "https://www.hubin.gov.cn/25113/616966560/1880626.html", "publisher": "湖滨区人民政府", "published_at": "2024-12-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2024年已任区委副书记"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "2022年前/早期岗位与教育背景未确认"
            },
            "open_questions": [
                {"priority": "critical", "question": "李平 2003 年参加工作后的早期具体岗位与教育背景是什么？", "why_it_matters": "早期履历影响对其职业根基的判断", "suggested_queries": ["李平 湖滨区 履历", "李平 三门峡 组织 履历", "李平 1979 环县"], "last_attempted": AS_OF}
            ]
        }
    }
]


# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-三门峡市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────────
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-三门峡市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()