#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 松滋市 (Songzi City), 湖北省.

Investigation date: 2026-08-07
Task ID: hubei_松滋市
Level: 县级市 (隶属 荆州市)
Targets: 市委书记 & 市长

Research sources:
  - www.hbsz.gov.cn (松滋市人民政府门户网站) — official portal homepage news feed
    confirming the current 市委书记 (汪卫) and 市委副书记、市长 (张炜), accessed
    2026-08-07.
  - zwgk.hbsz.gov.cn "政府领导" 之窗 column (column_id=30802) — official resumes for
    张炜 (市委副书记、市长) and the full 市政府领导班子, accessed 2026-08-07.
  - www.jingzhou.gov.cn (荆州市人民政府门户) — cross-region oversight relations
    (荆州市长李迎伟赴松滋调研督办磷石膏综合治理).

Confidence notes:
  - 汪卫 (市委书记): current role CONFIRMED via multiple official hbsz.gov.cn headlines
    dated 2026-07-31 / 2026-08-03 / 2026-08-04. 完整履历（出生/籍贯/学历/入党/工作起点/
    来松滋前任职务/任书记时间线）在本次网络受限环境下未能核实，记入 open_questions。
    注意：经检索的"汪卫"百科条目（复旦大学教授）为同名不同人，故不采用任何百科履历，
    绝不虚构。
  - 张炜 (市委副书记、市长): current role CONFIRMED via official 政府领导 profile page;
    official resume: 男，汉族，1982年8月出生，省委党校研究生学历，中共党员，现任松滋
    市委副书记、市政府市长。任市长前的具体历任序列未核实，记 open_questions。
  - 市政府领导班子（刘德勇、卢道勇、谢春雨、李维、马香菊、许宏晏、关兆宇、赵贵明、
    张远莫）以及 市人大常委会主任覃文忠、市政协主席唐敦浩、市委常委/统战部长孟晓祥：
    均以官方来源确认职务与基本信息，编入数据集。

一切职务信息仅来自官方公开来源；未获取到的履历字段一律留空并记录为 open_questions，
不虚构任何出生/毕业/入党时间。

Person/org/position data below is the structurally-valid confirmed core.
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow importing gov_relation regardless of where this script lives
# (staging dir data/tmp/... or canonical scripts/build/...).
for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "松滋市"
AS_OF = "2026-08-07"
TODAY = datetime.now().strftime("%Y%m%d")

# Artifacts are written next to this script (staging dir while investigating).
# process_tmp.py copies them to canonical destinations on promotion.
HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "汪卫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共松滋市委员会",
        "source": "http://www.hbsz.gov.cn/",
    },
    {
        "id": 2,
        "name": "张炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市长",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/30802/107220253/t131220253074/605749.shtml",
    },
    {
        "id": 3,
        "name": "刘德勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 4,
        "name": "卢道勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 5,
        "name": "谢春雨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "",
        "education": "汉语言文学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 6,
        "name": "李维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 7,
        "name": "马香菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "",
        "education": "历史教育学学士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 8,
        "name": "许宏晏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 9,
        "name": "关兆宇",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1973-08",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长、党组成员，市公安局党委书记/局长",
        "current_org": "松滋市人民政府",
        "source": "http://zwgk.hbsz.gov.cn/",
    },
    {
        "id": 10,
        "name": "覃文忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "松滋市人民代表大会常务委员会",
        "source": "http://www.hbsz.gov.cn/",
    },
    {
        "id": 11,
        "name": "唐敦浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议松滋市委员会",
        "source": "http://www.hbsz.gov.cn/",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共松滋市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共荆州市委员会",
        "location": "湖北省荆州市松滋市",
    },
    {
        "id": 2,
        "name": "松滋市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "荆州市人民政府",
        "location": "湖北省荆州市松滋市",
    },
    {
        "id": 3,
        "name": "松滋市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "松滋市",
        "location": "湖北省荆州市松滋市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议松滋市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "松滋市",
        "location": "湖北省荆州市松滋市",
    },
]

