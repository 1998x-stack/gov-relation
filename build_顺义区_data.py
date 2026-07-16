#!/usr/bin/env python3
"""
北京市顺义区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Shunyi District (顺义区) leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjshy.gov.cn/web/zwgk/ldjs3/index.html (official leadership page, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "顺义区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "顺义区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person ID convention: shunyi_{surname_givenname}
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（9人） ──
    ("shunyi_gong_zongyuan", "龚宗元", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委书记", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_cui_xiaohao", "崔小浩", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_wu_xiaojun", "吴晓军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_song_peng", "宋鹏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_ma_hongping", "马红萍", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_li_xin", "李欣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_geng_xiaojing", "耿晓婧", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_zhang_yitao", "张仪涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_liu_yongjun", "刘永军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委", "中共北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    # ── 区政府领导（除常委外） ──
    ("shunyi_dong_chenggang", "东成刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_huang_yongzhi", "黄永志", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_hou_ying", "侯颖", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_zhou_xin", "周鑫", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_wang_ke", "王科", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_li_baojie", "李保杰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长（挂职）", "北京市顺义区人民政府",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    # ── 区人大常委会 ──
    ("shunyi_bao_jian", "暴剑", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_zhang_aidong", "张爱冬", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_wang_jianyuan", "王鉴远", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_hu_xiaobing", "胡小兵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_hao_weiquan", "郝蔚泉", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_chen_xiaoyan", "陈小燕", "女", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区人大常委会副主任（不驻会）", "北京市顺义区人民代表大会常务委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    # ── 区政协 ──
    ("shunyi_zhou_xinchun", "周新春", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_li_yan", "李衍", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_shi_weidong", "史卫东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协副主席", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_yang_fenghui", "杨凤辉", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_yu_baoxin", "于宝鑫", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),

    ("shunyi_guo_yuhao", "郭玉颢", "男", "汉族", "待查", "待查",
     "待查", "待查", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市顺义区委员会",
     "bjshy.gov.cn/web/zwgk/ldjs3/index.html"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("org_shunyi_party", "中共北京市顺义区委员会", "党委", "正厅级", "中共北京市委", "北京市顺义区"),
    ("org_shunyi_gov", "北京市顺义区人民政府", "政府", "正厅级", "北京市人民政府", "北京市顺义区"),
    ("org_shunyi_discipline", "中共北京市顺义区纪律检查委员会", "党委", "正厅级", "中共北京市纪委", "北京市顺义区"),
    ("org_shunyi_organization", "中共北京市顺义区委组织部", "党委", "正处级", "中共北京市顺义区委员会", "北京市顺义区"),
    ("org_shunyi_propaganda", "中共北京市顺义区委宣传部", "党委", "正处级", "中共北京市顺义区委员会", "北京市顺义区"),
    ("org_shunyi_united_front", "中共北京市顺义区委统战部", "党委", "正处级", "中共北京市顺义区委员会", "北京市顺义区"),
    ("org_shunyi_politics_law", "中共北京市顺义区委政法委员会", "党委", "正处级", "中共北京市顺义区委员会", "北京市顺义区"),
    ("org_shunyi_people_congress", "北京市顺义区人民代表大会常务委员会", "人大", "正厅级", "北京市人大常委会", "北京市顺义区"),
    ("org_shunyi_cppcc", "中国人民政治协商会议北京市顺义区委员会", "政协", "正厅级", "北京市政协", "北京市顺义区"),
    ("org_shunyi_public_security", "北京市公安局顺义分局", "政府", "正处级", "北京市公安局", "北京市顺义区"),
    ("org_shunyi_armed_forces", "北京市顺义区人民武装部", "政府", "正处级", "北京卫戍区", "北京市顺义区"),
]

# Position assignments
POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 区委 ──
    ("shunyi_gong_zongyuan", "org_shunyi_party", "区委书记", "待查", "present", "正厅级", ""),
    ("shunyi_cui_xiaohao", "org_shunyi_gov", "区长", "待查", "present", "正厅级", ""),
    ("shunyi_cui_xiaohao", "org_shunyi_party", "区委副书记", "待查", "present", "正厅级", ""),
    ("shunyi_wu_xiaojun", "org_shunyi_party", "区委副书记", "待查", "present", "副厅级", ""),
    ("shunyi_song_peng", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),
    ("shunyi_ma_hongping", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),
    ("shunyi_li_xin", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),
    ("shunyi_li_xin", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_geng_xiaojing", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),
    ("shunyi_zhang_yitao", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),
    ("shunyi_liu_yongjun", "org_shunyi_party", "区委常委", "待查", "present", "副厅级", ""),

    # ── 区政府 ──
    ("shunyi_dong_chenggang", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_huang_yongzhi", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_hou_ying", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_zhou_xin", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_wang_ke", "org_shunyi_gov", "副区长", "待查", "present", "副厅级", ""),
    ("shunyi_li_baojie", "org_shunyi_gov", "副区长（挂职）", "待查", "present", "副厅级", "挂职"),

    # ── 人大 ──
    ("shunyi_bao_jian", "org_shunyi_people_congress", "主任", "待查", "present", "正厅级", ""),
    ("shunyi_zhang_aidong", "org_shunyi_people_congress", "副主任", "待查", "present", "副厅级", ""),
    ("shunyi_wang_jianyuan", "org_shunyi_people_congress", "副主任", "待查", "present", "副厅级", ""),
    ("shunyi_hu_xiaobing", "org_shunyi_people_congress", "副主任", "待查", "present", "副厅级", ""),
    ("shunyi_hao_weiquan", "org_shunyi_people_congress", "副主任", "待查", "present", "副厅级", ""),
    ("shunyi_chen_xiaoyan", "org_shunyi_people_congress", "副主任（不驻会）", "待查", "present", "副厅级", "不驻会"),

    # ── 政协 ──
    ("shunyi_zhou_xinchun", "org_shunyi_cppcc", "主席", "待查", "present", "正厅级", ""),
    ("shunyi_li_yan", "org_shunyi_cppcc", "副主席", "待查", "present", "副厅级", ""),
    ("shunyi_shi_weidong", "org_shunyi_cppcc", "副主席", "待查", "present", "副厅级", ""),
    ("shunyi_yang_fenghui", "org_shunyi_cppcc", "副主席（不驻会）", "待查", "present", "副厅级", "不驻会"),
    ("shunyi_yu_baoxin", "org_shunyi_cppcc", "副主席（不驻会）", "待查", "present", "副厅级", "不驻会"),
    ("shunyi_guo_yuhao", "org_shunyi_cppcc", "副主席（不驻会）", "待查", "present", "副厅级", "不驻会"),
]

# Relationships — these are inferred from shared organizational membership
# Strong relationships: top leaders working together in the same district government
RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period, confidence, strength

    # Top leader pairings
    ("shunyi_gong_zongyuan", "shunyi_cui_xiaohao", "overlap",
     "区委书记与区长在顺义区委区政府班子中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    # Party committee standing members
    ("shunyi_gong_zongyuan", "shunyi_wu_xiaojun", "overlap",
     "区委书记与副书记在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_wu_xiaojun", "overlap",
     "区长与副书记在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_song_peng", "overlap",
     "区委书记与常委在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_ma_hongping", "overlap",
     "区委书记与常委在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_li_xin", "overlap",
     "区委书记与常委副区长在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_geng_xiaojing", "overlap",
     "区委书记与常委在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_zhang_yitao", "overlap",
     "区委书记与常委在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    ("shunyi_gong_zongyuan", "shunyi_liu_yongjun", "overlap",
     "区委书记与常委在区委常委会中共事", "org_shunyi_party", "待查–present",
     "confirmed", "strong"),

    # Government team overlaps
    ("shunyi_cui_xiaohao", "shunyi_dong_chenggang", "overlap",
     "区长与副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_huang_yongzhi", "overlap",
     "区长与副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_hou_ying", "overlap",
     "区长与副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_zhou_xin", "overlap",
     "区长与副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_wang_ke", "overlap",
     "区长与副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "strong"),

    ("shunyi_cui_xiaohao", "shunyi_li_baojie", "overlap",
     "区长与挂职副区长在区政府班子中共事", "org_shunyi_gov", "待查–present",
     "confirmed", "medium"),
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def build_db(db_path):
    """Create SQLite database from hardcoded data."""
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute("""
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
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
            confidence TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    c.executemany(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        PERSONS
    )
    c.executemany(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
        ORGANIZATIONS
    )
    c.executemany(
        "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
        POSITIONS
    )
    c.executemany(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence, strength) VALUES (?,?,?,?,?,?,?,?)",
        RELATIONSHIPS
    )

    conn.commit()
    conn.close()
    print(f"  ✓ Database created: {db_path}")
    print(f"    - {len(PERSONS)} persons")
    print(f"    - {len(ORGANIZATIONS)} organizations")
    print(f"    - {len(POSITIONS)} positions")
    print(f"    - {len(RELATIONSHIPS)} relationships")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' string based on role."""
    title = p[9]  # current_post
    if "书记" in title and "副" not in title:
        return "255,50,50"  # Red for party secretary
    if "区长" in title and ("副" not in title or "常务" in title):
        if "副" in title and "常务" not in title:
            return "50,100,255"  # Blue for deputy
        return "50,100,255"  # Blue for district mayor
    if "主任" in title and ("副" not in title):
        if "人大" in title:
            return "50,100,255"
        return "100,100,100"
    if "主席" in title and ("副" not in title):
        if "政协" in title:
            return "100,100,100"
        return "100,100,100"
    if "纪委" in title or "纪律" in title:
        return "255,165,0"  # Orange for discipline
    return "100,100,100"  # Grey for others


