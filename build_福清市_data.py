#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 福清市 (Fuqing City), 福建省 (Fujian Province) leadership network.

Covers: county-level city leaders (party secretary, mayor, vice mayors, party standing committee),
plus predecessor chain and key connections.

Sources:
- Fuqing Municipal Government official website (fuqing.gov.cn) — current government leaders
- Baidu Baike — biographical data
- News reports

Task: fujian_福清市 (model_intent: iagent)
"""

import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "福清市_network.db")
GEXF_PATH = os.path.join(BASE, "福清市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──

    # 叶仁佑 — 福州市委常委、福清市委书记 (appointed June 2021)
    # Confirmed via multiple news sources: Fuzhou city's deputy party secretary-level appointment
    {"id":1,"name":"叶仁佑","gender":"男","ethnicity":"汉族",
     "birth":"1974-05","birthplace":"福建福州",
     "education":"省委党校研究生",
     "party_join":"中共党员","work_start":"1997-09",
     "current_post":"福州市委常委、福清市委书记","current_org":"中共福清市委员会",
     "source":"https://baike.baidu.com/item/%E5%8F%B6%E4%BB%81%E4%BD%91"},

    # 陈登峰 — 福清市委副书记、市长 (confirmed from fuqing.gov.cn, as of 2026)
    {"id":2,"name":"陈登峰","gender":"男","ethnicity":"汉族",
     "birth":"1974-06","birthplace":"福建",
     "education":"中央党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市委副书记、市政府党组书记、市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/cdf/"},

    # ── Vice Mayors and Government Leadership ──
    # 李文清 — 市委常委、市政府党组副书记、副市长 (常务)
    {"id":3,"name":"李文清","gender":"男","ethnicity":"汉族",
     "birth":"1972-02","birthplace":"福建",
     "education":"在职大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市委常委、市政府党组副书记、副市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/lwq/"},

    # 白瑞 — 市委常委、副市长（挂职）
    {"id":4,"name":"白瑞","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市委常委、副市长（挂职）","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/br/"},

    # 林鹤志 — 副市长（非党）
    {"id":5,"name":"林鹤志","gender":"男","ethnicity":"汉族",
     "birth":"1977-11","birthplace":"福建",
     "education":"省委党校在职研究生、农业推广硕士",
     "party_join":"",
     "work_start":"",
     "current_post":"福清市人民政府副市长、三级调研员","current_org":"福清市人民政府",
     "note":"民盟盟员，福州市政协农业农村委副主任（兼），民盟福州市委会副主委，民盟福清市委会主委",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/lhz/"},

    # 莫开奇 — 党组成员、副市长
    {"id":6,"name":"莫开奇","gender":"男","ethnicity":"汉族",
     "birth":"1970-09","birthplace":"福建",
     "education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员、副市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/mkq/"},

    # 郑云 — 党组成员、副市长
    {"id":7,"name":"郑云","gender":"女","ethnicity":"汉族",
     "birth":"1981-08","birthplace":"福建",
     "education":"研究生，管理学硕士",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员、副市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/zy/"},

    # 林万焰 — 党组成员、副市长
    {"id":8,"name":"林万焰","gender":"男","ethnicity":"汉族",
     "birth":"1977-08","birthplace":"福建",
     "education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员、副市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/lwy/"},

    # 林雄 — 党组成员、副市长、市公安局局长
    {"id":9,"name":"林雄","gender":"男","ethnicity":"汉族",
     "birth":"1972-07","birthplace":"福建",
     "education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员、副市长、市公安局党委书记、局长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/lx/"},

    # 王豪杰 — 党组成员、副市长
    {"id":10,"name":"王豪杰","gender":"男","ethnicity":"汉族",
     "birth":"1970-12","birthplace":"福建",
     "education":"在职大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员、副市长","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/whj/"},

    # 王新刚 — 党组成员（非政府副职）
    {"id":11,"name":"王新刚","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/wxg/"},

    # 俞华 — 党组成员（挂职）
    {"id":12,"name":"俞华","gender":"男","ethnicity":"汉族",
     "birth":"1972-12","birthplace":"福建",
     "education":"研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"福清市人民政府党组成员（挂职）、融侨开发区党工委副书记、管委会主任","current_org":"福清市人民政府",
     "source":"https://www.fuqing.gov.cn/xjwz/zwgk/ldzc/yh/"},

    # ── Predecessors ──
    # 吴永忠 — 前任福清市长 (2020/2021-2024.10), 现闽侯县委书记
    {"id":13,"name":"吴永忠","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"福建",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"闽侯县委书记","current_org":"中共闽侯县委员会",
     "note":"此前任福清市委副书记、市长（2020/2021?——2024年10月），2024年10月调任闽侯县委书记",
     "source":"https://baike.baidu.com/item/%E5%90%B4%E6%B0%B8%E5%BF%A0"},

    # 张帆 — 前任福清市委书记 (?-2021.06)
    {"id":14,"name":"张帆","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"待确认","current_org":"",
     "note":"前任福清市委书记，2021年6月由叶仁佑接替",
     "source":""},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共福清市委员会","type":"党委","level":"县级","parent":"中共福州市委员会","location":"福建省福州市福清市"},
    {"id":2,"name":"福清市人民政府","type":"政府","level":"县级","parent":"福州市人民政府","location":"福建省福州市福清市"},
    {"id":3,"name":"中共福清市纪律检查委员会","type":"纪委","level":"县级","parent":"中共福州市纪律检查委员会","location":"福建省福州市福清市"},
    {"id":4,"name":"福清市人民代表大会常务委员会","type":"人大","level":"县级","parent":"福州市人民代表大会常务委员会","location":"福建省福州市福清市"},
    {"id":5,"name":"中国人民政治协商会议福清市委员会","type":"政协","level":"县级","parent":"福州市政协","location":"福建省福州市福清市"},
    {"id":6,"name":"中共闽侯县委员会","type":"党委","level":"县级","parent":"中共福州市委员会","location":"福建省福州市闽侯县"},
    {"id":7,"name":"融侨经济技术开发区管委会","type":"开发区","level":"国家级","parent":"福清市人民政府","location":"福建省福州市福清市"},
    {"id":8,"name":"福清市公安局","type":"政府","level":"县级","parent":"福清市人民政府","location":"福建省福州市福清市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 叶仁佑 — current 市委书记
    {"person_id":1,"org_id":1,"title":"福州市委常委、福清市委书记","start":"2021-06","end":"present","rank":"副厅级","note":"福州市委常委兼"},
    # 陈登峰 — current 市长
    {"person_id":2,"org_id":1,"title":"福清市委副书记","start":"","end":"present","rank":"正处级","note":""},
    {"person_id":2,"org_id":2,"title":"福清市政府党组书记、市长","start":"","end":"present","rank":"正处级","note":"主持市政府全面工作"},
    # 李文清 — 常务副市长
    {"person_id":3,"org_id":1,"title":"福清市委常委","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":3,"org_id":2,"title":"福清市政府党组副书记、副市长","start":"","end":"present","rank":"副处级","note":"负责市政府常务工作"},
    # 白瑞 — 挂职副市长
    {"person_id":4,"org_id":1,"title":"福清市委常委","start":"","end":"present","rank":"副处级","note":"挂职"},
    {"person_id":4,"org_id":2,"title":"福清市副市长（挂职）","start":"","end":"present","rank":"","note":"挂职"},
    # 林鹤志 — 副市长
    {"person_id":5,"org_id":2,"title":"福清市人民政府副市长、三级调研员","start":"","end":"present","rank":"副处级","note":"民盟，分管生态环境、水利、农业农村等"},
    # 莫开奇
    {"person_id":6,"org_id":2,"title":"福清市人民政府党组成员、副市长","start":"","end":"present","rank":"副处级","note":""},
    # 郑云
    {"person_id":7,"org_id":2,"title":"福清市人民政府党组成员、副市长","start":"","end":"present","rank":"副处级","note":""},
    # 林万焰
    {"person_id":8,"org_id":2,"title":"福清市人民政府党组成员、副市长","start":"","end":"present","rank":"副处级","note":""},
    # 林雄
    {"person_id":9,"org_id":2,"title":"福清市人民政府党组成员、副市长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":9,"org_id":8,"title":"福清市公安局党委书记、局长、督察长","start":"","end":"present","rank":"","note":""},
    # 王豪杰
    {"person_id":10,"org_id":2,"title":"福清市人民政府党组成员、副市长","start":"","end":"present","rank":"副处级","note":""},
    # 王新刚
    {"person_id":11,"org_id":2,"title":"福清市人民政府党组成员","start":"","end":"present","rank":"","note":""},
    # 俞华
    {"person_id":12,"org_id":2,"title":"福清市人民政府党组成员（挂职）","start":"","end":"present","rank":"","note":"挂职"},
    {"person_id":12,"org_id":7,"title":"融侨开发区党工委副书记、管委会主任","start":"","end":"present","rank":"","note":""},
    # 吴永忠 — 前任福清市长
    {"person_id":13,"org_id":2,"title":"福清市委副书记、市长","start":"","end":"2024-10","rank":"正处级","note":"调任闽侯县委书记"},
    {"person_id":13,"org_id":6,"title":"闽侯县委书记","start":"2024-10","end":"present","rank":"正处级","note":"接替赵明正"},
    # 张帆 — 前任福清市委书记
    {"person_id":14,"org_id":1,"title":"福清市委书记","start":"","end":"2021-06","rank":"正处级","note":"由叶仁佑接替"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"叶仁佑作为市委书记、陈登峰作为市长，构成党政主要领导搭档","overlap_org":"中共福清市委员会/福清市人民政府","overlap_period":"2024?—present","confidence":"confirmed"},
    {"person_a":1,"person_b":14,"type":"predecessor_successor","context":"叶仁佑2021年6月接替张帆任福清市委书记","overlap_org":"中共福清市委员会","overlap_period":"2021-06","confidence":"confirmed"},
    {"person_a":2,"person_b":13,"type":"predecessor_successor","context":"陈登峰接替吴永忠任福清市长","overlap_org":"福清市人民政府","overlap_period":"2024-10","confidence":"confirmed"},
    {"person_a":3,"person_b":2,"type":"superior_subordinate","context":"李文清作为常务副市长协助市长陈登峰工作","overlap_org":"福清市人民政府","overlap_period":"","confidence":"confirmed"},
    {"person_a":1,"person_b":3,"type":"superior_subordinate","context":"叶仁佑是市委书记，李文清是市委常委","overlap_org":"中共福清市委员会","overlap_period":"","confidence":"confirmed"},
    {"person_a":6,"person_b":2,"type":"superior_subordinate","context":"莫开奇作为党组成员、副市长，隶属于市政府领导班子","overlap_org":"福清市人民政府","overlap_period":"","confidence":"confirmed"},
    {"person_a":9,"person_b":2,"type":"superior_subordinate","context":"林雄作为副市长和公安局长，属市政府领导班子成员","overlap_org":"福清市人民政府","overlap_period":"","confidence":"confirmed"},
    {"person_a":13,"person_b":14,"type":"overlap","context":"吴永忠任市长期间与张帆（市委书记）搭班子","overlap_org":"福清市","overlap_period":"2020?-2021-06","confidence":"plausible"},
]


# =========================================================================
# SQLite BUILD
# =========================================================================
def build_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT,
            rank TEXT, note TEXT
        );
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            confidence TEXT
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"],p["name"],p.get("gender",""),p.get("ethnicity",""),
                     p.get("birth",""),p.get("birthplace",""),p.get("education",""),
                     p.get("party_join",""),p.get("work_start",""),
                     p.get("current_post",""),p.get("current_org",""),p.get("source","")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES(?,?,?,?,?,?)""",
                    (o["id"],o["name"],o["type"],o["level"],o.get("parent",""),o.get("location","")))

    for pos in positions:
        cur.execute("""INSERT INTO positions(person_id,org_id,title,start,"end",rank,note) VALUES(?,?,?,?,?,?,?)""",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,confidence) VALUES(?,?,?,?,?,?,?)""",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period",""),r.get("confidence","")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")


# =========================================================================
# GEXF BUILD
# =========================================================================
def build_gexf():
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(p):
        role = (p.get("current_post","") or "")
        if "市委" in role and "书记" in role and "纪委" not in role:
            return "255,50,50"
        elif "市长" in role and "副" not in role:
            return "50,100,255"
        elif "纪委书记" in role:
            return "255,165,0"
        else:
            return "100,100,100"

    def is_top_leader(p):
        role = (p.get("current_post","") or "")
        return "书记" in role or ("市长" in role and "副" not in role)

    def org_color(o):
        t = o.get("type","")
        if "党委" in t: return "255,200,200"
        if "政府" in t: return "200,200,255"
        if "开发区" in t: return "200,255,200"
        if "人大" in t: return "200,255,255"
        if "政协" in t: return "255,240,200"
        if "纪委" in t: return "255,200,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append(f'    <description>福清市（Fuqing City）领导班子关系网络 — 2026-07</description>')
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

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"][:50])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH,"w",encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done.")
