#!/usr/bin/env python3
"""Build SQLite databases and GEXF graphs for:
   1) 共青城市 (Gongqingcheng City) — Jiujiang
   2) 庐山市 (Lushan City) — Jiujiang
Both are county-level cities (县级市) under Jiujiang, Jiangxi."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ═══════════════════════════════════════════════════════════════════
# PART 1: 共青城市 (Gongqingcheng)
# ═══════════════════════════════════════════════════════════════════

gqc_persons = [
    # ── Party Secretaries ──
    {"id": 1, "name": "艾菲", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共共青城市委书记", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},
    {"id": 2, "name": "万建明", "gender": "男", "ethnicity": "汉族",
     "birth": "1976", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原共青城市委书记（被查）", "current_org": "",
     "source": "https://www.163.com/dy/article/JD3HSLBK053469O3.html"},

    # ── Government Leaders ──
    {"id": 3, "name": "扶松涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委副书记、市政府市长候选人", "current_org": "共青城市人民政府",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},
    {"id": 4, "name": "刘阳青", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-12", "birthplace": "江西鄱阳", "education": "博士研究生（清华大学工程物理系核技术应用专业）",
     "party_join": "2009-04", "work_start": "2015-08",
     "current_post": "原共青城市委副书记、市长", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%88%98%E9%98%B3%E9%9D%92"},

    # ── Party Standing Committee Members ──
    {"id": 5, "name": "吴炎弘", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委副书记", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/"},
    {"id": 6, "name": "戴轶苏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委常委、组织部部长", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260714_7273892.html"},
    {"id": 7, "name": "鄢俊彬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委常委、宣传部部长、统战部部长", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260714_7273892.html"},
    {"id": 8, "name": "熊莎", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委常委", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},
    {"id": 9, "name": "胡胃东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市委常委", "current_org": "中共共青城市委员会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},

    # ── Previous Secretaries (historical) ──
    {"id": 10, "name": "黄斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://zh.wikipedia.org/zh-cn/%E5%85%B1%E9%9D%92%E5%9F%8E%E5%B8%82"},
    {"id": 11, "name": "王丰鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.jiujiang.gov.cn/"},

    # ── Other notable figures ──
    {"id": 12, "name": "况泉水", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市人大常委会主任", "current_org": "共青城市人大常委会",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},
    {"id": 13, "name": "杨祖荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "共青城市政协主席", "current_org": "共青城市政协",
     "source": "https://www.gongqing.gov.cn/02/01/202607/t20260703_7268755.html"},
]

gqc_orgs = [
    {"id": 1, "name": "中共共青城市委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江共青城"},
    {"id": 2, "name": "共青城市人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江共青城"},
    {"id": 3, "name": "共青城市人大常委会", "type": "人大", "level": "县处级", "parent": "九江市人大常委会", "location": "江西九江共青城"},
    {"id": 4, "name": "共青城市政协", "type": "政协", "level": "县处级", "parent": "九江市政协", "location": "江西九江共青城"},
]

gqc_positions = [
    # ── Ai Fei (艾菲) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共共青城市委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "现任"},

    # ── Wan Jianming (万建明) ──
    {"id": 2, "person_id": 2, "org_id": 1, "title": "中共共青城市委书记", "start": "2024-11", "end": "2026-01", "rank": "县处级正职", "note": "2026年1月被查，6月被双开"},

    # ── Fu Songtao (扶松涛) ──
    {"id": 3, "person_id": 3, "org_id": 2, "title": "市委副书记、市政府市长候选人", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "市长候选人"},

    # ── Liu Yangqing (刘阳青) ──
    {"id": 4, "person_id": 4, "org_id": 2, "title": "共青城市委副书记、市长", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": "前任市长"},
    {"id": 5, "person_id": 4, "org_id": 2, "title": "共青城市人民政府副市长、代市长", "start": "2021-08", "end": "2021-10", "rank": "县处级副职", "note": ""},
    {"id": 6, "person_id": 4, "org_id": 2, "title": "共青城市委副书记", "start": "2021-08", "end": "2026-07", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 4, "org_id": 1, "title": "原共青城市委副书记、市长", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "调离"},

    # ── Standing Committee ──
    {"id": 8, "person_id": 5, "org_id": 1, "title": "共青城市委副书记", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "共青城市委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 10, "person_id": 7, "org_id": 1, "title": "共青城市委常委、宣传部部长、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 11, "person_id": 8, "org_id": 1, "title": "共青城市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 12, "person_id": 9, "org_id": 1, "title": "共青城市委常委", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Historical ──
    {"id": 13, "person_id": 10, "org_id": 1, "title": "中共共青城市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "早期书记"},
    {"id": 14, "person_id": 11, "org_id": 1, "title": "中共共青城市委书记", "start": "", "end": "", "rank": "县处级正职", "note": ""},

    # ── NPC & CPPCC ──
    {"id": 15, "person_id": 12, "org_id": 3, "title": "共青城市人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 16, "person_id": 13, "org_id": 4, "title": "共青城市政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
]

gqc_relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "交接", "context": "艾菲接替被查的万建明任共青城市委书记（2026年7月）", "overlap_org": "中共共青城市委员会", "overlap_period": "2026-07"},
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "党政搭档", "context": "艾菲任市委书记，扶松涛为市长候选人", "overlap_org": "中共共青城市委员会", "overlap_period": "2026-07"},
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "党政搭档", "context": "万建明任市委书记时，刘阳青任市长", "overlap_org": "中共共青城市委员会", "overlap_period": "2024-11~2026-01"},
    {"id": 4, "person_a_id": 6, "person_b_id": 7, "type": "同僚", "context": "戴轶苏与鄢俊彬均为共青城市委常委", "overlap_org": "中共共青城市委员会", "overlap_period": ""},
    {"id": 5, "person_a_id": 8, "person_b_id": 9, "type": "同僚", "context": "熊莎与胡胃东均为共青城市委常委", "overlap_org": "中共共青城市委员会", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════
# PART 2: 庐山市 (Lushan)
# ═══════════════════════════════════════════════════════════════════

lushan_persons = [
    # ── Party Secretaries ──
    {"id": 1, "name": "邵九思", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "九江市委常委、庐山管理局党委书记、庐山市委书记", "current_org": "中共庐山市委/庐山管理局",
     "source": "https://www.lushan.gov.cn/"},

    # ── Government Leaders ──
    {"id": 2, "name": "熊杜明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "庐山管理局局长、庐山市市长", "current_org": "庐山市人民政府/庐山管理局",
     "source": "https://www.lushan.gov.cn/"},

    # ── Previous Secretaries ──
    {"id": 3, "name": "李甫勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-09", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E6%9D%8E%E7%94%AB%E5%8B%87"},
    {"id": 4, "name": "杨健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://www.jiujiang.gov.cn/"},
]

lushan_orgs = [
    {"id": 1, "name": "中共庐山市委", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江庐山"},
    {"id": 2, "name": "庐山市人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江庐山"},
    {"id": 3, "name": "庐山管理局", "type": "事业/管理", "level": "厅级", "parent": "九江市人民政府", "location": "江西九江庐山"},
]

lushan_positions = [
    # ── Shao Jiusi (邵九思) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "庐山市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 3, "title": "庐山管理局党委书记", "start": "", "end": "", "rank": "厅级", "note": "现任，兼任"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "九江市委常委", "start": "", "end": "", "rank": "副厅级", "note": "兼任庐山市委书记"},

    # ── Xiong Duming (熊杜明) ──
    {"id": 4, "person_id": 2, "org_id": 2, "title": "庐山市市长", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 5, "person_id": 2, "org_id": 3, "title": "庐山管理局局长", "start": "", "end": "", "rank": "厅级", "note": "现任，兼任"},

    # ── Li Fuyong (李甫勇) ──
    {"id": 6, "person_id": 3, "org_id": 1, "title": "庐山市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "前任书记"},

    # ── Yang Jian (杨健) ──
    {"id": 7, "person_id": 4, "org_id": 1, "title": "庐山市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "更早前任"},
]

lushan_relationships = [
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "邵九思任庐山市委书记，熊杜明任市长", "overlap_org": "中共庐山市委/庐山市人民政府", "overlap_period": ""},
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "交接", "context": "邵九思接替李甫勇任庐山市委书记", "overlap_org": "中共庐山市委", "overlap_period": ""},
    {"id": 3, "person_a_id": 3, "person_b_id": 4, "type": "交接", "context": "李甫勇接替杨健任庐山市委书记", "overlap_org": "中共庐山市委", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════
# HELPER: Build SQLite DB + GEXF for one city
# ═══════════════════════════════════════════════════════════════════

def build_database(db_path, persons, orgs, positions, rels, city_label):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE persons (
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

    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER NOT NULL,
        person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                     p["birthplace"], p["education"], p["party_join"], p["work_start"],
                     p["current_post"], p["current_org"], p["source"]))

    for o in orgs:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                    (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                     pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in rels:
        cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                    (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                     r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    psc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()

    print(f"  └─ {city_label}: {pc} persons, {oc} orgs, {psc} positions, {rc} relationships")
    return pc, oc, psc, rc


def build_gexf(gexf_path, persons, orgs, positions, rels, city_label):
    """Generate GEXF 1.3 graph using string formatting to avoid XML namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>{city_label}领导班子工作关系网络 - {TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="category" title="Category" type="string"/>')
    lines.append('      <attribute id="birth" title="Birth" type="string"/>')
    lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
    lines.append('      <attribute id="education" title="Education" type="string"/>')
    lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
    lines.append('      <attribute id="source" title="Source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="period" title="Period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        # Color by role
        if p["id"] == 1 or p["name"] in ["邵九思"]:
            color = '#E03C31'; size = 20.0  # red: Party Secretary
        elif p["id"] in [2, 3, 4] or p["name"] in ["熊杜明"]:
            color = '#2980B9'; size = 18.0  # blue: government leader
        elif p["name"] in ["吴炎弘"]:
            color = '#E67E22'; size = 16.0  # orange: deputy secretary
        elif p["current_post"].find("被查") >= 0:
            color = '#7F8C8D'; size = 14.0  # grey: former/investigated
        else:
            color = '#95A5A6'; size = 12.0  # grey: others

        lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="category" value="person"/>')
        lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
        lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
        lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
        lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'      </node>')

    # Organization nodes
    for o in orgs:
        oid = 1000 + o["id"]
        lines.append(f'      <node id="{oid}" label="{o["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="44" g="62" b="80"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_id = 1
    for pos in positions:
        oid = 1000 + pos["org_id"]
        period = f'{pos["start"] or "?"} → {pos["end"] or "今"}'
        lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
        lines.append(f'          <attvalue for="period" value="{period}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'      </edge>')
        edge_id += 1
    for r in rels:
        lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
        lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'      </edge>')
        edge_id += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(gexf_path), exist_ok=True)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_nodes = len(persons) + len(orgs)
    total_edges = len(positions) + len(rels)
    print(f"  └─ GEXF: {len(persons)} persons + {len(orgs)} orgs = {total_nodes} nodes, "
          f"{len(positions)} worked_at + {len(rels)} relations = {total_edges} edges")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

print("=" * 60)
print("九江市县级市领导班子工作关系网络数据生成")
print("=" * 60)
print()

# ── 1. 共青城市 ──
print("[1/2] 共青城市 (Gongqingcheng)...")
gqc_db = os.path.join(BASE, "data/database/gongqingcheng_network.db")
gqc_gexf = os.path.join(BASE, "data/graph/gongqingcheng_network.gexf")
build_database(gqc_db, gqc_persons, gqc_orgs, gqc_positions, gqc_relationships, "共青城市")
build_gexf(gqc_gexf, gqc_persons, gqc_orgs, gqc_positions, gqc_relationships, "共青城市")
print()

# ── 2. 庐山市 ──
print("[2/2] 庐山市 (Lushan)...")
lushan_db = os.path.join(BASE, "data/database/lushan_network.db")
lushan_gexf = os.path.join(BASE, "data/graph/lushan_network.gexf")
build_database(lushan_db, lushan_persons, lushan_orgs, lushan_positions, lushan_relationships, "庐山市")
build_gexf(lushan_gexf, lushan_persons, lushan_orgs, lushan_positions, lushan_relationships, "庐山市")
print()

print("─" * 60)
print("SUMMARY")
print("─" * 60)
print(f"  共青城市 DB:  {gqc_db}")
print(f"  共青城市 GEXF: {gqc_gexf}")
print(f"  庐山市 DB:    {lushan_db}")
print(f"  庐山市 GEXF:   {lushan_gexf}")
print()
print("Done!")
