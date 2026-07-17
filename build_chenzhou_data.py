#!/usr/bin/env python3
"""
郴州市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件
"""
import sqlite3
import os
from xml.sax.saxutils import escape

DB_PATH = "data/database/chenzhou.db"
GEXF_PATH = "data/graph/chenzhou.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

# ===== 数据定义 =====

orgs = [
    ("chenzhou_city", "郴州市", "地级市", "中共郴州市委/市政府", "湖南省"),
    ("chenzhou_beihu", "北湖区", "市辖区", "北湖区委/区政府", "北湖区"),
    ("chenzhou_suxian", "苏仙区", "市辖区", "苏仙区委/区政府", "苏仙区"),
    ("chenzhou_guiyang", "桂阳县", "县", "桂阳县委/县政府", "桂阳县"),
    ("chenzhou_yizhang", "宜章县", "县", "宜章县委/县政府", "宜章县"),
    ("chenzhou_yongxing", "永兴县", "县", "永兴县委/县政府", "永兴县"),
    ("chenzhou_jiahe", "嘉禾县", "县", "嘉禾县委/县政府", "嘉禾县"),
    ("chenzhou_linwu", "临武县", "县", "临武县委/县政府", "临武县"),
    ("chenzhou_rucheng", "汝城县", "县", "汝城县委/县政府", "汝城县"),
    ("chenzhou_guidong", "桂东县", "县", "桂东县委/县政府", "桂东县"),
    ("chenzhou_anren", "安仁县", "县", "安仁县委/县政府", "安仁县"),
    ("chenzhou_zixing", "资兴市", "县级市", "资兴市委/市政府", "资兴市"),
]

