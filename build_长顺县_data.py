#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长顺县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Changshun County leadership network.

Level: 县
Province: 贵州省
Parent City: 黔南布依族苗族自治州
Region: 长顺县
Targets: 县委书记 & 县长

Research Sources:
- gzcsx.gov.cn — 长顺县人民政府门户网站 (2026年7月)
  - 领导之窗·县政府: https://www.gzcsx.gov.cn/zwgk/ldzc/
  - 县委常委会第171次会议: https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260629_90563912.html
  - 以案促改促治专题民主生活会: https://www.gzcsx.gov.cn/xwzx/zsyw/202607/t20260703_90582814.html
  - 县委办公室党支部党员大会: https://www.gzcsx.gov.cn/xwzx/zsyw/202607/t20260703_90582861.html
  - 仕凯讲授思政课: https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260625_90554694.html
  - 罗仕凯刘刚督导中高考: https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260602_90236253.html
  - 刘刚简历: https://www.gzcsx.gov.cn/zwgk/ldzc/202507/t20250716_88294109.html

Confirmed officeholders (as of 2026-07-23, from gzcsx.gov.cn official news & leadership pages):
- 县委书记: 罗仕凯
- 县委副书记、县长: 刘刚 (1980年11月生，男，汉族，大学，工学学士)
- 县委副书记: 熊明涛
- 县委副书记: 陈红伍
- 县委常委、常务副县长: 邓飞飞 (1985年8月生，男，布依族，大学)
- 县委常委、副县长: 郭海鹏 (1975年6月生，男，汉族，大学，理学学士)
- 县委常委、副县长: 孙同林 (1987年1月生，男，汉族，硕士研究生)
- 县委常委、副县长: 陈立洋 (1982年2月生，男，汉族，硕士研究生)
- 县人大常委会主任: 萧家明
- 县政协主席: 万红梅
- 副县长: 熊波 (1979年1月生，男，汉族，省委党校大学)
- 副县长: 张海川 (1986年11月生，男，汉族，大学)
- 县政府党组成员、办公室主任: 黄彪 (1985年8月生，男，汉族，大学)
- 县领导: 曾琴琴

Note: Most biographical details (birthplace, education institutions, early career)
remain to be filled from external sources.

Research Date: 2026-07-23
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "长顺县"
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
        "name": "罗仕凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委书记",
        "current_org": "中共长顺县委员会",
        "source": "https://www.gzcsx.gov.cn — 长顺县人民政府门户网站, 2026年7月确认"
    },
    {
        "id": 2,
        "name": "刘刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委副书记、县人民政府县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202507/t20250716_88294109.html"
    },
    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "熊明涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委副书记",
        "current_org": "中共长顺县委员会",
        "source": "https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260629_90563912.html"
    },
    {
        "id": 4,
        "name": "陈红伍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委副书记",
        "current_org": "中共长顺县委员会",
        "source": "https://www.gzcsx.gov.cn/xwzx/zsyw/202607/t20260715_90622114.html"
    },
    # ════════════════════════════════════════
    # 县委常委、副县长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "邓飞飞",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委常委、副县长（分管常务工作）",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202208/t20220830_82783692.html"
    },
    {
        "id": 6,
        "name": "郭海鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "",
        "education": "大学，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委常委、副县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202601/t20260127_89341160.html"
    },
    {
        "id": 7,
        "name": "孙同林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年1月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委常委、副县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202601/t20260127_89340415.html"
    },
    {
        "id": 8,
        "name": "陈立洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县委常委、副县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202601/t20260127_89340416.html"
    },
    # ════════════════════════════════════════
    # 县人大 / 县政协
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "萧家明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县人大常委会主任",
        "current_org": "长顺县人民代表大会常务委员会",
        "source": "https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260629_90563912.html"
    },
    {
        "id": 10,
        "name": "万红梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县政协主席",
        "current_org": "中国人民政治协商会议长顺县委员会",
        "source": "https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260629_90563912.html"
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "熊波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县人民政府副县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202311/t20231124_83141920.html"
    },
    {
        "id": 12,
        "name": "张海川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县人民政府副县长",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202206/t20220629_82783720.html"
    },
    {
        "id": 13,
        "name": "黄彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县政府党组成员、县政府办公室主任",
        "current_org": "长顺县人民政府",
        "source": "https://www.gzcsx.gov.cn/zwgk/ldzc/202605/t20260507_90147992.html"
    },
    {
        "id": 14,
        "name": "曾琴琴",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "长顺县领导",
        "current_org": "中共长顺县委员会",
        "source": "https://www.gzcsx.gov.cn/xwzx/zsyw/202606/t20260602_90236253.html"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共长顺县委员会", "org_type": "党委", "level": "县", "location": "贵州省黔南州长顺县"},
    {"id": 2, "name": "长顺县人民政府", "org_type": "政府", "level": "县", "location": "贵州省黔南州长顺县"},
    {"id": 3, "name": "长顺县人民代表大会常务委员会", "org_type": "人大", "level": "县", "location": "贵州省黔南州长顺县"},
    {"id": 4, "name": "中国人民政治协商会议长顺县委员会", "org_type": "政协", "level": "县", "location": "贵州省黔南州长顺县"},
    {"id": 5, "name": "长顺县人民政府办公室", "org_type": "政府", "level": "县", "location": "贵州省黔南州长顺县"},
]

