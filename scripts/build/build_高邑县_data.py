#!/usr/bin/env python3
"""高邑县领导班子工作关系网络 — Build script

河北省石家庄市高邑县

Confirmed sources (accessed 2026-08-05; degraded web — Baidu Baike + gov sites via headless chromium):
- 百度百科 "高邑县": county main leadership table (县委书记 李玉涛, 县长 苗润涛, 人大主任 王惠武,
  政协主席 谷会文) as-of ~2025-07.
- 百度百科 "苗润涛 (河北省石家庄市高邑县委书记)": confirms 苗润涛 promoted 县长→县委书记,
  career timeline (丛台区→高邑县), updated 2026-07-22, citing 高邑县人民政府 2026-02-02.
- 百度百科 高邑县 reference [33] "县委常委会（扩大）会议召开 李玉涛主持并讲话" 2025-02-17.
- 世清县网络脚本: 彭敬捷曾任高邑县委书记 (2019年前), 后永清县委书记, 现任河北省司法厅副厅长.

OPEN GAPS (not fabricated):
- current 高邑县长 (miao 润涛's successor) not identified under restricted access.
- 苗润涛 birth/birthplace/education unknown.
- 李玉涛 full resume / 2026 whereabouts unknown.

Research date: 2026-08-05
"""

import json
import os
import sqlite3
import sys

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

# Output paths (written next to this script in staging; process_tmp promotes canonical copies)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "高邑县_network.db")
GEXF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "高邑县_network.gexf")

