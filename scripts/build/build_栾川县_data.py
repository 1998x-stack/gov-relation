#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 栾川县 (Luanchuan County), 河南省.

Investigation date: 2026-07-24
Task ID: henan_栾川县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.luanchuan.gov.cn/ (栾川县人民政府官网) — official leadership page (confirmed as-of 2026-07-24)
  - http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/ — 政府领导 (government leadership roster)
  - News articles on luanchuan.gov.cn confirming leaders' activities (2026-07-14信访接待, 2026-07-16党建会议, 2026-07-20基层减负会议, etc.)
  - http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/rsrm/ — 人事任免 documents

Confidence notes:
  - 曲万涛 (县委书记): confirmed via official news article (2026-07-14信访接待)
  - 杨会勉 (县长): confirmed via official leadership page and multiple news articles
  - Government leadership roster (副县长): confirmed via official 政府领导 page
  - Party standing committee members (县委常委): confirmed via cross-referencing news articles
  - 买勇 (县人大常委会主任) and 王冲 (县政协主席): confirmed via news article context
  - Career histories for all leaders: unverified — only current positions confirmed from official sources
  - Birth details, education, party join dates for all leaders: unverified
  - Web search tools (Exa, Google, Baidu) were rate-limited or blocked; data sourced entirely from direct government website access
