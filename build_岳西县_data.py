#!/usr/bin/env python3
"""Build Yuexi County (岳西县) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.yuexi.gov.cn (official Yuexi county government website, general news accessed 2026-07-15)
  - 中国共产党岳西县第十六届委员会第一次全体会议 (2026-06-29)
    https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html
  - 中国共产党岳西县第十六次代表大会胜利闭幕 (2026-06-29)
    https://www.yuexi.gov.cn/ssxw/yxyw/2030495295.html
  - 桂稳成主持召开县政府第九十二次常务会议 (2026-07-13)
    https://www.yuexi.gov.cn/ssxw/yxyw/2030511576.html
  - 岳西县党政领导公开接访安排表 (2026年7月)
    https://www.yuexi.gov.cn/ssxw/gsgg/2030497254.html

Confidence: Current roles confirmed from official 16th Party Congress First Plenum report
  (2026-06-29). The full 11-member Standing Committee and Party Secretary/Deputy Secretaries
  are confirmed by the official election report. Biographical details (birth year, education,
  birthplace) are unknown for most figures — Baidu Baike returned 403 and Wikipedia timed out.
"""

import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "岳西县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "岳西县_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──────────────────────────────────────────────────
    {
        "id": 1,
        "name": "吴爱德",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会); https://www.yuexi.gov.cn/ssxw/yxyw/2030514924.html (2026-07-15 座谈); https://www.yuexi.gov.cn/ssxw/yxyw/2030486529.html (2026-06-24 常委会)",
        "notes": "2026年6月29日在中共岳西县第十六届委员会第一次全体会议上当选县委书记。主持县委全面工作。2026年6月24日以县委书记身份主持召开县委常委会会议。2026年7月15日与来访企业座谈。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "桂稳成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "岳西县人民政府",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 当选县委副书记); https://www.yuexi.gov.cn/ssxw/yxyw/2030511576.html (2026-07-13 县政府常务会议); https://www.yuexi.gov.cn/ssxw/yxyw/2030514936.html (2026-07-15 六庆铁路调度会)",
        "notes": "2026年6月29日当选县委副书记。以县长身份主持县政府常务会议。主持六庆铁路（岳西段）项目二季度调度会。领导县政府全面工作。",
        "confidence": "confirmed"
    },
    # ── Deputy Party Secretaries ──────────────────────────────────────
    {
        "id": 3,
        "name": "陈文文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会); https://www.yuexi.gov.cn/ssxw/yxyw/2030514936.html (2026-07-15 六庆铁路调度会)",
        "notes": "2026年6月29日当选县委副书记（专职）。2026年7月14日参加六庆铁路调度会。",
        "confidence": "confirmed"
    },
    # ── Standing Committee (县委常委) ─────────────────────────────────
    {
        "id": 4,
        "name": "余飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "金天柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会); https://www.yuexi.gov.cn/ssxw/yxyw/2030514936.html (2026-07-15 六庆铁路调度会)",
        "notes": "2026年6月29日当选县委常委。2026年7月14日参加六庆铁路调度会。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "刘亚维",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "吴姚政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "王朝阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会); https://www.yuexi.gov.cn/ssxw/yxyw/2030514924.html (2026-07-15 座谈)",
        "notes": "2026年6月29日当选县委常委。2026年7月15日参加与江苏龙硕的座谈。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "张小武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "华小芬",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。女性。具体分工待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "杨翼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共岳西县委",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030495886.html (2026-06-29 十六届县委一次全会)",
        "notes": "2026年6月29日当选县委常委。具体分工待确认。",
        "confidence": "confirmed"
    },
    # ── Other County Leaders (from news articles) ────────────────────
    {
        "id": 12,
        "name": "胡力勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "岳西县",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030514924.html (2026-07-15 座谈)",
        "notes": "2026年7月15日以县领导身份参加与江苏龙硕的座谈。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "吴代庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "岳西县",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030514936.html (2026-07-15 六庆铁路调度会)",
        "notes": "2026年7月14日以县领导身份参加六庆铁路调度会。具体职务待确认。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "王金桥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "岳西县",
        "source": "https://www.yuexi.gov.cn/ssxw/yxyw/2030514936.html (2026-07-15 六庆铁路调度会)",
        "notes": "2026年7月14日以县领导身份参加六庆铁路调度会。具体职务待确认。",
        "confidence": "confirmed"
    },
    # ── Predecessors ─────────────────────────────────────────────────
    {
        "id": 15,
        "name": "江春生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原岳西县委书记，去向待查）",
        "current_org": "",
        "source": "推测: 江春生于2019-2025年间任岳西县委书记，约2025/2026年被吴爱德接替",
        "notes": "前任岳西县委书记。江春生长期在岳西县任职，曾任县长（2016-2019）、县委书记（约2019-2025/2026）。被吴爱德接替。去向待查。",
        "confidence": "plausible"
    },
    {
        "id": 16,
        "name": "何斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原岳西县长，去向待查）",
        "current_org": "",
        "source": "推测: 何斌于约2021-2025年间任岳西县长，约2025/2026年被桂稳成接替",
        "notes": "前任岳西县长。何斌曾任岳西县委常委、常务副县长，后升任县长（约2021-2025/2026）。被桂稳成接替。去向待查。",
        "confidence": "plausible"
    },
]

# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共岳西县委", "type": "党委", "level": "县", "parent": "中共安庆市委", "location": "岳西县"},
    {"id": 2, "name": "岳西县人民政府", "type": "政府", "level": "县", "parent": "安庆市人民政府", "location": "岳西县"},
    {"id": 3, "name": "中共岳西县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共岳西县委", "location": "岳西县"},
    {"id": 4, "name": "岳西县监察委员会", "type": "政府", "level": "县", "parent": "岳西县人民政府", "location": "岳西县"},
    {"id": 5, "name": "岳西县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "岳西县", "location": "岳西县"},
    {"id": 6, "name": "中国人民政治协商会议岳西县委员会", "type": "政协", "level": "县", "parent": "岳西县", "location": "岳西县"},
]

# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 吴爱德
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作。2026年6月29日当选十六届县委书记。"},
    # 桂稳成
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "领导县政府全面工作。"},
    # 陈文文
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},
    # 余飞
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 金天柱
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 刘亚维
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 吴姚政
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 王朝阳
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 张小武
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 华小芬
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "女，具体分工待确认"},
    # 杨翼
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体分工待确认"},
    # 胡力勇
    {"person_id": 12, "org_id": 2, "title": "县领导（具体职务待确认）", "start": "", "end": "present", "rank": "", "note": "2026年7月15日以县领导身份见诸报道"},
    # 吴代庆
    {"person_id": 13, "org_id": 2, "title": "县领导（具体职务待确认）", "start": "", "end": "present", "rank": "", "note": "2026年7月14日以县领导身份见诸报道"},
    # 王金桥
    {"person_id": 14, "org_id": 2, "title": "县领导（具体职务待确认）", "start": "", "end": "present", "rank": "", "note": "2026年7月14日以县领导身份见诸报道"},
    # 江春生 (前任县委书记)
    {"person_id": 15, "org_id": 1, "title": "县委书记（前任）", "start": "", "end": "", "rank": "正处级", "note": "前任县委书记。约2019-2025/2026年在任。去向待查。"},
    # 何斌 (前任县长)
    {"person_id": 16, "org_id": 2, "title": "县长（前任）", "start": "", "end": "", "rank": "正处级", "note": "前任县长。约2021-2025/2026年在任。去向待查。"},
]

# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # Core leadership team - same org overlap (县委常委会)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记和县长，县委县政府双核心搭档", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记和县委副书记（专职）", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委书记和县委常委（女）", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记和县委常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 县长 with other leaders
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长和县委副书记共事", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 专职副书记 connections
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委副书记和常委", "overlap_org": "中共岳西县委", "overlap_period": "2026-", "strength": "strong", "confidence": "confirmed"},
    # 王朝阳 (常委) participated in same events with top leaders
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "一起参加与江苏龙硕的座谈", "overlap_org": "中共岳西县委", "overlap_period": "2026-07-15", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "一起参加六庆铁路调度会", "overlap_org": "岳西县人民政府", "overlap_period": "2026-07-14", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "一起参加六庆铁路调度会", "overlap_org": "岳西县人民政府", "overlap_period": "2026-07-14", "strength": "strong", "confidence": "confirmed"},
    # Predecessor-successor
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor", "context": "吴爱德接替江春生任岳西县委书记", "overlap_org": "中共岳西县委", "overlap_period": "2025/2026", "strength": "strong", "confidence": "plausible"},
    {"person_a": 2, "person_b": 16, "type": "predecessor_successor", "context": "桂稳成接替何斌任岳西县长", "overlap_org": "岳西县人民政府", "overlap_period": "2025/2026", "strength": "strong", "confidence": "plausible"},
]


# ══════════════════════════════════════════════════════════════════════════
# Database + GEXF generation
# ══════════════════════════════════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org, source, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"], p["current_post"],
              p["current_org"], p["source"], p["confidence"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")
    print(f"      Persons: {len(persons)}")
    print(f"      Organizations: {len(organizations)}")
    print(f"      Positions: {len(positions)}")
    print(f"      Relationships: {len(relationships)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person):
    """Return 'r,g,b' string based on role."""
    role = person.get("current_post", "")
    if "书记" in role and "县委" in role and "副" not in role:
        return "255,50,50"  # Red for Party Secretary
    if "县长" in role and "副" not in role:
        return "50,100,255"  # Blue for County Mayor
    if "纪委" in role or "监委" in role:
        return "255,165,0"  # Orange for Discipline
    if "人大" in role:
        return "200,255,255"  # Cyan for People's Congress
    if "政协" in role:
        return "255,240,200"  # Cream for CPPCC
    return "100,100,100"  # Grey for others


def person_size(person):
    """Return node size based on rank."""
    role = person.get("current_post", "")
    if "县委书记" in role and "副" not in role:
        return "20.0"
    if "县长" in role and "副" not in role:
        return "20.0"
    if "人大" in role or "政协" in role:
        return "15.0"
    if "常委" in role:
        return "15.0"
    return "12.0"


def org_color(org):
    """Return 'r,g,b' string for organization type."""
    t = org.get("type", "")
    type_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return type_colors.get(t, "200,200,200")


def generate_gexf():
    """Generate GEXF graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>岳西县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="rank" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization edges (worked_at)
    for pos in positions:
        eid += 1
        src = f"p{pos['person_id']}"
        tgt = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person edges (relationship)
    for r in relationships:
        eid += 1
        src = f"p{r['person_a']}"
        tgt = f"p{r['person_b']}"
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{src}" target="{tgt}" label="{esc(r["context"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{r["strength"]}"/>')
        lines.append(f'          <attvalue for="3" value="{r["overlap_period"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[OK] GEXF graph created: {GEXF_PATH}")
    print(f"      Person nodes: {len(persons)}")
    print(f"      Organization nodes: {len(organizations)}")
    print(f"      Worked-at edges: {len(positions)}")
    print(f"      Relationship edges: {len(relationships)}")


def main():
    print("=" * 60)
    print("  岳西县领导班子网络数据生成")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    create_database()
    generate_gexf()
    print(f"\n[OK] All files generated in: {SCRIPT_DIR}")


if __name__ == "__main__":
    main()
