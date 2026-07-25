#!/usr/bin/env python3
"""
渭南市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

渭南市是陕西省下辖的地级市，位于关中平原东部，辖2区7县（含韩城市）。
辖临渭区、华州区，潼关县、大荔县、合阳县、澄城县、蒲城县、白水县、富平县，
代管韩城市（副地级市）。

数据来源：渭南市政府网站 (weinan.gov.cn) 公开新闻报道、
百度百科、公开媒体报道。Web搜索受限于Exa限流和部分网站403，
部分履历信息为推测/未确认，置信度已标注。
"""

import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

STAGING = Path(__file__).parent
DB_PATH = STAGING / "渭南市_network.db"
GEXF_PATH = STAGING / "渭南市_network.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
persons = [
    # 市本级核心领导
    (1, "王浩", "男", "汉族", "", "陕西省", "",
     "中共党员", "",
     "渭南市委书记", "中共渭南市委",
     "渭南市政府网站(weinan.gov.cn) 2026年7月新闻报道确认"),

    (2, "王心", "男", "汉族", "", "陕西省", "",
     "中共党员", "",
     "渭南市委副书记、市长", "渭南市人民政府",
     "渭南市政府网站(weinan.gov.cn) 2026年7月新闻报道确认"),

    # 市委常委（根据公开报道推断，待确认完整名单）
    (3, "待查_常务副市长", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、常务副市长", "渭南市人民政府",
     "公开报道推断，具体姓名待确认"),

    (4, "待查_组织部部长", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、组织部部长", "中共渭南市委组织部",
     "公开报道推断，具体姓名待确认"),

    (5, "待查_纪委书记", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、市纪委书记、市监委主任", "中共渭南市纪委/市监委",
     "公开报道推断，具体姓名待确认"),

    (6, "待查_宣传部部长", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、宣传部部长", "中共渭南市委宣传部",
     "公开报道推断，具体姓名待确认"),

    (7, "待查_政法委书记", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、政法委书记", "中共渭南市委政法委",
     "公开报道推断，具体姓名待确认"),

    (8, "待查_统战部部长", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市委常委、统战部部长", "中共渭南市委统战部",
     "公开报道推断，具体姓名待确认"),

    # 人大、政协领导
    (9, "待查_人大常委会主任", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市人大常委会主任", "渭南市人大常委会",
     "公开报道推断，具体姓名待确认"),

    (10, "待查_政协主席", "男", "汉族", "", "", "",
     "中共党员", "",
     "渭南市政协主席", "渭南市政协",
     "公开报道推断，具体姓名待确认"),

    # 前任领导
    (11, "待查_前市委书记", "男", "汉族", "", "", "",
     "中共党员", "",
     "前任渭南市委书记（已调离）", "",
     "公开报道推断，具体姓名待确认"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共渭南市委", "党委", "地级市", "中共陕西省委", "陕西省渭南市"),
    (2, "渭南市人民政府", "政府", "地级市", "陕西省人民政府", "陕西省渭南市"),
    (3, "中共渭南市纪委/市监委", "纪律检查", "地级市", "中共陕西省纪委", "陕西省渭南市"),
    (4, "渭南市人大常委会", "人大", "地级市", "陕西省人大常委会", "陕西省渭南市"),
    (5, "渭南市政协", "政协", "地级市", "陕西省政协", "陕西省渭南市"),
    (6, "中共渭南市委组织部", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (7, "中共渭南市委宣传部", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (8, "中共渭南市委政法委", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (9, "中共渭南市委统战部", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (10, "中共渭南市委政策研究室", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (11, "中共渭南市委编办", "党委", "地级市", "中共渭南市委", "陕西省渭南市"),
    (12, "渭南高新区管委会", "开发区", "地级市", "渭南市人民政府", "陕西省渭南市"),
]

# ===== 任职数据 =====
# (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    (1, 1, "渭南市委书记", "", "", "正厅级", "2026年7月在任"),
    (2, 1, "渭南市委副书记", "", "", "正厅级", "2026年7月在任"),
    (2, 2, "渭南市市长", "", "", "正厅级", "2026年7月在任"),
    (3, 2, "渭南市委常委、常务副市长", "", "", "副厅级", ""),
    (4, 6, "渭南市委常委、组织部部长", "", "", "副厅级", ""),
    (5, 3, "渭南市委常委、市纪委书记、市监委主任", "", "", "副厅级", ""),
    (6, 7, "渭南市委常委、宣传部部长", "", "", "副厅级", ""),
    (7, 8, "渭南市委常委、政法委书记", "", "", "副厅级", ""),
    (8, 9, "渭南市委常委、统战部部长", "", "", "副厅级", ""),
    (9, 4, "渭南市人大常委会主任", "", "", "正厅级", ""),
    (10, 5, "渭南市政协主席", "", "", "正厅级", ""),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    (1, 2, "overlap", "市委书记与市长搭档，共同领导渭南市党政工作", "渭南市", "2026-至今"),
    (1, 3, "superior_subordinate", "市委书记与常务副市长在市委常委班子中共事", "中共渭南市委", ""),
    (1, 4, "superior_subordinate", "市委书记与组织部部长在干部选拔任用方面密切协作", "中共渭南市委", ""),
    (1, 5, "superior_subordinate", "市委书记与纪委书记在市委常委班子中共事", "中共渭南市委", ""),
    (1, 6, "superior_subordinate", "市委书记与宣传部部长在市委常委班子中共事", "中共渭南市委", ""),
    (1, 7, "superior_subordinate", "市委书记与政法委书记在市委常委班子中共事", "中共渭南市委", ""),
    (1, 8, "superior_subordinate", "市委书记与统战部部长在市委常委班子中共事", "中共渭南市委", ""),
    (1, 9, "overlap", "市委书记与市人大常委会主任在市级班子中共事", "渭南市", ""),
    (1, 10, "overlap", "市委书记与市政协主席在市级班子中共事", "渭南市", ""),
    (2, 3, "superior_subordinate", "市长与常务副市长在市政府班子中密切配合", "渭南市人民政府", ""),
    (2, 4, "overlap", "市长与组织部部长在市委常委会共事", "中共渭南市委", ""),
    (2, 5, "overlap", "市长与纪委书记在市委常委会共事", "中共渭南市委", ""),
    (2, 6, "overlap", "市长与宣传部部长在市委常委会共事", "中共渭南市委", ""),
    (2, 7, "overlap", "市长与政法委书记在市委常委会共事", "中共渭南市委", ""),
    (2, 8, "overlap", "市长与统战部部长在市委常委会共事", "中共渭南市委", ""),
    (2, 9, "overlap", "市长与市人大常委会主任在市级班子中共事", "渭南市", ""),
    (2, 10, "overlap", "市长与市政协主席在市级班子中共事", "渭南市", ""),
]


# ===== SQLite 构建 =====
def build_database():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=OFF")

    for t in ("relationships", "positions", "organizations", "persons"):
        conn.execute(f"DROP TABLE IF EXISTS {t}")

    conn.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '', birth TEXT DEFAULT '', birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '', party_join TEXT DEFAULT '', work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
        level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL, title TEXT DEFAULT '',
        start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '', note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id))""")
    conn.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL, type TEXT DEFAULT '', context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id))""")

    for p in persons:
        conn.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in organizations:
        conn.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in positions:
        conn.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in relationships:
        conn.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"DB ready: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
    print(f"  DB: {DB_PATH}")


# ===== GEXF 构建 =====
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>渭南市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    def person_color(post):
        if "书记" in post and "纪委" not in post:
            return "255,50,50"
        elif "市长" in post or "区长" in post:
            return "50,100,255"
        elif "纪委" in post:
            return "255,165,0"
        elif "主任" in post:
            return "200,255,255"
        elif "主席" in post:
            return "255,240,200"
        else:
            return "100,100,100"

    def is_top_leader(post):
        return any(t in post for t in ("市委书记", "市长", "人大", "政协"))

    def org_color(otype):
        return {"党委": "255,200,200", "政府": "200,200,255", "纪律检查": "255,200,200",
                "人大": "200,255,255", "政协": "255,240,200", "开发区": "200,255,200"}.get(otype, "200,200,200")

    lines.append('    <nodes>')
    for p in persons:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        r, g, b = c.split(",")
        lines.append(f'      <node id="p{pid}" label="{escape(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{escape(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{escape(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{escape(birth)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid, name, otype, level, parent, location = o
        c = org_color(otype)
        r, g, b = c.split(",")
        lines.append(f'      <node id="o{oid}" label="{escape(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{escape(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{escape(level)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{escape(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{escape(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        pa, pb, rtype, ctx, overlap_org, overlap_period = r
        eid += 1
        weight = "2.0" if rtype == "overlap" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{escape(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{escape(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{escape(ctx[:80])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF ready: {GEXF_PATH}")
    print(f"  {len(persons)} person nodes, {len(organizations)} org nodes, {eid} edges")


if __name__ == "__main__":
    print("=== 渭南市领导班子关系网络数据构建 ===")
    build_database()
    build_gexf()
    print("=== Build complete ===")
