#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 西安区 (Xi'an District), 辽源市, 吉林省.

Level: 市辖区
Province: 吉林省
Parent city: 辽源市
Targets: 区委书记 (Party Secretary: 孙琥峰), 区长 (Mayor: 隋立宁)
Task ID: jilin_西安区

Research date: 2026-07-25
Official source: http://www.lyxa.gov.cn/ (辽源市西安区人民政府)

Current status (as of 2026-07-25, verified via 西安区人民政府 website):
- 区委书记: 孙琥峰 (男，汉族，曾任西安区区长，2025年底/2026年初转任区委书记)
- 区长: 隋立宁 (男，汉族，1981年3月生，研究生，曾任区委常委、常务副区长，2025年12月任代区长)
- Full government leadership roster confirmed on district website (区政府领导页面)
- 区委领导班子详细名册暂未在官网找到独立页面

Leadership roster sourced from:
  - http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/sln/ (隋立宁)
  - http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wxd/ (王晓东)
  - http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/thw/ (谭海文)
  - http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wjl/ (王军亮)
  - http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wyl/ (吴雨龙)

Confidence notes:
  孙琥峰 identity as 区委书记 confirmed via May 2026 news article on district website.
  隋立宁 identity confirmed via official government bio page (1981年生, 研究生, 中共党员).
  Full career histories before current roles not publicly available.
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited or timed out during this investigation.
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "辽源市西安区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 孙琥峰 — 区委书记 (former 区长)
    {
        "id": 1,
        "name": "孙琥峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西安区委员会",
        "source": "http://www.lyxa.gov.cn/xxgk/zwyw/jrxa/2026/202605/t20260526_738906.html",
    },
    # 2. 隋立宁 — 区委副书记、区长
    {
        "id": 2,
        "name": "隋立宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "西安区人民政府",
        "source": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/sln/",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 王晓东 — 区委常委、副区长
    {
        "id": 3,
        "name": "王晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "西安区人民政府",
        "source": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wxd/",
    },
    # 4. 谭海文 — 副区长
    {
        "id": 4,
        "name": "谭海文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安区人民政府",
        "source": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/thw/",
    },
    # 5. 王军亮 — 副区长、仙城公安分局局长
    {
        "id": 5,
        "name": "王军亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、仙城公安分局局长",
        "current_org": "西安区人民政府",
        "source": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wjl/",
    },
    # 6. 吴雨龙 — 副区长
    {
        "id": 6,
        "name": "吴雨龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "西安区人民政府",
        "source": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wyl/",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 7. 张立毅 — 前任区委书记
    {
        "id": 7,
        "name": "张立毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共西安区委员会（已离任）",
        "source": "http://www.lyxa.gov.cn/xxgk/zwgkzdlyxx/zdjsxm/202411/t20241105_697979.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共西安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共辽源市委员会",
        "location": "吉林省辽源市西安区",
    },
    {
        "id": 2,
        "name": "西安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "辽源市人民政府",
        "location": "吉林省辽源市西安区",
    },
    {
        "id": 3,
        "name": "西安区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "辽源市人大常委会",
        "location": "吉林省辽源市西安区",
    },
    {
        "id": 4,
        "name": "政协西安区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协辽源市委员会",
        "location": "吉林省辽源市西安区",
    },
    {
        "id": 5,
        "name": "西安区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共辽源市纪律检查委员会",
        "location": "吉林省辽源市西安区",
    },
    {
        "id": 6,
        "name": "辽源市公安局仙城分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "西安区人民政府",
        "location": "吉林省辽源市西安区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 孙琥峰 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026年初", "end": "present",
     "rank": "正处级", "note": "此前担任西安区区长; 2026年5月26日以区委书记身份公开调研"},
    # 孙琥峰 - 区长（前任职务）
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "", "end": "2025年底",
     "rank": "正处级", "note": "2025年12月23日仍以区长身份主持区政府常务会议"},
    # 隋立宁 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025年12月", "end": "present",
     "rank": "正处级", "note": "2025年12月25日在区十届人大五次会议上以代区长身份作政府工作报告; 此前曾任区委常委、常务副区长"},
    # 隋立宁 - 常务副区长（前任职务）
    {"person_id": 2, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "2025年12月",
     "rank": "副处级", "note": "2025年6月19日区政府第五次常务会议上以区委常委、常务副区长身份出席"},

    # ── 区政府领导 ──
    # 王晓东 - 区委常委、副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "协助区长分管区政府办公室、发改局、财政局、应急管理局、人社局、机关事务管理局等多个部门"},
    # 谭海文 - 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管区农业农村局、河长制办公室; 暂代分管区教育局、政务服务和数字化局等多个部门"},
    # 王军亮 - 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管区司法局、退役军人事务局、信访局、辽源市公安局西安分局"},
    {"person_id": 5, "org_id": 6, "title": "仙城公安分局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "兼任仙城公安分局局长"},
    # 吴雨龙 - 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管区民政局、住建局、城管局、环境卫生管理中心、矿区房屋管理处等; 联系各街道办事处"},

    # ── 前任领导 ──
    # 张立毅 - 前任区委书记
    {"person_id": 7, "org_id": 1, "title": "区委书记", "start": "", "end": "2025年底前",
     "rank": "正处级", "note": "2024年11月5日仍以区委书记身份调研重点项目建设; 之后由孙琥峰接任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 孙琥峰 <-> 隋立宁: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 孙琥峰曾任区长后转任书记，隋立宁接任区长",
     "overlap_org": "中共西安区委员会/西安区人民政府",
     "overlap_period": "2026年起"},

    # 孙琥峰 <-> 隋立宁: 前任与继任（区长职务交接）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "孙琥峰由区长晋升区委书记，隋立宁由常务副区长接任区长",
     "overlap_org": "西安区人民政府",
     "overlap_period": "2025年底-2026年初"},

    # 孙琥峰 <-> 王晓东: 书记与政府副职
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长; 区委领导班子搭档",
     "overlap_org": "中共西安区委员会/西安区人民政府",
     "overlap_period": "截至2026年7月"},

    # 隋立宁 <-> 王晓东: 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长; 政府领导班子搭档",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},

    # 隋立宁 <-> 谭海文: 区长与副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},

    # 隋立宁 <-> 王军亮: 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},

    # 隋立宁 <-> 吴雨龙: 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},

    # 孙琥峰 <-> 张立毅: 前任与继任（区委书记）
    {"person_a": 1, "person_b": 7, "type": "predecessor_successor",
     "context": "孙琥峰接替张立毅任西安区区委书记",
     "overlap_org": "中共西安区委员会",
     "overlap_period": "2025年底-2026年初"},

    # 隋立宁 <-> 孙琥峰: 常务副区长与区长（前任搭档）
    {"person_a": 2, "person_b": 1, "type": "superior_subordinate",
     "context": "隋立宁任常务副区长时曾作为孙琥峰（时任区长）的副手",
     "overlap_org": "西安区人民政府",
     "overlap_period": "至2025年底"},

    # 副区长之间的联系（政府班子成员）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "西安区人民政府",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "西安区人民政府官网-区政府领导-隋立宁",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/sln/",
            "publisher": "辽源市西安区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "隋立宁: 男，汉族，1981年3月生，研究生，中共党员，区委副书记、区长、区政府党组书记",
        },
        {
            "id": "S002",
            "title": "西安区人民政府官网-区政府领导-王晓东",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wxd/",
            "publisher": "辽源市西安区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王晓东: 男，汉族，1974年12月生，大学学历，中共党员，区委常委、副区长",
        },
        {
            "id": "S003",
            "title": "西安区人民政府官网-区政府领导-谭海文",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/thw/",
            "publisher": "辽源市西安区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "谭海文: 男，汉族，1973年12月生，大学学历，中共党员，副区长",
        },
        {
            "id": "S004",
            "title": "西安区人民政府官网-区政府领导-王军亮",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wjl/",
            "publisher": "辽源市西安区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王军亮: 男，汉族，1975年4月生，大学学历，中共党员，副区长、仙城公安分局局长",
        },
        {
            "id": "S005",
            "title": "西安区人民政府官网-区政府领导-吴雨龙",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/wyl/",
            "publisher": "辽源市西安区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "吴雨龙: 男，汉族，1986年11月生，大学学历，中共党员，副区长",
        },
        {
            "id": "S006",
            "title": "西安区人民政府-政务新闻-区委书记孙琥峰调研群腐集中整治工作",
            "url": "http://www.lyxa.gov.cn/xxgk/zwyw/jrxa/2026/202605/t20260526_738906.html",
            "publisher": "辽源市西安区人民政府",
            "published_at": "2026-05-26",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认孙琥峰为西安区区委书记（截至2026年5月）",
        },
        {
            "id": "S007",
            "title": "西安区人民政府-政务新闻-区长孙琥峰主持区政府常务会议",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/ldjh/202512/t20251223_728379.html",
            "publisher": "辽源市西安区人民政府",
            "published_at": "2025-12-23",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认孙琥峰在2025年12月仍以区长身份主持会议; 隋立宁以区委常委、常务副区长身份出席",
        },
        {
            "id": "S008",
            "title": "西安区人民政府-政府工作报告-2025年西安区人民政府工作报告",
            "url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/gzbg/202603/t20260313_733119.html",
            "publisher": "辽源市西安区人民政府",
            "published_at": "2026-03-13",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "隋立宁以代区长身份在2025年12月25日区人大会议上作政府工作报告",
        },
        {
            "id": "S009",
            "title": "西安区人民政府-政务新闻-区委书记张立毅调研重点项目建设",
            "url": "http://www.lyxa.gov.cn/xxgk/zwgkzdlyxx/zdjsxm/202411/t20241105_697979.html",
            "publisher": "辽源市西安区人民政府",
            "published_at": "2024-11-05",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张立毅为西安区前任区委书记（截至2024年11月）",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"xianqu_{name}"

    # ── 孙琥峰 (区委书记) ──
    if name == "孙琥峰":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "西安区",
                "job": "区委书记",
                "task_id": "jilin_西安区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "孙琥峰",
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
                    "name_birth": "孙琥峰_",
                    "name_birthplace": "孙琥峰_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共西安区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S006"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2025年底",
                    "org": "西安区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "吉林省辽源市西安区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "2025年12月23日仍以区长身份主持区政府常务会议",
                    "confidence": "confirmed",
                    "source_ids": ["S007"],
                },
                {
                    "start": "2026年初",
                    "end": "present",
                    "org": "中共西安区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "吉林省辽源市西安区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替张立毅任西安区区委书记; 2026年5月26日公开报道以区委书记身份调研",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共西安区委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省辽源市西安区"},
                {"org_id": 2, "name": "西安区人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省辽源市西安区"},
            ],
            "relationships": [
                {"person": "隋立宁", "person_id": "xianqu_隋立宁",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "孙琥峰由区长晋升区委书记，隋立宁由常务副区长接任区长",
                 "overlap_org": "西安区人民政府/中共西安区委员会",
                 "overlap_period": "2025年底-2026年初",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006", "S007", "S008"]},
                {"person": "隋立宁", "person_id": "xianqu_隋立宁",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共西安区委员会/西安区人民政府",
                 "overlap_period": "2026年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006"]},
                {"person": "张立毅", "person_id": "xianqu_张立毅",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "接替张立毅担任西安区区委书记",
                 "overlap_org": "中共西安区委员会",
                 "overlap_period": "2025年底-2026年初",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006", "S009"]},
                {"person": "王晓东", "person_id": "xianqu_王晓东",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区委常委、副区长",
                 "overlap_org": "中共西安区委员会",
                 "overlap_period": "2026年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2026年5月",
                    "domain": "discipline",
                    "achievement_or_event": "调研群众身边不正之风和腐败问题集中整治工作",
                    "role_in_event": "区委书记，带队调研",
                    "measurable_outcome": "实地查看社会福利服务中心、社区卫生服务中心、信访局和乡村",
                    "location": "辽源市西安区",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["辽源市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度; 从区长晋升区委书记属常见干部晋升路径",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "discipline_oriented",
                        "evidence": "着重调研群众身边不正之风和腐败问题整治，强调民生福祉和基层治理",
                        "confidence": "plausible",
                        "source_ids": ["S006"],
                    }
                ],
                "speech_themes": [
                    "坚持以人民为中心", "关注民生领域", "严抓党风廉政"
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
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "孙琥峰的完整履历（出生年月、籍贯、教育背景、任区长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "孙琥峰的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["孙琥峰 简历 辽源 西安区", "孙琥峰 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "孙琥峰何时开始担任西安区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["孙琥峰 任 西安区 区长", "孙琥峰 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "孙琥峰的具体何时由区长转任区委书记？",
                    "why_it_matters": "确认具体交接时间节点",
                    "suggested_queries": ["孙琥峰 任区委书记", "西安区 区委书记 任免"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "孙琥峰的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["孙琥峰 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 隋立宁 (区长) ──
    if name == "隋立宁":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "西安区",
                "job": "区长",
                "task_id": "jilin_西安区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "隋立宁",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1981年3月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "研究生",
                     "study_type": "unknown", "source_ids": ["S001"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "隋立宁_198103",
                    "name_birthplace": "隋立宁_",
                    "official_profile_url": "http://www.lyxa.gov.cn/xxgk/zwxxgkfl/zfld/qzfld/sln/",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "西安区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S008"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2025年12月",
                    "org": "西安区人民政府",
                    "title": "区委常委、常务副区长",
                    "level": "副处级",
                    "location": "吉林省辽源市西安区",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "2025年6月19日曾以区委常委、常务副区长身份出席区政府常务会议",
                    "confidence": "confirmed",
                    "source_ids": ["S007"],
                },
                {
                    "start": "2025年12月",
                    "end": "present",
                    "org": "西安区人民政府",
                    "title": "区长（代区长）",
                    "level": "正处级",
                    "location": "吉林省辽源市西安区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年12月25日在区十届人大五次会议上以代区长身份作政府工作报告; 2026年4月22日以区长身份主持召开区政府常务会议",
                    "confidence": "confirmed",
                    "source_ids": ["S008", "S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "西安区人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省辽源市西安区"},
            ],
            "relationships": [
                {"person": "孙琥峰", "person_id": "xianqu_孙琥峰",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "隋立宁接替孙琥峰担任西安区区长; 此前为孙琥峰副手（常务副区长）",
                 "overlap_org": "西安区人民政府",
                 "overlap_period": "至2025年底",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S007", "S008"]},
                {"person": "孙琥峰", "person_id": "xianqu_孙琥峰",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共西安区委员会/西安区人民政府",
                 "overlap_period": "2026年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006"]},
                {"person": "王晓东", "person_id": "xianqu_王晓东",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与区委常委、副区长",
                 "overlap_org": "西安区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "谭海文", "person_id": "xianqu_谭海文",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "西安区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "王军亮", "person_id": "xianqu_王军亮",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "西安区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
                {"person": "吴雨龙", "person_id": "xianqu_吴雨龙",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "西安区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S005"]},
            ],
            "governance_record": [
                {
                    "period": "2026年3月",
                    "domain": "other",
                    "achievement_or_event": "作2025年西安区人民政府工作报告，总结十四五时期工作",
                    "role_in_event": "代区长，作报告",
                    "measurable_outcome": "十四五期间地区生产总值年均增长5.02%，固定资产投资年均增长19.89%",
                    "location": "辽源市西安区",
                    "confidence": "confirmed",
                    "source_ids": ["S008"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government"],
                "geographic_pattern": ["辽源市"],
                "promotion_velocity": {
                    "summary": "从常务副区长晋升区长属正常晋升节奏",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议和报告为主，暂不足以判断工作风格",
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
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "完整履历：隋立宁任常务副区长前的教育背景（具体院校/专业）和全部早期任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "隋立宁的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["隋立宁 简历 西安区", "隋立宁 辽源"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "隋立宁何时开始担任西安区常务副区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["隋立宁 任 常务副区长", "隋立宁 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "隋立宁的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["隋立宁 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
        ("区委书记", "孙琥峰"),
        ("区长", "隋立宁"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-吉林省-辽源市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
