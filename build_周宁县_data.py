#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 周宁县 (Zhouning County, Ningde, Fujian).

Task: fujian_周宁县 — 县委书记 & 县长
Province: 福建省
City: 宁德市
Region: 周宁县
Level: 县
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17):
- 县委书记: 雷春雄 (confirmed from 宁德三下乡 news and multiple 2026 news articles)
- 代县长: 陈东越 (confirmed from 2026-07-04 周宁县人大常委会任命决定)
- 前任县委书记: 袁华军 (2020-2023, 去向未公开确认)
- 前任县长: 陈文卿 (2021-2026-07, 女, 福安人, 已辞职)

Sources:
- Baidu search results for 周宁县, 雷春雄, 陈东越, 陈文卿, 袁华军
- 东南网宁德站 (2026-07-04, 周宁县通过一批人事事项)
- 腾讯新闻: 解放思想大家谈 | 访周宁县委书记雷春雄 (2025-12-18)
- 今日头条: 福建4位代县(区)长上任 (2026-07-06)
- 汲古新知: 周宁县委书记调整 (2023-12-29)
- 网易: 2026年宁德市三下乡活动 (2026-02-08)
- 周宁县人民政府官网: www.zhouning.gov.cn (unreachable from research environment)
- fjdaily.com: 周宁县2026年第一季度招商签约活动 (2026-01-12)
- 搜狐: 周宁县领导开展生态环境保护"四下基层"调研 (2026-07-03)

Confidence: Current core leadership (雷春雄, 陈东越) confirmed.
Career details for 雷春雄 are solid from Baidu Baike and news articles.
Career details for 陈东越 available from Baidu Baike (应急管理厅 background).
前任县委书记袁华军去向未确认。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = SCRIPT_DIR
if "data/tmp" in SCRIPT_DIR:
    GOV_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
    STAGING = SCRIPT_DIR
    DB_PATH = os.path.join(STAGING, "周宁县_network.db")
    GEXF_PATH = os.path.join(STAGING, "周宁县_network.gexf")
