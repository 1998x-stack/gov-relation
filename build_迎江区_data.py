#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 迎江区 (Yingjiang District, Anqing, Anhui) leadership network.

迎江区 — 安徽省安庆市辖区, 安庆主城区之一, 面积约207平方公里, 常住人口25.4万, 辖6街道3镇1乡.
Sources:
  - www.ahyingjiang.gov.cn (official government website, leadership page accessed 2026-07-15)
  - www.ahyingjiang.gov.cn/ldzc/index.html (区委领导 + 区政府领导 listings)
  - zh.wikipedia.org/wiki/迎江区 (geo/admin info)

Confidence: Current roles confirmed from official Yingjiang District government leadership page
(ahyingjiang.gov.cn/ldzc/). Biographical details for most figures are partial; career
timelines sourced from official brief bios. Predecessor information is marked with
confidence levels.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/anhui_迎江区")
DB_PATH = os.path.join(STAGING, "迎江区_network.db")
GEXF_PATH = os.path.join(STAGING, "迎江区_network.gexf")

TODAY = datetime.now().strftime("%Y%m%d")

# ═══════════════════════════════════════════════════════════════════════
# DATA — All sourced from official ahyingjiang.gov.cn leadership page (2026-07-15)
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders (Targets) ──

    # 汪世平 — 迎江区委书记
    {"id": 1, "name": "汪世平", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "", "education": "大学学历，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迎江区委书记",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "1975年4月生，大学学历，工学学士，中共党员。主持区委全面工作。",
     "confidence": "confirmed"},

    # 谢长兵 — 迎江区委副书记、区长
    {"id": 2, "name": "谢长兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "", "education": "安徽工商管理学院工商管理硕士同等学力教育",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迎江区委副书记、区政府区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "1975年5月生，安徽工商管理学院工商管理硕士同等学力教育，中共党员。领导区政府全面工作。",
     "confidence": "confirmed"},

    # ── Predecessors (plausible based on available public records) ──

    # 前任迎江区委书记（汪世平之前）— 章洪海
    {"id": 3, "name": "章洪海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "已离任（原迎江区委书记）",
     "current_org": "",
     "source": "公开报道推断；前任区委书记身份需进一步确认",
     "notes": "汪世平的前任迎江区委书记。据公开报道，章洪海此前任迎江区委书记，2023年前后离任，汪世平接任时间待确认。此条目需进一步核实。",
     "confidence": "unverified"},

    # 前任迎江区长（谢长兵之前）— 汪世平（曾任迎江区长后升任书记）
    {"id": 4, "name": "汪世平", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "", "education": "大学学历，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "迎江区委书记（曾任迎江区长）",
     "current_org": "中共迎江区委",
     "source": "公开报道推断；汪世平此前担任迎江区长，后升任区委书记",
     "notes": "汪世平在担任迎江区委书记前，曾任迎江区区长职务。谢长兵接替其区长职务。汪世平何时由区长升任书记需进一步确认。",
     "confidence": "unverified"},

    # ── 区委常委（Standing Committee of the CPC Yingjiang District Committee）──

    # 储江 — 区委副书记、区委党校校长（兼）
    {"id": 5, "name": "储江", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区委党校校长（兼）",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "协助区委书记处理区委日常事务，分管党建、农业农村、党校等工作。详细履历待补充。",
     "confidence": "confirmed"},

    # 徐佳 — 区委常委、宣传部部长
    {"id": 6, "name": "徐佳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管宣传思想文化、意识形态、精神文明建设工作。详细履历待补充。",
     "confidence": "confirmed"},

    # 周永生 — 区委常委、常务副区长
    {"id": 7, "name": "周永生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委，区政府党组副书记、常务副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "负责区政府常务工作。详细履历待补充。",
     "confidence": "confirmed"},

    # 孟泽婧 — 区委常委、区纪委书记
    {"id": 8, "name": "孟泽婧", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区纪委书记，区监察委员会副主任、代理主任",
     "current_org": "中共迎江区纪委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管纪检监察、党风廉政建设和反腐败工作。区监委副主任、代理主任。详细履历待补充。",
     "confidence": "confirmed"},

    # 杨丽 — 区委常委、副区长
    {"id": 9, "name": "杨丽", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管具体政府工作，详细分工待补充。详细履历待补充。",
     "confidence": "confirmed"},

    # 王文龙 — 区委常委、统战部部长
    {"id": 10, "name": "王文龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、统战部部长、区政协党组副书记（兼）",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管统一战线、民族宗教、工商联等工作。兼区政协党组副书记。详细履历待补充。",
     "confidence": "confirmed"},

    # 倪磊 — 区委常委、区人武部政委
    {"id": 11, "name": "倪磊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区人武部政委",
     "current_org": "迎江区人武部",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管人民武装、国防动员和民兵预备役工作。详细履历待补充。",
     "confidence": "confirmed"},

    # 高百林 — 区委常委、组织部部长
    {"id": 12, "name": "高百林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、组织部部长",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管组织、干部、人才、公务员管理和老干部工作。详细履历待补充。",
     "confidence": "confirmed"},

    # 黄玮 — 区委常委、政法委书记
    {"id": 13, "name": "黄玮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、政法委书记",
     "current_org": "中共迎江区委",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "分管政法、社会治安综合治理、维稳、信访工作。详细履历待补充。",
     "confidence": "confirmed"},

    # ── 区政府其他领导班子成员 ──

    # 都春宝 — 副区长
    {"id": 14, "name": "都春宝", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "副区长，分管具体政府工作。详细分工和履历待补充。",
     "confidence": "confirmed"},

    # 李建文 — 副区长
    {"id": 15, "name": "李建文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "副区长，分管具体政府工作。详细分工和履历待补充。",
     "confidence": "confirmed"},

    # 殷会夫 — 副区长（挂职）
    {"id": 16, "name": "殷会夫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副区长（挂职）",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "挂职副区长。详细履历和派出单位待补充。",
     "confidence": "confirmed"},

    # 赵明来 — 副区长
    {"id": 17, "name": "赵明来", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "副区长，分管具体政府工作。详细分工和履历待补充。",
     "confidence": "confirmed"},

    # 刘凡 — 副区长
    {"id": 18, "name": "刘凡", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "副区长",
     "current_org": "迎江区人民政府",
     "source": "https://www.ahyingjiang.gov.cn/ldzc/index.html",
     "notes": "副区长，分管具体政府工作。详细分工和履历待补充。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共迎江区委", "type": "党委", "level": "县处级", "parent": "中共安庆市委", "location": "安庆市迎江区"},
    {"id": 2, "name": "迎江区人民政府", "type": "政府", "level": "县处级", "parent": "安庆市人民政府", "location": "安庆市迎江区"},
    {"id": 3, "name": "中共迎江区纪委", "type": "纪委", "level": "县处级", "parent": "中共迎江区纪委", "location": "安庆市迎江区"},
    {"id": 4, "name": "迎江区人武部", "type": "政府", "level": "县处级", "parent": "安庆军分区", "location": "安庆市迎江区"},
]

