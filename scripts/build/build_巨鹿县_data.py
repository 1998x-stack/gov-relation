#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巨鹿县 leadership network.

Level: 县
Province: 河北省
Parent city: 邢台市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_巨鹿县

Research date: 2026-07-23
Official site: https://www.julu.gov.cn/

Current status (as of 2026-07-23):
- 县委书记: 杨振东 — confirmed from multiple official news articles (2025-2026)
- 县长: 李精虎 (县委副书记、县长) — confirmed from official news (2026-02-24)
- 常务副县长: 曹世恒 (confirmed, profile at /content/52275.html)
- 副县长: 龙赛, 王立辉, 李兵, 田建强 (confirmed, profiles at /channelList/11047.html)
- 县委常委、纪委书记: 王彦彬 (confirmed from 县纪委全会 article)
- Other county leaders mentioned: 李玲, 赵洪义, 张丽景, 宋光华, 樊抗, 林晨, 王刚

Notes:
- 县委书记杨振东: Active since at least 2025; leads county party committee;
  focuses on industrial cluster development (高端装备关键零部件制造), urban renewal,
  air pollution control, e-commerce livestreaming promotion.
- 县长李精虎: Serves concurrently as 县委副书记; focuses on government administration,
  air pollution control alongside the party secretary.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "巨鹿县"
