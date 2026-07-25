#!/usr/bin/env python3
"""Build script for 东昌府区 (Dongchangfu District, Liaocheng, Shandong) leadership network.

Generated: 2026-07-26
Level: 市辖区
Province: 山东省
Parent City: 聊城市
Targets: 区委书记 & 区长

Research Note:
  Web access was severely degraded throughout the investigation:
    - Exa search API: rate-limited
    - Baidu search/Baike: 403/captcha blocked
    - Government site (www.dongchangfu.gov.cn): transport timeout/unreachable
    - Jina Reader: timeout
    - Google/Bing/DuckDuckGo: transport errors
    - So.com/search: captcha blocked
    - 央视网搜索: returned results but no leadership information
    - Wikipedia (zh): accessible, provided district geography only

  No leadership data could be independently verified via web sources.
  All person entries are marked with confidence=unverified.
  This is a "partial evidence" artifact — structurally valid but requires
  web-based verification when access is restored.

Sources:
  - https://zh.wikipedia.org/wiki/东昌府区 (district geography only)
  - https://www.dongchangfu.gov.cn/ (unreachable — government leadership page)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path
from datetime import datetime

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA — All entries unverified due to no web access
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders (NAMES UNVERIFIED — no web access) ──
    {
        "id": 1,
        "name": "【待查】东昌府区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东昌府区委书记（待查）",
        "current_org": "中共聊城市东昌府区委员会",
        "source": "GAP — 区委书记姓名未确认。已知前任书记马军权（约2021年上任），当前在职者需通过聊城市委组织部任前公示或区政府官网补充。区政府网站 www.dongchangfu.gov.cn 无法访问。",
    },
    {
        "id": 2,
        "name": "【待查】东昌府区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东昌府区委副书记、区长（待查）",
        "current_org": "聊城市东昌府区人民政府",
        "source": "GAP — 区长姓名未确认。需通过区政府官网或聊城市委组织部任前公示补充。",
    },

    # ── Known Previous Leaders (for reference, unverified) ──
    {
        "id": 3,
        "name": "马军权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任东昌府区委书记（约2021-2024/2025年任职，当前去向待查）",
        "current_org": "中共聊城市东昌府区委员会（前任）",
        "source": "GAP — 马军权曾任东昌府区委书记（约2021年起），具体任职起止时间和当前去向需通过聊城市委组织部公示确认。区政府网站无法访问。",
    },
    {
        "id": 4,
        "name": "江绍华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾任东昌府区长（约2019-2021年任职，当前去向待查）",
        "current_org": "聊城市东昌府区人民政府（前任）",
        "source": "GAP — 江绍华曾任东昌府区长，后马军权接任区委书记时江绍华去向待查。可能需要通过聊城市委公示核实。",
    },
]

# ── Organizations ──
ORGANIZATIONS = [
    {"id": 1, "name": "中共聊城市东昌府区委员会", "type": "党委",
     "level": "县处级", "parent": "中共聊城市委员会", "location": "山东省聊城市东昌府区"},
    {"id": 2, "name": "聊城市东昌府区人民政府", "type": "政府",
     "level": "县处级", "parent": "聊城市人民政府", "location": "山东省聊城市东昌府区"},
    {"id": 3, "name": "聊城市东昌府区纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共聊城市东昌府区委员会", "location": "山东省聊城市东昌府区"},
    {"id": 4, "name": "中共聊城市东昌府区委组织部", "type": "党委",
     "level": "县处级", "parent": "中共聊城市东昌府区委员会", "location": "山东省聊城市东昌府区"},
    {"id": 5, "name": "中共聊城市东昌府区委宣传部", "type": "党委",
     "level": "县处级", "parent": "中共聊城市东昌府区委员会", "location": "山东省聊城市东昌府区"},
    {"id": 6, "name": "聊城市东昌府区人大常委会", "type": "人大",
     "level": "县处级", "parent": "聊城市人大常委会", "location": "山东省聊城市东昌府区"},
    {"id": 7, "name": "政协聊城市东昌府区委员会", "type": "政协",
     "level": "县处级", "parent": "政协聊城市委员会", "location": "山东省聊城市东昌府区"},
    {"id": 8, "name": "聊城市东昌府区人民检察院", "type": "事业单位",
     "level": "县处级", "parent": "聊城市人民检察院", "location": "山东省聊城市东昌府区"},
    {"id": 9, "name": "聊城市东昌府区人民法院", "type": "事业单位",
     "level": "县处级", "parent": "聊城市中级人民法院", "location": "山东省聊城市东昌府区"},
    {"id": 10, "name": "聊城市委", "type": "党委",
     "level": "地厅级", "parent": "中共山东省委", "location": "山东省聊城市"},
    {"id": 11, "name": "聊城市人民政府", "type": "政府",
     "level": "地厅级", "parent": "山东省人民政府", "location": "山东省聊城市"},
]

# ── Positions (Placeholder — verified names needed) ──
POSITIONS = [
    # Current leaders (names pending)
    {"person_id": 1, "org_id": 1, "title": "东昌府区委书记",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "【待查】姓名未知，主持区委全面工作"},
    {"person_id": 2, "org_id": 2, "title": "东昌府区委副书记、区长",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "【待查】姓名未知，主持区政府全面工作"},

    # Known previous leaders
    {"person_id": 3, "org_id": 1, "title": "东昌府区委书记",
     "start_date": "2021(约)", "end_date": "", "rank": "县处级正职",
     "note": "马军权，前任区委书记。具体任职起止时间和当前去向待查"},
    {"person_id": 4, "org_id": 2, "title": "东昌府区委副书记、区长",
     "start_date": "2019(约)", "end_date": "2021(约)", "rank": "县处级正职",
     "note": "江绍华，前任区长。去向待查"},
]

# ── Relationships (Placeholder) ──
RELATIONSHIPS = [
    # Previous leader relationships (based on succession)
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "马军权接替江绍华（或另有任命安排），前后任关系",
     "overlap_org": "中共聊城市东昌府区委员会", "overlap_period": "2021(约)"},
]

# fmt: on

# ═══════════════════════════════════════════════════
# RUNTIME
# ═══════════════════════════════════════════════════

SLUG = "东昌府区"
BASE = Path(__file__).resolve().parent.parent.parent.parent  # repo root
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"


def main():
    print(f"═══ Building {SLUG} leadership network ═══")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()
    print("  ⚠  RESEARCH NOTE: All data is unverified due to complete web access")
    print("     restriction during the investigation period. No Baidu, government")
    print("     website, or news sources were accessible.")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"  ✓ Database: {DB_PATH}")
    print(f"  ✓ GEXF:     {GEXF_PATH}")
    print(f"═══ Build complete ═══")


if __name__ == "__main__":
    main()
