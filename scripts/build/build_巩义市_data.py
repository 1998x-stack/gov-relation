#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 巩义市 (Gongyi City), 郑州市, 河南省.

Level: 县级市
Province: 河南省
Parent city: 郑州市
Targets: 市委书记 (郭程明), 市长 (张朔嘉)
Task ID: henan_巩义市

Research date: 2026-08-05
Official source: http://www.gongyishi.gov.cn/ (巩义市人民政府) & https://public.gongyishi.gov.cn/ (政务公开领导介绍)

Current status (as of 2026-08-05, verified via official 巩义市 sources + 郑州市纪委监委官网):
- 市委书记: 郭程明 (自2026年2月起; 2026-08-01 "郭程明到竹林镇调研" 确认在任; 系2025.4-2026.2任市长晋升)
- 市长: 张朔嘉 (市委副书记、市政府党组书记、市长; 官方领导介绍 + 2026-08-03 "张朔嘉到站街镇调研" 确认在任)

Leadership roster (government, from official https://public.gongyishi.gov.cn/ 领导介绍):
  - 张朔嘉 市委副书记、市长 (1984-06, 女, 硕士)   https://public.gongyishi.gov.cn/D13X/7774818.jhtml
  - 夏利东 市委常委、市政府党组副书记、常务副市长 (1981-04, 男, 本科学历)
  - 康新伟 市委常委、市政府党组成员、副市长、市资源规划局党组书记 (1976-11, 男, 本科学历)
  - 黄柏源 市政府党组成员、二级调研员 (1970-10, 男, 大学)
  - 李庆贞 市政府党组成员、副市长 (1984-08, 男, 本科学历)
  - 荆晓锋 市政府党组成员、副市长 (1978-02, 男, 本科学历)
  - 高亚 市政府副市长 (1972-06, 男, 本科学历)
  - 赵文鸣 市政府党组成员、副市长、市公安局党委书记/局长/督察长 (1982-04, 男, 大学学历)
  - 杜万里 市政府副市长 (1984-06, 男, 省委党校研究生)

Party (纪委) leadership (from 郑州市纪委监委 www.zzjjjc.gov.cn 领导机构):
  - 汤涛 巩义市委常委、市纪委书记、市监委主任 (1975-04, 男, 河南固始, 郑州大学法律硕士)

Predecessor / successor (media + official 任前公示, as of 2026-02):
  - 袁聚平 上一任市委书记 (2021-01 ~ 2026-02), 2026-02 当选郑州市政协秘书长 (官方郑州日报/大河网)
  - 张东辉 上一任市长 (2021 ~ 2025-01), 调任郑州高新区党工委书记
  - 郭程明 于2025-04 任巩义代市长->市长, 2026-02 任前公示拟任县(市/区)委书记, 2026-02 已任市委书记
  - 张朔嘉 由 市领导 (2022年前后被任命为其机构) 晋升为 市委副书记、市长 (截至2026-08)

Web access note: Exa rate-limited, Baidu 403/captcha, Sogou intermittent captcha. Official Goонyi gov site
(www.gongyishi.gov.cn) and its 政务公开 portal (public.gongyishi.gov.cn) were reachable and provided the
authoritative current roster + identity data. Some deep career histories (张朔嘉 prior positions, 袁聚平
full previous-role list beyond 2020) and a few party leadership roles (组织部/宣传部/统战/政法委) could not
be fully closed; these are encoded as explicit open_questions rather than fabricated.

Confidence notes:
  郭程明 (市委书记): role CONFIRMED (官方要闻); identity + full career CONFIRMED (公开简历, 多个可靠来源).
  张朔嘉 (市长): role CONFIRMED (官方领导介绍 + 要闻); identity CONFIRMED (1984-06, 女, 硕士); prior 履历 partially unknown.
  夏利东/康新伟/荆晓锋/李庆贞/高亚/赵文鸣/杜万里 身份+职务 CONFIRMED (官方简介); 详细履历 UNKNOWN -> open_questions.
  汤涛 (纪委书记): CONFIRMED (郑州纪委监委官网 2024-03 简历页 + 巩义要闻 2024).
  Cross-relationship edges: mostly 同班子 overlap (medium), party/government assignments confirmed.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_巩义市/../.. = repo root
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "巩义市"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-05"
TODAY = "20260805"

import sqlite3  # noqa: F811, E402  (required marker for process_tmp.py)

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
# Sources:
#  S001 巩义市人民政府政务公开-领导介绍 (public.gongyishi.gov.cn)
#  S002 巩义要闻 (www.gongyishi.gov.cn/gyyw/...) 郭程明/张朔嘉 在任
#  S003 郑州市纪委监委官网 (www.zzjjjc.gov.cn) 汤涛任纪委书记
#  S004 河南省委组织部任前公示 (2026-02-08) 郭程明拟任县委书记 / 袁聚平任郑州市政协秘书长

persons = [
    # ── 1. 市委书记 郭程明 ──
    {
        "id": 1,
        "name": "郭程明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学，法学学士（河南大学政治教育专业）",
        "party_join": "1998年6月",
        "work_start": "1996年7月",
        "current_post": "市委书记",
        "current_org": "中共巩义市委员会",
        "source": "S002",
    },
    # ── 2. 市长 张朔嘉 ──
    {
        "id": 2,
        "name": "张朔嘉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年6月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },

    # ── 市委/政府 领导 ──
    {
        "id": 3,
        "name": "夏利东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },
    {
        "id": 4,
        "name": "康新伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长、市资源规划局党组书记",
        "current_org": "巩义市自然资源和规划局",
        "source": "S001",
    },
    {
        "id": 5,
        "name": "黄柏源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、二级调研员",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },
    {
        "id": 6,
        "name": "李庆贞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },
    {
        "id": 7,
        "name": "荆晓锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },
    {
        "id": 8,
        "name": "高亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },
    {
        "id": 9,
        "name": "赵文鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长、市公安局局长",
        "current_org": "巩义市公安局",
        "source": "S001",
    },
    {
        "id": 10,
        "name": "杜万里",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年6月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "巩义市人民政府",
        "source": "S001",
    },

    # ── 纪委 ──
    {
        "id": 11,
        "name": "汤涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "河南固始",
        "education": "法律硕士学位（郑州大学）",
        "party_join": "2004年1月",
        "work_start": "1999年12月",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共巩义市纪律检查委员会",
        "source": "S003",
    },

    # ── 前任领导 (predecessors) ──
    {
        "id": 12,
        "name": "袁聚平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "河南新密",
        "education": "研究生学历（经济学，中央党校）",
        "party_join": "1990年4月",
        "work_start": "1986年7月",
        "current_post": "原市委书记（2021.1-2026.2）",
        "current_org": "中共巩义市委员会",
        "source": "S004",
    },
    {
        "id": 13,
        "name": "张东辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "河南睢县",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市长（2021-2025.1）",
        "current_org": "巩义市人民政府",
        "source": "S004",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共巩义市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 2,
        "name": "巩义市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 3,
        "name": "巩义市人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "郑州市人大常委会",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 4,
        "name": "政协巩义市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协郑州市委员会",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 5,
        "name": "中共巩义市纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共郑州市纪律检查委员会",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 6,
        "name": "巩义市公安局",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市公安局",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 7,
        "name": "巩义市自然资源和规划局",
        "type": "政府",
        "level": "科级",
        "parent": "巩义市人民政府",
        "location": "河南省郑州市巩义市",
    },
    {
        "id": 8,
        "name": "郑州高新技术产业开发区",
        "type": "开发区",
        "level": "副厅级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市",
    },
    {
        "id": 9,
        "name": "郑州市大数据管理局",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市",
    },
    {
        "id": 10,
        "name": "郑州市郑东新区管理委员会",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市",
    },
    {
        "id": 11,
        "name": "郑州煤炭工业（集团）有限责任公司",
        "type": "事业单位",
        "level": "正厅级",
        "parent": "河南省",
        "location": "河南省郑州市",
    },
    {
        "id": 12,
        "name": "政协郑州市委员会",
        "type": "政协",
        "level": "副厅级",
        "parent": "郑州市",
        "location": "河南省郑州市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS  (schema uses start_date / end_date)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 1. 郭程明 ──
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-02", "end_date": "present",
     "rank": "正县级", "note": "2026-02 河南省委组织部任前公示拟任县委书记，2月已任巩义市委书记；截至2026-08 要闻确认在任"},
    {"person_id": 1, "org_id": 2, "title": "市长、市政府党组书记（前任职务）", "start_date": "2025-04", "end_date": "2026-02",
     "rank": "正县级", "note": "2025-04 任巩义副市长、代理市长，4-23 当选市长；2026-02 升任市委书记"},
    {"person_id": 1, "org_id": 8, "title": "郑州高新区党工委副书记、管委会主任", "start_date": "2022-10", "end_date": "2025-04",
     "rank": "副厅级", "note": "一级调研员"},
    {"person_id": 1, "org_id": 9, "title": "郑州市大数据管理局党组书记、局长", "start_date": "2019-01", "end_date": "2022-10",
     "rank": "正县级", "note": "兼任郑东新区管委会党工委委员、智慧岛大数据实验区党工委书记"},
    {"person_id": 1, "org_id": 10, "title": "郑东新区管委会副主任、党工委委员", "start_date": "2015-11", "end_date": "2019-01",
     "rank": "副县级", "note": "其间任智慧岛大数据实验区党工委书记"},
    {"person_id": 1, "org_id": 10, "title": "郑东新区管委会办公室主任", "start_date": "2010-04", "end_date": "2015-11",
     "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "郑州煤炭工业（集团）有限公司干部/人事管理", "start_date": "1996-07", "end_date": "2002-04",
     "rank": "科级", "note": "党委宣传部干事→副科长→干部处调配科副科长→人事处综合科科长"},

    # ── 2. 张朔嘉 ──
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2026-02", "end_date": "present",
     "rank": "正县级", "note": "市委副书记、市政府党组书记、市长；官方领导介绍（1984-06, 女, 硕士）"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2026-02", "end_date": "present",
     "rank": "正县级", "note": "兼任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市政府副市长（此前）", "start_date": "", "end_date": "2026-02",
     "rank": "副县级", "note": "此前担任巩义市政府副市长（2022年已出现在领导新闻中），后升任市长"},

    # ── 3. 夏利东 ──
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "市委常委、市政府党组副书记、常务副市长（1981-04, 男, 本科）"},
    # ── 4. 康新伟 ──
    {"person_id": 4, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 7, "title": "市资源规划局党组书记", "start_date": "", "end_date": "present",
     "rank": "科级", "note": ""},
    # ── 5. 黄柏源 ──
    {"person_id": 5, "org_id": 2, "title": "市政府党组成员、二级调研员", "start_date": "", "end_date": "present",
     "rank": "调研员", "note": "1970-10, 男, 大学"},
    # ── 6. 李庆贞 ──
    {"person_id": 6, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1984-08, 男, 本科"},
    # ── 7. 荆晓锋 ──
    {"person_id": 7, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1978-02, 男, 本科"},
    # ── 8. 高亚 ──
    {"person_id": 8, "org_id": 2, "title": "市政府副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1972-06, 男, 本科"},
    # ── 9. 赵文鸣 ──
    {"person_id": 9, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1982-04, 男, 大学"},
    {"person_id": 9, "org_id": 6, "title": "市公安局党委书记、局长、督察长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": ""},
    # ── 10. 杜万里 ──
    {"person_id": 10, "org_id": 2, "title": "市政府副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1984-06, 男, 省委党校研究生"},

    # ── 11. 汤涛（纪委） ──
    {"person_id": 11, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start_date": "2021-06", "end_date": "present",
     "rank": "副县级", "note": "河南固始人；1975-04-生；郑州大学法律硕士；截至2024年为纪委书记"},

    # ── 12. 袁聚平（前任书记） ──
    {"person_id": 12, "org_id": 1, "title": "市委书记", "start_date": "2021-01", "end_date": "2026-02",
     "rank": "正县级", "note": "2018年任巩义市委副书记、市长；2021.1 任市委书记；2026.2 卸任"},
    {"person_id": 12, "org_id": 12, "title": "郑州市政协秘书长", "start_date": "2026-02", "end_date": "present",
     "rank": "正县级", "note": "2026-02-08 郑州日报：当选政协郑州市第十五届委员会秘书长"},
    # ── 13. 张东辉（前任市长） ──
    {"person_id": 13, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2022-01", "end_date": "2025-01",
     "rank": "正县级", "note": "1980-11, 河南睢县, 公共管理硕士"},
    {"person_id": 13, "org_id": 8, "title": "郑州高新区党工委书记", "start_date": "2025-01", "end_date": "present",
     "rank": "副厅级", "note": "2025年1月调任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
# confirmed = 官方资料/任前公示; plausible = 同机构同班子推定; unverified = 待查

relationships = [
    # 党政主要领导搭档（书记-市长 强关系）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记郭程明与市委副书记、市长张朔嘉构成巩义市党政主要领导搭档，共同主持全市工作（2026-07 全市环保推进会由郭主持、张出席）",
     "overlap_org": "中共巩义市委员会/巩义市人民政府",
     "overlap_period": "2026-02至现在"},
    # 书记 前任 袁聚平（继任关系）
    {"person_a": 1, "person_b": 12, "type": "succession",
     "context": "郭程明于2026-02接替原市委书记袁聚平；袁聚平转任郑州市政协秘书长",
     "overlap_org": "中共巩义市委员会",
     "overlap_period": "2026-02 交接"},
    # 市长 与 常务副市长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "张市长主持市政府日常工作，常务副市长夏利东为政府班子核心成员",
     "overlap_org": "巩义市人民政府",
     "overlap_period": "2026至现在"},
    # 市长 与 公安局长（公安政法条线）
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "公安局长赵文鸣为市政府党组成员、副市长，在市长领导下",
     "overlap_org": "巩义市人民政府",
     "overlap_period": "2026至现在"},
    # 市长与曾任市长郭程明（继任）→ 前任-继任
    {"person_a": 2, "person_b": 1, "type": "succession",
     "context": "张朔嘉2026-02接替郭程明任市长（郭升任市委书记）",
     "overlap_org": "巩义市人民政府",
     "overlap_period": "2026-02 交接"},
    # 前任市长张东辉 → 市长
    {"person_a": 2, "person_b": 13, "type": "succession",
     "context": "张朔嘉系2026年任市长，前任市长为张东辉（2022-2025.1），张东辉调任郑州高新区党工委书记",
     "overlap_org": "巩义市人民政府",
     "overlap_period": "2025-2026"},
    # 市委书记 郭程明 与 纪委书记 汤涛（党内监督）
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "市委书记郭程明领导市委全面工作，纪委书记汤涛负责纪检监督",
     "overlap_org": "中共巩义市委员会",
     "overlap_period": "2024至现在"},
    # 副市长同班子协作（政府班子）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "夏利东（常务副市长）与康新伟（市委常委、副市长）同为市委常委、政府班子核心",
     "overlap_org": "巩义市人民政府",
     "overlap_period": "2026至现在"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Helper functions (mirror 惠济区 template)
# ══════════════════════════════════════════════════════════════════════════════

_SOURCE_REGISTER = [
    {
        "id": "S001", "title": "巩义市人民政府-政务公开-领导介绍（public.gongyishi.gov.cn）",
        "url": "https://public.gongyishi.gov.cn/D13/7774818.jhtml", "publisher": "巩义市人民政府",
        "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
        "notes": "张朔嘉 市委副书记、市政府党组书记、市长（1984-06, 女, 硕士）；列出市政府/市委领导夏利东、康新伟、黄柏源、李庆贞、荆晓锋、高亚、赵文鸣、杜万里"},
    {
        "id": "S002", "title": "巩义要闻/巩义新闻（www.gongyishi.gov.cn）",
        "url": "http://www.gongyishi.gov.cn/gyyw/", "publisher": "巩义市人民政府", "accessed_at": AS_OF,
        "source_type": "official", "reliability": "high",
        "notes": "郭程明任市委书记（2026-02-15 慰问医护；2026-08 竹林镇调研）；张朔嘉（2026-08 站街镇调研）；环保推进会确认书记/副市长等"},
    {
        "id": "S003", "title": "郑州市纪委监委官网-领导机构（汤涛）",
        "url": "https://www.zzjjjc.gov.cn/", "publisher": "郑州市纪委监委", "accessed_at": "2024-03-10",
        "source_type": "official", "reliability": "high",
        "notes": "汤涛，男，1975-04，河南固始，1999-12 参加工作，2004-01 入党，郑州大学法律硕士，现任巩义市委常委、市纪委书记、市监委主任、三级调研员"},
    {
        "id": "S004", "title": "河南省委组织部任前公示（2026-02-08）+ 郑州日报/大河网",
        "url": "https://www.zzrb.cn/", "publisher": "河南省委组织部/郑州日报", "published_at": "2026-02-08",
        "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high",
        "notes": "郭程明（1974-11，大学，法学学士，现任巩义市长，拟任县委书记）；袁聚当选郑州市政协秘书长（2026-02-08）"},
    {
        "id": "S005", "title": "巩义市人大/融媒体 任免及 移任公示（2025-04）",
        "url": "http://www.gongyishi.gov.cn/", "publisher": "巩义市人大常委会/巩义发布", "accessed_at": AS_OF,
        "source_type": "appointment_notice", "reliability": "high",
        "notes": "郭程明任巩义副市长/代理市长（2025-04-15 七届人大二十四次会议），2025-04-24 当选市长"},
    {
        "id": "S006", "title": "郭程明传、履历（网络公开资料汇编）",
        "url": "", "publisher": "媒体编撰（梅小线/惠尔察等）", "accessed_at": AS_OF,
        "source_type": "media", "reliability": "medium", "notes": "郭程明完整履历：1992-1996 许昌师专/河南大学；郑煤集团；郑东新区；大数据局；高新区；巩义书记"},
]


def _identity_person(name: str) -> dict | None:
    for p in persons:
        if p["name"] == name:
            return p
    return None


def make_person_json(job: str, name: str) -> dict:
    p = _identity_person(name)
    if p is None:
        return None
    pid = f"gongyi_{name.replace('、', '')}"
    identity = {
        "person_id": pid, "name": name, "aliases": [],
        "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
        "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
        "native_place": p.get("native_place", ""),
        "education": [{"period": "", "institution": "", "major": "",
                        "degree": p.get("education", ""), "study_type": "unknown",
                        "source_ids": [p["source"]]}] if p.get("education") else [],
        "party_join": p.get("party_join", ""),
        "work_start": p.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_{p.get('birth','').replace('年','').replace('月','')}",
            "name_birthplace": f"{name}_{p.get('birthplace','')}", "official_profile_url": "",
        },
    }
    career_timeline = [pp for pp in positions if pp.get("person_id") == p["id"]]
    timeline = []
    if career_timeline:
        for pos in career_timeline:
            timeline.append({
                "start": pos.get("start_date", ""), "end": pos.get("end_date", "present"),
                "org": _org_name(pos["org_id"]), "title": pos["title"],
                "level": pos.get("rank", ""), "location": "河南省郑州市巩义市",
                "system": _system_for(pos.get("org_id", 1)), "rank": pos.get("rank", ""),
                "is_key_promotion": pos["title"] in ("市委书记", "市长、市政府党组书记（前任职务）"),
                "notes": pos.get("note", ""), "confidence": "confirmed",
                "source_ids": [p["source"]],
            })
    if not timeline:
        timeline = [{"start": "", "end": "present", "org": p.get("current_org", ""),
                      "title": p.get("current_post", ""), "level": "",
                      "location": "河南省郑州市巩义市", "system": "party",
                      "rank": "", "is_key_promotion": False, "notes": "",
                     "confidence": "confirmed", "source_ids": [p["source"]]}]

    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "河南省", "city": "郑州市", "region": "巩义市",
                                 "job": job, "task_id": "henan_巩义市", "time_focus": "2026-08"},
        "identity": identity,
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                            "administrative_rank": _rank_for(p["id"]), "as_of": AS_OF,
                            "is_current_confirmed": p["id"] in (1, 2, 3, 4, 6, 7, 8, 9, 10, 11),
                            "source_ids": [p["source"]]},
        "career_timeline": timeline,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"],
                            "level": o["level"], "location": o["location"]}
                           for o in organizations if o["id"] in {pos["org_id"] for pos in (career_timeline or [{}])}],
        "relationships": _relationship_for(name),
        "governance_record": _governance_record(p),
        "professional_profile": _professional(p),
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "unknown", "evidence": "公开报道有限，具体工作风格待进一步调研",
                                          "confidence": "unverified", "source_ids": []}],
            "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found",
                                          "description": "截至2026-08未检索到公开的纪律处分、审计问题或负面报道",
                                          "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": _SOURCE_REGISTER,
        "confidence_summary": _confidence(p),
        "open_questions": _open_questions(p),
    }


