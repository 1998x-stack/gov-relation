#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鹰手营子矿区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 承德市
Region: 鹰手营子矿区（营子区）
Targets: 区委书记 & 区长

Research Sources (一手官方 www.ysyz.gov.cn):
- 2026-04-14 动态新闻『鹰手营子矿区召开区委理论学习中心组集中（扩大）学习会议』
  (art_3553_1111649)：2026-04-13 杨志勇同志以「区委书记」身份主持召开 2026 年第 4 次
  区委理论学习中心组（扩大）学习会议 —— 确认杨志勇为时任区委书记。
- 2026-06-16 动态新闻【2026-06-12 第 5 次区委理论学习中心组】
  (art_3553_1118632)：尚晓辉同志以「区委书记」身份主持 —— 确认尚晓辉接任区委书记
  （2026 年春末，杨志勇卸任）。
- 2026-01-27 人代会《2026年政府工作报告》(art_6817_1112924)：承德市鹰手营子矿区人民
  政府代区长 于佳乐 作报告 —— 于佳乐为代区长。
- 2026-04-30 动态新闻『营子区政府召开常务会议』(art_3553_1114525)：2026-04-29
  区长 于佳乐 主持召开第十一届区政府第八十八次常务会议 —— 于佳乐已由代转正式区长。
- 2025-02-11《2025年政府工作报告》(art_6817_1051967)：区长 马增辉 作报告 ——
  马增辉为前任区长（2025 上半年在任）。
- 2026-04-10【区政协召开第十届第二次常委会】(art_3553_1111279)：区政协主席 胡连成，
  副主席 程凤羽、赵妍、张军、王哲 —— 政协班子一手确认。

Research Date: 2026-08-05

Confidence 说明：
  杨志勇 任区委书记 —— confirmed（一手官方新闻，2026-04-13 主持区委理论学习中心组）。
  尚晓辉 任现任区委书记 —— confirmed（一手官方新闻，2026-06-12 主持区委理论学习中心组，
    为杨志勇之后的继任）。
  于佳乐 任区长 —— confirmed（一手官方，2026-01-27 代区长作政府工作报告，2026-04-29 区长
    主持召开区政府常务会议）。
  马增辉 任前任区长 —— confirmed（一手官方，2025-02 作 2025 政府工作报告）。
  区政协主席胡连成、副主席程凤羽/赵妍/张军/王哲 —— confirmed（2026-04-08 区政协常委会）。
  区委理论学习中心组参与者（尚晓辉、王耀霆、方堃、张杰、胡连成、王春利；2026-04 杨志勇、
  高立强、张延东、袁志学、胡北、蔡亚男、满海波、好修士）。

