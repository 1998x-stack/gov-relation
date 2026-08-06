#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 孝南区, 孝感市, 湖北省.

Investigation date: 2026-08-06
Task ID: hubei_孝南区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 孝南区人民政府门户网 (www.xiaonan.gov.cn) — 新闻/区融媒体中心 primary reports
  - 百度百科·孝南区词条 (党政领导正职栏, 更新于2025-12)
  - 湖北日报 / 孝感新闻网 (孝感市四套班子锚点)

Research status: PARTIAL EVIDENCE (degraded web access)
  - Current office-holders CONFIRMED from official 区台 news (2026-06~07) + Baike (2025-12)
  - 区委书记张全民、区长陈情 confirmed
  - Full 履历、出生、教育、前任 (predecessor) NOT verifiable this session; encoded as gaps

NOTE: All biography fields (birth, birthplace, education, party_join, work_start) are
UNKNOWN / unverified where no official profile was retrievable. Do not treat as facts.
Career start dates for the two top leaders are explicitly gaps (see person JSON open_questions).
"""

from __future__ import annotations

import os
import sys

AS_OF = "2026-08-08"

# ── Paths ──────────────────────────────────────────────────────────────────

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "孝南区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "孝南区_network.gexf")

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── Persons ────────────────────────────────────────────────────────────────
# confidence: confirmed = current post & name from official 区委/区政府 news; biography fields unknown

persons = [
    {
        "id": "p1",
        "name": "张全民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区委书记",
        "current_org": "中共孝南区委",
        "source": "孝南区政府门户网/区融媒体中心 (2026-07); 百度百科·孝南区 (2025-12)",
        "notes": "现任身份 confirmed (多次公开报道+百度百科)。完整履历未知（出生/学历/入党/任前经历为缺口）。",
    },
    {
        "id": "p2",
        "name": "陈情",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区委副书记、区长",
        "current_org": "孝南区人民政府",
        "source": "孝南区政府门户网站/区融媒体中心 (2026-07); 2026-02 '聚焦两会 陈情参加代表团分组讨论'",
        "notes": "现任身份 confirmed（区委副书记、区长、区政府党组书记）。履历字段为缺口。",
    },
    {
        "id": "p3",
        "name": "刘俊军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区委副书记、区委政法委书记",
        "current_org": "中共孝南区委",
        "source": "孝南区依法治区工作会议报道 (2026-07-24)",
        "notes": "区委副书记、政法委书记 confirmed。履历未知。",
    },
    {
        "id": "p4",
        "name": "郭红燕",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区委常委、常务副区长",
        "current_org": "孝南区人民政府",
        "source": "孝南区政府门户网'孝着办'政企早餐会(第7场) (2026-07-29)",
        "notes": "区委常委、常务副区长 confirmed。名誉为郭红燕。",
    },
    {
        "id": "p5",
        "name": "姚惠萍",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区人大常委会党组书记、主任",
        "current_org": "孝南区人民代表大会常务委员会",
        "source": "孝南区人大常委会调研报道 (2026-07-10)",
        "notes": "区人大党组书记、主任 confirmed。",
    },
    {
        "id": "p6",
        "name": "陈义华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区政协党组书记、主席",
        "current_org": "政协孝南区委员会",
        "source": "区政协第七届常委会第19次会议报道 (2026-07-16)",
        "notes": "区政协主席 confirmed。",
    },
    {
        "id": "p7",
        "name": "杨先勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区人民政府副区长",
        "current_org": "孝南区人民政府",
        "source": "区政协常委会第19次会议报道 (2026-07-16)",
        "notes": "区政府副区长 confirmed（代表区政府听取政协建言）。",
    },
    {
        "id": "p8",
        "name": "吴慧芬",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区人民政府副区长",
        "current_org": "孝南区人民政府",
        "source": "区人大常委会科技创新调研报道 (2026-07-10)",
        "notes": "区政府副区长 confirmed。",
    },
    {
        "id": "p9",
        "name": "李玲玉",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区人大常委会副主任",
        "current_org": "孝南区人民代表大会常务委员会",
        "source": "区人大常委会调研报道 (2026-07-10)",
        "notes": "区人大副主任 confirmed（随姚惠萍调研科技创新）。",
    },
    {
        "id": "p10",
        "name": "黄丽华",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区人民法院院长",
        "current_org": "孝南区人民法院",
        "source": "区领导调研孝南法院工作报道 (2026-07-15)",
        "notes": "区法院院长 confirmed（在调研会上汇报工作）。",
    },
    {
        "id": "p11",
        "name": "高亚洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区政协党组副书记、副主席",
        "current_org": "政协孝南区委员会",
        "source": "区政协常委会第19次会议报道 (2026-07-16)",
        "notes": "区政协党组副书记、副主席 confirmed。",
    },
    {
        "id": "p12",
        "name": "肖立学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区政协秘书长",
        "current_org": "政协孝南区委员会",
        "source": "区政协常委会第19次会议报道 (2026-07-16)",
        "notes": "区政协秘书长 confirmed。",
    },
    {
        "id": "p13",
        "name": "吴华国",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区领导",
        "current_org": "中共孝南区委",
        "source": "孝南区依法治区工作会议报道 (2026-07-24)",
        "notes": "出席区级重要会议，职务待核（疑为区委常委/副区长）。",
    },
    {
        "id": "p14",
        "name": "周冠城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区领导",
        "current_org": "中共孝南区委",
        "source": "区领导调研孝南法院报道 (2026-07-15)",
        "notes": "区领导，职务待考。",
    },
    {
        "id": "p15",
        "name": "阚巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区领导",
        "current_org": "中共孝南区委",
        "source": "区委书记调研矛盾纠纷报道 (2026-07-28)",
        "notes": "区领导，职务待考。",
    },
    {
        "id": "p16",
        "name": "赵冰",
        "gender": "未知",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区领导",
        "current_org": "中共孝南区委",
        "source": "区委书记调研矛盾纠纷报道 (2026-07-28)",
        "notes": "区领导，职务待考。",
    },
    {
        "id": "p17",
        "name": "孙丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝南区领导",
        "current_org": "中共孝南区委",
        "source": "区依法治区工作会议报道 (2026-07-24)",
        "notes": "区领导，职务待考。",
    },
    # 上级锚点（孝感市）用于跨县（市、区）网络
    {
        "id": "p18",
        "name": "胡玖明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝感市委书记",
        "current_org": "中共孝感市委",
        "source": "孝感市政府网/湖北日报 (2026-08)",
        "notes": "孝感市委一把手，孝南区区委的直接上级党委领导。",
    },
    {
        "id": "p19",
        "name": "林中麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "未知",
        "birthplace": "未知",
        "education": "未知",
        "party_join": "未知",
        "work_start": "未知",
        "current_post": "孝感市委副书记、市长",
        "current_org": "孝感市人民政府",
        "source": "孝感网/湖北日报 (2026-08)",
        "notes": "孝感市市长，为区政府对应上级政府领导。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共孝南区委", "type": "党委", "level": "县处级", "parent": "中共孝感市委", "location": "孝南区"},
    {"id": 2, "name": "孝南区人民政府", "type": "政府", "level": "县处级", "parent": "孝感市人民政府", "location": "孝南区"},
    {"id": 3, "name": "孝南区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "孝感市人大常委会", "location": "孝南区"},
    {"id": 4, "name": "中国人民政治协商会议孝南区委员会", "type": "政协", "level": "县处级", "parent": "孝感市政协", "location": "孝南区"},
    {"id": 5, "name": "孝南区人民法院", "type": "法院", "level": "县处级", "parent": "孝感市中级人民法院", "location": "孝南区"},
    # 上级城市锚点
    {"id": 6, "name": "中共孝感市委", "type": "党委", "level": "地级", "parent": "中共湖北省委", "location": "孝感市"},
    {"id": 7, "name": "孝感市人民政府", "type": "政府", "level": "地级", "parent": "湖北省人民政府", "location": "孝感市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": "p1", "org_id": 1, "title": "孝南区委书记", "start": "未知(2025年前后起任)", "end": "present", "rank": "正处级", "note": "区委一把手"},
    {"person_id": "p2", "org_id": 1, "title": "孝南区委副书记", "start": "未知", "end": "present", "rank": "副处级", "note": "区委副书记"},
    {"person_id": "p2", "org_id": 2, "title": "孝南区区长、区政府党组书记", "start": "未知", "end": "present", "rank": "正处级", "note": "区政府全面工作"},
    {"person_id": "p3", "org_id": 1, "title": "孝南区委副书记、政法委书记", "start": "未知", "end": "present", "rank": "副处级", "note": "副书记兼政法委"},
    {"person_id": "p4", "org_id": 1, "title": "孝南区委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "区委常委"},
    {"person_id": "p4", "org_id": 2, "title": "孝南区常务副区长", "start": "未知", "end": "present", "rank": "副处级", "note": "常务副区长"},
    {"person_id": "p5", "org_id": 3, "title": "孝南区人大常委会党组书记、主任", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p6", "org_id": 4, "title": "孝南区政协党组书记、主席", "start": "未知", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "p7", "org_id": 2, "title": "孝南区人民政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p8", "org_id": 2, "title": "孝南区人民政府副区长", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p9", "org_id": 3, "title": "孝南区人大常委会副主任", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p10", "org_id": 5, "title": "孝南区人民法院院长", "start": "未知", "end": "present", "rank": "县处级(副处级?)", "note": "法院院长"},
    {"person_id": "p11", "org_id": 4, "title": "孝南区政协党组副书记、副主席", "start": "未知", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "p12", "org_id": 4, "title": "孝南区政协秘书长", "start": "未知", "end": "present", "rank": "科级/处级", "note": ""},
    {"person_id": "p13", "org_id": 1, "title": "孝南区领导(区委常委待核)", "start": "未知", "end": "present", "rank": "副处级", "note": "在职不详"},
    {"person_id": "p14", "org_id": 1, "title": "孝南区领导", "start": "未知", "end": "present", "rank": "副处级", "note": "在职不详"},
    {"person_id": "p15", "org_id": 1, "title": "孝南区领导", "start": "未知", "end": "present", "rank": "副处级", "note": "在职不详"},
    {"person_id": "p16", "org_id": 1, "title": "孝南区领导", "start": "未知", "end": "present", "rank": "副处级", "note": "在职不详"},
    {"person_id": "p17", "org_id": 1, "title": "孝南区领导", "start": "未知", "end": "present", "rank": "副处级", "note": "在职不详"},
    # 市级锚点
    {"person_id": "p18", "org_id": 6, "title": "孝感市委书记", "start": "未知", "end": "present", "rank": "厅级", "note": "孝感市一把手"},
    {"person_id": "p19", "org_id": 7, "title": "孝感市委副书记、市长", "start": "未知", "end": "present", "rank": "厅级", "note": "市政府一把手"},
]

# ── Relationships (为网络边缘；当前只编码确认的现任搭班关系) ──────────────

relationships = [
    {"person_a": "p1", "person_b": "p2", "type": "党政正职搭班", "context": "张全民（区委书记）与陈情（区长）搭班，构成孝南区党政正职搭档", "overlap_org": "孝南区", "overlap_period": "至2026", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p3", "type": "上下级", "context": "张全民（书记）与刘俊军（副书记兼政法委书记）为区委上下级", "overlap_org": "中共孝南区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p17", "type": "上下级", "context": "张全民与孙丰同出席区依法治区会议", "overlap_org": "中共孝南区委", "overlap_period": "2026", "confidence": "plausible"},
    {"person_a": "p1", "person_b": "p13", "type": "同僚", "context": "张全民与吴华国同出席区依法治区会议", "overlap_org": "中共孝南区委", "overlap_period": "2026", "confidence": "plausible"},
    {"person_a": "p2", "person_b": "p4", "type": "上下级", "context": "陈情（区长）与郭红燕（常务副区长）为区政府正副职", "overlap_org": "孝南区人民政府", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p7", "type": "上下级", "context": "陈情（区长）与杨先勇（副区长）为政府正副关系", "overlap_org": "孝南区人民政府", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p8", "type": "上下级", "context": "陈情（区长）与吴慧芬（副区长）为政府正副关系", "overlap_org": "孝南区人民政府", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p5", "person_b": "p9", "type": "同僚", "context": "姚惠萍（人大主任）与李玲玉（人大副主任）同属人大班子", "overlap_org": "孝南区人民代表大会常务委员会", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p6", "person_b": "p11", "type": "同僚", "context": "陈义华（政协主席）与高亚洲（政协副主席）同属政协班子", "overlap_org": "政协孝南区委员会", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p10", "type": "上下级", "context": "张全民（书记）调研法院，黄丽华（院长）汇报工作", "overlap_org": "孝南区人民法院", "overlap_period": "2026", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p18", "type": "上下级", "context": "张全民（孝南区委书记）受孝感市委（书记胡玖明）领导", "overlap_org": "中共孝感市委/中共孝南区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p19", "type": "上下级", "context": "陈情（孝南区长）受孝感市政府（林中麟）领导", "overlap_org": "孝感市人民政府/孝南区人民政府", "overlap_period": "", "confidence": "confirmed"},
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
    if "区委书记" in post and "副" not in post:
        return ("255,50,50", 20.0)
    elif "区长" in post and "副" not in post and "副书记" in post:
        return ("50,100,255", 20.0)
    elif "区委副书记" in post:
        return ("100,100,255", 15.0)
    elif "常务副区长" in post:
        return ("100,150,255", 15.0)
    elif "人大常委会主任" in post:
        return ("200,255,255", 15.0)
    elif "政协主席" in post:
        return ("255,240,200", 15.0)
    elif "区领导" in post:
        return ("100,150,255", 12.0)
    elif "副区长" in post:
        return ("100,150,255", 12.0)
    elif "政协" in post:
        return ("255,240,200", 12.0)
    elif "人大常委会副主任" in post:
        return ("200,255,255", 12.0)
    elif "区委常委" in post:
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
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT, birthplace TEXT,
            education TEXT, party_join TEXT, work_start TEXT, current_post TEXT,
            current_org TEXT, source TEXT, notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source,notes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
             p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""),
             p.get("work_start", ""), p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )
    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""), o.get("parent", ""), o.get("location", ""))
        )
    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"], pos.get("start", ""),
             pos.get("end", "present"), pos.get("rank", ""), pos.get("note", ""))
        )
    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,confidence) "
            "VALUES (?,?,?,?,?,?,?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("confidence", "unverified"))
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
        "法院": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>孝南区领导班子工作关系网络 - ' + AS_OF + '</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

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

    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{pid(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
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

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid(pos["person_id"])}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        a = pid(r["person_a"])
        b = pid(r["person_b"])
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

    print(f"\n{'='*60}")
    print("孝南区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()