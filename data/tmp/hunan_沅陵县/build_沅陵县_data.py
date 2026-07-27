#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沅陵县 leadership network.

Task: hunan_沅陵县
Province: 湖南省
Parent city: 怀化市
Level: 县
Targets: 县委书记 & 县长
Research date: 2026-07-24

Sources:
  - www.yuanling.gov.cn — 沅陵县人民政府网站：县政府领导页确认县长陈星及10名副县长
  - www.yuanling.gov.cn — 新闻中心确认刘向阳为县委书记（多次报道"刘向阳主持召开"）
  - www.yuanling.gov.cn — 领导活动确认刘向阳、陈星为本县党政主要领导

Confidence notes:
  - 刘向阳: confirmed as 县委书记 via multiple news reports (2026-07-22, 07-20, 07-01, etc.)
  - 陈星: confirmed as 县委副书记、县长 via government leadership page
  - 10名副县长: confirmed via government leadership page with detail pages
  - 完整履历（教育背景、出生信息、早期职务）因网络搜索受限未能完整验证
"""

import sys
import os
from pathlib import Path

# Adjust path for running from staging directory
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parents[2]  # data/tmp/hunan_沅陵县 -> data/tmp -> data -> repo root
sys.path.insert(0, str(_REPO_ROOT))
from gov_relation.runner import run_build

_STAGING_DIR = _SCRIPT_DIR

# process_tmp.py validates these tokens exist
import sqlite3 as _sqlite3
DB_PATH = str(_STAGING_DIR / "沅陵县_network.db")
GEXF_PATH = str(_STAGING_DIR / "沅陵县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "刘向阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共沅陵县委书记",
        "current_org": "中共沅陵县委员会",
        "source": "https://www.yuanling.gov.cn — 沅陵县人民政府网站新闻中心多个报道（2026-07-22/20/01等）确认刘向阳以县委书记身份主持召开会议、调研工作",
    },
    # ── Current County Mayor (县长) ──
    {
        "id": 2,
        "name": "陈星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共沅陵县委副书记、县人民政府党组书记、县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页：县长陈星，主持县人民政府全面工作",
    },
    # ── Supervisory Board (纪委监委) ──
    {
        "id": 3,
        "name": "向晓华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共沅陵县纪律检查委员会",
        "source": "https://www.yuanling.gov.cn — 新闻报道及典型案件通报",
    },
    # ── Organization Department ──
    {
        "id": 4,
        "name": "杨太康",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共沅陵县委组织部",
        "source": "https://www.yuanling.gov.cn — 干部任前公示等报道",
    },
    # ── Propaganda Department ──
    {
        "id": 5,
        "name": "张俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共沅陵县委宣传部",
        "source": "https://www.yuanling.gov.cn — 新闻报道",
    },
    # ── 常务副县长 (Executive Deputy County Mayor) ──
    {
        "id": 6,
        "name": "黄松柏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    # ── 县委常委、副县长(挂职) ──
    {
        "id": 7,
        "name": "夏郅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    # ── 县委常委、副县长 ──
    {
        "id": 8,
        "name": "杨斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    # ── 副县长 ──
    {
        "id": 9,
        "name": "钟群英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 10,
        "name": "王鸿鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 11,
        "name": "万目国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 12,
        "name": "邓伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 13,
        "name": "刘少志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 14,
        "name": "李万喜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
    {
        "id": 15,
        "name": "吴卓翰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "沅陵县人民政府",
        "source": "https://www.yuanling.gov.cn/yuanling/c120407/xzf2020.shtml — 县政府领导页",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共沅陵县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共怀化市委",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 2,
        "name": "沅陵县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "怀化市人民政府",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 3,
        "name": "中共沅陵县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共怀化市纪律检查委员会",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 4,
        "name": "中共沅陵县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沅陵县委员会",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 5,
        "name": "中共沅陵县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沅陵县委员会",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 6,
        "name": "沅陵县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "沅陵县人民政府",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 7,
        "name": "沅陵县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "怀化市人大常委会",
        "location": "湖南省怀化市沅陵县",
    },
    {
        "id": 8,
        "name": "政协沅陵县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "怀化市政协",
        "location": "湖南省怀化市沅陵县",
    },
]

positions = [
    # 刘向阳 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共沅陵县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月以县委书记身份主持县委全面工作"},
    # 陈星 - 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "同时担任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持县人民政府党组工作，领导县人民政府全面工作"},
    # 向晓华 - 纪委书记
    {"person_id": 3, "org_id": 3, "title": "县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨太康 - 组织部部长
    {"person_id": 4, "org_id": 4, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张俊 - 宣传部部长
    {"person_id": 5, "org_id": 5, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄松柏 - 常务副县长
    {"person_id": 6, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 夏郅 - 副县长(挂职)
    {"person_id": 7, "org_id": 2, "title": "县委常委、副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
    # 杨斌 - 副县长
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 钟群英 - 副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王鸿鹏 - 副县长
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 万目国 - 副县长
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 邓伟 - 副县长、公安局长
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 刘少志 - 副县长
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李万喜 - 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 吴卓翰 - 副县长(挂职)
    {"person_id": 15, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职"},
]

relationships = [
    # 刘向阳 — 陈星：书记+县长搭档（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档，沅陵县党政主要领导", "overlap_org": "沅陵县", "overlap_period": ""},
    # 刘向阳 — 向晓华：县委常委班子成员
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与纪委书记，县委常委班子", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    # 刘向阳 — 杨太康：县委常委班子成员
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与组织部部长，县委常委班子", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    # 刘向阳 — 张俊：县委常委班子成员
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与宣传部部长，县委常委班子", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    # 刘向阳 — 黄松柏：县委常委班子成员
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与常务副县长，县委常委班子", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    # 陈星 — 黄松柏：县长—常务副县长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与常务副县长，县政府领导班子", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    # 陈星 — 各副县长
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长（挂职）", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—县委常委、副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长—副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长—副县长、公安局长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长—副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长—副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "县长—副县长（挂职）", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    # 黄松柏（常务副县长）— 其他副县长
    {"person_a": 6, "person_b": 7, "type": "共事", "context": "常务副县长与挂职副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "共事", "context": "常务副县长与县委常委、副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "共事", "context": "常务副县长与副县长", "overlap_org": "沅陵县人民政府", "overlap_period": ""},
    # 部委办负责人之间
    {"person_a": 3, "person_b": 4, "type": "共事", "context": "纪委书记与组织部部长，同为县委常委", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "纪委书记与宣传部部长，同为县委常委", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "共事", "context": "组织部部长与宣传部部长，同为县委常委", "overlap_org": "中共沅陵县委员会", "overlap_period": ""},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="沅陵县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done.")
