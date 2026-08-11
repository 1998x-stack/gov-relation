#!/usr/bin/env python3
"""Build the evidence-backed current leadership package for 南丹县."""

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
DB_PATH = TASK_DIR / "南丹县_network.db"
GEXF_PATH = TASK_DIR / "南丹县_network.gexf"
REPORT_PATH = TASK_DIR / "20260811-广西壮族自治区-河池市-南丹县-领导班子增量报告.md"

PERSONS = [
    {
        "canonical_name": "黄建辉",
        "gender": "男",
        "ethnicity": "壮族",
        "birth_text": "1979-09",
        "native_place": "广西大新",
        "education": "大学",
        "party_join_text": "2004-07",
        "_source_pk": "nandan-huang-jianhui-1979-09",
    },
    {
        "canonical_name": "闻飞熊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth_text": "1981-12",
        "education": "大学",
        "_source_pk": "nandan-wen-feixiong-1981-12",
    },
]

ORGANIZATIONS = [
    {"canonical_name": "中共南丹县委员会", "organization_type": "party", "location_text": "广西河池南丹县"},
    {"canonical_name": "南丹县人民政府", "organization_type": "government", "location_text": "广西河池南丹县"},
    {"canonical_name": "中共扶绥县委员会", "organization_type": "party", "location_text": "广西崇左扶绥县"},
    {"canonical_name": "扶绥县人民政府", "organization_type": "government", "location_text": "广西崇左扶绥县"},
    {"canonical_name": "广西凭祥综合保税区管理委员会", "organization_type": "development_zone", "location_text": "广西崇左凭祥市"},
    {"canonical_name": "中共河池市委组织部", "organization_type": "party_department", "location_text": "广西河池市"},
    {"canonical_name": "中共环江毛南族自治县委员会", "organization_type": "party", "location_text": "广西河池环江毛南族自治县"},
]

POSITIONS = [
    {
        "person_name": "黄建辉", "organization_name": "中共南丹县委员会",
        "organization_text": "中共南丹县委员会", "title": "县委书记",
        "start_text": "2025-10", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副厅级", "confidence": "confirmed",
    },
    {
        "person_name": "黄建辉", "organization_name": "广西凭祥综合保税区管理委员会",
        "organization_text": "广西凭祥综合保税区管理委员会",
        "title": "党工委副书记、管委会常务副主任",
        "start_text": "2025-03", "end_text": "2025-10", "sort_order": 10,
        "rank": "副厅级", "confidence": "confirmed",
    },
    {
        "person_name": "黄建辉", "organization_name": "中共扶绥县委员会",
        "organization_text": "中共扶绥县委员会", "title": "县委书记",
        "start_text": "不晚于2022-02", "end_text": "2025-03", "sort_order": 20,
        "confidence": "confirmed",
    },
    {
        "person_name": "黄建辉", "organization_name": "扶绥县人民政府",
        "organization_text": "扶绥县人民政府", "title": "县委副书记、县长",
        "start_text": "2020-05", "end_text": "未知", "sort_order": 30,
        "confidence": "plausible", "notes": "公开报道确认曾任，书记接任月仍待官方任免文书核定",
    },
    {
        "person_name": "闻飞熊", "organization_name": "南丹县人民政府",
        "organization_text": "南丹县人民政府", "title": "县委副书记、县长",
        "start_text": "2025-05前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "confidence": "confirmed",
    },
    {
        "person_name": "闻飞熊", "organization_name": "中共河池市委组织部",
        "organization_text": "中共河池市委组织部",
        "title": "副部长（分管日常工作）、一级调研员",
        "start_text": "未知", "end_text": "2025-02", "sort_order": 10,
        "confidence": "confirmed",
    },
    {
        "person_name": "闻飞熊", "organization_name": "中共环江毛南族自治县委员会",
        "organization_text": "中共环江毛南族自治县委员会", "title": "县委副书记",
        "start_text": "不晚于2023-03", "end_text": "未知", "sort_order": 20,
        "confidence": "plausible",
    },
]

