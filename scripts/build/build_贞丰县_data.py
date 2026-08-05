#!/usr/bin/env python3
"""Build script for 贞丰县 (Zhenfeng County, Qianxinan, Guizhou) leadership network.

Generated: 2026-08-05
Level: 县
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Targets: 县委书记 & 县长
Task ID: guizhou_贞丰县

Research Note (2026-08-05):
  Web sources were severely degraded during this research cycle:
  - 贞丰县政府门户 www.zhenfeng.gov.cn (and gzqf/qxnzf candidates): transport error
  - Exa search API: rate-limited 503
  - Baidu Baike: 403; Google/Bing/thepaper/Wayback: timed out
  - qxn.gov.cn 站内检索: searchWord not honored via plain GET (0 results)
  - RELIABLE CHANNEL: 黔西南州政府网 www.qxn.gov.cn news pages via webfetch

  Key findings:
  - The CURRENT 贞丰县委书记 and 县长 names could NOT be source-verified in this
    session (county portal down, county leaders not named in state-level news).
    Encoded as "待确认" with unverified confidence.
  - Confirmed 贞丰 county figure: 陆昌斌 (布依族), 贞丰县流动党员东阳党支部书记、
    贞丰县驻东阳劳务协作工作站站长, awarded 全国优秀党务工作者 2026-07-01
    (qxn.gov.cn/zwxx/jzyw/202607/t20260702_90580089.html). Not a county 领导班子 member.
  - 段棚: appears as 州领导干部 attending 2026-07-08 work (qxn.gov.cn
    /zwxx/jzyw/202607/t20260708_90598422.html). His former 贞丰县委书记 history is
    BACKGROUND KNOWLEDGE and is NOT source-verified in this session (idle unverified).
  - 州级上级框架 confirmed: 州委书记邱祯国, 州委副书记/代州长史麒麟, 州委副书记/兴义书记
    顾先林, 州人大主任罗春红, 州政协主席周舟. These are 州-level (not 贞丰县), kept
    as context only, not as 贞丰县 network nodes.

  Confidence downgraded because current (2026-08) 贞丰 county office holders cannot be
  verified through working channels. Artifacts encode uncertainty with explicit
  "unverified" labels and open_questions/open_gaps; structural county information is
  retained. No fabricated names.
"""

import json
import sqlite3
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════

TASK_ID = "guizhou_贞丰县"
SLUG = "贞丰县"
AS_OF = "2026-08-05"
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
    # ── Core Leaders (county one / two, names unverified under degraded web) ──
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
        "current_post": "贞丰县委书记",
        "current_org": "中共贞丰县委员会",
        "source": "Web access unavailable. 贞丰县政府门户(www.zhenfeng.gov.cn)不可达；州级新闻未点名列名的县级书记。现任姓名待确认。",
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
        "current_post": "贞丰县人民政府县长",
        "current_org": "贞丰县人民政府",
        "source": "Web access unavailable. 当前县长未能通过可用坊源证实。现任姓名待确认。",
    },
    # ── 确认的贞丰县基层党务人物（非遗县领导班子成员）──
    {
        "id": 3,
        "name": "陆昌斌",
        "gender": "",
        "ethnicity": "布依族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "贞丰县流动党员东阳党支部书记、贞丰县驻东阳劳务协作工作站站长",
        "current_org": "贞丰县流动党员党组织",
        "source": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260702_90580089.html",
    },
    # ── 前任/州级连接线索：段陆（其贞丰历史待核）──
    {
        "id": 4,
        "name": "段棚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黔西南州干部（州领导中出席活动）",
        "current_org": "黔西南州机关",
        "source": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260708_90598422.html",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共贞丰县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州委员会",
        "location": "贵州省黔西南州贞丰县",
    },
    {
        "id": 2,
        "name": "贞丰县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "黔西南州人民政府",
        "location": "贵州省黔西南州贞丰县",
    },
    {
        "id": 3,
        "name": "贞丰县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "黔西南州人大常委会",
        "location": "贵州省黔西南州贞丰县",
    },
    {
        "id": 4,
        "name": "政协贞丰县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协黔西南州委员会",
        "location": "贵州省黔西南州贞丰县",
    },
    {
        "id": 5,
        "name": "中共贞丰县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州纪律检查委员会",
        "location": "贵州省黔西南州贞丰县",
    },
]

