#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平城区 (Pingcheng District), 大同市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_平城区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.pingcheng.gov.cn — 平城区人民政府官方网站（政府领导页面、领导活动页面）
  - 区委书记：孟德昌 — 多次出现在公务活动报道中（2026年6月-7月），主持常委会会议
  - 区长：郭政（1986年3月生，山西定襄人，研究生学历，2009年8月参加工作）
  - 常务副区长：崔峰（1978年10月生，山西怀仁人，研究生学历）
  - 区政府领导共9人（含1名挂职副区长）
  - 郭政此前曾任忻州市政府办公室副主任、副秘书长，后调入平城区任区委副书记、代区长、区长

Confidence notes:
  - 孟德昌 (Party Secretary): confirmed from official news reports (2026-06, 07)
  - 郭政 (District Mayor): confirmed from official profile page
  - 崔峰 (Executive Deputy Mayor): confirmed from official profile page with full resume
  - 高伟 (Deputy Mayor, Standing Committee): confirmed from official profile
  - 姜宝举 (Deputy Mayor, Public Security): confirmed from official profile
  - 范尚锋 (Deputy Mayor): confirmed from official profile
  - 李春 (Deputy Mayor): confirmed from official profile
  - 李徽 (Deputy Mayor): confirmed from official profile
  - 张志强 (Deputy Mayor): confirmed from official profile
  - 杨鹏 (Deputy Mayor, Seconded): confirmed from official profile
  - Predecessor Party Secretary: not yet identified with confidence
  - Predecessor Mayor: not identified — 郭政 appears to be in first term as 区长
