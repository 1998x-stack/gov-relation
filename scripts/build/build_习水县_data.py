#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 习水县 (Xishui County), 遵义市, 贵州省.

Level: 县
Province: 贵州省
Parent city: 遵义市
Targets: 县委书记 & 县长
Task ID: guizhou_习水县
Investigation date: 2026-08-05

Research sources (all official county government website 习水县人民政府 www.xsx.gov.cn):
  - 领导之窗·政府领导: https://www.xsx.gov.cn/zwgk/ldzc/zfld/ (刘定杰/冉娟/黄能强/孙煜/王伟/张歆/王凯/周光亮 profiles)
  - 习水要闻 news 2026-06 ~ 2026-08:
      https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260714_90617215.html (冉崇庆到永安镇调研 — 县委书记)
      https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html (县委理论学习中心组 — 冉崇庆主持, 名单载领导班子)
      https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260724_90660166.html (县委常委会 — 冉崇庆主持, 刘定杰/冯沛红/苟明利出席)
      https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260724_90660105.html (县长见面日 — 刘定杰主持, 罗定宇/周光亮参加)
  - 遵义市 references: scripts/build/build_遵义市_data.py (冉崇庆曾任遵义市人民政府副市长)

Confidence notes:
  - 冉崇庆 (县委书记): confirmed via multiple official 2026-07 news articles. Earlier career
    (birth year, education, prior posts before 遵义市副市长) is UNVERIFIED — open gap.
  - 刘定杰 (县委副书记、县长): confirmed via official 领导之窗 profile + news.
  - 县政府领导班子 (冉/黄/孙/王伟/张歆/王凯/周光亮): confirmed via official 领导之窗 profiles.
  - 县委副书记 陈平国/阚龙霞, 人大主任 冯桂华, 政协主席 苟明利, 副县长 罗定宇: confirmed via official 习水要闻 news.
  - Birth/birthplace/education for several leaders: from profiles where published; otherwise blank (unverified).
  - Predecessors (前任县委书记/县长) and exact appointment dates: NOT found during this run (search
    engines degraded: Exa rate-limited, Baidu/Bing/Sogou blocked, Baike 403). Open gap.
  - Web search was degraded; all core data confirmed from the official county government website.