"""
# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "栾川县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "曲万涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-14/1073762.html"
    },
    {
        "id": 2,
        "name": "杨会勉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    # ═══════ 县委领导 ═══════
    {
        "id": 3,
        "name": "李江波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-16/1074116.html"
    },
    {
        "id": 4,
        "name": "符永帅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共栾川县委员会 / 栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 5,
        "name": "许高伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办主任",
        "current_org": "中共栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-20/1074580.html"
    },
    {
        "id": 6,
        "name": "何鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-16/1074116.html"
    },
    {
        "id": 7,
        "name": "马军会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/06-04/1065854.html"
    },
    {
        "id": 8,
        "name": "张雄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共栾川县委员会 / 栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 9,
        "name": "姚彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "中共栾川县委员会 / 栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    # ═══════ 县政府领导 ═══════
    {
        "id": 10,
        "name": "李文强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 11,
        "name": "高晓宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 12,
        "name": "冯艺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "栾川县人民政府 / 栾川县公安局",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 13,
        "name": "段朝辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "栾川县人民政府",
        "source": "http://www.luanchuan.gov.cn/zfxxgk/fdzdgknr/zfld/"
    },
    {
        "id": 14,
        "name": "姬明建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "栾川县人民政府",
        "source": "https://www.luanchuan.gov.cn/2026/05-07/1059620.html"
    },
    # ═══════ 县人大 ═══════
    {
        "id": 15,
        "name": "买勇",
        "gender": "",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "栾川县人民代表大会常务委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-09/1072913.html"
    },
    # ═══════ 县政协 ═══════
    {
        "id": 16,
        "name": "王冲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-09/1072904.html"
    },
    {
        "id": 17,
        "name": "智建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-09/1072904.html"
    },
    {
        "id": 18,
        "name": "谭建峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议栾川县委员会",
        "source": "https://www.luanchuan.gov.cn/2026/07-09/1072904.html"
    },
    # ═══════ 其他县处级领导 ═══════
    {
        "id": 19,
        "name": "梁燕燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（具体职务待查）",
        "current_org": "栾川县",
        "source": "https://www.luanchuan.gov.cn/2026/07-14/1073762.html"
    },
    {
        "id": 20,
        "name": "张震",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（具体职务待查）",
        "current_org": "栾川县",
        "source": "https://www.luanchuan.gov.cn/2026/07-14/1073762.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共栾川县委员会",
        "type": "party",
        "level": "county_party_committee",
        "parent": "中共洛阳市委",
        "location": "河南省洛阳市栾川县"
    },
    {
        "id": 2,
        "name": "栾川县人民政府",
        "type": "government",
        "level": "county_government",
        "parent": "洛阳市人民政府",
        "location": "河南省洛阳市栾川县"
    },
    {
        "id": 3,
        "name": "栾川县公安局",
        "type": "government",
        "level": "county_agency",
        "parent": "栾川县人民政府",
        "location": "河南省洛阳市栾川县"
    },
    {
        "id": 4,
        "name": "栾川县人民代表大会常务委员会",
        "type": "npc",
        "level": "county_npc",
        "parent": "栾川县",
        "location": "河南省洛阳市栾川县"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议栾川县委员会",
        "type": "cppcc",
        "level": "county_cppcc",
        "parent": "栾川县",
        "location": "河南省洛阳市栾川县"
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 曲万涛
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "confirmed as of 2026-07-14 via信访接待新闻"},
    # 杨会勉
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "正处级", "note": "confirmed as of 2026-07-24"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "正处级", "note": "presides over county government常务会议"},
    # 李江波
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "confirmed via 2026-07-16党建会议"},
    # 符永帅
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": "confirmed via government leadership page"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 许高伟
    {"person_id": 5, "org_id": 1, "title": "县委常委、县委办主任", "start": "", "end": "present",
     "rank": "副处级", "note": "confirmed via 2026-07-20基层减负会议"},
    # 何鹏
    {"person_id": 6, "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "confirmed via 2026-07-16党建会议"},
    # 马军会
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "confirmed via news article"},
    # 张雄
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 姚彬
    {"person_id": 9, "org_id": 1, "title": "县委常委（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": "挂职干部"},
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 李文强
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 高晓宇
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "supervises healthcare (医共体建设推进会)"},
    # 冯艺
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 3, "title": "县公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 段朝辉
    {"person_id": 13, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": "挂职干部"},
    # 姬明建
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 买勇
    {"person_id": 15, "org_id": 4, "title": "县人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    # 王冲
    {"person_id": 16, "org_id": 5, "title": "县政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": ""},
    # 智建军
    {"person_id": 17, "org_id": 5, "title": "县政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 谭建峰
    {"person_id": 18, "org_id": 5, "title": "县政协副主席", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 梁燕燕
    {"person_id": 19, "org_id": 1, "title": "县处级领导（具体职务待查）", "start": "", "end": "present",
     "rank": "副处级", "note": "mentioned in信访接待新闻, specific role未确认"},
    # 张震
    {"person_id": 20, "org_id": 1, "title": "县处级领导（具体职务待查）", "start": "", "end": "present",
     "rank": "副处级", "note": "mentioned in信访接待新闻, specific role未确认"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Strong relationships (same standing committee = direct work overlap)
relationships = [
    # 县委书记与县长（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政一把手搭档", "overlap_org": "中共栾川县委员会/栾川县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 县委书记与其他常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委/副县长", "overlap_org": "中共栾川县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委/县委办主任", "overlap_org": "中共栾川县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委/组织部部长", "overlap_org": "中共栾川县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 县长与副县长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "栾川县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "栾川县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长/公安局长", "overlap_org": "栾川县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "栾川县人民政府",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 县委副书记与其他常委
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "县委副书记与组织部部长（党建工作搭档）", "overlap_org": "中共栾川县委员会",
     "overlap_period": "当前", "strength": "strong", "confidence": "confirmed"},
    # 人大主任与政协主席（四套班子）
    {"person_a": 15, "person_b": 16, "type": "overlap",
     "context": "县人大主任与县政协主席（县四套班子领导）", "overlap_org": "栾川县",
     "overlap_period": "当前", "strength": "medium", "confidence": "confirmed"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def is_top_leader(person_id):
    """Check if a person is a top leader (书记/县长)."""
    return person_id in (1, 2)


def person_color(person_id):
    """Return GEXF color for a person based on their role."""
    if person_id == 1:  # 县委书记 - 红色
        return "255,50,50"
    elif person_id == 2:  # 县长 - 蓝色
        return "50,100,255"
    elif person_id == 15:  # 人大主任 - 青色
        return "0,200,200"
    elif person_id == 16:  # 政协主席 - 深黄
        return "200,180,50"
    elif person_id in (17, 18):  # 政协副主席
        return "180,160,80"
    else:  # 其他 - 灰色
        return "100,100,100"


def org_color(org_type):
    """Return GEXF color for an organization by type."""
    colors = {
        "party": "255,200,200",
        "government": "200,200,255",
        "npc": "200,255,255",
        "cppcc": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def person_size(person_id):
    """Return GEXF node size for a person."""
    if is_top_leader(person_id) or person_id in (15, 16):
        return "20.0"
    return "12.0"


def build_db():
    """Create SQLite database and populate it."""
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR IGNORE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                           education, party_join, work_start, current_post,
                                           current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""
            INSERT OR IGNORE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org,
                                        overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"  DB created: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>栾川县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["id"])
        sz = person_size(p["id"])
        role = "person"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{role}"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationships)
    for r in relationships:
        eid += 1
        weight = "2.0" if r.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("confidence", "plausible"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF created: {GEXF_PATH}")


def main():
    print(f"Building {SLUG} data...")
    print(f"  As of: {AS_OF}")
    build_db()
    build_gexf()
    print("Done.")


if __name__ == "__main__":
    main()
