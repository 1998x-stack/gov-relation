#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 江源区, 白山市, 吉林省.

Level: 市辖区
Province: 吉林省
Parent city: 白山市
Targets: 区委书记 (Party Secretary: 潘国强), 区长 (Mayor: 王文江)
Task ID: jilin_江源区

Research date: 2026-07-25
Official source: http://www.jiangyuan.gov.cn/ (白山市江源区人民政府 — unreachable: timed out)

Current status (as of 2026-07-25, via Baidu search results and news articles):
- 区委书记: 潘国强 (男，汉族，1980年5月生，2003年7月参加工作，2005年9月入党)
  - Appointed as 区委书记 around March 2025 (previously served as 区长)
  - Also holds the position of 白山市副市长
  - Predecessor: 李江波 (left 江源区 around early 2025, moved to 吉林省国资公司)
- 区长: 王文江 (男，汉族，1981年7月生，研究生学历，中共党员)
  - Appointed as 区长候选人 in March 2025, later confirmed as 区长
  - Previously: 白山市文化广播电视和旅游局党组书记、局长, the 体育局局长, the 文物局局长
  - Previously: 吉林省商务厅外国投资服务处副处长, 挂职抚松县委常委、副县长
- Predecessor as 区长: 潘国强 (moved up to 区委书记)
- Predecessor as 区委书记: 李江波 (1974年4月生，吉林白山人，在职研究生; moved to 吉林省国资公司)

Known leadership roster (partial, from 2024-07 meeting notice on 江源区人民政府):
  - 王明明: 区委常委、常务副区长
  - 李继龙: 区委常委、副区长
  - 张大镇: 区委常委、统战部部长, 政协党组副书记, 砟子镇党委书记
  - 张国辉: 副区长、公安局局长
  - 李祖春: 副区长
  - 楚绪... (incomplete)
  - 谢洪峰: 区委副书记 (2025年报道)
  - 郑体玲: 区委常委、组织部部长 (2023年报道)
  - 谢洪峰: 区委常委、纪委书记 (2023年报道, later became 区委副书记)

Confidence notes:
  - 潘国强 identity confirmed via Baidu Baike (1980年生, 吉林师范大学毕业) and "汲古新知" article
  - 王文江 identity confirmed via Baidu Baike and official government site snippet
  - 李江波 identity confirmed via Baidu Baike (1974年生，吉林白山，在职研究生)
  - Government site (jiangyuan.gov.cn) timed out — all open
  - Baidu Baike returned HTTP 403 on direct access
  - Full career histories beyond current/previous roles not publicly available
  - All current-role claims labeled per evidence standard in source_register
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

