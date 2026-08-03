#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yanggu County (阳谷县) leadership network.
   聊城市, 山东省.

Data confirmed from:
- yanggu.gov.cn leadership window page (2026-06-02)
- yanggu.gov.cn news articles (2026-07-29 to 2026-08-01)
"""

import sqlite3, os, sys, json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "阳谷县"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING / "persons"
REPORT_DIR = STAGING / "report"
os.makedirs(PERSONS_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

TODAY = "2026-08-03"
YG_SRC = "http://www.yanggu.gov.cn/"
YG_LDZC = "http://www.yanggu.gov.cn/channel_t_272_31043/doc_65213e4399b4c2316b3c262c.html"

# ── PERSONS (comprehensive, with all confirmed data) ──
persons = [
    {"id": 1, "name": "彭志国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共阳谷县委书记",
     "current_org": "中共阳谷县委员会",
     "source": YG_SRC + " (2026.07.29 走访驻军; 2026.07.30 工商联会议; 2026.07.30 县委常委会民主生活会)"},

    {"id": 2, "name": "杨旭博", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "", "education": "研究生/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县委副书记、县长",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 3, "name": "秦立忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县委常委、副县长（常务）",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 4, "name": "徐卫忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-01", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县委常委、副县长",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 5, "name": "申春青", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县副县长、四级调研员",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 6, "name": "卢加广", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县副县长",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 7, "name": "张昆", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县副县长、县公安局局长",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 8, "name": "唐恒波", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-03", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县副县长",
     "current_org": "阳谷县人民政府",
     "source": YG_LDZC},

    {"id": 9, "name": "贺洪贵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县领导",
     "current_org": "阳谷县",
     "source": YG_SRC + " (2026.07.29 走访驻军新闻)"},

    {"id": 10, "name": "李继帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县领导",
     "current_org": "阳谷县",
     "source": YG_SRC + " (2026.07.30 经济运行分析会)"},

    {"id": 11, "name": "刘凡成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县领导",
     "current_org": "阳谷县",
     "source": YG_SRC + " (2026.07.30 工商联会议)"},

    {"id": 12, "name": "马颖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县领导",
     "current_org": "阳谷县",
     "source": YG_SRC + " (2026.07.30 工商联会议)"},

    {"id": 13, "name": "孔帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县领导",
     "current_org": "阳谷县",
     "source": YG_SRC + " (2026.07.30 工商联会议)"},

    {"id": 14, "name": "王勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "阳谷县人大常委会副主任、县总工会主席",
     "current_org": "阳谷县人大常委会",
     "source": YG_SRC + " (2026.07.30 工商联会议群团致词)"},
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共阳谷县委员会", "type": "党委", "level": "县级", "parent": "中共聊城市委员会", "location": "聊城市阳谷县"},
    {"id": 2, "name": "阳谷县人民政府", "type": "政府", "level": "县级", "parent": "聊城市人民政府", "location": "聊城市阳谷县"},
    {"id": 3, "name": "阳谷县人大常委会", "type": "人大", "level": "县级", "parent": "聊城市人大常委会", "location": "聊城市阳谷县"},
    {"id": 4, "name": "阳谷县公安局", "type": "政府", "level": "县级", "parent": "阳谷县人民政府", "location": "聊城市阳谷县"},
    {"id": 5, "name": "阳谷县总工会", "type": "群团", "level": "县级", "parent": "阳谷县", "location": "聊城市阳谷县"},
    {"id": 6, "name": "阳谷县政协", "type": "政协", "level": "县级", "parent": "聊城市政协", "location": "聊城市阳谷县"},
    {"id": 7, "name": "阳谷县纪检监察委员会", "type": "纪委", "level": "县级", "parent": "中共聊城市纪委", "location": "聊城市阳谷县"},
]

# ── POSITIONS ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "中共阳谷县委书记", "start": "", "end": "present", "rank": "正处级", "note": "confirmed from yanggu.gov.cn 2026-07 news"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "confirmed from yanggu.gov.cn leadership window"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present", "rank": "正处级", "note": "confirmed from yanggu.gov.cn leadership window"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（常务）", "start": "", "end": "present", "rank": "副处级", "note": "负责县政府常务工作"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工业信息、市场监管、交通等"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责乡村振兴、农业农村等"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责工业园区、商务文旅、金融等"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、司法、信访等"},
    {"person_id": 7, "org_id": 4, "title": "县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责住建、自然资源、环保等"},
    {"person_id": 9, "org_id": 1, "title": "县领导（县委或政府班子）", "start": "", "end": "present", "rank": "", "note": "exact post unknown"},
    {"person_id": 10, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "exact post unknown"},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "exact post unknown"},
    {"person_id": 12, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "exact post unknown"},
    {"person_id": 13, "org_id": 1, "title": "县领导", "start": "", "end": "present", "rank": "", "note": "exact post unknown"},
    {"person_id": 14, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "县总工会主席", "start": "", "end": "present", "rank": "未知", "note": "兼任"},
]

# ── RELATIONSHIPS ──
relationships = [
    # Core duo
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "阳谷县委/县政府", "overlap_period": "2024-2026"},
    # Party vs government team
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长（县委常委）", "overlap_org": "阳谷县委常委会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委、副县长", "overlap_org": "阳谷县委常委会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长兼公安局长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    # Peers
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "同为县委常委、副县长", "overlap_org": "阳谷县", "overlap_period": "2026"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "同为副县长", "overlap_org": "阳谷县政府", "overlap_period": "2026"},
    # Event-based overlaps
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "共同参加八一走访驻军", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "共同参加八一走访驻军", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "共同参加经济运行分析会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "共同参加经济运行分析会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "共同参加经济运行分析会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "共同参加工商联代表大会", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "人大副主任出席工商联会议", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
    {"person_a": 14, "person_b": 2, "type": "overlap", "context": "人大副主任出席工商联会议", "overlap_org": "阳谷县", "overlap_period": "2026-07"},
]


def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def person_color(post):
    if "县委书记" in post and "副" not in post and "委" not in post.replace("副",""):
        return "255,50,50"
    if "县长" in post and "副" not in post and "常务" not in post:
        return "50,100,255"
    if "常委" in post:
        return "100,150,220"
    if "副主任" in post or "总工会" in post:
        return "60,180,60"
    if "县领导" in post:
        return "100,100,100"
    return "100,100,100"


def is_top_leader(post):
    return ("县委书记" in post and "副" not in post) or ("县长" in post and "副" not in post and "常务" not in post)


def org_color(otype):
    colors = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
              "政协": "255,240,200", "纪委": "255,200,150", "群团": "255,220,255"}
    return colors.get(otype, "200,200,200")


def build():
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
        pid = f"阳谷县_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender",""), p.get("ethnicity",""), p.get("birth",""),
                     p.get("birthplace",""), p.get("education",""), p.get("party_join",""), p.get("work_start",""),
                     p.get("current_post",""), p.get("current_org",""), p.get("source","")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o.get("level",""), o.get("parent",""), o.get("location","")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start",""),
                     pos.get("end",""), pos.get("rank",""), pos.get("note","")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org",""), r.get("overlap_period","")))

    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>阳谷县领导班子关系网络（基于yanggu.gov.cn官方新闻）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    build()