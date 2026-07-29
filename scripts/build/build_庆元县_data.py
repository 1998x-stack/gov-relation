#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 庆元县 (Qingyuan County), 浙江省, 丽水市."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TODAY = datetime.now().strftime("%Y-%m-%d")

# Staging paths
STAGING = os.path.join(BASE, "data/tmp/zhejiang_庆元县")
DB_PATH = os.path.join(STAGING, "庆元县_network.db")
GEXF_PATH = os.path.join(STAGING, "庆元县_network.gexf")
SLUG = "庆元县"

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1, "name": "田健晖", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "中共庆元县委书记", "current_org": "中共庆元县委员会",
        "source": "https://www.zjqy.gov.cn/"
    },
    {
        "id": 2, "name": "谭国庆", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "中共庆元县委副书记、县人民政府县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    # ── Government Leadership Team (from 2026 leadership division notice) ──
    {
        "id": 3, "name": "叶伟林", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县委常委、县人民政府常务副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 4, "name": "苏欣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 5, "name": "张延洪", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 6, "name": "徐海涛", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长、县公安局局长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 7, "name": "吕湘", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 8, "name": "周峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 9, "name": "杜波", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 10, "name": "蒋晓平", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府党组成员", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    {
        "id": 11, "name": "周利民", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府党组成员", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2026/art_bf833d42cdfd4e338832f4028527958e.html"
    },
    # ── Lead Party Committee (县委常委) identified from news ──
    {
        "id": 12, "name": "吴青松", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人大常委会主任", "current_org": "庆元县人民代表大会常务委员会",
        "source": "https://www.zjqy.gov.cn/col/col1229356024/art/2026/art_b4667560b4504353ab97fb9f4e529ee2.html"
    },
    {
        "id": 13, "name": "胡显平", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县政协主席", "current_org": "中国人民政治协商会议庆元县委员会",
        "source": "https://www.zjqy.gov.cn/col/col1229356027/art/2026/art_4d81a87fc66340008123818eed99cdf6.html"
    },
    {
        "id": 14, "name": "孔金峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县委常委", "current_org": "中共庆元县委员会",
        "source": "https://www.zjqy.gov.cn/col/col1229356024/art/2026/art_b4667560b4504353ab97fb9f4e529ee2.html"
    },
    # ── Predecessors (from 2025 leadership division - 李志远 was 副县长 in 2025) ──
    {
        "id": 15, "name": "李志远", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "庆元县人民政府原副县长", "current_org": "庆元县人民政府",
        "source": "https://www.zjqy.gov.cn/col/col1229428775/art/2025/art_156462926e2e4209914506e12529162f.html"
    },
]

