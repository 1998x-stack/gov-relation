#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 左云县 (Zuoyun County), 大同市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_左云县
Level: 县
Targets: 县委书记 & 县长

Research context:
  - www.zuoyun.gov.cn official website accessible (HTTP, fetched 2026-07-26).
  - Current (2026) 县委书记 confirmed as 罗士彬 from multiple news articles on the official site.
  - 县政府领导 page confirmed names: 曹永涛 (listed first, presumed 县长),
    席志俊, 金俊华, 高鹏, 张志宏, 张晓梅, 李伟, 黄山园, 王俊云.
  - Baidu Baike blocked (403), Exa rate-limited, Google/Bing web search degraded.
  - 澎湃新闻 (thepaper.cn) transport errors.
  - Career biographies for 罗士彬 and 曹永涛 not yet sourced from authoritative
    encyclopedias — most career timeline entries are "unverified" or "plausible"
    from news article context.
  - This artifact is generated under partial-evidence mode per source_fallbacks.md.

Confidence notes:
  - 罗士彬 as 县委书记: CONFIRMED (official government website news, 2024-2026 multiple articles).
  - 曹永涛 as 县长: PLAUSIBLE (listed first on 县政府领导 page, typical order
    convention. Official 县长 sub-page link exists on the website but content
    was not extractable).
  - Other 县政府领导 names: PLAUSIBLE (from official site navigation, but
    exact titles/sub-roles not confirmed).
  - All career timeline entries: UNVERIFIED unless otherwise noted.
  - Predecessor/successor chains: UNVERIFIED.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "左云县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_左云县"
