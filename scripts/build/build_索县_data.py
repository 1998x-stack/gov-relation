#!/usr/bin/env python3
"""
索县（西藏自治区那曲市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Suo County leadership.

Research environment notes:
  - Exa search engine rate-limited - not available
  - Baidu Baike access blocked (403)
  - www.nqsx.gov.cn (索县政府网站) unreachable
  - zh.wikipedia.org accessible via API (limited data)
  
All person-level data is marked with ⚠️ "待确认" and requires verification from:
  - http://www.nqsx.gov.cn/ (索县政府网领导之窗)
  - Baidu Baike entries for each individual
  - 那曲市委组织部任前公示
  - 西藏日报/那曲新闻网相关报道
"""

import sqlite3
import os
import sys
from datetime import datetime

# Staging paths (written to data/tmp/xizang_索县/)
STAGING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(STAGING_DIR, "..", "..", "..")  # repo root
DB_PATH = os.path.join(STAGING_DIR, "索县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "索县_network.gexf")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# ── PERSON DATA ─────────────────────────────────────────────────────
# ID convention: suo_{surname_givenname}
# All data marked ⚠️ 待确认 due to inaccessible web research environment

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══
    # ⚠️ 索县县委书记
    ("suo_secretary", "（待确认）", "男", "藏族（推測）", "待查", "待查",
     "待查", "待查", "待查",
     "县委书记", "中共索县委员会",
     "⚠️ 待确认：www.nqsx.gov.cn + 那曲市委组织部任前公示"),

    # ⚠️ 索县县长
    ("suo_mayor", "（待确认）", "男", "藏族（推測）", "待查", "待查",
     "待查", "待查", "待查",
     "县委副书记、县长", "索县人民政府",
     "⚠️ 待确认：www.nqsx.gov.cn"),

    # ═══ Standing Committee (推定岗位) ═══
    ("suo_deputy_sec", "（待确认）", "男", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委副书记（专职）", "中共索县委员会",
     "⚠️ 待确认"),
    ("suo_exec_vice", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、常务副县长", "索县人民政府",
     "⚠️ 待确认"),
    ("suo_discipline", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、纪委书记、监委主任", "中共索县纪律检查委员会",
     "⚠️ 待确认"),
    ("suo_org", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、组织部部长", "中共索县县委组织部",
     "⚠️ 待确认"),
    ("suo_propaganda", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共索县县委宣传部",
     "⚠️ 待确认"),
    ("suo_legal", "（待确认）", "男", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、政法委书记", "中共索县县委政法委员会",
     "⚠️ 待确认"),
    ("suo_united_front", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、统战部部长", "中共索县县委统战部",
     "⚠️ 待确认"),
    ("suo_armed", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县委常委、人武部政委（或部长）", "索县人民武装部",
     "⚠️ 待确认"),

    # ═══ Vice Mayors ═══
    ("suo_vice_mayor_01", "（待确认）", "男", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "副县长", "索县人民政府",
     "⚠️ 待确认"),
    ("suo_vice_mayor_02", "（待确认）", "男", "汉族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "副县长", "索县人民政府",
     "⚠️ 待确认"),
    ("suo_vice_mayor_03", "（待确认）", "女", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "副县长", "索县人民政府",
     "⚠️ 待确认"),

    # ═══ NPC & CPPCC ═══
    ("suo_npc_chair", "（待确认）", "男", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县人大常委会主任", "索县人民代表大会常务委员会",
     "⚠️ 待确认"),
    ("suo_cppcc_chair", "（待确认）", "男", "藏族（推）", "待查", "待查",
     "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议索县委员会",
     "⚠️ 待确认"),

    # ═══ 那曲市领导（关联参考）══════
    ("nq_zhang_haibo", "张海波", "男", "汉族", "1969-06", "待查",
     "待查", "中共党员", "待查",
     "那曲市委书记", "中共那曲市委员会",
     "https://zh.wikipedia.org/wiki/那曲市"),
    ("nq_zhaxi_duoji", "扎西多吉", "男", "藏族", "1970-03", "待查",
     "待查", "中共党员", "待查",
     "那曲市委副书记、市长", "那曲市人民政府",
     "https://zh.wikipedia.org/wiki/那曲市"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)

    # 索县本地组织
    ("suo_party", "中共索县委员会", "党委", "县处级", "中共那曲市委员会", "西藏那曲市索县"),
    ("suo_gov", "索县人民政府", "政府", "县处级", "那曲市人民政府", "西藏那曲市索县"),
    ("suo_discipline", "中共索县纪律检查委员会", "纪委", "县处级", "那曲市纪委监委", "西藏那曲市索县"),
    ("suo_org", "中共索县县委组织部", "党委部门", "乡科级", "中共索县委员会", "西藏那曲市索县"),
    ("suo_propaganda", "中共索县县委宣传部", "党委部门", "乡科级", "中共索县委员会", "西藏那曲市索县"),
    ("suo_legal", "中共索县县委政法委员会", "党委部门", "乡科级", "中共索县委员会", "西藏那曲市索县"),
    ("suo_united_front", "中共索县县委统战部", "党委部门", "乡科级", "中共索县委员会", "西藏那曲市索县"),
    ("suo_armed", "索县人民武装部", "军队", "县处级", "那曲军分区", "西藏那曲市索县"),
    ("suo_npc", "索县人民代表大会常务委员会", "人大", "县处级", "那曲市人大常委会", "西藏那曲市索县"),
    ("suo_cppcc", "中国人民政治协商会议索县委员会", "政协", "县处级", "那曲市政协", "西藏那曲市索县"),
    ("suo_public_security", "索县公安局", "公安", "乡科级", "那曲市公安局", "西藏那曲市索县"),

    # 那曲市组织
    ("nq_party", "中共那曲市委员会", "党委", "地厅级", "中共西藏自治区委员会", "西藏那曲市色尼区"),
    ("nq_gov", "那曲市人民政府", "政府", "地厅级", "西藏自治区人民政府", "西藏那曲市色尼区"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # ⚠️ 以下所有索县任职信息均待确认

    # 县委书记
    ("suo_secretary", "suo_party", "县委书记", "待查", "至今",
     "县处级正职", "⚠️ 待确认"),

    # 县长（兼县委副书记）
    ("suo_mayor", "suo_gov", "县长", "待查", "至今",
     "县处级正职", "⚠️ 待确认"),
    ("suo_mayor", "suo_party", "县委副书记", "待查", "至今",
     "县处级正职", "兼任政府主官"),

    # 专职副书记
    ("suo_deputy_sec", "suo_party", "县委副书记（专职）", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),

    # 常务副县长
    ("suo_exec_vice", "suo_gov", "常务副县长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_exec_vice", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 纪委书记
    ("suo_discipline", "suo_discipline", "县纪委书记、县监委主任", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_discipline", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 组织部部长
    ("suo_org", "suo_org", "组织部部长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_org", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 宣传部部长
    ("suo_propaganda", "suo_propaganda", "宣传部部长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_propaganda", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 政法委书记
    ("suo_legal", "suo_legal", "政法委书记", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_legal", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 统战部部长
    ("suo_united_front", "suo_united_front", "统战部部长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_united_front", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),

    # 人武部部长/政委
    ("suo_armed", "suo_party", "县委常委", "待查", "至今",
     "县处级副职", "兼任"),
    ("suo_armed", "suo_armed", "人武部部长（或政委）", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),

    # 副县长
    ("suo_vice_mayor_01", "suo_gov", "副县长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_vice_mayor_02", "suo_gov", "副县长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),
    ("suo_vice_mayor_03", "suo_gov", "副县长", "待查", "至今",
     "县处级副职", "⚠️ 待确认"),

    # 人大主任
    ("suo_npc_chair", "suo_npc", "县人大常委会主任", "待查", "至今",
     "县处级正职", "⚠️ 待确认"),

    # 政协主席
    ("suo_cppcc_chair", "suo_cppcc", "县政协主席", "待查", "至今",
     "县处级正职", "⚠️ 待确认"),

    # 那曲市领导（从既有资料已知）
    ("nq_zhang_haibo", "nq_party", "那曲市委书记", "2024-12", "至今",
     "地厅级正职", "接替庄劲松"),
    ("nq_zhang_duoji", "nq_gov", "那曲市委副书记、市长", "2024-05", "至今",
     "地厅级正职", ""),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # ⚠️ 以下关系待确认身份后补充
    ("suo_secretary", "suo_mayor", "党政搭档（推定）", "党政主要领导", "索县", "至今"),
    ("suo_secretary", "nq_zhang_haibo", "上下级关系（推定）", "市委-县委领导关系", "那曲市", "2024-12至今"),
    ("suo_mayor", "nq_zhang_duoji", "上下级关系（推定）", "市政府-县政府领导关系", "那曲市", "2024-05至今"),

    # 那曲市领导层关系
    ("nq_zhang_haibo", "nq_zhang_duoji", "党政搭档", "现任党政领导", "那曲市", "2024-12至今"),
]


# ── BUILD DATABASE ──

def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def generate_gexf():
    """Generate GEXF 1.3 with viz namespace using string formatting."""

    node_colors = {
        "party_secretary": (212, 52, 46),
        "gov_leader": (51, 102, 204),
        "gov_deputy": (80, 130, 200),
        "discipline": (204, 119, 34),
        "other_person": (102, 102, 102),
        "org_party": (180, 60, 60),
        "org_gov": (60, 80, 120),
        "org_other": (100, 100, 100),
    }

    def color_for_person(pid):
        for p in PERSONS:
            if p[0] == pid:
                post = p[9] or ""
                if "县委书记" in post and "纪委" not in post:
                    return "party_secretary", 20.0
                elif "县长" in post or "市长" in post:
                    return "gov_leader", 20.0
                elif "市委书记" in post:
                    return "party_secretary", 20.0
                elif "常务副县长" in post or "常务副" in post:
                    return "gov_leader", 16.0
                elif "副县长" in post or "副市长" in post:
                    return "gov_deputy", 14.0
                elif "纪委书记" in post or "纪委" in post:
                    return "discipline", 14.0
                else:
                    return "other_person", 12.0
        return "other_person", 12.0

    def color_for_org(oid):
        for o in ORGANIZATIONS:
            if o[0] == oid:
                tp = o[2]
                if "党委" in tp:
                    return "org_party", 8.0
                elif "政府" in tp or "公安" in tp:
                    return "org_gov", 8.0
                else:
                    return "org_other", 8.0
        return "org_other", 8.0

    nodes = []
    edges = []

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        g, sz = color_for_person(pid)
        r, gb, b = node_colors[g]
        nodes.append(f"""\
    <node id="{pid}" label="{label}">
      <attvalues>
        <attvalue for="node_type" value="person"/>
        <attvalue for="role" value="{p[9]}"/>
        <attvalue for="ethnicity" value="{p[3]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        g, sz = color_for_org(oid)
        r, gb, b = node_colors[g]
        nodes.append(f"""\
    <node id="{oid}" label="{label}">
      <attvalues>
        <attvalue for="node_type" value="org"/>
        <attvalue for="org_type" value="{o[2]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # worked_at edges
    eid = 0
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        edges.append(f"""\
    <edge id="e{eid}" source="{pid}" target="{oid}" type="directed" label="{title}">
      <attvalues>
        <attvalue for="edge_type" value="worked_at"/>
        <attvalue for="start" value="{start or ''}"/>
        <attvalue for="end" value="{end or ''}"/>
        <attvalue for="rank" value="{rank or ''}"/>
      </attvalue>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # relationship edges
    for rel in RELATIONSHIPS:
        a, b, typ, ctx, org, period = rel
        eid += 1
        is_strong = "强" in typ or "党政搭档" in typ
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges.append(f"""\
    <edge id="e{eid}" source="{a}" target="{b}" type="undirected" label="{ctx}">
      <attvalues>
        <attvalue for="edge_type" value="relationship"/>
        <attvalue for="strength" value="{typ}"/>
        <attvalue for="context" value="{ctx}"/>
        <attvalue for="overlap_org" value="{org}"/>
        <attvalue for="overlap_period" value="{period}"/>
      </attvalue>
      <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>
      <viz:thickness value="{thickness}"/>
    </edge>""")

    nodes_block = "\n".join(nodes)
    edges_block = "\n".join(edges)

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <meta>
    <creator>China-Gov-Network Investigation</creator>
    <description>索县领导班子工作关系网络 — 2026年8月（⚠️ 所有索县人员信息待确认）</description>
    <date>2026-08-03</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="node_type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="ethnicity" title="Ethnicity" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="edge_type" title="Edge Type" type="string"/>
      <attribute id="start" title="Start Date" type="string"/>
      <attribute id="end" title="End Date" type="string"/>
      <attribute id="rank" title="Rank" type="string"/>
      <attribute id="strength" title="Strength" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_block}
    </nodes>
    <edges>
{edges_block}
    </edges>
  </graph>
</gexf>"""

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf)
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
        if table == "persons":
            c.execute("SELECT COUNT(*) FROM persons WHERE source LIKE '%待确认%'")
            pending = c.fetchone()[0]
            print(f"    └─ 待确认: {pending}, 已确认: {cnt - pending}")
    conn.close()


if __name__ == "__main__":
    import sys
    print("=" * 60)
    print("  索县领导班子工作关系网络 — 数据构建")
    print("  ⚠️  注意：由于网络环境受限，所有索县人员信息均为占位符")
    print("  ⚠️  请从 www.nqsx.gov.cn 获取真实数据后更新此脚本")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n⚠️  IMPORTANT: This data contains placeholder entries only.")
    print("    To populate real data, access:")
    print("    - http://www.nqsx.gov.cn (索县政府网站)")
    print("    - https://baike.baidu.com (百度百科)")
    print("    - 那曲市委组织部任前公示")
    print("Done.")