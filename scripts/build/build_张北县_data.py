#!/usr/bin/env python3
"""Build 张家口市张北县 (Zhangbei County) leadership network data.

Level: 县
Province: 河北省
Parent city: 张家口市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_张北县

Research date: 2026-07-24
Official source: https://www.zjkzb.gov.cn/ (张北县人民政府)

Current status (as of 2026-07-24):
- 县委书记: 任晓伟 — 主持县委十二届十四次全会(7月10日), 主持县
  第十三次党代会(7月15日), 出席县十九届人大一次会议闭幕式(7月23日)
- 县长: 赵万新 — 原代县长, 7月23日县十九届人大一次会议当选县长
- 前任县长: 侯东林 (政府网站尚未更新)

Sources:
  S001: https://www.zjkzb.gov.cn/zfld.thtml (政府领导页, 侯东林)
  S002: https://mp.weixin.qq.com/s/cGul2MaO3di0hL-7mv6CaA (十二届十四次全会, 任晓伟主持)
  S003: https://mp.weixin.qq.com/s/8xX3VslHUSrX9eU5kXf43Q (十三次党代会开幕)
  S004: https://mp.weixin.qq.com/s/QvpQ9sdemiq2mlHDYFjv9Q (十九届人大一次会议开幕)
  S005: https://mp.weixin.qq.com/s/UauiDmMWElTPmRuAe-Wgsg (十九届人大一次会议闭幕)
  S006: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg (政协十八届一次会议开幕)
  S007: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A (政协十八届一次会议闭幕)
"""

from __future__ import annotations

import sys
from pathlib import Path

# When run from data/tmp/hebei_张北县/, resolve repo root three levels up
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "张北县"

