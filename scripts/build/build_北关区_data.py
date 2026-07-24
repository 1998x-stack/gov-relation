#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 北关区 (Beiguan District, Anyang, Henan) leadership network.

北关区 — 河南省安阳市辖区, 安阳市中心城区之一, 总面积59平方公里,
辖9个街道、1个镇, 常住人口约32万.

Data sources:
- 北关区人民政府门户网站 (www.beiguan.gov.cn) — official bio pages and news articles
- 北关区政府领导之窗 (updated 2025-11-04) — 区长及副区长简历
- 北关区新闻动态 (2026) — 区委书记元浩公开活动报道
- 区委常委、常务副区长金波简历页 (updated 2026-05-15)
- 副区长王建军、刘振清简历页 (updated 2026-05-15)

Confidence notes:
- 区委书记元浩: confirmed (homepage news, 2026-03-25)
- 区长可振虎: confirmed (official bio page, 2025-11-04)
- 副区长简历: confirmed from official bio pages
- 区委常委会成员: partial (from official leadership info - 金波、秦瑞光 confirmed as 区委常委)
- Career timelines beyond current role: limited; gaps marked as unverified
"""

import sys
import os
import sqlite3  # noqa - used via gov_relation.runner
from pathlib import Path

# Add project root to path
BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────

STAGING = BASE / "data/tmp/henan_北关区"
DB_PATH = STAGING / "北关区_network.db"
GEXF_PATH = STAGING / "北关区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders (Targets)
    # ══════════════════════════════════════════════════════════════════

    # 区委书记 元浩
    {"id": 1, "name": "元浩", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委书记", "current_org": "中共北关区委",
     "source": "北关区人民政府门户网站新闻 (www.beiguan.gov.cn, 2026-03-25会见河南大学一行)"},

    # 区委副书记、区长 可振虎
    {"id": 2, "name": "可振虎", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1986-03", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委副书记、区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623155.html)"},

    # ══════════════════════════════════════════════════════════════════
    # Party Committee Leaders (confirmed as 区委常委)
    # ══════════════════════════════════════════════════════════════════

    # 区委常委、常务副区长 金波
    {"id": 3, "name": "金波", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委常委、常务副区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2026/05-15/3644565.html)"},

    # 区委常委、宣传部部长、副区长 秦瑞光
    {"id": 4, "name": "秦瑞光", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-07", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委常委、宣传部部长、副区长", "current_org": "中共北关区委宣传部",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623156.html)"},

    # ══════════════════════════════════════════════════════════════════
    # Government Leaders
    # ══════════════════════════════════════════════════════════════════

    # 副区长、北关公安分局局长 户彬
    {"id": 5, "name": "户彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-12", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区副区长、公安分局局长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623154.html)"},

    # 副区长 李鑫
    {"id": 6, "name": "李鑫", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区副区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623157.html)"},

    # 副区长 王春庆
    {"id": 7, "name": "王春庆", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-12", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区副区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623159.html)"},

    # 副区长 王建军
    {"id": 8, "name": "王建军", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区副区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2025/11-04/3623158.html)"},

    # 副区长 刘振清
    {"id": 9, "name": "刘振清", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-11", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区副区长", "current_org": "北关区人民政府",
     "source": "北关区政府领导之窗 (www.beiguan.gov.cn/2026/05-15/3644565.html)"},

    # ══════════════════════════════════════════════════════════════════
    # Other Party Committee Standing Committee Members (推测/待确认)
    # ══════════════════════════════════════════════════════════════════

    # 区委副书记（专职）— 待确认姓名
    {"id": 10, "name": "待确认-区委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委副书记（推测）", "current_org": "中共北关区委",
     "source": "区委领导分工未公开; 推测存在专职副书记一职"},

    # 区纪委书记 — 待确认姓名
    {"id": 11, "name": "待确认-区纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委常委、区纪委书记（推测）", "current_org": "中共北关区纪委",
     "source": "区委领导分工未公开; 推测存在纪委书记一职"},

    # 区委组织部部长 — 待确认姓名
    {"id": 12, "name": "待确认-区委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委常委、组织部部长（推测）", "current_org": "中共北关区委组织部",
     "source": "区委领导分工未公开; 推测存在组织部长一职"},

    # 区委政法委书记 — 待确认姓名
    {"id": 13, "name": "待确认-区委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "北关区委常委、政法委书记（推测）", "current_org": "中共北关区委政法委",
     "source": "区委领导分工未公开; 推测存在政法委书记一职"},
]

organizations = [
    {"id": 1, "name": "中共北关区委", "type": "党委", "level": "县处级",
     "parent": "中共安阳市委", "location": "河南省安阳市北关区"},
    {"id": 2, "name": "北关区人民政府", "type": "政府", "level": "县处级",
     "parent": "安阳市人民政府", "location": "河南省安阳市北关区"},
    {"id": 3, "name": "中共北关区纪委", "type": "党委", "level": "县处级",
     "parent": "中共北关区委", "location": "河南省安阳市北关区"},
    {"id": 4, "name": "中共北关区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共北关区委", "location": "河南省安阳市北关区"},
    {"id": 5, "name": "中共北关区委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共北关区委", "location": "河南省安阳市北关区"},
    {"id": 6, "name": "中共北关区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共北关区委", "location": "河南省安阳市北关区"},
    {"id": 7, "name": "北关区人大常委会", "type": "人大", "level": "县处级",
     "parent": "安阳市人大常委会", "location": "河南省安阳市北关区"},
    {"id": 8, "name": "北关区政协", "type": "政协", "level": "县处级",
     "parent": "政协安阳市委员会", "location": "河南省安阳市北关区"},
    {"id": 9, "name": "安阳市公安局北关分局", "type": "政府", "level": "乡科级",
     "parent": "安阳市公安局", "location": "河南省安阳市北关区"},
    {"id": 10, "name": "北关区中原高新技术产业开发区", "type": "开发区", "level": "乡科级",
     "parent": "北关区人民政府", "location": "河南省安阳市北关区"},
]

positions = [
    # 元浩 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "北关区委书记", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "2026年3月以区委书记身份公开活动确认"},

    # 可振虎 — 区长
    {"person_id": 2, "org_id": 2, "title": "北关区区长", "start_date": "",
     "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "北关区委副书记", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "兼任区委副书记"},

    # 金波
    {"person_id": 3, "org_id": 1, "title": "北关区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "北关区常务副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责区政府常务工作"},

    # 秦瑞光
    {"person_id": 4, "org_id": 1, "title": "北关区委常委", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "北关区委宣传部部长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": ""},

    # 户彬
    {"person_id": 5, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法、信访等"},
    {"person_id": 5, "org_id": 9, "title": "北关公安分局局长", "start_date": "",
     "end_date": "present", "rank": "乡科级正职", "note": ""},

    # 李鑫
    {"person_id": 6, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责民政、卫健、医保等"},

    # 王春庆
    {"person_id": 7, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责工业、商务、市场监管等"},

    # 王建军
    {"person_id": 8, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责教育、农业农村、乡村振兴等"},

    # 刘振清
    {"person_id": 9, "org_id": 2, "title": "北关区副区长", "start_date": "",
     "end_date": "present", "rank": "县处级副职", "note": "负责科技等工作"},
]

relationships = [
    # ── 区委班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长搭档", "overlap_org": "中共北关区委",
     "overlap_period": "当前", "strength": "strong",
     "source": "北关区人民政府门户网站"},

    # ── 区委常委之间的工作关系 ──
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与常务副区长（区委常委）", "overlap_org": "中共北关区委常委会",
     "overlap_period": "当前", "strength": "strong",
     "source": "北关区政府领导页面"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与宣传部部长（区委常委）", "overlap_org": "中共北关区委常委会",
     "overlap_period": "当前", "strength": "strong",
     "source": "北关区政府领导页面"},

    # ── 政府班子关系 ──
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与常务副区长（协助分管审计）", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "strong",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长（宣传部长）", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与公安分局局长（副区长）", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},

    # ── 副区长之间的同事关系 ──
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "常务副区长与副区长（政府班子成员）", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "常务副区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 3, "person_b": 7, "type": "overlap",
     "context": "常务副区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 3, "person_b": 8, "type": "overlap",
     "context": "常务副区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 3, "person_b": 9, "type": "overlap",
     "context": "常务副区长与副区长", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "medium",
     "source": "北关区政府领导分工页面"},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "副区长（宣传部长）与副区长（协助文旅工作）", "overlap_org": "北关区人民政府",
     "overlap_period": "当前", "strength": "weak",
     "source": "领导分工显示李鑫协助秦瑞光分管文旅工作"},

    # ── 区委常委间的推测关系 ──
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "区委书记与专职副书记（推测搭档）", "overlap_org": "中共北关区委",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设有专职副书记"},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "区委书记与纪委书记（推测）", "overlap_org": "中共北关区委常委会",
     "overlap_period": "当前", "strength": "weak",
     "source": "推测: 区委常规设有纪委书记"},
]


def main():
    print(f"=== Building 北关区 network data ===")
    print(f"Target: 区委书记 & 区长")
    print(f"Date: {Path(__file__).stat().st_mtime_ns}")

    run_build(
        slug="北关区",
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
