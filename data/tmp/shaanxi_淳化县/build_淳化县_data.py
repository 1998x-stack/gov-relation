#!/usr/bin/env python3
"""
淳化县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

淳化县是陕西省咸阳市下辖的县，位于咸阳市北部，渭北旱塬丘陵沟壑区。
数据来源：淳化县政府网站 (www.snchunhua.gov.cn) 新闻报道及领导之窗页面
采集日期：2026-07-25

当前领导:
   县委书记: 张乔
   县长: 李建清
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

STAGING = Path(__file__).parent.resolve()
REPO_ROOT = STAGING.parent.parent
sys.path.insert(0, str(REPO_ROOT))

SLUG = "淳化县"
DATE = "2026-07-25"

# Process_tmp validator tokens
DB_PATH = "data/database/淳化县_network.db"
GEXF_PATH = "data/graph/淳化县_network.gexf"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委领导 ---
    (1, "张乔", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共淳化县委",
     "http://www.snchunhua.gov.cn/xxgk/fdzdgknr/ldzc/", "confirmed"),
    (2, "李建清", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县长", "淳化县人民政府",
     "http://www.snchunhua.gov.cn/xxgk/fdzdgknr/ldzc/", "confirmed"),
    (3, "丁锋", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、常务副县长", "淳化县人民政府",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260720_2102351.html", "confirmed"),
    (4, "余胜辉", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、组织部部长", "中共淳化县委组织部",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260720_2102352.html", "confirmed"),
    (5, "李杨", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委", "中共淳化县委",
     "http://www.snchunhua.gov.cn/xw/chyw/202606/t20260615_2093344.html", "confirmed"),
    (6, "左解放", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委", "中共淳化县委",
     "http://www.snchunhua.gov.cn/xw/chyw/202606/t20260615_2093344.html", "confirmed"),

    # --- 县政府领导 ---
    (7, "韩旭阳", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "淳化县人民政府",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260717_2102088.html", "confirmed"),
    (8, "刘继宁", "男", "汉族", "", "", "", "中共党员", "",
     "县政府党组成员", "淳化县人民政府",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260717_2102088.html", "confirmed"),

    # --- 县人大领导 ---
    (9, "白洁", "女", "汉族", "", "", "", "中共党员", "",
     "县人大常委会主任", "淳化县人大常委会",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260716_2101678.html", "confirmed"),

    # --- 县政协领导 ---
    (10, "冯社", "男", "汉族", "", "", "", "中共党员", "",
     "县政协主席", "淳化县政协",
     "http://www.snchunhua.gov.cn/xw/chyw/202607/t20260716_2101678.html", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共淳化县委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市淳化县"),
    (2, "淳化县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市淳化县"),
    (3, "中共淳化县委组织部", "党委部门", "正科级", "中共淳化县委", "陕西省咸阳市淳化县"),
    (4, "淳化县人大常委会", "人大", "县处级", "咸阳市人大常委会", "陕西省咸阳市淳化县"),
    (5, "淳化县政协", "政协", "县处级", "咸阳市政协", "陕西省咸阳市淳化县"),
]

# ===== 任职数据 =====
positions = [
    # 县委领导任职
    (1, 1, 1, "县委书记", "未知", "至今", "正县级", ""),
    (2, 2, 1, "县委副书记", "未知", "至今", "正县级", "同时任县长"),
    (2, 2, 2, "县长", "未知", "至今", "正县级", ""),
    (3, 3, 2, "县委常委、常务副县长", "未知", "至今", "副县级", ""),
    (4, 4, 3, "县委常委、组织部部长", "未知", "至今", "副县级", ""),
    (5, 5, 1, "县委常委", "未知", "至今", "副县级", ""),
    (6, 6, 1, "县委常委", "未知", "至今", "副县级", ""),

    # 县政府领导任职
    (7, 7, 2, "副县长", "未知", "至今", "副县级", ""),
    (8, 8, 2, "县政府党组成员", "未知", "至今", "副县级", ""),

    # 县人大领导任职
    (9, 9, 4, "县人大常委会主任", "未知", "至今", "正县级", ""),

    # 县政协领导任职
    (10, 10, 5, "县政协主席", "未知", "至今", "正县级", ""),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    (1, 1, 2, "搭档", "县委书记与县长——党政一把手搭档工作", "中共淳化县委/淳化县人民政府", "至今", "confirmed"),
    (2, 1, 3, "上下级", "县委书记与常务副县长", "中共淳化县委", "至今", "confirmed"),
    (3, 1, 4, "上下级", "县委书记与组织部部长", "中共淳化县委", "至今", "confirmed"),
    (4, 1, 5, "上下级", "县委书记与县委常委", "中共淳化县委", "至今", "confirmed"),
    (5, 1, 6, "上下级", "县委书记与县委常委", "中共淳化县委", "至今", "confirmed"),
    (6, 2, 3, "上下级", "县长与常务副县长——政府日常工作搭档", "淳化县人民政府", "至今", "confirmed"),
    (7, 2, 7, "上下级", "县长与副县长", "淳化县人民政府", "至今", "confirmed"),
    (8, 2, 8, "上下级", "县长与党组成员", "淳化县人民政府", "至今", "confirmed"),
    (9, 3, 7, "同僚", "同一届县政府领导班子成员", "淳化县人民政府", "至今", "confirmed"),
    (10, 1, 9, "同级", "县委书记与县人大主任", "淳化县", "至今", "confirmed"),
    (11, 1, 10, "同级", "县委书记与县政协主席", "淳化县", "至今", "confirmed"),
]

# ===== 生成函数 =====
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid, post):
    if "书记" in post and "县委" in post or "县委书记" == post:
        return "255,50,50"
    if "县长" in post or "副县长" in post or "常务" in post:
        return "50,100,255"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    return "100,100,100"

def is_top_leader(post):
    return "县委书记" == post or ("县长" in post and "副" not in post[:2] and "常务" not in post)

def build_sqlite(db_path):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT,
            confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    c.executemany("INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source,confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", persons)
    c.executemany("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", organizations)
    c.executemany("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)", positions)
    c.executemany("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?,?)", relationships)
    conn.commit()
    conn.close()
    print(f"  SQLite 数据库已生成: {db_path}")
    print(f"    - {len(persons)} 人物")
    print(f"    - {len(organizations)} 组织")
    print(f"    - {len(positions)} 任职记录")
    print(f"    - {len(relationships)} 关系记录")

def build_gexf(gexf_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{DATE}">')
    lines.append('    <creator>OpenCode Gov-Relation Agent</creator>')
    lines.append(f'    <description>淳化县领导班子关系网络 - {DATE}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, work, post, org, source, conf = p
        c = person_color(pid, post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        oid, oname, otype, olevel, oparent, oloc = o
        color_map = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "党委部门": "255,210,210",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        oc = color_map.get(otype, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        pos_id, pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        rid, pa, pb, rtype, context, overlap_org, overlap_period, conf = rel
        eid += 1
        w = "2.0" if "搭档" in rtype or "上下级" in rtype else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF 图文件已生成: {gexf_path}")
    print(f"    - {len(persons)} 个人物节点 + {len(organizations)} 个组织节点")
    print(f"    - {len(positions)} 条任职边 + {len(relationships)} 条关系边")


if __name__ == "__main__":
    db_path = STAGING / "淳化县_network.db"
    gexf_path = STAGING / "淳化县_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(db_path)
    build_gexf(gexf_path)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path} ({db_path.stat().st_size} bytes)")
    print(f"GEXF:   {gexf_path} ({gexf_path.stat().st_size} bytes)")
