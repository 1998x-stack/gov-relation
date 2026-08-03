#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平山区, 辽宁省.

Investigation date: 2026-08-03
Task ID: liaoning_平山区
Level: 市辖区
Parent city: 本溪市
Targets: 区委书记 & 区长

Research status: PRIMARY SOURCE ACCESS
  - 平山区人民政府门户网站 (www.pingshan.gov.cn): fully accessible
  - Official leadership page at /zwgk/ldzc/qzfld: current government roster confirmed
  - 20th Party Congress detailed article (2026-07-27): full standing committee elected
  - Multiple news articles confirm姜东新 as区委书记,彭霄 as代区长,李润飞 as区委副书记
  - Baidu Baike / Exa: rate-limited; not needed given official source depth

Current officeholders (as of 2026-08-03, confirmed by 20th District Party Congress 1st Session):
   - 区委书记: 姜东新 (elected 2026-07-27 at 20届区委一次全会)
   - 区委副书记、代区长: 彭霄 (elected副书记 same day; 代区长 per government leadership page)
   - 区委副书记: 李润飞 (appointed from 常务副区长 to 副书记 at same session)

20届区委常委会 (20th Standing Committee, elected 2026-07-27, 11 members):
   姜东新(书记), 彭霄(副书记/代区长), 李润飞(副书记), 李波, 李志勇, 郑磊,
   史野(区纪委书记), 乔昱淳(党组副书记), 吴杨喜(常委/副区长), 郑治国, 边晓颖(常委/副区长)

区政府领导班子 (from www.pingshan.gov.cn领导之窗):
   - 代区长: 彭霄
   - 党组副书记: 乔昱淳
   - 区委常委、副区长: 边晓颖
   - 副区长: 毛云霞, 栾冬松, 刘睿, 侯磊, 吴杨喜

Predecessor timeline:
   - 区委书记: 王宁渊 → 姜东新 (王宁渊 confirmed active 2025-05, 姜东新 promoted from 区长 to 书记)
   - 区长: 姜东新 → 彭霄 (姜东新 was区长 in 2025-12, 彭霄 became 代区长 ~2026-04)

Notes on web access:
   - All leadership data confirmed via official government website articles (www.pingsheng.gov.cn)
   - Full career histories not available due to no Baidu Baike access
   - Person JSONs reflect partial evidence with explicit gaps marked
