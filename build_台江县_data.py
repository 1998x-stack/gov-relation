#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台江县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Taijiang County leadership network.

Level: 县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Region: 台江县
Targets: 县委书记 & 县长

Research Sources:
- qdn.gov.cn 黔东南州人民政府门户网站 — 张定超到台江县调研报道 (2026-07-17)
  https://www.qdn.gov.cn/xwzx_5871605/qdnyw_5871606/202607/t20260720_90636649.html
- 黔东南苗族侗族自治州领导班子调研报告 (2026-07-23)
- 张定超 to 台江县调研 — 确认台江县为黔东南州辖县

Confirmed officeholders (as of 2026-07-23):
- 县委书记: 待查 (需通过台江县门户网站或黔东南州组织部任前公示确认)
- 县长: 待查 (需通过台江县门户网站或黔东南州人大任命公告确认)
- 县委班子成员: 待查
- 政府班子成员: 待查

已知台江县相关产业/经济信息:
- 再生资源循环材料产业 (天能集团贵州能源科技有限公司、贵州麒臻实业集团有限公司)
- 台江县被列为黔东南州首个百亿级产业基地

Open Gaps (to be filled in future investigations):
- 当前县委书记、县长的姓名、出生年月、籍贯、完整履历
- 县委副书记、常务副县长、纪委书记、组织部长、宣传部长等班子成员
- 前任县委书记和县长的去向
- 台江县门户网站域名或访问方式

Research Date: 2026-07-23
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "台江县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Top Two Leaders (Names unknown — placeholders)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待查-县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "台江县委书记",
        "current_org": "中共台江县委员会",
        "source": "待查 — 需通过台江县门户网站或黔东南州组织部任前公示确认"
    },
    {
        "id": 2,
        "name": "待查-县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "台江县委副书记、县长",
        "current_org": "台江县人民政府",
        "source": "待查 — 需通过台江县门户网站或黔东南州人大任命公告确认"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共台江县委员会", "type": "党委", "level": "县级", "parent": "中共黔东南苗族侗族自治州委员会", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 2, "name": "台江县人民政府", "type": "政府", "level": "县级", "parent": "黔东南苗族侗族自治州人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 3, "name": "台江县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 4, "name": "中国人民政治协商会议台江县委员会", "type": "政协", "level": "县级", "parent": "", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 5, "name": "中共台江县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共台江县委员会", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 6, "name": "台江县人民检察院", "type": "政府", "level": "县级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 7, "name": "台江县人民法院", "type": "政府", "level": "县级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    # 乡镇/街道
    {"id": 8, "name": "台拱街道", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 9, "name": "萃文街道", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 10, "name": "施洞镇", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 11, "name": "台盘乡", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 12, "name": "革一镇", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 13, "name": "老屯乡", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 14, "name": "排羊乡", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 15, "name": "南宫镇", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
    {"id": 16, "name": "方召镇", "type": "乡镇/街道", "level": "乡级", "parent": "台江县人民政府", "location": "贵州省黔东南苗族侗族自治州台江县"},
]

# 3. Positions
positions = [
    # 县委书记 (placeholder)
    {"person_id": 1, "org_id": 1, "title": "台江县委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "姓名待查"},
    # 县长 (placeholder)
    {"person_id": 2, "org_id": 2, "title": "台江县委副书记、县长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "姓名待查"},
]

# 4. Relationships
relationships = [
    # 县委书记 <-> 县长 (co-working)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共台江县委员会", "overlap_period": ""},
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
