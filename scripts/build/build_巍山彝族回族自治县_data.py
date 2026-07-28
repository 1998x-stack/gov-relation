#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 巍山彝族回族自治县 leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "巍山彝族回族自治县_network.db")
GEXF_PATH = os.path.join(BASE, "巍山彝族回族自治县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── DATA ─────────────────────────────────────────────────────────────
# Sources: https://www.dlweishan.gov.cn/ (official government portal)
# Party Secretary confirmed via multiple government news articles (July 2026)
# County Magistrate bio at /wsxrmzf/c103437/pc/content/...html

persons = [
    # ── Party Secretary (县委书记) ──
    {"id": 1, "name": "丁洪涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共巍山县委书记",
     "current_org": "中共巍山彝族回族自治县委员会",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102087/pc/list.html"},
    # ── County Magistrate (县长) ──
    {"id": 2, "name": "李增发", "gender": "男", "ethnicity": "彝族",
     "birth": "1981-02", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "巍山县委副书记、县长、县政府党组书记",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c103437/pc/content/1983764638855172096/content_1983764638855172096.html"},

    # ── Executive Deputy (常务副县长) ──
    {"id": 3, "name": "徐必祥", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "巍山县委常委、常务副县长、县人民政府党组副书记",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    # ── Deputy County Magistrates (副县长) ──
    {"id": 4, "name": "李宗明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 5, "name": "谢立", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 6, "name": "马永堂", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 7, "name": "毕国泉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 8, "name": "禹彩香", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 9, "name": "阿承文", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    {"id": 10, "name": "李御向", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员",
     "current_org": "巍山彝族回族自治县人民政府",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102596/pc/list.html"},
    # ── Standing Committee Members (县委常委) ──
    {"id": 11, "name": "潘宏戈", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "县委常委、组织部部长",
     "current_org": "中共巍山彝族回族自治县委员会",
     "source": "https://www.dlweishan.gov.cn/wsxrmzf/c102087/pc/list.html"},
]

organizations = [
    {"id": 1, "name": "中共巍山彝族回族自治县委员会", "type": "党委", "level": "县",
     "parent": "大理白族自治州", "location": "巍山彝族回族自治县"},
    {"id": 2, "name": "巍山彝族回族自治县人民政府", "type": "政府", "level": "县",
     "parent": "大理白族自治州", "location": "巍山彝族回族自治县"},
]

positions = [
    # Person -> Organization, with title, dates
    {"person_id": 1, "org_id": 1, "title": "中共巍山县委书记",
     "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长、县政府党组书记",
     "start_date": "", "end_date": "", "rank": "正县级", "note": "1981-02出生，彝族"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长、县政府党组副书记",
     "start_date": "", "end_date": "", "rank": "副县级", "note": "县委常委"},
    {"person_id": 4, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": "负责公安工作"},
    {"person_id": 7, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长、县政府党组成员",
     "start_date": "", "end_date": "", "rank": "副县级", "note": "中央定点帮扶挂职"},
    {"person_id": 11, "org_id": 1, "title": "县委常委、组织部部长",
     "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记和县长党政一把手搭档",
     "overlap_org": "巍山彝族回族自治县", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate",
     "context": "常务副县长协助县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 7, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 9, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长配合县长工作，中央定点帮扶挂职",
     "overlap_org": "巍山彝族回族自治县人民政府", "overlap_period": "当前"},
    {"person_a": 11, "person_b": 1, "type": "superior_subordinate",
     "context": "组织部部长在县委领导下工作",
     "overlap_org": "中共巍山彝族回族自治县委员会", "overlap_period": "当前"},
    {"person_a": 11, "person_b": 2, "type": "same_committee",
     "context": "组织部部长与县长同为县委常委",
     "overlap_org": "中共巍山彝族回族自治县委员会", "overlap_period": "当前"},
]


# ══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

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
    print(f"  巍山彝族回族自治县 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 巍山彝族回族自治县人民政府网站 (dlweishan.gov.cn)")
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
        if "县委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副县长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        colors = {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
        }
        return colors.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>巍山彝族回族自治县 领导班子关系网络</description>',
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
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
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
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
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
    print(f"\n  ✓ 巍出彝族回族自治县 数据构建完成。")


if __name__ == "__main__":
    run_build()