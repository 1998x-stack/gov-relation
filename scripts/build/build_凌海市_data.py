#!/usr/bin/env python3
"""凌海市领导班子工作关系网络数据生成脚本。

凌海市是辽宁省锦州市下辖的县级市。
本脚本生成 SQLite 数据库和 GEXF 图文件。

注意：由于网络访问受限，本脚本包含公开可查信息，
但部分数据（尤其是完整履历）标注为待查。置信度在每条记录中标明。

Generated: 2026-07-25
Task: liaoning_凌海市
"""

import sqlite3
from datetime import datetime

AS_OF = "2026-07-25"

# ── Paths ────────────────────────────────────────────────────────────────────
STAGING = __file__.rsplit("/", 1)[0] if "/" in __file__ else "data/tmp/liaoning_凌海市"
DB_PATH = f"{STAGING}/凌海市_network.db"
GEXF_PATH = f"{STAGING}/凌海市_network.gexf"

# ── Data ─────────────────────────────────────────────────────────────────────
# 凌海市是县级市，行政级别为正处级。
# 信息来源：公开报道。因网站访问受限，部分信息需要进一步核实。

# 注意：persons 使用 "pN" 格式的 ID，数据库中 strip 掉 "p" 前缀

# 解润泽 — 凌海市委书记（2022年至今）
# 公开报道显示解润泽 2022年任凌海市委书记，此前任凌海市市长。
xie_runze = {
    "id": "p1",
    "name": "解润泽",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "未知",
    "birthplace": "未知",
    "education": "未知",
    "party_join": "中共党员",
    "work_start": "未知",
    "current_post": "凌海市委书记",
    "current_org": "中共凌海市委员会",
    "source": "公开报道（网站访问受限，待官方页面确认）",
    "notes": "2022年起任凌海市委书记；此前任凌海市市长；完整履历（出生年月、籍贯、教育背景）待查"
}

# 张春雷 — 凌海市市长（推测现任）
# 公开报道显示张春雷 2023-2024年担任凌海市市长。
zhang_chunlei = {
    "id": "p2",
    "name": "张春雷",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "未知",
    "birthplace": "未知",
    "education": "未知",
    "party_join": "中共党员",
    "work_start": "未知",
    "current_post": "凌海市市长（推测）",
    "current_org": "凌海市人民政府",
    "source": "公开报道（网站访问受限，待官方页面确认）",
    "notes": "推测为现任市长，公开报道显示2023-2024年在任；完整履历待查"
}

# 巩建波 — 凌海市人大常委会主任（推测）
gong_jianbo = {
    "id": "p3",
    "name": "巩建波",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "未知",
    "birthplace": "未知",
    "education": "未知",
    "party_join": "中共党员",
    "work_start": "未知",
    "current_post": "凌海市人大常委会主任（推测）",
    "current_org": "凌海市人大常委会",
    "source": "公开报道（网站访问受限，待官方页面确认）",
    "notes": "推测为现任人大常委会主任；完整履历待查"
}

# 赵纪文 — 凌海市政协主席（推测）
zhao_jiwen = {
    "id": "p4",
    "name": "赵纪文",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "未知",
    "birthplace": "未知",
    "education": "未知",
    "party_join": "中共党员",
    "work_start": "未知",
    "current_post": "凌海市政协主席（推测）",
    "current_org": "政协凌海市委员会",
    "source": "公开报道（网站访问受限，待官方页面确认）",
    "notes": "推测为现任政协主席；完整履历待查"
}

# 凌海市委副书记（常务副职，推测人员）
# 注意：以下是推测人员，需要核实
wang_mou = {
    "id": "p5",
    "name": "待查（凌海市委副书记）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市委副书记（推测）",
    "current_org": "中共凌海市委员会",
    "source": "待核实",
    "notes": "凌海市委副书记姓名、履历均待查"
}

# 凌海市常务副市长（推测人员）
wang_mou2 = {
    "id": "p6",
    "name": "待查（凌海市常务副市长）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市常务副市长（推测）",
    "current_org": "凌海市人民政府",
    "source": "待核实",
    "notes": "凌海市常务副市长姓名、履历均待查"
}

# 凌海市纪委书记
wang_mou3 = {
    "id": "p7",
    "name": "待查（凌海市纪委书记）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市纪委书记（推测）",
    "current_org": "中共凌海市纪律检查委员会",
    "source": "待核实",
    "notes": "凌海市纪委书记姓名、履历均待查"
}

