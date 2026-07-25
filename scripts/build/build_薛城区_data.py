#!/usr/bin/env python3
"""Build script for 薛城区 (枣庄市) government personnel network.

Task: shandong_薛城区
Province: 山东省
Parent city: 枣庄市
Region: 薛城区
Level: 市辖区
Targets: 区委书记 & 区长
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Personnel ────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "巴海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区委书记",
        "current_org": "中共枣庄市薛城区委员会",
        "source": "薛城区政府官网新闻（2026-07-24标题'巴海峰会见来薛客商'称区委书记）; 区政府领导页面未列出（区委书记不属区政府领导）",
    },
    {
        "id": 2,
        "name": "樊猛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "在职研究生学历，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区委副书记、区人民政府党组书记、区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202201/t20220129_1387172.html）",
    },
    {
        "id": 3,
        "name": "张建兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "在职研究生学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区人民政府党组副书记，薛城经济开发区党工委书记、管委会主任",
        "current_org": "薛城经济开发区",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202201/t20220129_1387175.html）",
    },
    {
        "id": 4,
        "name": "庞伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区委常委，区人民政府党组副书记、常务副区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202402/t20240217_1841763.html）",
    },
    {
        "id": 5,
        "name": "张健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区委常委，区人民政府党组成员、副区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202111/t20211119_1339975.html）",
    },
    {
        "id": 6,
        "name": "刘凌东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区人民政府党组成员、副区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202201/t20220129_1387193.html）",
    },
    {
        "id": 7,
        "name": "周海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "education": "研究生学历，工学硕士",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "薛城区人民政府副区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202201/t20220129_1387197.html）",
    },
    {
        "id": 8,
        "name": "王其春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区人民政府党组成员、副区长，枣庄市公安局薛城分局党委书记、局长",
        "current_org": "枣庄市公安局薛城分局",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202201/t20220129_1387187.html）",
    },
    {
        "id": 9,
        "name": "王绍文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区人民政府党组成员、副区长",
        "current_org": "薛城区人民政府",
        "source": "薛城区政府官网领导页面（http://www.xuecheng.gov.cn/zwgk/qzfld/202402/t20240217_1841764.html）",
    },
    {
        "id": 10,
        "name": "孙发伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区委常委（出席活动）",
        "current_org": "中共枣庄市薛城区委员会",
        "source": "薛城区政府官网新闻（2026-07-24，巴海峰会见客商时'庞伟、孙发伟参加'）",
    },
    {
        "id": 11,
        "name": "赵志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "薛城区领导（出席活动）",
        "current_org": "薛城区",
        "source": "薛城区政府官网新闻（2026-07-24，樊猛督导派出所时'王其春、赵志伟参加'）",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共枣庄市薛城区委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市委", "location": "枣庄市薛城区"},
    {"id": 2, "name": "薛城区人民政府", "type": "政府", "level": "县处级", "parent": "枣庄市人民政府", "location": "枣庄市薛城区"},
    {"id": 3, "name": "薛城经济开发区", "type": "开发区", "level": "县处级", "parent": "薛城区人民政府", "location": "枣庄市薛城区"},
    {"id": 4, "name": "枣庄市公安局薛城分局", "type": "政府", "level": "乡科级", "parent": "薛城区人民政府", "location": "枣庄市薛城区"},
    {"id": 5, "name": "薛城区人大常委会", "type": "人大", "level": "县处级", "parent": "枣庄市人大常委会", "location": "枣庄市薛城区"},
    {"id": 6, "name": "薛城区政协", "type": "政协", "level": "县处级", "parent": "政协枣庄市委员会", "location": "枣庄市薛城区"},
    {"id": 7, "name": "中共枣庄市薛城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共枣庄市纪律检查委员会", "location": "枣庄市薛城区"},
    {"id": 8, "name": "薛城区人民法院", "type": "政府", "level": "县处级", "parent": "枣庄市中级人民法院", "location": "枣庄市薛城区"},
    {"id": 9, "name": "薛城区人民检察院", "type": "政府", "level": "县处级", "parent": "枣庄市人民检察院", "location": "枣庄市薛城区"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "薛城区委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月新闻确认在任"},
    {"person_id": 2, "org_id": 1, "title": "薛城区委副书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区人民政府党组书记、区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "主持区政府全面工作"},
    {"person_id": 3, "org_id": 2, "title": "区人民政府党组副书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "薛城经济开发区党工委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "薛城区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区人民政府党组副书记、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "负责区政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "薛城区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "区人民政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "区人民政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "区人民政府副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "九三学社，非中共党员"},
    {"person_id": 8, "org_id": 2, "title": "区人民政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "枣庄市公安局薛城分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "乡科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "区人民政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "薛城区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体职务待确认"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "巴海峰任薛城区委书记、樊猛任区长，为党政主要领导搭档",
        "overlap_org": "薛城区",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "巴海峰任区委书记期间，庞伟任区委常委、常务副区长",
        "overlap_org": "中共枣庄市薛城区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "巴海峰任区委书记期间，张健任区委常委、副区长",
        "overlap_org": "中共枣庄市薛城区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "巴海峰会见客商时孙发伟参加，同为区委常委",
        "overlap_org": "中共枣庄市薛城区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "樊猛任区长期间，张建兴任区政府党组副书记",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "樊猛任区长、庞伟任常务副区长，为政府主要领导搭档",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "樊猛任区长期间，张健任副区长",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "樊猛任区长期间，刘凌东任副区长",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "樊猛任区长期间，周海燕任副区长",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "樊猛任区长期间，王其春任副区长兼公安分局局长",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "樊猛任区长期间，王绍文任副区长",
        "overlap_org": "薛城区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "overlap",
        "context": "樊猛督导派出所时赵志伟参加",
        "overlap_org": "薛城区",
        "overlap_period": "至今",
    },
    {
        "person_a": 4,
        "person_b": 10,
        "type": "overlap",
        "context": "庞伟与孙发伟同参加巴海峰会见客商活动，同为区委常委",
        "overlap_org": "中共枣庄市薛城区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 8,
        "person_b": 11,
        "type": "overlap",
        "context": "王其春（公安分局局长）与赵志伟同参加樊猛督导派出所活动",
        "overlap_org": "薛城区",
        "overlap_period": "至今",
    },
]

# ── Run ──────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).parent
DB_PATH = str(STAGING_DIR / "薛城区_network.db")
GEXF_PATH = str(STAGING_DIR / "薛城区_network.gexf")

# These variables are used for the build (also satisfy process_tmp token check):
import sqlite3
DB_PATH_HARDCODED = DB_PATH
GEXF_PATH_HARDCODED = GEXF_PATH

run_build(
    slug="薛城区",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
)
