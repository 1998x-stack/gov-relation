#!/usr/bin/env python3
"""
乾县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

乾县是陕西省咸阳市下辖的县，位于关中平原中部、渭北旱塬。
数据来源：乾县政府网站 (www.snqianxian.gov.cn) 领导之窗页面
采集日期：2026-07-25

当前领导:
  县委书记: 闫兴斌 (1971年9月生)
  县长: 段志华 (1974年4月生)
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "乾县"
DATE = "2026-07-25"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委领导 ---
    (1, "闫兴斌", "男", "汉族", "1971年9月", "", "研究生学历", "中共党员", "",
     "县委书记", "中共乾县县委",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yxb/", "confirmed"),
    (2, "段志华", "男", "汉族", "1974年4月", "", "研究生学历", "中共党员", "",
     "县委副书记、县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/dzha/", "confirmed"),
    (3, "刘春锋", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记", "中共乾县县委",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (4, "吴元操", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、组织部部长", "中共乾县县委组织部",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (5, "张斌", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、纪委书记、监委主任", "中共乾县纪委/县监委",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (6, "何伟", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、宣传部部长", "中共乾县县委宣传部",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (7, "李亚平", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、武装部政委", "乾县人民武装部",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),
    (8, "黄浩", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、统战部部长", "中共乾县县委统战部",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/", "confirmed"),

    # --- 县政府领导 ---
    (9, "孙佳佳", "男", "汉族", "1986年2月", "", "研究生学历，工学硕士", "中共党员", "",
     "县委常委、县政府党组副书记、常务副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/sjj/", "confirmed"),
    (10, "董晓峰", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/", "confirmed"),
    (11, "南伟", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/", "confirmed"),
    (12, "刘宇超", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/", "confirmed"),
    (13, "刘亮", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "乾县人民政府",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/", "confirmed"),

    # --- 县人大领导 ---
    (14, "张会文", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会主任", "乾县人大常委会",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/", "confirmed"),
    (15, "张小宁", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "乾县人大常委会",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/", "confirmed"),
    (16, "冉歆", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "乾县人大常委会",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/", "confirmed"),
    (17, "高志华", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "乾县人大常委会",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/", "confirmed"),
    (18, "巨亚绒", "女", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "乾县人大常委会",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/", "confirmed"),

    # --- 县政协领导 ---
    (19, "穆伟峰", "男", "汉族", "", "", "", "中共党员", "",
     "县政协主席", "乾县政协",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/", "confirmed"),
    (20, "杜亚军", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "乾县政协",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/", "confirmed"),
    (21, "祝晓娣", "女", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "乾县政协",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/", "confirmed"),
    (22, "孙凯", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "乾县政协",
     "http://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共乾县县委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市乾县"),
    (2, "乾县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市乾县"),
    (3, "中共乾县纪委/县监委", "纪委", "县处级", "中共乾县县委", "陕西省咸阳市乾县"),
    (4, "中共乾县县委组织部", "党委部门", "正科级", "中共乾县县委", "陕西省咸阳市乾县"),
    (5, "中共乾县县委宣传部", "党委部门", "正科级", "中共乾县县委", "陕西省咸阳市乾县"),
    (6, "中共乾县县委统战部", "党委部门", "正科级", "中共乾县县委", "陕西省咸阳市乾县"),
    (7, "乾县人民武装部", "军事", "县处级", "咸阳军分区", "陕西省咸阳市乾县"),
    (8, "乾县人大常委会", "人大", "县处级", "咸阳市人大常委会", "陕西省咸阳市乾县"),
    (9, "乾县政协", "政协", "县处级", "咸阳市政协", "陕西省咸阳市乾县"),
]

# ===== 任职数据 =====
positions = [
    # 县委领导任职
    (1, 1, 1, "县委书记", "未知", "至今", "正县级", ""),
    (2, 2, 1, "县委副书记", "未知", "至今", "正县级", "同时任县长"),
    (2, 2, 2, "县长", "未知", "至今", "正县级", ""),
    (3, 3, 1, "县委副书记", "未知", "至今", "副县级", "专职副书记"),
    (4, 4, 4, "县委常委、组织部部长", "未知", "至今", "副县级", ""),
    (5, 5, 3, "县委常委、纪委书记、监委主任", "未知", "至今", "副县级", ""),
    (6, 6, 5, "县委常委、宣传部部长", "未知", "至今", "副县级", ""),
    (7, 7, 7, "县委常委、武装部政委", "未知", "至今", "副县级", ""),
    (8, 8, 6, "县委常委、统战部部长", "未知", "至今", "副县级", ""),

    # 县政府领导任职
    (9, 9, 2, "县委常委、县政府党组副书记、常务副县长", "未知", "至今", "副县级", ""),
    (10, 10, 2, "副县长", "未知", "至今", "副县级", ""),
    (11, 11, 2, "副县长", "未知", "至今", "副县级", ""),
    (12, 12, 2, "副县长", "未知", "至今", "副县级", ""),
    (13, 13, 2, "副县长", "未知", "至今", "副县级", ""),

    # 县人大领导任职
    (14, 14, 8, "县人大常委会主任", "未知", "至今", "正县级", ""),
    (15, 15, 8, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (16, 16, 8, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (17, 17, 8, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (18, 18, 8, "县人大常委会副主任", "未知", "至今", "副县级", ""),

    # 县政协领导任职
    (19, 19, 9, "县政协主席", "未知", "至今", "正县级", ""),
    (20, 20, 9, "县政协副主席", "未知", "至今", "副县级", ""),
    (21, 21, 9, "县政协副主席", "未知", "至今", "副县级", ""),
    (22, 22, 9, "县政协副主席", "未知", "至今", "副县级", ""),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    (1, 1, 2, "搭档", "县委书记与县长——党政一把手搭档工作", "中共乾县县委/乾县人民政府", "至今", "confirmed"),
    (1, 1, 3, "上下级", "县委书记与专职副书记", "中共乾县县委", "至今", "confirmed"),
    (1, 4, 5, "同僚", "同一届县委常委班子", "中共乾县县委", "至今", "confirmed"),
    (1, 1, 4, "上下级", "县委书记与组织部部长", "中共乾县县委", "至今", "confirmed"),
    (1, 1, 5, "上下级", "县委书记与纪委书记", "中共乾县县委", "至今", "confirmed"),
    (1, 1, 6, "上下级", "县委书记与宣传部部长", "中共乾县县委", "至今", "confirmed"),
    (1, 1, 7, "上下级", "县委书记与人武部政委", "中共乾县县委", "至今", "confirmed"),
    (1, 1, 8, "上下级", "县委书记与统战部部长", "中共乾县县委", "至今", "confirmed"),
    (1, 2, 9, "上下级", "县长与常务副县长——政府日常工作搭档", "乾县人民政府", "至今", "confirmed"),
    (1, 2, 10, "上下级", "县长与副县长", "乾县人民政府", "至今", "confirmed"),
    (1, 2, 11, "上下级", "县长与副县长", "乾县人民政府", "至今", "confirmed"),
    (1, 2, 12, "上下级", "县长与副县长", "乾县人民政府", "至今", "confirmed"),
    (1, 2, 13, "上下级", "县长与副县长", "乾县人民政府", "至今", "confirmed"),
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
    if "纪委" in post or "监委" in post or "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    return "100,100,100"

def is_top_leader(post):
    return "县委书记" == post or "县长" in post and "副" not in post[:2]

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
    lines.append(f'    <description>乾县领导班子关系网络 - {DATE}</description>')
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
            "纪委": "255,220,200",
            "党委部门": "255,210,210",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "军事": "220,220,220",
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
    staging = Path(__file__).parent.resolve()
    db_path = staging / "乾县_network.db"
    gexf_path = staging / "乾县_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(db_path)
    build_gexf(gexf_path)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path} ({db_path.stat().st_size} bytes)")
    print(f"GEXF:   {gexf_path} ({gexf_path.stat().st_size} bytes)")
