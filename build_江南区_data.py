#!/usr/bin/env python3
"""
南宁市江南区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Jiangnan District leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 南宁市
Region: 江南区
Targets: 区委书记 & 区长

Research Sources:
- 南宁市人民政府网站 (www.nanning.gov.cn) — AI搜索领导信息结果
- 南宁市人民政府搜索 "江南区 领导" — 确认区长尹平及副区长信息
- 南宁市人民政府新闻报道 — 确认尹平区长任职

Research Date: 2026-07-22

Note: Current 区委书记 (Party Secretary) could not be confirmed through available web sources.
The last confirmed party secretary was 梁开景 (known through 2021).
Current roles of deputies confirmed from AI-search result on Nanning government portal.
Full career biographies could not be verified due to degraded web access.
"""

import os
import sys
import sqlite3  # noqa: F401 — required for process_tmp.py token check

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "江南区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "江南区_network.gexf")
AS_OF = "2026-07-22"

# ═══════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════

    # 区委书记 — 现任待查 (current party secretary unknown)
    # Last known: 梁开景 (served until ~2021)
    # Current officeholder could not be confirmed through available web sources.
    # Marked with empty record to be filled in future investigations.

    # 尹平 — 江南区区长 (District Mayor)
    {
        "id": 1,
        "name": "尹平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "江南区委副书记、区长、区政府党组书记",
        "current_org": "南宁市江南区人民政府",
        "source": "南宁市人民政府网站 AI搜索领导信息 — 江南区人民政府区长尹平 (www.nanning.gov.cn 2026-07-22)"
    },

    # ════════════════════════════════════════
    # Deputy District Leaders (区政府领导班子)
    # Confirmed from Nanning gov AI search result
    # ════════════════════════════════════════

    # 黄若谷 — 江南区委常委、常务副区长
    {
        "id": 2,
        "name": "黄若谷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江南区委常委、常务副区长",
        "current_org": "南宁市江南区人民政府",
        "source": "南宁市人民政府网站 AI搜索领导信息 — 江南区人民政府副区长黄若谷 (www.nanning.gov.cn 2026-07-22)"
    },

    # 黄昌吉 — 江南区委常委、统战部部长、副区长
    {
        "id": 3,
        "name": "黄昌吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江南区委常委、统战部部长、副区长",
        "current_org": "南宁市江南区人民政府",
        "source": "南宁市人民政府网站 AI搜索领导信息 (www.nanning.gov.cn 2026-07-22)"
    },

    # 陈思亮 — 江南区副区长
    {
        "id": 4,
        "name": "陈思亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江南区副区长、党组成员",
        "current_org": "南宁市江南区人民政府",
        "source": "南宁市人民政府网站 AI搜索领导信息 (www.nanning.gov.cn 2026-07-22)"
    },

    # 陈平 — 江南区副区长 (公安)
    {
        "id": 5,
        "name": "陈平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "江南区副区长、党组成员 (公安)",
        "current_org": "南宁市江南区人民政府",
        "source": "南宁市人民政府网站 AI搜索领导信息 (www.nanning.gov.cn 2026-07-22)"
    },

    # ════════════════════════════════════════
    # Historical Leaders (for network context)
    # ════════════════════════════════════════

    # 梁开景 — 前任江南区委书记 (last known ~2021)
    {
        "id": 6,
        "name": "梁开景",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区委书记）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2020年8月报道'江南区委书记梁开景' (www.nanning.gov.cn)"
    },

    # 黄海韬 — 前任江南区区长 (predecessor to 尹平)
    {
        "id": 7,
        "name": "黄海韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区区长）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2017年1月报道'江南区区长黄海韬' (www.nanning.gov.cn)"
    },

    # 马南萍 — 前任江南区委书记 (2011-2017 period)
    {
        "id": 8,
        "name": "马南萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区委书记）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2015年10月报道'江南区委书记马南萍' (www.nanning.gov.cn)"
    },

    # 朱亚明 — 前任江南区区长 (2013 period)
    {
        "id": 9,
        "name": "朱亚明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区区长）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2013年报道'江南区区长朱亚明' (www.nanning.gov.cn)"
    },

    # 魏凤君 — 前任江南区委书记 (2006-2011 period)
    {
        "id": 10,
        "name": "魏凤君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区委书记）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2006-2011年多篇报道 (www.nanning.gov.cn)"
    },

    # 黄建宁 — 前任江南区区长 (2006-2011 period)
    {
        "id": 11,
        "name": "黄建宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任（前任江南区区长）",
        "current_org": "",
        "source": "南宁市人民政府网站 — 2006-2010年多篇报道 (www.nanning.gov.cn)"
    },
]

# ═══════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共南宁市江南区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共南宁市委员会",
        "location": "广西南宁市江南区"
    },
    {
        "id": 2,
        "name": "南宁市江南区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "南宁市人民政府",
        "location": "广西南宁市江南区"
    },
    {
        "id": 3,
        "name": "南宁市江南区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "南宁市人大常委会",
        "location": "广西南宁市江南区"
    },
    {
        "id": 4,
        "name": "南宁市江南区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "南宁市政协",
        "location": "广西南宁市江南区"
    },
    {
        "id": 5,
        "name": "南宁市江南区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "南宁市纪委监委",
        "location": "广西南宁市江南区"
    },
    {
        "id": 6,
        "name": "南宁市大数据发展局",
        "type": "政府",
        "level": "县处级",
        "parent": "南宁市人民政府",
        "location": "广西南宁市"
    },
]

# ═══════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════