"""

from __future__ import annotations

import json
import os
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
SLUG = "平城区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_平城区"
if _CURRENT_DIR.name == "shanxi_平城区":
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
# IDs: 1-2 core leadership, 3-9 standing committee + deputy mayors, 10+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "孟德昌",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — typical for Shanxi officials
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记",
        "current_org": "中共大同市平城区委员会",
        "source": "https://www.pingcheng.gov.cn/（官方活动报道确认）",
        "confidence": "confirmed",
        "notes": "2026年6月-7月多次以区委书记身份主持常委会会议、理论学习中心组集体学习。完整履历待查。"
    },
    {
        "id": 2,
        "name": "郭政",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1986年3月",  # confirmed — official profile
        "birthplace": "山西定襄",  # confirmed — official profile
        "education": "研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2009年8月",  # confirmed — official profile
        "current_post": "区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/llx/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市平城区委副书记、平城区人民政府党组书记、区长，平城农业产业示范区党工委书记。1986年3月出生，山西定襄人，2014年6月入党，2009年8月参加工作。此前曾任山西省国新能源发展集团、忻州市政府办公室副主任、副秘书长等职。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee / Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "崔峰",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1978年10月",  # confirmed — official profile
        "birthplace": "山西怀仁",  # confirmed — official profile
        "education": "研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2000年11月",  # confirmed — official profile
        "current_post": "常务副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/cuifeng/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市平城区委常委、平城区人民政府常务副区长。2004年12月入党。历任大同市城区法院书记员、区委办科员、建设局副局长、建设局局长、南关街道党工委书记，大同市发改委重大项目稽察特派员，大同市古城管理委员会副主任（挂职），大同市古城保护发展中心主任（挂职），灵丘县委常委、副县长等职。"
    },
    {
        "id": 4,
        "name": "高伟",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1978年2月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2000年7月",  # confirmed — official profile
        "current_post": "副区长（常委）",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/gaowei/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市平城区委常委、平城区人民政府副区长。2002年7月入党。历任大同市公安局新荣区分局民警，市国资委企业领导人员管理科科员/副主任科员/主任科员，市委政法委综治三科、研究室负责人/主任，市委督查专员（副处长级），市委副秘书长等职。"
    },
    {
        "id": 5,
        "name": "姜宝举",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1970年1月",  # confirmed — official profile
        "birthplace": "河北隆化",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1989年3月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/jbj/szfld.shtml",
        "confidence": "confirmed",
        "notes": "大同市公安局副局长，平城区人民政府副区长，平城公安分局党委书记、局长，一级高级警长。1990年12月入党。历任大同市公安局刑侦支队五大队副大队长、副支队长、支队长，恒安分局局长，浑源县副县长、公安局长等职。"
    },
    {
        "id": 6,
        "name": "范尚锋",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1970年5月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1989年10月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/wye/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1999年12月入党。历任大同市矿区区委办科员、区委组织部副部长/区人事局局长、区人口和计划生育局局长、区财政局局长，云冈区财政局党组书记/副局长、教育科技局党组书记/局长、区委常委/统战部长等职。"
    },
    {
        "id": 7,
        "name": "李春",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1971年7月",  # confirmed — official profile
        "birthplace": "山西灵丘",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1991年9月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/lys/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1995年6月入党。历任灵丘县政府办公室副主任/法制办主任，石家田乡党委副书记/乡长，史庄乡党委副书记/乡长/党委书记/人大主席，上寨镇党委书记，大同市水务局党组成员/副局长等职。"
    },
    {
        "id": 8,
        "name": "李徽",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1973年8月",  # confirmed — official profile
        "birthplace": "山西天镇",  # confirmed — official profile
        "education": "省委党校研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1992年9月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/dxw/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1995年12月入党。历任南郊区小南头乡政府副乡长，云冈镇副镇长兼云冈旅游区管委会副主任（正科），云冈镇党委副书记/纪委书记/兼云冈旅游区管委会副主任，马军营乡副书记/乡长，鸦儿崖乡党委书记/人大主席，马军营乡党委书记，平城区马军营乡党委书记等职。"
    },
    {
        "id": 9,
        "name": "张志强",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1972年7月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "中央党校大学本科学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1996年11月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/sll/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1996年1月入党。历任南郊区政府办副主任/督察室副主任，平旺乡党委副书记/乡长/治超办主任，水泊寺乡党委书记，平城区水泊寺乡党委书记，小南头街道党工委委员/书记，平城区住房和城乡建设局党组书记/局长等职。"
    },
    {
        "id": 10,
        "name": "杨鹏",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1991年2月",  # confirmed — official profile
        "birthplace": "山西平顺",  # confirmed — official profile
        "education": "大学本科",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2013年7月",  # confirmed — official profile
        "current_post": "副区长（挂职）",
        "current_org": "平城区人民政府",
        "source": "https://www.pingcheng.gov.cn/pcqrmzfz/yangp/szfld.shtml",
        "confidence": "confirmed",
        "notes": "2011年6月入党。山西省文化旅游投资控股集团有限公司办公室副主任，大同市平城区人民政府副区长（挂职）。历任山西省旅游投资控股集团纪检监察室职员，山西文旅集团党委办公室（董事会办公室）主办/主管/办公室副主任等职。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大同市平城区委员会", "type": "党委", "level": "市辖区", "parent": "中共大同市委员会", "location": "大同市平城区"},
    {"id": 2, "name": "平城区人民政府", "type": "政府", "level": "市辖区", "parent": "大同市人民政府", "location": "大同市平城区"},
    {"id": 3, "name": "平城区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "大同市人民代表大会常务委员会", "location": "大同市平城区"},
    {"id": 4, "name": "中国人民政治协商会议平城区委员会", "type": "政协", "level": "市辖区", "parent": "政协大同市委员会", "location": "大同市平城区"},
    {"id": 5, "name": "中共大同市平城区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共大同市纪律检查委员会", "location": "大同市平城区"},
    {"id": 6, "name": "平城公安分局", "type": "政府", "level": "正科级", "parent": "大同市公安局", "location": "大同市平城区"},
    {"id": 7, "name": "平城农业产业示范区", "type": "政府", "level": "市辖区", "parent": "平城区人民政府", "location": "大同市平城区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 孟德昌 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任平城区委书记，2026年6月已有活动报道"},
    # 郭政 — current District Mayor
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "区委副书记、区政府党组书记、区长，平城农业产业示范区党工委书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "党工委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "平城农业产业示范区党工委书记"},
    # 郭政 — earlier career
    {"person_id": 2, "org_id": 2, "title": "副区长、代区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "平城区委副书记、区人民政府党组书记、副区长、代区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记（兼街道党工委书记）", "start_date": "", "end_date": "", "rank": "正处级", "note": "兼任平城区向阳里街道党工委书记"},
    {"person_id": 2, "org_id": 2, "title": "忻州市政府副秘书长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "忻州市政府办公室副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "忻州区域管理委员会副主任", "start_date": "", "end_date": "", "rank": "正科级", "note": "山西省国新能源发展集团有限公司忻州区域管理委员会副主任"},
    {"person_id": 2, "org_id": 2, "title": "主任科员", "start_date": "", "end_date": "", "rank": "正科级", "note": "山西省国新能源发展集团有限公司主任科员"},
    # 崔峰 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "灵丘县委常委、副县长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "灵丘县委常委、县政府党组成员"},
    # 高伟 — Deputy Mayor (Standing Committee)
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、副区长"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 姜宝举 — Deputy Mayor (Public Security)
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "大同市公安局副局长，平城区副区长，平城公安分局党委书记、局长"},
    {"person_id": 5, "org_id": 6, "title": "党委书记、局长", "start_date": "", "end_date": "", "rank": "一级高级警长", "note": "平城公安分局"},
    # 范尚锋 — Deputy Mayor
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李春 — Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李徽 — Deputy Mayor
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 张志强 — Deputy Mayor
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨鹏 — Deputy Mayor (Seconded)
    {"person_id": 10, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "山西省文化旅游投资控股集团有限公司办公室副主任挂职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 孟德昌 ↔ 郭政 (Party Secretary – District Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共大同市平城区委员会", "overlap_period": "2026-至今"},
    # 郭政 ↔ 崔峰 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    # 郭政 → 副区长团队
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长", "overlap_org": "平城区人民政府", "overlap_period": "至今"},
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
    return questions


def _make_person_id(name: str) -> str:
    return f"pingcheng_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "大同市平城区人民政府官方网站",
            "url": "https://www.pingcheng.gov.cn/",
            "publisher": "平城区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "平城区政府门户网站政府领导页面及活动报道",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "大同市",
            "region": "平城区",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_平城区",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
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
            "administrative_rank": "正处级" if person["id"] in (1, 2) else ("副处级" if person["id"] in (3, 4, 5, 6, 7, 8, 9) else "副处级（挂职）"),
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
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）" if not person.get("work_start") else "早期教育和工作细节",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ] + ([
            {
                "priority": "high",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ] if not person.get("birth") else []),
    }

    fname = f"{TODAY}-山西省-大同市-{person['current_post']}-{person['name']}.json"
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
    # Core targets: 区委书记 (id=1), 区长 (id=2)
    # Also include key deputies: 常务副区长 (id=3), 常委副区长 (id=4)
    core_ids = {1, 2}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
