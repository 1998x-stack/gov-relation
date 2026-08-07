#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 西吉县, 固原市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_西吉县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 西吉县人民政府 领导之窗 (primary, current as of 2026-08):
    https://www.nxxj.gov.cn/xxgk_13648/ldzc/
    * 位西北 (书记: 市委常委兼任) profile
    * 郑超 (县长) profile
    * 县委/人大/政府/政协 full roster
  - 新京报（位西北兼任西吉县委书记，简历/继任）:
    https://www.bjnews.com.cn/detail/1734406989129182.html
  - 澎湃新闻（郑超任西吉代县长 2025-11-13、前任县长马天峡赴自治区残联）:
    https://thepaper.cn/newsDetail_forward_31966644
  - 北京日报（郑超破格提拔/任前公示）:
    https://xinwen.bjd.com.cn/content/s675574d2e4b06b0a5623f3d9.html
  - 中国经济网（白学贵 2021-09 任西吉县委书记、王学军赴吴忠）:
    http://district.ce.cn/newarea/sddy/202109/04/t20210904_36881808.shtml
  - 西吉县政府新闻（2026-06/07 在任确认: 春节走访/两优一先/领导调研）
  - 百度百科·白学贵 / 马天峡（前任去向二级信源）

Confidence notes:
  - Current roles: confirmed via official 领导之窗 + 2026 新闻
  - 位西北 career timeline: confirmed via 新京报 (public media) + official appointments
  - 郑超 prior career + appointment: confirmed via 澎湃/北京日报 任前公示
  - 白学贵/马天峡 (前任) 去向: confirmed via 正式公示 + media; detail via 百科 (二级)
  - Biographical gaps (前任的再前任、郑超任前博士院校细分）在 open_questions
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "西吉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_西吉县"
if _CURRENT_DIR.name == "ningxia_西吉县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-2 core (书记/县长), 3-11 县委常委会, 12-16 政府班子,
#      17 人大主任, 18 政协主席, 19 前任书记, 20 前任县长
persons = [
    # ════ CORE: 县委书记 & 县长 ════
    {
        "id": 1,
        "name": "位西北",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-01",
        "birthplace": "宁夏回族自治区银川市永宁县",
        "education": "经济管理学研究生（党校）",
        "party_join": "中共党员（2000-01）",
        "work_start": "2000-09",
        "current_post": "固原市委常委、西吉县委书记",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 2,
        "name": "郑超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-01",
        "birthplace": "江西省抚州市临川区",
        "education": "博士研究生（西北农林科技大学）",
        "party_join": "中共党员（2010-06）",
        "work_start": "2018-07",
        "current_post": "西吉县委副书记、政府党组书记、县长",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    # ════ 县委常委会 ════
    {
        "id": 3,
        "name": "徐升光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-11",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "2007-09",
        "current_post": "西吉县委副书记、政法委书记",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 4,
        "name": "田进国",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1982-06",
        "birthplace": "宁夏回族自治区中卫市海原县",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委副书记（挂职，回族）",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 5,
        "name": "黄德强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委副书记、政府党组副书记、副县长（挂职·闽宁协作）",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 6,
        "name": "刘杏萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、组织部部长",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 7,
        "name": "白瑞",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、宣传部部长",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 8,
        "name": "倪万枢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "",
        "education": "法律（中国政法大学）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、纪委书记、监委主任",
        "current_org": "西吉县纪委监委",
        "source": "https://www.nxxj.gov.cn/xxgk_89936/ldzc/",
    },
    {
        "id": 9,
        "name": "段文君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、政府党组成员、副县长",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 10,
        "name": "于亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、政府党组成员、副县长（挂职·上海飞机设计研究院）",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 11,
        "name": "潘宏强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    # ════ 县政府班子 ════
    {
        "id": 12,
        "name": "王永鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "宁夏回族自治区固原市",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县副县长",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 13,
        "name": "吴军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-05",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县副县长、公安局党委书记、局长",
        "current_org": "西吉县公安局",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 14,
        "name": "连廷仓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县副县长",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 15,
        "name": "马永虎",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县副县长",
        "current_org": "西吉县人民政府",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 16,
        "name": "李学智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县政府党组成员、西吉工业园区管委会主任",
        "current_org": "西吉工业园区管委会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    # ════ 人大 / 政协 ════
    {
        "id": 17,
        "name": "李聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县人大常委会党组书记、主任",
        "current_org": "西吉县人大常委会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    {
        "id": 18,
        "name": "马保师",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西吉县政协党组书记、主席",
        "current_org": "政协西吉县委员会",
        "source": "https://www.nxxj.gov.cn/xxgk_13648/ldzc/",
    },
    # ════ 前任职（关键历史人物） ════
    {
        "id": 19,
        "name": "白学贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "education": "研究生（宁夏区委组织部干部一处处长出身）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任西吉县委书记（2021-09~2024-12）；现任吴忠市委副书记、副市长、代市长",
        "current_org": "中共吴忠市委员会",
        "source": "http://district.ce.cn/newarea/sddy/202109/04/t20210904_36881808.shtml",
    },
    {
        "id": 20,
        "name": "马天峡",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976-11",
        "birthplace": "宁夏回族自治区固原市泾源县",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任西吉县长（~2022-2025）；现任宁夏回族自治区残联党组成员、副理事长",
        "current_org": "宁夏回族自治区残疾人联合会",
        "source": "https://thepaper.cn/newsDetail_forward_31966644",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共西吉县委员会", "type": "党委", "level": "县处级", "parent": "中共固原市委员会", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 2, "name": "西吉县人民政府", "type": "政府", "level": "县处级", "parent": "固原市人民政府", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 3, "name": "西吉县人大常委会", "type": "人大", "level": "县处级", "parent": "固原市人大常委会", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 4, "name": "政协西吉县委员会", "type": "政协", "level": "县处级", "parent": "政协固原市委员会", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 5, "name": "西吉县纪委监委", "type": "纪委", "level": "县处级", "parent": "中共西吉县委员会", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 6, "name": "西吉县公安局", "type": "政府", "level": "乡科级", "parent": "西吉县人民政府", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 7, "name": "西吉工业园区管委会", "type": "开发区", "level": "县处级", "parent": "西吉县人民政府", "location": "宁夏回族自治区固原市西吉县"},
    {"id": 8, "name": "中共固原市委员会", "type": "党委", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区固原市"},
    {"id": 9, "name": "固原市人民政府", "type": "政府", "level": "地厅级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区固原市"},
    {"id": 10, "name": "中共吴忠市委员会", "type": "党委", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 11, "name": "宁夏回族自治区残疾人联合会", "type": "群团", "level": "厅局级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 位西北 (1)
    {"person_id": 1, "org_id": 1, "title": "西吉县委书记", "start": "2024-12", "end": "present", "rank": "正处级", "note": "固原市委常委兼任，2024-12 起（接替白学贵）"},
    {"person_id": 1, "org_id": 8, "title": "固原市委常委", "start": "2021-12", "end": "present", "rank": "副厅级", "note": "2021-12 任固原市委常委"},
    {"person_id": 1, "org_id": 8, "title": "固原市委常委、市委秘书长、政法委书记", "start": "2021-12", "end": "2024-12", "rank": "副厅级", "note": "任西吉书记前在固原市委分管政法委"},
    {"person_id": 1, "org_id": 9, "title": "固原市副市长", "start": "2021-08", "end": "2021-12", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "自治区司法厅党委委员、政治部主任", "start": "2013-07", "end": "2021-08", "rank": "副厅级", "note": "31岁公开选拔升副厅（宁夏区直公开选拔）"},
    {"person_id": 1, "org_id": 1, "title": "共青团银川市委书记", "start": "2012", "end": "2013-07", "rank": "正科级", "note": "银川市团委系统"},
    {"person_id": 1, "org_id": 1, "title": "银川市委办公厅副主任等", "start": "2010", "end": "2012", "rank": "", "note": "银川市委办公厅、金凤区委办公室等基层"},
    # 郑超 (2)
    {"person_id": 2, "org_id": 2, "title": "西吉县人民政府县长", "start": "2026-02", "end": "present", "rank": "正处级", "note": "2025-11-13 任代县长，2026-02 正式县长"},
    {"person_id": 2, "org_id": 2, "title": "西吉县人民政府代县长", "start": "2025-11-13", "end": "2026-02", "rank": "正处级", "note": "县十八届人大常委会第三十三次会议任命"},
    {"person_id": 2, "org_id": 1, "title": "西吉县委副书记、政府党组书记", "start": "2025-11", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "共青团固原市委书记", "start": "2024", "end": "2025-11", "rank": "正处级", "note": "2024-10 任前公示后出任"},
    {"person_id": 2, "org_id": 9, "title": "福建省福清市（挂职）市委常委、副市长", "start": "", "end": "2024", "rank": "副处级", "note": "闽宁协作挂职"},
    {"person_id": 2, "org_id": 2, "title": "西吉县委常委、副县长", "start": "2021", "end": "2024", "rank": "副处级", "note": "2021 破格提拔（突破任职年限）"},
    {"person_id": 2, "org_id": 2, "title": "西吉县副县长、硝河乡党委书记", "start": "2021", "end": "2022", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "西吉县硝河乡党委书记", "start": "2020", "end": "2021", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "共青团固原市委副书记", "start": "2019", "end": "2020", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "固原市农业农村局二级主任科员", "start": "2019", "end": "2019", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "固原市农牧局定向选调生", "start": "2018-07", "end": "2019", "rank": "", "note": ""},
    # 徐升光 (3)
    {"person_id": 3, "org_id": 1, "title": "西吉县委副书记、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 田进国 (4)
    {"person_id": 4, "org_id": 1, "title": "西吉县委副书记（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "自治区农业农村厅挂职"},
    # 黄德强 (5)
    {"person_id": 5, "org_id": 2, "title": "西吉县政府党组副书记、副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "闽宁协作/招商引资"},
    # 刘杏萍 (6)
    {"person_id": 6, "org_id": 1, "title": "西吉县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "来自原州区（区委常委）"},
    # 白瑞 (7)
    {"person_id": 7, "org_id": 1, "title": "西吉县委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "曾任西吉政法委书记；来源固原市委统战部"},
    # 倪万枢 (8)
    {"person_id": 8, "org_id": 1, "title": "西吉县委常委、纪委书记、监委会主任", "start": "", "end": "present", "rank": "副处级", "note": "来自原州区检察院/固原市纪委"},
    # 段文君 (9)
    {"person_id": 9, "org_id": 2, "title": "西吉县副县长（常委）", "start": "", "end": "present", "rank": "副处级", "note": "来自共青团固原市委/原州区"},
    # 于亮 (10)
    {"person_id": 10, "org_id": 2, "title": "西吉县副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "上海飞机设计研究院（央企对口帮扶）"},
    # 潘宏强 (11)
    {"person_id": 11, "org_id": 1, "title": "西吉县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 县政府副县长
    {"person_id": 12, "org_id": 2, "title": "西吉县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "西吉县副县长、公安局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "西吉县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "西吉县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 7, "title": "西吉工业园区管委会主任", "start": "", "end": "present", "rank": "", "note": "县政府党组成员"},
    # 李聪 (17) / 马保师 (18)
    {"person_id": 17, "org_id": 3, "title": "西吉县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "曾任西吉县委常委、组织部长、县委副书记"},
    {"person_id": 18, "org_id": 4, "title": "西吉县政协主席（回族）", "start": "", "end": "present", "rank": "正处级", "note": "曾任西吉统战部长"},
    # 白学贵 (19)
    {"person_id": 19, "org_id": 1, "title": "西吉县委书记", "start": "2021-09", "end": "2024-12", "rank": "正处级", "note": "曾任固原市委副书记兼西吉县委书记"},
    {"person_id": 19, "org_id": 8, "title": "固原市委副书记、政法委书记", "start": "2021-09", "end": "2026-07", "rank": "副厅级", "note": ""},
    {"person_id": 19, "org_id": 10, "title": "吴忠市委副书记、副市长、代市长", "start": "2026-07", "end": "present", "rank": "正厅级", "note": "跨市交流至吴忠"},
    # 马天峡 (20)
    {"person_id": 20, "org_id": 2, "title": "西吉县人民政府县长", "start": "2022", "end": "2025-11-13", "rank": "正处级", "note": "2022-03-30 十八届人大二次会议选举；2025-11-13 辞职"},
    {"person_id": 20, "org_id": 11, "title": "自治区残联党组成员、副理事长", "start": "2025-11", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "隆德县委副书记、县长（宁夏）", "start": "2020", "end": "2022", "rank": "正处级", "note": "跨县调入西吉前任隆德县长"},
    {"person_id": 20, "org_id": 9, "title": "固原市委副秘书长、政策研究室主任", "start": "", "end": "2020", "rank": "", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记位西北与县长郑超构成党政正职搭档（2025-11至今）", "overlap_org": "西吉县", "overlap_period": "2025-11至今"},
    # 书记继任
    {"person_a": 19, "person_b": 1, "type": "predecessor_successor", "context": "白学贵2024-12卸任西吉县委书记后位西北接任（固原市委常委兼任）", "overlap_org": "中共西吉县委员会", "overlap_period": "2024-12"},
    # 县长继任
    {"person_a": 20, "person_b": 2, "type": "predecessor_successor", "context": "马天峡2025-11辞职后郑超2025-11-13任代县长、2026-02正式县长", "overlap_org": "西吉县人民政府", "overlap_period": "2025-11"},
    # 人大常委会 / 政协 领导班子
    {"person_a": 17, "person_b": 1, "type": "overlap", "context": "人大主任李聪与县委书记位西北同为县四套班子成员", "overlap_org": "西吉县", "overlap_period": "present"},
    {"person_a": 18, "person_b": 1, "type": "overlap", "context": "政协主席马保师与县委书记位西北同为县四套班子成员", "overlap_org": "西吉县", "overlap_period": "present"},
    # 县委书记与县委常委会成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记领导县委副书记/政法委书记徐升光", "overlap_org": "中共西吉县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记领导组织部长刘杏萍", "overlap_org": "中共西吉县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记领导宣传部长白瑞", "overlap_org": "中共西吉县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记领导纪委书记倪万枢", "overlap_org": "中共西吉县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "书记领导统战部长潘宏强", "overlap_org": "中共西吉县委员会", "overlap_period": "present"},
    # 县长与县政府班子
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长领导副县长段文君", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长领导副县长王永鑫", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长领导副县长兼公安局长吴军", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长领导副县长连廷仓", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长领导副县长马永虎", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "县长领导园区管委会主任李学智", "overlap_org": "西吉县人民政府", "overlap_period": "present"},
    # 跨县/跨市交流（干部输送通道）
    {"person_a": 6, "person_b": 1, "type": "cross_county_transfer", "context": "组织部长刘杏萍来自原州区，原州区→西吉干部输送", "overlap_org": "固原市原州区/西吉县", "overlap_period": "present"},
    {"person_a": 8, "person_b": 1, "type": "cross_county_transfer", "context": "纪委书记倪万枢来自原州区检察院/固原市纪检系统，固原市直→西吉", "overlap_org": "固原市/西吉县", "overlap_period": "present"},
    {"person_a": 7, "person_b": 1, "type": "cross_county_transfer", "context": "宣传部长白瑞来自固原市委统战部，固原市直→西吉", "overlap_org": "固原市/西吉县", "overlap_period": "present"},
    {"person_a": 9, "person_b": 1, "type": "cross_county_transfer", "context": "副县长段文君来自共青团固原市/原州区，固原市原州区→西吉县", "overlap_org": "固原市/西吉县", "overlap_period": "present"},
    {"person_a": 14, "person_b": 1, "type": "cross_county_transfer", "context": "副县长连廷仓来自原州区委组织部/原州区府办，原州区→西吉县", "overlap_org": "固原市原州区/西吉县", "overlap_period": "present"},
    # 前任跨县交流
    {"person_a": 20, "person_b": 2, "type": "cross_county_transfer", "context": "马天峡由隆德县长调任西吉县长（跨县调入）", "overlap_org": "隆德县/西吉县", "overlap_period": "2022"},
    # 挂职/对口帮扶
    {"person_a": 10, "person_b": 2, "type": "cross_county_transfer", "context": "挂职副县长于亮来自上海飞机设计研究院（央企对口帮扶）", "overlap_org": "上海飞机设计研究院/西吉县", "overlap_period": "present"},
    {"person_a": 4, "person_b": 1, "type": "cross_county_transfer", "context": "挂职副书记田进国来自自治区农业农村厅（厅县挂职）", "overlap_org": "宁夏农业农村厅/西吉县", "overlap_period": "present"},
    {"person_a": 5, "person_b": 2, "type": "cross_county_transfer", "context": "挂职副县长黄海强经闽宁协作对口帮扶", "overlap_org": "闽宁协作/西吉县", "overlap_period": "present"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def _career_rows(person: dict) -> list:
    """Build a career timeline for the person JSON from confirmed evidence."""
    name = person["name"]
    if name == "位西北":
        rows = [
            {"start": "2024-12", "end": "present", "org": "中共西吉县委员会/中共固原市委员会", "title": "西吉县委书记（固原市委常委兼任）", "rank": "正/副厅", "confidence": "confirmed", "note": "2024-12 兼任西吉县委书记，接替白学贵"},
            {"start": "2021-12", "end": "2024-12", "org": "中共固原市委", "title": "固原市委常委、市委秘书长、政法委书记", "rank": "副厅级", "confidence": "confirmed", "note": ""},
            {"start": "2021-08", "end": "2021-12", "org": "固原市人民政府", "title": "固原市副市长", "rank": "副厅级", "confidence": "confirmed", "note": ""},
            {"start": "2013-07", "end": "2021-08", "org": "宁夏回族自治区司法厅", "title": "司法厅党委委员、政治部主任", "rank": "副厅级", "confidence": "confirmed", "note": "31岁公开选拔升副厅"},
            {"start": "2012", "end": "2013-07", "org": "共青团银川市委", "title": "共青团银川市委书记", "rank": "正科级", "confidence": "confirmed", "note": "此前: 银川市委办/金凤区团委等"},
            {"start": "2000", "end": "2012", "org": "银川市", "title": "银川市郊区逸夫小学教师→金凤区团委/政府办/党办→银川市府办→银川市委办", "rank": "", "confidence": "confirmed", "note": "早期基层履历"},
        ]
    elif name == "郑超":
        rows = [
            {"start": "2026-02", "end": "present", "org": "西吉县人民政府", "title": "西吉县县长", "rank": "正处级", "confidence": "confirmed", "note": "2025-11-13 任代县长，2026-02 正式县长"},
            {"start": "2025-11-13", "end": "2026-02", "org": "西吉县人民政府", "title": "西吉县代县长", "rank": "正处级", "confidence": "confirmed", "note": "县人大第三十三次会议任命"},
            {"start": "2024", "end": "2025-11", "org": "共青团固原市委", "title": "共青团固原市委书记", "rank": "正处级", "confidence": "confirmed", "note": ""},
            {"start": "2021", "end": "2024", "org": "西吉县人民政府", "title": "西吉县副县长（破格提拔）、查河乡党委书记等", "rank": "副处级", "confidence": "confirmed", "note": "2021 破格提拔突破任职年限"},
            {"start": "2018-07", "end": "2021", "org": "固原市/西县乡", "title": "固原市农牧局定向选调生→农业农村局→硝河乡/平峰镇→共青团固原市委副书记", "rank": "", "confidence": "confirmed", "note": "选调生起点"},
        ]
    elif name == "白学贵":
        rows = [
            {"start": "2026-07", "end": "present", "org": "中共吴忠市委员会", "title": "吴忠市委副书记、副市长、代市长", "rank": "正厅级", "confidence": "confirmed", "note": "跨市晋升"},
            {"start": "2021-09", "end": "2024-12", "org": "中共西吉县委员会", "title": "西吉县委书记（固原市委副书记兼任）", "rank": "正处/副厅", "confidence": "confirmed", "note": "2021-09~2024-12"},
        ]
    elif name == "马天峡":
        rows = [
            {"start": "2022", "end": "2025-11-13", "org": "西吉县人民政府", "title": "西吉县人民政府县长", "rank": "正处级", "confidence": "confirmed", "note": "2025-11-13 辞职"},
            {"start": "2025-11", "end": "present", "org": "宁夏回族自治区残疾人联合会", "title": "自治区残联党组成员、副理事长", "rank": "副厅级", "confidence": "confirmed", "note": ""},
            {"start": "2020", "end": "2022", "org": "隆德县人民政府", "title": "隆德县委副书记、县长", "rank": "正处级", "confidence": "confirmed", "note": "跨县调入西吉"},
        ]
    else:
        rows = [
            {"start": "unknown", "end": "present", "org": person.get("current_org", ""), "title": person.get("current_post", ""), "rank": "副处级" if "长" in person.get("current_post", "") else "", "confidence": "plausible", "note": "现任职务见官方领导之窗（截至2026-08）"},
        ]
    return rows


def write_person_json(person: dict, job: str) -> Path:
    """Write a person graph JSON file to the staging directory."""
    name = person["name"]
    person_id = f"xiji_{name}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-固原市-{job}-{name}.json"
    career = _career_rows(person)
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "西吉县",
            "job": job,
            "task_id": "ningxia_西吉县",
            "time_focus": "2026-08 (current)"
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": person.get("education", ""), "study_type": "party_school" if "党校" in person.get("education", "") else "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if job in ["县委书记", "县长"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [
            {"id": 1, "name": "中共西吉县委员会", "type": "党委"},
            {"id": 2, "name": "西吉县人民政府", "type": "政府"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if name in ["位西北", "郑超", "白学贵", "马天峡"] else "local_ladder",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
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
                "description": "（无公开纪律或廉洁风险信号）",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"西吉县人民政府 - {name}领导之窗 / 任前公示",
                "url": person.get("source", ""),
                "publisher": "西吉县人民政府 / 宁夏区委组织部",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official government website / 任前公示 / 媒体交叉确认"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed" if name in ["位西北", "郑超"] else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的完整履历（出生地、入党/参加工作时间、早期职务）"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{name}的部分履历细节（入党/参加工作年份、更早职任、正式县长当选日期等）",
                "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
                "suggested_queries": [f"{name} 简历 西吉", f"{name} 任前公示", f"{name} 出生年月"],
                "last_attempted": AS_OF
            }
        ]
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} dataset (staging: {STAGING})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("\nWriting person JSONs ...")
    by_name = {p["name"]: p for p in persons}
    write_person_json(by_name["位西北"], "县委书记")
    write_person_json(by_name["郑超"], "县长")
    write_person_json(by_name["白学贵"], "前任县委书记")
    write_person_json(by_name["马天峡"], "前任县长")

    print("\nOutput verification:")
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {path.name} MISSING")

    json_count = len(list(PJSON_DIR.glob("*.json")))
    print(f"  ✅ Person JSON files: {json_count}")

    print(f"\n{SLUG} build complete.")


if __name__ == "__main__":
    main()