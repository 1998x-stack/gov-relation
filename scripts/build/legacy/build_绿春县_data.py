#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 绿春县 (Luchun County), 红河州, 云南省.

Targets: 县委书记 (何阳) & 县长 (龙艳雄)
Task: yunnan_绿春县
Date: 2026-07-28

All leadership data sourced from www.hhlc.gov.cn (official government website).
Biographical details (birth, education, early career) were unavailable — see gaps.
"""

import json, os, sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.now().strftime("%Y%m%d")
DB_PATH = os.path.join(BASE, "绿春县_network.db")
GEXF_PATH = os.path.join(BASE, "绿春县_network.gexf")

# ── DATA ───────────────────────────────────────────────────────────────────

persons = [
    {"id":1,"name":"何阳","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委书记","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn"},
    {"id":2,"name":"龙艳雄","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/info/1081/309821.htm"},
    {"id":3,"name":"马俊","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委副书记","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn"},
    {"id":4,"name":"严磊","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":5,"name":"李七间","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委、县委办主任","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn"},
    {"id":6,"name":"张猛","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"前任县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn"},
    {"id":7,"name":"朱江","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委、副县长（挂职）","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":8,"name":"李吉芳","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":9,"name":"张云","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":10,"name":"李聪","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":11,"name":"赵恒","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":12,"name":"刘杰","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长（挂职）","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":13,"name":"何荣山","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长（挂职）","current_org":"绿春县人民政府","source":"www.hhlc.gov.cn/xrmzf.htm"},
    {"id":14,"name":"王文华","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县人大常委会主任","current_org":"绿春县人民代表大会常务委员会","source":"www.hhlc.gov.cn/info/1081/309821.htm"},
    {"id":15,"name":"杨雷磊","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":16,"name":"白用明","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":17,"name":"陈光浩","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":18,"name":"李成昆","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":19,"name":"白迷诺","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":20,"name":"罗凤珍","gender":"女","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
    {"id":21,"name":"卢光荣","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"县委常委","current_org":"中共绿春县委员会","source":"www.hhlc.gov.cn/info/1081/309841.htm"},
]

organizations = [
    {"id":1,"name":"中共绿春县委员会","type":"党委","level":"县级","parent":"中共红河哈尼族彝族自治州委员会","location":"绿春县"},
    {"id":2,"name":"绿春县人民政府","type":"政府","level":"县级","parent":"红河哈尼族彝族自治州人民政府","location":"绿春县"},
    {"id":3,"name":"绿春县人民代表大会常务委员会","type":"人大","level":"县级","parent":"红河哈尼族彝族自治州人民代表大会常务委员会","location":"绿春县"},
    {"id":4,"name":"中国人民政治协商会议绿春县委员会","type":"政协","level":"县级","parent":"中国人民政治协商会议红河哈尼族彝族自治州委员会","location":"绿春县"},
]

positions = [
    {"pid":1,"oid":1,"t":"绿春县委书记","s":"","e":"present","r":"正处级","n":""},
    {"pid":2,"oid":2,"t":"绿春县人民政府县长","s":"2026-06-25","e":"present","r":"正处级","n":"2026-06-25选举产生"},
    {"pid":2,"oid":1,"t":"县委副书记","s":"2026-06","e":"present","r":"正处级","n":""},
    {"pid":3,"oid":1,"t":"县委副书记","s":"","e":"present","r":"正处级","n":""},
    {"pid":4,"oid":1,"t":"县委常委","s":"","e":"present","r":"副处级","n":""},
    {"pid":5,"oid":1,"t":"县委常委、县委办公室主任","s":"","e":"present","r":"副处级","n":""},
    {"pid":6,"oid":2,"t":"绿春县人民政府县长（前任）","s":"","e":"2026-01","r":"正处级","n":"2026-01-09最后一次露面"},
    {"pid":7,"oid":2,"t":"县委常委、副县长（挂职）","s":"","e":"present","r":"","n":""},
    {"pid":8,"oid":2,"t":"副县长","s":"","e":"present","r":"副处级","n":""},
    {"pid":9,"oid":2,"t":"副县长","s":"","e":"present","r":"副处级","n":""},
    {"pid":10,"oid":2,"t":"副县长","s":"","e":"present","r":"副处级","n":""},
    {"pid":11,"oid":2,"t":"副县长","s":"","e":"present","r":"副处级","n":""},
    {"pid":12,"oid":2,"t":"副县长（挂职）","s":"","e":"present","r":"","n":""},
    {"pid":13,"oid":2,"t":"副县长（挂职）","s":"","e":"present","r":"","n":""},
    {"pid":14,"oid":3,"t":"县人大常委会主任","s":"","e":"present","r":"正处级","n":""},
]

relations = [
    {"a":1,"b":2,"t":"superior_subordinate","c":"何阳（县委书记）与龙艳雄（县长）党政搭档","o":"绿春县","p":"2026-06至今"},
    {"a":1,"b":3,"t":"superior_subordinate","c":"何阳与马俊在县委常委会搭档","o":"中共绿春县委员会","p":""},
    {"a":1,"b":5,"t":"superior_subordinate","c":"何阳与李七间（书记+县委办主任）","o":"中共绿春县委员会","p":""},
    {"a":1,"b":6,"t":"overlap","c":"何阳与前任县长张猛共事","o":"绿春县","p":""},
    {"a":2,"b":6,"t":"predecessor_successor","c":"龙艳雄接替张猛任县长","o":"绿春县人民政府","p":""},
    {"a":1,"b":14,"t":"overlap","c":"何阳与王文华（人大主任）","o":"绿春县","p":""},
]

# ── HELPERS ─────────────────────────────────────────────────────────────────

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(n):
    if n in ("何阳",): return "255,50,50"
    if n in ("龙艳雄","张猛"): return "50,100,255"
    if n in ("马俊",): return "255,165,0"
    if n in ("王文华",): return "200,255,255"
    return "100,100,100"

def psize(n):
    return "20.0" if n in ("何阳","龙艳雄") else "12.0"

def ocolor(t):
    if "党" in t: return "255,200,200"
    if "政" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    return "200,200,200"

# ── BUILD DB ────────────────────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE persons(id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
        CREATE TABLE organizations(id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
        CREATE TABLE positions(id INTEGER PRIMARY KEY AUTOINCREMENT,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,end TEXT,rank TEXT,note TEXT);
        CREATE TABLE relationships(id INTEGER PRIMARY KEY AUTOINCREMENT,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT);
    """)
    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                   p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(?,?,?,?,?,?,?)",
                  (pos["pid"],pos["oid"],pos["t"],pos["s"],pos["e"],pos["r"],pos["n"]))
    for r in relations:
        c.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)",
                  (r["a"],r["b"],r["t"],r["c"],r["o"],r["p"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relations)} relationships")

