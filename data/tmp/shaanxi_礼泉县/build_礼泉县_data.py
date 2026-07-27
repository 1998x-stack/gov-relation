#!/usr/bin/env python3
"""
礼泉县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

礼泉县是陕西省咸阳市下辖的县，位于关中平原中部。
数据来源：礼泉县人民政府网站 (www.liquan.gov.cn) 领导之窗页面
采集日期：2026-07-25

当前领导:
  县委书记: 姚俊峰
  县长: 吴云锋
"""
import sys
import os
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

SLUG = "礼泉县"
DATE = "2026-07-25"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委领导 ---
    (1, "姚俊峰", "男", "汉族", "", "", "", "中共党员", "",
     "县委书记", "中共礼泉县委",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (2, "吴云锋", "男", "汉族", "", "", "", "中共党员", "",
     "县委副书记、县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (3, "侯晓娟", "女", "汉族", "", "", "", "中共党员", "",
     "县委常委、县纪委书记、监委会主任", "中共礼泉县纪委/县监委",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (4, "杜洪建", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、宣传部部长", "中共礼泉县委宣传部",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (5, "孙党军", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、政法委书记", "中共礼泉县委政法委",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (6, "史航宇", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、统战部部长", "中共礼泉县委统战部",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (7, "赵瑞刚", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、县政府副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (8, "陈三东", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、人民武装部部长", "礼泉县人民武装部",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),

    # --- 县政府领导 ---
    (9, "田小伟", "男", "汉族", "", "", "", "中共党员", "",
     "副县长、县公安局局长", "礼泉县公安局",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (10, "乔薏芯", "女", "汉族", "", "", "", "", "",
     "副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (11, "魏星", "男", "汉族", "", "", "", "", "",
     "副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (12, "王碧波", "男", "汉族", "", "", "", "", "",
     "副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (13, "李敏", "女", "汉族", "", "", "", "", "",
     "副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (14, "杨谦", "男", "汉族", "", "", "", "", "",
     "副县长", "礼泉县人民政府",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),

    # --- 县人大领导 ---
    (15, "曹国巍", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会主任", "礼泉县人大常委会",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (16, "李建源", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任、县总工会主席", "礼泉县人大常委会",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (17, "葛莹", "女", "汉族", "", "", "", "", "",
     "县人大常委会副主任", "礼泉县人大常委会",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (18, "王群虎", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会副主任", "礼泉县人大常委会",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (19, "洪雄利", "男", "汉族", "", "", "", "", "",
     "县人大常委会副主任", "礼泉县人大常委会",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),

    # --- 县政协领导 ---
    (20, "杨力年", "男", "汉族", "", "", "", "中共党员", "",
     "县政协主席", "礼泉县政协",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (21, "陈继华", "男", "汉族", "", "", "", "中共党员", "",
     "县政协副主席", "礼泉县政协",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (22, "张晓情", "女", "汉族", "", "", "", "", "",
     "县政协副主席", "礼泉县政协",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
    (23, "寇蕊", "女", "汉族", "", "", "", "", "",
     "县政协副主席", "礼泉县政协",
     "http://www.liquan.gov.cn/zfxxgk/fdzdgknr/ldzc/", "confirmed"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共礼泉县委", "党委", "县处级", "中共咸阳市委", "陕西省咸阳市礼泉县"),
    (2, "礼泉县人民政府", "政府", "县处级", "咸阳市人民政府", "陕西省咸阳市礼泉县"),
    (3, "中共礼泉县纪委/县监委", "纪委", "县处级", "中共礼泉县委", "陕西省咸阳市礼泉县"),
    (4, "中共礼泉县委宣传部", "党委部门", "正科级", "中共礼泉县委", "陕西省咸阳市礼泉县"),
    (5, "中共礼泉县委政法委", "党委部门", "正科级", "中共礼泉县委", "陕西省咸阳市礼泉县"),
    (6, "中共礼泉县委统战部", "党委部门", "正科级", "中共礼泉县委", "陕西省咸阳市礼泉县"),
    (7, "礼泉县人民武装部", "军事", "县处级", "咸阳军分区", "陕西省咸阳市礼泉县"),
    (8, "礼泉县公安局", "政府", "正科级", "礼泉县人民政府", "陕西省咸阳市礼泉县"),
    (9, "礼泉县人大常委会", "人大", "县处级", "咸阳市人大常委会", "陕西省咸阳市礼泉县"),
    (10, "礼泉县政协", "政协", "县处级", "咸阳市政协", "陕西省咸阳市礼泉县"),
]

# ===== 任职数据 =====
# (id, person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    # 县委领导任职
    (1, 1, 1, "县委书记", "未知", "至今", "正县级", ""),
    (2, 2, 1, "县委副书记", "未知", "至今", "正县级", "同时任县长"),
    (2, 2, 2, "县长", "未知", "至今", "正县级", ""),
    (3, 3, 3, "县委常委、县纪委书记、监委会主任", "未知", "至今", "副县级", ""),
    (4, 4, 4, "县委常委、宣传部部长", "未知", "至今", "副县级", ""),
    (5, 5, 5, "县委常委、政法委书记", "未知", "至今", "副县级", ""),
    (6, 6, 6, "县委常委、统战部部长", "未知", "至今", "副县级", ""),
    (7, 7, 2, "县委常委、县政府副县长", "未知", "至今", "副县级", ""),
    (8, 8, 7, "县委常委、人民武装部部长", "未知", "至今", "副县级", ""),

    # 县政府领导任职
    (9, 9, 8, "副县长、县公安局局长", "未知", "至今", "副县级", ""),
    (10, 10, 2, "副县长", "未知", "至今", "副县级", ""),
    (11, 11, 2, "副县长", "未知", "至今", "副县级", ""),
    (12, 12, 2, "副县长", "未知", "至今", "副县级", ""),
    (13, 13, 2, "副县长", "未知", "至今", "副县级", ""),
    (14, 14, 2, "副县长", "未知", "至今", "副县级", ""),

    # 县人大领导任职
    (15, 15, 9, "县人大常委会主任", "未知", "至今", "正县级", ""),
    (16, 16, 9, "县人大常委会副主任、县总工会主席", "未知", "至今", "副县级", ""),
    (17, 17, 9, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (18, 18, 9, "县人大常委会副主任", "未知", "至今", "副县级", ""),
    (19, 19, 9, "县人大常委会副主任", "未知", "至今", "副县级", ""),

    # 县政协领导任职
    (20, 20, 10, "县政协主席", "未知", "至今", "正县级", ""),
    (21, 21, 10, "县政协副主席", "未知", "至今", "副县级", ""),
    (22, 22, 10, "县政协副主席", "未知", "至今", "副县级", ""),
    (23, 23, 10, "县政协副主席", "未知", "至今", "副县级", ""),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # 县委书记 - 县长 (党政一把手搭档)
    (1, 1, 2, "搭档", "县委书记与县长——党政一把手搭档工作", "中共礼泉县委/礼泉县人民政府", "至今", "confirmed"),

    # 县委书记 - 各县委常委
    (1, 1, 3, "上下级", "县委书记与纪委书记", "中共礼泉县委", "至今", "confirmed"),
    (1, 1, 4, "上下级", "县委书记与宣传部部长", "中共礼泉县委", "至今", "confirmed"),
    (1, 1, 5, "上下级", "县委书记与政法委书记", "中共礼泉县委", "至今", "confirmed"),
    (1, 1, 6, "上下级", "县委书记与统战部部长", "中共礼泉县委", "至今", "confirmed"),
    (1, 1, 7, "上下级", "县委书记与副县长", "中共礼泉县委", "至今", "confirmed"),
    (1, 1, 8, "上下级", "县委书记与人武部部长", "中共礼泉县委", "至今", "confirmed"),

    # 县长 - 副县长
    (1, 2, 7, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 9, "上下级", "县长与副县长（公安局长）", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 10, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 11, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 12, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 13, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
    (1, 2, 14, "上下级", "县长与副县长", "礼泉县人民政府", "至今", "confirmed"),
]


# ===== 生成函数 =====
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid, post):
    if "县委书记" in post or ("书记" in post and "县委" in post):
        return "255,50,50"
    if "县长" in post or "副县长" in post:
        return "50,100,255"
    if "纪委" in post or "监委" in post or "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    return "100,100,100"

def is_top_leader(post):
    return "县委书记" in post or ("县长" in post and "副" not in post[:2])


def build_sqlite(db_path):
    conn = __import__('sqlite3').connect(str(db_path))
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
    lines.append(f'    <description>礼泉县领导班子关系网络 - {DATE}</description>')
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
        w = "2.0" if rtype in ("搭档", "上下级") else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
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
    staging = Path(__file__).resolve().parent
    DB_PATH = staging / "礼泉县_network.db"
    GEXF_PATH = staging / "礼泉县_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(DB_PATH)
    build_gexf(GEXF_PATH)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {DB_PATH} ({DB_PATH.stat().st_size} bytes) on success")
    print(f"GEXF:   {GEXF_PATH} ({GEXF_PATH.stat().st_size} bytes) on success")
