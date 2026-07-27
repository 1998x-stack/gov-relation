#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宕昌县 (甘肃省陇南市) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Tanchang County leadership network.

Level: 县
Province: 甘肃省
City: 陇南市
Region: 宕昌县
Targets: 县委书记 & 县长

Research Sources:
- 宕昌县人民政府官方网站 (tanchang.gov.cn) 领导之窗, 2026年7月确认
- 宕昌县人民政府网站新闻动态

Research Date: 2026-07-22
"""

import os
import sys
from pathlib import Path

# Add project root to path for gov_relation imports
_REPO_ROOT = Path(__file__).resolve()
for _parent in [_REPO_ROOT] + list(_REPO_ROOT.parents):
    if (_parent / "gov_relation" / "__init__.py").exists():
        _REPO_ROOT = _parent
        break
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # used by the runner internally; kept here for process_tmp.py validation

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, "宕昌县_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "宕昌县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张建强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宕昌县委员会",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 2,
        "name": "张继龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张文厚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共宕昌县委员会",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "汪小波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、官鹅沟大景区管理委员会主任",
        "current_org": "官鹅沟大景区管理委员会",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "王广毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 6,
        "name": "王小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共宕昌县委员会组织部",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 7,
        "name": "董倍宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共宕昌县纪律检查委员会/宕昌县监察委员会",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "蔡鸿鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共宕昌县委员会政法委员会",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 9,
        "name": "陶仲军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共宕昌县委员会统战部",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 10,
        "name": "李鼎新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共宕昌县委员会宣传部",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 11,
        "name": "胡义文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、人武部政委",
        "current_org": "宕昌县人民武装部",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 12,
        "name": "牛宿光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 县政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "巩小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局党委书记、局长",
        "current_org": "宕昌县人民政府/宕昌县公安局",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 14,
        "name": "王永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 15,
        "name": "冉小龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 16,
        "name": "张莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 17,
        "name": "杨武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 18,
        "name": "赵洪浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
    {
        "id": 19,
        "name": "苏继成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "二级调研员",
        "current_org": "宕昌县人民政府",
        "source": "https://www.tanchang.gov.cn/ldzc/",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共宕昌县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 2,
        "name": "中共宕昌县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 3,
        "name": "中共宕昌县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 4,
        "name": "中共宕昌县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 5,
        "name": "中共宕昌县委员会统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 6,
        "name": "宕昌县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "陇南市人民政府",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 7,
        "name": "中共宕昌县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 8,
        "name": "宕昌县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共宕昌县委员会",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 9,
        "name": "宕昌县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "宕昌县人民政府",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 10,
        "name": "宕昌县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "宕昌县人民政府",
        "location": "甘肃省陇南市宕昌县",
    },
    {
        "id": 11,
        "name": "官鹅沟大景区管理委员会",
        "type": "事业单位",
        "level": "县级",
        "parent": "宕昌县人民政府",
        "location": "甘肃省陇南市宕昌县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 张建强 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 张继龙 - 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    # 张文厚 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 汪小波 - 官鹅沟大景区管委会主任
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 11, "title": "官鹅沟大景区管理委员会主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王广毅 - 常务副县长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助县长负责县政府日常工作"},
    # 王小军 - 组织部部长
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 董倍宏 - 纪委书记
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 蔡鸿鸣 - 政法委书记
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陶仲军 - 统战部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "统战部部长、县政协党组副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李鼎新 - 宣传部部长
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 胡义文 - 人武部政委
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "人武部政委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 牛宿光 - 副县长
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 巩小军 - 副县长、公安局长
    {"person_id": 13, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 王永刚 - 副县长
    {"person_id": 14, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 冉小龙 - 副县长
    {"person_id": 15, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张莉 - 副县长
    {"person_id": 16, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨武 - 副县长
    {"person_id": 17, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 赵洪浩 - 副县长
    {"person_id": 18, "org_id": 6, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 苏继成 - 二级调研员
    {"person_id": 19, "org_id": 6, "title": "二级调研员", "start_date": "", "end_date": "present", "rank": "副县级", "note": "非领导职务"},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 张建强 —— 县委常委班子成员（共事于中共宕昌县委员会）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—专职副书记", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共宕昌县委员会/宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 7, "type": "监督", "context": "县委书记—纪委书记（同级监督）", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "县委书记—统战部部长", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "县委书记—副县长", "overlap_org": "中共宕昌县委员会/宕昌县人民政府", "overlap_period": "2026—"},
    # 张继龙 —— 县长与班子成员
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "县长—常务副县长", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长王永刚", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长冉小龙", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "县长—副县长张莉", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "县长—副县长杨武", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "县长—副县长赵洪浩", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长/公安局长巩小军", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    # 王广毅 —— 常务副县长与副县长们
    {"person_a": 5, "person_b": 12, "type": "共事", "context": "常务副县长—副县长牛宿光", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 14, "type": "共事", "context": "常务副县长—副县长王永刚", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 15, "type": "共事", "context": "常务副县长—副县长冉小龙", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 16, "type": "共事", "context": "常务副县长—副县长张莉", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 17, "type": "共事", "context": "常务副县长—副县长杨武", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 18, "type": "共事", "context": "常务副县长—副县长赵洪浩", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 5, "person_b": 13, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "宕昌县人民政府", "overlap_period": "2026—"},
    # 蔡鸿鸣 —— 政法委书记与公安局长
    {"person_a": 8, "person_b": 13, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "宕昌县政法系统", "overlap_period": "2026—"},
    # 董倍宏 —— 纪委书记
    {"person_a": 7, "person_b": 1, "type": "监督", "context": "纪委监督县委主要领导", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    # 王小军 —— 组织部部长与各乡镇人事
    {"person_a": 6, "person_b": 1, "type": "共事", "context": "组织部部长—县委书记（干部任命决策）", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    # 陶仲军 —— 统战部与政协
    {"person_a": 9, "person_b": 1, "type": "共事", "context": "统战部长—县委书记", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    # 李鼎新 —— 宣传部长
    {"person_a": 10, "person_b": 1, "type": "共事", "context": "宣传部长—县委书记", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
    # 专职副书记与县委常委
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "专职副书记—常务副县长", "overlap_org": "中共宕昌县委员会/宕昌县人民政府", "overlap_period": "2026—"},
    {"person_a": 3, "person_b": 6, "type": "共事", "context": "专职副书记—组织部部长", "overlap_org": "中共宕昌县委员会", "overlap_period": "2026—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("宕昌县（甘肃省陇南市）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()

    run_build(
        slug="宕昌县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("=" * 60)
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print("Build complete!")