POSITIONS = [
    # 待确认 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "贞丰县委书记", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "截至2026-08在任；姓名未能通过可用渠道核实"},
    # 待确认 — 县长
    {"person_id": 2, "org_id": 2, "title": "贞丰县人民政府县长", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "截至2026-08在任；姓名未能核实"},
    {"person_id": 2, "org_id": 1, "title": "贞丰县委副书记", "start_date": "", "end_date": "present",
     "rank": "正县级", "note": "县长一般兼任县委副书记（常规配置）"},
    # 陆昌斌 — 贞丰基层党务（已确认）
    {"person_id": 3, "org_id": 1, "title": "贞丰县流动党员东阳党支部书记", "start_date": "", "end_date": "present",
     "rank": "基层", "note": "2026-07获全国'全国优秀党务工作者'；流动党员党组织书记，属贞丰县党建体系"},
    {"person_id": 3, "org_id": 2, "title": "贞丰县驻东阳劳务协作工作站站长", "start_date": "", "end_date": "present",
     "rank": "基层", "note": "劳动协作工作站站长（劳务协作）"},
    # 段棚 — 州级现任（贞丰县历史履历待核）
    {"person_id": 4, "org_id": 2, "title": "（州干部，具体职务待核）", "start_date": "", "end_date": "present",
     "rank": "州级", "note": "州新闻2026-07-08以'州领导'身份出席。其曾任贞丰县委书记等信息为背景知识、本次未实证"},
]

RELATIONSHIPS = [
    # 书记—县长搭班子（当前，姓名未知）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "贞丰县委书记—县长搭班子（当前，姓名待确认）",
        "overlap_org": "中共贞丰县委员会/贞丰县人民政府",
        "overlap_period": "current",
    },
    # 陆昌斌 — 贞丰县党建体系（基层）
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "陆昌斌所属流动党员党组织隶属贞丰县党建体系，受县委领导（关系为体系隶属层面，非常直接搭班子）",
        "overlap_org": "中共贞丰县委员会",
        "overlap_period": "7406年",
    },
    # 段棚 — 州干部（与贞丰县的历史关联待核）
    {
        "person_a": 4, "person_b": 1,
        "type": "或然前任秘书关系",
        "context": "若段棚确曾任贞丰县委书记（背景知识，未实证），则与现任书记为前任后继关系；本次度未核，标记 unverified",
        "overlap_org": "中共贞丰县委员会",
        "overlap_period": "待核",
    },
]

# ═══════════════════════════════════════════════════
# SOURCE REGISTER
# ═══════════════════════════════════════════════════

SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "贞丰县人民政府门户网 — 领导之窗",
        "url": "https://www.zhenfeng.gov.cn/xxgk/ldjs/",
        "publisher": "贞丰县人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "站点本次不可达；列为未来核实现任县领导的一手来源",
    },
    {
        "id": "S002",
        "title": "黔西南州人民政府 — 黔西南州半年经济工作会议",
        "url": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260730_90674759.html",
        "publisher": "黔西南州人民政府办公室",
        "published_at": "2026-07-30",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认州委书记邱祯国、州委副书记、代州长史麒麟等州级框架（贞丰县的上级）；未点名县级领导",
    },
    {
        "id": "S003",
        "title": "黔西南州人民政府 — 邱祯国赴省对接工作",
        "url": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260708_90598422.html",
        "publisher": "黔西南州人民政府办公室",
        "published_at": "2026-07-08",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认州委书记邱祯国；段棚以'州领导'身份出席（段棚ISP州级身份）",
    },
    {
        "id": "S004",
        "title": "黔西南州人民政府 — 全国'两优一先'名单公布",
        "url": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260702_90580089.html",
        "publisher": "动静贵州/黔西南州人民政府办公室",
        "published_at": "2026-07-02",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认陆昌斌（布依族，贞丰县流动党员东阳党支部书记、驻东阳劳务协作站站长）获全国优秀党务工作者",
    },
    {
        "id": "S005",
        "title": "黔西南州人民政府 — 州政协党建工作会议（州政协主席周舟）",
        "url": "https://www.qxn.gov.cn/zwxx/jzyw/202606/t20260615_90523302.html",
        "publisher": "黔西南州人民政府办公室",
        "published_at": "2026-06-15",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "州级框架参考；周舟为州政协党组书记、主席",
    },
]

