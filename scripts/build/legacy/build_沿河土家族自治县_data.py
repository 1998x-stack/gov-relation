#!/usr/bin/env python3
"""Build script for 沿河土家族自治县 (Yanhe Tujia Autonomous County, Tongren, Guizhou).

Generated: 2026-08-05
Level: 县
Province: 贵州省
Parent City: 铜仁市
Targets: 县委书记 & 县长

Research Note:
  The full current leadership roster and individual bios were CONFIRMED directly from the
  official 沿河土家族自治县人民政府 website (www.yanhe.gov.cn) — 领导之窗 (leadership
  window) pages for 县委 / 县政府 / 县人大 / 县政协 plus 2026年6-8月 official news
  (领导活动 pages).

  Current top-two (as of 2026-07/08):
    - 县委书记  张晓亮: 男，汉族，1983年8月出生，研究生（法学硕士），中共党员。
    - 代 理 县长  杨小平: 县委副书记、副县长、代理县长；男，土家族，省委党校研究生，1979年生，中共党员。

  Predecessor note: 前任县长 代忠义 (2026年3月仍以县长身份作《政府工作报告》，2026-06-29官方新闻仍称"县委副书记、县长");
  杨小平于2026年7月起任县委副书记、副县长、代理县长。前任县委书记待查。

  Cross-county / 铜仁市 cadre-exchange edges (from official individual bios):
    - 石健 (组织部长) 曾任玉屏县委常委、县委办主任
    - 董道萍 (宣传部长) 曾任思南县人大常委会副主任
    - 黄思红 (常务副县长) 曾任松桃县委常委、县委办主任
    - 向阳 (纪委书记) 曾任铜仁市纪委监委第四监督检查室主任
    - 杨义军 (副县长/公安局长) 曾任玉屏县副县长、大龙经开区党工委委员、玉屏县公安局局长
    - 文自海 (县委副书记) 曾任铜仁市生态移民局党组成员、副局长
    - 金菲 (挂职副书记), 黄效荣 (挂职常委副县长), 李冬 (挂职常委/提名副县长) — 东西部协作 / 上级下派

Sources:
  - https://www.yanhe.gov.cn/zwgk/ldzc/xwld_5982833/202606/t20260624_90550310.html (张晓亮-县委书记)
  - https://www.yanhe.gov.cn/zwgk/ldzc/xwld_5982833/202607/t20260707_90592673.html (杨小平-代理县长)
  - https://www.yanhe.gov.cn/zwgk/ldzc/xwld_5982833/... (县委班子)
  - https://www.yanhe.gov.cn/zwgk/ldzc/xfld_5982835/... (县政府班子)
  - https://www.yanhe.gov.cn/zwgk/ldzc/xrdld_5982834/... (县人大班子)
  - https://www.yanhe.gov.cn/zwgk/ldzc/xzxld_5982836/... (县政协班子)
  - https://www.yanhe.gov.cn/zwgk/xwzx/ldhd/202608/t20260803_90685988.html (2026-07 八一走访慰问 确认四家班子)
  - https://www.yanhe.gov.cn/zwgk/jczk/rsxx/rsrm/202606/t20260623_...html (人事)
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
    # ── 核心领导：县委书记 & 代理县长 ──
    {
        "id": 1,
        "name": "张晓亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "",
        "education": "研究生（法学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿河土家族自治县委书记",
        "current_org": "中共沿河土家族自治县委员会",
        "source": "http://www.yanhe.gov.cn/zwgk/ldzc/xwld_5982833/202606/t20260624_90550310.html （官网领导之窗 — 主持县委全面工作）",
    },
    {
        "id": 2,
        "name": "杨小平",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1979年",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代理县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202607/t20260707_90592673.html （官网 — 主持县政府全面工作，负责财政、审计、人事、粮食方面工作）",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "文自海",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202503/t20250324_87250815.html （官网 — 协助县委书记抓党建；曾任铜仁市生态移民局副局长）",
    },
    {
        "id": 4,
        "name": "金芳",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1982年",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（挂职）",
        "current_org": "中共沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202509/t20250909_88592493.html （官网 — 挂职副书记，协助抓农业农村、乡村振兴）",
    },
    # ── 县委常委 ──
    {
        "id": 5,
        "name": "石健",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1985年7月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长、县委党校校长",
        "current_org": "中共沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202504/t20250401_87319618.html （官网 — 曾任玉屏县委常委、县委办主任）",
    },
    {
        "id": 6,
        "name": "董道萍",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、统战部部长",
        "current_org": "中共沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202503/t20250324_87250811.html （官网 — 曾任思南县人大常委会副主任）",
    },
    {
        "id": 7,
        "name": "黄思红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202607/t20260707_90592724.html （官网 — 曾任松桃县委常委、县委办主任）",
    },
    {
        "id": 8,
        "name": "黄效荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202503/t20250324_87250806.html （官网）",
    },
    {
        "id": 9,
        "name": "向阳",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1983年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共沿河土家族自治县纪律检查委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202508/t20250815_88471288.html （官网 — 曾任铜仁市纪委监委第四监督检查室主任）",
    },
    {
        "id": 10,
        "name": "薛琳",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办主任",
        "current_org": "中共沿河土家族自治县委员会办公室",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202503/t20250324_87250855.html （官网 — 曾任沿河县政府党组成员、副县长）",
    },
    {
        "id": 11,
        "name": "刘庆军",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1977年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长、经开区党工委副书记",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldfq/...87250854.html （官网：曾任沿河经开区管委会副主任）",
    },
    {
        "id": 12,
        "name": "李冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、提名副县长（挂职）",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xwl_5982833/202607/t20260730_90677982.html （官网）",
    },
    # ── 县政府领导班子 ──
    {
        "id": 13,
        "name": "汪涛",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202503/t20250324_87250856.html （官网：曾任沿河经开区党工委委员、副主任）",
    },
    {
        "id": 14,
        "name": "杨义军",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府副县长、县公安局局长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202508/t20250825_88513049.html （官网：曾任玉屏县副县长、大龙经开区党工委委员、玉屏县公安局局长）",
    },
    {
        "id": 15,
        "name": "白静明",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1981年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202503/t20250324_87250853.html （官网：曾任沿河县中寨镇党委副书记、镇长）",
    },
    {
        "id": 16,
        "name": "杨妮",
        "gender": "女",
        "ethnicity": "侗族",
        "birth": "1981年",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、提名副县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202607/t20260730_90677927.html （官网）",
    },
    {
        "id": 17,
        "name": "张禹",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1986年9月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府副县长",
        "current_org": "沿河土家族自治县人民政府",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202604/t20260415_90007056.html （官网，负责农业农村、乡村振兴）",
    },
    {
        "id": 18,
        "name": "刘承大",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民政府办公室党组书记、主任",
        "current_org": "沿河土家族自治县人民政府办公室",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzfld_5982835/202503/t20250324_87250852.html （官网）",
    },
    # ── 县人大班子 ──
    {
        "id": 19,
        "name": "杨超",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1972年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "沿河土家族自治县人民代表大会常务委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/crdld_5982834/202503/t20250324_87250882.html （官网 — 主持县人大常委会全面工作）",
    },
    {
        "id": 20,
        "name": "周宗烈",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1969年4月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "沿河土家族自治县人民代表大会常务委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xrdld_5982834/202503/t20250324_87250847.html （官网）",
    },
    {
        "id": 21,
        "name": "张金珠",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "民盟",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "沿河土家族自治县人民代表大会常务委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xrdld_5982834/202603/t20260327_89915607.html （官网）",
    },
    # ── 县政协班子 ──
    {
        "id": 22,
        "name": "崔永龙",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协党组书记、主席",
        "current_org": "中国人民政治协商会议沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzxld_5982836/202603/t20260318_89883768.html （官方 — 主持县政协全面工作）",
    },
    {
        "id": 23,
        "name": "孙勇",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldzc/xzxld_5982836/202503/t20250324_87250870.html （官网）",
    },
    {
        "id": 24,
        "name": "田小東",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1977年1月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议沿河土家族自治县委员会",
        "source": "https://www.yanhe.gov.cn/zwgk/ldg/xzxld_5982836/202503/t20250324_87250876.html （官网）",
    },
]

ORGANIZATIONS = [
    # ══ 党委系统 ══
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
        "name": "中共沿河土家族自治县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共铜仁市委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 3,
        "name": "中共沿河土家族自治县委员会纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共沿河土家族自治县委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 4,
        "name": "中共沿河土家族自治县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沿河土家族自治县委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 5,
        "name": "中共沿河土家族自治县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沿河土家族自治县委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 6,
        "name": "中共沿河土家族自治县委员会办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共沿河土家族自治县委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    # ══ 政府系统 ══
    {
        "id": 7,
        "name": "沿河土家族自治县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "铜仁市人民政府",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 8,
        "name": "沿河土家族自治县经济开发区",
        "type": "开发区",
        "level": "县级",
        "parent": "沿河土家族自治县人民政府",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 9,
        "name": "沿河土家族自治县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "沿河土家族自治县人民政府",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    # ══ 人大 / 政协 ══
    {
        "id": 10,
        "name": "沿河土家族自治县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "铜仁市人民代表大会常务委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
    {
        "id": 11,
        "name": "中国人民政治协商会议沿河土家族自治县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议铜仁市委员会",
        "location": "贵州省铜仁市沿河土家族自治县",
    },
]

POSITIONS = [
    # 张晓亮 — 县委书记
    {"person_id": 1, "org_id": 2, "title": "沿河土家族自治县委书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    # 杨小平 — 代理县长
    {"person_id": 2, "org_id": 2, "title": "沿河县委副书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "县人民政府代理县长", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作"},
    # 县委副书记
    {"person_id": 3, "org_id": 2, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助书记抓党建"},
    {"person_id": 4, "org_id": 2, "title": "县委副书记（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助抓农业农村、乡村振兴"},
    # 县委常委
    {"person_id": 5, "org_id": 2, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼县委党校校长"},
    {"person_id": 6, "org_id": 2, "title": "县委常委、宣传部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼县委教育工委书记"},
    {"person_id": 7, "org_id": 7, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助县长抓财政审计"},
    {"person_id": 8, "org_id": 7, "title": "县委常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "东西部协作"},
    {"person_id": 9, "org_id": 3, "title": "县委常委、县纪委书记、县监委代理主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "主持县纪委县监委工作"},
    {"person_id": 10, "org_id": 6, "title": "县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "县委常委、副县长、经开区党工委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "县委常委、提名副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 县政府副县长
    {"person_id": 8, "org_id": 7, "title": "县人民政府副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 7, "title": "县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "教育卫生"},
    {"person_id": 14, "org_id": 9, "title": "县人民政府副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 7, "title": "县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "县政府党组成员、提名副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 7, "title": "县人民政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "农业农村/乡村振兴"},
    {"person_id": 18, "org_id": 7, "title": "县人民政府办公室主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 人大
    {"person_id": 19, "org_id": 10, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县人大常委会工作"},
    {"person_id": 20, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "民盟盟员"},
    # 政协
    {"person_id": 22, "org_id": 11, "title": "县政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政协工作"},
    {"person_id": 23, "org_id": 11, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 24, "org_id": 11, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

RELATIONSHIPS = [
    # ── 县委书记 ↔ 代理县长（搭班子） ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记张晓亮与代理县长杨小平搭班子", "overlap_org": "中共沿河县委 / 沿河县政府", "overlap_period": "2026-至今"},
    # ── 县委副书记之间 ──
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同任县委副书记（金芳挂职）", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    # ── 县长与常务副县长 ──
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "代理县长杨小平与常务副县长黄思红（副手）", "overlap_org": "沿河县人民政府", "overlap_period": "2026-至今"},
    # ── 县长与副县长（班子同僚） ──
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县政府班子（汪涛-副县长）", "overlap_org": "沿河县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县政府班子（杨义军-副县长/公安局长）", "overlap_org": "沿河县人民政府", "overlap_period": "现任"},
    # ── 常委同僚关系 ──
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "同为县委常委会成员（石健-组织部长）", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "同为县委常委会成员（董道萍-宣传部长）", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "同为县委常委会成员（向阳-纪委书记）", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "同为县委常委会成员（杨小平+向阳）", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    # ── 铜仁市内部跨县交流（曾同县/同系统） ──
    {"person_a": 5, "person_b": 14, "type": "cross_county", "context": "石健与杨义军曾在玉屏任职（石健-玉屏县委常委、杨义军-玉屏副县长/公安局长）", "overlap_org": "贵州省铜仁市玉屏县", "overlap_period": "任职玉屏时期"},
    {"person_a": 6, "person_b": 19, "type": "cross_county", "context": "董道萍曾任思南县人大常委会副主任", "overlap_org": "贵州省铜仁市思南县", "overlap_period": "任职时期"},
    {"person_a": 7, "person_b": 14, "type": "cross_county", "context": "黄思红曾任松桃县委常委，杨义军曾任玉屏副县，均在铜仁市相邻县区", "overlap_org": "贵州省铜仁市", "overlap_period": "任职时期"},
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "向阳（纪委书记）在张晓亮（书记）领导下推进正风肃纪", "overlap_org": "中共沿河县委", "overlap_period": "现任"},
    {"person_a": 11, "person_b": 8, "type": "overlap", "context": "同属县政府领导（刘庆军-经开区、黄效荣-挂职）", "overlap_org": "沿河县人民政府", "overlap_period": "现任"},
    {"person_a": 19, "person_b": 22, "type": "overlap", "context": "县四家班子（人大主任杨超 & 政协主席崔永龙）", "overlap_org": "沿河县四家班子", "overlap_period": "现任"},
]
# fmt: on

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "沿河土家族自治县_network.db"
GEXF_PATH = STAGING_DIR / "沿河土家族自治县_network.gexf"

def main():
    run_build(
        slug="沿河土家族自治县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("沿河土家族自治县 network build complete.")
    print("  DB:   {}".format(DB_PATH))
    print("  GEXF: {}".format(GEXF_PATH))


if __name__ == "__main__":
    main()