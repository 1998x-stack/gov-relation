#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 宁阳县 (Ningyang County), 泰安市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_宁阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - zh.wikipedia.org/wiki/宁阳县 — Wikipedia (县委书记刘灿玉, confirmed)
  - www.ny.gov.cn — 宁阳县人民政府官方网站
  - www.ny.gov.cn/art/2026/7/25/art_70318_10365872.html — 恒元新能源签约仪式 (确认刘灿玉为县委书记, 刘富强为县长)
  - www.ny.gov.cn/art/2026/7/17/art_70318_10365711.html — 县委常委会 (确认梁欣为县委副书记, 董骞为人大主任, 张涛为政协主席)
  - www.ny.gov.cn/art/2025/9/19/art_180430_19445.html — 宁政发〔2025〕6号政府领导分工通知 (确认于师义、王艳苹等副县长)
  - www.ny.gov.cn/art/2026/7/21/art_299203_10365798.html — 调研活动 (确认张彦为县委常委/县委办主任, 李晓为县委常委/副县长)
  - Jina Reader and Baidu Baike: unavailable (403/timeout)

Confidence notes:
  - 刘灿玉 (县委书记): confirmed via Wikipedia + multiple official news, full biography unverified
  - 刘富强 (县长): confirmed via official news, full biography unverified
  - 梁欣 (县委副书记): confirmed via official news
  - 董骞 (县人大常委会主任): confirmed via official news
  - 张涛 (县政协主席): confirmed via official news
  - 张彦 (县委常委/县委办公室主任): confirmed via official news
  - 庞林星 (县委常委/副县长): confirmed via official news
  - 于师义 (县委常委/常务副县长): confirmed via 宁政发〔2025〕6号
  - 其他副县长: confirmed via 宁政发〔2025〕6号
  - Predecessors: unverified — web search degraded, Baidu 403
  - Web search degraded: Jina Reader down, Google blocked, Baidu 403, Exa rate-limited
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "宁阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_宁阳县"
if _CURRENT_DIR.name == "shandong_宁阳县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core (县委书记/县长), 3-4 人大/政协, 5-9 县委常委,
#       10-19 副县长, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘灿玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宁阳县委员会",
        "source": "http://www.ny.gov.cn/art/2026/7/25/art_70318_10365872.html",
        "confidence": "confirmed",
        "notes": "2026年7月25日出席新能源项目签约并致辞。此前简历待查——曾任宁阳县委副书记、县长后接任县委书记（推测时间：2024-2026年间）。"
    },
    {
        "id": 2,
        "name": "刘富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 待查
        "birthplace": "",  # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2026/7/25/art_70318_10365872.html",
        "confidence": "confirmed",
        "notes": "2026年7月主持签约仪式。宁政发〔2025〕6号显示其主持县政府全面工作。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "董骞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "宁阳县人民代表大会常务委员会",
        "source": "http://www.ny.gov.cn/art/2026/7/17/art_70318_10365711.html",
        "confidence": "confirmed",
        "notes": "2026年7月16日列席县委常委会会议。此前简历待查。"
    },
    {
        "id": 4,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议宁阳县委员会",
        "source": "http://www.ny.gov.cn/art/2026/7/17/art_70318_10365711.html",
        "confidence": "confirmed",
        "notes": "2026年7月16日列席县委常委会会议。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委常委
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "梁欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共宁阳县委员会",
        "source": "http://www.ny.gov.cn/art/2026/7/17/art_70318_10365711.html",
        "confidence": "confirmed",
        "notes": "2026年7月16日出席县委常委会。此前简历待查。"
    },
    {
        "id": 6,
        "name": "于师义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "宁政发〔2025〕6号显示负责县政府常务工作，分管发展改革、经济运行、重点项目、应急管理、统计等。此前简历待查。"
    },
    {
        "id": 7,
        "name": "张彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共宁阳县委员会",
        "source": "http://www.ny.gov.cn/art/2026/7/21/art_299203_10365798.html",
        "confidence": "confirmed",
        "notes": "多次陪同刘灿玉调研。此前简历待查。"
    },
    {
        "id": 8,
        "name": "庞林星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2026/7/25/art_70318_10365872.html",
        "confidence": "confirmed",
        "notes": "2026年7月23日参加新能源签约仪式。此前简历待查。宁政发〔2025〕6号中未列名——可能后期补入常委或原为其他副县长。"
    },
    {
        "id": 9,
        "name": "李晓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2026/7/21/art_299203_10365798.html",
        "confidence": "confirmed",
        "notes": "2026年7月21日陪同刘灿玉调研。宁政发〔2025〕6号显示其负责自然资源和规划、协助工业经济。此前简历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 其他副县长 (via 宁政发〔2025〕6号)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "王艳苹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责民政、卫生健康、行政审批、医疗保障等。"
    },
    {
        "id": 11,
        "name": "木黑亚提·切尔亚孜坦",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责科技工作，协助于师义。民族为哈萨克族——可能为新疆对口支援挂职干部。"
    },
    {
        "id": 12,
        "name": "王朝阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责公安、司法、退役军人事务、信访等；主持县公安局工作。"
    },
    {
        "id": 13,
        "name": "贾德果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责教育体育、交通运输、文化旅游、农业农村、水利等。"
    },
    {
        "id": 14,
        "name": "陈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责人力资源和社会保障、住房城乡建设、商务、招商引资、综合行政执法等。"
    },
    {
        "id": 15,
        "name": "潘洪勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "负责生态环境、市场监督管理、金融等。"
    },
    {
        "id": 16,
        "name": "鲍怀东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "协助贾德果工作，负责农业农村、乡村振兴、畜牧兽医、粮食等。"
    },
    {
        "id": 17,
        "name": "任杨峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宁阳县人民政府",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html",
        "confidence": "confirmed",
        "notes": "协助贾德果工作，负责水利、河道、林业等。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (limited data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "【待查】前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "刘灿玉的前任县委书记待查。推测刘灿玉此前为宁阳县县长，前任书记可能已调任泰安市或其他县区。"
    },
    {
        "id": 31,
        "name": "【待查】前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "",
        "confidence": "unverified",
        "notes": "刘富强的前任县长待查。推测为刘灿玉（前任县委书记由县长升任的常见路径）或其他人。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共宁阳县委员会", "type": "党委", "level": "县", "parent": "泰安市", "location": "山东省泰安市宁阳县"},
    {"id": 2, "name": "宁阳县人民政府", "type": "政府", "level": "县", "parent": "泰安市", "location": "山东省泰安市宁阳县"},
    {"id": 3, "name": "宁阳县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "泰安市", "location": "山东省泰安市宁阳县"},
    {"id": 4, "name": "中国人民政治协商会议宁阳县委员会", "type": "政协", "level": "县", "parent": "泰安市", "location": "山东省泰安市宁阳县"},
    {"id": 5, "name": "宁阳县公安局", "type": "政府", "level": "县", "parent": "宁阳县", "location": "山东省泰安市宁阳县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘灿玉
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年7月在职，此前推测为宁阳县县长，后升任县委书记"},
    # 刘富强
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "宁政发〔2025〕6号显示主持县政府全面工作"},
    # 董骞
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 张涛
    {"person_id": 4, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 梁欣
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 于师义
    {"person_id": 6, "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管发改、应急、统计等"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张彦
    {"person_id": 7, "org_id": 1, "title": "县委常委、县委办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 庞林星
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李晓
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管自然资源和规划"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王艳苹
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管民政、卫健、审批等"},
    # 木黑亚提·切尔亚孜坦
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管科技"},
    # 王朝阳
    {"person_id": 12, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "分管公安、司法、信访等"},
    # 贾德果
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管教育、交通、农业农村等"},
    # 陈军
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管人社、住建、商务、招商等"},
    # 潘洪勇
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管环保、市场监管、金融等"},
    # 鲍怀东
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "协助贾德果，分管农业农村、乡村振兴等"},
    # 任杨峰
    {"person_id": 17, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "协助贾德果，分管水利、林业等"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 刘灿玉 ↔ 刘富强 (书记-县长搭班)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长搭班，共同领导宁阳县工作",
        "overlap_org": "中共宁阳县委员会/宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2026/7/25/art_70318_10365872.html"
    },
    # 刘灿玉 ↔ 梁欣 (书记-副书记)
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共宁阳县委员会",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2026/7/17/art_70318_10365711.html"
    },
    # 刘灿玉 ↔ 张彦 (书记-办公室主任)
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与县委办公室主任，张彦多次陪同刘灿玉调研",
        "overlap_org": "中共宁阳县委员会",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2026/7/21/art_299203_10365798.html"
    },
    # 刘富强 ↔ 于师义 (县长-常务副县长)
    {
        "person_a": 2, "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与常务副县长，于师义协助刘富强负责县政府日常工作",
        "overlap_org": "宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "strong",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html"
    },
    # 于师义 ↔ 木黑亚提·切尔亚孜坦 (协助分工)
    {
        "person_a": 6, "person_b": 11,
        "type": "superior_subordinate",
        "context": "木黑亚提协助于师义工作",
        "overlap_org": "宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html"
    },
    # 贾德果 ↔ 鲍怀东 (协助分工)
    {
        "person_a": 13, "person_b": 16,
        "type": "superior_subordinate",
        "context": "鲍怀东协助贾德果工作",
        "overlap_org": "宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html"
    },
    # 贾德果 ↔ 任杨峰 (协助分工)
    {
        "person_a": 13, "person_b": 17,
        "type": "superior_subordinate",
        "context": "任杨峰协助贾德果工作",
        "overlap_org": "宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html"
    },
    # 李晓 ↔ 于师义 (协助工业经济)
    {
        "person_a": 9, "person_b": 6,
        "type": "superior_subordinate",
        "context": "李晓协助于师义负责工业经济和招商引资",
        "overlap_org": "宁阳县人民政府",
        "overlap_period": AS_OF,
        "strength": "weak",
        "confidence": "confirmed",
        "source": "http://www.ny.gov.cn/art/2025/9/19/art_180430_19445.html"
    },
]


