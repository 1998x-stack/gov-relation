#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
罗甸县（黔南布依族苗族自治州）领导班子关系网络数据生成脚本。

Targets: 县委书记、县长
Data as of: 2026-07-23
Status: PARTIAL — Web access to Chinese government sites was blocked during research.
         All person fields (birth, education, full career timeline) marked as gaps.
         Current officeholders identified from available sources.

Sources:
- qiannan.gov.cn (黔南州人民政府门户网站, accessed 2026-07-23)
- 罗甸县人民政府 (luodian.gov.cn — unreachable during research)
- 黔南州委组织部 — 任前公示 (inaccessible during research)

Research limitations:
- Exa search API: rate-limited
- luodian.gov.cn: timeout
- Baidu Baike: blocked
- Google/Bing/DuckDuckGo: timeout or blocked
- Jina reader: timeout on Chinese sites
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_罗甸县"
SLUG = "罗甸县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "黔南布依族苗族自治州"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_罗甸县"
_BASE_OVERRIDE = os.environ.get("LUODIAN_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "罗甸县_network.db")
GEXF_PATH = os.path.join(BASE, "罗甸县_network.gexf")
PERSONS_DIR = os.path.join(BASE, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  DATA                                                                   ║
# ║  NOTE: All fields below are PLACEHOLDERS pending successful web access.  ║
# ║  The current officeholders of 罗甸县 were not determinable from         ║
# ║  available channels during this research session.                       ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

persons = [
    # 1 - 县委书记 (Party Secretary)
    {
        "id": 1,
        "name": "【待查】罗甸县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委书记",
        "current_org": "中共罗甸县委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 2 - 县长 (County Mayor)
    {
        "id": 2,
        "name": "【待查】罗甸县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委副书记、县人民政府县长",
        "current_org": "罗甸县人民政府",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 3 - 县委副书记 (Deputy Party Secretary)
    {
        "id": 3,
        "name": "【待查】罗甸县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委副书记",
        "current_org": "中共罗甸县委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 4 - 常务副县长 (Executive Deputy County Mayor)
    {
        "id": 4,
        "name": "【待查】罗甸常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、常务副县长",
        "current_org": "罗甸县人民政府",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 5 - 纪委书记 (Discipline Inspection Secretary)
    {
        "id": 5,
        "name": "【待查】罗甸纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、县纪委书记、县监委主任",
        "current_org": "中共罗甸县纪律检查委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 6 - 组织部长 (Organization Department Head)
    {
        "id": 6,
        "name": "【待查】罗甸组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、县委组织部部长",
        "current_org": "中共罗甸县委组织部",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 7 - 宣传部长 (Propaganda Department Head)
    {
        "id": 7,
        "name": "【待查】罗甸宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、县委宣传部部长",
        "current_org": "中共罗甸县委宣传部",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 8 - 政法委书记 (Political and Legal Affairs Secretary)
    {
        "id": 8,
        "name": "【待查】罗甸政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、县委政法委书记",
        "current_org": "中共罗甸县委政法委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 9 - 统战部长 (United Front Work Department Head)
    {
        "id": 9,
        "name": "【待查】罗甸统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县委常委、县委统战部部长",
        "current_org": "中共罗甸县委统战部",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 10 - 人大常委会主任 (People's Congress Chair)
    {
        "id": 10,
        "name": "【待查】罗甸人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县人大常委会主任",
        "current_org": "罗甸县人民代表大会常务委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
    # 11 - 政协主席 (CPPCC Chair)
    {
        "id": 11,
        "name": "【待查】罗甸政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "罗甸县政协主席",
        "current_org": "中国人民政治协商会议罗甸县委员会",
        "source": "待查 — 罗甸县人民政府官网无法访问 (luodian.gov.cn timeout)",
    },
]

organizations = [
    {"id": 1, "name": "中共罗甸县委员会", "type": "党委", "level": "县处级", "parent": "中共黔南州委", "location": "罗甸县"},
    {"id": 2, "name": "罗甸县人民政府", "type": "政府", "level": "县处级", "parent": "黔南州人民政府", "location": "罗甸县"},
    {"id": 3, "name": "中共罗甸县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 4, "name": "中共罗甸县委组织部", "type": "党委", "level": "乡科级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 5, "name": "中共罗甸县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 6, "name": "中共罗甸县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 7, "name": "中共罗甸县委统战部", "type": "党委", "level": "乡科级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 8, "name": "罗甸县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "黔南州人大常委会", "location": "罗甸县"},
    {"id": 9, "name": "中国人民政治协商会议罗甸县委员会", "type": "政协", "level": "县处级", "parent": "黔南州政协", "location": "罗甸县"},
    # Key township-level orgs
    {"id": 10, "name": "中共罗甸县委办公室", "type": "党委", "level": "乡科级", "parent": "中共罗甸县委员会", "location": "罗甸县"},
    {"id": 11, "name": "罗甸县人民政府办公室", "type": "政府", "level": "乡科级", "parent": "罗甸县人民政府", "location": "罗甸县"},
]

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "罗甸县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任—姓名待确认"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "罗甸县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任—姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "罗甸县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "罗甸县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "罗甸县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "罗甸县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 组织部长
    {"person_id": 6, "org_id": 4, "title": "罗甸县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 宣传部长
    {"person_id": 7, "org_id": 5, "title": "罗甸县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 政法委书记
    {"person_id": 8, "org_id": 6, "title": "罗甸县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 统战部长
    {"person_id": 9, "org_id": 7, "title": "罗甸县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任—姓名待确认"},
    # 人大主任
    {"person_id": 10, "org_id": 8, "title": "罗甸县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任—姓名待确认"},
    # 政协主席
    {"person_id": 11, "org_id": 9, "title": "罗甸县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任—姓名待确认"},
]

relationships = [
    # 书记 ↔ 县长 (Party Secretary ↔ County Mayor — core duo)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长为县委常委会和政府班子核心搭档",
     "overlap_org": "中共罗甸县委员会/罗甸县人民政府",
     "overlap_period": "待查"},
    # 书记 ↔ 副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与专职副书记在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 县长 ↔ 常务副县长
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与常务副县长在县政府班子共事",
     "overlap_org": "罗甸县人民政府",
     "overlap_period": "待查"},
    # 县长 ↔ 副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长（县委副书记）与专职副书记在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与纪委书记在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 书记 ↔ 组织部长
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "县委书记与组织部长在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 书记 ↔ 宣传部长
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与宣传部长在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 书记 ↔ 政法委书记
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委书记与政法委书记在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 书记 ↔ 统战部长
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与统战部长在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    # 常务副县长 ↔ 其他常委
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "常务副县长与纪委书记在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "常务副县长与组织部长在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
    {"person_a": 4, "person_b": 7, "type": "overlap",
     "context": "常务副县长与宣传部长在县委常委会共事",
     "overlap_org": "中共罗甸县委员会",
     "overlap_period": "待查"},
]

source_register = [
    {"id": "S001", "title": "黔南州人民政府门户网站",
     "url": "https://www.qiannan.gov.cn/",
     "publisher": "黔南州人民政府", "published_at": "",
     "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high",
     "notes": "确认罗甸县为黔南州下辖县。领导之窗页面无法直接访问。"},
    {"id": "S002", "title": "罗甸县人民政府门户网站",
     "url": "https://www.luodian.gov.cn/",
     "publisher": "罗甸县人民政府", "published_at": "",
     "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high",
     "notes": "无法访问（连接超时）。预计包含领导之窗、领导分工等关键信息。"},
    {"id": "S003", "title": "黔南州政府新闻 — 领导分工通知",
     "url": "https://www.qiannan.gov.cn/zwgk/zfxxgk/fdzdgknr/rsrm/",
     "publisher": "黔南州人民政府", "published_at": "",
     "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high",
     "notes": "人事任免板块——页面无法访问（404）。可能包含罗甸县领导任命通知。"},
    {"id": "S004", "title": "百度百科 — 罗甸县",
     "url": "https://baike.baidu.com/item/罗甸县",
     "publisher": "百度百科", "published_at": "",
     "accessed_at": "2026-07-23",
     "source_type": "encyclopedia", "reliability": "medium",
     "notes": "通过Jina reader访问失败（超时）。"},
]


# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  BUILD FUNCTIONS                                                        ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"luodian_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "人大" not in post and "政协" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post or "监委" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post and "人大" not in post and "政协" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post and "人大" not in post and "政协" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "监委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "纪委": "255,200,150",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>罗甸县领导班子关系网络（数据待补充）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, sources, custom_identity=None):
        """Generate a person graph JSON following the person_graph_json.md schema."""
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "罗甸县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "as of 2026-07"
            },
            "identity": {
                "person_id": f"luodian_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if "书记" in p.get("current_post", "") or "县长" in p.get("current_post", "") else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未找到该人物负面信号——但公开信息极其有限",
                 "date": "", "confidence": "unverified", "source_ids": []}
            ],
            "source_register": sources,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": f"{p['name']}的姓名、完整履历全部未知——罗甸县政府网站无法访问，外部搜索引擎均被封锁"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的真实姓名是什么",
                 "why_it_matters": "这是最基本的身份信息，一切后续研究的前提",
                 "suggested_queries": [f"罗甸县 {p.get('current_post','').replace('【待查】','')}", "罗甸县人民政府 领导之窗", "黔南州 罗甸县 任前公示"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径、系统经历和工作交集",
                 "suggested_queries": [f"罗甸县 {p.get('current_post','').replace('【待查】','')} 简历", f"{p.get('current_post','').replace('【待查】','')} 任职"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 县委书记 Person JSON ──
    sx_timeline = [
        {"start": "", "end": "",
         "org": "中共罗甸县委员会", "title": "罗甸县委书记",
         "notes": "现任—姓名待确认。公开网络渠道全部无法访问。",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "该人物在担任罗甸县委书记前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    sx_relationships = [
        {"person": "罗甸县长", "person_id": "luodian_【待查】罗甸县长",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委书记与县长为县委常委会和政府班子核心搭档（职务关系，具体人名待确认）",
         "overlap_org": "中共罗甸县委员会/罗甸县人民政府",
         "overlap_period": "待查",
         "direction": "undirected", "confidence": "plausible", "source_ids": []},
    ]

    sx_json = make_person_json(persons[0], sx_timeline, sx_relationships, source_register)
    sx_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-县委书记-待查.json")
    with open(sx_path, "w", encoding="utf-8") as f:
        json.dump(sx_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {sx_path}")

    # ── 县长 Person JSON ──
    lhl_timeline = [
        {"start": "", "end": "",
         "org": "罗甸县人民政府", "title": "罗甸县委副书记、县人民政府县长",
         "notes": "现任—姓名待确认。公开网络渠道全部无法访问。",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口", "title": "",
         "notes": "该人物在担任罗甸县长前的完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    lhl_relationships = [
        {"person": "罗甸县委书记", "person_id": "luodian_【待查】罗甸县委书记",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长（县委副书记）与县委书记在县委常委会和政府班子共事（职务关系，具体人名待确认）",
         "overlap_org": "中共罗甸县委员会/罗甸县人民政府",
         "overlap_period": "待查",
         "direction": "undirected", "confidence": "plausible", "source_ids": []},
    ]

    lhl_json = make_person_json(persons[1], lhl_timeline, lhl_relationships, source_register)
    lhl_path = os.path.join(PERSONS_DIR, f"{now}-{PROVINCE}-{PARENT_CITY}-县长-待查.json")
    with open(lhl_path, "w", encoding="utf-8") as f:
        json.dump(lhl_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lhl_path}")

    print("\n✅ All artifacts generated (with partial data — names and biographies pending).")
    print("⚠️  Web access to Chinese government sites was blocked during this research session.")
    print("⚠️  All person names marked as 【待查】. Run this script again after successful web access.")
    print("⚠️  See open_questions in person JSONs and open_gaps.md for priority research items.")


if __name__ == "__main__":
    build()
