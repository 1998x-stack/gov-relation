#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 社旗县 leadership network.

社旗县 - 南阳市 - 河南省
Targets: 县委书记关文波, 县长姜涛
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
import json
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "社旗县"
TASK_ID = "henan_社旗县"
TODAY = "20260724"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "关文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "社旗县委书记",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-08/1418196.html",
    },
    {
        "id": 2,
        "name": "姜涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "社旗县委副书记、县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/xzf",
    },
    # ── Previous Leader ──
    {
        "id": 3,
        "name": "张荣印",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原社旗县委书记（已离任）",
        "current_org": "",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    # ── County Government Leaders ──
    {
        "id": 4,
        "name": "马珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 5,
        "name": "郑通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/2026/07-23/1422016.html",
    },
    {
        "id": 6,
        "name": "张黎晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/2025/09-02/1210269.html",
    },
    {
        "id": 7,
        "name": "杜鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/xzf",
    },
    {
        "id": 8,
        "name": "龚清桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/xzf",
    },
    # ── Other Key Leaders ──
    {
        "id": 9,
        "name": "谢男",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 10,
        "name": "朱宏范",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（原）",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 11,
        "name": "陈晓鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "社旗县人大常委会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 12,
        "name": "张东焕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 13,
        "name": "魏武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 14,
        "name": "魏乐乐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委代主任",
        "current_org": "中共社旗县纪律检查委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 15,
        "name": "韩向京",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 16,
        "name": "赵向龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 17,
        "name": "胡明柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 18,
        "name": "刘朝普",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 19,
        "name": "刘龙海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2025/08-18/1163643.html",
    },
    {
        "id": 20,
        "name": "王桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "中国共产党社旗县委员会",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 21,
        "name": "李英鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 22,
        "name": "张松涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "社旗县人民政府",
        "source": "https://www.sheqi.gov.cn/2026/07-16/1421076.html",
    },
    {
        "id": 23,
        "name": "文献充",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "社旗县人大常委会",
        "source": "https://www.sheqi.gov.cn/2026/07-23/1422016.html",
    },
    {
        "id": 24,
        "name": "张宛黎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "社旗县人大常委会",
        "source": "https://www.sheqi.gov.cn/2026/07-23/1422016.html",
    },
    {
        "id": 25,
        "name": "杨晗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "社旗县人大常委会",
        "source": "https://www.sheqi.gov.cn/2026/07-23/1422016.html",
    },
    {
        "id": 26,
        "name": "张东晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "社旗县人大常委会",
        "source": "https://www.sheqi.gov.cn/2026/07-23/1422016.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党社旗县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党南阳市委员会",
        "location": "社旗县",
    },
    {
        "id": 2,
        "name": "社旗县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "南阳市人民政府",
        "location": "社旗县",
    },
    {
        "id": 3,
        "name": "社旗县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "社旗县",
        "location": "社旗县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议社旗县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "社旗县",
        "location": "社旗县",
    },
    {
        "id": 5,
        "name": "中共社旗县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党社旗县委员会",
        "location": "社旗县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 关文波
    {"person_id": "p1", "org_id": 1, "title": "社旗县委书记", "start_date": "2024", "end_date": "present", "rank": "正县级", "note": "曾同时兼任县长"},
    # 姜涛
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start_date": "2026", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": "p2", "org_id": 2, "title": "县长", "start_date": "2026", "end_date": "present", "rank": "正县级", "note": ""},
    # 张荣印
    {"person_id": "p3", "org_id": 1, "title": "社旗县委书记（原）", "start_date": "", "end_date": "2024", "rank": "正县级", "note": "前任县委书记"},
    # 马珂
    {"person_id": "p4", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": "p4", "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 郑通
    {"person_id": "p5", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": "p5", "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张黎晓
    {"person_id": "p6", "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杜鑫
    {"person_id": "p7", "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 龚清桐
    {"person_id": "p8", "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 谢男
    {"person_id": "p9", "org_id": 1, "title": "县委副书记", "start_date": "2026", "end_date": "present", "rank": "副县级", "note": "兼政法委书记"},
    # 朱宏范
    {"person_id": "p10", "org_id": 1, "title": "县委副书记（原）", "start_date": "", "end_date": "2026", "rank": "副县级", "note": ""},
    # 陈晓鹏
    {"person_id": "p11", "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 张东焕
    {"person_id": "p12", "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 魏武
    {"person_id": "p13", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 魏乐乐
    {"person_id": "p14", "org_id": 5, "title": "县委常委、县纪委书记、监委代主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 韩向京
    {"person_id": "p15", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 赵向龙
    {"person_id": "p16", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 胡明柱
    {"person_id": "p17", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘朝普
    {"person_id": "p18", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘龙海
    {"person_id": "p19", "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 文献充
    {"person_id": "p23", "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张宛黎
    {"person_id": "p24", "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 杨晗
    {"person_id": "p25", "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 张东晓
    {"person_id": "p26", "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    {
        "person_a": "p1",
        "person_b": "p2",
        "type": "共事",
        "context": "关文波（县委书记）与姜涛（县长）党政正职搭档",
        "overlap_org": "社旗县",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p1",
        "person_b": "p3",
        "type": "前任继任",
        "context": "关文波接替张荣印任社旗县委书记",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "2024年交接",
    },
    {
        "person_a": "p1",
        "person_b": "p9",
        "type": "上下级",
        "context": "关文波（县委书记）与谢男（县委副书记、政法委书记）党委班子上下级关系",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p1",
        "person_b": "p10",
        "type": "上下级",
        "context": "关文波（县委书记）与朱宏范（原县委副书记）党委班子上下级关系",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "至2026年",
    },
    {
        "person_a": "p1",
        "person_b": "p11",
        "type": "共事",
        "context": "关文波（县委书记）与陈晓鹏（县人大常委会主任）党政班子与人大负责人关系",
        "overlap_org": "社旗县",
        "overlap_period": "至今",
    },
    {
        "person_a": "p1",
        "person_b": "p12",
        "type": "共事",
        "context": "关文波（县委书记）与张东焕（县政协主席）党政班子与政协负责人关系",
        "overlap_org": "社旗县",
        "overlap_period": "至今",
    },
    {
        "person_a": "p1",
        "person_b": "p14",
        "type": "上下级",
        "context": "关文波（县委书记）与魏乐乐（县纪委书记）党委班子上下级关系",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": "p2",
        "person_b": "p4",
        "type": "上下级",
        "context": "姜涛（县长）与马珂（副县长）政府班子上下级关系",
        "overlap_org": "社旗县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p2",
        "person_b": "p5",
        "type": "上下级",
        "context": "姜涛（县长）与郑通（副县长）政府班子上下级关系",
        "overlap_org": "社旗县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p2",
        "person_b": "p6",
        "type": "上下级",
        "context": "姜涛（县长）与张黎晓（副县长）政府班子上下级关系",
        "overlap_org": "社旗县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p2",
        "person_b": "p7",
        "type": "上下级",
        "context": "姜涛（县长）与杜鑫（副县长）政府班子上下级关系",
        "overlap_org": "社旗县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p2",
        "person_b": "p8",
        "type": "上下级",
        "context": "姜涛（县长）与龚清桐（副县长）政府班子上下级关系",
        "overlap_org": "社旗县人民政府",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p4",
        "person_b": "p5",
        "type": "共事",
        "context": "马珂与郑通同为县委常委、副县长",
        "overlap_org": "社旗县人民政府/县委",
        "overlap_period": "至今",
    },
    {
        "person_a": "p9",
        "person_b": "p14",
        "type": "共事",
        "context": "谢男（县委副书记、政法委书记）与魏乐乐（县纪委书记）党委班子工作关系",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": "p11",
        "person_b": "p12",
        "type": "共事",
        "context": "陈晓鹏（县人大常委会主任）与张东焕（县政协主席）四套班子工作关系",
        "overlap_org": "社旗县",
        "overlap_period": "至今",
    },
    {
        "person_a": "p1",
        "person_b": "p13",
        "type": "上下级",
        "context": "关文波（县委书记）与魏武（县委常委）党委班子上下级关系",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": "p10",
        "person_b": "p9",
        "type": "前任继任",
        "context": "谢男接替朱宏范任县委副书记",
        "overlap_org": "中国共产党社旗县委员会",
        "overlap_period": "2026年交接",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(f" Done.")
