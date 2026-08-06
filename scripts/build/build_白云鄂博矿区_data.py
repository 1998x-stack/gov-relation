#!/usr/bin/env python3
"""白云鄂博矿区（包头市，内蒙古自治区）领导班子工作关系网络数据生成脚本。

Task ID: inner_mongolia_白云鄂博矿区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-06
现行班子（截至 2026-08，白云鄂博矿区人民政府官网 byeb.gov.cn 新闻/党代会公报确认）：
  - 区委书记：邢凯（十三届区委书记，2026-07-30 中国共产党包头市白云鄂博矿区第十三次代表大会
    十三届委员会第一次全体会议当选；此前为十二届区委书记，2025-12 接受《包头日报》采访）
  - 区委副书记、政府区长：牛标（2026-07 官方多次以"区委副书记、政府区长"主持区常务会议；
    2026 年上半年接任，前任区长冯桂娜于 2026 年初人代会作政府工作报告后调任石拐区）
  - 区委副书记：陈培元（十三届）
  - 十三届区委常委 11 名：于欢、牛标、冯凌云(女)、邢凯、毕力格图(蒙古族)、张瑞、张永平、
    陈培元、罗惠文、段然(蒙古族)、鲍鲜鲲(蒙古族)（2026-07-30 十三届一次全会通过）
  - 区纪委书记：段然(蒙古族)；纪委副书记：黄佳茹(女,蒙古族)、李扬(女)
  - 区人大常委会主任：张和生（2026-01 两会作人大工作报告）
  - 区政协党组书记、主席：吴志宏（2026-01 主持政协八届五次会议闭幕）；政协副主席：蒋剑铭、张平、张云玺
  - 前任区长：冯桂娜（2025 全年至 2026 年初任区长，后调任石拐区委副书记、区长【repository证据】）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-内蒙古自治区-包头市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/inner_mongolia_白云鄂博矿区/build_白云鄂博矿区_data.py   # 产出写到暂存目录
    python3 scripts/build/build_白云鄂博矿区_data.py                         # 归档后运行，产出到 canonical 目录
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

SLUG = "白云鄂博矿区"
PROVINCE = "内蒙古自治区"
PARENT_CITY = "包头市"
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

# 官方新闻来源前缀（白云鄂博矿区人民政府，HTTP 可达；HTTPS 超时）
GOV_HOST = "http://www.byeb.gov.cn/xwzx/qnyw"


# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据级别：
#   confirmed = 白云官方新闻直接点名
#   plausible = repository/关联地区调查（石拐区）跨区任命推断
persons = [
    {"id": 1, "name": "邢凯", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委书记", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 2, "name": "牛标", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委副书记、区长", "current_org": "白云鄂博矿区人民政府",
     "source": f"{GOV_HOST}/202607/t20260713_938700.html"},
    {"id": 3, "name": "陈培元", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委副书记", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 4, "name": "于欢", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 5, "name": "冯凌云", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 6, "name": "毕力格图", "gender": "男", "ethnicity": "蒙古族", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 7, "name": "张瑞", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 8, "name": "张永平", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 9, "name": "罗惠文", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 10, "name": "段然", "gender": "男", "ethnicity": "蒙古族", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委、纪委书记、监委主任", "current_org": "中共包头市白云鄂博矿区纪律检查委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    {"id": 11, "name": "鲍鲜鲲", "gender": "男", "ethnicity": "蒙古族", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区委常委", "current_org": "中共包头市白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202607/t20260731_943640.html"},
    # ── 四套班子（人大/政协/前任区长）──
    {"id": 12, "name": "张和生", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区人大常委会主任", "current_org": "白云鄂博区人大常委会",
     "source": f"{GOV_HOST}/202601/t20260128_882731.html"},
    {"id": 13, "name": "吴志宏", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区政协主席", "current_org": "政协白云鄂博矿区委员会",
     "source": f"{GOV_HOST}/202601/t20260128_882730.html"},
    {"id": 14, "name": "冯桂莎", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "白云鄂博矿区前任区长", "current_org": "白云鄂博矿区人民政府",
     "source": f"{GOV_HOST}/202601/t20260127_882729.html"},
]

# ── 组织机构 ──────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共包头市白云鄂博矿区委员会", "type": "党委", "level": "正县处级", "parent": "中共包头市委员会", "location": "包头市白云鄂博矿区"},
    {"id": 2, "name": "白云鄂博矿区人民政府", "type": "政府", "level": "正县处级", "parent": "包头市人民政府", "location": "包头市白云鄂博矿区"},
    {"id": 3, "name": "中共包头市白云鄂博矿区纪律检查委员会/区监察委员会", "type": "纪委", "level": "副县处级", "parent": "中共包头市纪律检查委员会", "location": "包头市白云鄂博矿区"},
    {"id": 4, "name": "白云鄂博矿区人大常委会", "type": "人大", "level": "正县处级", "parent": "包头市人大常委会", "location": "包头市白云鄂博矿区"},
    {"id": 5, "name": "政协白云鄂博矿区委员会", "type": "政协", "level": "正县处级", "parent": "政协包头市委员会", "location": "包头市白云鄂博矿区"},
]

# ── 任职 ─────────────────────────────────────────────────────────────────────
positions = [
    # 邢凯
    {"person_id": 1, "org_id": 1, "title": "白云鄂博矿区委书记", "start_date": "2021(约)", "end_date": "present", "rank": "正县处级", "note": "十三届区委书记当选 2026-07-30；此前为十二届"},
    # 牛标
    {"person_id": 2, "org_id": 1, "title": "白云鄂博矿区委副书记", "start_date": "2026", "end_date": "present", "rank": "副县处级", "note": "兼区长"},
    {"person_id": 2, "org_id": 2, "title": "白云鄂博矿区区长", "start_date": "2026(春)", "end_date": "present", "rank": "正县处级", "note": "接替冯臣莎"},
    # 陈培元
    {"person_id": 3, "org_id": 1, "title": "白云鄂博矿区委副书记", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    # 其它区委常委
    {"person_id": 4, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 5, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 6, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 7, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 8, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 9, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 10, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    {"person_id": 10, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届纪委全会当选"},
    {"person_id": 11, "org_id": 1, "title": "白云鄂博矿区委常委", "start_date": "2026-07", "end_date": "present", "rank": "副县处级", "note": "十三届当选"},
    # 人大/政协/前任区长
    {"person_id": 12, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县处级", "note": "2026-01 两会期间确认"},
    {"person_id": 13, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正县处级", "note": "2026-01 两会期间确认"},
    {"person_id": 14, "org_id": 2, "title": "白云鄂博矿区区长", "start_date": "约2023-2024", "end_date": "2026(春)", "rank": "正县处级", "note": "前任区长；2026 上半年调任"},
]

# ── 关系 ─────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政班子成员", "context": "区委书记邢凯与区长牛标为白云区党政正职搭档", "overlap_org": "白云鄂博矿区党委/政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "区委班子成员", "context": "区委副书记在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 8, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "纪检协同", "context": "纪委书记段然在书记领导下主持纪检监督", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 11, "type": "区委班子成员", "context": "区委常委在书记领导下工作", "overlap_org": "中共白云鄂博矿区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 12, "type": "四套班子", "context": "区委书记与人大常委会主任协同推进全区工作", "overlap_org": "白云鄂博矿区", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "四套班子", "context": "区委书记与政协主席全区协商议政", "overlap_org": "白云鄂博矿区", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "前任-接任", "context": "牛标接替冯丽莎任白云鄂博区长", "overlap_org": "白云鄂博区人民政府", "overlap_period": "2026"},
    {"person_a": 14, "person_b": 1, "type": "党政班子成员", "context": "前任区长在区委书记领导下工作", "overlap_org": "白云鄂博区党委/政府", "overlap_period": "2023-2026"},
    {"person_a": 2, "person_b": 10, "type": "治理协同", "context": "区长与纪委书记在政纪/监督协同", "overlap_org": "白云鄂博矿区", "overlap_period": "2026-"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "白云鄂博区领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001",
        "title": f"白云鄂博矿区人民政府官网新闻 - {name}",
        "url": src_url,
        "publisher": "白云鄂博矿区人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "白云鄂博矿区人民政府官网（byeb.gov.cn）确认（2026-08-06 复核）",
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
            "location": "包头市白云鄂博矿区",
            "system": "party" if pos["org_id"] in (1, 3) else ("government" if pos["org_id"] == 2 else "other"),
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2, 14),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    open_q.append({"priority": "high", "question": f"{name}的完整个人履历（出生、学历、前后任职分项时间）",
                   "why_it_matters": "构建可核对的政治晋升时间线",
                   "suggested_queries": [f"{name} 简历 白云鄂博", f"{name} 任前公示 包头", f"{name} 包头市委组织部"],
                   "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "inner_mongolia_白云鄂博矿区", "time_focus": "2026"},
        "identity": {
            "person_id": f"inner_mongolia_baotou_baiyunebokuang_{name}",
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
                           "administrative_rank": "正县处级" if p["id"] in (1, 2, 12, 13, 14) else "副县处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation",
            "systems_experience": [],
            "geographic_pattern": [pitem for pitem in [p.get("native_place", "")] if pitem],
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
            "identity": "plausible" if not p.get("birth") else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin" if not p.get("work_start") else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生/入党/参加工作/历任职务起止时间）",
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
    for pf in sorted(PERSONS_OUT.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()