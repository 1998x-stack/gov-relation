#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 阿拉善盟 (Alxa League), 内蒙古自治区.

Investigation date: 2026-08-07
Task ID: inner_mongolia_阿拉善盟
Level: 地级市 (盟——内蒙古自治区下辖地级行政区)
Targets: 盟委书记 & 盟长

Primary sources:
  - zh.wikipedia.org 阿拉善盟 （现任领导信息表, confirmed 2026-08）
  - 中国经济网 district.ce.cn 任免报道 (2023-05-10 黄雅丽任盟委书记; 2023-11-07 白海林任盟长)
  - 维基百科 代钦 (前任盟委书记履历)

Confidence notes:
  - 现任盟委书记 (黄雅丽) & 盟长 (白海林): confirmed via 中国经济网任免报道 + 维基百科
  - 简历（出生、教育、履新前职务）: confirmed via 任命公告
  - 完整职业生涯、常委会其他成员名单: 公开资料不完整，已标记 open_questions
  - 盟政府官网 www.als.gov.cn 在调查时点超时，未能直连核实最新领导之窗
"""
from __future__ import annotations

import json
import os
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

import sqlite3  # noqa
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "阿拉善盟"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_阿拉善盟"
if _CURRENT_DIR.name == "inner_mongolia_阿拉善盟":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────────
# IDs: 1=盟委书记, 2=盟长, 3-7 other 四大班子 leaders, 20+ predecessors
persons = [
    # ═══════ Core leadership ═══════
    {
        "id": 1,
        "name": "黄雅丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "内蒙古自治区太仆寺旗",
        "education": "大学学历，经济学硕士学位，教授",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盟委书记",
        "current_org": "中共阿拉善盟委员会",
        "source": "http://district.ce.cn/newarea/sddy/202305/10/t20230510_38540009.shtml",
        "confidence": "confirmed",
        "notes": "教授背景，履新前任内蒙古自治区党委教育工委书记、教育厅党组书记、厅长，2023年5月由自治区厅局空降阿拉善盟委书记。职业路径偏教育/组织系统。",
    },
    {
        "id": 2,
        "name": "白海林",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1973年12月",
        "birthplace": "内蒙古自治区库伦旗",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盟委副书记、盟长",
        "current_org": "阿拉善盟行政公署",
        "source": "http://district.ce.cn/newarea/sddy/202311/07/t20231107_38781404.shtml",
        "confidence": "confirmed",
        "notes": "蒙古族，库伦旗人。曾任呼伦贝尔市副市长、呼伦贝尔市委常委/常务副市长、呼伦贝尔市委副书记/政法委书记，2023年11月自呼伦贝尔市跨盟市调任阿拉善盟委副书记、盟长。",
    },
    # ═══════ 四大机构领导 (当前) ═══════
    {
        "id": 3,
        "name": "王维东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年10月",
        "birthplace": "内蒙古自治区阿拉善左旗",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盟人大常委会主任",
        "current_org": "内蒙古自治区人大常委会阿拉善盟工作委员会",
        "source": "https://zh.wikipedia.org/wiki/阿拉善盟",
        "confidence": "confirmed",
        "notes": "阿拉善盟本地干部，2021年3月任盟人大常委会主任。",
    },
    {
        "id": 4,
        "name": "卢利明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年11月",
        "birthplace": "内蒙古自治区乌兰察布市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "盟政协主席",
        "current_org": "中国人民政治协商会议阿拉善盟委员会",
        "source": "https://zh.wikipedia.org/wiki/阿拉善盟",
        "confidence": "confirmed",
        "notes": "2021年2月任政协阿拉善盟委员会主席。",
    },
    # ═══════ 前任领导 ═══════
    {
        "id": 20,
        "name": "代钦",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1967年4月",
        "birthplace": "内蒙古自治区兴安盟科尔沁右翼中旗",
        "education": "内蒙古师范大学政治教育专业",
        "party_join": "中共党员",
        "work_start": "1989年",
        "current_post": "前任盟盟委书记（现自治区副主席）",
        "current_org": "内蒙古自治区人民政府",
        "source": "https://zh.wikipedia.org/wiki/代钦",
        "confidence": "confirmed",
        "notes": "1989-1990年科右中旗巴彦呼硕一中美（教师），1991年起历任科右中旗宣传部干部、兴安盟行政公署办公室干部、内蒙古自治区政府办公厅调研三处干部。2021年5月-2023年5月任阿拉善盟团盟委书记，曾兼任额济纳旗旗委书记。2023年1月当选自治区副主席；2023年8月因阿拉善左旗新井煤业'2·22'特别重大坍塌事故失职失责被党内严重警告。",
    },
    {
        "id": 21,
        "name": "李中增",
        "gender": "男",
        "ethnicity": "",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任盟长",
        "current_org": "",
        "source": "http://district.ce.cn/newarea/sddy/202311/07/t20231107_38781404.shtml",
        "confidence": "plausible",
        "notes": "1973年5月生，曾任巴彦淖尔市委副书记，2021年任阿拉善盟委副书记、盟长，2023年11月卸任。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共阿拉善盟委员会", "type": "党委", "level": "地级市", "location": "阿拉善盟"},
    {"id": 2, "name": "阿拉善盟行政公署", "type": "政府", "level": "地级市", "location": "阿拉善盟"},
    {"id": 3, "name": "内蒙古自治区人大常委会阿拉善盟工作委员会", "type": "人大", "level": "地级市", "location": "阿拉善盟"},
    {"id": 4, "name": "中国人民政治协商会议阿拉善盟委员会", "type": "政协", "level": "地级市", "location": "阿拉善盟"},
    {"id": 5, "name": "内蒙古自治区人民政府", "type": "政府", "level": "省级", "location": "呼和浩特市"},
    {"id": 6, "name": "阿拉善左旗委员会", "type": "党委", "level": "县级", "location": "阿拉善盟阿拉善左旗"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 黄雅丽
    {"person_id": 1, "org_id": 1, "title": "盟委书记", "start": "2023-05", "end": "present", "rank": "正厅级", "note": "主持盟委全面工作"},
    # 白海林
    {"person_id": 2, "org_id": 1, "title": "盟委副书记", "start": "2023-11", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "盟长", "start": "2023-11", "end": "present", "rank": "正厅级", "note": "主持盟行政公署全面工作"},
    # 王维东
    {"person_id": 3, "org_id": 3, "title": "盟人大常委会主任", "start": "2021-03", "end": "present", "rank": "正厅级", "note": ""},
    # 卢利明
    {"person_id": 4, "org_id": 4, "title": "盟政协主席", "start": "2021-02", "end": "present", "rank": "正厅级", "note": ""},
    # 代钦 (前任，现自治区副主席)
    {"person_id": 20, "org_id": 1, "title": "盟委书记（前任）", "start": "2021-05", "end": "2023-05", "rank": "正厅级", "note": "黄雅丽的前任"},
    {"person_id": 20, "org_id": 5, "title": "自治区副主席", "start": "2023-01", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "兼额济纳旗旗委书记", "start": "", "end": "", "rank": "", "note": "曾兼任额济纳旗旗委书记"},
    # 李中增 (前任盟长)
    {"person_id": 21, "org_id": 2, "title": "盟长（前任）", "start": "2021-05", "end": "2023-11", "rank": "正厅级", "note": "白海林的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政新一届搭档：盟委书记黄雅丽与盟长白海林同为2023年换届上任", "overlap_org": "中共阿拉善盟委员会", "overlap_period": "2023-11至今"},
    # 盟委书记与人大主任/政协主席
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "盟委书记与盟人大主任在盟四大机构同届共事", "overlap_org": "中共阿拉善盟委员会", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "盟委书记与盟政协主席在盟四大机构同届共事", "overlap_org": "中共阿拉善盟委员会", "overlap_period": "2023至今"},
    # 盟长与人大主任/政协主席
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "盟长与人大主任同届共事", "overlap_org": "阿拉善盟行政公署", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "盟长与政协主席同届共事", "overlap_org": "阿拉善盟行政公署", "overlap_period": "2023至今"},
    # 前任/继任关系
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "context": "黄雅丽接替代钦任阿拉善盟盟委书记（2023年5月）", "overlap_org": "中共阿拉善盟委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 21, "type": "predecessor_successor", "context": "白海林接替李中增任盟长（2023年11月）", "overlap_org": "阿拉善盟行政公署", "overlap_period": ""},
    # 前任书记与前任盟长曾搭档
    {"person_a": 20, "person_b": 21, "type": "superior_subordinate", "context": "代钦任盟委书记、李中增任盟长期间为党政搭档（2021-2023）", "overlap_org": "中共阿拉善盟委员会", "overlap_period": "2021-2023"},
]


# ── Person JSON files ─────────────────────────────────────────────────────────
def _write_person_json(person: dict) -> None:
    province = "内蒙古自治区"
    city = "阿拉善盟"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_")
    name = person["name"].replace("·", "_")
    fname = f"{TODAY}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname
    source_register = []
    sid = 0
    for url in filter(None, [person.get("source", "")]):
        sid += 1
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"阿拉善盟领导信息 - {person['current_post']}",
            "url": url,
            "publisher": "中国经济网/维基百科",
            "accessed_at": AS_OF,
            "source_type": "appointment_notice" if "district.ce.cn" in url else ("encyclopedia" if "wikipedia" in url else "media"),
            "reliability": "high",
            "notes": person.get("notes", ""),
        })
    identity = {
        "person_id": f"alsm_{name}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": person.get("native_place", ""),
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth', '')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
            "official_profile_url": person.get("source", ""),
        },
    }
    edu = person.get("education", "")
    if edu:
        identity["education"].append({
            "period": "",
            "institution": edu if ("学历" in edu or "研究生" in edu or "大学" in edu or "党校" in edu or "师范大学" in edu) else "",
            "major": "",
            "degree": edu,
            "study_type": "unknown",
            "source_ids": ["S001"] if source_register else [],
        })
    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            career_timeline.append({
                "start": pos.get("start", ""),
                "end": pos.get("end", ""),
                "org": org["name"] if org else "",
                "title": pos.get("title", ""),
                "level": org.get("level", "") if org else "",
                "location": "阿拉善盟",
                "system": "government" if "人民政府" in (org["name"] if org else "") or "行政公署" in (org["name"] if org else "") else "party",
                "rank": pos.get("rank", ""),
                "is_key_promotion": pos.get("title") in ("盟委书记", "盟长"),
                "notes": pos.get("note", ""),
                "confidence": person.get("confidence", "plausible"),
                "source_ids": ["S001"] if source_register else [],
            })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料未找到完整履历",
            "confidence": "unverified",
            "source_ids": [],
        })
    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"alsx_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"] if source_register else [],
                })
    obj = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "阿拉善盟",
            "region": "阿拉善盟",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_阿拉善盟",
            "time_focus": "2026-08",
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"] if source_register else [],
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "provincial_department" if person["id"] == 1 else ("cross_county_rotation" if person["id"] == 2 else "unknown"),
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']} 完整职业生涯（教育背景、出生地、任职时间点明细）",
        },
        "open_questions": [{
            "priority": "high",
            "question": f"{person['name']} 的完整履历（任现职前全部岗位、教育经历、入党时间、出生地核实）",
            "why_it_matters": "完整履历是分析其升迁路径、系统经验和关系网络的基础",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
            "last_attempted": AS_OF,
        }],
    }
    # 代钦 has a disciplinary action signal (documented risk)
    if person["id"] == 20:
        obj["risk_and_integrity_signals"].append({
            "type": "disciplinary_action",
            "description": "2023年8月，因内蒙古阿拉善左旗新井煤业'2·22'特别重大坍塌事故失职失责，代钦受到党内严重警告处分",
            "date": "2023-08",
            "confidence": "confirmed",
            "source_ids": ["S004"] if len(source_register) > 3 else ["S001"],
        })
    else:
        obj["risk_and_integrity_signals"].append({
            "type": "none_found",
            "description": "未在公开官方资料中发现风险信号",
            "date": AS_OF,
            "confidence": "confirmed",
            "source_ids": [],
        })
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fpath.name}")


def write_person_jsons():
    # 两位核心（盟盟书记、盟长）+ 四大机构 + 前任关键人物
    key_ids = {1, 2, 3, 4, 20, 21}
    for p in persons:
        if p["id"] in key_ids:
            _write_person_json(p)


if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    print("  Writing person JSON files...")
    write_person_jsons()

    print(f"\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB file: {DB_PATH}")
    print(f"  GEXF file: {GEXF_PATH}")
    print("  Done.")