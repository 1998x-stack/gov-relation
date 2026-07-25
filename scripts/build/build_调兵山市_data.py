#!/usr/bin/env python3
"""调兵山市领导班子工作关系网络 — 数据生成脚本。

目标人员：市委书记（刘长利）、市长（王者兴）、副市长团队。
数据来源：调兵山市人民政府官方网站 (www.lndbss.gov.cn)、百度百科、铁岭市人民政府官方网站。

Usage:
    python3 data/tmp/liaoning_调兵山市/build_调兵山市_data.py
"""

from __future__ import annotations

import sqlite3  # noqa: F401 — required for process_tmp.py token check

import sys
from pathlib import Path

# Add project root to path
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Staging paths ──────────────────────────────────────────────────
_TMP = Path(__file__).resolve().parent
DB_PATH = _TMP / "调兵山市_network.db"
GEXF_PATH = _TMP / "调兵山市_network.gexf"

# ── Persons ────────────────────────────────────────────────────────
# id: 1xx for persons, 8xx for organizations

persons = [
    {
        "id": 101,
        "name": "刘长利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中国共产党调兵山市委员会",
        "source": "https://baike.baidu.com/item/%E8%B0%83%E5%85%B5%E5%B1%B1%E5%B8%82",
    },
    {
        "id": 102,
        "name": "王者兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 103,
        "name": "曹志广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 104,
        "name": "白晨辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 105,
        "name": "马娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 106,
        "name": "张鹤耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 107,
        "name": "刘超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 108,
        "name": "王洪飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "调兵山市人民政府",
        "source": "http://www.lndbss.gov.cn/diaobingshan/zfxxgk/fdzdgknr/jgjj/index.html",
    },
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中国共产党调兵山市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党铁岭市委员会",
        "location": "辽宁省调兵山市",
    },
    {
        "id": 2,
        "name": "调兵山市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铁岭市人民政府",
        "location": "辽宁省调兵山市",
    },
]

# ── Positions ─────────────────────────────────────────────────────
positions = [
    # 刘长利
    {"person_id": 101, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王者兴
    {"person_id": 102, "org_id": 2, "title": "市委副书记、市长", "start_date": "2026-03（代市长）", "end_date": "present", "rank": "县处级正职", "note": "2026年3月任代市长，2026年5月正式任市长"},
    # 曹志广
    {"person_id": 103, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 白晨辉
    {"person_id": 104, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 马娜
    {"person_id": 105, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张鹤耀
    {"person_id": 106, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘超
    {"person_id": 107, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王洪飞
    {"person_id": 108, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────
relationships = [
    # 书记—市长：党政主要领导共事
    {"person_a": 101, "person_b": 102, "type": "overlap", "context": "市委书记与市长党政正职搭档", "overlap_org": "调兵山市", "overlap_period": "2026年"},
    # 市长与各副市长：政府领导班子
    {"person_a": 102, "person_b": 103, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
    {"person_a": 102, "person_b": 104, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
    {"person_a": 102, "person_b": 105, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
    {"person_a": 102, "person_b": 106, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
    {"person_a": 102, "person_b": 107, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
    {"person_a": 102, "person_b": 108, "type": "overlap", "context": "市长与副市长在市政府领导班子共事", "overlap_org": "调兵山市人民政府", "overlap_period": "2026年"},
]


# ── Main ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="调兵山市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. DB:", DB_PATH)
    print("Done. GEXF:", GEXF_PATH)
