#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
都安瑶族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和核心人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 河池市
Region: 都安瑶族自治县（瑶族自治县，全国乡村振兴重点帮扶县，喀斯特石漠化地区）
Targets: 县委书记 & 县长
Research Date: 2026-08-06

Research Note (sources: 都安瑶族自治县人民政府门户网站 http://www.duan.gov.cn/，融媒体中心，均 HTTP 可访问):
  2026年6-7月发生县委书记更替：
  - 李建君（截至2026-06-15仍为自治县党委书记）→ 覃平（2026-07起为自治县党委书记）
  - 中国共产党都安瑶族自治县第十六次代表大会 2026-07-28/29 召开，选举产生第十六届县委委员会。
    覃平致闭幕词并连任/当选第十六届县委书记，周海国代表纪委向大会报告工作（县纪委书记）。
  县长：蓝干宁，男，瑶族，1977年2月生，中共党员，在职研究生学历，现任自治县人民政府党组书记、县长。
  前任县长黄瑞吉约2019-2025-09任都安县县长，2025-09涉嫌严重违纪违法被查（此前曾任巴马县委常委、宣传部长、副县长）。

Sources:
  - http://www.duan.gov.cn/gdtt/t27964005.shtml (2026-07-29 党代会闭幕，覃平致闭幕词、蓝干宁主持)
  - http://www.duan.gov.cn/gddt/t27959305.shtml (2026-07-28 党代会开幕，覃平作报告、周显忠纪委报告)
  - http://www.duan.gov.cn/gddt/t27893748.shtml (2026-07-14 覃平以自治县党委书记主持县委常委会)
  - http://www.duan.gov.cn/xxgk/ldzc/xz/ (县长蓝干宁官方简介)
  - http://www.duan.gov.cn/xxgk/ldzc/ (县政府领导之窗：副县长名单)
  - http://www.duan.gov.cn/xxgk/zfhy/qthy/t27794818.shtml (2026-06-15 李建君任县委书记时主持常委会)
  - http://www.duan.gov.cn/ywdt/zwdt/t27973586.shtml (2026-08-02 覃平主持水域安全专题会、蓝干宁主持部署)
  - 巴马瑶族自治县 build 脚本交叉证据：黄瑞吉曾任巴马常委/宣传部长/副县长后任都安县长（2025-09被查）
  - 河池市：市委书记朱会东（2026-08 全市防汛调度会）、市长王军（前巴马县委书记）
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

SLUG = "都安瑶族自治县"
AS_OF = "2026-08-06"
TODAY = "20260806"

_staging = os.environ.get("STAGING_DIR")
if _staging:
    DB_PATH = os.path.join(_staging, "都安瑶族自治县_network.db")
    GEXF_PATH = os.path.join(_staging, "都安瑶族自治县_network.gexf")
    PERSONS_DIR = _staging
else:
    try:
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR as _REPO_PERSONS
        DB_PATH = DATABASE_DIR / "都安瑶族自治县_network.db"
        GEXF_PATH = GRAPH_DIR / "都安瑶族自治县_network.gexf"
        PERSONS_DIR = _REPO_PERSONS
    except Exception:
        _repo = next(_p for _p in Path(__file__).resolve().parents if (_p / "gov_relation").is_dir())
        if str(_repo) not in sys.path:
            sys.path.insert(0, str(_repo))
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR as _REPO_PERSONS
        DB_PATH = DATABASE_DIR / "都安瑶族自治县_network.db"
        GEXF_PATH = GRAPH_DIR / "都安瑶族自治县_network.gexf"
        PERSONS_DIR = _REPO_PERSONS

try:
    from gov_relation.runner import run_build
    HAS_RUNNER = True
except Exception:
    _repo = next((_p for _p in Path(__file__).resolve().parents if (_p / "gov_relation").is_dir()), None)
    if _repo is None:
        HAS_RUNNER = False
    else:
        if str(_repo) not in sys.path:
            sys.path.insert(0, str(_repo))
        from gov_relation.runner import run_build
        HAS_RUNNER = True

# =========================================================================
# 1. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共都安瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委员会", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 2, "name": "都安瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 3, "name": "都安瑶族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "河池市人大常委会", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 4, "name": "中国人民政治协商会议都安瑶族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协河池市委员会", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 5, "name": "中共都安瑶族自治县纪律检查委员会/都安瑶族自治县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共河池市纪律检查委员会", "location": "广西壮族自治区河池市都安瑶族自治县"},
    {"id": 6, "name": "中共河池市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区河池市"},
    {"id": 7, "name": "河池市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区河池市"},
    {"id": 8, "name": "中共巴马瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委员会", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 9, "name": "巴马瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "河池市人民政府", "location": "广西壮族自治区河池市巴马瑶族自治县"},
    {"id": 10, "name": "中共东兰县委员会", "type": "党委", "level": "县处级", "parent": "中共河池市委员会", "location": "广西壮族自治区河池市东兰县"},
]

# =========================================================================
# 2. PERSONS
# =========================================================================
persons = [
    # ── 核心：县委书记 ──
    {"id": 1, "name": "覃平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "中共都安瑶族自治县委书记", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27893748.shtml;http://www.duan.gov.cn/gddt/t27959305.shtml"},
    # ── 核心：县 长 ──
    {"id": 2, "name": "蓝干宁", "gender": "男", "ethnicity": "瑶族",
     "birth": "1977年2月", "birthplace": "",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县委副书记、县长", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/xz/"},
    # ── 前任县委书记 ──
    {"id": 3, "name": "李建君", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县原县委书记（2026上半年卸任）", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/xxgk/zfhy/qthy/t27794818.shtml"},
    # ── 前任县长（2025-09落马）──
    {"id": 4, "name": "黄瑞吉", "gender": "", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县原县长（2025-09被查）", "current_org": "都安瑶族自治县人民政府",
     "source": "scripts/build/build_巴马瑶族自治县_data.py; news.qq.com/rain/a/20250924A08DLU00"},
    # ── 县委副书记 ──
    {"id": 5, "name": "孙瑞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县委副书记", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27893748.shtml"},
    # ── 县纪委书记 ──
    {"id": 6, "name": "周海国", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县委常委、县纪委书记/监委主任", "current_org": "中共都安瑶族自治县纪律检查委员会",
     "source": "http://www.duan.gov.cn/gddt/t27959305.shtml（代表纪委向16次党代会报告工作）"},
    # ── 县人大主任 ──
    {"id": 7, "name": "谢贵善", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县人大常委会主任", "current_org": "都安瑶族自治县人民代表大会常务委员会",
     "source": "http://www.duan.gov.cn/xxgk/zfhy/qthy/t27794818.shtml"},
    # ── 县政协主席 ──
    {"id": 8, "name": "覃舟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "都安瑶族自治县政协主席", "current_org": "中国人民政治协商会议都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/xxgk/zfhy/qthy/t27794818.shtml"},
    # ── 县委常委/副县长（政府班子成员）──
    {"id": 9, "name": "韦念", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县常委、副县长", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/; http://www.duan.gov.cn/gddt/t27893748.shtml"},
    {"id": 10, "name": "蓝必林", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县常委、副县长", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    # ── 挂职副县长 ──
    {"id": 11, "name": "栾利建", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县副县长（挂职）", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    {"id": 12, "name": "孙龙", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县副县长（挂职）", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    {"id": 13, "name": "李宇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县副县长（挂职）", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    # ── 其他副县长 ──
    {"id": 14, "name": "杨刚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县副县长", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    {"id": 15, "name": "陈燕辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县副县长", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    # ── 县政府办公室主任 ──
    {"id": 16, "name": "韦军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县人民政府办公室主任", "current_org": "都安瑶族自治县人民政府",
     "source": "http://www.duan.gov.cn/xxgk/ldzc/"},
    # ── 县委其他领导（16次党代会主席台前排，新一届常委）──
    {"id": 17, "name": "周小东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县县委常委（16届县委主席台前排）", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27959305.shtml; http://www.duan.gov.cn/gddt/t27964005.shtml"},
    {"id": 18, "name": "马腾", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县县委常委", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27964005.shtml"},
    {"id": 19, "name": "梁丽丹", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县县委常委", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27964005.shtml"},
    {"id": 20, "name": "杨再平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县县委常委", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27964005.shtml"},
    {"id": 21, "name": "彭国安", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "都安瑶族自治县县委常委", "current_org": "中共都安瑶族自治县委员会",
     "source": "http://www.duan.gov.cn/gddt/t27964005.shtml"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 覃平 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "都安瑶族自治县委书记", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": "2026年7月起任自治县党委书记；7-28/29主持召开第十六次党代会并作十五届县委报告，当选/连任十六届县委书记"},
    # 蓝干宁 — 县长
    {"person_id": 2, "org_id": 2, "title": "都安瑶族自治县委副书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "自治县人民政府党组书记、县长，领导政府全面工作；接替2025-09被查的黄瑞吉，接任时间待核"},
    {"person_id": 2, "org_id": 1, "title": "都安瑶族自治县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李建君 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "都安瑶族自治县原县委书记", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "截至2026-06-15仍为自治县党委书记；6月中旬至7月中旬由覃宁接任（去向待核）"},
    # 黄瑞吉 — 前任县长
    {"person_id": 4, "org_id": 2, "title": "都安瑶族自治县委副书记、县长", "start_date": "2019", "end_date": "2025-09", "rank": "县处级正职", "note": "2025年9月涉嫌严重违纪违法被查"},
    {"person_id": 4, "org_id": 8, "title": "巴马瑶族自治县委常委、宣传部部长", "start_date": "", "end_date": "2018", "rank": "县处级副职", "note": "调任都安县前在巴马任职"},
    {"person_id": 5, "org_id": 1, "title": "都安瑶族自治县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十六届县委副书记"},
    {"person_id": 6, "org_id": 5, "title": "都安瑶族自治县纪委书记/监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "代表第十五届县纪委向十六次党代会报告工作"},
    {"person_id": 7, "org_id": 3, "title": "都安瑶族自治县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "列席县委常委会会议"},
    {"person_id": 8, "org_id": 4, "title": "都安瑶族自治县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "列席县委常委会会议"},
    {"person_id": 9, "org_id": 2, "title": "都安瑶族自治县常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府领导之窗列为副县戒，并出席县委常委会（县领导）"},
    {"person_id": 10, "org_id": 2, "title": "都安瑶族自治县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "都安瑶族自治县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "都安瑶族自治县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "都安瑶族自治县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "都安瑶族自治县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "都安瑶族自治县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "都安瑶族自治县政府办公室主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "都安瑶族自治县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十六届县委主席台前排"},
    {"person_id": 18, "org_id": 1, "title": "都安瑶族自治县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "出席县委常委会"},
    {"person_id": 19, "org_id": 1, "title": "都安瑶族自治县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十六届县委主席台前排"},
    {"person_id": 20, "org_id": 1, "title": "都安瑶族自治县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "出席县委会"},
    {"person_id": 21, "org_id": 1, "title": "都安瑶族自治县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十六届县委主席台前排"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 覃平 — 蓝干宁 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "覃平（县委书记）与蓝干宁（县长）为都安县党政一把手，同一班子共事", "overlap_org": "都安瑶族自治县", "overlap_period": "2026-07至今"},
    # 覃平 — 前任书记 李建君 前后任
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "覃平接替李建君任都安县委书记（2026年6-7月交接）", "overlap_org": "中共都安瑶族自治县委员会", "overlap_period": "2026-06/07"},
    # 蓝干宁 — 前任县长 黄瑞吉 前后任
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "蓝干宁接替黄瑞吉任都安县长；黄瑞吉2025-09被查，蓝干宁接任时间待核", "overlap_org": "都安瑶族自治县人民政府", "overlap_period": "2025-09 后"},
    {"person_a": 4, "person_b": 2, "type": "cross_county_exchange", "context": "黄瑞吉（前巴马常委/宣传部部长/副县长，至2018）接任都市县长，体现河池市内巴马-都市干部交流；蓝干宁（现任县长）为其继任", "overlap_org": "河池市/都安", "overlap_period": "2018-2025"},
    # 覃平 — 各常委
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "覃平任县委书记，周海国任县纪委书记、监委主任", "overlap_org": "中共都安瑶族自治县委员会", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "覃平任县委书记，韦念任县政府分管领导（县领导）", "overlap_org": "都安瑶族自治县人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "蓝干宁县长与副县长韦念进入政府班子正副职", "overlap_org": "都安瑶族自治县人民政府", "overlap_period": ""},
    # 蓝干宁 — 人大/政协
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "蓝干宁（县长）与谢贵善（县人大常委会主任）同列出席、列席县委常委会", "overlap_org": "都安瑶族自治县", "overlap_period": "2026-06/07"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "蓝干宁（县长）与覃舟（县政协主席）同列出席、列席县委常委会", "overlap_org": "都安瑶族自治县", "overlap_period": "2026-06/07"},
    # 覃平 — 县委副书记孙瑞
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "覃平书记与专职副书记孙瑞共事（十六届县委）", "overlap_org": "中共都安瑶族自治县委员会", "overlap_period": "2026-07至今"},
]

# =========================================================================
# 5. BUILD (DB + GEXF + Person JSON)
# =========================================================================

def write_person_json(person, suffix):
    fname = f"{TODAY}-广西壮族自治区-河池市-{suffix}-{person['name']}.json"
    fpath = os.path.join(PERSONS_DIR, fname)
    is_top = ("县委书记" in person["current_post"] or "县长" in person["current_post"])
    rank = "县处级正职" if is_top else "县处级副职"
    is_current = "原" not in person.get("current_post", "")
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "河池市",
            "region": "都安瑶族自治县",
            "job": suffix,
            "task_id": "guangxi_都安瑶族自治县",
            "time_focus": "截至2026年8月"
        },
        "identity": {
            "person_id": f"guangxi_duan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", "") or "", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": person["name"] + person.get("birth", ""), "name_birthplace": "", "official_profile_url": "http://www.duan.gov.cn/xxgk/ldzc/"}
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": rank if is_current else "县处级副职" if "副" in (person.get("current_post") or "") else "",
            "as_of": AS_OF,
            "is_current_confirmed": "原" not in person.get("current_post", ""),
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {"start": "", "end": "present", "org": person.get("current_org", ""), "title": person.get("current_post", ""), "level": "县处级", "location": "广西河池市都安瑶族自治县", "system": "party" if "书记" in (person.get("current_post") or "") else "government", "rank": rank if is_current else "", "is_key_promotion": is_current, "notes": "截至" + AS_OF + "公开信息", "confidence": "confirmed", "source_ids": ["S001"]}
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [
            {"period": "2026", "domain": "rural_revitalization", "achievement_or_event": "六都安建设（富裕、活力、宜居、生态、幸福、和谐）+ 乡村全面振兴、高质量发展", "role_in_event": "领导推动", "measurable_outcome": "", "location": "都安瑶族自治县", "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["广西壮族自治区河池市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["六个都安建设", "乡村全面振兴"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id": "S001", "title": "都安瑶族自治县人民政府门户网站—领导之窗", "url": "http://www.duan.gov.cn/xxgk/ldzc/", "publisher": "都安县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县政府领导名单与蓝干宁县长简介"},
            {"id": "S002", "title": "中国共产党都安瑶族自治县第十六次代表大会闭幕", "url": "http://www.duan.gov.cn/gddt/t27964005.shtml", "publisher": "都安县融媒体中心", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认覃平连任书记、蓝干宁主持"},
            {"id": "S003", "title": "覃平主持召开县委常委会会议", "url": "http://www.duan.gov.cn/gddt/t27893748.shtml", "publisher": "都安县融媒体中心", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认覃平任自治县党委书记"}
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed" if is_current else "plausible", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "出生年月、籍贯、教育背景、完整职业履历（尤其是覃平、李建君、黄瑞吉）缺失"},
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年月、籍贯、民族、教育背景与完整工作履历", "why_it_matters": "身份识别与网络时间线分析核心字段", "suggested_queries": [f"{person['name']} 都安 简历", f"{person['name']} 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}近期人事调整的joined时间（就任起始年月）", "why_it_matters": "确认现职任职起点，衔接前任交接", "suggested_queries": [f"{person['name']} 就任 都安"], "last_attempted": AS_OF}
        ]
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")


if __name__ == "__main__":
    print(f"Building {SLUG} data artifacts...")
    if HAS_RUNNER:
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
    else:
        raise RuntimeError("gov_relation.runner unavailable")
    core = {1: "县委书记", 2: "县长", 3: "原县委书记", 4: "原县长"}
    for pid in core:
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(p, core[pid])
    print("Done!")
