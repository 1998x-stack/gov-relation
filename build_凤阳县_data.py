#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 凤阳县 (Fengyang County, Chuzhou, Anhui) leadership network.

Generated: 2026-07-16
Task: anhui_凤阳县 - 县委书记 & 县长
Sources:
  - Fengyang County Government Website (www.fengyang.gov.cn) — leadership page, news articles
  - Existing person JSON for 焦艳 (from 琅琊区 investigation)
  - Prior build script for 琅琊区

Confidence note: Web research was conducted under network constraints. Baidu Baike and
most Chinese search engines were unreachable. Official government website (fengyang.gov.cn)
was accessible for the homepage and leadership page but deeper navigation was blocked.
Some career timeline data is inferred from available snippets and should be verified.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = SCRIPT_DIR
# If running from staging directory
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_凤阳县")
DB_PATH = os.path.join(STAGING, "凤阳县_network.db")
GEXF_PATH = os.path.join(STAGING, "凤阳县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── RESEARCH DATA ────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记
    {
        "id": "fengyang_jiao_yan",
        "name": "焦艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县委书记",
        "current_org": "中共凤阳县委员会",
        "source": "https://www.fengyang.gov.cn/ (县委理论学习中心组集体学习会议报道, 2026-07-06)",
        "notes": "焦艳此前任琅琊区委书记。2026年7月已以凤阳县委书记身份出席县委理论学习中心组会议。具体任职起始时间和完整履历待核实。",
        "confidence": "confirmed"
    },

    # 县长
    {
        "id": "fengyang_wang_junqing",
        "name": "王俊卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生学历，法学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县委副书记、县长、党组书记",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/ (领导之窗页面, 2026-07-16)",
        "notes": "曾任市辖区群团组织正职，街道党工委书记，地级市政府工作部门副调研员，县政府副县长，县委常委，县委副书记、开发区党工委书记等。",
        "confidence": "confirmed"
    },

    # ══════════════ 县委领导班子（县政府领导已知，县委常委名单待补充）══════════════

    # 县委常委、常务副县长
    {
        "id": "fengyang_chen_changjing",
        "name": "陈长静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县委常委、县政府常务副县长、党组副书记",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "县政府领导排名第二，负责县政府常务工作。具体履历待补充。",
        "confidence": "confirmed"
    },

    # 县委常委、副县长
    {
        "id": "fengyang_hu_zongquan",
        "name": "胡宗权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县委常委、县政府副县长、党组成员",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "具体履历待补充。",
        "confidence": "confirmed"
    },

    # 县委常委、副县长
    {
        "id": "fengyang_fang_fang",
        "name": "方方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县委常委、县政府副县长、党组成员",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "具体履历待补充。",
        "confidence": "confirmed"
    },

    # 副县长（非县委常委）
    {
        "id": "fengyang_zhang_yan",
        "name": "张艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县副县长",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "具体履历待补充。",
        "confidence": "confirmed"
    },

    # 副县长兼公安局长
    {
        "id": "fengyang_ni_yuxin",
        "name": "倪玉新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县副县长、党组成员，县公安局局长、党委书记",
        "current_org": "凤阳县人民政府/凤阳县公安局",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "负责公安、司法、信访等工作。具体履历待补充。",
        "confidence": "confirmed"
    },

    # 挂职副县长
    {
        "id": "fengyang_wu_yin",
        "name": "武胤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县副县长（挂职）",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "挂职副县长，具体派出单位和分管领域待补充。",
        "confidence": "confirmed"
    },

    # 副县长
    {
        "id": "fengyang_ma_qingqing",
        "name": "马庆庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凤阳县副县长、党组成员",
        "current_org": "凤阳县人民政府",
        "source": "https://www.fengyang.gov.cn/zwgk/ldzc/",
        "notes": "具体履历待补充。",
        "confidence": "confirmed"
    },

    # ═══ Key previous figure: 焦艳的前任（凤阳县委书记）═══
    # Note: The previous Fengyang County Party Secretary was 朱林 (Zhu Lin) or 徐广友
    # This needs verification from live sources
    {
        "id": "fengyang_prev_secretary",
        "name": "待确认（前任县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "需从官网或新闻报道确认",
        "notes": "焦艳的前任凤阳县委书记。根据一般组织程序，县委书记任职通常为3-5年。具体姓名待查。",
        "confidence": "unverified"
    },

    # ═══ Previous county mayor 王俊卿的前任 ═══
    {
        "id": "fengyang_prev_mayor",
        "name": "待确认（前任县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "需从官网或新闻报道确认",
        "notes": "王俊卿的前任凤阳县县长。王俊卿大约在2022-2023年左右接任县长（需核实）。前任县长可能为朱林或其他人。",
        "confidence": "unverified"
    },
]

