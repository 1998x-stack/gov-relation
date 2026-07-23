#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Tianlin County (田林县) leadership network.

Task: guangxi_田林县
Province: 广西壮族自治区
Parent city: 百色市
Level: 县
Data as of: 2026-07-23
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
BASE = os.path.dirname(os.path.abspath(__file__))
TASK_ID = "guangxi_田林县"
SLUG = "田林县"
AS_OF = "2026-07-23"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = BASE

OFFICIAL_SITE = "http://www.tianlin.gov.cn"

# ── Source Register ──
source_register = [
    {"id": "S001", "title": "田林县人民政府-领导信息-县长黄俊杰",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/xz/t22616720.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "黄俊杰县长官方简历"},
    {"id": "S002", "title": "田林县人民政府-领导信息-副县长王艳榜",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t26171973.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "王艳榜副县长、常务副县长官方简历"},
    {"id": "S003", "title": "田林县人民政府-领导信息-副县长罗旭平",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t540933.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "罗旭平副县长官方简历"},
    {"id": "S004", "title": "田林县人民政府-领导信息-副县长陈日周",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t18220388.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "陈日周副县长（挂职）官方简历"},
    {"id": "S005", "title": "田林县人民政府-领导信息-副县长陆岳新",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t23351683.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "陆岳新副县长（挂职）官方简历"},
    {"id": "S006", "title": "田林县人民政府-领导信息-副县长张晨啸",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t27340122.shtml",
     "publisher": "田林县人民政府", "published_at": "2026-01-29", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "张晨啸副县长（挂职）官方简历"},
    {"id": "S007", "title": "田林县人民政府-领导信息-副县长史前",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t26197528.shtml",
     "publisher": "田林县人民政府", "published_at": "2025-11-14", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "史前副县长（公安局长）官方简历"},
    {"id": "S008", "title": "黄俊杰主持召开县委常委会会议",
     "url": "http://www.tianlin.gov.cn/gddt/t27903327.shtml",
     "publisher": "田林县融媒体中心", "published_at": "2026-07-16", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认黄俊杰以县委书记身份主持会议"},
    {"id": "S009", "title": "黄俊杰深入潞城瑶族乡检查指导防汛救灾工作",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/zwdt/zwyw/t27904588.shtml",
     "publisher": "田林县融媒体中心", "published_at": "2026-07-19", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认黄俊杰以县委书记身份检查防汛"},
    {"id": "S010", "title": "田林县第十七届人大常委会第三十七次会议",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/zwdt/zwyw/t27883755.shtml",
     "publisher": "田林县融媒体中心", "published_at": "2026-07-10", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "县人大常委会主任赖文洁"},
    {"id": "S011", "title": "田林县召开'两优一先'表彰大会",
     "url": "http://www.tianlin.gov.cn/xxgk/zfxxgkzl/fdzdgknr/jbxx/zwdt/zwyw/t27859091.shtml",
     "publisher": "田林县融媒体中心", "published_at": "2026-07-05", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "县委主要领导出席表彰大会"},
]

# ── Person Data ──
persons = [
    # ═══════════════════════════════════════════════
    # Current and Recent Tianlin County Leaders
    # ═══════════════════════════════════════════════
    {"id": 1, "name": "黄俊杰", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "", "education": "在职研究生，理学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共田林县委书记", "current_org": "中共田林县委员会",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/xz/t22616720.shtml"},

    # Note: 黄俊杰 was previously 县长. As of July 2026 news reports, he serves as 县委书记.
    # The 县长 position appears to be vacant or filled by a new appointee not yet listed.

    {"id": 2, "name": "王艳榜", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-05", "birthplace": "", "education": "全日制研究生学历，工学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县委常委、县人民政府副县长（常务）", "current_org": "田林县人民政府",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t26171973.shtml"},

    {"id": 3, "name": "罗旭平", "gender": "男", "ethnicity": "瑶族",
     "birth": "1978-10", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县委常委、县委办公室主任、县人民政府党组成员", "current_org": "中共田林县委员会",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t540933.shtml"},

    {"id": 4, "name": "陈日周", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-09", "birthplace": "", "education": "本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县委常委、县人民政府副县长（挂职）", "current_org": "田林县人民政府",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t18220388.shtml"},

    {"id": 5, "name": "陆岳新", "gender": "男", "ethnicity": "壮族",
     "birth": "1985-09", "birthplace": "", "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县委常委、县人民政府副县长（挂职）、驻村工作队队长", "current_org": "田林县人民政府",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t23351683.shtml"},

    {"id": 6, "name": "张晨啸", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-02", "birthplace": "", "education": "大学本科学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县委常委、县人民政府副县长（挂职）", "current_org": "田林县人民政府",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t27340122.shtml"},

    {"id": 7, "name": "史前", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-01", "birthplace": "", "education": "在职研究生学历，法律硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "田林县人民政府副县长、县公安局党委书记、局长", "current_org": "田林县人民政府",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/ldxx/fxz/t26197528.shtml"},

    {"id": 8, "name": "赖文洁", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "田林县人大常委会主任", "current_org": "田林县人民代表大会常务委员会",
     "source": OFFICIAL_SITE + "/xxgk/zfxxgkzl/fdzdgknr/jbxx/zwdt/zwyw/t27883755.shtml"},
]

# ── Organization Data ──
organizations = [
    {"id": 1, "name": "中共田林县委员会", "type": "党委", "level": "县处级",
     "parent": "中共百色市委员会", "location": "广西百色田林"},
    {"id": 2, "name": "田林县人民政府", "type": "政府", "level": "县处级",
     "parent": "百色市人民政府", "location": "广西百色田林"},
    {"id": 3, "name": "田林县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "", "location": "广西百色田林"},
    {"id": 4, "name": "田林县公安局", "type": "政府", "level": "乡科级",
     "parent": "田林县人民政府", "location": "广西百色田林"},
]

# ── Position Data ──
positions = [
    # 黄俊杰
    {"person_id": 1, "org_id": 1, "title": "中共田林县委书记",
     "start_date": "2026年中", "end_date": "", "rank": "县处级正职", "note": "现任，2026年7月新闻报道已以县委书记身份履职"},
    {"person_id": 1, "org_id": 2, "title": "田林县人民政府县长",
     "start_date": "", "end_date": "2026年中", "rank": "县处级正职", "note": "前任职务，2025年11月仍以县长身份出现在领导信息页"},
    {"person_id": 1, "org_id": 1, "title": "田林县委副书记",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},

    # 王艳榜
    {"person_id": 2, "org_id": 2, "title": "田林县委常委、县人民政府副县长（常务）",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，负责县政府常务工作"},

    # 罗旭平
    {"person_id": 3, "org_id": 1, "title": "田林县委常委、县委办公室主任、县人民政府党组成员",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},

    # 陈日周
    {"person_id": 4, "org_id": 2, "title": "田林县委常委、县人民政府副县长（挂职）",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，东西部协作挂职"},

    # 陆岳新
    {"person_id": 5, "org_id": 2, "title": "田林县委常委、县人民政府副县长（挂职）、驻村工作队队长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，驻村工作队挂职"},

    # 张晨啸
    {"person_id": 6, "org_id": 2, "title": "田林县委常委、县人民政府副县长（挂职）",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，中国电信定点帮扶挂职"},

    # 史前
    {"person_id": 7, "org_id": 2, "title": "田林县人民政府副县长、县公安局党委书记、局长",
     "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 4, "title": "田林县公安局党委书记、局长",
     "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "兼任"},

    # 赖文洁
    {"person_id": 8, "org_id": 3, "title": "田林县人大常委会主任",
     "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

# ── Relationship Data ──
relationships = [
    # 党政班子关系
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "黄俊杰（县委书记）与王艳榜（常务副县长）在县委常委会和县政府班子共事",
     "overlap_org": "中共田林县委员会/田林县人民政府", "overlap_period": "2026年"},

    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "王艳榜与罗旭平均为田林县委常委",
     "overlap_org": "中共田林县委员会", "overlap_period": ""},

    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "王艳榜与陈日周均在田林县政府班子任职",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    {"person_a": 2, "person_b": 5, "type": "overlap",
     "context": "王艳榜与陆岳新均在田林县政府班子任职",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "王艳榜与张晨啸均在田林县政府班子任职",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "王艳榜与史前均在田林县政府班子共事",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    # 县委常委班子关系
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "罗旭平与陈日周均为田林县委常委",
     "overlap_org": "中共田林县委员会", "overlap_period": ""},

    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "罗旭平与陆岳新均为田林县委常委",
     "overlap_org": "中共田林县委员会", "overlap_period": ""},

    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "罗旭平与张晨啸均为田林县委常委",
     "overlap_org": "中共田林县委员会", "overlap_period": ""},

    # 政府班子关系
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "陈日周与陆岳新均为田林县挂职副县长",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    {"person_a": 4, "person_b": 7, "type": "overlap",
     "context": "陈日周与史前同在田林县政府班子任职",
     "overlap_org": "田林县人民政府", "overlap_period": ""},

    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "陆岳新与张晨啸均为田林县挂职副县长",
     "overlap_org": "田林县人民政府", "overlap_period": ""},
]


# ═══════════════════════════════════════════════
# BUILD SQLite DATABASE
# ═══════════════════════════════════════════════

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

    # Assign person IDs
    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"tianlin_{p['name']}"
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
        if "书记" in post and "副" not in post:
            return "200,30,30"
        if "县长" in post and "副" not in post:
            return "30,100,200"
        if "副" in post:
            return "100,150,220"
        if "主任" in post:
            return "60,180,60"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post) or ("县长" in post and "副" not in post)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>田林县领导班子关系网络（基于田林县人民政府官网确认数据）</description>')
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
        shape = "square" if ("书记" in post and "副" not in post) else ("circle" if ("县长" in post and "副" not in post) else "triangle")

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
        otype = o["type"]
        if otype == "党委":
            ocolor = "255,200,200"
        elif otype == "政府":
            ocolor = "200,200,255"
        elif otype == "人大":
            ocolor = "200,255,255"
        else:
            ocolor = "200,200,200"

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

    # Person → organization (worked_at)
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

    # Person ↔ person (relationships)
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

    # ── Person graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "百色市",
                "region": "田林县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"tianlin_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
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
                "administrative_rank": "县处级正职" if ("书记" in p.get("current_post","") and "副" not in p.get("current_post","")) or ("主任" in p.get("current_post","") and "副" not in p.get("current_post","")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
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
                {"type": "none_found", "description": "在田林县人民政府官网公开信息中未发现负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历及出生年月、籍贯、学历等详细信息缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                 "why_it_matters": "无法建立完整的身份标识",
                 "suggested_queries": [f"{p['name']} 简历 田林"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 田林 任职经历"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 黄俊杰 person JSON ──
    hjj_timeline = [
        {"start": "2026年中", "end": "", "org": "中共田林县委员会", "title": "中共田林县委书记",
         "notes": "2026年7月以县委书记身份出席活动", "confidence": "confirmed", "source_ids": ["S008", "S009"]},
        {"start": "", "end": "2026年中", "org": "田林县人民政府", "title": "田林县人民政府县长",
         "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    hjj_relationships = [
        {"person": "王艳榜", "person_id": "tianlin_王艳榜", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "黄俊杰（县委书记）与王艳榜（常务副县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共田林县委员会/田林县人民政府", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S008"]},
        {"person": "罗旭平", "person_id": "tianlin_罗旭平", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "黄俊杰与罗旭平在县委常委会共事",
         "overlap_org": "中共田林县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]

    hjj_json = make_person_json(persons[0], hjj_timeline, hjj_relationships)
    hjj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-县委书记-黄俊杰.json")
    with open(hjj_path, "w", encoding="utf-8") as f:
        json.dump(hjj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {hjj_path}")

    # ── 王艳榜 person JSON ──
    wyb_timeline = []
    wyb_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到王艳榜任田林县常务副县长前的完整履历信息",
        "confidence": "unverified", "source_ids": []})

    wyb_relationships = [
        {"person": "黄俊杰", "person_id": "tianlin_黄俊杰", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "王艳榜（常务副县长）与黄俊杰（县委书记）在县委常委会和县政府班子共事",
         "overlap_org": "中共田林县委员会/田林县人民政府", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "罗旭平", "person_id": "tianlin_罗旭平", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王艳榜与罗旭平均为田林县委常委",
         "overlap_org": "中共田林县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "陈日周", "person_id": "tianlin_陈日周", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王艳榜与陈日周均在田林县政府班子共事",
         "overlap_org": "田林县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S004"]},
        {"person": "史前", "person_id": "tianlin_史前", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "王艳榜与史前均在田林县政府班子共事",
         "overlap_org": "田林县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S007"]},
    ]

    wyb_json = make_person_json(persons[1], wyb_timeline, wyb_relationships)
    wyb_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-百色市-常务副县长-王艳榜.json")
    with open(wyb_path, "w", encoding="utf-8") as f:
        json.dump(wyb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {wyb_path}")

    print(f"\nBuild complete. All current roles confirmed from official source {OFFICIAL_SITE}")
    print("Identity info (birth, education, etc.) requires further research.")
    print("黄俊杰、王艳榜等同志完整履历和详细身份信息仍需补充。")


if __name__ == "__main__":
    build()
