#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 岳麓区 (Yuelu District), 长沙市, 湖南省.

Investigation date: 2026-08-06
Task ID: hunan_岳麓区
Level: 市辖区
Targets: 区委书记 & 区长

Context — 区政合一:
  岳麓区与湖南湘江新区（含长沙高新区）实行"区政合一"合一领导体制，区委书记由湘江新区党工委书记兼任，
  区长由湘江新区管委会主任兼任。故本调查的核心领导职务以"湘江新区(长沙高新区)党工委/管委会 + 岳麓区委/区人民政府"
  双重身份形式记录。

Research sources:
  - www.yuelu.gov.cn — 岳麓区人民政府门户网站"领导之窗 / 领导信息"（官方一手，primary）
  - 湘江新区/岳麓区政府"领导信息"栏目最新更新（2024-11 至 2026-03 profile 更新日期）
  - 湘江新区党工委（扩大）会议暨岳麓区第七次党代会报道（2026-08-03，官方）确认周健仍任党工委书记/岳麓区委书记
  - 湘江新区"领导讲话"栏目（2025-09 至 2026-04）出现 谭勇、何朝晖 讲话记录（旧领导线索）

Confirmed current leadership (官方领导信息，as of 2026-08):
  - 周健: 长沙市委副书记、湖南湘江新区(长沙高新区)党工委书记、岳麓区委书记（目标1）
  - 邹特: 湖南湘江新区(长沙高新区)党工委副书记、管委会主任、岳麓区委副书记、区长（目标2）
  - 张毅: 党工委副书记、管委会副主任、岳麓区委副书记、常务副区长
  - 钱胜: 党工委委员、纪检监察工委书记（纪委书记）
  - 师军: 党工委委员、组织工作部部长、岳麓区委常委、组织部部长
  - 谭海: 党工委委员、党政综合部部长、岳麓区委常委、区委办公室主任、区政府办公室主任
  - 帅军: 党工委委员、管委会副主任、岳麓区委常委
  - 任明: 党工委委员、管委会副主任、岳麓区人民政府副区长
  - 王玮: 党工委委员、管委会副主任
  - 王先民: 党工委委员、管委会副主任
  - 邹刚: 党工委委员、管委会副主任
  - 彭利芝: 党工委委员、岳麓区人大常委会主任
  - 杨杨成: 党工委委员、岳麓区政协主席