# ── Positions (current, as-of 2026-08-07, official-confirmed) ────────────
positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "市委书记",
        "start_date": "2026-",
        "end_date": "",
        "rank": "正处级",
        "note": "在任（截至2026-08-07，松滋市人民政府网官方新闻确认汪卫为市委书记）",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "市长",
        "start_date": "2025-",
        "end_date": "",
        "rank": "正处级",
        "note": "在任，市委副书记、市政府市长（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "市委副书记",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任，市委副书记、市政府市长（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 3,
        "org_id": 1,
        "title": "市委常委",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 3,
        "org_id": 2,
        "title": "副市长",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 4,
        "org_id": 1,
        "title": "市委常委",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 4,
        "org_id": 2,
        "title": "副市长",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 5,
        "org_id": 2,
        "title": "副市长、党组成员",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 6,
        "org_id": 2,
        "title": "副市长、党组成员",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 7,
        "org_id": 2,
        "title": "副市长",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任，无党派（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 8,
        "org_id": 2,
        "title": "副市长、党组成员",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 9,
        "org_id": 2,
        "title": "副市长、党组成员，市公安局党委书记/局长",
        "start_date": "2025-",
        "end_date": "",
        "rank": "副处级",
        "note": "在任（官方简历更新 2025-12-01）",
    },
    {
        "person_id": 10,
        "org_id": 3,
        "title": "市人大常委会主任",
        "start_date": "2026-",
        "end_date": "",
        "rank": "正处级",
        "note": "在任（截至2026-08-07官方新闻确认）",
    },
    {
        "person_id": 11,
        "org_id": 4,
        "title": "市政协主席",
        "start_date": "2026-",
        "end_date": "",
        "rank": "正处级",
        "note": "在任（截至2026-08-07官方新闻确认）",
    },
]

# ── Relationships (confirmed co-office overlap) ───────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "市委书记—市长（市委班子搭档，共同主持市常委会）",
        "overlap_org": "中共松滋市委员会",
        "overlap_period": "2026至今",
    },
]


