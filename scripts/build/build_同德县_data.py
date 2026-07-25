#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 同德县 (Tongde County), 海南藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_同德县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — web access was severely degraded during investigation:
  - Exa search API rate-limited
  - Baidu Baike returned HTTP 403
  - Government websites (同德县, 海南州) unreachable via HTTP(S) and Jina Reader
  - Google, Wikipedia (zh), Baidu all timed out via all available fetchers
  - Due to the above constraints, specific current officeholder names could NOT be
    verified from current primary sources in this session.

Confidence notes:
  - Administrative structure (organizations, levels) is confirmed from standard
    administrative division records (Wikipedia EN, qinghai_administrative_divisions.json).
  - Current officeholder names are marked as "待查_县委书记" and "待查_县长"
    (to be checked) — verifying from the 同德县 government website's 领导之窗 page
    or 海南州 appointment notices is required.
  - All biographical fields for persons are left empty with appropriate confidence markers.
  - The build script is structurally complete but requires populating specific
    leader names when official sources become accessible.

Expected government website: www.tongde.gov.cn
Expected leadership page: /xxgk/ldzc/ or /zwgk/ldzc/
Parent-city website: www.hainanzhou.gov.cn
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
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

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "同德县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_同德县"
if _CURRENT_DIR.name == "qinghai_同德县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
# NOTE: Specific officeholder names could NOT be verified due to complete
# web access degradation. All person-level biographic data requires manual
# verification from official sources.
# Expected domain: www.tongde.gov.cn

persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委书记",
        "current_org": "中共同德县委员会",
        "source": "Web access degraded — name unverified. Check 同德县领导之窗 at www.tongde.gov.cn",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委副书记、县长",
        "current_org": "同德县人民政府",
        "source": "Web access degraded — name unverified. Check 同德县领导之窗 at www.tongde.gov.cn",
    },
    # ════════════════════════════════════════════════════════════════════
    # County Standing Committee (县委常委)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委副书记 (Deputy Party Secretary, typically 3rd-ranking) ---
    {
        "id": 3,
        "name": "待查_副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委副书记",
        "current_org": "中共同德县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、副县长（常务） ---
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、副县长（常务）",
        "current_org": "同德县人民政府",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、纪委书记、监委主任 ---
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、纪委书记、监委主任",
        "current_org": "中共同德县纪律检查委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、组织部部长 ---
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、组织部部长",
        "current_org": "中共同德县委组织部",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、宣传部部长 ---
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、宣传部部长",
        "current_org": "中共同德县委宣传部",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、政法委书记 ---
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、政法委书记",
        "current_org": "中共同德县委政法委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、统战部部长 ---
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、统战部部长",
        "current_org": "中共同德县委统一战线工作部",
        "source": "Web access degraded — name unverified.",
    },
    # --- 县委常委、县委办公室主任 ---
    {
        "id": 10,
        "name": "待查_县委办主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县委常委、县委办公室主任",
        "current_org": "中共同德县委办公室",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # Key Deputy Positions
    # ════════════════════════════════════════════════════════════════════
    # --- 副县长、公安局局长 ---
    {
        "id": 11,
        "name": "待查_副县长兼公安局长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县副县长、公安局局长",
        "current_org": "同德县公安局",
        "source": "Web access degraded — name unverified.",
    },
    # --- 副县长（分管教育、卫生等） ---
    {
        "id": 12,
        "name": "待查_副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "同德县副县长",
        "current_org": "同德县人民政府",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县人大常委会主任 (County People's Congress Chairman)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "待查_人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县人大常委会主任",
        "current_org": "同德县人民代表大会常务委员会",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县政协主席 (County CPPCC Chairman)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县政协主席",
        "current_org": "中国人民政治协商会议同德县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县人民法院院长 (County Court President)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "待查_法院院长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县人民法院院长",
        "current_org": "同德县人民法院",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县人民检察院检察长 (County Procuratorate Chief)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "待查_检察长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "同德县人民检察院检察长",
        "current_org": "同德县人民检察院",
        "source": "Web access degraded — name unverified.",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    # Party Committee
    {
        "id": 1,
        "name": "中共同德县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海南藏族自治州委员会",
        "location": "青海省海南州同德县",
    },
    # County Government
    {
        "id": 2,
        "name": "同德县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海南藏族自治州人民政府",
        "location": "青海省海南州同德县",
    },
    # Discipline Inspection
    {
        "id": 3,
        "name": "中共同德县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海南州纪律检查委员会",
        "location": "青海省海南州同德县",
    },
    # Organization Department
    {
        "id": 4,
        "name": "中共同德县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共同德县委员会",
        "location": "青海省海南州同德县",
    },
    # Propaganda Department
    {
        "id": 5,
        "name": "中共同德县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共同德县委员会",
        "location": "青海省海南州同德县",
    },
    # Political and Legal Affairs Commission
    {
        "id": 6,
        "name": "中共同德县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共同德县委员会",
        "location": "青海省海南州同德县",
    },
    # United Front Work Department
    {
        "id": 7,
        "name": "中共同德县委统一战线工作部",
        "type": "党委",
        "level": "县级",
        "parent": "中共同德县委员会",
        "location": "青海省海南州同德县",
    },
    # County Party Committee Office
    {
        "id": 8,
        "name": "中共同德县委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共同德县委员会",
        "location": "青海省海南州同德县",
    },
    # Public Security Bureau
    {
        "id": 9,
        "name": "同德县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "同德县人民政府",
        "location": "青海省海南州同德县",
    },
    # People's Congress
    {
        "id": 10,
        "name": "同德县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "海南州人民代表大会常务委员会",
        "location": "青海省海南州同德县",
    },
    # CPPCC
    {
        "id": 11,
        "name": "中国人民政治协商会议同德县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协海南州委员会",
        "location": "青海省海南州同德县",
    },
    # Court
    {
        "id": 12,
        "name": "同德县人民法院",
        "type": "政府",
        "level": "县级",
        "parent": "海南州中级人民法院",
        "location": "青海省海南州同德县",
    },
    # Procuratorate
    {
        "id": 13,
        "name": "同德县人民检察院",
        "type": "政府",
        "level": "县级",
        "parent": "海南州人民检察院",
        "location": "青海省海南州同德县",
    },
    # County Government General Office (placeholder for deputy roles)
    {
        "id": 14,
        "name": "同德县人民政府办公室",
        "type": "政府",
        "level": "县级",
        "parent": "同德县人民政府",
        "location": "青海省海南州同德县",
    },
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同德县一把手"},
    # 县长（兼县委副书记）
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县人民政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 常务副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长（常务）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 纪委书记
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 组织部长
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 宣传部长
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 县委办主任
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "县委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 副县长兼公安局长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 副县长
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大常委会主任
    {"person_id": 13, "org_id": 10, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 政协主席
    {"person_id": 14, "org_id": 11, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 法院院长
    {"person_id": 15, "org_id": 12, "title": "县人民法院院长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 检察长
    {"person_id": 16, "org_id": 13, "title": "县人民检察院检察长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 县委书记 — 县长（党政正职关系）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县长党政搭档", "overlap_org": "同德县四套班子", "overlap_period": "截至2026年"},
    # 县委书记 — 县委副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—副书记", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    # 县委书记 — 纪委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记—纪委书记（同级监督关系）", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    # 县委书记 — 组织部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记—组织部长（干部管理）", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    # 县委常委间同僚关系
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共同德县委员会", "overlap_period": "截至2026年"},
    # 县长—常务副县长（政府班子）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—常务副县长", "overlap_org": "同德县人民政府", "overlap_period": "截至2026年"},
    # 县长—副县长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "同德县人民政府", "overlap_period": "截至2026年"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "同德县人民政府", "overlap_period": "截至2026年"},
]

# ── Person JSON Helpers ──────────────────────────────────────────────────
def write_person_json(person: dict, job: str) -> None:
    """Write a person graph JSON file to the staging directory."""
    safe_name = person["name"].replace("/", "_").replace(" ", "")
    filename = f"{TODAY}-青海省-海南藏族自治州-{job}-{safe_name}.json"
    filepath = PJSON_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "青海省",
            "city": "海南藏族自治州",
            "region": "同德县",
            "job": job,
            "task_id": "qinghai_同德县",
            "time_focus": "截至2026-07-25",
        },
        "identity": {
            "person_id": f"qinghai_hainan_tongde_{safe_name}_unknown",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
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
            "promotion_velocity": {"summary": "unknown — no verified career data"},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style indicators unavailable — no public evidence accessible in this session.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found. Web access was fully degraded; no sources could be checked.",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "All biographic fields unknown — complete web access failure prevented any source verification.",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Who is the current {person['current_post']} of 同德县?",
                "why_it_matters": "Core target for this investigation; entire network depends on accurate leadership identification.",
                "suggested_queries": [
                    f"同德县 现任 {person['current_post']}",
                    "同德县 领导之窗",
                    "同德县 领导分工",
                    "海南州 同德县 任前公示",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "What is the full career timeline of this person?",
                "why_it_matters": "Career timeline is needed for relationship network analysis and predecessor/successor mapping.",
                "suggested_queries": [f"同德县 {person['name']} 简历", f"{person['name']} 任职履历"],
                "last_attempted": AS_OF,
            },
        ],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


# ── Main ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")

    # 1. Build SQLite DB and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # 2. Write person JSON files for core leaders (县委书记 and 县长)
    print("--- Writing person JSON files ---")
    write_person_json(persons[0], "县委书记")
    write_person_json(persons[1], "县长")

    print(f"\nDone. Artifacts in {STAGING}:")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PJSON_DIR.glob(f"{TODAY}-*.json")):
        print(f"  JSON: {f}")