else:
    STAGING = os.path.join(GOV_ROOT, "data", "tmp", "fujian_周宁县")
    DB_PATH = os.path.join(GOV_ROOT, "data", "database", "周宁县_network.db")
    GEXF_PATH = os.path.join(GOV_ROOT, "data", "graph", "周宁县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 雷春雄
    {
        "id": "zhouning_lei_chunxiong",
        "name": "雷春雄",
        "gender": "男",
        "ethnicity": "畲族",
        "birth": "1977-09",
        "birthplace": "福建霞浦",
        "native_place": "福建霞浦",
        "education": "在职研究生学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "周宁县委书记",
        "current_org": "中共周宁县委员会",
        "source": "百度百科周宁县词条, 腾讯新闻(2025-12-18), 汲古新知(2023-12-29)",
        "notes": "2023年12月起任周宁县委书记。此前历任宁德市委办公室秘书四科科长、寿宁县委副书记兼组织部长、"
             "福安市委副书记、宁德市民政局党组书记局长、宁德市革命老根据地建设委员会办公室主任、"
             "宁德市委副秘书长兼办公室主任。畲族干部，在职研究生学历，经济学硕士。"
             "政府官网www.zhouning.gov.cn在调研环境下无法访问。",
        "confidence": "confirmed",
    },

    # 代县长 — 陈东越
    {
        "id": "zhouning_chen_dongyue",
        "name": "陈东越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-01",
        "birthplace": "",
        "native_place": "",
        "education": "博士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "周宁县委副书记、代县长",
        "current_org": "周宁县人民政府",
        "source": "百度百科陈东越词条, 东南网宁德站(2026-07-04), 今日头条(2026-07-06)",
        "notes": "1988年1月出生。2026年7月4日周宁县第十八届人大常委会第四十次会议任命为副县长、代理县长。"
             "此前曾任福建省应急管理厅应急指挥中心二级主任科员、一级主任科员、办公室副主任，"
             "挂职莆田市北岸经开区管委会科技副主任，周宁县七步镇党委书记，周宁县委副书记。"
             "博士研究生学历。",
        "confidence": "confirmed",
    },

    # ══════════════ Predecessors ══════════════

    # 前任县委书记 — 袁华军
    {
        "id": "zhouning_yuan_huajun",
        "name": "袁华军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "福建师范大学毕业",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "未知（已离任）",
        "current_org": "",
        "source": "汲古新知(2023-12-29), 搜狐网(2022-08-29)",
        "notes": "2020年至2023年12月任周宁县委书记。福建师范大学毕业后长期在省政府办公厅工作，"
             "期间两次到宁德市挂职。第二次挂职结束后留在宁德市工作，先后担任市政府办公室主任、"
             "福鼎市长，2020年升任周宁县委书记。2023年12月雷春雄接任后，去向未公开确认。",
        "confidence": "confirmed",
    },

    # 前任县长 — 陈文卿
    {
        "id": "zhouning_chen_wenqing",
        "name": "陈文卿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "福建福安",
        "native_place": "福建福安",
        "education": "中央党校函授学院经济管理专业（大学学历）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已辞去周宁县县长职务",
        "current_org": "",
        "source": "百度百科周宁县词条, 周宁县人民政府官网(2026-03-24常务会议), 东南网宁德站(2026-07-04)",
        "notes": "1969年9月出生，福建福安人。曾在福安市溪柄镇任党委副书记、镇长、党委书记，"
             "后任福安市政府党组成员、副市长，2017年2月任福安市委常委、副市长。"
             "2021年6月起调任周宁县委副书记、代县长，后任县长、一级调研员。"
             "福建省第十四届人大代表。2026年7月4日辞职。",
        "confidence": "confirmed",
    },

    # ══════════════ Key Deputies ══════════════

    # 原常务副县长 — 何晓建（2026年3月调任交投）
    {
        "id": "zhouning_he_xiaojian",
        "name": "何晓建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "福建周宁",
        "native_place": "福建周宁",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宁德市交通投资集团有限公司董事长",
        "current_org": "宁德市交通投资集团有限公司",
        "source": "百度百科何晓建词条, 人民网(2026-03-18), 网易(2026-04-05)",
        "notes": "1979年10月出生，福建周宁人。曾任周宁县狮城镇党委书记，2018年6月任周宁县人民政府副县长，"
             "后任周宁县委常委、常务副县长。2026年3月宁德市委组织部公示拟任市属国有企业正职，"
             "2026年4月提名为宁德市交通投资集团有限公司董事长。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": "cpc_zhouning", "name": "中共周宁县委员会", "type": "党委", "level": "县",
     "parent": "中共宁德市委员会", "location": "福建省宁德市周宁县"},
    {"id": "gov_zhouning", "name": "周宁县人民政府", "type": "政府", "level": "县",
     "parent": "宁德市人民政府", "location": "福建省宁德市周宁县"},
    {"id": "ningde_jiaotou", "name": "宁德市交通投资集团有限公司", "type": "事业单位", "level": "市属",
     "parent": "宁德市人民政府", "location": "福建省宁德市"},
]

