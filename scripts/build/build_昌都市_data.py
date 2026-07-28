#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 昌都市 (Chamdo/Qamdo), 西藏自治区 leadership network."""

import sqlite3, os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/xizang_昌都市")
DB_PATH = os.path.join(STAGING, "昌都市_network.db")
GEXF_PATH = os.path.join(STAGING, "昌都市_network.gexf")

# =========================================================================
# PERSONS (19 persons: 14 government leaders + 5 key party/connection figures)
# Sources: Official changdu.gov.cn leadership pages (y2023-02), news reports
# =========================================================================
persons = [
    # ── 市委书记 ──
    {"id":1,"name":"庄劲松","gender":"男","ethnicity":"","birth":"1970-03","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市委书记","current_org":"中共昌都市委员会",
     "source":"https://www.163.com/dy/article/JBVKEILF0550HXM1.html (career confirmed) + changdu.gov.cn news"},
    # ── 市长 ──
    {"id":2,"name":"罗庆伍","gender":"男","ethnicity":"藏族","birth":"1971-05","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市委副书记、市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/201903/3121b580f8be457a978463186d6e36c4.shtml"},
    # ── 常务副市长（3位援藏干部）──
    {"id":3,"name":"谭昊","gender":"男","ethnicity":"苗族","birth":"1979-10","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市委副书记、常务副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202509/83b705d678e940c2938f53f4c35ee8d2.shtml"},
    {"id":4,"name":"李树国","gender":"男","ethnicity":"汉族","birth":"1978-11","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市委副书记、常务副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202509/615bc83370fb4b10a28e2a4043ed8da4.shtml"},
    {"id":5,"name":"黄国剑","gender":"男","ethnicity":"汉族","birth":"1978-01","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市委副书记、常务副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202509/40fe20c87d7e45f681e8cc7f31176951.shtml"},
    # ── 副市长 ──
    {"id":6,"name":"蒲玉辉","gender":"男","ethnicity":"汉族","birth":"1972-10","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202309/7a81552c2b0a4f75a071cd6f9b41b7b7.shtml"},
    {"id":7,"name":"尼玛次仁","gender":"男","ethnicity":"藏族","birth":"1970-05","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长、市公安局局长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202007/d49e1c5a285e41fb4bd07df52b8737487.shtml"},
    {"id":8,"name":"吴剑","gender":"男","ethnicity":"汉族","birth":"1973-09","birthplace":"","education":"研究生","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202103/e38dd17fa14b4a62i268a2d4b7483.shtml"},
    {"id":9,"name":"米次","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202508/6366a5492df141fea05df2721b5ee0ce.shtml"},
    {"id":10,"name":"同敏玺绕","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202310/9839d9dac9dd4a6bb3dc44d7c4262f29.shtml"},
    {"id":11,"name":"杨文升","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/201907/2760e3b1738c4093a17b701f6acc8c.shtml"},
    {"id":12,"name":"高晓东","gender":"男","ethnicity":"汉族","birth":"1976-11","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202508/2226de288963403e1726c0280ec3be40.shtml"},
    {"id":13,"name":"卓玛曲西","gender":"女","ethnicity":"藏族","birth":"1975-01","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市副市长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202508/6a15b3032614461ca63bc3475fa99af5.shtml"},
    {"id":14,"name":"平措丁增","gender":"男","ethnicity":"藏族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"昌都市人民政府秘书长","current_org":"昌都市人民政府",
     "source":"https://www.changdu.gov.cn/cdrmzf/c101567/202109/f726b9af58be4545863d67dc7a0458b.shtml"},
    # ── 前任昌都市委书记 ──
    {"id":15,"name":"龚会才","gender":"男","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"西藏自治区党委常委、秘书长","current_org":"中共西藏自治区委员会",
     "source":"https://www.163.com/article/JBVUOGBF05563DJA.html"},
    {"id":16,"name":"罗布顿珠","gender":"男","ethnicity":"藏族","birth":"1960-12","birthplace":"西藏琼结","education":"","party_join":"","work_start":"1978","current_post":"西藏自治区党委常委、常务副主席","current_org":"西藏自治区人民政府",
     "source":"data/tmp/xizang_province/build_西藏自治区_data.py"},
    # ── 昌都籍国家级领导 ──
    {"id":17,"name":"嘎玛泽登","gender":"男","ethnicity":"藏族","birth":"1967-12","birthplace":"西藏江达","education":"","party_join":"1992-05","work_start":"1990-07","current_post":"西藏自治区党委副书记、政府主席","current_org":"西藏自治区人民政府",
     "source":"data/tmp/xizang_province/build_西藏自治区_data.py"},
    {"id":18,"name":"洛桑江村","gender":"男","ethnicity":"藏族","birth":"1957-07","birthplace":"西藏察雅","education":"","party_join":"","work_start":"","current_post":"全国人大常委会副委员长","current_org":"全国人大常委会",
     "source":"data/tmp/xizang_province/build_西藏自治区_data.py"},
    {"id":19,"name":"白玛赤林","gender":"男","ethnicity":"藏族","birth":"1952-01","birthplace":"西藏丁青","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席","current_org":"",
     "source":"data/tmp/xizang_province/build_西藏自治区_data.py"},
    {"id":20,"name":"向巴平措","gender":"男","ethnicity":"藏族","birth":"1947-04","birthplace":"西藏昌都","education":"","party_join":"","work_start":"","current_post":"原西藏自治区政府主席","current_org":"",
     "source":"data/tmp/xizang_province/build_西藏自治区_data.py"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共昌都市委员会","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区昌都市"},
    {"id":2,"name":"昌都市人民政府","type":"政府","level":"地级","parent":"西藏自治区人民政府","location":"西藏自治区昌都市"},
    {"id":3,"name":"中共昌都市纪律检查委员会","type":"纪委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
    {"id":4,"name":"中共昌都市委组织部","type":"党委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
    {"id":5,"name":"中共昌都市委宣传部","type":"党委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
    {"id":6,"name":"中共昌都市委统战部","type":"党委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
    {"id":7,"name":"中共昌都市委政法委","type":"党委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
    {"id":8,"name":"中共西藏自治区委员会","type":"党委","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":9,"name":"西藏自治区人民政府","type":"政府","level":"省级","parent":"","location":"西藏自治区拉萨市"},
    {"id":10,"name":"全国人大常委会","type":"人大","level":"国家级","parent":"","location":"北京市"},
    {"id":11,"name":"那曲市委","type":"党委","level":"地级","parent":"中共西藏自治区委员会","location":"西藏自治区那曲市"},
    {"id":12,"name":"中共昌都市委办公室","type":"党委","level":"地级","parent":"中共昌都市委员会","location":"西藏自治区昌都市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 庄劲松 — 市委书记 (2024.09 至今)
    {"id":1,"person_id":1,"org_id":1,"title":"昌都市委书记","start":"2024-09","end":"至今","rank":"正厅级","note":"2024年9月13日就任"},
    {"id":2,"person_id":1,"org_id":11,"title":"那曲市委书记","start":"2021-09","end":"2024-09","rank":"正厅级","note":""},
    {"id":3,"person_id":1,"org_id":1,"title":"西藏自治区党委宣传部副部长","start":"","end":"","rank":"","note":"早期在自治区党委宣传部工作"},
    {"id":4,"person_id":1,"org_id":1,"title":"西藏自治区政府驻成都办事处主任","start":"2012-12","end":"2018-09","rank":"正厅级","note":"2012年底赴任"},
    # 罗庆伍 — 市长
    {"id":5,"person_id":2,"org_id":2,"title":"昌都市市长","start":"","end":"至今","rank":"正厅级","note":"主持市政府全面工作，分管审计局"},
    # 3 位常务副市长（援藏干部）
    {"id":6,"person_id":3,"org_id":2,"title":"昌都市委副书记、常务副市长","start":"","end":"","rank":"副厅级","note":"援藏干部，分管国资委、招商、开发区"},
    {"id":7,"person_id":4,"org_id":2,"title":"昌都市委副书记、常务副市长","start":"","end":"","rank":"副厅级","note":"援藏干部，分管科技、文旅、融媒体"},
    {"id":8,"person_id":5,"org_id":2,"title":"昌都市委副书记、常务副市长","start":"","end":"","rank":"副厅级","note":"援藏干部，分管司法、卫健、医保"},
    # 副市长
    {"id":9,"person_id":6,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管教育、民政、退役"},
    {"id":10,"person_id":7,"org_id":2,"title":"昌都市副市长、市公安局局长","start":"","end":"","rank":"副厅级","note":"负责维稳、公安"},
    {"id":11,"person_id":8,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管民委、交通、信访"},
    {"id":12,"person_id":9,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管住建、市场监管、城管"},
    {"id":13,"person_id":10,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管自然资源、生态环境、林业"},
    {"id":14,"person_id":11,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管水利、农业农村、藏语文"},
    {"id":15,"person_id":12,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管发改、统计、能源"},
    {"id":16,"person_id":13,"org_id":2,"title":"昌都市副市长","start":"","end":"","rank":"副厅级","note":"分管经信、人社、商务"},
    {"id":17,"person_id":14,"org_id":12,"title":"昌都市人民政府秘书长","start":"","end":"","rank":"正处级","note":"主持市政府办公室全面工作"},
    # 前任书记
    {"id":18,"person_id":15,"org_id":1,"title":"昌都市委书记","start":"2023","end":"2024-09","rank":"正厅级","note":"兼任西藏自治区副主席"},
    {"id":19,"person_id":15,"org_id":8,"title":"西藏自治区党委常委、秘书长","start":"2024-07","end":"至今","rank":"副部级","note":""},
    {"id":20,"person_id":16,"org_id":1,"title":"昌都市委书记","start":"2011-11","end":"2017-04","rank":"正厅级","note":""},
    {"id":21,"person_id":16,"org_id":9,"title":"西藏自治区常务副主席","start":"2016-12","end":"","rank":"副部级","note":""},
    # 昌都籍国家级领导
    {"id":22,"person_id":17,"org_id":9,"title":"西藏自治区政府主席","start":"2025-01","end":"","rank":"正部级","note":"昌都江达县籍"},
    {"id":23,"person_id":18,"org_id":10,"title":"全国人大常委会副委员长","start":"2018","end":"","rank":"国家级","note":"昌都察雅县籍"},
    {"id":24,"person_id":19,"org_id":9,"title":"西藏自治区政府主席","start":"2010-01","end":"2013-01","rank":"正部级","note":"昌都丁青县籍"},
    {"id":25,"person_id":20,"org_id":9,"title":"西藏自治区政府主席","start":"2003-03","end":"2010-01","rank":"正部级","note":"昌都市籍"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 党政一把手关系
    {"id":1,"person_a":1,"person_b":2,"type":"superior_subordinate","context":"庄劲松(书记)与罗庆伍(市长)为党政一把手搭档","overlap_org":"中共昌都市委员会","overlap_period":"2024-至今","strength":"strong","confidence":"confirmed"},
    # 市长-常务副市长关系
    {"id":2,"person_a":2,"person_b":3,"type":"superior_subordinate","context":"罗庆伍(市长)与谭昊(常务副市长)","overlap_region":"昌都市人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},
    {"id":3,"person_a":2,"person_b":4,"type":"superior_subordinate","context":"罗庆伍(市长)与李树国(常务副市长)","overlap_region":"昌都市人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},
    {"id":4,"person_a":2,"person_b":5,"type":"superior_subordinate","context":"罗庆伍(市长)与黄国剑(常务副市长)","overlap_region":"昌都市人民政府","overlap_period":"","strength":"strong","confidence":"confirmed"},
    # 书记-前任书记关系
    {"id":5,"person_a":15,"person_b":1,"type":"predecessor_successor","context":"龚会才(前任)之于庄劲松(现任)","overlap_region":"中共昌都市委员会","overlap_period":"2024-09","strength":"strong","confidence":"confirmed"},
    {"id":6,"person_a":16,"person_b":15,"type":"predecessor_successor","context":"罗布顿珠→龚会才","overlap_region":"中共昌都市委员会","overlap_period":"2017-2023","strength":"weak","confidence":"unverified"},
    # 昌都籍干部网络
    {"id":7,"person_a":17,"person_b":18,"type":"same_hometown","context":"昌都籍国家级领导——嘎玛泽登(江达),洛桑江村(察雅)","overlap_region":"昌都","overlap_period":"","strength":"weak","confidence":"unverified"},
    {"id":8,"person_a":17,"person_b":19,"type":"same_hometown","context":"昌都籍国家级领导——嘎玛泽登(江达),白玛赤林(丁青)","overlap_region":"昌都","overlap_period":"","strength":"weak","confidence":"unverified"},
    {"id":9,"person_a":17,"person_b":20,"type":"same_hometown","context":"昌都籍藏族领导","overlap_region":"昌都","overlap_period":"","strength":"weak","confidence":"unverified"},
    # 庄劲松的前任那曲书记关系
    {"id":10,"person_a":1,"person_b":16,"type":"indirect_successor","context":"庄劲松接替那曲市委书记(2021)→后任昌都书记", "overlap_region":"","overlap_period":"","strength":"weak","confidence":"unverified"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================
def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def person_color(p):
    current = p.get("current_post","")
    if "书记" in current and "副" not in current and "纪委" not in current:
        return "255,50,50"
    if "市长" in current or "专员" in current:
        return "50,100,255"
    if "纪委" in current or "纪律" in current:
        return "255,165,0"
    if "常务副" in current:
        return "100,150,255"
    return "140,140,140"

def is_top_leader(p):
    pos = p.get("current_post","")
    # Party secretaries (书记) and mayors/chiefs (市长/专员/主席) are top leaders
    if "书记" in pos and "副" not in pos:
        return True
    if "市长" in pos and "副" not in pos:
        return True
    if "专员" in pos:
        return True
    if "副委员长" in pos or "主席" in pos:
        return True
    return False

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons(
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
        );
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_region TEXT, overlap_period TEXT
        );
    """)
    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o.get("type",""), o.get("level",""),
                   o.get("parent",""), o.get("location","")))
    for pos in positions:
        c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""),
                   pos.get("note","")))
    for r in relationships:
        c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
                  (r["id"], r["person_a"], r["person_b"], r["type"],
                   r["context"], r.get("overlap_region",""), r.get("overlap_period","")))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def org_color(o):
        ot = o.get("type","")
        if "党委" == ot or "纪委" == ot: return "255,200,200"
        if "政府" in ot: return "200,200,255"
        if "人大" in ot: return "200,255,255"
        if "政协" in ot: return "255,240,200"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>昌都市领导关系网络 - Chamdo Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('      <attribute id="3" title="ethnicity" type="string"/>')
    lines.append('      <attribute id="4" title="birth" type="string"/>')
    lines.append('      <attribute id="5" title="birthplace" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        r, g, b = c.split(",")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("ethnicity",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="5" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        co = org_color(o).split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{co[0]}" g="{co[1]}" b="{co[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value=" 组织"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <v:color r="180" g="180" b="180"/>')
        lines.append(f'        <v:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
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
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print("Done. 昌都市 network built.")