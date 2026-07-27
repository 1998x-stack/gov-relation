#!/usr/bin/env python3
"""
河北省沧州市东光县领导班子工作关系网络 — 2026-07-24
research_date: 2026-07-24
sources:
  - dongguang.gov.cn — 县政府领导工作分工 东政发〔2026〕5号 (2026-02-13)
  - dongguang.gov.cn — 县政府领导工作分工 东政发〔2024〕9号 (2024-08-28)
  - dongguang.gov.cn — 县政府领导工作分工 东政发〔2023〕1号 (2023-04-04)
  - dongguang.gov.cn — 县政府县长、副县长工作分工 东政发〔2021〕8号 (2021-12-01)
  - dongguang.gov.cn — 2026纸箱包装机械国际博览会 (2026-04-27)
  - dongguang.gov.cn — 县第十三届人民政府第六十四次常务会议 (2026-05-08)
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
# DB_PATH = DATABASE_DIR / "东光县_network.db"
# GEXF_PATH = GRAPH_DIR / "东光县_network.gexf"

SLUG = "东光县"

# ── PERSONS ──
persons = [
    # ===== Current county leaders (as of 2026-04+) =====
    {
        "id": 1,
        "name": "宋吉利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县委书记",
        "current_org": "中共东光县委",
        "source": "dongguang.gov.cn — 2026纸箱包装机械国际博览会报道 (2026-04-24); 东政发〔2021〕8号 (曾任东光县长2021-约2025)",
    },
    {
        "id": 2,
        "name": "唐景越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县委副书记、县长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 县第十三届人民政府第六十四次常务会议 (2026-05-08)",
    },
    {
        "id": 3,
        "name": "王健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县委常委、常务副县长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 东政发〔2024〕9号 (2024-08-28); 东政发〔2023〕1号 (2023-03)",
    },
    {
        "id": 4,
        "name": "卢万顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县政府党组成员、副县长、县公安局局长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 东政发〔2024〕9号; 东政发〔2023〕1号; 东政发〔2021〕8号 (连续任职至少自2021年起)",
    },
    {
        "id": 5,
        "name": "王秀民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县政府党组成员、副县长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 东政发〔2023〕1号 (原负责工业经济，现负责农业农村)",
    },
    {
        "id": 6,
        "name": "江兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县政府党组成员、副县长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 东政发〔2024〕9号; 东政发〔2023〕1号 (2023年为副县长候选人)",
    },
    {
        "id": 7,
        "name": "邓志英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县政府党组成员、副县长",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 东政发〔2026〕5号 (2026-02-13); 县第十三届人民政府第六十四次常务会议 (2026-05-08)",
    },
    # ===== Other current county leaders =====
    {
        "id": 8,
        "name": "陈桂鹏",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县领导（县委副书记或县委常委）",
        "current_org": "中共东光县委",
        "source": "dongguang.gov.cn — 县第十三届人民政府第六十四次常务会议 (2026-05-08) 列名出席",
    },
    {
        "id": 9,
        "name": "王洪源",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县领导",
        "current_org": "东光县人民政府",
        "source": "dongguang.gov.cn — 县第十三届人民政府第六十四次常务会议 (2026-05-08) 列名出席",
    },
    {
        "id": 10,
        "name": "刘福生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县人大常委会主任",
        "current_org": "东光县人大常委会",
        "source": "dongguang.gov.cn — 2026纸箱包装机械国际博览会报道 (2026-04-24)",
    },
    # ===== Previous leaders (for relations) =====
    {
        "id": 11,
        "name": "马占芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "",
        "source": "dongguang.gov.cn — 东政发〔2024〕9号 (2024-08,时任县长); 东政发〔2023〕1号 (2023-03,时任县长). 前任东光县长。",
    },
    {
        "id": 12,
        "name": "康利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "",
        "source": "dongguang.gov.cn — 东政发〔2021〕8号 (2021-07,时任常务副县长). 前任东光常务副县长。",
    },
    {
        "id": 13,
        "name": "曹秀华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "dongguang.gov.cn — 东政发〔2023〕1号 (2023-03,时任副县长); 东政发〔2021〕8号 (2021-07,时任副县长). 负责教育、卫健等，2026年被邓志英接替。",
    },
    {
        "id": 14,
        "name": "王国臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "东光县领导（人大或副县长转任）",
        "current_org": "东光县人大常委会",
        "source": "dongguang.gov.cn — 2026纸箱包装机械国际博览会报道 (2026-04-24); 东政发〔2024〕9号 (时任副县长); 东政发〔2021〕8号 (时任副县长)",
    },
    {
        "id": 15,
        "name": "李辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "",
        "source": "dongguang.gov.cn — 东政发〔2021〕8号 (2021-07,时任副县长). 负责城建、交通等。",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共东光县委", "type": "党委", "level": "县级", "location": "东光县"},
    {"id": 2, "name": "东光县人民政府", "type": "政府", "level": "县级", "location": "东光县"},
    {"id": 3, "name": "东光县人大常委会", "type": "人大", "level": "县级", "location": "东光县"},
    {"id": 4, "name": "东光县公安局", "type": "政府", "level": "县级", "location": "东光县"},
    {"id": 5, "name": "东光县政协", "type": "政协", "level": "县级", "location": "东光县"},
    {"id": 6, "name": "东光县纪委监委", "type": "党委", "level": "县级", "location": "东光县"},
    {"id": 7, "name": "东光经济开发区", "type": "开发区", "level": "县级", "location": "东光县"},
]

# ── POSITIONS ──
positions = [
    # Current
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "约2025", "end": "present", "rank": "正处级", "note": "前县长晋升"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "约2025", "end": "present", "rank": "正处级", "note": "接替马占芳"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "2023", "end": "present", "rank": "副处级"},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、副县长、县公安局局长", "start": "2021", "end": "present", "rank": "副处级"},
    {"person_id": 5, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2021", "end": "present", "rank": "副处级"},
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2023", "end": "present", "rank": "副处级"},
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2025/2026", "end": "present", "rank": "副处级"},
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级"},
    # Previous
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start": "2021-07", "end": "约2025", "rank": "正处级", "note": "前任县长，后晋升县委书记"},
    {"person_id": 11, "org_id": 2, "title": "县委副书记、县长", "start": "2023-03", "end": "约2025", "rank": "正处级", "note": "接替宋吉利"},
    {"person_id": 12, "org_id": 2, "title": "县委常委、常务副县长", "start": "2021-07", "end": "约2023", "rank": "副处级", "note": "接替康利的为王健"},
    {"person_id": 13, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2021-07", "end": "约2025", "rank": "副处级"},
    {"person_id": 14, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2021-07", "end": "约2025", "rank": "副处级"},
    {"person_id": 14, "org_id": 3, "title": "县领导（人大）", "start": "约2025", "end": "present", "rank": "正处级", "note": "从副县长转任人大"},
    {"person_id": 15, "org_id": 2, "title": "县政府党组成员、副县长", "start": "2021-07", "end": "约2023/2024", "rank": "副处级"},
]

# ── RELATIONSHIPS ──
relationships = [
    # Predecessor-successor: 县长
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "宋吉利→马占芳 东光县长交接（约2023）", "overlap_org": "东光县人民政府", "overlap_period": "2023"},
    {"person_a": 11, "person_b": 2, "type": "predecessor_successor", "context": "马占芳→唐景越 东光县长交接（约2025）", "overlap_org": "东光县人民政府", "overlap_period": "约2025"},
    # Predecessor-successor: 书记
    {"person_a": "未知前任", "person_b": 1, "type": "predecessor_successor", "context": "前任县委书记与宋吉利交接（约2025）", "overlap_org": "中共东光县委", "overlap_period": "约2025"},
    # Working overlap: 县长团队 (宋吉利+王健)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "宋吉利(县长)与王健(常务副县长)搭班子2021-约2025", "overlap_org": "东光县人民政府", "overlap_period": "2021-约2025", "strength": "strong"},
    # Working overlap: 县长团队 (马占芳+王健)
    {"person_a": 11, "person_b": 3, "type": "overlap", "context": "马占芳(县长)与王健(常务副县长)搭班子2023-约2025", "overlap_org": "东光县人民政府", "overlap_period": "2023-约2025", "strength": "strong"},
    # Working overlap: 县长团队 (唐景越+王健)
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "唐景越(县长)与王健(常务副县长)搭档2025-present", "overlap_org": "东光县人民政府", "overlap_period": "约2025-present", "strength": "strong"},
    # Long-serving team: 卢万顺 with 宋吉利
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "宋吉利(县长/书记)与卢万顺(公安局长)共事2021-约2025", "overlap_org": "东光县人民政府", "overlap_period": "2021-约2025", "strength": "strong"},
    # Long-serving team: 卢万顺 with 王健
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "王健(常务副县长)与卢万顺(公安局长)共事2023-present", "overlap_org": "东光县人民政府", "overlap_period": "2023-present", "strength": "strong"},
    # Long-serving team: 王秀民 with all
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "宋吉利(县长/书记)与王秀民(副县长)共事2021-present", "overlap_org": "东光县人民政府", "overlap_period": "2021-present", "strength": "strong"},
    {"person_a": 5, "person_b": 4, "type": "overlap", "context": "王秀民与卢万顺长期共事2021-present", "overlap_org": "东光县人民政府", "overlap_period": "2021-present", "strength": "strong"},
    {"person_a": 5, "person_b": 3, "type": "overlap", "context": "王秀民与王健共事2023-present", "overlap_org": "东光县人民政府", "overlap_period": "2023-present", "strength": "strong"},
    # 江兵 with team
    {"person_a": 6, "person_b": 3, "type": "overlap", "context": "王健(常务副县长)与江兵(副县长)共事2023-present", "overlap_org": "东光县人民政府", "overlap_period": "2023-present", "strength": "strong"},
    {"person_a": 6, "person_b": 4, "type": "overlap", "context": "江兵与卢万顺共事2023-present", "overlap_org": "东光县人民政府", "overlap_period": "2023-present", "strength": "medium"},
    # 邓志英 (replaced 曹秀华)
    {"person_a": 13, "person_b": 7, "type": "predecessor_successor", "context": "曹秀华→邓志英 教育卫生副县长交接（约2025/2026）", "overlap_org": "东光县人民政府", "overlap_period": "约2025/2026"},
    # 王国臣 transition
    {"person_a": 14, "person_b": 4, "type": "overlap", "context": "王国臣与卢万顺长期共事2021-present", "overlap_org": "东光县人民政府", "overlap_period": "2021-present", "strength": "strong"},
    # 康利→王健 (常务副县长交接)
    {"person_a": 12, "person_b": 3, "type": "predecessor_successor", "context": "康利→王健 常务副县长交接（约2023）", "overlap_org": "东光县人民政府", "overlap_period": "约2023"},
    # 李辉 (离任)
    {"person_a": 15, "person_b": 4, "type": "overlap", "context": "李辉与卢万顺共事2021-约2023", "overlap_org": "东光县人民政府", "overlap_period": "2021-约2023", "strength": "medium"},
]


if __name__ == "__main__":
    staging = Path(__file__).parent
    db_path = staging / "东光县_network.db"
    gexf_path = staging / "东光县_network.gexf"

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

    print(f"\n✅ Build complete for {SLUG}")
    print(f"   DB:   {db_path}")
    print(f"   GEXF: {gexf_path}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs:    {len(organizations)}")
    print(f"   Pos:     {len(positions)}")
    print(f"   Rel:     {len(relationships)}")
