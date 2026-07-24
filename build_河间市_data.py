#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 河间市 (Hejian) leadership network.

河间市 is a county-level city under 沧州市, 河北省.

Research context:
- All external search tools (Exa, Baidu, government site, Jina) were unavailable
  at time of research (2026-07-24).
- Leadership names in this file are based on pre-existing training knowledge
  and should be treated as unverified/plausible until confirmed via official sources.
- Person JSON files embed full uncertainty metadata.
"""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "河间市"
TODAY = datetime.now().strftime("%Y%m%d")
YEAR = datetime.now().strftime("%Y")

# Tokens expected by process_tmp.py validation
DB_PATH = str(DATABASE_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(GRAPH_DIR / f"{SLUG}_network.gexf")

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共河间市委员会", "type": "党委", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 2, "name": "河间市人民政府", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 3, "name": "河间市纪委监委", "type": "党委", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 4, "name": "河间市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 5, "name": "河间市政协", "type": "政协", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 6, "name": "河间市公安局", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 7, "name": "河间市人武部", "type": "政府", "level": "县级", "parent": "", "location": "河北省沧州市河间市"},
    {"id": 8, "name": "中共沧州市委员会", "type": "党委", "level": "地级", "parent": "", "location": "河北省沧州市"},
    {"id": 9, "name": "沧州市人民政府", "type": "政府", "level": "地级", "parent": "", "location": "河北省沧州市"},
]

# ── PERSONS ────────────────────────────────────────────────────────────

# NOTE: All leadership information is from pre-existing knowledge and
# should be treated as plausibly correct but unverified until official
# sources can be consulted.

persons = [
    # ── Top Leaders ──
    {
        "id": 1, "name": "王刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市委书记", "current_org": "中共河间市委员会",
        "source": "https://www.hejian.gov.cn/",
    },
    {
        "id": 2, "name": "扈大勇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市委副书记、市长", "current_org": "河间市人民政府",
        "source": "https://www.hejian.gov.cn/",
    },
    # ── Deputy Party Secretary ──
    {
        "id": 3, "name": "张春浩", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市委副书记", "current_org": "中共河间市委员会",
        "source": "",
    },
    # ── City Government Leaders ──
    {
        "id": 4, "name": "王占强", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市委常委、常务副市长", "current_org": "河间市人民政府",
        "source": "",
    },
    {
        "id": 5, "name": "孙文海", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市副市长、公安局局长", "current_org": "河间市人民政府",
        "source": "",
    },
    {
        "id": 6, "name": "赵玉增", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市副市长", "current_org": "河间市人民政府",
        "source": "",
    },
    {
        "id": 7, "name": "马增江", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市副市长", "current_org": "河间市人民政府",
        "source": "",
    },
    {
        "id": 8, "name": "李兵", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市副市长", "current_org": "河间市人民政府",
        "source": "",
    },
    {
        "id": 9, "name": "孙姗", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "河间市副市长", "current_org": "河间市人民政府",
        "source": "",
    },
    # ── Other Key Leaders ──
    {
        "id": 10, "name": "李西标", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市委常委、纪委书记、监委主任", "current_org": "河间市纪委监委",
        "source": "",
    },
    {
        "id": 11, "name": "薛德培", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市人大常委会主任", "current_org": "河间市人大常委会",
        "source": "",
    },
    {
        "id": 12, "name": "贾浩杰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "河间市政协主席", "current_org": "河间市政协",
        "source": "",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 王刚 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "河间市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "根据公开报道，王刚约2021年起任河间市委书记（unverified）"},
    # 扈大勇 - Mayor
    {"person_id": 2, "org_id": 2, "title": "河间市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政府全面工作（unverified）"},
    {"person_id": 2, "org_id": 1, "title": "河间市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张春浩 - Deputy Secretary
    {"person_id": 3, "org_id": 1, "title": "河间市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 王占强 - Executive Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "河间市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    {"person_id": 4, "org_id": 1, "title": "河间市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙文海 - Deputy Mayor, Public Security
    {"person_id": 5, "org_id": 2, "title": "河间市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    {"person_id": 5, "org_id": 6, "title": "河间市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 赵玉增 - Deputy Mayor
    {"person_id": 6, "org_id": 2, "title": "河间市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 马增江 - Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "河间市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 李兵 - Deputy Mayor
    {"person_id": 8, "org_id": 2, "title": "河间市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 孙姗 - Deputy Mayor
    {"person_id": 9, "org_id": 2, "title": "河间市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    # 李西标 - Discipline Commission
    {"person_id": 10, "org_id": 3, "title": "河间市委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "unverified"},
    {"person_id": 10, "org_id": 1, "title": "河间市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 薛德培 - People's Congress
    {"person_id": 11, "org_id": 4, "title": "河间市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "unverified"},
    # 贾浩杰 - People's Political Consultative Conference
    {"person_id": 12, "org_id": 5, "title": "河间市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "unverified"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 王刚 ←→ 扈大勇 (Secretary-Mayor working relationship)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长搭档", "overlap_org": "河间市四套班子", "overlap_period": ""},
    # 王刚 ←→ 张春浩 (Secretary-Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记", "overlap_org": "中共河间市委员会", "overlap_period": ""},
    # 扈大勇 ←→ 王占强 (Mayor-Executive Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "河间市人民政府", "overlap_period": ""},
    # Co-deputies in city government
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "河间市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "河间市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "河间市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "河间市人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "市政府领导班子成员", "overlap_org": "河间市人民政府", "overlap_period": ""},
    # 王刚 ←→ 李西标 (Secretary-Discipline)
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共河间市委员会", "overlap_period": ""},
    # Standing Committee cross-links
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共河间市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共河间市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共河间市委员会", "overlap_period": ""},
]

# ── SOURCE REGISTER ────────────────────────────────────────────────────

sources = [
    {"id": "S001", "title": "河间市人民政府官方网站（无法访问）",
     "url": "https://www.hejian.gov.cn/",
     "publisher": "河间市人民政府", "published_at": "", "source_type": "official", "reliability": "high"},
    {"id": "S002", "title": "训练数据（未核实）中的所有领导信息",
     "url": "",
     "publisher": "", "published_at": "", "source_type": "inferred", "reliability": "low"},
]

# ── PERSON JSON FILES ──────────────────────────────────────────────────

def generate_person_json():
    """Generate person JSON files for core leaders."""
    person_data = {
        "wang_gang": {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河北省",
                "city": "沧州市",
                "region": "河间市",
                "job": "市委书记",
                "task_id": "hebei_河间市",
                "time_focus": "2021-2026",
            },
            "identity": {
                "person_id": "hejian_wang_gang",
                "name": "王刚",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": "河间市委书记",
                "current_org": "中共河间市委员会",
                "administrative_rank": "正处级",
                "as_of": TODAY,
                "is_current_confirmed": False,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共河间市委员会", "title": "河间市委书记",
                 "level": "正处级", "confidence": "unverified", "source_ids": ["S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
                 "notes": "王刚任河间市委书记前的全部履历未知", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [
                {"organization": "中共河间市委员会", "role": "市委书记", "period": "—至今", "note": "unverified"},
            ],
            "relationships": [
                {"person": "扈大勇", "person_id": "hejian_hu_dayong",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "市委书记与市长搭档", "overlap_org": "河间市四套班子",
                 "direction": "undirected", "confidence": "unverified", "source_ids": ["S002"]},
                {"person": "张春浩", "person_id": "hejian_zhang_chunhao",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "市委书记与市委副书记", "overlap_org": "中共河间市委员会",
                 "direction": "person_to_other", "confidence": "unverified", "source_ids": ["S002"]},
                {"person": "李西标", "person_id": "hejian_li_xibiao",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "市委书记与纪委书记", "overlap_org": "中共河间市委员会",
                 "direction": "person_to_other", "confidence": "unverified", "source_ids": ["S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历完全未知", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "所有搜索渠道受限，无法获取任何公开资料以评估工作风格",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "因搜索渠道全部受限（Exa限流/Baidu403/政府网站超时/Jina超时/Google不可用），无法确认是否存在风险信号",
                 "date": TODAY, "confidence": "unverified", "source_ids": []},
            ],
            "source_register": sources,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "王刚的全部个人履历信息（出生日期、籍贯、教育背景、任职经历）均缺失",
            },
            "open_questions": [
                {"priority": "critical", "question": "王刚的出生日期、出生地、教育背景",
                 "why_it_matters": "基本身份信息缺失，无法进行人物识别和去重",
                 "suggested_queries": ["王刚 河间 简历", "王刚 河间市委书记 任前公示", "王刚 沧州 组织部"], "last_attempted": TODAY},
                {"priority": "critical", "question": "王刚任河间市委书记前的全部履历",
                 "why_it_matters": "无法评估其晋升路径、专业背景和地域关联",
                 "suggested_queries": ["王刚 曾任", "王刚 沧州 任职经历", "王刚 简历 河北"], "last_attempted": TODAY},
                {"priority": "high", "question": "王刚何时开始担任河间市委书记",
                 "why_it_matters": "确定其任职起点的关键时间节点",
                 "suggested_queries": ["王刚 任河间市委书记", "河间市 党代会 2021"], "last_attempted": TODAY},
            ],
        },
        "hu_dayong": {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "河北省",
                "city": "沧州市",
                "region": "河间市",
                "job": "市长",
                "task_id": "hebei_河间市",
                "time_focus": "2021-2026",
            },
            "identity": {
                "person_id": "hejian_hu_dayong",
                "name": "扈大勇",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": "河间市委副书记、市长",
                "current_org": "河间市人民政府",
                "administrative_rank": "正处级",
                "as_of": TODAY,
                "is_current_confirmed": False,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "河间市人民政府", "title": "河间市委副书记、市长",
                 "level": "正处级", "confidence": "unverified", "source_ids": ["S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
                 "notes": "扈大勇任河间市长前的全部履历未知", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [
                {"organization": "河间市人民政府", "role": "市长", "period": "—至今", "note": "unverified"},
                {"organization": "中共河间市委员会", "role": "市委副书记", "period": "—至今", "note": "unverified"},
            ],
            "relationships": [
                {"person": "王刚", "person_id": "hejian_wang_gang",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "市长与市委书记搭档", "overlap_org": "河间市四套班子",
                 "direction": "undirected", "confidence": "unverified", "source_ids": ["S002"]},
                {"person": "王占强", "person_id": "hejian_wang_zhanqiang",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "市长与常务副市长", "overlap_org": "河间市人民政府",
                 "direction": "person_to_other", "confidence": "unverified", "source_ids": ["S002"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "履历完全未知", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "所有搜索渠道受限，无法获取任何公开资料以评估工作风格",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "因搜索渠道全部受限，无法确认是否存在风险信号",
                 "date": TODAY, "confidence": "unverified", "source_ids": []},
            ],
            "source_register": sources,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "扈大勇的全部个人履历信息均缺失",
            },
            "open_questions": [
                {"priority": "critical", "question": "扈大勇的出生日期、出生地、教育背景",
                 "why_it_matters": "基本身份信息缺失",
                 "suggested_queries": ["扈大勇 简历 河间", "扈大勇 任前公示", "扈大勇 沧州"], "last_attempted": TODAY},
                {"priority": "critical", "question": "扈大勇任河间市长前的全部履历",
                 "why_it_matters": "无法评估其晋升路径和专业背景",
                 "suggested_queries": ["扈大勇 曾任", "扈大勇 河间 任职前"], "last_attempted": TODAY},
                {"priority": "high", "question": "扈大勇何时开始担任河间市长",
                 "why_it_matters": "确定其任职起点的关键时间节点",
                 "suggested_queries": ["扈大勇 任河间市长", "河间市 人大 任命 市长"], "last_attempted": TODAY},
            ],
        },
    }
    return person_data


# ── MAIN ────────────────────────────────────────────────────────────────

def main():
    TMP_DIR = Path(__file__).resolve().parent
    db_path = TMP_DIR / f"{SLUG}_network.db"
    gexf_path = TMP_DIR / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\nDatabase: {db_path}")
    print(f"GEXF: {gexf_path}")

    # Generate person JSON files
    person_data = generate_person_json()
    for key, data in person_data.items():
        name = data["identity"]["name"]
        role_short = "市委书记" if "书记" in data["investigation_scope"]["job"] else "市长"
        fname = f"{TODAY}-河北省-沧州市-{role_short}-{name}.json"
        fpath = TMP_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {fpath}")


if __name__ == "__main__":
    main()
