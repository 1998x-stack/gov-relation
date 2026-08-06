#!/usr/bin/env python3
"""鄂州市鄂城区领导班子工作关系网络 — 数据构建脚本。

级别: 市辖区
调查日期: 2026-08-06
网络状态: 本次调查公开网络严重受限（Exa rate-limited、百度/谷歌/Jina 403/超时、
          鄂城区子站超时、鄂州市官网仅首页可达且 JS 渲染空正文）。
依据本地一手档案（data/database/鄂州市_network.db，市级班子已确认）与
可参考公开资料识别区级班子；所有未核实字段显式登记为 unverified/plausible，
并纳入 person JSON 的 open_questions 与 report/open_gaps.md。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

# Ensure gov_relation package is importable
def _repo_root(start: Path) -> Path:
    cur = start
    while cur != cur.parent:
        if (cur / "gov_relation").is_dir():
            return cur
        cur = cur.parent
    return start


_REPO_ROOT = _repo_root(Path(__file__).resolve().parent)
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "鄂城区"
TODAY = "2026-08-06"
STAGING = Path(__file__).resolve().parent

BASE = _repo_root(STAGING)
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
PERSONS_DIR = BASE / "data" / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────
# 1xxx = 区委, 2xxx = 区政府, 3xxx = 人大/政协, 4xxx = 前任/外部
persons = [
    # ═══════════ 1. 现任区委书记（识别待一手核） ═══════════
    {
        "id": 1001,
        "name": "董国平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记（plausible，待一手核）",
        "current_org": "中共鄂州市鄂城区委员会",
        "source": "https://www.ezhou.gov.cn/（鄂州市人民政府网，区级领导信息页待抓）",
    },
    # ═══════════ 2. 现任区长（未公开一手核） ═══════════
    {
        "id": 2001,
        "name": "夏鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民政府区长（plausible，待一手核）",
        "current_org": "鄂城区人民政府",
        "source": "https://www.ezhou.gov.cn/（鄂州市委网，区级领导信息未能一手抓）",
    },
    # ═══════════ 3. 区委副书记（分管政法/党建，占位） ═══════════
    {
        "id": 1002,
        "name": "区委副书记（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（身份待查）",
        "current_org": "中共鄂州市鄂城区委员会",
        "source": "（网络受限，未核）",
    },
    # ═══════════ 4. 区委常委、常务副区长（占位） ═══════════
    {
        "id": 2002,
        "name": "常务副区长（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长（身份）",
        "current_org": "鄂城区人民政府",
        "source": "（2026-08-06 未核）",
    },
    # ═══════════ 5. 区委常委、纪委书记（占位） ═══════════
    {
        "id": 1003,
        "name": "区纪委书记（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任（身份）",
        "current_org": "中共鄂城区纪律检查委员会（区监委）",
        "source": "（2026-08-06 未核）",
    },
    # ═══════════ 6. 区人大常委会主任（占位） ═══════════
    {
        "id": 3001,
        "name": "区人大常委会主任（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任（身份）",
        "current_org": "鄂城区人民代表大会常务委员会",
        "source": "（2026-08-06 未核）",
    },
    # ═══════════ 7. 区政协主席（占位） ═══════════
    {
        "id": 3002,
        "name": "区政协主席（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席（身份）",
        "current_org": "政协鄂城区委员会",
        "source": "（2026-08-06 未核）",
    },
    # ═══════════ 8. 前任区委书记（链参考，占位） ═══════════
    {
        "id": 4001,
        "name": "前任区委书记（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记（去向/继任链待核）",
        "current_org": "中共鄂州市鄂城区委员会（历史）",
        "source": "（2026-08-06 未核）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄂州市鄂城区委员会", "type": "党委", "level": "县处级", "parent": "中共鄂州市委", "location": "鄂州市鄂城区"},
    {"id": 2, "name": "鄂城区人民政府", "type": "政府", "level": "县处级", "parent": "鄂州市人民政府", "location": "鄂州市鄂城区"},
    {"id": 3, "name": "鄂城区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鄂州市人大常委会", "location": "鄂州市鄂城区"},
    {"id": 4, "name": "政协鄂城区委员会", "type": "政协", "level": "县处级", "parent": "政协鄂州市委员会", "location": "鄂州市鄂城区"},
    {"id": 5, "name": "中共鄂城区纪律检查委员会（区监委）", "type": "纪委", "level": "县处级", "parent": "中共鄂州市纪委", "location": "鄂州市鄂城区"},
    {"id": 6, "name": "中共鄂州市委员会", "type": "党委", "level": "地厅级", "parent": "中共湖北省委", "location": "鄂州市"},
    {"id": 7, "name": "鄂州市人民政府", "type": "政府", "level": "地厅级", "parent": "湖北省人民政府", "location": "鄂州市"},
]

# ── Positions (任职) ────────────────────────────────────────────────────
positions = [
    # 区委
    {"person_id": 1001, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": "plausible，一手待核"},
    {"person_id": 1002, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": "身份待查"},
    {"person_id": 1003, "org_id": 5, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "身份待查"},
    {"person_id": 1003, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 区政府
    {"person_id": 2001, "org_id": 1, "title": "区委副书记、区人民政府区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "plausible，需一手核"},
    {"person_id": 2001, "org_id": 2, "title": "区人民政府区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "领导区政府全面工作"},
    {"person_id": 2002, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "身份待查"},
    # 人大/政协
    {"person_id": 3001, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": "身份待查"},
    {"person_id": 3002, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "县处级", "note": "身份待查"},
    # 前任
    {"person_id": 4001, "org_id": 1, "title": "区委书记（前任）", "start_date": "", "end_date": "", "rank": "县处级", "note": "去向/继任链待核"},
    # 父级关系
    {"person_id": 1001, "org_id": 6, "title": "受鄂州市委领导", "start_date": "", "end_date": "", "rank": "", "note": "区隶属市"},
    {"person_id": 2001, "org_id": 7, "title": "受鄂州市政府领导", "start_date": "", "end_date": "", "rank": "", "note": "区隶属市"},
]

# ── relationships (关系) ────────────────────────────────────────
relationships = [
    # 现任党政一把手搭档
    {"person_a": 1001, "person_b": 2001, "type": "同班子", "context": "区党政一把手搭档（拟），共同主持全区重大工作", "overlap_org": "中共鄂城区委/区政府", "overlap_period": "", "confidence": "plausible"},
    # 书记—副书记
    {"person_a": 1001, "person_b": 1002, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共鄂城区委", "overlap_period": "", "confidence": "plausible"},
    # 书记—纪委书记
    {"person_a": 1001, "person_b": 1003, "type": "上下级", "context": "区委书记—纪委书记（纪委全会）", "overlap_org": "中共鄂城区委", "overlap_period": "", "confidence": "plausible"},
    # 区长—常务副区长
    {"person_a": 2001, "person_b": 2002, "type": "上下级", "context": "区长—常务副区长（政府班子）", "overlap_org": "鄂城区人民政府", "overlap_period": "", "confidence": "plausible"},
    # 书记—人大主任 / 政协主席
    {"person_a": 1001, "person_b": 3001, "type": "工作联系", "context": "区委书记—区人大主任（两会）", "overlap_org": "鄂城区", "overlap_period": "", "confidence": "plausible"},
    {"person_a": 1001, "person_b": 3002, "type": "工作联系", "context": "区委书记—区政协主席（两会）", "overlap_org": "鄂城区", "overlap_period": "", "confidence": "plausible"},
    # 区——市隶属关系
    {"person_a": 1001, "person_b": 1001, "type": "隶属", "context": "", "overlap_org": "", "overlap_period": "", "confidence": "", "_skip": True},
]

# ── Main ─────────────────────────────────────────────────────────────────────

def person_json(person: dict) -> None:
    safe_name = person["name"]
    # 短文、规范的任务名标签
    short_job = {
        1001: "区委书记", 2001: "区长", 1002: "区委副书记",
        2003: "纪委书记", 2002: "常务副区长", 3001: "人大主任", 3002: "政协主席", 4001: "前任区委书记",
    }
    job_slug = short_job.get(person["id"], person["current_post"])
    filename = f"{TODAY.replace('-', '')}-湖北省-鄂州市-{job_slug}-{safe_name}.json"
    filepath = PERSONS_DIR / filename

    person_data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省", "city": "鄂州市", "region": "鄂城区",
            "job": person["current_post"], "task_id": "hubei_鄂城区", "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"hubei_ezhou_echeng_{safe_name}",
            "name": safe_name, "aliases": [], "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""), "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{safe_name}_{person.get('birth', '')}",
                            "name_birthplace": f"{safe_name}_{person.get('birthplace', '')}",
                            "official_profile_url": person.get("source", "")},
        },
        "current_status": {
            "current_post": person["current_post"], "current_org": person["current_org"],
            "administrative_rank": "县处级", "as_of": TODAY, "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {"start": "unknown", "end": "present", "org": person["current_org"],
             "title": person["current_post"], "level": "县处级", "location": "鄂州市鄂城区",
             "system": "party" if "书记" in person["current_post"] else "government",
             "rank": "县处级", "is_key_promotion": False, "notes": "因网络受限,履历待一手补充",
             "confidence": "unverified", "source_ids": ["S001"]},
        ],
        "organizations": [], "relationships": [],
        "governance_record": [], "professional_profile": {},
        "work_style_and_personality": {}, "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "not_checked", "description": "因网络受限未检索负面纪律/审计信号", "date": TODAY,
             "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "鄂州市人民政府门户网（父级市）", "url": "https://www.ezhou.gov.cn/",
             "publisher": "鄂州市人民政府", "published_at": "", "accessed_at": TODAY,
             "source_type": "official", "reliability": "high", "notes": "本次只见首页，区级领导正文未抓到；区级身份待一手核"}],
        "confidence_summary": {
            "identity": "unverified", "current_role": "unverified",
            "career_completeness": "empty", "relationship_confidence": "low",
            "biggest_gap": "身份/完整履历/生卒籍贯/入党参工均未一手核"},
        "open_questions": [
            {"priority": "critical", "question": f"{safe_name} 当前身份是否准确（区委书记/区长）",
             "why_it_matters": "目标的闭环", "suggested_queries": [f"鄂城区 区委书记 现任", f"鄂城区 区长 现任"],
             "last_attempted": TODAY},
            {"priority": "high", "question": f"{safe_name} 出生年月、籍贯、教育、入党/参工时间",
             "why_it_matters": "构建个人图谱基础", "suggested_queries": [f"{safe_name} 简历 任前公示"], "last_attempted": TODAY},
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  级别: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  网络状态: 受限 → 部分证据模式（partial-evidence）")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=[r for r in relationships if not r.get("_skip")],
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    for p in persons:
        if p["id"] in (1001, 2001):
            person_json(p)

    print(f"\n  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条  关系: {len([r for r in relationships if not r.get('_skip')])} 条")

    conn = sqlite3.connect(DB_PATH)
    for tab in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {tab}").fetchone()[0]
        print(f"    {tab}: {n}")
    conn.close()

    print(f"\n✅ {SLUG} 数据构建完成（部分证据模式）。")


if __name__ == "__main__":
    main()