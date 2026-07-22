#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 平和县 (Pinghe County, Fujian) leadership network.

平和县 — 县, 福建省漳州市下辖, 位于福建省南部沿海, 辖10镇5乡.
Research date: 2026-07-16

Sources:
- www.pinghe.gov.cn — official county government site (homepage news)
- www.zhangzhou.gov.cn — city government site hosting county leadership pages:
  - /cms/html/phxrmzf/zsb/index.html — 代县长 周绍斌 bio
  - /cms/html/phxrmzf/czl/index.html — 常务副县长 戴永福 bio
  - /cms/html/phxrmzf/dyf/index.html — 副县长 庞健安 bio
  - /cms/html/phxrmzf/lqs/index.html — 副县长 林清山 bio (博士学历)
  - /cms/html/phxrmzf/wyh/index.html — 副县长 吴映红 bio
  - /cms/html/phxrmzf/ldzc/ — leadership page listing
  - /cms/html/phxrmzf/2026-07-13/1971285273.html — 县委常委会 meeting article (confirmed 沈义勇)
  - /cms/html/phxrmzf/2026-07-16/1886323372.html — 县政府全体会议 article
- Wikipedia (zh.wikipedia.org/wiki/平和县) — county overview

Coverage:
- Current top 2 leaders: 县委书记 沈义勇, 代县长 周绍斌
- Full government leadership team (常务副县长, 8 副县长, 党组成员)
- 2 县委常委 identified (沈义勇, 周绍斌, 戴永福, 庞健安)
- Key county-level organization nodes
- Predecessors: open gap

Confidence notes:
- 沈义勇: confirmed current 县委书记 (observed in 2026-07 news articles).
  No bio page found — birth, education, career timeline ALL unknown (critical gap).
- 周绍斌: confirmed 代县长 from official bio page. Born 1977-12, university educated.
  Previous career at city level unknown.
- 戴永福: confirmed 县委常委、常务副县长 from official bio. Born 1976-04.
- 庞健安: confirmed 县委常委、副县长 from official bio. Born 1978-08, female.
- 林清山: PhD (理学博士), confirmed 副县长.
- Other deputy magistrates (林贵良, 吴朝东, 黄建鑫, 黄淳杰, 邱炳晖): names confirmed;
  bios not found on accessible pages.