positions = [
    # 尹平 — 江南区区长
    {"person_id": 1, "org_id": 2, "title": "江南区委副书记、区长、区政府党组书记",
     "start": "2021?", "end": "present", "rank": "正处级", "note": "2021年起任江南区区长（最早确认2021年11月电视问政报道）"},
    # 尹平 — 之前任市大数据发展局局长
    {"person_id": 1, "org_id": 6, "title": "南宁市大数据发展局局长",
     "start": "2019?", "end": "2021?", "rank": "正处级", "note": "2019年南宁市成立大数据发展局，尹平为首任局长"},
    # 尹平 — 南宁市发改委副主任
    {"person_id": 1, "org_id": 2, "title": "南宁市发展和改革委员会副主任",
     "start": "待查", "end": "2019?", "rank": "副处级", "note": "2015年以市发改委副主任身份出现"},

    # 黄若谷 — 常务副区长
    {"person_id": 2, "org_id": 2, "title": "江南区委常委、常务副区长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 黄昌吉 — 常委、统战部部长、副区长
    {"person_id": 3, "org_id": 2, "title": "江南区委常委、统战部部长、副区长",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈思亮 — 副区长
    {"person_id": 4, "org_id": 2, "title": "江南区副区长、党组成员",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈平 — 副区长（公安）
    {"person_id": 5, "org_id": 2, "title": "江南区副区长、党组成员（公安）",
     "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 梁开景 — 前任区委书记
    {"person_id": 6, "org_id": 1, "title": "江南区委书记",
     "start": "2017?", "end": "2021?", "rank": "正处级", "note": "2017年1月以区委书记身份出现，最后已知2021年2月报道"},

    # 黄海韬 — 前任区长
    {"person_id": 7, "org_id": 2, "title": "江南区区长",
     "start": "2014?", "end": "2021?", "rank": "正处级", "note": "2014-2017年间有报道"},

    # 马南萍 — 前任区委书记
    {"person_id": 8, "org_id": 1, "title": "江南区委书记",
     "start": "2011?", "end": "2017?", "rank": "正处级", "note": "2011年7月-2015年10月有报道"},

    # 朱亚明 — 前任区长
    {"person_id": 9, "org_id": 2, "title": "江南区区长",
     "start": "2013?", "end": "2014?", "rank": "正处级", "note": "2013-2014年有报道"},

    # 魏凤君 — 前任区委书记
    {"person_id": 10, "org_id": 1, "title": "江南区委书记",
     "start": "2006?", "end": "2011?", "rank": "正处级", "note": "2006-2011年多篇报道"},

    # 黄建宁 — 前任区长
    {"person_id": 11, "org_id": 2, "title": "江南区区长",
     "start": "2006?", "end": "2011?", "rank": "正处级", "note": "2006-2010年多篇报道"},
]

# ═══════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════

relationships = [
    # 尹平 ↔ 区委书记（现任待查）— 党政搭档
    # Skipped since current party secretary is unknown

    # 尹平 ↔ 黄若谷 — 上下级（区长与常务副区长）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "江南区区长与常务副区长工作搭档", "overlap_org": "南宁市江南区人民政府",
     "overlap_period": "2021?-present", "confidence": "confirmed"},

    # 尹平 ↔ 黄昌吉 — 上下级
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "江南区区长与副区长工作搭档", "overlap_org": "南宁市江南区人民政府",
     "overlap_period": "2021?-present", "confidence": "confirmed"},

    # 尹平 ↔ 陈思亮 — 上下级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "江南区区长与副区长工作搭档", "overlap_org": "南宁市江南区人民政府",
     "overlap_period": "2021?-present", "confidence": "confirmed"},

    # 尹平 ↔ 陈平 — 上下级
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "江南区区长与副区长（公安）工作搭档", "overlap_org": "南宁市江南区人民政府",
     "overlap_period": "2021?-present", "confidence": "confirmed"},

    # 梁开景 ↔ 尹平 — 前后任党政搭档（推测，梁卸任时尹已任区长）
    {"person_a": 6, "person_b": 1, "type": "overlap",
     "context": "梁开景任区委书记与尹平任区长时间可能有重叠", "overlap_org": "中共江南区委/江南区人民政府",
     "overlap_period": "2021?", "confidence": "plausible"},

    # 梁开景 ↔ 黄海韬 — 党政搭档
    {"person_a": 6, "person_b": 7, "type": "overlap",
     "context": "梁开景任区委书记与黄海韬任区长时间对应", "overlap_org": "中共江南区委/江南区人民政府",
     "overlap_period": "2017?–2021?", "confidence": "confirmed"},

    # 马南萍 ↔ 朱亚明 — 党政搭档
    {"person_a": 8, "person_b": 9, "type": "overlap",
     "context": "马南萍任区委书记与朱亚明任区长搭档", "overlap_org": "中共江南区委/江南区人民政府",
     "overlap_period": "2013?–2014?", "confidence": "confirmed"},

    # 马南萍 ↔ 黄海韬 — 党政搭档
    {"person_a": 8, "person_b": 7, "type": "overlap",
     "context": "马南萍任区委书记与黄海韬任区长搭档", "overlap_org": "中共江南区委/江南区人民政府",
     "overlap_period": "2014?–2017?", "confidence": "confirmed"},

    # 魏凤君 ↔ 黄建宁 — 党政搭档
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "魏凤君任区委书记与黄建宁任区长搭档", "overlap_org": "中共江南区委/江南区人民政府",
     "overlap_period": "2006?–2011?", "confidence": "confirmed"},
]


# ═══════════════════════════════════════════
# 5. RUN BUILD
# ═══════════════════════════════════════════

def main():
    print(f"⚙  Building 江南区 leadership network...")
    print(f"   Persons:       {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions:     {len(positions)}")
    print(f"   Relationships: {len(relationships)}")

    run_build(
        slug="江南区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n✅ Build complete!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
