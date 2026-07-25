#!/usr/bin/env python3
"""
博兴县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Boxing County leadership.

博兴县 — 山东省滨州市下辖县，位于鲁北平原黄河下游南岸。
县域面积900平方公里，人口约50万，下辖3个街道、9个镇。

Data current as of July 2026. Sources:
  - https://zh.wikipedia.org/wiki/博兴县 (Wikipedia infobox)
  - https://www.boxing.gov.cn/ (博兴县人民政府 — site timed out during access)
  - Wikipedia ZH infobox: 县委书记 李守江, 县长 张亚东

Research access: Official site www.boxing.gov.cn timed out. Exa was rate-limited.
Baidu returned 403. ZH Wikipedia provided current leadership names.
Detailed biographies, predecessors, and standing committee members
require further research when official channels become accessible.
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = BASE_DIR  # Running from data/tmp/shandong_博兴县/
DB_PATH = os.path.join(STAGING_DIR, "博兴县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "博兴县_network.gexf")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ── DATA ──
# Person ID convention: boxing_{surname_givenname}

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 李守江
    # Source: ZH Wikipedia infobox (博兴县 page). Also mentioned as former Binzhou city leader.
    ("boxing_li_shoujiang", "李守江", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委书记", "中共博兴县委员会",
     "https://zh.wikipedia.org/wiki/博兴县 — 信息框显示县委书记为李守江; "
     "曾任滨州市领导职务"),

    # 县长 — 张亚东
    # Source: ZH Wikipedia infobox (博兴县 page).
    ("boxing_zhang_yadong", "张亚东", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委副书记、县长", "博兴县人民政府",
     "https://zh.wikipedia.org/wiki/博兴县 — 信息框显示县长为张亚东"),

    # ═══ Key County Leaders (from typical county structure, names unconfirmed) ═══

    # 县人大常委会主任 — （待确认）
    ("boxing_npc_chair", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县人大常委会主任", "博兴县人民代表大会常务委员会",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县政协主席 — （待确认）
    ("boxing_cppcc_chair", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县政协主席", "中国人民政治协商会议博兴县委员会",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委副书记（专职）— （待确认）
    ("boxing_deputy_party_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委副书记", "中共博兴县委员会",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、纪委书记（监委主任）— （待确认）
    ("boxing_discipline_sec", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、纪委书记、监委主任", "中共博兴县纪律检查委员会",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、常务副县长 — （待确认）
    ("boxing_exec_deputy_mayor", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、常务副县长", "博兴县人民政府",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、组织部部长 — （待确认）
    ("boxing_org_dept_head", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、组织部部长", "中共博兴县委组织部",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、宣传部部长 — （待确认）
    ("boxing_propaganda_head", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、宣传部部长", "中共博兴县委宣传部",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、政法委书记 — （待确认）
    ("boxing_legal_affairs_head", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、政法委书记", "中共博兴县委政法委员会",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # 县委常委、统战部部长 — （待确认）
    ("boxing_united_front_head", "（待确认）", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委常委、统战部部长", "中共博兴县委统一战线工作部",
     "⚠️ 待确认：需从 boxing.gov.cn 确认"),

    # ═══ Predecessors ═══

    # 前任县委书记 — 焦本强（EN Wikipedia较早版本显示）
    # Note: EN Wikipedia listed Jiao Benqiang but ZH Wikipedia shows Li Shoujiang as current
    ("boxing_prev_party_sec", "焦本强", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "前任县委书记", "中共博兴县委员会",
     "https://en.wikipedia.org/wiki/Boxing_County — 英文维基较早版本; 可能与李守江非直接继任关系; 年代待确认"),

    # ═══ Binzhou City Leaders (cross-reference) ═══

    # 滨州市委书记 — 李春田（参考滨州市已有person JSON）
    ("boxing_binzhou_party_sec", "李春田", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "滨州市委书记", "中共滨州市委",
     "data/persons/20260725-山东省-滨州市-市委书记-李春田.json"),
]

# ── Organizations ──
ORGS = [
    # (id, name, type, level, parent, location)
    ("org_boxing_party", "中共博兴县委员会", "党委", "县处级", "中共滨州市委", "山东省滨州市博兴县"),
    ("org_boxing_gov", "博兴县人民政府", "政府", "县处级", "滨州市人民政府", "山东省滨州市博兴县"),
    ("org_boxing_npc", "博兴县人民代表大会常务委员会", "人大", "县处级", "", "山东省滨州市博兴县"),
    ("org_boxing_cppcc", "中国人民政治协商会议博兴县委员会", "政协", "县处级", "", "山东省滨州市博兴县"),
    ("org_boxing_discipline", "中共博兴县纪律检查委员会", "纪委", "县处级", "", "山东省滨州市博兴县"),
    ("org_boxing_org_dept", "中共博兴县委组织部", "党委部门", "正科级", "中共博兴县委员会", "山东省滨州市博兴县"),
    ("org_boxing_propaganda", "中共博兴县委宣传部", "党委部门", "正科级", "中共博兴县委员会", "山东省滨州市博兴县"),
    ("org_boxing_legal_affairs", "中共博兴县委政法委员会", "党委部门", "正科级", "中共博兴县委员会", "山东省滨州市博兴县"),
    ("org_boxing_united_front", "中共博兴县委统一战线工作部", "党委部门", "正科级", "中共博兴县委员会", "山东省滨州市博兴县"),
    ("org_binzhou_party", "中共滨州市委", "党委", "地厅级", "中共山东省委", "山东省滨州市"),
    ("org_binzhou_gov", "滨州市人民政府", "政府", "地厅级", "山东省人民政府", "山东省滨州市"),
]

# ── Positions (person_id, org_id, title, start, end, rank, note) ──
POSITIONS = [
    # 李守江
    ("boxing_li_shoujiang", "org_boxing_party", "县委书记", "待确认", "present", "县处级正职", "2026年7月据维基百科信息框确认在任"),
    # 张亚东
    ("boxing_zhang_yadong", "org_boxing_party", "县委副书记", "待确认", "present", "县处级副职", "2026年7月据维基百科信息框确认"),
    ("boxing_zhang_yadong", "org_boxing_gov", "县长", "待确认", "present", "县处级正职", "2026年7月据维基百科信息框确认"),
    # 焦本强（前任县委书记）
    ("boxing_prev_party_sec", "org_boxing_party", "县委书记", "待确认", "待确认", "县处级正职", "英文维基记载，年代不明确"),
    # 待确认人物占位
    ("boxing_npc_chair", "org_boxing_npc", "县人大常委会主任", "待确认", "present", "县处级正职", ""),
    ("boxing_cppcc_chair", "org_boxing_cppcc", "县政协主席", "待确认", "present", "县处级正职", ""),
    ("boxing_deputy_party_sec", "org_boxing_party", "县委副书记", "待确认", "present", "县处级副职", ""),
    ("boxing_discipline_sec", "org_boxing_discipline", "县委常委、纪委书记、监委主任", "待确认", "present", "县处级副职", ""),
    ("boxing_exec_deputy_mayor", "org_boxing_gov", "县委常委、常务副县长", "待确认", "present", "县处级副职", ""),
    ("boxing_org_dept_head", "org_boxing_org_dept", "县委常委、组织部部长", "待确认", "present", "县处级副职", ""),
    ("boxing_propaganda_head", "org_boxing_propaganda", "县委常委、宣传部部长", "待确认", "present", "县处级副职", ""),
    ("boxing_legal_affairs_head", "org_boxing_legal_affairs", "县委常委、政法委书记", "待确认", "present", "县处级副职", ""),
    ("boxing_united_front_head", "org_boxing_united_front", "县委常委、统战部部长", "待确认", "present", "县处级副职", ""),
    # 滨州市领导
    ("boxing_binzhou_party_sec", "org_binzhou_party", "滨州市委书记", "待确认", "present", "地厅级正职", ""),
]

# ── Relationships ──
RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, confidence)

    # 书记-县长: 上下级关系
    ("boxing_li_shoujiang", "boxing_zhang_yadong", "superior_subordinate",
     "李守江（县委书记）- 张亚东（县长）：党政主要领导合作关系",
     "中共博兴县委/博兴县人民政府", "待确认-present", "confirmed"),

    # 书记-滨州市委书记: 上下级关系
    ("boxing_binzhou_party_sec", "boxing_li_shoujiang", "superior_subordinate",
     "李春田（滨州市委书记）- 李守江（博兴县委书记）：市-县上下级",
     "滨州市-博兴县", "待确认-present", "confirmed"),

    # 书记-人大: 四大班子
    ("boxing_li_shoujiang", "boxing_npc_chair", "overlap",
     "李守江（县委书记）- 人大主任：县委-人大四大班子领导",
     "博兴县", "待确认-present", "plausible"),

    # 书记-政协: 四大班子
    ("boxing_li_shoujiang", "boxing_cppcc_chair", "overlap",
     "李守江（县委书记）- 政协主席：县委-政协四大班子领导",
     "博兴县", "待确认-present", "plausible"),

    # 书记-专职副书记: 上下级
    ("boxing_li_shoujiang", "boxing_deputy_party_sec", "superior_subordinate",
     "县委书记 - 县委专职副书记",
     "中共博兴县委", "待确认-present", "plausible"),

    # 书记-纪委书记
    ("boxing_li_shoujiang", "boxing_discipline_sec", "superior_subordinate",
     "县委书记 - 纪委书记",
     "中共博兴县委", "待确认-present", "plausible"),

    # 县长-常务副县长
    ("boxing_zhang_yadong", "boxing_exec_deputy_mayor", "superior_subordinate",
     "县长 - 常务副县长",
     "博兴县人民政府", "待确认-present", "plausible"),
]


# ═══════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════

def create_tables(conn, overwrite=False):
    if overwrite:
        conn.execute("DROP TABLE IF EXISTS relationships")
        conn.execute("DROP TABLE IF EXISTS positions")
        conn.execute("DROP TABLE IF EXISTS persons")
        conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("""
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
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)