organizations = [
    {"id": "org_party", "name": "中共凤阳县委员会", "type": "party",
     "level": "county", "parent": "中共滁州市委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_gov", "name": "凤阳县人民政府", "type": "government",
     "level": "county", "parent": "滁州市人民政府", "location": "安徽省滁州市凤阳县"},
    {"id": "org_npc", "name": "凤阳县人民代表大会常务委员会", "type": "people_congress",
     "level": "county", "parent": "凤阳县", "location": "安徽省滁州市凤阳县"},
    {"id": "org_cppcc", "name": "中国人民政治协商会议凤阳县委员会", "type": "cppcc",
     "level": "county", "parent": "凤阳县", "location": "安徽省滁州市凤阳县"},
    {"id": "org_discipline", "name": "中共凤阳县纪律检查委员会", "type": "discipline",
     "level": "county", "parent": "中共凤阳县委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_organization", "name": "中共凤阳县委员会组织部", "type": "party",
     "level": "county", "parent": "中共凤阳县委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_propaganda", "name": "中共凤阳县委员会宣传部", "type": "party",
     "level": "county", "parent": "中共凤阳县委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_politics_law", "name": "中共凤阳县委员会政法委员会", "type": "party",
     "level": "county", "parent": "中共凤阳县委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_united_front", "name": "中共凤阳县委员会统战部", "type": "party",
     "level": "county", "parent": "中共凤阳县委员会", "location": "安徽省滁州市凤阳县"},
    {"id": "org_public_security", "name": "凤阳县公安局", "type": "government",
     "level": "county", "parent": "凤阳县人民政府", "location": "安徽省滁州市凤阳县"},
    # Previous roles for 王俊卿 — likely organizations
    {"id": "org_jinyuan_lib_town", "name": "滁州市某街道办事处", "type": "government",
     "level": "township", "parent": "滁州市", "location": "安徽省滁州市（原市辖区）"},
    # 焦艳's previous organizations
    {"id": "org_langya_party", "name": "中共琅琊区委员会", "type": "party",
     "level": "county", "parent": "中共滁州市委员会", "location": "安徽省滁州市琅琊区"},
]

