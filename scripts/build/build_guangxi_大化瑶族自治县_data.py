#!/usr/bin/env python3
"""Build the evidence-backed current leadership package for 大化瑶族自治县."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

for parent in Path(__file__).resolve().parents:
    if (parent / "gov_relation").is_dir():
        sys.path.insert(0, str(parent))
        break

from gov_relation.factory import InsertFactory, PersonJSONFactory
from gov_relation.runner import run_build


TASK_DIR = Path(__file__).resolve().parent
DB_PATH = TASK_DIR / "大化瑶族自治县_network.db"
GEXF_PATH = TASK_DIR / "大化瑶族自治县_network.gexf"
REPORT_PATH = TASK_DIR / "20260811-广西壮族自治区-河池市-大化瑶族自治县-领导班子调查报告.md"

PERSONS = [
    {
        "canonical_name": "韦鸿臻",
        "gender": "男",
        "ethnicity": "壮族",
        "birth_text": "1978-04",
        "education": "在职大学",
        "party_join_text": "中共党员",
        "_source_pk": "dahua-wei-hongzhen-1978-04",
    },
    {
        "canonical_name": "蓝胜",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth_text": "1969-10",
        "native_place": "广西都安",
        "education": "广西区委党校在职研究生",
        "party_join_text": "1998-05",
        "work_start_text": "1992-07",
        "_source_pk": "dahua-lan-sheng-1969-10",
    },
    {
        "canonical_name": "梁宁",
        "_source_pk": "dahua-liang-ning-former-secretary",
    },
    {
        "canonical_name": "韦峥臻",
        "_source_pk": "dahua-wei-zhengzhen-deputy-secretary",
    },
]

ORGANIZATIONS = [
    {
        "canonical_name": "中共大化瑶族自治县委员会",
        "organization_type": "party",
        "location_text": "广西河池大化瑶族自治县",
    },
    {
        "canonical_name": "大化瑶族自治县人民政府",
        "organization_type": "government",
        "location_text": "广西河池大化瑶族自治县",
    },
    {
        "canonical_name": "河池市文化广电体育和旅游局",
        "organization_type": "government_department",
        "location_text": "广西河池市",
    },
    {
        "canonical_name": "中共大化瑶族自治县都阳镇委员会",
        "organization_type": "party",
        "location_text": "广西河池大化瑶族自治县都阳镇",
    },
]

POSITIONS = [
    {
        "person_name": "韦鸿臻",
        "organization_name": "中共大化瑶族自治县委员会",
        "organization_text": "中共大化瑶族自治县委员会",
        "title": "县委书记",
        "start_text": "2026-02",
        "end_text": "至今",
        "is_current": 1,
        "sort_order": 0,
        "rank": "正处级",
        "confidence": "confirmed",
        "notes": "2026-01-26任前公示；2月25日已以县党委书记身份活动",
    },
    {
        "person_name": "韦鸿臻",
        "organization_name": "河池市文化广电体育和旅游局",
        "organization_text": "河池市文化广电体育和旅游局",
        "title": "党组书记、局长、一级调研员，市文物局局长（兼）",
        "start_text": "不晚于2024-08",
        "end_text": "2026-02",
        "sort_order": 10,
        "confidence": "confirmed",
    },
    {
        "person_name": "蓝胜",
        "organization_name": "大化瑶族自治县人民政府",
        "organization_text": "大化瑶族自治县人民政府",
        "title": "县委副书记、县长",
        "start_text": "不晚于2020-06",
        "end_text": "至今",
        "is_current": 1,
        "sort_order": 0,
        "rank": "正处级",
        "confidence": "confirmed",
    },
    {
        "person_name": "梁宁",
        "organization_name": "中共大化瑶族自治县委员会",
        "organization_text": "中共大化瑶族自治县委员会",
        "title": "前任县委书记",
        "start_text": "不晚于2022-12",
        "end_text": "2026-02",
        "sort_order": 0,
        "confidence": "confirmed",
        "notes": "2026-01-22仍主持县党委常委会；继任者2月到任",
    },
    {
        "person_name": "韦峥臻",
        "organization_name": "中共大化瑶族自治县委员会",
        "organization_text": "中共大化瑶族自治县委员会",
        "title": "县委副书记",
        "start_text": "不晚于2026-03",
        "end_text": "至今",
        "is_current": 1,
        "sort_order": 0,
        "confidence": "confirmed",
    },
    {
        "person_name": "韦峥臻",
        "organization_name": "中共大化瑶族自治县都阳镇委员会",
        "organization_text": "中共大化瑶族自治县都阳镇委员会",
        "title": "党委书记",
        "start_text": "不晚于2026-03",
        "end_text": "至今",
        "is_current": 1,
        "sort_order": 10,
        "confidence": "confirmed",
    },
]

RELATIONSHIPS = [
    {
        "person_from_name": "韦鸿臻",
        "person_to_name": "蓝胜",
        "relationship_type": "overlap",
        "direction": "undirected",
        "strength": "strong",
        "confidence": "confirmed",
        "context": "大化瑶族自治县现任党政主要领导搭班",
        "overlap_organization_text": "大化瑶族自治县",
        "overlap_period_text": "2026-02至今",
    },
    {
        "person_from_name": "梁宁",
        "person_to_name": "韦鸿臻",
        "relationship_type": "predecessor_successor",
        "direction": "from_to",
        "strength": "strong",
        "confidence": "confirmed",
        "context": "梁宁为韦鸿臻的直接前任大化瑶族自治县党委书记",
        "overlap_organization_text": "中共大化瑶族自治县委员会",
        "overlap_period_text": "2026-02交接",
    },
    {
        "person_from_name": "梁宁",
        "person_to_name": "蓝胜",
        "relationship_type": "overlap",
        "direction": "undirected",
        "strength": "strong",
        "confidence": "confirmed",
        "context": "前一届大化瑶族自治县党政主要领导搭班",
        "overlap_organization_text": "大化瑶族自治县",
        "overlap_period_text": "不晚于2022-12至2026-02",
    },
]

SOURCES = [
    {
        "canonical_url": "http://www.gxdh.gov.cn/xxgk/ldjj/xz/hdbd/t27865762.shtml",
        "title": "韦鸿臻主持召开专题会议，听取专项巡察工作汇报",
        "publisher": "大化瑶族自治县人民政府门户网站",
        "published_at": "2026-07-07",
        "accessed_at": "2026-08-11",
        "source_type": "official",
        "reliability": "high",
    },
    {
        "canonical_url": "http://www.gxdh.gov.cn/xxgk/ldjj/xz/hdbd/t27855814.shtml",
        "title": "蓝胜主持召开自治县政府常务会议",
        "publisher": "大化瑶族自治县人民政府门户网站",
        "published_at": "2026-07-03",
        "accessed_at": "2026-08-11",
        "source_type": "official",
        "reliability": "high",
    },
    {
        "canonical_url": "http://www.gxdh.gov.cn/xxgk/ldjj/xz/hdbd/t27329694.shtml",
        "title": "韦鸿臻主持召开自治县党委常委会会议",
        "publisher": "大化瑶族自治县人民政府门户网站",
        "published_at": "2026-03-09",
        "accessed_at": "2026-08-11",
        "source_type": "official",
        "reliability": "high",
    },
    {
        "canonical_url": "http://www.gxdh.gov.cn/xxgk/ldjj/xz/hdbd/t27178441.shtml",
        "title": "梁宁主持召开自治县党委常委会会议",
        "publisher": "大化瑶族自治县人民政府门户网站",
        "published_at": "2026-01-23",
        "accessed_at": "2026-08-11",
        "source_type": "official",
        "reliability": "high",
    },
    {
        "canonical_url": "https://finance.sina.com.cn/jjxw/2026-01-26/doc-inhirukr8159754.shtml",
        "title": "广西发布一批领导干部任职前公示",
        "publisher": "广西日报（新浪转载）",
        "published_at": "2026-01-26",
        "accessed_at": "2026-08-11",
        "source_type": "appointment_notice",
        "reliability": "medium",
    },
    {
        "canonical_url": "https://www.gxnews.com.cn/staticpages/20260213/newgx698ed67d-21907891.shtml",
        "title": "广西5市发布最新人事信息",
        "publisher": "广西新闻网",
        "published_at": "2026-02-13",
        "accessed_at": "2026-08-11",
        "source_type": "media",
        "reliability": "high",
    },
    {
        "canonical_url": "https://gx.people.com.cn/n2/2023/0113/c179464-40265909.html",
        "title": "人民网专访广西人大代表、大化瑶族自治县县长蓝胜",
        "publisher": "人民网广西频道",
        "published_at": "2023-01-13",
        "accessed_at": "2026-08-11",
        "source_type": "media",
        "reliability": "high",
    },
    {
        "canonical_url": "https://www.gx.news.cn/20250116/436d4a981f894d5194c84ff1ac8ad580/c.html",
        "title": "蓝胜：筑底强基谋篇布局，共绘大化高质量发展美好蓝图",
        "publisher": "新华网",
        "published_at": "2025-01-16",
        "accessed_at": "2026-08-11",
        "source_type": "media",
        "reliability": "high",
    },
]


def add_evidence(conn: sqlite3.Connection) -> None:
    inserts = InsertFactory()
    people = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    source_ids = dict(conn.execute("SELECT canonical_url, source_id FROM sources"))
    evidence = {
        "韦鸿臻": [0, 2, 4, 5],
        "蓝胜": [0, 1, 6, 7],
        "梁宁": [3],
        "韦峥臻": [0, 2],
    }
    for name, indexes in evidence.items():
        for index in indexes:
            inserts.link_evidence(
                conn,
                source_ids[SOURCES[index]["canonical_url"]],
                "person",
                people[name],
                "identity_and_career",
            )
    for position_id, name in conn.execute(
        """SELECT p.position_id, pe.canonical_name
           FROM positions p JOIN persons pe ON pe.person_id=p.person_id"""
    ):
        for index in evidence[name]:
            inserts.link_evidence(
                conn,
                source_ids[SOURCES[index]["canonical_url"]],
                "position",
                position_id,
                "office_and_period",
            )
    for relationship_id in conn.execute(
        "SELECT relationship_id FROM relationships"
    ):
        for index in (0, 1, 2, 3):
            inserts.link_evidence(
                conn,
                source_ids[SOURCES[index]["canonical_url"]],
                "relationship",
                relationship_id[0],
                "leadership_overlap_or_succession",
            )
    conn.commit()


def write_profiles(conn: sqlite3.Connection) -> None:
    factory = PersonJSONFactory()
    settings = {
        "韦鸿臻": {
            "job": "县委书记",
            "career": "partial",
            "specializations": ["文化旅游", "县域产业", "巡视整改"],
            "questions": [
                "2019年任河池市接待办公室主任以前及文旅局任职起始时间待补",
                "2026年2月正式任命大化县党委书记的原始文件待取得",
            ],
        },
        "蓝胜": {
            "job": "县长",
            "career": "thin",
            "specializations": ["特色农业", "乡村振兴", "文旅融合"],
            "questions": [
                "1992年至出任大化县长前的完整履历缺少官方简历",
                "正式当选大化瑶族自治县县长的日期待人大公告核定",
            ],
        },
    }
    for name, config in settings.items():
        person_id = conn.execute(
            "SELECT person_id FROM persons WHERE canonical_name=?", (name,)
        ).fetchone()[0]
        profile = factory.build(conn, person_id)
        profile["schema_version"] = "1.0"
        profile["investigation_scope"] = {
            "province": "广西壮族自治区",
            "city": "河池市",
            "region": "大化瑶族自治县",
            "job": config["job"],
            "task_id": "guangxi_大化瑶族自治县",
            "time_focus": "截至2026-08-11",
        }
        profile["current_status"]["as_of"] = "2026-08-11"
        profile["current_status"]["is_current_confirmed"] = True
        profile["professional_profile"] = {
            "primary_specializations": config["specializations"],
            "career_pattern": "local_or_prefecture_rotation",
        }
        profile["confidence_summary"] = {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": config["career"],
            "relationship_confidence": "high",
            "biggest_gap": config["questions"][0],
        }
        profile["open_questions"] = [
            {
                "priority": "high",
                "question": question,
                "why_it_matters": "完善身份去重和干部流动时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": "2026-08-11",
            }
            for question in config["questions"]
        ]
        path = TASK_DIR / (
            f"20260811-广西壮族自治区-河池市-大化瑶族自治县-"
            f"{config['job']}-{name}.json"
        )
        path.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def write_report() -> None:
    REPORT_PATH.write_text(
        """# 大化瑶族自治县现任领导与书记交接调查

