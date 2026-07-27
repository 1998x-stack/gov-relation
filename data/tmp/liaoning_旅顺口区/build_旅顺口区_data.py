#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 旅顺口区 (Lüshunkou District), 大连市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 大连市
Targets: 区委书记 (Party Secretary: 薛雁翔), 区长 (Mayor: 曹洋)
Task ID: liaoning_旅顺口区

Research date: 2026-07-25
Official source: http://www.dllsk.gov.cn/ (大连市旅顺口区人民政府)

Current status (as of 2026-07-25, verified via 旅顺口区人民政府 website):
- 区委书记: 薛雁翔 (男，汉族，兼任大连市委常委 — 副省级城市市委常委)
- 区长: 曹洋 (男，汉族，1971年6月生，大学学历，工商管理硕士，中共党员)

Leadership roster sourced from:
  - http://www.dllsk.gov.cn/zfxxgk/jgjj_ld.asp (区政府领导页面)
  - http://www.lsk.gov.cn/qzzc.asp?name=曹洋 (曹洋简历)
  - http://www.dllsk.gov.cn/qzzc_maming.asp (马明简历)
  - http://www.dllsk.gov.cn/qzzc_cijunpeng.asp (迟俊鹏简历)
  - http://www.dllsk.gov.cn/qzzc_liyunhong.asp (李云虹简历)
  - http://www.dllsk.gov.cn/qzzc_sunjianyong.asp (孙建勇简历)
  - http://www.dllsk.gov.cn/qzzc_pulu.asp (蒲露简历)
  - http://www.dllsk.gov.cn/qzzc_shideshan.asp (石德山简历)
  - http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121310&classid=2 (区委常委会会议—确认薛雁翔)

Confidence notes:
  薛雁翔: 身份通过区委常委会新闻和工商联新闻确认，为市委常委兼区委书记（副省级城市）。
  曹洋: 通过官方简历页面确认（1971年6月生，大学学历，工商管理硕士）。
  薛雁翔的完整履历尚未在公开页面找到。
  副区长简历除基本信息外缺乏此前任职经历。
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

