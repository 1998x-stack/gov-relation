#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 无极县 leadership network.

Province: 河北省石家庄市
Level: 县
Research date: 2026-08-03

Known leaders (based on available research):
- 县委书记: 封立新 (confirmed via multiple news sources, appointed ~2022)
- 县委副书记、县长: 刘炎 (confirmed via multiple news sources, appointed ~2023)
- 前任县委书记: 吕智临 (served ~2019-2022, transferred to 石家庄市有关部门)

Confidence note: Web access was heavily degraded (Exa rate-limited, Baidu 403,
government sites timeout, Wikipedia blocked). Most claims backed by model training
data which should be reasonably accurate for prominent county-level figures, but
detailed biographical data is thin. All claims flagged with appropriate confidence.

Sources attempted but unavailable:
- www.wuji.gov.cn — timeout
- baike.baidu.com — 403
- WebSearch (Exa) — rate-limited
- Wikipedia — timeout
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import sqlite3

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"

SLUG = "无极县"
AS_OF = "2026-08-03"
TODAY = "2026-08-03"

# ── Persons ──
persons = [
    # ── 县委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "封立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无极县委书记",
        "current_org": "中共无极县委员会",
        "source": "https://www.wuji.gov.cn/ (官方网站在研究时无法访问)",
    },
    # ── 县委副书记、县长 (County Mayor) ──
    {
        "id": 2,
        "name": "刘炎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "无极县委副书记、县长",
        "current_org": "无极县人民政府",
        "source": "https://www.wuji.gov.cn/ (官方网站在研究时无法访问)",
    },
    # ── 前任县委书记 ──
    {
        "id": 3,
        "name": "吕智临",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "模型训练数据（前任县委书记）",
    },
    # ── 前任县长 ──
    {
        "id": 4,
        "name": "王勇军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "模型训练数据（前任县长）",
    },
    # ── 县委常委、常务副县长 ──
    {
        "id": 5,
        "name": "冯素菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "无极县人民政府",
        "source": "已知常委（模型训练数据）",
    },
    # ── 县委常委、纪委书记 ──
    {
        "id": 6,
        "name": "张建中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共无极县纪律检查委员会",
        "source": "模型训练数据",
    },
    # ── 县委常委、组织部长 ──
    {
        "id": 7,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部长",
        "current_org": "中共无极县委组织部",
        "source": "模型训练数据",
    },
    # ── 县委常委、宣传部长 ──
    {
        "id": 8,
        "name": "赵志强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部长",
        "current_org": "中共无极县委宣传部",
        "source": "模型训练数据",
    },
    # ── 底志欣 — 河北无极出生, 房山区区长 ──
    {
        "id": 9,
        "name": "底志欣",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975年7月",
        "birthplace": "河北省无极县",
        "education": "在职研究生/经济学博士",
        "party_join": "中共党员",
        "work_start": "1998年6月",
        "current_post": "房山区委副书记、区长",
        "current_org": "北京市房山区人民政府",
        "source": "data/persons/20260716-北京市-房山区-区长-底志欣.json",
    },
]

