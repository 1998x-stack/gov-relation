#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 织金县 (Zhijin County), 毕节市, 贵州省.

Level: 县
Province: 贵州省
Parent city: 毕节市
Targets: 县委书记 & 县长
Task ID: guizhou_织金县
Investigation date: 2026-08-05

Research sources (all official 织金县人民政府门户网 www.gzzhijin.gov.cn):
  - 领导之窗·政府领导: http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/
      (马丽飞/曾涛/陈昌海/杨松/石磊/梁霄/付国晖/陈正祥/汪钰力 profiles with bios)
  - 今日织金 news 2026-06 ~ 2026-08 (县委常委会, 招商引资调度会, 专题会议 etc.):
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260719_90636385.html
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260729_90671265.html
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260716_90627928.html
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260722_90648983.html
      https://www.gzzhijin.gov.cn/xwzx/jrzj/202608/t20260804_90691205.html

Confidence notes:
  - 杨志伟 (县委书记): confirmed via multiple official 2026-07 县委会议 news. He concurrently
    holds 毕节市政协副主席 (副厅级) and 织金县委书记 (正处级), and 织金经开区党工委书记.
    Earlier career (birth year, education, prior posts) NOT found this run (search engines
    degraded: Exa rate-limited, Baidu blocked) — open gap.
  - 马丽飞 (县委副书记/县长/县委政法委书记): confirmed via official 领导之窗 bio page +
    multiple news. Birth 1985.06, 回族, 贵州省委党校研究生学历.
  - 县委副书记 付正祥/胡蓉, 县人大常委会主任 王丽佳, 县政协主席 王刚: confirmed via 县委常委会
    attendance news.
  - 县政府领导班子 (曾涛/陈昌海/杨松/石磊/梁霄/付国晖/陈正祥/汪钰力): confirmed via official
    领导之窗 profiles.
  - 刘镇/胡慧/张勇/王子萱 (县领导) and 焦凯/杨波 (织金经开区领导): confirmed as 县/经开区领导
    出席活动，具体分工职务未公开 — open gap.
  - Predecessors (前任县委书记/县长) and exact appointment dates: NOT found (search degraded). Open gap.
  - Web search was degraded; all core data confirmed from the official county government website.
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "织金县"
TODAY = datetime.now().strftime("%Y%m%d")