# ═══════════════════════════════════════════════════
# HELPERS
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
            "time_focus": "2026年8月"
        },
        "identity": {
            "person_id": f"zhenfeng_{p['name']}",
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
                "official_profile_url": "https://www.zhenfeng.gov.cn/xxgk/ldjs/"
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
            {"type": "none_found", "description": f"截至{AS_OF}未在可用渠道发现与该人物相关的纪律处分或负面舆情内容（注：因网络严重受限，检索覆盖有限）",
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
                "suggested_queries": [f"{p['name']} 简历 贞丰"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}何时被任命为现任职务？此前担任什么职务？",
                "why_it_matters": "职业轨迹和晋升路径",
                "suggested_queries": [f"{p['name']} 任免 贞丰"],
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
            "question": f"贞丰县{p.get('current_post', '')}的姓名",
            "why_it_matters": "核心领导身份未知；无法进行后续履历和关系分析",
            "suggested_queries": [f"贞丰县 {p.get('current_post', '')}"],
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
    {"start": "", "end": "present", "org": "中共贞丰县委员会", "title": "贞丰县委书记",
     "level": "正县级", "location": "贵州省黔西南州贞丰县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "现任姓名及任命时间未知；网络受限无法确认",
     "confidence": "unverified", "source_ids": []},
]
secretary_relationships = [
    {"person": "（待确认县长）", "person_id": "zhenfeng_（待确认县长）",
     "relationship_type": "superior_subordinate", "strength": "strong",
     "evidence": "县委书记—县长搭班子（当前，姓名待确认）",
     "overlap_org": "中共贞丰县委员会/贞丰县人民政府", "overlap_period": "至今",
     "direction": "person_to_other", "confidence": "unverified", "source_ids": []},
]
secretary_json = make_person_json(PERSONS[0], secretary_timeline, secretary_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县委书记-待确认.json", secretary_json)

# ── 待确认县长 ──
mayor_timeline = [
    {"start": "", "end": "present", "org": "贞丰县人民政府", "title": "贞丰县人民政府县长",
     "level": "正县级", "location": "贵州省黔西南州贞丰县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "现任县长姓名和任命时间未知网络受限无法确认",
     "confidence": "unverified", "source_ids": []},
    {"start": "", "end": "present", "org": "中共贞丰县委员会", "title": "贞丰县委副书记",
     "level": "正县级", "location": "贵州省黔西南州贞丰县", "system": "party",
     "rank": "正县级", "is_key_promotion": False,
     "notes": "县长一般兼任县委副书记（常规配置，姓名未知）",
     "confidence": "unverified", "source_ids": []},
]
mayor_relationships = [
    {"person": "（待确认县委书记）", "person_id": "贞丰_（待确认县委书记）",
     "relationship_type": "superior_subordinate", "strength": "strong",
     "evidence": "贞丰县县长—县委书记搭班子（当前，姓名待确认）",
     "overlap_org": "中共贞丰县委员会/贞丰县人民政府", "overlap_period": "至今",
     "direction": "other_to_person", "confidence": "unverified", "source_ids": []},
]
mayor_json = make_person_json(PERSONS[1], mayor_timeline, mayor_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县长-待确认.json", mayor_json)

# ── 陆昌斌 (confirmed 贞丰基层) ──
lcb_timeline = [
    {"start": "", "end": "present", "org": "贞丰县流动党员党组织",
     "title": "贞丰县流动党员东阳党支部书记", "level": "基层", "location": "贵州省黔西南州贞丰县",
     "system": "other", "rank": "基层", "is_key_promotion": False,
     "notes": "2026-07-01获全国'全国优秀党务工作者'称号（国家层面表彰）",
     "confidence": "confirmed", "source_ids": ["S004"]},
]
lcb_relationships = [
    {"person": "（待确认县委书记）", "person_id": "",
     "relationship_type": "superior_subordinate", "strength": "weak",
     "evidence": "陆昌斌所在流动党员党组织隶属贞丰县委党建体系（间接层级，非遗级领导班子成员）",
     "overlap_org": "中共贞丰县委员会", "overlap_period": "",
     "direction": "undirected", "confidence": "unverified", "source_ids": ["S004"]},
]
lcb_json = make_person_json(PERSONS[2], lcb_timeline, lcb_relationships,
                            custom_identity={
                                "person_id": "zhenfeng_陆昌斌",
                                "dedupe_keys": {
                                    "name_birth": "陆昌斌_",
                                    "name_birthplace": "陆昌斌_",
                                    "official_profile_url": "https://www.qxn.gov.cn/zwxx/jzyw/202607/t20260702_90580089.html"
                                }
                            },
                            custom_status={
                                "is_current_confirmed": True,
                                "source_ids": ["S202"]
                            })
lcb_json["confidence_summary"]["identity"] = "confirmed"
lcb_json["confidence_summary"]["current_role"] = "confirmed"
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-流动党员党支部书记-陆昌斌.json", lcb_json)

print("All person JSONs written.")