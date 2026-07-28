#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 比如县 (Birü County) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/xizang_比如县")
DB_PATH = os.path.join(STAGING, "比如县_network.db")
GEXF_PATH = os.path.join(STAGING, "比如县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "李成统", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "", "education": "青海师范大学法学专业/区党委党校研究生",
     "party_join": "", "work_start": "2000-07",
     "current_post": "那曲市委常委、政法委书记（前比如县委书记）",
     "current_org": "中共那曲市委员会",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E6%88%90%E7%BB%9F/57636447"},
    {"id": 2, "name": "米玛次仁", "gender": "男", "ethnicity": "藏族",
     "birth": "1980-04", "birthplace": "西藏浪卡子县", "education": "西藏农牧学院农林经济管理专业",
     "party_join": "", "work_start": "2002-07",
     "current_post": "比如县委副书记、县长",
     "current_org": "比如县人民政府",
     "source": "https://baike.baidu.com/item/%E7%B1%B3%E7%8E%9B%E6%AC%A1%E4%BB%81/58638277"},
    {"id": 3, "name": "张洪军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委副书记、县人大常委会主任",
     "current_org": "比如县人民代表大会常务委员会",
     "source": "https://baike.baidu.com/item/%E6%AF%94%E5%A6%82%E5%8E%BF/2866286"},
    {"id": 4, "name": "杨春", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长",
     "current_org": "比如县人民政府",
     "source": "百度搜索: 比如县 2024 初中学考"},
    {"id": 5, "name": "赵亚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委领导（具体职务未确认）",
     "current_org": "中共比如县委员会",
     "source": "百度搜索: 2026年比如县"},
    {"id": 6, "name": "热地", "gender": "男", "ethnicity": "藏族",
     "birth": "1938-08", "birthplace": "西藏比如", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "原西藏自治区政府主席（后任全国人大副委员长）",
     "current_org": "",
     "source": "https://en.wikipedia.org/wiki/Raqdi"},
]

