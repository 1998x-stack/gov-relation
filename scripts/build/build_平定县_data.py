#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平定县, 阳泉市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_平定县
Level: 县
Targets: 县委书记 & 县长

Research context:
  - Current leadership roster confirmed from official source: pd.gov.cn/ldzc/ (live site, accessed 2026-07-26)
  - Biographical details: from training data knowledge, NOT independently verified against live web.
  - Exa search API rate-limited; Baidu/BaiduBaike web fetch timed out.
  - Government sub-pages (individual leader profiles) timed out.
  - Labels: "confirmed" for current roster from official source; "plausible"/"unverified" for biographies.
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used by gov_relation.runner
import sys
from datetime import date, datetime
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

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "平定县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_平定县"
if _CURRENT_DIR.name == "shanxi_平定县":
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
# IDs: 1-2 core leadership, 3-9 standing committee, 10-15 county government,
#       16-20 county congress, 21-25 county政协, 26-30 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (confirmed from pd.gov.cn/ldzc/)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "冯玉全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 2,
        "name": "王建源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委领导班子 (confirmed from pd.gov.cn/ldzc/)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "乔勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 4,
        "name": "马卉林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "文杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 6,
        "name": "史纪元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 7,
        "name": "王俊杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "李佩斯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 9,
        "name": "翟瑞庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 10,
        "name": "曹耀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共平定县委",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府 (confirmed from pd.gov.cn/ldzc/)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "郭建勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 12,
        "name": "赵苗怀",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 13,
        "name": "张少波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 14,
        "name": "王耀昌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 15,
        "name": "王强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "平定县人民政府",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县人大 (confirmed from pd.gov.cn/ldzc/)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "乔军华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大党组书记",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 17,
        "name": "王卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 18,
        "name": "刘顺彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 19,
        "name": "侯成军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 20,
        "name": "赵青山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 21,
        "name": "武子房",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "平定县人大常委会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政协 (confirmed from pd.gov.cn/ldzc/)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 22,
        "name": "路海平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协党组书记",
        "current_org": "政协平定县委员会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 23,
        "name": "李有义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协平定县委员会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 24,
        "name": "张锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协平定县委员会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 25,
        "name": "王瑞花",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协平定县委员会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    {
        "id": 26,
        "name": "刘文成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协平定县委员会",
        "source": "http://www.pd.gov.cn/ldzc/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (training data knowledge - UNVERIFIED)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 27,
        "name": "待查（前任县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "",
        "source": "",
    },
    {
        "id": 28,
        "name": "待查（前任县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "",
        "source": "",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共平定县委", "type": "党委", "level": "县级", "parent": "中共阳泉市委", "location": "平定县"},
    {"id": 2, "name": "平定县人民政府", "type": "政府", "level": "县级", "parent": "阳泉市人民政府", "location": "平定县"},
    {"id": 3, "name": "平定县人大常委会", "type": "人大", "level": "县级", "parent": "阳泉市人大常委会", "location": "平定县"},
    {"id": 4, "name": "政协平定县委员会", "type": "政协", "level": "县级", "parent": "政协阳泉市委员会", "location": "平定县"},
    {"id": 5, "name": "平定县纪委监委", "type": "党委", "level": "县级", "parent": "中共平定县委", "location": "平定县"},
    {"id": 6, "name": "中共阳泉市委", "type": "党委", "level": "地市级", "parent": "中共山西省委", "location": "阳泉市"},
    {"id": 7, "name": "阳泉市人民政府", "type": "政府", "level": "地市级", "parent": "山西省人民政府", "location": "阳泉市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 冯玉全 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "当前任职，确认来源：pd.gov.cn/ldzc/"},
    # 王建源 - 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 县委领导班子
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委、副县长"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县政府
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县人大
    {"person_id": 16, "org_id": 3, "title": "党组书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县政协
    {"person_id": 22, "org_id": 4, "title": "党组书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # Predecessors (org connection)
    {"person_id": 27, "org_id": 1, "title": "前任县委书记", "start": "", "end": "unknown", "rank": "正处级", "note": "待查"},
    {"person_id": 28, "org_id": 2, "title": "前任县长", "start": "", "end": "unknown", "rank": "正处级", "note": "待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Core working relationship: 书记 + 县长 (same-period overlap)
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "冯玉全（书记）与王建源（县长）为平定县核心党政搭档",
        "overlap_org": "中共平定县委/平定县人民政府",
        "overlap_period": AS_OF,
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "冯玉全（书记）与乔勇（副书记）为县委领导班子上下级",
        "overlap_org": "中共平定县委",
        "overlap_period": AS_OF,
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "王建源与乔勇同为县委副书记",
        "overlap_org": "中共平定县委",
        "overlap_period": AS_OF,
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "王建源（县长）与李佩斯（副县长）为县政府正副职",
        "overlap_org": "平定县人民政府",
        "overlap_period": AS_OF,
    },
]


# ═════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════
def write_person_json(pid: int, pdata: dict) -> None:
    """Write a person JSON file following the person_graph_json.md schema."""
    name = pdata["name"]
    job = pdata.get("current_post", "").replace("/", "_").replace("、", "_")
    fname = f"{TODAY}-山西省-阳泉市-{job}-{name}.json"
    fpath = PJSON_DIR / fname

    # Determine confidence
    is_placeholder = "待查" in name or not name
    role_conf = "confirmed" if not is_placeholder else "unverified"

    person_record = {
        "schema_version": "1.0",
        "generated_at": str(date.today()),
        "investigation_scope": {
            "province": "山西省",
            "city": "阳泉市",
            "region": "平定县",
            "job": pdata.get("current_post", ""),
            "task_id": "shanxi_平定县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"pingding_{name}",
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
            "administrative_rank": "正处级" if pid in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": role_conf == "confirmed",
            "source_ids": ["S001"]
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
                "summary": "履历信息待查 - 需通过Web搜索补充",
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
            {
                "id": "S001",
                "title": "平定县人民政府 - 领导之窗",
                "url": "http://www.pd.gov.cn/ldzc/",
                "publisher": "平定县人民政府",
                "published_at": "",
                "accessed_at": str(date.today()),
                "source_type": "official",
                "reliability": "high",
                "notes": "确认了当前平定县领导班子全体成员名单"
            }
        ],
        "confidence_summary": {
            "identity": role_conf,
            "current_role": role_conf,
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的出生信息、教育背景、完整履历均需通过Web搜索补充。pd.gov.cn仅列出职务名单，未提供个人详情。"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、民族",
                "why_it_matters": "身份识别和去重的基础信息",
                "suggested_queries": [
                    f"{name} 平定县 简历",
                    f"{name} 百度百科",
                    f"{name} 出生"
                ],
                "last_attempted": str(date.today())
            },
            {
                "priority": "critical",
                "question": f"{name}的完整履历（历任职务、晋升时间、教育背景）",
                "why_it_matters": "关系网络分析和跨县流动追踪的基础",
                "suggested_queries": [
                    f"{name} 任职经历",
                    f"{name} 任前公示",
                    f"阳泉市 平定县 {pdata.get('current_post', '')} {name}"
                ],
                "last_attempted": str(date.today())
            },
            {
                "priority": "high",
                "question": f"{name}的入党时间和参加工作时间",
                "why_it_matters": "评估政治资历和晋升速度",
                "suggested_queries": [
                    f"{name} 入党时间",
                    f"{name} 参加工作"
                ],
                "last_attempted": str(date.today())
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


# ═════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════
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
    write_person_json(1, persons[0])  # 冯玉全
    write_person_json(2, persons[1])  # 王建源

    print(f"\n═══ Done — {SLUG} ═══")
    print(f"  Persons: {len(persons)} ({sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  ✅ Current leadership roster CONFIRMED from pd.gov.cn/ldzc/")
    print(f"  ⚠ Biographical details are unverified (web search unavailable).")
    print(f"  ⚠ Predecessor/successor information is unverified.")
    print(f"  See individual person JSON files and open_gaps.md for priority gaps.")


if __name__ == "__main__":
    main()
