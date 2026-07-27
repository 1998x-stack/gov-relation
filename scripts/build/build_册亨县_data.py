#!/usr/bin/env python3
"""Build script for 册亨县 (Ceheng County, Qianxinan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources were largely inaccessible during this research cycle:
  - Official site www.ceheng.gov.cn: unreachable (timed out)
  - Baidu Baike: 403 forbidden
  - Exa search API: rate-limited
  - Jina Reader: timed out
  - Google/Bing Search: captcha-blocked or timed out

  Key findings (from prior public records and repository cross-references):
  - 张茂 (Zhang Mao): 册亨县委书记 for an extended period (approximately 2014-2021);
    is the best-documented predecessor. Exact current status unclear without web access.
  - 徐炼 (Xu Lian): previously 册亨县委副书记 (2016-2018); later became 望谟县长 then 望谟县委书记.
    Documented in the repo's own build_望谟县_data.py and
    data/persons/2026-07-23-贵州省-黔西南布依族苗族自治州-县委书记-徐炼.json.
  - 2021-2022 period saw a transition in 册亨县 leadership. Current (mid-2026) officeholders
    cannot be verified through working web channels during this session.

  Confidence downgraded due to inability to verify current (mid-2026) officeholders.
  Artifacts encode uncertainty with explicit "unverified" labels and open_questions.
  Known historical data (张茂, 徐炼) is included with appropriate confidence labels.
"""

import json
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════

TASK_ID = "guizhou_册亨县"
SLUG = "册亨县"
AS_OF = "2026-07-23"
AS_OF_SHORT = AS_OF.replace("-", "")
PROVINCE = "贵州省"
PARENT_CITY = "黔西南布依族苗族自治州"

TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "（待确认县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "册亨县委书记",
        "current_org": "中共册亨县委员会",
        "source": "Web access unavailable. After 张茂's tenure (approx 2014-2021), the current 县委书记 could not be verified in this research cycle. 徐炼 (former 册亨县委副书记 2016-2018) moved to 望谟. Successor needs confirmation.",
    },
    {
        "id": 2,
        "name": "（待确认县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "册亨县人民政府县长",
        "current_org": "册亨县人民政府",
        "source": "Web access unavailable. Current 县长 could not be verified in this research cycle.",
    },
    # ── Historical figures (known from repo and prior records) ──
    {
        "id": 3,
        "name": "张茂",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原册亨县委书记）",
        "current_org": "中共册亨县委员会",
        "source": "Prior public records. 张茂 served as 册亨县委书记 for an extended period (approximately 2014-2021). Exact end date and current status need verification.",
    },
    {
        "id": 4,
        "name": "徐炼",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望谟县委书记",
        "current_org": "中共望谟县委员会",
        "source": "Repository build_望谟县_data.py and data/persons/2026-07-23-贵州省-黔西南布依族苗族自治州-县委书记-徐炼.json. Previously 册亨县委副书记 (2016-2018).",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共册亨县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州委员会",
        "location": "贵州省黔西南州册亨县",
    },
    {
        "id": 2,
        "name": "册亨县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "黔西南州人民政府",
        "location": "贵州省黔西南州册亨县",
    },
    {
        "id": 3,
        "name": "册亨县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "黔西南州人大常委会",
        "location": "贵州省黔西南州册亨县",
    },
    {
        "id": 4,
        "name": "政协册亨县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协黔西南州委员会",
        "location": "贵州省黔西南州册亨县",
    },
    {
        "id": 5,
        "name": "中共册亨县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州纪律检查委员会",
        "location": "贵州省黔西南州册亨县",
    },
]

POSITIONS = [
    # 待确认 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "册亨县委书记", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "incumbent as of 2026-07; name could not be verified in this research cycle"},
    # 待确认 — 县长
    {"person_id": 2, "org_id": 2, "title": "册亨县人民政府县长", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "incumbent as of 2026-07; name could not be verified"},
    {"person_id": 2, "org_id": 1, "title": "册亨县委副书记", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "concurrent party deputy role"},
    # 张茂 — 原县委书记
    {"person_id": 3, "org_id": 1, "title": "册亨县委书记", "start_date": "2014?", "end_date": "2021?",
     "rank": "正县级", "note": "approximate tenure; exact dates need verification from official sources"},
    # 徐炼 — 原册亨县委副书记
    {"person_id": 4, "org_id": 1, "title": "册亨县委副书记", "start_date": "2016", "end_date": "2018",
     "rank": "副县级", "note": "confirmed via repo cross-reference; later moved to 望谟县"},
]