positions = [
    # 雷春雄
    {"person_id": "zhouning_lei_chunxiong", "org_id": "cpc_zhouning",
     "title": "周宁县委书记", "start": "2023-12", "end": "present",
     "rank": "正处级", "note": "2023年12月起任现职"},
    {"person_id": "zhouning_lei_chunxiong", "org_id": "cpc_zhouning",
     "title": "周宁县人武部党委第一书记", "start": "2024-01", "end": "present",
     "rank": "正处级", "note": "兼任"},

    # 陈东越
    {"person_id": "zhouning_chen_dongyue", "org_id": "cpc_zhouning",
     "title": "周宁县委副书记", "start": "unknown", "end": "present",
     "rank": "副处级", "note": "2026年7月前已任县委副书记"},
    {"person_id": "zhouning_chen_dongyue", "org_id": "gov_zhouning",
     "title": "周宁县代县长", "start": "2026-07-04", "end": "present",
     "rank": "正处级", "note": "县政府党组书记"},

    # 袁华军（前任县委书记）
    {"person_id": "zhouning_yuan_huajun", "org_id": "cpc_zhouning",
     "title": "周宁县委书记", "start": "2020", "end": "2023-12",
     "rank": "正处级", "note": ""},

    # 陈文卿（前任县长）
    {"person_id": "zhouning_chen_wenqing", "org_id": "gov_zhouning",
     "title": "周宁县县长", "start": "2021-06", "end": "2026-07-04",
     "rank": "正处级", "note": "2021年6月任代县长，后任县长、一级调研员"},

    # 何晓建（原常务副县长）
    {"person_id": "zhouning_he_xiaojian", "org_id": "gov_zhouning",
     "title": "周宁县副县长", "start": "2018-06", "end": "2020",
     "rank": "副处级", "note": ""},
    {"person_id": "zhouning_he_xiaojian", "org_id": "gov_zhouning",
     "title": "周宁县委常委、常务副县长", "start": "2020", "end": "2026-03",
     "rank": "副处级", "note": ""},
    {"person_id": "zhouning_he_xiaojian", "org_id": "ningde_jiaotou",
     "title": "宁德市交通投资集团有限公司董事长", "start": "2026-04", "end": "present",
     "rank": "正处级", "note": "市属国企正职"},
]

relationships = [
    # 雷春雄 ↔ 陈东越（书记↔代县长，党政一把手搭档）
    {"person_a": "zhouning_lei_chunxiong", "person_b": "zhouning_chen_dongyue",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，雷春雄主持县委全面工作，陈东越主持县政府全面工作",
     "overlap_org": "中共周宁县委员会/周宁县人民政府",
     "overlap_period": "2026年7月起", "confidence": "confirmed"},

    # 雷春雄 ↔ 陈文卿（书记↔县长，此前搭档）
    {"person_a": "zhouning_lei_chunxiong", "person_b": "zhouning_chen_wenqing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，2023年12月雷春雄到任后与陈文卿搭班子至2026年7月",
     "overlap_org": "中共周宁县委员会/周宁县人民政府",
     "overlap_period": "2023年12月至2026年7月", "confidence": "confirmed"},

    # 袁华军 ↔ 陈文卿（前任书记↔县长）
    {"person_a": "zhouning_yuan_huajun", "person_b": "zhouning_chen_wenqing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，袁华军任县委书记期间陈文卿任县长",
     "overlap_org": "中共周宁县委员会/周宁县人民政府",
     "overlap_period": "2021年至2023年12月", "confidence": "confirmed"},

    # 雷春雄 ↔ 何晓建（书记↔常务副县长）
    {"person_a": "zhouning_lei_chunxiong", "person_b": "zhouning_he_xiaojian",
     "type": "superior_subordinate", "strength": "medium",
     "context": "县委书记与常务副县长工作关系",
     "overlap_org": "周宁县人民政府",
     "overlap_period": "2023年12月至2026年3月", "confidence": "confirmed"},

    # 何晓建（周宁人）↔ 雷春雄（霞浦人）— 跨县但同在宁德系统
    {"person_a": "zhouning_lei_chunxiong", "person_b": "zhouning_he_xiaojian",
     "type": "same_system", "strength": "weak",
     "context": "同在宁德市党政系统工作多年，雷春雄在宁德市委办、市民政局等市直机关，何晓建在周宁县",
     "overlap_org": "宁德市党政系统",
     "overlap_period": "2018年起", "confidence": "plausible"},
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
             p.get("education", ""), p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p.get("notes", ""), p["confidence"]))

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
    if "县委书记" in current:
        return "255,50,50"
    if "县长" in current or "副县长" in current or "常务副" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "县委书记" in current or "县长" in current


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
    lines.append('    <description>周宁县领导班子工作关系网络 — 中共周宁县委员会、周宁县人民政府</description>')
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
