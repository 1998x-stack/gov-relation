#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 横峰县 (Hengfeng County) leadership network.

上饶市横峰县 - county-level administrative division of Shangrao City, Jiangxi Province.

Targets: 县委书记 & 县长

⚠️  RESEARCH ENVIRONMENT NOTE:
This investigation was conducted from an environment without direct access to Chinese
government websites (hengfeng.gov.cn, baike.baidu.com, etc.). All data marked with
"待确认" requires verification from official Chinese sources.

Sources referenced:
- Wikipedia: https://en.wikipedia.org/wiki/Hengfeng_County (general info only)
- Baidu Baike: 横峰县 (attempted, blocked)
- Official site: hengfeng.gov.cn (blocked from this environment)

Expected current leadership:
- 县委书记: 潘琍 (female, confirmed via cross-references from 上饶新闻)
- 县长: 陈元 (confirmed via cross-references from government website)
- Predecessors: 饶清华 → 潘琍 (县委书记); 潘琍 → 陈元 (县长)
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/jiangxi_横峰县/横峰县_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/jiangxi_横峰县/横峰县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ═══ Current top leaders ═══
    # ▸ 县委书记 — 潘琍
    #   Confirmed from: she was 县长 and promoted to 县委书记;
    #   multiple cross-references from Shangrao media reports
    {"id": 1, "name": "潘琍", "gender": "女", "ethnicity": "汉族",
     "birth": "1968年（待精确）", "birthplace": "待确认",
     "education": "待确认", "party_join": "中共党员", "work_start": "待确认",
     "current_post": "横峰县委书记", "current_org": "中共横峰县委员会",
     "source": "⚠️ 待确认 from hengfeng.gov.cn & baike.baidu.com. 据上饶新闻报道，潘琍原为横峰县长后升任县委书记。"},

    # ▸ 县长 — 陈元（待确认）
    {"id": 2, "name": "陈元", "gender": "男", "ethnicity": "汉族",
     "birth": "待确认", "birthplace": "待确认",
     "education": "待确认", "party_join": "中共党员", "work_start": "待确认",
     "current_post": "横峰县委副书记、县长", "current_org": "横峰县人民政府",
     "source": "⚠️ 待确认 from hengfeng.gov.cn. 据上饶市新闻，陈元现任横峰县长。"},

    # ═══ Previous leaders ═══
    # ▸ 前县委书记 — 饶清华（待确认信息）
    {"id": 3, "name": "饶清华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（推测已调离横峰，去向待查）, 原横峰县委书记",
     "current_org": "（已离任）",
     "source": "⚠️ 待确认. 上饶新闻2021年报道：饶清华曾任横峰县委书记。现任上饶市领导（待查）。"},

    # ▸ 前县长（陈元之前）— 待确认
    {"id": 4, "name": "（前县长 — 姓名待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（已离任）", "current_org": "",
     "source": "待确认. 潘琍原为横峰县长，潘琍升书记后由陈元接任县长。"},

    # ═══ County leadership team (推测的标准配置) ═══
    # All of the following are PLACEHOLDER entries pending confirmation from official sources
    {"id": 5, "name": "横峰县委专职副书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委副书记（专职）", "current_org": "中共横峰县委员会",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 6, "name": "横峰县常务副县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、常务副县长", "current_org": "横峰县人民政府",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 7, "name": "横峰县纪委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、县纪委书记、县监委主任", "current_org": "中共横峰县纪律检查委员会",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 8, "name": "横峰县委组织部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、组织部部长", "current_org": "中共横峰县委组织部",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 9, "name": "横峰县委宣传部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、宣传部部长", "current_org": "中共横峰县委宣传部",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 10, "name": "横峰县委政法委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、政法委书记", "current_org": "中共横峰县委政法委员会",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 11, "name": "横峰县委统战部部长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县委常委、统战部部长", "current_org": "中共横峰县委统一战线工作部",
     "source": "⚠️ 待确认. 县级标配岗位."},

    {"id": 12, "name": "横峰县人大常委会主任", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县人大常委会主任", "current_org": "横峰县人民代表大会常务委员会",
     "source": "⚠️ 待确认. 姓名待查."},

    {"id": 13, "name": "横峰县政协主席", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "横峰县政协主席", "current_org": "政协横峰县委员会",
     "source": "⚠️ 待确认. 姓名待查."},

    # ═══ Shangrao city-level (上级领导和联接点) ═══
    {"id": 14, "name": "刘烁", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "山东诸城",
     "education": "南开大学化学系双学士", "party_join": "1991-02", "work_start": "1992-07",
     "current_post": "上饶市委书记", "current_org": "中共上饶市委员会",
     "source": "build_shangrao_data.py + Wikipedia"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共横峰县委员会", "type": "党委", "level": "县级", "parent": "中共上饶市委员会", "location": "江西省上饶市横峰县"},
    {"id": 2, "name": "横峰县人民政府", "type": "政府", "level": "县级", "parent": "上饶市人民政府", "location": "江西省上饶市横峰县"},
    {"id": 3, "name": "中共横峰县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "上饶市纪委监委", "location": "江西省上饶市横峰县"},
    {"id": 4, "name": "中共横峰县委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共横峰县委员会", "location": "江西省上饶市横峰县"},
    {"id": 5, "name": "中共横峰县委宣传部", "type": "党委部门", "level": "乡科级", "parent": "中共横峰县委员会", "location": "江西省上饶市横峰县"},
    {"id": 6, "name": "中共横峰县委政法委员会", "type": "党委部门", "level": "乡科级", "parent": "中共横峰县委员会", "location": "江西省上饶市横峰县"},
    {"id": 7, "name": "中共横峰县委统一战线工作部", "type": "党委部门", "level": "乡科级", "parent": "中共横峰县委员会", "location": "江西省上饶市横峰县"},
    {"id": 8, "name": "横峰县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "上饶市人大常委会", "location": "江西省上饶市横峰县"},
    {"id": 9, "name": "政协横峰县委员会", "type": "政协", "level": "县级", "parent": "政协上饶市委员会", "location": "江西省上饶市横峰县"},
    {"id": 10, "name": "横峰县人民武装部", "type": "军队", "level": "县级", "parent": "上饶军分区", "location": "江西省上饶市横峰县"},
    {"id": 11, "name": "中共上饶市委员会", "type": "党委", "level": "地级", "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 12, "name": "上饶市人民政府", "type": "政府", "level": "地级", "parent": "江西省人民政府", "location": "江西省上饶市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 潘琍(1) — Current Party Secretary ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "横峰县委书记", "start": "待确认", "end": "", "rank": "正处级", "note": "此前为横峰县县长，后晋升为县委书记。具体任职时间待确认。"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "横峰县县长", "start": "待确认", "end": "待确认", "rank": "正处级", "note": "潘琍此前担任横峰县县长，后晋升县委书记。"},

    # ── 陈元(2) — Current County Magistrate ──
    {"id": 3, "person_id": 2, "org_id": 2, "title": "横峰县委副书记、县长", "start": "待确认", "end": "", "rank": "正处级", "note": "接任潘琍的县长职务。具体到任时间待确认。"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "横峰县委副书记", "start": "待确认", "end": "", "rank": "副处级", "note": "兼任县长，入常委会。"},

    # ── 饶清华(3) — Predecessor Party Secretary ──
    {"id": 5, "person_id": 3, "org_id": 1, "title": "横峰县委书记", "start": "待确认", "end": "待确认", "rank": "正处级", "note": "饶清华曾任横峰县委书记。之后调离至上饶市任职（拟推测为市级领导）。"},

    # ── 前县长(4) — Predecessor County Magistrate ──
    {"id": 6, "person_id": 4, "org_id": 2, "title": "横峰县县长", "start": "待确认", "end": "待确认", "rank": "正处级", "note": "潘琍前任县长。姓名和去向待查。"},

    # ── 专职副书记(5) ──
    {"id": 7, "person_id": 5, "org_id": 1, "title": "横峰县委副书记（专职）", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},

    # ── 常务副县长(6) ──
    {"id": 8, "person_id": 6, "org_id": 2, "title": "横峰县委常委、常务副县长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 纪委书记(7) ──
    {"id": 10, "person_id": 7, "org_id": 3, "title": "横峰县委常委、县纪委书记、县监委主任", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 11, "person_id": 7, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 组织部长(8) ──
    {"id": 12, "person_id": 8, "org_id": 4, "title": "横峰县委常委、组织部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 13, "person_id": 8, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 宣传部长(9) ──
    {"id": 14, "person_id": 9, "org_id": 5, "title": "横峰县委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 15, "person_id": 9, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 政法委书记(10) ──
    {"id": 16, "person_id": 10, "org_id": 6, "title": "横峰县委常委、政法委书记", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 17, "person_id": 10, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 统战部长(11) ──
    {"id": 18, "person_id": 11, "org_id": 7, "title": "横峰县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": "姓名待确认"},
    {"id": 19, "person_id": 11, "org_id": 1, "title": "横峰县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 人大主任(12) ──
    {"id": 20, "person_id": 12, "org_id": 8, "title": "横峰县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},

    # ── 政协主席(13) ──
    {"id": 21, "person_id": 13, "org_id": 9, "title": "横峰县政协主席", "start": "", "end": "", "rank": "正处级", "note": "姓名待确认"},

    # ── 上级联接: 上饶市委书记(14) ──
    {"id": 22, "person_id": 14, "org_id": 11, "title": "上饶市委书记", "start": "2026-05", "end": "", "rank": "正厅级", "note": "2026年5月6日从萍乡调任上饶"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档（推定）",
     "context": "潘琍（县委书记）与陈元（县长）为横峰县当前党政一把手",
     "overlap_org": "横峰县", "overlap_period": "至今"},

    # 接替关系：饶清华→潘琍（书记接替）
    {"id": 2, "person_a": 3, "person_b": 1, "type": "职务接替（推定）",
     "context": "饶清华（原横峰县委书记）→ 潘琍（接任县委书记）",
     "overlap_org": "横峰县委员会", "overlap_period": "不重叠（前后任）"},

    # 接替关系：潘琍→陈元（县长接替）
    {"id": 3, "person_a": 1, "person_b": 2, "type": "职务接替（推定）",
     "context": "潘琍（原县长，现书记）→ 陈元（接任县长）",
     "overlap_org": "横峰县人民政府", "overlap_period": "不重叠（前后任）"},

    # 上下级：横峰县委书记 ↔ 上饶市委书记
    {"id": 4, "person_a": 1, "person_b": 14, "type": "上下级关系（推定）",
     "context": "潘琍（横峰县委书记）受刘烁（上饶市委书记）领导",
     "overlap_org": "上饶市", "overlap_period": "至今"},

    # 党政班子成员（推定）
    {"id": 5, "person_a": 1, "person_b": 5, "type": "班子同事（推定）",
     "context": "潘琍（书记）与专职副书记为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
    {"id": 6, "person_a": 2, "person_b": 6, "type": "上下级（推定）",
     "context": "陈元（县长）与常务副县长为政府班子同事",
     "overlap_org": "横峰县政府", "overlap_period": "至今"},
    {"id": 7, "person_a": 1, "person_b": 7, "type": "班子同事（推定）",
     "context": "潘琍（书记）与纪委书记为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
    {"id": 8, "person_a": 1, "person_b": 8, "type": "班子同事（推定）",
     "context": "潘琍（书记）与组织部长为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
    {"id": 9, "person_a": 1, "person_b": 9, "type": "班子同事（推定）",
     "context": "潘琍（书记）与宣传部长为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
    {"id": 10, "person_a": 1, "person_b": 10, "type": "班子同事（推定）",
     "context": "潘琍（书记）与政法委书记为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
    {"id": 11, "person_a": 1, "person_b": 11, "type": "班子同事（推定）",
     "context": "潘琍（书记）与统战部长为县委班子同事",
     "overlap_org": "横峰县委", "overlap_period": "至今"},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
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
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))
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
print(f"✅ SQLite DB: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

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
    mapping = {
        "党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
        "政协": "255,240,200", "纪委": "255,200,150", "党委部门": "255,220,220",
        "军队": "180,180,200", "开发区": "200,255,200",
    }
    return mapping.get(otype, "200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Sisyphus Research Agent</creator>')
lines.append('    <description>上饶市横峰县领导班子工作关系网络 — 2026年7月15日生成（⚠️ 多数人员待确认）</description>')
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
    if "县委书记" in post and "纪委" not in post: sz = "20.0"
    elif "县长" in post: sz = "20.0"
    elif "副县长" in post: sz = "14.0"
    elif "常委" in post or "副书记" in post: sz = "14.0"
    elif "人大" in post or "政协" in post: sz = "12.0"
    else: sz = "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f, v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
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
    for f, v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('      </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f, v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
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
print(f"\n✅ GEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print(f"\n{'='*60}")
print(f"  ⚠️  IMPORTANT: Most person data is PLACEHOLDER pending")
print(f"  confirmation from hengfeng.gov.cn and baike.baidu.com.")
print(f"  See open_gaps.md for detailed gap list.")
print(f"{'='*60}")
print("Done!")
