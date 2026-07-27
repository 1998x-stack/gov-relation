#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 沙河口区, 大连市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 大连市
Targets: 区委书记 (Party Secretary: 姜茂生), 区长 (Mayor: 滕毓磐)
Task ID: liaoning_沙河口区

Investigation date: 2026-07-25
Official source: http://www.dlshk.gov.cn/ (大连市沙河口区人民政府)

Current status (as of 2026-07-25, verified via district government website news articles):
- 区委书记: 姜茂生 (男，汉族，原沙河口区长，2026年5月辞去区长职务，后转任区委书记)
- 区长: 滕毓磐 (2026年5月24日沙河口区十九届人大八次会议选举产生)
- 区人大常委会主任: 张洪运
- 区政协主席: 杨红艳
- 区委常委、区纪委书记/监委主任: 陈锋
- 副区长: 于雷、徐大明、刘晖(2026-07-03任命)、李婷(2026-07-03任命)
- 区法院院长: 杨全红
- 区检察院检察长: 金岩

Key timeline:
- 2026-05-19: 区人大常委会接受姜茂生辞去区长职务
- 2026-05-24: 区十九届人大八次会议选举产生新区长
- 2026-06-12: 姜茂生以区委书记身份主持警示教育会
- 2026-07-03: 任命刘晖、李婷为副区长
- 2026-07-06: 滕毓磐以区长身份列席区人大常委会第34次会议

Research confidence:
- Core leadership (书记/区长) identity: confirmed via official news articles
- Career histories: mostly unknown - no detailed bios available from public sources
- Predecessor info: limited - 姜茂生 was 区长 before becoming 书记
- Roster completeness: government leadership partially known; 区委常委 roster incomplete

Notes:
- 沙河口区 is a central urban district of Dalian city
- Website accessible at http://www.dlshk.gov.cn/ (政策公开 section)
- Web search tools (Exa, Baidu, Jina) were unavailable during this investigation
- All claims sourced from the district's own official news publications
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

import sqlite3  # noqa: F811 — used by gov_relation.runner

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "沙河口区"
DB_PATH = _STAGING_DIR / "data/database" / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / "data/graph" / f"{SLUG}_network.gexf"
TODAY = "20260725"
AS_OF = "2026-07-25"