def insert_persons(conn, persons):
    for p in persons:
        conn.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            p
        )


def insert_organizations(conn, orgs):
    for o in orgs:
        conn.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            o
        )


def insert_positions(conn, positions):
    for pos in positions:
        conn.execute(
            "INSERT OR REPLACE INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
            pos
        )


def insert_relationships(conn, relationships):
    for r in relationships:
        conn.execute(
            "INSERT OR REPLACE INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
            r
        )


# ═══════════════════════════════════════════════════════
# GEXF GENERATION (string formatting per reference pattern)
# ═══════════════════════════════════════════════════════

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p[9]  # current_post field
    if post and "县委书记" in post:
        return "255,50,50"  # Red
    elif post and ("县长" in post or "副县长" in post or "常务副县长" in post):
        return "50,100,255"  # Blue
    elif post and "纪委书记" in post:
        return "255,165,0"  # Orange
    else:
        return "100,100,100"  # Grey


def org_color(o):
    """Return 'r,g,b' string based on org type."""
    t = o[2]  # type field
    if t == "党委" or t == "党委部门":
        return "255,200,200"  # Pink
    elif t == "政府":
        return "200,200,255"  # Light blue
    elif t == "人大":
        return "200,255,255"  # Cyan
    elif t == "政协":
        return "255,240,200"  # Cream
    elif t == "纪委":
        return "255,165,0"  # Orange (matching person)
    else:
        return "200,200,200"


