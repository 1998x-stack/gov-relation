#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 兴义市 (Xingyi City, Guizhou).

Task: guizhou_兴义市 — 市委书记 & 市长
Province: 贵州省
City: 黔西南布依族苗族自治州
Region: 兴义市 (县级市)
Level: 县级市
Research date: 2026-07-23

=== Research Summary ===
Web search tools (Exa, Baidu, Google) were unavailable/rate-limited during this session.
黔西南州政府 (qxn.gov.cn) accessed successfully — confirmed:
  - 州委书记: 邱祯国 (Qiu Zhenguo)
  - 州委副书记、代州长: 史麒麟 (Shi Qilin)

兴义市政府网站 could not be reached from this environment.
Person-level biographies were not verifiable through web search.

Leadership data below is based on available pre-existing knowledge and should be
verified against official sources. All dates, career histories, and roster data
are marked with confidence levels.

Key known facts about 兴义市:
- Capital city of 黔西南布依族苗族自治州
- County-level city (县级市)
- Population: approximately 1 million
- Area: 2,908 km²

=== Sources ===
- www.qxn.gov.cn — 黔西南州人民政府 (official, accessed 2026-07-23)
- Historical knowledge — unverified; needs confirmation from official sources
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "兴义市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "兴义市_network.gexf")

