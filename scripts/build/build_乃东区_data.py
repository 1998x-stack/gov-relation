#!/usr/bin/env python3
"""
乃东区（山南市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Nêdong District (Nedong District) leadership.

Research sources:
  - http://www.naidong.gov.cn (乃东区人民政府官网)
  - 乃东区第三次代表大会新闻 (2026-07-03)
  - 乃东区两会党员大会新闻 (2026-07-07)
  - 全面从严治党暨党风廉政建设专题会议 (2026-07-22)
  - 周平主持召开三届区人民政府第1次常务会议 (2026-07-24)
  - 乃东区"两优一先"表彰大会 (2026-06-30)

Confidence: Core leadership confirmed via multiple official sources (2026-07).
Other deputy positions inferred from standard county-level committee structure.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乃东区"
# Canonical paths
DB_PATH = DATABASE_DIR / "乃东区_network.db"
GEXF_PATH = GRAPH_DIR / "乃东区_network.gexf"

# ── DATA ─────────────────────────────────────────────────────────────

# Person ID convention: naidong_{surname_givenname}

persons = [
    # ═══ Current Top Leaders ═══
    # 布多 (Bu Duo) — Party Secretary, confirmed 市委常委、区委书记
    {"id": 1, "name": "布多", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、区委书记", "current_org": "中共山南市乃东区委员会",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202607/t20260703_172577.html"},

    # 周平 (Zhou Ping) — District Mayor, confirmed 区委副书记、区长
    {"id": 2, "name": "周平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长", "current_org": "乃东区人民政府",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202607/t20260724_173932.html"},

    # ═══ Key Deputy Leaders (confirmed from news) ═══
    # 王波 (Wang Bo) — 区委常务副书记、常务副区长
    {"id": 3, "name": "王波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常务副书记、常务副区长", "current_org": "中共山南市乃东区委员会/乃东区人民政府",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202606/t20260630_172205.html"},

    # 侯树彬 (Hou Shubin) — 区委副书记
    {"id": 4, "name": "侯树彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共山南市乃东区委员会",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202606/t20260630_172205.html"},

    # 罗廷坤 (Luo Tingkun) — 市监委委员、区纪委书记、监委主任
    {"id": 5, "name": "罗廷坤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市监委委员、区纪委书记、监委主任", "current_org": "中共山南市乃东区纪律检查委员会/乃东区监察委员会",
     "source": "http://www.naidong.gov.cn/xwzx/ndyw/202607/t20260722_173825.html"},

    # ═══ Standard Standing Committee Positions (推断 - plausible) ═══
    # 组织部部长
    {"id": 6, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "中共山南市乃东区委组织部",
     "source": "⚠️ 待确认 - 标准岗位"},

    # 宣传部部长
    {"id": 7, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区委常委、宣传部部长", "current_org": "中共山南市乃东区委宣传部",
     "source": "⚠️ 待确认 - 标准岗位"},

    # 政法委书记
    {"id": 8, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区委常委、政法委书记", "current_org": "中共山南市乃东区委政法委员会",
     "source": "⚠️ 待确认 - 标准岗位"},

    # 统战部部长
    {"id": 9, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区委常委、统战部部长", "current_org": "中共山南市乃东区委统一战线工作部",
     "source": "⚠️ 待确认 - 标准岗位"},

    # 人武部部长/政委
    {"id": 10, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区委常委、人武部政委（或部长）", "current_org": "山南市乃东区人民武装部",
     "source": "⚠️ 待确认 - 标准岗位"},

    # ═══ People's Congress & CPPCC ═══
    {"id": 11, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "山南市乃东区人民代表大会常务委员会",
     "source": "⚠️ 待确认 - 第二届人大常委会已公布第三届人大名单"},

    {"id": 12, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "区政协主席", "current_org": "中国人民政治协商会议山南市乃东区委员会",
     "source": "⚠️ 待确认 - 标准岗位"},

    # ═══ Shannan City Level Leaders 山南市 ═══
    # 山南市委书记 (from shannan.gov.cn news - 2026-07 leadership activities)
    {"id": 13, "name": "李富忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "山南市委书记", "current_org": "中共山南市委员会",
     "source": "https//www.shannan.gov.cn (2026-07 领导活动)"},

    {"id": 14, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "山南市委副书记、市长", "current_org": "山南市人民政府",
     "source": "⚠️ 待确认"},
]

organizations = [
    # District-level party committee
    {"id": 1, "name": "中共山南市乃东区委员会", "type": "党委", "level": "县处级",
     "parent": "中共山南市委员会", "location": "西藏自治区山南市乃东区"},

    # District government
    {"id": 2, "name": "乃东区人民政府", "type": "政府", "level_pair": "县处级",
     "parent": "山南市人民政府", "location": "西藏自治区山南市乃东区"},

    # Discipline inspection
    {"id": 3, "name": "中共山南市乃东区纪律检查委员会/乃东区监察委员会", "type": "纪委",
     "level": "县处级", "parent": "山南市纪委监委", "location": "西藏自治区山南市乃东区"},

    # Party departments
    {"id": 4, "name": "中共山南市乃东区委组织部", "type": "党委部门", "level": "乡科级",
     "parent": "中共乃东区委员会", "location": "西藏自治区山南市乃东区"},
    {"id": 5, "name": "中共山南市乃东区委宣传部", "type": "党委部门", "level": "乡科级",
     "parent": "中共乃东区委员会", "location": "西藏自治区山南市乃东区"},
    {"id": 6, "name": "中共山南市乃东区委政法委员会", "type": "党委部门", "level": "乡科级",
     "parent": "中共乃东区委员会", "location": "西藏自治区山南市乃东区"},
    {"id": 7, "name": "中共山南市乃东区委统一战线工作部", "type": "党委部门", "level": "乡科级",
     "parent": "中共乃东区委员会", "location": "西藏自治区山南市乃东区"},
    {"id": 8, "name": "山南市乃东区人民武装部", "type": "军队", "level": "县处级",
     "parent": "山南军分区", "location": "西藏自治区山南市乃东区"},

    # NPC and CPPCC
    {"id": 9, "name": "山南市乃东区人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "山南市人大常委会", "location": "西藏自治区山南市乃东区"},
    {"id": 10, "name": "中国人民政治协商会议山南市乃东区委员会", "type": "政协",
     "level": "县处级", "parent": "山南市政协", "location": "西藏自治区山南市乃东区"},

    # City-level organizations
    {"id": 11, "name": "中共山南市委员会", "type": "党委", "level": "地市级",
     "parent": "中共西藏自治区委员会", "location": "西藏自治区山南市"},
    {"id": 12, "name": "山南市人民政府", "type": "政府", "level": "地市级",
     "parent": "西藏自治区人民政府", "location": "西藏自治区山南市"},
]

positions = [
    # ── Current confirmed positions ──
    # 布多: 市委常委、区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "至今",
     "rank": "县处级正职", "note": "同时兼任山南市委常委，confirmed 2026-07"},
    # 布多 – 山南市委常委
    {"person_id": 1, "org_id": 11, "title": "市委常委", "start_date": "", "end_date": "至今",
     "rank": "地市级副职", "note": "confirmed 2026-07"},

    # 周平 – 区委副书记、区长
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "confirmed 2026-07"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "至今",
     "rank": "县处级正职", "note": "confirmed 2026-07"},

    # 王波 – 区委常务副书记、常务副区长
    {"person_id": 3, "org_id": 1, "title": "区委常务副书记", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "confirmed 2026-06 via 两优一先表彰大会"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "confirmed 2026-06"},

    # 侯树彬 – 区委副书记
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "confirmed 2026-06 via 乃东区两优一先表彰大会"},

    # 罗廷坤 – 区纪委书记、监委主任
    {"person_id": 5, "org_id": 3, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "confirmed 2026-07 via 全面从严治党会议"},
    {"person_id": 5, "org_id": 11, "title": "市监委委员", "start_date": "", "end_date": "至今",
     "rank": "地市级副职", "note": "confirmed 2026-07"},

    # ── Standing Committee (standard positions — names unknown) ──
    {"person_id": 6, "org_id": 4, "title": "区委常委、组织部部长", "start_date": "", "end_date": "至今",
     "rank": "乡科级正职", "note": "⚠️ 待确认具体姓名"},
    {"person_id": 7, "org_id": 5, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "至今",
     "rank": "乡科级正职", "note": "⚠️ 待确认具体姓名"},
    {"person_id": 8, "org_id": 6, "title": "区委常委、政法委书记", "start_date": "", "end_date": "至今",
     "rank": "县处级副职", "note": "⚠️ 待确认具体姓名"},
    {"person_id": 9, "org_id": 7, "title": "区委常委、统战部部长", "start_date": "", "end_date": "至今",
     "rank": "乡科级正职", "note": "⚠️ 待确认具体姓名"},
    {"person_id": 10, "org_id": 8, "title": "区委常委、人武部部长/政委", "start_date": "", "end_date": "至今",
     "rank": "县处级正职", "note": "⚠️ 待确认具体姓名"},

    # 人大/政协
    {"person_id": 11, "org_id": 9, "title": "区人大常委会主任", "start_date": "", "end_date": "至今",
     "rank": "县处级正职", "note": "⚠️ 待确认具体姓名"},
    {"person_id": 12, "org_id": 10, "title": "区政协主席", "start_date": "", "end_date": "至今",
     "rank": "县处级正职", "note": "⚠️ 待确认具体姓名"},

    # 山南市领导 – 李富忠 (市委书记)
    {"person_id": 13, "org_id": 11, "title": "山南市委书记", "start_date": "", "end_date": "至今",
     "rank": "地市级正职", "note": "confirmed from shannan.gov.cn 2026-07 leader activities"},
]

relationships = [
    # ── Core team: Confirmed working relationships ──
    {"person_a": 1, "person_b": 2, "type": "工作关系",
     "context": "布多（区委书记）与周平（区长）为乃东区党政一把手搭档",
     "overlap_org": "中共山南市乃东区委员会/乃东区人民政府",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "工作关系",
     "context": "布多（区委书记）与王波（区委常务副书记）在区委常委会班子共事",
     "overlap_org": "中共山南市乃东区委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "工作关系",
     "context": "布多（区委书记）与侯树彬（区委副书记）在区委常委会班子共事",
     "overlap_org": "中共山南市乃东区委员会",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "工作关系",
     "context": "周平（区长）与王波（常务副区长）分别为区政府一、二把手",
     "overlap_org": "乃东区人民政府",
     "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "工作关系",
     "context": "周平与侯树彬在区委常委会共事",
     "overlap_org": "中共山南市乃东区委员会",
     "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "工作关系",
     "context": "布多（区委书记）主持召开从严治党会议，罗廷坤（区纪委书记）汇报工作",
     "overlap_org": "中共山南市乃东区委员会/区纪委监委",
     "overlap_period": "2026"},
    {"person_a": 3, "person_b": 4, "type": "工作关系",
     "context": "王波（常务副书记）与侯树彬（副书记）在区委班子共事",
     "overlap_org": "中共山南市乃东区委员会",
     "overlap_period": "2026"},
]

# ── Prompts for individuals ⚠️ 待确认 ──────────────────────────────
# The following persons are standard positions with names pending:
# - ID 6: 组织部部长 (发改委/七里河区 部长)
# - ID 7: 宣传部部长
# - ID 8: 政法委书记
# - ID 9: 统战部关部长
# - ID 10: 人武部部长/政委
# - ID 11: 人大常委会主任
# - ID 12: 政协主席
# - ID 14: 山南市长


if __name__ == "__main__":
    print("=" * 60)
    print("  山南市乃东区领导班子工作关系网络 — 数据构建")
    print("  Confirmed through official naidong.gov.cn (2026-07)")
    print("=" * 60)

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n📊 Summary ({SLUG}):")
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    for table in ["persons", "organizations", "positions", "relationships"]:
        cnt = conn.cursor().execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()

    print(f"\n✅ Generated files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")