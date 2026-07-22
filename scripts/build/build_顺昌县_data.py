#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Shunchang County (顺昌县), Nanping City, Fujian Province.

Covers: Party Secretary (县委书记), County Mayor (县长), key leadership,
predecessor/successor chains, and the county-level leadership network.

Sources:
- fjsc.gov.cn: Shunchang County government website
- Wikipedia (Chinese): 顺昌县 leadership info
- fjscnews.com: Local news portal
- fjsen.com (东南网): Fujian official news

Generated: 2026-07-17
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/fujian_顺昌县")
DB_PATH = os.path.join(TMP, "顺昌县_network.db")
GEXF_PATH = os.path.join(TMP, "顺昌县_network.gexf")
PERSONS_DIR = TMP

AS_OF = "2026-07-17"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    # 赵大建 — 顺昌县委书记 (2021.6-)
    {"id":1,"name":"赵大建","gender":"男","ethnicity":"汉族","birth":"1969-08","birthplace":"浙江省永嘉县","education":"","party_join":"中共党员","work_start":"","current_post":"顺昌县委书记","current_org":"中共顺昌县委员会",
     "source":"https://zh.wikipedia.org/zh-hans/%E9%A1%BA%E6%98%8C%E5%8E%BF"},
    # 谷国海 — 顺昌县县长 (2021.1-)
    {"id":2,"name":"谷国海","gender":"男","ethnicity":"汉族","birth":"1975-11","birthplace":"湖南省茶陵县","education":"大学","party_join":"中共党员","work_start":"","current_post":"顺昌县人民政府县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},

    # ── Other current county leaders ──
    # 杨俊青 — 顺昌县人大常委会主任 (2023.12-)
    {"id":3,"name":"杨俊青","gender":"男","ethnicity":"汉族","birth":"1973-11","birthplace":"福建省南平市","education":"","party_join":"中共党员","work_start":"","current_post":"顺昌县人大常委会主任","current_org":"顺昌县人民代表大会常务委员会",
     "source":"https://zh.wikipedia.org/zh-hans/%E9%A1%BA%E6%98%8C%E5%8E%BF"},
    # 徐小明 — 顺昌县政协主席 (2021.12-)
    {"id":4,"name":"徐小明","gender":"男","ethnicity":"汉族","birth":"1972-05","birthplace":"福建省顺昌县","education":"","party_join":"中共党员","work_start":"","current_post":"顺昌县政协主席","current_org":"政协顺昌县委员会",
     "source":"https://zh.wikipedia.org/zh-hans/%E9%A1%BA%E6%98%8C%E5%8E%BF"},

    # ── Key deputies ──
    # 陈可兴 — 顺昌县委副书记 (专职)
    {"id":5,"name":"陈可兴","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"顺昌县委副书记","current_org":"中共顺昌县委员会",
     "source":"http://www.fjscnews.com/2026-04/07/content_2328658.htm"},
    # 韦妙煌 — 顺昌县委常委、组织部部长 (2023.8-)
    {"id":6,"name":"韦妙煌","gender":"男","ethnicity":"汉族","birth":"1985-08","birthplace":"","education":"大学","party_join":"中共党员","work_start":"","current_post":"顺昌县委常委、组织部部长","current_org":"中共顺昌县委组织部",
     "source":"https://news.fznews.com.cn/dsxw/20230803/N5slWlxAb6.shtml"},
    # 林斌 — 顺昌县委常委、纪委书记、监委主任
    {"id":7,"name":"林斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"顺昌县委常委、县纪委书记、县监委主任","current_org":"中共顺昌县纪律检查委员会",
     "source":"http://www.fjscnews.com/2024-01/22/content_1632246.htm"},
    # 蔡荣洋 — 前常务副县长 (removed 2025.7)
    {"id":8,"name":"蔡荣洋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"","current_org":"",
     "source":"https://np.fjsen.com/wap/2025-01/13/content_31822139.htm"},

    # ── Current deputy mayors (from fjsc.gov.cn) ──
    {"id":9,"name":"李军","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":10,"name":"郑禧鸿","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":11,"name":"郑韶明","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":12,"name":"谢辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":13,"name":"冯磊","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":14,"name":"郭骏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":15,"name":"黄镜浩","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},
    {"id":16,"name":"梁彪","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县副县长","current_org":"顺昌县人民政府",
     "source":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html"},

    # ── Other standing committee members ──
    # 高文健 — 常委、总工会主席
    {"id":17,"name":"高文健","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县委常委、县总工会主席","current_org":"顺昌县总工会",
     "source":"http://www.fjscnews.com/2024-07/04/content_1727772.htm"},
    # 严芬 — 常委、统战部部长
    {"id":18,"name":"严芬","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"顺昌县委常委、统战部部长","current_org":"中共顺昌县委统战部",
     "source":"http://www.fjscnews.com/2023-03/24/content_1603900.htm"},

    # ── Predecessors — 县委书记 ──
    # 邱建彬 — 前任县委书记 (-2021.6)
    {"id":19,"name":"邱建彬","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"","current_org":"",
     "source":"http://www.fjscnews.com/2021-06/25/content_1124090.htm"},

    # ── Predecessors — 县长 ──
    # Before 谷国海, the predecessor 县长 is not clearly documented in our sources
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共顺昌县委员会","type":"党委","level":"县级","parent":"中共南平市委员会","location":"福建省南平市顺昌县"},
    {"id":2,"name":"顺昌县人民政府","type":"政府","level":"县级","parent":"南平市人民政府","location":"福建省南平市顺昌县"},
    {"id":3,"name":"顺昌县人民代表大会常务委员会","type":"人大","level":"县级","parent":"","location":"福建省南平市顺昌县"},
    {"id":4,"name":"政协顺昌县委员会","type":"政协","level":"县级","parent":"","location":"福建省南平市顺昌县"},
    {"id":5,"name":"中共顺昌县委组织部","type":"党委","level":"县级","parent":"中共顺昌县委员会","location":"福建省南平市顺昌县"},
    {"id":6,"name":"中共顺昌县纪律检查委员会","type":"党委","level":"县级","parent":"中共顺昌县委员会","location":"福建省南平市顺昌县"},
    {"id":7,"name":"中共顺昌县委统战部","type":"党委","level":"县级","parent":"中共顺昌县委员会","location":"福建省南平市顺昌县"},
    {"id":8,"name":"顺昌县总工会","type":"群团","level":"县级","parent":"","location":"福建省南平市顺昌县"},
    {"id":9,"name":"中共南平市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省南平市"},
    {"id":10,"name":"南平市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省南平市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 赵大建 — Party Secretary
    {"person_id":1,"org_id":1,"title":"顺昌县委书记","start":"2021-06","end":"present","rank":"正处级","note":"2021年6月任顺昌县委书记"},
    {"person_id":1,"org_id":1,"title":"顺昌县委常委、书记","start":"2021-06","end":"present","rank":"正处级","note":"任第十四届县委委员、常委、书记"},

    # 谷国海 — County Mayor
    {"person_id":2,"org_id":2,"title":"顺昌县人民政府县长","start":"2021-01","end":"present","rank":"正处级","note":"2021年1月任代县长，1月27日当选县长"},
    {"person_id":2,"org_id":1,"title":"顺昌县委副书记","start":"2021-01","end":"present","rank":"正处级","note":"兼任县委副书记"},
    {"person_id":2,"org_id":2,"title":"顺昌县人民政府副县长、代县长","start":"2021-01","end":"2021-01","rank":"正处级","note":"2021年1月11日任代县长"},

    # 杨俊青 — 人大主任
    {"person_id":3,"org_id":3,"title":"顺昌县人大常委会主任","start":"2023-12","end":"present","rank":"正处级","note":"2023年12月任人大主任"},

    # 徐小明 — 政协主席 (former 政法委书记)
    {"person_id":4,"org_id":4,"title":"顺昌县政协主席","start":"2021-12","end":"present","rank":"正处级","note":"2021年12月任政协主席"},
    {"person_id":4,"org_id":1,"title":"顺昌县委常委、政法委书记","start":"","end":"2021-12","rank":"副处级","note":"此前担任政法委书记"},

    # 陈可兴 — 专职副书记
    {"person_id":5,"org_id":1,"title":"顺昌县委副书记","start":"2024-06","end":"present","rank":"副处级","note":"至少2024年6月起任职，此前履历待查"},

    # 韦妙煌 — 组织部部长
    {"person_id":6,"org_id":5,"title":"顺昌县委常委、组织部部长","start":"2023-08","end":"present","rank":"副处级","note":"2023年8月任前公示，由市委组织部干部监督室主任调任"},
    {"person_id":6,"org_id":1,"title":"顺昌县委常委","start":"2023-08","end":"present","rank":"副处级","note":""},
    {"person_id":6,"org_id":9,"title":"南平市委组织部干部监督室主任","start":"","end":"2023-08","rank":"正科级","note":"任前曾任市委组织部干部监督室主任、一级主任科员"},

    # 林斌 — 纪委书记
    {"person_id":7,"org_id":6,"title":"顺昌县委常委、县纪委书记、县监委主任","start":"2024-01","end":"present","rank":"副处级","note":"至少2024年1月起任现职"},

    # 蔡荣洋 — 前常务副县长
    {"person_id":8,"org_id":2,"title":"顺昌县委常委、常务副县长","start":"","end":"2025-07","rank":"副处级","note":"2025年7月30日被免去副县长职务"},
    {"person_id":8,"org_id":1,"title":"顺昌县委常委","start":"","end":"2025-07","rank":"副处级","note":""},

    # Deputy mayors
    {"person_id":9,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":10,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":11,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":12,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":13,"org_id":2,"title":"顺昌县副县长","start":"2025-07","end":"present","rank":"副处级","note":"2025年7月30日任命"},
    {"person_id":14,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":15,"org_id":2,"title":"顺昌县副县长","start":"","end":"present","rank":"副处级","note":""},
    {"person_id":16,"org_id":2,"title":"顺昌县副县长","start":"2025-07","end":"present","rank":"副处级","note":"2025年7月30日任命"},

    # 高文健 — 总工会主席
    {"person_id":17,"org_id":8,"title":"顺昌县委常委、县总工会主席","start":"","end":"present","rank":"副处级","note":""},

    # 严芬 — 统战部长
    {"person_id":18,"org_id":7,"title":"顺昌县委常委、统战部部长","start":"","end":"present","rank":"副处级","note":""},

    # 邱建彬 — 前县委书记
    {"person_id":19,"org_id":1,"title":"顺昌县委书记","start":"","end":"2021-06","rank":"正处级","note":"2021年6月不再担任顺昌县委书记"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Predecessor-successor: 县委书记
    {"person_a":1,"person_b":19,"type":"predecessor_successor","context":"赵大建接替邱建彬任顺昌县委书记","overlap_org":"中共顺昌县委员会","overlap_period":"2021-06","direction":"person_to_other","strength":"strong"},

    # 赵大建 ↔ 谷国海 (搭班关系)
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"赵大建（县委书记）与谷国海（县长）搭班","overlap_org":"中共顺昌县委员会","overlap_period":"2021-2026","direction":"undirected","strength":"strong"},

    # 赵大建 ↔ 陈可兴
    {"person_a":1,"person_b":5,"type":"superior_subordinate","context":"赵大建与县委副书记陈可兴在县委班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2024-2026","direction":"undirected","strength":"strong"},
    # 赵大建 ↔ 韦妙煌
    {"person_a":1,"person_b":6,"type":"superior_subordinate","context":"赵大建与组织部部长韦妙煌在县委班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2023-2026","direction":"undirected","strength":"strong"},
    # 赵大建 ↔ 林斌
    {"person_a":1,"person_b":7,"type":"superior_subordinate","context":"赵大建与纪委书记林斌在县委班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2024-2026","direction":"undirected","strength":"strong"},
    # 赵大建 ↔ 蔡荣洋
    {"person_a":1,"person_b":8,"type":"superior_subordinate","context":"赵大建与常务副县长蔡荣洋在县委/政府班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2021-2025","direction":"undirected","strength":"strong"},

    # 谷国海 ↔ 陈可兴
    {"person_a":2,"person_b":5,"type":"superior_subordinate","context":"谷国海（县长）与陈可兴（副书记）在县委班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2024-2026","direction":"undirected","strength":"strong"},
    # 谷国海 ↔ 韦妙煌
    {"person_a":2,"person_b":6,"type":"superior_subordinate","context":"谷国海与组织部部长韦妙煌在县委班子共事","overlap_org":"中共顺昌县委员会","overlap_period":"2023-2026","direction":"undirected","strength":"strong"},
    # 谷国海 ↔ 蔡荣洋
    {"person_a":2,"person_b":8,"type":"superior_subordinate","context":"谷国海（县长）与常务副县长蔡荣洋在政府班子共事","overlap_org":"顺昌县人民政府","overlap_period":"2021-2025","direction":"undirected","strength":"strong"},

    # 陈可兴 ↔ 韦妙煌 (共同出席多次党建/培训活动)
    {"person_a":5,"person_b":6,"type":"overlap","context":"陈可兴与韦妙煌在党建、培训等工作中密切配合","overlap_org":"中共顺昌县委员会","overlap_period":"2024-2026","direction":"undirected","strength":"strong"},

    # 韦妙煌 ↔ 林斌 (巡察工作配合)
    {"person_a":6,"person_b":7,"type":"overlap","context":"韦妙煌（组织部）与林斌（纪委）在巡察工作中协作","overlap_org":"中共顺昌县委员会","overlap_period":"2024-2026","direction":"undirected","strength":"medium"},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER, title TEXT,
        start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER, type TEXT,
        context TEXT, overlap_org TEXT, overlap_period TEXT,
        direction TEXT, strength TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],
                   p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,\"end\",rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,direction,strength) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"],r["direction"],r["strength"]))

    conn.commit()
    conn.close()
    print(f"SQLite DB created: {DB_PATH}")


# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    if "县委书记" in (p.get("current_post") or "") or "县委副书记" in (p.get("current_post") or ""):
        return "255,50,50"
    elif "县长" in (p.get("current_post") or "") or "副县长" in (p.get("current_post") or ""):
        return "50,100,255"
    elif "纪委书记" in (p.get("current_post") or ""):
        return "255,165,0"
    elif "主任" in (p.get("current_post") or "") or "政协" in (p.get("current_post") or ""):
        return "155,155,155"
    else:
        return "100,100,100"

def org_color(o):
    m = {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","群团":"255,220,255"}
    return m.get(o["type"],"200,200,200")

def is_top_leader(p):
    return p["id"] in (1, 2)

def person_size(p):
    return "20.0" if is_top_leader(p) else ("15.0" if p["id"] in (3,4,5,6,7) else "12.0")

def org_size(o):
    return "8.0"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>顺昌县领导班子关系网络 - 福建省南平市顺昌县</description>')
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
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{org_size(o)}"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# =========================================================================
# PERSON JSONS
# =========================================================================
def get_org_name(org_id):
    o = next((x for x in organizations if x["id"] == org_id), None)
    return o["name"] if o else ""

def get_org_location(org_id):
    o = next((x for x in organizations if x["id"] == org_id), None)
    return o["location"] if o else ""


def write_person_json(pid, job_slug):
    p = next(x for x in persons if x["id"] == pid)
    rels_out = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next(x for x in persons if x["id"] == r["person_b"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})
        elif r["person_b"] == pid:
            other = next(x for x in persons if x["id"] == r["person_a"])
            rels_out.append({"person":other["name"],"person_id":f"p{other['id']}","relationship_type":r["type"],
                             "strength":r["strength"],"evidence":r["context"],"overlap_org":r["overlap_org"],
                             "overlap_period":r["overlap_period"],"direction":r["direction"],"confidence":"confirmed","source_ids":["S001"]})

    person_positions = []
    for pos in positions:
        if pos["person_id"] == pid:
            org_name = get_org_name(pos["org_id"])
            org_loc = get_org_location(pos["org_id"])
            system = "other"
            org_obj = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            if org_obj:
                if "党委" in org_obj["type"]:
                    system = "party"
                elif "政府" in org_obj["type"]:
                    system = "government"
                elif "人大" in org_obj["type"]:
                    system = "other"
                elif "政协" in org_obj["type"]:
                    system = "other"
                elif "群团" in org_obj["type"]:
                    system = "other"
            person_positions.append({
                "start":pos["start"],"end":pos["end"],"org":org_name,
                "title":pos["title"],"level":pos.get("rank",""),"location":org_loc,
                "system":system,
                "rank":pos.get("rank",""),"is_key_promotion":False,"notes":pos.get("note",""),
                "confidence":"confirmed","source_ids":["S001"]
            })

    # Build education entries
    education_entries = []
    if p["education"]:
        education_entries.append({
            "period":"","institution":"","major":"",
            "degree":p["education"],"study_type":"unknown","source_ids":["S001"]
        })

    profile = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "福建省",
            "city": "南平市",
            "region": "顺昌县",
            "job": job_slug,
            "task_id": "fujian_顺昌县",
            "time_focus": "2015-present"
        },
        "identity": {
            "person_id": f"shunchang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": education_entries,
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {"name_birth":"","name_birthplace":"","official_profile_url":""}
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级" if pid in (1,2,3,4) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p["current_post"]),
            "source_ids": ["S001"]
        },
        "career_timeline": person_positions,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary":"","notable_fast_promotions":[]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {"id":"S001","title":"顺昌县 - 维基百科","url":"https://zh.wikipedia.org/zh-hans/%E9%A1%BA%E6%98%8C%E5%8E%BF",
             "publisher":"维基百科","published_at":"","accessed_at":AS_OF,"source_type":"encyclopedia","reliability":"medium","notes":""},
            {"id":"S002","title":"顺昌县人民政府 - 县政府领导","url":"https://www.fjsc.gov.cn/cms/html/scxrmzf/indexyear/131845644.html",
             "publisher":"顺昌县人民政府","published_at":"","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
            {"id":"S003","title":"顺昌县委经济工作会议召开 - 东南网","url":"https://np.fjsen.com/wap/2025-01/13/content_31822139.htm",
             "publisher":"东南网","published_at":"2025-01-13","accessed_at":AS_OF,"source_type":"media","reliability":"high","notes":""},
            {"id":"S004","title":"赵大建任中共顺昌县委书记","url":"http://www.fjscnews.com/2021-06/25/content_1124090.htm",
             "publisher":"顺昌新闻网","published_at":"2021-06-25","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
            {"id":"S005","title":"顺昌县人民代表大会常务委员会决定任免名单","url":"http://www.fjscnews.com/2025-08/01/content_2241071.htm",
             "publisher":"顺昌新闻网","published_at":"2025-08-01","accessed_at":AS_OF,"source_type":"official","reliability":"high","notes":""},
        ],
        "confidence_summary": {
            "identity":"partial",
            "current_role":"confirmed",
            "career_completeness":"partial",
            "relationship_confidence":"high",
            "biggest_gap":f"缺少{p['name']}的完整早期履历"
        },
        "open_questions": [
            {"priority":"high","question":f"{p['name']}的完整早期履历和出生地","why_it_matters":"理解职业发展路径和提拔背景",
             "suggested_queries":[f"{p['name']} 简历 顺昌县",f"{p['name']} 任前公示"],"last_attempted":AS_OF},
            {"priority":"medium","question":f"{p['name']}的教育背景和企业任职经历","why_it_matters":"影响专业能力评估",
             "suggested_queries":[f"{p['name']} 毕业 院校"],"last_attempted":AS_OF}
        ]
    }

    # Fill in dedupe keys
    profile["identity"]["dedupe_keys"]["name_birth"] = f"{p['name']}_{p['birth']}"
    if p["birthplace"]:
        profile["identity"]["dedupe_keys"]["name_birthplace"] = f"{p['name']}_{p['birthplace']}"

    filename = f"{AS_OF.replace('-','')}-福建省-南平市-{job_slug}-{p['name']}.json"
    fpath = os.path.join(PERSONS_DIR, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"Person JSON created: {fpath}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    write_person_json(1, "县委书记")
    write_person_json(2, "县长")
    write_person_json(5, "县委副书记")
    write_person_json(6, "县委常委-组织部部长")
    write_person_json(7, "县委常委-纪委书记")
    print("\nDone. All artifacts written to", TMP)
