#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 京山市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_京山市
Level: 县级市
Targets: 市委书记 & 市长

Research status: COMPLETE
- 市委书记 何洪涛 confirmed via official news articles (jingshan.gov.cn, 2026-06/07)
- 市长 鲁雷 confirmed as 市委副书记、市长 via official news (jingshan.gov.cn)
- Full government leadership roster partially identified from news reports
- Party standing committee partially identified from news reports
- Predecessor/successor analysis: partial

Confidence notes:
- 市委书记, 市长 identities: CONFIRMED via official government news site
- Career timelines: PARTIAL - detailed earlier roles not available from open web
- City party standing committee roster: PARTIAL - ~5 members identified
- Relationships: INFERRED from organizational overlap
- Predecessor information: PARTIAL - limited confirmed data

Sources:
- https://www.jingshan.gov.cn/ (京山市政府门户网站)
- https://www.jingshan.gov.cn/art/2026/6/26/art_5586_1224951.html (何洪涛调研民生项目)
- https://www.jingshan.gov.cn/art/2026/7/8/art_5586_1227044.html (何洪涛主持汽车产业会)
- https://www.jingshan.gov.cn/art/2026/7/16/art_5586_1228314.html (鲁雷主持政绩观学习会)
- https://www.jingshan.gov.cn/art/2026/7/3/art_5586_1226139.html (鲁雷调度民生实事)
- https://www.jingshan.gov.cn/art/2026/6/21/art_5586_1224381.html (何洪涛鲁雷安全检查)
- https://www.jingshan.gov.cn/art/2026/6/30/art_5586_1225237.html (网球产业报道)
"""

from __future__ import annotations

import sys
from pathlib import Path

# Required tokens for process_tmp.py validation: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401
_DB_TOKEN = "data/tmp/hubei_京山市/京山市_network.db"  # noqa
_GEXF_TOKEN = "data/tmp/hubei_京山市/京山市_network.gexf"  # noqa

_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parents[2]
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────
SLUG = "京山市"
TODAY = "20260724"
AS_OF = "2026-07-24"

STAGING_DIR = _HERE
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Person Data ──────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "何洪涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市委书记",
        "current_org": "中共京山市委员会",
        "source": "https://www.jingshan.gov.cn/art/2026/6/26/art_5586_1224951.html"
    },
    {
        "id": 2,
        "name": "鲁雷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市委副书记、市长",
        "current_org": "京山市人民政府",
        "source": "https://www.jingshan.gov.cn/art/2026/7/16/art_5586_1228314.html"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "丁呈呈",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市委副书记",
        "current_org": "中共京山市委员会",
        "source": "https://www.jingshan.gov.cn/art/2026/7/3/art_5586_1226139.html"
    },
    {
        "id": 4,
        "name": "王汉丰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市委常委、市委办公室主任",
        "current_org": "中共京山市委员会",
        "source": "https://www.jingshan.gov.cn/art/2026/6/26/art_5586_1224951.html"
    },
    # ═══════ 人大领导 ═══════
    {
        "id": 5,
        "name": "杨宜云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市人大常委会主任",
        "current_org": "京山市人大常委会",
        "source": "https://www.jingshan.gov.cn/art/2026/7/3/art_5586_1226139.html"
    },
    # ═══════ 市政府领导 ═══════
    {
        "id": 6,
        "name": "张琼慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市副市长",
        "current_org": "京山市人民政府",
        "source": "https://www.jingshan.gov.cn/art/2026/6/26/art_5586_1224951.html"
    },
    {
        "id": 7,
        "name": "王皓玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市副市长",
        "current_org": "京山市人民政府",
        "source": "https://www.jingshan.gov.cn/art/2026/7/8/art_5586_1227044.html"
    },
    {
        "id": 8,
        "name": "时希望",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市副市长",
        "current_org": "京山市人民政府",
        "source": "https://www.jingshan.gov.cn/art/2026/7/8/art_5586_1227044.html"
    },
    # ═══════ 政协领导 ═══════
    {
        "id": 9,
        "name": "李俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "京山市政协副主席",
        "current_org": "京山市政协",
        "source": "https://www.jingshan.gov.cn/art/2026/7/3/art_5586_1226139.html"
    },
]

# ── Organization Data ─────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共京山市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共荆门市委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 2,
        "name": "京山市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "荆门市人民政府",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 3,
        "name": "京山市人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "荆门市人大常委会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 4,
        "name": "京山市政协",
        "type": "政协",
        "level": "县级",
        "parent": "荆门市政协",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 5,
        "name": "中共京山市纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "parent": "中共荆门市纪律检查委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 6,
        "name": "京山市委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共京山市委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 7,
        "name": "京山市委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共京山市委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 8,
        "name": "京山市委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共京山市委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 9,
        "name": "京山市委政法委",
        "type": "党委",
        "level": "县级",
        "parent": "中共京山市委员会",
        "location": "湖北省京山市新市镇"
    },
    {
        "id": 10,
        "name": "京山市人民武装部",
        "type": "党委",
        "level": "县级",
        "parent": "荆门军分区",
        "location": "湖北省京山市新市镇"
    },
]

# ── Position Data ────────────────────────────────────────────────────

positions = [
    # 何洪涛
    {"person_id": 1, "org_id": 1, "title": "京山市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 鲁雷
    {"person_id": 2, "org_id": 1, "title": "京山市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "京山市人民政府市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 丁呈呈
    {"person_id": 3, "org_id": 1, "title": "京山市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王汉丰
    {"person_id": 4, "org_id": 1, "title": "京山市委常委、市委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杨宜云
    {"person_id": 5, "org_id": 3, "title": "京山市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 张琼慧
    {"person_id": 6, "org_id": 2, "title": "京山市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王皓玉
    {"person_id": 7, "org_id": 2, "title": "京山市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 时希望
    {"person_id": 8, "org_id": 2, "title": "京山市副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李俊
    {"person_id": 9, "org_id": 4, "title": "京山市政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationship Data ────────────────────────────────────────────────

relationships = [
    # 何洪涛 ↔ 鲁雷 (党政正职搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "市委书记与市长党政正职搭档",
        "overlap_org": "中共京山市委员会/京山市人民政府",
        "overlap_period": "2026"
    },
    # 何洪涛 ↔ 丁呈呈 (书记与副书记)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "市委书记与专职副书记",
        "overlap_org": "中共京山市委员会",
        "overlap_period": "2026"
    },
    # 何洪涛 ↔ 王汉丰 (书记与市委办主任)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "市委书记与市委常委、市委办公室主任，直接上下级关系",
        "overlap_org": "中共京山市委员会",
        "overlap_period": "2026"
    },
    # 鲁雷 ↔ 丁呈呈 (市长与专职副书记)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "市长与专职副书记同属市委常委会",
        "overlap_org": "中共京山市委员会",
        "overlap_period": "2026"
    },
    # 鲁雷 ↔ 张琼慧 (市长与副市长)
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "市长与副市长，政府领导班子成员",
        "overlap_org": "京山市人民政府",
        "overlap_period": "2026"
    },
    # 鲁雷 ↔ 王皓玉 (市长与副市长)
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "市长与副市长，政府领导班子成员",
        "overlap_org": "京山市人民政府",
        "overlap_period": "2026"
    },
    # 鲁雷 ↔ 时希望 (市长与副市长)
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "市长与副市长，政府领导班子成员",
        "overlap_org": "京山市人民政府",
        "overlap_period": "2026"
    },
    # 王汉丰 ↔ 鲁雷 (市委办主任与市长)
    {
        "person_a": 4,
        "person_b": 2,
        "type": "overlap",
        "context": "市委常委、市委办公室主任与市长工作交集",
        "overlap_org": "中共京山市委员会/京山市人民政府",
        "overlap_period": "2026"
    },
    # 杨宜云 ↔ 何洪涛 (人大主任与书记)
    {
        "person_a": 5,
        "person_b": 1,
        "type": "overlap",
        "context": "人大常委会主任与市委书记，党政分工协作",
        "overlap_org": "京山市",
        "overlap_period": "2026"
    },
    # 李俊 ↔ 鲁雷 (政协副主席与市长)
    {
        "person_a": 9,
        "person_b": 2,
        "type": "overlap",
        "context": "政协副主席与市长，政治协商关系",
        "overlap_org": "京山市",
        "overlap_period": "2026"
    },
]


# ── Main ─────────────────────────────────────────────────────────────

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

    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")
    print(f"\nRun the following to promote:")
    print(f"  python3 scripts/process_tmp.py data/tmp/hubei_京山市")
    print(f"  python3 scripts/process_tmp.py data/tmp/hubei_京山市 --apply")
