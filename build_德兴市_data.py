#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 德兴市 (Dexing City) leadership network.

江西省上饶市德兴市 — county-level city under Shangrao City, Jiangxi Province.

Targets: 市委书记 & 市长

Current leadership (as of 2026-07, estimated):
- 德兴市委书记: 【待确认 — 杨秀福 (2021-2025在任); 可能需要确认新任书记】
- 德兴市长: 【待确认 — 陈武 (2021-2024在任); 可能需要确认现任市长】

Research note: Web access to Chinese government/Baidu sources was blocked during
investigation (2026-07-15). Leadership data is based on known appointment history
up to available knowledge cutoff. Use official sources to verify current officeholders.

Known historical chain:
- 德兴市委书记: 何金铭(~2011-2014, 被查) → 刘瑞英(2016.07-2019.08) → 郭峰(2019.08-2021.08) → 杨秀福(2021.08-~2025)
- 德兴市长: 刘瑞英(2015.02-2016.07) → 郭峰(2016.07-2019.08) → 杨秀福(2019.08-2021.08) → 陈武(2021.09-~2024)

Sources:
- CCTV news: https://news.cntv.cn (刘瑞英履历)
- Baidu Baike (access blocked during verification)
- Various news reports about 上饶市人事任免
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/jiangxi_德兴市/德兴市_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/jiangxi_德兴市/德兴市_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── Current/Recent Party Secretary (德兴市委书记) ──
    {"id": 1, "name": "杨秀福", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "江西", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德兴市委书记（~2021-）", "current_org": "中共德兴市委员会",
     "source": "综合新闻报道; 需官方确认"},

    # ── Current/Recent Mayor (德兴市长) ──
    {"id": 2, "name": "陈武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "江西", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "德兴市长（~2021-）", "current_org": "德兴市人民政府",
     "source": "综合新闻报道; 需官方确认"},

    # ── Previous Party Secretary — 刘瑞英 ──
    {"id": 3, "name": "刘瑞英", "gender": "女", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "江西瑞金?（待确认）", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原九江市委常委、组织部部长（2022年被查）", "current_org": "（原中共九江市委员会）",
     "source": "CCTV新闻: https://news.cntv.cn; 江西省纪委通报"},

    # ── Previous Party Secretary — 郭峰 ──
    {"id": 4, "name": "郭峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "江西", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原德兴市委书记", "current_org": "（原中共德兴市委员会）",
     "source": "综合新闻报道"},

    # ── Previous Party Secretary — 何金铭（被查） ──
    {"id": 5, "name": "何金铭", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "江西", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原德兴市委书记（2014年被查）", "current_org": "（原中共德兴市委员会）",
     "source": "CCTV新闻: https://news.cntv.cn"},

    # ── 常务副市长 (推定) ──
    {"id": 6, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市委常委、常务副市长", "current_org": "德兴市人民政府",
     "source": "待查"},

    # ── 纪委书记 (推定) ──
    {"id": 7, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市委常委、市纪委书记", "current_org": "中共德兴市纪律检查委员会",
     "source": "待查"},

    # ── 组织部部长 (推定) ──
    {"id": 8, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市委常委、组织部部长", "current_org": "中共德兴市委组织部",
     "source": "待查"},

    # ── 市委副书记 (推定) ──
    {"id": 9, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市委副书记", "current_org": "中共德兴市委员会",
     "source": "待查"},

    # ── 德兴市人大常委会主任 (推定) ──
    {"id": 10, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市人大常委会主任", "current_org": "德兴市人民代表大会常务委员会",
     "source": "待查"},

    # ── 德兴市政协主席 (推定) ──
    {"id": 11, "name": "【待确认】", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "德兴市政协主席", "current_org": "政协德兴市委员会",
     "source": "待查"},
]

