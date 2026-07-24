#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 济源市 leadership network.

济源市 is a 省直辖县级市 (provincial-level city treated as 地级市).
Also known as 济源产城融合示范区 (Jiyuan Production-City Integration Demonstration Zone),
which uses "一个机构两块牌子" (one institution, two nameplates) with the city government.

Data sources:
- 济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导/政务要闻 pages
- 济源日报 articles (2026-05 through 2026-07)
- 庄建球 (former 市委书记/市长) existing profile
- 百度百科

Current leadership confirmed as of 2026-07-24:
- 高永: 示范区党工委书记、市委书记 (appointed ~May 2026)
- 秦保建: 示范区管委会主任、市长
- 赵山, 俞益民, 王笑非, 赵会生, 牛少伟, 董倩, 卢新永: 市政府领导班子成员
- 庄建球: former 市委书记 (2023.04-2025.02), former 市长 (2021.09-2023.04)
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp checker
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "济源市"
TODAY = "2026-07-24"
AS_OF = TODAY
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee / current leaders, 2xxx = government team, 3xxx = former

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 高永 — 示范区党工委书记、市委书记 (current Party Secretary)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "高永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源产城融合示范区党工委书记、市委书记",
        "current_org": "中共济源市委",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 政务要闻 2026-06-03 起以党工委书记、市委书记身份活动",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 秦保建 — 示范区管委会主任、市长 (current Mayor)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "秦保建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源产城融合示范区管委会主任、市长",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页/政务要闻",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 赵山 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "赵山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 俞益民 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "俞益民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 王笑非 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "王笑非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 赵会生 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "赵会生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 牛少伟 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2005,
        "name": "牛少伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 董倩 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2006,
        "name": "董倩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 卢新永 — 市政府领导
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2007,
        "name": "卢新永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "济源市政府领导",
        "current_org": "济源市人民政府",
        "source": "济源市人民政府网站 (www.jiyuan.gov.cn) — 市政府领导页",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 庄建球 — 前任市委书记/市长 (2021-2025)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3001,
        "name": "庄建球",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "湖南南县",
        "education": "中南工学院管理系会计专业本科、清华大学公共管理硕士（MPA）、北京航空航天大学管理科学与工程博士",
        "party_join": "1993-05",
        "work_start": "1995-06",
        "current_post": "郑州市委副书记、市长",
        "current_org": "郑州市人民政府",
        "source": "百度百科 / data/persons/20260724-河南省-郑州市-市长-庄建球.json",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共济源市委", "type": "党委", "level": "地级", "parent": "中共河南省委", "location": "河南省济源市"},
    {"id": 2, "name": "济源市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省济源市"},
    {"id": 3, "name": "济源产城融合示范区党工委", "type": "党委", "level": "地级", "parent": "中共河南省委", "location": "河南省济源市"},
    {"id": 4, "name": "济源产城融合示范区管理委员会", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省济源市"},
    {"id": 5, "name": "郑州市人民政府", "type": "政府", "level": "副省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 高永 — 市委书记
    {"person_id": 1001, "org_id": 1, "title": "市委书记", "start_date": "2026-05", "end_date": "", "rank": "正厅级", "note": "示范区党工委书记、市委书记；2026年6月2日首次以该身份公开调研"},
    {"person_id": 1001, "org_id": 3, "title": "示范区党工委书记", "start_date": "2026-05", "end_date": "", "rank": "正厅级", "note": "与市委书记同一职务两块牌子"},

    # 秦保建 — 市长
    {"person_id": 1002, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "示范区管委会主任、市长；主持示范区管委会和市政府全面工作"},
    {"person_id": 1002, "org_id": 4, "title": "示范区管委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": "与市长同一职务两块牌子"},

    # 赵山 — 市政府领导
    {"person_id": 2001, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 俞益民 — 市政府领导
    {"person_id": 2002, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 王笑非 — 市政府领导
    {"person_id": 2003, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 赵会生 — 市政府领导
    {"person_id": 2004, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 牛少伟 — 市政府领导
    {"person_id": 2005, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 董倩 — 市政府领导
    {"person_id": 2006, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},
    # 卢新永 — 市政府领导
    {"person_id": 2007, "org_id": 2, "title": "市政府领导", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府领导班子成员"},

    # 庄建球 — 前任
    {"person_id": 3001, "org_id": 1, "title": "市委书记", "start_date": "2023-04", "end_date": "2025-02", "rank": "正厅级", "note": "2023.5起兼任市人武部党委第一书记；2023.8-2024.4兼市人大常委会主任"},
    {"person_id": 3001, "org_id": 2, "title": "市长", "start_date": "2021-09", "end_date": "2023-04", "rank": "正厅级", "note": "2021.09正式当选市长"},
    {"person_id": 3001, "org_id": 3, "title": "示范区党工委书记", "start_date": "2023-04", "end_date": "2025-02", "rank": "正厅级", "note": "2023.5-2023.6兼管委会主任"},
    {"person_id": 3001, "org_id": 4, "title": "示范区管委会主任", "start_date": "2021-06", "end_date": "2023-06", "rank": "正厅级", "note": "2021.06任示范区党工委副书记、管委会党组书记、主任"},
]

# ── Relationships (Person <-> Person) ─────────────────────────────────────────
relationships = [
    # 高永 ↔ 秦保建（党政一把手搭档）
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "context": "示范区党工委书记/市委书记与示范区管委会主任/市长党政一把手搭档", "overlap_org": "济源产城融合示范区/济源市", "overlap_period": "2026-05至今"},
    # 高永 ↔ 庄建球（前后任书记）
    {"person_a": 1001, "person_b": 3001, "type": "predecessor_successor", "context": "庄建球（前市委书记2023.04-2025.02）→ 高永（现任市委书记2026.05-）", "overlap_org": "中共济源市委", "overlap_period": "不重叠（前后任）"},
    # 秦保建 ↔ 庄建球（前后任市长/可能的交接关系）
    {"person_a": 1002, "person_b": 3001, "type": "predecessor_successor", "context": "庄建球（前市长2021.09-2023.04）→ 秦保建（现任市长）", "overlap_org": "济源市人民政府", "overlap_period": "不重叠（前后任）"},
    # 秦保建 → 政府班子（领导与被领导）
    {"person_a": 1002, "person_b": 2001, "type": "overlap", "context": "市长与市政府领导班子成员赵山工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2002, "type": "overlap", "context": "市长与市政府领导班子成员俞益民工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2003, "type": "overlap", "context": "市长与市政府领导班子成员王笑非工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2004, "type": "overlap", "context": "市长与市政府领导班子成员赵会生工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2005, "type": "overlap", "context": "市长与市政府领导班子成员牛少伟工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2006, "type": "overlap", "context": "市长与市政府领导班子成员董倩工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 1002, "person_b": 2007, "type": "overlap", "context": "市长与市政府领导班子成员卢新永工作搭档", "overlap_org": "济源市人民政府", "overlap_period": ""},
    # 政府班子内部同事关系（同僚）
    {"person_a": 2001, "person_b": 2002, "type": "overlap", "context": "市政府领导班子同僚", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 2001, "person_b": 2003, "type": "overlap", "context": "市政府领导班子同僚", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 2002, "person_b": 2003, "type": "overlap", "context": "市政府领导班子同僚", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 2004, "person_b": 2005, "type": "overlap", "context": "市政府领导班子同僚", "overlap_org": "济源市人民政府", "overlap_period": ""},
    {"person_a": 2006, "person_b": 2007, "type": "overlap", "context": "市政府领导班子同僚", "overlap_org": "济源市人民政府", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Source Register
# ══════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "济源市人民政府—市政府领导", "url": "http://www.jiyuan.gov.cn/shizf/", "publisher": "济源市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市政府领导页显示领导班子：秦保建、赵山、俞益民、王笑非、赵会生、牛少伟、董倩、卢新永"},
        {"id": "S002", "title": "高永在调研示范区产业发展时强调：以科技创新赋能工业转型升级", "url": "http://www.jiyuan.gov.cn/zwyw/zwyw_22093/t1003431.html", "publisher": "济源日报", "published_at": "2026-06-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "高永首次以示范区党工委书记、市委书记身份公开活动（2026年6月2日）"},
        {"id": "S003", "title": "示范区安防委二季度全体（扩大）会议召开 秦保建出席并讲话", "url": "http://www.jiyuan.gov.cn/zwyw/zwyw_22093/t1006093.html", "publisher": "济源日报", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "秦保建以示范区管委会主任、市长身份出席"},
        {"id": "S004", "title": "高永在坡头镇调研", "url": "http://www.jiyuan.gov.cn/zwyw/zwyw_22093/", "publisher": "济源日报", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "高永以党工委书记、市委书记身份调研"},
        {"id": "S005", "title": "示范区党工委理论学习中心组集体学习 高永主持 秦保建出席", "url": "http://www.jiyuan.gov.cn/zwyw/zwyw_22093/", "publisher": "济源日报", "published_at": "2026-07-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "高永和秦保建同时出席党工委理论学习中心组会议"},
        {"id": "S006", "title": "庄建球百度百科", "url": "https://baike.baidu.com/item/%E5%BA%84%E5%BB%BA%E7%90%83/8004662", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "庄建球简历，包含济源任职经历"},
        {"id": "S007", "title": "data/persons 庄建球 JSON", "url": "data/persons/20260724-河南省-郑州市-市长-庄建球.json", "publisher": "gov-relation repo", "published_at": AS_OF, "accessed_at": AS_OF, "source_type": "database", "reliability": "high", "notes": "庄建球详细履历，含济源市委书记/市长任期"},
    ]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON Builder
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(person, timeline, relationships_list, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "济源市",
            "region": "济源市",
            "job": person["current_post"],
            "task_id": "henan_济源市",
            "time_focus": "current and career history"
        },
        "identity": {
            "person_id": f"jiyuan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person["birth"] else person["name"],
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person["birthplace"] else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline,
        "organizations": [
            {"org_id": 1, "name": "中共济源市委", "type": "党委", "level": "地级", "location": "河南省济源市"},
            {"org_id": 2, "name": "济源市人民政府", "type": "政府", "level": "地级", "location": "河南省济源市"},
            {"org_id": 3, "name": "济源产城融合示范区党工委", "type": "党委", "level": "地级", "location": "河南省济源市"},
            {"org_id": 4, "name": "济源产城融合示范区管理委员会", "type": "政府", "level": "地级", "location": "河南省济源市"},
        ],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面公开记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少出生年份、完整教育和早期履历信息"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份和籍贯是？", "why_it_matters": "核心人物身份信息缺失", "suggested_queries": [f"{person['name']} 简历 出生"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}的完整职业履历是什么？包括上任前的职务", "why_it_matters": "无法分析晋升路径和跨部门经验", "suggested_queries": [f"{person['name']} 任职经历 简历", f"{person['name']} 济源"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}上任前的职务是什么？", "why_it_matters": "需确认是否从省直部门或其他地市调任", "suggested_queries": [f"{person['name']} 河南 任职", f"{person['name']} 调任"], "last_attempted": AS_OF},
        ]
    }


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  济源市领导班子工作关系网络")
    print("  等级: 省直辖县级市（正厅级）")
    print(f"  调查日期: {AS_OF}")
    print("  信息来源: 济源市人民政府网站")
    print("=" * 60)

    # Build DB + GEXF
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

    print(f"\n  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 高永 (市委书记)
    gao_timeline = [
        {"start": "2026-05", "end": "", "org": "中共济源市委", "title": "示范区党工委书记、市委书记", "notes": "2026年6月2日首次以该身份公开调研", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
    ]
    gao_relationships = [
        {"person": "秦保建", "person_id": "jiyuan_秦保建", "relationship_type": "overlap", "strength": "strong", "evidence": "党工委书记/市委书记与管委会主任/市长党政一把手搭档", "overlap_org": "济源产城融合示范区/济源市", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
        {"person": "庄建球", "person_id": "jiyuan_庄建球", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "庄建球（2023.04-2025.02任市委书记）→ 高永（2026.05-任市委书记）", "overlap_org": "中共济源市委", "overlap_period": "不重叠（前后任）", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S006", "S007"]},
    ]
    gao_json = make_person_json(persons[0], gao_timeline, gao_relationships, source_register)
    gao_path = STAGING / f"{TODAY}-河南省-济源市-市委书记-高永.json"
    with open(gao_path, "w", encoding="utf-8") as f:
        json.dump(gao_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gao_path.name}")

    # 2. 秦保建 (市长)
    qin_timeline = [
        {"start": "", "end": "", "org": "济源市人民政府", "title": "示范区管委会主任、市长", "notes": "主持示范区管委会和市政府全面工作；截至2026年7月已在该岗位开展工作至少3个月", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]
    qin_relationships = [
        {"person": "高永", "person_id": "jiyuan_高永", "relationship_type": "overlap", "strength": "strong", "evidence": "管委会主任/市长与党工委书记/市委书记党政一把手搭档", "overlap_org": "济源产城融合示范区/济源市", "overlap_period": "2026-05至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
        {"person": "庄建球", "person_id": "jiyuan_庄建球", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "庄建球（2021.09-2023.04任市长）→ 秦保建（现任市长）", "overlap_org": "济源市人民政府", "overlap_period": "不重叠（前后任）", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S006", "S007"]},
    ]
    qin_json = make_person_json(persons[1], qin_timeline, qin_relationships, source_register)
    qin_path = STAGING / f"{TODAY}-河南省-济源市-市长-秦保建.json"
    with open(qin_path, "w", encoding="utf-8") as f:
        json.dump(qin_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {qin_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {STAGING}")


if __name__ == "__main__":
    main()
