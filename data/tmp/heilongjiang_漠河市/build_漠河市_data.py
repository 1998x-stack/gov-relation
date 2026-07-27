#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 漠河市 (Mohe City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_漠河市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - https://www.mohe.gov.cn/ — 漠河市人民政府官网 (confirmed as-of 2026-07-24)
    Homepage news articles confirm:
    * 吴庆军 — 地区人大工委副主任、市委书记
    * 袁海舰 — 市委副书记、市长
  - Multiple news articles from mohe.gov.cn confirming activities (flood control, Spring Festival慰问, New Year speech)

Confidence notes:
  - 吴庆军 (市委书记): confirmed via official site news articles (春节走访慰问, 2026-07 news)
    Title is 地区人大工委副主任、市委书记 — holds concurrent positions at prefecture and city levels
  - 袁海舰 (市长): confirmed via official site news articles (新年致词, 春节走访慰问, 防汛调研)
    Title is 市委副书记、市长
  - Full leadership roster (市委常委、政府、人大、政协): UNVERIFIED — site 领导之窗 page could not be located or returned 404
  - Career histories for both leaders: unverified — only current positions confirmed from official sources
  - Birth details, education, party join dates for all leaders: unverified
  - Exa search was rate-limited; Baidu returned CAPTCHA; Jina Reader timed out
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
SLUG = "漠河市"
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
        "name": "吴庆军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记、地区人大工委副主任",
        "current_org": "中共漠河市委员会",
        "source": "https://www.mohe.gov.cn/"
    },
    {
        "id": 2,
        "name": "袁海舰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "漠河市人民政府",
        "source": "https://www.mohe.gov.cn/"
    },
    # ═══════ 市委常委 (unverified roster — based on standard county-level city structure) ═══════
    {
        "id": 3,
        "name": "待确认_常务副市长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "漠河市人民政府",
        "source": ""
    },
    {
        "id": 4,
        "name": "待确认_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共漠河市纪律检查委员会",
        "source": ""
    },
    {
        "id": 5,
        "name": "待确认_组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共漠河市委组织部",
        "source": ""
    },
    {
        "id": 6,
        "name": "待确认_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共漠河市委宣传部",
        "source": ""
    },
    {
        "id": 7,
        "name": "待确认_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共漠河市委政法委",
        "source": ""
    },
    # ═══════ 市政府班子 (unverified — standard roles listed) ═══════
    {
        "id": 8,
        "name": "待确认_副市长1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漠河市人民政府",
        "source": ""
    },
    {
        "id": 9,
        "name": "待确认_副市长2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漠河市人民政府",
        "source": ""
    },
    {
        "id": 10,
        "name": "待确认_公安局局长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、公安局局长",
        "current_org": "漠河市人民政府",
        "source": ""
    },
    # ═══════ 人大 ═══════
    {
        "id": 11,
        "name": "待确认_人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "漠河市人大常务委员会",
        "source": ""
    },
    # ═══════ 政协 ═══════
    {
        "id": 12,
        "name": "待确认_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协漠河市委员会",
        "source": ""
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漠河市委员会", "type": "党委", "level": "县级", "parent": "中共大兴安岭地区委员会", "location": "漠河市"},
    {"id": 2, "name": "漠河市人民政府", "type": "政府", "level": "县级", "parent": "大兴安岭地区行政公署", "location": "漠河市"},
    {"id": 3, "name": "中共漠河市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共大兴安岭地区纪律检查委员会", "location": "漠河市"},
    {"id": 4, "name": "中共漠河市委组织部", "type": "党委", "level": "县级", "parent": "中共漠河市委员会", "location": "漠河市"},
    {"id": 5, "name": "中共漠河市委宣传部", "type": "党委", "level": "县级", "parent": "中共漠河市委员会", "location": "漠河市"},
    {"id": 6, "name": "中共漠河市委政法委", "type": "党委", "level": "县级", "parent": "中共漠河市委员会", "location": "漠河市"},
    {"id": 7, "name": "漠河市人大常务委员会", "type": "人大", "level": "县级", "parent": "大兴安岭地区人大工作委员会", "location": "漠河市"},
    {"id": 8, "name": "政协漠河市委员会", "type": "政协", "level": "县级", "parent": "政协大兴安岭地区委员会", "location": "漠河市"},
    {"id": 9, "name": "漠河市公安局", "type": "政府", "level": "县级", "parent": "漠河市人民政府", "location": "漠河市"},
    {"id": 10, "name": "大兴安岭地区人大工作委员会", "type": "人大", "level": "地厅级", "parent": "黑龙江省人大常务委员会", "location": "大兴安岭地区"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 吴庆军
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持市委全面工作"},
    {"person_id": 1, "org_id": 10, "title": "地区人大工委副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任——此为地区级职务，非漠河市本级"},
    # 袁海舰
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持市政府全面工作"},
    # 待确认_常务副市长
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长（常务）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_纪委书记
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_组织部部长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "党校（行政学校）第一副校长"},
    # 待确认_宣传部部长
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_政法委书记
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_副市长1
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_副市长2
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 待确认_公安局局长
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 9, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "公安局党委书记（推定）"},
    # 待确认_人大主任
    {"person_id": 11, "org_id": 7, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 待确认_政协主席
    {"person_id": 12, "org_id": 8, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
# Only confirmed/strong relationships between core leaders; all placeholder roster items excluded
relationships = [
    # 吴庆军 ↔ 袁海舰（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吴庆军任市委书记，袁海舰任市长，为漠河市党政正职搭档", "overlap_org": "漠河市", "overlap_period": ""},
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
            "name": "吴庆军",
            "job": "市委书记",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "大兴安岭地区",
                    "region": "漠河市",
                    "job": "市委书记",
                    "task_id": "heilongjiang_漠河市",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "mohe_wuqingjun",
                    "name": "吴庆军",
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
                    "current_post": "市委书记、地区人大工委副主任",
                    "current_org": "中共漠河市委员会",
                    "administrative_rank": "正处级（兼任副厅级地区人大工委副主任）",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S002"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "present",
                        "org": "中共漠河市委员会",
                        "title": "漠河市委书记",
                        "level": "正处级",
                        "location": "漠河市",
                        "system": "party",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "袁海舰",
                        "person_id": "mohe_yuanhaijian",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "吴庆军任市委书记，袁海舰任市长，为漠河市党政正职搭档",
                        "overlap_org": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-01（春节前）",
                        "domain": "other",
                        "achievement_or_event": "春节前走访慰问老干部、老党员、老教师、困难党员、困难职工、优抚对象",
                        "role_in_event": "走访慰问",
                        "location": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S002"]
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
                            "evidence": "春节前夕走访慰问老干部、老党员、困难群众等，体现了基层关怀的工作风格",
                            "confidence": "plausible",
                            "source_ids": ["S002"]
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
                    {"id": "S001", "title": "漠河市人民政府官网", "url": "https://www.mohe.gov.cn/", "publisher": "漠河市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Official homepage — news articles confirming leadership roles"},
                    {"id": "S002", "title": "地区人大工委副主任、市委书记吴庆军春节前走访慰问", "url": "https://www.mohe.gov.cn/", "publisher": "漠河市人民政府", "published_at": "2026-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming 吴庆军 as 地区人大工委副主任、市委书记"},
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "medium",
                    "biggest_gap": "Full career history, education, birth details, and full leadership roster unknown"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": "吴庆军的完整履历（出生年月、籍贯、教育背景、历任职务）",
                        "why_it_matters": "市委书记是漠河市最高领导，兼任地区人大工委副主任——这一跨级兼任的晋升路径值得研究",
                        "suggested_queries": ["吴庆军 简历", "吴庆军 大兴安岭", "吴庆军 漠河市委书记 任命"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "吴庆军何时到任漠河市委书记",
                        "why_it_matters": "到任时间影响党政搭档关系时间线及前任去向",
                        "suggested_queries": ["吴庆军 任漠河市委书记"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "前任漠河市委书记是谁、去向如何",
                        "why_it_matters": "前任去向可揭示人事调动模式和权力结构",
                        "suggested_queries": ["漠河市 前任市委书记"],
                        "last_attempted": AS_OF
                    }
                ]
            }
        },
        {
            "id": 2,
            "name": "袁海舰",
            "job": "市长",
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "黑龙江省",
                    "city": "大兴安岭地区",
                    "region": "漠河市",
                    "job": "市长",
                    "task_id": "heilongjiang_漠河市",
                    "time_focus": "2026"
                },
                "identity": {
                    "person_id": "mohe_yuanhaijian",
                    "name": "袁海舰",
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
                    "current_post": "市委副书记、市长",
                    "current_org": "漠河市人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S003"]
                },
                "career_timeline": [
                    {
                        "start": "unknown",
                        "end": "present",
                        "org": "漠河市人民政府",
                        "title": "漠河市委副书记、市长",
                        "level": "正处级",
                        "location": "漠河市",
                        "system": "government",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "organizations": [],
                "relationships": [
                    {
                        "person": "吴庆军",
                        "person_id": "mohe_wuqingjun",
                        "relationship_type": "overlap",
                        "strength": "strong",
                        "evidence": "袁海舰任市长，吴庆军任市委书记，为漠河市党政正职搭档",
                        "overlap_org": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "governance_record": [
                    {
                        "period": "2026-01",
                        "domain": "other",
                        "achievement_or_event": "发表漠河市新年致词",
                        "role_in_event": "发表新年致词",
                        "location": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2026-01（春节前）",
                        "domain": "other",
                        "achievement_or_event": "春节前走访慰问驻漠部队官兵、移民管理警察、优抚对象、老教师",
                        "role_in_event": "走访慰问",
                        "location": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2026-01（春节前）",
                        "domain": "other",
                        "achievement_or_event": "春节前走访慰问老干部、老党员、困难党员、困难职工",
                        "role_in_event": "走访慰问",
                        "location": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    },
                    {
                        "period": "2026-07",
                        "domain": "public_security",
                        "achievement_or_event": "调研督导防汛备汛工作",
                        "role_in_event": "调研督导",
                        "location": "漠河市",
                        "confidence": "confirmed",
                        "source_ids": ["S004"]
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
                            "evidence": "春节走访慰问部队官兵、移民警察、老干部、困难群众，注重民生和一线队伍",
                            "confidence": "plausible",
                            "source_ids": ["S003"]
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
                    {"id": "S001", "title": "漠河市人民政府官网", "url": "https://www.mohe.gov.cn/", "publisher": "漠河市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "Official homepage — news articles confirming leadership roles"},
                    {"id": "S003", "title": "漠河市市长袁海舰新年致词/春节走访慰问", "url": "https://www.mohe.gov.cn/", "publisher": "漠河市人民政府", "published_at": "2026-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News articles confirming 袁海舰 as 市委副书记、市长"},
                    {"id": "S004", "title": "漠河市委副书记、市长袁海舰调研督导防汛备汛工作", "url": "https://www.mohe.gov.cn/", "publisher": "漠河市人民政府", "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "News article confirming role"},
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
                        "question": "袁海舰的完整履历（出生年月、籍贯、教育背景、历任职务）",
                        "why_it_matters": "市长是漠河市行政一把手，完整履历对理解其能力和关系网络至关重要",
                        "suggested_queries": ["袁海舰 简历", "袁海舰 大兴安岭"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "袁海舰何时到任漠河市长",
                        "why_it_matters": "到任时间影响党政搭档关系时间线",
                        "suggested_queries": ["袁海舰 任漠河市长"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": "前任漠河市长是谁、去向如何",
                        "why_it_matters": "前任去向可揭示人事调动模式",
                        "suggested_queries": ["漠河市 前任市长"],
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
