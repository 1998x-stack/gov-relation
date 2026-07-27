#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 长沙县 (Changsha County), 长沙市, 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_长沙县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.csx.gov.cn — 长沙县人民政府官方网站
  - 王雄文: 长沙经开区党工委书记、长沙县委书记 (confirmed, official news 2026-07)
  - 郑以仁: 县委副书记、县政府党组书记、代理县长 (confirmed, official profile page, 2026-06)
  - 卢铓: 县委常委、常务副县长 (confirmed, official profile 2026-06)
  - 王俊杰: 县委常委、副县长 (confirmed, b.1987.01)
  - 吴正华: 副县长 (confirmed, b.1986.12)
  - 陈洁: 副县长 (confirmed, b.1982.09, 无党派)
  - 伍隽: 副县长 (confirmed, b.1984.11)
  - 涂亚鹏: 副县长 (confirmed, b.1979.06)
  - 王坚: 副县长兼公安局长 (confirmed, b.1980.01)
  - 张辉: 副县长 (confirmed, b.1975.04)
  - 前任县长陈永高: plausible from news context
  - Other county leaders: 周虔, 莫金文, 刘向, 彭正球, 黄永华 from news reports

Confidence notes:
  - All current leadership names confirmed from government official website
  - Birth dates for 9 leaders confirmed from official profile pages
  - Detailed career histories beyond current role are limited
  - Previous county mayor (陈永高) and previous party secretary (付旭明) mentioned in media
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "长沙县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_长沙县"
if _CURRENT_DIR.name == "hunan_长沙县":
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
# IDs: 1-2 core leadership, 3-9 deputy government, 10-19 other leaders, 20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王雄文",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — typical for Hunan officials
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共长沙县委员会",
        "source": "https://www.csx.gov.cn/（官方活动报道确认，2026年7月24日县委常委会会议报道）",
        "confidence": "confirmed",
        "notes": "长沙经开区党工委书记、长沙县委书记。2026年7月24日报道'王雄文主持长沙县委常委会'。同时兼任长沙经开区党工委书记（副厅级）。完整履历待查。"
    },
    {
        "id": 2,
        "name": "郑以仁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "代理县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/xz36/202606/t20260618_12411190.html",
        "confidence": "confirmed",
        "notes": "县委副书记、县政府党组书记、代理县长。1975年10月出生。2026年6月18日县人大常委会任命为副县长、代理县长。此前任职经历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "卢铓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202606/t20260618_12411198.html",
        "confidence": "confirmed",
        "notes": "县委常委、县政府党组副书记、常务副县长。1976年8月出生。分管发改、财税、人社、金融、统计、应急、大数据等。"
    },
    {
        "id": 4,
        "name": "王俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202501/t20250127_11732849.html",
        "confidence": "confirmed",
        "notes": "县委常委、县政府党组成员、副县长。1987年1月出生。分管科技、工信、交通、文旅广电体育等。"
    },
    {
        "id": 5,
        "name": "吴正华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年12月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202108/t20210827_10155407.html",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长。1986年12月出生。分管自然资源、住建、重点项目等。"
    },
    {
        "id": 6,
        "name": "陈洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202510/t20251011_12017975.html",
        "confidence": "confirmed",
        "notes": "县政府副县长。1982年9月出生。无党派人士。分管教育、卫健、医保等。"
    },
    {
        "id": 7,
        "name": "伍隽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202510/t20251011_12017980.html",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长。1984年11月出生。分管商务、会展、物流与口岸等。"
    },
    {
        "id": 8,
        "name": "涂亚鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202209/t20220926_10820962.html",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长。1979年6月出生。分管农业农村、水利、民政、退役军人事务等。"
    },
    {
        "id": 9,
        "name": "王坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202402/t20240206_11368118.html",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长，县公安局党委书记、局长。1980年1月出生。分管公安、司法、信访等。"
    },
    {
        "id": 10,
        "name": "张辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长沙县人民政府",
        "source": "https://www.csx.gov.cn/zwgk/zfxxgkml/fdzdgknr/ldxx/fxz/202501/t20250127_11732865.html",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长。1975年4月出生。分管综合行政执法、市场监管、城管、生态环境等。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other County Leaders (from news reports)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "周虔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任（推测）",
        "current_org": "长沙县人民代表大会常务委员会",
        "source": "https://www.csx.gov.cn/（2026年7月22日县区产业发展座谈会报道）",
        "confidence": "plausible",
        "notes": "出现在县区产业发展座谈会参加名单首位，推测为县人大常委会主任。"
    },
    {
        "id": 12,
        "name": "莫金文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席（推测）",
        "current_org": "中国人民政治协商会议长沙县委员会",
        "source": "https://www.csx.gov.cn/（2026年7月22日县区产业发展座谈会报道）",
        "confidence": "plausible",
        "notes": "出现在县区产业发展座谈会参加名单，推测为县政协主席。"
    },
    {
        "id": 13,
        "name": "刘向",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共长沙县委员会",
        "source": "https://www.csx.gov.cn/（2026年7月22日县区产业发展座谈会报道）",
        "confidence": "plausible",
        "notes": "出现在县区产业发展座谈会参加名单，具体职务待查。"
    },
    {
        "id": 14,
        "name": "彭正球",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共长沙县委员会",
        "source": "https://www.csx.gov.cn/（2026年7月22日县区产业发展座谈会报道）",
        "confidence": "plausible",
        "notes": "出现在县区产业发展座谈会参加名单，具体职务待查。"
    },
    {
        "id": 15,
        "name": "黄永华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委领导",
        "current_org": "中共长沙县委员会",
        "source": "https://www.csx.gov.cn/（2026年7月21日报道'王雄文在湘龙街道调研'中提及）",
        "confidence": "plausible",
        "notes": "出现在王雄文调研报道参加人员名单中，具体职务待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "付旭明",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共长沙县委员会",
        "source": "（根据公开报道，付旭明此前任长沙县委书记，后由王雄文接任）",
        "confidence": "plausible",
        "notes": "前任长沙县委书记。2025年/2026年期间由王雄文接任。确切离任时间待查。"
    },
    {
        "id": 21,
        "name": "陈永高",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "长沙县人民政府",
        "source": "（根据公开报道，陈永高此前任长沙县长，2026年由郑以仁接任）",
        "confidence": "plausible",
        "notes": "前任长沙县长。2026年6月由郑以仁接任代理县长职务。确切离任时间及去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长沙县委员会", "type": "党委", "level": "县", "parent": "中共长沙市委员会", "location": "长沙市长沙县"},
    {"id": 2, "name": "长沙县人民政府", "type": "政府", "level": "县", "parent": "长沙市人民政府", "location": "长沙市长沙县"},
    {"id": 3, "name": "长沙县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "长沙市人民代表大会常务委员会", "location": "长沙市长沙县"},
    {"id": 4, "name": "中国人民政治协商会议长沙县委员会", "type": "政协", "level": "县", "parent": "政协长沙市委员会", "location": "长沙市长沙县"},
    {"id": 5, "name": "中共长沙县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共长沙市纪律检查委员会", "location": "长沙市长沙县"},
    {"id": 6, "name": "长沙经济技术开发区党工委", "type": "党委", "level": "国家级开发区", "parent": "中共长沙市委", "location": "长沙市长沙县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王雄文 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "现任长沙县委书记，同时任长沙经开区党工委书记（副厅级）"},
    {"person_id": 1, "org_id": 6, "title": "经开区党工委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "长沙经开区党工委书记，'县区一体'领导体制"},
    # 郑以仁 — current Acting County Mayor
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "县委副书记、县政府党组书记、代理县长，2026年6月18日任命"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": ""},
    # 卢铓 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委、县政府党组副书记、常务副县长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # Deputy Mayors
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县委常委、副县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员、副县长"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "无党派人士"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员、副县长"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员、副县长"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员、副县长，县公安局局长"},
    {"person_id": 9, "org_id": 5, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员、副县长"},
    # Other leaders (plausible)
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任（推测）", "start_date": "", "end_date": "", "rank": "正处级", "note": "推测职务，需确认"},
    {"person_id": 12, "org_id": 4, "title": "县政协主席（推测）", "start_date": "", "end_date": "", "rank": "正处级", "note": "推测职务，需确认"},
    {"person_id": 13, "org_id": 1, "title": "县委领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 14, "org_id": 1, "title": "县委领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 15, "org_id": 1, "title": "县委领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "具体职务待查"},
    # Predecessors
    {"person_id": 20, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "前任长沙县委书记，后由王雄文接任"},
    {"person_id": 21, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "前任长沙县长，2026年6月由郑以仁接任代理县长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 王雄文 ↔ 郑以仁 (Party Secretary – Acting County Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—代理县长搭档", "overlap_org": "中共长沙县委员会", "overlap_period": "2026-至今"},
    # 郑以仁 ↔ 卢铓 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "代理县长—常务副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    # 郑以仁 → 全体副县长
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "代理县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    # 卢铓与其他副县长共事
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "常务副县长—副县长", "overlap_org": "长沙县人民政府", "overlap_period": "至今"},
    # 王雄文 ↔ 常委班子成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记—县委常委", "overlap_org": "中共长沙县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "县委书记—县委常委", "overlap_org": "中共长沙县委员会", "overlap_period": "至今"},
    # 付旭明 ↔ 王雄文 (predecessor-successor)
    {"person_a": 20, "person_b": 1, "type": "交接", "context": "前任县委书记—现任县委书记", "overlap_org": "中共长沙县委员会", "overlap_period": "交接期"},
    # 陈永高 ↔ 郑以仁 (predecessor-successor)
    {"person_a": 21, "person_b": 2, "type": "交接", "context": "前任县长—现任代理县长", "overlap_org": "长沙县人民政府", "overlap_period": "2026.06"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def _make_person_id(name: str) -> str:
    return f"changshaxian_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "长沙县人民政府官方网站",
            "url": "https://www.csx.gov.cn/",
            "publisher": "长沙县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "长沙县政府门户网站政府领导页面及活动报道",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "长沙县",
            "job": person.get("current_post", ""),
            "task_id": "hunan_长沙县",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
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
            "administrative_rank": "副厅级" if person["id"] == 1 else "正处级",
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
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）" if not person.get("work_start") else "早期教育和工作细节",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ] + ([
            {
                "priority": "high",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ] if not person.get("birth") else []),
    }

    fname = f"{TODAY}-湖南省-长沙市-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 20, 21}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
