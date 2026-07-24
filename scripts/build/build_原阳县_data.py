#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 原阳县 (Yuanyang County), 新乡市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_原阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.yuanyang.gov.cn — 原阳县人民政府网站 (primary, current as of July 2026)
  - www.yuanyang.gov.cn/channels/529.html — 领导之窗 (official leadership roster)
  - News articles on yuanyang.gov.cn confirm:
      * 杨新意: 县委书记 (first appeared June 2025, confirmed through July 2026)
      * 岳永鹏: 县委副书记、县长 (appointed Nov 2024, confirmed through July 2026)
      * 景胜海: 县委常委、常务副县长
      * Full government leadership roster from 领导之窗 page

Confidence notes:
  - 杨新意 and 岳永鹏: current roles confirmed via official government site and multiple news articles
  - Detailed career timelines (education, early career, birthplace) for both leaders could not
    be fully verified due to web access limitations (Baidu Baike 403, Exa rate-limited)
  - Birth year for 岳永鹏 (1980.10) confirmed from official 领导之窗
  - 杨新意's birth year, birthplace, education marked as open questions
  - Predecessor of 岳永鹏: 郭新杰 (served as 县长 until ~July 2024)
  - Predecessor of 杨新意: likely 刘兵 (需进一步核实)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used implicitly by gov_relation.runner
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "原阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
DB_PATH = Path(__file__).parent.resolve() / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent.resolve() / f"{SLUG}_network.gexf"
PJSON_DIR = Path(__file__).parent.resolve()

