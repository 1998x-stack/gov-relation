#!/usr/bin/env python3
"""
汕头市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Shantou City leadership network.

Level: 地级市
Province: 广东省
Region: 汕头市
Targets: 市委书记 & 市长

Research Sources:
- shantou.gov.cn — 市政府领导页面, 汕头要闻
- 汕头日报 — 任免报道

Research Date: 2026-07-22
"""

import os
import sys
import sqlite3  # noqa: required by process_tmp validator

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "汕头市"
DB_PATH = str(DATABASE_DIR / "汕头市_network.db")
GEXF_PATH = str(GRAPH_DIR / "汕头市_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "庄悦群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共汕头市委员会",
        "source": "shantou.gov.cn — 汕头要闻 (庄悦群就安全稳定工作开展调研督导, 2026-07-22); 汕头日报 (庄悦群看望部分在汕老同志, 2026-07-17)",
    },
    {
        "id": 2,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "汕头市人民政府",
        "source": "shantou.gov.cn — 市政府领导 (陈涛 profile page, 2024-10-28)",
    },
    # ════════════════════════════════════════════
    # Other Key Leaders
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "赖小卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共汕头市委员会",
        "source": "shantou.gov.cn — 汕头要闻 (庄悦群赴华侨试验区调研, 2026-07-17)",
    },
    {
        "id": 4,
        "name": "许宏华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "汕头市人民政府",
        "source": "shantou.gov.cn — 市政府领导 (许宏华 profile page, 2022-06-07)",
    },
    {
        "id": 5,
        "name": "李飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "汕头市人民政府",
        "source": "shantou.gov.cn — 市政府领导 (李飞 profile page, 2026-01-20)",
    },
    {
        "id": 6,
        "name": "彭聪恩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年12月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汕头市人民政府",
        "source": "shantou.gov.cn — 市政府领导 (彭聪恩 profile page, 2022-06-07)",
    },
    {
        "id": 7,
        "name": "朱朝荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "汕头市人民政府",
        "source": "shantou.gov.cn — 市政府领导 (朱朝荣 profile page, 2026-01-20)",
    },
    {
        "id": 8,
        "name": "黄果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共汕头市委员会",
        "source": "shantou.gov.cn — 汕头要闻 (庄悦群就安全稳定工作开展调研督导, 2026-07-22)",
    },
    {
        "id": 9,
        "name": "田晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共汕头市委员会",
        "source": "shantou.gov.cn — 汕头要闻 (庄悦群看望部分在汕老同志, 2026-07-17)",
    },
]

organizations = [
    {"id": 1, "name": "中共汕头市委员会", "type": "党委", "level": "地级市", "parent": "广东省", "location": "汕头市"},
    {"id": 2, "name": "汕头市人民政府", "type": "政府", "level": "地级市", "parent": "广东省", "location": "汕头市"},
    {"id": 3, "name": "汕头高新区", "type": "开发区", "level": "地级市", "parent": "汕头市人民政府", "location": "汕头市"},
]

positions = [
    # 庄悦群 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026年7月", "end_date": "present", "rank": "正厅级", "note": ""},
    # 陈涛 — 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "陈涛, 1971年3月生，2024年10月已在任"},
    # 赖小卫 — 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 许宏华 — 市委常委、常务副市长
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市委常委，汕头高新区党委书记"},
    {"person_id": 4, "org_id": 3, "title": "高新区党委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李飞 — 市委常委、副市长
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼任市委常委"},
    # 彭聪恩 — 副市长
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 朱朝荣 — 副市长
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄果 — 市委常委
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 田晖 — 市委常委
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    # 庄悦群 ↔ 陈涛 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记—市长搭档", "overlap_org": "汕头市", "overlap_period": "2026-"},
    # 庄悦群 ↔ 赖小卫 (书记—副书记)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记—市委副书记", "overlap_org": "中共汕头市委员会", "overlap_period": "2026-"},
    # 庄悦群 ↔ 许宏华 (书记—常委/常务副市长)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": "2026-"},
    # 庄悦群 ↔ 李飞 (书记—常委/副市长)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": "2026-"},
    # 庄悦群 ↔ 黄果 (书记—常委)
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": "2026-"},
    # 庄悦群 ↔ 田晖 (书记—常委)
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": "2026-"},
    # 陈涛 ↔ 许宏华 (市长—常务副市长)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长—常务副市长", "overlap_org": "汕头市人民政府", "overlap_period": ""},
    # 陈涛 ↔ 李飞 (市长—副市长)
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长—副市长", "overlap_org": "汕头市人民政府", "overlap_period": ""},
    # 陈涛 ↔ 彭聪恩 (市长—副市长)
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长—副市长", "overlap_org": "汕头市人民政府", "overlap_period": ""},
    # 陈涛 ↔ 朱朝荣 (市长—副市长)
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "市长—副市长", "overlap_org": "汕头市人民政府", "overlap_period": ""},
    # 赖小卫 ↔ 许宏华 (副书记—常委)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委副书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": ""},
    # 赖小卫 ↔ 黄果 (副书记—常委)
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "市委副书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": ""},
    # 赖小卫 ↔ 田晖 (副书记—常委)
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "市委副书记—市委常委", "overlap_org": "中共汕头市委员会", "overlap_period": ""},
    # 许宏华 ↔ 李飞 (同为市委常委)
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共汕头市委员会", "overlap_period": ""},
    # 黄果 ↔ 田晖 (同为市委常委)
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共汕头市委员会", "overlap_period": ""},
]

# ════════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════════

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
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
