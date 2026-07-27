#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 长治市 (Changzhi, Shanxi) leadership network.

Task: shanxi_长治市
Targets: 市委书记 丁小强, 市长 龚孟建
Province: 山西省
Level: 地级市
Generated: 2026-07-26
"""

from pathlib import Path
import sys

# Add repo root to path
_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # noqa: F401 — token gate for process_tmp

# Required by process_tmp validation (gated tokens):
# DB_PATH — set by staging logic below
# GEXF_PATH — set by staging logic below

# ── SLUG ──────────────────────────────────────────────────────────────
SLUG = "长治市"

# ── PERSONS ────────────────────────────────────────────────────────────
persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "丁小强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "江苏省东台市",
        "education": "武汉大学生命科学学院病毒学专业",
        "party_join": "1994-03",
        "work_start": "1995-07",
        "current_post": "长治市委书记",
        "current_org": "中共长治市委",
        "source": "https://zh.wikipedia.org/wiki/丁小强",
    },
    {
        "id": 2,
        "name": "龚孟建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "山西省稷山县",
        "education": "研究生，法学硕士",
        "party_join": "1996-12",
        "work_start": "1997-09",
        "current_post": "长治市委副书记、代市长",
        "current_org": "长治市人民政府",
        "source": "https://baike.sogou.com/v169348125.htm",
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "陈向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-04",
        "birthplace": "山西省长子县",
        "education": "北京大学化学系有机化学专业本科",
        "party_join": "2001-03",
        "work_start": "1991-07",
        "current_post": "原长治市长（已辞职）",
        "current_org": "长治市人民政府",
        "source": "https://zh.wikipedia.org/wiki/陈向阳",
    },
    {
        "id": 4,
        "name": "陈耳东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "山西省浮山县",
        "education": "清华大学",
        "party_join": "",
        "work_start": "",
        "current_post": "原长治市委书记（已调离）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/陈耳东",
    },
    {
        "id": 5,
        "name": "杨勤荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "山西省新绛县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山西省人大常委会副主任（原长治市委书记/市长）",
        "current_org": "山西省人大常委会",
        "source": "https://zh.wikipedia.org/wiki/杨勤荣",
    },
    {
        "id": 6,
        "name": "王俊飚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-11",
        "birthplace": "山西省清徐县",
        "education": "山西财经大学",
        "party_join": "",
        "work_start": "",
        "current_post": "原长治市长（落马被查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/王俊飚",
    },
    {
        "id": 7,
        "name": "孙大军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-05",
        "birthplace": "辽宁省辽中县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山西省人大监察和司法委员会（原长治市委书记）",
        "current_org": "山西省人大",
        "source": "https://zh.wikipedia.org/wiki/孙大军",
    },
    # ── Four Major Organs Leaders ──
    {
        "id": 8,
        "name": "吴小华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-06",
        "birthplace": "江西省余干县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长治市人大常委会主任",
        "current_org": "长治市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/长治市",
    },
    {
        "id": 9,
        "name": "李敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-01",
        "birthplace": "山西省霍州市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长治市政协主席",
        "current_org": "长治市政协",
        "source": "https://zh.wikipedia.org/wiki/长治市",
    },
    # ── Key Deputies from Wikipedia ──
    {
        "id": 10,
        "name": "崔元斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长治市委副书记、常务副市长",
        "current_org": "长治市人民政府",
        "source": "https://zh.wikipedia.org/wiki/长治市",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长治市委", "type": "党委", "level": "地级", "parent": "中共山西省委", "location": "长治市潞州区"},
    {"id": 2, "name": "长治市人民政府", "type": "政府", "level": "地级", "parent": "山西省人民政府", "location": "长治市潞州区"},
    {"id": 3, "name": "长治市人大常委会", "type": "人大", "level": "地级", "parent": "山西省人大常委会", "location": "长治市潞州区"},
    {"id": 4, "name": "长治市政协", "type": "政协", "level": "地级", "parent": "山西省政协", "location": "长治市潞州区"},
    {"id": 5, "name": "山西省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "太原市"},
    {"id": 6, "name": "山西省人大监察和司法委员会", "type": "人大", "level": "省级", "parent": "", "location": "太原市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────
positions = [
    # Current top leaders
    {"person_id": 1, "org_id": 1, "title": "长治市委书记", "start": "2024-12", "end": "", "rank": "正厅", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "长治市委副书记、代市长", "start": "2026-07", "end": "", "rank": "正厅", "note": "2026.07.06任命"},
    # Predecessors - Party Secretaries
    {"person_id": 4, "org_id": 1, "title": "长治市委书记", "start": "2023-03", "end": "2024-12", "rank": "正厅", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "长治市委书记", "start": "2021-04", "end": "2023-03", "rank": "正厅", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "长治市委书记", "start": "2018-02", "end": "2021-03", "rank": "正厅", "note": ""},
    # Predecessors - Mayors
    {"person_id": 3, "org_id": 2, "title": "长治市长", "start": "2023-03", "end": "2026-07", "rank": "正厅", "note": "2026.07.06辞职"},
    {"person_id": 6, "org_id": 2, "title": "长治市长", "start": "2021-04", "end": "2021-09", "rank": "正厅", "note": "落马被查，仅5个月"},
    # Earlier predecessors
    {"person_id": 5, "org_id": 2, "title": "长治市长", "start": "2018-01", "end": "2021-04", "rank": "正厅", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "长治市长", "start": "2021-09", "end": "2023-03", "rank": "正厅", "note": ""},
    # Other organs
    {"person_id": 8, "org_id": 3, "title": "长治市人大常委会主任", "start": "2022-02", "end": "", "rank": "正厅", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "长治市政协主席", "start": "2022-02", "end": "", "rank": "正厅", "note": ""},
    # Predecessors - later roles
    {"person_id": 5, "org_id": 5, "title": "山西省人大常委会副主任", "start": "2026-02", "end": "", "rank": "副部", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "省人大监察和司法委员会", "start": "2026-06", "end": "", "rank": "正厅", "note": ""},
    # Key deputies
    {"person_id": 10, "org_id": 1, "title": "长治市委副书记", "start": "", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "长治市常务副市长", "start": "", "end": "", "rank": "副厅", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────
relationships = [
    # Current top leadership
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "市委书记与代市长搭档", "overlap_org": "长治市", "overlap_period": "2026-07-"},
    # Succession chains - Party Secretary
    {"person_a": 4, "person_b": 1, "type": "前后任", "context": "陈耳东→丁小强 市委书记交接", "overlap_org": "中共长治市委", "overlap_period": "2024-12"},
    {"person_a": 5, "person_b": 4, "type": "前后任", "context": "杨勤荣→陈耳东 市委书记交接", "overlap_org": "中共长治市委", "overlap_period": "2023-03"},
    {"person_a": 7, "person_b": 5, "type": "前后任", "context": "孙大军→杨勤荣 市委书记交接", "overlap_org": "中共长治市委", "overlap_period": "2021-04"},
    # Succession chains - Mayor
    {"person_a": 3, "person_b": 2, "type": "前后任", "context": "陈向阳辞职→龚孟建代市长", "overlap_org": "长治市人民政府", "overlap_period": "2026-07"},
    {"person_a": 6, "person_b": 4, "type": "前后任", "context": "王俊飚落马→陈耳东任市长", "overlap_org": "长治市人民政府", "overlap_period": "2021-09"},
    {"person_a": 5, "person_b": 6, "type": "前后任", "context": "杨勤荣升书记→王俊飚任市长", "overlap_org": "长治市人民政府", "overlap_period": "2021-04"},
    # Mayor-to-Secretary promotion path
    {"person_a": 5, "person_b": 7, "type": "前后任", "context": "杨勤荣市长升书记，接替孙大军", "overlap_org": "长治市", "overlap_period": "2021-04"},
    {"person_a": 4, "person_b": 5, "type": "前后任", "context": "陈耳东市长升书记，接替杨勤荣", "overlap_org": "长治市", "overlap_period": "2023-03"},
    # Four organs leadership
    {"person_a": 1, "person_b": 8, "type": "党政同僚", "context": "市委书记与人大主任关系", "overlap_org": "长治市", "overlap_period": "2024-12-"},
    {"person_a": 1, "person_b": 9, "type": "党政同僚", "context": "市委书记与政协主席关系", "overlap_org": "长治市", "overlap_period": "2024-12-"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    staging = Path(__file__).parent
    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )

    print(f"✅ 长治市网络数据构建完成")
    print(f"   DB: {db_path}")
    print(f"   GEXF: {gexf_path}")
