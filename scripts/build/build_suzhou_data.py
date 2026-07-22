#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 苏州市 (Suzhou City) leadership network.

Covers: City-level leadership (市委书记, 市长, 人大主任, 政协主席),
9 district/county-level sub-divisions: 虎丘区, 吴中区, 相城区, 姑苏区,
吴江区, 张家港市, 常熟市, 昆山市, 太仓市.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/suzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/suzhou_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 1. 范波 — 苏州市委书记 (1969-10, 湖北洪湖, 2025.11任, 江苏省委常委)
    {"id":1,"name":"范波","gender":"男","ethnicity":"汉族","birth":"1969-10","birthplace":"湖北洪湖","education":"","party_join":"","work_start":"","current_post":"苏州市委书记","current_org":"中共苏州市委员会","source":""},
    # 2. 王维 — 苏州市长 (1971年生)
    {"id":2,"name":"王维","gender":"男","ethnicity":"汉族","birth":"1971-00","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"苏州市长","current_org":"苏州市人民政府","source":""},
    # 3. 黄爱军 — 市人大常委会主任
    {"id":3,"name":"黄爱军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"苏州市人大常委会主任","current_org":"苏州市人大常委会","source":""},
    # 4. 朱民 — 市政协主席 (1963年生)
    {"id":4,"name":"朱民","gender":"男","ethnicity":"汉族","birth":"1963-00","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"苏州市政协主席","current_org":"政协苏州市委员会","source":""},

    # ── District/County-level leadership ──
    # 5. 俞愉 — 虎丘区委书记 (1973-03, 苏州人)
    {"id":5,"name":"俞愉","gender":"男","ethnicity":"汉族","birth":"1973-03","birthplace":"苏州","education":"","party_join":"","work_start":"","current_post":"虎丘区委书记","current_org":"中共虎丘区委员会","source":""},
    # 6. 吴琦 — 虎丘区代区长 (1977-04, 江苏泰兴)
    {"id":6,"name":"吴琦","gender":"男","ethnicity":"汉族","birth":"1977-04","birthplace":"江苏泰兴","education":"","party_join":"","work_start":"","current_post":"虎丘区代区长","current_org":"虎丘区人民政府","source":""},
    # 7. 丁立新 — 吴中区委书记
    {"id":7,"name":"丁立新","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"吴中区委书记","current_org":"中共吴中区委员会","source":""},
    # 8. 沈志栋 — 相城区委书记
    {"id":8,"name":"沈志栋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"相城区委书记","current_org":"中共相城区委员会","source":""},
    # 9. 方文浜 — 姑苏区委书记 (1969-11, 苏州人, 原兼任虎丘区书记)
    {"id":9,"name":"方文浜","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"苏州","education":"","party_join":"","work_start":"","current_post":"姑苏区委书记","current_org":"中共姑苏区委员会","source":""},
    # 10. 陈羔 — 姑苏区长 (1975-01, 苏州人)
    {"id":10,"name":"陈羔","gender":"男","ethnicity":"汉族","birth":"1975-01","birthplace":"苏州","education":"","party_join":"","work_start":"","current_post":"姑苏区长","current_org":"姑苏区人民政府","source":""},
    # 11. 王国荣 — 吴江区长
    {"id":11,"name":"王国荣","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"吴江区长","current_org":"吴江区人民政府","source":""},
    # 12. 韩卫 — 张家港市委书记
    {"id":12,"name":"韩卫","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"张家港市委书记","current_org":"中共张家港市委员会","source":""},
    # 13. 秦猛 — 常熟市长
    {"id":13,"name":"秦猛","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"常熟市长","current_org":"常熟市人民政府","source":""},
    # 14. 周伟 — 昆山市委书记 (1974-07, 张家港人)
    {"id":14,"name":"周伟","gender":"男","ethnicity":"汉族","birth":"1974-07","birthplace":"张家港","education":"","party_join":"","work_start":"","current_post":"昆山市委书记","current_org":"中共昆山市委员会","source":""},
    # 15. 陈丽艳 — 昆山市市长 (女, 1978-08, 宜兴人)
    {"id":15,"name":"陈丽艳","gender":"女","ethnicity":"汉族","birth":"1978-08","birthplace":"宜兴","education":"","party_join":"","work_start":"","current_post":"昆山市市长","current_org":"昆山市人民政府","source":""},
    # 16. 徐华东 — 太仓市长
    {"id":16,"name":"徐华东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"太仓市长","current_org":"太仓市人民政府","source":""},

    # ── Placeholder entries for missing data (待查) ──
    # 吴中区长
    {"id":17,"name":"吴中区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"吴中区长","current_org":"吴中区人民政府","source":""},
    # 相城区长
    {"id":18,"name":"相城区长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"相城区长","current_org":"相城区人民政府","source":""},
    # 吴江区委书记
    {"id":19,"name":"吴江区委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"吴江区委书记","current_org":"中共吴江区委员会","source":""},
    # 常熟市委书记
    {"id":20,"name":"常熟市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"常熟市委书记","current_org":"中共常熟市委员会","source":""},
    # 张家港市长
    {"id":21,"name":"张家港市长","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"张家港市长","current_org":"张家港市人民政府","source":""},
    # 太仓市委书记
    {"id":22,"name":"太仓市委书记","gender":"","ethnicity":"","birth":"","birthplace":"信息待查","education":"","party_join":"","work_start":"","current_post":"太仓市委书记","current_org":"中共太仓市委员会","source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Suzhou city-level core ──
    {"id":1,"name":"中共苏州市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省苏州市"},
    {"id":2,"name":"苏州市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省苏州市"},
    {"id":3,"name":"苏州市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省苏州市"},
    {"id":4,"name":"政协苏州市委员会","type":"政协","level":"地级","parent":"","location":"江苏省苏州市"},
    {"id":5,"name":"中共苏州市纪律检查委员会","type":"党委","level":"地级","parent":"中共苏州市委员会","location":"江苏省苏州市"},

    # ── 5 Districts — Party committees ──
    {"id":6,"name":"中共虎丘区委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市虎丘区"},
    {"id":7,"name":"中共吴中区委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市吴中区"},
    {"id":8,"name":"中共相城区委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市相城区"},
    {"id":9,"name":"中共姑苏区委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市姑苏区"},
    {"id":10,"name":"中共吴江区委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市吴江区"},

    # ── 4 County-level cities — Party committees ──
    {"id":11,"name":"中共张家港市委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市张家港市"},
    {"id":12,"name":"中共常熟市委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市常熟市"},
    {"id":13,"name":"中共昆山市委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市昆山市"},
    {"id":14,"name":"中共太仓市委员会","type":"党委","level":"县级","parent":"中共苏州市委员会","location":"江苏省苏州市太仓市"},

    # ── 5 Districts — Governments ──
    {"id":15,"name":"虎丘区人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市虎丘区"},
    {"id":16,"name":"吴中区人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市吴中区"},
    {"id":17,"name":"相城区人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市相城区"},
    {"id":18,"name":"姑苏区人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市姑苏区"},
    {"id":19,"name":"吴江区人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市吴江区"},

    # ── 4 County-level cities — Governments ──
    {"id":20,"name":"张家港市人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市张家港市"},
    {"id":21,"name":"常熟市人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市常熟市"},
    {"id":22,"name":"昆山市人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市昆山市"},
    {"id":23,"name":"太仓市人民政府","type":"政府","level":"县级","parent":"苏州市人民政府","location":"江苏省苏州市太仓市"},

    # ── External / higher-level orgs ──
    {"id":24,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":25,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 范波 (苏州市委书记, 江苏省委常委) ──
    {"id":1,"person_id":1,"org_id":1,"title":"苏州市委书记","start":"2025-11","end":"","rank":"副部级","note":"1969年生，湖北洪湖人，2025.11任，江苏省委常委"},
    {"id":2,"person_id":1,"org_id":1,"title":"苏州市委副书记","start":"2025-11","end":"","rank":"副部级","note":""},
    {"id":3,"person_id":1,"org_id":24,"title":"江苏省委常委","start":"2025-11","end":"","rank":"副部级","note":""},

    # ── 王维 (苏州市长) ──
    {"id":4,"person_id":2,"org_id":2,"title":"苏州市长","start":"","end":"","rank":"副部级","note":"1971年生"},
    {"id":5,"person_id":2,"org_id":1,"title":"苏州市委副书记","start":"","end":"","rank":"副部级","note":""},

    # ── 黄爱军 (市人大常委会主任) ──
    {"id":6,"person_id":3,"org_id":3,"title":"苏州市人大常委会主任","start":"","end":"","rank":"正厅级","note":""},

    # ── 朱民 (市政协主席) ──
    {"id":7,"person_id":4,"org_id":4,"title":"苏州市政协主席","start":"","end":"","rank":"正厅级","note":"1963年生"},

    # ── 俞愉 (虎丘区委书记) ──
    {"id":8,"person_id":5,"org_id":6,"title":"虎丘区委书记","start":"","end":"","rank":"正厅级","note":"1973-03，苏州人"},

    # ── 吴琦 (虎丘区代区长) ──
    {"id":9,"person_id":6,"org_id":15,"title":"虎丘区代区长","start":"","end":"","rank":"正厅级","note":"1977-04，江苏泰兴人"},

    # ── 丁立新 (吴中区委书记) ──
    {"id":10,"person_id":7,"org_id":7,"title":"吴中区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 沈志栋 (相城区委书记) ──
    {"id":11,"person_id":8,"org_id":8,"title":"相城区委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 方文浜 (姑苏区委书记) ──
    {"id":12,"person_id":9,"org_id":9,"title":"姑苏区委书记","start":"","end":"","rank":"正厅级","note":"1969-11，苏州人，此前曾兼任虎丘区委书记"},

    # ── 陈羔 (姑苏区长) ──
    {"id":13,"person_id":10,"org_id":18,"title":"姑苏区长","start":"","end":"","rank":"正厅级","note":"1975-01，苏州人"},

    # ── 王国荣 (吴江区长) ──
    {"id":14,"person_id":11,"org_id":19,"title":"吴江区长","start":"","end":"","rank":"正厅级","note":""},

    # ── 韩卫 (张家港市委书记) ──
    {"id":15,"person_id":12,"org_id":11,"title":"张家港市委书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 秦猛 (常熟市长) ──
    {"id":16,"person_id":13,"org_id":21,"title":"常熟市长","start":"","end":"","rank":"正厅级","note":""},

    # ── 周伟 (昆山市委书记) ──
    {"id":17,"person_id":14,"org_id":13,"title":"昆山市委书记","start":"","end":"","rank":"正厅级","note":"1974-07，张家港人"},

    # ── 陈丽艳 (昆山市市长, 女) ──
    {"id":18,"person_id":15,"org_id":22,"title":"昆山市市长","start":"","end":"","rank":"正厅级","note":"1978-08，宜兴人，女"},

    # ── 徐华东 (太仓市长) ──
    {"id":19,"person_id":16,"org_id":23,"title":"太仓市长","start":"","end":"","rank":"正厅级","note":""},

    # ── Placeholder positions ──
    {"id":20,"person_id":17,"org_id":16,"title":"吴中区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":21,"person_id":18,"org_id":17,"title":"相城区长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":22,"person_id":19,"org_id":10,"title":"吴江区委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":23,"person_id":20,"org_id":12,"title":"常熟市委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":24,"person_id":21,"org_id":20,"title":"张家港市长","start":"","end":"","rank":"正厅级","note":"信息待查"},
    {"id":25,"person_id":22,"org_id":14,"title":"太仓市委书记","start":"","end":"","rank":"正厅级","note":"信息待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 范波 ↔ 王维（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"范波（苏州市委书记）与王维（市长）为苏州市党政一把手搭档","overlap_org":"苏州市","overlap_period":"2025-11至今"},

    # ── 刘小涛 → 范波（前后任书记，刘小涛已升省长）──
    {"id":2,"person_a":0,"person_b":1,"type":"前后任","context":"刘小涛（前任苏州书记，已升省长）→ 范波（2025.11接任苏州书记）","overlap_org":"中共苏州市委员会","overlap_period":"不重叠（前后任）"},

    # ── 方文浜曾兼姑苏+虎丘两区书记（note only, represented in positions）──
    # 方文浜兼任信息已在position note中体现，此处添加跨区关联
    {"id":3,"person_a":5,"person_b":9,"type":"前后任","context":"俞愉（现虎丘区委书记）接替方文浜之前兼任的虎丘区委书记","overlap_org":"中共虎丘区委员会","overlap_period":"不重叠（前后任）"},

    # ── 各区委/市委书记与区长/市长（党政搭档）──
    # 虎丘区
    {"id":4,"person_a":5,"person_b":6,"type":"党政搭档","context":"俞愉（虎丘区委书记）与吴琦（虎丘区代区长）党政搭档","overlap_org":"虎丘区","overlap_period":""},
    # 吴中区
    {"id":5,"person_a":7,"person_b":17,"type":"党政搭档","context":"丁立新（吴中区委书记）与吴中区长党政搭档","overlap_org":"吴中区","overlap_period":""},
    # 相城区
    {"id":6,"person_a":8,"person_b":18,"type":"党政搭档","context":"沈志栋（相城区委书记）与相城区长党政搭档","overlap_org":"相城区","overlap_period":""},
    # 姑苏区
    {"id":7,"person_a":9,"person_b":10,"type":"党政搭档","context":"方文浜（姑苏区委书记）与陈羔（姑苏区长）党政搭档","overlap_org":"姑苏区","overlap_period":""},
    # 吴江区
    {"id":8,"person_a":19,"person_b":11,"type":"党政搭档","context":"吴江区委书记与王国荣（吴江区长）党政搭档","overlap_org":"吴江区","overlap_period":""},
    # 张家港市
    {"id":9,"person_a":12,"person_b":21,"type":"党政搭档","context":"韩卫（张家港市委书记）与张家港市长党政搭档","overlap_org":"张家港市","overlap_period":""},
    # 常熟市
    {"id":10,"person_a":20,"person_b":13,"type":"党政搭档","context":"常熟市委书记与秦猛（常熟市长）党政搭档","overlap_org":"常熟市","overlap_period":""},
    # 昆山市
    {"id":11,"person_a":14,"person_b":15,"type":"党政搭档","context":"周伟（昆山市委书记）与陈丽艳（昆山市市长）党政搭档","overlap_org":"昆山市","overlap_period":""},
    # 太仓市
    {"id":12,"person_a":22,"person_b":16,"type":"党政搭档","context":"太仓市委书记与徐华东（太仓市长）党政搭档","overlap_org":"太仓市","overlap_period":""},

    # ── 市区联系：各区委/市委书记向市委书记汇报 ──
    {"id":13,"person_a":1,"person_b":5,"type":"隶属关系","context":"范波（市委书记）领导俞愉（虎丘区委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":14,"person_a":1,"person_b":7,"type":"隶属关系","context":"范波（市委书记）领导丁立新（吴中区委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":15,"person_a":1,"person_b":8,"type":"隶属关系","context":"范波（市委书记）领导沈志栋（相城区委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":16,"person_a":1,"person_b":9,"type":"隶属关系","context":"范波（市委书记）领导方文浜（姑苏区委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":17,"person_a":1,"person_b":19,"type":"隶属关系","context":"范波（市委书记）领导吴江区委书记","overlap_org":"苏州市","overlap_period":""},
    {"id":18,"person_a":1,"person_b":12,"type":"隶属关系","context":"范波（市委书记）领导韩卫（张家港市委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":19,"person_a":1,"person_b":20,"type":"隶属关系","context":"范波（市委书记）领导常熟市委书记","overlap_org":"苏州市","overlap_period":""},
    {"id":20,"person_a":1,"person_b":14,"type":"隶属关系","context":"范波（市委书记）领导周伟（昆山市委书记）","overlap_org":"苏州市","overlap_period":""},
    {"id":21,"person_a":1,"person_b":22,"type":"隶属关系","context":"范波（市委书记）领导太仓市委书记","overlap_org":"苏州市","overlap_period":""},
]

# =========================================================================
# BUILD SQLITE
# =========================================================================
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# =========================================================================
# BUILD GEXF
# =========================================================================
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post and "市委" in post:
        return "200,30,30"  # deep red for party secretary
    if "市长" in post or "区长" in post or "县长" in post:
        return "30,80,200"  # deep blue for mayor/district head
    if "副书记" in post:
        return "220,60,60"
    if "副市长" in post or "副区长" in post:
        return "60,120,220"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    if "组织部长" in post or "统战部长" in post or "宣传部长" in post or "政法委" in post:
        return "180,90,180"
    if "政协" in post:
        return "180,160,220"
    if "人大" in post:
        return "160,200,220"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>苏州市（地级市）领导班子 + 9区市工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c_ = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","副书记"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c_ = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c_.split(",")[0]}" g="{c_.split(",")[1]}" b="{c_.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
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
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
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
print("\nDone!")
