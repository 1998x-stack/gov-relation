#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 湘潭市 leadership network."""

import sqlite3
import os
from datetime import date

DB_DIR = "data/database"
GRAPH_DIR = "data/graph"
DB_PATH = os.path.join(DB_DIR, "xiangtan_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, "xiangtan_network.gexf")
TODAY = "2026-07-14"

os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────

persons = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # A. City-level (湘潭市)
    ("xiangtan_hu_hebo", "胡贺波", "男", "汉族", "1972-05", "湖南华容",
     "湖南财经学院经济学硕士/湖南大学管理学博士/美国伊利诺伊大学芝加哥分校MBA", "中共党员", "1994-07",
     "市委书记（兼省韶山管理局党委书记）", "中共湘潭市委",
     "https://zh.wikipedia.org/wiki/胡贺波"),
    ("xiangtan_li_yongliang", "李永亮", "男", "汉族", "1975-09", "四川简阳",
     "西安公路交通大学（长安大学）工学学士", "中共党员", "1999-07",
     "市委副书记、市长", "湘潭市人民政府",
     "https://zh.wikipedia.org/wiki/李永亮"),
    ("xiangtan_liu_zhiren", "刘志仁", "男", "汉族", "1964-09", "湖南新邵",
     "湖南省水利水电学校（长沙理工大学）/中央党校/中南工业大学", "中共党员", "1986",
     "前任市委书记（已被查/开除党籍）", "湖南省人大环资委（原）",
     "https://zh.wikipedia.org/wiki/刘志仁_(1964年)"),

    # B. 雨湖区
    ("yuhu_liu_junhui", "柳军辉", "男", "汉族", "1972-12", "湖南湘乡", "", "", "",
     "区长", "雨湖区人民政府",
     "https://zh.wikipedia.org/wiki/雨湖区"),
    ("yuhu_duan_weichang", "段伟长", "男", "汉族", "1970-01", "湖南冷水江", "", "", "",
     "区委书记", "中共雨湖区委员会",
     "https://zh.wikipedia.org/wiki/雨湖区"),

    # C. 岳塘区
    ("yuetang_zhou_shangling", "周赏玲", "女", "汉族", "1978-01", "湖南湘乡", "", "", "",
     "区长", "岳塘区人民政府",
     "https://zh.wikipedia.org/wiki/岳塘区"),
    ("yuetang_zeng_zhijun", "曾志君", "男", "汉族", "1971-01", "湖南邵东", "", "", "",
     "区委书记", "中共岳塘区委员会",
     "https://zh.wikipedia.org/wiki/岳塘区"),

    # D. 湘潭县
    ("xiangtanxian_wang_li", "王利", "男", "汉族", "1982-12", "湖南湘乡", "", "", "",
     "县长", "湘潭县人民政府",
     "https://zh.wikipedia.org/wiki/湘潭县"),
    ("xiangtanxian_huang_jinsong", "黄劲松", "男", "汉族", "1971-02", "湖南湘乡", "", "", "",
     "县委书记", "中共湘潭县委员会",
     "https://zh.wikipedia.org/wiki/湘潭县"),

    # E. 湘乡市
    ("xiangxiang_guo_yong", "郭勇", "男", "汉族", "1974-06", "湖南沅江", "", "", "",
     "市长", "湘乡市人民政府",
     "https://zh.wikipedia.org/wiki/湘乡市"),
    ("xiangxiang_zhao_xinwen", "赵新文", "男", "汉族", "1968-12", "湖南湘潭", "", "", "",
     "市委书记", "中共湘乡市委员会",
     "https://zh.wikipedia.org/wiki/湘乡市"),

    # F. 韶山市
    ("shaoshan_yu_zhijun", "喻志军", "男", "汉族", "1977-10", "湖南宁乡", "", "", "",
     "市委书记", "中共韶山市委员会",
     "https://zh.wikipedia.org/wiki/韶山市"),
    ("shaoshan_deng_wangjun", "邓望军", "男", "汉族", "1974-12", "湖南湘乡", "", "", "",
     "市长", "韶山市人民政府",
     "https://zh.wikipedia.org/wiki/韶山市"),

    # G. Key city-level deputies
    ("xiangtan_liu_xinhua", "刘新华", "男", "汉族", "1973-10", "", "研究生/硕士", "", "",
     "市委常委、常务副市长", "湘潭市人民政府",
     "https://www.xiangtan.gov.cn/109/110/27252/index.htm"),
    ("xiangtan_zhou_yanxi", "周艳希", "女", "汉族", "1980-01", "", "研究生/硕士", "", "",
     "副市长（教育、人社、卫健）", "湘潭市人民政府",
     "https://www.xiangtan.gov.cn/109/110/index.htm"),
    ("xiangtan_chen_rui", "陈睿", "男", "汉族", "1973-10", "", "博士", "", "",
     "副市长（公安、司法、信访）", "湘潭市人民政府",
     "https://www.xiangtan.gov.cn/109/110/index.htm"),
    ("xiangtan_yang_xiaojun", "杨晓军", "男", "汉族", "1970-02", "", "在职工学", "", "",
     "副市长（商务、文旅）", "湘潭市人民政府",
     "https://www.xiangtan.gov.cn/109/110/index.htm"),
]

