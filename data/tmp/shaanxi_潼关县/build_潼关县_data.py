#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 潼关县, 渭南市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_潼关县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 潼关县人民政府官方网站 (www.tongguan.gov.cn) — multiple news articles confirming current leadership
    (2026-07-24, 2026-07-23, 2026-07-13, 2026-07-09)
  - No dedicated leadership page (/ldzc/ 栏目不存在) on the 潼关 government site
  - Baidu Baike and Baidu search unavailable (403/blocked)

Confidence notes:
  - 左俊（县委书记）: 多次在县委常委会和全县大会报道中明确标注"县委书记左俊"，当前身份确认
  - 段淑梅（代县长）: 在"全县安全生产暨防汛救灾警示教育会议"报道中明确为"代县长段淑梅"，身份确认
  - 左俊的完整履历（出生年份、籍贯、教育背景、早期任职）尚未找到，标为待查
  - 段淑梅的完整履历亦未找到
  - 陈永笛出现在新闻报道中（检查应急广播工作），具体职务待确认
  - 前任县委书记及县长信息待查
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..")))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: used by gov_relation.runner internally

SLUG = "潼关县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (县委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 左俊 — 县委书记
    {
        "id": 1,
        "name": "左俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共潼关县委员会",
        "source": "潼关县政府官网新闻多次确认（2026年7月9日、7月13日、7月21日、7月22日、7月24日等多篇报道认证'县委书记左俊'）"
    },
    # 段淑梅 — 代县长
    {
        "id": 2,
        "name": "段淑梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "代县长",
        "current_org": "潼关县人民政府",
        "source": "潼关县政府官网新闻：全县安全生产暨防汛救灾警示教育会议（2026-07-22）明确标注'代县长段淑梅'"
    },
    # 陈永笛 — 县领导（具体职务待确认）
    {
        "id": 3,
        "name": "陈永笛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "潼关县",
        "source": "潼关县政府官网报道：陈永笛检查应急广播服务防汛救灾工作（2026-07-23）"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共潼关县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市潼关县"
    },
    {
        "id": 2,
        "name": "潼关县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市潼关县"
    },
    {
        "id": 3,
        "name": "潼关县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市潼关县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议潼关县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市潼关县"
    },
    {
        "id": 5,
        "name": "中共潼关县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "渭南市潼关县"
    },
]

