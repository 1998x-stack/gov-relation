#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Shifang City leadership network.
   
   什邡市 (Shifang) — 四川省德阳市下辖县级市
   Current as of: 2026-07-26
   
   Sources:
   - https://www.shifang.gov.cn/leaders.htm (政府领导之窗)
   - https://www.shifang.gov.cn (政务新闻)
   - Investigation: sichuan_什邡市
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "什邡市_network.db")
GEXF_PATH = os.path.join(BASE, "什邡市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══
    {   # 市委书记
        "id": 1, "name": "晏世莹", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "中共什邡市委书记", "current_org": "中共什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113451.htm"
    },
    {   # 市委副书记、市长
        "id": 2, "name": "叶科", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "",
        "education": "清华大学热能与动力工程专业 工学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委副书记、市政府市长、党组书记", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/fc/10098761.htm"
    },
    # ═══ Party Committee Leadership ═══
    {   # 市委副书记（专职）
        "id": 3, "name": "丁斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共什邡市委副书记", "current_org": "中共什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113451.htm"
    },
    {   # 市委常委、常务副市长
        "id": 4, "name": "杨益", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-02", "birthplace": "",
        "education": "大学 教育学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、市政府常务副市长", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fwld/cw/10000611.htm"
    },
    {   # 市委常委、纪委书记、监委主任
        "id": 5, "name": "张仲可", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、市纪委书记、市监委主任", "current_org": "中共什邡市纪律检查委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113341.htm"
    },
    {   # 市委常委、组织部部长
        "id": 6, "name": "唐艳", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、组织部部长、社会工作部部长", "current_org": "中共什邡市委组织部",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113387.htm"
    },
    {   # 市委常委、政法委书记
        "id": 7, "name": "王愉", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-11", "birthplace": "四川绵竹",
        "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、市委政法委书记、市政府党组成员", "current_org": "中共什邡市委政法委员会",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/ffc/10098696.htm"
    },
    {   # 市委常委、统战部部长
        "id": 8, "name": "李成忠", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、市委统战部部长、市总工会主席", "current_org": "中共什邡市委统一战线工作部",
        "source": "https://www.shifang.gov.cn/gk/dtxx/xwdt/gzdt/yw/10113111.htm"
    },
    {   # 市委常委、副市长
        "id": 9, "name": "李轶", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-08", "birthplace": "",
        "education": "省委党校研究生 管理学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市委常委、市政府副市长", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/ffc/10098732.htm"
    },
    # ═══ Other Deputy Mayors ═══
    {
        "id": 10, "name": "伍曾魁", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-07", "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市政府副市长", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/ffc/10098796.htm"
    },
    {
        "id": 11, "name": "黄昌波", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-10", "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市政府副市长、市公安局党委书记、局长", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/ffc/10000612.htm"
    },
    {
        "id": 12, "name": "蔡昭霞", "gender": "女", "ethnicity": "汉族",
        "birth": "1982-11", "birthplace": "四川什邡",
        "education": "省委党校研究生",
        "party_join": "民革党员", "work_start": "2006-08",
        "current_post": "什邡市政府副市长", "current_org": "什邡市人民政府",
        "source": "https://www.shifang.gov.cn/gk/jgxx/ldjbg/fzfld/ffc/3000029.htm"
    },
    # ═══ NPC (人大) ═══
    {
        "id": 13, "name": "何学军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市人大常委会主任", "current_org": "什邡市人大常委会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113452.htm"
    },
    {
        "id": 14, "name": "孙顺斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市人大常委会副主任", "current_org": "什邡市人大常委会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113341.htm"
    },
    {
        "id": 15, "name": "卿尚发", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市人大常委会副主任", "current_org": "什邡市人大常委会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113341.htm"
    },
    {
        "id": 16, "name": "陈川儒", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市人大常委会副主任", "current_org": "什邡市人大常委会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113341.htm"
    },
    {
        "id": 17, "name": "陈述荣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市人大常委会副主任", "current_org": "什邡市人大常委会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113341.htm"
    },
    # ═══ CPPCC (政协) ═══
    {
        "id": 18, "name": "黄剑", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "什邡市政协主席", "current_org": "政协什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113445.htm"
    },
    {
        "id": 19, "name": "杨兵", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "什邡市政协副主席", "current_org": "政协什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113445.htm"
    },
    {
        "id": 20, "name": "魏远", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "什邡市政协副主席", "current_org": "政协什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113445.htm"
    },
    {
        "id": 21, "name": "喻敏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "什邡市政协副主席", "current_org": "政协什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/ywsb/sfyw/10113445.htm"
    },
    {
        "id": 22, "name": "袁秀丽", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "什邡市政协副主席", "current_org": "政协什邡市委员会",
        "source": "https://www.shifang.gov.cn/gk/dtxx/xwsb/gzdt/yw/10113228.htm"
    },
    # ═══ Previous Leaders ═══
    {
        "id": 23, "name": "王洪", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（曾任什邡市委书记）", "current_org": "",
        "source": "(前期报告推断)"
    },
]

