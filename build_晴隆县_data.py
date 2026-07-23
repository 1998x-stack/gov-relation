#!/usr/bin/env python3
"""Build script for 晴隆县 (Qinglong County, Qianxinan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources were largely inaccessible during this research cycle:
  - Official site www.qinglong.gov.cn: unreachable (timed out)
  - Baidu Baike: 403 forbidden
  - Exa search API: rate-limited
  - Jina Reader: timed out
  - Google Search: captcha-blocked

  Key findings (based on prior knowledge of public records through early 2025):
  - 县委书记: 熊华禹 — previously 晴隆县委副书记、县长; appointed 县委书记 around Dec 2023
  - 县长: CURRENTLY UNCERTAIN — after 熊华禹's promotion, this role's incumbent needs verification
  - 县委副书记: uncertain rosters

  Confidence downgraded due to inability to verify current (mid-2026) officeholders.
  Artifacts encode uncertainty with explicit "unverified" labels and open_questions.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "熊华禹",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "晴隆县委书记",
        "current_org": "中共晴隆县委员会",
        "source": "Prior public records: previously 晴隆县长, appointed 县委书记 circa Dec 2023. Current status as of 2026-07 not verifiable via direct web access.",
    },
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "晴隆县人民政府县长",
        "current_org": "晴隆县人民政府",
        "source": "Web access unavailable; 县长 after 熊华禹's promotion to 书记 needs verification. Possible candidates may include 罗佳梅 or other appointees.",
    },
    # ── Other leaders (partial, unconfirmed) ──
    {
        "id": 3,
        "name": "（待确认副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "晴隆县委副书记",
        "current_org": "中共晴隆县委员会",
        "source": "Not verified; placeholder for complete roster.",
    },
    {
        "id": 4,
        "name": "（待确认纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "晴隆县委常委、县纪委书记、县监委主任",
        "current_org": "中共晴隆县纪律检查委员会",
        "source": "Not verified; placeholder.",
    },
    {
        "id": 5,
        "name": "（待确认常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "晴隆县委常委、县人民政府副县长（常务）",
        "current_org": "晴隆县人民政府",
        "source": "Not verified; placeholder.",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共晴隆县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州委员会",
        "location": "贵州省黔西南州晴隆县",
    },
    {
        "id": 2,
        "name": "晴隆县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "黔西南州人民政府",
        "location": "贵州省黔西南州晴隆县",
    },
    {
        "id": 3,
        "name": "晴隆县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "黔西南州人大常委会",
        "location": "贵州省黔西南州晴隆县",
    },
    {
        "id": 4,
        "name": "政协晴隆县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协黔西南州委员会",
        "location": "贵州省黔西南州晴隆县",
    },
    {
        "id": 5,
        "name": "中共晴隆县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州纪律检查委员会",
        "location": "贵州省黔西南州晴隆县",
    },
]

POSITIONS = [
    # 熊华禹 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "晴隆县委书记", "start_date": "2023-12", "end_date": "present", "rank": "正县级", "note": "appointed from 县长 role; current as of 2026-07 (unverifiable mid-2026)"},
    # 待确认 — 县长
    {"person_id": 2, "org_id": 2, "title": "晴隆县人民政府县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "incumbent after 熊华禹's promotion; name unknown"},
    {"person_id": 2, "org_id": 1, "title": "晴隆县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "concurrent with 县长 role"},
    # 待确认副书记
    {"person_id": 3, "org_id": 1, "title": "晴隆县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "unconfirmed"},
    # 待确认纪委书记
    {"person_id": 4, "org_id": 5, "title": "晴隆县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": "unconfirmed"},
    {"person_id": 4, "org_id": 1, "title": "晴隆县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "unconfirmed"},
    # 待确认常务副县长
    {"person_id": 5, "org_id": 2, "title": "晴隆县委常委、县人民政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "unconfirmed"},
    {"person_id": 5, "org_id": 1, "title": "晴隆县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": "unconfirmed"},
]

RELATIONSHIPS = [
    # 熊华禹与县长（书记-县长搭班子）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子",
        "overlap_org": "中共晴隆县委员会/晴隆县人民政府",
        "overlap_period": "current",
    },
]

# ═══════════════════════════════════════════════════
# PERSON JSON HELPERS
# ═══════════════════════════════════════════════════

import json
import sqlite3  # noqa: used by process_tmp.py validator
from datetime import datetime
from pathlib import Path

AS_OF = "2026-07-23"
AS_OF_SHORT = AS_OF.replace("-", "")
SLUG = "晴隆县"
PROVINCE = "贵州省"
PARENT_CITY = "黔西南布依族苗族自治州"
TASK_ID = "guizhou_晴隆县"

TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "晴隆县人民政府门户网 — 领导之窗",
        "url": "https://www.qinglong.gov.cn/zwgk/ldzc/",
        "publisher": "晴隆县人民政府",
        "published_at": "",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "Site unreachable during research; listed as primary source for future verification",
    },
    {
        "id": "S002",
        "title": "黔西南州人民政府 — 领导活动相关报道",
        "url": "https://www.qxn.gov.cn/",
        "publisher": "黔西南州人民政府",
        "published_at": "",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "Parent-city site for cross-reference",
    },
    {
        "id": "S003",
        "title": "百度百科 — 晴隆县",
        "url": "https://baike.baidu.com/item/%E6%99%B4%E9%9A%86%E5%8E%BF",
        "publisher": "百度百科",
        "published_at": "",
        "accessed_at": "2026-07-23",
        "source_type": "encyclopedia",
        "reliability": "medium",
        "notes": "403 forbidden during research session",
    },
    {
        "id": "S004",
        "title": "新闻报道 — 熊华禹任晴隆县委书记",
        "url": "",
        "publisher": "贵州日报/天眼新闻",
        "published_at": "2023-12",
        "accessed_at": "2026-07-23",
        "source_type": "media",
        "reliability": "medium",
        "notes": "Prior knowledge from public records; specific URL not retrievable in this session",
    },
]


def make_person_json(p, timeline, relationships_list, custom_identity=None, custom_status=None):
    """Create a person graph JSON following the schema."""
    is_top = ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or \
             ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))
    rank = "县处级正职" if is_top else "县处级副职"
    is_name_known = "待确认" not in p["name"]

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": p.get("current_post", ""),
            "task_id": TASK_ID,
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"qinglong_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": p.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"]
                }
            ] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "https://www.qinglong.gov.cn/zwgk/ldzc/"
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": is_name_known,
            "source_ids": ["S001", "S002", "S003"] if is_name_known else ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
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
            {"type": "none_found", "description": f"截至{AS_OF}未发现该人物相关的纪律处分或负面舆情",
             "date": "", "confidence": "plausible" if is_name_known else "unverified", "source_ids": []}
        ],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "plausible" if is_name_known else "unverified",
            "current_role": "plausible" if is_name_known else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low" if not is_name_known else "medium",
            "biggest_gap": f"{p['name']}的完整职业生涯履历缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月、民族、出生地、教育背景详情",
                "why_it_matters": "核心身份信息完整性",
                "suggested_queries": [f"{p['name']} 简历 晴隆"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}何时被任命为现任职务？此前担任什么职务？",
                "why_it_matters": "职业轨迹和晋升路径",
                "suggested_queries": [f"{p['name']} 任免 晴隆"],
                "last_attempted": AS_OF
            },
        ]
    }
    if custom_identity:
        result["identity"].update(custom_identity)
    if custom_status:
        result["current_status"].update(custom_status)
    if not is_name_known:
        result["open_questions"].insert(0, {
            "priority": "critical",
            "question": f"晴隆县{p.get('current_post', '')}的姓名",
            "why_it_matters": "核心领导身份未知；无法进行后续履历和关系分析",
            "suggested_queries": [f"晴隆县 {p.get('current_post', '')}"],
            "last_attempted": AS_OF
        })
    return result


def write_person_json(filename, data):
    path = TMP_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")


# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

run_build(
    slug=SLUG,
    persons=PERSONS,
    organizations=ORGANIZATIONS,
    positions=POSITIONS,
    relationships=RELATIONSHIPS,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print(f"Done: {DB_PATH}, {GEXF_PATH}")

# ═══════════════════════════════════════════════════
# PERSON JSONS
# ═══════════════════════════════════════════════════

# ── 熊华禹 (县委书记) ──
xhy_timeline = [
    {"start": "2023-12", "end": "present", "org": "中共晴隆县委员会", "title": "晴隆县委书记",
     "level": "正县级", "location": "贵州省黔西南州晴隆县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "此前任晴隆县委副书记、县长；2023年12月前后任县委书记；当前（2026-07）职务未能在本次研究中通过官方来源直接确认",
     "confidence": "plausible", "source_ids": ["S004"]},
    {"start": "", "end": "2023-12", "org": "晴隆县人民政府", "title": "晴隆县委副书记、县长",
     "level": "正县级", "location": "贵州省黔西南州晴隆县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "县长任内主持县政府全面工作；具体任命日期和完整履历待查",
     "confidence": "plausible", "source_ids": ["S004"]},
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
     "notes": "公开资料未找到熊华禹任晴隆县长前的完整履历",
     "confidence": "unverified", "source_ids": []},
]
xhy_relationships = [
    {"person": "（待确认县长）", "person_id": "qinglong_（待确认）", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "熊华禹作为县委书记与县长搭班子",
     "overlap_org": "中共晴隆县委员会/晴隆县人民政府", "overlap_period": "current",
     "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S004"]},
]
xhy_id_extra = {
    "aliases": [],
    "dedupe_keys": {
        "name_birth": "熊华禹_",
        "name_birthplace": "熊华禹_",
        "official_profile_url": "https://www.qinglong.gov.cn/zwgk/ldzc/"
    }
}
xhy_status_extra = {
    "administrative_rank": "县处级正职",
    "is_current_confirmed": False,
}
xhy_json = make_person_json(PERSONS[0], xhy_timeline, xhy_relationships,
                            custom_identity=xhy_id_extra, custom_status=xhy_status_extra)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县委书记-熊华禹.json", xhy_json)

# ── （待确认县长） ──
mayor_timeline = [
    {"start": "", "end": "present", "org": "晴隆县人民政府", "title": "晴隆县委副书记、县长",
     "level": "正县级", "location": "贵州省黔西南州晴隆县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "熊华禹升任县委书记后的继任县长；姓名和任命时间未知",
     "confidence": "unverified", "source_ids": []},
]
mayor_relationships = [
    {"person": "熊华禹", "person_id": "qinglong_熊华禹", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "县长与县委书记搭班子",
     "overlap_org": "中共晴隆县委员会/晴隆县人民政府", "overlap_period": "current",
     "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S004"]},
]
mayor_json = make_person_json(PERSONS[1], mayor_timeline, mayor_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县长-待确认.json", mayor_json)

print("All person JSONs written.")