# ═══════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共德兴市委员会", "type": "党委", "level": "县级",
     "parent": "中共上饶市委员会", "location": "江西省上饶市德兴市"},
    {"id": 2, "name": "德兴市人民政府", "type": "政府", "level": "县级",
     "parent": "上饶市人民政府", "location": "江西省上饶市德兴市"},
    {"id": 3, "name": "德兴市人民代表大会常务委员会", "type": "人大", "level": "县级",
     "parent": "上饶市人民代表大会常务委员会", "location": "江西省上饶市德兴市"},
    {"id": 4, "name": "政协德兴市委员会", "type": "政协", "level": "县级",
     "parent": "政协上饶市委员会", "location": "江西省上饶市德兴市"},
    {"id": 5, "name": "中共德兴市纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共上饶市纪律检查委员会", "location": "江西省上饶市德兴市"},
    {"id": 6, "name": "中共德兴市委组织部", "type": "党委", "level": "县级",
     "parent": "中共德兴市委员会", "location": "江西省上饶市德兴市"},
    {"id": 7, "name": "德兴市监察委员会", "type": "政府", "level": "县级",
     "parent": "上饶市监察委员会", "location": "江西省上饶市德兴市"},
    {"id": 8, "name": "中共景德镇市委员会", "type": "党委", "level": "地级",
     "parent": "中共江西省委员会", "location": "江西省景德镇市"},
    {"id": 9, "name": "中共九江市委员会", "type": "党委", "level": "地级",
     "parent": "中共江西省委员会", "location": "江西省九江市"},
    {"id": 10, "name": "德兴经济开发区", "type": "开发区", "level": "省级",
     "parent": "德兴市人民政府", "location": "江西省上饶市德兴市"},
    {"id": 11, "name": "中共上饶市委员会", "type": "党委", "level": "地级",
     "parent": "中共江西省委员会", "location": "江西省上饶市"},
    {"id": 12, "name": "上饶市人民政府", "type": "政府", "level": "地级",
     "parent": "江西省人民政府", "location": "江西省上饶市"},
]

# ═══════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════

positions = [
    # ── 杨秀福 ──
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "德兴市委书记", "start": "2021-08", "end": "",
     "rank": "正处级",
     "note": "⚠️ 推定：杨秀福此前任德兴市长，2021年8月左右接任市委书记。需官方来源确认准确日期及是否仍在任。"},
    {"id": 2, "person_id": 1, "org_id": 2,
     "title": "德兴市委副书记、市长", "start": "2019-08", "end": "2021-08",
     "rank": "正处级",
     "note": "接替郭峰任市长"},

    # ── 陈武 ──
    {"id": 3, "person_id": 2, "org_id": 2,
     "title": "德兴市委副书记、市长", "start": "2021-09", "end": "",
     "rank": "正处级",
     "note": "⚠️ 推定：杨秀福升任书记后，陈武接任市长。具体任命时间及是否仍在任需官方确认。"},

    # ── 刘瑞英 ──
    {"id": 4, "person_id": 3, "org_id": 9,
     "title": "九江市委常委、组织部部长", "start": "2021-08", "end": "2022-09",
     "rank": "副厅级",
     "note": "2022年8月被查；2023年1月被双开"},
    {"id": 5, "person_id": 3, "org_id": 8,
     "title": "景德镇市委常委、组织部部长", "start": "2019-08", "end": "2021-08",
     "rank": "副厅级", "note": ""},
    {"id": 6, "person_id": 3, "org_id": 1,
     "title": "德兴市委书记", "start": "2016-07", "end": "2019-08",
     "rank": "正处级",
     "note": "来源: CCTV新闻报道"},
    {"id": 7, "person_id": 3, "org_id": 2,
     "title": "德兴市委副书记、市长", "start": "2015-02", "end": "2016-07",
     "rank": "正处级",
     "note": "2015年2月任代市长，后任市长"},
    {"id": 8, "person_id": 3, "org_id": 5,
     "title": "（此前）上饶市纪委副书记", "start": "", "end": "2014-12",
     "rank": "副处级",
     "note": "来源: CCTV新闻"},

    # ── 郭峰 ──
    {"id": 9, "person_id": 4, "org_id": 1,
     "title": "德兴市委书记", "start": "2019-08", "end": "2021-08",
     "rank": "正处级", "note": ""},
    {"id": 10, "person_id": 4, "org_id": 2,
     "title": "德兴市委副书记、市长", "start": "2016-07", "end": "2019-08",
     "rank": "正处级", "note": "接替刘瑞英任市长"},

    # ── 何金铭 ──
    {"id": 11, "person_id": 5, "org_id": 1,
     "title": "德兴市委书记", "start": "~2011", "end": "2014-06",
     "rank": "正处级",
     "note": "2014年6月4日被调查（来源: CCTV新闻）"},
]

# ═══════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════

