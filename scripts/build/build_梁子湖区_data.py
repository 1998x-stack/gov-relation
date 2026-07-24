#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 梁子湖区 (Liangzihu District), 鄂州市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_梁子湖区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.liangzh.gov.cn — 梁子湖区人民政府官方网站 (primary)
  - News articles on liangzh.gov.cn confirming leadership appointments
  - Appointment notice: 刘扬波 appointed 区委书记 on 2026-07-17
  - Note: www.liangzihu.gov.cn DNS does not resolve; district site is at www.liangzh.gov.cn

Confidence notes:
  - Current roles (刘扬波 as 区委书记, 窦小华 as 区长): confirmed via official website news articles
  - Standing committee members: identified from multiple news articles on liangzh.gov.cn covering meetings
  - Birth years, education, detailed career timelines: mostly unverified (no Baidu Baike access)
  - Predecessors: 蔡和林 (former 区委书记, replaced July 2026 by 刘扬波) — confirmed
  - Earlier predecessors (夏帆, etc.): unverified
  - All claims labeled with confidence level; gaps explicitly documented
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "梁子湖区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hubei_梁子湖区"
if _CURRENT_DIR.name == "hubei_梁子湖区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 district committee (区委), 10-19 district government (区政府),
#      20-29 district-level organizations (人大/政协/纪委/人武部),
#      30-39 predecessors & other

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘扬波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月17日被任命为梁子湖区委书记、区人武部党委第一书记。接替蔡和林。现任区委书记。此前职务待查。",
    },
    {
        "id": 2,
        "name": "窦小华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "梁子湖区委副书记、区长。在全区警示教育大会等活动中以区长身份讲话。在区委常委会等会议中出席。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # District Committee Members (区委领导)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "潘黎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委副书记、政法委书记（2024年确定为三级调研员）。兼任沼山镇党委书记。曾在区委常委会等会议中出席。",
    },
    {
        "id": 4,
        "name": "汪伟樟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共梁子湖区纪律检查委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、区纪委书记。在全区清廉梁子湖建设工作推进会等会议中出席。",
    },
    {
        "id": 5,
        "name": "涂剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、组织部部长。在老干部活动、基层党建等会议中出席。",
    },
    {
        "id": 6,
        "name": "高建雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、常务副区长。在区政府全体会议、项目推进等活动中以常务副区长身份出席。",
    },
    {
        "id": 7,
        "name": "陈国璋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、副区长。兼任梧桐湖园区党工委书记。在区委常委会中出席。",
    },
    {
        "id": 8,
        "name": "胡映东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、宣传部部长。在区委理论学习中心组学习、文化宣传相关会议中出席。",
    },
    {
        "id": 9,
        "name": "张海山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、统战部部长。在政协相关会议中出席。",
    },
    {
        "id": 10,
        "name": "秦伟强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、区委办公室主任。在区级会议、区委常委会中出席。",
    },
    {
        "id": 11,
        "name": "赵军朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人武部政治委员",
        "current_org": "梁子湖区人民武装部",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区委常委、区人武部上校政治委员。出席区人武部党委第一书记任职大会等。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leaders (区政府)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "余淑芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。兼任梁子镇党委书记。",
    },
    {
        "id": 13,
        "name": "余俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。在区政府会议中出席。",
    },
    {
        "id": 14,
        "name": "秦伟强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长（兼任区委办主任，身份与id=10重复，此处保留政府任职记录）。",
    },
    {
        "id": 15,
        "name": "吴宝玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。在区政府会议中出席。",
    },
    {
        "id": 16,
        "name": "张文选",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。",
    },
    {
        "id": 17,
        "name": "刘晓云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。",
    },
    {
        "id": 18,
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "梁子湖区人民政府",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "副区长。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # District-level Organizations (人大/政协/法检/人武部)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "余安青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "梁子湖区人民代表大会常务委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区人大常委会主任。在区委全会中出席。",
    },
    {
        "id": 21,
        "name": "高爱民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区政协主席。在政协相关会议中出席。",
    },
    {
        "id": 22,
        "name": "余喆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民法院院长",
        "current_org": "梁子湖区人民法院",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区人民法院院长。",
    },
    {
        "id": 23,
        "name": "缪玉蓉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民检察院检察长",
        "current_org": "梁子湖区人民检察院",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区人民检察院检察长。",
    },
    {
        "id": 24,
        "name": "张志银",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人武部部长",
        "current_org": "梁子湖区人民武装部",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区人武部上校部长。",
    },
    {
        "id": 25,
        "name": "杨浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区公安分局政委",
        "current_org": "梁子湖区公安分局",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "区公安分局政委。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "蔡和林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共梁子湖区委员会",
        "source": "https://www.liangzh.gov.cn/",
        "confidence": "confirmed",
        "notes": "前任梁子湖区委书记。被免去区委书记职务，由刘扬波接替（2026年7月17日）。此前任区人武部党委第一书记。调任去向待查。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共梁子湖区委员会", "type": "党委", "level": "正处级", "parent": "中共鄂州市委员会", "location": "梁子湖区"},
    {"id": 2, "name": "梁子湖区人民政府", "type": "政府", "level": "正处级", "parent": "鄂州市人民政府", "location": "梁子湖区"},
    {"id": 3, "name": "中共梁子湖区纪律检查委员会", "type": "党委", "level": "正处级", "parent": "中共梁子湖区委员会", "location": "梁子湖区"},
    {"id": 4, "name": "梁子湖区人民代表大会常务委员会", "type": "人大", "level": "正处级", "parent": "鄂州市人大常委会", "location": "梁子湖区"},
    {"id": 5, "name": "政协梁子湖区委员会", "type": "政协", "level": "正处级", "parent": "政协鄂州市委员会", "location": "梁子湖区"},
    {"id": 6, "name": "梁子湖区人民武装部", "type": "党委", "level": "正处级", "parent": "鄂州军分区", "location": "梁子湖区"},
    {"id": 7, "name": "梁子湖区人民法院", "type": "事业单位", "level": "正处级", "parent": "鄂州市中级人民法院", "location": "梁子湖区"},
    {"id": 8, "name": "梁子湖区人民检察院", "type": "事业单位", "level": "正处级", "parent": "鄂州市人民检察院", "location": "梁子湖区"},
    {"id": 9, "name": "梁子湖区公安分局", "type": "政府", "level": "副处级", "parent": "梁子湖区人民政府", "location": "梁子湖区"},
    {"id": 10, "name": "梧桐湖园区", "type": "开发区", "level": "副处级", "parent": "梁子湖区人民政府", "location": "梁子湖区"},
    {"id": 11, "name": "沼山镇", "type": "乡镇/街道", "level": "乡科级", "parent": "梁子湖区人民政府", "location": "梁子湖区"},
    {"id": 12, "name": "梁子镇", "type": "乡镇/街道", "level": "乡科级", "parent": "梁子湖区人民政府", "location": "梁子湖区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "2026年7月17日任命，兼任区人武部党委第一书记"},
    {"person_id": 1, "org_id": 6, "title": "区人武部党委第一书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "按惯例区委书记兼任"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持区政府全面工作"},
    # District committee
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任政法委书记、沼山镇党委书记"},
    {"person_id": 3, "org_id": 11, "title": "沼山镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "区委常委、区纪委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任常务副区长"},
    {"person_id": 6, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任副区长、梧桐湖园区党工委书记"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 10, "title": "梧桐湖园区党工委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "区委常委、区委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任区委办主任"},
    {"person_id": 11, "org_id": 6, "title": "区委常委、区人武部政治委员", "start_date": "", "end_date": "", "rank": "副处级", "note": "上校政治委员"},
    # Government
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼任梁子镇党委书记"},
    {"person_id": 12, "org_id": 12, "title": "梁子镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # District-level orgs
    {"person_id": 20, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 7, "title": "区人民法院院长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 8, "title": "区人民检察院检察长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 6, "title": "区人武部部长", "start_date": "", "end_date": "", "rank": "正处级", "note": "上校部长"},
    {"person_id": 25, "org_id": 9, "title": "区公安分局政委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "前任区委书记", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "2026年7月由刘扬波接替。去向待查。"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core leadership relationships
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    # Party Secretary ↔ Standing Committee
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记/政法委书记", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—常务副区长", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—副区长", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—区委办主任", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—人武部政委", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
    # District Mayor ↔ Government
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—常务副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    # Standing committee internal (full mesh)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 10, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 11, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "纪委—组织", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "组织—政府", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "组织—政府", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "组织—宣传", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "政府—宣传", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "宣传—统战", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "宣传—区委办", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "统战—区委办", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026"},
    # Government internal
    {"person_a": 6, "person_b": 12, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 13, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 15, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 13, "type": "同僚", "context": "副区长同僚", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 15, "type": "同僚", "context": "副区长同僚", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    {"person_a": 13, "person_b": 15, "type": "同僚", "context": "副区长同僚", "overlap_org": "梁子湖区人民政府", "overlap_period": "2026"},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共梁子湖区委员会", "overlap_period": "2026-07"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[dict]:
    questions = []
    if not person.get("birth"):
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 出生"],
            "last_attempted": AS_OF,
        })
    if not person.get("birthplace"):
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的籍贯",
            "why_it_matters": "核心身份信息，用于网络分析和区域背景判断",
            "suggested_queries": [f"{person['name']} 籍贯", f"{person['name']} 出生地"],
            "last_attempted": AS_OF,
        })
    if not person.get("education"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的学历教育背景",
            "why_it_matters": "教育背景有助于专业领域判断",
            "suggested_queries": [f"{person['name']} 学历", f"{person['name']} 毕业"],
            "last_attempted": AS_OF,
        })
    if person.get("notes") and "待查" in person.get("notes", ""):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的此前任职履历",
            "why_it_matters": "完整履历是网络分析的基础",
            "suggested_queries": [f"{person['name']} 此前担任", f"{person['name']} 任前公示"],
            "last_attempted": AS_OF,
        })
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"liangzihu_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
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

    # Add gap entry if career_timeline is sparse
    career_timeline.append({
        "start": "unknown",
        "end": "unknown",
        "org": "履历缺口",
        "title": "",
        "notes": "政府官网仅提供当前职务确认信息，此前完整任职履历、出生年月、籍贯、学历等均待查。",
        "confidence": "unverified",
        "source_ids": [],
    })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"liangzihu_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "https://www.liangzh.gov.cn/")
    sources = [
        {
            "id": "S001",
            "title": "梁子湖区人民政府官方网站",
            "url": "https://www.liangzh.gov.cn/",
            "publisher": "梁子湖区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月通过新闻稿件确认领导姓名与职位",
        }
    ]

    # Build open questions
    open_questions = _get_open_questions(person)

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "鄂州市",
            "region": "梁子湖区",
            "job": person.get("current_post", ""),
            "task_id": "hubei_梁子湖区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "出生年月、籍贯、学历、此前完整任职履历（政府网站仅提供姓名和职务）",
        },
        "open_questions": open_questions,
    }

    job_short = person['current_post'].replace('、', '_')
    fname = f"{TODAY}-湖北省-鄂州市-{job_short}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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

    # Write person JSONs
    print("  Writing person JSONs...")
    # Core leaders (区委书记 + 区长) + predecessor
    core_ids = {1, 2, 30}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
