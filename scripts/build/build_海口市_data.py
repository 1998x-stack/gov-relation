#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 海口市 (Haikou City) leadership network.

Covers: 市委书记 (party secretary 范少军, also 海南省委常委), 市长 (mayor 张勇),
the full 市政府领导班子 (deputy mayors + 秘书长), the predecessor 市委书记
(罗增斌), and the cross-region transfer chain (上海宝山 → 海南海口).

Focus organs: 中共海口市委员会 (party committee), 海口市人民政府 (municipal
government), 海口市公安局, plus the out-of-Hainan prior posts (上海市宝山区,
四川省绵阳市委) that explain the leadership's career trajectory.

Sources: official 海口市政府门户 (www.haikou.gov.cn leadership bios, accessed
2026-08-06), and local repo research artifacts (海南省 / 宝山区 / 美兰区 /
成都市 datasets).
"""
import sqlite3, os, sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "海口市_network.db")
GEXF_PATH = os.path.join(HERE, "海口市_network.gexf")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── 核心领导：市委书记 (一把手) ──
    # 范少军 — 海南省委常委、海口市委书记（前任 上海市宝山区）
    {"id":1,"name":"范少军","gender":"男","ethnicity":"汉族","birth":"1970-11","birthplace":"江苏邗江","education":"大学学历，工商管理硕士","party_join":"中共党员","work_start":"1992-08","current_post":"海南省委常委、海口市委书记","current_org":"中共海口市委员会","source":"https://baike.baidu.com/ (本地宝山区 DB)"},

    # ── 核心领导：市长 (二把手) ──
    # 张勇 — 海口市委副书记、市政府党组书记、市长
    {"id":2,"name":"张勇","gender":"男","ethnicity":"汉族","birth":"1974-05","birthplace":"","education":"大学，工程硕士，高级工程师，高级经济师","party_join":"中共党员","work_start":"","current_post":"海口市委副书记、市政府党组书记、市长","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202112/t269387.shtml"},

    # ── 市政府领导班子 ──
    {"id":3,"name":"党帅","gender":"男","ethnicity":"汉族","birth":"1984-02","birthplace":"","education":"研究生，工学博士，经济师","party_join":"中共党员","work_start":"","current_post":"海口市委常委、市政府党组副书记、常务副市长","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202607/t1534981.shtml"},
    {"id":4,"name":"仝贵婵","gender":"女","ethnicity":"汉族","birth":"1972-10","birthplace":"","education":"研究生，工学博士","party_join":"中共党员","work_start":"","current_post":"海口市委常委、市政府党组成员、副市长","current_org":"海口市人民政府","source":"本地既有调研（官网）"},
    {"id":5,"name":"吕小蕾","gender":"女","ethnicity":"汉族","birth":"1978-06","birthplace":"","education":"中央党校研究生，经济学学士","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、副市长","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202112/t269370.shtml"},
    {"id":6,"name":"马凯","gender":"男","ethnicity":"汉族","birth":"1968-06","birthplace":"","education":"大学，法学学士","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、副市长（兼市公安局局长）","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202411/t1389763.shtml"},
    {"id":7,"name":"冯勇","gender":"男","ethnicity":"汉族","birth":"1968-06","birthplace":"","education":"中央党校大学","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、副市长","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202307/t1303099.shtml"},
    {"id":8,"name":"何霁锋","gender":"男","ethnicity":"汉族","birth":"1976-03","birthplace":"","education":"在职研究生，在职工商管理硕士","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、副市长","current_org":"海口市人民政府","source":"本地既有调研（官网）"},
    {"id":9,"name":"李翊","gender":"男","ethnicity":"汉族","birth":"1971-09","birthplace":"","education":"大学，经济学硕士","party_join":"民革党员","work_start":"","current_post":"海口市人民政府副市长","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfld/202112/t269378.shtml"},
    {"id":10,"name":"徐健超","gender":"男","ethnicity":"汉族","birth":"1975-11","birthplace":"","education":"中央党校大学","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、副市长","current_org":"海口市人民政府","source":"本地既有调研（官网）"},
    {"id":11,"name":"王晓龙","gender":"男","ethnicity":"汉族","birth":"1973-01","birthplace":"","education":"大学本科，在职法学硕士","party_join":"中共党员","work_start":"","current_post":"海口市政府党组成员、市政府秘书长、办公室主任","current_org":"海口市人民政府","source":"http://www.haikou.gov.cn/xxgk/szfbjxxgk/dzld/zfmsz/202602/t1508153.shtml"},

    # ── 前任 ──
    {"id":12,"name":"罗增斌","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"（前任海口市委书记、海南省委常委）","current_org":"","source":"本地 成都/绵阳 调研（前任绵阳市委书记）"},
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id":1,"name":"中共海口市委员会","type":"党委","level":"地级","parent":"中共海南省委员会","location":"海南省海口市"},
    {"id":2,"name":"海口市人民政府","type":"政府","level":"地级","parent":"海南省人民政府","location":"海南省海口市"},
    {"id":3,"name":"海口市公安局","type":"政府","level":"地级市直","parent":"海口市人民政府","location":"海南省海口市"},
    {"id":4,"name":"上海市宝山区人民政府","type":"政府","level":"省级辖（区）","parent":"上海市人民政府","location":"上海市宝山区"},
    {"id":5,"name":"中共上海市宝山区委员会","type":"党委","level":"省级辖（区）","parent":"中共上海市委员会","location":"上海市宝山区"},
    {"id":6,"name":"中共海南省委员会","type":"党委","level":"省级","parent":"","location":"海南省海口市"},
    {"id":7,"name":"中共四川省绵阳市委","type":"党委","level":"地级","parent":"中共四川省委员会","location":"四川省绵阳市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # ── 范少军 (id=1) —— 上海 → 海南 跨省调任 ──
    {"person_id":1,"org_id":4,"title":"上海市宝山区区长","start_date":"2016","end_date":"2019","rank":"正厅级","note":"上海市宝山区人民政府"},
    {"person_id":1,"org_id":5,"title":"中共上海市宝山区委书记","start_date":"2019","end_date":"（转任海南）","rank":"副省级（直辖市区委书记）","note":"之后调任海南"},
    {"person_id":1,"org_id":1,"title":"海口市委书记（海南省委常委兼任）","start_date":"","end_date":"present","rank":"副部级","note":"接替罗增斌"},

    # ── 张勇 (id=2) —— 海口市长 ──
    {"person_id":2,"org_id":1,"title":"海口市委副书记","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":2,"org_id":2,"title":"海口市人民政府市长（党组书记）","start_date":"","end_date":"present","rank":"地级正职","note":"主持市政府全面工作，兼管旅游、文化、审计"},

    # ── 市政府领导班子 ──
    {"person_id":3,"org_id":1,"title":"海口市委常委","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":3,"org_id":2,"title":"海口市政府党组副书记、常务副市长","start_date":"","end_date":"present","rank":"地级副职","note":"班子内最年轻（1984年生）"},
    {"person_id":4,"org_id":1,"title":"海口市委常委","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":4,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":5,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":"分管海口国家高新区、商务、招商引资、口岸、会展"},
    {"person_id":6,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":"兼市公安局局长、督察长，市政法委副书记"},
    {"person_id":6,"org_id":3,"title":"海口市公安局党委书记、局长","start_date":"","end_date":"present","rank":"地级副职","note":"警务序列"},
    {"person_id":7,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":"分管海口综保区、工业、科技、通信、综合执法"},
    {"person_id":8,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":9,"org_id":2,"title":"海口市人民政府副市长","start_date":"","end_date":"present","rank":"地级副职","note":"分管生态环境、人社、城管（民革）"},
    {"person_id":10,"org_id":2,"title":"海口市政府党组成员、副市长","start_date":"","end_date":"present","rank":"地级副职","note":""},
    {"person_id":11,"org_id":2,"title":"海口市政府秘书长、办公室主任","start_date":"","end_date":"present","rank":"地级市直正职","note":"市政府党组成员、机关党组书记"},

    # ── 前任 ──
    {"person_id":12,"org_id":1,"title":"海口市委书记（海南省委常委兼任）","start_date":"","end_date":"present?","rank":"副部级","note":"前任书记"},
    {"person_id":12,"org_id":7,"title":"中共四川省绵阳市委书记","start_date":"","end_date":"","rank":"正厅级","note":"被曹立军接替后调海南"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记-市长 搭档
    {"person_a":1,"person_b":2,"type":"superior_subordinate","context":"范少军任海口市委书记，张勇任市长，党政一把手搭档","overlap_org":"中共海口市委员会","overlap_period":"现任","strength":"strong","confidence":"confirmed"},

    # 前后任 市委书记
    {"person_a":12,"person_b":1,"type":"predecessor_successor","context":"罗增斌离任/范少军接替任海口市委书记","overlap_org":"中共海口市委员会","overlap_period":"","strength":"strong","confidence":"plausible"},

    # 书记 ↔ 常务副市长 / 常委副市长
    {"person_a":1,"person_b":3,"type":"superior_subordinate","context":"市委书记领导市委常委、常务副市长","overlap_org":"中共海口市委员会","overlap_period":"现任","strength":"strong","confidence":"confirmed"},
    {"person_a":1,"person_b":4,"type":"superior_subordinate","context":"市委书记领导市委常委、副市长","overlap_org":"中共海口市委员会","overlap_period":"现任","strength":"strong","confidence":"confirmed"},

    # 市长 ↔ 常务副市长 / 公安局长/公安
    {"person_a":2,"person_b":3,"type":"superior_subordinate","context":"市长领导常务副市长（分管政府日常）","overlap_org":"海口市人民政府","overlap_period":"现任","strength":"strong","confidence":"confirmed"},
    {"person_a":2,"person_b":6,"type":"superior_subordinate","context":"市长领导公安局长（政府副市长）","overlap_org":"海口市人民政府","overlap_period":"现任","strength":"medium","confidence":"confirmed"},

    # 常务副市长 ↔ 其他副市长（同班子）
    {"person_a":3,"person_b":5,"type":"overlap","context":"同在市政府班子（常务与副市长）","overlap_org":"海口市人民政府","overlap_period":"现任","strength":"medium","confidence":"confirmed"},
    {"person_a":3,"person_b":7,"type":"overlap","context":"同在市政府班子（常务与副市长）","overlap_org":"海口市人民政府","overlap_period":"现任","strength":"medium","confidence":"confirmed"},
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================
def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS persons
        (id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
         birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
         work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS organizations
        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
         parent TEXT, location TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS positions
        (id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER,
         org_id INTEGER, title TEXT, start TEXT, end TEXT,
         rank TEXT, note TEXT,
         FOREIGN KEY(person_id) REFERENCES persons(id),
         FOREIGN KEY(org_id) REFERENCES organizations(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS relationships
        (id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER,
         person_b INTEGER, type TEXT, context TEXT,
         overlap_org TEXT, overlap_period TEXT,
         strength TEXT, confidence TEXT,
         FOREIGN KEY(person_a) REFERENCES persons(id),
         FOREIGN KEY(person_b) REFERENCES persons(id))''')

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                   p["birthplace"],p["education"],p["party_join"],
                   p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"],pos["org_id"],pos["title"],pos["start_date"],pos["end_date"],pos["rank"],pos["note"]))
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES (?,?,?,?,?,?,?,?)",
                  (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period",""),r["strength"],r["confidence"]))

    conn.commit()
    print(f"Database: {DB_PATH}")
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()

def person_color(p):
    """Return r,g,b string based on role."""
    role = p.get("current_post","")
    name = p.get("name","")
    if "书记" in role and "纪委" not in role and name in ("范少军",):
        return "255,50,50"    # Red — Party Secretary
    if name == "张勇":
        return "50,100,255"   # Blue — Mayor
    if "纪委" in role:
        return "255,165,0"    # Orange — Discipline
    if "书记" in role:
        return "220,80,80"    # Light red — other party secretaries
    if "市长" in role or "副市长" in role or "市长" in role:
        return "80,130,255"   # Light blue — Government leaders
    return "100,100,100"      # Grey — Others

def is_top_leader(p):
    return p["name"] in ("范少军","张勇")

def org_color(ot):
    colors = {
        "党委":"255,200,200","政府":"200,200,255","人大":"200,255,255",
        "政协":"255,240,200","事业单位":"220,220,220",
    }
    return colors.get(ot, "200,200,200")

def build_gexf():
    now = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{now}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>海口市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        eid += 1
        title = pos.get("title","")
        start = pos.get("start_date","")
        end_ = pos.get("end_date","")
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end_)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        if r["person_b"] <= 0:
            continue
        eid += 1
        ctx = r.get("context","")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()
    print("Done.")