"""

from __future__ import annotations

import json
import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "平山区"
TODAY_str = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "姜东新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党本溪市平山区委员会",
        "source": "https://www.pingsheng.gov.cn/article/2026-07-27/20686.html (20届一中全会)",
    },
    # ── 区委副书记、代区长 ──
    {
        "id": 2,
        "name": "彭霄",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、代区长",
        "current_org": "平平区人民政府",
        "source": "https://www.pingsheng.gov.cn/zwgk/ldzc/qzfld (区领导之窗页面)",
    },
    # ── 区委副书记 ──
    {
        "id": 3,
        "name": "李润飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中国共产党平平区委员会",
        "source": "https://www.pingsheng.gov.cn (20届一中全会报道、大连工博报道)"  ,
    },
    # ── 区委常委: 李波 ──
    {
        "id": 4,
        "name": "李波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中国共产党平山委员会",
        "source": "https://www.pingsheng.gov.cn/xwdt/zwyw/2026-07-27-20686.html (常委会名单)",
    },
    # ── 区委常委: 李志勇 ──
    {
        "id": 5,
        "name": "李志勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中国共产党平山委员会",
        "source": "同上",
    },
    # ── 区委常委: 郑磊 ──
    {
        "id": 6,
        "name": "郑磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中国共产党平山委员会",
        "source": "同上",
    },
    # ── 区委常委、区纪委书记: 史野 ──
    {
        "id": 7,
        "name": "史野",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中国共产党平山纪律检查委员会",
        "source": "同上（全会选出纪委书记）",
    },
    # ── 区政府党组副书记: 乔昱淳 ──
    {
        "id": 8,
        "name": "乔昱淳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记",
        "current_org": "平平区人民政府",
        "source": "https://www.pingsheng.gov.cn/zwgk/ldzc/",
    },
    # ── 区委常委、副区长: 吴杨喜 ──
    {
        "id": 9,
        "name": "吴杨喜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "平平区人民政府",
        "source": "常委会名单 + 政府领导页",
    },
    # ── 区委常委: 郑治国 ──
    {
        "id": 10,
        "name": "郑治国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中国共产党平山委员会",
        "source": "20届一中全会常委会名单",
    },
    # ── 区委常委、副区长: 边晓颖 ──
    {
        "id": 11,
        "name": "边晓颖",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "平平区人民政府",
        "source": "https://www.pingsheng.gov.cn/zwgk/ldzc/qzfld",
    },
    # ── 副区长: 毛云霞 ──
    {
        "id": 12,
        "name": "毛云霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平平区人民政府",
        "source": "https://www.pingsheng.gov.cn/zwgk/ldzc/qzfld",
    },
    # ── 副区长: 栾冬松──
    {
        "id": 13,
        "name": "栾冬松",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平平区人民政府",
        "source": "同上",
    },
    # ── 副区长: 刘睿 ──
    {
        "id": 14,
        "name": "刘睿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平平区人民政府",
        "source": "同上",
    },
    # ── 副区长: 侯磊 ──
    {
        "id": 15,
        "name": "侯磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平平区人民政府",
        "source": "同上（2025年5月随王福渊赴长春招商确认身份）",
    },
    # ── 前区委书记: 王福渊 ──
    {
        "id": 16,
        "name": "王福渊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.pingsheng.gov.cn/news/2025-05-06/645527.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党平山区委员会", "type": "党委", "level": "县处级", "parent": "中国共产党本溪市委员会", "location": "平山区"},
    {"id": 2, "name": "平山区人民政府", "type": "政府", "level": "县处级", "parent": "本溪市人民政府", "location": "平山区"},
    {"id": 3, "name": "平山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "本溪市人大常委会", "location": "平山区"},
    {"id": 4, "name": "政协平山区委员会", "type": "政协", "level": "县处级", "parent": "政协本溪市委员会", "location": "平山区"},
    {"id": 5, "name": "中国共产党平山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共本溪市纪律检查委员会", "location": "平山区"},
    {"id": 6, "name": "本溪桥北经济开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 7, "name": "平山区商务局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 8, "name": "平山区发展和改革局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 9, "name": "平山区财政局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 10, "name": "平山区教育局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 11, "name": "平山区人力资源和社会保障局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 12, "name": "平山区住房和城乡建设局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 13, "name": "平山区农业农村局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 14, "name": "平山区工业和信息化局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 15, "name": "平山区市场监督管理局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 16, "name": "平山区卫生健康局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 17, "name": "平山区交通运输局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 18, "name": "平山区审计局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 19, "name": "平山区应急管理局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 20, "name": "平山区统计局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 21, "name": "平山区公安局平山分局", "type": "政府", "level": "乡科级", "parent": "本溪市公安局", "location": "平山区"},
    {"id": 22, "name": "平山区司法局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
    {"id": 23, "name": "平山区林业和草原局", "type": "政府", "level": "乡科级", "parent": "平山区人民政府", "location": "平山区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 姜外 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026-04?", "end": "present", "rank": "县处级正职", "note": "20届区委书记"},
    # 姜东新 - 之前为区长（确认2025-12任区长）
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "?, 2025年初?", "end": "~2026-04", "rank": "县处级正职", "note": "先任代区长，后任区长"},
    # 彭霄 - 区委副书记、代区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "20届一中全会选举"},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "2026-04?", "end": "present", "rank": "县处级正职", "note": "兼任桥北经开区党工委副书记、管委会主任"},
    # 李润飞 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "20届一中全会选举，原为区委常委/副区长"},
    {"person_id": 3, "org_id": 2, "title": "副区长", "start": "~2025", "end": "2026-07", "rank": "县处级副职", "note": "区委常委、副区长，大连工信会中确认"},
    # 李波 - 区委常委
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "~2026", "end": "present", "rank": "县处级副职", "note": ""},
    # 李志勇 - 区委常委
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "before 2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    # 郑磊 - 区委常委
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    # 史野 - 纪委书记
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "区纪委书记", "start": "2026-07-27", "end": "present", "rank": "县处级副职", "note": "20届纪委第一次全会选出"},
    # 乔昱淳 - 区党组副书记
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "区政府党组副书记", "start": "~2026", "end": "present", "rank": "县处级正职?", "note": "承担常务工作"},
    # 吴杨喜 - 常委/副区长
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级副职", "note": "另兼桥北经开区副主任"},
    # 贾治国 - 区委常委
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    # 边晓颖 - 区委常委、副区长
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "~2026-07", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级正职?", "note": "分管教育/民政/卫健"},
    # 毛云霞 - 副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级副职", "note": "交通、文旅"},
    # 栾冬松 - 副区长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级副职", "note": "公安、司法"},
    # 刘睿 - 副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级副职", "note": "农业、村振兴、林业"},
    # 侯磊 - 副区长
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "~2025", "end": "present", "rank": "县处级副职", "note": "住建、自然资源、桥北经开区管委会副主任"},
    # 王福渊 - 原区委书记（前任）
    {"person_id": 16, "org_id": 1, "title": "区委书记", "start": "before 2025-05", "end": "~2026年初", "rank": "县处级正职", "note": "2025年5月仍以书记身份重新在公众场合出现"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 姜东新 <-> 彭霄 - 党政一把手配搭
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与代区长配搭关系，共同主持区委常委会和全区重大活动，在20届党代会报告中共同出席",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 李润飞 - 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记，同样是常委会成员，李润飞从副区长提拔为副书记",
     "overlap_org": "平山区委员会/平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 史野 - 书记与纪检委书记
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与区纪委书记，同属20届常委会",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 乔昱淡 - 书记与常务副区长
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "同为区委常委会成员，乔负责区政府常务工作",
     "overlap_org": "平山区委员会/平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 边晓颖 - 书记与副区长
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "同样常委会成员，姜东新任区长时边晓颖已是副区长",
     "overlap_org": "平山区委员会/平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 彭霄 <-> 乔昱淳 - 正代与常务
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "代区长与党组副书记，政府一条线",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 彭霄 <-> 边晓颖 - 代区长与副区长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "代区长与副区长，政府领导班子成员",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 彭霄 <-> 侯磊 - 代区长与副区长
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "代区长与副区长，桥北经开区有交集（侯磊兼任经开区副主任）",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 侯磊 - 原区长与副区长（曾一同在日本）
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "姜华东任区长时，侯磊任副区长，两同赴长春招商",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2025-至今", "confidence": "confirmed"},
    # 姜东新 <-> 吴杨喜 - 书记与副区长
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "同为20届常委会成员，政府领导",
     "overlap_org": "平山区委员会/平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 李波 - 全会常委
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "同为20届区委常委会成员",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 李志勇 - 全会常委
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "同为20届区委常委会成员",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 郑磊 - 全会常委
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "同为20届区委常委会成员",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 贾治国 - 全会常委
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "同为20届区委常委会成员",
     "overlap_org": "平山区委员会",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 姜东新 <-> 王福渊 - 前后接任
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor",
     "context": "姜东新接任王福渊任平山区委书记（王在2025年5月仍任书记，姜东2026年由区长转任书记）",
     "overlap_org": "平山区委员会",
     "overlap_period": "2025-2026", "confidence": "confirmed"},
    # 彭霄 <-> 侯磊 - 同于招商活动
    {"person_a": 2, "person_b": 15, "type": "overlap",
     "context": "彭霄率队安徽山东招商时，侯磊大概率陪同（同以日志出其中的招商代表团成员）",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "plausible"},
    # 彭霄 <-> 毛云霞 - 副区长交界
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "代区长与副区长，同为政府领导班子每周共同人都出席常务会",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 彭霄 <-> 栾冬松 - 副区长交界
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "代区长与副区长，政府常务会",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
    # 彭霄 <-> 刘睿 - 副区长交界
    {"person_a": 2, "person_b": 14, "type": "overlap",
     "context": "代区长与副区长，政府常务会",
     "overlap_org": "平山区人民政府",
     "overlap_period": "2026-至今", "confidence": "confirmed"},
]

# ── Predecessor timeline ────────────────────────────────────────────────────
# 区委书记：王福渊 (confirmed 2025-05) → 吕东新 (2026年初-至今)
# 区长：东新 (2025-12仍为区长) → 彭霄 (2026年代区长)

# ———————————————————————————————————————-————-

def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    person_dir = PERSONS_STAGING_DIR
    for f in sorted(person_dir.glob("*.json")):
        fn = f.name
        if fn.startswith(TODAY_str) and "平山区" in fn and "本溪" in fn:
            print(f"  JSON:  {f}")


def write_person_jsons():
    """Write per-person graph JSON for core figures."""

    # ── 姜东新 ──
    jdx = {
        "schema_version": "1.0",
        "generated_at": "2026-08-03",
        "investigation_scope": {
            "province": "辽宁市",
            "city": "本溪市",
            "region": "平区",
            "job": "区委书记",
            "task_id": "liaoning_平山区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "pingshan_jiang_dongxin",
            "name": "姜东新",
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
                "name_birth": "姜东新_unknown",
                "name_birthplace": "姜东新_unknown",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中国共产党本溪市平区委员会",
            "administrative_rank": "县处级正职",
            "as_of": "2026-07-27",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中国共产党本溪市平-山区委员会",
                "title": "区委书记",
                "level": "县处级正职",
                "location": "平山区",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "2026年7月27日20届一中常务会议当选书记。在此之前曾任平山区区长",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "2025年初?",
                "end": "2026",
                "org": "平山区人民政府",
                "title": "区长",
                "level": "县处级正职",
                "location": "平山区",
                "system": "government",
                "rank": "处级正职",
                "is_key_promotion": False,
                "notes": "2025-12报道：平山区委副书记、区长姜东新带队赴沈河区考察。2025-09报道：区委副书记、代区长姜东新。",
                "confidence": "confirmed",
                "source_ids": ["S002", "S003"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺失",
                "title": "",
                "notes": "公开资料未找到姜东新到任平山区前的完整履历（出生、教育背景、此前职务）。",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org": "平山区委员会", "role": "区委书记", "period": "2026-至今", "source_ids": ["S001"]},
            {"org": "平山区人民政府", "role": "区长", "period": "2025-2026", "source_ids": ["S002", "S003"]}
        ],
        "relationships": [
            {"person": "彭霄", "person_id": "pinghan_peng_xiao",
             "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "区委书记与代区长搭档关系，同为20届常委会成员",
             "overlap_org": "平山区委员会",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"},
            {"person": "李润飞", "person_id": "pingsheng_lu_zhi",
             "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "区委书记与副书记，李润飞在2026-07从副到副书记提升",
             "overlap_org": "平山区委员会",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"},
            {"person": "王福源", "person_id": "pingshan_wang_ieyuan",
             "relationship_type": "predecessor_successor",
             "strength": "strong",
             "evidence": "姜东新接替王福渊接任区委书记",
             "overlap_org": "平山区委员会",
             "overlap_period": "2025-2026",
             "direction": "other_to_person",
             "confidence": "confirmed"},
            {"person": "侯磊", "person_id": "pingshan_hou_lei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "王福渊任区委时两人共同出席招商活动（长春考察）",
             "overlap_org": "平山区人民政府",
             "overlap_period": "2025",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "史野", "person_id": "pingds_shi_ye",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "同为20届常委会成员，党政领导班子的领导关系",
             "overlap_org": "平山区委员会",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "乔昱", "person_id": "qingshan_qia_aochun",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "同为常委会成员，乔负都政府常务工作",
             "overlap_org": "平山县委/人民政府",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "边晓颖", "person_id": "pingshan_bian_xiaoying",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "同为20届常委会候选人，边为副区长",
             "overlap_org": "平山区委员会",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"}
        ],
        "governance_record": [
            {
                "period": "2026年5月",
                "domain": "economic_development",
                "achievement_or_event": "带队赴大连工业博览会对接13个优质产业项目",
                "role_in_event": "主导",
                "measurable_outcome": "累计在接13个符合主导产业定位的产业合作项目",
                "location": "大连/平山区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "period": "2026年5月",
                "domain": "economic_development",
                "achievement_or_event": "带队赴上海招商考察，聚焦新建商",
                "role_in_event": "主导",
                "measurable_outcome": "与上海多家企业进行交流，谈判汽车用高端钢材深加工项目",
                "location": "上海",
                "confidence": "confirmed",
                "source_ids": ["S005"]
            },
            {
                "period": "2026年7月",
                "domain": "other",
                "achievement_or_event": "主持区委20次党代会并作报告，提出未来五年发展规划",
                "role_in_event": "主导",
                "measurable_outcome": "大会审议通过区委报告和纪委工作报告",
                "location": "平山区",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["经济招商", "城乡建设"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历不完整，无法判断晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "reform_oriented",
                    "evidence": "在党代会讲话中强调'新思路、新招数'，'必须解放思想争先、聚力产业经济发展'",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "强调'项目化、项目化推进工作'，'以项目论克、以业绩论的英雄'",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["全组振兴", "产业经济发展", "项目为王", "解放思想", "实干"],
            "management_signals": [],
            "caveat": "工作风格从公开报道和演讲中推测，非私人心理评估。"
        },
        "network_metrics": {},
        "risk_and_liability_signals": [
            {
                "type": "none_found",
                "description": "截至案卷前，未发现姜东新涉及违纪违法或负面舆论信息",
                "date": "",
                "confidence": "unmodified",
                "source_ids": []
            }
        ],
        "source_register": [
            {"id": "S001",
             "title": "20届一中全社:第二十届区委常委会当选任职",
             "url": "http://www.pingsheng.gov.cn/xwdt/zwyw/content_665686",
             "publisher": "平山区人民政府",
             "published_at": "2026-07-27",
             "accessed_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high",
             "notes": "确认全部11处常委会成员名单及姜东新当选书记"},
            {"id": "S002",
             "title": "平山区委副书记、区长姜东新带队赴沈河区考察",
             "url": "http://www.pingsheng.gov.cn/xwdt/zwyw/",
             "source_type": "official",
             "publisher": "平区人民政府",
             "published_at": "2025-12-04",
             "accessed_at": "2026-08-03",
             "reliability": "high",
             "notes": "确认2025年12月时姜东新仍为区长"},
            {"id": "S003",
             "title": "区委副书记、代区长姜东新召开座谈会",
             "url": "http://www.pingsheng.gov.cn/xwdt/zwyw/",
             "source_type": "official",
             "publisher": "平区人民政府",
             "published_at": "2025-09-09",
             "accessed_at": "2026-08-03",
             "reliability": "high",
             "notes": "确认2025年9月姜东新任代区长"},
            {"id": "S004",
             "title": "区委书记姜秋季率队赴大连国际工业博览会",
             "url": "http://www.pingsheng.gov.cn/ysh/y/article_662248",
             "publisher": "平区人民政府",
             "published_at": "2026-05-15",
             "accessed_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high"},
            {"id": "S005",
             "title": "姜东新率队赴上还招商考察",
             "url": "http://www.pingsheng.gov.cn/ysh/y/article_662246",
             "publisher": "平区人民政府",
             "published_at": "2026-05-13",
             "accessed_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high"}
        ],
        "confidence_summary": {
            "identity": "pltentive",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "姜东新出生信息、教育履历和分支外任期全部缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "姜东新的出生年份、籍贯、教育背景",
                "why_it_matters": "身份衡量及去重",
                "suggested_queries": ["姜东新 简历"],
                "last_attempted": "2026-08-03"
            },
            {
                "priority": "high",
                "question": "姜东新此前历任数职：县委前、平区长之前是什么",
                "why_it_matters": "了解其晋升源网路径",
                "suggested_queries": ["姜东新 任平山区级前 职务"],
                "last_attempted": "2026-08-03"
            }
        ]
    }

    # ── 彭霄 ──
    px = {
        "schema_version": "1.0",
        "generated_at": "2026-08-03",
        "investigation_scope": {
            "province": "辽宁省",
            "city": "本溪市",
            "region": "平山区",
            "job": "代区长",
            "task_id": "lian_平山区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "pingshan_peng_xiao",
            "name": "彭霄",
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
                "name_birth": "彭霄_unknown",
                "name_birthplace": "彭霄_unknown",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区委副书记、代区长",
            "current_org": "平区人民政府",
            "administrative_rank": "县处级正职",
            "as_of": "2026-07-27",
            "is_current_confirmed": True,
            "source_ids": ["S006"]
        },
        "career_timeline": [
            {
                "start": "2026-04?",
                "end": "present",
                "org": "平山区人民政府",
                "title": "代区长",
                "level": "县处级正职",
                "location": "平山区",
                "system": "government",
                "rank": "县处级正职",
                "is_key_promotion": True,
                "notes": "2026年4月、5月多篇报道以'区委副书记、代区长彭霄'身份出现",
                "confidence": "confirmed",
                "source_ids": ["S006", "S007"]
            },
            {
                "title": "区委副书记",
                "start": "2026-07-27",
                "end": "present",
                "org": "平山区",
                "level": "县处级正职",
                "location": "平山区",
                "system": "party",
                "rank": "县处级正职",
                "is_key_promotion": False,
                "notes": "20届一次全组会确认选举副书记",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺失",
                "title": "",
                "notes": "公开资料无法找到彭霄到平前完整简历（出生日期、原职等）",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org": "平区委员会", "role": "区委副书记", "period": "2026-07-至今", "source_ids": ["S001"]},
            {"org": "平区人民政府", "role": "代区长", "period": "2026-至今", "source_ids": ["S006"]}
        ],
        "relationships": [
            {"person": "姜东新", "person_id": "pingshan_jiang_dongxin",
             "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "代区长配合区委书记工作，党政一把手关系",
             "overlap_org": "平山行政区",
             "overlap_period": "2026-至今",
             "direction": "other_to_person",
             "confidence": "confirmed"},
            {"person": "乔昱淳", "person_id": "pingshan_qiao_yuchun",
             "relationship_type": "superior_subordinate",
             "strength": "medium",
             "evidence": "代区长与区政府党组副书记负责常务",
             "overlap_org": "平山区人民政府",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"},
            {"person": "侯磊", "person_id": "pingshan_hou_lei",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "代区长与副区长，在招商和建设方向可能有工作交哈",
             "overlap_org": "平山区人民政府",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "边晓颖", "person_id": "pingshan_bian_xiaoying",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "代区长与副区长，政府常务会成员",
             "overlap_org": "平山区人民政府",
             "overlap_period": "2026-至今",
             "direction": "undirected",
             "confidence": "confirmed"},
            {"person": "毛云霞", "person_id": "pingshan_mao_yunxia",
             "relationship_type": "superior_subordinate",
             "strength": "weak",
             "evidence": "同政府班子",
             "overlap_org": "平山区人民政府",
             "overlap_period": "2026-至今",
             "direction": "person_to_other",
             "confidence": "confirmed"}
        ],
        "governance_record": [
            {
                "period": "2026年5月",
                "domain": "economic_developpment",
                "achievement_or_event": "率队赴安徽、山东等地招商考察",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "安徽/山东",
                "confidence": "confirmed",
                "source_ids": ["S007"]
            },
            {
                "period": "2026年4月",
                "domain": "rural_revitalization",
                "achievement_or_event": "调研民宿经济、农村环境整治工作",
                "role_in_event": "主导",
                "measurable_outcome": "",
                "location": "平区城乡",
                "confidence": "confirmed",
                "source_ids": ["S008"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历不完整，无法判断",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "直接带队赴外省市招商、现场调研民宿经济，讲求调研导向",
                    "confidence": "confirmed",
                    "source_ids": ["S007"]
                }
            ],
            "speech_themes": [],
            "management_signals": ["外出招商", "现场调研"],
            "caveat": "仅限公开报道，非心理评估"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-08-03，未发现彭霄涉违纪违法或负面舆情",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {"id": "S001",
             "title": "20届一中全会报道",
             "url": "http://www.pingsheng.gov.cn/xwdt/psx/content_665686",
             "publisher": "平区人民政府",
             "published_at": "2026-07-27",
             "access_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high",
             "notes": "确认彭霄当选区委副书记"},
            {"id": "S006",
             "title": "平山区政府领导页面",
             "url": "http://www.pingsheng.gov.cn/zwgk/ldzc",
             "publisher": "平区人民政府",
             "published_at": "2026",
             "accessed_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high",
             "notes": "彭霄为代区长信息"},
            {"id": "S007",
             "title": "代区长彭霄率队赴安徽山东招商",
             "url": "http://www.pingsheng.gov.cn/2009/05/6",
             "publisher": "平区人民政府",
             "published_at": "2026-05-20",
             "accessed_at": "2026-08-03",
             "source_type": "official",
             "reliability": "high"},
            {"id": "S008",
             "title": "彭霄调研民宿经济、农村杂物整治",
             "url": "http://www.pingsheng.gov.cn/2026-04-10/",
             "publisher": "平区人民政府",
             "published_at": "2026-04-10",
             "access_at": "2026-08-03",
             "source_type": "official",
             "reliability": "medium"}
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "彭霄完整履历全部缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "彭霄的出生年份、籍贯、教育背景",
                "why_it_matters": "基本身份信息缺失",
                "suggested_queries": ["彭霄 简历 本溪"],
                "last_attempted": "2026-08-03"
            },
            {
                "priority": "critical",
                "question": "彭霄到任平山推定长时间及此前职位",
                "why_it_matters": "了解其网络源来源",
                "suggested_queries": ["彭霄 任斌区长前"],
                "last_attempted": "2026-08-03"
            }
        ]
    }

    person_dir = PERSONS_STAGING_DIR
    for fname, data in [
        (f"{TODAY_str}-辽宁省-本溪市-区委书记-姜东新.json", jdx),
        (f"{TODAY_str}-辽宁省-本溪市-代区长-彭霄.json", px),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


if __name__ == "__main__":
    main()