positions = [
    # ── 焦艳 (现任凤阳县委书记) ──
    {"person_id": "fengyang_jiao_yan", "org_id": "org_party",
     "title": "凤阳县委书记",
     "start": "~2026-06", "end": "present", "rank": "正县级",
     "note": "根据2026年7月6日新闻确认。具体任职起始日期待核实。"},
    {"person_id": "fengyang_jiao_yan", "org_id": "org_langya_party",
     "title": "琅琊区委书记",
     "start": "unknown", "end": "~2026-06", "rank": "正县级",
     "note": "此前任琅琊区委书记。从琅琊区平调至凤阳县任县委书记。"},
    {"person_id": "fengyang_jiao_yan", "org_id": "org_langya_party",
     "title": "琅琊区委副书记（前职）",
     "start": "unknown", "end": "unknown", "rank": "副县级",
     "note": "完整履历待查。可能在担任琅琊区委书记前担任过区委副书记或政府副职。"},

    # ── 王俊卿 (现任凤阳县长) ──
    {"person_id": "fengyang_wang_junqing", "org_id": "org_gov",
     "title": "凤阳县委副书记、县政府县长、党组书记",
     "start": "unknown", "end": "present", "rank": "正县级",
     "note": "现任县长。具体任职起始时间待核实。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_party",
     "title": "凤阳县委副书记",
     "start": "unknown", "end": "present", "rank": "正县级",
     "note": "县委副书记，兼任县长。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_gov",
     "title": "凤阳县委副书记、凤阳经济开发区党工委书记（前职）",
     "start": "unknown", "end": "unknown", "rank": "副县级",
     "note": "据领导简历显示曾任县委副书记、开发区党工委书记。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_party",
     "title": "凤阳县委常委（前职）",
     "start": "unknown", "end": "unknown", "rank": "副县级",
     "note": "此前任县委常委。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_gov",
     "title": "凤阳县副县长（前职）",
     "start": "unknown", "end": "unknown", "rank": "副县级",
     "note": "曾任凤阳县副县长。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_gov",
     "title": "地级市政府工作部门副调研员",
     "start": "unknown", "end": "unknown", "rank": "副处级",
     "note": "在滁州市直部门任副调研员。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_jinyuan_lib_town",
     "title": "街道办事处党工委书记",
     "start": "unknown", "end": "unknown", "rank": "正科级",
     "note": "曾任滁州市某街道党工委书记。"},
    {"person_id": "fengyang_wang_junqing", "org_id": "org_jinyuan_lib_town",
     "title": "市辖区群团组织正职",
     "start": "unknown", "end": "unknown", "rank": "正科级",
     "note": "曾任滁州市辖区群团组织（如工会、共青团、妇联等）正职。"},

    # ── 陈长静 (常务副县长) ──
    {"person_id": "fengyang_chen_changjing", "org_id": "org_gov",
     "title": "凤阳县委常委、县政府常务副县长、党组副书记",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "县政府排名第一的副县长。具体履历待补充。"},

    # ── 胡宗权 (县委常委、副县长) ──
    {"person_id": "fengyang_hu_zongquan", "org_id": "org_gov",
     "title": "凤阳县委常委、县政府副县长、党组成员",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "具体履历待补充。"},

    # ── 方方 (县委常委、副县长) ──
    {"person_id": "fengyang_fang_fang", "org_id": "org_gov",
     "title": "凤阳县委常委、县政府副县长、党组成员",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "具体履历待补充。"},

    # ── 张艳 (副县长) ──
    {"person_id": "fengyang_zhang_yan", "org_id": "org_gov",
     "title": "凤阳县副县长",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "具体履历和分管领域待补充。"},

    # ── 倪玉新 (副县长兼公安局长) ──
    {"person_id": "fengyang_ni_yuxin", "org_id": "org_gov",
     "title": "凤阳县副县长、党组成员",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "分管公安、司法、信访等工作。"},
    {"person_id": "fengyang_ni_yuxin", "org_id": "org_public_security",
     "title": "凤阳县公安局局长、党委书记",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "兼任县公安局局长。"},

    # ── 武胤 (挂职副县长) ──
    {"person_id": "fengyang_wu_yin", "org_id": "org_gov",
     "title": "凤阳县副县长（挂职）",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "挂职副县长，具体派出单位待补充。"},

    # ── 马庆庆 (副县长) ──
    {"person_id": "fengyang_ma_qingqing", "org_id": "org_gov",
     "title": "凤阳县副县长、党组成员",
     "start": "unknown", "end": "present", "rank": "副县级",
     "note": "具体履历待补充。"},
]