RELATIONSHIPS = [
    {
        "person_from_name": "黄建辉", "person_to_name": "闻飞熊",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "南丹县现任党政主要领导搭班",
        "overlap_organization_text": "南丹县",
        "overlap_period_text": "2025-10至今",
    }
]

SOURCES = [
    {
        "canonical_url": "https://ssw.gxrb.com.cn/json/interface/epaper/api.php?code=01&date=2026-07-06&name=hcrb&xuhao=4",
        "title": "朱会东到金城江南丹督导调研时强调：全力以赴推进项目建设",
        "publisher": "河池日报", "published_at": "2026-07-06",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "high",
    },
    {
        "canonical_url": "https://ssw.gxrb.com.cn/json/interface/epaper/api.php?code=001&date=2025-11-03&name=gxrb&xuhao=7",
        "title": "关键金属的广西担当", "publisher": "广西日报",
        "published_at": "2025-11-03", "accessed_at": "2026-08-11",
        "source_type": "media", "reliability": "high",
    },
    {
        "canonical_url": "https://wsjkw.gxzf.gov.cn/xwdt_49370/xwdtzs/t11302611.shtml",
        "title": "广西卫生职业技术学院与扶绥县举行校地合作洽谈会",
        "publisher": "广西壮族自治区卫生健康委员会", "published_at": "2022-02-18",
        "accessed_at": "2026-08-11", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "https://finance.sina.com.cn/jjxw/2025-10-27/doc-infviaax0816191.shtml",
        "title": "前任县委书记落马后，广西南丹3个月内再换县委书记",
        "publisher": "澎湃新闻（新浪转载）", "published_at": "2025-10-27",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://www.sohu.com/a/865655530_121123734",
        "title": "广西5市发布领导干部任职前公示",
        "publisher": "搜狐（转载河池市委组织部公示）", "published_at": "2025-02-27",
        "accessed_at": "2026-08-11", "source_type": "appointment_notice", "reliability": "medium",
    },
    {
        "canonical_url": "https://kandian.sina.cn/article_2035321844_m79508bf403301fkpw.html?from=news&subch=onews",
        "title": "河池市五届人大七次会议代表通道｜闻飞熊：把南丹打造为全国关键金属高质量发展示范基地",
        "publisher": "河池融媒（新浪转载）", "published_at": "2026-02-27",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://www.sohu.com/a/651838742_121106875",
        "title": "环江纪念三八节暨全县女子体育比赛",
        "publisher": "环江融媒（搜狐转载）", "published_at": "2023-03-07",
        "accessed_at": "2026-08-11", "source_type": "media", "reliability": "medium",
    },
]


def add_evidence(conn: sqlite3.Connection) -> None:
    inserts = InsertFactory()
    people = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    source_ids = dict(conn.execute("SELECT canonical_url, source_id FROM sources"))
    by_person = {
        "黄建辉": [0, 1, 2, 3],
        "闻飞熊": [1, 4, 5, 6],
    }
    for name, indexes in by_person.items():
        for index in indexes:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "person", people[name], "identity_and_career",
            )
    for position_id, name, title in conn.execute(
        """SELECT p.position_id, pe.canonical_name, p.title
           FROM positions p JOIN persons pe ON pe.person_id=p.person_id"""
    ):
        indexes = by_person[name]
        if name == "黄建辉" and title == "县委书记":
            indexes = [0, 1, 3]
        elif name == "闻飞熊" and title == "县委副书记、县长":
            indexes = [1, 5]
        for index in indexes:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "position", position_id, "office_and_period",
            )
    relationship_id = conn.execute(
        "SELECT relationship_id FROM relationships"
    ).fetchone()[0]
    inserts.link_evidence(
        conn, source_ids[SOURCES[1]["canonical_url"]],
        "relationship", relationship_id, "joint_leadership",
    )
    conn.commit()


