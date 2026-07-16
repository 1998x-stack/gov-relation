#!/usr/bin/env python3
"""
重庆市南岸区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Nan'an District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 重庆市
Parent City: (直辖市辖区)
Targets: 区委书记 & 区长

Research Notes:
- Current 区委书记: 许洪斌 (serving as of July 2026, also 重庆经开区党工委书记兼)
- Current 区长: 刘晟 (appointed around April 2026, previously 代理区长; also 重庆经开区党工委副书记、管委会主任)
- Previous 区长: 喻显镔 (served until at least Aug 2025, succeeded by 刘晟)
- Leadership data compiled from cqna.gov.cn official website (2026-07-16)
- Government leadership roster confirmed from official cqna.gov.cn/zwgk_254/zfxxgkml/ldxx/
- Party committee data from news articles on cqna.gov.cn

Sources:
- https://www.cqna.gov.cn — official government website (primary)
- https://www.cqna.gov.cn/zwgk_254/zfxxgkml/ldxx/ — leadership info pages
- Baidu Baike — 许洪斌, 刘晟 entries
- 中国经济网 — leadership database
- 澎湃新闻 — appointment reports
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "南岸区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "南岸区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 区委班子 (Party Committee) ══
    ("na_xu_hongbin", "许洪斌", "男", "汉族", "1968年10月", "待查",
     "研究生/工学博士", "中共党员", "待查",
     "区委书记、重庆经开区党工委书记（兼）", "中共重庆市南岸区委员会",
     "cqna.gov.cn;media_reports"),

    ("na_liu_sheng", "刘晟", "男", "汉族", "1975年1月", "待查",
     "研究生/管理学硕士", "中共党员", "待查",
     "区委副书记、区政府党组书记、区长、重庆经开区党工委副书记、管委会主任", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    # 区委领导 (from meeting attendance and official listings)
    ("na_li_yong", "李勇", "男", "汉族", "1970年9月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区委常委、区政府党组副书记、常务副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_zhang_jin", "张进", "男", "汉族", "1969年10月", "待查",
     "研究生/理学学士", "中共党员", "待查",
     "区委常委、区政府党组成员、副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    # ══ 区政府领导 (Government leadership from cqna.gov.cn) ══
    ("na_jiang_wenxin", "蒋文新", "男", "汉族", "1967年1月", "待查",
     "大学", "民盟盟员", "待查",
     "区政府副区长、一级巡视员、民盟南岸区委会主委", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_you_yong", "游泳", "男", "汉族", "1970年3月", "待查",
     "大学/高级管理人员工商管理硕士", "中共党员", "待查",
     "区政府党组成员", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_yang_jian", "杨建", "女", "汉族", "1970年3月", "待查",
     "大学/法学学士", "中共党员", "待查",
     "区政府党组成员、副区长、区公安分局党委书记、局长、督察长（兼）", "重庆市公安局南岸区分局",
     "cqna.gov.cn_official"),

    ("na_jiang_nan", "江南", "女", "汉族", "1976年5月", "待查",
     "硕士研究生", "中共党员", "待查",
     "区政府党组成员、副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_chen_jinyu", "陈今玉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_li_min", "李敏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    ("na_zou_han", "邹晗", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长", "重庆市南岸区人民政府",
     "cqna.gov.cn_official"),

    # ══ 前任领导 ══
    ("na_yu_xianbin", "喻显镔", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委副书记、区长（已离任）", "重庆市南岸区人民政府（原）",
     "media_reports;cqna.gov.cn"),

    ("na_tang_xin", "唐昕", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委常委、区政府常务副区长（更早）", "重庆市南岸区人民政府（原）",
     "cqna.gov.cn_archived"),

    # ══ 经开区领导 (重庆经开区管委会) ══
    ("na_wang_jianhua", "王建华", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "重庆经开区领导", "重庆经济技术开发区管理委员会",
     "cqna.gov.cn_news"),

    ("na_xiao_dingguang", "肖鼎光", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "重庆经开区领导", "重庆经济技术开发区管理委员会",
     "cqna.gov.cn_news"),

    ("na_shu_kenke", "舒勤科", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "重庆经开区领导", "重庆经济技术开发区管理委员会",
     "cqna.gov.cn_news"),

    ("na_li_dong", "李东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "重庆经开区领导", "重庆经济技术开发区管理委员会",
     "cqna.gov.cn_news"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("na_party_committee", "中共重庆市南岸区委员会", "党委", "地厅级", "中共重庆市委", "重庆市南岸区"),
    ("na_gov", "重庆市南岸区人民政府", "政府", "地厅级", "重庆市人民政府", "重庆市南岸区"),
    ("na_discipline", "中共重庆市南岸区纪律检查委员会", "纪委", "地厅级", "重庆市纪委监委", "重庆市南岸区"),
    ("na_organization", "中共重庆市南岸区委组织部", "党委部门", "正处级", "南岸区委", "重庆市南岸区"),
    ("na_propaganda", "中共重庆市南岸区委宣传部", "党委部门", "正处级", "南岸区委", "重庆市南岸区"),
    ("na_united_front", "中共重庆市南岸区委统战部", "党委部门", "正处级", "南岸区委", "重庆市南岸区"),
    ("na_political_legal", "中共重庆市南岸区委政法委员会", "党委部门", "正处级", "南岸区委", "重庆市南岸区"),
    ("na_military_department", "重庆市南岸区人民武装部", "军事", "正师级", "重庆警备区", "重庆市南岸区"),
    ("na_public_security", "重庆市公安局南岸区分局", "政府", "正处级", "重庆市公安局", "重庆市南岸区"),
    ("na_gov_office", "重庆市南岸区人民政府办公室", "政府", "正处级", "南岸区政府", "重庆市南岸区"),
    ("na_npc", "重庆市南岸区人民代表大会常务委员会", "人大", "地厅级", "重庆市人大常委会", "重庆市南岸区"),
    ("na_cppcc", "中国人民政治协商会议重庆市南岸区委员会", "政协", "地厅级", "重庆市政协", "重庆市南岸区"),
    ("na_economic_development_zone", "重庆经济技术开发区管理委员会", "开发区", "正厅级", "重庆市人民政府", "重庆市南岸区"),
    ("na_council", "重庆市南岸区监察委员会", "纪委", "地厅级", "重庆市监委", "重庆市南岸区"),
    ("na_court", "重庆市南岸区人民法院", "政法", "正处级", "重庆市高级人民法院", "重庆市南岸区"),
    ("na_prosecutor", "重庆市南岸区人民检察院", "政法", "正处级", "重庆市人民检察院", "重庆市南岸区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 现任核心领导 ──
    ("na_xu_hongbin", "na_party_committee", "区委书记、重庆经开区党工委书记（兼）", "2021年？", "至今", "正厅级", "南岸区委主要负责人"),
    ("na_liu_sheng", "na_gov", "区委副书记、区长、重庆经开区党工委副书记、管委会主任", "2026年4月", "至今", "正厅级", "前为代理区长，后当选区长"),
    ("na_liu_sheng", "na_economic_development_zone", "重庆经开区党工委副书记、管委会主任", "2026年4月", "至今", "正厅级", "兼任"),

    # ── 区委常委兼任政府职务 ──
    ("na_li_yong", "na_gov", "区委常委、常务副区长", "待查", "至今", "副厅级", "区政府常务工作"),
    ("na_zhang_jin", "na_gov", "区委常委、副区长", "待查", "至今", "副厅级", "分管商务、外资外贸等"),

    # ── 区政府副区长 ──
    ("na_jiang_wenxin", "na_gov", "副区长、一级巡视员", "待查", "至今", "副厅级", "分管教育、民政、卫生健康等（非党）"),
    ("na_you_yong", "na_gov", "区政府党组成员", "待查", "至今", "副厅级", "分管工业、交通等"),
    ("na_yang_jian", "na_public_security", "副区长、区公安分局局长", "待查", "至今", "副厅级", "分管公安、司法、信访"),
    ("na_jiang_nan", "na_gov", "副区长", "待查", "至今", "副厅级", "分管规划、住建、城市管理等"),
    ("na_chen_jinyu", "na_gov", "副区长", "待查", "至今", "副厅级", "分管领域待查"),
    ("na_li_min", "na_gov", "副区长", "待查", "至今", "副厅级", "分管领域待查"),
    ("na_zou_han", "na_gov", "副区长", "待查", "至今", "副厅级", "分管领域待查"),

    # ── 前任领导 ──
    ("na_yu_xianbin", "na_gov", "区委副书记、区长", "2023年？", "2025年8月后离任", "正厅级", "前任区长"),
    ("na_tang_xin", "na_gov", "区委常委、常务副区长（更早）", "待查", "待查", "副厅级", "2024年1月常务会议记载"),

    # ── 经开区领导 ──
    ("na_wang_jianhua", "na_economic_development_zone", "重庆经开区领导", "待查", "至今", "副厅级", ""),
    ("na_xiao_dingguang", "na_economic_development_zone", "重庆经开区领导", "待查", "至今", "副厅级", ""),
    ("na_shu_kenke", "na_economic_development_zone", "重庆经开区领导", "待查", "至今", "副厅级", ""),
    ("na_li_dong", "na_economic_development_zone", "重庆经开区领导", "待查", "至今", "副厅级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ── 核心班子关系 ──
    ("na_xu_hongbin", "na_liu_sheng", "overlap", "区委书记与区长搭班子", "南岸区委/区政府", "2026年4月至今"),
    ("na_xu_hongbin", "na_li_yong", "overlap", "区委书记与常务副区长共事", "南岸区委/区政府", "至今"),
    ("na_xu_hongbin", "na_zhang_jin", "overlap", "区委书记与区委常委共事", "南岸区委/区政府", "至今"),
    ("na_liu_sheng", "na_li_yong", "overlap", "区长与常务副区长工作搭档", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_yu_xianbin", "predecessor_successor", "刘晟接替喻显镔任区长", "南岸区政府", "2026年"),

    # ── 政府领导班子内部 ──
    ("na_liu_sheng", "na_jiang_wenxin", "overlap", "区长与副区长", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_you_yong", "overlap", "区长与党组成员", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_yang_jian", "overlap", "区长与副区长、公安局长", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_jiang_nan", "overlap", "区长与副区长", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_chen_jinyu", "overlap", "区长与副区长", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_li_min", "overlap", "区长与副区长", "南岸区政府", "至今"),
    ("na_liu_sheng", "na_zou_han", "overlap", "区长与副区长", "南岸区政府", "至今"),

    # ── 经开区班子 ──
    ("na_liu_sheng", "na_wang_jianhua", "overlap", "经开区管委会主任与管委会领导", "重庆经开区", "至今"),
    ("na_liu_sheng", "na_xiao_dingguang", "overlap", "经开区管委会主任与管委会领导", "重庆经开区", "至今"),
    ("na_liu_sheng", "na_shu_kenke", "overlap", "经开区管委会主任与管委会领导", "重庆经开区", "至今"),
    ("na_liu_sheng", "na_li_dong", "overlap", "经开区管委会主任与管委会领导", "重庆经开区", "至今"),
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def create_database(db_path):
    """Create SQLite database with persons, organizations, positions, relationships."""
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
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
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS positions (
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
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {db_path}")
    print(f"   Persons: {len(PERSONS)}")
    print(f"   Organizations: {len(ORGANIZATIONS)}")
    print(f"   Positions: {len(POSITIONS)}")
    print(f"   Relationships: {len(RELATIONSHIPS)}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def person_color(pid):
    """Return 'r,g,b' string based on role."""
    name_to_role = {p[1]: p[-2] for p in PERSONS}
    name = next((p[1] for p in PERSONS if p[0] == pid), "")
    role_str = name_to_role.get(name, "")
    if "书记" in role_str and "区委" in role_str:
        return "255,50,50"  # Red for party secretary
    if "区长" in role_str or "主任" in role_str:
        if "党工委书记" in role_str:
            return "255,50,50"
        return "50,100,255"  # Blue for mayor/government head
    if "常务" in role_str:
        return "50,100,255"  # Blue for executive deputy
    if "公安" in role_str:
        return "50,100,255"
    if "副区长" in role_str or "党组成员" in role_str:
        return "100,130,200"  # Light blue for deputies
    if "前任" in role_str:
        return "150,150,150"  # Grey for predecessors
    return "100,100,100"  # Grey default


def is_top_leader(pid):
    name = next((p[1] for p in PERSONS if p[0] == pid), "")
    return name in ("许洪斌", "刘晟")


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,165,0",
        "政法": "200,200,255",
        "军事": "220,220,220",
        "党委部门": "255,220,220",
    }
    return colors.get(org_type, "200,200,200")


def create_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    os.makedirs(os.path.dirname(gexf_path) or ".", exist_ok=True)
    lines = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today_str}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>重庆市南岸区领导班子工作关系网络 - 区委书记许洪斌 &amp; 区长刘晟</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # ── Node attributes ──
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="education" type="string"/>')
    lines.append('    </attributes>')

    # ── Edge attributes ──
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # ── Person nodes ──
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, work, post, org, src = p
        rgb = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(edu)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb.split(",")[0]}" g="{rgb.split(",")[1]}" b="{rgb.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('        <viz:position x="0.0" y="0.0" z="0.0"/>')
        lines.append('      </node>')
    # ── Organization nodes ──
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        rgb = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb.split(",")[0]}" g="{rgb.split(",")[1]}" b="{rgb.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')
    # Person → Organization (worked_at)
    seen_pos = set()
    for pos in POSITIONS:
        if (pos[0], pos[1]) in seen_pos:
            continue
        seen_pos.add((pos[0], pos[1]))
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos[0]}" target="o{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5]) if len(pos) > 5 else ""}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos[3])}–{esc(pos[4])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    # Person → Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r[0]}" target="p{r[1]}" label="{esc(r[3])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r[5]) if len(r) > 5 else ""}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    content = "\n".join(lines)
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ GEXF file created: {gexf_path}")
    print(f"   Nodes: {len(PERSONS) + len(ORGANIZATIONS)}")
    print(f"   Edges: {eid}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("重庆市南岸区领导班子工作关系网络")
    print("Level: 市辖区(直辖市) — 正厅级")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    create_database(DB_PATH)
    print()
    create_gexf(GEXF_PATH)
    print()
    print(f"DB size: {os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0} bytes")
    print(f"GEXF size: {os.path.getsize(GEXF_PATH) if os.path.exists(GEXF_PATH) else 0} bytes")
    print("Done.")