organizations = [
    {"id": 1, "name": "中共庆元县委员会", "type": "党委", "level": "县", "parent": "中共丽水市委员会", "location": "浙江省丽水市庆元县"},
    {"id": 2, "name": "庆元县人民政府", "type": "政府", "level": "县", "parent": "丽水市人民政府", "location": "浙江省丽水市庆元县"},
    {"id": 3, "name": "庆元县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "丽水市人民代表大会常务委员会", "location": "浙江省丽水市庆元县"},
    {"id": 4, "name": "中国人民政治协商会议庆元县委员会", "type": "政协", "level": "县", "parent": "政协丽水市委员会", "location": "浙江省丽水市庆元县"},
    {"id": 5, "name": "庆元县纪委监委", "type": "党委", "level": "县", "parent": "丽水市纪委监委", "location": "浙江省丽水市庆元县"},
    {"id": 6, "name": "庆元县公安局", "type": "政府", "level": "县直", "parent": "庆元县人民政府", "location": "浙江省丽水市庆元县"},
]

positions = [
    # 田健晖 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共庆元县委书记", "start_date": "2025-? (assumed)", "end_date": "present", "rank": "正处", "note": "Confirmed by official news articles as current 县委书记"},
    # 谭国庆 - 县长
    {"person_id": 2, "org_id": 2, "title": "庆元县人民政府县长", "start_date": "2025-12", "end_date": "present", "rank": "正处", "note": "Listed as 代县长 in Dec 2025, now 县长"},
    # 叶伟林 - 常务副县长
    {"person_id": 3, "org_id": 2, "title": "庆元县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责县政府常务工作"},
    # 苏欣 - 副县长
    {"person_id": 4, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责城建、城市更新、交通等"},
    # 张延洪 - 副县长
    {"person_id": 5, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责工业、商务、科技等"},
    # 徐海涛 - 副县长兼公安局长
    {"person_id": 6, "org_id": 2, "title": "庆元县人民政府副县长、县公安局局长", "start_date": "", "end_date": "present", "rank": "副处", "note": "主持公安局工作"},
    {"person_id": 6, "org_id": 6, "title": "庆元县公安局局长", "start_date": "", "end_date": "present", "rank": "正科", "note": ""},
    # 吕湘 - 副县长
    {"person_id": 7, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责民政、农业农村等"},
    # 周峰 - 副县长
    {"person_id": 8, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "2025-12", "end_date": "present", "rank": "副处", "note": "负责教育、人社、文旅等"},
    # 杜波 - 副县长
    {"person_id": 9, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责水利、生态环境等"},
    # 蒋晓平 - 党组成员
    {"person_id": 10, "org_id": 2, "title": "庆元县人民政府党组成员", "start_date": "", "end_date": "present", "rank": "副处", "note": "负责对外协作、邮政等"},
    # 周利民 - 党组成员
    {"person_id": 11, "org_id": 2, "title": "庆元县人民政府党组成员", "start_date": "2026-01", "end_date": "present", "rank": "副处", "note": "负责国有资产管理、自然资源等"},
    # 吴青松 - 人大主任
    {"person_id": 12, "org_id": 3, "title": "庆元县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处", "note": "Confirmed in multiple news articles"},
    # 胡显平 - 政协主席
    {"person_id": 13, "org_id": 4, "title": "庆元县政协主席", "start_date": "", "end_date": "present", "rank": "正处", "note": "Confirmed from 县政协十届二十三次常委会"},
    # 孔金峰 - 县委常委
    {"person_id": 14, "org_id": 1, "title": "庆元县委常委", "start_date": "", "end_date": "present", "rank": "副处", "note": "Identified from news article as attending county party committee meeting"},
    # 李志远 - 原副县长 (no longer in 2026 division)
    {"person_id": 15, "org_id": 2, "title": "庆元县人民政府副县长", "start_date": "", "end_date": "2025-12", "rank": "副处", "note": "Appeared in Dec 2025 leadership division but not in Jan 2026 division"},
]

relationships = [
    # 田健晖 ↔ 谭国庆 - 正副搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政正职搭档", "overlap_org": "庆元县委/县政府", "overlap_period": "2025-present"},
    # 田健晖 ↔ 叶伟林 - 书记与常务副县长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "庆元县", "overlap_period": "present"},
    # 谭国庆 ↔ 叶伟林 - 县长与常务副
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    # 谭国庆 ↔ 各位副县长 - 县长与副手
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "庆元县人民政府", "overlap_period": "present"},
    # 县委常委之间的同僚关系
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共庆元县委员会", "overlap_period": "present"},
    {"person_a": 3, "person_b": 14, "type": "overlap", "context": "同为县委常委", "overlap_org": "中共庆元县委员会", "overlap_period": "present"},
    # 人大主任、政协主席与县委领导关系
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "县委与县人大领导", "overlap_org": "庆元县", "overlap_period": "present"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委与县政协领导", "overlap_org": "庆元县", "overlap_period": "present"},
    # 原副县长李志远的调整
    {"person_a": 8, "person_b": 15, "type": "predecessor_successor", "context": "周峰接替李志远分管教育文旅等工作", "overlap_org": "庆元县人民政府", "overlap_period": "2025-12"},
]


# ── SQLite ───────────────────────────────────────────────────────────

def create_tables(conn):
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")

    conn.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start_date TEXT, end_date TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 庆元县人民政府网站 (zjqy.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post or "党组成员" in post:
            return ("100,100,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)  # cyan
        elif "政协" in post:
            return ("255,240,200", 12.0)  # cream
        elif "县委常委" in post:
            return ("100,100,100", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()