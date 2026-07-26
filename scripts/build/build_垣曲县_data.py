#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 垣曲县, 运城市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_垣曲县
Level: 县
Targets: 县委书记 & 县长

Current Status (as of 2026-07-26):
  - 县委书记: 史玉江 (运城市人大常委会副主任兼任)
  - 县长: 马巍
  - 前县委书记: 杨彦康 (调任运城市副市长)

Research sources:
  - www.yuanqu.gov.cn — 垣曲县人民政府官方网站 (领导之窗)
  - 运城市人民政府网站

Confidence notes:
  - Current roster confirmed from government website (primary source, high confidence)
  - Career histories from government summaries (limited detail — see open_gaps.md)
  - Predecessor info from news reports (moderate confidence)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "垣曲县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_垣曲县"
if _CURRENT_DIR.name == "shanxi_垣曲县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# ID scheme:
#   1-2:   Core leadership (县委书记、县长)
#   3-13:  Standing committee (县委常委)
#   14-25: Government deputies (副县长、党组成员)
#   26-31: 人大领导
#   32-38: 政协领导
#   101+:   Predecessor figures

persons = [
    # ══════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════
    dict(id=1, name="史玉江", gender="男", ethnicity="汉族",
         birth="1969-08", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="运城市人大常委会党组成员、副主任，垣曲县委书记",
         current_org="中共垣曲县委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=2, name="马巍", gender="男", ethnicity="汉族",
         birth="1981-01", birthplace="",
         education="研究生", party_join="中共党员", work_start="",
         current_post="垣曲县委副书记、政府县长、一级调研员",
         current_org="垣曲县人民政府",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),

    # ══════════════════════════════════════════════════
    # Standing Committee (县委常委)
    # ══════════════════════════════════════════════════
    dict(id=3, name="雷刚", gender="男", ethnicity="汉族",
         birth="1976-04", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="垣曲县委副书记",
         current_org="中共垣曲县委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=4, name="卫靖", gender="女", ethnicity="汉族",
         birth="1985-02", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、宣传部部长",
         current_org="中共垣曲县委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=5, name="王杰", gender="男", ethnicity="汉族",
         birth="1982-12", birthplace="",
         education="大学，工学学士", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、组织部部长",
         current_org="中共垣曲县委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=6, name="王海军", gender="男", ethnicity="汉族",
         birth="1977-04", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、县政府党组副书记、副县长",
         current_org="垣曲县人民政府",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=7, name="张建玲", gender="女", ethnicity="汉族",
         birth="1978-03", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、统战部部长",
         current_org="中共垣曲县委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=8, name="杜斌", gender="男", ethnicity="汉族",
         birth="1984-06", birthplace="",
         education="大学", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、县纪委书记、监委代主任",
         current_org="中共垣曲县纪律检查委员会",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=9, name="李林涛", gender="男", ethnicity="汉族",
         birth="1980-12", birthplace="",
         education="大学，军事学学士", party_join="中共党员", work_start="",
         current_post="垣曲县委常委、县人民武装部上校部长",
         current_org="垣曲县人民武装部",
         source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=10, name="台雷", gender="男", ethnicity="汉族",
          birth="1976-08", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县委常委、副县长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=11, name="张广彦", gender="男", ethnicity="汉族",
          birth="1980-03", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县委常委、政法委书记",
          current_org="中共垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=12, name="杨文礼", gender="男", ethnicity="汉族",
          birth="1986-07", birthplace="",
          education="大学，法学学士、管理学学士", party_join="中共党员", work_start="",
          current_post="垣曲县委常委、副县长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xwld/"),
    dict(id=13, name="陈斌", gender="男", ethnicity="汉族",
          birth="1978-10", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲经济技术开发区管委会副主任、县委办主任",
          current_org="中共垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xwld/"),

    # ══════════════════════════════════════════════════
    # Government deputies (县政府领导，非常委)
    # ══════════════════════════════════════════════════
    dict(id=14, name="王坚", gender="男", ethnicity="汉族",
          birth="1966-06", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政府党组副书记、一级调研员",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=15, name="梁鹏", gender="男", ethnicity="汉族",
          birth="1984-12", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政府党组成员，垣曲经济技术开发区党工委书记、管委会主任",
          current_org="垣曲经济技术开发区",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=16, name="刘祥年", gender="男", ethnicity="汉族",
          birth="1973-02", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人民政府副县长、县公安局党委书记局长、二级高级警长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=17, name="翟朝霞", gender="女", ethnicity="汉族",
          birth="1975-03", birthplace="",
          education="大学", party_join="民盟盟员", work_start="",
          current_post="垣曲县人民政府副县长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=18, name="宁绍东", gender="男", ethnicity="汉族",
          birth="1978-02", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人民政府党组成员、副县长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=19, name="赵楠楠", gender="男", ethnicity="汉族",
          birth="1982-04", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人民政府党组成员、副县长",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=20, name="王爱东", gender="男", ethnicity="汉族",
          birth="1974-01", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政府党组成员、三级调研员",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),
    dict(id=21, name="王小东", gender="男", ethnicity="汉族",
          birth="1978-11", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政府党组成员、政府办公室主任",
          current_org="垣曲县人民政府",
          source="http://www.yuanqu.gov.cn/ldzc/xzfld/"),

    # ══════════════════════════════════════════════════
    # 人大领导
    # ══════════════════════════════════════════════════
    dict(id=22, name="孔祥虎", gender="男", ethnicity="汉族",
          birth="1969-02", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人大常委会党组书记、主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),
    dict(id=23, name="张应战", gender="男", ethnicity="汉族",
          birth="1968-12", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人大常委会党组成员、副主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),
    dict(id=24, name="杜涛", gender="男", ethnicity="汉族",
          birth="1971-05", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人大常委会党组成员、副主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),
    dict(id=25, name="闫锐明", gender="男", ethnicity="汉族",
          birth="1977-09", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人大常委会党组成员、副主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),
    dict(id=26, name="孙建寨", gender="男", ethnicity="汉族",
          birth="1970-10", birthplace="",
          education="大学", party_join="民建", work_start="",
          current_post="垣曲县人大常委会副主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),
    dict(id=27, name="雷恩克", gender="男", ethnicity="汉族",
          birth="1978-11", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县人大办公室主任",
          current_org="垣曲县人大常委会",
          source="http://www.yuanqu.gov.cn/ldzc/xrdld/"),

    # ══════════════════════════════════════════════════
    # 政协领导
    # ══════════════════════════════════════════════════
    dict(id=28, name="薛红泽", gender="男", ethnicity="汉族",
          birth="1972-04", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政协党组书记",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=29, name="李鹏", gender="男", ethnicity="汉族",
          birth="1967-10", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政协主席",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=30, name="雪增元", gender="男", ethnicity="汉族",
          birth="1964-05", birthplace="",
          education="大学", party_join="民盟盟员", work_start="",
          current_post="垣曲县政协副主席",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=31, name="丁莉萍", gender="女", ethnicity="回族",
          birth="1974-06", birthplace="",
          education="大学", party_join="", work_start="",
          current_post="垣曲县政协副主席",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=32, name="郭志宏", gender="男", ethnicity="汉族",
          birth="1966-12", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政协党组成员、副主席",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=33, name="李为农", gender="男", ethnicity="汉族",
          birth="1972-10", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政协党组成员、副主席",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),
    dict(id=34, name="郭红云", gender="男", ethnicity="汉族",
          birth="1972-08", birthplace="",
          education="大学", party_join="中共党员", work_start="",
          current_post="垣曲县政协党组成员、秘书长",
          current_org="政协垣曲县委员会",
          source="http://www.yuanqu.gov.cn/ldzc/xzxld/"),

    # ══════════════════════════════════════════════════
    # Predecessor figures
    # ══════════════════════════════════════════════════
    dict(id=101, name="杨彦康", gender="男", ethnicity="汉族",
          birth="1970-02", birthplace="",
          education="", party_join="中共党员", work_start="",
          current_post="运城市人民政府副市长",
          current_org="运城市人民政府",
          source="运城市人民政府网站"),
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    dict(id=1, name="省委", type="党委", level="",
         parent="中国共产党山西省委员会", location="山西省"),
    dict(id=2, name="市委", type="党委", level="地级市",
         parent="中共山西省委员会", location="山西省运城市"),
    dict(id=3, name="县委", type="党委", level="县",
         parent="中共运城市委员会", location="山西省运城市垣曲县"),
    dict(id=4, name="县政府", type="政府", level="县",
         parent="运城市人民政府", location="山西省运城市垣曲县"),
    dict(id=5, name="县人大", type="人大", level="县",
         parent="运城市人大常委会", location="山西省运城市垣曲县"),
    dict(id=6, name="县政协", type="政协", level="县",
         parent="政协运城市委员会", location="山西省运城市垣曲县"),
    dict(id=7, name="县纪委", type="纪委", level="县",
         parent="中共垣曲县委员会", location="山西省运城市垣曲县"),
    dict(id=8, name="县人民武装部", type="军队", level="县",
         parent="运城军分区", location="山西省运城市垣曲县"),
    dict(id=9, name="垣曲经济技术开发区", type="经济功能区", level="县",
         parent="垣曲县人民政府", location="山西省运城市垣曲县"),
    dict(id=10, name="县公安局", type="政府", level="县",
         parent="垣曲县人民政府", location="山西省运城市垣曲县"),
    dict(id=11, name="市委政法委", type="党委", level="地级市",
         parent="中共运城市委员会", location="山西省运城市"),
]

# ── Positions (person_id, org_id, title, start_date, end_date, rank, note) ──
positions = [
    # Core leadership
    dict(person_id=1, org_id=3, title="县委书记", start_date="", end_date="", rank="副厅级",
         note="兼任运城市人大常委会副主任"),
    dict(person_id=1, org_id=2, title="运城市人大常委会党组成员、副主任", start_date="", end_date="", rank="副厅级",
         note="高配"),
    dict(person_id=2, org_id=4, title="县长", start_date="", end_date="", rank="正处级",
         note="一级调研员"),
    dict(person_id=2, org_id=3, title="县委副书记", start_date="", end_date="", rank="正处级",
         note="县政府党组书记"),

    # Standing committee - party leadership
    dict(person_id=3, org_id=3, title="县委副书记", start_date="", end_date="", rank="副处级",
         note="专职副书记"),
    dict(person_id=4, org_id=3, title="县委常委、宣传部部长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=5, org_id=3, title="县委常委、组织部部长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=6, org_id=4, title="县委常委、县政府党组副书记、副县长", start_date="", end_date="", rank="副处级",
         note="常务副县长"),
    dict(person_id=7, org_id=3, title="县委常委、统战部部长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=8, org_id=7, title="县委常委、县纪委书记、监委代主任", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=9, org_id=8, title="县委常委、县人民武装部上校部长", start_date="", end_date="", rank="正团级",
         note=""),
    dict(person_id=10, org_id=4, title="县委常委、副县长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=11, org_id=3, title="县委常委、政法委书记", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=12, org_id=4, title="县委常委、副县长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=13, org_id=9, title="垣曲经济技术开发区管委会副主任", start_date="", end_date="", rank="副处级",
         note="县委办主任"),

    # Government deputies
    dict(person_id=14, org_id=4, title="县政府党组副书记、一级调研员", start_date="", end_date="", rank="正处级",
         note=""),
    dict(person_id=15, org_id=9, title="垣曲经济技术开发区党工委书记、管委会主任", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=16, org_id=10, title="副县长、县公安局局长", start_date="", end_date="", rank="副处级",
         note="二级高级警长"),
    dict(person_id=17, org_id=4, title="副县长", start_date="", end_date="", rank="副处级",
         note="民盟盟员"),
    dict(person_id=18, org_id=4, title="副县长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=19, org_id=4, title="副县长", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=20, org_id=4, title="县政府党组成员、三级调研员", start_date="", end_date="", rank="副处级",
         note="分管农业农村"),
    dict(person_id=21, org_id=4, title="县政府党组成员、办公室主任", start_date="", end_date="", rank="正科级",
         note=""),

    # 人大
    dict(person_id=22, org_id=5, title="县人大常委会主任", start_date="", end_date="", rank="正处级",
         note=""),
    dict(person_id=23, org_id=5, title="县人大常委会副主任", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=24, org_id=5, title="县人大常委会副主任", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=25, org_id=5, title="县人大常委会副主任", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=26, org_id=5, title="县人大常委会副主任", start_date="", end_date="", rank="副处级",
         note="民建"),
    dict(person_id=27, org_id=5, title="县人大办公室主任", start_date="", end_date="", rank="正科级",
         note=""),

    # 政协
    dict(person_id=28, org_id=6, title="县政协党组书记", start_date="", end_date="", rank="正处级",
         note=""),
    dict(person_id=29, org_id=6, title="县政协主席", start_date="", end_date="", rank="正处级",
         note=""),
    dict(person_id=30, org_id=6, title="县政协副主席", start_date="", end_date="", rank="副处级",
         note="民盟"),
    dict(person_id=31, org_id=6, title="县政协副主席", start_date="", end_date="", rank="副处级",
         note="回族"),
    dict(person_id=32, org_id=6, title="县政协副主席", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=33, org_id=6, title="县政协副主席", start_date="", end_date="", rank="副处级",
         note=""),
    dict(person_id=34, org_id=6, title="县政协秘书长", start_date="", end_date="", rank="正科级",
         note=""),

    # Predecessor
    dict(person_id=101, org_id=4, title="前任垣曲县委书记", start_date="", end_date="", rank="正处级",
          note="后调任运城市副市长"),
    dict(person_id=101, org_id=2, title="运城市人民政府副市长", start_date="", end_date="", rank="副厅级",
          note=""),
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core leadership pair
    dict(person_a=1, person_b=2, type="领导_副手",
         context="县委书记与县长搭档",
         overlap_org="中共垣曲县委员会", overlap_period=""),

    # 县委书记 → 副书记
    dict(person_a=1, person_b=3, type="领导_副手",
         context="县委书记与县委专职副书记",
         overlap_org="县委", overlap_period=""),
    dict(person_a=1, person_b=8, type="领导_副手",
         context="县委书记与县纪委书记",
         overlap_org="县委", overlap_period=""),

    # 县长 → 副县长
    dict(person_a=2, person_b=6, type="领导_副手",
         context="县长与常务副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=2, person_b=10, type="领导_副手",
         context="县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=2, person_b=12, type="领导_副手",
         context="县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=2, person_b=16, type="领导_副手",
         context="县长与公安局长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=2, person_b=18, type="领导_副手",
         context="县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=2, person_b=19, type="领导_副手",
         context="县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),

    # 县委常委之间
    dict(person_a=3, person_b=4, type="同僚",
         context="县委副书记与县委宣传部部长",
         overlap_org="中共垣曲县委员会", overlap_period=""),
    dict(person_a=3, person_b=5, type="同僚",
         context="县委副书记与县委组织部部长",
         overlap_org="中共垣曲县委员会", overlap_period=""),
    dict(person_a=4, person_b=5, type="同僚",
         context="宣传部部长与组织部部长",
         overlap_org="中共垣曲县委员会", overlap_period=""),
    dict(person_a=6, person_b=10, type="同僚",
         context="常务副县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),
    dict(person_a=6, person_b=12, type="同僚",
         context="常务副县长与副县长",
         overlap_org="垣曲县人民政府", overlap_period=""),

    # 人大与党委
    dict(person_a=1, person_b=22, type="领导_副手",
         context="县委书记与县人大主任",
         overlap_org="垣曲县", overlap_period=""),

    # 前任与现任
    dict(person_a=1, person_b=101, type="接任",
         context="杨彦康→史玉江接任县委书记",
         overlap_org="中共垣曲县委员会", overlap_period=""),
]


# ── Person JSON helpers ──────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = """\
{{
  "slug": "yuanqu_{name}",
  "name": "{name}",
  "title": "{title}",
  "investigation_date": "{date}",
  "aliases": [],
  "gender": "{gender}",
  "ethnicity": "{ethnicity}",
  "birth": "{birth}",
  "death": null,
  "birthplace": "{birthplace}",
  "education": {education_list},
  "party_join": "{party_join}",
  "work_start": null,
  "current": {{
    "post": "{current_post}",
    "organization": "{current_org}",
    "level": "{level}",
    "as_of": "{as_of}"
  }},
  "positions": [],
  "relationships": [],
  "achievements": [],
  "expertise": [],
  "style_clues": [],
  "confidence": "medium",
  "source_urls": [
    "http://www.yuanqu.gov.cn/ldzc/xwld/"
  ],
  "investigator": "codex-china-gov-network",
  "notes": "履历细节待补充（见open_gaps.md）"
}}
"""


def write_person_json(name: str, title: str, gender: str, ethnicity: str,
                      birth: str, birthplace: str, education: str,
                      party_join: str, current_post: str, current_org: str,
                      level: str) -> None:
    fname = f"{TODAY}-山西省-运城市-垣曲县-{title}-{name}.json"
    path = PJSON_DIR / fname
    content = PERSON_JSON_TEMPLATE.format(
        name=name,
        title=title.replace("，", "、").replace(" ", ""),
        date=TODAY,
        gender=gender,
        ethnicity=ethnicity,
        birth=birth,
        birthplace=birthplace,
        education_list=json.dumps(education.split("、") if education else []),
        party_join=party_join,
        current_post=current_post.replace('"', '\\"'),
        current_org=current_org,
        level=level,
        as_of=AS_OF,
    )
    path.write_text(content, encoding="utf-8")
    print(f"  Person JSON: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    print("=" * 60)
    print(f"Building {SLUG} network data")
    print(f"Date: {AS_OF}")
    print("=" * 60)

    # 1. Database + GEXF
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
    print(f"\n  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # 2. Person JSONs for core leaders
    print("\n--- Writing person JSONs ---")
    write_person_json(
        name="史玉江", title="县委书记",
        gender="男", ethnicity="汉族", birth="1969-08", birthplace="",
        education="大学", party_join="中共党员",
        current_post="运城市人大常委会党组成员、副主任，垣曲县委书记",
        current_org="中共垣曲县委员会",
        level="副厅级",
    )
    write_person_json(
        name="马巍", title="县长",
        gender="男", ethnicity="汉族", birth="1981-01", birthplace="",
        education="研究生", party_join="中共党员",
        current_post="垣曲县委副书记、县长、一级调研员",
        current_org="垣曲县人民政府",
        level="正处级",
    )
    write_person_json(
        name="雷刚", title="县委副书记",
        gender="男", ethnicity="汉族", birth="1976-04", birthplace="",
        education="大学", party_join="中共党员",
        current_post="垣曲县委副书记",
        current_org="中共垣曲县委员会",
        level="副处级",
    )
    print("\nDone!")


if __name__ == "__main__":
    main()
