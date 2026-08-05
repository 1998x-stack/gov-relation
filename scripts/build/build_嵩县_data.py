#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 嵩县 (Songxian County), 洛阳市, 河南省.

Investigation date: 2026-08-05 (re-investigation; supersedes thin 2026-07-24 partial-evidence build)
Task ID: henan_嵩县
Level: 县
Targets: 县委书记 & 县长

Research sources (all confirmed 2026-08-05):
  - 百度百科「辛俊峰」词条 (baike.baidu.com/item/辛俊峰)
  - 百度百科「任庆鹏」词条 (baike.baidu.com/item/任庆鹏)
  - 百度百科「中国共产党嵩县委员会」词条 (baike.baidu.com/item/中国共产党嵩县委员会)
  - 百度百科「宗玉红」词条 (baike.baidu.com/item/宗玉红)
  - 河南省委组织部任前公示 / 大象网 / 大河财立方 (2023-04-29公示, 2023-05-22宣布辛俊峰任县委书记)
  - 本地 repo 报告: report/20260724-伊川县-跨县干部交流网络.md (嵩县为多名洛阳县领导"初始地")

Confirmed roster / timeline:
- 辛俊峰(县委书记): 1975-11, 汉族, 大学(省委党校大学)学历, 法律专业, 中共党员;
  2017-10 洛阳市人民政府副秘书长 → 2021-08 嵩县县委副书记/副县长/代县长 → 2022-04 县长 →
  2023-05-22 任县委书记(兼县长至2023-12-05) → 现任县委书记. 河南省第十四届人大代表.
- 任庆鹏(县长): 1987-03, 汉族, 河南新乡人; 北京大学生命科学学院生化与分子生物学博士, 党员;
  2015-10 洛阳农林科学院副院长(挂市科技局副局长) → 2018-07 郑洛新自创区洛阳片区管委会专职副主任 →
  2021-08 伊川县委副书记/先进制造业开发区书记 → 2023-12-05 嵩县代县长 → 2024-01-18 当选县长.
- 前任县委书记 宗玉红(女,1966-05,河南洛阳人): 瀍河区→洛宁县副县长→洛阳市妇联→栾川(宣传/政法委/常务/副书记)→
  嵩县县长(2014-2021.7)→嵩县县委书记(2021.07-2023.05)→洛阳市政协副主席(2022.02起兼,2023.05起专职).
- 嵩县县委第十三届常委会(2021-08-29第一届): 书记辛俊峰, 副书记王雷、宋柯楠;
  常委: 曾红林(纪委书记/监委主任)、吕海泳(党组副书记/常务副县长)、周传江(人武部上校政委)、
  何建文(政法委书记)、吉跃龙(县委办公室主任)、史志锋(统战部长)、陈俊光(宣传部长/副县长).

