#!/usr/bin/env python3
"""
岭东区（黑龙江省双鸭山市）领导班子工作关系网络 — 2026-07-24
Build script for Lingdong District, Shuangyashan City, Heilongjiang Province.

Data sources:
- 双鸭山市人民政府官网 https://www.shuangyashan.gov.cn/ — city-level leadership info
- Lingdong District government website (URL pattern: lingdong.gov.cn or sub-page under shuangyashan.gov.cn)
- Various local news outlets and Baidu Baike entries

TASK: heilongjiang_岭东区
"""

import json
import os
import sqlite3
from datetime import datetime

TODAY = "2026-07-24"
AS_OF = TODAY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.normpath(os.path.join(BASE_DIR, "..", "..", ".."))
STAGING = BASE_DIR
DB_PATH = os.path.join(STAGING, "岭东区_network.db")
GEXF_PATH = os.path.join(STAGING, "岭东区_network.gexf")
PERSONS_DIR = STAGING

# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(role):
    if role is None:
        role = ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "区长" in role and "副" not in role:
        return "40,100,220"
    if "副区长" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role:
        return "220,160,40"
    if "政协" in role:
        return "200,150,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role:
        return "120,120,120"
    return "160,160,160"


def person_size(role):
    if role is None:
        role = ""
    if "区委书记" in role:
        return "20.0"
    if "区长" in role and "副" not in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    if "常委" in role:
        return "14.0"
    return "12.0"


def org_color(org_type):
    if org_type is None:
        org_type = ""
    if "党委" in org_type:
        return "200,60,60"
    if "政府" in org_type or "公安" in org_type:
        return "60,100,200"
    if "人大" in org_type:
        return "200,150,40"
    if "政协" in org_type:
        return "180,130,40"
    if "纪委" in org_type:
        return "160,120,40"
    if "党委部门" in org_type:
        return "200,80,80"
    return "120,120,120"


# =========================================================================
# DATA
# =========================================================================

# ── PERSONS ──
# [id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
#  current_post, current_org, source]

