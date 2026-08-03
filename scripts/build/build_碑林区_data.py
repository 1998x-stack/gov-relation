#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 碑林区, 西安市, 陕西省.

Investigation date: 2026-08-03
Task ID: shaanxi_碑林区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 碑林区人民政府官方网站 (www.beilin.gov.cn) — confirmed current leadership resumes
  - 百度百科—碑林区词条 (baike.baidu.com) — 主要领导表确认
  - 百度百科—刘其智词条 (baike.baidu.com) — 前任区委书记完整履历

Confidence notes:
  - 区政府领导（7人）姓名、职务、分工、简历全部在政府网站确认 (2026-06-01更新)
  - 区委书记张帆姓名和职务通过百度百科碑林区词条确认，详细履历待查
  - 区人大常委会主任周振强、区政协主席陈红利通过百度百科确认
  - 前任区委书记刘其智履历通过百度百科完整确认
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "碑林区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data — persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # 1: 张帆 — 区委书记
    {
        "id": 1,
        "name": "张帆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西安市碑林区委员会",
        "source": "https://baike.baidu.com/item/%E7%A2%91%E6%9E%97%E5%8C%BA/10703311",
    },
    # 2: 乔建宏 — 区委副书记、区长
    {
        "id": 2,
        "name": "乔建宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/qjh/1.html",
    },
    # 3: 黄华 — 区委常委、副区长（正区局级）
    {
        "id": 3,
        "name": "黄华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长（正区局级）",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/hh/1.html",
    },
    # 4: 张武 — 副区长
    {
        "id": 4,
        "name": "张武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/zw/1.html",
    },
    # 5: 王菲 — 副区长
    {
        "id": 5,
        "name": "王菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "",
        "education": "研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/wf/1.html",
    },
    # 6: 董晓楠 — 副区长
    {
        "id": 6,
        "name": "董晓楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/dxn/1.html",
    },
    # 7: 董鹏 — 副区长
    {
        "id": 7,
        "name": "董鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "西安市碑林区人民政府",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/dp/1.html",
    },
    # 8: 李鹏 — 副区长、公安碑林分局局长
    {
        "id": 8,
        "name": "李鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "education": "研究生，教育学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长，市公安局碑林分局局长、督察长",
        "current_org": "西安市公安局碑林分局",
        "source": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/lp/1.html",
    },
    # 9: 周振强 — 区人大常委会主任
    {
        "id": 9,
        "name": "周振强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "西安市碑林区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E7%A2%91%E6%9E%97%E5%8C%BA/10703311",
    },
    # 10: 陈红利 — 区政协主席
    {
        "id": 10,
        "name": "陈红利",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议西安市碑林区委员会",
        "source": "https://baike.baidu.com/item/%E7%A2%91%E6%9E%97%E5%8C%BA/10703311",
    },
    # 11: 刘其智 — 前任区委书记（2018-2023）
    {
        "id": 11,
        "name": "刘其智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年8月",
        "birthplace": "重庆巫溪",
        "education": "研究生，管理学博士",
        "party_join": "1992年5月",
        "work_start": "1990年7月",
        "current_post": "宝鸡市政协党组书记、主席",
        "current_org": "中国人民政治协商会议宝鸡市委员会",
        "source": "https://baike.baidu.com/item/%E5%88%98%E5%85%B6%E6%99%BA/6477465",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Data — organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共西安市碑林区委员会", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市碑林区"},
    {"id": 2, "name": "西安市碑林区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市碑林区"},
    {"id": 3, "name": "中共西安市碑林区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共西安市碑林区委员会", "location": "西安市碑林区"},
    {"id": 4, "name": "西安市碑林区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "西安市人大常委会", "location": "西安市碑林区"},
    {"id": 5, "name": "中国人民政治协商会议西安市碑林区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议西安市委员会", "location": "西安市碑林区"},
    {"id": 6, "name": "西安市公安局碑林分局", "type": "政府", "level": "县处级", "parent": "西安市公安局", "location": "西安市碑林区"},
    {"id": 7, "name": "中共西安市城市管理局党组", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市"},
    {"id": 8, "name": "西安市城市管理局（城市管理综合行政执法局）", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市"},
    {"id": 9, "name": "西北工业大学", "type": "事业单位", "level": "正厅级", "parent": "工业和信息化部", "location": "西安市"},
    {"id": 10, "name": "中共西安市莲湖区委员会", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市莲湖区"},
    {"id": 11, "name": "西安市莲湖区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市莲湖区"},
    {"id": 12, "name": "中共西安市长安区委员会", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市长安区"},
    {"id": 13, "name": "西安市长安区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市长安区"},
    {"id": 14, "name": "中共西安市灞桥区委员会", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市灞桥区"},
    {"id": 15, "name": "西安市雁塔区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市雁塔区"},
    {"id": 16, "name": "政协宝鸡市委员会", "type": "政协", "level": "地厅级", "parent": "政协陕西省委员会", "location": "宝鸡市"},
    # Historic orgs for 黄华 (from 延安)
    {"id": 17, "name": "陕西省志丹县人民政府", "type": "政府", "level": "县处级", "parent": "延安市人民政府", "location": "延安市志丹县"},
    {"id": 18, "name": "共青团延安市委", "type": "群团", "level": "县处级", "parent": "共青团陕西省委", "location": "延安市"},
    {"id": 19, "name": "中共延川县委员会", "type": "党委", "level": "县处级", "parent": "中共延安市委", "location": "延安市延川县"},
    {"id": 20, "name": "共青团陕西省委", "type": "群团", "level": "地厅级", "parent": "共青团中央", "location": "西安市"},
    # Historic for 张武
    {"id": 21, "name": "西安浐河开发区管委会", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市灞桥区"},
    {"id": 22, "name": "西安市灞桥区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市灞桥区"},
    # Historic for 王菲
    {"id": 23, "name": "西安市文物局", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市"},
    {"id": 24, "name": "西安大兴新区（土门地区）管委会", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市莲湖区"},
    {"id": 25, "name": "西安市莲湖区文化和旅游体育局", "type": "政府", "level": "县处级", "parent": "莲湖区人民政府", "location": "西安市莲湖区"},
    # Historic for 董晓楠
    {"id": 26, "name": "中共西安市雁塔区委员会", "type": "党委", "level": "县处级", "parent": "中共西安市委", "location": "西安市雁塔区"},
    # Historic for 董鹏 (from 未央区)
    {"id": 27, "name": "西安市未央区人民政府", "type": "政府", "level": "县处级", "parent": "西安市人民政府", "location": "西安市未央区"},
    # Historic for 李鹏 (公安系统)
    {"id": 28, "name": "陕西省人民警察培训学校", "type": "事业单位", "level": "", "parent": "陕西省公安厅", "location": "西安市"},
    {"id": 29, "name": "西安市公安局", "type": "政府", "level": "副厅级", "parent": "陕西省公安厅", "location": "西安市"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Data — positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 张帆 (id=1) ──
    {"person_id": 1, "org_id": 1, "title": "碑林区委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},

    # ── 乔建宏 (id=2) ──
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区政府党组书记、区长", "start_date": "", "end_date": "present", "rank": "", "note": "领导区政府全面工作，分管财政局、审计局"},
    {"person_id": 2, "org_id": 1, "title": "碑林区委常委", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "碑林区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长安区委常委", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长安区郭杜街道党工委书记、人大工委主任", "start_date": "", "end_date": "", "rank": "", "note": "兼西安郭杜教育科技产业开发区管委会党组书记、副主任"},
    {"person_id": 2, "org_id": 12, "title": "长安区王曲街道党工委书记、人大工委主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "长安区五星街道党工委副书记、办事处主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "长安区郭杜街道办事处副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 黄华 (id=3) ──
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府党组成员、副区长（正区局级）", "start_date": "", "end_date": "present", "rank": "", "note": "负责发改、人社、应急、营商环境、税务、消防"},
    {"person_id": 3, "org_id": 20, "title": "共青团陕西省委副书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 19, "title": "延川县委副书记（正处级）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 18, "title": "共青团延安市委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 17, "title": "志丹县副县长", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 张武 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "区政府副区长", "start_date": "", "end_date": "present", "rank": "", "note": "负责商贸、国资监管、市场监管、数据、生态环境"},
    {"person_id": 4, "org_id": 15, "title": "雁塔区副区长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 4, "org_id": 21, "title": "西安浐河开发区管委会主任兼洪庆工业园区管委会主任", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 王菲 (id=5) ──
    {"person_id": 5, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "", "note": "负责教育、科技、环大学创新产业带、文旅"},
    {"person_id": 5, "org_id": 23, "title": "西安市文物局党组成员、副局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 25, "title": "莲湖区文化和旅游体育局党组书记、局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 24, "title": "西安大兴新区（土门地区）管委会招商局副局长", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 董晓楠 (id=6) ──
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "", "note": "负责民宗、民政、招商引资、卫健、医保"},
    {"person_id": 6, "org_id": 26, "title": "雁塔区电子城街道党工委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 15, "title": "雁塔区电子城街道党工委副书记、办事处主任", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 董鹏 (id=7) ──
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "", "end_date": "present", "rank": "", "note": "负责城建、住房保障、旧城改造、城市治理"},
    {"person_id": 7, "org_id": 27, "title": "未央区住房和城市建设局党委书记、局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 27, "title": "未央区六村堡街道党工委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 李鹏 (id=8) ──
    {"person_id": 8, "org_id": 2, "title": "区政府党组成员、副区长，市公安局碑林分局局长、督察长", "start_date": "", "end_date": "present", "rank": "", "note": "负责公安、司法、退役军人、信访"},
    {"person_id": 8, "org_id": 29, "title": "市公安局办公室主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 29, "title": "市公安局团委书记", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 28, "title": "省人民警察培训学校办公室主任", "start_date": "", "end_date": "", "rank": "", "note": ""},

    # ── 周振强 (id=9) ──
    {"person_id": 9, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "", "note": ""},

    # ── 陈红利 (id=10) ──
    {"person_id": 10, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "", "note": ""},

    # ── 刘其智 (id=11) ──
    {"person_id": 11, "org_id": 16, "title": "宝鸡市政协党组书记、主席", "start_date": "2024-02", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "碑林区委书记", "start_date": "2018-04", "end_date": "2023-12", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "西安市城市管理局（城市管理综合行政执法局）局长、党组书记", "start_date": "2017-04", "end_date": "2018-04", "rank": "", "note": ""},
    {"person_id": 11, "org_id": 14, "title": "灞桥区委副书记", "start_date": "2016-03", "end_date": "2017-04", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 14, "title": "灞桥区委常委、副区长", "start_date": "2010-12", "end_date": "2016-03", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "莲湖区副区长", "start_date": "2002-12", "end_date": "2010-12", "rank": "副厅级", "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Data — relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "张帆接替刘其智担任碑林区委书记", "overlap_org": "中共西安市碑林区委员会", "overlap_period": "2024"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "张帆为区委书记，乔建宏为区长", "overlap_org": "中共西安市碑林区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "乔建宏为区长，黄华为常务副区长", "overlap_org": "西安市碑林区人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 2, "type": "overlap", "context": "刘其智为碑林区委书记时与乔建宏搭班", "overlap_org": "中共西安市碑林区委员会", "overlap_period": ""},
    {"person_a": 11, "person_b": 3, "type": "overlap", "context": "刘其智为碑林区委书记时与黄华搭班", "overlap_org": "中共西安市碑林区委员会", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def build_person_qiao():
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省", "city": "西安市", "region": "碑林区",
            "job": "区长", "task_id": "shaanxi_碑林区", "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": "beilin_qiao_jianhong", "name": "乔建宏", "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "1974年11月", "birthplace": "",
            "native_place": "", "party_join": "", "work_start": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "大学", "study_type": "unknown", "source_ids": ["S001"]}],
            "dedupe_keys": {"name_birth": "乔建宏_197411", "name_birthplace": "", "official_profile_url": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/qjh/1.html"}
        },
        "current_status": {
            "current_post": "区委副书记、区政府党组书记、区长", "current_org": "西安市碑林区人民政府",
            "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]
        },
        "career_timeline": [
            {"start": "", "end": "", "org": "西安市长安区郭杜街道办事处", "title": "副主任", "system": "government", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "长安区五星街道", "title": "党工委副书记、办事处主任", "system": "party", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "长安区王曲街道", "title": "党工委书记、人大工委主任", "system": "party", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "长安区郭杜街道", "title": "党工委书记、人大工委主任", "system": "party", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "西安郭杜教育科技产业开发区管委会", "title": "党组书记、副主任（兼）", "system": "government", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "长安区委", "title": "区委常委", "system": "party", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "", "org": "碑林区委", "title": "区委常委、常务副区长", "system": "party", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "", "end": "present", "org": "碑林区委/区政府", "title": "区委副书记、区政府党组书记、区长", "system": "government", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "relationships": [
            {"person": "张帆", "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "区委书记和区长搭班", "overlap_org": "中共西安市碑林区委员会",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "黄华", "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "区长和常务副区长搭班", "overlap_org": "西安市碑林区人民政府",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "source_register": [
            {"id": "S001", "title": "乔建宏-碑林区领导之窗", "url": "https://www.beilin.gov.cn/zwgk/fdzdgk/ldzc/qjh/1.html",
             "source_type": "official", "reliability": "high", "accessed_at": AS_OF},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "biggest_gap": "各任期具体开始、结束日期"},
        "open_questions": [{"priority": "medium", "question": "乔建宏在长安区和碑林区各职务的具体任职时段", "why_it_matters": "完善时间线", "suggested_queries": ["乔建宏 碑林区委组织部 任免"], "last_attempted": AS_OF}]
    }

def build_person_liu():
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省", "city": "西安市", "region": "碑林区",
            "job": "前任区委书记", "task_id": "shaanxi_碑林区", "time_focus": "2018-2023"
        },
        "identity": {
            "name": "刘其智", "person_id": "beilin_liu_qizhi", "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "1969年8月", "birthplace": "重庆巫溪", "native_place": "重庆",
            "party_join": "1992年5月", "work_start": "1990年7月",
            "education": [{"period": "", "institution": "西安交通大学", "major": "管理科学与工程", "degree": "管理学博士", "study_type": "part_time", "source_ids": ["S002"]}],
            "dedupe_keys": {"name_birth": "刘其智_196908", "name_birthplace": "刘其智_重庆巫溪", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "宝鸡市政协党组书记、主席", "current_org": "政协宝鸡市委员会",
            "administrative_rank": "正厅级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S002"]
        },
        "career_timeline": [
            {"start": "1990-07", "end": "1994-07", "org": "西北工业大学管理学院", "title": "辅导员、团工委书记", "system": "education", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "1994-07", "end": "1996-01", "org": "西北工业大学党委办公室", "title": "秘书", "system": "education", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "1996-01", "end": "1997-04", "org": "西北工业大学", "title": "党委研究生工作部副部长兼研究生院管理处副处长", "system": "education", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "1997-04", "end": "2001-12", "org": "西北工业大学", "title": "党委办公室副主任", "system": "education", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2001-12", "end": "2002-07", "org": "西北工业大学", "title": "党政办公室副主任", "system": "education", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2002-07", "end": "2002-12", "org": "西北工业大学", "title": "党委学生工作部部长、学生处处长、人武部部长", "system": "education", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2002-12", "end": "2010-12", "org": "西安市莲湖区", "title": "副区长", "system": "government", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2010-12", "end": "2016-03", "org": "西安市灞桥区", "title": "区委常委、副区长", "system": "government", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2016-03", "end": "2017-04", "org": "西安市灞桥区", "title": "区委副书记", "system": "party", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2017-04", "end": "2018-04", "org": "西安市城市管理局", "title": "局长、党组书记", "system": "government", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2018-04", "end": "2023-12", "org": "西安市碑林区", "title": "区委书记", "system": "party", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2024-01", "end": "2024-02", "org": "宝鸡市政协", "title": "党组书记", "system": "other", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2024-02", "end": "present", "org": "宝鸡市政协", "title": "党组书记、主席", "system": "other", "is_key_promotion": True, "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "relationships": [
            {"person": "张帆", "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "张帆接替刘其智担任碑林区委书记", "overlap_org": "中共西安市碑林区委员会",
             "overlap_period": "2024", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "乔建宏", "relationship_type": "overlap", "strength": "medium",
             "evidence": "刘其智在碑林区委书记任上，乔建宏曾任碑林区委常委、常务副区长",
             "overlap_org": "中共西安市碑林区委员会", "overlap_period": "",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {
            "primary_specializations": ["高校行政管理", "城市管理", "区委领导"],
            "career_pattern": "高校→西安市区政府→区委→市局→区委书记→市政协",
            "systems_experience": ["education", "government", "party"],
            "geographic_pattern": ["重庆→西安→宝鸡"],
            "promotion_velocity": {"summary": "高校系统深耕12年后转入地方政府，稳步晋升", "notable_fast_promotions": []}
        },
        "risk_and_integrity_signals": [{"type": "none_found", "description": "公开信息无纪检处分记录", "date": "", "confidence": "confirmed"}],
        "source_register": [
            {"id": "S002", "title": "刘其智-百度百科", "url": "https://baike.baidu.com/item/%E5%88%98%E5%85%B6%E6%99%BA/6477465",
             "source_type": "encyclopedia", "reliability": "medium", "accessed_at": AS_OF},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete", "biggest_gap": ""},
        "open_questions": []
    }

def build_person_zhangfan():
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省", "city": "西安市", "region": "碑林区",
            "job": "区委书记", "task_id": "shaanxi_碑林区", "time_focus": "2024-present"
        },
        "identity": {
            "person_id": "beilin_zhang_fan", "name": "张帆", "aliases": [],
            "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
            "education": [], "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "碑林区委书记", "current_org": "中共西安市碑林区委员会",
            "administrative_rank": "正厅级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S003"]
        },
        "career_timeline": [
            {"start": "unknown", "end": "2023-12", "org": "未知", "title": "",
             "notes": "全部履历待查——公开资料未找到任何职业生涯记录", "confidence": "unverified"},
            {"start": "2024-01", "end": "present", "org": "中共西安市碑林区委员会", "title": "碑林区委书记",
             "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "organizations": [],
        "relationships": [
            {"person": "乔建宏", "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "区委书记和区长搭班", "overlap_org": "中共西安市碑林区委员会",
             "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "刘其智", "relationship_type": "predecessor_successor", "strength": "strong",
             "evidence": "接替刘其智", "overlap_org": "中共西安市碑林区委员会",
             "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "risk_and_integrity_signals": [{"type": "none_found", "description": "公开资料极少", "confidence": "unverified"}],
        "source_register": [
            {"id": "S003", "title": "百度百科-碑林区词条", "url": "https://baike.baidu.com/item/%E7%A2%91%E6%9E%97%E5%8C%BA/10703311",
             "source_type": "encyclopedia", "reliability": "medium", "accessed_at": AS_OF, "notes": "确认张帆为碑林区委书记"},
        ],
        "confidence_summary": {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "biggest_gap": "全部履历"},
        "open_questions": [{"priority": "critical", "question": "张帆在担任碑林区委书记前的完整履历（出生、教育、所有职务）", "why_it_matters": "区委书记是关系网核心人物", "suggested_queries": ["张帆 碑林区委书记 简历", "张帆 任前公示 西安", "张帆 西安市委 任职"], "last_attempted": AS_OF}]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print("=" * 60)

    # 1. Build SQLite DB + GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

# 2. Write person JSONs
    for filename, builder in [
        (f"{TODAY}-陕西省-西安市-区长-乔建宏.json", build_person_qiao),
        (f"{TODAY}-陕西省-西安市-前任区委书记-刘其智.json", build_person_liu),
        (f"{TODAY}-陕西省-西安市-区委书记-张帆.json", build_person_zhangfan),
    ]:
        path = STAGING_DIR / filename
        data = builder()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] Person JSON: {path}")

    print(f"\nDone. Files in {STAGING_DIR}:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")


if __name__ == "__main__":
    main()