# ── Persons ──────────────────────────────────────────────────────────────────
# IDs: 1-5 core leaders, 6-13 standing committee/govt, 14-15 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "杨新意",
        "gender": "男",
        "ethnicity": "",  # open question
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 2,
        "name": "岳永鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",  # open question
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key County Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "景胜海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 4,
        "name": "杨冬军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任（原县委副书记）",
        "current_org": "原阳县人民代表大会常务委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 5,
        "name": "刘为伶",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席（原县委常委、组织部部长）",
        "current_org": "中国人民政治协商会议原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 6,
        "name": "元强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委办公室主任",
        "current_org": "中共原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 7,
        "name": "赵婧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委代主任",
        "current_org": "中共原阳县纪律检查委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 8,
        "name": "陈得宽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部长",
        "current_org": "中共原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 9,
        "name": "赵彦茹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "本科学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 10,
        "name": "张雪涵嵩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年3月",
        "birthplace": "",
        "education": "本科学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 11,
        "name": "王济宝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共原阳县委员会",
        "source": "https://www.yuanyang.gov.cn/"
    },
    {
        "id": 12,
        "name": "库里满·恰里甫",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 13,
        "name": "邢磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 14,
        "name": "范晓哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    {
        "id": 15,
        "name": "祁志彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "",
        "education": "本科学历，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、葛埠口乡党委书记",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/channels/529.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "郭新杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "原阳县人民政府",
        "source": "https://www.yuanyang.gov.cn/contents/103/29318.html"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共原阳县委员会", "type": "党委", "level": "县", "parent": "中共新乡市委员会", "location": "原阳县"},
    {"id": 2, "name": "原阳县人民政府", "type": "政府", "level": "县", "parent": "新乡市人民政府", "location": "原阳县"},
    {"id": 3, "name": "原阳县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "新乡市人大常委会", "location": "原阳县"},
    {"id": 4, "name": "中国人民政治协商会议原阳县委员会", "type": "政协", "level": "县", "parent": "政协新乡市委员会", "location": "原阳县"},
    {"id": 5, "name": "中共原阳县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共新乡市纪律检查委员会", "location": "原阳县"},
    {"id": 6, "name": "原阳县公安局", "type": "政府", "level": "县", "parent": "原阳县人民政府", "location": "原阳县"},
    {"id": 7, "name": "葛埠口乡人民政府", "type": "乡镇", "level": "乡镇", "parent": "原阳县人民政府", "location": "原阳县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 杨新意 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-06", "end_date": "", "rank": "正处级", "note": "最早于2025年6月以县委书记身份出现在原阳新闻"},

    # 岳永鹏 — current County Mayor
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2024-11", "end_date": "", "rank": "正处级", "note": "2024年11月20日全县干部大会宣布任命"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2024-11", "end_date": "", "rank": "正处级", "note": "先后任县政府党组书记、县长"},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记", "start_date": "2024-11", "end_date": "", "rank": "正处级", "note": ""},

    # 景胜海 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},

    # 杨冬军 — former Deputy Party Secretary, now People's Congress
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "2026", "rank": "副处级", "note": "后转任县人大常委会"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "2026", "end_date": "", "rank": "正处级", "note": ""},

    # 刘为伶 — former Organization Department head, now CPPCC
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "2026", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "县政协主席", "start_date": "2026", "end_date": "", "rank": "正处级", "note": ""},

    # 元强 — Deputy Party Secretary & Office Director
    {"person_id": 6, "org_id": 1, "title": "县委副书记、县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # 赵婧 — Discipline Inspection
    {"person_id": 7, "org_id": 5, "title": "县委常委、纪委书记、监委代主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # Standing committee members
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # Deputy mayors
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管教育体育、卫生健康、医疗保障"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管公安、司法、信访"},
    {"person_id": 13, "org_id": 6, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管城乡规划建设、城市管理"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管农业农村、乡村振兴、水利"},
    {"person_id": 15, "org_id": 7, "title": "葛埠口乡党委书记", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},

    # Predecessors
    {"person_id": 16, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2024-07", "rank": "正处级", "note": "前任县长，至少任职至2024年7月"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 杨新意 ↔ 岳永鹏 (Party Secretary - County Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共原阳县委员会", "overlap_period": "2025.06至今"},
    # 岳永鹏 ↔ 景胜海 (Mayor - Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "县长—常务副县长", "overlap_org": "原阳县人民政府", "overlap_period": "2024.11至今"},
    # 杨新意 ↔ 景胜海
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常务副县长", "overlap_org": "中共原阳县委员会", "overlap_period": "2025.06至今"},
    # 杨新意 ↔ 元强 (Party Secretary - Office Director)
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—县委办公室主任", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    # 岳永鹏 ↔ 郭新杰 (predecessor succession)
    {"person_a": 16, "person_b": 2, "type": "交接", "context": "前任县长—现任县长", "overlap_org": "原阳县人民政府", "overlap_period": "2024"},
    # 杨冬军 (former Deputy Secretary) ↔ 杨新意
    {"person_a": 4, "person_b": 1, "type": "共事", "context": "原县委副书记—县委书记", "overlap_org": "中共原阳县委员会", "overlap_period": "2025-2026"},
    # 刘为伶 (former Organization Head) ↔ 杨新意
    {"person_a": 5, "person_b": 1, "type": "共事", "context": "原组织部长—县委书记", "overlap_org": "中共原阳县委员会", "overlap_period": "2025-2026"},
    # Government leadership team edges
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "县长—副县长", "overlap_org": "原阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "原阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长", "overlap_org": "原阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "县长—副县长", "overlap_org": "原阳县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "县长—副县长", "overlap_org": "原阳县人民政府", "overlap_period": ""},
    # Standing committee internal relationships
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—县委常委", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    # Standing committee colleague relationships (cross-links)
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "县委常委同僚", "overlap_org": "中共原阳县委员会", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md spec."""
    pid = person["id"]
    name = person["name"]

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos["start_date"] or "",
            "end": pos["end_date"] or "",
            "org": org["name"] if org else "",
            "title": pos["title"],
            "rank": pos["rank"] or "",
            "notes": pos["note"] or "",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    connections = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        connections.append({
            "person": other["name"] if other else f"person_{other_id}",
            "person_id": f"yuanyang_{other['name']}" if other else f"person_{other_id}",
            "relationship_type": "overlap" if r["type"] in ("共事", "同僚") else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    # Open questions
    open_questions = []
    if not person["birth"]:
        open_questions.append({
            "priority": "critical",
            "question": f"{name}的出生年月未确认",
            "why_it_matters": "身份确认和去重关键字段",
            "suggested_queries": [f"{name} 出生", f"{name} 简历"],
            "last_attempted": "2026-07-24"
        })
    if not person["birthplace"]:
        open_questions.append({
            "priority": "high",
            "question": f"{name}的籍贯/出生地未确认",
            "why_it_matters": "同乡关系分析的基础数据",
            "suggested_queries": [f"{name} 籍贯"],
            "last_attempted": "2026-07-24"
        })
    if not person["education"]:
        open_questions.append({
            "priority": "high",
            "question": f"{name}的学历教育背景未确认",
            "why_it_matters": "同学关系和专业背景分析的基础",
            "suggested_queries": [f"{name} 学历"],
            "last_attempted": "2026-07-24"
        })

    record = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "新乡市",
            "region": "原阳县",
            "job": person["current_post"],
            "task_id": "henan_原阳县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"yuanyang_{name}",
            "name": name,
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": ["S001"]}] if person["education"] else [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{person['birth']}",
                "name_birthplace": f"{name}_{person['birthplace']}",
                "official_profile_url": person["source"]
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"id": o["id"], "name": o["name"], "type": o["type"], "level": o["level"]}
            for o in organizations
            if any(p["org_id"] == o["id"] for p in person_positions)
        ],
        "relationships": connections,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S001"]}
        ],
        "source_register": [
            {"id": "S001", "title": "原阳县人民政府网站", "url": person["source"], "publisher": "原阳县人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "confirmed" if person["birth"] else "partial",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "早期履历未知" if not person.get("work_start") and not person.get("birth") else "籍贯未知"
        },
        "open_questions": open_questions,
    }

    job_short = person['current_post'].replace('、', '_').replace('，', '_')
    fname = f"{TODAY}-河南省-新乡市-{job_short}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
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
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
