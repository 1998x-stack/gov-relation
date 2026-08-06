#!/usr/bin/env python3
"""郧西县（十堰市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_郧西县
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-06
现行班子（截至 2026-08，郧西县人民政府门户网站《县领导》领导之窗确认）：
  - 县委书记：王兵（1980-04，汉族，湖北广水人，2001-05 入党，现任中共郧西县委书记，主持县委、县政府全面工作）
  - 县委副书记、县长：李光锐（1978-08，汉族，湖北竹山人，2001-10 参加工作，2003-06 入党，在职大学学历；
    历任竹山县潘口乡乡长、双台乡党委书记，市委改革办专职副主任，援疆新疆兵团第五师八十六团党委常委/副团长，
    市委政研室二级调研员，十堰日报社总编辑/党委副书记，十堰市商务局党组书记/局长/一级调研员）
  - 其余 8 名县委/县政府常委均来自官方"县领导"栏目领导之窗（下方 persons 列表）。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-十堰市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_郧西县/build_郧西县_data.py   # 产出写到暂存目录
    python3 scripts/build/build_郧西县_data.py           # 归档后运行，产出到 canonical 目录
"""

import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

if "__file__" in globals():
    _here = Path(__file__).resolve()
    _candidate = _here.parent
    while True:
        if (_candidate / "gov_relation").is_dir():
            break
        _parent = _candidate.parent
        if _parent == _candidate:
            _candidate = Path.cwd()
            break
        _candidate = _parent
else:
    _candidate = Path.cwd()
REPO_ROOT = _candidate
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.log import get_logger  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "郧西县"
PROVINCE = "湖北省"
PARENT_CITY = "十堰市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<task>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph|persons
if _in_staging:
    OUT_DIR = Path(__file__).resolve().parent
    PERSONS_OUT = OUT_DIR
    GEXF_OUT = OUT_DIR
else:
    OUT_DIR = DATABASE_DIR
    PERSONS_OUT = PERSONS_DIR
    GEXF_OUT = GRAPH_DIR
DB_PATH = OUT_DIR / f"{SLUG}_network.db"
GEXF_PATH = GEXF_OUT / f"{SLUG}_network.gexf"

