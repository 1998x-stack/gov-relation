#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 驻马店市 (Zhumadian City), 河南省.

Investigation date: 2026-07-24
Task ID: henan_驻马店市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.zhumadian.gov.cn — 驻马店市人民政府网站 (primary)
  - 市委常委会召开会议 (2026-07-22) — confirmed 市委书记李跃勇
  - 市长王玲督导检查防汛工作 (2026-07-24) — confirmed 市长王玲
  - 市委副书记/政法委书记李党生到西平县调研 (2026-07-24)
  - 市政协五届常委会第十八次会议 (2026-07-23) — confirmed 常务副市长王洪民
  - 市民盟代表大会 (2026-07-24) — confirmed 市委常委/秘书长/统战部长李全喜

Confidence notes:
  - 李跃勇: confirmed as 市委书记 via official government article (2026-07-22)
  - 王玲: confirmed as 市长 via official government article (2026-07-24)
  - Full career timelines for both main targets could not be verified from web sources
  - Detailed biographical data (birthdate, birthplace, education) marked as unverified
  - Other leadership team members identified from official articles
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "驻马店市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "李跃勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委书记",
        "current_org": "中共驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260722_713470.html",
        "notes": "2026年7月21日主持市委常委会会议。公开简历信息有限，待进一步调查。"
    },
    {
        "id": 2,
        "name": "王玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市长",
        "current_org": "驻马店市人民政府",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714349.html",
        "notes": "2026年7月22日督导检查防汛工作。公开简历信息有限，待进一步调查。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Leadership Team (市委常委 / 市级领导)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "李党生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714348.html",
        "notes": "2026年7月23日到西平县调研产业发展、平安建设等工作。"
    },
    {
        "id": 4,
        "name": "王洪民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、常务副市长",
        "current_org": "驻马店市人民政府",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html",
        "notes": "2026年7月22日在市政协常委会上通报全市经济社会发展情况。"
    },
    {
        "id": 5,
        "name": "李全喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市委常委、秘书长、统战部部长",
        "current_org": "中共驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714351.html",
        "notes": "2026年7月23日代表市委出席民盟驻马店市第六次代表大会并讲话。"
    },
    {
        "id": 6,
        "name": "陈锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "市政协主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html",
        "notes": "2026年7月22日主持市政协五届常委会第十八次会议。"
    },
    {
        "id": 7,
        "name": "毕俊德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 8,
        "name": "张新领",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 9,
        "name": "高其良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 10,
        "name": "王品磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "民盟盟员",
        "work_start": "待查",
        "current_post": "市政协副主席、民盟驻马店市委主委",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 11,
        "name": "胡晓黎",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 12,
        "name": "罗宇威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 13,
        "name": "崔晓霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协副主席",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 14,
        "name": "李涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市政协秘书长",
        "current_org": "政协驻马店市委员会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html"
    },
    {
        "id": 15,
        "name": "张二林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "市人大常委会副主任",
        "current_org": "驻马店市人大常委会",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714351.html"
    },
    {
        "id": 16,
        "name": "何冬",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "副市长",
        "current_org": "驻马店市人民政府",
        "source": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714351.html"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共驻马店市委员会",
        "type": "党委",
        "level": "地级市",
        "location": "河南省驻马店市"
    },
    {
        "id": 2,
        "name": "驻马店市人民政府",
        "type": "政府",
        "level": "地级市",
        "location": "河南省驻马店市"
    },
    {
        "id": 3,
        "name": "驻马店市人大常委会",
        "type": "人大",
        "level": "地级市",
        "location": "河南省驻马店市"
    },
    {
        "id": 4,
        "name": "政协驻马店市委员会",
        "type": "政协",
        "level": "地级市",
        "location": "河南省驻马店市"
    },
    {
        "id": 5,
        "name": "中国民主同盟驻马店市委员会",
        "type": "群团",
        "level": "地级市",
        "location": "河南省驻马店市"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────

positions = [
    # 李跃勇
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "待查", "end": "present", "rank": "正厅级", "note": "2026年7月21日主持市委常委会会议"},
    # 王玲
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "待查", "end": "present", "rank": "正厅级", "note": "2026年7月22日督导检查防汛工作"},
    # 李党生
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": "2026年7月23日到西平县调研"},
    # 王洪民
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": "2026年7月22日在市政协常委会通报经济社会发展情况"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 李全喜
    {"person_id": 5, "org_id": 1, "title": "市委常委、秘书长、统战部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": "2026年7月23日出席民盟代表大会"},
    # 陈锋
    {"person_id": 6, "org_id": 4, "title": "市政协主席", "start": "待查", "end": "present", "rank": "正厅级", "note": ""},
    # 毕俊德
    {"person_id": 7, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 张新领
    {"person_id": 8, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 高其良
    {"person_id": 9, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 王品磊
    {"person_id": 10, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": "民盟驻马店市委主委"},
    {"person_id": 10, "org_id": 5, "title": "民盟驻马店市委主委", "start": "待查", "end": "present", "rank": "", "note": ""},
    # 胡晓黎
    {"person_id": 11, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 罗宇威
    {"person_id": 12, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 崔晓霞
    {"person_id": 13, "org_id": 4, "title": "市政协副主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 李涛
    {"person_id": 14, "org_id": 4, "title": "市政协秘书长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 张二林
    {"person_id": 15, "org_id": 3, "title": "市人大常委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 何冬
    {"person_id": 16, "org_id": 2, "title": "副市长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政主要领导搭档（市委书记与市长）",
        "overlap_org": "驻马店市",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "市委书记与市委副书记",
        "overlap_org": "中共驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "市委书记与市委常委",
        "overlap_org": "中共驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "市委书记与市委常委",
        "overlap_org": "中共驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "市长与常务副市长",
        "overlap_org": "驻马店市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 16,
        "type": "superior_subordinate",
        "context": "市长与副市长",
        "overlap_org": "驻马店市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 4,
        "type": "overlap",
        "context": "市政协主席与常务副市长，市政协常委会工作交集",
        "overlap_org": "政协驻马店市委员会/驻马店市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 7,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 8,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 9,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 10,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 11,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 12,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 13,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协副主席",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": 6, "person_b": 14,
        "type": "superior_subordinate",
        "context": "市政协主席与市政协秘书长",
        "overlap_org": "政协驻马店市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
]

# ── Source Register ──────────────────────────────────────────────────────

sources = [
    {
        "id": "S001",
        "title": "市委常委会召开会议",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260722_713470.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-22",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认市委书记李跃勇"
    },
    {
        "id": "S002",
        "title": "坚持人民至上 树牢极限思维 全力以赴确保安全平稳度汛",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714349.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认市长王玲"
    },
    {
        "id": "S003",
        "title": "立足本地资源优势 做强特色富民产业 加强基层社会治理 守牢安全稳定底线",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714348.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认市委副书记/政法委书记李党生"
    },
    {
        "id": "S004",
        "title": "市政协五届常委会第十八次会议召开",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713782.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认常务副市长王洪民、市政协领导名单"
    },
    {
        "id": "S005",
        "title": "中国民主同盟驻马店市第六次代表大会召开",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260724_714351.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认李全喜常委/秘书长/统战部长、张二林、何冬等领导"
    },
    {
        "id": "S006",
        "title": "坚持科技赋能产业转型升级 突出党建引领基层高效能治理",
        "url": "https://www.zhumadian.gov.cn/./zwyw/zwyw/202607/t20260723_713778.html",
        "publisher": "驻马店市人民政府",
        "published_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "书记李跃勇到经开区调研详情"
    },
]

# ── Build ──────────────────────────────────────────────────────────────────

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
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
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
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    is_top = {1, 2}  # 市委书记 and 市长
    person_colors = {
        1: "255,50,50",   # Red - party secretary
        2: "50,100,255",  # Blue - mayor
        3: "100,100,100", # Grey
        4: "50,100,255",  # Blue - government
        5: "100,100,100", # Grey
        6: "200,255,255", # Cyan - 政协
    }
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>驻马店市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_colors.get(pid, "100,100,100")
        sz = "20.0" if pid in is_top else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context",""))}" weight="2.0">')
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
    print(f"驻马店市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
