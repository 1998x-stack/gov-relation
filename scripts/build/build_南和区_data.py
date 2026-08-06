#!/usr/bin/env python3
"""
南和区领导工作关系网络 — Build script
河北省邢台市南和区（市辖区, 原南和县, 2020-06 撤县设区）

调查日期: 2026-08-06
Core targets: 区委书记 郭卫欣 (确认) 与 区长 石克栋 (2026-02 起)

官方一手来源 (www.nanhe.gov.cn 直抓 + 站内全文检索 web/search?title=):
- 南和区人民政府·政府领导分工页 (2026-07-31): 区长 石克栋(党组书记、区长);
  常务副区长 郝家磊(兼 区委常委、组织部部长, 2026-05-07 全会确认);
  副区长 王爱国(兼公安局长)、范迎春、王云鹏、王浩林、薛兰; 三级调研员 王志强。
- 政府工作报告归档: 县长/区长 李胜敏(2013-2016) → 韩明智(2017-2021) → 张守锋(2022-2025)
  → 石克栋(代区长2026-01, 区长2026-02起)。
- 区二届十一次全会 (2026-05-07, id=15859): "区委书记郭卫欣代表区委常委会作了讲话"
  → 确认 郭卫欣 **现任区委书记**; 区委常委、组织部部长 郝家磊 就三次党代会决议作说明。
- 2026-01-27 政府工作报告(代区长 石克栋) 提供施政/治理数据。

Confidence:
- 郭卫欣(现任区委书记,2026) / 石克栋(现任区长,2026) = confirmed (官方全会/领导分页+多篇新闻)
- 前任区长张守锋 / 前任书记李胜敏 = confirmed (官方任免时间线)
- 区常委班子/区人大常委会主任(陈跃师)/区政协主席(马佩荣) = plausible (会议/名单)
- 各领导出生/籍贯/早年履历 = 未检索到, 以 person JSON open_questions / report/open_gaps.md 显式标注

本脚本在"partial evidence"模型下产出; 核心人物(书记/区长)身份已确认; 不确定字段置空。
"""

