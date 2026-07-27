#!/usr/bin/env python3
"""神木市 领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-25
信息来源: 神木市人民政府网站 (www.sxsm.gov.cn) 新闻报道

主要人物:
- 段智博: 中共神木市委书记 (原市长)
- 张军: 中共神木市委副书记、市政府市长
"""

import sqlite3
from datetime import datetime

SLUG = "神木市"
TODAY = "2026-07-25"
DB_PATH = "神木市_network.db"
GEXF_PATH = "神木市_network.gexf"

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 核心领导 ──
    {
        "id": 1,
        "name": "段智博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共神木市委书记",
        "current_org": "中共神木市委",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10);韩秀晋领导分工页面提及;神木新闻"
    },
    {
        "id": 2,
        "name": "张军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市人民政府市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗(www.sxsm.gov.cn/zfxxgk/fdzdgknr/ldzc/)"
    },
    # ── 市委常委 ──
    {
        "id": 3,
        "name": "韩秀晋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委、常务副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗(www.sxsm.gov.cn/zfxxgk/fdzdgknr/ldzc/)"
    },
    {
        "id": 4,
        "name": "孟向平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委、副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 5,
        "name": "韩虎忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委",
        "current_org": "中共神木市委",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    {
        "id": 6,
        "name": "张海娥",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委",
        "current_org": "中共神木市委",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    {
        "id": 7,
        "name": "师瑜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委",
        "current_org": "中共神木市委",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    {
        "id": 8,
        "name": "李建鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市委常委",
        "current_org": "中共神木市委",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    # ── 市人大、市政协 ──
    {
        "id": 9,
        "name": "李文江",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市人大常委会主任",
        "current_org": "神木市人大常委会",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    {
        "id": 10,
        "name": "毛晔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市政协主席",
        "current_org": "神木市政协",
        "source": "神木市两优一先表彰大会报道(www.sxsm.gov.cn 2026-07-10)"
    },
    # ── 市政府其他领导 ──
    {
        "id": 11,
        "name": "丁杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市副市长、市公安局党委书记、局长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 12,
        "name": "贺建生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 13,
        "name": "李宏德",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 14,
        "name": "席拓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 15,
        "name": "梁伟华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市副市长",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
    {
        "id": 16,
        "name": "杨三建",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "神木市政府党组成员",
        "current_org": "神木市人民政府",
        "source": "神木市人民政府领导之窗"
    },
]

organizations = [
    {"id": 1, "name": "中共神木市委", "type": "党委", "level": "县级市", "parent": "中共榆林市委", "location": "陕西省榆林市神木市"},
    {"id": 2, "name": "神木市人民政府", "type": "政府", "level": "县级市", "parent": "榆林市人民政府", "location": "陕西省榆林市神木市"},
    {"id": 3, "name": "神木市人大常委会", "type": "人大", "level": "县级市", "parent": "榆林市人大常委会", "location": "陕西省榆林市神木市"},
    {"id": 4, "name": "神木市政协", "type": "政协", "level": "县级市", "parent": "榆林市政协", "location": "陕西省榆林市神木市"},
    {"id": 5, "name": "神木市公安局", "type": "政府", "level": "县级市", "parent": "神木市人民政府", "location": "陕西省榆林市神木市"},
]

positions = [
    # 段智博
    {"person_id": 1, "org_id": 1, "title": "中共神木市委书记", "start_date": "2026年", "end_date": "至今", "rank": "正处级", "note": "原神木市市长升任市委书记，具体任职日期待查"},
    {"person_id": 1, "org_id": 2, "title": "神木市人民政府市长", "start_date": "", "end_date": "2026年", "rank": "正处级", "note": "曾任神木市市长，后升任市委书记"},
    # 张军
    {"person_id": 2, "org_id": 2, "title": "神木市人民政府市长", "start_date": "2026年", "end_date": "至今", "rank": "正处级", "note": "1975年9月生，研究生学历"},
    # 韩秀晋
    {"person_id": 3, "org_id": 2, "title": "神木市委常委、常务副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "1981年3月生，协助段智博分管财政、审计"},
    # 孟向平
    {"person_id": 4, "org_id": 2, "title": "神木市委常委、副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "1972年6月生，负责自然资源、住建等"},
    # 其他市委常委
    {"person_id": 5, "org_id": 1, "title": "神木市委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "神木市委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "神木市委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "神木市委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李文江
    {"person_id": 9, "org_id": 3, "title": "神木市人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 毛晔
    {"person_id": 10, "org_id": 4, "title": "神木市政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 丁杰
    {"person_id": 11, "org_id": 2, "title": "神木市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "神木市公安局党委书记、局长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 其他副市长
    {"person_id": 12, "org_id": 2, "title": "神木市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "神木市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "神木市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "神木市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "神木市政府党组成员", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
]

relationships = [
    # 段智博 ↔ 张军 (党政一把手)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "段智博任神木市委书记、张军任市长，党政主要领导配合", "overlap_org": "神木市党政领导班子", "overlap_period": "2026年至今"},
    # 段智博 ↔ 韩秀晋 (原市长→常务副手的协助关系)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "韩秀晋协助段智博分管市财政局、市审计局", "overlap_org": "神木市人民政府", "overlap_period": ""},
    # 段智博 → 前任书记 (段智博接任书记)
    # 张军 ↔ 韩秀晋 (市长+常务副市长搭档)
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "张军任市长、韩秀晋任常务副市长，政府工作搭档", "overlap_org": "神木市人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "张军任市长、孟向平任副市长，政府工作搭档", "overlap_org": "神木市人民政府", "overlap_period": "2026年至今"},
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "韩秀晋与孟向平同为神木市委常委、副市长", "overlap_org": "中共神木市委", "overlap_period": ""},
    # 市委常委间的同僚关系
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "同为神木市委常委", "overlap_org": "中共神木市委", "overlap_period": ""},
    # 人大和政协领导与市委领导的关系
    {"person_a": 1, "person_b": 9, "type": "党政人大", "context": "市委书记与市人大常委会主任的工作关系", "overlap_org": "神木市", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "党政政协", "context": "市委书记与市政协主席的工作关系", "overlap_org": "神木市", "overlap_period": ""},
    # 副市长间的同僚关系
    {"person_a": 11, "person_b": 12, "type": "同僚", "context": "同为神木市副市长", "overlap_org": "神木市人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 13, "type": "同僚", "context": "同为神木市副市长", "overlap_org": "神木市人民政府", "overlap_period": ""},
    {"person_a": 12, "person_b": 13, "type": "同僚", "context": "同为神木市副市长", "overlap_org": "神木市人民政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 15, "type": "同僚", "context": "同为神木市副市长", "overlap_org": "神木市人民政府", "overlap_period": ""},
    # 张军与人大政协
    {"person_a": 2, "person_b": 9, "type": "政与人", "context": "市长与市人大常委会主任的工作关系", "overlap_org": "神木市", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "政与协", "context": "市长与市政协主席的工作关系", "overlap_org": "神木市", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

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
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "市委书记" in post:
        return ("255,50,50", 20.0)
    elif "市长" in post and "副市长" not in post:
        return ("50,100,255", 20.0)
    elif "常务" in post:
        return ("50,100,255", 15.0)
    elif "副市长" in post or "党组成员" in post:
        return ("100,100,255", 12.0)
    elif "人大主任" in post:
        return ("200,255,255", 15.0)
    elif "政协主席" in post:
        return ("255,240,200", 15.0)
    elif "市委常委" in post:
        return ("150,50,50", 15.0)
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
    print(f"  等级: 县级市")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 神木市人民政府网站 (www.sxsm.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
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

    # Person nodes
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

    # Organization nodes
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
    # person → org edges
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person edges
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
