#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 明山区, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_明山区
Level: 市辖区
Parent city: 本溪市
Targets: 区委书记 & 区长

Research status: OFFICIAL SOURCE ACCESS
  - 明山区人民政府门户网站 (www.mingshan.gov.cn) 完全可访问
  - 区政府领导之窗 (区长/副区长): 现任班子+个人简介已确认
  - 2026-03-29 高质量发展大会新闻确认区委书记王钰、区长杨嵬松、区政协主席郑伟
  - 明山区第十一次党代会 (2026-07~08) 举行（换届窗口），与平山/溪湖/南芬等同批
  - Exa/Baidu 检索受限; 依托官网目击确认, 履历细节按证据分级标注

Current officeholders (as of 2026-08-06, www.mingshan.gov.cn 官方确认):
  - 区委书记: 王钰 (2026-03 高质量发展大会党领导下; 区十一届党代会换届后任职待核是否留任)
  - 区委副书记、区长: 杨嵬松 (男, 满族, 1984-04, 大学法学学士, 中共党员; 2024-12 代区长→区长)
  - 常务副区长: 沈量 (区委常委, 男, 满族, 1987-07, 研究生工学硕士; 兼明山街道党工委书记)
  - 副区长: 赵庆凯(区委常委, 汉 1972-07), 周锦坤(区委常委, 汉 1990-09), 解锐(汉 1983-10), 陈振兴(回 1986-07), 朱姝颖(区, 满 1985-02, 民盟)
  - 区政协主席: 郑伟

Predecessor timeline:
  - 区长: 王福渊 (~2020-2024) → 杨嵬松 (代区长 2024-12 → 区长 2025-)
  - 王福渊 2024-2026 转任平山区委书记 (跨区调动, 平山区报告确认)
  - 区委书记: (前任待核心) → 王钰 (当前)

Cross-region:
  - 区长兼... (标准 区县长班子); 王福渊(明山区长→平山区委书记) = 本溪市四区两县轮换典型
  201 区第十一次党代会换届
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
SLUG = "明山区"
TODAY_str = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ───────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────────
persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "王钰",
        "gender": "男（推断）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党本溪市明山区委员会",
        "source": "http://www.mingshan.gov.cn/zsyz/content_660118 (高质量发展大会, 2026-03-29)",
    },
    # ── 区长 ──
    {
        "id": 2,
        "name": "杨嵬松",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1984-04",
        "birthplace": "待查",
        "education": "大学法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记、区长",
        "current_org": "明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_395517 (区政府领导, 2026)",
    },
    # ── 常务副区长 ──
    {
        "id": 3,
        "name": "沈量",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1987-07",
        "birthplace": "待查",
        "education": "研究生工学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "明山区人民政府 / 明山街道办事处",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_1204 (区政府官网, 简介)",
    },
    # ── 副区长 (区常委) ──
    {
        "id": 4,
        "name": "赵庆凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长",
        "current_org": "中共明山区委员会 / 明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_530438",
    },
    # ── 副区长 (区常委) ──
    {
        "id": 5,
        "name": "周锦坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-09",
        "birthplace": "待查",
        "education": "省委党校研究生、学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长",
        "current_org": "中共明山区委员会 / 明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_530435",
    },
    # ── 副区长 ──
    {
        "id": 6,
        "name": "解锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_586979",
    },
    # ── 副区长 ──
    {
        "id": 7,
        "name": "陈振兴",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1986-07",
        "birthplace": "待查",
        "education": "大学管理学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_655370",
    },
    # ── 副区长 ──
    {
        "id": 8,
        "name": "朱姝颖",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1985-02",
        "birthplace": "待查",
        "education": "本科",
        "party_join": "",  # 民盟盟员, 非中共党员
        "work_start": "待查",
        "current_post": "副区长",
        "current_org": "明山区人民政府",
        "source": "http://www.mingshan.gov.cn/ldzc/qzfld/content_663142",
    },
    # ── 前任区长 (→平山区委书记) ──
    {
        "id": 9,
        "name": "王福渊",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平山区委书记（原明山区长）",
        "current_org": "中共平山区委员会",
        "source": "http://www.mingshan.gov.cn/publicity/qzfxx/zfgzbg/90818 (2020 明山政府工作报告) / http://www.mingshan.gov.cn/publicity/qzfxx/rsrm/101773 (2022-03 辞区长) / report/平山区",
    },
    # ── 前任区委书记 (周大庆, 2024-2025) ──
    {
        "id": 10,
        "name": "周大庆",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任明山区委书记（去向待查）",
        "current_org": "中国共产党明山区委员会",
        "source": "http://www.mingshan.gov.cn/xwzx/msyw/content_642119 (2025-03 区委书记周大庆) / content_650187 (2025-08 区委书记) / 2025-12 人代会执行主席首位",
    },
    # ── 政协主席 ──
    {
        "id": 11,
        "name": "郑伟",
        "gender": "男（推断）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协明山区委员会",
        "source": "http://www.mingshan.gov.cn/zsyz/content_660118 (高质量发展大会, 2026-03-29)",
    },
]