PERSONS = [
    # ═══════════════════════════════════════════════════════════════════
    # TOP LEADERS
    # ═══════════════════════════════════════════════════════════════════

    # 王崇峰 — 岭东区委书记
    # Confirmed via media reports. Complete bio details pending further research.
    ["shuangyashan_lingdong_wang_chongfeng", "王崇峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "岭东区委书记",
     "中共双鸭山市岭东区委员会",
     "https://www.shuangyashan.gov.cn (岭东区委书记 as of 2023-2024; source: media reports and Baidu Baike)"],

    # 邵民学 — 岭东区委副书记、区长
    # Confirmed via media reports. Complete bio details pending further research.
    ["shuangyashan_lingdong_shao_minxue", "邵民学", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "岭东区委副书记、区长",
     "岭东区人民政府",
     "https://www.shuangyashan.gov.cn (岭东区长 as of 2023-2024; source: media reports and Baidu Baike)"],

    # ═══════════════════════════════════════════════════════════════════
    # DEPUTY LEADERS (岭东区领导班子)
    # ═══════════════════════════════════════════════════════════════════

    # 区委副书记 (推测 — 通常配有专职副书记)
    ["shuangyashan_lingdong_deputy_secretary_1", "（待查）岭东区委专职副书记", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委副书记（专职）（待确认姓名）",
     "中共双鸭山市岭东区委员会",
     "待确认 — 岭东区委领导班子成员需进一步核实"],

    # 常务副区长（推测 — 区委常委、副区长）
    ["shuangyashan_lingdong_executive_deputy_mayor", "（待查）岭东区常务副区长", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委常委、常务副区长（待确认姓名）",
     "岭东区人民政府",
     "待确认 — 岭东区政府领导班子成员需进一步核实"],

    # 纪委书记
    ["shuangyashan_lingdong_discipline_secretary", "（待查）岭东区纪委书记", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委常委、纪委书记、监委主任（待确认姓名）",
     "中共双鸭山市岭东区纪律检查委员会",
     "待确认 — 岭东区纪委监委主要领导需进一步核实"],

    # 组织部长
    ["shuangyashan_lingdong_org_minister", "（待查）岭东区委组织部部长", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委常委、组织部部长（待确认姓名）",
     "中共双鸭山市岭东区委组织部",
     "待确认 — 岭东区委组织部主要领导需进一步核实"],

    # 政法委书记
    ["shuangyashan_lingdong_politics_law", "（待查）岭东区委政法委书记", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委常委、政法委书记（待确认姓名）",
     "中共双鸭山市岭东区委政法委员会",
     "待确认 — 岭东区委政法委主要领导需进一步核实"],

    # 宣传部长
    ["shuangyashan_lingdong_propaganda_minister", "（待查）岭东区委宣传部部长", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区委常委、宣传部部长（待确认姓名）",
     "中共双鸭山市岭东区委宣传部",
     "待确认 — 岭东区委宣传部主要领导需进一步核实"],

    # 副区长若干名
    ["shuangyashan_lingdong_vice_mayor_1", "（待查）岭东区副区长1", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区副区长（待确认姓名及分工）",
     "岭东区人民政府",
     "待确认 — 岭东区政府领导班子成员需进一步核实"],

    ["shuangyashan_lingdong_vice_mayor_2", "（待查）岭东区副区长2", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区副区长（待确认姓名及分工）",
     "岭东区人民政府",
     "待确认 — 岭东区政府领导班子成员需进一步核实"],

    # ═══════════════════════════════════════════════════════════════════
    # 人大、政协
    # ═══════════════════════════════════════════════════════════════════

    ["shuangyashan_lingdong_npc_leader", "（待查）岭东区人大常委会主任", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区人大常委会主任（待确认姓名）",
     "岭东区人民代表大会常务委员会",
     "待确认"],

    ["shuangyashan_lingdong_cppcc_leader", "（待查）岭东区政协主席", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "岭东区政协主席（待确认姓名）",
     "中国人民政治协商会议双鸭山市岭东区委员会",
     "待确认"],

    # ═══════════════════════════════════════════════════════════════════
    # 前任
    # ═══════════════════════════════════════════════════════════════════

    # 王崇峰的前任区委书记 — 可能是 迟国君 或其他人
    # Need to verify
    ["shuangyashan_lingdong_prev_secretary", "（待查）岭东区委原书记（王崇峰前任）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原岭东区委书记，王崇峰前任，待确认姓名和去向）",
     "中共双鸭山市岭东区委员会（原）",
     "待确认 — 岭东区委前任书记信息需进一步核实"],

    # 邵民学的前任区长 — 可能是 王崇峰（若王崇峰曾任区长后升书记）或其他人
    ["shuangyashan_lingdong_prev_mayor", "（待查）岭东区原区长（邵民学前任）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "（原岭东区区长，邵民学前任，待确认姓名和去向）",
     "岭东区人民政府（原）",
     "待确认 — 岭东区原区长信息需进一步核实"],
]

# ── ORGANIZATIONS ──
# [id, name, type, level, parent, location]

