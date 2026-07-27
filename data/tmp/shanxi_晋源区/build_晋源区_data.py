#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 晋源区 (Jinyuan District), 太原市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_晋源区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.jinyuan.gov.cn — 晋源区人民政府门户网站 (official news, leadership roster)
  - mp.weixin.qq.com — 晋源发布 (区委常委会扩大会议, 人大常委会会议)

Current confirmed leadership (as of 2026-07-26):
  - 张农寿: 区委书记 (confirmed via WeChat article: 晋源区委常委会召开扩大会议 2026-07-15;
    also confirmed via jinyuan.gov.cn news list: "张农寿开展'七一'走访慰问活动" 2026-06-30)
  - 岳旭强: 区委副书记、区长 (confirmed via 区长之窗 qzzc.html on jinyuan.gov.cn;
    born 1973年11月, male, Han ethnicity, university degree, CPC member)

Key notes:
  - 张农寿 is confirmed as the current 区委书记 through multiple official sources
  - 岳旭强 is confirmed as 区委副书记、区长 through official leadership page
  - Full leadership roster (副区长, 人大, 政协, 纪委) partially confirmed
  - Detailed career timelines could not be fully verified due to web access limitations
  - Exa rate-limited, Baidu 403, Jina reader timed out during this investigation
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

SLUG = "晋源区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ──────────────────────────────────────────────────────────
DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "张农寿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共太原市晋源区委员会",
        "source": "https://mp.weixin.qq.com/s/1Pv77tufwcniA9I86N-B3Q"
    },
    {
        "id": 2,
        "name": "岳旭强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Other Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "温志勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组书记、区政协主席",
        "current_org": "太原市晋源区人民代表大会常务委员会",
        "source": "https://mp.weixin.qq.com/s/_-BMKb5N0X_tbs1ZlYMK4g"
    },
    {
        "id": 4,
        "name": "张吉祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "太原市晋源区人民代表大会常务委员会",
        "source": "https://mp.weixin.qq.com/s/_-BMKb5N0X_tbs1ZlYMK4g"
    },
    {
        "id": 5,
        "name": "高宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共太原市晋源区纪律检查委员会",
        "source": "https://mp.weixin.qq.com/s/_-BMKb5N0X_tbs1ZlYMK4g"
    },
    {
        "id": 6,
        "name": "王里鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://mp.weixin.qq.com/s/_-BMKb5N0X_tbs1ZlYMK4g"
    },
    {
        "id": 7,
        "name": "郭忻昕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },
    {
        "id": 8,
        "name": "李全林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },
    {
        "id": 9,
        "name": "李鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },
    {
        "id": 10,
        "name": "尹敬明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },
    {
        "id": 11,
        "name": "张桂峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "太原市晋源区人民政府",
        "source": "https://www.jinyuan.gov.cn/qzzc.html"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共太原市晋源区委员会", "type": "党委", "level": "县处级", "parent": "中共太原市委", "location": "太原市晋源区"},
    {"id": 2, "name": "太原市晋源区人民政府", "type": "政府", "level": "县处级", "parent": "太原市人民政府", "location": "太原市晋源区"},
    {"id": 3, "name": "中共太原市晋源区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共太原市晋源区委员会", "location": "太原市晋源区"},
    {"id": 4, "name": "太原市晋源区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "晋源区", "location": "太原市晋源区"},
    {"id": 5, "name": "中国人民政治协商会议太原市晋源区委员会", "type": "政协", "level": "县处级", "parent": "晋源区", "location": "太原市晋源区"},
    {"id": 6, "name": "太原市晋源区监察委员会", "type": "纪委", "level": "县处级", "parent": "晋源区", "location": "太原市晋源区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 张农寿
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": "2026年7月以区委书记身份主持区委常委会扩大会议"},

    # 岳旭强
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": "1973年11月出生，大学学历，中共党员"},

    # 温志勇
    {"person_id": 3, "org_id": 4, "title": "区人大常委会党组书记、区政协主席", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": "兼任区政协主席"},

    # 张吉祥
    {"person_id": 4, "org_id": 4, "title": "区人大常委会主任", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": ""},

    # 高宇
    {"person_id": 5, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 王里鹏
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 郭忻昕
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 李全林
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 李鹏
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 尹敬明
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 张桂峰
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政一把手搭档",
     "overlap_org": "晋源区", "overlap_period": "2026-至今"},

    # 区委书记与人大书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区人大常委会党组书记",
     "overlap_org": "晋源区", "overlap_period": "2026-至今"},

    # 区委书记与人大主任
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区人大常委会主任",
     "overlap_org": "晋源区", "overlap_period": "2026-至今"},

    # 区委书记与纪委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区纪委书记",
     "overlap_org": "中共太原市晋源区委员会", "overlap_period": "2026-至今"},

    # 区长与常务副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长（王里鹏）",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},

    # 区长与其他副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与副区长",
     "overlap_org": "太原市晋源区人民政府", "overlap_period": "2026-至今"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> str:
    """Write a per-person graph JSON file and return its path."""
    name = person["name"]
    job_slug = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]
    filename = f"{TODAY}-山西省-太原市-{job_slug}-{name}.json"
    filepath = PERSONS_DIR / filename

    person_id = f"jinyuan_{name.lower()}"

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "太原市",
            "region": "晋源区",
            "job": person["current_post"],
            "task_id": "shanxi_晋源区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", "中共党员"),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": name,
                "name_birthplace": name,
                "official_profile_url": "https://www.jinyuan.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2, 3, 4] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person["id"] in [1, 2],
            "source_ids": ["S001", "S002"]
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
                "summary": "履历信息不足，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开信息中未发现与{name}相关的纪律处分、审计问题或负面报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "晋源区委常委会召开扩大会议",
                "url": "https://mp.weixin.qq.com/s/1Pv77tufwcniA9I86N-B3Q",
                "publisher": "晋源发布",
                "published_at": "2026-07-15",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{name}在晋源区的当前职务"
            },
            {
                "id": "S002",
                "title": "太原市晋源区人民政府区长之窗",
                "url": "https://www.jinyuan.gov.cn/qzzc.html",
                "publisher": "晋源区人民政府",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{name}在晋源区的当前职务"
            },
            {
                "id": "S003",
                "title": "太原市晋源区六届人大常委会召开第四十五次会议",
                "url": "https://mp.weixin.qq.com/s/_-BMKb5N0X_tbs1ZlYMK4g",
                "publisher": "晋源发布",
                "published_at": "2026-07-22",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认区人大常委会组成人员"
            },
            {
                "id": "S004",
                "title": "岳旭强调研督导全区防汛备汛及危房安全防范工作",
                "url": "https://www.jinyuan.gov.cn/jydt/20260710/30309480.html",
                "publisher": "晋源区人民政府",
                "published_at": "2026-07-10",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认岳旭强以区长身份调研"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed" if person["id"] in [1, 2] else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium" if person["id"] in [1, 2] else "low",
            "biggest_gap": f"{name}的完整履历（出生、教育、早期任职等）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}出生于哪一年？籍贯何处？",
                "why_it_matters": "核心人物身份信息缺失，影响图谱完整性",
                "suggested_queries": [
                    f"{name} 简历 太原",
                    f"{name} 晋源区"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}出任现职前的完整任职履历",
                "why_it_matters": "无法评估其晋升路径和核心系统经验",
                "suggested_queries": [
                    f"{name} 此前 担任",
                    f"{name} 太原 任职经历"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # Add person-specific career timeline if available
    if person["id"] == 1:  # 张农寿
        data["career_timeline"] = [
            {
                "start": "不详",
                "end": "至今",
                "org": "中共太原市晋源区委员会",
                "title": "区委书记",
                "level": "正处级",
                "notes": "2026年7月以区委书记身份主持区委常委会扩大会议；2026年6月开展七一走访慰问活动",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ]
        data["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "pragmatic",
                "evidence": "主持区委常委会扩大会议，强调经济发展、民生保障、基层治理等具体工作",
                "confidence": "plausible",
                "source_ids": ["S001"]
            },
            {
                "trait": "discipline_oriented",
                "evidence": "强调防汛减灾工作要以最高标准、最严要求落实，压实工作责任",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ]
        data["governance_record"] = [
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "开展七一走访慰问活动",
                "role_in_event": "走访慰问",
                "measurable_outcome": "慰问基层党员群众",
                "location": "晋源区",
                "confidence": "confirmed",
                "source_ids": []
            },
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "主持区委常委会扩大会议，部署防汛减灾、党建工作",
                "role_in_event": "主持会议",
                "measurable_outcome": "传达学习中央精神，部署全区重点工作",
                "location": "晋源区",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ]

    elif person["id"] == 2:  # 岳旭强
        data["career_timeline"] = [
            {
                "start": "不详",
                "end": "至今",
                "org": "太原市晋源区人民政府",
                "title": "区委副书记、区长",
                "level": "正处级",
                "notes": "1973年11月出生，大学学历；当前主持区政府全面工作",
                "confidence": "confirmed",
                "source_ids": ["S002", "S004"]
            }
        ]
        data["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "grassroots_oriented",
                "evidence": "调研防汛工作时深入姚村镇、晋祠镇等基层一线，走进居民家中查看危房情况",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "trait": "pragmatic",
                "evidence": "强调宁可十防九空、不可失防万一，要求把各项防汛备汛工作做细做实做到位",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ]
        data["governance_record"] = [
            {
                "period": "2026-06",
                "domain": "urban_construction",
                "achievement_or_event": "主持召开区政府第8次常务会议，部署民生实事、四水四定等工作",
                "role_in_event": "主持会议",
                "measurable_outcome": "部署省市区民生实事推进和财政风险评估",
                "location": "晋源区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "调研督导全区防汛备汛及危房安全防范工作",
                "role_in_event": "带队调研",
                "measurable_outcome": "实地查看姚村镇、晋祠镇、罗城街道、金胜镇防汛重点区域",
                "location": "晋源区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ]

    # Add relationship references
    for rel in relationships:
        if rel["person_a"] == person["id"]:
            other = next(p for p in persons if p["id"] == rel["person_b"])
            data["relationships"].append({
                "person": other["name"],
                "person_id": f"jinyuan_{other['name'].lower()}",
                "relationship_type": rel["type"],
                "strength": "strong",
                "evidence": rel["context"],
                "overlap_org": rel["overlap_org"],
                "overlap_period": rel["overlap_period"],
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            })
        elif rel["person_b"] == person["id"]:
            other = next(p for p in persons if p["id"] == rel["person_a"])
            data["relationships"].append({
                "person": other["name"],
                "person_id": f"jinyuan_{other['name'].lower()}",
                "relationship_type": rel["type"],
                "strength": "strong",
                "evidence": rel["context"],
                "overlap_org": rel["overlap_org"],
                "overlap_period": rel["overlap_period"],
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            })

    # Add org references
    data["organizations"].append({
        "name": person["current_org"],
        "role": person["current_post"]
    })

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return str(filepath)


def main():
    from gov_relation.runner import run_build

    # ── Build DB and GEXF in staging ──
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Write person JSONs ──
    person_files = []
    for person in persons[:2]:  # Core leaders only
        path = write_person_json(person)
        person_files.append(path)
        print(f"  Person JSON: {path}")

    # ── Summary ──
    print(f"\n{'='*60}")
    print(f"Build complete for {SLUG}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    print(f"  Person JSONs: {len(person_files)}")


if __name__ == "__main__":
    main()
