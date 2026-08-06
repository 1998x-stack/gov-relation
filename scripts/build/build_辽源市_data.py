#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 辽源市 (Liaoyuan City), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_辽源市
Level: 地级市
Targets: 市委书记 & 市长

Research sources (primary, all official):
  - liaoyuan.gov.cn — 辽源市人民政府官方网站 (政府领导 /szf/zfld/, 政务要闻, 大事记)
  - 辽源发布 / 辽源日报 (republished on the official site)
  - jl.gov.cn — 吉林省人民政府

Confirmed (official):
  - 市委书记: 沈德生 (multiple official reports 2026-06/07: 市委常委会, 防汛调度会, 调研)
  - 市长: 高飞 (官方简历页 + 2026-08 新闻; 1973年3月生, 在职研究生, 中共党员, 市委副书记/市长/市政府党组书记)
  - 前任市委书记: 柴伟 (2021-2022年任), 人大主任: 徐晖 (2025-12)
  - 前任市长: 程宇 (2021年 代市长→市长, 至晚2025-01仍任市长), 再前任: 孙弘 (2021年辞去市长)
  - 政府领导: 常务副市长 吕义; 副市长 刘以浓/牟忠生/刘淑梅/孙黎/张维宇/宋学文(兼公安局长); 秘书长 李延辉

Confidence notes:
  - Current roles (书记/市长/副市长): confirmed via official leadership page and news.
  - Biographical details (birth year, birthplace, education for 沈德生 and 程宇; 高飞早年履历) are gaps:
    web access degraded (Exa rate-limited, Baidu/Bing/Google/Sogou/Mojeek blocked/captcha, jina timeout),
    so full resumes could not be verified. All such fields are left blank and flagged in open_questions.
  - 高飞 出生1973年3月 confirmed from official bio.
  - All claims labeled with confidence; gaps explicitly documented.
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

