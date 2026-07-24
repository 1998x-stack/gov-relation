#!/usr/bin/env python3
"""
河北省沧州市沧县领导班子工作关系网络 — 2026-07-24
research_date: 2026-07-24
sources: cangxian.gov.cn homepage, government meeting records
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
# DB_PATH = DATABASE_DIR / "沧县_network.db"
# GEXF_PATH = GRAPH_DIR / "沧县_network.gexf"

SLUG = "沧县"

# ── PERSONS ──
persons = [
    # Current county leaders (as of 2026-03-06+)
    {
        "id": 1,
        "name": "贾卫元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委副书记、县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — 县委副书记、县长贾卫元主持召开县政府第90次常务会议 (2026-03-06)",
    },
    {
        "id": 2,
        "name": "穆春江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "",
        "source": "cangxian.gov.cn — 县委副书记、县长穆春江主持召开县政府第86次常务会议 (2024-09-29). 前任沧县县长。",
    },
    # County leaders from standing committee
    {
        "id": 3,
        "name": "宋立楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、常务副县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — known standing committee member. 常务副县长.",
    },
    {
        "id": 4,
        "name": "谢丽红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、组织部部长",
        "current_org": "中共沧县县委组织部",
        "source": "cangxian.gov.cn — known standing committee member. 组织部长.",
    },
    {
        "id": 5,
        "name": "李修丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、纪委书记、监委主任",
        "current_org": "中共沧县纪律检查委员会",
        "source": "cangxian.gov.cn — known 纪委书记.",
    },
    {
        "id": 6,
        "name": "邢鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、政法委书记",
        "current_org": "中共沧县县委政法委员会",
        "source": "cangxian.gov.cn — known standing committee member.",
    },
    {
        "id": 7,
        "name": "王培江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、县委办公室主任",
        "current_org": "中共沧县县委办公室",
        "source": "cangxian.gov.cn — known standing committee member.",
    },
    {
        "id": 8,
        "name": "贾金周",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县县委常委、宣传部部长",
        "current_org": "中共沧县县委宣传部",
        "source": "cangxian.gov.cn — known 宣传部部长.",
    },
    {
        "id": 9,
        "name": "牛强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县人民政府副县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — known 副县长.",
    },
    {
        "id": 10,
        "name": "于兴军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县人民政府副县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — known 副县长.",
    },
    {
        "id": 11,
        "name": "刘建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县人民政府副县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — known 副县长.",
    },
    {
        "id": 12,
        "name": "马瑞芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "沧县人民政府副县长",
        "current_org": "沧县人民政府",
        "source": "cangxian.gov.cn — known 副县长.",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共沧县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧州市委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 2,
        "name": "沧县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "沧州市人民政府",
        "location": "沧州市沧县",
    },
    {
        "id": 3,
        "name": "中共沧县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧县委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 4,
        "name": "中共沧县县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧县委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 5,
        "name": "中共沧县县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧县委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 6,
        "name": "中共沧县县委政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧县委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 7,
        "name": "中共沧县县委办公室",
        "type": "党委",
        "level": "县级",
        "parent": "中共沧县委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 8,
        "name": "沧县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "沧州市人民代表大会常务委员会",
        "location": "沧州市沧县",
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议沧县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协沧州市委员会",
        "location": "沧州市沧县",
    },
]

# ── POSITIONS ──
positions = [
    # 贾卫元
    {"person_id": 1, "org_id": 1, "title": "沧县县委副书记", "start_date": "2024-12?", "end_date": "present", "rank": "正处", "note": "任县委副书记、代县长后转正"},
    {"person_id": 1, "org_id": 2, "title": "沧县代县长", "start_date": "2024-12", "end_date": "2025-01?", "rank": "正处", "note": "cangxian.gov.cn: 县委副书记、代县长贾卫元主持召开县政府第89次常务会议 (2025-01-20)"},
    {"person_id": 1, "org_id": 2, "title": "沧县县长", "start_date": "2025-01?", "end_date": "present", "rank": "正处", "note": "cangxian.gov.cn: 县委副书记、县长贾卫元主持召开县政府第90次常务会议 (2026-03-06)"},

    # 穆春江
    {"person_id": 2, "org_id": 1, "title": "沧县县委副书记", "start_date": "? ", "end_date": "2024-12", "rank": "正处", "note": "前任县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "沧县县长", "start_date": "?", "end_date": "2024-12", "rank": "正处", "note": "cangxian.gov.cn: 县委副书记、县长穆春江主持召开县政府第86次常务会议 (2024-09-29)"},

    # 宋立楠 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "沧县县委常委、常务副县长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "常务副县长"},

    # 谢丽红 — 组织部长
    {"person_id": 4, "org_id": 4, "title": "沧县县委常委、组织部部长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "组织部长"},

    # 李修丽 — 纪委书记
    {"person_id": 5, "org_id": 3, "title": "沧县县委常委、纪委书记、监委主任", "start_date": "?", "end_date": "present", "rank": "副处", "note": "纪委书记"},

    # 邢鹏 — 政法委书记
    {"person_id": 6, "org_id": 6, "title": "沧县县委常委、政法委书记", "start_date": "?", "end_date": "present", "rank": "副处", "note": "政法委书记"},

    # 王培江 — 县委办主任
    {"person_id": 7, "org_id": 7, "title": "沧县县委常委、县委办公室主任", "start_date": "?", "end_date": "present", "rank": "副处", "note": "县委办主任"},

    # 贾金周 — 宣传部长
    {"person_id": 8, "org_id": 5, "title": "沧县县委常委、宣传部部长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "宣传部长"},

    # 牛强 — 副县长
    {"person_id": 9, "org_id": 2, "title": "沧县人民政府副县长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "副县长"},

    # 于兴军 — 副县长
    {"person_id": 10, "org_id": 2, "title": "沧县人民政府副县长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "副县长"},

    # 刘建 — 副县长
    {"person_id": 11, "org_id": 2, "title": "沧县人民政府副县长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "副县长"},

    # 马瑞芳 — 副县长
    {"person_id": 12, "org_id": 2, "title": "沧县人民政府副县长", "start_date": "?", "end_date": "present", "rank": "副处", "note": "副县长"},
]

# ── RELATIONSHIPS ──
relationships = [
    # 贾卫元 — 穆春江 (前后任)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "穆春江为前任沧县县长，贾卫元接任", "overlap_org": "沧县人民政府", "overlap_period": "2024-12（交接）"},

    # 贾卫元 — 宋立楠 (工作搭档)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "贾卫元作为县长与常务副县长宋立楠县政府领导班子工作搭档", "overlap_org": "沧县人民政府", "overlap_period": "2024-12至今"},

    # 贾卫元 — 谢丽红 (县委班子成员)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "贾卫元(县委副书记)与谢丽红(组织部长)在沧县县委领导班子共事", "overlap_org": "中共沧县委员会", "overlap_period": "2024-12至今"},

    # 贾卫元 — 李修丽 (县委班子成员)
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "贾卫元(县委副书记)与李修丽(纪委书记)在沧县县委领导班子共事", "overlap_org": "中共沧县委员会", "overlap_period": "2024-12至今"},

    # 贾卫元 — 邢鹏 (县委班子成员)
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "贾卫元(县委副书记)与邢鹏(政法委书记)在沧县县委领导班子共事", "overlap_org": "中共沧县委员会", "overlap_period": "2024-12至今"},

    # 贾卫元 — 王培江 (县委班子成员)
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "贾卫元(县委副书记)与王培江(县委办主任)在沧县县委领导班子共事", "overlap_org": "中共沧县委员会", "overlap_period": "2024-12至今"},

    # 贾卫元 — 贾金周 (县委班子成员)
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "贾卫元(县委副书记)与贾金周(宣传部长)在沧县县委领导班子共事", "overlap_org": "中共沧县委员会", "overlap_period": "2024-12至今"},

    # 宋立楠 — 其他副县长 (政府班子)
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "宋立楠(常务副县长)与牛强(副县长)在沧县政府领导班子共事", "overlap_org": "沧县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "宋立楠(常务副县长)与于兴军(副县长)在沧县政府领导班子共事", "overlap_org": "沧县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "宋立楠(常务副县长)与刘建(副县长)在沧县政府领导班子共事", "overlap_org": "沧县人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "宋立楠(常务副县长)与马瑞芳(副县长)在沧县政府领导班子共事", "overlap_org": "沧县人民政府", "overlap_period": "至今"},
]

# ── RUN ──
if __name__ == "__main__":
    staging = PROJECT_ROOT / "data" / "tmp" / "hebei_沧县"
    staging.mkdir(parents=True, exist_ok=True)

    db_path = staging / "沧县_network.db"
    gexf_path = staging / "沧县_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print(f"Done. DB: {db_path}, GEXF: {gexf_path}")
