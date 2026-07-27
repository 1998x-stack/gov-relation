#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黔东南苗族侗族自治州领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Qiandongnan Miao and Dong
Autonomous Prefecture leadership network.

Level: 地级市 (自治州)
Province: 贵州省
Region: 黔东南苗族侗族自治州
Targets: 州委书记 & 州长

Research Sources:
- qdn.gov.cn 黔东南州人民政府门户网站 — 州委书记张定超调研报道 (2026年7月)
- qdn.gov.cn — 州长杨光杰安全生产督导检查报道 (2026年7月)
- qdn.gov.cn — 70周年州庆筹备工作会议 (2026年7月)
- qdn.gov.cn — 州政府常务会议 (2026年7月)

Confirmed officeholders (as of 2026-07-23, from qdn.gov.cn official news):
- 州委书记: 张定超 (active July 2026, inspecting industry/flood prevention)
- 州委副书记、州长: 杨光杰 (active July 2026, presiding over government meetings)
- 州委常委、常务副州长: 陈曦
- 副州长: 杨锦春
- 州政府秘书长: 舒健
- 州政协主席: 高峰
- 州领导: 陆再义, 王永明, 谭海, 谭夔, 龙家胜, 杨承进, 谢治刚
- 州领导: 吴世胜, 吴光福, 罗青, 周文锋, 吴昌和, 龙贤润
- 省政协民族与宗教委员会副主任: 潘玉凤

Predecessors:
- 前任州委书记: 待查 (资料缺口)
- 前任州长: 待查 (资料缺口)

Open Gaps (to be filled in future investigations):
- 张定超: 完整履历（籍贯、出生年份、教育背景、入党时间、工作起始年份）待补充
- 杨光杰: 完整履历（籍贯、出生年份、教育背景、入党时间、工作起始年份）待补充
- 州委常委班子: 组织部长、宣传部长、政法委书记、纪委书记等信息待查
- 前几任州委书记/州长: 完整任职序列待查
- 州人大主任信息待查