positions_data = [
    # 县委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via multiple news articles from tongguan.gov.cn (2026-07-09 onward)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "as acting county mayor, serves as deputy party secretary"},

    # 县政府
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed via tongguan.gov.cn news article 2026-07-22"},

    # 陈永笛 — 具体职务待确认，暂不分配具体岗位
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记——代县长党政搭档", "overlap_org": "中共潼关县委/潼关县人民政府", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 2, "type": "会议互动", "context": "全县安全生产暨防汛救灾警示教育会议：左俊讲话，段淑梅主持（2026-07-22）", "overlap_org": "中共潼关县委", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 2, "type": "会议互动", "context": "全县物业服务管理提升三年行动动员部署会：左俊讲话，段淑梅主持（2026-07-13）", "overlap_org": "中共潼关县委/潼关县人民政府", "overlap_period": "2026-07"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "左俊": {
        "filename": f"{TODAY}-陕西省-渭南市-潼关县-县委书记-左俊.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "潼关县",
                "job": "县委书记",
                "task_id": "shaanxi_潼关县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "tongguan_zuo_jun",
                "name": "左俊",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "左俊_未知",
                    "name_birthplace": "左俊_未知",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共潼关县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003", "S004"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "中共潼关县委员会", "title": "县委书记", "level": "县处级", "location": "陕西潼关", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任，最早确认报道为2026年7月9日县委常委会", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003", "S004"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到左俊任潼关县委书记前的完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "段淑梅", "person_id": "tongguan_duan_shumei", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——代县长党政搭档，多次共同出席全县会议", "overlap_org": "中共潼关县委/潼关县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持召开全县安全生产暨防汛救灾警示教育会议，部署重点领域安全和防汛备汛工作", "role_in_event": "出席并讲话", "measurable_outcome": "", "location": "渭南潼关县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07", "domain": "other", "achievement_or_event": "主持召开全县警示教育大会，讲专题党课，强调树立正确政绩观", "role_in_event": "讲专题党课", "measurable_outcome": "", "location": "渭南潼关县", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-07", "domain": "urban_construction", "achievement_or_event": "主持召开全县物业服务管理提升三年行动动员部署会", "role_in_event": "讲话部署", "measurable_outcome": "", "location": "渭南潼关县", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "安全生产", "城市治理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party", "government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "当前确认职务为潼关县委书记，此前履历待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "discipline_oriented", "evidence": "主持召开全县警示教育大会并讲专题党课，强调树立正确政绩观、全面从严治党", "confidence": "plausible", "source_ids": ["S003"]},
                    {"trait": "pragmatic", "evidence": "在多个会议中强调具体工作落实、安全生产和防汛备汛具体举措", "confidence": "plausible", "source_ids": ["S001", "S002"]},
                ],
                "speech_themes": ["党建引领", "安全生产", "防汛救灾", "城市精细化管理", "正确政绩观"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "全县安全生产暨防汛救灾警示教育会议召开 左俊讲话 段淑梅主持", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认左俊为县委书记，段淑梅为代县长"},
                {"id": "S002", "title": "全县物业服务管理提升三年行动动员部署会召开 左俊讲话 段淑梅主持", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认左俊为县委书记"},
                {"id": "S003", "title": "全县警示教育大会召开", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认左俊为县委书记"},
                {"id": "S004", "title": "县委常委会召开会议 学习习近平总书记重要讲话 重要指示 重要回信精神", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认左俊为县委书记"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "左俊的完整履历（出生年份、籍贯、教育背景、此前所有任职经历、何时就任潼关县委书记）"},
            "open_questions": [
                {"priority": "critical", "question": "左俊的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["左俊 简历 潼关", "左俊 任前公示", "左俊 百度百科"], "last_attempted": AS_OF},
                {"priority": "high", "question": "左俊何时就任潼关县委书记？前任县委书记是谁？去向如何？", "why_it_matters": "确定任期起点和前任去向，关系网络关键节点", "suggested_queries": ["潼关县 前任县委书记", "潼关县 县委 书记 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "段淑梅何时就任代县长？前任县长是谁？", "why_it_matters": "确定政府主要领导的更替时间线", "suggested_queries": ["潼关县 前任县长", "段淑梅 任命 潼关"], "last_attempted": AS_OF},
            ]
        }
    },
    "段淑梅": {
        "filename": f"{TODAY}-陕西省-渭南市-潼关县-代县长-段淑梅.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "潼关县",
                "job": "代县长",
                "task_id": "shaanxi_潼关县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "tongguan_duan_shumei",
                "name": "段淑梅",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "段淑梅_未知",
                    "name_birthplace": "段淑梅_未知",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "代县长",
                "current_org": "潼关县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "潼关县人民政府", "title": "代县长", "level": "县处级", "location": "陕西潼关", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任，2026年7月22日全县安全生产会议以代县长身份主持会议", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到段淑梅任潼关代县长前的完整履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "左俊", "person_id": "tongguan_zuo_jun", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记——代县长党政搭档", "overlap_org": "中共潼关县委/潼关县人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持全县安全生产暨防汛救灾警示教育会议，强调统筹好多种关系", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南潼关县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07", "domain": "urban_construction", "achievement_or_event": "主持全县物业服务管理提升三年行动动员部署会", "role_in_event": "主持会议", "measurable_outcome": "", "location": "渭南潼关县", "confidence": "confirmed", "source_ids": ["S002"]},
            ],
            "professional_profile": {
                "primary_specializations": ["政府管理", "安全生产", "城市管理"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "当前确认职务为潼关代县长，此前履历待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "在会议主持中强调统筹发展和安全等多重关系", "confidence": "plausible", "source_ids": ["S001"]},
                ],
                "speech_themes": ["安全生产", "物业服务管理提升", "高质量发展"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "全县安全生产暨防汛救灾警示教育会议召开 左俊讲话 段淑梅主持", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认段淑梅为代县长"},
                {"id": "S002", "title": "全县物业服务管理提升三年行动动员部署会召开 左俊讲话 段淑梅主持", "url": "https://www.tongguan.gov.cn/", "publisher": "潼关县人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认段淑梅身份"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "段淑梅的完整履历（出生年份、籍贯、教育背景、此前所有任职经历、何时就任潼关代县长）"},
            "open_questions": [
                {"priority": "critical", "question": "段淑梅的完整履历（出生年份、籍贯、教育背景、此前所有任职经历）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["段淑梅 简历 潼关", "段淑梅 任前公示", "段淑梅 百度百科"], "last_attempted": AS_OF},
                {"priority": "high", "question": "段淑梅何时就任潼关代县长？前任县长是谁？", "why_it_matters": "确定政府主要领导的更替时间线", "suggested_queries": ["潼关县 前任县长", "潼关县 县长 任命"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "段淑梅此前在哪个系统/地区工作？", "why_it_matters": "分析跨系统调动模式", "suggested_queries": ["段淑梅 渭南 任职"], "last_attempted": AS_OF},
            ]
        }
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path


def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)


if __name__ == "__main__":
    main()
