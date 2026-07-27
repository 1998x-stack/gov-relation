#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 肃宁县 leadership network.

Data source: www.suning.gov.cn (official government website)
Information currency: 2026-07-24 (current as of July 2026)

Core leaders confirmed from official news:
- 县委书记 穆春江 (confirmed 2026-07-22 via县委常委会召开扩大会议)
- 县委副书记、县长 高沛烜 (confirmed 2026-07-01 via "两优一先"表彰大会)
"""
from pathlib import Path

from gov_relation.runner import run_build  # uses sqlite3 internally

SLUG = "肃宁县"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # === 县委常委 ===
    {
        "id": 1, "name": "穆春江", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "肃宁县委书记",
        "current_org": "中共肃宁县委员会",
        "source": "https://www.suning.gov.cn/suning/c101086/202607/5a5c309cd0bc4b1ca827102c6b197b9d.shtml",
    },
    {
        "id": 2, "name": "高沛烜", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "肃宁县委副书记、县长",
        "current_org": "肃宁县人民政府",
        "source": "https://www.suning.gov.cn/suning/c101086/202607/8f824ad986ab4caf80602d783717b2e3.shtml",
    },
    # === 前任 ===
    {
        "id": 3, "name": "王志乾", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "训练数据（前任县委书记，约~2025年离任）",
    },
    {
        "id": 4, "name": "杨玲", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "训练数据（前任县长，约~2025年离任）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共肃宁县委员会", "type": "党委",
        "level": "县处级", "parent": "中共沧州市委员会", "location": "肃宁县",
    },
    {
        "id": 2, "name": "肃宁县人民政府", "type": "政府",
        "level": "县处级", "parent": "沧州市人民政府", "location": "肃宁县",
    },
    {
        "id": 3, "name": "中共沧县委员会", "type": "党委",
        "level": "县处级", "parent": "中共沧州市委员会", "location": "沧县",
    },
    {
        "id": 4, "name": "沧县人民政府", "type": "政府",
        "level": "县处级", "parent": "沧州市人民政府", "location": "沧县",
    },
    {
        "id": 5, "name": "沧州市人民政府", "type": "政府",
        "level": "地厅级", "parent": "河北省人民政府", "location": "沧州市",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────
positions = [
    # 穆春江 — 县委书记（现任）
    {"person_id": 1, "org_id": 1, "title": "肃宁县委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "confirmed via official news 2026-07-22"},
    # 穆春江 — 此前为沧县县长
    {"person_id": 1, "org_id": 4, "title": "沧县县长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "plausible from open_gaps.md - 前沧县县长 (confidence: plausible)"},
    # 高沛烜 — 县长（现任）
    {"person_id": 2, "org_id": 2, "title": "肃宁县委副书记、县长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "confirmed via official news 2026-07-01"},
    # 前任
    {"person_id": 3, "org_id": 1, "title": "肃宁县委书记（前任）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任县委书记，约2025年前离任（unverified）"},
    {"person_id": 4, "org_id": 2, "title": "肃宁县县长（前任）",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "前任县长，约2025年前离任（unverified）"},
]

# ── Relationships ─────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate", "context": "县委书记与县长（党政正职搭档）",
        "overlap_org": "肃宁县", "overlap_period": "2026-",
    },
]

# ── Run Build ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
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
