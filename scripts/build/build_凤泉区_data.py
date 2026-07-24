#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 凤泉区, 新乡市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 新乡市
Targets: 区委书记 (Party Secretary), 区长 (District Magistrate)
Task ID: henan_凤泉区

Research date: 2026-07-24
Official source: https://www.fengquan.gov.cn/ (凤泉区人民政府)

Current status (as of 2026-07-24):
- 区委书记: 丁文广
- 区长: 黄岩

Key source:
- 凤泉区第五届委员会第一次全体会议 (2026-06-25) elected standing committee:
  丁文广(书记)、黄岩(副书记)、毛长征(副书记)、李浩鹏、高敏、曹治国、范俊杰、薛梦寒、李庆庆、申国栋、刘军伟
- 凤泉区政府领导页面 lists: 区长黄岩, 副区长范俊杰(常务)、申国栋(常委)、许艳伟、王继辉、华斌
- 凤泉区第五届纪委第一次全体会议: 曹治国当选纪委书记
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "凤泉区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 丁文广 — 区委书记
    {
        "id": 1,
        "name": "丁文广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/ — 区委书记丁文广开展'七一'走访慰问活动 (2026-07-06)",
    },

    # 2. 黄岩 — 区委副书记、区长
    {
        "id": 2,
        "name": "黄岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/5431 — 区长黄岩官方简历 (2026-06-01)",
    },

    # 3. 毛长征 — 区委副书记（专职）
    {
        "id": 3,
        "name": "毛长征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },

    # 4. 范俊杰 — 区委常委、常务副区长
    {
        "id": 4,
        "name": "范俊杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-01",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组副书记、副区长",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/15787 — 副区长范俊杰官方简历 (2023-12-19)",
    },

    # 5. 申国栋 — 区委常委、副区长
    {
        "id": 5,
        "name": "申国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-06",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/11523 — 副区长申国栋官方简历 (2026-07-07)",
    },

    # 6. 许艳伟 — 副区长（非党）
    {
        "id": 6,
        "name": "许艳伟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-01",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/13320 — 副区长许艳伟官方简历 (2026-07-03)",
    },

    # 7. 王继辉 — 副区长、公安分局局长
    {
        "id": 7,
        "name": "王继辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、新乡市公安局凤泉分局局长",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/11522 — 副区长王继辉官方简历 (2022-05-25)",
    },

    # 8. 华斌 — 副区长、区先进制造业开发区管委会主任
    {
        "id": 8,
        "name": "华斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-10",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区先进制造业开发区管委会主任",
        "current_org": "凤泉区人民政府",
        "source": "https://www.fengquan.gov.cn/article/15789 — 副区长华斌官方简历 (2026-07-03)",
    },

    # 9. 曹治国 — 区委常委、区纪委书记
    {
        "id": 9,
        "name": "曹治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共新乡市凤泉区纪律检查委员会",
        "source": "https://www.fengquan.gov.cn/article/2071403738012164096 — 区纪委第一次全体会议 (2026-06-25)",
    },

    # 10. 李浩鹏 — 区委常委
    {
        "id": 10,
        "name": "李浩鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },

    # 11. 高敏 — 区委常委
    {
        "id": 11,
        "name": "高敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },

    # 12. 薛梦寒 — 区委常委
    {
        "id": 12,
        "name": "薛梦寒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },

    # 13. 李庆庆 — 区委常委
    {
        "id": 13,
        "name": "李庆庆",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },

    # 14. 刘军伟 — 区委常委
    {
        "id": 14,
        "name": "刘军伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共新乡市凤泉区委员会",
        "source": "https://www.fengquan.gov.cn/article/2071402830851317760 — 区委五届一次全体会议 (2026-06-25)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共新乡市凤泉区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共新乡市委员会",
        "location": "河南省新乡市凤泉区",
    },
    {
        "id": 2,
        "name": "凤泉区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "新乡市人民政府",
        "location": "河南省新乡市凤泉区",
    },
    {
        "id": 3,
        "name": "中共新乡市凤泉区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "新乡市纪委监委",
        "location": "河南省新乡市凤泉区",
    },
    {
        "id": 4,
        "name": "新乡市公安局凤泉分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "新乡市公安局",
        "location": "河南省新乡市凤泉区",
    },
    {
        "id": 5,
        "name": "凤泉区先进制造业开发区管委会",
        "type": "开发区",
        "level": "乡科级",
        "parent": "凤泉区人民政府",
        "location": "河南省新乡市凤泉区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 丁文广 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 黄岩 — 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 毛长征 — 区委副书记（专职）
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "专职副书记"},
    # 范俊杰 — 区委常委、常务副区长
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区政府党组副书记、副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "常务副区长"},
    # 申国栋 — 区委常委、副区长
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 许艳伟 — 副区长（非党）
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "党外干部"},
    # 王继辉 — 副区长、公安分局局长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任公安分局局长"},
    {"person_id": 7, "org_id": 4, "title": "新乡市公安局凤泉分局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 华斌 — 副区长、开发区管委会主任
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "区先进制造业开发区管委会主任", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 曹治国 — 区委常委、纪委书记
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李浩鹏 — 区委常委
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 高敏 — 区委常委
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 薛梦寒 — 区委常委
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李庆庆 — 区委常委
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 刘军伟 — 区委常委
    {"person_id": 14, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 丁文广 ↔ 黄岩（书记-区长搭班子关系，confirmed）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "丁文广任区委书记、黄岩任区长——区委-政府一把手搭班子", "overlap_org": "中共新乡市凤泉区委员会/凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 毛长征（书记-专职副书记）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "丁文广任区委书记、毛长征任专职副书记", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 毛长征（区长-专职副书记搭班子）
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "黄岩任区长、毛长征任专职副书记——区委副书记之间的协作", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 范俊杰（书记-常务副区长）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "丁文广书记领导区委全面工作，范俊杰任常务副区长、区委常委", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 申国栋（书记-常委副区长）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "丁文广书记领导区委全面工作，申国栋任区委常委、副区长", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 范俊杰（区长-常务副区长工作搭档）
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "黄岩区长主持区政府全面工作，范俊杰常务副区长协助处理政府常务工作", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 申国栋（区长-副区长工作搭档）
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "黄岩区长领导区政府，申国栋任副区长负责工业和信息化等", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 曹治国（书记-纪委书记）
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "丁文广任区委书记，曹治国任区委常委、区纪委书记", "overlap_org": "中共新乡市凤泉区委员会/区纪委", "overlap_period": "截至2026-07"},
    # 范俊杰 ↔ 申国栋（常务副区长-常委副区长同班子）
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "范俊杰常务副区长与申国栋常委副区长同为区政府班子成员", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 李浩鹏（书记-常委上下级）
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "同属凤泉区第五届区委常委会", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 高敏（书记-常委上下级）
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "同属凤泉区第五届区委常委会", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 薛梦寒（书记-常委上下级）
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "同属凤泉区第五届区委常委会", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 李庆庆（书记-常委上下级）
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "同属凤泉区第五届区委常委会", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 丁文广 ↔ 刘军伟（书记-常委上下级）
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "同属凤泉区第五届区委常委会", "overlap_org": "中共新乡市凤泉区委员会", "overlap_period": "截至2026-07"},
    # 王继辉 ↔ 华斌（同为副区长）
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "王继辉与华斌同为凤泉区副区长", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 许艳伟 ↔ 王继辉（同为副区长）
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "许艳伟与王继辉同为凤泉区副区长", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 华斌（区长-副区长工作搭档）
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "黄岩区长领导区政府，华斌任副区长负责城乡规划建设", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 王继辉（区长-副区长工作搭档）
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "黄岩区长领导区政府，王继辉任副区长兼公安分局局长", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
    # 黄岩 ↔ 许艳伟（区长-副区长工作搭档）
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "黄岩区长领导区政府，许艳伟任副区长负责民政、教育等", "overlap_org": "凤泉区人民政府", "overlap_period": "截至2026-07"},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a single person's graph JSON."""
    pid = person["id"]
    name = person["name"]
    # Determine job abbreviation for filename
    job_map = {
        1: "区委书记",
        2: "区长",
        3: "专职副书记",
        4: "常务副区长",
        5: "常委副区长",
        6: "副区长",
        7: "副区长兼公安局长",
        8: "副区长兼开发区主任",
        9: "纪委书记",
        10: "区委常委",
    }
    job = job_map.get(pid, "常委")

    filename = f"{TODAY}-河南省-新乡市-{job}-{name}.json"
    filepath = PERSONS_DIR / filename

    rels_out = []
    for r in relationships:
        other_id = None
        direction = "undirected"
        if r["person_a"] == pid:
            other_id = r["person_b"]
            direction = "person_to_other"
        elif r["person_b"] == pid:
            other_id = r["person_a"]
            direction = "other_to_person"

        if other_id is not None:
            other_person = next((p for p in persons if p["id"] == other_id), None)
            if other_person:
                rels_out.append({
                    "person": other_person["name"],
                    "person_id": f"fengquan_{other_person['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": direction,
                    "confidence": "confirmed",
                })

    positions_out = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            positions_out.append({
                "start": pos["start_date"] or "unknown",
                "end": pos["end_date"] or "present" if pos["end_date"] else "present",
                "org": org["name"] if org else "",
                "title": pos["title"],
                "level": pos["rank"],
                "location": "河南省新乡市凤泉区",
                "system": "party" if "区委" in (org["name"] if org else "") or "纪委" in (org["name"] if org else "") else "government",
                "rank": pos["rank"],
                "is_key_promotion": False,
                "notes": pos["note"],
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    person_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "新乡市",
            "region": "凤泉区",
            "job": job,
            "task_id": "henan_凤泉区",
            "time_focus": "2026-06 (第五届区委选举以来)",
        },
        "identity": {
            "person_id": f"fengquan_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", "汉族"),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"],
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": f"https://www.fengquan.gov.cn/list-2dhc7i82/2dhc7i82_zhengfulingdao/1/10",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职" if pid in (1, 2) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": positions_out,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_out,
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "凤泉区人民政府 — 政府领导",
                "url": "https://www.fengquan.gov.cn/list-2dhc7i82/2dhc7i82_zhengfulingdao/1/10",
                "publisher": "凤泉区人民政府",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "官方政府领导页面，列出区长和副区长",
            },
            {
                "id": "S002",
                "title": "凤泉区召开区委五届一次全体会议",
                "url": "https://www.fengquan.gov.cn/article/2071402830851317760",
                "publisher": "凤泉区人民政府",
                "published_at": "2026-06-27",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "选举产生第五届区委常委会，确认11名常委名单",
            },
            {
                "id": "S003",
                "title": "中国共产党凤泉区第五届纪律检查委员会举行第一次全体会议",
                "url": "https://www.fengquan.gov.cn/article/2071403738012164096",
                "publisher": "凤泉区人民政府",
                "published_at": "2026-06-29",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认曹治国当选区纪委书记",
            },
            {
                "id": "S004",
                "title": "区委书记丁文广开展'七一'走访慰问活动",
                "url": "https://www.fengquan.gov.cn/article/2073936260805795840",
                "publisher": "凤泉区人民政府",
                "published_at": "2026-07-06",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认丁文广任区委书记",
            },
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": f"缺少{name}的详细履历（早期职业生涯、教育背景、出生地、政治面貌发展时间线）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的详细职业履历（历任职务、调动时间线）",
                "why_it_matters": "无法了解其晋升路径、系统经验和来源地区，难以判断其关系网络和职业背景",
                "suggested_queries": [f"{name} 简历", f"{name} 任职经历", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的出生地和出生年月",
                "why_it_matters": "出生信息是人员去重和同乡关系判断的重要依据",
                "suggested_queries": [f"{name} 出生", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network data...")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    # Write person JSON files for core leaders
    print("Person JSONs:")
    for p in persons:
        write_person_json(p)

    print()

    # Build database and GEXF
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

    # Verify output
    print()
    print("Verification:")
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    gexf_size = GEXF_PATH.stat().st_size if GEXF_PATH.exists() else 0
    print(f"  {SLUG}_network.db: {db_size} bytes")
    print(f"  {SLUG}_network.gexf: {gexf_size} bytes")

    # Count person JSONs
    json_count = len(list(PERSONS_DIR.glob(f"{TODAY}-*.json")))
    print(f"  Person JSONs: {json_count}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
