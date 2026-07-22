#!/usr/bin/env python3
"""
北京市怀柔区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Huairou District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjhr.gov.cn (official leadership pages)
- Baidu Baike, government appointment notices, media reports
- As of: July 2026

Current leadership (as of 2026-07):
  区委书记: 张强 (since 2025-06-28)
  区委副书记、区长: 梁爽 (since 2024-07)
  区委副书记、政法委书记: 莫剑彬 (since 2025-05)
  区委常委、常务副区长: 王建刚
  区委常委、组织部部长: 刘敏华 (since 2025)
  区委常委、纪委书记/监委主任: 王志宇
  区委常委、副区长: 高志庆
  副区长: 孙乐 (female), 于家明, 季学伟, 夏文佳
  区人大常委会主任: 彭丽霞 (female)
  区政协主席: 刘久刚

Predecessors:
  前任区委书记: 郭延红 (2019-12 ~ 2025-06)
  前任区长: 于庆丰 (2020-01 ~ 2024-06, 调任市体育局局长)

Relationships:
- 张强曾任北京市委组织部副部长(2017-2020) → 长期在组织系统工作
- 梁爽曾任海淀区委常委、副区长(2020-2021) → 跨区调动
- 莫剑彬曾任怀柔区委常委、政法委书记(2022-2025) → 升任区委副书记
- 于庆丰→梁爽：区长前后任交接(2024)
- 郭延红→张强：书记前后任交接(2025)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "怀柔区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "怀柔区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── 区委班子 ──
    ("hr_zhang_qiang", "张强", "男", "汉族", "1973年9月", "辽宁台安",
     "北京大学哲学系/公共管理硕士", "1993年4月", "1997年7月",
     "区委书记、怀柔科学城党工委书记", "中共北京市怀柔区委员会",
     "bjhr.gov.cn;capital.beijing.gov.cn;baidu.baike"),
    ("hr_liang_shuang", "梁爽", "男", "汉族", "1980年2月", "黑龙江庆安",
     "大学(中国政法大学)/法学学士", "1999年5月", "2003年7月",
     "区委副书记、区长、怀柔科学城管委会主任", "北京市怀柔区人民政府",
     "bjhr.gov.cn;baidu.baike;media"),
    ("hr_mo_jianbin", "莫剑彬", "男", "汉族", "1971年8月", "待查",
     "中央党校研究生/教育学学士(北京师范大学)", "中共党员", "待查",
     "区委副书记、政法委书记", "中共北京市怀柔区委员会",
     "bjhr.gov.cn;baidu.baike;media"),
    ("hr_wang_jiangang", "王建刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),
    ("hr_liu_minhua", "刘敏华", "男", "汉族", "1976年6月", "待查",
     "研究生/工学博士", "中共党员", "待查",
     "区委常委、组织部部长(兼怀柔科学城党工委委员)", "中共北京市怀柔区委组织部",
     "bjhr.gov.cn;media"),
    ("hr_wang_zhiyu", "王志宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共北京市怀柔区纪律检查委员会",
     "bjhr.gov.cn;media"),
    ("hr_gao_zhiqing", "高志庆", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),

    # ── 副区长（非常委身份） ──
    ("hr_sun_le", "孙乐", "女", "回族", "1985年2月", "待查",
     "法律硕士", "中共党员", "待查",
     "副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),
    ("hr_yu_jiaming", "于家明", "男", "汉族", "1983年10月", "待查",
     "研究生/管理学硕士", "中共党员", "待查",
     "副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),
    ("hr_ji_xuewei", "季学伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),
    ("hr_xia_wenjia", "夏文佳", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市怀柔区人民政府",
     "bjhr.gov.cn;media"),

    # ── 人大、政协主要领导 ──
    ("hr_peng_lixia", "彭丽霞", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市怀柔区人民代表大会常务委员会",
     "bjhr.gov.cn;media"),
    ("hr_liu_jiugang", "刘久刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市怀柔区委员会",
     "bjhr.gov.cn;media"),

    # ── 前任领导 ──
    ("hr_guo_yanhong", "郭延红", "女", "汉族", "1967年1月", "山东淄博",
     "大学/工程硕士", "1994年12月", "1989年8月",
     "原区委书记(已离任)", "中共北京市怀柔区委员会(原)",
     "baidu.baike;capital.­beijing.gov.cn"),
    ("hr_yu_qingfeng", "于庆丰", "男", "汉族", "1970年6月", "待查",
     "中央党校研究生", "中共党员", "1992年7月",
     "原区长(现任市体育局局长)", "北京市怀柔区人民政府(原)",
     "baidu.baike;media"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("org_hr_qw", "中共北京市怀柔区委员会", "党委", "正厅级", "北京市委", "北京市怀柔区"),
    ("org_hr_zf", "北京市怀柔区人民政府", "政府", "正厅级", "北京市政府", "北京市怀柔区"),
    ("org_hr_jw", "中共北京市怀柔区纪律检查委员会", "党委", "副厅级", "北京市纪委监委", "北京市怀柔区"),
    ("org_hr_zzb", "中共北京市怀柔区委组织部", "党委", "正处级", "怀柔区委", "北京市怀柔区"),
    ("org_hr_zfw", "中共北京市怀柔区委政法委员会", "党委", "正处级", "怀柔区委", "北京市怀柔区"),
    ("org_hr_rd", "北京市怀柔区人民代表大会常务委员会", "人大", "正厅级", "北京市人大", "北京市怀柔区"),
    ("org_hr_zx", "中国人民政治协商会议北京市怀柔区委员会", "政协", "正厅级", "北京市政协", "北京市怀柔区"),
    ("org_hr_kxcs", "怀柔科学城管理委员会", "开发区", "正厅级", "北京市委市政府", "北京市怀柔区"),
    ("org_hr_tyj", "北京市体育局", "政府", "正厅级", "北京市政府", "北京市通州区(城市副中心)"),
]

POSITIONS = [
    # ── 区委班子(现任) ──
    ("hr_zhang_qiang", "org_hr_qw", "区委书记", "2025-06", "present", "正厅级", "接替郭延红"),
    ("hr_zhang_qiang", "org_hr_kxcs", "怀柔科学城党工委书记", "2025-06", "present", "正厅级", "兼任"),
    ("hr_liang_shuang", "org_hr_zf", "区长", "2024-07", "present", "正厅级", "由代区长转正"),
    ("hr_liang_shuang", "org_hr_kxcs", "怀柔科学城管委会主任", "2024-07", "present", "正厅级", "兼任"),
    ("hr_liang_shuang", "org_hr_qw", "区委副书记", "2023-03", "present", "正厅级", ""),
    ("hr_mo_jianbin", "org_hr_qw", "区委副书记", "2025-05", "present", "副厅级", "由区委常委升任"),
    ("hr_mo_jianbin", "org_hr_zfw", "区委政法委书记", "2025-05", "present", "正处级", "兼任"),
    ("hr_wang_jiangang", "org_hr_zf", "常务副区长", "待查", "present", "副厅级", "区委常委"),
    ("hr_liu_minhua", "org_hr_zzb", "组织部部长", "2025", "present", "正处级", "区委常委"),
    ("hr_liu_minhua", "org_hr_kxcs", "怀柔科学城党工委委员", "2025", "present", "", "兼任"),
    ("hr_wang_zhiyu", "org_hr_jw", "纪委书记、监委主任", "待查", "present", "副厅级", "区委常委"),
    ("hr_gao_zhiqing", "org_hr_zf", "副区长", "待查", "present", "副厅级", "区委常委"),
    ("hr_sun_le", "org_hr_zf", "副区长", "待查", "present", "副厅级", ""),
    ("hr_yu_jiaming", "org_hr_zf", "副区长", "待查", "present", "副厅级", "拟任区委常委(2025-04公示)"),
    ("hr_ji_xuewei", "org_hr_zf", "副区长", "待查", "present", "副厅级", ""),
    ("hr_xia_wenjia", "org_hr_zf", "副区长", "待查", "present", "副厅级", ""),
    ("hr_peng_lixia", "org_hr_rd", "区人大常委会主任", "待查", "present", "正厅级", ""),
    ("hr_liu_jiugang", "org_hr_zx", "区政协主席", "待查", "present", "正厅级", ""),

    # ── 前任领导 ──
    ("hr_guo_yanhong", "org_hr_qw", "区委书记", "2019-12", "2025-06", "正厅级", "接替戴彬彬"),
    ("hr_guo_yanhong", "org_hr_kxcs", "怀柔科学城党工委书记", "2019-12", "2025-06", "正厅级", "兼任"),
    ("hr_yu_qingfeng", "org_hr_zf", "区长", "2020-01", "2024-06", "正厅级", "由代区长转正"),
    ("hr_yu_qingfeng", "org_hr_kxcs", "怀柔科学城管委会主任", "2020-01", "2024-06", "正厅级", "兼任"),
    ("hr_yu_qingfeng", "org_hr_tyj", "市体育局局长", "2024-06", "present", "正厅级", "调任"),

    # ── 梁爽此前在怀柔的任职（升任区长前） ──
    ("hr_liang_shuang", "org_hr_zf", "副区长", "2021-12", "2023-03", "副厅级", "由海淀区调任"),
    ("hr_liang_shuang", "org_hr_kxcs", "怀柔科学城管委会副主任", "2021-12", "2024-07", "副厅级", "兼任"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period, confidence)
    # 前后任关系
    ("hr_guo_yanhong", "hr_zhang_qiang", "predecessor_successor",
     "郭延红2025年6月不再担任区委书记，张强接任",
     "中共北京市怀柔区委员会", "2025-06", "confirmed"),
    ("hr_yu_qingfeng", "hr_liang_shuang", "predecessor_successor",
     "于庆丰2024年6月调任市体育局，梁爽接任区长",
     "北京市怀柔区人民政府", "2024-06/07", "confirmed"),

    # 现任班子内部的上下级/共事关系
    ("hr_zhang_qiang", "hr_liang_shuang", "superior_subordinate",
     "张强任区委书记，梁爽任区委副书记、区长",
     "中共北京市怀柔区委员会", "2025-06~present", "confirmed"),
    ("hr_zhang_qiang", "hr_mo_jianbin", "superior_subordinate",
     "张强任区委书记，莫剑彬任区委副书记",
     "中共北京市怀柔区委员会", "2025-05~present", "confirmed"),
    ("hr_liang_shuang", "hr_mo_jianbin", "overlap",
     "梁爽任区委副书记、区长，莫剑彬任区委副书记、政法委书记",
     "中共北京市怀柔区委员会", "2025-05~present", "confirmed"),

    # 梁爽在海淀区的前任经历关联（跨区调动）
    ("hr_liang_shuang", "hr_yu_qingfeng", "predecessor_successor",
     "梁爽接替于庆丰为怀柔区长", "北京市怀柔区人民政府", "2024-06/07", "confirmed"),

    # 莫剑彬升任路径
    ("hr_mo_jianbin", "hr_wang_zhiyu", "overlap",
     "莫剑彬任区委政法委书记(兼)，王志宇任区纪委书记，均属区委常委",
     "中共北京市怀柔区委员会", "2025~present", "plausible"),

    # 组织部部长与书记的关系
    ("hr_zhang_qiang", "hr_liu_minhua", "superior_subordinate",
     "张强作为区委书记领导组织部工作，刘敏华任组织部长",
     "中共北京市怀柔区委员会", "2025~present", "confirmed"),

    # 前任区委书记与前任区长的共事
    ("hr_guo_yanhong", "hr_yu_qingfeng", "overlap",
     "郭延红任区委书记期间，于庆丰任区长",
     "中共北京市怀柔区委员会/怀柔区人民政府", "2020-01~2024-06", "confirmed"),

    # 张强此前长期在市委组织部——管理干部路径
    # （注：这一类属于 career background，不是 local overlap）
]

# ════════════════════════════════════════════
# BUILD SQLite DATABASE
# ════════════════════════════════════════════

def build_database():
    """Create and populate the SQLite database."""
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
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    c.executemany(
        "INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        PERSONS
    )
    c.executemany(
        "INSERT INTO organizations VALUES (?,?,?,?,?,?)",
        ORGANIZATIONS
    )
    c.executemany(
        "INSERT INTO positions(person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
        POSITIONS
    )
    c.executemany(
        "INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
        RELATIONSHIPS
    )

    conn.commit()
    conn.close()
    print(f"  Database created: {DB_PATH}")

# ════════════════════════════════════════════
# BUILD GEXF GRAPH
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Return 'r,g,b' color string for a person node based on role."""
    role_map = {
        "hr_zhang_qiang":   "255,50,50",    # party secretary - red
        "hr_liang_shuang":  "50,100,255",   # mayor - blue
        "hr_guo_yanhong":   "255,50,50",    # former secretary - red
        "hr_yu_qingfeng":   "50,100,255",   # former mayor - blue
        "hr_mo_jianbin":    "255,165,0",    # discipline-ish / deputy - orange
    }
    return role_map.get(person_id, "100,100,100")

def is_top_leader(person_id):
    return person_id in ("hr_zhang_qiang", "hr_liang_shuang", "hr_guo_yanhong", "hr_yu_qingfeng")

def org_color(org_type):
    color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }
    return color_map.get(org_type, "200,200,200")

def build_gexf():
    """Generate GEXF XML using string formatting (not ElementTree) to avoid namespace issues."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>北京市怀柔区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('      <attribute id="4" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="label" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    # Person nodes
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, ws, post, org, src = p
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        label_display = f"{name}\\n{post}"
        lines.append(f'      <node id="{pid}" label="{esc(label_display)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="4" value="person"/>')
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
        lines.append(f'          <attvalue for="1" value="{esc(name)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(otype)}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    # Person→Organization (worked_at) edges
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person↔Person (relationship) edges
    for rel in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period, confidence = rel
        lines.append(f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF graph created: {GEXF_PATH}")

# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

def main():
    print("Building 怀柔区 leadership network data...")
    build_database()
    build_gexf()
    print("Done.")

if __name__ == "__main__":
    main()