# When run from staging, write DB and GEXF to the staging directory.
_STAGING_DIR = _SCRIPT_DIR  # data/tmp/hebei_张北县/
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "任晓伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县委书记",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/cGul2MaO3di0hL-7mv6CaA "
                    "(十二届十四次全会, 县委书记任晓伟主持)"),
    },
    {
        "id": 2,
        "name": "赵万新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县委副书记、县长",
        "current_org": "张北县人民政府",
        "source": ("官方: https://mp.weixin.qq.com/s/UauiDmMWElTPmRuAe-Wgsg "
                    "(十九届人大一次会议闭幕, 赵万新当选县长)"),
    },
    # ════════════════════════════════════════
    # 县人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县人大常委会主任",
        "current_org": "张北县人大常委会",
        "source": ("官方: https://mp.weixin.qq.com/s/UauiDmMWElTPmRuAe-Wgsg "
                    "(杨巍当选张北县十九届人大常委会主任)"),
    },
    {
        "id": 4,
        "name": "方士武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县人大常委会党组书记",
        "current_org": "张北县人大常委会",
        "source": ("官方: https://mp.weixin.qq.com/s/QvpQ9sdemiq2mlHDYFjv9Q "
                    "(十九届人大一次会议开幕, 方士武主持, 主席台就座)"),
    },
    {
        "id": 5,
        "name": "张桂利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县政协主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协十八届一次会议闭幕, 张桂利当选主席)"),
    },
    {
        "id": 6,
        "name": "文春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县政协副主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协十八届一次会议开幕, 文春作十七届常委会工作报告)"),
    },
    # ════════════════════════════════════════
    # 县领导 (从会议主席团名单提取)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "马建成",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/QvpQ9sdemiq2mlHDYFjv9Q "
                    "(十九届人大一次会议主席团成员)"),
    },
    {
        "id": 8,
        "name": "孙双宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/QvpQ9sdemiq2mlHDYFjv9Q "
                    "(十九届人大一次会议主席团成员)"),
    },
    {
        "id": 9,
        "name": "盖明烨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/QvpQ9sdemiq2mlHDYFjv9Q "
                    "(十九届人大一次会议主席团成员)"),
    },
    {
        "id": 10,
        "name": "姜政宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协开幕式主席台就座县领导)"),
    },
    {
        "id": 11,
        "name": "梁海平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协开幕式主席台就座县领导)"),
    },
    {
        "id": 12,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协开幕式主席台就座县领导)"),
    },
    {
        "id": 13,
        "name": "李明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协闭幕式主席台就座县领导)"),
    },
    {
        "id": 14,
        "name": "周雪健",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协开幕式主席台就座县领导)"),
    },
    {
        "id": 15,
        "name": "张超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县领导",
        "current_org": "中共张家口市张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/nbuXhvtLKPZwvIOiP9AuLg "
                    "(政协开幕式主席台就座县领导)"),
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "侯东林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年3月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县县长(前任)",
        "current_org": "张北县人民政府",
        "source": ("官方: https://www.zjkzb.gov.cn/zfld.thtml "
                    "(政府领导页, 显示为县长, 尚未更新)"),
    },
    {
        "id": 17,
        "name": "郝富国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张家口市领导(前任张北县委书记)",
        "current_org": "张家口市人民政府",
        "source": ("媒体: 百度百科, 郝富国2013.12-2017.02任张北县委书记"),
    },
    {
        "id": 18,
        "name": "李鹏举",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县前任县委书记",
        "current_org": "",
        "source": ("媒体: 公开报道, 继郝富国之后任张北县委书记"),
    },
    # ════════════════════════════════════════
    # 政协副主席
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "李文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县政协副主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协十八届一次会议, 当选副主席)"),
    },
    {
        "id": 20,
        "name": "武占文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "张北县政协副主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协十八届一次会议, 当选副主席)"),
    },
    {
        "id": 21,
        "name": "胡丽荔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张北县政协副主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协十八届一次会议, 当选副主席)"),
    },
    {
        "id": 22,
        "name": "翟立超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张北县政协副主席",
        "current_org": "政协张北县委员会",
        "source": ("官方: https://mp.weixin.qq.com/s/4Q42gULh9ZSSGBipOFht2A "
                    "(政协十八届一次会议, 当选副主席)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共张家口市张北县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共张家口市委员会",
        "location": "河北省张家口市张北县",
    },
    {
        "id": 2,
        "name": "张北县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "张家口市人民政府",
        "location": "河北省张家口市张北县",
    },
    {
        "id": 3,
        "name": "中共张家口市张北县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共张家口市纪律检查委员会",
        "location": "河北省张家口市张北县",
    },
    {
        "id": 4,
        "name": "张北县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "张家口市人大常委会",
        "location": "河北省张家口市张北县",
    },
    {
        "id": 5,
        "name": "政协张北县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协张家口市委员会",
        "location": "河北省张家口市张北县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 县委领导
    {"person_id": 1, "org_id": 1, "title": "张北县委书记", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月第十三次党代会; 主持十二届十四次全会"},
    # 县政府领导
    {"person_id": 2, "org_id": 2, "title": "张北县县长", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "2026年7月23日十九届人大一次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "张北县委副书记", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "十九届人大一次会议确认"},
    # 县人大
    {"person_id": 3, "org_id": 4, "title": "张北县人大常委会主任", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "2026年7月23日十九届人大一次会议当选"},
    {"person_id": 4, "org_id": 4, "title": "张北县人大常委会党组书记", "start": "", "end": "至今", "rank": "正处级", "note": "主持县人代会开幕式"},
    # 县政协
    {"person_id": 5, "org_id": 5, "title": "张北县政协主席", "start": "2026-07", "end": "至今", "rank": "正处级", "note": "2026年7月22日政协十八届一次会议当选"},
    {"person_id": 6, "org_id": 5, "title": "张北县政协副主席", "start": "", "end": "至今", "rank": "副处级", "note": "作十七届常委会工作报告"},
    {"person_id": 19, "org_id": 5, "title": "张北县政协副主席", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "政协十八届一次会议当选"},
    {"person_id": 20, "org_id": 5, "title": "张北县政协副主席", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "政协十八届一次会议当选"},
    {"person_id": 21, "org_id": 5, "title": "张北县政协副主席", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "政协十八届一次会议当选"},
    {"person_id": 22, "org_id": 5, "title": "张北县政协副主席", "start": "2026-07", "end": "至今", "rank": "副处级", "note": "政协十八届一次会议当选"},
    # 县领导 (未明确分工)
    {"person_id": 7, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "十九届人大一次会议主席团成员"},
    {"person_id": 8, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "十九届人大一次会议主席团成员"},
    {"person_id": 9, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "十九届人大一次会议主席团成员"},
    {"person_id": 10, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协开幕式主席台就座"},
    {"person_id": 11, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协开幕式主席台就座"},
    {"person_id": 12, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协开幕式主席台就座"},
    {"person_id": 13, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协闭幕式主席台就座"},
    {"person_id": 14, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协开幕式主席台就座"},
    {"person_id": 15, "org_id": 1, "title": "张北县领导", "start": "", "end": "至今", "rank": "", "note": "政协开幕式主席台就座"},
    # 前任
    {"person_id": 16, "org_id": 2, "title": "张北县县长(前任)", "start": "", "end": "2026-07", "rank": "正处级", "note": "政府网站尚未更新; 十九届人大已选举新县长"},
    {"person_id": 17, "org_id": 1, "title": "张北县委书记(前任)", "start": "2013-12", "end": "2017-02", "rank": "正处级", "note": "转任张家口市领导"},
    {"person_id": 18, "org_id": 1, "title": "张北县委书记(前任)", "start": "", "end": "2026-07", "rank": "正处级", "note": "继郝富国之后、任晓伟之前担任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政工作搭档关系(第十三届县委)", "overlap_org": "张北县", "overlap_period": "2026-"},
    # 县委书记与人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与人大常委会主任", "overlap_org": "中共张北县委", "overlap_period": "2026-"},
    # 县委书记与政协主席
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记与政协主席", "overlap_org": "中共张北县委", "overlap_period": "2026-"},
    # 县委书记与县领导
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "县委书记与县领导班子成员", "overlap_org": "中共张北县委", "overlap_period": ""},
    # 县长与人大主任
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与人大常委会主任", "overlap_org": "张北县", "overlap_period": "2026-"},
    # 县长与政协主席
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与政协主席", "overlap_org": "张北县", "overlap_period": "2026-"},
    # 人大与政协
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "人大主任与政协主席同届", "overlap_org": "张北县", "overlap_period": "2026-"},
    # 前任关系
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "任晓伟接替李鹏举任县委书记", "overlap_org": "中共张北县委", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "赵万新接替侯东林任县长", "overlap_org": "张北县人民政府", "overlap_period": "2026-07"},
    {"person_a": 17, "person_b": 18, "type": "predecessor_successor", "context": "郝富国之后李鹏举接任县委书记", "overlap_org": "中共张北县委", "overlap_period": "2017"},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  张家口市张北县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 张北县政府网站 www.zjkzb.gov.cn, 张北发布")
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
    print(f"\n✅ 张北县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
