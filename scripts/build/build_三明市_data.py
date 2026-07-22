#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Sanming City (三明市), Fujian Province.

Covers: Party Secretary (市委书记), Mayor (市长), key leadership,
predecessor/successor chains, and the city-level leadership network.

Sources:
- Wikipedia: 三明市 leadership information
- Baidu Baike: biographical data
- Sanming City Government website (www.sm.gov.cn)

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/三明市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/三明市_network.gexf")
PERSONS_DIR = os.path.join(BASE, "data/persons")

# as_of date for current data
AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 李春 — 三明市委书记 (女，回族)
    {"id":1,"name":"李春","gender":"女","ethnicity":"回族","birth":"1969-03","birthplace":"安徽亳州","education":"","party_join":"","work_start":"","current_post":"三明市委书记","current_org":"中共三明市委员会","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 陈岳峰 — 三明市市长
    {"id":2,"name":"陈岳峰","gender":"男","ethnicity":"汉族","birth":"1973-10","birthplace":"福建漳浦","education":"","party_join":"","work_start":"","current_post":"三明市市长","current_org":"三明市人民政府","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},

    # ── Other current city leaders ──
    # 杨兴忠 — 三明市人大常委会主任
    {"id":3,"name":"杨兴忠","gender":"男","ethnicity":"汉族","birth":"1969-11","birthplace":"福建永安","education":"","party_join":"","work_start":"","current_post":"三明市人大常委会主任","current_org":"三明市人大常委会","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 陈云水 — 三明市政协主席
    {"id":4,"name":"陈云水","gender":"男","ethnicity":"汉族","birth":"1969-09","birthplace":"福建云霄","education":"","party_join":"","work_start":"","current_post":"三明市政协主席","current_org":"政协三明市委员会","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 黄晓峰 — 三明市监察委员会主任
    {"id":5,"name":"黄晓峰","gender":"男","ethnicity":"汉族","birth":"1979-03","birthplace":"福建南安","education":"","party_join":"","work_start":"","current_post":"三明市监察委员会主任","current_org":"三明市监察委员会","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},

    # ── Predecessors — 市委书记 ──
    # 李兴湖 — 前任市委书记 (2023.07-2024.11), 后升任福建省副省长, 现任交通运输部副部长
    {"id":6,"name":"李兴湖","gender":"男","ethnicity":"汉族","birth":"1970-07","birthplace":"福建邵武","education":"","party_join":"","work_start":"","current_post":"交通运输部副部长（原三明市委书记）","current_org":"中华人民共和国交通运输部","source":"https://zh.wikipedia.org/wiki/%E6%9D%8E%E5%85%B4%E6%B9%96"},
    # 黄如欣 — 前任市委书记 (2022.07-2023.07), 现任福建省政协副主席
    {"id":7,"name":"黄如欣","gender":"男","ethnicity":"汉族","birth":"1966-09","birthplace":"福建南安","education":"","party_join":"","work_start":"","current_post":"福建省政协副主席（原三明市委书记）","current_org":"福建省政协","source":"https://zh.wikipedia.org/wiki/%E9%BB%84%E5%A6%82%E6%AC%A3"},
    # 余红胜 — 前任市委书记 (2021.07-2022.07)
    {"id":8,"name":"余红胜","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 林兴禄 — 前任市委书记 (2019.03-2021.07)
    {"id":9,"name":"林兴禄","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 杜源生 — 前任市委书记 (2016.07-2019.03)
    {"id":10,"name":"杜源生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 邓本元 — 前任市委书记 (2013.02-2016.07)
    {"id":11,"name":"邓本元","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},

    # ── Predecessors — 市长 ──
    # 李春 — 前任市长 (2021.08-2024.11), 升任市委书记
    # (same person as person 1)
    # 余红胜 — 前任市长 (2016.08-2021.08), 后升任市委书记
    # (same person as person 8)
    # 杜源生 — 前任市长 (2013.02-2016.08), 后升任市委书记
    # (same person as person 10)
    # 邓本元 — 前任市长 (2011.07-2013.02), 后升任市委书记
    # (same person as person 11)
    # 刘道崎 — 前任市长 (2007.06-2011.07)
    {"id":12,"name":"刘道崎","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 张健 — 前任市长 (2003.07-2007.06)
    {"id":13,"name":"张健","gender":"男","ethnicity":"汉族","birth":"1956-03","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 叶继革 — 前任市长 (1999.05-2003.07), 后升任市委书记
    {"id":14,"name":"叶继革","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"","source":"https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82"},
    # 蔡奇 — 前任市长 (1997.11-1999.05)
    {"id":15,"name":"蔡奇","gender":"男","ethnicity":"汉族","birth":"1955-12","birthplace":"福建尤溪","education":"","party_join":"1975-08","work_start":"1973-03","current_post":"中央政治局委员、北京市委书记（原三明市长）","current_org":"中共中央","source":"https://baike.baidu.com/item/%E8%94%A1%E5%A5%87/175804"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Sanming city core
    {"id":1,"name":"中共三明市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省三明市"},
    {"id":2,"name":"三明市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省三明市"},
    {"id":3,"name":"三明市人大常委会","type":"人大","level":"地级","parent":"","location":"福建省三明市"},
    {"id":4,"name":"政协三明市委员会","type":"政协","level":"地级","parent":"","location":"福建省三明市"},
    {"id":5,"name":"三明市监察委员会","type":"党委","level":"地级","parent":"","location":"福建省三明市"},
    {"id":6,"name":"中共福建省纪律检查委员会","type":"党委","level":"省级","parent":"中共福建省委员会","location":"福建省福州市"},

    # Provincial / Central orgs for leaders who moved on
    {"id":7,"name":"福建省人民政府","type":"政府","level":"省级","parent":"","location":"福建省福州市"},
    {"id":8,"name":"福建省政协","type":"政协","level":"省级","parent":"","location":"福建省福州市"},
    {"id":9,"name":"中华人民共和国交通运输部","type":"政府","level":"国家级","parent":"国务院","location":"北京市"},
    {"id":10,"name":"中共中央","type":"党委","level":"国家级","parent":"","location":"北京市"},

    # Sanming subordinate districts/counties
    {"id":11,"name":"三元区人民政府","type":"政府","level":"县级","parent":"三明市人民政府","location":"福建省三明市三元区"},
    {"id":12,"name":"沙县区人民政府","type":"政府","level":"县级","parent":"三明市人民政府","location":"福建省三明市沙县区"},
    {"id":13,"name":"永安市人民政府","type":"政府","level":"县级","parent":"三明市人民政府","location":"福建省三明市永安市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 李春 — Party Secretary (previously Mayor)
    {"person_id":1,"org_id":1,"title":"三明市委书记","start":"2024-11","end":"present","rank":"正厅级","note":"2024年11月任市委书记，此前为市长"},
    {"person_id":1,"org_id":2,"title":"三明市市长","start":"2021-08","end":"2024-11","rank":"正厅级","note":"2021年8月任代市长，后当选市长"},

    # 陈岳峰 — Mayor
    {"person_id":2,"org_id":2,"title":"三明市市长","start":"2024-11","end":"present","rank":"正厅级","note":"2024年11月任代市长"},

    # 杨兴忠 — 人大主任
    {"person_id":3,"org_id":3,"title":"三明市人大常委会主任","start":"2026-01","end":"present","rank":"正厅级","note":"2026年1月当选"},

    # 陈云水 — 政协主席
    {"person_id":4,"org_id":4,"title":"三明市政协主席","start":"2025-05","end":"present","rank":"正厅级","note":"2025年5月就任"},

    # 黄晓峰 — 监委主任
    {"person_id":5,"org_id":5,"title":"三明市监察委员会主任","start":"2026-01","end":"present","rank":"正厅级","note":"2026年1月就任"},

    # Predecessors — 市委书记
    {"person_id":6,"org_id":1,"title":"三明市委书记","start":"2023-07","end":"2024-11","rank":"正厅级","note":"后升任福建省副省长，现任交通运输部副部长"},
    {"person_id":7,"org_id":1,"title":"三明市委书记","start":"2022-07","end":"2023-07","rank":"正厅级","note":"此前任福建省卫健委主任；后任福建省政协副主席"},
    {"person_id":8,"org_id":1,"title":"三明市委书记","start":"2021-07","end":"2022-07","rank":"正厅级","note":"此前任三明市市长"},
    {"person_id":9,"org_id":1,"title":"三明市委书记","start":"2019-03","end":"2021-07","rank":"正厅级","note":""},
    {"person_id":10,"org_id":1,"title":"三明市委书记","start":"2016-07","end":"2019-03","rank":"正厅级","note":"此前任三明市市长"},
    {"person_id":11,"org_id":1,"title":"三明市委书记","start":"2013-02","end":"2016-07","rank":"正厅级","note":"此前任三明市市长"},

    # Predecessors — 市长
    {"person_id":12,"org_id":2,"title":"三明市市长","start":"2007-06","end":"2011-07","rank":"正厅级","note":""},
    {"person_id":13,"org_id":2,"title":"三明市市长","start":"2003-07","end":"2007-06","rank":"正厅级","note":""},
    {"person_id":14,"org_id":2,"title":"三明市市长","start":"1999-05","end":"2003-07","rank":"正厅级","note":"后任三明市委书记"},
    {"person_id":15,"org_id":2,"title":"三明市市长","start":"1997-11","end":"1999-05","rank":"正厅级","note":"后任福建省副省长、北京市委书记、中央政治局委员"},

    # 李兴湖 — 福建省副省长、交通运输部副部长
    {"person_id":6,"org_id":7,"title":"福建省副省长","start":"2024-05","end":"2026-01","rank":"副省级","note":""},
    {"person_id":6,"org_id":9,"title":"交通运输部副部长","start":"2025-12","end":"present","rank":"副部级","note":""},

    # 黄如欣 — 福建省政协副主席
    {"person_id":7,"org_id":8,"title":"福建省政协副主席","start":"2023-01","end":"present","rank":"副省级","note":""},

    # 蔡奇 — 后续职务
    {"person_id":15,"org_id":10,"title":"中央政治局委员、北京市委书记","start":"2022-10","end":"present","rank":"国家级副职","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Succession — 市委书记
    {"person_a":1,"person_b":6,"type":"predecessor_successor","context":"李春接替李兴湖任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2024-11","strength":"strong","direction":"person_to_other"},
    {"person_a":6,"person_b":7,"type":"predecessor_successor","context":"李兴湖接替黄如欣任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2023-07","strength":"strong","direction":"person_to_other"},
    {"person_a":7,"person_b":8,"type":"predecessor_successor","context":"黄如欣接替余红胜任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2022-07","strength":"strong","direction":"person_to_other"},
    {"person_a":8,"person_b":9,"type":"predecessor_successor","context":"余红胜接替林兴禄任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2021-07","strength":"strong","direction":"person_to_other"},
    {"person_a":9,"person_b":10,"type":"predecessor_successor","context":"林兴禄接替杜源生任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2019-03","strength":"strong","direction":"person_to_other"},
    {"person_a":10,"person_b":11,"type":"predecessor_successor","context":"杜源生接替邓本元任三明市委书记","overlap_org":"中共三明市委员会","overlap_period":"2016-07","strength":"strong","direction":"person_to_other"},
    {"person_a":11,"person_b":12,"type":"predecessor_successor","context":"邓本元接替刘道崎任三明市市长后升任市委书记","overlap_org":"三明市人民政府","overlap_period":"2013-02","strength":"strong","direction":"person_to_other"},

    # Succession — 市长 (李春 was mayor before becoming party secretary)
    {"person_a":2,"person_b":1,"type":"predecessor_successor","context":"陈岳峰接替李春任三明市市长","overlap_org":"三明市人民政府","overlap_period":"2024-11","strength":"strong","direction":"person_to_other"},

    # Overlap — Current top leaders working together
    {"person_a":1,"person_b":2,"type":"overlap","context":"李春（市委书记）与陈岳峰（市长）在三明市共事","overlap_org":"中共三明市委员会","overlap_period":"2024-11至今","strength":"strong","direction":"undirected"},

    # Mayor-Chair succession chain
    {"person_a":1,"person_b":8,"type":"predecessor_successor","context":"李春接替余红胜任三明市市长","overlap_org":"三明市人民政府","overlap_period":"2021-08","strength":"strong","direction":"person_to_other"},
    {"person_a":8,"person_b":10,"type":"predecessor_successor","context":"余红胜接替杜源生任三明市市长","overlap_org":"三明市人民政府","overlap_period":"2016-08","strength":"strong","direction":"person_to_other"},
    {"person_a":10,"person_b":11,"type":"predecessor_successor","context":"杜源生接替邓本元任三明市市长","overlap_org":"三明市人民政府","overlap_period":"2013-02","strength":"strong","direction":"person_to_other"},

    # Internal promotion pattern — Mayor to Party Secretary
    {"person_a":1,"person_b":2,"type":"promotion_chain","context":"李春由市长升任市委书记，印证三明市市长升任书记的常见模式","overlap_org":"","overlap_period":"2021-2024","strength":"strong","direction":"person_to_other"},
    {"person_a":8,"person_b":10,"type":"promotion_chain","context":"余红胜由市长升任市委书记（2021年）","overlap_org":"","overlap_period":"2021","strength":"strong","direction":"other_to_person"},
    {"person_a":10,"person_b":11,"type":"promotion_chain","context":"杜源生由市长升任市委书记（2016年）","overlap_org":"","overlap_period":"2016","strength":"strong","direction":"other_to_person"},

    # 蔡奇 career trajectory (notable)
    {"person_a":15,"person_b":12,"type":"predecessor_successor","context":"蔡奇接替刘道崎任三明市市长","overlap_org":"三明市人民政府","overlap_period":"1997-11","strength":"strong","direction":"person_to_other"},
]

# =========================================================================
# SQLITE BUILD
# =========================================================================
def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations(
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions(
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships(
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for i, pos in enumerate(positions, 1):
        c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (i, pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))
    for i, rel in enumerate(relationships, 1):
        c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (i, rel["person_a"], rel["person_b"], rel["type"],
                   rel["context"], rel["overlap_org"], rel["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

# =========================================================================
# GEXF BUILD
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = (p.get("current_post") or "")
    if "市委书记" in title:
        return "255,50,50"
    if "市长" in title:
        return "50,100,255"
    if "人大常委会主任" in title:
        return "200,255,255"
    if "政协主席" in title:
        return "255,240,200"
    if "监察委员会主任" in title:
        return "255,165,0"
    return "100,100,100"

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"

def is_top_leader(p):
    title = (p.get("current_post") or "")
    return "市委书记" in title or "市长" in title or "人大常委会主任" in title or "政协主席" in title

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>三明市领导关系网络 — Party Secretary, Mayor, city leadership</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        role = esc(p.get("current_post", ""))
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('          <attvalue for="2" value="prefecture"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> org (worked_at)
    for pos in positions:
        eid += 1
        period = f"{pos['start']}–{pos['end']}"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationships)
    for rel in relationships:
        eid += 1
        ctx = esc(rel.get("context", ""))
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{ctx}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

# =========================================================================
# PERSON JSONS
# =========================================================================
def write_person_json(person_id, data):
    fname = data["filename"]
    path = os.path.join(PERSONS_DIR, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data["content"], f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")

def build_person_jsons():
    # 李春 — 市委书记
    write_person_json(1, {
        "filename": "20260716-福建省-三明市-市委书记-李春.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "三明市",
                "job": "市委书记",
                "task_id": "fujian_三明市",
                "time_focus": "2021-present"
            },
            "identity": {
                "person_id": "fujian_sanming_lichun_1969",
                "name": "李春",
                "aliases": [],
                "gender": "女",
                "ethnicity": "回族",
                "birth": "1969-03",
                "birthplace": "安徽亳州",
                "native_place": "安徽亳州",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "李春_1969",
                    "name_birthplace": "李春_安徽亳州",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "三明市委书记",
                "current_org": "中共三明市委员会",
                "administrative_rank": "正厅级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2024-11", "end": "present", "org": "中共三明市委员会", "title": "三明市委书记", "level": "正厅级", "location": "福建省三明市", "system": "party", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2021-08", "end": "2024-11", "org": "三明市人民政府", "title": "三明市市长", "level": "正厅级", "location": "福建省三明市", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2021年8月任代市长，后当选市长", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [{"org_id": 1, "name": "中共三明市委员会", "type": "党委", "level": "地级", "location": "福建省三明市"}, {"org_id": 2, "name": "三明市人民政府", "type": "政府", "level": "地级", "location": "福建省三明市"}],
            "relationships": [
                {"person": "陈岳峰", "person_id": "fujian_sanming_chenyuefeng_1973", "relationship_type": "overlap", "strength": "strong", "evidence": "李春（市委书记）与陈岳峰（市长）在三明市共事", "overlap_org": "中共三明市委员会", "overlap_period": "2024-11至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "李兴湖", "person_id": "fujian_sanming_lixinghu_1970", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "李春接替李兴湖任三明市委书记", "overlap_org": "中共三明市委员会", "overlap_period": "2024-11", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
                {"person": "余红胜", "person_id": "", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "李春接替余红胜任三明市市长", "overlap_org": "三明市人民政府", "overlap_period": "2021-08", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["福建省三明市"],
                "promotion_velocity": {"summary": "市长升任市委书记的典型路径", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "三明市 - 维基百科", "url": "https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-07-16", "source_type": "encyclopedia", "reliability": "medium", "notes": "维基百科三明市条目，含现任领导信息"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "high",
                "biggest_gap": "李春的早期履历（教育背景、工作经历起始、此前职务）尚未完全获取"
            },
            "open_questions": [
                {"priority": "high", "question": "李春的早期职业生涯和教育背景", "why_it_matters": "理解其职业路径和培养模式", "suggested_queries": ["李春 1969 简历 安徽 亳州 任职"], "last_attempted": "2026-07-16"},
                {"priority": "medium", "question": "李春在任市长期间的主要政绩", "why_it_matters": "评估其治理能力和工作风格", "suggested_queries": ["李春 三明市 市长 政绩"], "last_attempted": "2026-07-16"}
            ]
        }
    })

    # 陈岳峰 — 市长
    write_person_json(2, {
        "filename": "20260716-福建省-三明市-市长-陈岳峰.json",
        "content": {
            "schema_version": "1.0",
            "generated_at": "2026-07-16",
            "investigation_scope": {
                "province": "福建省",
                "city": "三明市",
                "region": "三明市",
                "job": "市长",
                "task_id": "fujian_三明市",
                "time_focus": "2024-present"
            },
            "identity": {
                "person_id": "fujian_sanming_chenyuefeng_1973",
                "name": "陈岳峰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1973-10",
                "birthplace": "福建漳浦",
                "native_place": "福建漳浦",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "陈岳峰_1973",
                    "name_birthplace": "陈岳峰_福建漳浦",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "三明市市长",
                "current_org": "三明市人民政府",
                "administrative_rank": "正厅级",
                "as_of": "2026-07-16",
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {"start": "2024-11", "end": "present", "org": "三明市人民政府", "title": "三明市市长", "level": "正厅级", "location": "福建省三明市", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2024年11月任代市长", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "organizations": [{"org_id": 2, "name": "三明市人民政府", "type": "政府", "level": "地级", "location": "福建省三明市"}],
            "relationships": [
                {"person": "李春", "person_id": "fujian_sanming_lichun_1969", "relationship_type": "overlap", "strength": "strong", "evidence": "陈岳峰接替李春任三明市市长，与市委书记李春共事", "overlap_org": "三明市人民政府", "overlap_period": "2024-11至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": ["福建省"],
                "promotion_velocity": {"summary": "暂缺详细履历", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "三明市 - 维基百科", "url": "https://zh.wikipedia.org/wiki/%E4%B8%89%E6%98%8E%E5%B8%82", "publisher": "维基百科", "published_at": "", "accessed_at": "2026-07-16", "source_type": "encyclopedia", "reliability": "medium", "notes": "维基百科三明市条目，含现任领导信息"}
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "high",
                "biggest_gap": "陈岳峰的完整履历尚未获取"
            },
            "open_questions": [
                {"priority": "critical", "question": "陈岳峰任职三明市长前的履历", "why_it_matters": "评估其工作经验和专业背景", "suggested_queries": ["陈岳峰 简历 福建 漳浦 任职"], "last_attempted": "2026-07-16"},
                {"priority": "high", "question": "陈岳峰的教育背景", "why_it_matters": "了解其专业训练", "suggested_queries": ["陈岳峰 学历"], "last_attempted": "2026-07-16"}
            ]
        }
    })

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    build_person_jsons()
    print("Done.")
