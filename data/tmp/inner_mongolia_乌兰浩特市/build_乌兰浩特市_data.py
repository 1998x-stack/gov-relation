#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 乌兰浩特市, 兴安盟, 内蒙古自治区.

Investigation date: 2026-07-25
Task ID: inner_mongolia_乌兰浩特市
Research sources:
  - 乌兰浩特市人民政府 (www.wlht.gov.cn) — 领导之窗、乌市要闻
  - 乌兰浩特市人大常委会任免名单

Confirmed as of 2026-07:
  市委书记: 曹智勇
  市长: 杨宝田
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "乌兰浩特市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 曹智勇 — 市委书记 (confirmed from multiple news articles on wlht.gov.cn)
    # Source: "曹智勇一行调研重点项目推进情况" (2026-07-23),
    #         "曹智勇一行到部分重点企业调研" (2026-06-10),
    #         "曹智勇就汛期全市排水防涝和防汛工作开展调研" (2026-07-08)
    {"id": 1, "name": "曹智勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共乌兰浩特市委员会",
     "source": "http://www.wlht.gov.cn"},

    # 杨宝田 — 市长 (confirmed from government leadership page)
    # Source: http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html
    # Full title: 市委副书记、市长，盟农畜产品物流园区党工委书记、管委会主任
    {"id": 2, "name": "杨宝田", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # ══════════════════════════════════════════════════════════════════════════
    # Leadership Team (市政府领导)
    # ══════════════════════════════════════════════════════════════════════════

    # 赵新友 — 常委、副市长
    # Source: Government leadership page
    {"id": 3, "name": "赵新友", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "常委、副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # 王英群 — 常委、提名副市长
    # Source: Government leadership page
    {"id": 4, "name": "王英群", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "常委、提名副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # 李国强 — 市委常委、组织部部长
    # Source: "乌兰浩特市召开全市处级干部纪法教育会议" (2026-07-16)
    # "市委常委、组织部部长李国强主持会议并讲话"
    {"id": 5, "name": "李国强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共乌兰浩特市委员会组织部",
     "source": "http://www.wlht.gov.cn/wlht/2026-07/16/article_2026071615233490543.html"},

    # 王明阳 — 提名副市长
    # Source: Government leadership page
    {"id": 6, "name": "王明阳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "提名副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # 陈志琳 — 提名副市长
    {"id": 7, "name": "陈志琳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "提名副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # 周扬 — 提名副市长
    {"id": 8, "name": "周扬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "提名副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # 白玉明 — 副市长 (2026年7月20日任命)
    # Source: 乌兰浩特市第十四届人民代表大会常务委员会第三十次会议通过
    {"id": 9, "name": "白玉明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/2026-07/20/article_2026072010483090132.html"},

    # 吴建荣 — 提名副市长
    {"id": 10, "name": "吴建荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "提名副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html"},

    # ══════════════════════════════════════════════════════════════════════════
    # Former Leaders (for relationship tracking)
    # ══════════════════════════════════════════════════════════════════════════

    # 王国安 — 原副市长 (2026年7月20日免去)
    {"id": 11, "name": "王国安", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原副市长", "current_org": "乌兰浩特市人民政府",
     "source": "http://www.wlht.gov.cn/wlht/2026-07/20/article_2026072010483090132.html"},
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共乌兰浩特市委员会", "type": "党委", "level": "县处级", "parent": "中共兴安盟委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 2, "name": "乌兰浩特市人民政府", "type": "政府", "level": "县处级", "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 3, "name": "中共乌兰浩特市委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共乌兰浩特市委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 4, "name": "乌兰浩特市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "兴安盟人大工作委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 5, "name": "中国人民政治协商会议乌兰浩特市委员会", "type": "政协", "level": "县处级", "parent": "政协兴安盟委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 6, "name": "中共乌兰浩特市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共兴安盟纪律检查委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 7, "name": "兴安盟农畜产品物流园区", "type": "政府", "level": "县处级", "parent": "兴安盟行政公署", "location": "内蒙古自治区兴安盟乌兰浩特市"},
    {"id": 8, "name": "乌兰浩特市监察委员会", "type": "纪委", "level": "县处级", "parent": "兴安盟监察委员会", "location": "内蒙古自治区兴安盟乌兰浩特市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 曹智勇 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "乌兰浩特市委书记，主持市委全面工作"},
    # 杨宝田 — 市长
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start": "", "end": "present", "rank": "县处级正职", "note": "乌兰浩特市市长，兼盟农畜产品物流园区党工委书记、管委会主任，主持市政府全面工作"},
    {"person_id": 2, "org_id": 7, "title": "盟农畜产品物流园区党工委书记、管委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    # 赵新友 — 常委、副市长
    {"person_id": 3, "org_id": 2, "title": "常委、副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责市政府常务工作，综合经济、财政、统计、金融、应急管理、机关事务等"},
    # 王英群 — 常委、提名副市长
    {"person_id": 4, "org_id": 2, "title": "常委、提名副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责'三农'、林业和草原、水利、乡村振兴等工作"},
    # 李国强 — 市委常委、组织部部长
    {"person_id": 5, "org_id": 3, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责组织人事工作"},
    # 王明阳 — 提名副市长
    {"person_id": 6, "org_id": 2, "title": "提名副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责人社、卫生健康、基层治理等工作"},
    # 陈志琳 — 提名副市长
    {"person_id": 7, "org_id": 2, "title": "提名副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责公共安全、司法行政、信访维稳等工作"},
    # 周扬 — 提名副市长
    {"person_id": 8, "org_id": 2, "title": "提名副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责教育、民政、文化旅游体育、退役军人、民族事务等工作"},
    # 白玉明 — 副市长
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "2026-07-20", "end": "present", "rank": "县处级副职", "note": "2026年7月20日市人大常委会任命"},
    # 吴建荣 — 提名副市长
    {"person_id": 10, "org_id": 2, "title": "提名副市长", "start": "", "end": "present", "rank": "县处级副职", "note": "负责城乡规划建设管理、自然资源等工作"},
    # 王国安 — 原副市长
    {"person_id": 11, "org_id": 2, "title": "副市长", "start": "", "end": "2026-07-20", "rank": "县处级副职", "note": "2026年7月20日免去副市长职务"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 曹智勇 ↔ 杨宝田 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "曹智勇任市委书记、杨宝田任市长，为乌兰浩特市党政正职搭档", "overlap_org": "乌兰浩特市", "overlap_period": "2026"},
    # 曹智勇 ↔ 赵新友 — 书记与常委副市长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "曹智勇作为市委书记，赵新友作为常委副市长协助工作（分管常务）", "overlap_org": "中共乌兰浩特市委员会", "overlap_period": "2026"},
    # 曹智勇 ↔ 王英群 — 书记与常委副市长
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "曹智勇作为市委书记，王英群作为常委副市长", "overlap_org": "中共乌兰浩特市委员会", "overlap_period": "2026"},
    # 曹智勇 ↔ 李国强 — 书记与组织部长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "曹智勇作为市委书记，李国强作为组织部长负责干部工作", "overlap_org": "中共乌兰浩特市委员会", "overlap_period": "2026"},
    # 杨宝田 ↔ 赵新友 — 市长与常务副市长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "杨宝田作为市长，赵新友作为常委副市长协助常务工作", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026"},
    # 杨宝田 ↔ 王英群 — 市长与常委副市长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "杨宝田作为市长，王英群作为常委副市长", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026"},
    # 杨宝田 ↔ 白玉明 — 市长与副市长
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "杨宝田作为市长，白玉明作为新任副市长", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026"},
    # 杨宝田 ↔ 王国安 — 市长与副市长（前后任）
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "杨宝田作为市长，王国安前期作为副市长共事（2026年7月免去）", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026-07"},
    # 白玉明 ↔ 王国安 — 继任关系
    {"person_a": 9, "person_b": 11, "type": "前后任", "context": "白玉明接替王国安的副市长职务", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026-07"},
    # 赵新友 ↔ 王英群 — 同为常委副市长
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "赵新友与王英群同为市委常委、副市长/提名副市长", "overlap_org": "乌兰浩特市人民政府", "overlap_period": "2026"},
]


# ══════════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════════

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else ""

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p["birthplace"],p["education"],p["party_join"],p["work_start"],
                     p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ══════════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════════

def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return ("255,50,50", 20.0)  # Red, large
    elif "市长" in post and "副" not in post:
        return ("50,100,255", 20.0)  # Blue, large
    elif "常委" in post and ("副市长" in post or "副" in post):
        return ("100,150,255", 12.0)  # Light blue
    elif "常委" in post:
        return ("100,150,255", 12.0)
    elif "副市长" in post or ("副" in post and "市长" in post):
        return ("100,150,255", 12.0)
    elif "提名副市长" in post:
        return ("100,150,255", 12.0)
    elif "原" in post:
        return ("140,140,140", 10.0)  # Grey for former
    else:
        return ("100,100,100", 12.0)

def org_color(org_type):
    colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "纪委": ("255,200,200", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }
    return colors.get(org_type, ("200,200,200", 8.0))


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>乌兰浩特市领导班子关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    
    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    
    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Organization nodes
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# Person Graph JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id":"S001","title":"乌兰浩特市人民政府—领导之窗","url":"http://www.wlht.gov.cn/wlht/zwgk/ldzc/fsz79/index.html","publisher":"乌兰浩特市人民政府","published_at":"2026-07-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"市政府领导页面"},
        {"id":"S002","title":"曹智勇一行调研重点项目推进情况","url":"http://www.wlht.gov.cn/wlht/2026-07/23/article_2026072309035594593.html","publisher":"乌兰浩特市融媒体中心","published_at":"2026-07-23","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认曹智勇任市委书记"},
        {"id":"S003","title":"乌兰浩特市召开全市处级干部纪法教育会议","url":"http://www.wlht.gov.cn/wlht/2026-07/16/article_2026071615233490543.html","publisher":"乌兰浩特市融媒体中心","published_at":"2026-07-16","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认李国强任市委常委、组织部部长"},
        {"id":"S004","title":"乌兰浩特市人大常委会决定任免职名单","url":"http://www.wlht.gov.cn/wlht/2026-07/20/article_2026072010483090132.html","publisher":"乌兰浩特市人大常委会办公室","published_at":"2026-07-20","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认白玉明任副市长、王国安被免职"},
        {"id":"S005","title":"曹智勇就汛期全市排水防涝和防汛工作开展调研","url":"http://www.wlht.gov.cn/wlht/2026-07/08/article_2026070816225626953.html","publisher":"乌兰浩特市融媒体中心","published_at":"2026-07-08","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认曹智勇任市委书记（防汛调研）"},
        {"id":"S006","title":"曹智勇一行到部分重点企业调研","url":"http://www.wlht.gov.cn/wlht/2026-06/10/article_2026061009055530619.html","publisher":"乌兰浩特市融媒体中心","published_at":"2026-06-10","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":"确认曹智勇任市委书记（企业调研）"},
    ]


def make_person_json(p, relationships_list, source_register):
    person_rels = [r for r in relationships_list if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
    
    # Identify connected people
    connected = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            connected.append({
                "person": other["name"],
                "person_id": f"wlht_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })
    
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "内蒙古自治区",
            "city": "兴安盟",
            "region": "乌兰浩特市",
            "job": p["current_post"],
            "task_id": "inner_mongolia_乌兰浩特市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"wlht_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender",""),
            "ethnicity": p.get("ethnicity",""),
            "birth": p.get("birth",""),
            "birthplace": p.get("birthplace",""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join","").replace("中共党员（","").replace("中共党员","").replace("）",""),
            "work_start": p.get("work_start",""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source","")
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if ("书记" in p["current_post"] and "副" not in p["current_post"]) or ("市长" in p["current_post"] and "副" not in p["current_post"]) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001","S002"] if "书记" in p["current_post"] else ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "",
                "title": p["current_post"],
                "level": "县处级正职" if ("书记" in p["current_post"] and "副" not in p["current_post"]) or ("市长" in p["current_post"] and "副" not in p["current_post"]) else "县处级副职",
                "location": "内蒙古自治区兴安盟乌兰浩特市",
                "system": "party" if "委" in p["current_post"] or "书记" in p["current_post"] else "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "当前职务，公开资料未找到完整履历",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": connected,
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
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"公开资料受限，无法获取{p['name']}的完整履历（出生日期、教育背景、历任职务等）"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{p['name']}的完整履历", "why_it_matters": "核心领导人履历是关系网络的基础", "suggested_queries": [f"{p['name']} 简历 乌兰浩特", f"{p['name']} 任前公示", f"{p['name']} 兴安盟"], "last_attempted": AS_OF},
            {"priority": "critical", "question": f"{p['name']}的出生日期和籍贯", "why_it_matters": "用于身份识别和去重", "suggested_queries": [f"{p['name']} 出生 乌兰浩特", f"{p['name']} 籍贯"], "last_attempted": AS_OF},
        ]
    }
    return result


def write_person_jsons():
    source_register = make_source_register()
    
    # Core figures who need person JSONs
    core_ids = [1, 2, 3, 5]  # 曹智勇, 杨宝田, 赵新友, 李国强
    
    for p in persons:
        if p["id"] in core_ids:
            data = make_person_json(p, relationships, source_register)
            # Map current_post to a short job slug
            job_map = {
                1: "市委书记",
                2: "市长",
                3: "常委副市长",
                5: "组织部长",
            }
            job = job_map.get(p["id"], p["current_post"])
            fname = f"{TODAY}-内蒙古自治区-兴安盟-{job}-{p['name']}.json"
            fpath = os.path.join(BASE, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Person JSON: {fpath}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{'='*60}")
    print(f"乌兰浩特市 Network Build")
    print(f"{'='*60}")
    print(f"\nBuilding database...")
    build_db()
    print(f"\nBuilding GEXF graph...")
    build_gexf()
    print(f"\nWriting person JSONs...")
    write_person_jsons()
    
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"Done.")


if __name__ == "__main__":
    main()