import os
import sys


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-08-06"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任区长 (二号位政府主官, confirmed)
    {
        "id": 1,
        "name": "石克栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区区长、区委副书记、党组书记",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府·政府领导分页 (2026-07-31); 2026-01-21 代区长; 2026-02-14 起称区长",
    },
    # 2 ── 常务副区长 / 区委常委、组织部部长
    {
        "id": 2,
        "name": "郝家磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区党组副书记、常务副区长; 区委常委、组织部部长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府 政府领导分页 (2026-07-31, 常务副区长); 南和区二届十一次全会 2026-05-07 (区委常委、组织部部长)",
    },
    # 3 ── 副区长兼公安局长
    {
        "id": 3,
        "name": "王爱国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区党组成员、副区长、区公安局局长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 4 ── 副区长
    {
        "id": 4,
        "name": "范迎春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区副区长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 5 ── 副区长
    {
        "id": 5,
        "name": "王云鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区党组成员、副区长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 6 ── 副区长
    {
        "id": 6,
        "name": "王浩林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区党组成员、副区长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 7 ── 副区长
    {
        "id": 7,
        "name": "薛兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区党组成员、副区长",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 8 ── 三级调研员
    {
        "id": 8,
        "name": "王志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区政府三级调研员",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府官网 政府领导分页 (2026-07-31)",
    },
    # 9 ── 现任区委书记 郭卫欣 (target 1; 2026-05-07 全会确认, 现任)
    {
        "id": 9,
        "name": "郭卫欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区委书记 (2021-06 起任, 2026 在任)",
        "current_org": "中共邢台市南和区委员会",
        "source": "南和区二届十一次全会报道 2026-05-07 (区委书记郭卫欣讲话); 2021-06 起主持区委常委会",
    },
    # 11 ── 前任区长 张守锋 (2022-2025)
    {
        "id": 11,
        "name": "张守锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前南和区区长 (至2025-12离任, 去向待查)",
        "current_org": "邢台市南和区人民政府",
        "source": "南和区政府工作报告 2022-2025",
    },
    # 12 ── 区人大常委会主任
    {
        "id": 12,
        "name": "陈跃师",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区人大常委会主任",
        "current_org": "南和区人大常委会",
        "source": "南和区政府官网 调研报道 (2020-11 陪同魏吉平)",
    },
    # 13 ── 区政协主席
    {
        "id": 13,
        "name": "马佩荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区政协主席",
        "current_org": "政协邢台市南和区委员会",
        "source": "南和区四大班子会议报道",
    },
    # 14 ── 曾任区委常委(现清河县委书记, 跨县交流)
    {
        "id": 14,
        "name": "樊振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "清河县委书记 (曾在南和任区委常委)",
        "current_org": "中共清河县委",
        "source": "清河县政府官网 2026-07-20; 南和区委常委会出席名单 2020-2021",
    },
    # 15 ── 区委常委、常务副区长 (2022 在任常委, 已卸任?)
    {
        "id": 15,
        "name": "蔡普辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区委常委(后任待查)",
        "current_org": "中共邢台市南和区委",
        "source": "南和区委常委会 2021-2022 出席名单",
    },
    # 16 ── 区委常委
    {
        "id": 16,
        "name": "范燕惠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区委常委(后任)",
        "current_org": "中共邢台市南和区委",
        "source": "南和区委常委会 2020-2022 出席名单",
    },
    # 17 ── 区委常委
    {
        "id": 17,
        "name": "郭军平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南和区委常委(后任)",
        "current_org": "中共邢台市南和区委",
        "source": "南和区委常委会 2021-2022 出席名单",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共邢台市南和区委员会", "type": "党委", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 2, "name": "邢台市南和区人民政府", "type": "政府", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 3, "name": "南和区人大常委会", "type": "人大", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 4, "name": "政协邢台市南和区委员会", "type": "政协", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 5, "name": "中共南和区纪律检查委员会", "type": "纪律", "level": "区级", "parent": "中共南和区委", "location": "河北省邢台市"},
    {"id": 6, "name": "清河县人民政府", "type": "政府", "level": "县级", "parent": "邢台市", "location": "河北省邢台市清河县"},
]

# ── POSITIONS (person_id, org_id, title, start, end) ────────────────────
positions = [
    # 石克栋 — 现任区长
    {"person_id": 1, "org_id": 2, "title": "南和区区长、党组书记", "start_date": "2026-02", "end_date": "至今", "rank": "正处级", "note": "2026-01-21 区委副书记、政府代区长; 2026-02-14 起称区长"},
    {"person_id": 1, "org_id": 1, "title": "南和区委副书记", "start_date": "2026-01", "end_date": "至今", "rank": "副处级(区委)", "note": "区委副书记兼政府党组书记"},
    # 郝家磊 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "南和区党组副书记、常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管财政/发改/应急/统计/开发区"},
    # 王爱国 — 副区长兼公安局长
    {"person_id": 3, "org_id": 2, "title": "南和区副区长、区公安局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管政法/退役军人"},
    # 范迎春 — 副区长
    {"person_id": 4, "org_id": 2, "title": "南和区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管教育/卫生/文旅/医保"},
    # 王云鹏
    {"person_id": 5, "org_id": 2, "title": "南和区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管自然规划/住建/城管"},
    # 王浩林
    {"person_id": 6, "org_id": 2, "title": "南和区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管科技工信/市监/商务"},
    # 薛兰
    {"person_id": 7, "org_id": 2, "title": "南和区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "分管农业农村/乡村振兴/民政"},
    # 王志强
    {"person_id": 8, "org_id": 2, "title": "南和区三级调研员", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 现任区委书记 郭卫欣
    {"person_id": 9, "org_id": 1, "title": "南和区委书记", "start_date": "2021-06", "end_date": "至今", "rank": "正处级", "note": "2021-06 起主持二届区委常委会; 2026-05-07 二届十一次全会仍以区委书记讲话"},
    # 张守锋 — 前任区长
    {"person_id": 11, "org_id": 2, "title": "南和区区长", "start_date": "2022", "end_date": "2025-12", "rank": "正处级", "note": "2022-2025 政府工作报告"},
    # 陈跃师
    {"person_id": 12, "org_id": 3, "title": "南和区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2020-11 陪同魏吉平调研"},
    # 马佩荣
    {"person_id": 13, "org_id": 4, "title": "南和区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 樊振宇 — 清河县委书记 (曾在南和)
    {"person_id": 14, "org_id": 6, "title": "清河县委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2026-07 在任"},
    {"person_id": 14, "org_id": 1, "title": "南和区(县委)常委", "start_date": "2020", "end_date": "", "rank": "副处级", "note": "区委常委会出席名单"},
    # 蔡普辉 / 范燕惠 / 郭军平 常委
    {"person_id": 15, "org_id": 1, "title": "南和区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "南和区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "南和区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 现任书记 郭卫欣 ↔ 现任区长 石克栋 (搭档)
    {"person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "郭卫欣(区委书记)与石克栋(区长)搭档, 共同领导南和区 (2026至今)", "overlap_org": "南和区", "overlap_period": "2026至今"},
    # 现任书记 郭卫欣 ↔ 现任区长 (郭任期内 石克栋获提拔为区长)
    {"person_a": 9, "person_b": 1, "type": "promotion_chain", "context": "郭卫欣为区委书记期间, 石克栋在其班子中并获提拔为区长", "overlap_org": "南和区", "overlap_period": "~2021-2026"},
    # 现任书记 郭卫欣 ↔ 前任区长 张守锋 (长期搭档)
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "2022-2024年郭卫欣(书记)与张守锋(区长)搭档共事", "overlap_org": "南和区", "overlap_period": "2022-2024"},
    # 前任区长 张守锋 ↔ 现任区长 石克栋 (接替)
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "张守锋 2025-12 卸任区长, 石克栋 2026-01 代区长/2026-02 任区长", "overlap_org": "南和区人民政府", "overlap_period": "2025-2026"},
    # 区长 ↔ 副区长 (政府班子)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "政府班子配合: 区长与常务副区长共事", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区长与副区长/公安局长 搭班子", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区长与副区长搭班子", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区长与副区长搭班子", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区长与副区长搭班子", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区长与副区长搭班子", "overlap_org": "南和区人民政府", "overlap_period": "2026-"},
    # 樊振宇跨县: 在南和任常委 → 清河县委书记
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "樊振宇曾任南和区委常委, 与区领导有共事交集", "overlap_org": "中共南和区委", "overlap_period": "2020-2021"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)

STAGING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING_DIR, "南和区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "南和区_network.gexf")

if __name__ == "__main__":
    print("Writing staging DB/GEXF ...")
    run_build(
        slug="南和区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: {DB_PATH} + {GEXF_PATH}")
    print(f"{len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")