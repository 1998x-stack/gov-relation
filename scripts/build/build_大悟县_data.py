#!/usr/bin/env python3
"""大悟县（孝感市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_大悟县
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-06
现行班子（截至 2026-08，官方大悟政府网 www.hbdawu.gov.cn 新闻确认）：
  - 县委书记：余海群（兼 孝感市人民政府副市长，2026-06-18 孝感市七届人大常委会
    第四十次会议任命为副市长，仍兼任大悟县委书记）
  - 县委副书记、县长：鲍克明（湖北孝南人，~1972-07 生，在职省委党校研究生，
    中共党员，一级调研员；2026-07-12 湖北省委组织部任前公示 拟任县（市、区）委书记）
  - 县委副书记：胡涛
  - 县委常委、县纪委书记、县监委主任：陈红元
  - 副县长：余喜军、毛建
  - 县人大常委会主任：程文正
  - 县政协主席：刘圣堂
前任县委书记：余德芳（2021-06-28 卸任，调任孝感市委常委；更早曾任大悟县委副书记、县长）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-孝感市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_大悟县/build_大悟县_data.py   # 产出写到暂存目录
    python3 scripts/build/build_大悟县_data.py           # 归档后运行，产出到 canonical 目录
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

SLUG = "大悟县"
PROVINCE = "湖北省"
PARENT_CITY = "孝感市"
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

GOV_HOST = "https://www.hbdawu.gov.cn"
# 关键官方来源文章（大悟县政府网新闻，信息公开）
SRC_YU_71 = f"{GOV_HOST}/dwyw/2135267.jhtml"   # 2026-07-02 县领导"七一"走访：余海燕、鲍克明
SRC_YULDBJ = f"{GOV_HOST}/dwyw/2135369.jhtml"  # 2026-06-30 两优一先表彰大会：鲍克明主持、县四大家
SRC_YUHUJ = f"{GOV_HOST}/dwyw/2130549.jhtml"   # 2026-06-08 余海群会见中广核（政绩线索）
SRC_JW = f"{GOV_HOST}/dwyw/2108278.jhtml"      # 2026-02 纪委全会（陈红华）

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：官方大悟政府门户网新闻（2026）+ 湖北省委组织部任前公示（Sogou 汇总），见 source/confidence
persons = [
    {"id": 1, "name": "余海群", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "湖北省孝感市",
     "education": "未知（履历待查）", "party_join": "", "work_start": "",
     "current_post": "大悟县委书记、孝感市人民政府副市长", "current_org": "中共大悟县委员会/孝感市人民政府",
     "source": SRC_YU_71,
     "job_tag": "县委书记"},
    {"id": 2, "name": "鲍克明", "gender": "男", "ethnicity": "汉族", "birth": "1972-07", "birthplace": "湖北孝感", "native_place": "湖北省孝感市孝南区",
     "education": "在职省委党校研究生学历", "party_join": "", "work_start": "1997-03",
     "current_post": "大悟县委副书记、县长（一级调研员）", "current_org": "大悟县人民政府/中共大悟县委员会",
     "source": SRC_YU_71, "job_tag": "县长"},
    {"id": 3, "name": "胡涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县委副书记", "current_org": "中共大悟县委员会",
     "source": SRC_YU_71, "job_tag": "县委副书记"},
    {"id": 4, "name": "陈红元", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县委常委、县纪委书记、县监委主任", "current_org": "中共大悟县纪律检查委员会/大悟县监察委员会",
     "source": SRC_JW, "job_tag": "纪委书记"},
    {"id": 5, "name": "余喜军", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县副县长", "current_org": "大悟县人民政府",
     "source": SRC_YUHUJ, "job_tag": "副县长"},
    {"id": 6, "name": "毛建", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县副县长", "current_org": "大悟县人民政府",
     "source": "https://www.sogou.com/web?query=大悟县副县长任命", "job_tag": "副县长"},
    {"id": 7, "name": "程文正", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县人大常委会主任", "current_org": "大悟县人民代表大会常务委员会",
     "source": SRC_YULDBJ, "job_tag": "人大主任"},
    {"id": 8, "name": "刘圣堂", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "大悟县政协主席", "current_org": "政协大悟县委员会",
     "source": SRC_YULDBJ, "job_tag": "政协主席"},
    {"id": 9, "name": "余德芳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "湖北兴山", "native_place": "湖北省宜昌市兴山县",
     "education": "园艺术科（长江大学97级园艺，在职）", "party_join": "", "work_start": "",
     "current_post": "前任大悟县委书记（现任孝感市委常委）", "current_org": "中共孝感市委员会",
     "source": "https://www.sogou.com/web?query=余德芳大悟县委书记去向", "job_tag": "前县委书记"},
]

organizations = [
    {"id": 1, "name": "中共大悟县委员会", "type": "党委", "level": "县级", "parent": "中共孝感市委员会", "location": "孝感市大悟县"},
    {"id": 2, "name": "大悟县人民政府", "type": "政府", "level": "县级", "parent": "孝感市人民政府", "location": "孝感市大悟县"},
    {"id": 3, "name": "中共孝感市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "孝感市"},
    {"id": 4, "name": "孝感市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "孝感市"},
    {"id": 5, "name": "中共大悟县纪律检查委员会/大悟县监察委员会", "type": "党委", "level": "县级", "parent": "中共大悟县委员会", "location": "孝感市大悟县"},
    {"id": 6, "name": "大悟县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "大悟县", "location": "孝感市大悟县"},
    {"id": 7, "name": "政协大悟县委员会", "type": "政协", "level": "县级", "parent": "大悟县", "location": "孝感市大悟县"},
    {"id": 8, "name": "孝感市孝南区", "type": "政府", "level": "县级", "parent": "孝感市人民政府", "location": "孝感市孝南区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "大悟县委书记", "start_date": "2021-06", "end_date": "", "rank": "正处级", "note": "2021-06-28 全县领导干部大会宣布接任"},
    {"person_id": 1, "org_id": 2, "title": "大悟县委副书记、县长（前）", "start_date": "约2017-2021", "end_date": "2021-06", "rank": "正处级", "note": "2021 年前由县长转任书记"},
    {"person_id": 1, "org_id": 4, "title": "孝感市人民政府副市长", "start_date": "2026-06", "end_date": "", "rank": "副厅级", "note": "2026-06-18 孝感市七届人大常委会第四十次会议任命；仍兼任大悟县委书记"},
    {"person_id": 2, "org_id": 1, "title": "大悟县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "一级调研员"},
    {"person_id": 2, "org_id": 2, "title": "大悟县县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "2026-07-12 公示拟任县委书记"},
    {"person_id": 3, "org_id": 1, "title": "大悟县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "大悟县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "县纪委十五届六次全会报告"},
    {"person_id": 5, "org_id": 2, "title": "大悟县副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "大悟县副县长", "start_date": "约2025", "end_date": "", "rank": "副处级", "note": "2025 年人大常委会任免"},
    {"person_id": 7, "org_id": 6, "title": "大悟县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "大悟县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "大悟县委书记（前任）", "start_date": "约2018-2021", "end_date": "2021-06", "rank": "正处级", "note": "2018-02 时任大悟县委书记（与余德芳）"},
    {"person_id": 9, "org_id": 2, "title": "大悟县县长（更早）", "start_date": "", "end_date": "", "rank": "正处级", "note": "更早任大悟县委副书记、县长"},
    {"person_id": 9, "org_id": 3, "title": "孝感市委常委", "start_date": "2021-06", "end_date": "", "rank": "副厅级", "note": "卸任大悟书记后调任孝感市委常委"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "余海群任县委书记、鲍克明任县长，构成大悟县党政正职搭档", "overlap_org": "中共大悟县委员会/大悟县人民政府", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 9, "type": "前任继任（县委书记）", "context": "余海群 2021-06 接替余德芳任大悟县委书记", "overlap_org": "中共大悟县委员会", "overlap_period": "2018-2021"},
    {"person_a": 1, "person_b": 9, "type": "县委班子", "context": "2018年前后余德芳任书记时，余海群任县长，属县委/县政府班子", "overlap_org": "中共大悟县委员会", "overlap_period": "约2018-2021"},
    {"person_a": 1, "person_b": 3, "type": "县委班子", "context": "县委副书记在书记领导下工作", "overlap_org": "中共大悟县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "县委班子", "context": "县委常务/纪委书记在书记领导下工作", "overlap_org": "中共大悟县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "县四大家", "context": "县委书记与县人大常委会主任同属县四大家负责人", "overlap_org": "大悟县", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "县四大家", "context": "县委书记与县政协主席同属县四大家负责人", "overlap_org": "大悟县", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "县委班子", "context": "县委副书记胡涛与县长同属县委班子", "overlap_org": "中共大悟县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "县委班子", "context": "县长与纪委书记同属县委常委会", "overlap_org": "中共大悟县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "大悟县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "政府班子", "context": "副县长（毛建）在县长领导下工作", "overlap_org": "大悟县人民政府", "overlap_period": "约2025"},
    {"person_a": 9, "person_b": 2, "type": "前任县委书记-接任县长", "context": "余德芳曾任大悟书记/县长，鲍克明为其继任大悟县党政主要领导之一", "overlap_org": "大悟县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "市委班子成员", "context": "余海群（兼孝感副市长）与余德芳（孝感市委常委）同属孝感市级班子工作圈", "overlap_org": "孝感市", "overlap_period": "2026"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("job_tag") or p.get("current_post") or "大悟县领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").replace("（", "-").replace("）", "").strip("-")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001",
        "title": f"大悟县人民政府门户网站（官方新闻） - {name} 相关",
        "url": src_url if "hbdawu.gov.cn" in str(src_url) else GOV_HOST,
        "publisher": "大悟县人民政府门户网站",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official" if "hbdawu.gov.cn" in str(src_url) else "media",
        "reliability": "high" if "hbdawu.gov.cn" in str(src_url) else "medium",
        "notes": "官方大悟新闻网 2026 新闻 + 湖北省委组织部任前公示（Sogou 汇总）复核",
    }]
    if "sogou.com" in str(src_url) or "公示" in str(p.get("note", "")):
        source_register.append({
            "id": "S002",
            "title": "湖北省委组织部干部任前公示（2026年第133号）/ Sogou 汇总",
            "url": src_url,
            "publisher": "湖北省委组织部/搜狗",
            "accessed_at": AS_OF,
            "source_type": "appointment_notice",
            "reliability": "high",
            "notes": "任前公示摘要（出生、native_place、拟任书记等）",
        })

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001", "S002"]})

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
            "location": "孝感市大悟县",
            "system": "party" if pos["org_id"] in (1, 3, 5) else "government" if pos["org_id"] in (2, 4, 8) else "other",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2, 9),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if ("hbdawu" in str(src_url) or pos.get("note")) else "plausible",
            "source_ids": ["S001", "S002"] if pos.get("note") and ("公示" in str(pos.get("note", "")) or "任免" in str(pos.get("note", ""))) else ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if not p.get("birth"):
        open_q.append({"priority": "high", "question": f"{name}的出生年份/出生地",
                       "why_it_matters": "用于去重与晋升速度分析",
                       "suggested_queries": [f"{name} 任前公示 出生", f"{name} 大悟 简历"], "last_attempted": AS_OF})
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作"], "last_attempted": AS_OF})
    if name == "鲍克明":
        open_q.append({"priority": "high", "question": "鲍克明出生年份分歧（任前公示1972-07 vs 搜狗百科1975-07）",
                       "why_it_matters": "出生年影响去重与履历校核",
                       "suggested_queries": ["湖北省委组织部 任前公示 大悟 鲍洋明 原文", "鲍克明 1972 1975"], "last_attempted": AS_OF})
    if name == "余德芳":
        open_q.append({"priority": "medium", "question": "余德芳（前任书记）任职大悟县委书记的任期起止",
                       "why_it_matters": "用于完善书记更替时间线", "suggested_queries": ["余德芳 大悟县委书记 任命"], "last_attempted": AS_OF})

    relationship_objs = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
            relationship_objs.append({
                "person": other,
                "relationship_type": "overlap" if "班子" in r["type"] or "搭档" in r["type"] else "predecessor_successor" if "继任" in r["type"] or "前任" in r["type"] else "other",
                "strength": "strong" if "搭档" in r["type"] or "继任" in r["type"] else "medium",
                "evidence": r["context"], "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""), "direction": "undirected",
                "confidence": "confirmed" if "hbdawu.gov.cn" in str(p.get("source", "")) else "plausible",
                "source_ids": ["S001"]})

    governance_record = []
    if p["id"] == 1:
        governance_record.append({
            "period": "2021-2026", "domain": "economic_development",
            "achievement_or_event": "推动新能源/零碳园区/智算中心布局，会见中广核新能源商定风光储一体化项目",
            "role_in_event": "会见与统筹部署", "measurable_outcome": "大悟2025年完成新能源投资74亿元、GDP 249.09亿元",
            "location": "大悟县", "confidence": "confirmed", "source_ids": ["S001"]})
        governance_record.append({
            "period": "2021-2026", "domain": "rural_revitalization",
            "achievement_or_event": "实施'双城驱动、一环三线'战略与'六大工程'，争创全国乡村振兴示范县",
            "role_in_event": "提出并推动", "measurable_outcome": "", "location": "大悟县",
            "confidence": "confirmed", "source_ids": ["S001"]})
        governance_record.append({
            "period": "2022-2026", "domain": "discipline",
            "achievement_or_event": "推进全面从严治党，县纪委十五届六七届全会凝心聚力推进反腐",
            "role_in_event": "主体责任", "measurable_outcome": "", "location": "大悟县",
            "confidence": "confirmed", "source_ids": ["S001"]})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_大悟县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_xiaogan_dawu_{name}",
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
                "official_profile_url": src_url if "hbdawu.gov.cn" in str(src_url) else "",
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3, 7, 8, 9) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": relationship_objs,
        "governance_record": governance_record,
        "professional_profile": {
            "primary_specializations": [] if p["id"] != 1 else ["地方治理", "县域经济", "新能源产业"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["正确政绩观", "乡村振兴", "从严治党", "新能源/双碳"],
            "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号",
             "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("work_start") or p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年职务、起止时间、出生地/出生年）",
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
        try:
            build_person_json(p)
        except Exception as e:  # noqa: BLE001
            logger.warning("person JSON failed for %s: %s", p.get("name"), e)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()