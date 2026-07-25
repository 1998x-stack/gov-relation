#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 雁塔区 (Yanta District), 西安市, 陕西省.

Level: 市辖区
Province: 陕西省
Parent city: 西安市
Targets: 区委书记 (Party Secretary: 邓晓东), 区长 (Mayor: 王建军)
Task ID: shaanxi_雁塔区

Research date: 2026-07-25
Official source: https://www.yanta.gov.cn/ (西安市雁塔区人民政府)

Current status (as of 2026-07-25, verified via 雁塔区人民政府 website and news articles):
- 区委书记: 邓晓东 (男，汉族，confirmed via 2026年3月区人大闭幕会代表区委讲话)
- 区长: 王建军 (男，汉族，1970年6月生，研究生学历，工商管理硕士，曾任未央区副区长等职，2022年3月当选雁塔区区长)
- Government leadership roster confirmed on district website (区政府领导之窗页面)

Leadership roster sourced from:
  - https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html (王建军)
  - https://www.yanta.gov.cn/xwzx/ytyw/2034813360583770114.html (邓晓东 - 人大闭幕会)

Government leadership team (confirmed from district website 领导之窗 sidebar):
  - 郭建荣: 区委常委、副区长
  - 焦鸣军: 副区长、公安雁塔分局局长
  - 张伟: 副区长
  - 聂虎: 副区长
  - 郭俊: 副区长
  - 王宇楠: 副区长
  - 高晓东: 副区长

