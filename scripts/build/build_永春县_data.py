#!/usr/bin/env python3
"""
永春县（泉州市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yongchun County leadership.

Research date: 2026-07-16
Source: fjyc.gov.cn (official government website), verified primary source.

Key leadership transition (2026年7月):
- 县委书记: 吕建成 → 郭宁 (between 2026-06-29 and 2026-07-10)
- 县长: 张照绿 → 许颖颖 (代县长, appointed 2026-07-07 by 县人大常委会)
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
# Canonical paths (for process_tmp.py token matching)
DB_PATH = os.path.join(PROJECT_DIR, "data/database/永春县_network.db")
GEXF_PATH = os.path.join(PROJECT_DIR, "data/graph/永春县_network.gexf")
# Staging paths
STAGING_DB = os.path.join(BASE_DIR, "永春县_network.db")
STAGING_GEXF = os.path.join(BASE_DIR, "永春县_network.gexf")

# ── DATA ──

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
    
    # ═══ Top Leaders ═══
    ("yongchun_guo_ning", "郭宁", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "县委书记", "中共永春县委员会",
     "https://www.fjyc.gov.cn/zwgk/gzdt/ycyw/202607/t20260711_3308432.htm — 2026年7月10日县委常委会（扩大）会议首次以县委书记身份出席"),
    
    ("yongchun_xu_yingying", "许颖颖", "女", "汉族", "1978年9月", "待查", "研究生学历，文学博士", "中共党员", "待查",
     "县委副书记、代县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/xyy/ — 政府官网领导专页；永政〔2026〕4号 2026年7月7日任副县长"),
    
    ("yongchun_zhang_zhaolu", "张照绿", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "原县长（已离任）", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/gzdt/ycyw/202606/t20260616_3301087.htm — 2026年6月15日仍以县长身份接访"),
    
    ("yongchun_lv_jiancheng", "吕建成", "男", "汉族", "待查", "待查", "待查", "中共党员", "待查",
     "原县委书记（已离任）", "中共永春县委员会",
     "https://www.fjyc.gov.cn/zwgk/gzdt/ycyw/202606/t20260630_3304758.htm — 2026年6月29日仍以县委书记身份慰问"),
    
    # ═══ Government Leadership ═══
    ("yongchun_xiao_haihua", "肖海华", "男", "汉族", "1978年12月", "待查", "在职研究生学历", "中共党员", "待查",
     "县委常委、副县长（常务）", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/xhh/ — 政府官网领导专页"),
    
    ("yongchun_guo_meixi", "郭美西", "女", "汉族", "1966年11月", "待查", "大专学历（中央党校函授经济管理专业）", "无党派人士", "待查",
     "副县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/gmx/ — 政府官网领导专页"),
    
    ("yongchun_qian_yongxin", "钱永新", "男", "汉族", "1970年7月", "待查", "中央党校大学学历", "中共党员", "待查",
     "副县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/qyx/ — 政府官网领导专页"),
    
    ("yongchun_zhuang_karong", "庄凯融", "男", "汉族", "1990年9月", "待查", "研究生学历，管理学博士", "中共党员", "待查",
     "副县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/zkr/ — 政府官网领导专页"),
    
    ("yongchun_zhou_boxiang", "周伯祥", "男", "汉族", "1974年1月", "待查", "中央党校大学学历", "中共党员", "待查",
     "副县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/zbx/ — 政府官网领导专页"),
    
    ("yongchun_qiu_xin", "邱鑫", "男", "汉族", "1975年12月", "待查", "大学本科，教育学学士", "中共党员", "待查",
     "副县长、县公安局局长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/qx/ — 政府官网领导专页"),
    
    ("yongchun_zheng_weize", "郑维泽", "男", "汉族", "1979年3月", "待查", "大学本科，工学学士", "中共党员", "待查",
     "副县长", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/zwz/ — 政府官网领导专页"),
    
    ("yongchun_lin_kang", "林康", "女", "汉族", "1981年9月", "待查", "省委党校研究生学历", "中共党员", "待查",
     "县政府党组成员（正处长级）", "永春县人民政府",
     "https://www.fjyc.gov.cn/zwgk/ldzy/lk/ — 政府官网领导专页"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("org_yongchun_party", "中共永春县委员会", "党委", "县", "中共泉州市委员会", "福建省泉州市永春县"),
    ("org_yongchun_gov", "永春县人民政府", "政府", "县", "泉州市人民政府", "福建省泉州市永春县"),
    ("org_yongchun_gov_office", "永春县人民政府办公室", "政府", "县", "永春县人民政府", "福建省泉州市永春县"),
    ("org_yongchun_psb", "永春县公安局", "政府", "县", "永春县人民政府", "福建省泉州市永春县"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)
    
    # 郭宁
    ("yongchun_guo_ning", "org_yongchun_party", "县委书记", "2026-07", "present", "正处级",
     "2026年7月10日首次以县委书记身份主持县委常委会扩大会议"),
    
    # 许颖颖
    ("yongchun_xu_yingying", "org_yongchun_gov", "代县长", "2026-07", "present", "正处级",
     "2026年7月7日县人大常委会任命为副县长、代县长"),
    ("yongchun_xu_yingying", "org_yongchun_party", "县委副书记", "2026-07", "present", "正处级",
     "政府官网显示为县委副书记"),
    
    # 张照绿（前任县长）
    ("yongchun_zhang_zhaolu", "org_yongchun_gov", "县长", "2020?", "2026-06", "正处级",
     "2026年6月15日仍以县长身份接访，2026年7月7日许颖颖接任"),
    
    # 吕建成（前任县委书记）
    ("yongchun_lv_jiancheng", "org_yongchun_party", "县委书记", "2021?", "2026-06", "正处级",
     "2026年6月29日仍以县委书记身份慰问，2026年7月10日郭宁已接任"),
    
    # 肖海华
    ("yongchun_xiao_haihua", "org_yongchun_gov", "副县长（常务）", "在任", "present", "副处级",
     "县委常委、副县长、党组副书记"),
    ("yongchun_xiao_haihua", "org_yongchun_party", "县委常委", "在任", "present", "副处级", ""),
    
    # 郭美西
    ("yongchun_guo_meixi", "org_yongchun_gov", "副县长", "在任", "present", "副处级", "无党派人士"),
    
    # 钱永新
    ("yongchun_qian_yongxin", "org_yongchun_gov", "副县长", "在任", "present", "副处级", ""),
    
    # 庄凯融
    ("yongchun_zhuang_karong", "org_yongchun_gov", "副县长", "在任", "present", "副处级", "1990年出生，管理学博士"),
    
    # 周伯祥
    ("yongchun_zhou_boxiang", "org_yongchun_gov", "副县长", "在任", "present", "副处级", ""),
    
    # 邱鑫
    ("yongchun_qiu_xin", "org_yongchun_gov", "副县长、县公安局局长", "在任", "present", "副处级", "县公安局党委书记、局长、督察长、三级高级警长"),
    ("yongchun_qiu_xin", "org_yongchun_psb", "局长", "在任", "present", "副处级", ""),
    
    # 郑维泽
    ("yongchun_zheng_weize", "org_yongchun_gov", "副县长", "在任", "present", "副处级", ""),
    
    # 林康
    ("yongchun_lin_kang", "org_yongchun_gov", "县政府党组成员", "在任", "present", "正处级", "正处长级干部"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)
    
    # Top leadership team
    ("yongchun_guo_ning", "yongchun_xu_yingying", "superior_subordinate",
     "县委书记与代县长党政搭档关系", "中共永春县委员会/永春县人民政府", "2026-07至今"),
    
    ("yongchun_xiao_haihua", "yongchun_xu_yingying", "superior_subordinate",
     "常务副县长协助代县长主持县政府日常工作", "永春县人民政府", "2026-07至今"),
    
    ("yongchun_xiao_haihua", "yongchun_guo_ning", "superior_subordinate",
     "县委常委向县委书记汇报", "中共永春县委员会", "2026-07至今"),
    
    # 前任-现任交接
    ("yongchun_lv_jiancheng", "yongchun_guo_ning", "predecessor_successor",
     "吕建成卸任县委书记，郭宁接任（2026年7月）", "中共永春县委员会", "2026-07"),
    
    ("yongchun_zhang_zhaolu", "yongchun_xu_yingying", "predecessor_successor",
     "张照绿卸任县长，许颖颖接任代县长（2026年7月7日）", "永春县人民政府", "2026-07"),
    
    # 前任搭档关系
    ("yongchun_lv_jiancheng", "yongchun_zhang_zhaolu", "overlap",
     "吕建成与张照绿曾长期搭档（党政双首长）", "中共永春县委员会/永春县人民政府", "2020?–2026-06"),
    
    # 县政府班子成员之间的工作关系
    ("yongchun_xiao_haihua", "yongchun_qian_yongxin", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_zhou_boxiang", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_zheng_weize", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_qiu_xin", "overlap",
     "常务副县长与公安局长的业务关系", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_lin_kang", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_guo_meixi", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
    ("yongchun_xiao_haihua", "yongchun_zhuang_karong", "overlap",
     "同为县政府领导班子成员", "永春县人民政府", "在任期间"),
]


# ── SQLite Database ──

def create_db(db_path):
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
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
        CREATE TABLE IF NOT EXISTS relationships (
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
    
    print(f"✅ SQLite database created: {db_path}")


# ── GEXF Graph ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(person_id):
    """Color by role."""
    secretaries = {"yongchun_guo_ning", "yongchun_lv_jiancheng"}
    gov_leaders = {"yongchun_xu_yingying", "yongchun_zhang_zhaolu", "yongchun_xiao_haihua",
                   "yongchun_guo_meixi", "yongchun_qian_yongxin", "yongchun_zhuang_karong",
                   "yongchun_zhou_boxiang", "yongchun_qiu_xin", "yongchun_zheng_weize",
                   "yongchun_lin_kang"}
    if person_id in secretaries:
        return "255,50,50"  # Red — party secretary
    elif person_id in gov_leaders:
        return "50,100,255"  # Blue — government leader
    else:
        return "100,100,100"  # Grey — other

def is_top_leader(person_id):
    return person_id in {"yongchun_guo_ning", "yongchun_xu_yingying",
                          "yongchun_lv_jiancheng", "yongchun_zhang_zhaolu"}

def org_color(org_id):
    colors = {
        "org_yongchun_party": "255,200,200",    # Pink — 党委
        "org_yongchun_gov": "200,200,255",       # Light blue — 政府
        "org_yongchun_gov_office": "200,200,255",
        "org_yongchun_psb": "200,200,255",
    }
    return colors.get(org_id, "200,200,200")

def create_gexf(gexf_path):
    os.makedirs(os.path.dirname(gexf_path) if os.path.dirname(gexf_path) else ".", exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Research Agent</creator>')
    lines.append('    <description>永春县（泉州市）领导班子工作关系网络</description>')
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
    
    # --- Nodes ---
    lines.append('    <nodes>')
    
    # Person nodes
    for p in PERSONS:
        pid, name = p[0], p[1]
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        role = f"{p[9]} — {p[10]}"  # current_post — current_org
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # Organization nodes
    for o in ORGANIZATIONS:
        oid, oname = o[0], o[1]
        c = org_color(oid)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    
    lines.append('    </nodes>')
    
    # --- Edges ---
    lines.append('    <edges>')
    eid = 0
    
    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid, oid, title = pos[0], pos[1], pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa, pb, rtype, ctx = r[0], r[1], r[2], r[3]
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ GEXF graph created: {gexf_path}")


# ── Summary ──

def print_summary():
    print(f"\n📊 Summary:")
    print(f"  Persons: {len(PERSONS)}")
    print(f"  Organizations: {len(ORGANIZATIONS)}")
    print(f"  Positions: {len(POSITIONS)}")
    print(f"  Relationships: {len(RELATIONSHIPS)}")
    print(f"\n⚠️  Notes:")
    print(f"  - Most persons lack full career histories (birthplace, education details, earlier positions)")
    print(f"  - 郭宁 and 许颖颖 are newly appointed (July 2026) — previous career histories need further research")
    print(f"  - 肖海华 (县委常委/常务副县长) and 钱永新 are also Party members known from gov bio")
    print(f"  - The full 县委常委会 (county party standing committee) composition is unknown — only 郭宁, 许颖颖, 肖海华 confirmed as members")
    print(f"  - This is a staging build. After validation, use scripts/process_tmp.py to promote.")


if __name__ == "__main__":
    print("🔨 永春县领导班子数据构建脚本")
    print("=" * 50)
    create_db(STAGING_DB)
    create_gexf(STAGING_GEXF)
    print_summary()
