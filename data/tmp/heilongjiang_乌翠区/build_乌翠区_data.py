#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乌翠区 (Wucui District), 伊春市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_乌翠区
Research sources:
  - 乌翠区人民政府网站 (www.ycwc.gov.cn)
  - 领导之窗 pages (区政府领导分工)
  - 乌翠新闻 articles
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "乌翠区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = os.path.join(BASE, "..", "..", "database", f"{SLUG}_network.db")
CANONICAL_GEXF = os.path.join(BASE, "..", "..", "graph", f"{SLUG}_network.gexf")
CANONICAL_BUILD = os.path.join(BASE, "..", "..", "..", f"build_{SLUG}_data.py")
CANONICAL_PERSONS = Path(BASE) / ".." / ".." / "persons"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 刘志浩 — 区委书记 (as of July 2026)
    {"id": 1, "name": "刘志浩", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml; http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # 梁倬 — 区委副书记、区长
    {"id": 2, "name": "梁倬", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202311/332576.shtml; http://www.ycwc.gov.cn/wcqrmzf/c100351/202606/428920.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # Government Leadership Team (区政府领导班子)
    # ══════════════════════════════════════════════════════════════════════════

    # 王延佳 — 区委常委、副区长 (常务副区长)
    {"id": 3, "name": "王延佳", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-08", "birthplace": "", "education": "哈尔滨工业大学华德应用技术学院，理学学士",
     "party_join": "2005-05", "work_start": "2007-09",
     "current_post": "区委常委、副区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202204/1292.shtml"},

    # 胡起华 — 区委常委、副区长
    {"id": 4, "name": "胡起华", "gender": "男", "ethnicity": "汉族",
     "birth": "1990-04", "birthplace": "", "education": "哈尔滨工业大学高级管理人员工商管理专业研究生",
     "party_join": "2021-12", "work_start": "2012-07",
     "current_post": "区委常委、副区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202504/398921.shtml"},

    # 王海涛 — 区政府党组成员、副区长
    {"id": 5, "name": "王海涛", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "", "education": "黑龙江大学行政管理专业",
     "party_join": "2000-12", "work_start": "1986-12",
     "current_post": "区政府党组成员、副区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202401/338859.shtml"},

    # 张爽 — 区政府党组成员、副区长
    {"id": 6, "name": "张爽", "gender": "女", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "", "education": "哈尔滨师范大学汉语言文学专业在职大学",
     "party_join": "2001-08", "work_start": "1997-10",
     "current_post": "区政府党组成员、副区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202307/319794.shtml"},

    # 王亮 — 区政府副区长
    {"id": 7, "name": "王亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-10", "birthplace": "", "education": "东北林业大学法学专业",
     "party_join": "2010-11", "work_start": "2007-07",
     "current_post": "区政府副区长", "current_org": "乌翠区人民政府",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100361/202101/1262.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # Other Party Committee members (identified from news reports)
    # ══════════════════════════════════════════════════════════════════════════

    # 潘丹 — 区委领导 (from 警示教育会 article)
    {"id": 8, "name": "潘丹", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml"},

    # 唐艳秋 — 区委领导
    {"id": 9, "name": "唐艳秋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml"},

    # 黄绍峰 — 区委领导
    {"id": 10, "name": "黄绍峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml; http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # 苏传波 — 区委领导
    {"id": 11, "name": "苏传波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml; http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # 鞠长城 — 区委领导 (also 纪委书记 from the article context - 通报典型案例)
    {"id": 12, "name": "鞠长城", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导、区纪委书记（推测）", "current_org": "中共乌翠区纪律检查委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202607/430137.shtml; http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # 宫勋 — 区委领导 (from 2025新年徒步活动)
    {"id": 13, "name": "宫勋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导", "current_org": "中共乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # ══════════════════════════════════════════════════════════════════════════
    # Former/Other Leaders
    # ══════════════════════════════════════════════════════════════════════════

    # 周晓宏 — 区领导 (from 2025新年徒步活动，推测为区人大主任)
    {"id": 14, "name": "周晓宏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区人大领导（推测）", "current_org": "乌翠区人大常委会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},

    # 张斐 — 区领导 (from 2025新年徒步活动，推测为区政协主席)
    {"id": 15, "name": "张斐", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区政协领导（推测）", "current_org": "政协乌翠区委员会",
     "source": "http://www.ycwc.gov.cn/wcqrmzf/c100304/202501/385685.shtml"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    # District-level
    {"id": 1, "name": "中共乌翠区委员会", "type": "党委", "level": "县处级",
     "parent": "中共伊春市委员会", "location": "黑龙江省伊春市乌翠区"},
    {"id": 2, "name": "乌翠区人民政府", "type": "政府", "level": "县处级",
     "parent": "伊春市人民政府", "location": "黑龙江省伊春市乌翠区"},
    {"id": 3, "name": "中共乌翠区纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市乌翠区"},
    {"id": 4, "name": "乌翠区人大常委会", "type": "人大", "level": "县处级",
     "parent": "伊春市人大常委会", "location": "黑龙江省伊春市乌翠区"},
    {"id": 5, "name": "政协乌翠区委员会", "type": "政协", "level": "县处级",
     "parent": "政协伊春市委员会", "location": "黑龙江省伊春市乌翠区"},

    # Parent city-level
    {"id": 6, "name": "中共伊春市委员会", "type": "党委", "level": "地市级",
     "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市"},
    {"id": 7, "name": "伊春市人民政府", "type": "政府", "level": "地市级",
     "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市"},
    {"id": 8, "name": "中共伊春市纪律检查委员会", "type": "党委", "level": "地市级",
     "parent": "中共黑龙江省纪律检查委员会", "location": "黑龙江省伊春市"},
    {"id": 9, "name": "伊春市人大常委会", "type": "人大", "level": "地市级",
     "parent": "黑龙江省人大常委会", "location": "黑龙江省伊春市"},
    {"id": 10, "name": "政协伊春市委员会", "type": "政协", "level": "地市级",
     "parent": "政协黑龙江省委员会", "location": "黑龙江省伊春市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘志浩 — Party Secretary
    {"id": 1, "person_id": 1, "org_id": 1, "title": "区委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "当前任职，至少从2025年1月起任区委书记"},
    # Also likely other earlier positions — unknown

    # 梁倬 — District Mayor
    {"id": 2, "person_id": 2, "org_id": 2, "title": "区委副书记、区长",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "当前任职，主持区政府全面工作"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "区委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "兼任区委副书记"},

    # 王延佳 — Executive Deputy Mayor
    {"id": 4, "person_id": 3, "org_id": 2, "title": "区委常委、副区长（常务）",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "负责区政府常务工作"},
    {"id": 5, "person_id": 3, "org_id": 1, "title": "区委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 胡起华 — Deputy Mayor
    {"id": 6, "person_id": 4, "org_id": 2, "title": "区委常委、副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "负责文化体育旅游、园林绿化等工作"},
    {"id": 7, "person_id": 4, "org_id": 1, "title": "区委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 王海涛 — Deputy Mayor (Public Security)
    {"id": 8, "person_id": 5, "org_id": 2, "title": "区政府党组成员、副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "负责公共安全等方面工作"},

    # 张爽 — Deputy Mayor
    {"id": 9, "person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "负责人力资源、教育、医疗保障等工作"},

    # 王亮 — Deputy Mayor
    {"id": 10, "person_id": 7, "org_id": 2, "title": "区政府副区长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "负责工业经济、招商引资、民政等工作"},

    # Party Committee Members
    {"id": 11, "person_id": 8, "org_id": 1, "title": "区委领导",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 12, "person_id": 9, "org_id": 1, "title": "区委领导",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 13, "person_id": 10, "org_id": 1, "title": "区委领导",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 14, "person_id": 11, "org_id": 1, "title": "区委领导",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 15, "person_id": 12, "org_id": 3, "title": "区委领导、区纪委书记（推测）",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "在警示教育会上通报典型案例"},
    {"id": 16, "person_id": 13, "org_id": 1, "title": "区委领导",
     "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # NPC / CPPCC
    {"id": 17, "person_id": 14, "org_id": 4, "title": "区人大领导（推测）",
     "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 18, "person_id": 15, "org_id": 5, "title": "区政协领导（推测）",
     "start": "", "end": "", "rank": "县处级正职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 刘志浩 ↔ 梁倬 — 党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "刘志浩（区委书记）与梁倬（区委副书记、区长）为乌翠区党政一把手搭档",
     "overlap_org": "乌翠区", "overlap_period": "当前"},

    # 刘志浩 — party leadership team
    {"id": 2, "person_a": 1, "person_b": 8, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员潘丹",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 3, "person_a": 1, "person_b": 9, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员唐艳秋",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 4, "person_a": 1, "person_b": 10, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员黄绍峰",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 5, "person_a": 1, "person_b": 11, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员苏传波",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 6, "person_a": 1, "person_b": 12, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员、纪委书记鞠长城",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 7, "person_a": 1, "person_b": 13, "type": "上下级",
     "context": "刘志浩作为区委书记领导区委班子成员宫勋",
     "overlap_org": "中共乌翠区委员会", "overlap_period": "当前"},

    # 梁倬 — government team
    {"id": 8, "person_a": 2, "person_b": 3, "type": "上下级",
     "context": "梁倬作为区长领导副区长王延佳（常务副区长）",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},
    {"id": 9, "person_a": 2, "person_b": 4, "type": "上下级",
     "context": "梁倬作为区长领导副区长胡起华",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},
    {"id": 10, "person_a": 2, "person_b": 5, "type": "上下级",
     "context": "梁倬作为区长领导副区长王海涛",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},
    {"id": 11, "person_a": 2, "person_b": 6, "type": "上下级",
     "context": "梁倬作为区长领导副区长张爽",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},
    {"id": 12, "person_a": 2, "person_b": 7, "type": "上下级",
     "context": "梁倬作为区长领导副区长王亮",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},

    # Same organization overlaps
    {"id": 13, "person_a": 3, "person_b": 4, "type": "同级",
     "context": "王延佳与胡起华同为区委常委、副区长",
     "overlap_org": "乌翠区人民政府/中共乌翠区委员会", "overlap_period": "当前"},
    {"id": 14, "person_a": 5, "person_b": 6, "type": "同级",
     "context": "王海涛与张爽同为区政府党组成员、副区长",
     "overlap_org": "乌翠区人民政府", "overlap_period": "当前"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "区委书记" in post:
        return "255,50,50"  # red for party secretary
    if "区长" in post:
        return "50,100,255"  # blue for gov leader
    if "副区长" in post:
        return "80,140,230"
    if "纪委书记" in post:
        return "255,165,0"  # orange for discipline
    if "人大" in post:
        return "180,200,255"
    if "政协" in post:
        return "200,180,255"
    if "区委" in post:
        return "200,150,150"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,230,255",
            "政协":"230,200,255"}.get(otype,"200,200,200")

def get_size_for_person(p):
    post = p.get("current_post","")
    if "区委书记" in post or "区长" in post:
        return "20.0"
    if "区委" in post:
        return "12.0"
    if "副区长" in post:
        return "12.0"
    return "10.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>乌翠区领导班子工作关系网络 — 2026年7月24日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = get_size_for_person(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