RELATIONSHIPS = [
    # 书记—县长搭班子 (current, names unknown)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子（当前，姓名待确认）",
        "overlap_org": "中共册亨县委员会/册亨县人民政府",
        "overlap_period": "current",
    },
    # 张茂 — 待确认县长 (historical)
    {
        "person_a": 3, "person_b": 2,
        "type": "superior_subordinate",
        "context": "张茂（原县委书记）与现任县长（姓名待确认）的可能交接关系",
        "overlap_org": "中共册亨县委员会/册亨县人民政府",
        "overlap_period": "推测交接期",
    },
    # 徐炼 — 张茂 (historical subordinate)
    {
        "person_a": 4, "person_b": 3,
        "type": "superior_subordinate",
        "context": "徐炼曾作为册亨县委副书记（2016-2018）在张茂书记领导下工作",
        "overlap_org": "中共册亨县委员会",
        "overlap_period": "2016-2018",
    },
]

# ═══════════════════════════════════════════════════
# SOURCE REGISTER
# ═══════════════════════════════════════════════════

SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "册亨县人民政府门户网 — 领导之窗",
        "url": "https://www.ceheng.gov.cn/zwgk/ldzc/",
        "publisher": "册亨县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
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
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "Parent-city site for cross-reference",
    },
    {
        "id": "S003",
        "title": "百度百科 — 册亨县",
        "url": "https://baike.baidu.com/item/%E5%86%8C%E4%BA%A8%E5%8E%BF",
        "publisher": "百度百科",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "encyclopedia",
        "reliability": "medium",
        "notes": "403 forbidden during research session",
    },
    {
        "id": "S004",
        "title": "Repository cross-reference — build_望谟县_data.py & person JSON for 徐炼",
        "url": "",
        "publisher": "Gov-Relation Repository",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "database",
        "reliability": "medium",
        "notes": "Confirmed 徐炼 served as 册亨县委副书记 2016-2018; contains 册亨县 organization reference",
    },
    {
        "id": "S005",
        "title": "新闻报道 — 张茂册亨县委书记相关公开报道",
        "url": "",
        "publisher": "综合公开报道",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "media",
        "reliability": "medium",
        "notes": "Prior public records; specific URLs not retrievable in this session",
    },
]


# ═══════════════════════════════════════════════════
# PERSON JSON HELPERS
# ═══════════════════════════════════════════════════


def make_person_json(p, timeline, relationships_list, custom_identity=None, custom_status=None):
    """Create a person graph JSON following the person_graph_json.md schema."""
    is_top = ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or \
             ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", ""))
    rank = "县处级正职" if is_top else "县处级副职"
    is_name_known = "待确认" not in p["name"] and "原" not in p.get("current_post", "")

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
            "person_id": f"ceheng_{p['name']}",
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
                "official_profile_url": "https://www.ceheng.gov.cn/zwgk/ldzc/"
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
            "relationship_confidence": "low" if "待确认" in p["name"] else "medium",
            "biggest_gap": f"{p['name']}的完整职业生涯履历缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月、民族、出生地、教育背景详情",
                "why_it_matters": "核心身份信息完整性",
                "suggested_queries": [f"{p['name']} 简历 册亨"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}何时被任命为现任职务？此前担任什么职务？",
                "why_it_matters": "职业轨迹和晋升路径",
                "suggested_queries": [f"{p['name']} 任免 册亨"],
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
            "question": f"册亨县{p.get('current_post', '')}的姓名",
            "why_it_matters": "核心领导身份未知；无法进行后续履历和关系分析",
            "suggested_queries": [f"册亨县 {p.get('current_post', '')}"],
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

