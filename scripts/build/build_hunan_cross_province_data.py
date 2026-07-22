#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for Hunan cross-province cadre exchange network.
Captures all inter-provincial personnel flows involving Hunan Province.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/hunan_cross_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/hunan_cross_province_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

# Provinces/regions as nodes
provinces = [
    {"id": 1, "name": "湖南", "full_name": "湖南省", "region": "中部"},
    {"id": 2, "name": "浙江", "full_name": "浙江省", "region": "东部"},
    {"id": 3, "name": "上海", "full_name": "上海市", "region": "东部"},
    {"id": 4, "name": "江苏", "full_name": "江苏省", "region": "东部"},
    {"id": 5, "name": "江西", "full_name": "江西省", "region": "中部"},
    {"id": 6, "name": "海南", "full_name": "海南省", "region": "南部"},
    {"id": 7, "name": "广东", "full_name": "广东省", "region": "南部"},
    {"id": 8, "name": "陕西", "full_name": "陕西省", "region": "西部"},
    {"id": 9, "name": "吉林", "full_name": "吉林省", "region": "东北"},
    {"id": 10, "name": "甘肃", "full_name": "甘肃省", "region": "西部"},
    {"id": 11, "name": "北京", "full_name": "北京市（中央部委）", "region": "中央"},
    {"id": 12, "name": "黑龙江", "full_name": "黑龙江省", "region": "东北"},
    {"id": 13, "name": "西藏", "full_name": "西藏自治区", "region": "西部"},
    {"id": 14, "name": "新疆", "full_name": "新疆维吾尔自治区", "region": "西部"},
]

# Key individuals involved in cross-province flows (team, confirmed)
persons = [
    # ── Between Hunan and Zhejiang ──
    {"id": 1, "name": "毛伟明", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-05", "birthplace": "浙江衢州", "education": "浙江大学，工学学士",
     "party_join": "1985-09", "work_start": "1982-08",
     "current_post": "湖南省省长",
     "source": "https://zh.wikipedia.org/wiki/毛伟明"},
    {"id": 2, "name": "沈晓明", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-05", "birthplace": "浙江上虞", "education": "上海第二医科大学博士",
     "party_join": "1984-08", "work_start": "1987-07",
     "current_post": "湖南省委书记",
     "source": "https://zh.wikipedia.org/wiki/沈晓明"},
    {"id": 3, "name": "杜家毫", "gender": "男", "ethnicity": "汉族",
     "birth": "1955-07", "birthplace": "浙江鄞县", "education": "华东师范大学",
     "party_join": "1973-12", "work_start": "1973-03",
     "current_post": "曾任湖南省委书记（2016-2020）",
     "source": "https://zh.wikipedia.org/wiki/杜家毫"},

    # ── Between Hunan and Jiangxi ──
    {"id": 4, "name": "李小豹", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "湖南永兴", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任江西萍乡市委书记（已落马）",
     "source": "https://zh.wikipedia.org/wiki/李小豹"},
    {"id": 5, "name": "刘锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-08", "birthplace": "湖南衡阳", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任江西景德镇市委书记",
     "source": "https://zh.wikipedia.org/wiki/刘锋"},

    # ── Between Hunan and Shanghai ──
    {"id": 6, "name": "杜家毫（沪）", "gender": "男", "ethnicity": "汉族",
     "birth": "1955-07", "birthplace": "浙江鄞县", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任上海市委副秘书长（湖南前任书记）",
     "source": ""},

    # ── Between Hunan and Hainan ──
    {"id": 7, "name": "沈晓明（琼）", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-05", "birthplace": "浙江上虞", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任海南省委书记（调任湖南前）",
     "source": ""},

    # ── Between Hunan and Beijing/central ──
    {"id": 8, "name": "许达哲", "gender": "男", "ethnicity": "汉族",
     "birth": "1956-09", "birthplace": "湖南浏阳", "education": "哈尔滨工业大学硕士",
     "party_join": "1982-01", "work_start": "1975-12",
     "current_post": "曾任湖南省委书记（2021-2023）",
     "source": "https://zh.wikipedia.org/wiki/许达哲"},

    # ── Between Hunan and Gansu ──
    {"id": 9, "name": "徐守盛", "gender": "男", "ethnicity": "汉族",
     "birth": "1953-01", "birthplace": "江苏如东", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任湖南省长（2010-2013，已故）",
     "source": "https://zh.wikipedia.org/wiki/徐守盛"},

    # ── Between Hunan and Shaanxi ──
    {"id": 10, "name": "魏建锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-04", "birthplace": "", "education": "研究生，工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省纪委书记（从陕西调任）",
     "source": ""},

    # ── Between Hunan and Jilin ──
    {"id": 11, "name": "郭灵计", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委组织部部长（从吉林调任）",
     "source": ""},

    # ── Between Hunan and Guangdong ──
    {"id": 12, "name": "刘红兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省委宣传部部长（从广东调任）",
     "source": ""},

    # ── Between Hunan and Jiangsu ──
    {"id": 13, "name": "毛伟明（苏）", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-05", "birthplace": "浙江衢州", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "曾任江苏省副省长/省府秘书长（调任工信部前）",
     "source": ""},

    # ── Between Hunan and Beijing/Heilongjiang ──
    {"id": 14, "name": "张庆伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1961-11", "birthplace": "河北乐亭", "education": "西北工业大学硕士",
     "party_join": "1992-10", "work_start": "1982-08",
     "current_post": "曾任湖南省委书记（2021-2023），后任黑龙江",
     "source": "https://zh.wikipedia.org/wiki/张庆伟"},
]

