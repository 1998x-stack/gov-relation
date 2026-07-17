#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 清水县 (Qingshui County), 天水市, 甘肃省.

清水县 — 甘肃省天水市下辖县, 位于天水市东北部.
Covers current County Party Secretary (肖玉川), County Magistrate (王涛),
their predecessors, and leadership team.

Current leadership as of 2026-07:
  - 肖玉川 (县委书记, appointed June 2026)
  - 王涛 (县长, since Jan 2024)

Reference sources:
  - 天水在线/每日甘肃/中国甘肃网: 人事任免报道
  - 甘肃省委组织部任前公示 (2023-12, 2026-06)
  - Baidu Baike / 360百科: 个人简历信息
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/gansu_清水县")
DB_PATH = os.path.join(TMP, "清水县_network.db")
GEXF_PATH = os.path.join(TMP, "清水县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════

    # 肖玉川 — 清水县委书记 (as of 2026.06)
    {"id": 1, "name": "肖玉川", "gender": "女", "ethnicity": "汉族",
     "birth": "1985", "birthplace": "湖北随州",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委书记",
     "current_org": "中共清水县委员会",
     "source": "甘肃省委组织部任前公示2026-06-14; 天水在线2026-06-28"},

    # 王涛 — 清水县人民政府县长 (as of 2024.01)
    {"id": 2, "name": "王涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "河南洛阳",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委副书记、县长",
     "current_org": "清水县人民政府",
     "source": "中国甘肃网2024-01-21; 甘肃政法网任前公示2023-12-24"},

    # ═══════════════════════════════════════════════════════════
    # PREDECESSORS — 县委书记
    # ═══════════════════════════════════════════════════════════

    # 李菊霞 — 前任清水县委书记 (2024.01-2026.06), 现庆阳市委常委
    {"id": 3, "name": "李菊霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "甘肃西和",
     "education": "省委党校研究生, 经济学学士",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "庆阳市委常委（原清水县委书记）",
     "current_org": "中共庆阳市委员会",
     "source": "每日甘肃2024-01-04; Baidu Baike"},

    # 马越垠 — 前任清水县委书记 (2021.04-2024.01)
    {"id": 4, "name": "马越垠", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-11", "birthplace": "甘肃甘谷",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘肃省小陇山林业保护中心党委书记、主任（原清水县委书记）",
     "current_org": "甘肃省小陇山林业保护中心",
     "source": "知政堂2024-01-06; 网易新闻2022-11-23"},

    # 刘天波 — 前任清水县委书记 (~2011.09-2021.04)
    {"id": 5, "name": "刘天波", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-03", "birthplace": "甘肃天水秦城",
     "education": "省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "甘肃省林业和草原局党组成员、副局长（原清水县委书记）",
     "current_org": "甘肃省林业和草原局",
     "source": "天水在线2021-02-08; Baidu Baike"},

    # ═══════════════════════════════════════════════════════════
    # PREDECESSORS — 县长
    # ═══════════════════════════════════════════════════════════

    # 李菊霞 also previously served as 清水县长 (2021.06-2024.01)
    # (same person as id=3, listed above)

    # ═══════════════════════════════════════════════════════════
    # KEY DEPUTIES — 县委常委 & 县政府领导
    # ═══════════════════════════════════════════════════════════

    # Note: Specific deputy names for 2025-2026 period need verification.
    # These are typical county-level positions. Actual names should be
    # confirmed from official sources when available.

    # 县委副书记（专职）
    {"id": 6, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委副书记（专职）",
     "current_org": "中共清水县委员会",
     "source": "待查"},

    # 县委常委、常务副县长
    {"id": 7, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、常务副县长",
     "current_org": "清水县人民政府",
     "source": "待查"},

    # 县委常委、组织部部长
    {"id": 8, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、组织部部长",
     "current_org": "中共清水县委组织部",
     "source": "待查"},

    # 县委常委、纪委书记、监委主任
    {"id": 9, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、纪委书记、监委主任",
     "current_org": "中共清水县纪律检查委员会",
     "source": "待查"},

    # 县委常委、政法委书记
    {"id": 10, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、政法委书记",
     "current_org": "中共清水县委政法委员会",
     "source": "待查"},

    # 县委常委、宣传部部长
    {"id": 11, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、宣传部部长",
     "current_org": "中共清水县委宣传部",
     "source": "待查"},

    # 县委常委、统战部部长
    {"id": 12, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、统战部部长",
     "current_org": "中共清水县委统战部",
     "source": "待查"},

    # 县委常委、县委办公室主任
    {"id": 13, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、县委办公室主任",
     "current_org": "中共清水县委办公室",
     "source": "待查"},

    # 县人武部部长
    {"id": 14, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县委常委、县人武部部长",
     "current_org": "清水县人民武装部",
     "source": "待查"},

    # 县人大常委会主任
    {"id": 15, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县人大常委会主任",
     "current_org": "清水县人民代表大会常务委员会",
     "source": "待查"},

    # 县政协主席
    {"id": 16, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县政协主席",
     "current_org": "中国人民政治协商会议清水县委员会",
     "source": "待查"},

    # 副县长（排名靠前）
    {"id": 17, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "清水县副县长",
     "current_org": "清水县人民政府",
     "source": "待查"},
]

