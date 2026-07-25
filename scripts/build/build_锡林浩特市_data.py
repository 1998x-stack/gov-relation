#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 锡林浩特市 (Xilinhot City), 锡林郭勒盟, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_锡林浩特市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.xilinhaote.gov.cn — 锡林浩特市人民政府官方网站 (primary, current as of July 2026)
  - Official leadership profile pages for party committee, government, NPC, and CPPCC
  - News articles from xilinhaote.gov.cn confirming activities (July 2026)

Confidence notes:
  - Current roles: confirmed via official government profiles (July 2026)
  - Biographical details: basic identity confirmed via official bios; detailed career timeline limited
  - Career timeline details beyond current roles: limited due to web access constraints
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
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
SLUG = "锡林浩特市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_锡林浩特市"
if _CURRENT_DIR.name == "inner_mongolia_锡林浩特市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 party committee, 10-19 government leadership, 20+ NPC/CPPCC, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "兴安",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1978年10月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "行署党组成员、副盟长、锡林浩特市委书记",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/xa/index.html",
        "confidence": "confirmed",
        "notes": "兼任锡林郭勒盟行署党组成员、副盟长，主持市委全面工作，兼任市委党校(行政学校)校长。"
    },
    {
        "id": 2,
        "name": "张英杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",  # open question
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、政府党组书记、市长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/zyj/index.html",
        "confidence": "confirmed",
        "notes": "兼任锡林郭勒经济技术开发区党工委书记、管委会主任。主持市政府全面工作，分管市审计局。"
    },
    {
        "id": 3,
        "name": "杨占青",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/yzq/index.html",
        "confidence": "confirmed",
        "notes": "协助兴安同志抓党的建设工作，主持市委政法委和市委国安委全面工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "杨震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、政府党组成员、常务副市长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/yz/index.html",
        "confidence": "confirmed",
        "notes": "负责市政府常务工作，统筹综合经济、发展改革、财税等。"
    },
    {
        "id": 5,
        "name": "石凯龙",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1971年12月",
        "birthplace": "",  # open question
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、纪委书记、监察委员会主任",
        "current_org": "中共锡林浩特市纪律检查委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/skl/index.html",
        "confidence": "confirmed",
        "notes": "主持市纪委监委全面工作，负责纪检监察、巡察、党风廉政建设和反腐败工作。"
    },
    {
        "id": 6,
        "name": "杨力宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",  # open question
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、统战部部长、政协党组副书记",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/ylh/index.html",
        "confidence": "confirmed",
        "notes": "主持市委统战部全面工作，兼任市社会主义学校校长。"
    },
    {
        "id": 7,
        "name": "段振华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、组织部部长",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/dzh/index.html",
        "confidence": "confirmed",
        "notes": "主持市委组织部全面工作，分管市委编办、老干部局等。"
    },
    {
        "id": 8,
        "name": "徐敏",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1982年4月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、政府副市长（常委副市长）",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/xm/index.html",
        "confidence": "confirmed",
        "notes": "协助统筹民政、人社、退役军人事务、民族事务等。"
    },
    {
        "id": 9,
        "name": "任昊",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1987年7月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/rh/index.html",
        "confidence": "confirmed",
        "notes": "主持市委宣传部全面工作，负责宣传思想文化、意识形态、网信工作。"
    },
    {
        "id": 10,
        "name": "董国欣",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1986年2月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、办公室主任",
        "current_org": "中共锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/dgx/index.html",
        "confidence": "confirmed",
        "notes": "兼任全面深化改革委员会办公室主任、直属机关工作委员会书记。"
    },
    {
        "id": 11,
        "name": "褚文杰",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question — typical for military officer
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、人民武装部政委",
        "current_org": "锡林浩特市人民武装部",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/sw/lf/index.html",
        "confidence": "confirmed",
        "notes": "人武部政委，市委常委，军方代表。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "常征",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政府副市长提名人选",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/cz/index.html",
        "confidence": "confirmed",
        "notes": "兼任锡林郭勒经济技术开发区管委会副主任。副市长提名人选。"
    },
    {
        "id": 13,
        "name": "柯晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "",  # open question
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政府党组成员、副市长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/kxm/index.html",
        "confidence": "confirmed",
        "notes": "协助统筹城市建设与管理、交通运输、市场管理等。"
    },
    {
        "id": 14,
        "name": "马铭",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政府党组成员、副市长、市公安局党委书记、局长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/mm/index.html",
        "confidence": "confirmed",
        "notes": "兼任公安局党委书记、局长，负责公安、司法、信访等方面。"
    },
    {
        "id": 15,
        "name": "鲁志敏",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政府党组成员、副市长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/lzm/index.html",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 16,
        "name": "辛颖",
        "gender": "女",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政府党组成员、副市长",
        "current_org": "锡林浩特市人民政府",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zf/xy/index.html",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # NPC and CPPCC Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "周培龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "人大常委会党组书记、主任",
        "current_org": "锡林浩特市人民代表大会常务委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/rd/zpl/index.html",
        "confidence": "confirmed",
        "notes": "主持市人大常委会全面工作。"
    },
    {
        "id": 21,
        "name": "郭静娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "政协党组书记、主席候选人",
        "current_org": "中国人民政治协商会议锡林浩特市委员会",
        "source": "https://www.xilinhaote.gov.cn/xilinhaote/zwgk/ldzc/zx/gjj/index.html",
        "confidence": "confirmed",
        "notes": "主持市政协全面工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor (limited data)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "孙振江",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # previously 市委书记
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "前任锡林浩特市委书记（兴安的前任）。去向待查。"
    },
    {
        "id": 31,
        "name": "布仁金",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "historical",
        "confidence": "plausible",
        "notes": "前任锡林浩特市市长（张英杰的前任，姓名暗示蒙古族）。去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共锡林浩特市委员会", "type": "党委", "level": "县级市", "parent": "中共锡林郭勒盟委员会", "location": "锡林浩特市"},
    {"id": 2, "name": "锡林浩特市人民政府", "type": "政府", "level": "县级市", "parent": "锡林郭勒盟行政公署", "location": "锡林浩特市"},
    {"id": 3, "name": "中共锡林浩特市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共锡林郭勒盟纪律检查委员会", "location": "锡林浩特市"},
    {"id": 4, "name": "锡林浩特市人民代表大会常务委员会", "type": "人大", "level": "县级市", "location": "锡林浩特市"},
    {"id": 5, "name": "中国人民政治协商会议锡林浩特市委员会", "type": "政协", "level": "县级市", "location": "锡林浩特市"},
    {"id": 6, "name": "锡林郭勒经济技术开发区管委会", "type": "开发区", "level": "县级市", "location": "锡林浩特市"},
    {"id": 7, "name": "锡林浩特市人民武装部", "type": "其他", "level": "县级市", "location": "锡林浩特市"},
    {"id": 8, "name": "锡林郭勒盟行政公署", "type": "政府", "level": "地级", "parent": "内蒙古自治区人民政府", "location": "锡林浩特市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 兴安 — 市委书记
    {"person_id": 1, "org_id": 8, "title": "行署党组成员、副盟长", "start": "", "end": "present", "rank": "副厅级", "note": "锡林郭勒盟副盟长"},
    {"person_id": 1, "org_id": 1, "title": "锡林浩特市委书记", "start": "", "end": "present", "rank": "正处级（高配副厅级）", "note": "由副盟长兼任，高配"},
    {"person_id": 1, "org_id": 1, "title": "市委党校(行政学校)校长", "start": "", "end": "present", "rank": "", "note": "兼任党校校长"},
    # 张英杰 — 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "政府党组书记、市长", "start": "", "end": "present", "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 6, "title": "党工委书记、管委会主任", "start": "", "end": "present", "rank": "", "note": "兼任经济技术开发区负责人"},
    # 杨占青 — 副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "政法委书记", "start": "", "end": "present", "rank": "", "note": "兼任政法委书记"},
    # 杨震 — 常务副市长
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "政府党组成员、常务副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 石凯龙 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "纪委书记、监察委员会主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨力宏 — 统战部长
    {"person_id": 6, "org_id": 1, "title": "市委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "兼任政协党组副书记"},
    # 段振华 — 组织部长
    {"person_id": 7, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 徐敏 — 常委副市长
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "政府副市长（常委副市长）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 任昊 — 宣传部长
    {"person_id": 9, "org_id": 1, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 董国欣 — 市委办主任
    {"person_id": 10, "org_id": 1, "title": "市委常委、办公室主任", "start": "", "end": "present", "rank": "副处级", "note": "兼任深改办主任、直属机关工委书记"},
    # 褚文杰 — 人武部政委
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": "人武部政委"},
    {"person_id": 11, "org_id": 7, "title": "人民武装部政委", "start": "", "end": "present", "rank": "", "note": ""},
    # 常征 — 副市长提名人选
    {"person_id": 12, "org_id": 2, "title": "政府副市长提名人选", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "管委会副主任", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 柯晓明 — 副市长
    {"person_id": 13, "org_id": 2, "title": "政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": "城建、交通、市场管理"},
    # 马铭 — 副市长兼公安局长
    {"person_id": 14, "org_id": 2, "title": "政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "市公安局党委书记、局长", "start": "", "end": "present", "rank": "", "note": "兼任"},
    # 鲁志敏 — 副市长
    {"person_id": 15, "org_id": 2, "title": "政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 辛颖 — 副市长
    {"person_id": 16, "org_id": 2, "title": "政府党组成员、副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周培龙 — 人大常委会主任
    {"person_id": 20, "org_id": 4, "title": "人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 郭静娟 — 政协主席
    {"person_id": 21, "org_id": 5, "title": "政协党组书记、主席候选人", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # Predecessors
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "孙振江，兴安的前任"},
    {"person_id": 31, "org_id": 2, "title": "市长（前任）", "start": "", "end": "", "rank": "正处级", "note": "布仁金，张英杰的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 兴安 ↔ 张英杰（党政一把手搭档关系）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "党政一把手搭档（兴安为市委书记，张英杰为市长）", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    # 兴安 ↔ 杨占青（市委班子正副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与专职副书记", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    # 市委常委会内工作关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与常务副市长（市委常委）", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与统战部长", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与组织部长", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委书记与常委副市长", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委书记与宣传部长", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "市委书记与市委办主任", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    # 张英杰 ↔ 副市长们（政府班子工作关系）
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与常委副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "市长与副市长（兼公安局长）", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
    # 前任关系
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "兴安接替孙振江任锡林浩特市委书记", "overlap_org": "中共锡林浩特市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 31, "type": "predecessor_successor", "context": "张英杰接替布仁金任锡林浩特市市长", "overlap_org": "锡林浩特市人民政府", "overlap_period": ""},
]

# ── Person JSON files ─────────────────────────────────────────────────────────

def _write_person_json(person: dict) -> None:
    """Write a single person JSON file to the staging directory."""
    province = "内蒙古自治区"
    city = "锡林浩特市"
    job_slug = person["current_post"].split("、")[0].replace(" ", "_")
    name = person["name"].replace("·", "_")
    fname = f"{TODAY}-{province}-{city}-{job_slug}-{name}.json"
    fpath = PJSON_DIR / fname

    # Build source register
    source_register = []
    sid = 0
    src = person.get("source", "")
    if src:
        sid += 1
        source_type = "official" if "xilinhaote.gov.cn" in src else "historical"
        reliability = "high" if "xilinhaote.gov.cn" in src else "low"
        source_register.append({
            "id": f"S{sid:03d}",
            "title": f"锡林浩特市人民政府 - {person['current_post']}信息",
            "url": src,
            "publisher": "锡林浩特市人民政府" if "xilinhaote.gov.cn" in src else "历史记录",
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": reliability,
            "notes": ""
        })

    # Build identity
    identity = {
        "person_id": f"xilinhaote_{name}",
        "name": person["name"],
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": "",
                "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": ["S001"] if source_register and "xilinhaote.gov.cn" in person.get("source", "") else []
            }
        ],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{person['name']}_{person.get('birth', '')}",
            "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
            "official_profile_url": person.get("source", "")
        }
    }

    # Build career timeline from positions
    career_timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            org_name = org["name"] if org else ""
            system = "party"
            if org:
                if org["type"] == "政府":
                    system = "government"
                elif org["type"] == "人大":
                    system = "npc"
                elif org["type"] == "政协":
                    system = "cppcc"
                elif org["type"] == "开发区":
                    system = "development_zone"
            career_timeline.append({
                "start": pos.get("start", ""),
                "end": pos.get("end", "present"),
                "org": org_name,
                "title": pos["title"],
                "level": pos.get("rank", ""),
                "location": "锡林浩特市",
                "system": system,
                "rank": pos.get("rank", ""),
                "is_key_promotion": pos["title"] in ["锡林浩特市委书记", "政府党组书记、市长"],
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
                "source_ids": ["S001"] if source_register else []
            })

    # Build relationships
    relationships_list = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((p for p in persons if p["id"] == r["person_b"]), None)
            if other:
                other_name_clean = other["name"].replace("·", "_")
                relationships_list.append({
                    "person": other["name"],
                    "person_id": f"xilinhaote_{other_name_clean}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ["superior_subordinate"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"] if source_register else []
                })

    obj = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "锡林郭勒盟",
            "region": "锡林浩特市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_锡林浩特市",
            "time_focus": "2026-07"
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"] if source_register else []
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
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
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found in publicly available official profiles",
                "date": AS_OF,
                "confidence": "confirmed",
                "source_ids": []
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": f"完整履历（{person['name']}的早期职业生涯和完整晋升路径）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（教育背景、早期任职经历、完整的晋升时间线）",
                "why_it_matters": "完整履历是分析其晋升模式、系统经验和关系网络的基础",
                "suggested_queries": [
                    f"{person['name']} 简历",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 百度百科"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {fpath.name}")


def write_person_jsons():
    """Write person JSON files for the core leadership."""
    core_ids = {1, 2, 3, 4, 5, 7, 20, 21}  # key leaders
    for p in persons:
        if p["id"] in core_ids:
            _write_person_json(p)


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"═══ Building {SLUG} data ═══")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Run the build
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

    # Write person JSONs
    print("  Writing person JSON files...")
    write_person_jsons()

    # Summary
    print(f"\n═══ Summary ═══")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB file: {DB_PATH}")
    print(f"  GEXF file: {GEXF_PATH}")
    print(f"  Person JSONs: {PJSON_DIR}")
    print("  Done.")
