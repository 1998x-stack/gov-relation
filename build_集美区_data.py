#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 集美区 (Jimei District, Xiamen) leadership network.

集美区 — 厦门市所辖市辖区，位于厦门市几何中心，著名的文教区和侨乡。
厦门市为副省级城市，集美区为副省级城市辖区（副厅级或正处级建制）。

Research date: 2026-07-16
Sources:
- 集美区人民政府官方网站 (www.jimei.gov.cn) — leadership roster, confirmed
- Wikipedia (zh.wikipedia.org/wiki/集美区) — Party Secretary confirmed
- 厦门市人民政府网站

Coverage: 区委、区政府四套班子核心成员及关键副职。
Confidence notes:
- Core leadership (区委书记胡旭彬, 区长倪杰): confirmed from official website + Wikipedia
- 区人大常委会主任张剑鸣, 区政协主席蔡冬梅: confirmed from official website
- 常务副区长洪清岩及区委常委: confirmed from official website
- Career timeline details: partial, lacking early career for most figures
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_集美区")
DB_PATH = os.path.join(STAGING, "集美区_network.db")
GEXF_PATH = os.path.join(STAGING, "集美区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 胡旭彬 — 集美区委书记 (as of 2025/2026)
    {"id":1,"name":"胡旭彬","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委书记",
     "current_org":"中共集美区委",
     "source":"zh.wikipedia.org/wiki/集美区; www.jimei.gov.cn"},
    # 倪杰 — 集美区委副书记、区长 (as of 2026)
    {"id":2,"name":"倪杰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委副书记、区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn/xxgk/xxgk/F396/F1906/"},

    # ── 2. District People's Congress & Political Consultative Conference ──
    # 张剑鸣 — 集美区人大常委会主任
    {"id":3,"name":"张剑鸣","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 蔡冬梅 — 集美区政协主席
    {"id":4,"name":"蔡冬梅","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区政协主席",
     "current_org":"政协集美区委员会",
     "source":"www.jimei.gov.cn"},

    # ── 3. Key Deputy Leaders ──
    # 洪清岩 — 集美区委常委、常务副区长
    {"id":5,"name":"洪清岩","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委、常务副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 庄志辉 — 集美区委常委
    {"id":6,"name":"庄志辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 江彩蓉 — 集美区委常委
    {"id":7,"name":"江彩蓉","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 张云鹏 — 集美区委常委
    {"id":8,"name":"张云鹏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 马元富 — 集美区委常委
    {"id":9,"name":"马元富","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 吴宇鹏 — 集美区委常委
    {"id":10,"name":"吴宇鹏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 张清海 — 集美区委常委
    {"id":11,"name":"张清海","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},
    # 段林献 — 集美区委常委
    {"id":12,"name":"段林献","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区委常委",
     "current_org":"中共集美区委",
     "source":"www.jimei.gov.cn"},

    # ── 4. Deputy District Mayors ──
    # 李俊勇 — 集美区副区长
    {"id":13,"name":"李俊勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 曾胜军 — 集美区副区长
    {"id":14,"name":"曾胜军","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 郑彦 — 集美区副区长
    {"id":15,"name":"郑彦","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 方胜杰 — 集美区副区长
    {"id":16,"name":"方胜杰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 黄灵敏 — 集美区副区长
    {"id":17,"name":"黄灵敏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},
    # 徐墩煌 — 集美区副区长
    {"id":18,"name":"徐墩煌","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区副区长",
     "current_org":"集美区人民政府",
     "source":"www.jimei.gov.cn"},

    # ── 5. Deputy NPC & CPPCC ──
    # 陈泽昭 — 区人大常委会副主任
    {"id":19,"name":"陈泽昭","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会副主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 黄金喜 — 区人大常委会副主任
    {"id":20,"name":"黄金喜","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会副主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 黄大阳 — 区人大常委会副主任
    {"id":21,"name":"黄大阳","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会副主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 李江平 — 区人大常委会副主任
    {"id":22,"name":"李江平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会副主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 蔡爱兰 — 区人大常委会副主任
    {"id":23,"name":"蔡爱兰","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"集美区人大常委会副主任",
     "current_org":"集美区人大常委会",
     "source":"www.jimei.gov.cn"},
    # 黄云茜 — 区政协副主席
    {"id":24,"name":"黄云茜","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区政协副主席",
     "current_org":"政协集美区委员会",
     "source":"www.jimei.gov.cn"},
    # 蔡路鹏 — 区政协副主席
    {"id":25,"name":"蔡路鹏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区政协副主席",
     "current_org":"政协集美区委员会",
     "source":"www.jimei.gov.cn"},
    # 李梅 — 区政协副主席
    {"id":26,"name":"李梅","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区政协副主席",
     "current_org":"政协集美区委员会",
     "source":"www.jimei.gov.cn"},
    # 李福川 — 区政协副主席
    {"id":27,"name":"李福川","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区政协副主席",
     "current_org":"政协集美区委员会",
     "source":"www.jimei.gov.cn"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共集美区委","type":"党委","level":"副厅级","parent":"中共厦门市委","location":"厦门市集美区"},
    {"id":2,"name":"集美区人民政府","type":"政府","level":"副厅级","parent":"厦门市人民政府","location":"厦门市集美区"},
    {"id":3,"name":"集美区人大常委会","type":"人大","level":"副厅级","parent":"","location":"厦门市集美区"},
    {"id":4,"name":"政协集美区委员会","type":"政协","level":"副厅级","parent":"","location":"厦门市集美区"},
    {"id":5,"name":"中共集美区纪律检查委员会","type":"纪委","level":"正处级","parent":"中共集美区委","location":"厦门市集美区"},
    {"id":6,"name":"集美区监察委员会","type":"纪委","level":"正处级","parent":"","location":"厦门市集美区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # Current top leaders
    {"person_id":1,"org_id":1,"title":"集美区委书记","start":"","end":"","rank":"副厅级","note":"现任，信息来源：官方政府网站及维基百科"},
    {"person_id":2,"org_id":1,"title":"集美区委副书记","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":2,"org_id":2,"title":"集美区区长","start":"","end":"","rank":"副厅级","note":"现任"},

    # NPC & CPPCC
    {"person_id":3,"org_id":3,"title":"集美区人大常委会主任","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":4,"org_id":4,"title":"集美区政协主席","start":"","end":"","rank":"副厅级","note":"现任"},

    # Standing Committee
    {"person_id":5,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":5,"org_id":2,"title":"集美区常务副区长","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":6,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":7,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":8,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":9,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":10,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":11,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},
    {"person_id":12,"org_id":1,"title":"集美区委常委","start":"","end":"","rank":"副厅级","note":"现任"},

    # Deputy Mayors
    {"person_id":13,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":14,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":15,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":16,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":17,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":18,"org_id":2,"title":"集美区副区长","start":"","end":"","rank":"正处级","note":"现任"},

    # NPC Deputy Chairs
    {"person_id":19,"org_id":3,"title":"集美区人大常委会副主任","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":20,"org_id":3,"title":"集美区人大常委会副主任","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":21,"org_id":3,"title":"集美区人大常委会副主任","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":22,"org_id":3,"title":"集美区人大常委会副主任","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":23,"org_id":3,"title":"集美区人大常委会副主任","start":"","end":"","rank":"正处级","note":"现任"},

    # CPPCC Deputy Chairs
    {"person_id":24,"org_id":4,"title":"集美区政协副主席","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":25,"org_id":4,"title":"集美区政协副主席","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":26,"org_id":4,"title":"集美区政协副主席","start":"","end":"","rank":"正处级","note":"现任"},
    {"person_id":27,"org_id":4,"title":"集美区政协副主席","start":"","end":"","rank":"正处级","note":"现任"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core working relationships
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"胡旭彬（区委书记）与倪杰（区长）党政搭档","overlap_org":"中共集美区委/集美区人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":3,"type":"党政同僚","context":"区委书记与人大主任","overlap_org":"集美区","overlap_period":"现任"},
    {"person_a":1,"person_b":4,"type":"党政同僚","context":"区委书记与政协主席","overlap_org":"集美区","overlap_period":"现任"},

    # Leadership pairs — 区委书记 with standing committee
    {"person_a":1,"person_b":5,"type":"上下级","context":"区委书记与常务副区长","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":6,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":7,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":8,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":9,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":10,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":11,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},
    {"person_a":1,"person_b":12,"type":"上下级","context":"区委书记与区委常委","overlap_org":"中共集美区委","overlap_period":"现任"},

    # 区长 with deputies
    {"person_a":2,"person_b":5,"type":"上下级","context":"区长与常务副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":13,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":14,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":15,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":16,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":17,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},
    {"person_a":2,"person_b":18,"type":"上下级","context":"区长与副区长","overlap_org":"集美区人民政府","overlap_period":"现任"},

    # 人大与政协
    {"person_a":3,"person_b":19,"type":"同级同僚","context":"人大主任与副主任","overlap_org":"集美区人大常委会","overlap_period":"现任"},
    {"person_a":3,"person_b":20,"type":"同级同僚","context":"人大主任与副主任","overlap_org":"集美区人大常委会","overlap_period":"现任"},
    {"person_a":3,"person_b":21,"type":"同级同僚","context":"人大主任与副主任","overlap_org":"集美区人大常委会","overlap_period":"现任"},
    {"person_a":3,"person_b":22,"type":"同级同僚","context":"人大主任与副主任","overlap_org":"集美区人大常委会","overlap_period":"现任"},
    {"person_a":3,"person_b":23,"type":"同级同僚","context":"人大主任与副主任","overlap_org":"集美区人大常委会","overlap_period":"现任"},
    {"person_a":4,"person_b":24,"type":"同级同僚","context":"政协主席与副主席","overlap_org":"政协集美区委员会","overlap_period":"现任"},
    {"person_a":4,"person_b":25,"type":"同级同僚","context":"政协主席与副主席","overlap_org":"政协集美区委员会","overlap_period":"现任"},
    {"person_a":4,"person_b":26,"type":"同级同僚","context":"政协主席与副主席","overlap_org":"政协集美区委员会","overlap_period":"现任"},
    {"person_a":4,"person_b":27,"type":"同级同僚","context":"政协主席与副主席","overlap_org":"政协集美区委员会","overlap_period":"现任"},
]

# =========================================================================
# BUILD DATABASE
# =========================================================================
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for po in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                (po["person_id"], po["org_id"], po["title"], po["start"], po["end"], po["rank"], po["note"]))

for r in relationships:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Print summary
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

print(f"✅ Database created: {DB_PATH}")
print(f"   Persons: {person_count} | Orgs: {org_count} | Positions: {pos_count} | Relationships: {rel_count}")

# =========================================================================
# BUILD GEXF
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def color_for_role(title):
    t = title or ""
    if "书记" in t and "副" not in t and "纪委" not in t:
        return (255,50,50)   # Red for Party Secretary
    if "区长" in t and "副" not in t:
        return (50,100,255)  # Blue for District Mayor
    if "人大主任" in t:
        return (200,100,100) # Darker for People's Congress
    if "政协主席" in t:
        return (100,100,200) # Purple for CPPCC
    if "纪委" in t or "纪检" in t:
        return (255,165,0)   # Orange for discipline
    if "副" in t and ("区长" in t or "县长" in t or "市长" in t):
        return (100,150,255) # Lighter blue for deputy government
    if "常委" in t:
        return (150,100,100) # Brown-red for Standing Committee
    if "人大" in t:
        return (200,150,150)
    if "政协" in t:
        return (150,150,200)
    return (100,100,100)

def person_size(p):
    t = p.get("current_post","") or ""
    if ("书记" in t and "副" not in t and "纪委" not in t) or ("区长" in t and "副" not in t):
        return "20.0"
    if "常委" in t or "主任" in t or "主席" in t:
        return "15.0"
    return "12.0"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>集美区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attribute declarations
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="org" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="birthplace" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    pid = f"jm_{p['id']}"
    c = color_for_role(p.get("current_post",""))
    sz = person_size(p)
    label = esc(f"{p['name']} ({p.get('current_post','?')})")
    lines.append(f'      <node id="{pid}" label="{label}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p.get("birthplace",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# Organization nodes
org_colors = {
    "党委": (255,200,200), "政府": (200,200,255),
    "人大": (200,255,255), "政协": (255,240,200),
    "纪委": (255,220,180), "default": (200,200,200)
}
for o in organizations:
    oid = f"jm_org_{o['id']}"
    oc = org_colors.get(o["type"], org_colors["default"])
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges: person→organization (worked_at)
lines.append('    <edges>')
edge_id = 0
for po in positions:
    p = next(x for x in persons if x["id"] == po["person_id"])
    o = next(x for x in organizations if x["id"] == po["org_id"])
    edge_id += 1
    label = esc(f"{p['name']} → {o['name']} ({po['title']})")
    lines.append(f'      <edge id="e{edge_id}" source="jm_{p["id"]}" target="jm_org_{o["id"]}" label="{label}" weight="1.0">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po.get("title",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

# Edges: person↔person (relationship)
for r in relationships:
    if r["person_a"] == r["person_b"]:
        continue
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    context = esc(r.get("context",""))
    lines.append(f'      <edge id="e{edge_id}" source="jm_{p_a["id"]}" target="jm_{p_b["id"]}" label="{context}" weight="2.0">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{context}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ GEXF created: {GEXF_PATH}")
print(f"   Nodes: {len(persons) + len(organizations)} | Edges: {edge_id}")

conn.close()
print("✅ Done!")