organizations = [
    {"id": 1, "name": "中共比如县委员会", "type": "党委", "level": "县处级", "parent": "中共那曲市委员会", "location": "西藏那曲市比如县"},
    {"id": 2, "name": "比如县人民政府", "type": "政府", "level": "县处级", "parent": "那曲市人民政府", "location": "西藏那曲市比如县"},
    {"id": 3, "name": "比如县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "那曲市人大常委会", "location": "西藏那曲市比如县"},
    {"id": 4, "name": "中共那曲市委员会", "type": "党委", "level": "地厅级", "parent": "中共西藏自治区委员会", "location": "西藏那曲市"},
    {"id": 5, "name": "那曲市人民政府", "type": "政府", "level": "地厅级", "parent": "西藏自治区人民政府", "location": "西藏那曲市"},
    {"id": 6, "name": "嘉黎县委", "type": "党委", "level": "县处级", "parent": "中共那曲市委员会", "location": "西藏那曲市嘉黎县"},
    {"id": 7, "name": "嘉黎县人民政府", "type": "政府", "level": "县处级", "parent": "那曲市人民政府", "location": "西藏那曲市嘉黎县"},
    {"id": 8, "name": "聂荣县委", "type": "党委", "level": "县处级", "parent": "中共那曲市委员会", "location": "西藏那曲市聂荣县"},
    {"id": 9, "name": "聂荣县人民政府", "type": "政府", "level": "县处级", "parent": "那曲市人民政府", "location": "西藏那曲市聂荣县"},
    # 嘉黎县下属单位
    {"id": 10, "name": "嘉黎县措拉乡", "type": "乡镇/街道", "level": "乡科级", "parent": "嘉黎县", "location": "西藏那曲市嘉黎县"},
    {"id": 11, "name": "嘉黎县阿扎镇", "type": "乡镇/街道", "level": "乡科级", "parent": "嘉黎县", "location": "西藏那曲市嘉黎县"},
    {"id": 12, "name": "嘉黎县忠玉乡", "type": "乡镇/街道", "level": "乡科级", "parent": "嘉黎县", "location": "西藏那曲市嘉黎县"},
    {"id": 13, "name": "嘉黎县尼屋乡", "type": "乡镇/街道", "level": "乡科级", "parent": "嘉黎县", "location": "西藏那曲市嘉黎县"},
    {"id": 14, "name": "嘉黎县人大常委会", "type": "人大", "level": "县处级", "parent": "嘉黎县", "location": "西藏那曲市嘉黎县"},
    {"id": 15, "name": "那曲地委政法委", "type": "党委", "level": "地厅级", "parent": "中共那曲地区委员会", "location": "西藏那曲市"},
    {"id": 16, "name": "那曲地区公安处", "type": "政府", "level": "地厅级", "parent": "那曲地区行政公署", "location": "西藏那曲市"},
    {"id": 17, "name": "那曲市人大", "type": "人大", "level": "地厅级", "parent": "那曲市", "location": "西藏那曲市"},
    {"id": 18, "name": "那曲市委政法委", "type": "党委", "level": "地厅级", "parent": "中共那曲市委员会", "location": "西藏那曲市"},
    {"id": 19, "name": "西藏自治区政府", "type": "政府", "level": "省部级", "parent": "中央人民政府", "location": "西藏拉萨"},
    {"id": 20, "name": "全国人大常委会", "type": "人大", "level": "国家级", "parent": "全国人民代表大会", "location": "北京"},
    {"id": 21, "name": "嘉黎县农牧局", "type": "政府", "level": "县处级以下", "parent": "嘉黎县人民政府", "location": "西藏那曲市嘉黎县"},
]

positions = [
    # 李成统
    {"person_id": 1, "org_id": 4, "title": "市委常委、政法委书记", "start": "2026-06", "end": "至今", "rank": "副地厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县委书记（兼那曲市人大常委会副主任）", "start": "2022-06", "end": "2026-06", "rank": "副地厅级", "note": "同时任那曲市人大常委会副主任"},
    {"person_id": 1, "org_id": 1, "title": "县委书记、县长", "start": "2022-04", "end": "2022-06", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长（二级巡视员）", "start": "2021-05", "end": "2022-04", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "副书记、县长（二级巡视员）", "start": "2020-04", "end": "2021-05", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "副书记、县长", "start": "2015-01", "end": "2020-04", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "副书记（主持县政府工作）", "start": "2014-05", "end": "2015-01", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "党委副书记、常务副处长（正县级）", "start": "2014-01", "end": "2014-05", "rank": "正县处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "常务副书记、政法委书记，县公安局政委、党委书记", "start": "2012-12", "end": "2014-01", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "副书记、综治办副主任（正县级）", "start": "2012-04", "end": "2012-12", "rank": "正县处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "班子成员、综治办副主任（副县级）", "start": "2010-09", "end": "2012-04", "rank": "副县处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "办公室主任", "start": "2008-06", "end": "2010-09", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "执法督察科科长", "start": "2006-06", "end": "2008-06", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "执法督察科副科长", "start": "2004-05", "end": "2006-06", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "科员", "start": "2003-07", "end": "2004-05", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "督察科科员（那曲地区公安处）", "start": "2000-07", "end": "2003-07", "rank": "科员", "note": ""},
    # 米玛次仁
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "2022-08", "end": "至今", "rank": "县处级", "note": "2026年7月5日第十四届人大一次会议选举连任"},
    {"person_id": 2, "org_id": 6, "title": "县委常委、二级调研员", "start": "2021-12", "end": "2022-08", "rank": "副县处级", "note": "此前2021.04-2021.12 挂职浙江省余姚市副市长"},
    {"person_id": 2, "org_id": 13, "title": "县委常委、尼屋乡党委书记、二级调研员", "start": "2020-11", "end": "2021-12", "rank": "副县处级", "note": "2019.03-2020.01挂职浙江省宁波市余姚市副市长"},
    {"person_id": 2, "org_id": 13, "title": "县委常委、尼屋乡党委书记、三级调研员", "start": "2020-04", "end": "2020-11", "rank": "副县处级", "note": "挂职余姚市副市长"},
    {"person_id": 2, "org_id": 13, "title": "县委常委、尼屋乡党委书记", "start": "2017-01", "end": "2020-04", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "副主任兼忠玉乡党委书记", "start": "2015-08", "end": "2016-09", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "党委书记（副县级）", "start": "2013-04", "end": "2015-08", "rank": "副县处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "党委书记（正科级）", "start": "2012-04", "end": "2013-04", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "党委副书记、镇长", "start": "2010-07", "end": "2012-04", "rank": "正科级", "note": "其中2009.10-2010.07为代理镇长"},
    {"person_id": 2, "org_id": 10, "title": "党委副书记、乡长", "start": "2007-10", "end": "2009-10", "rank": "正科级", "note": "2006.04-2007.10为代理乡长"},
    {"person_id": 2, "org_id": 10, "title": "副乡长", "start": "2005-06", "end": "2006-04", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "科员", "start": "2003-09", "end": "2005-06", "rank": "科员", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "科员", "start": "2002-07", "end": "2003-09", "rank": "科员", "note": ""},
    # 张洪军
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "?", "end": "至今", "rank": "副县处级", "note": "具体任职时间待查"},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "?", "end": "至今", "rank": "县处级", "note": ""},
    # 杨春
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start": "?", "end": "至今", "rank": "副县处级", "note": ""},
    # 赵亚
    {"person_id": 5, "org_id": 1, "title": "县委领导", "start": "?", "end": "至今", "rank": "", "note": "具体职务未确认"},
    # 热地
    {"person_id": 6, "org_id": 19, "title": "西藏自治区政府主席", "start": "", "end": "", "rank": "省部级", "note": "历史数据"},
    {"person_id": 6, "org_id": 20, "title": "全国人大常委会副委员长", "start": "", "end": "", "rank": "国家级", "note": "历史数据"},
]

