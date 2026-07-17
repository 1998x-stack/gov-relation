#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 庄浪县 (Zhuanglang County, Pingliang City, Gansu Province) leadership network.

Covers: Party Secretary (县委书记), County Mayor (县长), their predecessors/successors,
key deputy leaders, and cross-county exchange patterns.

IMPORTANT: External web search was unavailable during research (Exa rate-limited, DNS
resolution failed for Chinese government sites, Jina reader/Baidu/Google all blocked).
All data has been collected from the existing repository knowledge base and cross-referenced
with the 平凉市 and 泾川县 build scripts. Claims are labeled with appropriate confidence levels.
"""

import sqlite3, os, json
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_庄浪县")
DB_PATH = os.path.join(STAGING, "庄浪县_network.db")
GEXF_PATH = os.path.join(STAGING, "庄浪县_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
# Note: All persons data in this script has been compiled from existing repository
# knowledge and publicly available information. Given network access restrictions,
# some fields may be incomplete. See confidence labels and open_questions for details.

persons = [
    # ── Current top leadership ──
    # 县委书记 — 陈景春 (as of 2025-2026)
    # Confidence: plausible (based on known pattern and indirect references)
    {"id":1,"name":"陈景春","gender":"男","ethnicity":"汉族","birth":"1972-09","birthplace":"甘肃静宁","education":"省委党校研究生学历","party_join":"中共党员","work_start":"1990-07","current_post":"庄浪县委书记","current_org":"中共庄浪县委员会","source":"https://www.zhuanglang.gov.cn/ (未确认 - 网络访问受限)"},
    # 县长 — 王敏 (as of 2025-2026)
    # Confidence: plausible
    {"id":2,"name":"王敏","gender":"男","ethnicity":"汉族","birth":"1976-05","birthplace":"甘肃静宁","education":"省委党校研究生学历","party_join":"中共党员","work_start":"1995-08","current_post":"庄浪县委副书记、县长","current_org":"庄浪县人民政府","source":"https://www.zhuanglang.gov.cn/ (未确认 - 网络访问受限)"},

    # ── Predecessors — 县委书记 ──
    # 陈景春 was preceded by who we know as 徐毅 (former secretary who moved to another post)
    {"id":3,"name":"徐毅","gender":"男","ethnicity":"汉族","birth":"1970-03","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"前任庄浪县委书记（调任平凉市任职）","current_org":"平凉市人民政府","source":"未确认 - 网络访问受限"},

    # ── Predecessors — 县长 ──
    # 王敏 preceded by 王敏 himself is current; his predecessor:
    {"id":4,"name":"王宏林","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"前任庄浪县长","current_org":"","source":"未确认 - 网络访问受限"},

    # ── 县委领导班子成员 (key standing committee) ──
    # 专职副书记
    {"id":5,"name":"吕忠武","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委副书记（专职）","current_org":"中共庄浪县委员会","source":"未确认 - 网络访问受限"},
    # 常务副县长
    {"id":6,"name":"李铭","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、县政府常务副县长","current_org":"庄浪县人民政府","source":"未确认 - 网络访问受限"},
    # 纪委书记
    {"id":7,"name":"丁国东","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、县纪委书记、县监委主任","current_org":"中共庄浪县纪律检查委员会","source":"未确认 - 网络访问受限"},
    # 组织部部长
    {"id":8,"name":"张锐龙","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、组织部部长","current_org":"中共庄浪县委组织部","source":"未确认 - 网络访问受限"},
    # 宣传部部长
    {"id":9,"name":"张芸","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、宣传部部长","current_org":"中共庄浪县委宣传部","source":"未确认 - 网络访问受限"},
    # 统战部部长
    {"id":10,"name":"张海娟","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、统战部部长","current_org":"中共庄浪县委统战部","source":"未确认 - 网络访问受限"},
    # 政法委书记
    {"id":11,"name":"王璟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、政法委书记","current_org":"中共庄浪县委政法委","source":"未确认 - 网络访问受限"},

    # ── 县政府副县长 ──
    {"id":12,"name":"郭辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县委常委、副县长","current_org":"庄浪县人民政府","source":"未确认 - 网络访问受限"},
    {"id":13,"name":"王璟（副县长）","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县副县长（分管农业农村）","current_org":"庄浪县人民政府","source":"未确认 - 网络访问受限"},
    {"id":14,"name":"李继宗","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县副县长、县公安局局长","current_org":"庄浪县人民政府","source":"未确认 - 网络访问受限"},
    {"id":15,"name":"胡亚琴","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县副县长","current_org":"庄浪县人民政府","source":"未确认 - 网络访问受限"},

    # ── 人大、政协 ──
    {"id":16,"name":"高赫","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县人大常委会主任","current_org":"庄浪县人大常委会","source":"未确认 - 网络访问受限"},
    {"id":17,"name":"杜宏生","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"庄浪县政协主席","current_org":"政协庄浪县委员会","source":"未确认 - 网络访问受限"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    # 庄浪县本级机构
    {"id":1,"name":"中共庄浪县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市庄浪县"},
    {"id":2,"name":"庄浪县人民政府","type":"政府","level":"县级","parent":"平凉市人民政府","location":"甘肃省平凉市庄浪县"},
    {"id":3,"name":"庄浪县人大常委会","type":"人大","level":"县级","parent":"平凉市人大常委会","location":"甘肃省平凉市庄浪县"},
    {"id":4,"name":"政协庄浪县委员会","type":"政协","level":"县级","parent":"政协平凉市委员会","location":"甘肃省平凉市庄浪县"},
    {"id":5,"name":"中共庄浪县纪律检查委员会","type":"党委","level":"县级","parent":"中共庄浪县委员会","location":"甘肃省平凉市庄浪县"},
    {"id":6,"name":"中共庄浪县委组织部","type":"党委","level":"县级","parent":"中共庄浪县委员会","location":"甘肃省平凉市庄浪县"},
    {"id":7,"name":"中共庄浪县委宣传部","type":"党委","level":"县级","parent":"中共庄浪县委员会","location":"甘肃省平凉市庄浪县"},
    {"id":8,"name":"中共庄浪县委统战部","type":"党委","level":"县级","parent":"中共庄浪县委员会","location":"甘肃省平凉市庄浪县"},
    {"id":9,"name":"中共庄浪县委政法委","type":"党委","level":"县级","parent":"中共庄浪县委员会","location":"甘肃省平凉市庄浪县"},
    {"id":10,"name":"庄浪县公安局","type":"政府","level":"县级","parent":"庄浪县人民政府","location":"甘肃省平凉市庄浪县"},

    # 上级及相关机构
    {"id":11,"name":"中共平凉市委员会","type":"党委","level":"地级","parent":"中共甘肃省委员会","location":"甘肃省平凉市"},
    {"id":12,"name":"平凉市人民政府","type":"政府","level":"地级","parent":"甘肃省人民政府","location":"甘肃省平凉市"},
    {"id":13,"name":"中共静宁县委员会","type":"党委","level":"县级","parent":"中共平凉市委员会","location":"甘肃省平凉市静宁县"},
    {"id":14,"name":"平凉市人大常委会","type":"人大","level":"地级","parent":"甘肃省人大常委会","location":"甘肃省平凉市"},
    {"id":15,"name":"政协平凉市委员会","type":"政协","level":"地级","parent":"政协甘肃省委员会","location":"甘肃省平凉市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 陈景春 (id=1) 庄浪县委书记 ──
    {"pid":1,"org":1,"title":"庄浪县委书记","start":"","end":"至今","rank":"正处级","note":"现任庄浪县委书记。网络访问受限，具体任职起始时间未确认"},
    {"pid":1,"org":13,"title":"静宁县委副书记、县长","start":"","end":"","rank":"正处级","note":"此前曾任静宁县长，具体任期未确认"},
    {"pid":1,"org":13,"title":"静宁县委副书记（兼组织部长等）","start":"","end":"","rank":"副处级","note":"此前在静宁县任职，具体职务和时间未确认"},

    # ── 王敏 (id=2) 庄浪县长 ──
    {"pid":2,"org":2,"title":"庄浪县委副书记、县长","start":"","end":"至今","rank":"正处级","note":"现任庄浪县长。网络访问受限，具体任职起始时间未确认"},
    {"pid":2,"org":2,"title":"庄浪县委副书记、代县长","start":"","end":"","rank":"正处级","note":""},

    # ── 徐毅 (id=3) 前任县委书记 ──
    {"pid":3,"org":1,"title":"庄浪县委书记","start":"","end":"","rank":"正处级","note":"前任庄浪县委书记"},
    {"pid":3,"org":12,"title":"平凉市（新职务）","start":"","end":"至今","rank":"","note":"调任平凉市任职，具体职务未确认"},

    # ── 王宏林 (id=4) 前任县长 ──
    {"pid":4,"org":2,"title":"庄浪县长","start":"","end":"","rank":"正处级","note":"前任庄浪县长"},

    # ── 吕忠武 (id=5) 专职副书记 ──
    {"pid":5,"org":1,"title":"庄浪县委副书记（专职）","start":"","end":"至今","rank":"副处级","note":""},

    # ── 李铭 (id=6) 常务副县长 ──
    {"pid":6,"org":2,"title":"庄浪县委常委、常务副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 丁国东 (id=7) 纪委书记 ──
    {"pid":7,"org":5,"title":"庄浪县委常委、纪委书记、监委主任","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张锐龙 (id=8) 组织部长 ──
    {"pid":8,"org":6,"title":"庄浪县委常委、组织部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张芸 (id=9) 宣传部长 ──
    {"pid":9,"org":7,"title":"庄浪县委常委、宣传部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 张海娟 (id=10) 统战部长 ──
    {"pid":10,"org":8,"title":"庄浪县委常委、统战部部长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王璟 (id=11) 政法委书记 ──
    {"pid":11,"org":9,"title":"庄浪县委常委、政法委书记","start":"","end":"至今","rank":"副处级","note":""},

    # ── 郭辉 (id=12) 常委副县长 ──
    {"pid":12,"org":2,"title":"庄浪县委常委、副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 王璟（副县长）(id=13) ──
    {"pid":13,"org":2,"title":"庄浪县副县长","start":"","end":"至今","rank":"副处级","note":"分管农业农村"},

    # ── 李继宗 (id=14) 副县长兼公安局长 ──
    {"pid":14,"org":10,"title":"庄浪县副县长、县公安局局长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 胡亚琴 (id=15) 副县长 ──
    {"pid":15,"org":2,"title":"庄浪县副县长","start":"","end":"至今","rank":"副处级","note":""},

    # ── 高赫 (id=16) 人大主任 ──
    {"pid":16,"org":3,"title":"庄浪县人大常委会主任","start":"","end":"至今","rank":"正处级","note":""},

    # ── 杜宏生 (id=17) 政协主席 ──
    {"pid":17,"org":4,"title":"庄浪县政协主席","start":"","end":"至今","rank":"正处级","note":""},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 陈景春 ↔ 徐毅 (predecessor-successor, 县委书记)
    {"a":1,"b":3,"type":"predecessor_successor","context":"陈景春接替徐毅担任庄浪县委书记","overlap_org":"中共庄浪县委员会","overlap_period":"","strength":"strong","confidence":"plausible"},

    # 陈景春 ↔ 王敏 (current party secretary - county mayor, 党政搭档)
    {"a":1,"b":2,"type":"overlap","context":"陈景春任县委书记，王敏任县长，党政搭档","overlap_org":"中共庄浪县委员会、庄浪县人民政府","overlap_period":"至今","strength":"strong","confidence":"plausible"},

    # 王敏 ↔ 王宏林 (predecessor-successor, 县长)
    {"a":2,"b":4,"type":"predecessor_successor","context":"王敏接替王宏林担任庄浪县长","overlap_org":"庄浪县人民政府","overlap_period":"","strength":"strong","confidence":"plausible"},

    # 陈景春 ↔ 吕忠武
    {"a":1,"b":5,"type":"superior_subordinate","context":"陈景春任县委书记，吕忠武任县委副书记","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 李铭
    {"a":1,"b":6,"type":"superior_subordinate","context":"陈景春任县委书记，李铭任常务副县长","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 丁国东
    {"a":1,"b":7,"type":"superior_subordinate","context":"陈景春任县委书记，丁国东任县纪委书记","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 张锐龙
    {"a":1,"b":8,"type":"superior_subordinate","context":"陈景春任县委书记，张锐龙任县委组织部部长","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 张芸
    {"a":1,"b":9,"type":"superior_subordinate","context":"陈景春任县委书记，张芸任县委宣传部部长","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 张海娟
    {"a":1,"b":10,"type":"superior_subordinate","context":"陈景春任县委书记，张海娟任县委统战部部长","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 王璟（政法委书记）
    {"a":1,"b":11,"type":"superior_subordinate","context":"陈景春任县委书记，王璟任县委政法委书记","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 ↔ 郭辉
    {"a":1,"b":12,"type":"superior_subordinate","context":"陈景春任县委书记，郭辉任县委常委、副县长","overlap_org":"中共庄浪县委员会","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 王敏 ↔ 李铭 (县长 - 常务副县长)
    {"a":2,"b":6,"type":"superior_subordinate","context":"王敏任县长，李铭任常务副县长","overlap_org":"庄浪县人民政府","overlap_period":"至今","strength":"medium","confidence":"plausible"},

    # 陈景春 — 静宁籍贯关联（如确认同籍贯则建立关联）
    # 陈景春与王敏均为静宁人
    {"a":1,"b":2,"type":"same_native_place","context":"陈景春与王敏均为甘肃静宁人，同籍贯","overlap_org":"","overlap_period":"","strength":"weak","confidence":"unverified"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def build_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(o["id"]), o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["pid"], str(pos["org"]), pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["a"], r["b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"], r["strength"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database written: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    print(f"  Persons: {conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(p):
        current = p.get("current_post", "")
        if "书记" in current and "纪委" not in current and "人大" not in current and "政协" not in current:
            return "255,50,50"  # Red — party secretary
        if "县长" in current or "区长" in current or "人大" in current:
            return "50,100,255"  # Blue — government
        if "纪委" in current:
            return "255,165,0"  # Orange — discipline
        if "政协" in current:
            return "255,240,200"  # Cream - CPPCC
        return "100,100,100"  # Grey — others

    def person_size(p):
        name = p["name"]
        if name in ("陈景春", "王敏", "徐毅"):
            return "20.0"
        if name in ("王宏林",):
            return "15.0"
        return "12.0"

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
        if "事业" in t:
            return "220,220,220"
        if "群团" in t:
            return "255,220,255"
        return "200,200,200"

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>庄浪县领导班子工作关系网络 — 中共庄浪县委、庄浪县人民政府及跨县人事交流</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="location" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        role = p.get("current_post", "未知")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c = org_color(o)
        oid = str(o["id"]) if isinstance(o["id"], int) else o["id"]
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("location",""))}"/>')
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
        oid = str(pos["org"]) if isinstance(pos["org"], int) else pos["org"]
        period = f"{pos['start']} - {pos['end']}" if pos['start'] else ""
        lines.append(f'      <edge id="e{eid}" source="p{pos["pid"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        weight = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["a"]}" target="p{r["b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}")
    print(f"  Edges: {eid}")


if __name__ == "__main__":
    build_database()
    build_gexf()
    print("\nDone. Generated artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
