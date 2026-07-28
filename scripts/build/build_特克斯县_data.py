#!/usr/bin/env python3
"""
特克斯县领导班子工作关系网络 — 数据构建脚本
"""
import sqlite3, os, sys
from datetime import datetime

# Make gov_relation importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "特克斯县_network.db")
GEXF_PATH = os.path.join(BASE, "特克斯县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s else ""

# Person IDs are integers (0+)
PERSONS = [
    {"id":0,"name":"（待确认）","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委书记","current_org":"中共特克斯县委员会","source":"县委网站tksdj.gov.cn无法访问"},
    {"id":1,"name":"阿里木江·吾斯曼","gender":"男","ethnicity":"维吾尔族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委副书记、政府县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":2,"name":"唐尉","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"县委常委、政府副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/jrtks/202607/3125502d8a484b8a92be70ea160f5fed.shtml"},
    {"id":3,"name":"王庭辉","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":4,"name":"徐平","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":5,"name":"王天恒","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":6,"name":"欧日鲁格","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":7,"name":"哈米旦·排足拉","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
    {"id":8,"name":"热巴提·艾尔肯","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"副县长","current_org":"特克斯县人民政府","source":"www.zgtks.gov.cn/zgtks/ldxx/list_ld.shtml"},
]

ORG = [
    {"id":1,"name":"中共特克斯县委员会","type":"党委","level":"县级","parent":"中共伊犁州委员会","location":"特克斯县"},
    {"id":2,"name":"特克斯县人民政府","type":"政府","level":"县级","parent":"伊犁州人民政府","location":"特克斯县"},
]

POS = [
    {"person_id":0,"org_id":1,"title":"县委书记","start_date":"","end_date":"现任","rank":"正县级","note":"姓名待确认"},
    {"person_id":1,"org_id":2,"title":"县长","start_date":"","end_date":"现任","rank":"正县级","note":"兼县委副书记"},
    {"person_id":1,"org_id":1,"title":"县委副书记","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":2,"org_id":2,"title":"县委常委、政府副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":2,"org_id":1,"title":"县委常委","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":3,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":4,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":5,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":6,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":7,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
    {"person_id":8,"org_id":2,"title":"副县长","start_date":"","end_date":"现任","rank":"副县级","note":""},
]

REL = [
    {"person_a":0,"person_b":1,"type":"工作关系","context":"党政一把手搭档","overlap_org":"中共特克斯县委员会","overlap_period":"现任"},
    {"person_a":1,"person_b":2,"type":"工作关系","context":"政府班子搭档","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":0,"person_b":2,"type":"工作关系","context":"县委班子成员","overlap_org":"中共特克斯县委员会","overlap_period":"现任"},
    {"person_a":1,"person_b":3,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":4,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":5,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":6,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":7,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":1,"person_b":8,"type":"工作关系","context":"县政府班子","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":3,"person_b":4,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":3,"person_b":5,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":4,"person_b":5,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":3,"person_b":6,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":4,"person_b":6,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":5,"person_b":6,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":5,"person_b":7,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":5,"person_b":8,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":6,"person_b":7,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":6,"person_b":8,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
    {"person_a":7,"person_b":8,"type":"同事关系","context":"同为副县长","overlap_org":"特克斯县人民政府","overlap_period":"现任"},
]

def build():
    conn = sqlite3.connect(DB_PATH)
    for t in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.executescript("""
        CREATE TABLE persons(id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
        CREATE TABLE organizations(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
        CREATE TABLE positions(id INTEGER PRIMARY KEY AUTOINCREMENT,person_id INTEGER,org_id INTEGER,title TEXT,start_date TEXT,end_date TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
        CREATE TABLE relationships(id INTEGER PRIMARY KEY AUTOINCREMENT,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
    """)
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education","party_join","work_start","current_post","current_org","source"]
    for p in PERSONS:
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", [p.get(c,"") for c in cols_p])
    cols_o = ["id","name","type","level","parent","location"]
    for o in ORG:
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", [o.get(c,"") for c in cols_o])
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for po in POS:
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", [po.get(c,"") for c in cols_pos])
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in REL:
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", [r.get(c,"") for c in cols_r])
    conn.commit()
    conn.close()
    print(f"DB: {len(PERSONS)}p, {len(ORG)}o, {len(POS)}pos, {len(REL)}rel")

    # GEXF
    def pcolor(p):
        t = p["current_post"] or ""
        if "县委书记" in t: return ("255,50,50", 20.0)
        if "县长" in t and "副" not in t: return ("50,100,255", 20.0)
        return ("100,100,255", 12.0)
    def ocolor(o):
        return {"党委":"255,200,200","政府":"200,200,255","人大":"200,255,255","政协":"255,240,200","纪委":"255,165,0"}.get(o["type"],"200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Sisyphus</creator>')
    lines.append('    <description>特克斯县领导工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in PERSONS:
        c, sz = pcolor(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in ORG:
        c = ocolor(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for po in POS:
        lines.append(f'      <edge id="{eid}" source="p{po["person_id"]}" target="o{po["org_id"]}" label="{esc(po["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(po["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in REL:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build()