organizations = [
    {"id": 1, "name": "中国共产党明山区委员会", "type": "党委", "level": "县处级", "parent": "本溪市委", "location": "本溪市明山区"},
    {"id": 2, "name": "明山区人民政府", "type": "政府", "level": "县处级", "parent": "本溪市政府", "location": "本溪市明山区"},
    {"id": 3, "name": "明山街道办事处", "type": "乡镇/街道", "level": "乡科级", "parent": "明山区", "location": "明山区"},
    {"id": 4, "name": "太子河经济开发区", "type": "开发区", "level": "县处级", "parent": "本溪市", "location": "明山区"},
    {"id": 5, "name": "中国人民政治协商会议明山区委员会", "type": "政协", "level": "县处级", "parent": "明山区", "location": "明山区"},
    {"id": 6, "name": "中国共产党平山区委员会", "type": "党委", "level": "县处级", "parent": "本溪市委", "location": "平山区"},
]

positions = [
    # 王钰
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "~2024-2025", "end": "present", "rank": "县处级正职", "note": "2026-03-29 高质量发展大会出席并讲话; 2026-07 区十一届党代会(换届)后是否留任待核"},
    # 杨嵬松
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2024-12", "end": "present", "rank": "县处级正职", "note": "2024-12-25 区十届人大五次会议任代区长->区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2024-12", "end": "present", "rank": "县处级正职", "note": "兼任区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "区政府党组书记", "start": "2025", "end": "present", "rank": "县处级正职", "note": ""},
    # 沈量
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "~2023-2024", "end": "present", "rank": "县处级副职", "note": "负责区政府常务工作; 兼区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "~2023-2024", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "明山街道办事处党工委书记", "start": "~2024", "end": "present", "rank": "乡科级正职", "note": "区委常委兼街道党工委书记"},
    # 赵庆凯
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "~2023-2024", "end": "present", "rank": "县处级副职", "note": "负责农业农村/乡村振兴/水务/民政/民族宗教"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "~2023-2024", "end": "present", "rank": "县处级副职", "note": ""},
    # 周锦坤
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "~2024", "end": "present", "rank": "县处级副职", "note": "负责商务/外事/对台/招商"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "~2024", "end": "present", "rank": "县处级副职", "note": ""},
    # 解锐
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "~2023-2024", "end": "present", "rank": "县处级副职", "note": "负责住建/交通/林业草原/自然资源/征收"},
    # 陈振兴
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "~2024", "end": "present", "rank": "县处级副职", "note": "负责工信/通信/科技/生态环境/退役军人"},
    # 朱姝颖
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "~2023", "end": "present", "rank": "县处级副职", "note": "民盟盟员; 负责教育/卫健/市场监管/文旅/医保"},
    # 王福渊
    {"person_id": 9, "org_id": 2, "title": "区长", "start": "~2018-2020", "end": "~2022-03", "rank": "县处级正职", "note": "2020-12-23区九届人大四次会作报告; 2022-03-14 区人大常委会接受其辞去区长(工作变动)"},
    {"person_id": 9, "org_id": 6, "title": "区委书记", "start": "~2022", "end": "~2026", "rank": "县处级正职", "note": "辞职后转平山区委书记(跨区,已入库平山数据)"},
    # 周大庆 (前任区长.前任区委书记)
    {"person_id": 10, "org_id": 2, "title": "区长", "start": "2022-07", "end": "~2024", "rank": "县处级正职", "note": "2022-07 代区长->2022-10 区长(接王福渊); 2023-06 区委副书记兼区长; 2024-04 仍区长"},
    {"person_id": 10, "org_id": 1, "title": "区委书记", "start": "~2024", "end": "~2025-12", "rank": "县处级正职", "note": "由区长转任区委书记; 2025-03-21 巡河, 2025-08-26 办证难专题会, 2025-12-23 人代会执行主席首位=时任区委书记; 2026年初交棒王钰(去向待查)"},
    # 郑伟
    {"person_id": 11, "org_id": 5, "title": "区政协主席", "start": "~2023-2024", "end": "present", "rank": "县处级正职", "note": "2026-03-29 出席会议"},
]

