#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 溪湖区, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_溪湖区
Level: 市辖区
Parent city: 本溪市
Targets: 区委书记 & 区长

Research status: PRIMARY SOURCE ACCESS
  - 溪湖区人民政府门户网站 (www.xihu.gov.cn): fully accessible
  - 区政府领导之窗 (区长/副区长): current roster confirmed with full bios for 区长
  - 区第二十一次党代会 (2026-07-26~28): 郭鑫代表二十届区委作报告 (书记身份确认)
  - 溪湖区委书记、高新区管委会主任 官宣冲突 (本溪高新区官网 cnmc.gov.cn 仍列 李涛为管委会主任、何涛为党工委书记)
  - Exa/Bing/Baidu/Sogou 检索受限; 依托官网目击确认, 履历细节按证据分级标注

Current officeholders (as of 2026-08-06, confirmed by official www.xihu.gov.cn):
   - 区委书记: 郭鑫 (官宣 "溪湖区委书记、高新区管委会主任"; 高新区官网存异, 标记 plausible)
   - 区委副书记、区长: 何宇翥 (男, 锡伯族, 1979-02, 大学+公共管理硕士, 中共党员; 兼本溪湖经济开发区党工委书记)
   - 常务副区长: 杨于 (区委常委、副区长、党组副书记, 负责政府常务工作)
   - 副区长: 王佳(区委常委), 纪延妍, 巴翔, 王福牮, 管磊

Predecessor timeline:
   - 区委书记: 代萍 (~2021-2025) → 郭鑫 (2025-2026)
   - 区长: 高飞 (~2021-2024) → 何宇翥 (2025-)
   - 更早: 王世平 (书记 ~2017-2021); 代萍曾任区长 (2017-2021)

Cross-region:
   - 区长兼本溪湖经济开发区党工委书记 = 全市标准化"区县长兼经开区书记"结构
   - 郭鑫 possibly 本溪高新区党管会主任 (与 cnmc.gov.cn 冲突, 待核)
   - 本溪市委副书记/政法委/高新区党工委书记 何涛 (女, 满族, 1972)
