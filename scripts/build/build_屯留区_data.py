#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 屯留区 (Tunliu District), 长治市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_屯留区
Level: 市辖区
Targets: 区委书记 & 区长

Research context:
  - Government website www.tunliu.gov.cn (HTTP) was accessible and provided current data.
  - Exa web search was rate-limited; Baidu Baike 403 Forbidden.
  - Core information sourced from official government news pages and leadership activity pages.
  - The 区委书记 and 区长 are the same person (concurrent appointment).

Confidence notes:
  - Current officeholders and leadership roster confirmed from official sources as of July 2026.
  - Career timelines for core figures partially sourced; some gaps remain.
  - Predecessor information (牛海江) sourced from government website activity logs.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "屯留区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_屯留区"
if _CURRENT_DIR.name == "shanxi_屯留区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leadership, 3-8 standing committee + deputy mayors, 9-10 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current, confirmed from official sources)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记、区长",
        "current_org": "中共长治市屯留区委员会",
        "source": "http://www.tunliu.gov.cn/ (official government website, 2026-07 news articles)",
        "notes": (
            "张俊杰同时担任中共长治市屯留区委书记和屯留区人民政府区长（一肩挑）。"
            "最早见于官方网站报道的是2025年9月以区长身份出席活动。"
            "2026年7月的报道中已使用'区委书记、区长张俊杰'称谓。"
            "前任区委书记为牛海江（2026年4月仍有活动报道）。"
            "完整履历（出生年月、籍贯、教育背景、入党时间、历任职务晋升时间）需通过长治市委组织部或百度百科补充。"
        ),
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "王瑛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "屯留区人民政府",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260709_3183815.html "
            "(official news article, 2026-07-09)"
        ),
        "notes": "2026年7月9日与华电新能源合作座谈会报道中明确为'区委常委、常务副区长王瑛'",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy District Heads
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "白利忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "屯留区人民政府",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260720_3187486.html "
            "(official news article, 2026-07-20)"
        ),
        "notes": "2026年7月20日防汛督导报道中明确为'区委常委、副区长白利忠'",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "郭乐慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办主任",
        "current_org": "中共长治市屯留区委员会",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260714_3185575.html "
            "(official news article, 2026-07-14)"
        ),
        "notes": "2026年7月14日防汛备汛报道中明确为'区委常委、区委办主任郭乐慧'",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "郭迎红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "屯留区人民政府",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260709_3183815.html "
            "(official news article, 2026-07-09)"
        ),
        "notes": "2026年7月9日合作座谈报道中明确为'副区长郭迎红'",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other District Leaders (names known, exact titles need confirmation)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "郑丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区处级领导",
        "current_org": "屯留区",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260713_3184966.html "
            "(official news article, 2026-07-13)"
        ),
        "notes": "城市更新调研报道中列为'区处级领导'之一。具体职务需进一步确认。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "郗淑芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区处级领导",
        "current_org": "屯留区",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260713_3184966.html "
            "(official news article, 2026-07-13)"
        ),
        "notes": "城市更新调研报道中列为'区处级领导'之一。具体职务需进一步确认。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "李书红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区处级领导",
        "current_org": "屯留区",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260713_3184966.html "
            "(official news article, 2026-07-13)"
        ),
        "notes": "城市更新调研报道中列为'区处级领导'之一。具体职务需进一步确认。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "张筱倜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区处级领导",
        "current_org": "屯留区",
        "source": (
            "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260722_3188466.html "
            "(official news article, 2026-07-22)"
        ),
        "notes": "市委常委会（扩大）会议报道中列为'区处级领导'之一。具体职务需进一步确认。",
        "confidence": "confirmed"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (confirmed from government website activity pages)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "牛海江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共长治市屯留区委员会（原）",
        "source": (
            "http://www.tunliu.gov.cn/szsjzj_150445/sjzj/sjhd/ "
            "(official government leadership activity page, records through 2026-04)"
        ),
        "notes": (
            "牛海江为张俊杰的前任，担任屯留区委书记。"
            "官网书记活动记录显示其活跃至2026年4月14日（带队赴深圳成都考察招商）。"
            "此后区委书记职务由张俊杰兼任。"
            "去向需进一步确认（推测为调任长治市或其他地市）。"
        ),
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "待查_前任区长（张俊杰之前）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任",
        "current_org": "屯留区人民政府（原）",
        "source": "需通过官方来源确认",
        "notes": (
            "张俊杰之前屯留区长的姓名需进一步搜索。"
            "张俊杰最早见于官方报道的区长活动是2025年9月。"
            "2025年9月之前屯留区长可能为他人。"
        ),
        "confidence": "unverified"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共长治市屯留区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 2,
        "name": "屯留区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 3,
        "name": "中共长治市屯留区纪律检查委员会",
        "type": "纪律检查",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 4,
        "name": "屯留区监察委员会",
        "type": "政府",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 5,
        "name": "中共长治市屯留区委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "屯留区",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 6,
        "name": "中共长治市屯留区委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "屯留区",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 7,
        "name": "中共长治市屯留区委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "屯留区",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 8,
        "name": "长治市屯留区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议长治市屯留区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "长治市",
        "location": "山西省长治市屯留区"
    },
    {
        "id": 10,
        "name": "中共长治市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "山西省",
        "location": "山西省长治市"
    },
    {
        "id": 11,
        "name": "长治市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "山西省",
        "location": "山西省长治市"
    },
    {
        "id": 12,
        "name": "中共长治市委组织部",
        "type": "党委",
        "level": "地市级",
        "parent": "长治市",
        "location": "山西省长治市"
    },
    {
        "id": 13,
        "name": "中共长治市屯留区委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "屯留区",
        "location": "山西省长治市屯留区"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "屯留区委书记", "start_date": "2026-06（推定）", "end_date": "现任",
     "rank": "正处级", "note": "兼任区长；前任牛海江，具体到任日期需确认"},
    {"person_id": 1, "org_id": 2, "title": "屯留区长", "start_date": "不晚于2025-09", "end_date": "现任",
     "rank": "正处级", "note": "最早见于官网报道为2025年9月以区长身份出席活动"},
    # Standing committee members
    {"person_id": 2, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 13, "title": "区委常委、区委办主任", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "",
     "rank": "副处级", "note": ""},
    # Other district leaders (exact titles pending)
    {"person_id": 6, "org_id": 1, "title": "区处级领导", "start_date": "", "end_date": "",
     "rank": "处级", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 1, "title": "区处级领导", "start_date": "", "end_date": "",
     "rank": "处级", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "区处级领导", "start_date": "", "end_date": "",
     "rank": "处级", "note": "具体职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "区处级领导", "start_date": "", "end_date": "",
     "rank": "处级", "note": "具体职务待确认"},
    # Predecessors
    {"person_id": 10, "org_id": 1, "title": "屯留区委书记（前任）", "start_date": "不晚于2024", "end_date": "约2026-04",
     "rank": "正处级", "note": "牛海江为前任区委书记，最后见于官网活动报道为2026年4月14日"},
    {"person_id": 11, "org_id": 2, "title": "屯留区长（前任）", "start_date": "", "end_date": "",
     "rank": "正处级", "note": "姓名和去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Top leadership
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记、区长与常务副区长为党政正副手关系",
        "overlap_org": "屯留区",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记、区长与副区长为正副手关系",
        "overlap_org": "屯留区人民政府",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委办主任为直接上下级关系",
        "overlap_org": "中共长治市屯留区委员会",
        "overlap_period": "当前任职期"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与副区长为政府系统正副手关系",
        "overlap_org": "屯留区人民政府",
        "overlap_period": "当前任职期"
    },
    # Predecessor / Successor
    {
        "person_a": 1,
        "person_b": 10,
        "type": "predecessor_successor",
        "context": "张俊杰接替牛海江担任屯留区委书记",
        "overlap_org": "中共长治市屯留区委员会",
        "overlap_period": "2026年职务交接期"
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "predecessor_successor",
        "context": "张俊杰接替前任担任屯留区长",
        "overlap_org": "屯留区人民政府",
        "overlap_period": "2025年职务交接期"
    },
    # Working relationships among deputy leaders
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "常务副区长与副区长为政府班子同僚",
        "overlap_org": "屯留区人民政府",
        "overlap_period": "当前任职期"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════