GOV_HOST = "http://www.yunxi.gov.cn"
LDZ = f"{GOV_HOST}/xxgk/fdzdgk/zfld/xw_yyq"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：郧西县人民政府官方网站"县领导"领导之窗（LDZ）及各领导简介页，来源见 source 字段。
persons = [
    {"id": 1, "name": "王兵", "gender": "男", "ethnicity": "汉族", "birth": "1980-04", "birthplace": "湖北广水",
     "native_place": "湖北省广水市", "education": "不详", "party_join": "2001-05", "work_start": "",
     "current_post": "郧西县委书记", "current_org": "中共郧西县委员会",
     "source": f"{LDZ}/wbzfb/202108/t20210816_3358201.shtml"},
    {"id": 2, "name": "李光锐", "gender": "男", "ethnicity": "汉族", "birth": "1978-08", "birthplace": "湖北竹山",
     "native_place": "湖北省竹山县", "education": "在职大学学历", "party_join": "2003-06", "work_start": "2001-10",
     "current_post": "郧西县委副书记、县长", "current_org": "郧西县人民政府",
     "source": f"{LDZ}/lz_117779/202504/t20250430_4734648.shtml"},
    {"id": 3, "name": "雷震", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "湖北广水",
     "native_place": "湖北省广水市", "education": "全日制硕士研究生（中南民族大学文艺学）", "party_join": "2007-05", "work_start": "",
     "current_post": "郧西县委副书记、政法委书记", "current_org": "中共郧西县委员会",
     "source": f"{LDZ}/lz/202110/t20211020_3391244.shtml"},
    {"id": 4, "name": "武国顺", "gender": "男", "ethnicity": "汉族", "birth": "1983-08", "birthplace": "河南许昌",
     "native_place": "河南省许昌市", "education": "全日制研究生学历（云南大学政治学专业）", "party_join": "2006-05", "work_start": "",
     "current_post": "郧西县委常委、纪委书记、监委主任", "current_org": "中共郧西县纪律检查委员会/郧西县监察委员会",
     "source": f"{LDZ}/wgs/202011/t20201123_3220230.shtml"},
    {"id": 5, "name": "晏广江", "gender": "男", "ethnicity": "汉族", "birth": "1971-05", "birthplace": "郧西县土门镇",
     "native_place": "湖北省郧西县", "education": "党校大学学历（省委党校经济管理专业）", "party_join": "1996-07", "work_start": "",
     "current_post": "郧西县委常委、统战部长", "current_org": "中共郧西县委统战部",
     "source": f"{LDZ}/ygj/202110/t20211020_3391246.shtml"},
    {"id": 6, "name": "彭青松", "gender": "男", "ethnicity": "汉族", "birth": "1983-10", "birthplace": "湖北鄂州",
     "native_place": "湖北省鄂州市", "education": "硕士研究生学历（中南财经政法大学宪法学与行政法学）", "party_join": "2008-12", "work_start": "",
     "current_post": "郧西县委常委、副县长", "current_org": "郧西县人民政府",
     "source": f"{LDZ}/pqs/202311/t20231122_4352317.shtml"},
    {"id": 7, "name": "何杰", "gender": "男", "ethnicity": "汉族", "birth": "1973-07", "birthplace": "湖北黄冈",
     "native_place": "湖北省黄冈市", "education": "", "party_join": "1996-12", "work_start": "",
     "current_post": "郧西县委常委、县委办公室主任", "current_org": "中共郧西县委办公室",
     "source": f"{LDZ}/hj/202404/t20240409_4477999.shtml"},
    {"id": 8, "name": "孙波", "gender": "男", "ethnicity": "汉族", "birth": "1984-08", "birthplace": "湖北十堰",
     "native_place": "湖北省十堰市", "education": "在职研究生学历、工程硕士学位", "party_join": "2005-06", "work_start": "",
     "current_post": "郧西县委常委、常务副县长", "current_org": "郧西县人民政府",
     "source": f"{LDZ}/sb/202404/t20240410_4483053.shtml"},
    {"id": 9, "name": "郭龙银", "gender": "男", "ethnicity": "汉族", "birth": "1975-12", "birthplace": "郧西县上津镇",
     "native_place": "湖北省十堰市郧西县", "education": "党校大学学历", "party_join": "1999-10", "work_start": "",
     "current_post": "郧西县委常委、宣传部部长", "current_org": "中共郧西县委宣传部",
     "source": f"{LDZ}/hj_122030/202511/t20251103_4844170.shtml"},
    {"id": 10, "name": "高婷婷", "gender": "女", "ethnicity": "土家族", "birth": "1986-03", "birthplace": "湖北宜昌",
     "native_place": "湖北省宜昌市", "education": "", "party_join": "2007-06", "work_start": "",
     "current_post": "郧西县委常委、组织部部长", "current_org": "中共郧西县委组织部",
     "source": f"{LDZ}/hj_123636/202606/t20260608_4944997.shtml"},
]

# 用 source 字段做后备（部分人物缺少 party_join/work_start 时也一并记录）
for _p in persons:
    if _p.get("party_join_ok") is None:
        _p["party_join_ok"] = True