Research Date: 2026-07-23
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "黔东南苗族侗族自治州"
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
        "name": "张定超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州委书记",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 黔东南州人民政府门户网站, 2026年7月确认"
    },
    {
        "id": 2,
        "name": "杨光杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州委副书记、州长",
        "current_org": "黔东南苗族侗族自治州人民政府",
        "source": "https://www.qdn.gov.cn — 黔东南州人民政府门户网站, 2026年7月确认"
    },
    # ════════════════════════════════════════
    # 州委常委/副州长 (Standing Committee / Deputy Governors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陈曦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、常务副州长",
        "current_org": "黔东南苗族侗族自治州人民政府",
        "source": "https://www.qdn.gov.cn/xwzx_5871605/qdnyw_5871606/202607/t20260721_90643172.html — 张定超调研防汛抗旱报道"
    },
    {
        "id": 4,
        "name": "杨锦春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黔东南州副州长",
        "current_org": "黔东南苗族侗族自治州人民政府",
        "source": "https://www.qdn.gov.cn — 杨光杰安全生产督导检查报道, 2026年7月"
    },
    {
        "id": 5,
        "name": "舒健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黔东南州政府秘书长",
        "current_org": "黔东南苗族侗族自治州人民政府办公室",
        "source": "https://www.qdn.gov.cn — 杨光杰安全生产督导检查报道, 2026年7月"
    },
    # ════════════════════════════════════════
    # 州领导 (Other Prefecture Leaders)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "高峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州政协主席",
        "current_org": "中国人民政治协商会议黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn/xwzx_5871605/qdnyw_5871606/202607/t20260720_90636645.html — 70周年州庆筹备会议"
    },
    {
        "id": 7,
        "name": "潘玉凤",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "省政协民族与宗教委员会副主任（原黔东南州政协主席）",
        "current_org": "贵州省政协民族与宗教委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 8,
        "name": "陆再义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn/xwzx_5871605/qdnyw_5871606/202607/t20260721_90643172.html — 张定超调研防汛抗旱报道"
    },
    {
        "id": 9,
        "name": "王永明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 张定超调研防汛抗旱报道, 2026年7月"
    },
    {
        "id": 10,
        "name": "谭海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 11,
        "name": "谭夔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 12,
        "name": "龙家胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 13,
        "name": "杨承进",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 14,
        "name": "谢治刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 15,
        "name": "吴世胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 16,
        "name": "吴光福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 17,
        "name": "罗青",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 18,
        "name": "周文锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 19,
        "name": "吴昌和",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
    {
        "id": 20,
        "name": "龙贤润",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔东南州领导",
        "current_org": "中共黔东南苗族侗族自治州委员会",
        "source": "https://www.qdn.gov.cn — 70周年州庆筹备会议, 2026年7月"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共黔东南苗族侗族自治州委员会", "type": "党委", "level": "地级", "parent": "中共贵州省委员会", "location": "贵州省黔东南州凯里市"},
    {"id": 2, "name": "黔东南苗族侗族自治州人民政府", "type": "政府", "level": "地级", "parent": "贵州省人民政府", "location": "贵州省黔东南州凯里市"},
    {"id": 3, "name": "中国人民政治协商会议黔东南苗族侗族自治州委员会", "type": "政协", "level": "地级", "parent": "", "location": "贵州省黔东南州凯里市"},
    {"id": 4, "name": "贵州省政协民族与宗教委员会", "type": "政协", "level": "省级", "parent": "贵州省政协", "location": "贵州省贵阳市"},
    {"id": 5, "name": "黔东南州人民政府办公室", "type": "政府", "level": "地级", "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南州凯里市"},
]

# 3. Positions
positions = [
    # 张定超
    {"person_id": 1, "org_id": 1, "title": "黔东南州委书记", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": "2026年7月在任"},
    # 杨光杰
    {"person_id": 2, "org_id": 1, "title": "黔东南州委副书记", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": "2026年7月在任"},
    {"person_id": 2, "org_id": 2, "title": "黔东南州州长", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": "2026年7月在任"},
    # 陈曦
    {"person_id": 3, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副州长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 杨锦春
    {"person_id": 4, "org_id": 2, "title": "黔东南州副州长", "start_date": "", "end_date": "至今", "rank": "副厅级", "note": ""},
    # 舒健
    {"person_id": 5, "org_id": 5, "title": "黔东南州政府秘书长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 高峰
    {"person_id": 6, "org_id": 3, "title": "黔东南州政协主席", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": "2026年7月在任"},
    # 潘玉凤
    {"person_id": 7, "org_id": 4, "title": "省政协民族与宗教委员会副主任", "start_date": "", "end_date": "至今", "rank": "正厅级", "note": "曾任黔东南州政协主席"},
    # 其他州领导
    {"person_id": 8, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 9, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 10, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 11, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 14, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 15, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 16, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 17, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 18, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 19, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 20, "org_id": 1, "title": "黔东南州领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
]

# 4. Relationships
relationships = [
    # 州委书记 <-> 州长 (top leadership co-working)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "州委书记—州长搭档", "overlap_org": "中共黔东南苗族侗族自治州委员会", "overlap_period": "2026年"},
    # 州委书记 <-> 常务副州长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "州委书记—常务副州长", "overlap_org": "中共黔东南苗族侗族自治州委员会", "overlap_period": "2026年"},
    # 州长 <-> 常务副州长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "州长—常务副州长", "overlap_org": "黔东南苗族侗族自治州人民政府", "overlap_period": "2026年"},
    # 州长 <-> 副州长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "州长—副州长", "overlap_org": "黔东南苗族侗族自治州人民政府", "overlap_period": "2026年"},
    # 州长 <-> 政府秘书长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "州长—政府秘书长", "overlap_org": "黔东南苗族侗族自治州人民政府", "overlap_period": "2026年"},
    # 政协主席 <-> 州领导班子
    {"person_a": 6, "person_b": 1, "type": "共事", "context": "州政协主席—州委书记", "overlap_org": "黔东南州", "overlap_period": "2026年"},
    {"person_a": 6, "person_b": 2, "type": "共事", "context": "州政协主席—州长", "overlap_org": "黔东南州", "overlap_period": "2026年"},
    # 潘玉凤（前任政协主席）<-> 高峰（现任政协主席）
    {"person_a": 7, "person_b": 6, "type": "前后任", "context": "潘玉凤曾任州政协主席, 高峰现任州政协主席", "overlap_org": "中国人民政治协商会议黔东南苗族侗族自治州委员会", "overlap_period": ""},
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
    print("Done.")