# Use person_a key for relationships
relationships = [
    # 党政一把手搭档
    {"a": 1, "b": 2, "type": "党政搭档",
     "context": "晏世莹为什邡市委书记，叶科为什邡市长、市委副书记",
     "overlap_org": "中共什邡市委员会", "overlap_period": "2025-今"},
    {"a": 1, "b": 3, "type": "上下级",
               "context": "晏世莹为市委书记，丁斌为专职副书记", "overlap_org": "中共什邡市委员会", "overlap_period": ""},
    # 前任-现任书记
    {"a": 23, "b": 1, "type": "前后任",
               "context": "王洪为前任什邡市委书记，晏世莹为现任", "overlap_org": "中共什邡市委员会", "overlap_period": ""},
    # 常委同僚
    {"a": 4, "b": 9, "type": "同僚",
               "context": "同为市委常委、副市长", "overlap_org": "什邡市人民政府", "overlap_period": ""},
    {"a": 4, "b": 7, "type": "同僚",
               "context": "杨益（常务）与王愉（政法委书记）同为市委常委", "overlap_org": "中共什邡市委员会", "overlap_period": ""},
    {"a": 5, "b": 1, "type": "监督关系",
               "context": "市纪委书记监督市委常委会", "overlap_org": "中共什邡市委员会", "overlap_period": ""},
    # 同乡
    {"a": 7, "b": 23, "type": "同乡",
               "context": "王愉为绵竹人，王洪原任绵竹市领导（待核实）", "overlap_org": "", "overlap_period": ""},
]

organizations = [
    {"id": 1, "name": "中共什邡市委员会", "type": "党委", "level": "县级", "parent": "中共德阳市委", "location": "四川省什邡市"},
    {"id": 2, "name": "什邡市人民政府", "type": "政府", "level": "县级", "parent": "德阳市人民政府", "location": "四川省什邡市"},
    {"id": 3, "name": "什邡市纪委监委", "type": "党委", "level": "县级", "parent": "德阳市纪委监委", "location": "四川省什邡市"},
    {"id": 4, "name": "中共什邡市委组织部", "type": "党委", "level": "县级", "parent": "中共什邡市委员会", "location": "四川省什邡市"},
    {"id": 5, "name": "中共什邡市委政法委", "type": "党委", "level": "县级", "parent": "中共什邡市委员会", "location": "四川省什邡市"},
    {"id": 6, "name": "什邡市人大常委会", "type": "人大", "level": "县级", "location": "四川省什邡市"},
    {"id": 7, "name": "政协什邡市委员会", "type": "政协", "level": "县级", "location": "四川省什邡市"},
    {"id": 8, "name": "什邡市公安局", "type": "政府", "level": "县级", "location": "四川省什邡市"},
]

