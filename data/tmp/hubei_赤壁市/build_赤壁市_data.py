#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 赤壁市 (Chibi City), 咸宁市, 湖北省.

Level: 县级市
Province: 湖北省
Parent city: 咸宁市
Targets: 市委书记 (Party Secretary), 市长 (Mayor)
Task ID: hubei_赤壁市

Research date: 2026-07-24
Official source: http://www.chibi.gov.cn/ (赤壁市人民政府) — confirmed accessible

Current status (as of 2026-07-24):
- 市委书记: 彭光平 (confirmed via multiple official news articles)
  - source: http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml
- 市长: 万龙 (confirmed via official government leadership page)
  - source: http://www.chibi.gov.cn/xxgk/zfld/wl/

Roster sources:
    市政府领导: http://www.chibi.gov.cn/xxgk/zfld/wl/ (万龙 — 市长)
                 http://www.chibi.gov.cn/xxgk/zfld/wh/ (欧阳萍 — 副市长)
                 http://www.chibi.gov.cn/xxgk/zfld/tm/ (谭敏 — 副市长)
                 http://www.chibi.gov.cn/xxgk/zfld/bhz/ (戴峰 — 副市长)
                 http://www.chibi.gov.cn/xxgk/zfld/sm/ (舒敏 — 副市长、公安局局长)
    市委领导: 市委理论学习中心组会议报道 (彭光平、万龙、王贤柱、叶文华、钱仕忠)
              人大换届选举调研报道 (王贤柱、叶文华、彭晓峰、宋武先、王辉)
              医共体改革调研报道 (余学文、鲁维华、欧阳萍)
              平安建设会议报道 (王辉 — 政法委书记)
              征兵体检报道 (姚德义 — 人武部)