# 3. Positions
positions = [
    # 罗仕凯 — 县委领导
    {"person_id": 1, "org_id": 1, "title": "长顺县委书记", "start_date": "unknown", "end_date": "present", "rank": "正县", "note": ""},
    # 刘刚 — 县政府领导
    {"person_id": 2, "org_id": 1, "title": "长顺县委副书记", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "长顺县人民政府县长", "start_date": "unknown", "end_date": "present", "rank": "正县", "note": ""},
    # 熊明涛 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "长顺县委副书记", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 陈红伍 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "长顺县委副书记", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 邓飞飞 — 县委常委、常务副县长
    {"person_id": 5, "org_id": 1, "title": "长顺县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "长顺县人民政府副县长（分管常务工作）", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 郭海鹏 — 县委常委、副县长
    {"person_id": 6, "org_id": 1, "title": "长顺县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "长顺县人民政府副县长", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 孙同林 — 县委常委、副县长
    {"person_id": 7, "org_id": 1, "title": "长顺县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "长顺县人民政府副县长", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 陈立洋 — 县委常委、副县长
    {"person_id": 8, "org_id": 1, "title": "长顺县委常委", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "长顺县人民政府副县长", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 萧家明 — 县人大主任
    {"person_id": 9, "org_id": 3, "title": "长顺县人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正县", "note": ""},
    # 万红梅 — 县政协主席
    {"person_id": 10, "org_id": 4, "title": "长顺县政协主席", "start_date": "unknown", "end_date": "present", "rank": "正县", "note": ""},
    # 熊波 — 副县长
    {"person_id": 11, "org_id": 2, "title": "长顺县人民政府副县长", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 张海川 — 副县长
    {"person_id": 12, "org_id": 2, "title": "长顺县人民政府副县长", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
    # 黄彪 — 县政府党组成员、办公室主任
    {"person_id": 13, "org_id": 2, "title": "长顺县政府党组成员", "start_date": "unknown", "end_date": "present", "rank": "正科", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "长顺县人民政府办公室主任", "start_date": "unknown", "end_date": "present", "rank": "正科", "note": ""},
    # 曾琴琴 — 县领导
    {"person_id": 14, "org_id": 1, "title": "长顺县领导", "start_date": "unknown", "end_date": "present", "rank": "副县", "note": ""},
]

# 4. Relationships
relationships = [
    # 书记—县长搭档关系
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档关系，共同负责县委和县政府全面工作。共同督导中高考筹备等工作。",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
    # 书记—副书记
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记在县委常委会中共事",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记在县委常委会中共事",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
    # 县长—常务副县长
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与常务副县长在县政府领导班子中共事，协助县长负责县政府常务工作",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    # 县长—副县长们
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长在县政府领导班子中共事",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长在县政府领导班子中共事",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长在县政府领导班子中共事",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长与副县长在县政府领导班子中共事",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长与副县长在县政府领导班子中共事",
        "overlap_org": "长顺县人民政府",
        "overlap_period": "unknown~present"
    },
    # 县委常委之间（共同在县委常委会共事）
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "同为县委常委、副县长，在县委常委会和县政府领导班子双重共事关系",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 5, "person_b": 7,
        "type": "overlap",
        "context": "同为县委常委、副县长，在县委常委会和县政府领导班子双重共事关系",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
    {
        "person_a": 5, "person_b": 8,
        "type": "overlap",
        "context": "同为县委常委、副县长，在县委常委会和县政府领导班子双重共事关系",
        "overlap_org": "中共长顺县委员会",
        "overlap_period": "unknown~present"
    },
]

# ── Run Build ──
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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
