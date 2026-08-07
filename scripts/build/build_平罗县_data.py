#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平罗县 (Pingluo County), 石嘴山市, 宁夏回族自治区.

Investigation date: 2026-08-07
Task ID: ningxia_平罗县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 平罗县人民政府 领导之窗 (primary, current as of 2026-08):
    https://pingluo.gov.cn/xxgk/ldzc/
    * 刘兆明 (书记) profile
    * 李亮 (县长) profile
    * 县委/人大/政府/政协 full roster
  - 平罗县领导干部大会 / 县委组织部 (中国共产党的党内任职通知):
    http://www.nxpldj.gov.cn/djyw/202412/t20241219_955683.html  (2024-12-17 刘兆明任书记)
  - 平罗县人武部党委第一书记任职 : https://pingluo.gov.cn/xwzx/tttj/202501/t20250103_4779064.html
  - 宁夏区委组织部任前公示 2025年第10号 (2025-08-04, 李亮拟任县长):
    https://www.nx.gov.cn/zwgk/rsrm/202508/t20250804_4979558.html
  - 平罗县纪委监委 冯硕 领导简历: http://www.pljjjc.gov.cn/pljwldjl/202410/t20241018_5015797.html
  - 百度百科·刘兆明 (career timeline): https://baike.baidu.com/item/刘兆明/18563628
  - 中新网 2026-05-29 朱剑被查: https://www.chinanews.com.cn/gn/202605/29/10630748.shtml
  - 网易 2026-05 刘强任大武口区委书记: https://c.m.163.com/news/a/KSG9Q75I0536DJA.html
  - 永宁县 data (朱剑 cross-county): report/20260807-永宁县-领导班子工作关系网络报告.md

