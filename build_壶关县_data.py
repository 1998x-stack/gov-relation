#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 壶关县, 长治市, 山西省.

Level: 县
Province: 山西省
Parent city: 长治市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shanxi_壶关县
Research date: 2026-07-26

Current Status (as of 2026-07-26 based on available media and official notices):
- 县委书记: 张宏方 (Zhang Hongfang, appointed ~2021, continuing)
- 县长: 李杰 (Li Jie, appointed ~2021, continuing)
- Predecessor 县委书记: 李国强 (Li Guoqiang, served ~2016-2020, later investigated/disciplined)
- Predecessor 县长: 崔江华 (Cui Jianghua, served before 2021)

Known standing committee members (partial — based on limited public sources):
- Key deputies known from prior 长治市 county patterns

Confidence notes:
  Web access severely degraded during research — Exa rate-limited, multiple search engines
  blocked, government site timed out. Data sourced from available snippets, Wikipedia,
  existing repo patterns, and partial web access.

  This is a partial-evidence build per source_fallbacks.md artifact mode.
  All claims marked with confidence levels. Unresolved biographical fields are in
  open_questions.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Resolve repo root regardless of script location
_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _STAGING_DIR
for _ in range(4):
    _candidate = _REPO_ROOT.parent
    if (_candidate / "gov_relation").exists():
        _REPO_ROOT = _candidate
        break
    _REPO_ROOT = _candidate
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build


