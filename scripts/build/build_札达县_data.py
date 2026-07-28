#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 札达县 (Zanda County), 阿里地区, 西藏自治区.

Current officeholders as of 2026-07:
  - Party Secretary (县委书记): 陈代均 (confirmed from 2026-07 news articles)
  - County Mayor (县长): 扎西旺堆 (confirmed from official leadership page, zhada.gov.cn)
  - Deputy Secretary & Executive Vice Mayor: 王子超 (县委常务副书记、常务副县长)
  - Executive Vice Mayor: 董小勇 (县委常委、政府常务副县长)

Sources:
  - http://www.zhada.gov.cn/zfxxgk/ldzc.htm (official leadership page)
  - Individual leader profiles at http://www.zhada.gov.cn/info/1031/*.htm
  - News items on zhada.gov.cn confirming 陈代均 as Party Secretary

Web access note: Exa rate-limited, Baidu 403. Core leader names are confirmed from
official county website (zhada.gov.cn), but full biographical details (birthplace,
specific career timeline entries before current role) remain unverified for most
deputies.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-28"
STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING, "札达县_network.db")
GEXF_PATH = os.path.join(STAGING, "札达县_network.gexf")

# =========================================================================
# PERSONS
# Confidence labels: confirmed=official source, plausible=credible media,
#                    unverified=insufficient evidence
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "陈代均",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "札达县委书记",
        "current_org": "中共札达县委员会",
        "source": "Confirmed: multiple news articles on zhada.gov.cn (2026-07), e.g. '陈代均前往县民政和退役军人事务局督导调研' (2026-07-10)"
    },
    {
        "id": 2,
        "name": "扎西旺堆",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县委副书记、政府县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: official leadership page zhada.gov.cn/info/1031/109301.htm (2026-07-21 update)"
    },
    {
        "id": 3,
        "name": "王子超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "在职硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县委常务副书记、常务副县长",
        "current_org": "中共札达县委员会",
        "source": "Confirmed: zhada.gov.cn/info/1031/102911.htm (2026-01-16 update)"
    },
    {
        "id": 4,
        "name": "董小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县委常委、政府常务副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/77781.htm (2020-04-27 update)"
    },
    {
        "id": 5,
        "name": "曹文海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县委常委、政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/102651.htm (2026-01-14 update)"
    },
    {
        "id": 6,
        "name": "朱贤卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/109371.htm (2026-07-21 update)"
    },
    {
        "id": 7,
        "name": "周秀飞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1993年6月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/109341.htm (2026-07-21 update)"
    },
    {
        "id": 8,
        "name": "旦增索朗",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/109321.htm (2026-07-21 update)"
    },
    {
        "id": 9,
        "name": "伦珠",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "硕士学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/102661.htm (2026-01-16 update)"
    },
    {
        "id": 10,
        "name": "邓高祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年12月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/102641.htm (2026-01-14 update)"
    },
    {
        "id": 11,
        "name": "洛桑罗布",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1986年3月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "札达县政府副县长",
        "current_org": "札达县人民政府",
        "source": "Confirmed: zhada.gov.cn/info/1031/102631.htm (2026-01-14 update)"
    },
    # ── Predecessors (partial info) ──
    {
        "id": 12,
        "name": "巴桑罗布",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Unverified: mentioned in zhada.gov.cn news '巴桑罗布深入实地开展巡视整改回头看' (2026-06-13). Role uncertain."
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共札达县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共阿里地区委员会",
        "location": "西藏自治区阿里地区札达县"
    },
    {
        "id": 2,
        "name": "札达县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "阿里地区行政公署",
        "location": "西藏自治区阿里地区札达县"
    },
    {
        "id": 3,
        "name": "札达县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "阿里地区人大工委",
        "location": "西藏自治区阿里地区札达县"
    },
    {
        "id": 4,
        "name": "札达县政协",
        "type": "政协",
        "level": "县",
        "parent": "阿里地区政协",
        "location": "西藏自治区阿里地区札达县"
    },
    {
        "id": 5,
        "name": "札达县纪委监委",
        "type": "纪委",
        "level": "县",
        "parent": "阿里地区纪委监委",
        "location": "西藏自治区阿里地区札达县"
    },
]

# =========================================================================
# POSITIONS (Career timeline / current roles)
# =========================================================================
positions = [
    # 陈代均 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "札达县委书记", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed active in 2026-07 news"},
    # 扎西旺堆 - County Mayor
    {"person_id": 2, "org_id": 2, "title": "札达县委副书记、政府县长", "start": "", "end": "present", "rank": "正县级", "note": "Confirmed as of 2026-07-21"},
    # 王子超 - Deputy Secretary & Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "札达县委常务副书记", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "札达县常务副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 董小勇 - Executive Deputy Mayor
    {"person_id": 4, "org_id": 1, "title": "札达县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "札达县政府常务副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 曹文海 - Deputy Mayor
    {"person_id": 5, "org_id": 1, "title": "札达县委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "札达县政府副县长", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Top leadership team member overlaps
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭档",
        "overlap_org": "札达县",
        "overlap_period": "present",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记—常务副书记",
        "overlap_org": "中共札达县委员会",
        "overlap_period": "present",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记—县委常委/常务副县长",
        "overlap_org": "札达县",
        "overlap_period": "present",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记—县委常委",
        "overlap_org": "中共札达县委员会",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长—常务副县长",
        "overlap_org": "札达县人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长—常务副县长",
        "overlap_org": "札达县人民政府",
        "overlap_period": "present",
    },
    # Team members working together in the county government
    {"person_a": 2, "person_b": 6,  "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7,  "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8,  "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9,  "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    # Colleague deputies
    {"person_a": 6, "person_b": 7,  "type": "overlap", "context": "县政府副县长同事", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 6, "person_b": 8,  "type": "overlap", "context": "县政府副县长同事", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 7, "person_b": 8,  "type": "overlap", "context": "县政府副县长同事", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "县政府副县长同事", "overlap_org": "札达县人民政府", "overlap_period": "present"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "县政府副县长同事", "overlap_org": "札达县人民政府", "overlap_period": "present"},
]

# =========================================================================
# BUILD
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="札达县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Summary
    print(f"\nDone. Artifacts in staging ({STAGING}):")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # Database size
    db_size = os.path.getsize(DB_PATH)
    print(f"  DB size: {db_size:,} bytes")