# Cross-province transfer events
transfers = [
    # ── Outbound from Hunan ──
    {"id": 1, "person_name": "张庆伟", "from_province": "湖南", "to_province": "黑龙江",
     "from_role": "湖南省委书记", "to_role": "黑龙江省委书记/副委员长",
     "year": "2023",
     "type": "平行调任（跨省平调）",
     "context": "张庆伟2021年从黑龙江调任湖南书记，2023年又回调黑龙江/进入中央",
     "source": ""},
    {"id": 2, "person_name": "李小豹", "from_province": "湖南", "to_province": "江西",
     "from_role": "湖南永兴人/毕业后分配", "to_role": "江西萍乡市委书记",
     "year": "1990s-2022",
     "type": "跨省任职（湘籍干部在赣）",
     "context": "湖南永兴人，毕业后分配至江西，历任江西省内多个职务后任萍乡市委书记（2022年落马）",
     "source": "https://zh.wikipedia.org/wiki/李小豹"},
    {"id": 3, "person_name": "刘锋", "from_province": "湖南", "to_province": "江西",
     "from_role": "湖南衡阳人/毕业分配", "to_role": "江西景德镇市委书记",
     "year": "1990s-2026",
     "type": "跨省任职（湘籍干部在赣）",
     "context": "湖南衡阳人，在江西任职34年，从上饶基层逐步升至景德镇书记",
     "source": ""},

    # ── Inbound to Hunan ──
    {"id": 4, "person_name": "沈晓明", "from_province": "海南", "to_province": "湖南",
     "from_role": "海南省委书记", "to_role": "湖南省委书记",
     "year": "2023",
     "type": "省际调任",
     "context": "从海南省委书记平调湖南省委书记",
     "source": "https://zh.wikipedia.org/wiki/沈晓明"},
    {"id": 5, "person_name": "毛伟明", "from_province": "北京", "to_province": "湖南",
     "from_role": "国家电网董事长", "to_role": "湖南省省长",
     "year": "2020",
     "type": "央企→省长",
     "context": "从国家电网（北京）调任湖南省省长，此前还在江西、工信部任职",
     "source": "https://zh.wikipedia.org/wiki/毛伟明"},
    {"id": 6, "person_name": "许达哲", "from_province": "北京", "to_province": "湖南",
     "from_role": "工信部副部长/国防科工局局长", "to_role": "湖南省长→书记",
     "year": "2013",
     "type": "中央→地方",
     "context": "从工信部/国防科工局调任湖南省省长",
     "source": "https://zh.wikipedia.org/wiki/许达哲"},
    {"id": 7, "person_name": "杜家毫", "from_province": "上海", "to_province": "湖南",
     "from_role": "上海市委副秘书长/浦东新区区长", "to_role": "湖南省副省长→省长→书记",
     "year": "2011",
     "type": "省际调任",
     "context": "从上海市调任湖南省政府领导",
     "source": "https://zh.wikipedia.org/wiki/杜家毫"},
    {"id": 8, "person_name": "徐守盛", "from_province": "甘肃", "to_province": "湖南",
     "from_role": "甘肃省常务副省长", "to_role": "湖南省省长",
     "year": "2010",
     "type": "省际调任",
     "context": "从甘肃省常务副省长调任湖南省省长",
     "source": "https://zh.wikipedia.org/wiki/徐守盛"},
    {"id": 9, "person_name": "张庆伟", "from_province": "黑龙江", "to_province": "湖南",
     "from_role": "黑龙江省委书记", "to_role": "湖南省委书记",
     "year": "2021",
     "type": "省际调任",
     "context": "从黑龙江省委书记平调湖南省委书记",
     "source": ""},
    {"id": 10, "person_name": "魏建锋", "from_province": "陕西", "to_province": "湖南",
     "from_role": "陕西省副省长", "to_role": "湖南省纪委书记",
     "year": "2023~",
     "type": "省际调任",
     "context": "从陕西调任湖南省纪委书记",
     "source": ""},
    {"id": 11, "person_name": "郭灵计", "from_province": "吉林", "to_province": "湖南",
     "from_role": "吉林省四平市委书记", "to_role": "湖南省委组织部部长",
     "year": "2024~",
     "type": "省际调任",
     "context": "从吉林四平调任湖南省委组织部长",
     "source": ""},
    {"id": 12, "person_name": "刘红兵", "from_province": "广东", "to_province": "湖南",
     "from_role": "广东省湛江市委书记", "to_role": "湖南省委宣传部部长",
     "year": "2024~",
     "type": "省际调任",
     "context": "从广东湛江调任湖南省委宣传部长",
     "source": ""},
]

