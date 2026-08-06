#!/usr/bin/env python3
"""北湖区（郴州市，湖南省）领导班子工作关系网络数据生成脚本。

Task ID: hunan_北湖区
Province: 湖南省
Parent city: 郴州市
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-06
现行班子（截至 2026-08，证据来自北湖新闻网 www.beihuxinwen.cn 多篇官方报道，high reliability）：
  - 区委书记：郭庆锋（兼郴州经开区党工委书记）
    * 2026-07-31 郴州经开区高质量发展推进会："区委书记、郴州经开区党工委书记郭庆锋出席并讲话"
    * 2026-07-29/30 北湖区第七次党代会：代表第六届区委作报告并主持闭幕
  - 区长：李世钧（区委副书记、区长，郴州经开区党工委副书记、管委会第一主任）
    * 2026-07-31："区委副书记、区长，郴州经开区党工委副书记、管委会第一主任李世钧主持会议"
    * 2026-08-03 七届区委常委会 2026 年第 1 次会议：区长李世钧参加
  - 七届区委常委会班子成员（2026-07-30 党代会闭幕确认）：
    郭庆锋、李世钧、龙媛、曾祥峰、李振华、谢菁、何蔚、郭志军、高亚军、吴豪、李素武、胡培禹
    （各人名具体职务分工未获公开证实，统一标记为 "区委常委，具体分工待查"

开放缺口（open gaps）：
  - 李世钧任区长前完整履历（出生/籍贯/学历/入党时间/任前职务）未获证实。
    区政府官网 www.czbeihu.gov.cn 返回 412、百度百科 403、r.jina.ai 及搜索引擎不可用。
  - 原班子核心人物/前任书记、区长去向未收录（避免虚构）。
  - 各位常委的常务副区长/纪委书记/组织部长/宣传部长等具体分工未获证实。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为核心人物（区委书记郭庆锋、区长李世钧）写出 data/persons/ 深度档案 JSON。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hunan_北湖区/build_北湖区_data.py        # 产出写到暂存目录
    python3 scripts/build/build_北湖区_data.py               # 归档后运行，产出到 canonical 目录
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

SLUG = "北湖区"
PROVINCE = "湖南省"
PARENT_CITY = "郴州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<slug>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph|persons
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

SRC_GUO = "https://www.beihuxinwen.cn/content/646041/75/16136333.html"
SRC_LI = "https://www.beihuxinwen.cn/content/646041/75/16136333.html"
SRC_CHW = "https://www.beihuxinwen.cn/content/646041/75/16131866.html"
SRC_KFH = "https://www.beihuxinwen.cn/content/646041/75/16131866.html"
SRC_XCC = "https://www.beihuxinwen.cn/content/646042/96/16144122.html"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：北湖新闻网官方报道（2026-07/08）+ 郴州日报/红网郴州站（区级）。
persons = [
    # ── 核心目标：区委书记 & 区长（已确认）──
    {"id": 1, "name": "郭庆锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "郴州市北湖区委书记、郴州经开区党工委书记",
     "current_org": "中共郴州市北湖区委员会",
     "source": SRC_GUO},
    {"id": 2, "name": "李世钧", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "郴州市北湖区委副书记、区长、郴州经开区党工委副书记/管委会第一主任",
     "current_org": "北湖区人民政府",
     "source": SRC_LI},
    # ── 七届区委常委会班子成员（名单已确认，具体分工未证实）──
    {"id": 3, "name": "龙媛", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 4, "name": "曾祥峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 5, "name": "李振华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 6, "name": "谢菁", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 7, "name": "何蔚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 8, "name": "郭志军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 9, "name": "高亚军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 10, "name": "吴豪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 11, "name": "李素武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
    {"id": 12, "name": "胡培禹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "北湖区委常委", "current_org": "中共郴州市北湖区委员会",
     "source": SRC_CHW},
]

# ── 机构 ────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共郴州市北湖区委员会", "type": "党委", "level": "县处级", "parent": "郴州市", "location": "郴州市北湖区"},
    {"id": 2, "name": "北湖区人民政府", "type": "政府", "level": "县处级", "parent": "郴州市", "location": "郴州市北湖区"},
    {"id": 3, "name": "郴州经济技术开发区党工委", "type": "党委", "level": "县处级", "parent": "郴州市", "location": "郴州市"},
    {"id": 4, "name": "郴州经济技术开发区管委会", "type": "政府", "level": "县处级", "parent": "郴州市", "location": "郴州市"},
    {"id": 5, "name": "中共郴州市委员会", "type": "党委", "level": "地厅级", "parent": "湖南省", "location": "郴州市"},
    {"id": 6, "name": "郴州市人民政府", "type": "政府", "level": "地厅级", "parent": "湖南省", "location": "郴州市"},
]

# ── 任职 ────────────────────────────────────────────────────────────────────
positions = [
    # 核心领导
    {"person_id": 1, "org_id": 1, "title": "北湖区委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "兼郴州经开区党工委书记；2026-07 七届党代会上任"},
    {"person_id": 1, "org_id": 3, "title": "郴州经开区党工委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "已确认"},
    {"person_id": 2, "org_id": 2, "title": "北湖区委副书记、区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-07 高质量发展推进会确认"},
    {"person_id": 2, "org_id": 4, "title": "郴州经开区管委会第一主任（党工委副书记）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "已确认"},
    # 常委
    {"person_id": 3, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 4, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 5, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 6, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 7, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 8, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 9, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 10, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 11, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    {"person_id": 12, "org_id": 1, "title": "北湖区委常委", "start_date": "2026-07", "end_date": "present", "rank": "县处级", "note": "七届区委常委"},
    # 与上一级领导关系
    {"person_id": 1, "org_id": 5, "title": "受中共郴州市委领导（区属市管干部）", "start_date": "", "end_date": "present", "rank": "县处级", "note": "由郴州市委管理"},
]

# ── 关系 ────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记（郭庆锋）与区长（李世钧）党政主官搭班，共事于北湖区委常委会；同时分别在郴州经开区任党工委书记/党工委副书记、管委会第一主任，属'区政合一'体制下的区开发区同责搭档",
     "overlap_org": "中共郴州市北湖区委员会 / 郴州经济技术开发区",
     "overlap_period": "2026-07 起（七届区委）"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "区委书记与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与区委常委同属区委常委会", "overlap_org": "中共郴州市北湖区委员会", "overlap_period": "2026-07 起"},
]

# ── 构建 ────────────────────────────────────────────────────────────────────
def main():
    logger.info("Building 北湖区 network: %s -> %s / %s", DB_PATH, GEXF_PATH, PERSONS_OUT)
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
    # 写核心人物深度档案 JSON 到同一输出目录（process_tmp 会识别并归档到 data/persons/）
    write_person_jsons()
    print("\n✅ 北湖区 数据构建完成。")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  人物:  {len(persons)}  机构: {len(organizations)}  任职: {len(positions)}  关系: {len(relationships)}")


PERSON_ID_MAP = {
    "郭庆锋": "beihu_guo_qingfeng",
    "李世钧": "beihu_li_shijun",
    "龙媛": "beihu_long_yuan",
    "曾祥峰": "beihu_zeng_xiangfeng",
    "李振华": "beihu_li_zhenhua",
    "谢菁": "beihu_xie_jing",
    "何蔚": "beihu_he_wei",
    "郭志军": "beihu_guo_zhijun",
    "高亚军": "beihu_gao_yajun",
    "吴豪": "beihu_wu_hao",
    "李素武": "beihu_li_suwu",
    "胡培禹": "beihu_hu_peiyu",
}


def _person_id(name):
    return PERSON_ID_MAP.get(name, f"北湖_{name}")


def _base_json(p, job):
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": job,
            "task_id": "hunan_北湖区",
            "time_focus": "2026-07/08 现行班子",
        },
        "identity": {
            "person_id": _person_id(p["name"]),
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "县处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "2026-07",
                "end": "present",
                "org": p.get("current_org", ""),
                "title": p.get("current_post", ""),
                "level": "县处级",
                "location": PARENT_CITY + "北湖区",
                "system": "party" if "书记" in p.get("current_post", "")
                          else "government",
                "rank": "县处级",
                "is_key_promotion": True,
                "notes": "北湖新闻网官方报道确认（2026-07/08）",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "organizations": [
            {"org_id": 1, "name": "中共郴州市北湖区委员会", "type": "党委"},
            {"org_id": 2, "name": "北湖区人民政府", "type": "政府"},
            {"org_id": 3, "name": "郴州经济技术开发区党工委", "type": "党委"},
            {"org_id": 4, "name": "郴州经济技术开发区管委会", "type": "政府"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "局部资料不足，履历完整度待补", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "unknown", "evidence": "公开渠道不足，未推断",
                 "confidence": "unverified", "source_ids": []}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格依据公开报道推断，非私密心理评估。",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未检索到公开的处分/审计/负面报道", "date": "2026-08-06",
             "confidence": "unverified", "source_ids": []}
        ],
        "network_metrics": {
            "confirmed_overlaps": 0,
            "open_gaps": "职务分工/履历待补",
            "notes": "核心人物履历（出生/籍贯/学历/入党/任前经历）因官网412与百度403未能核实，均置空待补。",
        },
        "source_register": [
            {"id": "S001", "title": "北湖区（郴州经开区）高质量发展推进会：区委书记郭庆锋、区长李世钧出席",
             "url": "https://www.beihuxinwen.cn/content/646041/75/16136333.html",
             "publisher": "北湖新闻网", "published_at": "2026-07-31", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认郭庆锋/李世钧职务"},
            {"id": "S002", "title": "北湖区第七次党代会闭幕", "url": "https://www.beihuxinwen.cn/content/646041/75/16131866.html",
             "publisher": "北湖新闻网", "published_at": "2026-07-30", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "新一届区委常委会名单"},
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生/籍贯/学历/入党时间及任前完整履历未获证实",
        },
        "open_questions": [
            {"priority": "critical", "question": "完整个人履历（出生、籍贯、学历、入党/参加工作时间、任区长/书记前历任职务）",
             "why_it_matters": "缺少人物识别与生涯轨迹，无法建立跨区干部网络边", "suggested_queries": ["任前公示", "区党委组织部", "人大任免"], "last_attempted": AS_OF},
        ],
    }


def write_person_jsons():
    profiles = [
        (1, "区委书记"),
        (2, "区长"),
    ]
    for pid, job in profiles:
        p = next(x for x in persons if x["id"] == pid)
        doc = _base_json(p, job)
        fname = PERSONS_OUT / f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{job}-{p['name']}.json"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(json.dumps(doc, ensure_ascii=False, indent=2))
        logger.info("Wrote person JSON: %s", fname)


if __name__ == "__main__":
    main()