positions = [
    # 市委
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "今", "rank": "正处级"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "今", "rank": "正处级"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "今", "rank": "副处级"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start": "", "end": "今"},
    # 市政府
    {"person_id": 2, "org_id": 2, "title": "市长、党组书记", "start": "", "end": "今"},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start": "", "end": "今"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "今"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "今"},
    {"person_id": 11, "org_id": 2, "title": "副市长、公安局局长", "start": "", "end": "今"},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "", "end": "今"},
    # 纪委
    {"person_id": 5, "org_id": 3, "title": "市纪委书记、市监委主任", "start": "", "end": "今"},
    # 组织部
    {"person_id": 6, "org_id": 4, "title": "市委组织部部长、社会工作部部长", "start": "", "end": "今"},
    # 政法委
    {"person_id": 7, "org_id": 5, "title": "市委政法委书记", "start": "", "end": "今"},
    # 人大
    {"person_id": 13, "org_id": 6, "title": "市人大常委会主任", "start": "", "end": "今"},
    {"person_id": 14, "org_id": 6, "title": "市人大常委会副主任", "start": "", "end": "今"},
    {"person_id": 15, "org_id": 6, "title": "市人大常委会副主任", "start": "", "end": "今"},
    {"person_id": 16, "org_id": 6, "title": "市人大常委会副主任", "start": "", "end": "今"},
    {"person_id": 17, "org_id": 6, "title": "市人大常委会副主任", "start": "", "end": "今"},
    # 政协
    {"person_id": 18, "org_id": 7, "title": "市政协主席", "start": "", "end": "今"},
    {"person_id": 19, "org_id": 7, "title": "市政协副主席", "start": "", "end": "今"},
    {"person_id": 20, "org_id": 7, "title": "市政协副主席", "start": "", "end": "今"},
    {"person_id": 21, "org_id": 7, "title": "市政协副主席", "start": "", "end": "今"},
    {"person_id": 22, "org_id": 7, "title": "市政协副主席", "start": "", "end": "今"},
    # 公安局
    {"person_id": 11, "org_id": 8, "title": "党委书记、局长", "start": "", "end": "今"},
    # Previous leaders
    {"person_id": 23, "org_id": 1, "title": "市委书记", "start": "2019", "end": "2025", "rank": "正处级"},
]




# ── BUILD SQLITE DB ──────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id, name, gender, ethnicity, birth, birthplace, education,
        party_join, work_start, current_post, current_org, source
    );
    CREATE TABLE IF NOT EXISTS organizations (
        id, name, type, level, parent, location
    );
    CREATE TABLE IF NOT EXISTS positions (
        person_id, org_id, title, start, end, rank, note
    );
    CREATE TABLE IF NOT EXISTS relationships (
        person_a, person_b, type, context, overlap_org, overlap_period
    );
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"],
                 p["birth"], p["birthplace"], p["education"],
                 p["party_join"], p["work_start"],
                 p["current_post"], p.get("current_org", ""),
                 p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"],
                 o.get("parent", ""), o.get("location", "")))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?)""",
                (pos["person_id"], pos["org_id"], pos["title"],
                 pos.get("start", ""), pos.get("end", ""),
                 pos.get("rank", ""), ""))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?)""",
                (r["a"], r["b"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary
cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
psc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
conn.close()
print(f"SQLite DB written: {DB_PATH}")
print(f"  Persons: {pc}, Organizations: {oc}, Positions: {psc}, Relationships: {rc}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network / Sisyphus</creator>')
lines.append(f'    <description>什邡市领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# Nodes: Persons
lines.append('    <nodes>')
for p in persons:
    pid = p["id"]
    if pid == 1:
        color = (224, 60, 49)  # red: Party Secretary
        size = 20.0
    elif pid == 2:
        color = (41, 128, 185)  # blue: government leader
        size = 18.0
    elif pid == 23:
        color = (230, 126, 34)  # orange: former leader
        size = 14.0
    elif pid in [5]:
        color = (230, 126, 34)  # orange: discipline
        size = 14.0
    elif pid in [13, 18]:
        color = (155, 89, 182)  # purple: NPC/CPPCC head
        size = 14.0
    else:
        color = (149, 165, 166)  # grey: others
        size = 12.0

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# Nodes: Organizations
org_colors = {
    1: (200, 50, 50),    # 党委
    2: (70, 130, 200),   # 政府
    3: (200, 100, 50),   # 纪委
    6: (100, 180, 180),  # 人大
    7: (200, 180, 100),  # 政协
}
for o in organizations:
    pid = 1000 + o["id"]
    c = org_colors.get(o["id"], (200, 200, 200))
    lines.append(f'      <node id="{pid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 1

# person→organization (worked_at)
for pos in positions:
    pid = pos["person_id"]
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{eid}" source="{pid}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos.get("start", "?")} → {pos.get("end", "今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    eid += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{eid}" source="{r["a"]}" target="{r["b"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r["overlap_period"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {total_nodes}")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relations = {total_edges}")
print("\nDone!")