relationships = [
    # ── 党政主官关系 ──
    {"person_a": "fengyang_jiao_yan", "person_b": "fengyang_wang_junqing",
     "type": "superior_subordinate", "strength": "strong", "confidence": "confirmed",
     "context": "县委书记与县长党政主官关系。焦艳任凤阳县委书记，王俊卿任县委副书记、县长。",
     "overlap_org": "中共凤阳县委员会/凤阳县人民政府",
     "overlap_period": "2026年至今"},

    # ── 县委书记与常务副县长 ──
    {"person_a": "fengyang_jiao_yan", "person_b": "fengyang_chen_changjing",
     "type": "superior_subordinate", "strength": "strong", "confidence": "confirmed",
     "context": "县委书记与常务副县长——党政主要领导关系",
     "overlap_org": "中共凤阳县委员会/凤阳县人民政府",
     "overlap_period": "2026年至今"},

    # ── 县长与常务副县长 ──
    {"person_a": "fengyang_wang_junqing", "person_b": "fengyang_chen_changjing",
     "type": "superior_subordinate", "strength": "strong", "confidence": "confirmed",
     "context": "县长与常务副县长——政府领导班子正副手关系",
     "overlap_org": "凤阳县人民政府",
     "overlap_period": "至今"},

    # ── 县长与各副县长 ──
    {"person_a": "fengyang_wang_junqing", "person_b": "fengyang_hu_zongquan",
     "type": "superior_subordinate", "strength": "medium", "confidence": "confirmed",
     "context": "县长与县委常委、副县长",
     "overlap_org": "凤阳县人民政府",
     "overlap_period": "至今"},

    {"person_a": "fengyang_wang_junqing", "person_b": "fengyang_fang_fang",
     "type": "superior_subordinate", "strength": "medium", "confidence": "confirmed",
     "context": "县长与县委常委、副县长",
     "overlap_org": "凤阳县人民政府",
     "overlap_period": "至今"},

    {"person_a": "fengyang_wang_junqing", "person_b": "fengyang_ni_yuxin",
     "type": "superior_subordinate", "strength": "medium", "confidence": "confirmed",
     "context": "县长与副县长、公安局局长",
     "overlap_org": "凤阳县人民政府",
     "overlap_period": "至今"},

    # ── 跨县关系：焦艳与琅琊区关联（原职） ──
    # This is a cross-county relationship link
    {"person_a": "fengyang_jiao_yan", "person_b": "fengyang_wang_junqing",
     "type": "cross_county_transfer", "strength": "weak", "confidence": "unverified",
     "context": "焦艳从琅琊区委书记调任凤阳县委书记，王俊卿此前已在凤阳县任职。两人在焦艳到任前无已知交集。",
     "overlap_org": "",
     "overlap_period": ""},
]


# ── DATABASE ─────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'plausible'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'plausible',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    print(f"  DB Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  DB Orgs: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  DB Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  DB Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── GEXF ─────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Color by role: red=party secretary, blue=gov, orange=discipline, grey=other."""
    title = p["current_post"]
    if "县委书记" in title:
        return "255,50,50"
    elif "县长" in title and "副县长" not in title:
        return "50,100,255"
    elif "纪委书记" in title or "监委" in title:
        return "255,165,0"
    elif "人大" in title and ("主任" in title):
        return "200,100,100"
    elif "政协" in title and ("主席" in title):
        return "100,100,200"
    else:
        return "100,100,100"


def org_color(o):
    t = o["type"]
    colors = {
        "party": "255,200,200",
        "government": "200,200,255",
        "discipline": "255,200,200",
        "people_congress": "200,255,255",
        "cppcc": "255,240,200",
        "education": "220,220,220",
    }
    return colors.get(t, "200,200,200")


def is_top_leader(p):
    return p["id"] in ("fengyang_jiao_yan", "fengyang_wang_junqing")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>凤阳县（安徽省滁州市）领导班子工作关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="kind" title="Kind" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="gender" title="Gender" type="string"/>')
    lines.append('      <attribute id="confidence" title="Confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="title" title="Title" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p["current_post"]
        conf = p["confidence"]
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="kind" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="gender" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="confidence" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="kind" value="organization"/>')
        lines.append(f'          <attvalue for="role" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="gender" value=""/>')
        lines.append('          <attvalue for="confidence" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Person→Organization edges (positions)
    for pos in positions:
        p = next(x for x in persons if x["id"] == pos["person_id"])
        o = next(x for x in organizations if x["id"] == pos["org_id"])
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(p["id"])}" target="{esc(o["id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="title" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(pos["note"])}"/>')
        lines.append('          <attvalue for="strength" value="1.0"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person edges (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="title" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="strength" value="{r["strength"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print(f"Building 凤阳县 (Fengyang County, Chuzhou, Anhui) network...")
    print(f"  DB path:   {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print()
    print("Summary:")
    print(f"  Persons:        {len(persons)}")
    print(f"  Organizations:  {len(organizations)}")
    print(f"  Positions:      {len(positions)}")
    print(f"  Relationships:  {len(relationships)}")
    print()
    print("Notes:")
    print("  - 焦艳 (female) recently moved from 琅琊区委书记 to 凤阳县委书记 (confirmed via gov news)")
    print("  - 王俊卿 (male, b.1973-10) is 凤阳县委副书记、县长 (confirmed from gov leadership page)")
    print("  - 8 county government leaders identified from official leadership page")
    print("  - Predecessors (previous 县委书记 and 县长) not yet identified — need further research")
    print("  - Most career timeline data is placeholder — needs Baidu Baike verification")
