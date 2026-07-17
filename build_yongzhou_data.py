#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 永州市 (Yongzhou City) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yongzhou_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yongzhou_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════
    # A. CITY LEVEL
    # ═══════════════════════════════════════════════════════════════

    # ── 1. 市委书记 ──
    {"id": 1, "name": "陈爱林", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-05", "birthplace": "湖北浠水", "education": "湖北大学经济学学士(1990)/天津财经大学经济学硕士(1996)/中国人民大学经济学博士(2000)",
     "party_join": "中共党员", "work_start": "1990",
     "current_post": "永州市委书记", "current_org": "中共永州市委",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E7%88%B1%E6%9E%97_(1970%E5%B9%B4)"},

    # ── 2. 市长（空缺）──
    {"id": 2, "name": "（空缺）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "永州市市长（空缺）", "current_org": "永州市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%B7%9E%E5%B8%82"},

    # ── 3. 人大主任 ──
    {"id": 3, "name": "蒋强先", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "湖南南县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永州市人大常委会主任", "current_org": "永州市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%B7%9E%E5%B8%82"},

    # ── 4. 政协主席 ──
    {"id": 4, "name": "谢景林", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-04", "birthplace": "湖南新田", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "永州市政协主席", "current_org": "永州市政协",
     "source": "https://zh.wikipedia.org/wiki/%E6%B0%B8%E5%B7%9E%E5%B8%82"},

    # ── 5. 前任市委书记（2021-2026）──
    {"id": 5, "name": "朱洪武", "gender": "男", "ethnicity": "黎族",
     "birth": "1971-09", "birthplace": "海南澄迈", "education": "海南大学/中山大学/中央党校",
     "party_join": "1993", "work_start": "",
     "current_post": "前任永州市委书记（2021-2026，另有任用）", "current_org": "中共永州市委（前任）",
     "source": "https://zh.wikipedia.org/wiki/%E6%9C%B1%E6%B4%AA%E6%AD%A6_(1971%E5%B9%B4)"},

    # ── 6. 前前任市委书记（2019-2021）──
    {"id": 6, "name": "严华", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-08", "birthplace": "湖南澧县", "education": "湖南师范大学/湖南大学",
     "party_join": "1987", "work_start": "1991",
     "current_post": "前任邵阳市委书记/永州市委书记（2019-2021）", "current_org": "中共邵阳市委（前任）",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%A5%E5%8D%8E_(1968%E5%B9%B4)"},

    # ═══════════════════════════════════════════════════════════════
    # B. DISTRICT/COUNTY LEVEL
    # ═══════════════════════════════════════════════════════════════

    # ── 3. 东安县 ──
    {"id": 20, "name": "唐何", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "湖南华容", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "东安县委书记", "current_org": "中共东安县委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%9C%E5%AE%89%E5%8E%BF"},
    {"id": 21, "name": "蒋华", "gender": "男", "ethnicity": "瑶族",
     "birth": "1980-10", "birthplace": "湖南道县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "东安县县长", "current_org": "东安县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%9C%E5%AE%89%E5%8E%BF"},

    # ── 4. 双牌县 ──
    {"id": 22, "name": "张跃斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-10", "birthplace": "永州冷水滩", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "双牌县委书记", "current_org": "中共双牌县委",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF"},
    {"id": 23, "name": "蔡富强", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "永州冷水滩", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "双牌县县长", "current_org": "双牌县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8F%8C%E7%89%8C%E5%8E%BF"},

    # ── 5. 道县 ──
    {"id": 24, "name": "唐超学", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-08", "birthplace": "湖南宁远", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "道县县委书记", "current_org": "中共道县县委",
     "source": "https://zh.wikipedia.org/wiki/%E9%81%93%E5%8E%BF"},
    {"id": 25, "name": "刘华中", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "湖南隆回", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "道县县长", "current_org": "道县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%81%93%E5%8E%BF"},

    # ── 6. 江永县 ──
    {"id": 26, "name": "唐德荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-12", "birthplace": "永州冷水滩", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江永县委书记", "current_org": "中共江永县委",
     "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E6%B0%B8%E5%8E%BF"},
    {"id": 27, "name": "何德波", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-12", "birthplace": "湖南道县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江永县县长", "current_org": "江永县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E6%B0%B8%E5%8E%BF"},

    # ── 7. 宁远县 ──
    {"id": 28, "name": "胡勇刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-08", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁远县委书记", "current_org": "中共宁远县委",
     "source": "https://zh.wikipedia.org/wiki/%E5%AE%81%E8%BF%9C%E5%8E%BF"},
    {"id": 29, "name": "毛政", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "湖南衡阳", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "宁远县县长", "current_org": "宁远县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%AE%81%E8%BF%9C%E5%8E%BF"},

    # ── 8. 蓝山县 ──
    {"id": 30, "name": "邓群", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "湖南双牌", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓝山县委书记", "current_org": "中共蓝山县委",
     "source": "https://zh.wikipedia.org/wiki/%E8%93%9D%E5%B1%B1%E5%8E%BF"},
    {"id": 31, "name": "曾艺", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-08", "birthplace": "湖南新化", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "蓝山县县长", "current_org": "蓝山县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%93%9D%E5%B1%B1%E5%8E%BF"},

    # ── 9. 新田县 ──
    {"id": 32, "name": "陈雄", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "湖南东安", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新田县委书记", "current_org": "中共新田县委",
     "source": "https://zh.wikipedia.org/wiki/%E6%96%B0%E7%94%B0%E5%8E%BF"},
    {"id": 33, "name": "黄永英", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-06", "birthplace": "湖南蓝山", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新田县县长", "current_org": "新田县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%96%B0%E7%94%B0%E5%8E%BF"},

    # ── 10. 江华瑶族自治县 ──
    {"id": 34, "name": "段贵建", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "湖南祁阳", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江华瑶族自治县委书记", "current_org": "中共江华瑶族自治县委",
     "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E5%8D%8E%E7%91%B6%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8E%BF"},
    {"id": 35, "name": "吴军臣", "gender": "男", "ethnicity": "瑶族",
     "birth": "1978-12", "birthplace": "江华瑶族自治县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "江华瑶族自治县县长", "current_org": "江华瑶族自治县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%B1%9F%E5%8D%8E%E7%91%B6%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8E%BF"},

    # ── 11. 祁阳市 ──
    {"id": 36, "name": "蒋崇华", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-03", "birthplace": "湖南东安", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "祁阳市委书记", "current_org": "中共祁阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E7%A5%81%E9%98%B3%E5%B8%82"},
    {"id": 37, "name": "向子顺", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-08", "birthplace": "湖南洪江", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "祁阳市市长", "current_org": "祁阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E7%A5%81%E9%98%B3%E5%B8%82"},
]

# ── ORGANIZATIONS ──

organizations = [
    {"id": 1, "name": "中共永州市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "永州市"},
    {"id": 2, "name": "永州市人民政府", "type": "政府", "level": "地市级", "parent": "", "location": "永州市"},
    {"id": 3, "name": "永州市人大常委会", "type": "人大", "level": "地市级", "parent": "", "location": "永州市"},
    {"id": 4, "name": "永州市政协", "type": "政协", "level": "地市级", "parent": "", "location": "永州市"},
    {"id": 20, "name": "中共东安县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市东安县"},
    {"id": 21, "name": "东安县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市东安县"},
    {"id": 22, "name": "中共双牌县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市双牌县"},
    {"id": 23, "name": "双牌县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市双牌县"},
    {"id": 24, "name": "中共道县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市道县"},
    {"id": 25, "name": "道县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市道县"},
    {"id": 26, "name": "中共江永县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市江永县"},
    {"id": 27, "name": "江永县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市江永县"},
    {"id": 28, "name": "中共宁远县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市宁远县"},
    {"id": 29, "name": "宁远县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市宁远县"},
    {"id": 30, "name": "中共蓝山县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市蓝山县"},
    {"id": 31, "name": "蓝山县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市蓝山县"},
    {"id": 32, "name": "中共新田县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市新田县"},
    {"id": 33, "name": "新田县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市新田县"},
    {"id": 34, "name": "中共江华瑶族自治县委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市江华县"},
    {"id": 35, "name": "江华瑶族自治县人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市江华县"},
    {"id": 36, "name": "中共祁阳市委", "type": "党委", "level": "县级", "parent": "中共永州市委", "location": "永州市祁阳市"},
    {"id": 37, "name": "祁阳市人民政府", "type": "政府", "level": "县级", "parent": "永州市人民政府", "location": "永州市祁阳市"},
]

# ── POSITIONS ──
positions = [
    # City level
    (1, 1, 1, "市委书记", "2026-05", None, "gleichzeitig先任市长后升书记"),
    (1, 2, 2, "市长/代理市长", "2021-08", "2026-05", "升任市委书记"),
    (5, 1, 1, "市委书记", "2021-08", "2026-05", "另有任用"),
    (5, 2, 2, "市长", "2019-12", "2021-08", "升任书记"),
    (6, 1, 1, "市委书记", "2019-02", "2021-08", "调任邵阳市委书记"),
    (3, 1, 3, "市人大常委会主任", "2023-12", None, ""),
    (4, 1, 4, "市政协主席", "2022-01", None, ""),
    # County level
    (20, 20, 20, "县委书记", "2021-07", None, ""),
    (21, 21, 21, "县长", "2021-07", None, ""),
    (22, 22, 22, "县委书记", "2021-10", None, ""),
    (23, 23, 23, "县长", "2021-10", None, ""),
    (24, 24, 24, "县委书记", "2024-10", None, ""),
    (25, 25, 25, "县长", "2024-12", None, ""),
    (26, 26, 26, "县委书记", "2021-07", None, ""),
    (27, 27, 27, "县长", "2021-06", None, ""),
    (28, 28, 28, "县委书记", "2022-01", None, ""),
    (29, 29, 29, "县长", "2021-07", None, ""),
    (30, 30, 30, "县委书记", "2025-12", None, ""),
    (31, 31, 31, "县长", "2026-01", None, ""),
    (32, 32, 32, "县委书记", "2024-02", None, ""),
    (33, 33, 33, "县长", "2021-06", None, ""),
    (34, 34, 34, "县委书记", "2021-05", None, ""),
    (35, 35, 35, "县长", "2021-07", None, ""),
    (36, 36, 36, "市委书记", "2021-04", None, ""),
    (37, 37, 37, "市长", "2025-03", None, ""),
]

# ── RELATIONSHIPS ──
relationships = [
    # 1. Chen Ailin and Zhu Hongwu worked together (mayor-secretary pair)
    (1, 5, "上下级搭档", "陈爱林任市长时朱洪武任市委书记", "永州市人民政府/市委", "2021-08~2026-05"),
    # 2. Yan Hua was Zhu Hongwu's predecessor as secretary
    (6, 5, "前后任交接", "严华调任邵阳后朱洪武接任永州市委书记", "中共永州市委", "2021-08"),
    # 3. Chen Ailin succeeds Zhu Hongwu
    (1, 5, "前后任交接", "陈爱林接替朱洪武任永州市委书记", "中共永州市委", "2026-05"),
    # Known cross-county connections
    (21, 27, "同乡/籍贯", "蒋华（东安县长）与何德波（江永县长）均籍贯道县", "道县", ""),
    (27, 25, "同县", "何德波（江永县长）与刘华中（道县县长）", "道县/隆回", ""),
]

# ═══════════════════════════════════════════════════════════════════
# BUILD SQLITE
# ═══════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
    work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
    parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("INSERT OR IGNORE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("INSERT OR IGNORE INTO organizations VALUES (?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, note) VALUES (?,?,?,?,?,?)",
              (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]))

for r in relationships:
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
              (r[0], r[1], r[2], r[3], r[4], r[5]))

conn.commit()

# ═══════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <meta>')
lines.append(f'    <creator>Yongzhou Leadership Network Builder</creator>')
lines.append(f'    <description>永州市领导班子工作关系网络</description>')
lines.append(f'    <date>{datetime.now().isoformat()}</date>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Nodes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="role" title="角色" type="string"/>')
lines.append('      <attribute id="birth" title="出生" type="string"/>')
lines.append('      <attribute id="birthplace" title="籍贯" type="string"/>')
lines.append('      <attribute id="source" title="来源" type="string"/>')
lines.append('    </attributes>')

lines.append('    <nodes>')
for p in persons:
    if p["name"] == "（空缺）":
        continue
    # Role color: red=party secretary, blue=gov leader, orange=discipline, grey=other
    post = p["current_post"]
    if "书记" in post and ("县委" in post or "市委" in post or "区委" in post):
        role = "党委党组书记"
    elif "市长" in post or "县长" in post or "区长" in post:
        role = "政府正职"
    elif "人大" in post:
        role = "人大主任"
    elif "政协" in post:
        role = "政协主席"
    else:
        role = "其他"
    lines.append(f'      <node id="p{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="{role}"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    if role == "党委党组书记":
        lines.append(f'        <viz:color r="200" g="30" b="30"/>')  # Red
        lines.append(f'        <viz:size value="20.0"/>')
    elif role == "政府正职":
        lines.append(f'        <viz:color r="30" g="80" b="180"/>')  # Blue
        lines.append(f'        <viz:size value="20.0"/>')
    elif role == "人大主任":
        lines.append(f'        <viz:color r="30" g="160" b="80"/>')  # Green
        lines.append(f'        <viz:size value="15.0"/>')
    elif role == "政协主席":
        lines.append(f'        <viz:color r="200" g="130" b="20"/>')  # Orange
        lines.append(f'        <viz:size value="15.0"/>')
    else:
        lines.append(f'        <viz:color r="128" g="128" b="128"/>')  # Grey
        lines.append(f'        <viz:size value="12.0"/>')
    lines.append(f'      </node>')

# Organization nodes
for o in organizations:
    lines.append(f'      <node id="org_{o["id"]}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="组织机构"/>')
    lines.append(f'          <attvalue for="birth" value=""/>')
    lines.append(f'          <attvalue for="birthplace" value=""/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="180" g="180" b="180"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
eid = 0
# Person ↔ Org
for pos in positions:
    pid = pos[0]  # person_id
    oid = pos[1]  # org_id
    person_name = next((p["name"] for p in persons if p["id"] == pid), "")
    if person_name == "（空缺）":
        continue
    org_name = next((o["name"] for o in organizations if o["id"] == oid), "")
    lines.append(f'      <edge id="e{eid}" source="p{pid}" target="org_{oid}" label="{pos[2]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="任职"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="160" g="160" b="160"/>')
    lines.append(f'        <viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')
    eid += 1

# Person ↔ Person
for r in relationships:
    lines.append(f'      <edge id="e{eid}" source="p{r[0]}" target="p{r[1]}" label="{r[2]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="role" value="{r[2]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="180" g="140" b="0"/>')  # Gold for relationships
    lines.append(f'        <viz:thickness value="2.0"/>')
    lines.append(f'      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

conn.close()

# ═══════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════

print("=" * 60)
print("永州市 (Yongzhou) Leadership Network — Build Complete")
print("=" * 60)
print(f"  Database:  {DB_PATH}")
print(f"  GEXF:      {GEXF_PATH}")
print(f"  Persons:   {len(persons)} ({sum(1 for p in persons if p['name'] != '（空缺）')} real people)")
print(f"  Orgs:      {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relations: {len(relationships)}")
print(f"  Date:      {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)
