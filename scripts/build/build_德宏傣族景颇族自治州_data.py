#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Dehong Prefecture leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TMPDIR = os.path.join(BASE, "data/tmp/yunnan_德宏傣族景颇族自治州")
DB_PATH = os.path.join(TMPDIR, "德宏傣族景颇族自治州_network.db")
GEXF_PATH = os.path.join(TMPDIR, "德宏傣族景颇族自治州_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "德宏傣族景颇族自治州"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "王云霏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共德宏州委书记", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/"},
    {"id": 2, "name": "李正环", "gender": "男", "ethnicity": "景颇族",
     "birth": "1971-10", "birthplace": "", "education": "在职硕士",
     "party_join": "", "work_start": "",
     "current_post": "中共德宏州委副书记、州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_F0_0_6HKNIJA577939556D7B843F9B0.htm"},

    # ── Government Leaders ──
    {"id": 3, "name": "郑洪云", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州常务副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 4, "name": "程涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 5, "name": "雪琳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 6, "name": "刘毅鹏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 7, "name": "李飞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 8, "name": "董其然", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 9, "name": "张世影", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州副州长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 10, "name": "马云峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州政府党组成员", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},
    {"id": 11, "name": "罗宏榆", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州政府党组成员、秘书长", "current_org": "德宏州人民政府",
     "source": "https://www.dh.gov.cn/Web/_M15_4O8C9WOJ103266A4FC484246BF_1.htm"},

    # ── Party Committee Leaders ──
    {"id": 12, "name": "李佳锟", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州委常委、组织部部长", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/ (2026-07-13 news)"},
    {"id": 13, "name": "陈力", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州领导", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/ (news reports)"},
    {"id": 14, "name": "尚腊边", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州领导", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/ (2026-07-20 news)"},
    {"id": 15, "name": "杨艳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州领导", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/ (2026-07-20 news)"},
    {"id": 16, "name": "寸待纯", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德宏州领导", "current_org": "中共德宏州委员会",
     "source": "https://www.dh.gov.cn/ (2026-07-28 news)"},

    # ── Predecessors ──
    {"id": 17, "name": "姜山", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任德宏州委书记（2022-2024）", "current_org": "云南省委统战部",
     "source": "public records"},
    {"id": 18, "name": "赵刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任德宏州委书记（~2019-2022）", "current_org": "云南省政府",
     "source": "public records"},
    {"id": 19, "name": "王俊强", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任德宏州委书记（2015-2019，被调查）", "current_org": "",
     "source": "public records"},
]

organizations = [
    {"id": 1, "name": "中共德宏州委员会", "type": "党委", "level": "厅级", "parent": "中共云南省委员会", "location": "云南德宏芒市"},
    {"id": 2, "name": "德宏州人民政府", "type": "政府", "level": "厅级", "parent": "云南省人民政府", "location": "云南德宏芒市"},
    {"id": 3, "name": "德宏州纪律检查委员会", "type": "纪委", "level": "厅级", "parent": "中共云南省纪律检查委员会", "location": "云南德宏芒市"},
    {"id": 4, "name": "德宏州委组织部", "type": "党委部门", "level": "厅级", "parent": "中共德宏州委员会", "location": "云南德宏芒市"},
    {"id": 5, "name": "中共云南省委统战部", "type": "党委部门", "level": "省级", "parent": "中共云南省委员会", "location": "云南昆明"},
    {"id": 6, "name": "云南省政府办公厅", "type": "政府", "level": "省级", "parent": "云南省人民政府", "location": "云南昆明"},
]

