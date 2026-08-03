#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 错那市 (Cuona City) leadership network.

错那市 is a county-level city in 山南市 (Shannan), 西藏自治区.
Established as a city on 2024-04-15 (formerly 错那县).

Research date: 2026-08-03
Sources: cuona.gov.cn, shannan.gov.cn, 错那市人大/政协会议 reports
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/xizang_错那市")
DB_PATH = os.path.join(STAGING, "错那市_network.db")
GEXF_PATH = os.path.join(STAGING, "错那市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 巴桑欧珠 — 错那市委书记 (also 山南市人大常委会副主任, 副厅级)
    {"id":1,"name":"巴桑欧珠","gender":"男","ethnicity":"藏族",
     "birth":"","birthplace":"西藏自治区","education":"",
     "party_join":"","work_start":"",
     "current_post":"山南市人大常委会副主任、错那市委书记",
     "current_org":"中共错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146492.html"},

    # 邹云 — 市委副书记、市长 (2026年履新)
    {"id":2,"name":"邹云","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"错那市委副书记、市长",
     "current_org":"错那市人民政府",
     "source":"http://www.cuona.gov.cn/xwzx/ldhd/"},

    # 鲁绪超 — 原市长 (2025.01时尚在任，已离任)
    {"id":3,"name":"鲁绪超","gender":"男","ethnicity":"藏族",
     "birth":"","birthplace":"西藏自治区","education":"",
     "party_join":"","work_start":"",
     "current_post":"原错那市委副书记、市长（已离任）",
     "current_org":"",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146489.html"},

    # ── 领导班子成员 ──
    # 曹勇 — 人大常委会主任
    {"id":4,"name":"曹勇","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人大常委会主任",
     "current_org":"错那市人大常委会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146492.html"},

    # 次旺罗布 — 政协主席
    {"id":5,"name":"次旺罗布","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},

    # 张烁 — 市委常委、政法委书记、公安局局长
    {"id":6,"name":"张烁","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市委常委、政法委书记、公安局局长",
     "current_org":"中共错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/ttxw/202605/t20260525_170101.html"},

    # 斗卓玛 — 副市长
    {"id":7,"name":"斗卓玛","gender":"女","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民政府副市长",
     "current_org":"错那市人民政府",
     "source":"http://www.cuona.gov.cn/xwzx/ttxw/202605/t20260525_170101.html"},

    # 王森 — 副市长
    {"id":8,"name":"王森","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民政府副市长",
     "current_org":"错那市人民政府",
     "source":"http://www.cuona.gov.cn/xwzx/ldhd/202607/t20260708_172943.html"},

    # 扎西 — 副市长
    {"id":9,"name":"扎西","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民政府副市长",
     "current_org":"错那市人民政府",
     "source":"http://www.cuona.gov.cn/xwzx/ldhd/202606/t20260626_171672.html"},

    # 汪海涛 — 副市长
    {"id":10,"name":"汪海涛","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民政府副市长",
     "current_org":"错那市人民政府",
     "source":"http://www.cuona.gov.cn/xwzx/ttxw/202607/t20260709_173136.html"},

    # 尼玛琼达 — 人民法院院长
    {"id":11,"name":"尼玛琼达","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民法院院长",
     "current_org":"错那市人民法院",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146489.html"},

    # 邓晶晶 — 人民检察院检察长
    {"id":12,"name":"邓晶晶","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市人民检察院检察长",
     "current_org":"错那市人民检察院",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146489.html"},

    # 索朗巴珠 — 政协副主席
    {"id":13,"name":"索朗巴珠","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协副主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},

    # 冯勇卫 — 政协副主席
    {"id":14,"name":"冯勇卫","gender":"男","ethnicity":"","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协副主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},

    # 边巴次仁 — 政协副主席
    {"id":15,"name":"边巴次仁","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协副主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},

    # 阿边 — 政协副主席
    {"id":16,"name":"阿边","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协副主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},

    # 益西边久 — 政协副主席
    {"id":17,"name":"益西边久","gender":"男","ethnicity":"藏族","birth":"","birthplace":"",
     "education":"","party_join":"","work_start":"",
     "current_post":"错那市政协副主席",
     "current_org":"政协错那市委员会",
     "source":"http://www.cuona.gov.cn/xwzx/lzyw/202501/t20250122_146488.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共错那市委员会","type":"党委","level":"县级","parent":"中共山南市委员会","location":"西藏自治区山南市错那市"},
    {"id":2,"name":"错那市人民政府","type":"政府","level":"县级","parent":"山南市人民政府","location":"西藏自治区山南市错那市"},
    {"id":3,"name":"错那市人大常委会","type":"人大","level":"县级","parent":"山南市人大常委会","location":"西藏自治区山南市错那市"},
    {"id":4,"name":"政协错那市委员会","type":"政协","level":"县级","parent":"政协山南市委员会","location":"西藏自治区山南市错那市"},
    {"id":5,"name":"中共错那市纪律检查委员会","type":"党委","level":"县级","parent":"中共错那市委员会","location":"西藏自治区山南市错那市"},
    {"id":6,"name":"错那市人民法院","type":"政府","level":"县级","parent":"","location":"西藏自治区山南市错那市"},
    {"id":7,"name":"错那市人民检察院","type":"政府","level":"县级","parent":"","location":"西藏自治区山南市错那市"},
    {"id":8,"name":"错那市公安局","type":"政府","level":"县级","parent":"错那市人民政府","location":"西藏自治区山南市错那市"},
    {"id":9,"name":"山南市人大常委会","type":"人大","level":"地级","parent":"","location":"西藏自治区山南市乃东区"},
    {"id":10,"name":"中共山南市委员会","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区山南市乃东区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 巴桑欧珠
    {"id":1,"person_id":1,"org_id":1,"title":"错那市委书记","start":"","end":"","rank":"副厅级","note":"同时任山南市人大常委会副主任"},
    {"id":2,"person_id":1,"org_id":9,"title":"山南市人大常委会副主任","start":"","end":"","rank":"副厅级","note":"兼任错那市委书记"},
    {"id":3,"person_id":1,"org_id":10,"title":"山南市人大常委会副主任","start":"","end":"","rank":"副厅级","note":""},

    # 邹云
    {"id":4,"person_id":2,"org_id":1,"title":"错那市委副书记","start":"2025/2026?","end":"","rank":"正处级","note":"当前在任"},
    {"id":5,"person_id":2,"org_id":2,"title":"错那市人民政府市长","start":"2025/2026?","end":"","rank":"正处级","note":""},

    # 鲁绪超 (原市长)
    {"id":6,"person_id":3,"org_id":2,"title":"错那市市长","start":"?","end":"~2025","rank":"正处级","note":"2025年1月时尚任市长，已离任"},
    {"id":7,"person_id":3,"org_id":1,"title":"错那市委副书记","start":"","end":"~2025","rank":"正处级","note":""},

    # 曹勇
    {"id":8,"person_id":4,"org_id":3,"title":"错那市人大常委会主任","start":"","end":"","rank":"正处级","note":"2025年1月人代会主持闭幕会"},

    # 次旺罗布
    {"id":9,"person_id":5,"org_id":4,"title":"错那市政协主席","start":"","end":"","rank":"正处级","note":"2025年1月政协会议主持"},

    # 张烁
    {"id":10,"person_id":6,"org_id":1,"title":"错那市委常委","start":"","end":"","rank":"副处级","note":""},
    {"id":11,"person_id":6,"org_id":5,"title":"错那市委政法委书记","start":"","end":"","rank":"副处级","note":""},
    {"id":12,"person_id":6,"org_id":8,"title":"错那市公安局局长","start":"","end":"","rank":"副处级","note":""},

    # 斗卓玛
    {"id":13,"person_id":7,"org_id":2,"title":"错那市人民政府副市长","start":"","end":"","rank":"副处级","note":""},

    # 王森
    {"id":14,"person_id":8,"org_id":2,"title":"错那市人民政府副市长","start":"","end":"","rank":"副处级","note":""},

    # 扎西
    {"id":15,"person_id":9,"org_id":2,"title":"错那市人民政府副市长","start":"","end":"","rank":"副处级","note":""},

    # 汪海涛
    {"id":16,"person_id":10,"org_id":2,"title":"错那市人民政府副市长","start":"","end":"","rank":"副处级","note":""},

    # 尼玛琼达
    {"id":17,"person_id":11,"org_id":6,"title":"错那市人民法院院长","start":"","end":"","rank":"正处级","note":""},

    # 邓晶晶
    {"id":18,"person_id":12,"org_id":7,"title":"错那市人民检察院检察长","start":"","end":"","rank":"正处级","note":""},

    # 索朗巴珠
    {"id":19,"person_id":13,"org_id":4,"title":"错那市政协副主席","start":"","end":"","rank":"副处级","note":""},

    # 冯勇卫
    {"id":20,"person_id":14,"org_id":4,"title":"错那市政协副主席","start":"","end":"","rank":"副处级","note":""},

    # 边巴次仁
    {"id":21,"person_id":15,"org_id":4,"title":"错那市政协副主席","start":"","end":"","rank":"副处级","note":""},

    # 阿边
    {"id":22,"person_id":16,"org_id":4,"title":"错那市政协副主席","start":"","end":"","rank":"副处级","note":""},

    # 益西边久
    {"id":23,"person_id":17,"org_id":4,"title":"错那市政协副主席","start":"","end":"","rank":"副处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 巴桑欧珠 <-> 邹云 (书记-市长搭档)
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate",
     "context":"错那市委书记与市长搭档","overlap_org":"中共错那市委员会/错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},

    # 巴桑欧珠 <-> 曹勇 (书记/人大主任)
    {"id":2,"person_a":1,"person_b":4,"type":"superior_subordinate",
     "context":"市委与市人大常委会工作关系","overlap_org":"错那市",
     "overlap_period":"","confidence":"confirmed"},

    # 邹云 <-> 鲁绪超 (前后任市长)
    {"id":3,"person_a":2,"person_b":3,"type":"predecessor_successor",
     "context":"鲁绪超任错那市长，邹云接任","overlap_org":"错那市人民政府",
     "overlap_period":"2025交接","confidence":"confirmed"},

    # 邹云 <-> 斗卓玛 (市长/副市长)
    {"id":4,"person_a":2,"person_b":7,"type":"superior_subordinate",
     "context":"市长与副市长工作关系","overlap_org":"错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},

    # 邹云 <-> 王森
    {"id":5,"person_a":2,"person_b":8,"type":"superior_subordinate",
     "context":"市长与副市长工作关系","overlap_org":"错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},

    # 邹云 <-> 扎西
    {"id":6,"person_a":2,"person_b":9,"type":"superior_subordinate",
     "context":"市长与副市长工作关系","overlap_org":"错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},

    # 邹云 <-> 汪海涛
    {"id":7,"person_a":2,"person_b":10,"type":"superior_subordinate",
     "context":"市长与副市长工作关系","overlap_org":"错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},

    # 巴桑欧珠 <-> 次旺罗布 (书记/政协主席)
    {"id":8,"person_a":1,"person_b":5,"type":"superior_subordinate",
     "context":"市委-市政协工作关系","overlap_org":"错那市",
     "overlap_period":"","confidence":"confirmed"},

    # 张烁 <-> 邹云 (常委/市长)
    {"id":9,"person_a":6,"person_b":2,"type":"superior_subordinate",
     "context":"市委常委与市长工作关系","overlap_org":"中共错那市委员会/错那市人民政府",
     "overlap_period":"2025-至今","confidence":"confirmed"},
]

# =========================================================================
# GEXF Builder with string formatting
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    if "书记" in p.get("current_post",""):
        return "255,50,50"  # Red
    if "市长" in p.get("current_post","") and "副书记" in p.get("current_post",""):
        return "50,100,255"  # Blue
    if "市长" in p.get("current_post",""):
        return "50,100,255"  # Blue
    if "政法委" in p.get("current_post",""):
        return "255,165,0"  # Orange
    if "人民法院" in p.get("current_post","") or "人民检察院" in p.get("current_post",""):
        return "255,165,0"  # Orange
    return "100,100,100"  # Grey

def org_color(o):
    t = o.get("type","")
    if t == "党委": return "255,200,200"
    if t == "政府": return "200,200,255"
    if t == "人大": return "200,255,255"
    if t == "政协": return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    post = p.get("current_post","")
    if "书记" in post and "副" not in post: return True
    if "市长" in post and "副" not in post: return True
    if "人大主任" in post: return True
    if "政协主席" in post: return True
    return False

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation researcher</creator>')
    lines.append('    <description>错那市领导干部工作关系网络 - Cuona City leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start","") + " - " + pos.get("end",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH} ({eid} edges)")

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert data
    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons
            (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"],p["name"],p.get("gender",""),p.get("ethnicity",""),p.get("birth",""),
             p.get("birthplace",""),p.get("education",""),p.get("party_join",""),p.get("work_start",""),
             p.get("current_post",""),p.get("current_org",""),p.get("source","")))

    for o in organizations:
        cur.execute("INSERT OR IGNORE INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
            (o["id"],o["name"],o["type"],o.get("level",""),o.get("parent",""),o.get("location","")))

    for pos in positions:
        cur.execute("INSERT OR IGNORE INTO positions (id,person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?,?)",
            (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))

    for rel in relationships:
        cur.execute("INSERT OR IGNORE INTO relationships (id,person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?,?)",
            (rel["id"],rel["person_a"],rel["person_b"],rel["type"],rel["context"],rel.get("overlap_org",""),rel.get("overlap_period","")))

    counts = (
        cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0],
        cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0],
    )
    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH} ({counts[0]} persons, {counts[1]} orgs, {counts[2]} positions, {counts[3]} relationships)")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print("Building 错那市 network data...")
    build_db()
    build_gexf()
    print("Done.")