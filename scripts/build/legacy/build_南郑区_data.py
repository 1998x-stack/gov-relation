#!/usr/bin/env python3
"""南郑区 领导班子工作关系网络 — 数据构建脚本"""

import sqlite3, os, sys
from datetime import date

TODAY = date.today().isoformat()
SLUG = "南郑区"
SHORT = "南郑"

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "南郑区_network.db")
GEXF_PATH = os.path.join(BASE, "南郑区_network.gexf")

# ── RESEARCH DATA ──────────────────────────────────────────────────────────

persons = [
    {
        "id": 1, "name": "王志伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "南郑区委书记", "current_org": "中共汉中市南郑区委员会",
        "source": "https://www.nanzheng.gov.cn/"
    },
    {
        "id": 2, "name": "吴辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-12", "birthplace": "", "education": "在职研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "南郑区委副书记、区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 3, "name": "鲁咏涛", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "南郑区人大常委会主任", "current_org": "汉中市南郑区人民代表大会常务委员会",
        "source": "https://www.nanzheng.gov.cn/"
    },
    {
        "id": 4, "name": "李鹏程", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 5, "name": "缪锐", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 6, "name": "孙建", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 7, "name": "饶庆", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 8, "name": "李强", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 9, "name": "陈艳洁", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 10, "name": "高翔", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 11, "name": "李元军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
    {
        "id": 12, "name": "马欢", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "汉中市南郑区人民政府",
        "source": "https://www.nanzheng.gov.cn/nzqrmzf/wuhui/ldzc.shtml"
    },
]

organizations = [
    {"id": 1, "name": "中共汉中市南郑区委员会", "type": "党委", "level": "县处级", "parent": "中共汉中市委", "location": "汉中市南郑区"},
    {"id": 2, "name": "汉中市南郑区人民政府", "type": "政府", "level": "县处级", "parent": "汉中市人民政府", "location": "汉中市南郑区"},
    {"id": 3, "name": "汉中市南郑区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "汉中市人民代表大会常务委员会", "location": "汉中市南郑区"},
]

positions = [
    # 王志伟
    {"person_id": 1, "org_id": 1, "title": "南郑区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026年7月已在任"},
    # 吴辉
    {"person_id": 2, "org_id": 2, "title": "南郑区委副书记、区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2025-08-25前已在任"},
    {"person_id": 2, "org_id": 1, "title": "南郑区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区委副书记"},
    # 鲁咏涛
    {"person_id": 3, "org_id": 3, "title": "南郑区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "党政搭档", "context": "王志伟作为区委书记、吴辉作为区长共同领导南郑区工作",
        "overlap_org": "南郑区", "overlap_period": "2025-至今"
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "党政人大协同", "context": "区委书记与区人大常委会主任工作协同",
        "overlap_org": "南郑区", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 10,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 11,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
    {
        "person_a": 2, "person_b": 12,
        "type": "上下级", "context": "区长与副区长工作关系",
        "overlap_org": "南郑区人民政府", "overlap_period": "2025-至今"
    },
]

# ── DATABASE BUILD ─────────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 南郑区人民政府网站 (nanzheng.gov.cn)")
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

    # ── GEXF ──────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "区委书记" in post:
            return ("255,50,50", 20.0)
        elif "区长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "副区长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
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
        lines.append(f'        <viz:size value="8.0"/>')
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
