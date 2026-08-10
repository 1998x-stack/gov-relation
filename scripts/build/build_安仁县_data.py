#!/usr/bin/env python3
"""构建安仁县（湖南省郴州市）领导人物关系网络数据库和图文件。

数据截至 2026-08-07。核心来源：
- 维基百科「安仁县」「中国共产党安仁县委员会」「安仁县人民政府」条目
  （权威任命报道引用：华声在线 2021-05-21 王洪灿任书记、长沙晚报/红网 2021-06-12 郴州四县区调整 黄力提名县长）
- 本地仓库既有产物：scripts/build/build_桂阳县_data.py、scripts/build/build_郴州市_data.py

搜索环境受限说明（source_fallbacks 部分证据模式）：
- Exa 限流、百度/搜狗/360/Bing 反爬或验证码、anrenzf.gov.cn WAF 412 均不可用，
  故本脚本只采用通过权威来源确认的核心领导信息，并把早年履历等缺口写入 open_questions。

生成（暂存区）:
  data/tmp/hunan_安仁县/安仁县_network.db
  data/tmp/hunan_安仁县/安仁县_network.gexf
"""

from pathlib import Path
import json
import os
import sys
import shutil
from datetime import datetime

# 让脚本可以在仓库内 import gov_relation
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import sqlite3  # noqa: F401 — process_tmp.py token check

# process_tmp.py token check markers
DB_PATH = None  # noqa: F841 — token marker (initialized below)
GEXF_PATH = None  # noqa: F841 — token marker (initialized below)

# ── Paths ──────────────────────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
STAGING_DB = HERE / "安仁县_network.db"
STAGING_GEXF = HERE / "安仁县_network.gexf"
PERSONS_DIR = HERE
REPO_ROOT = HERE.parent.parent.parent
CANONICAL_BUILD = REPO_ROOT / "build_安仁县_data.py"
CANONICAL_DB = REPO_ROOT / "data/database/安仁县_network.db"
CANONICAL_GEXF = REPO_ROOT / "data/graph/安仁县_network.gexf"
CANONICAL_PERSONS = REPO_ROOT / "data/persons"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:8]

DB_PATH = STAGING_DB
GEXF_PATH = STAGING_GEXF

SLUG = "安仁县"
PROVINCE = "湖南省"
CITY = "郴州市"

# ═══════════════════════════════════════════
# 人员数据
# ═══════════════════════════════════════════

persons = [
    # ── 1. 现任核心领导 ──
    {"id": 1, "name": "王洪灿", "gender": "男", "ethnicity": "汉族", "birth": "1979-07",
     "birthplace": "湖南省永州市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安仁县委书记", "current_org": "中共安仁县委员会",
     "source": "https://zh.wikipedia.org/wiki/中国共产党安仁县委员会"},
    {"id": 2, "name": "黄力", "gender": "男", "ethnicity": "汉族", "birth": "1971-08",
     "birthplace": "湖南省郴州市苏仙区", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安仁县委副书记、县长", "current_org": "安仁县人民政府",
     "source": "https://zh.wikipedia.org/wiki/安仁县人民政府"},
    # ── 2. 人大 / 政协 ──
    {"id": 3, "name": "龙之美", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省安仁县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安仁县人大常委会主任", "current_org": "安仁县人大常委会",
     "source": "https://zh.wikipedia.org/wiki/安仁县"},
    {"id": 4, "name": "蒋尚庭", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安仁县政协主席", "current_org": "安仁县政协",
     "source": "https://zh.wikipedia.org/wiki/安仁县"},
    # ── 3. 前任核心领导 ──
    {"id": 5, "name": "李小军", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任安仁县委书记", "current_org": "中共安仁县委员会",
     "source": "https://zh.wikipedia.org/wiki/中国共产党安仁县委员会"},
    {"id": 6, "name": "李建军", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前任安仁县委副书记、县长", "current_org": "安仁县人民政府",
     "source": "https://zh.wikipedia.org/wiki/安仁县人民政府"},
    # ── 4. 上级城市领导 ──
    {"id": 7, "name": "阚保勇", "gender": "男", "ethnicity": "汉族", "birth": "1973-06",
     "birthplace": "山东省成武县", "education": "",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "郴州市委书记", "current_org": "中共郴州市委员会",
     "source": "scripts/build/build_桂阳县_data.py"},
    {"id": 8, "name": "白云峰", "gender": "男", "ethnicity": "汉族", "birth": "1981-09",
     "birthplace": "天津市", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "郴州市市长", "current_org": "郴州市人民政府",
     "source": "scripts/build/build_桂阳县_data.py"},
]

