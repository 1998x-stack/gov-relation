#!/usr/bin/env python3
"""
彬州市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

彬州市是陕西省咸阳市下辖的县级市，位于咸阳市西北部。
数据来源：彬州市政府网站 (www.snbinzhou.gov.cn) 领导之窗页面
采集日期：2026-07-25

当前领导:
  市委书记: 陈加宝 (1985年5月生)
  市长: 尚小刚 (1974年10月生)
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "彬州市"
DATE = "2026-07-25"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 市委领导 ---
    (1, "陈加宝", "男", "汉族", "1985年5月", "", "研究生学历", "中共党员", "",
     "市委书记", "中共彬州市委",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776667.html", "confirmed"),
    (2, "尚小刚", "男", "汉族", "1974年10月", "", "省委党校研究生学历", "中共党员", "",
     "市委副书记、市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776666.html", "confirmed"),
    (3, "王斌", "男", "汉族", "1979年6月", "", "省委党校研究生学历", "中共党员", "",
     "市委副书记", "中共彬州市委",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776665.html", "confirmed"),
    (4, "李军申", "男", "汉族", "1971年11月", "", "在职研究生学历", "中共党员", "",
     "市委常委、常务副市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776662.html", "confirmed"),
    (5, "郭嘉楠", "男", "汉族", "1984年9月", "", "在职研究生学历", "中共党员", "",
     "市委常委、宣传部部长", "中共彬州市委宣传部",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776661.html", "confirmed"),
    (6, "吕银河", "男", "汉族", "1973年8月", "", "在职研究生学历", "中共党员", "",
     "市委常委、副市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202409/t20240903_1807428.html", "confirmed"),
    (7, "张明军", "男", "汉族", "1979年3月", "", "在职研究生学历", "中共党员", "",
     "市委常委、政法委书记", "中共彬州市委政法委",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776660.html", "confirmed"),
    (8, "李剑", "男", "汉族", "1981年7月", "", "大学学历", "中共党员", "",
     "市委常委、组织部部长", "中共彬州市委组织部",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776658.html", "confirmed"),
    (9, "葛兵", "男", "汉族", "1983年12月", "", "研究生学历", "中共党员", "",
     "市委常委、纪委书记", "中共彬州市纪委/市监委",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776663.html", "confirmed"),
    (10, "权海峰", "男", "汉族", "1978年7月", "", "大学学历", "中共党员", "",
     "市委常委、人武部政委", "彬州市人民武装部",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776664.html", "confirmed"),
    (11, "唐海岗", "男", "汉族", "1981年12月", "", "在职研究生学历", "中共党员", "",
     "市委常委、统战部部长", "中共彬州市委统战部",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202511/t20251128_2037379.html", "confirmed"),

    # --- 市政府领导 ---
    (12, "姜岗", "男", "汉族", "1975年12月", "", "大学学历", "中共党员", "",
     "副市长、公安局局长", "彬州市公安局",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202207/t20220705_787014.html", "confirmed"),
    (13, "伊丽娜", "女", "维吾尔族", "1981年5月", "", "大学学历", "民建会员/中共党员", "",
     "副市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202301/t20230116_1586733.html", "confirmed"),
    (14, "赵亚鹏", "男", "汉族", "1974年11月", "", "大学学历", "中共党员", "",
     "副市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202409/t20240903_1807392.html", "confirmed"),
    (15, "怀刚", "男", "汉族", "1980年8月", "", "大学学历", "中共党员", "",
     "副市长", "彬州市人民政府",
     "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202207/t20220705_787013.html", "confirmed"),

    # --- 人大领导 --- (from 乾县 pattern - not listed on official ldzc page, included as plausible)
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共彬州市委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市彬州市"),
    (2, "彬州市人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市彬州市"),
    (3, "中共彬州市纪委/市监委", "纪委", "县处级", "中共彬州市委", "陕西省咸阳市彬州市"),
    (4, "中共彬州市委组织部", "党委部门", "正科级", "中共彬州市委", "陕西省咸阳市彬州市"),
    (5, "中共彬州市委宣传部", "党委部门", "正科级", "中共彬州市委", "陕西省咸阳市彬州市"),
    (6, "中共彬州市委统战部", "党委部门", "正科级", "中共彬州市委", "陕西省咸阳市彬州市"),
    (7, "中共彬州市委政法委", "党委部门", "正科级", "中共彬州市委", "陕西省咸阳市彬州市"),
    (8, "彬州市人民武装部", "军事", "县处级", "咸阳军分区", "陕西省咸阳市彬州市"),
    (9, "彬州市公安局", "政府", "正科级", "彬州市人民政府", "陕西省咸阳市彬州市"),
]

# ===== 任职数据 =====
# (id, person_id, org_id, title, start, end, rank, note)
positions = [
    # 市委领导任职
    (1, 1, 1, "市委书记", "未知", "至今", "正县级", "主持市委全面工作"),
    (2, 2, 1, "市委副书记", "未知", "至今", "正县级", "同时任市长"),
    (2, 2, 2, "市长", "未知", "至今", "正县级", "领导市政府全面工作"),
    (3, 3, 1, "市委副书记", "未知", "至今", "副县级", "协助书记抓党建，分管三农、群团"),
    (4, 4, 1, "市委常委", "未知", "至今", "副县级", ""),
    (4, 4, 2, "常务副市长", "未知", "至今", "副县级", "分管发改、应急、人社等"),
    (5, 5, 1, "市委常委", "未知", "至今", "副县级", ""),
    (5, 5, 5, "宣传部部长", "未知", "至今", "副县级", "分管宣传、意识形态、网信"),
    (6, 6, 1, "市委常委", "未知", "至今", "副县级", ""),
    (6, 6, 2, "副市长", "未知", "至今", "副县级", "分管工信、民政、交通、经开区"),
    (7, 7, 1, "市委常委", "未知", "至今", "副县级", ""),
    (7, 7, 7, "政法委书记", "未知", "至今", "副县级", "负责政法、平安建设、信访"),
    (8, 8, 1, "市委常委", "未知", "至今", "副县级", ""),
    (8, 8, 4, "组织部部长", "未知", "至今", "副县级", "负责组织工作"),
    (9, 9, 1, "市委常委", "未知", "至今", "副县级", ""),
    (9, 9, 3, "纪委书记", "未知", "至今", "副县级", "主持纪委监委工作"),
    (10, 10, 1, "市委常委", "未知", "至今", "副县级", ""),
    (10, 10, 8, "人武部政委", "未知", "至今", "副县级", "负责军事和人民武装"),
    (11, 11, 1, "市委常委", "未知", "至今", "副县级", ""),
    (11, 11, 6, "统战部部长", "未知", "至今", "副县级", "负责统一战线、民族宗教"),

    # 市政府领导任职
    (12, 12, 9, "副市长、公安局局长", "未知", "至今", "副县级", "分管公安、司法、退役军人"),
    (13, 13, 2, "副市长", "未知", "至今", "副县级", "分管教育、文旅、卫健、医保"),
    (14, 14, 2, "副市长", "未知", "至今", "副县级", "分管自然资源、水利、农业农村"),
    (15, 15, 2, "副市长", "未知", "至今", "副县级", "分管科技、招商"),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # 党政一把手
    (1, 1, 2, "搭档", "市委书记与市长——党政一把手搭档工作", "中共彬州市委/彬州市人民政府", "至今", "confirmed"),

    # 书记与市委常委
    (1, 1, 3, "上下级", "市委书记与专职副书记", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 4, "上下级", "市委书记与常务副市长", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 5, "上下级", "市委书记与宣传部部长", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 6, "上下级", "市委书记与副市长吕银河", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 7, "上下级", "市委书记与政法委书记", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 8, "上下级", "市委书记与组织部部长", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 9, "上下级", "市委书记与纪委书记", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 10, "上下级", "市委书记与人武部政委", "中共彬州市委", "至今", "confirmed"),
    (1, 1, 11, "上下级", "市委书记与统战部部长", "中共彬州市委", "至今", "confirmed"),

    # 市长与副市长
    (1, 2, 4, "上下级", "市长与常务副市长——政府日常工作搭档", "彬州市人民政府", "至今", "confirmed"),
    (1, 2, 6, "上下级", "市长与副市长吕银河", "彬州市人民政府", "至今", "confirmed"),
    (1, 2, 12, "上下级", "市长与副市长、公安局长姜岗", "彬州市人民政府", "至今", "confirmed"),
    (1, 2, 13, "上下级", "市长与副市长伊丽娜", "彬州市人民政府", "至今", "confirmed"),
    (1, 2, 14, "上下级", "市长与副市长赵亚鹏", "彬州市人民政府", "至今", "confirmed"),
    (1, 2, 15, "上下级", "市长与副市长怀刚", "彬州市人民政府", "至今", "confirmed"),

    # 常委屈内部常委间关系
    (1, 4, 8, "同僚", "同一届市委常委班子中的工作协作", "中共彬州市委", "至今", "confirmed"),
    (1, 8, 9, "同僚", "组织部与纪委的工作协作（干部监督）", "中共彬州市委", "至今", "confirmed"),
    (1, 7, 12, "同僚", "政法委与公安局的工作协作", "中共彬州市委/彬州市公安局", "至今", "confirmed"),
]

# ===== 生成函数 =====
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid, post):
    if "市委书记" == post:
        return "255,50,50"
    if "市长" in post and "副" not in post[:2]:
        return "50,100,255"
    if "常务" in post or ("副市长" in post):
        return "50,100,255"
    if "纪委" in post or "监委" in post or "纪委书记" in post:
        return "255,165,0"
    return "100,100,100"

def is_top_leader(post):
    return "市委书记" == post or ("市长" in post and "副" not in post[:2])

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
    lines.append(f'    <description>彬州市领导班子关系网络 - {DATE}</description>')
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
    db_path = staging / "彬州市_network.db"
    gexf_path = staging / "彬州市_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(db_path)
    build_gexf(gexf_path)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path} ({db_path.stat().st_size} bytes)")
    print(f"GEXF:   {gexf_path} ({gexf_path.stat().st_size} bytes)")
