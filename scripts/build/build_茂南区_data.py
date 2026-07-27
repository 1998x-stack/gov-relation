#!/usr/bin/env python3
"""Build 茂南区 (Maonan District, 茂名市, 广东省) personnel network.

Generated: 2026-07-22
Task: guangdong_茂南区
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

# Add project root to path
BASE = str(Path(__file__).resolve().parent.parent.parent.parent)
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── slug ──────────────────────────────────────────────────────────────
SLUG = "茂南区"
TASK_ID = "guangdong_茂南区"
DB_PATH = os.path.join(BASE, "data", "database", "茂南区_network.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", "茂南区_network.gexf")

# ── Persons ───────────────────────────────────────────────────────────
persons = [
    # ---- Top leaders ----
    {
        "id": 1,
        "name": "梁剑辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委书记",
        "current_org": "中共茂南区委",
        "source": "https://baike.baidu.com/item/%E6%A2%81%E5%89%91%E8%BE%89/24458445",
    },
    {
        "id": 2,
        "name": "吕国记",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "1990年",
        "current_post": "茂南区委副书记、区长",
        "current_org": "茂南区人民政府",
        "source": "https://baike.baidu.com/item/%E5%90%95%E5%9B%BD%E8%AE%B0",
    },
    {
        "id": 3,
        "name": "廖述毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "湖南武冈",
        "education": "博士研究生学历，文学博士",
        "party_join": "1999年6月",
        "work_start": "2001年7月",
        "current_post": "茂名市人大常委会党组成员、副主任",
        "current_org": "茂名市人大常委会",
        "source": "https://baike.baidu.com/item/%E5%BB%96%E8%BF%B0%E6%AF%85/22137672",
    },
    # ---- Standing committee members ----
    {
        "id": 4,
        "name": "杨杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委副书记",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1624840.html",
    },
    {
        "id": 5,
        "name": "吴岳奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、常务副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1373270.html",
    },
    {
        "id": 6,
        "name": "杨华靖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、组织部部长、党校校长",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1612250.html",
    },
    {
        "id": 7,
        "name": "詹燕萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、纪委书记、区监委主任",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1591333.html",
    },
    {
        "id": 8,
        "name": "李祖源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、政法委书记",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1592969.html",
    },
    {
        "id": 9,
        "name": "李成波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、统战部部长",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1595634.html",
    },
    {
        "id": 10,
        "name": "吴春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委、副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1623521.html",
    },
    {
        "id": 11,
        "name": "黄蓉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1624840.html",
    },
    {
        "id": 12,
        "name": "林大全",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区委常委",
        "current_org": "中共茂南区委",
        "source": "http://www.maonan.gov.cn/zwxw/mndt/content/post_1624840.html",
    },
    # ---- Deputy mayors ----
    {
        "id": 13,
        "name": "黄建业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1373540.html",
    },
    {
        "id": 14,
        "name": "陈海玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区副区长、区公安分局局长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1569328.html",
    },
    {
        "id": 15,
        "name": "梁梨宁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1419415.html",
    },
    {
        "id": 16,
        "name": "刘仁生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "大学/工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "茂南区副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1290946.html",
    },
    {
        "id": 17,
        "name": "杨海璇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "本科",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "茂南区副区长",
        "current_org": "茂南区人民政府",
        "source": "http://www.maonan.gov.cn/zwgk/ldbz/qzf/fuquzhang/content/post_1227007.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共茂南区委", "type": "党委", "level": "县处级", "parent": "中共茂名市委", "location": "茂名市茂南区"},
    {"id": 2, "name": "茂南区人民政府", "type": "政府", "level": "县处级", "parent": "茂名市人民政府", "location": "茂名市茂南区"},
    {"id": 3, "name": "茂南区纪委监委", "type": "纪律检查", "level": "县处级", "parent": "中共茂南区委", "location": "茂名市茂南区"},
    {"id": 4, "name": "茂名市人大常委会", "type": "人大", "level": "地厅级", "parent": "广东省人大常委会", "location": "茂名市"},
    {"id": 5, "name": "茂名市国资委", "type": "政府", "level": "地厅级", "parent": "茂名市人民政府", "location": "茂名市"},
    {"id": 6, "name": "茂名市城市管理和综合执法局", "type": "政府", "level": "地厅级", "parent": "茂名市人民政府", "location": "茂名市"},
    {"id": 7, "name": "茂名市委办公室", "type": "党委", "level": "地厅级", "parent": "中共茂名市委", "location": "茂名市"},
    {"id": 8, "name": "茂名日报社", "type": "事业单位", "level": "地厅级", "parent": "中共茂名市委", "location": "茂名市"},
    {"id": 9, "name": "茂名高新区", "type": "开发区", "level": "地厅级", "parent": "茂名市人民政府", "location": "茂名市"},
    {"id": 10, "name": "茂名市金融工作局", "type": "政府", "level": "地厅级", "parent": "茂名市人民政府", "location": "茂名市"},
    {"id": 11, "name": "茂南区公安分局", "type": "政府", "level": "县处级", "parent": "茂南区人民政府", "location": "茂名市茂南区"},
    {"id": 12, "name": "宁波大学", "type": "事业单位", "level": "其他", "parent": "", "location": "浙江省宁波市"},
    {"id": 13, "name": "南京大学", "type": "事业单位", "level": "其他", "parent": "", "location": "江苏省南京市"},
    {"id": 14, "name": "湖南师范大学", "type": "事业单位", "level": "其他", "parent": "", "location": "湖南省长沙市"},
    {"id": 15, "name": "广西师范大学", "type": "事业单位", "level": "其他", "parent": "", "location": "广西桂林市"},
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    # 梁剑辉
    {"person_id": 1, "org_id": 1, "title": "茂南区委书记", "start_date": "2025?", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "茂名市国资委党委书记、主任", "start_date": "2023-03-09", "end_date": "present", "rank": "地厅级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "茂名高新区党工委副书记、管委会主任", "start_date": "", "end_date": "2023?", "rank": "地厅级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "茂名市金融工作局党组书记、局长", "start_date": "", "end_date": "2023?", "rank": "地厅级", "note": ""},
    # 吕国记
    {"person_id": 2, "org_id": 2, "title": "茂南区区长", "start_date": "2021-11", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "茂南区委副书记", "start_date": "2021-11", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "茂名市城市管理和综合执法局局长", "start_date": "2019-01", "end_date": "2020-08", "rank": "地厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "茂南区委常委（挂任）", "start_date": "2015-04", "end_date": "2015-12", "rank": "县处级", "note": "挂任"},
    {"person_id": 2, "org_id": 7, "title": "茂名市委副秘书长", "start_date": "2007-03", "end_date": "2014-06", "rank": "地厅级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "茂名市委机关事务管理局局长", "start_date": "2001-09", "end_date": "2010-09", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "茂名市委办公室科员/副科长/科长", "start_date": "1992-08", "end_date": "2001-09", "rank": "", "note": ""},
    # 廖述毅
    {"person_id": 3, "org_id": 1, "title": "茂南区委书记", "start_date": "2021-10", "end_date": "2025-03", "rank": "县处级", "note": "前任区委书记"},
    {"person_id": 3, "org_id": 2, "title": "茂南区区长", "start_date": "2018-01", "end_date": "2021-10", "rank": "县处级", "note": "前任区长"},
    {"person_id": 3, "org_id": 4, "title": "茂名市人大常委会副主任", "start_date": "2025-03", "end_date": "present", "rank": "地厅级", "note": "晋升"},
    {"person_id": 3, "org_id": 8, "title": "茂名日报社社长", "start_date": "2011-09", "end_date": "2017-09", "rank": "地厅级", "note": ""},
    {"person_id": 3, "org_id": 13, "title": "南京大学博士生", "start_date": "1998-09", "end_date": "2001-06", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 14, "title": "湖南师范大学本科生", "start_date": "1992-09", "end_date": "1996-06", "rank": "", "note": ""},
    # 杨杰
    {"person_id": 4, "org_id": 1, "title": "茂南区委副书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 吴岳奇
    {"person_id": 5, "org_id": 2, "title": "茂南区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 杨华靖
    {"person_id": 6, "org_id": 1, "title": "茂南区委常委、组织部部长、党校校长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 詹燕萍
    {"person_id": 7, "org_id": 3, "title": "茂南区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 李祖源
    {"person_id": 8, "org_id": 1, "title": "茂南区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 李成波
    {"person_id": 9, "org_id": 1, "title": "茂南区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 吴春雷
    {"person_id": 10, "org_id": 2, "title": "茂南区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 黄蓉
    {"person_id": 11, "org_id": 1, "title": "茂南区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体分工待确认"},
    # 林大全
    {"person_id": 12, "org_id": 1, "title": "茂南区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "具体分工待确认"},
    # 黄建业
    {"person_id": 13, "org_id": 2, "title": "茂南区副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 陈海玲
    {"person_id": 14, "org_id": 11, "title": "茂南区副区长、公安分局局长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 梁梨宁
    {"person_id": 15, "org_id": 2, "title": "茂南区副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 刘仁生
    {"person_id": 16, "org_id": 2, "title": "茂南区副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 杨海璇
    {"person_id": 17, "org_id": 2, "title": "茂南区副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "民盟盟员"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    # 梁剑辉 — 吕国记: 区委书记 & 区长搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长搭档关系", "overlap_org": "茂南区", "overlap_period": "2025-"},
    # 梁剑辉 — 廖述毅: 前后任区委书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "梁剑辉接替廖述毅任茂南区委书记", "overlap_org": "中共茂南区委", "overlap_period": "2025"},
    # 吕国记 — 廖述毅: 曾经区长+区委书记搭档
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "吕国记任区长时廖述毅任区委书记", "overlap_org": "茂南区", "overlap_period": "2021-2025"},
    # 吕国记 — 吴岳奇: 区长与常务副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与常务副区长工作关系", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 杨杰 — 梁剑辉: 正副书记
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "区委副书记协助区委书记工作", "overlap_org": "中共茂南区委", "overlap_period": ""},
    # 杨杰 — 吕国记: 区委副书记与区长
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "区委副书记与区长党政配合", "overlap_org": "茂南区", "overlap_period": ""},
    # 吕国记 — 杨华靖: 干部人事配合
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "区长与组织部长干部工作配合", "overlap_org": "茂南区", "overlap_period": ""},
    # 梁剑辉 — 詹燕萍: 党委与纪委
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与纪委书记监督关系", "overlap_org": "中共茂南区委", "overlap_period": ""},
    # 梁剑辉 — 李祖源: 党委与政法委
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与政法委书记工作关系", "overlap_org": "中共茂南区委", "overlap_period": ""},
    # 吕国记 — 陈海玲: 区长与公安局长
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长分管公安工作", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吕国记 — 黄建业: 区长与副区长
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吕国记 — 梁梨宁: 区长与副区长
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吕国记 — 刘仁生: 区长与副区长
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吕国记 — 杨海璇: 区长与副区长
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "副区长协助区长工作", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吴岳奇 — 黄建业: 常务副区长与副区长
    {"person_a": 5, "person_b": 13, "type": "overlap", "context": "常务副区长与副区长工作配合", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 吴岳奇 — 梁梨宁: 常务副区长与副区长
    {"person_a": 5, "person_b": 15, "type": "overlap", "context": "常务副区长与副区长工作配合", "overlap_org": "茂南区人民政府", "overlap_period": ""},
    # 杨华靖 — 詹燕萍: 组织与纪委干部监督配合
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "组织部长与纪委书记干部监督配合", "overlap_org": "中共茂南区委", "overlap_period": ""},
    # 李祖源 — 陈海玲: 政法委与公安
    {"person_a": 8, "person_b": 14, "type": "overlap", "context": "政法委书记与公安局长政法工作配合", "overlap_org": "茂南区", "overlap_period": ""},
]


def main() -> None:
    staging = Path(BASE) / "data" / "tmp" / TASK_ID
    staging.mkdir(parents=True, exist_ok=True)

    staging_db = staging / f"{SLUG}_network.db"
    staging_gexf = staging / f"{SLUG}_network.gexf"

    # Write to staging directory
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=staging_db,
        gexf_path=staging_gexf,
        overwrite=True,
    )

    # Also write to canonical paths (for direct use when not using staging)
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

    print(f"\nDone. Files in: {staging}")
    print(f"  DB:    {staging_db}")
    print(f"  GEXF:  {staging_gexf}")
    print(f"\nCanonical paths:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")


if __name__ == "__main__":
    main()
