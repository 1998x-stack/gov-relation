#!/usr/bin/env python3
"""洋县（汉中市）领导班子工作关系网络 — 构建脚本

调查任务: shaanxi_洋县（陕西省 汉中市 洋县，县）
核心调查对象: 县委书记（现任张小平）、县长（现任张军）。
数据来源: 洋县人民政府网站（领导之窗 / 洋县新闻）。web 检索受限(Exa 限流、百度/搜狗反爬、搜索镜像超时)，
        故仅用官方站点直连取证；核心领导人现职均已确认为 official (高置信)。
"""

from __future__ import annotations

import sqlite3  # noqa: used by gov_relation.runner via import
import sys
from pathlib import Path

# Ensure project root is on sys.path
_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "洋县"
STAGING = Path(__file__).parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

AS_OF = "2026-08-07"

# ── 人员定义 ──────────────────────────────────────────────────────────
# 现状确认依据（来自 www.yangxian.gov.cn 官方）:
#  - 张小平: 2026-07-10 县委常委会(扩大)会议“县委书记...主持会议”；2026-07-01 两优一先大会讲话 → 现任县委书记 (confirmed)
#  - 张军: 洋县领导之窗 (县长页)：代理县长 2021.8、县长 2022.3；2026-05-13 人大十八届五次会议作政府工作报告 → 现任县长 (confirmed)
PERSONS = [
    {
        "id": 1,
        "name": "张小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委书记",
        "current_org": "中共洋县委员会",
        "source": "洋县发布 2026-07-10 县委常委会; 2026-07-01 两优一先大会",
    },
    {
        "id": 2,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西·安塞",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委副书记、县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 洋县领导之窗-张军",
    },
    {
        "id": 3,
        "name": "霍波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "四川·三台",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委、常务副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 领导之窗-霍波",
    },
    {
        "id": 4,
        "name": "李国鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县人大常委会主任",
        "current_org": "洋县人民代表大会常务委员会",
        "source": "洋县发布 2026-06-18 警示教育会议; 2026-05-13 人大开幕会",
    },
    {
        "id": 5,
        "name": "路建侠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县政协主席",
        "current_org": "政协洋县委员会",
        "source": "洋县发布 2026-06-18 警示教育会议",
    },
    {
        "id": 6,
        "name": "张飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西·西乡",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县副县长、县公安局局长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 领导之窗-张飞",
    },
    {
        "id": 7,
        "name": "黄海宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西·洋县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 领导之窗-黄海宁",
    },
    {
        "id": 8,
        "name": "李洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西·汉台区",
        "education": "研究生学历",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "洋县副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 领导之窗-李洁",
    },
    {
        "id": 9,
        "name": "周斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "陕西·略阳",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 领导之窗-周斌",
    },
    {
        "id": 10,
        "name": "刘一叶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委、副县长",
        "current_org": "洋县人民政府",
        "source": "洋县发布 2026-07-02 两优一先大会 “县委常委刘一叶”; 政府领导页",
    },
    {
        "id": 11,
        "name": "刘子辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委",
        "current_org": "中共洋县委员会",
        "source": "洋县发布 2026-07-02 两优一先表彰大会",
    },
    {
        "id": 12,
        "name": "王永红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委",
        "current_org": "中共洋县委员会",
        "source": "洋县发布 2026-07-02 两优一先表彰大会",
    },
    {
        "id": 13,
        "name": "廖丹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委",
        "current_org": "中共洋县委员会",
        "source": "洋县发布 2026-07-02 两优一先表彰大会",
    },
    {
        "id": 14,
        "name": "李金林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县县委常委",
        "current_org": "中共洋县委员会",
        "source": "洋县发布 2026-07-02 两优一先表彰大会",
    },
    {
        "id": 15,
        "name": "陈旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 政府领导页",
    },
    {
        "id": 16,
        "name": "夏建国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "洋县副县长",
        "current_org": "洋县人民政府",
        "source": "www.yangxian.gov.cn 政府领导页",
    },
    # 上级(汉中市)背景（来自既有 repo 数据，context）
    {
        "id": 17,
        "name": "张烨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "河北·秦皇岛",
        "education": "大学(法学)、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "1995年",
        "current_post": "汉中市委书记",
        "current_org": "中共汉中市委",
        "source": "data/persons/20260807-陕西省-汉中市-市委书记-张烨.json",
    },
    {
        "id": 18,
        "name": "王建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "未公开",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉中市市长",
        "current_org": "汉中市人民政府",
        "source": "data/persons/20260807-陕西省-汉中市-市长-王建平.json; 2026-07-14 王建平到洋县明察暗访",
    },
]

