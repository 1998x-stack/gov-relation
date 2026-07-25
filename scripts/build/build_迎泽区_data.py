#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 迎泽区 (Yingze District), 太原市, 山西省.

Investigation date: 2026-07-25
Task ID: shanxi_迎泽区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.yingze.gov.cn — 迎泽区人民政府门户网站 (official leadership pages, news)
  - www.taiyuan.gov.cn — 太原市人民政府网站 (city-level context)
  - 区委领导页面: /qwld/20250421/30212480.html (区委常委)
  - 区政府领导页面: /qzfld/20250606/30002913.html (区政府领导班子分工)
  - News articles from 2026-05 to 2026-07 confirming current officeholders

Current confirmed leadership (as of 2026-07-25):
  - 张耀: 区委书记 (confirmed via multiple news articles: 2026-05-01, 2026-05-23, 2026-06-17, 2026-06-29, 2026-07-14)
  - 刘爱国: 区委副书记、区长 (confirmed via news: 2026-04-30, 2026-05-01, 2026-05-20, 2026-06-29)

Confidence notes:
  - 张耀 and 刘爱国 are confirmed as current top two leaders through multiple official yingze.gov.cn news articles dated 2026-05 to 2026-07
  - The party leadership page (updated 2025-04-21) appears outdated — still lists 赵学军 as 区委副书记/区长, but all 2026 news uses 刘爱国 as 区长
  - Detailed career timelines (education, early career) for most figures could not be fully verified due to web access limitations
  - Web search tools (Exa) were rate-limited during this investigation; data primarily from direct website fetches
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

