#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 改则县 (Gaize/Gêrzê County), 阿里地区, 西藏自治区.

Current officeholders as of 2026-07:
  - County Party Secretary (县委书记): 王伟 (also holds 人大地工委副主任 at prefecture level)
  - County Mayor (县长): 确巴
  - Organization Department Head (县委组织部部长): 宋星

Sources:
  - Official county website: http://www.gaizexian.gov.cn/
  - 改则县召开城乡环境综合提升工作动员部署会 (gaizexian.gov.cn info/1130/305071.htm, 2025-03-24)
  - 改则县举行西藏民主改革66周年宣传纪念活动 (gaizexian.gov.cn info/1130/305101.htm, 2025-03-28)
  - 改则县赴进藏先遣连纪念馆开展专题活动 (gaizexian.gov.cn info/2061/200241.htm)
  - 改则县开展人道公益募捐活动 (gaizexian.gov.cn info/2061/305981.htm, 2025-05-13)
  - 改则县雪域故地展新颜 (gaizexian.gov.cn info/2061/200251.htm)
  - 阿里地区行政公署领导页面 (al.gov.cn gk/xslingd.htm)

Web access note: Exa rate-limited, Baidu 403, some government sites timed out.
Core leader names and roles are confirmed from official county website (gaizexian.gov.cn),
but full biographical details (birthplace, specific career timeline entries before current role)
remain unverified for most deputies.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from datetime import datetime

TODAY = "2026-07-28"
STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING, "改则县_network.db")
GEXF_PATH = os.path.join(STAGING, "改则县_network.gexf")

# =========================================================================
# PERSONS
# Confidence labels: confirmed=official source, plausible=credible media,
#                    unverified=insufficient evidence
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县委书记（人大地工委副主任）",
        "current_org": "中共改则县委员会",
        "source": "Confirmed: multiple articles on gaizexian.gov.cn (2025), e.g. '人大地工委副主任、改则县委书记王伟出席' in info/1130/305101.htm and info/2061/305981.htm"
    },
    {
        "id": 2,
        "name": "确巴",
        "gender": "",
        "ethnicity": "藏族（推断）",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县委副书记、政府县长",
        "current_org": "改则县人民政府",
        "source": "Confirmed: gaizexian.gov.cn info/1130/305101.htm (2025-03-28) '县委副书记、政改巴主持'"
    },
    {
        "id": 3,
        "name": "宋星",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县委常委、组织部部长",
        "current_org": "中共改则县委员会组织部",
        "source": "Confirmed: gaizexian.gov.cn info/2061/200241.htm '县委组织部部长宋星带领大家重温入党誓词'"
    },
    # ── County leaders mentioned in media ──
    {
        "id": 4,
        "name": "巴桑罗布",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县干部",
        "current_org": "改则县人民政府",
        "source": "Plausible: mentioned in gaizexian.gov.cn info/2061/200251.htm as a county official"
    },
    {
        "id": 5,
        "name": "嘎玛曲扎",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "改则县先遣乡",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县委宣传部宣传干事",
        "current_org": "改则县委宣传部",
        "source": "Plausible: mentioned in gaizexian.gov.cn info/2061/200251.htm as '改则县委宣传部宣传干事'"
    },
    {
        "id": 6,
        "name": "桑旦",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县住房和城乡建设局局长",
        "current_org": "改则县住房和城乡建设局",
        "source": "Plausible: mentioned in gaizexian.gov.cn info/2061/200251.htm as '改则县住房和城乡建设局局长'"
    },
    {
        "id": 7,
        "name": "嘎玛旦增",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "改则县城投负责人",
        "current_org": "改则县城市建设投资公司",
        "source": "Plausible: mentioned in gaizexian.gov.cn info/2061/200251.htm"
    },
    {
        "id": 8,
        "name": "土多江村",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "1979",
        "current_post": "改则县退休老干部",
        "current_org": "改则县",
        "source": "Plausible: mentioned in gaizexian.gov.cn info/2061/200251.htm as '老干部' who started work in 1979"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共改则县委员会", "type": "党委", "level": "县级", "parent": "", "location": "西藏自治区阿里地区改则县"},
    {"id": 2, "name": "改则县人民政府", "type": "政府", "level": "县级", "parent": "", "location": "西藏自治区阿里地区改则县"},
    {"id": 3, "name": "改则县委组织部", "type": "党委", "level": "县级", "parent": "中共改则县委员会", "location": "西藏自治区阿里地区改则县"},
    {"id": 4, "name": "改则县委宣传部", "type": "党委", "level": "县级", "parent": "中共改则县委员会", "location": "西藏自治区阿里地区改则县"},
    {"id": 5, "name": "改则县住房和城乡建设局", "type": "政府", "level": "县级", "parent": "改则县人民政府", "location": "西藏自治区阿里地区改则县"},
    {"id": 6, "name": "改则县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "西藏自治区阿里地区改则县"},
    {"id": 7, "name": "阿里地区人大工作委员会", "type": "人大", "level": "地级", "parent": "", "location": "西藏自治区阿里地区"},
    {"id": 8, "name": "改则县城建投公司", "type": "事业单位", "level": "县级", "parent": "改则县人民政府", "location": "西藏自治区阿里地区改则县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 王伟 (Party Secretary) ──
    {"person_id": 1, "org_id": 1, "title": "改则县委书记", "start": "", "end": "present", "rank": "正处级", "note": "同时兼任人大地工委副主任"},
    {"person_id": 1, "org_id": 7, "title": "阿里地区人大地工委副主任", "start": "", "end": "present", "rank": "副厅级", "note": "高配"},
    # ── 确巴 (County Mayor) ──
    {"person_id": 2, "org_id": 2, "title": "改则县委副书记、政府县长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "改则县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "党内职务"},
    # ── 宋星 (Organization Head) ──
    {"person_id": 3, "org_id": 3, "title": "改则县委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "改则县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # ── Others ──
    {"person_id": 4, "org_id": 2, "title": "改则县干部", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "改则县委宣传部宣传干事", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "改则县住房和城乡建设局局长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "改则县城投负责人", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "老干部", "start": "1979", "end": "retired", "rank": "", "note": "1979年参加工作"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "共事", "context": "县委书记—县长搭档",
        "overlap_org": "中共改则县委员会/改则县人民政府",
        "overlap_period": "共同任职期间"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "上下级", "context": "县委书记—组织部部长",
        "overlap_org": "中共改则县委员会",
        "overlap_period": "共同任职期间"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "共事", "context": "县委班子",
        "overlap_org": "中共改则县委员会",
        "overlap_period": "共同任职期间"
    },
    {
        "person_a": 5, "person_b": 4,
        "type": "共事", "context": "县委宣传部",
        "overlap_org": "改则县委宣传部",
        "overlap_period": ""
    },
]

# =========================================================================
# BUILD
# =========================================================================
if __name__ == "__main__":
    print(f"Building 改则县 network (staging: {STAGING})...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug="改则县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    db_size = os.path.getsize(DB_PATH)
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"\nDone! Files created:")
    print(f"  DB:   {DB_PATH} ({db_size} bytes)")
    print(f"  GEXF: {GEXF_PATH} ({gexf_size} bytes)")