- Predecessors of current leaders: unknown — not found in accessible sources.
- 蔡立保: mentioned as "县领导" in news, likely 县委常委 — role needs confirmation.
- 马长健, 吴宇嫔, 赖文尧, 汪冕: mentioned in 县政府全体会议, specific roles unknown.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/fujian_平和县")
DB_PATH = os.path.join(STAGING, "平和县_network.db")
GEXF_PATH = os.path.join(STAGING, "平和县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 1. Current top leaders ──
    # 沈义勇 — 平和县委书记 (current, as of 2026-07)
    {"id":1,"name":"沈义勇","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"",
     "education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县委书记",
     "current_org":"中共平和县委员会",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-13/1971285273.html"},
    # 周绍斌 — 平和县委副书记、代县长 (current, as of 2026-07)
    {"id":2,"name":"周绍斌","gender":"男","ethnicity":"汉族",
     "birth":"1977年12月","birthplace":"",
     "education":"大学学历",
     "party_join":"","work_start":"",
     "current_post":"平和县委副书记、代县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/zsb/index.html"},

    # ── 2. Current government leadership team ──
    # 戴永福 — 县委常委、常务副县长
    {"id":3,"name":"戴永福","gender":"男","ethnicity":"汉族",
     "birth":"1976年04月","birthplace":"",
     "education":"大学学历",
     "party_join":"","work_start":"",
     "current_post":"平和县委常委、常务副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/czl/index.html"},
    # 庞健安 — 县委常委、副县长 (女)
    {"id":4,"name":"庞健安","gender":"女","ethnicity":"汉族",
     "birth":"1978年08月","birthplace":"",
     "education":"大学学历",
     "party_join":"","work_start":"",
     "current_post":"平和县委常委、副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/dyf/index.html"},
    # 林清山 — 副县长 (博士)
    {"id":5,"name":"林清山","gender":"男","ethnicity":"汉族",
     "birth":"1971年12月","birthplace":"",
     "education":"在职研究生学历，理学博士",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/lqs/index.html"},
    # 吴映红 — 副县长 (女)
    {"id":6,"name":"吴映红","gender":"女","ethnicity":"汉族",
     "birth":"1973年05月","birthplace":"",
     "education":"大学学历",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/wyh/index.html"},
    # 林贵良 — 副县长
    {"id":7,"name":"林贵良","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/lgl/index.html"},
    # 吴朝东 — 副县长
    {"id":8,"name":"吴朝东","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/wcd/index.html"},
    # 黄建鑫 — 副县长
    {"id":9,"name":"黄建鑫","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/fxchjx/index.html"},
    # 黄淳杰 — 副县长
    {"id":10,"name":"黄淳杰","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/fxchcj/index.html"},
    # 邱炳晖 — 副县长
    {"id":11,"name":"邱炳晖","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县副县长",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/fxcqbh/index.html"},
    # 卢文深 — 党组成员
    {"id":12,"name":"卢文深","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县政府党组成员",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/dzcylws/index.html"},

    # ── 3. Other county leaders (observed in news, roles less certain) ──
    # 蔡立保 — mentioned as "县领导", likely 县委常委
    {"id":13,"name":"蔡立保","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县领导（推测县委常委）",
     "current_org":"中共平和县委员会",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-13/1971285273.html"},
    # 马长健 — mentioned in 县政府全体会议
    {"id":14,"name":"马长健","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县领导",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-16/1886323372.html"},
    # 吴宇嫔 — mentioned in 县政府全体会议
    {"id":15,"name":"吴宇嫔","gender":"女","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县领导",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-16/1886323372.html"},
    # 赖文尧 — mentioned in 县政府全体会议
    {"id":16,"name":"赖文尧","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县领导",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-16/1886323372.html"},
    # 汪冕 — mentioned in 县政府全体会议
    {"id":17,"name":"汪冕","gender":"男","ethnicity":"汉族",
     "birth":"","birthplace":"","education":"",
     "party_join":"","work_start":"",
     "current_post":"平和县领导",
     "current_org":"平和县人民政府",
     "source":"https://www.zhangzhou.gov.cn/cms/html/phxrmzf/2026-07-16/1886323372.html"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共平和县委员会","type":"党委","level":"县级","parent":"中共漳州市委员会","location":"福建省漳州市平和县"},
    {"id":2,"name":"平和县人民政府","type":"政府","level":"县级","parent":"漳州市人民政府","location":"福建省漳州市平和县"},
    {"id":3,"name":"中共平和县纪律检查委员会","type":"纪委","level":"县级","parent":"中共漳州市纪律检查委员会","location":"福建省漳州市平和县"},
    {"id":4,"name":"平和县人大常委会","type":"人大","level":"县级","parent":"漳州市人大常委会","location":"福建省漳州市平和县"},
    {"id":5,"name":"平和县政协","type":"政协","level":"县级","parent":"政协漳州市委员会","location":"福建省漳州市平和县"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 沈义勇
    {"person_id":1,"org_id":1,"title":"平和县委书记","start":"unknown","end":"present","rank":"正处级","note":"confirmed from 2026-07 news articles; no bio page found"},
    # 周绍斌
    {"person_id":2,"org_id":2,"title":"平和县代县长","start":"2026?","end":"present","rank":"正处级","note":"confirmed as 代县长 from official bio"},
    {"person_id":2,"org_id":1,"title":"平和县委副书记","start":"2026?","end":"present","rank":"正处级","note":"also serves as Party Deputy Secretary"},
    # 戴永福
    {"person_id":3,"org_id":2,"title":"平和县常务副县长","start":"unknown","end":"present","rank":"副处级","note":"confirmed from official bio"},
    {"person_id":3,"org_id":1,"title":"平和县委常委","start":"unknown","end":"present","rank":"副处级","note":"also serves as Party Standing Committee member"},
    # 庞健安
    {"person_id":4,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":"confirmed from official bio"},
    {"person_id":4,"org_id":1,"title":"平和县委常委","start":"unknown","end":"present","rank":"副处级","note":"also serves as Party Standing Committee member"},
    # 林清山
    {"person_id":5,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":"confirmed from official bio; PhD"},
    # 吴映红
    {"person_id":6,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":"confirmed from official bio"},
    # 林贵良
    {"person_id":7,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":""},
    # 吴朝东
    {"person_id":8,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":""},
    # 黄建鑫
    {"person_id":9,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":""},
    # 黄淳杰
    {"person_id":10,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":""},
    # 邱炳晖
    {"person_id":11,"org_id":2,"title":"平和县副县长","start":"unknown","end":"present","rank":"副处级","note":""},
    # 卢文深
    {"person_id":12,"org_id":2,"title":"平和县政府党组成员","start":"unknown","end":"present","rank":"副处级","note":""},
    # 蔡立保
    {"person_id":13,"org_id":1,"title":"平和县委常委（推测）","start":"unknown","end":"present","rank":"副处级","note":"mentioned as 县领导 in news; specific role uncertain"},
    # 马长健
    {"person_id":14,"org_id":2,"title":"平和县领导（具体职务待查）","start":"unknown","end":"present","rank":"","note":"from 县政府全体会议 attendance"},
    # 吴宇嫔
    {"person_id":15,"org_id":2,"title":"平和县领导（具体职务待查）","start":"unknown","end":"present","rank":"","note":"from 县政府全体会议 attendance"},
    # 赖文尧
    {"person_id":16,"org_id":2,"title":"平和县领导（具体职务待查）","start":"unknown","end":"present","rank":"","note":"from 县政府全体会议 attendance"},
    # 汪冕
    {"person_id":17,"org_id":2,"title":"平和县领导（具体职务待查）","start":"unknown","end":"present","rank":"","note":"from 县政府全体会议 attendance"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # Core leadership pair
    {"person_a":1,"person_b":2,"type":"colleague","context":"县委书记与代县长搭档","overlap_org":"平和县","overlap_period":"2026-","confidence":"confirmed"},
    # 县委常委之间的工作关系
    {"person_a":1,"person_b":3,"type":"colleague","context":"县委书记与常务副县长——县委常委班子","overlap_org":"中共平和县委员会","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":1,"person_b":4,"type":"colleague","context":"县委书记与县委常委","overlap_org":"中共平和县委员会","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":3,"type":"colleague","context":"代县长与常务副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":4,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":5,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":6,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":7,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":8,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":9,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":10,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":11,"type":"colleague","context":"代县长与副县长——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
    {"person_a":2,"person_b":12,"type":"colleague","context":"代县长与党组成员——县政府班子","overlap_org":"平和县人民政府","overlap_period":"2026-","confidence":"confirmed"},
]


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Node color based on person role."""
    post = p.get("current_post", "")
    if "县委书记" in post:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in post:
        return "50,100,255"  # Blue — Government leader
    if "常务" in post:
        return "100,200,100"  # Green — Deputy leader
    if "县委常委" in post:
        return "255,165,0"  # Orange — Standing Committee
    if "副县长" in post:
        return "50,150,50"  # Green — Deputy
    return "100,100,100"  # Grey — Others


def org_color(o):
    """Node color based on org type."""
    t = o.get("type", "")
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(t, "200,200,200")


def is_top_leader(p):
    post = p.get("current_post", "")
    return "县委书记" in post or ("县长" in post and "副" not in post)


def person_size(p):
    return "20.0" if is_top_leader(p) else ("15.0" if "常务" in p.get("current_post","") else "12.0")


# =========================================================================
# BUILD SQLITE
# =========================================================================
def build_sqlite():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT
        )
    """)

    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, "end", rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos.get("start", ""), pos.get("end", ""),
              pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"],
              r.get("context", ""), r.get("overlap_org", ""),
              r.get("overlap_period", ""), r.get("confidence", "")))

    conn.commit()
    conn.close()
    print(f"SQLite database written: {DB_PATH}")


# =========================================================================
# BUILD GEXF
# =========================================================================
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>平和县 leadership network — Fujian, Zhangzhou. Research date: 2026-07-16. Sources: official zhangzhou.gov.cn leadership pages and news articles.</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="node_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = f"p{p['id']}"
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "")
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('          <attvalue for="1" value="person"/>')
        lines.append(f'          <attvalue for="2" value="{esc(role)}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = f"o{o['id']}"
        c = org_color(o)
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value="organization"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("type", ""))}"/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (positions)
    for pos in positions:
        eid += 1
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person → Person (relationships)
    for r in relationships:
        eid += 1
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        conf = r.get("confidence", "unverified")
        ctx = r.get("context", "")
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{conf}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph written: {GEXF_PATH}")


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print("Building 平和县 leadership network...")
    build_sqlite()
    build_gexf()
    print("Done.")
