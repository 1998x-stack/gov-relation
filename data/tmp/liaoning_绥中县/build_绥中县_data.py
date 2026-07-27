#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 绥中县, 葫芦岛市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_绥中县
Level: 县
Targets: 县委书记 & 县长

Research status: WEB ACCESS PARTIAL
  - Exa API rate-limited (free tier exhausted)
  - Baidu Baike: 403 forbidden
  - Official 绥中县人民政府网站 (www.szx.gov.cn): accessible (Suizhong county gov site)
  - 葫芦岛市人民政府网站 (www.hld.gov.cn): accessible
  - Jina Reader: timeout errors
  - Baidu web search: 403 captcha block

Confirmed current officeholders (from official sources):
  - 县委书记: 马天峰 (confirmed via county People's Congress news, 2026-07-24)
    Also: 东戴河新区党工委书记
  - 县长: 单伟 (confirmed via county government leadership duty notice, 2026-05-28;
    formally elected at People's Congress, 2026-07-24)
    Also: 东戴河新区管委会主任

Notes:
  - Suizhong county government site (szx.gov.cn) was the primary reliable source.
    The DNS for suizhong.gov.cn failed to resolve; szx.gov.cn has the same content.
  - Personnel appointment notices and leadership duty assignment documents
    were directly accessible via Python urllib requests.
  - Party committee leadership (县委常委) composition partially inferred from
    meeting reports; detailed biographies not yet collected from web.
  - Predecessor/successor data for 县委书记 requires further research.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "绥中县"
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
        "name": "马天峰",
        "current_post": "县委书记",
        "current_org": "中共绥中县委员会",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
    },
    # ── 县长 ──
    {
        "id": 2,
        "name": "单伟",
        "current_post": "县长",
        "current_org": "绥中县人民政府",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 常务副县长 ──
    {
        "id": 3,
        "name": "邱枫",
        "current_post": "常务副县长",
        "current_org": "绥中县人民政府",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 副县长（分管城建交通）──
    {
        "id": 4,
        "name": "叶明",
        "current_post": "副县长",
        "current_org": "绥中县人民政府",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 副县长（分管农业农村）──
    {
        "id": 5,
        "name": "王启明",
        "current_post": "副县长",
        "current_org": "绥中县人民政府",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 副县长（分管商务招商）──
    {
        "id": 6,
        "name": "王尧",
        "current_post": "副县长",
        "current_org": "绥中县人民政府",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 副县长、公安局长 ──
    {
        "id": 7,
        "name": "吴旭",
        "current_post": "副县长、县公安局局长",
        "current_org": "绥中县人民政府、绥中县公安局",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
    },
    # ── 县人大常委会副主任 ──
    {
        "id": 8,
        "name": "马勇",
        "current_post": "县人大常委会副主任",
        "current_org": "绥中县人大常委会",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
    },
    # ── 县监察委员会主任 ──
    {
        "id": 9,
        "name": "蒲文涛",
        "current_post": "县监察委员会主任",
        "current_org": "绥中县监察委员会",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
    },
    # ── 县政协主席 ──
    {
        "id": 10,
        "name": "杨国刚",
        "current_post": "县政协主席",
        "current_org": "绥中县政协",
        "aliases": "",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "party_join": "",
        "work_start": "",
        "education": "",
        "source": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共绥中县委员会", "type": "党委", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 2, "name": "绥中县人民政府", "type": "政府", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 3, "name": "绥中县人大常委会", "type": "人大", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 4, "name": "绥中县政协", "type": "政协", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 5, "name": "绥中县监察委员会", "type": "纪委", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 6, "name": "绥中县公安局", "type": "政府", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
    {"id": 7, "name": "东戴河新区", "type": "开发区", "level": "县级", "location": "辽宁省葫芦岛市绥中县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 马天峰
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "未知", "end": "现任", "confidence": "confirmed"},
    {"person_id": 1, "org_id": 7, "title": "东戴河新区党工委书记", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 单伟
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2026-05", "end": "现任", "confidence": "confirmed"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start": "2026-05前", "end": "2026-07", "confidence": "confirmed"},
    {"person_id": 2, "org_id": 7, "title": "东戴河新区管委会主任", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 邱枫
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 叶明
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 王启明
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 王尧
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 吴旭
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    {"person_id": 7, "org_id": 6, "title": "县公安局局长", "start": "未知", "end": "现任", "confidence": "confirmed"},
    # 马勇
    {"person_id": 8, "org_id": 3, "title": "县人大常委会副主任", "start": "2026-07", "end": "现任", "confidence": "confirmed"},
    # 蒲文涛
    {"person_id": 9, "org_id": 5, "title": "县监察委员会主任", "start": "2026-07", "end": "现任", "confidence": "confirmed"},
    # 杨国刚
    {"person_id": 10, "org_id": 4, "title": "县政协主席", "start": "未知", "end": "现任", "confidence": "confirmed"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 马天峰 <-> 单伟: top leaders in same county
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长，党政主要领导搭档",
     "overlap_org": "绥中县", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 马天峰 <-> 邱枫: 书记与常务副县长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与常务副县长，邱枫协助党建工作",
     "overlap_org": "绥中县", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 单伟 <-> 邱枫: 县长与常务副县长（助手关系）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长，邱枫协助县长分管审计局",
     "overlap_org": "绥中县人民政府", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 单伟 <-> 叶明: 县长与副县长
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与副县长，同一届政府班子",
     "overlap_org": "绥中县人民政府", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 单伟 <-> 王启明: 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "县长与副县长，同一届政府班子",
     "overlap_org": "绥中县人民政府", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 单伟 <-> 王尧: 县长与副县长
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与副县长，同一届政府班子",
     "overlap_org": "绥中县人民政府", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
    # 单伟 <-> 吴旭: 县长与公安局长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长兼公安局长",
     "overlap_org": "绥中县人民政府", "overlap_period": "2026年至今",
     "confidence": "confirmed"},
]


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    # Ensure staging directory exists
    _CURRENT_DIR.mkdir(parents=True, exist_ok=True)

    # Run the build
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

    # Write person JSON files
    write_person_jsons()

    print(f"\nDone. Artifacts in {_CURRENT_DIR}/")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")


def write_person_jsons() -> None:
    """Write individual person JSON files for core leaders (马天峰 and 单伟)."""
    persons_dir = _CURRENT_DIR
    today = TODAY

    # ── 马天峰 (县委书记) ──
    matianfeng = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "辽宁省",
            "city": "葫芦岛市",
            "region": "绥中县",
            "job": "县委书记",
            "task_id": "liaoning_绥中县",
            "time_focus": "2026年当前"
        },
        "identity": {
            "person_id": "liaoning_huludao_suizhong_matianfeng",
            "name": "马天峰",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "马天峰",
                "name_birthplace": "马天峰",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "县委书记",
            "current_org": "中共绥中县委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "现任",
                "org": "中共绥中县委员会",
                "title": "县委书记",
                "level": "正处级",
                "location": "辽宁省葫芦岛市绥中县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "同时担任东戴河新区党工委书记。在2026年7月绥中县第十七届人民代表大会第七次会议上发表讲话。",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "未知",
                "end": "现任",
                "org": "东戴河新区",
                "title": "东戴河新区党工委书记",
                "level": "未知",
                "location": "辽宁省葫芦岛市绥中县",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "东戴河新区党工委书记，与县委书记同一职务兼任",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"org_name": "中共绥中县委员会", "role": "书记", "period": "现任"},
            {"org_name": "东戴河新区", "role": "党工委书记", "period": "现任"}
        ],
        "relationships": [
            {
                "person": "单伟",
                "person_id": "liaoning_huludao_suizhong_shanwei",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县委书记与县长搭档，2026年7月县人代会共同出席会议",
                "overlap_org": "绥中县",
                "overlap_period": "2026年至今",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [
            {
                "period": "截至2026年7月",
                "domain": "other",
                "achievement_or_event": "在绥中县第十七届人民代表大会第七次会议闭幕会上发表讲话，提出四点意见：坚持党的领导、紧扣发展大局、践行初心使命、加强自身建设",
                "role_in_event": "县委书记",
                "measurable_outcome": "",
                "location": "绥中县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "公开资料有限，仅从县人代会讲话可见其重视党的领导和制度建设",
                    "confidence": "unverified",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["党的全面领导", "高质量发展", "民生福祉", "自身建设"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开渠道未发现马天峰的负面信息或纪律处分记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "绥中县第十七届人民代表大会第七次会议闭幕",
                "url": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
                "publisher": "绥中县人民政府",
                "published_at": "2026-07-24",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "官方新闻报道，确认马天峰担任县委书记，单伟当选县长"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "马天峰的完整履历（出生年月、籍贯、教育背景、历任职务）均未查到"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "马天峰的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "核心领导身份字段缺失，影响人物唯一性确认",
                "suggested_queries": ["马天峰 简历 绥中", "马天峰 出生", "马天峰 个人简历"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "马天峰调到绥中县任县委书记前担任什么职务？",
                "why_it_matters": "了解其职业路径和地域调动模式",
                "suggested_queries": ["马天峰 任前公示 葫芦岛", "马天峰 任职 简历"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "马天峰何时开始担任绥中县委书记？",
                "why_it_matters": "确定任期起点，支持任期重叠分析",
                "suggested_queries": ["马天峰 绥中县委书记 任命"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    shanwei = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "辽宁省",
            "city": "葫芦岛市",
            "region": "绥中县",
            "job": "县长",
            "task_id": "liaoning_绥中县",
            "time_focus": "2026年当前"
        },
        "identity": {
            "person_id": "liaoning_huludao_suizhong_shanwei",
            "name": "单伟",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "单伟",
                "name_birthplace": "单伟",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "县长",
            "current_org": "绥中县人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {
                "start": "2026-05之前",
                "end": "2026-07",
                "org": "绥中县人民政府",
                "title": "代县长",
                "level": "正处级",
                "location": "辽宁省葫芦岛市绥中县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "代县长，后正式当选县长。担任东戴河新区管委会主任。",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "2026-07-23",
                "end": "现任",
                "org": "绥中县人民政府",
                "title": "县长",
                "level": "正处级",
                "location": "辽宁省葫芦岛市绥中县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月23日在绥中县第十七届人民代表大会第七次会议上正式当选县长",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "未知",
                "end": "现任",
                "org": "东戴河新区",
                "title": "东戴河新区管委会主任",
                "level": "未知",
                "location": "辽宁省葫芦岛市绥中县",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "东戴河新区管委会主任，与县长职务兼任",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"org_name": "绥中县人民政府", "role": "县长", "period": "2026年至今"},
            {"org_name": "东戴河新区", "role": "管委会主任", "period": "现任"}
        ],
        "relationships": [
            {
                "person": "马天峰",
                "person_id": "liaoning_huludao_suizhong_matianfeng",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "2026年7月当选后表态'在以天峰书记为班长的带领下'工作，确认党政正职关系",
                "overlap_org": "绥中县",
                "overlap_period": "2026年至今",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "邱枫",
                "person_id": "",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "县长与常务副县长，邱枫协助县长分管审计局等工作",
                "overlap_org": "绥中县人民政府",
                "overlap_period": "2026年至今",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "当选县长后表态提出'产业强、创新优、港口兴、开放活、生态美'目标，推进'一核牵引、四片协同、三产循环'全域发展战略",
                "role_in_event": "县长",
                "measurable_outcome": "",
                "location": "绥中县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "表态整顿政府系统'宽松软'积弊，推动12345热线办理",
                "role_in_event": "县长",
                "measurable_outcome": "",
                "location": "绥中县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "reform_oriented",
                    "evidence": "当选后表态要'刀刃向内的自我革命'扭转'宽松软'积弊",
                    "confidence": "plausible",
                    "source_ids": ["S001"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "表态聚焦项目建设和产业发展，强调'项目为王'",
                    "confidence": "plausible",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["产业强县", "项目为王", "自我革命", "民生福祉"],
            "management_signals": ["强调制度建设和纪律约束", "重视12345热线诉求办理"],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开渠道未发现单伟的负面信息或纪律处分记录",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "绥中县第十七届人民代表大会第七次会议闭幕",
                "url": "https://www.szx.gov.cn/xwdt/szxw/202607/t20260724_1242724.html",
                "publisher": "绥中县人民政府",
                "published_at": "2026-07-24",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认单伟当选县长及施政表态"
            },
            {
                "id": "S002",
                "title": "绥中县人民政府办公室关于县政府领导同志工作分工的通知",
                "url": "https://www.szx.gov.cn/xxgk_21446/zfxxgk/fdzdgknr/zfwj/szbf/202605/t20260529_1238314.html",
                "publisher": "绥中县人民政府办公室",
                "published_at": "2026-05-28",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认单伟主持县政府全面工作，以及各位副县长分工"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "单伟的出生年月、籍贯、教育背景、任县长前的完整履历均未查到"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "单伟的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "核心领导身份字段缺失",
                "suggested_queries": ["单伟 绥中 县长 简历", "单伟 出生", "单伟 个人简历"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "单伟任代县长前担任什么职务？",
                "why_it_matters": "追踪其晋升路径和来源",
                "suggested_queries": ["单伟 任前公示 葫芦岛", "单伟 绥中 任职"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "单伟何时开始担任代县长？",
                "why_it_matters": "精确任期起点",
                "suggested_queries": ["单伟 代县长 任命 绥中"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # Write person JSON files
    fname1 = f"{today}-辽宁省-葫芦岛市-县委书记-马天峰.json"
    fname2 = f"{today}-辽宁省-葫芦岛市-县长-单伟.json"

    with open(persons_dir / fname1, "w", encoding="utf-8") as f:
        json.dump(matianfeng, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {persons_dir / fname1}")

    with open(persons_dir / fname2, "w", encoding="utf-8") as f:
        json.dump(shanwei, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {persons_dir / fname2}")


if __name__ == "__main__":
    main()
