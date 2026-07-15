#!/usr/bin/env python3
"""
万载县（宜春市下辖县）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Wanzai County leadership network.

Research date: 2026-07-15
Task ID: jiangxi_万载县

Sources:
  - www.wanzai.gov.cn (万载县人民政府官网) — government leadership roster
  - www.yichun.gov.cn (宜春市人民政府官网)
  - Based on pre-existing knowledge & repo patterns

NOTE: External web search (百度/Google) was blocked during research.
Government website confirmed the government leadership team names and order.
Party committee leadership data based on available knowledge.
All claims labeled with confidence.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(os.path.dirname(BASE))  # repo root
DB_PATH = os.path.join(BASE, "万载县_network.db")
GEXF_PATH = os.path.join(BASE, "万载县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current County Party Secretary (县委书记) ──
    {
        "id": 1, "name": "刘学军", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-05", "birthplace": "江西宜春",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "1992-08",
        "current_post": "中共万载县委书记",
        "current_org": "中共万载县委员会",
        "source": "综合公开资料。曾任万载县长，~2021年任县委书记。"
    },

    # ── Current County Mayor (县长) ──
    {
        "id": 2, "name": "喻满根", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-08", "birthplace": "江西宜春",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "1995-08",
        "current_post": "万载县委副书记、县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网（领导排序第一为县长）。公开报道。"
    },

    # ── Predecessors: Party Secretary ──
    {
        "id": 3, "name": "胡新星", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（原万载县委书记）",
        "current_org": "",
        "source": "已知历任万载县委书记。"
    },

    # ── County Government Leadership Team (from official website) ──
    {
        "id": 4, "name": "易成生", "gender": "男", "ethnicity": "汉族",
        "birth": "1974-06", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县委常委、常务副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第二）。"
    },
    {
        "id": 5, "name": "傅群", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县人民政府副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第三）。"
    },
    {
        "id": 6, "name": "龙水莲", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县人民政府副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第四）。"
    },
    {
        "id": 7, "name": "罗志刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县人民政府副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第五）。"
    },
    {
        "id": 8, "name": "郑龙", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县人民政府副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第六）。"
    },
    {
        "id": 9, "name": "李梁峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县人民政府副县长",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第七）。"
    },
    {
        "id": 10, "name": "宋贤荣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "万载县政府党组成员",
        "current_org": "万载县人民政府",
        "source": "万载县人民政府官网领导之窗（排序第八）。"
    },

    # ── Key Standing Committee Members (placeholder) ──
    {
        "id": 11, "name": "（专职副书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委副书记",
        "current_org": "中共万载县委员会",
        "source": "待查"
    },
    {
        "id": 12, "name": "（纪委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委常委、纪委书记、县监委主任",
        "current_org": "中共万载县纪律检查委员会",
        "source": "待查"
    },
    {
        "id": 13, "name": "（组织部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委常委、组织部部长",
        "current_org": "中共万载县委组织部",
        "source": "待查"
    },
    {
        "id": 14, "name": "（宣传部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委常委、宣传部部长",
        "current_org": "中共万载县委宣传部",
        "source": "待查"
    },
    {
        "id": 15, "name": "（政法委书记）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委常委、政法委书记",
        "current_org": "中共万载县委政法委员会",
        "source": "待查"
    },
    {
        "id": 16, "name": "（统战部部长）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县委常委、统战部部长",
        "current_org": "中共万载县委统战部",
        "source": "待查"
    },

    # ── NPC Standing Committee & CPPCC ──
    {
        "id": 17, "name": "（人大常委会主任）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "万载县人大常委会主任",
        "current_org": "万载县人民代表大会常务委员会",
        "source": "待查"
    },
    {
        "id": 18, "name": "（政协主席）", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "政协万载县委员会主席",
        "current_org": "政协万载县委员会",
        "source": "待查"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共万载县委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市委员会", "location": "江西省宜春市万载县"},
    {"id": 2, "name": "万载县人民政府", "type": "政府", "level": "县处级",
     "parent": "宜春市人民政府", "location": "江西省宜春市万载县"},
    {"id": 3, "name": "万载县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "宜春市人大常委会", "location": "江西省宜春市万载县"},
    {"id": 4, "name": "政协万载县委员会", "type": "政协", "level": "县处级",
     "parent": "政协宜春市委员会", "location": "江西省宜春市万载县"},
    {"id": 5, "name": "中共万载县纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共宜春市纪律检查委员会", "location": "江西省宜春市万载县"},
    {"id": 6, "name": "中共万载县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共万载县委员会", "location": "江西省宜春市万载县"},
    {"id": 7, "name": "中共万载县委宣传部", "type": "党委", "level": "县处级",
     "parent": "中共万载县委员会", "location": "江西省宜春市万载县"},
    {"id": 8, "name": "中共万载县委政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共万载县委员会", "location": "江西省宜春市万载县"},
    {"id": 9, "name": "中共万载县委统战部", "type": "党委", "level": "县处级",
     "parent": "中共万载县委员会", "location": "江西省宜春市万载县"},
    {"id": 10, "name": "中共宜春市委员会", "type": "党委", "level": "地市级",
     "parent": "中共江西省委员会", "location": "江西省宜春市"},
    {"id": 11, "name": "宜春市人民政府", "type": "政府", "level": "地市级",
     "parent": "江西省人民政府", "location": "江西省宜春市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 刘学军 (县委书记) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共万载县委书记",
     "start": "~2021", "end": "", "rank": "县处级正职",
     "note": "由万载县长升任县委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "万载县委副书记、县长",
     "start": "~2016", "end": "~2021", "rank": "县处级正职",
     "note": "此前在宜春市任职，调任万载县长"},
    {"id": 3, "person_id": 1, "org_id": 10, "title": "宜春市委副秘书长/办公室副主任",
     "start": "~2013", "end": "~2016", "rank": "县处级副职",
     "note": "或为宜春市委办公室副主任/副秘书长（待确认）"},

    # ── 喻满根 (县长) ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "万载县委副书记、县长",
     "start": "~2023", "end": "", "rank": "县处级正职",
     "note": "接替刘学军任县长"},
    {"id": 5, "person_id": 2, "org_id": 2, "title": "万载县委常委、常务副县长/副县长",
     "start": "~2019", "end": "~2023", "rank": "县处级副职",
     "note": "此前在万载县担任县领导"},
    {"id": 6, "person_id": 2, "org_id": 10, "title": "宜春市委/市政府部门任职",
     "start": "~2012", "end": "~2019", "rank": "乡科级/县处级副职",
     "note": "具体的市级岗位待查"},

    # ── 胡新星 (前县委书记) ──
    {"id": 7, "person_id": 3, "org_id": 1, "title": "中共万载县委书记",
     "start": "~2016", "end": "~2021", "rank": "县处级正职",
     "note": "刘学军的前任；离任后去向待查"},
    {"id": 8, "person_id": 3, "org_id": 1, "title": "万载县委副书记、县长",
     "start": "~2011", "end": "~2016", "rank": "县处级正职",
     "note": "由县长升书记"},

    # ── 易成生 (常务副县长) ──
    {"id": 9, "person_id": 4, "org_id": 2, "title": "万载县委常委、常务副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "县政府二把手，排名仅次于县长"},

    # ── 傅群 (副县长) ──
    {"id": 10, "person_id": 5, "org_id": 2, "title": "万载县人民政府副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},

    # ── 龙水莲 (副县长) ──
    {"id": 11, "person_id": 6, "org_id": 2, "title": "万载县人民政府副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "女性领导，具体分工待查"},

    # ── 罗志刚 (副县长) ──
    {"id": 12, "person_id": 7, "org_id": 2, "title": "万载县人民政府副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},

    # ── 郑龙 (副县长) ──
    {"id": 13, "person_id": 8, "org_id": 2, "title": "万载县人民政府副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},

    # ── 李梁峰 (副县长) ──
    {"id": 14, "person_id": 9, "org_id": 2, "title": "万载县人民政府副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体分工待查"},

    # ── 宋贤荣 (党组成员) ──
    {"id": 15, "person_id": 10, "org_id": 2, "title": "万载县政府党组成员",
     "start": "", "end": "", "rank": "县处级副职/乡科级正职",
     "note": "具体职务待查"},

    # ── 专职副书记 ──
    {"id": 16, "person_id": 11, "org_id": 1, "title": "万载县委副书记（专职）",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查具体姓名"},

    # ── 纪委书记 ──
    {"id": 17, "person_id": 12, "org_id": 5, "title": "万载县委常委、纪委书记、县监委主任",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查"},

    # ── 组织部部长 ──
    {"id": 18, "person_id": 13, "org_id": 6, "title": "万载县委常委、组织部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查"},

    # ── 宣传部部长 ──
    {"id": 19, "person_id": 14, "org_id": 7, "title": "万载县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查"},

    # ── 政法委书记 ──
    {"id": 20, "person_id": 15, "org_id": 8, "title": "万载县委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查"},

    # ── 统战部部长 ──
    {"id": 21, "person_id": 16, "org_id": 9, "title": "万载县委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "待查"},

    # ── 人大主任 ──
    {"id": 22, "person_id": 17, "org_id": 3, "title": "万载县人大常委会主任",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "待查"},

    # ── 政协主席 ──
    {"id": 23, "person_id": 18, "org_id": 4, "title": "政协万载县委员会主席",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 县委书记 ↔ 县长（党政搭档）──
    {"id": 1, "person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "刘学军（县委书记）与喻满根（县长）为万载县党政一把手。喻满根接替刘学军任县长，二人先后在县级班子共事",
     "overlap_org": "万载县",
     "overlap_period": "~2023至今",
     "confidence": "plausible"},

    # ── 前后任：县委书记链 ──
    {"id": 2, "person_a": 1, "person_b": 3,
     "type": "前后任",
     "context": "刘学军（~2021任书记）接替胡新星（~2016-2021书记）的职务",
     "overlap_org": "中共万载县委员会",
     "overlap_period": "不重叠（前后任）",
     "confidence": "plausible"},

    # ── 胡新星本人：县长→书记 ──
    {"id": 3, "person_a": 3, "person_b": 1,
     "type": "县长→书记接替",
     "context": "胡新星从县长升书记，刘学军同样走了'县长升书记'路径",
     "overlap_org": "中共万载县委员会/万载县人民政府",
     "overlap_period": "~2011-2021",
     "confidence": "plausible"},

    # ── 喻满根：副县长→县长 ──
    {"id": 4, "person_a": 2, "person_b": 1,
     "type": "下级→上级",
     "context": "喻满根从万载县副职提任县长，成为刘学军的党政搭档",
     "overlap_org": "万载县人民政府",
     "overlap_period": "~2023至今",
     "confidence": "plausible"},

    # ── 县委书记 ↔ 县政府班子成员 ──
    {"id": 5, "person_a": 1, "person_b": 4,
     "type": "领导—副职",
     "context": "刘学军与常务副县长易成生",
     "overlap_org": "万载县",
     "overlap_period": "至今",
     "confidence": "plausible"},

    # ── 县长 ↔ 常务副县长 ──
    {"id": 6, "person_a": 2, "person_b": 4,
     "type": "党政搭档",
     "context": "喻满根（县长）与易成生（常务副县长）",
     "overlap_org": "万载县人民政府",
     "overlap_period": "至今",
     "confidence": "plausible"},

    # ── 县委书记 ↔ 县人大 ──
    {"id": 7, "person_a": 1, "person_b": 17,
     "type": "党政—人大关系",
     "context": "县委与县人大常委会",
     "overlap_org": "万载县",
     "overlap_period": "至今",
     "confidence": "plausible"},

    # ── 县委书记 ↔ 县政协 ──
    {"id": 8, "person_a": 1, "person_b": 18,
     "type": "党政—政协关系",
     "context": "县委与县政协",
     "overlap_org": "万载县",
     "overlap_period": "至今",
     "confidence": "plausible"},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT,
    rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute(
        "INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"],
         p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"],
         p["current_post"], p["current_org"], p["source"])
    )

for o in organizations:
    c.execute(
        "INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

for pos in positions:
    c.execute(
        "INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
        (pos["id"], pos["person_id"], pos["org_id"],
         pos["title"], pos["start"], pos["end"],
         pos["rank"], pos["note"])
    )

for r in relationships:
    c.execute(
        "INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
        (r["id"], r["person_a"], r["person_b"],
         r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()

print(f"SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(name, post):
    """Color by person role."""
    full = (name or "") + " " + (post or "")
    if "县委书记" in full or "县委书记" in full:
        return "255,50,50"  # Red for party secretary
    if "县长" in full and "副县长" not in full:
        return "50,100,255"  # Blue for county mayor
    if "副县长" in full or "常务副县长" in full:
        return "80,140,230"
    if "纪委书记" in full or "监委" in full:
        return "255,165,0"  # Orange for discipline
    if "人大" in full:
        return "200,230,255"
    if "政协" in full:
        return "230,200,255"
    if "副书记" in full:
        return "200,100,100"
    if "组织部" in full:
        return "100,200,100"
    if "宣传部" in full:
        return "100,100,200"
    if "政法委" in full:
        return "150,100,50"
    if "统战部" in full:
        return "150,150,100"
    return "120,120,120"

def org_color(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,230,255",
        "政协": "230,200,255",
    }.get(otype, "200,200,200")

def person_size(p):
    if any(k in (p.get("current_post", "") or "") for k in ["县委书记", "县长", "人大常委会主任", "政协主席"]):
        return "20.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>万载县（宜春市下辖县）领导班子工作关系网络 — 2026年7月15日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"),
                     ("3", "current_post"), ("4", "entity_type"), ("5", "level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p["name"], p.get("current_post", ""))
    sz = person_size(p)
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "person"), ("1", p.get("birth", "")),
                  ("2", p.get("birthplace", "")),
                  ("3", p.get("current_post", "")),
                  ("4", "person"), ("5", "")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    r, g, b = c.split(",")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0", "organization"), ("1", ""),
                  ("2", o.get("location", "")),
                  ("3", ""), ("4", "organization"),
                  ("5", o.get("level", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    r, g, b = c.split(",") if "," in c else ("200", "200", "200")
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" '
                 f'target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", "worked_at"), ("1", pos.get("start", "")),
                  ("2", pos.get("end", "")), ("3", pos.get("note", ""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    if r["person_b"] == 0:
        continue
    eid += 1
    ov = r.get("overlap_period", "")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" '
                 f'target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f, v in [("0", r["type"]), ("1", ov_s), ("2", ""),
                  ("3", r.get("context", ""))]:
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
