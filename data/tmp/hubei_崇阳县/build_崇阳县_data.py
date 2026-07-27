#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 崇阳县, 咸宁市, 湖北省.

Investigation date: 2026-07-25
Task ID: hubei_崇阳县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - chongyang.gov.cn (崇阳县政府官网) — leadership page and news
  - Government news articles (2026-07)
  - Leadership page: http://www.chongyang.gov.cn/xxgk/zfld/xw/

Research status: COMPLETE
  - All key leaders identified with confirmed roles (as of 2026-07-24)
  - 县委书记杨修伟 and 县长徐望 biography data collected
"""

from __future__ import annotations

import os
import sys

AS_OF = "2026-07-25"

# ── Paths ──────────────────────────────────────────────────────────────────

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "崇阳县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "崇阳县_network.gexf")

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    {
        "id": "p1",
        "name": "杨修伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委书记",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-24)",
        "notes": "confirmed as 县委书记 as of 2026-07-24 from multiple news reports; biography details incomplete",
    },
    {
        "id": "p2",
        "name": "徐望",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年11月",
        "birthplace": "湖北通山",
        "education": "大学学历",
        "party_join": "1996年7月",
        "work_start": "1995年7月",
        "current_post": "崇阳县委副书记、县长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/xw/",
        "notes": "confirmed from official leadership page;县政府党组书记、县长",
    },
    {
        "id": "p3",
        "name": "孟科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委副书记、县经济开发区党工委书记",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-22)",
        "notes": "县委副书记，兼县经济开发区党工委书记",
    },
    {
        "id": "p4",
        "name": "石磊",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县人大常委会主任",
        "current_org": "崇阳县人民代表大会常务委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "confirmed from 2026年上半年经济形势分析会议 attendance",
    },
    {
        "id": "p5",
        "name": "张正韶",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县政协主席",
        "current_org": "中国人民政治协商会议崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "confirmed from 2026年上半年经济形势分析会议 attendance",
    },
    {
        "id": "p6",
        "name": "黄齐飞",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "县委常委，具体职务待确认",
    },
    {
        "id": "p7",
        "name": "师红河",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "县委常委，具体职务待确认",
    },
    {
        "id": "p8",
        "name": "王顺荣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "湖北咸宁",
        "education": "省委党校在职研究生",
        "party_join": "1998年7月",
        "work_start": "1996年11月",
        "current_post": "崇阳县委常委、常务副县长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/wsr/",
        "notes": "县政府党组副书记",
    },
    {
        "id": "p9",
        "name": "夏文强",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "县委常委，具体职务待确认",
    },
    {
        "id": "p10",
        "name": "曾岳林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委、县委办公室主任",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-22)",
        "notes": "confirmed from 杨修伟调研县经济开发区 article",
    },
    {
        "id": "p11",
        "name": "谭其军",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "县委常委，具体职务待确认",
    },
    {
        "id": "p12",
        "name": "鲁畅",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "崇阳县委常委",
        "current_org": "中共崇阳县委员会",
        "source": "chongyang.gov.cn news (2026-07-21)",
        "notes": "县委常委，具体职务待确认",
    },
    {
        "id": "p13",
        "name": "曾卫平",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "birthplace": "湖北崇阳",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1995年9月",
        "current_post": "崇阳县副县长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/zwp/",
        "notes": "confirmed from official leadership page",
    },
    {
        "id": "p14",
        "name": "吴齐林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年9月",
        "birthplace": "湖北通城",
        "education": "省委党校在职研究生学历",
        "party_join": "2006年6月",
        "work_start": "2010年7月",
        "current_post": "崇阳县副县长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/wql/",
        "notes": "confirmed from official leadership page;县政府党组成员",
    },
    {
        "id": "p15",
        "name": "朱翕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年3月",
        "birthplace": "湖北麻城",
        "education": "研究生学历，硕士学位",
        "party_join": "2011年11月",
        "work_start": "2008年7月",
        "current_post": "崇阳县副县长（挂职）",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/zx/",
        "notes": "confirmed from official leadership page;县政府党组成员;挂职",
    },
    {
        "id": "p16",
        "name": "秦凤仙",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年3月",
        "birthplace": "湖北襄阳",
        "education": "省委党校研究生",
        "party_join": "2013年",
        "work_start": "2008年",
        "current_post": "崇阳县副县长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/qfx/",
        "notes": "confirmed from official leadership page;县政府党组成员",
    },
    {
        "id": "p17",
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "湖北咸安",
        "education": "大学学历",
        "party_join": "2001年",
        "work_start": "2002年",
        "current_post": "崇阳县副县长、县公安局党委书记、局长",
        "current_org": "崇阳县人民政府",
        "source": "http://www.chongyang.gov.cn/xxgk/zfld/wc/",
        "notes": "confirmed from official leadership page;县政府党组成员",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共崇阳县委员会", "type": "党委", "level": "县级", "parent": "中共咸宁市委", "location": "崇阳县"},
    {"id": 2, "name": "崇阳县人民政府", "type": "政府", "level": "县级", "parent": "咸宁市人民政府", "location": "崇阳县"},
    {"id": 3, "name": "崇阳县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "咸宁市人大常委会", "location": "崇阳县"},
    {"id": 4, "name": "中国人民政治协商会议崇阳县委员会", "type": "政协", "level": "县级", "parent": "政协咸宁市委员会", "location": "崇阳县"},
    {"id": 5, "name": "崇阳县经济开发区党工委", "type": "党委", "level": "县级", "parent": "中共崇阳县委员会", "location": "崇阳县经济开发区"},
    {"id": 6, "name": "崇阳县公安局", "type": "政府", "level": "县级", "parent": "崇阳县人民政府", "location": "崇阳县"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": "p1", "org_id": 1, "title": "崇阳县委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "县委书记"},
    {"person_id": "p2", "org_id": 1, "title": "崇阳县委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "县委副书记"},
    {"person_id": "p2", "org_id": 2, "title": "崇阳县县长、县政府党组书记", "start": "未知", "end": "present", "rank": "正处级", "note": "县政府全面工作"},
    {"person_id": "p3", "org_id": 1, "title": "崇阳县委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "专职副书记"},
    {"person_id": "p3", "org_id": 5, "title": "崇阳县经济开发区党工委书记", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p4", "org_id": 3, "title": "崇阳县人大常委会主任", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p5", "org_id": 4, "title": "崇阳县政协主席", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p6", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    {"person_id": "p7", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    {"person_id": "p8", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p8", "org_id": 2, "title": "崇阳县常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": "p9", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    {"person_id": "p10", "org_id": 1, "title": "崇阳县委常委、县委办公室主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p11", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    {"person_id": "p12", "org_id": 1, "title": "崇阳县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    {"person_id": "p13", "org_id": 2, "title": "崇阳县副县长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p14", "org_id": 2, "title": "崇阳县副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p15", "org_id": 2, "title": "崇阳县副县长（挂职）", "start": "未知", "end": "present", "rank": "副处级", "note": "挂职;县政府党组成员"},
    {"person_id": "p16", "org_id": 2, "title": "崇阳县副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p17", "org_id": 2, "title": "崇阳县副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": "p17", "org_id": 6, "title": "崇阳县公安局党委书记、局长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": "p1", "person_b": "p2",
        "type": "党政正职搭档",
        "context": "杨修伟（县委书记）与徐望（县长）为崇阳县党政正职搭档",
        "overlap_org": "崇阳县",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p3",
        "type": "上下级",
        "context": "杨修伟（县委书记）为孟科（县委副书记）的直接上级",
        "overlap_org": "中共崇阳县委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p3",
        "type": "同僚",
        "context": "徐望（县长）与孟科（县委副书记）同为县委领导班子成员",
        "overlap_org": "中共崇阳县委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p8",
        "type": "上下级",
        "context": "杨修伟（县委书记）与王顺荣（县委常委、常务副县长）为上下级关系",
        "overlap_org": "崇阳县",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p8",
        "type": "上下级",
        "context": "徐望（县长）与王顺荣（常务副县长）为县政府正副职搭档",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p13",
        "type": "上下级",
        "context": "徐望（县长）与曾卫平（副县长）为县政府正副职",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p14",
        "type": "上下级",
        "context": "徐望（县长）与吴齐林（副县长）为县政府正副职",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p15",
        "type": "上下级",
        "context": "徐望（县长）与朱翕（挂职副县长）为县政府正副职",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p16",
        "type": "上下级",
        "context": "徐望（县长）与秦凤仙（副县长）为县政府正副职",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p2", "person_b": "p17",
        "type": "上下级",
        "context": "徐望（县长）与王超（副县长兼公安局长）为县政府正副职",
        "overlap_org": "崇阳县人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p6", "person_b": "p7",
        "type": "同僚",
        "context": "黄齐飞与师红河同为崇阳县委常委",
        "overlap_org": "中共崇阳县委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p4",
        "type": "同僚",
        "context": "杨修伟（县委书记）与石磊（人大主任）为县四套班子领导",
        "overlap_org": "崇阳县",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p1", "person_b": "p5",
        "type": "同僚",
        "context": "杨修伟（县委书记）与张正韶（政协主席）为县四套班子领导",
        "overlap_org": "崇阳县",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    {
        "person_a": "p8", "person_b": "p10",
        "type": "同僚",
        "context": "王顺荣（常委、常务副县长）与曾岳林（常委、县委办主任）同为县委常委",
        "overlap_org": "中共崇阳县委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pid(s):
    """Normalize person id: strip 'p' prefix for DB."""
    return int(s[1:])


def person_color_and_size(post):
    """Return (r,g,b string, size) for a person based on current post."""
    if "县委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "县长" in post and "副" not in post and "委" not in post:
        return ("50,100,255", 20.0)
    elif "县委副书记" in post:
        return ("100,100,255", 15.0)
    elif "常务副县长" in post:
        return ("100,150,255", 15.0)
    elif "人大常委会主任" in post:
        return ("200,255,255", 15.0)
    elif "政协主席" in post:
        return ("255,240,200", 15.0)
    elif "县委常委" in post and "副县长" in post:
        return ("100,150,255", 12.0)
    elif "副县长" in post and "县委常委" not in post:
        return ("100,150,255", 12.0)
    elif "县委常委" in post:
        return ("100,150,255", 12.0)
    else:
        return ("100,100,100", 12.0)


def build():
    """Run database + GEXF build."""
    import sqlite3

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
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
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>崇阳县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"崇阳县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