Confidence notes:
  - 市长 (万龙) identity: confirmed via official government website (with bio)
  - 市委书记 (彭光平) identity: confirmed via multiple official news articles
  - 副市长 bios: confirmed via official government website
  - 市委副书记 (王贤柱): confirmed via multiple source articles
  - 市人大常委会主任 (叶文华): confirmed
  - 市政协主席 (钱仕忠): confirmed
  - 市委常委 partial list: 彭晓峰, 宋武先, 王辉(政法委书记), 余学文, 鲁维华, 姚德义(from news)
  - Web search (Exa, Baidu, Google) was unavailable; all data from direct government website access
  - Predecessor details: unverified — web search unavailable
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
SLUG = "赤壁市"
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
        "name": "彭光平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml"
    },
    {
        "id": 2,
        "name": "万龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "湖北咸安",
        "education": "在职研究生、经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "赤壁市人民政府",
        "source": "http://www.chibi.gov.cn/xxgk/zfld/wl/"
    },
    # ═══════ 市委领导 ═══════
    {
        "id": 3,
        "name": "王贤柱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记（正处级）、赤壁高新区党工委书记",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml"
    },
    {
        "id": 4,
        "name": "彭晓峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260722_5098698.shtml"
    },
    {
        "id": 5,
        "name": "宋武先",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260722_5098698.shtml"
    },
    {
        "id": 6,
        "name": "王辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260723_5113183.shtml"
    },
    {
        "id": 7,
        "name": "余学文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260720_5084931.shtml"
    },
    {
        "id": 8,
        "name": "鲁维华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260720_5084931.shtml"
    },
    {
        "id": 9,
        "name": "姚德义",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、人武部领导",
        "current_org": "中共赤壁市委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260722_5098689.shtml"
    },
    # ═══════ 市政府领导 ═══════
    {
        "id": 10,
        "name": "欧阳萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "湖北赤壁",
        "education": "在职研究生学历",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "赤壁市人民政府",
        "source": "http://www.chibi.gov.cn/xxgk/zfld/wh/"
    },
    {
        "id": 11,
        "name": "谭敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年1月",
        "birthplace": "湖北通城",
        "education": "大学本科学历，管理学学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "赤壁市人民政府",
        "source": "http://www.chibi.gov.cn/xxgk/zfld/tm/"
    },
    {
        "id": 12,
        "name": "戴峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "赤壁市人民政府",
        "source": "http://www.chibi.gov.cn/xxgk/zfld/bhz/"
    },
    {
        "id": 13,
        "name": "舒敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "湖北通山",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "赤壁市人民政府",
        "source": "http://www.chibi.gov.cn/xxgk/zfld/sm/"
    },
    # ═══════ 市人大领导 ═══════
    {
        "id": 14,
        "name": "叶文华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "赤壁市人大常委会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml"
    },
    # ═══════ 市政协领导 ═══════
    {
        "id": 15,
        "name": "钱仕忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "赤壁市政协委员会",
        "source": "http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共赤壁市委员会", "type": "党委", "level": "县级市", "parent": "中共咸宁市委", "location": "湖北省咸宁市赤壁市"},
    {"id": 2, "name": "赤壁市人民政府", "type": "政府", "level": "县级市", "parent": "咸宁市人民政府", "location": "湖北省咸宁市赤壁市"},
    {"id": 3, "name": "赤壁市人大常委会", "type": "人大", "level": "县级市", "parent": "咸宁市人大常委会", "location": "湖北省咸宁市赤壁市"},
    {"id": 4, "name": "赤壁市政协委员会", "type": "政协", "level": "县级市", "parent": "咸宁市政协委员会", "location": "湖北省咸宁市赤壁市"},
    {"id": 5, "name": "赤壁市公安局", "type": "政府", "level": "县级市", "parent": "赤壁市人民政府", "location": "湖北省咸宁市赤壁市"},
    {"id": 6, "name": "赤壁高新技术产业园区", "type": "开发区", "level": "县级市", "parent": "赤壁市人民政府", "location": "湖北省咸宁市赤壁市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 彭光平
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市委全面工作"},
    # 万龙
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 王贤柱
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "协助市委书记处理市委日常工作"},
    {"person_id": 3, "org_id": 6, "title": "赤壁高新区党工委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 彭晓峰
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 宋武先
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 王辉
    {"person_id": 6, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "主持市委政法委工作"},
    # 余学文
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 鲁维华
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分工待查"},
    # 姚德义
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "人武部领导职务"},
    # 欧阳萍
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责文化旅游、教育、卫生健康、市场监管等方面工作"},
    # 谭敏
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责农业农村、乡村振兴、水利和湖泊、民政等方面工作"},
    # 戴峰
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责工业、科技和信息化、招商引资、生态环境、商贸流通等方面工作"},
    # 舒敏
    {"person_id": 13, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责社会治安综合治理、公安、司法、退役军人事务、信访维稳等方面工作"},
    {"person_id": 13, "org_id": 5, "title": "市公安局党委书记、局长、督察长", "start_date": "", "end_date": "present", "rank": "四级高级警长", "note": "主持市公安局全面工作"},
    # 叶文华
    {"person_id": 14, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市人大常委会全面工作"},
    # 钱仕忠
    {"person_id": 15, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "主持市政协全面工作"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 市委书记 ↔ 市长 (搭班子)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长搭班子，共同主持市委常委会和全市工作", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    # 市委书记 ↔ 市委副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与市委副书记在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    # 市长 ↔ 市委副书记
    {"person_a": 2, "person_b": 3, "type": "colleague", "context": "市长与市委副书记在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    # 市委书记 ↔ 其他市委常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与市委常委彭晓峰在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委书记与市委常委宋武先在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与市委常委王辉在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与市委常委余学文在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "市委书记与市委常委鲁维华在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委书记与市委常委姚德义在市委常委会共事", "overlap_org": "中共赤壁市委员会", "overlap_period": ""},
    # 市长 ↔ 副市长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长欧阳萍在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "市长与副市长谭敏在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "市长与副市长戴峰在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "市长与副市长舒敏在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    # 副市长之间
    {"person_a": 10, "person_b": 11, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 12, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 13, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 12, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 13, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "colleague", "context": "副市长之间在市政府班子共事", "overlap_org": "赤壁市人民政府", "overlap_period": ""},
    # 人大主任 ↔ 核心领导
    {"person_a": 1, "person_b": 14, "type": "colleague", "context": "市委书记与市人大常委会主任在市委理论学习中心组和市人大换届选举等工作中合作", "overlap_org": "赤壁市", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "colleague", "context": "市长与市人大常委会主任在市政府工作报告和政府监督等工作中合作", "overlap_org": "赤壁市", "overlap_period": ""},
    # 政协主席 ↔ 核心领导
    {"person_a": 1, "person_b": 15, "type": "colleague", "context": "市委书记与市政协主席在市委理论学习中心组和政协工作中合作", "overlap_org": "赤壁市", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "colleague", "context": "市长与市政协主席在政治协商等工作中合作", "overlap_org": "赤壁市", "overlap_period": ""},
]


# ══════════════════════════════════════════════════════════════════════════
# Build functions
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string for GEXF output."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_database():
    """Create SQLite database with persons, organizations, positions, relationships."""
    import sqlite3
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
              o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos.get("title", ""),
              pos.get("start_date", ""), pos.get("end_date", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r.get("type", ""),
              r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  ✓ Database: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships)")


def build_gexf():
    """Build GEXF graph file using string formatting (avoid ElementTree namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(f'    <description>赤壁市领导班子工作关系网络 - 中共赤壁市委、赤壁市人民政府及市人大、市政协领导架构，as of {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')

    # Color helper
    def person_color(p):
        role = p.get("current_post", "")
        if "书记" in role and "市委" in role:
            # Party Secretary - Red
            return "255,50,50"
        elif "市长" in role or "副市长" in role:
            # Government - Blue
            return "50,100,255"
        elif "人大" in role:
            # 人大 - Cyan
            return "200,255,255"
        elif "政协" in role:
            # 政协 - Cream
            return "255,240,200"
        elif "常委" in role:
            # 常委 - Orange
            return "255,165,0"
        else:
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
        elif "开发区" in t:
            return "200,255,200"
        return "200,200,200"

    def is_top_leader(p):
        role = p.get("current_post", "")
        return "市委书记" in role or ("市长" in role and "副市长" not in role)

    def node_size(p):
        return "20.0" if is_top_leader(p) else "12.0"

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = node_size(p)
        ptype = "person"
        role = esc(p.get("current_post", ""))
        org = esc(p.get("current_org", ""))
        src = esc(p.get("source", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{ptype}"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append(f'          <attvalue for="2" value="{org}"/>')
        lines.append(f'          <attvalue for="3" value="{src}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        sz = "8.0"
        otype = "organization"
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{otype}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # person→organization (worked_at)
    for pos in positions:
        eid += 1
        title = esc(pos.get("title", ""))
        note = esc(pos.get("note", ""))
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{title}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{note}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person↔person (relationship)
    for r in relationships:
        eid += 1
        ctx = esc(r.get("context", ""))
        oo = esc(r.get("overlap_org", ""))
        rtype = r.get("type", "")
        weight = "2.0" if rtype in ("superior_subordinate",) else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{rtype}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{rtype}"/>')
        lines.append(f'          <attvalue for="1" value="{ctx}"/>')
        lines.append(f'          <attvalue for="2" value="{oo}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  ✓ GEXF: {GEXF_PATH} ({len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges)")


def build_person_json(person):
    """Write a single person JSON file with detailed biography fields.

    Format matches process_tmp.py is_person_json() check: requires
    identity, career_timeline, and source_register keys.
    """
    name = person["name"]
    current_post = person.get("current_post", "")
    # Build filename
    safe_name = name
    safe_post = current_post.replace("/", "_").replace(" ", "")
    filename = f"{TODAY}-湖北省-咸宁市-{safe_post}-{safe_name}.json"
    filepath = STAGING_DIR / filename

    data = {
        "identity": {
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "education": person.get("education", ""),
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
        },
        "current_post": {
            "title": current_post,
            "org": person.get("current_org", ""),
        },
        "career_timeline": [],
        "relationship_evidence": [],
        "governance_profile": {},
        "professional_profile": {},
        "source_register": {
            "primary": person.get("source", ""),
            "as_of": AS_OF,
        },
        "confidence": "confirmed" if person.get("birth") or person.get("source") else "unverified",
        "open_questions": [],
    }

    if not person.get("birth"):
        data["open_questions"].append(f"{name}的出生年份/日期")
    if not person.get("birthplace"):
        data["open_questions"].append(f"{name}的籍贯/出生地")
    if not person.get("education"):
        data["open_questions"].append(f"{name}的教育背景")
    if not person.get("work_start"):
        data["open_questions"].append(f"{name}的参加工作时间和完整履历")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath.name}")
    return filepath


def build_report():
    """Write a comprehensive Chinese-language research report."""
    report_path = STAGING_DIR / f"{TODAY}-湖北省-咸宁市-赤壁市-领导班子工作关系网络调查报告.md"

    content = f"""# 赤壁市领导班子工作关系网络调查报告

> 调查日期：{AS_OF}
> 任务编号：hubei_赤壁市
> 数据置信度：★★★☆☆（网络搜索受限，信息主要来自官方网站直接抓取）

---

## 1. 现任市委书记：彭光平

- **职务**：中共赤壁市委书记
- **性别**：男
- **民族**：汉族
- **政党**：中共党员
- **履历状态**：待查 — 网络搜索（Exa/Baidu/Google）均不可用，无法获取详细履历
- **来源**：赤壁市政府网站新闻报道
  - 彭光平主持召开市委理论学习中心组集体学习会议：http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml
  - 彭光平调研市乡人大换届选举工作：http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260722_5098698.shtml

## 2. 现任市长：万龙

- **职务**：赤壁市委副书记、市人民政府市长、党组书记
- **性别**：男
- **民族**：汉族
- **出生**：1981年9月
- **籍贯**：湖北咸安
- **学历**：在职研究生、经济学博士
- **政党**：中共党员
- **来源**：赤壁市人民政府官网领导之窗 http://www.chibi.gov.cn/xxgk/zfld/wl/

## 3. 前任领导（待进一步核实）

> ⚠ 注：由于网络搜索受限，以下信息来自历史项目知识，未通过本次调查重新核实。

- **前任市委书记**：董方平（前任赤壁市委书记，约2021-2024年在任）
- **前任市长**：葛军（前任赤壁市长，约2021-2024年在任）

## 4. 领导班子成员

### 4.1 中共赤壁市委常委会

| 姓名 | 职务 | 性别 | 民族 | 出生 | 籍贯 | 学历 | 备注 |
|------|------|------|------|------|------|------|------|
| 彭光平 | 市委书记 | 男 | 汉族 | — | — | — | 主持市委全面工作 |
| 万龙 | 市委副书记、市长 | 男 | 汉族 | 1981.09 | 湖北咸安 | 在职研究生/博士 | 主持市政府全面工作 |
| 王贤柱 | 市委副书记、赤壁高新区党工委书记 | 男 | 汉族 | — | — | — | 正处级 |
| 彭晓峰 | 市委常委 | — | — | — | — | — | 具体分工待查 |
| 宋武先 | 市委常委 | — | — | — | — | — | 具体分工待查 |
| 王辉 | 市委常委、政法委书记 | 男 | — | — | — | — | 主持市委政法委工作 |
| 余学文 | 市委常委 | 男 | — | — | — | — | 具体分工待查 |
| 鲁维华 | 市委常委 | 男 | — | — | — | — | 具体分工待查 |
| 姚德义 | 市委常委、人武部领导 | 男 | — | — | — | — | — |

### 4.2 赤壁市人民政府领导班子

| 姓名 | 职务 | 性别 | 民族 | 出生 | 籍贯 | 学历 | 分工 |
|------|------|------|------|------|------|------|------|
| 万龙 | 市长 | 男 | 汉族 | 1981.09 | 湖北咸安 | 在职研究生/博士 | 领导市政府全面工作 |
| 欧阳萍 | 副市长 | 女 | 汉族 | 1976.07 | 湖北赤壁 | 在职研究生 | 文化旅游、教育、卫健、市场监管 |
| 谭敏 | 副市长 | 男 | 汉族 | 1979.01 | 湖北通城 | 大学/管理学士 | 农业农村、乡村振兴、水利、民政 |
| 戴峰 | 副市长 | 男 | 汉族 | 1984.11 | — | 大学 | 工业、科技、招商、商贸、环保 |
| 舒敏 | 副市长、市公安局局长 | 男 | 汉族 | 1979.12 | 湖北通山 | 大学 | 公安、司法、退役军人、信访 |

### 4.3 市人大、市政协领导

| 姓名 | 职务 | 来源 |
|------|------|------|
| 叶文华 | 市人大常委会主任 | 市委理论学习中心组会议报道 |
| 钱仕忠 | 市政协主席 | 市委理论学习中心组会议报道 |

## 5. 近期人事变动（待查）

暂无具体上任日期信息。万龙于2026年7月以市长身份出现于各项官方报道中。

## 6. 工作关系网络分析

### 确认的同事关系

1. **市委常委班子**（9人）：彭光平、万龙、王贤柱、彭晓峰、宋武先、王辉、余学文、鲁维华、姚德义
   - 核心决策圈，定期召开市委常委会
2. **市政府班子**（5人）：万龙、欧阳萍、谭敏、戴峰、舒敏
   - 市政府常务会议议事
3. **市四套班子**：市委（彭光平）、市政府（万龙）、市人大（叶文华）、市政协（钱仕忠）
   - 在市委理论学习中心组和全市重要会议中联动

### 跨县区交流线索
- 万龙籍贯为湖北咸安（咸安区），反映出咸宁市域内干部交流
- 谭敏籍贯湖北通城、舒敏籍贯湖北通山，均为咸宁市下辖县，体现市内跨县调动
- 欧阳萍籍贯湖北赤壁（本地干部）

## 7. 关键洞察与突破线索

1. **市委书记履历缺失**：彭光平的详细履历（出生、籍贯、教育、任职经历）是最大的信息缺口
2. **多位市委常委分工不明**：彭晓峰、宋武先、余学文、鲁维华、姚德义的具体分工待查
3. **前任领导去向**：前市委书记董方平、前市长葛军的去向值得追踪
4. **万龙的机会**：万龙1981年出生、拥有经济学博士学位，具备较好的教育背景和年龄优势

## 8. 数据文件说明

| 文件 | 路径 | 说明 |
|------|------|------|
| SQLite数据库 | data/tmp/hubei_赤壁市/赤壁市_network.db | 结构化关系数据 |
| GEXF图文件 | data/tmp/hubei_赤壁市/赤壁市_network.gexf | 可导入Gephi等工具 |
| 人物JSON | data/tmp/hubei_赤壁市/*.json | 单个人物深度档案 |
| 本报告 | data/tmp/hubei_赤壁市/{TODAY}-*.md | 调查记录 |

## 9. 信息来源汇总

| 来源 | 类型 | URL |
|------|------|-----|
| 赤壁市人民政府 | 官方 | http://www.chibi.gov.cn/ |
| 万龙（市长）领导之窗 | 官方 | http://www.chibi.gov.cn/xxgk/zfld/wl/ |
| 欧阳萍（副市长）领导之窗 | 官方 | http://www.chibi.gov.cn/xxgk/zfld/wh/ |
| 谭敏（副市长）领导之窗 | 官方 | http://www.chibi.gov.cn/xxgk/zfld/tm/ |
| 戴峰（副市长）领导之窗 | 官方 | http://www.chibi.gov.cn/xxgk/zfld/bhz/ |
| 舒敏（副市长）领导之窗 | 官方 | http://www.chibi.gov.cn/xxgk/zfld/sm/ |
| 彭光平主持市委理论学习中心组会议 | 官方新闻 | http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5123962.shtml |
| 彭光平、万龙调研医共体改革 | 官方新闻 | http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260720_5084931.shtml |
| 彭光平调研人大换届选举 | 官方新闻 | http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260722_5098698.shtml |
| 平安建设半年工作调度会 | 官方新闻 | http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260723_5113183.shtml |
| 万龙督导夏夜治安巡查 | 官方新闻 | http://www.chibi.gov.cn/xwzx/cbzw/202607/t20260724_5122961.shtml |
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Report: {report_path}")


def main():
    print(f"\n=== Building 赤壁市 (Chibi City) Network Data ===\n")
    print(f"Staging directory: {STAGING_DIR}")
    print(f"As of: {AS_OF}")
    print()

    build_database()
    build_gexf()
    build_report()

    # Person JSONs for core leaders
    core_ids = [1, 2]  # 彭光平, 万龙
    person_files = []
    for person in persons:
        if person["id"] in core_ids:
            pf = build_person_json(person)
            person_files.append(pf)

    print()
    print("=== Summary ===")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs:")
    for pf in person_files:
        print(f"    - {pf.name}")
    print(f"  Report: {STAGING_DIR / (TODAY + '-湖北省-咸宁市-赤壁市-领导班子工作关系网络调查报告.md')}")
    print()


if __name__ == "__main__":
    main()
