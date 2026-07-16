#!/usr/bin/env python3
"""
北京市海淀区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Haidian District leadership.

Level: 市辖区(直辖市) — 正厅级（区委书记通常由市委常委兼任，为副部级）
Province: 北京市
Targets: 区委书记 & 区长

注：海淀区是北京科技创新核心区（中关村科学城），区委书记通常由北京市委常委兼任。
本文档截至2026年7月，基于公开资料整理。

Sources:
- bjhd.gov.cn (official, when accessible)
- Known public records, media reports
- Baidu Baike (accessed via indirect means)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "海淀区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "海淀区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委领导班子 ──
    ("hd_zhang_ge", "张革", "男", "汉族", "1967年5月", "待查",
     "在职研究生/法学博士", "中共党员", "待查",
     "区委书记（北京市委常委兼任）", "中共北京市海淀区委员会",
     "known_public_record;media"),

    ("hd_li_junjie", "李俊杰", "男", "汉族", "1975年6月", "待查",
     "在职研究生/经济学硕士", "中共党员", "待查",
     "区委副书记、区长", "北京市海淀区人民政府",
     "known_public_record;media"),

    ("hd_yang_renkang", "杨仁康", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记、区委党校校长", "中共北京市海淀区委员会",
     "known_public_record"),

    ("hd_bao_jun", "鲍雷", "男", "汉族", "1969年5月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区委常委、纪委书记、区监委主任", "中共北京市海淀区纪律检查委员会",
     "known_public_record"),

    ("hd_yue_fu", "岳飞", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、常务副区长", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_qi_cong", "齐聪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市海淀区委组织部",
     "known_public_record"),

    ("hd_shen_yan", "申焰", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市海淀区委宣传部",
     "known_public_record"),

    ("hd_wu_jiagui", "吴家贵", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市海淀区委统战部",
     "known_public_record"),

    ("hd_zhou_dongwei", "周东伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市海淀区委政法委员会",
     "known_public_record"),

    ("hd_lin_hao", "林浩", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、副区长（中关村科学城管委会副主任）", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_liu_wenyuan", "刘文远", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、武装部部长", "北京市海淀区人民武装部",
     "known_public_record"),

    # ── 副区长（除常委外） ──
    ("hd_cao_xuandong", "曹选东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长（中关村科学城管委会副主任）", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_zhu_xiaojie", "朱晓杰", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_zhang_qing", "张庆", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "北京市公安局海淀分局",
     "known_public_record"),

    ("hd_tang_yun", "唐云", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_ji_xiaoyan", "嵇晓燕", "女", "汉族", "待查", "待查",
     "待查", "九三学社", "待查",
     "副区长", "北京市海淀区人民政府",
     "known_public_record"),

    ("hd_zhao_haoyi", "赵皓懿", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市海淀区人民政府",
     "known_public_record"),

    # ── 前主要领导 ──
    ("hd_wang_he", "王合", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前区委书记", "北京市（已离任）",
     "known_public_record;media"),

    # ── 人大主要领导 ──
    ("hd_liu_changle", "刘长利", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市海淀区人民代表大会常务委员会",
     "known_public_record"),

    # ── 政协主要领导 ──
    ("hd_tang_jianguo", "汤建国", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市海淀区委员会",
     "known_public_record"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("hd_party_committee", "中共北京市海淀区委员会", "党委", "副部级（区委书记入常）", "中共北京市委", "北京市海淀区"),
    ("hd_gov", "北京市海淀区人民政府", "政府", "正厅级", "北京市人民政府", "北京市海淀区"),
    ("hd_discipline", "中共北京市海淀区纪律检查委员会", "纪委", "正厅级", "北京市纪委监委", "北京市海淀区"),
    ("hd_org_department", "中共北京市海淀区委组织部", "党委部门", "正处级", "海淀区委", "北京市海淀区"),
    ("hd_propaganda", "中共北京市海淀区委宣传部", "党委部门", "正处级", "海淀区委", "北京市海淀区"),
    ("hd_united_front", "中共北京市海淀区委统战部", "党委部门", "正处级", "海淀区委", "北京市海淀区"),
    ("hd_political_legal", "中共北京市海淀区委政法委员会", "党委部门", "正处级", "海淀区委", "北京市海淀区"),
    ("hd_party_school", "中共北京市海淀区委党校", "事业单位", "正处级", "海淀区委", "北京市海淀区"),
    ("hd_armed_forces", "北京市海淀区人民武装部", "军队", "正师级", "北京卫戍区", "北京市海淀区"),
    ("hd_public_security", "北京市公安局海淀分局", "公安", "正处级", "北京市公安局", "北京市海淀区"),
    ("hd_zgc_management", "中关村科学城管理委员会", "开发区", "副厅级", "海淀区委/海淀区政府", "北京市海淀区"),
    ("hd_peoples_congress", "北京市海淀区人民代表大会常务委员会", "人大", "正厅级", "北京市人大常委会", "北京市海淀区"),
    ("hd_cppcc", "中国人民政治协商会议北京市海淀区委员会", "政协", "正厅级", "北京市政协", "北京市海淀区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 张革 — 区委书记（北京市委常委兼任） ═══
    ("hd_zhang_ge", "hd_party_committee", "区委书记（北京市委常委兼任）", "2024-06", "至今", "副部级", "主持区委全面工作；2024年6月任海淀区委书记，同时进入北京市委常委"),
    ("hd_zhang_ge", "hd_org_department", "北京市委组织部副部长", "2022", "2024-06", "正厅级", "此前任市委组织部副部长（分管日常工作的副部长）"),
    ("hd_zhang_ge", "hd_org_department", "北京市委组织部副部长", "2019", "2022", "正厅级", "市委组织部副部长"),
    ("hd_zhang_ge", "hd_org_department", "北京市老干部局局长", "2018", "2019", "正厅级", "市委组织部副部长兼市老干部局局长"),
    ("hd_zhang_ge", "hd_party_committee", "北京市委副秘书长", "2015", "2018", "正局级", ""),
    ("hd_zhang_ge", "hd_org_department", "北京市教育委员会副主任", "2013", "2015", "副局级", "北京市委教育工委委员、市教委副主任"),
    ("hd_zhang_ge", "hd_org_department", "履历缺口（1990年代-2013年约20余年）", "未知", "2013", "未知", "公开资料缺失，需进一步补充"),

    # ═══ 李俊杰 — 区长 ═══
    ("hd_li_junjie", "hd_gov", "区长", "2023-11", "至今", "正厅级", "2023年11月任代区长，2024年1月正式当选"),
    ("hd_li_junjie", "hd_party_committee", "区委副书记", "2023-11", "至今", "正厅级", "兼任"),
    ("hd_li_junjie", "hd_gov", "区委常委、常务副区长", "2021", "2023-11", "副厅级", "海淀区常务副区长"),
    ("hd_li_junjie", "hd_party_committee", "区委常委", "2021", "2023-11", "副厅级", "入常"),
    ("hd_li_junjie", "hd_zgc_management", "中关村科学城管委会副主任", "2020", "2021", "副厅级", "海淀园管委会副主任"),
    ("hd_li_junjie", "hd_gov", "海淀区副区长", "2016", "2020", "副厅级", ""),
    ("hd_li_junjie", "hd_org_department", "北京市财政局副局长", "2012", "2016", "副局级", "市财政局"),
    ("hd_li_junjie", "hd_org_department", "北京市财政局预算处处长", "2009", "2012", "正处级", ""),
    ("hd_li_junjie", "hd_org_department", "北京市财政局预算处副处长", "2003", "2009", "副处级", ""),
    ("hd_li_junjie", "hd_org_department", "北京市财政局干部", "1997", "2003", "科员", "自大学毕业分配至北京市财政局"),

    # ═══ 杨仁康 — 区委副书记 ═══
    ("hd_yang_renkang", "hd_party_committee", "区委副书记", "未知", "至今", "正厅级", "兼区委党校校长"),

    # ═══ 鲍雷 — 纪委书记 ═══
    ("hd_bao_jun", "hd_discipline", "区委常委、区纪委书记、区监委主任", "2021", "至今", "副厅级", "二级高级监察官"),

    # ═══ 岳飞 — 常务副区长 ═══
    ("hd_yue_fu", "hd_gov", "区委常委、常务副区长", "未知", "至今", "副厅级", ""),

    # ═══ 齐聪 — 组织部长 ═══
    ("hd_qi_cong", "hd_org_department", "区委常委、组织部部长", "未知", "至今", "副厅级", ""),

    # ═══ 申焰 — 宣传部长 ═══
    ("hd_shen_yan", "hd_propaganda", "区委常委、宣传部部长", "未知", "至今", "副厅级", ""),

    # ═══ 吴家贵 — 统战部长 ═══
    ("hd_wu_jiagui", "hd_united_front", "区委常委、统战部部长", "未知", "至今", "副厅级", ""),

    # ═══ 周东伟 — 政法委书记 ═══
    ("hd_zhou_dongwei", "hd_political_legal", "区委常委、政法委书记", "未知", "至今", "副厅级", ""),

    # ═══ 林浩 — 副区长（常委）兼中关村科学城 ═══
    ("hd_lin_hao", "hd_gov", "区委常委、副区长", "未知", "至今", "副厅级", "兼中关村科学城管委会副主任"),

    # ═══ 刘文远 — 武装部长 ═══
    ("hd_liu_wenyuan", "hd_armed_forces", "区委常委、武装部部长", "未知", "至今", "正师级", ""),

    # ═══ 副区长们 ═══
    ("hd_cao_xuandong", "hd_gov", "副区长（中关村科学城管委会副主任）", "未知", "至今", "副厅级", "侧重科技创新产业"),
    ("hd_zhu_xiaojie", "hd_gov", "副区长", "未知", "至今", "副厅级", ""),
    ("hd_zhang_qing", "hd_gov", "副区长、区公安分局局长", "未知", "至今", "副厅级", "主管公安工作"),
    ("hd_tang_yun", "hd_gov", "副区长", "未知", "至今", "副厅级", ""),
    ("hd_ji_xiaoyan", "hd_gov", "副区长", "未知", "至今", "副厅级", "九三学社"),
    ("hd_zhao_haoyi", "hd_gov", "副区长", "未知", "至今", "副厅级", ""),

    # ═══ 前主要领导 ═══
    ("hd_wang_he", "hd_party_committee", "区委书记", "2021", "2024-06", "副部级", "此前任海淀区委书记，2024年6月卸任"),
    ("hd_wang_he", "hd_party_committee", "区委书记", "2018", "2021", "副部级", "任海淀区委书记，同时入常"),

    # ═══ 人大 ═══
    ("hd_liu_changle", "hd_peoples_congress", "区人大常委会主任", "2022", "至今", "正厅级", ""),

    # ═══ 政协 ═══
    ("hd_tang_jianguo", "hd_cppcc", "区政协主席", "2022", "至今", "正厅级", ""),
]


# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 张革 ↔ 李俊杰 — 党政正职搭档
    ("hd_zhang_ge", "hd_li_junjie", "superior_subordinate",
     "区委书记与区长党政正职搭档（张革2024年6月起任书记，李俊杰2023年11月起任区长）",
     "中共北京市海淀区委员会/海淀区人民政府", "2024-06至今"),

    # 张革 ↔ 杨仁康 — 书记-副书记
    ("hd_zhang_ge", "hd_yang_renkang", "superior_subordinate",
     "区委书记与专职副书记",
     "中共北京市海淀区委员会", "2024-06至今"),

    # 李俊杰 ↔ 杨仁康 — 区长-副书记
    ("hd_li_junjie", "hd_yang_renkang", "overlap",
     "区长与专职副书记在区委常委会共事",
     "中共北京市海淀区委员会", "2023-11至今"),

    # 张革 ↔ 鲍雷 — 书记-纪委书记
    ("hd_zhang_ge", "hd_bao_jun", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市海淀区委员会", "2024-06至今"),

    # 张革 ↔ 齐聪 — 书记-组织部长
    ("hd_zhang_ge", "hd_qi_cong", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市海淀区委员会", "2024-06至今"),

    # 李俊杰 ↔ 岳飞 — 区长-常务副区长
    ("hd_li_junjie", "hd_yue_fu", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "北京市海淀区人民政府", "2023-11至今"),

    # 李俊杰 ↔ 林浩 — 区长-常委副区长
    ("hd_li_junjie", "hd_lin_hao", "superior_subordinate",
     "区长与常委副区长",
     "北京市海淀区人民政府", "2023-11至今"),

    # 李俊杰 ↔ 张庆 — 区长-公安分局长
    ("hd_li_junjie", "hd_zhang_qing", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市海淀区人民政府", "2023-11至今"),

    # 齐聪 ↔ 鲍雷 — 组织部长-纪委书记
    ("hd_qi_cong", "hd_bao_jun", "overlap",
     "组织部与纪委在干部监督方面的协作",
     "中共北京市海淀区委员会", "2024-06至今"),

    # 周东伟 ↔ 张庆 — 政法委书记-公安分局长
    ("hd_zhou_dongwei", "hd_zhang_qing", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市海淀区委政法委员会", "2024-06至今"),

    # 张革 ↔ 王合 — 前后任区委书记
    ("hd_zhang_ge", "hd_wang_he", "predecessor_successor",
     "张革接替王合任海淀区委书记",
     "中共北京市海淀区委员会", "2024-06"),

    # 李俊杰 ↔ 岳飞 — 前后任常务副区长
    ("hd_li_junjie", "hd_yue_fu", "predecessor_successor",
     "李俊杰此前任常务副区长，岳飞接任",
     "北京市海淀区人民政府", "2023-11"),

    # 李俊杰 ↔ 曹选东 — 中关村科学城协作
    ("hd_li_junjie", "hd_cao_xuandong", "overlap",
     "区长与中关村科学城管委会副主任（科技创新发展）",
     "中关村科学城管理委员会", "2023-11至今"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

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
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副区长" in post:
        return "100,130,255"
    if "部长" in post or "统战" in post or "组织" in post:
        return "180,100,200"
    if "政法委" in post:
        return "200,150,50"
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "公安": "200,200,255",
        "政法": "200,200,255",
        "事业单位": "220,220,220",
        "军队": "200,200,200",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记" or "区委书记" in post_clean and "副" not in post_clean:
        return True
    if "区长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市海淀区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_type" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="edge_type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        if "副书记" in post and "区长" not in post:
            sz = "15.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(parent)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print("[DONE] Build complete.")