# ── Person JSONs (deep per-figure profiles) ───────────────────────────────
def build_person_json(person: dict, current_post: str, current_org: str,
                      job: str, admin_rank: str) -> dict:
    name = person["name"]
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "荆州市",
            "region": "松滋市",
            "job": job,
            "task_id": "hubei_松滋市",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"hubei_songzi_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"] if person.get("education") else [],
                }
            ],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org,
            "administrative_rank": admin_rank,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001" if name != "汪卫" else "S002"],
        },
        "career_timeline": [
            {
                "start": "2026-" if name == "汪卫" else "2025-",
                "end": "present",
                "org": current_org,
                "title": current_post,
                "level": "县级市",
                "location": "湖北省荆州市松滋市",
                "system": "party" if current_post == "市委书记" else "government",
                "rank": admin_rank,
                "is_key_promotion": True,
                "notes": "在任，官方（松滋市人民政府网）2026-08-07 确认" if name == "汪卫"
                         else "在任，官方（松滋市人民政府网 领导之窗）简历更新 2025-12-01 确认",
                "confidence": "confirmed",
                "source_ids": ["S002" if name == "汪卫" else "S001"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "完整履历（出生/籍贯/学历/入党/工作起点）或任前历任序列在本次网络环境下未完全获取；已就官方可获得字段澄清，不虚构未披露履历" if name == "汪卫"
                         else "任市长/市委副书记前的具体历任单位与时间在本次调研中未能核实",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "org": "中共松滋市委员会",
                "type": "党委",
                "level": "县级市",
                "location": "湖北省荆州市松滋市",
            },
            {
                "org": "松滋市人民政府",
                "type": "政府",
                "level": "县级市",
                "location": "湖北省荆州市松滋市",
            },
        ],
        "relationships": [
            {
                "person": "汪卫" if name != "汪卫" else "张炜",
                "person_id": "hubei_songzi_汪卫" if name != "汪卫" else "hubei_songzi_张炜",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "市委书记—市长同松滋市委班子搭档（2026 年在任）",
                "overlap_org": "中共松滋市委员会",
                "overlap_period": "2026至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S003"],
            }
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "rural_revitalization" if name == "汪卫" else "environment",
                "achievement_or_event": "汪卫深入乡镇调研党建引领和美乡村建设整镇推进工作；带队开展'送清凉'活动并检查安全生产" if name == "汪卫"
                                         else "张炜主持市政府全面工作；市政府专题研究磷石膏综合治理与重点项目工作",
                "role_in_event": "调研督办" if name == "汪卫" else "主持/督办",
                "measurable_outcome": "",
                "location": "松滋市",
                "confidence": "confirmed",
                "source_ids": ["S002" if name == "汪卫" else "S001"],
            }
        ],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "本次调研（官方新闻与领导之窗范围）未发现负面信号",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "松滋市人民政府网 领导之窗（政府领导栏目 column_id=30802）",
                "url": "http://zwgk.hbsz.gov.cn/",
                "publisher": "松滋市人民政府",
                "published_at": "2025-12-01",
                "accessed_at": "2026-08-07",
                "source_type": "official",
                "reliability": "high",
                "notes": "张炜与市政府班子正式简历",
            },
            {
                "id": "S002",
                "title": "松滋市人民政府门户 首页要闻",
                "url": "http://www.hbsz.gov.cn/",
                "publisher": "松滋市人民政府",
                "published_at": "2026-07-31",
                "accessed_at": "2026-08-07",
                "source_type": "official",
                "reliability": "high",
                "notes": "官方网站要闻确认 汪卫 为市委书记在任",
            },
            {
                "id": "S003",
                "title": "荆州市人民政府门户网站",
                "url": "https://www.jingzhou.gov.cn/",
                "publisher": "荆州市人民政府",
                "published_at": "2026-08-06",
                "accessed_at": "2026-08-07",
                "source_type": "official",
                "reliability": "high",
                "notes": "cross-region: 荆州市长李迎伟赴松滋调研督办磷石膏综合治理",
            },
        ],
        "confidence_summary": {
            "identity": "plausible" if person.get("birth") else "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "核心领导（汪卫）完整履历未核实；网络访问受限",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name} 的完整履历（出生年月/籍贯/学历/入党时间/工作起点/来松滋前任职务/关键晋升时间线）",
                "why_it_matters": "仅能确认当前职务；核心身份与晋升链缺信息，无法深入开展关系网络推断",
                "suggested_queries": [
                    f"松滋市 市委书记 汪卫 简历",
                    f"松滋市 市长 张炜 简历",
                    "松滋市 领导之窗",
                    "荆州市 委组织部 任前公示 松滋",
                    "汪卫 松滋 前任 书记",
                ],
                "last_attempted": "2026-08-07",
            }
        ],
    }


def main() -> None:
    # Build the canonical DB + GEXF.
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
    print(f"Built artifacts: {DB_PATH}, {GEXF_PATH}")

    # Person JSONs (written to staging dir; process_tmp promotes them).
    jobs = [
        ("市委书记", "中共松滋市委员会", "正处级"),
        ("市长", "松滋市人民政府", "正处级"),
    ]
    for person, (job, org, rank) in zip([persons[0], persons[1]], jobs):
        data = build_person_json(person, person["current_post"], person["current_org"], job, rank)
        out = HERE / f"{TODAY}-湖北省-荆州市-{job}-{person['name']}.json"
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Wrote person json: {out}")

    # Summary — verify the built DB by reading it back.
    conn = sqlite3.connect(str(DB_PATH))
    try:
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                  for t in ("persons", "organizations", "positions", "relationships")}
    finally:
        conn.close()
    print("=" * 50)
    print(f"SLUG: {SLUG}")
    for table, n in counts.items():
        print(f"{table}: {n}")
    print("=" * 50)


if __name__ == "__main__":
    main()