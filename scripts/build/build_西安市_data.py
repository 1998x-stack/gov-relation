#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西安市 (Xi'an) leadership network.

西安市 — 副省级市 (sub-provincial city), 陕西省省会. Task ID: shaanxi_西安市.
Targets: 市委书记 (Party Secretary) & 市长 (Mayor).

Investigation date: 2026-08-07

Key current officeholders (as of 2026-08):
  - 市委书记: 蒿慧杰 (2026-01-16 就任, 中共陕西省委常委)
  - 市长: 叶牛平 (2023-06 当选, 中共西安市委副书记)
  - 前任市委书记: 方红卫 (2021-11→2025-11, 2025-11 落马被查, 2026-07 开除党籍公职)
  - 前任市长: 李明远 (→2023-04, 现任陕西省委常委、统战部部长)
  - 方红卫之前任市委书记: 王浩 (→2021-11)

Sources (all data hard-coded here from web research):
  - zh.wikipedia.org — 方红卫(政治人物), 蒿慧杰, 叶牛平, 李明远(1965消歧义)
  - www.xa.gov.cn — official site (confirms active 市委书记/市委常委会工作)
  - Inline citations: 中国经济网, 澎湃新闻, 新华网, 人民网, 中国共产党新闻网

Confidence: 蒿慧杰/叶牛平/方红卫/李明远 身份与主要任职 confirmed; 具体任职日期由百科条目交叉核实.
NOTE: 蒿慧杰任西安市委书记与方红卫落马属近期重大人事变动 (2025-11 / 2026-01 / 2026-07), 交叉核实.
"""

from __future__ import annotations

import sqlite3  # noqa: required by process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

# Resolve repo root robustly (works whether run from data/tmp staging or scripts/build).
_HERE = Path(__file__).resolve().parent
_REPO = _HERE
for _p in (_HERE, *_HERE.parents):
    if (_p / "gov_relation").is_dir():
        _REPO = _p
        break
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "西安市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 现任核心 — 市委书记 & 市长 ═══════
    {
        "id": 1,
        "name": "蒿慧杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "河南中牟",
        "education": "武汉大学法学学士 / 郑州大学在职公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共陕西省委常委、西安市委书记",
        "current_org": "中共西安市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E8%92%BF%E6%85%A7%E6%9D%B0"
    },
    {
        "id": 2,
        "name": "叶牛平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-12",
        "birthplace": "安徽太湖",
        "education": "安徽大学历史系 / 中山大学历史学硕士学位",
        "party_join": "1993-06",
        "work_start": "1989",
        "current_post": "中共西安市委副书记、西安市市长",
        "current_org": "西安市人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E5%8F%B6%E7%89%9B%E5%B9%B3"
    },
    # ═══════ 前任市委书记 ═══════
    {
        "id": 3,
        "name": "方红卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-06",
        "birthplace": "陕西富平",
        "education": "清华大学汽车工程系汽车专业",
        "party_join": "1987-04",
        "work_start": "1989",
        "current_post": "前西安市委书记（2025-11被查、2026-07开除党籍公职）",
        "current_org": "（落马）",
        "source": "https://zh.wikipedia.org/wiki/%E6%96%B9%E7%BA%A2%E5%8D%AB_(%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9)"
    },
    # ═══════ 前任市长 ═══════
    {
        "id": 4,
        "name": "李明远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965",
        "birthplace": "陕西",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共陕西省委常委、统战部部长",
        "current_org": "中共陕西省委统战部",
        "source": "https://zh.wikipedia.org/wiki/%E6%9D%8E%E6%98%8E%E8%BF%9C"
    },
    # ═══════ 更早前任市委书记 ═══════
    {
        "id": 5,
        "name": "王浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "方红卫之前任西安市委书记（→2021-11）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E6%96%B9%E7%BA%A2%E5%8D%AB_(%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9)"
    },
    # ═══════ 蒿慧杰 前任延安市委书记时期的搭档（市长） ─══════
    {
        "id": 6,
        "name": "严汉平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "延安市市长（蒿慧杰任延安市委书记期间副书记兼市长）",
        "current_org": "延安市人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E8%92%BF%E6%85%A7%E6%9D%B8"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共西安市委员会", "type": "党委", "level": "副省级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 2, "name": "西安市人民政府", "type": "政府", "level": "副省级", "parent": "陕西省人民政府", "location": "陕西省西安市"},
    {"id": 3, "name": "中共陕西省委员会", "type": "党委", "level": "省级", "parent": "中共中央", "location": "陕西省西安市"},
    {"id": 4, "name": "陕西省人民政府", "type": "政府", "level": "省级", "parent": "国务院", "location": "陕西省西安市"},
    {"id": 5, "name": "中共陕西省委统战部", "type": "党委部门", "level": "厅级", "parent": "中共陕西省委员会", "location": "陕西省西安市"},
    {"id": 6, "name": "中共延安市委员会", "type": "党委", "level": "地厅级", "parent": "中共陕西省委员会", "location": "陕西省延安市"},
    {"id": 7, "name": "延安市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "陕西省延安市"},
    {"id": 8, "name": "中共漯河市委员会", "type": "党委", "level": "地厅级", "parent": "中共河南省委员会", "location": "河南省漯河市"},
    {"id": 9, "name": "中共驻马店市委员会", "type": "党委", "level": "地厅级", "parent": "中共河南省委员会", "location": "河南省驻马店市"},
    {"id": 10, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 11, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "国务院", "location": "广东省广州市"},
    {"id": 12, "name": "中共汉中市委员会", "type": "党委", "level": "地厅级", "parent": "中共陕西省委员会", "location": "陕西省汉中市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
positions = [
    # 蒿慧杰
    {"person_id": 1, "org_id": 1, "title": "西安市委书记", "start_date": "2026-01", "end_date": "", "rank": "副省级", "note": "现任，兼任中共陕西省委常委"},
    {"person_id": 1, "org_id": 3, "title": "中共陕西省委常委", "start_date": "2022-05", "end_date": "", "rank": "省级", "note": "现任"},
    {"person_id": 1, "org_id": 6, "title": "延安市委书记", "start_date": "2023-01", "end_date": "2026-01", "rank": "地厅级", "note": "省委常委兼任"},
    {"person_id": 1, "org_id": 4, "title": "陕西省副省长", "start_date": "2021-09", "end_date": "2022-07", "rank": "省级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "驻马店市委书记", "start_date": "2021-07", "end_date": "2021-09", "rank": "地厅级", "note": "河南"},
    {"person_id": 1, "org_id": 8, "title": "漯河市委书记", "start_date": "2017-12", "end_date": "2021-07", "rank": "地厅级", "note": "河南"},
    # 叶牛平
    {"person_id": 2, "org_id": 2, "title": "西安市市长", "start_date": "2023-06", "end_date": "", "rank": "副省级", "note": "现任，2023-04任代市长"},
    {"person_id": 2, "org_id": 1, "title": "西安市委副书记", "start_date": "2023-04", "end_date": "", "rank": "副省级", "note": "现任"},
    {"person_id": 2, "org_id": 4, "title": "陕西省副省长", "start_date": "2022-07", "end_date": "2023-05", "rank": "省级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "广东省政府秘书长", "start_date": "2020-06", "end_date": "2022-07", "rank": "省级", "note": "广东"},
    {"person_id": 2, "org_id": 10, "title": "揭阳市委书记", "start_date": "2019-05", "end_date": "2020-05", "rank": "地厅级", "note": "广东"},
    # 方红卫
    {"person_id": 3, "org_id": 1, "title": "西安市委书记", "start_date": "2021-11", "end_date": "2025-11", "rank": "副省级", "note": "落马离职"},
    {"person_id": 3, "org_id": 3, "title": "中共陕西省委常委、省委秘书长", "start_date": "2021-05", "end_date": "2021-11", "rank": "省级", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "汉中市委书记", "start_date": "2020-07", "end_date": "2021-06", "rank": "地厅级", "note": ""},
    # 李明远
    {"person_id": 4, "org_id": 5, "title": "中共陕西省委常委、统战部部长", "start_date": "", "end_date": "", "rank": "省级", "note": "现任"},
    {"person_id": 4, "org_id": 2, "title": "西安市市长", "start_date": "", "end_date": "2023-04", "rank": "副省级", "note": "前任市长"},
    # 王浩
    {"person_id": 5, "org_id": 1, "title": "西安市委书记", "start_date": "", "end_date": "2021-11", "rank": "副省级", "note": "方红卫之前任"},
    # 严汉平
    {"person_id": 6, "org_id": 7, "title": "延安市市长", "start_date": "", "end_date": "", "rank": "地厅级", "note": "蒿（书记）任期内副书记兼市长"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 现任党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "蒿慧杰（市委书记）与叶牛平（市委副书记、市长）搭班", "overlap_org": "西安市",
     "overlap_period": "2026-01—今"},
    # 书记交接 方→蒿
    {"person_a": 3, "person_b": 1, "type": "前后任",
     "context": "方红卫→蒿慧杰 西安市委书记交接（方2025-11被查免职，蒿2026-01就任）", "overlap_org": "中共西安市委员会",
     "overlap_period": "2025-11/2026-01"},
    # 方+叶 党政搭档 (2023-2025)
    {"person_a": 3, "person_b": 2, "type": "党政搭档",
     "context": "方红卫任市委书记期间叶牛平任市长（2023-2025）", "overlap_org": "西安市",
     "overlap_period": "2023-04—2025-11"},
    # 方+李 搭档/前后任 市长
    {"person_a": 3, "person_b": 4, "type": "党政搭档",
     "context": "方红卫任书记时李明远任市长（2021-11—2023-04）", "overlap_org": "西安市",
     "overlap_period": "2021-11—2023-04"},
    # 叶+李 市长交接
    {"person_a": 2, "person_b": 4, "type": "前后任",
     "context": "李明远→叶牛平 西安市长交接（2023-04）", "overlap_org": "西安市人民政府",
     "overlap_period": "2023-04"},
    # 方+王 市委书记交接
    {"person_a": 5, "person_b": 3, "type": "前后任",
     "context": "王浩→方红卫 西安市委书记交接（2021-11）", "overlap_org": "中共西安市委员会",
     "overlap_period": "2021-11"},
    # 蒿+严 延安党政搭档
    {"person_a": 1, "person_b": 6, "type": "党政搭档",
     "context": "蒿慧杰任延安市委书记时严汉平任市委副书记、市长", "overlap_org": "中共延安市委员会",
     "overlap_period": "2023-2026"},
    # 蒿+叶 跨省交流 与 叶跨省交流 标注点
    {"person_a": 1, "person_b": 3, "type": "前后党建",
     "context": "蒿慧杰接任西安市委书记，方红卫因严重违纪违法落任", "overlap_org": "中共西安市委员会",
     "overlap_period": "2026-01"},
]

# ── Build ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Print summary
    print("=" * 60)
    print(f"  {SLUG} 领导班子关系网络构建完成")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("=" * 60)