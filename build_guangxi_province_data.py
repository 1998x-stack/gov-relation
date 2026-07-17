#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Guangxi Province (广西壮族自治区) leadership network.
   Covers: Party Secretary (陈刚), Government Chairman (韦韬), and Standing Committee (11 members)."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/guangxi_province_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/guangxi_province_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (自治区党委书记) ──
    {"id": 1, "name": "陈刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1965-04", "birthplace": "江苏高邮", "education": "博士（北京大学无机化学）",
     "party_join": "1986-12", "work_start": "1990-08",
     "current_post": "广西壮族自治区党委书记", "current_org": "中共广西壮族自治区委员会",
     "source": "https://zh.wikipedia.org/zh-cn/%E9%99%88%E5%88%9A_(1965%E5%B9%B4)"},

    # ── Government Chairman (自治区政府主席) ──
    {"id": 2, "name": "韦韬", "gender": "男", "ethnicity": "壮族",
     "birth": "1970-04", "birthplace": "广西罗城", "education": "本科（重庆大学冶金）",
     "party_join": "1998-05", "work_start": "1992-07",
     "current_post": "广西壮族自治区党委副书记、政府主席", "current_org": "广西壮族自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E9%9F%A6%E9%9F%AC"},

    # ── Discipline Inspection Secretary (纪委书记) ──
    {"id": 3, "name": "房灵敏", "gender": "男", "ethnicity": "汉族",
     "birth": "1964-05", "birthplace": "山东郓城", "education": "研究生（西藏大学）",
     "party_join": "中共党员", "work_start": "1983-07",
     "current_post": "广西壮族自治区纪委书记、自治区监委主任", "current_org": "中共广西壮族自治区纪律检查委员会",
     "source": "https://zh.wikipedia.org/wiki/%E6%88%BF%E7%81%B5%E6%95%8F"},

    # ── Military Commander (广西军区司令员) ──
    {"id": 4, "name": "庄革", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "军事院校",
     "party_join": "中共党员", "work_start": "",
     "current_post": "广西军区司令员", "current_org": "中国人民解放军广西军区",
     "source": "https://zh.wikipedia.org/zh-cn/%E5%BA%84%E9%9D%A9",
     "note": "海军少将，2019年晋升。曾任海军参谋部规划和编制局局长。2024年1月任广西军区司令员。"},

    # ── Propaganda Department Head (宣传部部长) ──
    {"id": 5, "name": "陈奕君", "gender": "女", "ethnicity": "汉族",
     "birth": "1967-03", "birthplace": "浙江宁波", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "1985-09",
     "current_post": "广西壮族自治区党委宣传部部长", "current_org": "中共广西壮族自治区委员会宣传部",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E5%A5%95%E5%90%9B"},

    # ── Organization Department Head (组织部部长) ──
    {"id": 6, "name": "王心富", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "河南商城", "education": "博士（中国人民大学马克思主义理论）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "广西壮族自治区党委组织部部长", "current_org": "中共广西壮族自治区委员会组织部",
     "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E5%BF%83%E5%AF%8C"},

    # ── Nanning Party Secretary (南宁市委书记) ──
    {"id": 7, "name": "许永锞", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-11", "birthplace": "广东潮州", "education": "本科（北京大学地球物理）",
     "party_join": "中共党员", "work_start": "1991-07",
     "current_post": "广西壮族自治区党委常委、南宁市委书记", "current_org": "中共南宁市委员会",
     "source": "https://zh.wikipedia.org/wiki/%E8%AE%B8%E6%B0%B8%E9%94%9E"},

    # ── Executive Vice Chairman (常务副主席) ──
    {"id": 8, "name": "蔡允革", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "河北霸州", "education": "博士（重庆大学）",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "广西壮族自治区党委常委、政府常务副主席", "current_org": "广西壮族自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E8%94%A1%E5%85%81%E9%9D%A9"},

    # ── Vice Chairman (政府副主席) ──
    {"id": 9, "name": "卢新宁", "gender": "女", "ethnicity": "汉族",
     "birth": "1966-12", "birthplace": "江苏淮安", "education": "大学（北京大学中文系）",
     "party_join": "中共党员", "work_start": "1991-07",
     "current_post": "广西壮族自治区党委常委、政府副主席", "current_org": "广西壮族自治区人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%A2%E6%96%B0%E5%AE%81"},

    # ── Political-Legal Committee Secretary (政法委书记) ──
    {"id": 10, "name": "苗庆旺", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "广西壮族自治区党委政法委书记", "current_org": "中共广西壮族自治区委员会政法委员会",
     "source": "https://zh.wikipedia.org/wiki/%E8%8B%97%E5%BA%86%E6%97%BA"},

    # ── United Front Department Head (统战部部长) ──
    {"id": 11, "name": "谭丕创", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "广西贵港", "education": "研究生",
     "party_join": "中共党员", "work_start": "2003-12",
     "current_post": "广西壮族自治区党委统战部部长", "current_org": "中共广西壮族自治区委员会统战部",
     "source": "https://zh.wikipedia.org/wiki/%E8%B0%AD%E4%B8%95%E5%88%9B"},

    # ── Previously: 周异决 (秘书长, departed Feb 2026) ──
    {"id": 12, "name": "周异决", "gender": "男", "ethnicity": "壮族",
     "birth": "1965-09", "birthplace": "广西贵港", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "广西壮族自治区政协副主席", "current_org": "广西壮族自治区政协",
     "source": "https://zh.wikipedia.org/wiki/%E5%91%A8%E5%BC%82%E5%86%B3"},
]