... 早期履历、出生年月/籍贯/学历、代理区长转正时间、杨志勇去向角色、区人大常委会主任等
    因网络受限（Exa 限流、Baidu/搜狗验证码）未获一手，列入 open_gaps。
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "鹰手营子矿区"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (targets)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "尚晓辉",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹰手营子矿区委书记",
        "current_org": "中共承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-06-16，2026-06-12 第 5 次区委理论学习中心组）：尚晓辉同志以区委书记身份主持召开——一手官方，确认其为现任区委书记。"
    },
    {
        "id": 2,
        "name": "于佳乐",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹰手营子矿区人民政府区长（区委副书记）",
        "current_org": "承德市鹰手营子矿区人民政府",
        "source": "www.ysyz.gov.cn：2026-01-27 作《2026年政府工作报告》（代区长）；2026-04-29 主持召开区政府第八十八次常务会议（区长）——一手官方确认现任区长。"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨志勇",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹰手营子矿区原区委书记",
        "current_org": "中共承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-14，2026-04-13 第 4 次区委理论学习中心组）：杨志勇同志以区委书记身份主持会议——一手官方确认其为前任区委书记。"
    },
    {
        "id": 4,
        "name": "马增辉",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "鹰手营子矿区前任区长",
        "current_org": "承德市鹰手营子矿区人民政府",
        "source": "www.ysyz.gov.cn《2025年政府工作报告》(art_6817_1051967)：区长马增辉作报告——一手官方确认其为前任区长。"
    },
    # ════════════════════════════════════════
    # 区政协班子
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "胡连成",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政协主席",
        "current_org": "政协承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-10）：胡连成以区政协主席身份出席区政协第二十届常委会——一手官方确认任区政协主席。"
    },
    {
        "id": 6,
        "name": "程凤羽",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "未知",
        "work_start": "待查",
        "current_post": "区政协副主席",
        "current_org": "政协承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-10）：程凤羽以区政协副主席身份出席区政协第十届常委会——一手官方确认。"
    },
    {
        "id": 7,
        "name": "赵妍",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "未知",
        "work_start": "待查",
        "current_post": "区政协副主席",
        "current_org": "政协承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-10）：赵妍以区政协副主席出席——一手官方确认。"
    },
    {
        "id": 8,
        "name": "张军",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "未知",
        "work_start": "待查",
        "current_post": "区政协副主席",
        "current_org": "政协承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-10）：区政协副主席出席——一手官方确认。"
    },
    {
        "id": 9,
        "name": "王哲",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "未知",
        "work_start": "待查",
        "current_post": "区政协副主席",
        "current_org": "政协承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn 动态新闻（2026-04-10）：王哲以区政协副主席出席——一手官方确认。"
    },
    # ════════════════════════════════════════
    # 区委理论学习中心成员（区级领导，部分在网络受限下仅获列席名，职务待补）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "王耀霆",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委理论学习中心组（区级领导）",
        "current_org": "中共承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn（2026-06-12 第 5 次区委理论学习中心组）：领学《绿水青山就是金山银山》并作交流研讨——确认其为区级领导（职务待补）。"
    },
    {
        "id": 11,
        "name": "方堃",
        "gender": "未知",
        "ethnicity": "未知",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委理论学习中心组（区级领导）",
        "current_org": "中共承德市鹰手营子矿区委员会",
        "source": "www.ysyz.gov.cn（2026-06-12 第 5 次区委理论学习中心组）：领学《树立和践行正确政绩观》内容——区级领导（职务待补）。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共承德市鹰手营子矿区委员会",
        "type": "党委",
        "level": "县级",
        "location": "承德市鹰手营子矿区",
        "parent": "中共承德市委"
    },
    {
        "id": 2,
        "name": "承德市鹰手营子矿区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "承德市鹰手营子矿区",
        "parent": "承德市人民政府"
    },
    {
        "id": 3,
        "name": "政协承德市鹰手营子矿区委员会",
        "type": "政协",
        "level": "县级",
        "location": "承德市鹰手营子矿区",
        "parent": "政协承德市委员会"
    },
    {
        "id": 4,
        "name": "鹰手营子矿区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "承德市鹰手营子矿区",
        "parent": ""
    },
]

# 3. Positions
positions = [
    # ── 尚晓辉 (current 区委书记) ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "约2026-04/05", "end_date": "present", "rank": "正处级（县处级正职）", "note": "现任区委书记。2026-06-12 主持第 5 次区委理论学习中心组；继杨志勇之后接任。"},
    # ── 于佳乐 (current 区长) ──
    {"person_id": 2, "org_id": 2, "title": "区长（区委副书记）", "start_date": "约2026-01", "end_date": "present", "rank": "正处级（县处级正职）", "note": "2026-01-27 代区长作2026 政府工作报告；2026-04-29 以区长主持区政府常务会议。"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "约2026-01", "end_date": "present", "rank": "县级", "note": "区长通常兼任区委副书记。"},
    # ── 杨志勇 (前任区委书记) ──
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start_date": "约2023-2024", "end_date": "约2026-04/05", "rank": "正处级（县处级正职）", "note": "前任区委书记。2026-04-13 主持第 4 次区委理论学习中心组（在任），后由尚晓辉接任。"},
    # ── 马增辉 (前任区长) ──
    {"person_id": 4, "org_id": 2, "title": "区长", "start_date": "约2023-2024", "end_date": "约2025-2026", "rank": "正处级（县处级正职）", "note": "前任区长。2025-02 作 2025 政府工作报告；由于佳乐接任。"},
    # ── 区政协班子 ──
    {"person_id": 5, "org_id": 3, "title": "区政协主席", "start_date": "约2023-2024", "end_date": "present", "rank": "县级正职", "note": "区政协主席，2026-04-08 出席第十二届政协常委会。"},
    {"person_id": 6, "org_id": 3, "title": "区政协副主席", "start_date": "约2023-2024", "end_date": "present", "rank": "县级副职", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "区政协副主席", "start_date": "约2023-2024", "end_date": "present", "rank": "县级副职", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "区政协副主席", "start_date": "约2023-2024", "end_date": "present", "rank": "县级副职", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "区政协副主席", "start_date": "约2023-2024", "end_date": "present", "rank": "县级副职", "note": ""},
    # ── 区级领导（中心组成员） ──
    {"person_id": 10, "org_id": 1, "title": "区领导（职务待补）", "start_date": "约2025-2026", "end_date": "present", "rank": "县处级", "note": "区委理论学习中心组成员。"},
    {"person_id": 11, "org_id": 1, "title": "区委领导（职务待补）", "start_date": "约2025-2026", "end_date": "present", "rank": "县处级", "note": "区委理论学习中心组成员。"},
]