organizations = [
    # id, name, type, level, parent, location
    ("org_xiangtan_city", "湘潭市", "地级市", "地厅级", "湖南省", "湖南湘潭"),
    ("org_xiangtan_party", "中共湘潭市委", "党委", "地厅级", "org_xiangtan_city", "湖南湘潭"),
    ("org_xiangtan_gov", "湘潭市人民政府", "政府", "地厅级", "org_xiangtan_city", "湖南湘潭"),
    ("org_yuhu", "雨湖区", "市辖区", "县处级", "org_xiangtan_city", "湖南湘潭雨湖区"),
    ("org_yuhu_party", "中共雨湖区委员会", "党委", "县处级", "org_yuhu", "湖南湘潭雨湖区"),
    ("org_yuhu_gov", "雨湖区人民政府", "政府", "县处级", "org_yuhu", "湖南湘潭雨湖区"),
    ("org_yuetang", "岳塘区", "市辖区", "县处级", "org_xiangtan_city", "湖南湘潭岳塘区"),
    ("org_yuetang_party", "中共岳塘区委员会", "党委", "县处级", "org_yuetang", "湖南湘潭岳塘区"),
    ("org_yuetang_gov", "岳塘区人民政府", "政府", "县处级", "org_yuetang", "湖南湘潭岳塘区"),
    ("org_xiangtanxian", "湘潭县", "县", "县处级", "org_xiangtan_city", "湖南湘潭湘潭县"),
    ("org_xiangtanxian_party", "中共湘潭县委员会", "党委", "县处级", "org_xiangtanxian", "湖南湘潭湘潭县"),
    ("org_xiangtanxian_gov", "湘潭县人民政府", "政府", "县处级", "org_xiangtanxian", "湖南湘潭湘潭县"),
    ("org_xiangxiang", "湘乡市", "县级市", "县处级", "org_xiangtan_city", "湖南湘潭湘乡市"),
    ("org_xiangxiang_party", "中共湘乡市委员会", "党委", "县处级", "org_xiangxiang", "湖南湘潭湘乡市"),
    ("org_xiangxiang_gov", "湘乡市人民政府", "政府", "县处级", "org_xiangxiang", "湖南湘潭湘乡市"),
    ("org_shaoshan", "韶山市", "县级市", "县处级", "org_xiangtan_city", "湖南湘潭韶山市"),
    ("org_shaoshan_party", "中共韶山市委员会", "党委", "县处级", "org_shaoshan", "湖南湘潭韶山市"),
    ("org_shaoshan_gov", "韶山市人民政府", "政府", "县处级", "org_shaoshan", "湖南湘潭韶山市"),
    ("org_shaoshan_admin", "湖南省韶山管理局", "事业单位", "省管", "org_xiangtan_city", "湖南湘潭韶山市"),
]

