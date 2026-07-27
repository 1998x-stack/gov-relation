#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 义马市 leadership network.

义马市 — 河南省三门峡市下辖县级市
"""

import sys
import os
from pathlib import Path

# Add project root to path
BASE = Path(__file__).resolve().parents[3]  # data/tmp/henan_义马市/ -> project root
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── 1. 姚振波 — 市委书记 (current) ──
    {
        "id": 1,
        "name": "姚振波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "义马市委书记",
        "current_org": "中共义马市委员会",
        "source": "https://baike.baidu.com/item/%E4%B9%89%E9%A9%AC%E5%B8%82/6861185",
    },
    # ── 2. 赵麒 — 市长 (current) ──
    {
        "id": 2,
        "name": "赵麒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "义马市长",
        "current_org": "义马市人民政府",
        "source": "https://baike.baidu.com/item/%E4%B9%89%E9%A9%AC%E5%B8%82/6861185",
    },
    # ── 3. 张光明 — 市人大常委会主任 ──
    {
        "id": 3,
        "name": "张光明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "义马市人大常委会主任",
        "current_org": "义马市人大常委会",
        "source": "https://baike.baidu.com/item/%E4%B9%89%E9%A9%AC%E5%B8%82/6861185",
    },
    # ── 4. 邹晓东 — 市政协主席 ──
    {
        "id": 4,
        "name": "邹晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "义马市政协主席",
        "current_org": "政协义马市委员会",
        "source": "https://baike.baidu.com/item/%E4%B9%89%E9%A9%AC%E5%B8%82/6861185",
    },
    # ── 5. 袁锐锋 — 前任市委书记（2023.06-2026.01），现任湖滨区委书记 ──
    {
        "id": 5,
        "name": "袁锐锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "河南安阳",
        "education": "在职研究生学历（农业推广硕士）",
        "party_join": "1995-11",
        "work_start": "1997-08",
        "current_post": "三门峡市湖滨区委书记",
        "current_org": "中共三门峡市湖滨区委员会",
        "source": "https://baike.baidu.com/item/%E8%A2%81%E9%94%90%E9%94%8B/55883389",
    },
    # ── 6. 何军 — 更早的前任义马市委书记 ──
    {
        "id": 6,
        "name": "何军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原义马市委书记，已调离）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/%E8%A2%81%E9%94%90%E9%94%8B/55883389",
    },
]

organizations = [
    {"id": 1, "name": "中共义马市委员会", "type": "党委", "level": "县级", "parent": "中共三门峡市委员会", "location": "河南省三门峡市义马市"},
    {"id": 2, "name": "义马市人民政府", "type": "政府", "level": "县级", "parent": "三门峡市人民政府", "location": "河南省三门峡市义马市"},
    {"id": 3, "name": "义马市人大常委会", "type": "人大", "level": "县级", "parent": "三门峡市人大常委会", "location": "河南省三门峡市义马市"},
    {"id": 4, "name": "政协义马市委员会", "type": "政协", "level": "县级", "parent": "政协三门峡市委员会", "location": "河南省三门峡市义马市"},
    {"id": 5, "name": "中共三门峡市湖滨区委员会", "type": "党委", "level": "县级", "parent": "中共三门峡市委员会", "location": "河南省三门峡市湖滨区"},
    {"id": 6, "name": "湖滨区人民政府", "type": "政府", "level": "县级", "parent": "三门峡市人民政府", "location": "河南省三门峡市湖滨区"},
    {"id": 7, "name": "义马市人武部", "type": "事业单位", "level": "县级", "parent": "三门峡军分区", "location": "河南省三门峡市义马市"},
]

positions = [
    # 姚振波
    {"person_id": 1, "org_id": 1, "title": "义马市委书记", "start_date": "未知", "end_date": "现任", "rank": "正县级", "note": "此前曾任义马市长"},
    # 赵麒
    {"person_id": 2, "org_id": 2, "title": "义马市长", "start_date": "未知", "end_date": "现任", "rank": "正县级", "note": "现任义马市人民政府市长"},
    # 张光明
    {"person_id": 3, "org_id": 3, "title": "义马市人大常委会主任", "start_date": "未知", "end_date": "现任", "rank": "正县级", "note": ""},
    # 邹晓东
    {"person_id": 4, "org_id": 4, "title": "义马市政协主席", "start_date": "未知", "end_date": "现任", "rank": "正县级", "note": ""},
    # 袁锐锋 — 曾任义马市委书记
    {"person_id": 5, "org_id": 1, "title": "义马市委书记", "start_date": "2023-06", "end_date": "2026-01", "rank": "正县级", "note": "2023年6月任义马市委书记，2023年7月兼任义马市人武部党委第一书记"},
    {"person_id": 5, "org_id": 5, "title": "湖滨区委书记", "start_date": "2026-01", "end_date": "现任", "rank": "正县级", "note": "2026年1月任三门峡市湖滨区委书记，2026年4月兼任湖滨区人武部党委第一书记"},
    # 袁锐锋 — 更早的职务
    {"person_id": 5, "org_id": 7, "title": "义马市人武部党委第一书记", "start_date": "2023-07", "end_date": "2025-12", "rank": "", "note": ""},
    # 何军 — 更早义马市委书记
    {"person_id": 6, "org_id": 1, "title": "义马市委书记", "start_date": "未知", "end_date": "未知", "rank": "正县级", "note": "何军曾任义马市委书记，后由袁锐锋接任"},
]

relationships = [
    # 姚振波 — 袁锐锋 (书记前后任)
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "姚振波接替袁锐锋担任义马市委书记", "overlap_org": "中共义马市委员会", "overlap_period": "2026"},
    # 姚振波 — 赵麒 (书记+市长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "姚振波任市委书记、赵麒任市长，党政正职搭档", "overlap_org": "义马市", "overlap_period": "2026-"},
    # 袁锐锋 — 姚振波 (市长升书记)
    {"person_a": 5, "person_b": 1, "type": "predecessor_successor", "context": "袁锐锋任市委书记时姚振波任市长，后姚振波接任书记", "overlap_org": "义马市", "overlap_period": "2023-2026"},
    # 袁锐锋 — 何军 (书记前后任)
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "何军任义马市委书记，后由袁锐锋接任", "overlap_org": "中共义马市委员会", "overlap_period": "2023"},
    # 张光明 — 邹晓东 (人大+政协正职)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "张光明任人大主任、邹晓东任政协主席，同为四套班子正职", "overlap_org": "义马市", "overlap_period": "2026-"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    staging = Path(__file__).parent
    db_path = staging / "义马市_network.db"
    gexf_path = staging / "义马市_network.gexf"

    run_build(
        slug="义马市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"Build complete: {db_path}, {gexf_path}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")
