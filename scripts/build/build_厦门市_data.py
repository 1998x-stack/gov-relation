#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 厦门市 (Xiamen City, Fujian) leadership network.

厦门市 — 副省级城市, 中国最早开放的经济特区之一.

Research date: 2026-07-16
Sources:
- Wikipedia (zh.wikipedia.org/wiki/厦门市) — current leadership table
- Wikipedia (en.wikipedia.org/wiki/Cui_Yonghui) — predecessor biography
- Fujian Provincial Government official website (www.fujian.gov.cn)
- Baidu Baike (partial, geo-restricted access)

Coverage: City-level four major organs (市委、市人大、市政府、市政协),
district-level leaders (6 districts), and predecessor/successor chains.

Confidence notes:
- Core leadership (Party Secretary, Mayor) identity: confirmed from Wikipedia
- Career timeline details for top figures: based on Wikipedia, plausible
- District-level leaders: largely unverified (no direct access to official pages)
- Early career and education details: partial, flagged as open questions
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_厦门市")
DB_PATH = os.path.join(STAGING, "厦门市_network.db")
GEXF_PATH = os.path.join(STAGING, "厦门市_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current city-level top leaders ──
    # 林涛 — 厦门市委书记 (as of 2026.04)
    {"id":1,"name":"林涛","gender":"男","ethnicity":"汉族",
     "birth":"1971-07","birthplace":"广东揭阳","education":"未详",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"厦门市委书记",
     "current_org":"中共厦门市委",
     "source":"zh.wikipedia.org/wiki/厦门市"},
    # 伍斌 — 厦门市市长 (as of 2024.09)
    {"id":2,"name":"伍斌","gender":"男","ethnicity":"汉族",
     "birth":"1967-09","birthplace":"福建泰宁","education":"未详",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"厦门市人民政府市长",
     "current_org":"厦门市人民政府",
     "source":"zh.wikipedia.org/wiki/厦门市"},
    # 杨国豪 — 厦门市人大常委会主任 (as of 2022.01)
    {"id":3,"name":"杨国豪","gender":"男","ethnicity":"汉族",
     "birth":"1963-05","birthplace":"福建莆田","education":"未详",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"厦门市人大常委会主任",
     "current_org":"厦门市人大常委会",
     "source":"zh.wikipedia.org/wiki/厦门市"},
    # 张国旺 — 厦门市政协主席 (as of 2025.01)
    {"id":4,"name":"张国旺","gender":"男","ethnicity":"汉族",
     "birth":"1964-10","birthplace":"福建建瓯","education":"未详",
     "party_join":"中共党员","work_start":"未详",
     "current_post":"厦门市政协主席",
     "current_org":"政协厦门市委员会",
     "source":"zh.wikipedia.org/wiki/厦门市"},

    # ── 2. Predecessors — 市委书记 ──
    # 崔永辉 — 原厦门市委书记 (2021.10-2026.04)
    {"id":5,"name":"崔永辉","gender":"男","ethnicity":"汉族",
     "birth":"1970-11","birthplace":"湖北恩施","education":"华中师范大学政治教育专业",
     "party_join":"中共党员","work_start":"1991",
     "current_post":"（原厦门市委书记）",
     "current_org":"",
     "source":"en.wikipedia.org/wiki/Cui_Yonghui"},
    # 赵龙 — 原厦门市委书记 (2020-2021), 现福建省省长 (the predecessor of Cui)
    {"id":6,"name":"赵龙","gender":"男","ethnicity":"汉族",
     "birth":"1967-09","birthplace":"辽宁盘锦","education":"中国人民大学土地管理系",
     "party_join":"1988-12","work_start":"1989-07",
     "current_post":"福建省省长（原厦门市委书记）",
     "current_org":"福建省人民政府",
     "source":"福建省_network.db (existing artifacts)"},

    # ── 3. Predecessors — 市长 ──
    # 黄文辉 — 原厦门市长 (2021-2024)
    {"id":7,"name":"黄文辉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原厦门市人民政府市长）",
     "current_org":"",
     "source":"zh.wikipedia.org/wiki/厦门市"},
    # 庄稼汉 — 原厦门市长 (2016-2020)
    {"id":8,"name":"庄稼汉","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原厦门市人民政府市长）",
     "current_org":"",
     "source":"公开报道"},
    # 裴金佳 — 原厦门市长(2015-2016)、后任市委书记(2016-2020)
    {"id":9,"name":"裴金佳","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原厦门市委书记、市长）",
     "current_org":"",
     "source":"公开报道"},

    # ── 4. Key deputy leaders (市委常委会) — partial, need verification ──
    # Note: The following are based on limited public sources
    # 常务副市长 — unverified name
    {"id":10,"name":"（常务副市长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、常务副市长（待确认）",
     "current_org":"厦门市人民政府",
     "source":"待确认"},
    # 市纪委书记 — unverified name
    {"id":11,"name":"（市纪委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、市纪委书记（待确认）",
     "current_org":"中共厦门市纪律检查委员会",
     "source":"待确认"},
    # 组织部部长 — unverified name
    {"id":12,"name":"（组织部部长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、组织部部长（待确认）",
     "current_org":"中共厦门市委组织部",
     "source":"待确认"},
    # 宣传部部长 — unverified name
    {"id":13,"name":"（宣传部部长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、宣传部部长（待确认）",
     "current_org":"中共厦门市委宣传部",
     "source":"待确认"},
    # 政法委书记 — unverified name
    {"id":14,"name":"（政法委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、政法委书记（待确认）",
     "current_org":"中共厦门市委政法委员会",
     "source":"待确认"},
    # 秘书长 — unverified name
    {"id":15,"name":"（市委秘书长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、秘书长（待确认）",
     "current_org":"中共厦门市委",
     "source":"待确认"},
    # 统战部部长 — unverified name
    {"id":16,"name":"（统战部部长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"厦门市委常委、统战部部长（待确认）",
     "current_org":"中共厦门市委统一战线工作部",
     "source":"待确认"},

    # ── 5. District-level top leaders (6 districts) ──
    # Most district-level names are placeholders pending verification
    # 思明区
    {"id":17,"name":"（思明区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"思明区委书记（待确认）",
     "current_org":"中共思明区委",
     "source":"待确认"},
    {"id":18,"name":"（思明区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"思明区区长（待确认）",
     "current_org":"思明区人民政府",
     "source":"待确认"},
    # 湖里区
    {"id":19,"name":"（湖里区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"湖里区委书记（待确认）",
     "current_org":"中共湖里区委",
     "source":"待确认"},
    {"id":20,"name":"（湖里区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"湖里区区长（待确认）",
     "current_org":"湖里区人民政府",
     "source":"待确认"},
    # 集美区
    {"id":21,"name":"（集美区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区委书记（待确认）",
     "current_org":"中共集美区委",
     "source":"待确认"},
    {"id":22,"name":"（集美区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"集美区区长（待确认）",
     "current_org":"集美区人民政府",
     "source":"待确认"},
    # 海沧区
    {"id":23,"name":"（海沧区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"海沧区委书记（待确认）",
     "current_org":"中共海沧区委",
     "source":"待确认"},
    {"id":24,"name":"（海沧区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"海沧区区长（待确认）",
     "current_org":"海沧区人民政府",
     "source":"待确认"},
    # 同安区
    {"id":25,"name":"（同安区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"同安区委书记（待确认）",
     "current_org":"中共同安区委",
     "source":"待确认"},
    {"id":26,"name":"（同安区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"同安区区长（待确认）",
     "current_org":"同安区人民政府",
     "source":"待确认"},
    # 翔安区
    {"id":27,"name":"（翔安区委书记）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"翔安区委书记（待确认）",
     "current_org":"中共翔安区委",
     "source":"待确认"},
    {"id":28,"name":"（翔安区长）","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"翔安区区长（待确认）",
     "current_org":"翔安区人民政府",
     "source":"待确认"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # City-level core organs
    {"id":1,"name":"中共厦门市委","type":"党委","level":"副省级","parent":"中共福建省委","location":"厦门市思明区"},
    {"id":2,"name":"厦门市人民政府","type":"政府","level":"副省级","parent":"福建省人民政府","location":"厦门市思明区"},
    {"id":3,"name":"厦门市人大常委会","type":"人大","level":"副省级","parent":"","location":"厦门市思明区"},
    {"id":4,"name":"政协厦门市委员会","type":"政协","level":"副省级","parent":"","location":"厦门市思明区"},
    {"id":5,"name":"中共厦门市纪律检查委员会","type":"纪委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},
    {"id":6,"name":"中共厦门市委组织部","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},
    {"id":7,"name":"中共厦门市委宣传部","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},
    {"id":8,"name":"中共厦门市委政法委员会","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},
    {"id":9,"name":"中共厦门市委统一战线工作部","type":"党委","level":"副省级","parent":"中共厦门市委","location":"厦门市思明区"},

    # Higher-level parent orgs
    {"id":10,"name":"中共福建省委","type":"党委","level":"省级","parent":"","location":"福建省福州市"},
    {"id":11,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},

    # District-level organs
    {"id":12,"name":"中共思明区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"思明区"},
    {"id":13,"name":"思明区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"思明区"},
    {"id":14,"name":"中共湖里区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"湖里区"},
    {"id":15,"name":"湖里区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"湖里区"},
    {"id":16,"name":"中共集美区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"集美区"},
    {"id":17,"name":"集美区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"集美区"},
    {"id":18,"name":"中共海沧区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"海沧区"},
    {"id":19,"name":"海沧区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"海沧区"},
    {"id":20,"name":"中共同安区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"同安区"},
    {"id":21,"name":"同安区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"同安区"},
    {"id":22,"name":"中共翔安区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"翔安区"},
    {"id":23,"name":"翔安区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"翔安区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # City-level top leaders
    {"person_id":1,"org_id":1,"title":"厦门市委书记","start":"2026-04","end":"","rank":"副部","note":"现任"},
    {"person_id":2,"org_id":2,"title":"厦门市人民政府市长","start":"2024-09","end":"","rank":"副部","note":"现任"},
    {"person_id":3,"org_id":3,"title":"厦门市人大常委会主任","start":"2022-01","end":"","rank":"副部","note":"现任"},
    {"person_id":4,"org_id":4,"title":"厦门市政协主席","start":"2025-01","end":"","rank":"副部","note":"现任"},

    # Predecessors — Party Secretary
    {"person_id":5,"org_id":1,"title":"厦门市委书记","start":"2021-10","end":"2026-04","rank":"副部","note":"前任书记，调离"},
    {"person_id":5,"org_id":10,"title":"福建省委常委、省委秘书长","start":"2021-06","end":"2021-10","rank":"副部","note":"调任厦门前职务"},
    {"person_id":6,"org_id":1,"title":"厦门市委书记","start":"2020","end":"2021-09","rank":"副部","note":"前任书记，升任福建省省长"},
    {"person_id":6,"org_id":11,"title":"福建省省长","start":"2021-10","end":"","rank":"正部","note":"现任福建省省长"},
    {"person_id":9,"org_id":1,"title":"厦门市委书记","start":"2016-09","end":"2020","rank":"副部","note":"前任书记"},

    # Predecessors — Mayor
    {"person_id":7,"org_id":2,"title":"厦门市人民政府市长","start":"2021","end":"2024-09","rank":"副部","note":"前任市长"},
    {"person_id":8,"org_id":2,"title":"厦门市人民政府市长","start":"2016","end":"2020","rank":"副部","note":"前任市长"},
    {"person_id":9,"org_id":2,"title":"厦门市人民政府市长","start":"2015","end":"2016-09","rank":"副部","note":"前任市长，后任市委书记"},

    # Standing Committee — placeholder positions (unverified names)
    {"person_id":10,"org_id":2,"title":"厦门市委常委、常务副市长","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":11,"org_id":5,"title":"厦门市委常委、市纪委书记","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":12,"org_id":6,"title":"厦门市委常委、组织部部长","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":13,"org_id":7,"title":"厦门市委常委、宣传部部长","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":14,"org_id":8,"title":"厦门市委常委、政法委书记","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":15,"org_id":1,"title":"厦门市委常委、秘书长","start":"","end":"","rank":"正厅","note":"待确认"},
    {"person_id":16,"org_id":9,"title":"厦门市委常委、统战部部长","start":"","end":"","rank":"正厅","note":"待确认"},

    # District-level — placeholder positions
    {"person_id":17,"org_id":12,"title":"思明区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":18,"org_id":13,"title":"思明区区长","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":19,"org_id":14,"title":"湖里区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":20,"org_id":15,"title":"湖里区区长","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":21,"org_id":16,"title":"集美区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":22,"org_id":17,"title":"集美区区长","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":23,"org_id":18,"title":"海沧区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":24,"org_id":19,"title":"海沧区区长","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":25,"org_id":20,"title":"同安区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":26,"org_id":21,"title":"同安区区长","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":27,"org_id":22,"title":"翔安区委书记","start":"","end":"","rank":"正处","note":"待确认"},
    {"person_id":28,"org_id":23,"title":"翔安区区长","start":"","end":"","rank":"正处","note":"待确认"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Current top leadership pairs
    {"person_a":1,"person_b":2,"type":"党政同僚","context":"厦门市委书记与市长搭档","overlap_org":"厦门市","overlap_period":"2026.04-"},
    {"person_a":1,"person_b":3,"type":"党政同僚","context":"市委书记与人大主任同届工作","overlap_org":"厦门市","overlap_period":"2026-"},
    {"person_a":1,"person_b":4,"type":"党政同僚","context":"市委书记与政协主席同届工作","overlap_org":"厦门市","overlap_period":"2026-"},
    {"person_a":2,"person_b":3,"type":"党政同僚","context":"市长与人大主任同届工作","overlap_org":"厦门市","overlap_period":"2024-"},
    {"person_a":2,"person_b":4,"type":"党政同僚","context":"市长与政协主席同届工作","overlap_org":"厦门市","overlap_period":"2025-"},

    # Predecessor-successor chains — Party Secretary
    {"person_a":5,"person_b":1,"type":"前后任","context":"崔永辉→林涛 厦门市委书记交接(2026.04)","overlap_org":"中共厦门市委","overlap_period":"2026-04"},
    {"person_a":6,"person_b":5,"type":"前后任","context":"赵龙→崔永辉 厦门市委书记交接(2021.10)","overlap_org":"中共厦门市委","overlap_period":"2021-10"},
    {"person_a":9,"person_b":6,"type":"前后任","context":"裴金佳→赵龙 厦门市委书记交接(2020)","overlap_org":"中共厦门市委","overlap_period":"2020"},

    # Predecessor-successor chains — Mayor
    {"person_a":2,"person_b":7,"type":"前后任","context":"黄文辉→伍斌 厦门市长交接(2024.09)","overlap_org":"厦门市人民政府","overlap_period":"2024-09"},
    {"person_a":7,"person_b":8,"type":"前后任","context":"庄稼汉→黄文辉 厦门市长交接(2021)","overlap_org":"厦门市人民政府","overlap_period":"2021"},
    {"person_a":8,"person_b":9,"type":"前后任","context":"裴金佳→庄稼汉 厦门市长交接(2016)","overlap_org":"厦门市人民政府","overlap_period":"2016"},

    # Same person mayor→secretary transition (裴金佳)
    {"person_a":9,"person_b":9,"type":"职务转换","context":"裴金佳由厦门市长转任市委书记","overlap_org":"厦门市","overlap_period":"2016"},

    # Cross-government relationship
    {"person_a":5,"person_b":6,"type":"上下级","context":"崔永辉接替赵龙任厦门市委书记","overlap_org":"中共厦门市委","overlap_period":"2021"},
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
        return (255,50,50)  # Red for Party Secretary
    if "市长" in t and "副" not in t:
        return (50,100,255)  # Blue for Mayor
    if "人大" in t and "主任" in t and "副" not in t:
        return (200,100,100)
    if "政协" in t and "主席" in t and "副" not in t:
        return (100,100,200)
    if "纪委" in t or "纪检" in t:
        return (255,165,0)   # Orange for discipline
    if "副" in t:
        return (100,150,255) # Lighter blue for deputies
    if "（待确认）" in t or "待确认" in t:
        return (180,180,180) # Grey for unknown
    return (100,100,100)

def is_top_leader(p):
    t = p.get("current_post","") or ""
    return ("书记" in t and "副" not in t and "纪委" not in t and "（待确认）" not in t)

def is_mayor(p):
    t = p.get("current_post","") or ""
    return ("市长" in t and "副" not in t) or ("区长" in t and "副" not in t) or ("县长" in t and "副" not in t)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>厦门市领导班子工作关系网络</description>')
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
    pid = f"xm_{p['id']}"
    c = color_for_role(p.get("current_post",""))
    sz = "20.0" if is_top_leader(p) else "15.0" if is_mayor(p) else "12.0"
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
    oid = f"xm_org_{o['id']}"
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
    lines.append(f'      <edge id="e{edge_id}" source="xm_{p["id"]}" target="xm_org_{o["id"]}" label="{label}" weight="1.0">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(po.get("title",""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

# Edges: person↔person (relationship)
for r in relationships:
    if r["person_a"] == r["person_b"]:
        continue  # Skip self-references
    p_a = next(x for x in persons if x["id"] == r["person_a"])
    p_b = next(x for x in persons if x["id"] == r["person_b"])
    edge_id += 1
    context = esc(r.get("context",""))
    lines.append(f'      <edge id="e{edge_id}" source="xm_{p_a["id"]}" target="xm_{p_b["id"]}" label="{context}" weight="2.0">')
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
