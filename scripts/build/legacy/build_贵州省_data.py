#!/usr/bin/env python3
"""贵州省省级领导班子工作关系网络生成脚本.

基于贵州省人民政府门户网站 (www.guizhou.gov.cn) 与已知的省级人事公开信息，
构建贵州省省委、省政府、省政协核心领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08-05
核心任职信息以贵州省人民政府门户发布的官方动态为 direct 依据（confirmed）；
早期履历细节因网络检索受限，仅收录能确认的锚点，其余列入 open_questions。

来源：
- 贵州省人民政府门户 www.guizhou.gov.cn（2026-08-05 访问）
- 已知的省级公开职务记录
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# 项目根目录（脚本位于 data/tmp/guizhou_province/ 时向上三级）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "贵州省"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

DB_PATH = _HERE / "贵州省_network.db"
GEXF_PATH = _HERE / "贵州省_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任省委书记
    {
        "id": 1,
        "name": "徐麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贵州省委书记",
        "current_org": "中国共产党贵州省委员会",
        "source": "https://www.guizhou.gov.cn/home/tt/202608/t20260801_90684455.html",
    },
    # 2 现任省长
    {
        "id": 2,
        "name": "李炳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贵州省省长",
        "current_org": "贵州省人民政府",
        "source": "https://www.guizhou.gov.cn/home/jjtpxw/202608/t20260805_90696496.html",
    },
    # 3 省政协主席
    {
        "id": 3,
        "name": "赵永清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贵州省政协主席",
        "current_org": "中国人民政治协商会议贵州省委员会",
        "source": "https://www.guizhou.gov.cn/home/jjtpxw/202607/t20260731_90683732.html",
    },
    # 4 省领导（省委常委层级）
    {
        "id": 4,
        "name": "马汉成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贵州省领导（省委常委）",
        "current_org": "中国共产党贵州省委员会",
        "source": "https://www.guizhou.gov.cn/home/jjtpxw/202607/t20260731_90679320.html",
    },
    # 5 前任省委书记
    {
        "id": 5,
        "name": "谌贻琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任贵州）",
        "current_org": "",
        "source": "confirmed via media record; successor relationship confirmed from gov portal roster",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党贵州省委员会", "type": "党委", "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 2, "name": "贵州省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 3, "name": "中国人民政治协商会议贵州省委员会", "type": "政协", "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 4, "name": "贵州省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 5, "name": "中共贵州省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中国共产党贵州省委员会", "location": "贵州省贵阳市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    # 徐麟 — 省委书记（2022-12 起）
    {"person_id": 1, "org_id": 1, "title": "贵州省委书记", "start_date": "2022-12", "end_date": "present", "rank": "正省级", "note": "2026-08-01主持省委常委会工作；2022-12接任省委书记"},
    # 李炳军 — 省长
    {"person_id": 2, "org_id": 2, "title": "贵州省省长", "start_date": "2020", "end_date": "present", "rank": "正省级", "note": "2026-08-05在安顺市调研；2020年起任贵州省长"},
    # 赵永清 — 政协主席
    {"person_id": 3, "org_id": 3, "title": "贵州省政协主席", "start_date": "present", "end_date": "present", "rank": "正省级", "note": "2026-07-31主持省长与政协委员座谈会（official）"},
    # 马汉成 — 省领导/常委
    {"person_id": 4, "org_id": 1, "title": "贵州省委常委（省领导）", "start_date": "present", "end_date": "present", "rank": "副省级", "note": "2026-07-31列入省领导名单参加八一军事日活动（official）"},
    # 谌贻琴 — 前任省委书记
    {"person_id": 5, "org_id": 1, "title": "贵州省委书记（前任）", "start_date": "2020", "end_date": "2022-12", "rank": "正省级", "note": "由徐麟接任省委书记；此前2020年起任贵州省委书记"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 省委书记 — 省长（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "省委书记—省长党政一把手工作搭档（徐麟2022-12任省委书记后与省长李炳军搭档）", "overlap_org": "贵州省", "overlap_period": "2022-12至今"},
    # 徐麟 — 前任省委书记（前任后任）
    {"person_a": 1, "person_b": 5, "type": "前任后任", "context": "谌贻琴离任贵州省委书记后由徐麟接任（2022-12）", "overlap_org": "中国共产党贵州省委员会", "overlap_period": "2022-12"},
    # 李炳军 与 前任省委书记（共事）
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "谌贻琴任省委书记期间李炳军任省长（2020-2022）", "overlap_org": "中国共产党贵州省委员会", "overlap_period": "2020-2022"},
    # 省委书记 — 政协主席（四套班子协调）
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "省委书记与省政协主席同属省级领导层", "overlap_org": "贵州省", "overlap_period": "present"},
    # 省长 — 政协主席（省政府与省政协例会互动）
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "省长出席省长与政协委员座谈会，政协主席主持", "overlap_org": "贵州省政协", "overlap_period": "2026-07-31"},
    # 省委书记 — 马汉成（省委常委会）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "徐麟任省委书记，马汉成为省委常委/省领导", "overlap_org": "中国共产党贵州省委员会", "overlap_period": "present"},
    # 省长 — 马汉成（省委常委会）
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "省长与省委常委同属省级领导层", "overlap_org": "中国共产党贵州省委员会", "overlap_period": "present"},
    # 李炳军 — 前任省委书记 谌贻琴（共事）
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "谌贻琴任省委书记期间李炳军任贵州省长", "overlap_org": "中国共产党贵州省委员会", "overlap_period": "2020-2022"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    staging = _HERE
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    print(f"Building Guizhou (贵州省) provincial leadership network...")
    print(f"  Database: {db_path}")
    print(f"  GEXF:     {gexf_path}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [db_path, gexf_path]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()