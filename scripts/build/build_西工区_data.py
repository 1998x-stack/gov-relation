#!/usr/bin/env python3
"""Build the 西工区 (Xigong District, 洛阳市, 河南省) personnel network.

Research date: 2026-08-05
Sources: official www.xigong.gov.cn leadership pages + confirmed news reports.
Confidence: Leader identities + current roster confirmed from official district site;
career timelines for core figures partial (张丽娟/袁峥 prior roles pending deeper research).
"""

import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

import sqlite3  # noqa: F401  (used by gov_relation.runner for schema)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "西工区_network.db"
GEXF_PATH = STAGING_DIR / "西工区_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "张丽娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委书记、区人武部党委第一书记",
        "current_org": "中共西工区委员会",
        "source": "http://www.xigong.gov.cn/2026/07-30/1076754.html 区人武部党委第一书记任职宣布大会（2026-06-16任）; 2026-07多项活动以区委书记身份主持",
    },
    {
        "id": 2,
        "name": "袁峥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "大学学历、工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委副书记、区长、区政府党组书记",
        "current_org": "西工区人民政府",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页（2026-04-25当选区长）",
    },
    {
        "id": 3,
        "name": "李夏影",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委副书记",
        "current_org": "中共西工区委员会",
        "source": "区十五届人大四/七次会议主席台名单（2024-2026）",
    },
    {
        "id": 4,
        "name": "高国龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年4月",
        "birthplace": "",
        "education": "本科学历、管理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委常委、副区长",
        "current_org": "西工区人民政府",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 5,
        "name": "王彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1991年10月",
        "birthplace": "",
        "education": "硕士学历、环境工程专业硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委常委、宣传部部长、副区长",
        "current_org": "中共西工区委员会",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 6,
        "name": "吴彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委常委、纪委书记、区监委主任",
        "current_org": "西工区纪委监委",
        "source": "区十五届人大四次会议选举（2024-01当选区监委主任）| 主席台就座名单",
    },
    {
        "id": 7,
        "name": "关云波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "education": "本科文化程度、法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区副区长",
        "current_org": "西工区人民政府",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 8,
        "name": "薛耀辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区副区长、洛阳市公安局西工分局局长",
        "current_org": "洛阳市公安局西工分局",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 9,
        "name": "柳瑞丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区副区长",
        "current_org": "西工区人民政府",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 10,
        "name": "孟庆凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区副区长",
        "current_org": "西工区人民政府",
        "source": "http://www.xigong.gov.cn/zwgk/zfxxgk/zfxxgkml/zfld/ 官方政府领导页",
    },
    {
        "id": 11,
        "name": "王建伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区委常委/区领导",
        "current_org": "中共西工区委员会",
        "source": "张丽娟调研报道（2026-07）随同区领导；人大会议主席台名单",
    },
    {
        "id": 12,
        "name": "周传江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区领导/区委常委",
        "current_org": "中共西工区委员会",
        "source": "区人武部党委第一书记任职宣布大会列席（2026-06），人大会议主席台名单",
    },
    {
        "id": 13,
        "name": "王升",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西工区领导",
        "current_org": "中共西工区委员会",
        "source": "区人武部党委第一书记任职宣布大会列席（2026-06），人大会议主席台名单",
    },
    {
        "id": 14,
        "name": "王进",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任西工区委书记（2026Q1卸任）",
        "current_org": "中共西工区委员会",
        "source": "2024-01人大四次会议以区委书记身份讲话；2026-04人大七次会议主席台常务主席；去向未确认",
    },
    {
        "id": 15,
        "name": "史千灵",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任西工区区长（2026年4月前卸任）",
        "current_org": "西工区人民政府",
        "source": "区十五届人大四次会议（2024）主席台常务主席、区长；2026-04人大七次会议前离任",
    },
]
# 其他区领导（列席/quota）：李振江、叶占芳、苏娜、李海雅、张红涛、常丹（作为班子扩展，统一在组织关系中体现）
# 依据区政府领导页 + 人大会议（2024/2026）到场区领导名单

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共西工区委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "洛阳市西工区"},
    {"id": 2, "name": "西工区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "洛阳市西工区"},
    {"id": 3, "name": "西工区人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "洛阳市西工区"},
    {"id": 4, "name": "西工区政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "洛阳市西工区"},
    {"id": 5, "name": "西工区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "洛阳市西工区"},
    {"id": 6, "name": "西工区监察委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市监察委员会", "location": "洛阳市西工区"},
    {"id": 7, "name": "西工区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共西工区委员会", "location": "洛阳市西工区"},
    {"id": 8, "name": "洛阳市公安局西工分局", "type": "政府", "level": "乡科级", "parent": "洛阳市公安局", "location": "洛阳市西工区"},
    {"id": 9, "name": "区人武部（西工区人民武装部）", "type": "党委", "level": "乡科级", "parent": "洛阳军分区", "location": "洛阳市西工区"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 张丽娟 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "西工区委书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级正职", "note": "2026-06-16任区人武部党委第一书记（区委书记兼任）"},
    {"person_id": 1, "org_id": 9, "title": "区人武部党委第一书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级正职", "note": "任职宣布大会（2026-06-16）"},
    # 袁峥 — 区长
    {"person_id": 2, "org_id": 1, "title": "西工区委副书记", "start_date": "2026-04", "end_date": "present", "rank": "县处级副职", "note": "官方领导页确认"},
    {"person_id": 2, "org_id": 2, "title": "西工区区长、区政府党组书记", "start_date": "2026-04", "end_date": "present", "rank": "县处级正职", "note": "2026-04-25区十五届人大七次会议当选"},
    # 李夏影 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "西工区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人大会议主席台名单"},
    # 高国龙
    {"person_id": 4, "org_id": 1, "title": "西工区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方政府领导页"},
    # 王彬
    {"person_id": 5, "org_id": 1, "title": "西工区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "西工区委宣传部部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "官方政府领导页"},
    # 吴彦 — 纪委书记/监委主任
    {"person_id": 6, "org_id": 1, "title": "西工区委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "西工区纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "西工区监察委员会主任", "start_date": "2024-01", "end_date": "present", "rank": "县处级正职", "note": "2024-01区十五届人大四次会议当选"},
    # 关云波
    {"person_id": 7, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 薛耀辉 — 副区长/公安分局局长
    {"person_id": 8, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    {"person_id": 8, "org_id": 8, "title": "洛阳市公安局西工分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "党委书记"},
    # 柳瑞丽
    {"person_id": 9, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 孟庆凯
    {"person_id": 10, "org_id": 2, "title": "西工区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 王建伟
    {"person_id": 11, "org_id": 1, "title": "西工区委常委（区领导）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "随同区委书记调研"},
    # 周传江
    {"person_id": 12, "org_id": 1, "title": "西工区领导（区委常委）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人武部任职宣布大会列席"},
    # 王升
    {"person_id": 13, "org_id": 1, "title": "西工区领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "人武部任职宣布大会列席"},
    # 王进 — 前任区委书记
    {"person_id": 14, "org_id": 1, "title": "西工区委书记", "start_date": "2023", "end_date": "2026", "rank": "县处级正职", "note": "至少2023年在任；2026年4月前/后续卸任，去向未确认"},
    # 史千灵 — 前任区长
    {"person_id": 15, "org_id": 1, "title": "西工区委副书记", "start_date": "2024", "end_date": "2026-04", "rank": "县处级副职", "note": "2024年前在任"},
    {"person_id": 15, "org_id": 2, "title": "西工区区长", "start_date": "2024", "end_date": "2026-04", "rank": "县处级正职", "note": "2026-04区人大七会议前卸任"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# 关系基于官方领导页/人大会议主席台名单/区委重要会议列席记录，全部为当前在任的确认关系。

relationships = [
    # 现任四大班子对子
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长搭档（书长对子）", "overlap_org": "中共西工区委员会 / 西工区人民政府", "overlap_period": "2026-06至今"},
    # 区委书记—常委会成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委、宣传部长", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区委常委、纪委书记", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    # 区长—副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长（常委）", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长（宣传部长）", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长兼公安分局长", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    # 常委会成员之间（同事/同僚）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为区委常委/政府班子", "overlap_org": "中共西工区委员会 / 西工区人民政府", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为区委常委", "overlap_org": "中共西工区委员会", "overlap_period": "当前"},
    # 政府班子内部共事
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "同区政府班子", "overlap_org": "西工区人民政府", "overlap_period": "当前"},
    # 前任/继任链
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记→现任区委书记（王进→张丽娟）", "overlap_org": "中共西工区委员会", "overlap_period": "2026年换届"},
    {"person_a": 15, "person_b": 2, "type": "predecessor_successor", "context": "前任区长→现任区长（史千灵→袁峥）", "overlap_org": "西工区人民政府", "overlap_period": "2026-04换届"},
    # 前任对子
    {"person_a": 14, "person_b": 15, "type": "superior_subordinate", "context": "前任区委书记与前任区长搭档", "overlap_org": "中共西工区委员会 / 西工区人民政府", "overlap_period": "2024-2026"},
]

# ── Run Build ────────────────────────────────────────────────────────────────

SLUG = "西工区"

if __name__ == "__main__":
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print(f"\nDone. Files in {STAGING_DIR}:")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")