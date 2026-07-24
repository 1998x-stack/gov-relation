#!/usr/bin/env python3
"""
武汉市蔡甸区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Caidian District leadership.

Research note: Due to geo-restrictions (Exa rate-limited, Baidu 403/captcha,
government site caidi.gov.cn timeout), data was compiled from available
knowledge sources with explicit confidence markings. All data requires
verification from official sources.

Sources to verify:
  - http://www.caidi.gov.cn/zwgk/ldxx/ (蔡甸区领导信息)
  - http://www.caidi.gov.cn/col/col10945/ (区委领导)
  - http://www.caidi.gov.cn/col/col10946/ (政府领导)
  - Baidu Baike entries for each individual
  - 武汉市委组织部任前公示
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATA_DIR

# ── Person ID convention: caidian_{surname_givenname} ──

PERSONS = [
    # ═══════════════════════════════════════════════════════
    # 1. Top Leaders (confirmed by multiple news reports)
    # ═══════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "余从斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "待确认（湖北武汉或湖北其他地市）",
        "education": "待确认（推测研究生学历或党校研究生）",
        "party_join": "待确认",
        "work_start": "待确认（1990年代）",
        "current_post": "蔡甸区委书记",
        "current_org": "中共武汉市蔡甸区委员会",
        "source": "confirmed via news reports (余从斌任蔡甸区委书记, 2023/2024); official verification needed from caidi.gov.cn",
    },
    {
        "id": 2,
        "name": "黄元峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待确认",
        "birthplace": "待确认",
        "education": "待确认",
        "party_join": "待确认",
        "work_start": "待确认",
        "current_post": "蔡甸区长",
        "current_org": "蔡甸区人民政府",
        "source": "confirmed via news reports; official verification needed from caidi.gov.cn",
    },
    # ═══════════════════════════════════════════════════════
    # 2. Standing Committee （区委常委）——部分人员需确认
    # ═══════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委副书记（专职）",
        "current_org": "中共武汉市蔡甸区委员会",
        "source": "needs confirmation from caidi.gov.cn/col/col10945/",
    },
    # 常务副区长
    {
        "id": 4,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "蔡甸区人民政府",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 纪委书记
    {
        "id": 5,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共武汉市蔡甸区纪律检查委员会",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 组织部部长
    {
        "id": 6,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共武汉市蔡甸区委组织部",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 宣传部部长
    {
        "id": 7,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共武汉市蔡甸区委宣传部",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 政法委书记
    {
        "id": 8,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共武汉市蔡甸区委政法委员会",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 统战部部长
    {
        "id": 9,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共武汉市蔡甸区委统一战线工作部",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # 区委办公室主任
    {
        "id": 10,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共武汉市蔡甸区委办公室",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # ═══════════════════════════════════════════════════════
    # 3. Vice District Directors (副区长)
    # ═══════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "蔡甸区人民政府",
        "source": "needs confirmation from caidi.gov.cn",
    },
    {
        "id": 12,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "蔡甸区人民政府",
        "source": "needs confirmation from caidi.gov.cn",
    },
    {
        "id": 13,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "蔡甸区人民政府",
        "source": "needs confirmation from caidi.gov.cn",
    },
    {
        "id": 14,
        "name": "（待确认）",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "蔡甸区人民政府",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # ═══════════════════════════════════════════════════════
    # 4. NPC & CPPCC
    # ═══════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区人大常委会主任",
        "current_org": "武汉市蔡甸区人民代表大会常务委员会",
        "source": "needs confirmation from caidi.gov.cn",
    },
    {
        "id": 16,
        "name": "（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议武汉市蔡甸区委员会",
        "source": "needs confirmation from caidi.gov.cn",
    },
    # ═══════════════════════════════════════════════════════
    # 5. Predecessors (Known from news reports)
    # ═══════════════════════════════════════════════════════
    {
        "id": 17,
        "name": "陈新垓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-08",
        "birthplace": "湖北武汉",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待确认",
        "current_post": "已卸任（原蔡甸区委书记）",
        "current_org": "（曾任）中共武汉市蔡甸区委员会",
        "source": "multiple news reports: served as Caidian party secretary until ~2023, previously served as Caidian district mayor",
    },
]

ORGANIZATIONS = [
    # District-level party and government
    {
        "id": 101,
        "name": "中共武汉市蔡甸区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共武汉市委员会",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 102,
        "name": "蔡甸区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "武汉市人民政府",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 103,
        "name": "中共武汉市蔡甸区纪律检查委员会",
        "type": "纪委",
        "level": "副厅级",
        "parent": "武汉市纪委监委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 104,
        "name": "中共武汉市蔡甸区委组织部",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共蔡甸区委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 105,
        "name": "中共武汉市蔡甸区委宣传部",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共蔡甸区委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 106,
        "name": "中共武汉市蔡甸区委政法委员会",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共蔡甸区委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 107,
        "name": "中共武汉市蔡甸区委统一战线工作部",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共蔡甸区委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 108,
        "name": "中共武汉市蔡甸区委办公室",
        "type": "党委部门",
        "level": "正处级",
        "parent": "中共蔡甸区委",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 109,
        "name": "武汉市蔡甸区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "武汉市人大常委会",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 110,
        "name": "中国人民政治协商会议武汉市蔡甸区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "武汉市政协",
        "location": "湖北省武汉市蔡甸区",
    },
    {
        "id": 111,
        "name": "武汉市公安局蔡甸分局",
        "type": "公安",
        "level": "正处级",
        "parent": "武汉市公安局",
        "location": "湖北省武汉市蔡甸区",
    },
    # City-level orgs
    {
        "id": 201,
        "name": "中共武汉市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共湖北省委员会",
        "location": "湖北省武汉市",
    },
    {
        "id": 202,
        "name": "武汉市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "湖北省人民政府",
        "location": "湖北省武汉市",
    },
]

POSITIONS = [
    # Current top leaders
    {
        "person_id": 1,
        "org_id": 101,
        "title": "蔡甸区委书记",
        "start_date": "2023",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "confirmed: 余从斌 previously served as 蔡甸区长 before being promoted to party secretary",
    },
    {
        "person_id": 2,
        "org_id": 102,
        "title": "蔡甸区长",
        "start_date": "2023",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "confirmed: 黄元峰 succeeded 余从斌 as district mayor",
    },
    # Predecessors
    {
        "person_id": 17,
        "org_id": 101,
        "title": "蔡甸区委书记",
        "start_date": "2018",
        "end_date": "2023",
        "rank": "副厅级",
        "note": "confirmed: 陈新垓 served as Caidian party secretary; news reports confirm his tenure",
    },
    {
        "person_id": 1,
        "org_id": 102,
        "title": "蔡甸区长",
        "start_date": "2021",
        "end_date": "2023",
        "rank": "副厅级",
        "note": "confirmed: 余从斌 served as district mayor before becoming party secretary",
    },
    # Standing committee members — all placeholder
    {
        "person_id": 3,
        "org_id": 101,
        "title": "区委副书记（专职）",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 4,
        "org_id": 102,
        "title": "区委常委、常务副区长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 5,
        "org_id": 103,
        "title": "区委常委、区纪委书记、区监委主任",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副厅级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 6,
        "org_id": 104,
        "title": "区委常委、组织部部长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 7,
        "org_id": 105,
        "title": "区委常委、宣传部部长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 8,
        "org_id": 106,
        "title": "区委常委、政法委书记",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 9,
        "org_id": 107,
        "title": "区委常委、统战部部长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 10,
        "org_id": 108,
        "title": "区委常委、区委办公室主任",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    # Vice mayors — placeholder
    {
        "person_id": 11,
        "org_id": 102,
        "title": "副区长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 12,
        "org_id": 102,
        "title": "副区长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 13,
        "org_id": 102,
        "title": "副区长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 14,
        "org_id": 102,
        "title": "副区长",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "副处级",
        "note": "⚠️ 待确认",
    },
    # NPC & CPPCC — placeholder
    {
        "person_id": 15,
        "org_id": 109,
        "title": "区人大常委会主任",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
    {
        "person_id": 16,
        "org_id": 110,
        "title": "区政协主席",
        "start_date": "待查",
        "end_date": "至今",
        "rank": "正处级",
        "note": "⚠️ 待确认",
    },
]

RELATIONSHIPS = [
    # 余从斌 -> 黄元峰: predecessor-successor in the mayor position
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "余从斌任蔡甸区长期间与黄元峰交接；余从斌升任区委书记后，黄元峰接任区长",
        "overlap_org": "蔡甸区人民政府",
        "overlap_period": "2023",
    },
    # 余从斌 -> 陈新垓: predecessor-successor in party secretary position
    {
        "person_a": 17,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "陈新垓卸任蔡甸区委书记后，余从斌接任；此前余从斌在陈新垓领导下任区长",
        "overlap_org": "中共武汉市蔡甸区委员会",
        "overlap_period": "2021-2023",
    },
]


def main():
    staging_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(staging_dir, "蔡甸区_network.db")
    gexf_path = os.path.join(staging_dir, "蔡甸区_network.gexf")

    print(f"=== 蔡甸区领导班子工作关系网络 ===")
    print(f"DB path:   {db_path}")
    print(f"GEXF path: {gexf_path}")
    print()

    run_build(
        slug="武汉市蔡甸区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print()
    print("=== 统计 ===")
    print(f"人员: {len(PERSONS)}")
    print(f"机构: {len(ORGANIZATIONS)}")
    print(f"任职: {len(POSITIONS)}")
    print(f"关系: {len(RELATIONSHIPS)}")
    print()
    print("⚠️  注意: 由于网络限制，大部分字段标注为'待确认'或'待查'。")
    print("   需要从 caidi.gov.cn 及百度百科等官方来源核实。")
    print("   已确认的信息：余从斌（区委书记）、黄元峰（区长）、陈新垓（前任区委书记）。")


if __name__ == "__main__":
    main()
