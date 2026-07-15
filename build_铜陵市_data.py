#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 铜陵市 (Tongling City, Anhui) leadership network.

铜陵市 — 安徽省辖地级市, 中国古铜都.
Research date: 2026-07-15
Sources:
  - https://zh.wikipedia.org/wiki/铜陵市 (Wikipedia, accessed 2026-07-15)
  - https://zh.wikipedia.org/wiki/孔涛_(1974年) (Wikipedia biography, accessed 2026-07-15)
  - https://zh.wikipedia.org/wiki/丁纯_(1970年) (Wikipedia biography, accessed 2026-07-15)
  - https://www.tl.gov.cn/ (铜陵市人民政府官方网站, accessed 2026-07-15)
  - Wikipedia 铜陵市页面现任领导表格 (四大机构现任领导)

Confidence: Current roles confirmed from Wikipedia (铜陵市页面四大机构现任领导)
  and official government website. Biographical details for 杨宏星 are partial
  (Baidu Baike blocked from current network; Wikipedia page not created yet).
  孔涛 biography is well-documented on Wikipedia.
"""

import sqlite3
import os
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/铜陵市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/铜陵市_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ A. City-level top leadership ═══
    # Party Secretary
    {
        "id": 1,
        "name": "杨宏星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-10",
        "birthplace": "安徽长丰",
        "native_place": "安徽长丰",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共铜陵市委",
        "source": "https://zh.wikipedia.org/wiki/铜陵市 (现任领导表格); "
                 "2024年12月任铜陵市委书记。公开履历待补充。",
        "notes": "1968年10月生，安徽长丰人，汉族。2024年12月任铜陵市委书记。"
                 "前任丁纯转任黄山市委书记。",
        "confidence": "confirmed"
    },
    # Mayor
    {
        "id": 2,
        "name": "孔涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "山东烟台",
        "native_place": "山东烟台",
        "education": "大学（郑州粮食学院）/ 在职研究生 / 中国人民大学公共管理硕士",
        "party_join": "1996-03",
        "work_start": "1996-07",
        "current_post": "市委副书记、市长",
        "current_org": "铜陵市人民政府",
        "source": "https://zh.wikipedia.org/wiki/孔涛_(1974年); "
                 "https://zh.wikipedia.org/wiki/铜陵市 (现任领导表格)",
        "notes": "1974年3月生，山东烟台人。1996年3月入党，1996年7月参加工作。"
                 "历任中储粮、中国侨联、合肥市委常委/副市长、团安徽省委书记、"
                 "亳州市委副书记。2021年4月任铜陵市代市长，2021年5月当选市长。",
        "confidence": "confirmed"
    },
    # ═══ B. Predecessors ═══
    # Former Party Secretary (predecessor)
    {
        "id": 3,
        "name": "丁纯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "江苏江阴",
        "native_place": "江苏江阴",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "黄山市委书记（原铜陵市委书记2019.12-2024.12）",
        "current_org": "中共黄山市委",
        "source": "https://zh.wikipedia.org/wiki/丁纯_(1970年)",
        "notes": "1970年10月生，江苏江阴人。2017年2月-2019年12月任常州市市长，"
                 "2019年12月跨省任铜陵市委书记，2024年12月转任黄山市委书记。"
                 "第十三届全国人大代表。",
        "confidence": "confirmed"
    },
    # Former Mayor (predecessor)
    {
        "id": 4,
        "name": "胡启生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-05",
        "birthplace": "安徽桐城",
        "native_place": "安徽桐城",
        "education": "研究生/法学博士",
        "party_join": "1992-06",
        "work_start": "1993-07",
        "current_post": "原铜陵市长（2018-2021）",
        "current_org": "（原）铜陵市人民政府",
        "source": "https://zh.wikipedia.org/wiki/铜陵市 (前任领导信息)",
        "notes": "1971年5月生，安徽桐城人。2018年任铜陵市市长，"
                 "2021年由孔涛接替。后任河北省副省长、省委政法委副书记等。",
        "confidence": "confirmed"
    },
    # ═══ C. Standing Committee (市委常委会) key members ═══
    # Executive Vice Mayor (常务副市长)
    {
        "id": 5,
        "name": "吴祚麓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-11",
        "birthplace": "安徽怀宁",
        "native_place": "安徽怀宁",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席（原市委常委、常务副市长）",
        "current_org": "政协铜陵市委员会",
        "source": "https://zh.wikipedia.org/wiki/铜陵市 (现任领导表格)",
        "notes": "1968年11月生，安徽怀宁人。2026年1月任铜陵市政协主席。"
                 "曾任市委常委、常务副市长。公开履历待补充。",
        "confidence": "confirmed"
    },
    # NPC Standing Committee Chair
    {
        "id": 6,
        "name": "（空缺）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任（空缺）",
        "current_org": "铜陵市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/铜陵市 (现任领导表格)",
        "notes": "铜陵市人大常委会主任目前空缺。",
        "confidence": "confirmed"
    },
    # ═══ D. District/County leaders ═══
    # 枞阳县
    {
        "id": 7,
        "name": "杨如松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "安徽颍上",
        "native_place": "安徽颍上",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "枞阳县委书记（？ 待确认）",
        "current_org": "中共枞阳县委",
        "source": "公开报道（信息待核实）",
        "notes": "注：枞阳县委书记信息待确认。曾任枞阳县长、铜陵市副市长。",
        "confidence": "plausible"
    },
    # 铜官区
    {
        "id": 8,
        "name": "王书春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "铜官区委书记（？ 待确认）",
        "current_org": "中共铜官区委",
        "source": "公开报道（信息待核实）",
        "notes": "铜官区委书记信息待确认。",
        "confidence": "unverified"
    },
    # 义安区
    {
        "id": 9,
        "name": "姚贵平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "义安区委书记（？ 待确认）",
        "current_org": "中共义安区委",
        "source": "公开报道（信息待核实）",
        "notes": "义安区委书记信息待确认。",
        "confidence": "unverified"
    },
    # 郊区
    {
        "id": 10,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "郊区委书记（？ 待确认）",
        "current_org": "中共郊区委",
        "source": "公开报道（信息待核实）",
        "notes": "郊区委书记信息待确认。",
        "confidence": "unverified"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中国共产党铜陵市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省铜陵市铜官区"
    },
    {
        "id": 2,
        "name": "铜陵市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "安徽省人民政府",
        "location": "安徽省铜陵市铜官区"
    },
    {
        "id": 3,
        "name": "铜陵市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "铜陵市",
        "location": "安徽省铜陵市"
    },
    {
        "id": 4,
        "name": "政协铜陵市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "铜陵市",
        "location": "安徽省铜陵市"
    },
    {
        "id": 5,
        "name": "中国共产党黄山市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省黄山市"
    },
    {
        "id": 6,
        "name": "常州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "江苏省人民政府",
        "location": "江苏省常州市"
    },
    {
        "id": 7,
        "name": "中国共产主义青年团安徽省委员会",
        "type": "群团",
        "level": "省级",
        "parent": "共青团中央",
        "location": "安徽省合肥市"
    },
    {
        "id": 8,
        "name": "中共合肥市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省合肥市"
    },
    {
        "id": 9,
        "name": "中共亳州市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中国共产党安徽省委员会",
        "location": "安徽省亳州市"
    },
    {
        "id": 10,
        "name": "中共枞阳县委",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党铜陵市委员会",
        "location": "安徽省铜陵市枞阳县"
    },
    {
        "id": 11,
        "name": "中共铜官区委",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党铜陵市委员会",
        "location": "安徽省铜陵市铜官区"
    },
    {
        "id": 12,
        "name": "中共义安区委",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党铜陵市委员会",
        "location": "安徽省铜陵市义安区"
    },
    {
        "id": 13,
        "name": "中共郊区委",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党铜陵市委员会",
        "location": "安徽省铜陵市郊区"
    },
]

positions = [
    # 杨宏星
    {"id": 1, "person_id": 1, "org_id": 1, "title": "铜陵市委书记",
     "start": "2024-12", "end": "present", "rank": "正厅级",
     "note": "2024年12月任铜陵市委书记"},
    # 孔涛 - full career
    {"id": 2, "person_id": 2, "org_id": 2, "title": "铜陵市市长",
     "start": "2021-04", "end": "present", "rank": "正厅级",
     "note": "2021年4月任代市长，5月当选"},
    {"id": 3, "person_id": 2, "org_id": 9, "title": "亳州市委副书记",
     "start": "2020-07", "end": "2021-04", "rank": "副厅级",
     "note": ""},
    {"id": 4, "person_id": 2, "org_id": 7, "title": "共青团安徽省委书记",
     "start": "2017-12", "end": "2020-07", "rank": "正厅级",
     "note": ""},
    {"id": 5, "person_id": 2, "org_id": 8, "title": "合肥市委常委、副市长",
     "start": "2016", "end": "2017-12", "rank": "副厅级",
     "note": "挂职"},
    {"id": 6, "person_id": 2, "org_id": 3, "title": "中国侨联海外联谊部部长",
     "start": "unknown", "end": "2016", "rank": "正局级",
     "note": "此前任副部长（副局级）"},
    # 丁纯
    {"id": 7, "person_id": 3, "org_id": 1, "title": "铜陵市委书记",
     "start": "2019-12", "end": "2024-12", "rank": "正厅级",
     "note": ""},
    {"id": 8, "person_id": 3, "org_id": 5, "title": "黄山市委书记",
     "start": "2024-12", "end": "present", "rank": "正厅级",
     "note": ""},
    {"id": 9, "person_id": 3, "org_id": 6, "title": "常州市市长",
     "start": "2017-02", "end": "2019-12", "rank": "正厅级",
     "note": ""},
    # 胡启生
    {"id": 10, "person_id": 4, "org_id": 2, "title": "铜陵市市长",
     "start": "2018", "end": "2021-04", "rank": "正厅级",
     "note": ""},
    # 吴祚麓
    {"id": 11, "person_id": 5, "org_id": 4, "title": "铜陵市政协主席",
     "start": "2026-01", "end": "present", "rank": "正厅级",
     "note": ""},
    # District/county leaders
    {"id": 12, "person_id": 7, "org_id": 10, "title": "枞阳县委书记",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "信息待核实"},
    {"id": 13, "person_id": 8, "org_id": 11, "title": "铜官区委书记",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "信息待核实"},
    {"id": 14, "person_id": 9, "org_id": 12, "title": "义安区委书记",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "信息待核实"},
    {"id": 15, "person_id": 10, "org_id": 13, "title": "郊区委书记",
     "start": "unknown", "end": "present", "rank": "正处级",
     "note": "信息待核实"},
]

relationships = [
    # 杨宏星 — 孔涛 (top duo, current)
    {"id": 1, "person_a_id": 1, "person_b_id": 2,
     "type": "superior_subordinate",
     "context": "当前铜陵市委书记与市长搭档关系，共同领导铜陵市党政工作",
     "overlap_org": "铜陵市",
     "overlap_period": "2024-12至今"},
    # 杨宏星 — 丁纯 (predecessor/successor)
    {"id": 2, "person_a_id": 1, "person_b_id": 3,
     "type": "predecessor_successor",
     "context": "杨宏星接替丁纯任铜陵市委书记",
     "overlap_org": "中共铜陵市委",
     "overlap_period": "2024-12"},
    # 孔涛 — 胡启生 (predecessor/successor)
    {"id": 3, "person_a_id": 2, "person_b_id": 4,
     "type": "predecessor_successor",
     "context": "孔涛接替胡启生任铜陵市市长",
     "overlap_org": "铜陵市人民政府",
     "overlap_period": "2021-04"},
    # 孔涛 — 丁纯 (overlap)
    {"id": 4, "person_a_id": 2, "person_b_id": 3,
     "type": "overlap",
     "context": "孔涛（市长）与丁纯（市委书记）在铜陵搭档约3年半",
     "overlap_org": "铜陵市",
     "overlap_period": "2021-04至2024-12"},
]


# ── BUILD SQLite ────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
                   pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ─────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "市委" in p.get("current_org", ""):
        return "255,50,50"  # Red - Party Secretary
    if "市长" in post:
        return "50,100,255"  # Blue - Mayor
    if "政协" in p.get("current_org", ""):
        return "200,200,100"  # Yellow - CPPCC
    if "人大" in p.get("current_org", ""):
        return "200,255,255"  # Cyan - NPC
    return "100,100,100"  # Grey - others


def is_top_leader(p):
    post = p.get("current_post", "")
    return "书记" in post or "市长" in post


def org_color(o):
    types = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }
    return types.get(o["type"], "200,200,200")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>铜陵市（Tongling City）领导关系网络 - 安徽省地级市</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birthplace", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", ""))} - {esc(pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"  # Standard weight for relationships
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created {GEXF_PATH}")
    print(f"  Person nodes: {len(persons)}")
    print(f"  Organization nodes: {len(organizations)}")
    print(f"  Edges: {eid}")


# ── MAIN ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  铜陵市（Tongling City）领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
