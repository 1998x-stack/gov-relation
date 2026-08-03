#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 呼玛县 (Huma County), 黑龙江省.

Investigation date: 2026-08-03
Task ID: heilongjiang_呼玛县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.huma.gov.cn/ (呼玛县人民政府官网) — official news and leadership writings
  - http://www.huma.gov.cn/huma/c100674/202607/c13_341085.shtml — 党政联席会议(张广海主持)
  - http://www.huma.gov.cn/huma/c100674/202606/c13_339532.shtml — 县委常委会(魏志民主持)
  - http://www.huma.gov.cn/huma/c100674/202604/c13_334139.shtml — 县委常委会(魏志民主持)
  - http://www.huma.gov.cn/huma/c100724/202607/c13_342172.shtml — 第十次常务会议(张广海)
  - http://www.huma.gov.cn/huma/c100724/202606/c13_339530.shtml — 第七次常务会议(张广海)
  - http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml — 政府办公室领导信息

Confidence notes:
  - 张广海 (县委书记/县长): confirmed via multiple official government articles (2026-06 to 2026-07)
  - 魏志民 (前任县委书记): confirmed via official news articles (2026-03 to 2026-05)
  - 高壮利 (政府办主任): confirmed via government office leadership page
  - Career histories for both leaders: unverified — only current/recent positions confirmed
  - Birth details, education, party join dates for most leaders: unverified
  - No leadership page (领导之窗) found on the website — may not be published or located at a different path
  - Exa search was rate-limited; Baidu returned CAPTCHA; Jina/Google/Bing timed out
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
SLUG = "呼玛县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

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
        "name": "张广海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记、县长",
        "current_org": "中共呼玛县委员会 / 呼玛县人民政府",
        "source": "http://www.huma.gov.cn/huma/c100674/202607/c13_341085.shtml"
    },
    {
        "id": 2,
        "name": "魏志民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共呼玛县委员会（前任）",
        "source": "http://www.huma.gov.cn/huma/c100674/202606/c13_339532.shtml"
    },
    # ═══════ 县政府办公室领导 ═══════
    {
        "id": 3,
        "name": "高壮利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "呼玛县人民政府办公室主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    # ═══════ 现有新闻报道中出现的关键人物 ═══════
    {
        "id": 4,
        "name": "白玉峰",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "计算机网络中心副主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 5,
        "name": "胡富菊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府办公室人员",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c100674/202607/c13_341085.shtml"
    },
    {
        "id": 6,
        "name": "陈琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年12月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "计算机网络中心主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 7,
        "name": "李钰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "呼玛县接待服务中心主任",
        "current_org": "呼玛县接待服务中心",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 8,
        "name": "李展",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "呼玛县人民政府办公室副主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 9,
        "name": "杨晓纯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年6月",
        "birthplace": "",
        "education": "大专",
        "party_join": "",
        "work_start": "",
        "current_post": "呼玛县人民政府办公室副主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 10,
        "name": "马笑野",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1989年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "呼玛县人民政府办公室副主任",
        "current_org": "呼玛县人民政府办公室",
        "source": "http://www.huma.gov.cn/huma/c102064/bm_jgsz.shtml"
    },
    {
        "id": 11,
        "name": "孟凡博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "编者",
        "current_org": "呼玛县政府办公室",
        "source": "http://www.huma.gov.cn/huma/c100724/202607/c13_342172.shtml"
    },
    {
        "id": 12,
        "name": "胡永泉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "编者",
        "current_org": "呼玛县政府办公室",
        "source": "http://www.huma.gov.cn/huma/c100724/202607/c13_342172.shtml"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共呼玛县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共大兴安岭地委",
        "location": "黑龙江省大兴安岭地区呼玛县"
    },
    {
        "id": 2,
        "name": "呼玛县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "大兴安岭地区行政公署",
        "location": "黑龙江省大兴安岭地区呼玛县"
    },
    {
        "id": 3,
        "name": "呼玛县人民政府办公室",
        "type": "政府",
        "level": "正科级",
        "parent": "呼玛县人民政府",
        "location": "黑龙江省大兴安岭地区呼玛县"
    },
    {
        "id": 4,
        "name": "呼玛县接待服务中心",
        "type": "事业单位",
        "level": "股级",
        "parent": "呼玛县人民政府办公室",
        "location": "黑龙江省大兴安岭地区呼玛县"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 张广海
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月起以县长身份主持召开政府常务会议；2026年7月起以县委书记、县长双重身份主持会议"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start": "2025?", "end": "present", "rank": "正处级", "note": "2026年5-6月以县长身份主持政府常务会议"},
    # 魏志民
    {"id": 3, "person_id": 2, "org_id": 1, "title": "县委书记", "start": "? ", "end": "2026-05", "rank": "正处级", "note": "2026年3月至5月主持县委常委会会议，5月底后未再出现"},
    # 高壮利
    {"id": 4, "person_id": 3, "org_id": 3, "title": "呼玛县人民政府办公室主任", "start": "?", "end": "present", "rank": "正科级", "note": "同时在多篇新闻稿件中以\"终审\"身份出现在编辑栏"},
    # 白玉峰
    {"id": 5, "person_id": 4, "org_id": 3, "title": "计算机网络中心副主任", "start": "?", "end": "present", "rank": "", "note": "复审编辑身份出现在政府新闻稿件中"},
    # 胡富菊
    {"id": 6, "person_id": 5, "org_id": 3, "title": "初审编辑", "start": "?", "end": "present", "rank": "", "note": "初审编辑出现在政府新闻稿件中"},
    # 陈琳
    {"id": 7, "person_id": 6, "org_id": 3, "title": "计算机网络中心主任", "start": "?", "end": "present", "rank": "", "note": ""},
    # 李钰
    {"id": 8, "person_id": 7, "org_id": 4, "title": "呼玛县接待服务中心主任", "start": "?", "end": "present", "rank": "", "note": ""},
    # 李展
    {"id": 9, "person_id": 8, "org_id": 3, "title": "呼玛县人民政府办公室副主任", "start": "?", "end": "present", "rank": "", "note": ""},
    # 杨晓纯
    {"id": 10, "person_id": 9, "org_id": 3, "title": "呼玛县人民政府办公室副主任", "start": "?", "end": "present", "rank": "", "note": ""},
    # 马笑野
    {"id": 11, "person_id": 10, "org_id": 3, "title": "呼玛县人民政府办公室副主任", "start": "?", "end": "present", "rank": "", "note": ""},
    # 孟凡博
    {"id": 12, "person_id": 11, "org_id": 3, "title": "编者", "start": "?", "end": "present", "rank": "", "note": ""},
    # 胡永泉
    {"id": 13, "person_id": 12, "org_id": 3, "title": "编者", "start": "?", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 张广海 — 魏志民：前后任(书记)
    {"id": 1, "person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "魏志民是前县委书记，张广海继任县委书记", "overlap_org": "中共呼玛县委员会", "overlap_period": "2026"},
    # 张广海 — 高壮利：上下级（县长—办公室主任）
    {"id": 2, "person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "张广海(县长/书记)与高壮利(县政府办主任)为上下级关系", "overlap_org": "呼玛县人民政府", "overlap_period": "2024-2026"},
    # 高壮利 — 白玉峰：同事（政府办）
    {"id": 3, "person_a": 3, "person_b": 4, "type": "overlap", "context": "同为政府办公室同事", "overlap_org": "呼玛县人民政府办公室", "overlap_period": "?"},
    # 高壮利 — 陈琳：同事
    {"id": 4, "person_a": 3, "person_b": 6, "type": "overlap", "context": "同为政府办公室同事", "overlap_org": "呼玛县人民政府办公室", "overlap_period": "?"},
    # 高壮利 — 李展：上下级
    {"id": 5, "person_a": 3, "person_b": 8, "type": "superior_subordinate", "context": "高壮利为政府办主任，李展为副主任", "overlap_org": "呼玛县人民政府办公室", "overlap_period": "?"},
    # 高壮利 — 杨晓纯：上下级
    {"id": 6, "person_a": 3, "person_b": 9, "type": "superior_subordinate", "context": "高壮利为政府办主任，杨晓纯为副主任", "overlap_org": "呼玛县人民政府办公室", "overlap_period": "?"},
    # 高壮利 — 马笑野：上下级
    {"id": 7, "person_a": 3, "person_b": 10, "type": "superior_subordinate", "context": "高壮利为政府办主任，马笑野为副主任", "overlap_org": "呼玛县人民政府办公室", "overlap_period": "?"},
]

# ── SQLite Setup ───────────────────────────────────────────────────────────
import sqlite3

os.makedirs(STAGING_DIR, exist_ok=True)

# Remove existing DB
if DB_PATH.exists():
    DB_PATH.unlink()

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
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT DEFAULT '',
        end TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
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

# Insert data
for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
         p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"])
    )

for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
    )

for pos in positions:
    cur.execute(
        "INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pos["id"], pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"])
    )

