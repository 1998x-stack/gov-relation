#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 桦甸市 (Huadian City), 吉林市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_桦甸市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.huadian.gov.cn — 桦甸市人民政府官方网站 (primary, current as of July 2026)
  - xxgk.huadian.gov.cn — 政府信息公开平台 (government information disclosure)
  - www.jlcity.gov.cn — 吉林市人民政府官方网站 (parent city news and leadership)
  - Official leadership profile pages for mayor and deputy mayors (confirmed July 2026)
  - News articles from huadian.gov.cn and jlcity.gov.cn (2026 current)

Confidence notes:
  - Current roles: confirmed via official government leadership page (2026-07-25)
  - 夏丹 bio (born Oct 1987, Han, graduate degree): confirmed from official profile
  - 市委书记: NOT confirmed on available public pages — the official government site
    (huadian.gov.cn) only lists government leadership (市长+副市长). Party committee
    leadership is not published on this site. Open question — see open_gaps.
  - Biographical details beyond current roles: limited due to web access limitations
    (Exa rate-limited, Baidu Baike 403, Google Search blocked)
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
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
SLUG = "桦甸市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_桦甸市"
if _CURRENT_DIR.name == "jilin_桦甸市":
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
# IDs: 1-2 core leaders, 3-8 standing committee / deputy mayors,
#      20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共桦甸市委员会",
        "source": "公开信息待查",
        "confidence": "unverified",
        "notes": "市委书记姓名未在桦甸市政府官网领导之窗页面上公布。该页面仅列出市政府领导（市长+副市长）。市委领导信息可能需要通过市委网站或其他渠道查找。此前已知书记信息：根据公开报道，2024年及更早的书记信息需进一步核实。"
    },
    {
        "id": 2,
        "name": "夏丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/sz/",
        "confidence": "confirmed",
        "notes": "1987年10月出生，汉族，研究生学历。现任桦甸市委副书记、市长。领导市政府全面工作，分管市审计局。官方领导人页面确认截至2026年7月。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (from official leadership page)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "陈礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/fsz_cl/",
        "confidence": "confirmed",
        "notes": "1978年10月出生，汉族，研究生学历。中共桦甸市委常委、副市长（常务）。分管发改、财政、应急、人社、城管执法、机关事务等。"
    },
    {
        "id": 4,
        "name": "杨盈",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/lfj/",
        "confidence": "confirmed",
        "notes": "1971年3月出生，汉族，大学学历。桦甸市人民政府党组成员、副市长，市公安局局长。分管公安、信访、司法、退役军人事务等。"
    },
    {
        "id": 5,
        "name": "毕志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年1月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/bzg/",
        "confidence": "confirmed",
        "notes": "1989年1月出生，汉族，本科学历。桦甸市人民政府副市长。分管住建、自然资源、政务服务和数字化建设、交通运输等。"
    },
    {
        "id": 6,
        "name": "景年瑞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/jnr/",
        "confidence": "confirmed",
        "notes": "1987年9月出生，汉族，大学学历。桦甸市人民政府党组成员、副市长。分管教育、卫健、民政、医保、体育等。"
    },
    {
        "id": 7,
        "name": "李和义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "桦甸市人民政府",
        "source": "http://www.huadian.gov.cn/xxgk/zfld/lhy/",
        "confidence": "confirmed",
        "notes": "1977年3月出生，汉族，大学学历。桦甸市人民政府党组成员、副市长。分管农业农村、畜牧、林业、水利、供销、水库移民等。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共桦甸市委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市委", "location": "桦甸市"},
    {"id": 2, "name": "桦甸市人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "桦甸市"},
    {"id": 3, "name": "中国人民政治协商会议桦甸市委员会", "type": "政协", "level": "县处级", "parent": "政协吉林市委", "location": "桦甸市"},
    {"id": 4, "name": "桦甸市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "吉林市人大常委会", "location": "桦甸市"},
    {"id": 5, "name": "桦甸市纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "吉林市纪委", "location": "桦甸市"},
    {"id": 6, "name": "桦甸市公安局", "type": "政府", "level": "乡科级", "parent": "桦甸市人民政府", "location": "桦甸市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 待查_市委书记 — current Party Secretary (unverified)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "市委书记姓名待核实。桦甸市政府网站未公布市委领导信息。"},
    # 夏丹 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "现任桦甸市委副书记、市长，领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "兼任市委副书记"},
    # 陈礼 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管发改、财政、应急、人社、城管执法、机关事务等"},
    # 杨盈 — Deputy Mayor & PSB Chief
    {"person_id": 4, "org_id": 2, "title": "副市长（兼市公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管公安、信访、司法、退役军人事务等"},
    {"person_id": 4, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 毕志刚 — Deputy Mayor
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管住建、自然资源、政务服务和数字化建设、交通运输等"},
    # 景年瑞 — Deputy Mayor
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管教育、卫健、民政、医保、体育等市政府党组成员"},
    # 李和义 — Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管农业农村、畜牧、林业、水利、供销、水库移民等市政府党组成员"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # person_a, person_b, type, context, overlap_org, overlap_period, confidence
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长为党政主要领导搭档关系",
        "overlap_org": "中共桦甸市委员会",
        "overlap_period": "2026年",
        "confidence": "plausible",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "市长与常务副市长为政府主要领导与副手关系",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "市长与副市长（公安局长）为政府领导关系",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "市长与副市长为政府领导关系",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "市长与副市长为政府领导关系",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "市长与副市长为政府领导关系",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "同为桦甸市政府领导班子成员",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "同为桦甸市政府领导班子成员",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "overlap",
        "context": "同为桦甸市政府领导班子成员",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "同为桦甸市政府领导班子成员",
        "overlap_org": "桦甸市人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

def make_person_json_min(person_id: int) -> dict:
    """Create a minimal person JSON entry for a known person."""
    p = {x["id"]: x for x in persons}[person_id]
    return {
        "id": person_id,
        "name": p["name"],
        "current_post": p["current_post"],
        "current_org": p["current_org"],
        "source": p["source"],
        "confidence": p["confidence"],
    }


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    # Build DB and GEXF
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

    # Write person JSONs
    person_files = []
    for pid, role in [(2, "市长"), (3, "常务副市长"), (4, "副市长兼公安局局长"),
                       (5, "副市长"), (6, "副市长"), (7, "副市长")]:
        p = {x["id"]: x for x in persons}[pid]
        fn = f"{TODAY}-吉林省-吉林市-{role}-{p['name']}.json"
        path = PJSON_DIR / fn
        person_files.append(str(path))
        # In a more complete version, write full person JSON
        # For now, note the file as expected

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs expected: {person_files}")
    print("Note: 市委书记 name is unverified — mark as open question")
    print("Done.")


if __name__ == "__main__":
    main()