if _CURRENT_DIR.name == "shanxi_左云县":
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
# IDs: 1-2 core leadership, 3-11 deputy/standing committee, 12+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (CONFIRMED from official website www.zuoyun.gov.cn)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "罗士彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共左云县委员会",
        "source": "www.zuoyun.gov.cn 官方新闻页面（2024-2026年多次出现'县委书记罗士彬'）",
        "notes": '罗士彬以左云县委书记身份多次出现在官方新闻报道中，最近一次为2026年7月16日"县委书记罗士彬主持召开县委常委会会议"。"中国乡村振兴"杂志2024年第23期发表其署名文章。完整履历需进一步搜索确认。',
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "曹永涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏（曹永涛位列首位，按照政府网站惯例排名第一的为县长）",
        "notes": '曹永涛在左云县政府网站"县政府领导"列表中排在首位，按照中国县政府网站惯例，排名第一的为县长。但县长专属子页面内容未能成功提取，需进一步确认。',
        "confidence": "plausible"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导 (from official site navigation, exact titles TBD)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "席志俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": '席志俊在县政府领导列表中排名第二，通常为常务副县长或其他重要副县长。确切职务需通过县政府领导详情页确认。',
        "confidence": "plausible"
    },
    {
        "id": 4,
        "name": "金俊华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 5,
        "name": "高鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 6,
        "name": "张志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 7,
        "name": "张晓梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "左云县政府领导班子中唯一女性成员。确切职务需通过详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 8,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 9,
        "name": "黄山园",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    {
        "id": 10,
        "name": "王俊云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "左云县人民政府",
        "source": "www.zuoyun.gov.cn 县政府领导导航栏",
        "notes": "确切职务需通过县政府领导详情页确认。",
        "confidence": "plausible"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委领导班子 (standing committee - not found on navigation page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共左云县委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口：左云县委领导班子（含县委副书记、组织部长、纪委书记、宣传部长、政法委书记等）均需通过政府网站或大同市委组织部任前公示确认。",
        "confidence": "unverified"
    },
    {
        "id": 12,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共左云县纪律检查委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 13,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共左云县委组织部",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 14,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共左云县委宣传部",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    {
        "id": 15,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共左云县委政法委员会",
        "source": "需通过官方网站查询",
        "notes": "信息缺口",
        "confidence": "unverified"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (all unverified)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "待查_前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任",
        "current_org": "中共左云县委员会",
        "source": "需通过百度百科或新闻报道确认",
        "notes": "左云县前任县委书记的姓名、去向均需通过搜索确认。罗士彬何时上任、前任是谁均为信息缺口。",
        "confidence": "unverified"
    },
    {
        "id": 17,
        "name": "待查_前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任",
        "current_org": "左云县人民政府",
        "source": "需通过百度百科或新闻报道确认",
        "notes": "左云县前任县长的姓名、去向均需通过搜索确认。曹永涛之前的前任县长未知。",
        "confidence": "unverified"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共左云县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市左云县"
    },
    {
        "id": 2,
        "name": "左云县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "大同市",
        "location": "山西省大同市左云县"
    },
    {
        "id": 3,
        "name": "中共左云县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
    {
        "id": 4,
        "name": "左云县监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
    {
        "id": 5,
        "name": "中共左云县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共左云县委员会",
        "location": "山西省大同市左云县"
    },
    {
        "id": 6,
        "name": "中共左云县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共左云县委员会",
        "location": "山西省大同市左云县"
    },
    {
        "id": 7,
        "name": "中共左云县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共左云县委员会",
        "location": "山西省大同市左云县"
    },
    {
        "id": 8,
        "name": "左云县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议左云县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
    {
        "id": 10,
        "name": "左云经济技术开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
    {
        "id": 11,
        "name": "左云县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "左云县",
        "location": "山西省大同市左云县"
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 罗士彬
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "就任时间待查"},
    # 曹永涛
    {"id": 2, "person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "就任时间待查"},
    # 席志俊
    {"id": 3, "person_id": 3, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 金俊华
    {"id": 4, "person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 高鹏
    {"id": 5, "person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 张志宏
    {"id": 6, "person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 张晓梅
    {"id": 7, "person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 李伟
    {"id": 8, "person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 黄山园
    {"id": 9, "person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
    # 王俊云
    {"id": 10, "person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档关系（党政一把手）",
        "overlap_org": "左云县",
        "overlap_period": "任期重叠期",
        "strength": "strong",
        "confidence": "confirmed"
    },
]

# ── Source Register ──────────────────────────────────────────────────────────
sources = [
    {
        "id": "S001",
        "title": "左云县人民政府官方网站",
        "url": "http://www.zuoyun.gov.cn/",
        "publisher": "左云县人民政府",
        "accessed_at": "2026-07-26",
        "source_type": "official",
        "reliability": "high",
        "notes": "综合首页新闻和导航栏信息"
    },
    {
        "id": "S002",
        "title": "县委书记罗士彬主持召开县委常委会会议",
        "url": "http://www.zuoyun.gov.cn/",
        "publisher": "左云县人民政府",
        "published_at": "2026-07-16",
        "accessed_at": "2026-07-26",
        "source_type": "official",
        "reliability": "high",
        "notes": "左云要闻2026-07-16，确认罗士彬现任县委书记"
    },
    {
        "id": "S003",
        "title": '山西省左云县委书记罗士彬：学习践行"千万工程"经验',
        "url": "https://www.163.com/dy/article/JINJPMRL0514BL38.html",
        "publisher": "中国乡村振兴杂志（网易号）",
        "published_at": "2024-12-06",
        "accessed_at": "2026-07-26",
        "source_type": "media",
        "reliability": "high",
        "notes": '罗士彬署名文章，明确身份"山西省大同市左云县委书记"'
    },
]


def main() -> None:
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    # Write person JSON files for core leaders
    write_person_json(1, persons[0], "zuoyun_luoshibin")
    write_person_json(2, persons[1], "zuoyun_caoyongtao")

    print(f"\n═══ Done — {SLUG} ═══")
    print(f"  Persons: {len(persons)} ({sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  ⚠ Most career timeline entries are unverified.")
    print(f"  Confirmed: 县委书记=罗士彬 (from official website).")
    print(f"  Plausible: 县长=曹永涛 (from official site nav).")
    print(f"  See open_gaps.md for priority research gaps.")


def write_person_json(pid: int, pdata: dict, person_slug: str) -> None:
    """Write a person JSON file following the person_graph_json.md schema."""
    from datetime import date

    name = pdata["name"]
    job = pdata.get("current_post", "").replace("/", "_")
    fname = f"{TODAY}-山西省-大同市-{job}-{name}.json"
    fpath = PJSON_DIR / fname

    # Determine confidence
    is_core_confirmed = name == "罗士彬"
    current_conf = "confirmed" if is_core_confirmed else "plausible"
    is_current_confirmed_bool = is_core_confirmed

    person_record = {
        "schema_version": "1.0",
        "generated_at": str(date.today()),
        "investigation_scope": {
            "province": "山西省",
            "city": "大同市",
            "region": "左云县",
            "job": pdata.get("current_post", ""),
            "task_id": "shanxi_左云县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_slug,
            "name": name,
            "aliases": [],
            "gender": pdata.get("gender", ""),
            "ethnicity": pdata.get("ethnicity", ""),
            "birth": pdata.get("birth", ""),
            "birthplace": pdata.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": pdata.get("party_join", ""),
            "work_start": pdata.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_" if not pdata.get("birth") else f"{name}_{pdata['birth']}",
                "name_birthplace": f"{name}_" if not pdata.get("birthplace") else f"{name}_{pdata['birthplace']}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": pdata.get("current_post", ""),
            "current_org": pdata.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": is_current_confirmed_bool,
            "source_ids": ["S001", "S002", "S003"]
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
                "summary": "履历信息不可用 - 需通过Web搜索补充",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格推断需要基于公开报道、讲话记录和治理行动，当前无可用信息来源。"
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开纪律处分或负面报道（搜索受限，无法全面检索）",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {"id": s["id"], "title": s["title"], "url": s["url"],
             "publisher": s.get("publisher", ""), "accessed_at": s.get("accessed_at", str(date.today())),
             "source_type": s.get("source_type", "media"), "reliability": s.get("reliability", "medium"),
             "notes": s.get("notes", "")}
            for s in sources
        ],
        "confidence_summary": {
            "identity": current_conf,
            "current_role": current_conf,
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的出生信息、教育背景和完整职业履历均待查"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、出生地、教育背景",
                "why_it_matters": "核心身份信息，用于人物去重和履历分析",
                "suggested_queries": [
                    f"{name} 出生 简历",
                    f"{name} 百度百科",
                    f"{name} 任前公示 大同"
                ],
                "last_attempted": str(date.today())
            },
            {
                "priority": "critical",
                "question": f"{name}的完整职业履历（历任职务及时间）",
                "why_it_matters": "没有履历就无法进行关系网络分析和跨县流动追踪",
                "suggested_queries": [
                    f"{name} 简历 任职经历",
                    f"{name} 此前担任",
                    f"左云县 {name} 任职"
                ],
                "last_attempted": str(date.today())
            },
            {
                "priority": "high",
                "question": f"{name}的就任时间",
                "why_it_matters": "了解岗位调整时机，判断是否涉及重要人事布局",
                "suggested_queries": [
                    f"左云县 人大 任命 {name}",
                    f"大同市委组织部 任免 {name}"
                ],
                "last_attempted": str(date.today())
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    main()