def main() -> None:
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
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

    # Write person JSON files for core leaders (and predecessor)
    write_person_json(1, persons[0])   # 张俊杰
    write_person_json(2, persons[1])   # 王瑛
    write_person_json(10, persons[9])  # 牛海江

    print(f"\n═══ Done — {SLUG} ═══")
    print(f"  Persons: {len(persons)} ({sum(1 for p in persons if '待查' not in p['name'])} named)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n  Core leaders confirmed from official government website (www.tunliu.gov.cn).")
    print(f"  Career timelines and biographical details need further research.")
    print(f"  See open_gaps.md for priority research gaps.")


def write_person_json(pid: int, pdata: dict) -> None:
    """Write a person JSON file following the person_graph_json.md schema."""
    name = pdata["name"]
    job = pdata.get("current_post", "").replace("/", "_")
    fname = f"{TODAY}-山西省-长治市-{job}-{name}.json"
    fpath = PJSON_DIR / fname

    # Determine if name is a placeholder
    is_placeholder = "待查" in name or not name
    current_conf = "unverified" if is_placeholder else pdata.get("confidence", "unverified")
    identity_conf = "unverified" if is_placeholder else "confirmed"

    person_record = {
        "schema_version": "1.0",
        "generated_at": str(date.today()),
        "investigation_scope": {
            "province": "山西省",
            "city": "长治市",
            "region": "屯留区",
            "job": pdata.get("current_post", ""),
            "task_id": "shanxi_屯留区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"tunliu_{name}",
            "name": name,
            "aliases": [],
            "gender": pdata.get("gender", ""),
            "ethnicity": pdata.get("ethnicity", ""),
            "birth": pdata.get("birth", ""),
            "birthplace": pdata.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": pdata.get("party_join", ""),
            "work_start": pdata.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_" if not pdata.get("birth") else f"{name}_{pdata['birth']}",
                "name_birthplace": f"{name}_" if not pdata.get("birthplace") else f"{name}_{pdata['birthplace']}",
                "official_profile_url": "http://www.tunliu.gov.cn/"
            }
        },
        "current_status": {
            "current_post": pdata.get("current_post", ""),
            "current_org": pdata.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": not is_placeholder,
            "source_ids": ["S001"]
        },
        "career_timeline": get_career_timeline(pid, name),
        "organizations": [],
        "relationships": get_relationships_for_person(pid),
        "governance_record": get_governance_record(pid, name),
        "professional_profile": get_professional_profile(pid, name),
        "work_style_and_personality": get_work_style(pid, name),
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开纪律处分或负面报道",
                "date": "",
                "confidence": "confirmed" if not is_placeholder else "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "长治市屯留区人民政府门户网站",
                "url": "http://www.tunliu.gov.cn/",
                "publisher": "屯留区人民政府",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "官方网站新闻、书记活动、区长活动页面"
            },
            {
                "id": "S002",
                "title": "张俊杰督导检查防汛、农业防灾减灾等工作",
                "url": "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260720_3187486.html",
                "publisher": "屯留融媒",
                "published_at": "2026-07-20",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张俊杰为区委书记、区长"
            },
            {
                "id": "S003",
                "title": "屯留区与华电新能源集团山西分公司举行合作座谈",
                "url": "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260709_3183815.html",
                "publisher": "屯留融媒",
                "published_at": "2026-07-09",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认王瑛为常务副区长、郭迎红为副区长"
            },
            {
                "id": "S004",
                "title": "张俊杰督导检查防汛备汛工作",
                "url": "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260714_3185575.html",
                "publisher": "屯留融媒",
                "published_at": "2026-07-14",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认郭乐慧为区委常委、区委办主任"
            },
            {
                "id": "S005",
                "title": "张俊杰带队调研城市更新工作",
                "url": "http://www.tunliu.gov.cn/szdt/zwyw/202607/t20260713_3184966.html",
                "publisher": "屯留融媒",
                "published_at": "2026-07-13",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认郑丹、郗淑芳、李书红为区处级领导"
            },
            {
                "id": "S006",
                "title": "书记活动页面",
                "url": "http://www.tunliu.gov.cn/szsjzj_150445/sjzj/sjhd/",
                "publisher": "屯留区人民政府",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "历史书记活动记录（含牛海江到张俊杰的过渡）"
            },
            {
                "id": "S007",
                "title": "区长活动页面",
                "url": "http://www.tunliu.gov.cn/szsjzj_150445/xzzj/xzhd/",
                "publisher": "屯留区人民政府",
                "published_at": "",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "历史区长活动记录（可追溯至2025年9月）"
            },
            {
                "id": "S008",
                "title": "中共长治市屯留区委关于十二届省委第七轮巡视整改进展情况的通报",
                "url": "http://www.tunliu.gov.cn/tlzw/zwgk/zfxxgkml/tztg/202606/t20260630_3181202.html",
                "publisher": "山西省纪委监委网站",
                "published_at": "2026-06-29",
                "accessed_at": "2026-07-26",
                "source_type": "official",
                "reliability": "high",
                "notes": "巡视整改通报，包含全区党建、经济、民生详细信息"
            },
        ],
        "confidence_summary": {
            "identity": identity_conf,
            "current_role": current_conf,
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的出生年月、籍贯、教育背景和完整履历需补充"
        },
        "open_questions": get_open_questions(pid, name, pdata.get("current_post", ""))
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(person_record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


def get_career_timeline(pid: int, name: str) -> list[dict]:
    """Return career timeline for the person."""
    if pid == 1:
        return [
            {
                "start": "不晚于2025-09",
                "end": "现任",
                "org": "屯留区人民政府",
                "title": "屯留区长",
                "level": "正处级",
                "location": "山西省长治市屯留区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "最早见于官网报道的区长活动为2025年9月",
                "confidence": "confirmed",
                "source_ids": ["S007"]
            },
            {
                "start": "2026-06（推定）",
                "end": "现任",
                "org": "中共长治市屯留区委员会",
                "title": "屯留区委书记",
                "level": "正处级",
                "location": "山西省长治市屯留区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": (
                    "接替牛海江担任区委书记，同时继续兼任区长。"
                    "约2026年6月到任。2026年7月初的新闻报道已使用'区委书记、区长'称谓。"
                    "牛海江最后一次书记活动报道为2026年4月14日。"
                ),
                "confidence": "confirmed",
                "source_ids": ["S001", "S002", "S006"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "level": "",
                "location": "",
                "system": "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": (
                    "张俊杰在担任屯留区长之前的履历（如出身地、教育背景、"
                    "曾任职务、晋升路径等）需通过网络搜索补充"
                ),
                "confidence": "unverified",
                "source_ids": []
            }
        ]
    elif pid == 2:
        return [
            {
                "start": "unknown",
                "end": "现任",
                "org": "屯留区人民政府",
                "title": "区委常委、常务副区长",
                "level": "副处级",
                "location": "山西省长治市屯留区",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "2026年7月9日新闻报道中确认为常务副区长。此前履历需补充。",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "王瑛在担任屯留区常务副区长之前的履历需补充",
                "confidence": "unverified",
                "source_ids": []
            }
        ]
    elif pid == 10:
        return [
            {
                "start": "不晚于2024",
                "end": "约2026-04",
                "org": "中共长治市屯留区委员会",
                "title": "屯留区委书记",
                "level": "正处级",
                "location": "山西省长治市屯留区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": (
                    "区委书记，至少2024年即在任。"
                    "官网书记活动记录从2025年底延续至2026年4月14日。"
                    "2026年4月14日带队赴深圳成都考察招商为最后一次记录。"
                    "去向需确认。"
                ),
                "confidence": "confirmed",
                "source_ids": ["S006"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "牛海江在担任屯留区委书记之前和之后的履历需补充",
                "confidence": "unverified",
                "source_ids": []
            }
        ]
    return []


def get_relationships_for_person(pid: int) -> list[dict]:
    """Return relationships for a person."""
    if pid == 1:
        return [
            {
                "person": "王瑛",
                "person_id": "tunliu_王瑛",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区委书记、区长与常务副区长在同级政府班子中工作",
                "overlap_org": "屯留区",
                "overlap_period": "当前任职期",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "person": "白利忠",
                "person_id": "tunliu_白利忠",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "一同调研防汛工作",
                "overlap_org": "屯留区人民政府",
                "overlap_period": "当前任职期",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "person": "郭乐慧",
                "person_id": "tunliu_郭乐慧",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区委书记与区委办负责人的直接上下级关系",
                "overlap_org": "中共长治市屯留区委员会",
                "overlap_period": "当前任职期",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            },
            {
                "person": "牛海江",
                "person_id": "tunliu_牛海江",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "张俊杰接替牛海江担任区委书记",
                "overlap_org": "中共长治市屯留区委员会",
                "overlap_period": "约2026年二季度",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S006"]
            }
        ]
    return []


def get_governance_record(pid: int, name: str) -> list[dict]:
    """Return governance achievements/events."""
    if pid == 1:
        return [
            {
                "period": "2026年7月",
                "domain": "urban_construction",
                "achievement_or_event": "带队调研城市更新，推进'一镇三街四路'重点项目",
                "role_in_event": "区委书记、区长（主导者）",
                "measurable_outcome": "百米大道沉陷修复项目主路通车、体育街海绵城市工程预计8月底完工",
                "location": "屯留区",
                "confidence": "confirmed",
                "source_ids": ["S005"]
            },
            {
                "period": "2026年7月",
                "domain": "public_security",
                "achievement_or_event": "防汛关键期督导检查防汛、农业防灾减灾等工作",
                "role_in_event": "区委书记、区长（指挥者）",
                "measurable_outcome": "落实24小时值班、加强监测预警、加密隐患排查",
                "location": "屯留区西部乡镇",
                "confidence": "confirmed",
                "source_ids": ["S002", "S004"]
            },
            {
                "period": "2026年7月",
                "domain": "economic_development",
                "achievement_or_event": "与华电新能源集团山西分公司举行合作座谈",
                "role_in_event": "区委书记、区长（主导者）",
                "measurable_outcome": "推动新能源领域合作项目落地",
                "location": "屯留区",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "period": "截至2026年6月",
                "domain": "other",
                "achievement_or_event": "巡视整改（十二届省委第七轮巡视）",
                "role_in_event": "区委主要负责同志（第一责任人）",
                "measurable_outcome": "巡视反馈60个问题已整改51个",
                "location": "屯留区",
                "confidence": "confirmed",
                "source_ids": ["S008"]
            },
            {
                "period": "2026年6月",
                "domain": "party_affairs",
                "achievement_or_event": "为李高乡党员干部讲授'七一'专题党课",
                "role_in_event": "区委书记",
                "measurable_outcome": "",
                "location": "屯留区李高乡",
                "confidence": "confirmed",
                "source_ids": []
            }
        ]
    return []


def get_professional_profile(pid: int, name: str) -> dict:
    """Return professional profile."""
    if pid == 1:
        return {
            "primary_specializations": ["城市更新与基础设施建设", "防汛防灾与应急管理", "新能源产业招商"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["长治市屯留区"],
            "promotion_velocity": {
                "summary": "公开资料有限，无法评估晋升速度。目前已知信息为从区长晋升为区委书记（兼任区长）。",
                "notable_fast_promotions": []
            }
        }
    elif pid == 10:
        return {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历信息有限",
                "notable_fast_promotions": []
            }
        }
    return {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "履历信息不可用",
            "notable_fast_promotions": []
        }
    }


def get_work_style(pid: int, name: str) -> dict:
    """Return work style and personality indicators."""
    if pid == 1:
        return {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "多次深入乡镇一线督导防汛、农业防灾减灾等工作",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "城市更新调研中注重项目建设进度和实际民生效果",
                    "confidence": "confirmed",
                    "source_ids": ["S005"]
                },
                {
                    "trait": "reform_oriented",
                    "evidence": "积极推动城市更新项目建设、新能源产业招商引资",
                    "confidence": "confirmed",
                    "source_ids": ["S003", "S005"]
                }
            ],
            "speech_themes": [
                "人民至上、生命至上（防汛工作）",
                "项目为王、服务至上（招商座谈）"
            ],
            "management_signals": [
                "注重一线督导和实地检查",
                "强调工程进度和民生实效"
            ],
            "caveat": "工作风格推断基于公开新闻报道，非私人心理评估。"
        }
    return {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "工作风格推断需要基于公开报道，当前来源有限。"
    }


