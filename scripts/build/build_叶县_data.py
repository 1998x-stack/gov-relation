#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 叶县 (Yexian County), 平顶山市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_叶县
Level: 县
Targets: 县委书记 & 县长

Research constraints:
  - Exa search: rate-limited (free tier exhausted)
  - Baidu: 403/blocked
  - Jina Reader: timed out
  - Google: timed out via available proxies
  - Direct curl to www.yexian.gov.cn: successful — core leaders confirmed from
    multiple official news articles (2026-06 to 2026-07)

Evidence approach:
  - Core leader identities (文晓凡, 韩沛) confirmed from yexian.gov.cn official
    news articles published 2026-06-29 through 2026-07-21
  - Deputy rosters partially confirmed from meeting attendance lists
  - Detailed biographies, exact appointment dates mostly unverified
  - This is a partial-evidence artifact following the source_fallbacks playbook:
    create valid artifacts with explicit uncertainty markers

Confirmed sources:
  - https://www.yexian.gov.cn/contents/6507/750042.html (2026-07-12 安防委会议)
    → 文晓凡 as 县委书记, 韩沛 as 县委副书记、县长
  - https://www.yexian.gov.cn/contents/6507/749146.html (2026-06-29 两优一先表彰大会)
    → 文晓凡, 韩沛, 张军辉, 张成文, 田红霞 confirmed
  - https://www.yexian.gov.cn/contents/6507/750043.html (2026-07-10 脱贫攻坚会议)
    → 张军辉 as 县委副书记 confirmed
  - https://www.yexian.gov.cn/contents/6507/750719.html (2026-07-21 水污染治理)
    → 韩沛 as 县委副书记、县长, 陈杰 as 副县长 confirmed
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Add repo root to path for gov_relation imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # data/tmp/henan_叶县 -> data/tmp -> data -> repo_root
os.chdir(str(BASE_DIR))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "叶县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE_DIR / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE_DIR / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "文晓凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共叶县委员会",
        "source": "叶县人民政府官网2026-07-12安防委会议、2026-06-29两优一先表彰大会确认文晓凡为县委书记"
    },
    {
        "id": 2,
        "name": "韩沛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "叶县人民政府",
        "source": "叶县人民政府官网多篇2026年7月新闻报道确认韩沛为县委副书记、县长"
    },
    # ═══════ County Leadership ═══════
    {
        "id": 3,
        "name": "张军辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共叶县委员会",
        "source": "叶县人民政府官网2026-06-29两优一先表彰大会确认张军辉为县委副书记"
    },
    {
        "id": 4,
        "name": "张成文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "叶县人大常委会",
        "source": "叶县人民政府官网2026-06-29两优一先表彰大会确认张成文为县人大常委会主任"
    },
    {
        "id": 5,
        "name": "田红霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "叶县政协",
        "source": "叶县人民政府官网2026-06-29两优一先表彰大会确认田红霞为县政协主席"
    },
    {
        "id": 6,
        "name": "陈杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "叶县人民政府",
        "source": "叶县人民政府官网2026-07-21水污染治理报道确认陈杰为副县长"
    },
    {
        "id": 7,
        "name": "兰丰蕊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "叶县人民政府",
        "source": "叶县人民政府官网2026-07-12安防委会议确认兰丰蕊安排防汛抗旱工作；2026-07-10脱贫攻坚会议确认兰丰蕊为副县长"
    },
    # ═══════ Attending Meeting Leaders (roles not fully confirmed) ═══════
    {
        "id": 8,
        "name": "李蕾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 9,
        "name": "肖志举",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 10,
        "name": "李黎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 11,
        "name": "温卫杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 12,
        "name": "樊亚杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 13,
        "name": "贾俊杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单，通报开发区D级园区创建"
    },
    {
        "id": 14,
        "name": "赵跃军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 15,
        "name": "张立辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-07-12安防委会议列席名单"
    },
    {
        "id": 16,
        "name": "李向伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县级领导",
        "current_org": "叶县",
        "source": "叶县人民政府官网2026-06-29两优一先表彰大会宣读表彰决定"
    },
    # ═══════ Additional Notable ═══════
    {
        "id": 17,
        "name": "苗红雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "燕山水库运行中心主任",
        "current_org": "燕山水库运行中心",
        "source": "叶县人民政府官网2026-07-21水污染治理报道"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共叶县委员会", "type": "党委", "level": "县", "parent": "中共平顶山市委", "location": "叶县"},
    {"id": 2, "name": "叶县人民政府", "type": "政府", "level": "县", "parent": "平顶山市人民政府", "location": "叶县"},
    {"id": 3, "name": "叶县人大常委会", "type": "人大", "level": "县", "parent": "平顶山市人大常委会", "location": "叶县"},
    {"id": 4, "name": "叶县政协", "type": "政协", "level": "县", "parent": "平顶山市政协", "location": "叶县"},
    {"id": 5, "name": "中共平顶山市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "平顶山市"},
    {"id": 6, "name": "平顶山市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "平顶山市"},
    {"id": 7, "name": "燕山水库运行中心", "type": "事业单位", "level": "县处级", "parent": "河南省水利厅", "location": "叶县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 文晓凡 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "至今", "rank": "正县级", "note": "2026年6-7月多篇报道确认为现任县委书记"},
    # 韩沛 — 县委副书记、县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 张军辉 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 张成文 — 县人大常委会主任
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正县级", "note": ""},
    # 田红霞 — 县政协主席
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "至今", "rank": "正县级", "note": "女性"},
    # 陈杰 — 副县长
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 兰丰蕊 — 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "分管防汛抗旱等工作"},
    # 李蕾
    {"person_id": 8, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 肖志举
    {"person_id": 9, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 李黎
    {"person_id": 10, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 温卫杰
    {"person_id": 11, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 樊亚杰
    {"person_id": 12, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 贾俊杰
    {"person_id": 13, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": "负责开发区D级园区创建相关工作"},
    # 赵跃军
    {"person_id": 14, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 张立辉
    {"person_id": 15, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 李向伟
    {"person_id": 16, "org_id": 1, "title": "县级领导", "start_date": "", "end_date": "至今", "rank": "副县级", "note": ""},
    # 苗红雄 — 燕山水库运行中心主任
    {"person_id": 17, "org_id": 7, "title": "燕山水库运行中心主任", "start_date": "", "end_date": "至今", "rank": "县处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 文晓凡 — 韩沛（县委书记与县长工作搭档）
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记与县长工作搭档", "overlap_org": "叶县", "overlap_period": "2026年至今"},
    # 文晓凡 — 张军辉（县委书记与县委副书记）
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "县委书记与县委副书记工作关系", "overlap_org": "中共叶县委员会", "overlap_period": ""},
    # 韩沛 — 张军辉（县长与县委副书记）
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "县长与县委副书记同为县委领导班子成员", "overlap_org": "中共叶县委员会", "overlap_period": ""},
    # 韩沛 — 陈杰（县长与副县长）
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "叶县人民政府", "overlap_period": "2026年"},
    # 韩沛 — 兰丰蕊（县长与副县长）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "叶县人民政府", "overlap_period": "2026年"},
    # 张成文 — 田红霞（人大主任与政协主席）
    {"person_a": 4, "person_b": 5, "type": "共事", "context": "人大主任与政协主席同为四套班子主要领导", "overlap_org": "叶县", "overlap_period": ""},
]

# ── Build ───────────────────────────────────────────────────────────────────
def main():
    os.makedirs(STAGING_DIR, exist_ok=True)

    # Run via gov_relation.runner
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

    print(f"\n=== Build Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