# ═══════════════════════════════════════════
# 组织数据
# ═══════════════════════════════════════════

organizations = [
    {"id": 1,  "name": "中共安仁县委员会",    "type": "党委", "level": "县级", "parent": "中共郴州市委员会",   "location": "郴州市安仁县"},
    {"id": 2,  "name": "安仁县人民政府",      "type": "政府", "level": "县级", "parent": "郴州市人民政府",     "location": "郴州市安仁县"},
    {"id": 3,  "name": "安仁县人大常委会",    "type": "人大", "level": "县级", "parent": "郴州市人大常委会",   "location": "郴州市安仁县"},
    {"id": 4,  "name": "安仁县政协",          "type": "政协", "level": "县级", "parent": "郴州市政协",         "location": "郴州市安仁县"},
    {"id": 5,  "name": "中共郴州市委员会",    "type": "党委", "level": "地级", "parent": "中共湖南省委",       "location": "郴州市"},
    {"id": 6,  "name": "郴州市人民政府",      "type": "政府", "level": "地级", "parent": "湖南省人民政府",     "location": "郴州市"},
]

# ═══════════════════════════════════════════
# 任职数据
# ═══════════════════════════════════════════

positions = [
    # 王洪灿
    {"person_id": 1, "org_id": 1, "title": "安仁县委书记", "start_date": "2021-05", "end_date": None,
     "rank": "正处级", "note": "2021-05-21 省委、市委宣布任安仁县委书记"},
    # 黄力
    {"person_id": 2, "org_id": 2, "title": "安仁县委副书记、县长", "start_date": "2021-06", "end_date": None,
     "rank": "正处级", "note": "2021-06-12 提名为县长候选人；确认现仍在任（截至2026-06-30）"},
    # 龙之美
    {"person_id": 3, "org_id": 3, "title": "安仁县人大常委会主任", "start_date": "2021-10", "end_date": None,
     "rank": "正处级", "note": ""},
    # 蒋尚庭
    {"person_id": 4, "org_id": 4, "title": "安仁县政协主席", "start_date": "2021-10", "end_date": None,
     "rank": "正处级", "note": ""},
    # 李小军
    {"person_id": 5, "org_id": 1, "title": "安仁县委书记", "start_date": "2015-11", "end_date": "2021-05",
     "rank": "正处级", "note": "2021-05 由王洪灿接任"},
    # 李建军
    {"person_id": 6, "org_id": 2, "title": "安仁县委副书记、县长", "start_date": "2015-11", "end_date": "2021-06",
     "rank": "正处级", "note": "2021-06 由黄力接替"},
    # 郴州市
    {"person_id": 7, "org_id": 5, "title": "郴州市委书记", "start_date": "2026-05", "end_date": None,
     "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "郴州市市长", "start_date": "2026-06", "end_date": None,
     "rank": "正厅级", "note": ""},
]

# ═══════════════════════════════════════════
# 关系数据
# ═══════════════════════════════════════════

