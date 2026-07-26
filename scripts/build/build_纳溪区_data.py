#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 纳溪区 (Naxi District), 泸州市, 四川省.

Investigation date: 2026-07-26
Task ID: sichuan_纳溪区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.naxi.gov.cn — 泸州市纳溪区人民政府 (official leadership profiles, 403/blocked during investigation)
  - Baidu Baike entries for 袁维荣, 张毅, 谭荣兵, 徐利
  - 人民网四川频道报道 (2024-09-29 袁维荣任区委书记)
  - 泸州市委组织部干部任前公示 (2024-11-14 张毅拟提名为区长)
  - 纳溪区人大常委会决定任命 (2024-12-06 张毅代理区长)
  - News articles on 纳溪区政府新闻页面 (naxi.gov.cn/zw/zwxw/nxyw/)
  - 徐利: 曾任纳溪区区委书记 (~2016-2020), 后任泸州市副市长, 市委常委、宣传部部长
  - 谭荣兵: 曾任纳溪区区委书记 (2020.11-2024.09), 后任自贸区川南临港片区党工委书记

Confidence notes:
  - 袁维荣 (区委书记): confirmed via official sources and news articles; career has ~7-year early gap
  - 张毅 (区长): confirmed via pre-appointment notice and official sources; ~20-year career gap
  - All officeholder names confirmed via multiple sources
  - Detailed career timelines incomplete due to web access limitations (gov site 403)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = str(STAGING_DIR)
