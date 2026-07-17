#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 福鼎市 (Fuding City, Ningde, Fujian).

Task: fujian_福鼎市 — 市委书记 & 市长
Province: 福建省
City: 宁德市
Region: 福鼎市
Level: 县级市
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 市委书记: 柳岳 (born 1979.08, male, Han, Fujian, in-service university)
- 市长: 叶浩文 (born 1978.08, male, Han, in-service university + MPA)
- 副市长 (2026年6月新任): 缪联华, 李修意, 陈斌

Known predecessors:
- 前任市委书记: 林青 (任至约2025年底/2026年初)
- 前任市长: 袁华军 (后任周宁县委书记 2020-2023)

Sources:
- www.fuding.gov.cn (official government site)
- www.fuding.gov.cn/dwgk/swxx/swld/ (市委领导页面)
- zh.wikipedia.org 福鼎市
- news articles on fuding.gov.cn

Confidence: Current top 2 leaders confirmed from official fuding.gov.cn sources.
Full leadership roster and career details mostly partial — marked gaps explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "data" else SCRIPT_DIR
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_福鼎市")
DB_PATH = os.path.join(STAGING, "福鼎市_network.db")
GEXF_PATH = os.path.join(STAGING, "福鼎市_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 市委书记 — 柳岳
    {
        "id": "fuding_liu_yue",
        "name": "柳岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "福建",
        "native_place": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福鼎市委书记",
        "current_org": "中共福鼎市委员会",
        "source": "fuding.gov.cn/dwgk/swxx/swld/ly/ (市委领导页面)",
        "notes": "1979年8月生，汉族。现任福鼎市委书记。曾任宁德市某职务。完整履历、此前职务待补充。",
        "confidence": "confirmed",
    },

    # 市长 — 叶浩文
    {
        "id": "fuding_ye_haowen",
        "name": "叶浩文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "",
        "native_place": "",
        "education": "在职大学学历、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福鼎市委副书记、市长",
        "current_org": "福鼎市人民政府",
        "source": "fuding.gov.cn/dwgk/swxx/swld/yhw/ (市长页面)",
        "notes": "1978年8月生，在职大学学历，公共管理硕士。现任福鼎市委副书记、市政府党组书记、市长。"
             "主持市政府全面工作。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ 副市长 (2026年6月新任) ══════════════

    # 缪联华 — 副市长
    {
        "id": "fuding_miao_lianhua",
        "name": "缪联华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福鼎市副市长",
        "current_org": "福鼎市人民政府",
        "source": "fuding.gov.cn (2026年6月25日第十八届人大常委会第四十次会议任命)",
        "notes": "2026年6月25日由福鼎市第十八届人大常委会第四十次会议决定任命为副市长。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 李修意 — 副市长
    {
        "id": "fuding_li_xiuyi",
        "name": "李修意",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福鼎市副市长",
        "current_org": "福鼎市人民政府",
        "source": "fuding.gov.cn (2026年6月25日人大常委会第四十次会议任命)",
        "notes": "2026年6月25日任命为副市长。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 陈斌 — 副市长
    {
        "id": "fuding_chen_bin",
        "name": "陈斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "福鼎市副市长",
        "current_org": "福鼎市人民政府",
        "source": "fuding.gov.cn (2026年6月25日人大常委会第四十次会议任命)",
        "notes": "2026年6月25日任命为副市长。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ 前任领导 ══════════════

    # 林青 — 前任市委书记
    {
        "id": "fuding_lin_qing",
        "name": "林青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任福鼎市委书记",
        "current_org": "",
        "source": "zh.wikipedia.org (福鼎市), news articles",
        "notes": "此前任福鼎市委书记（根据Wikipedia福鼎市词条）。2025年底或2026年初已卸任，由柳岳接替。去向待确认。",
        "confidence": "confirmed",
    },

    # 庄超和 — 前任副市长 (2025年12月免职)
    {
        "id": "fuding_zhuang_chaohe",
        "name": "庄超和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任福鼎市副市长",
        "current_org": "",
        "source": "fuding.gov.cn (市十八届人大常委会第三十五次会议决定免职 2025年12月19日)",
        "notes": "2025年12月19日由福鼎市第十八届人大常委会第三十五次会议决定免去副市长职务。去向待确认。",
        "confidence": "confirmed",
    },

    # 袁华军 — 前任市长 (后任周宁县委书记)
    {
        "id": "fuding_yuan_huajun",
        "name": "袁华军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "福建",
        "native_place": "",
        "education": "福建师范大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已卸任",
        "current_org": "",
        "source": "report/20260717-周宁县-领导班子.md",
        "notes": "福建师范大学毕业后在省政府办公厅工作，两赴宁德挂职，后任宁德市政府办公室主任、福鼎市长。"
             "2020年至2023年12月任周宁县委书记。2023年12月卸任周宁县委书记后去向未公开确认。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": "cpc_fuding", "name": "中共福鼎市委员会", "type": "党委", "level": "县级市", "parent": "中共宁德市委员会", "location": "福建省宁德市福鼎市"},
    {"id": "gov_fuding", "name": "福鼎市人民政府", "type": "政府", "level": "县级市", "parent": "宁德市人民政府", "location": "福建省宁德市福鼎市"},
    {"id": "npc_fuding", "name": "福鼎市人大常委会", "type": "人大", "level": "县级市", "parent": "", "location": "福建省宁德市福鼎市"},
    {"id": "cppcc_fuding", "name": "福鼎市政协", "type": "政协", "level": "县级市", "parent": "", "location": "福建省宁德市福鼎市"},
    {"id": "dis_fuding", "name": "中共福鼎市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共宁德市纪律检查委员会", "location": "福建省宁德市福鼎市"},
    {"id": "org_fuding", "name": "中共福鼎市委员会组织部", "type": "党委", "level": "县级市", "parent": "中共福鼎市委员会", "location": "福建省宁德市福鼎市"},
    {"id": "prop_fuding", "name": "中共福鼎市委员会宣传部", "type": "党委", "level": "县级市", "parent": "中共福鼎市委员会", "location": "福建省宁德市福鼎市"},
    {"id": "polit_fuding", "name": "中共福鼎市委员会政法委员会", "type": "党委", "level": "县级市", "parent": "中共福鼎市委员会", "location": "福建省宁德市福鼎市"},
    {"id": "psb_fuding", "name": "福鼎市公安局", "type": "政府", "level": "县级市", "parent": "福鼎市人民政府", "location": "福建省宁德市福鼎市"},
    # 乡镇/街道组织机构
    {"id": "ts_fuding", "name": "桐山街道", "type": "乡镇/街道", "level": "乡镇", "parent": "福鼎市人民政府", "location": "福建省宁德市福鼎市"},
    {"id": "tc_fuding", "name": "桐城街道", "type": "乡镇/街道", "level": "乡镇", "parent": "福鼎市人民政府", "location": "福建省宁德市福鼎市"},
    {"id": "sq_fuding", "name": "山前街道", "type": "乡镇/街道", "level": "乡镇", "parent": "福鼎市人民政府", "location": "福建省宁德市福鼎市"},
    {"id": "la_fuding", "name": "龙安街道", "type": "乡镇/街道", "level": "乡镇", "parent": "福鼎市人民政府", "location": "福建省宁德市福鼎市"},
]


positions = [
    # 柳岳
    {"person_id": "fuding_liu_yue", "org_id": "cpc_fuding", "title": "福鼎市委书记", "start": "2025", "end": "present", "rank": "正处级", "note": "主持市委全面工作"},
    # 叶浩文
    {"person_id": "fuding_ye_haowen", "org_id": "cpc_fuding", "title": "福鼎市委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "fuding_ye_haowen", "org_id": "gov_fuding", "title": "福鼎市市长", "start": "", "end": "present", "rank": "正处级", "note": "市政府党组书记，主持市政府全面工作"},
    # 缪联华
    {"person_id": "fuding_miao_lianhua", "org_id": "gov_fuding", "title": "福鼎市副市长", "start": "2026-06-25", "end": "present", "rank": "副处级", "note": "市十八届人大常委会第四十次会议任命"},
    # 李修意
    {"person_id": "fuding_li_xiuyi", "org_id": "gov_fuding", "title": "福鼎市副市长", "start": "2026-06-25", "end": "present", "rank": "副处级", "note": "市十八届人大常委会第四十次会议任命"},
    # 陈斌
    {"person_id": "fuding_chen_bin", "org_id": "gov_fuding", "title": "福鼎市副市长", "start": "2026-06-25", "end": "present", "rank": "副处级", "note": "市十八届人大常委会第四十次会议任命"},
    # 林青（前任书记）
    {"person_id": "fuding_lin_qing", "org_id": "cpc_fuding", "title": "福鼎市委书记（前任）", "start": "", "end": "2025", "rank": "正处级", "note": "卸任后由柳岳接替"},
    # 庄超和（前任副市长）
    {"person_id": "fuding_zhuang_chaohe", "org_id": "gov_fuding", "title": "福鼎市副市长（前任）", "start": "", "end": "2025-12-19", "rank": "副处级", "note": "2025年12月19日免职"},
    # 袁华军（前任市长）
    {"person_id": "fuding_yuan_huajun", "org_id": "gov_fuding", "title": "福鼎市长（前任）", "start": "", "end": "", "rank": "正处级", "note": "后任周宁县委书记"},
]


relationships = [
    # 柳岳 ↔ 叶浩文 (书记↔市长，党政一把手搭档)
    {"person_a": "fuding_liu_yue", "person_b": "fuding_ye_haowen",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，柳岳主持市委全面工作，叶浩文主持市政府全面工作",
     "overlap_org": "中共福鼎市委员会/福鼎市人民政府",
     "overlap_period": "2025年起", "confidence": "confirmed"},

    # 叶浩文 ↔ 缪联华 (市长↔副市长)
    {"person_a": "fuding_ye_haowen", "person_b": "fuding_miao_lianhua",
     "type": "superior_subordinate", "strength": "strong",
     "context": "市长与副市长的领导关系",
     "overlap_org": "福鼎市人民政府",
     "overlap_period": "2026年6月起", "confidence": "confirmed"},

    # 叶浩文 ↔ 李修意 (市长↔副市长)
    {"person_a": "fuding_ye_haowen", "person_b": "fuding_li_xiuyi",
     "type": "superior_subordinate", "strength": "strong",
     "context": "市长与副市长的领导关系",
     "overlap_org": "福鼎市人民政府",
     "overlap_period": "2026年6月起", "confidence": "confirmed"},

    # 叶浩文 ↔ 陈斌 (市长↔副市长)
    {"person_a": "fuding_ye_haowen", "person_b": "fuding_chen_bin",
     "type": "superior_subordinate", "strength": "strong",
     "context": "市长与副市长的领导关系",
     "overlap_org": "福鼎市人民政府",
     "overlap_period": "2026年6月起", "confidence": "confirmed"},

    # 林青 ↔ 柳岳 (前任书记↔现任书记)
    {"person_a": "fuding_lin_qing", "person_b": "fuding_liu_yue",
     "type": "predecessor_successor", "strength": "strong",
     "context": "林青卸任福鼎市委书记后，由柳岳接任",
     "overlap_org": "中共福鼎市委员会",
     "overlap_period": "2025（交接）", "confidence": "plausible"},

    # 袁华军 ↔ 叶浩文 (前任市长↔现任市长)
    {"person_a": "fuding_yuan_huajun", "person_b": "fuding_ye_haowen",
     "type": "predecessor_successor", "strength": "medium",
     "context": "袁华军曾任福鼎市长，后由叶浩文接任市长",
     "overlap_org": "福鼎市人民政府",
     "overlap_period": "", "confidence": "plausible"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p["education"], p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p["notes"], p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    current = p.get("current_post", "")
    if "市委书记" in current:
        return "255,50,50"
    if "市长" in current or "副市长" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "市委书记" in current or "市长" in current


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "乡镇" in t:
        return "255,255,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>福鼎市领导班子工作关系网络 — 中共福鼎市委员会、福鼎市人民政府</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for rel in relationships:
        w = "2.0" if rel.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
