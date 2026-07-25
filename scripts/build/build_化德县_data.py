#!/usr/bin/env python3
"""化德县领导班子工作关系网络数据构建脚本。

化德县 — 内蒙古自治区乌兰察布市下辖县。

调查日期: 2026-07-25
数据来源: 化德县人民政府网站 (www.huade.gov.cn)
"""

from datetime import datetime

AS_OF = "2026-07-25"
SLUG = "化德县"
DB_PATH = f"{SLUG}_network.db"
GEXF_PATH = f"{SLUG}_network.gexf"

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1. 县委书记
    {
        "id": "p1",
        "name": "薛峰青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县委书记",
        "current_org": "化德县委",
        "source": "化德县政府网站新闻报道 (2026-07)",
        "notes": "2026年7月多次以县委书记身份调研白音特拉乡、七号镇并主持县委常委会会议"
    },
    # 2. 代县长
    {
        "id": "p2",
        "name": "王永生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县委副书记、政府代县长",
        "current_org": "化德县人民政府",
        "source": "化德县政府网站 (2026-07-22 政府常务会议报道)",
        "notes": "2026年7月22日以县委副书记、政府代县长身份主持政府常务会议；代县长表明为新近任命"
    },
    # 3. 县人大常委会主任
    {
        "id": "p3",
        "name": "闫军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县人大常委会主任",
        "current_org": "化德县人大常委会",
        "source": "化德县政府网站 (2026-07-21 人大常委会会议报道)",
        "notes": "主持第十六届人大常委会第三十一次会议"
    },
    # 4. 县委常委、统战部部长
    {
        "id": "p4",
        "name": "任烨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "化德县委统战部",
        "source": "化德县政府网站 (2026-07-16)",
        "notes": "2026年7月16日以县委常委、统战部部长身份深入宗教活动场所走访调研"
    },
    # 5. 县委常委、政府副县长
    {
        "id": "p5",
        "name": "叶明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政府副县长",
        "current_org": "化德县人民政府",
        "source": "化德县政府网站 (2026-07-21 人大常委会会议报道)",
        "notes": "列席第十六届人大常委会第三十一次会议"
    },
    # 6. 县委常委、纪委书记、监委主任
    {
        "id": "p6",
        "name": "安志文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "化德县纪委、监委",
        "source": "化德县政府网站 (2026-07-21 人大常委会会议报道)",
        "notes": "列席第十六届人大常委会第三十一次会议"
    },
    # 7. 副县长
    {
        "id": "p7",
        "name": "张国鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "化德县人民政府",
        "source": "化德县政府网站 (2026-07-24)",
        "notes": "陪同县委书记薛峰青赴七号镇调研"
    },
    # 8. 人民法院院长候选人
    {
        "id": "p8",
        "name": "谢旭红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县人民法院院长候选人",
        "current_org": "化德县人民法院",
        "source": "化德县政府网站 (2026-07-21 人大常委会会议报道)",
        "notes": "列席第十六届人大常委会第三十一次会议，为院长候选人"
    },
    # 9. 人民检察院检察长候选人
    {
        "id": "p9",
        "name": "李志鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县人民检察院检察长候选人",
        "current_org": "化德县人民检察院",
        "source": "化德县政府网站 (2026-07-21 人大常委会会议报道)",
        "notes": "列席第十六届人大常委会第三十一次会议，为检察长候选人"
    },
    # 10. 政协主席 (已知政协存在但具体人物待查)
    {
        "id": "p10",
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "化德县政协主席",
        "current_org": "化德县政协",
        "source": "",
        "notes": "化德县政协存在但主席姓名尚未从公开报道中确认"
    },
]

organizations = [
    {"id": 1, "name": "化德县委", "type": "党委", "level": "县处级", "parent": "乌兰察布市委", "location": "乌兰察布市化德县"},
    {"id": 2, "name": "化德县人民政府", "type": "政府", "level": "县处级", "parent": "化德县委", "location": "乌兰察布市化德县"},
    {"id": 3, "name": "化德县人大常委会", "type": "人大", "level": "县处级", "parent": "化德县委", "location": "乌兰察布市化德县"},
    {"id": 4, "name": "化德县委统战部", "type": "党委", "level": "乡科级", "parent": "化德县委", "location": "乌兰察布市化德县"},
    {"id": 5, "name": "化德县纪委、监委", "type": "党委", "level": "县处级", "parent": "化德县委", "location": "乌兰察布市化德县"},
    {"id": 6, "name": "化德县人民法院", "type": "政府", "level": "县处级", "parent": "乌兰察布市中级人民法院", "location": "乌兰察布市化德县"},
    {"id": 7, "name": "化德县人民检察院", "type": "政府", "level": "县处级", "parent": "乌兰察布市人民检察院", "location": "乌兰察布市化德县"},
    {"id": 8, "name": "化德县政协", "type": "政协", "level": "县处级", "parent": "化德县委", "location": "乌兰察布市化德县"},
]

