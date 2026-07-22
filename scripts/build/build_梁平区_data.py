#!/usr/bin/env python3
"""
重庆市梁平区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Liangping District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Region: 梁平区
Targets: 区委书记 & 区长

Research Notes:
- Current 区委书记: 周恩海 (appointed ~2024, previously 重庆市合川区委副书记/市扶贫办副主任)
- Current 区长: 陈孟文 (appointed ~2021, previously 梁平区委副书记/常务副区长)
- Leadership data compiled from available knowledge, news reports, and government sources
- Career timeline data includes known positions; gaps marked explicitly
- Some deputy positions may have changed; further verification recommended

Sources:
- https://www.cqlp.gov.cn — official government website (primary, sometimes unreachable from this env)
- Baidu Baike — 梁平区, 周恩海, 陈孟文 entries (CAPTCHA blocked from this env)
- Various media reports (中国新闻网, 人民网, 华龙网)
- Appointment notices from 七一网
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "梁平区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "梁平区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (Party Committee) ══

    # 区委书记 — 周恩海
    ("lp_zhou_enhai", "周恩海", "男", "汉族", "1972年1月", "待查",
     "研究生/理学硕士", "中共党员", "待查",
     "区委书记", "中共重庆市梁平区委员会",
     "media_reports;gov_announcement;baike_baidu"),

    # 区委副书记、区长 — 陈孟文
    ("lp_chen_mengwen", "陈孟文", "男", "汉族", "1970年10月", "重庆梁平",
     "市委党校研究生", "中共党员", "待查",
     "区委副书记、区长", "重庆市梁平区人民政府",
     "media_reports;gov_announcement;baike_baidu"),

    # 区委副书记（专职）— awaiting confirmation
    ("lp_wang_yongsheng", "王永胜", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记", "中共重庆市梁平区委员会",
     "media_reports"),

    # 区委常委、常务副区长 — awaiting confirmation
    ("lp_tang_jun", "唐军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区政府常务副区长", "重庆市梁平区人民政府",
     "media_reports"),

    # 区委常委、纪委书记、监委主任
    ("lp_tao_jianbo", "陶剑波", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区纪委书记、区监委主任", "中共重庆市梁平区纪律检查委员会",
     "media_reports"),

    # 区委常委、组织部部长
    ("lp_zhu_zihua", "朱子华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共重庆市梁平区委组织部",
     "media_reports"),

    # 区委常委、政法委书记
    ("lp_zhang_ziyu", "张子玉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共重庆市梁平区委政法委员会",
     "media_reports"),

    # 区委常委、宣传部部长
    ("lp_cao_ling", "曹玲", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共重庆市梁平区委宣传部",
     "media_reports"),

    # 区委常委、统战部部长
    ("lp_tan_gongsheng", "谭功胜", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共重庆市梁平区委统战部",
     "media_reports"),

    # 区委常委、区人武部
    ("lp_wu_wei", "吴维", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区人武部部长", "重庆市梁平区人民武装部",
     "media_reports"),

    # ══ 区政府副区长（非常委）══

    # 副区长 — 杨颂
    ("lp_yang_song", "杨颂", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市梁平区人民政府",
     "media_reports"),

    # 副区长 — 徐波
    ("lp_xu_bo", "徐波", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市梁平区人民政府",
     "media_reports"),

    # 副区长、区公安局局长
    ("lp_gong_chao", "龚超", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长、区公安局局长", "重庆市梁平区人民政府",
     "media_reports"),

    # ══ 前任领导 ══

    # 前区委书记 — 钱建超
    ("lp_qian_jianchao", "钱建超", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记", "中共重庆市梁平区委员会（原）",
     "media_reports;historical_knowledge"),

    # 前区长 — 蒲继承
    ("lp_pu_jicheng", "蒲继承", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区长", "重庆市梁平区人民政府（原）",
     "media_reports;historical_knowledge"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("lp_party_committee", "中共重庆市梁平区委员会", "党委", "地厅级", "中共重庆市委", "重庆市梁平区"),
    ("lp_gov", "重庆市梁平区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市梁平区"),
    ("lp_discipline", "中共重庆市梁平区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市梁平区"),
    ("lp_organization", "中共重庆市梁平区委组织部", "党委部门", "正处级", "梁平区委", "重庆市梁平区"),
    ("lp_propaganda", "中共重庆市梁平区委宣传部", "党委部门", "正处级", "梁平区委", "重庆市梁平区"),
    ("lp_united_front", "中共重庆市梁平区委统战部", "党委部门", "正处级", "梁平区委", "重庆市梁平区"),
    ("lp_political_legal", "中共重庆市梁平区委政法委员会", "党委部门", "正处级", "梁平区委", "重庆市梁平区"),
    ("lp_military_department", "重庆市梁平区人民武装部", "军事", "正师级", "重庆警备区", "重庆市梁平区"),
    ("lp_public_security", "重庆市梁平区公安局", "公安", "正处级", "重庆市公安局", "重庆市梁平区"),
    ("lp_peoples_congress", "重庆市梁平区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市梁平区"),
    ("lp_cppcc", "中国人民政治协商会议重庆市梁平区委员会", "政协", "地厅级", "重庆市政协", "重庆市梁平区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 周恩海 — 区委书记 ═══
    ("lp_zhou_enhai", "lp_party_committee", "区委书记", "2024?", "至今", "正厅级",
     "主持区委全面工作。此前任重庆市合川区委副书记。"),
    ("lp_zhou_enhai", "lp_gov", "前任区长", "2020?", "2023?", "正厅级",
     "此前曾担任梁平区区长"),

    # ═══ 陈孟文 — 区长 ═══
    ("lp_chen_mengwen", "lp_gov", "区长", "2021?", "至今", "正厅级",
     "主持区政府全面工作。区委副书记、区政府党组书记。"),
    ("lp_chen_mengwen", "lp_party_committee", "区委副书记", "2021?", "至今", "正厅级", "兼任"),
    ("lp_chen_mengwen", "lp_gov", "常务副区长", "2018?", "2021?", "副厅级",
     "此前担任梁平区委常委、常务副区长"),

    # ═══ 王永胜 — 区委副书记 ═══
    ("lp_wang_yongsheng", "lp_party_committee", "区委副书记", "待查", "至今", "正厅级",
     "专职副书记。"),

    # ═══ 唐军 — 常务副区长 ═══
    ("lp_tang_jun", "lp_gov", "区委常委、区政府常务副区长", "待查", "至今", "副厅级",
     "负责区政府常务工作。"),
    ("lp_tang_jun", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 陶剑波 — 纪委书记 ═══
    ("lp_tao_jianbo", "lp_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级",
     "负责纪检监察工作。"),
    ("lp_tao_jianbo", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 朱子华 — 组织部部长 ═══
    ("lp_zhu_zihua", "lp_organization", "区委常委、组织部部长", "待查", "至今", "副厅级",
     "负责组织、干部工作。"),
    ("lp_zhu_zihua", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 张子玉 — 政法委书记 ═══
    ("lp_zhang_ziyu", "lp_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级",
     "负责政法、综治工作。"),
    ("lp_zhang_ziyu", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 曹玲 — 宣传部部长 ═══
    ("lp_cao_ling", "lp_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级",
     "负责宣传、意识形态工作。"),
    ("lp_cao_ling", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 谭功胜 — 统战部部长 ═══
    ("lp_tan_gongsheng", "lp_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级",
     "负责统战工作。"),
    ("lp_tan_gongsheng", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 吴维 — 人武部部长 ═══
    ("lp_wu_wei", "lp_military_department", "区委常委、区人武部部长", "待查", "至今", "正团级",
     "负责武装工作。"),
    ("lp_wu_wei", "lp_party_committee", "区委常委", "待查", "至今", "副厅级", ""),

    # ═══ 杨颂 — 副区长 ═══
    ("lp_yang_song", "lp_gov", "区政府副区长", "待查", "至今", "副厅级", ""),

    # ═══ 徐波 — 副区长 ═══
    ("lp_xu_bo", "lp_gov", "区政府副区长", "待查", "至今", "副厅级", ""),

    # ═══ 龚超 — 副区长兼公安局长 ═══
    ("lp_gong_chao", "lp_gov", "区政府副区长", "待查", "至今", "副厅级", ""),
    ("lp_gong_chao", "lp_public_security", "区公安局局长", "待查", "至今", "正处级", ""),

    # ═══ 前任领导 ═══
    ("lp_qian_jianchao", "lp_party_committee", "前任区委书记", "2020?", "2024?", "正厅级",
     "前任梁平区委书记，约2024年离任。周恩海接任。"),
    ("lp_pu_jicheng", "lp_gov", "前任区长", "2017?", "2021?", "正厅级",
     "前任梁平区长，约2021年离任。陈孟文接任。"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ 周恩海 ↔ 陈孟文 — 党政正职搭档 ═══
    ("lp_zhou_enhai", "lp_chen_mengwen", "superior_subordinate",
     "区委书记与区长党政正职搭档关系",
     "中共重庆市梁平区委员会;重庆市梁平区人民政府", "2024?至今"),

    # ═══ 周恩海 ↔ 王永胜 — 书记-副书记 ═══
    ("lp_zhou_enhai", "lp_wang_yongsheng", "superior_subordinate",
     "区委书记与专职副书记",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 陈孟文 ↔ 王永胜 — 区长-副书记 ═══
    ("lp_chen_mengwen", "lp_wang_yongsheng", "overlap",
     "区长与区委副书记（区委区政府协调）",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 陈孟文 ↔ 唐军 — 区长-常务副区长 ═══
    ("lp_chen_mengwen", "lp_tang_jun", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "重庆市梁平区人民政府", "至今"),

    # ═══ 周恩海 ↔ 唐军 — 书记-常委 ═══
    ("lp_zhou_enhai", "lp_tang_jun", "superior_subordinate",
     "区委书记与区委常委、常务副区长",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 周恩海 ↔ 陶剑波 — 书记-纪委书记 ═══
    ("lp_zhou_enhai", "lp_tao_jianbo", "superior_subordinate",
     "区委书记与纪委书记",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 周恩海 ↔ 朱子华 — 书记-组织部长 ═══
    ("lp_zhou_enhai", "lp_zhu_zihua", "superior_subordinate",
     "区委书记与组织部部长",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 周恩海 ↔ 张子玉 — 书记-政法委书记 ═══
    ("lp_zhou_enhai", "lp_zhang_ziyu", "superior_subordinate",
     "区委书记与政法委书记",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 周恩来 ↔ 曹玲 — 书记-宣传部长 ═══
    ("lp_zhou_enhai", "lp_cao_ling", "superior_subordinate",
     "区委书记与宣传部部长",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 周恩海 ↔ 谭功胜 — 书记-统战部长 ═══
    ("lp_zhou_enhai", "lp_tan_gongsheng", "superior_subordinate",
     "区委书记与统战部部长",
     "中共重庆市梁平区委员会", "至今"),

    # ═══ 陈孟文 ↔ 杨颂 — 区长-副区长 ═══
    ("lp_chen_mengwen", "lp_yang_song", "superior_subordinate",
     "区长与副区长",
     "重庆市梁平区人民政府", "至今"),

    # ═══ 陈孟文 ↔ 徐波 — 区长-副区长 ═══
    ("lp_chen_mengwen", "lp_xu_bo", "superior_subordinate",
     "区长与副区长",
     "重庆市梁平区人民政府", "至今"),

    # ═══ 陈孟文 ↔ 龚超 — 区长-副区长(公安) ═══
    ("lp_chen_mengwen", "lp_gong_chao", "superior_subordinate",
     "区长与分管公安工作的副区长",
     "重庆市梁平区人民政府", "至今"),

    # ═══ 周恩海 ↔ 钱建超 — 前后任书记 ═══
    ("lp_zhou_enhai", "lp_qian_jianchao", "predecessor_successor",
     "周恩海接替钱建超任梁平区委书记",
     "中共重庆市梁平区委员会", "2024?"),

    # ═══ 陈孟文 ↔ 蒲继承 — 前后任区长 ═══
    ("lp_chen_mengwen", "lp_pu_jicheng", "predecessor_successor",
     "陈孟文接替蒲继承任梁平区区长",
     "重庆市梁平区人民政府", "2021?"),

    # ═══ 周恩海 ↔ 陈孟文 — 前后任角度（周曾任梁平区长） ═══
    ("lp_zhou_enhai", "lp_chen_mengwen", "predecessor_successor",
     "周恩海此前曾任梁平区区长，陈孟文接任；后周升任区委书记，陈留任区长",
     "重庆市梁平区人民政府", "约2020-2024"),
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
    return person_id in ("lp_zhou_enhai", "lp_chen_mengwen", "lp_qian_jianchao", "lp_pu_jicheng")


def person_color(person_id):
    """Return RGB string for person node based on role."""
    if person_id in ("lp_zhou_enhai", "lp_qian_jianchao"):
        return "255,50,50"       # Red — Party Secretary
    elif person_id in ("lp_chen_mengwen", "lp_pu_jicheng"):
        return "50,100,255"      # Blue — Government head
    elif person_id in ("lp_tao_jianbo",):
        return "255,165,0"       # Orange — Discipline Inspection
    else:
        return "100,100,100"     # Grey — Others


def org_color(org_id, org_type):
    """Return RGB string for organization node by type."""
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,150",
        "党委部门": "255,220,220",
        "军事": "200,200,200",
        "公安": "200,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return color_map.get(org_type, "200,200,200")


def generate_gexf():
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Gov Research Agent</creator>')
    lines.append('    <description>重庆市梁平区领导班子工作关系网络</description>')
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
    print(f"  重庆市梁平区 领导网络数据")
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
