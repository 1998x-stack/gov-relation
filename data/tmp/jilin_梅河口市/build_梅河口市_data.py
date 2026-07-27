#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 梅河口市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_梅河口市
Level: 县级市 (省直管县试点)
Targets: 市委书记 & 市长

Research sources:
  - mhk.gov.cn — 梅河口市人民政府官方网站 (HTTP可访问)
  - mhk.gov.cn/xqxz/ldbz/ — 领导简历页面
  - 澎湃新闻 — 人事任免报道
  - 快懂百科 — 朱欢履历

Key facts:
  - 梅河口市是吉林省省直管县试点（2013年开始）
  - 同时挂"梅河新区"牌子（省级新区，2021年设立），党工委与市委一套班子
  - 市委书记为副厅级（较一般县级市正处级高半级）
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(os.path.dirname(STAGING_DIR)))
SLUG = "梅河口市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING_DIR)

# ══════════════════════════════════════════════════════════════════════════
# Persons
# ══════════════════════════════════════════════════════════════════════════
# ID range: 1-20 persons, 101-120 orgs

persons = [
    # ═══════════════ Core Leaders ═══════════════
    {
        "id": 1,
        "name": "朱欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "浙江杭州",
        "education": "浙江大学研究生学历",
        "party_join": "1999年12月",
        "work_start": "1998年8月",
        "current_post": "梅河新区党工委书记、梅河口市委书记",
        "current_org": "中共梅河口市委员会",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 2,
        "name": "刘铁铎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "辽宁清原",
        "education": "吉林农业大学博士研究生",
        "party_join": "2000年1月",
        "work_start": "2002年7月",
        "current_post": "梅河新区管委会主任、梅河口市委副书记、市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    # ═══════════════ 市委常委/副市长 ═══════════════
    {
        "id": 3,
        "name": "林小明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "2003年9月",
        "current_post": "梅河新区党工委委员、管委会副主任，市委常委、常务副市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 4,
        "name": "陈楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河新区党工委委员、市委常委、组织部部长、市委教育工委书记",
        "current_org": "中共梅河口市委组织部",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 5,
        "name": "郭俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河新区党工委委员、管委会副主任，市委常委、副市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 6,
        "name": "邹文博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河新区党工委委员、管委会副主任，市委常委、副市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 7,
        "name": "周君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市委常委",
        "current_org": "中共梅河口市委员会",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 8,
        "name": "王震宇",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市委常委",
        "current_org": "中共梅河口市委员会",
        "source": "2026年任前公示"
    },
    {
        "id": 9,
        "name": "汪晓梅",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1998年11月",
        "current_post": "梅河新区党工委委员、管委会副主任，副市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 10,
        "name": "林树杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "广东汕头",
        "education": "研究生学历，法学博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河新区党工委委员、管委会副主任，副市长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 11,
        "name": "冯珉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年",
        "birthplace": "吉林柳河",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1993年",
        "current_post": "梅河新区党工委委员",
        "current_org": "梅河新区党工委",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 12,
        "name": "何向平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年2月",
        "birthplace": "浙江景宁",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1997年9月",
        "current_post": "梅河口市副市长（浙江挂职干部）",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 13,
        "name": "赵昕晔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "河北乐亭",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1998年7月",
        "current_post": "梅河口市副市长、公安局局长",
        "current_org": "梅河口市人民政府",
        "source": "mhk.gov.cn 官方简历"
    },
    {
        "id": 14,
        "name": "吴玉安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "吉林长岭",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1992年9月",
        "current_post": "梅河新区管委会二级巡视员",
        "current_org": "梅河新区管委会",
        "source": "mhk.gov.cn 官方简历"
    },
    # ═══════════════ 人大、政协 ═══════════════
    {
        "id": 15,
        "name": "宁洪友",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市人大常委会主任、党组书记",
        "current_org": "梅河口市人大常委会",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 16,
        "name": "李宏艳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市政协主席、党组书记",
        "current_org": "中国人民政治协商会议梅河口市委员会",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 17,
        "name": "瞿鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市人大常委会副主任、总工会主席",
        "current_org": "梅河口市人大常委会",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 18,
        "name": "杨绍忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市人大常委会副主任",
        "current_org": "梅河口市人大常委会",
        "source": "mhk.gov.cn 新闻报道"
    },
    {
        "id": 19,
        "name": "霍光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "梅河口市政协副主席、农业农村局局长",
        "current_org": "中国人民政治协商会议梅河口市委员会",
        "source": "mhk.gov.cn 新闻报道"
    },
    # ═══════════════ 前书记 ═══════════════
    {
        "id": 20,
        "name": "王爱明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吉林省民族事务委员会主任、党组书记",
        "current_org": "吉林省民族事务委员会",
        "source": "澎湃新闻、人民网"
    },
    {
        "id": 21,
        "name": "庞庆波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "白城市委书记",
        "current_org": "中共白城市委员会",
        "source": "中国经济网"
    },
    # ═══════════════ 前市长 ═══════════════
    {
        "id": 22,
        "name": "宋钦炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通化市人大常委会党组书记",
        "current_org": "通化市人大常委会",
        "source": "澎湃新闻"
    },
    {
        "id": 23,
        "name": "牟大鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "吉林大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "澎湃新闻"
    },
    {
        "id": 24,
        "name": "崔彦磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "澎湃新闻"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Organizations
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    # 梅河口市 — 省直管县级市
    {"id": 101, "name": "中共梅河口市委员会", "type": "党委", "level": "副厅级",
     "parent": "中共吉林省委员会", "location": "梅河口市"},
    {"id": 102, "name": "梅河口市人民政府", "type": "政府", "level": "副厅级",
     "parent": "吉林省人民政府", "location": "梅河口市"},
    {"id": 103, "name": "梅河口市人大常委会", "type": "人大", "level": "副厅级",
     "parent": "吉林省人民代表大会常务委员会", "location": "梅河口市"},
    {"id": 104, "name": "中国人民政治协商会议梅河口市委员会", "type": "政协", "level": "副厅级",
     "parent": "中国人民政治协商会议吉林省委员会", "location": "梅河口市"},
    {"id": 105, "name": "中共梅河口市纪律检查委员会", "type": "党委", "level": "副厅级",
     "parent": "中共吉林省纪律检查委员会", "location": "梅河口市"},
    {"id": 106, "name": "中共梅河口市委组织部", "type": "党委", "level": "副处级",
     "parent": "中共梅河口市委员会", "location": "梅河口市"},
    # 梅河新区（2021年设立，与梅河口市一套人马两块牌子）
    {"id": 107, "name": "梅河新区党工委", "type": "党委", "level": "副厅级",
     "parent": "中共吉林省委员会", "location": "梅河口市"},
    {"id": 108, "name": "梅河新区管委会", "type": "政府", "level": "副厅级",
     "parent": "吉林省人民政府", "location": "梅河口市"},
    # 上级组织
    {"id": 109, "name": "中共通化市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共吉林省委员会", "location": "通化市"},
    # 跨区域组织
    {"id": 110, "name": "吉林省民族事务委员会", "type": "政府", "level": "正厅级",
     "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 111, "name": "中共白城市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共吉林省委员会", "location": "白城市"},
    {"id": 112, "name": "通化市人大常委会", "type": "人大", "level": "地厅级",
     "parent": "吉林省人民代表大会常务委员会", "location": "通化市"},
    {"id": 113, "name": "梅河口市公安局", "type": "政府", "level": "正科级",
     "parent": "梅河口市人民政府", "location": "梅河口市"},
    {"id": 114, "name": "梅河口市总工会", "type": "群团", "level": "正科级",
     "parent": "吉林省总工会", "location": "梅河口市"},
]

# ══════════════════════════════════════════════════════════════════════════
# Positions
# ══════════════════════════════════════════════════════════════════════════

positions = [
    # === 朱欢 ===
    {"person_id": 1, "org_id": 107, "title": "梅河新区党工委书记",
     "start_date": "2024年6月", "end_date": "present", "rank": "副厅级",
     "note": "兼任梅河口市委书记"},
    {"person_id": 1, "org_id": 101, "title": "梅河口市委书记",
     "start_date": "2024年6月", "end_date": "present", "rank": "副厅级",
     "note": "同时担任梅河新区党工委书记"},
    # 朱欢浙江履历
    {"person_id": 1, "org_id": 101, "title": "宁波市副市长",
     "start_date": "2022年1月", "end_date": "2024年6月", "rank": "副厅级",
     "note": "浙江省宁波市副市长、市政府党组成员"},
    {"person_id": 1, "org_id": 101, "title": "建德市委书记",
     "start_date": "2018年", "end_date": "2021年", "rank": "副厅级",
     "note": "浙江省建德市委书记"},
    {"person_id": 1, "org_id": 101, "title": "建德市委副书记、市长",
     "start_date": "2016年", "end_date": "2018年", "rank": "正处级",
     "note": "浙江省建德市委副书记、市长"},
    {"person_id": 1, "org_id": 101, "title": "杭州市西湖区委常委、副区长",
     "start_date": "", "end_date": "2016年", "rank": "副厅级",
     "note": "杭州市西湖区委常委、副区长"},

    # === 刘铁铎 ===
    {"person_id": 2, "org_id": 108, "title": "梅河新区管委会主任",
     "start_date": "2025年2月", "end_date": "present", "rank": "副厅级",
     "note": "2025年2月任代主任，2025年3月正式任命"},
    {"person_id": 2, "org_id": 102, "title": "梅河口市市长",
     "start_date": "2025年3月", "end_date": "present", "rank": "副厅级",
     "note": "2025年2月任代市长，2025年3月正式任命"},
    {"person_id": 2, "org_id": 101, "title": "梅河口市委副书记",
     "start_date": "2025年2月", "end_date": "present", "rank": "副厅级",
     "note": ""},
    {"person_id": 2, "org_id": 109, "title": "吉林省委宣传部副部长、吉林广播电视台党组书记、台长",
     "start_date": "2023年8月", "end_date": "2025年2月", "rank": "副厅级",
     "note": ""},
    {"person_id": 2, "org_id": 109, "title": "松原市委常委、常务副市长",
     "start_date": "2021年11月", "end_date": "2023年8月", "rank": "副厅级",
     "note": "松原市委常委、市政府党组副书记、常务副市长"},
    {"person_id": 2, "org_id": 109, "title": "松原市委常委、宣传部部长",
     "start_date": "2020年4月", "end_date": "2021年11月", "rank": "副厅级",
     "note": ""},
    {"person_id": 2, "org_id": 109, "title": "共青团吉林省委员会副书记",
     "start_date": "2013年5月", "end_date": "2020年4月", "rank": "副厅级",
     "note": "共青团吉林省委员会副书记、党组成员，吉林省青年联合会主席"},
    {"person_id": 2, "org_id": 109, "title": "共青团吉林省委城市青年工作部部长",
     "start_date": "", "end_date": "2013年5月", "rank": "正处级",
     "note": ""},
    {"person_id": 2, "org_id": 109, "title": "磐石市副市长（挂职）",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": "挂职锻炼"},
    {"person_id": 2, "org_id": 109, "title": "共青团吉林省委农村青年工作部副部长、部长",
     "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},

    # === 林小明 ===
    {"person_id": 3, "org_id": 102, "title": "梅河口市常务副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、管委会副主任，市委常委、常务副市长"},
    {"person_id": 3, "org_id": 101, "title": "榆树市委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 3, "org_id": 102, "title": "榆树市委副书记、市长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},

    # === 陈楠 ===
    {"person_id": 4, "org_id": 106, "title": "梅河口市委组织部部长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、市委常委、组织部部长、市委教育工委书记"},

    # === 郭俊 ===
    {"person_id": 5, "org_id": 102, "title": "梅河口市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、管委会副主任，市委常委、副市长"},

    # === 邹文博 ===
    {"person_id": 6, "org_id": 102, "title": "梅河口市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、管委会副主任，市委常委、副市长"},

    # === 周君 ===
    {"person_id": 7, "org_id": 101, "title": "梅河口市委常委",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "具体分管工作待查"},

    # === 王震宇 ===
    {"person_id": 8, "org_id": 101, "title": "梅河口市委常委",
     "start_date": "2026年6月", "end_date": "present", "rank": "副厅级",
     "note": "曾任梅河口市副市长、二级调研员，2026年6月拟任市委常委"},

    # === 汪晓梅 ===
    {"person_id": 9, "org_id": 102, "title": "梅河口市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、管委会副主任，副市长。曾任梅河口市委常委、宣传部部长"},

    # === 林树杰 ===
    {"person_id": 10, "org_id": 102, "title": "梅河口市副市长",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "梅河新区党工委委员、管委会副主任，副市长"},

    # === 冯珉 ===
    {"person_id": 11, "org_id": 107, "title": "梅河新区党工委委员",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": "曾任柳河县副县长、长白山管委会池北区党委书记"},

    # === 何向平 ===
    {"person_id": 12, "org_id": 102, "title": "梅河口市副市长（挂职）",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "浙江景宁挂职干部"},

    # === 赵昕晔 ===
    {"person_id": 13, "org_id": 102, "title": "梅河口市副市长、公安局局长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},
    {"person_id": 13, "org_id": 113, "title": "梅河口市公安局局长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "兼任副市长"},

    # === 吴玉安 ===
    {"person_id": 14, "org_id": 108, "title": "梅河新区管委会二级巡视员",
     "start_date": "", "end_date": "present", "rank": "二级巡视员",
     "note": ""},

    # === 宁洪友 ===
    {"person_id": 15, "org_id": 103, "title": "梅河口市人大常委会主任、党组书记",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},

    # === 李宏艳 ===
    {"person_id": 16, "org_id": 104, "title": "梅河口市政协主席、党组书记",
     "start_date": "", "end_date": "present", "rank": "副厅级",
     "note": ""},

    # === 瞿鹏 ===
    {"person_id": 17, "org_id": 103, "title": "梅河口市人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "兼任市总工会主席"},
    {"person_id": 17, "org_id": 114, "title": "梅河口市总工会主席",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": ""},

    # === 杨绍忠 ===
    {"person_id": 18, "org_id": 103, "title": "梅河口市人大常委会副主任",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": ""},

    # === 霍光 ===
    {"person_id": 19, "org_id": 104, "title": "梅河口市政协副主席",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "兼任农业农村局局长"},

    # === 王爱明 ===
    {"person_id": 20, "org_id": 110, "title": "吉林省民族事务委员会主任、党组书记",
     "start_date": "2024年", "end_date": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 20, "org_id": 101, "title": "梅河口市委书记",
     "start_date": "2016年", "end_date": "2024年6月", "rank": "副厅级",
     "note": "同时担任梅河新区党工委书记、通化市委常委（挂职）"},

    # === 庞庆波 ===
    {"person_id": 21, "org_id": 111, "title": "白城市委书记",
     "start_date": "", "end_date": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 21, "org_id": 101, "title": "梅河口市委书记",
     "start_date": "2012年", "end_date": "2015年11月", "rank": "副厅级",
     "note": "曾任通化县委书记、县长"},

    # === 宋钦炜 ===
    {"person_id": 22, "org_id": 112, "title": "通化市人大常委会党组书记",
     "start_date": "2025年3月", "end_date": "present", "rank": "正厅级",
     "note": ""},
    {"person_id": 22, "org_id": 102, "title": "梅河口市市长",
     "start_date": "2021年", "end_date": "2025年2月", "rank": "副厅级",
     "note": "兼任梅河新区管委会主任"},
]

# ══════════════════════════════════════════════════════════════════════════
# Relationships
# ══════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记与市长作为党政主要领导搭档，共同主持梅河口市全面工作",
     "overlap_org": "梅河口市", "overlap_period": "2025年3月至今"},

    # 前后任书记
    {"person_a": 20, "person_b": 1, "type": "predecessor_successor",
     "context": "王爱明任市委书记至2024年6月，朱欢接任",
     "overlap_org": "中共梅河口市委员会", "overlap_period": "2016年-2024年"},

    {"person_a": 21, "person_b": 20, "type": "predecessor_successor",
     "context": "庞庆波任市委书记至2015年11月，王爱明接任",
     "overlap_org": "中共梅河口市委员会", "overlap_period": "2012年-2015年"},

    # 前后任市长
    {"person_a": 22, "person_b": 2, "type": "predecessor_successor",
     "context": "宋钦炜任市长至2025年2月，刘铁铎接任",
     "overlap_org": "梅河口市人民政府", "overlap_period": "2021年-2025年"},

    # 常委班子成员同事实关系
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "市委书记与常务副市长在同一班子",
     "overlap_org": "中共梅河口市委员会", "overlap_period": "至今"},

    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "市委书记与组织部部长在同一班子",
     "overlap_org": "中共梅河口市委员会", "overlap_period": "至今"},

    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "市长与常务副市长：政府班子正副职",
     "overlap_org": "梅河口市人民政府", "overlap_period": "至今"},

    # 跨地区干部交流模式
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "朱欢与何向平均为浙江籍/浙江系统干部，存在跨省交流背景",
     "overlap_org": "浙江省党政系统", "overlap_period": ""},

    # 跨县区调动链
    {"person_a": 21, "person_b": 109, "type": "overlap",
     "context": "庞庆波曾任通化县委书记，后任梅河口市委书记",
     "overlap_org": "通化市", "overlap_period": ""},

    {"person_a": 22, "person_b": 109, "type": "overlap",
     "context": "宋钦炜从梅河口市长调任通化市人大常委会党组书记",
     "overlap_org": "通化市", "overlap_period": "2025年"},
]


# ══════════════════════════════════════════════════════════════════════════
# Helper: XML escape
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Build database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
              p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# Build GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name, post):
    combined = (name or "") + (post or "")
    if "党工委书记" in combined or "市委书记" in combined:
        return "255,50,50"
    if "市长" in combined and "副主任" not in combined:
        return "50,100,255"
    if "主任" in combined and "人大" in post:
        return "50,100,255"
    if "副主任" in combined:
        return "50,100,255"
    if "政协" in combined:
        return "100,100,200"
    if "常委" in combined:
        return "200,100,50"
    if "部长" in combined and "组织" in combined:
        return "200,150,50"
    if "巡视员" in combined:
        return "150,150,150"
    return "100,100,100"


def person_size(name, post):
    combined = (name or "") + (post or "")
    if "党工委书记" in combined or "市委书记" in combined or "市长" in combined:
        return "20.0"
    if "主任" in combined or "政协" in combined or "常委" in combined or "部长" in combined:
        return "15.0"
    return "12.0"


def org_color(o_type):
    if "党委" in o_type:
        return "255,200,200"
    if "政府" in o_type:
        return "200,200,255"
    if "人大" in o_type:
        return "200,255,255"
    if "政协" in o_type:
        return "255,240,200"
    if "群团" in o_type:
        return "255,220,255"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>梅河口市领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"], p.get("current_post", ""))
        sz = person_size(p["name"], p.get("current_post", ""))
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o["type"])
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(p, timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "通化市",
            "region": "梅河口市",
            "job": p.get("current_post", ""),
            "task_id": "jilin_梅河口市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"meihekou_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True if p["name"] in ["朱欢", "刘铁铎"] else False,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "公开信息未发现该人物负面信号", "date": "", "confidence": "plausible", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p["name"] in ["朱欢", "刘铁铎"] else "plausible",
            "current_role": "confirmed" if p["name"] in ["朱欢", "刘铁铎"] else "plausible",
            "career_completeness": "partial" if p["name"] in ["朱欢", "刘铁铎"] else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{p['name']}: 部分履历时间段缺失" if p["name"] in ["朱欢", "刘铁铎"] else f"{p['name']}: 仅有基本职务信息，履历细节缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历，特别是早期任职经历",
                "why_it_matters": "核心人物，履历对网络分析至关重要",
                "suggested_queries": [f"{p['name']} 简历 {p.get('birthplace','')}"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    source_register = [
        {"id": "S001", "title": "梅河口市人民政府官方网站", "url": "http://www.mhk.gov.cn/",
         "publisher": "梅河口市人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "领导简历页面可访问，包含朱欢、刘铁铎、林小明等人官方简历"},
        {"id": "S002", "title": "梅河口市领导简历页面", "url": "http://www.mhk.gov.cn/xqxz/ldbz/",
         "publisher": "梅河口市人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "包含所有市领导简历"},
        {"id": "S003", "title": "澎湃新闻", "url": "https://www.thepaper.cn/",
         "publisher": "澎湃新闻", "published_at": "", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high",
         "notes": "王爱明、宋钦炜等人事任免报道"},
        {"id": "S004", "title": "快懂百科", "url": "https://www.baike.com/",
         "publisher": "快懂百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "朱欢百科资料"},
    ]

    # === 1. 朱欢 ===
    zhu_timeline = [
        {"start": "2024年6月", "end": "present", "org": "梅河新区党工委", "title": "梅河新区党工委书记、梅河口市委书记",
         "notes": "跨省交流干部，从浙江调任吉林", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"start": "2022年1月", "end": "2024年6月", "org": "宁波市人民政府", "title": "宁波市副市长",
         "notes": "浙江省宁波市副市长、市政府党组成员", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"start": "2018年", "end": "2021年", "org": "中共建德市委", "title": "建德市委书记",
         "notes": "浙江建德", "confidence": "plausible", "source_ids": ["S004"]},
        {"start": "2016年", "end": "2018年", "org": "建德市人民政府", "title": "建德市委副书记、市长",
         "notes": "浙江建德", "confidence": "plausible", "source_ids": ["S004"]},
        {"start": "unknown", "end": "2016年", "org": "杭州市西湖区", "title": "杭州市西湖区委常委、副区长",
         "notes": "", "confidence": "plausible", "source_ids": ["S004"]},
    ]
    zhu_relationships = [
        {"person": "刘铁铎", "person_id": "meihekou_刘铁铎",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "市委书记与市长作为党政主要领导搭档",
         "overlap_org": "梅河口市", "overlap_period": "2025年3月至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王爱明", "person_id": "meihekou_王爱明",
         "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "王爱明为前任市委书记",
         "overlap_org": "中共梅河口市委员会", "overlap_period": "2016年-2024年",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    zhu_json = make_person_json(persons[0], zhu_timeline, zhu_relationships, source_register)
    zhu_json["professional_profile"]["career_pattern"] = "cross_province_rotation"
    zhu_json["professional_profile"]["systems_experience"] = ["government", "party"]
    zhu_json["professional_profile"]["geographic_pattern"] = ["浙江杭州", "浙江建德", "浙江宁波", "吉林梅河口"]
    zhu_json["professional_profile"]["promotion_velocity"]["summary"] = "2022年任宁波市副市长（副厅级），2024年跨省任梅河口市委书记（副厅级），未出现异常快速晋升"
    zhu_path = PERSONS_DIR / f"{TODAY}-吉林省-通化市-市委书记-朱欢.json"
    with open(zhu_path, "w", encoding="utf-8") as f:
        json.dump(zhu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhu_path.name}")

    # === 2. 刘铁铎 ===
    liu_timeline = [
        {"start": "2025年3月", "end": "present", "org": "梅河口市人民政府", "title": "梅河口市市长",
         "notes": "2025年2月任代市长，3月正式任命", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2023年8月", "end": "2025年2月", "org": "吉林省委宣传部", "title": "省委宣传部副部长、吉林广播电视台台长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2021年11月", "end": "2023年8月", "org": "松原市人民政府", "title": "松原市委常委、常务副市长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2020年4月", "end": "2021年11月", "org": "中共松原市委宣传部", "title": "松原市委常委、宣传部部长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "2013年5月", "end": "2020年4月", "org": "共青团吉林省委员会", "title": "共青团吉林省委员会副书记",
         "notes": "兼任吉林省青年联合会主席", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "unknown", "end": "2013年5月", "org": "共青团吉林省委", "title": "共青团吉林省委城市青年工作部部长",
         "notes": "此前历任敦化市委办、共青团敦化市委、延边州委组织部、省青少年宣教中心、团省委农村部、磐石市挂职等", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    liu_relationships = [
        {"person": "朱欢", "person_id": "meihekou_朱欢",
         "relationship_type": "overlap", "strength": "strong",
         "evidence": "市长与市委书记作为党政主要领导搭档",
         "overlap_org": "梅河口市", "overlap_period": "2025年3月至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "宋钦炜", "person_id": "meihekou_宋钦炜",
         "relationship_type": "predecessor_successor", "strength": "strong",
         "evidence": "宋钦炜为前任市长",
         "overlap_org": "梅河口市人民政府", "overlap_period": "2021年-2025年",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    liu_json = make_person_json(persons[1], liu_timeline, liu_relationships, source_register)
    liu_json["professional_profile"]["career_pattern"] = "local_ladder_with_cyl_track"
    liu_json["professional_profile"]["systems_experience"] = ["government", "party", "cyl", "media"]
    liu_json["professional_profile"]["geographic_pattern"] = ["敦化", "延边", "长春", "松原", "梅河口"]
    liu_json["professional_profile"]["promotion_velocity"]["summary"] = "2013年34岁升副厅级（团省委副书记），属于团干部快速晋升通道"
    liu_path = PERSONS_DIR / f"{TODAY}-吉林省-通化市-市长-刘铁铎.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_db()
    build_gexf()
    build_person_jsons()
    print(f"\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in PERSONS_DIR.glob(f"{TODAY}-*.json"):
        print(f"  Person: {p}")
    print("Done.")