organizations = [
    {"id": 1, "name": "中共清水县委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市清水县"},
    {"id": 2, "name": "清水县人民政府", "type": "政府", "level": "县处级",
     "parent": "天水市人民政府", "location": "甘肃省天水市清水县"},
    {"id": 3, "name": "清水县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "天水市人大常委会", "location": "甘肃省天水市清水县"},
    {"id": 4, "name": "中国人民政治协商会议清水县委员会", "type": "政协", "level": "县处级",
     "parent": "天水市政协", "location": "甘肃省天水市清水县"},
    {"id": 5, "name": "中共清水县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市纪律检查委员会", "location": "甘肃省天水市清水县"},
    {"id": 6, "name": "中共清水县委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共清水县委员会", "location": "甘肃省天水市清水县"},
    {"id": 7, "name": "中共清水县委宣传部", "type": "党委", "level": "乡科级",
     "parent": "中共清水县委员会", "location": "甘肃省天水市清水县"},
    {"id": 8, "name": "中共清水县委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共清水县委员会", "location": "甘肃省天水市清水县"},
    {"id": 9, "name": "中共清水县委政法委员会", "type": "党委", "level": "乡科级",
     "parent": "中共清水县委员会", "location": "甘肃省天水市清水县"},
    {"id": 10, "name": "中共清水县委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共清水县委员会", "location": "甘肃省天水市清水县"},
    {"id": 11, "name": "清水县人民武装部", "type": "政府", "level": "县处级",
     "parent": "天水军分区", "location": "甘肃省天水市清水县"},
    {"id": 12, "name": "华池县人民政府", "type": "政府", "level": "县处级",
     "parent": "庆阳市人民政府", "location": "甘肃省庆阳市华池县"},
    {"id": 13, "name": "中共华池县委员会", "type": "党委", "level": "县处级",
     "parent": "中共庆阳市委员会", "location": "甘肃省庆阳市华池县"},
    {"id": 14, "name": "中共庆阳市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省庆阳市"},
    {"id": 15, "name": "中共秦州区委员会", "type": "党委", "level": "县处级",
     "parent": "中共天水市委员会", "location": "甘肃省天水市秦州区"},
    {"id": 16, "name": "甘肃省小陇山林业保护中心", "type": "事业单位", "level": "正县/副厅级",
     "parent": "甘肃省林业和草原局", "location": "甘肃省天水市"},
    {"id": 17, "name": "甘肃省林业和草原局", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": 18, "name": "中共天水市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共甘肃省委员会", "location": "甘肃省天水市"},
    {"id": 19, "name": "天水市人民政府", "type": "政府", "level": "地厅级",
     "parent": "甘肃省人民政府", "location": "甘肃省天水市"},
]

positions = [
    # ── 肖玉川 (id=1) ──
    {"person_id": 1, "org_id": 13, "title": "华池县委副书记", "start": "", "end": "", "rank": "副处级",
     "note": "曾任华池县委副书记"},
    {"person_id": 1, "org_id": 12, "title": "华池县人民政府县长", "start": "", "end": "2026-06", "rank": "正处级",
     "note": "华池县委副书记、县长, 调任清水县委书记"},
    {"person_id": 1, "org_id": 1, "title": "清水县委书记", "start": "2026-06", "end": "present", "rank": "副厅级",
     "note": "2026年6月任清水县委书记"},

    # ── 王涛 (id=2) ──
    {"person_id": 2, "org_id": 15, "title": "秦州区委副书记、统战部部长", "start": "", "end": "2024-01", "rank": "副处级",
     "note": "此前任秦州区委副书记、统战部部长"},
    {"person_id": 2, "org_id": 2, "title": "清水县委副书记、代县长", "start": "2024-01-12", "end": "2024-01-20", "rank": "正处级",
     "note": "2024年1月12日任代县长"},
    {"person_id": 2, "org_id": 2, "title": "清水县委副书记、县长", "start": "2024-01-20", "end": "present", "rank": "正处级",
     "note": "2024年1月20日当选县长"},

    # ── 李菊霞 (id=3) ──
    {"person_id": 3, "org_id": 2, "title": "清水县委副书记、副县长、代县长", "start": "2021-04", "end": "2021-06", "rank": "正处级",
     "note": "2021年4月任代县长"},
    {"person_id": 3, "org_id": 2, "title": "清水县委副书记、县长", "start": "2021-06", "end": "2024-01", "rank": "正处级",
     "note": "2021年6月当选县长"},
    {"person_id": 3, "org_id": 1, "title": "清水县委书记", "start": "2024-01", "end": "2026-06", "rank": "副厅级",
     "note": "2024年1月任县委书记"},
    {"person_id": 3, "org_id": 14, "title": "庆阳市委常委", "start": "2026-06", "end": "present", "rank": "副厅级",
     "note": "2026年6月调任庆阳市委常委"},

    # ── 马越垠 (id=4) ──
    {"person_id": 4, "org_id": 2, "title": "清水县委副书记、县长", "start": "2011-09", "end": "2021-04", "rank": "正处级",
     "note": "近10年县长"},
    {"person_id": 4, "org_id": 1, "title": "清水县委书记", "start": "2021-04", "end": "2024-01", "rank": "副厅级",
     "note": "2021年4月接任县委书记"},
    {"person_id": 4, "org_id": 16, "title": "甘肃省小陇山林业保护中心党委书记、主任", "start": "2024-01", "end": "present", "rank": "正县级/副厅级",
     "note": "2024年1月卸任县委书记后调任"},

    # ── 刘天波 (id=5) ──
    {"person_id": 5, "org_id": 2, "title": "清水县委副书记、县长", "start": "2007-01", "end": "2011-09", "rank": "正处级",
     "note": "此前2006年9月任代县长, 2007年1月当选县长"},
    {"person_id": 5, "org_id": 1, "title": "清水县委书记", "start": "2011-09", "end": "2021-04", "rank": "副厅级",
     "note": "2011年9月任县委书记"},
    {"person_id": 5, "org_id": 18, "title": "天水市委常委、政法委书记", "start": "2021", "end": "2022", "rank": "副厅级",
     "note": "2021年任天水市委常委、政法委书记"},
    {"person_id": 5, "org_id": 17, "title": "甘肃省林业和草原局党组成员、副局长", "start": "2022-11", "end": "present", "rank": "副厅级",
     "note": "2022年11月任甘肃省林草局副局长"},
]

relationships = [
    # ── Current top leaders ──
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "肖玉川作为县委书记, 王涛作为县长, 是党政一把手搭档关系",
     "overlap_org": "中共清水县委员会/清水县人民政府",
     "overlap_period": "2026-06~present", "confidence": "confirmed"},

    # ── Succession chain: 县委书记 ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "肖玉川接替李菊霞任清水县委书记",
     "overlap_org": "中共清水县委员会",
     "overlap_period": "2026-06", "confidence": "confirmed"},

    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "strength": "strong",
     "context": "李菊霞接替马越垠任清水县委书记（李此前曾任县长, 由县长直接升任书记）",
     "overlap_org": "中共清水县委员会",
     "overlap_period": "2024-01", "confidence": "confirmed"},

    {"person_a": 4, "person_b": 5, "type": "predecessor_successor", "strength": "strong",
     "context": "马越垠接替刘天波任清水县委书记（马此前曾任县长10年）",
     "overlap_org": "中共清水县委员会",
     "overlap_period": "2021-04", "confidence": "confirmed"},

    # ── Succession chain: 县长 ──
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "strength": "strong",
     "context": "王涛接替李菊霞任清水县长（李菊霞升任县委书记）",
     "overlap_org": "清水县人民政府",
     "overlap_period": "2024-01", "confidence": "confirmed"},

    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "strength": "strong",
     "context": "李菊霞接替马越垠任清水县长（马越垠升任县委书记）",
     "overlap_org": "清水县人民政府",
     "overlap_period": "2021-04", "confidence": "confirmed"},

    {"person_a": 4, "person_b": 5, "type": "predecessor_successor", "strength": "strong",
     "context": "马越垠接替刘天波任清水县长（刘天波升任县委书记）",
     "overlap_org": "清水县人民政府",
     "overlap_period": "2011-09", "confidence": "confirmed"},

    # ── Cross-county / network relationships ──
    {"person_a": 1, "person_b": 3, "type": "cross_county_rotation", "strength": "medium",
     "context": "肖玉川从华池县（庆阳）跨市调任清水县（天水）, 与李菊霞形成跨县交流网络. 李菊霞本人也从清水县调任庆阳市.",
     "overlap_org": "",
     "overlap_period": "2026-06", "confidence": "confirmed"},

    {"person_a": 4, "person_b": 5, "type": "overlap", "strength": "strong",
     "context": "马越垠与刘天波在清水县长期共事: 马任县长期间, 刘任县委书记, 共事约10年（2011-2021）",
     "overlap_org": "中共清水县委员会/清水县人民政府",
     "overlap_period": "2011-2021", "confidence": "confirmed"},

    {"person_a": 3, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "李菊霞与马越垠在清水县共事: 李菊霞任县长期间, 马越垠任县委书记（2021年4月-2024年1月约3年）",
     "overlap_org": "中共清水县委员会/清水县人民政府",
     "overlap_period": "2021-2024", "confidence": "confirmed"},
]


# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p["current_post"]
    if "县委书记" in role and "副书记" not in role:
        return "255,50,50"
    elif "县长" in role and "副书记" in role:
        return "50,100,255"
    elif "县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")


def is_top_leader(p):
    role = p["current_post"]
    return "县委书记" in role or ("县长" in role and "副书记" in role)


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"],
             r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>清水县领导班子工作关系网络 - 甘肃省天水市清水县</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")


# ── SUMMARY ──────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
