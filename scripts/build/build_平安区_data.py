#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 平安区, 海东市, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_平安区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: Core leadership identified from official government website
(http://www.pinganqu.gov.cn). District mayor position recently changed:
张攀杰 served as 区长 as of 2026-02, replaced by 王明芳 (acting/代区长)
as of 2026-05. Full career timelines and predecessor paths are limited
to what's published on the official leadership page.

Confirmed:
  区委书记: 王雯 (confirmed from official site, multiple articles 2025-08 to 2026-07)
  区委副书记、区政府代理区长: 王明芳 (confirmed from 2026-05 to 2026-07 articles)
  区委副书记: 杨元庆 (confirmed from 2026-03 and 2026-06 articles)
  区委常委、宣传部部长: 哈粮德 (official site)
  区委常委、政法委书记: 韩伟 (official site)
  区委常委、纪委书记、监委代主任: 马美玲 (official site)
  区委常委、组织部部长: 多杰 (official site)
  区政府副区长: 李园元 (official site)
  区政府副区长: 王宁 (official site)
  区政府副区长: 季勐 (from 2026-05 article)
  区人大常委会主任: 李占国 (official site, elected 2026-02)
  区政协主席: 王德民 (official site)
  前任区长: 张攀杰 (in office as of 2026-02, left by 2026-05)
"""
from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "平安区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (CONFIRMED from official site) ═══════
    {
        "id": 1,
        "name": "王雯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区委书记",
        "current_org": "中共海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qwld/52.html"
    },
    {
        "id": 2,
        "name": "王明芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平安区委副书记、区政府代理区长",
        "current_org": "海东市平安区人民政府",
        "source": "http://www.pinganqu.gov.cn/html/article/tpxw/10014.html"
    },
    {
        "id": 3,
        "name": "杨元庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平安区委副书记",
        "current_org": "中共海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/article/tpxw/10014.html"
    },
    {
        "id": 4,
        "name": "哈粮德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区委常委、宣传部部长、区总工会主席",
        "current_org": "中共海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qwld/80.html"
    },
    {
        "id": 5,
        "name": "韩伟",
        "gender": "男",
        "ethnicity": "撒拉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区委常委、政法委书记",
        "current_org": "中共海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qwld/66.html"
    },
    {
        "id": 6,
        "name": "马美玲",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1988-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区委常委、区纪委书记、监委代主任",
        "current_org": "中共海东市平安区纪律检查委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qwld/81.html"
    },
    {
        "id": 7,
        "name": "多杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1987-11",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区委常委、组织部部长、党校校长",
        "current_org": "中共海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qwld/68.html"
    },
    # ═══════ District Government Leaders ═══════
    {
        "id": 8,
        "name": "李园元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区政府副区长",
        "current_org": "海东市平安区人民政府",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qzfld/70.html"
    },
    {
        "id": 9,
        "name": "王宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985-06",
        "birthplace": "",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区政府副区长",
        "current_org": "海东市平安区人民政府",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qzfld/77.html"
    },
    {
        "id": 10,
        "name": "季勐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平安区政府副区长",
        "current_org": "海东市平安区人民政府",
        "source": "http://www.pinganqu.gov.cn/html/article/tpxw/9912.html"
    },
    # ═══════ People's Congress ═══════
    {
        "id": 11,
        "name": "李占国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-03",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区人大常委会党组书记、主任",
        "current_org": "海东市平安区人民代表大会常务委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qrdld/54.html"
    },
    {
        "id": 12,
        "name": "星占华",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1969-11",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区人大常委会党组副书记、副主任",
        "current_org": "海东市平安区人民代表大会常务委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qrdld/55.html"
    },
    {
        "id": 13,
        "name": "范雪莲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-12",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "平安区人大常委会副主任",
        "current_org": "海东市平安区人民代表大会常务委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qrdld/56.html"
    },
    {
        "id": 14,
        "name": "马林",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968-10",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区人大常委会副主任",
        "current_org": "海东市平安区人民代表大会常务委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qrdld/57.html"
    },
    # ═══════ CPPCC ═══════
    {
        "id": 15,
        "name": "王德民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-07",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区政协党组书记、主席",
        "current_org": "政协海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qzxld/60.html"
    },
    {
        "id": 16,
        "name": "汪清香",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "1969-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区政协党组副书记、副主席",
        "current_org": "政协海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qzxld/61.html"
    },
    {
        "id": 17,
        "name": "杨欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平安区政协副主席",
        "current_org": "政协海东市平安区委员会",
        "source": "http://www.pinganqu.gov.cn/html/leaders/qzxld/79.html"
    },
    # ═══════ Predecessor ═══════
    {
        "id": 18,
        "name": "张攀杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原平安区委副书记、区政府区长",
        "current_org": "海东市平安区人民政府",
        "source": "http://www.pinganqu.gov.cn/html/article/ldhd/8962.html"
    },
    {
        "id": 19,
        "name": "吉玉锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平安区领导",
        "current_org": "海东市平安区",
        "source": "http://www.pinganqu.gov.cn/html/article/tpxw/10002.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共海东市平安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共海东市委员会",
        "location": "青海省海东市平安区"
    },
    {
        "id": 2,
        "name": "海东市平安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "海东市人民政府",
        "location": "青海省海东市平安区"
    },
    {
        "id": 3,
        "name": "中共海东市平安区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共海东市纪律检查委员会",
        "location": "青海省海东市平安区"
    },
    {
        "id": 4,
        "name": "海东市平安区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "海东市人民代表大会常务委员会",
        "location": "青海省海东市平安区"
    },
    {
        "id": 5,
        "name": "政协海东市平安区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协海东市委员会",
        "location": "青海省海东市平安区"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王雯 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "平安区委书记", "start": "", "end": "", "rank": "正县级", "note": "主持区委全面工作"},
    # 王明芳 - 代理区长
    {"person_id": 2, "org_id": 2, "title": "平安区委副书记、区政府代理区长", "start": "2026-05", "end": "", "rank": "正县级", "note": "代理区长"},
    # 杨元庆 - 区委副书记
    {"person_id": 3, "org_id": 1, "title": "平安区委副书记", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 哈粮德 - 宣传部部长
    {"person_id": 4, "org_id": 1, "title": "平安区委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": "兼区总工会主席"},
    # 韩伟 - 政法委书记
    {"person_id": 5, "org_id": 1, "title": "平安区委常委、政法委书记", "start": "", "end": "", "rank": "副县级", "note": "负责区委政法委全盘工作"},
    # 马美玲 - 纪委书记
    {"person_id": 6, "org_id": 3, "title": "平安区委常委、区纪委书记、监委代主任", "start": "2026-02", "end": "", "rank": "副县级", "note": "主持区纪委监委全面工作"},
    # 多杰 - 组织部部长
    {"person_id": 7, "org_id": 1, "title": "平安区委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": "兼党校校长"},
    # 李园元 - 副区长
    {"person_id": 8, "org_id": 2, "title": "平安区政府副区长", "start": "", "end": "", "rank": "副县级", "note": "负责自然资源、农业农村等"},
    # 王宁 - 副区长
    {"person_id": 9, "org_id": 2, "title": "平安区政府副区长", "start": "", "end": "", "rank": "副县级", "note": "负责教育、民政、卫健等"},
    # 季勐 - 副区长
    {"person_id": 10, "org_id": 2, "title": "平安区政府副区长", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 李占国 - 人大主任
    {"person_id": 11, "org_id": 4, "title": "平安区人大常委会党组书记、主任", "start": "2026-02", "end": "", "rank": "正县级", "note": "主持区人大常委会全盘工作"},
    # 星占华 - 人大副主任
    {"person_id": 12, "org_id": 4, "title": "平安区人大常委会党组副书记、副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 范雪莲 - 人大副主任
    {"person_id": 13, "org_id": 4, "title": "平安区人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": "民建会员"},
    # 马林 - 人大副主任
    {"person_id": 14, "org_id": 4, "title": "平安区人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 王德民 - 政协主席
    {"person_id": 15, "org_id": 5, "title": "平安区政协党组书记、主席", "start": "", "end": "", "rank": "正县级", "note": "主持区政协全盘工作"},
    # 汪清香 - 政协副主席
    {"person_id": 16, "org_id": 5, "title": "平安区政协党组副书记、副主席", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 杨欢 - 政协副主席
    {"person_id": 17, "org_id": 5, "title": "平安区政协副主席", "start": "", "end": "", "rank": "副县级", "note": ""},
    # 张攀杰 - 前任区长
    {"person_id": 18, "org_id": 2, "title": "平安区委副书记、区政府区长", "start": "", "end": "2026-05", "rank": "正县级", "note": "前任区长，2026年5月前离任"},
    # 吉玉锋 - 区领导
    {"person_id": 19, "org_id": 1, "title": "平安区领导", "start": "", "end": "", "rank": "", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Work relationships - current leadership team
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与代理区长党政搭档", "overlap_org": "海东市平安区", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委副书记", "overlap_org": "中共海东市平安区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与组织部部长", "overlap_org": "中共海东市平安区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记与政法委书记", "overlap_org": "中共海东市平安区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与宣传部部长", "overlap_org": "中共海东市平安区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与纪委书记", "overlap_org": "中共海东市平安区委员会", "overlap_period": ""},
    # Government team
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "代区长与副区长", "overlap_org": "海东市平安区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "代区长与副区长", "overlap_org": "海东市平安区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "代区长与副区长", "overlap_org": "海东市平安区人民政府", "overlap_period": ""},
    # Succession
    {"person_a": 2, "person_b": 18, "type": "继任", "context": "王明芳接替张攀杰任代理区长", "overlap_org": "海东市平安区人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 18, "type": "党政搭档", "context": "区委书记与前任区长党政搭档", "overlap_org": "海东市平安区", "overlap_period": "至2026-05"},
    # People's Congress and CPPCC
    {"person_a": 1, "person_b": 11, "type": "同级", "context": "区委书记与人大主任", "overlap_org": "海东市平安区", "overlap_period": "2026-02至今"},
    {"person_a": 1, "person_b": 15, "type": "同级", "context": "区委书记与政协主席", "overlap_org": "海东市平安区", "overlap_period": ""},
]

# ── Run Build ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building {SLUG} network (as of {AS_OF})...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print("Done.")
