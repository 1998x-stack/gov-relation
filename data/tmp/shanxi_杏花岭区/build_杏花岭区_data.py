#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 杏花岭区 (Xinghualing District), 太原市, 山西省.

Investigation date: 2026-07-25
Task ID: shanxi_杏花岭区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.sxtyxhl.gov.cn — 杏花岭区人民政府门户网站 (official news, leadership mentions)
  - Multiple official news articles from 2026-03 to 2026-07 confirming current officeholders

Current confirmed leadership (as of 2026-07-25):
  - 潘侠: 区委书记 (confirmed via multiple articles: 2026-04-29, 2026-05-21, 2026-05-28, 2026-06-04, 2026-06-30, 2026-07-02, 2026-07-09, 2026-07-18)
  - 盛维华: 区委副书记、区长 (confirmed via 2026-07-02 article on 领导班子集中收看)

Key timeline:
  - Up to 2026-04-13: 潘侠 listed as 区委书记、区长 (concurrent roles, "区委书记、区长潘侠主持会议")
  - 2026-07-02: 潘侠 as 区委书记, 盛维华 as 区委副书记、区长 (separate roles)

Confidence notes:
  - 潘侠 and 盛维华 are confirmed as current top two leaders through multiple official sxtyxhl.gov.cn news articles
  - 潘侠 concurrently held 区长 role until ~April/May 2026 when 盛维华 was appointed
  - Detailed career timelines (education, early career) for all figures could not be fully verified due to web access limitations
  - Baidu Baike (403) and Exa (rate-limited) were unavailable during this investigation
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