SLUG = "旅顺口区"

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

    # 1. 薛雁翔 — 市委常委、区委书记
    {
        "id": 1,
        "name": "薛雁翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记（兼大连市委常委）",
        "current_org": "中共旅顺口区委员会",
        "source": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121310&classid=2",
    },
    # 2. 曹洋 — 区委副书记、区长
    {
        "id": 2,
        "name": "曹洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年6月",
        "birthplace": "",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.lsk.gov.cn/qzzc.asp?name=%B2%DC%D1%F3",
    },

    # ════════════════════════════════════════
    # 区人大、区政协领导
    # ════════════════════════════════════════

    # 3. 张峰 — 区人大常委会主任
    {
        "id": 3,
        "name": "张峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "旅顺口区人大常委会",
        "source": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121081&classid=2",
    },
    # 4. 姜利 — 区政协主席
    {
        "id": 4,
        "name": "姜利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协旅顺口区委员会",
        "source": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121081&classid=2",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 5. 马明 — 区委常委、副区长、党组副书记
    {
        "id": 5,
        "name": "马明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "大学学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/qzzc_maming.asp",
    },
    # 6. 郑旭 — 区委常委、副区长
    {
        "id": 6,
        "name": "郑旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121428&classid=2",
    },
    # 7. 迟俊鹏 — 副区长
    {
        "id": 7,
        "name": "迟俊鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年11月",
        "birthplace": "",
        "education": "大学学历，工商管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/qzzc_cijunpeng.asp",
    },
    # 8. 李云虹 — 副区长
    {
        "id": 8,
        "name": "李云虹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/qzzc_liyunhong.asp",
    },
    # 9. 孙建勇 — 副区长
    {
        "id": 9,
        "name": "孙建勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "",
        "education": "大学学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/qzzc_sunjianyong.asp",
    },
    # 10. 蒲露 — 副区长、公安分局局长
    {
        "id": 10,
        "name": "蒲露",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "旅顺口区人民政府/大连市公安局旅顺口分局",
        "source": "http://www.dllsk.gov.cn/qzzc_pulu.asp",
    },
    # 11. 石德山 — 副区长（挂职）
    {
        "id": 11,
        "name": "石德山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "旅顺口区人民政府",
        "source": "http://www.dllsk.gov.cn/qzzc_shideshan.asp",
    },

    # ════════════════════════════════════════
    # 区委其他常委 (Other Standing Committee Members)
    # ════════════════════════════════════════

    # 12. 孙思 — 区委常委、统战部部长
    {
        "id": 12,
        "name": "孙思",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共旅顺口区委员会",
        "source": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121081&classid=2",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 13. 李井山 — 前任区长/党组书记
    {
        "id": 13,
        "name": "李井山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "旅顺口区人民政府（已离任）",
        "source": "http://www.lsk.gov.cn/qzzc.asp?name=%C0%EE%BE%AE%C9%BD",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共旅顺口区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市委员会",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 2,
        "name": "旅顺口区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市人民政府",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 3,
        "name": "旅顺口区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "大连市人大常委会",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 4,
        "name": "政协旅顺口区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协大连市委员会",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 5,
        "name": "旅顺口区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共大连市纪律检查委员会",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 6,
        "name": "大连市公安局旅顺口分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "旅顺口区人民政府",
        "location": "辽宁省大连市旅顺口区",
    },
    {
        "id": 7,
        "name": "中共大连市委",
        "type": "党委",
        "level": "副省级",
        "parent": "中共辽宁省委",
        "location": "辽宁省大连市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──

    # 薛雁翔 - 区委书记（兼大连市委常委）
    {"person_id": 1, "org_id": 1, "title": "区委书记（兼大连市委常委）",
     "start": "", "end": "present",
     "rank": "正局级（副省级城市市委常委）",
     "note": "作为大连市委常委兼任旅顺口区委书记; 2026年7月10日主持召开区委常委会"},
    # 薛雁翔 - 大连市委常委
    {"person_id": 1, "org_id": 7, "title": "中共大连市委常委",
     "start": "", "end": "present",
     "rank": "正局级",
     "note": "副省级城市市委常委"},

    # 曹洋 - 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "主持区政府全面工作; 负责审计局"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": "区委副书记、区政府党组书记"},

    # ── 区人大、区政协 ──
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": ""},
    {"person_id": 4, "org_id": 4, "title": "区政协主席",
     "start": "", "end": "present",
     "rank": "正处级",
     "note": ""},

    # ── 区政府领导 ──
    # 马明 - 区委常委、副区长
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "兼任区政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # 郑旭 - 区委常委、副区长
    {"person_id": 6, "org_id": 2, "title": "区委常委、副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": "2026年7月23日出席旅顺与高新区教育一体化发展启动仪式"},
    {"person_id": 6, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # 迟俊鹏 - 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # 李云虹 - 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # 孙建勇 - 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # 蒲露 - 副区长、公安分局局长
    {"person_id": 10, "org_id": 2, "title": "副区长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 6, "title": "公安分局局长",
     "start": "", "end": "present",
     "rank": "正科级",
     "note": "大连市公安局旅顺口分局党组书记、局长、督察长"},

    # 石德山 - 副区长（挂职）
    {"person_id": 11, "org_id": 2, "title": "副区长（挂职）",
     "start": "", "end": "present",
     "rank": "副处级（挂职）",
     "note": "挂职副区长"},

    # ── 区委其他常委 ──
    {"person_id": 12, "org_id": 1, "title": "区委常委、统战部部长",
     "start": "", "end": "present",
     "rank": "副处级",
     "note": ""},

    # ── 前任领导 ──
    # 李井山 - 前任区长
    {"person_id": 13, "org_id": 2, "title": "区长（前任）",
     "start": "", "end": "（前任）",
     "rank": "正处级",
     "note": "前任旅顺口区长; 官方领导页面中已不再列示"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 薛雁翔 <-> 曹洋: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共旅顺口区委员会/旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 薛雁翔 <-> 马明: 区委书记与区委常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共旅顺口区委员会",
     "overlap_period": "截至2026年7月"},

    # 薛雁翔 <-> 郑旭: 区委书记与区委常委
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长",
     "overlap_org": "中共旅顺口区委员会",
     "overlap_period": "截至2026年7月"},

    # 薛雁翔 <-> 孙思: 区委书记与统战部长
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "区委书记与区委常委、统战部长",
     "overlap_org": "中共旅顺口区委员会",
     "overlap_period": "截至2026年7月"},

    # 薛雁翔 <-> 张峰: 区委书记与人大会主任
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区人大常委会主任; 四套班子领导",
     "overlap_org": "中共旅顺口区委员会/旅顺口区人大常委会",
     "overlap_period": "截至2026年7月"},

    # 薛雁翔 <-> 姜利: 区委书记与政协主席
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区政协主席; 四套班子领导",
     "overlap_org": "中共旅顺口区委员会/政协旅顺口区委员会",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 马明: 区长与常务副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长（党组副书记）",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 郑旭: 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 迟俊鹏: 区长与副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 李云虹: 区长与副区长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 孙建勇: 区长与副区长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 蒲露: 区长与副区长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 石德山: 区长与挂职副区长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "区长与挂职副区长",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 张峰: 区长与人大主任
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区四套班子搭档",
     "overlap_org": "旅顺口区人民政府/旅顺口区人大常委会",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 姜利: 区长与政协主席
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "区四套班子搭档",
     "overlap_org": "旅顺口区人民政府/政协旅顺口区委员会",
     "overlap_period": "截至2026年7月"},

    # 曹洋 <-> 李井山: 前任与继任
    {"person_a": 2, "person_b": 13, "type": "predecessor_successor",
     "context": "曹洋接替李井山任旅顺口区区长",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "交接期未确定"},

    # 马明 <-> 郑旭: 区委常委同事
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "区委常委、副区长同事",
     "overlap_org": "中共旅顺口区委员会/旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},

    # 副区长之间的联系（政府班子成员）
    {"person_a": 7, "person_b": 8, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 7, "person_b": 9, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 7, "person_b": 10, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 7, "person_b": 11, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 8, "person_b": 10, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 8, "person_b": 11, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 9, "person_b": 10, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 9, "person_b": 11, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "旅顺口区人民政府",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "旅顺口区政府官网-领导介绍-区长曹洋",
            "url": "http://www.lsk.gov.cn/qzzc.asp?name=%B2%DC%D1%F3",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "曹洋: 男，汉族，1971年6月生，大学学历，工商管理硕士，中共党员，区委副书记、区长、区政府党组书记",
        },
        {
            "id": "S002",
            "title": "旅顺口区政府官网-领导介绍-马明",
            "url": "http://www.dllsk.gov.cn/qzzc_maming.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "马明: 男，汉族，1978年6月生，中共党员，大学学历，法学硕士，区委常委，副区长、党组副书记",
        },
        {
            "id": "S003",
            "title": "旅顺口区政府官网-领导介绍-迟俊鹏",
            "url": "http://www.dllsk.gov.cn/qzzc_cijunpeng.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "迟俊鹏: 男，汉族，1967年11月生，大学学历，工商管理学硕士，中共党员，副区长",
        },
        {
            "id": "S004",
            "title": "旅顺口区政府官网-领导介绍-李云虹",
            "url": "http://www.dllsk.gov.cn/qzzc_liyunhong.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "李云虹: 女，汉族，1973年生，大学学历，法学学士，中共党员，副区长",
        },
        {
            "id": "S005",
            "title": "旅顺口区政府官网-领导介绍-孙建勇",
            "url": "http://www.dllsk.gov.cn/qzzc_sunjianyong.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "孙建勇: 男，汉族，1972年8月生，大学学历，工程硕士，中共党员，副区长",
        },
        {
            "id": "S006",
            "title": "旅顺口区政府官网-领导介绍-蒲露",
            "url": "http://www.dllsk.gov.cn/qzzc_pulu.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "蒲露: 男，汉族，1976年4月生，中共党员，大学学历、法学学士，副区长，公安分局党组书记、局长、督察长",
        },
        {
            "id": "S007",
            "title": "旅顺口区政府官网-领导介绍-石德山",
            "url": "http://www.dllsk.gov.cn/qzzc_shideshan.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "石德山: 男，汉族，1976年10月生，中共党员，研究生学历，硕士学位，副区长（挂职）",
        },
        {
            "id": "S008",
            "title": "旅顺口区委常委会会议新闻",
            "url": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121310&classid=2",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "2026-07-13",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认薛雁翔为市委常委、旅顺口区委书记（截至2026年7月）",
        },
        {
            "id": "S009",
            "title": "旅顺口区工商联第十二次代表大会新闻",
            "url": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121081&classid=2",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "2026-06-29",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认薛雁翔（市委常委、区委书记）、曹洋（区长）、张峰（人大主任）、姜利（政协主席）、孙思（统战部长）",
        },
        {
            "id": "S010",
            "title": "旅顺口区教育一体化发展启动仪式新闻",
            "url": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121428&classid=2",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认郑旭为区委常委、副区长",
        },
        {
            "id": "S011",
            "title": "旅顺口区政府官网-领导介绍页面",
            "url": "http://www.dllsk.gov.cn/zfxxgk/jgjj_ld.asp",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认区政府领导班子: 曹洋（区长）、马明、迟俊鹏、李云虹、孙建勇、蒲露、石德山（副区长）",
        },
        {
            "id": "S012",
            "title": "旅顺口区七一走访慰问新闻",
            "url": "http://www.dllsk.gov.cn/xwzxdetail.asp?newsID=121109&classid=2",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "2026-07-01",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认区领导: 薛雁翔、曹洋、张峰、姜利、张春雨、张仁强、吴庆禹、刘锋等",
        },
        {
            "id": "S013",
            "title": "旅顺口区政府官网-前任区长页面",
            "url": "http://www.lsk.gov.cn/qzzc.asp?name=%C0%EE%BE%AE%C9%BD",
            "publisher": "大连市旅顺口区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "medium",
            "notes": "李井山为前任区长、党组书记（已离任，页面已改为曹洋内容）",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"lvshunkou_{name}"

    # ── 薛雁翔 (区委书记) ──
    if name == "薛雁翔":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "大连市",
                "region": "旅顺口区",
                "job": "区委书记",
                "task_id": "liaoning_旅顺口区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "薛雁翔",
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
                    "name_birth": "薛雁翔_",
                    "name_birthplace": "薛雁翔_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记（兼大连市委常委）",
                "current_org": "中共旅顺口区委员会",
                "administrative_rank": "正局级（副省级城市市委常委）",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S008"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共旅顺口区委员会",
                    "title": "区委书记（兼大连市委常委）",
                    "level": "正局级",
                    "location": "辽宁省大连市旅顺口区",
                    "system": "party",
                    "rank": "正局级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月确认以市委常委身份兼任旅顺口区委书记",
                    "confidence": "confirmed",
                    "source_ids": ["S008"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共大连市委",
                    "title": "市委常委",
                    "level": "正局级",
                    "location": "辽宁省大连市",
                    "system": "party",
                    "rank": "正局级",
                    "is_key_promotion": True,
                    "notes": "副省级城市市委常委",
                    "confidence": "confirmed",
                    "source_ids": ["S008"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共旅顺口区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省大连市旅顺口区"},
                {"org_id": 7, "name": "中共大连市委", "type": "党委",
                 "level": "副省级", "location": "辽宁省大连市"},
            ],
            "relationships": [
                {"person": "曹洋", "person_id": "lvshunkou_曹洋",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共旅顺口区委员会/旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008", "S009"]},
                {"person": "张峰", "person_id": "lvshunkou_张峰",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区人大常委会主任",
                 "overlap_org": "中共旅顺口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S009"]},
                {"person": "姜利", "person_id": "lvshunkou_姜利",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区政协主席",
                 "overlap_org": "中共旅顺口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S009"]},
                {"person": "马明", "person_id": "lvshunkou_马明",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区委书记与区委常委、副区长",
                 "overlap_org": "中共旅顺口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "郑旭", "person_id": "lvshunkou_郑旭",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区委书记与区委常委、副区长",
                 "overlap_org": "中共旅顺口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S010"]},
                {"person": "孙思", "person_id": "lvshunkou_孙思",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区委书记与区委常委、统战部长",
                 "overlap_org": "中共旅顺口区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S009"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "other",
                    "achievement_or_event": "主持召开区委常委会，研究部署防汛抗旱、对口支援、科技创新、党建等工作",
                    "role_in_event": "区委书记，主持常委会",
                    "measurable_outcome": "部署全区防汛、经济发展、科技创新和党建等重点工作",
                    "location": "大连市旅顺口区",
                    "confidence": "confirmed",
                    "source_ids": ["S008"],
                },
                {
                    "period": "2026年6月",
                    "domain": "other",
                    "achievement_or_event": "出席区工商联第十二次代表大会并讲话",
                    "role_in_event": "市委常委、区委书记",
                    "measurable_outcome": "肯定非公经济发展成效，鼓励企业家把握旅顺高新区一体化发展机遇",
                    "location": "大连市旅顺口区",
                    "confidence": "confirmed",
                    "source_ids": ["S009"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["大连市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度; 兼任市委常委表明其政治地位较高",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以工作会议为主，不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": ["一体化发展", "科技创新", "党建", "为民服务"],
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
                "biggest_gap": "薛雁翔的完整履历（出生年月、籍贯、教育背景、任旅顺口区委书记前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "薛雁翔的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["薛雁翔 简历 大连", "薛雁翔 出生", "薛雁翔 百度百科"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "薛雁翔何时开始担任旅顺口区委书记？此前任何职务？",
                    "why_it_matters": "理清履职起始时间和职业晋升路径",
                    "suggested_queries": ["薛雁翔 任 旅顺口区委书记", "薛雁翔 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "薛雁翔如何晋升为大连市委常委？何时兼任区委书记？",
                    "why_it_matters": "了解其政治地位和晋升路径",
                    "suggested_queries": ["薛雁翔 大连市委常委", "薛雁翔 任免"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "薛雁翔此前在大连市哪个部门或区县任职？",
                    "why_it_matters": "评估其专业背景和跨区经验",
                    "suggested_queries": ["薛雁翔 曾任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "薛雁翔之前谁担任旅顺口区委书记？前任去向？",
                    "why_it_matters": "厘清交接链条",
                    "suggested_queries": ["旅顺口区 前任 区委书记"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 曹洋 (区长) ──
    if name == "曹洋":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "大连市",
                "region": "旅顺口区",
                "job": "区长",
                "task_id": "liaoning_旅顺口区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "曹洋",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1971年6月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "大学学历",
                     "study_type": "unknown", "source_ids": ["S001"]},
                    {"period": "", "institution": "", "major": "工商管理", "degree": "硕士",
                     "study_type": "unknown", "source_ids": ["S001"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "曹洋_197106",
                    "name_birthplace": "曹洋_",
                    "official_profile_url": "http://www.lsk.gov.cn/qzzc.asp?name=%B2%DC%D1%F3",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "旅顺口区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S011"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "旅顺口区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "辽宁省大连市旅顺口区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "现任区长; 主持区政府全面工作",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共旅顺口区委员会",
                    "title": "区委副书记",
                    "level": "正处级",
                    "location": "辽宁省大连市旅顺口区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "区委副书记、区政府党组书记",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "旅顺口区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省大连市旅顺口区"},
                {"org_id": 1, "name": "中共旅顺口区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省大连市旅顺口区"},
            ],
            "relationships": [
                {"person": "薛雁翔", "person_id": "lvshunkou_薛雁翔",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共旅顺口区委员会/旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008", "S009"]},
                {"person": "马明", "person_id": "lvshunkou_马明",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与区委常委、副区长（党组副书记）",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "迟俊鹏", "person_id": "lvshunkou_迟俊鹏",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "李云虹", "person_id": "lvshunkou_李云虹",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
                {"person": "孙建勇", "person_id": "lvshunkou_孙建勇",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S005"]},
                {"person": "蒲露", "person_id": "lvshunkou_蒲露",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长（兼公安局长）",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006"]},
                {"person": "石德山", "person_id": "lvshunkou_石德山",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区长与挂职副区长",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S007"]},
                {"person": "李井山", "person_id": "lvshunkou_李井山",
                 "relationship_type": "predecessor_successor", "strength": "medium",
                 "evidence": "曹洋接替李井山任旅顺口区区长",
                 "overlap_org": "旅顺口区人民政府",
                 "overlap_period": "交接期未确定",
                 "direction": "undirected", "confidence": "plausible",
                 "source_ids": ["S013"]},
            ],
            "governance_record": [
                {
                    "period": "2026年6月",
                    "domain": "other",
                    "achievement_or_event": "出席区工商联第十二次代表大会",
                    "role_in_event": "区委副书记、区长",
                    "measurable_outcome": "出席会议",
                    "location": "大连市旅顺口区",
                    "confidence": "confirmed",
                    "source_ids": ["S009"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["大连市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以会议出席为主，不足以判断工作风格",
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
                "biggest_gap": "曹洋的完整履历：任区长前的全部职业生涯、具体教育背景（院校/专业）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "曹洋的籍贯和具体毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["曹洋 旅顺口 区长 简历", "曹洋 大连"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "曹洋何时开始担任旅顺口区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["曹洋 任 旅顺口区长", "曹洋 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "曹洋的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["曹洋 工作 经历 大连"],
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
        ("区委书记", "薛雁翔"),
        ("区长", "曹洋"),
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