"""
# process_tmp.py required tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "习水县"
TODAY = datetime.now().strftime("%Y%m%d")

# Staging paths (written into data/tmp/guizhou_习水县/)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ 县委主要领导（一把手／二把手）═══════
    {
        "id": 1,
        "name": "冉崇庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共习水县委书记",
        "current_org": "中共习水县委",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260714_90617215.html; https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html"
    },
    {
        "id": 2,
        "name": "刘定杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "贵州遵义",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委副书记、县人民政府党组书记、县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/202412/t20241211_86333244.html"
    },
    # ═══════ 县委副书记 ═══════
    {
        "id": 3,
        "name": "陈平国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委副书记",
        "current_org": "中共习水县委",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html"
    },
    {
        "id": 4,
        "name": "阚龙霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委副书记",
        "current_org": "中共习水县委",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html; https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260724_90660166.html"
    },
    # ═══════ 县委常委、副县长 ═══════
    {
        "id": 5,
        "name": "冉娟",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1982年3月",
        "birthplace": "",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委常委、县政府党组成员、副县长（分管常务工作）",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/201908/t20190824_81943491.html"
    },
    {
        "id": 6,
        "name": "黄能强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年3月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委常委、县政府党组成员、副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/202506/t20250609_88112789.html"
    },
    {
        "id": 7,
        "name": "孙煜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年5月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县委常委、县人民政府党组成员、副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/202506/t20250609_88112794.html"
    },
    # ═══════ 县政府副县长 ═══════
    {
        "id": 8,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "大学学历，教育学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人民政府党组成员、副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/201908/t20190824_81943488.html"
    },
    {
        "id": 9,
        "name": "张歆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人民政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "习水县公安局",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/202405/t20240509_84607275.html"
    },
    {
        "id": 10,
        "name": "王凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年10月",
        "birthplace": "",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人民政府党组成员、副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/201908/t20190824_79355908.html"
    },
    {
        "id": 11,
        "name": "周光亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "硕士研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人民政府党组成员、副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/zwgk/ldzc/zfld/201908/t20190824_81943490.html"
    },
    {
        "id": 12,
        "name": "罗定宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人民政府副县长",
        "current_org": "习水县人民政府",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260724_90660105.html"
    },
    # ═══════ 县人大 / 政协 ═══════
    {
        "id": 13,
        "name": "冯沛红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "习水县人大常委会主任",
        "current_org": "习水县人大常委会",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html"
    },
    {
        "id": 14,
        "name": "苟明利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协习水县委员会主席",
        "current_org": "政协习水县委员会",
        "source": "https://www.xsx.gov.cn/xwzx/xsyw/202607/t20260717_90631174.html"
    },
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共习水县委", "type": "党委", "level": "县级", "parent": "中共遵义市委", "location": "遵义市习水县"},
    {"id": 2, "name": "习水县人民政府", "type": "政府", "level": "县级", "parent": "遵义市人民政府", "location": "遵义市习水县"},
    {"id": 3, "name": "习水县公安局", "type": "政府", "level": "县级", "parent": "习水县人民政府", "location": "遵义市习水县"},
    {"id": 4, "name": "习水县人大常委会", "type": "人大", "level": "县级", "parent": "遵义市人大常委会", "location": "遵义市习水县"},
    {"id": 5, "name": "政协习水县委员会", "type": "政协", "level": "县级", "parent": "政协遵义市委员会", "location": "遵义市习水县"},
    {"id": 6, "name": "遵义市人民政府", "type": "政府", "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省遵义市"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 冉崇庆 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共习水县委书记", "start": "", "end": "present", "rank": "正处级",
     "note": "主持县委全面工作。2026年7月以县委书记身份主持县委常委会并赴永安镇调研。早前曾任遵义市人民政府副市长（遵义市政府官网机构简介，见scripts/build/build_遵义市_data.py）。"},
    {"id": 2, "person_id": 1, "org_id": 6, "title": "遵义市人民政府副市长", "start": "", "end": "", "rank": "副厅级",
     "note": "遵义市政府官网机构简介列入副市长（兼任或此前曾任）；随后任习水县委书记。"},
    # 刘定杰 — 县长
    {"id": 3, "person_id": 2, "org_id": 1, "title": "习水县委副书记、县人民政府党组书记", "start": "", "end": "present", "rank": "正处级",
     "note": "兼任县政府党组书记。"},
    {"id": 4, "person_id": 2, "org_id": 2, "title": "习水县县长", "start": "", "end": "present", "rank": "正处级",
     "note": "领导县政府全面工作，负责人事、审计。主持县政府常务会议。"},
    # 县委副书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "习水县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年7月16日出席县委理论学习中心组。"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "习水县委副书记", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年7月16日、7月23日出席县委会议。"},
    # 县委常委、副县长
    {"id": 7, "person_id": 5, "org_id": 2, "title": "习水县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管常务工作，分管县发展改革局等。"},
    {"id": 8, "person_id": 6, "org_id": 2, "title": "习水县委常委、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责珠海东西部协作和对口交流。"},
    {"id": 9, "person_id": 7, "org_id": 2, "title": "习水县委常委、副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "负责政务公开、政务服务、行政审批改革。"},
    # 副县长
    {"id": 10, "person_id": 8, "org_id": 2, "title": "习水县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 11, "person_id": 9, "org_id": 2, "title": "习水县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "兼任县公安局党委书记、局长，主持公安全面工作。"},
    {"id": 12, "person_id": 9, "org_id": 3, "title": "习水县公安局党委书记、局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 13, "person_id": 10, "org_id": 2, "title": "习水县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"id": 14, "person_id": 11, "org_id": 2, "title": "习水县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "2026年7月13日与县委书记冉崇庆一同到永安镇调研防汛。"},
    {"id": 15, "person_id": 12, "org_id": 2, "title": "习水县人民政府副县长", "start": "", "end": "present", "rank": "副处级",
     "note": "分管乡村振兴。"},
    # 四套班子
    {"id": 16, "person_id": 13, "org_id": 4, "title": "习水县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"id": 17, "person_id": 14, "org_id": 5, "title": "政协习水县委员会主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记冉崇庆与县长刘定杰党政正职搭档", "overlap_org": "中共习水县委/习水县政府", "overlap_period": "2026"},
    {"id": 2, "person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导县委副书记陈平国", "overlap_org": "中共习水县委", "overlap_period": "2026"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委副书记阚龙霞", "overlap_org": "中共习水县委", "overlap_period": "2026"},
    {"id": 4, "person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记领导县委常委、常务副县长冉娟", "overlap_org": "中共习水县委", "overlap_period": "2026"},
    {"id": 5, "person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记领导县委常委、副县长黄能强", "overlap_org": "中共习水县委", "overlap_period": "2026"},
    {"id": 6, "person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记领导县委常委、副县长孙煜", "overlap_org": "中共习水县委", "overlap_period": "2026"},
    {"id": 7, "person_a": 2, "person_b": 5, "type": "上下级", "context": "县长领导常务副县长冉娟", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 8, "person_a": 2, "person_b": 6, "type": "上下级", "context": "县长领导副县长黄能强", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 9, "person_a": 2, "person_b": 7, "type": "上下级", "context": "县长领导副县长孙煜", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 10, "person_a": 2, "person_b": 8, "type": "上下级", "context": "县长领导副县长王伟", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 11, "person_a": 2, "person_b": 9, "type": "上下级", "context": "县长领导副县长、公安局长张歆", "overlap_org": "习水县人民政府/习水县公安局", "overlap_period": "2026"},
    {"id": 12, "person_a": 2, "person_b": 10, "type": "上下级", "context": "县长领导副县长王凯", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 13, "person_a": 2, "person_b": 11, "type": "上下级", "context": "县长领导副县长周光亮", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 14, "person_a": 2, "person_b": 12, "type": "上下级", "context": "县长领导副县长罗定宇", "overlap_org": "习水县人民政府", "overlap_period": "2026"},
    {"id": 15, "person_a": 1, "person_b": 11, "type": "同级协作", "context": "县委书记冉崇庆与副县长周光亮一同到永安镇调研防汛", "overlap_org": "习水县永安镇", "overlap_period": "2026-07-13"},
    {"id": 16, "person_a": 1, "person_b": 13, "type": "同级协作", "context": "县委书记与县人大常委会主任冯桂红同台出席县委会议", "overlap_org": "习水县四套班子", "overlap_period": "2026"},
    {"id": 17, "person_a": 1, "person_b": 14, "type": "同级协作", "context": "县委书记与县政协主席苟明利同台出席县委会议", "overlap_org": "习水县四套班子", "overlap_period": "2026"},
    {"id": 18, "person_a": 2, "person_b": 13, "type": "同级协作", "context": "县长与县人大常委会主任冯桂红同台出席县委会议", "overlap_org": "习水县四套班子", "overlap_period": "2026"},
    {"id": 19, "person_a": 2, "person_b": 14, "type": "同级协作", "context": "县长与县政协主席苟明利同台出席县委会议", "overlap_org": "习水县四套班子", "overlap_period": "2026"},
]

# ── SQLite Build ───────────────────────────────────────────────────────────
conn = sqlite3.connect(str(DB_PATH))
cur = conn.cursor()
conn.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )
for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )
for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )
for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )
conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post:
        return "255,50,50"
    elif "县长" in post and "副" not in post:
        return "50,100,255"
    elif "副县长" in post:
        return "50,120,255"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    return any(kw in p.get("current_post", "") for kw in ("书记", "县长"))

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>习水县领导班子工作关系网络 - 贵州省遵义市</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"习水县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print("Confidence notes:")
print("  - 冉崇庆 (县委书记): confirmed via official 2026-07 news; earlier career unverified (gap)")
print("  - 刘定杰 (县长): confirmed via official profile + news")
print("  - 县政府领导: confirmed via official 领导之窗 profiles")
print("  - 县委副书记/人大/政协: confirmed via official 习水要闻")
print("  - Predecessors & appointment dates: not verified this run (search degraded)")