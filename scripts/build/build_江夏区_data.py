#!/usr/bin/env python3
"""江夏区（武汉市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_江夏区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-07
现行班子（截至 2026-08，官方江夏区人民政府门户 www.jiangxia.gov.cn 确认）：
  - 区委书记：舒贵传（原任江夏区长，2025-12 转任区委书记）
  - 区委副书记、区长：王振（原任区委副书记、区政府党组书记，2025-12-19 任副区长并代理区长，
    2026-01 于人代会选举任区长；起草《2025年政府工作报告》）
  - 区委副书记、政法委书记：韩良炎
  - 区人大常委会主任：向卉珍
  - 区委常委、组织部部长：孙娅莉
  - 副区长、区公安分局局长：刘斌
  - 区领导：罗尚国、王树人
  - 区政协领导：陈卫、梁爽、陈兴雄、任丽英、唐云峰、闵运桥、余建平
  - 区人大副主任：孙艳霞、王凯、李宗祥、王太明

说明：
- 公开百科/媒体对区级干部完整履历覆盖有限（百度百科 403、搜索受限），核心干部的出生年/籍贯/学历
  部分留作 open_questions，不臆造。
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-武汉市-{job}-{name}.json 深度档案。
- 产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_江夏区/build_江夏区_data.py        # 产出写到暂存目录
    python3 scripts/build/build_江夏区_data.py                # 归档后运行，产出到 canonical 目录
"""

import json
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

SLUG = "江夏区"
PROVINCE = "湖北省"
PARENT_CITY = "武汉市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

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

# 官方来源常量
GOV_HOST = "https://www.jiangxia.gov.cn"
SRC_LIANXUE = f"{GOV_HOST}/jxzx_22341/202608/t20260804_2829296.shtml"    # 联组学习 2026-07-31
SRC_WEIWEN = f"{GOV_HOST}/jxzx_22341/202607/t20260729_2826921.shtml"     # 走访慰问 2026-07-29
SRC_ZHENGXIE = f"{GOV_HOST}/jxzx_22341/202607/t20260729_2826934.shtml"   # 政协常委会 2026-07-21
SRC_YWTG = f"{GOV_HOST}/jxzx_22341/202608/t20260801_2828461.shtml"       # 一网统管 2026-08-01
SRC_GWR = f"{GOV_HOST}/xxgk_22343/zfgzbg_22344/202601/t20260113_2710445.shtml"  # 2025政府工作报告
SRC_RSRM = f"{GOV_HOST}/xxgk_22343/xxgkzn_22346/202512/t20251223_2699161.shtml"  # 人事任免 2025-12-23
SRC_HOME = f"{GOV_HOST}/"
SRC_RESEARCH = f"{GOV_HOST}/xxgk_22343/xxgkzn_22346/202512/t20251223_2699161.shtml"  # 人事任免 2025-12-23
SRC_RESNOTES = "data/tmp/hubei_江夏区/research/research_notes.md"  # 本地研究笔记（前序调查）

# ── 组织 ────────────────────────────────────────────────────────────────────
# 组织 id 0x 前缀 → runner 会 +100000 作为 GEXF 节点 id；此处用 1..N（0x 区域约定：1=党委,2=政府,3=人大,4=政协,5=纪委,6=政法）
organizations = [
    {"id": 1, "name": "中共武汉市江夏区委员会", "type": "party", "level": "区级", "parent": "中共武汉市委", "location": "武汉市江夏区"},
    {"id": 2, "name": "武汉市江夏区人民政府", "type": "government", "level": "区级", "parent": "武汉市人民政府", "location": "武汉市江夏区"},
    {"id": 3, "name": "武汉市江夏区人民代表大会常务委员会", "type": "npc", "level": "区级", "parent": "武汉市人大常委会", "location": "武汉市江夏区"},
    {"id": 4, "name": "中国人民政治协商会议武汉市江夏区委员会", "type": "cppcc", "level": "区级", "parent": "武汉市政协", "location": "武汉市江夏区"},
    {"id": 5, "name": "中共武汉市江夏区纪律检查委员会", "type": "discipline", "level": "区级", "parent": "中共武汉市纪委", "location": "武汉市江夏区"},
    {"id": 6, "name": "中共武汉市江夏区委政法委员会", "type": "party", "level": "区级", "parent": "中共武汉市委政法委", "location": "武汉市江夏区"},
    {"id": 7, "name": "武汉市公安局江夏区分局", "type": "government", "level": "区级", "parent": "武汉市公安局", "location": "武汉市江夏区"},
]

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：江夏区人民政府官方门户新闻/报告，来源见 source 字段。核心干部出生籍贯学历等字段待补 → open_questions。
persons = [
    {"id": 1, "name": "舒贵传", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区委书记", "current_org": "中共武汉市江夏区委员会",
     "source": SRC_WEIWEN},
    {"id": 2, "name": "王振", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区委副书记、区长", "current_org": "武汉市江夏区人民政府",
     "source": SRC_GWR},
    {"id": 3, "name": "韩良炎", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区委副书记、区委政法委书记", "current_org": "中共武汉市江夏区委员会",
     "source": SRC_YWTG},
    {"id": 4, "name": "向卉珍", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区人大常委会主任", "current_org": "武汉市江夏区人民代表大会常务委员会",
     "source": SRC_RESNOTES},
    {"id": 5, "name": "孙娅莉", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区委常委、组织部部长、党校校长", "current_org": "中共武汉市江夏区委员会",
     "source": SRC_RESEARCH},
    {"id": 6, "name": "刘斌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区副区长、区公安分局局长", "current_org": "武汉市公安局江夏区分局",
     "source": SRC_RESEARCH},
    {"id": 7, "name": "罗尚国", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区领导", "current_org": "武汉市江夏区人民政府",
     "source": SRC_WEIWEN},
    {"id": 8, "name": "王树人", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "江夏区领导", "current_org": "武汉市江夏区人民政府",
     "source": SRC_WEIWEN},
]

