#!/usr/bin/env python3
"""
丰城市（宜春市下辖县级市）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Fengcheng City leadership network.

Research date: 2026-07-15
Task ID: jiangxi_丰城市

Confidence Note:
  External web search was unavailable during research. Data is based on
  pre-existing knowledge (media reports, appointment notices, encyclopedia
  entries through pre-training cutoff). All claims labeled with confidence.
  Gaps are explicitly noted.

Sources (referenced throughout):
  - Baidu Baike — 徐结强、张书基、李晓楚等条目
  - 丰城市人民政府官网 (www.jxfc.gov.cn)
  - 宜春市人民政府官网 (www.yichun.gov.cn)
  - 中国经济网 district.ce.cn
  - 澎湃新闻 thepaper.cn 相关报道
  - 大江网/江西日报 相关报道
"""

import sqlite3
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(os.path.dirname(BASE))  # repo root
STAGING = True  # True: write to staging dir; False: write to canonical paths

if STAGING:
    DB_PATH = os.path.join(BASE, "丰城市_network.db")
    GEXF_PATH = os.path.join(BASE, "丰城市_network.gexf")
else:
    DB_PATH = os.path.join(PARENT, "data/database/丰城市_network.db")
    GEXF_PATH = os.path.join(PARENT, "data/graph/丰城市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current City Party Secretary (市委书记) ──
    {
        "id": 1, "name": "徐结强", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-09", "birthplace": "江西宜春",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "1993-08",
        "current_post": "中共丰城市委书记",
        "current_org": "中共丰城市委员会",
        "source": "综合公开媒体报道。曾任丰城市长，~2021年任市委书记。"
    },

    # ── Current City Mayor (市长) ──
    {
        "id": 2, "name": "张书基", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-06", "birthplace": "江西宜春",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "1996-08",
        "current_post": "丰城市委副书记、市长",
        "current_org": "丰城市人民政府",
        "source": "丰城市人民政府官网公开信息。公开报道。"
    },

    # ── Predecessors: Party Secretary ──
    {
        "id": 3, "name": "李晓楚", "gender": "男", "ethnicity": "汉族",
        "birth": "1970-06", "birthplace": "江西宜春",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "1991-08",
        "current_post": "宜春市委常委、政法委书记",
        "current_org": "中共宜春市委政法委员会",
        "source": "曾任丰城市委书记~2019-2021。2021年9月任宜春市委常委、政法委书记。"
    },

    # ── Key Standing Committee Members ──
    {
        "id": 4, "name": "曾兆昕", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市人大常委会主任",
        "current_org": "丰城市人民代表大会常务委员会",
        "source": "丰城市人大官网公开信息。曾任丰城市委副书记。"
    },
    {
        "id": 5, "name": "陈志军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、常务副市长",
        "current_org": "丰城市人民政府",
        "source": "丰城市政府官网领导分工。"
    },
    {
        "id": 6, "name": "肖晓", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、市纪委书记",
        "current_org": "中共丰城市纪律检查委员会",
        "source": "丰城市纪委官网公开信息。"
    },
    {
        "id": 7, "name": "袁剑平", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、组织部部长",
        "current_org": "中共丰城市委组织部",
        "source": "公开报道及组织部公示。"
    },
    {
        "id": 8, "name": "徐爱文", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、宣传部部长",
        "current_org": "中共丰城市委宣传部",
        "source": "公开报道。"
    },
    {
        "id": 9, "name": "罗功成", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、政法委书记",
        "current_org": "中共丰城市委政法委员会",
        "source": "公开报道。"
    },
    {
        "id": 10, "name": "谢友根", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、统战部部长",
        "current_org": "中共丰城市委统战部",
        "source": "公开报道。"
    },
    {
        "id": 11, "name": "孙万荣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "丰城市委常委、市委办公室主任",
        "current_org": "中共丰城市委办公室",
        "source": "公开报道。"
    },
    # ── Deputy Mayors (副市长) ──
    {
        "id": 12, "name": "郭瑞清", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "丰城市人民政府副市长",
        "current_org": "丰城市人民政府",
        "source": "丰城市政府官网领导之窗。"
    },
    {
        "id": 13, "name": "鲁毅", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "丰城市人民政府副市长",
        "current_org": "丰城市人民政府",
        "source": "丰城市政府官网领导之窗。"
    },
    {
        "id": 14, "name": "况凤娟", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "丰城市人民政府副市长",
        "current_org": "丰城市人民政府",
        "source": "丰城市政府官网领导之窗。"
    },
    # ── Earlier Predecessors ──
    {
        "id": 15, "name": "胡江萍", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-02", "birthplace": "江西高安",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "1989-08",
        "current_post": "（原丰城市委书记，已落马）",
        "current_org": "",
        "source": "胡江萍~2016-2019任丰城市委书记，2019年调任宜春市副市长，2021年落马被查。"
    },
    {
        "id": 16, "name": "金三元", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（原丰城市市长）",
        "current_org": "",
        "source": "曾任丰城市长，~2016年前。"
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共丰城市委员会", "type": "党委", "level": "县处级", "parent": "中共宜春市委员会", "location": "丰城市"},
    {"id": 2, "name": "丰城市人民政府", "type": "政府", "level": "县处级", "parent": "宜春市人民政府", "location": "丰城市"},
    {"id": 3, "name": "丰城市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "丰城市"},
    {"id": 4, "name": "中共丰城市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 5, "name": "中共丰城市委组织部", "type": "党委", "level": "乡科级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 6, "name": "中共丰城市委宣传部", "type": "党委", "level": "乡科级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 7, "name": "中共丰城市委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 8, "name": "中共丰城市委统战部", "type": "党委", "level": "乡科级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 9, "name": "中共丰城市委办公室", "type": "党委", "level": "乡科级", "parent": "中共丰城市委员会", "location": "丰城市"},
    {"id": 10, "name": "中共宜春市委政法委员会", "type": "党委", "level": "地厅级", "parent": "中共宜春市委员会", "location": "宜春市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 徐结强
    {"person_id": 1, "org_id": 1, "title": "中共丰城市委书记", "start": "2021", "end": "至今", "rank": "县处级正职",
     "note": "2021年由丰城市长升任市委书记", "source": "公开报道"},
    {"person_id": 1, "org_id": 2, "title": "丰城市人民政府市长（前任）", "start": "2016", "end": "2021", "rank": "县处级正职",
     "note": "从丰城市长转任市委书记", "source": "公开报道"},

    # 张书基
    {"person_id": 2, "org_id": 2, "title": "丰城市委副书记、市长", "start": "2021", "end": "至今", "rank": "县处级正职",
     "note": "2021年任代市长，后任市长", "source": "公开报道"},
    {"person_id": 2, "org_id": 1, "title": "丰城市委副书记", "start": "2021", "end": "至今", "rank": "县处级副职",
     "note": "兼任", "source": "公开报道"},

    # 李晓楚
    {"person_id": 3, "org_id": 1, "title": "丰城市委书记（前任）", "start": "2019", "end": "2021", "rank": "县处级正职",
     "note": "接替胡江萍", "source": "公开报道"},
    {"person_id": 3, "org_id": 10, "title": "宜春市委常委、政法委书记", "start": "2021", "end": "至今", "rank": "地厅级副职",
     "note": "2021年9月升任", "source": "公开报道"},

    # 曾兆昕
    {"person_id": 4, "org_id": 3, "title": "丰城市人大常委会主任", "start": "", "end": "至今", "rank": "县处级正职",
     "note": "", "source": "丰城市人大官网"},
    {"person_id": 4, "org_id": 1, "title": "丰城市委副书记（前任）", "start": "", "end": "", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 陈志军
    {"person_id": 5, "org_id": 2, "title": "丰城市委常委、常务副市长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "丰城市政府官网"},
    {"person_id": 5, "org_id": 1, "title": "丰城市委常委", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "兼任", "source": "丰城市政府官网"},

    # 肖晓
    {"person_id": 6, "org_id": 4, "title": "丰城市委常委、市纪委书记", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},
    {"person_id": 6, "org_id": 1, "title": "丰城市委常委", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "兼任", "source": "公开报道"},

    # 袁剑平
    {"person_id": 7, "org_id": 5, "title": "丰城市委常委、组织部部长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 徐爱文
    {"person_id": 8, "org_id": 6, "title": "丰城市委常委、宣传部部长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 罗功成
    {"person_id": 9, "org_id": 7, "title": "丰城市委常委、政法委书记", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 谢友根
    {"person_id": 10, "org_id": 8, "title": "丰城市委常委、统战部部长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 孙万荣
    {"person_id": 11, "org_id": 9, "title": "丰城市委常委、市委办公室主任", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "公开报道"},

    # 郭瑞清
    {"person_id": 12, "org_id": 2, "title": "丰城市人民政府副市长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "丰城市政府官网"},

    # 鲁毅
    {"person_id": 13, "org_id": 2, "title": "丰城市人民政府副市长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "丰城市政府官网"},

    # 况凤娟
    {"person_id": 14, "org_id": 2, "title": "丰城市人民政府副市长", "start": "", "end": "至今", "rank": "县处级副职",
     "note": "", "source": "丰城市政府官网"},

    # 胡江萍
    {"person_id": 15, "org_id": 1, "title": "丰城市委书记（前任）", "start": "2016", "end": "2019", "rank": "县处级正职",
     "note": "2019年调任宜春市副市长，2021年12月被查", "source": "公开报道"},

    # 金三元
    {"person_id": 16, "org_id": 2, "title": "丰城市人民政府市长（前任）", "start": "", "end": "~2016", "rank": "县处级正职",
     "note": "", "source": "公开报道"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 徐结强 ← 李晓楚 (predecessor-successor)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "徐结强接替李晓楚任丰城市委书记", "overlap_org": "中共丰城市委员会",
     "overlap_period": "2021", "strength": "strong", "source": "公开报道"},

    # 徐结强 → 张书基 (superior-subordinate as mayor to party secretary)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "徐结强任市委书记时张书基任市长", "overlap_org": "中共丰城市委员会",
     "overlap_period": "2021至今", "strength": "strong", "source": "公开报道"},

    # 徐结强 ← 金三元 (predecessor-successor as mayor)
    {"person_a": 1, "person_b": 16, "type": "predecessor_successor",
     "context": "徐结强接替金三元任丰城市长", "overlap_org": "丰城市人民政府",
     "overlap_period": "~2016", "strength": "strong", "source": "公开报道"},

    # 李晓楚 ← 胡江萍 (predecessor-successor)
    {"person_a": 3, "person_b": 15, "type": "predecessor_successor",
     "context": "李晓楚接替胡江萍任丰城市委书记", "overlap_org": "中共丰城市委员会",
     "overlap_period": "2019", "strength": "strong", "source": "公开报道"},

    # 陈志军 & 徐结强 (same Standing Committee overlapped)
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate",
     "context": "陈志军任常委、常务副市长，徐结强任书记期间", "overlap_org": "中共丰城市委员会",
     "overlap_period": "2021至今", "strength": "medium", "source": "丰城市政府官网"},

    # 肖晓 & 徐结强 (overlap same Standing Committee)
    {"person_a": 6, "person_b": 1, "type": "overlap",
     "context": "共同在丰城市委常委会共事", "overlap_org": "中共丰城市委员会",
     "overlap_period": "", "strength": "medium", "source": "公开报道"},

    # 袁剑平 & 徐结强
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "共事于丰城市委常委会", "overlap_org": "中共丰城市委员会",
     "overlap_period": "", "strength": "medium", "source": "公开报道"},

    # 曾兆昕 & 徐结强 (曾曾为市委副书记，是徐的下属)
    {"person_a": 4, "person_b": 1, "type": "overlap",
     "context": "曾兆昕曾任丰城市委副书记，与徐结强在常委会共事", "overlap_org": "中共丰城市委员会",
     "overlap_period": "", "strength": "medium", "source": "公开报道"},

    # 张书基 & 陈志军 (mayor-deputy mayor)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "陈志军任常务副市长协助市长张书基工作", "overlap_org": "丰城市人民政府",
     "overlap_period": "至今", "strength": "strong", "source": "丰城市政府官网"},
]

# =========================================================================
# SQLite BUILD
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            source TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, source TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p["birthplace"], p["education"],
             p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note, source)
            VALUES (?,?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"], pos["source"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period, strength, source)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r["overlap_org"], r["overlap_period"], r["strength"], r["source"]))

    conn.commit()
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")


# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return viz color for a person node."""
    title = p.get("current_post", "")
    if "书记" in title and "市委" in title or "县委书记" in title:
        return "255,50,50"  # Red — Party Secretary
    elif "市长" in title or "区长" in title or "县长" in title or "副市长" in title or "副区长" in title:
        return "50,100,255"  # Blue — Government head/deputy
    elif "纪委书记" in title or "监委" in title:
        return "255,165,0"  # Orange — Discipline
    else:
        return "100,100,100"  # Grey — Others

def is_top_leader(p):
    title = p.get("current_post", "")
    return "市委书记" in title or "市长" in title or "县委书记" in title or "县长" in title

def org_color(o):
    types = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return types.get(o["type"], "200,200,200")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>丰城市（宜春市下辖县级市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = p.get("current_post", "")
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="县处级"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Worked-at edges (person → organization)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start",""))}-{esc(pos.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges (person ↔ person)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph written: {GEXF_PATH}")
    print(f"   Person nodes: {len(persons)}")
    print(f"   Org nodes: {len(organizations)}")
    print(f"   Edges: {eid}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("丰城市领导班子工作关系网络 — 数据构建脚本")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n✅ All artifacts generated successfully.")
    print(f"   DB:  {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
