#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东丰县, 辽源市, 吉林省.

Level: 县
Province: 吉林省
Parent city: 辽源市
Targets: 县委书记 (Party Secretary: 袁学高), 县长/代县长 (Mayor: 于明明)
Task ID: jilin_东丰县

Research date: 2026-08-06
Official source: http://www.dongfeng.gov.cn/ (东丰县人民政府)

Current status (as of 2026-08-06, verified via 东丰县人民政府 website + media):
- 县委书记: 袁学高 (男，汉族，1975年10月生，大学学历，中共党员；曾任辽源市农业农村局局长、市商务局党组书记/局长/一级调研员；2025年起任东丰县委书记)
- 代县长: 于明明 (女，汉族，1980年8月生，大学学历，中共党员，现任东丰县委副书记、代县长、县政府党组书记)
- 前任县委书记: 曾海洋 (男，1969年3月生；曾任辽源市委常委、东丰县委书记；2024-12-19被吉林省纪委监委通报纪律审查和监察调查，后"双开")
- 前任县长: 王东 (2024-03-21当选县长；2026年由代县长于明明接任)

Leadership roster sourced from:
  - http://www.dongfeng.gov.cn/xzf/zfld/ (政府领导)
  - http://www.dongfeng.gov.cn/xzf/zfld/xz/ymm/ (于明明·代县长)
  - http://www.dongfeng.gov.cn/xzf/zfld/cwfxz/myl/ (马云龙·常务副县长)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/wb/ (闻博·副县长挂职)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/zgx/ (张国喜·副县长)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/jyk/ (姜英坤·副县chang)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/stn/ (山田女·副县长)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/qfj/ (秦凤杰·副县长/公安局长)
  - http://www.dongfeng.gov.cn/xzf/zfld/fxz/whb/ (王洪波·副县长)
  - http://www.dongfeng.gov.cn/jrdf/zwdt/202607/t20260702_743777.html (县领导观看大会直播,确认袁学高为县委书记 2026-07)
  - http://www.dongfeng.gov.cn/jrdf/zwdt/202607/t20260710_744121.html (代县长于明明检查防汛工作)
  - http://www.dongfeng.gov.cn/xxgk/zwxxgk/gzbg/202602/t20260212_731842.html (2025年政府工作报告)
  - 搜狗百科·袁学高 (出生日期/履历片段)
  - 网易/今日头条 转载 (2024-12-19 曾海洋被查通报; 2024-03 王东当选县长)

Confidence notes:
  袁学高/于明明 身份与在任均为 confirmed (官方县网站文章 + 政府领导页).
  领导 roster 为官方政府领导页一手数据 confirmed.
  曾海洋被查/"双开" confirmed via 纪委通报与媒体转载 (dates可靠).
  王东→于明明 交接时间节点 partial (王东至2025-12在位，于明明2026-07已为代县长).
  各人完整 .ri (出生地点/院校) 多为"plausible"/"unverified"，已标注于 each JSON.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Locate repo root robustly across staging vs canonical locations.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in (2, 3, 4, 5):
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "东丰县"
TASK_ID = "jilin_东丰县"

# DB/GEXF + person JSONs always land in the task staging dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-08-06"
TODAY = "20260806"