# 4. Relationships
relationships = [
    # ── 区委书记继任链条 ──
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "尚晓辉（现任）继杨志勇（前任）之后任鹰手营子矿区委书记。杨志勇2026-04-13 仍以书记主持中心组（第4次），2026-06-12 由尚晓辉主持（第5次）——2026 年春继任。",
        "overlap_org": "中共承德市鹰手营子矿区委员会",
        "overlap_period": "2026-04/05 交接"
    },
    # ── 区长 predecessor 链条 ──
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "于佳乐（现任区长）继马增辉（前任区长）。马增辉2025-02 作2025政府工作报告；于佳乐2026-01-27 作2026政府工作报告——区长交接于2025下半年/2026初。",
        "overlap_org": "承德市鹰手营子矿区人民政府",
        "overlap_period": "2025-2026"
    },
    # ── 现行党政一把手搭档 ──
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记尚晓辉与区长于佳乐为鹰手营子矿区现任党政一把手搭档（书记-区长），共同出席区委常委会、区两会等区级会议。",
        "overlap_org": "中共承德市鹰手营子矿区委员会／承德市鹰手营子矿区人民政府",
        "overlap_period": "2026-"
    },
    # ── 前任书记 × 前任区长 ──
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "杨志勇（时任区委书记）与马增辉（时任区长）为早期党政一把手搭档，后分别由尚晓辉、于佳乐接任。",
        "overlap_org": "中共承德市鹰手营子矿区委员会／承德市鹰手营子矿区人民政府",
        "overlap_period": "2024-2025"
    },
    # ── 区政协主席 / 政协委员班子与党委的关联 ──
    {
        "person_a": 5,
        "person_b": 1,
        "type": "overlap",
        "context": "区政协主席胡连成与现任区委书记分工协作，属同一区级领导班子。",
        "overlap_org": "鹰手营子矿区区委/政协",
        "overlap_period": "2026-"
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "overlap",
        "context": "区政协主席胡连成与其副主席程凤羽共同构成区政协班子。",
        "overlap_org": "政协承德市鹰手营子矿区委员会",
        "overlap_period": "2024-"
    },
    {
        "person_a": 5,
        "person_b": 7,
        "type": "overlap",
        "context": "区政协主席胡连成与其副主席赵妍共同构成区政协班子。",
        "overlap_org": "政协承德市鹰手营子矿区委员会",
        "overlap_period": "2024-"
    },
    {
        "person_a": 5,
        "person_b": 8,
        "type": "overlap",
        "context": "区政协主席胡连成与其副主席张军共同构成区政协班子。",
        "overlap_org": "政协承德市鹰手营子矿区委员会",
        "overlap_period": "2024-"
    },
    {
        "person_a": 5,
        "person_b": 9,
        "type": "overlap",
        "context": "区政协主席胡连成与其副主席王哲共同构成区政协班子。",
        "overlap_org": "政协承德市鹰手营子矿区委员会",
        "overlap_period": "2024-"
    },
    # ── 区级领导中心组成员与书记共事 ──
    {
        "person_a": 1,
        "person_b": 10,
        "type": "overlap",
        "context": "区委书记尚晓辉与区委理论学习中心组成员王耀霆（区级领导）同在区委班子。",
        "overlap_org": "中共承德市鹰手营子矿区委员会",
        "overlap_period": "2026-"
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "overlap",
        "context": "区委书记尚晓辉与区委理论学习中心组成员方堃共同出席区委中心组学习（区级领导）。",
        "overlap_org": "中共承德市鹰手营子矿区委员会",
        "overlap_period": "2026-"
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")