organizations = [
    {"id": 1, "name": "中共广西壮族自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 2, "name": "广西壮族自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 3, "name": "中共广西壮族自治区纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 4, "name": "中国人民解放军广西军区", "type": "军队", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 5, "name": "中共广西壮族自治区委员会宣传部", "type": "党委部门", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 6, "name": "中共广西壮族自治区委员会组织部", "type": "党委部门", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 7, "name": "中共南宁市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 8, "name": "中共广西壮族自治区委员会政法委员会", "type": "党委部门", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 9, "name": "中共广西壮族自治区委员会统战部", "type": "党委部门", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 10, "name": "广西壮族自治区人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "广西南宁"},
    {"id": 11, "name": "广西壮族自治区政协", "type": "政协", "level": "省级", "parent": "", "location": "广西南宁"},
]

positions = [
    # 陈刚
    {"person_id": 1, "org_id": 1, "title": "广西壮族自治区党委书记", "start": "2024-12", "end": "", "rank": "正省级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "广西壮族自治区人大常委会主任", "start": "2025-01", "end": "", "rank": "正省级", "note": ""},
    # 韦韬
    {"person_id": 2, "org_id": 2, "title": "广西壮族自治区党委副书记、政府主席", "start": "2025-07", "end": "", "rank": "正省级", "note": "代理主席，2025年7月3日起"},
    # 房灵敏
    {"person_id": 3, "org_id": 3, "title": "广西壮族自治区纪委书记、监委主任", "start": "2017-09", "end": "", "rank": "副省级", "note": ""},
    # 庄革
    {"person_id": 4, "org_id": 4, "title": "广西军区司令员", "start": "2024-01", "end": "", "rank": "正军级", "note": "海军少将"},
    # 陈奕君
    {"person_id": 5, "org_id": 5, "title": "广西壮族自治区党委宣传部部长", "start": "2023-05", "end": "", "rank": "副省级", "note": ""},
    # 王心富
    {"person_id": 6, "org_id": 6, "title": "广西壮族自治区党委组织部部长", "start": "2025-05", "end": "", "rank": "副省级", "note": "此前为统战部部长"},
    # 许永锞
    {"person_id": 7, "org_id": 7, "title": "南宁市委书记", "start": "2025-12", "end": "", "rank": "副省级", "note": "兼任广西壮族自治区党委常委"},
    # 蔡允革
    {"person_id": 8, "org_id": 2, "title": "广西壮族自治区常务副主席", "start": "2026-01", "end": "", "rank": "副省级", "note": ""},
    # 卢新宁
    {"person_id": 9, "org_id": 2, "title": "广西壮族自治区副主席", "start": "2024-08", "end": "", "rank": "副省级", "note": ""},
    # 苗庆旺
    {"person_id": 10, "org_id": 8, "title": "广西壮族自治区党委政法委书记", "start": "2024-07", "end": "", "rank": "副省级", "note": ""},
    # 谭丕创
    {"person_id": 11, "org_id": 9, "title": "广西壮族自治区党委统战部部长", "start": "2025-09", "end": "", "rank": "副省级", "note": ""},
    # 周异决
    {"person_id": 12, "org_id": 11, "title": "广西壮族自治区政协副主席", "start": "2026-02", "end": "", "rank": "副省级", "note": "此前曾任自治区党委秘书长、常委"},
]

relationships = [
    # 陈刚 ↔ 韦韬 (书记+主席搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "自治区党委书记与政府主席", "overlap_org": "广西壮族自治区", "overlap_period": "2025-07至今"},
    # 陈刚 ↔ 房灵敏 (书记+纪委书记)
    {"person_a": 1, "person_b": 3, "type": "党政关系", "context": "党委书记与纪委书记", "overlap_org": "中共广西壮族自治区委员会", "overlap_period": "2024-12至今"},
    # 陈刚 ↔ 陈奕君 (同姓+前后任浙江)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "党委书记与宣传部部长", "overlap_org": "中共广西壮族自治区委员会", "overlap_period": "2024-12至今"},
    # 韦韬 ↔ 许永锞 — 同届常委
    {"person_a": 2, "person_b": 7, "type": "党政关系", "context": "政府主席与南宁市委书记", "overlap_org": "广西壮族自治区党委常委会", "overlap_period": "2025-12至今"},
    # 许永锞 ↔ 蔡允革 — 先后任常务副主席
    {"person_a": 7, "person_b": 8, "type": "前后任", "context": "许永锞此前为常务副主席，蔡允革继任", "overlap_org": "广西壮族自治区人民政府", "overlap_period": "2026-01"},
    # 陈奕君 ↔ 卢新宁 — 女性常委
    {"person_a": 5, "person_b": 9, "type": "同级", "context": "同为自治区党委女性常委", "overlap_org": "中共广西壮族自治区委员会", "overlap_period": "2024-08至今"},
    # 王心富 ↔ 谭丕创 — 前后任统战部长
    {"person_a": 6, "person_b": 11, "type": "前后任", "context": "王心富曾任统战部长，谭丕创继任", "overlap_org": "中共广西壮族自治区委员会统战部", "overlap_period": "2025-05"},
    # 韦韬 ↔ 谭丕创 — 均贵港/河池本地
    {"person_a": 2, "person_b": 11, "type": "同乡", "context": "韦韬(罗城/河池)、谭丕创(贵港)，均为广西籍常委", "overlap_org": "广西壮族自治区党委常委会", "overlap_period": "2025-09至今"},
    # 苗庆旺 ↔ 房灵敏 — 纪检系统前后辈
    {"person_a": 10, "person_b": 3, "type": "党政关系", "context": "政法委书记与纪委书记，同属党纪政法系统", "overlap_org": "广西壮族自治区党委", "overlap_period": "2024-07至今"},
    # 陈刚 ↔ 蔡允革
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "党委书记与常务副主席", "overlap_org": "广西壮族自治区党委常委会", "overlap_period": "2026-01至今"},
    # 周异决（前任常委）↔ 许永锞 — 同为党组秘书长系统
    {"person_a": 12, "person_b": 7, "type": "同级", "context": "周异决(此前常委/秘书长)与许永锞(南宁书记)", "overlap_org": "广西壮族自治区党委常委会", "overlap_period": "2025-12至2026-02"},
]

# ── BUILD: SQLite Database ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript('''
CREATE TABLE persons (
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
    current_org TEXT,
    source TEXT
);
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
''')

for p in persons:
    cur.execute('''INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                (p['id'], p['name'], p['gender'], p['ethnicity'], p['birth'],
                 p['birthplace'], p['education'], p['party_join'], p['work_start'],
                 p['current_post'], p['current_org'], p['source']))