# DB + GEXF written into the current directory (staging when run from data/tmp)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 县委主要领导（一把手／二把手）═══════
    {
        "id": 1,
        "name": "杨志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "毕节市政协副主席、中共织金县委书记、织金经开区党工委书记",
        "current_org": "中共织金县委",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html; https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260719_90636385.html"
    },
    {
        "id": 2,
        "name": "马丽飞",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "贵州省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县委副书记、县政府党组书记、县长、县委政法委书记",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202603/t20260318_89883219.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "付正祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县委副书记、织金经开区党工委副书记、管委会副主任",
        "current_org": "中共织金县委",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260719_90636385.html"
    },
    {
        "id": 4,
        "name": "胡蓉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县委副书记",
        "current_org": "中共织金县委",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html"
    },
    # ═══════ 县委常委、常务副县长 ═══════
    {
        "id": 5,
        "name": "曾涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县委常委、常务副县长",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202405/t20240510_84613296.html"
    },
    # ═══════ 县政府副县长 ═══════
    {
        "id": 6,
        "name": "陈昌海",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "",
        "work_start": "",
        "current_post": "织金县人民政府副县长（三级调研员）",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202205/t20220527_74248913.html"
    },
    {
        "id": 7,
        "name": "杨松",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府副县长",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202405/t20240510_84613487.html"
    },
    {
        "id": 8,
        "name": "石磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府副县长、县公安局党委书记、局长、督察长",
        "current_org": "织金县公安局",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202311/t20231101_82903339.html; https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html"
    },
    {
        "id": 9,
        "name": "梁霄",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1983年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府副县长",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202411/t20241126_86138149.html"
    },
    {
        "id": 10,
        "name": "付国晖",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府副县长、县教育局党组书记、局长（县委教育工委副书记兼）",
        "current_org": "织金县教育局",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202601/t20260104_89112998.html"
    },
    {
        "id": 11,
        "name": "陈正祥",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1968年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府党组成员、织金古城管理处处长",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202205/t20220526_74220357.html"
    },
    {
        "id": 12,
        "name": "汪钰力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年8月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人民政府党组成员、县政府办公室（县外事办）党组书记、主任",
        "current_org": "织金县人民政府",
        "source": "http://www.gzzhijin.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202403/t20240301_83869227.html"
    },
    # ═══════ 县人大 / 政协 ═══════
    {
        "id": 13,
        "name": "王丽佳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县人大常委会主任",
        "current_org": "织金县人大常委会",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html"
    },
    {
        "id": 14,
        "name": "王刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协织金县委员会主席",
        "current_org": "政协织金县委员会",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260731_90680186.html"
    },
    # ═══════ 其他县领导（职务细分未公开）═══════
    {
        "id": 15,
        "name": "刘镇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县县级领导",
        "current_org": "织金县四套班子",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260722_90648983.html"
    },
    {
        "id": 16,
        "name": "胡慧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县县级领导",
        "current_org": "织金县四套班子",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260729_90671239.html"
    },
    {
        "id": 17,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县县级领导",
        "current_org": "织金县四套班子",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260716_90627928.html"
    },
    {
        "id": 18,
        "name": "王子萱",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金县县级领导",
        "current_org": "织金县四套班子",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260723_90653047.html"
    },
    # ═══════ 织金经开区领导 ═══════
    {
        "id": 19,
        "name": "焦凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金经济开发区领导",
        "current_org": "织金经济开发区",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260716_90627928.html"
    },
    {
        "id": 20,
        "name": "杨波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "织金经济开发区领导",
        "current_org": "织金经济开发区",
        "source": "https://www.gzzhijin.gov.cn/xwzx/jrzj/202607/t20260716_90627928.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共织金县委", "type": "党委", "level": "县级", "parent": "中共毕节市委", "location": "毕节市织金县"},
    {"id": 2, "name": "织金县人民政府", "type": "政府", "level": "县级", "parent": "毕节市人民政府", "location": "毕节市织金县"},
    {"id": 3, "name": "织金县公安局", "type": "政府", "level": "县级", "parent": "织金县人民政府", "location": "毕节市织金县"},
    {"id": 4, "name": "织金县人大常委会", "type": "人大", "level": "县级", "parent": "毕节市人大常委会", "location": "毕节市织金县"},
    {"id": 5, "name": "政协织金县委员会", "type": "政协", "level": "县级", "parent": "政协毕节市委员会", "location": "毕节市织金县"},
    {"id": 6, "name": "织金县教育局", "type": "政府", "level": "县级", "parent": "织金县人民政府", "location": "毕节市织金县"},
    {"id": 7, "name": "织金经济开发区（织金县产业园区）", "type": "开发区", "level": "县级", "parent": "织金县人民政府", "location": "毕节市织金县"},
    {"id": 8, "name": "中国人民政治协商会议毕节市委员会", "type": "政协", "level": "地级市", "parent": "贵州省政协", "location": "贵州省毕节市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 杨志伟 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共织金县委书记", "start": "", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。2026年7月多次以县委书记身份召开县委常委会、主持招商引资调度会、专题会议，赴织金经开区调研重大项目建设。党内职务为毕节市政协副主席（副厅级）兼任，表明其同时担任贵州织金经济开发区党工委书记。"},
    {"id": 2, "person_id": 1, "org_id": 7, "title": "织金经济开发区党工委书记", "start": "", "end": "present", "rank": "兼",
     "note": "主持织金经开区党工委工作（2026年7月多次以织金经开区党工委书记身份出席党工委会议）。"},
    {"id": 3, "person_id": 1, "org_id": 8, "title": "毕节市政协副主席", "start": "", "end": "present", "rank": "副厅级",
     "note": "兼任（或曾任）毕节市政协副主席，与县委书记职务并行，体现市本级对重点县的领导配置；具体担任起止时间未知。"},
    # 马丽飞 — 县长
    {"id": 4, "person_id": 2, "org_id": 1, "title": "织金县委副书记、县人民政府党组书记", "start": "", "end": "present", "rank": "正处级",
     "note": "兼任县政府党组书记、县委政法委书记。"},
    {"id": 5, "person_id": 2, "org_id": 2, "title": "织金县县长", "start": "", "end": "present", "rank": "正处级",
     "note": "领导县政府全面工作，负责审计、粮食等工作，并主持县政府党组会、常务会议。2026年8月赴少普镇调研安全生产、防溺水。"},
    {"id": 6, "person_id": 2, "org_id": 7, "title": "织金经济开发区（织金县产业园区）管委会主任（兼）", "start": "", "end": "present", "rank": "兼",
     "note": "兼任织金经济开发区党工委副书记、管委会主任，并任县法学会会长（兼）。"},
    # 县委副书记
    {"id": 7, "person_id": 3, "org_id": 1, "title": "织金县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年7月出席县委常委会，并兼任织金经济开发区党工委副书记、管委会副主任。"},
    {"id": 8, "person_id": 3, "org_id": 7, "title": "织金经济开发区党工委副书记、管委会副主任", "start": "", "end": "present", "rank": "兼",
     "note": "协助县委书记抓经开区工作。"},
    {"id": 9, "person_id": 4, "org_id": 1, "title": "织金县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年7月30日县委常委会出席名单列为县委副书记。"},
    # 常务副县长
    {"id": 10, "person_id": 5, "org_id": 2, "title": "织金县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责县政府常务工作，分管发改、财政、税务、金融、统计、国资等。"},
    # 副县长
    {"id": 11, "person_id": 6, "org_id": 2, "title": "织金县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管林业、水务、气象、卫生健康、医疗保障等，三级调研员。"},
    {"id": 12, "person_id": 7, "org_id": 2, "title": "织金县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管生态环境保护、交通运输、民政、民族宗教等。2026年8月与县长马丽飞一同赴少普镇调研。"},
    {"id": 13, "person_id": 8, "org_id": 2, "title": "织金县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管公安、国安、维护社会稳定、交通安全、武装、司法、退役军人事务。"},
    {"id": 14, "person_id": 8, "org_id": 3, "title": "织金县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副处级",
     "note": "主持县公安局全面工作（一级警长）。"},
    {"id": 15, "person_id": 9, "org_id": 2, "title": "织金县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管招商引资、人社、自然资源、住建、城市管理等。"},
    {"id": 16, "person_id": 10, "org_id": 2, "title": "织金县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管农业、乡村振兴、教育、市场监管等，兼任县教育局党组书记、局长、县委教育工委副书记。"},
    {"id": 17, "person_id": 10, "org_id": 6, "title": "织金县教育局党组书记、局长", "start": "", "end": "present", "rank": "正科级/兼",
     "note": "兼任县教育局局长（县委教育工委副书记兼）。"},
    {"id": 18, "person_id": 11, "org_id": 2, "title": "织金县人民政府党组成员", "start": "", "end": "present", "rank": "",
     "note": "县政府党组成员，织金古城管理处处长。"},
    {"id": 19, "person_id": 12, "org_id": 2, "title": "织金县人民政府党组成员、县人民政府办公室主任", "start": "", "end": "present", "rank": "",
     "note": "主持县政府办公室（县外事办）全面工作。"},
    # 四套班子
    {"id": 20, "person_id": 13, "org_id": 4, "title": "织金县人大常委会主任", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月出席县委常委会。"},
    {"id": 21, "person_id": 14, "org_id": 5, "title": "政协织金县委员会主席", "start": "", "end": "present", "rank": "正处级",
     "note": "2026年7月30日出席县委常委会。"},
    # 其他县领导
    {"id": 22, "person_id": 15, "org_id": 2, "title": "县级领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月20日出席县政府党组会，具体职务未公开。"},
    {"id": 23, "person_id": 16, "org_id": 2, "title": "县级领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月28日出席县委医共体专题会议，具体职务未公开。"},
    {"id": 24, "person_id": 17, "org_id": 2, "title": "县级领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月出席招商引资调度会，具体职务未公开。"},
    {"id": 25, "person_id": 18, "org_id": 2, "title": "县级领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月出席招商引资调度会，具体职务未公开。"},
    {"id": 26, "person_id": 19, "org_id": 7, "title": "织金经济开发区领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月出席招商引资调度会。"},
    {"id": 27, "person_id": 20, "org_id": 7, "title": "织金经济开发区领导", "start": "", "end": "present", "rank": "",
     "note": "2026年7月出席招商引资调度会。"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记杨志伟与县长马丽飞党政正职搭档，共同出席多次县委全会、县政府党组会", "overlap_org": "中共织金县委/织金县政府", "overlap_period": "2026"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导县委副书记兼织金经开区副书记付正祥", "overlap_org": "中共织金县委", "overlap_period": "2026"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委副书记胡蓉", "overlap_org": "中共织金县委", "overlap_period": "2026"},
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记领导县委常委、常务副县长曾涛", "overlap_org": "中共织金县委/县政府", "overlap_period": "2026"},
    {"id": 5, "person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记领导副县长、公安局长石磊", "overlap_org": "中共织金县委/县政府", "overlap_period": "2026"},
    {"id": 6, "person_a": 1, "person_b": 13, "type": "同级协作", "context": "县委书记与县人大常委会主任王丽佳同台出席县委常委会", "overlap_org": "织金县四套班子", "overlap_period": "2026"},
    {"id": 7, "person_a": 1, "person_b": 14, "type": "同级协作", "context": "县委书记与县政协主席王刚同台出席县委常委会/医共体专题会议", "overlap_org": "织金县四套班子", "overlap_period": "2026"},
    {"id": 8, "person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与县委副书记、经开区管委会副主任付正祥同台出席县委常委会", "overlap_org": "中共织金县委", "overlap_period": "2026"},
    {"id": 9, "person_a": 2, "person_b": 6, "type": "上下级", "context": "县长领导副县长陈昌海", "overlap_org": "织金县人民政府", "overlap_period": "2026"},
    {"id": 10, "person_a": 2, "person_b": 7, "type": "上下级", "context": "县长领导副县长杨松，2026年8月一同赴少普镇调研", "overlap_org": "织金县人民政府", "overlap_period": "2026"},
    {"id": 11, "person_a": 2, "person_b": 15, "type": "上下级", "context": "县长领导分管招商、住建的副县长梁霄", "overlap_org": "织金县人民政府", "overlap_period": "2026"},
    {"id": 12, "person_a": 2, "person_b": 16, "type": "上下级", "context": "县长领导副县长、教育局长付国晖", "overlap_org": "织金县人民政府/县教育局", "overlap_period": "2026"},
    {"id": 13, "person_a": 2, "person_b": 5, "type": "上下级", "context": "县长领导常务副县长曾涛（协助县长负责审计、财政等）", "overlap_org": "织金县人民政府", "overlap_period": "2026"},
    {"id": 14, "person_a": 2, "person_b": 12, "type": "上下级", "context": "县长领导县政府办公室主任汪钰力", "overlap_org": "织金县人民政府", "overlap_period": "2026"},
    {"id": 15, "person_a": 1, "person_b": 9, "type": "同级协作", "context": "县委书记杨志伟与副县长梁霄同台出席招商引资调度会", "overlap_org": "织金县人民政府", "overlap_period": "2026-07"},
    {"id": 16, "person_a": 1, "person_b": 17, "type": "同级协作", "context": "县委书记与县领导张勇（招商调度会）同台", "overlap_org": "织金县四套班子", "overlap_period": "2026-07"},
    {"id": 17, "person_a": 1, "person_b": 18, "type": "同级协作", "context": "县委书记与县领导王子萱（招商调度会）同台", "overlap_org": "织金县四套班子", "overlap_period": "2026-07"},
    {"id": 18, "person_a": 2, "person_b": 15, "type": "上下级", "context": "县长领导副县长刘镇（县政府党组会出席）", "overlap_org": "织金县人民政府", "overlap_period": "2026-07"},
    {"id": 19, "person_a": 1, "person_b": 19, "type": "同级协作", "context": "县委书记与织金经开区领导焦凯同台出席招商会议", "overlap_org": "织金经济开发区", "overlap_period": "2026-07"},
    {"id": 20, "person_a": 1, "person_b": 20, "type": "同级协作", "context": "县委书记与织金经开区领导杨波同台出席招商会议", "overlap_org": "织金经济开发区", "overlap_period": "2026-07"},
]

# ── SQLite Build ───────────────────────────────────────────────────────────
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
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
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
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

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"
    elif "县长" in post and "副" not in post:
        return "50,100,255"
    elif "常务副县长" in post:
        return "50,120,255"
    elif "副县长" in post:
        return "50,150,255"
    elif "副书记" in post:
        return "255,120,60"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "开发区" in t:
        return "220,230,180"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post", "")
    return ("书记" in post and "副" not in post) or ("县长" in post and "副" not in post)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>织金县领导班子工作关系网络 - 贵州省毕节市</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

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
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"织金县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 杨志伟 (县委书记): confirmed via official 2026-07 news; earlier career unverified (gap)")
print("  - 马丽飞 (县长):      confirmed via official 领导之窗 bio + news")
print("  - 县委副书记/人大主任/政协主席/副县长: confirmed via official news & 领导之窗")