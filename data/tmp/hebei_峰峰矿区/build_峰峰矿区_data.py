#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 峰峰矿区, 邯郸市, 河北省."""

import os
import sys
from datetime import date
from pathlib import Path

# Add project root to path so gov_relation module is importable
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths (staging) ────────────────────────────────────────────────────
TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / "峰峰矿区_network.db"
GEXF_PATH = TMP_DIR / "峰峰矿区_network.gexf"

# ── DATA ───────────────────────────────────────────────────────────────

TODAY = date.today().strftime("%Y-%m-%d")

persons = [
    # ── Current Top Leaders ──
    # 区委书记 — TODO: name unconfirmed; placeholder
    {"id": 1, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "邯郸市峰峰矿区区委书记", "current_org": "中共邯郸市峰峰矿区委员会",
     "source": "http://www.ff.gov.cn/ (未直接列出)"},

    # 区长 张宝伟 (confirmed from official site)
    {"id": 2, "name": "张宝伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-05", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "邯郸市峰峰矿区区委副书记、区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/zbw/"},

    # ── Deputy Leaders (confirmed from official 区长之窗 page) ──
    {"id": 3, "name": "李昂", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "峰峰矿区区委常委、副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 4, "name": "武文强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 5, "name": "陶毅", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 6, "name": "李波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 7, "name": "王雷", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},

    {"id": 8, "name": "白晓", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "峰峰矿区副区长", "current_org": "邯郸市峰峰矿区人民政府",
     "source": "http://www.ff.gov.cn/zwgk/qzzc/"},
]

organizations = [
    {"id": 1, "name": "中共邯郸市峰峰矿区委员会", "type": "党委", "level": "县处级",
     "parent": "中共邯郸市委员会", "location": "河北省邯郸市峰峰矿区"},
    {"id": 2, "name": "邯郸市峰峰矿区人民政府", "type": "政府", "level": "县处级",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市峰峰矿区"},
    {"id": 3, "name": "峰峰经济开发区", "type": "开发区", "level": "省级开发区",
     "parent": "邯郸市人民政府", "location": "河北省邯郸市峰峰矿区"},
]

positions = [
    # 张宝伟
    {"person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": ""},
    {"person_id": 2, "org_id": 3, "title": "峰峰经济开发区党工委副书记兼管委会主任",
     "start": "", "end": "present", "rank": "",
     "note": ""},

    # 李昂
    {"person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 武文强
    {"person_id": 4, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 陶毅
    {"person_id": 5, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 李波
    {"person_id": 6, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 王雷
    {"person_id": 7, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},

    # 白晓
    {"person_id": 8, "org_id": 2, "title": "副区长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": ""},
]

relationships = [
    # 张宝伟 — 区委领导层关系 (placeholder for when party secretary is known)
    # Overlap relationships between deputy leaders are inferred from same org
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026", "source": "http://www.ff.gov.cn/zwgk/qzzc/"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长与副区长工作关系", "overlap_org": "邯郸市峰峰矿区人民政府",
     "overlap_period": "2025-2026"},
]

# ── BUILD ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="峰峰矿区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