# ── BUILD GEXF ──────────────────────────────────────────────────────────────

def build_gexf():
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        '  <meta lastmodifieddate="' + TODAY + '">',
        '    <creator>OpenCode Research Agent</creator>',
        '    <description>绿春县领导班子工作关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="role" type="string"/>',
        '      <attribute id="2" title="org" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]
    for p in persons:
        col = pcolor(p["name"]).split(",")
        sz = psize(p["name"])
        lines.append('      <node id="p' + str(p["id"]) + '" label="' + esc(p["name"]) + '">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value="' + esc(p["current_post"]) + '"/>')
        lines.append('          <attvalue for="2" value="' + esc(p["current_org"]) + '"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="' + col[0] + '" g="' + col[1] + '" b="' + col[2] + '"/>')
        lines.append('        <viz:size value="' + sz + '"/>')
        lines.append('      </node>')
    for o in organizations:
        col = ocolor(o["type"]).split(",")
        lines.append('      <node id="o' + str(o["id"]) + '" label="' + esc(o["name"]) + '">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value="' + esc(o["type"]) + '"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="' + col[0] + '" g="' + col[1] + '" b="' + col[2] + '"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append('      <edge id="' + str(eid) + '" source="p' + str(pos["pid"]) + '" target="o' + str(pos["oid"]) + '" label="' + esc(pos["t"]) + '" weight="1.0"/>')
    for r in relations:
        eid += 1
        lines.append('      <edge id="' + str(eid) + '" source="p' + str(r["a"]) + '" target="p' + str(r["b"]) + '" label="' + esc(r["t"]) + '" weight="2.0"/>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {eid} edges")

if __name__ == "__main__":
    print("Building 绿春县 network data...")
    build_db()
    build_gexf()
    print("Done.")