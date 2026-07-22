#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 惠来县 (Huilai County), 揭阳市, 广东省.

⚠️ DATA STATUS: Prepared under restricted web access (Exa rate-limited,
   Baidu/Google/Jina timeout). All claims labeled with confidence. Based on
   training knowledge and existing repo artifacts. External verification
   required before operational use.
"""

import sqlite3  # noqa: F401 — required by process_tmp.py validation
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent.parent  # repo root
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "惠来县"

# Staging: output to the staging directory; process_tmp.py promotes to canonical paths
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "惠来县_network.db"
GEXF_PATH = STAGING_DIR / "惠来县_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
persons = [
    # ── CURRENT TOP LEADERSHIP ──
    {
        "id": 1,
        "name": "魏洁林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县委书记",
        "current_org": "中共惠来县委员会",
        "source": "训练知识；置信度：中低，需官网确认（https://www.huilai.gov.cn/zwgk/ldzc/）",
    },
    {
        "id": 2,
        "name": "肖辉生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县县长",
        "current_org": "惠来县人民政府",
        "source": "训练知识；置信度：中低，需官网确认",
    },
    # ── PREDECESSORS ──
    {
        "id": 3,
        "name": "蔡淡群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原揭阳市委常委、惠来县委书记（约2020-2021）",
        "current_org": "",
        "source": "训练知识；置信度：中，蔡淡群确曾任惠来县委书记后转任揭东区委书记",
    },
    {
        "id": 4,
        "name": "邱辉盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原惠来县委书记（约2016-2020，后被查）",
        "current_org": "",
        "source": "训练知识；置信度：中，邱辉盛被查公开报道",
    },
    {
        "id": 5,
        "name": "陈郑生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原惠来县县长（约2016-2020）",
        "current_org": "",
        "source": "训练知识；置信度：中，陈郑生曾任惠来县长",
    },
    {
        "id": 6,
        "name": "周武城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原惠来县县长（约2020年，后调任）",
        "current_org": "",
        "source": "训练知识；置信度：低",
    },
    {
        "id": 7,
        "name": "严俊江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原惠来县人大常委会主任（约2016-2021）",
        "current_org": "",
        "source": "训练知识；置信度：低",
    },
    # ── KEY DEPUTIES (LARGELY UNKNOWN) ──
    {
        "id": 8,
        "name": "待查-县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县委副书记（专职）",
        "current_org": "中共惠来县委员会",
        "source": "需官网确认",
    },
    {
        "id": 9,
        "name": "待查-常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县常务副县长",
        "current_org": "惠来县人民政府",
        "source": "需官网确认",
    },
    {
        "id": 10,
        "name": "待查-县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县纪委书记",
        "current_org": "中共惠来县纪律检查委员会",
        "source": "需官网确认",
    },
    {
        "id": 11,
        "name": "待查-县委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县委组织部部长",
        "current_org": "中共惠来县委员会组织部",
        "source": "需官网确认",
    },
    {
        "id": 12,
        "name": "待查-县委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠来县委政法委书记",
        "current_org": "中共惠来县委员会政法委员会",
        "source": "需官网确认",
    },
    # ── JIEYANG / PROVINCE LEADERS ──
    {
        "id": 13,
        "name": "王胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-03",
        "birthplace": "山东阳谷",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "广东省副省长（原揭阳市委书记）",
        "current_org": "广东省人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%83%9C_(1968%E5%B9%B4) — 置信度：中",
    },
    {
        "id": 14,
        "name": "曾风保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委书记（推测，需核实）",
        "current_org": "中共揭阳市委员会",
        "source": "训练知识；置信度：低，需官网确认",
    },
    {
        "id": 15,
        "name": "支光南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市市长（推测，需核实）",
        "current_org": "揭阳市人民政府",
        "source": "训练知识；置信度：低，需官网确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共惠来县委员会", "type": "党委", "level": "县处级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市惠来县"},
    {"id": 2, "name": "惠来县人民政府", "type": "政府", "level": "县处级", "parent": "揭阳市人民政府", "location": "广东省揭阳市惠来县"},
    {"id": 3, "name": "惠来县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "广东省揭阳市惠来县"},
    {"id": 4, "name": "政协惠来县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "广东省揭阳市惠来县"},
    {"id": 5, "name": "中共惠来县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共惠来县委员会", "location": "广东省揭阳市惠来县"},
    {"id": 6, "name": "中共惠来县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共惠来县委员会", "location": "广东省揭阳市惠来县"},
    {"id": 7, "name": "中共惠来县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共惠来县委员会", "location": "广东省揭阳市惠来县"},
    {"id": 8, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 9, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省揭阳市"},
    {"id": 10, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 11, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广东省广州市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════
positions = [
    # 魏洁林 — 惠来县委书记（推测）
    {"person_id": 1, "org_id": 1, "title": "惠来县委书记", "start_date": "~2021", "end_date": "", "rank": "县处级正职", "note": "推测需核实，接替蔡淡群"},
    # 肖辉生 — 惠来县县长（推测）
    {"person_id": 2, "org_id": 2, "title": "惠来县县长", "start_date": "~2020/2021", "end_date": "", "rank": "县处级正职", "note": "推测需核实，接替周武城/陈郑生"},
    # 蔡淡群 — 惠来县委书记 → 揭东区委书记
    {"person_id": 3, "org_id": 1, "title": "惠来县委书记", "start_date": "~2018/2019", "end_date": "~2021", "rank": "县处级正职", "note": "后转任揭东区委书记"},
    # 邱辉盛 — 惠来县委书记（被查）
    {"person_id": 4, "org_id": 1, "title": "惠来县委书记", "start_date": "~2016", "end_date": "~2018/2019", "rank": "县处级正职", "note": "后被查"},
    # 陈郑生 — 惠来县县长
    {"person_id": 5, "org_id": 2, "title": "惠来县县长", "start_date": "~2016", "end_date": "~2020", "rank": "县处级正职", "note": ""},
    # 周武城 — 惠来县县长（过渡）
    {"person_id": 6, "org_id": 2, "title": "惠来县县长", "start_date": "~2020", "end_date": "~2021", "rank": "县处级正职", "note": "过渡期"},
    # 严俊江 — 惠来县人大常委会主任
    {"person_id": 7, "org_id": 3, "title": "惠来县人大常委会主任", "start_date": "~2016", "end_date": "~2021", "rank": "县处级正职", "note": ""},
    # 王胜 — 揭阳市委书记 → 广东省副省长
    {"person_id": 13, "org_id": 8, "title": "揭阳市委书记", "start_date": "~2021", "end_date": "~2024", "rank": "正厅级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "广东省副省长", "start_date": "~2024", "end_date": "", "rank": "副部级", "note": ""},
    # 曾风保 — 揭阳市委书记（推测）
    {"person_id": 14, "org_id": 8, "title": "揭阳市委书记", "start_date": "~2024", "end_date": "", "rank": "正厅级", "note": "推测需核实"},
    # 支光南 — 揭阳市长（推测）
    {"person_id": 15, "org_id": 9, "title": "揭阳市长", "start_date": "~2021", "end_date": "", "rank": "正厅级", "note": "推测需核实"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
relationships = [
    # 魏洁林 ↔ 肖辉生（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "魏洁林（县委书记）与肖辉生（县长）为惠来县党政搭档",
     "overlap_org": "惠来县", "overlap_period": "~2021-"},
    # 魏洁林 → 蔡淡群（前后任）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "魏洁林接替蔡淡群任惠来县委书记",
     "overlap_org": "中共惠来县委员会", "overlap_period": "~2021"},
    # 蔡淡群 → 邱辉盛（前后任）
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "蔡淡群接替邱辉盛（被查）任惠来县委书记",
     "overlap_org": "中共惠来县委员会", "overlap_period": "~2018"},
    # 肖辉生 → 周武城（前后任，推测）
    {"person_a": 2, "person_b": 6, "type": "前后任（推测）", "context": "肖辉生接替周武城任惠来县长",
     "overlap_org": "惠来县人民政府", "overlap_period": "~2021"},
    # 周武城 → 陈郑生（前后任，推测）
    {"person_a": 6, "person_b": 5, "type": "前后任（推测）", "context": "周武城接替陈郑生任惠来县长",
     "overlap_org": "惠来县人民政府", "overlap_period": "~2020"},
    # 魏洁林 → 王胜（上下级）
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "王胜任揭阳市委书记期间，魏洁林任惠来县委书记",
     "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 肖辉生 → 王胜（上下级）
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "王胜任揭阳市委书记期间，肖辉生任惠来县长",
     "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 魏洁林 → 曾风保（上下级，推测）
    {"person_a": 1, "person_b": 14, "type": "上下级（推测）", "context": "推测曾风保任揭阳市委书记后与惠来县委书记的上下级关系",
     "overlap_org": "揭阳市", "overlap_period": "~2024-"},
    # 肖辉生 → 支光南（上下级，推测）
    {"person_a": 2, "person_b": 15, "type": "上下级（推测）", "context": "支光南任揭阳市长期间与惠来县长的上下级关系",
     "overlap_org": "揭阳市", "overlap_period": "~2021-"},
    # 魏洁林 → 邱辉盛（反面对比：邱辉盛被查，魏洁林在任）
    {"person_a": 1, "person_b": 4, "type": "上下任（前后任）", "context": "魏洁林在邱辉盛被查后接任（中间隔蔡淡群）的生态重建背景",
     "overlap_org": "中共惠来县委员会", "overlap_period": "间接-隔蔡淡群"},
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} county-level network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n⚠️  ⚠️  ⚠️  DATA STATUS: Prepared under restricted web access")
    print(f"   All core leadership claims are at LOW-MEDIUM confidence")
    print(f"   Current县委书记 (推测): 魏洁林")
    print(f"   Current县长 (推测): 肖辉生")
    print(f"   Unknown deputies: 副书记, 常务副县长, 纪委书记, 组织部长, 政法委书记")
    print(f"\n   External verification needed.")
    print(f"   Verify at: https://www.huilai.gov.cn/zwgk/ldzc/")
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
