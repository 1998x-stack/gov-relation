#!/usr/bin/env python3
"""
Build SQLite database + GEXF graph for 自贡市 cadre exchange network investigation.
Data sourced from Baidu/Bing searches (2026-07-26).
"""

import sqlite3
import json
import os
from datetime import datetime

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(OUT_DIR, "自贡市_network.db")
GEXF_PATH = os.path.join(OUT_DIR, "自贡市_network.gexf")
REPORT_DATE = "20260726"

# ── Data ──────────────────────────────────────────────────────

persons = [
    {
        "id": "zigong_zeng_hongyang",
        "name": "曾洪扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-02",
        "birthplace": "四川广汉",
        "education": "上海交通大学(学士)",
        "party_join": "1993-03",
        "work_start": "1994-07",
        "current_post": "自贡市委书记",
        "current_org": "中共自贡市委",
        "source": "百度百科/川观新闻",
    },
    {
        "id": "zigong_shi_gang",
        "name": "石钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-07",
        "birthplace": "四川渠县",
        "education": "西南财经大学工商管理",
        "party_join": "1999-06",
        "work_start": "1991-07",
        "current_post": "自贡市市长",
        "current_org": "自贡市人民政府",
        "source": "百度搜索",
    },
    {
        "id": "zigong_he_li",
        "name": "何礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "离任(原自贡市委书记)",
        "current_org": "",
        "source": "川观新闻2023.2.16",
    },
    {
        "id": "zigong_fan_bo",
        "name": "范波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "山东省(原自贡市委书记)",
        "current_org": "山东省",
        "source": "百度搜索",
        "note": "2021年跨省调任山东省，是自贡近年最重要的跨省干部输出案例"
    },
    {
        "id": "zigong_li_gang",
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "历任巴中市委书记等地",
        "current_org": "",
        "source": "百度搜索(部分)",
    },
    {
        "id": "zigong_huang_xuezhi",
        "name": "黄雪智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原自贡市副市长(已免)",
        "current_org": "",
        "source": "自贡市人大常委会公告",
    },
    {
        "id": "zigong_zhu_bin",
        "name": "朱斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贡市人大常委会副主任",
        "current_org": "自贡市人大常委会",
        "source": "2025年2月自贡市人代会公告",
    },
    {
        "id": "zigong_tan_bao",
        "name": "谭豹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贡市人大常委会主任",
        "current_org": "自贡市人大常委会",
        "source": "自贡人大网",
    },
    {
        "id": "zigong_zhang_ying",
        "name": "张颖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贡市人民政府副市长",
        "current_org": "自贡市人民政府",
        "source": "2025年12月自贡人大常委会任命",
    },
    {
        "id": "zigong_huang_rubei",
        "name": "黄如贝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贡市人民政府秘书长",
        "current_org": "自贡市人民政府",
        "source": "2025年12月四川观察",
    },
]

organizations = [
    {"id": "org_zigong_city", "name": "自贡市", "type": "地级市", "level": "prefecture", "parent": "四川省", "location": "四川"},
    {"id": "org_zigong_cpc", "name": "中共自贡市委", "type": "党委", "level": "prefecture", "parent": "四川省委", "location": "自贡"},
    {"id": "org_zigong_gov", "name": "自贡市人民政府", "type": "政府", "level": "prefecture", "parent": "自贡市委", "location": "自贡"},
    {"id": "org_zigong_npc", "name": "自贡市人大常委会", "type": "人大", "level": "prefecture", "parent": "", "location": "自贡"},
    {"id": "org_leshan_cpc", "name": "中共乐山市委", "type": "党委", "level": "prefecture", "parent": "四川省委", "location": "乐山"},
    {"id": "org_sichuan_housing", "name": "四川省住房和城乡建设厅", "type": "政府厅局", "level": "provincial department", "parent": "四川省政府", "location": "成都"},
    {"id": "org_sichuan_finance", "name": "四川省财政厅", "type": "政府厅局", "level": "provincial department", "parent": "四川省政府", "location": "成都"},
    {"id": "org_sichuan_ndrc", "name": "四川省发展和改革委员会", "type": "政府厅局", "level": "provincial department", "parent": "四川省政府", "location": "成都"},
    {"id": "org_shandong", "name": "山东省", "type": "省份", "level": "province", "parent": "中国", "location": "山东"},
    {"id": "org_guangan", "name": "广安市", "type": "地级市", "level": "prefecture", "parent": "四川省", "location": "广安"},
    {"id": "org_bazhong", "name": "巴中市", "type": "地级市", "level": "prefecture", "parent": "四川省", "location": "巴中"},
]

