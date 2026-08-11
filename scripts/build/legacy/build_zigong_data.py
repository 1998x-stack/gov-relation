#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 自贡市 cadre exchange network investigation.
"""

import sqlite3, os

OUT_DIR = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(OUT_DIR, "zigong_network.db")
GEXF_PATH = os.path.join(OUT_DIR, "zigong_network.gexf")

# ── Persons ──────────────────────────────────
persons = [
    ("zigong_zeng_hongyang", "曾洪扬", "男", "汉族", "1972-02", "四川广汉", "上海交通大学(学士)", "1993-03", "1994-07", "自贡市委书记", "中共自贡市委", "百度百科/川观新闻"),
    ("zigong_shi_gang", "石钢", "男", "汉族", "1970-07", "四川渠县", "西南财经大学工商管理", "1999-06", "1991-07", "自贡市市长", "自贡市人民政府", "百度搜索"),
    ("zigong_he_li", "何礼", "男", "汉族", "", "", "", "", "", "离任(原自贡市委书记)", "", "川观新闻2023.2.16"),
    ("zigong_fan_bo", "范波", "男", "汉族", "", "", "", "", "", "山东省任职(原自贡市委书记)", "山东省", "百度搜索"),
    ("zigong_li_gang", "李刚", "男", "汉族", "", "", "", "", "", "历任巴中市委书记等", "", "百度搜索"),
    ("zigong_huang_xuezhi", "黄雪智", "男", "汉族", "", "", "", "", "", "原自贡市副市长(已免)", "自贡市人民政府", "自贡市人大常委会公告"),
    ("zigong_zhu_bin", "朱斌", "男", "汉族", "", "", "", "", "", "自贡市人大常委会副主任", "自贡市人大常委会", "2025年2月公告"),
    ("zigong_tan_bao", "谭豹", "男", "汉族", "", "", "", "", "", "自贡市人大常委会主任", "自贡市人大常委会", "自贡人大网"),
    ("zigong_ying_zhang", "张颖", "男", "汉族", "", "", "", "", "", "自贡市人民政府副市长", "自贡市人民政府", "2025年12月任命"),
    ("zigong_huang_rubei", "黄如贝", "男", "汉族", "", "", "", "", "", "自贡市人民政府秘书长", "自贡市人民政府", "2025年12月任命"),
]

# ── Organizations ─────────────────────────────
orgs = [
    ("org_zigong_city", "自贡市", "地级市", "prefecture", "四川省", "四川"),
    ("org_zigong_cpc", "中共自贡市委", "党委", "prefecture", "四川省委", "自贡"),
    ("org_zigong_gov", "自贡市人民政府", "政府", "prefecture", "自贡市委", "自贡"),
    ("org_zigong_npc", "自贡市人大常委会", "人大", "prefecture", "", "自贡"),
    ("org_leshan_cpc", "中共乐山市委", "党委", "prefecture", "四川省委", "乐山"),
    ("org_sch_housing", "四川省住建厅", "政府厅局", "prov_dept", "四川省政府", "成都"),
    ("org_sch_finance", "四川省财政厅", "政府厅局", "prov_dept", "四川省政府", "成都"),
    ("org_sch_ndrc", "四川省发改委", "政府厅局", "prov_dept", "四川省政府", "成都"),
    ("org_shandong", "山东省", "省份", "province", "中国", "山东"),
    ("org_guangan", "广安市", "地级市", "prefecture", "四川省", "广安"),
    ("org_bazhong", "巴中市", "地级市", "prefecture", "四川省", "巴中"),
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    ("zigong_zeng_hongyang", "org_guangan", "广安市基层/中层任职", "1994", "2015", "", "广安工作起步"),
    ("zigong_zeng_hongyang", "org_leshan_cpc", "中共乐山市委副书记", "2016", "2021", "vice-prefecture", "时任乐山市委副书记"),
    ("zigong_zeng_hongyang", "org_zigong_gov", "自贡市市长", "2021", "2023-02", "prefecture", "乐山→自贡"),
    ("zigong_zeng_hongyang", "org_zigong_cpc", "自贡市委书记", "2023-02", "", "prefecture", "本市晋升"),
    ("zigong_shi_gang", "org_sichuan_housing", "四川省住建厅副厅长", "", "2023-2024", "deputy-prov-dept", "来源"),
    ("zigong_shi_gang", "org_zigong_gov", "自贡市市长", "2023-2024", "", "prefecture", "省厅→地市"),
    ("zigong_he_li", "org_sichuan_finance", "四川省财政厅", "", "", "", ""),
    ("zigong_he_li", "org_zigong_cpc", "自贡市委书记", "2021", "2023-02", "primary", "2023年2月卸任"),
    ("zigong_fan_bo", "org_sichuan_ndrc", "四川省发改委相关职务", "", "2017", "", ""),
    ("zigong_fan_bo", "org_zigong_cpc", "自贡市委书记", "2017", "2021", "major", ""),
    ("zigong_fan_bo", "org_shandong", "山东省任职", "2021", "", "", "跨省调任"),
    ("zigong_li_gang", "org_zigong_cpc", "自贡市委书记", "", "2016", "major", "前任"),
    ("zigong_zhu_bin", "org_zigong_gov", "自贡市人民政府秘书长", "", "2025-02", "deputy", ""),
    ("zigong_zhu_bin", "org_zigong_npc", "自贡市人大常委会副主任", "2025-02", "", "deputy", "当选"),
    ("zigong_huang_xuezhi", "org_zigong_gov", "自贡市人民政府副市长", "", "", "deputy", "已免"),
    ("zigong_ying_zhang", "org_zigong_gov", "自贡市人民政府副市长", "2025-12", "", "deputy", "新任命"),
    ("zigong_huang_rubei", "org_zigong_gov", "自贡市人民政府秘书长", "2025-12", "", "deputy", "新任命"),
    ("zigong_tan_bao", "org_zigong_npc", "自贡市人大常委会主任", "", "", "major", ""),
]

# ── Relationships ─────────────────────────────
relationships = [
    ("zigong_zeng_hongyang", "zigong_he_li", "succession", "曾洪扬接替何礼任自贡市委书记", "org_zigong_cpc", "2023年"),
    ("zigong_he_li", "zigong_fan_bo", "succession", "何礼接替范波任自贡市委书记", "org_zigong_cpc", "约2021年"),
    ("zigong_li_gang", "zigong_fan_bo", "succession", "李刚→范波(自贡市委书记依次)", "org_zigong_cpc", "约2017年"),
    ("zigong_zeng_hongyang", "zigong_shi_gang", "colleague", "曾洪扬(书记)+石钢(市长)搭班子", "org_zigong_cpc", "2023至今"),
    ("zigong_zeng_hongyang", "zigong_zhu_bin", "colleague", "同属自贡市领导系统", "org_zigong_city", ""),
]

# ── SQLite ─────────────────────────────────────────────
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT,
    start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT,
    context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
for o in orgs:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)
for pos in positions:
    cur.execute("INSERT INTO positions (person_id, org_id, position, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
for rel in rels:
    cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", rel)

conn.commit()
conn.close()
print(f"[SQLite] {DB_PATH} — {len(persons)} persons, {len(orgs)} orgs, {len(positions)} positions, {len(rels)} rels")

# ── GEXF ─────────────────────────────────────────────────────────
def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

nodes = ""
for p in persons:
    pid, name = p[0], p[1]
    role = p[9]
    if "书记" in role and "副" not in role:
        color = 'r="200" g="40" b="50"'
        sz = "20.0"
    elif "市长" in role and "副" not in role:
        color = 'r="30" g="100" b="200"'
        sz = "20.0"
    elif "副" in role:
        color = 'r="240" g="140" b="30"'
        sz = "12.0"
    else:
        color = 'r="150" g="150" b="150"'
        sz = "12.0"
    label = f"{esc(name)}\n{esc(role)}"
    nodes += f'  <node id="{esc(pid)}" label="{label}">\n'
    nodes += f'    <viz:color {color}/>\n'
    nodes += f'    <viz:size value="{sz}"/>\n'
    nodes += '  </node>\n'

for o in orgs:
    oid, oname = o[0], o[1]
    nodes += f'  <node id="{esc(oid)}" name="{esc(oname)}">\n'
    nodes += '    <viz:color r="80" g="180" b="80"/>\n'
    nodes += '    <viz:size value="8.0"/>\n'
    nodes += '  </node>\n'

edges = ""
eid = 0
for pos in positions:
    eid += 1
    edges += f'  <edge id="e{eid}" source="{esc(pos[0])}" target="{esc(pos[1])}" type="directed">\n'
    edges += f'    <attvalues><attvalue for="title" value="{esc(pos[2])}"/></attvalues>\n'
    edges += '  </edge>\n'

for rel in rels:
    eid += 1
    edges += f'  <edge id="e{eid}" source="{esc(rel[0])}" target="{esc(rel[1])}" type="undirected">\n'
    edges += f'    <attvalues><attvalue for="context" value="{esc(rel[3])}"/></attvalues>\n'
    edges += '  </edge>\n'

gexf_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      version="1.3">
  <meta>
    <description>自贡市干部交流网络 (2026-07-26)</description>
  </mear>
  <graph mode="static" defaultedgetype="directed">
    <attributes class="edge">
      <attribute id="type" title="edge_type" type="string"/>
      <attribute id="title" title="position_title" type="string"/>
    </attributes>
    <nodes>
{nodes}
    </nodes>
    <edges>
{edges}
    </edges>
  </graph>
</gexf>'''

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf_content)
print(f"[GEXF] {GEXF_PATH} — {len(persons)+len(orgs)} nodes, {eid} edges")

print("\n=== DONE ===")
print(f"Report:  report/20260726-自贡市-干部交流网络分析.md")
print(f"SQLite:  {DB_PATH}")
print(f"GEXF:    {GEXF_PATH}")