# Province-to-province edges: aggregated flow counts
province_edges = [
    {"from": "湖南", "to": "江西", "count": 2, "type": "湘籍干部赴赣任职",
     "list": "李小豹、刘锋"},
    {"from": "湖南", "to": "黑龙江", "count": 1, "type": "省委书记回调",
     "list": "张庆伟"},
    {"from": "海南", "to": "湖南", "count": 1, "type": "省委书记调任",
     "list": "沈晓明"},
    {"from": "北京", "to": "湖南", "count": 2, "type": "中央/央企→省",
     "list": "许达哲、毛伟明"},
    {"from": "上海", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "杜家毫"},
    {"from": "甘肃", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "徐守盛"},
    {"from": "陕西", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "魏建锋"},
    {"from": "吉林", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "郭灵计"},
    {"from": "广东", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "刘红兵"},
    {"from": "黑龙江", "to": "湖南", "count": 1, "type": "省际调任",
     "list": "张庆伟（2021调入湖南）"},
]


# ── BUILD SQLite ────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS provinces (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            full_name TEXT,
            region TEXT
        );
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS transfers (
            id INTEGER PRIMARY KEY,
            person_name TEXT NOT NULL,
            from_province TEXT NOT NULL,
            to_province TEXT NOT NULL,
            from_role TEXT,
            to_role TEXT,
            year TEXT,
            type TEXT,
            context TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS province_relationships (
            id INTEGER PRIMARY KEY,
            province_a TEXT NOT NULL,
            province_b TEXT NOT NULL,
            flow_count INTEGER,
            flow_type TEXT,
            person_list TEXT
        );
    """)

    for p in provinces:
        cur.execute("""INSERT OR REPLACE INTO provinces VALUES (?,?,?,?)""",
                     (p["id"], p["name"], p["full_name"], p["region"]))

    for p in persons:
        cur.execute("""INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                     (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                      p["birthplace"], p["education"], p["party_join"], p["work_start"],
                      p["current_post"], p["source"]))

    for t in transfers:
        cur.execute("""INSERT OR REPLACE INTO transfers VALUES (?,?,?,?,?,?,?,?,?,?)""",
                     (t["id"], t["person_name"], t["from_province"], t["to_province"],
                      t["from_role"], t["to_role"], t["year"], t["type"], t["context"],
                      t["source"]))

    eid = 0
    for e in province_edges:
        eid += 1
        cur.execute("""INSERT OR REPLACE INTO province_relationships VALUES (?,?,?,?,?,?)""",
                     (eid, e["from"], e["to"], e["count"], e["type"], e["list"]))

    conn.commit()
    conn.close()
    print(f"✓ SQLite DB created: {DB_PATH}")


