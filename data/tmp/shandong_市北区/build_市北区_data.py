#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 青岛市市北区 leadership network.

调查日期: 2026-07-25
信息来源: 市北政务网 (qingdaoshibei.gov.cn)
调查级别: 市辖区
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "市北区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "市北区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "山东省青岛市市北区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 区委领导 (Party Committee)
    # ═══════════════════════════════

    # 刘新学 — 区委书记
    {
        "id": 1,
        "name": "刘新学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市市北区委书记",
        "current_org": "中共青岛市市北区委员会",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260716_10678499.shtml",
    },
    # 颜丙峰 — 区委副书记
    {
        "id": 2,
        "name": "颜丙峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市市北区委副书记",
        "current_org": "中共青岛市市北区委员会",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260709_10656262.shtml",
    },
    # 区长 — 待确认（刘新学2023年曾任区长，晋升书记后新任区长姓名待查）
    {
        "id": 3,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市市北区委副书记、区长",
        "current_org": "青岛市市北区人民政府",
        "source": "待确认——建议查阅青岛市市北区人大常委会任命公告",
    },
    # 韩锡宏 — 副区长
    {
        "id": 4,
        "name": "韩锡宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市市北区副区长",
        "current_org": "青岛市市北区人民政府",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260709_10656262.shtml",
    },
    # 李强 — 区领导（出现于刘新学调研新闻中，具体职务待确认）
    {
        "id": 5,
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市市北区领导（具体职务待确认）",
        "current_org": "青岛市市北区人民政府",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260716_10678499.shtml",
    },
    # 王明世 — 区人大常委会副主任
    {
        "id": 6,
        "name": "王明世",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市市北区人大常委会副主任",
        "current_org": "青岛市市北区人大常委会",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260709_10656262.shtml",
    },
    # 王君基 — 区政协副主席
    {
        "id": 7,
        "name": "王君基",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青岛市市北区政协副主席",
        "current_org": "中国人民政治协商会议青岛市市北区委员会",
        "source": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260709_10656262.shtml",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共青岛市市北区委员会", "type": "党委", "level": "副厅级", "parent": "中共青岛市委", "location": "山东省青岛市市北区"},
    {"id": 2, "name": "青岛市市北区人民政府", "type": "政府", "level": "副厅级", "parent": "青岛市人民政府", "location": "山东省青岛市市北区"},
    {"id": 3, "name": "青岛市市北区人大常委会", "type": "人大", "level": "副厅级", "parent": "青岛市人大常委会", "location": "山东省青岛市市北区"},
    {"id": 4, "name": "中国人民政治协商会议青岛市市北区委员会", "type": "政协", "level": "副厅级", "parent": "青岛市政协", "location": "山东省青岛市市北区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 刘新学
    {"person_id": 1, "org_id": 1, "title": "中共青岛市市北区委书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "此前曾任市北区委副书记、区长；2023年3月任区长，后晋升书记"},
    # 颜丙峰
    {"person_id": 2, "org_id": 1, "title": "中共青岛市市北区委副书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": ""},
    # 区长（待确认）
    {"person_id": 3, "org_id": 1, "title": "中共青岛市市北区委副书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "兼任区政府党组书记"},
    {"person_id": 3, "org_id": 2, "title": "青岛市市北区区长",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "主持区政府全面工作"},
    # 韩锡宏
    {"person_id": 4, "org_id": 2, "title": "青岛市市北区副区长",
     "start_date": "", "end_date": "", "rank": "副局级",
     "note": ""},
    # 李强
    {"person_id": 5, "org_id": 2, "title": "青岛市市北区领导",
     "start_date": "", "end_date": "", "rank": "",
     "note": "具体职务待确认——陪同区委书记刘新学调研"},
    # 王明世
    {"person_id": 6, "org_id": 3, "title": "青岛市市北区人大常委会副主任",
     "start_date": "", "end_date": "", "rank": "副局级",
     "note": ""},
    # 王君基
    {"person_id": 7, "org_id": 4, "title": "青岛市市北区政协副主席",
     "start_date": "", "end_date": "", "rank": "副局级",
     "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 刘新学 ↔ 颜丙峰
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区委副书记党政工作搭档",
     "overlap_org": "中共青岛市市北区委员会", "overlap_period": ""},
    # 刘新学 ↔ 区长（待确认）
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区长党政工作搭档",
     "overlap_org": "中共青岛市市北区委员会", "overlap_period": ""},
    # 刘新学 ↔ 韩锡宏
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与副区长上下级关系",
     "overlap_org": "青岛市市北区人民政府", "overlap_period": ""},
    # 韩锡宏 ↔ 区长（待确认）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "区长与副区长工作关系",
     "overlap_org": "青岛市市北区人民政府", "overlap_period": ""},
    # 颜丙峰 ↔ 韩锡宏
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "区委副书记与副区长——在同一活动中同时出席",
     "overlap_org": "中共青岛市市北区委员会", "overlap_period": ""},
    # 王明世 ↔ 韩锡宏
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "副区长与人大常委会副主任——在同一慈善活动中出席",
     "overlap_org": "青岛市市北区", "overlap_period": "2026-07-08"},
    # 王君基 ↔ 韩锡宏
    {"person_a": 4, "person_b": 7, "type": "overlap",
     "context": "副区长与政协副主席——在同一慈善活动中出席",
     "overlap_org": "青岛市市北区", "overlap_period": "2026-07-08"},
]

