#!/usr/bin/env python3
"""Build script for 西安市莲湖区 cadre exchange network investigation."""

import json
import os
import sqlite3  # noqa: used indirectly via gov_relation.runner
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-08-03"

# Staging paths
STAGING = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING, "莲湖区_network.db")
GEXF_PATH = os.path.join(STAGING, "莲湖区_network.gexf")
PERSONS_DIR = os.path.join(STAGING, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================
# Sources:
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/dx/1.html (董旭)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/fq/1.html (傅强)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/cyh/1.html (陈晏辉)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/fj/1.html (符杰)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/mxj/1.html (马晓娟)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/2021152826163027969.html (区委全会: 马翔, 胡广乐, 区委常委)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/2034808059527225345.html (人代会: 胡广乐)
# - http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/2035904462711717890.html (人代会闭幕: 张营当选)
# =========================================================================

AS_OF_SHORT = AS_OF.replace("-", "")

# ── Persons ──

persons = [
    {
        "id": 1,
        "name": "马翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委书记",
        "current_org": "中共西安市莲湖区委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                   "2021152826163027969.html"),
    },
    {
        "id": 2,
        "name": "董旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-09",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莲湖区委副书记、区政府代区长",
        "current_org": "西安市莲湖区人民政府",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/dx/1.html"),
    },
    {
        "id": 3,
        "name": "胡广乐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区原区长（2026年上半年离任）",
        "current_org": "",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 4,
        "name": "尤骁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委副书记",
        "current_org": "中共西安市莲湖区委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2035904462711717890.html"),
    },
    {
        "id": 5,
        "name": "傅强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莲湖区委常委、区政府副区长、区政府党组成员",
        "current_org": "西安市莲湖区人民政府",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/fq/1.html"),
    },
    {
        "id": 6,
        "name": "周兴鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委、区纪委书记",
        "current_org": "中共西安市莲湖区纪律检查委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 7,
        "name": "缪宝辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委、区委政法委书记",
        "current_org": "中共西安市莲湖区委政法委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 8,
        "name": "王蓬勃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委、区委组织部部长",
        "current_org": "中共西安市莲湖区委组织部",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 9,
        "name": "孙广卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委",
        "current_org": "中共西安市莲湖区委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 10,
        "name": "武蓉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委、区委统战部部长",
        "current_org": "中共西安市莲湖区委统战部",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 11,
        "name": "王洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区委常委",
        "current_org": "中共西安市莲湖区委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 12,
        "name": "陈晏辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-03",
        "birthplace": "",
        "education": "大学，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莲湖区副区长、区政府党组成员",
        "current_org": "西安市莲湖区人民政府",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/cyh/1.html"),
    },
    {
        "id": 13,
        "name": "符杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莲湖区副区长、区政府党组成员，公安莲湖分局局长",
        "current_org": "西安市莲湖区人民政府",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/fj/1.html"),
    },
    {
        "id": 14,
        "name": "马晓娟",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1977-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莲湖区副区长、区政府党组成员、北院门街道党工委书记",
        "current_org": "西安市莲湖区人民政府",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/ldxx/mxj/1.html"),
    },
    {
        "id": 15,
        "name": "张营",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区人大常委会主任",
        "current_org": "西安市莲湖区人民代表大会常务委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2035904462711717890.html"),
    },
    {
        "id": 16,
        "name": "刘永毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区人大常委会原主任",
        "current_org": "西安市莲湖区人民代表大会常务委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2021152826163027969.html"),
    },
    {
        "id": 17,
        "name": "上官拥军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莲湖区政协主席",
        "current_org": "中国人民政治协商会议西安市莲湖区委员会",
        "source": ("http://www.lianhu.gov.cn/zwgk/jcxxgk/zyhy/zthy/"
                  "2034470395327901698.html"),
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共西安市莲湖区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委员会",
        "location": "西安市莲湖区",
    },
    {
        "id": 2,
        "name": "西安市莲湖区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市莲湖区",
    },
    {
        "id": 3,
        "name": "中共西安市莲湖区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市纪律检查委员会",
        "location": "西安市莲湖区",
    },
    {
        "id": 4,
        "name": "中共西安市莲湖区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委政法委员会",
        "location": "西安市莲湖区",
    },
    {
        "id": 5,
        "name": "中共西安市莲湖区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委组织部",
        "location": "西安市莲湖区",
    },
    {
        "id": 6,
        "name": "中共西安市莲湖区委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委统战部",
        "location": "西安市莲湖区",
    },
    {
        "id": 7,
        "name": "西安市公安局莲湖分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安市公安局",
        "location": "西安市莲湖区",
    },
    {
        "id": 8,
        "name": "西安市莲湖区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "西安市人民代表大会常务委员会",
        "location": "西安市莲湖区",
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议西安市莲湖区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议西安市委员会",
        "location": "西安市莲湖区",
    },
    {
        "id": 10,
        "name": "西安市未央区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市未央区",
    },
    {
        "id": 11,
        "name": "西安市新城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市新城区",
    },
    {
        "id": 12,
        "name": "西安市公安局新城分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安市公安局",
        "location": "西安市新城区",
    },
    {
        "id": 13,
        "name": "西安市公安局站前分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安市公安局",
        "location": "西安市新城区",
    },
    {
        "id": 14,
        "name": "西安市自然资源和规划局",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市",
    },
    {
        "id": 15,
        "name": "西安电子科技大学",
        "type": "事业单位",
        "level": "厅局级",
        "parent": "教育部",
        "location": "西安市",
    },
    {
        "id": 16,
        "name": "莲湖区北院门街道党工委",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共西安市莲湖区委员会",
        "location": "西安市莲湖区北院门街道",
    },
]

