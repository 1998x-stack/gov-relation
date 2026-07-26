#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大邑县 (Dayi County), Chengdu, Sichuan.

Research as of July 2026.
Web access severely degraded — see source confidence notes.
"""
import sys, os, sqlite3
from datetime import datetime
# scripts/build/ -> repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from gov_relation.runner import run_build

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DB_PATH = os.path.join(BASE, "data/database/大邑县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/大邑县_network.gexf")

# ══════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════

persons = [
    # ── Current/Recent Top Leaders ──
    {
        "id": 1,
        "name": "连华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大邑县委书记（推定）",
        "current_org": "中共大邑县委员会",
        "source": "https://zh.wikipedia.org/wiki/大邑县悬挂式单轨 (confirmed 县长 2020; 县委书记 inferred 2021-2025)",
    },
    {
        "id": 2,
        "name": "李燎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任大邑县委书记",
        "current_org": "",
        "source": "推定 — 待查（可能调任成都其他职务）",
    },
    {
        "id": 3,
        "name": "余戬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大邑县县长（推定）",
        "current_org": "大邑县人民政府",
        "source": "推定 — 待查",
    },
    # ── Historical Leaders ──
    {
        "id": 10,
        "name": "宋朝华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-05",
        "birthplace": "四川邛崃",
        "education": "温江师范专科学校中文专业",
        "party_join": "",
        "work_start": "",
        "current_post": "四川省人大常委会副主任（已退休，曾任大邑县委书记 1997-2002）",
        "current_org": "四川省人大常委会",
        "source": "https://zh.wikipedia.org/wiki/宋朝华",
    },
    {
        "id": 11,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-07",
        "birthplace": "四川大邑",
        "education": "电子科大工商管理硕士、中央党校经济学在职研究生",
        "party_join": "1986-09",
        "work_start": "1982-12",
        "current_post": "被开除党籍公职（2025-04，曾任大邑县委常委、副县长、副书记 1997-2001）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/李刚_(1965年)",
    },
    {
        "id": 12,
        "name": "曾万明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-01-04",
        "birthplace": "四川成都",
        "education": "西南财经大学农业经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "已故（2021-09-08，曾任大邑县委书记 2002-2005）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/曾万明",
    },
]

# ══════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共大邑县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市委员会",
        "location": "四川省成都市大邑县晋原街道",
    },
    {
        "id": 2,
        "name": "大邑县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "成都市人民政府",
        "location": "四川省成都市大邑县晋原街道桃源大道66号",
    },
    {
        "id": 3,
        "name": "大邑县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "成都市人民代表大会常务委员会",
        "location": "四川省成都市大邑县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议大邑县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "成都市政协",
        "location": "四川省成都市大邑县",
    },
    {
        "id": 5,
        "name": "中国共产党大邑县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市纪律检查委员会",
        "location": "四川省成都市大邑县",
    },
    {
        "id": 6,
        "name": "大邑县电力公司",
        "type": "企业",
        "level": "县处级",
        "location": "四川省成都市大邑县",
    },
]

# ══════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════

positions = [
    # Current Leadership (推定)
    {"person_id": 1, "org_id": 1, "title": "大邑县委书记", "start": "推定 2022-2023", "end": "至今", "rank": "县处级正职",
     "note": "推定 — 连华2020年任县长后可能升任书记; 待任前公示确认"},
    {"person_id": 3, "org_id": 2, "title": "大邑县人民政府县长", "start": "推定 2023-2025", "end": "至今", "rank": "县处级正职",
     "note": "推定 — 接替连华升任书记后的县长空缺"},

    # Confirmed historical positions for 连华
    {"person_id": 1, "org_id": 2, "title": "大邑县委副书记、县长", "start": "最迟 2020-03", "end": "推定 2022-2023", "rank": "县处级正职",
     "note": "confirmed: Wikipedia 大邑县悬挂式单轨 cited 连华 as 县委副书记、县长 in March 2020"},

    # Predecessor
    {"person_id": 2, "org_id": 1, "title": "大邑县委书记", "start": "推定 2016-2021", "end": "推定 2022", "rank": "县处级正职",
     "note": "待查: 李燎可能在大邑县委书记任内调任; 去向待确认"},

    # Historical - 宋朝华
    {"person_id": 10, "org_id": 1, "title": "大邑县委书记", "start": "1997-10", "end": "2002-12", "rank": "县处级正职",
     "note": "confirmed by Wikipedia: 1997年10月任大邑县委书记, 2002年12月转任新津县委书记"},
    {"person_id": 10, "org_id": 2, "title": "大邑县委副书记、代县长", "start": "1997-03", "end": "1997-10", "rank": "县处级正职",
     "note": "confirmed by Wikipedia"},
    {"person_id": 10, "org_id": 1, "title": "大邑县委常委、组织部部长", "start": "", "end": "1997-03", "rank": "县处级副职",
     "note": "confirmed by Wikipedia"},

    # Historical - 李刚
    {"person_id": 11, "org_id": 6, "title": "大邑县电力公司员工", "start": "1982-12", "end": "1990", "rank": "普通员工",
     "note": "confirmed by Wikipedia"},
    {"person_id": 11, "org_id": 1, "title": "大邑县委常委、副县长", "start": "1997-12", "end": "", "rank": "县处级副职",
     "note": "confirmed by Wikipedia"},
    {"person_id": 11, "org_id": 1, "title": "大邑县委副书记", "start": "", "end": "2001-06", "rank": "县处级副职",
     "note": "confirmed by Wikipedia: 2001年6月调任温江县委副书记、县长"},

    # Historical - 曾万明
    {"person_id": 12, "org_id": 1, "title": "大邑县委书记", "start": "2002-12", "end": "2005-05", "rank": "县处级正职",
     "note": "confirmed by Wikipedia: 2002年12月调任大邑县委书记, 2005年5月升任成都市副市长"},
]

# ══════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "连华推定接替李燎任大邑县委书记",
        "overlap_org": "中共大邑县委员会",
        "overlap_period": "推定",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "连华作为县委书记与县长余戬推定搭班子",
        "overlap_org": "大邑县",
        "overlap_period": "推定 2023至今",
    },
    {
        "person_a": 10,
        "person_b": 11,
        "type": "colleague",
        "context": "宋朝华（县委书记）与李刚（县委常委、副县长/副书记）曾在1997-2001年间在大邑县委共事",
        "overlap_org": "中共大邑县委员会",
        "overlap_period": "1997-2001",
    },
    {
        "person_a": 10,
        "person_b": 12,
        "type": "predecessor_successor",
        "context": "宋朝华2002年12月转任新津县委书记后，曾万明接任大邑县委书记",
        "overlap_org": "中共大邑县委员会",
        "overlap_period": "2002",
    },
]

# ══════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug="大邑县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done - staging files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