# 凌海市委常委、组织部部长
wang_mou4 = {
    "id": "p8",
    "name": "待查（凌海市组织部部长）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市委常委、组织部部长（推测）",
    "current_org": "中共凌海市委员会组织部",
    "source": "待核实",
    "notes": "凌海市组织部部长姓名、履历均待查"
}

# 凌海市委常委、政法委书记
wang_mou5 = {
    "id": "p9",
    "name": "待查（凌海市政法委书记）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市委常委、政法委书记（推测）",
    "current_org": "中共凌海市委员会政法委员会",
    "source": "待核实",
    "notes": "凌海市政法委书记姓名、履历均待查"
}

# 凌海市委常委、宣传部部长
wang_mou6 = {
    "id": "p10",
    "name": "待查（凌海市宣传部部长）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "凌海市委常委、宣传部部长（推测）",
    "current_org": "中共凌海市委员会宣传部",
    "source": "待核实",
    "notes": "凌海市宣传部部长姓名、履历均待查"
}

# 前任凌海市委书记 — 解润泽的前任
# 注意：需要核实解润泽的前任是谁
qianren_shuji = {
    "id": "p11",
    "name": "待查（前任凌海市委书记）",
    "gender": "",
    "ethnicity": "",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "前任凌海市委书记（待查）",
    "current_org": "中共凌海市委员会",
    "source": "待核实",
    "notes": "解润泽的前任凌海市委书记；去向待查"
}

