#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 海原县 (Haiyuan County), 中卫市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_海原县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Current leadership roster, bios, and 工作分工 confirmed from the OFFICIAL
    primary source: 海原县人民政府门户网站 - 领导之窗
    (http://www.hy.gov.cn/xxgk/ldzc/), accessed 2026-08-07.
  - 2026年海原县人民政府工作报告 (2026-01-17) confirms 县长李明 delivered the
    report and provides governance/economic context.
  - Web access was partially degraded:
    - Exa search API rate-limited (stopped using it for this task).
    - Baidu Baike returned HTTP 403.
    - Bing / Jina Reader / Google timed out.
  - Former-secretary name is currently uncertain (marked pending verification);
    predecessor/successor and cross-county transfer detail is encoded as open
    questions rather than fabricated.

Confidence notes:
  - Identity (name/gender/ethnicity/birth/education) for every rostered leader is
    CONFIRMED from the official 领导之窗 page.
  - Career timelines beyond the current post are NOT available from the official
    page and are marked "unverified" / open questions.
  - Administrative ranks, parent orgs, and org types are standard and confirmed.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
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

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "海原县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_海原县"
if _CURRENT_DIR.name == "ningxia_海原县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
# All confirmed from 海原县人民政府领导之窗 (www.hy.gov.cn/xxgk/ldzc/), 2026-08-07.
persons = [
    # === 县委领导班子 (Party Committee) ===
    # id1 县委书记
    {"id": 1, "name": "胡斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-02", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中卫市委委员、常委、海原县委书记、海兴开发区党工委书记",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 http://www.hy.gov.cn/xxgk/ldzc/ (Confirmed)"},
    # id2 县委副书记、县长
    {"id": 2, "name": "李明", "gender": "男", "ethnicity": "回族",
     "birth": "1981-10", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委副书记、县政府党组书记、县长、海兴开发区管委会主任",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 + 2026年海原县政府工作报告 (Confirmed)"},
    # id3 县委副书记
    {"id": 3, "name": "杨春梅", "gender": "女", "ethnicity": "回族",
     "birth": "1981-08", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委副书记",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id4 县委副书记、统战部长
    {"id": 4, "name": "吴佳伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委副书记、国安办主任、统战部部长、县政协党组副书记",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id5 县委副书记、政府副县长
    {"id": 5, "name": "陈结定", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-02", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委副书记、政府副县长",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id6 县委常委、政法委书记
    {"id": 6, "name": "李芳", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-12", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、政法委书记",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id7 县委常委、人武部政委
    {"id": 7, "name": "黄振龙", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、人武部政治委员",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id8 县委常委、政府副县长
    {"id": 8, "name": "蒋文韬", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id9 县委常委、纪委书记
    {"id": 9, "name": "张楠", "gender": "男", "ethnicity": "汉族",
     "birth": "1989-06", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、纪委书记、监委代主任",
     "current_org": "中共海原县纪律检查委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id10 县委常委、九彩乡党委书记
    {"id": 10, "name": "洪兴志", "gender": "男", "ethnicity": "回族",
     "birth": "1976-02", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、九彩乡党委书记",
     "current_org": "中共海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id11 县委常委、政府副县长
    {"id": 11, "name": "李红强", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县委常委、政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},

    # === 政府领导班子 (Government deputies) ===
    # id12 副县长、公安局长
    {"id": 12, "name": "王学新", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长、公安局局长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id13 副县长
    {"id": 13, "name": "杨虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-02", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id14 副县长
    {"id": 14, "name": "赵春凤", "gender": "女", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id15 副县长（挂职）
    {"id": 15, "name": "董少波", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-06", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长（挂职）",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id16 副县长
    {"id": 16, "name": "尹向奎", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-12", "birthplace": "", "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id17 副县长
    {"id": 17, "name": "梁舜杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-10", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人民政府副县长",
     "current_org": "海原县人民政府",
     "source": "海原县人民政府领导之窗 (Confirmed)"},

    # === 人大 (People's Congress) ===
    # id18 人大主任
    {"id": 18, "name": "马斌", "gender": "女", "ethnicity": "回族",
     "birth": "1970-11", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人大常委会主任、一级调研员",
     "current_org": "海原县人民代表大会常务委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
    # id19 人大党组书记
    {"id": 19, "name": "黄飞虎", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县人大常委会党组书记",
     "current_org": "海原县人民代表大会常务委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},

    # === 政协（CPPCC）===
    # id20 政协党组书记、主席候选人
    {"id": 20, "name": "卢俊福", "gender": "男", "ethnicity": "回族",
     "birth": "1973-08", "birthplace": "", "education": "宁夏党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海原县政协党组书记、主席候选人",
     "current_org": "中国人民政治协商会议海原县委员会",
     "source": "海原县人民政府领导之窗 (Confirmed)"},
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共海原县委员会", "type": "党委",
     "level": "县处级", "parent": "中共中卫市委员会",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 2, "name": "海原县人民政府", "type": "政府",
     "level": "县处级", "parent": "中卫市人民政府",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 3, "name": "中共海原县纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共海原县委员会",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 4, "name": "海原县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "中卫市人民代表大会常务委员会",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 5, "name": "政协海原县委员会", "type": "政协",
     "level": "县处级", "parent": "政协中卫市委员会",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 6, "name": "海原县公安局", "type": "政府",
     "level": "正科级", "parent": "海原县人民政府",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 7, "name": "海原县海兴开发区", "type": "开发区",
     "level": "县级管理区", "parent": "中卫市人民政府",
     "location": "宁夏回族自治区中卫市海原县"},
    {"id": 8, "name": "中共中卫市委员会", "type": "党委",
     "level": "地厅级", "parent": "中共宁夏回族自治区委员会",
     "location": "宁夏回族自治区中卫市"},
    {"id": 9, "name": "中卫市人民政府", "type": "政府",
     "level": "地厅级", "parent": "宁夏回族自治区人民政府",
     "location": "宁夏回族自治区中卫市"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # Core leadership (县委书记/县长)
    {"person_id": 1, "org_id": 1, "title": "海原县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},
    {"person_id": 1, "org_id": 7, "title": "海兴开发区党工委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "海兴开发区管委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # Standing Committee (委员)
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县委财经委日常工作，分管县总工会、共青团、妇联、科协"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助书记处理县委日常工作"},
    {"person_id": 5, "org_id": 1, "title": "县委副书记、政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "主持县委政法委、县委办公室工作"},
    {"person_id": 7, "org_id": 1, "title": "县委常委、人武部政治委员",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党管武装工作"},
    {"person_id": 8, "org_id": 1, "title": "县委常委、政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、纪委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "县纪委书记、县监委代主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委、九彩乡党委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委、政府副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Government deputies
    {"person_id": 12, "org_id": 2, "title": "副县长、公安局局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长（挂职）",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # People's Congress and Political Consultative Conference
    {"person_id": 18, "org_id": 4, "title": "海原县人大常委会主任、一级调研员",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "海原县人大常委会党组书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 20, "org_id": 5, "title": "海原县政协党组书记、主席候选人",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Top leadership core (书记-县长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长，党政主要领导工作搭档",
     "overlap_org": "中共海原县委员会/海原县人民政府", "overlap_period": "current"},
    # 书记 — 副书记
    {"person_a": 3, "person_b": 1, "type": "overlap",
     "context": "县委副书记协助县委书记、负责财经委工作",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 1, "type": "overlap",
     "context": "县委副书记（统战部长）协助县委书记处理日常工作",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "县委副书记、副县长与书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    # 书记 — 其他常委
    {"person_a": 6, "person_b": 1, "type": "overlap",
     "context": "政法委书记与县委书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 1, "type": "overlap",
     "context": "纪委书记与县委书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 11, "person_b": 1, "type": "overlap",
     "context": "县委常委、副县长与县委书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    # 县长 — 政府班子
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate",
     "context": "县委副书记、副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate",
     "context": "县委常委、副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "县委常委、副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 12, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长、公安局长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 13, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 14, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 16, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    {"person_a": 17, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    # 常委班子 peer relationships
    {"person_a": 6, "person_b": 4, "type": "overlap",
     "context": "政法委书记与副书记（统战）班子关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 6, "type": "overlap",
     "context": "纪委书记与政法委书记班子关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 8, "person_b": 11, "type": "overlap",
     "context": "副县长（常委）班子同僚",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    # 人大、政协 — 书记/县长
    {"person_a": 18, "person_b": 1, "type": "overlap",
     "context": "人大主任与县委书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 20, "person_b": 1, "type": "overlap",
     "context": "政协党组书记、主席候选人与县委书记工作关系",
     "overlap_org": "中共海原县委员会", "overlap_period": "current"},
    {"person_a": 20, "person_b": 2, "type": "overlap",
     "context": "政协党组书记与县长工作关系",
     "overlap_org": "海原县人民政府", "overlap_period": "current"},
    # 上级（中卫市）
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "海原县委书记为中卫市委委员、常委，属中卫市委直管",
     "overlap_org": "中共中卫市委员会", "overlap_period": "current"},
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "县长接受中卫市人民政府领导",
     "overlap_org": "中卫市人民政府", "overlap_period": "current"},
]

# ── Person JSON data ────────────────────────────────────────────────────
PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "宁夏回族自治区",
        "city": "中卫市",
        "region": "海原县",
        "job": "",
        "task_id": "ningxia_海原县",
        "time_focus": "current"
    },
    "identity": {
        "person_id": "",
        "name": "",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "",
            "name_birthplace": "",
            "official_profile_url": "http://www.hy.gov.cn/xxgk/ldzc/"
        }
    },
    "current_status": {
        "current_post": "",
        "current_org": "",
        "administrative_rank": "",
        "as_of": AS_OF,
        "is_current_confirmed": True,
        "source_ids": ["S001"]
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
        "geographic_pattern": ["宁夏回族自治区", "中卫市", "海原县"],
        "promotion_velocity": {
            "summary": "",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "工作风格基于公开记录、讲话与报道治理行为推断，非私密心理评估。"
    },
    "network_metrics": {
        "direct_reports": [],
        "peer_relations": [],
        "organizational_affiliations": [],
        "centrality_estimate": "unknown"
    },
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "截至2026-08-07，官方领导之窗与公开检索未发现该人物的纪律审查、审计问题或负面报道信息。",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "海原县人民政府 - 领导之窗",
            "url": "http://www.hy.gov.cn/xxgk/ldzc/",
            "publisher": "海原县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认现任领导名单、简历、分工"
        }
    ],
    "confidence_summary": {
        "identity": "confirmed",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "领导之窗证实现任姓名/简历，但此前任职履历与前任/继任去向未获一手来源，待补充。"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "该人物的此前任职履历（晋升路径）",
            "why_it_matters": "构建完整职业轨迹与跨县交流网络",
            "suggested_queries": ["胡斌 简历 宁夏 中卫", "李明 海原 县长 简历"],
            "last_attempted": AS_OF
        }
    ]
}


def make_education(bio_education: str) -> list:
    """结构化教育字段 from 领导之窗学历描述."""
    if not bio_education:
        return []
    return [{
        "period": "",
        "institution": "",
        "major": "",
        "degree": bio_education,
        "study_type": "unknown",
        "source_ids": []
    }]


def write_person_json(person: dict, post: str, org: str, rank: str,
                      filename_suffix: str, relationships: list,
                      org_affil: list) -> None:
    """Write a person JSON file to the staging directory."""
    data = json.loads(json.dumps(PERSON_JSON_TEMPLATE))
    data["investigation_scope"]["job"] = post
    data["identity"]["person_id"] = f"haiyuan_{person['name']}"
    data["identity"]["name"] = person["name"]
    data["identity"]["gender"] = person.get("gender", "")
    data["identity"]["ethnicity"] = person.get("ethnicity", "")
    data["identity"]["birth"] = person.get("birth", "")
    data["identity"]["education"] = make_education(person.get("education", ""))
    data["identity"]["dedupe_keys"]["name_birth"] = f"{person['name']}_{person.get('birth','')}"
    data["current_status"]["current_post"] = person.get("current_post", post)
    data["current_status"]["current_org"] = org
    data["current_status"]["administrative_rank"] = rank
    data["organizations"] = org_affil
    data["relationships"] = relationships or []
    # A current-post row in the timeline
    add_career_core(data, person.get("current_post", post), org, rank, person.get("education", ""))
    filename = f"{TODAY}-宁夏回族自治区-中卫市-{filename_suffix}.json"
    path = PJSON_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path}")


def add_career_core(data: dict, title: str, org: str, rank: str, education: str) -> None:
    data["career_timeline"].append({
        "start": "unknown", "end": "present",
        "org": org, "title": title, "level": "", "location": "",
        "system": "party",
        "rank": "", "is_key_promotion": True,
        "notes": f"现任{title}（{education or '学历'}）",
        "confidence": "confirmed", "source_ids": ["S001"]
    })


# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} leadership network...")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)} | Orgs: {len(organizations)} | Positions: {len(positions)} | Relationships: {len(relationships)}")
    sys.stdout.flush()

    # Build database and GEXF
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

    # Write person JSONs for core leaders (书记/县长) and key deputies
    print("  Writing person JSONs...")
    # 县委书记
    write_person_json(
        persons[0], "县委书记", "中共海原县委员会", "县处级正职",
        "县委书记-胡斌",
        relationships=[
            {"person": "李明", "relationship_type": "superior_subordinate",
             "strength": "strong",
             "evidence": "县委书记与县长党政主要领导搭档",
             "overlap_org": "中共海原县委员会/海原县人民政府",
             "overlap_period": "current", "direction": "undirected",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "杨春梅", "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "县委副书记协助县委书记工作",
             "overlap_org": "中共海原县委员会", "overlap_period": "current",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "吴佳伟", "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "县委副书记（统战部长）协助县委书记处理日常工作",
             "overlap_org": "中共海原县委员会", "overlap_period": "current",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        org_affil=[{"org_id": "haiyuan_org_party", "org_name": "中共海原县委员会",
                    "role": "县委书记", "period": "present", "org_type": "党委", "level": "县处级"}],
    )
    # 县长
    write_person_json(
        persons[1], "县长", "海原县人民政府", "县长",
        "县长-李明",
        relationships=[
            {"person": "胡斌", "person_id": "haiyuan_胡斌",
             "relationship_type": "superior_subordinate", "strength": "strong",
             "evidence": "县长与县委书记党政主要领导搭档",
             "overlap_org": "中共海原县委员会/海原县人民政府",
             "overlap_period": "current", "direction": "undirected",
             "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "蒋文韬", "person_id": "haiyuan_蒋文韬",
             "relationship_type": "superior_subordinate", "strength": "medium",
             "evidence": "县委常委、副县长协助县长工作",
             "overlap_org": "海原县人民政府", "overlap_period": "current",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "李红强", "person_id": "haiyuan_李红强",
             "relationship_type": "superior_subordinate", "strength": "medium",
             "evidence": "县委常委、副县长协助县长工作",
             "overlap_org": "海原县人民政府", "overlap_period": "current",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        org_affil=[{"org_id": "haiyuan_org_party", "org_name": "中共海原县委员会",
                    "role": "县委副书记", "period": "present", "org_type": "党委", "level": "县处级"},
                   {"org_id": "haiyuan_org_gov", "org_name": "海原县人民政府",
                    "role": "县长", "period": "present", "org_type": "政府", "level": "县处级"}],
    )

    print(f"\nDone. Staged artifacts in: {STAGING}")
    print(f"  1. Build script: {__file__}")
    print(f"  2. Database: {DB_PATH}")
    print(f"  3. GEXF: {GEXF_PATH}")
    print(f"  4. Person JSONs: {PJSON_DIR}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()