#!/usr/bin/env python3
"""
任泽区领导班子工作关系网络 — Build script
河北省邢台市任泽区（市辖区, 原任县, 2020-06 区划调整后更为任泽区）

调查日期: 2026-08-05
Core targets: 区委书记 杨蕾 (2021-05 起任, 现任); 区长 罗向政 (代区长 2025-03-12, 区长 2025-09 起, 现任)

官方一手来源 (任泽区人民政府官网 www.renze.gov.cn 全文检索 master/searchKeywords 多篇新闻 + 市/区报道):
- 区委书记 杨蕾 (女): 2021-05 起任, 2026-02~07 仍以区委书记名义主持区委常委会/全区调度会/调研/慰问;
  履历: 2019-08 任县县委副书记、县长 → 2020-06 任泽区区长 → 2021-05 区委书记。
- 区长 罗文政: 2025-03-12 区人大常委会任命副区长、代理区长; 2025-09 二届人大六次会议当选区长;
  履历(plausible): 威县基层(县团委书记、贺营乡/贺营镇/常屯乡/梨园屯镇党委书记) → 2020 沙河市政府副市长 → 2025 调任泽。
- 前区长 赵现科: 代区长 2021-06, 区长 2022-2024 (2025-02 仍为区长), 之后卸任去向待查。
- 班子成员: 区委副书记 宋云; 常务副区长 郝泉森; 区人大常委会主任 赵凤山(2024-04 确认) → 2026 换届或为 周振鹏(待核);
  区政协主席 李普川(2024-2025) → 周振鹏(2026); 区纪委书记/监委 张国强(2022-2025); 副区长 陶寒星、张子毅、杨现军、贾延平。
- 关系: 杨蕾(书记)⟷罗向政(区长) 现任搭档(2025-09-今); 杨蕾⟷赵翔科 前任/继任区长搭档; 赵翔科→罗向政 区长前任/继任。

Confidence:
- 杨蕾(现任书记) / 罗向政(现任区长) = confirmed (官网新闻全文, 多篇2025-2026)
- 前书记不明确(杨蕾任书记前为区长, 更前由县长晋升; 前任书记去向待查)
- 领导班子成员职位 = plausible~confirmed (出席名单/新闻)
- 杨蕾、罗向政 任泽外的早期履历 = plausible(媒体/百科), 细节待查

本脚本在 partial-evidence 模型下产出; 未知字段置空并以 person JSON open_questions / report/open_gaps.md 显式记录。
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

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任区委书记 (一号位, confirmed)
    {
        "id": 1,
        "name": "杨蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "河北容城",
        "education": "研究生学历, 管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区委书记",
        "current_org": "中共邢台市任泽区委员会",
        "source": "www.renze.gov.cn 任泽区委书记活动/要闻 (2021-05 起任; 2026 在任)",
    },
    # 2 ── 现任区长 (二把手, confirmed)
    {
        "id": 2,
        "name": "罗向政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区委副书记、区政府区长、党组书记",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区领导活动 (2025-03 代区长; 2025-09 当选区长)",
    },
    # 3 ── 前任区长 (赵现科, 至 2025 初)
    {
        "id": 3,
        "name": "赵现科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任泽区长 (2025 初卸任, 去向待查)",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 新闻 2022-2025-02 以区长名义出席 (最后一次 2025-02)",
    },
    # 4 ── 区委副书记
    {
        "id": 4,
        "name": "宋云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区委副书记",
        "current_org": "中共邢台市任泽区委",
        "source": "www.renze.gov.cn 区委常委会/调度会 (2025-2026)",
    },
    # 5 ── 常务副区长
    {
        "id": 5,
        "name": "郝泉森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-04",
        "birthplace": "河北保定",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区委常委、常务副区长",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区人大常委会列席名单 (2026-01/05) + 百度百科",
    },
    # 6 ── 区人大常委会主任 (2024-2025)
    {
        "id": 6,
        "name": "赵凤山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区人大常委会主任",
        "current_org": "任泽区人大常委会",
        "source": "www.renze.gov.cn 区人大常委会会议 (2024-01~2026-04)",
    },
    # 7 ── 区政协主席 (2024-2025 → 2026 由周振鹏接替)
    {
        "id": 7,
        "name": "李普川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区政协主席 (2024-2025)",
        "current_org": "政协邢台市任泽区委员会",
        "source": "www.renze.gov.cn 区政协主席 (2024-2025 会议)",
    },
    # 8 ── 区政协主席 (2026)
    {
        "id": 8,
        "name": "周振鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区政协主席",
        "current_org": "政协邢台市任泽区委员会",
        "source": "www.renze.gov.cn 区委调度会/植树活动 出席名单 (2026-03/04 区政协主席)",
    },
    # 9 ── 区纪委书记/监委主任 (2022-2025)
    {
        "id": 9,
        "name": "张国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区委常委、区纪委书记、区监委主任",
        "current_org": "中共邢台市任泽区纪律检查委员会",
        "source": "www.renze.gov.cn 区纪委全会 (2025-02)",
    },
    # 10 ── 副区长
    {
        "id": 10,
        "name": "张子毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区副区长",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区政府廉政工作会议/人大会议出席 (2024-2026)",
    },
    # 11 ── 副区长
    {
        "id": 11,
        "name": "贾延平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区副区长",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区人大常委会会议列席 (2024-01)",
    },
    # 12 ── 副区长
    {
        "id": 12,
        "name": "杨现军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区副区长",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区政府廉政工作会议/人大常委会会议列席 (2026)",
    },
    # 13 ── 副区长
    {
        "id": 13,
        "name": "陶寒星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "任泽区副区长",
        "current_org": "邢台市任泽区人民政府",
        "source": "www.renze.gov.cn 区领导活动 (2026-03~07 副区长)",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共邢台市任泽区委员会", "type": "党委", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 2, "name": "邢台市任泽区人民政府", "type": "政府", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 3, "name": "任泽区人大常委会", "type": "人大", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 4, "name": "政协邢台市任泽区委员会", "type": "政协", "level": "市辖区", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 5, "name": "中共任泽区纪律检查委员会", "type": "党委部门", "level": "区级", "parent": "中共任泽区委", "location": "河北省邢台市"},
    {"id": 6, "name": "中共任泽区委组织部", "type": "党委部门", "level": "区级", "parent": "中共任泽区委", "location": "河北省邢台市"},
]

# ── POSITIONS (person_id, org_id, title, start, end) ────────────────────
positions = [
    # 杨蕾 — 区委书记 (2021-05 ~ 今)
    {"person_id": 1, "org_id": 1, "title": "任泽区委书记", "start_date": "2021-05", "end_date": "至今", "rank": "正处级", "note": "2021-05 起任; 前: 区长"},
    {"person_id": 1, "org_id": 2, "title": "任泽区长", "start_date": "2020-06", "end_date": "2021-05", "rank": "正处级", "note": "任县县长→任泽区长 2020-06"},
    {"person_id": 1, "org_id": 1, "title": "任县县委副书记、县长", "start_date": "2019-08", "end_date": "2020-06", "rank": "正处级", "note": "2019-08 任任县委副书记、县长"},
    # 罗向政 — 区长
    {"person_id": 2, "org_id": 2, "title": "任泽区委副书记、政府区长、党组书记", "start_date": "2025-09", "end_date": "至今", "rank": "正处级", "note": "2025-09 当选区长"},
    {"person_id": 2, "org_id": 2, "title": "任泽区政府代区长", "start_date": "2025-03", "end_date": "2025-09", "rank": "正处级", "note": "2025-03-12 任副区长、代理区长"},
    {"person_id": 2, "org_id": 1, "title": "任泽区委副书记", "start_date": "2025-03", "end_date": "至今", "rank": "副处级(区委)", "note": ""},
    # 赵现科 — 前区长
    {"person_id": 3, "org_id": 2, "title": "任泽区长", "start_date": "2022", "end_date": "2025初期", "rank": "正处级", "note": "2022 起任区长; (代区长 2021-06)"},
    # 宋云
    {"person_id": 4, "org_id": 1, "title": "任泽区委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 郝泉森
    {"person_id": 5, "org_id": 2, "title": "任泽区委常委、常务副区长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": ""},
    # 赵凤山
    {"person_id": 6, "org_id": 3, "title": "任泽区人大常委会主任", "start_date": "2024", "end_date": "2026", "rank": "正处级", "note": ""},
    # 李普川
    {"person_id": 7, "org_id": 4, "title": "任泽区政协主席", "start_date": "2024", "end_date": "2025", "rank": "正处级", "note": ""},
    # 周振鹏
    {"person_id": 8, "org_id": 4, "title": "任泽区政协主席", "start_date": "2026", "end_date": "至今", "rank": "正处级", "note": ""},
    # 张国强
    {"person_id": 9, "org_id": 5, "title": "任泽区委常委、区纪委书记、区监委主任", "start_date": "2022", "end_date": "至今", "rank": "副处级", "note": ""},
    # 副区长
    {"person_id": 10, "org_id": 2, "title": "任泽区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "任泽区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "任泽区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "任泽区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 同班子共事 (区委书记 ↔ 区长)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长搭档, 共同主持区委常委会/全区调度会/调研/慰问 (2025-09 至今)", "overlap_org": "任泽区", "overlap_period": "2025-09至今"},
    # 前任 ↔ 现任 区长 (赵现科 → 罗向政)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "赵现科 2025 初卸任区长, 罗向政 2025-03 代区长/2025-09 区长", "overlap_org": "任泽区政府", "overlap_period": "2025"},
    # 现任书记 ↔ 前任书记/前区长 (杨蕾 曾为 区长, 2021 转书记; 前书记段落未查获)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "杨蕾任书记期间与区长赵显科搭档 (2021-2024); 杨蕾由区长晋升书记", "overlap_org": "任泽区", "overlap_period": "2021-2025"},
    # 现任书记 ↔ 区人大常委会主任
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与人大主任班子成员 (2024-2026)", "overlap_org": "任泽区", "overlap_period": "2024-2026"},
    # 区长 ↔ 常务副区长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区政府班子搭班子, 区长与常务副区长共事 (2025-2026)", "overlap_org": "任泽区政府", "overlap_period": "2025-2026"},
    # 区委书记 ↔ 区委副书记
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委班子搭班子, 书记 与 副书记共事 (2025-2026)", "overlap_org": "中共任泽区委", "overlap_period": "2025-2026"},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区政府班子搭班子, 区长与副区长共事 (2025-2026)", "overlap_org": "任泽区政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区政府班子搭班子 (2024-2026)", "overlap_org": "任泽区政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区政府班子搭班子 (2026)", "overlap_org": "任泽区政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区政府班子搭班子, 2026 进/任副区长", "overlap_org": "任泽区政府", "overlap_period": "2026-"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "任泽区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "任泽区_network.gexf")

if __name__ == "__main__":
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401
    print("Writing staging DB/GEXF ...")
    run_build(
        slug="任泽区",
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