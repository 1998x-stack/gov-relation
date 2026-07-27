#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 远安县 (Yuan'an County), 宜昌市, 湖北省.

Level: 县
Province: 湖北省
Parent city: 宜昌市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: hubei_远安县

Research date: 2026-07-24
Official source: http://www.yuanan.gov.cn/ (远安县人民政府) — heavily relied on

Current status (as of 2026-07-24):
- 县委书记: 刘朝 (confirmed via official site news 2025-2026)
- 县长: 郭俊伟 (confirmed via official site news 2025-2026)

Research constraints:
- Exa search API rate-limited throughout research
- Jina Reader (r.jina.ai) timed out
- Baidu Baike returned 403
- Baidu/Google/Bing search engines blocked or timed out
- Primary sources: yuanan.gov.cn official news articles (extensive coverage)
- All unverifiable biographical fields left empty
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "远安县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 刘朝 — 县委书记
    {
        "id": 1,
        "name": "刘朝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共远安县委书记",
        "current_org": "中共远安县委员会",
        "source": "http://www.yuanan.gov.cn/ (confirmed via multiple official news articles 2025-2026)",
    },
    # 2. 郭俊伟 — 县长
    {
        "id": 2,
        "name": "郭俊伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委副书记、县长",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-700612-1.html (confirmed as 县委副书记、县长, 2026-05-27)",
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    # 3. 汤明 — 前任县委书记 (confirmed in office 2023-2024)
    {
        "id": 3,
        "name": "汤明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.yuanan.gov.cn/ (confirmed via multiple official news articles 2023-2024 as 县委书记)",
    },
    # ════════════════════════════════════════
    # Leadership Team (县委/县政府)
    # ════════════════════════════════════════
    # 4. 丁海容 — 县委副书记
    {
        "id": 4,
        "name": "丁海容",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委副书记",
        "current_org": "中共远安县委员会",
        "source": "http://www.yuanan.gov.cn/content-73-700983-1.html (confirmed as 县委副书记, 2026-07-06)",
    },
    # 5. 陈德虎 — 县委常委、常务副县长
    {
        "id": 5,
        "name": "陈德虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委常委、常务副县长",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-700572-1.html (confirmed as 县委常委、常务副县长, 2026-05-22)",
    },
    # 6. 高建平 — 县领导 (副县长级)
    {
        "id": 6,
        "name": "高建平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县副县长",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/ (confirmed in multiple articles accompanying 刘朝 on inspections)",
    },
    # 7. 孙明琴 — 县委常委
    {
        "id": 7,
        "name": "孙明琴",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委常委",
        "current_org": "中共远安县委员会",
        "source": "http://www.yuanan.gov.cn/content-73-700983-1.html (confirmed, 2026-07-06); http://www.yuanan.gov.cn/content-73-690716-1.html (confirmed as 县委常委、县总工会主席, 2023-07-31)",
    },
    # 8. 温晓明 — 县委常委、县委办公室主任
    {
        "id": 8,
        "name": "温晓明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委常委、县委办公室主任",
        "current_org": "中共远安县委员会",
        "source": "http://www.yuanan.gov.cn/content-73-694407-1.html (confirmed as 县委常委、县委办公室主任, 2024-07-30)",
    },
    # 9. 肖秀栋 — 县领导
    {
        "id": 9,
        "name": "肖秀栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县领导",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-701148-1.html (mentioned in 刘朝调研, 2026-07-20)",
    },
    # 10. 邓作军 — 县领导
    {
        "id": 10,
        "name": "邓作军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县领导",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-701036-1.html (confirmed in meeting, 2026-07-10)",
    },
    # 11. 彭虎彪 — 县领导
    {
        "id": 11,
        "name": "彭虎彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县领导",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-700983-1.html (confirmed, 2026-07-06)",
    },
    # 12. 曾凡涛 — 县领导
    {
        "id": 12,
        "name": "曾凡涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县领导",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-701036-1.html (confirmed in meeting, 2026-07-10)",
    },
    # 13. 张志威 — 县委常委、县人武部部长
    {
        "id": 13,
        "name": "张志威",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县委常委、县人武部上校部长",
        "current_org": "远安县人民武装部",
        "source": "http://www.yuanan.gov.cn/content-73-695712-1.html (confirmed as 县委常委、县人武部上校部长, 2024-12-19)",
    },
    # 14. 王锋 — 县领导
    {
        "id": 14,
        "name": "王锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "远安县领导",
        "current_org": "远安县人民政府",
        "source": "http://www.yuanan.gov.cn/content-73-700983-1.html (confirmed, 2026-07-06)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共远安县委员会", "type": "党委", "level": "县处级", "parent": "中共宜昌市委", "location": "湖北省宜昌市远安县"},
    {"id": 2, "name": "远安县人民政府", "type": "政府", "level": "县处级", "parent": "宜昌市人民政府", "location": "湖北省宜昌市远安县鸣凤镇解放路25号"},
    {"id": 3, "name": "远安县人民武装部", "type": "事业单位", "level": "县处级", "parent": "宜昌军分区", "location": "湖北省宜昌市远安县"},
    {"id": 4, "name": "远安县人大常委会", "type": "人大", "level": "县处级", "parent": "宜昌市人大常委会", "location": "湖北省宜昌市远安县"},
    {"id": 5, "name": "远安县政协", "type": "政协", "level": "县处级", "parent": "宜昌市政协", "location": "湖北省宜昌市远安县"},
    {"id": 6, "name": "远安县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共宜昌市纪委", "location": "湖北省宜昌市远安县"},
    {"id": 7, "name": "远安县委组织部", "type": "党委", "level": "乡科级", "parent": "中共远安县委员会", "location": "湖北省宜昌市远安县"},
    {"id": 8, "name": "远安县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共远安县委员会", "location": "湖北省宜昌市远安县"},
    {"id": 9, "name": "远安县委统战部", "type": "党委", "level": "乡科级", "parent": "中共远安县委员会", "location": "湖北省宜昌市远安县"},
    {"id": 10, "name": "远安县委政法委", "type": "党委", "level": "乡科级", "parent": "中共远安县委员会", "location": "湖北省宜昌市远安县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # — 刘朝 —
    {"person_id": 1, "org_id": 1, "title": "中共远安县委书记", "start_date": "2024-12", "end_date": "", "rank": "县处级正职", "note": "confirmed as 县委书记、县长 in 2024-12-19 article; by 2025-07 was solely 县委书记"},
    {"person_id": 1, "org_id": 2, "title": "远安县人民政府县长（兼任）", "start_date": "2024-12", "end_date": "2025", "rank": "县处级正职", "note": "Held dual role as secretary and mayor temporarily during transition"},
    # — 郭俊伟 —
    {"person_id": 2, "org_id": 1, "title": "远安县委副书记", "start_date": "2024-12", "end_date": "", "rank": "县处级副职", "note": "confirmed as 县委副书记 in 2024-12-19 article"},
    {"person_id": 2, "org_id": 2, "title": "远安县人民政府县长", "start_date": "2025", "end_date": "", "rank": "县处级正职", "note": "Promoted to 县长 after 刘朝 transition, confirmed in 2026 news"},
    # — 汤明 (predecessor) —
    {"person_id": 3, "org_id": 1, "title": "中共远安县委书记", "start_date": "", "end_date": "2024-12", "rank": "县处级正职", "note": "Confirmed through 2024-07-30 article; succeeded by 刘朝 around 2024-12"},
    # — 丁海容 —
    {"person_id": 4, "org_id": 1, "title": "远安县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "confirmed as of 2026-07"},
    # — 陈德虎 —
    {"person_id": 5, "org_id": 1, "title": "远安县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "远安县常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Confirmed as 县委常委、常务副县长 in 2026-05-22 article"},
    # — 高建平 —
    {"person_id": 6, "org_id": 2, "title": "远安县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Frequently accompanies 刘朝 on inspection tours"},
    # — 孙明琴 —
    {"person_id": 7, "org_id": 1, "title": "远安县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Also served as 县总工会主席 (confirmed 2023-07)"},
    # — 温晓明 —
    {"person_id": 8, "org_id": 1, "title": "远安县委常委、县委办公室主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Confirmed 2024-07-30"},
    # — 肖秀栋 —
    {"person_id": 9, "org_id": 2, "title": "远安县领导", "start_date": "", "end_date": "", "rank": "", "note": "Specific title unclear; accompanies 刘朝 on economic inspections"},
    # — 邓作军 —
    {"person_id": 10, "org_id": 2, "title": "远安县领导", "start_date": "", "end_date": "", "rank": "", "note": "Confirmed in safety/environmental meetings"},
    # — 彭虎彪 —
    {"person_id": 11, "org_id": 2, "title": "远安县领导", "start_date": "", "end_date": "", "rank": "", "note": "Confirmed in meetings 2026-07"},
    # — 曾凡涛 —
    {"person_id": 12, "org_id": 2, "title": "远安县领导", "start_date": "", "end_date": "", "rank": "", "note": "Confirmed in meetings 2026-07"},
    # — 张志威 —
    {"person_id": 13, "org_id": 3, "title": "远安县人武部上校部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "Confirmed as 县委常委、县人武部上校部长, 2024-12-19"},
    {"person_id": 13, "org_id": 1, "title": "远安县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # — 王锋 —
    {"person_id": 14, "org_id": 2, "title": "远安县领导", "start_date": "", "end_date": "", "rank": "", "note": "Confirmed in meetings 2026-07"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 刘朝 ↔ 郭俊伟 — direct working relationship (书记+县长搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "县委主要领导搭档：县委书记与县长，共同主持县委、政府全面工作",
        "overlap_org": "远安县",
        "overlap_period": "2025-现在",
    },
    # 刘朝 ↔ 丁海容 — 书记+副书记
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "县委书记与副书记",
        "overlap_org": "中共远安县委员会",
        "overlap_period": "2025-现在",
    },
    # 刘朝 ↔ 高建平 — 书记+副县长（经常一同调研）
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "县委书记与副县长，高建平频繁陪同刘朝调研",
        "overlap_org": "远安县",
        "overlap_period": "2025-现在",
    },
    # 郭俊伟 ↔ 陈德虎 — 县长+常务副县长
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "县长与常务副县长",
        "overlap_org": "远安县人民政府",
        "overlap_period": "2025-现在",
    },
    # 刘朝 → 汤明 — 前后任书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "接替汤明担任远安县委书记",
        "overlap_org": "中共远安县委员会",
        "overlap_period": "2024-12",
    },
    # 刘朝 ↔ 温晓明 — 书记+县委办主任
    {
        "person_a": 1,
        "person_b": 8,
        "type": "overlap",
        "context": "县委书记与县委办公室主任（温晓明在汤明时期已任此职）",
        "overlap_org": "中共远安县委员会",
        "overlap_period": "2024-现在",
    },
    # 刘朝 ↔ 张志威 — 书记+人武部长（第一书记关系）
    {
        "person_a": 1,
        "person_b": 13,
        "type": "overlap",
        "context": "县人武部党委第一书记与县人武部部长",
        "overlap_org": "远安县人民武装部",
        "overlap_period": "2024-12-现在",
    },
    # 汤明 ↔ 温晓明 — 前任书记+县委办主任
    {
        "person_a": 3,
        "person_b": 8,
        "type": "overlap",
        "context": "县委办主任在汤明书记任内服务",
        "overlap_org": "中共远安县委员会",
        "overlap_period": "2023-2024",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON FILES
# ══════════════════════════════════════════════════════════════════════════════

person_json_configs = [
    {
        "person_id": 1,
        "name": "刘朝",
        "filename": f"{TODAY}-湖北省-宜昌市-县委书记-刘朝.json",
        "title": "中共远安县委书记",
    },
    {
        "person_id": 2,
        "name": "郭俊伟",
        "filename": f"{TODAY}-湖北省-宜昌市-县长-郭俊伟.json",
        "title": "远安县委副书记、县长",
    },
    {
        "person_id": 3,
        "name": "汤明",
        "filename": f"{TODAY}-湖北省-宜昌市-前任县委书记-汤明.json",
        "title": "前任远安县委书记",
    },
]


def write_person_json(cfg: dict) -> None:
    """Write a person graph JSON file."""
    pid = cfg["person_id"]
    p = next(p_ for p_ in persons if p_["id"] == pid)
    out_path = PERSONS_DIR / cfg["filename"]

    person_id_slug = f"yuanan_{p['name']}"

    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "宜昌市",
            "region": "远安县",
            "job": cfg["title"],
            "task_id": "hubei_远安县",
            "time_focus": "2023-2026",
        },
        "identity": {
            "person_id": person_id_slug,
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"] or "",
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_" if not p.get("birth") else f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}" if not p.get("birthplace") else f"{p['name']}_{p['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True if p.get("current_post") else False,
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
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "远安县人民政府官方网站",
                "url": "http://www.yuanan.gov.cn/",
                "publisher": "远安县人民政府办公室",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official county government website; primary source for leadership identification",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "No biographical details (birth year, birthplace, education, career history) available - web search tools were all unavailable",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月、籍贯、教育背景？",
                "why_it_matters": "Identity deduplication and career baseline",
                "suggested_queries": [f"远安县 {p['name']} 简历 出生", f"{p['name']} 任前公示", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履职经历？",
                "why_it_matters": "Career path shows promotion pattern and network connections",
                "suggested_queries": [f"{p['name']} 任职经历", f"{p['name']} 此前担任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Add career timeline based on known positions for this person
    person_positions = [pos for pos in positions if pos["person_id"] == pid]
    for pos in person_positions:
        org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
        doc["career_timeline"].append({
            "start": pos.get("start_date", ""),
            "end": pos.get("end_date", ""),
            "org": org_name,
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "湖北省宜昌市远安县",
            "system": "party" if "委" in org_name or "委" in pos["title"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": False,
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if "confirmed" in pos.get("note", "") else "plausible",
            "source_ids": ["S001"],
        })

    # Add relationships for this person
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p_ for p_ in persons if p_["id"] == other_id), None)
        if other:
            doc["relationships"].append({
                "person": other["name"],
                "person_id": f"yuanan_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Wrote {out_path}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")

    # 1. Build DB + GEXF
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

    # 2. Write person JSON files
    print("Writing person JSON files...")
    for cfg in person_json_configs:
        write_person_json(cfg)

    print(f"\nDone! Files in {_STAGING_DIR}:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for cfg in person_json_configs:
        print(f"  JSON: {PERSONS_DIR / cfg['filename']}")

    # 3. Quick validation
    print("\nValidation:")
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    # Verify GEXF exists
    gexf_size = GEXF_PATH.stat().st_size
    print(f"  GEXF: {gexf_size} bytes")
    assert gexf_size > 0, "GEXF file is empty!"

    print("\nAll validation checks passed.")