positions = [
    # id, person_id, org_id, title, start, end, rank, note
    # 胡贺波
    ("pos_huhebo_1", "xiangtan_hu_hebo", "org_xiangtan_party", "市委书记", "2024-08", "", "正厅级", ""),
    ("pos_huhebo_2", "xiangtan_hu_hebo", "org_xiangtan_gov", "市长", "2021-07", "2024-10", "正厅级", "此前为代市长"),
    ("pos_huhebo_3", "xiangtan_hu_hebo", "org_shaoshan_admin", "党委书记（兼）", "2024-08", "", "正厅级", "兼任"),
    ("pos_huhebo_4", "xiangtan_hu_hebo", "org_xiangtan_gov", "代市长", "2021-07", "2022-01", "正厅级", ""),
    # 刘志仁（前任）
    ("pos_liuzhiren_1", "xiangtan_liu_zhiren", "org_xiangtan_party", "市委书记", "2022-03", "2024-08", "正厅级", ""),
    # 李永亮
    ("pos_liyongliang_1", "xiangtan_li_yongliang", "org_xiangtan_gov", "市长", "2024-10", "", "正厅级", "代理后转正"),
    ("pos_liyongliang_2", "xiangtan_li_yongliang", "org_xiangtan_party", "市委副书记", "2024-10", "", "正厅级", ""),
    # 雨湖区
    ("pos_yuhu_duan", "yuhu_duan_weichang", "org_yuhu_party", "区委书记", "2022-01", "", "县处级正职", ""),
    ("pos_yuhu_liu", "yuhu_liu_junhui", "org_yuhu_gov", "区长", "2021-10", "", "县处级正职", ""),
    # 岳塘区
    ("pos_yuetang_zeng", "yuetang_zeng_zhijun", "org_yuetang_party", "区委书记", "2021-07", "", "县处级正职", ""),
    ("pos_yuetang_zhou", "yuetang_zhou_shangling", "org_yuetang_gov", "区长", "2021-10", "", "县处级正职", ""),
    # 湘潭县
    ("pos_xtx_huang", "xiangtanxian_huang_jinsong", "org_xiangtanxian_party", "县委书记", "2021-07", "", "县处级正职", ""),
    ("pos_xtx_wang", "xiangtanxian_wang_li", "org_xiangtanxian_gov", "县长", "2022-04", "", "县处级正职", ""),
    # 湘乡市
    ("pos_xx_zhao", "xiangxiang_zhao_xinwen", "org_xiangxiang_party", "市委书记", "2021-05", "", "县处级正职", ""),
    ("pos_xx_guo", "xiangxiang_guo_yong", "org_xiangxiang_gov", "市长", "2021-10", "", "县处级正职", ""),
    # 韶山市
    ("pos_ss_yu", "shaoshan_yu_zhijun", "org_shaoshan_party", "市委书记", "2026-06", "", "县处级正职", ""),
    ("pos_ss_deng", "shaoshan_deng_wangjun", "org_shaoshan_gov", "市长", "2021-10", "", "县处级正职", ""),
    # 副市长
    ("pos_liuxinhua", "xiangtan_liu_xinhua", "org_xiangtan_gov", "常务副市长", "", "", "副厅级", ""),
    ("pos_zhouyanxi", "xiangtan_zhou_yanxi", "org_xiangtan_gov", "副市长", "", "", "副厅级", ""),
    ("pos_chenrui", "xiangtan_chen_rui", "org_xiangtan_gov", "副市长", "", "", "副厅级", ""),
    ("pos_yangxiaojun", "xiangtan_yang_xiaojun", "org_xiangtan_gov", "副市长", "", "", "副厅级", ""),
]

relationships = [
    # id, person_a, person_b, type, context, overlap_org, overlap_period
    # 胡贺波 → 李永亮（前后任市长）
    ("rel_hu_li_1", "xiangtan_hu_hebo", "xiangtan_li_yongliang", "succession",
     "胡贺波任市长期间，李永亮接替其出任代市长/市长", "湘潭市人民政府", "2024-10"),
    # 刘志仁 → 胡贺波（前后任书记）
    ("rel_liu_hu_1", "xiangtan_liu_zhiren", "xiangtan_hu_hebo", "succession",
     "刘志仁卸任市委书记，胡贺波接任", "中共湘潭市委", "2024-08"),
    # 杨晓军 - 同时任韶山书记和湘潭副市长（交集）
    ("rel_yang_shaoshan", "xiangtan_yang_xiaojun", "shaoshan_yu_zhijun", "same_region",
     "杨晓军曾任韶山市委书记（前任），喻志军现任", "韶山市", "~2024~2026"),
]

# ── Build DB ─────────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
  DROP TABLE IF EXISTS relationships;
  DROP TABLE IF EXISTS positions;
  DROP TABLE IF EXISTS organizations;
  DROP TABLE IF EXISTS persons;

  CREATE TABLE persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
  );
  CREATE TABLE organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
  );
  CREATE TABLE positions (
    id TEXT PRIMARY KEY, person_id TEXT, org_id TEXT, title TEXT,
    start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
  );
  CREATE TABLE relationships (
    id TEXT PRIMARY KEY, person_a TEXT, person_b TEXT, type TEXT,
    context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
  );
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)", pos)
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)", r)

conn.commit()

# Stats
stats = {}
stats["persons"] = c.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
stats["orgs"] = c.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
stats["positions"] = c.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
stats["rels"] = c.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]

