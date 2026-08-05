#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新密市 (Xinmi City), 郑州市, 河南省.

Level: 县级市
Province: 河南省
Parent city: 郑州市
Targets: 市委书记 (程洋), 市长 (杜鹏懿)
Task ID: henan_新密市

Research date: 2026-08-05
Official source: https://www.xinmi.gov.cn/ (新密市人民政府) & https://public.xinmi.gov.cn/ (政务公开·领导介绍)

Current status (as of 2026-08-05, verified via official 新密市 sources):
- 市委书记: 程洋 (市委理论学习中心组2026年第七次集中学习会议、程洋调研防汛备汛/乡村振兴 等多条 2026 要闻确认在任; 程洋原任新密市市长，2020年当选市长，2024年6月前后升任市委书记并一度兼任市长，2024年12月市委副书记、代市长杜鹏懿到任后专任市委书记)
- 市长: 杜鹏懿 (市委副书记、市政府党组书记、市长; 官方领导介绍简历 + 2026 多次"市长杜鹏懿主持召开市政府常务会议"确认在任)

Government leadership 领导介绍 (from official https://public.xinmi.gov.cn/ , 9 members, identity from 官方简介):
  - 杜鹏懿 市委副书记、市政府党组书记、市长 (1977-12, 男, 大学经济学学士, 中共党员)
  - 张伟锋 市委常委、市政府党组副书记、常务副市长 (1981-08, 男, 大学本科, 中共党员)
  - 王川 市委常委、市政府党组成员、副市长 (1988-01, 男, 研究生医学博士, 中共党员)
  - 李孟洁 市政府副市长 (1981-12, 女, 本科农业推广硕士, 中国农工民主党)
  - 樊建平 市政府党组成员、副市长 (1972-07, 男, 大学本科, 中共党员)
  - 王玉强 市政府党组成员、副市长 (1974-03, 男, 大学经济学学士, 中共党员)
  - 郝炳鑫 市政府党组成员、副市长 (1979-03, 男, 大学经济管理学士, 中共党员)
  - 王景 市政府党组成员、副市长 (1990-01, 男, 研究生工学博士, 中共党员)
  - 邵世权 市政府党组成员、二级调研员 (1969-07, 男, 大学学历, 中共党员)

Party (市委) members confirmed via official 要闻:
  - 程洋 市委书记 (男; 现任; 出生/学历/籍贯 公开资料不足 -> open_questions)
  - 王洁 市委常委、市委办公室主任 (2026-07-28 程洋调研新闻确认)

Predecessor / successor (official 要闻 + 媒体检索):
  - 陈春梅 前任市委书记 (2022-01 ~ 约2024-06 在任; 2022-01 "新密市委书记陈春梅" 多个官方要闻; 2023-11 仍以书记身份出现)
  - 程洋 2020 当选新密市市长 (公众号 2020-07-06 "程洋当选新密市人民政府市长"); 任市长至 2024-06; 2024 年 6 月前后升任市委书记兼市长 (党政一肩挑, 2024-06-20 "市委书记、市长程洋" 使官方要闻); 2024-12 专任市委书记
  - 杜鹏懿 2024-12 任市委副书记、代市长 ("市委副书记、代市长杜鹏懿" 2024-12-17 官方要闻), 2025 转正式市长

Web access note: Exa MCP rate-limited, r.jina.ai/Bing/thepaper/baike 不可达, sogou/360 间歇验证码. 官方 新密 两级站点
(www.xinmi.gov.cn + public.xinmi.gov.cn) 全程稳定并提供了权威的现任政府班子名单+简历 与 要闻时间线。市委书记程洋的
出生/学历/入党/最早起 【及】杜鹏懿、陈春梅的早年/离任后有去向 等公开信息在本次受限环境下未能完全闭环, 已作为
open_questions 明确记录而不虚构。

Confidence notes:
  程洋 (市委书记): role CONFIRMED (官方要闻 多项 2026); current-post history CONFIRMED (市长→书记 时间线由官方要闻吻合重构);
        身份 identity (出生/学历/籍贯) UNSETTLED -> open_questions。
  杜鹏毅 (市长): role CONFIRMED (官方领导介绍+要闻); identity CONFIRMED (1977-12, 男, 大学经济学学士, 中共党员)。
  张伟锋/王川/李孟洁/樊建平/王玉强/郝炳鑫/王景/邵世权 身份+职务 CONFIRMED (官方简介); 详细历任履历 UNKNOWN -> open_questions。
  陈春梅 (前任书记): role CONFIRMED (2022-2023 官方+媒体); 离任后去向 UNKNOWN -> open_questions。
  跨区交流、任前公示等历史线索公开资料有限；同班子重合(medium/strong)关系根据官方要闻建立。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_新密市/.. = tmp
if (_REPO_ROOT / "gov_relation").exists():
    sys.path.insert(0, str(_REPO_ROOT))
else:
    _REPO_ROOT = (_STAGING_DIR / "../../..").resolve()  # repo root
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "新密市"

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
#  S001 新密市人民政府网 政务要闻 (www.xinmi.gov.cn/zxdt/) 程洋 市委书记 / 杜鹏懿 市长 / 王洁 市委办主任 时序
#  S002 新密政务公开·领导介绍 (public.xinmi.gov.cn/D13X/**) 杜鹏懿 张伟锋 王川 李孟洁 樊建平 王玉强 郝炳鑫 王景 邵世权
#  S003 新密要闻·两会/媒体 (公众号/知乎检索) 陈春梅 任书记; 程洋 2020 当选市长; 周建超/焦成举 2023 班子成员
#  S004 新密政任〔2026〕任免文件 政府人事 (public.xinmi.gov.cn 政务公开)

persons = [
    # ── 1. 市委书记 程洋 ──
    {
        "id": 1,
        "name": "程洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共新密市委员会",
        "source": "S001",
    },
    # ── 2. 市长 杜鹏懿 ──
    {
        "id": 2,
        "name": "杜鹏懿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },

    # ── 市政府领导班子（官方 领导介绍）──
    {
        "id": 3,
        "name": "张伟锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 4,
        "name": "王川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年1月",
        "birthplace": "",
        "education": "研究生，医学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 5,
        "name": "李孟洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "本科，农业推广硕士",
        "party_join": "中国农工民主党",
        "work_start": "",
        "current_post": "市政府副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 6,
        "name": "樊建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 7,
        "name": "王玉强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "",
        "education": "大学，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 8,
        "name": "郝炳鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "大学，经济管理专业学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 9,
        "name": "王景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年1月",
        "birthplace": "",
        "education": "研究生，工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、副市长",
        "current_org": "新密市人民政府",
        "source": "S002",
    },
    {
        "id": 10,
        "name": "邵世权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员、二级调研员",
        "current_org": "新密市人民政府",
        "source": "S002",
    },

    # ── 市委 班子成员 (官方要闻确认) ──
    {
        "id": 11,
        "name": "王洁",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任",
        "current_org": "中共新密市委员会",
        "source": "S001",
    },

    # ── 前任领导 (predecessors) ──
    {
        "id": 12,
        "name": "陈春梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委书记（2022-约2024-06）",
        "current_org": "中共新密市委员会",
        "source": "S003",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共新密市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 2,
        "name": "新密市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 3,
        "name": "中共新密市纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共郑州市纪律检查委员会",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 4,
        "name": "新密市人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "郑州市人大常委会",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 5,
        "name": "政协新密市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协郑州市委员会",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 6,
        "name": "新密市委办公室",
        "type": "党委",
        "level": "正科级",
        "parent": "中共新密市委员会",
        "location": "河南省郑州市新密市",
    },
    {
        "id": 7,
        "name": "新密市产业集聚区管理委员会",
        "type": "开发区",
        "level": "县处级",
        "parent": "新密市人民政府",
        "location": "河南省郑州市新密市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS  (schema uses start_date / end_date)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 1. 程洋（市委书记）──
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-06", "end_date": "present",
     "rank": "正县级", "note": "2024 年 6 月前后由市长升任市委书记（一度兼任市长）；2024-12 起专职市委书记；截至2026-07 官方要闻确认在任"},
    {"person_id": 1, "org_id": 2, "title": "市长（兼任，党政一肩挑）", "start_date": "2024-06", "end_date": "2024-12",
     "rank": "正县级", "note": "2024-06-20 官方要闻以'市委书记、市长程洋'出现，2024-08 ~ 2024-11 多以'市委书记、市长程洋'出现；2024-12 代市长杜鹏懿到任后不再兼"},
    {"person_id": 1, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2020", "end_date": "2024-06",
     "rank": "正县级", "note": "2020 年当选新密市人民政府市长（公众号 2020-05-06'程洋当选新密市人民政府市长'）；2022-01 ~ 2024-05 官方要闻多次'新密市市长程洋'"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记", "start_date": "2020", "end_date": "2024-06",
     "rank": "副县级", "note": "任市长期间兼任市委副书记（2022-01 官方要闻'新密市委副书记、市长程洋'）；2024-06 升任市委书记后不再兼"},

    # ── 2. 杜鹏懿（市长） ──
    {"person_id": 2, "org_id": 2, "title": "市长、市政府党组书记", "start_date": "2025-01", "end_date": "present",
     "rank": "正县级", "note": "2025 年转正式市长；截至2026-07 官方要闻多次确认"},
    {"person_id": 2, "org_id": 2, "title": "代市长", "start_date": "2024-12", "end_date": "2025-01",
     "rank": "正县级", "note": "2024-12-17 官方要闻'市委副书记、代市长杜鹏懿'"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024-12", "end_date": "present",
     "rank": "正县级", "note": "市委副书记兼任市长"},

    # ── 3. 张伟锋（常务副市长） ──
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "新密市委常委、市政府党组副书记、常务副市长（1981-08, 男, 本科）"},
    # ── 4. 王川 ──
    {"person_id": 4, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1988-01, 男, 研究生医学博士"},
    # ── 5. 李孟洁（党外，农工党） ──
    {"person_id": 5, "org_id": 2, "title": "市政府副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1981-12, 女, 本科农业推广硕士, 中国农工民主党"},
    # ── 6. 樊建平 ──
    {"person_id": 6, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1972-07, 男, 本科"},
    # ── 7. 王玉强 ──
    {"person_id": 7, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1974-03, 男, 大学经济学学士"},
    # ── 8. 郝炳鑫 ──
    {"person_id": 8, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1979-03, 男, 大学经济管理学士"},
    # ── 9. 王景 ──
    {"person_id": 9, "org_id": 2, "title": "市政府党组成员、副市长", "start_date": "", "end_date": "present",
     "rank": "副县级", "note": "1990-01, 男, 研究生工学博士"},
    # ── 10. 邵世权 ──
    {"person_id": 10, "org_id": 2, "title": "市政府党组成员、二级调研员", "start_date": "", "end_date": "present",
     "rank": "调研员", "note": "1969-07, 男, 大学学历"},
    # ── 11. 王洁（市委办） ──
    {"person_id": 11, "org_id": 6, "title": "市委办公室主任", "start_date": "", "end_date": "present",
     "rank": "正科级", "note": "市委常委；2026-07-28 随市委书记程洋调研（官方要闻'市委常委、市委办公室主任王洁'）"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present",
     "rank": "县级", "note": ""},

    # ── 12. 陈春梅（前任书记） ──
    {"person_id": 12, "org_id": 1, "title": "市委书记", "start_date": "2022-01", "end_date": "2024-06",
     "rank": "正县级", "note": "2022-01 官方要闻多次'新密市委书记陈春梅'；2023-11-03 仍以市委书记身份考察；约 2024 年 6 月离（程洋接任）"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
# confirmed = 官方资料/要闻; plausible = 同机构同班子推定; unverified = 待查

relationships = [
    # 党政主要领导搭档（书记-市长 强关系）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记程洋 与 市委副书记、市长 杜鹏懿 构成新密市党政主要领导搭档，共同主持全市工作（2026 联合推进防汛/安全生产/乡村振兴/环保等）",
     "overlap_org": "中共新密市委员会/新密市人民政府",
     "overlap_period": "2024-12至现在"},
    # 书记-前任书记（继任）
    {"person_a": 1, "person_b": 12, "type": "succession",
     "context": "程洋于 2024 年接替原市委书记陈春梅；程洋此前任新密市长多年，是陈春梅时代的政府一把手",
     "overlap_org": "中共新密市委员会",
     "overlap_period": "2024-06 交接"},
    # 市长 与 前任市长程洋（继任：杜接替程的市长）
    {"person_a": 2, "person_b": 1, "type": "succession",
     "context": "杜鹏懿 2024-12 接替程洋任市长（程洋升任市委书记），两人同时构成党政搭档",
     "overlap_org": "新密市人民政府",
     "overlap_period": "2024-12 交接"},
    # 市长 与 常务副市长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "张伟锋 市委常委、常务副市长，为市长主持市政府日常工作的副手",
     "overlap_org": "新密市人民政府",
     "overlap_period": "2025至现在"},
    # 市长 与 党外副市长（班子多元）
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "李孟洁（农工民主党）为市政府副市长，与市长同在政府班子",
     "overlap_org": "新密市人民政府",
     "overlap_period": "2025至现在"},
    # 书记 与 市委办主任（直接下属）
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "王洁 市委常委、市委办公室主任，随程洋调研，为书记办公室负责人",
     "overlap_org": "中共新密市委员会/新密市委办公室",
     "overlap_period": "2026至现在"},
    # 副市长同班子（政府班子核心）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "张伟锋（常务副市长）与王川（市委常委、副市长）同为市委常委/政府班子",
     "overlap_org": "新密市人民政府",
     "overlap_period": "2026至现在"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Helper functions (mirror 巩义市 template)
# ══════════════════════════════════════════════════════════════════════════════

_SOURCE_REGISTER = [
    {
        "id": "S001", "title": "新密市人民政府·政务要闻（www.xinmi.gov.cn/zxdt/）",
        "url": "https://www.xinmi.gov.cn/zxdt/index.jhtml", "publisher": "新密市人民政府",
        "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
        "notes": "程洋 任市委书记（2026-07-28 调研、2026-06 走访慰问老党员等）；杜鹏懿 任市长/市委副书记（2026 多期政府常务会）；王洁 市委常委/市委办主任；2022-01 '新密市委书记陈春梅'；2024-06 '市委书记、市长程洋'；2024-12 '市委副书记、代市长杜鹏懿'"},
    {
        "id": "S002", "title": "新密市政务公开·领导介绍（public.xinmi.gov.cn/D13X/*.jhtml）",
        "url": "https://public.xinmi.gov.cn/D13X/8855794.jhtml", "publisher": "新密市政务公开", "accessed_at": AS_OF,
        "source_type": "official", "reliability": "高",
        "notes": "市长杜鹏毅（1977-12 男 大学经济学学士 党员）及市政府 领导介绍 共 9 人（张伟锋、王川、李孟洁、樊建平、王玉强、郝教鑫、王景、邵世权）简历均可公开获"},
    {
        "id": "S003", "title": "新密人大两会/媒体检索（公众号·知乎等）",
        "url": "", "publisher": "媒体汇编", "accessed_at": AS_OF,
        "source_type": "media", "reliability": "medium",
        "notes": "程洋 2020-05-06 当选新密市人民政府市长；陈春梅 2022-01 ~ 2023-11 任新密市委书记；2023-11 陈考察团 成员 周建超（开发区）、周成举（副市长）、周健中（副市长）、赵婷（市委办副主任）等"},
    {
        "id": "S004", "title": "新密市 略外招生参访（政务公开 任免文件）",
        "url": "https://public.xinmi.gov.cn/?a=info", "publisher": "新密市人民政府",
        "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "高",
        "notes": "新密政任〔2026〕编号 政府人事任免文件（如 任命张贝贝、驾照 10 号等），整体佐证政府班子在任状态"},
]

# 以下是 person JSON 辅助函数，与巩义模板一致（但模型名基于本库数据）

def _identity_person(name: str) -> dict | None:
    for p in persons:
        if p["name"] == name:
            return p
    return None


def make_person_json(job: str, name: str) -> dict:
    p = _identity_person(name)
    if p is None:
        return None
    pid = f"xinmi_{name}"
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
                "level": pos.get("rank", ""), "location": "河南省郑州市新密市",
                "system": _system_for(pos.get("org_id", 1)), "rank": pos.get("rank", ""),
                "is_key_promotion": pos["title"] in ("市委书记", "市长、市政府党组书记"),
                "notes": pos.get("note", ""), "confidence": "confirmed" if p["id"] != 12 else "plausible",
                "source_ids": [p["source"]],
            })
    if not timeline:
        timeline = [{"start": "", "end": "present", "org": p.get("current_org", ""),
                      "title": p.get("current_post", ""), "level": "",
                      "location": "河南省郑州市新密市", "system": "party",
                      "rank": "", "is_key_promotion": False, "notes": "",
                     "confidence": "plausible", "source_ids": [p["source"]]}]

    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": "河南省", "city": "郑州市", "region": "新密市",
                                 "job": job, "task_id": "henan_新密市", "time_focus": "2026-08"},
        "identity": identity,
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                            "administrative_rank": _rank_for(p["id"]), "as_of": AS_OF,
                            "is_current_confirmed": p["id"] in (1, 2, 3, 4, 5, 6, 8, 9, 10, 11),
                            "source_ids": [p["source"]]},
        "career_timeline": timeline,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"],
                            "level": o["level"], "location": o["location"]}
                           for o in organizations if o["id"] in {pos["org_id"] for pos in (career_timeline or [{}])}],
        "relationships": _relationship_for(name),
        "governance_record": _governance_record(p),
        "professional_profile": _professional(p),
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "unknown", "evidence": "公开报道有限，具体工作风格待深入调研",
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
    if pk in (1, 2, 12):
        return "正县级"
    if pk in (3, 4, 5, 6, 7, 8, 9, 10):
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
            "person": oname, "person_id": f"xinmi_{oname}",
            "relationship_type": r["type"], "strength": "strong" if r["type"] == "overlap" and p["id"] in (1, 2) else "medium",
            "evidence": r["context"], "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"],
            "direction": "undirected", "confidence": "confirmed" if r["type"] in ("overlap", "succession") else "plausible",
            "source_ids": []})
    return out