# ── Positions ──

positions = [
    # 马翔 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "莲湖区委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "区委常委会主持，区委十四届十次全会（2026年2月）"},

    # 董旭 — 代区长
    {"person_id": 2, "org_id": 1, "title": "莲湖区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026年7月任代区长"},  # Updated from 区政府领导页面
    {"person_id": 2, "org_id": 2, "title": "莲湖区代区长",
     "start_date": "2026-07", "end_date": "present", "rank": "县处级正职",
     "note": "2026年7月任代区长，此前为常务副区长"},
    {"person_id": 2, "org_id": 2, "title": "莲湖区委常委、区政府常务副区长",
     "start_date": "", "end_date": "2026-06", "rank": "县处级副职",
     "note": "晋升代区长前任此职"},
    {"person_id": 2, "org_id": 10, "title": "未央区住建局副局长、草滩街道办主任/书记、区委办主任",
     "start_date": "", "end_date": "", "rank": "",
     "note": "赴莲湖区任职前在未央区工作的履历"},

    # 胡广乐 — 原区长
    {"person_id": 3, "org_id": 2, "title": "莲湖区区长",
     "start_date": "", "end_date": "2026-06", "rank": "县处级正职",
     "note": "2026年3月人代会仍以区长身份作政府工作报告，2026年7月已由董旭接任"},
    {"person_id": 3, "org_id": 1, "title": "莲湖区委副书记",
     "start_date": "", "end_date": "2026-06", "rank": "县处级副职", "note": ""},

    # 尤骁 — 区委副书记
    {"person_id": 4, "org_id": 1, "title": "莲湖区委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "列席区人大、政协会议主席台"},  # From 人代会报道
    {"person_id": 4, "org_id": 2, "title": "莲湖区副区长（曾任）",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "从政府副职转任专职副书记"},

    # 傅强 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 2, "title": "莲湖区副区长、区政府党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 11, "title": "新城区太华路街道武装部部长、西一路街道办事处副主任、区信访局局长、自强路街道党工委书记、区住建局局长",
     "start_date": "", "end_date": "", "rank": "",
     "note": "赴莲湖区前任新城区多岗位工作"},

    # 周兴鹏 — 纪委书记
    {"person_id": 6, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "莲湖区纪委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "区监委主任兼任"},

    # 缪宝辉 — 政法委书记
    {"person_id": 7, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "莲湖区政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 王蓬勃 — 组织部部长
    {"person_id": 8, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "莲湖区委组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 孙广卫 — 区委常委
    {"person_id": 9, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 武蓉 — 统战部部长
    {"person_id": 10, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "莲湖区委统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 王洋 — 区委常委
    {"person_id": 11, "org_id": 1, "title": "莲湖区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 陈晏辉 — 副区长
    {"person_id": 12, "org_id": 2, "title": "莲湖区副区长、区政府党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管民政、教育、城市更新等工作"},
    {"person_id": 12, "org_id": 15, "title": "西安电子科技大学校团委副书记、学生工作处副处长",
     "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 14, "title": "西安市自然资源和规划局处长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "历任政策法规处副处长、纪委副书记、规划与科技处处长、国土空间总体规划处处长"},

    # 符杰 — 副区长、公安局长
    {"person_id": 13, "org_id": 2, "title": "莲湖区副区长、区政府党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责公安、司法、信访等工作"},
    {"person_id": 13, "org_id": 7, "title": "公安莲湖分局局长、督察长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 13, "org_id": 12, "title": "西安市公安局新城分局副局长",
     "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 13, "org_id": 13, "title": "西安市公安局站前分局局长",
     "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "公安莲湖分局党委副书记、政委",
     "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},

    # 马晓娟 — 副区长
    {"person_id": 14, "org_id": 2, "title": "莲湖区副区长、区政府党组成员",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责应急管理、城管、招商、文旅、市场监管、民族宗教等"},
    {"person_id": 14, "org_id": 16, "title": "北院门街道党工委书记",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": ""},
    {"person_id": 14, "org_id": 1, "title": "莲湖区青年路街道党工委书记",
     "start_date": "", "end_date": "", "rank": "乡科级正职",
     "note": "曾任"},
    {"person_id": 14, "org_id": 1, "title": "莲湖区北院门街道办主任",
     "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "莲湖区纪委派出土门街道纪工委书记",
     "start_date": "", "end_date": "", "rank": "乡科级",
     "note": ""},

    # 张营 — 人大常委会主任
    {"person_id": 15, "org_id": 8, "title": "莲湖区人大常委会主任",
     "start_date": "2026-03", "end_date": "present", "rank": "县处级正职",
     "note": "2026年3月21日区十九届人大五次会议当选"},

    # 刘永毅 — 原人大常委会主任
    {"person_id": 16, "org_id": 8, "title": "莲湖区人大常委会主任",
     "start_date": "", "end_date": "2026-03", "rank": "县处级正职",
     "note": "2026年3月换届卸任"},

    # 上官拥军 — 政协主席
    {"person_id": 17, "org_id": 9, "title": "莲湖区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": ""},
]

# ── Relationships ──

relationships = [
    # 马翔 ↔ 董旭 — 区委书记与代区长（上下级）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与代区长——班子正副班长关系",
     "overlap_org": "中共西安市莲湖区委员会",
     "overlap_period": "2026-07至今"},

    # 马翔 ↔ 胡广乐 — 原搭档
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区长——原正副班长搭档",
     "overlap_org": "中共西安市莲湖区委员会",
     "overlap_period": "至2026-06"},

    # 董旭 ↔ 傅强 — 同为区政府班子成员
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "区政府正副职——区长与常务副区长",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": ""},

    # 符杰 ↔ 傅强 — 同为副区长
    {"person_a": 5, "person_b": 13, "type": "overlap",
     "context": "区政府班子成员",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": ""},

    # 陈晏辉 ↔ 傅强 — 同为副区长
    {"person_a": 5, "person_b": 12, "type": "overlap",
     "context": "区政府班子成员",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": ""},

    # 马晓娟 ↔ 傅强 — 同为副区长
    {"person_a": 5, "person_b": 14, "type": "overlap",
     "context": "区政府班子成员",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": ""},

    # 马晓娟 ↔ 符杰 — 同为副区长
    {"person_a": 13, "person_b": 14, "type": "overlap",
     "context": "区政府班子成员",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": ""},

    # 张营 ↔ 刘永毅 — 前任继任
    {"person_a": 15, "person_b": 16, "type": "predecessor_successor",
     "context": "人大主任交接——张营2026年3月接替刘永毅",
     "overlap_org": "西安市莲湖区人民代表大会常务委员会",
     "overlap_period": "2026-03"},

    # 董旭 ↔ 胡广乐 — 前任继任（区长）
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor",
     "context": "区长交接——董旭代胡广乐任代区长",
     "overlap_org": "西安市莲湖区人民政府",
     "overlap_period": "2026-07"},

    # 马翔 ↔ 周兴鹏 — 区委党委书记与纪委书记
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委常委会班子——书记与纪委书记",
     "overlap_org": "中共西安市莲湖区委员会",
     "overlap_period": ""},

    # 马翔 ↔ 缪宝辉
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委常委会班子",
     "overlap_org": "中共西安市莲湖区委员会",
     "overlap_period": ""},

    # 马翔 ↔ 王蓬勃
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "区委常委会班子——书记与组织部长",
     "overlap_org": "中共西安市莲湖区委员会",
     "overlap_period": ""},

    # 上官拥军 ↔ 马翔 — 政协与党委
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "区委与区政协",
     "overlap_org": "",
     "overlap_period": ""},
]

# =========================================================================
# Person JSON helpers
# =========================================================================


def write_person_json(person: dict) -> None:
    """Write a single person JSON from research data.人物深度图谱"""
    os.makedirs(PERSONS_DIR, exist_ok=True)

    post = person["current_post"]
    if "区委书记" in post:
        role_label = "区委书记"
    elif "副区长" in post:
        role_label = "副区长"
    elif "代区长" in post:
        role_label = "代区长"
    elif "原区长" in post or ("区长" in post and "副" not in post):
        role_label = "区长"
    elif "区委副书记" in post:
        role_label = "区委副书记"
    elif "纪委书记" in post:
        role_label = "纪委书记"
    elif "政法委书记" in post:
        role_label = "政法委书记"
    elif "组织部" in post:
        role_label = "组织部部长"
    elif "统战部" in post:
        role_label = "统战部部长"
    elif "人大" in post:
        role_label = "人大常委会主任"
    elif "政协" in post:
        role_label = "政协主席"
    else:
        role_label = "区委常委"

    # Find person-specific positions
    person_positions = [pos for pos in positions if pos["person_id"] == person["id"]]
    timeline = []
    for pos in person_positions:
        oid = pos["org_id"]
        org_name = next((o["name"] for o in organizations if o["id"] == oid), f"org_{oid}")
        timeline.append({
            "start": pos["start_date"],
            "end": pos["end_date"],
            "org": org_name,
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "confidence": "confirmed",
            "source_ids": ["S1"],
        })

    sources = [{
        "id": "S1",
        "title": f"莲湖区府领导信息",
        "url": person["source"],
        "publisher": "西安市莲湖区人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "",
    }]

    # Education
    edu_entries = []
    if person["education"]:
        edu_entries.append({
            "period": "", "institution": "", "major": "",
            "degree": person["education"],
            "study_type": "unknown",
            "source_ids": ["S1"],
        })

    filename = f"{AS_OF_SHORT}-陕西省-西安市-{role_label}-{person['name']}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    missing_bio = not person["birth"]
    open_qs = []
    if missing_bio:
        open_qs.append({
            "priority": "critical",
            "question": f"{person['name']}的出生年月、籍贯、教育背景和早期职业生涯",
            "why_it_matters": "核心领导缺失基本身份信息，无法做全国范围的规范识别",
            "suggested_queries": [f"{person['name']} 简历 莲湖区",
                                   f"{person['name']} 任前公示"],
            "last_attempted": AS_OF,
        })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省", "city": "西安市",
            "region": "莲湖区", "job": role_label,
            "task_id": "shaanxi_莲湖区",
            "time_focus": "截至2026年8月",
        },
        "identity": {
            "person_id": f"lianhu_{person['name']}",
            "name": person["name"],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": "",
            "native_place": "",
            "education": edu_entries,
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S1"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style inferred from public records — not a private psychological assessment.",
        },
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if not missing_bio else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if len(timeline) > 1 else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "基本信息/早期履历缺失" if missing_bio else "细节履历需补充",
        },
        "open_questions": open_qs,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")


# === MAIN ===
if __name__ == "__main__":
    print("=" * 60)
    print("  莲湖区 cadre exchange network build")
    print("  陕西省西安市莲湖区")
    print(f"  人员: {len(persons)}  机构: {len(organizations)}")
    print(f"  任职: {len(positions)}  关系: {len(relationships)}")
    print("=" * 60)

    run_build(
        slug="莲湖区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("\n—— Person JSON ——")
    core_ids = {1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 17}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n✓ DB:  {DB_PATH}")
    print(f"✓ GEXF: {GEXF_PATH}")