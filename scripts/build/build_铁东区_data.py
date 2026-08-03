#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 铁东区, 鞍山市, 辽宁省.

Investigation date: 2026-08-03
Task ID: liaoning_铁东区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL WEB ACCESS
  - 铁东区政府网站 (www.tiedong.gov.cn): accessible (HTTP fallback)
  - Exa API: rate-limited
  - Baidu/Baidu Baike: 403
  - Google: redirect block
  - Jina Reader: timeout

Confirmed official sources:
  - 区政府领导页: http://www.tiedong.gov.cn/asstdq/zwgk/zfld/glist.html
  - 区长周锋 page: http://www.tiedong.gov.cn/html/ASTDQ/202507/0175187805424735.html
  - 副区长郑红 page: http://www.tiedong.gov.cn/html/ASTDQ/202310/0169898246020261.html
  - 副区长刘枳江 page: http://www.tiedong.gov.cn/html/ASTDQ/202301/0166590568395321.html
  - 副区长常明 page: http://www.tiedong.gov.cn/html/ASTDQ/202301/0165389789186937.html
  - 副区长马浦元 page: http://www.tiedong.gov.cn/html/ASTDQ/202301/0157770698797513.html
  - 副区长谭富鑫 page: http://www.tiedong.gov.cn/html/ASTDQ/202406/0171756122790869.html
  - 副区长王宇 page: http://www.tiedong.gov.cn/html/ASTDQ/202301/0164032304950271.html
  - 八一节慰问 article: http://www.tiedong.gov.cn/html/ASTD/202607/0178545796654961.html
  - 教育工作会 article: http://www.tiedong.gov.cn/html/ASTD/202607/0178529142945775.html
  - 王士伟宣讲 article: http://www.tiedong.gov.cn/html/ASTD/202512/0176655457483864.html
  - 许家洋宣讲 article: http://www.tiedong.gov.cn/html/ASTD/202512/0176655658050062.html

