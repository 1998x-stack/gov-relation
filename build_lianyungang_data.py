#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 连云港市 (Lianyungang City) leadership network.

Covers: City-level leadership (市委书记, 市长, 政协主席),
6 district/county-level sub-divisions: 赣榆区, 东海县, 灌云县, 灌南县,
海州区, 连云区.
"""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/lianyungang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/lianyungang_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── City-level leadership — 市委 ──
    # 1. 邢正军 — 连云港市委书记
    {"id":1,"name":"邢正军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"江苏滨海","education":"","party_join":"","work_start":"","current_post":"连云港市委书记","current_org":"中共连云港市委员会","source":"https://www.lyg.gov.cn, https://ldzl.people.com.cn/dfzlk/front/personPage19813.htm"},
    # 2. 周进 — 连云港市长 (1975年生)
    {"id":2,"name":"周进","gender":"男","ethnicity":"汉族","birth":"1975-08","birthplace":"江苏泰州","education":"大学，理学学士","party_join":"","work_start":"","current_post":"连云港市长","current_org":"连云港市人民政府","source":"https://www.lyg.gov.cn/zglygzfmhwz/msg/msg.html"},
    # 3. 黄远征 — 市政协主席
    {"id":3,"name":"黄远征","gender":"男","ethnicity":"汉族","birth":"","birthplace":"四川梓潼","education":"","party_join":"","work_start":"","current_post":"连云港市政协主席","current_org":"政协连云港市委员会","source":"https://zh.wikipedia.org/zh-cn/连云港市"},

    # ── 原赣榆区委书记 吕洁 — 已升任副市长 ──
    {"id":4,"name":"吕洁","gender":"男","ethnicity":"汉族","birth":"1971-08","birthplace":"待查","education":"研究生，哲学硕士","party_join":"","work_start":"","current_post":"连云港市副市长","current_org":"连云港市人民政府","source":"https://www.lyg.gov.cn/zglygzfmhwz/gsh/gsh.html"},

    # ── District/County-level leadership — 已全部确认（2026年7月） ──
    # 苏卫哲 — 连云区委书记（兼市开发区党工委书记）
    {"id":5,"name":"苏卫哲","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"连云区委书记","current_org":"中共连云区委员会","source":"https://www.lyg.gov.cn/zglygzfmhwz/xqdt/content/84425ed3-367f-4b54-92f2-62aae3ced46f.html"},
    # 郭鹏 — 连云区长
    {"id":6,"name":"郭鹏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"连云区长","current_org":"连云区人民政府","source":"https://www.lyg.gov.cn/zglygzfmhwz/xqdt/content/84425ed3-367f-4b54-92f2-62aae3ced46f.html"},
    # 李锋 — 海州区委书记（兼连云港高新区党工委书记）
    {"id":7,"name":"李锋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"海州区委书记","current_org":"中共海州区委员会","source":"http://www.lyghz.gov.cn/lyghzqrmzf/ttxw/content/65dec404-f6b9-4246-bed2-1e87a7e76a6c.html"},
    # 朱伟哲 — 海州区长（兼连云港高新区管委会主任）
    {"id":8,"name":"朱伟哲","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"海州区长","current_org":"海州区人民政府","source":"http://www.lyghz.gov.cn/lyghzqrmzf/hzyw/content/36f9918c-d88a-4f79-ad9e-52ee324d2b27.html"},
    # 吴洋 — 赣榆区委书记（接替吕洁）
    {"id":9,"name":"吴洋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"赣榆区委书记","current_org":"中共赣榆区委员会","source":"https://www.lyg.gov.cn/zglygzfmhwz/xqdt/content/f3dea531-50f3-4c2a-9eff-6fdc32e05d97.html"},
    # 齐庆磊 — 赣榆代区长
    {"id":10,"name":"齐庆磊","gender":"男","ethnicity":"汉族","birth":"1983-11","birthplace":"安徽寿县","education":"研究生，工学硕士","party_join":"","work_start":"","current_post":"赣榆代区长","current_org":"赣榆区人民政府","source":"http://www.ganyu.gov.cn/gyqzf/ll/ll.html"},
    # 张其兵 — 东海县委书记
    {"id":11,"name":"张其兵","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"东海县委书记","current_org":"中共东海县委员会","source":"https://www.lyg.gov.cn/zglygzfmhwz/xqdt/content/bb8115ab-2d3f-414b-ba95-70a9d97ee721.html"},
    # 封波 — 东海县长
    {"id":12,"name":"封波","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"东海县长","current_org":"东海县人民政府","source":"https://www.lyg.gov.cn/zglygzfmhwz/xqdt/content/bb8115ab-2d3f-414b-ba95-70a9d97ee721.html"},
    # 曹明丽 — 灌云县委书记
    {"id":13,"name":"曹明丽","gender":"女","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"灌云县委书记","current_org":"中共灌云县委员会","source":"http://www.guanyun.gov.cn/gyxzf/gyyw/content/505337b3-cb03-4868-b759-c8e5f672b8f0.html"},
    # 陈创 — 灌云县长
    {"id":14,"name":"陈创","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"灌云县长","current_org":"灌云县人民政府","source":"http://www.guanyun.gov.cn/gyxzf/gyyw/content/505337b3-cb03-4868-b759-c8e5f672b8f0.html"},
    # 赵厚峰 — 灌南县委书记
    {"id":15,"name":"赵厚峰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"灌南县委书记","current_org":"中共灌南县委员会","source":"http://www.guannan.gov.cn/gnzx/gnyw/content/bdb9e347-91ab-4819-95d7-2ae509580403.html"},
    # 高站 — 灌南县长
    {"id":16,"name":"高站","gender":"男","ethnicity":"汉族","birth":"","birthplace":"待查","education":"","party_join":"","work_start":"","current_post":"灌南县长","current_org":"灌南县人民政府","source":"http://www.guannan.gov.cn/gnzx/gnyw/content/bdb9e347-91ab-4819-95d7-2ae509580403.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # ── Lianyungang city-level core ──
    {"id":1,"name":"中共连云港市委员会","type":"党委","level":"地级","parent":"中共江苏省委员会","location":"江苏省连云港市"},
    {"id":2,"name":"连云港市人民政府","type":"政府","level":"地级","parent":"江苏省人民政府","location":"江苏省连云港市"},
    {"id":3,"name":"连云港市人大常委会","type":"人大","level":"地级","parent":"","location":"江苏省连云港市"},
    {"id":4,"name":"政协连云港市委员会","type":"政协","level":"地级","parent":"","location":"江苏省连云港市"},
    {"id":5,"name":"中共连云港市纪律检查委员会","type":"党委","level":"地级","parent":"中共连云港市委员会","location":"江苏省连云港市"},

    # ── 3 Districts — Party committees ──
    {"id":6,"name":"中共连云区委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市连云区"},
    {"id":7,"name":"中共海州区委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市海州区"},
    {"id":8,"name":"中共赣榆区委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市赣榆区"},

    # ── 3 Counties — Party committees ──
    {"id":9,"name":"中共东海县委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市东海县"},
    {"id":10,"name":"中共灌云县委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市灌云县"},
    {"id":11,"name":"中共灌南县委员会","type":"党委","level":"县级","parent":"中共连云港市委员会","location":"江苏省连云港市灌南县"},

    # ── 3 Districts — Governments ──
    {"id":12,"name":"连云区人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市连云区"},
    {"id":13,"name":"海州区人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市海州区"},
    {"id":14,"name":"赣榆区人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市赣榆区"},

    # ── 3 Counties — Governments ──
    {"id":15,"name":"东海县人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市东海县"},
    {"id":16,"name":"灌云县人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市灌云县"},
    {"id":17,"name":"灌南县人民政府","type":"政府","level":"县级","parent":"连云港市人民政府","location":"江苏省连云港市灌南县"},

    # ── External / higher-level orgs ──
    {"id":18,"name":"中共江苏省委员会","type":"党委","level":"省级","parent":"","location":"江苏省南京市"},
    {"id":19,"name":"江苏省人民政府","type":"政府","level":"省级","parent":"","location":"江苏省南京市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 邢正军 (连云港市委书记) ──
    {"id":1,"person_id":1,"org_id":1,"title":"连云港市委书记","start":"","end":"","rank":"正厅级","note":""},
    {"id":2,"person_id":1,"org_id":1,"title":"连云港市委副书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 周进 (连云港市长) ──
    {"id":3,"person_id":2,"org_id":2,"title":"连云港市长","start":"","end":"","rank":"正厅级","note":"1975年生"},
    {"id":4,"person_id":2,"org_id":1,"title":"连云港市委副书记","start":"","end":"","rank":"正厅级","note":""},

    # ── 黄远征 (市政协主席) ──
    {"id":5,"person_id":3,"org_id":4,"title":"连云港市政协主席","start":"","end":"","rank":"正厅级","note":""},

    # ── 吕洁 (连云港市副市长) — 原赣榆区委书记现已升任 ──
    {"id":6,"person_id":4,"org_id":2,"title":"连云港市副市长","start":"","end":"","rank":"副厅级","note":"原赣榆区委书记，现兼徐圩新区党工委书记"},

    # ── 苏卫哲 (连云区委书记兼市开发区党工委书记) ──
    {"id":7,"person_id":5,"org_id":6,"title":"连云区委书记","start":"","end":"","rank":"正处级","note":"兼连云港经济技术开发区党工委书记"},
    # ── 郭鹏 (连云区长) ──
    {"id":8,"person_id":6,"org_id":12,"title":"连云区长","start":"","end":"","rank":"正处级","note":""},
    # ── 李锋 (海州区委书记兼高新区党工委书记) ──
    {"id":9,"person_id":7,"org_id":7,"title":"海州区委书记","start":"","end":"","rank":"正处级","note":"兼连云港高新区党工委书记"},
    # ── 朱伟哲 (海州区长兼高新区管委会主任) ──
    {"id":10,"person_id":8,"org_id":13,"title":"海州区长","start":"","end":"","rank":"正处级","note":"兼连云港高新区管委会主任"},
    # ── 吴洋 (赣榆区委书记) ──
    {"id":11,"person_id":9,"org_id":8,"title":"赣榆区委书记","start":"","end":"","rank":"正处级","note":"接替吕洁"},
    # ── 齐庆磊 (赣榆代区长) ──
    {"id":12,"person_id":10,"org_id":14,"title":"赣榆代区长","start":"","end":"","rank":"正处级","note":"1983年11月生，安徽寿县人"},
    # ── 张其兵 (东海县委书记) ──
    {"id":13,"person_id":11,"org_id":9,"title":"东海县委书记","start":"","end":"","rank":"正处级","note":""},
    # ── 封波 (东海县长) ──
    {"id":14,"person_id":12,"org_id":15,"title":"东海县长","start":"","end":"","rank":"正处级","note":""},
    # ── 曹明丽 (灌云县委书记) ──
    {"id":15,"person_id":13,"org_id":10,"title":"灌云县委书记","start":"","end":"","rank":"正处级","note":""},
    # ── 陈创 (灌云县长) ──
    {"id":16,"person_id":14,"org_id":16,"title":"灌云县长","start":"","end":"","rank":"正处级","note":""},
    # ── 赵厚峰 (灌南县委书记) ──
    {"id":17,"person_id":15,"org_id":11,"title":"灌南县委书记","start":"","end":"","rank":"正处级","note":""},
    # ── 高站 (灌南县长) ──
    {"id":18,"person_id":16,"org_id":17,"title":"灌南县长","start":"","end":"","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # ── 邢正军 ↔ 周进（党政搭档）──
    {"id":1,"person_a":1,"person_b":2,"type":"党政搭档","context":"邢正军（连云港市委书记）与周进（市长）为连云港市党政一把手搭档","overlap_org":"连云港市","overlap_period":""},

    # ── 各区委/县委书记与区长/县长（党政搭档）──
    # 连云区: 苏卫哲 ↔ 郭鹏
    {"id":2,"person_a":5,"person_b":6,"type":"党政搭档","context":"苏卫哲（连云区委书记）与郭鹏（连云区长）党政搭档","overlap_org":"连云区","overlap_period":""},
    # 海州区: 李锋 ↔ 朱伟哲
    {"id":3,"person_a":7,"person_b":8,"type":"党政搭档","context":"李锋（海州区委书记）与朱伟哲（海州区长）党政搭档","overlap_org":"海州区","overlap_period":""},
    # 赣榆区: 吴洋 ↔ 齐庆磊
    {"id":4,"person_a":9,"person_b":10,"type":"党政搭档","context":"吴洋（赣榆区委书记）与齐庆磊（赣榆代区长）党政搭档","overlap_org":"赣榆区","overlap_period":""},
    # 东海县: 张其兵 ↔ 封波
    {"id":5,"person_a":11,"person_b":12,"type":"党政搭档","context":"张其兵（东海县委书记）与封波（东海县长）党政搭档","overlap_org":"东海县","overlap_period":""},
    # 灌云县: 曹明丽 ↔ 陈创
    {"id":6,"person_a":13,"person_b":14,"type":"党政搭档","context":"曹明丽（灌云县委书记）与陈创（灌云县长）党政搭档","overlap_org":"灌云县","overlap_period":""},
    # 灌南县: 赵厚峰 ↔ 高站
    {"id":7,"person_a":15,"person_b":16,"type":"党政搭档","context":"赵厚峰（灌南县委书记）与高站（灌南县长）党政搭档","overlap_org":"灌南县","overlap_period":""},

    # ── 市区联系：各区/县委书记向市委书记汇报 ──
    {"id":8,"person_a":1,"person_b":5,"type":"隶属关系","context":"邢正军（市委书记）领导连云区委书记","overlap_org":"连云港市","overlap_period":""},
    {"id":9,"person_a":1,"person_b":7,"type":"隶属关系","context":"邢正军（市委书记）领导海州区委书记","overlap_org":"连云港市","overlap_period":""},
    {"id":10,"person_a":1,"person_b":9,"type":"隶属关系","context":"邢正军（市委书记）领导吴洋（赣榆区委书记）","overlap_org":"连云港市","overlap_period":""},
    {"id":11,"person_a":1,"person_b":11,"type":"隶属关系","context":"邢正军（市委书记）领导张其兵（东海县委书记）","overlap_org":"连云港市","overlap_period":""},
    {"id":12,"person_a":1,"person_b":13,"type":"隶属关系","context":"邢正军（市委书记）领导曹明丽（灌云县委书记）","overlap_org":"连云港市","overlap_period":""},
    {"id":13,"person_a":1,"person_b":15,"type":"隶属关系","context":"邢正军（市委书记）领导赵厚峰（灌南县委书记）","overlap_org":"连云港市","overlap_period":""},
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
lines.append('    <description>连云港市（地级市）领导班子 + 6区县工作关系网络 — 2026年7月14日生成</description>')
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
