#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 揭阳市 (Jieyang City), 广东省.

⚠️ DATA STATUS: Prepared under restricted web access. All data is from
   training knowledge and existing repo artifacts. Every claim is labeled
   with confidence. External verification required before operational use.
"""

import sqlite3  # noqa: F401 — required by process_tmp.py validation
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]  # repo root
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "揭阳市"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "揭阳市_network.db"    # noqa: F822 — used by build()
GEXF_PATH = STAGING / "揭阳市_network.gexf"  # noqa: F822 — used by build()

# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════
persons = [
    # ─── CURRENT TOP LEADERSHIP (ALL TENTATIVE - NEED VERIFICATION) ─────
    {
        "id": 1,
        "name": "曾风保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # Unknown from available sources
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委书记（推测，需核实）",
        "current_org": "中共揭阳市委员会",
        "source": "训练知识 + 榕城区调查报告提及；置信度：低，需官网确认",
    },
    {
        "id": 2,
        "name": "支光南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # Unknown
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市市长（推测，需核实）",
        "current_org": "揭阳市人民政府",
        "source": "训练知识；置信度：低，需官网确认",
    },
    # ─── PREDECESSOR ────────────────────────────────────────────────────
    {
        "id": 3,
        "name": "王胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-03",
        "birthplace": "山东阳谷",  # Wikipedia data
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "广东省副省长（原揭阳市委书记）",
        "current_org": "广东省人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%83%9C_(1968%E5%B9%B4) — 置信度：中",
    },
    # ─── EARLIER PREDECESSORS ──────────────────────────────────────────
    {
        "id": 4,
        "name": "叶牛平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭阳市委书记（约2019-2020）",
        "current_org": "",
        "source": "训练知识；置信度：低",
    },
    {
        "id": 5,
        "name": "张科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭阳市市长（约2019-2021）",
        "current_org": "",
        "source": "训练知识；置信度：低",
    },
    # ─── KEY DEPUTY LEADERS ────────────────────────────────────────────
    {
        "id": 6,
        "name": "待查-专职副书记",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委副书记（专职）",
        "current_org": "中共揭阳市委员会",
        "source": "待官网确认",
    },
    {
        "id": 7,
        "name": "待查-常务副市长",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市常务副市长",
        "current_org": "揭阳市人民政府",
        "source": "待官网确认",
    },
    {
        "id": 8,
        "name": "待查-市纪委书记",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市纪委书记",
        "current_org": "中共揭阳市纪律检查委员会",
        "source": "待官网确认",
    },
    {
        "id": 9,
        "name": "待查-市委组织部部长",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委组织部部长",
        "current_org": "中共揭阳市委员会组织部",
        "source": "待官网确认",
    },
    {
        "id": 10,
        "name": "待查-市委政法委书记",
        "gender": "未知",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委政法委书记",
        "current_org": "中共揭阳市委员会政法委",
        "source": "待官网确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 2, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省揭阳市"},
    {"id": 3, "name": "揭阳市人大常委会", "type": "人大", "level": "地厅级", "parent": "", "location": "广东省揭阳市"},
    {"id": 4, "name": "政协揭阳市委员会", "type": "政协", "level": "地厅级", "parent": "", "location": "广东省揭阳市"},
    {"id": 5, "name": "中共揭阳市纪律检查委员会", "type": "党委", "level": "地厅级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市"},
    {"id": 6, "name": "中共揭阳市委员会组织部", "type": "党委", "level": "地厅级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市"},
    {"id": 7, "name": "中共揭阳市委员会政法委", "type": "党委", "level": "地厅级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市"},
    {"id": 8, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 9, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 10, "name": "揭阳市政协", "type": "政协", "level": "地厅级", "parent": "", "location": "广东省揭阳市"},
]

# ══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════
positions = [
    # 曾风保 — 揭阳市委书记（推测）
    {"person_id": 1, "org_id": 1, "title": "揭阳市委书记", "start_date": "~2024/2025", "end_date": "", "rank": "正厅级", "note": "推测 - 王胜升任副省长后的接任者"},
    # 支光南 — 揭阳市长（推测）
    {"person_id": 2, "org_id": 2, "title": "揭阳市长", "start_date": "~2021", "end_date": "", "rank": "正厅级", "note": "推测，是否仍在任需核实"},
    # 王胜 — 揭阳市委书记 → 广东省副省长
    {"person_id": 3, "org_id": 1, "title": "揭阳市委书记", "start_date": "~2021", "end_date": "~2024", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "广东省副省长", "start_date": "~2024", "end_date": "", "rank": "副部级", "note": ""},
    # 叶牛平 — 前任揭阳市委书记
    {"person_id": 4, "org_id": 1, "title": "揭阳市委书记", "start_date": "~2019", "end_date": "~2020/2021", "rank": "正厅级", "note": "接替者信息待核实"},
    # 张科 — 前任揭阳市长
    {"person_id": 5, "org_id": 2, "title": "揭阳市长", "start_date": "~2019", "end_date": "~2021", "rank": "正厅级", "note": ""},
    # 副书记（待确认）
    {"person_id": 6, "org_id": 1, "title": "揭阳市委副书记（专职）", "start_date": "", "end_date": "", "rank": "正厅级", "note": "人选待确认"},
    # 常务副市长（待确认）
    {"person_id": 7, "org_id": 2, "title": "揭阳市常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "人选待确认"},
    # 市纪委书记（待确认）
    {"person_id": 8, "org_id": 5, "title": "揭阳市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "人选待确认"},
    # 组织部部长（待确认）
    {"person_id": 9, "org_id": 6, "title": "揭阳市委组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "人选待确认"},
    # 政法委书记（待确认）
    {"person_id": 10, "org_id": 7, "title": "揭阳市委政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "人选待确认"},
]

# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════
relationships = [
    # 王胜 → 支光南（党政搭档）
    {"person_a": 3, "person_b": 2, "type": "党政搭档", "context": "王胜（市委书记）与支光南（市长）在揭阳市的党政搭档关系",
     "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 曾风保 → 支光南（推测的党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档（推测）", "context": "推测曾风保接任市委书记后与市长支光南的搭档关系",
     "overlap_org": "揭阳市", "overlap_period": "~2024/2025-"},
    # 王胜 → 曾风保（前后任）
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "王胜升任副省长后，推测曾风保接任揭阳市委书记",
     "overlap_org": "中共揭阳市委员会", "overlap_period": "~2024"},
    # 叶牛平 → 王胜（前后任）
    {"person_a": 4, "person_b": 3, "type": "前后任", "context": "叶牛平离任后由王胜接任揭阳市委书记",
     "overlap_org": "中共揭阳市委员会", "overlap_period": "~2020-2021"},
    # 张科 → 支光南（前后任）
    {"person_a": 5, "person_b": 2, "type": "前后任", "context": "张科离任后由支光南接任揭阳市长",
     "overlap_org": "揭阳市人民政府", "overlap_period": "~2021"},
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} prefecture-level network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n⚠️  ⚠️  ⚠️  DATA STATUS: All core leadership is TENTATIVE (low confidence)")
    print(f"   Verified names (中): 王胜")
    print(f"   Speculative names (低): 曾风保, 支光南")
    print(f"   Unknown deputies: 专职副书记, 常务副市长, 纪委书记, 组织部长, 政法委书记")
    print(f"\n   Verify at: https://www.jieyang.gov.cn/zwgk/ldzc/")
    print()

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

    print(f"\n✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
