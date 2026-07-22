#!/usr/bin/env python3
"""
尤溪县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Youxi County leadership.

Sources:
- 尤溪县人民政府官网 (fjyx.gov.cn) — news articles and leadership activities
- Wikipedia (zh.wikipedia.org) — Youxi County overview
- Baidu Baike (baike.baidu.com) — biographical data (limited access)

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "尤溪县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "尤溪县_network.gexf")
PERSONS_DIR = STAGING_DIR

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

AS_OF = "2026-07-16"

# Person ID convention: youxi_{surname_givenname}
PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 肖世龙
    # Source: Wikipedia, fjyx.gov.cn news articles
    ("youxi_xiao_shilong", "肖世龙", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共尤溪县委员会",
     "https://zh.wikipedia.org/wiki/%E5%B0%A4%E6%BA%AA%E5%8E%BF — Wikipedia confirms 肖世龙 as current 县委书记"),

    # 代县长 — 曾志华 (as of 2026-07-08)
    # Source: fjyx.gov.cn — 2026-07-09 "尤溪县政府组成部门工作会议召开"
    ("youxi_zeng_zhihua", "曾志华", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、代县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm — 以县委副书记、代县长身份主持会议"),

    # ═══ Standing Committee Members ═══

    # 常务副县长 — 蓝积文
    ("youxi_lan_jiwen", "蓝积文", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm — 县领导蓝积文参加会议"),

    # 县委常委、副县长 — 魏帅
    ("youxi_wei_shuai", "魏帅", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm — 县领导魏帅参加会议"),

    # 县委常委、宣传部部长 — 邱建蓉 (女)
    ("youxi_qiu_jianrong", "邱建蓉", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共尤溪县委宣传部",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202606/t20260608_2214400.htm — 出席网络达人活动"),

    # 县委常委、人武部政委 — 李晋
    ("youxi_li_jin", "李晋", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县人武部政委", "尤溪县人民武装部",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260708_2238262.htm — 参加人武部主官任职命令宣布大会"),

    # ═══ Vice County Mayors ═══
    ("youxi_wu_jianrong", "吴建荣", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_cai_xiaobin", "蔡晓斌", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_hu_fengpeng", "胡凤鹏", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_feng_suping", "冯素萍", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_wan_boshen", "万博绅", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_chen_huijuan", "陈慧娟", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260709_2238308.htm"),
    ("youxi_zhan_liyzhong", "詹立忠", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "尤溪县人民政府",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202606/t20260624_2231640.htm — 链博会招商签约"),

    # ═══ NPC & CPPCC ═══
    ("youxi_wu_zuoming", "吴佐明", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "尤溪县人民代表大会常务委员会",
     "Baidu Baike — 尤溪县 overview"),
    ("youxi_lin_yongtian", "林永田", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议尤溪县委员会",
     "Baidu Baike — 尤溪县 overview"),

    # ═══ Predecessors ═══
    # 邱烈泉 — 前任县长 (until ~June 2026)
    ("youxi_qiu_liequan", "邱烈泉", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "（原县长，已离任）", "尤溪县人民政府（前任）",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202606/t20260608_2214399.htm — 2026-06-05仍以县长身份出席"),

    # ═══ 县人武部 ═══
    ("youxi_lin_ning", "林宁", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人武部部长", "尤溪县人民武装部",
     "https://www.fjyx.gov.cn/zwgk/gzdt/202607/t20260708_2238262.htm — 人武部新任职"),
]

# ── Organizations ──
ORGANIZATIONS = [
    ("中共尤溪县委员会", "党委", "县级", "中共三明市委员会", "尤溪县"),
    ("尤溪县人民政府", "政府", "县级", "三明市人民政府", "尤溪县"),
    ("中共尤溪县委宣传部", "党委", "部门", "中共尤溪县委员会", "尤溪县"),
    ("尤溪县人民武装部", "政府", "部门", "尤溪县人民政府", "尤溪县"),
    ("尤溪县人民代表大会常务委员会", "人大", "县级", "尤溪县", "尤溪县"),
    ("中国人民政治协商会议尤溪县委员会", "政协", "县级", "尤溪县", "尤溪县"),
]

# ── Positions ──
# (person_id, org_name, title, start_date, end_date, rank, note)
POSITIONS = [
    # Current
    ("youxi_xiao_shilong", "中共尤溪县委员会", "县委书记", "待查", "任职中", "正处级", ""),
    ("youxi_zeng_zhihua", "尤溪县人民政府", "县委副书记、代县长", "2026-07", "任职中", "正处级", "2026年7月由代县长主持县政府工作"),
    ("youxi_lan_jiwen", "尤溪县人民政府", "县委常委、常务副县长", "待查", "任职中", "副处级", ""),
    ("youxi_wei_shuai", "尤溪县人民政府", "县委常委、副县长", "待查", "任职中", "副处级", ""),
    ("youxi_qiu_jianrong", "中共尤溪县委宣传部", "县委常委、宣传部部长", "待查", "任职中", "副处级", ""),
    ("youxi_li_jin", "尤溪县人民武装部", "县委常委、县人武部政委", "2026-07", "任职中", "副处级", "2026年7月8日人武部主官任职命令宣布大会"),
    ("youxi_lin_ning", "尤溪县人民武装部", "县人武部部长", "2026-07", "任职中", "副处级", "新任职"),
    ("youxi_wu_jianrong", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_cai_xiaobin", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_hu_fengpeng", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_feng_suping", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_wan_boshen", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_chen_huijuan", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_zhan_liyzhong", "尤溪县人民政府", "副县长", "待查", "任职中", "副处级", ""),
    ("youxi_wu_zuoming", "尤溪县人民代表大会常务委员会", "县人大常委会主任", "待查", "任职中", "正处级", ""),
    ("youxi_lin_yongtian", "中国人民政治协商会议尤溪县委员会", "县政协主席", "待查", "任职中", "正处级", ""),

    # Historical
    ("youxi_qiu_liequan", "尤溪县人民政府", "县委副书记、县长", "待查", "2026-06", "正处级", "2026年6月5日最后一次以县长身份公开露面"),
]

# ── Relationships ──
# (person_a, person_b, type, context, overlap_org, overlap_period, confidence, direction)
RELATIONSHIPS = [
    ("youxi_zeng_zhihua", "youxi_xiao_shilong", "superior_subordinate",
     "曾志华（代县长）在肖世龙（书记）领导下主持县政府工作",
     "中共尤溪县委员会/尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_lan_jiwen", "youxi_zeng_zhihua", "overlap",
     "蓝积文作为常务副县长协助代县长曾志华工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_zeng_zhihua", "youxi_qiu_liequan", "predecessor_successor",
     "曾志华接替邱烈泉出任县长（代）",
     "尤溪县人民政府", "2026-06/07", "confirmed", "other_to_person"),
    ("youxi_lan_jiwen", "youxi_qiu_liequan", "overlap",
     "蓝积文在邱烈泉任县长期间担任常务副县长",
     "尤溪县人民政府", "~2026-06", "confirmed", "undirected"),
    # All deputy county magistrates work together in county government
    ("youxi_wu_jianrong", "youxi_zeng_zhihua", "overlap",
     "吴建荣副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_cai_xiaobin", "youxi_zeng_zhihua", "overlap",
     "蔡晓斌副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_hu_fengpeng", "youxi_zeng_zhihua", "overlap",
     "胡凤鹏副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_feng_suping", "youxi_zeng_zhihua", "overlap",
     "冯素萍副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_wan_boshen", "youxi_zeng_zhihua", "overlap",
     "万博绅副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
    ("youxi_chen_huijuan", "youxi_zeng_zhihua", "overlap",
     "陈慧娟副县长在代县长曾志华领导下工作",
     "尤溪县人民政府", "2026-07至今", "confirmed", "other_to_person"),
]


# ═══════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def build_db():
    """Create SQLite database with persons, organizations, positions, relationships."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, type TEXT,
        level TEXT, parent TEXT, location TEXT
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_name TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT, confidence TEXT,
        direction TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations (name,type,level,parent,location) VALUES (?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT OR REPLACE INTO positions (person_id,org_name,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT OR REPLACE INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period,confidence,direction) VALUES (?,?,?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def build_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>尤溪县领导班子工作关系网络 — Party Secretary: 肖世龙, Acting County Mayor: 曾志华</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # ── Person node color mapping ──
    def person_color(pid, post):
        if "县委书记" in post or "书记" == post.split("、")[0]:
            return "255,50,50"  # Red
        elif "县长" in post or "代县长" in post:
            return "50,100,255"  # Blue
        elif "纪委书记" in post:
            return "255,165,0"  # Orange
        else:
            return "100,100,100"  # Grey

    def person_size(post):
        if any(k in post for k in ["县委书记", "县长", "代县长", "人大常委会主任", "政协主席"]):
            return "20.0"
        return "12.0"

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid, name, _, _, _, _, _, _, _, post, org, src = p
        c = person_color(pid, post)
        sz = person_size(post)
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    for o in ORGANIZATIONS:
        name, otype, _, _, _ = o
        oc = org_colors.get(otype, "200,200,200")
        lines.append(f'      <node id="org_{esc(name)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid, org_name, title, start, end, _, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="org_{esc(org_name)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(note)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, confidence, direction = r
        eid += 1
        weight = "2.0" if confidence == "confirmed" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(overlap_period.split("至今")[0].strip() if "至今" in overlap_period else overlap_period)}"/>')
        lines.append(f'          <attvalue for="3" value="{"至今" if "至今" in overlap_period else overlap_period}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_summary():
    """Print summary statistics."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\n📊 数据摘要 / Summary")
    print("=" * 40)
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")

    print(f"\n  As of date: {AS_OF}")
    conn.close()


if __name__ == "__main__":
    print("🔨 构建尤溪县领导班子工作关系网络数据...")
    print(f"  暂存目录: {STAGING_DIR}")
    build_db()
    build_gexf()
    print_summary()
    print("\n✅ 构建完成 / Build complete")