positions = [
    # 王云霏 — current
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共德宏州委书记", "start": "", "end": "", "rank": "厅级", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 1, "title": "瑞丽国家重点开发开放试验区党工委书记", "start": "", "end": "", "rank": "厅级", "note": "兼任"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "瑞丽产业协作园区党工委书记", "start": "", "end": "", "rank": "厅级", "note": "兼任"},
    # 李正环 — current
    {"id": 4, "person_id": 2, "org_id": 1, "title": "中共德宏州委副书记", "start": "", "end": "", "rank": "厅级", "note": "现任"},
    {"id": 5, "person_id": 2, "org_id": 2, "title": "德宏州人民政府州长", "start": "", "end": "", "rank": "厅级", "note": "现任"},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "州政府党组书记", "start": "", "end": "", "rank": "厅级", "note": "现任"},
    # Government leadership
    {"id": 7, "person_id": 3, "org_id": 2, "title": "德宏州常务副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 8, "person_id": 4, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 9, "person_id": 5, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 10, "person_id": 6, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 11, "person_id": 7, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 12, "person_id": 8, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 13, "person_id": 9, "org_id": 2, "title": "德宏州副州长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 14, "person_id": 10, "org_id": 2, "title": "德宏州政府党组成员", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 15, "person_id": 11, "org_id": 2, "title": "德宏州政府党组成员、秘书长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # Party committee
    {"id": 16, "person_id": 12, "org_id": 4, "title": "德宏州委常委、组织部部长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 17, "person_id": 13, "org_id": 1, "title": "德宏州领导", "start": "", "end": "", "rank": "", "note": "现任"},
    {"id": 18, "person_id": 14, "org_id": 1, "title": "德宏州领导", "start": "", "end": "", "rank": "", "note": "现任"},
    {"id": 19, "person_id": 15, "org_id": 1, "title": "德宏州领导", "start": "", "end": "", "rank": "", "note": "现任"},
    {"id": 20, "person_id": 16, "org_id": 1, "title": "德宏州领导", "start": "", "end": "", "rank": "", "note": "现任"},
    # Predecessors
    {"id": 21, "person_id": 17, "org_id": 1, "title": "中共德宏州委书记", "start": "2022", "end": "2024-12", "rank": "厅级", "note": "前任"},
    {"id": 22, "person_id": 17, "org_id": 5, "title": "云南省委统战部副部长", "start": "2024-12", "end": "", "rank": "厅级", "note": "调任"},
    {"id": 23, "person_id": 18, "org_id": 1, "title": "中共德宏州委书记", "start": "~2019", "end": "2022-06", "rank": "厅级", "note": "前任"},
    {"id": 24, "person_id": 18, "org_id": 6, "title": "云南省政府秘书长", "start": "2022-07", "end": "", "rank": "厅级", "note": "调任"},
    {"id": 25, "person_id": 19, "org_id": 1, "title": "中共德宏州委书记", "start": "2015", "end": "2019", "rank": "厅级", "note": "前任，被调查"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档", "context": "王云霏（州委书记）与李正环（州长）为当前党政主要领导搭档", "overlap_org": "中共德宏州委员会", "overlap_period": "现任"},
    {"id": 2, "person_a": 17, "person_b": 1, "type": "交接", "context": "姜山→王云霏 德宏州委书记交接（2024-2025年间）", "overlap_org": "中共德宏州委员会", "overlap_period": "2024-2025"},
    {"id": 3, "person_a": 18, "person_b": 17, "type": "交接", "context": "赵刚→姜山 德宏州委书记交接（2022年）", "overlap_org": "中共德宏州委员会", "overlap_period": "2022"},
    {"id": 4, "person_a": 19, "person_b": 18, "type": "交接", "context": "王俊强→赵刚 德宏州委书记交接（~2019年）", "overlap_org": "中共德宏州委员会", "overlap_period": "~2019"},
    {"id": 5, "person_a": 3, "person_b": 2, "type": "上下级", "context": "郑洪云（常务副州长）协助李正环（州长）工作", "overlap_org": "德宏州人民政府", "overlap_period": "现任"},
    {"id": 6, "person_a": 12, "person_b": 1, "type": "上下级", "context": "李佳锟（组织部部长）受王云霏（州委书记）领导", "overlap_org": "中共德宏州委员会", "overlap_period": "现任"},
]


# ── BUILD SQLite DATABASE ────────────────────────────────────────────

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
    print(f"  等级: 地级市/自治州")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 德宏州人民政府官方网站 (dh.gov.cn) 及新闻报道")
    print("=" * 60)

    # Remove existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    posc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {pc} 人")
    print(f"  机构: {oc} 个")
    print(f"  任职: {posc} 条")
    print(f"  关系: {rc} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        p = post or ""
        if "州委书记" in p and "副书记" not in p:
            return ("255,50,50", 20.0)
        elif "州长" in p:
            return ("50,100,255", 20.0)
        elif "常务" in p or "副书记" in p:
            return ("50,100,255", 15.0)
        elif "副州长" in p or "常委" in p:
            return ("100,100,255", 12.0)
        elif "前任" in p:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "纪委": ("255,165,0"),
            "党委部门": ("220,200,200"),
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
        lines.append('          <attvalue for="0" value="person"/>')
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

    total_nodes = len(persons) + len(organizations)
    print(f"\n  GEXF: {GEXF_PATH}")
    print(f"  节点: {total_nodes} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


# Fix: rename color to person_color to avoid conflict
def color(post):
    return person_color(post)


if __name__ == "__main__":
    run_build()