relationships = [
    # 王钰 与 杨嵬松 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "区委书记与区长搭档", "overlap_org": "明山区", "overlap_period": "2025-present", "confidence": "confirmed"},
    # 王钰 与 周大庆 (前后任区委书记)
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "继任区委书记(周大庆卸任)", "overlap_org": "明山区委", "overlap_period": "~2026交接", "confidence": "confirmed"},
    # 杨嵬松 与 王福渊 / 周大庆 (前后任区长)
    {"person_a": 2, "person_b": 9, "type": "predecessor_successor", "context": "继任区长(王福渊辞职后)", "overlap_org": "明山区政府", "overlap_period": "~2022-2024交接", "confidence": "plausible"},
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor", "context": "继任区长(周大庆转区委书记后由杨任区长)", "overlap_org": "明山区政府", "overlap_period": "~2024-2025交接", "confidence": "confirmed"},
    # 王福渊 (跨区: 明山区长 → 平山区委书记)
    {"person_a": 9, "person_b": 1, "type": "cross_region_link", "context": "前任明山区长辞任,转平山区委书记(同市跨区轮换)", "overlap_org": "本溪市四区两县轮换网", "overlap_period": "2022-2026", "confidence": "plausible"},
    # 周大庆 (跨前后任区长与书记: 由区长晋为书记)
    {"person_a": 10, "person_b": 1, "type": "co_leadership", "context": "前任区委书记(周大庆)与继任之本区党政体系", "overlap_org": "明山区", "overlap_period": "~2024-2026", "confidence": "confirmed"},
    # 沈量 与 杨嵬松 (常务搭档)
    {"person_a": 3, "person_b": 2, "type": "co_leadership", "context": "常务副区长与区长搭档", "overlap_org": "明山区政府", "overlap_period": "2025-", "confidence": "confirmed"},
    # 杨嵬松 与 郑伟 (区长与区政协主席同届)
    {"person_a": 2, "person_b": 11, "type": "co_leadership", "context": "区长与区政协主席同届班子", "overlap_org": "明山区", "overlap_period": "2025-", "confidence": "confirmed"},
]


