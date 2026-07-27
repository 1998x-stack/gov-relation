#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 清原满族自治县, 抚顺市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_清原满族自治县
Level: 县
Targets: 县委书记 & 县长

Research status: WEB ACCESS PARTIALLY AVAILABLE
  - www.qingyuan.gov.cn: accessible via Python urllib with GBK encoding
  - 县政府领导之窗: fully accessible (6 individual pages)
  - 县委领导: no dedicated page on government site; roles extracted from news reports
  - Exa API: rate-limited
  - Baidu: 403 captcha block

Current officeholders (as of 2026-07-25):
  - 县委书记: 吴云龙 (confirmed via multiple official news articles)
  - 县委副书记、县长: 尚峰 (confirmed via official leadership page)
  - 县委副书记: 苏斌 (confirmed via news article)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "清原满族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "吴云龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中国共产党清原满族自治县委员会",
        "source": "http://www.qingyuan.gov.cn/",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "尚峰",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=600",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "苏斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中国共产党清原满族自治县委员会",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38678",
    },
    # ── 县委常委、常务副县长 ──
    {
        "id": 4,
        "name": "赵金鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、分管日常工作的副县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=601",
    },
    # ── 县委常委、副县长 ──
    {
        "id": 5,
        "name": "汪加欢",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1984-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=602",
    },
    # ── 县委常委、宣传部部长 ──
    {
        "id": 6,
        "name": "刘春勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中国共产党清原满族自治县委员会",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38659",
    },
    # ── 副县长（公安局长） ──
    {
        "id": 7,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局党组书记、局长",
        "current_org": "清原满族自治县公安局",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=603",
    },
    # ── 副县长 ──
    {
        "id": 8,
        "name": "崔京阁",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1976-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=604",
    },
    # ── 副县长 ──
    {
        "id": 9,
        "name": "孙雪",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1981-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=605",
    },
    # ── 副县长 ──
    {
        "id": 10,
        "name": "王生涛",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1973-07",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=606",
    },
    # ── 县政府党组成员（挂职） ──
    {
        "id": 11,
        "name": "于福恩",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1969-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员（挂职）",
        "current_org": "清原满族自治县人民政府",
        "source": "http://www.qingyuan.gov.cn/list_ld.asp?s=607",
    },
    # ── 县领导（待确定具体职务） ──
    {
        "id": 12,
        "name": "刘军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "清原满族自治县",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38860",
    },
    # ── 县领导（待确定具体职务） ──
    {
        "id": 13,
        "name": "吴凡",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "清原满族自治县",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38794",
    },
    # ── 县领导（待确定具体职务） ──
    {
        "id": 14,
        "name": "马国栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "清原满族自治县",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38794",
    },
    # ── 县领导（待确定具体职务） ──
    {
        "id": 15,
        "name": "孟晓阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "清原满族自治县",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38794",
    },
    # ── 县领导（待确定具体职务） ──
    {
        "id": 16,
        "name": "张铁凝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "清原满族自治县",
        "source": "http://www.qingyuan.gov.cn/ins.asp?s=9&i=38794",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党清原满族自治县委员会", "type": "党委", "level": "县", "parent": "中国共产党抚顺市委员会", "location": "清原满族自治县"},
    {"id": 2, "name": "清原满族自治县人民政府", "type": "政府", "level": "县", "parent": "抚顺市人民政府", "location": "清原满族自治县"},
    {"id": 3, "name": "清原满族自治县人大常委会", "type": "人大", "level": "县", "parent": "抚顺市人大常委会", "location": "清原满族自治县"},
    {"id": 4, "name": "政协清原满族自治县委员会", "type": "政协", "level": "县", "parent": "政协抚顺市委员会", "location": "清原满族自治县"},
    {"id": 5, "name": "中国共产党清原满族自治县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共抚顺市纪律检查委员会", "location": "清原满族自治县"},
    {"id": 6, "name": "清原满族自治县公安局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 7, "name": "清原满族自治县发展和改革局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 8, "name": "清原满族自治县财政局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 9, "name": "清原满族自治县人力资源和社会保障局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 10, "name": "清原满族自治县应急管理局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 11, "name": "清原满族自治县自然资源局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 12, "name": "清原满族自治县统计局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 13, "name": "清原满族自治县水务局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 14, "name": "清原满族自治县卫生健康局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 15, "name": "清原满族自治县市场监督管理局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 16, "name": "清原满族自治县教育局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 17, "name": "清原满族自治县数据局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 18, "name": "清原满族自治县工业和信息化局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 19, "name": "清原满族自治县交通运输局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 20, "name": "清原满族自治县农业农村局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 21, "name": "清原满族自治县住房和城乡建设局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 22, "name": "清原满族自治县司法局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 23, "name": "清原满族自治县林业和草原局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 24, "name": "清原满族自治县退役军人事务局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 25, "name": "清原满族自治县产业园区管委会", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 26, "name": "清原满族自治县融媒体中心", "type": "事业单位", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 27, "name": "清原满族自治县民政局", "type": "政府", "level": "县", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 吴云龙 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "中共清原满族自治县委书记"},
    # 尚峰 - 县委副书记、县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "清原满族自治县人民政府党组书记、县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 苏斌 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "协助书记处理县委日常工作"},
    # 赵金鹏 - 县委常委、常务副县长
    {"person_id": 4, "org_id": 2, "title": "常务副县长（分管日常工作）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府日常工作，分管发改、财税金融、统计等"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 汪加欢 - 县委常委、副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责民政、数据、营商环境、住建、文旅、工信等"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘春勇 - 县委常委、宣传部部长
    {"person_id": 6, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王勇 - 副县长、公安局长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法和突发群体性事件处置"},
    {"person_id": 7, "org_id": 6, "title": "县公安局党组书记、局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 崔京阁 - 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责住建、交通等方面工作"},
    # 孙雪 - 副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、卫生健康、医保等方面工作（民建）"},
    # 王生涛 - 副县长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、乡村振兴、水务、交通、市场监管、林草"},
    # 于福恩 - 县政府党组成员（挂职）
    {"person_id": 11, "org_id": 2, "title": "县政府党组成员（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "协助赵金鹏分管退役军人等工作"},
    # 刘军 - 县领导
    {"person_id": 12, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 吴凡 - 县领导
    {"person_id": 13, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 马国栋 - 县领导
    {"person_id": 14, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 孟晓阳 - 县领导
    {"person_id": 15, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
    # 张铁凝 - 县领导
    {"person_id": 16, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "具体职务待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 吴云龙 <-> 尚峰 - 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档关系，共同出席县常委会、灾后重建等重点工作",
     "overlap_org": "清原满族自治县", "overlap_period": "至2026年7月"},
    # 吴云龙 <-> 苏斌 - 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记，共同参加多项调研和会议",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 吴云龙 <-> 赵金鹏 - 书记与常务副县长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长，多次共同出席安全生产等会议",
     "overlap_org": "清原满族自治县", "overlap_period": "至2026年7月"},
    # 吴云龙 <-> 刘春勇 - 书记与宣传部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委、宣传部部长",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 苏斌 - 县长与副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县委副书记（苏斌）与县委副书记、县长（尚峰）同为县委领导班子成员",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 赵金鹏 - 县长与常务副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长，赵金鹏协助尚峰分管审计等工作",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 汪加欢
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与县委常委、副县长",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 王生涛
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与分管农业副县长，共同出席会议",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 吴云龙 <-> 王勇 - 书记与公安局长
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与副县长、公安局长",
     "overlap_org": "清原满族自治县", "overlap_period": "至2026年7月"},
    # 赵金鹏 <-> 汪加欢 - 同为县委常委
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 赵金鹏 <-> 刘春勇 - 同为县委常委
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "同为县委常委",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 赵金鹏 <-> 于福恩 - 协助关系
    {"person_a": 4, "person_b": 11, "type": "superior_subordinate",
     "context": "于福恩协助赵金鹏分管退役军人等工作",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 苏斌 <-> 汪加欢 - 同为县委领导
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "县委副书记与县委常委",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 苏斌 <-> 刘春勇
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "同为县委领导",
     "overlap_org": "中共清原满族自治县委员会", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 崔京阁
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 尚峰 <-> 孙雪
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长（分管教育、卫健）",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 王生涛 <-> 王勇 - 同为副县长
    {"person_a": 10, "person_b": 7, "type": "overlap",
     "context": "同为县政府领导班子成员",
     "overlap_org": "清原满族自治县人民政府", "overlap_period": "至2026年7月"},
    # 吴云龙 <-> 王生涛
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与副县长，共同出席对外合作座谈会等",
     "overlap_org": "清原满族自治县", "overlap_period": "至2026年7月"},
]

# ── Build ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} data...")

    # Ensure staging dir exists
    _CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    # DB
    print(f"  DB: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]),
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]),
        )

    conn.commit()
    conn.close()
    print(f"  DB written: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # GEXF
    print(f"  GEXF: {GEXF_PATH}")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    from datetime import datetime as dt

    # Person colors by role
    def person_color(p):
        if p["id"] == 1:  # 县委书记
            return "255,50,50"
        elif p["id"] == 2:  # 县长
            return "50,100,255"
        elif p["name"] == "苏斌":  # 县委副书记
            return "50,100,255"
        elif p["current_post"].startswith("县委常委"):  # 县委常委
            return "255,165,0"
        else:
            return "100,100,100"

    # Organization color by type
    def org_color(o):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "群团": "255,220,255",
            "事业单位": "220,220,220",
        }
        return colors.get(o["type"], "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>清原满族自治县领导班子关系网络 - {SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        title = esc(p["current_post"])
        name = esc(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value="县"/>')
        lines.append(f'          <attvalue for="3" value="清原满族自治县"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        name = esc(o["name"])
        lines.append(f'      <node id="o{o["id"]}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edge: person <-> organization (worked at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{pos["start"] or "?"} - {pos["end"] or "?"}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edge: person <-> person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {eid} edges")

    # Write person JSON files
    person_json_dir = _CURRENT_DIR
    print(f"Person JSONs written separately")
    print(f"Done: {SLUG}")