positions = [
    # 薛峰青 — 县委书记
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "未知", "end": "present", "rank": "县处级正职", "note": "现任县委书记"},
    # 王永生 — 代县长
    {"person_id": "p2", "org_id": 2, "title": "县委副书记、政府代县长", "start": "2026", "end": "present", "rank": "县处级正职", "note": "2026年任代县长"},
    # 闫军 — 人大主任
    {"person_id": "p3", "org_id": 3, "title": "县人大常委会主任", "start": "未知", "end": "present", "rank": "县处级正职", "note": ""},
    # 任烨 — 统战部长
    {"person_id": "p4", "org_id": 4, "title": "县委常委、统战部部长", "start": "未知", "end": "present", "rank": "县处级副职", "note": ""},
    # 叶明 — 常委、副县长
    {"person_id": "p5", "org_id": 2, "title": "县委常委、政府副县长", "start": "未知", "end": "present", "rank": "县处级副职", "note": ""},
    # 安志文 — 纪委书记
    {"person_id": "p6", "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start": "未知", "end": "present", "rank": "县处级副职", "note": ""},
    # 张国鑫 — 副县长
    {"person_id": "p7", "org_id": 2, "title": "副县长", "start": "未知", "end": "present", "rank": "县处级副职", "note": ""},
    # 谢旭红 — 法院院长候选人
    {"person_id": "p8", "org_id": 6, "title": "院长候选人", "start": "2026", "end": "present", "rank": "县处级正职", "note": "2026年7月为院长候选人"},
    # 李志鹏 — 检察院检察长候选人
    {"person_id": "p9", "org_id": 7, "title": "检察长候选人", "start": "2026", "end": "present", "rank": "县处级正职", "note": "2026年7月为检察长候选人"},
    # 政协主席
    {"person_id": "p10", "org_id": 8, "title": "政协主席", "start": "未知", "end": "present", "rank": "县处级正职", "note": "具体人物待查"},
]

relationships = [
    # 薛峰青 ↔ 王永生 (党政一把手)
    {"person_a": "p1", "person_b": "p2", "type": "superior_subordinate",
     "context": "县委书记与代县长党政搭档关系", "overlap_org": "化德县委、县政府",
     "overlap_period": "2026-", "confidence": "confirmed"},
    # 薛峰青 ↔ 安志文 (县委领导)
    {"person_a": "p1", "person_b": "p6", "type": "superior_subordinate",
     "context": "县委书记与纪委书记在同一县委常委会共事", "overlap_org": "化德县委",
     "overlap_period": "2026-", "confidence": "confirmed"},
    # 薛峰青 ↔ 任烨 (县委领导)
    {"person_a": "p1", "person_b": "p4", "type": "superior_subordinate",
     "context": "县委书记与统战部部长在同一县委常委会共事", "overlap_org": "化德县委",
     "overlap_period": "2026-", "confidence": "confirmed"},
    # 薛峰青 ↔ 叶明 (县委领导)
    {"person_a": "p1", "person_b": "p5", "type": "superior_subordinate",
     "context": "县委书记与常务副县长在同一县委常委会共事", "overlap_org": "化德县委",
     "overlap_period": "2026-", "confidence": "confirmed"},
    # 薛峰青 ↔ 张国鑫 (调研陪同)
    {"person_a": "p1", "person_b": "p7", "type": "superior_subordinate",
     "context": "县委书记薛峰青赴七号镇调研时张国鑫陪同", "overlap_org": "化德县",
     "overlap_period": "2026-07", "confidence": "confirmed"},
    # 王永生 ↔ 叶明 (县政府正副职)
    {"person_a": "p2", "person_b": "p5", "type": "superior_subordinate",
     "context": "代县长与常务副县长在县政府共事", "overlap_org": "化德县人民政府",
     "overlap_period": "2026-", "confidence": "confirmed"},
    # 王永生 ↔ 张国鑫 (县政府正副职)
    {"person_a": "p2", "person_b": "p7", "type": "superior_subordinate",
     "context": "代县长与副县长在县政府共事", "overlap_org": "化德县人民政府",
     "overlap_period": "2026-", "confidence": "confirmed"},
]


# ── Build ──────────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    import sqlite3
    import os

    os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
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
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid(p["id"]), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and ("副" in post or "组织" in post or "政法" in post or "宣传" in post or "统战" in post):
            return ("100,150,255", 12.0)
        elif "副" in post and "县长" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post or "政协" in post:
            return ("200,255,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>化德县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # Summary
    print(f"\n{'='*60}")
    print(f"化德县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
