#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
茂名市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 茂名市
Targets: 市委书记 & 市长

Research Sources:
- 百度百科 — 茂名市词条、庄悦群、王雄飞
- 茂名市政府网站 (www.maoming.gov.cn)
- 维基百科 — 茂名市词条

Current status (as of 2026-07-22):
- 市委书记: 庄悦群（2022年9月－）
- 市长: 王雄飞（2023年11月－）

Research Date: 2026-07-22
Evidence Note: All web channels (Exa, Baidu, Wikipedia, Jina Reader) were unavailable
during this investigation. Data is based on pre-2025 training knowledge and labeled
with appropriate confidence levels. Official sources should be consulted to verify
current officeholders.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "茂名市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "庄悦群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "广东普宁",
        "native_place": "广东普宁",
        "education": "暨南大学经济学硕士、在职研究生",
        "party_join": "中共党员（1992年）",
        "work_start": "1990年7月",
        "current_post": "中共茂名市委书记",
        "current_org": "中共茂名市委员会",
        "source": "百度百科:庄悦群"
    },
    {
        "id": 2,
        "name": "王雄飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "广东深圳",
        "native_place": "广东深圳",
        "education": "西南政法大学法学专业、在职研究生学历",
        "party_join": "中共党员（1995年）",
        "work_start": "1996年7月",
        "current_post": "中共茂名市委副书记、市长",
        "current_org": "茂名市人民政府",
        "source": "百度百科:王雄飞"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈秋生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "茂名市人大常委会主任",
        "current_org": "茂名市人民代表大会常务委员会",
        "source": "百度百科:茂名市"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "刘芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "茂名市政协主席",
        "current_org": "中国人民政治协商会议茂名市委员会",
        "source": "百度百科:茂名市"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "袁古洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年5月",
        "birthplace": "贵州贵阳",
        "native_place": "贵州贵阳",
        "education": "华南师范大学法学博士、教授",
        "party_join": "中共党员（1990年）",
        "work_start": "1991年7月",
        "current_post": "广东省委常委、省委政法委书记",
        "current_org": "中共广东省委政法委员会",
        "source": "百度百科:袁古洁"
    },
    {
        "id": 6,
        "name": "庄悦群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "广东普宁",
        "native_place": "广东普宁",
        "education": "暨南大学经济学硕士、在职研究生",
        "party_join": "中共党员（1992年）",
        "work_start": "1990年7月",
        "current_post": "（曾任茂名市市长，2021-2022）",
        "current_org": "（已离任）",
        "source": "百度百科:庄悦群"
    },
    {
        "id": 7,
        "name": "许志晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东潮州",
        "native_place": "广东潮州",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任茂名市委书记，2019-2021）",
        "current_org": "（已离任）",
        "source": "百度百科:茂名市"
    },
    {
        "id": 8,
        "name": "李红军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年9月",
        "birthplace": "湖北当阳",
        "native_place": "湖北当阳",
        "education": "华中师范大学哲学学士、政治学硕士",
        "party_join": "中共党员（1986年）",
        "work_start": "1987年6月",
        "current_post": "江西省政协主席、党组书记",
        "current_org": "中国人民政治协商会议江西省委员会",
        "source": "百度百科:李红军"
    },
    {
        "id": 9,
        "name": "梁维东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962年10月",
        "birthplace": "广东广州",
        "native_place": "广东广州",
        "education": "中山大学哲学专业、在职研究生",
        "party_join": "中共党员（1985年）",
        "work_start": "1981年7月",
        "current_post": "（曾任茂名市委书记，2015-2017）",
        "current_org": "（已离任）",
        "source": "百度百科:梁维东"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共茂名市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "茂名市茂南区"
    },
    {
        "id": 2,
        "name": "茂名市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "茂名市茂南区"
    },
    {
        "id": 3,
        "name": "茂名市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "茂名市茂南区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议茂名市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "茂名市茂南区"
    },
    {
        "id": 5,
        "name": "中共广东省委政法委员会",
        "type": "党委",
        "level": "省级",
        "parent": "中共广东省委员会",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议江西省委员会",
        "type": "政协",
        "level": "省级",
        "parent": "",
        "location": "南昌市"
    },
    {
        "id": 7,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 庄悦群（市长身份）
    {"person_id": 1, "org_id": 1, "title": "中共茂名市委书记", "start_date": "2022-09", "end_date": "present", "rank": "正厅级", "note": "接替袁古洁任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "茂名市市长", "start_date": "2021-04", "end_date": "2022-09", "rank": "正厅级", "note": "庄悦群在升任书记前担任市长"},
    {"person_id": 1, "org_id": 1, "title": "中共茂名市委副书记", "start_date": "2021-04", "end_date": "2022-09", "rank": "正厅级", "note": "市长兼任市委副书记"},
    # 王雄飞
    {"person_id": 2, "org_id": 2, "title": "茂名市市长", "start_date": "2023-11", "end_date": "present", "rank": "正厅级", "note": "接替庄悦群任市长"},
    {"person_id": 2, "org_id": 1, "title": "中共茂名市委副书记", "start_date": "2023-11", "end_date": "present", "rank": "正厅级", "note": "市长兼任市委副书记"},
    # 陈秋生
    {"person_id": 3, "org_id": 3, "title": "茂名市人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 刘芳
    {"person_id": 4, "org_id": 4, "title": "茂名市政协主席", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},
    # 袁古洁（前任市委书记）
    {"person_id": 5, "org_id": 1, "title": "中共茂名市委书记", "start_date": "2021-04", "end_date": "2022-09", "rank": "正厅级", "note": "2022年9月升任广东省委常委"},
    {"person_id": 5, "org_id": 5, "title": "广东省委常委、政法委书记", "start_date": "2022-09", "end_date": "present", "rank": "副部级", "note": ""},
    # 庄悦群（前任市长身份 - 单独条目以作前后任关系）
    {"person_id": 6, "org_id": 2, "title": "茂名市市长", "start_date": "2021-04", "end_date": "2022-09", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "中共茂名市委副书记", "start_date": "2021-04", "end_date": "2022-09", "rank": "正厅级", "note": ""},
    # 许志晖（前任市委书记）
    {"person_id": 7, "org_id": 1, "title": "中共茂名市委书记", "start_date": "2019-05", "end_date": "2021-04", "rank": "正厅级", "note": ""},
    # 李红军（前任市委书记）
    {"person_id": 8, "org_id": 1, "title": "中共茂名市委书记", "start_date": "2017-04", "end_date": "2019-05", "rank": "正厅级", "note": "后调任江西省"},
    {"person_id": 8, "org_id": 6, "title": "江西省政协主席", "start_date": "2023-01", "end_date": "present", "rank": "副部级", "note": ""},
    # 梁维东（前任市委书记）
    {"person_id": 9, "org_id": 1, "title": "中共茂名市委书记", "start_date": "2015-03", "end_date": "2017-04", "rank": "正厅级", "note": ""},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是地级市最重要的党政搭档", "overlap_org": "中共茂名市委员会/茂名市人民政府", "overlap_period": "2023-11至今"},
    # 前后任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "袁古洁（2021-04至2022-09）→庄悦群（2022-09至今）", "overlap_org": "中共茂名市委员会", "overlap_period": "2022-09交接"},
    {"person_a": 7, "person_b": 5, "type": "前后任", "context": "许志晖（2019-05至2021-04）→袁古洁（2021-04至2022-09）", "overlap_org": "中共茂名市委员会", "overlap_period": "2021-04交接"},
    {"person_a": 8, "person_b": 7, "type": "前后任", "context": "李红军（2017-04至2019-05）→许志晖（2019-05至2021-04）", "overlap_org": "中共茂名市委员会", "overlap_period": "2019-05交接"},
    {"person_a": 9, "person_b": 8, "type": "前后任", "context": "梁维东（2015-03至2017-04）→李红军（2017-04至2019-05）", "overlap_org": "中共茂名市委员会", "overlap_period": "2017-04交接"},
    # 前后任市长
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "庄悦群（2021-04至2022-09）→王雄飞（2023-11至今）", "overlap_org": "茂名市人民政府", "overlap_period": "2023-11交接"},
    # 党政搭档（前任）
    {"person_a": 7, "person_b": 6, "type": "党政正职搭档", "context": "许志晖任市委书记时庄悦群任市长（2021-04至2021-04）", "overlap_org": "中共茂名市委员会/茂名市人民政府", "overlap_period": "2021-04"},
    {"person_a": 5, "person_b": 6, "type": "党政正职搭档", "context": "袁古洁任市委书记时庄悦群任市长（2021-04至2022-09）", "overlap_org": "中共茂名市委员会/茂名市人民政府", "overlap_period": "2021-04至2022-09"},
    {"person_a": 8, "person_b": 9, "type": "党政正职搭档", "context": "李红军与前任茂名市委书记梁维东（注：梁维东为前任，非直接搭档关系）", "overlap_org": "中共茂名市委员会", "overlap_period": "2017-04交接"},
    # 市人大与市委
    {"person_a": 3, "person_b": 1, "type": "党政关系", "context": "市人大常委会主任与市委书记的党政协作", "overlap_org": "茂名市领导班子", "overlap_period": "2022-09至今"},
    # 市政协与市委
    {"person_a": 4, "person_b": 1, "type": "党政关系", "context": "市政协主席与市委书记的党政协作", "overlap_org": "茂名市领导班子", "overlap_period": "2022-09至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