for o in organizations:
    cur.execute('''INSERT INTO organizations VALUES (?,?,?,?,?,?)''',
                (o['id'], o['name'], o['type'], o['level'], o['parent'], o['location']))
for pos in positions:
    cur.execute('''INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                   VALUES (?,?,?,?,?,?,?)''',
                (pos['person_id'], pos['org_id'], pos['title'], pos['start'], pos['end'], pos['rank'], pos['note']))
for r in relationships:
    cur.execute('''INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                   VALUES (?,?,?,?,?,?)''',
                (r['person_a'], r['person_b'], r['type'], r['context'], r['overlap_org'], r['overlap_period']))

conn.commit()
conn.close()
print(f"[OK] SQLite -> {DB_PATH} ({len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships)")

# ── BUILD: GEXF Graph ─────────────────────────────────────────────────

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")

gexf = f'''<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta lastmodifieddate="{today}">
    <creator>gov-relation research</creator>
    <description>Guangxi Province Leadership Network - 广西壮族自治区领导班子工作关系网络</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node" mode="static">
      <attribute id="role_type" title="角色类型" type="string"/>
      <attribute id="birthplace" title="籍贯" type="string"/>
      <attribute id="ethnicity" title="民族" type="string"/>
      <attribute id="birth" title="出生" type="string"/>
      <attribute id="source" title="来源" type="string"/>
    </attributes>
    <attributes class="edge" mode="static">
      <attribute id="type" title="关系类型" type="string"/>
      <attribute id="context" title="关系描述" type="string"/>
      <attribute id="overlap_period" title="重叠期" type="string"/>
    </attributes>
    <nodes>
'''