SLUG = "江源区"

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

    # 1. 潘国强 — 区委书记 (former 区长)
    {
        "id": 1,
        "name": "潘国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "education": "吉林师范大学",
        "party_join": "中共党员",
        "work_start": "2003年7月",
        "current_post": "区委书记、白山市副市长",
        "current_org": "中共江源区委员会",
        "source": "https://baike.baidu.com/item/潘国强 (Baidu Baike, 403 on direct fetch, confirmed via search snippet)",
    },
    # 2. 王文江 — 区委副书记、区长
    {
        "id": 2,
        "name": "王文江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1998年12月",
        "current_post": "区长",
        "current_org": "江源区人民政府",
        "source": "https://baike.baidu.com/item/王文江 (Baidu Baike snippet; 江源区人民政府官网领导简介)",
    },

    # ════════════════════════════════════════
    # 区委/区政府领导 (Known Roster)
    # ════════════════════════════════════════

    # 3. 谢洪峰 — 区委副书记 (formerly 纪委书记)
    {
        "id": 3,
        "name": "谢洪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共江源区委员会",
        "source": "江源区人民政府网站新闻报道 (2025年2月25日报道)",
    },
    # 4. 王明明 — 区委常委、常务副区长
    {
        "id": 4,
        "name": "王明明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "江源区人民政府",
        "source": "江源区人民政府2024年7月26日领导小组成员名单",
    },
    # 5. 李继龙 — 区委常委、副区长
    {
        "id": 5,
        "name": "李继龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "江源区人民政府",
        "source": "江源区人民政府2024年7月26日领导小组成员名单",
    },
    # 6. 张大镇 — 区委常委、统战部部长
    {
        "id": 6,
        "name": "张大镇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长、政协党组副书记、砟子镇党委书记",
        "current_org": "中共江源区委员会",
        "source": "江源区人民政府2024年7月26日领导小组成员名单",
    },
    # 7. 张国辉 — 副区长、公安局局长
    {
        "id": 7,
        "name": "张国辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安局局长",
        "current_org": "江源区人民政府",
        "source": "江源区人民政府2024年7月26日领导小组成员名单",
    },
    # 8. 李祖春 — 副区长
    {
        "id": 8,
        "name": "李祖春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "江源区人民政府",
        "source": "江源区人民政府2024年7月26日领导小组成员名单; 2025年2月25日报道",
    },
    # 9. 郑体玲 — 区委常委、组织部部长 (2023年)
    {
        "id": 9,
        "name": "郑体玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共江源区委员会",
        "source": "江源区人民政府2023年11月报道",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 10. 李江波 — 前任区委书记
    {
        "id": 10,
        "name": "李江波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年4月",
        "birthplace": "吉林白山",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吉林省国资公司党委书记、董事长",
        "current_org": "吉林省国资公司",
        "source": "Baidu Baike (李江波); 汲古新知 article",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共江源区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共白山市委员会",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 2,
        "name": "江源区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "白山市人民政府",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 3,
        "name": "江源区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "白山市人大常委会",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 4,
        "name": "政协江源区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协白山市委员会",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 5,
        "name": "江源区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共白山市纪律检查委员会",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 6,
        "name": "白山市公安局江源分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "江源区人民政府",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 7,
        "name": "江源区委统战部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共江源区委员会",
        "location": "吉林省白山市江源区",
    },
    {
        "id": 8,
        "name": "吉林省国资公司",
        "type": "国企",
        "level": "省属",
        "parent": "吉林省人民政府",
        "location": "吉林省长春市",
    },
    {
        "id": 9,
        "name": "白山市文化广播电视和旅游局",
        "type": "政府",
        "level": "地市级",
        "parent": "白山市人民政府",
        "location": "吉林省白山市",
    },
    {
        "id": 10,
        "name": "吉林省商务厅",
        "type": "政府",
        "level": "省级",
        "parent": "吉林省人民政府",
        "location": "吉林省长春市",
    },
    {
        "id": 11,
        "name": "中共浑江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共白山市委员会",
        "location": "吉林省白山市浑江区",
    },
    {
        "id": 12,
        "name": "浑江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "白山市人民政府",
        "location": "吉林省白山市浑江区",
    },
    {
        "id": 13,
        "name": "中共白山市委组织部",
        "type": "党委",
        "level": "地市级",
        "parent": "中共白山市委员会",
        "location": "吉林省白山市",
    },
    {
        "id": 14,
        "name": "抚松县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "白山市人民政府",
        "location": "吉林省白山市抚松县",
    },
    {
        "id": 15,
        "name": "中共抚松县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共白山市委员会",
        "location": "吉林省白山市抚松县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership (Current) ──
    # 潘国强 - 区委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025年3月", "end": "present",
     "rank": "正处级", "note": "2025年3月8日'江源发布'消息显示已任区委书记"},
    # 潘国强 also 白山市副市长
    {"person_id": 1, "org_id": 2, "title": "白山市副市长", "start": "", "end": "present",
     "rank": "副厅级", "note": "兼任白山市副市长; Baidu Baike记载"},
    # 潘国强 - 前区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2021年7月", "end": "2025年3月",
     "rank": "正处级", "note": "2021年7月任代区长，11月去代转正; 2025年1月仍以区长身份主持区政府常务会议"},
    # 潘国强 - 浑江区委常委、副区长
    {"person_id": 1, "org_id": 12, "title": "区委常委、副区长", "start": "2019年4月", "end": "2021年7月",
     "rank": "副处级", "note": "2019年4月调任浑江区委常委、副区长"},
    # 潘国强 - 江源区委常委、组织部部长
    {"person_id": 1, "org_id": 1, "title": "区委常委、组织部部长", "start": "2016年8月", "end": "2019年4月",
     "rank": "副处级", "note": "2016年8月任江源区委常委、组织部部长"},
    # 潘国强 - 白山市委组织部党政干部科
    {"person_id": 1, "org_id": 13, "title": "党政干部科副科长（主持工作）/科长", "start": "2016年前", "end": "2016年8月",
     "rank": "乡科级", "note": "曾任白山市委组织部党政干部科副科长、副科长（主持工作）、科长; 具体时间未明确"},

    # 王文江 - 区长 (current)
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025年3月", "end": "present",
     "rank": "正处级", "note": "2025年3月任区长候选人; 后任区委副书记、区政府党组书记、区长"},
    # 王文江 - 白山市文化广播电视和旅游局局长
    {"person_id": 2, "org_id": 9, "title": "党组书记、局长", "start": "2023年", "end": "2025年2月",
     "rank": "正处级", "note": "同时兼任市体育局局长、市文物局局长"},
    # 王文江 - 挂职抚松县委常委、副县长
    {"person_id": 2, "org_id": 14, "title": "县委常委、副县长（挂职）", "start": "", "end": "2023年",
     "rank": "副处级", "note": "挂职担任抚松县委常委、副县长"},
    # 王文江 - 吉林省商务厅
    {"person_id": 2, "org_id": 10, "title": "外国投资服务处副处长", "start": "", "end": "",
     "rank": "副处级", "note": "曾任吉林省商务厅外国投资服务处副处长"},

    # ── 区委领导 ──
    # 谢洪峰 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "2025年2月25日以区委副书记身份参加调研"},
    # 谢洪峰 - 区纪委书记（前任）
    {"person_id": 3, "org_id": 5, "title": "区委常委、纪委书记", "start": "", "end": "",
     "rank": "副处级", "note": "2023年11月报道中以区委常委、纪委书记身份出席会议"},
    # 王明明 - 区委常委、常务副区长
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2024年7月26日领导小组成员名单"},
    # 李继龙 - 区委常委、副区长
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2024年7月26日领导小组成员名单"},
    # 张大镇 - 区委常委、统战部部长
    {"person_id": 6, "org_id": 7, "title": "区委常委、统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "同时兼任区政协党组副书记、砟子镇党委书记、砟子镇人民武装部政治教导员"},
    # 郑体玲 - 区委常委、组织部部长
    {"person_id": 9, "org_id": 1, "title": "区委常委、组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "2023年11月报道中出席安全生产会议"},

    # ── 区政府领导 ──
    # 张国辉 - 副区长、公安局局长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任区公安局局长"},
    {"person_id": 7, "org_id": 6, "title": "区公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "兼任区公安局局长"},
    # 李祖春 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2024年7月及2025年2月新闻报道"},

    # ── 前任领导 ──
    # 李江波 - 前任区委书记
    {"person_id": 10, "org_id": 1, "title": "区委书记", "start": "", "end": "2025年初",
     "rank": "正处级", "note": "2024年7月26日仍以区委书记身份出现在领导小组名单; 后调任吉林省国资公司"},
    # 李江波 - 吉林省国资公司
    {"person_id": 10, "org_id": 8, "title": "党委书记、董事长", "start": "2025年初", "end": "present",
     "rank": "省属正职", "note": "接任吉林省国资公司党委书记、董事长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 潘国强 <-> 王文江: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共江源区委员会/江源区人民政府",
     "overlap_period": "2025年3月起"},

    # 潘国强 <-> 王文江: 前任与继任（区长职务交接）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "潘国强由区长晋升区委书记，王文江接任区长",
     "overlap_org": "江源区人民政府",
     "overlap_period": "2025年3月"},

    # 潘国强 <-> 李江波: 前任与继任（区委书记）
    {"person_a": 10, "person_b": 1, "type": "predecessor_successor",
     "context": "李江波调任吉林省国资公司，潘国强由区长升任区委书记",
     "overlap_org": "中共江源区委员会",
     "overlap_period": "2025年初-2025年3月"},

    # 潘国强 <-> 李江波: 同班子搭档
    {"person_a": 10, "person_b": 1, "type": "overlap",
     "context": "李江波任区委书记期间，潘国强任区长，多年党政搭档",
     "overlap_org": "中共江源区委员会/江源区人民政府",
     "overlap_period": "2021年7月-2025年初"},

    # 潘国强 <-> 谢洪峰: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "潘国强任区委书记，谢洪峰任区委副书记",
     "overlap_org": "中共江源区委员会",
     "overlap_period": "2025年起"},

    # 王文江 <-> 王明明 : 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "王文江任区长，王明明任常务副区长",
     "overlap_org": "江源区人民政府",
     "overlap_period": "2025年起"},

    # 王文江 <-> 抚松县任职: 来源地
    {"person_a": 2, "person_b": 0, "type": "overlap",
     "context": "王文江曾挂职抚松县委常委、副县长；江源区与抚松县同在白山市辖区内",
     "overlap_org": "白山市",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")

    # Write person JSONs
    from gov_relation.paths import PERSONS_DIR as CANONICAL_PERSONS_DIR

    # 潘国强 person JSON
    pan_json = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "吉林省",
            "city": "白山市",
            "region": "江源区",
            "job": "区委书记",
            "task_id": "jilin_江源区",
            "time_focus": "2016–2026"
        },
        "identity": {
            "person_id": "jiangyuan_潘国强",
            "name": "潘国强",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1980年5月",
            "birthplace": "",
            "native_place": "",
            "education": [
                {
                    "period": "1999–2003",
                    "institution": "吉林师范大学",
                    "major": "",
                    "degree": "大学",
                    "study_type": "full_time",
                    "source_ids": ["S001"]
                }
            ],
            "party_join": "2005年9月",
            "work_start": "2003年7月",
            "dedupe_keys": {
                "name_birth": "潘国强_198005",
                "name_birthplace": "潘国强_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区委书记、白山市副市长",
            "current_org": "中共江源区委员会",
            "administrative_rank": "副厅级（兼任白山市副市长）",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S003"]
        },
        "career_timeline": [
            {
                "start": "2016年前",
                "end": "2016年8月",
                "org": "白山市委组织部",
                "title": "党政干部科副科长/科长",
                "level": "乡科级",
                "location": "吉林省白山市",
                "system": "organization",
                "rank": "乡科级",
                "is_key_promotion": False,
                "notes": "曾任白山市委组织部党政干部科副科长、副科长（主持工作）、科长",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "start": "2016年8月",
                "end": "2019年4月",
                "org": "中共江源区委员会",
                "title": "区委常委、组织部部长",
                "level": "副处级",
                "location": "吉林省白山市江源区",
                "system": "organization",
                "rank": "副处级",
                "is_key_promotion": True,
                "notes": "2016年8月任江源区委常委、组织部部长",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "start": "2019年4月",
                "end": "2021年7月",
                "org": "浑江区人民政府",
                "title": "区委常委、副区长",
                "level": "副处级",
                "location": "吉林省白山市浑江区",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "2019年4月调任浑江区委常委、副区长",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "start": "2021年7月",
                "end": "2025年3月",
                "org": "江源区人民政府",
                "title": "区长",
                "level": "正处级",
                "location": "吉林省白山市江源区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2021年7月任江源区委副书记、代区长，11月去代转正; 2025年1月仍以区长身份主持区政府常务会议",
                "confidence": "confirmed",
                "source_ids": ["S003", "S005"]
            },
            {
                "start": "2025年3月",
                "end": "present",
                "org": "中共江源区委员会",
                "title": "区委书记",
                "level": "正处级",
                "location": "吉林省白山市江源区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2025年3月8日'江源发布'消息显示已任区委书记; 同时兼任白山市副市长",
                "confidence": "confirmed",
                "source_ids": ["S003", "S004"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "李江波",
                "person_id": "jiangyuan_李江波",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "李江波为前任区委书记，潘国强接任; 此前两人在江源区党政班子搭档多年（书记+区长）",
                "overlap_org": "中共江源区委员会/江源区人民政府",
                "overlap_period": "2021年7月–2025年3月",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            },
            {
                "person": "王文江",
                "person_id": "jiangyuan_王文江",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "潘国强由区长升任书记，王文江接任区长; 现为党政主要领导搭档",
                "overlap_org": "江源区人民政府",
                "overlap_period": "2025年3月起",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["组织人事", "地方治理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["organization", "government", "party"],
            "geographic_pattern": ["白山市（江源区→浑江区→江源区）"],
            "promotion_velocity": {
                "summary": "2016年副处级（区委常委、组织部长），2021年正处级（区长），2025年兼任副厅级（副市长）。晋升节奏稳步较快。",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面纪律审查或处分记录",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "潘国强 — 百度百科",
                "url": "https://baike.baidu.com/item/潘国强",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Baidu Baike returned 403 on direct fetch; data extracted from search snippet"
            },
            {
                "id": "S003",
                "title": "潘国强任白山市江源区委书记",
                "url": "（汲古新知 2025年3月8日）",
                "publisher": "汲古新知",
                "published_at": "2025-03-08",
                "accessed_at": "2026-07-25",
                "source_type": "media",
                "reliability": "medium",
                "notes": "Contains full career timeline from 白山市委组织部 through 区委书记 appointment"
            },
            {
                "id": "S004",
                "title": "王文江已任白山市江源区区长候选人",
                "url": "（汲古新知 2025年3月8日）",
                "publisher": "汲古新知",
                "published_at": "2025-03-08",
                "accessed_at": "2026-07-25",
                "source_type": "media",
                "reliability": "medium",
                "notes": "Reports 潘国强 appointment as 区委书记 and 王文江 as 区长候选人"
            },
            {
                "id": "S005",
                "title": "白山市江源区人民政府2025年第1次常务会议",
                "url": "https://www.jiangyuan.gov.cn/",
                "publisher": "江源区人民政府",
                "published_at": "2025-02-10",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "潘国强仍以区长身份主持会议（2025年1月）"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "2003年大学毕业后至2016年间的早期履历细节（白山市委组织部期间的具体任职时间）"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "潘国强的出生地和籍贯？",
                "why_it_matters": "完善人物基本背景信息",
                "suggested_queries": ["潘国强 出生地 籍贯 吉林"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "medium",
                "question": "潘国强在白山市委组织部期间的具体任职时间和职务细节？",
                "why_it_matters": "早期履历不完整",
                "suggested_queries": ["潘国强 白山市委组织部 党政干部科 任职时间"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    wang_json = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "吉林省",
            "city": "白山市",
            "region": "江源区",
            "job": "区长",
            "task_id": "jilin_江源区",
            "time_focus": "2023–2026"
        },
        "identity": {
            "person_id": "jiangyuan_王文江",
            "name": "王文江",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1981年7月",
            "birthplace": "",
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "研究生",
                    "study_type": "unknown",
                    "source_ids": ["S011"]
                }
            ],
            "party_join": "2000年6月",
            "work_start": "1998年12月",
            "dedupe_keys": {
                "name_birth": "王文江_198107",
                "name_birthplace": "王文江_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "江源区人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S010", "S011"]
        },
        "career_timeline": [
            {
                "start": "1998年12月",
                "end": "未知",
                "org": "",
                "title": "参加工作",
                "level": "",
                "location": "",
                "system": "unknown",
                "rank": "",
                "is_key_promotion": False,
                "notes": "1998年12月参加工作; 2000年6月入党; 早期履历不详",
                "confidence": "unverified",
                "source_ids": ["S011"]
            },
            {
                "start": "未知",
                "end": "2023年前",
                "org": "吉林省商务厅",
                "title": "外国投资服务处副处长",
                "level": "副处级",
                "location": "吉林省长春市",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "曾任吉林省商务厅外国投资服务处副处长",
                "confidence": "confirmed",
                "source_ids": ["S004", "S009"]
            },
            {
                "start": "未知",
                "end": "2023年前",
                "org": "抚松县人民政府",
                "title": "县委常委、副县长（挂职）",
                "level": "副处级",
                "location": "吉林省白山市抚松县",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "挂职担任白山市抚松县委常委、副县长",
                "confidence": "confirmed",
                "source_ids": ["S004", "S009"]
            },
            {
                "start": "2023年",
                "end": "2025年2月",
                "org": "白山市文化广播电视和旅游局",
                "title": "党组书记、局长",
                "level": "正处级",
                "location": "吉林省白山市",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "同时兼任市体育局局长、市文物局局长",
                "confidence": "confirmed",
                "source_ids": ["S009"]
            },
            {
                "start": "2025年3月",
                "end": "present",
                "org": "江源区人民政府",
                "title": "区长",
                "level": "正处级",
                "location": "吉林省白山市江源区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2025年2月省管干部任前公示，3月任区长候选人，后任区委副书记、区政府党组书记、区长",
                "confidence": "confirmed",
                "source_ids": ["S004", "S009", "S010"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "潘国强",
                "person_id": "jiangyuan_潘国强",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "王文江接替潘国强任区长; 现为党政主要领导搭档",
                "overlap_org": "江源区人民政府",
                "overlap_period": "2025年3月起",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S004"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["商务/外资", "文化旅游"],
            "secondary_specializations": ["地方治理"],
            "career_pattern": "provincial_department_to_local",
            "systems_experience": ["government", "business_promotion"],
            "geographic_pattern": ["长春市（省商务厅）→白山市（抚松县→市直→江源区）"],
            "promotion_velocity": {
                "summary": "从省商务厅副处长到挂职副县长，到市直正职，再到区长。跨系统（省商务厅→地方文旅→县区政府）经历丰富。",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面纪律审查或处分记录",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S004",
                "title": "王文江已任白山市江源区区长候选人",
                "url": "（汲古新知 2025年3月8日）",
                "publisher": "汲古新知",
                "published_at": "2025-03-08",
                "accessed_at": "2026-07-25",
                "source_type": "media",
                "reliability": "medium",
                "notes": "Reports 王文江 as 区长候选人, career history"
            },
            {
                "id": "S009",
                "title": "吉林省省管干部任职前公示公告",
                "url": "（中国共产党新闻网 2025年3月3日）",
                "publisher": "中国共产党新闻网",
                "published_at": "2025-03-03",
                "accessed_at": "2026-07-25",
                "source_type": "appointment_notice",
                "reliability": "high",
                "notes": "省管干部任前公示确认王文江拟提名为县（市、区）政府正职候选人; 确认其1981年7月生，研究生学历，时任白山市文旅局局长"
            },
            {
                "id": "S010",
                "title": "王文江 — 百度百科",
                "url": "https://baike.baidu.com/item/王文江",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Baidu Baike snippet confirms identity and current role"
            },
            {
                "id": "S011",
                "title": "江源区人民政府 — 区长领导简介",
                "url": "https://www.jiangyuan.gov.cn/ (区长页面)",
                "publisher": "江源区人民政府",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "Official bio page confirms 王文江 as 区长; site timed out on direct fetch, data from Baidu search snippet"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "1998年参加工作后至省商务厅任职前的早期履历（含教育背景、毕业院校、专业）"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "王文江的毕业院校和专业？",
                "why_it_matters": "教育背景信息缺失",
                "suggested_queries": ["王文江 研究生 毕业院校 专业"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "王文江的出生地和籍贯？",
                "why_it_matters": "完善人物基本背景信息",
                "suggested_queries": ["王文江 出生地 籍贯"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "medium",
                "question": "王文江1998年至省商务厅间的早期履历？",
                "why_it_matters": "早期职业经历空白",
                "suggested_queries": ["王文江 早期 工作 经历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    li_json = {
        "schema_version": "1.0",
        "generated_at": "2026-07-25",
        "investigation_scope": {
            "province": "吉林省",
            "city": "白山市",
            "region": "江源区",
            "job": "前任区委书记",
            "task_id": "jilin_江源区",
            "time_focus": "曾任江源区委书记"
        },
        "identity": {
            "person_id": "jiangyuan_李江波",
            "name": "李江波",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1974年4月",
            "birthplace": "吉林白山",
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": "在职研究生",
                    "study_type": "part_time",
                    "source_ids": ["S020"]
                }
            ],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "李江波_197404",
                "name_birthplace": "李江波_吉林白山",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "党委书记、董事长",
            "current_org": "吉林省国资公司",
            "administrative_rank": "省属正职",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S020"]
        },
        "career_timeline": [
            {
                "start": "未知",
                "end": "2025年初",
                "org": "中共江源区委员会",
                "title": "区委书记",
                "level": "正处级",
                "location": "吉林省白山市江源区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2024年7月仍以区委书记身份出现在领导小组名单; 2024年11月调研文物保护",
                "confidence": "confirmed",
                "source_ids": ["S006", "S007"]
            },
            {
                "start": "2025年初",
                "end": "present",
                "org": "吉林省国资公司",
                "title": "党委书记、董事长",
                "level": "省属正职",
                "location": "吉林省长春市",
                "system": "state_owned_enterprise",
                "rank": "省属正职",
                "is_key_promotion": True,
                "notes": "调任吉林省国资公司党委书记、董事长（省属国企）",
                "confidence": "confirmed",
                "source_ids": ["S003", "S020"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "潘国强",
                "person_id": "jiangyuan_潘国强",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "李江波调离后，潘国强接任区委书记; 此前李江波任书记、潘国强任区长搭档多年",
                "overlap_org": "中共江源区委员会/江源区人民政府",
                "overlap_period": "2021年7月–2025年初",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S003"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方治理"],
            "secondary_specializations": ["国企管理"],
            "career_pattern": "local_to_soe",
            "systems_experience": ["party", "state_owned_enterprise"],
            "geographic_pattern": ["白山市（江源区）→长春市（省属国企）"],
            "promotion_velocity": {
                "summary": "从县级区委书记晋升为省属国企正职（省国资公司党委书记、董事长），属跨系统晋升。",
                "notable_fast_promotions": ["江源区委书记 → 吉林省国资公司党委书记、董事长"]
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现负面纪律审查或处分记录",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S003",
                "title": "潘国强任白山市江源区委书记",
                "url": "（汲古新知 2025年3月8日）",
                "publisher": "汲古新知",
                "published_at": "2025-03-08",
                "accessed_at": "2026-07-25",
                "source_type": "media",
                "reliability": "medium",
                "notes": "提到李江波已任吉林省国资公司党委书记、董事长"
            },
            {
                "id": "S006",
                "title": "江源区委召开2024年第4次常委(扩大)会议",
                "url": "",
                "publisher": "微信公众平台",
                "published_at": "2024-03-21",
                "accessed_at": "2026-07-25",
                "source_type": "media",
                "reliability": "medium",
                "notes": "李江波以区委书记身份主持会议"
            },
            {
                "id": "S007",
                "title": "江源区人民政府 — 2024年7月26日领导小组成员名单",
                "url": "https://www.jiangyuan.gov.cn/",
                "publisher": "江源区人民政府",
                "published_at": "2024-07-26",
                "accessed_at": "2026-07-25",
                "source_type": "official",
                "reliability": "high",
                "notes": "包含李江波（组长: 区委书记）在内的领导小组成员名单"
            },
            {
                "id": "S020",
                "title": "李江波 — 百度百科",
                "url": "https://baike.baidu.com/item/李江波",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "确认李江波1974年4月生，吉林白山人，汉族，中共党员，在职研究生; 现任吉林省国资公司党委书记、董事长（Baidu Baike snippet）"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "李江波的完整履历（何时开始任职江源区，此前历任职务）"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "李江波的完整履历（何时开始任江源区委书记，此前历任职务）",
                "why_it_matters": "缺少关键履历信息",
                "suggested_queries": ["李江波 江源区 任前公示 履历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }

    # Write person JSON files
    for fname, data in [
        (f"{TODAY}-吉林省-白山市-区委书记-潘国强.json", pan_json),
        (f"{TODAY}-吉林省-白山市-区长-王文江.json", wang_json),
        (f"{TODAY}-吉林省-白山市-前任区委书记-李江波.json", li_json),
    ]:
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {fpath}")

    print(f"\nDone. Files in {_STAGING_DIR}:")
    for f in sorted(_STAGING_DIR.glob("*")):
        print(f"  {f.name} ({f.stat().st_size} bytes)")
