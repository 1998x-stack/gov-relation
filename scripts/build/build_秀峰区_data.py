#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
秀峰区领导班子工作关系网络 — 数据构建脚本 (staging)
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广西壮族自治区
Parent City: 桂林市
Region: 秀峰区
Targets: 区委书记 & 区长

Research Date: 2026-07-22
Sources: 秀峰区人民政府官网 (http://www.glxfq.gov.cn/)
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

SLUG = "秀峰区"
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    {"id": 1, "name": "刘丰华", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-12", "birthplace": "河南开封",
     "education": "北京大学分子医学研究所细胞生物学专业，研究生学历，理学博士",
     "party_join": "2007-04", "work_start": "2014-07",
     "current_post": "区委书记、区长",
     "current_org": "桂林市秀峰区委员会/秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/qz/"},
    {"id": 2, "name": "蒋闻", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区政府主要负责同志（推测为代区长）",
     "current_org": "秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 3, "name": "周琥", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委副书记", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27852041.shtml"},
    {"id": 4, "name": "蒋鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "广西桂林",
     "education": "广西师范大学行政管理专业在职研究生学历，理学学士",
     "party_join": "", "work_start": "2009-08",
     "current_post": "区委常委、常务副区长",
     "current_org": "桂林市秀峰区委员会/秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/cwfqz/t26634296.shtml"},
    {"id": 5, "name": "赵宇宁", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-05", "birthplace": "广西全州",
     "education": "中国人民公安大学安全技术及工程专业毕业",
     "party_join": "2011-11", "work_start": "2012-10",
     "current_post": "副区长、市公安局秀峰分局局长",
     "current_org": "秀峰区人民政府/桂林市公安局秀峰分局",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/fqz/t26634305.shtml"},
    {"id": 6, "name": "陆军", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-11", "birthplace": "湖南武冈",
     "education": "广西财经学院会计系会计专业，助理会计师",
     "party_join": "1999-12", "work_start": "1990-07",
     "current_post": "副区长", "current_org": "秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/fqz/t26634312.shtml"},
    {"id": 7, "name": "蔡俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "广西桂林",
     "education": "广西师范大学国民经济学专业在职研究生学历，理学学士",
     "party_join": "2006-10", "work_start": "2002-08",
     "current_post": "副区长", "current_org": "秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/fqz/t27327541.shtml"},
    {"id": 8, "name": "凤彬", "gender": "女", "ethnicity": "瑶族",
     "birth": "1984-01", "birthplace": "广西灌阳",
     "education": "西南政法大学管理学院会计学专业、法学专业，助理会计师",
     "party_join": "", "work_start": "2005-07",
     "current_post": "副区长", "current_org": "秀峰区人民政府",
     "source": "http://www.glxfq.gov.cn/zfxxgk/fdzdgknr/jcxxgk/zfld/fqz/t26634318.shtml"},
    {"id": 9, "name": "余捷", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任区委书记（至约2025-12/2026-01）",
     "current_org": "去向待查",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t26683938.shtml"},
    {"id": 10, "name": "陈建国", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "秀峰区人大常委会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 11, "name": "苏绍坤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区政协主席", "current_org": "秀峰区政协",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 12, "name": "喻孝迦", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 13, "name": "龙宪智", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27852041.shtml"},
    {"id": 14, "name": "姚国艳", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27852041.shtml"},
    {"id": 15, "name": "王新红", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 16, "name": "谭雅纹", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
    {"id": 17, "name": "梁莹", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委、组织部部长", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27852049.shtml"},
    {"id": 18, "name": "魏勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委常委（具体职务待查）", "current_org": "桂林市秀峰区委员会",
     "source": "http://www.glxfq.gov.cn/zwdt/xfdt/t27873265.shtml"},
]

organizations = [
    {"id": 0, "name": "中国共产党桂林市秀峰区委员会", "type": "党委",
     "level": "县处级", "parent": "桂林市委", "location": "桂林市秀峰区"},
    {"id": 1, "name": "秀峰区人民政府", "type": "政府",
     "level": "县处级", "parent": "桂林市人民政府", "location": "桂林市秀峰区"},
    {"id": 2, "name": "秀峰区人大常委会", "type": "人大",
     "level": "县处级", "parent": "", "location": "桂林市秀峰区"},
    {"id": 3, "name": "秀峰区政协", "type": "政协",
     "level": "县处级", "parent": "", "location": "桂林市秀峰区"},
    {"id": 4, "name": "桂林市公安局秀峰分局", "type": "政府",
     "level": "乡科级", "parent": "桂林市公安局", "location": "桂林市秀峰区"},
    {"id": 5, "name": "秀峰区纪委监委", "type": "党委",
     "level": "县处级", "parent": "桂林市纪委监委", "location": "桂林市秀峰区"},
]

positions = [
    {"person_id": 1, "org_id": 0, "title": "区委书记",
     "start_date": "2026-01", "end_date": "present",
     "rank": "正处级", "note": "从区长升任区委书记，形成一肩挑"},
    {"person_id": 1, "org_id": 1, "title": "区长",
     "start_date": "~2024", "end_date": "present",
     "rank": "正处级", "note": "兼任区长"},
    {"person_id": 1, "org_id": 0, "title": "区委副书记",
     "start_date": "~2024", "end_date": "2026-01",
     "rank": "副处级", "note": "升任区长前的职务"},
    {"person_id": 2, "org_id": 1, "title": "区政府主要负责同志（推测代区长）",
     "start_date": "2026-07", "end_date": "present",
     "rank": "正处级", "note": "首次公开出现于2026年7月8日区委常委会"},
    {"person_id": 3, "org_id": 0, "title": "区委副书记",
     "start_date": "~2026", "end_date": "present",
     "rank": "副处级", "note": "专职副书记"},
    {"person_id": 4, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "常务副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "分局局长",
     "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任"},
    {"person_id": 6, "org_id": 1, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "副区长",
     "start_date": "2026-01", "end_date": "present", "rank": "副处级", "note": "2026年1月新任命"},
    {"person_id": 8, "org_id": 1, "title": "副区长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "无党派人士"},
    {"person_id": 9, "org_id": 0, "title": "区委书记",
     "start_date": "~2021", "end_date": "~2025-12",
     "rank": "正处级", "note": "前任区委书记，去向待查"},
    {"person_id": 10, "org_id": 2, "title": "区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "区政协主席",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 14, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 15, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 16, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    {"person_id": 17, "org_id": 0, "title": "区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 0, "title": "区委常委",
     "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "刘丰华原兼任区长，蒋闻以区政府主要负责同志身份接班",
     "overlap_org": "秀峰区人民政府", "overlap_period": "2026-07"},
    {"person_a": 9, "person_b": 1, "type": "predecessor_successor",
     "context": "余捷为前任区委书记，刘丰华于2026年初接任",
     "overlap_org": "桂林市秀峰区委员会", "overlap_period": "~2025-12/2026-01"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "刘丰华为区委书记，周琥为区委副书记",
     "overlap_org": "桂林市秀峰区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "刘丰华为区长，蒋鹏为常务副区长",
     "overlap_org": "秀峰区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor",
     "context": "周琥原为常务副区长，升任区委副书记后由蒋鹏接替常务副区长",
     "overlap_org": "秀峰区人民政府/桂林市秀峰区委员会", "overlap_period": "~2026"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "秀峰区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "秀峰区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "秀峰区人民政府", "overlap_period": "2026-01至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "秀峰区人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "overlap",
     "context": "同为副区长，在同届区政府中共事",
     "overlap_org": "秀峰区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate",
     "context": "区委书记—组织部部长",
     "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 12, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 17, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 14, "person_b": 15, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 16, "person_b": 18, "type": "overlap",
     "context": "同为区委常委", "overlap_org": "桂林市秀峰区委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 1, "type": "overlap",
     "context": "人大常委会主任与区委书记共事",
     "overlap_org": "秀峰区", "overlap_period": ""},
    {"person_a": 11, "person_b": 1, "type": "overlap",
     "context": "政协主席与区委书记共事",
     "overlap_org": "秀峰区", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# SQLITE
# ═══════════════════════════════════════════════════════════════════════════════

def build_db():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript("""
        CREATE TABLE persons (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '', current_org TEXT DEFAULT '',
            source TEXT DEFAULT '');
        CREATE TABLE organizations (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            type TEXT DEFAULT '', level TEXT DEFAULT '', parent TEXT DEFAULT '',
            location TEXT DEFAULT '');
        CREATE TABLE positions (id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id));
        CREATE TABLE relationships (id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id));
    """)

    pcols = ["id","name","gender","ethnicity","birth","birthplace",
             "education","party_join","work_start","current_post","current_org","source"]
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(pcols)}) VALUES ({','.join(['?']*len(pcols))})",
                     [p.get(c,"") for c in pcols])

    ocols = ["id","name","type","level","parent","location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join(['?']*len(ocols))})",
                     [o.get(c,"") for c in ocols])

    pscols = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(pscols)}) VALUES ({','.join(['?']*len(pscols))})",
                     [pos.get(c,"") for c in pscols])

    rcols = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join(['?']*len(rcols))})",
                     [r.get(c,"") for c in rcols])

    conn.commit()
    conn.close()
    print(f"DB created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# GEXF
# ═══════════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(post):
    if "书记" in post and "副" not in post: return "255,50,50"
    if "区长" in post or ("长" in post and "副" not in post): return "50,100,255"
    if "纪委" in post: return "255,165,0"
    return "100,100,100"

def person_sz(post):
    if ("书记" in post and "副" not in post) or ("长" in post and "副" not in post):
        return "20.0"
    return "12.0"

def org_color(t):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
            "政协":"255,240,200"}.get(t, "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Investigator</creator>')
    lines.append(f'    <description>{SLUG} 领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    for aid,aname,atype in [("0","type","string"),("1","current_post","string"),
                            ("2","current_org","string"),("3","birth","string"),
                            ("4","birthplace","string"),("5","source","string")]:
        lines.append(f'      <attribute id="{aid}" title="{aname}" type="{atype}"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for eid,ename,etype in [("0","type","string"),("1","context","string"),
                            ("2","overlap_org","string"),("3","overlap_period","string")]:
        lines.append(f'      <attribute id="{eid}" title="{ename}" type="{etype}"/>')
    lines.append('    </attributes>')

    # nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["current_post"])
        sz = person_sz(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"][:80])}"/>')
        if p["birth"]: lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        if p["birthplace"]: lines.append(f'          <attvalue for="4" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p["source"][:80])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        if o["parent"]: lines.append(f'          <attvalue for="3" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        if pos.get("start_date"): lines.append(f'          <attvalue for="2" value="{esc(pos["start_date"])}"/>')
        if pos.get("end_date"): lines.append(f'          <attvalue for="3" value="{esc(pos["end_date"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["type"] in ("predecessor_successor","superior_subordinate") else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        if r["overlap_org"]: lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        if r["overlap_period"]: lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    GEXF_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    build_db()
    build_gexf()
    print(f"Summary: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print("Build complete!")

if __name__ == "__main__":
    main()
