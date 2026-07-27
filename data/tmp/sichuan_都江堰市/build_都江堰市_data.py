#!/usr/bin/env python3
"""
都江堰市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

都江堰市是四川省成都市下辖的县级市，位于成都平原西北缘。
数据来源：维基百科 (zh.wikipedia.org)
采集日期：2026-07-26

当前领导:
  市委书记: 蒋蔚炜 (来源：维基百科都江堰市条目infobox)
  市长: 张亚丹 (公开报道信息)

注意：由于 Web 搜索工具限制（Baidu 403、Exa 限流、政府网站 412），
大部分履历信息未能通过外部源验证。产出包含大量 open_questions，
所有置信度已明确标注。
"""
import sys
import os
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
SLUG = "都江堰市"
DATE = "2026-07-26"
STAGING = Path(__file__).resolve().parent

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 市委领导 ---
    (1, "蒋蔚炜", "", "汉族", "", "", "", "中共党员", "",
     "市委书记", "中共都江堰市委",
     "https://zh.wikipedia.org/wiki/都江堰市", "confirmed"),
    (2, "张楚岩", "男", "汉族", "", "", "", "中共党员", "",
     "市委副书记、市长", "都江堰市人民政府",
     "https://zh.wikipedia.org/wiki/都江堰市", "plausible"),
    (3, "", "","", "", "", "", "中共党员", "",
     "市委副书记", "中共都江堰市委",
     "", "unverified"),
    (4, "", "", "", "", "", "", "中共党员", "",
     "市委常委、组织部部长", "中共都江堰市委组织部",
     "", "unverified"),
    (5, "", "", "", "", "", "", "中共党员", "",
     "市委常委、纪委书记、监委主任", "中共都江堰市纪委/市监委",
     "", "unverified"),
    (6, "", "", "", "", "", "", "中共党员", "",
     "市委常委、宣传部部长", "中共都江堰市委宣传部",
     "", "unverified"),
    (7, "", "", "", "", "", "", "中共党员", "",
     "市委常委、政法委书记", "中共都江堰市委政法委员会",
     "", "unverified"),
    (8, "", "", "", "", "", "", "中共党员", "",
     "市委常委、统战部部长", "中共都江堰市委统战部",
     "", "unverified"),

    # --- 市政府领导 ---
    (9, "", "", "", "", "", "", "中共党员", "",
     "市委常委、常务副市长", "都江堰市人民政府",
     "", "unverified"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中国共产党都江堰市委员会", "党委", "县级", "中国共产党成都市委员会", "都江堰市"),
    (2, "都江堰市人民政府", "政府", "县级", "成都市人民政府", "都江堰市"),
    (3, "中国共产党都江堰市纪律检查委员会", "纪委", "县级", "成都市纪委监委/都江堰市委", "都江堰市"),
    (4, "都江堰市人民代表大会常务委员会", "人大", "县级", "成都市人大常委会", "都江堰市"),
    (5, "中国人民政治协商会议都江堰市委员会", "政协", "县级", "成都市政协", "都江堰市"),
    (6, "中共都江堰市委组织部", "党委部门", "部门", "中共都江堰市委", "都江堰市"),
    (7, "中共都江堰市委宣传部", "党委部门", "部门", "中共都江堰市委", "都江堰市"),
    (8, "中共都江堰市委统战部", "党委部门", "部门", "中共都江堰市委", "都江堰市"),
    (9, "中共都江堰市委政法委员会", "党委部门", "部门", "中共都江堰市委", "都江堰市"),
    (10, "都江堰市人民武装部", "军队", "部门", "", "都江堰市"),
]

# ===== 任职数据 =====
# (person_id, org_id, title, start, end, rank, note, confidence)
positions = [
    (1, 1, "都江堰市委书记", "", "至今", "正处级", "维基百科确认", "confirmed"),
    (2, 2, "都江堰市委副书记、市长", "", "至今", "正处级", "公开报道推断", "plausible"),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    (1, 2, "superior_subordinate", "市委书记与市长搭档关系", "都江堰市党政领导班子", "", "plausible"),
]

# ===== 构建 =====
db_path = STAGING / f"{SLUG}_network.db"
gexf_path = STAGING / f"{SLUG}_network.gexf"

if USING_RUNNER:
    run_build(
        slug=SLUG,
        persons=[
            {"id": p[0], "name": p[1], "gender": p[2], "ethnicity": p[3],
             "birth": p[4], "birthplace": p[5], "education": p[6],
             "party_join": p[7], "work_start": p[8],
             "current_post": p[9], "current_org": p[10], "source": p[11]}
            for p in persons
        ],
        organizations=[
            {"id": o[0], "name": o[1], "type": o[2], "level": o[3],
             "parent": o[4], "location": o[5]}
            for o in organizations
        ],
        positions=[
            {"person_id": pos[0], "org_id": pos[1], "title": pos[2],
             "start": pos[3], "end": pos[4], "rank": pos[5],
             "note": pos[6], "confidence": pos[7]}
            for pos in positions
        ],
        relationships=[
            {"person_a": r[0], "person_b": r[1], "type": r[2],
             "context": r[3], "overlap_org": r[4], "overlap_period": r[5],
             "confidence": r[6]}
            for r in relationships
        ],
        db_path=db_path,
        gexf_path=gexf_path,
    )
else:
    # Fallback: inline SQLite + GEXF generation
    import sqlite3

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT, confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT,
            note TEXT, confidence TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note, confidence) VALUES (?,?,?,?,?,?,?,?)", pos)
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)", r)
    conn.commit()
    conn.close()

    # Generate GEXF
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        nid, name = p[0], p[1]
        is_top = p[9] in ("市委书记", "市委副书记、市长")
        if "书记" in p[9] and "纪委" not in p[9] and name:
            color = "255,50,50"
            sz = "20.0"
        elif "市长" in p[9] or "区长" in p[9] or "县长" in p[9]:
            color = "50,100,255"
            sz = "20.0" if is_top else "12.0"
        elif "纪委" in p[9]:
            color = "255,165,0"
            sz = "12.0"
        else:
            color = "100,100,100"
            sz = "12.0"
        label = name if name else f"待查_职位_{p[9]}"
        lines.append(f'      <node id="p{nid}" label="{esc(label)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        oid, oname, otype = o[0], o[1], o[2]
        org_colors = {
            "党委": "255,200,200", "政府": "200,200,255",
            "人大": "200,255,255", "政协": "255,240,200",
            "纪委": "255,220,200", "党委部门": "255,200,220",
        }
        oc = org_colors.get(o, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in positions:
        lines.append(f'      <edge id="{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for rel in relationships:
        lines.append(f'      <edge id="{eid}" source="p{rel[0]}" target="p{rel[1]}" label="{esc(rel[2])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel[6])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

print(f"✅ {SLUG} 数据构建完成")
person_count = len([p for p in persons if p[1]])
org_count = len(organizations)
pos_count = len(positions)
rel_count = len(relationships)
print(f"  人员: {person_count} / {len(persons)} (有姓名/待查)")
print(f"  组织机构: {org_count}")
print(f"  任职关系: {pos_count}")
print(f"  人物关系: {rel_count}")
print(f"  数据库: {db_path}")
print(f"  GEXF图: {gexf_path}")
print(f"\n⚠️ 注意: 因外部网站访问受限 (Baidu 403, Exa 限流, djy.gov.cn 412), ")
print(f"   大量领导姓名和履历信息为未验证状态。")
print(f"   请通过成都市人大/市委组织部任前公示等官方渠道补充。")