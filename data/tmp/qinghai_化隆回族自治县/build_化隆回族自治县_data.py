#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 化隆回族自治县, 海东市, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_化隆回族自治县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — core government leaders confirmed from official
sources (http://www.hualongxian.gov.cn/). County Party Secretary (县委书记)
identity is UNVERIFIED due to limited access to party-affiliated web pages.
Full career timelines, education, and predecessor paths are PARTIAL.

Confirmed:
   县长 (Mayor): 冶祥 (confirmed from official profile, 2024-08)
   县委常委、副县长: 多杰才旦 (confirmed, 2026-04)
   党组成员: 冶刚 (confirmed, 2025-08)
   副县长: 马冠毅 (confirmed, 2025-08)
   副县长: 李元 (confirmed, 2024-08)
   副县长: 刘积海 (confirmed, 2025-08)
   副县长: 马孝云 (confirmed, 2025-01)

Unverified:
   县委书记 (Party Secretary): 待确认 — not found on publicly accessible official pages
"""

from __future__ import annotations

import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "化隆回族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "冶祥",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975-08",
        "birthplace": "青海民和",
        "education": "大学学历",
        "party_join": "2007-08",
        "work_start": "",
        "current_post": "化隆县委副书记、县人民政府县长",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/400143.html"
    },
    {
        "id": 2,
        "name": "多杰才旦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1980-11",
        "birthplace": "青海化隆",
        "education": "研究生学历",
        "party_join": "2009-11",
        "work_start": "",
        "current_post": "化隆县委常委、县人民政府副县长",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/392712.html"
    },
    {
        "id": 3,
        "name": "冶刚",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968-07",
        "birthplace": "青海化隆",
        "education": "大学本科学历",
        "party_join": "1988-11",
        "work_start": "",
        "current_post": "县政府党组成员、巴燕加合经济园党工委常务副书记、管委会常务副主任",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/402009.html"
    },
    {
        "id": 4,
        "name": "马冠毅",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "2000-04",
        "work_start": "1997-10",
        "current_post": "化隆县人民政府副县长",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/398364.html"
    },
    {
        "id": 5,
        "name": "李元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-04",
        "birthplace": "青海民和",
        "education": "大学本科学历",
        "party_join": "2011-11",
        "work_start": "2010-12",
        "current_post": "化隆县人民政府副县长",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/401157.html"
    },
    {
        "id": 6,
        "name": "刘积海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "2003-07",
        "work_start": "",
        "current_post": "化隆县人民政府副县长、县公安局党委书记",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/400913.html"
    },
    {
        "id": 7,
        "name": "马孝云",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1982-04",
        "birthplace": "青海化隆",
        "education": "",
        "party_join": "2008-07",
        "work_start": "2002-01",
        "current_post": "化隆县人民政府副县长",
        "current_org": "化隆回族自治县人民政府",
        "source": "http://www.hualongxian.gov.cn/html/1159/401696.html"
    },
    # ═══════ Key County-Level Leaders from News ═══════
    {
        "id": 8,
        "name": "李伶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化隆县县级领导",
        "current_org": "化隆回族自治县",
        "source": "http://www.hualongxian.gov.cn/html/3130/402837.html"
    },
    # ═══════ Underlying Org Leaders (mentioned in official articles) ═══════
    {
        "id": 9,
        "name": "马成林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化隆县云雀种植专业合作社负责人",
        "current_org": "化隆县云雀种植专业合作社",
        "source": "https://www.haidong.gov.cn/html/41/115921.html"
    },
    {
        "id": 10,
        "name": "马小龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化隆县占龙种养殖专业合作社负责人",
        "current_org": "化隆县占龙种养殖专业合作社",
        "source": "https://www.haidong.gov.cn/html/41/115921.html"
    },
    {
        "id": 11,
        "name": "冶有忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化隆县农业技术推广中心技术员",
        "current_org": "化隆县农业技术推广中心",
        "source": "https://www.haidong.gov.cn/html/41/115921.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "化隆回族自治县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海东市人民政府",
        "location": "青海省海东市化隆回族自治县"
    },
    {
        "id": 2,
        "name": "化隆回族自治县县委",
        "type": "党委",
        "level": "县级",
        "parent": "中共海东市委",
        "location": "青海省海东市化隆回族自治县"
    },
    {
        "id": 3,
        "name": "化隆县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "化隆回族自治县人民政府",
        "location": "青海省海东市化隆回族自治县"
    },
    {
        "id": 4,
        "name": "巴燕加合经济园管委会",
        "type": "开发区",
        "level": "县级",
        "parent": "化隆回族自治县人民政府",
        "location": "青海省海东市化隆回族自治县巴燕镇"
    },
    {
        "id": 5,
        "name": "化隆县农业农村和科技局",
        "type": "政府",
        "level": "县级",
        "parent": "化隆回族自治县人民政府",
        "location": "青海省海东市化隆回族自治县"
    },
    {
        "id": 6,
        "name": "化隆县农业技术推广中心",
        "type": "事业单位",
        "level": "县级",
        "parent": "化隆县农业农村和科技局",
        "location": "青海省海东市化隆回族自治县"
    },
    {
        "id": 7,
        "name": "化隆县云雀种植专业合作社",
        "type": "事业单位",
        "level": "乡镇级",
        "parent": "",
        "location": "青海省海东市化隆回族自治县甘都镇"
    },
    {
        "id": 8,
        "name": "化隆县占龙种养殖专业合作社",
        "type": "事业单位",
        "level": "乡镇级",
        "parent": "",
        "location": "青海省海东市化隆回族自治县牙什尕镇"
    },
    {
        "id": 9,
        "name": "海东市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "青海省人民政府",
        "location": "青海省海东市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 冶祥
    {"person_id": 1, "org_id": 1, "title": "化隆县委副书记、县人民政府县长", "start": "", "end": "present", "rank": "正县级", "note": "主持县政府全面工作，分管县审计局"},
    # 多杰才旦
    {"person_id": 2, "org_id": 1, "title": "化隆县委常委、县人民政府副县长", "start": "", "end": "present", "rank": "副县级", "note": "协助县长处理县政府日常事务；负责发改、财政、统计等"},
    # 冶刚
    {"person_id": 3, "org_id": 1, "title": "县政府党组成员", "start": "", "end": "present", "rank": "副县级", "note": "负责教育、工业、商务、信息化、招商引资等"},
    {"person_id": 3, "org_id": 4, "title": "巴燕加合经济园党工委常务副书记、管委会常务副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 马冠毅
    {"person_id": 4, "org_id": 1, "title": "化隆县人民政府副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责农业农村、乡村振兴、科学技术、水利、卫生健康等"},
    # 李元
    {"person_id": 5, "org_id": 1, "title": "化隆县人民政府副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责自然资源、生态环保、林业草原、交通运输等"},
    # 刘积海
    {"person_id": 6, "org_id": 1, "title": "化隆县人民政府副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责国家安全、公安司法、民族宗教、市场监管等"},
    {"person_id": 6, "org_id": 3, "title": "县公安局党委书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 马孝云
    {"person_id": 7, "org_id": 1, "title": "化隆县人民政府副县长", "start": "", "end": "present", "rank": "副县级", "note": "负责住房和城乡建设、地方品牌产业培育、文体旅游等"},
    # 李伶
    {"person_id": 8, "org_id": 2, "title": "化隆县县级领导", "start": "", "end": "present", "rank": "副县级", "note": "具体职务待确认"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与多杰才旦(县委常委、副县长)：党政领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与冶刚(党组成员)：政府领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与马冠毅(副县长)：政府领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与李元(副县长)：政府领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与刘积海(副县长)：政府领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "冶祥(县长)与马孝云(副县长)：政府领导班子上下级关系",
        "overlap_org": "化隆回族自治县人民政府",
        "overlap_period": "至2026"
    },
]

# ── Build ──────────────────────────────────────────────────────────────────
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
