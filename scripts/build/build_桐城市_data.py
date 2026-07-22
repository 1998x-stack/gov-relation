#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 桐城市 (Tongcheng City) leadership network.

桐城市 (Tongcheng) is a county-level city under 安庆市 (Anqing), 安徽省 (Anhui Province).
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "桐城市_network.db")
GEXF_PATH = os.path.join(BASE, "桐城市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "刘婉贞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共桐城市委书记", "current_org": "中共桐城市委员会",
     "source": "https://www.tongcheng.gov.cn"},

    {"id": 2, "name": "王静", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市人民政府市长", "current_org": "桐城市人民政府",
     "source": "https://www.tongcheng.gov.cn"},

    # ── Predecessors ──
    {"id": 3, "name": "章周中", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E7%AB%A0%E5%91%A8%E4%B8%AD"},

    {"id": 4, "name": "徐雄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%BE%90%E9%9B%84"},

    # ── Other Government Leaders ──
    {"id": 5, "name": "桂稳成", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市委常委、常务副市长", "current_org": "桐城市人民政府",
     "source": ""},

    {"id": 6, "name": "章友厚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市委常委、组织部部长", "current_org": "中共桐城市委员会",
     "source": ""},

    {"id": 7, "name": "殷锐", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市委常委、宣传部部长", "current_org": "中共桐城市委员会",
     "source": ""},

    {"id": 8, "name": "汪杰贤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市委常委、纪委书记", "current_org": "中共桐城市纪律检查委员会",
     "source": ""},

    {"id": 9, "name": "祖聪", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市委常委、政法委书记", "current_org": "中共桐城市委员会",
     "source": ""},

    {"id": 10, "name": "金天柱", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市人民政府副市长、公安局局长", "current_org": "桐城市人民政府",
     "source": ""},

    # ── Other Deputy Mayors ──
    {"id": 11, "name": "占娜", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桐城市人民政府副市长", "current_org": "桐城市人民政府",
     "source": ""},

    {"id": 12, "name": "张树", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "桐城市人民政府副市长", "current_org": "桐城市人民政府",
     "source": ""},

    {"id": 13, "name": "卢俊霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "桐城市人民政府副市长（挂职）", "current_org": "桐城市人民政府",
     "source": ""},

    # ── Key Organizations ──
    {"id": 14, "name": "中共桐城市委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 15, "name": "桐城市人民政府", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 16, "name": "桐城市人民代表大会常务委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 17, "name": "中国人民政治协商会议桐城市委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 18, "name": "中共桐城市纪律检查委员会", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 19, "name": "桐城市人民法院", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},

    {"id": 20, "name": "桐城市人民检察院", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "", "current_org": "",
     "source": ""},
]

organizations = [
    {"id": 1, "name": "中共桐城市委员会", "type": "党委", "level": "县级", "parent": "中共安庆市委", "location": "安徽省安庆市桐城市"},
    {"id": 2, "name": "桐城市人民政府", "type": "政府", "level": "县级", "parent": "安庆市人民政府", "location": "安徽省安庆市桐城市"},
    {"id": 3, "name": "中共桐城市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共安庆市纪委", "location": "安徽省安庆市桐城市"},
    {"id": 4, "name": "桐城市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "安庆市人大常委会", "location": "安徽省安庆市桐城市"},
    {"id": 5, "name": "中国人民政治协商会议桐城市委员会", "type": "政协", "level": "县级", "parent": "安庆市政协", "location": "安徽省安庆市桐城市"},
    {"id": 6, "name": "桐城市人民法院", "type": "司法", "level": "县级", "parent": "安庆市中级人民法院", "location": "安徽省安庆市桐城市"},
    {"id": 7, "name": "桐城市人民检察院", "type": "司法", "level": "县级", "parent": "安庆市人民检察院", "location": "安徽省安庆市桐城市"},
    {"id": 8, "name": "中共安庆市委", "type": "党委", "level": "地市级", "parent": "中共安徽省委", "location": "安徽省安庆市"},
    {"id": 9, "name": "安庆市人民政府", "type": "政府", "level": "地市级", "parent": "安徽省人民政府", "location": "安徽省安庆市"},
]

positions = [
    # 刘婉贞
    {"person_id": 1, "org_id": 1, "title": "中共桐城市委书记", "start": "", "end": "present", "rank": "正处级", "note": "confirmed via official website 2026-07"},

    # 王静
    {"person_id": 2, "org_id": 2, "title": "桐城市人民政府市长", "start": "", "end": "present", "rank": "正处级", "note": "confirmed via official website 2026-07"},

    # 桂稳成 - 常务副市长
    {"person_id": 5, "org_id": 2, "title": "桐城市人民政府常务副市长", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},
    {"person_id": 5, "org_id": 1, "title": "桐城市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 章友厚 - 组织部部长
    {"person_id": 6, "org_id": 1, "title": "桐城市委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},

    # 殷锐 - 宣传部部长
    {"person_id": 7, "org_id": 1, "title": "桐城市委常委、宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},

    # 汪杰贤 - 纪委书记
    {"person_id": 8, "org_id": 3, "title": "桐城市纪委书记、监委主任", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},
    {"person_id": 8, "org_id": 1, "title": "桐城市委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 祖聪 - 政法委书记
    {"person_id": 9, "org_id": 1, "title": "桐城市委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},

    # 金天柱 - 副市长兼公安局长
    {"person_id": 10, "org_id": 2, "title": "桐城市人民政府副市长、公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "confirmed via official website"},

    # 占娜 - 副市长
    {"person_id": 11, "org_id": 2, "title": "桐城市人民政府副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张树 - 副市长
    {"person_id": 12, "org_id": 2, "title": "桐城市人民政府副市长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 卢俊霞 - 挂职副市长
    {"person_id": 13, "org_id": 2, "title": "桐城市人民政府副市长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # 市委书记 - 市长（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "刘婉贞任桐城市委书记，王静任桐城市长，为党政主要负责人", "overlap_org": "中共桐城市委员会/桐城市人民政府", "overlap_period": "present"},

    # 市委书记 - 常务副市长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "桂稳成作为常委、常务副市长，在书记领导下工作", "overlap_org": "中共桐城市委员会", "overlap_period": "present"},

    # 市长 - 常务副市长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "桂稳成作为常务副市长，协助市长工作", "overlap_org": "桐城市人民政府", "overlap_period": "present"},

    # 市委书记 - 纪委书记
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "汪杰贤作为纪委书记，在市委领导下工作", "overlap_org": "中共桐城市委员会", "overlap_period": "present"},

    # 市委书记 - 组织部长
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "章友厚作为组织部长，在书记领导下负责干部工作", "overlap_org": "中共桐城市委员会", "overlap_period": "present"},

    # 市委书记 - 政法委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "祖聪作为政法委书记，在书记领导下工作", "overlap_org": "中共桐城市委员会", "overlap_period": "present"},

    # 市长 - 副市长（分管）
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "金天柱作为副市长兼公安局长，在市长领导下工作", "overlap_org": "桐城市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "占娜作为副市长，在市长领导下工作", "overlap_org": "桐城市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "张树作为副市长，在市长领导下工作", "overlap_org": "桐城市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "卢俊霞作为挂职副市长，在市长领导下工作", "overlap_org": "桐城市人民政府", "overlap_period": "present"},
]


# ── BUILD SQLite ──────────────────────────────────────────────────

def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"],
                   p["birth"], p["birthplace"], p["education"],
                   p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite database written: {DB_PATH}")


# ── BUILD GEXF ────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_is_party_secretary(p):
    return "书记" in p["current_post"] and "纪委" not in p["current_post"] and "政法委" not in p["current_post"]

def person_is_gov_leader(p):
    return "市长" in p["current_post"] or "副市长" in p["current_post"] or "县长" in p["current_post"] or "区长" in p["current_post"]

def person_is_discipline(p):
    return "纪委" in p["current_post"] or "监委" in p["current_post"]

def person_color(p):
    if person_is_party_secretary(p):
        return "255,50,50"
    elif person_is_gov_leader(p):
        return "50,100,255"
    elif person_is_discipline(p):
        return "255,165,0"
    else:
        return "100,100,100"

def person_size(p):
    if p["current_post"] in ("中共桐城市委书记", "桐城市人民政府市长"):
        return "20.0"
    elif p["current_post"].startswith("桐城市"):
        return "12.0"
    else:
        return "8.0"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "纪委":
        return "255,200,150"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    else:
        return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>桐城市（安徽省安庆市）领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes: node
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="name" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('      <attribute id="3" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Attributes: edge
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="relation" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: persons ──
    lines.append('    <nodes>')
    for p in persons:
        if not p["name"]:
            continue
        c = person_color(p)
        sz = person_size(p)
        pid = f"p{p['id']}"
        ntype = "person"
        role = esc(p["current_post"])
        org = esc(p["current_org"])
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{ntype}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["name"])}"/>')
        lines.append(f'          <attvalue for="2" value="{role}"/>')
        lines.append(f'          <attvalue for="3" value="{org}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: organizations ──
    for o in organizations:
        c = org_color(o)
        oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["name"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Position edges: person -> organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        title = esc(pos["title"])
        lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="worked_at" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{title}"/>')
        lines.append(f'          <attvalue for="2" value="{title} at {esc(pos["start"] or "unknown")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Relationship edges: person <-> person
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        ctx = esc(r["context"])
        rtype = esc(r["type"])
        lines.append(f'      <edge id="{eid}" source="{pa}" target="{pb}" label="relationship" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{rtype}"/>')
        lines.append(f'          <attvalue for="2" value="{ctx}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph written: {GEXF_PATH}")


# ── MAIN ──────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("桐城市（安徽省安庆市）领导班子工作关系网络")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    build_db()
    build_gexf()

    # Stats
    real_persons = [p for p in persons if p["name"]]
    print(f"\n📊 Summary:")
    print(f"  Persons: {len(real_persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB size: {os.path.getsize(DB_PATH)} bytes")
    print(f"  GEXF size: {os.path.getsize(GEXF_PATH)} bytes")
    print("✅ Done.")


if __name__ == "__main__":
    main()