ORGANIZATIONS = [
    ["shuangyashan_lingdong_party_committee", "中共双鸭山市岭东区委员会", "党委", "县处级",
     "中共双鸭山市委", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_gov", "岭东区人民政府", "政府", "县处级",
     "双鸭山市人民政府", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_discipline", "中共双鸭山市岭东区纪律检查委员会", "纪委", "县处级",
     "中共双鸭山市纪委", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_org_dept", "中共双鸭山市岭东区委组织部", "党委部门", "正科级",
     "中共双鸭山市岭东区委员会", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_propaganda_dept", "中共双鸭山市岭东区委宣传部", "党委部门", "正科级",
     "中共双鸭山市岭东区委员会", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_politics_law_committee", "中共双鸭山市岭东区委政法委员会", "党委部门", "正科级",
     "中共双鸭山市岭东区委员会", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_people_congress", "岭东区人民代表大会常务委员会", "人大", "县处级",
     "双鸭山市人民代表大会常务委员会", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_lingdong_cppcc", "中国人民政治协商会议双鸭山市岭东区委员会", "政协", "县处级",
     "中国人民政治协商会议双鸭山市委员会", "黑龙江省双鸭山市岭东区"],
    ["shuangyashan_city_party_committee", "中共双鸭山市委员会", "党委", "地厅级",
     "中共黑龙江省委", "黑龙江省双鸭山市"],
    ["shuangyashan_city_gov", "双鸭山市人民政府", "政府", "地厅级",
     "黑龙江省人民政府", "黑龙江省双鸭山市"],
]

# ── POSITIONS ──
# [person_id, org_id, title, start, end, rank, note]

POSITIONS = [
    # 王崇峰
    ["shuangyashan_lingdong_wang_chongfeng", "shuangyashan_lingdong_party_committee",
     "岭东区委书记", "待查", "present", "县处级",
     "confirmed as 岭东区委书记 as of 2023-2024 via media reports"],

    # 邵民学
    ["shuangyashan_lingdong_shao_minxue", "shuangyashan_lingdong_gov",
     "岭东区区长", "待查", "present", "县处级",
     "confirmed as 岭东区区长 as of 2023-2024 via media reports"],
    ["shuangyashan_lingdong_shao_minxue", "shuangyashan_lingdong_party_committee",
     "岭东区委副书记", "待查", "present", "县处级", ""],

    # 专职副书记
    ["shuangyashan_lingdong_deputy_secretary_1", "shuangyashan_lingdong_party_committee",
     "岭东区委副书记（专职）", "待查", "present", "县处级",
     "待确认姓名"],

    # 常务副区长
    ["shuangyashan_lingdong_executive_deputy_mayor", "shuangyashan_lingdong_gov",
     "岭东区委常委、常务副区长", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_executive_deputy_mayor", "shuangyashan_lingdong_party_committee",
     "岭东区委常委", "待查", "present", "副县处级", ""],

    # 纪委书记
    ["shuangyashan_lingdong_discipline_secretary", "shuangyashan_lingdong_discipline",
     "岭东区委常委、纪委书记、监委主任", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_discipline_secretary", "shuangyashan_lingdong_party_committee",
     "岭东区委常委", "待查", "present", "副县处级", ""],

    # 组织部长
    ["shuangyashan_lingdong_org_minister", "shuangyashan_lingdong_org_dept",
     "岭东区委常委、组织部部长", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_org_minister", "shuangyashan_lingdong_party_committee",
     "岭东区委常委", "待查", "present", "副县处级", ""],

    # 政法委书记
    ["shuangyashan_lingdong_politics_law", "shuangyashan_lingdong_politics_law_committee",
     "岭东区委常委、政法委书记", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_politics_law", "shuangyashan_lingdong_party_committee",
     "岭东区委常委", "待查", "present", "副县处级", ""],

    # 宣传部长
    ["shuangyashan_lingdong_propaganda_minister", "shuangyashan_lingdong_propaganda_dept",
     "岭东区委常委、宣传部部长", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_propaganda_minister", "shuangyashan_lingdong_party_committee",
     "岭东区委常委", "待查", "present", "副县处级", ""],

    # 副区长
    ["shuangyashan_lingdong_vice_mayor_1", "shuangyashan_lingdong_gov",
     "岭东区副区长", "待查", "present", "副县处级",
     "待确认姓名"],
    ["shuangyashan_lingdong_vice_mayor_2", "shuangyashan_lingdong_gov",
     "岭东区副区长", "待查", "present", "副县处级",
     "待确认姓名"],

    # 人大主任
    ["shuangyashan_lingdong_npc_leader", "shuangyashan_lingdong_people_congress",
     "岭东区人大常委会主任", "待查", "present", "县处级",
     "待确认姓名"],

    # 政协主席
    ["shuangyashan_lingdong_cppcc_leader", "shuangyashan_lingdong_cppcc",
     "岭东区政协主席", "待查", "present", "县处级",
     "待确认姓名"],
]

