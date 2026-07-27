#!/usr/bin/env python3
"""Build script for 平坝区 (Pingba District, Anshun, Guizhou) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 贵州省
Parent City: 安顺市
Targets: 区委书记 & 区长

Research Notes:
  Primary sources: pingba.gov.cn leadership pages (领导之窗) and news articles.
  All government leader bios confirmed from official 平坝区政府 website.
  Party secretary (王金源) identified from news articles (区委常委会, 区委党的建设工作领导小组).
  
Gaps:
  - 王金源 (区委书记): Full career history / biography not available on open web
  - 全优, 龙翔 (区委副书记): Birth info, career history unknown
  - 夏永忠, 杨慧, 张宇 (区委常委): Full details unknown
  - 汪波 (区人大常委会主任): Birth info unknown
  - 陈先锋 (区政协主席): Birth info unknown
  - Predecessor history: Tang Youlun (唐友伦) was earlier party secretary, needing confirmation
  - Most 副区长 lack full career timelines

Sources:
  - http://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/ (领导之窗)
  - https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260720_90637737.html (区委常委会)
  - https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626468.html (区委理论学习中心组)
  - https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626448.html (区委党的建设工作领导小组)
  - https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626445.html (集中整治工作)
"""

import sqlite3
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "王金源",
        "gender": "男",
        "ethnicity": "",  # Not specified in sources
        "birth": "",  # Unknown - not listed on gov site
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委书记",
        "current_org": "中共安顺市平坝区委员会",
        "source": "Confirmed from multiple news articles on pingba.gov.cn: https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260720_90637737.html; https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626468.html; https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626448.html",
    },
    {
        "id": 2,
        "name": "王元鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",  # Not listed on official bio
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委副书记、区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202502/t20250225_86946192.html (official gov bio)",
    },
    # ── Other District Leaders ──
    {
        "id": 3,
        "name": "汪波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区人大常委会主任",
        "current_org": "平坝区人大常委会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260720_90637737.html (区委常委会 article mentions 汪波 as 区人大常委会主任)",
    },
    {
        "id": 4,
        "name": "陈先锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区政协主席",
        "current_org": "平坝区政协",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260720_90637737.html (区委常委会 article mentions 陈先锋 as 区政协主席)",
    },
    {
        "id": 5,
        "name": "全优",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委副书记",
        "current_org": "中共安顺市平坝区委员会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260720_90637737.html",
    },
    {
        "id": 6,
        "name": "龙翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委副书记",
        "current_org": "中共安顺市平坝区委员会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626468.html",
    },
    # ── District Government Deputy Leaders ──
    {
        "id": 7,
        "name": "李树华",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1986年1月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委常委、常务副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202501/t20250102_86447849.html (official gov bio)",
    },
    {
        "id": 8,
        "name": "罗平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委常委、副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202405/t20240506_84471111.html (official gov bio)",
    },
    {
        "id": 9,
        "name": "黄君",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975年2月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202307/t20230718_81025144.html (official gov bio)",
    },
    {
        "id": 10,
        "name": "王秀勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202406/t20240613_84868749.html (official gov bio)",
    },
    {
        "id": 11,
        "name": "郭萧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202108/t20210811_80529006.html (official gov bio)",
    },
    {
        "id": 12,
        "name": "谢天",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区副区长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202307/t20230718_81025421.html (official gov bio)",
    },
    {
        "id": 13,
        "name": "卢平",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区副区长、市公安局平坝分局局长",
        "current_org": "安顺市平坝区人民政府",
        "source": "https://www.pingba.gov.cn/zwgk/jcxxgk/zfgk/ldzc/202603/t20260311_89628116.html (official gov bio)",
    },
    # ── Other Standing Committee Members (区委常委) ──
    {
        "id": 14,
        "name": "夏永忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委常委",
        "current_org": "中共安顺市平坝区委员会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626445.html (mentioned as 区领导 attending 集中整治工作领导小组会议)",
    },
    {
        "id": 15,
        "name": "杨慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委常委",
        "current_org": "中共安顺市平坝区委员会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626445.html",
    },
    {
        "id": 16,
        "name": "张宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平坝区委常委",
        "current_org": "中共安顺市平坝区委员会",
        "source": "https://www.pingba.gov.cn/xwzx/pbyw/202607/t20260715_90626445.html",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共安顺市平坝区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "贵州省安顺市平坝区",
    },
    {
        "id": 2,
        "name": "安顺市平坝区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "贵州省安顺市平坝区",
    },
    {
        "id": 3,
        "name": "平坝区人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "贵州省安顺市平坝区",
    },
    {
        "id": 4,
        "name": "平坝区政协",
        "type": "政协",
        "level": "县处级",
        "location": "贵州省安顺市平坝区",
    },
    {
        "id": 5,
        "name": "平坝区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "贵州省安顺市平坝区",
    },
]