for r in relationships:
    cur.execute(
        "INSERT INTO relationships (id, person_a, person_b, type, context, overlap_org, overlap_period) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (r["id"], r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()

# ── GEXF Generation ────────────────────────────────────────────────────────
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return r,g,b string based on role."""
    post = p.get("current_post", "")
    if "书记" in post:
        return "255,50,50"
    elif "县长" in post:
        return "50,100,255"
    else:
        return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "事业" in t:
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    return any(kw in p.get("current_post", "") for kw in ("书记", "县长"))

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Research Agent - gov-relation</creator>')
lines.append('    <description>呼玛县领导班工作关系网络 - 黑龙江省大兴安岭地区</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Nodes: Organizations
for o in organizations:
    cid = f'o{o["id"]}'
    c = org_color(o)
    lines.append(f'      <node id="{cid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# person -> organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# person<->person (relationship)
for r in relationships:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ── Summary ────────────────────────────────────────────────────────────────
print(f"呼玛县 network build complete.")
print(f"  Database:        {DB_PATH} ({DB_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  GEXF:            {GEXF_PATH} ({GEXF_PATH.stat().st_size / 1024:.1f} KB)")
print(f"  Persons:         {len(persons)}")
print(f"  Organizations:   {len(organizations)}")
print(f"  Positions:       {len(positions)}")
print(f"  Relationships:   {len(relationships)}")
print()
print(f"Confidence notes:")
print(f"  - 张广海 (县委书记/县长): confirmed via official sources (2026-06 to 2026-07)")
print(f"  - 魏志民 (前县委书记): confirmed (2026-03 to 2026-05)")
print(f"  - 高壮利 (县政府办主任): confirmed via office leadership page")
print(f"  - Office staff bios: confirmed via official staff page")
print(f"  - Career histories: unverified — only current positions confirmed")
print(f"  - Leadership could not be found (no 领导之窗 page found)")
print(f"  - We search was severely degraded (Exa rate-limited, failed CAPTCHA, Jina timeouts)")