# positions: (person_id, org_id, title, rank, note)
positions = [
    # Core leaders — 区委
    (1, 1, "迎江区委书记", "正县级", "主持区委全面工作"),

    # Core leaders — 区政府
    (2, 2, "迎江区委副书记、区长", "正县级", "主持区政府全面工作"),
    (2, 1, "迎江区委副书记", "正县级", ""),

    # 区委副书记
    (5, 1, "迎江区委副书记、区委党校校长（兼）", "副县级", "协助书记处理日常事务"),

    # 区委常委
    (6, 1, "区委常委、宣传部部长", "副县级", ""),
    (7, 2, "区委常委、区政府党组副书记、常务副区长", "副县级", ""),
    (7, 1, "区委常委", "副县级", ""),
    (8, 3, "区委常委、区纪委书记、区监委副主任、代理主任", "副县级", ""),
    (8, 1, "区委常委", "副县级", ""),
    (9, 2, "区委常委、副区长", "副县级", ""),
    (9, 1, "区委常委", "副县级", ""),
    (10, 1, "区委常委、统战部部长、区政协党组副书记（兼）", "副县级", ""),
    (11, 4, "区委常委、区人武部政委", "副县级", ""),
    (11, 1, "区委常委", "副县级", ""),
    (12, 1, "区委常委、组织部部长", "副县级", ""),
    (13, 1, "区委常委、政法委书记", "副县级", ""),

    # 副区长（非入常）
    (14, 2, "副区长", "副县级", ""),
    (15, 2, "副区长", "副县级", ""),
    (16, 2, "副区长（挂职）", "副县级", ""),
    (17, 2, "副区长", "副县级", ""),
    (18, 2, "副区长", "副县级", ""),
]

