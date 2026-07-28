#!/usr/bin/env python3
"""加查县（Gyaca County）领导班子工作关系网络 — 构建脚本"""

import sqlite3, os, sys
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "加查县"
STAGING = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING, "加查县_network.db")
GEXF_PATH = os.path.join(STAGING, "加查县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "侯宝萍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县委书记",
        "current_org": "中共加查县委员会",
        "source": "jiacha.gov.cn - 领导活动: 带队慰问人大代表政协委员(2026-07-16), 七一走访慰问(2026-07-03)"
    },
    {
        "id": 2,
        "name": "格桑次仁",
        "gender": "",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县委副书记、县长",
        "current_org": "加查县人民政府",
        "source": "jiacha.gov.cn - 领导之窗; 主持县政府会议、调研洛林乡(2026-06-18)"
    },
    {
        "id": 3,
        "name": "蒙汐恒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县副县长（分管生态环保）",
        "current_org": "加查县人民政府",
        "source": "jiacha.gov.cn - 领导活动: 深入一线检查生态环境保护工作(2026-03-17)"
    },
    {
        "id": 4,
        "name": "杨伟涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县副县长",
        "current_org": "加查县人民政府",
        "source": "jiacha.gov.cn - 领导活动: 带队开展森林草原防火专项检查(2026-03-05)"
    },
    {
        "id": 5,
        "name": "陈明伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县委常委",
        "current_org": "中共加查县委员会",
        "source": "jiacha.gov.cn - 领导活动: 三大节日走访慰问(2026-02-09), 住建领域调研(2025-12-30)"
    },
    {
        "id": 6,
        "name": "刘洁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "加查县领导（副县级）",
        "current_org": "加查县人民政府",
        "source": "jiacha.gov.cn - 领导活动: 巡林(2026-01-15), 物交会慰问(2025-12-03)"
    },
    {
        "id": 7,
        "name": "王功赵",
        "gender": "",
        "ethnicity": "",
        "birth": "1982-12",
        "birthplace": "",
        "education": "大学、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "猇亭区副区长（援藏加查县）",
        "current_org": "猇亭区人民政府 / 加查县对口支援",
        "source": "build_猇亭区_data.py"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共加查县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共山南市委员会",
        "location": "西藏自治区山南市加查县"
    },
    {
        "id": 2,
        "name": "加查县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "山南市人民政府",
        "location": "西藏自治区山南市加查县"
    },
    {
        "id": 3,
        "name": "加查县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "山南市人大常委会",
        "location": "西藏自治区山南市加查县"
    },
    {
        "id": 4,
        "name": "政协加查县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协山南市委员会",
        "location": "西藏自治区山南市加查县"
    },
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "加查县委书记，主持县委全面工作"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "加查县委副书记、县长，主持政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "加查县委副书记"},
    {"person_id": 3, "org_id": 2, "title": "副县长（分管生态环保）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管生态环境工作"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管森林草原防火等工作"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管住建等领域"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管林长制、物资交流等工作"},
]

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "侯宝萍作为县委书记与格桑次仁（县长）搭档，共同主持加查县党政全面工作",
        "overlap_org": "中共加查县委员会 / 加查县人民政府",
        "overlap_period": "截至2026年7月"
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(post):
    if "县委书记" in post and "副书记" not in post:
        return ("255,50,50", 20.0)
    elif "县长" in post:
        return ("50,100,255", 20.0)
    elif "常务" in post or "副书记" in post:
        return ("150,100,100", 15.0)
    elif "副县长" in post or "常委" in post:
        return ("100,100,255", 12.0)
    elif "前" in post:
        return ("150,150,150", 10.0)
    else:
        return ("100,100,100", 12.0)

def org_color(typ):
    return {
        "党委": (255,200,200),
        "政府": (200,200,255),
        "人大": (200,255,255),
        "政协": (255,240,200),
        "事业单位": (220,220,220),
        "检察院": (220,220,240),
        "法院": (240,220,220),
    }.get(typ, (200,200,200))

def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 加查县人民政府网站 (jiacha.gov.cn) 及新闻报道")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
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

    # ── GEXF ──────────────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

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
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
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