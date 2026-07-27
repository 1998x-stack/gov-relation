#!/usr/bin/env python3
"""
河北省保定市高阳县领导班子工作关系网络 — 2026-07-23
research_date: 2026-07-23
sources: gaoyang.gov.cn leadership page, news articles (infoid 10171, 11166, 11648, 10858, etc.)
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "高阳县"

# ── PERSONS ──
persons = [
    # Current county leaders (as of 2026-02-14+)
    {
        "id": 1,
        "name": "齐志国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "高阳县委书记",
        "current_org": "中共高阳县委员会",
        "source": "gaoyang.gov.cn article 11648 (2026-02-14), previously served as 高阳县长/代县长",
    },
    {
        "id": 2,
        "name": "赵胜男",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "高阳县委副书记、代县长",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 11648 (2026-02-14), leadership page lists first",
    },
    # Previous county leaders
    {
        "id": 3,
        "name": "蒋东方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "",
        "source": "gaoyang.gov.cn articles: served as 县长 (infoid ~9000+), then 县委书记 (infoid ~10000-11648). Replaced by 齐志国 as 县委书记 around 2026",
    },
    # County government leaders
    {
        "id": 4,
        "name": "回彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "高阳县副县长候选人（分工常务工作）",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page (ldzc.asp?infoid=544)",
    },
    {
        "id": 5,
        "name": "梁伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page and article 10171 (2023-08-07 flood inspection)",
    },
    {
        "id": 6,
        "name": "梁恒",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    {
        "id": 7,
        "name": "杨进忠",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    {
        "id": 8,
        "name": "贾英超",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    {
        "id": 9,
        "name": "韩立通",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    {
        "id": 10,
        "name": "刘影",
        "gender": "女",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    {
        "id": 11,
        "name": "代志伟",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn leadership page",
    },
    # Additional county leaders mentioned in news
    {
        "id": 12,
        "name": "黄明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 10171 (2023-08 flood inspection), article 11648 (2026-02 Spring Festival慰问)",
    },
    {
        "id": 13,
        "name": "续金明",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 11648 (2026-02 Spring Festival慰问)",
    },
    {
        "id": 14,
        "name": "范海金",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 10171 (2023-08 flood inspection), 11648 (2026-02)",
    },
    {
        "id": 15,
        "name": "黄旺",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 11648 (2026-02 Spring Festival慰问)",
    },
    {
        "id": 16,
        "name": "魏双振",
        "gender": "男",
        "birth": "待查",
        "current_post": "高阳县领导",
        "current_org": "高阳县人民政府",
        "source": "gaoyang.gov.cn article 11648 (2026-02 Spring Festival慰问)",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共高阳县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共保定市委员会",
        "location": "河北省保定市高阳县",
    },
    {
        "id": 2,
        "name": "高阳县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "保定市人民政府",
        "location": "河北省保定市高阳县",
    },
]

# ── POSITIONS ──
positions = [
    # 齐志国
    {"person_id": 1, "org_id": 1, "title": "高阳县委书记", "start_date": "约2026", "end_date": "至今", "rank": "正处级", "note": "从县长/代县长晋升为县委书记"},
    {"person_id": 1, "org_id": 2, "title": "高阳县长", "start_date": "约2024（代）", "end_date": "约2026", "rank": "正处级", "note": "从代县长转为县长"},
    {"person_id": 1, "org_id": 2, "title": "高阳代县长", "start_date": "约2023", "end_date": "约2024", "rank": "正处级", "note": "接替蒋东方"},
    # 赵胜男
    {"person_id": 2, "org_id": 2, "title": "高阳县委副书记、代县长", "start_date": "约2026-02", "end_date": "至今", "rank": "正处级", "note": "接替齐志国任代县长"},
    # 蒋东方
    {"person_id": 3, "org_id": 1, "title": "高阳县委书记", "start_date": "约2022-2023", "end_date": "约2026", "rank": "正处级", "note": "从县长晋升"},
    {"person_id": 3, "org_id": 2, "title": "高阳县长", "start_date": "约2020-2021", "end_date": "约2022-2023", "rank": "正处级", "note": ""},
    # 回彬
    {"person_id": 4, "org_id": 2, "title": "高阳县副县长（常务）", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "县政府官网领导之窗列为副县长候选人(分工常务工作)"},
    # Other leaders
    {"person_id": 5, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "最早见于2023年8月报道"},
    {"person_id": 6, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "连续在2023-2026年报道中出现"},
    {"person_id": 13, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "高阳县领导", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ──
relationships = [
    # 齐志国 ↔ 蒋东方: 前后任 (succession chain)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "齐志国接替蒋东方任高阳县委书记",
        "overlap_org": "中共高阳县委员会",
        "overlap_period": "约2023-2026",
    },
    # 齐志国 ↔ 赵胜男: 前后任 (succession chain 县长)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "赵胜男接替齐志国任代县长（齐志国升任县委书记后）",
        "overlap_org": "高阳县人民政府",
        "overlap_period": "约2026-02",
    },
    # 蒋东方 ↔ 齐志国: 搭档转交接
    {
        "person_a": 3,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "蒋东方任县委书记时，齐志国任县长/代县长",
        "overlap_org": "高阳县党政领导班子",
        "overlap_period": "约2023-2026",
    },
    # 齐志国 ↔ 黄明: 共同出席活动
    {
        "person_a": 1,
        "person_b": 12,
        "type": "overlap",
        "context": "齐志国与黄明共同参加2026春节慰问活动",
        "overlap_org": "高阳县党政领导班子",
        "overlap_period": "2023-2026",
    },
    # 赵胜男 ↔ 黄明: 共同出席活动
    {
        "person_a": 2,
        "person_b": 12,
        "type": "overlap",
        "context": "赵胜男与黄明共同参加2026春节慰问活动",
        "overlap_org": "高阳县党政领导班子",
        "overlap_period": "2026-02",
    },
    # 黄明 ↔ 范海金: 长期共同任职
    {
        "person_a": 12,
        "person_b": 14,
        "type": "overlap",
        "context": "黄明与范海金在2023年防汛检查和2026年春节慰问活动中同时出席",
        "overlap_org": "高阳县党政领导班子",
        "overlap_period": "2023-2026",
    },
]


def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "高阳县_network.db")
    gexf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "高阳县_network.gexf")

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


if __name__ == "__main__":
    main()
