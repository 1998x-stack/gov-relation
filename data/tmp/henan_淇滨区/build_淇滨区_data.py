#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 鹤壁市淇滨区 leadership network.

淇滨区 - 河南省鹤壁市 (市辖区)
Targets: 区委书记, 区长
"""

import sqlite3  # noqa: F401
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "淇滨区"
TASK_ID = "henan_淇滨区"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ⚠️ DATA STATUS: All data below is sourced from pre-existing knowledge and
#    general public records. Web access was completely unavailable during
#    research (Exa rate-limited, all Chinese government/Baidu/Wikipedia
#    sites unreachable). All claims marked as "unverified" until confirmed
#    against official government sources. See open_gaps.md for details.

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ═══════════════ 1: Core Leaders ═══════════════
    # 淇滨区委书记 — 需确认现任人员
    # Option A: 张育文 (2023年调任鹤壁市淇滨区任职的报道)
    # Option B: 另有他人 — 待多渠道验证
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共鹤壁市淇滨区委书记（待确认）",
        "current_org": "中国共产党鹤壁市淇滨区委员会",
        "source": "待补充",
    },
    # 淇滨区区长 — 需确认现任人员
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鹤壁市淇滨区区长（待确认）",
        "current_org": "鹤壁市淇滨区人民政府",
        "source": "待补充",
    },
    # ═══════════════ 2: Previous Leaders (Predecessors) ═══════════════
    # 前任淇滨区委书记 — 历史记载
    {
        "id": 3,
        "name": "待确认（前任区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "待确认",
        "current_org": "",
        "source": "待补充",
    },
    # 前任淇滨区区长
    {
        "id": 4,
        "name": "待确认（前任区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "待确认",
        "current_org": "",
        "source": "待补充",
    },
    # ═══════════════ 3: District Leadership Team ═══════════════
    # 区委副书记（协助书记工作）
    {
        "id": 5,
        "name": "待确认（区委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委副书记",
        "current_org": "中国共产党鹤壁市淇滨区委员会",
        "source": "待补充",
    },
    # 常务副区长
    {
        "id": 6,
        "name": "待确认（常务副区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、常务副区长",
        "current_org": "鹤壁市淇滨区人民政府",
        "source": "待补充",
    },
    # 区纪委书记/监委主任
    {
        "id": 7,
        "name": "待确认（区纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、区纪委书记、区监委主任",
        "current_org": "中共鹤壁市淇滨区纪律检查委员会",
        "source": "待补充",
    },
    # 组织部部长
    {
        "id": 8,
        "name": "待确认（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、组织部部长",
        "current_org": "中国共产党鹤壁市淇滨区委员会组织部",
        "source": "待补充",
    },
    # 宣传部部长
    {
        "id": 9,
        "name": "待确认（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、宣传部部长",
        "current_org": "中国共产党鹤壁市淇滨区委员会宣传部",
        "source": "待补充",
    },
    # 政法委书记
    {
        "id": 10,
        "name": "待确认（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、政法委书记",
        "current_org": "中国共产党鹤壁市淇滨区委员会政法委员会",
        "source": "待补充",
    },
    # 统战部部长
    {
        "id": 11,
        "name": "待确认（统战部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区委常委、统战部部长",
        "current_org": "中国共产党鹤壁市淇滨区委员会统战部",
        "source": "待补充",
    },
    # ═══════════════ 4: District-level Officials ═══════════════
    # 区人大常委会主任
    {
        "id": 12,
        "name": "待确认（区人大主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区人大常委会主任",
        "current_org": "鹤壁市淇滨区人民代表大会",
        "source": "待补充",
    },
    # 区政协主席
    {
        "id": 13,
        "name": "待确认（区政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区政协主席",
        "current_org": "中国人民政治协商会议鹤壁市淇滨区委员会",
        "source": "待补充",
    },
    # 副区长（分管公安）
    {
        "id": 14,
        "name": "待确认（副区长、公安分局局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "淇滨区副区长、市公安局淇滨分局局长",
        "current_org": "鹤壁市淇滨区人民政府",
        "source": "待补充",
    },
]

# ── Organizations ────────────────────────────────────────────────────────

organizations = [
    # 党委系统
    {"id": 1, "name": "中国共产党鹤壁市淇滨区委员会", "type": "党委", "level": "县级", "parent": "中国共产党鹤壁市委员会", "location": "鹤壁市淇滨区"},
    {"id": 2, "name": "中共鹤壁市淇滨区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
    {"id": 3, "name": "中国共产党鹤壁市淇滨区委员会组织部", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
    {"id": 4, "name": "中国共产党鹤壁市淇滨区委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
    {"id": 5, "name": "中国共产党鹤壁市淇滨区委员会统战部", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
    {"id": 6, "name": "中国共产党鹤壁市淇滨区委员会政法委员会", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
    # 政府系统
    {"id": 7, "name": "鹤壁市淇滨区人民政府", "type": "政府", "level": "县级", "parent": "鹤壁市人民政府", "location": "鹤壁市淇滨区"},
    # 人大/政协/监察
    {"id": 8, "name": "鹤壁市淇滨区人民代表大会", "type": "人大", "level": "县级", "parent": "", "location": "鹤壁市淇滨区"},
    {"id": 9, "name": "中国人民政治协商会议鹤壁市淇滨区委员会", "type": "政协", "level": "县级", "parent": "", "location": "鹤壁市淇滨区"},
    {"id": 10, "name": "鹤壁市淇滨区监察委员会", "type": "监察", "level": "县级", "parent": "", "location": "鹤壁市淇滨区"},
    {"id": 11, "name": "鹤壁市公安局淇滨分局", "type": "政府", "level": "县级", "parent": "鹤壁市淇滨区人民政府", "location": "鹤壁市淇滨区"},
    # 上级组织
    {"id": 12, "name": "中国共产党鹤壁市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党河南省委员会", "location": "鹤壁市"},
    {"id": 13, "name": "鹤壁市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "鹤壁市"},
    {"id": 14, "name": "中国共产党河南省委员会", "type": "党委", "level": "省级", "parent": "", "location": "郑州市"},
    {"id": 15, "name": "河南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "郑州市"},
    # 乡镇/街道（淇滨区下辖）
    {"id": 16, "name": "中国共产党鹤壁市淇滨区委员会办公室", "type": "党委部门", "level": "县级", "parent": "中国共产党鹤壁市淇滨区委员会", "location": "鹤壁市淇滨区"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 区委书记（待确认）
    {"person_id": 1, "org_id": 1, "title": "中共鹤壁市淇滨区委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "现任，姓名待确认"},
    # 区长（待确认）
    {"person_id": 2, "org_id": 7, "title": "鹤壁市淇滨区区长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "现任，姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "中共鹤壁市淇滨区委副书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "中共鹤壁市淇滨区委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    # 前任区长
    {"person_id": 4, "org_id": 7, "title": "鹤壁市淇滨区区长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    # 区委副书记
    {"person_id": 5, "org_id": 1, "title": "淇滨区委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 常务副区长
    {"person_id": 6, "org_id": 7, "title": "淇滨区委常委、常务副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 区纪委书记
    {"person_id": 7, "org_id": 2, "title": "淇滨区委常委、区纪委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 10, "title": "淇滨区监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "合署办公"},
    # 组织部部长
    {"person_id": 8, "org_id": 3, "title": "淇滨区委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 宣传部部长
    {"person_id": 9, "org_id": 4, "title": "淇滨区委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 政法委书记
    {"person_id": 10, "org_id": 6, "title": "淇滨区委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 统战部部长
    {"person_id": 11, "org_id": 5, "title": "淇滨区委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    # 区人大主任
    {"person_id": 12, "org_id": 8, "title": "淇滨区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "姓名待确认"},
    # 区政协主席
    {"person_id": 13, "org_id": 9, "title": "淇滨区政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "姓名待确认"},
    # 副区长/公安分局局长
    {"person_id": 14, "org_id": 7, "title": "淇滨区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 14, "org_id": 11, "title": "鹤壁市公安局淇滨分局局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "姓名待确认"},
]

# ── Relationships ────────────────────────────────────────────────────────

relationships = [
    # 核心党政搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记与区长为淇滨区党政正职搭档关系（姓名待确认）",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会/鹤壁市淇滨区人民政府",
     "overlap_period": ""},
    # 上下级关系：书记-副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委副书记的工作关系",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    # 上下级关系：区长-常务副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与常务副区长的政府工作关系",
     "overlap_org": "鹤壁市淇滨区人民政府",
     "overlap_period": ""},
    # 区委常委班子内部同级关系
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 9, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    {"person_a": 5, "person_b": 11, "type": "overlap",
     "context": "同为淇滨区委常委班子成员",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    # 书记-前任书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "现任区委书记接替前任（姓名均待确认）",
     "overlap_org": "中国共产党鹤壁市淇滨区委员会",
     "overlap_period": ""},
    # 区长-前任区长
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "现任区长接替前任（姓名均待确认）",
     "overlap_org": "鹤壁市淇滨区人民政府",
     "overlap_period": ""},
]

# ── Build ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} network... (⚠️ ALL DATA UNVERIFIED - web access unavailable)")
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
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done. ⚠️  All person names are '待确认' because web research was blocked.")
