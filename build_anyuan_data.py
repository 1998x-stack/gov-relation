#!/usr/bin/env python3
"""
萍乡市安源区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Anyuan District leadership.

Research note: Due to geo-restrictions, Chinese government websites (jxay.gov.cn, 
baike.baidu.com) and Chinese search engines were inaccessible from this environment.
All data marked with ⚠️ "待确认" requires verification from:
  - http://www.jxay.gov.cn/col/col5023/index.html (区委领导页面)
  - http://www.jxay.gov.cn/col/col5021/index.html (区政府领导页面)
  - Baidu Baike entries for each individual
  - 萍乡市委组织部任前公示
"""

import sqlite3
import os

# ── DATA ──
# Person ID convention: anyuan_{surname_givenname}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/anyuan_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/anyuan_network.gexf")

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
    
    # ═══ Top Leaders ═══
    # ⚠️ 安源区委书记 — 需从 jxay.gov.cn 确认
    ("anyuan_secretary_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委书记", "中共萍乡市安源区委员会", "⚠️ 待确认：jxay.gov.cn/col/col5023/"),
    
    # ⚠️ 安源区长 — 需确认
    ("anyuan_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区长", "安源区人民政府", "⚠️ 待确认：jxay.gov.cn/col/col5021/"),
    
    # ═══ Standing Committee (推测的区委常委标配岗位) ═══
    # ⚠️ 区委副书记（专职）
    ("anyuan_deputy_sec_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委副书记", "中共萍乡市安源区委员会", "⚠️ 待确认"),
    
    # ⚠️ 常务副区长
    ("anyuan_exec_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、常务副区长", "安源区人民政府", "⚠️ 待确认"),
    
    # ⚠️ 纪委书记
    ("anyuan_discipline_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、区纪委书记、区监委主任", "中共萍乡市安源区纪律检查委员会", "⚠️ 待确认"),
    
    # ⚠️ 组织部部长
    ("anyuan_org_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、组织部部长", "中共萍乡市安源区委组织部", "⚠️ 待确认"),
    
    # ⚠️ 宣传部部长
    ("anyuan_propaganda_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、宣传部部长", "中共萍乡市安源区委宣传部", "⚠️ 待确认"),
    
    # ⚠️ 政法委书记
    ("anyuan_legal_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、政法委书记", "中共萍乡市安源区委政法委员会", "⚠️ 待确认"),
    
    # ⚠️ 统战部部长
    ("anyuan_united_front_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、统战部部长", "中共萍乡市安源区委统一战线工作部", "⚠️ 待确认"),
    
    # ⚠️ 人武部部长/政委
    ("anyuan_armed_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区委常委、人武部政委（或部长）", "萍乡市安源区人民武装部", "⚠️ 待确认"),
    
    # ═══ Vice District Directors (副区长) ═══
    ("anyuan_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副区长", "安源区人民政府", "⚠️ 待确认"),
    ("anyuan_vice_mayor_02", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副区长", "安源区人民政府", "⚠️ 待确认"),
    ("anyuan_vice_mayor_03", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副区长", "安源区人民政府", "⚠️ 待确认"),
    ("anyuan_vice_mayor_04", "（待确认）", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副区长", "安源区人民政府", "⚠️ 待确认"),
    
    # ═══ NPC & CPPCC ═══
    ("anyuan_npc_chair_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区人大常委会主任", "萍乡市安源区人民代表大会常务委员会", "⚠️ 待确认"),
    ("anyuan_cppcc_chair_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "区政协主席", "中国人民政治协商会议萍乡市安源区委员会", "⚠️ 待确认"),
    
    # ═══ Pingxiang City-level Leaders (from existing build_pingxiang_data.py) ═══
    ("px_yu_zhengkun", "余正琨", "男", "汉族", "1971-01", "江西共青城", "待查", "中共党员", "待查",
     "萍乡市委书记", "中共萍乡市委员会", "https://zh.wikipedia.org/wiki/萍乡市"),
    ("px_fu_zhenghua", "傅正华", "男", "汉族", "1969-08", "江西吉安县", "南昌大学/法学学士", "1998-12", "1992-08",
     "萍乡市委副书记、市长", "萍乡市人民政府", "build_pingxiang_data.py"),
    ("px_bao_fengting", "鲍峰庭", "男", "汉族", "1968-03", "江西万载", "江西农业大学/大学，工程硕士", "1989-06", "1990-07",
     "萍乡市委专职副书记", "中共萍乡市委员会", "build_pingxiang_data.py"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("anyuan_party", "中共萍乡市安源区委员会", "党委", "县处级", "中共萍乡市委员会", "江西省萍乡市安源区"),
    ("anyuan_gov", "安源区人民政府", "政府", "县处级", "萍乡市人民政府", "江西省萍乡市安源区"),
    ("anyuan_discipline", "中共萍乡市安源区纪律检查委员会", "纪委", "县处级", "萍乡市纪委监委", "江西省萍乡市安源区"),
    ("anyuan_org", "中共萍乡市安源区委组织部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_propaganda", "中共萍乡市安源区委宣传部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_legal", "中共萍乡市安源区委政法委员会", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_united_front", "中共萍乡市安源区委统一战线工作部", "党委部门", "乡科级", "中共安源区委", "江西省萍乡市安源区"),
    ("anyuan_armed", "萍乡市安源区人民武装部", "军队", "县处级", "萍乡军分区", "江西省萍乡市安源区"),
    ("anyuan_npc", "萍乡市安源区人民代表大会常务委员会", "人大", "县处级", "萍乡市人大常委会", "江西省萍乡市安源区"),
    ("anyuan_cppcc", "中国人民政治协商会议萍乡市安源区委员会", "政协", "县处级", "萍乡市政协", "江西省萍乡市安源区"),
    ("anyuan_public_security", "萍乡市公安局安源分局", "公安", "乡科级", "萍乡市公安局", "江西省萍乡市安源区"),
    # City-level orgs
    ("px_party", "中共萍乡市委员会", "党委", "地市级", "中共江西省委员会", "江西省萍乡市"),
    ("px_gov", "萍乡市人民政府", "政府", "地市级", "江西省人民政府", "江西省萍乡市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)
    
    # ⚠️ 以下所有任职信息均待确认
    # 区委书记
    ("anyuan_secretary_01", "anyuan_party", "区委书记", "待查", "至今", "县处级正职", "⚠️ 待确认"),
    
    # 区长
    ("anyuan_mayor_01", "anyuan_gov", "区长", "待查", "至今", "县处级正职", "⚠️ 待确认"),
    ("anyuan_mayor_01", "anyuan_party", "区委副书记", "待查", "至今", "县处级正职", "兼任政府主官"),
    
    # 区委副书记（专职）
    ("anyuan_deputy_sec_01", "anyuan_party", "区委副书记（专职）", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    
    # 常务副区长
    ("anyuan_exec_vice_mayor_01", "anyuan_gov", "常务副区长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_exec_vice_mayor_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 纪委书记
    ("anyuan_discipline_01", "anyuan_discipline", "区纪委书记、区监委主任", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_discipline_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 组织部长
    ("anyuan_org_01", "anyuan_org", "组织部部长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_org_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 宣传部长
    ("anyuan_propaganda_01", "anyuan_propaganda", "宣传部部长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_propaganda_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 政法委书记
    ("anyuan_legal_01", "anyuan_legal", "政法委书记", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_legal_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 统战部长
    ("anyuan_united_front_01", "anyuan_united_front", "统战部部长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_united_front_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 人武部
    ("anyuan_armed_01", "anyuan_armed", "人武部政委（或部长）", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_armed_01", "anyuan_party", "区委常委", "待查", "至今", "县处级副职", "兼任"),
    
    # 副区长们
    ("anyuan_vice_mayor_01", "anyuan_gov", "副区长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_vice_mayor_02", "anyuan_gov", "副区长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_vice_mayor_03", "anyuan_gov", "副区长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    ("anyuan_vice_mayor_04", "anyuan_gov", "副区长", "待查", "至今", "县处级副职", "⚠️ 待确认"),
    
    # 人大主任
    ("anyuan_npc_chair_01", "anyuan_npc", "区人大常委会主任", "待查", "至今", "县处级正职", "⚠️ 待确认"),
    
    # 政协主席
    ("anyuan_cppcc_chair_01", "anyuan_cppcc", "区政协主席", "待查", "至今", "县处级正职", "⚠️ 待确认"),
    
    # City-level connections (from existing build_pingxiang_data.py)
    ("px_yu_zhengkun", "px_party", "萍乡市委书记", "2026-05", "至今", "正厅级", "接替刘烁"),
    ("px_fu_zhenghua", "px_gov", "萍乡市委副书记、市长", "2026-06", "至今", "正厅级", "2026.06.25正式当选"),
    ("px_bao_fengting", "px_party", "萍乡市委专职副书记", "2021-03", "至今", "副厅级", ""),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)
    
    # ⚠️ 以下关系待确认身份后补充
    ("anyuan_secretary_01", "anyuan_mayor_01", "强关系（推定）", "党政搭档", "安源区", "至今"),
    ("anyuan_secretary_01", "px_yu_zhengkun", "弱关系（推定）", "上下级关系", "萍乡市", "至今"),
    ("anyuan_mayor_01", "px_fu_zhenghua", "弱关系（推定）", "上下级关系", "萍乡市", "至今"),
    # Cross-city connections from existing data
    ("px_yu_zhengkun", "px_fu_zhenghua", "强关系", "党政搭档", "萍乡市", "2026-05至今"),
    ("px_fu_zhenghua", "px_bao_fengting", "弱关系", "市长×副书记", "萍乡市", "2026-至今"),
]


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
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
        "party": (212, 52, 46),
        "gov_leader": (51, 102, 204),
        "gov_deputy": (80, 130, 200),
        "discipline": (204, 119, 34),
        "other": (102, 102, 102),
        "org_party": (85, 51, 51),
        "org_gov": (51, 68, 85),
        "org_other": (68, 68, 68),
    }

    def color_for_person(pid):
        for p in PERSONS:
            if p[0] == pid:
                post = p[9] or ""
                if "书记" in post and "纪委" not in post:
                    return "party", 20.0
                elif "区长" in post or "县长" in post:
                    return "gov_leader", 20.0
                elif "常务副" in post:
                    return "gov_leader", 16.0
                elif "副区长" in post or "副县长" in post:
                    return "gov_deputy", 14.0
                elif "纪委书记" in post:
                    return "discipline", 14.0
                else:
                    return "other", 12.0
        return "other", 12.0

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

    nodes_xml = []
    edges_xml = []

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        g, sz = color_for_person(pid)
        r, gb, b = node_colors[g]
        title = f"{p[1]}\\n{p[9]}\\n{p[3]}·{p[4] if p[4] else '未知'}\\n籍贯: {p[5] if p[5] else '未知'}"
        nodes_xml.append(f"""\
    <node id="{pid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{p[9]}"/>
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
        nodes_xml.append(f"""\
    <node id="{oid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{o[2]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # work_at edges
    edge_id = 0
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        edge_id += 1
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{title}">
      <attvalues>
        <attvalue for="type" value="worked_at"/>
        <attvalue for="start" value="{start or ''}"/>
        <attvalue for="end" value="{end or ''}"/>
        <attvalue for="rank" value="{rank or ''}"/>
      </attvalues>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # relationship edges
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = "强关系" in typ
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{context}">
      <attvalues>
        <attvalue for="type" value="relationship"/>
        <attvalue for="strength" value="{typ}"/>
        <attvalue for="context" value="{context}"/>
        <attvalue for="overlap_org" value="{overlap_org}"/>
        <attvalue for="overlap_period" value="{overlap_period}"/>
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
    <description>萍乡市安源区领导班子工作关系网络 — 2026年7月（⚠️ 所有人员信息待确认）</description>
    <date>2026-07-14</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Edge Type" type="string"/>
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

    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
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
            # Count how many are confirmed vs pending
            c.execute("SELECT COUNT(*) FROM persons WHERE source LIKE '%待确认%'")
            pending = c.fetchone()[0]
            print(f"    └─ 待确认: {pending}, 已确认: {cnt - pending}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  萍乡市安源区领导班子工作关系网络 — 数据构建")
    print("  ⚠️  注意：由于网络环境受限，所有区级人员信息均为占位符")
    print("  ⚠️  请从 jxay.gov.cn 获取真实数据后更新此脚本")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("\n⚠️  IMPORTANT: This data contains placeholder entries only.")
    print("    To populate real data, access http://www.jxay.gov.cn/")
    print("    from within mainland China or via a proxy.")
    print("Done.")
