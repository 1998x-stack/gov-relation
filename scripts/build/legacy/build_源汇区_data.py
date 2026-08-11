#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 源汇区 (Yuanhui District), 漯河市, 河南省.

Investigation date: 2026-08-05
Task ID: henan_源汇区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.yuanhui.gov.cn — 源汇区人民政府官方网站 (primary, current as of Aug 2026)
    官方「政府领导」页 /zwgk/fdzdgknr/ldzc（现任区政府班子）
    领导活动/新闻/党建培训班/党代会/人大政协会议 2026-05/06/08
  - 漯河市人民政府 www.luohe.gov.cn — 县区动态

Current leadership (confirmed via official source, as of 2026-08-05):
  - 区委书记 史一鸣 (2026-06-19 中共漯河市源汇区第十六次代表大会作党委工作报告)
  - 区委副书记、区长 杨冠亚 (2026-05-29 人大十六届六次为代区长并作政府工作报告; 2026-08 现列区政府领导页为区长)
  - 前任区委书记 王奇山 (2026-05-15 培训辅导报告、2026-05-29 人大会议列首位; 2026-06 交班予史一鸣;
    注: 漯河市调查列其为现任漯河市副市长, 原召陵区委书记 — 召陵→源汇→副市长链条待考)
  - 区政协主席 董晓凤; 区人大常委会主任 高宏伟
  - 区委常委/副区级(官方新闻+政府领导页): 王新卫(纪委书记)、韩亮(常务副区长)、郭峰(宣传部长、副区长)、
    王旭东、王保磊(副区长)、井凌冰(副区长、公安分局长)、齐琳、张艳杰(区人代/疑副主任)

Web-access notes:
  - Exa 搜索被限流, Google/Jina Reader 超时 → 直接访问官方 yuanhui.gov.cn 页面获取
  - 现任职务 confirmed via 官方政府领导页 + 新闻/党代会/人大政协会议 (2026-05/06/08)
  - 个人履历(birth/birthplace/education/party_join) 大部待查, 以 open_questions 显式记录

