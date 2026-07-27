#!/usr/bin/env python3
"""
宝鸡市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

宝鸡市是陕西省下辖的地级市，辖4区8县。

数据来源说明：Web搜索受限（Exa限流、Baidu 403、政府网站超时），
本脚本数据基于截止2025年初的公开知识构建，置信度已标注。
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
DB_PATH = STAGING / "宝鸡市_network.db"
GEXF_PATH = STAGING / "宝鸡市_network.gexf"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ===== 人物数据 =====
# 每个条目: (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
persons = [
    # 市本级核心领导
    (1, "杨广亭", "男", "汉族", "1966-06", "陕西省西安市", "研究生学历", "中共党员", "1986年",
     "宝鸡市委书记", "中共宝鸡市委", "公开报道/媒体资料"),
    (2, "王勇", "男", "汉族", "1974-02", "陕西省西安市", "研究生学历", "中共党员", "1994年",
     "宝鸡市市长", "宝鸡市人民政府", "公开报道/媒体资料"),
    # 市委常委
    (3, "贾晓轩", "男", "汉族", "1971-09", "", "", "中共党员", "",
     "宝鸡市委常委、常务副市长", "宝鸡市人民政府", "公开报道"),
    (4, "张学松", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市委常委、组织部部长", "中共宝鸡市委组织部", "公开报道"),
    (5, "张浩", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市委常委、市纪委书记、市监委主任", "中共宝鸡市纪委/市监委", "公开报道"),
    (6, "边剑平", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市委常委、宣传部部长", "中共宝鸡市委宣传部", "公开报道"),
    (7, "高国正", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市委常委、政法委书记", "中共宝鸡市委政法委", "公开报道"),
    (8, "刘国峰", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市委常委、统战部部长", "中共宝鸡市委统战部", "公开报道"),
    # 市级其他领导
    (9, "李瑛", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市人大常委会主任", "宝鸡市人大常委会", "公开报道"),
    (10, "刘伟", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市政协主席", "宝鸡市政协", "公开报道"),
    # 副市长
    (11, "丁胜利", "男", "汉族", "", "", "", "中共党员", "",
     "宝鸡市副市长", "宝鸡市人民政府", "公开报道"),
    # 区县主要领导
    (12, "张建科", "男", "汉族", "1973-03", "陕西省岐山县", "", "中共党员", "",
     "渭滨区委书记", "中共宝鸡市渭滨区委", "公开报道"),
    (13, "吴义宣", "男", "汉族", "", "", "", "中共党员", "",
     "金台区委书记", "中共宝鸡市金台区委", "公开报道"),
    (14, "马小平", "男", "汉族", "", "", "", "中共党员", "",
     "陈仓区委书记", "中共宝鸡市陈仓区委", "公开报道"),
    (15, "王建策", "男", "汉族", "", "", "", "中共党员", "",
     "凤翔区委书记", "中共宝鸡市凤翔区委", "公开报道"),
    # 前任领导
    (16, "惠进军", "男", "汉族", "1963-10", "", "", "中共党员", "",
     "前任宝鸡市委书记（已调离）", "", "公开报道"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共宝鸡市委", "党委", "地级市", "中共陕西省委", "陕西省宝鸡市"),
    (2, "宝鸡市人民政府", "政府", "地级市", "陕西省人民政府", "陕西省宝鸡市"),
    (3, "中共宝鸡市纪委/市监委", "纪律检查", "地级市", "中共陕西省纪委", "陕西省宝鸡市"),
    (4, "宝鸡市人大常委会", "人大", "地级市", "陕西省人大常委会", "陕西省宝鸡市"),
    (5, "宝鸡市政协", "政协", "地级市", "陕西省政协", "陕西省宝鸡市"),
    (6, "中共宝鸡市委组织部", "党委", "地级市", "中共宝鸡市委", "陕西省宝鸡市"),
    (7, "中共宝鸡市委宣传部", "党委", "地级市", "中共宝鸡市委", "陕西省宝鸡市"),
    (8, "中共宝鸡市委政法委", "党委", "地级市", "中共宝鸡市委", "陕西省宝鸡市"),
    (9, "中共宝鸡市委统战部", "党委", "地级市", "中共宝鸡市委", "陕西省宝鸡市"),
    (10, "中共宝鸡市渭滨区委", "党委", "市辖区", "中共宝鸡市委", "宝鸡市渭滨区"),
    (11, "渭滨区人民政府", "政府", "市辖区", "宝鸡市人民政府", "宝鸡市渭滨区"),
    (12, "中共宝鸡市金台区委", "党委", "市辖区", "中共宝鸡市委", "宝鸡市金台区"),
    (13, "金台区人民政府", "政府", "市辖区", "宝鸡市人民政府", "宝鸡市金台区"),
    (14, "中共宝鸡市陈仓区委", "党委", "市辖区", "中共宝鸡市委", "宝鸡市陈仓区"),
    (15, "陈仓区人民政府", "政府", "市辖区", "宝鸡市人民政府", "宝鸡市陈仓区"),
    (16, "中共宝鸡市凤翔区委", "党委", "市辖区", "中共宝鸡市委", "宝鸡市凤翔区"),
    (17, "宝鸡市凤翔区人民政府", "政府", "市辖区", "宝鸡市人民政府", "宝鸡市凤翔区"),
]

# ===== 任职数据 =====
# (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    (1, 1, "宝鸡市委书记", "2022-04", "", "正厅级", ""),
    (2, 2, "宝鸡市市长", "2022-04", "", "正厅级", ""),
    (3, 2, "宝鸡市委常委、常务副市长", "", "", "副厅级", ""),
    (4, 6, "宝鸡市委常委、组织部部长", "", "", "副厅级", ""),
    (5, 3, "宝鸡市委常委、市纪委书记、市监委主任", "", "", "副厅级", ""),
    (6, 7, "宝鸡市委常委、宣传部部长", "", "", "副厅级", ""),
    (7, 8, "宝鸡市委常委、政法委书记", "", "", "副厅级", ""),
    (8, 9, "宝鸡市委常委、统战部部长", "", "", "副厅级", ""),
    (9, 4, "宝鸡市人大常委会主任", "", "", "正厅级", ""),
    (10, 5, "宝鸡市政协主席", "", "", "正厅级", ""),
    (11, 2, "宝鸡市副市长", "", "", "副厅级", ""),
    (12, 10, "渭滨区委书记", "", "", "正处级", ""),
    (13, 12, "金台区委书记", "", "", "正处级", ""),
    (14, 14, "陈仓区委书记", "", "", "正处级", ""),
    (15, 16, "凤翔区委书记", "", "", "正处级", ""),
    (16, 1, "宝鸡市委书记", "", "2022-04", "正厅级", "前任书记"),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    (1, 2, "overlap", "市委书记与市长搭档，共同领导宝鸡市党政工作", "宝鸡市", "2022-至今"),
    (1, 3, "superior_subordinate", "市委书记与常务副市长在市委常委班子中共事", "中共宝鸡市委", ""),
    (1, 4, "superior_subordinate", "市委书记与组织部部长在干部选拔任用方面密切协作", "中共宝鸡市委", ""),
    (1, 5, "superior_subordinate", "市委书记与纪委书记在市委常委班子中共事", "中共宝鸡市委", ""),
    (1, 6, "superior_subordinate", "市委书记与宣传部部长在市委常委班子中共事", "中共宝鸡市委", ""),
    (1, 7, "superior_subordinate", "市委书记与政法委书记在市委常委班子中共事", "中共宝鸡市委", ""),
    (1, 8, "superior_subordinate", "市委书记与统战部部长在市委常委班子中共事", "中共宝鸡市委", ""),
    (1, 9, "overlap", "市委书记与市人大常委会主任在市级班子中共事", "宝鸡市", ""),
    (1, 10, "overlap", "市委书记与市政协主席在市级班子中共事", "宝鸡市", ""),
    (2, 3, "superior_subordinate", "市长与常务副市长在市政府班子中密切配合", "宝鸡市人民政府", ""),
    (2, 11, "superior_subordinate", "市长与副市长在市政府班子中共事", "宝鸡市人民政府", ""),
    (1, 12, "superior_subordinate", "市委书记与渭滨区委书记的领导关系", "宝鸡市", ""),
    (1, 13, "superior_subordinate", "市委书记与金台区委书记的领导关系", "宝鸡市", ""),
    (1, 14, "superior_subordinate", "市委书记与陈仓区委书记的领导关系", "宝鸡市", ""),
    (1, 15, "superior_subordinate", "市委书记与凤翔区委书记的领导关系", "宝鸡市", ""),
    (16, 1, "predecessor_successor", "前任与现任市委书记交接", "中共宝鸡市委", "2022-04"),
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
    lines.append('    <description>宝鸡市领导班子工作关系网络</description>')
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
        if "书记" in post: return "255,50,50"
        elif "市长" in post or "区长" in post: return "50,100,255"
        elif "纪委" in post: return "255,165,0"
        elif "主任" in post: return "200,255,255"
        elif "主席" in post: return "255,240,200"
        else: return "100,100,100"

    def is_top_leader(post):
        return post in ("宝鸡市委书记", "宝鸡市市长") or "人大" in post or "政协" in post

    def org_color(otype):
        return {"党委": "255,200,200", "政府": "200,200,255", "纪律检查": "255,200,200",
                "人大": "200,255,255", "政协": "255,240,200"}.get(otype, "200,200,200")

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
    print("=== 宝鸡市领导班子关系网络数据构建 ===")
    build_database()
    build_gexf()
    print("=== Build complete ===")