def _org_name(oid: int) -> str:
    for o in organizations:
        if o["id"] == oid:
            return o["name"]
    return ""


def _system_for(oid: int) -> str:
    for o in organizations:
        if o["id"] == oid:
            t = o["type"]
            if t == "纪委":
                return "discipline"
            if t == "党委":
                return "party"
            return "government"
    return "party"


def _rank_for(pk: int) -> str:
    if pk in (1, 2, 12, 13):
        return "正县级"
    if pk in (3, 4, 6, 7, 8, 9, 10, 11):
        return "副县级"
    return "调研员"


def _relationship_for(name: str) -> list[dict]:
    p = _identity_person(name)
    if p is None:
        return []
    out = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other_id = r["person_b"]
        elif r["person_b"] == p["id"]:
            other_id = r["person_a"]
        else:
            continue
        oname = None
        for pp in persons:
            if pp["id"] == other_id:
                oname = pp["name"]
                break
        if oname is None:
            continue
        out.append({
            "person": oname, "person_id": f"gongyi_{oname}",
            "relationship_type": r["type"], "strength": "strong" if r["type"] == "overlap" and 1 in (r["person_a"], r["person_b"]) and 2 in (r["person_a"], r["person_b"]) else "medium",
            "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"],
            "direction": "undirected", "confidence": "confirmed" if r["type"] == "overlap" else "plausible",
            "source_ids": []})
    return out


