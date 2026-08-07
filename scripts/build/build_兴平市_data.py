#!/usr/bin/env python3
"""
兴平市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

兴平市是陕西省咸阳市下辖的县级市，位于咸阳市西部。
数据来源：兴平市人民政府官网 领导之窗 (https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/)
采集日期：2026-08-07

当前领导（官方确认）:
  市委书记: 马鸿（男，汉族，大学，中共党员；此前任兴平市长，2026年晋升书记）
  市委副书记、市长: 杨杰（男，汉族，研究生学历，中共党员）

注意：领导之窗近期处于换届/调整期，个别页面在编人员呈现略有差异
(如市政府领导除杨杰/高论/王维外，另见 赵之汉/赵青/高明/梁养奎/张晓勇 及 刘泉/白选周 等)。
本脚本以领导之窗索引页为准记录在职常委班子与政府主要成员。
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "兴平市"
DATE = "2026-08-07"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 市委常委会 ---
    (1, "马鸿", "男", "汉族", "", "", "大学", "中共党员", "",
     "市委书记", "中共兴平市委",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/mh/", "confirmed"),
    (2, "杨杰", "男", "汉族", "", "", "研究生", "中共党员", "",
     "市委副书记、市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/mh_32488/", "confirmed"),
    (3, "冯永胜", "男", "汉族", "", "", "大学", "中共党员", "",
     "市委副书记", "中共兴平市委",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/fys/", "confirmed"),
    (4, "高论", "男", "汉族", "", "", "研究生", "中共党员", "",
     "市委常委、常务副市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/gl/", "confirmed"),
    (5, "李剑", "男", "汉族", "", "", "研究生", "中共党员", "",
     "市委常委、纪委书记", "中共兴平市纪律检查委员会/市监委",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/lj/", "confirmed"),
    (6, "纪鹏玉", "男", "汉族", "", "", "大学", "中共党员", "",
     "市委常委、组织部部长", "中共兴平市委组织部",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/jpy/", "confirmed"),
    (7, "张倩", "女", "汉族", "", "", "研究生", "中共党员", "",
     "市委常委、宣传部部长", "中共兴平市委宣传部",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/zq/", "confirmed"),
    (8, "李国栋", "男", "汉族", "", "", "大学", "中共党员", "",
     "市委常委、政法委书记", "中共兴平市委政法委员会",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/hjq_29404/", "confirmed"),
    (9, "王维", "男", "汉族", "", "", "研究生", "中共党员", "",
     "市委常委、副市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/ww/", "confirmed"),
    (10, "赵兴军", "男", "汉族", "", "", "大学", "中共党员", "",
     "市委常委、统战部部长、市政协党组副书记", "中共兴平市委统战部",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/jpy_32863/", "confirmed"),
    # --- 市政府其他领导 ---
    (11, "赵之汉", "男", "汉族", "", "", "", "中共党员", "",
     "副市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/swld_17782/mh/", "plausible"),
    (12, "赵青", "男", "汉族", "", "", "", "中共党员", "",
     "副市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "plausible"),
    (13, "高明", "男", "汉族", "", "", "", "中共党员", "",
     "副市长", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "plausible"),
    (14, "梁养奎", "男", "汉族", "", "", "", "中共党员", "",
     "市政府党组成员、高新区管委会主任", "兴平高新技术产业开发区",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "plausible"),
    (15, "张晓勇", "男", "汉族", "", "", "", "中共党员", "",
     "市政府党组成员", "兴平市人民政府",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "plausible"),
    # --- 市人大 / 市政协 ---
    (16, "王敏", "男", "汉族", "", "", "", "中共党员", "",
     "市人大常委会主任", "兴平市人大常委会",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "confirmed"),
    (17, "庞联昌", "男", "汉族", "", "", "", "中共党员", "",
     "市政协主席", "兴平市政协",
     "https://www.snxingping.gov.cn/zwgk/fdzdgknr/ldzc/", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共兴平市委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市兴平市"),
    (2, "兴平市人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市兴平市"),
    (3, "中共兴平市纪委/市监委", "纪委", "县处级", "中共咸阳市委", "陕西省咸阳市兴平市"),
    (4, "中共兴平市委组织部", "党委部门", "正科级", "中共兴平市委", "陕西省咸阳市兴平市"),
    (5, "中共兴平市委宣传部", "党委部门", "正科级", "中共兴平市委", "陕西省咸阳市兴平市"),
    (6, "中共兴平市委统战部", "党委部门", "正科级", "中共兴平市委", "陕西省咸阳市兴平市"),
    (7, "中共兴平市委政法委员会", "党委部门", "正科级", "中共兴平市委", "陕西省咸阳市兴平市"),
    (8, "兴平市人大常委会", "人大", "县处级", "咸阳市人大常委会", "陕西省咸阳市兴平市"),
    (9, "兴平市政协", "政协", "县处级", "咸阳市政协", "陕西省咸阳市兴平市"),
    (10, "兴平高新技术产业开发区", "开发区", "县级", "咸阳市人民政府", "陕西省咸阳市兴平市"),
]

# ===== 任职数据 =====
# (id, person_id, org_id, title, start, end, rank, note)
positions = [
    (1, 1, 1, "市委书记", "约2026年", "至今", "正县级", "主持市委全面工作；此前任兴平市长"),
    (2, 2, 1, "市委副书记", "约2026年", "至今", "副县级", "协助书记抓政府全面工作"),
    (3, 2, 2, "市长", "约2026年", "至今", "正县级", "主持市政府全面工作，分管市财政局、市审计局"),
    (4, 3, 1, "市委副书记", "至今", "至今", "副县级", "协助书记抓党建、统管三农，兼任市委党校校长"),
    (5, 4, 1, "市委常委", "至今", "至今", "副县级", ""),
    (6, 4, 2, "常务副市长", "至今", "至今", "副县级", "负责市政府常务工作，兼高新区工委书记，负责高新区全面工作"),
    (7, 5, 1, "市委常委", "至今", "至今", "副县级", ""),
    (8, 5, 3, "纪委书记", "至今", "至今", "副县级", "主持市纪委监委全面工作，分管市委巡察办"),
    (9, 6, 1, "市委常委", "至今", "至今", "副县级", ""),
    (10, 6, 4, "组织部部长", "至今", "至今", "副县级", "主持市委组织部全面工作，分管编办、总工会、群团"),
    (11, 7, 1, "市委常委", "至今", "至今", "副县级", ""),
    (12, 7, 5, "宣传部部长", "至今", "至今", "副县级", "主持市委宣传部，兼市委网信办主任，分管融媒体中心"),
    (13, 8, 1, "市委常委", "至今", "至今", "副县级", ""),
    (14, 8, 7, "政法委书记", "至今", "至今", "副县级", "负责政法、综治、信访和社会稳定"),
    (15, 9, 1, "市委常委", "至今", "至今", "副县级", ""),
    (16, 9, 2, "副市长", "至今", "至今", "副县级", "负责城市建设、综合治理和文化旅游"),
    (17, 10, 1, "市委常委", "至今", "至今", "副县级", ""),
    (18, 10, 6, "统战部部长", "至今", "至今", "副县级", "主持市委统战部，兼市政协党组副书记"),
    (19, 11, 2, "副市长", "至今", "至今", "副县级", ""),
    (20, 12, 2, "副市长", "至今", "至今", "副县级", ""),
    (21, 13, 2, "副市长", "至今", "至今", "副县级", ""),
    (22, 14, 10, "高新区党工委副书记、管委会主任", "至今", "至今", "副县级", "市政府党组成员"),
    (23, 15, 2, "市政府党组成员", "至今", "至今", "副县级", ""),
    (24, 16, 8, "市人大常委会主任", "至今", "至今", "正县级", ""),
    (25, 17, 9, "市政协主席", "至今", "至今", "正县级", ""),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # 党政一把手搭档
    (1, 1, 2, "搭档", "市委书记与市长——近期新上任的党政一把手搭档", "中共兴平市委/兴平市人民政府", "至今", "confirmed"),
    # 书记与党委副书记/常委
    (2, 1, 3, "上下级", "市委书记与专职副书记", "中共兴平市委", "至今", "confirmed"),
    (3, 1, 4, "上下级", "市委书记与常务副市长", "中共兴平市委", "至今", "confirmed"),
    (4, 1, 5, "上下级", "市委书记与纪委书记", "中共兴平市委", "至今", "confirmed"),
    (5, 1, 6, "上下级", "市委书记与组织部部长", "中共兴平市委", "至今", "confirmed"),
    (6, 1, 7, "上下级", "市委书记与宣传部部长", "中共兴平市委", "至今", "confirmed"),
    (7, 1, 8, "上下级", "市委书记与政法委书记", "中共兴平市委", "至今", "confirmed"),
    (8, 1, 9, "上下级", "市委书记与副市长王维", "中共兴平市委", "至今", "confirmed"),
    (9, 1, 10, "上下级", "市委书记与统战部部长", "中共兴平市委", "至今", "confirmed"),
    # 市长与副市长
    (10, 2, 4, "上下级", "市长与常务副市长高论——政府日常工作主要搭档", "兴平市人民政府", "至今", "confirmed"),
    (11, 2, 9, "上下级", "市长与副市长王维", "兴平市人民政府", "至今", "confirmed"),
    (12, 2, 11, "上下级", "市长与副市长", "兴平市人民政府", "至今", "confirmed"),
    (13, 2, 12, "上下级", "市长与副市长", "兴平市人民政府", "至今", "confirmed"),
    (14, 2, 13, "上下级", "市长与副市长", "兴平市人民政府", "至今", "confirmed"),
    # 常委之间协作
    (15, 6, 5, "同僚", "组织部与纪委在干部监督上的协作", "中共兴平市委", "至今", "confirmed"),
    (16, 8, 5, "同僚", "政法委与纪委在涉法涉诉、作风监督上的协作", "中共兴平市委", "至今", "confirmed"),
    # 市委与人大政协
    (17, 1, 16, "上下级", "市委书记与市人大常委会主任", "中共兴平市委/兴平市人大常委会", "至今", "confirmed"),
    (18, 1, 17, "上下级", "市委书记与市政协主席", "中共兴平市委/兴平市政协", "至今", "confirmed"),
]

# ===== 生成函数 =====
def esc(s):
    return escape(str(s)) if s is not None else ""

def person_color(pid, post):
    if post == "市委书记":
        return "255,50,50"
    if "市长" in post and "副" not in post[:2]:
        return "50,100,255"
    if "常务" in post or ("副市长" in post):
        return "50,100,255"
    if "纪委" in post or "监委" in post or "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "50,150,150"
    if "政协" in post:
        return "150,80,150"
    return "100,100,100"

def is_top_leader(post):
    return post == "市委书记" or ("市长" in post and "副" not in post[:2])

def build_sqlite(DB_PATH):
    conn = sqlite3.connect(str(DB_PATH))
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
    print(f"  SQLite 数据库已生成: {DB_PATH}")
    print(f"    - {len(persons)} 人物")
    print(f"    - {len(organizations)} 组织")
    print(f"    - {len(positions)} 任职记录")
    print(f"    - {len(relationships)} 关系记录")

def build_gexf(GEXF_PATH):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{DATE}">')
    lines.append('    <creator>OpenCode Gov-Relation Agent</creator>')
    lines.append(f'    <description>兴平市领导班子关系网络 - {DATE}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

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

    for o in organizations:
        oid, oname, otype, olevel, oparent, oloc = o
        color_map = {
            "党委": "255,200,200", "政府": "200,200,255",
            "纪委": "255,220,200", "党委部门": "255,210,210",
            "人大": "200,255,255", "政协": "255,240,200", "开发区": "200,255,200",
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
        w = "2.0" if ("搭档" in rtype or "上下级" in rtype) else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF 图文件已生成: {GEXF_PATH}")
    print(f"    - {len(persons)} 个人物节点 + {len(organizations)} 个组织节点")
    print(f"    - {len(positions)} 条任职边 + {len(relationships)} 条关系边")


if __name__ == "__main__":
    staging = Path(__file__).parent.resolve()
    DB_PATH = staging / "兴平市_network.db"
    GEXF_PATH = staging / "兴平市_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(DB_PATH)
    build_gexf(GEXF_PATH)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {DB_PATH} ({DB_PATH.stat().st_size} bytes)")
    print(f"GEXF:   {GEXF_PATH} ({GEXF_PATH.stat().st_size} bytes)")