def node_color(pid, pname):
    """Color by role: red=secretary, blue=gov, orange=discipline, green=other, grey=org"""
    if pid == 1:
        return '#E03C31', 20.0  # red - party secretary
    elif pid == 2:
        return '#2563EB', 20.0  # blue - government head
    elif pid == 3:
        return '#EA580C', 15.0  # orange - discipline
    else:
        return '#4B5563', 12.0  # grey - other

# Person nodes
for p in persons:
    c, sz = node_color(p['id'], p['name'])
    label = f"{p['name']}\\n{p['current_post']}"
    bplace = p['birthplace'] if p['birthplace'] else '未公开'
    gexf += f'''      <node id="person_{p['id']}" label="{label}">
        <attvalues>
          <attvalue for="role_type" value="person"/>
          <attvalue for="birthplace" value="{bplace}"/>
          <attvalue for="ethnicity" value="{p['ethnicity']}"/>
          <attvalue for="birth" value="{p['birth']}"/>
          <attvalue for="source" value="{p['source']}"/>
        </attvalues>
        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>
        <viz:size value="{sz}"/>
        <viz:shape value="circle"/>
      </node>
'''

# Organization nodes
for o in organizations:
    if o['type'] == '党委' or o['type'] == '党委部门':
        c = '#7C3AED'  # purple
    elif o['type'] == '政府':
        c = '#2563EB'  # blue
    elif o['type'] == '纪委':
        c = '#EA580C'  # orange
    elif o['type'] == '军队':
        c = '#059669'  # green
    else:
        c = '#6B7280'  # grey
    gexf += f'''      <node id="org_{o['id']}" label="{o['name']}">
        <attvalues>
          <attvalue for="role_type" value="organization"/>
        </attvalues>
        <viz:color r="{int(c[1:3],16)}" g="{int(c[3:5],16)}" b="{int(c[5:7],16)}"/>
        <viz:size value="8.0"/>
        <viz:shape value="square"/>
      </node>
'''

gexf += '''    </nodes>
    <edges>
'''

# Edges: person -> organization (worked_at)
edge_id = 0
for pos in positions:
    edge_id += 1
    gexf += f'''      <edge id="e{edge_id}" source="person_{pos['person_id']}" target="org_{pos['org_id']}" type="directed" weight="2.0" label="worked_at">
        <attvalues>
          <attvalue for="type" value="worked_at"/>
          <attvalue for="context" value="{pos['title']} ({pos['start']}-{pos['end'] or '至今'})"/>
        </attvalues>
      </edge>
'''

# Edges: person <-> person (relationship)
for r in relationships:
    edge_id += 1
    # Strong (gold) for overlapping leadership team, thin (grey) for general
    gexf += f'''      <edge id="e{edge_id}" source="person_{r['person_a']}" target="person_{r['person_b']}" type="undirected" weight="3.0" label="relationship">
        <attvalues>
          <attvalue for="type" value="relationship"/>
          <attvalue for="context" value="{r['type']}: {r['context']}"/>
          <attvalue for="overlap_period" value="{r['overlap_period']}"/>
        </attvalues>
      </edge>
'''

gexf += '''    </edges>
  </graph>
</gexf>'''

with open(GEXF_PATH, 'w', encoding='utf-8') as f:
    f.write(gexf)
print(f"[OK] GEXF  -> {GEXF_PATH}")

# ── Summary Stats ─────────────────────────────────────────────────────

print(f"\nSummary:")
print(f"  Persons:       {len(persons)} (incl. {sum(1 for p in persons if p['gender']=='女')} female)")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions:     {len(positions)}")
print(f"  Relationships: {len(relationships)}")
print(f"  DB file:       {os.path.getsize(DB_PATH)} bytes")
print(f"  GEXF file:     {os.path.getsize(GEXF_PATH)} bytes")
print("Done.")