persons = [
    # 市本级
    ("chenzhou_kan_baoyong", "阚保勇", "男", "汉族", "1973-06", "山东省成武县",
     "郴州市委书记", "chenzhou_city", "https://zh.wikipedia.org/wiki/阚保勇"),
    ("chenzhou_bai_yunfeng", "白云峰", "男", "汉族", "1981-09", "天津市",
     "郴州市市长", "chenzhou_city", "https://zh.wikipedia.org/wiki/郴州市"),
    ("chenzhou_jiang_bo", "江波", "男", "汉族", "1966-11", "湖南省醴陵市",
     "郴州市人大主任", "chenzhou_city", "https://zh.wikipedia.org/wiki/郴州市"),
    ("chenzhou_chen_yuewen", "陈跃文", "男", "汉族", "1968-07", "湖南省益阳市",
     "郴州市政协主席", "chenzhou_city", "https://zh.wikipedia.org/wiki/郴州市"),
    # 桂阳县
    ("chenzhou_wu_chuhua", "巫初华", "男", "汉族", "1973-12", "江西省宜丰县",
     "桂阳县委书记", "chenzhou_guiyang", "https://zh.wikipedia.org/wiki/桂阳县"),
    ("chenzhou_li_zhiqiang", "李志强", "男", "汉族", "1980-06", "湖南省武冈市",
     "桂阳县县长", "chenzhou_guiyang", "https://zh.wikipedia.org/wiki/桂阳县"),
    ("chenzhou_liu_jiuzheng", "刘久正", "男", "汉族", "1968-04", "湖南省蓝山县",
     "桂阳县人大主任", "chenzhou_guiyang", "https://zh.wikipedia.org/wiki/桂阳县"),
    ("chenzhou_xiao_hui", "肖晖", "男", "汉族", "1968-07", "湖南省桂阳县",
     "桂阳县政协主席", "chenzhou_guiyang", "https://zh.wikipedia.org/wiki/桂阳县"),
    # 资兴市
    ("chenzhou_yang_licheng", "杨理诚", "男", "汉族", "1976", "湖南省湘阴县",
     "资兴市委书记", "chenzhou_zixing", "https://zh.wikipedia.org/wiki/资兴市"),
    ("chenzhou_chen_zhanhua", "陈占华", "男", "汉族", "1973-02", "湖南省永兴县",
     "资兴市市长", "chenzhou_zixing", "https://zh.wikipedia.org/wiki/资兴市"),
    ("chenzhou_wang_renqing", "王仁庆", "男", "汉族", "1968-11", "湖南省安仁县",
     "资兴市人大主任", "chenzhou_zixing", "https://zh.wikipedia.org/wiki/资兴市"),
    ("chenzhou_chen_yizhi", "陈一之", "男", "汉族", "", "",
     "资兴市政协主席", "chenzhou_zixing", "https://zh.wikipedia.org/wiki/资兴市"),
    # 宜章县
    ("chenzhou_zhang_runhuai", "张润槐", "男", "侗族", "1976-03", "湖南省新晃侗族自治县",
     "宜章县委书记", "chenzhou_yizhang", "https://zh.wikipedia.org/wiki/宜章县"),
    ("chenzhou_deng_shenghua", "邓生华", "男", "汉族", "1981-03", "湖南省桂阳县",
     "宜章县县长", "chenzhou_yizhang", "https://zh.wikipedia.org/wiki/宜章县"),
    ("chenzhou_li_xiufang", "李秀芳", "男", "汉族", "1970-05", "湖南省宜章县",
     "宜章县人大主任", "chenzhou_yizhang", "https://zh.wikipedia.org/wiki/宜章县"),
    ("chenzhou_zhou_xiaowen", "周小文", "男", "汉族", "", "",
     "宜章县政协主席", "chenzhou_yizhang", "https://zh.wikipedia.org/wiki/宜章县"),
    # 永兴县
    ("chenzhou_liu_zhaohui", "刘朝晖", "男", "汉族", "1974-02", "湖南省攸县",
     "永兴县委书记", "chenzhou_yongxing", "https://zh.wikipedia.org/wiki/永兴县"),
    ("chenzhou_bin_xinhua", "宾心华", "男", "汉族", "1981-06", "湖南省衡山县",
     "永兴县县长", "chenzhou_yongxing", "https://zh.wikipedia.org/wiki/永兴县"),
    ("chenzhou_wang_mei", "王梅", "女", "汉族", "1969-09", "安徽省凤台县",
     "永兴县人大主任", "chenzhou_yongxing", "https://zh.wikipedia.org/wiki/永兴县"),
    ("chenzhou_li_linghua", "李玲华", "女", "汉族", "1969-08", "湖南省耒阳市",
     "永兴县政协主席", "chenzhou_yongxing", "https://zh.wikipedia.org/wiki/永兴县"),
    # 前任
    ("chenzhou_wu_jüpei", "吴巨培", "男", "汉族", "1975-11", "湖南省涟源市",
     "郴州市委原书记（另有任用）", "chenzhou_city", "https://zh.wikipedia.org/wiki/吴巨培"),
    ("chenzhou_liu_zhiren", "刘志仁", "男", "汉族", "1964-09", "湖南省新邵县",
     "郴州市委原书记（已被查）", "chenzhou_city", "https://zh.wikipedia.org/wiki/刘志仁_(1964年)"),
]

# 职位关系 - person → org (worked_at)
positions = [
    ("chenzhou_kan_baoyong", "chenzhou_city", "市委书记", "2026-05", None, "confirmed"),
    ("chenzhou_bai_yunfeng", "chenzhou_city", "市长", "2026-06", None, "confirmed"),
    ("chenzhou_jiang_bo", "chenzhou_city", "人大主任", "2022-01", None, "confirmed"),
    ("chenzhou_chen_yuewen", "chenzhou_city", "政协主席", "2022-01", None, "confirmed"),
    ("chenzhou_wu_chuhua", "chenzhou_guiyang", "县委书记", "2021-07", None, "confirmed"),
    ("chenzhou_li_zhiqiang", "chenzhou_guiyang", "县长", "2021-04", None, "confirmed"),
    ("chenzhou_yang_licheng", "chenzhou_zixing", "市委书记", "2021-07", None, "confirmed"),
    ("chenzhou_chen_zhanhua", "chenzhou_zixing", "市长", "2021-07", None, "confirmed"),
    ("chenzhou_zhang_runhuai", "chenzhou_yizhang", "县委书记", "2021-05", None, "confirmed"),
    ("chenzhou_deng_shenghua", "chenzhou_yizhang", "县长", "2021-07", None, "confirmed"),
    ("chenzhou_liu_zhaohui", "chenzhou_yongxing", "县委书记", "2021-05", None, "confirmed"),
    ("chenzhou_bin_xinhua", "chenzhou_yongxing", "县长", "2021-06", None, "confirmed"),
    ("chenzhou_wu_jüpei", "chenzhou_city", "市委书记", "2022-03", "2026-05", "confirmed"),
]