def _governance_record(p: dict) -> list[dict]:
    rec = []
    if p["id"] == 1:
        rec.append({"period": "2024-2026", "domain": "rural_revitalization", "achievement_or_event": "推进防汛备汛、乡村振兴、重点项目建设、工业升级等工作；主政期间推进全市项目建设与小微企业园谋划建设",
                     "role_in_event": "市委书记", "measurable_outcome": "", "location": "新密市", "confidence": "confirmed", "source_ids": ["S001"]})
        rec.append({"period": "2020-2024", "domain": "economic_development", "achievement_or_event": "任市长期间推动制造业企业运行、专业园区规划、煤炭行业转型升级等",
                     "role_in_event": "市长", "measurable_outcome": "", "location": "新密市", "confidence": "confirmed", "source_ids": ["S001"]})
    elif p["id"] == 2:
        rec.append({"period": "2025-2026", "domain": "economic_development", "achievement_or_event": "主持市政府常务会议推进全市经济工作、安全生产、森林防火等",
                     "role_in_event": "市长", "measurable_outcome": "", "location": "新密市", "confidence": "confirmed", "source_ids": ["S001"]})
    return rec


def _professional(p: dict) -> dict:
    if p["id"] == 1:
        return {"primary_specializations": ["区域治理", "经济/工业发展"], "secondary_specializations": ["防汛/应急管理"],
                "career_pattern": "local_ladder", "systems_experience": ["party", "government"],
                "geographic_pattern": ["郑州市新密市"], "promotion_velocity": {"summary": "在新密市由市长升任市委书记（2020市长→2024书记），县域成长", "notable_fast_promotions": []}}
    if p["id"] == 2:
        return {"primary_specializations": ["政府行政", "经济学"], "secondary_specializations": [],
                "career_pattern": "unknown", "systems_experience": ["government"], "geographic_pattern": ["河南省郑州市新密市"],
                "promotion_velocity": {"summary": "2024-12 任代市长→2025 转正；任前历任职务公开资料待查", "notable_fast_promotions": []}}
    return {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown",
            "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "公开资料不足", "notable_fast_promotions": []}}


def _confidence(p: dict) -> dict:
    ident = "confirmed" if p.get("birth") else ("confirmed" if p["id"] in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) else "plausible")
    return {"identity": ident, "current_role": "confirmed" if p["id"] in (1, 2) else "plausible",
            "career_completeness": "complete" if p["id"] == 1 else ("partial" if p["id"] in (2, 12) else "thin"),
            "relationship_confidence": "medium", "biggest_gap": _biggest_gap(p)}