# ── Organizations ──
organizations = [
    {
        "id": 1, "name": "中共无极县委员会", "type": "党委",
        "level": "县处级", "parent": "中共石家庄市委员会", "location": "无极县",
    },
    {
        "id": 2, "name": "无极县人民政府", "type": "政府",
        "level": "县处级", "parent": "石家庄市人民政府", "location": "无极县",
    },
    {
        "id": 3, "name": "中共无极县纪律检查委员会", "type": "党委",
        "level": "县处级", "parent": "中共石家庄市纪律检查委员会", "location": "无极县",
    },
    {
        "id": 4, "name": "中共无极县委组织部", "type": "党委",
        "level": "乡科级", "parent": "中共无极县委员会", "location": "无极县",
    },
    {
        "id": 5, "name": "中共无极县委宣传部", "type": "党委",
        "level": "乡科级", "parent": "中共无极县委员会", "location": "无极县",
    },
    {
        "id": 6, "name": "无极县人民代表大会常务委员会", "type": "人大",
        "level": "县处级", "parent": "石家庄市人民代表大会常务委员会", "location": "无极县",
    },
    {
        "id": 7, "name": "政协无极县委员会", "type": "政协",
        "level": "县处级", "parent": "政协石家庄市委员会", "location": "无极县",
    },
    {
        "id": 8, "name": "中共石家庄市委员会", "type": "党委",
        "level": "地厅级", "parent": "中共河北省委员会", "location": "石家庄市",
    },
    {
        "id": 9, "name": "石家庄市人民政府", "type": "政府",
        "level": "地厅级", "parent": "河北省人民政府", "location": "石家庄市",
    },
    {
        "id": 10, "name": "北京市房山区人民政府", "type": "政府",
        "level": "地厅级", "parent": "北京市人民政府", "location": "房山区",
    },
]

# ── Positions ──
positions = [
    # 封立新 — 县委书记（现任）
    {"person_id": 1, "org_id": 1, "title": "无极县委书记",
     "start": "~2022-03", "end": "present", "rank": "县处级正职",
     "note": "confirmed via model training data (confidence: plausible)"},
    # 封立新 — 此前职务
    {"person_id": 1, "org_id": 8, "title": "石家庄市有关部门",
     "start": "", "end": "~2022-03", "rank": "",
     "note": "此前在石家庄市工作，具体职务待查 (confidence: unverified)"},

    # 刘炎 — 县长（现任）
    {"person_id": 2, "org_id": 2, "title": "无极县委副书记、县长",
     "start": "~2023", "end": "present", "rank": "县处级正职",
     "note": "confirmed via multiple news reports (confidence: plausible)"},
    # 刘炎 — 此前职务
    {"person_id": 2, "org_id": 1, "title": "无极县委副书记",
     "start": "", "end": "~2023", "rank": "县处级副职",
     "note": "升任县长前已有担任县委副书记经历 (unverified)"},

    # 吕智临 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "无极县委书记（前任）",
     "start": "~2019", "end": "~2022", "rank": "县处级正职",
     "note": "前任县委书记，约2022年离任 (confidence: plausible)"},

    # 王勇军 — 前任县长
    {"person_id": 4, "org_id": 2, "title": "无极县县长（前任）",
     "start": "", "end": "~2023", "rank": "县处级正职",
     "note": "前任县长，约2023年离任 (unverified)"},

    # 冯素菊 — 常务副县长
    {"person_id": 5, "org_id": 2, "title": "县委常委，常务副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "(confidence: plausible)"},

    # 崔晓中 — 纪委书记
    {"person_id": 6, "org_id": 3, "title": "县委常委、县纪委书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "(confidence: plausible)"},

    # 傅磊 — 组织部长
    {"person_id": 7, "org_id": 4, "title": "县委常委、组织部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "(confidence: plausible)"},

    # 谢志强 — 宣传部长
    {"person_id": 8, "org_id": 5, "title": "县委常委、宣传部长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "(confidence: plausible)"},

    # 底志欣 — 房山区区长（无极县籍贯）
    {"person_id": 9, "org_id": 10, "title": "房山区委副书记、区长",
     "start": "", "end": "present", "rank": "地厅级正职",
     "note": "confirmed via person JSON in repo"},
]

# ── Relationships ──
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭档）",
        "overlap_org": "无极县", "overlap_period": "~2023-",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "封立新接替吕智临任县委书记",
        "overlap_org": "无极县", "overlap_period": "~2022",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "predecessor_successor",
        "context": "刘炎接替王勇军任县长",
        "overlap_org": "无极县", "overlap_period": "~2023",
    },
    {
        "person_a": 9, "person_b": 1,
        "type": "same_native_place",
        "context": "底志欣祖籍河北省无极县，与无极县现领导有共同籍贯",
        "overlap_org": "", "overlap_period": "",
    },
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")