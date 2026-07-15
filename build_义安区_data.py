#!/usr/bin/env python3
"""
义安区（铜陵市市辖区）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Yi'an District leadership network.

Research date: 2026-07-15
Sources used:
  - zh.wikipedia.org (维基百科) — 义安区 page / 铜陵市 page
  - district.ce.cn (中国经济网)
  - baike.baidu.com (百度百科)
  - thepaper.cn (澎湃新闻)
  - sohu.com (搜狐新闻)
  - tl.gov.cn (铜陵市人民政府)
  - ahtlyaq.gov.cn (义安区人民政府)

Note: This investigation was conducted with limited web search availability (Exa rate-limited,
Baidu 403, Bing timeouts). Key data sources are Wikipedia and official website structural pages.
Several biographical details remain unconfirmed and are marked as such.
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Staging paths
STAGING_DIR = BASE_DIR
DB_PATH = os.path.join(STAGING_DIR, "义安区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "义安区_network.gexf")

# ── PERSONS ──
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
PERSONS = [
    # ═══ Current Top Leaders ═══

    # 区委书记 (截至2025年6月维基百科资料)
    # 方小雄，维基百科义安区页面同时标注为"区委书记"和"区长"
    # 推测：他可能此前任区长，后升任书记，维基条目未完全区分
    ("ya_fang_xiaoxiong", "方小雄", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "义安区委书记", "中共铜陵市义安区委员会",
     "https://zh.wikipedia.org/wiki/义安区"),

    # 区长（待确认现任区长是否为方小雄兼任或另有其人）
    # 维基同时标记方小雄为区委书记和区长，通常意味着他此前任区长后升书记
    # 新区长信息在公开资料中暂未明确
    ("ya_mayor_unknown", "（区长待确认）", "待查", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "义安区区长（待确认）", "义安区人民政府",
     "https://zh.wikipedia.org/wiki/义安区"),

    # ═══ NPC & CPPCC ═══

    # 区人大常委会主任（维基百科确认）
    ("ya_wang_guangming", "汪光明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "义安区人大常委会主任", "铜陵市义安区人民代表大会常务委员会",
     "https://zh.wikipedia.org/wiki/义安区"),

    # 区政协主席（维基百科确认）
    ("ya_xu_changning", "徐常宁", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "义安区政协主席", "中国人民政治协商会议铜陵市义安区委员会",
     "https://zh.wikipedia.org/wiki/义安区"),

    # ═══ 前任领导人 ═══

    # 前区委书记 姚贵平（方小雄前任，推测2020年代前期任义安区委书记）
    ("ya_yao_guiping", "姚贵平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原义安区委书记，后去向待查）", "中共铜陵市义安区委员会",
     "https://zh.wikipedia.org/wiki/义安区"),

    # 前区长 方小雄（此前任区长，后升区委书记）

    # ═══ City-level leaders (connections) ═══

    # 铜陵市委书记
    ("tl_yang_hongxing", "杨宏星", "男", "汉族", "1968-10", "安徽长丰",
     "待查", "中共党员", "待查",
     "铜陵市委书记", "中共铜陵市委员会",
     "https://zh.wikipedia.org/wiki/铜陵市"),

    # 铜陵市长
    ("tl_kong_tao", "孔涛", "男", "汉族", "1974-03", "山东烟台",
     "待查", "中共党员", "待查",
     "铜陵市委副书记、市长", "铜陵市人民政府",
     "https://zh.wikipedia.org/wiki/铜陵市"),

    # 铜陵市政协主席
    ("tl_wu_zuolu", "吴祚麓", "男", "汉族", "1968-11", "安徽怀宁",
     "待查", "中共党员", "待查",
     "铜陵市政协主席", "中国人民政治协商会议铜陵市委员会",
     "https://zh.wikipedia.org/wiki/铜陵市"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("ya_party", "中共铜陵市义安区委员会", "党委", "县处级", "中共铜陵市委员会", "安徽省铜陵市义安区"),
    ("ya_gov", "义安区人民政府", "政府", "县处级", "铜陵市人民政府", "安徽省铜陵市义安区"),
    ("ya_npc", "铜陵市义安区人民代表大会常务委员会", "人大", "县处级", "铜陵市人大常委会", "安徽省铜陵市义安区"),
    ("ya_cppcc", "中国人民政治协商会议铜陵市义安区委员会", "政协", "县处级", "铜陵市政协", "安徽省铜陵市义安区"),
    # City level
    ("tl_party", "中共铜陵市委员会", "党委", "地市级", "中共安徽省委员会", "安徽省铜陵市"),
    ("tl_gov", "铜陵市人民政府", "政府", "地市级", "安徽省人民政府", "安徽省铜陵市"),
    ("tl_npc", "铜陵市人大常委会", "人大", "地市级", "安徽省人大常委会", "安徽省铜陵市"),
    ("tl_cppcc", "中国人民政治协商会议铜陵市委员会", "政协", "地市级", "安徽省政协", "安徽省铜陵市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # ═══ 方小雄 — 完整履历 ═══
    ("ya_fang_xiaoxiong", "ya_party", "义安区委书记", "约2024", "至今", "县处级正职",
     "据维基百科，现为义安区委书记（截至2025年6月）"),
    ("ya_fang_xiaoxiong", "ya_gov", "义安区区长（前任）", "约2022", "约2024", "县处级正职",
     "推测此前任义安区区长，后升任区委书记。维基同时标注书记和区长，可能未及时更新"),

    # ═══ 汪光明 ═══
    ("ya_wang_guangming", "ya_npc", "义安区人大常委会主任", "待查", "至今", "县处级正职",
     "来源：维基百科义安区页面"),

    # ═══ 徐常宁 ═══
    ("ya_xu_changning", "ya_cppcc", "义安区政协主席", "待查", "至今", "县处级正职",
     "来源：维基百科义安区页面"),

    # ═══ 姚贵平（前区委书记） ═══
    ("ya_yao_guiping", "ya_party", "义安区委书记（前任）", "约2021", "约2024", "县处级正职",
     "来源推测"),

    # ═══ 市级领导 ═══
    ("tl_yang_hongxing", "tl_party", "铜陵市委书记", "2024-12", "至今", "正厅级",
     "2024年12月任铜陵市委书记"),
    ("tl_kong_tao", "tl_gov", "铜陵市委副书记、市长", "2021-04", "至今", "正厅级",
     "2021年4月任铜陵市长"),
    ("tl_kong_tao", "tl_party", "铜陵市委副书记", "2021-04", "至今", "正厅级",
     ""),
    ("tl_wu_zuolu", "tl_cppcc", "铜陵市政协主席", "2026-01", "至今", "正厅级",
     "2026年1月任铜陵市政协主席"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # ═══ 党政搭档（方小雄书记 → 区长待确认） ═══
    # 方小雄如果同时兼任书记和区长，则无党政搭档之分
    # 如已升书记后有新区长，则需补充

    # ═══ 前后任书记 ═══
    ("ya_yao_guiping", "ya_fang_xiaoxiong", "职务接替",
     "姚贵平→方小雄（义安区委书记前后任）", "中共义安区委", "约2024"),

    # ═══ 区级人大政协领导关系 ═══
    ("ya_fang_xiaoxiong", "ya_wang_guangming", "弱关系（推定）",
     "区委书记×人大主任（推定工作关系）", "义安区", "至今"),
    ("ya_fang_xiaoxiong", "ya_xu_changning", "弱关系（推定）",
     "区委书记×政协主席（推定工作关系）", "义安区", "至今"),

    # ═══ 区级领导与市级领导关系 ═══
    ("ya_fang_xiaoxiong", "tl_yang_hongxing", "弱关系（推定）",
     "义安区委书记×铜陵市委书记（上下级）", "铜陵市", "2024-12至今"),
    ("ya_fang_xiaoxiong", "tl_kong_tao", "弱关系（推定）",
     "义安区委书记×铜陵市长（上下级）", "铜陵市", "至今"),

    ("ya_yao_guiping", "tl_kong_tao", "弱关系（推定）",
     "原义安区委书记×铜陵市长（上下级）", "铜陵市", "约2021-2024"),
    ("ya_yao_guiping", "tl_yang_hongxing", "弱关系（推定）",
     "原义安区委书记×铜陵市委书记（上下级）", "铜陵市", "2024-12至今"),
]


# ── HELPERS ──

def esc(s):
    """Escape XML special chars."""
    return (str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;"))


def person_color(role_str):
    """Return (r,g,b) for a person node based on current_post."""
    s = str(role_str)
    if s.startswith("义安区委书记"):
        return (220, 30, 30)   # 红色 = 书记
    if s.startswith("义安区区长") or "区长" in s:
        return (40, 100, 220)  # 蓝色 = 政府一把手
    if "人大" in s:
        return (200, 150, 40)  # 橙色 = 人大
    if "政协" in s:
        return (200, 150, 40)  # 橙色 = 政协
    if "铜陵市委" in s or "铜陵市长" in s:
        return (80, 150, 80)   # 绿色 = 市级领导
    if "铜陵市" in s and "政协" in s:
        return (80, 150, 80)
    return (160, 160, 160)     # 灰色 = 其他


def org_color(org_type):
    t = str(org_type)
    if "党委" in t: return (200, 60, 60)
    elif "政府" in t or "公安" in t: return (60, 100, 200)
    elif "人大" in t: return (200, 150, 40)
    elif "政协" in t: return (200, 150, 40)
    elif "纪委" in t: return (160, 120, 40)
    elif "园区" in t: return (100, 160, 100)
    else: return (120, 120, 120)


# ── BUILD SQLITE DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Persons table
    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
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
            source TEXT
        )
    """)
    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    # Organizations table
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    # Positions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
        )
    """)
    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    # Relationships table
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)
    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


# ── BUILD GEXF GRAPH ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    # Build lookup
    person_role_map = {}
    for p in PERSONS:
        pid = p[0]
        person_role_map[pid] = p[8]  # current_post

    nodes_xml = []
    edges_xml = []
    edge_id = 0

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[8] or ""
        birth = p[4] or ""
        birthplace = p[5] or ""
        r, g_val, b = person_color(role)
        sz = 15.0
        if "区委书记" in role:
            sz = 20.0
        elif "区长" in role:
            sz = 18.0
        elif "人大" in role or "政协" in role:
            sz = 14.0
        elif "铜陵市委" in role or "铜陵市长" in role:
            sz = 15.0
        elif "铜陵市" in role and "政协" in role:
            sz = 15.0
        nodes_xml.append(f"""\
    <node id="{pid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{esc(role)}"/>
        <attvalue for="birth" value="{esc(birth)}"/>
        <attvalue for="birthplace" value="{esc(birthplace)}"/>
      </attvalues>
      <viz:color r="{r}" g="{g_val}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        r, g_val, b = org_color(o[2])
        nodes_xml.append(f"""\
    <node id="{oid}" label="{esc(label)}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{esc(o[2])}"/>
      </attvalues>
      <viz:color r="{r}" g="{g_val}" b="{b}" a="1.0"/>
      <viz:size value="8.0"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Work edges (person → org)
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        edge_id += 1
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{esc(title)}">
      <attvalues>
        <attvalue for="type" value="worked_at"/>
        <attvalue for="start" value="{esc(start or '')}"/>
        <attvalue for="end" value="{esc(end or '')}"/>
        <attvalue for="rank" value="{esc(rank or '')}"/>
      </attvalues>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # Relationship edges (person ↔ person)
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = "强关系" in typ or "职务接替" in typ
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{esc(context)}">
      <attvalues>
        <attvalue for="type" value="relationship"/>
        <attvalue for="strength" value="{esc(typ)}"/>
        <attvalue for="context" value="{esc(context)}"/>
      </attvalues>
      <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>
      <viz:thickness value="{thickness}"/>
    </edge>""")

    nodes_block = "\n".join(nodes_xml)
    edges_block = "\n".join(edges_xml)

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <meta>
    <creator>China-Gov-Network Investigation</creator>
    <description>义安区（铜陵市）领导班子工作关系网络 — 2026年7月</description>
    <date>2026-07-15</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="birth" title="Birth" type="string"/>
      <attribute id="birthplace" title="Birthplace" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Edge Type" type="string"/>
      <attribute id="start" title="Start Date" type="string"/>
      <attribute id="end" title="End Date" type="string"/>
      <attribute id="rank" title="Rank" type="string"/>
      <attribute id="strength" title="Strength" type="string"/>
      <attribute id="context" title="Context" type="string"/>
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
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  义安区（铜陵市市辖区）领导班子工作关系网络")
    print(f"  区划代码: 340706 | 类别: 市辖区")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n✅ Done.")
