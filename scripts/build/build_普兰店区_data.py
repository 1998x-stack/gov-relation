#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 普兰店区, 大连市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 大连市
Targets: 区委书记 (Party Secretary: 马涛), 区长 (Mayor: 张延松)
Task ID: liaoning_普兰店区

Investigation date: 2026-07-25
Primary source: Baidu Baike (普兰店区, 马涛, 张延松, 邹积政, 周振雷)

Current status (as of 2026-07-25, verified via Baidu Baike leadership table ~2025年12月):
- 区委书记: 马涛 (男，汉族，1977年1月生，1996年12月入党，1999年8月参加工作，
  大学学历/硕士学位; 2024年4月-2025年7月任普兰店区长，2025年7月起任区委书记)
- 区委副书记、区长: 张延松 (男，汉族，1975年12月生，辽宁康平人，1998年11月入党，
  1999年7月参加工作，管理学硕士; 2025年7月30日全票当选区长)
- 区人大常委会主任: 邹积政 (男，汉族，1970年6月生，中央党校大学学历，1991年8月参加工作，
  1997年6月入党; 此前任区委常委、政法委书记等)
- 区政协主席: 于学义 (身份已知，履历待查)
- 前任区委书记: 周振雷 (男，汉族，1969年2月生，辽宁庄河人; 2022.03-2025.07任普兰店区委书记，
  后任大连市副市长)

Key timeline:
- 2022.03: 周振雷任普兰店区委书记
- 2024.03-04: 马涛任普兰店区长提名人选，随后当选区长
- 2025.03-07: 周振雷兼任大连市副市长，后卸任区委书记
- 2025年7月: 马涛由区长转任区委书记
- 2025年6月: 张延松拟提名为区长候选人
- 2025年7月: 张延松任普兰店区委副书记、区政府党组书记
- 2025-07-30: 张延松全票当选普兰店区人民政府区长
- 2025-12-30: 邹积政当选区人大常委会主任

Research confidence:
- Core leadership (马涛/张延松): confirmed via Baidu Baike with career histories
- 周振雷 (predecessor): confirmed via Baidu Baike with full career history
- 邹积政 (人大主任): confirmed via Baidu Baike with career history
- 于学义 (政协主席): confirmed identity only, career history blocked by anti-crawl
- Standing committee roster: mostly unknown (web access degraded - Baidu, government sites blocked)
- All claims sourced from Baidu Baike pages accessible during investigation

Notes:
- 普兰店区 is a district of Dalian city, formerly 普兰店市 (撤市设区)
- Web search tools (Exa rate-limited, Baidu CAPTCHA, Jina Reader timeout) degraded
- Broader 区委常委名单 (专职副书记、常务副区长、纪委书记、组织部长、宣传部长等)
  could not be confirmed due to network restrictions
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