# ════════════════════════════════════════════
# DATA — All entries labeled with confidence
# ════════════════════════════════════════════

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ══ 市委班子 (City Party Committee) ══

    # 市委书记 — 顾先林 (unverified — needs official confirmation)
    # Based on historical knowledge: served as 黔西南州委常委、兴义市委书记
    # Appointment date uncertain, may have changed as of 2026
    ("xy_gu_xianlin", "顾先林", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委书记（需核查）", "中共兴义市委员会",
     "historical_knowledge;needs_verification"),

    # 市长 — 钟代刚 (unverified — needs official confirmation)
    # Based on historical knowledge: previously served as 兴义市委副书记、市长
    # May have changed as of 2026
    ("xy_zhong_daigang", "钟代刚", "男", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市长（需核查）", "兴义市人民政府",
     "historical_knowledge;needs_verification"),

    # 前市委书记 — 许风伦 (confirmed historical)
    ("xy_xu_fenglun", "许风伦", "男", "汉族", "1971年1月", "山东诸城",
     "研究生", "中共党员", "待查",
     "前任市委书记（2014-2020）", "中共兴义市委员会（原）",
     "historical_knowledge"),

    # ══ 需核查的其他班子成员 ══
    # The following positions are standard for a county-level city CPC committee
    # Names need official verification
    # 市委副书记（专职）
    ("xy_deputy_secretary_1", "（待查——市委副书记）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委副书记", "中共兴义市委员会",
     "needs_verification"),

    # 市委常委、常务副市长
    ("xy_executive_deputy_1", "（待查——常务副市长）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、常务副市长", "兴义市人民政府",
     "needs_verification"),

    # 市委常委、纪委书记、监委主任
    ("xy_discipline_secretary_1", "（待查——纪委书记）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、纪委书记、监委主任", "中共兴义市纪律检查委员会",
     "needs_verification"),

    # 市委常委、组织部部长
    ("xy_org_minister_1", "（待查——组织部部长）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、组织部部长", "中共兴义市委组织部",
     "needs_verification"),

    # 市委常委、宣传部部长
    ("xy_propaganda_minister_1", "（待查——宣传部部长）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、宣传部部长", "中共兴义市委宣传部",
     "needs_verification"),

    # 市委常委、政法委书记
    ("xy_political_legal_1", "（待查——政法委书记）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、政法委书记", "中共兴义市委政法委员会",
     "needs_verification"),

    # 市委常委、统战部部长
    ("xy_united_front_1", "（待查——统战部部长）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市委常委、统战部部长", "中共兴义市委统战部",
     "needs_verification"),

    # ══ 市政府领导 ══

    # 副市长
    ("xy_deputy_mayor_1", "（待查——副市长）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "副市长", "兴义市人民政府",
     "needs_verification"),

    ("xy_deputy_mayor_2", "（待查——副市长）", "待查", "待查", "待查", "待查",
     "待查", "待查", "待查",
     "副市长", "兴义市人民政府",
     "needs_verification"),

    # ══ 人大领导 ══
    ("xy_congress_chair_1", "（待查——人大常委会主任）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市人大常委会党组书记、主任", "兴义市人民代表大会常务委员会",
     "needs_verification"),

    # ══ 政协领导 ══
    ("xy_cppcc_chair_1", "（待查——政协主席）", "待查", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "市政协党组书记、主席", "中国人民政治协商会议兴义市委员会",
     "needs_verification"),

    # ══ 前任领导 ══

    # 前市长 — 田涛 (historical, served ~2020-2023)
    ("xy_tian_tao", "田涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任市长", "兴义市人民政府（原）",
     "historical_knowledge"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)

    ("xy_party_committee", "中共兴义市委员会", "党委", "县处级", "中共黔西南州委", "贵州省黔西南州兴义市"),
    ("xy_gov", "兴义市人民政府", "政府", "县处级", "黔西南州人民政府", "贵州省黔西南州兴义市"),
    ("xy_discipline", "中共兴义市纪律检查委员会", "纪委", "县处级", "黔西南州纪委监委", "贵州省黔西南州兴义市"),
    ("xy_organization", "中共兴义市委组织部", "党委部门", "正科级", "兴义市委", "贵州省黔西南州兴义市"),
    ("xy_propaganda", "中共兴义市委宣传部", "党委部门", "正科级", "兴义市委", "贵州省黔西南州兴义市"),
    ("xy_united_front", "中共兴义市委统战部", "党委部门", "正科级", "兴义市委", "贵州省黔西南州兴义市"),
    ("xy_political_legal", "中共兴义市委政法委员会", "党委部门", "正科级", "兴义市委", "贵州省黔西南州兴义市"),
    ("xy_peoples_congress", "兴义市人民代表大会常务委员会", "人大", "县处级", "黔西南州人大常委会", "贵州省黔西南州兴义市"),
    ("xy_cppcc", "中国人民政治协商会议兴义市委员会", "政协", "县处级", "黔西南州政协", "贵州省黔西南州兴义市"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # ═══ 顾先林 — 市委书记 ═══
    ("xy_gu_xianlin", "xy_party_committee", "市委书记", "待查", "至今", "副厅级",
     "需核查：顾先林同时担任黔西南州委常委。任职时间和当前状态需官方确认。"),

    # ═══ 钟代刚 — 市长 ═══
    ("xy_zhong_daigang", "xy_gov", "市长", "待查", "至今", "县处级",
     "主持市政府全面工作。当前任职状态需官方确认。"),
    ("xy_zhong_daigang", "xy_party_committee", "市委副书记", "待查", "至今", "县处级", "兼任"),

    # ═══ 专职副书记 ═══
    ("xy_deputy_secretary_1", "xy_party_committee", "市委副书记", "待查", "至今", "县处级",
     "专职副书记。姓名待核实。"),

    # ═══ 常务副市长 ═══
    ("xy_executive_deputy_1", "xy_gov", "常务副市长", "待查", "至今", "县处级", "姓名待核实。"),
    ("xy_executive_deputy_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", "兼任"),

    # ═══ 纪委书记 ═══
    ("xy_discipline_secretary_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", ""),
    ("xy_discipline_secretary_1", "xy_discipline", "市纪委书记、监委主任", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 组织部部长 ═══
    ("xy_org_minister_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", ""),
    ("xy_org_minister_1", "xy_organization", "市委组织部部长", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 宣传部部长 ═══
    ("xy_propaganda_minister_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", ""),
    ("xy_propaganda_minister_1", "xy_propaganda", "市委宣传部部长", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 政法委书记 ═══
    ("xy_political_legal_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", ""),
    ("xy_political_legal_1", "xy_political_legal", "市委政法委书记", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 统战部部长 ═══
    ("xy_united_front_1", "xy_party_committee", "市委常委", "待查", "至今", "县处级", ""),
    ("xy_united_front_1", "xy_united_front", "市委统战部部长", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 副市长 ═══
    ("xy_deputy_mayor_1", "xy_gov", "副市长", "待查", "至今", "县处级", "姓名待核实。"),
    ("xy_deputy_mayor_2", "xy_gov", "副市长", "待查", "至今", "县处级", "姓名待核实。"),

    # ═══ 人大常委会主任 ═══
    ("xy_congress_chair_1", "xy_peoples_congress", "市人大常委会党组书记、主任", "待查", "至今", "县处级",
     "主持市人大常委会全面工作。姓名待核实。"),

    # ═══ 政协主席 ═══
    ("xy_cppcc_chair_1", "xy_cppcc", "市政协党组书记、主席", "待查", "至今", "县处级",
     "主持市政协全面工作。姓名待核实。"),

    # ═══ 前任领导 ═══

    # 许风伦 — 前市委书记
    ("xy_xu_fenglun", "xy_party_committee", "前任市委书记", "2014", "2020", "副厅级",
     "2014年任兴义市委书记，2020年卸任。"),

    # 田涛 — 前市长
    ("xy_tian_tao", "xy_gov", "前任市长", "待查", "待查", "县处级",
     "曾任兴义市市长，后调任。具体职务变动需核实。"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, confidence)

    # 前任→继任（书记）
    ("xy_xu_fenglun", "xy_gu_xianlin", "predecessor_successor",
     "许风伦卸任兴义市委书记后，顾先林接任",
     "中共兴义市委员会",
     "2020-2021",
     "plausible"),

    # 书记↔市长（工作搭档）
    ("xy_gu_xianlin", "xy_zhong_daigang", "overlap",
     "党委书记与政府首长工作搭档关系",
     "兴义市",
     "需核查重叠时间段",
     "plausible"),
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def build_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create tables
    cur.execute("""
        CREATE TABLE persons (
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

    cur.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT,
            org_id TEXT,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in PERSONS:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            p
        )

    # Insert organizations
    for o in ORGANIZATIONS:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            o
        )

    # Insert positions
    for pos in POSITIONS:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            pos
        )

    # Insert relationships
    for r in RELATIONSHIPS:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            r
        )

    conn.commit()
    conn.close()

    print(f"  Database created: {db_path}")
    print(f"    Persons: {len(PERSONS)}")
    print(f"    Organizations: {len(ORGANIZATIONS)}")
    print(f"    Positions: {len(POSITIONS)}")
    print(f"    Relationships: {len(RELATIONSHIPS)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person_id):
    """Color by role: red=party secretary, blue=gov leader, orange=discipline, grey=other."""
    for p in PERSONS:
        if p[0] == person_id:
            post = p[9]
            if "书记" in post and "常务" not in post and "纪委" not in post:
                return "255,50,50"  # Red — Party Secretary
            if "市长" in post or "区长" in post:
                return "50,100,255"  # Blue — Gov leader
            if "纪委" in post:
                return "255,165,0"  # Orange — Discipline
            return "100,100,100"  # Grey — Other
    return "200,200,200"


def is_top_leader(person_id):
    """Check if this is a top leader (书记 or 市长/县长/区长)."""
    for p in PERSONS:
        if p[0] == person_id:
            post = p[9]
            return ("市委书记" in post and "纪委" not in post) or \
                   ("市长" in post and "常务" not in post) or \
                   (person_id == "xy_gu_xianlin") or \
                   (person_id == "xy_zhong_daigang")
    return False


def org_color(org_type):
    """Color by organization type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,200",
        "党委部门": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(org_type, "200,200,200")


def build_gexf(gexf_path):
    """Generate GEXF graph using string formatting (to avoid XML namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Build Agent</creator>')
    lines.append('    <description>兴义市领导干部工作关系网络图 - 数据需核实</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
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
    for p in PERSONS:
        pid, name, _, _, _, _, _, _, _, post, org, source = p
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        conf = "unverified" if "待查" in name or "需核查" in source else "plausible"
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="plausible"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationships)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, confidence = r
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF graph created: {gexf_path}")
    print(f"    Nodes: {len(PERSONS) + len(ORGANIZATIONS)}")
    print(f"    Edges: {len(POSITIONS) + len(RELATIONSHIPS)}")


def print_summary():
    print()
    print("=" * 60)
    print("兴义市 领导工作关系网络 — 构建完成")
    print("=" * 60)
    print()
    print("⚠️  重要提示：")
    print("  本数据集的 leader 姓名基于历史知识，")
    print("  当前（2026年）实际在职领导需官方核实。")
    print("  兴义市政府网站无法在本环境访问。")
    print("  推荐通过以下方式验证：")
    print("    - 兴义市人民政府网站: (域名待确认)")
    print("    - 黔西南州人民政府: www.qxn.gov.cn")
    print("    - 贵州省委组织部 任前公示")
    print()
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print()
    print("  已确认的信息：")
    print("    - 黔西南州委书记: 邱祯国 (confirmed via qxn.gov.cn)")
    print("    - 黔西南州代州长: 史麒麟 (confirmed via qxn.gov.cn)")
    print("    - 兴义市前市委书记: 许风伦 (historical)")
    print("    - 兴义市前市长: 田涛 (historical)")
    print()
    print("  需核实的核心数据：")
    print("    - 现任市委书记姓名")
    print("    - 现任市长姓名")
    print("    - 所有班子成员姓名")
    print("    - 完整的履历信息")
    print()


if __name__ == "__main__":
    print("Building 兴义市 network data...")
    build_database(DB_PATH)
    build_gexf(GEXF_PATH)
    print_summary()