Gaps flagged in person JSON `open_questions`:
  - 辛俊峰2017年前的出生地/籍贯/早期基层履历
  - 任庆鹏2009-2015(PKU博士至洛阳农林科学院)空白
  - 各常委完整履历
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "嵩县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR
REPORT_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══ Core Leadership ═══
    {
        "id": 1,
        "name": "辛俊峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学（省委党校大学）学历，法律专业",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共嵩县委员会",
        "source": "百度百科「辛俊峰」；河南省委组织部任前公示(2023-04)；大象网/大河报(2023-05-22任书记)",
    },
    {
        "id": 2,
        "name": "任庆鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年3月",
        "birthplace": "河南新乡",
        "education": "北京大学生命科学学院生物化学与分子生物学专业，博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "嵩县人民政府",
        "source": "百度百科「任庆鹏」；嵩县十五届人大四次会议(2024-01-18当选县长)",
    },
    # ═══ Predecessor ═══
    {
        "id": 3,
        "name": "宗玉红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1966年5月",
        "birthplace": "河南洛阳",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛阳市政协副主席",
        "current_org": "洛阳市政协",
        "source": "百度百科「宗玉红」(曾任嵩县县长2014-2021、县委书记2021.7-2023.5)",
    },
    # ═══ Current associates ═══
    {
        "id": 4,
        "name": "吕海泳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "嵩县人民政府",
        "source": "百度百科「中国共产党嵩县委员会」(县委第十三届常委会常委、县政府党组副书记、常务副县长)",
    },
    {
        "id": 5,
        "name": "曾红林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、县监委主任",
        "current_org": "嵩县纪委监委",
        "source": "百度百科「中国共产党嵩县委员会」(县委第十三届常委会常委、县纪委书记、监委主任)",
    },
    {
        "id": 6,
        "name": "何建文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共嵩县委员会",
        "source": "百度百科「中国共产党嵩县委员会」(第十三届常委会常委、政法委书记)",
    },
    {
        "id": 7,
        "name": "陈俊光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共嵩县委员会",
        "source": "百度百科「中国共产党嵩县委员会」(第十三届常委会常委、宣传部部长)",
    },
    {
        "id": 8,
        "name": "史志锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共嵩县委员会",
        "source": "百度百科「中国共产党嵩县委员会」(第十三届常委会常委、统战部部长)",
    },
    {
        "id": 9,
        "name": "吉跃龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共嵩县委员会",
        "source": "百度百科「中国共产党嵩县委员会」(第十三届常委会常委、县委办公室主任)",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共嵩县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "嵩县"},
    {"id": 2, "name": "嵩县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "嵩县"},
    {"id": 3, "name": "嵩县人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "嵩县"},
    {"id": 4, "name": "嵩县政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "嵩县"},
    {"id": 5, "name": "嵩县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "嵩县"},
    {"id": 6, "name": "嵩县监察委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市监察委员会", "location": "嵩县"},
    {"id": 7, "name": "洛阳市政协", "type": "政协", "level": "地厅级", "parent": "河南省政协", "location": "洛阳市"},
    {"id": 8, "name": "洛阳市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "洛阳市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 辛俊峰
    {"person_id": 1, "org_id": 8, "title": "洛阳市人民政府副秘书长", "start_date": "2017-10", "end_date": "2021-07", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "嵩县县委副书记", "start_date": "2021-08", "end_date": "2023-05", "rank": "县处级副职", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "嵩县副县长、代县长", "start_date": "2021-08", "end_date": "2022-04", "rank": "县处级正职", "note": "兼县产业集聚区党工委书记、管委会主任"},
    {"person_id": 1, "org_id": 2, "title": "嵩县县长", "start_date": "2022-04", "end_date": "2023-12", "rank": "县处级正职", "note": "2023-05任县委书记后仍兼县长至2023-12-05"},
    {"person_id": 1, "org_id": 1, "title": "嵩县县委书记", "start_date": "2023-05", "end_date": "present", "rank": "县处级正职", "note": "2023-05-22任; 兼县人武部党委第一书记"},
    # 任庆鹏
    {"person_id": 2, "org_id": 1, "title": "嵩县县委副书记", "start_date": "2023-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "嵩县副县长、代理县长", "start_date": "2023-12-05", "end_date": "2024-01", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "嵩县县长", "start_date": "2024-01-18", "end_date": "present", "rank": "县处级正职", "note": "县十五届人大四次会议当选"},
    # 宗玉红
    {"person_id": 3, "org_id": 1, "title": "嵩县县委副书记、县长", "start_date": "2014-09", "end_date": "2021-07", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "嵩县县委书记", "start_date": "2021-07", "end_date": "2023-05", "rank": "县处级正职", "note": "2022-02起兼洛阳市政协副主席"},
    {"person_id": 3, "org_id": 7, "title": "洛阳市政协副主席", "start_date": "2022-02", "end_date": "present", "rank": "地厅级副职", "note": "2023-05起不再任书记,专职副席"},
    # 王海泳 — 常务副县长
    {"person_id": 4, "org_id": 1, "title": "嵩县县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "嵩县常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "县政府党组副书记"},
    # 曾红林 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "嵩县县委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "嵩县纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "嵩县监委主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 何建文 — 政法委书记
    {"person_id": 6, "org_id": 1, "title": "嵩县县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈俊光 — 宣传部长/副县长
    {"person_id": 7, "org_id": 1, "title": "嵩县县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "嵩县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 史志锋 — 统战部长
    {"person_id": 8, "org_id": 1, "title": "嵩县县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 吉跃龙 — 县委办主任
    {"person_id": 9, "org_id": 1, "title": "嵩县县委常委、县委办公室主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 辛俊峰 ↔ 任庆鹏（党政正职搭档 + 前后任）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "辛俊峰任县委书记,任庆鹏任县长,为嵩县党政正职搭档。辛俊顺先任县长,任庆鹏后接县长(前后任兼上下级)", "overlap_org": "嵩县", "overlap_period": "2023-12至今"},
    # 辛俊峰 ↔ 宗玉红（前后任县委书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "宗玉红任县委书记(2021.7-2023.5)时辛俊顺任县长;2023-05宗卸任,辛接任书记", "overlap_org": "中共嵩县委员会", "overlap_period": "2021-2023"},
    # 任庆鹏 ↔ 宗玉红（前后任县长）
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "宗玉红2014-2021任嵩县县长,任庆鹏2024接任县长,前后任", "overlap_org": "嵩县人民政府", "overlap_period": "2014-2024"},
    # 书记—常委会成员
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "嵩县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "嵩县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "嵩县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与宣传部长", "overlap_org": "嵩县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与统战部长", "overlap_org": "嵩县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县委办主任", "overlap_org": "嵩县", "overlap_period": "当前"},
    # 县长 ↔ 县政府成员
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "嵩县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长(宣传部长)", "overlap_org": "嵩县人民政府", "overlap_period": "当前"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "辛俊峰",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "嵩县",
                "job": "县委书记",
                "task_id": "henan_嵩县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_songxian_xinjunfeng",
                "name": "辛俊峰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1975年11月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "省委党校大学", "major": "法律专业", "degree": "大学", "study_type": "party_school", "source_ids": ["S001", "S004"]}
                ],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "辛俊峰_1975年11月",
                    "name_birthplace": "",
                    "official_profile_url": "https://baike.baidu.com/item/辛俊峰/12646409"
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共嵩县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "2017-10", "end": "2021-07", "org": "洛阳市人民政府", "title": "副秘书长", "level": "地厅级机关县处级", "location": "洛阳市", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-08", "end": "2022-04", "org": "嵩县人民政府", "title": "副县长(代县长)", "level": "县处级正职", "location": "嵩县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "兼县产业集聚区党工委书记、管委会主任", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2022-04", "end": "2023-05", "org": "嵩县人民政府", "title": "县长", "level": "县处级正职", "location": "嵩县", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2023-05", "end": "present", "org": "中共嵩县委员会", "title": "县委书记", "level": "县处级正职", "location": "嵩县", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2023-05-22任;2023-12-05前兼任县长", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "2017年之前(含出生地、籍贯、入党/参加工作起点、省委党校大学前经历)未获公开资料", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "中共嵩县委员会", "role": "县委书记", "period": "2023-05至今", "source_ids": ["S001", "S002"]},
                {"name": "嵩县人民政府", "role": "县长(前任)", "period": "2021-08~2023-12", "source_ids": ["S001"]},
                {"name": "洛阳市人民政府", "role": "副秘书长", "period": "2017-10~2021-07", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "任庆鹏", "person_id": "henan_songxian_renqingpeng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "辛俊顺任书记,任庆鹏任县长,党政正对;辛俊顺先任县长,任庆鹏后接续县长", "overlap_org": "嵩县", "overlap_period": "2023-12至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "宗玉红", "person_id": "henan_songxian_zongyuhong", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "宗玉红任书记时辛任县长;2023-05辛接任书记", "overlap_org": "中共嵩县委员会", "overlap_period": "2021-2023", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "governance_record": [
                {"period": "2024", "domain": "other", "achievement_or_event": "河南省第十四届人大代表", "role_in_event": "人大代表", "measurable_outcome": "当选", "location": "河南省", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "cross_county_rotation",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["洛阳市", "嵩县"],
                "promotion_velocity": {
                    "summary": "从洛阳市副秘书长空降嵩县,按县委副书记→县长→县委书记典型路径在约6年内登顶县级班子",
                    "notable_fast_promotions": ["2021-08到2023-05约22个月完成县长→书记晋升"]
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "2026-08赴县信访局接访,强调'把群众反映的民生关切作为首要任务'", "confidence": "plausible", "source_ids": ["S005"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「辛俊峰」", "url": "https://baike.baidu.com/item/辛俊峰/12646409", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "含人物履历、担任职务、职务任免"},
                {"id": "S002", "title": "河南省委组织部任前公示(2023-04)", "url": "https://www.ha.12371.cn", "publisher": "河南省委组织部", "published_at": "2023-04-29", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "辛俊峰1975年11月、省委党校大学、时任县长,拟任县(市、区)委书记"},
                {"id": "S003", "title": "大象新闻/大河财立方「辛俊峰任中共嵩县县委书记」", "url": "https://www.dahe.cn", "publisher": "河南广播电视台-大象网", "published_at": "2023-05-22", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "宣布宗玉红不再任,辛俊峰接任"},
                {"id": "S005", "title": "洛阳信访(2026-08-03)「嵩县县委书记辛俊峰到县信访局接访」", "url": "https://www.lyd.com.cn", "publisher": "洛阳网", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "工作风格线索"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "辛俊峰2017年之前(出生地籍贯、入党/参加工作起点、早期基层履历)未获公开资料"
            },
            "open_questions": [
                {"priority": "high", "question": "辛俊峰的籍贯、出生地和2017年任洛阳市副秘书长前的工作经历是什么?", "why_it_matters": "还原其成长路径和早期关系网络", "suggested_queries": ["辛俊峰 洛阳 副秘书长 此前"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "辛俊峰上任县委书记前在洛阳市副秘书长岗位上具体分管哪些领域?", "why_it_matters": "了解其晋升背后的工作背景", "suggested_queries": ["辛俊峰 洛阳市人民政府 副秘书长"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "任庆鹏",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "洛阳市",
                "region": "嵩县",
                "job": "县长",
                "task_id": "henan_嵩县",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_songxian_renqingpeng",
                "name": "任庆鹏",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1987年3月",
                "birthplace": "河南新乡",
                "native_place": "河南新乡",
                "education": [
                    {"period": "", "institution": "北京大学生命科学学院", "major": "生物化学与分子生物学", "degree": "博士研究生", "study_type": "full_time", "source_ids": ["S001"]}
                ],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "任庆鹏_1987年3月",
                    "name_birthplace": "任庆鹏_河南新乡",
                    "official_profile_url": "https://baike.baidu.com/item/任庆鹏/20387893"
                }
            },
            "current_status": {
                "current_post": "县委副书记、县长",
                "current_org": "嵩县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {"start": "2015-10", "end": "", "org": "洛阳农林科学院", "title": "副院长(挂任市科技局副局长)", "level": "副县处级", "location": "洛阳市", "system": "other", "rank": "副县级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2018-07", "end": "", "org": "郑洛新国家自主创新示范区洛阳片区管委会", "title": "专职副主任(副县级)", "level": "副县处级", "location": "洛阳市", "system": "development_zone", "rank": "副县级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-08", "end": "2023-11", "org": "中共伊川县委", "title": "县委副书记", "level": "县处级副职", "location": "伊川县", "system": "party", "rank": "县处级副职", "is_key_promotion": True, "notes": "兼伊川县先进制造业开发区党工委书记、管委会主任;2021年8月调伊川县", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
                {"start": "2023-12-05", "end": "2024-01-17", "org": "嵩县人民政府", "title": "副县长、代理县长", "level": "县处级正职", "location": "嵩县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "2023-12-05嵩县人大常委会十四次会议任命", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2024-01-18", "end": "present", "org": "嵩县人民政府", "title": "县长", "level": "县处级正职", "location": "嵩县", "system": "government", "rank": "县处级正职", "is_key_promotion": False, "notes": "县十五届人大四次会议当选", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "2009-2015年(大学毕业至2015年入洛阳农林科学院)履历待查", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "嵩县人民政府", "role": "县长", "period": "2023-12至今", "source_ids": ["S001", "S002"]},
                {"name": "中共嵩县委员会", "role": "县委副书记", "period": "2023-12至今", "source_ids": ["S001"]},
                {"name": "中共伊川县委", "role": "县委副书记", "period": "2021-08~2023-11", "source_ids": ["S001", "S003"]},
                {"name": "洛阳农林科学院", "role": "副院长", "period": "2015-10始", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "辛俊峰", "person_id": "henan_songxian_xinjunfeng", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "任庆鹏任县长,辛任书记,党政正对", "overlap_org": "嵩县", "overlap_period": "2023-12至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"person": "宗玉红", "person_id": "henan_songxian_zongyuhong", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "宗任县长(2014-2021),任庆鹏后任县长", "overlap_org": "嵩县人民政府", "overlap_period": "2014-2024", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2024", "domain": "economic_development", "achievement_or_event": "县域经济发展", "role_in_event": "政府主要负责人", "measurable_outcome": "", "location": "嵩县", "confidence": "plausible", "source_ids": []}
            ],
            "professional_profile": {
                "primary_specializations": ["technocrat", "science_research"],
                "secondary_specializations": [],
                "career_pattern": "technical_specialist",
                "systems_experience": ["party", "government", "development_zone", "science"],
                "geographic_pattern": ["新乡", "洛阳市", "伊川县", "嵩县"],
                "promotion_velocity": {
                    "summary": "北大生化博士入县院,经科技园区、伊川副书记跨县至嵩县县长,展现高知技术干部升级之路",
                    "notable_fast_promotions": ["2021-2023伊川县副书记→2023嵩县县长(跨县正处级)"]
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "technocratic", "evidence": "北大博士、生化与分子生物学专业出身,长期从事科技创新与园区管理", "confidence": "plausible", "source_ids": ["S001"]}
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「任庆鹏」", "url": "https://baike.baidu.com/item/任庆鹏/20387893", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "含人物履历、职务任免"},
                {"id": "S002", "title": "嵩县第十五届人大常委会第十四次会议/县十五届人大四次会议", "url": "https://www.songxian.gov.cn", "publisher": "嵩县人大常委会/县政府", "published_at": "2023-12-05 / 2024-01-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "任代县长及当选县长"},
                {"id": "S003", "title": "百度百科「中国共产党伊县县委」/伊川县跨县干部交流报告", "url": "", "publisher": "各异", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "任庆鹏任伊川县委副书记/开发区书记记录,呼应跨县干部交流模式"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "任庆鹏2009-2015年(毕业至洛阳农林科学院前)履历未获公开资料"
            },
            "open_questions": [
                {"priority": "high", "question": "任庆鹏2009-2015年(大学毕业至2015年任洛阳农林科学院副院长)的履历?", "why_it_matters": "还原其早期职业发展和技术干部路径", "suggested_queries": ["任庆鹏 北京大学 洛阳 研究员", "任庆鹏 嵩县县长 履历"], "last_attempted": AS_OF},
                {"priority": "medium", "question": "任庆鹏在伊川县副书记任上是否与嵩县有前期工作交集?", "why_it_matters": "验证跨县干部交流的深层联系", "suggested_queries": ["任庆鹏 伊川 嵩县"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────
    CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
    CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
    CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
    CANONICAL_PERSONS = BASE / "data" / "persons"

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()