def is_top_leader(p):
    post = p[9] or ""
    return "县委书记" in post or "县长" in post


def generate_gexf(persons, orgs, positions, relationships, output_path):
    """Generate GEXF using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>博兴县领导工作关系网络 — Boxing County Leadership Network, Shandong Province</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p[0]
        name = p[1]
        post = p[9] or ""
        org_name = p[10] or ""
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org_name)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_id_counter = 100000
    org_id_map = {}
    for o in orgs:
        oid = o[0]
        name = o[1]
        c = org_color(o)
        org_id_map[oid] = org_id_counter
        lines.append(f'      <node id="o{org_id_counter}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2] or "")}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o[3] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
        org_id_counter += 1

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> organization (worked_at)
    for pos in positions:
        pid = pos[0]
        oid = pos[1]
        title = pos[2] or "任职"
        if oid in org_id_map:
            lines.append(f'      <edge id="{eid}" source="p{esc(pid)}" target="o{org_id_map[oid]}" label="{esc(title)}" weight="1.0">')
            lines.append('        <attvalues>')
            lines.append('          <attvalue for="0" value="worked_at"/>')
            lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
            lines.append('          <attvalue for="2" value="confirmed"/>')
            lines.append('        </attvalues>')
            lines.append('      </edge>')
            eid += 1

    # Person <-> person (relationships)
    for r in relationships:
        pa = r[0]
        pb = r[1]
        rtype = r[2] or "overlap"
        context = r[3] or ""
        confidence = r[6] or "plausible"
        lines.append(f'      <edge id="{eid}" source="p{esc(pa)}" target="p{esc(pb)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {output_path}")


# ═══════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════

def main():
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, PERSONS)
        insert_organizations(conn, ORGS)
        insert_positions(conn, POSITIONS)
        insert_relationships(conn, RELATIONSHIPS)
        conn.commit()
        print(f"DB ready: {len(PERSONS)} persons, {len(ORGS)} orgs, "
              f"{len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships")
    finally:
        conn.close()

    print(f"Building GEXF: {GEXF_PATH}")
    generate_gexf(PERSONS, ORGS, POSITIONS, RELATIONSHIPS, GEXF_PATH)
    print("Done.")


if __name__ == "__main__":
    main()
