#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 太子河区, 辽阳市, 辽宁省.

Investigation date: 2026-08-07
Task ID: liaoning_太子河区
Level: 市辖区
Targets: 区委书记(薛松) & 区长(曲仁刚)

Research sources (accessed 2026-08-07):
  - http://www.tzh.gov.cn/ — 辽阳市太子河区人民政府门户网站 (official, primary, HTTP via curl_cffi)
      * 区委书记薛松看望慰问区公安分局一线公安干警 2025-01-24 (薛松/冯光 公安局长 confirmed)
      * 薛松带队到市消防救援支队开展走访慰问 2026-02-18 (区委书记 薛松; 区长 曲仁刚 一同参加; 副区长邵艳梅、区政协副主席张明晰陪同)
      * 曲仁刚走访慰问驻区部队官兵 2026-02-18 (区委副书记、区长 曲仁刚 confirmed)
      * 胡铁深深入区公安分局开展走访慰问 2026-02-18 (区政协党组书记、主席 胡铁山 confirmed)
  - 辽阳市政府门户 http://www.liaoyang.gov.cn/ (归属市级, 二手参照)

Confidence notes:
  - 现任区委书记 薛松 — confirmed (官方新闻 2025-01-24 及 2026-02-18 以"区委书记"署名)
  - 现任区委副书记、区长 曲仁刚 — confirmed (官方新闻 2026-02-18 "区委副书记、区长曲仁刚"; 一同参加慰问)
  - 区政协党组书记、主席 胡铁山 — confirmed (官方新闻 2026-02-18 走访慰问公安分局)
  - 副区长 邵艳梅 — confirmed (官方新闻 2026-02-18 "副区长邵艳梅陪同慰问")
  - 区政协副主席 张明晰 — confirmed (官方新闻 2026-02-18 陪同慰问)
  - 区公安分局局长 冯光 — confirmed (官方新闻 2025-01-24 "局长冯光代表全局")
  - 官网未开放领导之窗/完整常委名单; 两大核心人物(薛松/曲仁刚)此前履历、出生、学历等 —— 留 open_questions
  - 前任区委书记、前任区长未见公开线索 —— 留 open_questions