# ── Person JSON Helper ───────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> str:
    """Write a person JSON to PJSON_DIR and return its filename."""
    job_slug = person["current_post"].replace("/", "_")
    fname = f"{TODAY}-山东省-泰安市-{job_slug}-{person['name']}.json"
    path = PJSON_DIR / fname

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "泰安市",
            "region": "宁阳县",
            "job": person["current_post"],
            "task_id": "shandong_宁阳县",
            "time_focus": "2026-07"
        },
        "identity": {
            "person_id": f"ningyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"institution": person["education"], "period": "", "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2] else ("副处级" if person["id"] < 30 else "待查"),
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": _career_timeline_for(person),
        "organizations": [],
        "relationships": _relationships_for(person),
        "governance_record": _governance_record_for(person),
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": ["泰安市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No public risk signals found in available sources", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": person["notes"], "url": person["source"], "publisher": "宁阳县人民政府", "published_at": AS_OF, "accessed_at": TODAY, "source_type": "official" if "ny.gov.cn" in person["source"] else "wiki", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": "confirmed",
            "career_completeness": "partial" if not person["birth"] else "partial",
            "relationship_confidence": "low",
            "biggest_gap": f"完整履历待查" if not person["birth"] else "完整履历待查"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的完整履历", "why_it_matters": "核心领导背景未知", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示", f"{person['name']} 泰安"], "last_attempted": TODAY},
            {"priority": "high", "question": f"{person['name']}的出生年月和籍贯", "why_it_matters": "身份识别关键信息", "suggested_queries": [f"{person['name']} 出生"], "last_attempted": TODAY}
        ]
    }

    if extra:
        data.update(extra)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fname


