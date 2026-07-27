#!/usr/bin/env python3
"""
襄垣县领导班子工作关系网络构建脚本

来源: 搜狗搜索、微信搜索、襄垣县人民政府网站
数据截止: 2026年7月
"""

import json
import os
import sqlite3
from datetime import datetime

SLUG = "襄垣县_2026"
AS_OF = "2026-07-26"
TODAY = "20260726"
PROVINCE = "山西省"
CITY = "长治市"

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE, "data", "database", f"{SLUG}.db")
GEXF_PATH = os.path.join(BASE, "data", "graph", f"{SLUG}.gexf")
PERSONS_DIR = os.path.join(BASE, "data", "persons")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
os.makedirs(PERSONS_DIR, exist_ok=True)

esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s else ""


# ───────────────────────────────────────────────────────────────────
# DATA
# ───────────────────────────────────────────────────────────────────

persons = [
    # 当前领导班子
    {"id":1,"name":"李瑜","gender":"男","ethnicity":"汉族","birth":"1972年3月","birthplace":"","education":"在职研究生","party_join":"中共党员","work_start":"","current_post":"襄垣县委书记","current_org":"中国共产党襄垣县委员会","source":"https://www.sxgov.cn/c/2023-01/09/content_11350352.html"},
    {"id":2,"name":"元海波","gender":"男","ethnicity":"汉族","birth":"1975年8月","birthplace":"山西省潞城市","education":"在职大学","party_join":"中共党员","work_start":"","current_post":"襄垣县人民政府县长","current_org":"襄垣县人民政府","source":"https://www.sxgov.cn/c/2026-05/21/content_13156872.html"},
    {"id":3,"name":"贾钢辉","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委副书记","current_org":"中国共产党襄垣县委员会","source":"https://www.sohu.com/a/774587584_121124275"},
    {"id":4,"name":"鲍明敏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、常务副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":5,"name":"周炳良","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":6,"name":"张帆","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、纪委书记、监委主任","current_org":"襄垣县纪律检查委员会","source":"https://news.sohu.com/a/760667637_121124275"},
    {"id":7,"name":"魏巍","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、宣传部部长","current_org":"中国共产党襄垣县委员会","source":"https://www.sohu.com/a/774587584_121124275"},
    {"id":8,"name":"贾永兴","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、统战部部长","current_org":"中国共产党襄垣县委员会","source":"https://weixin.sogou.com/ — 太原市襄垣商会2026年迎新春乡情招商联谊会报道"},
    {"id":9,"name":"杜娟","gender":"女","ethnicity":"汉族","birth":"1983年3月","birthplace":"","education":"在职研究生","party_join":"中共党员","work_start":"","current_post":"襄垣县委常委、副县长(挂职)","current_org":"襄垣县人民政府","source":"https://www.sohu.com/a/774587584_121124275"},
    {"id":10,"name":"张小锋","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":11,"name":"赵楠楠","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":12,"name":"王建方","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":13,"name":"宋双麒","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":14,"name":"赵俊杰","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县副县长","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":15,"name":"郭瑞华","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县政府领导","current_org":"襄垣县人民政府","source":"http://www.xiangyuan.gov.cn/xwzx/ldzc/"},
    {"id":16,"name":"田福合","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县监察委员会主任","current_org":"襄垣县纪律检查委员会","source":"https://cz.sxgov.cn/content/2026-07/24/content_13577533.html"},
    # 前领导人
    {"id":101,"name":"段联刚","gender":"男","ethnicity":"汉族","birth":"1976年4月","birthplace":"山西省黎城县","education":"中央党校研究生","party_join":"1999年12月","work_start":"1996年12月","current_post":"怀仁市委书记(原襄垣县长)","current_org":"","source":"https://baike.sogou.com/"},
    {"id":102,"name":"张晋伟","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原襄垣县委书记(2019-2022)","current_org":"","source":"https://www.163.com/d/article/E97UO0G505148KHO.html"},
    {"id":103,"name":"翟卫华","gender":"女","ethnicity":"汉族","birth":"1969年","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原襄垣县委书记(2022.7-2022.11)","current_org":"","source":"https://i.ifeng.com/c/8CxHZxO9UQS"},
    {"id":104,"name":"王辉","gender":"男","ethnicity":"汉族","birth":"1971年2月","birthplace":"","education":"中央党校大学","party_join":"中共党员","work_start":"","current_post":"襄垣县人大常委会主任(原组织部部长)","current_org":"","source":"https://new.qq.com/rain/a/20250407A03JXM00"},
    {"id":105,"name":"王建斌","gender":"男","ethnicity":"汉族","birth":"1969年","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"襄垣县人大常委会副主任","current_org":"","source":"https://www.163.com/dy/article/J5AHC4JT0514R9P4.html"},
    {"id":106,"name":"杨勇","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"中共党员","work_start":"","current_post":"原襄垣县委副书记(2021届)","current_org":"","source":"https://www.sohu.com/a/467546702_121124275"},
]

organizations = [
    {"id":1,"name":"中国共产党襄垣县委员会","type":"党委","level":"县级","parent":"","location":"山西省长治市襄垣县"},
    {"id":2,"name":"襄垣县人民政府","type":"政府","level":"县级","parent":"","location":"山西省长治市襄垣县"},
    {"id":3,"name":"襄垣县纪律检查委员会","type":"纪委","level":"县级","parent":"","location":"山西省长治市襄垣县"},
    {"id":4,"name":"襄垣县人大常委会","type":"人大","level":"县级","parent":"","location":"山西省长治市襄垣县"},
    {"id":5,"name":"襄垣县政协","type":"政协","level":"县级","parent":"","location":"山西省长治市襄垣县"},
]

positions = [
    # 李瑜
    {"person_id":1,"org_id":1,"title":"襄垣县委书记","start":"2023-01","end":"","rank":"正处级","note":"2023年1月任县委书记"},
    {"person_id":1,"org_id":2,"title":"襄垣县县长","start":"2020","end":"2023-01","rank":"正处级","note":"此前任县长，后升任县委书记"},
    # 元海波
    {"person_id":2,"org_id":2,"title":"襄垣县县长","start":"2026-07","end":"","rank":"正处级","note":"2026年7月当选县长"},
    # 贾钢辉
    {"person_id":3,"org_id":1,"title":"县委副书记","start":"2024-09","end":"","rank":"副处级","note":""},
    # 鲍明敏
    {"person_id":4,"org_id":2,"title":"常务副县长","start":"","end":"","rank":"副处级","note":"县委常委"},
    # 周炳良
    {"person_id":5,"org_id":2,"title":"副县长","start":"","end":"","rank":"副处级","note":"县委常委"},
    # 张帆
    {"person_id":6,"org_id":3,"title":"县纪委书记、监委主任","start":"2024-02","end":"","rank":"副处级","note":"县委常委"},
    # 魏巍
    {"person_id":7,"org_id":1,"title":"县委宣传部部长","start":"2024-09","end":"","rank":"副处级","note":"县委常委"},
    # 贾永兴
    {"person_id":8,"org_id":1,"title":"统战部部长","start":"","end":"","rank":"副处级","note":"县委常委"},
    # 杜娟
    {"person_id":9,"org_id":2,"title":"副县长(挂职)","start":"2025-03","end":"","rank":"副处级","note":"县委常委，挂职一年"},
    # 其他副县长
    {"person_id":10,"org_id":2,"title":"副县长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":11,"org_id":2,"title":"副县长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":12,"org_id":2,"title":"副县长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":13,"org_id":2,"title":"副县长","start":"","end":"","rank":"副处级","note":""},
    {"person_id":14,"org_id":2,"title":"副县长","start":"2024-04","end":"","rank":"副处级","note":""},
    # 前领导人
    {"person_id":101,"org_id":2,"title":"县长","start":"2023-03","end":"2026-04","rank":"正处级","note":"2026年4月调任怀仁市委书记"},
    {"person_id":101,"org_id":0,"title":"长治市信访局局长","start":"2021-10","end":"2023-03","rank":"正处级","note":""},
    {"person_id":102,"org_id":1,"title":"县委书记","start":"2019-03","end":"2022-07","rank":"正处级","note":"后调任大同市副市长"},
    {"person_id":103,"org_id":1,"title":"县委书记","start":"2022-07","end":"2022-11","rank":"正处级","note":"上任仅4个月后坠楼去世"},
    {"person_id":104,"org_id":4,"title":"县人大常委会主任","start":"2025-05","end":"","rank":"正处级","note":"原县委组织部部长"},
    {"person_id":104,"org_id":1,"title":"县委组织部部长","start":"","end":"2025-04","rank":"副处级","note":"县委常委"},
    {"person_id":105,"org_id":4,"title":"县人大常委会副主任","start":"","end":"","rank":"副处级","note":""},
    {"person_id":106,"org_id":1,"title":"县委副书记","start":"2021","end":"2023","rank":"副处级","note":"2021年襄垣县第十四届县委副书记"},
]

relationships = [
    {"person_a":1,"person_b":2,"type":"党政搭档","context":"县委书记与县长搭档","overlap_org":"襄垣县","overlap_period":"2026-07至今"},
    {"person_a":1,"person_b":101,"type":"党政搭档","context":"李瑜任县委书记时段联刚为县长(2023-2026)","overlap_org":"襄垣县","overlap_period":"2023-03至2026-04"},
    {"person_a":1,"person_b":102,"type":"上下级","context":"张晋伟任县委书记时李瑜为县长(2021-2022)","overlap_org":"襄垣县","overlap_period":"2019至2022"},
    {"person_a":1,"person_b":103,"type":"上下级","context":"翟卫华任县委书记时李瑜为县长(2022.7-2022.11)","overlap_org":"襄垣县","overlap_period":"2022-07至2022-11"},
    {"person_a":101,"person_b":102,"type":"前任关系","context":"县长交接","overlap_org":"襄垣县","overlap_period":""},
    {"person_a":102,"person_b":103,"type":"接任关系","context":"县委书记交接","overlap_org":"襄垣县委","overlap_period":"2022-07"},
    {"person_a":103,"person_b":1,"type":"接任关系","context":"翟卫华去世后李瑜接任书记","overlap_org":"襄垣县委","overlap_period":"2023-01"},
    {"person_a":1,"person_b":106,"type":"搭档","context":"2021届县委副书记搭档","overlap_org":"襄垣县委","overlap_period":"2021-2023"},
    {"person_a":1,"person_b":104,"type":"同事","context":"县委书记与组织部长共事","overlap_org":"襄垣县委","overlap_period":""},
    {"person_a":3,"person_b":7,"type":"同事","context":"同时被任命为县委副书记和宣传部长","overlap_org":"襄垣县委","overlap_period":"2024-09至今"},
    {"person_a":6,"person_b":1,"type":"上下级","context":"纪委书记向县委书记汇报","overlap_org":"襄垣县委","overlap_period":"2024-02至今"},
]


# ───────────────────────────────────────────────────────────────────
# SQLite DB Builder
# ───────────────────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT
    )""")
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],
                     p.get("birthplace",""),p.get("education",""),p.get("party_join",""),
                     p.get("work_start",""),p["current_post"],p.get("current_org",""),p.get("source","")))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o.get("parent",""),o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r.get("overlap_org",""),r.get("overlap_period","")))
    conn.commit()
    conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")


# ───────────────────────────────────────────────────────────────────
# GEXF Graph Builder
# ───────────────────────────────────────────────────────────────────

def person_color(post):
    if "县委书记" in post:
        return ("200,50,50", 20.0)
    elif "县长" in post and "副" not in post:
        return ("50,100,200", 20.0)
    elif "纪委书记" in post or "监委主任" in post:
        return ("200,150,50", 12.0)
    elif "常委" in post and "副县长" in post:
        return ("100,150,255", 12.0)
    elif "常委" in post:
        return ("140,140,255", 12.0)
    elif "副县长" in post:
        return ("100,180,255", 10.0)
    elif "副书记" in post:
        return ("180,80,80", 15.0)
    else:
        return ("160,160,160", 10.0)

def org_color(t):
    return {"党委": ("200,100,100", 8.0), "政府": ("100,150,200", 8.0),
            "纪委": ("220,180,50", 8.0), "人大": ("100,200,180", 8.0),
            "政协": ("200,180,100", 8.0)}.get(t, ("180,180,180", 8.0))

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{PROVINCE}{CITY}襄垣县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c, sz = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="worked_at">')
        lines.append(f'        <attvalues><attvalue for="0" value="worked_at"/><attvalue for="1" value="{esc(pos.get("note",""))}"/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}">')
        lines.append(f'        <attvalues><attvalue for="0" value="relationship"/><attvalue for="1" value="{esc(r["context"])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ───────────────────────────────────────────────────────────────────
# Main
# ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG}...")
    build_db()
    build_gexf()
    print("Done.")