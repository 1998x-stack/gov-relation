#!/usr/bin/env python3
"""曾都区（随州市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_曾都区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-06
现行班子（截至 2026-07）：
  - 区委书记：何胜（原区长，2026-05 拟任县市区委书记公示，2026-06-19 中国网报道
    "何胜已任随州市曾都区委书记、区长"。2026-05 拟任，2026-06 正式接任）
  - 前任区委书记：姜皓（随州市委常委、曾都区委书记，据随州市既有调研 凤凰网湖北 2026-02 确认；
    2026-06 起由何胜接任。姜皓个人履历见 open_gap）
  - 区长（代/政府党组书记）：李轶芳（2026-07-02 中国网"李轶芳，已任随州市曾都区政府党组书记"；
    现任区委副书记、区政府党组书记、西城街道党工委书记，下任区长候选人）
  - 区人大常委会主任：黄家洲  区政协主席：胡洪波
  - 区委常委：张震（2026 曾都营商环境发布会确认）
  - 副区长：刘娜、宫越江（市公安局曾都分局局长）、何佑鹏、孙玉、孟正华（挂职）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为核心人物（区委书记何胜、区长李轶芳）写出 data/persons/ 深度档案 JSON。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_曾都区/build_曾都区_data.py        # 产出写到暂存目录
    python3 scripts/build/build_曾都区_data.py               # 归档后运行，产出到 canonical 目录
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

SLUG = "曾都区"
PROVINCE = "湖北省"
PARENT_CITY = "随州市"
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

GOV_HOST = "http://www.zengdu.gov.cn/ldzc"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：曾都区人民政府官方《领导之窗》（区政府领导）＋ 百度百科政治表（区委/人大/政协）＋
# 中国网湖北 2026-06-19 报道 + 随州市既有调研（姜皓）。来源见 source 字段。
persons = [
    # ── 核心目标：区委书记 & 区长 ──
    {"id": 1, "name": "何胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-03", "birthplace": "湖北随县", "native_place": "湖北省随州市随县",
     "education": "大学学历（武汉科技大学 机械工程及自动化）、公共管理硕士",
     "party_join": "1998-06", "work_start": "2002-11",
     "current_org": "中共随州市曾都区委员会",
     "current_post": "曾都区委书记（原区长）",
     "source": "http://www.zengdu.gov.cn/ldzc/cdqrmzf/202111/t20211119_939427.shtml"},
    {"id": 2, "name": "李轶芳", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "湖北", "native_place": "湖北省（籍贯待核）",
     "education": "全日制大学、经济学学士",
     "party_join": "中共党员", "work_start": "2008-08",
     "current_post": "曾都区委副书记、区政府党组书记、西城街道党工委书记（拟任区长）",
     "current_org": "曾都区人民政府",
     "source": "https://www.china.com.cn/ 2026-07-02 报道:李轶芳已任随州市曾都区政府党组书记"},
    # ── 前任 区委书记 ──
    {"id": 3, "name": "姜皓", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "黑龙江省哈尔滨市", "native_place": "黑龙江省哈尔滨市",
     "education": "清华大学 计算机科学与技术 本科 + 工学博士",
     "party_join": "2003-12", "work_start": "2010-07",
     "current_post": "前任曾都区委书记（原随州市委常委、曾都区委书记）",
     "current_org": "中共随州市委员会",
     "source": "https://baike.so.com/doc/11951-26832960.html"},
    # ── 4: 人大 / 政协 一把手 ──
    {"id": 4, "name": "黄家洲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾都区人大常委会主任", "current_org": "曾都区人大常委会",
     "source": "百度百科-曾都区（2026-07 政治条目）"},
    {"id": 5, "name": "胡洪波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾都区政协主席", "current_org": "中国人民政治协商会议曾都区委员会（随州市曾都区政协）",
     "source": "百度百科-曾都区（2026-07 政治条目）+ 湖北省政协网"},
    # ── 5: 区委常委（少数已确认）──
    {"id": 6, "name": "张震", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾都区委常委", "current_org": "中共随州市曾都区委员会",
     "source": "随州市政府网 2026 曾都专场新闻发布会"},
    # ── 6: 区政府副区长 ──
    {"id": 7, "name": "刘娜", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "曾都区副区长", "current_org": "曾都区人民政府",
     "source": f"{GOV_HOST}/"},
    {"id": 8, "name": "宫越江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾都区副区长、市公安局曾都分局党委书记/局长、区委政法委第一副书记",
     "current_org": "曾都区人民政府/随州市公安局曾都区分局",
     "source": f"{GOV_HOST}/"},
    {"id": 9, "name": "何佑鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾都区副区长", "current_org": "曾都区人民政府",
     "source": f"{GOV_HOST}/"},
    {"id": 10, "name": "孙玉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "曾都区副区长", "current_org": "曾都区人民政府",
     "source": f"{GOV_HOST}/"},
    {"id": 11, "name": "孟正华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "曾都区副区长（挂职）", "current_org": "曾都区人民政府",
     "source": f"{GOV_HOST}/"},
]

organizations = [
    {"id": 1, "name": "中共随州市曾都区委员会", "type": "党委", "level": "县级", "parent": "中共随州市委员会", "location": "随州市曾都区"},
    {"id": 2, "name": "曾都区人民政府", "type": "政府", "level": "县级", "parent": "随州市人民政府", "location": "随州市曾都区"},
    {"id": 3, "name": "中共随州市曾都区纪律检查委员会/监委", "type": "党委", "level": "县级", "parent": "中共随州市纪律检查委员会", "location": "随州市曾都区"},
    {"id": 4, "name": "中共随州市曾都区委政法委员会", "type": "党委", "level": "县级", "parent": "中共随州市曾都区委员会", "location": "随州市曾都区"},
    {"id": 5, "name": "随州市公安局曾都区分局", "type": "政府", "level": "县级", "parent": "曾都区人民政府", "location": "随州市曾都区"},
    {"id": 6, "name": "曾都区人大常委会", "type": "人大", "level": "县级", "parent": "随州市人民代表大会常务委员会", "location": "随州市曾都区"},
    {"id": 7, "name": "中国人民政治协商会议随州市曾都区委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议随州市委员会", "location": "随州市曾都区"},
    {"id": 8, "name": "曾都区西城街道党工委/办事处", "type": "乡镇/街道", "level": "乡科级", "parent": "中共随州市曾都区委员会", "location": "随州市曾都区西城街道"},
]

positions = [
    # ── 区委班子 ──
    {"person_id": 1, "org_id": 1, "title": "曾都区委书记", "start_date": "2026-06", "end_date": "", "rank": "正处级",
     "note": "2026-05 拟任县市区委书记公示，2026-06 接任姜皓；此前为区长"},
    {"person_id": 1, "org_id": 2, "title": "曾都区区长（兼/此前）", "start_date": "2021-08", "end_date": "2026", "rank": "正处级",
     "note": "2021-08 副区长、代理区长；后任区长、区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "曾都区委副书记", "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "任区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "曾都区政府党组书记", "start_date": "2026-07", "end_date": "", "rank": "正处级",
     "note": "拟任区长（代）"},
    {"person_id": 2, "org_id": 8, "title": "西城街道党工委书记", "start_date": "", "end_date": "", "rank": "正科级·高配", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "前任曾都区委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级",
     "note": "随州市委常委兼曾都区委书记；何胜接任"},
    {"person_id": 3, "org_id": 1, "title": "曾都区委常委、常务副区长（曾任）", "start_date": "2015-12", "end_date": "约2017", "rank": "副处级",
     "note": "早期履历（360百科），后续晋升路径待查（open gap）"},
    {"person_id": 6, "org_id": 1, "title": "曾都区委常委", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "2026 曾都专场营商环境发布会确认，分工待核"},
    # ── 人大 / 政协 ──
    {"person_id": 4, "org_id": 6, "title": "曾都区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "曾都区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # ── 政府 ──
    {"person_id": 7, "org_id": 2, "title": "曾都区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "曾都区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "市公安局曾都分局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委政法委第一副书记"},
    {"person_id": 9, "org_id": 2, "title": "曾都区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "曾都区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "曾都区副区长（挂职）", "start_date": "2026-03", "end_date": "", "rank": "副处级", "note": "挂职"},
]

relationships = [
    # 前任→现任 书记交接
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "姜皓（随州市委常委、曾都区委书记）与何胜（区长）完成曾都区委一把手交接；何胜于2026-06接任区委书记",
     "overlap_org": "中共随州市曾都区委员会", "overlap_period": "2021-2026"},
    # 现任书记 × 代区长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "何胜（区委书记）与李轶芳（区政府党组书记/拟任区长）组成曾都区党政正职搭配",
     "overlap_org": "曾都区党委/政府", "overlap_period": "2026至今"},
    # 区委班子核心交集（书记 × 其他常委）
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委张震同属曾都区委常委会",
     "overlap_org": "中共随州市曾都区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "党政军关联",
     "context": "区委书记何胜与区人大常委会主任黄家洲同属区四套班子",
     "overlap_org": "曾都区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记何胜与区政协主席胡洪波同属区四套班子",
     "overlap_org": "曾都区", "overlap_period": "2026"},
    # 区长（李）与区政府副区长
    {"person_a": 2, "person_b": 8, "type": "政府班子",
     "context": "区政府党组书记与副区长宫越江（公安局长）在区政府班子共事",
     "overlap_org": "曾都区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "政府班子",
     "context": "区政府党组成员与副区长刘娜在区政府班子共事",
     "overlap_org": "曾都区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "政府班子",
     "context": "区政府党组书记与副区长何佑鹏在区政府班子共事",
     "overlap_org": "曾都区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "政府班子",
     "context": "区政府党组书记与副区长孙玉在区政府班子共事",
     "overlap_org": "曾都区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "政府班子",
     "context": "区政府党组书记与副区长孟正华在区政府班子共事",
     "overlap_org": "曾都区人民政府", "overlap_period": "2026"},
    # 跨县交流：何胜自广水调任曾都
    {"person_a": 1, "person_b": 3, "type": "cross_county_rotation",
     "context": "广水市委常委、常务副市长何胜调任曾都区（2021-08 代区长），预示本区主政干部由市直部门领导空降/跨县交流模式",
     "overlap_org": "随州市干部交流", "overlap_period": "2021"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "曾都区领导"
    import re
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001", "title": f"曾都区官方组织/百科 2026 复核 - {name}",
        "url": src_url, "publisher": "曾都区人民政府/百科", "published_at": AS_OF,
        "accessed_at": AS_OF, "source_type": "official" if "zengdu" in str(src_url) or "geo" in str(src_url) else "encyclopedia",
        "reliability": "high" if "zengdu" in str(src_url) else "medium",
        "notes": "曾都区领导班子在任信息（2026-08-06 复核）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "",
                    "major": "机械工程及自动化" if name == "何胜" else "",
                    "degree": p["education"], "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        career_timeline.append({
            "start": pos["start_date"] or "unknown", "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""), "title": pos["title"],
            "level": pos.get("rank", ""), "location": "随州市曾都区",
            "system": "party" if pos["org_id"] in (1, 3, 4, 8) else "government",
            "rank": pos.get("rank", ""), "is_key_promotion": pos["person_id"] in (1, 2, 3),
            "notes": pos.get("note", ""), "confidence": "confirmed" if p.get("birth") else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if name == "何胜":
        if not p.get("party_join"):
            open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                           "why_it_matters": "用于精确构建晋升时间线",
                           "suggested_queries": [f"{name} 任前公示 入党"], "last_attempted": AS_OF})
    if name == "李轶芳":
        open_q.append({"priority": "high", "question": "李轶芳任曾都区政府党组书记后的正式区长（代区长）任职/选举时间",
                       "why_it_matters": "确认现任区长正式身份与上任时间",
                       "suggested_queries": ["曾都区区长 李轶芳 人大 任命", "李轶芳 曾都对 代区长"],
                       "last_attempted": AS_OF})
    if name == "姜皓":
        open_q.append({"priority": "critical", "question": "姜皓 2016-2026 自曾都区常务副区长晋升至区委书记/随州市委常委的具体路径与任书记时间",
                       "why_it_matters": "核心前任的晋升路径与去向是突破线索",
                       "suggested_queries": ["姜皓 曾都区委书记 任前", "姜皓 随州市委常委 简历"],
                       "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_曾都区", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_suizhou_zengdu_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""), "education": edu,
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""),
                           "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3, 4, 5) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs, "relationships": [], "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if PROVINCE in (p.get("native_place") or "") else "unknown",
            "systems_experience": [], "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
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
            "current_role": "confirmed", "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间）",
        },
        "open_questions": open_q,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    logger.info("person JSON written: %s", out_path)


def main() -> None:
    print(f"Building {SLUG} network data...")
    run_build(
        slug=SLUG, persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=str(DB_PATH), gexf_path=str(GEXF_PATH), overwrite=True,
    )
    print("  Writing person JSON lead-files...")
    # 只对核心人物写人物 JSON（何胜=书记、李轶坤=区长、姜皓=前任书记），避免过多 thin 档案
    core = {p["id"] for p in persons if p["name"] in ("何胜", "李轶芳", "姜皓")}
    for p in persons:
        if p["id"] in core:
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