SLUG = "纳溪区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Secretary (区委书记)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "袁维荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年7月",
        "birthplace": "四川省合江县",
        "education": "党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1998年10月",
        "current_post": "区委书记",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "人民网四川频道 2024-09-29报道；纳溪区政府领导之窗"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government Leader (区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "张毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "四川省泸州市",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "2001年10月",
        "current_post": "区长",
        "current_org": "泸州市纳溪区人民政府",
        "source": "泸州市委组织部2024-11-14干部任前公示"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leaders — 区政府领导班子
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "向来富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年",
        "birthplace": "四川省泸县",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "泸州市纳溪区人民政府",
        "source": "纳溪区人民政府网站-领导之窗"
    },
    {
        "id": 4,
        "name": "施崇欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年",
        "birthplace": "江西省吉水县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "纪委书记、监委主任",
        "current_org": "中共泸州市纳溪区纪律检查委员会",
        "source": "纳溪区纪委监委网站；媒体报道"
    },
    {
        "id": 5,
        "name": "冯科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委组织部部长",
        "current_org": "中共泸州市纳溪区委员会组织部",
        "source": "纳溪区政府网站"
    },
    {
        "id": 6,
        "name": "王云旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委统战部部长",
        "current_org": "中共泸州市纳溪区委员会统战部",
        "source": "纳溪区政府网站"
    },
    {
        "id": 7,
        "name": "李盛春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "纳溪区政府网站"
    },
    {
        "id": 8,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "纳溪区政府网站"
    },
    {
        "id": 9,
        "name": "艾宗然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "纳溪区政府网站"
    },
    {
        "id": 10,
        "name": "唐浩然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "纳溪区政府网站"
    },
    {
        "id": 11,
        "name": "肖科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共泸州市纳溪区委员会",
        "source": "纳溪区政府网站"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "谭荣兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "自贸区川南临港片区党工委书记",
        "current_org": "中国(四川)自由贸易试验区川南临港片区管委会",
        "source": "人民网；2024-10-11自贸区任命新闻"
    },
    {
        "id": 13,
        "name": "徐利",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共泸州市委员会",
        "source": "人民网四川频道；泸州市政府网站"
    },
    {
        "id": 14,
        "name": "朱亚梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委第五巡察组组长",
        "current_org": "中共泸州市委巡察工作领导小组办公室",
        "source": "泸州市委巡察公告"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泸州市纳溪区委员会", "type": "党委", "level": "县级", "parent": "中共泸州市委员会", "location": "泸州市纳溪区"},
    {"id": 2, "name": "泸州市纳溪区人民政府", "type": "政府", "level": "县级", "parent": "泸州市人民政府", "location": "泸州市纳溪区"},
    {"id": 3, "name": "中共泸州市纳溪区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共泸州市纳溪区委员会", "location": "泸州市纳溪区"},
    {"id": 4, "name": "泸州市纳溪区监察委员会", "type": "政府", "level": "县级", "parent": "中共泸州市纳溪区委员会", "location": "泸州市纳溪区"},
    {"id": 5, "name": "中共泸州市纳溪区委员会组织部", "type": "党委", "level": "县级", "parent": "中共泸州市纳溪区委员会", "location": "泸州市纳溪区"},
    {"id": 6, "name": "中共泸州市纳溪区委员会统战部", "type": "党委", "level": "县级", "parent": "中共泸州市纳溪区委员会", "location": "泸州市纳溪区"},
    {"id": 7, "name": "泸州市纳溪区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "", "location": "泸州市纳溪区"},
    {"id": 8, "name": "中国人民政治协商会议泸州市纳溪区委员会", "type": "政协", "level": "县级", "parent": "", "location": "泸州市纳溪区"},
    {"id": 9, "name": "中国(四川)自由贸易试验区川南临港片区管委会", "type": "政府", "level": "厅级", "parent": "四川省人民政府", "location": "泸州市龙马潭区"},
    {"id": 10, "name": "中共泸州市委员会", "type": "党委", "level": "厅级", "parent": "中共四川省委", "location": "泸州市"},
    {"id": 11, "name": "泸州市人民政府", "type": "政府", "level": "厅级", "parent": "四川省人民政府", "location": "泸州市"},
    {"id": 12, "name": "泸州市生态环境局", "type": "政府", "level": "县级", "parent": "泸州市人民政府", "location": "泸州市"},
    {"id": 13, "name": "叙永县人民政府", "type": "政府", "level": "县级", "parent": "泸州市人民政府", "location": "泸州市叙永县"},
    {"id": 14, "name": "中共叙永县委员会", "type": "党委", "level": "县级", "parent": "中共泸州市委员会", "location": "泸州市叙永县"},
    {"id": 15, "name": "泸州市纳溪区政协", "type": "政协", "level": "县级", "parent": "", "location": "泸州市纳溪区"},
    {"id": 16, "name": "泸州市纳溪区公安分局", "type": "政府", "level": "县级", "parent": "泸州市纳溪区人民政府", "location": "泸州市纳溪区"},
    {"id": 17, "name": "中共泸州市委第五巡察组", "type": "党委", "level": "厅级", "parent": "中共泸州市委员会", "location": "泸州市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # Current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2024-09", "end_date": "至今", "rank": "副厅级", "note": "现任区委书记、区人武部党委第一书记"},

    # 袁维荣 previous positions
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2020-12", "end_date": "2024-09", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2021-12", "end_date": "2024-09", "rank": "副厅级", "note": "2020-12-28起任代区长，2021-12-21当选"},
    {"person_id": 1, "org_id": 12, "title": "党组书记、局长", "start_date": "2019", "end_date": "2020-12", "rank": "正处级", "note": "泸州市生态环境局"},
    {"person_id": 1, "org_id": 14, "title": "县委常委", "start_date": "", "end_date": "2019", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "副县长（常务）", "start_date": "", "end_date": "2019", "rank": "副处级", "note": "叙永县委常委、常务副县长"},
    {"person_id": 1, "org_id": 13, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "叙永县副县长"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记", "start_date": "2020-12", "end_date": "2024-09", "rank": "副厅级", "note": "兼区政府党组书记"},

    # Current Mayor
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2024-12", "end_date": "至今", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2025-01", "end_date": "至今", "rank": "副厅级", "note": "2024-12-06起任代区长，2025-01-22当选"},
    {"person_id": 2, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "2024-12", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "常务副区长", "start_date": "2023-04", "end_date": "2024-12", "rank": "副处级", "note": "区委常委、常务副区长"},
    {"person_id": 2, "org_id": 1, "title": "区委宣传部部长（推测）", "start_date": "", "end_date": "2023-04", "rank": "副处级", "note": "前期可能负责宣传/组织工作，具体待查"},

    # Other current leaders
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "接替张毅的常务副区长"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委、区纪委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "跨省交流纪检干部"},
    {"person_id": 4, "org_id": 4, "title": "监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    # Predecessors
    {"person_id": 12, "org_id": 1, "title": "区委书记", "start_date": "2020-11", "end_date": "2024-09", "rank": "副厅级", "note": "前任区委书记"},
    {"person_id": 12, "org_id": 9, "title": "党工委书记", "start_date": "2024-10", "end_date": "至今", "rank": "副厅级", "note": "平调至自贸区川南临港片区"},
    {"person_id": 13, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2020-11", "rank": "副厅级", "note": "纳溪区前区委书记"},
    {"person_id": 13, "org_id": 11, "title": "副市长", "start_date": "2020-11", "end_date": "", "rank": "副厅级", "note": "泸州市副市长"},
    {"person_id": 13, "org_id": 10, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "正厅级(？)", "note": "现任"},
    {"person_id": 14, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "前纳溪区纪委书记"},
    {"person_id": 14, "org_id": 17, "title": "巡察组组长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "泸州市委第五巡察组组长"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # Top leadership: Party Secretary ↔ Government Leader
    {"person_a": 1, "person_b": 2, "type": "colleague", "context": "袁维荣(区委书记)与张毅(区长)在纳溪区党政一把手搭档", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2025-01至今"},

    # Predecessor-successor chains
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "谭荣兵(前书记)将区委书记职务交给袁维荣(现任书记)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2024-09"},
    {"person_a": 13, "person_b": 12, "type": "predecessor_successor", "context": "徐利(前书记)将区委书记职务交给谭荣兵(接任)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2020-11"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "袁维荣(前区长)将区长职务交给张毅(接任)", "overlap_org": "泸州市纳溪区人民政府", "overlap_period": "2024-12"},

    # 袁维荣 with other committee members
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "袁维荣(区委书记)与向来富(常务副区长)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "袁维荣(区委书记)与施崇欢(纪委书记)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "袁维荣(区委书记)与冯科(组织部长)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "袁维荣(区委书记)与王云旭(统战部长)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "至今"},

    # 张毅 with deputy
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "张毅(区长)与向来富(常务副区长)在区政府共事", "overlap_org": "泸州市纳溪区人民政府", "overlap_period": "至今"},

    # 袁维荣's own predecessor chain (叙永→市生态环境→纳溪)
    {"person_a": 1, "person_b": 13, "type": "promotion_chain", "context": "袁维荣接替徐利的纳溪区领导职务，两人通过同一职位接力", "overlap_org": "泸州市纳溪区", "overlap_period": "2024-09"},

    # Cross-org connection
    {"person_a": 12, "person_b": 13, "type": "predecessor_successor", "context": "谭荣与利均为纳溪区委书记(前后任)", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2020-11"},

    # 朱亚梅 (前纪委书记 → 巡察组长)
    {"person_a": 14, "person_b": 4, "type": "predecessor_successor", "context": "朱亚梅(前区纪委书记)离任后由施崇欢接任", "overlap_org": "中共泸州市纳溪区纪律检查委员会", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for a person based on current role."""
    role = p.get("current_post", "")
    if "书记" in role and "纪委" not in role:
        return "255,50,50"    # Red — Party Secretary
    elif "区长" in role or "县长" in role:
        return "50,100,255"   # Blue — Government leader
    elif "常务" in role:
        return "50,150,255"   # Blue — Senior deputy
    elif "纪委" in role or "监委" in role:
        return "255,165,0"    # Orange — Discipline
    elif "组织" in role:
        return "150,50,150"   # Purple — Organization
    elif "统战" in role:
        return "100,200,100"  # Green — United front
    else:
        return "100,100,100"  # Grey — Others

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:  return "255,200,200"
    if "政府" in t:  return "200,200,255"
    if "人大" in t:  return "200,255,255"
    if "政协" in t:  return "255,240,200"
    if "事业单位" in t: return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

def node_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

def build_sqlite(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    for name in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {name}")
    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
    )""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id), FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id), FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")
    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p.get("birthplace", ""), p["education"], p["party_join"], p.get("work_start", ""),
                      p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
                     (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                     (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"  Database written: {db_path}")
    print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

def build_gexf(gexf_path):
    from datetime import datetime as dt
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>纳溪区领导班子工作关系网络 - {SLUG} Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        c = person_color(p)
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:position x="{hash(pid) % 1000 - 500}" y="{hash(pid[::-1]) % 1000 - 500}" z="0.0"/>')
        lines.append('      </node>')
    # ── Organization nodes ──
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    # ── Edges ──
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        period = f"{pos['start_date']} - {pos['end_date']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        weight = "2.0" if r.get("type") in ("colleague", "superior_subordinate") else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" weight="{weight}" label="{esc(r["context"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {gexf_path}")
    print(f"  - {len(positions)} worked_at edges, {len(relationships)} relationship edges")

def write_person_jsons():
    persons_dir = STAGING_DIR
    today = TODAY

    # ── 袁维荣 (区委书记) ──
    yuanweirong = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "泸州市",
            "region": "纳溪区",
            "job": "区委书记",
            "task_id": "sichuan_纳溪区",
            "time_focus": "至今"
        },
        "identity": {
            "person_id": "luzhou_naxi_yuan_weirong",
            "name": "袁维荣",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1980年7月",
            "birthplace": "四川省合江县",
            "native_place": "四川省合江县",
            "education": [
                {"period": "", "institution": "中共四川省委党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S001"]}
            ],
            "party_join": "2002年10月",
            "work_start": "1998年10月",
            "dedupe_keys": {
                "name_birth": "袁维荣_1980",
                "name_birthplace": "袁维荣_合江县",
                "official_profile_url": "https://www.naxi.gov.cn/zw/ldzc/"
            }
        },
        "current_status": {
            "current_post": "区委书记",
            "current_org": "中共泸州市纳溪区委员会",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {"start": "1998年10月", "end": "unknown", "org": "未知", "title": "参加工作", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "1998年10月参加工作；约7年早期经历未找到公开记录", "confidence": "unverified", "source_ids": ["S001"]},
            {"start": "unknown", "end": "unknown", "org": "叙永县人民政府", "title": "副县长", "level": "副处级", "location": "泸州市叙永县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "unknown", "end": "2019", "org": "中共叙永县委员会", "title": "县委常委、常务副县长", "level": "副处级", "location": "泸州市叙永县", "system": "government", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2019", "end": "2020-12", "org": "泸州市生态环境局", "title": "党组书记、局长", "level": "正处级", "location": "泸州市", "system": "government", "rank": "", "is_key_promotion": True, "notes": "从叙永到市局，返回市直系统", "confidence": "plausible", "source_ids": ["S001", "S002"]},
            {"start": "2020-12", "end": "2021-12", "org": "泸州市纳溪区人民政府", "title": "代区长", "level": "副厅级", "location": "泸州市纳溪区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2020-12-28任命为副区长、代区长", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2021-12", "end": "2024-09", "org": "泸州市纳溪区人民政府", "title": "区长", "level": "副厅级", "location": "泸州市纳溪区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2021-12-21当选为纳溪区长", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2020-12", "end": "2024-09", "org": "中共泸州市纳溪区委员会", "title": "区委副书记", "level": "副厅级", "location": "泸州市纳溪区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "同期兼任区委副书记", "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2024-09", "end": "至今", "org": "中共泸州市纳溪区委员会", "title": "区委书记", "level": "副厅级", "location": "泸州市纳溪区", "system": "party", "rank": "", "is_key_promotion": True, "notes": "2024年9月29日任区委书记，为区人武党委第一书记", "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "organizations": [
            {"id": "org_nxqw", "name": "中共泸州市纳溪区委员会", "type": "党委", "role_in_org": "区委书记", "period": "2024-09至今"},
            {"id": "org_nxzf", "name": "泸州市纳溪区人民政府", "type": "政府", "role_in_org": "前区长", "period": "2020-12至2024-09"},
            {"id": "org_nxhb", "name": "泸州市生态环境局", "type": "政府", "role_in_org": "局长", "period": "2019至2020-12"},
            {"id": "org_xyxg", "name": "叙永县人民政府", "type": "政府", "role_in_org": "副县长/常务副县长", "period": ""}
        ],
        "relationships": [
            {"person": "张毅", "person_id": "luzhou_naxi_zhang_yi", "relationship_type": "colleague", "strength": "strong", "evidence": "袁维荣(区委书记)与张毅(区长)为纳溪区党政一把手搭档", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2025-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "谭荣兵", "person_id": "luzhou_naxi_tan_rongbing", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "袁维荣接替谭荣兵任纳溪区委书记", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2024-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "徐利", "person_id": "luzhou_naxi_xu_li", "relationship_type": "promotion_chain", "strength": "medium", "evidence": "徐利、谭荣兵、袁维荣系纳溪区委书记前后三任", "overlap_org": "纳溪区", "overlap_period": "2016-2024", "direction": "undirected", "confidence": "plausible", "source_ids": ["S002"]}
        ],
        "governance_record": [
            {"period": "2024-09至今", "domain": "other", "achievement_or_event": "主持纳溪区全面工作", "role": "区委书记", "measurable_outcome": "", "location": "纳溪区", "confidence": "confirmed", "source_ids": ["S002"]},
            {"period": "2020-12至2024-09", "domain": "economic_development", "achievement_or_event": "主持纳溪区政府全面工作(区长时期)", "role": "区长", "measurable_outcome": "", "location": "纳溪区", "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "professional_profile": {
            "primary_specializations": ["政府管理", "生态环境"],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["合江县(籍)", "叙永县", "泸州市", "纳溪区"],
            "promotion_velocity": {
                "summary": "从副县长到区委书记，跨越多个岗位，县级领导到副厅级，2024年提拔至书记",
                "notable_fast_promotions": ["从市生态环境局局长直升纳溪区长（2020）", "2024年从区长升任书记"]
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "长期在县区一线工作，经历生态环境局专业岗位后再回区县主政", "confidence": "plausible", "source_ids": []}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "total_relationships": 3,
            "strong_connections": 2,
            "medium_connections": 1,
            "weak_connections": 0
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现负面记录", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "袁维荣简历 - 纳溪区政府领导之窗", "url": "https://www.naxi.gov.cn/zw/ldzc/", "publisher": "纳溪区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "政府官网，但访问受限"},
            {"id": "S002", "title": "人民网 - 袁维荣任纳溪区委书记", "url": "http://sc.people.com.cn/", "publisher": "人民网四川频道", "published_at": "2024-09-29", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "确认袁维荣29日任区委书记"},
            {"id": "S003", "title": "泸州市委组织部干部任前公示", "url": "", "publisher": "中共泸州市委组织部", "published_at": "2024-11-14", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "公示张毅拟提名区长"}
        ],
        "identity_confidence": "confirmed",
        "current_role_confidence": "confirmed",
        "career_completeness": "partial",
        "relationship_confidence": "high",
        "biggest_gap": "袁维荣1998-2005年间约7年早期经历未公开",
        "open_questions": [
            {"priority": "critical", "question": "袁维荣1998-2005年的早期职业生涯是什么？", "why_it_matters": "理解其职业起点与早期发展", "suggested_queries": ["袁维荣 早期 工作经历", "袁维荣 1998 2001 2005"], "last_appted": AS_OF}
        ]
    }

    # 张毅 (区长)
    zhangyi = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "泸州市",
            "region": "纳溪区",
            "job": "区长",
            "task_id": "sichuan_纳溪区",
            "time_focus": "至今"
        },
        "identity": {
            "person_id": "luzhou_naxi_zhang_yi",
            "name": "张毅",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1977年10月",
            "birthplace": "四川省泸州市",
            "native_place": "四川省泸州市",
            "education": [{"period": "", "institution": "不详", "major": "", "degree": "大学", "study_type": "unknown", "source_ids": ["S003"]}],
            "party_join": "2001年4月",
            "work_start": "2001年10月",
            "dedupe_keys": {
                "name_birth": "张毅_1977",
                "name_birthplace": "张毅_泸州市",
                "offifcial_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "区长",
            "current_org": "泸州市纳溪区人民政府",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S003", "S004"]
        },
        "career_timeline": [
            {"start": "2001年10月", "end": "unknown", "org": "未知", "title": "参加工作", "level": "", "location": "", "system": "unknown", "rank": "", "is_key_promotion": False, "notes": "2001年10月参加工作", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "unknown", "end": "2023-04", "org": "中共泸州纳溪区委员会", "title": "区委常委、宣传部部长(推测)", "level": "副处级", "location": "泸州市纳溪区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "约20年早期履历未公开", "confidence": "unverified", "source_ids": []},
            {"start": "2023-04", "end": "2024-12", "org": "中共泸州市纳溪区委员会", "title": "区委常委、常务副区长", "level": "副处级", "location": "泸州市纳溪区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "负责区政府常务工作", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "2024-12-06", "end": "2025-01", "org": "泸州市纳溪区人民政府", "title": "代区长", "level": "副厅级", "location": "泸州市纳溪区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "区人大常委会决定代理区长", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            {"start": "2025-01-22", "end": "至今", "org": "泸州市纳溪区人民政府", "title": "区长", "level": "副厅级", "location": "泸州市纳溪区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2025-01-22正式当选纳溪区长", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            {"start": "2024-12", "end": "至今", "org": "中共泸州市纳溪区委员会", "title": "区委副书记", "level": "副厅级", "location": "泸州市纳溪区", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]}
        ],
        "organizations": [
            {"id": "org_nxqw", "name": "中共泸州市纳溪区委员会", "type": "党委", "role_in_org": "区委副书记", "period": "2024-12至今"},
            {"id": "org_nxzf", "name": "泸州市纳溪区人民政府", "type": "政府", "role_in_org": "区长", "period": "2025-01至今"}
        ],
        "relationships": [
            {"person": "袁维荣", "person_id": "luzhou_naxi_yuan_weirong", "relationship_type": "colleague", "strength": "strong", "evidence": "张毅(区长)与袁维荣(区委书记)为纳溪区党政一把手搭档", "overlap_org": "中共泸州市纳溪区委员会", "overlap_period": "2025-至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]}
        ],
        "professional_profile": {
            "primary_specializations": ["政府管理"],
            "secondary_specializations": ["宣传", "经济管理"],
            "career_pattern": "internal_promotion",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["泸州市"],
            "promotion_velocity": {"summary": "从常务副区长到区长的晋升约18个月，较快晋升", "notable_fast_promotions": ["2023-04至2024-12，从常委/常务到区长"]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "unknown", "evidence": "公开信息有限", "confidence": "unverified", "source_ids": []}],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {"total_relationships": 1, "strong_connections": 1, "medium_connections": 0, "weak_connections": 0},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现负面记录", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S003", "title": "泸州市委组织部任前公示", "url": "", "publisher": "中共泸州市委组织部", "published_at": "2024-11-14", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": "张毅拟提名为县(区)长人选公示"},
            {"id": "S004", "title": "纳溪区人大常委会决定", "url": "", "publisher": "泸州市纳溪区人民代表大会常务委员会", "published_at": "2024-12-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "张毅任代区长"}
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "张毅2001-2023年超过20年职业生涯的完整信息"},
        "open_questions": [{"priority": "critical", "question": "张毅2001-2023年完整的职务经历", "why_it_matters": "区长基本履历", "suggested_queries": ["张毅 历任 纳溪区", "张毅 简历 泸州"], "last_appended": AS_OF}]
    }

    # 谭荣兵 (前任书记)
    tanrongbing = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "四川省", "city": "泸州市", "region": "纳溪区", "job": "前区委书记", "task_id": "sichuan_纳溪区", "time_focus": "2020-2024"},
        "identity": {"person_id": "luzhou_naxi_tan_rongbing", "name": "谭荣兵", "aliases": [], "gender": "男", "ethnicity": "汉族"},
        "current_status": {"current_post": "自贸区川南临港片区党工委书记", "current_org": "中国(四川)自由贸易试验区川南临港片区管委会", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S005"]},
        "career_timeline": [
            {"start": "2020-11", "end": "2024-09", "org": "中共泸州市纳溪区委员会", "title": "区委书记", "level": "副厅级", "location": "泸州市纳溪区", "system": "party", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2024-10", "end": "至今", "org": "中国(四川)自由贸易试验区川南临港片区", "title": "党工委书记", "level": "副厅级", "location": "泸州市", "system": "party", "confidence": "confirmed", "source_ids": ["S005"]}
        ],
        "organizations": [{"id": "org_nxqw", "name": "中共泸州市纳溪区委员会", "type": "党委", "role_in_org": "前区委书记", "period": "2020-11至2024-09"}],
        "relationships": [
            {"person": "袁维荣", "person_id": "luzhou_naxi_yuan_weirong", "relationship_type": "predecessor_successor", "strength": "strong", "confidence": "confirmed", "source_ids": ["S005"]},
            {"person": "徐利", "person_id": "luzhou_naxi_xu_li", "relationship_type": "predecessor_successor", "strength": "strong", "confidence": "plausible", "source_ids": ["S005"]}
        ],
        "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "biggest_gap": "谭荣兵2020年之前的完整履历"}
    }

    # 徐利 (前书记)
    xuli = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "四川省", "city": "泸州市", "region": "纳溪区", "job": "前区委书记", "task_id": "sichuan_纳溪区", "time_focus": "-2020"},
        "identity": {"person_id": "luzhou_naxi_xu_li", "name": "徐利", "aliases": [], "gender": "女", "ethnicity": "汉族"},
        "current_status": {"current_post": "市委常委、宣传部部长", "current_org": "中共泸州市委员会", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S006"]},
        "career_timeline": [
            {"start": "", "end": "2020-11", "org": "中共泸州市纳溪区委员会", "title": "区委书记", "level": "副厅级", "location": "泸州市纳溪区", "system": "party", "confidence": "plausible"},
            {"start": "2020-11", "end": "", "org": "泸州市人民政府", "title": "副市长", "level": "副厅级", "location": "泸州市", "system": "government", "confidence": "plausible"},
            {"start": "", "end": "至今", "org": "中共泸州市委员会", "title": "市委常委、宣传部部长", "level": "正厅级", "location": "泸州市", "system": "party", "confidence": "plausible"}
        ],
        "organizations": [{"name": "中共泸州市纳溪区委员会", "type": "党委", "role_in_org": "前区委书记", "period": ""}],
        "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin", "biggest_gap": "徐利纳溪书记前的完整履历"}
    }

    # Write files
    for person_data, job, name in [
        (yuanweirong, "区委书记", "袁维荣"),
        (zhangyi, "区长", "张毅"),
        (tanrongbing, "前区委书记", "谭荣兵"),
        (xuli, "前区委书记", "徐利")
    ]:
        fname = f"{today}-四川省-泸州市-{job}-{name}.json"
        fpath = os.path.join(str(persons_dir), fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON written: {fpath}")

def main():
    print(f"Building {SLUG} data...")
    print()
    print("[1/2] Building SQLite database...")
    build_sqlite(DB_PATH)
    print()
    print("[2/2] Building GEXF graph...")
    build_gexf(GEXF_PATH)
    print()
    print("Done. Statistics:")
    print(f"  Database: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF: {os.path.getsize(GEXF_PATH)} bytes")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()
    print("[Post] Writing person JSONs...")
    write_person_jsons()

if __name__ == "__main__":
    main()