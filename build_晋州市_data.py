#!/usr/bin/env python3
"""
晋州市政府领导班子工作关系网络数据库和GEXF图生成脚本。

晋州市是河北省石家庄市下辖的县级市。
现状领导层（截至2026-07-23）：
- 市委书记: （待确认 - 未找到公开来源确认现任）
- 市长: 王林（晋州市委副书记、市长，开发区党工委副书记、管委会主任）
  王林，男，汉族，1980年1月生，中共党员，全日制大学学历。
  来源：晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202105/31/af49898b-cb32-4caa-87c5-76a27ad5e1ff.html

本脚本生成：
- data/database/晋州市_network.db (SQLite数据库)
- data/graph/晋州市_network.gexf (Gephi用的GEXF图)
"""
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = BASE_DIR

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "晋州市_network.db"
GEXF_REL = "晋州市_network.gexf"

DB_PATH = os.path.join(STAGING_DIR, DB_REL)
GEXF_PATH = os.path.join(STAGING_DIR, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "王林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "待查",
        "education": "全日制大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "晋州市委副书记、市长，开发区党工委副书记、管委会主任",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202105/31/af49898b-cb32-4caa-87c5-76a27ad5e1ff.html ; 晋州市2026年政府工作报告（王林代表市政府作报告） http://www.jzs.gov.cn/columns/5a2872b8-0f52-48a0-afaa-87c1a2723b80/202603/10/dd75a198-6fb7-40a9-9c49-391984c96efc.html",
    },
    {
        "id": 2,
        "name": "王涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "晋州市委常委、常务副市长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202306/25/928cbd32-c606-4230-a846-ced5e0be2e70.html",
    },
    {
        "id": 3,
        "name": "刘峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "（待确认）",
        "work_start": "待查",
        "current_post": "晋州市副市长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202103/25/aa844223-04c2-44c1-96d0-911d5e06ecb3.html",
    },
    {
        "id": 4,
        "name": "冀涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "（待确认）",
        "work_start": "待查",
        "current_post": "晋州市副市长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202306/25/4f6bc379-7a2e-41eb-8072-51500bc7353f.html",
    },
    {
        "id": 5,
        "name": "吉占芳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "晋州市副市长、公安局局长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202408/05/b7367e72-8521-4ddf-b17a-fc8ff71ecfe3.html",
    },
    {
        "id": 6,
        "name": "陈建民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "（待确认）",
        "work_start": "待查",
        "current_post": "晋州市副市长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202412/03/f077f5d6-9994-4bef-acb5-44e08646e167.html",
    },
    {
        "id": 7,
        "name": "曹晔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "（待确认）",
        "work_start": "待查",
        "current_post": "晋州市副市长",
        "current_org": "晋州市人民政府",
        "source": "晋州市人民政府官网领导之窗 http://www.jzs.gov.cn/columns/160fbcba-1a01-4f3e-add6-1e838a2b14e9/202306/25/bab44445-d051-4729-a0e6-96061cd50331.html",
    },
    # ---- 市委书记（待确认）----
    {
        "id": 8,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "晋州市委书记（待确认）",
        "current_org": "中共晋州市委员会",
        "source": "⚠️ 待确认：晋州市政府官网领导之窗仅列出政府领导，未列出市委领导。公开报道中未出现市委书记姓名。",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共晋州市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市晋州市",
    },
    {
        "id": 2,
        "name": "晋州市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市晋州市",
    },
    {
        "id": 3,
        "name": "晋州经济开发区",
        "type": "政府",
        "level": "县级市",
        "parent": "晋州市人民政府",
        "location": "河北省石家庄市晋州市",
    },
]

positions = [
    # 王林 — 市长
    {
        "id": 1,
        "person_id": 1,
        "org_id": 2,
        "title": "晋州市委副书记、市长",
        "start": "（最迟2021年任市长）",
        "end": "",
        "rank": "县处级正职",
        "note": "现任晋州市委副书记、市长，开发区党工委副书记、管委会主任。1980年1月生，全日制大学学历。2026年2月9日在晋州市第八届人大第六次会议上作政府工作报告。",
    },
    # 王涛 — 常务副市长
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "晋州市委常委、常务副市长",
        "start": "（最迟2023年任此职）",
        "end": "",
        "rank": "县处级副职",
        "note": "负责市政府常务工作。分管发改、财政、环保、人社、自然资源、应急、统计、数据和政务服务等。",
    },
    # 刘峰
    {
        "id": 3,
        "person_id": 3,
        "org_id": 2,
        "title": "晋州市副市长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "负责科技和工信、市场监管、商务、投资促进、项目建设。",
    },
    # 冀涛
    {
        "id": 4,
        "person_id": 4,
        "org_id": 2,
        "title": "晋州市副市长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "负责教育、卫生健康、文化旅游、体育、医疗保障。",
    },
    # 吉占芳
    {
        "id": 5,
        "person_id": 5,
        "org_id": 2,
        "title": "晋州市副市长、公安局局长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "负责公安、民政、司法、退役军人、民族宗教。",
    },
    # 陈建民
    {
        "id": 6,
        "person_id": 6,
        "org_id": 2,
        "title": "晋州市副市长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "负责住建、城市管理、交通运输、征收拆迁。",
    },
    # 曹晔
    {
        "id": 7,
        "person_id": 7,
        "org_id": 2,
        "title": "晋州市副市长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "负责农业农村、乡村振兴、水利、供销。",
    },
    # 市委书记（待确认）
    {
        "id": 8,
        "person_id": 8,
        "org_id": 1,
        "title": "晋州市委书记（待确认）",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "⚠️ 待确认：公开资料尚未确认现任晋州市委书记的姓名。2026年7月15日石家庄市委书记张超超到晋州调研检查，晋州市负责同志陪同但报道未点名。",
    },
]

relationships = [
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政搭档",
        "context": "王林（市长）与王涛（常务副市长）为晋州市政府正副职搭档关系",
        "overlap_org": "晋州市人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 8,
        "type": "党政搭档",
        "context": "王林（市委副书记、市长）与市委书记为晋州市党政正职搭档关系（市委书记待确认）",
        "overlap_org": "晋州市",
        "overlap_period": "现任",
    },
]


# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    post = post or ""
    if "书记" in post and ("市委" in post or "党委" in post) and "副书记" not in post and "纪委" not in post:
        return "230,50,50"
    if "市长" in post or "区长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "副书记" in post:
        return "180,60,180"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    if "人大" in post or "政协" in post:
        return "220,160,40"
    return "120,120,120"


def ocolor_viz(otype):
    return {"党委": "255,200,200", "政府": "200,200,255"}.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)",
                  (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                   pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships VALUES(?,?,?,?,?,?,?)",
                  (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>晋州市领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post", ""))
        sz = "20.0" if p["id"] == 1 else "15.0" if p["id"] == 8 else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c_val = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start", "")), ("2", pos.get("end", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("晋州市 Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    import sys
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