def write_profiles(conn: sqlite3.Connection) -> None:
    factory = PersonJSONFactory()
    settings = {
        "黄建辉": {
            "job": "县委书记",
            "questions": [
                "1979年9月出生信息需取得原始干部公示复核",
                "扶绥县长转任县委书记的精确月份及更早履历待官方简历补齐",
            ],
            "career": "partial",
            "specializations": ["县域治理", "产业园区", "关键金属产业"],
        },
        "闻飞熊": {
            "job": "县长",
            "questions": [
                "出生地、入党和参加工作时间尚缺官方来源",
                "环江任职前履历及调任河池市委组织部的精确时间待补",
                "南丹县长的正式人大选举日期待核定",
            ],
            "career": "thin",
            "specializations": ["组织工作", "乡村振兴", "关键金属产业"],
        },
    }
    for person_id, name in conn.execute(
        "SELECT person_id, canonical_name FROM persons ORDER BY canonical_name"
    ):
        profile = factory.build(conn, person_id)
        config = settings[name]
        profile["schema_version"] = "1.0"
        profile["investigation_scope"] = {
            "province": "广西壮族自治区", "city": "河池市",
            "region": "南丹县", "job": config["job"],
            "task_id": "guangxi_南丹县", "time_focus": "截至2026-08-11",
        }
        profile["current_status"]["as_of"] = "2026-08-11"
        profile["current_status"]["is_current_confirmed"] = True
        profile["professional_profile"] = {
            "primary_specializations": config["specializations"],
            "career_pattern": "cross_county_rotation",
        }
        profile["confidence_summary"] = {
            "identity": "confirmed", "current_role": "confirmed",
            "career_completeness": config["career"],
            "relationship_confidence": "high",
            "biggest_gap": config["questions"][0],
        }
        profile["open_questions"] = [
            {
                "priority": "high", "question": question,
                "why_it_matters": "完善身份去重与干部流动时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": "2026-08-11",
            }
            for question in config["questions"]
        ]
        filename = (
            f"20260811-广西壮族自治区-河池市-南丹县-{config['job']}-{name}.json"
        )
        (TASK_DIR / filename).write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def write_report() -> None:
    REPORT_PATH.write_text(
        """# 南丹县现任党政主官增量调查

**核验日期：** 2026-08-11  
**任务：** `guangxi_南丹县`

## 当前领导

| 人物 | 当前职务 | 当前性判断 | 主要证据 |
|---|---|---|---|
| 黄建辉 | 南丹县委书记、河池市人大常委会副主任 | confirmed | 河池日报 2026-07-06 |
| 闻飞熊 | 南丹县委副书记、县长 | confirmed | 河池融媒 2026-02-27；广西日报 2025-11-03 |

## 履历摘要

- 黄建辉：曾任扶绥县县长、县委书记；2025年3月任广西凭祥综合保税区党工委副书记、管委会常务副主任；2025年10月调任南丹县委书记。
- 闻飞熊：曾任环江毛南族自治县委副书记；后任河池市委组织部副部长（分管日常工作）、一级调研员；2025年内出任南丹县长。

## 关系网络

黄建辉与闻飞熊自2025年10月起作为南丹县党政主要领导搭班。该边仅表示公开任职重叠，不推断私人关系。

## 数据边界与开放问题

- 黄建辉更早履历及扶绥县长转任书记精确时间仍需原始官方简历。
- 闻飞熊出生地、入党/工作时间、完整早期履历及正式当选县长日期待补。
- 所有来源商业授权状态保持 `unknown`，不会进入商业导出视图。
""",
        encoding="utf-8",
    )


def main() -> None:
    run_build(
        slug="南丹县", persons=PERSONS, organizations=ORGANIZATIONS,
        positions=POSITIONS, relationships=RELATIONSHIPS, sources=SOURCES,
        claims=[], db_path=DB_PATH, gexf_path=GEXF_PATH,
        backend="v3", overwrite=True,
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