Confidence notes:
  - All current leadership names + 分工 confirmed from 官方政府门户网站"领导信息"栏目 (high reliability)
  - Full career resumes (履历) for 周健/邹特 and most deputies are NOT published on the profile pages;
    biographies for most leaders remain 开gap (open questions)
  - Previous 党工委书记/区委书记 (谭勇) and previous 管委会主任线索 (何朝晖) appear in 2025 领导讲话 records
    but are NOT in the 2026 current roster — flagged as unverified predecessor leads
  - Birth dates, native places not available from official pages — encoded as open questions
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "岳麓区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_岳麓区"
if _CURRENT_DIR.name == "hunan_岳麓区":
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
# IDs: 1-2 核心党政正职；3-11 区委常委/管委会/政府班子；12-13 人大主任、政协主席
persons = [
    # ══ 目标1：区委书记 ══
    {
        "id": 1,
        "name": "周健",
        "gender": "男",
        "ethnicity": "",        # open question
        "birth": "",           # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共长沙市岳麓区委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202305/t20230529_11115143.html",
        "confidence": "confirmed",
        "notes": "长沙市委副书记、湖南湘江新区(长沙高新区)党工委书记、岳麓区委书记。2026-07 区第七次党代会代表党工委(第六届岳麓区委)作报告。区政合一体制下为岳麓区委一把手。完整履历待核。",
    },
    # ═══ 目标2：区长 ═══
    {
        "id": 2,
        "name": "邹特",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "长沙岳麓区人民政府",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/201912/t20191217_5156374.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委副书记、管委会主任，岳麓区委副书记、区长，主持管委会与区人民政府全面工作，分管新区财政金融局、新区审计局。完整履历待核。",
    },
    # ═══ 常务副区长 / 区委副书记 ═══
    {
        "id": 3,
        "name": "张毅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "长沙岳麓区人民政府",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654221.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委副书记、管委会副主任，岳麓区委副书记、区政府党组副书记、常务副区长。协助党工委书记抓党建，负责发改、财政、国资、应急等，分管新区经济发展局、应急管理局、多支国资集团。",
    },
    # ═══ 纪委书记（纪检监察工委书记）═══
    {
        "id": 4,
        "name": "钱胜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "纪委书记",
        "current_org": "中共长沙岳麓区纪律检查委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202305/t20230529_11115178.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、纪检监察工委书记（即岳麓区纪委书记），负责纪检监察工委全面工作及巡察工作，分管新区纪检监察工委机关。",
    },
    # ═══ 县委组织部部长 ═══
    {
        "id": 5,
        "name": "师军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委组织部部长",
        "current_org": "中共长沙岳麓区委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202305/t20230529_11115294.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、组织工作部部长，岳麓区委常委、组织部部长。负责组织、机构编制、党校、联系教育。",
    },
    # ═══ 党政办主任（区委秘书长角色）═══
    {
        "id": 6,
        "name": "谭海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委办公室主任",
        "current_org": "中共长沙岳麓区委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654235.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、党政综合部部长，岳麓区委常委、区委办公室主任、区政府办公室主任。负责党政综合、机关事务、国安办、机关党委。",
    },
    # ═══ 管委会副主任 / 区委常委 ═══
    {
        "id": 7,
        "name": "帅军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "湖南湘江新区管理委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654235.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、管委会副主任、岳麓区委常委。负责商务、市场监管、知识产权，分管商务和市场监管局、长沙信息产业片区管理办公室、岳麓高新区管委会。",
    },
    {
        "id": 8,
        "name": "任明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "湖南湘江新区管理委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654225.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、管委会副主任，岳麓区人民政府副区长。负责自然资源、林业、开发建设和交通运输，分管自然资源和规划局、开发建设局(交通运输局)、土地储备中心、岳麓山风景名胜区管理局。",
    },
    {
        "id": 9,
        "name": "王玮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "湖南湘江新区管理委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654227.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、管委会副主任。负责政务服务、数据资源、金融，分管行政审批服务局、政务服务中心、湘江新区国有资本投资有限公司。",
    },
    {
        "id": 10,
        "name": "王先民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "湖南湘江新区管理委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202411/t20241114_11654229.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、管委会副主任。负责科技、工业和信息化、通信，分管科技创新和产业促进局、湘江科学城(岳麓山大学科技城)管委会、湘江智能科技创新中心。",
    },
    {
        "id": 11,
        "name": "邹刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "管委会副主任",
        "current_org": "湖南湘江新区管理委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/202603/t20260327_12347146.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、管委会副主任(2026-03更新)。负责农业农村、生态环境、民政、人社、医保、退役、信访、维稳，新区信访工作联席会议第一召集人。",
    },
    # ═══ 人大主任 / 政协主席 ═══
    {
        "id": 12,
        "name": "彭利芝",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "长沙岳麓区人民代表大会常务委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldxx/202411/t20241114_11654231.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、岳麓区人大常委会主任。主持人大常委会工作。",
    },
    {
        "id": 13,
        "name": "杨利成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议岳麓区委员会",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/ldxx/202411/t20241114_11654233.html",
        "confidence": "confirmed",
        "notes": "湖南湘江新区(长沙高新区)党工委委员、岳麓区政协主席。主持政协工作。",
    },
    # ═══ 前任/前任线索（plausible，2025 领导讲话）═══
    {
        "id": 20,
        "name": "谭勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任领导班子成员（线索）",
        "current_org": "湖南湘江新区",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/zldzc/lddtxw/（领导讲话栏目 2025-09 谭勇讲话记录）",
        "confidence": "unverified",
        "notes": "2025-09 至 2025-11 在湘江新区'领导讲话'栏目有讲话/调研记录（含召开党工委会议）。不在2026-08现职领导信息栏目中，疑为前任党工委/管委会领导，具体职务与接替关系待核实。",
    },
    {
        "id": 21,
        "name": "何朝晖",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任/调任领导（线索）",
        "current_org": "湖南湘江新区",
        "source": "http://www.yuelu.gov.cn/yl_xxgk/zldzc/lddtxw/（领导讲话栏目 2025-09/10 何朝晖讲话记录）",
        "confidence": "unverified",
        "notes": "2025-09 至 2025-10 在湘江新区'领导讲话'记录（招商引资调度、湘江科学城督导）。据娄底资料曾任娄底市领导；可能为前任管委会主任或调任至湘江新区，待核实。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长沙市岳麓区委员会", "type": "党委", "level": "县处级", "parent": "中共长沙市委", "location": "长沙市岳麓区"},
    {"id": 2, "name": "长沙市岳麓区人民政府", "type": "政府", "level": "县处级", "parent": "长沙市人民政府", "location": "长沙市岳麓区"},
    {"id": 3, "name": "湖南湘江新区（长沙高新区）党工委", "type": "党委", "level": "省级派出一级管理", "parent": "中共湖南省委", "location": "长沙市"},
    {"id": 4, "name": "湖南湘江新区（长沙高新区）管理委员会", "type": "政府", "level": "省级派出机构", "parent": "湖南省人民政府", "location": "长沙市"},
    {"id": 5, "name": "中共长沙市岳麓区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共长沙市纪委", "location": "长沙市岳麓区"},
    {"id": 6, "name": "长沙市岳麓区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "长沙市人大常委", "location": "长沙市岳麓区"},
    {"id": 7, "name": "中国人民政治协商会议长沙市岳麓区委员会", "type": "政协", "level": "县处级", "parent": "政协长沙市委", "location": "长沙市岳麓区"},
    {"id": 8, "name": "新区组织工作部", "type": "事业单位", "level": "厅级处室", "parent": "湘江新区党工委", "location": "长沙市"},
    {"id": 9, "name": "新区党政综合部", "type": "事业单位", "level": "厅级处室", "parent": "湘江新区党工委", "location": "长沙市"},
    {"id": 10, "name": "新区经济发展局", "type": "事业单位", "level": "厅级处室", "parent": "湘江新区管委会", "location": "长沙市"},
    {"id": 11, "name": "新区财政金融局", "type": "事业单位", "level": "厅级处室", "parent": "湘江新区管委会", "location": "长沙市"},
    {"id": 12, "name": "新区审计局", "type": "事业单位", "level": "厅级处室", "parent": "湘江新区管委会", "location": "长沙市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 周健 —— 区委书记 / 党工委书记
    {"person_id": 1, "org_id": 1, "title": "岳麓区委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "区政合一——岳麓区委书记由湘江新区党工委书记兼任"},
    {"person_id": 1, "org_id": 3, "title": "湖南湘江新区(长沙高新区)党工委书记", "start_date": "2023年前", "end_date": "present", "rank": "副部级辖区书记/正厅级", "note": "兼任长沙市委副书记，主持全面工作"},
    # 邹特 —— 区长 / 管委会主任
    {"person_id": 2, "org_id": 2, "title": "岳麓区区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "主持区政府全面工作，分管财政金融、审计"},
    {"person_id": 2, "org_id": 1, "title": "岳麓区委副书记", "start_date": "", "end_date": "present", "rank": "", "note": "党政正职搭档"},
    {"person_id": 2, "org_id": 4, "title": "湘江新区管委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "主持新区管委会全面工作，分管新区财政金融局、新区审计局"},
    # 张毅 —— 常务副区长 / 副书记
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "岳麓区委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分管经济发展局、应急管理局、发展集团等"},
    # 钱胜 —— 纪委书记
    {"person_id": 4, "org_id": 5, "title": "岳麓区纪委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼湘江新区纪检监察工委书记"},
    {"person_id": 4, "org_id": 3, "title": "湘江新区纪检监察工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责巡察、纪检监察"},
    # 师军 —— 组织部部长
    {"person_id": 5, "org_id": 8, "title": "新区组织工作部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "党工委委员"},
    {"person_id": 5, "org_id": 1, "title": "岳麓区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 谭海 —— 党政综合部部长
    {"person_id": 6, "org_id": 9, "title": "新区党政综合部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "党工委委员"},
    {"person_id": 6, "org_id": 1, "title": "岳麓区委常委、办公室主任、政府办公室主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 帅军 —— 管委会副主任 / 区委常委
    {"person_id": 7, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责商务、市场监管、知识产权"},
    {"person_id": 7, "org_id": 1, "title": "岳麓区委常委", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 任明 —— 管委会副主任 / 副区长
    {"person_id": 8, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责自然资源、开发建设、交通"},
    {"person_id": 8, "org_id": 2, "title": "岳麓区副区长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 王玮
    {"person_id": 9, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责政务服务、数据、金融"},
    # 王先民
    {"person_id": 10, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责科技、工业、通信"},
    # 邹刚
    {"person_id": 11, "org_id": 4, "title": "湘江新区管委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责农业农村、生态环境、民政、信访"},
    # 彭利芝 —— 人大主任
    {"person_id": 12, "org_id": 6, "title": "岳麓区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "湘江新区党工委委员(兼职)", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 杨利成 —— 政协主席
    {"person_id": 13, "org_id": 7, "title": "岳麓区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "湘江新区党工委委员(兼职)", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 前任领导线索
    {"person_id": 20, "org_id": 3, "title": "党工委领导(线索)", "start_date": "", "end_date": "2025", "rank": "", "note": "2025年召开党工委会议记录，已不在现任名单"},
    {"person_id": 21, "org_id": 4, "title": "管委会领导(线索)", "start_date": "", "end_date": "2025", "rank": "", "note": "2025年招商引资/湘江科学城记录，身份待核实"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档",
     "context": "周健（区委书记/党工委书记）与邹特（区长/管委会主任）组成岳麓区党政正职搭档（区政合一副厅级领导体制）",
     "overlap_org": "岳麓区委、区政府", "overlap_period": "至今"},
    # 书记—副书记/常务
    {"person_a": 1, "person_b": 3, "type": "上级-下级",
     "context": "周健（党工委书记）与张毅（党工委副书记、常务副区长）",
     "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "工作搭档",
     "context": "邹特（区长/管委会主任）与张毅（常务副区长/管委会副主任）",
     "overlap_org": "岳麓区政府、湘江新区管委会", "overlap_period": "至今"},
    # 区长 — 各副区长/管委会副主任
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长(任明)", "overlap_org": "岳麓区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—管委会副主任(王玮)", "overlap_org": "湘江新区管委会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—管委会副主任(王先民)", "overlap_org": "湘江新区管委会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—管委会副主任(邹刚)", "overlap_org": "湘江新区管委会", "overlap_period": "至今"},
    # 书记 — 各党工委委员/常委
    {"person_a": 1, "person_b": 4, "type": "上级-下级", "context": "党工委书记—纪检监察工委书记(钱胜)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上级-下级", "context": "党工委书记—组织工作部部长(师军)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上级-下级", "context": "党工委书记—党政综合部部长(谭海)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上级-下级", "context": "党工委书记—管委会副主任/区委常委(帅军)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    # 人大主任 / 政协主席
    {"person_a": 1, "person_b": 12, "type": "同工委领导班子", "context": "党工委书记—人大主任(彭利芝, 同为党工委委员)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "同工委领导班子", "context": "党工委书记—政协主席(杨利成, 同为党工委委员)", "overlap_org": "湘江新区党工委", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "选举/履职关系", "context": "区长由区人大选举并对其负责，彭利芝为人大常委会主任", "overlap_org": "岳麓区人大", "overlap_period": "至今"},
    # 前任领导线索（unverified 为主）
    {"person_a": 20, "person_b": 1, "type": "前任线索", "context": "谭勇2025年在党工委会议/领导讲话栏目有记录，推测曾任党工委主要领导，接替关系待核", "overlap_org": "湘江新区党工委", "overlap_period": "2025"},
    {"person_a": 21, "person_b": 2, "type": "前任线索", "context": "何朝晖2025年在管委会(招商引资、湘江科学城)讲话，推测曾任/调任管委会领导，与邹特关系待核", "overlap_org": "湘江新区管委会", "overlap_period": "2025"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _make_person_id(name: str) -> str:
    return f"yuelu_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] != "前任线索" else "weak",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "岳麓区人民政府门户网站 — 领导信息",
            "url": "http://www.yuelu.gov.cn/yl_xxgk/ldzc/ldxx/",
            "publisher": "岳麓区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "湖南湘江新区(长沙高新区)管理委员会 长沙市岳麓区人民政府领导之窗——领导信息栏目",
        },
        {
            "id": "S002",
            "title": "岳麓区领导之窗——领导讲话栏目",
            "url": "http://www.yuelu.gov.cn/yl_xxgk/zldzc/lddtxw/",
            "publisher": "岳麓区人民政府门户",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "medium",
            "notes": "2025-2026年领导讲话记录，含前任领导线索(谭勇、何朝晖)",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "长沙市",
            "region": "岳麓区",
            "job": person.get("current_post", ""),
            "task_id": "hunan_岳麓区",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": _make_person_id(name),
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副厅级及以上(区政合一)" if pid in (1, 2) else "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": _fr(person),
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "截至集中检索（2026-08-06），未见公开的纪律处分、审计问题或负面报道信号。",
            "date": AS_OF,
            "confidence": "plausible",
            "source_ids": ["S001"],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "partial",   # 官方确认职务，但出生等身份信息缺失
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早期任职履历与出生/籍贯/教育细节",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的精确起止时间）",
                "why_it_matters": "关系网络分析需要在时间线上确认任职交集",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 湘江新区 任命"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的出生年月、籍贯与教育背景",
                "why_it_matters": "核心身份信息，用于去重与跨区域关联分析",
                "suggested_queries": [f"{name} 籍贯", f"{name} 出生"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖南省-长沙市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


def _fr(person: dict) -> list:
    """Build governance_record from confirmed 分工 (portfolio) evidence."""
    pid = person["id"]
    domains = {
        1: [("经济发展", "主持岳麓区/湘江新区全面工作", "confirmed", "S001"),
            ("体制改革", "落实区政合一副领导体制，推动湘江新区与岳麓区一体化", "confirmed", "S001")],
        2: [("经济发展", "主持管委会与区政府全面工作，分管财政、审计(绩效考核、财政廉政)", "confirmed", "S001")],
        3: [("经济发展", "分管发改、统计、税务、国资、应急、电力、湘江科学城指挥部", "confirmed", "S001")],
        4: [("纪律检查", "负责纪检监察、巡察工作", "confirmed", "S001")],
        5: [("组织建设", "负责组织、机构编制、党校、联系教育工作", "confirmed", "S001")],
        6: [("综合协调", "负责党政综合协调、机关事务管理", "confirmed", "S001")],
        11: [("民生社利", "分管农业农村、民政、人社、医保、退役军人、信访维稳", "confirmed", "S001")],
    }.get(pid, [])
    return [{
        "period": "2026",
        "domain": d,
        "achievement_or_event": desc,
        "role_in_event": "分管/主持",
        "measured_outcome": "",
        "location": "长沙岳麓区",
        "confidence": conf,
        "source_ids": ids,
    } for d, desc, conf, ids in domains]


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    # 核心人物：区委书记/区长 + 常务副区长 + 前领袖+现有领导2位
    core_ids = {1, 2, 3, 4, 5}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  符合人 JSON 写入目录: {PJSON_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())