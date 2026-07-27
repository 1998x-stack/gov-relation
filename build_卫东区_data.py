#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 卫东区 (Weidong District, Pingdingshan, Henan) leadership network.

卫东区 — 河南省平顶山市辖区, 平顶山市中心城区之一, 总面积101平方公里,
辖12个街道, 38个社区、24个行政村, 常住人口30.7万.

Data sources:
- 卫东区人民政府门户网站 (www.weidong.gov.cn) — official bio pages and news articles
- 区十次党代会报道 (2026-06-24/25) — new leadership election
- 区政府领导信息页 (updated 2024-05-14) — bio summaries

Confidence notes:
- Current roles: confirmed (official source, as of 2026-07)
- Identity data for 宋建立, 赵飞, 李海强, 张世卿, 王昀灿: confirmed from official biography pages
- Identity data for 孟宪强, 朱晓鹏 and other party committee members: partial (from news mentions)
- Career timelines beyond current role: limited; gaps marked as unverified
"""

import sys
import os
from pathlib import Path

# Add project root to path
BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_卫东区"
DB_PATH = STAGING / "卫东区_network.db"
GEXF_PATH = STAGING / "卫东区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 孟宪强
    {"id": 1, "name": "孟宪强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委书记", "current_org": "中共卫东区委",
     "source": "卫东区十次党代会一次全会报道 (www.weidong.gov.cn, 2026-06-25)"},

    # 区委副书记、区长 宋建立
    {"id": 2, "name": "宋建立", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "",
     "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委副书记、区长", "current_org": "卫东区人民政府",
     "source": "区政府领导信息页 (www.weidong.gov.cn/contents/31112/12220.html)"},

    # ══════════════════════════════════════════════════════════════════
    # Party Committee Leaders
    # ══════════════════════════════════════════════════════════════════

    # 区委副书记 朱晓鹏
    {"id": 3, "name": "朱晓鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委副书记", "current_org": "中共卫东区委",
     "source": "区十次党代会一次全会报道 (2026-06-25)"},

    # 区委常委、组织部部长 李彩霞
    {"id": 4, "name": "李彩霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委、组织部部长", "current_org": "中共卫东区委组织部",
     "source": "区委理论学习中心组报道 (2026-05-29, 06-30)、老干部通报会 (2026-07-17)"},

    # 区委常委、区纪委书记、政法委书记 金武军
    {"id": 5, "name": "金武军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区委理论学习中心组报道、老干部通报会"},

    # ══════════════════════════════════════════════════════════════════
    # Government Leaders (from official bio pages)
    # ══════════════════════════════════════════════════════════════════

    # 区委常委、常务副区长 赵飞
    {"id": 6, "name": "赵飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-09", "birthplace": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委、常务副区长", "current_org": "卫东区人民政府",
     "source": "区政府领导信息页 (www.weidong.gov.cn/contents/31112/15992.html)"},

    # 副区长、卫东公安分局局长 李海强
    {"id": 7, "name": "李海强", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-01", "birthplace": "",
     "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区副区长、公安分局局长", "current_org": "平顶山市公安局卫东分局",
     "source": "区政府领导信息页 (www.weidong.gov.cn/contents/31112/12217.html)"},

    # 副区长 张世卿
    {"id": 8, "name": "张世卿", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "",
     "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区副区长", "current_org": "卫东区人民政府",
     "source": "区政府领导信息页 (www.weidong.gov.cn/contents/31112/12215.html)"},

    # 副区长 王昀灿
    {"id": 9, "name": "王昀灿", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-05", "birthplace": "",
     "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区副区长", "current_org": "卫东区人民政府",
     "source": "区政府领导信息页 (www.weidong.gov.cn/contents/31112/12216.html)"},

    # ══════════════════════════════════════════════════════════════════
    # Other Standing Committee Members (from 党代会执行主席名单)
    # ══════════════════════════════════════════════════════════════════

    # 区委常委 尹小曼
    {"id": 10, "name": "尹小曼", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区十次党代会主席台就座名单 (2026-06-24)"},

    # 区委常委 胡瑞挺
    {"id": 11, "name": "胡瑞挺", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区十次党代会主席台就座名单"},

    # 区委常委 刘彦福
    {"id": 12, "name": "刘彦福", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区十次党代会主席台就座名单"},

    # 区委常委、区纪委书记 王延锋
    {"id": 13, "name": "王延锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委、区纪委书记", "current_org": "中共卫东区纪委",
     "source": "区纪委一次全会报道 (2026-06-25)"},

    # 区委常委 张新蕾
    {"id": 14, "name": "张新蕾", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区委理论学习中心组报道 (2026-06-30)"},

    # 区委常委 马勇
    {"id": 15, "name": "马勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "区委理论学习中心组报道"},

    # 区委常委 丁建民
    {"id": 16, "name": "丁建民", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区委常委", "current_org": "中共卫东区委",
     "source": "光华路街道调研报道 (2026-07-06)"},

    # ══════════════════════════════════════════════════════════════════
    # Other Government Leaders
    # ══════════════════════════════════════════════════════════════════

    # 人大常委会副主任 宋志勇 (mentioned in 区政府第五次全体会议)
    {"id": 17, "name": "宋志勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区人大常委会副主任", "current_org": "卫东区人大常委会",
     "source": "区政府第五次全体会议报道 (2026-07-17)"},

    # 政协副主席 季梅香 (mentioned in 区政府第五次全体会议)
    {"id": 18, "name": "季梅香", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "卫东区政协副主席", "current_org": "卫东区政协",
     "source": "区政府第五次全体会议报道 (2026-07-17)"},

    # 区委领导 陈汶 (mentioned in 走访慰问党员)
    {"id": 19, "name": "陈汶", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "卫东区领导", "current_org": "中共卫东区委",
     "source": "走访慰问党员报道 (2026-06-29)"},

    # ══════════════════════════════════════════════════════════════════
    # Predecessors (partially known)
    # ══════════════════════════════════════════════════════════════════

    # 前任区委书记 (九届区委书记)
    {"id": 20, "name": "前任区委书记（九届）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "已离任", "current_org": "",
     "source": "区十次党代会报道提及九届区委工作报告（姓名待查）"},
]

organizations = [
    {"id": 1, "name": "中共卫东区委", "type": "党委", "level": "县处级",
     "parent": "中共平顶山市委", "location": "河南省平顶山市卫东区"},
    {"id": 2, "name": "卫东区人民政府", "type": "政府", "level": "县处级",
     "parent": "平顶山市人民政府", "location": "河南省平顶山市卫东区"},
    {"id": 3, "name": "中共卫东区纪委", "type": "党委", "level": "县处级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 4, "name": "中共卫东区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 5, "name": "卫东区人大常委会", "type": "人大", "level": "县处级",
     "parent": "平顶山市人大常委会", "location": "河南省平顶山市卫东区"},
    {"id": 6, "name": "卫东区政协", "type": "政协", "level": "县处级",
     "parent": "政协平顶山市委员会", "location": "河南省平顶山市卫东区"},
    {"id": 7, "name": "平顶山市公安局卫东分局", "type": "政府", "level": "乡科级",
     "parent": "平顶山市公安局", "location": "河南省平顶山市卫东区"},
    {"id": 8, "name": "卫东区现代服务业开发区", "type": "开发区", "level": "乡科级",
     "parent": "卫东区人民政府", "location": "河南省平顶山市卫东区"},
]

positions = [
    # 孟宪强
    {"person_id": 1, "org_id": 1, "title": "卫东区委书记", "start": "2026-06",
     "end": "present", "rank": "县处级正职", "note": "2026年6月24日十届一次全会当选"},
    # 宋建立
    {"person_id": 2, "org_id": 2, "title": "卫东区区长", "start": "",
     "end": "present", "rank": "县处级正职", "note": "兼任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "卫东区委副书记", "start": "2026-06",
     "end": "present", "rank": "县处级副职", "note": "十届一次全会当选副书记"},
    # 朱晓鹏
    {"person_id": 3, "org_id": 1, "title": "卫东区委副书记", "start": "2026-06",
     "end": "present", "rank": "县处级副职", "note": "十届一次全会当选副书记"},
    # 李彩霞
    {"person_id": 4, "org_id": 1, "title": "卫东区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "区委组织部部长", "start": "",
     "end": "present", "rank": "乡科级正职", "note": "推测担任(列名在副书记之后、其他常委之前)"},
    # 金武军
    {"person_id": 5, "org_id": 1, "title": "卫东区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    # 赵飞
    {"person_id": 6, "org_id": 2, "title": "卫东区常务副区长", "start": "",
     "end": "present", "rank": "县处级副职", "note": "区委常委、区政府党组副书记"},
    {"person_id": 6, "org_id": 1, "title": "卫东区委常委", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    # 李海强
    {"person_id": 7, "org_id": 7, "title": "卫东公安分局局长", "start": "",
     "end": "present", "rank": "乡科级正职", "note": "二级高级警长"},
    {"person_id": 7, "org_id": 2, "title": "卫东区副区长", "start": "",
     "end": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 张世卿
    {"person_id": 8, "org_id": 2, "title": "卫东区副区长", "start": "",
     "end": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 王昀灿
    {"person_id": 9, "org_id": 2, "title": "卫东区副区长", "start": "",
     "end": "present", "rank": "县处级副职", "note": "区政府党组成员"},
    # 王延锋
    {"person_id": 13, "org_id": 3, "title": "卫东区纪委书记", "start": "2026-06",
     "end": "present", "rank": "县处级副职", "note": "十届区纪委一次全会当选，区委常委"},
    # 宋志勇
    {"person_id": 17, "org_id": 5, "title": "人大常委会副主任", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
    # 季梅香
    {"person_id": 18, "org_id": 6, "title": "政协副主席", "start": "",
     "end": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    # ── 区委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档", "overlap_org": "中共卫东区委",
     "overlap_period": "2026-06至今", "strength": "strong",
     "source": "区十次党代会"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与专职副书记搭档", "overlap_org": "中共卫东区委",
     "overlap_period": "2026-06至今", "strength": "strong",
     "source": "区十次党代会"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区委副书记（均为副书记）", "overlap_org": "中共卫东区委常委会",
     "overlap_period": "2026-06至今", "strength": "medium",
     "source": "区十次党代会"},

    # ── 区委常委之间的工作关系 ──
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "区委书记与纪委书记", "overlap_org": "中共卫东区委常委会",
     "overlap_period": "2026-06至今", "strength": "strong",
     "source": "区纪委一次全会"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "区委书记与常务副区长", "overlap_org": "中共卫东区委常委会",
     "overlap_period": "2026-06至今", "strength": "medium",
     "source": "区十次党代会主席台名单"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与组织部长（干部工作）", "overlap_org": "中共卫东区委常委会",
     "overlap_period": "2026-06至今", "strength": "medium",
     "source": "区委理论学习中心组报道"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与常委（政法或统战）", "overlap_org": "中共卫东区委常委会",
     "overlap_period": "2026-06至今", "strength": "medium",
     "source": "老干部工作通报会报道"},

    # ── 政府班子关系 ──
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与常务副区长（协助分管审计）", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "strong",
     "source": "区政府领导分工页面"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与公安分局局长（副区长）", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "区政府领导分工页面"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "区政府领导分工页面"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "区政府领导分工页面"},

    # ── 常委间的其他关系 ──
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "常务副区长与副区长（均为政府班子成员）", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "medium",
     "source": "区政府领导分工页面"},
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "副区长同事", "overlap_org": "卫东区人民政府",
     "overlap_period": "", "strength": "weak",
     "source": "区政府领导分工页面"},
]


def main():
    print(f"=== Building 卫东区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"Date: {Path(__file__).stat().st_mtime_ns}")

    run_build(
        slug="卫东区",
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
