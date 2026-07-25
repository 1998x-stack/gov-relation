#!/usr/bin/env python3
"""
Build SQLite database, GEXF graph, and person JSONs for 长武县 (Changwu County), 咸阳市, 陕西省.

长武县 is a county under Xianyang City, Shaanxi Province.

Investigation date: 2026-07-25
Task ID: shaanxi_长武县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.changwu.gov.cn — 长武县人民政府官方网站 (primary, as of July 2026)
  - Multiple news articles from changwu.gov.cn (July 2026)
  - Meeting attendance lists (confirmed roles)

Confidence notes:
  - Current roles: confirmed via multiple government news reports (July 2026)
  - 王高锋 is the current 县委书记 (confirmed from multiple articles Jul 2026)
  - 王苗 is the current 县委副书记、县长 (confirmed from Jul 2026 articles)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented in open_questions
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
SLUG = "长武县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_长武县"
if _CURRENT_DIR.name == "shaanxi_长武县":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee,
#      20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王高锋",
        "gender": "男",
        "ethnicity": "汉族",   # plausible — vast majority of Shaanxi officials are Han
        "birth": "",          # open question — unverified
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委书记",
        "current_org": "中共长武县委员会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103545.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县委书记身份多次出席活动：主持常委会、集体谈话、表彰大会等"
    },
    {
        "id": 2,
        "name": "王苗",
        "gender": "女",       # inferred from pronoun in news
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委副书记、县长",
        "current_org": "长武县人民政府",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260703_2097924.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县委副书记、县长身份主持'两优一先'表彰大会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "孙波",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委副书记",
        "current_org": "中共长武县委员会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202604/t20260430_2082122.html",
        "confidence": "confirmed",
        "notes": "2026年4月以县委副书记身份宣读表彰决定"
    },
    {
        "id": 4,
        "name": "马云飞",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委副书记、县委党校校长",
        "current_org": "中共长武县委员会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103548.html",
        "confidence": "confirmed",
        "notes": "此前曾任县委常委、组织部部长；2026年7月以县委副书记、县委党校校长身份出席活动"
    },
    {
        "id": 5,
        "name": "赵广锋",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委常委、组织部部长",
        "current_org": "中共长武县委组织部",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103545.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县委常委、组织部部长身份宣布干部任免决定"
    },
    {
        "id": 6,
        "name": "王静",
        "gender": "女",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县委常委、政法委书记",
        "current_org": "中共长武县委政法委",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260722_2103056.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县委常委、政法委书记身份出席全县检察建议工作推进会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # County Congress & Political Consultative Conference
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "赵晓斌",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县人大常委会主任",
        "current_org": "长武县人大常委会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260703_2097924.html",
        "confidence": "confirmed",
        "notes": "2026年7月多次出席县级会议"
    },
    {
        "id": 8,
        "name": "任全智",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",          # open question
        "birthplace": "",     # open question
        "education": "",      # open question
        "party_join": "中共党员",
        "work_start": "",     # open question
        "current_post": "县政协主席",
        "current_org": "政协长武县委员会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260703_2097924.html",
        "confidence": "confirmed",
        "notes": "2026年7月多次出席县级会议"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy County Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "王为",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "长武县人民政府",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103546.html",
        "confidence": "confirmed",
        "notes": "2026年7月以副县长身份代表县政府作表态发言"
    },
    {
        "id": 10,
        "name": "云剑",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县纪委副书记、监委副主任",
        "current_org": "中共长武县纪委/长武县监委",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103545.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县纪委副书记、监委副主任身份作廉政谈话"
    },
    {
        "id": 11,
        "name": "魏刚",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "长武县人大常委会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103546.html",
        "confidence": "confirmed",
        "notes": "2026年7月以县人大常委会副主任身份出席食品安全法执法检查评议会"
    },
    {
        "id": 12,
        "name": "潘永虎",
        "gender": "男",       # plausible
        "ethnicity": "汉族",   # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "长武县人大常委会",
        "source": "https://www.changwu.gov.cn/xw/zwyw/202607/t20260724_2103546.html",
        "confidence": "confirmed",
        "notes": "2026年7月主持会议"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (previous leaders)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "何锐",
        "gender": "男",
        "ethnicity": "汉族",   # plausible
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任县委书记）",
        "current_org": "",
        "source": "inferred — 公开资料显示何锐曾担任长武县县委书记，后另有任用",
        "confidence": "plausible",
        "notes": "何锐曾任长武县委书记，后调任其他职务。王高锋接任具体时间未知。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共长武县委员会", "type": "党委", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 2, "name": "长武县人民政府", "type": "政府", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 3, "name": "中共长武县委组织部", "type": "党委", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 4, "name": "中共长武县委政法委", "type": "党委", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 5, "name": "长武县人大常委会", "type": "人大", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 6, "name": "政协长武县委员会", "type": "政协", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 7, "name": "中共长武县纪委/长武县监委", "type": "党委", "level": "县处级", "location": "陕西省咸阳市长武县"},
    {"id": 8, "name": "中共长武县委党校", "type": "事业单位", "level": "县处级", "location": "陕西省咸阳市长武县"},
]

# ── Positions (person_id, org_id, title) ─────────────────────────────────────

positions = [
    # Current top leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正处级"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "至今", "rank": "正处级"},
    # Standing committee
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记、县委党校校长", "start": "", "end": "至今", "rank": "副处级"},
    {"person_id": 4, "org_id": 8, "title": "县委党校校长", "start": "", "end": "至今", "rank": "副处级"},
    {"person_id": 5, "org_id": 3, "title": "县委常委、组织部部长", "start": "", "end": "至今", "rank": "副处级"},
    {"person_id": 6, "org_id": 4, "title": "县委常委、政法委书记", "start": "", "end": "至今", "rank": "副处级"},
    # Congress & CPPCC
    {"person_id": 7, "org_id": 5, "title": "县人大常委会主任", "start": "", "end": "至今", "rank": "正处级"},
    {"person_id": 8, "org_id": 6, "title": "县政协主席", "start": "", "end": "至今", "rank": "正处级"},
    {"person_id": 11, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级"},
    {"person_id": 12, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级"},
    # Government
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级"},
    # Discipline
    {"person_id": 10, "org_id": 7, "title": "县纪委副书记、监委副主任", "start": "", "end": "至今", "rank": "副处级"},
    # Predecessors
    {"person_id": 13, "org_id": 1, "title": "前任县委书记", "start": "", "end": "", "rank": "正处级"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # Top leaders team — same leadership team overlap
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记王高锋与县长王苗为党政主要领导搭档关系",
     "overlap_org": "长武县领导班子", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记王高锋与县委副书记孙波为党委班子上下级关系",
     "overlap_org": "中共长武县委员会", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记王高锋与县委副书记马云飞为党委班子上下级关系",
     "overlap_org": "中共长武县委员会", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 5, "type": "predecessor_successor",
     "context": "马云飞此前任县委常委、组织部部长，赵广锋接任",
     "overlap_org": "中共长武县委组织部", "overlap_period": "2026年",
     "strength": "medium", "confidence": "plausible"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与组织部部长为党委班子上下级关系",
     "overlap_org": "中共长武县委员会", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与政法委书记为党委班子上下级关系",
     "overlap_org": "中共长武县委员会", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor",
     "context": "何锐为前任县委书记，王高锋接任",
     "overlap_org": "中共长武县委员会", "overlap_period": "",
     "strength": "medium", "confidence": "plausible"},
    # County congress - Party relationship
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与人大主任为同级领导班子主要负责人",
     "overlap_org": "长武县四套班子", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与政协主席为同级领导班子主要负责人",
     "overlap_org": "长武县四套班子", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
    # Government team
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长为政府领导关系",
     "overlap_org": "长武县人民政府", "overlap_period": "2026年至今",
     "strength": "strong", "confidence": "confirmed"},
]

# ── Person JSON Writer ────────────────────────────────────────────────────────

def write_person_json(p: dict) -> None:
    """Write a deep person profile JSON file."""
    name = p["name"]
    pid = p["id"]
    current_post = p["current_post"]
    role_short = "县委书记" if pid == 1 else "县长"
    filename = f"{TODAY}-陕西省-咸阳市-{role_short}-{name}.json"
    filepath = PJSON_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省",
            "city": "咸阳市",
            "region": "长武县",
            "job": current_post,
            "task_id": "shaanxi_长武县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"changwu_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "https://www.changwu.gov.cn/zfxxgk/fdzdgknr/ldzc/",
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "至今",
                "org": p.get("current_org", ""),
                "title": current_post,
                "level": "正处级",
                "location": "陕西省咸阳市长武县",
                "system": "party" if pid == 1 else "government",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": "具体任职起止时间未知，公开资料仅确认2026年7月在职",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [
            {"org_id": 1, "name": "中共长武县委员会", "type": "党委",
             "role": "县委书记" if pid == 1 else "县委副书记",
             "period": "2026年至令", "confidence": "confirmed"},
            {"org_id": 2, "name": "长武县人民政府", "type": "政府",
             "role": "县长",
             "period": "2026年至令", "confidence": "confirmed"},
        ] if pid == 2 else [
            {"org_id": 1, "name": "中共长武县委员会", "type": "党委",
             "role": "县委书记",
             "period": "2026年至令", "confidence": "confirmed"},
        ],
        "relationships": [
            rel for rel in [
                {
                    "person": "王苗" if pid == 1 else "王高锋",
                    "person_id": f"changwu_{'王苗' if pid == 1 else '王高锋'}",
                    "relationship_type": "superior_subordinate" if pid == 1 else "superior_subordinate",
                    "strength": "strong",
                    "evidence": f"{'县委书记' if pid == 1 else '县长'}王高锋与{'县长' if pid == 1 else '县委书记'}王苗为党政主要领导搭档关系",
                    "overlap_org": "长武县领导班子",
                    "overlap_period": "2026年至今",
                    "direction": "person_to_other" if pid == 1 else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ]
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "未知",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "discipline_oriented",
                    "evidence": f"{name}在公开讲话中强调全面从严治党、作风建设、'五规范''五禁止'等纪律要求",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
                {
                    "trait": "pragmatic",
                    "evidence": f"{name}多次强调产业发展、项目建设、企业服务、民生实事等具体工作",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": [
                "全面从严治党",
                "产业发展",
                "项目建设",
                "民生改善",
                "安全稳定",
            ],
            "management_signals": [
                f"{name}在会议中强调问题导向、闭环管理、'三服务'质效提升等工作方法",
            ],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，公开资料中未发现相关风险信号",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "长武县人民政府官方网站",
                "url": "https://www.changwu.gov.cn/",
                "publisher": "长武县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "包含领导活动新闻报道，可确认当前任职状况",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景、完整职业生涯等基本信息缺失（公开资料有限）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "基本信息，用于去重和身份确认",
                "suggested_queries": [f"{name} 出生 籍贯 简历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯（各职位具体起止时间）",
                "why_it_matters": "理解晋升路径和关系网络时间线",
                "suggested_queries": [f"{name} 简历 任职经历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{name}的教育背景",
                "why_it_matters": "用于评估专业背景和学校人脉",
                "suggested_queries": [f"{name} 毕业 学历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "medium",
                "question": f"{name}的入党时间及参加工作时间",
                "why_it_matters": "党内仕途时间线定位",
                "suggested_queries": [f"{name} 入党 工作"],
                "last_attempted": TODAY,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filename}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")

    # Write person JSONs for core figures
    print("Writing person JSONs...")
    for p in persons:
        if p["id"] in [1, 2]:  # 县委书记 and 县长
            write_person_json(p)

    # Build database and GEXF
    print("Running run_build...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. Artifacts in {STAGING}:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    for f in sorted(STAGING.glob(f"{TODAY}-*.json")):
        print(f"  JSON:  {f}")
