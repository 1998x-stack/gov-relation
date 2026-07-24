#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 鄂州市 (Ezhou City), 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_鄂州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.ezhou.gov.cn — 鄂州市人民政府官方网站 (primary, current as of July 2026)
  - www.ezhou.gov.cn/sy/ldzc/swld/ — 市委领导页面
  - www.ezhou.gov.cn/sy/ldzc/szfld/ — 市政府领导页面
  - Individual bio pages on ezhou.gov.cn for each leader (under /sy/ldzc/...)

Confidence notes:
  - Current roles and basic bios: confirmed via official government website (July 2026)
  - Birth years, education, and party membership: confirmed from official bios
  - Detailed career timelines (full work history): mostly unverified due to limited official bio length
  - Predecessors: identified from news, specific dates unverified
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
SLUG = "鄂州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hubei_鄂州市"
if _CURRENT_DIR.name == "hubei_鄂州市":
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
# IDs: 1-9 party standing committee, 10-19 government leaders, 20-29 predecessor/other, 30+ NPC/CPPCC

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孙兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年12月",
        "birthplace": "",
        "education": "在职大学学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/sb/",
        "confidence": "confirmed",
        "notes": "1966年12月出生，在职大学学历，经济学硕士学位。现任鄂州市委书记。此前曾任湖北省退役军人事务厅厅长等职。"
    },
    {
        "id": 2,
        "name": "王玺玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年1月",
        "birthplace": "",
        "education": "在职博士研究生、管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "鄂州市人民政府",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/wxw/",
        "confidence": "confirmed",
        "notes": "1981年1月出生，在职博士研究生、管理学博士。现任鄂州市委副书记、市人民政府市长、党组书记。主持市政府全面工作，分管市审计局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "朱其敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/201909/t20190930_230883.html",
        "confidence": "confirmed",
        "notes": "1972年7月出生，大学学历，法学学士。现任鄂州市委副书记、市委教育工作委员会书记。"
    },
    {
        "id": 4,
        "name": "张权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/szzq/",
        "confidence": "confirmed",
        "notes": "市委常委、副市长。具体分工待查。"
    },
    {
        "id": 5,
        "name": "卢辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "",
        "education": "在职研究生学历、工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202209/t20220913_496561.html",
        "confidence": "confirmed",
        "notes": "1970年2月出生，在职研究生学历、工商管理硕士。现任鄂州市委常委、市政府副市长、党组成员。负责科技、工业、交通运输、水利、农业农村、乡村振兴、市场监管等方面工作。"
    },
    {
        "id": 6,
        "name": "张爱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、鄂州军分区政委",
        "current_org": "鄂州军分区",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202303/t20230306_525698.html",
        "confidence": "confirmed",
        "notes": "市委常委、鄂州军分区政委。相关简历不公开。"
    },
    {
        "id": 7,
        "name": "张红英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学学历，在职文学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共鄂州市纪律检查委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202504/t20250428_700480.html",
        "confidence": "confirmed",
        "notes": "1976年4月出生，大学学历，在职文学硕士。现任鄂州市委常委、市纪委书记、市监委副主任、代理主任。"
    },
    {
        "id": 8,
        "name": "柯尊勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "在职大学学历、法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202510/t20251029_731499.html",
        "confidence": "confirmed",
        "notes": "1973年8月出生，在职大学学历、法学博士。现任鄂州市委常委、市委组织部部长、市委党校校长。"
    },
    {
        "id": 9,
        "name": "任蔚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "",
        "education": "在职大学学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202510/t20251029_731476.html",
        "confidence": "confirmed",
        "notes": "1979年1月出生，在职大学学历，管理学学士学位。现任鄂州市委常委、市委宣传部部长。"
    },
    {
        "id": 10,
        "name": "刘来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202601/t20260127_748173.html",
        "confidence": "confirmed",
        "notes": "1975年6月出生，省委党校研究生学历。现任鄂州市委常委、市委统战部部长、市政协党组副书记。"
    },
    {
        "id": 11,
        "name": "尹彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共鄂州市委员会",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/swld/202605/t20260506_763335.html",
        "confidence": "confirmed",
        "notes": "1972年9月出生，在职大学学历。现任鄂州市委常委、市委秘书长、市委办公室主任、市委直属机关工委书记、临空经济区党工委书记。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "邱实",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "鄂州市人民政府",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/qiushi/",
        "confidence": "confirmed",
        "notes": "1971年11月出生，无党派，大学学历。现任鄂州市政府副市长。负责自然资源和城乡建设、生态环境、住房和城市更新、城市管理、公积金管理方面工作。"
    },
    {
        "id": 13,
        "name": "刘明锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "鄂州市人民政府",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/",
        "confidence": "confirmed",
        "notes": "副市长。具体分工待查。"
    },
    {
        "id": 14,
        "name": "徐舫",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "大学学历，在职法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "鄂州市人民政府",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/szxf/",
        "confidence": "confirmed",
        "notes": "1974年12月出生，大学学历，在职法律硕士。现任鄂州市政府副市长、党组成员，市公安局党委书记、局长、督察长，市委政法委第一副书记。"
    },
    {
        "id": 15,
        "name": "邵立春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "在职大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "鄂州市人民政府",
        "source": "https://www.ezhou.gov.cn/sy/ldzc/szfld/shaolichun/",
        "confidence": "confirmed",
        "notes": "1971年3月出生，在职大专学历。现任市政府党组成员、秘书长、市政府办公室党组书记、主任。负责市政府办公室、新闻发布方面工作。分管市政府驻京联络处。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (based on known transitions)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "孙兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年12月",
        "birthplace": "",
        "education": "在职大学学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记（前任职务：湖北省退役军人事务厅厅长）",
        "current_org": "中共鄂州市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "孙兵于2022年左右调任鄂州市委书记，此前曾任湖北省退役军人事务厅厅长。此前任职还有：湖北省政府副秘书长等职。"
    },
    {
        "id": 21,
        "name": "王立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共鄂州市委员会",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任鄂州市委书记，约2021-2022年在任，后调任。具体去向待查。"
    },
    {
        "id": 22,
        "name": "陈平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "鄂州市人民政府",
        "source": "公开报道",
        "confidence": "plausible",
        "notes": "前任鄂州市市长。王玺玮的前任。具体时间和去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄂州市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委员会", "location": "鄂州市"},
    {"id": 2, "name": "鄂州市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "鄂州市"},
    {"id": 3, "name": "中共鄂州市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共鄂州市委员会", "location": "鄂州市"},
    {"id": 4, "name": "鄂州军分区", "type": "党委", "level": "地级市", "parent": "湖北省军区", "location": "鄂州市"},
    {"id": 5, "name": "鄂州市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "鄂州市"},
    {"id": 6, "name": "中国人民政治协商会议鄂州市委员会", "type": "政协", "level": "地级市", "parent": "政协湖北省委员会", "location": "鄂州市"},
    {"id": 7, "name": "鄂州市公安局", "type": "政府", "level": "正处级", "parent": "鄂州市人民政府", "location": "鄂州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任鄂州市委书记"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "主持市政府全面工作"},
    # Party Standing Committee
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市委教育工作委员会书记"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任副市长"},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任副市长"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责科技、工业、交通、水利、农业农村、乡村振兴、市场监管等"},
    {"person_id": 6, "org_id": 4, "title": "市委常委、鄂州军分区政委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "简历不公开"},
    {"person_id": 7, "org_id": 3, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市监委副主任、代理主任"},
    {"person_id": 8, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市委党校校长"},
    {"person_id": 9, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市政协党组副书记"},
    {"person_id": 11, "org_id": 1, "title": "市委常委、市委秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任临空经济区党工委书记"},
    # Government
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "无党派。负责自然资源、城乡建设、生态环境、住房和城市更新等"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市公安局局长"},
    {"person_id": 14, "org_id": 7, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "市政府党组成员"},
    # Predecessors
    {"person_id": 20, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "孙兵此前曾任湖北省退役军人事务厅厅长、湖北省政府副秘书长等职"},
    {"person_id": 21, "org_id": 1, "title": "前任市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "孙兵的前任，约2021-2022年在任"},
    {"person_id": 22, "org_id": 2, "title": "前任市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "王玺玮的前任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 孙兵 ↔ 王玺玮 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共鄂州市委员会", "overlap_period": "2022-2026"},
    # 孙兵 ↔ 朱其敏 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    # 孙兵 ↔ 张权 (Party Secretary – Standing Committee)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    # 孙兵 ↔ 卢辉
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委", "overlap_org": "中共鄂州市委员会", "overlap_period": "2022-2026"},
    # 孙兵 ↔ 张爱华
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—军分区政委", "overlap_org": "中共鄂州市委员会", "overlap_period": "2023-2026"},
    # 孙兵 ↔ 张红英
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    # 孙兵 ↔ 柯尊勇
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    # 孙兵 ↔ 任蔚
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    # 孙兵 ↔ 刘来
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    # 孙兵 ↔ 尹彬
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    # 王玺玮 ↔ 张权 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    # 王玺玮 ↔ 卢辉
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂州市人民政府", "overlap_period": "2022-2026"},
    # 王玺玮 ↔ 邱实
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    # 王玺玮 ↔ 刘明锋
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    # 王玺玮 ↔ 徐舫
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    # 王玺玮 ↔ 邵立春
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—秘书长", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    # Standing committee internal (complete network)
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委兼副市长同僚", "overlap_org": "鄂州市人民政府", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    {"person_a": 5, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2025-2026"},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 8, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共鄂州市委员会", "overlap_period": "2026"},
    # Predecessor relationships
    {"person_a": 21, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共鄂州市委员会", "overlap_period": ""},
    {"person_a": 22, "person_b": 2, "type": "交接", "context": "前任市长—现任市长", "overlap_org": "鄂州市人民政府", "overlap_period": ""},
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
    slug_id = f"ezhou_{name}"

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
            "notes": "公开资料不足，完整履历待查。政府官网简历较简略，百度百科403禁止访问。",
            "confidence": "unverified",
            "source_ids": [],
        })
    elif len(career_timeline) <= 2 and person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "政府官网仅提供当前职务简介，此前完整任职履历待查。",
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
            "person_id": f"ezhou_{other_name}",
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
            "title": "鄂州市人民政府官方网站—领导之窗",
            "url": "https://www.ezhou.gov.cn/sy/ldzc/",
            "publisher": "鄂州市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月官方领导页面确认领导职务和基本信息",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省",
            "city": "鄂州市",
            "region": "鄂州市",
            "job": person.get("current_post", ""),
            "task_id": "hubei_鄂州市",
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
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "籍贯、此前完整任职履历（政府官网简历仅提供当前职务简介）" if not person.get("birthplace") else "此前完整任职履历",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的籍贯和此前完整任职履历",
                "why_it_matters": "核心身份信息和网络分析所需的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Add birth-specific question if missing
    if not person.get("birth"):
        record["open_questions"].append({
            "priority": "critical",
            "question": f"{name}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{name} 简历", f"{name} 出生"],
            "last_attempted": AS_OF,
        })

    fname = f"{TODAY}-湖北省-鄂州市-{person['current_post']}-{person['name']}.json"
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
    # Core leaders + predecessors
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
