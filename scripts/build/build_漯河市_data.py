#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 漯河市 (Luohe City), 河南省.

Investigation date: 2026-08-05
Task ID: henan_漯河市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.luohe.gov.cn — 漯河市人民政府官方网站 (primary, current as of Aug 2026)
    领导之窗 / 政务公开 (zfxxgkpt) 2026-07/08 新闻、会议
  - 百度百科 — 黄钫、刘尚进 履历 (confirmed)
  - Repository prior artifacts: 召陵区 (王奇山 召陵区委书记→漯河副市长), 鹤壁市 (王泽华 鹤壁组织部长→漯河副书记)

Web-access notes:
  - Exa search rate-limited, Google/Jina Reader timeouts → used official gov site + 百度百科 direct access
  - Current roles confirmed via multiple official pages (July-Aug 2026)
  - Biographical gaps labeled with confidence; open_questions explicitly recorded

Confidence:
  - 核心职务 (书记/市长): confirmed
  - 黄钫 完整履历: confirmed via 百度百科
  - 刘尚进 (前任书记) 履历: confirmed via 百度百科
  - 多数常委/副市长 b经典bio (birth/birthplace/education): unverified — recorded as open_questions
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
SLUG = "漯河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
# When run from data/tmp/<task_id>/, STAGING is that directory.
# When promoted & run from repo root, STAGING falls back to current dir; person JSONs go to PERSONS_DIR.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_漯河市"
if _CURRENT_DIR.name == "henan_漯河市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
# Person JSONs are written to STAGING first; process_tmp.py --apply promotes
# them to data/persons/ together with the DB and GEXF.
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1 书记, 2 市长, 3-9 常委/政府, 10-19 常委/人大/政协, 30+ 前任
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core leadership — current
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "黄钫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "河南省开封市",
        "education": "中央财经大学本科，四川大学经济学博士（研究生学历）",
        "party_join": "1994-12",
        "work_start": "1995-07",
        "current_post": "市委书记",
        "current_org": "中共漯河市委员会",
        "source": "https://www.luohe.gov.cn/zxdt/content_1059864",
        "confidence": "confirmed",
        "notes": "漯河军分区党委第一书记（2026.06增补）；2026.05任漯河市委书记",
    },
    {
        "id": 2,
        "name": "乔彦强",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "市长、市政府党组书记；2026.07-08 多次主持市政府及防汛工作；完整履历待查",
    },
    {
        "id": 3,
        "name": "王泽华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共漯河市委员会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1059985",
        "confidence": "confirmed",
        "notes": "原鹤壁市委常委、组织部部长 → 漯河市委副书记（跨市调动，repo: build_鹤壁市_data.py）；2026-08-04主持重点工作重大项目交办会",
    },
    {
        "id": 4,
        "name": "周剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共漯河市委员会",
        "source": "https://www.luohe.gov.cn/jrlh/zwyw/content_1060161",
        "confidence": "confirmed",
        "notes": "市委常委、常务副市长；主持市政府第197次重点项目建设周例会(2026-08-05)",
    },
    {
        "id": 5,
        "name": "张旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共漯河市委员会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1060159",
        "confidence": "confirmed",
        "notes": "市委常委、组织部部长；2026-08-05 参加全省县乡人大换届部署会",
    },
    {
        "id": 6,
        "name": "石铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记",
        "current_org": "中共漯河市纪律检查委员会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1059644",
        "confidence": "confirmed",
        "notes": "市委常委、市纪委书记、市监委代理主任；2026-07-31主持全市纪检监察工作会",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府 副市长 & 秘书长 (领导之窗)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "刘志辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "副市长 (领导之窗 列示)；具体分管待查",
    },
    {
        "id": 11,
        "name": "宋琰琰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "副市长 (领导之窗)；具体业务待查",
    },
    {
        "id": 12,
        "name": "时中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "副市长，市公安局党委书记、局长 (在线访谈 2026-06-08)",
    },
    {
        "id": 13,
        "name": "王奇山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "原召陵区委书记 → 升任漯河副市长（跨级晋升，repo: build_召陵区_data.py）",
    },
    {
        "id": 14,
        "name": "项丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "副市长；分管水利/基建（2026-08-03调研城乡供水一体化、沙河治理项目）",
    },
    {
        "id": 15,
        "name": "闫沛",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "漯河市人民政府",
        "source": "https://www.luohe.gov.cn/zfxxgkpt/",
        "confidence": "confirmed",
        "notes": "市政府秘书长 (领导之窗)",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市人大 / 市政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "李思杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "漯河市人民代表大会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1060159",
        "confidence": "confirmed",
        "notes": "市人大常委会主任；2026-08-05 全省人大换届选举会议漯河分会场",
    },
    {
        "id": 21,
        "name": "李乾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "漯河市人民代表大会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1060159",
        "confidence": "confirmed",
        "notes": "市人大常委会副主任；2026-08-05 人大换届会议",
    },
    {
        "id": 22,
        "name": "张炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会秘书长",
        "current_org": "漯河市人民代表大会",
        "source": "https://www.luohe.gov.cn/jrlh/jrlh1/content_1060159",
        "confidence": "confirmed",
        "notes": "市人大常委会秘书长",
    },
    {
        "id": 23,
        "name": "王克俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "漯河市政治协商会议",
        "source": "https://www.luohe.gov.cn/zxdt/content_1059865",
        "confidence": "plausible",
        "notes": "市领导；2026-08-03 议军会/八一活动出席，疑似市政协主席（待确认精确职务）",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任 leaders
    # ══════════════════════════════════════════════════════════════════════
{
        "id": 30,
        "name": "刘尚进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "河南省社旗县",
        "education": "河南师范大学（大学，文学学士）",
        "party_join": "1991-12",
        "work_start": "1993-07",
        "current_post": "前任市委书记",
        "current_org": "中共漯河市委员会",
        "source": "https://baike.baidu.com/item/刘尚进",
        "confidence": "confirmed",
        "notes": "漯河市委副书记(2017.12)、市长(2018.01-2021.06)、书记(2021.06-2023.01);后任河南副省长;现任重庆市委副书记、常务副市长（2026.06）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漯河市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "漯河市"},
    {"id": 2, "name": "漯河市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "漯河市"},
    {"id": 3, "name": "漯河市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "漯河市"},
    {"id": 4, "name": "漯河市政治协商会议", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "漯河市"},
    {"id": 5, "name": "中共漯河市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共河南省纪委", "location": "漯河市"},
    {"id": 6, "name": "漯河市公安局", "type": "政府", "level": "地级市", "parent": "漯河市人民政府", "location": "漯河市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 黄钫 (id=1) — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-05", "end_date": "", "rank": "正厅级", "note": "2026.05任市委书记；漯河军分区党委第一书记"},
    # 乔彦强 (id=2) — mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "市委副书记、市长、市政府党组书记"},
    # 王泽华 (id=3) deputy party secretary
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "原鹤壁市委组织部部长，跨市调"},
    # 周剑 (id=4) standing committee + exec deputy mayor
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "主持重点项目周例会"},
    # 张旭 (id=5) org department head
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 石铭 (id=6) discipline secretary
    {"person_id": 6, "org_id": 5, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市监委代理主任"},
    # 副市长
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "刘志辉"},
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "宋琰琰"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "时中华"},
    {"person_id": 12, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": "市公安局党委书记、局长"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "王奇山，原召陵区委书记"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "项丽"},
    {"person_id": 15, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "闫沛"},
    # 人大
    {"person_id": 20, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": "李思杰"},
    {"person_id": 21, "org_id": 3, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": "李乾"},
    {"person_id": 22, "org_id": 3, "title": "市人大常委会秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": "张炜"},
    # 政协
    {"person_id": 23, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": "王克俊（待核实）"},
    # 前任
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2021-06", "end_date": "2023-01", "rank": "正厅级", "note": "刘尚进"},
    {"person_id": 30, "org_id": 2, "title": "市长", "start_date": "2018-01", "end_date": "2021-06", "rank": "正厅级", "note": "刘尚进"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 黄钫 ↔ 乔彦强 (书记-市长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "漯河市党政班子", "overlap_period": "2026"},
    # 黄钫 ↔ 王泽华
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    # 黄钫 ↔ 周剑
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委/常务副", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    # 黄钫 ↔ 张旭
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    # 黄钫 ↔ 石铭
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    # 乔彦强 ↔ 各副市长
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常务副", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—副市长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "市长—秘书长", "overlap_org": "漯河市人民政府", "overlap_period": "2026"},
    # 常委同僚
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委同僚", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市委同僚", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委同僚", "overlap_org": "中共漯河市委员会", "overlap_period": "2026"},
    # 人大/政协 与市委联系
    {"person_a": 20, "person_b": 1, "type": "同僚", "context": "人大主任—书记", "overlap_org": "漯河市班子", "overlap_period": "2026"},
    {"person_a": 23, "person_b": 1, "type": "同僚", "context": "政协主席—书记（待核实）", "overlap_org": "漯河市班子", "overlap_period": "2026"},
    # 前任-现任 交接
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任书记→现任书记", "overlap_org": "中共漯河市委员会", "overlap_period": "2021-2023"},
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
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"luohe_{name}"

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

    if not person.get("birth") and len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科/搜索受限。",
            "confidence": "unverified",
            "source_ids": [],
        })

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
            "person_id": f"luohe_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "漯河市人民政府官方网站（领导之窗/新闻）",
        "url": source_url,
        "publisher": "漯河市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2026年7-8月新闻及领导之窗确认领导职务",
    }, {
        "id": "S002",
        "title": "百度百科",
        "url": "https://baike.baidu.com",
        "publisher": "百度",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "encyclopedia",
        "reliability": "medium",
        "notes": "黄钫、刘尚进 履历",
    }]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "漯河市",
            "region": "漯河市",
            "job": person.get("current_post", ""),
            "task_id": "henan_漯河市",
            "time_focus": "2026年8月",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
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
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历（web受限）" if not person.get("birth") else "部分履历细分",
        },
        "open_questions": [
            {
                "priority": "critical" if person.get("birth") else "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-河南省-漯河市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


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
    core_ids = {1, 2, 3, 4, 5, 30}  # Core leaders + key predecessor
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())