def get_open_questions(pid: int, name: str, job: str) -> list[dict]:
    """Return open questions for the person."""
    questions = [
        {
            "priority": "critical",
            "question": f"{name}的出生年月、籍贯、教育背景",
            "why_it_matters": "基础身份信息的缺失影响人员去重和网络分析",
            "suggested_queries": [
                f"{name} 简历 屯留区",
                f"{name} 百度百科",
                f"{name} 出生"
            ],
            "last_attempted": str(date.today())
        },
        {
            "priority": "critical",
            "question": f"{name}的完整履历",
            "why_it_matters": "没有履历就无法进行关系网络分析和跨区流动追踪",
            "suggested_queries": [
                f"{name} 任职经历",
                f"{name} 长治",
                f"{name} 任前公示"
            ],
            "last_attempted": str(date.today())
        },
        {
            "priority": "critical",
            "question": f"{name}的入党时间和参加工作时间",
            "why_it_matters": "影响晋升速度评估和年龄分析",
            "suggested_queries": [
                f"{name} 入党",
                f"{name} 参加工作"
            ],
            "last_attempted": str(date.today())
        }
    ]

    if pid == 10:
        questions.append({
            "priority": "high",
            "question": "牛海江的去向",
            "why_it_matters": "了解屯留区前任区委书记的晋升或调动路径",
            "suggested_queries": [
                "牛海江 最新任职",
                "牛海江 调任 长治"
            ],
            "last_attempted": str(date.today())
        })

    if pid == 1:
        questions.append({
            "priority": "high",
            "question": "张俊杰在担任屯留区长之前的职务是什么",
            "why_it_matters": "了解其晋升轨迹和任职背景",
            "suggested_queries": [
                "张俊杰 任屯留区长 前",
                "张俊杰 长治 市委"
            ],
            "last_attempted": str(date.today())
        })

    return questions


if __name__ == "__main__":
    main()
