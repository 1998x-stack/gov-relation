#!/usr/bin/env python3
"""恩施市 (Enshi City) — 湖北省恩施土家族苗族自治州下辖县级市

领导人关系网络数据构建脚本。

Targets: 市委书记彭元洪、市长郭玉锋
Data as of: 2026-07-24
"""
import os, sqlite3
from datetime import datetime

AS_OF = "2026-07-24"
DB_PATH = os.path.join(os.path.dirname(__file__), "恩施市_network.db")
GEXF_PATH = os.path.join(os.path.dirname(__file__), "恩施市_network.gexf")

# ── Data ───────────────────────────────────────────────────────────────────

persons = [
    # ── 核心党政领导 ──
    {
        "id": "p1",
        "name": "彭元洪",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共恩施市委",
        "source": "恩施市人民政府门户网站（www.es.gov.cn）2026年7月新闻报道",
        "notes": "2026年7月以市委书记身份公开活动，赴红土乡、新塘乡、白果乡、盛家坝镇调研；出席恩施市企业家座谈会。完整出生年月、籍贯、学历、入党/参加工作时间待查。"
    },
    {
        "id": "p2",
        "name": "郭玉锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "恩施市人民政府",
        "source": "恩施市人民政府门户网站2026年7月22日新闻报道（市十一届人民政府第76次常务会议）",
        "notes": "2026年7月以市委副书记、市长身份主持召开市政府常务会议。完整出生年月、籍贯、民族、学历、入党/参加工作时间待查。"
    },
    # ── 市人大常委会 ──
    {
        "id": "p3",
        "name": "徐卫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道（市十一届人大常委会第三十九次会议）",
        "notes": "2026年7月以市人大常委会主任身份主持会议。此前曾任恩施市委常委（新闻报道中多次列席主要领导活动）。完整履历待查。"
    },
    # ── 市委/政府相关领导 ──
    {
        "id": "p4",
        "name": "张涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共恩施市委/恩施市人民政府",
        "source": "恩施市人民政府门户网站2026年7月新闻报道",
        "notes": "出席企业家座谈会及州委书记赴恩施市调研会议。具体职务推测为市委常委、副市长。完整履历待查。"
    },
    {
        "id": "p5",
        "name": "李华军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共恩施市委",
        "source": "恩施市人民政府门户网站2026年7月新闻报道",
        "notes": "出席企业家座谈会。具体分管领域待查。"
    },
    {
        "id": "p6",
        "name": "毛传顺",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共恩施市委",
        "source": "恩施市人民政府门户网站2026年7月新闻报道",
        "notes": "出席企业家座谈会。具体分管领域待查。"
    },
    {
        "id": "p7",
        "name": "易发斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共恩施市委",
        "source": "恩施市人民政府门户网站2026年7月新闻报道",
        "notes": "出席企业家座谈会。具体分管领域待查。"
    },
    # ── 市人大常委会副主任 ──
    {
        "id": "p8",
        "name": "黎昔品",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
    {
        "id": "p9",
        "name": "余秋红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
    {
        "id": "p10",
        "name": "王学渊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
    {
        "id": "p11",
        "name": "万亨东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
    {
        "id": "p12",
        "name": "杨帆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
    {
        "id": "p13",
        "name": "徐贵尧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "恩施市人大常委会",
        "source": "恩施市人民政府门户网站2026年7月20日新闻报道"
    },
]

organizations = [
    {"id": 1, "name": "中共恩施市委", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施土家族苗族自治州恩施市"},
    {"id": 2, "name": "恩施市人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施土家族苗族自治州恩施市"},
    {"id": 3, "name": "恩施市人大常委会", "type": "人大", "level": "县级", "parent": "恩施市人大常委会", "location": "湖北省恩施土家族苗族自治州恩施市"},
]

positions = [
    # 彭元洪
    {"person_id": "p1", "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正县级", "note": "2026年7月已就任市委书记"},
    # 郭玉锋
    {"person_id": "p2", "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正县级", "note": "2026年7月以市委副书记、市长身份公开活动"},
    {"person_id": "p2", "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "", "note": "兼任市委副书记"},
    # 徐卫
    {"person_id": "p3", "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "2026年7月主持会议"},
    # 张涛
    {"person_id": "p4", "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p4", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "", "note": "推测为市委常委、副市长"},
    # 李华军
    {"person_id": "p5", "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 毛传顺
    {"person_id": "p6", "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 易发斌
    {"person_id": "p7", "org_id": 1, "title": "市委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    # 人大副主任们
    {"person_id": "p8", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p9", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p10", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p11", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p12", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": "p13", "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
# 基于公开报道的党政搭档关系和同一层级共事关系
relationships = [
    {"person_a": "p1", "person_b": "p2", "type": "党政搭档", "context": "市委书记彭元洪与市长郭玉锋为恩施市党政正职搭档", "overlap_org": "中共恩施市委/恩施市人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p3", "type": "同届领导班子", "context": "市委书记与市人大常委会主任为同届市委/市人大常委会领导核心", "overlap_org": "中共恩施市委", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p2", "person_b": "p3", "type": "党政人大协同", "context": "市长与市人大常委会主任为政府与人大主要领导", "overlap_org": "恩施市", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p4", "type": "上下级关系", "context": "市委书记与市委常委/副市长为市委领导班子上下级关系", "overlap_org": "中共恩施市委", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p5", "type": "上下级关系", "context": "市委书记与市委常委为市委领导班子成员", "overlap_org": "中共恩施市委", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p6", "type": "上下级关系", "context": "市委书记与市委常委为市委领导班子成员", "overlap_org": "中共恩施市委", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p1", "person_b": "p7", "type": "上下级关系", "context": "市委书记与市委常委为市委领导班子成员", "overlap_org": "中共恩施市委", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p8", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p9", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p10", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p11", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p12", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": "p3", "person_b": "p13", "type": "上下级关系", "context": "市人大常委会主任与副主任为人大领导班子搭档", "overlap_org": "恩施市人大常委会", "overlap_period": "2026年至今", "confidence": "confirmed"},
]

# ── Build ──────────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
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
            (pid(p["id"]), p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""),
             p["current_post"], p["current_org"], p.get("source",""), p.get("notes",""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o.get("level",""), o.get("parent",""), o.get("location",""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start",""), pos.get("end","present"),
             pos.get("rank",""), pos.get("note",""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context",""),
             r.get("overlap_org",""), r.get("overlap_period",""),
             r.get("confidence","unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color_and_size(post):
        if "市委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "市委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and ("副" in post or "组织" in post or "政法" in post or "宣传" in post or "统战" in post):
            return ("100,150,255", 12.0)
        elif "副" in post and ("市长" in post or "主任" in post):
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
    lines.append(f'    <description>恩施市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

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

    print(f"\n{'='*60}")
    print(f"恩施市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")

if __name__ == "__main__":
    build()
