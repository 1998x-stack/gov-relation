#!/usr/bin/env python3
"""三亚市崖州区领导班子工作关系网络 build script.

任务: hainan_崖州区 (海南省三亚市崖州区, 市辖区)
目标: 区委书记 & 区长
数据基准: 截至 2026-08-07
运行: python3 data/tmp/hainan_崖州区/build_崖州区_data.py
"""

import sqlite3
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── 目录（暂存区）────────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "崖州区_network.db"
GEXF_PATH = STAGING / "崖州区_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)
# 置信度: confirmed=官方来源; plausible=可信媒体/推演; unverified=待查
# ══════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1,
        "name": "季端荣",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三亚市崖州区委书记",
        "current_org": "中共三亚市崖州区委员会",
        "source": "三亚市崖州区人民政府官网领导动态(2025-11至2026-08多篇;2025-12-23区委常委议军会,2026-08-03区委常委会第175次会议)",
    },
    {
        "id": 2,
        "name": "童立艳",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区委副书记、区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml);领导动态(2023-11至2026-07);2025-01三届人大五次会议",
    },
    {
        "id": 3,
        "name": "冯永杰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区政协主席",
        "current_org": "政协三亚市崖州区委员会",
        "source": "崖州区全国文明城市创建工作推进会(2026-06-25)",
    },
    {
        "id": 4,
        "name": "樊木",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原崖州区委书记(约2022年中至2025)",
        "current_org": "",
        "source": "崖州区委书记樊木带队检查台风防御(2022-07);樊木看望慰问一线值班执勤(2025-02);区委书记樊木公开接待群众来访(2024-10)",
    },
    {
        "id": 5,
        "name": "李凯",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 6,
        "name": "郭玄伟",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 7,
        "name": "王道云",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 8,
        "name": "陈隆",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 9,
        "name": "徐辉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 10,
        "name": "李静",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 11,
        "name": "阳超",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区副区长",
        "current_org": "三亚市崖州区人民政府",
        "source": "崖州区人民政府官网区政府领导页(qzf.shtml)",
    },
    {
        "id": 12,
        "name": "黄志刚",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区监察委员会主任(2025当选)",
        "current_org": "崖州区监察委员会",
        "source": "崖州区三届人大五次会议闭幕消息(2025-01)",
    },
    {
        "id": 13,
        "name": "蔡燕",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区人大常委会副主任(2025当选)",
        "current_org": "崖州区人大常委会",
        "source": "崖州区三届人大五次会议闭幕消息(2025-01)",
    },
    {
        "id": 14,
        "name": "陈曦",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区人大主席团常务主席、主持三届人大五次会议闭幕会(即为人大常委会主要任职,plausible)",
        "current_org": "崖州区人大常委会",
        "source": "崖州区三届人大五次会议闭幕消息(2025-01);陈曦主持闭幕会",
    },
    {
        "id": 15,
        "name": "王祺扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三亚市委书记",
        "current_org": "中共三亚市委员会",
        "source": "天涯区调查(2026-07-23);市级领导统筹三亚各区",
    },
    {
        "id": 16,
        "name": "陈希",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "三亚市长",
        "current_org": "三亚市人民政府",
        "source": "天涯区调查(2026-07-23);市级领导统筹三亚各区",
    },
    {
        "id": 17,
        "name": "刘金红",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崖州区人大主席团常务主席",
        "current_org": "崖州区人大常委会",
        "source": "崖州区三届人大五次会议闭幕消息(2025-01)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共三亚市崖州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共三亚市委员会",
        "location": "海南省三亚市崖州区",
    },
    {
        "id": 2,
        "name": "三亚市崖州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "三亚市人民政府",
        "location": "海南省三亚市崖州区",
    },
    {
        "id": 3,
        "name": "三亚市崖州区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "崖州区",
        "location": "海南省三亚市崖州区",
    },
    {
        "id": 4,
        "name": "政协三亚市崖州区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "崖州区",
        "location": "海南省三亚市崖州区",
    },
    {
        "id": 5,
        "name": "崖州区监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共三亚市崖州区委员会",
        "location": "海南省三亚市崖州区",
    },
    {
        "id": 6,
        "name": "中共三亚市委员会",
        "type": "党委",
        "level": "厅局级",
        "parent": "中共海南省委",
        "location": "海南省三亚市",
    },
    {
        "id": 7,
        "name": "三亚市人民政府",
        "type": "政府",
        "level": "厅局级",
        "parent": "海南省人民政府",
        "location": "海南省三亚市",
    },
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 季端荣 (1) 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025-11", "end_date": "present", "rank": "县处级正职/副厅级", "note": "官网首见于2025-11;持续主持区委常委会至2026-08"},
    # 童立艳 (2) 区长
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长", "start_date": "2023-11", "end_date": "present", "rank": "正处级", "note": "官网首见于2023-11;主持区政府全面工作、任区总河河长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2023-11", "end_date": "present", "rank": "县处级", "note": ""},
    # 冯永杰 (3) 政协主席
    {"person_id": 3, "org_id": 4, "title": "区政协主席", "start_date": "2025-01", "end_date": "present", "rank": "县处级正职", "note": "2025-01三届人大五次会议就座;2026-06出席工作会"},
    # 樊木 (4) 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "区委书记", "start_date": "2022-07", "end_date": "2025", "rank": "县处级正职/副厅级", "note": "2022-07检查台风防御至2025-02慰问;任期约2022-2025"},
    # 副区长 (5-11)
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": "官网区政府领导页"},
    # 黄志刚 (12) 监委主任
    {"person_id": 12, "org_id": 5, "title": "区监委主任", "start_date": "2025-01", "end_date": "present", "rank": "县处级", "note": "2025-01三届人大五次会议当选"},
    # 蔡燕 (13) 区人大常委会副主任
    {"person_id": 13, "org_id": 3, "title": "区人大常委会副主任", "start_date": "2025-01", "end_date": "present", "rank": "县处级", "note": "2025-01三届人大五次会议当选"},
    # 陈曦 (14) 人大主席团常务主席
    {"person_id": 14, "org_id": 3, "title": "区人大主席团常务主席/执行主席", "start_date": "2025-01", "end_date": "present", "rank": "县处级", "note": "主持三届人大五次会议闭幕会;较可能兼任人大常委会主要负责人(plausible)"},
    # 王祺扬 (15) 市委书记
    {"person_id": 15, "org_id": 6, "title": "三亚市委书记", "start_date": "2024", "end_date": "present", "rank": "厅局级", "note": "市级领导,统筹三亚四区"},
    # 陈希 (16) 市长
    {"person_id": 16, "org_id": 7, "title": "三亚市长", "start_date": "2021", "end_date": "present", "rank": "厅局级", "note": "市级领导,统筹三亚四区"},
    # 刘金红 (17) 人大主席团常务主席
    {"person_id": 17, "org_id": 3, "title": "区人大主席团常务主席", "start_date": "2025-01", "end_date": "present", "rank": "县处级", "note": "三届人大五次会议主席团"},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记—区长党政搭班子", "overlap_org": "崖州区四家班子", "overlap_period": "2025-11—present"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记—区政协主席四家班子", "overlap_org": "崖州区四家班子", "overlap_period": "2025-11—present"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长—区政协主席", "overlap_org": "崖州区四家班子", "overlap_period": "2025-01—present"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记—区监委主任", "overlap_org": "崖州区四家班子", "overlap_period": "2025-11—present"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "区委书记—区四届人大常委会领导", "overlap_org": "崖州区四家班子", "overlap_period": "2025-11—present"},
    {"person_a": 4, "person_b": 1, "type": "predecessor_successor", "context": "樊木卸任区委书记后由季端荣接任", "overlap_org": "中共三亚市崖州区委员会", "overlap_period": "2025"},
    {"person_a": 4, "person_b": 2, "type": "overlap", "context": "樊木任区委书记时童立艳任区长", "overlap_org": "崖州区四家班子", "overlap_period": "2022-2025"},
    {"person_a": 15, "person_b": 1, "type": "superior_subordinate", "context": "三亚市委书记—崖州区委书记上下级", "overlap_org": "三亚市委", "overlap_period": "2025—present"},
    {"person_a": 16, "person_b": 2, "type": "superior_subordinate", "context": "三亚市长—崖州区区长上下级", "overlap_org": "三亚市人民政府", "overlap_period": "2023—present"},
    {"person_a": 5, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 6, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 7, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 8, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 9, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
    {"person_a": 11, "person_b": 2, "type": "overlap", "context": "副区长—区长政府班子", "overlap_org": "崖州区人民政府", "overlap_period": "2026—present"},
]


def main() -> None:
    run_build(
        slug="崖州区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    conn.close()


if __name__ == "__main__":
    main()