SLUG = "迎泽区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ──────────────────────────────────────────────────────────
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "张耀",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/yzdt/20260523/30299925.html"
    },
    {
        "id": 2,
        "name": "刘爱国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/yzdt/20260520/30299929.html"
    },
    {
        "id": 3,
        "name": "郑林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/yzdt/20260629/30308401.html"
    },
    {
        "id": 4,
        "name": "苏国清",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、统战部部长",
        "current_org": "中共太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    {
        "id": 5,
        "name": "赵晋胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    {
        "id": 6,
        "name": "石磐",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、人武部上校部长",
        "current_org": "迎泽区人民武装部",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    {
        "id": 7,
        "name": "李永强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、党校校长",
        "current_org": "中共太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    {
        "id": 8,
        "name": "刘学民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共太原市迎泽区纪律检查委员会",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    {
        "id": 9,
        "name": "裴涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、老军营街道党工委书记",
        "current_org": "中共太原市迎泽区老军营街道工作委员会",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # District Government — Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "王树仁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "太原市公安局迎泽分局",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 11,
        "name": "陈文生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 12,
        "name": "张渊学",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 13,
        "name": "李敏",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 14,
        "name": "刘晓",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 15,
        "name": "范勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html"
    },
    {
        "id": 16,
        "name": "桑都哈什·巴依木拉提",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市迎泽区人民政府",
        "source": "http://www.yingze.gov.cn/yzdt/20260523/30299925.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 17,
        "name": "赵学军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.yingze.gov.cn/qwld/20250421/30212480.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # District People's Congress (人大)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 18,
        "name": "薛凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "太原市迎泽区人民代表大会常务委员会",
        "source": "http://www.yingze.gov.cn/qrdld/20250819/30248247.html"
    },
    {
        "id": 19,
        "name": "韩石俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "太原市迎泽区人民代表大会常务委员会",
        "source": "http://www.yingze.gov.cn/qrdld/20250819/30248247.html"
    },
    {
        "id": 20,
        "name": "秦宇星",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "太原市迎泽区人民代表大会常务委员会",
        "source": "http://www.yingze.gov.cn/qrdld/20250819/30248247.html"
    },
    {
        "id": 21,
        "name": "孟晋忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "太原市迎泽区人民代表大会常务委员会",
        "source": "http://www.yingze.gov.cn/qrdld/20250819/30248247.html"
    },
    {
        "id": 22,
        "name": "叶涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "太原市迎泽区人民代表大会常务委员会",
        "source": "http://www.yingze.gov.cn/qrdld/20250819/30248247.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # District Political Consultative Conference (政协)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 23,
        "name": "闫晓琴",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qzxld/20260618/30304828.html"
    },
    {
        "id": 24,
        "name": "王素云",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qzxld/20260618/30304828.html"
    },
    {
        "id": 25,
        "name": "王孝兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qzxld/20260618/30304828.html"
    },
    {
        "id": 26,
        "name": "李斌玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qzxld/20260618/30304828.html"
    },
    {
        "id": 27,
        "name": "刘俊刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议太原市迎泽区委员会",
        "source": "http://www.yingze.gov.cn/qzxld/20260618/30304828.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────

organizations = [
    # Party
    {
        "id": 1,
        "name": "中共太原市迎泽区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共太原市委",
        "location": "山西省太原市迎泽区"
    },
    {
        "id": 2,
        "name": "中共太原市迎泽区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共太原市纪委",
        "location": "山西省太原市迎泽区"
    },
    {
        "id": 3,
        "name": "中共太原市迎泽区委组织部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共太原市迎泽区委员会",
        "location": "山西省太原市迎泽区"
    },
    {
        "id": 4,
        "name": "中共太原市迎泽区委宣传部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共太原市迎泽区委员会",
        "location": "山西省太原市迎泽区"
    },
    {
        "id": 5,
        "name": "中共太原市迎泽区委统战部",
        "type": "党委",
        "level": "正科级",
        "parent": "中共太原市迎泽区委员会",
        "location": "山西省太原市迎泽区"
    },
    # Government
    {
        "id": 6,
        "name": "太原市迎泽区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "太原市人民政府",
        "location": "山西省太原市迎泽区"
    },
    {
        "id": 7,
        "name": "太原市公安局迎泽分局",
        "type": "政府",
        "level": "正科级",
        "parent": "太原市公安局",
        "location": "山西省太原市迎泽区"
    },
    # Military
    {
        "id": 8,
        "name": "迎泽区人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "太原警备区",
        "location": "山西省太原市迎泽区"
    },
    # Street / Town
    {
        "id": 9,
        "name": "中共太原市迎泽区老军营街道工作委员会",
        "type": "乡镇/街道",
        "level": "正科级",
        "parent": "中共太原市迎泽区委员会",
        "location": "山西省太原市迎泽区老军营街道"
    },
    # People's Congress
    {
        "id": 10,
        "name": "太原市迎泽区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "太原市人民代表大会常务委员会",
        "location": "山西省太原市迎泽区"
    },
    # CPPCC
    {
        "id": 11,
        "name": "中国人民政治协商会议太原市迎泽区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议太原市委员会",
        "location": "山西省太原市迎泽区"
    },
]

# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "Confirmed as of 2026-06-29 from表彰大会新闻"},
    {"person_id": 4, "org_id": 1, "title": "区委常委、宣传部部长、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "副区长（常务）", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管常务工作"},
    {"person_id": 6, "org_id": 8, "title": "上校部长", "start_date": "", "end_date": "", "rank": "正团级", "note": "区委常委"},
    {"person_id": 7, "org_id": 3, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委"},
    {"person_id": 8, "org_id": 2, "title": "纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委"},
    {"person_id": 9, "org_id": 9, "title": "党工委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": "区委常委"},
    # Deputy mayors
    {"person_id": 10, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "主管公安分局"},
    {"person_id": 10, "org_id": 7, "title": "局长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管民政、人社、农业农村等"},
    {"person_id": 12, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管城乡管理、生态环境等"},
    {"person_id": 13, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管文旅、卫健、医保、市场监管"},
    {"person_id": 14, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管政府办、外事、科技等"},
    {"person_id": 15, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管自然资源、住建、城改等"},
    {"person_id": 16, "org_id": 6, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "哈萨克族, 陪同区委书记调研防汛"},
    # Predecessor
    {"person_id": 17, "org_id": 1, "title": "区委副书记（原）", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任区长，已被刘爱国接替"},
    {"person_id": 17, "org_id": 6, "title": "区长（原）", "start_date": "", "end_date": "", "rank": "正处级", "note": "领导页面仍显示但已被刘爱国取代"},
    # People's Congress
    {"person_id": 18, "org_id": 10, "title": "主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 10, "title": "副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 10, "title": "副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # CPPCC
    {"person_id": 23, "org_id": 11, "title": "主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 11, "title": "副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 11, "title": "副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 11, "title": "副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 11, "title": "副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "张耀（区委书记）与刘爱国（区长）为区党政一把手搭档",
     "overlap_org": "中共太原市迎泽区委员会/太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "张耀（区委书记）与郑林（区委副书记）为上下级关系",
     "overlap_org": "中共太原市迎泽区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "刘爱国（区长）与郑林（区委副书记）同为区委副书记",
     "overlap_org": "中共太原市迎泽区委员会",
     "overlap_period": "2026-至今"},
    # Standing committee interconnections
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "张耀（区委书记）与苏国清（宣传部部长）为上下级",
     "overlap_org": "中共太原市迎泽区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "张耀（区委书记）与李永强（组织部部长）为上下级",
     "overlap_org": "中共太原市迎泽区委员会",
     "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "张耀（区委书记）与刘学民（纪委书记）为上下级",
     "overlap_org": "中共太原市迎泽区委员会",
     "overlap_period": "2026-至今"},
    # District government leadership core
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "刘爱国（区长）与赵晋胜（常务副区长）为正副手关系",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "刘爱国（区长）与王树仁（副区长/公安分局局长）为上下级",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "刘爱国（区长）与陈文生（副区长）为上下级",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "刘爱国（区长）与张渊学（副区长）为上下级",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "刘爱国（区长）与范勇（副区长）为上下级",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2026-至今"},
    # Predecessor relationships
    {"person_a": 17, "person_b": 2, "type": "predecessor_successor",
     "context": "赵学军（原区长）与刘爱国（现任区长）为前后任交接",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2025-2026"},
    # District party-government cross-org
    {"person_a": 18, "person_b": 23, "type": "overlap",
     "context": "薛凯（人大主任）与闫晓琴（政协主席）同为区四套班子主要领导",
     "overlap_org": "迎泽区四套班子",
     "overlap_period": "2026"},
    # Zhao Xuejun's connections with standing committee
    {"person_a": 17, "person_b": 5, "type": "superior_subordinate",
     "context": "赵学军（原区长）与赵晋胜（常务副区长）曾为上下级",
     "overlap_org": "太原市迎泽区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 17, "person_b": 8, "type": "overlap",
     "context": "赵学军（原区长）与刘学民（纪委书记）同届共事",
     "overlap_org": "迎泽区",
     "overlap_period": "2025-2026"},
    # Cross-team connections
    {"person_a": 1, "person_b": 18, "type": "overlap",
     "context": "张耀（区委书记）与薛凯（人大主任）为党政与人大领导协作",
     "overlap_org": "迎泽区",
     "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 18, "type": "overlap",
     "context": "刘爱国（区长）与薛凯（人大主任）为政府与人大领导协作",
     "overlap_org": "迎泽区",
     "overlap_period": "2026-至今"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════

def main():
    # Use gov_relation runner if available
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

        # For staging, use explicit paths
        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
        )
        print(f"\nDB: {DB_PATH}")
        print(f"GEXF: {GEXF_PATH}")
    except ImportError:
        print("gov_relation not found at REPO_ROOT, using inline build.")
        _inline_build()

    # Write person JSONs
    _write_person_jsons()

    print(f"\nAll artifacts for {SLUG} written to {BASE}/")
    print(f"  DB: {'exists' if os.path.exists(DB_PATH) else 'MISSING'}")
    print(f"  GEXF: {'exists' if os.path.exists(GEXF_PATH) else 'MISSING'}")


def _write_person_jsons():
    """Write per-person graph JSON files for core leaders."""
    today = TODAY

    person_files = [
        {
            "filename": f"{today}-山西省-太原市-区委书记-张耀.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": today,
                "investigation_scope": {
                    "province": "山西省",
                    "city": "太原市",
                    "region": "迎泽区",
                    "job": "区委书记",
                    "task_id": "shanxi_迎泽区",
                    "time_focus": "2025-2026"
                },
                "identity": {
                    "person_id": "taiyuan_yingze_zhang_yao",
                    "name": "张耀",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "张耀",
                        "name_birthplace": "张耀",
                        "official_profile_url": "http://www.yingze.gov.cn/"
                    }
                },
                "current_status": {
                    "current_post": "区委书记",
                    "current_org": "中共太原市迎泽区委员会",
                    "administrative_rank": "正处级",
                    "as_of": "2026-05-01",
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002", "S003", "S004"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "履历缺口",
                        "title": "",
                        "notes": "公开资料暂未找到出任迎泽区委书记前的详细履历",
                        "confidence": "unverified",
                        "source_ids": []
                    }
                ],
                "organizations": [
                    {"name": "中共太原市迎泽区委员会", "role": "区委书记"}
                ],
                "relationships": [
                    {
                        "person": "刘爱国",
                        "person_id": "taiyuan_yingze_liu_aiguo",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "区委书记与区长党政一把手搭档，共同出席调研活动",
                        "overlap_org": "中共太原市迎泽区委员会/太原市迎泽区人民政府",
                        "overlap_period": "2026-至今",
                        "direction": "person_to_other",
                        "confidence": "confirmed",
                        "source_ids": ["S001", "S002", "S003"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-05",
                        "domain": "public_security",
                        "achievement_or_event": "带队检查防汛备汛、入河排污口整治",
                        "role_in_event": "带队调研",
                        "measurable_outcome": "要求加快南沙河等重点河段清淤进度",
                        "location": "迎泽区南沙河沿线",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    },
                    {
                        "period": "2026-06",
                        "domain": "economic_development",
                        "achievement_or_event": "主持区委常委会扩大会议，部署实体经济发展",
                        "role_in_event": "主持会议",
                        "measurable_outcome": "聚焦商圈改造、楼宇提升、文旅融合等领域",
                        "location": "迎泽区",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2026-06",
                        "domain": "other",
                        "achievement_or_event": "出席迎泽区'两优一先'表彰大会并讲话",
                        "role_in_event": "讲话",
                        "measurable_outcome": "表彰100名优秀共产党员等先进典型",
                        "location": "迎泽区",
                        "confidence": "confirmed",
                        "source_ids": ["S004"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "履历信息不足，无法评估晋升速度",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "调研中强调'挂图作战''倒排工期'，注重实效",
                            "confidence": "plausible",
                            "source_ids": ["S001"]
                        },
                        {
                            "trait": "discipline_oriented",
                            "evidence": "多次强调安全生产责任和防汛纪律",
                            "confidence": "plausible",
                            "source_ids": ["S001", "S002"]
                        }
                    ],
                    "speech_themes": ["高质量发展", "安全底线", "群众立场"],
                    "management_signals": ["强调闭环管理", "要求压实责任"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "截至2026年7月，公开信息中未发现与张耀相关的纪律处分、审计问题或负面报道",
                        "date": "2026-07-25",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "张耀调研检查防汛备汛工作",
                        "url": "http://www.yingze.gov.cn/yzdt/20260523/30299925.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-05-23",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认张耀为区委书记"
                    },
                    {
                        "id": "S002",
                        "title": "张耀刘爱国检查假日安全生产、文旅服务、护林防火等工作",
                        "url": "http://www.yingze.gov.cn/yzdt/20260501/30296666.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-05-01",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认张耀为区委书记，刘爱国为区长"
                    },
                    {
                        "id": "S003",
                        "title": "区委常委会召开扩大会议",
                        "url": "http://www.yingze.gov.cn/yzdt/20260617/30305583.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-06-17",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "区委常委会由张耀主持"
                    },
                    {
                        "id": "S004",
                        "title": "迎泽区'两优一先'表彰大会召开",
                        "url": "http://www.yingze.gov.cn/yzdt/20260629/30308401.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-06-29",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "张耀讲话，刘爱国主持，郑林为区委副书记"
                    }
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "high",
                    "biggest_gap": "张耀任迎泽区委书记前的完整履历（出生、教育、早期任职等）"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "张耀出生于哪一年？籍贯何处？",
                        "why_it_matters": "核心人物身份信息缺失，影响图谱完整性",
                        "suggested_queries": ["张耀 简历 太原", "张耀 任前公示 迎泽区委书记"],
                        "last_attempted": "2026-07-25"
                    },
                    {
                        "priority": "high",
                        "question": "张耀出任迎泽区委书记前的任职履历",
                        "why_it_matters": "无法评估其晋升路径和核心系统经验",
                        "suggested_queries": ["张耀 此前 担任", "张耀 太原 组织部"],
                        "last_attempted": "2026-07-25"
                    }
                ]
            }
        },
        {
            "filename": f"{today}-山西省-太原市-区长-刘爱国.json",
            "data": {
                "schema_version": "1.0",
                "generated_at": today,
                "investigation_scope": {
                    "province": "山西省",
                    "city": "太原市",
                    "region": "迎泽区",
                    "job": "区长",
                    "task_id": "shanxi_迎泽区",
                    "time_focus": "2025-2026"
                },
                "identity": {
                    "person_id": "taiyuan_yingze_liu_aiguo",
                    "name": "刘爱国",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": "刘爱国",
                        "name_birthplace": "刘爱国",
                        "official_profile_url": "http://www.yingze.gov.cn/"
                    }
                },
                "current_status": {
                    "current_post": "区委副书记、区长",
                    "current_org": "太原市迎泽区人民政府",
                    "administrative_rank": "正处级",
                    "as_of": "2026-05-20",
                    "is_current_confirmed": True,
                    "source_ids": ["S005", "S006", "S007"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "unknown",
                        "org": "太原市迎泽区人民政府",
                        "title": "区委常委、副区长（常务）",
                        "notes": "出任区长前担任区委常委、常务副区长",
                        "confidence": "confirmed",
                        "source_ids": ["S006"]
                    },
                    {
                        "start": "unknown",
                        "end": "至今",
                        "org": "太原市迎泽区人民政府",
                        "title": "区委副书记、区长",
                        "notes": "接替赵学军出任区长",
                        "confidence": "confirmed",
                        "source_ids": ["S005", "S006", "S007"]
                    }
                ],
                "organizations": [
                    {"name": "中共太原市迎泽区委员会", "role": "区委副书记"},
                    {"name": "太原市迎泽区人民政府", "role": "区长"}
                ],
                "relationships": [
                    {
                        "person": "张耀",
                        "person_id": "taiyuan_yingze_zhang_yao",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "区长与区委书记党政搭档，共同参加调研",
                        "overlap_org": "迎泽区",
                        "overlap_period": "2026-至今",
                        "direction": "other_to_person",
                        "confidence": "confirmed",
                        "source_ids": ["S005", "S006"]
                    },
                    {
                        "person": "赵学军",
                        "person_id": "taiyuan_yingze_zhao_xuejun",
                        "relationship_type": "predecessor_successor",
                        "strength": "strong",
                        "evidence": "赵学军为前任区长，刘爱国接任",
                        "overlap_org": "太原市迎泽区人民政府",
                        "overlap_period": "2025-2026",
                        "direction": "other_to_person",
                        "confidence": "plausible",
                        "source_ids": ["S008"]
                    },
                    {
                        "person": "赵晋胜",
                        "person_id": "taiyuan_yingze_zhao_jinsheng",
                        "relationship_type": "superior_subordinate",
                        "strength": "strong",
                        "evidence": "赵晋胜为常务副区长，是刘爱国的主要副手",
                        "overlap_org": "太原市迎泽区人民政府",
                        "overlap_period": "2026-至今",
                        "direction": "person_to_other",
                        "confidence": "confirmed",
                        "source_ids": ["S006", "S007"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-04",
                        "domain": "public_security",
                        "achievement_or_event": "带队开展节假日安全专项检查",
                        "role_in_event": "带队检查",
                        "measurable_outcome": "检查观家峪森林防火、外麻地沟交通、铜锣湾消防",
                        "location": "迎泽区",
                        "confidence": "confirmed",
                        "source_ids": ["S005"]
                    },
                    {
                        "period": "2026-05",
                        "domain": "economic_development",
                        "achievement_or_event": "调研督导重点项目建设",
                        "role_in_event": "带队调研",
                        "measurable_outcome": "现场办公协调解决太原站新建东站房、水峪城改二期等项目问题",
                        "location": "迎泽区",
                        "confidence": "confirmed",
                        "source_ids": ["S007"]
                    }
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "履历信息不足，无法评估晋升速度",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "调研中强调'现场办公协调解决难点堵点问题'",
                            "confidence": "plausible",
                            "source_ids": ["S007"]
                        },
                        {
                            "trait": "low_profile",
                            "evidence": "公开活动多为陪同区委书记或独立调研具体项目",
                            "confidence": "plausible",
                            "source_ids": ["S005", "S006", "S007"]
                        }
                    ],
                    "speech_themes": ["项目推进", "安全生产", "服务企业"],
                    "management_signals": ["现场交办", "倒排工期", "挂图作战"],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "截至2026年7月，公开信息中未发现与刘爱国相关的纪律处分、审计问题或负面报道",
                        "date": "2026-07-25",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {
                        "id": "S005",
                        "title": "刘爱国检查节假日安全（含在张耀刘爱国联合检查报道中）",
                        "url": "http://www.yingze.gov.cn/yzdt/20260501/30296666.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-05-01",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认刘爱国为区委副书记、区长"
                    },
                    {
                        "id": "S006",
                        "title": "区政府领导分工页面",
                        "url": "http://www.yingze.gov.cn/qzfld/20250606/30002913.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2025-06-06",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "页面显示赵学军为区长但政府分工列出刘爱国为区委常委、副区长（可能页面已过时）"
                    },
                    {
                        "id": "S007",
                        "title": "刘爱国调研督导重点项目建设",
                        "url": "http://www.yingze.gov.cn/yzdt/20260520/30299929.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2026-05-20",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "确认刘爱国为区委副书记、区长"
                    },
                    {
                        "id": "S008",
                        "title": "区委领导页面",
                        "url": "http://www.yingze.gov.cn/qwld/20250421/30212480.html",
                        "publisher": "迎泽区人民政府",
                        "published_at": "2025-04-21",
                        "accessed_at": "2026-07-25",
                        "source_type": "official",
                        "reliability": "medium",
                        "notes": "显示赵学军为区委副书记、区长（可能已过时）"
                    }
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "high",
                    "biggest_gap": "刘爱国完整履历（出生、教育、早期任职等），尤其是升任区长前的全部经历"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "刘爱国出生于哪一年？籍贯何处？",
                        "why_it_matters": "核心人物身份信息缺失，影响图谱完整性",
                        "suggested_queries": ["刘爱国 简历 太原", "刘爱国 迎泽区"],
                        "last_attempted": "2026-07-25"
                    },
                    {
                        "priority": "high",
                        "question": "刘爱国出任区长前的完整任职履历",
                        "why_it_matters": "仅知其此前为常务副区长，更早经历空白",
                        "suggested_queries": ["刘爱国 太原 任职经历"],
                        "last_attempted": "2026-07-25"
                    },
                    {
                        "priority": "medium",
                        "question": "刘爱国何时接替赵学军出任区长",
                        "why_it_matters": "精确的交接时间有助于分析人事调整节奏",
                        "suggested_queries": ["迎泽区 人大常委会 任命 刘爱国"],
                        "last_attempted": "2026-07-25"
                    }
                ]
            }
        },
    ]

    for pf in person_files:
        path = PERSONS_DIR / pf["filename"]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def _inline_build():
    """Fallback: build without gov_relation package."""
    import sqlite3
    from datetime import datetime

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")

    # Create tables
    conn.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '', start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    # Insert persons
    pcols = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
             "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in pcols]
        conn.execute(f"INSERT INTO persons ({','.join(pcols)}) VALUES ({','.join(['?']*len(pcols))})", vals)

    # Insert organizations
    ocols = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in ocols]
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join(['?']*len(ocols))})", vals)

    # Insert positions
    poscols = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in poscols]
        conn.execute(f"INSERT INTO positions ({','.join(poscols)}) VALUES ({','.join(['?']*len(poscols))})", vals)

    # Insert relationships
    rcols = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in rcols]
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join(['?']*len(rcols))})", vals)

    conn.commit()
    conn.close()
    print(f"SQLite: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

    # ── GEXF ──
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        post = p.get("current_post", "")
        if "书记" in post and "纪委" not in post:
            return "255,50,50"
        elif "区长" in post or "副区" in post:
            return "50,100,255"
        elif "纪委" in post:
            return "255,165,0"
        else:
            return "100,100,100"

    def org_color(o):
        t = o.get("type", "")
        if "党委" in t:
            return "255,200,200"
        elif "政府" in t:
            return "200,200,255"
        elif "乡镇" in t:
            return "255,255,200"
        elif "人大" in t:
            return "200,255,255"
        elif "政协" in t:
            return "255,240,200"
        else:
            return "200,200,200"

    def is_top_leader(p):
        post = p.get("current_post", "")
        return "区委书记" == post or "区长" == post or "区委副书记、区长" == post

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} — 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: positions (person -> org)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start_date", "") or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: relationships (person <-> person)
    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] in ("superior_subordinate", "predecessor_successor") else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