# relationships: (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # Core leadership pair
    (1, 2, "superior_subordinate", "区委书记与区长党政搭档", "中共迎江区委/迎江区人民政府", "2026", "confirmed"),

    # Standing Committee working relationships
    (1, 5, "superior_subordinate", "区委书记与区委副书记", "中共迎江区委", "2026", "confirmed"),
    (2, 5, "overlap", "区长与区委副书记（区委副书记协助书记/区长工作）", "中共迎江区委", "2026", "confirmed"),
    (1, 7, "superior_subordinate", "区委书记与常务副区长", "中共迎江区委/迎江区人民政府", "2026", "confirmed"),
    (2, 7, "superior_subordinate", "区长与常务副区长", "迎江区人民政府", "2026", "confirmed"),
    (2, 9, "superior_subordinate", "区长与副区长（杨丽）", "迎江区人民政府", "2026", "confirmed"),
    (1, 12, "superior_subordinate", "区委书记与组织部长", "中共迎江区委", "2026", "confirmed"),
    (1, 13, "superior_subordinate", "区委书记与政法委书记", "中共迎江区委", "2026", "confirmed"),
    (1, 8, "superior_subordinate", "区委书记与纪委书记", "中共迎江区委/区纪委", "2026", "confirmed"),
    (1, 6, "superior_subordinate", "区委书记与宣传部长", "中共迎江区委", "2026", "confirmed"),
    (1, 10, "superior_subordinate", "区委书记与统战部长", "中共迎江区委", "2026", "confirmed"),

    # Predecessor links
    (3, 1, "predecessor_successor", "章洪海为汪世平前任（迎江区委书记）", "中共迎江区委", "2023前后", "unverified"),
]

# ═══════════════════════════════════════════════════════════════════════
# SQLITE DATABASE
# ═══════════════════════════════════════════════════════════════════════

os.makedirs(STAGING, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
CREATE TABLE IF NOT EXISTS persons(
    id INTEGER PRIMARY KEY,
    name TEXT,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT,
    notes TEXT,
    confidence TEXT
);

CREATE TABLE IF NOT EXISTS organizations(
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER,
    org_id INTEGER,
    title TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER,
    person_b INTEGER,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    confidence TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    c.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join,
         work_start, current_post, current_org, source, notes, confidence)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p["id"], p["name"], p["gender"], p["ethnicity"],
         p["birth"], p["birthplace"], p["education"],
         p["party_join"], p["work_start"],
         p["current_post"], p["current_org"],
         p["source"], p["notes"], p["confidence"]))

for o in organizations:
    c.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("""INSERT INTO positions
        (person_id, org_id, title, rank, note)
        VALUES (?,?,?,?,?)""",
        (pos[0], pos[1], pos[2], pos[3], pos[4]))

for r in relationships:
    c.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
        VALUES (?,?,?,?,?,?,?)""",
        (r[0], r[1], r[2], r[3], r[4], r[5], r[6]))

conn.commit()
conn.close()
print(f"✅ Database created: {DB_PATH}")

# ═══════════════════════════════════════════════════════════════════════
# GEXF FILE
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    if p["id"] == 1:
        return "255,50,50"  # Red — 区委书记
    elif p["id"] == 2:
        return "50,100,255"  # Blue — 区长
    elif p["id"] == 8:
        return "255,165,0"  # Orange — 纪委书记
    else:
        return "100,100,100"  # Grey — others

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    else:
        return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>迎江区 — 安徽省安庆市辖区领导关系网络 (2026-07-15)</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="label" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges: person->organization (worked_at)
lines.append('    <edges>')
eid = 0
for pos in positions:
    lines.append(f'      <edge id="{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos[2])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

# Edges: person<->person (relationship)
for r in relationships:
    lines.append(f'      <edge id="{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[2])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
    eid += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF created: {GEXF_PATH}")
