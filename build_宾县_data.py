#!/usr/bin/env python3
"""Build script for 宾县 (黑龙江省哈尔滨市) — county-level leadership network."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR, REPORT_DIR

SLUG = "宾县"
PROVINCE = "黑龙江省"
CITY = "哈尔滨市"
REGION = "宾县"
LEVEL = "县"
AS_OF = "2026-07-24"

STAGING = Path(__file__).parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "赵洪臣",
        "gender": "男",
        "current_post": "县委书记",
        "current_org": "中共宾县委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134947.shtml",
    },
    {
        "id": 2,
        "name": "刘海龙",
        "gender": "男",
        "current_post": "县委副书记、县长",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134947.shtml",
    },
    {
        "id": 3,
        "name": "孙欣",
        "gender": "男",
        "current_post": "县委常委、副县长",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202604/c01_1121450.shtml",
    },
    {
        "id": 4,
        "name": "刘研",
        "gender": "男",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共宾县委员会组织部",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1133162.shtml",
    },
    {
        "id": 5,
        "name": "黄永鑫",
        "gender": "男",
        "current_post": "副县长",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 6,
        "name": "周广兴",
        "gender": "男",
        "current_post": "副县长",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 7,
        "name": "郭源雪",
        "gender": "男",
        "current_post": "县领导",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202604/c01_1121450.shtml",
    },
    {
        "id": 8,
        "name": "曹庆丰",
        "gender": "男",
        "current_post": "县领导",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134947.shtml",
    },
    {
        "id": 9,
        "name": "石喜瑞",
        "gender": "男",
        "current_post": "县人大常委会副主任",
        "current_org": "宾县人民代表大会常务委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 10,
        "name": "张戈胜",
        "gender": "男",
        "current_post": "县人大常委会副主任",
        "current_org": "宾县人民代表大会常务委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 11,
        "name": "王羡",
        "gender": "男",
        "current_post": "县人大常委会副主任",
        "current_org": "宾县人民代表大会常务委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 12,
        "name": "肖春生",
        "gender": "男",
        "current_post": "县政协主席（提名）",
        "current_org": "中国人民政治协商会议宾县委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134578.shtml",
    },
    {
        "id": 13,
        "name": "管宏宇",
        "gender": "男",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议宾县委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134578.shtml",
    },
    {
        "id": 14,
        "name": "刘海英",
        "gender": "女",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议宾县委员会",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134578.shtml",
    },
    {
        "id": 15,
        "name": "刘瑞鑫",
        "gender": "男",
        "current_post": "县领导",
        "current_org": "宾县人民政府",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    # Predecessors
    {
        "id": 16,
        "name": "庄汝坤",
        "gender": "男",
        "current_post": "",
        "current_org": "",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134578.shtml",
    },
    {
        "id": 17,
        "name": "谢卓",
        "gender": "男",
        "current_post": "",
        "current_org": "",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
    {
        "id": 18,
        "name": "孙洪利",
        "gender": "男",
        "current_post": "",
        "current_org": "",
        "source": "http://www.chinabx.gov.cn/hebbx/gzdt/202607/c01_1134579.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宾县委员会", "type": "党委", "level": "县", "location": "黑龙江省哈尔滨市宾县"},
    {"id": 2, "name": "宾县人民政府", "type": "政府", "level": "县", "location": "黑龙江省哈尔滨市宾县"},
    {"id": 3, "name": "中共宾县委员会组织部", "type": "党委", "level": "县", "location": "黑龙江省哈尔滨市宾县"},
    {"id": 4, "name": "宾县人民代表大会常务委员会", "type": "人大", "level": "县", "location": "黑龙江省哈尔滨市宾县"},
    {"id": 5, "name": "中国人民政治协商会议宾县委员会", "type": "政协", "level": "县", "location": "黑龙江省哈尔滨市宾县"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "As of 2026-07"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "As of 2026-07"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "宾县第十八届人大常委会第四十次会议任命"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "宾县第十八届人大常委会第四十次会议任命"},
    {"person_id": 7, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 4, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "县政协主席（提名）", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026年6月任县政协党组书记，提名主席候选人"},
    {"person_id": 13, "org_id": 5, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # Historical / former
    {"person_id": 12, "org_id": 1, "title": "县委宣传部部长", "start_date": "unknown", "end_date": "2026-06", "rank": "副处级", "note": "任职至2026年6月"},
    {"person_id": 16, "org_id": 5, "title": "县政协主席", "start_date": "unknown", "end_date": "2026-06", "rank": "正处级", "note": "2026年6月免去县政协党组书记职务"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "2026-07", "rank": "副处级", "note": "2026年7月免职"},
    {"person_id": 18, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "2026-07", "rank": "副处级", "note": "2026年7月免职"},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长——党委与政府主要领导搭档", "overlap_org": "宾县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委常委、副县长", "overlap_org": "宾县", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委、组织部部长", "overlap_org": "宾县", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与县委常委、副县长", "overlap_org": "宾县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与新任副县长", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与新任副县长", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "同为副县长（孙欣为常务副县长）", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "同为副县长", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 17, "person_b": 5, "type": "predecessor_successor", "context": "谢卓被免副县长，黄永鑫接任", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 18, "person_b": 6, "type": "predecessor_successor", "context": "孙洪利被免副县长，周广兴接任", "overlap_org": "宾县人民政府", "overlap_period": "2026-07"},
    {"person_a": 12, "person_b": 16, "type": "predecessor_successor", "context": "肖春生接替庄汝坤任政协主席", "overlap_org": "宾县政协", "overlap_period": "2026-06"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "同为人大常委会副主任", "overlap_org": "宾县人大常委会", "overlap_period": "2026"},
    {"person_a": 9, "person_b": 11, "type": "overlap", "context": "同为人大常委会副主任", "overlap_org": "宾县人大常委会", "overlap_period": "2026"},
    {"person_a": 13, "person_b": 14, "type": "overlap", "context": "同为政协副主席", "overlap_org": "宾县政协", "overlap_period": "2026"},
]

# ── Run ──────────────────────────────────────────────────────────────────
def main():
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print(f"DB: {db_path}")
    print(f"GEXF: {gexf_path}")


if __name__ == "__main__":
    main()