relationships = [
    {"person_a_id": 1, "person_b_id": 2, "type": "predecessor_successor",
     "context": "李成统2022年4月任县委书记时，米玛次仁2022年8月接任县长。2022.04-2022.06李成统兼任县长过渡期。",
     "overlap_org": "中共比如县委员会、比如县人民政府",
     "overlap_period": "2022-2026"},
    {"person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "李成统任县委书记期间，张洪军任县委副书记、县人大主任。",
     "overlap_org": "中共比如县委员会",
     "overlap_period": "约2022-2026"},
    {"person_a_id": 2, "person_b_id": 3, "type": "overlap",
     "context": "米玛次仁与张洪军同为县委领导，在县委县政府班子中共事。",
     "overlap_org": "中共比如县委员会",
     "overlap_period": "2022-至今"},
    {"person_a_id": 2, "person_b_id": 4, "type": "overlap",
     "context": "米玛次仁为县长，杨春为副县长，为直接上下级关系。",
     "overlap_org": "比如县人民政府",
     "overlap_period": ""},
]

# ── BUILD SQLITE DATABASE ─────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
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
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT,
    start_date TEXT,
    end_date TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
         p.get("birth",""), p.get("birthplace",""), p.get("education",""),
         p.get("party_join",""), p.get("work_start",""),
         p.get("current_post",""), p.get("current_org",""), p.get("source",""))
    )

for o in organizations:
    cur.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location",""))
    )

for pos in positions:
    cur.execute(
        "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note",""))
    )

for r in relationships:
    cur.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
        (r["person_a_id"], r["person_b_id"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF GRAPH ───────────────────────────────────────────────────

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    t = p.get("current_post","")
    if "县委书记" in t and "县委副书记" not in t:
        return "255,50,50"
    elif "县长" in t:
        return "50,100,255"
    elif "人大" in t:
        return "200,255,255"
    elif "纪委书记" in t or "监委" in t:
        return "255,165,0"
    elif "常委" in t:
        return "60,120,60"
    else:
        return "100,100,100"

def person_size(p):
    pid = p["id"]
    if pid == 1:
        return "15.0"  # former 书记
    elif pid == 2:
        return "20.0"  # 县长
    elif pid in (3, 4, 5):
        return "13.0"
    elif pid == 6:
        return "15.0"  # national-level historical figure
    else:
        return "12.0"

def org_color(o):
    typ = o.get("type","")
    if "党委" in typ: return "255,200,200"
    elif "政府" in typ: return "200,200,255"
    elif "纪委" in typ: return "255,200,150"
    elif "人大" in typ: return "200,255,255"
    elif "乡镇" in typ: return "255,255,200"
    else: return "200,200,200"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>比如县县级领导班子关系网络（2026年7月）</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="org_type" title="org_type" type="string"/>')
lines.append('      <attribute id="rank" title="rank" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')

lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('      <attribute id="period" title="period" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = person_size(p)
    rgb = c.split(",")
    pid = p["id"]
    lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="org_type" value=""/>')
    lines.append(f'          <attvalue for="rank" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    oc = org_color(o)
    orgb = oc.split(",")
    oid = 1000 + o["id"]
    lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="org_type" value="{esc(o.get("type",""))}"/>')
    lines.append(f'          <attvalue for="rank" value="{esc(o.get("level",""))}"/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{orgb[0]}" g="{orgb[1]}" b="{orgb[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

lines.append('    <edges>')
eid = 1
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{oid}" label="worked_at">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos.get("start","?")} → {pos.get("end","今")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

for r in relationships:
    lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r.get("overlap_period",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")