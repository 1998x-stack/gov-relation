#!/usr/bin/env python3
"""
重庆市沙坪坝区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Shapingba District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Parent City: (直辖市辖区)
Targets: 区委书记 & 区长

Research Notes:
- Current 区委书记: 林旭阳 (appointed July 2026, previously 北碚区委书记)
- Current 区长: 王银川 (elected April 2025, previously 重庆市财政局副局长)
- Leadership data compiled from cqspb.gov.cn official website and verified media reports (2026-07-16)
- Career timeline for 林旭阳 from Baidu Baike / public media reports
- Career timeline for 王银川 from official gov bio and media reports
- Some deputy positions may have changed; official cqspb.gov.cn leadership page as primary source

Sources:
- https://www.cqspb.gov.cn — official government website (primary)
- Baidu Baike — 林旭阳, 王银川, 祁美文, 屈克逊 entries
- 中国经济网 — leadership database
- 腾讯新闻 — appointment reports
- 澎湃新闻 — leadership news
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "沙坪坝区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "沙坪坝区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (Party Committee) ══
    ("spb_lin_xuyang", "林旭阳", "男", "汉族", "1975年5月", "福建莆田（福建安溪出生）",
     "在职研究生/经济学硕士（厦门大学）", "中共党员", "1998年？",
     "区委书记", "中共重庆市沙坪坝区委员会",
     "baike_baidu;media_reports;cqspb.gov.cn"),

    ("spb_wang_yinchuan", "王银川", "男", "汉族", "1976年7月", "待查",
     "大学/理学硕士", "中共党员", "待查",
     "区委副书记、区长", "重庆市沙坪坝区人民政府",
     "cqspb.gov.cn_official;media_reports;ce_cn"),

    ("spb_hu_yi", "户邑", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记（专职）", "中共重庆市沙坪坝区委员会",
     "cqspb.gov.cn;baike_baidu"),

    ("spb_he_yong", "何勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区政府常务副区长", "重庆市沙坪坝区人民政府",
     "cqspb.gov.cn"),

    ("spb_qu_kexun", "屈克逊", "男", "汉族", "1974年6月", "待查",
     "大学/经济学学士", "中共党员", "待查",
     "区委常委、西部科学城沙坪坝片区党工委书记", "中共西部（重庆）科学城沙坪坝片区工作委员会",
     "baike_baidu;cqspb.gov.cn"),

    ("spb_yang_yong", "阳勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区委政法委书记", "中共重庆市沙坪坝区委政法委员会",
     "cqspb.gov.cn;media_reports"),

    # ══ 前任领导 ══
    ("spb_qi_meiwen", "祁美文", "男", "汉族", "1973年9月", "重庆市开州区",
     "市委党校研究生/北京航空航天工程硕士", "中共党员", "1990年7月",
     "前任区委书记", "中共重庆市沙坪坝区委员会（原）",
     "baike_baidu;media_reports"),

    ("spb_tang_xiaoping", "唐小平", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记（更早）", "中共重庆市沙坪坝区委员会（原）",
     "media_reports"),

    ("spb_xiao_qinghua", "肖庆华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区长", "重庆市沙坪坝区人民政府（原）",
     "media_reports"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("spb_party_committee", "中共重庆市沙坪坝区委员会", "党委", "地厅级", "中共重庆市委", "重庆市沙坪坝区"),
    ("spb_gov", "重庆市沙坪坝区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市沙坪坝区"),
    ("spb_discipline", "中共重庆市沙坪坝区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市沙坪坝区"),
    ("spb_organization", "中共重庆市沙坪坝区委组织部", "党委部门", "正处级", "沙坪坝区委", "重庆市沙坪坝区"),
    ("spb_propaganda", "中共重庆市沙坪坝区委宣传部", "党委部门", "正处级", "沙坪坝区委", "重庆市沙坪坝区"),
    ("spb_united_front", "中共重庆市沙坪坝区委统战部", "党委部门", "正处级", "沙坪坝区委", "重庆市沙坪坝区"),
    ("spb_political_legal", "中共重庆市沙坪坝区委政法委员会", "党委部门", "正处级", "沙坪坝区委", "重庆市沙坪坝区"),
    ("spb_military_department", "重庆市沙坪坝区人民武装部", "军事", "正师级", "重庆警备区", "重庆市沙坪坝区"),
    ("spb_science_park", "中共西部（重庆）科学城沙坪坝片区工作委员会", "开发区", "正处级", "沙坪坝区委", "重庆市沙坪坝区"),
    ("spb_finance_bureau", "重庆市沙坪坝区财政局", "政府", "正处级", "沙坪坝区政府", "重庆市沙坪坝区"),
    ("spb_public_security", "重庆市公安局沙坪坝区分局", "公安", "正处级", "重庆市公安局", "重庆市沙坪坝区"),
    ("spb_procuratorate", "重庆市沙坪坝区人民检察院", "检察院", "正处级", "重庆市检察院", "重庆市沙坪坝区"),
    ("spb_court", "重庆市沙坪坝区人民法院", "法院", "正处级", "重庆市高院", "重庆市沙坪坝区"),
    ("spb_peoples_congress", "重庆市沙坪坝区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市沙坪坝区"),
    ("spb_cppcc", "中国人民政治协商会议重庆市沙坪坝区委员会", "政协", "地厅级", "重庆市政协", "重庆市沙坪坝区"),

    # External orgs for career timeline
    ("spb_xiamen_gov", "厦门市人民政府", "政府", "副省级", "福建省人民政府", "福建省厦门市"),
    ("spb_wuyishan_city", "武夷山市人民政府", "政府", "县级市", "南平市人民政府", "福建省武夷山市"),
    ("spb_nanping_party", "中共南平市委", "党委", "地厅级", "中共福建省委", "福建省南平市"),
    ("spb_putian_gov", "莆田市人民政府", "政府", "地厅级", "福建省人民政府", "福建省莆田市"),
    ("spb_beibei_party", "中共重庆市北碚区委", "党委", "地厅级", "中共重庆市委", "重庆市北碚区"),
    ("spb_chongqing_finance", "重庆市财政局", "政府", "地厅级", "重庆市人民政府", "重庆市"),
    ("spb_taizhou_gov", "浙江省台州市人民政府", "政府", "地厅级", "浙江省人民政府", "浙江省台州市"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 林旭阳 — 区委书记 ═══
    ("spb_lin_xuyang", "spb_party_committee", "区委书记", "2026-07", "至今", "正厅级",
     "主持区委全面工作。第十四届全国人大代表、重庆市第六届人大代表。"),
    ("spb_lin_xuyang", "spb_beibei_party", "北碚区委书记", "2024-10", "2026-07", "正厅级",
     "2024年10月跨省交流至重庆任北碚区委书记"),
    ("spb_lin_xuyang", "spb_putian_gov", "莆田市委副书记、市长", "2021", "2024-10", "正厅级",
     "莆田市委副书记、市长。2024年10月跨省交流至重庆任职。"),
    ("spb_lin_xuyang", "spb_nanping_party", "南平市委常委、组织部部长", "2019", "2021", "副厅级", ""),
    ("spb_lin_xuyang", "spb_wuyishan_city", "武夷山市委书记", "2017", "2019", "副厅级", ""),
    ("spb_lin_xuyang", "spb_wuyishan_city", "武夷山市长", "2016", "2017", "县处级正职", ""),
    ("spb_lin_xuyang", "spb_xiamen_gov", "厦门市思明区副区长", "2011", "2016", "副厅级",
     "正式级别为副厅级（副区级）"),
    ("spb_lin_xuyang", "spb_xiamen_gov", "厦门市委宣传部部务会成员、办公室主任", "2008", "2011", "正处级", ""),
    ("spb_lin_xuyang", "spb_xiamen_gov", "厦门市湖里团区委书记", "2003", "2008", "正处级", ""),
    ("spb_lin_xuyang", "spb_xiamen_gov", "厦门市湖里区殿前街道团委书记（起步）", "1998?", "2003", "科级",
     "早期基层履历，具体时间线待查"),

    # ═══ 王银川 — 区长 ═══
    ("spb_wang_yinchuan", "spb_gov", "区长", "2025-04", "至今", "正厅级",
     "主持区政府全面工作；负责审计工作。主管区政府办公室、区审计局。联系区人大常委会、区政协。"),
    ("spb_wang_yinchuan", "spb_party_committee", "区委副书记", "2024-12", "至今", "正厅级", "兼任"),
    ("spb_wang_yinchuan", "spb_taizhou_gov", "台州市副市长（挂职）", "2024-04", "2025-01", "副厅级",
     "挂职交流，东部省份跨省挂职副市长"),
    ("spb_wang_yinchuan", "spb_chongqing_finance", "重庆市财政局副局长", "2021?", "2024-04", "副厅级",
     "党组成员，分管预算、国库等"),
    ("spb_wang_yinchuan", "spb_chongqing_finance", "重庆市财政局总会计师", "2020?", "2021?", "正处级", ""),
    ("spb_wang_yinchuan", "spb_chongqing_finance", "重庆市财政局预算处处长", "2018?", "2020?", "正处级", ""),
    ("spb_wang_yinchuan", "spb_chongqing_finance", "重庆市财政局研究室主任", "2015?", "2018?", "正处级", ""),
    ("spb_wang_yinchuan", "spb_chongqing_finance", "重庆市财政局办公室副主任", "2012?", "2015?", "副处级",
     "早期财政系统经历，具体时间线待查"),

    # ═══ 户邑 — 区委副书记 ═══
    ("spb_hu_yi", "spb_party_committee", "区委副书记", "待查", "至今", "正厅级",
     "专职副书记，兼任区委党校（区行政学校）校长、区委国安办主任"),

    # ═══ 何勇 — 常务副区长 ═══
    ("spb_he_yong", "spb_gov", "区委常委、区政府常务副区长", "待查", "至今", "副厅级",
     "一级巡视员，区政府党组副书记。负责区政府常务工作；分管发展改革、财政、税务、统计、国资等"),
    ("spb_he_yong", "spb_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 屈克逊 — 科学城党工委书记 ═══
    ("spb_qu_kexun", "spb_science_park", "区委常委、西部科学城沙坪坝片区党工委书记", "待查", "至今", "副厅级",
     "兼任西部（重庆）科学城沙坪坝片区党工委书记"),
    ("spb_qu_kexun", "spb_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 阳勇 — 政法委书记 ═══
    ("spb_yang_yong", "spb_political_legal", "区委常委、区委政法委书记", "待查", "至今", "副厅级", ""),

    # ═══ 前任领导 ═══
    ("spb_qi_meiwen", "spb_party_committee", "前任区委书记", "2024-09", "2026-07", "正厅级",
     "2024年9月-2026年7月任区委书记。此前任重庆市酉阳县委书记、重庆市扶贫办主任等职。"),
    ("spb_tang_xiaoping", "spb_party_committee", "前任区委书记（更早）", "2021-12?", "2024-09", "正厅级",
     "前面一任区委书记，2024年9月离任"),
    ("spb_xiao_qinghua", "spb_gov", "前任区长", "待查", "2024?", "正厅级",
     "王银川的前任区长"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 林旭阳 ↔ 王银川 — 党政正职搭档 ═══
    ("spb_lin_xuyang", "spb_wang_yinchuan", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市沙坪坝区委员会;重庆市沙坪坝区人民政府", "2026-07至今"),

    # ═══ 林旭阳 ↔ 户邑 — 书记-副书记 ═══
    ("spb_lin_xuyang", "spb_hu_yi", "superior_subordinate",
     "区委书记与专职副书记（区委日常工作协调）",
     "中共重庆市沙坪坝区委员会", "2026-07至今"),

    # ═══ 林旭阳 ↔ 何勇 — 书记-常务副区长 ═══
    ("spb_lin_xuyang", "spb_he_yong", "superior_subordinate",
     "区委书记与常务副区长（区政府常务工作）",
     "中共重庆市沙坪坝区委员会", "2026-07至今"),

    # ═══ 林旭阳 ↔ 屈克逊 — 书记-区委常委 ═══
    ("spb_lin_xuyang", "spb_qu_kexun", "superior_subordinate",
     "区委书记与区委常委（科学城片区工作）",
     "中共重庆市沙坪坝区委员会", "2026-07至今"),

    # ═══ 林旭阳 ↔ 阳勇 — 书记-政法委书记 ═══
    ("spb_lin_xuyang", "spb_yang_yong", "superior_subordinate",
     "区委书记与政法委书记（政法系统工作）",
     "中共重庆市沙坪坝区委员会", "2026-07至今"),

    # ═══ 王银川 ↔ 何勇 — 区长-常务副区长 ═══
    ("spb_wang_yinchuan", "spb_he_yong", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市沙坪坝区人民政府", "2025-04至今"),

    # ═══ 王银川 ↔ 户邑 — 区长-副书记 ═══
    ("spb_wang_yinchuan", "spb_hu_yi", "overlap",
     "区长与区委副书记（区委区政府协调）",
     "中共重庆市沙坪坝区委员会", "2025-04至今"),

    # ═══ 林旭阳 — 前任书记（祁美文） ═══
    ("spb_lin_xuyang", "spb_qi_meiwen", "predecessor_successor",
     "林旭阳接替祁美文任沙坪坝区委书记",
     "中共重庆市沙坪坝区委员会", "2026-07"),

    # ═══ 祁美文 — 前任书记（唐小平） ═══
    ("spb_qi_meiwen", "spb_tang_xiaoping", "predecessor_successor",
     "祁美文接替唐小平任沙坪坝区委书记",
     "中共重庆市沙坪坝区委员会", "2024-09"),

    # ═══ 王银川 — 前任区长（肖庆华） ═══
    ("spb_wang_yinchuan", "spb_xiao_qinghua", "predecessor_successor",
     "王银川接替肖庆华任沙坪坝区长",
     "重庆市沙坪坝区人民政府", "2024-2025"),

    # ═══ 祁美文 ↔ 户邑 — 前任书记-副书记 ═══
    ("spb_qi_meiwen", "spb_hu_yi", "superior_subordinate",
     "前任区委书记与专职副书记（曾共同工作）",
     "中共重庆市沙坪坝区委员会", "2024-2026"),

    # ═══ 祁美文 ↔ 何勇 — 前任书记-常委 ═══
    ("spb_qi_meiwen", "spb_he_yong", "superior_subordinate",
     "前任区委书记与区委常委、常务副区长",
     "中共重庆市沙坪坝区委员会", "2024-2026"),
]

# ════════════════════════════════════════════
# SQLITE SETUP
# ════════════════════════════════════════════

def create_database():
    """Create SQLite database with persons, organizations, positions, relationships tables."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
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

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
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

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT,
            person_b TEXT,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF GENERATION
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(person_id):
    return person_id in ("spb_lin_xuyang", "spb_wang_yinchuan", "spb_qi_meiwen", "spb_tang_xiaoping", "spb_xiao_qinghua")

