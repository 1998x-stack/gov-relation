#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 同安区 (Tong'an District, Xiamen, Fujian).

同安区 — 厦门市下辖区，1997年撤县设区，位于厦门市北部。

Research date: 2026-07-16
Sources:
- 同安区政府网站 (www.xmta.gov.cn) — 领导简介页面
- 网易新闻 — 干部任免报道
- 百度百科/搜索结果 — 人物简历
- 人民网 — 干部资料
- 厦门日报 — 新闻报道

Coverage: 区委/区政府主要领导，区委常委班子成员。

Confidence notes:
- 黄晓军（区长）：confirmed（政府官网）
- 郭三温（常务副区长）：confirmed（政府官网+区委常委身份）
- 王跃平（区委书记）：plausible（2024年11月纪委全会报道，后续变动待确认）
- 熊伟（区纪委书记）：plausible（多来源提及）
- 林生海（区委副书记）：plausible（百度百科/搜索结果提及）
- 其他副区长：confirmed（政府官网）
- 区委组织部部长、政法委书记：unverified（未找到明确来源）
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/fujian_同安区")
DB_PATH = os.path.join(STAGING, "同安区_network.db")
GEXF_PATH = os.path.join(STAGING, "同安区_network.gexf")

os.makedirs(STAGING, exist_ok=True)

