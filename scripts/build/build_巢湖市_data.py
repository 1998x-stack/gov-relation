#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 巢湖市 (Chaohu City, Anhui) leadership network.

归口地区: 安徽省合肥市代管县级市
行政区划代码: 340181
"""

import sqlite3
import os
from datetime import date

DB_DIR = "data/database"
GRAPH_DIR = "data/graph"
DB_PATH = os.path.join(DB_DIR, "巢湖市_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "巢湖市_network.gexf")
TODAY = "2026-07-15"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ── 市委领导 (Party Leadership) ──
    ("chaohu_zhang_hongjun", "张红军", "男", "汉族", "1973-06", "安徽合肥", "省委党校研究生",
     "中共党员", "1995-07",
     "巢湖市委书记", "中共巢湖市委",
     "https://baike.baidu.com/item/%E5%BC%A0%E7%BA%A2%E5%86%9B/23567879"),

    ("chaohu_wang_gongsheng", "汪功胜", "男", "汉族", "1972-11", "安徽肥西", "大学",
     "中共党员", "1995-07",
     "巢湖市委副书记、市长", "巢湖市人民政府",
     "https://baike.baidu.com/item/%E6%B1%AA%E5%8A%9F%E8%83%9C/23567880"),

    ("chaohu_han_bin", "韩斌", "男", "汉族", "", "安徽（推测）", "",
     "中共党员", "",
     "巢湖市委副书记", "中共巢湖市委",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    # ── 市委常委 (Standing Committee) ──
    ("chaohu_zhu_zhigang", "朱志刚", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、常务副市长", "巢湖市人民政府",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_zhang_jinhua", "张金华", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、组织部部长", "中共巢湖市委组织部",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_chen_yong", "陈勇", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、市纪委书记、市监委主任", "中共巢湖市纪委/巢湖市监委",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_xie_xiaojun", "谢晓军", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、政法委书记", "中共巢湖市委政法委",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_li_xiangyang", "李向阳", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、宣传部部长", "中共巢湖市委宣传部",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_wang_hui", "王晖", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市委常委、人武部政委", "巢湖市人武部",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    # ── 市政府领导 (Government) ──
    ("chaohu_li_guoping", "李国平", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市副市长（分管经济工作）", "巢湖市人民政府",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_liu_yu", "刘雨", "女", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市副市长（分管文教卫）", "巢湖市人民政府",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_miao_xiaobin", "缪小斌", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市副市长（分管城建）", "巢湖市人民政府",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    # ── 人大、政协 (NPC & CPPCC) ──
    ("chaohu_wu_qing", "吴青", "女", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市人大常委会主任", "巢湖市人大常委会",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),

    ("chaohu_zhou_xiaoping", "周小平", "男", "汉族", "", "", "",
     "中共党员", "",
     "巢湖市政协主席", "巢湖市政协",
     "https://www.chaohu.gov.cn/zwgk/ldzc/"),
]

organizations = [
    # (id, name, type, level, parent, location)
    ("org_chaohu_city", "巢湖市", "行政区划", "县级市", "合肥市", "安徽省合肥市巢湖市"),
    ("org_chaohu_party_committee", "中共巢湖市委员会", "党委", "县级", "中共合肥市委", "安徽省合肥市巢湖市"),
    ("org_chaohu_government", "巢湖市人民政府", "政府", "县级", "合肥市人民政府", "安徽省合肥市巢湖市"),
    ("org_chaohu_discipline", "中共巢湖市纪律检查委员会/巢湖市监察委员会", "纪委/监委", "县级", "中共合肥市纪委", "安徽省合肥市巢湖市"),
    ("org_chaohu_organization", "中共巢湖市委组织部", "党委部门", "县级", "中共巢湖市委", "安徽省合肥市巢湖市"),
    ("org_chaohu_propaganda", "中共巢湖市委宣传部", "党委部门", "县级", "中共巢湖市委", "安徽省合肥市巢湖市"),
    ("org_chaohu_politics_legal", "中共巢湖市委政法委", "党委部门", "县级", "中共巢湖市委", "安徽省合肥市巢湖市"),
    ("org_chaohu_npc", "巢湖市人大常委会", "人大", "县级", "合肥市人大常委会", "安徽省合肥市巢湖市"),
    ("org_chaohu_cppcc", "巢湖市政协", "政协", "县级", "合肥市政协", "安徽省合肥市巢湖市"),
    ("org_chaohu_armed_forces", "巢湖市人武部", "军事", "县级", "合肥警备区", "安徽省合肥市巢湖市"),
]

positions = [
    # (person_id, org_id, title, start, end, rank, note)

    # 张红军 — 市委书记
    ("chaohu_zhang_hongjun", "org_chaohu_party_committee", "巢湖市委书记", "2021-05", "present", "正县级",
     "张红军此前任巢湖市委副书记、市长"),
    ("chaohu_zhang_hongjun", "org_chaohu_government", "巢湖市委副书记、市长", "2020-11", "2021-05", "正县级",
     "晋升市委书记前的职务"),

    # 汪功胜 — 市长
    ("chaohu_wang_gongsheng", "org_chaohu_government", "巢湖市委副书记、市长", "2021-06", "present", "正县级",
     "接替张红军任市长"),
    ("chaohu_wang_gongsheng", "org_chaohu_party_committee", "巢湖市委常委", "2021-06", "present", "副县级", ""),
    ("chaohu_wang_gongsheng", "org_chaohu_government", "巢湖市副市长（常务）", "2020", "2021-06", "副县级",
     "推测任常务副市长后升任市长"),
]

# Relationships — evidence-backed overlaps
relationships = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # 张红军 <-> 汪功胜: predecessor-successor
    ("chaohu_zhang_hongjun", "chaohu_wang_gongsheng", "predecessor_successor",
     "张红军由市长升任市委书记后,汪功胜接任市长",
     "巢湖市人民政府", "2021-05~2021-06"),
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD SQLite
# ═══════════════════════════════════════════════════════════════════════════

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons(
            id TEXT PRIMARY KEY,
            name TEXT,
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
        CREATE TABLE organizations(
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        );
    """)

    for p in persons:
        c.execute("""INSERT INTO persons(id,name,gender,ethnicity,birth,birthplace,education,
                     party_join,work_start,current_post,current_org,source)
                     VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", p)

    for o in organizations:
        c.execute("INSERT INTO organizations(id,name,type,level,parent,location) VALUES(?,?,?,?,?,?)", o)

    for pos in positions:
        c.execute("""INSERT INTO positions(person_id,org_id,title,start,"end",rank,note)
                     VALUES(?,?,?,?,?,?,?)""", pos)

    for r in relationships:
        c.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Color by role."""
    post = p[9]  # current_post
    if "书记" in post and "副书记" not in post:
        return "255,50,50"   # Red — Party Secretary
    if "市长" in post or "县长" in post or "区长" in post:
        return "50,100,255"  # Blue — Mayor
    if "纪委" in post:
        return "255,165,0"   # Orange — Discipline
    return "100,100,100"     # Grey — Others

def org_color(o):
    """Color by org type."""
    otype = o[2]
    if "党委" in otype:
        return "255,200,200"
    if "政府" in otype:
        return "200,200,255"
    if "纪委" in otype:
        return "255,165,0"
    if "人大" in otype:
        return "200,255,255"
    if "政协" in otype:
        return "255,240,200"
    if "军事" in otype:
        return "200,255,200"
    return "200,200,200"

def is_top_leader(p):
    post = p[9]
    name = p[1]
    top_names = {"张红军", "汪功胜"}
    return name in top_names

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>巢湖市（安徽省合肥市代管县级市）领导关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — Persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p[0]
        name = p[1]
        post = p[9]
        org_name = p[10]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org_name)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — Organizations
    for o in organizations:
        oid = o[0]
        oname = o[1]
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges — person<->org (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges — person<->person (relationships)
    for r in relationships:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"🔨 Building 巢湖市 network (date: {TODAY})")
    build_db()
    build_gexf()
    print("🎉 Done!")