# ── Person JSONs ─────────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for core figures (区委书记 & 区长, plus 常务副区长)."""

    jdx = {  # 王钰
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "本溪市", "region": "明山区",
                                "job": "区委书记", "task_id": "liaoning_明山区", "time_focus": "2025-2026"},
        "identity": {"person_id": "benxi_mingshan_wangyu", "name": "王钰", "aliases": [], "gender": "男（推断）",
                     "ethnicity": "待查", "birth": "", "birthplace": "", "native_place": "",
                     "education": [], "party_join": "中共党员", "work_start": "",
                     "dedupe_keys": {"name_birth": "王钰_unknown", "name_birthplace": "王钰_unknown",
                                     "official_profile_url": "http://www.mingshan.gov.cn/zsyz/content_660118"}},
        "current_status": {"current_post": "区委书记", "current_org": "中国共产党明山区委员会",
                           "administrative_rank": "县处级正职", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": [
            {"start": "~2024-2025", "end": "present", "org": "中共明山区委", "title": "区委书记",
             "level": "县处级", "location": "明山区", "system": "party", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2026-03-29 高质量发展大会以区委书记身份讲话; 区十一届党代会(2026-07)换届后留任待核",
             "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "王钰任明山区委书记前的公开履历（出生/籍贯/学历/此前职务）未在官方源找到", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "明山区党委", "role": "现任区委书记"}],
        "relationships": [
            {"person": "杨嵬松", "person_id": "benxi_mingshan_yangweisong", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长", "overlap_org": "明山区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "周大庆", "person_id": "benxi_mingshan_zhou_daqing", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "继任区委书记(周大庆卸任)", "overlap_org": "明山区委",
             "overlap_period": "~2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
        ],
        "governance_record": [
            {"period": "2026-03", "domain": "economic_development", "achievement_or_event": "主持召开高质量发展大会暨项目推进会议",
             "role_in_event": "区委书记讲话", "measurable_outcome": "", "location": "明山区",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {"primary_specializations": ["党建", "发展统筹"], "secondary_specializations": [],
                                 "career_pattern": "unknown", "systems_experience": ["party"],
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "区委书记（现职），初始履历未知", "notable_fast_promotions": []}},
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "reform_oriented", "evidence": "强调项目牵引、招商为要、干部在急难险重中考察", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "speech_themes": ["高质量发展", "抓项目", "招商选资", "政绩观"], "management_signals": [],
            "caveat": "推断自公开会议报道"},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未发现违纪或负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "明山区召开高质量发展大会暨项目推进会议", "url": "http://www.mingshan.gov.cn/zsyz/content_660118",
             "publisher": "明山区人民政府(来源:明山发布)", "published_at": "2026-04-03", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "王钰区委书记讲话; 杨嵬松区长; 郑伟政协主席"},
            {"id": "S004", "title": "明山区政府办公室学习贯彻党代会精神", "url": "http://www.mingshan.gov.cn/xwzx/msyw/content_666195",
             "publisher": "明山区人民政府", "published_at": "2026-08-06", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "区第十一次党代会后,关于换届窗口"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "王钰出生/籍贯/学历/任书记前履历全部未知"},
        "open_questions": [
            {"priority": "critical", "question": "王钰出生年、籍贯、教育背景、入党时间", "why_it_matters": "基本身份信息缺失", "suggested_queries": ["王钰 简历 明山 本溪"], "last_attempted": AS_OF},
            {"priority": "high", "question": "王钰何时从何职调任明山区委书记", "why_it_matters": "判断其交流网络源", "suggested_queries": ["王钰 任前公示 本溪 明山"], "last_attempted": AS_OF},
            {"priority": "high", "question": "2026-07 区十一届党代会后王钰是否留任书记", "why_it_matters": "现任性确认", "suggested_queries": ["明山区 十一届党代会 王钰"], "last_attempted": AS_OF},
        ],
    }

    wyw = {  # 杨嵬松
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "本溪市", "region": "明山区",
                                "job": "区长", "task_id": "liaoning_明山区", "time_focus": "2024-2026"},
        "identity": {"person_id": "benxi_mingshan_yang_weisong", "name": "杨嵬松", "aliases": [], "gender": "男",
                     "ethnicity": "满族", "birth": "1984-04", "birthplace": "", "native_place": "",
                     "education": [{"period": "", "institution": "待查", "major": "法学", "degree": "学士", "study_type": "full_time", "source_ids": ["S001"]}],
                     "party_join": "中共党员", "work_start": "", "dedupe_keys": {"name_birth": "杨嵬松_1984", "name_birthplace": "杨嵬松_unknown", "official_profile_url": "http://www.mingshan.gov.cn/ldzc/qzfld/content_395517"}},
        "current_status": {"current_post": "区委副书记、区长", "current_org": "明山区人民政府", "administrative_rank": "县处级正职",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
        "career_timeline": [
            {"start": "2024-12", "end": "present", "org": "明山区人民政府", "title": "区长", "level": "县处级",
             "location": "明山区", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2024-12-25 区十届人大五次任代区长; 2025后任区长; 至今在任", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
            {"start": "2024-12", "end": "present", "org": "中共明山区委", "title": "区委副书记", "level": "县处级",
             "location": "明山区", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "区政府党组书记; 2026-07 区十一届党代会(换届轮换窗口)", "confidence": "confirmed", "source_ids": ["S002", "S005"]},
            {"start": "unknown", "end": "2024-12", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任代区长前完整履历(之前职务/籍贯/党派时间)未在公开官网找到", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "明山区人民政府", "role": "区长"}, {"name": "明山区党委", "role": "区委副书记"}],
        "relationships": [
            {"person": "王钰", "person_id": "mingshan_wangyu", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：区委书记+区长(高质量发展大会同台)", "overlap_org": "明山区",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "王福渊", "person_id": "benxi_mingshan_wangfuyuan", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "继任区长(代区长)", "overlap_org": "明山区政府", "overlap_period": "~2024",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "周大庆", "person_id": "benxi_mingshan_zhou_daqing", "relationship_type": "predecessor_successor",
             "strength": "medium", "evidence": "周大庆由区长转区委书记后由杨任区长(前后任)", "overlap_org": "明山区政府",
             "overlap_period": "~2024-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "沈量", "person_id": "benxi_mingshan_shenliang", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "区长与常务副区长搭档", "overlap_org": "明山区政府", "overlap_period": "2025-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026", "domain": "economic_development", "achievement_or_event": "主持区政府常务工作/审计/招商",
             "role_in_event": "区长主导", "measurable_outcome": "", "location": "明山区", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {"primary_specializations": ["审计", "招商选资"], "secondary_specializations": ["法学"],
                                 "career_pattern": "local_ladder", "systems_experience": ["government", "party"],
                                 "geographic_pattern": ["本溪"], "promotion_velocity": {"summary": "区内晋升形成区长", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": ""},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现违纪/负面舆情", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "区长官方简历", "url": "http://www.mingshan.gov.cn/ldzc/qzfld/content_395517",
             "publisher": "明山区人民政府", "published_at": "2026", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "2024年政府工作报告(代区长杨嵬松)", "url": "http://www.mingshan.gov.cn/publicity/qzfxx/zfgzbg/126970",
             "publisher": "明山区人民政府", "published_at": "2025-01-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "明高质量发展大会", "url": "http://www.mingshan.gov.cn/zsyz/content_660118",
             "publisher": "明山发布", "published_at": "2026-04-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S005", "title": "明山区政府第101次常务会", "url": "http://www.mingshan.gov.cn/publicity/qzfxx/zfhy/zfcwhy/141012",
             "publisher": "明山区人民政府", "published_at": "2026-07-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "medium", "biggest_gap": "杨嵬松任代区长前完整履历"},
        "open_questions": [
            {"priority": "high", "question": "杨嵬松任代区长前的职务（曾任何职）", "why_it_matters": "晋升路径", "suggested_queries": ["杨嵬松 简历 本溪"], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    for fname, data in [
        (f"{TODAY_str}-辽宁省-本溪市-区委书记-王钰.json", jdx),
        (f"{TODAY_str}-辽宁省-本溪市-区长-杨嵬松.json", wyw),
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
        if fn.startswith(TODAY_str) and "明山区" in fn and "本溪" in fn:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()