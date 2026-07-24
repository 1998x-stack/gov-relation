#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 镇平县 leadership network.

镇平县 - 南阳市 - 河南省
Targets: 县委书记艾进德, 县长李靖
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "镇平县"
TASK_ID = "henan_镇平县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "艾进德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "镇平县委书记",
        "current_org": "中国共产党镇平县委员会",
        "source": "https://www.zhenping.gov.cn/",
    },
    {
        "id": 2,
        "name": "李靖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2026/05-18/1405804.html",
    },
    # ── Previous Leaders ──
    {
        "id": 3,
        "name": "黄静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原镇平县长（已离任）",
        "current_org": "",
        "source": "https://www.zhenping.gov.cn/xzf/xzhdj/",
    },
    # ── Government Leaders ──
    {
        "id": 4,
        "name": "薛江峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、常务副县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2024/09-12/617592.html",
    },
    {
        "id": 5,
        "name": "宋珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年8月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2026/07-02/1417160.html",
    },
    {
        "id": 6,
        "name": "白兆文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年11月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组副书记",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2022/11-20/580431.html",
    },
    {
        "id": 7,
        "name": "王斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长、县公安局局长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2022/11-04/580435.html",
    },
    {
        "id": 8,
        "name": "陈云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2022/11-03/580432.html",
    },
    {
        "id": 9,
        "name": "曹光志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2026/07-02/1417159.html",
    },
    {
        "id": 10,
        "name": "李虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年2月",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "镇平县人民政府",
        "source": "https://www.zhenping.gov.cn/2026/07-02/1417158.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党镇平县委员会",
        "type": "党委",
        "level": "县级",
        "location": "河南省南阳市镇平县",
    },
    {
        "id": 2,
        "name": "镇平县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "河南省南阳市镇平县",
    },
    {
        "id": 3,
        "name": "镇平县公安局",
        "type": "政府",
        "level": "县级",
        "location": "河南省南阳市镇平县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 艾进德
    {"person_id": 1, "org_id": 1, "title": "镇平县委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 李靖
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县政府党组书记、县长", "start": "2026-05", "end": "present", "rank": "正处级", "note": "2026年5月任镇平县长"},
    # 黄静（前任县长）
    {"person_id": 3, "org_id": 2, "title": "镇平县长", "start": "2021?", "end": "2026-05", "rank": "正处级", "note": "前任县长，2026年5月离任"},
    # 薛江峰
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 宋珂
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 白兆文
    {"person_id": 6, "org_id": 2, "title": "县政府党组副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王斌
    {"person_id": 7, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈云峰
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 曹光志
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李虎
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "艾进德（县委书记）与李靖（县长）党政正职搭档", "overlap_org": "镇平县", "overlap_period": "2026-至今"},
    # 前任继承
    {"person_a": 2, "person_b": 3, "type": "前任继任", "context": "李靖接替黄静任镇平县长", "overlap_org": "镇平县人民政府", "overlap_period": "2026年交接"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "艾进德（县委书记）与黄静（原县长）前任党政正职搭档", "overlap_org": "镇平县", "overlap_period": "至2026年"},
    # 上下级关系：县长与副县长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "李靖（县长）与薛江峰（常务副县长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "李靖（县长）与宋珂（副县长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "李靖（县长）与白兆文（党组副书记）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "李靖（县长）与王斌（副县长、公安局长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "李靖（县长）与陈云峰（副县长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "李靖（县长）与曹光志（副县长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "李靖（县长）与李虎（副县长）政府班子上下级关系", "overlap_org": "镇平县人民政府", "overlap_period": "2026-至今"},
    # 县委常委之间的共事关系
    {"person_a": 4, "person_b": 5, "type": "共事", "context": "薛江峰与宋珂同为县委常委", "overlap_org": "中国共产党镇平县委员会", "overlap_period": "至今"},
    # 县委书记与前任县长的关系
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "艾进德（县委书记）与薛江峰（县委常委）党委班子上下级关系", "overlap_org": "中国共产党镇平县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "艾进德（县委书记）与宋珂（县委常委）党委班子上下级关系", "overlap_org": "中国共产党镇平县委员会", "overlap_period": "至今"},
]

# ── Run ──────────────────────────────────────────────────────────────

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
    print(f"\nDone: {DB_PATH}  {GEXF_PATH}")
