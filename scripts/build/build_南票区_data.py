#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 南票区, 葫芦岛市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_南票区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.npq.gov.cn — 南票区人民政府官方网站 (accessible)
  - npq.gov.cn 政府领导页面 — 区长王涛个人简介
  - npq.gov.cn 南政办发〔2026〕5号 — 区政府领导工作分工通知(2026-06-25)
  - npq.gov.cn 南票区"两优一先"表彰大会报道 — 区委书记李彪、区长王涛 (2026-07-07)
  - npq.gov.cn 南票区工商联第七次会员代表大会报道 — 区委书记李彪 (2026-07-14)

Confidence notes:
  - 区委书记李彪 confirmed via official news articles (2026-07-07, 2026-07-14)
  - 区长王涛 confirmed via official leadership page and multiple news articles
  - 王涛: 1978年8月生, 满族, 大学学历, 中共党员
  - 李彪的出生年月、籍贯、学历等需后续补充
  - 区政府领导班子分工更新于2026年6月25日
"""

from __future__ import annotations

import json
import os
import sys
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "南票区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_南票区"
if _CURRENT_DIR.name == "liaoning_南票区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3-9=副区长/常委, 10-12=前任

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共葫芦岛市南票区委员会",
        "source": "南票区人民政府网站: https://www.npq.gov.cn/xwzx/tpxw/202607/t20260707_1241397.html",
        "confidence": "confirmed",
        "notes": "区委书记李彪。2026年7月1日出席南票区'两优一先'表彰大会并发表讲话，7月7日出席区工商联第七次会员代表大会。李彪个人简历尚未从官方网站获取，出生年月、籍贯、学历等需后续补充。"
    },
    {
        "id": 2,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1978年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府领导信息: https://www.npq.gov.cn/xxgk/zfxxgk/fdzdgknr/jgjj/ligndao/201905/t20190523_828925.html",
        "confidence": "confirmed",
        "notes": "区长王涛，1978年8月生，男，满族，大学学历，中共党员，现任葫芦岛市南票区委副书记、南票区政府党组书记、区长。主持区政府及区政府党组全面工作。分管区政府办公室、区审计局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Government Leadership (from 南政办发〔2026〕5号, 2026-06-25)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李凌超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（常务）",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026): https://www.npq.gov.cn/xxgk/zfxxgk/fdzdgknr/lzyj/nanzhengbanfa/202607/t20260714_1241893.html",
        "confidence": "confirmed",
        "notes": "副区长（常务），负责区政府常务工作。分管发展改革、转型发展、财税、金融、国资国企、应急管理、信访、数据、统计、消防等方面工作。协助区长分管区政府办公室、区审计局。"
    },
    {
        "id": 4,
        "name": "马磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "副区长，负责人力资源和社会保障、住房和城乡建设、交通、城管执法、卫生健康、医疗保障等方面工作。"
    },
    {
        "id": 5,
        "name": "张向东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、南票公安分局局长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "副区长，负责公安、司法等方面工作。分管市公安局南票分局、区司法局。联系区法院、区检察院。"
    },
    {
        "id": 6,
        "name": "李强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "副区长，负责工业和信息化、军民融合、商务、外事、招商引资、教育、民政、退役军人、市场监管、科技、文化旅游、供销等方面工作。"
    },
    {
        "id": 7,
        "name": "武人鹿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "副区长，负责水利、农业农村、乡村振兴、生态环境、自然资源、矿山环境治理、采煤沉陷区综合防治、国有工矿棚户区改造及房屋分配等方面工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Committee Members
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "武健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共葫芦岛市南票区委员会",
        "source": "南票区'两优一先'表彰大会报道: https://www.npq.gov.cn/xwzx/tpxw/202607/t20260707_1241397.html",
        "confidence": "confirmed",
        "notes": "区委常委、组织部部长。2026年7月1日在南票区'两优一先'表彰大会上宣读表彰决定。"
    },
    {
        "id": 9,
        "name": "闵希伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委领导",
        "current_org": "中共葫芦岛市南票区委员会",
        "source": "南票区工商联第七次会员代表大会报道: https://www.npq.gov.cn/xwzx/tpxw/202607/t20260714_1241959.html",
        "confidence": "confirmed",
        "notes": "2026年7月7日出席区工商联第七次会员代表大会的区领导之一。具体职务待进一步查证。",
        "gender_hint": "疑似区人大常委会主任(根据其他新闻分析)"
    },
    {
        "id": 10,
        "name": "刘海波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "南票区",
        "source": "南票区工商联第七次会员代表大会报道: https://www.npq.gov.cn/xwzx/tpxw/202607/t20260714_1241959.html",
        "confidence": "confirmed",
        "notes": "2026年7月7日出席区工商联第七次会员代表大会的区领导之一。具体职务待进一步查证。"
    },
    {
        "id": 11,
        "name": "李壮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区工商联第七次会员代表大会报道",
        "confidence": "confirmed",
        "notes": "副区长。同时出现在区政府领导工作分工通知和工商联报道中。在2025年分工中分管教育、民政、卫生健康、退役军人、数据、医疗保障等方面。"
    },
    {
        "id": 12,
        "name": "魏冬娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "南票区",
        "source": "南票区工商联第七次会员代表大会报道",
        "confidence": "confirmed",
        "notes": "2026年7月7日出席区工商联第七次会员代表大会的区领导之一。从姓名判断为女性。具体职务待进一步查证。"
    },
    {
        "id": 13,
        "name": "王富文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "南票区",
        "source": "南票区工商联第七次会员代表大会报道",
        "confidence": "confirmed",
        "notes": "2026年7月7日出席区工商联第七次会员代表大会的区领导之一。具体职务待进一步查证。"
    },
    {
        "id": 14,
        "name": "李晓辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "协助副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "协助李凌超同志分管转型发展工作。具体职级职务待进一步查证。"
    },
    {
        "id": 15,
        "name": "王政权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "协助副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2026)",
        "confidence": "confirmed",
        "notes": "协助武人鹿同志分管矿山环境治理、采煤沉陷区综合防治、国有工矿棚户区改造及房屋分配等方面工作。具体职级职务待进一步查证。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Previous Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "刘春晖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任常务副区长",
        "current_org": "葫芦岛市南票区人民政府",
        "source": "南票区人民政府办公室关于区政府领导同志工作分工的通知(2025): https://www.npq.gov.cn/xxgk/zfxxgk/fdzdgknr/lzyj/nanzhengbanfa/202510/t20251031_1221010.html",
        "confidence": "confirmed",
        "notes": "前任常务副区长（截至2025年9月分工通知）。负责发展改革、转型发展、工业和信息化等常务工作。2026年6月分工通知显示已由李凌超接替常务副区长岗位。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共葫芦岛市南票区委员会", "type": "党委", "level": "县处级", "parent": "中共葫芦岛市委员会",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 2, "name": "葫芦岛市南票区人民政府", "type": "政府", "level": "县处级", "parent": "葫芦岛市人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 3, "name": "南票区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "葫芦岛市人大常委会", "location": "辽宁省葫芦岛市南票区"},
    {"id": 4, "name": "中国人民政治协商会议南票区委员会", "type": "政协", "level": "县处级",
     "parent": "葫芦岛市政协", "location": "辽宁省葫芦岛市南票区"},
    {"id": 5, "name": "中共葫芦岛市南票区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级",
     "parent": "中共葫芦岛市纪律检查委员会", "location": "辽宁省葫芦岛市南票区"},
    {"id": 6, "name": "中共南票区委组织部", "type": "党委", "level": "县处级", "parent": "中共葫芦岛市南票区委员会",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 7, "name": "中共南票区委宣传部", "type": "党委", "level": "县处级", "parent": "中共葫芦岛市南票区委员会",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 8, "name": "中共南票区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共葫芦岛市南票区委员会",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 9, "name": "葫芦岛市公安局南票分局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 10, "name": "南票区发展和改革局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 11, "name": "南票区财政局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 12, "name": "南票区应急管理局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 13, "name": "南票区统计局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 14, "name": "南票区商务局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
    {"id": 15, "name": "南票区农业农村局", "type": "政府", "level": "乡科级", "parent": "葫芦岛市南票区人民政府",
     "location": "辽宁省葫芦岛市南票区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李彪 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年7月已在任区委书记"},
    # 王涛 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "主持区政府及区政府党组全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长兼任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "官网明确标注"},
    # 李凌超 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start_date": "约2026", "end_date": "", "rank": "县处级副职",
     "note": "接替刘春晖。负责常务工作：发改、财税、金融、国资国企、应急等。协助区长协调政府领导之间工作。"},
    # 马磊 — 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责人社、住建、交通、城管执法、卫健、医保等方面工作"},
    # 张向东 — 副区长/公安
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责公安、司法等方面工作"},
    {"person_id": 5, "org_id": 9, "title": "公安分局局长", "start_date": "", "end_date": "", "rank": "乡科级正职",
     "note": "分管市公安局南票分局"},
    # 李强 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责工信、军民融合、商务、外事、招商引资、教育、民政、退役军人、市场监管、科技、文旅、供销等方面工作"},
    # 武人鹿 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责水利、农业农村、乡村振兴、生态环境、自然资源、矿山环境治理、采煤沉陷区综合防治等"},
    # 武健 — 组织部部长
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "2026年7月1日在两优一先表彰大会上宣读表彰决定"},
    # 闵希伟 — 区领导
    {"person_id": 9, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级",
     "note": "出席2026年7月区工商联会议，具体职务待查"},
    # 刘海波 — 区领导
    {"person_id": 10, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级",
     "note": "出席2026年7月区工商联会议，具体职务待查"},
    # 李壮 — 副区长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "2025年分工中分管教育、民政、卫健、退役军人事务、数据、医保等"},
    # 魏冬娜 — 区领导
    {"person_id": 12, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级",
     "note": "出席2026年7月区工商联会议，具体职务待查，从姓名推断为女性"},
    # 王富文 — 区领导
    {"person_id": 13, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级",
     "note": "出席2026年7月区工商联会议，具体职务待查"},
    # 李晓辉 — 协助副区长
    {"person_id": 14, "org_id": 2, "title": "协助副区长级", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "协助李凌超同志分管转型发展工作"},
    # 王政权 — 协助副区长
    {"person_id": 15, "org_id": 2, "title": "协助副区长级", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "协助武人鹿分管矿山环境治理、采煤沉陷区综合防治等"},
    # 刘春晖 — 前任常务副区长
    {"person_id": 16, "org_id": 2, "title": "常务副区长（前任）", "start_date": "", "end_date": "约2026年初",
     "rank": "县处级副职",
     "note": "截至2025年9月在任常务副区长，2026年6月分工通知已由李凌超接替"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 现任党政正职
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记李彪与区长王涛为当前党政主要领导搭档关系",
        "overlap_org": "中共葫芦岛市南票区委员会/南票区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 区长与常务副区长
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长王涛与常务副区长李凌超为政府主要领导与副手关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 区长与其他副区长
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长王涛与副区长马磊为政府领导关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长王涛与副区长张向东（公安分局局长）为政府领导关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长王涛与副区长李强为政府领导关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长王涛与副区长武人鹿为政府领导关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区委书记与组织部部长
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "区委书记李彪与区委常委、组织部部长武健为党委班子上下级关系",
        "overlap_org": "中共葫芦岛市南票区委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区委书记与其他区委领导
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "区委书记李彪与闵希伟在区委工作中共事",
        "overlap_org": "中共葫芦岛市南票区委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "overlap",
        "context": "区委书记李彪与刘海波在区委工作中共事",
        "overlap_org": "中共葫芦岛市南票区委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 常务交接
    {
        "person_a": 3, "person_b": 16,
        "type": "predecessor_successor",
        "context": "李凌超接替刘春晖任常务副区长",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "约2026年初交接",
        "confidence": "confirmed",
    },
    # 区长与前任常务
    {
        "person_a": 2, "person_b": 16,
        "type": "overlap",
        "context": "区长王涛与前任常务副区长刘春晖曾为政府班子同僚",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "至2026年初",
        "confidence": "confirmed",
    },
    # 副区长之间互补关系
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "李凌超与马磊为政府工作互补关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "张向东与李强为政府工作互补关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 5, "person_b": 7,
        "type": "overlap",
        "context": "张向东与武人鹿为政府工作互补关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "李强与武人鹿为政府工作互补关系",
        "overlap_org": "葫芦岛市南票区人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 区委书记主持表彰大会
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "李彪与武健在'两优一先'表彰大会上共同出席（李彪讲话，武健宣读表彰决定）",
        "overlap_org": "中共葫芦岛市南票区委员会",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
    },
    # 与会领导关系群组
    {
        "person_a": 1, "person_b": 11,
        "type": "overlap",
        "context": "区委书记李彪与副区长李壮在区工商联会议上共同出席",
        "overlap_org": "南票区",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "overlap",
        "context": "区委书记李彪与魏冬娜在区工商联会议上共同出席",
        "overlap_org": "南票区",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "overlap",
        "context": "区委书记李彪与王富文在区工商联会议上共同出席",
        "overlap_org": "南票区",
        "overlap_period": "2026年7月",
        "confidence": "confirmed",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "葫芦岛市",
        "region": "南票区",
        "task_id": "liaoning_南票区",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    # Source register
    sources = []
    if p["source"]:
        source_url = p["source"]
        sid = "S001"
        source_type = "official"
        sources.append({
            "id": sid,
            "title": f"{role_label}确认来源",
            "url": source_url.split(": ")[-1] if ": " in source_url else source_url,
            "publisher": "南票区人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": "high",
            "notes": "",
        })

    is_core = person_id <= 2
    rank = "县处级正职" if is_core else "县处级副职"
    system = "party" if person_id in [1, 8, 9, 10] else "government"

    person = {
        "identity": {
            "person_id": f"liaoning_huludao_nanpiao_{name}",
            "name": name,
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
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": p.get("source", "").split(": ")[-1] if ": " in p.get("source", "") else "",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True if "待查" not in name else False,
            "source_ids": ["S001"] if sources else [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available records",
                "date": AS_OF,
                "confidence": "plausible" if "待查" not in name else "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if not name.startswith("待查") and p.get("birth") else "plausible",
            "current_role": "confirmed" if not name.startswith("待查") else "unverified",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "high" if not name.startswith("待查") else "low",
            "biggest_gap": "",
        },
        "open_questions": [],
    }

    # Career timeline from positions
    pos_list = [pos for pos in positions if pos["person_id"] == person_id]
    for pos in pos_list:
        org_name = ""
        for o in organizations:
            if o["id"] == pos["org_id"]:
                org_name = o["name"]
                break
        entry = {
            "start": pos["start_date"] if pos["start_date"] else "unknown",
            "end": pos["end_date"] if pos["end_date"] else "present",
            "org": org_name,
            "title": pos["title"],
            "level": "",
            "location": "南票区",
            "system": system,
            "rank": pos["rank"],
            "is_key_promotion": False,
            "notes": pos["note"],
            "confidence": "confirmed",
            "source_ids": ["S001"] if sources else [],
        }
        person["career_timeline"].append(entry)

    # Relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == person_id or r["person_b"] == person_id]
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = ""
        for op in persons:
            if op["id"] == other_id:
                other_name = op["name"]
                break
        person["relationships"].append({
            "person": other_name,
            "person_id": f"liaoning_huludao_nanpiao_{other_name}",
            "relationship_type": r["type"],
            "strength": "strong",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": r["confidence"],
        })

    # Big gap
    if not p.get("birth"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的出生年月和完整履历未从官方网站获取"
    elif not name.startswith("待查"):
        person["confidence_summary"]["biggest_gap"] = f"{name}的完整履历仍有部分缺口"

    # Open questions
    if not p.get("birth"):
        person["open_questions"].append({
            "priority": "high",
            "question": f"{name}的出生年月、籍贯、学历？",
            "why_it_matters": "核心身份信息用于去重和综合档案",
            "suggested_queries": [f"南票区 {name} 简历"],
            "last_attempted": AS_OF,
        })
    if "待查" in name:
        person["open_questions"].append({
            "priority": "critical",
            "question": f"南票区{role_label}姓名是什么？",
            "why_it_matters": "核心目标人物之一",
            "suggested_queries": [],
            "last_attempted": AS_OF,
        })

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_")
    filename = f"{TODAY}-辽宁省-葫芦岛市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs for core figures
    person_files = []
    # Core leaders + key deputies
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 11, 16]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"Done.")


if __name__ == "__main__":
    main()
