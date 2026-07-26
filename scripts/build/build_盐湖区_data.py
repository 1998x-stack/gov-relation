#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 盐湖区 (Yanhu District), 运城市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_盐湖区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.yanhu.gov.cn — 运城市盐湖区人民政府官方网站 (primary, current as of July 2026)
  - www.yanhu.gov.cn/ldzc/qwld/index.shtml — 区委领导 page (confirmed)
  - www.yanhu.gov.cn/ldzc/qzfld/index.shtml — 区政府领导 page (confirmed)

Confidence notes:
  - Current roles/names/birth/education: confirmed via official leadership pages
  - Full career timelines (prior positions): unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in range(1, 6):
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break

SLUG = "盐湖区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# Staging paths
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3=副书记, 4=纪委书记, 5=常务副区长
#      6=统战部长, 7=政法委书记, 8=宣传部长, 9=人武部政委,
#      10=组织部长, 11=副区长(常委), 12=区委办公室主任,
#      13=副区长(公安), 14=副区长(卫健/环境), 15=副区长(城建),
#      16=副区长(农业/教育), 17=副区长(工业/商务),
#      18=二级调研员, 19=政府办主任
#      20=人大主任, 21=政协主席
#      21-33: 区人大/政协领导

persons = [
    # ===== 区委领导 =====
    {
        "id": 1, "name": "李永辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-08", "birthplace": "", "education": "中央党校研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委书记", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 2, "name": "武鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-06", "birthplace": "", "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 3, "name": "卢静", "gender": "女", "ethnicity": "汉族",
        "birth": "1979-10", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、运城中学党委书记", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 4, "name": "张晓波", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-09", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任", "current_org": "中共运城市盐湖区纪律检查委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 5, "name": "王军", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-02", "birthplace": "", "education": "省委党校研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区政府党组副书记、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 6, "name": "郭亚明", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-09", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、统战部部长", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 7, "name": "杨建帮", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-01", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、政法委书记", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 8, "name": "王大风", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-07", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、宣传部部长", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 9, "name": "板海静", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-02", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、人武部政委", "current_org": "运城市盐湖区人武部",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 10, "name": "秦盛华", "gender": "女", "ethnicity": "汉族",
        "birth": "1986-02", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、组织部部长、区委党校校长", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 11, "name": "郑冬", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-12", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 12, "name": "李宝拴", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-08", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区委办公室主任", "current_org": "中共运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    # ===== 区政府领导 =====
    {
        "id": 13, "name": "秦浩", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-10", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副区长、市公安局盐湖分局局长", "current_org": "运城市公安局盐湖分局",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 14, "name": "穆首翔", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-07", "birthplace": "", "education": "在职研究生学历",
        "party_join": "", "work_start": "",
        "current_post": "区政府党组成员、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 15, "name": "王坚强", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-10", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "", "work_start": "",
        "current_post": "区政府党组成员、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 16, "name": "李娟", "gender": "女", "ethnicity": "汉族",
        "birth": "1983-10", "birthplace": "", "education": "大学学历",
        "party_join": "", "work_start": "",
        "current_post": "区政府党组成员、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 17, "name": "高超", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-04", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府党组成员、副区长", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 18, "name": "薛国鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-01", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府二级调研员", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 19, "name": "程国良", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-05", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府党组成员、区政府办公室主任", "current_org": "盐湖区人民政府",
        "source": "yanhu.gov.cn"
    },
    # ===== 区人大领导 =====
    {
        "id": 20, "name": "张军", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-05", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组书记、主任", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 21, "name": "李金果", "gender": "女", "ethnicity": "汉族",
        "birth": "1967-12", "birthplace": "", "education": "大学学历",
        "party_join": "民建会员", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 22, "name": "雷云峰", "gender": "男", "ethnicity": "汉族",
        "birth": "1967-11", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组成员、副主任", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 23, "name": "赵洪波", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-05", "birthplace": "", "education": "大专学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组成员、副主任", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 24, "name": "周鸿", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-08", "birthplace": "", "education": "大专学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组成员、副主任", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 25, "name": "薛世鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-02", "birthplace": "", "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区人大常委会党组成员、秘书长", "current_org": "盐湖区人民代表大会常务委员会",
        "source": "yanhu.gov.cn"
    },
    # ===== 区政协领导 =====
    {
        "id": 26, "name": "宁华文", "gender": "男", "ethnicity": "汉族",
        "birth": "1967-04", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协主席", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 27, "name": "李锐", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-04", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组书记", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 28, "name": "马红琴", "gender": "女", "ethnicity": "汉族",
        "birth": "1967-07", "birthplace": "", "education": "大学学历",
        "party_join": "民盟盟员", "work_start": "",
        "current_post": "区政协副主席、民盟盐湖区委主委", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 29, "name": "麻芙蓉", "gender": "女", "ethnicity": "汉族",
        "birth": "1973-04", "birthplace": "", "education": "大学学历",
        "party_join": "民革党员", "work_start": "",
        "current_post": "区政协副主席", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 30, "name": "卫晓军", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-08", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组成员、副主席", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 31, "name": "卫开河", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-03", "birthplace": "", "education": "中央党校大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组成员、副主席", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
    {
        "id": 32, "name": "戈米", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-09", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协党组成员、秘书长", "current_org": "中国人民政治协商会议运城市盐湖区委员会",
        "source": "yanhu.gov.cn"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共运城市盐湖区委员会", "type": "党委", "level": "县处级", "parent": "中共运城市委员会", "location": "山西省运城市盐湖区"},
    {"id": 2, "name": "盐湖区人民政府", "type": "政府", "level": "县处级", "parent": "运城市人民政府", "location": "山西省运城市盐湖区"},
    {"id": 3, "name": "中共运城市盐湖区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共运城市盐湖区委员会", "location": "山西省运城市盐湖区"},
    {"id": 4, "name": "运城市公安局盐湖分局", "type": "政府", "level": "乡科级", "parent": "盐湖区人民政府", "location": "山西省运城市盐湖区"},
    {"id": 5, "name": "运城市盐湖区人武部", "type": "军队", "level": "县处级", "parent": "运城军分区", "location": "山西省运城市盐湖区"},
    {"id": 6, "name": "运城中学", "type": "事业单位", "level": "乡科级", "parent": "盐湖区人民政府", "location": "山西省运城市盐湖区"},
    {"id": 7, "name": "盐湖区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "山西省运城市盐湖区"},
    {"id": 8, "name": "中国人民政治协商会议运城市盐湖区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "山西省运城市盐湖区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 区委领导
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "区委一把手"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "区政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "运城中学党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "兼任"},
    {"person_id": 4, "org_id": 3, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "区政府党组副书记、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "常务副区长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "人武部政委", "start_date": "", "end_date": "", "rank": "正团级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼"},
    {"person_id": 10, "org_id": 1, "title": "区委常委、组织部部长、区委党校校长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "区委常委、区委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 区政府领导
    {"person_id": 13, "org_id": 4, "title": "副区长、市公安局盐湖分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 18, "org_id": 2, "title": "区政府二级调研员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "区政府党组成员、区政府办公室主任", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},

    # 区人大领导
    {"person_id": 20, "org_id": 7, "title": "区人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 7, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "民建"},
    {"person_id": 22, "org_id": 7, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 7, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 7, "title": "区人大常委会秘书长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},

    # 区政协领导
    {"person_id": 26, "org_id": 8, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 27, "org_id": 8, "title": "区政协党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 28, "org_id": 8, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "民盟"},
    {"person_id": 29, "org_id": 8, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "民革"},
    {"person_id": 30, "org_id": 8, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 31, "org_id": 8, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 32, "org_id": 8, "title": "区政协秘书长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "领导_副手", "context": "区委书记与区长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    # 区委书记与副书记
    {"person_a": 1, "person_b": 3, "type": "领导_副手", "context": "区委书记与区委副书记", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    # 区委书记与其他常委
    {"person_a": 1, "person_b": 4, "type": "领导_副手", "context": "区委书记与纪委书记", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "领导_副手", "context": "区委书记与常务副区长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "领导_副手", "context": "区委书记与统战部长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "领导_副手", "context": "区委书记与政法委书记", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "领导_副手", "context": "区委书记与宣传部长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "领导_副手", "context": "区委书记与人武部政委", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "领导_副手", "context": "区委书记与组织部长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "领导_副手", "context": "区委书记与副区长(常委)", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "领导_副手", "context": "区委书记与区委办主任", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    # 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "领导_副手", "context": "区长与常务副区长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "领导_副手", "context": "区长与副区长(常委)", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "领导_副手", "context": "区长与公安局长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "领导_副手", "context": "区长与副区长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "领导_副手", "context": "区长与副区长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "领导_副手", "context": "区长与副区长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "领导_副手", "context": "区长与副区长", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 19, "type": "领导_副手", "context": "区长与政府办主任", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    # 常委之间
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "纪委书记与常务副区长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "纪委书记与政法委书记", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "同僚", "context": "常务副区长与组织部长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "同僚", "context": "常务副区长与副区长(常委)", "overlap_org": "盐湖区人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 13, "type": "工作关系", "context": "政法委书记与公安局长", "overlap_org": "", "overlap_period": ""},
    {"person_a": 10, "person_b": 3, "type": "同僚", "context": "组织部长与区委副书记", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "统战部长与宣传部长", "overlap_org": "中共运城市盐湖区委员会", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
#  Build functions
# ═════════════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "区委书记" in post and "前任" not in post:
        return ("255,50,50", 20.0)  # Red, top leader
    elif "区长" in post and "副" not in post and "前任" not in post:
        return ("50,100,255", 20.0)  # Blue
    elif "区委副书记" in post:
        return ("150,50,50", 15.0)
    elif "区政协主席" in post:
        return ("255,240,200", 15.0)
    elif "区人大常委会主任" in post:
        return ("200,255,255", 15.0)
    elif "人大常委会" in post and "主任" in post:
        return ("200,255,255", 12.0)
    elif "人大" in post:
        return ("200,255,255", 12.0)
    elif "纪委书记" in post:
        return ("255,165,0", 12.0)  # Orange
    elif "区委常委" in post or "区委" in post:
        return ("100,150,255", 12.0)
    elif "副区长" in post:
        return ("100,100,255", 12.0)
    elif "政协" in post:
        return ("255,240,200", 12.0)
    elif "前任" in post:
        return ("150,150,150", 10.0)
    else:
        return ("100,100,100", 12.0)


def org_color(typ):
    return {
        "党委": ("255,200,200"),
        "政府": ("200,200,255"),
        "人大": ("200,255,255"),
        "政协": ("255,240,200"),
        "纪委": ("255,200,200"),
        "军队": ("200,200,200"),
        "事业单位": ("220,220,220"),
    }.get(typ, ("200,200,200"))


def build_db():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")


def build_gexf():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")


def write_person_jsons():
    """Write person JSON files for core figures."""
    PERSONS_DIR = STAGING_DIR
    for p in persons:
        # Only write for top leaders and key figures
        if p["id"] in (1, 2, 3, 4, 5, 10, 7, 20, 26):
            job_slug = p["current_post"].replace("、", "_").replace("，", "_").replace("、", "_")
            filename = f"{TODAY}-山西省-运城市-{job_slug}-{p['name']}.json"
            path = PERSONS_DIR / filename
            data = {
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "山西省",
                    "city": "运城市",
                    "region": "盐湖区",
                    "job": p["current_post"],
                    "task_id": "shanxi_盐区",
                    "time_focus": "current as of 2026-07-26"
                },
                "identity": {
                    "person_id": f"yanhu_{p['name']}",
                    "name": p["name"],
                    "aliases": [],
                    "gender": p["gender"],
                    "ethnicity": p["ethnicity"],
                    "birth": p["birth"],
                    "birthplace": "",
                    "native_place": "",
                    "education": [{"period": "", "institution": "", "major": "", "degree": p["education"],
                                   "study_type": "unknown", "source_ids": ["S001"]}],
                    "party_join": p["party_join"],
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": f"{p['name']}_{p['birth']}",
                        "name_birthplace": f"{p['name']}_",
                        "official_profile_url": "http://www.yanhu.gov.cn/ldzc/qwld/index.shtml"
                    }
                },
                "current_status": {
                    "current_post": p["current_post"],
                    "current_org": p["current_org"],
                    "administrative_rank": "",
                    "as_of": "2026-07-26",
                    "is_current_confirmed": True,
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料未找到完整履历。仅有官方简历显示当前职务，升迁前经历未知。",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "无法判断 (缺少完整履历)", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "unknown",
                            "evidence": "暂未收集到足量的公开演讲、调研报道来判定工作风格",
                            "confidence": "unverified",
                            "source_ids": []
                        }
                    ],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "截至2026年7月，公开渠道未发现该贪腐调查或纪律处分记录",
                        "date": "",
                        "confidence": "unverified",
                        "source_ids": ["S001"]
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "盐湖区委领导之窗",
                        "url": "http://www.yanhu.gov.cn/ldzc/qwld/index.shtml",
                        "publisher": "运城市盐湖区人民政府",
                        "published_at": "",
                        "accessed_at": "2026-07-26",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "官方网站，其本简历涵盖当前职务、出生年月、性别、族别、学历"
                    },
                    {
                        "id": "S002",
                        "title": "盐湖区政府领导之窗",
                        "url": "http://www.yanhu.gov.cn/ldzc/qzfld/index.shtml",
                        "publisher": "运城市区人民政府",
                        "published_at": "",
                        "accessed_at": "2026-07-26",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "区政府领导相关信息，含职务分工"
                    }
                ],
                "confidence_summary": {
                    "identity": "confirmed",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "完整履历 (任职此前的升迁和担任职务)"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": f"{p['name']}的完整政治作息时间线是怎样？此次在此前担任过哪些职务？",
                        "why_it_matters": "缺少履历表，无法建立与其他官员的关系量化分析",
                        "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示", f"{p['name']} 历任"],
                        "last_attempted": "2026-07-26"
                    }
                ]
            }
            # Fix the syntax errors from the conditional above by just writing for all top figures
            with open(STAGING_DIR / filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  JSON: {filename}")


def write_main_person_json():
    """Write person JSON files for the two main targets."""
    core_ids = [1, 2]
    core_persons = [p for p in persons if p["id"] in core_ids]
    for p in core_persons:
        job_slug = p["current_post"].replace(" ", "_").replace("，", "_").replace("、", "_")
        filename = f"{TODAY}-山西省-运城区-{job_slug}-{p['name']}.json"
        path = STAGING_DIR / filename
        data = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "山西省",
                "city": "运城市",
                "region": "盐湖区",
                "job": p["current_post"],
                "task_id": "shanxi_盐区",
                "time_focus": "as of 2026-07-26"
            },
            "identity": {
                "person_id": f"yanhu_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p["gender"],
                "ethnicity": p["ethnicity"],
                "birth": p["birth"],
                "birthplace": "",
                "native_place": "",
                "education": [{"period": "", "institution": "", "major": "", "degree": p["education"],
                               "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": p["party_join"],
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p['birth']}",
                    "name_birthplace": f"{p['name']}_",
                    "official_profile_url": "http://www.yanhu.gov.cn/ldzc/qwld/index.shtml"
                }
            },
            "current_status": {
                "current_post": p["current_post"],
                "current_org": p["current_org"],
                "administrative_rank": "",
                "as_of": "2026-07-26",
                "is_current_confirmed": True,
                "source_refs": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": f"公开资料仅展示现任职务。{p['name']}此前的完整政治生涯未从官方渠道找到。",
                    "confidence": "unverified",
                    "source_refs": []
                }
            ],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "无法判定 — 缺少个人履历表",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "未收集到公开工作风格线索",
                        "confidence": "unverified",
                        "source_refs": []
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，公开渠道未发现纪律处分或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_refs": ["S001"]
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "盐湖区领导之窗 - 首页领导",
                    "url": "http://www.yanhu.gov.cn/ldzc/qwld/index.shtml",
                    "publisher": "运城市盐湖区人民政府",
                    "published_at": "",
                    "accessed_at": "2026-07-26",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "官方简历，包含姓名、性别、民族、出生年月、学历、党员身份、当前职务"
                },
                {
                    "id": "S002",
                    "title": "盐湖区政府领导之窗",
                    "url": "http://www.yanhu.gov.cn/ldzc/qzfld/index.shtml",
                    "publisher": "运城市盐湖区人民政府",
                    "published_at": "",
                    "accessed_at": "2026-07-26",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "区政府领导名单和责任分工"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的完整履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{p['name']}的完整政治履历是什么？",
                    "why_it_matters": "无完整履历，无法进行关系和绩效分析",
                    "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 历任职务", f"{p['name']} 任前公示"],
                    "last_attempted": "2026-07-26"
                }
            ]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")


# ═════════════════════════════════════════════════════════════════════════════
#  Main
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  个人信息来源: 运城市盐湖区人民政府官方网站 (yanhu.gov.cn)")
    print("=" * 60)

    print("\n--- Building SQLite database ---")
    build_db()

    print("\n--- Building GEXF graph ---")
    build_gexf()

    print("\n--- Writing person JSONs ---")
    write_main_person_json()

    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   DB: {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   Person JSONs in: {STAGING_DIR}/")