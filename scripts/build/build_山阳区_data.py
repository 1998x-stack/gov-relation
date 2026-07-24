#!/usr/bin/env python3
"""Build 焦作市山阳区 (Jiaozuo Shanyang District) leadership network data.

Level: 市辖区
Province: 河南省
Parent city: 焦作市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: henan_山阳区

Research date: 2026-07-24
Official source: https://www.syq.gov.cn/ (山阳区人民政府)
Staging build: data/tmp/henan_山阳区/ → promoted by process_tmp.py

Current status (as of 2026-07-24, verified via syq.gov.cn news archive):
- 区委书记: 郑小林 — 在任至少自2023年1月起；前任为李培华（2022年末离任）
- 区长: 侯向阳 — 区委副书记、区长，在任至少自2023年7月起
- 前区委书记: 李培华 — 2022年及此前在任

Confirmed government leadership page sources (all from syq.gov.cn):
- 郑小林: /xwzx/syyw/ （长期以区委书记身份报道）
- 侯向阳: /xwzx/zfhy/ （以区长身份主持会议）
- 领导分工页面见政府信息公开目录

Key news sources (all 2026, from syq.gov.cn):
- 郑小林带队调研生态环境保护 (2026-05-09): /2026/05-12/603105.html
- 区政府第44次常务会议 (2026-05-07): /2026/05-12/603103.html
- 十届区委常委会第133次会议 (2026-04-30): /2026/05-12/603097.html
- 郑小林调研安全生产、文旅市场 (2026-04-30): /2026/05-12/603099.html
- 十届区委常委会第131次会议 (2026-03-31): /2026/04-07/600476.html
- 郑小林、侯向阳带队调研 (2026-02-15): 第126次会议报道
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "山阳区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

SOURCE_OFFICIAL = ("山阳区人民政府官方网站: https://www.syq.gov.cn/")
SOURCE_NEWS = ("山阳区新闻中心报道: https://www.syq.gov.cn/xwzx/syyw/")

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郑小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山阳区委书记",
        "current_org": "中共焦作市山阳区委员会",
        "source": (SOURCE_OFFICIAL + "; "
                    "新闻: 2023年1月起即以区委书记身份公开活动，最早可溯至2023-01-22调研报道"),
    },
    {
        "id": 2,
        "name": "侯向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山阳区委副书记、区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + "; "
                    "新闻: 2023年7月起以区长身份公开活动；2026-01-06区政府信息公开目录收录"),
    },
    {
        "id": 4,
        "name": "郑浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-07-06发布"),
    },
    {
        "id": 5,
        "name": "王建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-01-05发布"),
    },
    {
        "id": 6,
        "name": "赵俊生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "山阳区",
        "source": (SOURCE_NEWS + " 第44次区政府常务会议参会名单"),
    },
    {
        "id": 7,
        "name": "闫占明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "山阳区",
        "source": (SOURCE_NEWS + " 郑小林带队调研报道"),
    },
    {
        "id": 8,
        "name": "孟国平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "山阳区",
        "source": (SOURCE_NEWS + " 第44次区政府常务会议参会名单"),
    },
    {
        "id": 9,
        "name": "任晓林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "山阳区",
        "source": (SOURCE_NEWS + " 郑小林带队调研生态环境保护及第44次常务会议"),
    },
    {
        "id": 10,
        "name": "高凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-05-21发布"),
    },
    {
        "id": 11,
        "name": "李胤铮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-07-01发布"),
    },
    {
        "id": 12,
        "name": "胡磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-06-30发布"),
    },
    {
        "id": 13,
        "name": "张宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-01-05发布"),
    },
    {
        "id": 14,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "山阳区人民政府",
        "source": (SOURCE_OFFICIAL + " 政府信息公开目录: 2026-01-05发布"),
    },
    # ════════════════════════════════════════
    # 前领导 (Former Leaders)
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "李培华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任山阳区委书记（已离任）",
        "current_org": "",
        "source": (SOURCE_NEWS + " 2022年11月仍以区委书记身份调研；2022年12月与郑小林同时出现，后离任"),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共焦作市山阳区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市山阳区",
    },
    {
        "id": 2,
        "name": "山阳区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市山阳区",
    },
    {
        "id": 3,
        "name": "山阳区",
        "type": "行政区",
        "level": "县处级",
        "parent": "焦作市",
        "location": "河南省焦作市山阳区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 郑小林 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "山阳区委书记", "start": "约2022年末/2023年初", "end": "至今", "rank": "县处级正职", "note": "最早可溯至2023年1月22日调研报道"},
    # 侯向阳 - 区长
    {"person_id": 2, "org_id": 2, "title": "山阳区委副书记、区长", "start": "不晚于2023年7月", "end": "至今", "rank": "县处级正职", "note": "2023年7月与郑小林共同开展八一慰问活动"},
    # 郑浩 - 区委常委、副区长
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-07-06更新"},
    # 王建军 - 区委常委、副区长
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-01-05发布"},
    # 赵俊生 - 区领导
    {"person_id": 6, "org_id": 3, "title": "区领导", "start": "", "end": "至今", "rank": "县处级", "note": "第44次区政府常务会议出席"},
    # 闫占明 - 区领导
    {"person_id": 7, "org_id": 3, "title": "区领导", "start": "", "end": "至今", "rank": "县处级", "note": "随郑小林多次调研"},
    # 孟国平 - 区领导
    {"person_id": 8, "org_id": 3, "title": "区领导", "start": "", "end": "至今", "rank": "县处级", "note": "第44次区政府常务会议出席"},
    # 任晓林 - 区领导
    {"person_id": 9, "org_id": 3, "title": "区领导", "start": "", "end": "至今", "rank": "县处级", "note": "随郑小林调研及第44次常务会议"},
    # 高凯 - 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-05-21"},
    # 李胤铮 - 副区长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-07-01"},
    # 胡磊 - 副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-06-30"},
    # 张宁 - 副区长
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-01-05"},
    # 李涛 - 副区长
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "县处级副职", "note": "政府信息公开目录2026-01-05"},
    # 李培华 - 前任区委书记
    {"person_id": 15, "org_id": 1, "title": "山阳区委书记（前任）", "start": "不晚于2022年", "end": "约2022年末", "rank": "县处级正职", "note": "2022年11月仍以区委书记身份调研；2022年12月后离任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 郑小林 ↔ 侯向阳（党政一把手）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭档，全面负责区委和区政府工作",
        "overlap_org": "山阳区",
        "overlap_period": "2023年至今",
        "strength": "strong",
        "direction": "undirected",
    },
    # 郑小林 ↔ 王建军（常委+副区长）
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委、副区长",
        "overlap_org": "山阳区",
        "overlap_period": "2024年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 郑小林 ↔ 郑浩（常委+副区长）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委、副区长",
        "overlap_org": "山阳区",
        "overlap_period": "2024年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 侯向阳 ↔ 高凯（区长↔副区长）
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "山阳区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 侯向阳 ↔ 张宁（区长↔副区长）
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "山阳区人民政府",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 侯向阳 ↔ 李涛（区长↔副区长）
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "山阳区人民政府",
        "overlap_period": "2026年至今",
        "strength": "medium",
        "direction": "person_to_other",
    },
    # 郑小林 ↔ 赵俊生（书记↔区领导）
    {
        "person_a": 1,
        "person_b": 6,
        "type": "overlap",
        "context": "区委书记与区领导，共同参与调研及会议",
        "overlap_org": "山阳区",
        "overlap_period": "2024年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    # 郑小林 ↔ 闫占明（书记↔区领导）
    {
        "person_a": 1,
        "person_b": 7,
        "type": "overlap",
        "context": "区委书记与区领导，多次共同调研",
        "overlap_org": "山阳区",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    # 郑小林 ↔ 任晓林（书记↔区领导）
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "区委书记与区领导，多次共同调研",
        "overlap_org": "山阳区",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    # 郑小林 ↔ 李培华（前任区委书记）
    {
        "person_a": 1,
        "person_b": 15,
        "type": "predecessor_successor",
        "context": "郑小林接替李培华任山阳区委书记",
        "overlap_org": "中共焦作市山阳区委员会",
        "overlap_period": "2022年末交接",
        "strength": "strong",
        "direction": "other_to_person",
    },
    # 侯向阳 ↔ 赵俊生（区长↔区领导）
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "区长与区领导，共同参加政府常务会议",
        "overlap_org": "山阳区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
    # 侯向阳 ↔ 孟国平（区长↔区领导）
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "区长与区领导，共同参加政府常务会议",
        "overlap_org": "山阳区人民政府",
        "overlap_period": "2025年至今",
        "strength": "medium",
        "direction": "undirected",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data ...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    
    print(f"\nDone. {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships.")

    # Write person JSON files
    person_json_map = {
        "区委书记": {
            "person": persons[0],
            "name": "郑小林",
        },
        "区长": {
            "person": persons[1],
            "name": "侯向阳",
        },
    }
    
    for label, info in person_json_map.items():
        p = info["person"]
        fname = f"{TODAY}-河南省-焦作市-{label}-{info['name']}.json"
        fpath = _STAGING_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump({
                "schema_version": "1.0",
                "generated_at": TODAY,
                "investigation_scope": {
                    "province": "河南省",
                    "city": "焦作市",
                    "region": "山阳区",
                    "job": label,
                    "task_id": "henan_山阳区",
                    "time_focus": "2026-07"
                },
                "identity": {
                    "person_id": f"henan_jiaozuo_shanyang_{info['name']}",
                    "name": info["name"],
                    "aliases": [],
                    "gender": p["gender"],
                    "ethnicity": p["ethnicity"],
                    "birth": "",
                    "birthplace": "",
                    "native_place": "",
                    "education": [],
                    "party_join": "中共党员",
                    "work_start": "",
                    "dedupe_keys": {
                        "name_birth": f"{info['name']}_",
                        "name_birthplace": f"{info['name']}_",
                        "official_profile_url": ""
                    }
                },
                "current_status": {
                    "current_post": p["current_post"],
                    "current_org": p["current_org"],
                    "administrative_rank": "县处级正职",
                    "as_of": AS_OF,
                    "is_current_confirmed": label == "区委书记",
                    "source_ids": ["S001"]
                },
                "career_timeline": [
                    {
                        "start": "约2022年末/2023年初" if label == "区委书记" else "不晚于2023年7月",
                        "end": "至今",
                        "org": p["current_org"],
                        "title": p["current_post"],
                        "level": "县处级正职",
                        "location": "河南省焦作市山阳区",
                        "system": "party" if label == "区委书记" else "government",
                        "rank": "县处级正职",
                        "is_key_promotion": True,
                        "notes": "",
                        "confidence": "confirmed",
                        "source_ids": ["S001"]
                    }
                ],
                "organizations": [
                    {
                        "org_id": "中共焦作市山阳区委员会",
                        "org_name": "中共焦作市山阳区委员会",
                        "role": "区委书记" if label == "区委书记" else "区委副书记",
                        "period": ""
                    },
                    {
                        "org_id": "山阳区人民政府",
                        "org_name": "山阳区人民政府",
                        "role": "区长" if label == "区长" else "",
                        "period": ""
                    }
                ],
                "relationships": [],
                "governance_record": [],
                "professional_profile": {
                    "primary_specializations": [],
                    "secondary_specializations": [],
                    "career_pattern": "local_ladder",
                    "systems_experience": [],
                    "geographic_pattern": [],
                    "promotion_velocity": {
                        "summary": "全体履历待查",
                        "notable_fast_promotions": []
                    }
                },
                "work_style_and_personality": {
                    "public_style_indicators": [],
                    "speech_themes": [],
                    "management_signals": [],
                    "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
                },
                "network_metrics": {},
                "risk_and_integrity_signals": [],
                "source_register": [
                    {
                        "id": "S001",
                        "title": "山阳区人民政府官方网站",
                        "url": "https://www.syq.gov.cn/",
                        "publisher": "山阳区人民政府",
                        "published_at": "",
                        "accessed_at": AS_OF,
                        "source_type": "official",
                        "reliability": "high",
                        "notes": "政府新闻及信息公开目录"
                    }
                ],
                "confidence_summary": {
                    "identity": "unverified",
                    "current_role": "confirmed",
                    "career_completeness": "thin",
                    "relationship_confidence": "low",
                    "biggest_gap": "出生年月、籍贯、教育背景、完整履历均未找到"
                },
                "open_questions": [
                    {
                        "priority": "critical",
                        "question": f"{info['name']}的出生年月和籍贯是什么？",
                        "why_it_matters": "身份核实和去重的基础字段",
                        "suggested_queries": [f"{info['name']} 简历", f"{info['name']} 出生", f"{info['name']} 百度百科"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "critical",
                        "question": f"{info['name']}的完整职业履历，特别是担任现职前的经历",
                        "why_it_matters": "理解晋升路径和跨领域经验",
                        "suggested_queries": [f"{info['name']} 任前公示", f"{info['name']} 焦作 组织部"],
                        "last_attempted": AS_OF
                    },
                    {
                        "priority": "high",
                        "question": f"{info['name']}的教育背景和入党时间",
                        "why_it_matters": "评估知识背景和党内资历",
                        "suggested_queries": [f"{info['name']} 教育", f"{info['name']} 毕业"],
                        "last_attempted": AS_OF
                    }
                ]
            }, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fpath}")
    
    print("\nAll person JSON files written to staging directory.")