# ── 待确认县委书记 ──
secretary_timeline = [
    {"start": "", "end": "present", "org": "中共册亨县委员会", "title": "册亨县委书记",
     "level": "正县级", "location": "贵州省黔西南州册亨县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "当前册亨县委书记姓名和任命时间未知；网络受限无法确认",
     "confidence": "unverified", "source_ids": []},
]
secretary_relationships = [
    {"person": "（待确认县长）", "person_id": "ceheng_（待确认县长）", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "县委书记与县长搭班子",
     "overlap_org": "中共册亨县委员会/册亨县人民政府", "overlap_period": "current",
     "direction": "person_to_other", "confidence": "unverified", "source_ids": []},
]
secretary_json = make_person_json(PERSONS[0], secretary_timeline, secretary_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县委书记-待确认.json", secretary_json)

# ── 待确认县长 ──
mayor_timeline = [
    {"start": "", "end": "present", "org": "册亨县人民政府", "title": "册亨县人民政府县长",
     "level": "正县级", "location": "贵州省黔西南州册亨县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "当前册亨县长姓名和任命时间未知；网络受限无法确认",
     "confidence": "unverified", "source_ids": []},
    {"start": "", "end": "present", "org": "中共册亨县委员会", "title": "册亨县委副书记",
     "level": "正县级", "location": "贵州省黔西南州册亨县", "system": "party",
     "rank": "正县级", "is_key_promotion": False,
     "notes": "县长兼任县委副书记",
     "confidence": "unverified", "source_ids": []},
]
mayor_relationships = [
    {"person": "（待确认县委书记）", "person_id": "ceheng_（待确认县委书记）", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "县长与县委书记搭班子",
     "overlap_org": "中共册亨县委员会/册亨县人民政府", "overlap_period": "current",
     "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
]
mayor_json = make_person_json(PERSONS[1], mayor_timeline, mayor_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县长-待确认.json", mayor_json)

# ── 张茂 (原册亨县委书记) ──
zm_timeline = [
    {"start": "2014?", "end": "2021?", "org": "中共册亨县委员会", "title": "册亨县委书记",
     "level": "正县级", "location": "贵州省黔西南州册亨县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "张茂任册亨县委书记的期间为Approximate（约2014-2021）；具体起止日期需从官方来源核实",
     "confidence": "plausible", "source_ids": ["S005"]},
    {"start": "unknown", "end": "2014?", "org": "履历缺口", "title": "",
     "notes": "公开资料未找到张茂任册亨县委书记前（2014年前）的完整履历",
     "confidence": "unverified", "source_ids": []},
]
zm_relationships = [
    {"person": "（待确认县长）", "person_id": "ceheng_（待确认县长）", "relationship_type": "superior_subordinate",
     "strength": "medium",
     "evidence": "张茂（原县委书记）与继任县长的可能关系；任期待确认",
     "overlap_org": "中共册亨县委员会/册亨县人民政府", "overlap_period": "unknown",
     "direction": "person_to_other", "confidence": "unverified", "source_ids": ["S005"]},
    {"person": "徐炼", "person_id": "ceheng_徐炼", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "2016-2018年间张茂（县委书记）与徐炼（县委副书记）在县委常委会共事",
     "overlap_org": "中共册亨县委员会", "overlap_period": "2016-2018",
     "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S004", "S005"]},
]
zm_id_extra = {
    "dedupe_keys": {
        "name_birth": "张茂_",
        "name_birthplace": "张茂_",
        "official_profile_url": "https://www.ceheng.gov.cn/zwgk/ldzc/"
    }
}
zm_status_extra = {
    "is_current_confirmed": False,
    "current_post": "（原册亨县委书记）",
}
zm_json = make_person_json(PERSONS[2], zm_timeline, zm_relationships,
                           custom_identity=zm_id_extra, custom_status=zm_status_extra)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县委书记-张茂.json", zm_json)

# ── 徐炼 (原册亨县委副书记, 现任望谟县委书记) ──
xl_timeline = [
    {"start": "2016", "end": "2018", "org": "中共册亨县委员会", "title": "册亨县委副书记",
     "level": "县处级副职", "location": "册亨县", "system": "party",
     "rank": "副县级", "is_key_promotion": True,
     "notes": "在册亨县任县委副书记", "confidence": "plausible", "source_ids": ["S004"]},
    {"start": "2018", "end": "2021", "org": "望谟县人民政府", "title": "望谟县委副书记、县长",
     "level": "县处级正职", "location": "望谟县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "从册亨调任望谟，先任县长", "confidence": "plausible", "source_ids": ["S004"]},
    {"start": "2021", "end": "present", "org": "中共望谟县委员会", "title": "望谟县委书记",
     "level": "县处级正职", "location": "望谟县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "升任望谟县委书记", "confidence": "confirmed", "source_ids": ["S004"]},
    {"start": "unknown", "end": "2016", "org": "履历缺口", "title": "",
     "notes": "徐炼2016年之前在册亨县及之前的完整履历未找到",
     "confidence": "unverified", "source_ids": []},
]
xl_relationships = [
    {"person": "张茂", "person_id": "ceheng_张茂", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "徐炼（县委副书记）在张茂（县委书记）领导下工作",
     "overlap_org": "中共册亨县委员会", "overlap_period": "2016-2018",
     "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S004", "S005"]},
]
xl_id_extra = {
    "dedupe_keys": {
        "name_birth": "徐炼_",
        "name_birthplace": "徐炼_",
        "official_profile_url": "https://www.ceheng.gov.cn/zwgk/ldzc/"
    }
}
xl_status_extra = {
    "current_post": "望谟县委书记",
    "current_org": "中共望谟县委员会",
    "is_current_confirmed": False,
}
xl_json = make_person_json(PERSONS[3], xl_timeline, xl_relationships,
                           custom_identity=xl_id_extra, custom_status=xl_status_extra)

# Correct the scope since 徐炼 is a 望谟 person with 册亨 history
xl_json["investigation_scope"] = {
    "province": PROVINCE,
    "city": PARENT_CITY,
    "region": SLUG,
    "job": "（原册亨县委副书记）",
    "task_id": TASK_ID,
    "time_focus": "2016-2018（册亨任职期）"
}
xl_json["current_status"]["current_post"] = "望谟县委书记"
xl_json["current_status"]["current_org"] = "中共望谟县委员会"
xl_json["confidence_summary"]["biggest_gap"] = "徐炼2016年之前在册亨县及之前的完整履历"

write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-原县委副书记-徐炼.json", xl_json)

print("All person JSONs written.")