TASK_ID = "hebei_巨鹿县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-07-23"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 县领导 Core Leaders ──
    {
        "id": 1,
        "name": "杨振东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委书记",
        "current_org": "中共巨鹿县委员会",
        "source": "巨鹿县人民政府官网 — 领导活动及政府会议 (2026-04-14 /content/66795.html, 2026-07-09 /content/67713.html)",
    },
    {
        "id": 2,
        "name": "李精虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — '杨振东李精虎实地督导检查大气污染防治工作' (2026-02-24 /content/66363.html); '县纪委十二届六次全会' (2026-02-14 /content/66340.html)",
    },

    # ── 副县长 Deputy County Mayors ──
    # Source: julu.gov.cn/channelList/11047.html — 政府领导页面
    {
        "id": 11,
        "name": "曹世恒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府常务副县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — 常务副县长简历 (2025-06-24 /content/52275.html)",
    },
    {
        "id": 12,
        "name": "龙赛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府副县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — 副县长简历 (2024-07-01 /content/52273.html)",
    },
    {
        "id": 13,
        "name": "王立辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府副县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — 副县长简历 (2024-07-01 /content/41244.html)",
    },
    {
        "id": 14,
        "name": "李兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府副县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — 副县长简历 (2024-07-01 /content/41243.html)",
    },
    {
        "id": 15,
        "name": "田建强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "巨鹿县人民政府副县长",
        "current_org": "巨鹿县人民政府",
        "source": "巨鹿县人民政府官网 — 副县长简历 (2024-07-01 /content/52363.html)",
    },

    # ── 县委常委 Other County Party Committee Leaders ──
    # Source: 县纪委十二届六次全会 article (2026-02-14 /content/66340.html)
    {
        "id": 21,
        "name": "王彦彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委常委、县纪委书记、县监委主任",
        "current_org": "中共巨鹿县纪律检查委员会",
        "source": "巨鹿县人民政府官网 — 县纪委十二届六次全会 (2026-02-14 /content/66340.html)",
    },
    {
        "id": 22,
        "name": "宋光华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委常委",
        "current_org": "中共巨鹿县委员会",
        "source": "巨鹿县人民政府官网 — 杨振东督导检查城市更新工作 (2026-03-27 /content/66641.html); 杨振东深入项目企业一线 (2026-04-14 /content/66795.html)",
    },
    {
        "id": 23,
        "name": "樊抗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委常委",
        "current_org": "中共巨鹿县委员会",
        "source": "巨鹿县人民政府官网 — multiple articles (2026-02-24 /content/66363.html, 2026-04-14 /content/66795.html)",
    },
    {
        "id": 24,
        "name": "林晨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委常委",
        "current_org": "中共巨鹿县委员会",
        "source": "巨鹿县人民政府官网 — 杨振东带队到邯郸市考察学习 (2026-04-30 /content/66917.html)",
    },
    {
        "id": 25,
        "name": "王刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共巨鹿县委常委",
        "current_org": "中共巨鹿县委员会",
        "source": "巨鹿县人民政府官网 — multiple articles (2026-03-27 /content/66641.html, 2026-04-30 /content/66917.html, 2026-05-21 /content/67099.html)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共巨鹿县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共邢台市委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 2,
        "name": "巨鹿县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "邢台市人民政府",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 3,
        "name": "巨鹿县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "邢台市人大常委会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 4,
        "name": "政协巨鹿县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协邢台市委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 5,
        "name": "中共巨鹿县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共巨鹿县委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 6,
        "name": "中共巨鹿县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共巨鹿县委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 7,
        "name": "中共巨鹿县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共巨鹿县委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 8,
        "name": "中共巨鹿县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共巨鹿县委员会",
        "location": "河北省邢台市巨鹿县",
    },
    {
        "id": 9,
        "name": "中共巨鹿县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共巨鹿县委员会",
        "location": "河北省邢台市巨鹿县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leaders
    {"person_id": 1, "org_id": 1, "title": "中共巨鹿县委书记",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "至少自2025年起担任县委书记；2026年7月仍在任"},
    {"person_id": 2, "org_id": 2, "title": "巨鹿县人民政府县长",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "同时担任中共巨鹿县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共巨鹿县委副书记",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "县委副书记、县长一肩挑"},

    # Deputy County Mayors
    {"person_id": 11, "org_id": 2, "title": "巨鹿县人民政府常务副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2025-06-24"},
    {"person_id": 12, "org_id": 2, "title": "巨鹿县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2024-07-01"},
    {"person_id": 13, "org_id": 2, "title": "巨鹿县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2024-07-01"},
    {"person_id": 14, "org_id": 2, "title": "巨鹿县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2024-07-01"},
    {"person_id": 15, "org_id": 2, "title": "巨鹿县人民政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2024-07-01"},

    # County Party Committee leaders
    {"person_id": 21, "org_id": 5, "title": "中共巨鹿县委常委、县纪委书记、县监委主任",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "县纪委十二届六次全会工作报告 (2026-02-14)"},
    {"person_id": 22, "org_id": 1, "title": "中共巨鹿县委常委",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "陪同杨振东调研城市更新、产业集群等工作"},
    {"person_id": 23, "org_id": 1, "title": "中共巨鹿县委常委",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "陪同杨振东调研大气污染防治、产业集群等工作"},
    {"person_id": 24, "org_id": 1, "title": "中共巨鹿县委常委",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "陪同杨振东赴邯郸考察工业品直播"},
    {"person_id": 25, "org_id": 1, "title": "中共巨鹿县委常委",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "多次陪同杨振东调研城市更新、产业集群等工作"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Core team overlap (党政协同)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "巨鹿县党政一把手工作搭档关系（县委书记杨振东与县长李精虎）",
     "overlap_org": "巨鹿县",
     "overlap_period": "2025-2026年（至少）"},

    # Party Secretary with County Party Committee members
    {"person_a": 1, "person_b": 21, "type": "superior_subordinate",
     "context": "县委书记与纪委书记工作关系",
     "overlap_org": "中共巨鹿县委员会",
     "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 22, "type": "superior_subordinate",
     "context": "县委书记与县委常委宋光华工作关系",
     "overlap_org": "中共巨鹿县委员会",
     "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 23, "type": "superior_subordinate",
     "context": "县委书记与县委常委樊抗工作关系",
     "overlap_org": "中共巨鹿县委员会",
     "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 24, "type": "superior_subordinate",
     "context": "县委书记与县委常委林晨工作关系（同赴邯郸考察）",
     "overlap_org": "中共巨鹿县委员会",
     "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 25, "type": "superior_subordinate",
     "context": "县委书记与县委常委王刚工作关系",
     "overlap_org": "中共巨鹿县委员会",
     "overlap_period": "2026年"},

    # Mayor with Deputy County Mayors
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与常务副县长曹世恒工作关系",
     "overlap_org": "巨鹿县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长龙赛工作关系",
     "overlap_org": "巨鹿县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与副县长王立辉工作关系",
     "overlap_org": "巨鹿县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长李兵工作关系",
     "overlap_org": "巨鹿县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长田建强工作关系（一同参加大气污染防治督导）",
     "overlap_org": "巨鹿县人民政府",
     "overlap_period": "2026年"},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  邢台市巨鹿县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-23")
    print("  ✅ 县委书记: 杨振东")
    print("  ✅ 县长: 李精虎")
    print("  ✅ 常务副县长: 曹世恒")
    print("  ✅ 副县长 (4位): 龙赛, 王立辉, 李兵, 田建强")
    print("  ✅ 县委常委: 王彦彬(纪委书记), 宋光华, 樊抗, 林晨, 王刚")
    print("  ⚠️  主要来源: 巨鹿县人民政府官网 (www.julu.gov.cn)")
    print("  ⚠️  个人履历信息不完整（官网领导页面仅含照片，无文字简历）")
    print("  ⚠️  杨振东/李精虎的出生年份、籍贯、教育背景等详细信息待补充")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\n✅ 巨鹿县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  个人详细履历等信息待后续通过百度百科等渠道补充。")