# ── 组织定义 ──────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中共洋县委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市委", "location": "陕西省汉中市洋县"},
    {"id": 2, "name": "洋县人民政府", "type": "政府", "level": "县处级", "parent": "汉中市人民政府", "location": "陕西省汉中市洋县"},
    {"id": 3, "name": "洋县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "汉中市人民代表大会常务委员会", "location": "陕西省汉中市洋县"},
    {"id": 4, "name": "政协洋县委员会", "type": "政协", "level": "县处级", "parent": "政协汉中市委员会", "location": "陕西省汉中市洋县"},
    {"id": 5, "name": "中共汉中市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "陕西省汉中市"},
    {"id": 6, "name": "汉中市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "陕西省汉中市"},
]

# ── 任职关系 ──────────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "洋县县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作(confirmed 2026-07)"},
    {"person_id": 2, "org_id": 1, "title": "洋县县委副书记", "start_date": "2021-08", "end_date": "present", "rank": "县处级副职", "note": "兼县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "洋县县长", "start_date": "2022-03", "end_date": "present", "rank": "县处级正职", "note": "领导县政府全面工作，分管县财政局、县审计局"},
    {"person_id": 3, "org_id": 2, "title": "洋县县委常委、常务副县长", "start_date": "2024-02", "end_date": "present", "rank": "县处级副职", "note": "负责县政府日常工作"},
    {"person_id": 4, "org_id": 3, "title": "洋县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "洋县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "洋县副县长、县公安局局长", "start_date": "2023-06", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "洋县副县长", "start_date": "2022-03", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "洋县副县长", "start_date": "2021-09", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "洋县副县长", "start_date": "2024-10", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "洋县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "洋县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分工待查"},
    {"person_id": 12, "org_id": 1, "title": "洋县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分工待查"},
    {"person_id": 13, "org_id": 1, "title": "洋县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分工待查"},
    {"person_id": 14, "org_id": 1, "title": "洋县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体分工待查"},
    {"person_id": 15, "org_id": 2, "title": "洋县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "洋县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 上级市领导
    {"person_id": 17, "org_id": 5, "title": "汉中市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "上级领导（洋县县委书记的直接上级）"},
    {"person_id": 18, "org_id": 6, "title": "汉中市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "上级领导（洋县县长的直接上级）"},
]

# ── 工作关系 ──────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记张小平与县委副书记、县长张军，洋县党政主要领导搭档", "overlap_org": "中共洋县委员会/洋县人民政府", "overlap_period": "2021年至今"},
    # 县委与领导班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与常务副县长", "overlap_org": "中共洋县委员会", "overlap_period": "2024-02至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "县委书记与县委常委（刘一叶）", "overlap_org": "中共洋县委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长（县政府日常）", "overlap_org": "洋县人民政府", "overlap_period": "2024-02至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长、公安局长", "overlap_org": "洋县人民政府", "overlap_period": "2023-06至今"},
    {"person_a": 1, "person_b": 4, "type": "党政班底", "context": "县委书记与县人大常委会主任", "overlap_org": "中共洋县委员会/洋县人大", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "党政班底", "context": "县委书记与县政协主席", "overlap_org": "中共洋县委员会/政协洋县委员会", "overlap_period": "至今"},
    # 县委领导班子内部 (2026-07-02 两优一先“县委常委”名单)
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委书记与县委常委刘子辉", "overlap_org": "中共洋县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "县委书记与县委常委王永红", "overlap_org": "中共洋县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "县委书记与县委常委廖丹", "overlap_org": "中共洋县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "县委书记与县委常委李金林", "overlap_org": "中共洋县委员会", "overlap_period": "至今"},
    # 上级市领导关系
    {"person_a": 1, "person_b": 17, "type": "上下级", "context": "洋县县委书记与汉中市委书记（上下级）", "overlap_org": "中共汉中市委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 18, "type": "上下级", "context": "洋县县长与汉中市市长（上下级）", "overlap_org": "汉中市人民政府", "overlap_period": "至今"},
    # 跨县交流网络（履历证据）
    {"person_a": 2, "person_b": 3, "type": "同市跨县", "context": "张军(洋县)后担任勉县常务副县长，霍波曾任城固县委常委——均在汉中市县级领导序列流动", "overlap_org": "汉中市所辖县区", "overlap_period": "早于2024"},
    {"person_a": 6, "person_b": 2, "type": "同市跨县", "context": "张飞此前任留坝县副县长，后调洋县；张军此前任勉县常务副县长", "overlap_org": "汉中市所辖县区", "overlap_period": ""},
    {"person_a": 6, "person_b": 1, "type": "上下级", "context": "副县长(公安局长)受县委书记领导", "overlap_org": "中共洋县委员会", "overlap_period": "2023-06至今"},
]


def main() -> None:
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  调查日期: {AS_OF}")
    print(f"  信息来源: www.yangxian.gov.cn (官方)")
    print("=" * 60)
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF:{GEXF_PATH}")
    run_build(
        slug=f"{SLUG}领导班子关系图",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF:{GEXF_PATH}")


if __name__ == "__main__":
    main()