conn.close()
print(f"DB: {DB_PATH}")
print(f"  Persons: {stats['persons']}, Orgs: {stats['orgs']}, Positions: {stats['positions']}, Relationships: {stats['rels']}")

# ── Build GEXF ────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

# Role colors
ROLE_COLORS = {
    "party": "#E03C31",   # red - party secretary
    "gov": "#2563EB",     # blue - government leader
    "discipline": "#F59E0B",  # orange - discipline
    "other": "#6B7280",   # grey - other persons
    "org": "#374151",     # dark grey - organizations
}

def person_role(person_id):
    if any(x in person_id for x in ["_hu_hebo", "_liu_zhiren", "_duan_weichang", "_zeng_zhijun",
                                      "_huang_jinsong", "_zhao_xinwen", "_yu_zhijun"]):
        return "party"
    if "_yang_xiaojun" in person_id:
        return "party"
    return "gov"

# Build the GEXF manually (string formatting avoids ElementTree namespace issues)
lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    pid, name, gender, ethnicity, birth, birthplace = p[0], p[1], p[2], p[3], p[4], p[5]
    role = person_role(pid)
    color = ROLE_COLORS[role]
    size = 20.0 if role == "party" else 12.0
    label = f"{name}\\n{birth}" if birth else name
    lines.append(f'      <node id="{esc(pid)}" label="{esc(label)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'        <viz:shape value="disc"/>')
    lines.append(f'      </node>')
for o in organizations:
    oid, oname = o[0], o[1]
    lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="org"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(ROLE_COLORS["org"][1:3],16)}" g="{int(ROLE_COLORS["org"][3:5],16)}" b="{int(ROLE_COLORS["org"][5:7],16)}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'        <viz:shape value="square"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
# Person -> Organization edges
pos_edges = [
    # (person_id, org_id, title)
    ("xiangtan_hu_hebo", "org_xiangtan_party", "市委书记"),
    ("xiangtan_hu_hebo", "org_xiangtan_gov", "市长（2021-2024）"),
    ("xiangtan_hu_hebo", "org_shaoshan_admin", "党委书记（兼）"),
    ("xiangtan_li_yongliang", "org_xiangtan_gov", "市长"),
    ("xiangtan_li_yongliang", "org_xiangtan_party", "市委副书记"),
    ("xiangtan_liu_zhiren", "org_xiangtan_party", "市委书记（前任）"),
    ("yuhu_duan_weichang", "org_yuhu_party", "区委书记"),
    ("yuhu_liu_junhui", "org_yuhu_gov", "区长"),
    ("yuetang_zeng_zhijun", "org_yuetang_party", "区委书记"),
    ("yuetang_zhou_shangling", "org_yuetang_gov", "区长"),
    ("xiangtanxian_huang_jinsong", "org_xiangtanxian_party", "县委书记"),
    ("xiangtanxian_wang_li", "org_xiangtanxian_gov", "县长"),
    ("xiangxiang_zhao_xinwen", "org_xiangxiang_party", "市委书记"),
    ("xiangxiang_guo_yong", "org_xiangxiang_gov", "市长"),
    ("shaoshan_yu_zhijun", "org_shaoshan_party", "市委书记"),
    ("shaoshan_deng_wangjun", "org_shaoshan_gov", "市长"),
    ("xiangtan_liu_xinhua", "org_xiangtan_gov", "常务副市长"),
    ("xiangtan_zhou_yanxi", "org_xiangtan_gov", "副市长"),
    ("xiangtan_chen_rui", "org_xiangtan_gov", "副市长"),
    ("xiangtan_yang_xiaojun", "org_xiangtan_gov", "副市长"),
]
for pid, oid, title in pos_edges:
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="{esc(oid)}" label="{esc(title)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(title)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="156" g="163" b="175"/>')
    lines.append(f'        <viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')

# Person -> Person relationship edges
for r in relationships:
    eid += 1
    src, tgt = r[1], r[2]
    rtype = r[3]
    ctx = r[4]
    if rtype == "succession":
        color = "#C9A94E"
        thick = 2.0
    else:
        color = "#93C5FD"
        thick = 1.5
    lines.append(f'      <edge id="e{eid}" source="{esc(src)}" target="{esc(tgt)}" label="{esc(ctx)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(rtype)}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(ctx)}"/>')
    lines.append(f'        </attvalues>')
    r_, g_, b_ = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    lines.append(f'        <viz:color r="{r_}" g="{g_}" b="{b_}"/>')
    lines.append(f'        <viz:thickness value="{thick}"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons) + len(organizations)}")
print(f"  Edges: {eid}")
print("Done.")