PERSONS_DIR = _STAGING_DIR / "data/persons"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 姜茂生 — 区委书记 (former 区长)
    {
        "id": 1,
        "name": "姜茂生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共大连市沙河口区委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=2ad1a06684c7455ead4adf92b504fb71",
    },
    # 2. 滕毓磐 — 区委副书记、区长
    {
        "id": 2,
        "name": "滕毓磐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "大连市沙河口区人民政府",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },

    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════

    # 3. 前任区委书记 (before 姜茂生) — name unknown from available sources
    {
        "id": 3,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共大连市沙河口区委员会（已离任）",
        "source": "Information gap - needs further investigation",
    },

    # ════════════════════════════════════════
    # Key Leadership Roster
    # ════════════════════════════════════════

    # 4. 张洪运 — 区人大常委会主任
    {
        "id": 4,
        "name": "张洪运",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "沙河口区人民代表大会常务委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 5. 杨红艳 — 区政协主席
    {
        "id": 5,
        "name": "杨红艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议沙河口区委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=2ad1a06684c7455ead4adf92b504fb71",
    },
    # 6. 陈锋 — 区委常委、区纪委书记/监委主任
    {
        "id": 6,
        "name": "陈锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共大连市沙河口区纪律检查委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 7. 于雷 — 副区长
    {
        "id": 7,
        "name": "于雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市沙河口区人民政府",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 8. 徐大明 — 副区长
    {
        "id": 8,
        "name": "徐大明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市沙河口区人民政府",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=18c4d2537a93491ab82ea2bc43d4b364",
    },
    # 9. 刘晖 — 副区长 (2026-07-03任命)
    {
        "id": 9,
        "name": "刘晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市沙河口区人民政府",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 10. 李婷 — 副区长 (2026-07-03任命)
    {
        "id": 10,
        "name": "李婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市沙河口区人民政府",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 11. 杨全红 — 区法院院长
    {
        "id": 11,
        "name": "杨全红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区法院院长",
        "current_org": "沙河口区人民法院",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 12. 金岩 — 区检察院检察长
    {
        "id": 12,
        "name": "金岩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区检察院检察长",
        "current_org": "沙河口区人民检察院",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 13. 蒋建平 — 区人大常委会副主任
    {
        "id": 13,
        "name": "蒋建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "沙河口区人民代表大会常务委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 14. 姜彦 — 区人大常委会副主任
    {
        "id": 14,
        "name": "姜彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "沙河口区人民代表大会常务委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 15. 辛斌 — 区人大常委会副主任
    {
        "id": 15,
        "name": "辛斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "沙河口区人民代表大会常务委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 16. 勾学勇 — 区人大常委会副主任
    {
        "id": 16,
        "name": "勾学勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "沙河口区人民代表大会常务委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
    },
    # 17. 戚斌 — 区政协副主席
    {
        "id": 17,
        "name": "戚斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议沙河口区委员会",
        "source": "http://www.dlshk.gov.cn/web/shk/information/detail?id=c3d3532629db43458b084a685f7acb72",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共大连市沙河口区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市委员会",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 2,
        "name": "大连市沙河口区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市人民政府",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 3,
        "name": "沙河口区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "大连市人大常委会",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议沙河口区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协大连市委员会",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 5,
        "name": "中共大连市沙河口区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共大连市纪律检查委员会",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 6,
        "name": "沙河口区人民法院",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市中级人民法院",
        "location": "辽宁省大连市沙河口区",
    },
    {
        "id": 7,
        "name": "沙河口区人民检察院",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市人民检察院",
        "location": "辽宁省大连市沙河口区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 姜茂生 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026年5月/6月", "end": "present",
     "rank": "正处级", "note": "此前担任沙河口区长; 2026年6月12日以区委书记身份主持警示教育会"},
    # 姜茂生 - 区长（前任职务）
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "未知", "end": "2026-05-19",
     "rank": "正处级", "note": "2026年5月19日区人大常委会接受姜茂生辞去区长职务"},
    # 滕毓磐 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2026-05-24", "end": "present",
     "rank": "正处级", "note": "2026年5月24日沙河口区十九届人大八次会议选举产生; 2026年7月6日以区长身份列席区人大常委会第34次会议"},

    # ── 区人大常委会 ──
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月6日主持区人大常委会第34次会议"},
    {"person_id": 13, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # ── 区政协 ──
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年6月12日出席警示教育会"},
    {"person_id": 17, "org_id": 4, "title": "区政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # ── 区纪委监委 ──
    {"person_id": 6, "org_id": 5, "title": "区委常委、区纪委书记、区监委主任", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年7月6日列席区人大常委会第34次会议"},

    # ── 区政府领导 ──
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年7月6日列席区人大常委会第34次会议"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年5月19日列席区人大常委会第33次会议"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "2026-07-03", "end": "present",
     "rank": "副处级", "note": "2026年7月3日区人大常委会第34次会议任命"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "2026-07-03", "end": "present",
     "rank": "副处级", "note": "2026年7月3日区人大常委会第34次会议任命"},

    # ── 法检两院 ──
    {"person_id": 11, "org_id": 6, "title": "区法院院长", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月6日列席区人大常委会第34次会议"},
    {"person_id": 12, "org_id": 7, "title": "区检察院检察长", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月6日列席区人大常委会第34次会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 姜茂生 <-> 滕毓磐: 党政主要领导搭档 & 区长职务交接
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "姜茂生由区长转任区委书记，滕毓磐接任区长",
     "overlap_org": "大连市沙河口区人民政府",
     "overlap_period": "2026年5月"},
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共大连市沙河口区委员会/大连市沙河口区人民政府",
     "overlap_period": "2026年6月起"},

    # 姜茂生 <-> 张洪运: 区委书记与人大主任
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区人大常委会主任工作搭档",
     "overlap_org": "中共大连市沙河口区委员会/沙河口区人大常委会",
     "overlap_period": "截至2026年7月"},

    # 姜茂生 <-> 杨红艳: 区委书记与政协主席
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区政协主席工作搭档",
     "overlap_org": "中共大连市沙河口区委员会/沙河口区政协",
     "overlap_period": "截至2026年7月"},

    # 姜茂生 <-> 陈锋: 区委书记与纪委书记
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委、纪委书记; 区委领导班子搭档",
     "overlap_org": "中共大连市沙河口区委员会",
     "overlap_period": "截至2026年7月"},

    # 滕毓磐 <-> 于雷: 区长与副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "大连市沙河口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 滕毓磐 <-> 徐大明: 区长与副区长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "大连市沙河口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 滕毓磐 <-> 刘晖: 区长与副区长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与新任副区长工作搭档",
     "overlap_org": "大连市沙河口区人民政府",
     "overlap_period": "2026年7月起"},

    # 滕毓磐 <-> 李婷: 区长与副区长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与新任副区长工作搭档",
     "overlap_org": "大连市沙河口区人民政府",
     "overlap_period": "2026年7月起"},

    # 姜茂生 <-> 于雷: 书记与副区长
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与副区长工作搭档（姜茂生曾任区长时于雷即任副区长）",
     "overlap_org": "中共大连市沙河口区委员会/大连市沙河口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张洪运 <-> 蒋建平: 人大主任与副主任
    {"person_a": 4, "person_b": 13, "type": "overlap",
     "context": "区人大常委会领导班子同事",
     "overlap_org": "沙河口区人民代表大会常务委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 4, "person_b": 14, "type": "overlap",
     "context": "区人大常委会领导班子同事",
     "overlap_org": "沙河口区人民代表大会常务委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 4, "person_b": 15, "type": "overlap",
     "context": "区人大常委会领导班子同事",
     "overlap_org": "沙河口区人民代表大会常务委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 4, "person_b": 16, "type": "overlap",
     "context": "区人大常委会领导班子同事",
     "overlap_org": "沙河口区人民代表大会常务委员会",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTRY
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "沙河口区警示教育会召开（确认姜茂生区委书记身份）",
            "url": "http://www.dlshk.gov.cn/web/shk/information/detail?id=2ad1a06684c7455ead4adf92b504fb71",
            "publisher": "沙河口区纪委监委/大连市沙河口区人民政府",
            "published_at": "2026-06-12",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记姜茂生主持会议并讲话，区长滕毓磐、区人大常委会主任张洪运、区政协主席杨红艳出席",
        },
        {
            "id": "S002",
            "title": "沙河口区第十九届人大常委会第三十四次会议（确认滕毓磐区长身份）",
            "url": "http://www.dlshk.gov.cn/web/shk/information/detail?id=bccc2cffc0b3410f8fa661ca2d78e49c",
            "publisher": "沙河口区人大办/大连市沙河口区人民政府",
            "published_at": "2026-07-06",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委副书记、区长滕毓磐列席; 任命刘晖、李婷为副区长",
        },
        {
            "id": "S003",
            "title": "沙河口区第十九届人大常委会第三十三次会议（确认姜茂生辞去区长职务）",
            "url": "http://www.dlshk.gov.cn/web/shk/information/detail?id=18c4d2537a93491ab82ea2bc43d4b364",
            "publisher": "沙河口区人大办/大连市沙河口区人民政府",
            "published_at": "2026-05-21",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "接受姜茂生辞去区长职务; 区十九届人大八次会议定于5月24日选举区长; 副区长徐大明列席",
        },
        {
            "id": "S004",
            "title": "沙河口区政协开展重点提案协商督办（确认戚斌政协副主席身份）",
            "url": "http://www.dlshk.gov.cn/web/shk/information/detail?id=c3d3532629db43458b084a685f7acb72",
            "publisher": "沙河口区政协办/大连市沙河口区人民政府",
            "published_at": "2026-06-02",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区政协副主席戚斌带队开展提案督办",
        },
        {
            "id": "S005",
            "title": "共青团沙河口区十五届三次全委会议",
            "url": "http://www.dlshk.gov.cn/web/shk/information/detail?id=43650218cacf4a88bb40d0fde3a2a07a",
            "publisher": "沙河口区团区委/大连市沙河口区人民政府",
            "published_at": "2026-05-09",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "提到一湾两核三园空间布局和现代化品质城区建设目标",
        },
    ]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON GENERATORS
# ══════════════════════════════════════════════════════════════════════════════


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"shahekouqu_{name}"

    # ── 姜茂生 (区委书记) ──
    if name == "姜茂生":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "大连市",
                "region": "沙河口区",
                "job": "区委书记",
                "task_id": "liaoning_沙河口区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "姜茂生",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "姜茂生_",
                    "name_birthplace": "姜茂生_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共大连市沙河口区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2026-05-19",
                    "org": "大连市沙河口区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "辽宁省大连市沙河口区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "2026年5月19日辞去区长职务",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
                {
                    "start": "2026年6月",
                    "end": "present",
                    "org": "中共大连市沙河口区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "辽宁省大连市沙河口区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替前任区委书记; 2026年6月12日以区委书记身份主持警示教育会",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共大连市沙河口区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省大连市沙河口区"},
                {"org_id": 2, "name": "大连市沙河口区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省大连市沙河口区"},
            ],
            "relationships": [
                {"person": "滕毓磐", "person_id": "shahekouqu_滕毓磐",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "姜茂生由区长转任区委书记，滕毓磐接任区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "2026年5月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S003"]},
                {"person": "滕毓磐", "person_id": "shahekouqu_滕毓磐",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共大连市沙河口区委员会/大连市沙河口区人民政府",
                 "overlap_period": "2026年6月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "张洪运", "person_id": "shahekouqu_张洪运",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区人大常委会主任工作搭档",
                 "overlap_org": "中共大连市沙河口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "杨红艳", "person_id": "shahekouqu_杨红艳",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区政协主席工作搭档",
                 "overlap_org": "中共大连市沙河口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "陈锋", "person_id": "shahekouqu_陈锋",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区委常委、纪委书记",
                 "overlap_org": "中共大连市沙河口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "于雷", "person_id": "shahekouqu_于雷",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与副区长（姜茂生任区长时于雷即任副区长）",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2026年6月",
                    "domain": "discipline",
                    "achievement_or_event": "主持沙河口区警示教育会，强调树立正确政绩观",
                    "role_in_event": "区委书记，主持会议并讲话",
                    "measurable_outcome": "部署五项重点纠治工作，强调风腐同治",
                    "location": "大连市沙河口区",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2026年5月前",
                    "domain": "other",
                    "achievement_or_event": "主持区政府全面工作",
                    "role_in_event": "区长",
                    "measurable_outcome": "政府工作报告、债务管理等",
                    "location": "大连市沙河口区",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["大连市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度; 从区长转任区委书记属常见干部晋升路径",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "discipline_oriented",
                        "evidence": "主持警示教育会强调政绩观、风腐同治、营商环境整治",
                        "confidence": "plausible",
                        "source_ids": ["S001"],
                    }
                ],
                "speech_themes": [
                    "树立正确政绩观",
                    "坚持以人民为中心",
                    "风腐同治",
                    "新官必理旧账",
                ],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "姜茂生的完整履历（出生年月、籍贯、教育背景、任区长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "姜茂生的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["姜茂生 简历 大连 沙河口区", "姜茂生 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "姜茂生何时开始担任沙河口区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["姜茂生 任 沙河口区 区长", "姜茂生 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "姜茂生的前任区委书记是谁？现在何处？",
                    "why_it_matters": "完成前任-继任链条和跨区人事交流网络",
                    "suggested_queries": ["沙河口区 前任 区委书记", "大连 沙河口区 区委书记 任免"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "姜茂生的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["姜茂生 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 滕毓磐 (区长) ──
    if name == "滕毓磐":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "大连市",
                "region": "沙河口区",
                "job": "区长",
                "task_id": "liaoning_沙河口区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "滕毓磐",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "滕毓磐_",
                    "name_birthplace": "滕毓磐_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "大连市沙河口区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002", "S003"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2026年5月",
                    "org": "未知",
                    "title": "未知（此前职务）",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "任区长前的职务和经历公开信息未找到",
                    "confidence": "unverified",
                    "source_ids": [],
                },
                {
                    "start": "2026-05-24",
                    "end": "present",
                    "org": "大连市沙河口区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "辽宁省大连市沙河口区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年5月24日沙河口区十九届人大八次会议选举产生; 2026年7月6日以区长身份列席区人大常委会第34次会议",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S003"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "大连市沙河口区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省大连市沙河口区"},
            ],
            "relationships": [
                {"person": "姜茂生", "person_id": "shahekouqu_姜茂生",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "滕毓磐接替姜茂生担任沙河口区区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "2026年5月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002", "S003"]},
                {"person": "姜茂生", "person_id": "shahekouqu_姜茂生",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共大连市沙河口区委员会/大连市沙河口区人民政府",
                 "overlap_period": "2026年6月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "于雷", "person_id": "shahekouqu_于雷",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "徐大明", "person_id": "shahekouqu_徐大明",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "刘晖", "person_id": "shahekouqu_刘晖",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与新任副区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "2026年7月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "李婷", "person_id": "shahekouqu_李婷",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与新任副区长",
                 "overlap_org": "大连市沙河口区人民政府",
                 "overlap_period": "2026年7月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "other",
                    "achievement_or_event": "列席区人大常委会第34次会议，参与政府债务管理和公共文化服务讨论",
                    "role_in_event": "区长，列席会议",
                    "measurable_outcome": "针对债务风险管控、公共文化服务体系建设等提出工作要求",
                    "location": "大连市沙河口区",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议为主，暂不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "滕毓磐的完整履历（出生年月、籍贯、教育背景、任区长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "滕毓磐的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["滕毓磐 简历 大连 沙河口区", "滕毓磐 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "滕毓磐任区长前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["滕毓磐 任 沙河口区 区长 之前", "滕毓磐 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "滕毓磐的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["滕毓磐 工作 经历"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "滕毓磐此前是否在大连其他区县任职？",
                    "why_it_matters": "评估跨区交流网络",
                    "suggested_queries": ["滕毓磐 大连 任职"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    os.makedirs(PERSONS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    person_configs = [
        ("区委书记", "姜茂生"),
        ("区长", "滕毓磐"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-辽宁省-大连市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
