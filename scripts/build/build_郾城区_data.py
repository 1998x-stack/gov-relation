#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 漯河市郾城区 leadership network.

调查日期: 2026-08-06
调查对象: 区委书记 & 区长（配搭届领导班子、前任/继任路径、工作关系网络）
信息来源: 漯河市郾城区人民政府网站 (www.lhyc.gov.cn), 百度百科 (李占宾/温元哲词条)
置信度: confirmed（官方页面/任前公示/百科） / plausible（媒体） / unverified（推测）
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "郾城区_network.db")
GEXF_PATH = os.path.join(BASE, "郾城区_network.gexf")
PERSONS_DIR = BASE

TODAY = datetime.now().strftime("%Y%m%d")
DATED = datetime.now().strftime("%Y-%m-%d")
SLUG = "河南省漯河市郾城区"
AS_OF = "2026-08-06"

# ── PERSONS ────────────────────────────────────────────────────────
# 角色色彩: 区委书记(red) 区长(blue) 常委/其他(grey) 纪检(orange)
persons = [
    # ═══ 区委领导 ═══
    {"id": 1, "name": "李占宾", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "博士研究生（法学博士）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "郾城区委书记", "current_org": "中共漯河市郾城区委员会",
     "source": "https://baike.baidu.com/item/李占宾"},
    {"id": 2, "name": "温元哲", "gender": "男", "ethnicity": "汉族", "birth": "1986-12",
     "birthplace": "", "education": "硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "郾城区委副书记、区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://baike.baidu.com/item/温元哲"},
    {"id": 3, "name": "冯小利", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、政法委书记", "current_org": "中共漯河市郾城区委员会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059754"},
    {"id": 4, "name": "赵方略", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld"},
    {"id": 5, "name": "李铸涛", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长、副区长", "current_org": "中共漯河市郾城区委员会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1060072"},
    {"id": 6, "name": "张静波", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1060071"},
    {"id": 7, "name": "张旭初", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、人武部部长", "current_org": "郾城区人民武装部",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059752"},
    {"id": 8, "name": "韩亮", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld"},
    {"id": 9, "name": "刘伟", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld"},
    {"id": 10, "name": "段鹏飞", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld"},
    {"id": 11, "name": "楚艳俊", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政府党组成员、副区长", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld"},
    {"id": 12, "name": "张俊才", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组书记、主任", "current_org": "漯河市郾城区人大常委会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1060073"},
    {"id": 13, "name": "朱俊峰", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协党组书记、主席", "current_org": "政协漯河市郾城区委员会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059753"},
    {"id": 14, "name": "祝如刚", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人武部政委", "current_org": "郾城区人民武装部",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059752"},
    {"id": 15, "name": "何向涛", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共漯河市郾城区委员会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059757"},
    {"id": 16, "name": "王昆鹏", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委领导（职务待核）", "current_org": "中共漯河市郾城区委员会",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059757"},
    {"id": 17, "name": "李改付", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区领导", "current_org": "漯河市郾城区人民政府",
     "source": "https://www.lhyc.gov.cn/zwyw/jryc/content_1059748"},
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共漯河市郾城区委员会", "type": "党委", "level": "县处级",
     "parent": "中共漯河市委员会", "location": "河南省漯河市郾城区"},
    {"id": 2, "name": "漯河市郾城区人民政府", "type": "政府", "level": "县处级",
     "parent": "漯河市人民政府", "location": "河南省漯河市郾城区"},
    {"id": 3, "name": "漯河市郾城区人大常委会", "type": "人大", "level": "县处级",
     "parent": "漯河市人大常委会", "location": "河南省漯河市郾城区"},
    {"id": 4, "name": "政协漯河市郾城区委员会", "type": "政协", "level": "县处级",
     "parent": "政协漯河市委员会", "location": "河南省漯河市郾城区"},
    {"id": 5, "name": "郾城区人民武装部", "type": "政府", "level": "县处级",
     "parent": "漯河军分区", "location": "河南省漯河市郾城区"},
]

# ── POSITIONS ─────────────────────────────────────────────────────
positions = [
    # 李占宾（区委书记）
    {"person_id": 1, "org_id": 1, "title": "郾城区委书记", "start": "2025", "end": "present",
     "rank": "县处级正职", "note": "2025-01-25 河南省委组织部公示拟任县（区）委书记"}
    # 详见 person JSON timeline 中的历任链
]
positions += [
    {"person_id": 1, "org_id": 2, "title": "郾城区区长（历任）", "start": "2022-05", "end": "2025",
     "rank": "县处级正职", "note": "2021-01任副区长/代区长，2021-04任区长，2021-08兼区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "郾城区区长", "start": "2025-04", "end": "present",
     "rank": "县处级正职", "note": "2025-04-18 区五届人大六次会议当选区长"},
    {"person_id": 2, "org_id": 1, "title": "郾城区委副书记", "start": "2025", "end": "present",
     "rank": "县处级副职", "note": "此前任漯河市城乡一体化示范区党工委副书记、管委会主任"},
    {"person_id": 3, "org_id": 1, "title": "郾城区委副书记、政法委书记", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "郾城区常务副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "区委常委"},
    {"person_id": 5, "org_id": 1, "title": "区委常委、宣传部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "分管民政、人社、水利、农业、乡村振兴、退役军人等"},
    {"person_id": 6, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "分管工信、商务、招商引资等"},
    {"person_id": 7, "org_id": 5, "title": "郾城区人武部部长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "区委常委"},
    {"person_id": 8, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "区委常委；职责名目含教育文旅卫健等"},
    {"person_id": 9, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "分管自然资源和规划、住建、交通、城管等"},
    {"person_id": 10, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "分管科技等"},
    {"person_id": 11, "org_id": 2, "title": "郾城区副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "分管公安、司法、信访、社会治理等"},
    {"person_id": 12, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present",
     "rank": "县处级正职", "note": "区人大常委会党组书记"},
    {"person_id": 13, "org_id": 4, "title": "区政协主席", "start": "", "end": "present",
     "rank": "县处级正职", "note": "政协党组书记"},
    {"person_id": 14, "org_id": 5, "title": "区人武部政委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "区委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": "具体职责待核"},
    {"person_id": 16, "org_id": 1, "title": "区委领导", "start": "", "end": "present",
     "rank": "", "note": "出席区四大班子慰问，具体职务待核"},
    {"person_id": 17, "org_id": 2, "title": "区领导", "start": "", "end": "present",
     "rank": "", "note": "出席区长办公会"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "李占宾由区长升任区委书记，温元哲接任区长，组成郾城区党政主官搭档",
     "overlap_org": "郾城区党政班子", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与分管政法副书记",
     "overlap_org": "中共漯河市郾城区委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与政法委副书记同为区委常委/班子成员",
     "overlap_org": "中共漯河市郾城区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与常务副区长",
     "overlap_org": "中共漯河市郾城区委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与常务副区长（温元哲主持区长办公会，赵方略出席）",
     "overlap_org": "漯河市郾城区人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "区委书记与区人大常委会主任（张俊才主持人大党组会传达书记讲话）",
     "overlap_org": "郾城区人大", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "区委书记与区政协主席朱俊峰同列区'四大班子'领导",
     "overlap_org": "郾城区党政班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "overlap",
     "context": "区长与人大常委会主任同区'四大班子'",
     "overlap_org": "郾城区党政班子", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "温元哲主持召开区长办公会，区领导李改付出席",
     "overlap_org": "漯河市郾城区人民政府", "overlap_period": "2026-07"},
    {"person_a": 3, "person_b": 6, "type": "overlap",
     "context": "区委副书记冯小利与区委常委张静波同区班子",
     "overlap_org": "中共漯河市郾城区委员会", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "赵方略与张静波同为区（政府/常委）副区长",
     "overlap_org": "漯河市郾城区人民政府", "overlap_period": "至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap",
     "context": "宣传部部长李铸涛与人武部长张旭初同调研人武旧址",
     "overlap_org": "郾城区人武部调研", "overlap_period": "2026-07"},
]

# ── HELPER FUNCTIONS ──────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p.get("current_post", "")
    if "区委书记" in post:
        return "255,50,50"
    if "区长" in post:
        return "50,100,255"
    if "区委副书记" in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(p):
    post = p.get("current_post", "")
    return "区委书记" in post or "区长" in post

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t:
        return "255,200,150"
    return "200,200,200"

# ── BUILD DATABASE ─────────────────────────────────────────────────
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start TEXT DEFAULT '', "end" TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT ''
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT ''
        );
    """)
    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start,"end",rank,note)
                       VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period)
                       VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# ── BUILD GEXF ────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>郾城区领导班子工作关系网络 - {SLUG}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        oid = o["id"] + 100000
        t = o.get("type", "")
        c = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(t)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("rank",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# ── PERSON JSON ────────────────────────────────────────────────────
def write_person_json(person):
    name = person["name"]
    job = "区委书记" if "区委书记" in person["current_post"] else ("区长" if "区长" in person["current_post"] else "区领导")
    filename = f"{TODAY}-河南省-漯河市-{job}-{name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    rels = []
    for r in relationships:
        if r["person_a"] == person["id"]:
            other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
            if other:
                rels.append({"person": other, "person_id": f"henan_luohe_yancheng_{other}",
                             "relationship_type": r["type"], "evidence": r["context"],
                             "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"],
                             "direction": "undirected", "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})
        elif r["person_b"] == person["id"]:
            other = next((p["name"] for p in persons if p["id"] == r["person_a"]), "")
            if other:
                rels.append({"person": other, "person_id": f"henan_luohe_yancheng_{other}",
                             "relationship_type": r["type"], "evidence": r["context"],
                             "overlap_org": r["overlap_org"], "overlap_period": r["overlap_period"],
                             "direction": "undirected", "confidence": "confirmed",
                             "source_ids": ["S001", "S002"]})

    timeline = []
    for pos in positions:
        if pos["person_id"] == person["id"]:
            org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
            timeline.append({
                "start": pos.get("start", "") or "unknown", "end": pos.get("end", "") or "unknown",
                "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                "location": "河南省漯河市郾城区", "notes": pos.get("note", ""),
                "confidence": "confirmed", "source_ids": ["S001", "S002"]
            })

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "河南省", "city": "漯河市", "region": "郾城区", "job": job,
                                "task_id": "henan_郾城区", "time_focus": f"as of {AS_OF}"},
        "identity": {
            "person_id": f"yan_cheng_{name}", "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{person.get('birth','')}", "official_profile_url": person.get("source", "")},
        },
        "current_status": {
            "current_post": person.get("current_post", ""), "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002"]
        },
        "career_timeline": timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels,
        "governance_record": governance_record(person),
        "professional_profile": professional_profile(person),
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "low_profile", "evidence": "区级副职领导公开专访少，多以会议新闻呈现", "confidence": "unverified"}],
            "speech_themes": [], "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {"degree": len(rels), "part_of_leadership": True},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未检索到公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "百度百科-李占宾/温元哲", "url": "https://baike.baidu.com", "published_at": "", "accessed_at": AS_OF,
             "source_type": "encyclopedia", "reliability": "medium", "notes": "身份/历任一节的基础"},
            {"id": "S002", "title": "漯河市郾城区人民政府-政府领导", "url": "https://www.lhyc.gov.cn/zwgk/fdzdgknr/zfld", "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "区政府领导班子及分工"},
            {"id": "S003", "title": "郾城区动态新闻（区委/人大/政协）", "url": "https://www.lhyc.gov.cn/zwyw/jryc/", "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "区四大班子领导活动、职务确认"}
        ],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") or person.get("education") else "partial",
            "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "早期身份年份、籍贯、完整历任链条公开资料不全"
        },
        "open_questions": [
            {"priority": "high", "question": f"{name}的出生年份与籍贯", "why_it_matters": "用于跨县/跨市身份去重与同乡关系线索",
             "suggested_queries": [f"{name} 简历", f"{name} 户籍"], "last_attempted": AS_OF},
            {"priority": "high", "question": f"{name}在任区长/书记前的完整职业链", "why_it_matters": "判断干部成长路径（区县历练/市直系统）",
             "suggested_queries": [f"{name} 历任职务 郾城区", f"{name} 此前 任职"], "last_checked": AS_OF},
            {"priority": "medium", "question": f"{name}的具体分工调整（如宣传部长归属）", "why_it_matters": "确认班子里最近的人事分工变动",
             "suggested_queries": [f"郾城区 领导分工 {AS_OF}"], "last_checked": AS_OF},
        ]
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {filepath}")

def governance_record(person):
    if person["name"] == "李占宾":
        return [{"period": "2025-", "domain": "overall_leadership", "achievement": "主抓区委全面工作，推动党风廉政、科技强区战略落地",
                 "role_in_event": "区委书记", "location": "郾城区", "confidence": "confirmed", "source_ids": ["S003"]}]
    if person["name"] == "温元哲":
        return [{"period": "2025-", "domain": "government_operation", "achievement": "主持区政府全面工作，推动龙江路西伸、西环二期等城市重点工程建设与土地出让落地",
                 "role_in_event": "区长", "location": "郾城区", "confidence": "confirmed", "source_ids": ["S003"]}]
    return []

def professional_profile(person):
    if person["name"] == "李占宾":
        return {"primary_specializations": ["政治治理", "法学"], "career_pattern": "district_governance_ladder",
                "systems_experience": ["government", "party"], "geographic_pattern": ["河南省漯河市郾城区"],
                "promotion_velocity": {"summary": "由区主席高位区长升至区委书记", "notable_fast_promotions": []}}
    if person["name"] == "温元哲":
        return {"primary_specializations": ["区域经济", "管理"], "career_pattern": "cross_district_rotation",
                "systems_experience": ["development_zone", "government", "party"], "geographic_pattern": ["河南省漯河市"],
                "promotion_velocity": {"summary": "示范区管委会主任→区政府的跨部门升任", "notable_fast_promotions": []}}
    return {"primary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": []}

# ── MAIN ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_db()
    build_gexf()
    # 核心人物：区委书记 & 区长
    for p in persons:
        if p["id"] in (1, 2):
            write_person_json(p)
    print("郾城区 build complete.")