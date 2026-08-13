#!/usr/bin/env python3
import sqlite3  # noqa — used by gov_relation.runner via import; direct import for process_tmp.py validation
"""Build SQLite database, GEXF graph, and person JSONs for 武功县 (Wugong County), 陕西省咸阳市.

Investigation date: 2026-07-25
Task ID: shaanxi_武功县
Level: 县
Targets: 县委书记 & 县长
Province: 陕西省
Parent city: 咸阳市

Research sources:
  - www.wugong.gov.cn — 武功县人民政府官方网站 (primary, accessed July 2026)
  - 武功县政府网站新闻栏目（县委常委议军会议、全面深化改革委员会会议、军事日活动等）
  - Confidence: current roster confirmed via multiple official news articles (July 2026)

Confidence notes:
  - Current leaders: confirmed via official government website (July 24, 2026 news: 县委常委议军会议)
  - 张延武 (县委书记): name confirmed, detailed bio not available from official site
  - 韩佩 (县委副书记、县长): name confirmed, detailed bio not available
  - 杨博 (县委副书记): name confirmed from 深化改革会议 and 军事日活动
  - Full career histories: NOT available — official site does not provide 领导之窗 section
  - Birth years, education, ethnicity: unverified from current sources
  - Predecessor info: not available from current search results
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Path resolution ──────────────────────────────────────────────────────────
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
SLUG = "武功县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_武功县"
if _CURRENT_DIR.name == "shaanxi_武功县":
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
# IDs: 1-8 县委常委会, 9-11 政府领导, 12-13 人大/政协, 14+ additional

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委常委会 — confirmed from 县委常委议军会议 (2026-07-24) and other articles
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "张延武", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委书记、县人武部党委第一书记", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 2, "name": "韩佩", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "武功县人民政府",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 3, "name": "杨博", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委副书记", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260717_2102074.html"
    },
    {
        "id": 4, "name": "沈靓", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 5, "name": "罗曦", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 6, "name": "乔永锋", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 7, "name": "梁江峰", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 8, "name": "亢鹏刚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 9, "name": "王刚", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县委常委", "current_org": "中共武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260720_2102649.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政府领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10, "name": "李亚鑫", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副县长、县公安局局长", "current_org": "武功县人民政府",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11, "name": "朱小团", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "武功县人民代表大会常务委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    {
        "id": 12, "name": "陈卫", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县人大常委会副主任、县总工会主席", "current_org": "武功县人民代表大会常务委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103788.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13, "name": "谢保卫", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "县政协主席", "current_org": "中国人民政治协商会议武功县委员会",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 其他
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14, "name": "朱枰虎", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "武功高新区管委会主任", "current_org": "武功高新技术产业开发区",
        "source": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103788.html"
    },
]

organizations = [
    {"id": 1, "name": "中共武功县委员会", "type": "党委", "level": "县处级", "parent": "中共咸阳市委员会",
     "location": "陕西省咸阳市武功县"},
    {"id": 2, "name": "武功县人民政府", "type": "政府", "level": "县处级", "parent": "咸阳市人民政府",
     "location": "陕西省咸阳市武功县"},
    {"id": 3, "name": "武功县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "咸阳市人大常委会",
     "location": "陕西省咸阳市武功县"},
    {"id": 4, "name": "中国人民政治协商会议武功县委员会", "type": "政协", "level": "县处级", "parent": "咸阳市政协",
     "location": "陕西省咸阳市武功县"},
    {"id": 5, "name": "武功县公安局", "type": "政府", "level": "乡科级", "parent": "武功县人民政府",
     "location": "陕西省咸阳市武功县"},
    {"id": 6, "name": "武功高新技术产业开发区", "type": "开发区", "level": "县处级", "parent": "武功县人民政府",
     "location": "陕西省咸阳市武功县"},
]

positions = [
    # ── 张延武 ──
    {"person_id": 1, "org_id": 1, "title": "县委书记、县人武部党委第一书记", "start": "", "end": "present",
     "rank": "正县级", "note": "2026年7月在职，来源：县委常委议军会议报道"},

    # ── 韩佩 ──
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "", "end": "present",
     "rank": "正县级", "note": "2026年7月在职"},

    # ── 杨博 ──
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副县级", "note": "2026年7月在职"},

    # ── 沈靓 ──
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # ── 罗曦 ──
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # ── 乔永锋 ──
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # ── 梁江峰 ──
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # ── 亢鹏刚 ──
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": ""},

    # ── 王刚 ──
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副县级", "note": "根据县委全面深化改革委员会第三十次会议报道确认"},

    # ── 李亚鑫 ──
    {"person_id": 10, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present",
     "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "县公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": ""},

    # ── 朱小团 ──
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present",
     "rank": "正县级", "note": ""},

    # ── 陈卫 ──
    {"person_id": 12, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present",
     "rank": "副县级", "note": "兼县总工会主席"},

    # ── 谢保卫 ──
    {"person_id": 13, "org_id": 4, "title": "县政协主席", "start": "", "end": "present",
     "rank": "正县级", "note": ""},

    # ── 朱枰虎 ──
    {"person_id": 14, "org_id": 6, "title": "武功高新区管委会主任", "start": "", "end": "present",
     "rank": "正县级或副县级", "note": ""},
]

relationships = [
    # ── 党政一把手 ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "张延武作为县委书记，韩佩作为县长，是党政一把手搭档关系",
     "overlap_org": "中共武功县委员会/武功县人民政府",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    # ── 县委班子内部 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "张延武与杨博在武功县委班子共事（书记与副书记）",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "韩佩与杨博在武功县委班子共事（县长与副书记）",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "张延武与沈靓在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "张延武与罗曦在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "张延武与乔永锋在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "张延武与梁江峰在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "张延武与亢鹏刚在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "张延武与王刚在武功县委常委班子共事",
     "overlap_org": "中共武功县委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    # ── 人大/政协与县委 ──
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "张延武（县委书记）与朱小团（县人大常委会主任）在武功县党政班子共事",
     "overlap_org": "武功县",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "韩佩（县长）与朱小团（县人大常委会主任）在武功县共事",
     "overlap_org": "武功县",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "张延武（县委书记）与谢保卫（县政协主席）在武功县党政班子共事",
     "overlap_org": "武功县",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    # ── 政府内部 ──
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "韩佩（县长）与李亚鑫（副县长兼公安局长）在县政府班子共事",
     "overlap_org": "武功县人民政府",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "张延武（县委书记）与李亚鑫（副县长兼公安局长）共事",
     "overlap_org": "武功县",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    # ── 高新区 ──
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "张延武（县委书记）与朱枰虎（高新区管委会主任）共事",
     "overlap_org": "武功高新技术产业开发区",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},

    # ── 人大内部 ──
    {"person_a": 11, "person_b": 12, "type": "overlap",
     "context": "朱小团（县人大常委会主任）与陈卫（县人大常委会副主任）在人大共事",
     "overlap_org": "武功县人民代表大会常务委员会",
     "overlap_period": "截至2026年7月", "confidence": "confirmed"},
]

# ── Person JSON for core figures ─────────────────────────────────────────────
PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "陕西省",
        "city": "咸阳市",
        "region": "武功县",
        "job": "",
        "task_id": "shaanxi_武功县",
        "time_focus": "2026年7月"
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
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "",
            "name_birthplace": "",
            "official_profile_url": ""
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
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "",
            "title": "",
            "level": "",
            "location": "陕西省咸阳市武功县",
            "system": "party|government",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到完整履历",
            "confidence": "unverified",
            "source_ids": ["S001"]
        }
    ],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "截至2026年7月，公开渠道未发现违纪违法或负面报道",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": ["S001"]
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "武功县人民政府 - 县委常委议军会议",
            "url": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260724_2103789.html",
            "publisher": "武功县融媒体中心",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认当前领导班子名单"
        },
        {
            "id": "S002",
            "title": "武功县人民政府 - 县委全面深化改革委员会第三十次会议",
            "url": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260720_2102649.html",
            "publisher": "武功县融媒体中心",
            "published_at": "2026-07-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认杨博为县委副书记"
        },
        {
            "id": "S003",
            "title": "武功县人民政府 - 我县开展军事日活动",
            "url": "https://www.wugong.gov.cn/xw/zwyw/202607/t20260717_2102074.html",
            "publisher": "武功县融媒体中心",
            "published_at": "2026-07-17",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认全体县级领导名单"
        }
    ],
    "confidence_summary": {
        "identity": "unverified",
        "current_role": "confirmed",
        "career_completeness": "thin",
        "relationship_confidence": "high",
        "biggest_gap": "所有核心人物的出生年月、教育背景、完整履历均未找到"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "张延武的完整履历（包括出生年月、籍贯、教育背景、此前任职经历）",
            "why_it_matters": "县委书记是本研究的核心目标人物，缺乏基本身份信息",
            "suggested_queries": ["张延武 简历", "张延武 任前公示", "张延武 陕西"],
            "last_attempted": AS_OF
        },
        {
            "priority": "critical",
            "question": "韩佩的完整履历（包括出生年月、籍贯、教育背景、此前任职经历）",
            "why_it_matters": "县长是本研究的核心目标人物",
            "suggested_queries": ["韩佩 武功县 简历", "韩佩 任前公示"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "武功县前任县委书记和县长的去向",
            "why_it_matters": "前任去向可揭示人事流动模式和晋升路径",
            "suggested_queries": ["武功县 前任县委书记", "武功县 前任县长"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "县委常委的具体分工（谁负责组织、纪检、政法、宣传等）",
            "why_it_matters": "分工信息可增强关系网络分析",
            "suggested_queries": ["武功县 领导分工", "武功县委 常委分工"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "县级领导（朱小团、谢保卫、陈卫等）的履历背景",
            "why_it_matters": "丰富人大/政协领导的背景对网络完整性有帮助",
            "suggested_queries": ["朱小团 武功县 简历", "谢保卫 武功县 简历"],
            "last_attempted": AS_OF
        }
    ]
}


def build_person_json(person: dict) -> None:
    """Generate and write a person JSON file for the given person dict."""
    import copy
    pj = copy.deepcopy(PERSON_JSON_TEMPLATE)
    name = person["name"]
    role_short = person["current_post"].replace("、", "_").replace("，", "_").replace(" ", "_")

    pj["investigation_scope"]["job"] = person["current_post"]
    pj["identity"]["person_id"] = f"wugong_{name}"
    pj["identity"]["name"] = name
    pj["identity"]["gender"] = person.get("gender", "")
    pj["identity"]["ethnicity"] = person.get("ethnicity", "")
    pj["identity"]["birth"] = person.get("birth", "")
    pj["identity"]["birthplace"] = person.get("birthplace", "")
    pj["identity"]["education"] = [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                                     "study_type": "unknown", "source_ids": []}] if person.get("education") else []
    pj["identity"]["party_join"] = person.get("party_join", "")
    pj["identity"]["work_start"] = person.get("work_start", "")
    pj["current_status"]["current_post"] = person["current_post"]
    pj["current_status"]["current_org"] = person["current_org"]
    pj["current_status"]["administrative_rank"] = "正县级" if "书记" in person["current_post"] and "副" not in person["current_post"] else "副县级"

    if person["current_post"].find("县委书记") >= 0 or person["current_post"].find("县长") >= 0:
        pj["career_timeline"][0]["level"] = "正县级"
    else:
        pj["career_timeline"][0]["level"] = "副县级"
    pj["career_timeline"][0]["title"] = person["current_post"]
    pj["career_timeline"][0]["org"] = person["current_org"]

    # Relationships for top leaders
    if person["id"] in [1, 2]:
        for r in relationships:
            rel_person = None
            if r["person_a"] == person["id"]:
                rel_person = next((p for p in persons if p["id"] == r["person_b"]), None)
            elif r["person_b"] == person["id"]:
                rel_person = next((p for p in persons if p["id"] == r["person_a"]), None)
            if rel_person:
                pj["relationships"].append({
                    "person": rel_person["name"],
                    "person_id": f"wugong_{rel_person['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": r["confidence"],
                    "source_ids": ["S001"]
                })

    filename = f"{TODAY}-陕西省-咸阳市-{role_short}-{name}.json"
    filepath = PJSON_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(pj, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {filepath}")


# ── BUILD ────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network...")

    # Build DB + GEXF
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

    # Build person JSONs for core figures (县委书记 张延武, 县长 韩佩)
    for p in persons:
        if p["id"] in [1, 2]:  # Only top 2 leaders
            build_person_json(p)

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: 2 (张延武, 韩佩)")


if __name__ == "__main__":
    main()
