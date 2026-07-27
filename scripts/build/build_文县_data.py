#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文县 (甘肃省陇南市) 领导班子工作关系网络数据构建脚本
Generate SQLite database + GEXF graph for Wen County leadership network.

Level: 县
Province: 甘肃省
City: 陇南市
Region: 文县
Targets: 县委书记 & 县长

Research Sources:
- 文县人民政府官方网站 (lnwx.gov.cn) 领导之窗, 2026年7月确认
- Baidu Baike 文县人民政府词条, 2026年7月

Research Date: 2026-07-22
"""

import os
import sys
from pathlib import Path

# Add project root to path for gov_relation imports
# Find project root: walk up until gov_relation/__init__.py is found
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
DB_PATH = os.path.join(STAGING_DIR, "文县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "文县_network.gexf")

# ═══════════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委主要领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "贾爱会",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共文县委员会",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 2,
        "name": "牛军平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共文县委员会",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 县委常委
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长",
        "current_org": "中共文县委员会组织部",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 4,
        "name": "曹斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委宣传部部长",
        "current_org": "中共文县委员会宣传部",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "何留",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委政法委书记",
        "current_org": "中共文县委员会政法委员会",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 6,
        "name": "李缘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 7,
        "name": "梁丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共文县纪律检查委员会/文县监察委员会",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "杨明亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政府副县长",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 9,
        "name": "周晓鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "文县人民武装部",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 10,
        "name": "刘青春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政府副县长（挂职）",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 11,
        "name": "周强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政府副县长（挂职）",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 12,
        "name": "柳婷婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政府副县长（挂职）",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    # ════════════════════════════════════════
    # 政府副县长（非县委常委）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "王俊学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政府副县长",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 14,
        "name": "王瑛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政府副县长",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 15,
        "name": "王海飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政府副县长",
        "current_org": "文县人民政府",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
    {
        "id": 16,
        "name": "赵梁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政府副县长、县公安局局长",
        "current_org": "文县人民政府/文县公安局",
        "source": "https://www.lnwx.gov.cn/ldzc/",
    },
]

# ═══════════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共文县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共陇南市委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 2,
        "name": "中共文县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共文县委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 3,
        "name": "中共文县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共文县委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 4,
        "name": "中共文县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共文县委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 5,
        "name": "文县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "陇南市人民政府",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 6,
        "name": "中共文县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共文县委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 7,
        "name": "文县监察委员会",
        "type": "监察",
        "level": "县级",
        "parent": "中共文县委员会",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 8,
        "name": "文县人民武装部",
        "type": "政府",
        "level": "县级",
        "parent": "文县人民政府",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 9,
        "name": "文县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "文县人民政府",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 10,
        "name": "文县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "文县",
        "location": "甘肃省陇南市文县",
    },
    {
        "id": 11,
        "name": "中国人民政治协商会议文县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "文县",
        "location": "甘肃省陇南市文县",
    },
]

# ═══════════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════════

positions = [
    # 贾爱会 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作"},
    {"person_id": 1, "org_id": 5, "title": "县长（此前曾任）", "start_date": "", "end_date": "", "rank": "正县级", "note": "后升任县委书记"},
    # 牛军平 - 县委副书记
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李丽 - 组织部部长
    {"person_id": 3, "org_id": 2, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 曹斌 - 宣传部部长
    {"person_id": 4, "org_id": 3, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 何留 - 政法委书记
    {"person_id": 5, "org_id": 4, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李缘 - 常务副县长
    {"person_id": 6, "org_id": 5, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 梁丰 - 纪委书记
    {"person_id": 7, "org_id": 6, "title": "县委常委、县纪委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨明亮 - 副县长
    {"person_id": 8, "org_id": 5, "title": "县委常委、政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 周晓鹏 - 人武部部长
    {"person_id": 9, "org_id": 8, "title": "县委常委、县人武部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘青春 - 挂职副县长
    {"person_id": 10, "org_id": 5, "title": "县委常委、政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    # 周强 - 挂职副县长
    {"person_id": 11, "org_id": 5, "title": "县委常委、政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    # 柳婷婷 - 挂职副县长
    {"person_id": 12, "org_id": 5, "title": "县委常委、政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职"},
    # 王俊学 - 副县长
    {"person_id": 13, "org_id": 5, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王瑛 - 副县长
    {"person_id": 14, "org_id": 5, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王海飞 - 副县长
    {"person_id": 15, "org_id": 5, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 赵梁 - 副县长、公安局长
    {"person_id": 16, "org_id": 5, "title": "政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

# ═══════════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════════

relationships = [
    # 贾爱会 —— 县委常委班子成员（共事于中共文县委员会）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县委副书记搭档", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—组织部部长", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—宣传部部长", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "县委书记—政法委书记", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "县委书记—常务副县长", "overlap_org": "中共文县委员会/文县人民政府", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "县委书记—纪委书记", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "县委书记—副县长", "overlap_org": "中共文县委员会/文县人民政府", "overlap_period": "2026—"},
    # 李缘 —— 常务副县长与班子成员
    {"person_a": 6, "person_b": 8, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 6, "person_b": 13, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 6, "person_b": 14, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 6, "person_b": 15, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 6, "person_b": 16, "type": "共事", "context": "常务副县长—副县长/公安局长", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    # 梁丰 —— 纪委书记
    {"person_a": 7, "person_b": 1, "type": "监督", "context": "纪委监督县委主要领导", "overlap_org": "中共文县委员会", "overlap_period": "2026—"},
    # 挂职副县长
    {"person_a": 10, "person_b": 11, "type": "共事", "context": "挂职副县长同僚", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 10, "person_b": 12, "type": "共事", "context": "挂职副县长同僚", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    {"person_a": 11, "person_b": 12, "type": "共事", "context": "挂职副县长同僚", "overlap_org": "文县人民政府", "overlap_period": "2026—"},
    # 政法委-公安局线
    {"person_a": 5, "person_b": 16, "type": "领导关系", "context": "政法委书记—公安局长", "overlap_org": "文县政法系统", "overlap_period": "2026—"},
    # 赵梁 - 公安局
    {"person_a": 16, "person_b": 5, "type": "隶属", "context": "公安局长受政法委领导", "overlap_org": "文县政法系统", "overlap_period": "2026—"},
]

# ═══════════════════════════════════════════════
# 执行构建
# ═══════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("文县（甘肃省陇南市）领导班子工作关系网络数据构建")
    print("=" * 60)
    print()

    run_build(
        slug="文县",
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