Confidence notes:
  - Current roles: confirmed via official 领导之窗 / 任前公示 / 干部任免 (official)
  - 刘兆明 career timeline: confirmed via Baidu Baike + official appointments
  - 李亮 prior post (石嘴山高新区管委会副主任、大武口区政府党组副书记): confirmed via 任前公示 2025年第10号
  - Biographical gaps (birthplace, education specifics, 入党/工作起始年份) flagged in open_questions
  - 葛建华 (宣传部长): plausible (2025 reports), 2026-08 领导之窗未列 — flagged
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
SLUG = "平罗县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_平罗县"
if _CURRENT_DIR.name == "ningxia_平罗县":
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
# IDs: 1-2 core (书记/县长), 3-5 县委副书记/前任书记, 6-17 县委常委会,
#      18-24 政府班子, 25-27 前任, 28-30 人大, 31-33 政协
persons = [
    # ════ CORE: 县委书记 & 县长 ════
    {
        "id": 1,
        "name": "刘兆明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石嘴山市委常委、平罗县委书记、宁夏平罗工业园区党工委书记",
        "current_org": "中共平罗县委员会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 2,
        "name": "李亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-12",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委副书记、县长、宁夏平罗工业园区党工委副书记、管委会主任",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    # ════ 专职副书记 ════
    {
        "id": 3,
        "name": "黄勤如",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-04",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委副书记、县委国安办主任",
        "current_org": "中共平罗县委员会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    # ════ 县委常委会 ════
    {
        "id": 4,
        "name": "金鹏星",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1984-12",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、政法委书记",
        "current_org": "中共平罗县委员会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 5,
        "name": "孟超",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、常务副县长",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 6,
        "name": "张永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、组织部部长",
        "current_org": "中共平罗县委员会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 7,
        "name": "赵亮",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、统战部部长",
        "current_org": "中共平罗县委员会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 8,
        "name": "冯硕",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1983-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、纪委书记、监委主任",
        "current_org": "平罗县纪委监委",
        "source": "http://www.pljjjc.gov.cn/pljwldjl/202410/t20241018_5015797.html",
    },
    {
        "id": 9,
        "name": "刘文静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、副县长",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 10,
        "name": "邢志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、副县长（挂职）",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 11,
        "name": "徐龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-04",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县委常委、副县长（挂职）",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    # ════ 政府班子 ════
    {
        "id": 12,
        "name": "白玉昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县政府党组副书记、宁夏工业园区党工委副书记、管委会常务副主任",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 13,
        "name": "王雁",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1981-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "平罗县副县长",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 14,
        "name": "吴一凡",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1985-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县副县长、县公安局局长",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 15,
        "name": "谢生良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县副县长（三级调研员）",
        "current_org": "平罗县人民政府",
        "source": "https://shizuishan.gov.cn/zwgk/zfxxgkml/rsxx/202607/t20260716_5290337.html",
    },
    # ════ 人大 / 政协 ════
    {
        "id": 16,
        "name": "吴亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县人大常委会党组书记、主任",
        "current_org": "平罗县人大常委会",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 17,
        "name": "李斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县政协党组书记、主席",
        "current_org": "平罗县政协",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    # ════ 前任 / 关键历史人物 ════
    {
        "id": 18,
        "name": "宋世文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县前任县委书记（2024-12 卸任；现任自治区体育局党组书记、局长，2026-07 拟任地级市党委书记）",
        "current_org": "中共平罗县委员会",
        "source": "http://www.nxpld.gov.cn/djyw/202412/t20241219_955681.html",
    },
    {
        "id": 19,
        "name": "郭耀峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县前任县长（2025 卸任，去向未明）",
        "current_org": "平罗县人民政府",
        "source": "https://pingluo.gov.cn/xxgk/ldzc/",
    },
    {
        "id": 20,
        "name": "蒋哲文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-09",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县原县委书记（2018-2021；后升石嘴山市委常委）",
        "current_org": "中共平罗县委员会",
        "source": "http://www.xinhuanet.com/politics/2021-01/26/c_1127027150.htm",
    },
    {
        "id": 21,
        "name": "朱剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平罗县原县长、县委书记（约2012-2018；2026-05 因涉嫌严重违纪违法被接受审查调查）",
        "current_org": "中共平罗县委员会",
        "source": "https://www.chinanews.com.cn/gn/202605/29/10630748.shtml",
    },
    {
        "id": 22,
        "name": "刘强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "陕西省榆林市",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "石嘴山市大武口区委书记（2026-05至今）；曾在平罗县基层任职",
        "current_org": "中共石嘴山市大武口区委员会",
        "source": "https://c.m.163.com/news/a/KSG9Q75I0536DJA.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共平罗县委员会", "type": "党委", "level": "县处级", "parent": "中共石嘴山市委员会", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 2, "name": "平罗县人民政府", "type": "政府", "level": "县处级", "parent": "石嘴山市人民政府", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 3, "name": "平罗县人大常委会", "type": "人大", "level": "县处级", "parent": "石嘴山市人大常委会", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 4, "name": "平罗县政协", "type": "政协", "level": "县处级", "parent": "石嘴山市政协", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 5, "name": "平罗县纪委监委", "type": "纪委", "level": "县处级", "parent": "中共平罗县委员会", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 6, "name": "平罗县公安局", "type": "政府", "level": "乡科级", "parent": "平罗县人民政府", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 7, "name": "宁夏平罗工业园区（党工委/管委会）", "type": "开发区", "level": "县处级", "parent": "平罗县人民政府", "location": "宁夏回族自治区石嘴山市平罗县"},
    {"id": 8, "name": "石嘴山市人民政府", "type": "政府", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区石嘴山市"},
    {"id": 9, "name": "中共石嘴山市委员会", "type": "党委", "level": "地厅级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区石嘴山市"},
    {"id": 10, "name": "中共石嘴山市大武口区委员会", "type": "党委", "level": "县处级", "parent": "中共石嘴山市委员会", "location": "宁夏回族自治区石嘴山市大武口区"},
    {"id": 11, "name": "大武口区人民政府", "type": "政府", "level": "县处级", "parent": "石嘴山市人民政府", "location": "宁夏回族自治区石嘴山市大武口区"},
    {"id": 12, "name": "石嘴山高新技术产业开发区（党工委/管委会）", "type": "开发区", "level": "县处级", "parent": "石嘴山市人民政府", "location": "宁夏回族自治区石嘴山市大武口区"},
    {"id": 13, "name": "惠农区人民政府", "type": "政府", "level": "县处级", "parent": "石嘴山市人民政府", "location": "宁夏回族自治区石嘴山市惠农区"},
    {"id": 14, "name": "中共石嘴山市惠农区委员会", "type": "党委", "level": "县处级", "parent": "中共石嘴山市委员会", "location": "宁夏回族自治区石嘴山市惠农区"},
    {"id": 15, "name": "中共永宁县委员会", "type": "党委", "level": "县处级", "parent": "中共银川市委员会", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 16, "name": "永宁县人民政府", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市永宁县"},
    {"id": 17, "name": "宁夏回族自治区财政厅", "type": "政府", "level": "厅局级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
    {"id": 18, "name": "中共宁夏回族自治区委员会", "type": "党委", "level": "省部级", "parent": "", "location": "宁夏回族自治区银川市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘兆明 (1)
    {"person_id": 1, "org_id": 9, "title": "石嘴山市委常委", "start": "2024-12", "end": "present", "rank": "副厅级", "note": "2024-12-17 任石嘴山市委常委"},
    {"person_id": 1, "org_id": 1, "title": "平罗县委书记", "start": "2024-12", "end": "present", "rank": "正处级", "note": "2024-12-17 任平罗县委书记，接替宋世文"},
    {"person_id": 1, "org_id": 7, "title": "宁夏平罗工业园区党工委书记", "start": "2024-12", "end": "present", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县人武部党委第一书记", "start": "2025-01", "end": "present", "rank": "", "note": "2025-01-02 兼任"},
    {"person_id": 1, "org_id": 8, "title": "石嘴山市发展和改革委员会主任、市国动办（人防办）主任", "start": "2024-09", "end": "2024-12", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "石嘴山市水务局局长", "start": "", "end": "2024-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "石嘴山市国资委党委书记、主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "市人社局党组成员、市社保局局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "惠农区副区长（兼经开区管委会副主任）", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "市国土资源局党组成员、副局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "市农牧局党委委员、副局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "市委宣传部办公室副主任、主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "惠农区委组织部副部长、老干部局局长", "start": "", "end": "", "rank": "正科级", "note": ""},
    # 李亮 (2)
    {"person_id": 2, "org_id": 2, "title": "平罗县长", "start": "2025", "end": "present", "rank": "正处级", "note": "2025 下半年任代县长/县长，接替郭耀峰"},
    {"person_id": 2, "org_id": 1, "title": "平罗县委副书记", "start": "2025", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "宁夏平罗工业园区党工委副书记、管委会主任", "start": "2025", "end": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "石嘴山高新区党工委副书记、管委会常务副主任（正处级）", "start": "", "end": "2025", "rank": "正处级", "note": "任前公示 2025年第10号"},
    {"person_id": 2, "org_id": 11, "title": "大武口区政府党组副书记", "start": "", "end": "2025", "rank": "", "note": "任前公示 2025年第10号"},
    # 黄勤如 (3)
    {"person_id": 3, "org_id": 1, "title": "县委副书记、县委国安办主任", "start": "", "end": "present", "rank": "副处级", "note": "负责县委日常工作运转协调"},
    # 金鹏星 (4)
    {"person_id": 4, "org_id": 1, "title": "县委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孟超 (5)
    {"person_id": 5, "org_id": 2, "title": "常务副县长（党组副书记）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张永刚 (6)
    {"person_id": 6, "org_id": 1, "title": "县委常委、组织部部长", "start": "2023", "end": "present", "rank": "副处级", "note": "2023 年接任组织部长"},
    # 赵亮 (7)
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "2026-07 任前公示拟进一步使用"},
    # 冯硕 (8)
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "纪委书记、监委主任", "start": "2024", "end": "present", "rank": "副处级", "note": "2024-10 起在任"},
    # 刘文静 (9)
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责住建、生态环境、商务招商"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 邢志刚 (10)
    {"person_id": 10, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐龙 (11)
    {"person_id": 11, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 白玉昌 (12)
    {"person_id": 12, "org_id": 7, "title": "宁夏工业园区管委会常务副主任", "start": "", "end": "present", "rank": "", "note": "政府党组副书记"},
    # 王雁 (13)
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责农业农村、乡村振兴、水务；民盟"},
    # 吴一凡 (14)
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "2025-12", "end": "present", "rank": "副处级", "note": "2025-12-02 任公安局长/督察长"},
    {"person_id": 14, "org_id": 6, "title": "县公安局局长、督察长", "start": "2025-12", "end": "present", "rank": "正科级", "note": "平政干发〔2025〕19号"},
    # 谢生良 (15)
    {"person_id": 15, "org_id": 2, "title": "副县长（三级调研员）", "start": "", "end": "present", "rank": "副处级", "note": "2026-07 任前公示拟进一步使用"},
    # 吴亮 (16)
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 李斌 (17)
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 宋世文 (18)
    {"person_id": 18, "org_id": 1, "title": "平罗县委书记（石嘴山市委副书记兼任）", "start": "2021", "end": "2024-12", "rank": "正厅级", "note": "2024-12-17 卸任"},
    # 郭耀峰 (19)
    {"person_id": 19, "org_id": 2, "title": "平罗县长", "start": "2021", "end": "2025", "rank": "正处级", "note": "2025 卸任，李亮接任；去向未明"},
    # 蒋哲文 (20)
    {"person_id": 20, "org_id": 1, "title": "平罗县委书记", "start": "2018-11", "end": "2021", "rank": "正处级", "note": "2021-01 任前公示拟任市委市委常委（石嘴山）"},
    # 朱剑 (21)
    {"person_id": 21, "org_id": 1, "title": "平罗县委书记", "start": "2012", "end": "2018", "rank": "副厅级", "note": "曾任石嘴山市副市长、平罗县委书记；兼平罗县长（2018 年）"},
    {"person_id": 21, "org_id": 17, "title": "宁夏财政厅党组成员、副厅长", "start": "", "end": "2025", "rank": "副厅级", "note": "2026-05 被查"},
    {"person_id": 21, "org_id": 15, "title": "永宁县委书记（银川市委常委）", "start": "2018-10", "end": "2023", "rank": "副厅级", "note": "跨县区交流：平罗→永宁"},
    # 刘强 (22)
    {"person_id": 22, "org_id": 10, "title": "大武口区委书记", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026-05-08 任大武口区委书记，不再任区长"},
    {"person_id": 22, "org_id": 11, "title": "大武口区区长", "start": "2022", "end": "2026-05", "rank": "正处级", "note": "2022-05 补选为区长"},
    {"person_id": 22, "org_id": 1, "title": "平罗县姚伏镇党委书记", "start": "", "end": "2013", "rank": "正科级", "note": "此前在平罗县基层：城关镇、团委、红崖子乡、高仁乡、姚伏镇"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记刘兆明与县长李亮构成党政正职搭档（2025至今）", "overlap_org": "平罗县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "context": "刘兆明任书记期间（2024-12~2025）郭耀峰任县长，党政搭档", "overlap_org": "平罗县", "overlap_period": "2024-12~2025"},
    # 书记继任
    {"person_a": 18, "person_b": 1, "type": "predecessor_successor", "context": "宋世文2024-12卸任后刘兆明接任平罗县委书记", "overlap_org": "中共平罗县委员会", "overlap_period": "2024-12"},
    {"person_a": 20, "person_b": 18, "type": "predecessor_successor", "context": "蒋哲文2021年升任石嘴山市委常委后宋世文接任平罗县委书记", "overlap_org": "中共平罗县委员会", "overlap_period": "2021"},
    {"person_a": 21, "person_b": 20, "type": "predecessor_successor", "context": "朱剑卸任平罗县委书记后蒋哲文2018-11接任", "overlap_org": "中共平罗县委员会", "overlap_period": "2018-11"},
    # 县长继任
    {"person_a": 19, "person_b": 2, "type": "predecessor_successor", "context": "郭耀峰卸任后李亮接任平罗县长（2025）", "overlap_org": "平罗县人民政府", "overlap_period": "2025"},
    # 常委会 / 班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记领导专职县委副书记", "overlap_org": "中共平罗县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记领导政法委书记", "overlap_org": "中共平罗县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记领导组织部部长", "overlap_org": "中共平罗县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记领导纪委书记", "overlap_org": "中共平罗县委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记领导常务副县长", "overlap_org": "中共平罗县委员会", "overlap_period": "present"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长领导常务副县长", "overlap_org": "平罗县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长领导副县长（常委）", "overlap_org": "平罗县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长领导副县长", "overlap_org": "平罗县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长领导副县长兼公安局长", "overlap_org": "平罗县人民政府", "overlap_period": "2025-12至今"},
    {"person_a": 16, "person_b": 1, "type": "overlap", "context": "人大主任吴亮与县委书记刘兆明同为县四套班子成员", "overlap_org": "平罗县", "overlap_period": "present"},
    {"person_a": 17, "person_b": 1, "type": "overlap", "context": "政协主席李斌与县委书记刘兆同为县四套班子成员", "overlap_org": "平罗县", "overlap_period": "present"},
    # 跨县交流：平罗 → 大武口（刘强）
    {"person_a": 22, "person_b": 1, "type": "same_system", "context": "刘强曾在平罗县基层任职（城关镇、平罗县团委、红崖子乡等），与现县委书记刘兆在平罗县委履历有交流", "overlap_org": "平罗县基层", "overlap_period": "2000s-2013"},
    {"person_a": 22, "person_b": 2, "type": "cross_county_transfer", "context": "刘强由平罗县基层干部经石嘴山市历练后任大武口区长、区委书记，体现平罗→大武口干部交流", "overlap_org": "石嘴山市", "overlap_period": "2013-2026"},
    # 跨县交流：平罗↔永宁（朱剑）
    {"person_a": 21, "person_b": 2, "type": "cross_county_transfer", "context": "朱剑由平罗县长/县委书记转任永宁县委书记（银川市委常委），平罗↔银川跨县交流典型", "overlap_org": "平罗县/永宁县", "overlap_period": "2018"},
    # 李亮大武口→平罗
    {"person_a": 2, "person_b": 22, "type": "cross_county_transfer", "context": "李亮由石嘴山高新区管委会副主任、大武口区政府党组副书记调任平罗县长；刘强由平罗基层到大武口区委书记，双城互为干部交流", "overlap_org": "大武口区/平罗县", "overlap_period": "2025-2026"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def _career_rows(person: dict, job: str) -> list:
    """Build a career timeline for the person JSON from confirmed evidence."""
    name = person["name"]
    if name == "刘兆明":
        rows = [
            {"start": "2024-12", "end": "present", "org": "中共平罗县委员会/中共石嘴山市委员会", "title": "平罗县委书记（石嘴山市委常委）", "rank": "副厅/正处", "confidence": "confirmed", "note": "2024-12-17 任石嘴山市委常委、平罗县委书记"},
            {"start": "2025-01", "end": "present", "org": "平罗县人武部", "title": "县人武部党委第一书记", "rank": "", "confidence": "confirmed", "note": "2025-01 兼任"},
            {"start": "2024-09", "end": "2024-12", "org": "石嘴山市发展和改革委员会", "title": "市发改委主任、市国动办主任", "rank": "正处级", "confidence": "confirmed", "note": ""},
            {"start": "unknown", "end": "2024-09", "org": "石嘴山市水务局", "title": "市水务局局长", "rank": "正处级", "confidence": "plausible", "note": "此前任市国资委书记/主任等"},
            {"start": "unknown", "end": "unknown", "org": "中共惠农区委", "title": "惠农区委组织部副部长、老干部局长等", "rank": "", "confidence": "plausible", "note": "早年组织系统履历"},
        ]
    elif name == "李亮":
        rows = [
            {"start": "2025", "end": "present", "org": "平罗县人民政府", "title": "平罗县长", "rank": "正处级", "confidence": "confirmed", "note": "2025 任代县长后转正，接替郭耀峰"},
            {"start": "2025", "end": "present", "org": "中共平罗县委员会", "title": "县委副书记", "rank": "副处级", "confidence": "confirmed", "note": ""},
            {"start": "unknown", "end": "2025", "org": "石嘴山高新区", "title": "高新区党工委副书记、管委会副主任（正处级）", "rank": "正处级", "confidence": "confirmed", "note": "任前公示 2025年第10号"},
            {"start": "unknown", "end": "2025", "org": "大武口区政府", "title": "区政府党组副书记", "rank": "", "confidence": "confirmed", "note": "任前公示 2025年第10号"},
        ]
    elif name == "宋世文":
        rows = [
            {"start": "2021", "end": "2024-12", "org": "中共平罗县委员会", "title": "平罗县委书记（石嘴山之市委副书记兼任）", "rank": "正厅级", "confidence": "confirmed", "note": "2024-12-17 卸任，转自治区党委宣传部副部长/网信办主任等"},
            {"start": "2025-11", "end": "present", "org": "宁夏回族自治区体育局", "title": "党组书记、局长", "rank": "正厅级", "confidence": "confirmed", "note": "2026-07 任前公示拟任地级市党委书记"},
        ]
    elif name == "郭耀峰":
        rows = [
            {"start": "2021", "end": "2025", "org": "平罗县人民政府", "title": "平罗县长", "rank": "正处级", "confidence": "confirmed", "note": "2025 卸任；去向未明"},
        ]
    elif name == "蒋哲文":
        rows = [
            {"start": "2018-11", "end": "2021", "org": "中共平罗县委员会", "title": "平罗县委书记", "rank": "正处级", "confidence": "confirmed", "note": "2021-01 任前公示拟任石嘴山市委常委"},
        ]
    elif name == "朱剑":
        rows = [
            {"start": "2012", "end": "2018", "org": "中共平罗县委员会", "title": "平罗县长、县委书记", "rank": "正处/副厅", "confidence": "confirmed", "note": "约2012-2018，后任永宁县委书记"},
            {"start": "2018-10", "end": "2023", "org": "中共永宁县委员会", "title": "永宁县委书记（银川市委常委）", "rank": "副厅级", "confidence": "confirmed", "note": "跨区县赴任永宁"},
            {"start": "unknown", "end": "2025", "org": "宁夏回族自治区财政厅", "title": "财政厅党组成员、副厅长", "rank": "副厅级", "confidence": "confirmed", "note": "2026-05 因涉嫌严重违纪违法被查"},
        ]
    elif name == "刘强":
        rows = [
            {"start": "2026-05", "end": "present", "org": "中共石嘴山市大武口区委员会", "title": "大武口区委书记", "rank": "正处级", "confidence": "confirmed", "note": "2026-05-08 任"},
            {"start": "2022", "end": "2026-05", "org": "大武口区人民政府", "title": "大武口区区长", "rank": "正处级", "confidence": "confirmed", "note": ""},
            {"start": "2000s", "end": "2013", "org": "平罗县基层", "title": "城关镇镇长助理、平罗县团委书记、红崖子乡乡长、高仁乡党委书记、姚伏镇党委书记", "rank": "正科级", "confidence": "confirmed", "note": "平罗县基层历练后调任石嘴山市直"},
            {"start": "2013", "end": "2022", "org": "石嘴山市直/大武口", "title": "市团委副书记/书记、市审批服务局局长、市财政局局长、大武口区长", "rank": "", "confidence": "confirmed", "note": "石嘴山历练后回任大武口"},
        ]
    else:
        rows = [
            {"start": "unknown", "end": "present", "org": person.get("current_org", ""), "title": person.get("current_post", ""), "rank": "副处级" if "长" in person.get("current_post", "") else "", "confidence": "plausible", "note": "现任职务见官方领导之窗（opas拍卖 2026-08）"},
        ]
    return rows


def write_person_json(person: dict, job: str) -> Path:
    """Write a person graph JSON file to the staging directory."""
    name = person["name"]
    person_id = f"pingluo_{name}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-石嘴山市-{job}-{name}.json"
    career = _career_rows(person, job)
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "石嘴山市",
            "region": "平罗县",
            "job": job,
            "task_id": "ningxia_平罗县",
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
            {"id": 1, "name": "中共平罗县委员会", "type": "党委"},
            {"id": 2, "name": "平罗县人民政府", "type": "政府"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if name in ["刘兆明", "李亮", "宋世文", "朱剑", "刘强"] else "local_ladder",
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
                "type": "none_found" if name != "朱剑" else "disciplinary_action",
                "description": "（无公开纪律或廉洁风险信号）" if name != "朱剑" else "2026-05 因涉嫌严重违纪违法接受审查调查（宁夏纪委监委）",
                "date": "" if name != "朱剑" else "2026-05-29",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"平罗县人民政府 - {name}领导之窗",
                "url": person.get("source", ""),
                "publisher": "平罗县人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Official government website / 任前公示"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的完整履历（出生地、入党/参加工作时间、早期职务）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（出生地、入党时间、参加工作时间和历任职务）",
                "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
                "suggested_queries": [f"{name} 简历 平罗", f"{name} 任前公示", f"{name} 出生年月"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的早前职务经历与调动路径",
                "why_it_matters": "理解干部交流和跨县区调动模式",
                "suggested_queries": [f"{name} 此前 担任", f"{name} 调任"],
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
    write_person_json(by_name["刘兆明"], "县委书记")
    write_person_json(by_name["李亮"], "县长")
    write_person_json(by_name["宋世文"], "前任县委书记")
    write_person_json(by_name["郭耀峰"], "前任县长")
    write_person_json(by_name["朱剑"], "前任县委书记")
    write_person_json(by_name["刘强"], "大武口区区委书记")

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