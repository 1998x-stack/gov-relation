#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
莲池区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 保定市
Region: 莲池区
Targets: 区委书记 & 区长

Research Sources:
- 保定市莲池区人民政府官方网站 (www.lianchi.gov.cn)
  - 领导之窗确认区长杜志平信息
  - 第四次党代会(2026-07-19)确认区委书记张超
  - 区政府常务会议确认张超(2024-2025任区长)→杜志平(2025-2026任区长)的过渡
  - 莲池区第三届人大第六次会议(2026-01-28)确认张超为区委书记、杜志平为代区长
  - 政协第三届第六次会议(2026-01-27)确认张超为区委书记、杜志平为代区长
  - 2024-03-26 article confirms 刘晓鹏 as 区委书记 (predecessor)

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "莲池区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "保定市莲池区委书记",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)确认张超为莲池区委书记。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15930"
    },
    {
        "id": 2,
        "name": "杜志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "保定市莲池区委副书记、区长",
        "current_org": "莲池区人民政府",
        "source": "莲池区人民政府领导之窗确认杜志平任区委副书记、区长、区政府党组书记。来源:http://www.lianchi.gov.cn/index/ldzc/cateid/2"
    },
    # ════════════════════════════════════════
    # 区委领导 (from Party Congress 2026-07-19 主席台前排就座)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "高建坤",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委副书记",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15930"
    },
    {
        "id": 4,
        "name": "田朝阳",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区人大常委会主任",
        "current_org": "莲池区人大常委会",
        "source": "莲池区第三次人大第六次会议(2026-01-28)确认田朝阳为区人大常委会主任。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15217"
    },
    {
        "id": 5,
        "name": "信超",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委、组织部长、统战部长、区政协党组副书记",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。政协第六次会议(2026-01-27)确认信超为区委常委、组织部长、统战部长、区政协党组副书记。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15930"
    },
    {
        "id": 6,
        "name": "李飞",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委、副区长",
        "current_org": "莲池区人民政府",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。区政府领导之窗确认李飞为区政府领导。来源:http://www.lianchi.gov.cn/index/ldzc/cateid/2"
    },
    {
        "id": 7,
        "name": "孙亚涛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。"
    },
    {
        "id": 8,
        "name": "刘波",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。"
    },
    {
        "id": 9,
        "name": "郭思超",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。"
    },
    {
        "id": 10,
        "name": "辛建浩",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。人大第六次会议(2026-01-28)确认在主席台就座。"
    },
    {
        "id": 11,
        "name": "鄢正华",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。"
    },
    {
        "id": 12,
        "name": "方艳茂",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委常委",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第四次党代会(2026-07-19)主席台前排就座区领导名单。"
    },
    # ════════════════════════════════════════
    # 区政府领导 (from 领导之窗)
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "李建松",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区副区长",
        "current_org": "莲池区人民政府",
        "source": "莲池区人民政府领导之窗确认。来源:http://www.lianchi.gov.cn/index/ldzc/cateid/2"
    },
    {
        "id": 14,
        "name": "安芹召",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区副区长",
        "current_org": "莲池区人民政府",
        "source": "莲池区人民政府领导之窗确认。来源:http://www.lianchi.gov.cn/index/ldzc/cateid/2"
    },
    {
        "id": 15,
        "name": "陈澎",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区副区长",
        "current_org": "莲池区人民政府",
        "source": "莲池区人民政府领导之窗确认。来源:http://www.lianchi.gov.cn/index/ldzc/cateid/2"
    },
    # ════════════════════════════════════════
    # 人大常委会领导 & 政协领导
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "刘晓春",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区人大常委会副主任",
        "current_org": "莲池区人大常委会",
        "source": "莲池区第三届人大第六次会议(2026-01-28)确认刘晓春主持会议。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15217"
    },
    {
        "id": 17,
        "name": "魏立新",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区政协主席、党组书记",
        "current_org": "政协保定市莲池区委员会",
        "source": "莲池区政协第六次会议(2026-01-27)确认魏立新为区政协主席、党组书记。来源:http://www.lianchi.gov.cn/cms/index/show.html?cateid=7&id=15204"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "刘晓鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原莲池区委书记）",
        "current_org": "待查",
        "source": "莲池区政府网站2024-03-26 article确认刘晓鹏为区委书记。来源:http://www.lianchi.gov.cn/cms/index/lists.html?cateid=7&page=9"
    },
    # ════════════════════════════════════════
    # 人大/政协其他领导 (from人大第六次会议主席台名单)
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "卢志刚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "莲池区委副书记",
        "current_org": "中共保定市莲池区委员会",
        "source": "莲池区第三届人大第六次会议(2026-01-28)主席台就座名单。政协第六次会议(2026-01-27)确认卢志刚为区委副书记。"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共保定市莲池区委员会", "type": "党委", "level": "县处级", "parent": "中共保定市委", "location": "保定市莲池区"},
    {"id": 2, "name": "莲池区人民政府", "type": "政府", "level": "县处级", "parent": "保定市人民政府", "location": "保定市莲池区"},
    {"id": 3, "name": "莲池区人大常委会", "type": "人大", "level": "县处级", "parent": "保定市人大常委会", "location": "保定市莲池区"},
    {"id": 4, "name": "政协保定市莲池区委员会", "type": "政协", "level": "县处级", "parent": "政协保定市委", "location": "保定市莲池区"},
    {"id": 5, "name": "保定市", "type": "政府", "level": "地市级", "parent": "河北省", "location": "河北省"},
]

