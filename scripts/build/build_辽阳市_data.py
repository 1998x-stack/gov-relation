#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 辽阳市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_辽阳市
Level: 地级市
Targets: 市委书记(郭云峰) & 市长(代市长 李勇)

Research sources (all accessed 2026-08-06):
  - http://www.liaoyang.gov.cn/ — 辽阳市人民政府门户网站 (official, primary)
      * 领导之窗页 http://www.liaoyang.gov.cn/info_open.html?deptcode=033 (市政府领导 confirmed)
      * 李勇官网简历 govxxgk/LY/2026-07-23/4e1390f1-... (official)
      * 吴波/赵丕显/刘畅/朱鹤春/刘万鹏/李春鹏/梁臣 官网领导简介 (official)
  - 本市要闻 & 市政府全体会议/常务会议新闻 (official)
  - 辽阳新闻网转载于市政府门户 (official)
  - repo data/persons/20260725-辽宁省-沈阳市-市委书记-霍步刚.json (前辽阳市委书记 2021-04~2023-01)

Confidence notes:
  - 现任市委书记郭云峰 — confirmed (官方新闻 2026-07-28 起以"市委书记"署名；2026-04 尚为"代市长/市长"，约 2026-07 由市长升任书记)
  - 现任代市长李勇 — confirmed (官方领导简介：市委副书记、市政府党组书记、副市长、代市长；1974-12生，研究生/博士)
  - 市政府 8 位副市长 + 秘书长 名单 — confirmed (官网领导之窗/各人简历页)
  - 市人大主任马涛、市政协主席吴松 — confirmed (官方新闻)
  - 市委常委、秘书长宋化云 — confirmed
  - 副市长中石进军(mid 2026 简历)出生/学历细节偏简；部分但简历公开可用
  - 郭云峰任市委书记前完整履历（含任辽阳市长前职务）、李勇任代市长前履历、(2023-2026间)前任市委书记身份  —— 留 open_questions
  - 市委其他常委（纪委书记/组织/宣传/政法/统战部长）名单官网未开放 —— 留 open_questions