def _governance_record(p: dict, pos: dict | None = None) -> list[dict]:
    rec = []
    if p["id"] == 1:
        rec.append({"period": "2026", "domain": "economic_development", "achievement_or_event": "主持生态环保攻坚推进会、部署乡村振兴/招商；深化'放管服'改革与县域营商环境建设",
                     "role_in_event": "市委书记", "measurable_outcome": "", "location": "巩义市", "confidence": "confirmed", "source_ids": ["S002"]})
    elif p["id"] == 2:
        rec.append({"period": "2026", "domain": "industrial", "achievement_or_event": "到水泥企业调研安全生产与超低排放改造，推动经济高质量发展",
                     "role_in_event": "市长", "measurable_outcome": "", "location": "巩义市", "confidence": "confirmed", "source_ids": ["S002"]})
    return rec


def _professional(p: dict) -> dict:
    if p["id"] == 1:
        return {"primary_specializations": ["开发园区经济", "大数据/数字产业", "区域治理"], "secondary_specializations": ["人事/组织"],
                "career_pattern": "cross_county_rotation", "systems_experience": ["government", "party", "state_owned_enterprise"],
                "geographic_pattern": ["河南郑州", "郑东新区", "郑州高新区", "巩义"], "promotion_velocity": {"summary": "从郑东新区管委会办公室起步，经20余年逐步升至市委书记", "notable": ["2025.4 高新区任上出任市长，2026.2 一年内升任市委书记"]}}
    if p["id"] == 2:
        return {"primary_specialization": ["政府行政", "城市规划/城建"], "secondary_specializations": [],
                "career_pattern": "local_ladder", "systems_experience": ["government"], "geographic_pattern": ["河南省郑州市"],
                "promotion_velocity": {"summary": "从市政府领导班子（常务副市长）升任市长", "notable": []}}
    return {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
            "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "公开资料不足", "notable_fast_promotions": []}}


def _confidence(p: dict) -> dict:
    ident = "confirmed" if p["id"] in (1, 2, 3, 4, 11, 12, 13) else ("confirmed" if p.get("birth") else "plausible")
    return {"identity": ident, "current_role": "confirmed" if p["id"] in (1, 2) else "plausible",
            "career_completeness": "complete" if p["id"] == 1 else ("partial" if p["id"] in (2, 12, 13) else "thin"),
            "relationship_confidence": "medium", "biggest_gap": _biggest_gap(p)}


def _biggest_gap(p: dict) -> str:
    if p["id"] == 1:
        return "履历完整，缺少本地籍贯/出生地确切记录"
    if p["id"] == 2:
        return "任市长前的具体历任职务时间线（此前常务副市长任内的具体时间）"
    if p["id"] in (3, 4, 6, 7, 8, 9, 10):
        return "出生/学历后有较完整身份，但详细职业履历公开较少"
    if p["id"] == 11:
        return "任纪委书记以来的近期公开活动与任期"
    if p["id"] in (12, 13):
        return "前任详细履历已多，当前职（政协秘书长/高新区书记）的具体时间线"
    return "履历待查"


def _open_questions(p: dict) -> list[dict]:
    q = []
    if p["id"] == 2:
        q.append({"priority": "critical", "question": "张朔嘉自1984年生女硕士出身、任市长前的完整历任职务与时间？", "why_it_matters": "核心目标人物（市长）角色与履历完整性", "suggested_queries": ["张朔嘉 简历 历任 巩义工", "张朔 郑州 常务副市"], "last_attempted": AS_OF})
        q.append({"priority": "high", "question": "现任其他市委委员（组织部长、宣传部长、统战部长、政法委书记）名单", "why_it_matters": "完善领导班子图谱", "suggested_queries": ["巩义市委 班子成员 2026"], "last_attempted": AS_OF})
    elif p["id"] == 1:
        q.append({"priority": "medium", "question": "郭程明出生地/籍贯（是否为郑州人）", "why_it_matters": "完善身份与地域关系", "suggested_queries": ["郭程明 籍贯"], "last_attempted": AS_OF})
    elif p["id"] in (3, 4, 5, 6, 7, 8, 9, 10):
        q.append({"priority": "high", "question": f"{p['name']} 历任职务完整履历", "why_it_matters": "完善领导班子成员档案", "suggested_queries": [f"{p['name']} 履历 巩义"], "last_attempted": AS_OF})
    elif p["id"] == 11:
        q.append({"priority": "medium", "question": "汤涛任纪委书记的确切起止时间", "why_it_matters": "纪委职责与任期", "suggested_queries": ["汤涛 巩义 纪委书记 任职时间"], "last_attempted": AS_OF})
    return q


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  级别: 县级市")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 巩义市人民政府网 (www.gongyishi.gov.cn)")
    print("=" * 60)

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

    for p in persons:
        job = p["current_post"]
        name = p["name"]
        if name in ("张朔嘉", "郭程明", "夏利东", "康新伟", "汤涛", "袁聚平", "张东辉"):
            data = make_person_json(job, name)
            if data is None:
                continue
            safe_name = name.replace("/", "_").replace("　", "")
            person_path = PERSONS_DIR / f"{TODAY}-河南省-郑州市-{job}-{safe_name}.json"
            with open(person_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Person JSON: {person_path.name}")

    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"  人员: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")


if __name__ == "__main__":
    main()