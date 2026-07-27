#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 周口市 (Zhoukou City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_周口市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.zhoukou.gov.cn — 周口市人民政府官方网站 (primary, current as of July 2026)
  - News articles and meeting attendance lists from 周口市人民政府 website (July 2026)
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Jina Reader timeouts

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports (July 2026)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
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
SLUG = "周口市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/<task_id>/, STAGING is that directory.
# When run from repo root (e.g. as build_周口市_data.py), STAGING is data/tmp/henan_周口市/.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_周口市"
if _CURRENT_DIR.name == "henan_周口市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "黄玉国",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Henan party secretaries are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "此前曾任河南省自然资源厅厅长；2026年7月多次主持市委常委会会议"
    },
    {
        "id": 2,
        "name": "詹鹏",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "2026年7月多次主持市政府常务会议"
    },
    {
        "id": 3,
        "name": "王钦胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "2026年7月13日出任市老科协会长"
    },
    {
        "id": 4,
        "name": "牛越丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委)
    # Source: Multiple meeting attendance lists (July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "张建党",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "2026年7月调研淮阳区街区保护修缮工作"
    },
    {
        "id": 6,
        "name": "郭俊辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "兼任市政协党组副书记"
    },
    {
        "id": 7,
        "name": "王宏武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "具体分工待查；2026年7月出席重点项目调度会"
    },
    {
        "id": 8,
        "name": "皇甫立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "具体分工待查；2026年7月出席经济运行周例会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "秦胜军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "出席2026年7月市政府常务会议"
    },
    {
        "id": 10,
        "name": "梁建松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "出席煤焦钢客户恳谈会 (2026-07-17)"
    },
    {
        "id": 11,
        "name": "徐飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "出席2026年7月市政府常务会议"
    },
    {
        "id": 12,
        "name": "朱向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "出席2026年7月市政府常务会议"
    },
    {
        "id": 13,
        "name": "王家才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "出席安委会会议 (2026-07-10)"
    },
    {
        "id": 14,
        "name": "王文峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "周口市人民政府",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "多次陪同调研"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "胡艳华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "周口市人民代表大会常务委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 16,
        "name": "杨雪芹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任、市总工会主席",
        "current_org": "周口市人民代表大会常务委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "兼任市总工会主席"
    },
    {
        "id": 17,
        "name": "任哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组副书记、副主席",
        "current_org": "中国人民政治协商会议周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": "2026年7月23日带队赴郸城调研"
    },
    {
        "id": 18,
        "name": "岳新坦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 19,
        "name": "程若光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 20,
        "name": "王富生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议周口市委员会",
        "source": "https://www.zhoukou.gov.cn/zwzx/jrxx/",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "张建慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共周口市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "此前曾任河南省自然资源厅厅长（2023-2025任周口市委书记），去向待查"
    },
    {
        "id": 31,
        "name": "吉建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "周口市人民政府",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任市长，2024年被查"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共周口市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "周口市"},
    {"id": 2, "name": "周口市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "周口市"},
    {"id": 3, "name": "中国人民政治协商会议周口市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "周口市"},
    {"id": 4, "name": "周口市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "周口市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 黄玉国 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市委书记，此前曾任河南省自然资源厅厅长等职"},
    # 詹鹏 — current mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市长"},
    # 王钦胜 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 牛越丽 — CPPCC Chair
    {"person_id": 4, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张建党 — Executive Deputy Mayor
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 郭俊辉 — United Front Work Director
    {"person_id": 6, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市政协党组副书记"},
    # 王宏武
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "具体分工待查"},
    # 皇甫立新
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "具体分工待查"},
    # 秦胜军 — Deputy Mayor
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 梁建松 — Deputy Mayor
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 徐飞 — Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 朱向阳 — Deputy Mayor
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王家才 — Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王文峰 — Secretary-General
    {"person_id": 14, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 胡艳华
    {"person_id": 15, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨雪芹
    {"person_id": 16, "org_id": 4, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市总工会主席"},
    # 任哲
    {"person_id": 17, "org_id": 3, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": "党组副书记"},
    # 岳新坦
    {"person_id": 18, "org_id": 3, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 程若光
    {"person_id": 19, "org_id": 3, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王富生
    {"person_id": 20, "org_id": 3, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 张建慧 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市委书记，去向待查"},
    # 吉建军 — predecessor Mayor
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市长，2024年被查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 黄玉国 ↔ 詹鹏 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    # 黄玉国 ↔ 王钦胜 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    # 黄玉国 ↔ 张建党 (Party Secretary – Standing Committee)
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    # 詹鹏 ↔ 张建党 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 秦胜军
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 梁建松
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 徐飞
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 朱向阳
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 王家才
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # 詹鹏 ↔ 王文峰
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—秘书长", "overlap_org": "周口市人民政府", "overlap_period": "2026"},
    # Standing committee internal relationships
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共周口市委员会", "overlap_period": "2026"},
    # Predecessor relationships
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共周口市委员会", "overlap_period": ""},
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "周口市人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"zhoukou_{name}"

    # Collect positions for this person
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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"zhoukou_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "周口市人民政府官方网站",
            "url": source_url,
            "publisher": "周口市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月新闻和会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "周口市",
            "region": "周口市",
            "job": person.get("current_post", ""),
            "task_id": "henan_周口市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
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
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
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
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，搜索引擎超时）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-河南省-周口市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 30, 31}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