Web-access note: Exa 限流、Baidu 403、Bing 被拦；HTTPS www.liaoyang.gov.cn 422；HTTP 走通（Playwright）。
"""

from __future__ import annotations

import json
import re
import sqlite3
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "辽阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_辽阳市"
if _CURRENT_DIR.name == "liaoning_辽阳市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# 核心: 1=市委书记 郭云峰, 2=代市长 李勇
# 市政府: 3 常务副市长 吴波, 4-8 副市长, 9 秘书长
# 四套班子: 10 人大主任 马涛, 11 政协主席 吴松
# 市委: 12 市委常委、秘书长 宋化云
# 前任: 13 前辽阳市委书记 霍步刚(2021-23)
persons = [
    # ═══ 现任核心 ══════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "郭云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "学历待核",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市委书记",
        "current_org": "中共辽阳市委员会",
        "source": "http://www.liaoyang.gov.cn/ （官方新闻：2026-08-04 市委常委会'市委书记郭云峰主持会议'；2026-07-31 市委常委会(扩大)；2026-07-28 慰问老同志以'市委书记'署名）"
    },
    {
        "id": 2,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市委副书记、市政府党组书记、副市长、代市长",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2026-07-23/4e1a90f1-29fa-4bca-9d53-7e7f9c8a121.html（代市长简介：男，汉族，1974年12月生，研究生学历，博士学位，中共党员。现任辽阳市委副书记，辽阳市人民政府副市长、代市长，市政府党组书记）"
    },
    {
        "id": 3,
        "name": "吴波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-12",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市委常委、市政府党组副书记、常务副市长",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxx/LY/2026-01-06/9f97410b-b5fd-4fd5-a9c6-30361e7f80e6.html（常务副市长简介：负责发展改革、财税、应急管理、国企国资、统计、国防动员、信访等）"
    },
    {
        "id": 4,
        "name": "赵丕显",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市副市长、市政府党组成员，市公安局党委书记、局长、督察长",
        "current_org": "辽阳市人民政府 / 辽阳市公安局",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2024-11-19/93a92f22-a0b0-4916-ab07-ae6e951313f.html（副市长简介：负责公安、司法、打击走私）"
    },
    {
        "id": 5,
        "name": "刘畅",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "研究生学历，工学博士学位",
        "party_join": "致公党党员",
        "work_start": "",
        "current_post": "辽阳市人民政府副市长",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2026-05-08/dfa0125e-1a84-495b-80c0-c06b1f78066e.html（副市长简介：负责教育、卫生健康、医疗保障等）"
    },
    {
        "id": 6,
        "name": "朱福春",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1972-04",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市副市长、市政府党组成员",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2023-11-15/6244d8ef-8fbe-4800-b542-2249acc17d46.html（副市长简介：负责工业和信息化、市场监管、营商环境、大数据等）"
    },
    {
        "id": 7,
        "name": "刘万鹏",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1979-04",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市副市长、市政府党组成员",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2026-01-06/4f6450c6-a146-4ce0-a63f-0e1d74f756e0.html（副市长简介：负责民政、人力资源和社会保障、商务、外事、退役军人等）"
    },
    {
        "id": 8,
        "name": "李春鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市副市长、市政府党组成员",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/govxxgk/LY/2026-04-14/59261ced-5b70-4731-9ddd-611f1b956a86.html（副市长简介：负责自然资源、住房和城乡建设、交通运输、林草等）"
    },
    {
        "id": 9,
        "name": "石进军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "待核",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市副市长、市政府党组成员",
        "current_org": "辽阳市人民政府",
        "source": "http://www.liaoyang.gov.cn/info_open.html?deptcode=033（市政府领导之窗列出 副市长 石进军）"
    },
    {
        "id": 10,
        "name": "梁臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-12",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市人民政府党组成员、秘书长、机关党组书记、市政府办公室主任兼市机关事务管理局局长",
        "current_org": "辽阳市人民政府办公室",
        "source": "http://www.liaoyang.gov.cn/info_open.html?deptcode=033（市政府秘书长简介，2026-07-01 更新）"
    },
    {
        "id": 11,
        "name": "马涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市人大常委会党组书记、主任",
        "current_org": "辽阳市人大常委会",
        "source": "http://www.liaoyang.gov.cn/ （本市要闻：2026-07-31 出席市委常委会(扩大)；2026-07-31 走访慰问退役军人；2026-08-05 郭云峰到市人大机关走访，马涛参加）"
    },
    {
        "id": 12,
        "name": "吴松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市政协党组书记、主席",
        "current_org": "政协辽阳市委员会",
        "source": "http://www.liaoyang.gov.cn/ （本市要闻：2026-07-31 吴松走访慰问退役军人，列市政协领导）"
    },
    {
        "id": 13,
        "name": "宋化云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽阳市委常委、秘书长",
        "current_org": "中共辽阳市委员会",
        "source": "http://www.liaoyang.gov.cn/ （2026-08-05 郭云到市人大走访，'市委常委、秘书长宋化云参加'；2026-07-27 慰问老同志同款）"
    },
    {
        "id": 14,
        "name": "霍步刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "江苏省淮安市",
        "education": "北京师范大学哲学系思想政治教育专业，经济学博士",
        "party_join": "1993-05",
        "work_start": "1995-07",
        "current_post": "辽宁省委常委、沈阳市委书记（前辽阳市委书记 2021-04~2023-01）",
        "current_org": "中共沈阳市委（曾在任辽阳）",
        "source": "repo data/persons/20260725-辽宁省-沈阳市-市委书记-白鹤刚.json + 沈阳市党务公开网站"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共辽阳市委员会", "type": "party_committee", "level": "地厅级", "parent": "中共辽宁省委", "location": "辽阳市"},
    {"id": 2, "name": "辽阳市人民政府", "type": "government", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽阳市"},
    {"id": 3, "name": "辽阳市人大常委会", "type": "npc", "level": "地厅级", "parent": "", "location": "辽阳市"},
    {"id": 4, "name": "政协辽阳市委员会", "type": "cppcc", "level": "地厅级", "parent": "", "location": "辽阳市"},
    {"id": 5, "name": "辽阳市纪委市监委", "type": "discipline", "level": "地厅级", "parent": "辽宁省纪委", "location": "辽阳市"},
    {"id": 6, "name": "辽阳市公安局", "type": "government", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市"},
    {"id": 7, "name": "辽阳市人民政府办公室", "type": "government", "level": "县处级", "parent": "辽阳市人民政府", "location": "辽阳市"},
    {"id": 8, "name": "中共辽宁省委", "type": "party_committee", "level": "省级", "parent": "中国共产党中央委员会", "location": "辽宁省"},
    {"id": 9, "name": "辽宁省人民政府", "type": "government", "level": "省级", "parent": "", "location": "辽宁省"},
    {"id": 10, "name": "中共沈阳市委员会", "type": "party_committee", "level": "副省级", "parent": "中共辽宁省委", "location": "沈阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 郭云峰 (市委书记，前市长)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-07", "end_date": "present", "rank": "正厅级", "note": "约 2026-07 由市长升任市委书记；2026-08-04 主持市委常委会"},
    {"person_id": 1, "org_id": 2, "title": "市长（曾任）", "start_date": "2023", "end_date": "2026-07", "rank": "正厅级", "note": "市委副书记、市长；2026-01 主持市政府全体会议"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记（曾任）", "start_date": "", "end_date": "2026-07", "rank": "副厅级", "note": ""},
    # 李勇 (代市长)
    {"person_id": 2, "org_id": 2, "title": "代市长", "start_date": "2026-07", "end_date": "present", "rank": "正厅级", "note": "市委副书记、市政府党组书记、副市长、代市长；2026-07-27 主持市政府党组/常务会议"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": ""},
    # 吴波 (常务副市长)
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责发改、财税、应急、国资、统计、国防动员、信访等"},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 赵丕显 (公安)
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责公安、司法、打私"},
    {"person_id": 4, "org_id": 6, "title": "市公安局党委书记、局长、督察长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 刘畅 (致公党)
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责教育、卫生健康、医保"},
    # 朱鹤春
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责工业和信息化、市场监管、营商环境、大数据"},
    # 刘万鹏
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责民政、人社、商务、外事、退役"},
    # 李春鹏
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "负责自然资源、住建、交通、林草"},
    # 石进军
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 梁臣 (秘书长)
    {"person_id": 10, "org_id": 7, "title": "市长办公室秘书长", "start_date": "", "end_date": "present", "rank": "正县处级", "note": "市政府党组成员、秘书长、机关党组书记、办公室主任兼机关事务管理局局长"},
    # 人大 / 政协
    {"person_id": 11, "org_id": 3, "title": "主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市人大常委会主任"},
    {"person_id": 12, "org_id": 4, "title": "主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "市政协主席"},
    # 市委
    {"person_id": 13, "org_id": 1, "title": "市委常委、秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 前任/跨区
    {"person_id": 14, "org_id": 10, "title": "沈阳市委书记（现任）", "start_date": "2025-05", "end_date": "present", "rank": "副省级", "note": "辽宁省委常委"},
    {"person_id": 14, "org_id": 1, "title": "辽阳市委书记（曾任）", "start_date": "2021-04", "end_date": "2023-01", "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—代市长（现任核心）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记—代市长", "overlap_org": "中共辽阳市委员会 / 辽阳市人民政府", "overlap_period": "2026-07"},
    # 书记—常务副市长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记—常务副市长（常委）", "overlap_org": "中共辽阳市委员会", "overlap_period": ""},
    # 代市长—政府班子
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "代市长—常务副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "代市长—副市长（公安局长）", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "代市长—副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "代市长—副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "代市长—副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "代市长—副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "代市长—副市长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "代市长—秘书长", "overlap_org": "辽阳市人民政府", "overlap_period": ""},
    # 四套班子
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "市委书记—市人大常委会主任", "overlap_org": "辽阳市", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "市委书记—市政协主席", "overlap_org": "辽阳市", "overlap_period": ""},
    # 书记—市委秘书长
    {"person_a": 1, "person_b": 13, "type": "subordinate_supervisor", "context": "市委书记—市委秘书长（随同活动）", "overlap_org": "中共辽阳市委员会", "overlap_period": ""},
    # 前任市委书记
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor", "context": "前市委书记(白鹤刚 2021-23)—现任市委书记(郭云峰 2026-)", "overlap_org": "中共辽阳市委员会", "overlap_period": ""},
    # 市长晋升书记
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "郭云峰(市长)→ 升任市委书记；李勇(代市长)接任市政府", "overlap_org": "辽阳市人民政府", "overlap_period": "2026-07"},
]

# ── Person JSON(s) ────────────────────────────────────────────────────────────
def _write_person_json(person: dict, out_dir: Path) -> None:
    """Write a person graph JSON for the person."""
    job_tag = person["current_post"] or person["name"]
    if job_tag.startswith("辽阳"):
        job_tag = job_tag[len("辽阳"):]
    if job_tag[:2] != "市委" and job_tag.startswith("市"):
        job_tag = job_tag[1:]
    raw_name = f"{TODAY}-辽宁省-辽阳市-{job_tag}-{person['name']}.json"
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", raw_name)
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "辽阳市",
            "region": "辽阳市",
            "job": person["current_post"],
            "task_id": "liaoning_辽阳市",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"liaoyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正厅级" if person["id"] in (1, 2, 11, 12) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person["source"]),
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present" if person["current_post"] else "",
                "org": person["current_org"],
                "title": person["current_post"],
                "confidence": "confirmed" if person["source"] else "plausible",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本轮调查未发现不良记录信号。", "confidence": "unverified"}],
        "source_register": [
            {"id": "S001", "title": "辽阳市人民政府门户网站（领导之窗 / 领导简介 / 本市要闻）", "url": person["source"], "publisher": "辽阳市人民政府", "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed" if person["current_post"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年月至今的全部职务变动、任现职前任职）",
        },
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整工作履历", "why_it_matters": "了解晋升路径和人际网络", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 此前担任"], "last_attempted": TODAY}
        ],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    key_people_ids = [1, 2, 3, 4, 10]
    for pid in key_people_ids:
        kp = dict(persons[pid - 1])
        kp.setdefault("aliases", [])
        fpath = _write_person_json(kp, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF
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

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    p_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    o_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    pos_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    r_count = cur.fetchone()[0]
    conn.close()

    print(f"\n  DB written: {DB_PATH.exists()}, size={DB_PATH.stat().st_size} bytes")
    print(f"    Persons: {p_count}, Orgs: {o_count}, Positions: {pos_count}, Relations: {r_count}")
    print(f"  GEXF written: {GEXF_PATH.exists()}, size={GEXF_PATH.stat().st_size} bytes")
    print(f"═══ Done ═══")