#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 沈阳市于洪区 leadership network."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "database", "yuhong_network.db")
GEXF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "graph", "yuhong_network.gexf")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ===== DATA =====

persons = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
    ("yuhong_wang_hongchao", "王洪超", "男", "汉族", "", "", "硕士研究生", "", "", "区委书记", "中共沈阳市于洪区委员会", "https://www.syyh.gov.cn"),
    ("yuhong_liu_wei", "刘伟", "男", "汉族", "1978年3月", "", "硕士研究生/硕士", "中共党员", "", "区委副书记、代区长、区政府党组书记", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/qz/202112/t20211220_2266180.html"),
    ("yuhong_yao_jiawei", "么家伟", "男", "", "", "", "", "中共党员", "", "区委副书记", "中共沈阳市于洪区委员会", "https://www.syyh.gov.cn/xwzx/jryh/202603/t20260313_4999362.html"),
    ("yuhong_lu_yao", "鲁瑶", "男", "", "", "", "", "中共党员", "", "区委副书记", "中共沈阳市于洪区委员会", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260715_5057101.html"),
    ("yuhong_hao_wei", "郝威", "男", "汉族", "1984年12月", "", "大学/硕士", "中共党员", "", "区委常委、常务副区长、区政府党组副书记", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256864.html"),
    ("yuhong_wang_yongliang", "王永亮", "男", "汉族", "1971年2月", "", "在职大学", "中共党员", "", "区委常委、副区长、区政府党组成员", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3225979.html"),
    ("yuhong_jiao_jian", "矫健", "女", "汉族", "1980年11月", "", "在职大学", "中共党员", "", "区委常委、副区长", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256965.html"),
    ("yuhong_guan_wei", "关伟", "男", "", "", "", "", "中共党员", "", "区委常委、统战部部长", "中共沈阳市于洪区委员会", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260706_5052641.html"),
    ("yuhong_zhou_wenhui", "周文辉", "男", "", "", "", "", "中共党员", "", "区委常委、组织部部长", "中共沈阳市于洪区委员会", "https://www.syyh.gov.cn/xwzx/jryh/202605/t20260527_5031883.html"),
    ("yuhong_ye_guichun", "冶桂春", "女", "回族", "1975年2月", "", "研究生/硕士", "无党派", "", "副区长", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3257135.html"),
    ("yuhong_dong_tieshi", "董铁石", "男", "汉族", "1976年10月", "", "大学/学士", "中共党员", "", "副区长、区政府党组成员", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256994.html"),
    ("yuhong_chen_jianing", "陈嘉宁", "男", "汉族", "1971年9月", "", "在职大学", "中共党员", "", "副区长、区政府党组成员、公安分局局长", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256896.html"),
    ("yuhong_wang_taiwen", "王太文", "男", "汉族", "1976年3月", "", "大学/学士", "中共党员", "", "副区长、区政府党组成员", "于洪区人民政府", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3236389.html"),
    ("yuhong_li_guangjie", "李广杰", "男", "", "", "", "", "中共党员", "", "区人大常委会主任", "于洪区人大常委会", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    ("yuhong_zhang_dianjun", "张殿军", "男", "", "", "", "", "中共党员", "", "区政协主席", "于洪区政协", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    ("yuhong_liu_cheng", "刘成", "男", "", "", "", "", "中共党员", "", "区政协党组书记", "于洪区政协", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    ("yuhong_gao_zhengwei", "高政威", "男", "", "", "", "", "中共党员", "", "原区委书记（已离任）", "（调离）", "https://www.syyh.gov.cn/xwzx/jryh/202512/t20251208_4949972.html"),
    ("yuhong_zhang_long", "张龙", "男", "", "", "", "", "中共党员", "", "原区委常委、常务副区长（已离任）", "（调离）", "https://www.syyh.gov.cn/zwgk/fdzdgknr/zfwj/syzbfwj/202604/t20260403_5010964.html"),
]

organizations = [
    ("org_yuhong_party", "中共沈阳市于洪区委员会", "党委", "县级", "中共沈阳市委", "沈阳市于洪区"),
    ("org_yuhong_gov", "于洪区人民政府", "政府", "县级", "沈阳市人民政府", "沈阳市于洪区"),
    ("org_yuhong_npc", "于洪区人大常委会", "人大", "县级", "沈阳市人大常委会", "沈阳市于洪区"),
    ("org_yuhong_cppcc", "于洪区政协", "政协", "县级", "沈阳市政协", "沈阳市于洪区"),
    ("org_yuhong_police", "沈阳市公安局于洪分局", "政府", "县级", "沈阳市公安局", "沈阳市于洪区"),
]

positions = [
    (1,  "yuhong_wang_hongchao", "org_yuhong_party", "区委书记", "2026-06", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202606/t20260629_5049245.html"),
    (2,  "yuhong_liu_wei", "org_yuhong_gov", "区委副书记、代区长、区政府党组书记", "2026-06", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/qz/202112/t20211220_2266180.html"),
    (3,  "yuhong_yao_jiawei", "org_yuhong_party", "区委副书记", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202603/t20260313_4999362.html"),
    (4,  "yuhong_lu_yao", "org_yuhong_party", "区委副书记", "2026-06", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260715_5057101.html"),
    (5,  "yuhong_hao_wei", "org_yuhong_gov", "区委常委、常务副区长、区政府党组副书记", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256864.html"),
    (6,  "yuhong_wang_yongliang", "org_yuhong_gov", "区委常委、副区长、区政府党组成员", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3225979.html"),
    (7,  "yuhong_jiao_jian", "org_yuhong_gov", "区委常委、副区长", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256965.html"),
    (8,  "yuhong_guan_wei", "org_yuhong_party", "区委常委、统战部部长", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260706_5052641.html"),
    (9,  "yuhong_zhou_wenhui", "org_yuhong_party", "区委常委、组织部部长", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202605/t20260527_5031883.html"),
    (10, "yuhong_ye_guichun", "org_yuhong_gov", "副区长", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3257135.html"),
    (11, "yuhong_dong_tieshi", "org_yuhong_gov", "副区长、区政府党组成员", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256994.html"),
    (12, "yuhong_chen_jianing", "org_yuhong_police", "副区长、区政府党组成员、公安分局局长", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3256896.html"),
    (13, "yuhong_wang_taiwen", "org_yuhong_gov", "副区长、区政府党组成员", "", None, "current", "https://www.syyh.gov.cn/zwgk/fdzdgknr/jgjj/qzfldbzfg/fqz/202206/t20220615_3236389.html"),
    (14, "yuhong_li_guangjie", "org_yuhong_npc", "区人大常委会主任", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    (15, "yuhong_zhang_dianjun", "org_yuhong_cppcc", "区政协主席", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    (16, "yuhong_liu_cheng", "org_yuhong_cppcc", "区政协党组书记", "", None, "current", "https://www.syyh.gov.cn/xwzx/jryh/202607/t20260723_5061278.html"),
    (17, "yuhong_gao_zhengwei", "org_yuhong_party", "原区委书记", "", "2026-06", "former", "https://www.syyh.gov.cn/xwzx/jryh/202512/t20251208_4949972.html"),
    (18, "yuhong_wang_hongchao", "org_yuhong_gov", "原区长", "", "2026-06", "former", "https://www.syyh.gov.cn/xwzx/jryh/202603/t20260313_4999362.html"),
    (19, "yuhong_zhang_long", "org_yuhong_gov", "原区委常委、常务副区长", "", "2026-05", "former", "https://www.syyh.gov.cn/zwgk/fdzdgknr/zfwj/syzbfwj/202604/t20260403_5010964.html"),
]

relationships = [
    (1, "yuhong_wang_hongchao", "yuhong_liu_wei", "上下级", "书记与代区长", "于洪区委区政府", "2026-06~"),
    (2, "yuhong_wang_hongchao", "yuhong_yao_jiawei", "上下级", "书记与副书记", "于洪区委", "2026-03~"),
    (3, "yuhong_wang_hongchao", "yuhong_lu_yao", "上下级", "书记与副书记", "于洪区委", "2026-06~"),
    (4, "yuhong_wang_hongchao", "yuhong_hao_wei", "上下级", "书记与常务副区长", "于洪区党政", "2026-06~"),
    (5, "yuhong_gao_zhengwei", "yuhong_wang_hongchao", "前后任", "前书记现书记（原区长升任）", "于洪区", "2026-06"),
    (6, "yuhong_zhang_long", "yuhong_hao_wei", "前后任", "常务副区长前后任", "于洪区政府", "2026-05~06"),
    (7, "yuhong_wang_hongchao", "yuhong_gao_zhengwei", "搭档", "原书记与区长", "于洪区", "~2026-06"),
]

# ===== BUILD SQLITE =====
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS organizations;

CREATE TABLE persons (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT REFERENCES persons(id),
    org_id TEXT REFERENCES organizations(id),
    title TEXT,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT REFERENCES persons(id),
    person_b TEXT REFERENCES persons(id),
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT
);
""")

for p in persons:
    cur.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

for o in organizations:
    cur.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)

for pos in positions:
    cur.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)", pos)

for r in relationships:
    cur.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?,?)", r)

conn.commit()

# Stats
p_count = cur.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
o_count = cur.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
pos_count = cur.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
r_count = cur.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
print(f"SQLite DB created: {p_count} persons, {o_count} orgs, {pos_count} positions, {r_count} relationships")
conn.close()

# ===== BUILD GEXF =====

def color(r, g, b):
    return f'viz:color r="{r}" g="{g}" b="{b}" a="1.0"'

# Person colors by role
role_colors = {
    "书记": (255, 50, 50),
    "区长": (50, 100, 255),
    "副书记": (200, 100, 50),
    "常委": (180, 130, 70),
    "副区长": (100, 130, 200),
    "人大": (0, 180, 180),
    "政协": (180, 180, 50),
    "其他": (100, 100, 100),
}

person_colors = {
    "yuhong_wang_hongchao": role_colors["书记"],
    "yuhong_liu_wei": role_colors["区长"],
    "yuhong_yao_jiawei": role_colors["副书记"],
    "yuhong_lu_yao": role_colors["副书记"],
    "yuhong_hao_wei": role_colors["常委"],
    "yuhong_wang_yongliang": role_colors["常委"],
    "yuhong_jiao_jian": role_colors["常委"],
    "yuhong_guan_wei": role_colors["常委"],
    "yuhong_zhou_wenhui": role_colors["常委"],
    "yuhong_ye_guichun": role_colors["副区长"],
    "yuhong_dong_tieshi": role_colors["副区长"],
    "yuhong_chen_jianing": role_colors["副区长"],
    "yuhong_wang_taiwen": role_colors["副区长"],
    "yuhong_li_guangjie": role_colors["人大"],
    "yuhong_zhang_dianjun": role_colors["政协"],
    "yuhong_liu_cheng": role_colors["政协"],
    "yuhong_gao_zhengwei": role_colors["其他"],
    "yuhong_zhang_long": role_colors["其他"],
}

person_sizes = {
    "yuhong_wang_hongchao": 20.0,
    "yuhong_liu_wei": 18.0,
    "yuhong_yao_jiawei": 14.0,
    "yuhong_lu_yao": 14.0,
    "yuhong_hao_wei": 14.0,
}

org_colors = {
    "org_yuhong_party": (220, 50, 50),
    "org_yuhong_gov": (50, 100, 220),
    "org_yuhong_npc": (0, 200, 200),
    "org_yuhong_cppcc": (200, 200, 50),
    "org_yuhong_police": (50, 50, 200),
}

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <meta><creator>gov-relation investigator</creator><description>沈阳市于洪区领导班子工作关系网络</description></meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"><default>person</default></attribute>')
lines.append('      <attribute id="role" title="Role" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="ethnicity" title="Ethnicity" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('    </attributes>')

# Nodes — persons
lines.append('    <nodes>')
for p in persons:
    pid, name, gender, ethnicity, birth, bp, edu, pj, ws, post, org, src = p
    c = person_colors.get(pid, (100, 100, 100))
    sz = person_sizes.get(pid, 12.0)
    lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="role" value="{esc(post)}"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(birth)}"/>')
    lines.append(f'          <attvalue for="ethnicity" value="{esc(ethnicity)}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(src)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <{color(*c)}/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# Nodes — organizations
for oid, oname, otype, olev, opar, oloc in organizations:
    oc = org_colors.get(oid, (150, 150, 150))
    lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="organization"/>')
    lines.append(f'          <attvalue for="role" value="{esc(otype)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <{color(*oc)}/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person→Org (worked_at)
for pos in positions:
    eid += 1
    pid, p_person, p_org, title, start, end, rank, note = pos
    lines.append(f'      <edge id="{eid}" source="{esc(p_person)}" target="{esc(p_org)}" weight="1.0" label="{esc(title)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(title)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

# Person↔Person (relationships)
for r in relationships:
    eid += 1
    rid, pa, pb, rtype, ctx, oorg, oper = r
    w = 2.0 if rtype in ("前后任", "搭档") else 1.5
    lines.append(f'      <edge id="{eid}" source="{esc(pa)}" target="{esc(pb)}" weight="{w}" label="{esc(rtype)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="context" value="{esc(ctx)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF created: {len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges")
print("Done!")
