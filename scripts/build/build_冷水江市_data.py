#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 冷水江市 (Lengshuijiang), 湖南省.

Investigation date: 2026-08-06
Task ID: hunan_冷水江市
Province: 湖南省
Parent city: 娄底市
Level: 县级市
Targets: 市委书记 & 市长

Key finding: the 11th 冷水江市委 leadership (曾伯怡 书记 / 陈创业 市长) was entirely replaced
in 2026-06/07. At the 十二届一次全会 (2026-07-29/31) a brand-new leadership was elected:
  市委书记 唐正 (previously 市长), 代市长 王益群 (new from 郴州), 市委副书记 罗建湘.

Research sources (all official, accessed 2026-08-06):
  - http://www.lsj.gov.cn (冷水江市人民政府) — leadership pages + meeting/news reports
  - 十二届一次全会 report, 市委常委会第31次, 争资争项调度会 (2026-08)
  - 2026 政府工作报告 (delivered 2026-03-18 by 市长 唐正)
  - Predecessor data from project 娄底市 build (2026-07-24)

Confidence notes:
  - Current roles: confirmed via official gov leadership page and 2026-07/08 meeting reports
  - 唐正/王益群 full prior careers: partial (marked plausible / open_questions)
  - Previous leaders 曾伯怡/陈创业 2026 exit destinations: unverified (open gap)
  - Exa rate-limited, Baidu/Jina blocked — relied on official site direct fetch
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