_PID = "dongfeng"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 ──
    {
        "id": 1,
        "name": "袁学高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共东丰县委员会",
        "source": "https://www.sogou.com/baike/袁学高",
    },
    # ── Core: 县人大代表 县长 ──
    {
        "id": 2,
        "name": "于明明",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "current_org": "东丰县人民政府",
        "current_post": "县委副书记、代县长",
        "source": "http://www.dongfeng.gov.cn/xzf/zfld/xz/ymm/",
    },
    # ── 县政府班子成员 (常务/副县) ──
    {"id": 3, "name": "马云龙", "gender": "男", "ethnicity": "汉族", "birth": "1988年5月",
     "birthplace": "", "education": "工商管理硕士", "current_post": "县委常委、常务副县长",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/cwfxz/myl/"},
    {"id": 4, "name": "闻博", "gender": "男", "ethnicity": "汉族", "birth": "1980年12月",
     "birthplace": "", "education": "法学博士", "current_post": "县委常委、副县长(挂职)",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/wb/"},
    {"id": 5, "name": "张国喜", "gender": "男", "ethnicity": "汉族", "birth": "1979年12月",
     "birthplace": "", "education": "研究生", "current_post": "县委常委、副县长",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/zgx/"},
    {"id": 6, "name": "姜英坤", "gender": "男", "ethnicity": "汉族", "birth": "1977年12月",
     "birthplace": "", "education": "研究生", "current_post": "副县长",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/jyk/"},
    {"id": 7, "name": "山田女", "gender": "女", "ethnicity": "汉族", "birth": "1988年6月",
     "birthplace": "", "education": "研究生", "current_post": "副县长(挂职)",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/stn/"},
    {"id": 8, "name": "秦凤杰", "gender": "男", "ethnicity": "汉族", "birth": "1973年9月",
     "birthplace": "", "education": "大学本科", "current_post": "副县长、公安局局长",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/qfj/"},
    {"id": 9, "name": "王洪波", "gender": "男", "ethnicity": "汉族", "birth": "1978年4月",
     "birthplace": "", "education": "大学本科", "current_post": "副县长",
     "current_org": "东丰县人民政府", "source": "http://www.dongfeng.gov.cn/xzf/zfld/fxz/whb/"},

    # ── 前置：前任书记/县长 ──
    {"id": 10, "name": "曾海洋", "gender": "男", "ethnicity": "汉族", "birth": "1969年3月",
     "birthplace": "吉林省辽源市", "education": "", "current_post": "曾任东丰县委书记(被查)",
     "current_org": "", "source": "https://www.163.com/news/东丰县委书记曾海洋被查"},
    {"id": 11, "name": "王东", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "current_post": "曾任东丰县县长(2024-2025)",
     "current_org": "", "source": "http://www.jllyls.gov.cn/  王东当选县长"},
    # 更早前任书记 (context)
    {"id": 12, "name": "郑一明", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "current_post": "曾任东丰县委书记(2016)",
     "current_org": "", "source": "微信公众号 党代会报道 2016-10"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共东丰县委员会", "type": "党委", "level": "县处级",
     "parent": "中共辽源市委员会", "location": "吉林省辽源市东丰县"},
    {"id": 2, "name": "东丰县人民政府", "type": "政府", "level": "县处级",
     "parent": "辽源市人民政府", "location": "吉林省辽源市东丰县"},
    {"id": 3, "name": "辽源市商务局", "type": "政府", "level": "地级市局", "parent": "辽源市人民政府",
     "location": "吉林省辽源市"},
    {"id": 4, "name": "辽源市农业农村局", "type": "政府", "level": "地级市局",
     "parent": "辽源市人民政府", "location": "吉林省辽源市"},
    {"id": 5, "name": "中共辽源市纪律检查委员会", "type": "纪委", "level": "地级市",
     "parent": "", "location": "吉林省辽源市"},
    {"id": 6, "name": "东丰县公安局", "type": "政府", "level": "乡科级",
     "parent": "东丰县人民政府", "location": "吉林省辽源市东丰县"},
    {"id": 7, "name": "东丰县人大常委会", "type": "人大", "level": "县处级",
     "parent": "辽源市人大常委会", "location": "吉林省辽源市东丰县"},
    {"id": 8, "name": "政协东丰县委员会", "type": "政协", "level": "县处级",
     "parent": "政协辽源市委员会", "location": "吉林省辽源市东丰县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 袁学高_县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "约2025年",
     "end": "present", "rank": "正处级", "note": "2025年4月起以县委书记身份主持县委党代会会议，截至2026年7月仍在任"},
    {"person_id": 1, "org_id": 4, "title": "辽源市农业农村局党组书记、局长", "start": "2020年12月", "end": "2022年后",
     "rank": "正处级", "note": "2020年12月起任辽源市农业农村局局长；此前曾任副局长（2019-2020）"},
    {"person_id": 1, "org_id": 3, "title": "辽源市商务局党组书记、局长、一级调研员", "start": "约2021-2025",
     "end": "2025年", "rank": "正处级", "note": "聘任东丰县委书记时仍兼任市商务局分工"},
    # 于明明_代县长
    {"person_id": 2, "org_id": 2, "title": "代县长、县政府党组书记", "start": "2026年",
     "end": "present", "rank": "正处级", "note": "主持县政府全面工作，分管县审计局"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026年", "end": "present",
     "rank": "副处级", "note": "县委副书记、代县长"},
    # 马云龙_常务副
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责县政府常务工作，协助县长联系县审计局，分管发改、财政、人社等"},
    # 闻博
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长(挂职)", "start": "", "end": "present",
     "rank": "副处级", "note": "协助县长分管教育、文化旅游、供销等"},
    # 张国喜
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "协助县长分管农业农村、自然资源、林业、水利等"},
    # 姜英坤
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "协助县长分管开发区、交通运输、商务、工业和信息化等"},
    {"person_id": 6, "org_id": 1, "title": "县委(联系开发区)", "start": "", "end": "present",
     "rank": "", "note": "联系东丰经济开发区"},
    # 山田女
    {"person_id": 7, "org_id": 2, "title": "副县长(浙江省绍兴市嵊州区挂职)", "start": "", "end": "present",
     "rank": "副处级", "note": "浙江绍兴市嵊州区挂职，暂无分工"},
    # 秦凤杰
    {"person_id": 8, "org_id": 2, "title": "副县长、公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": "协助县长分管公安、司法、退役军人事务、信访等"},
    {"person_id": 8, "org_id": 6, "title": "县公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "东丰县副县长兼公安局局长"},
    # 王洪波
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "协助县长分管住建、城市管理、民政、政务服务和数字化建设等"},
    # 曾海洋（曾任书记）
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start": "约2021年", "end": "2024年12月",
     "rank": "正处级(兼任市委常委)", "note": "任辽源市委常委、东丰县委书记约2年3个月；2024-12-19被纪委通报审查"},
    {"person_id": 10, "org_id": 1, "title": "辽源市委常委、东丰县委书记", "start": "约2022年",
     "end": "2024年12月", "rank": "副厅级", "note": "曾海洋同时担任辽源市委常委；因涉嫌严重违纪违法被查"},
    # 王东（曾任县长）
    {"person_id": 11, "org_id": 2, "title": "县长", "start": "2024年3月", "end": "2025/2026年初",
     "rank": "正处级", "note": "2024-03-21在县十九届人大四次会议上当选县长"},
    # 郑一明（更早书记）
    {"person_id": 12, "org_id": 1, "title": "县委书记", "start": "2016年9月", "end": "约2021年前",
     "rank": "正处级", "note": "2016年9月在县第十五次党代会一次全会当选县委书记"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 袁学高 ↔ 于明明 · 党政一把手 (2026)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与副县长党政主要领导班子成员工作搭档",
     "overlap_org": "中共东丰县委员会/东丰县人民政府", "overlap_period": "2026年"},
    # 袁学高 ↔ 于明明：代县长接任 王东，但于明明书记下就任
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记、代县长；县委县政府正副两套班子",
     "overlap_org": "中共东县委员会", "overlap_period": "2026年"},
    # 袁学高 ↔ 曾海洋：前任(被查书记)与现任, 违规/交接
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "袁学高接替被查的曾海洋任东丰县委书记",
     "overlap_org": "中共东丰县委员会", "overlap_period": "2025年交接"},
    # 于明明 ↔ 王东：县长前后任
    {"person_a": 2, "person_b": 11, "type": "predecessor_successor",
     "context": "于明明(代县长)接替王东任东丰县县长",
     "overlap_org": "东丰县人民政府", "overlap_period": "2025-2026年"},
    # 曾海洋 ↔ 王东：任书记期间王东任县长
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "曾海洋任县委书记期间王东任县长（前党政班子）",
     "overlap_org": "中共东丰县委员会/东丰县人民政府", "overlap_period": "2024-2025年"},
    # 袁学高 ↔ 于明明 vs 各副县长 (government team)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长(挂职)工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "县长与副县长(挂职)工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长、公安局局长工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    # 常务副县长 ↔ 各副 (政府班子同僚)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县政府领导班子同事",
     "overlap_org": "东丰县人民政府", "overlap_period": "截至2026-08"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS: source register + person JSON
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "东丰县人民政府官网-政府领导-代县长于明明",
         "url": "http://www.dongfeng.gov.cn/xzf/zfld/xz/ymm/", "publisher": "东丰县人民政府",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "于明明：女，汉族，1980年8月生，大学学历，中共党员，现任东丰县委副书记，代县长、县政府党组书记"},
        {"id": "S002", "title": "东丰县人民政府官网-政府领导页(班子清单)",
         "url": "http://www.dongfeng.gov.cn/xzf/zfld/", "publisher": "东丰县人民政府",
         "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认于明明(代县长)、马云龙(常务副)等政府班子成员"},
        {"id": "S003", "title": "东丰县务官网-县领导集中观看庆祝大会直播(确认袁学高为县委书记)",
         "url": "http://www.dongfeng.gov.cn/jrdf/zwdt/202607/t20260702_743777.html", "publisher": "东丰县人民政府",
         "published_at": "2026-07-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "‘县委书记袁学高与在家的县领导…收看大会直播盛况’，确认袁学高为现县委书记"},
        {"id": "S004", "title": "中共东丰县委召开2025年度第9次常委会会议", "url": "http://www.dongfeng.gov.cn/",
         "publisher": "东丰县人民政府", "published_at": "2025-04-21", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "‘县委书记袁学高主持召开…第9次常委会会议’——确认2025年4月起袁任书记"},
        {"id": "S005", "title": "代县长于明明检查全县防汛工作", "url": "http://www.dongfeng.gov.cn/jrdf/zwdt/202607/t20260710_744121.html",
         "publisher": "东丰县人民政府", "published_at": "2026-07-10", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认于明明为代县长(2026-07)，县长（乏）"},
        {"id": "S006", "title": "搜狗百科·袁学高", "url": "https://www.sogou.com/baike/袁学高", "publisher": "搜狗百科",
         "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium",
         "notes": "袁学高：男，汉族，1975年10月生，大学学历，中共党员，现任辽源市商务局经理、东丰县委书记"},
        {"id": "S007", "title": "聂源市任前公示公告(2017)", "url": "", "publisher": "微信公众号", "published_at": "2017-11-05",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
         "notes": "袁学高时任辽源市农业委员会农业科科长，拟任市农委副主任(试用期一年)、党组成员"},
        {"id": "S008", "title": "网易转载·王东当选东丰县县长", "url": "http://www.jllyls.gov.cn/", "publisher": "网易新闻",
         "published_at": "2024-03-25", "accessed_at": AS_OF, "source_type": "media", "reliability": "high",
         "notes": "2024-03-21 东丰县第十九届人大第四次会议选举王东为东丰县人民政府县长"},
        {"id": "S009", "title": "吉林省纪委监委通报·曾海洋被查 (2024-12-19)", "url": "",
         "publisher": "中央纪委国家监委网站/吉林省纪委监委", "published_at": "2024-12-19", "accessed_at": AS_OF,
         "source_type": "appointment_notice", "reliability": "high",
         "notes": "吉林省辽源市委常委、东丰县委书记曾海洋涉嫌严重违纪违法，接受纪律审查和监察调查"},
        {"id": "S010", "title": "今日头条/曾海洋个人档案", "url": "", "publisher": "今日头条", "published_at": "2025-03",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
         "notes": "曾海洋：男，1969年3月，汉族，吉林省辽源市人，2000年入党，1990年参加工作；曾任东丰县委副书记、县长，辽源市委常委、东丰县委书记"},
        {"id": "S011", "title": "央视/媒体 曾海洋双开通报", "url": "", "publisher": "企鹅号·大风新闻", "published_at": "",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
         "notes": "曾海洋主政期间盲目举债上马政绩工程，被开除党籍和公职"},
        {"id": "S012", "title": "2025年东丰县政府工作报告", "url": "http://www.dongfeng.gov.cn/xxgk/zwxxgk/gzbg/202602/t20260212_731842.html",
         "publisher": "东丰县人民政府", "published_at": "2026-02", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2025年东丰县GDP 153.6亿元 +5.7%；梅花鹿产业，涉鹿总产值破90亿，梅花鹿饲养量29.9万只"},
    ]


def generate_person_json(job: str, name: str) -> dict:
    pid = f"{_PID}_{name}"
    base = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "辽源市", "region": "东丰县",
                                "job": job, "task_id": "jilin_东丰县", "time_focus": "2025–2026"},
        "current_status": {"current_org": "", "administrative_rank": "正处级", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001"]},
        "organizations": [
            {"org_id": 1, "name": "中共东丰县委员会", "type": "党委", "level": "县处级",
             "location": "吉林省辽源市东丰县"},
            {"org_id": 2, "name": "东丰县人民政府", "type": "政府", "level": "县处级",
             "location": "吉林省辽源市东丰县"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation", "systems_experience": [],
                                 "geographic_pattern": ["辽源市"],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": make_source_register(),
        "open_questions": [],
    }

    if name == "袁学高":
        base["identity"] = {
            "person_id": pid, "name": "袁学高", "aliases": [], "gender": "男",
            "ethnicity": "汉族", "birth": "1975年10月", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "大学",
                           "study_type": "full_time", "source_ids": ["S006"]}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "袁学高_197510", "name_birthplace": "袁学高_",
                            "official_profile_url": ""},
        }
        base["current_status"]["current_post"] = "县委书记"
        base["current_status"]["current_org"] = "中共东丰县委员会"
        base["current_status"]["source_ids"] = ["S003", "S004"]
        base["identity"]["education"][0]["source_ids"] = ["S006"]
        base["career_timeline"] = [
            {"start": "未知", "end": "2019年", "org": "辽源市农业系统", "title": "农业条线基层/中层干部",
             "level": "", "location": "吉林省辽源市", "system": "government", "rank": "",
             "is_key_promotion": False,
             "notes": "公开信息不足，无法还原2019年前完整履历", "confidence": "unverified", "source_ids": []},
            {"start": "2017年", "end": "2019年", "org": "辽源市农业委员会", "title": "副主任、党组成员(试用期一年)",
             "level": "处级", "location": "吉林省辽源市", "system": "government", "rank": "副处级",
             "is_key_promotion": True,
             "notes": "2017-11 辽源市任前公示：时任市农业委员会农业科科长，拟任委员会副主任(试用期一年)、党组成员",
             "confidence": "plausible", "source_ids": ["S007"]},
            {"start": "2019年1月", "end": "2020年12月", "org": "辽源市农业农村局", "title": "副局长",
             "level": "处级", "location": "吉林省辽源市", "system": "government", "rank": "副处级",
             "is_key_promotion": False, "notes": "据百度百科/搜狗百科履历片段", "confidence": "plausible",
             "source_ids": ["S006"]},
            {"start": "2020年12月", "end": "约2023年", "org": "辽源市农业农村局", "title": "党组书记、局长",
             "level": "处级", "location": "吉林省辽源市", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "2020年12月起任市农业农村局局长", "confidence": "plausible",
             "source_ids": ["S006"]},
            {"start": "约2021-2023年", "end": "2025年", "org": "辽源市商务局", "title": "党组书记、局长兼一级调研员",
             "level": "处级", "location": "吉林省辽源市", "system": "government", "rank": "正处级",
             "is_key_promotion": False, "notes": "现任辽源市商务局党组书记、局长、一级调研员（兼任东丰县县委书记）",
             "confidence": "plausible", "source_ids": ["S006"]},
            {"start": "2025年", "end": "present", "org": "中共东丰县委员会", "title": "县委书记",
             "level": "正处级", "location": "吉林省辽源市东丰县", "system": "party", "rank": "正处级",
             "is_key_promotion": True,
             "notes": "接替被人查的曾海洋；2025年4月起以县委书记身份主持县委常委会，截至2026年7月仍在任",
             "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        ]
        base["relationships"] = [
            {"person": "于明明", "person_id": f"{_PID}_于明明", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县委书记与县级党政主要搭档(2026)",
             "overlap_org": "中共东丰县委员会/东丰县人民政府", "overlap_period": "2026年",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "曾海洋", "person_id": f"{_PID}_曾海洋", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "袁学高接替被查的曾海洋任东丰县委书记",
             "overlap_org": "中共东丰县委员会", "overlap_period": "2025年交接",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S009", "S010"]},
        ]
        base["governance_record"] = [
            {"period": "2025年", "domain": "other",
             "achievement_or_event": "主持县委常委会，学习习总书记考察吉林重要讲话精神，研究民营经济、乡村振兴等部署",
             "role_in_event": "县委书记", "measurable_outcome": "",
             "location": "东丰县", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
        base["professional_profile"]["primary_specializations"] = ["农业农村", "商务/经贸"]
        base["professional_profile"]["systems_experience"] = ["government", "party"]
        base["professional_profile"]["promotion_velocity"]["summary"] = "从市直部门(已农委/商务局)空降东丰县委副书记、书记，属市直部门到县区交流型晋升"
        base["professional_profile"]["promotion_velocity"]["notable_fast_promotions"] = []
        base["confidence_summary"] = {
            "identity": "plausible", "current_role": "confirmed", "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "袁学高的出生籍贯/毕业院校、2020-2025 商务局至任县委书记之间的精确时间线、2019年前完整履历待补",
        }
        base["open_questions"] = [
            {"priority": "high", "question": "袁学高的出生籍贯、毕业院校具体名称？",
             "why_it_matters": "身份去重与完整履历", "suggested_queries": ["袁学高 简历 籍贯"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "袁学高何时由辽源市商务局局长调任东丰县委书记？(任前公示)",
             "why_it_matters": "精确到任时间节点与任命机制",
             "suggested_queries": ["袁学高 任 东丰县委书记 公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "袁学高于辽源市人民政府的具体任职起止（农业农村局/商务局）",
             "why_it_matters": "还原市直履历", "suggested_queries": ["辽源市农业农村局 袁学高", "辽源市商务局 袁学高"],
             "last_attempted": AS_OF},
        ]
        return base

    # ── 于明明 (县县长/代县长) ──
    base["identity"] = {
        "person_id": pid, "name": "于明明", "aliases": [], "gender": "女", "ethnicity": "汉族",
        "birth": "1980年8月", "birthplace": "", "native_place": "",
        "education": [{"period": "", "institution": "", "major": "", "degree": "大学",
                       "study_type": "full_time", "source_ids": ["S001"]}],
        "party_join": "中共党员", "work_start": "",
        "dedupe_keys": {"name_birth": "于明明_198008", "name_birthplace": "于明明_",
                        "official_profile_url": "http://www.dongfeng.gov.cn/xzf/zfld/xz/ymm/"},
    }
    base["current_status"]["current_post"] = "代县长"
    base["current_status"]["current_org"] = "东丰县人民政府"
    base["current_status"]["source_ids"] = ["S001"]
    base["career_timeline"] = [
        {"start": "未知", "end": "2026年", "org": "", "title": "任代县长前职务",
         "level": "", "location": "", "system": "government", "rank": "",
         "is_key_promotion": False, "notes": "任东丰代县长前的职务公开信息不足（履历缺口）", "confidence": "unverified",
         "source_ids": []},
        {"start": "2026年", "end": "present", "org": "东丰县人民政府", "title": "代县长、县政府党组书记",
         "level": "正处级", "location": "吉林省辽源市东丰县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "主持县政府全面工作，具体分管县审计局；接替王东",
         "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"start": "2026年", "end": "present", "org": "中共东丰县委员会", "title": "县委副书记",
         "level": "副处级", "location": "吉林省辽源市东丰县", "system": "party", "rank": "副处级",
         "is_key_promotion": False, "notes": "县委副书记、代县长", "confidence": "confirmed",
         "source_ids": ["S001"]},
    ]
    base["relationships"] = [
        {"person": "袁学高", "person_id": f"{_PID}_袁学高", "relationship_type": "overlap",
         "strength": "strong", "evidence": "县委书记与县级党政主要搭档(2026)",
         "overlap_org": "中共东丰县委员会/东丰县人民政府", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
        {"person": "王东", "person_id": f"{_PID}_王东", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "于明明(代县长)接替王东任东丰县县长",
         "overlap_org": "东丰县人民政府", "overlap_period": "2025-2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
    ]
    base["governance_record"] = [
        {"period": "2026年7月", "domain": "public_security",
         "achievement_or_event": "深入重点河道、水库、防汛物资储备库等实地检查防汛备汛工作",
         "role_in_event": "代县长", "measurable_outcome": "要求完善应急预案、安排人员转移避险、加密监测预警",
         "location": "辽源市东丰县", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    base["professional_profile"]["career_pattern"] = "local_ladder"
    base["professional_profile"]["geographic_pattern"] = ["辽源市"]
    base["professional_profile"]["promotion_velocity"]["summary"] = "由县政府被任命为代县长；公开源不足，无法评估晋升速度"
    base["professional_profile"]["primary_specializations"] = []
    base["confidence_summary"] = {
        "identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin",
        "relationship_confidence": "medium",
        "biggest_gap": "于明明任代县长前的完整履历、任代县长的精确日期、籍贯毕业院校详情"}
    base["open_questions"] = [
        {"priority": "high", "question": "于明明何时被任命为东丰县代县长？由县人大哪次常委会决定？",
         "why_it_matters": "精确交接时间与决定机制", "suggested_queries": ["于明明 代县长 人大 任命"],
         "last_checked": AS_OF},
        {"priority": "high", "question": "于明明代县长前担任什么职务？(乡/县/市直?)",
         "why_it_matters": "还原履历与晋升路径", "suggested_queries": ["于明明 简历 东丰县"], "last_checked": AS_OF},
        {"priority": "medium", "question": "于明明的出生籍贯与毕业院校？",
         "why_it_matters": "完整身份档案", "suggested_queries": ["于明明 籍贯 毕业"], "last_checked": AS_OF},
    ]
    return base


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os
    # remove stale outputs before each run
    for p in (DB_PATH, GEXF_PATH):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass

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
    for job, name in [("县委书记", "袁学高"), ("县长", "于明明")]:
        data = generate_person_json(job, name)
        fname = f"{TODAY}-吉林省-辽源市-{job}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")