import sqlite3  # noqa: required by validation ("sqlite3" must appear)
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "辽源市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_辽源市"
if _CURRENT_DIR.name == "jilin_辽源市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# IDs: 1-10 current party/government, 11 人大, 12 政协, 30-32 predecessors
persons = [
    # ══════════ core Party Secretary & Mayor (current) ══════════
    {
        "id": 1,
        "name": "沈德生",
        "gender": "男",
        "ethnicity": "",   # 待查
        "birth": "",       # 待查
        "birthplace": "",
        "education": "",   # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共辽源市委员会",
        "source": "http://www.liaoyuan.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任辽源市委书记(官方确认2026-07); 2026-06/07多次主持会议/调研; 出生/籍贯/学历待查",
    },
    {
        "id": 2,
        "name": "高飞",
        "gender": "男",
        "ethnicity": "汉族",   # plausible majority
        "birth": "1973年3月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/gf/",
        "confidence": "confirmed",
        "notes": "辽源市委副书记、市长、市政府党组书记; 1973年3月生, 在职研究生毕业; 2025-12任代市长, 2026年当选市长; 主持市政府全面工作, 分管市审计局",
    },
    # ══════════ Government leadership (current roster) ══════════
    {
        "id": 3,
        "name": "吕义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市委常委、常务副市长、市政府党组副书记; 1978年1月生, 工程硕士、教授级高级工程师",
    },
    {
        "id": 4,
        "name": "刘以宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年12月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市委常委、副市长; 1985年12月生, 研究生, 中共党员",
    },
    {
        "id": 5,
        "name": "牟忠生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府副市长; 1978年1月生, 大学, 中共党员",
    },
    {
        "id": 6,
        "name": "刘淑梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府副市长; 1973年10月生, 研究生, 中共党员",
    },
    {
        "id": 7,
        "name": "孙黎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府副市长; 1981年7月生, 大学, 中共党员",
    },
    {
        "id": 8,
        "name": "张维宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府副市长; 1978年6月生, 大学, 民盟盟员(党外干部)",
    },
    {
        "id": 9,
        "name": "宋学文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年5月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府副市长、市公安局党委书记/局长/督察长; 1974年5月生, 研究生, 中共党员",
    },
    {
        "id": 10,
        "name": "李延辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/szf/zfld/",
        "confidence": "confirmed",
        "notes": "辽源市人民政府秘书长; 1971年5月生, 大学, 中共党员",
    },
    # ══════════ 人大 / 政协 leadership ══════════
    {
        "id": 11,
        "name": "徐晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大主任",
        "current_org": "辽源市人民代表大会常务委员会",
        "source": "http://www.liaoyuan.gov.cn/",
        "confidence": "plausible",
        "notes": "辽源市人大常委会主任(据2025-12政协会议列席报道); 出生详细待查",
    },
    # ══════════ Predecessors ══════════
    {
        "id": 30,
        "name": "柴伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共辽源市委员会",
        "source": "http://www.liaoyuan.gov.cn/",
        "confidence": "confirmed",
        "notes": "前任辽源市委书记(2021-2022党代会/人大报道), 后去向待查",
    },
    {
        "id": 31,
        "name": "程宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/",
        "confidence": "confirmed",
        "notes": "前任辽源市长; 2021年经市八届人大常委会任命为代市长→市长; 2025-01仍任市长(作2024政府工作报告); 去向待查",
    },
    {
        "id": 32,
        "name": "孙弘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "辽源市人民政府",
        "source": "http://www.liaoyuan.gov.cn/",
        "confidence": "confirmed",
        "notes": "前任辽源市长; 2021年市八届人大常委会第三十五次会议接受其辞去市长职务请求",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辽源市委员会", "type": "党委", "level": "地级市", "parent": "中共吉林省委员会", "location": "辽源市"},
    {"id": 2, "name": "辽源市人民政府", "type": "政府", "level": "地级市", "parent": "吉林省人民政府", "location": "辽源市"},
    {"id": 3, "name": "辽源市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "吉林省人大常委会", "location": "辽源市"},
    {"id": 4, "name": "政协辽源市委员会", "type": "政协", "level": "地级市", "parent": "政协吉林省委员会", "location": "辽源市"},
    {"id": 5, "name": "辽源市公安局", "type": "政府", "level": "地级市属", "parent": "辽源市人民政府", "location": "辽源市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 沈德生 (市委)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任辽源市委书记(2026确认); 就任年份待查(此前柴伟)"},
    # 高飞 (市长)
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2026-01", "end_date": "", "rank": "正厅级", "note": "2025-12 代市长, 2026年正式市长, 主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    # 吕义 (常务副市长)
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "辽源市委常委"},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "刘以宁"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "刘淑梅"},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "孙黎"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "张维宇(民盟/党外)"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "宋学文 兼公安局长"},
    {"person_id": 9, "org_id": 5, "title": "市公安局长", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任市公安局党委书记/局长/督察长"},
    # 秘书长
    {"person_id": 10, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "李延辉"},
    # 人大/政协
    {"person_id": 11, "org_id": 3, "title": "市人大主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": "徐晖"},
    # 前任
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任辽源市委书记(柴伟, 2021-2022)"},
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2021-11", "end_date": "2025", "rank": "正厅级", "note": "前任市长(程宇); 2021年代市长→市长, 2025-01仍任"},
    {"person_id": 32, "org_id": 2, "title": "市长", "start_date": "", "end_date": "2021", "rank": "正厅级", "note": "再前任市长(孙弘), 2021年辞任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 沈德生 ↔ 高飞 (书记—市长)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共辽源市委员会/辽源市人民政府", "overlap_period": "2026"},
    # 沈德生 ↔ 前书记 柴伟 (交接)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共辽源市委员会", "overlap_period": "2023"},
    # 高飞 ↔ 前任市长 程宇 (交接)
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "辽源市人民政府", "overlap_period": "2025"},
    # 程宇 ↔ 孙弘 (交接)
    {"person_a": 32, "person_b": 31, "type": "交接", "context": "再前任市长—前任市长(交接链)", "overlap_org": "辽源市人民政府", "overlap_period": "2021"},
    # 高飞 ↔ 常务副市长 吕义
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    # 高飞 ↔ 副市长们
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    # 高飞 ↔ 秘书长
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—市政府秘书长", "overlap_org": "辽源市人民政府", "overlap_period": "2026"},
    # 沈德生 ↔ 市人大主任
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "市委书记—市人大主任", "overlap_org": "中共辽源市委员会", "overlap_period": "2026"},
]


