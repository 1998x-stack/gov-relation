#!/usr/bin/env python3
"""Build script for 思南县 (Sinan County, Tongren, Guizhou) leadership network.

Generated: 2026-08-05
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note:
  Current leadership roster and biographies were CONFIRMED directly from the official
  思南县人民政府 website (www.sinan.gov.cn) — 领导之窗 (leadership window) pages for
  县委 / 县政府 / 人大 / 政协, plus 2026年7月 official news articles (县委常委会,
  县政府常务会, 县第十七届人大常委会第四十五次会议).

  Generic search engines were degraded at research time (Exa rate-limited, Baidu 403,
  Jina reader unreachable), so all facts below come from primary official sources.

  Current top-two (as of 2026-07):
    - 县委书记  陈浩 (now): 男，土家族，1976年8月生，大学学历，中共党员。
    - 县    长  张琴: 女，苗族，1984年3月出生，省委党校研究生学历，中共党员。

Sources:
  - http://www.sinan.gov.cn/zwgk/ldzc/ (思南县政府领导之窗)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211177.html (陈浩-县委书记简介)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211201.html (张琴-县长简介)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211171.html (何寻梦-副书记)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211165.html (卢忠卫-常务副县长)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202607/t20260722_90647911.html (万胜法-纪委书记)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202607/t20260727_90663162.html (潘诗文-组织部长)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211164.html (黄丽洪-政法委书记)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211194.html (滕树炳-县委办主任)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211161.html (杨光富-副县长)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211159.html (佘国旺-挂职副县长)
  - http://www.sinan.gov.cn/zwgk/ldzc/xw1/202509/t20250915_88618192.html (范俊敏-宣传部长)
  - http://www.sinan.gov.cn/zwgk/ldzc/rd1/202503/t20250320_87211213.html (刘开洪-人大主任)
  - http://www.sinan.gov.cn/zwgk/ldzc/zx1/202503/t20250320_87211222.html (祝成-政协主席)
  - http://www.sinan.gov.cn/xwzx/snyw/202607/t20260728_90665764.html (县委常委会-确认陈浩主持/张琴)
  - http://www.sinan.gov.cn/xwzx/snyw/202607/t20260729_90672752.html (张琴主持县政府第56次常务会)
  - http://www.sinan.gov.cn/xwzx/snyw/202607/t20260727_90662818.html (市委书记李作勋在思南调研)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── 核心领导：县委书记 & 县长 ──
    {
        "id": 1,
        "name": "陈浩",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委书记",
        "current_org": "中共思南县委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211177.html （官网领导之窗确认 — 男，土家族，1976年8月生，大学学历，中共党员，主持县委全面工作）",
    },
    {
        "id": 2,
        "name": "张琴",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1984年3月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委副书记、县人民政府县长",
        "current_org": "中共思南县委员会 / 思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211201.html （官网确认 — 主持县政府全面工作，负责财政、审计、粮食方面工作）",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "何寻梦",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委副书记",
        "current_org": "中共思南县委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211171.html （官网 — 协助书记抓党建，分管农业农村/乡村振兴/工青妇）",
    },
    {
        "id": 4,
        "name": "王济农",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委副书记（挂职）",
        "current_org": "中共思南县委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202509/t20250901_88545961.html （官网 — 挂职副书记，抓三农/驻村帮扶）",
    },
    # ── 县委常委 ──
    {
        "id": 5,
        "name": "万胜法",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共思南县纪律检查委员会 / 思南县监察委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202607/t20260722_90647911.html （官网 — 主持县纪委县监委全面工作）",
    },
    {
        "id": 6,
        "name": "潘诗文",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县委组织部部长、县委党校校长（兼）",
        "current_org": "中共思南县委员会组织部",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202607/t20260727_90663162.html （官网 — 主持县委组织部全面工作）",
    },
    {
        "id": 7,
        "name": "卢忠卫",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县人民政府常务副县长",
        "current_org": "思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211165.html （官网 — 协助张琴分管财政、审计，负责财税金融/人社/统计/应急等）",
    },
    {
        "id": 8,
        "name": "黄丽洪",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1981年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县委政法委书记",
        "current_org": "中共思南县委员会政法委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211164.html （官网 — 主持县委政法委全面工作）",
    },
    {
        "id": 9,
        "name": "滕树炳",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县委办公室主任、县直机关工委书记",
        "current_org": "中共思南县委员会办公室",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211194.html （官网 — 主持县委办公室全面工作）",
    },
    {
        "id": 10,
        "name": "杨光富",
        "gender": "男",
        "ethnicity": "",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县人民政府副县长",
        "current_org": "思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211161.html （官网 — 负责发改/交通/水利/移民/大数据等）",
    },
    {
        "id": 11,
        "name": "佘国旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县人民政府副县长（挂职）",
        "current_org": "思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202503/t20250320_87211159.html （官网 — 挂职，协助抓东西部协作）",
    },
    {
        "id": 12,
        "name": "范俊敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县委宣传部部长、县委统战部部长，县委教育工作委员会书记",
        "current_org": "中共思南县委员会宣传部",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202509/t20250915_88618192.html （官网 — 主持宣传部/统战部全面工作）",
    },
    {
        "id": 13,
        "name": "谢家轶",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1981年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县委常委、县人武部上校政治委员",
        "current_org": "思南县人民武装部",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xw1/202604/t20260411_89986093.html （官网）",
    },
    # ── 县政府领导 ──
    {
        "id": 14,
        "name": "张桂凤",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1975年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县人民政府副县长",
        "current_org": "思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xzf1/202503/t20250320_87211195.html （官网 — 负责卫生健康/医保/市场监管/民政/老龄）",
    },
    {
        "id": 15,
        "name": "石华意",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县人民政府（提名）副县长",
        "current_org": "思南县人民政府",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/xzf1/202607/t20260721_90646141.html （官网 — 组织提名副县长）",
    },
    # ── 人大 / 政协 ──
    {
        "id": 16,
        "name": "刘开洪",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1974年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县人大常委会党组书记、主任",
        "current_org": "思南县人民代表大会常务委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/rd1/202503/t20250320_87211213.html （官网 — 主持县人大常委会全面工作）",
    },
    {
        "id": 17,
        "name": "祝成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "思南县政协党组书记、主席",
        "current_org": "中国人民政治协商会议思南县委员会",
        "source": "http://www.sinan.gov.cn/zwgk/ldzc/zx1/202503/t20250320_87211222.html （官网 — 主持县政协全面工作）",
    },
]

ORGANIZATIONS = [
    # ── 党委系统 ──
    {
        "id": 1,
        "name": "中共铜仁市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共贵州省委员会",
        "location": "贵州省铜仁市",
    },
    {
        "id": 2,
        "name": "中共思南县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 3,
        "name": "中共思南县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共思南县委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 4,
        "name": "中共思南县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共思南县委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 5,
        "name": "中共思南县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共思南县委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 6,
        "name": "中共思南县委员会办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共思南县委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 7,
        "name": "中共思南县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共思南县委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 8,
        "name": "思南县人民武装部",
        "type": "党委",
        "level": "县级",
        "parent": "铜仁军分区",
        "location": "贵州省铜仁市思南县",
    },
    # ── 政府系统 ──
    {
        "id": 9,
        "name": "思南县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市思南县",
    },
    # ── 人大 / 政协 ──
    {
        "id": 10,
        "name": "思南县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "铜仁市人民代表大会常务委员会",
        "location": "贵州省铜仁市思南县",
    },
    {
        "id": 11,
        "name": "中国人民政治协商会议思南县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议铜仁市委员会",
        "location": "贵州省铜仁市思南县",
    },
]

POSITIONS = [
    # 陈浩 — 县委书记
    {"person_id": 1, "org_id": 2, "title": "思南县委书记", "start_date": "2024", "end_date": "present", "rank": "正县级", "note": "主持县委全面工作"},
    # 张琴 — 县委副书记兼县长
    {"person_id": 2, "org_id": 2, "title": "思南县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "思南县人民政府县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政府全面工作"},
    # 县委副书记
    {"person_id": 3, "org_id": 2, "title": "思南县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业农村/乡村振兴/群团"},
    {"person_id": 4, "org_id": 2, "title": "思南县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "驻村帮扶"},
    # 县委常委
    {"person_id": 5, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "县纪委书记、县监委代理主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "县委组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼县委党校校长"},
    {"person_id": 7, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 9, "title": "县人民政府常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "协助张琴分管财政、审计"},
    {"person_id": 8, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "县委政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "县委办公室主任、县直机关工委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "东西部协作"},
    {"person_id": 12, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "县委宣传部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "思南县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "县人民武装部上校政治委员", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 县政府副县长
    {"person_id": 14, "org_id": 9, "title": "思南县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "卫生健康/医保/民政"},
    {"person_id": 15, "org_id": 9, "title": "思南县人民政府（提名）副县长", "start_date": "2026", "end_date": "present", "rank": "副县级", "note": "2026年组织提名"},
    # 人大 / 政协
    {"person_id": 16, "org_id": 10, "title": "思南县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县人大常委会全面工作"},
    {"person_id": 17, "org_id": 11, "title": "思南县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "主持县政协全面工作"},
]

RELATIONSHIPS = [
    # ── 县委书记 ↔ 县长（搭班子） ──
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记陈浩与县长张琴搭班子",
        "overlap_org": "中共思南县委员会 / 思南县人民政府",
        "overlap_period": "现任",
    },
    # ── 县委副书记之间 ──
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "均任思南县委副书记（王济农挂职）",
        "overlap_org": "中共思南县委员会",
        "overlap_period": "现任",
    },
    # ── 县长与常务副县长 ──
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长张琴与常务副县长卢忠卫（卢忠卫协助张琴分管财政、审计）",
        "overlap_org": "思南县人民政府",
        "overlap_period": "现任",
    },
    # ── 县长与副县长 ──
    {
        "person_a": 2, "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长张琴与副县长杨光富在工作上协同（杨光富分管发改/交通/水利等）",
        "overlap_org": "思南县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 14,
        "type": "overlap",
        "context": "县长张琴与副县长张桂凤同属县政府班子成员",
        "overlap_org": "思南县人民政府",
        "overlap_period": "现任",
    },
    # ── 县委常委会内部（常委同僚关系） ──
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "同为思南县委常委会成员（陈浩-书记，万胜法-纪委书记）",
        "overlap_org": "中共思南县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "同为思南县委常委会成员（潘诗文-组织部长）",
        "overlap_org": "中共思南县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "同为思南县委常委会成员（黄丽洪-政法委书记）",
        "overlap_org": "中共思南县委员会",
        "overlap_period": "现任",
    },
    # ── 纪委书记 × 组织部长（常委共事） ──
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "县委常委会成员，分管纪检与组织工作",
        "overlap_org": "中共思南县委员会",
        "overlap_period": "现任",
    },
]

# fmt: on

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "思南县_network.db"
GEXF_PATH = STAGING_DIR / "思南县_network.gexf"


def main() -> None:
    run_build(
        slug="思南县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("✅ 思南县 network build complete.")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()