POSITIONS = [
    # 王金源
    {"person_id": 1, "org_id": 1, "title": "平坝区委书记", "start": "", "end": "", "rank": "正处级", "note": "Current party secretary"},
    # 王元鹏
    {"person_id": 2, "org_id": 1, "title": "平坝区委副书记", "start": "", "end": "", "rank": "副处级", "note": "Also serves as district mayor"},
    {"person_id": 2, "org_id": 2, "title": "平坝区区长", "start": "", "end": "", "rank": "正处级", "note": "Current district mayor"},
    # 汪波
    {"person_id": 3, "org_id": 3, "title": "平坝区人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 陈先锋
    {"person_id": 4, "org_id": 4, "title": "平坝区政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    # 全优
    {"person_id": 5, "org_id": 1, "title": "平坝区委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 龙翔
    {"person_id": 6, "org_id": 1, "title": "平坝区委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 李树华
    {"person_id": 7, "org_id": 1, "title": "平坝区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "平坝区常务副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 罗平
    {"person_id": 8, "org_id": 1, "title": "平坝区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "平坝区副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 黄君
    {"person_id": 9, "org_id": 2, "title": "平坝区副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 王秀勇
    {"person_id": 10, "org_id": 2, "title": "平坝区副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 郭萧
    {"person_id": 11, "org_id": 2, "title": "平坝区副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 谢天
    {"person_id": 12, "org_id": 2, "title": "平坝区副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 卢平
    {"person_id": 13, "org_id": 2, "title": "平坝区副区长、市公安局平坝分局局长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 夏永忠
    {"person_id": 14, "org_id": 1, "title": "平坝区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 杨慧
    {"person_id": 15, "org_id": 1, "title": "平坝区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 张宇
    {"person_id": 16, "org_id": 1, "title": "平坝区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    # Core leadership pair
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档",
        "context": "王金源（区委书记）与王元鹏（区长）为平坝区党政主要负责人",
        "overlap_org": "中共安顺市平坝区委员会/安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    # Party secretary and deputy secretaries
    {
        "person_a": 1, "person_b": 5,
        "type": "上下级",
        "context": "王金源（区委书记）与全优（区委副书记）为直接上下级",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "上下级",
        "context": "王金源（区委书记）与龙翔（区委副书记）为直接上下级",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    # Standing committee members
    {
        "person_a": 1, "person_b": 7,
        "type": "上下级",
        "context": "王金源（区委书记）与李树华（区委常委、常务副区长）",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 14,
        "type": "上下级",
        "context": "王金源（区委书记）与夏永忠（区委常委）",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 15,
        "type": "上下级",
        "context": "王金源（区委书记）与杨慧（区委常委）",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 16,
        "type": "上下级",
        "context": "王金源（区委书记）与张宇（区委常委）",
        "overlap_org": "中共安顺市平坝区委员会",
        "overlap_period": "现任",
    },
    # Eight-person leadership group (mentioned in 集中整治 article)
    {
        "person_a": 1, "person_b": 3,
        "type": "同僚",
        "context": "王金源（区委书记）与汪波（区人大常委会主任）同为区四套班子主要负责人",
        "overlap_org": "平坝区四套班子",
        "overlap_period": "现任",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "同僚",
        "context": "王金源（区委书记）与陈先锋（区政协主席）同为区四套班子主要负责人",
        "overlap_org": "平坝区四套班子",
        "overlap_period": "现任",
    },
    # Government team
    {
        "person_a": 2, "person_b": 7,
        "type": "上下级",
        "context": "王元鹏（区长）与李树华（常务副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "上下级",
        "context": "王元鹏（区长）与罗平（副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "上下级",
        "context": "王元鹏（区长）与黄君（副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "上下级",
        "context": "王元鹏（区长）与王秀勇（副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "上下级",
        "context": "王元鹏（区长）与郭萧（副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "上下级",
        "context": "王元鹏（区长）与谢天（副区长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2, "person_b": 13,
        "type": "上下级",
        "context": "王元鹏（区长）与卢平（副区长、公安分局局长）为政府班子正副职",
        "overlap_org": "安顺市平坝区人民政府",
        "overlap_period": "现任",
    },
]


# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    STAGING = Path(__file__).parent
    DB_PATH = STAGING / "平坝区_network.db"
    GEXF_PATH = STAGING / "平坝区_network.gexf"

    run_build(
        slug="平坝区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("✅ Build complete for 平坝区 (Pingba District)")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Orgs:    {len(ORGANIZATIONS)}")
    print(f"  Pos:     {len(POSITIONS)}")
    print(f"  Rels:    {len(RELATIONSHIPS)}")