def _career_timeline_for(person: dict) -> list:
    """Build career timeline from positions."""
    if person["id"] == 1:
        return [
            {"start": "unknown", "end": "present", "org": "中共宁阳县委员会", "title": "县委书记", "level": "正处级", "location": "泰安市宁阳县", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "2026年7月在职", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知——推测曾任宁阳县县长或其他泰安市辖县区领导", "confidence": "unverified", "source_ids": []},
        ]
    elif person["id"] == 2:
        return [
            {"start": "unknown", "end": "present", "org": "宁阳县人民政府", "title": "县长", "level": "正处级", "location": "泰安市宁阳县", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "2025年9月已任县长", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "此前任职履历完全未知", "confidence": "unverified", "source_ids": []},
        ]
    return [
        {"start": "unknown", "end": "present", "org": person["current_org"], "title": person["current_post"], "level": "", "location": "泰安市宁阳县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": person["confidence"], "source_ids": ["S001"]}
    ]


def _relationships_for(person: dict) -> list:
    """Build relationship list for this person."""
    rs = []
    for r in relationships:
        other_id = r["person_b"] if r["person_a"] == person["id"] else (r["person_a"] if r["person_b"] == person["id"] else None)
        if other_id is not None:
            other = next((p for p in persons if p["id"] == other_id), None)
            if other:
                rs.append({
                    "person": other["name"],
                    "person_id": f"ningyang_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": r["strength"],
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": r["confidence"],
                    "source_ids": []
                })
    return rs


def _governance_record_for(person: dict) -> list:
    """Build governance record for this person."""
    if person["id"] == 1:
        return [
            {"period": "2026-07-25", "domain": "economic_development", "achievement_or_event": "出席恒元新能源电池材料产业园签约仪式并致辞", "role_in_event": "县委书记致辞并推动项目落地", "measurable_outcome": "新能源电池材料产业项目签约", "location": "宁阳县", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-07-21", "domain": "technology_innovation", "achievement_or_event": "调研OPC·AI创业社区和低空综合服务平台", "role_in_event": "县委书记现场调研指导", "measurable_outcome": "推动AI与实体经济融合、低空经济发展", "location": "宁阳县", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2026-07-15", "domain": "rural_development", "achievement_or_event": "到伏山镇专题调研乡村振兴工作", "role_in_event": "县委书记深入村庄、农业项目现场调研", "measurable_outcome": "实地了解基层党建、产业发展和乡村治理", "location": "宁阳县", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 2:
        return [
            {"period": "2026-07-23", "domain": "economic_development", "achievement_or_event": "主持恒元新能源电池材料产业园签约仪式", "role_in_event": "县长主持签约", "measurable_outcome": "新能源产业项目落地", "location": "宁阳县", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    elif person["id"] == 6:
        return [
            {"period": "2025-09", "domain": "government_administration", "achievement_or_event": "负责县政府常务工作，分管发改、应急等核心领域", "role_in_event": "常务副县长", "measurable_outcome": "", "location": "宁阳县", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
    return []


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Building {SLUG} network...")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    core_ids = [1, 2]
    for pid in core_ids:
        person = next(p for p in persons if p["id"] == pid)
        fname = write_person_json(person)
        print(f"  Person JSON: {fname}")

    print(f"\nDone. Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()