# 人物间关系
relationships = [
    ("chenzhou_kan_baoyong", "chenzhou_bai_yunfeng", "工作搭档", "chenzhou_city", "2026-06至今"),
    ("chenzhou_kan_baoyong", "chenzhou_wu_jüpei", "前任继任", "chenzhou_city", "2026-05"),
    ("chenzhou_wu_jüpei", "chenzhou_liu_zhiren", "前任继任", "chenzhou_city", "2022-03"),
]

# 同届/同地关系
same_county_relations = [
    ("chenzhou_wu_chuhua", "chenzhou_li_zhiqiang", "党政搭档", "桂阳县"),
    ("chenzhou_yang_licheng", "chenzhou_chen_zhanhua", "党政搭档", "资兴市"),
    ("chenzhou_zhang_runhuai", "chenzhou_deng_shenghua", "党政搭档", "宜章县"),
    ("chenzhou_liu_zhaohui", "chenzhou_bin_xinhua", "党政搭档", "永兴县"),
]

# ===== 构建SQLite数据库 =====

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 建表
c.executescript("""
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT, start TEXT, end TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for org in orgs:
    c.execute("INSERT OR IGNORE INTO organizations (id, name, type, parent, location) VALUES (?,?,?,?,?)", org)

for p in persons:
    c.execute("INSERT OR IGNORE INTO persons (id, name, gender, ethnicity, birth, birthplace, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?)", p)

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, note) VALUES (?,?,?,?,?,?)", pos)

for rel in relationships:
    # Pad to 6 fields: person_a, person_b, type, context, overlap_org, overlap_period
    while len(rel) < 6:
        rel = rel + ("",)
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", rel)

for rel in same_county_relations:
    if len(rel) == 4:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org) VALUES (?,?,?,?,?)", rel + ("",))
    else:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org) VALUES (?,?,?,?,?)", rel)

conn.commit()

# 统计
print(f"✅ 数据库写入完成: {DB_PATH}")
print(f"   - {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]} 人")
print(f"   - {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]} 组织")
print(f"   - {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]} 任职")
print(f"   - {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]} 关系")

conn.close()

# ===== 构建GEXF =====

def xml_escape(s):
    return escape(str(s))

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('  <meta>')
gexf_parts.append('    <creator>chenzhou_network_builder</creator>')
gexf_parts.append('    <description>郴州市领导班子工作关系网络</description>')
gexf_parts.append('  </meta>')
gexf_parts.append('  <graph mode="static" defaultedgetype="directed">')

# 节点
gexf_parts.append('    <nodes>')
for pid, name, gender, ethnicity, birth, birthplace, current_post, current_org, source in persons:
    # 角色分类
    if "书记" in current_post:
        color = 'r="200" g="50" b="50"'  # 红色 - 党委
        size = 20.0
    elif "市长" in current_post or "县长" in current_post or "区长" in current_post:
        color = 'r="50" g="100" b="200"'  # 蓝色 - 政府
        size = 15.0
    elif "主任" in current_post:
        color = 'r="200" g="150" b="50"'  # 橙色 - 人大
        size = 12.0
    elif "主席" in current_post:
        color = 'r="100" g="180" b="100"'  # 绿色 - 政协
        size = 12.0
    else:
        color = 'r="150" g="150" b="150"'  # 灰色
        size = 10.0

    gexf_parts.append(f'      <node id="{pid}" label="{xml_escape(name)}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="role" value="{xml_escape(current_post)}"/>')
    gexf_parts.append(f'          <attvalue for="birth" value="{xml_escape(birth)}"/>')
    gexf_parts.append(f'          <attvalue for="birthplace" value="{xml_escape(birthplace)}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color {color}/>')
    gexf_parts.append(f'        <viz:size value="{size}"/>')
    gexf_parts.append(f'      </node>')

# 组织节点
for oid, oname, otype, parent, location in orgs:
    gexf_parts.append(f'      <node id="{oid}" label="{xml_escape(oname)}">')
    gexf_parts.append(f'        <viz:color r="180" g="180" b="180"/>')
    gexf_parts.append(f'        <viz:size value="8.0"/>')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="type" value="organization"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'      </node>')

gexf_parts.append('    </nodes>')

# 边
gexf_parts.append('    <edges>')
edge_id = 0

# worked_at 边 - 人物→组织
for pid, oid, title, start, end, note in positions:
    gexf_parts.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" label="{xml_escape(title)}" type="directed">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="type" value="worked_at"/>')
    gexf_parts.append(f'          <attvalue for="title" value="{xml_escape(title)}"/>')
    gexf_parts.append(f'          <attvalue for="start" value="{xml_escape(start or "")}"/>')
    gexf_parts.append(f'          <attvalue for="end" value="{xml_escape(end or "")}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color r="180" g="180" b="180"/>')
    gexf_parts.append(f'        <viz:thickness value="1.0"/>')
    gexf_parts.append(f'      </edge>')
    edge_id += 1

# relationship 边 - 人物↔人物
all_rels = relationships + same_county_relations
for rel in all_rels:
    pa, pb, rtype, context, *rest = rel
    if len(rest) >= 1:
        overlap_org = rest[0]
    else:
        overlap_org = ""
    if "搭档" in rtype:
        thick = 3.0
        color = 'r="200" g="180" b="50"'
    elif "前任" in rtype or "继任" in rtype:
        thick = 2.0
        color = 'r="100" g="100" b="200"'
    else:
        thick = 1.5
        color = 'r="150" g="150" b="150"'

    gexf_parts.append(f'      <edge id="e{edge_id}" source="{pa}" target="{pb}" label="{xml_escape(rtype)}" type="undirected">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="type" value="relationship"/>')
    gexf_parts.append(f'          <attvalue for="relation_type" value="{xml_escape(rtype)}"/>')
    gexf_parts.append(f'          <attvalue for="context" value="{xml_escape(context)}"/>')
    gexf_parts.append(f'          <attvalue for="overlap_org" value="{xml_escape(overlap_org)}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color {color}/>')
    gexf_parts.append(f'        <viz:thickness value="{thick}"/>')
    gexf_parts.append(f'      </edge>')
    edge_id += 1

gexf_parts.append('    </edges>')

# 属性定义
gexf_parts.append('    <attributes class="node">')
gexf_parts.append('      <attribute id="role" title="Role" type="string"/>')
gexf_parts.append('      <attribute id="birth" title="Birth" type="string"/>')
gexf_parts.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
gexf_parts.append('      <attribute id="type" title="Type" type="string"/>')
gexf_parts.append('    </attributes>')
gexf_parts.append('    <attributes class="edge">')
gexf_parts.append('      <attribute id="type" title="Edge Type" type="string"/>')
gexf_parts.append('      <attribute id="title" title="Title" type="string"/>')
gexf_parts.append('      <attribute id="start" title="Start" type="string"/>')
gexf_parts.append('      <attribute id="end" title="End" type="string"/>')
gexf_parts.append('      <attribute id="relation_type" title="Relation Type" type="string"/>')
gexf_parts.append('      <attribute id="context" title="Context" type="string"/>')
gexf_parts.append('      <attribute id="overlap_org" title="Overlap Org" type="string"/>')
gexf_parts.append('    </attributes>')

gexf_parts.append('  </graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF写入完成: {GEXF_PATH}")
print(f"   - {len(persons) + len(orgs)} 节点")
print(f"   - {len(positions) + len(all_rels)} 边")
print("✅ 全部完成！")