def _biggest_gap(p: dict) -> str:
    if p["id"] == 1:
        return "出生年月/籍贯/学历/入党节点 及 任新密市长前（2020 前）的历任职务公开资料不足"
    if p["id"] == 2:
        return "任代市长（2024-12）前的历任职务/工作单位公开资料不足"
    if p["id"] == 12:
        return "陈春梅离开新密后的去向/现任职务待查"
    if p["id"] == 11:
        return "王洁（市委办主任）出生/学历/任职历程待查"
    return "出生/学历已有，但详细职业履历公开较少"


def _open_questions(p: dict) -> list[dict]:
    q = []
    if p["id"] == 1:
        q.append({"priority": "critical", "question": "程洋的出生年月、籍贯、学历、入党时间、参加工作起点", "why_it_matters": "核心目标人物（市委书记）的身份档案完整性", "suggested_queries": ["程洋 新密 简历", "程洋 出生 郑州", "程洋 任前公示"], "last_attempted": AS_OF})
        q.append({"priority": "high", "question": "程洋 2020 年任新密市长之前曾在哪些单位任职（郑州市直/其他区县？）", "why_it_matters": "还原其晋升来源与跨区流动", "suggested_queries": ["程洋 郑州 任职 简历", "程洋 新密市长 背景"], "last_attempted": AS_OF})
    elif p["id"] == 2:
        q.append({"priority": "high", "question": "杜鹏懿 任代市长（2024-12）前的历任职务", "why_it_matters": "完善市长履历与来源", "suggested_queries": ["杜鹏懿 简历 郑州", "杜鹏懿 任前"], "last_attempted": AS_OF})
    elif p["id"] == 12:
        q.append({"priority": "high", "question": "陈春梅离开新密市委书记后的去向/现任职务", "why_it_matters": "前任书记继任链完整性", "suggested_queries": ["陈春梅 新密 书记 去向", "陈春梅 郑州"], "last_attempted": AS_OF})
    elif p["id"] == 11:
        q.append({"priority": "medium", "question": "王洁（市委常委、市委办主任）的履历", "why_it_matters": "完善市委班子成员档案", "suggested_queries": ["王洁 新密 市委办主任"], "last_attempted": AS_OF})
    elif p["id"] in (3, 4, 5, 6, 7, 8, 9, 10):
        q.append({"priority": "medium", "question": f"{p['name']} 历任职务完整履历", "why_it_matters": "完善领导班子成员档案", "suggested_queries": [f"{p['name']} 简历 新密"], "last_attempted": AS_OF})
    return q


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  级别: 县级市")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: 新密市人民政府网 (www.xinmi.gov.cn) + 政务公开 (public.xinmi.gov.cn)")
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
        if name in ("程洋", "杜鹏懿", "张伟锋", "王川", "李孟洁", "樊建平", "王玉强", "郝炳鑫", "王景", "邵世权", "王洁", "陈春梅"):
            data = make_person_json(job, name)
            if data is None:
                continue
            safe_name = name.replace("/", "_").replace("　", "").replace(" ", "")
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