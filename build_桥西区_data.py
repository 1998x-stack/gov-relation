#!/usr/bin/env python3
"""Build 张家口市桥西区 (Zhangjiakou Qiaoxi District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 张家口市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_桥西区

Research date: 2026-07-24
Official source: http://www.zjkqxq.gov.cn/ (张家口市桥西区人民政府)

Current status (as of 2026-07-24):
- 区委书记: 左克平 — 2026年7月18日召开的桥西区第十二次党代会上
  代表十一届区委作报告, 7月19日主持闭幕大会, 确认连任/当选新一届区委书记
- 区长: 戈录伟 — 区第十二次党代会执行主席并主持开幕式,
  确认出任区委副书记, 预计将担任区长; 区政府领导页面上任显示为区委副书记、区长
"""

from __future__ import annotations

import sys
from pathlib import Path

# When run from data/tmp/hebei_桥西区/, resolve repo root two levels up
_SCRIPT_DIR = Path(__file__).resolve().parent
# The canonical build script lives at scripts/build/build_桥西区_data.py
# and will be run from the repo root. For staging we keep the paths consistent.
_REPO_ROOT = _SCRIPT_DIR.parent.parent  # data/tmp/hebei_桥西区/ -> repo root
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桥西区"

# When run from staging, write DB and GEXF to the staging directory.
# The canonical promotion process copies them to DATA_DIR and GRAPH_DIR.
_STAGING_DIR = _SCRIPT_DIR  # data/tmp/hebei_桥西区/
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "左克平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委书记",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/11/96120.html "
                    "(十二次党代会闭幕, 左克平主持)"),
    },
    {
        "id": 2,
        "name": "戈录伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委副书记、区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会开幕, 戈录伟主持)"),
    },
    # ════════════════════════════════════════
    # 区委常委 (Standing Committee)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "吉树强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 4,
        "name": "胡海飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 5,
        "name": "马玉红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 6,
        "name": "杨建章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 7,
        "name": "孙丹峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记",
        "current_org": "中共张家口市桥西区纪律检查委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/22/96118.html "
                    "(十二届纪委第一次全体会议, 孙丹峰当选书记)"),
    },
    {
        "id": 8,
        "name": "卢宗生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 9,
        "name": "李艳娇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 10,
        "name": "刘建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 11,
        "name": "刘海军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共张家口市桥西区委员会",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/12/96126.html "
                    "(十二次党代会主席团成员)"),
    },
    {
        "id": 12,
        "name": "杨巍洁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45063.html "
                    "(常务副区长分工及履历)"),
    },
    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "黄向义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/55582.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 14,
        "name": "陈建民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45062.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 15,
        "name": "王平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/60237.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 16,
        "name": "倪明远",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/55577.html "
                    "(副区长分工及履历)"),
    },
    {
        "id": 17,
        "name": "王则栋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "桥西区人民政府",
        "source": ("官方: http://www.zjkqxq.gov.cn/single/98/45061.html "
                    "(副区长分工及履历)"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共张家口市桥西区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共张家口市委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 2,
        "name": "桥西区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "张家口市人民政府",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 3,
        "name": "中共张家口市桥西区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区",
        "parent": "中共张家口市纪律检查委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 4,
        "name": "桥西区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "张家口市人大常委会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 5,
        "name": "政协桥西区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协张家口市委员会",
        "location": "河北省张家口市桥西区",
    },
    {
        "id": 6,
        "name": "张家口市公安局桥西分局",
        "type": "政府",
        "level": "区直部门",
        "parent": "张家口市公安局",
        "location": "河北省张家口市桥西区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 区委领导
    {"person_id": 1, "org_id": 1, "title": "桥西区委书记", "start": "", "end": "至今", "rank": "正处级", "note": "2026年7月第十二次党代会连任"},
    {"person_id": 2, "org_id": 2, "title": "桥西区区长", "start": "", "end": "至今", "rank": "正处级", "note": "第十二次党代会执行主席"},
    {"person_id": 2, "org_id": 1, "title": "桥西区委副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 4, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 5, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 6, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 7, "org_id": 3, "title": "桥西区纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "十二届纪委第一次全会当选"},
    {"person_id": 7, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 9, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 10, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 11, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": "十二次党代会主席团成员"},
    {"person_id": 12, "org_id": 2, "title": "桥西区常务副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区委常委、区政府党组副书记"},
    {"person_id": 12, "org_id": 1, "title": "桥西区委常委", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 区政府领导
    {"person_id": 13, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员, 兼公安分局局长"},
    {"person_id": 14, "org_id": 6, "title": "桥西公安分局局长", "start": "", "end": "至今", "rank": "正科级", "note": "党委书记、局长、督察长"},
    {"person_id": 15, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 16, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "桥西区副区长", "start": "", "end": "至今", "rank": "副处级", "note": "区政府党组成员"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系", "overlap_org": "桥西区", "overlap_period": "2026-"},
    # 区委常委班子
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与纪委书记", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委常委班子成员", "overlap_org": "中共桥西区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记与常务副区长", "overlap_org": "中共桥西区委", "overlap_period": ""},
    # 区长与副区长
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长与常务副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与副区长工作搭档", "overlap_org": "桥西区政府", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  张家口市桥西区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 桥西区政府网站 www.zjkqxq.gov.cn")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\n✅ 桥西区数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
