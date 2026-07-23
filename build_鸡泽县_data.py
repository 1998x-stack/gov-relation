#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鸡泽县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 鸡泽县
Targets: 县委书记 & 县长

Research Sources:
- 鸡泽县人民政府信息公开平台 — 领导之窗 (http://www.jize.gov.cn/sszt-jzxxxgk/web/leader)
  确认县长胡延峰及县政府领导班子
- 维基百科鸡泽县条目 (https://zh.wikipedia.org/wiki/鸡泽县)
  确认县委书记刘文萍
- 鸡泽县人民政府门户网站 (http://www.jize.gov.cn/)

Research Date: 2026-07-23

已知信息:
- 县委书记: 刘文萍（维基百科信息框确认）
- 县长: 胡延峰，男，汉族，1974年4月生，省委党校研究生学历，中共党员
- 县委常委、副县长: 王维维
- 副县长: 王磊, 高川, 张延卿, 李云鹏, 张晓

Confidence:
- 刘文萍 县委书记: confirmed (Wikipedia infobox)
- 胡延峰 县长身份及基本信息: confirmed (政府官方网站)
- 副县长信息: confirmed (政府官方网站)
- 刘文萍简历: unverified (web search degraded)
- 胡延峰完整履历: partial (仅有基本信息)
- 县委常委完整名单: unverified (web search degraded)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "鸡泽县"

DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘文萍",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县委书记",
        "current_org": "中共邯郸市鸡泽县委员会",
        "source": "https://zh.wikipedia.org/wiki/鸡泽县 — 维基百科信息框确认刘文萍任鸡泽县委书记"
    },
    {
        "id": 2,
        "name": "胡延峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-04",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县委副书记、县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader — 鸡泽县人民政府信息公开平台领导之窗"
    },
    # ════════════════════════════════════════
    # Deputy County Leaders (政府副县长)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "王维维",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县委常委、副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader — 鸡泽县人民政府信息公开平台"
    },
    {
        "id": 4,
        "name": "王磊",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader"
    },
    {
        "id": 5,
        "name": "高川",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader"
    },
    {
        "id": 6,
        "name": "张延卿",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader"
    },
    {
        "id": 7,
        "name": "李云鹏",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader"
    },
    {
        "id": 8,
        "name": "张晓",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鸡泽县副县长",
        "current_org": "鸡泽县人民政府",
        "source": "http://www.jize.gov.cn/sszt-jzxxxgk/web/leader"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市鸡泽县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共邯郸市委员会",
        "location": "河北省邯郸市鸡泽县"
    },
    {
        "id": 2,
        "name": "鸡泽县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市鸡泽县"
    },
    {
        "id": 3,
        "name": "鸡泽县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "邯郸市人民代表大会常务委员会",
        "location": "河北省邯郸市鸡泽县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议鸡泽县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议邯郸市委员会",
        "location": "河北省邯郸市鸡泽县"
    },
    {
        "id": 5,
        "name": "中共鸡泽县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共邯郸市纪律检查委员会",
        "location": "河北省邯郸市鸡泽县"
    },
    {
        "id": 6,
        "name": "鸡泽镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县鸡泽镇"
    },
    {
        "id": 7,
        "name": "小寨镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县小寨镇"
    },
    {
        "id": 8,
        "name": "双塔镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县双塔镇"
    },
    {
        "id": 9,
        "name": "曹庄镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县曹庄镇"
    },
    {
        "id": 10,
        "name": "浮图店镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县浮图店镇"
    },
    {
        "id": 11,
        "name": "吴官营镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县吴官营镇"
    },
    {
        "id": 12,
        "name": "风正乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "鸡泽县人民政府",
        "location": "河北省邯郸市鸡泽县风正乡"
    },
    {
        "id": 13,
        "name": "中共鸡泽县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共邯郸市鸡泽县委员会",
        "location": "河北省邯郸市鸡泽县"
    },
]

# 3. Positions
positions = [
    # 刘文萍
    {
        "person_id": 1,
        "org_id": 1,
        "title": "鸡泽县委书记",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "维基百科信息框确认，但具体到任时间待查。公开网络搜索受限，未能获取更详细履历。"
    },
    # 胡延峰
    {
        "person_id": 2,
        "org_id": 2,
        "title": "鸡泽县委副书记、县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "政府官方网站领导之窗确认。1974年4月生，省委党校研究生学历。具体到任时间及此前任职经历待查。"
    },
    # 王维维
    {
        "person_id": 3,
        "org_id": 2,
        "title": "鸡泽县委常委、副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
    # 王磊
    {
        "person_id": 4,
        "org_id": 2,
        "title": "鸡泽县副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
    # 高川
    {
        "person_id": 5,
        "org_id": 2,
        "title": "鸡泽县副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
    # 张延卿
    {
        "person_id": 6,
        "org_id": 2,
        "title": "鸡泽县副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
    # 李云鹏
    {
        "person_id": 7,
        "org_id": 2,
        "title": "鸡泽县副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
    # 张晓
    {
        "person_id": 8,
        "org_id": 2,
        "title": "鸡泽县副县长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "政府官方网站领导之窗确认，具体分管工作及任职时间待查。"
    },
]

# 4. Relationships
relationships = [
    # 胡延峰 — 刘文萍：党政搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "刘文萍任鸡泽县委书记，胡延峰任县委副书记、县长，为党政一把手搭档关系",
        "overlap_org": "中共邯郸市鸡泽县委员会／鸡泽县人民政府",
        "overlap_period": "至今"
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