positions = [
    # 曾洪扬
    {"person_id": "zigong_zeng_hongyang", "org_id": "org_guangan", "title": "广安市基层/中层任职", "start": "1994", "end": "2015", "rank": "general", "note": "1994-2015广安工作经历(具体职务待查)"},
    {"person_id": "zigong_zeng_hongyang", "org_id": "org_leshan_cpc", "title": "中共乐山市委副书记", "start": "2016", "end": "2021", "rank": "vice-prefecture", "note": "跨市调任关键节点"},
    {"person_id": "zigong_zeng_hongyang", "org_id": "org_zigong_gov", "title": "自贡市市长", "start": "2021", "end": "2023-02", "rank": "prefecture", "note": "从乐山副书记调任"},
    {"person_id": "zigong_zeng_hongyang", "org_id": "org_zigong_cpc", "title": "自贡市委书记", "start": "2023-02", "end": "", "rank": "prefecture", "note": "本市晋升"},
    # 石钢
    {"person_id": "zigong_shi_gang", "org_id": "org_sichuan_housing", "title": "四川省住建厅副厅长", "start": "", "end": "2023-2024", "rank": "deputy provincial department", "note": ""},
    {"person_id": "zigong_shi_gang", "org_id": "org_zigong_gov", "title": "自贡市市长", "start": "2023-2024", "end": "", "rank": "prefecture", "note": "从省住建厅副厅长调任"},
    # 何礼
    {"person_id": "zigong_he_li", "org_id": "org_sichuan_finance", "title": "四川省财政厅(何礼曾任)", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": "zigong_he_li", "org_id": "org_zigong_cpc", "title": "自贡市委书记", "start": "2021", "end": "2023-02", "rank": "prefecture", "note": "2023年2月卸任"},
    # 范波
    {"person_id": "zigong_fan_bo", "org_id": "org_sichuan_ndrc", "title": "四川省发改委副主任/相关职务", "start": "", "end": "2017", "rank": "", "note": ""},
    {"person_id": "zigong_fan_bo", "org_id": "org_zigong_cpc", "title": "自贡市委书记", "start": "2017", "end": "2021", "rank": "prefecture", "note": ""},
    {"person_id": "zigong_fan_bo", "org_id": "org_shandong", "title": "山东省任职", "start": "2021", "end": "", "rank": "", "note": "跨省调任"},
    # 李刚
    {"person_id": "zigong_li_gang", "org_id": "org_zigong_cpc", "title": "自贡市委书记(前任)", "start": "", "end": "2016", "rank": "prefecture", "note": ""},
    # 朱斌
    {"person_id": "zigong_zhu_bin", "org_id": "org_zigong_gov", "title": "自贡市人民政府秘书长", "start": "", "end": "2025-02", "rank": "deputy-prefecture", "note": ""},
    {"person_id": "zigong_zhu_bin", "org_id": "org_zigong_npc", "title": "自贡市人大常委会副主任", "start": "2025-02", "end": "", "rank": "deputy-prefecture", "note": "当选"},
    # 黄雪智
    {"person_id": "zigong_huang_xuezhi", "org_id": "org_zigong_gov", "title": "自贡市人民政府副市长", "start": "", "end": "", "rank": "deputy-prefecture", "note": "已免"},
    # 张颖
    {"person_id": "zigong_zhang_ying", "org_id": "org_zigong_gov", "title": "自贡市人民政府副市长", "start": "2025-12", "end": "", "rank": "deputy-prefecture", "note": "任命"},
    # 黄如贝
    {"person_id": "zigong_huang_rubei", "org_id": "org_zigong_gov", "title": "自贡市人民政府秘书长", "start": "2025-12", "end": "", "rank": "deputy-prefecture", "note": "任命"},
    # 谭豹
    {"person_id": "zigong_tan_bao", "org_id": "org_zigong_npc", "title": "自贡市人大常委会主任", "start": "", "end": "", "rank": "prefecture", "note": ""},
]

relationships = [
    {"person_a": "zigong_zeng_hongyang", "person_b": "zigong_he_li", "type": "succession", "context": "曾洪扬接替何礼任自贡市委书记", "overlap_org": "org_zigong_cpc", "overlap_period": "2023年换"},
    {"person_a": "zigong_he_li", "person_b": "zigong_fan_bo", "type": "succession", "context": "何礼接替范波任自贡市委书记", "overlap_org": "org_zigong_cpc", "overlap_period": "约2021年"},
    {"person_a": "zigong_li_gang", "person_b": "zigong_fan_bo", "type": "succession", "context": "李刚卸任自贡市委书记，范波接任", "overlap_org": "org_zigong_cpc", "overlap_period": "约2017年"},
    {"person_a": "zigong_zeng_hongyang", "person_b": "zigong_shi_gang", "type": "colleague", "context": "曾洪扬书记+石钢市长搭班子", "overlap_org": "org_zigong_cpc", "overlap_period": "2023/2024至今"},
    {"person_a": "zigong_zeng_hongyang", "person_b": "zigong_zhu_bin", "type": "colleague", "context": "曾洪扬(市委)+朱斌(人大)先后同属自贡系统", "overlap_org": "org_zigong_cpc", "overlap_period": ""},
]

# ── Step 1: SQLite ─────────────────────────────────────

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id TEXT, org_id TEXT, title TEXT,
    start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a TEXT, person_b TEXT, type TEXT,
    context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], 
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                   VALUES (?,?,?,?,?,?,?)""",
                (pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                   VALUES (?,?,?,?,?,?)""",
                (r["person_a"], r["person_b"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()

print(f"[SQLite] Written: {DB_PATH}")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ── GEXF ───────────────────────────────────────────────

def gexf_escape(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

citation_list = [
    "百度搜索-曾洪扬简历/自贡市委书记",
    "百度搜索-石钢简历/自贡市长",
    "川观新闻2023.2.16: 四川省委关于曾洪扬任职决定",
    "自贡市政府人事任免公告(2025-2026)",
    "自贡人大常委会公告(2025年2月)",
    "四川观察(2025年12月人事任免)",
    "四川省自然资源厅:自贡市自然资源系统轮岗交流",
    "百度搜索-范波简历(跨省调任山东)",
    "百度搜索-何礼/李刚职务变动"
]

nodes_xml = ""
edges_xml = ""

for p in persons:
    color = ""
    if "书记" in p["current_post"] and "副" not in p["current_post"]:
        color = 'r="200" g="40" b="50"'  # red for party secretary
    elif "市长" in p["current_post"] and "副" not in p["current_post"]:
        color = 'r="30" g="100" b="200"'   # blue for mayor
    elif "常委" in p["current_post"] or "副" in p["current_post"]:
        color = 'r="240" g="140" b="30"'   # orange for deputy
    else:
        color = 'r="150" g="150" b="150"'  # grey for others
    
    size = '20.0' if p["current_post"] in ["自贡市委书记", "自贡市市长"] else '12.0'
    label = f"{p['name']}\\n{p['current_post']}"
    nodes_xml += f"""  <node id="{gexf_escape(p['id'])}" label="{gexf_escape(label)}">
    <attvalues>
      <attvalue for="name" value="{gexf_escape(p['name'])}"/>
      <attvalue for="gender" value="{gexf_escape(p['gender'])}"/>
      <attvalue for="birth" value="{gexf_escape(p['birth'])}"/>
      <attvalue for="birthplace" value="{gexf_escape(p['birthplace'])}"/>
      <attvalue for="role" value="{gexf_escape(p['current_post'])}"/>
    </attvalues>
    <viz:color {color}/>
    <viz:size value="{size}"/>
  </node>
"""

for o in organizations:
    if "厅" in o["name"] or "常委" in o["type"] or "人大" in o["name"]:
        color = 'r="100" g="100" b="200"'  # bureaucratic orgs
    else:
        color = 'r="80" g="180" b="80"'   # others
    nodes_xml += f"""  <node id="{gexf_escape(o['id'])}">
    <attvalues>
      <att value="{gexf_escape(o['name'])}"/>
      <att value="{gexf_escape(o['type'])}"/>
      <att value="{gexf_escape(o['location'])}"/>
    </atvalues>
    <viz:color {color}/>
    <viz:size value="8.0"/>
  </node>
"""

for pos in positions:
    edges_xml += f"""  <edge id="{pos['person_id']}_{战士  id={pos['org_id']}" source="{pos['person_id']}" target="{pos['org_id']}" type="directed" key="worked_at">
    <att values>
      <att for="start" value="{gexf_escape(pos['start'])}"/>
      <att for="end" value="{gexf_escape(pos['end'])}"/>
      <att for="title" value="{gexf_escape(pos['title'])}"/>
    </atvalues>
    <viz:thickness value="1.0"/>
  </edge>
"""

for i, r in enumerate(relationships):
    edge_type = r["type"]
    color = 'r="0" g="0" b="0"'
    if edge_type == "ely":
        color = 'r="180" g="120" b="30"'  # gold for succession
    elif edge_type == "temporal":
        color = 'r="60" g="60" b="2010"'  # blue for colleague
    edges_xml += f"""  <edge id="rel_{r}" source="{r['person_a']}" target="{r['person_b']}" type="relationship" key="relationship">
    <attvalues>
      <att value="{gexf_escape(r['context'])}"/>
      <att value="{gexf_escape(r['overlap_period'])}"/>
    </atvalues>
    <viz:color {color}/>
    <viz:thickness total="100.0"/>
  </edge>
"""

gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:viz="http://gexf.net/1.3/viz"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <metadata>
    <description>自贡市跨地区干部交流网络 • {REPORT_DIR}</description>
    <creators>OpenCode china-gov-network skill</creators>
    <keywords>自贡, 干部交流, 跨市调任, 四川省</keywords>
  </metadata>
  <graph mode="static" defaultedgetype="directed">
    <attributes class="node">
      <att id="name" title="person/org_name" type="string"/>
      {custom_attrs}
    </attributes>
    <attributes class="edge">
        <att id="start" title="start_date" type="string"/>
        <att id="end" title="end_date" type="string"/>
        <att id="title" title="position_title" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}
    </nodes>
    <edges>
{edges_xml}
    </edges>
  </graph>
  <sources>
    <clipboard id="citations" type="visual"/>
    <clipboardHeadline>数据来源</clipboardHeadline>
    <sourcelist>
      <source>百度搜索(曾洪扬)</source>
      <source>百度搜索(石钢)</source>
      <source>川观新闻2023.2.16</source>
      <source>自贡市政府人事任免(2025-2026)</source>
      <source>自贡人大常委会公告</source>
      <source>四川观察(2025.12)</source>
      <source>四川省自然资源厅</source>
    </sourcelist>
  </sources>
</gexf>
"""

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf)

print(f"[✓] GEXF Written: {GEXF_PATH}")
print(f"   Nodes: {len(persons) + len(organizations)}")
print(f"   Edges: {len(positions) + len(relationships)}")

print("\n=== Summary ===")
print(f"Report: report/20260726-自贡市-干部交流网络分析.md")
print(f"SQLite: {DB_PATH}  ({os.path.getsize(DB_PATH)} bytes)")
print(f"GEXF:   {GEXF_PATH}  ({os.path.getsize(GEXF_PATH)} bytes)")
print("Done.")
