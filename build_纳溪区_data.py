#!/usr/bin/env python3
"""纳溪区 领导班子工作关系网络 — 数据构建脚本"""

import sqlite3
import os

SLUG = "纳溪区"
TODAY = "2026-07-26"
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data", "database", f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", f"{SLUG}_network.gexf")

PERSONS = [
]

ORGANIZATIONS = [
]

POSITIONS = [
]

RELATIONSHIPS = [
]

ORGS = [
    (1, "中共泸州市纳溪区委员会", "党委", "市辖区", "中共泸州市委", "泸州市纳溪区"),
    (2, "泸州市纳溪区人民政府", "政府", "市辖区", "泸州市人民政府", "泸州市纳溪区"),
    (3, "泸州市纳溪区人大常委会", "人大", "市辖区", "泸州市人大常委会", "泸州市纳溪区"),
    (4, "泸州市纳溪区政协委员会", "政协", "市辖区", "泸州市政协", "泸州市纳溪区"),
    (5, "泸州市城市管理行政执法局", "政府", "市直", "泸州市人民政府", "泸州市"),
    (6, "中国（四川）自由贸易试验区川南临港片区", "政府", "正县级", "泸州市人民政府", "泸州市龙马潭区"),
    (7, "泸州市纳溪区公安局", "政府", "区级", "纳溪区人民政府", "泸州市纳溪区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note
    (1, 1, "纳溪区委书记", "2024-09", "", "正县级", "前身为纳溪区长"),
    (1, 2, "纳溪区区长", "2021.12", "2024.09", "正县级", "升任区委书记"),
    (2, 2, "纳溪区区长", "2025.01", "", "正县级", "2024.12代理, 2025.01正式当选"),
    (2, 2, "纳溪区委常委、常务副区长", "2021.07", "2024.06", "副县级", "升任区长"),
    (3, 1, "纳溪区委副书记", "~2021", "2026.06", "副县级", "调离"),
    (3, 5, "泸州市城管执法局局长", "2026.06", "", "正县级", "从纳溪区调任"),
    (4, 3, "纳溪区人大常委会主任", "", "", "正县级", "在职"),
    (5, 4, "纳溪区政协主席", "", "", "正县级", "在职"),
    (6, 2, "纳溪区委常委、常务副区长", "", "", "副县级", "最年轻的班子成员"),
    (7, 1, "纳溪区委书记", "2020.11", "2024.09", "正县级", "前任区委书记"),
    (7, 6, "自贸区川南临港片区党工委书记", "2024.09", "", "正县级", "调任去向"),
    (8, 7, "纳溪区副区长、公安分局局长", "", "", "副县级", "兼任公安局长"),
    (9, 2, "纳溪区副区长", "", "", "副县级", "分管不详"),
    (10, 2, "纳溪区副区长", "", "", "副县级", "分管不详"),
    (11, 2, "纳溪区副区长", "", "", "副县级", "分管不详"),
    (12, 2, "纳溪区副区长", "", "", "副县级", "1988.07生"),
    (13, 1, "纳溪区委副书记", "", "", "正县级（拟）", "2025年公示"),
    (14, 2, "纳溪区副区长（挂职）", "", "", "挂职", "挂职干部"),
]

RELATIONS = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    (1, 2, "党政搭档", "区委书记+区长搭班子", "纳溪区委区政府", "2024.12至今"),
    (1, 7, "前后任", "袁维荣接替谭荣兵任区委书记", "纳溪区委", "2024.09"),
    (1, 3, "同事", "袁维荣与刘彬在纳溪区委同任常委", "纳溪区委", "2021~2026"),
    (2, 4, "党政人大", "区长与区人大主任的常规工作关系", "纳溪区政府/人大", "2025.01至今"),
    (1, 6, "上下级", "袁维荣与向来富（隶属区委常委）", "纳溪区委", "至今"),
    (7, 1, "前任-继任", "谭荣兵—袁维荣，前后任区委书记", "纳溪区委", "2024.09交接"),
    (3, 13, "同事", "刘彬与唐浩然的可能的交接关系", "纳溪区委", "2025~2026"),
]

# ── data/database/ ├─ data/graph/ ──────────────────────────────
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)


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


def esc(s):
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "区委书记" in post and "前任" not in post:
        return ("255,50,50", 20.0)
    elif "区长" in post and "副" not in post and "前任" not in post:
        return ("50,100,255", 20.0)
    elif "区委副书记" in post:
        return ("150,50,50", 15.0)
    elif "区政协主席" in post:
        return ("255,240,200", 15.0)
    elif "区人大常委会主任" in post and "副" not in post:
        return ("200,255,255", 15.0)
    elif "常务副区长" in post:
        return ("50,100,255", 15.0)
    elif "同事们" in post:
        return ("100,150,255", 12.0)  # other CCP committee members
    elif "副区长" in post:
        return ("100,100,255", 12.0)
    elif "前任" in post:
        return ("150,150,150", 10.0)
    else:
        return ("100,100,100", 12.0)


def org_color(typ):
    return {
        "党委": ("255,200,200"),
        "政府": ("200,200,255"),
        "人大": ("200,255,255"),
        "政协": ("255,240,200"),
    }.get(typ, ("200,200,200"))


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 泸州市人民政府网、百度百科、新闻报道")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in PERS:
        conn.execute(
            f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})",
            [p[i] if i < len(p) else "" for i in range(len(cols_p))])

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in ORGS:
        conn.execute(
            f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})",
            [str(o[i]) if i < len(o) else "" for i in range(len(cols_o))])

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in POSITIONS:
        conn.execute(
            f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})",
            [str(pos[i]) if i < len(pos) else "" for i in range(len(cols_pos))])

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in RELS:
        conn.execute(
            f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})",
            [str(r[i]) if i < len(r) else "" for i in range(len(cols_r))])

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(PERS)} 人")
    print(f"  机构: {len(ORGS)} 个")
    print(f"  任职: {len(POSITIONS)} 条")
    print(f"  关系: {len(RELS)} 条")

    # ── GEXF ──
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

    for p in PERS:
        c, sz = person_color(p[9])
        lines.append(f'      <node id="p{p[0]}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p[4])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p[11])}"/>')
        lines.append('        </attvalues>')
        r_, g_, b_ = c.split(",")
        lines.append(f'        <viz:color r="{r_}" g="{g_}" b="{b_}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGS:
        c = org_color(o[2])
        lines.append(f'      <node id="o{o[0]}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        r_, g_, b_ = c.split(",")
        lines.append(f'        <viz:color r="{r_}" g="{g_}" b="{b_}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos[0]}" target="o{pos[1]}" '
            f'label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[6])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELS:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r[0]}" target="p{r[1]}" '
            f'label="{esc(r[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r[2])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r[4])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r[5])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(PERS) + len(ORGS)} 个")
    print(f"  边: {eid} 条")
    print(f"\n{SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()