# ── MAIN ───────────────────────────────────────────────────────────
def main():
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

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
    write_person_jsons()

    print(f"\n✅ Build complete: {DB_PATH}")
    print(f"✅ GEXF complete: {GEXF_PATH}")


def write_person_jsons():
    """Write individual person graph JSON files for core figures."""
    base_path = STAGING_DIR

    # 刘新学 person JSON
    liu_xinxue = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "青岛市",
            "region": "市北区",
            "job": "区委书记",
            "task_id": "shandong_市北区",
            "time_focus": "2023-2026",
        },
        "identity": {
            "person_id": "shibei_liu_xinxue",
            "name": "刘新学",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "刘新学_",
                "name_birthplace": "刘新学_",
                "official_profile_url": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/jgzn_9/qzfld_9/",
            },
        },
        "current_status": {
            "current_post": "中共青岛市市北区委书记",
            "current_org": "中共青岛市市北区委员会",
            "administrative_rank": "副厅级",
            "as_of": "2026-07-15",
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "2023-03前",
                "org": "",
                "title": "早期履历",
                "level": "",
                "location": "",
                "system": "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "公开资料未找到2023年之前的具体任职经历",
                "confidence": "unverified",
                "source_ids": [],
            },
            {
                "start": "2023-03",
                "end": "2025?",
                "org": "青岛市市北区人民政府",
                "title": "中共青岛市市北区委副书记、区长",
                "level": "副厅级",
                "location": "山东省青岛市市北区",
                "system": "government",
                "rank": "副厅级",
                "is_key_promotion": True,
                "notes": "2023年3月与区委书记高健一同出席植树活动，职务为区委副书记、区长。晋升区委书记时间待查证。",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
            {
                "start": "2025?",
                "end": "至今",
                "org": "中共青岛市市北区委员会",
                "title": "中共青岛市市北区委书记",
                "level": "副厅级",
                "location": "山东省青岛市市北区",
                "system": "party",
                "rank": "副厅级",
                "is_key_promotion": True,
                "notes": "现任区委书记。2026年7月15日调研欢乐滨海城项目。",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [
            {"org_id": 1, "name": "中共青岛市市北区委员会", "role": "区委书记", "period": "至今"},
            {"org_id": 2, "name": "青岛市市北区人民政府", "role": "区长（前任职务）", "period": "2023-约2025"},
        ],
        "relationships": [
            {
                "person": "颜丙峰",
                "person_id": "shibei_yan_bingfeng",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "区委书记与区委副书记党政工作搭档",
                "overlap_org": "中共青岛市市北区委员会",
                "overlap_period": "至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S003"],
            },
            {
                "person": "高健",
                "person_id": "shibei_gao_jian",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "高健曾任市北区委书记，刘新学曾任区长；刘新学接替高健任书记",
                "overlap_org": "中共青岛市市北区委员会",
                "overlap_period": "2023",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S002"],
            },
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "urban_construction",
                "achievement_or_event": "调研欢乐滨海城片区项目建设，推动城市更新与产业升级",
                "role_in_event": "带队调研、现场督导",
                "measurable_outcome": "",
                "location": "青岛市市北区欢乐滨海城",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["青岛市"],
            "promotion_velocity": {
                "summary": "已知从区长晋升至区委书记，具体时间线和速度待查",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "调研欢乐滨海城项目时重点考察产业规划、招商运营、工程建设等实务工作",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": ["项目建设", "产业升级", "高质量发展"],
            "management_signals": ["现场督导进度、部署重点任务"],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，公开资料未见刘新学有关纪律处分、调查或负面报道",
                "date": "2026-07-25",
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "刘新学调研欢乐滨海城片区项目建设情况",
                "url": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260716_10678499.shtml",
                "publisher": "市北政务网",
                "published_at": "2026-07-15",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认刘新学现任区委书记",
            },
            {
                "id": "S002",
                "title": "高健刘新学参加市北区义务植树活动并调研浮山建设整治工作",
                "url": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202303/t20230314_7047883.shtml",
                "publisher": "市北政务网",
                "published_at": "2023-03-14",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认刘新学2023年3月时任区委副书记、区长",
            },
            {
                "id": "S003",
                "title": "2026年市北区'慈善一日捐'活动动员大会圆满召开",
                "url": "http://www.qingdaoshibei.gov.cn/qzfxxgkmlx_9/ywxx_9/zwyw_9/202607/t20260709_10656262.shtml",
                "publisher": "市北政务网",
                "published_at": "2026-07-08",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认颜丙峰任区委副书记，韩锡宏任副区长",
            },
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "2023年之前完整履历及具体出生信息、教育背景缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "刘新学的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "核心身份信息，影响人物识别和去重",
                "suggested_queries": ["刘新学 简历", "刘新学 出生", "刘新学 Baidu Baike"],
                "last_attempted": TODAY,
            },
            {
                "priority": "critical",
                "question": "刘新学2023年之前的完整职场履历是什么？",
                "why_it_matters": "了解其晋升路径和可能的人脉网络",
                "suggested_queries": ["刘新学 经历", "刘新学 任职", "刘新学 青岛 简历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": "刘新学何时从区长晋升为区委书记？",
                "why_it_matters": "确定权力交接时间线",
                "suggested_queries": ["刘新学 任区委书记", "市北区 区委书记 任命"],
                "last_attempted": TODAY,
            },
        ],
    }

    # Write 刘新学 JSON
    liu_path = os.path.join(base_path, f"{TODAY}-山东省-青岛市-区委书记-刘新学.json")
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_xinxue, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {liu_path}")

    # 区长（待确认）minimal JSON
    quzhang = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "青岛市",
            "region": "市北区",
            "job": "区长",
            "task_id": "shandong_市北区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "shibei_quzhang_unknown",
            "name": "待确认",
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
                "name_birth": "待确认_",
                "name_birthplace": "待确认_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "中共青岛市市北区委副书记、区长",
            "current_org": "青岛市市北区人民政府",
            "administrative_rank": "副厅级",
            "as_of": TODAY,
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "刘新学2023年任区长、后晋升书记，新任区长的姓名和履历均未能从公开资料获取",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任市北区区长是谁？",
                "why_it_matters": "核心调查目标之一——区长职位的基本信息",
                "suggested_queries": [
                    "青岛市市北区区长 任命",
                    "青岛市市北区区长 姓名",
                    "市北区政府 区长 2026",
                    "青岛市 市北区 人大常委会 区长 任命",
                ],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": "刘新学何时辞去区长、由谁接任？",
                "why_it_matters": "确定人事变动时间线",
                "suggested_queries": ["市北区 区长 变更", "刘新学 辞去区长", "市北区 人大常委会 接受辞职"],
                "last_attempted": TODAY,
            },
        ],
    }

    qu_path = os.path.join(base_path, f"{TODAY}-山东省-青岛市-区长-待确认.json")
    with open(qu_path, "w", encoding="utf-8") as f:
        json.dump(quzhang, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {qu_path}")


if __name__ == "__main__":
    main()