Web-access note (per rules): Exa rate-limited; Baidu/Bing/360/Sogou 验证码; Jina reader/Baidu Baike 超时/403;
official site www.tzh.gov.cn reachable via curl_cffi (Chrome impersonation) — 主要一手来源。
"""

from __future__ import annotations

import json
import re
import sqlite3
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

from gov_relation.runner import run_build

# ── Metadata ────────────────────────────────────────────────────────────────
SLUG = "太子河区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_太子河区"
if _CURRENT_DIR.name == "liaoning_太子河区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

SRC = "http://www.tzh.gov.cn/（太子河区人民政府门户网站，官方一手，curl_cffi）"
# ── Persons ─────────────────────────────────────────────────────────────────
# 核心: 1=区委书记 薛松, 2=区长 曲仁刚
# 班子/相关: 3 胡铁山(区政协党组书记、主席), 4 邵艳梅(副区长), 5 张明晰(区政协副主席), 6 冯光(区公安分局局长)
persons = [
    # ═══ 现任核心 ══════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "薛松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区委书记",
        "current_org": "中共辽阳市太子河区委",
        "source": SRC + " 2026-02-18 走访慰问市消防救援支队以'区委书记'署名; 2025-01-24 看望慰问公安干警以'区委书记'署名",
    },
    {
        "id": 2,
        "name": "曲仁刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区委副书记、区长",
        "current_org": "辽阳市太子河区人民政府",
        "source": SRC + " 2026-02-18 走访慰问驻区部队以'区委副书记、区长'署名; 2026-02-18 与薛松一同慰问",
    },
    # ═══ 班子 / 相关 ═══════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "胡铁山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区政协党组书记、主席",
        "current_org": "政协辽阳市太子河区委员会",
        "source": SRC + " 2026-02-18 深入区公安分局走访慰问以'区政协党组书记、主席'署名",
    },
    {
        "id": 4,
        "name": "邵艳梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区人民政府副区长",
        "current_org": "辽阳市太子河区人民政府",
        "source": SRC + " 2026-02-18 陪同慰问（官方新闻：副区长邵艳梅陪同慰问）",
    },
    {
        "id": 5,
        "name": "张明晰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区政协副主席",
        "current_org": "政协辽阳市太子河区委员会",
        "source": SRC + " 2026-02-18 陪同慰问（区政协副主席）",
    },
    {
        "id": 6,
        "name": "冯光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "太子河区公安分局局长",
        "current_org": "辽阳市太子河区公安分局",
        "source": SRC + " 2025-01-24 '局长冯光代表全局'（走访慰问区公安分局）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辽阳市太子河区委", "type": "party_committee", "level": "县处级", "parent": "中共辽阳市委", "location": "辽阳市太子河区"},
    {"id": 2, "name": "辽阳市太子河区人民政府", "type": "government", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市太子河区"},
    {"id": 3, "name": "辽阳市太子河区人大常委会", "type": "npc", "level": "县处级", "parent": "辽阳市人大常委会", "location": "辽阳市太子河区"},
    {"id": 4, "name": "政协辽阳市太子河区委员会", "type": "cppcc", "level": "县处级", "parent": "政协辽阳市委员会", "location": "辽阳市太子河区"},
    {"id": 5, "name": "中共辽阳市太子河区纪委区监委", "type": "discipline", "level": "县处级", "parent": "辽阳市纪委", "location": "辽阳市太子河区"},
    {"id": 6, "name": "辽阳市太子河区公安分局", "type": "government", "level": "科级", "parent": "辽阳市公安局", "location": "辽阳市太子河区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 薛松 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2025-01 及 2026-02 官方新闻确认在任"},
    # 曲仁刚 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026-02-18 官方新闻以'区委副书记、区长'署名"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 胡铁山 政协主席
    {"person_id": 3, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026-02-18 官方新闻确认"},
    {"person_id": 3, "org_id": 4, "title": "区政协党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 邵艳梅 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-02-18 陪同慰问"},
    # 张明晰 政协副主席
    {"person_id": 5, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-02-18 陪同慰问"},
    # 冯光 公安局长
    {"person_id": 6, "org_id": 6, "title": "区公安分局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "2025-01-24 代表全局"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—区长 核心搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长（常委会搭档，2026年慰问活动同框）", "overlap_org": "中共辽阳市太子河区委员会 / 辽阳市太子河区人民政府", "overlap_period": "现有任期"},
    # 书记—政协主席
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记—区政协主席（同框履职）", "overlap_org": "辽阳市太子河区区级班子", "overlap_period": ""},
    # 区长—副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "辽阳市太子河区人民政府", "overlap_period": ""},
    # 政协主席—政协副主席
    {"person_a": 3, "person_b": 5, "type": "superior_subordinate", "context": "区政协主席—副主席", "overlap_org": "政协辽阳市太子河区委员会", "overlap_period": ""},
    # 书记—公安局长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记—区公安分局局长（走访慰问）", "overlap_org": "辽阳市太子河区公安分局", "overlap_period": "2025-01"},
]

# ── Person JSON(s) ────────────────────────────────────────────────────────────
_RANK_BY_ID = {1: "正处级", 2: "正处级", 3: "正处级", 4: "副处级", 5: "副处级", 6: "正科级"}


def _job_tag(person: dict) -> str:
    post = person.get("current_post") or person.get("current_part") or ""
    if "区委书记" in post:
        return "区委书记"
    if "副区长" in post:
        return "副区长"
    if "区长" in post:
        return "区长"
    if "政协" in post and "主席" in post and "副主席" not in post:
        return "区政协主席"
    if "政协" in post:
        return "区政协副主席"
    if "公安" in post:
        return "区公安分局局长"
    return "领导"


def _write_person_json(person: dict, out_dir: Path) -> Path:
    job_tag = _job_tag(person)
    raw_name = TODAY + "-辽宁省-辽阳市-" + job_tag + "-" + person["name"] + ".json"
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", raw_name)
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "辽阳市",
            "region": "太子河区",
            "job": job_tag,
            "task_id": "liaoning_太子河区",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": "taizihe_" + person["name"],
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": person["name"] + "_", "official_profile_url": "http://www.tzh.gov.cn/"},
        },
        "current_status": {
            "current_post": person.get("current_post", person.get("current_part", "")),
            "current_org": person.get("current_org", ""),
            "administrative_rank": _RANK_BY_ID.get(person["id"], "县处级"),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开渠道未找到" + person["name"] + "担任" + job_tag + "之前的履历信息",
                "confidence": "unverified",
                "source_ids": [],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", person.get("current_part", "")),
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [person.get("current_post", person.get("current_part", ""))],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "未公开，无法评估", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "现有公开证据不足（仅有官方走访慰问新闻），未对工作风格/性格做出推断。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 " + AS_OF + " 未检索到" + person["name"] + "的纪律/负面信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "太子河区人民政府门户网站（新闻中心/政务活动）",
                "url": "http://www.tzh.gov.cn/",
                "publisher": "辽阳市太子河区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": person.get("source", ""),
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景、入党时间、工作起点及任现职前完整履历全部未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": person["name"] + "的完整履历（出生年月、籍贯、学历、入党时间、工作起点、任现职前职务及精确时间线）",
                "why_it_matters": "判断晋升路径与跨区交流网络",
                "suggested_queries": [person["name"] + " 简历", person["name"] + " 任前公示", person["name"] + " 辽宁 任职"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "太子河区前任区委书记（薛松之前）、前任区长（曲仁刚之前）的身份与去向",
                "why_it_matters": "建立一把手/二把手更替链与跨区交流网络",
                "suggested_queries": ["太子河区 前任 区委书记", "太子河区 前任 区长"],
                "last_attempted": TODAY,
            },
        ],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Posits:  {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

    # Person JSON for every listed person
    for p in persons:
        fpath = _write_person_json(p, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF via runner (uses gov_relation schema/gexf)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=[o for o in organizations if isinstance(o, dict) and "name" in o],
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    p_count = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    o_count = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    pos_count = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    r_count = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    print(f"\n  DB written: {DB_PATH.exists()}, size={DB_PATH.stat().st_size} bytes")
    print(f"    Persons: {p_count}, Orgs: {o_count}, Positions: {pos_count}, Relations: {r_count}")
    print(f"  GEXF written: {GEXF_PATH.exists()}, size={GEXF_PATH.stat().st_size} bytes")
    print(f"═══ Done ═══")