relationships = [
    # 杨秀福 & 陈武 — 前后任搭档
    {"id": 1, "person_a": 1, "person_b": 2,
     "type": "前后任搭档",
     "context": "杨秀福（前任书记）与陈武（市长）在德兴市党政班子共事",
     "overlap_org": "德兴市",
     "overlap_period": "2021-09至今"},

    # 刘瑞英 → 郭峰 → 杨秀福 — 书记传承链
    {"id": 2, "person_a": 3, "person_b": 4,
     "type": "前后任",
     "context": "刘瑞英升任景德镇后，郭峰接任德兴市委书记",
     "overlap_org": "德兴市",
     "overlap_period": "2019-08"},

    {"id": 3, "person_a": 4, "person_b": 1,
     "type": "前后任",
     "context": "郭峰调离后，杨秀福接任德兴市委书记",
     "overlap_org": "德兴市",
     "overlap_period": "2021-08"},

    # 刘瑞英 & 郭峰 — 党政搭档
    {"id": 4, "person_a": 3, "person_b": 4,
     "type": "党政搭档",
     "context": "刘瑞英（书记）与郭峰（市长）在德兴市党政领导班子共事",
     "overlap_org": "德兴市",
     "overlap_period": "2016-07至2019-08"},

    # 郭峰 & 杨秀福 — 党政搭档
    {"id": 5, "person_a": 4, "person_b": 1,
     "type": "党政搭档",
     "context": "郭峰（书记）与杨秀福（市长）在德兴市党政领导班子共事",
     "overlap_org": "德兴市",
     "overlap_period": "2019-08至2021-08"},

    # 何金铭（被查）— 风险信号
    {"id": 6, "person_a": 5, "person_b": 3,
     "type": "间接前后任",
     "context": "何金铭（被查前书记）与刘瑞英（后任书记）之间隔了一位代理书记",
     "overlap_org": "德兴市",
     "overlap_period": "间接"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD DATABASE
# ═══════════════════════════════════════════════════════════════════════

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
    id INTEGER PRIMARY KEY, name TEXT, type TEXT,
    level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY, person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY, person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"],
               p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

counts = {}
for table in ["persons", "organizations", "positions", "relationships"]:
    c.execute(f"SELECT COUNT(*) FROM {table}")
    counts[table] = c.fetchone()[0]
conn.close()

print(f"SQLite DB written: {DB_PATH}")
print(f"  persons={counts['persons']}, organizations={counts['organizations']}, positions={counts['positions']}, relationships={counts['relationships']}")


# ═══════════════════════════════════════════════════════════════════════
# BUILD GEXF
# ═══════════════════════════════════════════════════════════════════════

from xml.sax.saxutils import escape

edge_counter = 0

def next_edge():
    global edge_counter
    edge_counter += 1
    return f"e{edge_counter}"

# Color scheme
COLOR_PARTY_SEC = {"r": "255", "g": "50", "b": "50"}    # Red for party secretary
COLOR_GOV_LEADER = {"r": "50", "g": "100", "b": "255"}  # Blue for government leader
COLOR_DISCIPLINE = {"r": "255", "g": "165", "b": "0"}   # Orange for discipline
COLOR_PERSON_OTHER = {"r": "100", "g": "100", "b": "100"}  # Grey for others

COLOR_ORG_PARTY = {"r": "255", "g": "200", "b": "200"}   # Light pink
COLOR_ORG_GOV = {"r": "200", "g": "200", "b": "255"}     # Light blue
COLOR_ORG_DEVELOP = {"r": "200", "g": "255", "b": "200"} # Light green
COLOR_ORG_OTHER = {"r": "220", "g": "220", "b": "220"}   # Light grey
COLOR_ORG_人大 = {"r": "200", "g": "255", "b": "255"}    # Cyan
COLOR_ORG_政协 = {"r": "255", "g": "240", "b": "200"}    # Cream

def person_color(p):
    post = p.get("current_post", "")
    if "书记" in post:
        return COLOR_PARTY_SEC
    elif "市长" in post or "区长" in post:
        return COLOR_GOV_LEADER
    elif "纪委" in post:
        return COLOR_DISCIPLINE
    return COLOR_PERSON_OTHER

def org_color(o_type):
    m = {
        "党委": COLOR_ORG_PARTY,
        "政府": COLOR_ORG_GOV,
        "开发区": COLOR_ORG_DEVELOP,
        "人大": COLOR_ORG_人大,
        "政协": COLOR_ORG_政协,
    }
    return m.get(o_type, COLOR_ORG_OTHER)

def is_top_leader(p):
    return p["id"] in [1, 2, 3, 4]  # 书记、市长级别的核心人物

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'<meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('<creator>OpenCode gov-relation network builder</creator>')
lines.append('<description>德兴市领导班子工作关系网络</description>')
lines.append('</meta>')
lines.append('<graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('<attributes class="node">')
lines.append('<attribute id="type" title="Type" type="string"/>')
lines.append('<attribute id="role" title="Role" type="string"/>')
lines.append('<attribute id="birth" title="Birth" type="string"/>')
lines.append('<attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('<attribute id="education" title="Education" type="string"/>')
lines.append('</attributes>')

# Edge attributes
lines.append('<attributes class="edge">')
lines.append('<attribute id="type" title="Edge Type" type="string"/>')
lines.append('<attribute id="period" title="Period" type="string"/>')
lines.append('<attribute id="context" title="Context" type="string"/>')
lines.append('</attributes>')

# Nodes
lines.append('<nodes>')

# Person nodes
for p in persons:
    if "【待确认】" in p["name"]:
        continue  # Skip placeholder entries

    node_id = f"dexing_{p['name']}"
    label = f"{p['name']}\n{p['current_post'][:20]}"
    clr = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"

    lines.append(f'<node id="{escape(node_id)}" label="{escape(label)}">')
    lines.append('<attvalues>')
    lines.append('<attvalue for="type" value="person"/>')
    lines.append(f'<attvalue for="role" value="{escape(p["current_post"][:50])}"/>')
    lines.append(f'<attvalue for="birth" value="{p.get("birth","")}"/>')
    lines.append(f'<attvalue for="birthplace" value="{p.get("birthplace","")}"/>')
    lines.append(f'<attvalue for="education" value="{escape(p.get("education","")[:50])}"/>')
    lines.append('</attvalues>')
    lines.append(f'<viz:color r="{clr["r"]}" g="{clr["g"]}" b="{clr["b"]}" a="1"/>')
    lines.append(f'<viz:size value="{sz}"/>')
    lines.append('</node>')

# Organization nodes
for o in organizations:
    node_id = f"org_{o['id']}"
    label = o["name"]
    clr = org_color(o["type"])

    lines.append(f'<node id="{escape(node_id)}" label="{escape(label)}">')
    lines.append('<attvalues>')
    lines.append('<attvalue for="type" value="org"/>')
    lines.append(f'<attvalue for="role" value="{o["type"]} {o["level"]}"/>')
    lines.append('</attvalues>')
    lines.append(f'<viz:color r="{clr["r"]}" g="{clr["g"]}" b="{clr["b"]}" a="1"/>')
    lines.append('<viz:size value="8.0"/>')
    lines.append('</node>')

lines.append('</nodes>')

# Edges
lines.append('<edges>')

# Position edges (person -> org)
for pos in positions:
    p_name = next((p["name"] for p in persons if p["id"] == pos["person_id"]), "")
    if "【待确认】" in p_name:
        continue

    source = f"dexing_{p_name}"
    target = f"org_{pos['org_id']}"
    eid = next_edge()
    label = f"{pos['title']} ({pos['start']}-{pos['end'] if pos['end'] else '至今'})"

    lines.append(f'<edge id="{eid}" source="{escape(source)}" target="{escape(target)}" label="{escape(label)}" weight="1">')
    lines.append('<attvalues>')
    lines.append('<attvalue for="type" value="worked_at"/>')
    lines.append(f'<attvalue for="period" value="{pos["start"]}—{pos["end"] if pos["end"] else "至今"}"/>')
    lines.append(f'<attvalue for="context" value="{escape(pos.get("note","")[:150])}"/>')
    lines.append('</attvalues>')
    lines.append('</edge>')

# Relationship edges (person <-> person)
for r in relationships:
    p_a = next((p["name"] for p in persons if p["id"] == r["person_a"]), "")
    p_b = next((p["name"] for p in persons if p["id"] == r["person_b"]), "")
    if "【待确认】" in p_a or "【待确认】" in p_b:
        continue

    source = f"dexing_{p_a}"
    target = f"dexing_{p_b}"
    eid = next_edge()

    if "党政搭档" in r["type"] or "前后任搭档" in r["type"]:
        weight = "3"
    elif "前后任" in r["type"] or "搭档" in r["type"]:
        weight = "2"
    else:
        weight = "1"

    lines.append(f'<edge id="{eid}" source="{escape(source)}" target="{escape(target)}" label="{escape(r["type"])}" weight="{weight}">')
    lines.append('<attvalues>')
    lines.append('<attvalue for="type" value="relationship"/>')
    lines.append(f'<attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'<attvalue for="context" value="{escape(r["context"][:150])}"/>')
    lines.append('</attvalues>')
    lines.append('</edge>')

lines.append('</edges>')
lines.append('</graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"GEXF graph written: {GEXF_PATH}")
print("Done!")
