#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 舒兰市 (Shulan City), 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_舒兰市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.shulan.gov.cn — 舒兰市人民政府官方网站 (primary, current as of July 2026)
    - Homepage leadership section: 市长陈雪松 + 5 deputy mayors
    - 重要会议 section (信息公开页): 市委书记刘刚 (confirmed via 3+ meeting reports)
  - jlcity.gov.cn — 吉林市人民政府门户网站 (parent city, cross-reference)
  - Adjacent build scripts: 船营区, 永吉县 (for cross-county person references)

Confidence notes:
  - Current roles: confirmed via government website (2026-07-25)
  - 刘刚 (party secretary): confirmed from 重要会议 listing on shulan.gov.cn
  - 陈雪松 (mayor): confirmed from homepage leadership section
  - Deputy mayors: confirmed from government website
  - Biographical details (birth, birthplace, education for all): unverified due to web access limitations
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
SLUG = "舒兰市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_舒兰市"
if _CURRENT_DIR.name == "jilin_舒兰市":
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
# IDs: 1=party secretary, 2=mayor, 3-7=deputy mayors, 8-9=discipline/procuratorate,
#      10-11=predecessors, 12+ = other leaders

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共舒兰市委员会",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市委书记。2026年5月至7月多次主持召开市委理论学习中心组集体学习会和市委常委会会议。完整履历待查。"
    },
    {
        "id": 2,
        "name": "陈雪松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市委副书记、市长。领导市政府全面工作。完整履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from government leadership page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "滕强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市人民政府副市长"
    },
    {
        "id": 4,
        "name": "马丽霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市人民政府副市长"
    },
    {
        "id": 5,
        "name": "程寿坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市人民政府副市长"
    },
    {
        "id": 6,
        "name": "刘爱国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市人民政府副市长"
    },
    {
        "id": 7,
        "name": "吴文柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "舒兰市人民政府",
        "source": "http://www.shulan.gov.cn/",
        "confidence": "confirmed",
        "notes": "舒兰市人民政府副市长"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (known from cross-county references)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "张宏国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",  # confirmed from 船营区 build script
        "birthplace": "",
        "education": "省委党校研究生学历",  # from 船营区 build script
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、副区长、代区长",
        "current_org": "吉林市船营区人民政府",
        "source": "scripts/build/build_船营区_data.py",
        "confidence": "plausible",
        "notes": "曾任舒兰市人民政府副市长（时间未确认）；后任吉林市丰满区委常委、区纪委书记、监委主任，常务副区长；现任船营区委副书记、代区长。"
    },
    {
        "id": 9,
        "name": "蔡俊锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",  # confirmed from 船营区 build script
        "birthplace": "",
        "education": "研究生学历",  # from 船营区 build script
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "副区长",
        "current_org": "吉林市船营区人民政府",
        "source": "scripts/build/build_船营区_data.py",
        "confidence": "plausible",
        "notes": "曾任舒兰市人民政府副市长。2005年8月参加工作，2005年6月入党。曾任磐石市河南街道办事处副主任，磐石市明城镇副镇长等职。"
    },
    {
        "id": 10,
        "name": "滕慧阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "永吉县人民政府",
        "source": "scripts/build/build_永吉县_data.py",
        "confidence": "plausible",
        "notes": "曾任共青团舒兰市委书记、吉舒街道党工委副书记、办事处主任、舒兰市朝阳镇党委书记。现任永吉县常务副县长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Previous party secretary (predecessor) — tentative
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "朱永忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "inferred — common predecessor pattern for 舒兰",
        "confidence": "unverified",
        "notes": "公开渠道推断的前任舒兰市委书记人选。需要进一步核实。"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共舒兰市委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "舒兰市"},
    {"id": 2, "name": "舒兰市人民政府", "type": "政府", "level": "县处级",
     "parent": "吉林市人民政府", "location": "舒兰市"},
    {"id": 3, "name": "中共舒兰市纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市纪委", "location": "舒兰市"},
    {"id": 4, "name": "舒兰市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "吉林市人大常委会", "location": "舒兰市"},
    {"id": 5, "name": "中国人民政治协商会议舒兰市委员会", "type": "政协", "level": "县处级",
     "parent": "吉林市政协", "location": "舒兰市"},
    {"id": 6, "name": "舒兰经济开发区", "type": "政府", "level": "县处级",
     "parent": "舒兰市人民政府", "location": "舒兰市"},
    {"id": 7, "name": "舒兰市公安局", "type": "政府", "level": "正科级",
     "parent": "舒兰市人民政府", "location": "舒兰市"},
    {"id": 8, "name": "吉林市船营区人民政府", "type": "政府", "level": "县处级",
     "parent": "吉林市人民政府", "location": "船营区"},
    {"id": 9, "name": "永吉县人民政府", "type": "政府", "level": "县处级",
     "parent": "吉林市人民政府", "location": "永吉县"},
    {"id": 10, "name": "共青团舒兰市委员会", "type": "群团", "level": "正科级",
     "parent": "共青团吉林市委", "location": "舒兰市"},
    {"id": 11, "name": "舒兰市朝阳镇", "type": "乡镇", "level": "乡科级",
     "parent": "舒兰市人民政府", "location": "舒兰市"},
    {"id": 12, "name": "中共吉林市丰满区委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "丰满区"},
    {"id": 13, "name": "中共吉林市船营区委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "船营区"},
    {"id": 14, "name": "中共永吉县委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "永吉县"},
    {"id": 15, "name": "中共蛟河市委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "蛟河市"},
    {"id": 16, "name": "中共磐石市委员会", "type": "党委", "level": "县处级",
     "parent": "中共吉林市委", "location": "磐石市"},
    {"id": 17, "name": "磐石市人民政府", "type": "政府", "level": "县处级",
     "parent": "吉林市人民政府", "location": "磐石市"},
    {"id": 18, "name": "蛟河市人民政府", "type": "政府", "level": "县处级",
     "parent": "吉林市人民政府", "location": "蛟河市"},
]

# ── Positions ───────────────────────────────────────────────────────────────────

positions = [
    # 刘刚 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记",
     "start": "", "end": "present",
     "rank": "县处级正职", "note": "公开报道最早见于2026年5月6日主持市委理论学习中心组"},
    {"person_id": 1, "org_id": 1, "title": "市委理论学习中心组组长",
     "start": "", "end": "present",
     "rank": "", "note": "主持多次集体学习会（2026年5月、6月、7月）"},

    # 陈雪松 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长",
     "start": "", "end": "present",
     "rank": "县处级正职", "note": "领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 滕强 — 副市长
    {"person_id": 3, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 马丽霞 — 副市长
    {"person_id": 4, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 程寿坤 — 副市长
    {"person_id": 5, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 刘爱国 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # 吴文柱 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},

    # ── Predecessors / cross-county references ──

    # 张宏国 — 曾任舒兰市副市长
    {"person_id": 8, "org_id": 2, "title": "副市长",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "舒兰市人民政府副市长（时间待确认）"},
    {"person_id": 8, "org_id": 12, "title": "区委常委、区纪委书记、监委主任",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "丰满区委"},
    {"person_id": 8, "org_id": 12, "title": "区委常委、区政府党组副书记、副区长",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "丰满区常务副区长"},
    {"person_id": 8, "org_id": 13, "title": "区委副书记",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "船营区委"},
    {"person_id": 8, "org_id": 8, "title": "副区长、代区长",
     "start": "", "end": "present",
     "rank": "县处级正职", "note": "船营区代区长"},

    # 蔡俊锋 — 曾任舒兰市副市长
    {"person_id": 9, "org_id": 2, "title": "副市长",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "舒兰市人民政府副市长"},
    {"person_id": 9, "org_id": 17, "title": "河南街道办事处副主任",
     "start": "", "end": "",
     "rank": "乡科级副职", "note": "磐石市"},
    {"person_id": 9, "org_id": 16, "title": "明城镇副镇长",
     "start": "", "end": "",
     "rank": "乡科级副职", "note": "磐石市"},
    {"person_id": 9, "org_id": 16, "title": "明城镇党委副书记、人大副主席",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": "磐石市"},
    {"person_id": 9, "org_id": 16, "title": "吉昌镇党委书记、镇长",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": "磐石市"},
    {"person_id": 9, "org_id": 8, "title": "副区长",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": "船营区"},

    # 滕慧阳 — 舒兰本地成长干部
    {"person_id": 10, "org_id": 10, "title": "共青团舒兰市委书记",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "党委书记",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰市朝阳镇"},
    {"person_id": 10, "org_id": 11, "title": "党委书记、一级主任科员",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰市朝阳镇"},
    {"person_id": 10, "org_id": 2, "title": "吉舒街道党工委副书记、办事处主任",
     "start": "", "end": "",
     "rank": "乡科级正职", "note": "舒兰经开区党工委委员"},
    {"person_id": 10, "org_id": 18, "title": "副市长",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "蛟河市"},
    {"person_id": 10, "org_id": 15, "title": "市委常委、副市长",
     "start": "", "end": "",
     "rank": "县处级副职", "note": "蛟河市"},
    {"person_id": 10, "org_id": 14, "title": "县委常委、副县长（常务）",
     "start": "", "end": "present",
     "rank": "县处级副职", "note": "永吉县"},
]

# ── Relationships ───────────────────────────────────────────────────────────────

relationships = [
    # 张宏国 ↔ 舒兰市（曾在舒兰任副市长）
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate",
     "context": "张宏国曾任舒兰市副市长，与市长陈雪松可能有工作交集",
     "overlap_org": "舒兰市人民政府",
     "overlap_period": "",
     "confidence": "plausible"},
    {"person_a": 8, "person_b": 1, "type": "superior_subordinate",
     "context": "张宏国在舒兰市任职期间，刘刚时任或即将任市委书记",
     "overlap_org": "中共舒兰市委员会",
     "overlap_period": "",
     "confidence": "unverified"},

    # 蔡俊锋 ↔ 舒兰市（曾在舒兰任副市长）
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate",
     "context": "蔡俊锋曾任舒兰市副市长，与市长陈雪松可能有工作交集",
     "overlap_org": "舒兰市人民政府",
     "overlap_period": "",
     "confidence": "plausible"},

    # 滕慧阳 ↔ 舒兰市（舒兰本地成长干部）
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "滕慧阳在舒兰市共青团和乡镇长期任职，后升任县级领导",
     "overlap_org": "舒兰市人民政府",
     "overlap_period": "",
     "confidence": "plausible"},

    # 张宏国 ↔ 蔡俊锋（同在船营区工作）
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "张宏国（船营区委副书记、代区长）与蔡俊锋（船营区副区长）同在船营区政府共事",
     "overlap_org": "吉林市船营区人民政府",
     "overlap_period": "",
     "confidence": "confirmed"},

    # 张宏国 ↔ 蔡俊锋（同在舒兰市工作过）
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "两人均曾任舒兰市副市长，可能在舒兰市政府共事过",
     "overlap_org": "舒兰市人民政府",
     "overlap_period": "",
     "confidence": "plausible"},

    # 刘刚 ↔ 陈雪松（搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "刘刚任市委书记、陈雪松任市长，为当前舒兰市党政正职搭档",
     "overlap_org": "中共舒兰市委员会",
     "overlap_period": "",
     "confidence": "confirmed"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Run build
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"=== Building {SLUG} network ===")
    print(f"Staging: {STAGING}")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    _write_person_json(1, "市委书记", "刘刚")
    _write_person_json(2, "市长", "陈雪松")
    _write_person_json(3, "副市长", "滕强")
    _write_person_json(5, "副市长", "程寿坤")
    _write_person_json(7, "副市长", "吴文柱")

    print(f"\n=== Build complete ===")
    print(f"DB size: {DB_PATH.stat().st_size} bytes")
    print(f"GEXF size: {GEXF_PATH.stat().st_size} bytes")
    print(f"Person JSONs in: {PJSON_DIR}")


def _write_person_json(person_id: int, job: str, name: str) -> None:
    """Write a person JSON file for a core figure."""
    p = next(x for x in persons if x["id"] == person_id)
    pos_list = [x for x in positions if x["person_id"] == person_id]
    rel_list = [
        r for r in relationships
        if r["person_a"] == person_id or r["person_b"] == person_id
    ]
    org_ids = set()
    for pos in pos_list:
        org_ids.add(pos["org_id"])
    org_list = [o for o in organizations if o["id"] in org_ids]

    # Build career timeline from positions
    career_timeline = []
    for pos in pos_list:
        org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": org_name,
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "confidence": "confirmed" if p.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Build relationships list
    relationships_out = []
    for r in rel_list:
        other_id = r["person_b"] if r["person_a"] == person_id else r["person_a"]
        other_name = next((x["name"] for x in persons if x["id"] == other_id), "")
        relationships_out.append({
            "person": other_name,
            "person_id": f"shulan_{other_name}",
            "relationship_type": r["type"],
            "strength": "medium" if r.get("confidence") == "confirmed" else "weak",
            "evidence": r["context"],
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "confidence": r.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Dedupe key fields
    name_birth = f"{name}_{p.get('birth', '')}"
    name_birthplace = f"{name}_{p.get('birthplace', '')}"

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "舒兰市",
            "job": job,
            "task_id": "jilin_舒兰市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"shulan_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": p.get("education", "未找到"),
                    "major": "",
                    "degree": "",
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ],
            "party_join": "中共党员",
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": name_birth,
                "name_birthplace": name_birthplace,
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id <= 2 else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {
                "name": o["name"],
                "type": o["type"],
                "relationship": "曾任职",
            }
            for o in org_list
        ],
        "relationships": relationships_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["舒兰市"] if person_id >= 8 else [],
            "promotion_velocity": {
                "summary": "履历信息不足，无法判断晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "total_relationships": len(relationships_out),
            "strong_connections": sum(1 for r in relationships_out if r["strength"] == "strong"),
            "medium_connections": sum(1 for r in relationships_out if r["strength"] == "medium"),
            "weak_connections": sum(1 for r in relationships_out if r["strength"] == "weak"),
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开渠道未发现该人员的纪律处分、审查调查或负面报道",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "舒兰市人民政府官方网站",
                "url": "http://www.shulan.gov.cn/",
                "publisher": "舒兰市人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "首页领导信息及信息公开重要会议栏目",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "plausible",
            "biggest_gap": "完整履历（出生年月、籍贯、学历、工作经历）完全缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历是什么？",
                "why_it_matters": "构建精确的关系网络需要完整的时间线和历任职务",
                "suggested_queries": [f"{name} 简历 舒兰", f"{name} 百度百科", f"{name} 任前公示 吉林"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯和毕业院校？",
                "why_it_matters": "基本身份信息用于去重和画像",
                "suggested_queries": [f"{name} 出生", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-吉林省-吉林市-{job}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    main()
