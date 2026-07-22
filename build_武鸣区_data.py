#!/usr/bin/env python3
"""
Build 武鸣区 (Wuming District, 南宁市, 广西壮族自治区) government personnel
relationship network — SQLite database + GEXF graph.

武鸣区 is a district under 南宁市, Guangxi Zhuang Autonomous Region.
Current as of: 2026-07-22

Targets: 区委书记 & 区长
Core figures: 张然 (区委书记), 林博亮 (代理区长)

== TRANSITION NOTE ==
- 尹玉林 resigned as 区长 on 2026-07-21
- 林博亮 (formerly 副区长) appointed acting 区长 on 2026-07-21

Sources:
- 武鸣区人民政府门户网站 www.wuming.gov.cn 领导之窗 (2026年7月)
- 武鸣区融媒体中心新闻报道 (2026年7月)
"""

import sys
import os
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "武鸣区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "武鸣区_network.gexf")

REPO_ROOT = os.path.abspath(os.path.join(STAGING_DIR, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# ── DATA ─────────────────────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

persons = [
    # ── Core leaders ────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "张然",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区委书记",
        "current_org": "中共南宁市武鸣区委员会",
        "source": "武鸣区融媒体中心 2026年7月多篇报道确认区委书记职务（区委常委会会议、调研活动等）https://www.wuming.gov.cn",
    },
    {
        "id": 2,
        "name": "林博亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区委副书记、代理区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人大常委会决定：林博亮代理区长职务（2026-07-21）https://www.wuming.gov.cn/yw/wmyw/t6686080.html",
    },
    # ── Predecessor 区长 ──────────────────────────────────────────────
    {
        "id": 3,
        "name": "尹玉林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原武鸣区区长（已辞职）",
        "current_org": "",
        "source": "武鸣区人大常委会接受尹玉林辞去区长职务（2026-07-21）；原为武鸣区领导之窗公示区长 https://www.wuming.gov.cn",
    },
    # ── Key deputies: 副区长 ──────────────────────────────────────────
    {
        "id": 4,
        "name": "陈卫国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    {
        "id": 5,
        "name": "黄任含",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    {
        "id": 6,
        "name": "潘新世",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    {
        "id": 7,
        "name": "黄海珍",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    {
        "id": 8,
        "name": "温瀚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    {
        "id": 9,
        "name": "陆坚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区副区长",
        "current_org": "武鸣区人民政府",
        "source": "武鸣区人民政府领导之窗 https://www.wuming.gov.cn",
    },
    # ── 人大常委会主任 ────────────────────────────────────────────────
    {
        "id": 10,
        "name": "黄国录",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区人大常委会主任",
        "current_org": "武鸣区人大常委会",
        "source": "武鸣区第二届人大常委会第四十三次会议报道 https://www.wuming.gov.cn/yw/wmyw/t6686097.html",
    },
    # ── 城区领导陪同调研 ───────────────────────────────────────────────
    {
        "id": 11,
        "name": "张莉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区领导",
        "current_org": "",
        "source": "武鸣区融媒体中心报道：张莉陪同区委书记张然调研 https://www.wuming.gov.cn",
    },
    {
        "id": 12,
        "name": "张杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武鸣区领导",
        "current_org": "",
        "source": "武鸣区融媒体中心报道：张杰陪同区委书记张然调研 https://www.wuming.gov.cn",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共南宁市武鸣区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共南宁市委员会",
        "location": "南宁市武鸣区",
    },
    {
        "id": 2,
        "name": "武鸣区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "南宁市人民政府",
        "location": "南宁市武鸣区",
    },
    {
        "id": 3,
        "name": "武鸣区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "南宁市人大常委会",
        "location": "南宁市武鸣区",
    },
]

positions = [
    # 张然
    {"person_id": 1, "org_id": 1, "title": "武鸣区委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "主持区委全面工作"},
    # 林博亮
    {"person_id": 2, "org_id": 2, "title": "武鸣区副区长、代理区长", "start_date": "2026-07", "end_date": "至今", "rank": "正处级", "note": "2026年7月21日区人大常委会任命为副区长、代理区长"},
    # 尹玉林（原区长）
    {"person_id": 3, "org_id": 2, "title": "武鸣区区长", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "2026年7月21日辞去区长职务"},
    # 副区长
    {"person_id": 4, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "武鸣区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 黄国录
    {"person_id": 10, "org_id": 3, "title": "武鸣区人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 张莉、张杰
    {"person_id": 11, "org_id": 1, "title": "武鸣区领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 1, "title": "武鸣区领导", "start_date": "", "end_date": "至今", "rank": "", "note": "具体职务待查"},
]

relationships = [
    # 党委—政府核心搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与代理区长：党委与政府主要领导工作搭档关系",
        "overlap_org": "武鸣区领导班子",
        "overlap_period": "2026-07至今",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与原区长：党委与政府主要领导工作搭档关系",
        "overlap_org": "武鸣区领导班子",
        "overlap_period": "张然任区委书记期间",
    },
    # 区长更替
    {
        "person_a": 2, "person_b": 3,
        "type": "predecessor_successor",
        "context": "林博亮接替尹玉林代理区长职务",
        "overlap_org": "武鸣区人民政府",
        "overlap_period": "2026-07",
    },
    # 区委书记与副区长团队
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与副区长", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    # 人大主任与党委、政府
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "人大常委会主任与区委书记", "overlap_org": "武鸣区领导班子", "overlap_period": ""},
    {"person_a": 10, "person_b": 2, "type": "overlap", "context": "人大常委会主任与代理区长（颁发任命书）", "overlap_org": "武鸣区人大常委会", "overlap_period": "2026-07"},
    # 陪同调研记录
    {"person_a": 11, "person_b": 1, "type": "overlap", "context": "陪同区委书记调研基层党建与乡村振兴", "overlap_org": "武鸣区", "overlap_period": "2026-07"},
    {"person_a": 12, "person_b": 1, "type": "overlap", "context": "陪同区委书记调研基层党建与乡村振兴", "overlap_org": "武鸣区", "overlap_period": "2026-07"},
]


# ── Build ─────────────────────────────────────────────────────────────────

def main():
    # Use gov_relation.runner if available, otherwise standalone
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
        run_build(
            slug="武鸣区",
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=DB_PATH,
            gexf_path=GEXF_PATH,
        )
    except ImportError:
        # Fallback standalone implementation
        _standalone_build()

    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print("Done.")


def _standalone_build():
    import sqlite3
    from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships
    from gov_relation.gexf import GEXFBuilder

    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn)
        insert_persons(conn, persons)
        insert_organizations(conn, organizations)
        insert_positions(conn, positions)
        insert_relationships(conn, relationships)
    finally:
        conn.close()

    builder = GEXFBuilder(title="武鸣区领导班子关系图")
    for p in persons:
        builder.add_person(
            id=p["id"],
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in organizations:
        builder.add_organization(
            id=o["id"] + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in relationships:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(GEXF_PATH)


if __name__ == "__main__":
    main()
