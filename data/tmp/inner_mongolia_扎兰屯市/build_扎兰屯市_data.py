#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 扎兰屯市 (Zalantun City), 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_扎兰屯市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.zhalantun.gov.cn — 扎兰屯市人民政府官方网站 (primary, current as of July 2026)
  - 领导之窗 pages for all 市委/市人大/市政府/市政协 leaders
  - Multiple news articles confirming roles through July 2026

Confidence notes:
  - Current roles: confirmed via official leadership portal (as of 2026-07-25)
  - Biographical details confirmed via official government profile pages
  - Career timeline details beyond current roles: limited due to only short bios on leadership page
  - Party standing committee composition confirmed via meeting attendance
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
SLUG = "扎兰屯市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_扎兰屯市"
if _CURRENT_DIR.name == "inner_mongolia_扎兰屯市":
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
# IDs: 1-11 party standing committee, 12-19 government, 20-24人大, 25-29政协, 30+ predecessor

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee (市委)
    # ══════════════════════════════════════════════════════════════════════

    # 1 - 市委书记
    {
        "id": 1,
        "name": "迟君德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1063.html",
        "confidence": "confirmed",
        "notes": "主持市委全面工作；2026年7月到任（'真诚欢迎迟君德同志到扎兰屯市工作'--老同志语）"
    },
    # 2 - 市委副书记、市长
    {
        "id": 2,
        "name": "孟刚",
        "gender": "男",
        "ethnicity": "达斡尔族",
        "birth": "1983年1月",
        "birthplace": "",  # open question
        "education": "硕士学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/471.html",
        "confidence": "confirmed",
        "notes": "市委副书记、市政府党组书记、市长；主持市人民政府全面工作，负责审计等方面工作"
    },
    # 3 - 市委副书记、政法委书记
    {
        "id": 3,
        "name": "郑力军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "",  # open question
        "education": "大学学历，历史学学士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1049.html",
        "confidence": "confirmed",
        "notes": "协助市委书记抓党的建设和维护稳定工作"
    },
    # 4 - 市委常委、常务副市长
    {
        "id": 4,
        "name": "田旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、常务副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/973.html",
        "confidence": "confirmed",
        "notes": "市委常委、市政府党组副书记、常务副市长"
    },
    # 5 - 市委常委、副市长
    {
        "id": 5,
        "name": "郭平",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970年9月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1020.html",
        "confidence": "confirmed",
        "notes": "市委常委、市政府党组成员、副市长"
    },
    # 6 - 市委常委、宣传部部长
    {
        "id": 6,
        "name": "刘国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年4月",
        "birthplace": "",  # open question
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/457.html",
        "confidence": "confirmed",
    },
    # 7 - 市委常委、统战部部长
    {
        "id": 7,
        "name": "李东方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "",  # open question
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、统战部部长",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/459.html",
        "confidence": "confirmed",
        "notes": "市政协党组副书记，市社会主义学校校长"
    },
    # 8 - 市委常委、纪委书记
    {
        "id": 8,
        "name": "茹华安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年1月",
        "birthplace": "",  # open question
        "education": "大学学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共扎兰屯市纪律检查委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1038.html",
        "confidence": "confirmed",
        "notes": "2026年1月当选市监察委员会主任"
    },
    # 9 - 市委常委、组织部部长
    {
        "id": 9,
        "name": "李雁来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、组织部部长",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1018.html",
        "confidence": "confirmed",
    },
    # 10 - 市委常委、办公室主任
    {
        "id": 10,
        "name": "迟龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、办公室主任",
        "current_org": "中共扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/972.html",
        "confidence": "confirmed",
    },
    # 11 - 市委常委、人武部政委
    {
        "id": 11,
        "name": "王健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年6月",
        "birthplace": "",  # open question
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委常委、人武部上校政治委员",
        "current_org": "扎兰屯市人民武装部",
        "source": "https://www.zhalantun.gov.cn/Leader/show/114/1033.html",
        "confidence": "confirmed",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Government (市政府 - non-standing committee members)
    # ══════════════════════════════════════════════════════════════════════

    # 12 - 副市长、公安局长
    {
        "id": 12,
        "name": "卢文锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长、公安局局长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/116/958.html",
        "confidence": "confirmed",
        "notes": "二级高级警长"
    },
    # 13 - 副市长
    {
        "id": 13,
        "name": "卢亚光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/116/472.html",
        "confidence": "confirmed",
    },
    # 14 - 副市长
    {
        "id": 14,
        "name": "韩志立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/116/858.html",
        "confidence": "confirmed",
    },
    # 15 - 副市长
    {
        "id": 15,
        "name": "尹晓辉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",  # open question
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/116/901.html",
        "confidence": "confirmed",
    },
    # 16 - 副市长（无党派）
    {
        "id": 16,
        "name": "杨絮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "",  # open question
        "education": "大学学历，文学双学位",
        "party_join": "",
        "work_start": "",  # open question
        "current_post": "副市长",
        "current_org": "扎兰屯市人民政府",
        "source": "https://www.zhalantun.gov.cn/Leader/show/116/1055.html",
        "confidence": "confirmed",
        "notes": "无党派人士；此前任工信局、商务局局长"
    },

    # ══════════════════════════════════════════════════════════════════════
    # 人大领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 17,
        "name": "孙修非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "扎兰屯市人民代表大会常务委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/115/461.html",
        "confidence": "confirmed",
    },
    {
        "id": 18,
        "name": "宋辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "扎兰屯市人民代表大会常务委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/115/853.html",
        "confidence": "confirmed",
    },
    {
        "id": 19,
        "name": "张传福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "扎兰屯市人民代表大会常务委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/115/464.html",
        "confidence": "confirmed",
    },
    {
        "id": 20,
        "name": "陈辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "扎兰屯市人民代表大会常务委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/115/854.html",
        "confidence": "confirmed",
    },

    # ══════════════════════════════════════════════════════════════════════
    # 政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "张立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "中国人民政治协商会议扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/117/850.html",
        "confidence": "confirmed",
    },
    {
        "id": 22,
        "name": "鲁垚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/117/473.html",
        "confidence": "confirmed",
    },
    {
        "id": 23,
        "name": "房平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组成员、副主席",
        "current_org": "中国人民政治协商会议扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/117/859.html",
        "confidence": "confirmed",
    },
    {
        "id": 24,
        "name": "刘仁德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组成员、副主席",
        "current_org": "中国人民政治协商会议扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/117/479.html",
        "confidence": "confirmed",
    },
    {
        "id": 25,
        "name": "焦健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议扎兰屯市委员会",
        "source": "https://www.zhalantun.gov.cn/Leader/show/117/478.html",
        "confidence": "confirmed",
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessor (前任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "白志军",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # currently unknown/transitioning
        "current_org": "",
        "source": "https://www.zhalantun.gov.cn/News/show/1407029.html",
        "confidence": "confirmed",
        "notes": "前任扎兰屯市委书记（至2026年中）；2026年1月兼任呼伦贝尔市政协副主席；迟君德2026年7月已接任市委书记"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    # Party
    {"id": 1, "name": "中共扎兰屯市委员会", "type": "党委", "level": "县级", "location": "扎兰屯市"},
    {"id": 2, "name": "中共扎兰屯市纪律检查委员会", "type": "党委", "level": "县级", "location": "扎兰屯市"},

    # Government
    {"id": 3, "name": "扎兰屯市人民政府", "type": "政府", "level": "县级", "location": "扎兰屯市"},
    {"id": 4, "name": "扎兰屯市公安局", "type": "政府", "level": "县级", "location": "扎兰屯市"},
    {"id": 5, "name": "扎兰屯市人民武装部", "type": "政府", "level": "县级", "location": "扎兰屯市"},

    # People's Congress
    {"id": 6, "name": "扎兰屯市人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "扎兰屯市"},

    # CPPCC
    {"id": 7, "name": "中国人民政治协商会议扎兰屯市委员会", "type": "政协", "level": "县级", "location": "扎兰屯市"},

    # Higher-level org
    {"id": 8, "name": "中国人民政治协商会议呼伦贝尔市委员会", "type": "政协", "level": "地级", "location": "呼伦贝尔市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # Party committee members
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "市长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "常务副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 6, "org_id": 1, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "市政协党组副书记"},
    {"person_id": 8, "org_id": 1, "title": "市委常委、市纪委书记", "start": "2026-01", "end": "present", "rank": "副处级", "note": "2026年1月当选市监察委员会主任"},
    {"person_id": 9, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委、办公室主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "市委常委、人武部上校政治委员", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # Government (non-standing committee)
    {"person_id": 12, "org_id": 3, "title": "副市长、公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "公安局党委书记、局长，二级高级警长"},
    {"person_id": 13, "org_id": 3, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 14, "org_id": 3, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 15, "org_id": 3, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "市政府党组成员"},
    {"person_id": 16, "org_id": 3, "title": "副市长", "start": "", "end": "present", "rank": "副处级", "note": "无党派人士"},

    # 人大
    {"person_id": 17, "org_id": 6, "title": "市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 6, "title": "市人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 6, "title": "市人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 政协
    {"person_id": 21, "org_id": 7, "title": "市政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 7, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 7, "title": "市政协党组成员、副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 7, "title": "市政协党组成员、副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 7, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # Predecessor
    {"person_id": 30, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "2026-06", "rank": "正处级", "note": "同时任呼伦贝尔市政协副主席（2026-01）"},
    {"person_id": 30, "org_id": 8, "title": "呼伦贝尔市政协副主席", "start": "", "end": "", "rank": "副厅级", "note": "2026年1月以该身份参加政协会议"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    # Party secretary - Mayor: key leadership duo
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市长搭档", "overlap_org": "中共扎兰屯市委员会/扎兰屯市人民政府", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # Party secretary - Deputy party secretary
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记与副书记/政法委书记工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # Party secretary - Organization department head
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委书记与组织部部长工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # Party secretary - Office director
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委书记与市委办公室主任工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # Party secretary - Discipline secretary
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委书记与纪委书记工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "2026-07至今", "confidence": "confirmed"},

    # Mayor - Deputy mayors (government team)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "市长与常务副市长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长与副市长（市政府党组成员）工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "市长与公安局长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "市长与副市长工作关系", "overlap_org": "扎兰屯市人民政府", "overlap_period": "至今", "confidence": "confirmed"},

    # Predecessor-successor: 白志军 → 迟君德
    {"person_a": 30, "person_b": 1, "type": "predecessor_successor", "context": "前任市委书记白志军与现任市委书记迟君德交接", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "2026年交接", "confidence": "confirmed"},

    # Predecessor - other leaders who previously worked together
    {"person_a": 30, "person_b": 2, "type": "overlap", "context": "前任市委书记与市长曾共同工作", "overlap_org": "中共扎兰屯市委员会/扎兰屯市人民政府", "overlap_period": "至2026年6月", "confidence": "confirmed"},
    {"person_a": 30, "person_b": 3, "type": "overlap", "context": "前任市委书记与副书记工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "至2026年6月", "confidence": "confirmed"},

    # Standing committee internal relationships
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "市委副书记与常务副市长工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "宣传部与统战部工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "组织部与市委办公室工作关系", "overlap_org": "中共扎兰屯市委员会", "overlap_period": "至今", "confidence": "confirmed"},
]

# ── Runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
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
    print(f"DB:  {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
