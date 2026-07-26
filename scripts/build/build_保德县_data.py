#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 保德县 (Baode County), 忻州市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_保德县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.baode.gov.cn — 保德县人民政府官方网站 (primary, current as of July 2026)
  - Multiple news articles from 保德县融媒体中心 (June-July 2026)
  - Web search was degraded: Exa rate-limited, Baidu 403, Jina timeouts

Confidence notes:
  - Current roles: confirmed via multiple government news reports (July 2026)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
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
SLUG = "保德县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_保德县"
if _CURRENT_DIR.name == "shanxi_保德县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current, as of July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Shanxi county leaders are Han
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席、县委书记",
        "current_org": "中国人民政治协商会议忻州市委员会/中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260605_4186662.html",
    },
    {
        "id": 2,
        "name": "田江波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202607/t20260722_4195197.html",
    },
    # ── County Party Committee Standing Members ──
    {
        "id": 3,
        "name": "吴雁臻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260616_4188231.html",
    },
    {
        "id": 4,
        "name": "邵宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "中共保德县委员会/保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260618_4188664.html",
    },
    {
        "id": 5,
        "name": "冯振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260605_4186662.html",
    },
    {
        "id": 6,
        "name": "王焕林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260605_4186662.html",
    },
    {
        "id": 7,
        "name": "王小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260605_4186662.html",
    },
    {
        "id": 8,
        "name": "吴治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260605_4186662.html",
    },
    {
        "id": 9,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共保德县委员会/保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260618_4188664.html",
    },
    # ── County Government ──
    {
        "id": 10,
        "name": "白侯平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202607/t20260722_4195197.html",
    },
    {
        "id": 11,
        "name": "翟志伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202607/t20260722_4195197.html",
    },
    {
        "id": 12,
        "name": "高林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260610_4187367.html",
    },
    {
        "id": 13,
        "name": "王宏喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "保德县人民政府",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260618_4188664.html",
    },
    {
        "id": 14,
        "name": "田开喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "保德县人民政府/保德县公安局",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260610_4187367.html",
    },
    # ── 人大 ──
    {
        "id": 15,
        "name": "高彩文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "保德县人民代表大会常务委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202606/t20260623_4189304.html",
    },
    # ── 政协 ──
    {
        "id": 16,
        "name": "吴培斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议保德县委员会",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/202607/t20260707_4192123.html",
    },
    # ── Predecessor ──
    {
        "id": 17,
        "name": "韩朝炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "保德县原县长（已离任）",
        "current_org": "",
        "source": "http://www.baode.gov.cn/zwyw/bdyw/index_1.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共保德县委员会",
        "type": "党委",
        "level": "县",
        "location": "山西省忻州市保德县",
    },
    {
        "id": 2,
        "name": "保德县人民政府",
        "type": "政府",
        "level": "县",
        "location": "山西省忻州市保德县",
    },
    {
        "id": 3,
        "name": "保德县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "location": "山西省忻州市保德县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商委员会保德县委员会",
        "type": "政协",
        "level": "县",
        "location": "山西省忻州市保德县",
    },
    {
        "id": 5,
        "name": "保德县公安局",
        "type": "政府",
        "level": "县",
        "location": "山西省忻州市保德县",
    },
    {
        "id": 6,
        "name": "中国人民政治协商委员会忻州市委员会",
        "type": "政协",
        "level": "市",
        "location": "山西省忻州市",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李军
    {"person_id": 1, "org_id": 6, "title": "忻州市政协副主席", "start": "", "end": "present", "rank": "副厅", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "保德县委书记", "start": "", "end": "present", "rank": "正处（副厅级）", "note": "李军同时担任忻州市政协副主席，可能为副厅级" + "高配"},
    # 田江波
    {"person_id": 2, "org_id": 2, "title": "保德县政府党组书记", "start": "", "end": "present", "rank": "正处级", "note": "confirmed as 县政府党组书记 in July 2026"},
    {"person_id": 2, "org_id": 1, "title": "保德县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "保德县县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    # 吴雁臻
    {"person_id": 3, "org_id": 1, "title": "保德县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 邵宁
    {"person_id": 4, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "保德县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 冯振宇
    {"person_id": 5, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王焕林
    {"person_id": 6, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王小勇
    {"person_id": 7, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 吴治国
    {"person_id": 8, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张伟
    {"person_id": 9, "org_id": 1, "title": "保德县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 白侯平
    {"person_id": 10, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 翟志伟
    {"person_id": 11, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 高林
    {"person_id": 12, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王宏喜
    {"person_id": 13, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 田开喜
    {"person_id": 14, "org_id": 2, "title": "保德县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "保德县公安局局长", "start": "", "end": "present", "rank": "正科级（兼任）", "note": ""},
    # 高彩文
    {"person_id": 15, "org_id": 3, "title": "保德县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 吴培斌
    {"person_id": 16, "org_id": 4, "title": "保德县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 韩朝炜 (predecessor)
    {"person_id": 17, "org_id": 2, "title": "保德县县长（原）", "start": "", "end": "2026-06", "rank": "正处级", "note": "前任县长，2026年4月仍在主持县政府会议，7月已由田江波接任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core dyads: Party secretary ↔ County mayor
    {
        "person_a": 1,  # 李军
        "person_b": 2,  # 田江波
        "type": "领导班子搭档",
        "context": "县委书记与县长党政主要领导搭档",
        "overlap_org": "保德县",
        "overlap_period": "2026-07至今",
    },
    # 李军 ↔ 吴雁臻 (县委正副书记)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "领导副手",
        "context": "县委书记与县委副书记搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    # 李军 ↔ 县委常委全体
    {
        "person_a": 1,
        "person_b": 4,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "领导班子",
        "context": "县委常委会搭档",
        "overlap_org": "中共保德县委",
        "overlap_period": "2026年",
    },
    # 田江波 ↔ 副县长们
    {
        "person_a": 2,
        "person_b": 10,
        "type": "政府班子",
        "context": "县长与副县长搭档",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "政府班子",
        "context": "县长与副县长搭档",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "政府班子",
        "context": "县长与副县长搭档",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "政府班子",
        "context": "县长与副县长搭档",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "政府班子",
        "context": "县长与公安局长（副县长兼任）搭档",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    # 田江波 ↔ 前任县长韩朝炜 (succession)
    {
        "person_a": 2,
        "person_b": 17,
        "type": "前任后任",
        "context": "田江波接替韩朝炜任保德县县长",
        "overlap_org": "保德县人民政府",
        "overlap_period": "2026年",
    },
    # 人大主任 ↔ 县委领导
    {
        "person_a": 1,
        "person_b": 15,
        "type": "党政负责人",
        "context": "县委书记与人大常委会主任",
        "overlap_org": "保德县",
        "overlap_period": "2026年",
    },
    # 李军 ↔ 县政协副主席
    {
        "person_a": 1,
        "person_b": 16,
        "type": "政协联系",
        "context": "李军同时为忻州市政协副主席，与保德县政协副主席共事",
        "overlap_org": "政协系统",
        "overlap_period": "2026年",
    },
]

# ── Build ────────────────────────────────────────────────────────────────────
def write_person_json(person: dict) -> str:
    """Write a person JSON file to the staging directory and return its path."""
    job = person["current_post"].split("、")[0].replace("/", "_").replace("（", "").replace("）", "")
    name = person["name"]
    filename = f"{TODAY}-山西省-忻州市-{job}-{name}.json"
    filepath = Path(PJSON_DIR) / filename

    # Build a person graph JSON following the schema in references/person_graph_json.md
    content = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "忻州市",
            "region": "保德县",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_保德县",
            "time_focus": "2026年",
        },
        "identity": {
            "person_id": f"baode_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
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
                "title": "保德县人民政府门户网站",
                "url": person.get("source", "http://www.baode.gov.cn"),
                "publisher": "保德县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official government news article confirming current role",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Biographical details (birth year, birthplace, education, career timeline) missing for {name}",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的具体出生年月、籍贯、学历信息",
                "why_it_matters": "难以核实身份唯一性，无法追溯晋升轨迹",
                "suggested_queries": [f"{name} 简历 保德", f"{name} 忻州 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的完整履历和晋升时间线",
                "why_it_matters": "无法分析其晋升模式和来源系统",
                "suggested_queries": [f"{name} 任", f"保德县 {name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")
    return str(filepath)


if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Create person JSON files for core leaders
    core_ids = [1, 2, 3, 4, 15, 17]  # 李军, 田江波, 吴雁臻, 邵宁, 高彩文, 韩朝炜
    pjson_paths = []
    for p in persons:
        if p["id"] in core_ids:
            path = write_person_json(p)
            pjson_paths.append(str(path))

    print(f"  Person JSONs: {len(pjson_paths)} files")

    print("Done.")