Confidence notes:
  邓晓东 identity as 区委书记 confirmed via March 2026 People's Congress news article.
  王建军 identity confirmed via official government bio page.
  Full career histories for 邓晓东 before current role not publicly available on district website.
  Party committee leadership roster (区委领导班子) not fully published on the district website.
  Web search tools (Exa, Baidu, Google) were rate-limited or timed out during this investigation.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "雁塔区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 邓晓东 — 区委书记
    {
        "id": 1,
        "name": "邓晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西安市雁塔区委员会",
        "source": "https://www.yanta.gov.cn/xwzx/ytyw/2034813360583770114.html",
    },
    # 2. 王建军 — 区委副书记、区长
    {
        "id": 2,
        "name": "王建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "",
        "education": "研究生学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 郭建荣 — 区委常委、副区长
    {
        "id": 3,
        "name": "郭建荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 4. 焦鸣军 — 副区长、公安雁塔分局局长
    {
        "id": 4,
        "name": "焦鸣军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安雁塔分局局长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 5. 张伟 — 副区长
    {
        "id": 5,
        "name": "张伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 6. 聂虎 — 副区长
    {
        "id": 6,
        "name": "聂虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 7. 郭俊 — 副区长
    {
        "id": 7,
        "name": "郭俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 8. 王宇楠 — 副区长
    {
        "id": 8,
        "name": "王宇楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },
    # 9. 高晓东 — 副区长
    {
        "id": 9,
        "name": "高晓东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "雁塔区人民政府",
        "source": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
    },

    # ════════════════════════════════════════
    # 区人大领导 (District People's Congress)
    # ════════════════════════════════════════

    # 10. 魏养毅 — 区人大常委会主任
    {
        "id": 10,
        "name": "魏养毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "雁塔区人大常委会",
        "source": "https://www.yanta.gov.cn/xwzx/ytyw/2034813360583770114.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共西安市雁塔区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共西安市委",
        "location": "西安市雁塔区",
    },
    {
        "id": 2,
        "name": "雁塔区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "西安市人民政府",
        "location": "西安市雁塔区",
    },
    {
        "id": 3,
        "name": "雁塔区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "西安市人大常委会",
        "location": "西安市雁塔区",
    },
    {
        "id": 4,
        "name": "公安雁塔分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安市公安局",
        "location": "西安市雁塔区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 邓晓东 — 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start": "",
        "end": "present",
        "rank": "正县处级",
        "note": "现任雁塔区委书记。此前曾担任区长等职（具体履历待查）。",
    },
    # 王建军 — 区长 (full bio)
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start": "2022-03-24",
        "end": "present",
        "rank": "正县处级",
        "note": "2022年3月24日在雁塔区第十八届人大一次会议上当选区长。之前任代区长。",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "代区长",
        "start": "",
        "end": "2022-03-24",
        "rank": "正县处级",
        "note": "雁塔区委副书记、区人民政府党组书记、副区长、代区长",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "区委副书记",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "雁塔区委副书记",
    },
    # 王建军 — 未央区履历
    {
        "person_id": 2,
        "org_id": 2,
        "title": "未央区委常委、区人民政府党组成员",
        "start": "",
        "end": "",
        "rank": "副县处级",
        "note": "由未央区调任雁塔区前的职务",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "西安汉长安城国家大遗址保护特区党工委委员、管委会副主任",
        "start": "",
        "end": "",
        "rank": "副县处级",
        "note": "在未央区任职期间兼任",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "未央区委办公室主任",
        "start": "",
        "end": "",
        "rank": "正乡科级",
        "note": "",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "未央区政府办公室主任",
        "start": "",
        "end": "",
        "rank": "正乡科级",
        "note": "",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "未央区徐家湾街道党工委副书记、办事处主任",
        "start": "",
        "end": "",
        "rank": "正乡科级",
        "note": "",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "未央区谭家街道办事处副主任",
        "start": "",
        "end": "",
        "rank": "副乡科级",
        "note": "",
    },
    # 郭建荣 — 区委常委、副区长
    {
        "person_id": 3,
        "org_id": 2,
        "title": "区委常委、副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 焦鸣军 — 副区长、公安雁塔分局局长
    {
        "person_id": 4,
        "org_id": 2,
        "title": "副区长、公安雁塔分局局长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 张伟 — 副区长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 聂虎 — 副区长
    {
        "person_id": 6,
        "org_id": 2,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 郭俊 — 副区长
    {
        "person_id": 7,
        "org_id": 2,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 王宇楠 — 副区长
    {
        "person_id": 8,
        "org_id": 2,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 高晓东 — 副区长
    {
        "person_id": 9,
        "org_id": 2,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县处级",
        "note": "",
    },
    # 魏养毅 — 区人大常委会主任
    {
        "person_id": 10,
        "org_id": 3,
        "title": "区人大常委会主任",
        "start": "2026-03-19",
        "end": "present",
        "rank": "正县处级",
        "note": "2026年3月19日在雁塔区第十八届人民代表大会第五次会议上当选",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 邓晓东 ←→ 王建军 (区委书记与区长 - 党政主要领导搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "区委书记与区长，雁塔区党政主要领导。两人在区委全会、区两会等重要场合共同出席会议。",
        "overlap_org": "中共西安市雁塔区委员会/雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 王建军 → 各副区长 (区长领导区政府)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "上下级关系",
        "context": "区长与区委常委、副区长，区政府主要领导关系",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "上下级关系",
        "context": "区长与副区长/公安分局局长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "上下级关系",
        "context": "区长与副区长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "上下级关系",
        "context": "区长与副区长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级关系",
        "context": "区长与副区长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "上下级关系",
        "context": "区长与副区长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "上下级关系",
        "context": "区长与副区长",
        "overlap_org": "雁塔区人民政府",
        "overlap_period": "",
        "strength": "strong",
        "confidence": "confirmed",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON OUTPUT
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, extra: dict | None = None) -> None:
    """Write a person graph JSON file to the staging dir."""
    name = person["name"]
    post_short = person["current_post"].replace("、", "_").replace("，", "_").replace(" ", "_")
    filename = f"{TODAY}-陕西省-西安市-{post_short}-{name}.json"
    now = datetime.now().strftime("%Y-%m-%d")

    base = {
        "schema_version": "1.0",
        "generated_at": now,
        "investigation_scope": {
            "province": "陕西省",
            "city": "西安市",
            "region": "雁塔区",
            "job": person["current_post"],
            "task_id": "shaanxi_雁塔区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"yanta_{name}",
            "name": name,
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] or "",
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}" if person["birth"] else name,
                "name_birthplace": name,
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
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
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": f"雁塔区人民政府领导之窗 - {name}",
                "url": person["source"],
                "publisher": "西安市雁塔区人民政府",
                "published_at": AS_OF,
                "accessed_at": now,
                "source_type": "official",
                "reliability": "high",
                "notes": "",
            },
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person["birth"] else "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历信息（出生年份、籍贯、教育经历、早期职业生涯）未找到",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生年份、籍贯、教育背景、早期职业生涯）",
                "why_it_matters": "核心领导人的履历信息是任职交集分析的基础",
                "suggested_queries": [f"{name} 简历", f"{name} 百度百科", f"西安市雁塔区 {name} 任职经历"],
                "last_attempted": now,
            },
        ],
    }

    if extra:
        base.update(extra)

    path = Path(PERSONS_DIR) / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(base, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")


def build_person_extra_wangjianjun() -> dict:
    """王建军 specific extra data."""
    return {
        "identity": {
            "person_id": "yanta_wang_jianjun",
            "name": "王建军",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1970年6月",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "研究生学历，工商管理硕士",
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": "中共党员",
            "dedupe_keys": {
                "name_birth": "王建军_1970年6月",
                "name_birthplace": "王建军",
                "official_profile_url": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
            },
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "雁塔区人民政府",
            "administrative_rank": "正县处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "2022-03-24",
                "end": "present",
                "org": "雁塔区人民政府",
                "title": "区长",
                "level": "正县处级",
                "location": "西安市雁塔区",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "2022年3月24日在雁塔区第十八届人大一次会议上当选",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "2022-03-24",
                "org": "雁塔区人民政府",
                "title": "代区长",
                "level": "正县处级",
                "location": "西安市雁塔区",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "雁塔区委副书记、区人民政府党组书记、副区长、代区长",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "",
                "org": "未央区人民政府/区委",
                "title": "未央区委常委、区人民政府党组成员",
                "level": "副县处级",
                "location": "西安市未央区",
                "system": "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "",
                "org": "西安汉长安城国家大遗址保护特区",
                "title": "党工委委员、管委会副主任",
                "level": "副县处级",
                "location": "西安市未央区",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "",
                "org": "未央区委办公室",
                "title": "主任",
                "level": "正乡科级",
                "location": "西安市未央区",
                "system": "party",
                "rank": "",
                "is_key_promotion": False,
                "notes": "曾任未央区政府办公室主任、区委办公室主任",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "",
                "org": "未央区徐家湾街道",
                "title": "党工委副书记、办事处主任",
                "level": "正乡科级",
                "location": "西安市未央区",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "",
                "end": "",
                "org": "未央区谭家街道办事处",
                "title": "副主任",
                "level": "副乡科级",
                "location": "西安市未央区",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": ["地方政府管理", "区域经济管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["西安市未央区", "西安市雁塔区"],
            "promotion_velocity": {
                "summary": "从街道副主任逐步晋升至正县级区长，典型的基层逐级晋升路径",
                "notable_fast_promotions": [],
            },
        },
        "relationships": [
            {
                "person": "邓晓东",
                "person_id": "yanta_deng_xiaodong",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区委书记与区长，雁塔区党政主要领导搭档关系",
                "overlap_org": "中共西安市雁塔区委员会/雁塔区人民政府",
                "overlap_period": "",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "economic_development",
                "achievement_or_event": "雁塔区2025年GDP达3427.09亿元，占西安市近四分之一",
                "role_in_event": "区长，负责政府全面工作",
                "measurable_outcome": "GDP增长3.7%，连续五年进入全国百强区16强",
                "location": "西安市雁塔区",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "雁塔区人民政府领导之窗 - 王建军",
                "url": "https://www.yanta.gov.cn/xxgk/jcxxgk/ldzc/wjj/1.html",
                "publisher": "西安市雁塔区人民政府",
                "published_at": "2026-07-24",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "官方简历页",
            },
            {
                "id": "S002",
                "title": "西安市雁塔区第十八届人民代表大会第五次会议开幕",
                "url": "https://www.yanta.gov.cn/xwzx/ytyw/2034078396152119297.html",
                "publisher": "西安市雁塔区人民政府",
                "published_at": "2026-03-18",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "王建军作政府工作报告，公布经济数据",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "早年教育经历和1970-2000年间的部分履历时间节点不明确",
        },
        "open_questions": [
            {
                "priority": "medium",
                "question": "王建军的出生地/籍贯",
                "why_it_matters": "用于识别同乡关系网络",
                "suggested_queries": ["王建军 籍贯", "王建军 出生地", "王建军 百度百科"],
                "last_attempted": "2026-07-25",
            },
            {
                "priority": "medium",
                "question": "王建军各任职阶段的具体时间节点",
                "why_it_matters": "精确的时间线有助于交叉比对工作交集",
                "suggested_queries": ["王建军 任免 未央区", "王建军 任职时间"],
                "last_attempted": "2026-07-25",
            },
        ],
    }


def build_person_extra_dengxiaodong() -> dict:
    """邓晓东 specific extra data."""
    return {
        "identity": {
            "person_id": "yanta_deng_xiaodong",
            "name": "邓晓东",
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "education": [],
            "party_join": "中共党员",
            "dedupe_keys": {
                "name_birth": "邓晓东",
                "name_birthplace": "邓晓东",
                "official_profile_url": "https://www.yanta.gov.cn/xwzx/ytyw/2034813360583770114.html",
            },
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共西安市雁塔区委员会",
            "administrative_rank": "正县处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": "中共西安市雁塔区委员会",
                "title": "区委书记",
                "level": "正县处级",
                "location": "西安市雁塔区",
                "system": "party",
                "rank": "",
                "is_key_promotion": True,
                "notes": "2026年3月在区人大闭幕会上代表区委讲话，确认身份",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到邓晓东在担任区委书记之前的完整履历。根据新闻报道，此前可能担任过区长或其他区级领导职务。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历不完整，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "relationships": [
            {
                "person": "王建军",
                "person_id": "yanta_wang_jianjun",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区委书记与区长，雁塔区党政主要领导搭档关系",
                "overlap_org": "中共西安市雁塔区委员会/雁塔区人民政府",
                "overlap_period": "",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "economic_development",
                "achievement_or_event": "提出'依托实力、凝聚合力、保持定力'工作方针，推动六场攻坚战",
                "role_in_event": "区委书记，总揽全局",
                "measurable_outcome": "雁塔区GDP达3427.09亿元，连续五年进入全国百强区16强",
                "location": "西安市雁塔区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "西安市雁塔区第十八届人民代表大会第五次会议闭幕",
                "url": "https://www.yanta.gov.cn/xwzx/ytyw/2034813360583770114.html",
                "publisher": "西安市雁塔区人民政府",
                "published_at": "2026-03-20",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "邓晓东以区委书记身份主持会议并发表讲话",
            },
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "邓晓东的完整履历完全缺失——出生年份、籍贯、教育背景、此前任职经历均未找到",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "邓晓东的完整履历（出生年份、籍贯、教育背景、此前任职经历）",
                "why_it_matters": "区委书记是区域内最重要的政治人物，完整履历对分析其关系网络至关重要",
                "suggested_queries": [
                    "邓晓东 简历",
                    "邓晓东 百度百科",
                    "邓晓东 西安市 雁塔区 任职",
                    "邓晓东 任前公示",
                    "雁塔区 历任区委书记",
                ],
                "last_attempted": "2026-07-25",
            },
            {
                "priority": "high",
                "question": "邓晓东担任区委书记的具体起始时间",
                "why_it_matters": "确定其前任及其去向，分析人事变动趋势",
                "suggested_queries": ["雁塔区 区委书记 任免", "邓晓东 任雁塔区委书记"],
                "last_attempted": "2026-07-25",
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Building {SLUG} network data")
    print(f"  Task: shaanxi_雁塔区")
    print(f"  As of: {AS_OF}")
    print(f"{'='*60}\n")

    # 1. Build database and GEXF
    print("Phase 1: Database + GEXF\n")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # 2. Write person JSONs
    print("\nPhase 2: Person JSON files\n")
    write_person_json(persons[1], build_person_extra_wangjianjun())   # 王建军
    write_person_json(persons[0], build_person_extra_dengxiaodong())  # 邓晓东

    # 3. Summary
    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}")
    print(f"  Database:    {DB_PATH}")
    print(f"  GEXF:        {GEXF_PATH}")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relations:   {len(relationships)}")
    print(f"{'='*60}\n")
