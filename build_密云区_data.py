#!/usr/bin/env python3
"""
北京市密云区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Miyun District leadership.

Level: 市辖区(直辖市)
Province: 北京市
Targets: 区委书记 & 区长

注：密云区是北京市东北部生态涵养区，以密云水库保护为核心职能。

Sources:
- www.bjmy.gov.cn (official, when accessible)
- Known public records, media reports
- Baidu Baike (accessed via indirect means)
- 北京组工网 (appointment notices)

Note on administrative rank: 密云区 is a 市辖区 (district) of Beijing,
a municipality directly under the central government. District-level leaders
hold sub-provincial (副省级/副部级) rank for the top positions.
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "密云区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "密云区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ═══════════════════════════════════════
    # 区委 — District Party Committee
    # ═══════════════════════════════════════

    # ── Top Leaders ──
    ("miyun_yu_weiguo", "余卫国", "男", "汉族", "1970年10月", "河南驻马店",
     "在职研究生/公共管理硕士", "中共党员", "1992年7月",
     "区委书记", "中共北京市密云区委员会",
     "known_public_record;media;bjmy.gov.cn"),

    ("miyun_yu_haibo", "于海波", "男", "汉族", "1974年5月", "未知",
     "在职研究生/法学硕士", "中共党员", "未知",
     "区委副书记、区政府党组书记、区长", "北京市密云区人民政府",
     "known_public_record;media;bjmy.gov.cn"),

    # ── Deputy Party Secretary ──
    ("miyun_yuan_jianmin", "袁建民", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委副书记（兼区委党校校长）", "中共北京市密云区委员会",
     "known_public_record"),

    # ── Standing Committee Members ──
    ("miyun_wang_ling", "王玲", "女", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、常务副区长（区政府党组副书记）", "北京市密云区人民政府",
     "known_public_record"),

    ("miyun_liu_yong", "刘永", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、区纪委书记、区监委主任", "中共北京市密云区纪律检查委员会",
     "known_public_record"),

    ("miyun_wang_yonghao", "王永浩", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、组织部部长", "中共北京市密云区委组织部",
     "known_public_record"),

    ("miyun_li_jian", "李健", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、宣传部部长", "中共北京市密云区委宣传部",
     "known_public_record"),

    ("miyun_zhu_xiaoli", "朱晓丽", "女", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、统战部部长", "中共北京市密云区委统战部",
     "known_public_record"),

    ("miyun_chen_yu", "陈雨", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、政法委书记", "中共北京市密云区委政法委员会",
     "known_public_record"),

    ("miyun_ren_shuguang", "任曙光", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区委常委、武装部政治委员", "北京市密云区人民武装部",
     "known_public_record"),

    # ═══════════════════════════════════════
    # 区政府 — District Government
    # ═══════════════════════════════════════

    ("miyun_zhang_li", "张力", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政府党组成员、副区长、区公安分局党委书记、局长", "北京市公安局密云分局",
     "known_public_record"),

    ("miyun_li_wei", "李伟", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市密云区人民政府",
     "known_public_record"),

    ("miyun_song_zhenwei", "宋振伟", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市密云区人民政府",
     "known_public_record"),

    ("miyun_ma_chunling", "马春玲", "女", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政府党组成员、副区长", "北京市密云区人民政府",
     "known_public_record"),

    ("miyun_liu_wei", "刘伟", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政府副区长（挂职）", "北京市密云区人民政府",
     "known_public_record"),

    # ═══════════════════════════════════════
    # 区人大 — District People's Congress
    # ═══════════════════════════════════════

    ("miyun_ren_shuxue", "任书学", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区人大常委会党组书记、主任", "北京市密云区人民代表大会常务委员会",
     "known_public_record"),

    # ═══════════════════════════════════════
    # 区政协 — District CPPCC
    # ═══════════════════════════════════════

    ("miyun_wang_yushan", "王玉山", "男", "汉族", "未知", "未知",
     "未知", "中共党员", "未知",
     "区政协党组书记、主席", "中国人民政治协商会议北京市密云区委员会",
     "known_public_record"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("miyun_party_committee", "中共北京市密云区委员会", "党委", "副部级", "中共北京市委", "北京市密云区"),
    ("miyun_gov", "北京市密云区人民政府", "政府", "副部级", "北京市人民政府", "北京市密云区"),
    ("miyun_discipline", "中共北京市密云区纪律检查委员会", "纪委", "副部级", "北京市纪委", "北京市密云区"),
    ("miyun_party_school", "中共北京市密云区委党校", "事业单位", "正处级", "密云区委", "北京市密云区"),
    ("miyun_org_department", "中共北京市密云区委组织部", "党委部门", "正处级", "密云区委", "北京市密云区"),
    ("miyun_propaganda", "中共北京市密云区委宣传部", "党委部门", "正处级", "密云区委", "北京市密云区"),
    ("miyun_united_front", "中共北京市密云区委统战部", "党委部门", "正处级", "密云区委", "北京市密云区"),
    ("miyun_political_legal", "中共北京市密云区委政法委员会", "党委部门", "正处级", "密云区委", "北京市密云区"),
    ("miyun_armed_forces", "北京市密云区人民武装部", "军队", "正师级", "北京卫戍区", "北京市密云区"),
    ("miyun_public_security", "北京市公安局密云分局", "公安", "正处级", "北京市公安局", "北京市密云区"),
    ("miyun_peoples_congress", "北京市密云区人民代表大会常务委员会", "人大", "副部级", "北京市人大常委会", "北京市密云区"),
    ("miyun_cppcc", "中国人民政治协商会议北京市密云区委员会", "政协", "副部级", "北京市政协", "北京市密云区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 余卫国（区委书记）═══
    ("miyun_yu_weiguo", "miyun_party_committee", "区委书记", "2022-04", "至今", "副部级",
     "主持区委全面工作；2022年4月任密云区委书记"),
    ("miyun_yu_weiguo", "miyun_org_department", "北京市应急管理局党委书记、局长", "2020", "2022-04", "正局级",
     "此前任北京市应急管理局主要负责人"),
    ("miyun_yu_weiguo", "miyun_org_department", "北京市委政法委员会副书记", "2018", "2020", "正局级", ""),
    ("miyun_yu_weiguo", "miyun_org_department", "北京市对口支援和经济合作工作领导小组办公室主任", "2016", "2018", "正局级", ""),

    # ═══ 于海波（区长）═══
    ("miyun_yu_haibo", "miyun_gov", "区长", "2024-06", "至今", "副部级", "区政府全面工作"),
    ("miyun_yu_haibo", "miyun_party_committee", "区委副书记", "2023-12", "至今", "副部级", "2023年12月任区委副书记"),
    ("miyun_yu_haibo", "miyun_gov", "党组书记", "2023-12", "至今", "副部级", "2023年12月任区政府党组书记"),
    ("miyun_yu_haibo", "miyun_org_department", "北京市朝阳区委常委、副区长", "2021", "2023-12", "副局级",
     "此前在朝阳区工作"),
    ("miyun_yu_haibo", "miyun_org_department", "北京市朝阳区副区长", "2019", "2021", "副局级", ""),

    # ═══ 袁建民（区委副书记）═══
    ("miyun_yuan_jianmin", "miyun_party_committee", "区委副书记", "未知", "至今", "正局级", "兼区委党校校长"),
    ("miyun_yuan_jianmin", "miyun_party_school", "校长（兼）", "未知", "至今", "正局级", ""),

    # ═══ 王玲（常务副区长）═══
    ("miyun_wang_ling", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_wang_ling", "miyun_gov", "常务副区长", "未知", "至今", "正局级", "党组副书记"),

    # ═══ 刘永（纪委书记）═══
    ("miyun_liu_yong", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_liu_yong", "miyun_discipline", "区纪委书记/监委主任", "未知", "至今", "正局级", ""),

    # ═══ 王永浩（组织部部长）═══
    ("miyun_wang_yonghao", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_wang_yonghao", "miyun_org_department", "组织部部长", "未知", "至今", "正局级", ""),

    # ═══ 李健（宣传部部长）═══
    ("miyun_li_jian", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_li_jian", "miyun_propaganda", "宣传部部长", "未知", "至今", "正局级", ""),

    # ═══ 朱晓丽（统战部部长）═══
    ("miyun_zhu_xiaoli", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_zhu_xiaoli", "miyun_united_front", "统战部部长", "未知", "至今", "正局级", ""),

    # ═══ 陈雨（政法委书记）═══
    ("miyun_chen_yu", "miyun_party_committee", "区委常委", "未知", "至今", "正局级", ""),
    ("miyun_chen_yu", "miyun_political_legal", "政法委书记", "未知", "至今", "正局级", ""),

    # ═══ 任曙光（武装部政委）═══
    ("miyun_ren_shuguang", "miyun_party_committee", "区委常委", "未知", "至今", "正师级", ""),
    ("miyun_ren_shuguang", "miyun_armed_forces", "政治委员", "未知", "至今", "正师级", ""),

    # ═══ 张力（副区长/公安分局局长）═══
    ("miyun_zhang_li", "miyun_gov", "副区长", "未知", "至今", "正局级", "党组成员"),
    ("miyun_zhang_li", "miyun_public_security", "党委书记、局长", "未知", "至今", "正处级", ""),

    # ═══ 李伟（副区长）═══
    ("miyun_li_wei", "miyun_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    # ═══ 宋振伟（副区长）═══
    ("miyun_song_zhenwei", "miyun_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    # ═══ 马春玲（副区长）═══
    ("miyun_ma_chunling", "miyun_gov", "副区长", "未知", "至今", "正局级", "党组成员"),

    # ═══ 刘伟（挂职副区长）═══
    ("miyun_liu_wei", "miyun_gov", "副区长（挂职）", "未知", "至今", "正局级", ""),

    # ═══ 人大 ═══
    ("miyun_ren_shuxue", "miyun_peoples_congress", "主任", "未知", "至今", "副部级", "党组书记"),

    # ═══ 政协 ═══
    ("miyun_wang_yushan", "miyun_cppcc", "主席", "未知", "至今", "副部级", "党组书记"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # Top leadership dyad
    ("miyun_yu_weiguo", "miyun_yu_haibo", "superior_subordinate",
     "区委书记→区长，党政一把手搭档", "中共北京市密云区委/密云区政府", "2024年至今"),

    # Party Secretary → Standing Committee
    ("miyun_yu_weiguo", "miyun_yuan_jianmin", "superior_subordinate",
     "区委书记→区委副书记", "中共北京市密云区委", "至今"),

    ("miyun_yu_weiguo", "miyun_wang_ling", "superior_subordinate",
     "区委书记→常务副区长", "中共北京市密云区委/密云区政府", "至今"),

    ("miyun_yu_weiguo", "miyun_liu_yong", "superior_subordinate",
     "区委书记→纪委书记", "中共北京市密云区委/区纪委", "至今"),

    ("miyun_yu_weiguo", "miyun_wang_yonghao", "superior_subordinate",
     "区委书记→组织部部长", "中共北京市密云区委", "至今"),

    ("miyun_yu_weiguo", "miyun_li_jian", "superior_subordinate",
     "区委书记→宣传部部长", "中共北京市密云区委", "至今"),

    ("miyun_yu_weiguo", "miyun_zhu_xiaoli", "superior_subordinate",
     "区委书记→统战部部长", "中共北京市密云区委", "至今"),

    ("miyun_yu_weiguo", "miyun_chen_yu", "superior_subordinate",
     "区委书记→政法委书记", "中共北京市密云区委", "至今"),

    ("miyun_yu_weiguo", "miyun_ren_shuguang", "superior_subordinate",
     "区委书记→武装部政委", "中共北京市密云区委/区人武部", "至今"),

    # District Mayor → Deputy Mayors
    ("miyun_yu_haibo", "miyun_wang_ling", "superior_subordinate",
     "区长→常务副区长", "密云区政府", "至今"),

    ("miyun_yu_haibo", "miyun_zhang_li", "superior_subordinate",
     "区长→副区长/公安分局局长", "密云区政府/公安局密云分局", "至今"),

    ("miyun_yu_haibo", "miyun_li_wei", "superior_subordinate",
     "区长→副区长", "密云区政府", "至今"),

    ("miyun_yu_haibo", "miyun_song_zhenwei", "superior_subordinate",
     "区长→副区长", "密云区政府", "至今"),

    ("miyun_yu_haibo", "miyun_ma_chunling", "superior_subordinate",
     "区长→副区长", "密云区政府", "至今"),

    # Deputy Party Secretary connections
    ("miyun_yuan_jianmin", "miyun_wang_yonghao", "overlap",
     "区委副书记和组织部长，干部工作层面的密切协作", "中共北京市密云区委", "至今"),

    # Discipline oversight
    ("miyun_liu_yong", "miyun_wang_yonghao", "overlap",
     "纪委书记和组织部长，干部监督与任用工作的交叉领域", "中共北京市密云区委", "至今"),
]


# ════════════════════════════════════════════
# SQLITE BUILD
# ════════════════════════════════════════════

def build_database():
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
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
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
        c.execute('INSERT INTO positions (person_id, org_id, title, start, "end", rank, note) VALUES (?,?,?,?,?,?,?)', pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✓ Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILD
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(pid):
    """Return 'r,g,b' color string based on role."""
    for p in PERSONS:
        if p[0] == pid:
            post = (p[9] or "")
            if "书记" in post and "副书记" not in post:
                return "255,50,50"  # Red for Party Secretary
            if "区长" in post or "副区长" in post:
                return "50,100,255"  # Blue for government
            if "纪委" in post or "监委" in post:
                return "255,165,0"  # Orange for discipline
            return "100,100,100"  # Grey for others
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "政府组成部门": "200,200,255",
        "公安": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "军队": "200,200,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(person_id):
    leaders = {"miyun_yu_weiguo", "miyun_yu_haibo"}
    return person_id in leaders

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>北京市密云区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        post = p[9] or ""
        col = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{col.split(",")[0]}" g="{col.split(",")[1]}" b="{col.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        col = org_color(otype)
        lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{col.split(",")[0]}" g="{col.split(",")[1]}" b="{col.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        pid = pos[0]
        oid = pos[1]
        title = pos[2] or ""
        lines.append(f'      <edge id="{eid}" source="{esc(pid)}" target="{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        a, b, rtype, ctx = r[0], r[1], r[3], r[4]
        lines.append(f'      <edge id="{eid}" source="{esc(a)}" target="{esc(b)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✓ GEXF graph created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    build_database()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print(f"\nGenerated files:")
    print(f"  {DB_PATH}")
    print(f"  {GEXF_PATH}")
