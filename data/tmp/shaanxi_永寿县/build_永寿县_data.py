#!/usr/bin/env python3
"""
永寿县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

永寿县是陕西省咸阳市下辖的县，位于咸阳市北部。
数据来源：永寿县政府网站 (www.yongshou.gov.cn) 领导之窗页面
采集日期：2026-07-25

当前领导:
   县委书记: 杨孟珠
   县长: 闫启东
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

SLUG = "永寿县"
DATE = "2026-07-25"

# #################### TEMP STAGING ####################
# When the script lives under data/tmp/<task_id>/, output there.
# After promotion to repo root, output goes to canonical locations.
SCRIPT_DIR = Path(__file__).parent.resolve()
IS_STAGED = SCRIPT_DIR.parent.name == "tmp"

if IS_STAGED:
    DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
    GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"
else:
    if USING_RUNNER:
        DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
        GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"
    else:
        DB_PATH = REPO_ROOT / "data" / "database" / f"{SLUG}_network.db"
        GEXF_PATH = REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委领导 ---
    (1, "杨孟珠", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/ymz/", "confirmed"),
    (2, "闫启东", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县政府党组书记、县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yqd_33017/", "confirmed"),
    (3, "王斌", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记", "中共永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/wb/", "confirmed"),
    (4, "张凯祺", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、宣传部部长", "中共永寿县委宣传部",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/zkq/", "confirmed"),
    (5, "李婉妮", "女", "汉族", "", "", "", "中共党员", "",
     "县委常委、县政府党组副书记、副县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/can_32659/", "confirmed"),
    (6, "文海荣", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、纪委书记、监委会主任", "中共永寿县纪律检查委员会/县监察委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/hj_32619/", "confirmed"),
    (7, "燕军永", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yjy/", "confirmed"),
    (8, "畅阿妮", "女", "汉族", "", "", "", "中共党员", "",
     "县委常委、组织部部长", "中共永寿县委组织部",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/can/", "confirmed"),
    (9, "梁高峰", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、统战部部长", "中共永寿县委统战部",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lgf/", "confirmed"),
    (10, "姚红良", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长（挂职）", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yhl_26656/", "confirmed"),
    (11, "李爽", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长（挂职）", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/ls/", "confirmed"),
    (12, "王剑", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、副县长（挂职）", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/wj_33114/", "confirmed"),

    # --- 县政府领导 ---
    (13, "杨君锋", "男", "汉族", "", "", "", "中共党员", "",
     "副县长兼公安局局长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/yjf_33027/", "confirmed"),
    (14, "王宁", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/wn/", "confirmed"),
    (15, "董伟国", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/dwg/", "confirmed"),
    (16, "王振", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "永寿县人民政府",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/yjy_32663/", "confirmed"),

    # --- 县人大领导 ---
    (17, "屈春生", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会党组书记、主任", "永寿县人民代表大会常务委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/qcs/", "confirmed"),
    (18, "师保忠", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会党组副书记、副主任", "永寿县人民代表大会常务委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/sbz/", "confirmed"),
    (19, "郭志龙", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "永寿县人民代表大会常务委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/gzl/", "confirmed"),
    (20, "李涛", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "永寿县人民代表大会常务委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/lt/", "confirmed"),
    (21, "孙丽", "女", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "永寿县人民代表大会常务委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/sl/", "confirmed"),

    # --- 县政协领导 ---
    (22, "樊莉霞", "女", "汉族", "", "", "", "中共党员", "",
     "县政协党组书记、主席", "中国人民政治协商会议永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/flx/", "confirmed"),
    (23, "贾鹏飞", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "中国人民政治协商会议永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/jpf/", "confirmed"),
    (24, "姚旭辉", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "中国人民政治协商会议永寿县委员会",
     "https://www.yongshou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/yxh/", "confirmed"),

    # --- 前任领导 ---
    (25, "王飞", "男", "汉族", "", "", "", "中共党员", "",
     "原县委书记（前任）", "中共永寿县委员会",
     "https://www.yongshou.gov.cn/xwzx/jrys/202603/t20260327_2071955.html", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共永寿县委员会", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市永寿县"),
    (2, "永寿县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市永寿县"),
    (3, "中共永寿县委宣传部", "党委部门", "正科级", "中共永寿县委员会", "陕西省咸阳市永寿县"),
    (4, "中共永寿县委组织部", "党委部门", "正科级", "中共永寿县委员会", "陕西省咸阳市永寿县"),
    (5, "中共永寿县纪律检查委员会/县监察委员会", "纪委", "县处级", "中共永寿县委员会", "陕西省咸阳市永寿县"),
    (6, "中共永寿县委统战部", "党委部门", "正科级", "中共永寿县委员会", "陕西省咸阳市永寿县"),
    (7, "永寿县公安局", "政府部门", "正科级", "永寿县人民政府", "陕西省咸阳市永寿县"),
    (8, "永寿县人民代表大会常务委员会", "人大", "县处级", "陕西省人大常委会", "陕西省咸阳市永寿县"),
    (9, "中国人民政治协商会议永寿县委员会", "政协", "县处级", "陕西省政协", "陕西省咸阳市永寿县"),
]

# ===== 任职数据 =====
# (person_id, org_id, title, start, end, rank, note)
positions = [
    # 县委
    (1, 1, "县委书记", "", "至今", "正处级", "主持县委全面工作"),
    (2, 1, "县委副书记", "", "至今", "副处级", ""),
    (2, 2, "县政府党组书记、县长", "", "至今", "正处级", "领导县政府全面工作"),
    (3, 1, "县委副书记", "", "至今", "副处级", "协助书记抓党的建设工作，分管三农、群团等"),
    (4, 3, "县委常委、宣传部部长", "", "至今", "副处级", "主持县委宣传部全面工作"),
    (5, 1, "县委常委", "", "至今", "副处级", ""),
    (5, 2, "县政府党组副书记、副县长", "", "至今", "副处级", "常务副县长"),
    (6, 5, "县委常委、纪委书记、监委会主任", "", "至今", "副处级", "主持县纪委监委全面工作"),
    (7, 1, "县委常委", "", "至今", "副处级", ""),
    (7, 2, "副县长", "", "至今", "副处级", "分管住建、市场监管、文旅、林业等"),
    (8, 4, "县委常委、组织部部长", "", "至今", "副处级", "主持县委组织部全面工作"),
    (9, 6, "县委常委、统战部部长", "", "至今", "副处级", "主持县委统战部全面工作"),
    (10, 2, "副县长（挂职）", "", "至今", "副处级", ""),
    (11, 2, "副县长（挂职）", "", "至今", "副处级", ""),
    (12, 2, "副县长（挂职）", "", "至今", "副处级", ""),
    # 县政府
    (13, 2, "副县长", "", "至今", "副处级", "分管公安、司法、退役军人事务"),
    (13, 7, "县公安局局长", "", "至今", "正科级", ""),
    (14, 2, "副县长", "", "至今", "副处级", "分管交通、教育、卫健、招商、医保"),
    (15, 2, "副县长", "", "至今", "副处级", "分管工信、民政、科技、生态环境"),
    (16, 2, "副县长", "", "至今", "副处级", ""),
    # 人大
    (17, 8, "县人大常委会党组书记、主任", "", "至今", "正处级", ""),
    (18, 8, "县人大常委会党组副书记、副主任", "", "至今", "副处级", ""),
    (19, 8, "县人大常委会副主任", "", "至今", "副处级", ""),
    (20, 8, "县人大常委会副主任", "", "至今", "副处级", ""),
    (21, 8, "县人大常委会副主任", "", "至今", "副处级", ""),
    # 政协
    (22, 9, "县政协党组书记、主席", "", "至今", "正处级", ""),
    (23, 9, "县政协副主席", "", "至今", "副处级", ""),
    (24, 9, "县政协副主席", "", "至今", "副处级", ""),
    # 前任
    (25, 1, "县委书记", "", "2026年前后", "正处级", "前任县委书记"),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 县委班子内部关系 - 同一届县委常委会
    (1, 2, "党政协同", "县委书记与县长党政正职搭配", "中共永寿县委员会/永寿县人民政府", "至今"),
    (1, 3, "上下级", "县委书记与县委副书记", "中共永寿县委员会", "至今"),
    (1, 4, "上下级", "县委书记与宣传部长", "中共永寿县委员会", "至今"),
    (1, 5, "上下级", "县委书记与常务副县长", "中共永寿县委员会/永寿县人民政府", "至今"),
    (1, 6, "上下级", "县委书记与纪委书记", "中共永寿县委员会", "至今"),
    (1, 7, "上下级", "县委书记与副县长", "中共永寿县委员会/永寿县人民政府", "至今"),
    (1, 8, "上下级", "县委书记与组织部长", "中共永寿县委员会", "至今"),
    (1, 9, "上下级", "县委书记与统战部长", "中共永寿县委员会", "至今"),
    (2, 5, "上下级", "县长与常务副县长", "永寿县人民政府", "至今"),
    (2, 7, "上下级", "县长与副县长", "永寿县人民政府", "至今"),
    (2, 13, "上下级", "县长与副县长", "永寿县人民政府", "至今"),
    (2, 14, "上下级", "县长与副县长", "永寿县人民政府", "至今"),
    (2, 15, "上下级", "县长与副县长", "永寿县人民政府", "至今"),
    (2, 16, "上下级", "县长与副县长", "永寿县人民政府", "至今"),
    # 前任-现任关系
    (25, 1, "前后任", "前任县委书记与现任县委书记交接", "中共永寿县委员会", "2025-2026"),
    # 人大与县委
    (17, 1, "党政协同", "人大主任与县委书记", "永寿县", "至今"),
    # 政协与县委
    (22, 1, "党政协同", "政协主席与县委书记", "永寿县", "至今"),
]

# ===== 辅助函数 =====
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id, name, current_post):
    """返回 GEXF 节点颜色 r,g,b 字符串"""
    if "县委书记" in current_post or "原县委书记" in current_post:
        return "255,50,50"  # Red
    if "县长" in current_post and "副" not in current_post:
        return "50,100,255"  # Blue
    if "纪委书记" in current_post or "监委会" in current_post:
        return "255,165,0"  # Orange
    if "县委副书记" in current_post:
        return "200,50,50"  # Dark red
    if "副县长" in current_post or "常务副县长" in current_post:
        return "100,150,255"  # Light blue
    if "人大" in current_post:
        return "200,255,255"  # Cyan
    if "政协" in current_post:
        return "255,240,200"  # Cream
    return "100,100,100"  # Grey default

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "政府部门": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(current_post):
    return "县委书记" in current_post and "副" not in current_post

def person_size(current_post):
    if "县委书记" in current_post and "副" not in current_post:
        return "20.0"
    if "县长" in current_post and "副" not in current_post:
        return "20.0"
    if "人大主任" in current_post or "政协主席" in current_post:
        return "16.0"
    return "12.0"

def build_db():
    os.makedirs(str(DB_PATH.parent), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons(
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
            source TEXT,
            confidence TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"  Database written: {DB_PATH}")

def build_gexf():
    os.makedirs(str(GEXF_PATH.parent), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{DATE}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        pid, name, _, _, _, _, _, _, _, current_post, current_org, source, confidence = p
        c = person_color(pid, name, current_post)
        sz = person_size(current_post)
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(current_post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(current_org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        oid, name, otype, level, parent, location = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(level)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges - positions (person -> org)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges - relationships (person <-> person)
    for r in relationships:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(GEXF_PATH), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")

def main():
    print(f"Building {SLUG} leadership network data...")
    build_db()
    build_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
