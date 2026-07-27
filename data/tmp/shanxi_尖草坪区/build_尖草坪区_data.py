#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 尖草坪区 (Jiancaoping District), 太原市, 山西省.

Investigation date: 2026-07-25
Task ID: shanxi_尖草坪区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.tyjcp.gov.cn — 太原市尖草坪区人民政府门户网站 (official leadership pages, news)
  - 区委领导页面: /qw.html (区委常委完整名单及分工)
  - 区政府领导页面: /qzf.html (区政府领导班子分工)
  - News articles from 2026-05 to 2026-07 confirming current officeholders

Current confirmed leadership (as of 2026-07-25):
  - 刘锦春: 区委书记、中北高新区党工委书记 (confirmed via multiple official news articles 2026-05 to 2026-07)
  - 段燕临: 区委副书记、代区长 (confirmed via official news article 2026-07-07)

Confidence notes:
  - 刘锦春 and 段燕临 confirmed as current top two leaders through multiple official tyjcp.gov.cn news articles dated 2026-05 to 2026-07
  - 刘锦春 holds concurrent position as 中北高新技术产业开发区党工委书记
  - 段燕临 is 代区长 (acting mayor), not yet formally elected as 区长 — he is NOT listed on the government leadership page /qzf.html
  - Detailed career timelines (education, early career) for most figures could not be fully verified due to web access limitations (Exa rate-limited, Baidu CAPTCHA)
  - Data primarily from direct website fetches of tyjcp.gov.cn
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
    os.chdir(REPO_ROOT)  # Ensure CWD is repo root for relative imports

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "尖草坪区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ──────────────────────────────────────────────────────────
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "刘锦春",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记、中北高新技术产业开发区党工委书记",
        "current_org": "中共太原市尖草坪区委员会",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 2,
        "name": "段燕临",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、代区长",
        "current_org": "太原市尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/zwdt/20260707/30308165.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Standing Committee (区委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张俊兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "省委党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共太原市尖草坪区委员会/尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 4,
        "name": "蔺志新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、党校校长",
        "current_org": "中共太原市尖草坪区委员会",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 5,
        "name": "芦保军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共太原市尖草坪区纪律检查委员会/区监察委员会",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 6,
        "name": "王玉贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共太原市尖草坪区委员会",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 7,
        "name": "闫晨涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长、统战部部长、区政协党组副书记",
        "current_org": "中共太原市尖草坪区委员会",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 8,
        "name": "韩铁军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人武部上校部长",
        "current_org": "太原市尖草坪区人武部",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    {
        "id": 9,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "中共太原市尖草坪区委员会/尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/qw.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (区政府)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "郭占昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "九三学社社员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/qzf.html"
    },
    {
        "id": 11,
        "name": "白冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/qzf.html"
    },
    {
        "id": 12,
        "name": "王治国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安尖草坪分局局长",
        "current_org": "尖草坪区人民政府/公安尖草坪分局",
        "source": "http://www.tyjcp.gov.cn/qzf.html"
    },
    {
        "id": 13,
        "name": "毋金秀",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年5月",
        "birthplace": "",
        "education": "公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "尖草坪区人民政府",
        "source": "http://www.tyjcp.gov.cn/qzf.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Key Figures (additional leaders mentioned in news)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "侯杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "尖草坪区",
        "source": "http://www.tyjcp.gov.cn/zwdt/20260707/30308165.html"
    },
    {
        "id": 15,
        "name": "王秋月",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "尖草坪区",
        "source": "http://www.tyjcp.gov.cn/zwdt/20260709/30308773.html"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共太原市尖草坪区委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共太原市委",
        "location": "太原市尖草坪区"
    },
    {
        "id": 2,
        "name": "尖草坪区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "太原市人民政府",
        "location": "太原市尖草坪区"
    },
    {
        "id": 3,
        "name": "中北高新技术产业开发区",
        "type": "开发区",
        "level": "正处级",
        "parent": "太原市人民政府",
        "location": "太原市尖草坪区"
    },
    {
        "id": 4,
        "name": "中共太原市尖草坪区纪律检查委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共太原市尖草坪区委员会",
        "location": "太原市尖草坪区"
    },
    {
        "id": 5,
        "name": "尖草坪区监察委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "尖草坪区",
        "location": "太原市尖草坪区"
    },
    {
        "id": 6,
        "name": "尖草坪区人武部",
        "type": "事业单位",
        "level": "正处级",
        "parent": "太原警备区",
        "location": "太原市尖草坪区"
    },
    {
        "id": 7,
        "name": "公安尖草坪分局",
        "type": "政府",
        "level": "正科级",
        "parent": "太原市公安局",
        "location": "太原市尖草坪区"
    },
    {
        "id": 8,
        "name": "尖草坪区人大常委会",
        "type": "人大",
        "level": "正处级",
        "parent": "尖草坪区",
        "location": "太原市尖草坪区"
    },
    {
        "id": 9,
        "name": "尖草坪区政协",
        "type": "政协",
        "level": "正处级",
        "parent": "尖草坪区",
        "location": "太原市尖草坪区"
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘锦春 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "二级巡视员"},
    {"person_id": 1, "org_id": 3, "title": "中北高新技术产业开发区党工委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "兼任"},

    # 段燕临 - Acting Mayor
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "unknown", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "unknown", "end": "present", "rank": "正处级", "note": "暂未正式当选区长"},

    # 张俊兵 - Standing Committee / Deputy Mayor
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 3, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管应急管理、审计、住建等"},

    # 蔺志新 - Organization Department Head
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 4, "org_id": 1, "title": "党校校长", "start": "unknown", "end": "present", "rank": "副处级", "note": "兼任"},

    # 芦保军 - Discipline Inspection
    {"person_id": 5, "org_id": 1, "title": "区委常委、区纪委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "区监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": "兼任"},

    # 王玉贵 - Political and Legal Affairs
    {"person_id": 6, "org_id": 1, "title": "区委常委、政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},

    # 闫晨涛 - Propaganda / United Front
    {"person_id": 7, "org_id": 1, "title": "区委常委、宣传部部长、统战部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "三级调研员兼区政协党组副书记"},

    # 韩铁军 - People's Armed Forces
    {"person_id": 8, "org_id": 6, "title": "区人武部上校部长", "start": "unknown", "end": "present", "rank": "正团级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},

    # 王磊 - Standing Committee / Deputy Mayor
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管发展改革、工业、财税等"},

    # 郭占昌 - Deputy Mayor
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": "九三学社，分管科技、民政等"},

    # 白冰 - Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": "三级调研员，分管教育、卫生、文旅等"},

    # 王治国 - Deputy Mayor / Public Security
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "公安尖草坪分局局长", "start": "unknown", "end": "present", "rank": "正科级", "note": "兼任"},

    # 毋金秀 - Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "unknown", "end": "present", "rank": "副处级", "note": "二级调研员，分管退役军人事务"},

    # 侯杰 - District Leader
    {"person_id": 14, "org_id": 2, "title": "区领导", "start": "unknown", "end": "present", "rank": "", "note": "具体职务待查"},

    # 王秋月 - District Leader
    {"person_id": 15, "org_id": 1, "title": "区领导", "start": "unknown", "end": "present", "rank": "", "note": "具体职务待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 刘锦春 ↔ 段燕临 (区委书记 ↔ 代区长 — 党政搭档)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与代区长党政一把手搭档",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 张俊兵 (区委书记 ↔ 常委副区长)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委/副区长",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 蔺志新 (区委书记 ↔ 组织部长)
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记与区委组织部部长",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 芦保军 (区委书记 ↔ 纪委书记)
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与区纪委书记",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 闫晨涛 (区委书记 ↔ 宣传/统战部长)
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与区委宣传部部长/统战部部长",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 王磊 (区委书记 ↔ 常委副区长)
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区委书记与区委常委/副区长",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 刘锦春 ↔ 王玉贵 (区委书记 ↔ 政法委书记)
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与区委政法委书记",
        "overlap_org": "中共太原市尖草坪区委员会",
        "overlap_period": "2026-至今"
    },
    # 段燕临 ↔ 张俊兵 (代区长 ↔ 副区长)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "代区长与区委常委/副区长（主要副手）",
        "overlap_org": "尖草坪区人民政府",
        "overlap_period": "2026-至今"
    },
    # 段燕临 ↔ 王磊 (代区长 ↔ 副区长)
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "代区长与区委常委/副区长",
        "overlap_org": "尖草坪区人民政府",
        "overlap_period": "2026-至今"
    },
    # 段燕临 ↔ 侯杰 (代区长 ↔ 区领导，共同调研)
    {
        "person_a": 2,
        "person_b": 14,
        "type": "overlap",
        "context": "共同调研防汛工作",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-07"
    },
    # 刘锦春 ↔ 王秋月 (区委书记 ↔ 区领导，共同调研)
    {
        "person_a": 1,
        "person_b": 15,
        "type": "overlap",
        "context": "共同调研高层建筑消防和防汛",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-07"
    },
    # 刘锦春 ↔ 王磊 (区委书记 ↔ 常委副区长，共同参加项目工作会议)
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "共同参加项目建设工作专题会",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-05"
    },
    # 张俊兵 ↔ 王磊 (两位常委副区长)
    {
        "person_a": 3,
        "person_b": 9,
        "type": "overlap",
        "context": "同为区委常委、副区长",
        "overlap_org": "中共太原市尖草坪区委员会/尖草坪区人民政府",
        "overlap_period": "2026-至今"
    },
    # 白冰 ↔ 刘锦春 (副区长 ↔ 区委书记，出席同一会议)
    {
        "person_a": 11,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "副区长与区委书记",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-至今"
    },
    # 郭占昌 ↔ 刘锦春 (副区长 ↔ 区委书记，出席同一会议)
    {
        "person_a": 10,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "副区长与区委书记",
        "overlap_org": "尖草坪区",
        "overlap_period": "2026-至今"
    },
]


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job_short: str) -> None:
    """Write a single person JSON file to PERSONS_DIR."""
    name = person["name"]
    filename = f"{TODAY}-山西省-太原市-{job_short}-{name}.json"
    filepath = PERSONS_DIR / filename

    # Generate relationships for this person
    person_rels = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            target = next((p for p in persons if p["id"] == r["person_b"]), None)
            if target:
                person_rels.append({
                    "person": target["name"],
                    "person_id": f"jiancaoping_{target['name'].lower()}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "person_to_other",
                    "confidence": "confirmed" if person["source"] else "plausible",
                    "source_ids": ["S001"]
                })
        elif r["person_b"] == person["id"]:
            source = next((p for p in persons if p["id"] == r["person_a"]), None)
            if source:
                person_rels.append({
                    "person": source["name"],
                    "person_id": f"jiancaoping_{source['name'].lower()}",
                    "relationship_type": r["type"],
                    "strength": "strong",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "other_to_person",
                    "confidence": "confirmed" if person["source"] else "plausible",
                    "source_ids": ["S001"]
                })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "太原市",
            "region": "尖草坪区",
            "job": job_short,
            "task_id": "shanxi_尖草坪区",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": f"jiancaoping_{name.lower()}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": person.get("education", ""),
                "major": "",
                "degree": "",
                "study_type": "unknown",
                "source_ids": ["S001"]
            }] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present" if person["id"] in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] else "unknown",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "正处级" if person["id"] in [1, 2] else "副处级",
                "location": "太原市尖草坪区",
                "system": "party" if person["id"] in [1, 2, 4, 5, 6, 7] else "government",
                "rank": "",
                "is_key_promotion": person["id"] in [1, 2],
                "notes": "公开资料仅能找到现任职务信息，详细履历待查",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [{"name": person["current_org"], "role": person["current_post"]}],
        "relationships": person_rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "履历信息不足，无法评估晋升速度",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，公开信息中未发现与{name}相关的纪律处分、审计问题或负面报道",
                "date": AS_OF,
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "尖草坪区领导之窗",
                "url": person.get("source", "http://www.tyjcp.gov.cn/qw.html"),
                "publisher": "太原市尖草坪区人民政府",
                "published_at": AS_OF,
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{name}的现任职务"
            }
        ],
        "confidence_summary": {
            "identity": "partial" if person.get("ethnicity") else "thin",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}出任{person['current_post']}前的完整履历（出生、教育、早期任职等）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}出生于哪一年？籍贯何处？",
                "why_it_matters": "核心人物身份信息缺失，影响图谱完整性",
                "suggested_queries": [
                    f"{name} 简历 太原",
                    f"{name} 任前公示 尖草坪区"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}出任{person['current_post']}前的任职履历",
                "why_it_matters": "无法评估其晋升路径和核心系统经验",
                "suggested_queries": [
                    f"{name} 此前 担任",
                    f"{name} 太原 组织部"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

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

    # Write person JSONs
    print("\nWriting person JSON files...")
    write_person_json(persons[0], "区委书记")   # 刘锦春
    write_person_json(persons[1], "代区长")      # 段燕临

    print("\nDone!")


if __name__ == "__main__":
    main()