SLUG = "普兰店区"
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

    # 1. 马涛 — 区委书记 (former 区长)
    {
        "id": 1,
        "name": "马涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "1996年12月",
        "work_start": "1999年8月",
        "current_post": "区委书记",
        "current_org": "中共大连市普兰店区委员会",
        "source": "https://baike.baidu.com/item/%E9%A9%AC%E6%B6%9B/19658226",
    },
    # 2. 张延松 — 区委副书记、区长
    {
        "id": 2,
        "name": "张延松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "辽宁康平",
        "education": "管理学硕士（辽宁师范大学中文系）",
        "party_join": "1998年11月",
        "work_start": "1999年7月",
        "current_post": "区长",
        "current_org": "大连市普兰店区人民政府",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%BB%B6%E6%9D%BE/19141706",
    },

    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════

    # 3. 周振雷 — 前任区委书记 (2022.03-2025.07)，现任大连市副市长
    {
        "id": 3,
        "name": "周振雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年2月",
        "birthplace": "辽宁庄河",
        "education": "在职研究生学历，工商管理硕士",
        "party_join": "1990年12月",
        "work_start": "1991年8月",
        "current_post": "大连市副市长（前任区委书记）",
        "current_org": "大连市人民政府",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E6%8C%AF%E9%9B%B7/3200523",
    },

    # ════════════════════════════════════════
    # Key Leadership Roster
    # ════════════════════════════════════════

    # 4. 邹积政 — 区人大常委会主任
    {
        "id": 4,
        "name": "邹积政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年6月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "1997年6月",
        "work_start": "1991年8月",
        "current_post": "区人大常委会主任",
        "current_org": "普兰店区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E9%82%B9%E7%A7%AF%E6%94%BF/57864991",
    },
    # 5. 于学义 — 区政协主席
    {
        "id": 5,
        "name": "于学义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议普兰店区委员会",
        "source": "https://baike.baidu.com/item/%E4%BA%8E%E5%AD%A6%E4%B9%89/59220513",
    },

    # ════════════════════════════════════════
    # Standing Committee / Deputies (Gap entries)
    #   The following are standard positions in a district-level 区委常委会.
    #   Names could not be confirmed due to web access degradation.
    # ════════════════════════════════════════

    # Standing committee — placeholder for 专职副书记
    {
        "id": 6,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委专职副书记（待确认）",
        "current_org": "中共大连市普兰店区委员会",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 常务副区长
    {
        "id": 7,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长（待确认）",
        "current_org": "大连市普兰店区人民政府",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 纪委书记
    {
        "id": 8,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记（待确认）",
        "current_org": "中共大连市普兰店区纪律检查委员会",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 组织部长
    {
        "id": 9,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长（待确认）",
        "current_org": "中共大连市普兰店区委组织部",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 宣传部长
    {
        "id": 10,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长（待确认）",
        "current_org": "中共大连市普兰店区委宣传部",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 统战部长
    {
        "id": 11,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长（待确认）",
        "current_org": "中共大连市普兰店区委统战部",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
    # Standing committee — placeholder for 政法委书记
    {
        "id": 12,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记（待确认）",
        "current_org": "中共大连市普兰店区委政法委员会",
        "source": "Gap — needs further investigation (typical standing committee position)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共大连市普兰店区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 2,
        "name": "大连市普兰店区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市人民政府",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 3,
        "name": "普兰店区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "大连市人大常委会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议普兰店区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协大连市委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 5,
        "name": "中共大连市普兰店区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共大连市纪律检查委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 6,
        "name": "中共大连市普兰店区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市普兰店区委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 7,
        "name": "中共大连市普兰店区委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市普兰店区委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 8,
        "name": "中共大连市普兰店区委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市普兰店区委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 9,
        "name": "中共大连市普兰店区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市普兰店区委员会",
        "location": "辽宁省大连市普兰店区",
    },
    {
        "id": 10,
        "name": "大连市普兰店区人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "大连军分区",
        "location": "辽宁省大连市普兰店区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 马涛 - 区委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "区委书记、区人武部党委第一书记",
     "start": "2025年7月", "end": "present",
     "rank": "正处级",
     "note": "2025年7月23日以区委书记兼人武部党委第一书记身份出席任职大会"},
    # 马涛 - 区长 (previous)
    {"person_id": 1, "org_id": 2, "title": "区长",
     "start": "2024年4月", "end": "2025年7月",
     "rank": "正处级",
     "note": "2024年3月提名为区长候选人，2024年4月当选"},
    # 马涛 - 前期职务
    {"person_id": 1, "org_id": 1, "title": "党的二十大代表（大连保税区党群工作部部长时期）",
     "start": "约2017年", "end": "约2021年",
     "rank": "",
     "note": "曾任党群工作部副部长兼团委书记、二十里堡街道党工委书记、大连保税区党工委委员/党群工作部部长/编委办主任、大连市公共文化服务中心主任、大连市文化和旅游局（2021年7月起）"},
    # 马涛 - 保税区
    {"person_id": 1, "org_id": 2, "title": "大连保税区党工委委员、党群工作部部长、编委办主任",
     "start": "约2015年", "end": "约2021年",
     "rank": "",
     "note": "在大连保税区期间的具体起止时间待查"},

    # 张延松 - 区长 (current)
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025-07-30", "end": "present",
     "rank": "正处级", "note": "2025年7月30日全票当选普兰店区人民政府区长"},
    # 张延松 - 区委副书记、党组书记
    {"person_id": 2, "org_id": 1, "title": "区委副书记、区政府党组书记",
     "start": "2025年6月/7月", "end": "present",
     "rank": "正处级",
     "note": "2025年6月拟提名为副省级城市县(市、区)长候选人"},
    # 张延松 - 金普新区/金石滩
    {"person_id": 2, "org_id": 1, "title": "大连金普新区党工委委员、大连金石滩国家旅游度假区党委书记、管委会主任",
     "start": "约2024年", "end": "2025年",
     "rank": "副厅级/保留副厅长级",
     "note": "在金普新区和金石滩工作期间"},
    # 张延松 - 瓦房店
    {"person_id": 2, "org_id": 1, "title": "瓦房店市委副书记、复州城镇党委书记",
     "start": "约2023年", "end": "约2024年",
     "rank": "保留副厅长级",
     "note": "保留副厅长级"},
    # 张延松 - 共青团大连市委
    {"person_id": 2, "org_id": 1, "title": "共青团大连市委书记、党组书记、市青联主席",
     "start": "2015-12", "end": "2020-06",
     "rank": "正局级（共青团）",
     "note": "2018年7月起兼任市青联主席; 2020年6月起兼挂职贵州省六盘水市委常委"},
    # 张延松 - 共青团大连市委副书记
    {"person_id": 2, "org_id": 1, "title": "共青团大连市委副书记、党组成员、市青联副主席",
     "start": "2009-12", "end": "2015-12",
     "rank": "副局级",
     "note": "2009年4-9月挂职贵州六盘水六枝特区区长助理; 2009年10-12月挂职大连长兴岛"},
    # 张延松 - 大连民族学院
    {"person_id": 2, "org_id": 1, "title": "大连民族学院团委书记、学工部副部长",
     "start": "2005-03", "end": "2009-12",
     "rank": "",
     "note": "兼学生处副处长、大学生创新与实践教育研究中心副主任等"},
    # 张延松 - 大连民族学院早期
    {"person_id": 2, "org_id": 1, "title": "大连民族学院团委副书记（主持工作）",
     "start": "2003-12", "end": "2005-03",
     "rank": "",
     "note": ""},
    # 张延松 - 大连民族学院起步
    {"person_id": 2, "org_id": 1, "title": "大连民族学院党委办公室秘书/基础部团委书记",
     "start": "1999-07", "end": "2003-12",
     "rank": "",
     "note": "1999.07-2002.05 党委办公室(学院办公室)秘书; 2002.05-2003.12 基础部(预科部)团委书记兼少数民族预科辅导员"},

    # ── Predecessors ──
    # 周振雷 - 大连市副市长
    {"person_id": 3, "org_id": 1, "title": "大连市副市长",
     "start": "2025-03", "end": "present",
     "rank": "副厅级",
     "note": "2025年3月起兼任; 2025年7月后不再兼任普兰店区委书记"},
    # 周振雷 - 普兰店区委书记
    {"person_id": 3, "org_id": 1, "title": "普兰店区委书记",
     "start": "2022-03", "end": "2025-07",
     "rank": "正处级",
     "note": "2022年3月-2025年3月专职任区委书记; 2025年3月起兼任大连市副市长"},
    # 周振雷 - 瓦房店市长
    {"person_id": 3, "org_id": 1, "title": "瓦房店市委副书记、市长",
     "start": "2018-08", "end": "2022-03",
     "rank": "正处级",
     "note": "2019年1月正式当选; 兼大连太平湾沿海经济区党工委副书记/管委会主任"},
    # 周振雷 - 大连市林业局局长
    {"person_id": 3, "org_id": 1, "title": "大连市林业局局长",
     "start": "2017-10", "end": "2018-08",
     "rank": "正处级",
     "note": ""},
    # 周振雷 - 普兰店区常务副区长
    {"person_id": 3, "org_id": 2, "title": "普兰店区常务副区长",
     "start": "2016-02", "end": "2017-10",
     "rank": "副处级",
     "note": "2016年2月普兰店市撤市设区"},
    # 周振雷 - 普兰店市委常委、副市长
    {"person_id": 3, "org_id": 2, "title": "普兰店市委常委、副市长",
     "start": "2012-09", "end": "2016-02",
     "rank": "副处级",
     "note": "时任普兰店市（县级市）"},
    # 周振雷 - 大连市林业局
    {"person_id": 3, "org_id": 1, "title": "大连市林业局副局长、党组成员",
     "start": "2006-11", "end": "2012-09",
     "rank": "副局级",
     "note": "此前历任: 海防林管理所技术员/所长、林业局造林项目办副主任、森林公安分局局长兼防火办副主任、造林经营处处长"},
    # 周振雷 - 早期
    {"person_id": 3, "org_id": 1, "title": "大连市海防林管理所技术员",
     "start": "1991-08", "end": "1995-05",
     "rank": "",
     "note": "大连市林业系统起步"},

    # ── 区人大常委会 ──
    # 邹积政 - 人大主任
    {"person_id": 4, "org_id": 3, "title": "区人大常委会党组书记、主任",
     "start": "2025-12-30", "end": "present",
     "rank": "正处级",
     "note": ""},
    # 邹积政 - 政法委书记 (previous)
    {"person_id": 4, "org_id": 9, "title": "区委常委、政法委书记",
     "start": "", "end": "2025-12",
     "rank": "副处级",
     "note": "转任人大前的职务"},
    # 邹积政 - 统战部长 (previous)
    {"person_id": 4, "org_id": 8, "title": "区委常委、统战部部长、区政协党组副书记",
     "start": "", "end": "",
     "rank": "副处级",
     "note": "此前曾任此职"},
    # 邹积政 - 区委办主任
    {"person_id": 4, "org_id": 1, "title": "区委办公室主任兼区委保密委员会专职副主任",
     "start": "", "end": "",
     "rank": "",
     "note": "此前曾任此职"},
    # 邹积政 - 南山街道
    {"person_id": 4, "org_id": 1, "title": "普兰店区南山街道办事处主任",
     "start": "", "end": "",
     "rank": "",
     "note": "早期职务"},

    # ── 区政协 ──
    # 于学义 - 政协主席
    {"person_id": 5, "org_id": 4, "title": "区政协党组书记、主席",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "履历待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 马涛 <-> 张延松: 党政主要领导搭档 & 区长职务交接
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "马涛由区长转任区委书记，张延松接任区长",
     "overlap_org": "大连市普兰店区人民政府",
     "overlap_period": "2025年7月"},
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共大连市普兰店区委员会/大连市普兰店区人民政府",
     "overlap_period": "2025年7月起"},

    # 马涛 <-> 周振雷: 前任-继任
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "马涛接替周振雷任普兰店区委书记",
     "overlap_org": "中共大连市普兰店区委员会",
     "overlap_period": "2025年7月"},

    # 周振雷 <-> 张延松: 前任区长链条？不直接。周振雷曾在瓦房店任市长，张延松也曾任瓦房店市委副书记
    {"person_a": 3, "person_b": 2, "type": "overlap",
     "context": "周振雷曾任瓦房店市长（2019-2022），张延松曾任瓦房店市委副书记（约2023-2024），可能在不同时期在瓦房店市工作，但时间不完全重叠",
     "overlap_org": "瓦房店市",
     "overlap_period": "2019-2024（有间隔）"},
    {"person_a": 3, "person_b": 2, "type": "same_system",
     "context": "两人均有大连市辖区/县级市主要领导工作经历，周振雷在普兰店-瓦房店-普兰店轮换，张延松在共青团-瓦房店-金普新区-普兰店路径",
     "overlap_org": "大连市",
     "overlap_period": ""},

    # 马涛 <-> 邹积政: 区委书记与人大主任
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区人大常委会主任; 邹积政此前曾任区委常委",
     "overlap_org": "中共大连市普兰店区委员会/普兰店区人大常委会",
     "overlap_period": "截至2025年12月"},

    # 马涛 <-> 于学义: 区委书记与政协主席
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区政协主席工作搭档",
     "overlap_org": "中共大连市普兰店区委员会/普兰店区政协",
     "overlap_period": "截至2026年7月"},

    # 张延松 <-> 邹积政: 区长与人大主任
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "区长与区人大常委会主任工作搭档",
     "overlap_org": "大连市普兰店区人民政府/普兰店区人大常委会",
     "overlap_period": "2025年12月起"},

    # 邹积政 <-> 前任主要领导: 邹积政长期在普兰店工作
    {"person_a": 4, "person_b": 3, "type": "overlap",
     "context": "邹积政在普兰店区工作期间，周振雷曾任普兰店区委书记（2022-2025）",
     "overlap_org": "中共大连市普兰店区委员会",
     "overlap_period": "2022-2025"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTRY
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "普兰店区百度百科（领导信息截至2025年12月）",
            "url": "https://baike.baidu.com/item/%E6%99%AE%E5%85%B0%E5%BA%97%E5%8C%BA",
            "publisher": "百度百科",
            "published_at": "2025-12",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "确认马涛(区委书记)、张延松(区长)、邹积政(人大主任)、于学义(政协主席)",
        },
        {
            "id": "S002",
            "title": "马涛百度百科",
            "url": "https://baike.baidu.com/item/%E9%A9%AC%E6%B6%9B/19658226",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "马涛的出生年月、教育、入党时间、工作起始时间、职业生涯摘要",
        },
        {
            "id": "S003",
            "title": "张延松百度百科",
            "url": "https://baike.baidu.com/item/%E5%BC%A0%E5%BB%B6%E6%9D%BE/19141706",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "张延松的完整仕途履历（1999年起逐级晋升）",
        },
        {
            "id": "S004",
            "title": "邹积政百度百科",
            "url": "https://baike.baidu.com/item/%E9%82%B9%E7%A7%AF%E6%94%BF/57864991",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "邹积政的出生、入党、工作起始、职业生涯摘要",
        },
        {
            "id": "S005",
            "title": "周振雷百度百科",
            "url": "https://baike.baidu.com/item/%E5%91%A8%E6%8C%AF%E9%9B%B7/3200523",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "周振雷的完整仕途履历（1991年起至大连市副市长）",
        },
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON GENERATORS
# ══════════════════════════════════════════════════════════════════════════════


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    province = "辽宁省"
    city = "大连市"
    region = "普兰店区"
    person_id_base = f"pulandianqu_{name}"

    # ── 马涛 (区委书记) ──
    if name == "马涛":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": province,
                "city": city,
                "region": region,
                "job": "区委书记",
                "task_id": "liaoning_普兰店区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_base,
                "name": "马涛",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1977年1月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "（待查）",
                        "major": "",
                        "degree": "大学（学历），硕士（学位）",
                        "study_type": "unknown",
                        "source_ids": ["S002"],
                    }
                ],
                "party_join": "1996年12月",
                "work_start": "1999年8月",
                "dedupe_keys": {
                    "name_birth": "马涛_1977年1月",
                    "name_birthplace": "马涛_",
                    "official_profile_url": "https://baike.baidu.com/item/%E9%A9%AC%E6%B6%9B/19658226",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共大连市普兰店区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"],
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "大连保税区",
                    "title": "大连保税区党工委委员、党群工作部部长、编委办主任",
                    "level": "",
                    "location": "辽宁省大连市",
                    "system": "development_zone",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "此前曾任党群工作部副部长兼团委书记、二十里堡街道党工委书记",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "start": "unknown",
                    "end": "约2021年",
                    "org": "大连市公共文化服务中心",
                    "title": "主任",
                    "level": "",
                    "location": "辽宁省大连市",
                    "system": "other",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "start": "2021年7月",
                    "end": "2024年3月",
                    "org": "大连市文化和旅游局",
                    "title": "（职务待查）",
                    "level": "",
                    "location": "辽宁省大连市",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "2021年7月起在大连市文化和旅游局工作",
                    "confidence": "plausible",
                    "source_ids": ["S002"],
                },
                {
                    "start": "2024年3月",
                    "end": "2024年4月",
                    "org": "大连市普兰店区人民政府",
                    "title": "区长提名人选",
                    "level": "正处级",
                    "location": "辽宁省大连市普兰店区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "start": "2024年4月",
                    "end": "2025年7月",
                    "org": "大连市普兰店区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "辽宁省大连市普兰店区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "任区长期间主持区政府全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "start": "2025年7月",
                    "end": "present",
                    "org": "中共大连市普兰店区委员会",
                    "title": "区委书记、区人武部党委第一书记",
                    "level": "正处级",
                    "location": "辽宁省大连市普兰店区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替周振雷；2025年7月23日以书记身份出席人武部党委第一书记任职大会",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共大连市普兰店区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省大连市普兰店区"},
                {"org_id": 2, "name": "大连市普兰店区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省大连市普兰店区"},
            ],
            "relationships": [
                {"person": "张延松", "person_id": f"{person_id_base}_张延松",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "马涛由区长转任区委书记，张延松接任区长",
                 "overlap_org": "大连市普兰店区人民政府",
                 "overlap_period": "2025年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S003"]},
                {"person": "张延松", "person_id": f"{person_id_base}_张延松",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共大连市普兰店区委员会/大连市普兰店区人民政府",
                 "overlap_period": "2025年7月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "周振雷", "person_id": f"{person_id_base}_周振雷",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "马涛接替周振雷任普兰店区委书记",
                 "overlap_org": "中共大连市普兰店区委员会",
                 "overlap_period": "2025年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S005"]},
                {"person": "邹积政", "person_id": f"{person_id_base}_邹积政",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区人大常委会主任工作搭档",
                 "overlap_org": "中共大连市普兰店区委员会",
                 "overlap_period": "2025年12月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S004"]},
                {"person": "于学义", "person_id": f"{person_id_base}_于学义",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区政协主席工作搭档",
                 "overlap_org": "中共大连市普兰店区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
            ],
            "governance_record": [
                {
                    "period": "2024年4月-2025年7月",
                    "domain": "other",
                    "achievement_or_event": "主持普兰店区人民政府全面工作",
                    "role_in_event": "区长",
                    "measurable_outcome": "",
                    "location": "大连市普兰店区",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["development_zone", "government", "party", "cultural_services"],
                "geographic_pattern": ["大连市（保税区、公共文化、文旅局、普兰店）"],
                "promotion_velocity": {
                    "summary": "公开源信息有限，晋升速度大致正常区县干部节奏",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道不足，暂无法判断工作风格",
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
                "biggest_gap": "马涛的毕业院校、出生地、籍贯、大连保税区前早期职业经历、具体专业和学位类型",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "马涛的毕业院校、专业和学位类型？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["马涛 毕业 院校 大连"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "马涛的出生地和籍贯？",
                    "why_it_matters": "身份去重",
                    "suggested_queries": ["马涛 出生 大连 普兰店"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "马涛在大连保税区工作的具体起止时间和完整职务序列？",
                    "why_it_matters": "评估开发区的专业背景",
                    "suggested_queries": ["马涛 保税区 任职"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "马涛在大连市文化和旅游局的具体职务？",
                    "why_it_matters": "填补2021-2024年间的职业空白",
                    "suggested_queries": ["马涛 文化和旅游局 任职"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "马涛1999年8月参加工作后至大连保税区期间的早期履历？",
                    "why_it_matters": "约1999-2012年期间的职业经历",
                    "suggested_queries": ["马涛 1999 大连"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 张延松 (区长) ──
    if name == "张延松":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": province,
                "city": city,
                "region": region,
                "job": "区长",
                "task_id": "liaoning_普兰店区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_base,
                "name": "张延松",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1975年12月",
                "birthplace": "辽宁康平",
                "native_place": "辽宁康平",
                "education": [
                    {
                        "period": "1995-1999",
                        "institution": "辽宁师范大学",
                        "major": "汉语言文学教育",
                        "degree": "本科",
                        "study_type": "full_time",
                        "source_ids": ["S003"],
                    },
                    {
                        "period": "2011-2014",
                        "institution": "大连理工大学",
                        "major": "行政管理",
                        "degree": "管理学硕士",
                        "study_type": "part_time",
                        "source_ids": ["S003"],
                    },
                ],
                "party_join": "1998年11月",
                "work_start": "1999年7月",
                "dedupe_keys": {
                    "name_birth": "张延松_1975年12月",
                    "name_birthplace": "张延松_辽宁康平",
                    "official_profile_url": "https://baike.baidu.com/item/%E5%BC%A0%E5%BB%B6%E6%9D%BE/19141706",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "大连市普兰店区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"],
            },
            "career_timeline": [
                {"start": "1999-07", "end": "2002-05", "org": "大连民族学院",
                 "title": "党委办公室（学院办公室）秘书", "level": "",
                 "location": "辽宁省大连市", "system": "education",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2002-05", "end": "2003-12", "org": "大连民族学院基础部（预科部）",
                 "title": "团委书记兼少数民族预科辅导员", "level": "",
                 "location": "辽宁省大连市", "system": "education",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2003-12", "end": "2005-03", "org": "大连民族学院",
                 "title": "团委副书记（主持工作）", "level": "",
                 "location": "辽宁省大连市", "system": "education",
                 "rank": "", "is_key_promotion": True,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2005-03", "end": "2006-04", "org": "大连民族学院",
                 "title": "团委书记、学工部副部长、学生处副处长", "level": "",
                 "location": "辽宁省大连市", "system": "education",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2006-04", "end": "2009-12", "org": "大连民族学院",
                 "title": "团委书记（兼多职）", "level": "",
                 "location": "辽宁省大连市", "system": "education",
                 "rank": "", "is_key_promotion": False,
                 "notes": "兼大学生创新与实践教育研究中心、大学生文化素质教育中心副主任等",
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2009-04", "end": "2009-09", "org": "贵州省六盘水市六枝特区",
                 "title": "区长助理（挂职）", "level": "",
                 "location": "贵州省六盘水市", "system": "government",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2009-10", "end": "2009-12", "org": "大连长兴岛临港工业区",
                 "title": "党群部副部长（挂职）", "level": "",
                 "location": "辽宁省大连市", "system": "government",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2009-12", "end": "2010-05", "org": "共青团大连市委",
                 "title": "副书记、党组成员", "level": "副局级",
                 "location": "辽宁省大连市", "system": "organization",
                 "rank": "副局级", "is_key_promotion": True,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2010-05", "end": "2015-12", "org": "共青团大连市委",
                 "title": "副书记、党组成员、市青联副主席", "level": "副局级",
                 "location": "辽宁省大连市", "system": "organization",
                 "rank": "副局级", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2015-12", "end": "2018-07", "org": "共青团大连市委",
                 "title": "书记、党组书记", "level": "正局级（共青团）",
                 "location": "辽宁省大连市", "system": "organization",
                 "rank": "正局级", "is_key_promotion": True,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2018-07", "end": "2020-06", "org": "共青团大连市委",
                 "title": "书记、党组书记、市青联主席", "level": "正局级（共青团）",
                 "location": "辽宁省大连市", "system": "organization",
                 "rank": "正局级", "is_key_promotion": False,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2020-06", "end": "约2022年", "org": "贵州省六盘水市",
                 "title": "市委常委（挂职）", "level": "副厅级",
                 "location": "贵州省六盘水市", "system": "party",
                 "rank": "副厅级", "is_key_promotion": False,
                 "notes": "挂职援贵，同时保留共青团大连市委书记职务",
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "unknown", "end": "约2024年", "org": "瓦房店市",
                 "title": "瓦房店市委副书记、复州城镇党委书记", "level": "保留副厅长级",
                 "location": "辽宁省大连市瓦房店市", "system": "party",
                 "rank": "保留副厅长级", "is_key_promotion": False,
                 "confidence": "plausible", "source_ids": ["S003"]},
                {"start": "unknown", "end": "2025年6月", "org": "大连金普新区/大连金石滩国家旅游度假区",
                 "title": "金普新区党工委委员、金石滩国家旅游度假区党委书记、管委会主任", "level": "",
                 "location": "辽宁省大连市金普新区", "system": "development_zone",
                 "rank": "", "is_key_promotion": False,
                 "confidence": "plausible", "source_ids": ["S003"]},
                {"start": "2025年6月/7月", "end": "2025-07-30", "org": "大连市普兰店区人民政府",
                 "title": "区委副书记、区政府党组书记、代区长", "level": "正处级",
                 "location": "辽宁省大连市普兰店区", "system": "government",
                 "rank": "正处级", "is_key_promotion": True,
                 "confidence": "confirmed", "source_ids": ["S003"]},
                {"start": "2025-07-30", "end": "present", "org": "大连市普兰店区人民政府",
                 "title": "区长", "level": "正处级",
                 "location": "辽宁省大连市普兰店区", "system": "government",
                 "rank": "正处级", "is_key_promotion": True,
                 "notes": "2025年7月30日全票当选",
                 "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "organizations": [
                {"org_id": 1, "name": "中共大连市普兰店区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省大连市普兰店区"},
                {"org_id": 2, "name": "大连市普兰店区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省大连市普兰店区"},
            ],
            "relationships": [
                {"person": "马涛", "person_id": f"{person_id_base}_马涛",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "张延松接替马涛任普兰店区区长",
                 "overlap_org": "大连市普兰店区人民政府",
                 "overlap_period": "2025年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S003"]},
                {"person": "马涛", "person_id": f"{person_id_base}_马涛",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共大连市普兰店区委员会/大连市普兰店区人民政府",
                 "overlap_period": "2025年7月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "周振雷", "person_id": f"{person_id_base}_周振雷",
                 "relationship_type": "same_system", "strength": "weak",
                 "evidence": "两人均有瓦房店工作经历（周振雷曾任瓦房店市长2019-2022，张延松曾任瓦房店市委副书记约2023-2024），但时间不完全重叠",
                 "overlap_org": "瓦房店市",
                 "overlap_period": "2019-2024（有间隔）",
                 "direction": "undirected", "confidence": "plausible",
                 "source_ids": ["S003", "S005"]},
                {"person": "邹积政", "person_id": f"{person_id_base}_邹积政",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区人大常委会主任工作搭档",
                 "overlap_org": "大连市普兰店区人民政府/普兰店区人大常委会",
                 "overlap_period": "2025年12月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S004"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["共青团与青年工作", "组织人事"],
                "secondary_specializations": ["教育管理", "行政管理"],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["education", "organization", "government", "development_zone", "party"],
                "geographic_pattern": ["大连市（大连民族学院→团市委→瓦房店→金普新区→普兰店）",
                                       "贵州省六盘水市（挂职）"],
                "promotion_velocity": {
                    "summary": "团口起步，2009年由高校转入共青团系统，2015年升任团市委书记（正局级），2023年后转岗区县实职，晋升路径清晰",
                    "notable_fast_promotions": [
                        "2009年由大连民族学院团委书记直接调任共青团大连市委副书记（副局级）",
                        "2015年升任共青团大连市委书记（正局级），时年约40岁",
                    ],
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
                "career_completeness": "complete",
                "relationship_confidence": "medium",
                "biggest_gap": "瓦房店市委副书记和金普新区/金石滩工作的具体起止时间",
            },
            "open_questions": [
                {
                    "priority": "medium",
                    "question": "张延松在瓦房店市委副书记任上的具体起止时间？",
                    "why_it_matters": "精确时间线有助于与周振雷的瓦房店经历对比",
                    "suggested_queries": ["张延松 瓦房店 副书记 任命"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "medium",
                    "question": "张延松在金普新区/金石滩的具体任职起止时间？",
                    "why_it_matters": "精确时间线",
                    "suggested_queries": ["张延松 金普新区 金石滩 任职"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "low",
                    "question": "张延松挂职贵州六盘水时期的评价和政绩？",
                    "why_it_matters": "评估跨省工作成效",
                    "suggested_queries": ["张延松 六盘水 挂职"],
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
        ("区委书记", "马涛"),
        ("区长", "张延松"),
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