# ── RELATIONSHIPS ──
# [person_a, person_b, type, context, overlap_org, overlap_period]

RELATIONSHIPS = [
    # 党政搭档
    ["shuangyashan_lingdong_wang_chongfeng", "shuangyashan_lingdong_shao_minxue",
     "党政搭档", "区委书记与区长党政正职搭档", "中共岭东区委员会/岭东区人民政府",
     "待查-至今"],

    # 区领导与上下级
    ["shuangyashan_lingdong_wang_chongfeng", "shuangyashan_lingdong_deputy_secretary_1",
     "上下级关系", "区委书记与专职副书记", "中共岭东区委员会",
     "待查-至今"],
    ["shuangyashan_lingdong_wang_chongfeng", "shuangyashan_lingdong_discipline_secretary",
     "上下级关系", "区委书记与纪委书记", "中共岭东区委员会",
     "待查-至今"],
    ["shuangyashan_lingdong_shao_minxue", "shuangyashan_lingdong_executive_deputy_mayor",
     "上下级关系", "区长与常务副区长", "岭东区人民政府",
     "待查-至今"],

    # 同僚关系
    ["shuangyashan_lingdong_executive_deputy_mayor", "shuangyashan_lingdong_vice_mayor_1",
     "同僚", "同为区政府领导", "岭东区人民政府",
     "待查-至今"],
    ["shuangyashan_lingdong_executive_deputy_mayor", "shuangyashan_lingdong_vice_mayor_2",
     "同僚", "同为区政府领导", "岭东区人民政府",
     "待查-至今"],

    # 区委常委同僚
    ["shuangyashan_lingdong_discipline_secretary", "shuangyashan_lingdong_org_minister",
     "同僚", "区委常委", "中共岭东区委员会",
     "待查-至今"],
    ["shuangyashan_lingdong_org_minister", "shuangyashan_lingdong_propaganda_minister",
     "同僚", "区委常委", "中共岭东区委员会",
     "待查-至今"],
    ["shuangyashan_lingdong_politics_law", "shuangyashan_lingdong_propaganda_minister",
     "同僚", "区委常委", "中共岭东区委员会",
     "待查-至今"],
]


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")


# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append('    <description>黑龙江省双鸭山市岭东区领导班子工作关系网络</description>')
    lines.append(f'    <date>{TODAY}</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="rank" title="Rank" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[9] or ""
        birth = p[4] or ""
        c = person_color(role)
        sz = person_size(role)
        rgb = c.split(",")
        lines.append(f'      <node id="{pid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="birth" value="{esc(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        c = org_color(o[2])
        rgb = c.split(",")
        lines.append(f'      <node id="{oid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end_, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
        lines.append(f'          <attvalue for="end" value="{esc(end_ or "")}"/>')
        lines.append(f'          <attvalue for="rank" value="{esc(rank or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        a, b, typ, context, overlap_org, overlap_period = r
        is_strong = True
        cr, cg_val, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        lines.append(f'      <edge id="e{eid}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="strength" value="strong"/>')
        lines.append(f'          <attvalue for="context" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{cr}" g="{cg_val}" b="{cb}" a="0.8"/>')
        lines.append(f'        <viz:thickness value="{thickness}"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph created: {GEXF_PATH}")


# ── STATS ──

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  黑龙江省双鸭山市岭东区领导班子工作关系网络")
    print("  等级: 市辖区（县处级）")
    print(f"  生成日期: {TODAY}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\nSummary:")
    print_stats()
    print("\nDone.")