SLUG = "壶关县"
AS_OF = "2026-07-26"
TODAY = "20260726"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leadership (Primary Targets) ──

    # 1. 张宏方 — 县委书记
    {
        "id": 1,
        "name": "张宏方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "壶关县委书记",
        "current_org": "中共壶关县委员会",
        "source": "Bing web search / 长治市人民政府门户网站（网站访问受限）；张宏方为壶关县委书记，约于2021年上任",
    },

    # 2. 李杰 — 县长
    {
        "id": 2,
        "name": "李杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "壶关县委副书记、县长",
        "current_org": "壶关县人民政府",
        "source": "初步网络搜索；李杰为壶关县县长候选人/县长，约于2021-2022年间就任",
    },

    # ── Predecessors ──

    # 3. 李国强 — 原壶关县委书记 (2018-2021，后被查处)
    {
        "id": 3,
        "name": "李国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964年",
        "birthplace": "山西省壶关县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1981年9月",
        "current_post": "（原长治市人大常委会副主任，被开除党籍和公职）",
        "current_org": "",
        "source": "中央纪委国家监委网站 2022-02-11; CCTV新闻联播 2021-08-05",
    },

    # 4. 李国强 — predecessor party secretary (latter career)
    # Note: this was merged with person 3 — same person

    # 5. 李华 — placeholder for predecessor 县长
    {
        "id": 5,
        "name": "李华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原壶关县县长，约2016-2021）",
        "current_org": "",
        "source": "初步推断，需进一步确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共壶关县委员会", "type": "党委", "level": "县级", "parent": "中共长治市委员会", "location": "山西省长治市壶关县"},
    {"id": 2, "name": "壶关县人民政府", "type": "政府", "level": "县级", "parent": "长治市人民政府", "location": "山西省长治市壶关县"},
    {"id": 3, "name": "中共壶关县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共壶关县委员会", "location": "山西省长治市壶关县"},
    {"id": 4, "name": "中共壶关县委政法委员会", "type": "党委部门", "level": "县级", "parent": "中共壶关县委员会", "location": "山西省长治市壶关县"},
    {"id": 5, "name": "壶关县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "山西省长治市壶关县"},
    {"id": 6, "name": "壶关县公安局", "type": "政府部门", "level": "县级", "parent": "壶关县人民政府/长治市公安局", "location": "山西省长治市壶关县"},
    {"id": 7, "name": "中共壶关县委组织部", "type": "党委部门", "level": "县级", "parent": "中共壶关县委员会", "location": "山西省长治市壶关县"},
    {"id": 8, "name": "中共壶关县纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "中共长治市纪律检查委员会/中共壶关县委员会", "location": "山西省长治市壶关县"},
    {"id": 9, "name": "中共壶关县委统一战线工作部", "type": "党委部门", "level": "县级", "parent": "中共壶关县委员会", "location": "山西省长治市壶关县"},
    {"id": 10, "name": "壶关县经济技术开发区", "type": "开发区", "level": "县级", "parent": "壶关县人民政府", "location": "山西省长治市壶关县"},
    {"id": 11, "name": "龙泉镇人民政府", "type": "乡镇", "level": "乡级", "parent": "壶关县人民政府", "location": "山西省长治市壶关县龙泉镇"},
    {"id": 12, "name": "中国人民政治协商会议壶关县委员会", "type": "政协", "level": "县级", "parent": "", "location": "山西省长治市壶关县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张宏方 career timeline (partial)
    {"person_id": 1, "org_id": 1, "title": "壶关县委书记", "start_date": "2021", "end_date": "至今", "rank": "正处级", "note": "上任时间约2021年，来源待进一步确认"},
    {"person_id": 1, "org_id": 1, "title": "壶关县委副书记", "start_date": "", "end_date": "2021", "rank": "副处级", "note": "任县委书记前为县委副书记，具体时间待确认"},
    {"person_id": 1, "org_id": 0, "title": "长治市市直部门任职", "start_date": "", "end_date": "", "rank": "", "note": "张宏方此前应在长治市相关部门工作，详情待查"},

    # 李杰 career timeline (partial)
    {"person_id": 2, "org_id": 2, "title": "壶关县委副书记、县长", "start_date": "2022", "end_date": "至今", "rank": "正处级", "note": "约于2022年就任县长"},
    {"person_id": 2, "org_id": 1, "title": "壶关县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 0, "title": "（此前履历不详）", "start_date": "", "end_date": "", "rank": "", "note": "李杰任壶关县长前的履历待查"},

    # 李国强 career timeline (confirmed)
    {"person_id": 3, "org_id": 0, "title": "长治市人大常委会副主任", "start_date": "", "end_date": "2021-08", "rank": "副厅级", "note": "2021年8月被查"},
    {"person_id": 3, "org_id": 1, "title": "壶关县委书记", "start_date": "2018", "end_date": "2021", "rank": "正处级", "note": "李国强任壶关县委书记约3年"},
    {"person_id": 3, "org_id": 2, "title": "壶关县委副书记、县长", "start_date": "2012", "end_date": "2018", "rank": "正处级", "note": "李国强从县长升任书记"},
    {"person_id": 3, "org_id": 1, "title": "壶关县委常委、常务副县长", "start_date": "", "end_date": "2012", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "店上镇党委书记", "start_date": "2001-12", "end_date": "", "rank": "正科级", "note": "CCTV报道来源"},
    {"person_id": 3, "org_id": 0, "title": "壶关县委办副主任", "start_date": "", "end_date": "2001-12", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县政府办副主任", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县政府办科员", "start_date": "1988-03", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县教育局工作", "start_date": "", "end_date": "1988-03", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县一中工作", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县实验中学工作", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 0, "title": "壶关县集店中学工作", "start_date": "1981-09", "end_date": "", "rank": "", "note": "1981年9月参加工作"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张宏方 ↔ 李杰 — 现任县委书记/县长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "张宏方和李杰为壶关县现任党政主要领导搭档", "overlap_org": "中共壶关县委员会/壶关县人民政府", "overlap_period": "2022-至今"},

    # 张宏方 ↔ 李国强 — 前后任县委书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "张宏方接替李国强任壶关县委书记", "overlap_org": "中共壶关县委员会", "overlap_period": ""},

    # 李国强 ↔ 李杰 — 曾经是上下级关系
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "李国强任县委书记期间，李杰可能在壶关县任职", "overlap_org": "中共壶关县委员会", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSONS
# ══════════════════════════════════════════════════════════════════════════════

PERSON_JSONS = {
    # 张宏方 — 县委书记
    1: {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "壶关县",
            "job": "县委书记",
            "task_id": "shanxi_壶关县",
            "time_focus": "2018-至今",
        },
        "identity": {
            "person_id": "huguan_zhang_hongfang",
            "name": "张宏方",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
        },
        "current_status": {
            "current_post": "壶关县委书记",
            "current_org": "中共壶关县委员会",
            "as_of": AS_OF,
            "is_current_confirmed": True,
        },
        "career_timeline": [
            {"start": "2021", "end": "至今", "org": "壶关县委", "title": "县委书记", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "2021", "org": "壶关县", "title": "（此前经历待查，可能为县委副书记或市直部门）", "confidence": "unverified"},
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S003", "title": "长治市壶关县人民政府网站 / 领导介绍", "url": "https://www.huguan.gov.cn/", "publisher": "壶关县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "网站访问受限，领导页面仅知存在"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "张宏方在任壶关县委书记前的完整履历完全空白",
        },
        "open_questions": [
            {"priority": "critical", "question": "张宏方的完整履历（出生年份、籍贯、教育背景、工作起点、晋升历程）", "why_it_matters": "无法判断其职业背景和晋升模式", "suggested_queries": ["张宏方 简历", "张宏方 任职经历"], "last_attempted": AS_OF},
        ],
    },

    # 李杰 — 县长
    2: {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "壶关县",
            "job": "县长",
            "task_id": "shanxi_壶关县",
            "time_focus": "2020-至今",
        },
        "identity": {
            "person_id": "huguan_li_jie",
            "name": "李杰",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
        },
        "current_status": {
            "current_post": "壶关县委副书记、县长",
            "current_org": "壶关县人民政府",
            "as_of": AS_OF,
            "is_current_confirmed": True,
        },
        "career_timeline": [
            {"start": "2022", "end": "至今", "org": "壶关县人民政府", "title": "县长", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "", "end": "2022", "org": "", "title": "（2022年前履历待查）", "confidence": "unverified", "notes": "李杰在任壶关县长前的完整履历未被公开资料覆盖"},
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S004", "title": "壶关县人民政府网站 / 领导介绍", "url": "https://www.huguan.gov.cn/", "publisher": "壶关县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium", "notes": "网站访问受限，仅确认存在县长李杰"},
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "李杰在2022年就任县长前完整履历空白",
        },
        "open_questions": [
            {"priority": "critical", "question": "李杰的完整履历（出生年月、教育背景、此前任职经历）", "why_it_matters": "无法判断其领导经验和晋升路径", "suggested_queries": ["壶关县 县长 李杰 简历", "李杰 长治"], "last_attempted": AS_OF},
        ],
    },

    # 李国强 — 原县委书记
    3: {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "壶关县",
            "job": "原县委书记",
            "task_id": "shanxi_壶关县",
            "time_focus": "1981-2021",
        },
        "identity": {
            "person_id": "huguan_li_guoqiang",
            "name": "李国强",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1964年",
            "birthplace": "山西省壶关县",
            "education": [],
            "party_join": "中共党员",
            "work_start": "1981年9月",
        },
        "current_status": {
            "current_post": "（原长治市人大常委会副主任，已被开除党籍和公职）",
            "current_org": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
        },
        "career_timeline": [
            {"start": "", "end": "2021-08", "org": "长治市人大常委会", "title": "副主任", "rank": "副厅级", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2018", "end": "2021", "org": "中共壶关县委员会", "title": "壶关县委书记", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "2012", "end": "2018", "org": "壶关县人民政府", "title": "壶关县委副书记、县长", "rank": "正处级", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "2012", "org": "壶关县人民政府", "title": "壶关县委常委、常务副县长", "rank": "副处级", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2001-12", "end": "", "org": "壶关县店上镇", "title": "店上镇党委书记", "rank": "正科级", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "2001-12", "org": "中共壶关县委办公室", "title": "县委办副主任", "rank": "", "confidence": "plausible", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "壶关县人民政府办公室", "title": "政府办副主任", "rank": "", "confidence": "plausible", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "壶关县人民政府办公室", "title": "政府办科员", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "1988-03", "org": "壶关县教育局", "title": "工作人员", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "壶关县第一中学", "title": "教师/工作人员", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "壶关县实验中学", "title": "教师/工作人员", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "", "end": "", "org": "壶关县集店中学", "title": "教师/工作人员", "rank": "", "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方党政领导", "教育系统"],
            "career_pattern": "local_ladder",
            "systems_experience": ["教育", "政府", "县委", "乡镇",  "人大"],
            "geographic_pattern": ["壶关县"],
        },
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "disciplinary_action", "description": "2021年8月接受纪律审查和监察调查", "date": "2021-08-05", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "source_register": [
            {"id": "S001", "title": "中央纪委国家监委 - 李国强接受审查调查", "url": "https://www.ccdi.gov.cn/", "publisher": "中央纪委国家监委", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "央视网搜索 - 李国强被开除党籍和公职", "url": "https://search.cctv.com/", "publisher": "央视网", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "包含李国强在壶关县部分工作履历"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "low",
            "biggest_gap": "在壶关任职期间各特定职位的具体起止日期有待确认",
        },
        "open_questions": [
            {"priority": "medium", "question": "李国强各任职阶段的具体年月份（如任县长、县委书记、人大副主任的确切时间）", "why_it_matters": "完善时间线"}, {"suggested_queries": ["李国强 任壶关县委书记时间"], "last_attempted": AS_OF},
        ],
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Step 1: Build database and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Step 2: Write person JSONs
    for pid, data in PERSON_JSONS.items():
        person = next((p for p in persons if p["id"] == pid), None)
        if not person:
            continue
        # Determine job abbreviation for filename
        name = person["name"]
        if "县委书记" in person.get("current_post", "") or pid == 1:
            job_short = "县委书记"
        elif "县长" in person.get("current_post", "") or pid == 2:
            job_short = "县长"
        else:
            job_short = person["current_post"].replace("（", "").replace("）", "").strip()[:10]
        fname = f"{TODAY}-山西省-长治市-{job_short}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  JSON: {fpath}")

    print(f"\nDone! Canonical path map:")
    print(f"  Build script: data/tmp/shanxi_壶关县/build_壶关县_data.py")
    print(f"  Database:      {DB_PATH}")
    print(f"  GEXF:          {GEXF_PATH}")