"""

from __future__ import annotations

import json
import os
import sys
import sqlite3
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "溪湖区"
TODAY_str = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths (script writes artifacts into its own directory) ─────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────────
persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "郭鑫",
        "gender": "男",
        "ethnicity": "汉族（推断，待确认）",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党本溪市溪湖区委员会",
        "source": "http://www.xihu.gov.cn/xwzx/gzdt/content_665644 (区二十一届党代会, 2026-07-26)",
    },
    # ── 区长 ──
    {
        "id": 2,
        "name": "何宇翥",
        "gender": "男",
        "ethnicity": "锡伯族",
        "birth": "1979-02",
        "birthplace": "待查",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区长",
        "current_org": "本溪市溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_634659",
    },
    # ── 常务副区长 ──
    {
        "id": 3,
        "name": "杨于",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "待查",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "常务副区长",
        "current_org": "本溪市溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_528530",
    },
    # ── 副区长 (区常委) ──
    {
        "id": 4,
        "name": "王佳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986-09",
        "birthplace": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长",
        "current_org": "中共本溪市溪湖区委员会 / 溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_633054",
    },
    # ── 副区长 ──
    {
        "id": 5,
        "name": "纪延妍",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1983-01",
        "birthplace": "待查",
        "education": "大学，公共管理硕士",
        "party_join": "",  # 民建会员，非中共党员
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "本溪市溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_528532",
    },
    # ── 副区长 (公安) ──
    {
        "id": 6,
        "name": "巴勇",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1971-10",
        "birthplace": "待查",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长、区公安分局局长",
        "current_org": "本溪市溪湖区人民政府 / 本溪市公安局溪湖分局",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_606162",
    },
    # ── 副区长 ──
    {
        "id": 7,
        "name": "王福牮",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1982-02",
        "birthplace": "待查",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "本溪市溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_606161",
    },
    # ── 副区长 ──
    {
        "id": 8,
        "name": "管磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-03",
        "birthplace": "待查",
        "education": "大学学历，哲学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "本溪市溪湖区人民政府",
        "source": "http://www.xihu.gov.cn/ldzc/qzfld/content_655522",
    },
    # ── 前任区委书记 ──
    {
        "id": 9,
        "name": "代萍",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任溪湖区委书记（去向待查）",
        "current_org": "",
        "source": "http://www.xihu.gov.cn/xwzx/gzdt/content_644214 (2025-04-30)",
    },
    # ── 前任区长 ──
    {
        "id": 10,
        "name": "高飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任溪湖区区长",
        "current_org": "",
        "source": "http://www.xihu.gov.cn/xwzx/gzdt/content_633520 (2024-10)",
    },
    # ── 本溪市市委副书记/高新区党工委书记 (跨区网) ──
    {
        "id": 11,
        "name": "何涛",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1972-07",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "本溪市委副书记、市委政法委书记、本溪高新区党工委书记",
        "current_org": "中共本溪市委员会",
        "source": "http://www.cnmc.gov.cn/zwgk/ldzc/content_645755",
    },
]

organizations = [
    {"id": 1, "name": "中国共产党本溪市溪湖区委员会", "type": "党委", "level": "县处级", "parent": "本溪市委", "location": "本溪市溪湖区"},
    {"id": 2, "name": "本溪市溪湖区人民政府", "type": "政府", "level": "县处级", "parent": "本溪市政府", "location": "本溪市溪湖区"},
    {"id": 3, "name": "本溪湖经济开发区党工委", "type": "开发区", "level": "县处级", "parent": "本溪市", "location": "本溪市溪湖区"},
    {"id": 4, "name": "本溪高新技术产业开发区管委会", "type": "开发区", "level": "地厅级", "parent": "本溪市", "location": "本溪市高新区"},
    {"id": 5, "name": "本溪市公安局溪湖分局", "type": "公安", "level": "县处级", "parent": "本溪市公安局", "location": "本溪市溪湖区"},
    {"id": 6, "name": "中国共产党本溪市委员会", "type": "党委", "level": "地厅级", "parent": "辽宁省委", "location": "本溪市"},
]

positions = [
    # 郭鑫
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "~2025-2026", "end": "present", "rank": "县处级正职", "note": "区二十一届党代会(2026-07)代表二十届区委作报告; 于2026确认任书记"},
    {"person_id": 1, "org_id": 4, "title": "高新区管委会主任(待核)", "start": "~2026", "end": "present", "rank": "县处级正职?", "note": "溪湖区政府官网称之为高新区管委会主任; 与cnmc.gov.cn(何涛/李涛)存在冲突"},
    # 何宇翥
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "~2025", "end": "present", "rank": "县处级正职", "note": "2025年2月新闻报道已任区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "~2025", "end": "present", "rank": "县处级正职", "note": "兼任区长"},
    {"person_id": 2, "org_id": 3, "title": "本溪湖经济开发区党工委书记", "start": "~2025", "end": "present", "rank": "县处级正职", "note": "区长兼经开区书记"},
    # 杨于
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "~2023-2025", "end": "present", "rank": "县处级副职", "note": "负责区政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "~2023-2025", "end": "present", "rank": "县处级副职", "note": "区政府党组副书记"},
    # 王佳
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "~2025-2026", "end": "present", "rank": "县处级副职", "note": "区委常委、副区长"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "~2025-2026", "end": "present", "rank": "县处级副职", "note": ""},
    # 纪延妍
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "~2022", "end": "present", "rank": "县处级副职", "note": "民建会员"},
    # 巴勇
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "~2023", "end": "present", "rank": "县处级副职", "note": "公安、司法"},
    {"person_id": 6, "org_id": 5, "title": "区公安分局局长", "start": "~2023", "end": "present", "rank": "县处级副职", "note": "党委(分局), 二级高级警长"},
    # 王福牮
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "~2023", "end": "present", "rank": "县处级副职", "note": "工业、商务、科技"},
    # 管磊
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "~2026", "end": "present", "rank": "县处级副职", "note": "自然资源、住建、交通"},
    # 代萍
    {"person_id": 9, "org_id": 1, "title": "区委书记", "start": "~2021", "end": "~2025", "rank": "县处级正职", "note": "前任书记; 2025-04任内 (去向待查)"},
    {"person_id": 9, "org_id": 2, "title": "区长", "start": "~2017", "end": "~2021", "rank": "县处级正职", "note": "后转任区委书记"},
    # 高飞
    {"person_id": 10, "org_id": 2, "title": "区长", "start": "~2021-2022", "end": "~2024-2025", "rank": "县处级正职", "note": "前任区长 (2024-10仍任已内)"},
    # 何涛
    {"person_id": 11, "org_id": 6, "title": "市委副书记、政法委书记", "start": "~2025", "end": "present", "rank": "地厅级副职", "note": "本溪高新区党工委书记"},
]

relationships = [
    # 郭鑫 与 何宇翥 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "区委书记与区长搭档", "overlap_org": "溪湖区", "overlap_period": "2025-present", "confidence": "confirmed"},
    # 郭鑫 与 代萍 (前后任书记)
    {"person_a": 1, "person_b": 9, "type": "predecessor_successor", "context": "继任区委书记", "overlap_org": "溪湖区", "overlap_period": "~2025交接", "confidence": "confirmed"},
    # 何宇翥 与 高飞 (前后任区长)
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor", "context": "继任区长", "overlap_org": "溪湖区", "overlap_period": "~2025交接", "confidence": "confirmed"},
    # 郭鑫 与 何涛 (跨区: 高新区关联)
    {"person_a": 1, "person_b": 11, "type": "cross_region_link", "context": "区委书记(兼高新区管委会主任候选) 与 市委副书记/高新区党工委书记 之高新区交叉", "overlap_org": "本溪高新区", "overlap_period": "~2026", "confidence": "plausible"},
    # 杨于 与 何宇翥 (常务搭档)
    {"person_a": 3, "person_b": 2, "type": "co_leadership", "context": "常务副区长与区长搭档", "overlap_org": "溪湖区政府", "overlap_period": "2025-", "confidence": "confirmed"},
]


# ── Person JSONs ─────────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for core figures (书记 & 区长, plus key deputies)."""

    jdx = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "本溪市",
            "region": "溪湖区",
            "job": "区委书记",
            "task_id": "liaoning_溪湖区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "benxi_xihu_guoxin",
            "name": "郭鑫",
            "aliases": [],
            "gender": "男",
            "ethnicity": "待查（推断汉族）",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "郭鑫_unknown",
                "name_birthplace": "郭鑫_unknown",
                "official_profile_url": "http://www.xihu.gov.cn/xwzx/gzdt/content_665644",
            },
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中国共产党本溪市溪湖区委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": [
            {"start": "~2025-2026", "end": "present", "org": "本溪市溪湖区委", "title": "区委书记",
             "level": "县处级", "location": "本溪市溪湖区", "system": "party", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2026-07 区二十一届党代会任书记并作报告", "confidence": "confirmed",
             "source_ids": ["S001", "S003"]},
            {"start": "~2026", "end": "present", "org": "本溪高新技术产业开发区管委会", "title": "管委会主任（待核）",
             "level": "县处级", "location": "本溪高新区", "system": "development_zone", "rank": "县处级正职",
             "is_key_promotion": False, "notes": "溪湖区政府官网（2026-07-23）称'高新区管委会主任郭鑫'；cnmc官网列何涛/李涛为党工委书记/管委会主任，存在冲突，标记 plausible。",
             "confidence": "plausible", "source_ids": ["S002"]},
        ],
        "organizations": [{"name": "本溪市溪湖区党委", "role": "现任区委书记"},
                          {"name": "本溪高新区管委会", "role": "管委会主任（待核）"}],
        "relationships": [
            {"person": "何宇翥", "person_id": "benxi_xihu_heyuzhu", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长", "overlap_org": "溪湖区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "代萍", "person_id": "benxi_xihu_daiping", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "前后任区委书记交接", "overlap_org": "溪湖区",
             "overlap_period": "~2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        ],
        "governance_record": [
            {"period": "2026", "domain": "public_security", "achievement_or_event": "防汛隐患点位调研",
             "role_in_event": "区委书记带队", "measurable_outcome": "", "location": "溪湖区",
             "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "professional_profile": {
            "primary_specializations": ["党建", "经开区管理（待核）"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party", "development_zone"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "区委书记（现职），初始履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "多次走访调研（防汛点位/对接产业）", "confidence": "plausible", "source_ids": ["S003"]}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "区党代表大会开幕（区二十一届）", "url": "http://www.xihu.gov.cn/xwzx/gzdt/content_665644",
             "publisher": "溪湖区人民政府", "published_at": "2026-07-26", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "确认郭鑫为区委书记"},
            {"id": "S002", "title": "溪湖区委书记、高新区管委会主任郭鑫会见省能源研究会", "url": "http://www.xihu.gov.cn/xwzx/gzdt/content_665550",
             "publisher": "溪湖区人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "以高新区管委会主任为名"},
            {"id": "S003", "title": "区委书记郭鑫带队调研防汛隐患点位", "url": "http://www.xihu.gov.cn/xwzx/gzdt/content_664905",
             "publisher": "溪湖区人民政府", "published_at": "2026-07-08", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S005", "title": "区委书记、区总河长代萍开展巡河（前任）", "url": "http://www.xihu.gov.cn/xwzx/gzdt/content_644214",
             "publisher": "溪湖区人民政府", "published_at": "2025-04-30", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "代萍为前任区委书记"},
        ],
        "confidence_summary": {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium", "biggest_gap": "郭鑫完整履历（出生/籍贯/学历/南京履历）全部缺失",
        },
        "open_questions": [
            {"priority": "critical", "question": "郭鑫出生年、籍贯、教育背景、入党时间、参加工作时间", "why_it_matters": "基本身份信息缺失", "suggested_queries": ["郭鑫 简历 本溪 溪湖"], "last_attempted": AS_OF},
            {"priority": "high", "question": "郭鑫何时何地调任溪湖区委书记，前职为何", "why_it_matters": "判断其交流网络源头", "suggested_queries": ["郭鑫 任前公示 本溪"], "last_attempted": AS_OF},
            {"priority": "high", "question": "郭鑫是否确任本溪高新区管委会主任（官网冲突）", "why_it_matters": "跨区兼领是重要权力结构信号", "suggested_queries": ["本溪高新区 管委会主任 郭鑫"], "last_attempted": AS_OF},
        ],
    }

    hyz = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "本溪市", "region": "溪湖区",
            "job": "区长", "task_id": "liaoning_溪湖区", "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "benxi_xihu_he_yu_zhu",
            "name": "何宇翥",
            "aliases": [],
            "gender": "男",
            "ethnicity": "锡伯族",
            "birth": "1979-02",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "公共管理", "degree": "硕士", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "何宇翥_1979", "name_birthplace": "何宇翥_unknown", "official_profile_url": "http://www.xihu.gov.cn/ldzc/qzfld/content_634659"},
        },
        "current_status": {
            "current_post": "区长", "current_org": "本溪市溪湖区人民政府", "administrative_rank": "县处级正职",
            "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {"start": "~2025", "end": "present", "org": "本溪市溪湖区人民政府", "title": "区长",
             "level": "县处级", "location": "本溪市溪湖区", "system": "government", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2025年2月愈发频繁以区长身份出席区政府常务会议", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "2024", "end": "~2025", "org": "本溪湖经济开发区", "title": "主任/党工委书记",
             "level": "县处级", "location": "本溪市溪湖区", "system": "development_zone", "rank": "县处级正职",
             "is_key_promotion": False, "notes": "2024年5月以经开区主任身份出席; 提升为区长", "confidence": "plausible", "source_ids": ["S004"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任经开区主任之前的早年履历未找到公开资料", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "溪湖区人民政府", "role": "区长"},
                          {"name": "本溪湖经济开发区", "role": "经开区党工委书记"}],
        "relationships": [
            {"person": "郭鑫", "person_id": "benxi_xihu_guoxin", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长", "overlap_org": "溪湖区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "高飞", "person_id": "benxi_xihu_gaofei", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "继任区长", "overlap_org": "溪湖区", "overlap_period": "~2025",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance_record": [
            {"period": "2026", "domain": "economic_development", "achievement_or_event": "本溪湖经济开发区招商引资、审计",
             "role_in_event": "区政府负责人", "measurable_outcome": "", "location": "溪湖区", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {
            "primary_specializations": ["经济开发区管理", "公共管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["government", "development_zone"],
            "geographic_pattern": ["本溪市"],
            "promotion_velocity": {"summary": "经开区主任→区长（区内晋升）", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "technocratic", "evidence": "经开区主任出身，主攻招商引资与审计", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "speech_themes": [], "management_signals": [], "caveat": "推断自公开记录"},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "溪湖区区长官方简历", "url": "http://www.xihu.gov.cn/ldzc/qzfld/content_634659",
             "publisher": "溪湖区人民政府", "published_at": "2024-10", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "区政府第78次常务会议（何宇翥主持）", "url": "http://www.xihu.gov.cn/publicity/zdxx/hl8x/index.html",
             "publisher": "溪湖区人民政府", "published_at": "2026-03", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "区委副书记、区长高飞（前任）", "url": "http://www.xihu.gov.cn/xwzx/gzdt/content_633520",
             "publisher": "溪湖区人民政府", "published_at": "2024-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "本溪湖经济开发区主任何宇翥（2024-05）", "url": "http://www.xihu.gov.cn/gxxh/index.html",
             "publisher": "溪湖区人民政府", "published_at": "2024-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium"},
        ],
        "confidence_summary": {
            "identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
            "relationship_confidence": "medium", "biggest_gap": "何宇翥(任经开区主任前)更早的公开履历",
        },
        "open_questions": [
            {"priority": "high", "question": "何宇翥任本溪湖经开区管委会主任之前的职务", "why_it_matters": "判断晋升路径起点", "suggested_queries": ["何宇翥 简历 本溪"], "last_attempted": AS_OF},
        ],
    }

    yq = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "本溪市", "region": "溪湖区", "job": "常务副区长",
                                "task_id": "liaoning_溪湖区", "time_focus": "2025-2026"},
        "identity": {"person_id": "benxi_xihu_yangyu", "name": "杨于", "aliases": [], "gender": "男",
                     "ethnicity": "汉族", "birth": "1979-04", "birthplace": "", "native_place": "",
                     "education": [{"period": "", "institution": "中央党校", "major": "", "degree": "大学", "study_type": "party_school", "source_ids": ["S001"]}],
                     "party_join": "中共党员", "work_start": "", "dedupe_keys": {"name_birth": "杨于_1979", "name_birthplace": "杨于_unknown", "official_profile_url": "http://www.xihu.gov.cn/ldgk/qzfld/content_528530"}},
        "current_status": {"current_post": "常务副区长", "current_org": "本溪市溪湖区人民政府", "administrative_rank": "县处级副职",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": [
            {"start": "~2023", "end": "present", "org": "溪湖区政府", "title": "常务副区长", "level": "县处级",
             "location": "溪湖区", "system": "government", "rank": "县处级副职", "is_key_promotion": False,
             "notes": "负责政府常务工作，分管发改/财税/人社/应急等", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "organizations": [{"name": "溪湖区人民政府", "role": "常务副区长"}],
        "relationships": [
            {"person": "何宇翥", "person_id": "benxi_xihu_huang_yuzhu", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "区长与常务副区长搭档", "overlap_org": "溪湖区政府", "overlap_period": "2025-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": ["财政", "财税", "应急管理"], "career_pattern": "local_ladder",
                                 "systems_experience": ["government"], "geographic_pattern": ["本溪"],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现风险信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "常务副区长官方简历", "url": "http://www.xihu.gov.cn/lldgk/qfqld/content_528530",
             "publisher": "溪湖区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "区外履历"},
        "open_questions": [{"priority": "medium", "question": "杨于调任副区长前职务", "why_it_matters": "网络源", "suggested_queries": ["杨于 本溪 履历"], "last_attempted": AS_OF}],
    }

    person_dir = PERSONS_STAGING_DIR
    for fname, data in [
        (f"{TODAY_str}-辽宁省-本溪市-溪湖区-区委书记-郭鑫.json", jdx),
        (f"{TODAY_str}-辽宁省-本溪市-溪湖区-区长-何宇翥.json", hyz),
        (f"{TODAY_str}-辽宁省-本溪市-溪湖区-常务副区长-杨于.json", yq),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        fn = f.name
        if fn.startswith(TODAY_str) and "溪湖区" in fn and "本溪" in fn:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()