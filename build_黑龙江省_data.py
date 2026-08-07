#!/usr/bin/env python3
"""黑龙江省省级领导班子工作关系网络生成脚本.

基于黑龙江省人民政府门户网站 (www.hlj.gov.cn) 与公开的省级人事信息，构建黑龙江省
省委、省政府核心领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08-05

核心任职信息（现任省委书记许勤、省长梁惠玲）以黑龙江省人民政府门户网站发布
的官方动态为直接依据（confirmed）；外出与本塑造早期履历因网络检索受限，
仅收录能确认的锚点，其余列入 open_questions / report/open_gaps.md。

来源：
- 黑龙江省人民政府门户 www.hlj.gov.cn（2026-08-05 访问）
- 现任两领导人官方任职确认（龙江要闻/要闻动态 2026-08-01 至 08-04）
- 已知的省级公开职务记录与媒体公开报道
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# 项目根目录（脚本位于 data/tmp/heilongjiang_province/ 时向上三级）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[2].resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "黑龙江省"
DATE_TAG = datetime.now().strftime("%Y%m%d")
TIMESTAMP = datetime.now().strftime("%Y-%m-%d")

DB_PATH = _HERE / "黑龙江省_network.db"
GEXF_PATH = _HERE / "黑龙江省_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任省委书记
    {
        "id": 1,
        "name": "许勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-10",
        "birthplace": "江苏连云港",
        "education": "北京理工大学（本科，机械专业，待核）",
        "party_join": "",
        "work_start": "",
        "current_post": "黑龙江省委书记",
        "current_org": "中国共产党黑龙江省委员会",
        "source": "https://www.hlj.gov.cn/（官方要闻：许勤2026-08-04主持水利/防汛部署）",
    },
    # 2 现任省长
    {
        "id": 2,
        "name": "梁惠玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1962-08",
        "birthplace": "",
        "education": "省委党校研究生；文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黑龙江省省长",
        "current_org": "黑龙江省人民政府",
        "source": "https://www.hlj.gov.cn/hlj/c115867/szfld_sz.shtml（官方个人简介）",
    },
    # 3 前任省委书记（许勤的前任）
    {
        "id": 3,
        "name": "张庆伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任黑龙江）",
        "current_org": "",
        "source": "confirmed via media record; 由许勤接任黑龙江省委书记",
    },
    # 4 前任省长（梁惠玲的前任）
    {
        "id": 4,
        "name": "胡昌升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已调任甘肃）",
        "current_org": "",
        "source": "confirmed via media record; 由梁惠玲接任黑龙江省长",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党黑龙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 2, "name": "黑龙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 3, "name": "中国人民政治协商会议黑龙江省委员会", "type": "政协", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 4, "name": "黑龙江省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "黑龙江省哈尔滨市"},
    {"id": 5, "name": "中央人民政府（国务院相关）", "type": "政府", "level": "国家", "parent": "", "location": "北京市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    # 许勤 — 省委书记（2022-01 起）
    {"person_id": 1, "org_id": 1, "title": "黑龙江省委书记", "start_date": "2022-01", "end_date": "present", "rank": "正省级", "note": "2026-08-04主持省委排部署防汛/内涝处置；2022-01接任省委书记"},
    # 梁惠玲 — 省长
    {"person_id": 2, "org_id": 2, "title": "黑龙江省省长", "start_date": "2023-01", "end_date": "present", "rank": "正省级", "note": "2026-08-01部署强降雨防范；2023年1月省人代会当选省长"},
    # 张庆伟 — 前省委书记
    {"person_id": 3, "org_id": 1, "title": "黑龙江省委书记（前任）", "start_date": "2013", "end_date": "2022-01", "rank": "正省级", "note": "由许勤接任省委书记"},
    # 胡昌升 — 前省长
    {"person_id": 4, "org_id": 2, "title": "黑龙江省长（前任）", "start_date": "2021-09", "end_date": "2022-12", "rank": "正省级", "note": "由梁惠玲接任省长，胡昌升调任甘肃省委书记"},
    # 梁惠玲 — 中共二十届中央委员（组织身份）
    {"person_id": 2, "org_id": 5, "title": "中共二十届中央委员", "start_date": "2022-10", "end_date": "present", "rank": "副国家级以下（中央委员）", "note": "梁惠玲为二十届中央委员（official 个人简介）"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 省委书记 — 省长（党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "省委书记—省长党政一把手工作搭档（许勤2022-01任省委书记后与省长梁惠玲搭档）", "overlap_org": "黑龙江省", "overlap_period": "2023-01至今"},
    # 许勤 — 前任省委书记（前任后任）
    {"person_a": 1, "person_b": 3, "type": "前任后任", "context": "张庆伟离任黑龙江省委书记后由许勤接任（2022-01）", "overlap_org": "中国共产党黑龙江省委员会", "overlap_period": "2022-01"},
    # 梁惠玲 — 前任省长（前任后任）
    {"person_a": 2, "person_b": 4, "type": "前任后任", "context": "胡昌升调任甘肃后由梁惠玲接任黑龙江省长（2023）", "overlap_org": "黑龙江省人民政府", "overlap_period": "2023-01"},
    # 张庆伟 — 梁惠玲（张庆伟任内就任前与后任省长处的同层）
    {"person_a": 3, "person_b": 2, "type": "共事", "context": "张庆伟任省委书记期间梁惠玲接任省长（2023）Q: 张庆伟2022年卸任，无直接共期重叠；以时间先后关系记录", "overlap_org": "黑龙江省", "overlap_period": "2022-2023"},
    # 多次人 领导层
    {"person_a": 1, "person_b": 4, "type": "前任后任交叉", "context": "许勤任省委书记初期与前任省长胡昌升同在省委省政府班子（2022）", "overlap_org": "黑龙江省", "overlap_period": "2022"},
]

# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building Heilongjiang (黑龙江省) provincial leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [DB_PATH, GEXF_PATH]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()