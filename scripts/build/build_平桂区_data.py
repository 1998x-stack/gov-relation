#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build SQLite database and GEXF graph for 贺州市平桂区 leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 贺州市
Region: 平桂区
Targets: 区委书记 & 区长

Research Date: 2026-07-23
Sources:
  - http://www.pinggui.gov.cn/xxgk/ (official gov portal, leadership page)
  - http://www.pinggui.gov.cn/gddt/t27942475.shtml (区委书记 article)
  - http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml (全领导会议)
  - http://www.pinggui.gov.cn/xxgk/zwdt/ldhd/ (leadership activity news)
"""

from __future__ import annotations

import os, sqlite3, sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE))
from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "平桂区"
STAGING = TMP_DIR / "guangxi_平桂区"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# persons
persons = [
    {"id": 1, "name": "周诚", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区委书记", "current_org": "中共平桂区委",
     "source": "http://www.pinggui.gov.cn/gddt/t27942475.shtml"},
    {"id": 2, "name": "逯宇", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区委副书记、区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 3, "name": "杨超武", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区委副书记", "current_org": "中共平桂区委",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 4, "name": "张伟辉", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区人大常委会党组书记", "current_org": "平桂区人大常委会",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 5, "name": "陈志勇", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区委常委、副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 6, "name": "唐姗", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "平桂区委常委、副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/ldhd/t27897289.shtml"},
    {"id": 7, "name": "郑力", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 8, "name": "王菊辉", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 9, "name": "黎明", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 10, "name": "董明玉", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/"},
    {"id": 11, "name": "夏宏平", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区副区长", "current_org": "平桂区人民政府",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/ldhd/t27893701.shtml"},
    {"id": 12, "name": "黄诗活", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/gddt/t27942475.shtml"},
    {"id": 13, "name": "蒋灵青", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 14, "name": "徐亮", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 15, "name": "吴泽灵", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 16, "name": "毛湘婷", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 17, "name": "蒙荣奎", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/ldhd/t27942315.shtml"},
    {"id": 18, "name": "何家松", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区领导", "current_org": "平桂区",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
    {"id": 19, "name": "潘龙江", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "平桂区人民检察院检察长", "current_org": "平桂区人民检察院",
     "source": "http://www.pinggui.gov.cn/xxgk/zwdt/zfhy/qthy/t27942193.shtml"},
]

organizations = [
    {"id": 0, "name": "中共平桂区委", "type": "党委", "level": "县处级",
     "parent": "中共贺州市委", "location": "贺州市平桂区"},
    {"id": 1, "name": "平桂区人民政府", "type": "政府", "level": "县处级",
     "parent": "贺州市人民政府", "location": "贺州市平桂区"},
    {"id": 2, "name": "平桂区人大常委会", "type": "人大", "level": "县处级",
     "parent": "", "location": "贺州市平桂区"},
    {"id": 3, "name": "平桂区政协", "type": "政协", "level": "县处级",
     "parent": "", "location": "贺州市平桂区"},
    {"id": 4, "name": "平桂区人民检察院", "type": "政府", "level": "县处级",
     "parent": "", "location": "贺州市平桂区"},
]

positions = [
    {"person_id": 1, "org_id": 0, "title": "平桂区委书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026年7月在任"},
    {"person_id": 2, "org_id": 0, "title": "平桂区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "平桂区区长", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 3, "org_id": 0, "title": "区委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区人大常委会党组书记", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委、副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "平桂区人民检察院检察长", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "书记与区长搭档", "overlap_org": "平桂区", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "周诚赴京招商，唐姗随同", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "逯宇调研，陈志勇参加", "overlap_org": "平桂区人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 11, "type": "overlap",
     "context": "逯宇调研固废治理，夏宏平参加", "overlap_org": "平桂区人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 16, "type": "overlap",
     "context": "逯宇调研防汛，毛湘婷参加", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "逯宇调研防汛，郑力参加", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 17, "type": "overlap",
     "context": "逯宇调研，蒙荣奎参加", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "书记与副书记共事", "overlap_org": "中共平桂区委", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "周诚走访商会，黄诗活陪同", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "全区推进会共同出席", "overlap_org": "平桂区", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "副书记与人大党组书记共同参会", "overlap_org": "平桂区", "overlap_period": "2026-07"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG, persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True,
    )
    print(f"\nDone: {SLUG} staging build complete.")