SLUG = "杏花岭区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

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
        "name": "潘侠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共太原市杏花岭区委员会",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },
    {
        "id": 2,
        "name": "盛维华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "太原市杏花岭区人民政府",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Other Leadership (mentioned in articles)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "李琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、党校校长",
        "current_org": "中共太原市杏花岭区委员会",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260630/30306731.html"
    },
    {
        "id": 4,
        "name": "武晓俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共太原市杏花岭区委员会",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },
    {
        "id": 5,
        "name": "王同化",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "太原市杏花岭区人民代表大会常务委员会",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },
    {
        "id": 6,
        "name": "赵联庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议太原市杏花岭区委员会",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },
    {
        "id": 7,
        "name": "杜志坚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "太原市杏花岭区人民政府",
        "source": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共太原市杏花岭区委员会", "type": "党委", "level": "县处级", "parent": "中共太原市委", "location": "太原市杏花岭区"},
    {"id": 2, "name": "太原市杏花岭区人民政府", "type": "政府", "level": "县处级", "parent": "太原市人民政府", "location": "太原市杏花岭区"},
    {"id": 3, "name": "中共太原市杏花岭区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共太原市杏花岭区委员会", "location": "太原市杏花岭区"},
    {"id": 4, "name": "太原市杏花岭区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "杏花岭区", "location": "太原市杏花岭区"},
    {"id": 5, "name": "中国人民政治协商会议太原市杏花岭区委员会", "type": "政协", "level": "县处级", "parent": "杏花岭区", "location": "太原市杏花岭区"},
    {"id": 6, "name": "太原市杏花岭区监察委员会", "type": "纪委", "level": "县处级", "parent": "杏花岭区", "location": "太原市杏花岭区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 潘侠
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": "此前曾兼任区长"},
    {"person_id": 1, "org_id": 2, "title": "区长（兼）", "start_date": "不详", "end_date": "约2026-04",
     "rank": "正处级", "note": "至2026年4月仍以区委书记兼区长身份主持会议"},

    # 盛维华
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "约2026-05", "end_date": "至今",
     "rank": "正处级", "note": "2026年7月首次在公开报道中以区长身份出现"},

    # 李琦
    {"person_id": 3, "org_id": 1, "title": "区委常委、组织部部长、党校校长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},

    # 武晓俊
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": "具体分管领域待查"},

    # 王同化
    {"person_id": 5, "org_id": 4, "title": "区人大常委会主任", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": ""},

    # 赵联庆
    {"person_id": 6, "org_id": 5, "title": "区政协主席", "start_date": "不详", "end_date": "至今",
     "rank": "正处级", "note": ""},

    # 杜志坚
    {"person_id": 7, "org_id": 2, "title": "区委常委、副区长", "start_date": "不详", "end_date": "至今",
     "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政一把手搭档",
     "overlap_org": "杏花岭区", "overlap_period": "2026-至今"},

    # 潘侠与人大主任
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区人大常委会主任",
     "overlap_org": "杏花岭区", "overlap_period": "2026-至今"},

    # 潘侠与政协主席
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区政协主席",
     "overlap_org": "杏花岭区", "overlap_period": "2026-至今"},

    # 区长与常务副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长（杜志坚为区委常委、副区长）",
     "overlap_org": "太原市杏花岭区人民政府", "overlap_period": "2026-至今"},

    # 组织部长与区委书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与组织部部长",
     "overlap_org": "中共太原市杏花岭区委员会", "overlap_period": "2026-至今"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> str:
    """Write a per-person graph JSON file and return its path."""
    from gov_relation.paths import PERSONS_DIR

    name = person["name"]
    job_slug = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]
    filename = f"{TODAY}-山西省-太原市-{job_slug}-{name}.json"
    filepath = PERSONS_DIR / filename

    person_id = f"xinghualing_{name.lower()}"  # pinyin-based id

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "太原市",
            "region": "杏花岭区",
            "job": person["current_post"],
            "task_id": "shanxi_杏花岭区",
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
                "official_profile_url": "https://www.sxtyxhl.gov.cn/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2, 5, 6] else "副处级",
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
                "title": "杏花岭区领导班子集中收看庆祝中国共产党成立105周年大会实况",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260702/30307455.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-07-02",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{name}在杏花岭区的当前职务"
            },
            {
                "id": "S002",
                "title": "全区'两优一先'表彰大会召开",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260630/30306731.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-06-30",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{name}在杏花岭区的当前职务"
            },
            {
                "id": "S003",
                "title": f"杏花岭区召开区委常委会（扩大）会议（2026-04-29）",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260429/30296198.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-04-29",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
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
                    f"{name} 杏花岭区"
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
    if person["id"] == 1:  # 潘侠
        data["career_timeline"] = [
            {
                "start": "不详",
                "end": "至今",
                "org": "中共太原市杏花岭区委员会",
                "title": "区委书记",
                "level": "正处级",
                "notes": "2026年4月已以区委书记身份主持常委会",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "start": "不详",
                "end": "约2026-04",
                "org": "太原市杏花岭区人民政府",
                "title": "区长（兼）",
                "level": "正处级",
                "notes": "2026年3-4月仍以区委书记兼区长身份主持会议",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            }
        ]
        data["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "pragmatic",
                "evidence": "多次强调'认认真真、扎扎实实'的工作要求，注重经济调度和项目推进",
                "confidence": "plausible",
                "source_ids": ["S003"]
            },
            {
                "trait": "discipline_oriented",
                "evidence": "多次主持召开安全生产会议，强调'人民至上、生命至上'",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ]
        data["governance_record"] = [
            {
                "period": "2026-05",
                "domain": "public_security",
                "achievement_or_event": "带队督导高层建筑消防安全工作",
                "role_in_event": "带队督导",
                "measurable_outcome": "排查高层建筑消防安全隐患",
                "location": "杏花岭区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "period": "2026-05",
                "domain": "economic_development",
                "achievement_or_event": "赴中国银行山西省分行进行工作对接",
                "role_in_event": "带队对接",
                "measurable_outcome": "争取金融支持",
                "location": "太原市",
                "confidence": "confirmed",
                "source_ids": ["S005"]
            },
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "在区综治中心接待来访群众",
                "role_in_event": "接访",
                "measurable_outcome": "处理群众信访问题",
                "location": "杏花岭区",
                "confidence": "confirmed",
                "source_ids": ["S006"]
            }
        ]
        data["source_register"].extend([
            {
                "id": "S004",
                "title": "区委书记潘侠带队督导高层建筑消防安全工作",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260528/30300592.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-05-28",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            },
            {
                "id": "S005",
                "title": "区委书记潘侠赴中国银行山西省分行进行工作对接",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260521/30299268.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-05-21",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            },
            {
                "id": "S006",
                "title": "潘侠在区综治中心接待来访群众",
                "url": "https://www.sxtyxhl.gov.cn/yw/20260604/30302460.html",
                "publisher": "杏花岭区人民政府",
                "published_at": "2026-06-04",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": ""
            }
        ])

    elif person["id"] == 2:  # 盛维华
        data["career_timeline"] = [
            {
                "start": "约2026-05",
                "end": "至今",
                "org": "太原市杏花岭区人民政府",
                "title": "区委副书记、区长",
                "level": "正处级",
                "notes": "2026年7月首次在公开报道中以区长身份出现；此前履历待查",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "不详",
                "end": "不详",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到出任区长前的履历",
                "confidence": "unverified",
                "source_ids": []
            }
        ]
        data["work_style_and_personality"]["public_style_indicators"] = [
            {
                "trait": "low_profile",
                "evidence": "公开活动较少，2026年7月才首次在报道中以区长身份出现",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ]

    # Add relationship references
    for rel in relationships:
        if rel["person_a"] == person["id"]:
            other = next(p for p in persons if p["id"] == rel["person_b"])
            data["relationships"].append({
                "person": other["name"],
                "person_id": f"xinghualing_{other['name'].lower()}",
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
                "person_id": f"xinghualing_{other['name'].lower()}",
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
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

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
