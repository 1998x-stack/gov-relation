#!/usr/bin/env python3
"""
延川县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

延川县是陕西省延安市下辖的县，位于陕西省北部、延安市东北部。
数据来源：延川县人民政府网站 (www.yanchuan.gov.cn) 领导之窗页面及本地要闻
采集日期：2026-07-25

当前领导:
  县委书记: 崔亚军
  县长: 高汉武 (1973年7月生)
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

SLUG = "延川县"
DATE = "2026-07-25"

# process_tmp.py 校验用路径变量
DB_PATH = ""
GEXF_PATH = ""

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委领导 ---
    (1, "崔亚军", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共延川县委",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077325933283086337.html", "confirmed"),
    (2, "高汉武", "男", "汉族", "1973年7月", "陕西省志丹县", "大学本科学历", "中共党员", "1994年7月",
     "县委副书记、县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xc/ghw/1.html", "confirmed"),
    (3, "张修谦", "男", "汉族", "1972年9月", "延安市宝塔区", "研究生学历", "中共党员", "1992年7月",
     "县委常委、常务副县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/cwfxc/zxq/1.html", "confirmed"),
    (4, "韩永星", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、政法委书记", "中共延川县委政法委",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2079001147055542273.html", "confirmed"),
    (5, "段向斌", "男", "汉族", "", "", "研究生学历（中央党校函授）", "中共党员", "",
     "县委常委、副县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/dxb/1.html", "confirmed"),
    (6, "江城", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长（挂职）", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2029372332568723458.html", "confirmed"),

    # --- 县政府领导 ---
    (7, "高蕊", "女", "汉族", "1978年7月", "陕西宝塔区", "省委党校研究生学历，管理学学士", "无党派", "2002年12月",
     "副县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/gr/1.html", "confirmed"),
    (8, "宜振银", "男", "汉族", "1972年1月", "", "大学学历，法学学士", "中共党员", "1995年7月",
     "副县长、公安局局长", "延川县公安局",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/yzy/1.html", "confirmed"),
    (9, "崔泰康", "男", "汉族", "1984年7月", "陕西延长", "研究生学历，法学硕士", "中共党员", "2007年8月",
     "副县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/ctk/1.html", "confirmed"),
    (10, "白波", "男", "汉族", "1989年10月", "", "研究生学历", "中共党员", "",
     "副县长", "延川县人民政府",
     "https://www.yanchuan.gov.cn/zfxxgk/fdzdgknr/ldzc/fxc/bb/1.html", "confirmed"),

    # --- 县人大领导 ---
    (11, "吴慧婷", "女", "汉族", "", "", "", "中共党员", "",
     "县人大常委会主任", "延川县人大常委会",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077188300568813570.html", "confirmed"),
    (12, "董国璟", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "延川县人大常委会",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077188300568813570.html", "confirmed"),
    (13, "白志斌", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "延川县人大常委会",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077188300568813570.html", "confirmed"),
    (14, "张群", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "延川县人大常委会",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077188300568813570.html", "confirmed"),
    (15, "王东娥", "女", "汉族", "", "", "", "", "",
     "县人大常委会副主任", "延川县人大常委会",
     "https://www.yanchuan.gov.cn/zwdt/bdyw/2077188300568813570.html", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共延川县委", "党委", "县处级", "中共延安市委", "陕西省延安市延川县"),
    (2, "延川县人民政府", "政府", "县处级", "延安市人民政府", "陕西省延安市延川县"),
    (3, "中共延川县委政法委", "党委部门", "正科级", "中共延川县委", "陕西省延安市延川县"),
    (4, "延川县公安局", "政府", "正科级", "延川县人民政府", "陕西省延安市延川县"),
    (5, "延川县人大常委会", "人大", "县处级", "延安市人大常委会", "陕西省延安市延川县"),
]

# ===== 任职数据 =====
positions = [
    # 县委领导任职
    (1, 1, 1, "县委书记", "未知", "至今", "正县级", ""),
    (2, 2, 1, "县委副书记", "2021年8月", "至今", "正县级", "2021年8月任代县长，2022年3月任县长"),
    (2, 2, 2, "县长", "2022年3月", "至今", "正县级", ""),
    (3, 3, 2, "县委常委、常务副县长", "2021年9月", "至今", "副县级", "曾任县委常委、政法委书记（2019-2021）"),
    (3, 3, 1, "县委常委", "2019年9月", "至今", "副县级", ""),
    (4, 4, 3, "县委常委、政法委书记", "未知", "至今", "副县级", ""),
    (4, 4, 1, "县委常委", "未知", "至今", "副县级", ""),
    (5, 5, 2, "县委常委、副县长", "2024年1月", "至今", "副县级", "2024年1月起任县委常委、副县长；此前任副县长（2020.12-2024.01）"),
    (5, 5, 1, "县委常委", "2024年1月", "至今", "副县级", ""),
    (6, 6, 2, "县委常委、副县长（挂职）", "未知", "至今", "副县级", "江阴对口协作挂职干部"),

    # 县政府领导任职
    (7, 7, 2, "副县长", "2026年1月", "至今", "副县级", "此前任甘泉县副县长（2020.12-2026.01）"),
    (8, 8, 4, "副县长、公安局局长", "2021年10月", "至今", "副县级", "2021年9月任延川县公安局局长；2021年10月任副县长"),
    (9, 9, 2, "副县长", "2021年10月", "至今", "副县级", ""),
    (10, 10, 2, "副县长", "未知", "至今", "副县级", ""),

    # 县人大领导任职
    (11, 11, 5, "县人大常委会主任", "未知", "至今", "正县级", ""),
    (12, 12, 5, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (13, 13, 5, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (14, 14, 5, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (15, 15, 5, "县人大常委会副主任", "未知", "至今", "副县级", ""),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    (1, 1, 2, "搭档", "县委书记与县长——党政一把手搭档工作", "中共延川县委/延川县人民政府", "至今", "confirmed"),
    (1, 1, 3, "上下级", "县委书记与常务副县长", "中共延川县委", "至今", "confirmed"),
    (1, 1, 4, "上下级", "县委书记与政法委书记", "中共延川县委", "至今", "confirmed"),
    (1, 1, 5, "上下级", "县委书记与县委常委、副县长", "中共延川县委", "至今", "confirmed"),
    (1, 1, 6, "上下级", "县委书记与挂职副县长", "中共延川县委", "至今", "confirmed"),
    (2, 2, 3, "上下级", "县长与常务副县长——政府日常工作搭档", "延川县人民政府", "至今", "confirmed"),
    (2, 2, 7, "上下级", "县长与副县长", "延川县人民政府", "至今", "confirmed"),
    (2, 2, 9, "上下级", "县长与副县长", "延川县人民政府", "至今", "confirmed"),
    (2, 2, 10, "上下级", "县长与副县长", "延川县人民政府", "至今", "confirmed"),
    (2, 2, 5, "上下级", "县长与县委常委、副县长", "延川县人民政府", "至今", "confirmed"),
    (2, 2, 6, "上下级", "县长与挂职副县长", "延川县人民政府", "至今", "confirmed"),
    (1, 3, 4, "同僚", "同一届县委常委班子", "中共延川县委", "至今", "confirmed"),
    (1, 3, 5, "同僚", "同一届县委常委班子", "中共延川县委", "至今", "confirmed"),
    (1, 4, 5, "同僚", "同一届县委常委班子", "中共延川县委", "至今", "confirmed"),
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
    if "政法" in post:
        return "150,150,50"
    return "100,100,100"

def is_top_leader(post):
    return "县委书记" == post or ("县长" in post and "副" not in post[:2])

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
    lines.append(f'    <description>延川县领导班子关系网络 - {DATE}</description>')
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
    db_path = staging / "延川县_network.db"
    gexf_path = staging / "延川县_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(db_path)
    build_gexf(gexf_path)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path} ({db_path.stat().st_size} bytes)")
    print(f"GEXF:   {gexf_path} ({gexf_path.stat().st_size} bytes)")