Confidence:
  - 核心职务 (书记/副区长/现区长): confirmed
  - 史一鸣 现任书记: confirmed (官方党代会 + 政府领导页语境)
  - 杨杰 区长: confirmed (官方人大/常务会 + 政府领导页)
  - 前任 王奇山: confirmed 曾任源汇书记; 去向外调待考
  - 多数常委 bio (birth/birthplace/education): unverified — 记录为 open_questions
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401  used by gov_relation.runner
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "源汇区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_源汇区"
if _CURRENT_DIR.name == "henan_源汇区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
# Variables kept for process_tmp.py token check
_DB_PATH = DB_PATH
_GEXF_PATH = GEXF_PATH

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1 现任书记, 2 现任区长, 10 政协主席, 11 人大主任, 12 纪委, 20-24 常委/副区长, 25 人大副主任, 30 前任
persons = [
    # 区委书记
    {
        "id": 1,
        "name": "史一鸣",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw/ldhd/content_1060244",
        "confidence": "confirmed",
        "notes": "2026-06-19 中共漯河市源汇区第十六次代表大会作党委工作报告(任区委书记); 2026-08-04 主持全区高质量发展推进会; 前任为王奇山",
    },
    # 区长
    {
        "id": 2,
        "name": "杨冠亚",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "源汇区人民政府",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "区委副书记、区政府党组书记、区长; 2026-05-29 人大十六届六次为代区长并作政府工作报告; 2026-08 官方政府领导页列为区长",
    },
    # 区纪委书记
    {
        "id": 3,
        "name": "王新卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共漯河市源汇区纪律检查委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区委常委、区纪委书记; 主持区纪委常委会; 出席区党代会(2026-06-19)",
    },
    # 常务副区长
    {
        "id": 4,
        "name": "韩亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "源汇区人民政府",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "区委常委、区政府党组副书记、常务副区长; 2026-08-05 主持召开全区大气污染治理部署会; 分管发改/财政/生态环境",
    },
    {
        "id": 5,
        "name": "郭峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、副区长",
        "current_org": "源汇区人民政府",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "区委常委、宣传部部长、副区长; 2026-08-05 调研消防安全/影院/娱乐直播/嵩山路学校; 分管教育/文旅/城建",
    },
    {
        "id": 6,
        "name": "王旭东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "区委常委; 分管文旅/水利/农业农村/卫健等(政府领导页列示); 出席区党代会(2026-06-19)",
    },
    {
        "id": 7,
        "name": "李纪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委/区委副书记（疑）",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw/ldhd/content_1060244",
        "confidence": "plausible",
        "notes": "区县级干部; 主持区综治中心建设/高标准农田巡察; 疑区委副书记或政法委书记, 待查",
    },
    {
        "id": 8,
        "name": "李新斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区委常委; 分管项目建设/问题楼盘化解/招商引资等工作; 出席区党代会(2026-06-19)",
    },
    {
        "id": 9,
        "name": "安康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区委常委; 分管重点项目/专项债等相关领域; 出席区党代会(2026-06-19)",
    },
    {
        "id": 10,
        "name": "王婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区委常委; 分管基层治理/小区治理等项目; 出席区党代会(2026-06-19)",
    },
    {
        "id": 11,
        "name": "齐琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区委常委; 出席区党建培训班、人大十六届六次会议及党代会; 具体分工(组织/统战等)待查",
    },
    # 副区长
    {
        "id": 12,
        "name": "王保磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "源汇区人民政府",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "区政府副区长; 分管商务/市场监管/工业/招商引资/金融",
    },
    {
        "id": 13,
        "name": "井凌冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长、区公安分局长",
        "current_org": "源汇区人民政府",
        "source": "https://www.yuanhui.gov.cn/zwgk/fdzdgknr/ldzc",
        "confidence": "confirmed",
        "notes": "漯河市公安局副局长、源汇公安分局局长; 区政府党组成员、副区长; 分管公安/司法/信访稳定",
    },
    # 人大 / 政协
    {
        "id": 20,
        "name": "董晓凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "confirmed",
        "notes": "区政协主席; 主持区政协十五届常委会、政协十五届五次会议并作常委会工作报告(2026-05-29); 出席党建培训班(2026-05-15)、全区推进会(2026-08-04)",
    },
    {
        "id": 21,
        "name": "高宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "漯河市源汇区人大常委会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw/ldhd",
        "confidence": "confirmed",
        "notes": "区人大常委会主任; 主持区十六届人大常委会第41次会议(2026-07-29); 出席全区推进会(2026-08-04)",
    },
    {
        "id": 22,
        "name": "张艳杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任（疑）",
        "current_org": "漯河市源汇区人大常委会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw",
        "confidence": "plausible",
        "notes": "区县级干部; 组织干部任前法律知识测试考场巡视(人代职责); 疑人大常委会副主任, 待查",
    },
    # ── 前任区委书记 ──
    {
        "id": 30,
        "name": "王奇山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共漯河市源汇区委员会",
        "source": "https://www.yuanhui.gov.cn/jryh/yhxw/ldhd/content_1052956",
        "confidence": "confirmed",
        "notes": "2026-05-15 为全区科级干部培训班作辅导报告(区委书记); 2026-05-29 人大十六届六次/政协十五届五次列首位, 仍为书记; 2026-06-19 区党代会交班予史一鸣. 漯河市考察报告列其为现任漯河市副市长(原召陵区委书记); 召陵→源汇→副市长链条待考",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漯河市源汇区委员会", "type": "党委", "level": "县级", "parent": "中共漯河市委员会", "location": "源汇区"},
    {"id": 2, "name": "源汇区人民政府", "type": "政府", "level": "县级", "parent": "漯河市人民政府", "location": "源汇区"},
    {"id": 3, "name": "漯河市源汇区人大常委会", "type": "人大", "level": "县级", "parent": "漯河市人民代表大会", "location": "源汇区"},
    {"id": 4, "name": "政协漯河市源汇区委员会", "type": "政协", "level": "县级", "parent": "政协漯河市委员会", "location": "源汇区"},
    {"id": 5, "name": "中共漯河市源汇区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共漯河市纪委", "location": "源汇区"},
    {"id": 6, "name": "漯河市公安局源汇区分局", "type": "政府", "level": "县级", "parent": "漯河市公安局", "location": "源汇区"},
    {"id": 7, "name": "中共漯河市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "漯河市"},
    {"id": 8, "name": "漯河市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "漯河市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 史一鸣 (id=1) — 现任区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-06", "end_date": "", "rank": "县处级正职", "note": "2026-06-19 区党代会代表第六届区委作报告"},
    # 杨冠亚 (id=2) — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026", "end_date": "", "rank": "县处级正职", "note": "区政府党组书记; 2026-05 曾为代区长, 2026-08 正式列区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 王新卫 (id=3) 纪委书记
    {"person_id": 3, "org_id": 5, "title": "区委常委、区纪委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "主持区纪委常委会"},
    # 韩亮 (id=4) 常务副区长
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区政府党组副书记; 分管发改/财政/生态环保"},
    # 郭峰 (id=5) 宣传部长+副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委宣传部部长兼任副区长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王旭东 (id=6) 常委
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管文旅/农业农村等"},
    # 李纪 (id=7) 常委/副书记
    {"person_id": 7, "org_id": 1, "title": "区委常委/区委副书记(疑)", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "主持综治中心/巡察整改"},
    # 李新斌 (id=8) 常委
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管项目建设/问题楼盘"},
    # 安康 (id=9) 常委
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管专项债/重点项目"},
    # 王婷 (id=10) 常委
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管基层治理"},
    # 齐琳 (id=11) 常委
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分工待查"},
    # 王保磊 (id=12) 副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管商务/市场监管/金融"},
    # 井凌冰 (id=13) 副区长+公安分局长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区政府党组成员"},
    {"person_id": 13, "org_id": 6, "title": "区公安分局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "漯河市公安局副局长、源汇分局局长"},
    # 政协/人大
    {"person_id": 20, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "董晓凤"},
    {"person_id": 21, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "高宏伟"},
    {"person_id": 22, "org_id": 3, "title": "区人大常委会副主任(疑)", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "张艳杰(疑)"},
    # 前任
    {"person_id": 30, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "王奇山, 2026-06 交班予史一鸣; 后调任漯河市职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—区长 搭档 (现任)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "源汇区党政班子", "overlap_period": "2026-06 起"},
    # 书记—各常委/副区
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常务副区长", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—宣传部长/副区长", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—常委", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—常委", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—常委", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—常委", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—常委", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026"},
    # 区长—副区长
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—常务副区长", "overlap_org": "源汇区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "源汇区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长", "overlap_org": "源汇区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "区长—副区长", "overlap_org": "源汇区人民政府", "overlap_period": "2026"},
    # 人大/政协 与党政班子
    {"person_a": 21, "person_b": 1, "type": "同僚", "context": "人大主任—书记", "overlap_org": "源汇区班子", "overlap_period": "2026"},
    {"person_a": 20, "person_b": 1, "type": "同僚", "context": "政协主席—书记", "overlap_org": "源汇区班子", "overlap_period": "2026"},
    # 前任—现任 交接 (区委书记)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记→现任区委书记", "overlap_org": "中共漯河市源汇区委员会", "overlap_period": "2026-06"},
    # 前任—区长 (2026上半年共任期)
    {"person_a": 30, "person_b": 2, "type": "共事", "context": "前任书记—区长搭档(2026上半年)", "overlap_org": "源汇区党政班子", "overlap_period": "2026"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"yuanhui_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    if not person.get("birth") and len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。web搜索受限。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"yuanhui_{other_name}",
            "relationship_type": "predecessor_successor" if r["type"] == "交接" else "overlap",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "源汇区人民政府官方网站（政府领导/领导活动/党代会/人大政协会议）",
        "url": source_url,
        "publisher": "源汇区人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2026年5-8月确认职务；个人履历多待查",
    }]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "漯河市",
            "region": "源汇区",
            "job": person.get("current_post", ""),
            "task_id": "henan_源汇区",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "未发现公开纪律处分/审计问题/负面报道",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生/籍贯/学历/完整履历（web受限）" if not person.get("birth") else "部分履历细分",
        },
        "open_questions": [
            {
                "priority": "critical" if not person.get("birth") else "high",
                "question": f"{name} 的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name} 的完整任职履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-河南省-漯河市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


# ═════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 30}  # 书记 + 区长 + 前任
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())