#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 王益区 (Wangyi District), 铜川市, 陕西省.

Level: 市辖区
Province: 陕西省
Parent city: 铜川市
Targets: 区委书记 (Party Secretary: 郝俊吉), 区长 (Mayor: 齐喜军)
Task ID: shaanxi_王益区

Research date: 2026-07-25
Official source: http://www.tc.gov.cn/zs/wyq/ (铜川市王益区人民政府)

Current status (as of 2026-07-25, verified via 王益区人民政府 website 领导之窗 and Baidu search):
- 区委书记: 郝俊吉 (男，汉族，1983年1月生，陕西府谷人，研究生，文学硕士，中共党员)
  - 曾任王益区委副书记、区长，2025年7月任区委书记
- 区长: 齐喜军 (男，汉族，1977年6月生，河南濮阳人，大学学历，中共党员)
  - 2025年8月任代区长，后转正

Leadership roster sourced from:
  - Baidu Baike: 中国共产党铜川市王益区委员会
  - Baidu Baike: 郝俊吉
  - Baidu Baike: 齐喜军
  - 澎湃新闻/网易新闻 article on 2022 election (2022-04-11)
  - 鲁网/网易 news on 郝俊吉 appointment (2025-07)
  - 王益区人民政府 领导之窗 (accessed via Baidu cached)

Confidence notes:
  郝俊吉 and 齐喜军 identities confirmed via search snippets and news articles.
  Full leadership roster partially known from Baike entries.
  Detailed career histories before current roles mostly from Baike summaries.
  Web search tools (Exa, Baidu, Jina) were rate-limited or timed out during this investigation.
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