# ── BUILD GEXF ──────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def province_color(region):
    colors = {
        "中部": "200,200,100",
        "东部": "100,200,200",
        "南部": "100,200,100",
        "西部": "200,150,100",
        "东北": "150,150,200",
        "中央": "200,100,100",
    }
    return colors.get(region, "180,180,180")

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Government Personnel Network Investigator</creator>')
    lines.append('    <description>湖南省跨省干部交流网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="directed">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="region" type="string"/>')
    lines.append('      <attribute id="2" title="detail" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="count" type="integer"/>')
    lines.append('      <attribute id="2" title="persons" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: provinces
    lines.append('    <nodes>')
    for p in provinces:
        c = province_color(p["region"])
        sz = "20.0" if p["name"] == "湖南" else "14.0"
        lines.append(f'      <node id="prov_{p["name"]}" label="{esc(p["full_name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="province"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["region"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        rgb = c.split(",")
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: key individuals
    for p in persons:
        lines.append(f'      <node id="per_{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("birthplace",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="150" g="150" b="150"/>')
        lines.append('        <viz:size value="10.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')

    # Province-to-province flow edges
    for e in province_edges:
        eid += 1
        weight = str(e["count"])
        lines.append(f'      <edge id="e{eid}" source="prov_{e["from"]}" target="prov_{e["to"]}" label="{esc(e["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="flow"/>')
        lines.append(f'          <attvalue for="1" value="{e["count"]}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(e["list"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person-to-province edges (work in)
    person_province = {
        "毛伟明": "湖南", "沈晓明": "湖南", "杜家毫": "湖南",
        "许达哲": "湖南", "徐守盛": "湖南", "张庆伟": "湖南",
        "魏建锋": "湖南", "郭灵计": "湖南", "刘红兵": "湖南",
        "李小豹": "江西", "刘锋": "江西",
    }
    for p in persons:
        base_name = p["name"].split("（")[0]
        target = person_province.get(base_name)
        if target:
            eid += 1
            lines.append(f'      <edge id="e{eid}" source="per_{p["id"]}" target="prov_{target}" label="works_in" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="works_in"/>')
            lines.append('          <attvalue for="1" value="1"/>')
            lines.append(f'          <attvalue for="2" value="{esc(p.get("current_post",""))}"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')

    # Person-to-person edges (same person across roles - connection edges)
    # Mao Weiming ↔ Shen Xiaoming (both Zhejiang origin, work together)
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="per_1" target="per_2" label="浙籍同僚" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="same_origin"/>')
    lines.append('          <attvalue for="1" value="2"/>')
    lines.append('          <attvalue for="2" value="浙江籍+湖南省委正副书记"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

    # Du Jiahao ↔ Mao Weiming (both Zhejiang, both Hunan governors)
    eid += 1
    lines.append(f'      <edge id="e{eid}" source="per_3" target="per_1" label="浙籍前后任" weight="1.5">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="same_origin"/>')
    lines.append('          <attvalue for="1" value="2"/>')
    lines.append('          <attvalue for="2" value="浙江籍+先后任湖南省长"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_db()
    build_gexf()
    print(f"\n  Provinces: {len(provinces)}")
    print(f"  Key Persons: {len(persons)}")
    print(f"  Transfer Events: {len(transfers)}")
    print(f"  Province-Province Edges: {len(province_edges)}")
    print("✓ Done")