**核验日期：** 2026-08-11  
**任务：** `guangxi_大化瑶族自治县`

## 当前党政主官

| 人物 | 当前职务 | 当前性 | 核心证据 |
|---|---|---|---|
| 韦鸿臻 | 大化瑶族自治县党委书记 | confirmed | 大化政府网 2026-03-06、2026-07-03活动报道 |
| 蓝胜 | 大化瑶族自治县党委副书记、县长 | confirmed | 大化政府网 2026-07-02政府常务会议 |

## 书记交接

- 2026年1月22日，梁宁仍以自治县党委书记身份主持常委会。
- 2026年1月26日，韦鸿臻以河池市文广体旅局党组书记、局长、一级调研员身份获公示拟任县级党政正职。
- 2026年2月12日，河池市人大常委会免去韦鸿臻原市文广体旅局局长职务。
- 2026年3月6日及以后，官方报道持续确认韦鸿臻任自治县党委书记。

据此可确认梁宁—韦鸿臻为直接前后任关系，交接窗口在2026年2月。未取得单独的书记任命全文，因此精确日期保留为开放问题。

## 公开履历和治理重点

- 韦鸿臻，男，壮族，1978年4月生，在职大学，中共党员；此前任河池市文化广电体育和旅游局党组书记、局长、一级调研员，兼市文物局局长。到任后公开工作聚焦产业复工、项目建设、巡视整改与基层矛盾治理。
- 蓝胜，男，瑶族，1969年10月生，广西都安人，区委党校在职研究生；至少自2020年6月起任大化县长。公开工作重点包括七百弄鸡、羊、鱼等特色农业，乡村振兴、文旅融合和重大项目建设。

## 关系边界

韦鸿臻—蓝胜、梁宁—蓝胜仅表示公开任职重叠；梁宁—韦鸿臻表示正式职务前后任，不推断私人关系。

## 开放问题

- 韦鸿臻2019年以前及河池市文广体旅局任职起始时间待补。
- 蓝胜1992年至出任大化县长前的完整履历待官方简历补齐。
- 书记交接和蓝胜正式当选县长的精确人大/党委文件待取得。
""",
        encoding="utf-8",
    )


def main() -> None:
    run_build(
        slug="大化瑶族自治县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        sources=SOURCES,
        claims=[],
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        backend="v3",
        overwrite=True,
    )
    conn = sqlite3.connect(DB_PATH)
    try:
        add_evidence(conn)
        write_profiles(conn)
    finally:
        conn.close()
    write_report()


if __name__ == "__main__":
    main()