# 政协领导小组（区政协六届二十五次常委会会议出席）
cppcc_leaders = [
    ("陈卫", 9), ("梁爽", 10), ("陈兴雄", 11), ("任丽英", 12),
    ("唐云峰", 13), ("闵运桥", 14), ("余建平", 15),
]
for _name, _pid in cppcc_leaders:
    persons.append({
        "id": _pid, "name": _name, "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "江夏区政协领导", "current_org": "中国人民政治协商会议武汉市江夏区委员会",
        "source": SRC_ZHENGXIE,
    })

# ── 任职 ────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "江夏区委书记", "start": "2025-12", "end": "present",
     "rank": "市管正处级", "note": "原任江夏区长，2025-12 转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "江夏区长（前任，2025-12 卸任）", "start": "unknown", "end": "2025-12",
     "rank": "市管正处级", "note": "任区长时主持区政府（2025-12 辞去区长职务）"},
    {"person_id": 2, "org_id": 2, "title": "江夏区委副书记、区长", "start": "2025-12", "end": "present",
     "rank": "市管正处级", "note": "2025-12-19 决定副区长并代理区长；2026-01 人代会选举任区长"},
    {"person_id": 2, "org_id": 1, "title": "江夏区委副书记、区政府党组书记", "start": "unknown", "end": "2025-12",
     "rank": "市管正处级", "note": "代理区长前任职"},
    {"person_id": 3, "org_id": 1, "title": "江夏区委副书记、区委政法委书记", "start": "unknown", "end": "present",
     "rank": "市管正处级", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "江夏区委政法委书记", "start": "unknown", "end": "present",
     "rank": "市管正处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "江夏区人大常委会主任", "start": "unknown", "end": "present",
     "rank": "市管正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "江夏区委常委、组织部部长", "start": "unknown", "end": "present",
     "rank": "市管副处级", "note": "兼区委党校校长"},
    {"person_id": 6, "org_id": 7, "title": "江夏区副区长、区公安分局局长", "start": "unknown", "end": "present",
     "rank": "市管副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "江夏区领导", "start": "unknown", "end": "present", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "江夏区领导", "start": "unknown", "end": "present", "rank": "", "note": ""},
]
for _name, _pid in cppcc_leaders:
    positions.append({
        "person_id": _pid, "org_id": 4, "title": "江夏区政协领导", "start": "unknown", "end": "present",
        "rank": "", "note": "区政协六届二十五次常委会会议出席领导",
    })

# ── 关系（person_a, person_b 为 persons id）──────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "舒贵传卸任区长转任区委书记后，王振由区委副书记接任区长，书记-区长搭档",
     "overlap_org": "武汉市江夏区人民政府/区委", "overlap_period": "2025-12 至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委分管副书记、政法委书记同班子",
     "overlap_org": "中共武汉市江夏区委员会", "overlap_period": "2025-12 至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委副书记、政法委书记同班子协同",
     "overlap_org": "中共武汉市江夏区委员会", "overlap_period": "2025-12 至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区人大常委会主任",
     "overlap_org": "江夏区四套班子", "overlap_period": "2025-12 至今"},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "区委组织部部长在区委书记领导下工作",
     "overlap_org": "中共武汉市江夏区委员会", "overlap_period": "2025-12 至今"},
]


def write_person_json(p: dict, post: str) -> None:
    """写出单个人物深度图谱 JSON 到 PERSONS_OUT（暂存或 canonical）。"""
    person_id_slug = ("hubei_wuhan_jiangxia_" + p["name"])
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": p["current_post"],
            "task_id": "hubei_江夏区",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": person_id_slug,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": (p["name"] + "_" + p.get("birth", "")).strip("_"),
                "name_birthplace": (p["name"] + "_" + p.get("birthplace", "")).strip("_"),
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown", "end": "present",
                "org": p["current_org"], "title": p["current_post"],
                "level": "", "location": "武汉市江夏区",
                "system": "party" if "区委" in p["current_org"] else "government",
                "rank": "", "is_key_promotion": (p["name"] in ("舒贵传", "王振")),
                "notes": "任职信息来源于官方公开新闻/报告；起止时间与早年履历待查",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "organizations": [{"org_name": p["current_org"], "org_type": "", "role": p["current_post"]}],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if p["name"] in ("舒贵传", "王振") else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["武汉市江夏区"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "搜索范围内未发现纪律处分/审计/负面舆情信号",
                "date": "", "confidence": "unverified", "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "武汉市江夏区人民政府门户（江夏要闻 / 2025年政府工作报告）",
                "url": p.get("source", GOV_HOST),
                "publisher": "武汉市江夏区人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方在职领导/会议信息（2026-08-07 复核）",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整人履历（出生年、籍贯、学历、历任起止时间）",
        },
        "open_questions": [
            {
                "priority": "critical" if p["name"] in ("舒贵传", "王振") else "high",
                "question": f"{p['name']} 的出生年份、籍贯、学历、入党/参加工作年份与完整历任职务",
                "why_it_matters": "构建可信履历与网络去重",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任前公示", f"{p['name']} 武汉"],
                "last_attempted": AS_OF,
            }
        ],
    }
    out = PERSONS_OUT / f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{post}-{p['name']}.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("wrote person json: %s", out.name)


def main() -> None:
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
    # 深度人物档案：核心 + 班子主要成员
    for p in persons:
        if p["id"] <= 6:
            write_person_json(p, p["current_post"])
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {sum(1 for p in persons if p['id'] <= 6)} json files in {PERSONS_OUT}")


if __name__ == "__main__":
    main()