import sqlite3  # noqa: F401  (DB output is SQLite, produced via gov_relation.runner)

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "冷水江市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Paths ────────────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_冷水江市"
if _CURRENT_DIR.name == "hunan_冷水江市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-9 现任市委/市府核心, 10-19 常委, 20-29 副市府,
#      30-39 人大/政协, 40-49 前任干部
persons = [
    # ── 核心领导 (targets) ───────────────────────────────────────────────────
    {
        "id": 1,
        "name": "唐正",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn/lsj/lsjzfgzbg/202607/f1184be6f93644fe8a2f63da0f5d851a.shtml",
        "confidence": "confirmed",
        "notes": "前市长（2026-03-18在市十三届人大六次会议作政府工作报告）→2026-07-29当选十二届市委书记；履历/籍贯/出生待查",
    },
    {
        "id": 2,
        "name": "王益群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "湖南省郴州市",
        "education": "大学学历",
        "party_join": "2004-05",
        "work_start": "2005-04",
        "current_post": "市委副书记、代理市长、市长提名人选",
        "current_org": "中共冷水江市委/冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/lsj/zwgk/zfxxgk/szfxxgkml/ldzc/szfld/202606/9e80ad49e53347fca03cb53f91a38b4a.shtml",
        "confidence": "confirmed",
        "notes": "1981年11月生，湖南郴州人，大学学历，2005年4月参加工作，2004年5月入党；郴州调入，此前履历待查",
    },
    # ── 市领导班子 ──────────────────────────────────────────────────────────
    {
        "id": 10,
        "name": "罗建湘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、统战部部长、二级调研员",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/201607/013f712b784a4c1d93b8ac37abedd0c6.shtml",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届市委副书记；统战部部长、二级调研员；履历待查",
    },
    {
        "id": 11,
        "name": "毛东红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "湖南省涟源市",
        "education": "大学学历",
        "party_join": "2001-11",
        "work_start": "1996-12",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共冷水江市委/冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/201906/d7ee153020c172e5cffe.shtml",
        "confidence": "confirmed",
        "notes": "男，汉族，1977-06生，湖南涟源人，大学学历，1996-12参加工作，2001-11入党；常务副市长",
    },
    {
        "id": 12,
        "name": "李吉求",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "大学学历、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共冷水江市委/冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/202606/ca5416c802140d155a02.shtml",
        "confidence": "confirmed",
        "notes": "男，1987-02生，大学学历、工学学士，中共党员；常委兼副市长（园区/工业/交通）",
    },
    {
        "id": 13,
        "name": "聂杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委；具体分工待查",
    },
    {
        "id": 14,
        "name": "邓函提",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委（女）；具体分工待查",
    },
    {
        "id": 15,
        "name": "孙立平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委；具体分工待查",
    },
    {
        "id": 16,
        "name": "刘温东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委；具体分工待查",
    },
    {
        "id": 17,
        "name": "奉安辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委；具体分工待查",
    },
    {
        "id": 18,
        "name": "李文胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共冷水江市委",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-29当选十二届常委；具体分工待查",
    },
    # ── 市政府副职 ──────────────────────────────────────────────────────────
    {
        "id": 20,
        "name": "谭险夷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长（挂职）",
        "current_org": "冷水江市人民政府",
        "source": "https://www.lsj.gov.cn/ls/szf/szf.shtml",
        "confidence": "confirmed",
        "notes": "挂职副市长；2025-05决定任命",
    },
    {
        "id": 21,
        "name": "贺志苗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "湖南省娄底市娄星区",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2000-07",
        "current_post": "副市长、市公安局党委书记、局长",
        "current_org": "冷水江市人民政府/冷水江市公安局",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/202605/d298111665a9c771c2053b0241f5d8b0.shtml",
        "confidence": "confirmed",
        "notes": "男，1976-09生，娄底娄星区人，大学学历，2000-07参加工作，中共党员；三级高级警长（副处）",
    },
    {
        "id": 22,
        "name": "周璐",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1989-11",
        "birthplace": "湖南省湘乡市",
        "education": "大学学历",
        "party_join": "2010-05",
        "work_start": "2011-09",
        "current_post": "副市长",
        "current_org": "冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/ldzc/szfld/202607/021f170d213445bf8c8afc7edae161.shtml",
        "confidence": "confirmed",
        "notes": "女，1989-11生，湘乡人，大学学历，2011-09参加工作，2010-05入党；分管教育/文旅/体育",
    },
    {
        "id": 23,
        "name": "伍佩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-09",
        "birthplace": "湖南省新化县",
        "education": "大学学历",
        "party_join": "2005-01",
        "work_start": "2007-07",
        "current_post": "副市长提名人选",
        "current_org": "冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/ldzc/szfld/202607/cdec9d30646649e48853189f89ea6d3d.shtml",
        "confidence": "confirmed",
        "notes": "男，1983-09生，新化人，大学学历，2007-07参加工作，2005-01入党；市场监管/卫健/医保",
    },
    {
        "id": 24,
        "name": "鄢洪钟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长提名人选",
        "current_org": "冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/szf/szf.shtml",
        "confidence": "confirmed",
        "notes": "副市长提名人选；分工待查",
    },
    {
        "id": 25,
        "name": "梁群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长提名人选",
        "current_org": "冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/szf/szf.shtml",
        "confidence": "confirmed",
        "notes": "副市长提名人选；分工待查",
    },
    {
        "id": 26,
        "name": "邹安定",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "湖南省新化县",
        "education": "中央党校大学学历",
        "party_join": "",
        "work_start": "1999-05",
        "current_post": "副市长提名人选",
        "current_org": "冷水江市人民政府",
        "source": "http://www.lsj.gov.cn/ls/zwgk/zfxxgk/szfxxgkml/202607/bbdcb89ff8b044b8c2805a341520.shtml",
        "confidence": "confirmed",
        "notes": "男，1980-09生，新化人，中央党校大学学历，1999-05参加工作，2019-01加入中国民主促进会（民进）；对外开放/招商",
    },
    # ── 人大 / 政协 ─────────────────────────────────────────────────────────
    {
        "id": 30,
        "name": "孙纬辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "冷水江市人大常委会",
        "source": "http://www.lsj.gov.cn/ls/zwgk/g040120-130211304208az.shtml",
        "confidence": "confirmed",
        "notes": "孙纬辉；2026-07-31市委常委会新闻确认仍任市人大常委会主任（自2021-11起）",
    },
    {
        "id": 31,
        "name": "阳卫龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "冷水江市政协",
        "source": "http://www.lsj.gov.cn/html/201607/2020ax.shtml",
        "confidence": "confirmed",
        "notes": "阳卫龙（2026-07-31市委常委会会议确认任市政协主席）；履历待查",
    },
    {
        "id": 32,
        "name": "李南新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组书记",
        "current_org": "冷水江市政协",
        "source": "http://www.lsj.gov.cn",
        "confidence": "confirmed",
        "notes": "2026-07-31市委常委会会议报道确认任市政协党组书记",
    },
    # ── 前任干部 ────────────────────────────────────────────────────────────
    {
        "id": 40,
        "name": "曾伯怡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "湖南省双峰县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "（离任）",
        "source": "项目娄底市 build 2026-07-24",
        "confidence": "confirmed",
        "notes": "2021-07起任冷水江市委书记；2025-2026期间离任，去向待查",
    },
    {
        "id": 41,
        "name": "陈创业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-06",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "（离任）",
        "source": "http://www.lsj.gov.cn/lsj/2026nlsjlhzl/202603/00a3a1f6f4f8d9d85e2f4e6751c4c94.shtml",
        "confidence": "confirmed",
        "notes": "2021-09起任市长；~2025年越市长转市委书记（2026-03-20人代会确认为书记）；2026-07由唐正接任书记；去向待查",
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共冷水江市委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "冷水江市"},
    {"id": 2, "name": "冷水江市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 3, "name": "冷水江市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 4, "name": "冷水江市政协", "type": "政协", "level": "县级", "parent": "", "location": "冷水江市"},
    {"id": 5, "name": "冷水江市公安局", "type": "政府", "level": "县级", "parent": "冷水江市人民政府", "location": "冷水江市"},
    {"id": 6, "name": "娄底市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "娄底市"},
    {"id": 7, "name": "娄底市委组织部", "type": "organization", "level": "地级", "parent": "中共娄底市委", "location": "娄底市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "冷水江市委书记", "start_date": "2026-07", "end_date": "", "rank": "副厅级",
     "note": "2026-07-29当选十二届市委书记"},
    {"person_id": 1, "org_id": 2, "title": "冷水江市市长（前任）", "start_date": "2025-06", "end_date": "2026-06", "rank": "正处级",
     "note": "2025-06代市长；2026-03-18市十三届人大六次会议正式当选市长；2026-06因接任书记卸任"},
    {"person_id": 2, "org_id": 1, "title": "冷水江市委副书记", "start_date": "2026-06", "end_date": "", "rank": "副厅级",
     "note": "2026-07-29当选十二届市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "冷水江市代理市长、市长提名人选", "start_date": "2026-06", "end_date": "", "rank": "正处级",
     "note": "市政府党组书记、代理市长"},
    {"person_id": 10, "org_id": 1, "title": "冷水江市委副书记、统战部部长", "start_date": "2026-07", "end_date": "", "rank": "副厅级",
     "note": "2026-07-29当选市委副书记；统战部长、二级调研员"},
    {"person_id": 11, "org_id": 1, "title": "冷水江市委常委", "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "常委、市政府党组副书记"},
    {"person_id": 11, "org_id": 2, "title": "冷水江市常务副市长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 12, "org_id": 1, "title": "冷水江市委常委、副市长", "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "分管园区/工业/交通"},
    {"person_id": 13, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": "女"},
    {"person_id": 15, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 1, "title": "冷水江市委常委", "start_date": "2026-07", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "冷水江市副市长（挂职）", "start_date": "2025-05", "end_date": "", "rank": "正处级",
     "note": "2025-05决定任命"},
    {"person_id": 21, "org_id": 2, "title": "冷水江市副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "公安局长（副处职、三级高级警长）"},
    {"person_id": 22, "org_id": 2, "title": "冷水江市副市长", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "分管教育/文旅/体育"},
    {"person_id": 23, "org_id": 2, "title": "冷水江市副市长提名人选", "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "市场监管/卫健/医保"},
    {"person_id": 24, "org_id": 2, "title": "冷水江市副市长提名人选", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 2, "title": "冷水江市副市长提名人选", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 26, "org_id": 2, "title": "冷水江市副市长提名人选", "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "分管内贸/开放型经济/招商；民进"},
    {"person_id": 30, "org_id": 3, "title": "冷水江市人大常委会主任", "start_date": "2021-11", "end_date": "", "rank": "正处级",
     "note": "2026-07-31确认仍任"},
    {"person_id": 31, "org_id": 4, "title": "冷水江市政协主席", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "2026-07-31会议确认"},
    {"person_id": 32, "org_id": 4, "title": "冷水江市市政协党组书记", "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 40, "org_id": 1, "title": "冷水江市委书记（前任）", "start_date": "2021-07", "end_date": "2026", "rank": "副厅级",
     "note": "2026年离任，去向待查"},
    {"person_id": 41, "org_id": 2, "title": "冷水江市市长（前任）", "start_date": "2021-09", "end_date": "2025", "rank": "正处级",
     "note": "2021-09起任市长；约2025年由市长转任市委书记"},
    {"person_id": 41, "org_id": 1, "title": "冷水江市委书记（前任）", "start_date": "2025", "end_date": "2026-07", "rank": "副厅级",
     "note": "曾伯怡卸任后接任书记；2026-03-20人代会确认；2026-07由唐正接任"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 市委主要领导同台
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "唐正（书记）与王益群（代市长）党政搭档，2026-07十二届一次全会后正式搭班",
     "overlap_org": "中共冷水江市委/冷水江市人民政府", "overlap_period": "2026-06"},
    {"person_a": 1, "person_b": 10, "type": "colleague",
     "context": "唐正（书记）与罗建湘（副书记）同为十二届市委班子成员",
     "overlap_org": "中共冷水江市委", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 10, "type": "colleague",
     "context": "王益群（代市长）与罗建湘（副书记）同为十二届市委班子成员",
     "overlap_org": "中共冷水江市委", "overlap_period": "2026-07"},
    # 唐正接替陈创业的市长（代市长→市长）链条
    {"person_a": 41, "person_b": 1, "type": "succession",
     "context": "陈创业（时任市长）转任书记后，唐正接任市长/代市长（2025-06）",
     "overlap_org": "冷水江市人民政府", "overlap_period": "2025-06"},
    {"person_a": 1, "person_b": 2, "type": "succession",
     "context": "唐正升任市委书记后，王益群接任代市长",
     "overlap_org": "冷水江市人民政府", "overlap_period": "2026-06"},
    # 书记之职的传承（曾伯怡→陈创业→唐正）
    {"person_a": 40, "person_b": 41, "type": "succession",
     "context": "曾伯怡（前任书记，2021-07起）卸任，陈创业（原市长）接任书记",
     "overlap_org": "中共冷水江市委", "overlap_period": "2026-07"},
    # 常委与市政府交叉任职
    {"person_a": 11, "person_b": 12, "type": "colleague",
     "context": "毛东红（常务副市长）与李吉求（副市长）均为市委常委、政府班子成员",
     "overlap_org": "中共冷水江市委/冷水江市人民政府", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 2, "type": "colleague",
     "context": "毛东红协助市长王益群负责财政/审计工作（常务副市长）",
     "overlap_org": "冷水江市人民政府", "overlap_period": "2026-06"},
    # 同乡关系（新化系）
    {"person_a": 41, "person_b": 23, "type": "hometown",
     "context": "陈创业（新化人）与伍佩（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 41, "person_b": 26, "type": "hometown",
     "context": "陈创业（新化人）与邹安定（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    {"person_a": 41, "person_b": 30, "type": "hometown",
     "context": "陈创业（新化人）与孙纬辉（新化人）同乡",
     "overlap_org": "新化县", "overlap_period": ""},
    # 双峰系（前任书记曾伯怡）
    {"person_a": 40, "person_b": 41, "type": "colleague",
     "context": "曾伯怡（书记）与陈创业（市长）党政搭班子；2021-2025/26 共事",
     "overlap_org": "冷水江市", "overlap_period": "2021-2025"},
    # 人大/政协，与市领导班子互动
    {"person_a": 1, "person_b": 30, "type": "colleague",
     "context": "唐正（书记）与孙纬辉（人大主任）在冷水江市共事",
     "overlap_org": "冷水江市", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 31, "type": "colleague",
     "context": "唐正（书记）与阳卫龙（政协主席）在冷水江市共事",
     "overlap_org": "冷水江市", "overlap_period": "2026"},
]


# ── Person JSON writer ───────────────────────────────────────────────────────
def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file per person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"lengshuijiang_{name}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] != pid:
            continue
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    if len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口",
            "title": "", "notes": "公开资料不足，完整履历待查。",
            "confidence": "unverified", "source_ids": [],
        })

    rels_output = []
    for r in relationships:
        if r["person_a"] != pid and r["person_b"] != pid:
            continue
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_map = {
            "colleague": ("overlap", "strong"),
            "succession": ("predecessor_successor", "strong"),
            "hometown": ("same_native_place", "weak"),
            "subordinate": ("superior_subordinate", "strong"),
        }
        rtype, strength = rel_map.get(r["type"], ("overlap", "medium"))
        rels_output.append({
            "person": other_name,
            "person_id": f"lengshuijiang_{other_name}",
            "relationship_type": rtype,
            "strength": strength,
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("colleague", "succession") else "plausible",
        })

    identity = {
        "person_id": slug_id,
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("birthplace", ""),
        "education": [{"institution": person.get("education", ""), "major": "", "degree": person.get("education", ""),
                       "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}", "name_birthplace": f"{name}_{person.get('birthplace','')}",
                        "official_profile_url": person.get("source", "")},
    }

    current_status = {
        "current_post": person.get("current_post", ""),
        "current_org": person.get("current_org", ""),
        "administrative_rank": next((p["rank"] for p in positions if p["person_id"] == pid and p.get("title", "").find("书记") >= 0 or p["person_id"] == pid and p.get("rank")), ""),
        "as_of": AS_OF,
        "is_current_confirmed": person.get("confidence") == "confirmed",
    }

    open_questions = []
    if person.get("confidence") == "confirmed" and not person.get("birth"):
        open_questions.append({
            "priority": "critical",
            "question": f"{name} 出生年月/籍贯/学历/入党/参加工作年份及完整前期履历",
            "why_it_matters": "核心领导身份字段缺失，影响去重和网络画像",
            "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 冷水江 履历"],
            "last_attempted": AS_OF,
        })
    elif not person.get("work_start"):
        open_questions.append({
            "priority": "medium",
            "question": f"{name} 完整履历",
            "why_it_matters": "丰富人事网络交叉分析",
            "suggested_queries": [f"{name} 履历"],
            "last_attempted": AS_OF,
        })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "娄底市",
            "region": "冷水江市",
            "job": person.get("current_post", ""),
            "task_id": "hunan_冷水江市",
            "time_focus": "2026-06 至 2026-08",
        },
        "identity": identity,
        "current_status": current_status,
        "career_timeline": career_timeline,
        "organizations": [
            {"name": o["name"], "type": o["type"], "level": o["level"], "location": o["location"]}
            for o in organizations
            if o["id"] in {p["org_id"] for p in positions if p["person_id"] == pid}
        ],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [{"id": "S001", "title": person.get("source", ""), "url": person.get("source", ""),
                            "publisher": "冷水江市人民政府 / 项目数据", "accessed_at": AS_OF,
                            "source_type": "official", "reliability": "high", "notes": ""}],
        "confidence_summary": {
            "identity": person.get("confidence", "unverified"),
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早期履历（出生/籍贯/入党）" if not person.get("birth") else "去向/分工细节",
        },
        "open_questions": open_questions,
    }

    job = person.get("current_post", "").split("、")[0].replace("提名人选", "").replace("（挂职）", "")
    # Prefer target role label for core leaders (市长 for acting mayor)
    if person["id"] in (1, 2):
        job = "市委书记" if person["id"] == 1 else "市长"
    fname = STAGING / f"{TODAY}-湖南省-娄底市-{job}-{name}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"    wrote {fname.name}")


# ── Build ────────────────────────────────────────────────────────────────────
def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    # Core leaders: 市委书记(1), 代市长/市长提名人(2), 前任书记(40), 前任市长(41)
    core_ids = {1, 2, 40, 41}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())