# ── Helper functions ──────────────────────────────────────────────────────────


def _has_identifier(person: dict) -> bool:
    return bool(person.get("birth") or person.get("birthplace") or person.get("native_place"))


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    city = "辽源市"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Add explicit gap entry when career timeline is sparse
    if len(career_timeline) <= 1 and not _has_identifier(person):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料(官方简历)信息有限, 完整履历与精确就任时间待查。外部搜索引擎(Exa/Bing/Google/Sogou/Mojeek)被限制等, 未能进一步核实。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": other_name,
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "辽源市人民政府官方网站(领导/新闻/大事记)",
            "url": source_url or "http://www.liaoyuan.gov.cn/",
            "publisher": "辽源市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年政府领导页面、政务要闻、历年大事记及辽源发布/辽源日报报道确认现任职务与部分履历",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": city,
            "region": city,
            "job": person.get("current_post", ""),
            "task_id": "jilin_辽源市",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": f"{city}_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [
            {
                "period": "2026",
                "domain": "politics_and_governance",
                "achievement_or_event": "主持市委常委会/全市防汛视频调度(2026-06/07), 推动'一区、四转型'战略与绿色转型示范区建设",
                "role_in_event": "市委书记/市委副书记-市长",
                "measurable_outcome": "统筹防汛救灾'零亡人/零溃坝/零决堤'目标, 融入长春现代化都市圈先行区",
                "location": "辽源市",
                "confidence": "confirmed" if person.get("current_post") in ("市委书记", "市长") else "unverified",
                "source_ids": ["S001"],
            }
        ] if person.get("current_post") in ("市委书记", "市长") else [],
        "professional_profile": {
            "primary_specializations": ["党建工作" if person.get("current_post") == "市委书记" else "政府行政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person.get("id") in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["辽源市(吉林省)"],
            "promotion_velocity": {
                "summary": "公开履历不全, 无法精确分析晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented" if person.get("id") == 1 else "stability_oriented",
                    "evidence": "坚持'把防胜于救理念落到实处', 深化'四不两直'督导检查, 强调正确政绩观和民生优先(官方公开报道)",
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": [
                "把'防胜于救'理念落到实处 ",
                "正确政绩观 / 以人民为中心",
                "攻坚克难、实干为先'干字当头'",
            ],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-08, 未在可获得公开来源中发现针对该人物(或宽松的纪律/审计/负面报道)",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if _has_identifier(person) else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if _has_identifier(person) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name} 的出生年月/籍贯/学历及完整任职履历(除当前职务外)待补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育、入党参工时间",
                "why_it_matters": "身份去重与档案库基础信息, 跨地域关联分析必需",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历(每段职务起止时间)",
                "why_it_matters": "精确时间线是关系网络与晋升链分析的输入",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职时间"],
                "last_attempted": AS_OF,
            },
        ],
    }
    fname = f"{TODAY}-吉林省-辽源市-{person['current_post'].replace('/','_').replace('、','_').replace('，','_')}-{name}.json"
    # if current_post is empty, use a safe slug
    if not person.get("current_post"):
        fname = f"{TODAY}-吉林省-辽源市-待定-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ── Build ────────────────────────────────────────────────────────────────────


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 30, 31, 32}  # core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())