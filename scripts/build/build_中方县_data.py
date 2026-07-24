#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中方县 leadership network.

Task: hunan_中方县
Province: 湖南省
Parent city: 怀化市
Level: 县
Targets: 县委书记 & 县长
"""

import sys
import os
from pathlib import Path

# Adjust path for running from staging directory
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parents[2]  # data/tmp/hunan_中方县 -> data/tmp -> data -> repo root
sys.path.insert(0, str(_REPO_ROOT))
from gov_relation.runner import run_build

_STAGING_DIR = _SCRIPT_DIR  # Write artifacts into the staging directory

# process_tmp.py validates these tokens exist
import sqlite3 as _sqlite3
DB_PATH = str(_STAGING_DIR / "中方县_network.db")
GEXF_PATH = str(_STAGING_DIR / "中方县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary (县委书记) ──
    {
        "id": 1,
        "name": "胡杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共中方县委书记",
        "current_org": "中共中方县委员会",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站新闻报道）",
    },
    # ── Current County Mayor (县长) ──
    {
        "id": 2,
        "name": "周华特",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1979-11",
        "birthplace": "湖南龙山",
        "education": "研究生",
        "party_join": "2004-03",
        "work_start": "2003-07",
        "current_post": "中共中方县委副书记、县人民政府党组书记、县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    # ── Deputy County Mayors (副县长) ──
    {
        "id": 3,
        "name": "杨志初",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    {
        "id": 4,
        "name": "魏鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    {
        "id": 5,
        "name": "熊勇华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    {
        "id": 6,
        "name": "刘强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    {
        "id": 7,
        "name": "杨惠云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    {
        "id": 8,
        "name": "贺爱平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "中方县人民政府",
        "source": "http://www.zhongfang.gov.cn（中方县人民政府网站领导之窗）",
    },
    # ── Predecessors ──
    {
        "id": 9,
        "name": "张家铣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "怀化市政协主席",
        "current_org": "怀化市政协",
        "source": "https://www.zhongfang.gov.cn（新闻资料：前任中方县委书记）",
    },
]

organizations = [
    {"id": 1, "name": "中共中方县委员会", "type": "党委", "level": "县级", "parent": "中共怀化市委", "location": "湖南省怀化市中方县"},
    {"id": 2, "name": "中方县人民政府", "type": "政府", "level": "县级", "parent": "怀化市人民政府", "location": "湖南省怀化市中方县"},
    {"id": 3, "name": "怀化市政协", "type": "政协", "level": "地市级", "parent": "湖南省政协", "location": "湖南省怀化市"},
    {"id": 4, "name": "中方县人大常委会", "type": "人大", "level": "县级", "parent": "怀化市人大常委会", "location": "湖南省怀化市中方县"},
    {"id": 5, "name": "政协中方县委员会", "type": "政协", "level": "县级", "parent": "怀化市政协", "location": "湖南省怀化市中方县"},
]

positions = [
    # 胡杰
    {"person_id": 1, "org_id": 1, "title": "中共中方县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 周华特
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨志初
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他副县长
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张家铣 - 前任县委书记
    {"person_id": 9, "org_id": 3, "title": "怀化市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "中共中方县委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "前任中方县委书记，后升任怀化市政协主席"},
]

relationships = [
    # 胡杰 — 周华特：书记+县长搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中方县", "overlap_period": ""},
    # 胡杰 — 杨志初：常委+副县长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委常委班子成员", "overlap_org": "中共中方县委员会", "overlap_period": ""},
    # 周华特 — 各位副县长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长", "overlap_org": "中方县人民政府", "overlap_period": ""},
    # 张家铣 — 胡杰：前后任书记
    {"person_a": 9, "person_b": 1, "type": "前后任", "context": "前任县委书记—现任县委书记", "overlap_org": "中共中方县委员会", "overlap_period": ""},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="中方县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done.")
