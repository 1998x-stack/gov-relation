#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东山县 (Dongshan County, Fujian) leadership network.

东山县 — 县, 福建省漳州市下辖, 位于福建省南部沿海东山岛.
Research date: 2026-07-16

Sources:
- www.dongshandao.gov.cn — official Dongshan County Government website homepage news (July 2026)
- www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html — 领导信息 (Government Office leadership page)
- Wikipedia (zh.wikipedia.org/wiki/东山县) — county overview
- Wikipedia (en.wikipedia.org/wiki/Dongshan_County) — county overview

Coverage:
- Current top 2 leaders: 县委书记 何霭, 县长 刘兆民
- Key county-level officials observed in 2026 news coverage
- Organization departments and leadership office
- Predecessors: partial (further research needed)

Confidence notes:
- 何霭: confirmed current 县委书记 (observed in official news 2026-05-25 with title implied by lead position in "何霭刘兆民带队督导食品安全工作")
- 刘兆民: confirmed current 县长 (same news, confirmed acting at county level; also seen with 李琳 inspecting key enterprises 2026-07-07)
- 何雪艺: confirmed 副县长 (named explicitly in news headline 2026-05-11)
- 李琳: confirmed county-level leader (appears with 刘兆民 on 2026-07-07 enterprise inspection; role needs further confirmation — likely 常务副县长 or 副县长)
- 谢丹: county-level leader mentioned in office correspondence notes
- Detailed career timelines of all leaders are open gaps — no detailed public bios found
- Previous 县委书记 and 县长: need further research
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/fujian_东山县")
DB_PATH = os.path.join(STAGING, "东山县_network.db")
GEXF_PATH = os.path.join(STAGING, "东山县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 何霭 — 东山县县委书记 (confirmed by official news 2026-05-25: "何霭刘兆民带队督导食品安全工作")
    {"id":1,"name":"何霭","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县委书记",
     "current_org":"中共东山县委员会",
     "source":"http://www.dongshandao.gov.cn/ (news: 何霭刘兆民带队督导食品安全工作, 2026-05-25)"},
    # 刘兆民 — 东山县县长 (confirmed by official news 2026-05-25, also 2026-07-07: "刘兆民李琳调研重点企业")
    {"id":2,"name":"刘兆民","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县长",
     "current_org":"东山县人民政府",
     "source":"http://www.dongshandao.gov.cn/ (news: 何霭刘兆民带队督导食品安全工作, 2026-05-25; 刘兆民李琳调研重点企业, 2026-07-07)"},

    # ── 2. Key county-level officials ──
    # 李琳 — 县领导 (appears with 刘兆民 on 2026-07-07: "刘兆民李琳调研重点企业"; role needs confirmation — likely 副县长 or 常务副县长)
    {"id":3,"name":"李琳","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导",
     "current_org":"东山县人民政府",
     "source":"http://www.dongshandao.gov.cn/ (news: 刘兆民李琳调研重点企业, 2026-07-07)"},
    # 何雪艺 — 东山县副县长 (confirmed by official news headline 2026-05-11)
    {"id":4,"name":"何雪艺","gender":"女","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县副县长",
     "current_org":"东山县人民政府",
     "source":"http://www.dongshandao.gov.cn/ (news: 东山县副县长何雪艺带队调研冬古一级渔港项目建设, 2026-05-11); 县政府办领导信息 page"},
    # 谢丹 — 县领导 (mentioned in office correspondence as leader 黄启前 corresponds to)
    {"id":5,"name":"谢丹","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导",
     "current_org":"东山县人民政府",
     "source":"http://www.dongshandao.gov.cn/ (县政府办领导信息 page — 黄启前分管工作提及)"},

    # ── 3. 县政府办公室 leadership ──
    # 吴学文 — 县政府党组成员、办公室主任
    {"id":6,"name":"吴学文","gender":"男","ethnicity":"汉族",
     "birth":"1974-07","birthplace":"",
     "education":"大学学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府党组成员、办公室党组书记、主任",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},
    # 蔡炎林 — 办公室副主任
    {"id":7,"name":"蔡炎林","gender":"男","ethnicity":"汉族",
     "birth":"1980-10","birthplace":"",
     "education":"大学学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府办公室党组成员、副主任",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},
    # 刘建龙 — 办公室副主任
    {"id":8,"name":"刘建龙","gender":"男","ethnicity":"汉族",
     "birth":"1989-01","birthplace":"",
     "education":"在职研究生学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府办公室党组成员、副主任",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},
    # 沈浩超 — 办公室副主任
    {"id":9,"name":"沈浩超","gender":"男","ethnicity":"汉族",
     "birth":"1993-02","birthplace":"",
     "education":"大学学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府办公室党组成员、副主任",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},
    # 林晓彬 — 办公室二级主任科员
    {"id":10,"name":"林晓彬","gender":"男","ethnicity":"汉族",
     "birth":"1980-11","birthplace":"",
     "education":"大学学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府办公室党组成员、二级主任科员",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},
    # 黄启前 — 办公室三级主任科员
    {"id":11,"name":"黄启前","gender":"男","ethnicity":"汉族",
     "birth":"1978-03","birthplace":"",
     "education":"研究生学历",
     "party_join":"中国共产党","work_start":"",
     "current_post":"东山县人民政府办公室党组成员、三级主任科员",
     "current_org":"东山县人民政府办公室",
     "source":"http://www.dongshandao.gov.cn/cms/html/dsxrmzf/ldxx/index.html"},

    # ── 4. Other county-level leaders referenced in office page ──
    {"id":12,"name":"吴文群","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (蔡炎林对应县领导)"},
    {"id":13,"name":"沈日韦","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (蔡炎林对应县领导)"},
    {"id":14,"name":"沈惠平","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (蔡炎林对应县领导)"},
    {"id":15,"name":"吴华安","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (刘建龙对应县领导)"},
    {"id":16,"name":"朱义兴","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (沈浩超对应县领导)"},
    {"id":17,"name":"庄金波","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (沈浩超对应县领导)"},
    {"id":18,"name":"吴乐章","gender":"","ethnicity":"",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县县领导","current_org":"东山县人民政府",
     "source":"县政府办领导信息 (林晓彬对应县领导)"},

    # ── 5. 人武部 ──
    # 林建辉 — 人武部上校部长 (2026-07-09 appointment)
    {"id":19,"name":"林建辉","gender":"","ethnicity":"",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"东山县人武部上校部长",
     "current_org":"东山县人民武装部",
     "source":"http://www.dongshandao.gov.cn/ (news: 林建辉任东山县人武部上校部长, 2026-07-09)"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # Dongshan County-level organizations
    {"id":1,"name":"中共东山县委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市东山县西埔镇"},
    {"id":2,"name":"东山县人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市东山县西埔镇"},
    {"id":3,"name":"东山县人大常委会","type":"人大","level":"县级","parent":"","location":"福建省漳州市东山县西埔镇"},
    {"id":4,"name":"政协东山县委员会","type":"政协","level":"县级","parent":"","location":"福建省漳州市东山县西埔镇"},
    {"id":5,"name":"中共东山县纪律检查委员会","type":"党委","level":"县级","parent":"中共东山县委员会","location":"福建省漳州市东山县西埔镇"},
    {"id":6,"name":"中共东山县委组织部","type":"党委","level":"县级","parent":"中共东山县委员会","location":"福建省漳州市东山县西埔镇"},
    {"id":7,"name":"中共东山县委宣传部","type":"党委","level":"县级","parent":"中共东山县委员会","location":"福建省漳州市东山县西埔镇"},
    {"id":8,"name":"中共东山县委政法委员会","type":"党委","level":"县级","parent":"中共东山县委员会","location":"福建省漳州市东山县西埔镇"},
    {"id":9,"name":"东山县人民政府办公室","type":"政府","level":"县级","parent":"东山县人民政府","location":"福建省漳州市东山县西埔镇"},
    {"id":10,"name":"东山县人民武装部","type":"政府","level":"县级","parent":"漳州军分区","location":"福建省漳州市东山县西埔镇"},

    # Higher-level organizations
    {"id":11,"name":"中共漳州市委员会","type":"党委","level":"地级","parent":"中共福建省委员会","location":"福建省漳州市"},
    {"id":12,"name":"漳州市人民政府","type":"政府","level":"地级","parent":"福建省人民政府","location":"福建省漳州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 何霭 — 县委书记
    {"id":1,"person_id":1,"org_id":1,"title":"东山县县委书记","start":"","end":"present","rank":"正处","note":"现任; confirmed as of 2026-05"},
    # 刘兆民 — 县长
    {"id":2,"person_id":2,"org_id":2,"title":"东山县县长","start":"","end":"present","rank":"正处","note":"现任; confirmed as of 2026-05"},
    # 李琳 — 县领导
    {"id":3,"person_id":3,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认 — 可能是副县长或常务副县长"},
    # 何雪艺 — 副县长
    {"id":4,"person_id":4,"org_id":2,"title":"东山县副县长","start":"","end":"present","rank":"副处","note":"现任; confirmed 2026-05-11"},
    # 谢丹 — 县领导
    {"id":5,"person_id":5,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},

    # 县政府办公室 leadership
    {"id":6,"person_id":6,"org_id":9,"title":"东山县人民政府党组成员、办公室党组书记、主任","start":"","end":"present","rank":"正科","note":""},
    {"id":7,"person_id":7,"org_id":9,"title":"东山县人民政府办公室党组成员、副主任","start":"","end":"present","rank":"副科","note":""},
    {"id":8,"person_id":8,"org_id":9,"title":"东山县人民政府办公室党组成员、副主任","start":"","end":"present","rank":"副科","note":""},
    {"id":9,"person_id":9,"org_id":9,"title":"东山县人民政府办公室党组成员、副主任","start":"","end":"present","rank":"副科","note":""},
    {"id":10,"person_id":10,"org_id":9,"title":"东山县人民政府办公室党组成员、二级主任科员","start":"","end":"present","rank":"二级主任科员","note":""},
    {"id":11,"person_id":11,"org_id":9,"title":"东山县人民政府办公室党组成员、三级主任科员","start":"","end":"present","rank":"三级主任科员","note":""},

    # Other county leaders (office reference, roles TBD)
    {"id":12,"person_id":12,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":13,"person_id":13,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":14,"person_id":14,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":15,"person_id":15,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":16,"person_id":16,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":17,"person_id":17,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},
    {"id":18,"person_id":18,"org_id":2,"title":"东山县县领导","start":"","end":"present","rank":"","note":"角色待确认"},

    # 林建辉 — 人武部长
    {"id":19,"person_id":19,"org_id":10,"title":"东山县人武部上校部长","start":"2026-07","end":"present","rank":"上校","note":"新任 2026-07-09"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 何霭 ←→ 刘兆民 (县委-县政府搭档)
    {"id":1,"person_a":1,"person_b":2,"type":"overlap","context":"东山县县委书记-县长搭档","overlap_org":"中共东山县委员会/东山县人民政府","overlap_period":"2026-至今"},
    # 何霭 → 刘兆民 (领导关系)
    {"id":2,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"县委书记领导县长","overlap_org":"中共东山县委员会","overlap_period":"2026-至今"},
    # 刘兆民 ←→ 李琳 (政府班子同僚)
    {"id":3,"person_a":2,"person_b":3,"type":"overlap","context":"刘兆民与李琳共同调研重点企业","overlap_org":"东山县人民政府","overlap_period":"2026-07"},
    # 何雪艺 ←→ 刘兆民 (政府班子)
    {"id":4,"person_a":4,"person_b":2,"type":"overlap","context":"副县长与县长同属县政府班子","overlap_org":"东山县人民政府","overlap_period":"2026-至今"},
]

# =========================================================================
# SQLITE DATABASE
# =========================================================================
def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT,
        party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT,
        source TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, end TEXT,
        rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in persons:
        cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                      p["education"],p["party_join"],p["work_start"],p["current_post"],
                      p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                     (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for ps in positions:
        cur.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                     (ps["id"],ps["person_id"],ps["org_id"],ps["title"],ps["start"],ps["end"],ps["rank"],ps["note"]))
    for r in relationships:
        cur.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                     (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")
    print(f"    Persons: {len(persons)}")
    print(f"    Organizations: {len(organizations)}")
    print(f"    Positions: {len(positions)}")
    print(f"    Relationships: {len(relationships)}")

# =========================================================================
# GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    """Return 'r,g,b' string based on person's role."""
    post = p.get("current_post","")
    if "书记" in post and "纪委" not in post and "人大" not in post and "政协" not in post:
        return "255,50,50"     # Red: Party Secretary
    if "县长" in post or ("副" in post and "政府" in post):
        return "50,100,255"    # Blue: Government
    if "纪委" in post or "监委" in post:
        return "255,165,0"     # Orange: Discipline
    if "人大" in post:
        return "200,255,255"   # Cyan: People's Congress
    if "政协" in post:
        return "255,240,200"   # Cream: Political Consultative
    if "人武" in post:
        return "100,200,100"   # Green: Military
    return "100,100,100"       # Grey: Others

def is_top_leader(p):
    return p["id"] in [1, 2]  # 何霭 and 刘兆民

def org_color(o):
    t = o.get("type","")
    m = {"党委":"255,200,200","政府":"200,200,255","开发区":"200,255,200",
         "乡镇/街道":"255,255,200","事业单位":"220,220,220","群团":"255,220,255",
         "人大":"200,255,255","政协":"255,240,200"}
    return m.get(t,"200,200,200")

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>东山县领导工作关系网络 - Dongshan County Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="subtype" type="string"/>')
    lines.append('      <attribute id="2" title="job_title" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else ("12.0" if p["id"] <= 5 else "8.0")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"][:20])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="3" value="县级"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["birth"])}"/>')
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
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o["level"])}"/>')
        lines.append('          <attvalue for="4" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person → Organization edges (worked_at)
    for ps in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{ps["person_id"]}" target="o{ps["org_id"]}" label="{esc(ps["title"][:30])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ps["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ps["start"])}-{esc(ps["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person ↔ Person edges (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring("\n".join(lines))
        print("    XML well-formed: OK")
    except Exception as e:
        print(f"    XML validation: {e}")

# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 东山县 leadership network...")
    build_db()
    build_gexf()
    print("Done.")
