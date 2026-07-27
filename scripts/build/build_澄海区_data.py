#!/usr/bin/env python3
"""
澄海区领导班子工作关系网络数据构建脚本
广东省汕头市澄海区 — 区委书记 & 区长
生成日期: 2026-07-22
数据来源: Wikipedia, 汕头市政府门户网站, 百度百科, 公开报道

注意: 由于网络搜索受限（Exa限流、百度百科403、Jina Reader超时），
部分信息为基于公开资料和临近区县已有调查数据的合理推断。
区委书记姓名尚未确定（待查批示: 澄海区政府网站 chenghai.gov.cn 无法访问）。
"""

import sqlite3
import os
from datetime import datetime

# ── 路径 ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "澄海区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "澄海区_network.gexf")

# ── 人员数据 ──
persons = [
    # 区长 — 陈少麟
    {
        "id": "chenghai_chen_shaolin",
        "name": "陈少麟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长",
        "current_org": "澄海区人民政府",
        "source": "Wikipedia — 澄海区词条显示区长为陈少麟; 详细履历待查"
    },
]

# 区委书记 — 待确定，添加占位节点
# 由于 chenghai.gov.cn 无法访问，区委书记信息缺失
# 待数据补充后更新

# ── 组织数据 ──
organizations = [
    {
        "id": "chenghai_party",
        "name": "中共汕头市澄海区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共汕头市委",
        "location": "汕头市澄海区"
    },
    {
        "id": "chenghai_gov",
        "name": "澄海区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "汕头市人民政府",
        "location": "汕头市澄海区"
    },
    {
        "id": "chenghai_cpc",
        "name": "澄海区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "汕头市人大常委会",
        "location": "汕头市澄海区"
    },
    {
        "id": "chenghai_ppcc",
        "name": "中国人民政治协商会议汕头市澄海区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "汕头市政协",
        "location": "汕头市澄海区"
    },
]

# ── 任职数据 ──
positions = [
    # 陈少麟 — 澄海区区长
    {"person_id": "chenghai_chen_shaolin", "org_id": "chenghai_gov", "title": "区长、区委副书记、区政府党组书记", "start": "", "end": "至今", "rank": "县处级正职", "note": "Wikipedia确认；完整到任时间和履历待补充"},
]

# ── 关系数据 ──
relationships = [
]

# ── 辅助函数 ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "区长" in title or "县长" in title or "市长" in title:
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "人大" in title:
        return "200,255,255"  # Cyan
    if "政协" in title:
        return "255,240,200"  # Cream
    return "100,100,100"      # Grey

def person_size(p):
    title = p["current_post"]
    if "书记" in title and "纪委" not in title:
        return "20.0"
    if "区长" in title or "县长" in title or "市长" in title:
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>澄海区领导班子工作关系网络 - 数据来源: Wikipedia及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="汕头市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="广东省"/>')
        lines.append('          <attvalue for="3" value="汕头市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──

def main():
    print(f"=== 澄海区网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")
    print(f"注意: 区委书记信息缺失，因澄海区政府网站(chenghai.gov.cn)无法访问且百度百科403。")
    print(f"区长陈少麟信息来自Wikipedia。请在网络恢复后补充完整数据。")

if __name__ == "__main__":
    main()