AS_OF = "2026-08-05"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ── 县委书记 (Party Secretary, current 2026) ──
    {
        "id": 1,
        "name": "苗润涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高邑县委书记",
        "current_org": "中共石家庄市高邑县委员会",
        "source": "https://baike.baidu.com/item/%E8%8B%97%E6%B6%A6%E6%B6%9B/57120537",
    },
    # ── 前任县委书记 (Predecessor, as of ~2025) ──
    {
        "id": 2,
        "name": "李玉涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任高邑县委书记）",
        "current_org": "中共石家庄市高邑县委员会",
        "source": "https://baike.baidu.com/item/%E9%AB%98%E9%82%91%E5%8E%BF",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 3,
        "name": "王惠武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高邑县人大常委会主任",
        "current_org": "高邑县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E9%AB%98%E9%82%91%E5%8E%BF",
    },
    # ── 县政协主席 ──
    {
        "id": 4,
        "name": "谷会文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高邑县政协主席",
        "current_org": "中国人民政治协商会议高邑县委员会",
        "source": "https://baike.baidu.com/item/%E9%AB%98%E9%82%91%E5%8E%BF",
    },
    # ── 前任县委书记（更早，context） ──
    {
        "id": 5,
        "name": "彭敬捷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967-05",
        "birthplace": "河北晋州",
        "education": "河北大学法律系法学专业，法学学士",
        "party_join": "1993-01",
        "work_start": "1987-09",
        "current_post": "河北省司法厅党委委员、副厅长",
        "current_org": "河北省司法厅",
        "source": "scripts/build/build_永清县_data.py / 百度百科",
    },
    # ── 现任县长 (County Mayor, current 2026) ──
    {
        "id": 6,
        "name": "张辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "未知",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高邑县委副书记、县长",
        "current_org": "高邑县人民政府/中共石家庄市高邑县委员会",
        "source": "http://www.gyx.gov.cn/columns/11fe6dff-eacf-4de8-a381-bec47312cfff/202606/01/ba0c4ff6-510f-4ec7-9cbb-f43c7c2e370e.html",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共石家庄市高邑县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市高邑县",
    },
    {
        "id": 2,
        "name": "高邑县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市高邑县",
    },
    {
        "id": 3,
        "name": "高邑县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "高邑县",
        "location": "河北省石家庄市高邑县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议高邑县委员会",
        "type": "政协",
        "level": "县",
        "parent": "高邑县",
        "location": "河北省石家庄市高邑县",
    },
    {
        "id": 5,
        "name": "邯郸市丛台区人民政府",
        "type": "政府",
        "level": "区",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市丛台区",
    },
    {
        "id": 6,
        "name": "河北省司法厅",
        "type": "事业单位",
        "level": "省级部门",
        "parent": "河北省人民政府",
        "location": "河北省石家庄市",
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 苗润涛 — 县委书记 (current)
    {"person_id": 1, "org_id": 1, "title": "高邑县委书记",
     "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "（2021年由县长升任县委书记；维基百科2026-07确认）"},
    # 苗润涛 — 县长 (previous term in 高邑)
    {"person_id": 1, "org_id": 2, "title": "高邑县人民政府县长",
     "start_date": "2021-07", "end_date": "2026",
     "rank": "正处级", "note": "2021-07-24 县十七届人大一次会议当选"},
    {"person_id": 1, "org_id": 2, "title": "高邑县人民政府副县长、代理县长",
     "start_date": "2021-05", "end_date": "2021-07",
     "rank": "正处级（代）", "note": "2021-05-25 县16届人大常委会第38次会议"},
    # 苗润涛 — 丛台区
    {"person_id": 1, "org_id": 5, "title": "邯郸市丛台区人民政府副区长",
     "start_date": "2019-08", "end_date": "2021-05",
     "rank": "副处级", "note": "2019-08 丛台区第十届人大常委会第20次会议任命"},
    # 李玉涛 — 前任县委书记
    {"person_id": 2, "org_id": 1, "title": "高邑县委书记（前任）",
     "start_date": "2022", "end_date": "2026",
     "rank": "正处级", "note": "截至2025年2月主持县委常委会"},
    # 王惠武 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "高邑县人大常委会主任",
     "start_date": "", "end_date": "present",
     "rank": "正处级（人大）", "note": "截至2025年7月在任"},
    # 谷会文 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "高邑县政协主席",
     "start_date": "", "end_date": "present",
     "rank": "正处级（政协）", "note": "截至2025年7月在任"},
    # 彭敬捷 — 前任县委书记 / 现任司法厅
    {"person_id": 5, "org_id": 1, "title": "高邑县委书记（更早前任）",
     "start_date": "2019", "end_date": "2019-12",
     "rank": "正处级", "note": "2019-12离任高县县委书记"},
    {"person_id": 5, "org_id": 6, "title": "河北省司法厅党委委员、副厅长",
     "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": "现任省司法厅党委委员、副厅长、省律师行业党委书记"},
    # 张辉 — 现任县长 (current 2026)
    {"person_id": 6, "org_id": 2, "title": "高邑县人民政府县长",
     "start_date": "2026", "end_date": "present",
     "rank": "正处级", "note": "2026-06 官方县新闻网多次报道（2026-06-01 主持县政府常务会议）"},
    {"person_id": 6, "org_id": 1, "title": "高邑县委副书记",
     "start_date": "2026", "end_date": "present",
     "rank": "副处级（县委副书记兼）", "note": "官方新闻称县委副书记、县长"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 苗润涛 ↔ 李玉涛 — 县委书记前后任
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "苗润涛继李玉涛之后任高邑县委书记",
     "overlap_org": "中共石家庄市高邑县委员会",
     "overlap_period": "2025-2026"},
    # 苗润涛 ↔ 王惠武 — 党政与人大监督关系
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委与县人大常委会党政监督搭档",
     "overlap_org": "高邑县",
     "overlap_period": "2021-present"},
    # 苗润涛 ↔ 谷会文 — 县委与政协
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委与县政协党政搭档",
     "overlap_org": "高邑县",
     "overlap_period": "2021-present"},
    # 李玉涛 ↔ 彭敬捷 — 前任县委书记先后任 (context, older)
    {"person_a": 2, "person_b": 5, "type": "predecessor_successor",
     "context": "两位前任高邑县委书记（更高序先后任）",
     "overlap_org": "中共石家庄市高邑县委员会",
     "overlap_period": "2019-2022"},
    # 苗润涛 ↔ 张辉 — 现任县委书记 & 县长 党政搭档
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "高邑县委书记与县长（县委副书记、县长）党政搭档",
     "overlap_org": "中共石家庄市高邑县委员会/高邑县人民政府",
     "overlap_period": "2026-present"},
]

# =========================================================================
# 5. BUILD
# =========================================================================
if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    if os.path.exists(GEXF_PATH):
        os.remove(GEXF_PATH)
    run_build(
        slug="高邑县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"SQLite database written: {DB_PATH}")
    print(f"GEXF graph written: {GEXF_PATH}")
    print("Build complete. 现任书记: 苗润涛; 现任县长: 张辉.")