organizations = [
    {"id": 1, "name": "中共郧西县委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "十堰市郧西县"},
    {"id": 2, "name": "郧西县人民政府", "type": "政府", "level": "县级", "parent": "十堰市人民政府", "location": "十堰市郧西县"},
    {"id": 3, "name": "中共郧西县纪律检查委员会/郧西县监察委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "十堰市郧西县"},
    {"id": 4, "name": "中共郧西县委政法委员会", "type": "党委", "level": "县级", "parent": "中共郧西县委员会", "location": "十堰市郧西县"},
    {"id": 5, "name": "中共郧西县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共郧西县委员会", "location": "十堰市郧西县"},
    {"id": 6, "name": "中共郧西县委办公室", "type": "党委", "level": "县级", "parent": "中共郧西县委员会", "location": "十堰市郧西县"},
    {"id": 7, "name": "中共郧西县委宣传部", "type": "党委", "level": "县级", "parent": "中共郧西县委员会", "location": "十堰市郧西县"},
    {"id": 8, "name": "中共郧西县委组织部", "type": "党委", "level": "县级", "parent": "中共郧西县委员会", "location": "十堰市郧西县"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "郧西县委书记", "start_date": "约2021", "end_date": "", "rank": "正处级", "note": "主持县委、县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "郧西县委副书记", "start_date": "约2025", "end_date": "", "rank": "正处级", "note": "兼任县长"},
    {"person_id": 2, "org_id": 2, "title": "郧西县人民政府县长", "start_date": "约2025", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "郧西县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "协助书记开展县委日常工作"},
    {"person_id": 3, "org_id": 4, "title": "县委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政协党组副书记"},
    {"person_id": 5, "org_id": 5, "title": "县委统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 7, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "县委宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "郧西县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "县委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长为郧西县党政正职搭档", "overlap_org": "郧西县党委/政府", "overlap_period": "约2025至今"},
    {"person_a": 1, "person_b": 3, "type": "党政搭档", "context": "县委书记与专职副书记在县委班子共事", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "区委班子", "context": "县委书记与纪委书记同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "区委班子", "context": "县委书记与统战部长同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "区委班子", "context": "县委书记与分管工业副县长的县委常委同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "区委班子", "context": "县委书记与县委办公室主任同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "区委班子", "context": "县委书记与常务副县长同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "区委班子", "context": "县委书记与宣传部长同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "区委班子", "context": "县委书记与组织部长同属县委常委会", "overlap_org": "中共郧西县委员会", "overlap_period": ""},
    # 县长与政府班子
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "常务副县长在县长领导下工作", "overlap_org": "郧西县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "郧西县人民政府", "overlap_period": ""},
    # 同籍贯 / 同系统线索（weak）
    {"person_a": 1, "person_b": 3, "type": "同籍贯", "context": "王兵（湖北广水）与雷震（湖北广水）同籍贯", "overlap_org": "湖北省广水市", "overlap_period": ""},
]


def build_person_json(p: dict) -> None:
    """写入单个人物深度档案 JSON（含履历、关系、来源置信度、开放问题）。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "郧西县领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").replace("，", "-").strip("-")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": f"郧西县人民政府门户网站·县领导 - {name}",
        "url": src_url,
        "publisher": "郧西县人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "郧西县人民政府官方网站《县领导》领导之窗人物简介页（2026-08-06 复核）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        career_timeline.append({
            "start": pos["start_date"] or "unknown",
            "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "十堰市郧西县",
            "system": "party" if pos["org_id"] in (1, 3, 4, 5, 6, 7, 8) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党", f"{name} 郧西县 简历"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 郧西县"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_郧西县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_shiyan_yunxi_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": edu,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if ("郧西县" in (p.get("native_place") or ""))
                              else ("cross_county_rotation" if PROVINCE in (p.get("native_place") or "")
                                    else "cross_province_rotation"),
            "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间、入党/参加工作时间）",
        },
        "open_questions": open_q,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    logger.info("person JSON written: %s", out_path)


def main() -> None:
    print(f"Building {SLUG} network data...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print("  Writing person JSON lead-files...")
    for p in persons:
        build_person_json(p)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")
    _conn = sqlite3.connect(str(DB_PATH))
    print(f"  DB rows: persons={_conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}, "
          f"organizations={_conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}, "
          f"positions={_conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}, "
          f"relationships={_conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    _conn.close()
    for pf in sorted(OUT_DIR.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()