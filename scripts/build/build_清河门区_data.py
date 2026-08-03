#!/usr/bin/env python3
"""清河门区 领导班子工作关系网络 — 数据构建脚本

数据来源: fxqhm.gov.cn（清河门区政府官网）
  区委书记: 李国凯（2026年7月第十次党代会连任）
  区    长: 满佳（第十届区政府）
  区委常委: 秦福成、张维广、秦川、卜凡鹏、颜金梁、付大成、张子元

用法:
    python3 data/tmp/liaoning_清河门区/build_清河门区_data.py
"""

import sqlite3
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "清河门区"
STAGING = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING, "清河门区_network.db")
GEXF_PATH = os.path.join(STAGING, "清河门区_network.gexf")

# ══════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════

persons = [
    {"id":1,"name":"李国凯","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委书记","current_org":"中共清河门区委员会","source":"fxqhm.gov.cn"},
    {"id":2,"name":"满佳","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 政府领导页面"},
    {"id":3,"name":"秦福成","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委副书记","current_org":"中共清河门区委员会","source":"fxqhm.gov.cn 第十次党代会"},
    {"id":4,"name":"张维广","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委、副区长（常务）","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":5,"name":"秦川","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委","current_org":"中共清河门区委员会","source":"fxqhm.gov.cn 第十次党代会"},
    {"id":6,"name":"卜凡鹏","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委、组织部部长","current_org":"中共清河门区委组织部","source":"fxqhm.gov.cn 巡察会议"},
    {"id":7,"name":"颜金梁","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委","current_org":"中共清河门区委员会","source":"fxqhm.gov.cn 第十次党代会"},
    {"id":8,"name":"付大成","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委、副区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":9,"name":"张子元","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区委常委、纪委书记、监委代主任","current_org":"中共清河门区纪律检查委员会","source":"fxqhm.gov.cn 巡察会议"},
    {"id":10,"name":"甄理","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区副区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":11,"name":"穆迪","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区副区长（援疆）","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":12,"name":"段百炼","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区副区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":13,"name":"马微","gender":"","ethnicity":"","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区副区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 分工通知"},
    {"id":14,"name":"赵国亮","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区人大常委会主任","current_org":"清河门区人大常委会","source":"fxqhm.gov.cn 建军节慰问"},
    {"id":15,"name":"李红梅","gender":"女","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"清河门区政协主席","current_org":"政协清河门区委员会","source":"fxqhm.gov.cn 建军节慰问"},
    {"id":16,"name":"白一光","gender":"男","ethnicity":"汉族","birth":"","birthplace":"","education":"","party_join":"","work_start":"","current_post":"前任清河门区副区长","current_org":"清河门区人民政府","source":"fxqhm.gov.cn 2025年12月分工通知"},
]

organizations = [
    {"id":1,"name":"中共清河门区委员会","type":"党委","level":"县处级","parent":"中共阜新市委","location":"阜新市清河门区"},
    {"id":2,"name":"清河门区人民政府","type":"政府","level":"县处级","parent":"阜新市人民政府","location":"阜新市清河门区"},
    {"id":3,"name":"中共清河门区委组织部","type":"党委","level":"县处级","parent":"中共清河门区委员会","location":"阜新市清河门区"},
    {"id":4,"name":"中共清河门区纪律检查委员会","type":"党委","level":"县处级","parent":"中共清河门区委员会","location":"阜新市清河门区"},
    {"id":5,"name":"清河门区人大常委会","type":"人大","level":"县处级","parent":"阜新市人大常委会","location":"阜新市清河门区"},
    {"id":6,"name":"政协清河门区委员会","type":"政协","level":"县处级","parent":"政协阜新市委员会","location":"阜新市清河门区"},
    {"id":7,"name":"辽宁阜新皮革产业开发区","type":"开发区","level":"县处级","parent":"","location":"阜新市清河门区"},
]

positions = [
    {"person_id":1,"org_id":1,"title":"清河门区委书记","start_date":"","end_date":"present","rank":"县处级正职","note":"2026年7月第十次党代会连任"},
    {"person_id":2,"org_id":2,"title":"清河门区长","start_date":"","end_date":"present","rank":"县处级正职","note":"第十届区政府"},
    {"person_id":2,"org_id":1,"title":"清河门区委副书记","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":3,"org_id":1,"title":"清河门区委副书记","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":4,"org_id":2,"title":"常务副区长","start_date":"","end_date":"present","rank":"县处级副职","note":"区政府党组副书记"},
    {"person_id":4,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":5,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":6,"org_id":3,"title":"组织部部长","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":6,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":7,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":8,"org_id":2,"title":"副区长","start_date":"2026-01","end_date":"present","rank":"县处级副职","note":"住建、农林水利、市场监管"},
    {"person_id":8,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":9,"org_id":4,"title":"纪委书记、监委代主任","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":9,"org_id":1,"title":"清河门区委常委","start_date":"","end_date":"present","rank":"县处级副职","note":""},
    {"person_id":10,"org_id":2,"title":"副区长","start_date":"","end_date":"present","rank":"县处级副职","note":"招商、工业、交通、环保"},
    {"person_id":11,"org_id":2,"title":"副区长（援疆）","start_date":"","end_date":"present","rank":"县处级副职","note":"援疆暂不分管"},
    {"person_id":12,"org_id":2,"title":"副区长","start_date":"","end_date":"present","rank":"县处级副职","note":"公安、司法"},
    {"person_id":13,"org_id":2,"title":"副区长","start_date":"2026-01","end_date":"present","rank":"县处级副职","note":"教育、文化、卫生、民政"},
    {"person_id":14,"org_id":5,"title":"人大主任","start_date":"","end_date":"present","rank":"县处级正职","note":""},
    {"person_id":15,"org_id":6,"title":"政协主席","start_date":"","end_date":"present","rank":"县处级正职","note":""},
    {"person_id":16,"org_id":2,"title":"副区长（前任）","start_date":"","end_date":"2025-12","rank":"县处级副职","note":"原住建、综合执法"},
]

relationships = [
    {"person_a":1,"person_b":2,"type":"党政正职搭档","context":"区委书记与区长","overlap_org":"清河门区","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":3,"type":"上下级","context":"书记与副书记","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":9,"type":"上下级","context":"书记与纪委书记","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":6,"type":"上下级","context":"书记与组织部长","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":2,"person_b":4,"type":"上下级","context":"区长与常务副区长","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":2,"person_b":8,"type":"上下级","context":"区长与付大成","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":2,"person_b":10,"type":"上下级","context":"区长与甄理","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":2,"person_b":12,"type":"上下级","context":"区长与段百炼","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":2,"person_b":13,"type":"上下级","context":"区长与马微","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":4,"type":"区委常委会同僚","context":"均为区委常委","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":5,"type":"区委常委会同僚","context":"书记与秦川","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":7,"type":"区委常委会同僚","context":"书记与颜金梁","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":3,"person_b":4,"type":"区委常委会同僚","context":"副书记与常务副区长","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":6,"person_b":9,"type":"区委常委会同僚","context":"组织部长与纪委书记","overlap_org":"中共清河门区委员会","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":14,"type":"党政负责人","context":"书记与人大主任","overlap_org":"清河门区","overlap_period":"2026-至今"},
    {"person_a":1,"person_b":15,"type":"党政负责人","context":"书记与政协主席","overlap_org":"清河门区","overlap_period":"2026-至今"},
    {"person_a":4,"person_b":8,"type":"AB角互补","context":"张维广与付大成","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":10,"person_b":13,"type":"AB角互补","context":"甄理与马微","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":4,"person_b":12,"type":"AB角互补","context":"张维广与段百炼","overlap_org":"清河门区人民政府","overlap_period":"2026-至今"},
    {"person_a":8,"person_b":16,"type":"前任继任","context":"付大成接替白一光分管领域","overlap_org":"清河门区人民政府","overlap_period":""},
]


# ══════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '', party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL,
            type TEXT DEFAULT '', level TEXT DEFAULT '',
            parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '', rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: fxqhm.gov.cn（官方）")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        conn.execute("INSERT INTO persons (" + ",".join(cols_p) +
                     ") VALUES (" + ",".join(["?"]*len(cols_p)) + ")",
                     [p.get(c,"") for c in cols_p])

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        conn.execute("INSERT INTO organizations (" + ",".join(cols_o) +
                     ") VALUES (" + ",".join(["?"]*len(cols_o)) + ")",
                     [o.get(c,"") for c in cols_o])

    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        conn.execute("INSERT INTO positions (" + ",".join(cols_pos) +
                     ") VALUES (" + ",".join(["?"]*len(cols_pos)) + ")",
                     [pos.get(c,"") for c in cols_pos])

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        conn.execute("INSERT INTO relationships (" + ",".join(cols_r) +
                     ") VALUES (" + ",".join(["?"]*len(cols_r)) + ")",
                     [r.get(c,"") for c in cols_r])

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "区长" in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("150,100,100", 15.0)
        elif "副" in post or "常委" in post:
            return ("100,100,255", 12.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,200,100", 15.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {"党委":("255,200,200"),"政府":("200,200,255"),"人大":("200,255,255"),
                "政协":("255,240,200"),"开发区":("200,255,200")}.get(typ,("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]
    for p in persons:
        c,sz = person_color(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    # Clean old DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    run_build()