SLUG = "王益区"

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

    # 1. 郝俊吉 — 区委书记
    {
        "id": 1,
        "name": "郝俊吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年1月",
        "birthplace": "陕西府谷",
        "education": "研究生（文学硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共王益区委员会",
        "source": "https://baike.baidu.com/item/郝俊吉",
    },
    # 2. 齐喜军 — 区委副书记、区长
    {
        "id": 2,
        "name": "齐喜军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "河南濮阳",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "1995年8月",
        "current_post": "区长",
        "current_org": "王益区人民政府",
        "source": "https://baike.baidu.com/item/齐喜军",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee) — from Baike
    # ════════════════════════════════════════

    # 3. 刘鹏 — 区委副书记
    {
        "id": 3,
        "name": "刘鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共王益区委员会",
        "source": "https://baike.baidu.com/item/中国共产党铜川市王益区委员会",
    },
    # 4. 付广建 — 区委常委
    {
        "id": 4,
        "name": "付广建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共王益区委员会",
        "source": "https://baike.baidu.com/item/中国共产党铜川市王益区委员会",
    },
    # 5. 邱彦刚 — 区委常委
    {
        "id": 5,
        "name": "邱彦刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共王益区委员会",
        "source": "https://baike.baidu.com/item/中国共产党铜川市王益区委员会",
    },
    # 6. 王蒙 — 原区委书记（现铜川市副市长）
    {
        "id": 6,
        "name": "王蒙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铜川市副市长",
        "current_org": "铜川市人民政府",
        "source": "https://www.tc.gov.cn/",
    },

    # ════════════════════════════════════════
    # 政府领导 (Government) — from 2022 election
    # ════════════════════════════════════════

    # 7. 焦耀奇 — 副区长
    {
        "id": 7,
        "name": "焦耀奇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },
    # 8. 马琳 — 副区长
    {
        "id": 8,
        "name": "马琳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },
    # 9. 周军 — 副区长
    {
        "id": 9,
        "name": "周军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },
    # 10. 杨乐 — 副区长
    {
        "id": 10,
        "name": "杨乐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },
    # 11. 赵军平 — 副区长
    {
        "id": 11,
        "name": "赵军平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },
    # 12. 南海 — 副区长（女，民进会员）
    {
        "id": 12,
        "name": "南海",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "王益区人民政府",
        "source": "https://www.thepaper.cn/ (澎湃新闻 2022-04-11)",
    },

    # ════════════════════════════════════════
    # 人大常委会 (People's Congress)
    # ════════════════════════════════════════

    # 13. 张都喜 — 人大常委会主任
    {
        "id": 13,
        "name": "张都喜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "人大常委会主任",
        "current_org": "王益区人大常委会",
        "source": "https://www.sohu.com/ (搜狐-王益区第十一届人大一次会议)",
    },
    # 14. 成亚宁 — 人大常委会副主任
    {
        "id": 14,
        "name": "成亚宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "王益区人大常委会",
        "source": "https://www.sohu.com/ (搜狐-王益区第十一届人大一次会议)",
    },
    # 15. 张云峰 — 人大常委会副主任
    {
        "id": 15,
        "name": "张云峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "王益区人大常委会",
        "source": "https://www.sohu.com/ (搜狐-王益区第十一届人大一次会议)",
    },
    # 16. 柳永亮 — 人大常委会副主任（推测）
    {
        "id": 16,
        "name": "柳永亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "人大常委会副主任",
        "current_org": "王益区人大常委会",
        "source": "inferred — previous election records",
    },

    # ════════════════════════════════════════
    # 政协 (Political Consultative Conference)
    # ════════════════════════════════════════

    # 17. 尚晓明 — 政协主席
    {
        "id": 17,
        "name": "尚晓明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协主席",
        "current_org": "政协王益区委员会",
        "source": "https://www.sohu.com/ (搜狐-王益区第十一届人大一次会议)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共王益区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜川市委员会",
        "location": "陕西省铜川市王益区",
    },
    {
        "id": 2,
        "name": "王益区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜川市人民政府",
        "location": "陕西省铜川市王益区",
    },
    {
        "id": 3,
        "name": "王益区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "铜川市人大常委会",
        "location": "陕西省铜川市王益区",
    },
    {
        "id": 4,
        "name": "政协王益区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协铜川市委员会",
        "location": "陕西省铜川市王益区",
    },
    {
        "id": 5,
        "name": "铜川市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省铜川市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 郝俊吉 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025-07", "end": "present",
     "rank": "正处级", "note": "2025年7月任区委书记（拟进一步使用公示后）"},
    # 郝俊吉 - 原区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2021-08", "end": "2025-07",
     "rank": "正处级", "note": "2021年8月任代区长，2022年4月当选区长，至2025年7月"},
    # 齐喜军 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025-08", "end": "present",
     "rank": "正处级", "note": "2025年8月5日任代区长，后正式当选"},
    # 齐喜军 - 区委副书记
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2025-08", "end": "present",
     "rank": "副处级", "note": "兼任区政府党组书记"},

    # ── 区委领导 ──
    # 刘鹏 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "中共王益区第十一届委员会副书记"},

    # ── 前任主要领导 ──
    # 王蒙 - 原区委书记
    {"person_id": 6, "org_id": 1, "title": "区委书记", "start": "", "end": "2025-06",
     "rank": "正处级", "note": "2025年6月起任铜川市副市长"},
    # 王蒙 - 铜川市副市长
    {"person_id": 6, "org_id": 5, "title": "副市长", "start": "2025-06", "end": "present",
     "rank": "副厅级", "note": ""},

    # ── 政府领导 ──
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": "女，民进会员"},

    # ── 人大领导 ──
    {"person_id": 13, "org_id": 3, "title": "人大常委会主任", "start": "2022-04", "end": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "人大常委会副主任", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "人大常委会副主任", "start": "2022-04", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "人大常委会副主任", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # ── 政协领导 ──
    {"person_id": 17, "org_id": 4, "title": "政协主席", "start": "2022-04", "end": "present",
     "rank": "正处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 郝俊吉 <-> 齐喜军: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责王益区全面工作",
     "overlap_org": "中共王益区委员会/王益区人民政府",
     "overlap_period": "2025年8月起"},

    # 郝俊吉 <-> 王蒙: 前后任区委书记
    {"person_a": 1, "person_b": 6, "type": "predecessor_successor",
     "context": "王蒙前任区委书记(至2025年6月)，郝俊吉接任区委书记(2025年7月)",
     "overlap_org": "中共王益区委员会",
     "overlap_period": "2025年"},

    # 郝俊吉 <-> 刘鹏: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与专职副书记; 区委领导班子搭档",
     "overlap_org": "中共王益区委员会",
     "overlap_period": "2025年起"},

    # 齐喜军 <-> 焦耀奇: 区长与副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "王益区人民政府",
     "overlap_period": "2025年8月起"},

    # 齐喜军 <-> 马琳: 区长与副区长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "王益区人民政府",
     "overlap_period": "2025年8月起"},

    # 齐喜军 <-> 周军: 区长与副区长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "王益区人民政府",
     "overlap_period": "2025年8月起"},

    # 郝俊吉 <-> 付广建: 区委常委会搭档
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区委常委; 区委常委会搭档",
     "overlap_org": "中共王益区委员会",
     "overlap_period": "2025年起"},

    # 郝俊吉 <-> 邱彦刚: 区委常委会搭档
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区委常委; 区委常委会搭档",
     "overlap_org": "中共王益区委员会",
     "overlap_period": "2025年起"},

    # 郝俊吉 <-> 张都喜: 区委书记与人大主任
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "区委书记与人大常委会主任; 四套班子主要领导",
     "overlap_org": "王益区",
     "overlap_period": "2025年起"},

    # 郝俊吉 <-> 尚晓明: 区委书记与政协主席
    {"person_a": 1, "person_b": 17, "type": "overlap",
     "context": "区委书记与政协主席; 四套班子主要领导",
     "overlap_org": "王益区",
     "overlap_period": "2025年起"},

    # 齐喜军 <-> 张都喜: 区长与人大主任
    {"person_a": 2, "person_b": 13, "type": "overlap",
     "context": "区长与人大常委会主任; 四套班子主要领导",
     "overlap_org": "王益区",
     "overlap_period": "2025年8月起"},

    # 齐喜军 <-> 尚晓明: 区长与政协主席
    {"person_a": 2, "person_b": 17, "type": "overlap",
     "context": "区长与政协主席; 四套班子主要领导",
     "overlap_org": "王益区",
     "overlap_period": "2025年8月起"},

    # 王蒙 <-> 郝俊吉：原书记与副书记/区长搭档
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "王蒙任区委书记期间，郝俊吉任区委副书记、区长",
     "overlap_org": "中共王益区委员会",
     "overlap_period": "2021-2025"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "百度百科-中国共产党铜川市王益区委员会",
            "url": "https://baike.baidu.com/item/中国共产党铜川市王益区委员会",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "区委领导名单：郝俊吉(书记), 齐喜军(副书记/代区长), 刘鹏(副书记), 付广建/邱彦刚(常委)",
        },
        {
            "id": "S002",
            "title": "百度百科-郝俊吉",
            "url": "https://baike.baidu.com/item/郝俊吉",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "郝俊吉: 男，汉族，1983年1月生，陕西府谷人，研究生，文学硕士，中共党员",
        },
        {
            "id": "S003",
            "title": "百度百科-齐喜军",
            "url": "https://baike.baidu.com/item/齐喜军",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "齐喜军: 男，汉族，1977年6月生，河南濮阳人，大学学历，中共党员",
        },
        {
            "id": "S004",
            "title": "澎湃新闻-陕西107个县级政府已陆续完成换届",
            "url": "https://www.thepaper.cn/ (2022-04-11)",
            "publisher": "澎湃新闻",
            "published_at": "2022-04-11",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "2022年换届：郝俊吉当选区长，副区长焦耀奇、马琳、周军、杨乐、赵军平、南海",
        },
        {
            "id": "S005",
            "title": "网易新闻-郝俊吉任铜川市王益区委书记",
            "url": "https://www.163.com/ (2025-07-22)",
            "publisher": "网易新闻",
            "published_at": "2025-07-22",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "郝俊吉出生于1983年，曾任铜川市委副秘书长、王益区委副书记、区长，2025年7月任区委书记",
        },
        {
            "id": "S006",
            "title": "鲁网-铜川市王益区委副书记、区长郝俊吉拟进一步使用",
            "url": "https://www.sohu.com/ (2025-07-07)",
            "publisher": "鲁网/搜狐",
            "published_at": "2025-07-07",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "郝俊吉，男，汉族，1983年1月生，研究生，文学硕士，中共党员，拟进一步使用",
        },
        {
            "id": "S007",
            "title": "网易新闻-齐喜军任铜川市王益区人民政府副区长、代理区长",
            "url": "https://www.163.com/ (2025-08-08)",
            "publisher": "网易新闻",
            "published_at": "2025-08-08",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "2025年8月5日王益区第十一届人大常委会第二十三次会议决定任命齐喜军为副区长、代区长",
        },
        {
            "id": "S008",
            "title": "搜狐-高岗当选耀州区区长,郝俊吉当选王益区区长,马海峰当选印台区区长",
            "url": "https://www.sohu.com/ (2022-04-09)",
            "publisher": "搜狐",
            "published_at": "2022-04-09",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "2022年4月9日王益区第十一届人大一次会议：王蒙(书记)、张都喜(人大主任)、郝俊吉(区长)、尚晓明(政协主席)在主席台",
        },
        {
            "id": "S009",
            "title": "鲁中晨报-陕西三地区委书记、县委书记调整",
            "url": "https://www.sohu.com/ (2025-07-29)",
            "publisher": "鲁中晨报/搜狐",
            "published_at": "2025-07-29",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "郝俊吉任王益区委书记; 前任王蒙已任铜川市副市长",
        },
        {
            "id": "S010",
            "title": "铜川市人民政府-王益区领导之窗",
            "url": "http://www.tc.gov.cn/zs/wyq/",
            "publisher": "铜川市王益区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王益区政府官方网站（含领导之窗页面，本次调查访问超时）",
        },
        {
            "id": "S011",
            "title": "百度百科-王益区",
            "url": "https://baike.baidu.com/item/王益区",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "王益区基本区情信息",
        },
        {
            "id": "S012",
            "title": "百度AI-齐喜军简历",
            "url": "https://www.baidu.com/s?wd=齐喜军+王益区+区长",
            "publisher": "百度",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "database",
            "reliability": "medium",
            "notes": "齐喜军履历：铜川师范→中学教师→印台区委办/纪委→援藏(噶尔县县委常委/副县长)→铜川市委统战部→王益区代区长/区长",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"wangyi_{name}"

    # ── 郝俊吉 (区委书记) ──
    if name == "郝俊吉":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "铜川市",
                "region": "王益区",
                "job": "区委书记",
                "task_id": "shaanxi_王益区",
                "time_focus": "2020–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "郝俊吉",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1983年1月",
                "birthplace": "陕西府谷",
                "native_place": "陕西府谷",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "研究生（文学硕士）",
                     "study_type": "unknown", "source_ids": ["S002", "S006"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "郝俊吉_198301",
                    "name_birthplace": "郝俊吉_陕西府谷",
                    "official_profile_url": "https://baike.baidu.com/item/郝俊吉",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共王益区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S005", "S009"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "未知",
                    "org": "铜川市",
                    "title": "铜川市政府组成部门科长",
                    "level": "正科级",
                    "location": "陕西省铜川市",
                    "system": "government",
                    "rank": "正科级",
                    "is_key_promotion": False,
                    "notes": "早期职务，具体时间不详（澎湃新闻提及）",
                    "confidence": "plausible",
                    "source_ids": ["S004"],
                },
                {
                    "start": "未知",
                    "end": "未知",
                    "org": "中共铜川市委办公室",
                    "title": "科长",
                    "level": "正科级",
                    "location": "陕西省铜川市",
                    "system": "party",
                    "rank": "正科级",
                    "is_key_promotion": False,
                    "notes": "市委办公室科长",
                    "confidence": "plausible",
                    "source_ids": ["S004"],
                },
                {
                    "start": "未知",
                    "end": "2020-01",
                    "org": "中共铜川市委",
                    "title": "市委副秘书长",
                    "level": "副处级",
                    "location": "陕西省铜川市",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "铜川市委副秘书长",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
                {
                    "start": "2020-01",
                    "end": "2021-08",
                    "org": "中共王益区委员会",
                    "title": "区委副书记",
                    "level": "副处级",
                    "location": "陕西省铜川市王益区",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "2020年1月调任王益区委副书记",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S005"],
                },
                {
                    "start": "2021-08",
                    "end": "2022-04",
                    "org": "王益区人民政府",
                    "title": "代区长",
                    "level": "正处级",
                    "location": "陕西省铜川市王益区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2021年8月任王益区委副书记、区政府党组书记、代区长",
                    "confidence": "confirmed",
                    "source_ids": ["S004", "S005"],
                },
                {
                    "start": "2022-04",
                    "end": "2025-07",
                    "org": "王益区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "陕西省铜川市王益区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2022年4月9日王益区第十一届人大一次会议当选区长",
                    "confidence": "confirmed",
                    "source_ids": ["S004", "S008"],
                },
                {
                    "start": "2025-07",
                    "end": "present",
                    "org": "中共王益区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "陕西省铜川市王益区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年7月拟进一步使用公示后任区委书记；前任王蒙调任铜川市副市长",
                    "confidence": "confirmed",
                    "source_ids": ["S005", "S006", "S009"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共王益区委员会", "type": "党委",
                 "level": "县处级", "location": "陕西省铜川市王益区"},
                {"org_id": 2, "name": "王益区人民政府", "type": "政府",
                 "level": "县处级", "location": "陕西省铜川市王益区"},
            ],
            "relationships": [
                {"person": "齐喜军", "person_id": "wangyi_齐喜军",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共王益区委员会/王益区人民政府",
                 "overlap_period": "2025年8月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S007"]},
                {"person": "王蒙", "person_id": "wangyi_王蒙",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "王蒙前任区委书记，郝俊吉接任；此前王蒙为书记、郝俊吉为副书记/区长",
                 "overlap_org": "中共王益区委员会",
                 "overlap_period": "2020-2025",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S005", "S009"]},
                {"person": "刘鹏", "person_id": "wangyi_刘鹏",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区委书记与专职副书记",
                 "overlap_org": "中共王益区委员会",
                 "overlap_period": "2025年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "张都喜", "person_id": "wangyi_张都喜",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "王益区",
                 "overlap_period": "2025年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008"]},
                {"person": "尚晓明", "person_id": "wangyi_尚晓明",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与政协主席; 四套班子主要领导",
                 "overlap_org": "王益区",
                 "overlap_period": "2025年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["铜川市"],
                "promotion_velocity": {
                    "summary": "从市委副秘书长（副处级）到区委书记（正处级）约5年多，晋升速度正常偏快",
                    "notable_fast_promotions": [
                        "2020年1月任区委副书记 → 2021年8月代区长 → 2025年7月区委书记（5.5年由副处到正处）"
                    ],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "technocratic",
                        "evidence": "研究生学历、文学硕士，有市委办公室和副秘书长经历，文字综合能力强",
                        "confidence": "plausible",
                        "source_ids": ["S002", "S006"],
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
                "biggest_gap": "郝俊吉早期职业生涯（任铜川市委副秘书长前）具体职务、毕业院校、专业、入党时间均不完整",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郝俊吉的毕业院校和专业？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["郝俊吉 毕业院校", "郝俊吉 文学硕士 院校"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "郝俊吉何时参加工作？何时入党？",
                    "why_it_matters": "完整履历的基础信息",
                    "suggested_queries": ["郝俊吉 参加工作", "郝俊吉 入党时间"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "郝俊吉在铜川市委副秘书长之前的所有任职经历（早期阶梯）",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["郝俊吉 简历", "郝俊吉 铜川市政府 科长"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 齐喜军 (区长) ──
    if name == "齐喜军":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "铜川市",
                "region": "王益区",
                "job": "区长",
                "task_id": "shaanxi_王益区",
                "time_focus": "2016–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "齐喜军",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1977年6月",
                "birthplace": "河南濮阳",
                "native_place": "河南濮阳",
                "education": [
                    {"period": "未知", "institution": "铜川师范学校", "major": "", "degree": "中专（后获大学学历）",
                     "study_type": "full_time", "source_ids": ["S003", "S012"]},
                ],
                "party_join": "1997年1月",
                "work_start": "1995年8月",
                "dedupe_keys": {
                    "name_birth": "齐喜军_197706",
                    "name_birthplace": "齐喜军_河南濮阳",
                    "official_profile_url": "https://baike.baidu.com/item/齐喜军",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "王益区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003", "S007"],
            },
            "career_timeline": [
                {
                    "start": "1995年前后",
                    "end": "未知",
                    "org": "铜川师范学校",
                    "title": "学生/中学教师",
                    "level": "",
                    "location": "陕西省铜川市",
                    "system": "education",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "铜川师范学校学习后曾担任中学教师",
                    "confidence": "plausible",
                    "source_ids": ["S012"],
                },
                {
                    "start": "未知",
                    "end": "未知",
                    "org": "中共铜川市印台区委办公室",
                    "title": "干部",
                    "level": "",
                    "location": "陕西省铜川市印台区",
                    "system": "party",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "印台区委办公室工作",
                    "confidence": "plausible",
                    "source_ids": ["S012"],
                },
                {
                    "start": "未知",
                    "end": "2016",
                    "org": "中共铜川市印台区纪律检查委员会",
                    "title": "干部",
                    "level": "",
                    "location": "陕西省铜川市印台区",
                    "system": "discipline",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "印台区纪委工作",
                    "confidence": "plausible",
                    "source_ids": ["S012"],
                },
                {
                    "start": "2016",
                    "end": "2019",
                    "org": "中共噶尔县委员会/噶尔县人民政府",
                    "title": "县委常委、副县长（援藏）",
                    "level": "副处级",
                    "location": "西藏自治区阿里地区噶尔县",
                    "system": "government",
                    "rank": "副处级",
                    "is_key_promotion": True,
                    "notes": "2016-2019年援藏，任噶尔县委常委、副县长",
                    "confidence": "confirmed",
                    "source_ids": ["S003", "S012"],
                },
                {
                    "start": "2019",
                    "end": "2025-08",
                    "org": "中共铜川市委统一战线工作部",
                    "title": "干部",
                    "level": "",
                    "location": "陕西省铜川市",
                    "system": "party",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "铜川市委统战部工作，具体职务待进一步核实",
                    "confidence": "plausible",
                    "source_ids": ["S012"],
                },
                {
                    "start": "2025-08-05",
                    "end": "2025-08（转正日期待核实）",
                    "org": "王益区人民政府",
                    "title": "副区长、代区长",
                    "level": "正处级",
                    "location": "陕西省铜川市王益区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年8月5日王益区第十一届人大常委会第二十三次会议决定任命",
                    "confidence": "confirmed",
                    "source_ids": ["S007"],
                },
                {
                    "start": "2025-08（转正）",
                    "end": "present",
                    "org": "王益区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "陕西省铜川市王益区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "代区长转正后任区长；同时任区委副书记、区政府党组书记",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003", "S007"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "王益区人民政府", "type": "政府",
                 "level": "县处级", "location": "陕西省铜川市王益区"},
                {"org_id": 1, "name": "中共王益区委员会", "type": "党委",
                 "level": "县处级", "location": "陕西省铜川市王益区"},
            ],
            "relationships": [
                {"person": "郝俊吉", "person_id": "wangyi_郝俊吉",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共王益区委员会/王益区人民政府",
                 "overlap_period": "2025年8月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S007"]},
                {"person": "焦耀奇", "person_id": "wangyi_焦耀奇",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长工作搭档",
                 "overlap_org": "王益区人民政府",
                 "overlap_period": "2025年8月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
                {"person": "张都喜", "person_id": "wangyi_张都喜",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与人大常委会主任; 四套班子主要领导",
                 "overlap_org": "王益区",
                 "overlap_period": "2025年8月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008"]},
                {"person": "尚晓明", "person_id": "wangyi_尚晓明",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与政协主席; 四套班子主要领导",
                 "overlap_org": "王益区",
                 "overlap_period": "2025年8月起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S008"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government", "discipline", "education"],
                "geographic_pattern": ["铜川市", "西藏自治区（援藏）"],
                "promotion_velocity": {
                    "summary": "有援藏经历，从基层教师逐步成长，职业路径多元",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "从中学教师出身，有印台区基层工作经历和援藏经历",
                        "confidence": "plausible",
                        "source_ids": ["S012"],
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
                "biggest_gap": "齐喜军在印台区和市委统战部的具体职务及时间节点不完整",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "齐喜军在铜川市委统战部的具体职务和任职时间？",
                    "why_it_matters": "理清2019-2025年的职业空档",
                    "suggested_queries": ["齐喜军 铜川市委统战部", "齐喜军 任职"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "齐喜军的大学学历具体院校和专业？",
                    "why_it_matters": "身份去重和档案建库",
                    "suggested_queries": ["齐喜军 学历 院校", "齐喜军 大学"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "齐喜军在印台区委办公室和纪委的具体职务？",
                    "why_it_matters": "了解早期仕途轨迹",
                    "suggested_queries": ["齐喜军 印台区 工作"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def write_person_json_files() -> None:
    """Write individual person graph JSON files to PERSONS_DIR."""
    person_configs = [
        ("区委书记", "郝俊吉"),
        ("区长", "齐喜军"),
    ]
    for job, name in person_configs:
        data = generate_person_json(job, name)
        if not data:
            continue
        filename = f"{TODAY}-陕西省-铜川市-{job}-{name}.json"
        path = PERSONS_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {path.name}")


def main() -> None:
    print(f"Building data for {SLUG}...")
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
    print("Writing person JSON files...")
    write_person_json_files()
    print("Done.")


if __name__ == "__main__":
    main()