Confidence notes:
  - 区委书记宗培楠: confirmed via official article (2026-07-28 八一走访慰问)
  - 区长周锋: confirmed via official government leadership page (2026-06-30)
  - All 6 副区长: confirmed via official profiles
  - Party committee leadership (许家洋, 王士伟): confirmed via official articles
  - 人大主任刘峰, 政协主席候选人许家洋: confirmed from 八一 article
  - Career histories for most figures are PARTIAL — no Baidu BiKe access
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "铁东区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_铁东区"
if _CURRENT_DIR.name == "liaoning_铁东区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3-14=other leaders

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # Core Leadership — CONFIRMED from official sources
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "宗培楠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "铁东区委书记",
        "current_org": "中共鞍山市铁东区委员会",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202607/0178545796654961.html",
        "confidence": "confirmed",
        "notes": "铁东区委书记、千山风景名胜区党工委书记。Confirmed from 2026-07-28 八一走访慰问 article. Full biography unavailable due to Baidu Baike 403.",
    },
    {
        "id": 2,
        "name": "周锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "education": "大学学历、管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202507/0175187805424735.html",
        "confidence": "confirmed",
        "notes": "中共铁东区委副书记，区人民政府党组书记、区长，千山风景名胜区党工委副书记、管委会主任. Holds 管理学学士. Officially listed as 区长 on government website since 2026-06-30.",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Deputy Leadership — Government side (confirmed from official pages)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "郑红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202310/0169898246020261.html",
        "confidence": "confirmed",
        "notes": "中共铁东区委常委，区人民政府党组副书记、副区长. Handles executive (常务) responsibilities: development & reform, finance, HR, emergency management, statistics, state assets, petition, inspection, street offices.",
    },
    {
        "id": 4,
        "name": "刘枳江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "研究生学历、工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202301/0166590568395321.html",
        "confidence": "confirmed",
        "notes": "中共铁东区委常委，区人民政府党组成员、副区长. Handles industry, technology, civil affairs, agriculture.",
    },
    {
        "id": 5,
        "name": "常明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202301/0165389789186937.html",
        "confidence": "confirmed",
        "notes": "区政府党组成员、副区长，公安铁东分局局长. Handles public security, justice, social stability, social governance. Older member born 1971.",
    },
    {
        "id": 6,
        "name": "马浦元",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1982年8月",
        "birthplace": "",
        "education": "大学学历、经济学学士",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202301/0157770698797513.html",
        "confidence": "confirmed",
        "notes": "Non-CCP member (民盟). Handles education, health, veterans affairs, medical security, culture, tourism, and broadcast. 满族 ethnicity.",
    },
    {
        "id": 7,
        "name": "谭富鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202406/0171756122790869.html",
        "confidence": "confirmed",
        "notes": "区政府党组成员、副区长. Handles commerce, market supervision, food/drug safety, business environment, administrative approval, investment promotion.",
    },
    {
        "id": 8,
        "name": "王宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁东区人民政府",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202301/0164032304950271.html",
        "confidence": "confirmed",
        "notes": "区政府党组成员、副区长. Handles housing & urban construction, land resources, comprehensive law enforcement, environment protection, land transfer.",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Party Leadership (confirmed from news articles)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "许家洋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共铁东区委员会",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202512/0176655658050062.html",
        "confidence": "confirmed",
        "notes": "铁东区委副书记 (since at least Dec 2025). Also listed as 政协党组书记、主席候选人 in 八一 article (2026-07-28), suggesting transition to 政协主席 role.",
    },
    {
        "id": 10,
        "name": "王士伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记",
        "current_org": "中共铁东区纪律检查委员会",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202512/0176655457483864.html",
        "confidence": "confirmed",
        "notes": "铁东区委常委、纪委书记、区监察委员会主任. Mentioned in 2025-12宣讲article about 20th Fourth Plenary Session.",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # NPC & CPPCC Leadership
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "刘峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "铁东区人大常委会",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202607/0178545796654961.html",
        "confidence": "confirmed",
        "notes": "Mentioned in 八一 article (2026-07-28) participating in visit to military units.",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Other Identified District Leaders (roles not fully confirmed)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "赵伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "铁东区",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202607/0178545796654961.html",
        "confidence": "plausible",
        "notes": "Mentioned in the 八一 article as 区领导. Role/rank not specified.",
    },
    {
        "id": 13,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "铁东区",
        "source": "http://www.tiedong.gov.cn/html/ASTDQ/202607/0178545796654961.html",
        "confidence": "plausible",
        "notes": "Mentioned in 八一 article as 区领导. Specific role not specified.",
    },
    {
        "id": 14,
        "name": "崔岩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "铁东区",
        "source": "http://www.tiedong.gov.cn/html/ASTD/202607/0178529142945775.html",
        "confidence": "plausible",
        "notes": "Mentioned as attending education work meeting in 2026-07.",
    },
    {
        "id": 15,
        "name": "陈振宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "铁东区",
        "source": "http://www.tiedong.gov.cn/html/ASTD/202607/0178529142945775.html",
        "confidence": "plausible",
        "notes": "Mentioned as attending education work meeting in 2026-07. Likely 副区长 or 区委常委.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共鞍山市铁东区委员会", "type": "党委", "level": "县区级", "parent": "鞍山市", "location": "鞍山市铁东区"},
    {"id": 2, "name": "铁东区人民政府", "type": "政府", "level": "县区级", "parent": "鞍山市", "location": "鞍山市铁东区"},
    {"id": 3, "name": "中共铁东区纪律检查委员会", "type": "党委", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 4, "name": "铁东区人大常委会", "type": "人大", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 5, "name": "铁东区政协", "type": "政协", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 6, "name": "公安铁东分局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 7, "name": "千山风景名胜区", "type": "事业单位", "level": "地市级", "parent": "鞍山市", "location": "鞍山市千山区"},
    {"id": 8, "name": "铁东区人民政府办公室", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 9, "name": "铁东区发展和改革局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 10, "name": "铁东区财政局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 11, "name": "铁东区教育局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 12, "name": "铁东区审计局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
    {"id": 13, "name": "铁东区应急管理局", "type": "政府", "level": "县区级", "parent": "铁东区", "location": "鞍山市铁东区"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════

positions = [
    # 宗培楠 (1)
    {"person_id": 1, "org_id": 1, "title": "铁东区委书记", "start": "", "end": "present", "rank": "正处级", "note": "Also serves as 千山风景票区党工委书记"},
    {"person_id": 1, "org_id": 7, "title": "千山风景名胜区党工委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 周锋 (2)
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "中共铁东区委副书记，区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "千山风景名胜区党工委副书记、管委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 郑红 (3)
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "区委常委，区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘枳江 (4)
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区委常委，区政府党组成员"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 常明 (5)
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 5, "org_id": 6, "title": "公安铁东分局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 马浦元 (6)
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "民盟盟员"},
    # 谭富鑫 (7)
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员"},
    # 王宇 (8)
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "区政府党组成员"},
    # 许家洋 (9)
    {"person_id": 9, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": "Also 政协党组书记、主席候选人"},
    {"person_id": 9, "org_id": 5, "title": "政协党组书记、主席候选人", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 王士伟 (10)
    {"person_id": 10, "org_id": 3, "title": "区纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘峰 (11)
    {"person_id": 11, "org_id": 4, "title": "区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 赵伟 (12)
    {"person_id": 12, "org_id": 1, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "Role not specified in source"},
    # 王勇 (13)
    {"person_id": 13, "org_id": 1, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "Role not specified"},
    # 崔岩 (14)
    {"person_id": 14, "org_id": 1, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "Likely 区委常委 or 副区长"},
    # 陈振宇 (15)
    {"person_id": 15, "org_id": 1, "title": "区领导", "start": "", "end": "present", "rank": "", "note": "Likely 区委常委 or 副区长"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记(宗培楠)和区长(周鋒)配搭", "overlap_org": "铁东区", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委副书记(许家洋)", "overlap_org": "铁东区", "overlap_period": "2025-"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与纪委书记(王士伟)", "overlap_org": "铁东区", "overlap_period": "2025-"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长(郑红)", "overlap_org": "铁东区政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为区委常委、副区长", "overlap_org": "铁东区", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "区委常委同事", "overlap_org": "铁东区", "overlap_period": ""},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "区委常委同事", "overlap_org": "铁东区", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationship: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    person_json_configs = [
        {"id": 1, "name": "宗培楠", "job": "区委书记"},
        {"id": 2, "name": "周锋", "job": "区长"},
        {"id": 9, "name": "许家洋", "job": "区委副书记"},
        {"id": 10, "name": "王士伟", "job": "纪委书记"},
        {"id": 11, "name": "刘峰", "job": "人大常委会主任"},
    ]

    for cfg in person_json_configs:
        pid = cfg["id"]
        person_data = persons[pid - 1]
        pjson = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "鞍山市",
                "region": "铁东区",
                "job": cfg["job"],
                "task_id": "liaoning_铁东区",
                "time_focus": "2026",
            },
            "identity": {
                "name": person_data["name"],
                "gender": person_data["gender"],
                "ethnicity": person_data["ethnicity"],
                "birth": person_data["birth"],
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": person_data["education"] if person_data["education"] else "",
                        "study_type": "unknown",
                        "source_ids": ["S001"],
                    }
                ],
                "party_join": person_data["party_join"],
                "work_start": person_data["work_start"],
            },
            "current_status": {
                "current_post": person_data["current_post"],
                "current_org": person_data["current_org"],
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": person_data["confidence"] == "confirmed",
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "",
                    "end": "present",
                    "org": person_data["current_org"],
                    "title": person_data["current_post"],
                    "notes": "Currently serving. Career history before current role is unknown (Baidu Baike 403, other search engines blocked).",
                    "confidence": person_data["confidence"],
                    "source_ids": ["S001"],
                }
            ],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "career_pattern": "unknown",
            },
            "risk_and_integrity_signals": [],
            "source_register": [
                {
                    "id": "S001",
                    "url": person_data["source"],
                    "publisher": "鞍山市铁东区人民政府",
                    "published_at": AS_OF,
                    "accessed_at": AS_OF,
                    "reliability": "high",
                    "notes": "Official government website leadership page",
                }
            ],
            "confidence_summary": {
                "identity": person_data["confidence"],
                "career_completeness": "thin",
                "biggest_gap": f"{person_data['name']}的完整履历、出生地、学历详情、入党时间和工作时间均缺失，因不可访问Baidu百科和搜索引擎",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{person_data['name']}之前的完整任职履历是什么？",
                    "why_it_matters": "建立该干部的晋升轨迹和跨区交流网络",
                    "suggested_queries": [f"{person_data['name']} 简历", f"{person_data['name']} 任前公示", f"{person_data['name']} 百度百科"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": f"{person_data['name']}的出生地/籍贯在哪里？",
                    "why_it_matters": "识别同乡关系网络",
                    "suggested_queries": [f"{person_data['name']} 出生"],
                    "last_attempted": AS_OF,
                },
            ],
        }
        pjson_path = PJSON_DIR / f"{TODAY}-辽宁省-鞍山市-{cfg['job']}-{cfg['name']}.json"
        with open(pjson_path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {pjson_path}")

    print(f"\nDone. Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {PJSON_DIR}")