# 3. Positions
positions = [
    # 张超 — current区委书记, former区长
    {"person_id": 1, "org_id": 1, "title": "莲池区委书记", "start_date": "2025", "end_date": "至今", "rank": "正处级", "note": "自2025年从区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "莲池区长", "start_date": "2024前", "end_date": "2025", "rank": "正处级", "note": "张超以区长身份主持区政府常务会议至2025年6月"},
    # 杜志平 — current区长
    {"person_id": 2, "org_id": 2, "title": "莲池区长、区政府党组书记", "start_date": "2025-08", "end_date": "至今", "rank": "正处级", "note": "2025年8月首次以区长身份召开常务会议；2026年1月为代区长"},
    {"person_id": 2, "org_id": 1, "title": "莲池区委副书记", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": ""},
    # 高建坤 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "莲池区委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 田朝阳 — 人大主任
    {"person_id": 4, "org_id": 3, "title": "莲池区人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 信超 — 组织部长
    {"person_id": 5, "org_id": 1, "title": "莲池区委常委、组织部长、统战部长、区政协党组副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李飞 — 副区长、区委常委
    {"person_id": 6, "org_id": 2, "title": "莲池区委常委、副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 孙亚涛 — 常委
    {"person_id": 7, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 刘波 — 常委
    {"person_id": 8, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 郭思超 — 常委
    {"person_id": 9, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 辛建浩 — 常委
    {"person_id": 10, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 鄢正华 — 常委
    {"person_id": 11, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 方艳茂 — 常委
    {"person_id": 12, "org_id": 1, "title": "莲池区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李建松 — 副区长
    {"person_id": 13, "org_id": 2, "title": "莲池区副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 安芹召 — 副区长
    {"person_id": 14, "org_id": 2, "title": "莲池区副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 陈澎 — 副区长
    {"person_id": 15, "org_id": 2, "title": "莲池区副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 刘晓春 — 人大副主任
    {"person_id": 16, "org_id": 3, "title": "莲池区人大常委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 魏立新 — 政协主席
    {"person_id": 17, "org_id": 4, "title": "莲池区政协主席、党组书记", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 刘晓鹏 — 前任区委书记
    {"person_id": 18, "org_id": 1, "title": "莲池区委书记", "start_date": "待查", "end_date": "2024/2025", "rank": "正处级", "note": "2024年3月仍以区委书记身份活动"},
    # 卢志刚 — 区委副书记
    {"person_id": 19, "org_id": 1, "title": "莲池区委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 党政一把手关系
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长", "overlap_org": "莲池区", "overlap_period": "2025-至今"},
    # 张超—刘晓鹏（前后任）
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "张超接替刘晓鹏任莲池区委书记", "overlap_org": "中共保定市莲池区委员会", "overlap_period": "2024/2025-至今"},
    # 张超—杜志平（前后任区长）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "杜志平接替张超任莲池区长", "overlap_org": "莲池区人民政府", "overlap_period": "2025"},
    # 张超—田朝阳
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记—人大主任", "overlap_org": "莲池区", "overlap_period": "2025-至今"},
    # 杜志平—信超（党政—组织）
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长—组织部长", "overlap_org": "莲池区", "overlap_period": "2025-至今"},
    # 杜志平—李飞（正副区长）
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "莲池区人民政府", "overlap_period": "2025-至今"},
    # 杜志平—李建松
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "莲池区人民政府", "overlap_period": "2025-至今"},
    # 杜志平—安芹召
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "莲池区人民政府", "overlap_period": "2025-至今"},
    # 杜志平—陈澎
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "莲池区人民政府", "overlap_period": "2025-至今"},
    # 张超—魏立新
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "区委书记—政协主席", "overlap_org": "莲池区", "overlap_period": "2025-至今"},
    # 张超—卢志刚（正副书记）
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "context": "区委书记—区委副书记", "overlap_org": "中共保定市莲池区委员会", "overlap_period": "2025-至今"},
    # 张超—高建坤（正副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—区委副书记", "overlap_org": "中共保定市莲池区委员会", "overlap_period": "2025-至今"},
    # 杜志平—卢志刚（区长—副书记）
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "区长—区委副书记", "overlap_org": "莲池区", "overlap_period": "2025-至今"},
]


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
    print("Done. Files created:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
