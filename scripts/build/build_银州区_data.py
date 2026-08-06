#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 银州区, 铁岭市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_银州区
Level: 市辖区
Targets: 区委书记(待查) & 区长(高海峰)

Research sources (accessed 2026-08-06):
  - www.tlyz.gov.cn — 铁岭市银州区人民政府门户网站 (official, primary, reachable via curl_cffi over HTTP)
      * 机关简介·区政府领导·区长 高海峰 - /zfxxgk/fdzdgknr1/jgjj/qzfld/qz/2022041516520329555/index.html (2024-11-20)
      * 机关简介·区政府领导·副区长 訾宏宇/王凯/王占林/邓宇/康丽/刘泽坤 - /jgjj/qzfld/fqz/* (2024-2026)
      * 十一届区政府第64-69次常务会议纪要 (2025-11 至 2026-03) 记录班子名单与参会副区长

Confidence notes:
  - 现任区长 高海峰 — confirmed (区政府门户领导页 + 多份常务会议纪要"区长高海峰主持")
  - 现任副区长 訾宏宇(常委/常务)、王凯(常委)、王占林、邓宇、康丽、刘泽坤 — confirmed (区政府门户领导页)
  - 部分副区长(赵宝丹、郎玉芳)在 2026 常务会议纪要中出现但不在当前领导页——或已离任/任职状态存疑, 未列入现任
  - 现任区委书记 — unresolved. 银州区政府门户仅公开区政府领导班子, 区委书记未公开;
    Exa 限流、Baidadu 验证码、搜狗反爬、Bing 丢弃查询、直连与 Jina 超时,Baitune 外部渠道在本环境中不可达。
    故我区区委书记暂记「待查_区委书记」(沿用仓库既有通化市「待查_县委书记」约定), 属 critical 缺口。
  - 核心领导(高海峰等)任现职前的完整履历 —— open_questions / open_gaps
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
SLUG = "银州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
if _CURRENT_DIR.name == "liaoning_银州区" or (_CURRENT_DIR / "银州区_network.db").parent.name.startswith("tmp"):
    STAGING = _CURRENT_DIR
else:
    STAGING = REPO_ROOT / "data/tmp/liaoning_银州区"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

SRC_GOV = "http://www.tlyz.gov.cn/（铁岭市银州区人民政府门户网站，官方一手，领导页/常务会议纪要）"
SRC_MEET = "http://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/zfhy/zfhy/（银州区十一届区政府常务会议纪要）"
SRC_QW_PENDING = "待查-区委书记（区政府门户仅有政府班子，区委书记未公开；外部渠道不可达）"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══ 核心：区长(已确认) & 区委书记(待查) ═══════════════════════════════
    {
        "id": 1,
        "name": "高海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-02",
        "birthplace": "",
        "education": "全日制大专，在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/qz/2022041516520329555/index.html",
    },
    {
        "id": 2,
        "name": "待查_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共铁岭市银州区委",
        "source_url": "",
        "is_pending": True,
    },
    # ═══ 副区长（区政府领导班子，已确认） ═══════════════════════════════════
    {
        "id": 3,
        "name": "訾宏宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-09",
        "birthplace": "",
        "education": "全日制本科，在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、常务副区长",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2025112115000836928/index.html",
    },
    {
        "id": 4,
        "name": "王凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2025022416413837491/index.html",
    },
    {
        "id": 5,
        "name": "王占林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局党委书记、局长（兼市公安局反恐专员）",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2025092908491175396/index.html",
    },
    {
        "id": 6,
        "name": "邓宇",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1980-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2024082609445554965/index.html",
    },
    {
        "id": 7,
        "name": "康丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2026070609442971673/index.html",
    },
    {
        "id": 8,
        "name": "刘泽坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-06",
        "birthplace": "",
        "education": "工学博士",
        "party_join": "致公党党员",
        "work_start": "",
        "current_post": "政府班子副职（挂职锻炼）",
        "current_org": "铁岭市银州区人民政府",
        "source_url": "https://www.tlyz.gov.cn/yinzhou/zfxxgk/fdzdgknr1/jgjj/qzfld/fqz/2025022611221261173/index.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共铁岭市银州区委", "type": "party_committee", "level": "县处级", "parent": "中共铁岭市委", "location": "银州区"},
    {"id": 2, "name": "铁岭市银州区人民政府", "type": "government", "level": "县处级", "parent": "铁岭市人民政府", "location": "银州区"},
    {"id": 3, "name": "铁岭市银州区人大常委会", "type": "npc", "level": "县处级", "parent": "", "location": "银州区"},
    {"id": 4, "name": "政协铁岭市银州区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "银州区"},
    {"id": 5, "name": "中共铁岭市银州区纪委区监委", "type": "discipline", "level": "县处级", "parent": "铁岭市纪委", "location": "银州区"},
    {"id": 6, "name": "铁岭市银州区公安分局", "type": "government", "level": "科级", "parent": "铁岭市公安局", "location": "银州区"},
    {"id": 7, "name": "铁岭银州经济开发区管委会", "type": "development_zone", "level": "县处级", "parent": "银州区人民政府", "location": "银州区"},
    {"id": 8, "name": "中共铁岭市委", "type": "party_committee", "level": "地厅级", "parent": "中共辽宁省委", "location": "铁岭市"},
    {"id": 9, "name": "铁岭市人民政府", "type": "government", "level": "地厅级", "parent": "辽宁省人民政府", "location": "铁岭市"},
]
organizations = [o for o in organizations if isinstance(o, dict) and "name" in o]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 高海峰 区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "现任区委副书记、区政府党组书记、区长；分管经济开发区管委会和区审计局"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委班子成员"},
    # 待查 区委书记
    {"person_id": 2, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待确认（待查）；区政府门户未公开区委班子"},
    # 訾宏宇 常务
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长（党组副书记）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王凯
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长（党组成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管工业、科技、民营经济、农业农村等"},
    # 王占林
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "另任市公安局反恐专员"},
    {"person_id": 5, "org_id": 6, "title": "区公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "科级", "note": ""},
    # 邓宇
    {"person_id": 6, "org_id": 2, "title": "副区长（党组成员）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管商务、外事等"},
    # 康丽
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管教育、文化旅游、卫健等"},
    # 刘泽坤
    {"person_id": 8, "org_id": 2, "title": "政府班子副职（挂职锻炼）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "工学博士，致公党党员"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 区长—政府班子（上下级/搭档）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区长—常务副区长(党组副书记)", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区长—副区长/公安局长", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区长—挂职副职(锻炼服务)", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    # 常务——其他副区（政府内层级）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "常务副区长—副区长(同政府班子、常委会包络)", "overlap_org": "铁岭市银州区人民政府", "overlap_period": "2026"},
    # 区委常委链接（区委->常委会体）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区长(区委副书记)—区委书记(待查)", "overlap_org": "中共铁岭市银州区委", "overlap_period": "", "confidence": "unverified"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "区委常委—区委书记(待查)", "overlap_org": "中共铁岭市银州区委", "overlap_period": "", "confidence": "unverified"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "区委常委—区委书记(待查)", "overlap_org": "中共铁岭市银州区委", "overlap_period": "", "confidence": "unverified"},
]

# ── Person JSON ────────────────────────────────────────────────────────────
_RANK_BY_ID = {
    1: "正处级",  # 区长
    2: "县处级正职",  # 区委书记(待查)
    3: "副处级",  # 常务副区长/常委
    4: "副处级",
    5: "副处级",
    6: "副处级",
    7: "副处级",
    8: "副处级",
}


def _write_person_json(person: dict, out_dir: Path) -> None:
    job_tag = person.get("current_post") or person["name"]
    raw_name = TODAY + "-辽宁省-铁岭市-" + job_tag + "-" + person["name"] + ".json"
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", raw_name)
    filepath = out_dir / safe_name
    pend = person.get("is_pending", False)
    has_src = bool(person.get("source_url") or person.get("source"))
    ident_conf = "unverified" if pend else ("confirmed" if has_src else "unverified")
    role_conf = "unverified" if pend else ("confirmed" if has_src else "plausible")
    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "铁岭市",
            "region": "银州区",
            "job": job_tag,
            "task_id": "liaoning_银州区",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": "yinzhou_" + person["name"],
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "", "institution": "", "major": "",
                "degree": person.get("education", ""), "study_type": "unknown", "source_ids": [],
            }],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": person["name"] + "_" + person.get("birth", ""),
                "official_profile_url": person.get("source_url", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": _RANK_BY_ID.get(person["id"], "副处级"),
            "as_of": AS_OF,
            "is_current_confirmed": not pend,
            "source_ids": [],
        },
        "career_timeline": [{
            "start": "",
            "end": "present" if person.get("current_post") else "",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "",
            "location": "银州区",
            "system": "party" if "区委" in str(person.get("current_org", "")) else "government",
            "rank": _RANK_BY_ID.get(person["id"], ""),
            "is_key_promotion": False,
            "notes": "区政府门户领导页确认" if has_src and not pend else "身份/履历待核",
            "confidence": role_conf,
            "source_ids": ["S001"] if (has_src and not pend) else [],
        }],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [person.get("current_post", "")],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [{
            "id": "S001",
            "title": "铁岭市银州区人民政府门户网站·机关简介·区政府领导",
            "url": person.get("source_url", "https://www.tlyz.gov.cn/"),
            "publisher": "铁岭市银州区人民政府",
            "source_type": "official",
            "reliability": "high",
        }] if not pend else [],
        "confidence_summary": {
            "identity": ident_conf,
            "current_role": role_conf,
            "career_completeness": "thin",
            "relationship_confidence": "low" if pend else "medium",
            "biggest_gap": "任现职前的完整工作履历与精确在职时间" if not pend else
                "区委书记姓名完全未知。区政府门户仅有政府班子；区委书记载于市委组织部/辽望等在本环境中不可达的外部渠道。",
        },
        "open_questions": [{
            "priority": "critical" if pend else "high",
            "question": ("银州区区委书记姓名是什么？" if pend else
                        person["name"] + "任现职前的完整履历与精确时间线"),
            "why_it_matters": "区委书记是两大核心目标之一，须确认姓名与身份才能完成工作关系网络" if pend else "判断晋升路径与跨区交流网络",
            "suggested_queries": [] if pend else [person["name"] + " 简历"],
            "last_attempted": TODAY,
        }],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Person JSON for all figures (incl. 待查_区委书记)
    for i, p in enumerate(persons):
        kp = dict(p)
        fpath = _write_person_json(kp, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF via runner (uses gov_relation schema/gexf)
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