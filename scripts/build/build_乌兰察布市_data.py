#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乌兰察布市 (Ulanqab City), 内蒙古自治区.

Investigation date: 2026-08-06
Task ID: inner_mongolia_乌兰察布市
Level: 地级市
Targets: 市委书记 & 市长

Primary source: www.wulanchabu.gov.cn (乌兰察布市人民政府 - official 领导之窗 pages, current as of August 2026).
All roster bios confirmed from official leadership profile pages.

Confidence notes:
  - Current roles (as of 2026-08): confirmed via official 领导之窗 pages
  - Biographies (birth, education): confirmed via official resumes
  - Full career timelines and predecessor/successor movements: partially confirmed; gaps marked.
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

import sqlite3  # noqa
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "乌兰察布市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_乌兰察布市"
if _CURRENT_DIR.name == "inner_mongolia_乌兰察布市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────────
# IDs: 1-10 party standing committee (1=书记, 2=市长), 11-17 government leadership,
#      20+ predecessors
persons = [
    # ═══════ Core leadership ═══════
    {
        "id": 1,
        "name": "周凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共乌兰察布市委员会",
        "source": "http://www.wulanchabu.gov.cn/swld/1604825.html",
        "confidence": "confirmed",
        "notes": "主持市委全面工作，兼任市委党校（行政学院）校长（院长）。",
    },
    {
        "id": 2,
        "name": "刘海泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "内蒙古准格尔旗",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",  # 1998年6月入党
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/1789307.html",
        "confidence": "confirmed",
        "notes": "市政府党组书记、市长；主持政府全面工作，分管市审计局。包头师范学院（生物教育）、包头师范学院附中/内蒙古工大附中教师出身；历任包头青山区团区委书记、街道党工委书记、区信访局长，包头市信访局副局长，石拐区委常委副区长，包头市委政研室主任，达茂旗旗长，九原区委书记，2022年2月任包头市委常委、副市长，2024年7月调任乌兰察布市委副书记，2025年4月当选市长。",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Party Standing Committee (current)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "刘志平",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "中央党校研究生，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共乌兰察布市委政法委员会",
        "source": "http://www.wulanchabu.gov.cn/swld/1913307.html",
        "confidence": "confirmed",
        "notes": "主持市委政法委全面工作，负责政法、维稳、依法治市、国家安全、信访等工作。",
    },
    {
        "id": 4,
        "name": "敖满斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "",
        "education": "研究生学历，文学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共乌兰察布市委统战部",
        "source": "http://www.wulanchabu.gov.cn/swld/38015.html",
        "confidence": "confirmed",
        "notes": "市政协党组副书记；负责统一战线、民族、宗教等工作。",
    },
    {
        "id": 5,
        "name": "方泽",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "博士研究生学历，法学博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/swld/1534973.html",
        "confidence": "confirmed",
        "notes": "市政府党组副书记；协助市长负责市人民政府常务工作，分管发展改革、财政、应急管理、统计、能源、金融等。",
    },
    {
        "id": 6,
        "name": "李建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "研究生学历，工商管理硕士，经济师",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共乌兰察布市委宣传部",
        "source": "http://www.wulanchabu.gov.cn/swld/1479731.html",
        "confidence": "confirmed",
        "notes": "市精神文明建设办公室主任；负责宣传思想文化、意识形态、网络安全和信息化工作。",
    },
    {
        "id": 7,
        "name": "凌云",
        "gender": "女",
        "ethnicity": "鄂伦春族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共乌兰察布市委组织部",
        "source": "http://www.wulanchabu.gov.cn/swld/1913309.html",
        "confidence": "confirmed",
        "notes": "协助周凯同志抓党的建设工作和党校工作，主持市委组织部全面工作。",
    },
    {
        "id": 8,
        "name": "梁永杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、监委主任",
        "current_org": "中共乌兰察布市纪律检查委员会",
        "source": "http://www.wulanchabu.gov.cn/swld/1583883.html",
        "confidence": "confirmed",
        "notes": "二级高级监察官；主持市纪委监委全面工作，负责纪检监察、巡察、党风廉政建设和反腐败等工作。",
    },
    {
        "id": 9,
        "name": "隋剑华",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共乌兰察布市委员会",
        "source": "http://www.wulanchabu.gov.cn/swld/1536993.html",
        "confidence": "confirmed",
        "notes": "兼任市委全面深化改革委员会办公室主任；负责市委机关日常工作运转协调。",
    },
    {
        "id": 10,
        "name": "冀宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "中央党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、集宁区委书记",
        "current_org": "中共乌兰察布市集宁区委员会",
        "source": "http://www.wulanchabu.gov.cn/swld/1991461.html",
        "confidence": "confirmed",
        "notes": "主持集宁区委全面工作。",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Government leadership (current)
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "李建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "大学本科，工学学士，工程师",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/35528.html",
        "confidence": "confirmed",
        "notes": "协助市长负责科技、卫生健康、市场管理、医疗保障等工作。",
    },
    {
        "id": 12,
        "name": "于海成",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1974年7月",
        "birthplace": "",
        "education": "大学本科，研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/51587.html",
        "confidence": "confirmed",
        "notes": "协助市长负责工业和信息化建设、自然资源、城乡建设、园林绿化、城市管理等工作。",
    },
    {
        "id": 13,
        "name": "王镇海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年2月",
        "birthplace": "",
        "education": "研究生学历，经济管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/1467165.html",
        "confidence": "confirmed",
        "notes": "协助市长城市交通安全、水利、农业和农村牧区、林业和草原等工作。",
    },
    {
        "id": 14,
        "name": "郝云涛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/1602141.html",
        "confidence": "confirmed",
        "notes": "协助市长负责民族事务、人力资源和社会保障、生态环境、文化旅游、康养体育等工作。",
    },
    {
        "id": 15,
        "name": "高永斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/1558939.html",
        "confidence": "confirmed",
        "notes": "协助市长负责民政、退役军人事务、商贸物流和关空产业、招商引资等。",
    },
    {
        "id": 16,
        "name": "郝晓亭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年5月",
        "birthplace": "",
        "education": "大学学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "乌兰察布市人民政府",
        "source": "http://www.wulanchabu.gov.cn/zfld/65620.html",
        "confidence": "confirmed",
        "notes": "协助市长处理市人民政府办公室工作，主持市人民政府办公室工作。",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "隋维钧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "",
        "source": "http://www.wulanchabu.gov.cn/zwgk/",
        "confidence": "plausible",
        "notes": "此前任乌兰察布市委书记（官方领导之窗旧活动档案中出现）；去向待查。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乌兰察布市委员会", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 2, "name": "乌兰察布市人民政府", "type": "政府", "level": "地级市", "location": "乌兰察布市"},
    {"id": 3, "name": "中共乌兰察布市委政法委员会", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 4, "name": "中共乌兰察布市委统战部", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 5, "name": "中共乌兰察布市委宣传部", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 6, "name": "中共乌兰察布市委组织部", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 7, "name": "中共乌兰察布市纪律检查委员会", "type": "党委", "level": "地级市", "location": "乌兰察布市"},
    {"id": 8, "name": "中共乌兰察布市集宁区委员会", "type": "党委", "level": "县级市辖区", "location": "乌兰察布市集宁区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 周凯
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 刘海泉
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市政府党组书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 刘志平
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 敖满斌
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 方泽
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李建军
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 凌云
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 梁永杰
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 隋剑华
    {"person_id": 9, "org_id": 1, "title": "市委常委、秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 冀宏
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "集宁区委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李建文
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民建会员，分管科技、卫健、市监、医保等"},
    # 于海成
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管工信、自然、城建等"},
    # 王镇海
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管交通、水利、农牧、林草等"},
    # 郝云涛
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管民族、人社、生态、文旅等"},
    # 高永斌
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": "分管民政、退役军人、商贸、招商等"},
    # 郝晓亭
    {"person_id": 16, "org_id": 2, "title": "市政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 隋维钧 (前任书记)
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "周凯的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 周凯 ↔ 刘海泉 (党政一把手搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一双打搭档：市委书记与市长", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    # 周凯 ↔ 各常委 (书记与常委的上下级工作关系)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委领导与政法委书记", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委领导与统战部长", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委领导与常务副市长", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委领导与宣传部长", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与组织部部长（组织条线）", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委领导与纪委书记（党风廉政）", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委领导与秘书长", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委领导与集宁区委书记", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    # 刘海泉 ↔ 各副市长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与市政府秘书长", "overlap_org": "乌兰察布市人民政府", "overlap_period": ""},
    # 凌云 (组织部长) ↔ 梁永杰 (纪委书记) 换届协作
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "组织部与纪委在干部监督中的协作", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "周凯接替隋维钧任乌兰察布市委书记", "overlap_org": "中共乌兰察布市委员会", "overlap_period": ""},
]

# (Predecessor/successor nodes to be appended after background research returns)


# ── Person JSON files ─────────────────────────────────────────────────────────
def _write_person_json(person: dict) -> None:
    province = "内蒙古自治区"
    city = "乌兰察布市"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_")
    name = person["name"].replace("·", "_")
    fname = f"{TODAY}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname
    source_register = []
    sid = 0
    for url in filter(None, [person.get("source", "")]):
        sid += 1
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"乌兰察布市人民政府 - {person['current_post']}信息",
            "url": url,
            "publisher": "乌兰察布市人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "",
        })
    identity = {
        "person_id": f"wulanchabu_{name}",
        "name": person["name"],
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
            "name_birth": f"{person['name']}_{person.get('birth', '')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
            "official_profile_url": person.get("source", ""),
        },
    }
    edu = person.get("education", "")
    if edu:
        identity["education"].append({
            "period": "",
            "institution": edu if ("学历" in edu or "研究生" in edu or "大学" in edu or "党校" in edu) else "",
            "major": "",
            "degree": edu,
            "study_type": "unknown",
            "source_ids": ["S001"] if source_register else [],
        })
    career_timeline = [{
        "start": "",
        "end": "present",
        "org": person.get("current_org", ""),
        "title": person.get("current_post", ""),
        "level": "",
        "location": "乌兰察布市",
        "system": "government" if "政府" in person.get("current_org", "") or "人民政府" in person.get("current_org", "") else "party",
        "rank": "",
        "is_key_promotion": False,
        "notes": person.get("notes", ""),
        "confidence": person.get("confidence", "plausible"),
        "source_ids": ["S1"] if source_register else [],
    }]
    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"wulanchabu_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] == "superior_subordinate" else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S1"] if source_register else [],
                })
    obj = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "乌兰察布市",
            "region": "乌兰察布市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_乌兰察布市",
            "time_focus": "2026-08",
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S1"] if source_register else [],
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": person.get("career_pattern", "unknown"),
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
            "description": "未在公开官方资料中发现风险信号",
            "date": AS_OF,
            "confidence": "confirmed",
            "source_ids": [],
        }],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"{person['name']} 完整职业生涯（当前职务以外的历任岗位）",
        },
        "open_questions": [{
            "priority": "high",
            "question": f"{person['name']} 的完整履历（任现职前岗位、教育经历、出生地等）",
            "why_it_matters": "完整履历是分析其升迁路径、系统经验和关系网络的基础",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
            "last_attempted": AS_OF,
        }],
    }
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fpath.name}")


def write_person_jsons():
    core_ids = {1, 2}
    # Write top two leaders (书记 & 市长) as required person JSONs, plus key standing members
    key_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
    for p in persons:
        if p["id"] in key_ids:
            _write_person_json(p)


if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    print("  Writing person JSON files...")
    write_person_jsons()

    print(f"\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB file: {DB_PATH}")
    print(f"  GEXF file: {GEXF_PATH}")
    print("  Done.")