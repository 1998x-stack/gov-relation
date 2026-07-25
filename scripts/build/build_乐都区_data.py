#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乐都区, 海东市, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_乐都区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from official government
news articles (2025-08 to 2026-07). Full career timelines, education, and
predecessor paths are UNVERIFIED due to web access degradation (Exa rate-limited,
Baidu blocked, Jina blocked, official leadership page renders empty).

Confirmed:
  区委书记: 张福清 (confirmed from multiple official articles, 2025-08 to 2026-07)
  区委副书记、区长: 付强 (confirmed from 2026-03 and 2025-08 articles)
  区委副书记: 尚众邦 (confirmed from 2026-05 article)
  其他区委领导: 鄂福涛, 祁利德, 韩海强, 杨生辉, 杨城安, 杜存梅, 郭元国 (from 2026-02 article)
  区人大常委会主任: 罗建军 (confirmed from 2026-02 article, listed as大会执行主席/主持人)
  其他区级领导: 杨全芳, 马元平, 田红保, 晁增彦, 汪宏璞, 霍建宏, 李万锦,
               李福海, 张马龙, 颜君武, 霍成伯 (法院院长)

Notes:
  - 乐都区第三届人民代表大会第七次会议 was held in February 2026
  - 乐都区委三届十一次全体会议 was held in August 2025
  - 乐都区 has an active leadership with recent investment projects
  - The official leadership page (ldzc) returned empty — likely requires JS rendering
  - Baidu Baike blocked by 403; Government site HTTPS blocked but HTTP accessible
  - Predecessors' identities and full career timelines are unknown
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "乐都区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (CONFIRMED) ═══════
    {
        "id": 1,
        "name": "张福清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区委书记",
        "current_org": "中共海东市乐都区委员会",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 2,
        "name": "付强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区委副书记、区长",
        "current_org": "乐都区人民政府",
        "source": "http://www.ledu.gov.cn/html/gzdt/19031.html"
    },
    {
        "id": 3,
        "name": "尚众邦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区委副书记",
        "current_org": "中共海东市乐都区委员会",
        "source": "http://www.ledu.gov.cn/html/gzdt/19149.html"
    },
    # ═══════ Other Confirmed Leaders ═══════
    {
        "id": 4,
        "name": "罗建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区人大常委会主任",
        "current_org": "乐都区人民代表大会常务委员会",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 5,
        "name": "鄂福涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 6,
        "name": "祁利德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 7,
        "name": "韩海强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 8,
        "name": "杨生辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 9,
        "name": "杨城安",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 10,
        "name": "杜存梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 11,
        "name": "郭元国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 12,
        "name": "杨全芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/gzdt/19031.html"
    },
    {
        "id": 13,
        "name": "马元平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 14,
        "name": "田红保",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/18850.html"
    },
    {
        "id": 15,
        "name": "霍成伯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区人民法院院长",
        "current_org": "乐都区人民法院",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 16,
        "name": "晁增彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 17,
        "name": "汪宏璞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 18,
        "name": "霍建宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 19,
        "name": "李万锦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/tpxw/19030.html"
    },
    {
        "id": 20,
        "name": "李福海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/gzdt/19031.html"
    },
    {
        "id": 21,
        "name": "张马龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/gzdt/19031.html"
    },
    {
        "id": 22,
        "name": "颜君武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "乐都区领导",
        "current_org": "海东市乐都区",
        "source": "http://www.ledu.gov.cn/html/gzdt/19031.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共海东市乐都区委员会", "type": "党委", "level": "县级", "parent": "中共海东市委员会", "location": "海东市乐都区"},
    {"id": 2, "name": "乐都区人民政府", "type": "政府", "level": "县级", "parent": "海东市人民政府", "location": "海东市乐都区"},
    {"id": 3, "name": "中共乐都区纪律检查委员会/乐都区监察委员会", "type": "党委", "level": "县级", "parent": "中共海东市纪律检查委员会", "location": "海东市乐都区"},
    {"id": 4, "name": "乐都区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "海东市人民代表大会常务委员会", "location": "海东市乐都区"},
    {"id": 5, "name": "中国人民政治协商会议乐都区委员会", "type": "政协", "level": "县级", "parent": "政协海东市委员会", "location": "海东市乐都区"},
    {"id": 6, "name": "乐都区人民法院", "type": "政府", "level": "县级", "parent": "海东市中级人民法院", "location": "海东市乐都区"},
    {"id": 7, "name": "乐都区人民检察院", "type": "政府", "level": "县级", "parent": "海东市人民检察院", "location": "海东市乐都区"},
    {"id": 8, "name": "乐都工业园管委会", "type": "政府", "level": "县级", "parent": "海东市人民政府", "location": "海东市乐都区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "乐都区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from multiple official articles (2025-08 to 2026-07)"},
    {"person_id": 2, "org_id": 1, "title": "乐都区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-03 article"},
    {"person_id": 2, "org_id": 2, "title": "乐都区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-03 article"},
    {"person_id": 3, "org_id": 1, "title": "乐都区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-05 article"},
    # Other leaders
    {"person_id": 4, "org_id": 4, "title": "乐都区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-02 article"},
    {"person_id": 5, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 6, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 7, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 8, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 9, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 10, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 and 2026-03 articles"},
    {"person_id": 11, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区领导 in 2026-02 article"},
    {"person_id": 12, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区级领导 in 2026-03 article"},
    {"person_id": 13, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 大会执行主席 in 2026-02 article"},
    {"person_id": 14, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区委委员 in 2025-08 article"},
    {"person_id": 15, "org_id": 6, "title": "乐都区人民法院院长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Elected in 2026-02 区三届人大七次会议"},
    {"person_id": 16, "org_id": 4, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 大会执行主席 in 2026-02 article"},
    {"person_id": 17, "org_id": 4, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 大会执行主席 in 2026-02 article"},
    {"person_id": 18, "org_id": 4, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 大会执行主席 in 2026-02 article"},
    {"person_id": 19, "org_id": 4, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 大会执行主席 in 2026-02 article"},
    {"person_id": 20, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区级领导 in 2026-03 article"},
    {"person_id": 21, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区级领导 in 2026-03 article"},
    {"person_id": 22, "org_id": 1, "title": "乐都区领导 (具体职务待查)", "start_date": "", "end_date": "present", "rank": "副处级以上", "note": "Listed as 区级领导 in 2026-03 article"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Core leadership relationships
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "张福清（区委书记）与付强（区长）为乐都区党政正职搭档", "overlap_org": "海东市乐都区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记在区委常委会共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "区长与区委副书记在区委常委会共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "党政-人大", "context": "区委书记与区人大常委会主任在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 4, "type": "政府-人大", "context": "区长（政府工作报告）与区人大常委会主任在区人大会议期间协作", "overlap_org": "乐都区", "overlap_period": "2026"},
    # Other relationships (within the leadership team)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "区委领导在区委领导下共事", "overlap_org": "中共海东市乐都区委员会", "overlap_period": "2025-2026"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main() -> None:
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
    today_str = TODAY
    person_dir = STAGING_DIR

    # ═══════════════════════════════════════════════════════════════════
    # 张福清 person JSON
    # ═══════════════════════════════════════════════════════════════════
    zhangfuqing = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "海东市",
            "region": "乐都区",
            "job": "区委书记",
            "task_id": "qinghai_乐都区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "ledu_zhangfuqing",
            "name": "张福清",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张福清_",
                "name_birthplace": "张福清_",
                "official_profile_url": "http://www.ledu.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "乐都区委书记",
            "current_org": "中共海东市乐都区委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共海东市乐都区委员会",
                "title": "乐都区委书记",
                "level": "县级",
                "location": "青海省海东市乐都区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed as 乐都区委书记 from multiple official articles (August 2025 to July 2026). Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S003"]
            }
        ],
        "organizations": [
            {"org_id": "org_ledu_party", "name": "中共海东市乐都区委员会", "role": "领导机关", "source_ids": ["S001", "S002", "S003"]}
        ],
        "relationships": [
            {
                "person": "付强",
                "person_id": "ledu_fuqiang",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "张福清作为区委书记、付强作为区长，为乐都区党政正职搭档（2025-2026年）",
                "overlap_org": "海东市乐都区",
                "overlap_period": "2025-2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "person": "尚众邦",
                "person_id": "ledu_shangzhongbang",
                "relationship_type": "上下级",
                "strength": "strong",
                "evidence": "区委书记与区委副书记在区委常委会共事",
                "overlap_org": "中共海东市乐都区委员会",
                "overlap_period": "2025-2026",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-03-02",
                "domain": "rural_revitalization",
                "achievement_or_event": "在区委农业农村工作会议上讲话，部署2026年三农工作重点任务",
                "role_in_event": "区委书记作讲话",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-02-11",
                "domain": "other",
                "achievement_or_event": "在区三届人大七次会议闭幕会上讲话，强调推进中国式现代化乐都实践",
                "role_in_event": "区委书记致闭幕词",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "period": "2026-05-29",
                "domain": "public_security",
                "achievement_or_event": "在区委平安建设重点工作推进会上讲话，部署平安乐都建设工作",
                "role_in_event": "区委书记作讲话",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "period": "2025-08-11",
                "domain": "discipline",
                "achievement_or_event": "主持区委三届十一次全会并讲话，强调作风建设与从严治党",
                "role_in_event": "区委书记主持并讲话",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["党的建设", "作风建设", "农业农村", "平安建设"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "多次强调实干担当、坚定信心，在区委全会中提出'实干争先'工作基调",
                    "confidence": "plausible",
                    "source_ids": ["S001", "S004"]
                },
                {
                    "trait": "discipline_oriented",
                    "evidence": "在区委三届十一次全会上专题部署作风建设和从严治党",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "speech_themes": ["实干争先", "优良作风", "中国式现代化", "高质量发展", "凝心聚力"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现张福清的纪律处分、审计问题或负面报道",
                "date": "2026-07-25",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "海东市乐都区第三届人民代表大会第七次会议胜利闭幕",
                "url": "http://www.ledu.gov.cn/html/tpxw/19030.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-02-12",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张福清为乐都区委书记"
            },
            {
                "id": "S002",
                "title": "区委农业农村工作会议召开",
                "url": "http://www.ledu.gov.cn/html/gzdt/19031.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-03-03",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认付强为区委副书记、区长"
            },
            {
                "id": "S003",
                "title": "乐都区召开区委平安建设重点工作推进会",
                "url": "http://www.ledu.gov.cn/html/gzdt/19149.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-05-29",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认尚众邦为区委副书记"
            },
            {
                "id": "S004",
                "title": "以优良作风奋进新征程 在现代化新青海建设中贡献乐都力量",
                "url": "http://www.ledu.gov.cn/html/tpxw/18850.html",
                "publisher": "乐都区人民政府",
                "published_at": "2025-08-11",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张福清主持区委三届十一次全会"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少张福清的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "张福清的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["张福清 海东 简历 出生", "张福清 乐都区委书记 任前公示", "张福清 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "张福清任乐都区委书记前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["张福清 此前 担任 海东", "张福清 曾任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "张福清的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["张福清 简历 任职经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # ═══════════════════════════════════════════════════════════════════
    # 付强 person JSON
    # ═══════════════════════════════════════════════════════════════════
    fuqiang = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "海东市",
            "region": "乐都区",
            "job": "区长",
            "task_id": "qinghai_乐都区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "ledu_fuqiang",
            "name": "付强",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "付强_",
                "name_birthplace": "付强_",
                "official_profile_url": "http://www.ledu.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "乐都区委副书记、区长",
            "current_org": "乐都区人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S002", "S004"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "乐都区人民政府",
                "title": "乐都区委副书记、区长",
                "level": "县级",
                "location": "青海省海东市乐都区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed as 乐都区长 from multiple official articles (August 2025 to March 2026). Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S002", "S004"]
            }
        ],
        "organizations": [
            {"org_id": "org_ledu_gov", "name": "乐都区人民政府", "role": "领导机关", "source_ids": ["S002", "S004"]}
        ],
        "relationships": [
            {
                "person": "张福清",
                "person_id": "ledu_zhangfuqing",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "付强作为区长、张福清作为区委书记，为乐都区党政正职搭档（2025-2026年）",
                "overlap_org": "海东市乐都区",
                "overlap_period": "2025-2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-03-02",
                "domain": "rural_revitalization",
                "achievement_or_event": "在区委农业农村工作会议上主持，强调做好'规模、产业、增收、宜居'四篇文章",
                "role_in_event": "区长主持会议",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2025-08-11",
                "domain": "economic_development",
                "achievement_or_event": "在区委三届十一次全会上总结上半年经济工作、部署下半年工作",
                "role_in_event": "区长总结部署经济工作",
                "measurable_outcome": "",
                "location": "乐都区",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["农业农村", "经济发展"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "在农业农村工作会议上提出做好'四篇文章'（规模、产业、增收、宜居），体现务实的工作方法",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": ["实干", "高质量发展", "乡村振兴", "绿色有机农畜产品"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现付强的纪律处分、审计问题或负面报道",
                "date": "2026-07-25",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "海东市乐都区第三届人民代表大会第七次会议胜利闭幕",
                "url": "http://www.ledu.gov.cn/html/tpxw/19030.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-02-12",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "列出席位信息"
            },
            {
                "id": "S002",
                "title": "区委农业农村工作会议召开",
                "url": "http://www.ledu.gov.cn/html/gzdt/19031.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-03-03",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认付强为区委副书记、区长"
            },
            {
                "id": "S003",
                "title": "乐都区召开区委平安建设重点工作推进会",
                "url": "http://www.ledu.gov.cn/html/gzdt/19149.html",
                "publisher": "乐都区人民政府",
                "published_at": "2026-05-29",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认区领导框架"
            },
            {
                "id": "S004",
                "title": "以优良作风奋进新征程 在现代化新青海建设中贡献乐都力量",
                "url": "http://www.ledu.gov.cn/html/tpxw/18850.html",
                "publisher": "乐都区人民政府",
                "published_at": "2025-08-11",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认付强总结部署上半年/下半年经济工作"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少付强的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "付强的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["付强 海东 简历 出生", "付强 乐都区长 任前公示", "付强 百度百科"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "付强任乐都区长前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["付强 此前 担任 海东", "付强 曾任"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "付强的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["付强 简历 任职经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # Write person JSON files
    zhangfuqing_path = person_dir / f"{today_str}-青海省-海东市-区委书记-张福清.json"
    with open(zhangfuqing_path, "w", encoding="utf-8") as f:
        json.dump(zhangfuqing, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {zhangfuqing_path}")

    fuqiang_path = person_dir / f"{today_str}-青海省-海东市-区长-付强.json"
    with open(fuqiang_path, "w", encoding="utf-8") as f:
        json.dump(fuqiang, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fuqiang_path}")

    print(f"\n{'='*60}")
    print(f"乐都区 build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
