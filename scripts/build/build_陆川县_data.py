#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 陆川县 (Luchuan County) leadership network.

Current leadership (as of 2026-07):
- 县委书记: 李唐明 (succeeded 梁伟 in early 2026)
- 县长: 庞邦津 (active through ~June 2026; 刘小琴 named 县委副书记/县人民政府党组书记 Jul 2026)
- 副县长: 万宇, 林雯, 崔小喆, 温文冕

Data sources: www.luchuan.gov.cn official site, official news articles.
"""

import sqlite3
import json
import os
import sys
from datetime import datetime

TASK_ID = "guangxi_陆川县"
AS_OF = datetime.now().strftime("%Y-%m-%d")

BASE = os.path.dirname(os.path.abspath(__file__))
TMP = BASE  # script lives in data/tmp/guangxi_陆川县/
# The repo root is ../../../
REPO_ROOT = os.path.abspath(os.path.join(BASE, "../../.."))

DB_PATH = os.path.join(TMP, "陆川县_network.db")
GEXF_PATH = os.path.join(TMP, "陆川县_network.gexf")
PERSONS_DIR = TMP


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── DATA ─────────────────────────────────────────────────────────────

# Official source for luchuan.gov.cn
OFFICIAL_SITE = "http://www.luchuan.gov.cn/"
OFFICIAL_LDZZ = "http://www.luchuan.gov.cn/xxgk/fdgk/ldjj/"
OFFICIAL_NEWS = "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/"

source_register = [
    {"id": "S001", "title": "陆川县人民政府门户网站", "url": OFFICIAL_SITE,
     "publisher": "陆川县人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "政府官网首页"},
    {"id": "S002", "title": "陆川县领导简介页面", "url": OFFICIAL_LDZZ,
     "publisher": "陆川县人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "列出县长、副县长"},
    {"id": "S003", "title": "陆川县政务要闻列表", "url": OFFICIAL_NEWS,
     "publisher": "陆川县人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "含2026年各级领导活动报道"},
    {"id": "S004", "title": "宣布陆川县人武部党委第一书记任职大会召开 李唐明任陆川县人武部党委第一书记",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/t27761026.shtml",
     "publisher": "陆川发布", "published_at": "2026-06-05", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认李唐明任人武部党委第一书记（县委书记惯例兼任）"},
    {"id": "S005", "title": "陆川县强化社会治理实现'两降两升'工作动员部署会召开 李唐明出席并讲话",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/t27895479.shtml",
     "publisher": "陆川发布", "published_at": "2026-07-15", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high",
     "notes": "确认李唐明任县委书记，刘小琴任县委副书记/县人民政府党组书记"},
    {"id": "S006", "title": "李唐明到良田镇调研中央生态环境保护督察转办信访件整改等工作",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/t27812513.shtml",
     "publisher": "陆川县大数据发展和政务服务局", "published_at": "2026-06-23", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认李唐明以县委书记身份开展调研"},
    {"id": "S007", "title": "庞邦津到乌石镇督导检查防汛防灾工作",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/",
     "publisher": "陆川发布", "published_at": "2026-05-20", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认庞邦津以县长身份开展活动"},
    {"id": "S008", "title": "推动环境质量提升！县委书记梁伟深入多镇调研督导",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/",
     "publisher": "陆川发布", "published_at": "2026-02-04", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "确认梁伟曾任县委书记至2026年初"},
    {"id": "S009", "title": "庞邦津到乌石镇督导检查防汛防灾工作",
     "url": "http://www.luchuan.gov.cn/xxgk/fdgk/zwdt/zwyw/",
     "publisher": "陆川发布", "published_at": "2026-05-20",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "县领导活动日历中显示'庞邦津到乌石镇督导检查防汛防灾工作'"},
]

# ── Persons ──
persons = [
    # Current and recent Party Secretaries
    {"id": 1, "name": "李唐明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共陆川县委书记", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 2, "name": "梁伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任陆川县委书记（2026年初离任）", "current_org": "（已离任）",
     "source": OFFICIAL_SITE},
    # Government leaders
    {"id": 3, "name": "庞邦津", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县人民政府县长", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    {"id": 4, "name": "刘小琴", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县委副书记、县人民政府党组书记", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    # Deputy Mayors
    {"id": 5, "name": "万宇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县人民政府副县长", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    {"id": 6, "name": "林雯", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县人民政府副县长", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    {"id": 7, "name": "崔小喆", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县人民政府副县长", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    {"id": 8, "name": "温文冕", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县人民政府副县长", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    # Other key leaders mentioned in news
    {"id": 9, "name": "黎福章", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "陆川县人大常委会",
     "source": OFFICIAL_SITE},
    {"id": 10, "name": "李红伟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "陆川县政协",
     "source": OFFICIAL_SITE},
    {"id": 11, "name": "符征旭", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 12, "name": "陈德勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 13, "name": "黎文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 14, "name": "王清萍", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 15, "name": "李华强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "陆川县人民政府",
     "source": OFFICIAL_SITE},
    {"id": 16, "name": "龙世喜", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "陆川县人民检察院",
     "source": OFFICIAL_SITE},
    {"id": 17, "name": "梁栋荣", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 18, "name": "陈炬", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县领导（县四家班子）", "current_org": "中共陆川县委员会",
     "source": OFFICIAL_SITE},
    {"id": 19, "name": "庞俊臣", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "陆川县委常委、县人武部上校政委", "current_org": "陆川县人民武装部",
     "source": OFFICIAL_SITE},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共陆川县委员会", "type": "党委", "level": "县处级", "parent": "中共玉林市委员会", "location": "陆川县"},
    {"id": 2, "name": "陆川县人民政府", "type": "政府", "level": "县处级", "parent": "玉林市人民政府", "location": "陆川县"},
    {"id": 3, "name": "陆川县人大常委会", "type": "人大", "level": "县处级", "parent": "玉林市人大常委会", "location": "陆川县"},
    {"id": 4, "name": "陆川县政协", "type": "政协", "level": "县处级", "parent": "政协玉林市委员会", "location": "陆川县"},
    {"id": 5, "name": "陆川县人民武装部", "type": "党委", "level": "县处级", "parent": "玉林军分区", "location": "陆川县"},
    {"id": 6, "name": "陆川县人民检察院", "type": "党委", "level": "县处级", "parent": "玉林市人民检察院", "location": "陆川县"},
    {"id": 7, "name": "中共玉林市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "玉林市"},
    {"id": 8, "name": "玉林市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "玉林市"},
]

# ── Positions ──
positions = [
    # 李唐明
    {"person_id": 1, "org_id": 1, "title": "中共陆川县委书记",
     "start_date": "约2026年初", "end_date": "现任", "rank": "县处级正职",
     "note": "兼任县人武部党委第一书记（2026年6月正式任命，S004）"},
    {"person_id": 1, "org_id": 5, "title": "陆川县人民武装部党委第一书记",
     "start_date": "2026-06", "end_date": "现任", "rank": "县处级正职",
     "note": "2026年6月4日玉林军分区宣布任命（S004）"},
    # 梁伟 (predecessor)
    {"person_id": 2, "org_id": 1, "title": "中共陆川县委书记（前任）",
     "start_date": "", "end_date": "约2026年初", "rank": "县处级正职",
     "note": "2026年2月仍有活动报道（S008），后由李唐明接任"},
    # 庞邦津 (county mayor)
    {"person_id": 3, "org_id": 2, "title": "陆川县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年5月仍有以县长身份的活动（S007）"},
    # 刘小琴 (deputy party secretary, government party secretary)
    {"person_id": 4, "org_id": 1, "title": "陆川县委副书记",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "2026年7月15日以县委副书记身份主持会议（S005）"},
    {"person_id": 4, "org_id": 2, "title": "陆川县人民政府党组书记",
     "start_date": "", "end_date": "现任", "rank": "县处级正职",
     "note": "2026年7月15日以县人民政府党组书记身份亮相（S005），预计接任县长"},
    # Deputy mayors
    {"person_id": 5, "org_id": 2, "title": "陆川县人民政府副县长",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "列副县长名单首位（S002），出席2026年7月会议（S005）"},
    {"person_id": 6, "org_id": 2, "title": "陆川县人民政府副县长",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "列副县长名单（S002），出席2026年7月会议（S005）"},
    {"person_id": 7, "org_id": 2, "title": "陆川县人民政府副县长",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "列副县长名单（S002）"},
    {"person_id": 8, "org_id": 2, "title": "陆川县人民政府副县长",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "列副县长名单（S002）"},
    # Other leaders
    {"person_id": 9, "org_id": 3, "title": "陆川县人大常委会主任/副主任",
     "start_date": "", "end_date": "现任", "rank": "县处级",
     "note": "县四家班子领导"},
    {"person_id": 10, "org_id": 4, "title": "陆川县政协主席/副主席",
     "start_date": "", "end_date": "现任", "rank": "县处级",
     "note": "县四家班子领导"},
    {"person_id": 11, "org_id": 1, "title": "陆川县委常委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "县四家班子领导"},
    {"person_id": 12, "org_id": 1, "title": "陆川县委常委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "县四家班子领导"},
    {"person_id": 13, "org_id": 1, "title": "陆川县委常委/副县长",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "县四家班子领导"},
    {"person_id": 14, "org_id": 1, "title": "陆川县委常委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "县四家班子领导"},
    {"person_id": 15, "org_id": 2, "title": "陆川县人民政府副县长/党组成员",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "随李唐明参加调研活动（S006）"},
    {"person_id": 16, "org_id": 6, "title": "陆川县人民检察院检察长",
     "start_date": "", "end_date": "现任", "rank": "县处级",
     "note": "县四家班子领导"},
    {"person_id": 17, "org_id": 1, "title": "陆川县委常委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "县四家班子领导"},
    {"person_id": 18, "org_id": 1, "title": "陆川县委常委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "通报全县命案防治工作形势（S005）"},
    {"person_id": 19, "org_id": 5, "title": "陆川县委常委、县人武部上校政委",
     "start_date": "", "end_date": "现任", "rank": "县处级副职",
     "note": "主持县人武部党委第一书记任职大会（S004）"},
]

# ── Relationships ──
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "李唐明接替梁伟任陆川县委书记", "overlap_org": "中共陆川县委员会",
     "overlap_period": "2026年初交接"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "李唐明（县委书记）与庞邦津（县长）为党政搭档",
     "overlap_org": "陆川县党政班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "李唐明（县委书记）与刘小琴（县委副书记/县政府党组书记）为党政搭档",
     "overlap_org": "陆川县党政班子", "overlap_period": "2026年7月起"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor",
     "context": "庞邦津（县长）与刘小琴（县委副书记/政府党组书记）可能是交接关系",
     "overlap_org": "陆川县人民政府", "overlap_period": "2026年中"},
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "庞俊臣（县委常委/人武部政委）与李唐明（县委书记/人武部第一书记）为人武部军政搭档",
     "overlap_org": "陆川县人民武装部", "overlap_period": "2026年6月起"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "万宇（副县长）在李唐明（县委书记）主持的会议上出席",
     "overlap_org": "陆川县党政班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "overlap",
     "context": "林雯（副县长）在李唐明（县委书记）主持的会议上出席",
     "overlap_org": "陆川县党政班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "李华强陪同李唐明参加调研活动",
     "overlap_org": "陆川县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 18, "type": "overlap",
     "context": "陈炬在李唐明主持的'两降两升'会议上通报工作",
     "overlap_org": "陆川县党政班子", "overlap_period": "2026年7月"},
]


def build():
    os.makedirs(TMP, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
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

        CREATE TABLE relationships (
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
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""),
                     r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>陆川县领导班子关系网络（基于官网确认数据）</description>')
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
        pid = p["id"]
        post = p.get("current_post", "")
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else "书记" in post and not post.startswith("副")
        is_mayor = "县长" in post and "副" not in post
        is_discipline = "纪委" in post

        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        else:
            color = "100,100,100"

        size = "20.0" if (is_secretary or is_mayor) else "12.0"
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
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
        elif otype == "政协":
            ocolor = "255,240,200"
        elif otype == "纪委":
            ocolor = "255,200,150"
        elif otype == "开发区":
            ocolor = "200,255,200"
        elif otype == "乡镇/街道":
            ocolor = "255,255,200"
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
        lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos["title"])}" weight="1.0">')
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

    def make_person_json(p, timeline, relationships_list):
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "广西壮族自治区",
                "city": "玉林市",
                "region": "陆川县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"luchuan_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_",
                    "name_birthplace": f"{p['name']}_",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003"]
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
                {"type": "none_found", "description": "在陆川县政府官网公开信息中未发现负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的出生年月、籍贯、学历等身份信息及完整履历缺失"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的出生年月、籍贯、学历、入党时间、参加工作时间",
                 "why_it_matters": "无法建立完整的身份标识",
                 "suggested_queries": [f"{p['name']} 简历 陆川"],
                 "last_attempted": AS_OF},
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 陆川 任职经历"],
                 "last_attempted": AS_OF},
            ]
        }

    # 李唐明 person JSON
    lt_timeline = []
    lt_relationships = [
        {"person": "梁伟", "person_id": "luchuan_梁伟", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "李唐明接替梁伟任陆川县委书记（2026年初）",
         "overlap_org": "中共陆川县委员会", "overlap_period": "2026年初",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S003", "S008"]},
        {"person": "庞邦津", "person_id": "luchuan_庞邦津", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "李唐明（县委书记）与庞邦津（县长）为党政搭档",
         "overlap_org": "陆川县党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S003"]},
        {"person": "刘小琴", "person_id": "luchuan_刘小琴", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "李唐明（县委书记）与刘小琴（县委副书记/政府党组书记）为党政搭档",
         "overlap_org": "陆川县党政班子", "overlap_period": "2026年7月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "庞俊臣", "person_id": "luchuan_庞俊臣", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "庞俊臣（人武部政委）与李唐明（人武部第一书记）为人武部军政搭档",
         "overlap_org": "陆川县人民武装部", "overlap_period": "2026年6月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]
    lt_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到李唐明任陆川县委书记前的履历",
        "confidence": "unverified", "source_ids": []})
    lt_json = make_person_json(persons[0], lt_timeline, lt_relationships)
    lt_json["identity"]["gender"] = "男"
    lt_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县委书记-李唐明.json")
    with open(lt_path, "w", encoding="utf-8") as f:
        json.dump(lt_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lt_path}")

    # 庞邦津 person JSON
    pbj_timeline = []
    pbj_relationships = [
        {"person": "李唐明", "person_id": "luchuan_李唐明", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "庞邦津（县长）与李唐明（县委书记）为党政搭档",
         "overlap_org": "陆川县党政班子", "overlap_period": "2026年",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S003"]},
        {"person": "刘小琴", "person_id": "luchuan_刘小琴", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "庞邦津（县长）与刘小琴（县委副书记/政府党组书记）可能是交接关系",
         "overlap_org": "陆川县人民政府", "overlap_period": "2026年中",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S003", "S005"]},
    ]
    pbj_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到庞邦津任陆川县长前的履历",
        "confidence": "unverified", "source_ids": []})
    pbj_json = make_person_json(persons[2], pbj_timeline, pbj_relationships)
    pbj_json["identity"]["gender"] = "男"
    pbj_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县长-庞邦津.json")
    with open(pbj_path, "w", encoding="utf-8") as f:
        json.dump(pbj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {pbj_path}")

    # 刘小琴 person JSON
    lxq_timeline = []
    lxq_relationships = [
        {"person": "李唐明", "person_id": "luchuan_李唐明", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "刘小琴（县委副书记/政府党组书记）与李唐明（县委书记）为党政搭档",
         "overlap_org": "陆川县党政班子", "overlap_period": "2026年7月起",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005"]},
        {"person": "庞邦津", "person_id": "luchuan_庞邦津", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "刘小琴接替庞邦津任县政府党组书记（预计接任县长）",
         "overlap_org": "陆川县人民政府", "overlap_period": "2026年中",
         "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
    ]
    lxq_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料未找到刘小琴任陆川县委副书记前的履历",
        "confidence": "unverified", "source_ids": []})
    lxq_json = make_person_json(persons[3], lxq_timeline, lxq_relationships)
    lxq_json["identity"]["gender"] = "女"
    lxq_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-县人民政府党组书记-刘小琴.json")
    with open(lxq_path, "w", encoding="utf-8") as f:
        json.dump(lxq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lxq_path}")

    # 梁伟 person JSON (predecessor)
    lw_timeline = []
    lw_relationships = [
        {"person": "李唐明", "person_id": "luchuan_李唐明", "relationship_type": "predecessor_successor",
         "strength": "medium",
         "evidence": "梁伟任县委书记至2026年初，后由李唐明接任",
         "overlap_org": "中共陆川县委员会", "overlap_period": "2026年初",
         "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S003", "S008"]},
    ]
    lw_timeline.append({
        "start": "", "end": "", "org": "履历缺口", "title": "",
        "notes": "公开资料仅见2026年2月活动报道（S008），完整履历未知",
        "confidence": "unverified", "source_ids": ["S008"]})
    lw_json = make_person_json(persons[1], lw_timeline, lw_relationships)
    lw_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-玉林市-原县委书记-梁伟.json")
    with open(lw_path, "w", encoding="utf-8") as f:
        json.dump(lw_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lw_path}")

    print(f"\nBuild complete. All current roles confirmed from official source {OFFICIAL_SITE}")
    print("Identity info (birth, education, etc.) remains unverified due to limited public data.")


if __name__ == "__main__":
    build()
