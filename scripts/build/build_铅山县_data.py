#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 铅山县 (Yanshan County) leadership network.

上饶市铅山县 - county-level administrative division of Shangrao City, Jiangxi Province.

Targets: 县委书记 & 县长

Current leadership (as of 2026-07):
- 县委书记: 待核实 — Chinese government websites and Baidu Baike unreachable from this environment
- 县长: 待核实 — Same access restrictions
- Predecessors: 待核实

Sources:
- Env limitation: www.ysx.gov.cn (铅山县政府), baike.baidu.com, zh.wikipedia.org all unreachable
- Parent city data confirmed from shangrao_network.db

Research date: 2026-07-15
"""

import sqlite3, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = BASE_DIR  # we're already in the staging dir
DB_PATH = os.path.join(STAGING_DIR, "铅山县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "铅山县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current top leaders (姓名待核实) ──
    {
        "id": 1, "name": "（待核实）铅山县委书记",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "铅山县委书记", "current_org": "中共铅山县委员会",
        "source": "待核实 — ysx.gov.cn 不可达, 需通过上饶市委组织部任前公示或铅山县政府官网领导之窗核实"
    },
    {
        "id": 2, "name": "（待核实）铅山县县长",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "铅山县委副书记、县长", "current_org": "铅山县人民政府",
        "source": "待核实 — 同上"
    },

    # ── Predecessors (known from historical data) ──
    # 危岩 — known former 铅山县委书记 from Baidu Baike (historical)
    {
        "id": 3, "name": "危岩",
        "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "（待核实）原铅山县委书记", "current_org": "（待核实）",
        "source": "历史资料 — 危岩曾长期在铅山县任职，曾任铅山县长、县委书记。具体任期起止和当前去向待核实。来源: baike.baidu.com (不可达)"
    },
    # 未小刚 — known former/likely current 铅山县长 from historical data
    {
        "id": 4, "name": "未小刚",
        "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
        "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "（待核实）原铅山县长", "current_org": "（待核实）",
        "source": "历史资料 — 未小刚曾任铅山县长。任期起止和当前去向待核实。来源: baike.baidu.com (不可达)"
    },

    # ── 铅山籍知名人士 (connections) ──
    {
        "id": 5, "name": "曾衍敏",
        "gender": "男", "ethnicity": "汉族", "birth": "1976-08", "birthplace": "江西铅山",
        "education": "省委党校在职研究生学历", "party_join": "中共党员", "work_start": "1996-07",
        "current_post": "原莲花县委副书记、县长（卸任，去向待查）", "current_org": "莲花县人民政府",
        "source": "build_莲花县_data.py — 曾衍敏1976年8月生，江西铅山人，曾任莲花县长（2021.08-2026.02）"
    },

    # ── 上饶市领导 (parent city) ──
    {
        "id": 6, "name": "刘烁",
        "gender": "男", "ethnicity": "汉族", "birth": "1970-02", "birthplace": "山东诸城",
        "education": "南开大学化学系化学专业+企业管理专业双学士", "party_join": "1991-02", "work_start": "1992-07",
        "current_post": "上饶市委书记", "current_org": "中共上饶市委员会",
        "source": "shangrao_network.db — shangrao_network.gexf from this project"
    },
    {
        "id": 7, "name": "李建涛",
        "gender": "男", "ethnicity": "汉族", "birth": "1977-05", "birthplace": "河南方城",
        "education": "研究生学历，理学博士", "party_join": "中共党员", "work_start": "",
        "current_post": "上饶市委副书记、市长", "current_org": "上饶市人民政府",
        "source": "shangrao_network.db — 2025年9月从上饶市长，跨省交流干部"
    },
]


# ═══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════

organizations = [
    # ── 铅山县 ──
    {"id": 1, "name": "中共铅山县委员会", "type": "党委", "level": "县级",
     "parent": "中共上饶市委员会", "location": "江西省上饶市铅山县"},
    {"id": 2, "name": "铅山县人民政府", "type": "政府", "level": "县级",
     "parent": "上饶市人民政府", "location": "江西省上饶市铅山县"},
    {"id": 3, "name": "铅山县人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "上饶市人大常委会", "location": "江西省上饶市铅山县"},
    {"id": 4, "name": "政协铅山县委员会", "type": "政协", "level": "县级",
     "parent": "政协上饶市委员会", "location": "江西省上饶市铅山县"},
    {"id": 5, "name": "铅山县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共铅山县委员会", "location": "江西省上饶市铅山县"},
    {"id": 6, "name": "中共铅山县委政法委员会", "type": "党委", "level": "县级",
     "parent": "中共铅山县委员会", "location": "江西省上饶市铅山县"},
    {"id": 7, "name": "中共铅山县委组织部", "type": "党委", "level": "县级",
     "parent": "中共铅山县委员会", "location": "江西省上饶市铅山县"},
    {"id": 8, "name": "中共铅山县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共铅山县委员会", "location": "江西省上饶市铅山县"},
    {"id": 9, "name": "中共铅山县委统战部", "type": "党委", "level": "县级",
     "parent": "中共铅山县委员会", "location": "江西省上饶市铅山县"},
    {"id": 10, "name": "铅山县人民武装部", "type": "军队", "level": "县级",
     "parent": "上饶军分区", "location": "江西省上饶市铅山县"},

    # ── 上饶市 (parent city) ──
    {"id": 11, "name": "中共上饶市委员会", "type": "党委", "level": "地级",
     "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 12, "name": "上饶市人民政府", "type": "政府", "level": "地级",
     "parent": "江西省人民政府", "location": "江西省上饶市"},
    {"id": 13, "name": "上饶市人大常委会", "type": "人大", "level": "地级",
     "parent": "江西省人大常委会", "location": "江西省上饶市"},
    {"id": 14, "name": "政协上饶市委员会", "type": "政协", "level": "地级",
     "parent": "政协江西省委员会", "location": "江西省上饶市"},

    # ── 莲花县 (曾衍敏关联) ──
    {"id": 15, "name": "莲花县人民政府", "type": "政府", "level": "县级",
     "parent": "萍乡市人民政府", "location": "江西省萍乡市莲花县"},
    {"id": 16, "name": "中共莲花县委员会", "type": "党委", "level": "县级",
     "parent": "中共萍乡市委员会", "location": "江西省萍乡市莲花县"},
]


# ═══════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════

positions = [
    # 铅山县委书记 (1) - 姓名待核实
    {"id": 1, "person_id": 1, "org_id": 1, "title": "铅山县委书记",
     "start": "", "end": "", "rank": "正处级",
     "note": "姓名待核实。需访问 ysx.gov.cn 领导之窗或上饶市委组织部任前公示"},

    # 铅山县县长 (2) - 姓名待核实
    {"id": 2, "person_id": 2, "org_id": 2, "title": "铅山县委副书记、县长",
     "start": "", "end": "", "rank": "正处级",
     "note": "姓名待核实。同上"},

    # 危岩 (3) - 前任书记
    {"id": 3, "person_id": 3, "org_id": 1, "title": "铅山县委书记（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "历史任职，起止时间待核实。危岩曾长期在铅山工作"},

    # 未小刚 (4) - 前任县长
    {"id": 4, "person_id": 4, "org_id": 2, "title": "铅山县委副书记、县长（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "历史任职，起止时间待核实"},

    # 曾衍敏 (5) - 铅山籍
    {"id": 5, "person_id": 5, "org_id": 15, "title": "莲花县委副书记、县长",
     "start": "2021-08", "end": "2026-02", "rank": "正处级",
     "note": "曾衍敏，江西铅山人，1976-08出生。2021年8月至2026年2月任莲花县长"},
    {"id": 6, "person_id": 5, "org_id": 16, "title": "莲花县委副书记",
     "start": "2021-08", "end": "2026-02", "rank": "副处级",
     "note": "兼任县委副书记"},

    # 刘烁 (6) - 上饶市委书记
    {"id": 7, "person_id": 6, "org_id": 11, "title": "上饶市委书记",
     "start": "2026-05", "end": "", "rank": "正厅级",
     "note": "2026年5月6日从萍乡调任"},

    # 李建涛 (7) - 上饶市长
    {"id": 8, "person_id": 7, "org_id": 12, "title": "上饶市委副书记、市长",
     "start": "2025-09", "end": "", "rank": "正厅级",
     "note": "2025年7月任代市长，9月26日当选市长；跨省交流干部(河南→江西)"},
]


# ═══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════

relationships = [
    # 铅山县与上饶市 — 隶属关系
    {"id": 1, "person_a": 6, "person_b": 1, "type": "上下级",
     "context": "刘烁（上饶市委书记）与铅山县委书记为上下级关系",
     "overlap_org": "上饶市", "overlap_period": "至今"},

    # 曾衍敏 — 铅山籍人士与家乡的关系
    {"id": 2, "person_a": 5, "person_b": 1, "type": "同籍",
     "context": "曾衍敏（莲花县原县长）为铅山籍人，与现任铅山县委书记可能有同乡/系统关联",
     "overlap_org": "铅山县", "overlap_period": ""},

    # 党政搭档 (待核实)
    {"id": 3, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "铅山县委书记与县长为县党政一把手（姓名均待核实）",
     "overlap_org": "铅山县", "overlap_period": "至今"},

    # 危岩 → 现任书记 (前后任)
    {"id": 4, "person_a": 3, "person_b": 1, "type": "职务接替",
     "context": "危岩（原书记）→ （待核实现任）接任铅山县委书记。起止时间待核实",
     "overlap_org": "铅山县委", "overlap_period": "不重叠（前后任）"},

    # 未小刚 → 现任县长 (前后任)
    {"id": 5, "person_a": 4, "person_b": 2, "type": "职务接替",
     "context": "未小刚（原县长）→ （待核实现任）接任铅山县长。起止时间待核实",
     "overlap_org": "铅山县政府", "overlap_period": "不重叠（前后任）"},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD SQLITE
# ═══════════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
    birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"],
               p["work_start"], p["current_post"], p["current_org"], p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")


# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "县委书记" in post and "纪委" not in post: return "255,50,50"
    elif "县长" in post or "副县长" in post: return "50,100,255"
    elif "纪委书记" in post or "监委" in post: return "255,165,0"
    elif "政法委" in post: return "150,100,200"
    elif "宣传部" in post: return "100,200,150"
    elif "组织部" in post: return "200,150,100"
    elif "统战部" in post: return "200,100,150"
    elif "人武部" in post: return "100,150,100"
    elif "人大" in post: return "100,200,200"
    elif "政协" in post: return "200,200,100"
    return "100,100,100"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
            "政协":"255,240,200","群团":"255,220,255","事业单位":"220,220,220",
            "开发区":"200,255,200","国企":"255,255,200","军队":"180,180,200"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>上饶市铅山县领导班子工作关系网络 — 2026年7月15日生成（注：核心领导姓名待核实，因中国境内网站不可达）</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid, atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid, atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    post = p.get("current_post","")
    if "县委书记" in post and "纪委" not in post:
        sz = "20.0"
    elif "县长" in post and "代县长" in post:
        sz = "20.0"
    elif "副县长" in post:
        sz = "14.0"
    elif "常委" in post or "副书记" in post:
        sz = "12.0"
    elif "人大" in post or "政协" in post:
        sz = "12.0"
    else:
        sz = "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),
                ("3",p.get("current_post","")),("4","person"),("5","")]:
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
    lines.append('        <viz:size value="8.0"/>')
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
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
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
print("\nDone! ⚠️ Note: Core leaders (id=1,2) have placeholder names — real names must be filled when Chinese websites become accessible.")