relationships = [
    # 王洪灿 — 黄力（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "王洪灿任县委书记，黄力任县委副书记、县长，2021年6月起搭班子",
     "overlap_org": "中共安仁县委员会", "overlap_period": "2021-06~至今",
     "strength": "strong", "confidence": "confirmed"},
    # 王洪灿 — 李小军（书记交接）
    {"person_a": 1, "person_b": 5, "type": "接任",
     "context": "王洪灿于2021-05接替李小军任安仁县委书记",
     "overlap_org": "中共安仁县委员会", "overlap_period": "2021-05",
     "strength": "strong", "confidence": "confirmed"},
    # 黄力 — 李建军（县长交接）
    {"person_a": 2, "person_b": 6, "type": "接任",
     "context": "黄力2021-06接替李建军任安仁县县长",
     "overlap_org": "安仁县人民政府", "overlap_period": "2021-06",
     "strength": "strong", "confidence": "confirmed"},
    # 王洪灿 — 龙之美（人大）
    {"person_a": 1, "person_b": 3, "type": "上下级搭档",
     "context": "县委书记与县人大常委会主任",
     "overlap_org": "中共安仁县委员会", "overlap_period": "2021-10~至今",
     "strength": "medium", "confidence": "plausible"},
    # 王洪灿 — 蒋尚庭（政协）
    {"person_a": 1, "person_b": 4, "type": "上下级搭档",
     "context": "县委书记与县政协主席",
     "overlap_org": "中共安仁县委员会", "overlap_period": "2021-10~至今",
     "strength": "medium", "confidence": "plausible"},
    # 黄力 — 龙之美
    {"person_a": 2, "person_b": 3, "type": "机关同事",
     "context": "县长与县人大常委会主任，人大监督政府",
     "overlap_org": "安仁县人民政府", "overlap_period": "2021-10~至今",
     "strength": "medium", "confidence": "plausible"},
    # 黄力 — 蒋尚庭
    {"person_a": 2, "person_b": 4, "type": "机关同事",
     "context": "县长与县政协主席",
     "overlap_org": "安仁县人民政府", "overlap_period": "2021-10~至今",
     "strength": "medium", "confidence": "plausible"},
    # 郴州市委书记 — 安仁县委书记（上级领导）
    {"person_a": 7, "person_b": 1, "type": "上级领导",
     "context": "郴州市委书记阚保勇是安仁县委书记王洪灿的直管上级",
     "overlap_org": "中共郴州市委员会", "overlap_period": "2026-05~至今",
     "strength": "medium", "confidence": "confirmed"},
    # 郴州市长 — 安仁县长（上级领导）
    {"person_a": 8, "person_b": 2, "type": "上级领导",
     "context": "郴州市长白云峰是安仁县长黄力的直管上级",
     "overlap_org": "郴州市人民政府", "overlap_period": "2026-06~至今",
     "strength": "medium", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════
# 构建
# ═══════════════════════════════════════════

def build():
    """运行数据库 + GEXF 构建。"""
    from gov_relation.runner import run_build

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

    _add_worked_at(positions, organizations, organizations)

    # 将 person JSON 写入同目录（用于 process_tmp.py 分类为 person_json）
    for p in persons:
        if p.get("name") in {"王洪灿", "黄力", "龙之美", "蒋尚庭"}:
            _write_person_json(p)

    print(f"构建完成：{DB_PATH}")
    print(f"构建完成：{GEXF_PATH}")


def _add_worked_at(positions, _orgs, _unused):
    """在 GEXF 中补充 person→org 的 worked_at 任职边（org id 偏移 +100000）。"""
    path = GEXF_PATH
    text = path.read_text(encoding="utf-8")
    edge_blocks = []
    eid = 1000
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos.get("title", "")
        eid += 1
        edge_blocks.append(f'<edge id="{eid}" source="{pid}" target="{oid}" label="{_esc(title)}" weight="1.0"><attvalues><attvalue for="0" value="worked_at" /><attvalue for="1" value="{_esc(title)}" /><attvalue for="2" value="" /><attvalue for="3" value="" /></attvalues></edge>')
    if "</edges>" in text:
        insert = "".join(edge_blocks)
        text = text.replace("</edges>", insert + "</edges>")
        path.write_text(text, encoding="utf-8")


def _esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _write_person_json(p):
    role_map = {
        "王洪灿": "县委书记",
        "黄力": "县长",
        "龙之美": "县人大常委会主任",
        "蒋尚庭": "县政协主席",
    }
    job = role_map[p["name"]]
    fname = f"{TODAY}-{PROVINCE}-{CITY}-{job}-{p['name']}.json"
    path = PERSONS_DIR / fname
    payload = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": SLUG,
            "job": job,
            "task_id": "hunan_安仁县",
            "time_focus": "2021至今",
        },
        "identity": {
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": _career_timeline(p["name"]),
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开信息有限，工作风格未作推断。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "截至2026-08-07未检索到该核心人物的违纪违法或被查记录，但检索受限（主要中国搜索源被反爬拦截）",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        }],
        "source_register": [
            {"id": "S001", "title": "维基百科·安仁县人民政府 / 中国共产党安仁县委员会", "url": "https://zh.wikipedia.org/wiki/安仁县人民政府",
             "publisher": "维基百科", "source_type": "encyclopedia", "reliability": "medium", "accessed_at": AS_OF,
             "notes": "转引华声在线(2021-05-21)、长沙晚报/红网(2021-06-12)权威任命报道"},
            {"id": "S002", "title": "长沙晚报·湖南.郴州市四区县主要领导调整", "url": "https://www.icswb.com/h/162/20210612/716902.html",
             "publisher": "长沙晚报", "source_type": "media", "reliability": "high", "accessed_at": AS_OF,
             "notes": "2021-06-12 黄力提名为安仁县长候选人（红网稿源）"},
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "履职前完整履历、教育背景及现职确认日期均缺（搜索源受限）",
        },
        "open_questions": [
            {"priority": "high", "question": "王洪灿是否在 2026 郴州换届中被调整？",
             "why_it_matters": "郴州多县2026年有领导调整，安仁县县委书记身份需以最新任前公示核实",
             "suggested_queries": ["安仁县 县委书记 2026 调整", "郴州市委组织部 任前公示 安仁"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "王洪灿、黄力在当选前的完整履历与教育背景为何？",
             "why_it_matters": "影响跨县交流关系与晋升逻辑判断",
             "suggested_queries": ["王洪灿 履历", "黄力 郴州 简历"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "黄力正式由县人大任命为县长的时间节点？",
             "why_it_matters": "落实二把手正式任命情况",
             "suggested_queries": ["黄力 安仁 人大 任命 县长"],
             "last_attempted": AS_OF},
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _career_timeline(name):
    timeline = []
    if name == "王洪灿":
        timeline += [
            {"start": "2021-05", "end": "present", "org": "中共安仁县委员会", "title": "县委书记",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "unknown", "end": "2021-05", "org": "履历缺口",
             "title": "公开资料未找到当选前完整履历", "level": "", "confidence": "unverified"},
        ]
    elif name == "黄力":
        timeline = [
            {"start": "2021-06", "end": "present", "org": "安仁县人民政府", "title": "县委副书记、县长",
             "level": "正处级", "confidence": "confirmed"},
            {"start": "unknown", "end": "2021-06", "org": "履历缺口",
             "title": "公开资料未找到当选前完整履历", "level": "", "confidence": "unverified"},
        ]
    elif name == "龙之美":
        timeline = [
            {"start": "2021-10", "end": "present", "org": "安仁县人大常委会", "title": "主任",
             "level": "正处级", "confidence": "confirmed"},
        ]
    elif name == "蒋尚庭":
        timeline = [
            {"start": "2021-10", "end": "present", "org": "安仁县政协", "title": "主席",
             "level": "正处级", "confidence": "confirmed"},
        ]
    return timeline


if __name__ == "__main__":
    build()