def is_top_leader(p):
    """Check if person is a top leader (书记 or 区长/县长)."""
    title = p[9]
    if ("书记" in title and "副" not in title and "副书记" not in title):
        return True
    if ("区长" in title or "县长" in title or "市长" in title or "长" in title) and "副" not in title:
        return True
    return False


def org_color(org_type):
    """Return color for organization by type."""
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇": "255,255,200",
        "事业单位": "220,220,220",
        "群团": "255,220,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def build_gexf(gexf_path):
    """Generate GEXF 1.3 graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>北京市顺义区领导班子工作关系网络 - 顺义区 leadership relationship network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('      <attribute id="3" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes ──
    lines.append('    <nodes>')

    # Person nodes
    for p in PERSONS:
        pid = f"p_{p[0]}"
        name = p[1]
        title = p[9]
        org = p[10]
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"

        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = f"o_{o[0]}"
        oname = o[1]
        otype = o[2]
        c = org_color(otype)

        lines.append(f'      <node id="{esc(oid)}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in POSITIONS:
        pid = f"p_{pos[0]}"
        oid = f"o_{pos[1]}"
        title = pos[2]
        lines.append(f'      <edge id="{eid}" source="{esc(pid)}" target="{esc(oid)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="confirmed"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationships), weight="2.0"
    for r in RELATIONSHIPS:
        pid_a = f"p_{r[0]}"
        pid_b = f"p_{r[1]}"
        rtype = r[2]
        context = r[3]
        confidence = r[6]
        strength = r[7]

        w = "2.0" if strength == "strong" else "1.5" if strength == "medium" else "1.0"
        lines.append(f'      <edge id="{eid}" source="{esc(pid_a)}" target="{esc(pid_b)}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(confidence)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(strength)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(gexf_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  ✓ GEXF graph created: {gexf_path}")
    print(f"    - {len(PERSONS) + len(ORGANIZATIONS)} nodes")
    print(f"    - {len(POSITIONS) + len(RELATIONSHIPS)} edges")


def main():
    print("=" * 60)
    print("北京市顺义区领导班子工作关系网络 — 数据构建")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("\n[1/2] Building SQLite database...")
    build_db(DB_PATH)

    print("\n[2/2] Building GEXF graph...")
    build_gexf(GEXF_PATH)

    print("\n" + "=" * 60)
    print("Done! Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"\nStatistics:")
    print(f"  Persons:         {len(PERSONS)}")
    print(f"  Organizations:   {len(ORGANIZATIONS)}")
    print(f"  Positions:       {len(POSITIONS)}")
    print(f"  Relationships:   {len(RELATIONSHIPS)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