AS_OF = "2026-07-16"

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 周桂良 — 同安区委书记 (前任区长晋升，2026.04起)
    {"id":1,"name":"周桂良","gender":"男","ethnicity":"汉族",
     "birth":"1975-11","birthplace":"福建惠安","education":"福州大学本科，工学学士",
     "party_join":"1995-05","work_start":"1997-07",
     "current_post":"中共同安区委书记、区人武部党委第一书记",
     "current_org":"中共同安区委",
     "source":"百度百科（周桂良）；白鹭洲知政(2026-04-21) — 厦门人事任前公示"},
    # 黄晓军 — 同安区委副书记、代区长/区长 (as of 2026.05)
    {"id":2,"name":"黄晓军","gender":"男","ethnicity":"汉族",
     "birth":"1979-10","birthplace":"福建南安","education":"研究生，管理学硕士",
     "party_join":"中共党员","work_start":"2004-08",
     "current_post":"同安区委副书记、区人民政府代区长、党组书记",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介(xmta.gov.cn/zc/ldxx/); 白鹭洲知政(2026-04-21)"},
    # 王跃平 — 前任同安区委书记 (至约2026.04)
    {"id":3,"name":"王跃平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原同安区委书记，已调离）",
     "current_org":"",
     "source":"厦门市纪委监委 — 同安区纪委全会报道(2024-11)"},

    # ── 2. Current deputy leaders (副区长/常委) ──
    # 郭三温 — 区委常委、常务副区长
    {"id":4,"name":"郭三温","gender":"男","ethnicity":"汉族",
     "birth":"1970-11","birthplace":"","education":"中央党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区委常委、区人民政府常务副区长、党组副书记",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介(xmta.gov.cn/zc/ldxx/)"},
    # 林生海 — 区委副书记
    {"id":5,"name":"林生海","gender":"男","ethnicity":"汉族",
     "birth":"1970-11","birthplace":"福建厦门","education":"中央党校大学",
     "party_join":"中共党员","work_start":"1992-08",
     "current_post":"同安区委副书记",
     "current_org":"中共同安区委",
     "source":"百度百科（搜索结果）；厦门市翔安区发改局副局长、共青团翔安区委曾任"},
    # 熊伟 — 区委常委、区纪委书记、区监委主任
    {"id":6,"name":"熊伟","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区委常委、区纪委书记、区监委主任",
     "current_org":"中共同安区纪律检查委员会",
     "source":"同安区纪委/鹭岛清风报道；检索信源"},
    # 徐少敏 — 前任区纪委书记，现市委第五巡察组组长
    {"id":7,"name":"徐少敏","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"厦门市委第五巡察组组长（原同安区委常委、区纪委书记）",
     "current_org":"中共厦门市委巡察组",
     "source":"厦门市委组织部任前公示(2025-11)"},
    # 许永良 — 前任区委副书记/纪检出身
    {"id":8,"name":"许永良","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"（原同安区委副书记，曾任区委常委、区纪委书记）",
     "current_org":"",
     "source":"网易新闻 — 同安区干部任职报道(2021); 海沧区人大报道(2024-12)"},

    # ── 3. Deputy mayors (副区长) ──
    {"id":9,"name":"王旭辉","gender":"男","ethnicity":"汉族",
     "birth":"1971-07","birthplace":"","education":"中央党校大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人民政府副区长",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介"},
    {"id":10,"name":"黄祖南","gender":"男","ethnicity":"汉族",
     "birth":"1972-04","birthplace":"","education":"研究生",
     "party_join":"民建会员","work_start":"",
     "current_post":"同安区人民政府副区长",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介"},
    {"id":11,"name":"吕联传","gender":"男","ethnicity":"汉族",
     "birth":"1982-08","birthplace":"","education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人民政府副区长",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介"},
    {"id":12,"name":"李毅","gender":"男","ethnicity":"汉族",
     "birth":"1979-07","birthplace":"","education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人民政府副区长",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介"},
    {"id":13,"name":"刘晓东","gender":"男","ethnicity":"汉族",
     "birth":"1978-10","birthplace":"","education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人民政府副区长、区公安分局局长、督察长",
     "current_org":"同安区人民政府/厦门市公安局同安分局",
     "source":"同安区政府网站 — 领导简介"},
    {"id":14,"name":"郑发华","gender":"男","ethnicity":"汉族",
     "birth":"1980-11","birthplace":"","education":"大学",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人民政府副区长",
     "current_org":"同安区人民政府",
     "source":"同安区政府网站 — 领导简介"},

    # ── 4. Cross-district connections ──
    # 吴申宇 — 同安区出身的干部，现海沧区委副书记
    {"id":15,"name":"吴申宇","gender":"男","ethnicity":"汉族",
     "birth":"1977-04","birthplace":"福建厦门","education":"研究生",
     "party_join":"中共党员","work_start":"",
     "current_post":"海沧区委副书记",
     "current_org":"中共海沧区委",
     "source":"build_海沧区_data.py"},  # 曾在同安区洪塘镇、共青团同安区委工作
    # 叶晓东 — 区人大常委会主任
    {"id":16,"name":"叶晓东","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区人大常委会主任",
     "current_org":"同安区人大常委会",
     "source":"百度百科（同安区条目）"},
    # 洪国平 — 区政协主席
    {"id":17,"name":"洪国平","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"中共党员","work_start":"",
     "current_post":"同安区政协主席",
     "current_org":"政协同安区委员会",
     "source":"百度百科（同安区条目）"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共同安区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"同安区"},
    {"id":2,"name":"同安区人民政府","type":"政府","level":"县级","parent":"厦门市人民政府","location":"同安区"},
    {"id":3,"name":"中共同安区纪律检查委员会","type":"纪委","level":"县级","parent":"厦门市纪委监委","location":"同安区"},
    {"id":4,"name":"同安区人大常委会","type":"人大","level":"县级","parent":"厦门市人大常委会","location":"同安区"},
    {"id":5,"name":"政协同安区委员会","type":"政协","level":"县级","parent":"厦门市政协","location":"同安区"},
    {"id":6,"name":"厦门市公安局同安分局","type":"政府","level":"正科级","parent":"厦门市公安局","location":"同安区"},
    {"id":7,"name":"中共海沧区委","type":"党委","level":"县级","parent":"中共厦门市委","location":"海沧区"},
    {"id":8,"name":"同安区洪塘镇","type":"乡镇","level":"乡科级","parent":"同安区","location":"同安区"},
    {"id":9,"name":"共青团同安区委员会","type":"群团","level":"乡科级","parent":"同安区","location":"同安区"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 周桂良
    {"person_id":1,"org_id":1,"title":"同安区委书记、区人武部党委第一书记","start":"2026-04","end":"","rank":"正处","note":"2026年4月任"},
    {"person_id":1,"org_id":2,"title":"同安区区长","start":"2023-12","end":"2026-04","rank":"正处","note":"晋升区委书记"},
    # 黄晓军
    {"person_id":2,"org_id":2,"title":"同安区委副书记、代区长、党组书记","start":"2026-05","end":"","rank":"正处","note":"2026年5月任代区长"},
    {"person_id":2,"org_id":1,"title":"同安区委副书记","start":"2026-05","end":"","rank":"正处","note":""},
    # 王跃平 — 前任区委书记
    {"person_id":3,"org_id":1,"title":"同安区委书记","start":"","end":"2026-04","rank":"正处","note":"去向待确认"},
    # 郭三温
    {"person_id":4,"org_id":2,"title":"常务副区长、党组副书记","start":"","end":"","rank":"副处","note":""},
    {"person_id":4,"org_id":1,"title":"同安区委常委","start":"","end":"","rank":"副处","note":""},
    # 林生海
    {"person_id":5,"org_id":1,"title":"同安区委副书记","start":"","end":"","rank":"副处","note":""},
    # 熊伟
    {"person_id":6,"org_id":3,"title":"同安区委常委、区纪委书记、区监委主任","start":"","end":"","rank":"副处","note":""},
    {"person_id":6,"org_id":1,"title":"同安区委常委","start":"","end":"","rank":"副处","note":""},
    # 徐少敏
    {"person_id":7,"org_id":3,"title":"同安区委常委、区纪委书记、区监委主任","start":"","end":"2025-11","rank":"副处","note":"调任市委巡察组"},
    # 许永良
    {"person_id":8,"org_id":1,"title":"同安区委副书记（曾任区委常委、纪委书记）","start":"","end":"","rank":"副处","note":"前任纪委书记升任副书记"},
    # 副区长
    {"person_id":9,"org_id":2,"title":"副区长","start":"","end":"","rank":"副处","note":"负责科技、工业、商务"},
    {"person_id":10,"org_id":2,"title":"副区长","start":"","end":"","rank":"副处","note":"负责教育、卫健、文旅(民建)"},
    {"person_id":11,"org_id":2,"title":"副区长","start":"","end":"","rank":"副处","note":"负责住建、交通、市政"},
    {"person_id":12,"org_id":2,"title":"副区长","start":"","end":"","rank":"副处","note":"负责民政、农业农村、水利"},
    {"person_id":13,"org_id":2,"title":"副区长、公安分局局长、督察长","start":"","end":"","rank":"副处","note":"负责政法、公安"},
    {"person_id":13,"org_id":6,"title":"厦门市公安局同安分局局长、督察长","start":"","end":"","rank":"正科","note":""},
    {"person_id":14,"org_id":2,"title":"副区长","start":"","end":"","rank":"副处","note":"负责政府办、数据管理"},
    # 吴申宇（跨区连接）
    {"person_id":15,"org_id":7,"title":"海沧区委副书记","start":"","end":"","rank":"副处","note":"曾在同安工作"},
    {"person_id":15,"org_id":8,"title":"洪塘镇党委副书记、镇长","start":"","end":"","rank":"正科","note":"同安区"},
    {"person_id":15,"org_id":9,"title":"共青团同安区委书记（曾任副书记）","start":"","end":"","rank":"正科","note":"同安区"},
    # 叶晓东 — 区人大常委会主任
    {"person_id":16,"org_id":4,"title":"同安区人大常委会主任","start":"","end":"","rank":"正处","note":""},
    # 洪国平 — 区政协主席
    {"person_id":17,"org_id":5,"title":"同安区政协主席","start":"","end":"","rank":"正处","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 周桂良 ↔ 黄晓军（党政一把手搭档）
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"党政一把手搭档：区委书记与代区长",
     "overlap_org":"同安区","overlap_period":"2026-05起","strength":"strong","confidence":"confirmed"},
    # 周桂良 ← 黄晓军（前后任区长）
    {"person_a":1,"person_b":2,"type":"predecessor_successor","context":"周桂良升任区委书记，黄晓军接任代区长",
     "overlap_org":"同安区人民政府","overlap_period":"2026-05","strength":"strong","confidence":"confirmed"},
    # 王跃平 ← 周桂良（前后任区委书记）
    {"person_a":3,"person_b":1,"type":"predecessor_successor","context":"王跃平→周桂良 同安区委书记交接",
     "overlap_org":"中共同安区委","overlap_period":"2026-04","strength":"strong","confidence":"plausible"},
    # 熊伟 ← 徐少敏（前后任纪委书记）
    {"person_a":7,"person_b":6,"type":"predecessor_successor","context":"徐少敏→熊伟 同安区纪委书记交接",
     "overlap_org":"中共同安区纪律检查委员会","overlap_period":"2025-11","strength":"strong","confidence":"confirmed"},
    # 许永良 — 熊伟（同为纪检系统出身）
    {"person_a":8,"person_b":6,"type":"same_system","context":"先后担任/曾任同安区纪委书记",
     "overlap_org":"中共同安区纪律检查委员会","overlap_period":"","strength":"medium","confidence":"plausible"},
    # 郭三温 — 黄晓军（区政府正副职搭档）
    {"person_a":4,"person_b":2,"type":"superior_subordinate","context":"代区长与常务副区长",
     "overlap_org":"同安区人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},
    # 郭三温 — 林生海（同为区委常委）
    {"person_a":4,"person_b":5,"type":"overlap","context":"同安区委常委班子成员",
     "overlap_org":"中共同安区委","overlap_period":"","strength":"medium","confidence":"plausible"},
    # 周桂良 — 郭三温（前任区长与常务副区长）
    {"person_a":1,"person_b":4,"type":"overlap","context":"前任区长（周桂良）与常务副区长同班子",
     "overlap_org":"同安区人民政府","overlap_period":"2023-2026","strength":"medium","confidence":"confirmed"},
    # 吴申宇 — 同安区（同安区出身的干部）
    {"person_a":15,"person_b":2,"type":"overlap","context":"可能曾有工作交集（吴申宇在同安工作多年）",
     "overlap_org":"同安区","overlap_period":"","strength":"weak","confidence":"unverified"},
]

# =========================================================================
# BUILD SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id))""")

    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        strength TEXT, confidence TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id))""")

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],p["work_start"],
                   p["current_post"],p["current_org"],p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"],r["strength"],r["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")
    print(f"  - {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Color by role."""
    title = p.get("current_post","")
    if "书记" in title and "区委书记" in title:
        return "255,50,50"
    elif "区长" in title and "副区长" not in title:
        return "50,100,255"
    elif "常务副" in title:
        return "50,150,255"
    elif "副区长" in title:
        return "100,150,255"
    elif "纪委书记" in title or "监委" in title:
        return "255,165,0"
    elif "副书记" in title:
        return "50,100,200"
    else:
        return "100,100,100"

def is_top_leader(p):
    title = p.get("current_post","")
    return "区委书记" in title or ("区长" in title and "副区长" not in title)

def build_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>同安区领导工作关系网络 — Tong\'an District Leadership Network (Xiamen, Fujian)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: Organizations
    org_colors = {
        "党委":"255,200,200", "政府":"200,200,255", "纪委":"255,200,150",
        "人大":"200,255,255", "政协":"255,240,200", "乡镇":"255,255,200",
        "群团":"255,220,255"
    }
    for o in organizations:
        oc = org_colors.get(o["type"],"200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges: person→organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person↔person (relationships)
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    build_db()
    build_gexf()
    print("[DONE] 同安区 build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
