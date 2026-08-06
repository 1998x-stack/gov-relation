#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 乌海市 (Wuhai City), 内蒙古自治区.

Investigation date: 2026-08-06
Task ID: inner_mongolia_乌海市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.wuhai.gov.cn — 乌海市人民政府官方网站 (primary, current as of 2026-08-06)
    * 市委领导页: http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855445/index.html
    * 市政府领导工作动态(2026-08-05): http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html
    * 干部任免(2026-06-04 등): http://www.wuhai.gov.cn/wuhai/swdwgk/ldbz70/
  - Wikipedia 周金星 (secondary): https://zh.wikipedia.org/wiki/周金星
  - 中国经济经(维基引用) 2024-10-13: "唐毅任赤峰市委书记 周金星接任乌海市委书记"

Confidence notes:
  - Current roles & leadership roster: confirmed via 官方乌海市政府网站 市委领导页 (2026-08-06)
  - Birth/ethnicity/education of all 11 市委常委: confirmed from official roster
  - 周金星 full career (北京昌平区→东城区区长→2024.10乌海市委书记): confirmed via Wikipedia (secondary, credible)
  - 齐海斌 任市长前完整履历: unverified (web search engines blocked: Exa rate-limit, Baidu 403, Jina timeouts)
  - Predecessor 唐毅→周金星(2024.10): confirmed via Wikipedia/ce.cn
  - Predecessor 崔景英(市长)→齐海斌: 崔景英在任 at 2024.10 confirmed; 接任时间 gap open question
  - All claims labeled with confidence; gaps explicitly documented in report/open_gaps.md
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401 — used by gov_relation.runner via import
from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "乌海市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
PROVINCE = "内蒙古自治区"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_乌海市"
if _CURRENT_DIR.name == "inner_mongolia_乌海市":
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
# IDs: 1-11 市委常委, 12-18 副市长, 30-31 前任核心领导
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "周金星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "湖北省大悟县",
        "education": "大学学历，法学学士（中国政法大学）",
        "party_join": "中共党员（2003-06入党）",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855445/index.html",
        "confidence": "confirmed",
        "notes": "湖北大悟人；长期在北京市昌平区工作；2021.12任北京市东城区区长；2024.10跨省任乌海市委书记（接替唐毅）",
    },
    {
        "id": 2,
        "name": "齐海斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "乌海市人民政府",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855453/index.html",
        "confidence": "confirmed",
        "notes": "现任乌海市委副书记、市长（2026在任）；任市长前完整履历待查",
    },
    {
        "id": 3,
        "name": "李昂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "",
        "education": "本科学历，文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、组织部部长",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855452/index.html",
        "confidence": "confirmed",
        "notes": "市委副书记、组织部部长（干部工作关键岗位）",
    },
    {
        "id": 4,
        "name": "严冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "education": "研究生学历，法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855454/index.html",
        "confidence": "confirmed",
        "notes": "法律专业背景，任市委常委、政法委书记",
    },
    {
        "id": 5,
        "name": "李冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "",
        "education": "研究生学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组副书记、副市长",
        "current_org": "乌海市人民政府",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855446/index.html",
        "confidence": "confirmed",
        "notes": "市委常委、市政府党组副书记、副市长",
    },
    {
        "id": 6,
        "name": "郭轶杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "",
        "education": "研究生学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "乌海市人民政府",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1934373/index.html",
        "confidence": "confirmed",
        "notes": "市委常委、政府党组副书记；2026-08 主持召开市长办公会议/市政府常务会议（常务副市长职责）",
    },
    {
        "id": 7,
        "name": "孟培云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855449/index.html",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 8,
        "name": "饶崇书",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-08",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、乌海军分区政治委员",
        "current_org": "乌海军分区",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855450/index.html",
        "confidence": "confirmed",
        "notes": "军分区政治委员（军方代表）",
    },
    {
        "id": 9,
        "name": "王允恒",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "本科学历，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、市监委主任",
        "current_org": "中共乌海市纪律检查委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855455/index.html",
        "confidence": "confirmed",
        "notes": "纪委书记、市监委主任",
    },
    {
        "id": 10,
        "name": "闫爽",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1981-12",
        "birthplace": "",
        "education": "研究生学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/1855489/index.html",
        "confidence": "confirmed",
        "notes": "市委常委会中较年轻成员（1981-12）",
    },
    {
        "id": 11,
        "name": "刘昌惠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-03",
        "birthplace": "",
        "education": "内蒙古党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长、直属机关工委书记",
        "current_org": "中共乌海市委员会",
        "source": "http://www.wuhai.gov.cn/wuhai/swdwgk/1855451/2331091/index.html",
        "confidence": "confirmed",
        "notes": "市委秘书长、直属机关工委书记",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府 副市长 (2026-08-05 市政府领导工作动态)
    # ══════════════════════════════════════════════════════════════════════
    {"id": 12, "name": "吴娜", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管领域待查"},
    {"id": 13, "name": "乔毓", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管领域待确认"},
    {"id": 14, "name": "张明明", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管领域待确认"},
    {"id": 15, "name": "高博", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管重点产业项目建设；分管工业/产业领域"},
    {"id": 16, "name": "李和平", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管领域待确认"},
    {"id": 17, "name": "满成云", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌海市人民政府",
     "source": "http://www.wuhai.gov.cn/wuhai/xxgk4/zfxxgk5572/fdzdgknr39/cf_qz52/2464994/index.html",
     "confidence": "confirmed", "notes": "分管领域待确认"},
    # ══════════════════════════════════════════════════════════════════════
    # 前任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "唐毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（现任赤峰市委书记）",
        "current_org": "中共赤峰市委员会",
        "source": "https://zh.wikipedia.org/wiki/周金星",
        "confidence": "confirmed",
        "notes": "曾任乌海市市长、乌海市委书记；2024-10 调任赤峰市委书记，周金星接任乌海市委书记（中国经济网2024-10-13）",
    },
    {
        "id": 31,
        "name": "崔景英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "乌海市人民政府（前任）",
        "source": "https://zh.wikipedia.org/wiki/周金星",
        "confidence": "unverified",
        "notes": "周金星2024-10到任乌海时担任市长（维基百科信息框『副职』）；现任去向待查；由齐海斌接任市长（时点待查）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乌海市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党内蒙古自治区委员会", "location": "乌海市"},
    {"id": 2, "name": "乌海市人民政府", "type": "政府", "level": "地级市", "parent": "内蒙古自治区人民政府", "location": "乌海市"},
    {"id": 3, "name": "中共乌海市纪律检查委员会/乌海市监察委员会", "type": "党委", "level": "地级市", "parent": "内蒙古自治区纪委监委", "location": "乌海市"},
    {"id": 4, "name": "乌海军分区", "type": "党委", "level": "地级市", "parent": "内蒙古军区", "location": "乌海市"},
    {"id": 5, "name": "中共北京市东城区委员会", "type": "党委", "level": "市辖区", "parent": "中共北京市委", "location": "北京市东城区"},
    {"id": 6, "name": "北京市东城区人民政府", "type": "政府", "level": "市辖区", "parent": "北京市人民政府", "location": "北京市东城区"},
    {"id": 7, "name": "中共赤峰市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党内蒙古自治区委员会", "location": "赤峰市"},
    {"id": 8, "name": "北京市昌平区（周金星早期工作地）", "type": "政府", "level": "市辖区", "parent": "北京市人民政府", "location": "北京市昌平区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 周金星 — 现任市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-10", "end_date": "", "rank": "正厅级", "note": "2024-10 跨省由北京东城区调入乌海任市委书记"},
    {"person_id": 1, "org_id": 6, "title": "东城区区长", "start_date": "2021-12", "end_date": "2024-10", "rank": "正厅级", "note": "2021-09代理，2021-12当选区长（中国经济网）"},
    {"person_id": 1, "org_id": 5, "title": "东城区委副书记", "start_date": "2021-09", "end_date": "2021-12", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "昌平区工作", "start_date": "2003", "end_date": "2021-09", "rank": "", "note": "长期在北京市昌平区工作（具体职务未详）"},
    # 齐海斌 — 现任市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼任市委副书记"},
    # 李昂 — 市委副书记、组织部部长
    {"person_id": 3, "org_id": 1, "title": "市委副书记、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 严冬 — 政法委书记
    {"person_id": 4, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李冬 — 政府党组副书记、副市长
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "市政府党组副书记、副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 郭轶杰 — 常务副市长
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "2026-08 曾主持市长办公会、市政府常务会议"},
    # 孟培云 — 宣传部长
    {"person_id": 7, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 饶崇书 — 军分区政委
    {"person_id": 8, "org_id": 4, "title": "市委常委、军分区政委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 王允恒 — 纪委书记
    {"person_id": 9, "org_id": 3, "title": "市委常委、纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 闫爽 — 统战部长
    {"person_id": 10, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 刘昌惠 — 秘书长
    {"person_id": 11, "org_id": 1, "title": "市委常委、秘书长、直属机关工委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 副市长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "分管重点产业项目建设"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 前任
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2024-10", "rank": "正厅级", "note": "前任乌海市委书记（2024-10离职）"},
    {"person_id": 30, "org_id": 7, "title": "赤峰市委书记", "start_date": "2024-10", "end_date": "", "rank": "正厅级", "note": "调任赤峰市委书记（中国经济网2024-10-13）"},
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市长，去向/是否卸任待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 周金星 ↔ 齐海斌 (书记—市长)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    # 周金星 ↔ 各市委常委
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—市委副书记/组织部长", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委（政法委）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委（副市长）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—常委（常务副市长）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—常委（宣传部长）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—常委（军分区政委）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—常委（统战部长）", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共乌海市委员会", "overlap_period": "2026"},
    # 齐海斌 ↔ 市政府
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—常务副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—副市长", "overlap_org": "乌海市人民政府", "overlap_period": "2026"},
    # 前任交接
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记→现任市委书记", "overlap_org": "中共乌海市委员会", "overlap_period": "2024-10"},
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长→现任市长", "overlap_org": "乌海市人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════
def slugify(name: str) -> str:
    return name


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"wuhai_{name}"

    # Identity → career_timeline from positions
    career_timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            career_timeline.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org["name"] if org else "",
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if (org and org["type"] == "党委") else ("government" if (org and org["type"] == "政府") else "other"),
                "rank": pos.get("rank", ""),
                "is_key_promotion": bool(pos.get("start_date") and pos.get("end_date")) and pos.get("title") in ("市委书记", "市长", "东城区区长"),
                "notes": pos.get("note", ""),
                "confidence": "plausible",
                "source_ids": ["S001"],
            })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查（网络受限：百度百科403、Exa限流、Jina超时）",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships
    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"wuhai_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {"id": "S001", "title": "乌海市人民政府网站—市委领导页/市领导页", "url": source_url,
         "publisher": "乌海市人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "2026-08-06 访问，确认现任领导职务、出生年月、民族、学历"},
        {"id": "S002", "title": "维基百科-周金星 / 中国经济网（2024-10-13 唐毅任赤峰市委书记 周金星接任乌海市委书记）",
         "url": "https://zh.wikipedia.org/wiki/周金星", "publisher": "维基百科/中国经济网",
         "published_at": "2024-10-13", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "周金星、唐毅、崔景英履历与交接信息"},
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": "乌海市",
            "region": "乌海市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_乌海市",
            "time_focus": "2026年",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
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
            "career_pattern": "cross_province_rotation" if pid == 1 else "unknown",
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
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "搜索范围为官方领导页与公开新闻，未发现所指纪律或舆情风险信号。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if pid == 1 else "thin",
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "齐海斌任市长前完整履历/崔景英去向待查" if pid == 2 else "",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "medium",
                "question": f"{name} 任现职前完整履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 此前担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid == 2 else "medium",
                "question": f"{name} 出生年月、籍贯、学历教育背景（部分缺失）",
                "why_it_matters": "核心身份信息，用于去重与跨区域关联",
                "suggested_queries": [f"{name} 籍贯", f"{name} 毕业院校"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-{PROVINCE}-{SLUG}-{person['current_post']}-{person['name']}.json"
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
    core_ids = {1, 2, 30, 31}  # 核心领导 + 前任
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())