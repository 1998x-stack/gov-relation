#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 塔河县 (Tahe County), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_塔河县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.dxalth.gov.cn/ (塔河县人民政府官网) — official leadership page (confirmed as-of 2026-07-24)
  - http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml — 领导之窗 (complete roster)
  - http://www.dxalth.gov.cn/dxalth/c101048/list.shtml — 塔河要闻 news articles confirming activities

Confidence notes:
  - 李宁 (县委书记): confirmed via official leadership page and multiple news articles (2026-07-13 bicycle race prep, flood control inspection)
  - 任英寰 (县长): confirmed via official leadership page and multiple news articles (2026-07-21 project inspection, flood control meeting)
  - Full leadership roster (县委常委、政府、人大、政协): confirmed via official 领导之窗 page
  - Career histories for both leaders: unverified — only current positions confirmed from official sources
  - Birth details, education, party join dates for all leaders: unverified
  - Exa search was rate-limited; Baidu returned CAPTCHA
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "塔河县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "李宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 2,
        "name": "任英寰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    # ═══════ 县委常委 ═══════
    {
        "id": 3,
        "name": "于艳清",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共塔河县纪律检查委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 4,
        "name": "王丽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共塔河县委组织部",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 5,
        "name": "李建平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共塔河县委宣传部",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 6,
        "name": "张春霖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    # ═══════ 县政府领导班子 ═══════
    {
        "id": 7,
        "name": "郭宝福",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 8,
        "name": "王宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 9,
        "name": "王连义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 10,
        "name": "刘文涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长候选人",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 11,
        "name": "杨炳辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副处级干部",
        "current_org": "塔河县人民政府",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    # ═══════ 人大 ═══════
    {
        "id": 12,
        "name": "刘桂兰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "塔河县人大常务委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 13,
        "name": "栾建华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "塔河县人大常务委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 14,
        "name": "盛之英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "塔河县人大常务委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 15,
        "name": "周瑞峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "塔河县人大常务委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    # ═══════ 政协 ═══════
    {
        "id": 16,
        "name": "胡艳丽",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 17,
        "name": "包爱萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 18,
        "name": "丁良宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 19,
        "name": "王大利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
    {
        "id": 20,
        "name": "刘作益",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协秘书长",
        "current_org": "政协塔河县委员会",
        "source": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共塔河县委员会", "type": "党委", "level": "县级", "parent": "中共大兴安岭地区委员会", "location": "塔河县"},
    {"id": 2, "name": "塔河县人民政府", "type": "政府", "level": "县级", "parent": "大兴安岭地区行政公署", "location": "塔河县"},
    {"id": 3, "name": "中共塔河县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共大兴安岭地区纪律检查委员会", "location": "塔河县"},
    {"id": 4, "name": "中共塔河县委组织部", "type": "党委", "level": "县级", "parent": "中共塔河县委员会", "location": "塔河县"},
    {"id": 5, "name": "中共塔河县委宣传部", "type": "党委", "level": "县级", "parent": "中共塔河县委员会", "location": "塔河县"},
    {"id": 6, "name": "塔河县人大常务委员会", "type": "人大", "level": "县级", "parent": "大兴安岭地区人大工作委员会", "location": "塔河县"},
    {"id": 7, "name": "政协塔河县委员会", "type": "政协", "level": "县级", "parent": "政协大兴安岭地区委员会", "location": "塔河县"},
    {"id": 8, "name": "塔河县公安局", "type": "政府", "level": "县级", "parent": "塔河县人民政府", "location": "塔河县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 李宁
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持县委全面工作"},
    # 任英寰
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作"},
    # 于艳清
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "四级高级监察官"},
    # 王丽
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "党校（行政学校）第一副校长"},
    # 李建平
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张春霖
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 郭宝福
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王宇
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王连义
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 8, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "公安局党委书记"},
    # 刘文涛
    {"person_id": 10, "org_id": 2, "title": "副县长候选人", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨炳辉
    {"person_id": 11, "org_id": 2, "title": "副处级干部", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘桂兰
    {"person_id": 12, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 栾建华
    {"person_id": 13, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 盛之英
    {"person_id": 14, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 周瑞峰
    {"person_id": 15, "org_id": 6, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 胡艳丽
    {"person_id": 16, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 包爱萍
    {"person_id": 17, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 丁良宇
    {"person_id": 18, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王大利
    {"person_id": 19, "org_id": 7, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘作益
    {"person_id": 20, "org_id": 7, "title": "县政协秘书长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 李宁 ↔ 任英寰（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "李宁任县委书记，任英寰任县长，为塔河县党政正职搭档", "overlap_org": "塔河县", "overlap_period": ""},
    # 李宁 ↔ 于艳清（县委常委班子）
    {"person_a": 1, "person_b": 3, "type": "县委常委班子", "context": "于艳清任县委常委、纪委书记，李宁为县委书记", "overlap_org": "中共塔河县委员会", "overlap_period": ""},
    # 李宁 ↔ 王丽（县委常委班子）
    {"person_a": 1, "person_b": 4, "type": "县委常委班子", "context": "王丽任县委常委、组织部部长，李宁为县委书记", "overlap_org": "中共塔河县委员会", "overlap_period": ""},
    # 李宁 ↔ 李建平（县委常委班子）
    {"person_a": 1, "person_b": 5, "type": "县委常委班子", "context": "李建平任县委常委、宣传部部长，李宁为县委书记", "overlap_org": "中共塔河县委员会", "overlap_period": ""},
    # 李宁 ↔ 张春霖（县委常委班子）
    {"person_a": 1, "person_b": 6, "type": "县委常委班子", "context": "张春霖任县委常委、副县长，李宁为县委书记", "overlap_org": "中共塔河县委员会", "overlap_period": ""},
    # 任英寰 ↔ 张春霖（政府班子）
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "张春霖任副县长，任英寰为县长", "overlap_org": "塔河县人民政府", "overlap_period": ""},
    # 任英寰 ↔ 郭宝福（政府班子）
    {"person_a": 2, "person_b": 7, "type": "政府班子", "context": "郭宝福任副县长，任英寰为县长", "overlap_org": "塔河县人民政府", "overlap_period": ""},
    # 任英寰 ↔ 王宇（政府班子）
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "王宇任副县长，任英寰为县长", "overlap_org": "塔河县人民政府", "overlap_period": ""},
    # 任英寰 ↔ 王连义（政府班子）
    {"person_a": 2, "person_b": 9, "type": "政府班子", "context": "王连义任副县长、公安局局长，任英寰为县长", "overlap_org": "塔河县人民政府", "overlap_period": ""},
    # 任英寰 ↔ 刘文涛（政府班子）
    {"person_a": 2, "person_b": 10, "type": "政府班子", "context": "刘文涛任副县长候选人，任英寰为县长", "overlap_org": "塔河县人民政府", "overlap_period": ""},
]

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    person_files = [
        {
            "id": 1,
            "name": "李宁",
            "job": "县委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "大兴安岭地区",
                    "region": "塔河县",
                    "job": "县委书记",
                    "task_id": "heilongjiang_塔河县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "tahe_lining",
                    "name": "李宁",
                    "gender": "",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "",
                    "work_start": "",
                },
                "current_status": {
                    "current_post": "县委书记",
                    "current_org": "中共塔河县委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "present",
                        "org": "中共塔河县委员会",
                        "title": "塔河县委书记",
                        "level": "正处级",
                        "location": "塔河县",
                        "system": "party",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "任英寰",
                        "person_id": "tahe_renyinghuan",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "李宁任县委书记，任英寰任县长，为塔河县党政正职搭档",
                        "overlap_org": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "调研指导2026年大兴安岭·塔河第八届全国森林自行车赛筹备工作，实地踏查赛道全程",
                        "role_in_event": "调研指导",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "调研督导防汛备汛工作",
                        "role_in_event": "调研督导",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "other",
                        "achievement_or_event": "讲授树立和践行正确政绩观学习教育专题党课",
                        "role_in_event": "讲授",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S004"]
                    },
                    {
                        "period": "2026-06",
                        "domain": "other",
                        "achievement_or_event": "走访慰问离休老干部、因公殉职党员干部家属",
                        "role_in_event": "走访慰问",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S005"]
                    },
                ],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "多次深入一线调研防汛、重大项目、赛事筹备等现场工作",
                            "confidence": "plausible",
                            "source_ids": ["S002", "S003"]
                        }
                    ],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "No risk signals found in public records as of 2026-07-24",
                        "date": "",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {"id": "S001", "title": "塔河县领导之窗", "url": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml", "publisher": "塔河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Official leadership roster"},
                    {"id": "S002", "title": "塔河县委书记李宁调研指导自行车赛筹备工作", "url": "http://www.dxalth.gov.cn/dxalth/c101048/202607/c13_341191.shtml", "publisher": "塔河县人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming role"},
                    {"id": "S003", "title": "塔河县委书记李宁调研督导防汛备汛工作", "url": "http://www.dxalth.gov.cn/dxalth/c101048/202607/c13_341189.shtml", "publisher": "塔河县人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming role"},
                    {"id": "S004", "title": "塔河县委书记李宁讲授专题党课", "url": "http://www.dxalth.gov.cn/dxalth/c101048/list.shtml", "publisher": "塔河县人民政府", "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News listing referencing 李宁"},
                    {"id": "S005", "title": "塔河县委书记李宁走访慰问", "url": "http://www.dxalth.gov.cn/dxalth/c101048/list.shtml", "publisher": "塔河县人民政府", "published_at": "2026-06-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News listing referencing 李宁"},
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "Full career history, education, birth details unknown"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "李宁的完整履历（出生年月、籍贯、教育背景、历任职务）",
                        "why_it_matters": "县委书记是该县最高领导，完整履历对理解其晋升路径和关系网络至关重要",
                        "suggested_queries": ["李宁 塔河 简历", "李宁 大兴安岭 任职经历"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "李宁何时到任塔河县委书记",
                        "why_it_matters": "到任时间影响党政搭档关系时间线",
                        "suggested_queries": ["李宁 任塔河县委书记"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "前任县委书记是谁、去向如何",
                        "why_it_matters": "前任去向可揭示人事调动模式和权力结构",
                        "suggested_queries": ["塔河县 前任县委书记"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "任英寰",
            "job": "县长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "大兴安岭地区",
                    "region": "塔河县",
                    "job": "县长",
                    "task_id": "heilongjiang_塔河县",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "tahe_renyinghuan",
                    "name": "任英寰",
                    "gender": "",
                    "ethnicity": "",
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "",
                    "work_start": "",
                },
                "current_status": {
                    "current_post": "县长",
                    "current_org": "塔河县人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S006"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "present",
                        "org": "塔河县人民政府",
                        "title": "塔河县委副书记、县长",
                        "level": "正处级",
                        "location": "塔河县",
                        "system": "government",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "李宁",
                        "person_id": "tahe_lining",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "任英寰任县长，李宁任县委书记，为塔河县党政正职搭档",
                        "overlap_org": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-07",
                        "domain": "urban_construction",
                        "achievement_or_event": "调研全县重点项目建设及安全生产工作，督导老旧楼房供热管道改造、学校消防设施建设、道路改建、热电升级改造等民生项目",
                        "role_in_event": "调研督导",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S006"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "组织召开2026年塔河县防汛工作推进会议并调研督导防汛备汛工作",
                        "role_in_event": "会议组织、调研督导",
                        "location": "塔河县",
                        "confidence": "confirmed",
                        "source_ids": ["S007"]
                    },
                ],
                "professional_profile": {
                    "primary_specializations": ["urban_construction"],
                    "secondary_specializations": ["public_security"],
                    "career_pattern": "unknown",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "深入重点项目施工现场督导民生基建工作，关注民生细节如供热、校园安全、道路改建",
                            "confidence": "plausible",
                            "source_ids": ["S006"]
                        }
                    ],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [
                    {
                        "type": "none_found",
                        "description": "No risk signals found in public records as of 2026-07-24",
                        "date": "",
                        "confidence": "plausible",
                        "source_ids": []
                    }
                ],
                "source_register": [
                    {"id": "S001", "title": "塔河县领导之窗", "url": "http://www.dxalth.gov.cn/dxalth/c100910/leaders.shtml", "publisher": "塔河县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Official leadership roster"},
                    {"id": "S006", "title": "塔河县委副书记、县长任英寰调研全县重点项目建设及安全生产工作", "url": "http://www.dxalth.gov.cn/dxalth/c101048/202607/c13_341861.shtml", "publisher": "塔河县人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming role and governance record"},
                    {"id": "S007", "title": "塔河县委副书记、县长任英寰组织召开防汛工作推进会议", "url": "http://www.dxalth.gov.cn/dxalth/c101048/202607/c13_341097.shtml", "publisher": "塔河县人民政府", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming role"},
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "Full career history, education, birth details unknown"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "任英寰的完整履历（出生年月、籍贯、教育背景、历任职务）",
                        "why_it_matters": "县长是该县行政一把手，完整履历对理解其能力和关系网络至关重要",
                        "suggested_queries": ["任英寰 简历", "任英寰 大兴安岭"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "任英寰何时到任塔河县长",
                        "why_it_matters": "到任时间影响党政搭档关系时间线",
                        "suggested_queries": ["任英寰 任塔河县长"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "前任县长是谁、去向如何",
                        "why_it_matters": "前任去向可揭示人事调动模式",
                        "suggested_queries": ["塔河县 前任县长"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
    ]

    for pf in person_files:
        filename = f"{TODAY}-黑龙江省-大兴安岭地区-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")

    print(f"\n✅ Build complete: {SLUG}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