def is_organization(node_id):
    return node_id.startswith("o")

def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id == "spb_lin_xuyang" or person_id == "spb_qi_meiwen" or person_id == "spb_tang_xiaoping":
        return "255,50,50"       # Red — Party Secretary
    elif person_id == "spb_wang_yinchuan" or person_id == "spb_xiao_qinghua":
        return "50,100,255"      # Blue — Government head
    elif person_id == "spb_yang_yong":
        return "255,165,0"       # Orange — Discipline/政法
    else:
        return "100,100,100"     # Grey — Others

def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "公安": "200,200,200",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "军事": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "法院": "200,200,255",
        "检察院": "200,200,255",
    }
    return color_map.get(org_type, "200,200,200")

def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市沙坪坝区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="level" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[8]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="person"/>')
        lines.append(f'          <attvalue for="3" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        olevel = o[3]
        c = org_color(oid, otype)
        lines.append(f'      <node id="o{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(olevel)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at via positions)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3] if pos[3] else ""
        end = pos[4] if pos[4] else ""
        eid += 1
        period = f"{start}-{end}" if start or end else ""
        lines.append(f'      <edge id="e{eid}" source="p{esc(pid)}" target="o{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(oid)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        overlap_org = r[4]
        overlap_period = r[5]
        weight = "2.0"  # person-person edges stronger than person-org
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{esc(pa)}" target="p{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(overlap_period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════

def print_summary():
    print(f"\n{'='*60}")
    print(f"  重庆市沙坪坝区 领导网络数据")
    print(f"{'='*60}")
    print(f"  人物: {len(PERSONS)}")
    print(f"  机构: {len(ORGANIZATIONS)}")
    print(f"  任职记录: {len(POSITIONS)}")
    print(f"  关系边: {len(RELATIONSHIPS)}")
    print(f"{'='*60}")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"{'='*60}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    generate_gexf()
    print_summary()