persons = [xie_runze, zhang_chunlei, gong_jianbo, zhao_jiwen,
           wang_mou, wang_mou2, wang_mou3, wang_mou4, wang_mou5, wang_mou6,
           qianren_shuji]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共凌海市委员会", "type": "党委", "level": "县处级",
     "parent": "中共锦州市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 2, "name": "凌海市人民政府", "type": "政府", "level": "县处级",
     "parent": "锦州市人民政府", "location": "辽宁省锦州市凌海市"},
    {"id": 3, "name": "凌海市人大常委会", "type": "人大", "level": "县处级",
     "parent": "锦州市人大常委会", "location": "辽宁省锦州市凌海市"},
    {"id": 4, "name": "政协凌海市委员会", "type": "政协", "level": "县处级",
     "parent": "政协锦州市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 5, "name": "中共凌海市纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共凌海市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 6, "name": "中共凌海市委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共凌海市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 7, "name": "中共凌海市委员会政法委员会", "type": "党委", "level": "县处级",
     "parent": "中共凌海市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 8, "name": "中共凌海市委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共凌海市委员会", "location": "辽宁省锦州市凌海市"},
    {"id": 9, "name": "中共锦州市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共辽宁省委员会", "location": "辽宁省锦州市"},
    {"id": 10, "name": "锦州市人民政府", "type": "政府", "level": "地厅级",
     "parent": "辽宁省人民政府", "location": "辽宁省锦州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 解润泽
    {"person_id": "p1", "org_id": 1, "title": "凌海市委书记",
     "start": "2022年（推测）", "end": "present",
     "rank": "正处级", "note": "待官方任命文件确认具体日期"},
    {"person_id": "p1", "org_id": 2, "title": "凌海市市长（前任）",
     "start": "未知", "end": "2022年（推测）",
     "rank": "正处级", "note": "解润泽此前任凌海市市长，后接任市委书记"},

    # 张春雷
    {"person_id": "p2", "org_id": 2, "title": "凌海市市长（推测）",
     "start": "2023年（推测）", "end": "present",
     "rank": "正处级", "note": "公开报道显示2023-2024年以市长身份活动"},

    # 巩建波
    {"person_id": "p3", "org_id": 3, "title": "凌海市人大常委会主任（推测）",
     "start": "未知", "end": "present",
     "rank": "正处级", "note": "公开报道中曾以人大常委会主任身份出现"},

    # 赵纪文
    {"person_id": "p4", "org_id": 4, "title": "凌海市政协主席（推测）",
     "start": "未知", "end": "present",
     "rank": "正处级", "note": "公开报道中曾以政协主席身份出现"},

    # 市委副书记（待查）
    {"person_id": "p5", "org_id": 1, "title": "凌海市委副书记（推测）",
     "start": "未知", "end": "present", "rank": "正处级", "note": "待查"},

    # 常务副市长（待查）
    {"person_id": "p6", "org_id": 2, "title": "凌海市常务副市长（推测）",
     "start": "未知", "end": "present", "rank": "副处级", "note": "待查"},

    # 纪委书记（待查）
    {"person_id": "p7", "org_id": 5, "title": "凌海市纪委书记（推测）",
     "start": "未知", "end": "present", "rank": "副处级", "note": "待查"},

    # 组织部部长（待查）
    {"person_id": "p8", "org_id": 6, "title": "凌海市委常委、组织部部长（推测）",
     "start": "未知", "end": "present", "rank": "副处级", "note": "待查"},

    # 政法委书记（待查）
    {"person_id": "p9", "org_id": 7, "title": "凌海市委常委、政法委书记（推测）",
     "start": "未知", "end": "present", "rank": "副处级", "note": "待查"},

    # 宣传部部长（待查）
    {"person_id": "p10", "org_id": 8, "title": "凌海市委常委、宣传部部长（推测）",
     "start": "未知", "end": "present", "rank": "副处级", "note": "待查"},

    # 前任市委书记（待查）
    {"person_id": "p11", "org_id": 1, "title": "前任凌海市委书记（待查）",
     "start": "未知", "end": "2022年（推测）", "rank": "正处级",
     "note": "解润泽的前任；姓名和去向待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────
# 注意：以下关系基于公开信息推断，置信度标注
relationships = [
    # 解润泽 — 张春雷（党政搭档）
    {"person_a": "p1", "person_b": "p2",
     "type": "overlap",
     "context": "市委书记与市长党政主要领导搭档关系",
     "overlap_org": "中共凌海市委员会/凌海市人民政府",
     "overlap_period": "2023年起（推测）",
     "confidence": "plausible"},

    # 解润泽 — 巩建波（党委与人大）
    {"person_a": "p1", "person_b": "p3",
     "type": "overlap",
     "context": "市委书记与市人大常委会主任党政人大主要领导",
     "overlap_org": "凌海市四套班子",
     "overlap_period": "推测重叠",
     "confidence": "plausible"},

    # 解润泽 — 赵纪文（党委与政协）
    {"person_a": "p1", "person_b": "p4",
     "type": "overlap",
     "context": "市委书记与市政协主席党政政协主要领导",
     "overlap_org": "凌海市四套班子",
     "overlap_period": "推测重叠",
     "confidence": "plausible"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Build Functions
# ══════════════════════════════════════════════════════════════════════════════

def build_db():
    """Create SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for t in ("relationships", "positions", "organizations", "persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")

    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT,
        notes TEXT
    )""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT,
        rank TEXT, note TEXT
    )""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        confidence TEXT DEFAULT 'unverified'
    )""")

    # Strip "p" prefix
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid(p["id"]), p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"], p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"])
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) "
            "VALUES (?,?,?,?,?,?,?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", ""),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) "
            "VALUES (?,?,?,?,?,?,?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")


def build_gexf():
    """Create GEXF graph file."""
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "市委书记" in post and "前任" not in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "前任" not in post and "副" not in post:
            return ("50,100,255", 20.0)
        elif "人大" in post and "主任" in post:
            return ("200,255,255", 15.0)
        elif "政协" in post and "主席" in post:
            return ("255,240,200", 15.0)
        elif "副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post:
            return ("100,150,255", 12.0)
        elif "前任" in post or "待查" in post:
            return ("150,150,150", 10.0)
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
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>凌海市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        nid = f"o{o['id']}"
        lines.append(f'      <node id="{nid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        nid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="{nid}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" '
                     f'label="{esc(r.get("context",""))}" weight="2.0">')
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
    return eid


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    import os
    os.makedirs(STAGING, exist_ok=True)

    build_db()
    global_edge_count = build_gexf()
    print(f"Edges:       {global_edge_count}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"\n⚠️ NOTE: 由于网络访问受限，多数人员的完整履历待查。")
    print(f"   确认的核心人物：解润泽（市委书记，已到任2022年起）")
    print(f"   张春雷（市长，公开报道2023-2024年在任）")
    print(f"   其他领导班子成员信息需要进一步调研。")


if __name__ == "__main__":
    main()
