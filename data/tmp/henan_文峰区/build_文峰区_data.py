#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 文峰区 (Wenfeng District, Anyang, Henan) leadership network.

文峰区 — 河南省安阳市辖区, 安阳市中心城区, 总面积179平方公里,
辖12个街道、1个镇, 常住人口约60万.

Data sources:
- 网易新闻 (2024-03-25): 文峰区委书记崔元锋带队调研软弱涣散村整顿工作
- 安阳市人民政府门户网站 (www.anyang.gov.cn) — references to Wenfeng District
- 文峰区人民政府门户网站 (www.wenfeng.gov.cn) — inaccessible during investigation

Confidence notes:
- 区委书记崔元锋: confirmed (163.com news, 2024-03-25)
- 区长姓名: unverified (could not access wenfeng.gov.cn or find recent appointment notices)
- 副区长列表: unverified (could not access official leadership page)
- 区委常委会成员: unknown (no accessible source)
- Career timelines: unverified (no biographical data accessible)
- ALL claims not marked "confirmed" should be treated as unverified
"""
from __future__ import annotations

import sys
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_文峰区"
DB_PATH = STAGING / "文峰区_network.db"
GEXF_PATH = STAGING / "文峰区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 崔元锋
    # Source: 网易新闻 2024-03-25 "文峰区委书记崔元锋带队调研指导软弱涣散村整顿工作"
    {"id": 1, "name": "崔元锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委书记", "current_org": "中共文峰区委",
     "source": "网易新闻 2024-03-25; 文峰区人民政府门户网站（无法访问）"},

    # 区长 — 未确认
    {"id": 2, "name": "待确认-文峰区区长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委副书记、区长（待确认）", "current_org": "文峰区人民政府",
     "source": "文峰区人民政府门户网站无法访问；未找到任前公示"},

    # ══════════════════════════════════════════════════════════════════
    # Historically known leaders (from prior knowledge)
    # ══════════════════════════════════════════════════════════════════

    # 前任区委书记 — 推测
    {"id": 3, "name": "待确认-前任区委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（待确认去向）", "current_org": "",
     "source": "公开报道未检索到; 崔元锋就任时间待查"},

    # 前任区长 — 推测
    {"id": 4, "name": "待确认-前任区长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "已调离（待确认去向）", "current_org": "",
     "source": "公开报道未检索到"},

    # ══════════════════════════════════════════════════════════════════
    # Other Standing Committee Members (推测)
    # ══════════════════════════════════════════════════════════════════

    # 区委专职副书记 — 待确认
    {"id": 5, "name": "待确认-区委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委副书记（推测）", "current_org": "中共文峰区委",
     "source": "区委常规设有专职副书记; 姓名未公开"},

    # 区纪委书记 — 待确认
    {"id": 6, "name": "待确认-区纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、区纪委书记（推测）", "current_org": "中共文峰区纪委",
     "source": "区委常规设有纪委书记; 姓名未公开"},

    # 区委组织部部长 — 待确认
    {"id": 7, "name": "待确认-区委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、组织部部长（推测）", "current_org": "中共文峰区委组织部",
     "source": "区委常规设有组织部长; 姓名未公开"},

    # 区委宣传部部长 — 待确认
    {"id": 8, "name": "待确认-区委宣传部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、宣传部部长（推测）", "current_org": "中共文峰区委宣传部",
     "source": "区委常规设有宣传部长; 姓名未公开"},

    # 区委政法委书记 — 待确认
    {"id": 9, "name": "待确认-区委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、政法委书记（推测）", "current_org": "中共文峰区委政法委",
     "source": "区委常规设有政法委书记; 姓名未公开"},

    # 常务副区长 — 待确认
    {"id": 10, "name": "待确认-常务副区长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、常务副区长（推测）", "current_org": "文峰区人民政府",
     "source": "区人民政府常规设有常务副区长; 姓名未公开"},

    # 人武部部长/政委 — 待确认
    {"id": 11, "name": "待确认-人武部主官", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、人武部主官（推测）", "current_org": "文峰区人民武装部",
     "source": "区委常规设有人武部主官兼职常委; 姓名未公开"},

    # 区委办主任 — 待确认
    {"id": 12, "name": "待确认-区委办主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "文峰区委常委、区委办公室主任（推测）", "current_org": "中共文峰区委办公室",
     "source": "区委常规设有区委办主任; 姓名未公开"},
]

organizations = [
    {"id": 1, "name": "中共文峰区委", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委", "location": "河南省安阳市文峰区"},
    {"id": 2, "name": "文峰区人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市文峰区"},
    {"id": 3, "name": "中共文峰区纪委", "type": "党委", "level": "县处级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 4, "name": "中共文峰区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 5, "name": "中共文峰区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 6, "name": "中共文峰区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 7, "name": "中共文峰区委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共文峰区委", "location": "河南省安阳市文峰区"},
    {"id": 8, "name": "文峰区人民武装部", "type": "党委", "level": "县处级",
     "parent": "安阳军分区", "location": "河南省安阳市文峰区"},
    {"id": 9, "name": "文峰区人大常委会", "type": "人大", "level": "县处级",
     "parent": "安阳市人大常委会", "location": "河南省安阳市文峰区"},
    {"id": 10, "name": "文峰区政协", "type": "政协", "level": "县处级",
     "parent": "政协安阳市委员会", "location": "河南省安阳市文峰区"},
]

positions = [
    # 崔元锋 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "文峰区委书记", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2024年3月以区委书记身份公开活动确认"},

    # 区长 — 待确认
    {"person_id": 2, "org_id": 2, "title": "文峰区区长", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "文峰区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼任区委副书记"},

    # 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "文峰区委书记（前任）", "start_date": "",
     "end_date": "", "rank": "县处级正职", "note": "姓名待确认; 去向待确认"},

    # 前任区长
    {"person_id": 4, "org_id": 2, "title": "文峰区区长（前任）", "start_date": "",
     "end_date": "", "rank": "县处级正职", "note": "姓名待确认; 去向待确认"},

    # 专职副书记
    {"person_id": 5, "org_id": 1, "title": "文峰区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 纪委书记
    {"person_id": 6, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "文峰区纪委书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 组织部长
    {"person_id": 7, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "文峰区委组织部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 宣传部长
    {"person_id": 8, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "文峰区委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 政法委书记
    {"person_id": 9, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "文峰区委政法委书记", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},

    # 常务副区长
    {"person_id": 10, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "文峰区常务副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 人武部主官
    {"person_id": 11, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "文峰区人武部主官", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "姓名待确认"},

    # 区委办主任
    {"person_id": 12, "org_id": 1, "title": "文峰区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "文峰区委办公室主任", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": "姓名待确认"},
]

relationships = [
    # ── 区委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档", "overlap_org": "中共文峰区委",
     "overlap_period": "当前", "strength": "strong",
     "source": "推测: 区级领导班子常规分工"},

    # ── 区委书记与常委 ──
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与专职副书记", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与纪委书记", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "区委书记与组织部长", "overlap_org": "中共文峰区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设置"},

    # ── 区长与副区长 ──
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "文峰区人民政府",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 政府领导班子常规分工"},

    # ── 继任关系 ──
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "前任区委书记与现任", "overlap_org": "中共文峰区委",
     "overlap_period": "交接期", "strength": "weak",
     "source": "推测: 崔元锋接任前任书记"},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "前任区长与现任", "overlap_org": "文峰区人民政府",
     "overlap_period": "交接期", "strength": "weak",
     "source": "推测: 前任区长已调任（去向待确认）"},
]


def main():
    print("=== Building 文峰区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"Note: Limited web access — many fields are unverified")

    run_build(
        slug="文峰区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Summary
    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")


if __name__ == "__main__":
    main()
