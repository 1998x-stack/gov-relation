#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 方城县 (Fangcheng County), 南阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_方城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - https://www.fangcheng.gov.cn/ — official government website
  - Government leadership page: /cjglycd/zfld/ (7 government leaders with bios)
  - Individual bio pages for each government leader
  - News articles on fcyw/ pages confirming 县委书记刘伟 (Sept 2025—)
  - News articles confirming 县长李霞 (active 2025-2026)
  - 县人大常委会公告 2025-12-29: 王洋任副县长、公安局局长

Confidence notes:
  - 刘伟 (县委书记): confirmed via multiple official news articles since Sept 2025.
    Full birth year and early career unverified.
  - 李霞 (县长): confirmed via official government bio page (女, 汉族, 研究生, 
    公共管理硕士, 中共党员). Full birth year and early career unverified.
  - Government leadership team: bios confirmed from official site.
  - 段文汉 (predecessor): served as 方城县委书记 before 刘伟, based on news timeline.
  - Party standing committee: partial — 岳太斌 (县委常委、宣传部部长、副县长) and 
    艾克拜尔·依明 (县委常委、副县长) confirmed. Others unknown.
  - This is a partial-evidence artifact: core leader identities and government team are
    well-documented; party committee detailed bios and standing committee role assignments
    are incomplete.
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
SLUG = "方城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Helper: ID offset for orgs ─────────────────────────────────────────────
ORG_OFFSET = 100000

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "刘伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共方城县委员会",
        "source": "Confirmed as 县委书记 via official news articles (Sept 2025—). Earliest mention: 2025-09-12 '县委书记刘伟调研方城烩面产业发展情况'. Previous role uncertain."
    },
    {
        "id": 2,
        "name": "李霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/10-15/641167.html — 女，汉族，研究生，公共管理硕士，中共党员. Active as 县长 in 2025-2026 news articles."
    },
    {
        "id": 3,
        "name": "段文汉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记（去向待查）",
        "current_org": "",
        "source": "Previous 方城县委书记. Referenced in historical news context. Exact term dates and current position unverified."
    },
    # ═══════ Government Leadership ═══════
    {
        "id": 4,
        "name": "岳太斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长，县政府副县长",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/11-21/820635.html — 男，大学，中共党员. Oversees education, health, culture, transport."
    },
    {
        "id": 5,
        "name": "艾克拜尔·依明",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/10-15/641170.html — 男，维吾尔族，大学，中共党员. Oversees defense, veterans, finance."
    },
    {
        "id": 6,
        "name": "李振广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员，先进制造业开发区党工委书记、管委会主任",
        "current_org": "方城县先进制造业开发区",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/11-21/820614.html — 男，汉族，大学，中共党员. Oversees industry, economy, tech, investment."
    },
    {
        "id": 7,
        "name": "王桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/10-15/641172.html — 男，汉族，大学，中共党员. Oversees market, commerce, civil affairs."
    },
    {
        "id": 8,
        "name": "任义卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/10-15/641176.html — 男，汉族，大学，中共党员. Oversees natural resources, housing, urban mgmt."
    },
    {
        "id": 9,
        "name": "樊海鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长、党组成员",
        "current_org": "方城县人民政府",
        "source": "Official bio: https://www.fangcheng.gov.cn/2024/10-15/641177.html — 男，汉族，大专，中共党员. Oversees agriculture, poverty alleviation, forestry."
    },
    # ═══════ Other Key Figures ═══════
    {
        "id": 10,
        "name": "王洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、县公安局局长",
        "current_org": "方城县公安局",
        "source": "Confirmed via 县人大常委会公告: https://www.fangcheng.gov.cn/2026/01-11/1372394.html — Appointed Dec 2025."
    },
    {
        "id": 11,
        "name": "甘泉涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（参加烩面产业调研）",
        "current_org": "方城县",
        "source": "Mentioned in '县委书记刘伟调研方城烩面产业发展情况' (2025-09-12) as accompanying leader."
    },
    {
        "id": 12,
        "name": "温阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（参加便民服务调研）",
        "current_org": "方城县",
        "source": "Mentioned in '县委书记刘伟调研便民服务工作' (2025-10-13) as accompanying leader."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共方城县委员会", "type": "党委", "level": "县处级", "parent": "中共南阳市委", "location": "方城县"},
    {"id": 2, "name": "方城县人民政府", "type": "政府", "level": "县处级", "parent": "南阳市人民政府", "location": "方城县"},
    {"id": 3, "name": "方城县人大常委会", "type": "人大", "level": "县处级", "parent": "南阳市人大常委会", "location": "方城县"},
    {"id": 4, "name": "方城县政协", "type": "政协", "level": "县处级", "parent": "南阳市政协", "location": "方城县"},
    {"id": 5, "name": "方城县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "南阳市纪委监委", "location": "方城县"},
    {"id": 6, "name": "中共方城县委宣传部", "type": "党委", "level": "县处级", "parent": "中共方城县委", "location": "方城县"},
    {"id": 7, "name": "方城县公安局", "type": "政府", "level": "县处级", "parent": "方城县人民政府", "location": "方城县"},
    {"id": 8, "name": "方城县先进制造业开发区", "type": "开发区", "level": "县处级", "parent": "方城县人民政府", "location": "方城县"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 刘伟 (id=1)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-09", "end_date": "present", "rank": "县处级正职", "note": "最早公开报道为2025年9月12日"},
    # 李霞 (id=2)
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作，具体到任时间待查"},
    # 段文汉 (id=3) — predecessor
    {"person_id": 3, "org_id": 1, "title": "县委书记（前任）", "start_date": "", "end_date": "~2025-09", "rank": "县处级正职", "note": "前任方城县委书记，刘伟的前任"},
    # 岳太斌 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责教育、体育、卫健、医保、文旅、交通"},
    # 艾克拜尔·依明 (id=5)
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责国防动员、退役军人、金融等"},
    # 李振广 (id=6)
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "先进制造业开发区党工委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工业经济、科技创新、招商引资"},
    # 王桥 (id=7)
    {"person_id": 7, "org_id": 2, "title": "副县长、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责市场监管、商贸流通、民政等"},
    # 任义卓 (id=8)
    {"person_id": 8, "org_id": 2, "title": "副县长、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责自然资源、住建、城管、环保"},
    # 樊海鹏 (id=9)
    {"person_id": 9, "org_id": 2, "title": "副县长、党组成员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、水利、林业"},
    # 王洋 (id=10)
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "2025-12", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "县公安局局长", "start_date": "2025-12", "end_date": "present", "rank": "县处级副职", "note": "2025年12月29日任命"},
    # 甘泉涛 (id=11)
    {"person_id": 11, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    # 温阳 (id=12)
    {"person_id": 12, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 刘伟 ↔ 李霞（党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "刘伟任县委书记，李霞任县委副书记、县长，为方城县党政正职搭档",
        "overlap_org": "方城县",
        "overlap_period": "2025—"
    },
    # 段文汉 → 刘伟（前后任书记）
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "段文汉为前任县委书记，刘伟接任（约2025年9月）",
        "overlap_org": "中共方城县委员会",
        "overlap_period": "2025"
    },
    # 刘伟 ↔ 岳太斌（上下级）
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "刘伟为县委书记，岳太斌为县委常委、宣传部部长、副县长",
        "overlap_org": "方城县委常委班子",
        "overlap_period": "当前"
    },
    # 刘伟 ↔ 艾克拜尔·依明（上下级）
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "刘伟为县委书记，艾克拜尔·依明为县委常委、副县长",
        "overlap_org": "方城县委常委班子",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 岳太斌（政府正副职搭档）
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "李霞为县长，岳太斌为副县长，方城县政府正副职搭档",
        "overlap_org": "方城县人民政府",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 王桥（政府正副职）
    {
        "person_a": 2, "person_b": 7,
        "type": "superior_subordinate",
        "context": "李霞为县长，王桥为副县长",
        "overlap_org": "方城县人民政府",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 任义卓（政府正副职）
    {
        "person_a": 2, "person_b": 8,
        "type": "superior_subordinate",
        "context": "李霞为县长，任义卓为副县长",
        "overlap_org": "方城县人民政府",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 樊海鹏（政府正副职）
    {
        "person_a": 2, "person_b": 9,
        "type": "superior_subordinate",
        "context": "李霞为县长，樊海鹏为副县长",
        "overlap_org": "方城县人民政府",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 李振广（政府正副职）
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "李霞为县长，李振广为县政府党组成员",
        "overlap_org": "方城县人民政府",
        "overlap_period": "当前"
    },
    # 李霞 ↔ 王洋（政府正副职）
    {
        "person_a": 2, "person_b": 10,
        "type": "superior_subordinate",
        "context": "李霞为县长，王洋为副县长、公安局局长",
        "overlap_org": "方城县人民政府",
        "overlap_period": "2025.12—"
    },
    # 艾克拜尔·依明 ↔ 岳太斌（同僚）
    {
        "person_a": 5, "person_b": 4,
        "type": "overlap",
        "context": "同为县委常委、副县长",
        "overlap_org": "方城县委常委班子",
        "overlap_period": "当前"
    },
    # 刘伟 ↔ 甘泉涛（上下级）
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "甘泉涛陪同刘伟调研烩面产业",
        "overlap_org": "方城县",
        "overlap_period": "2025—"
    },
    # 刘伟 ↔ 温阳（上下级）
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "温阳陪同刘伟调研便民服务工作",
        "overlap_org": "方城县",
        "overlap_period": "2025—"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "刘伟",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "南阳市",
                "region": "方城县",
                "job": "县委书记",
                "task_id": "henan_方城县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "fangcheng_liu_wei",
                "name": "刘伟",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "刘伟_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共方城县委员会",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "~2025-08",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到刘伟在任方城县委书记前的履历",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "2025-09",
                    "end": "present",
                    "org": "中共方城县委员会",
                    "title": "县委书记",
                    "level": "县处级正职",
                    "location": "河南省南阳市方城县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "最早公开报道为2025年9月12日调研方城烩面产业",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [
                {"org": "中共方城县委员会", "role": "县委书记", "period": "2025—至今"}
            ],
            "relationships": [
                {
                    "person": "李霞",
                    "person_id": "fangcheng_li_xia",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "党政正职搭档：刘伟为县委书记，李霞为县长",
                    "overlap_org": "方城县",
                    "overlap_period": "2025—",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003"]
                },
                {
                    "person": "段文汉",
                    "person_id": "fangcheng_duan_wenhan",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "段文汉为前任县委书记，刘伟接任",
                    "overlap_org": "中共方城县委员会",
                    "overlap_period": "2025",
                    "direction": "other_to_person",
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "governance_record": [
                {
                    "period": "2025-09",
                    "domain": "industry",
                    "achievement_or_event": "调研方城烩面产业发展，推动品牌化、标准化、规模化",
                    "role_in_event": "主持调研",
                    "location": "方城县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2025-10",
                    "domain": "other",
                    "achievement_or_event": "围绕便民服务工作进行调研，推动'接诉即办'和'一件事一次办'",
                    "role_in_event": "主持调研",
                    "location": "方城县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历信息不足，无法评估晋升速度",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "深入烩面企业和便民服务中心调研，关注产业和民生",
                        "confidence": "plausible",
                        "source_ids": ["S001", "S002"]
                    }
                ],
                "speech_themes": ["产业发展", "便民服务", "接诉即办", "闭环管理"],
                "management_signals": ["注重产业品牌化", "关注基层服务"],
                "caveat": "工作风格基于公开报道推断"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现刘伟相关的纪检处分、审计问题或负面媒体报道",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "县委书记刘伟调研方城烩面产业发展情况", "url": "https://www.fangcheng.gov.cn/2025/09-12/1212419.html", "publisher": "方城县人民政府", "published_at": "2025-09-12", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认刘伟为县委书记"},
                {"id": "S002", "title": "县委书记刘伟围绕便民服务工作进行调研", "url": "https://www.fangcheng.gov.cn/2025/10-13/1326941.html", "publisher": "方城县人民政府", "published_at": "2025-10-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S003", "title": "李霞-政府领导", "url": "https://www.fangcheng.gov.cn/2024/10-15/641167.html", "publisher": "方城县人民政府", "published_at": "2024-11-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府领导页面，确认李霞为县长"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "刘伟任县委书记前的完整履历未知"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "刘伟任方城县委书记前的职业履历是什么？",
                    "why_it_matters": "核心人物的完整背景对评估其关系网络至关重要",
                    "suggested_queries": ["刘伟 简历 方城", "刘伟 南阳 任职", "刘伟 河南 组织部 任前公示"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "刘伟的出生年份、籍贯、学历信息",
                    "why_it_matters": "基本信息缺失，影响身份确认",
                    "suggested_queries": ["刘伟 出生 方城县委书记"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "李霞",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "南阳市",
                "region": "方城县",
                "job": "县委副书记、县长",
                "task_id": "henan_方城县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "fangcheng_li_xia",
                "name": "李霞",
                "aliases": [],
                "gender": "女",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": "公共管理硕士",
                        "study_type": "unknown",
                        "source_ids": ["S001"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "李霞_unknown",
                    "name_birthplace": "",
                    "official_profile_url": "https://www.fangcheng.gov.cn/2024/10-15/641167.html"
                }
            },
            "current_status": {
                "current_post": "县委副书记、县长",
                "current_org": "方城县人民政府",
                "administrative_rank": "县处级正职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到李霞任方城县长前的完整履历",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "",
                    "end": "present",
                    "org": "方城县人民政府",
                    "title": "县委副书记、县长、党组书记",
                    "level": "县处级正职",
                    "location": "河南省南阳市方城县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "主持县政府全面工作，负责审计。具体到任时间待查。",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [
                {"org": "方城县人民政府", "role": "县长、党组书记", "period": "至今"}
            ],
            "relationships": [
                {
                    "person": "刘伟",
                    "person_id": "fangcheng_liu_wei",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "刘伟为县委书记，李霞为县长，党政正职搭档",
                    "overlap_org": "方城县",
                    "overlap_period": "2025—",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002", "S003"]
                },
                {
                    "person": "岳太斌",
                    "person_id": "fangcheng_yue_taibin",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "李霞为县长，岳太斌为副县长",
                    "overlap_org": "方城县人民政府",
                    "overlap_period": "当前",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S004"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-05",
                    "domain": "public_security",
                    "achievement_or_event": "主持召开全县消防安全暨道路交通安全工作会议",
                    "role_in_event": "主持",
                    "location": "方城县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2026-05",
                    "domain": "economic_development",
                    "achievement_or_event": "调研汉山水库建设、麦田管理等工作",
                    "role_in_event": "调研",
                    "location": "方城县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                },
                {
                    "period": "2026-04",
                    "domain": "industry",
                    "achievement_or_event": "到县先进制造业开发区开展现场办公",
                    "role_in_event": "现场办公",
                    "location": "方城县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历信息不足，无法评估晋升速度",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "频繁深入乡镇、企业调研，涉及三夏生产、安全生产、教育等多领域",
                        "confidence": "confirmed",
                        "source_ids": ["S003"]
                    }
                ],
                "speech_themes": ["安全生产", "项目建设", "财税工作", "民生保障"],
                "management_signals": ["注重一线调研", "关注安全生产和民生"],
                "caveat": "工作风格基于公开报道推断"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现李霞相关的纪检处分或负面信息",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "李霞-政府领导", "url": "https://www.fangcheng.gov.cn/2024/10-15/641167.html", "publisher": "方城县人民政府", "published_at": "2024-11-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "官方领导页面，含分工和简历"},
                {"id": "S002", "title": "方城县人民政府网要闻", "url": "https://www.fangcheng.gov.cn/", "publisher": "方城县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "多篇新闻报道确认李霞为县长"},
                {"id": "S003", "title": "方城县人民政府新闻中心", "url": "https://www.fangcheng.gov.cn/cjglycd/ywzx/fcyw", "publisher": "方城县人民政府", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "多个以李霞为县长的新闻条目"},
                {"id": "S004", "title": "岳太斌-政府领导", "url": "https://www.fangcheng.gov.cn/2024/11-21/820635.html", "publisher": "方城县人民政府", "published_at": "2024-11-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""}
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "李霞任方城县长前的完整履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "李霞任方城县长前的职业履历是什么？",
                    "why_it_matters": "核心人物的完整背景对评估其关系网络至关重要",
                    "suggested_queries": ["李霞 方城 县长 简历", "李霞 南阳 任职经历"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "李霞的出生年份、籍贯信息",
                    "why_it_matters": "基本信息缺失",
                    "suggested_queries": ["李霞 出生 方城"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "李霞何时到任方城县长",
                    "why_it_matters": "确定党政搭档的具体共事时间",
                    "suggested_queries": ["李霞 任命 方城县 县长"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
]

# ══════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════

def main():
    # Use the public runner library from gov_relation
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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
        person_name = pf["name"]
        job = pf["job"]
        filename = f"{TODAY}-河南省-南阳市-{job}-{person_name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print(f"\nDone. Build complete for {SLUG}.")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()
